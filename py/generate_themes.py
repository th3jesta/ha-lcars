#!/usr/bin/env python3
"""
Generate themes/lcars.yaml from src/

Usage:
    python3 py/generate_themes.py

Theme files live in src/themes/*.yaml (numbered for output order).
Shared palette, base settings, and card-mod CSS live in src/preamble.yaml.
Default values for optional variables live in src/defaults.yaml.

DO NOT edit themes/lcars.yaml directly — run this script instead.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).parent.parent
SRC = REPO_ROOT / "src"
PREAMBLE_FILE = SRC / "preamble.yaml"
DEFAULTS_FILE = SRC / "defaults.yaml"
THEMES_DIR = SRC / "themes"
OUTPUT_FILE = REPO_ROOT / "themes" / "lcars.yaml"

# Every theme must define these variables.
REQUIRED_VARS = [
    "lcars-ui-primary",
    "lcars-ui-secondary",
    "lcars-ui-tertiary",
    "lcars-ui-quaternary",
    "lcars-ui-config-button",
    "lcars-background-color",
    "lcars-ui-text-heading",
    "lcars-card-top-color",
    "lcars-card-mid-color",
    "lcars-card-button-color",
    "lcars-card-bottom-color",
    "lcars-card-top-text",
    "lcars-card-mid-text",
    "lcars-card-button-text",
    "lcars-card-bottom-text",
]

# Output order for each section; variables not in any section go at the end.
SECTIONS: dict[str, list[str]] = {
    "UI Colors": [
        "lcars-ui-primary",
        "lcars-ui-primary-text",
        "lcars-ui-secondary",
        "lcars-ui-secondary-text",
        "lcars-ui-tertiary",
        "lcars-ui-tertiary-text",
        "lcars-ui-quaternary",
        "lcars-ui-quaternary-text",
        "lcars-ui-accent-color",
        "lcars-ui-accent-text",
        "lcars-background-color",
        "lcars-background-text",
        "lcars-alert-color",
        "lcars-ui-text-heading",
    ],
    "Header / Sidebar": [
        "lcars-ui-app-header-background-color",
        "lcars-ui-app-header-text-color",
        "lcars-ui-app-header-clock",
        "lcars-ui-config-button",
        "lcars-ui-config-icon",
    ],
    "Sidebar": [
        "lcars-sidebar-background",
        "lcars-sidebar-item-color",
        "lcars-sidebar-text",
        "lcars-sidebar-icon-color",
        "lcars-sidebar-icon-background",
        "lcars-sidebar-selected-color",
        "lcars-sidebar-notification-color",
    ],
    "Card colors": [
        "lcars-card-top-color",
        "lcars-card-mid-color",
        "lcars-card-button-color",
        "lcars-card-bottom-color",
    ],
    "Card text": [
        "lcars-card-top-text",
        "lcars-card-mid-text",
        "lcars-card-button-text",
        "lcars-card-bottom-text",
    ],
    "Status colors": [
        "success-color",
        "warning-color",
        "error-color",
    ],

}

# Flattened set of all explicitly sectioned variables.
_SECTIONED = {v for vs in SECTIONS.values() for v in vs}

# HA standard variables for which we emit rgb-* counterparts.
# The frontend skips auto-derivation when the value is var() rather than a hex,
# so we resolve the chain here and inject the result explicitly.
_RGB_TARGETS = [
    "card-background-color",
    "primary-text-color",
    "secondary-text-color",
    "primary-color",
    "accent-color",
    "primary-background-color",
    "secondary-background-color",
]

_VAR_RE = re.compile(r"^var\(--([^,)]+)(?:,.*)?\)$")


def load_preamble_vars(preamble_path: Path) -> tuple[dict, dict]:
    """Return (palette, base_vars) extracted from preamble.yaml.

    palette   — the &lcars-variables block (raw hex color names)
    base_vars — the &base block (HA standard var mappings)
    """
    try:
        data = yaml.safe_load(preamble_path.read_text())
    except yaml.YAMLError as exc:
        print(f"WARNING: could not parse preamble for rgb derivation: {exc}")
        return {}, {}

    palette: dict = {}
    base_vars: dict = {}
    for _key, value in (data or {}).items():
        if not isinstance(value, dict):
            continue
        flat = {k: str(v) for k, v in value.items() if isinstance(v, (str, int, float))}
        if "lcars-space-white" in flat:
            palette = flat
        elif "primary-color" in flat and "card-background-color" in flat:
            base_vars = flat
    return palette, base_vars


def var_resolve(key: str, context: dict, depth: int = 0) -> str | None:
    """Follow var(--foo) chains in *context* until a hex value or dead end."""
    if depth > 15:
        return None
    value = context.get(key, "").strip()
    if not value:
        return None
    m = _VAR_RE.match(value)
    if m:
        return var_resolve(m.group(1), context, depth + 1)
    if value.startswith("#"):
        return value
    return None


def hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")[:6]  # drop alpha channel if present
    return f"{int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)}"



def fmt(value: object) -> str:
    """Format a variable value for YAML output.

    Hex colors must be quoted so YAML doesn't treat '#' as a comment.
    Everything else (var() references, plain strings) is emitted as-is.
    """
    s = str(value)
    if s.startswith("#"):
        return f'"{s}"'
    return s


def render_theme(name: str, variables: dict, modes: dict | None = None) -> str:
    lines: list[str] = [
        f"{name}:",
        f"  card-mod-theme: {name}",
        "  <<: *lcars-variables",
        "  <<: *base",
        "  <<: *card-mod-css",
    ]

    for section_label, var_names in SECTIONS.items():
        section_lines = [
            f"  {v}: {fmt(variables[v])}"
            for v in var_names
            if v in variables
        ]
        if section_lines:
            lines.append(f"  # {section_label}")
            lines.extend(section_lines)

    # Derived rgb-* variables (resolved from var() chains by generate_themes.py).
    rgb_vars = {k: v for k, v in variables.items() if k.startswith("rgb-")}
    if rgb_vars:
        lines.append("  # Derived RGB")
        for k, v in rgb_vars.items():
            lines.append(f'  {k}: "{v}"')

    # Anything left over (e.g. lcars-tab-selected-bg in 25C).
    extras = {k: v for k, v in variables.items() if k not in _SECTIONED and not k.startswith("rgb-")}
    if extras:
        lines.append("  # Theme-specific")
        for k, v in extras.items():
            lines.append(f"  {k}: {fmt(v)}")

    if modes:
        lines.append("  modes:")
        for mode_name, mode_vars in modes.items():
            lines.append(f"    {mode_name}:")
            for k, v in (mode_vars or {}).items():
                lines.append(f"      {k}: {fmt(v)}")

    return "\n".join(lines)


def load_theme(path: Path, defaults: dict) -> tuple[str, dict, dict | None]:
    with path.open() as f:
        data: dict = yaml.safe_load(f)

    name = data.get("name")
    if not name:
        raise ValueError(f"{path.name}: missing required 'name' field")

    # Deep-merge modes: default modes are the base, theme modes override per-key.
    default_modes: dict = defaults.get("modes") or {}
    theme_modes: dict = data.get("modes") or {}
    all_mode_keys = set(default_modes) | set(theme_modes)
    modes: dict | None = (
        {mk: {**(default_modes.get(mk) or {}), **(theme_modes.get(mk) or {})} for mk in all_mode_keys}
        if all_mode_keys else None
    )

    base_defaults = {k: v for k, v in defaults.items() if k != "modes"}
    variables = {**base_defaults, **{k: v for k, v in data.items() if k not in ("name", "modes")}}
    return name, variables, modes


def validate(name: str, variables: dict, errors: list[str]) -> None:
    missing = [v for v in REQUIRED_VARS if v not in variables]
    if missing:
        errors.append(f"{name}: missing required variables: {', '.join(missing)}")

    known = _SECTIONED | {"lcars-tab-selected-bg", "lcars-alert-color"}  # extend as new specials emerge
    unknown = [k for k in variables if k not in known]
    if unknown:
        # Warn but don't fail — new variables may be legitimately added.
        print(f"  WARNING {name}: unknown variables (add to SECTIONS if intentional): "
              f"{', '.join(unknown)}")


def main() -> None:
    with DEFAULTS_FILE.open() as f:
        defaults: dict = yaml.safe_load(f)

    theme_files = sorted(THEMES_DIR.glob("*.yaml"))
    if not theme_files:
        sys.exit(f"ERROR: no theme files found in {THEMES_DIR}")

    themes: list[tuple[str, dict, dict | None]] = []
    errors: list[str] = []

    for path in theme_files:
        try:
            name, variables, modes = load_theme(path, defaults)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(str(exc))
            continue
        validate(name, variables, errors)
        themes.append((name, variables, modes))

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)

    palette, base_vars = load_preamble_vars(PREAMBLE_FILE)
    preamble = PREAMBLE_FILE.read_text().rstrip()

    chunks: list[str] = [
        preamble,
        "",
        "# ======================================================= #",
        "#                    THEME DEFINITIONS                    #",
        "# ======================================================= #",
        "#",
        "# DO NOT edit this section by hand.",
        "# Edit src/themes/<name>.yaml and run generate_themes.py.",
        "",
    ]

    for name, variables, modes in themes:
        # Resolve var() chains to hex and inject rgb-* for HA standard vars.
        # Context priority: theme/defaults > base_vars > palette (lowest).
        context = {**palette, **base_vars, **variables}
        for key in _RGB_TARGETS:
            hex_val = var_resolve(key, context)
            if hex_val:
                variables[f"rgb-{key}"] = hex_to_rgb(hex_val)
        chunks.append(render_theme(name, variables, modes))
        chunks.append("")

    chunks.append("# ================ Paste your themes here =============== |")
    chunks.append("# (or add a file to src/themes/ and run generate_themes.py)")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(chunks) + "\n")

    print(f"Written {OUTPUT_FILE} ({len(themes)} themes):")
    for name, _, __ in themes:
        print(f"  {name}")


if __name__ == "__main__":
    main()
