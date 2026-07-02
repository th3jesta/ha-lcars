# Contributing to HA LCARS

## How the theme is built

The file that HACS installs — `themes/lcars.yaml` — is generated. Do not edit it directly; changes will be overwritten the next time `generate_themes.py` runs.

```
src/
  preamble.yaml          # YAML anchors: palette, &base HA vars, &card-mod-css
  defaults.yaml          # Default values for optional per-theme variables
  themes/
    default.yaml         # One file per theme variant
    classic.yaml
    25c.yaml
    ...
generate_themes.py       # Assembles the above into themes/lcars.yaml
themes/
  lcars.yaml             # Generated output installed by HACS — do not edit
  lcars_flat.yaml        # Generated flattened version for iOS and Qt browsers that need it — do not edit
py/
  flatten_ha_theme_css.py  # Flattens nested CSS in lcars.yaml → lcars_flat.yaml
```

### `src/preamble.yaml`

Contains three YAML anchors that every theme references:

| Anchor | Purpose |
|--------|---------|
| `&lcars-variables` | The full color palette — every named LCARS color as a hex value. These are the only place raw hex codes should appear. |
| `&base` | HA standard CSS custom property mappings (`primary-color`, `card-background-color`, font settings, sidebar vars, etc.) expressed in terms of `lcars-*` semantic tokens. |
| `&card-mod-css` | card-mod YAML blobs (`card-mod-card-yaml`, `card-mod-root-yaml`, etc.) that inject CSS into Home Assistant's shadow DOM. |

### `src/defaults.yaml`

Default values for semantic tokens that themes can override but are not required to. Every key here appears in every generated theme unless the theme file explicitly overrides it. Comments describe rendered surfaces, not CSS internals.

### `src/themes/*.yaml`

One file per theme variant. Each file has a required `name:` key and then only the variables that differ from `defaults.yaml`. Required variables (validated by `generate_themes.py`) must be present either in the theme file itself or in `defaults.yaml`.

### `generate_themes.py`

Assembles the output file:

