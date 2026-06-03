#!/usr/bin/env python3
"""
Test the proposed cascade fix by injecting it into the live page and
checking if --primary-text-color resolves to black at the Mudroom Light
text element.

Theory: CSS substitutes var() eagerly at the declaring scope, so the
:root-level `--primary-text-color: var(--lcars-primary-text)` declaration
was baked to WHITE at root time. Adding a card-level redeclaration of
--primary-text-color: var(--lcars-primary-text) should re-resolve it
to the locally-overridden BLACK value.
"""
from __future__ import annotations

import os
import time

from playwright.sync_api import sync_playwright

HA_URL = "https://ps2nfvpesdke44vv04irms1d3bym6rsj.ui.nabu.casa"
DASHBOARD_PATH = "/lovelace/home-flexible"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiI2YmM5NWI4NmUxZjA0ZjEzODI0NTZhMDM3YTQ2NGI3NCIsImlhdCI6MTc3OTIzNTYwNSwiZXhwIjoyMDk0NTk1NjA1fQ"
    ".QIgVN0W_lMHjlO_Vo7OxMO38i1htOKJepVR7iB711Wo"
)
TARGET = "Mudroom Light"


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

        # Function we'll call before and after the patch
        probe_js = """(TARGET) => {
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
            const el = findAll(document)[0];
            if (!el) return null;
            const cs = getComputedStyle(el);
            return {
                color: cs.color,
                lcarsPrimary: cs.getPropertyValue('--lcars-primary-text').trim(),
                primaryText: cs.getPropertyValue('--primary-text-color').trim(),
                lcarsQuatText: cs.getPropertyValue('--lcars-ui-quaternary-text').trim(),
            };
        }"""

        before = page.evaluate(probe_js, TARGET)
        print("BEFORE fix injection:")
        for k, v in before.items():
            print(f"  {k:<15} {v}")

        # Inject the proposed fix: walk to the host of the shadow root containing the target,
        # find its containing ha-card, and apply the cascade fix via a style attribute override.
        patch_result = page.evaluate(
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
                const el = findAll(document)[0];
                if (!el) return 'target not found';

                // Walk up composed tree, find the nearest hui-entities-card
                let n = el;
                while (n) {
                    if (n.localName === 'hui-entities-card') break;
                    const r = n.getRootNode();
                    n = n.parentElement || (r instanceof ShadowRoot ? r.host : null);
                }
                if (!n) return 'no hui-entities-card ancestor found';

                // Apply the fix as an inline style
                n.style.setProperty('--primary-text-color', 'var(--lcars-primary-text)');
                n.style.setProperty('--secondary-text-color', 'var(--lcars-secondary-text)');
                n.style.setProperty('--text-primary-color', 'var(--lcars-primary-text)');
                n.style.setProperty('--ha-card-header-color', 'var(--lcars-primary-text)');
                return 'patched ' + n.localName + ' (class=' + (n.className||'') + ')';
            }""",
            TARGET,
        )
        print(f"\nPatch: {patch_result}")

        after = page.evaluate(probe_js, TARGET)
        print("\nAFTER fix injection:")
        for k, v in after.items():
            print(f"  {k:<15} {v}")

        # Verdict
        print("\n=== VERDICT ===")
        if "0, 0, 0" in after["color"] or after["color"].lower() in ("#000000", "black"):
            print("FIX WORKS: text color resolved to black.")
        else:
            print(f"FIX DID NOT WORK: color is still {after['color']}.")
            print("Need to look at higher / earlier rules.")

        browser.close()


if __name__ == "__main__":
    main()
