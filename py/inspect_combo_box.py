#!/usr/bin/env python3
"""Trace the cascade for the span inside ha-combo-box-item for a given entity."""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

HA_URL = "https://ps2nfvpesdke44vv04irms1d3bym6rsj.ui.nabu.casa"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiI2YmM5NWI4NmUxZjA0ZjEzODI0NTZhMDM3YTQ2NGI3NCIsImlhdCI6MTc3OTIzNTYwNSwiZXhwIjoyMDk0NTk1NjA1fQ"
    ".QIgVN0W_lMHjlO_Vo7OxMO38i1htOKJepVR7iB711Wo"
)
TARGET = sys.argv[1] if len(sys.argv) > 1 else "Nursery Wake Up Light"

TRACKED = [
    "color",
    "opacity",
    "--primary-text-color",
    "--secondary-text-color",
    "--lcars-primary-text",
    "--lcars-secondary-text",
    "--text-primary-color",
    "--mdc-theme-on-surface",
    "--md-sys-color-on-surface",
    "--md-sys-color-on-surface-variant",
    "--md-comp-filled-field-content-color",
    "--md-filled-text-field-input-text-color",
    "--md-filled-select-input-text-color",
    "--mdc-select-ink-color",
    "--mdc-select-label-ink-color",
    "--mdc-text-field-ink-color",
    "--mdc-text-field-label-ink-color",
    "--ha-select-text-color",
    "--state-icon-color",
]


def main():
    os.environ.setdefault("PLAYWRIGHT_HOST_PLATFORM_OVERRIDE", "ubuntu24.04-x64")
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        ctx = b.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()
        page.goto(HA_URL, wait_until="domcontentloaded")
        page.evaluate(
            "([t,u,e])=>localStorage.setItem('hassTokens',JSON.stringify({access_token:t,token_type:'Bearer',expires_in:315360000,expires_at:e,hassUrl:u,clientId:u+'/'}))",
            [TOKEN, HA_URL, time.time() + 315360000],
        )
        page.goto(HA_URL + "/lovelace/home-flexible", wait_until="domcontentloaded")
        page.wait_for_function("!location.pathname.startsWith('/auth/')", timeout=90_000)
        page.wait_for_function(
            "()=>{const h=document.querySelector('home-assistant');return h&&h.shadowRoot!==null}",
            timeout=90_000,
        )
        time.sleep(7)

        elem = page.evaluate_handle(
            """(T) => {
                function findAll(root) {
                    const hits = [];
                    const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
                    let el;
                    while ((el = w.nextNode())) {
                        for (const ch of el.childNodes) {
                            if (ch.nodeType === 3 && ch.textContent.trim() === T) { hits.push(el); break; }
                        }
                        if (el.shadowRoot) hits.push(...findAll(el.shadowRoot));
                    }
                    return hits;
                }
                return findAll(document)[0] || null;
            }""",
            TARGET,
        )

        page.evaluate(
            """(el) => {
                let n = el; let d = 0;
                while (n && d < 20) {
                    if (n.nodeType === 1) { n.setAttribute('data-cdp-anc', String(d)); d++; }
                    const r = n.getRootNode();
                    n = n.parentElement || (r instanceof ShadowRoot ? r.host : null);
                }
            }""",
            elem,
        )

        cdp = ctx.new_cdp_session(page)
        cdp.send("DOM.enable")
        cdp.send("CSS.enable")
        cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})

        nodes = []
        for d in range(20):
            sr = cdp.send("DOM.performSearch", {"query": f"[data-cdp-anc='{d}']", "includeUserAgentShadowDOM": True})
            if sr["resultCount"] == 0: break
            ns = cdp.send("DOM.getSearchResults", {"searchId": sr["searchId"], "fromIndex": 0, "toIndex": sr["resultCount"]})
            nodes.append(ns["nodeIds"][-1])

        # Computed values at target
        cs = cdp.send("CSS.getComputedStyleForNode", {"nodeId": nodes[0]})
        cmap = {p["name"]: p["value"] for p in cs["computedStyle"]}
        print(f"=== Computed at {TARGET!r} span ===")
        for v in TRACKED:
            val = cmap.get(v)
            if val and val.strip():
                print(f"  {v:<45} {val}")

        # Matched rules per ancestor
        print(f"\n=== Matched rules setting TRACKED vars ===\n")
        for d, nid in enumerate(nodes):
            try:
                ms = cdp.send("CSS.getMatchedStylesForNode", {"nodeId": nid})
            except Exception:
                continue
            desc = cdp.send("DOM.describeNode", {"nodeId": nid})["node"]
            tag = desc.get("localName", "")
            attrs = dict(zip(desc.get("attributes", [])[::2], desc.get("attributes", [])[1::2]))
            cls = attrs.get("class", "")

            inline_rel = [p for p in ms.get("inlineStyle", {}).get("cssProperties", []) if p.get("name") in TRACKED]
            rules_rel = []
            for entry in ms.get("matchedCSSRules", []):
                rule = entry.get("rule", {})
                sel = ", ".join(s.get("text", "") for s in rule.get("selectorList", {}).get("selectors", []))
                origin = rule.get("origin", "")
                props = [p for p in rule.get("style", {}).get("cssProperties", []) if p.get("name") in TRACKED]
                if props:
                    rules_rel.append((sel, origin, props))

            if inline_rel or rules_rel:
                print(f"[{d}] <{tag} class=\"{cls[:70]}\">")
                for p in inline_rel:
                    print(f"    INLINE: {p['name']}: {p.get('value','')}{' !important' if p.get('important') else ''}")
                for sel, origin, props in rules_rel:
                    print(f"    {origin:<10} {sel}")
                    for p in props:
                        print(f"        {p['name']}: {p.get('value','')}{' !important' if p.get('important') else ''}{' [disabled]' if p.get('disabled') else ''}")
                print()

        page.evaluate("""() => document.querySelectorAll('[data-cdp-anc]').forEach(e => e.removeAttribute('data-cdp-anc'))""")
        b.close()


if __name__ == "__main__":
    main()