1. Reads `defaults.yaml` as the base variable set.
2. For each theme file in `src/themes/`, merges defaults → theme-specific variables.
3. Validates that all `REQUIRED_VARS` are present.
4. Reads `preamble.yaml` verbatim as the top of the output file (YAML anchors are preserved).
5. For each theme, emits a theme block that merges `*lcars-variables`, `*base`, and `*card-mod-css` via YAML anchors, then writes the per-theme variables in section order.
6. Auto-derives `rgb-*` counterparts for HA standard color vars (required because HA's frontend only derives these from hex literals, not `var()` references).

Run it after any change to `src/`:

```bash
python3 py/generate_themes.py
```

### flatten_ha_theme_css.py
`lcars_flat.yaml` is generated automatically on release tags — you do not need to run the flatten script locally. If you need a flat file locally for testing:

```bash
python3 py/flatten_ha_theme_css.py -o themes/lcars_flat.yaml themes/lcars.yaml
```

---

## CI/CD workflows

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `validate.yaml` | push, PR, daily | HACS theme validation |
| `hassfest.yml` | push, PR, daily | Home Assistant `hassfest` validation |
| `flatten.yml` | push of any tag | Runs `py/flatten_ha_theme_css.py` and commits `themes/lcars_flat.yaml` to `master` |
| `purge-jsdelivr.yml` | push to `js-main` branch | Purges the jsDelivr CDN cache for `lcars.js` |

---

## Adding a new theme variant

1. Create `src/themes/<slug>.yaml`. The filename has no required format; use something descriptive.

2. Set the required `name:` key — this is the display name shown in the HA theme picker:

   ```yaml
   name: LCARS My Variant
   ```

3. Set all required variables. Check `REQUIRED_VARS` in `generate_themes.py` for the current list. Variables with defaults in `defaults.yaml` are optional — only override what differs:

   ```yaml
   name: LCARS My Variant

   # Required color palette
   lcars-ui-primary: var(--lcars-gold)
   lcars-ui-secondary: var(--lcars-orange)
   lcars-ui-tertiary: var(--lcars-mars)
   lcars-ui-quaternary: var(--lcars-dark-gray)
   lcars-ui-config-button: var(--lcars-ui-secondary)
   lcars-background-color: var(--lcars-black)
   lcars-ui-text-heading: var(--lcars-text-gray)

   # Required card colors
   lcars-card-top-color: var(--lcars-gold)
   lcars-card-mid-color: var(--lcars-orange)
   lcars-card-button-color: var(--lcars-orange)
   lcars-card-bottom-color: var(--lcars-dark-gray)
   lcars-card-top-text: var(--lcars-text-dark)
   lcars-card-mid-text: var(--lcars-text-dark)
   lcars-card-button-text: var(--lcars-text-dark)
   lcars-card-bottom-text: var(--lcars-text-dark)
   ```

4. All color values must reference palette names from `&lcars-variables` in `preamble.yaml` using `var(--<name>)`. Do not introduce new raw hex values — add them to the palette first if needed.

5. Run the generator and confirm no errors:

   ```bash
   python3 py/generate_themes.py
   ```

   Warnings about unknown variables are non-fatal but should be addressed (see below).

6. Copy `themes/lcars.yaml` into your Home Assistant instance, reload themes (Developer Tools > Services > `frontend.reload_themes`) and verify the theme looks correct.

7. Create a PR to merge the new theme into `master`.

### Choosing text colors (light vs. dark)

LCARS is a dark-text design. The rule below keeps that aesthetic by default and only swaps to light when staying dark would be illegible.

For each background variable (`lcars-ui-primary`, `lcars-ui-secondary`, `lcars-ui-tertiary`, `lcars-ui-quaternary`, `lcars-card-top-color`, `lcars-card-mid-color`, `lcars-card-button-color`, `lcars-card-bottom-color`), compute the WCAG contrast ratio of the background hex against `#000000` (`dark_ratio`), then pick the text color per mode:

| Mode | Rule |
|------|------|
| **Light mode** (theme top-level values) | text is **dark** iff `dark_ratio > 4.5` — otherwise **light**. |
| **Dark mode** (`modes.dark` block) | text is **dark** iff `dark_ratio > 3.0` — otherwise **light**. |

Then:

1. Set the top-level `*-text` variable to the **light-mode** result.
2. If the **dark-mode** result differs (the same background, or a `modes.dark` override of the background, lands on a different recommendation), override the `*-text` variable inside the `modes.dark` block.

Why these thresholds:

- The light-mode `4.5:1` floor is WCAG AA for normal text. Dark text only stays put if it clears AA outright; otherwise we switch to light, which is always the better choice when `dark_ratio < 4.5` (since `dark_ratio · light_ratio = 21` always, so `dark_ratio < 4.5` implies `light_ratio > 4.67`).
- The dark-mode `3.0` floor is the WCAG AA-Large minimum. Below 3:1 dark text becomes unreadable; above it, dark text reads as canonical LCARS even when light has a numerically higher contrast.

---

## Adding a new semantic variable

Semantic variables (`lcars-ui-*`, `lcars-card-*`, `lcars-sidebar-*`) are the interface between theme files and the CSS in `preamble.yaml`. Adding one involves up to four files.

### 1. Add a default in `src/defaults.yaml`

If the variable should have a sensible value across all themes without requiring every theme file to set it, add it here with a comment describing which rendered surface it controls:

```yaml
# tooltip/popover background
lcars-ui-popover-color: var(--lcars-dark-gray)
```

### 2. Use it in `src/preamble.yaml`

Reference the new variable in `&base` (for HA standard property mappings) or `&card-mod-css` (for shadow DOM CSS overrides):

```yaml
# in &base, this applies broadly everywhere the var is used:
tooltip-background: var(--lcars-ui-popover-color)

# or in &card-mod-css, this can be targeted to specific elements:
ha-tooltip {
  --tooltip-background: var(--lcars-ui-popover-color);
}
```

### 3. Register it in `generate_themes.py`

Add the variable name to the appropriate section in `SECTIONS` so it appears in the generated output in a predictable order and is recognized by the validator:

```python
SECTIONS: dict[str, list[str]] = {
    "UI Colors": [
        ...
        "lcars-ui-popover-color",   # add here
        ...
    ],
```

If the variable must be present in every theme (not just defaulted), also add it to `REQUIRED_VARS`.

### 4. Override in individual themes (optional)

If a specific theme needs a different value, add it to that theme's file in `src/themes/`:

```yaml
lcars-ui-popover-color: var(--lcars-slate)
```

---

## Adding an auto-computed variable

The only current auto-derived variables are `rgb-*` counterparts for HA standard color vars. If you need to derive another variable from a resolved hex value, add the computation to `generate_themes.py`'s `main()` loop after the `rgb-*` block:

```python
# After the rgb-* loop in main():
hex_val = var_resolve("lcars-ui-new-bg", context)
if hex_val:
    variables["lcars-ui-new-text"] = _text_on(hex_val)   # or other derivation
```

`var_resolve(key, context)` follows `var()` chains until it reaches a hex literal. Returns `None` if the chain cannot be resolved — add a fallback in `defaults.yaml` for that case. Add the derived variable to `SECTIONS` so it appears in output order.

---

## Palette colors

All raw hex values live in the `&lcars-variables` block in `src/preamble.yaml`. LCARS historically has a limited palette for each show/generation. This helps keep the palette limited and organized. When a theme or default needs a color not already in the palette, add it there first:

```yaml
lcars-my-new-color: "#aabbcc"
```

Then reference it everywhere else as `var(--lcars-my-new-color)`. Hex literals should not appear anywhere else in the source files. 
