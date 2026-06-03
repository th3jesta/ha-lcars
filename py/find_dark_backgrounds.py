#!/usr/bin/env python3
"""
Crawl /config sub-pages and find every visible element with a dark
(low-luma, non-transparent) background, then emit a card-mod selector
chain (with `$` shadow-root piercing) for each. De-duplicate by
selector pattern so repeated rows/cells don't flood the output.

Goal: identify all surfaces inside settings panels that need their text
kept LIGHT, so that a panel-wide `--lcars-primary-text` darkening doesn't
make text on dark backgrounds unreadable.

Usage:
    python3 py/find_dark_backgrounds.py
"""
from __future__ import annotations

import json
import os
import time
from collections import defaultdict
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
]

# Luma threshold (0-255) — anything under is "dark"
DARK_LUMA = 60


SCAN_JS = r"""
(args) => {
    const DARK_LUMA = args.darkLuma;
    const out = [];

    function rgbToLuma(rgb) {
        const m = rgb.match(/(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)/);
        if (!m) return null;
        const [r, g, b] = [+m[1], +m[2], +m[3]];
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }
    function alphaOf(rgb) {
        const m = rgb.match(/rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*([0-9.]+)\s*\)/);
        return m ? parseFloat(m[1]) : 1.0;
    }
    function hasDirectText(el) {
        for (const ch of el.childNodes) {
            if (ch.nodeType === 3 && ch.textContent.trim().length > 0) return true;
        }
        return false;
    }
    function hasAnyText(el) {
        return el.textContent && el.textContent.trim().length > 0;
    }

    /**
     * Build a card-mod selector chain.
     *
     * Walks up from `target` recording each step. A step is either:
     *   - a "shadow" hop: we crossed a shadow-root boundary upward
     *   - a "light" hop: we walked through parentElement in the same tree
     *
     * Only custom elements (tag contains "-") are kept as named waypoints;
     * plain div/span ancestors are skipped, but a "light" hop crossing
     * intermediate non-custom elements still emits a single descendant
     * combinator (a space).
     *
     * Joins:
     *   - " $ " for a shadow boundary
     *   - " "   for descendant (one or more light-DOM hops)
     */
    function buildShadowSelector(target) {
        function isCustom(el) {
            return el && el.localName && el.localName.includes("-");
        }
        function describe(el) {
            let s = el.localName;
            if (el.id) s += "#" + el.id;
            else if (el.classList && el.classList.length) {
                const c = [...el.classList].filter(c => !c.startsWith("style-scope")).slice(0, 3).join(".");
                if (c) s += "." + c;
            }
            return s;
        }

        // We collect segments target→root. Each segment stores `sepFromParent`,
        // the separator to place BEFORE this segment in root→target order — i.e.,
        // it describes the relationship between this segment and the next-higher
        // (parent) segment in the chain.
        //
        // While walking UP, we accumulate whether a shadow boundary was crossed
        // since the last custom segment. When we reach the next custom segment,
        // we use that accumulator to set the previous custom segment's
        // sepFromParent (because the previous custom segment is "closer to target"
        // than this one; its sepFromParent describes how to get from its parent
        // (the segment we're about to push) down to it).
        const segs = [{ name: describe(target), sepFromParent: null }];
        let n = target;
        let crossedShadow = false;
        while (n) {
            const root = n.getRootNode();
            const parent = n.parentElement;
            let nextN;
            if (parent) {
                nextN = parent;
            } else if (root instanceof ShadowRoot) {
                nextN = root.host;
                crossedShadow = true;
            } else {
                break;
            }
            if (isCustom(nextN)) {
                segs[segs.length - 1].sepFromParent = crossedShadow ? " $ " : " ";
                segs.push({ name: nextN.localName, sepFromParent: null });
                crossedShadow = false;
            }
            n = nextN;
        }

        // Reverse to root→target and assemble
        const ordered = segs.slice().reverse();
        let out = "";
        for (let i = 0; i < ordered.length; i++) {
            const seg = ordered[i];
            if (i === 0) {
                out = seg.name;
            } else {
                out += seg.sepFromParent + seg.name;
            }
        }
        return out;
    }

    function walk(root) {
        const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
        let el;
        while ((el = w.nextNode())) {
            // Skip non-visible elements
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) {
                if (el.shadowRoot) walk(el.shadowRoot);
                continue;
            }
            // Skip if not in viewport-ish range (likely virtual/off-screen but rendered)
            // Allow off-screen since data tables may be wider than viewport
            const cs = getComputedStyle(el);
            if (cs.display === "none" || cs.visibility === "hidden" || cs.opacity === "0") {
                if (el.shadowRoot) walk(el.shadowRoot);
                continue;
            }

            const bg = cs.backgroundColor;
            const luma = rgbToLuma(bg);
            const alpha = alphaOf(bg);
            const isDark = luma !== null && luma < DARK_LUMA && alpha > 0.5;

            if (isDark && hasAnyText(el)) {
                // Only emit elements that are reasonable "containers" — skip
                // tiny inline elements where text is from descendants only
                if (rect.width >= 40 && rect.height >= 16) {
                    out.push({
                        tag: el.localName,
                        cls: (el.className && typeof el.className === "string" ? el.className : "").trim().slice(0, 100),
                        id: el.id || "",
                        bg,
                        luma: Math.round(luma),
                        w: Math.round(rect.width),
                        h: Math.round(rect.height),
                        selector: buildShadowSelector(el),
                        text_preview: el.textContent.trim().slice(0, 60),
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


def normalize_selector(sel: str) -> str:
    """Strip transient ID/class suffixes so repeated rows collapse to one entry."""
    # Drop trailing `.style-scope-*` and bracketed indices, generic class lists
    # Keep the path structure intact
    return sel


def main() -> None:
    os.environ.setdefault("PLAYWRIGHT_HOST_PLATFORM_OVERRIDE", "ubuntu24.04-x64")

    # Map: selector pattern -> {paths_seen, sample_bg, sample_luma, sample_text}
    aggregated: dict[str, dict] = {}

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

        for path in CONFIG_PATHS:
            url = HA_URL + path
            try:
                print(f"\nScanning {path} ...")
                page.goto(url, wait_until="domcontentloaded", timeout=45_000)
                page.wait_for_function(
                    "() => !location.pathname.startsWith('/auth/')", timeout=30_000
                )
                page.wait_for_function(
                    "() => { const ha = document.querySelector('home-assistant'); return ha && ha.shadowRoot !== null; }",
                    timeout=30_000,
                )
                time.sleep(5)
            except Exception as e:
                print(f"  [skip] {e.__class__.__name__}: {str(e)[:80]}")
                continue

            try:
                results = page.evaluate(SCAN_JS, {"darkLuma": DARK_LUMA})
            except Exception as e:
                print(f"  [scan failed] {e}")
                continue

            page_unique = set()
            for r in results:
                key = normalize_selector(r["selector"])
                if key in page_unique:
                    continue  # avoid duplicates within the same page (rows)
                page_unique.add(key)

                if key not in aggregated:
                    aggregated[key] = {
                        "selector": key,
                        "tag": r["tag"],
                        "sample_bg": r["bg"],
                        "sample_luma": r["luma"],
                        "sample_text": r["text_preview"],
                        "paths": [],
                    }
                if path not in aggregated[key]["paths"]:
                    aggregated[key]["paths"].append(path)

            print(f"  {len(page_unique)} unique dark-bg containers")

        browser.close()

    # Sort: prefer common selectors (used on multiple paths) first
    entries = sorted(aggregated.values(), key=lambda e: (-len(e["paths"]), e["selector"]))

    # Cluster by panel-host prefix to reveal cross-panel patterns
    # A panel-host prefix is the substring before the first non-prefix "$".
    # Strip everything after the panel-host segment to find common tail patterns.
    tail_patterns: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        sel = e["selector"]
        # tail = everything after the second-level "$" — the part within the panel
        parts = sel.split(" $ ")
        # parts[0]=home-assistant, parts[1]=home-assistant-main, parts[2]=panel-host, rest=tail
        if len(parts) > 3:
            panel = parts[2]
            tail = " $ ".join(parts[3:])
        else:
            panel = parts[-1] if parts else ""
            tail = ""
        tail_patterns[tail].append({**e, "panel": panel})

    print(f"\n{'='*60}")
    print(f"Total unique dark-bg selectors: {len(entries)}")
    print(f"Unique tail patterns (panel-agnostic): {len(tail_patterns)}")

    print("\n=== Tail patterns shared across panels (>=2 panels) ===\n")
    for tail, items in sorted(tail_patterns.items(), key=lambda kv: -len(kv[1])):
        if len(items) < 2:
            continue
        print(f"TAIL: {tail or '(panel root)'}")
        print(f"  panels: {', '.join(sorted(set(i['panel'] for i in items)))}")
        sample = items[0]
        print(f"  bg={sample['sample_bg']}  luma={sample['sample_luma']}  text={sample['sample_text']!r}")
        print()

    print("\n=== Panel-specific (only on 1 panel) ===\n")
    for tail, items in sorted(tail_patterns.items(), key=lambda kv: -len(kv[1])):
        if len(items) >= 2:
            continue
        item = items[0]
        print(f"{item['selector']}")
        print(f"  bg={item['sample_bg']}  luma={item['sample_luma']}  text={item['sample_text']!r}")
        print(f"  paths: {', '.join(item['paths'])}")
        print()

    (OUT_DIR / "dark-backgrounds.json").write_text(json.dumps({
        "entries": entries,
        "tail_patterns": {k: v for k, v in tail_patterns.items()},
    }, indent=2, default=str))
    print(f"Full report: {OUT_DIR / 'dark-backgrounds.json'}")


if __name__ == "__main__":
    main()
