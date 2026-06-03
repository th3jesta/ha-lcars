#!/usr/bin/env python3
"""
Crawl /config sub-pages, find mdc-data-table elements with dark backgrounds,
and emit card-mod selector chains (with `$` shadow-root piercing) that point
at each one. Use these selectors to scope an override that keeps the text
light on dark data tables while the panel-wide --lcars-primary-text is set
to a dark color for cards.

Usage:
    python3 py/find_dark_data_tables.py
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HA_URL = "https://ps2nfvpesdke44vv04irms1d3bym6rsj.ui.nabu.casa"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiI2YmM5NWI4NmUxZjA0ZjEzODI0NTZhMDM3YTQ2NGI3NCIsImlhdCI6MTc3OTIzNTYwNSwiZXhwIjoyMDk0NTk1NjA1fQ"
    ".QIgVN0W_lMHjlO_Vo7OxMO38i1htOKJepVR7iB711Wo"
)

OUT_DIR = Path(__file__).parent.parent / "docs" / "data-table-audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Settings sub-panels to crawl. Excludes pages that need special setup
# (dialogs, editors with unsaved warnings, etc.).
CONFIG_PATHS = [
    "/config",
    "/config/dashboard",
    "/config/integrations",
    "/config/devices",
    "/config/devices/dashboard",
    "/config/entities",
    "/config/areas",
    "/config/labels",
    "/config/automation",
    "/config/automation/dashboard",
    "/config/script",
    "/config/script/dashboard",
    "/config/scene",
    "/config/scene/dashboard",
    "/config/blueprint",
    "/config/blueprint/dashboard",
    "/config/helpers",
    "/config/hardware",
    "/config/hardware/overview",
    "/config/network",
    "/config/storage",
    "/config/general",
    "/config/system_health",
    "/config/info",
    "/config/logs",
    "/config/repairs",
    "/config/updates",
    "/config/users",
    "/config/zone",
    "/config/person",
    "/config/voice-assistants",
    "/config/voice-assistants/expose",
    "/config/voice-assistants/assistants",
    "/config/lovelace/dashboards",
    "/config/lovelace/resources",
    "/config/tags",
    "/config/cloud",
    "/config/core",
    "/config/server_control",
    "/config/url",
    "/config/auth_provider",
    "/config/customize",
    "/config/devices/dashboard?historyBack=1",
]


# JS that walks the document including shadow roots, finds mdc-data-table*
# elements, captures their computed background, and emits a card-mod selector
# chain (using $ to pierce each shadow boundary).
SCAN_JS = r"""
() => {
    function rgbToLuma(rgb) {
        // Parse "rgb(r, g, b)" or "rgba(r, g, b, a)" — return relative luma
        const m = rgb.match(/(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)/);
        if (!m) return null;
        const [r, g, b] = [+m[1], +m[2], +m[3]];
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }

    function isTransparent(rgb) {
        if (!rgb) return true;
        const m = rgb.match(/rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*([0-9.]+)\s*)?\)/);
        if (m && m[1] !== undefined && parseFloat(m[1]) === 0) return true;
        return rgb === "transparent";
    }

    /**
     * Build a card-mod-style selector chain that pierces shadow boundaries
     * with `$`. Starts from <html> and walks down to `target`. Inside a single
     * shadow tree we collapse parent chains into a single CSS selector for
     * the target (or its closest stable ancestor) and emit `$` whenever we
     * cross a shadow boundary into a custom element host.
     */
    function buildShadowSelector(target) {
        // Walk up composed tree, splitting into segments at each shadow boundary
        const segments = [];   // each entry: { host: <element-or-null>, lastInTree: <element> }
        let n = target;
        let lastInTree = target;
        while (n) {
            const root = n.getRootNode();
            const parent = n.parentElement;
            if (parent) {
                lastInTree = parent;
                n = parent;
            } else if (root instanceof ShadowRoot) {
                // We're at the top of this shadow tree.
                segments.unshift({ host: root.host, lastInTree });
                n = root.host;
                lastInTree = root.host;
            } else {
                // Top of document
                segments.unshift({ host: null, lastInTree });
                break;
            }
        }

        // Build human-readable segments
        // For each segment except the last (where the target lives), we just need
        // the host tag name. For the last segment, we describe the target.
        const parts = [];
        for (let i = 0; i < segments.length; i++) {
            const seg = segments[i];
            if (seg.host) {
                // Use the host element's local name
                parts.push(seg.host.localName);
            }
        }

        // Describe the target (last segment)
        function describe(el) {
            let s = el.localName;
            if (el.classList && el.classList.length) {
                const c = [...el.classList].filter(c => !c.startsWith("style-scope")).slice(0, 2).join(".");
                if (c) s += "." + c;
            }
            return s;
        }

        const targetDesc = describe(target);
        // Chain segments with " $ " between them (card-mod shadow pierce)
        const chain = parts.length > 0
            ? parts.join(" $ ") + " $ " + targetDesc
            : targetDesc;
        return chain;
    }

    const out = [];
    function walk(root) {
        const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
        let el;
        while ((el = w.nextNode())) {
            const cls = el.className && typeof el.className === "string" ? el.className : "";
            // Match the .mdc-data-table root, common dark surfaces
            const isDataTable =
                /\bmdc-data-table\b/.test(cls) ||
                el.localName === "ha-data-table";

            if (isDataTable) {
                const cs = getComputedStyle(el);
                const bg = cs.backgroundColor;
                const luma = rgbToLuma(bg);
                const dark = !isTransparent(bg) && luma !== null && luma < 60;

                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    const sel = buildShadowSelector(el);
                    out.push({
                        tag: el.localName,
                        cls: cls.trim().slice(0, 120),
                        bg,
                        luma,
                        dark,
                        selector: sel,
                    });
                }
            }
            if (el.shadowRoot) walk(el.shadowRoot);
        }
    }
    walk(document);
    return out;
}
"""


def main() -> None:
    os.environ.setdefault("PLAYWRIGHT_HOST_PLATFORM_OVERRIDE", "ubuntu24.04-x64")

    findings: dict[str, list[dict]] = {}

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()

        # Seed auth once
        page.goto(HA_URL, wait_until="domcontentloaded")
        page.evaluate(
            """([t, u, e]) => localStorage.setItem('hassTokens', JSON.stringify({
                access_token: t, token_type: 'Bearer', expires_in: 315360000,
                expires_at: e, hassUrl: u, clientId: u + '/'
            }))""",
            [TOKEN, HA_URL, time.time() + 315360000],
        )

        for path in CONFIG_PATHS:
            url = HA_URL + path
            try:
                print(f"\nScanning {path} ...")
                page.goto(url, wait_until="domcontentloaded", timeout=45_000)
                page.wait_for_function(
                    "() => !location.pathname.startsWith('/auth/')",
                    timeout=30_000,
                )
                page.wait_for_function(
                    "() => { const ha = document.querySelector('home-assistant'); return ha && ha.shadowRoot !== null; }",
                    timeout=30_000,
                )
                time.sleep(5)  # let theme + tabs render
            except Exception as e:
                print(f"  [skip] {e.__class__.__name__}: {str(e)[:80]}")
                continue

            try:
                results = page.evaluate(SCAN_JS)
            except Exception as e:
                print(f"  [scan failed] {e}")
                continue

            if results:
                findings[path] = results
                dark_count = sum(1 for r in results if r["dark"])
                total = len(results)
                print(f"  {total} data-table-ish element(s), {dark_count} dark")
                for r in results:
                    marker = "DARK" if r["dark"] else "    "
                    print(f"    [{marker}] <{r['tag']}> bg={r['bg']} luma={r['luma']:.0f}" if r["luma"] is not None
                          else f"    [{marker}] <{r['tag']}> bg={r['bg']} luma=n/a")
                    print(f"             {r['selector']}")
            else:
                print("  (no mdc-data-table or ha-data-table elements)")

        browser.close()

    # Aggregate unique dark selectors
    dark_selectors = set()
    for path, items in findings.items():
        for it in items:
            if it["dark"]:
                dark_selectors.add(it["selector"])

    out = {
        "scanned_paths": CONFIG_PATHS,
        "findings_by_path": findings,
        "unique_dark_selectors": sorted(dark_selectors),
    }
    (OUT_DIR / "data-table-audit.json").write_text(json.dumps(out, indent=2))
    print(f"\n{'='*60}")
    print(f"Unique dark mdc-data-table selectors: {len(dark_selectors)}")
    for s in sorted(dark_selectors):
        print(f"  {s}")
    print(f"\nFull report: {OUT_DIR / 'data-table-audit.json'}")


if __name__ == "__main__":
    main()
