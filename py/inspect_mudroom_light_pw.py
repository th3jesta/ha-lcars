#!/usr/bin/env python3
"""
Find "Mudroom Light" on the home-flexible dashboard and trace which CSS
rule is winning the cascade for --lcars-primary-text / --primary-text-color
via Chrome DevTools Protocol.

Requires:
    PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64

Usage:
    python3 py/inspect_mudroom_light_pw.py
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HA_URL = "https://ps2nfvpesdke44vv04irms1d3bym6rsj.ui.nabu.casa"
DASHBOARD_PATH = "/lovelace/home-flexible"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiI2YmM5NWI4NmUxZjA0ZjEzODI0NTZhMDM3YTQ2NGI3NCIsImlhdCI6MTc3OTIzNTYwNSwiZXhwIjoyMDk0NTk1NjA1fQ"
    ".QIgVN0W_lMHjlO_Vo7OxMO38i1htOKJepVR7iB711Wo"
)
TARGET_TEXT = "Mudroom Light"
TRACKED_VARS = (
    "--lcars-primary-text",
    "--primary-text-color",
    "--lcars-ui-quaternary-text",
)

OUT_DIR = Path(__file__).parent.parent / "docs" / "light-text-audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def find_target_nodeid(page, cdp) -> int | None:
    """Locate the deepest element whose direct text == TARGET, return its CDP backend nodeId.

    We use JS to find it (handles shadow DOM), then resolve to a CDP nodeId via
    DOM.requestNode after pushing it into the inspector.
    """
    handle = page.evaluate_handle(
        """(TARGET) => {
            function findAll(root) {
                const hits = [];
                const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
                let el;
                while ((el = w.nextNode())) {
                    for (const ch of el.childNodes) {
                        if (ch.nodeType === 3 && ch.textContent.trim() === TARGET) {
                            hits.push(el);
                            break;
                        }
                    }
                    if (el.shadowRoot) hits.push(...findAll(el.shadowRoot));
                }
                return hits;
            }
            const all = findAll(document);
            return all[0] || null;
        }""",
        TARGET_TEXT,
    )

    # Convert JSHandle into a CDP nodeId
    object_id = handle.evaluate_handle("e => e").json_value if False else None
    # Use Playwright's underlying object ID
    remote_object = handle._impl_obj._channel._object._remote_object  # type: ignore[attr-defined]
    # Simpler: use page.evaluate with element handle conversion via CDP.DOM.requestNode
    elem = handle.as_element()
    if not elem:
        return None
    desc = cdp.send("DOM.describeNode", {"objectId": elem._impl_obj._guid})  # may fail
    return desc.get("node", {}).get("nodeId")


def matched_rules_for_node(cdp, node_id: int) -> dict:
    """Fetch CSS.getMatchedStylesForNode for a node and return condensed info."""
    res = cdp.send("CSS.getMatchedStylesForNode", {"nodeId": node_id})
    # inline + matched rules
    summary = {
        "inline": [],
        "rules": [],   # list of {selector, origin, source, properties}
    }
    inline = res.get("inlineStyle", {})
    for p in inline.get("cssProperties", []):
        summary["inline"].append({
            "name": p["name"],
            "value": p.get("value", ""),
            "important": p.get("important", False),
        })
    for entry in res.get("matchedCSSRules", []):
        rule = entry.get("rule", {})
        sel = ", ".join(s.get("text", "") for s in rule.get("selectorList", {}).get("selectors", []))
        origin = rule.get("origin", "")
        style = rule.get("style", {})
        props = []
        for p in style.get("cssProperties", []):
            if "name" not in p:
                continue
            props.append({
                "name": p["name"],
                "value": p.get("value", ""),
                "important": p.get("important", False),
                "disabled": p.get("disabled", False),
            })
        summary["rules"].append({
            "selector": sel,
            "origin": origin,
            "properties": props,
        })
    return summary


def main() -> None:
    if os.environ.get("PLAYWRIGHT_HOST_PLATFORM_OVERRIDE") != "ubuntu24.04-x64":
        os.environ["PLAYWRIGHT_HOST_PLATFORM_OVERRIDE"] = "ubuntu24.04-x64"

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()

        print("Seeding auth token...")
        page.goto(HA_URL, wait_until="domcontentloaded")
        page.evaluate(
            """([token, hassUrl, expiresAt]) => {
                localStorage.setItem('hassTokens', JSON.stringify({
                    access_token: token, token_type: 'Bearer',
                    expires_in: 315360000, expires_at: expiresAt,
                    hassUrl, clientId: hassUrl + '/',
                }));
            }""",
            [TOKEN, HA_URL, time.time() + 315360000],
        )

        print(f"Loading {HA_URL}{DASHBOARD_PATH} ...")
        page.goto(HA_URL + DASHBOARD_PATH, wait_until="domcontentloaded")
        page.wait_for_function("!location.pathname.startsWith('/auth/')", timeout=90_000)
        page.wait_for_function(
            "() => { const ha = document.querySelector('home-assistant'); return ha && ha.shadowRoot !== null; }",
            timeout=90_000,
        )
        print("Letting theme apply (7s)...")
        time.sleep(7)

        cdp = ctx.new_cdp_session(page)
        cdp.send("DOM.enable")
        cdp.send("CSS.enable")

        # Get root document to enable nodeId enumeration
        cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})

        # Find the target element via JS, return a JSHandle, then ask CDP for its nodeId
        elem_handle = page.evaluate_handle(
            """(TARGET) => {
                function findAll(root) {
                    const hits = [];
                    const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
                    let el;
                    while ((el = w.nextNode())) {
                        for (const ch of el.childNodes) {
                            if (ch.nodeType === 3 && ch.textContent.trim() === TARGET) {
                                hits.push(el); break;
                            }
                        }
                        if (el.shadowRoot) hits.push(...findAll(el.shadowRoot));
                    }
                    return hits;
                }
                return findAll(document)[0] || null;
            }""",
            TARGET_TEXT,
        )

        # Use CDP runtime to get the remote object ID from the JSHandle
        # Playwright JSHandle has _guid which maps to a Channel; we need the
        # underlying remote object. The clean way is JSHandle._impl_obj._channel._object._remoteObject
        # but that's brittle. Instead, use page.evaluate to inject a marker attr,
        # then DOM.querySelector to find it from CDP.
        page.evaluate(
            """(el) => { el.setAttribute('data-cdp-pick', 'mudroom-target'); }""",
            elem_handle,
        )

        # Now use DOM.performSearch to find it through the shadow piercing
        search_result = cdp.send("DOM.performSearch", {
            "query": "[data-cdp-pick='mudroom-target']",
            "includeUserAgentShadowDOM": True,
        })
        search_id = search_result["searchId"]
        count = search_result["resultCount"]
        print(f"CDP search found {count} matching nodes")

        if count == 0:
            print("Target element not found via CDP search.")
            browser.close()
            return

        nodes = cdp.send("DOM.getSearchResults", {
            "searchId": search_id,
            "fromIndex": 0,
            "toIndex": count,
        })
        node_ids = nodes["nodeIds"]
        target_id = node_ids[-1]  # deepest match wins for nested cases

        # Walk up the composed tree via DOM.getDocument flat tree + parentId
        # But it's easier to just collect ancestor nodeIds via JS into attributes
        page.evaluate(
            """(el) => {
                let n = el;
                let depth = 0;
                while (n && depth < 14) {
                    if (n.nodeType === 1) {
                        n.setAttribute('data-cdp-anc', String(depth));
                        depth++;
                    }
                    const r = n.getRootNode();
                    n = n.parentElement || (r instanceof ShadowRoot ? r.host : null);
                }
            }""",
            elem_handle,
        )

        ancestor_nodes = []
        for depth in range(14):
            sr = cdp.send("DOM.performSearch", {
                "query": f"[data-cdp-anc='{depth}']",
                "includeUserAgentShadowDOM": True,
            })
            if sr["resultCount"] == 0:
                break
            ns = cdp.send("DOM.getSearchResults", {
                "searchId": sr["searchId"],
                "fromIndex": 0,
                "toIndex": sr["resultCount"],
            })
            ancestor_nodes.append(ns["nodeIds"][-1])

        print(f"\nCollected {len(ancestor_nodes)} ancestor nodes (composed tree).")

        # Get target computed style for the tracked vars
        target_computed = cdp.send("CSS.getComputedStyleForNode", {"nodeId": ancestor_nodes[0]})
        computed_map = {p["name"]: p["value"] for p in target_computed["computedStyle"]}
        print(f"\n=== Target: {TARGET_TEXT} ===")
        print(f"color (resolved):                  {computed_map.get('color')}")
        for v in TRACKED_VARS:
            print(f"{v:<35} {computed_map.get(v, '[unset]')}")

        # For each ancestor, get the matched rules and filter to TRACKED_VARS only
        print(f"\n=== Matched rules setting tracked vars (winning rule first) ===\n")
        full_report = []
        for depth, nid in enumerate(ancestor_nodes):
            try:
                ms = matched_rules_for_node(cdp, nid)
            except Exception as e:
                print(f"  [{depth}] nodeId={nid}: error {e}")
                continue

            relevant_rules = []
            for rule in ms["rules"]:
                relevant_props = [p for p in rule["properties"] if p["name"] in TRACKED_VARS]
                if relevant_props:
                    relevant_rules.append({
                        "selector": rule["selector"],
                        "origin": rule["origin"],
                        "props": relevant_props,
                    })
            relevant_inline = [p for p in ms["inline"] if p["name"] in TRACKED_VARS]

            # Get the element's tag/classes for context
            desc = cdp.send("DOM.describeNode", {"nodeId": nid})
            node = desc["node"]
            tag = node.get("localName", "")
            attrs = node.get("attributes", [])
            attr_pairs = dict(zip(attrs[::2], attrs[1::2]))
            classes = attr_pairs.get("class", "")

            if relevant_rules or relevant_inline:
                print(f"[{depth}] <{tag} class=\"{classes[:80]}\">")
                if relevant_inline:
                    for p in relevant_inline:
                        bang = " !important" if p["important"] else ""
                        print(f"    INLINE: {p['name']}: {p['value']}{bang}")
                for r in relevant_rules:
                    print(f"    {r['origin']:<10} {r['selector']}")
                    for p in r["props"]:
                        bang = " !important" if p["important"] else ""
                        dis = " [disabled]" if p["disabled"] else ""
                        print(f"        {p['name']}: {p['value']}{bang}{dis}")
                print()

            full_report.append({
                "depth": depth,
                "tag": tag,
                "classes": classes,
                "inline": relevant_inline,
                "rules": relevant_rules,
            })

        (OUT_DIR / "mudroom-cdp-trace.json").write_text(json.dumps({
            "target_computed": {k: computed_map.get(k) for k in [*TRACKED_VARS, "color"]},
            "ancestors": full_report,
        }, indent=2))
        print(f"\nFull CDP trace: {OUT_DIR / 'mudroom-cdp-trace.json'}")

        # Cleanup
        page.evaluate("""() => {
            document.querySelectorAll('[data-cdp-pick],[data-cdp-anc]').forEach(e => {
                e.removeAttribute('data-cdp-pick');
                e.removeAttribute('data-cdp-anc');
            });
        }""")

        browser.close()


if __name__ == "__main__":
    main()
