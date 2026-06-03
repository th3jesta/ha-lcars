#!/usr/bin/env python3
"""
Find the "Mudroom Light" element on the home-flexible dashboard, identify
its computed text color, and walk up the composed ancestor tree to
determine which CSS custom property / selector is winning the cascade.

Usage:
    python3 py/inspect_mudroom_light.py
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait

HA_URL = "https://ps2nfvpesdke44vv04irms1d3bym6rsj.ui.nabu.casa"
DASHBOARD_PATH = "/lovelace/home-flexible"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiI2YmM5NWI4NmUxZjA0ZjEzODI0NTZhMDM3YTQ2NGI3NCIsImlhdCI6MTc3OTIzNTYwNSwiZXhwIjoyMDk0NTk1NjA1fQ"
    ".QIgVN0W_lMHjlO_Vo7OxMO38i1htOKJepVR7iB711Wo"
)
TARGET_TEXT = "Mudroom Light"

OUT_DIR = Path(__file__).parent.parent / "docs" / "light-text-audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)


FIND_AND_TRACE_JS = r"""
const TARGET = arguments[0];
const results = [];

function getPath(el) {
    const parts = [];
    let node = el;
    while (node && node.nodeType === Node.ELEMENT_NODE) {
        let seg = node.localName;
        if (node.id) { seg += '#' + node.id; }
        else if (node.className && typeof node.className === 'string') {
            const cls = node.className.trim().split(/\s+/).slice(0, 2).join('.');
            if (cls) seg += '.' + cls;
        }
        parts.unshift(seg);
        const root = node.getRootNode();
        node = node.parentElement || (root instanceof ShadowRoot ? root.host : null);
    }
    return parts.join(' > ');
}

function ancestorChain(el) {
    // Walk up the COMPOSED tree (through shadow boundaries).
    const chain = [];
    let node = el;
    while (node) {
        chain.push(node);
        const root = node.getRootNode();
        if (node.parentElement) {
            node = node.parentElement;
        } else if (root instanceof ShadowRoot) {
            node = root.host;
        } else {
            node = null;
        }
    }
    return chain;
}

// Probe a CSS variable by attaching a temporary child to el and reading its color.
function probeVar(el, varName) {
    const probe = document.createElement('span');
    probe.style.cssText = `position:absolute;opacity:0;pointer-events:none;color:var(${varName})`;
    el.appendChild(probe);
    const c = window.getComputedStyle(probe).color;
    el.removeChild(probe);
    return c;
}

// Variables to probe at each ancestor
const VARS = [
    '--primary-text-color',
    '--secondary-text-color',
    '--lcars-primary-text',
    '--lcars-secondary-text',
    '--lcars-background-text',
    '--lcars-text-light',
    '--lcars-text-dark',
    '--lcars-text-gray',
    '--lcars-ui-quaternary-text',
    '--lcars-ui-primary-text',
    '--lcars-card-top-text',
    '--lcars-card-mid-text',
    '--lcars-card-button-text',
    '--lcars-card-bottom-text',
    '--state-icon-color',
    '--card-background-color',
];

function findAll(root) {
    const matches = [];
    const iter = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
    let el;
    while ((el = iter.nextNode())) {
        for (const child of el.childNodes) {
            if (child.nodeType === Node.TEXT_NODE && child.textContent.trim() === TARGET) {
                matches.push(el);
                break;
            }
        }
        if (el.shadowRoot) matches.push(...findAll(el.shadowRoot));
    }
    return matches;
}

const found = findAll(document);

for (const el of found) {
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();

    // Build full composed ancestor chain
    const chain = ancestorChain(el);

    // For each ancestor, record:
    //  - what classes / element it is
    //  - what each tracked var resolves to AT THAT ancestor (probed via injected span)
    const ancestorReport = [];
    for (const a of chain.slice(0, 12)) {  // limit depth for readability
        const inShadow = a.getRootNode() instanceof ShadowRoot;
        const cls = (a.className && typeof a.className === 'string') ? a.className.trim() : '';
        const entry = {
            path: getPath(a),
            inShadow,
            classes: cls,
            vars: {},
        };
        for (const v of VARS) {
            try { entry.vars[v] = probeVar(a, v); } catch (e) { entry.vars[v] = '[error]'; }
        }
        ancestorReport.push(entry);
    }

    results.push({
        text: el.textContent.trim().slice(0, 80),
        tag: el.localName,
        path: getPath(el),
        computedColor: style.color,
        inheritedSource: style.getPropertyValue('--primary-text-color') || '[empty]',
        rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) },
        ancestors: ancestorReport,
    });
}

return results;
"""


def main() -> None:
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--width=1600")
    opts.add_argument("--height=900")
    opts.binary_location = "/snap/firefox/current/usr/lib/firefox/firefox"

    service = Service(log_output="/dev/null")
    driver = webdriver.Firefox(service=service, options=opts)
    driver.set_window_size(1600, 900)

    try:
        print("Seeding auth token...")
        driver.get(HA_URL)
        time.sleep(1)
        driver.execute_script(f"""
            localStorage.setItem('hassTokens', JSON.stringify({{
                access_token: '{TOKEN}',
                token_type: 'Bearer',
                expires_in: 315360000,
                expires_at: {time.time() + 315360000},
                hassUrl: '{HA_URL}',
                clientId: '{HA_URL}/',
            }}));
        """)

        print(f"Loading {HA_URL}{DASHBOARD_PATH} ...")
        driver.get(HA_URL + DASHBOARD_PATH)

        wait = WebDriverWait(driver, 90)
        wait.until(lambda d: "/auth/" not in d.current_url)
        wait.until(lambda d: d.execute_script(
            "const ha = document.querySelector('home-assistant'); "
            "return ha !== null && ha.shadowRoot !== null;"
        ))
        print("Waiting for theme to apply...")
        time.sleep(7)

        driver.save_screenshot(str(OUT_DIR / "mudroom-dashboard.png"))

        print(f"Searching for {TARGET_TEXT!r}...")
        results = driver.execute_script(FIND_AND_TRACE_JS, TARGET_TEXT)

        print(f"\nFound {len(results)} match(es) for {TARGET_TEXT!r}\n")
        for i, r in enumerate(results):
            print(f"=== Match {i+1} ===")
            print(f"  text:          {r['text']!r}")
            print(f"  tag:           <{r['tag']}>")
            print(f"  path:          {r['path']}")
            print(f"  computedColor: {r['computedColor']}")
            print(f"  position:      ({r['rect']['x']}, {r['rect']['y']})  {r['rect']['w']}×{r['rect']['h']}")
            print(f"  ancestors (showing CSS var values at each):")
            for j, a in enumerate(r["ancestors"]):
                shadow = " [shadow]" if a["inShadow"] else ""
                print(f"    [{j}] {a['path']}{shadow}")
                if a["classes"]:
                    print(f"        classes: {a['classes'][:120]}")
                # show only non-empty / non-default vars
                interesting = {k: v for k, v in a["vars"].items()
                               if v and "rgba(0, 0, 0, 0)" not in v}
                for k, v in interesting.items():
                    print(f"        {k:<35} → {v}")
            print()

        out_json = OUT_DIR / "mudroom-trace.json"
        out_json.write_text(json.dumps(results, indent=2))
        print(f"\nFull trace JSON: {out_json}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
