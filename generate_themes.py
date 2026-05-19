#!/usr/bin/env python3
"""
Generate themes/lcars.yaml from src/

Usage:
    python generate_themes.py

Theme files live in src/themes/*.yaml (numbered for output order).
Shared palette, base settings, and card-mod CSS live in src/preamble.yaml.
Default values for optional variables live in src/defaults.yaml.

DO NOT edit themes/lcars.yaml directly — run this script instead.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent
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
        "lcars-ui-secondary",
        "lcars-ui-tertiary",
        "lcars-ui-quaternary",
        "lcars-ui-accent-color",
        "lcars-background-color",
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


def fmt(value: object) -> str:
    """Format a variable value for YAML output.

    Hex colors must be quoted so YAML doesn't treat '#' as a comment.
    Everything else (var() references, plain strings) is emitted as-is.
    """
    s = str(value)
    if s.startswith("#"):
        return f'"{s}"'
    return s


def render_theme(name: str, variables: dict) -> str:
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

    # Anything left over (e.g. lcars-tab-selected-bg in 25C).
    extras = {k: v for k, v in variables.items() if k not in _SECTIONED}
    if extras:
        lines.append("  # Theme-specific")
        for k, v in extras.items():
            lines.append(f"  {k}: {fmt(v)}")

    return "\n".join(lines)


def load_theme(path: Path, defaults: dict) -> tuple[str, dict]:
    with path.open() as f:
        data: dict = yaml.safe_load(f)

    name = data.get("name")
    if not name:
        raise ValueError(f"{path.name}: missing required 'name' field")

    # defaults first, theme values override
    variables = {**defaults, **{k: v for k, v in data.items() if k != "name"}}
    return name, variables


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

    themes: list[tuple[str, dict]] = []
    errors: list[str] = []

    for path in theme_files:
        try:
            name, variables = load_theme(path, defaults)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(str(exc))
            continue
        validate(name, variables, errors)
        themes.append((name, variables))

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)

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

    for name, variables in themes:
        chunks.append(render_theme(name, variables))
        chunks.append("")

    chunks.append("# ================ Paste your themes here =============== |")
    chunks.append("# (or add a file to src/themes/ and run generate_themes.py)")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(chunks) + "\n")

    print(f"Written {OUTPUT_FILE} ({len(themes)} themes):")
    for name, _ in themes:
        print(f"  {name}")


if __name__ == "__main__":
    main()
