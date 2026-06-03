#!/usr/bin/env python3
"""
Find the icon of an entity (e.g., "Mantel Light") and identify which CSS
variable / rule controls its color via CDP.
"""
from __future__ import annotations

import json
import os
import sys
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
TARGET = sys.argv[1] if len(sys.argv) > 1 else "Mantel Light"

OUT_DIR = Path(__file__).parent.parent / "docs" / "light-text-audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TRACKED = [
    "--state-icon-color",
    "--paper-item-icon-color",
    "--state-light-inactive-color",
    "--state-light-active-color",
    "--state-icon-active-color",
    "--state-inactive-color",
    "--state-active-color",
    "--state-light-off-color",
    "--rgb-disabled-color",
    "--disabled-text-color",
    "--lcars-primary-text",
    "--primary-text-color",
    "--primary-color",
    "--lcars-ui-tertiary",
    "--lcars-card-top-color",
    "--lcars-bluey",
    "--mdc-icon-button-icon-color",
    "color",
    "fill",
]


def main() -> None:
    os.environ.setdefault("PLAYWRIGHT_HOST_PLATFORM_OVERRIDE", "ubuntu24.04-x64")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()

        page.goto(HA_URL, wait_until="domcontentloaded")
        page.evaluate(
            """([t, u, e]) => localStorage.setItem('hassTokens', JSON.stringify({
                access_token: t, token_type: 'Bearer', expires_in: 315360000,
                expires_at: e, hassUrl: u, clientId: u + '/'
            }))""",
            [TOKEN, HA_URL, time.time() + 315360000],
        )

        page.goto(HA_URL + DASHBOARD_PATH, wait_until="domcontentloaded")
        page.wait_for_function("!location.pathname.startsWith('/auth/')", timeout=90_000)
        page.wait_for_function(
            "() => { const ha = document.querySelector('home-assistant'); return ha && ha.shadowRoot !== null; }",
            timeout=90_000,
        )
        time.sleep(7)

        # Find the row with TARGET text, then find the icon (ha-state-icon / ha-icon / state-badge)
        # in that row
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
                function findIconInRow(textEl) {
                    // walk up to hui-generic-entity-row or state-badge
                    let row = textEl;
                    while (row) {
                        if (row.localName === 'hui-generic-entity-row' ||
                            row.localName === 'hui-toggle-entity-row' ||
                            row.localName === 'hui-state-label-badge') break;
                        const r = row.getRootNode();
                        row = row.parentElement || (r instanceof ShadowRoot ? r.host : null);
                    }
                    if (!row) return null;
                    // walk into the row for ha-state-icon, then its child ha-svg-icon
                    function descend(node) {
                        if (!node) return null;
                        if (node.localName === 'ha-state-icon' || node.localName === 'ha-svg-icon' ||
                            node.localName === 'ha-icon' || node.localName === 'state-badge') return node;
                        const root = node.shadowRoot || node;
                        for (const ch of root.children || []) {
                            const f = descend(ch);
                            if (f) return f;
                        }
                        if (node.shadowRoot) {
                            for (const ch of node.shadowRoot.children) {
                                const f = descend(ch);
                                if (f) return f;
                            }
                        }
                        return null;
                    }
                    return descend(row);
                }
                const texts = findAll(document);
                if (!texts.length) return null;
                // For each candidate text element, try to find an icon sibling
                for (const t of texts) {
                    const icon = findIconInRow(t);
                    if (icon) return icon;
                }
                return null;
            }""",
            TARGET,
        )

        elem = elem_handle.as_element()
        if not elem:
            print(f"Could not find icon for {TARGET!r}")
            browser.close()
            return

        # Probe the icon's computed values & tag/path
        details = elem.evaluate(
            """(el) => {
                function getPath(n) {
                    const parts = [];
                    while (n && n.nodeType === 1) {
                        let s = n.localName;
                        if (n.id) s += '#' + n.id;
                        else if (n.className && typeof n.className === 'string') {
                            const c = n.className.trim().split(/\\s+/).slice(0, 2).join('.');
                            if (c) s += '.' + c;
                        }
                        parts.unshift(s);
                        const r = n.getRootNode();
                        n = n.parentElement || (r instanceof ShadowRoot ? r.host : null);
                    }
                    return parts.join(' > ');
                }
                const cs = getComputedStyle(el);
                return {
                    tag: el.localName,
                    path: getPath(el),
                    color: cs.color,
                    fill: cs.fill,
                };
            }"""
        )
        print(f"=== Icon for {TARGET!r} ===")
        print(f"  tag:  <{details['tag']}>")
        print(f"  path: {details['path']}")
        print(f"  color: {details['color']}")
        print(f"  fill:  {details['fill']}")

        # Mark the icon and walk up its composed ancestors via attrs for CDP
        page.evaluate(
            """(el) => {
                let n = el;
                let depth = 0;
                while (n && depth < 24) {
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

        cdp = ctx.new_cdp_session(page)
        cdp.send("DOM.enable")
        cdp.send("CSS.enable")
        cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})

        ancestor_nodes = []
        for depth in range(24):
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

        # Computed style at the icon
        target_computed = cdp.send("CSS.getComputedStyleForNode", {"nodeId": ancestor_nodes[0]})
        computed_map = {p["name"]: p["value"] for p in target_computed["computedStyle"]}
        print(f"\n=== Computed values at icon ===")
        for v in TRACKED:
            val = computed_map.get(v)
            if val and val.strip():
                print(f"  {v:<35} {val}")

        # Matched rules setting any TRACKED var across ancestors
        print(f"\n=== Matched rules setting icon-related vars ===\n")
        for depth, nid in enumerate(ancestor_nodes):
            try:
                ms = cdp.send("CSS.getMatchedStylesForNode", {"nodeId": nid})
            except Exception as e:
                continue
            desc = cdp.send("DOM.describeNode", {"nodeId": nid})
            node = desc["node"]
            tag = node.get("localName", "")
            attrs = node.get("attributes", [])
            attr_pairs = dict(zip(attrs[::2], attrs[1::2]))
            classes = attr_pairs.get("class", "")

            inline_rel = []
            for p in ms.get("inlineStyle", {}).get("cssProperties", []):
                if p.get("name") in TRACKED:
                    inline_rel.append(p)
            rules_rel = []
            for entry in ms.get("matchedCSSRules", []):
                rule = entry.get("rule", {})
                sel = ", ".join(s.get("text", "") for s in rule.get("selectorList", {}).get("selectors", []))
                origin = rule.get("origin", "")
                props = [p for p in rule.get("style", {}).get("cssProperties", []) if p.get("name") in TRACKED]
                if props:
                    rules_rel.append((sel, origin, props))

            if inline_rel or rules_rel:
                print(f"[{depth}] <{tag} class=\"{classes[:80]}\">")
                for p in inline_rel:
                    bang = " !important" if p.get("important") else ""
                    print(f"    INLINE: {p['name']}: {p.get('value','')}{bang}")
                for sel, origin, props in rules_rel:
                    print(f"    {origin:<10} {sel}")
                    for p in props:
                        bang = " !important" if p.get("important") else ""
                        dis = " [disabled]" if p.get("disabled") else ""
                        print(f"        {p['name']}: {p.get('value','')}{bang}{dis}")
                print()

        # Cleanup
        page.evaluate("""() => {
            document.querySelectorAll('[data-cdp-anc]').forEach(e => e.removeAttribute('data-cdp-anc'));
        }""")

        browser.close()


if __name__ == "__main__":
    main()
