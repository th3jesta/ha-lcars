#!/usr/bin/env python3
"""
flatten_ha_theme_css.py

Flatten nested CSS inside Home Assistant theme YAML files.

This parser preserves the YAML as plain text and only rewrites the blocks that
actually contain CSS. It is built for Home Assistant theme files that embed 
card-mod YAML inside YAML inside YAML.

Usage:
    python3 ha_theme_flatten_nested_css.py input.yaml -o output.yaml
    python3 ha_theme_flatten_nested_css.py input.yaml --in-place

Maintainer: Treyfane Dingo <dingo@furcom.org>
Project: pythonscripts
Licence: MIT
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class CssRule:
    selectors: List[str] = field(default_factory=list)
    declarations: List[str] = field(default_factory=list)
    children: List["CssRule"] = field(default_factory=list)
    at_rule: Optional[str] = None


_LITERAL_RE = re.compile(
    r'^(?P<indent>[ \t]*)(?P<head>[^#\n][^\n]*?:[ \t]*(?:[&*!][^|#\n]+\s+)*)?(?P<style>\|[+-]?)\s*(?:#.*)?$'
)

_NESTED_LITERAL_MARKER_RE = re.compile(
    r'^\s*(?:"[^"\n]*"|\'[^\'\n]*\'|[^:\n][^:\n]*)\s*:\s*(?:[&*!][^|#\n]+\s+)*\|[+-]?\s*(?:#.*)?$'
)

_TEMPLATE_RE = re.compile(r"\{\{.*?\}\}|\{%.*?%\}", flags=re.S)


def normalise_literal_marker_line_for_match(line: str) -> str:
    """Normalise spacing in YAML literal markers for regex matching only."""
    line = re.sub(r"\$\s*:\s*\|", "$: |", line)
    line = re.sub(r":\s*\|", ": |", line)
    return line


def mask_templates(text: str) -> Tuple[str, Dict[str, str]]:
    mapping: Dict[str, str] = {}
    counter = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal counter
        token = f"__HA_TEMPLATE_{counter}__"
        mapping[token] = match.group(0)
        counter += 1
        return token

    return _TEMPLATE_RE.sub(repl, text), mapping


def restore_templates(text: str, mapping: Dict[str, str]) -> str:
    for token, original in mapping.items():
        text = text.replace(token, original)
    return text


def strip_css_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def normalise_css_source(text: str) -> str:
    """
    Remove block comments, un-comment CSS lines that were prefixed with '#'
    inside YAML blocks, and repair missing semicolons before nested rules.
    """
    text = strip_css_comments(text)
    unhashed: List[str] = []

    for line in text.splitlines():
        stripped = line.lstrip()
        # A line beginning with # inside CSS is usually an ID selector (#view,
        # #item, #add-view).  The older version treated every such line as a
        # commented-out CSS line and removed the hash, which broke the HA
        # header/menu/sidebar selectors.  Real YAML/CSS comments should stay
        # comments or disappear, not be converted into live CSS.
        if stripped.startswith("#"):
            after_hash = stripped[1:].lstrip()
            if after_hash.startswith((".", ":", "[", ">", "+", "~", "@")):
                # Optional compatibility escape hatch: allow commented-out CSS
                # fragments like '# .foo {' to be revived, but never '#id'.
                indent = line[: len(line) - len(stripped)]
                unhashed.append(indent + after_hash)
            else:
                # Preserve ID selectors and ignore ordinary YAML-style comments.
                # The CSS parser will skip true comments; selectors remain intact.
                unhashed.append(line)
            continue
        unhashed.append(line)

    def next_significant_line(lines: List[str], start: int) -> str:
        for candidate in lines[start + 1:]:
            stripped = candidate.strip()
            if stripped:
                return stripped
        return ""

    def looks_like_declaration(line: str) -> bool:
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            return False
        if stripped.startswith(("{%", "{{", "@", "/*", "*", "//")):
            return False
        if stripped.endswith((";", "{", "}", ",")):
            return False
        property_name = stripped.split(":", 1)[0].strip()
        return re.fullmatch(r"(?:--)?[A-Za-z_][\w-]*", property_name) is not None

    repaired: List[str] = []
    for index, line in enumerate(unhashed):
        if looks_like_declaration(line):
            following = next_significant_line(unhashed, index)
            if following and (
                following == "}"
                or following.startswith("@")
                or following.endswith("{")
                or following.startswith(("&", ":", "::", ".", "#", ">", "+", "~"))
                or re.match(r"^[A-Za-z_*:-][^;{}]*\{$", following)
                or (following.startswith("{%") and following.endswith("%}"))
            ):
                line = line.rstrip() + ";"
        repaired.append(line)

    return "\n".join(repaired)


def skip_ws(text: str, i: int) -> int:
    while i < len(text) and text[i].isspace():
        i += 1
    return i


def read_until_top_level(text: str, start: int, stop_chars: str) -> Tuple[str, int]:
    i = start
    n = len(text)
    out: List[str] = []
    paren = 0
    bracket = 0
    quote: Optional[str] = None

    while i < n:
        ch = text[i]

        if quote is not None:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                i += 1
                out.append(text[i])
            elif ch == quote:
                quote = None
            i += 1
            continue

        if ch in ("'", '"'):
            quote = ch
            out.append(ch)
            i += 1
            continue

        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            if end == -1:
                out.append(text[i:])
                return "".join(out), n
            out.append(text[i:end + 2])
            i = end + 2
            continue

        if paren == 0 and bracket == 0 and ch in stop_chars:
            break

        if ch == "(":
            paren += 1
        elif ch == ")":
            paren = max(0, paren - 1)
        elif ch == "[":
            bracket += 1
        elif ch == "]":
            bracket = max(0, bracket - 1)

        out.append(ch)
        i += 1

    return "".join(out), i


def split_top_level_commas(text: str) -> List[str]:
    parts: List[str] = []
    current: List[str] = []
    paren = 0
    bracket = 0
    quote: Optional[str] = None
    i = 0

    while i < len(text):
        ch = text[i]

        if quote is not None:
            current.append(ch)
            if ch == "\\" and i + 1 < len(text):
                i += 1
                current.append(text[i])
            elif ch == quote:
                quote = None
            i += 1
            continue

        if ch in ("'", '"'):
            quote = ch
            current.append(ch)
            i += 1
            continue

        if ch == "/" and i + 1 < len(text) and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            if end == -1:
                current.append(text[i:])
                break
            current.append(text[i:end + 2])
            i = end + 2
            continue

        if ch == "(":
            paren += 1
        elif ch == ")":
            paren = max(0, paren - 1)
        elif ch == "[":
            bracket += 1
        elif ch == "]":
            bracket = max(0, bracket - 1)

        if ch == "," and paren == 0 and bracket == 0:
            piece = "".join(current).strip()
            if piece:
                parts.append(piece)
            current = []
            i += 1
            continue

        current.append(ch)
        i += 1

    piece = "".join(current).strip()
    if piece:
        parts.append(piece)

    return parts


def normalise_selector(selector: str) -> str:
    selector = re.sub(r"\s+", " ", selector.strip())
    selector = re.sub(r"\(\s+", "(", selector)
    selector = re.sub(r"\s+\)", ")", selector)
    selector = re.sub(r"\s*,\s*", ", ", selector)
    selector = re.sub(r"\s*([>+~])\s*", r" \1 ", selector)
    selector = re.sub(r"\s+", " ", selector).strip()
    selector = re.sub(r":is\(\s*(#[A-Za-z0-9_-]+)\s*\)", r"\1", selector)
    return selector




def simplify_self_is_pseudo(selector: str) -> str:
    """Simplify cases created by nesting such as ha-card.foo:is(ha-card).

    CSS nesting often uses &:is(ha-card) to mean "the current element, when it is
    an ha-card". A string-only expansion would concatenate the tag and produce
    ha-card.fooha-card. This removes the :is(tag) part when the current compound
    selector already starts with that tag.
    """
    pattern = re.compile(r":is\(([^()]*)\)")

    def previous_compound(text: str, pos: int) -> str:
        # Last compound selector before the pseudo, after combinators/commas/spaces.
        j = pos - 1
        while j >= 0 and text[j].isspace():
            j -= 1
        k = j
        while k >= 0 and text[k] not in " >+~,{\n":
            k -= 1
        return text[k + 1:j + 1]

    def repl(match: re.Match[str]) -> str:
        inner = match.group(1)
        opts = [o.strip() for o in split_top_level_commas(inner)]
        compound = previous_compound(selector, match.start())
        tag_match = re.match(r"^[A-Za-z][\w-]*", compound)
        if tag_match and any(o == tag_match.group(0) for o in opts):
            remaining = [o for o in opts if o != tag_match.group(0)]
            if not remaining:
                return ""
            return ":is(" + ", ".join(remaining) + ")"
        return match.group(0)

    previous = None
    while previous != selector:
        previous = selector
        selector = pattern.sub(repl, selector)
    return selector


def expand_is_pseudo(selector: str) -> List[str]:
    """Expand simple :is(...) selector lists into separate selectors."""
    start = selector.find(":is(")
    if start == -1:
        return [selector]

    i = start + 4
    depth = 0
    quote = None
    end = -1

    while i < len(selector):
        ch = selector[i]
        if quote is not None:
            if ch == "\\" and i + 1 < len(selector):
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ("'", '"'):
            quote = ch
            i += 1
            continue
        if ch == '(':
            depth += 1
        elif ch == ')':
            if depth == 0:
                end = i
                break
            depth -= 1
        i += 1

    if end == -1:
        return [selector]

    inner = selector[start + 4:end]
    options = split_top_level_commas(inner)
    if not options:
        return [selector]

    prefix = selector[:start]
    suffix = selector[end + 1:]
    expanded: List[str] = []
    for option in options:
        combined = prefix + option.strip() + suffix
        expanded.extend(expand_is_pseudo(combined))
    return expanded


def rewrite_multi_not(selector: str) -> str:
    parts: List[str] = []
    i = 0
    while i < len(selector):
        if selector.startswith(":not(", i):
            j = i + 5
            depth = 0
            quote = None
            end = -1
            while j < len(selector):
                ch = selector[j]
                if quote is not None:
                    if ch == "\\" and j + 1 < len(selector):
                        j += 2
                        continue
                    if ch == quote:
                        quote = None
                    j += 1
                    continue
                if ch in ("'", '"'):
                    quote = ch
                    j += 1
                    continue
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    if depth == 0:
                        end = j
                        break
                    depth -= 1
                j += 1
            if end == -1:
                parts.append(selector[i:])
                break
            inner = selector[i + 5:end]
            opts = split_top_level_commas(inner)
            if len(opts) > 1:
                parts.append(''.join(f':not({opt.strip()})' for opt in opts if opt.strip()))
            else:
                parts.append(selector[i:end + 1])
            i = end + 1
            continue
        parts.append(selector[i])
        i += 1
    return ''.join(parts)


def clean_legacy_selector(selector: str) -> List[str]:
    selector = simplify_self_is_pseudo(selector)
    if ":has(" in selector:
        return []
    selectors = expand_is_pseudo(selector)
    cleaned: List[str] = []

    for item in selectors:
        item = rewrite_multi_not(item)
        item = normalise_selector(item)
        item = re.sub(r">\s+:not\(", "> *:not(", item)
        item = re.sub(r"(#[A-Za-z0-9_-]+)(?:\1)+", r"\1", item)

        # Legacy selector engines do not support complex selectors inside :not().
        # This rule used to spare bar-large-left/right, which left exactly the
        # compatibility problem this script is supposed to remove.
        if ":not(div > *)" in item:
            # The source uses `ha-card:is(...):not(div > *)` to avoid styling
            # nested/internal ha-cards. Simply deleting the complex :not() makes
            # the rule much too broad and breaks the inner header rounding.
            # For legacy selector engines, narrow those ha-card selectors to the
            # direct card below the card-mod host instead.
            item = re.sub(
                r"(?<![\w-])ha-card((?:\.[A-Za-z0-9_-]+)+):not\(div > \*\)",
                r":host > ha-card\1",
                item,
            )
            item = item.replace(":not(div > *)", "")
            item = normalise_selector(item)

        if ";" in item or "__HA_CONTROL_LINE_" in item:
            continue
        cleaned.append(item)

    out: List[str] = []
    seen = set()
    for item in cleaned:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out

def parse_css(css_text: str) -> List[CssRule]:
    rules, _ = _parse_block(css_text.replace("\r\n", "\n").replace("\r", "\n"), 0)
    return rules


def _parse_block(text: str, start: int) -> Tuple[List[CssRule], int]:
    rules: List[CssRule] = []
    i = start
    n = len(text)

    while i < n:
        i = skip_ws(text, i)
        if i >= n:
            break

        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end == -1:
                break
            i = end + 2
            continue

        if text[i] == "}":
            return rules, i + 1

        header, j = read_until_top_level(text, i, "{;}")
        header = header.strip()

        if not header:
            i = j + 1 if j < n else j
            continue

        if j >= n:
            break

        stop = text[j]

        if stop == ";":
            i = j + 1
            continue

        if header.startswith("@"):
            children, next_i = _parse_block(text, j + 1)
            rules.append(CssRule(at_rule=header, children=children))
            i = next_i
            continue

        selectors = split_top_level_commas(header)
        items, next_i = _parse_rule_body(text, j + 1)

        rule = CssRule(selectors=selectors)
        for kind, value in items:
            if kind == "decl":
                rule.declarations.append(value)
            else:
                rule.children.append(value)

        rules.append(rule)
        i = next_i

    return rules, i


def _parse_rule_body(text: str, start: int) -> Tuple[List[Tuple[str, object]], int]:
    items: List[Tuple[str, object]] = []
    i = start
    n = len(text)

    while i < n:
        i = skip_ws(text, i)
        if i >= n:
            break

        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end == -1:
                break
            items.append(("decl", text[i:end + 2].strip()))
            i = end + 2
            continue

        if text[i] == "}":
            return items, i + 1

        chunk, j = read_until_top_level(text, i, "{;}")
        chunk = chunk.strip()

        if not chunk:
            i = j + 1 if j < n else j
            continue

        if j >= n:
            break

        stop = text[j]

        if stop == ";":
            items.append(("decl", chunk + ";"))
            i = j + 1
            continue

        if chunk.startswith("@"):
            children, next_i = _parse_block(text, j + 1)
            items.append(("rule", CssRule(at_rule=chunk, children=children)))
            i = next_i
            continue

        selectors = split_top_level_commas(chunk)
        nested_items, next_i = _parse_rule_body(text, j + 1)

        rule = CssRule(selectors=selectors)
        for kind, value in nested_items:
            if kind == "decl":
                rule.declarations.append(value)
            else:
                rule.children.append(value)

        items.append(("rule", rule))
        i = next_i

    return items, i


def combine_selectors(parents: List[str], children: List[str]) -> List[str]:
    if not parents:
        return [expanded for child in children if child.strip() for expanded in clean_legacy_selector(child)]

    combined: List[str] = []

    for parent in parents:
        p = normalise_selector(parent)
        for child in children:
            c = child.strip()
            if not c:
                continue

            if "&" in c:
                full = c.replace("&", p)
            elif c.startswith((">", "+", "~")):
                full = f"{p} {c}"
            elif c.startswith((":", "::")):
                full = f"{p}{c}"
            else:
                full = f"{p} {c}"

            combined.extend(clean_legacy_selector(full))

    return combined


def flatten_css_rules(
    rules: List[CssRule],
    parents: Optional[List[str]] = None,
    at_stack: Optional[List[str]] = None,
    out: Optional[List[Tuple[List[str], List[str], List[str]]]] = None,
) -> List[Tuple[List[str], List[str], List[str]]]:
    if parents is None:
        parents = []
    if at_stack is None:
        at_stack = []
    if out is None:
        out = []

    for rule in rules:
        if rule.at_rule:
            flatten_css_rules(rule.children, parents, at_stack + [rule.at_rule], out)
            continue

        selectors = combine_selectors(parents, rule.selectors) if parents else [
            expanded for selector in rule.selectors if selector.strip() for expanded in clean_legacy_selector(selector)
        ]

        declarations = [declaration.rstrip() for declaration in rule.declarations if str(declaration).strip()]
        if selectors and declarations:
            out.append((selectors, declarations, at_stack.copy()))

        if rule.children:
            flatten_css_rules(rule.children, selectors, at_stack, out)

    return out


def render_flat_css(flat_rules: List[Tuple[List[str], List[str], List[str]]]) -> str:
    lines: List[str] = []

    for selectors, declarations, at_stack in flat_rules:
        level = 0

        for at_rule in at_stack:
            lines.append(f"{'  ' * level}{at_rule} {{")
            level += 1

        if len(selectors) == 1:
            lines.append(f"{'  ' * level}{selectors[0]} {{")
        else:
            for index, selector in enumerate(selectors):
                suffix = "," if index < len(selectors) - 1 else " {"
                lines.append(f"{'  ' * level}{selector}{suffix}")

        for declaration in declarations:
            lines.append(f"{'  ' * (level + 1)}{declaration}")

        lines.append(f"{'  ' * level}" + "}")

        for close_level in range(level - 1, -1, -1):
            lines.append(f"{'  ' * close_level}" + "}")

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"



def flatten_css_block(css_text: str) -> str:
    cleaned = normalise_css_source(css_text)

    # Jinja control lines are not CSS. If they are parsed as selectors, they get
    # combined with their parent selector and produce invalid CSS such as
    # ":host __HA_CONTROL_LINE_0__". Keep the CSS valid for legacy engines by
    # removing those control lines before parsing. Template expressions inside
    # declarations are still masked/restored below.
    protected_lines: List[str] = []
    for line in cleaned.splitlines():
        stripped = line.strip()
        if stripped.startswith("{%") and stripped.endswith("%}"):
            continue
        protected_lines.append(line)

    masked, mapping = mask_templates("\n".join(protected_lines))
    parsed = parse_css(masked)
    flattened = flatten_css_rules(parsed)
    rendered = render_flat_css(flattened)
    restored = restore_templates(rendered, mapping)

    return restored


def looks_like_css_block(text: str) -> bool:
    sample = strip_css_comments(text)
    if "{" not in sample or "}" not in sample:
        return False

    if not re.search(r"--[\w-]+\s*:", sample) and not re.search(r"[\w-]+\s*:\s*[^;{}]+;", sample):
        return False

    return True


def contains_nested_literal_syntax(block_text: str) -> bool:
    return any(_NESTED_LITERAL_MARKER_RE.match(normalise_literal_marker_line_for_match(line)) for line in block_text.splitlines())


def extract_block(lines: List[str], start_index: int, base_indent: int) -> Tuple[List[str], int]:
    block_lines: List[str] = []
    i = start_index

    while i < len(lines):
        raw = lines[i].rstrip("\n")

        if raw.strip() == "":
            block_lines.append(lines[i])
            i += 1
            continue

        current_indent = len(raw) - len(raw.lstrip(" "))
        if current_indent <= base_indent:
            break

        block_lines.append(lines[i])
        i += 1

    return block_lines, i


def dedent_block(block_lines: List[str]) -> Tuple[str, int]:
    non_empty = [line.rstrip("\n") for line in block_lines if line.strip()]
    if not non_empty:
        return "".join(block_lines), 0

    min_indent = min(len(line) - len(line.lstrip(" ")) for line in non_empty)
    out: List[str] = []

    for line in block_lines:
        if line.strip():
            out.append(line[min_indent:])
        else:
            out.append("\n" if line.endswith("\n") else "")

    return "".join(out), min_indent


def indent_text(text: str, indent: int) -> str:
    prefix = " " * indent
    return "".join(prefix + line if line.strip() else line for line in text.splitlines(keepends=True))


def strip_has_pseudo_from_selector_text(text: str) -> str:
    """Remove :has(...) from selector text without being fooled by nested parens."""
    out: List[str] = []
    i = 0
    while i < len(text):
        if text.startswith(":has(", i):
            j = i + 5
            depth = 0
            quote = None
            while j < len(text):
                ch = text[j]
                if quote is not None:
                    if ch == "\\" and j + 1 < len(text):
                        j += 2
                        continue
                    if ch == quote:
                        quote = None
                    j += 1
                    continue
                if ch in ("'", '"'):
                    quote = ch
                    j += 1
                    continue
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    if depth == 0:
                        j += 1
                        break
                    depth -= 1
                j += 1
            i = j
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def normalise_legacy_yaml_selector_line(line: str) -> str:
    # card-mod also uses selector strings as YAML keys, e.g.
    # "ha-card:has(ha-sortable)$": |. Older selector engines reject :has().
    if ":has(" not in line:
        return line
    return strip_has_pseudo_from_selector_text(line)

def process_text(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: List[str] = []
    i = 0

    while i < len(lines):
        line = normalise_legacy_yaml_selector_line(lines[i])
        match = _LITERAL_RE.match(normalise_literal_marker_line_for_match(line.rstrip("\n")))

        if not match:
            out.append(line)
            i += 1
            continue

        out.append(line)
        base_indent = len(match.group("indent"))
        block_lines, i = extract_block(lines, i + 1, base_indent)

        if not block_lines:
            continue

        block_text, min_indent = dedent_block(block_lines)
        recursively_processed = process_text(block_text)

        if contains_nested_literal_syntax(recursively_processed):
            out.append(indent_text(recursively_processed, min_indent))
            continue

        if looks_like_css_block(recursively_processed):
            try:
                flattened = flatten_css_block(recursively_processed)
                out.append(indent_text(flattened, min_indent))
            except Exception:
                out.append(indent_text(recursively_processed, min_indent))
        else:
            out.append(indent_text(recursively_processed, min_indent))

    return "".join(out)

def insert_legacy_sidebar_menu_icon_centering(text: str) -> str:
    """Add an old iOS/QtWebKit centering fix for sidebar menu icons."""

    anchor = (
        '      ha-user-badge {\n'
        '        box-sizing: border-box;\n'
        '        width: calc( var(--mdc-icon-size,24px) + 37px);\n'
        '        padding-block: 8px;\n'
        '      }\n'
    )
    fix = (
        '\n'
        '      ha-list-item-button:not(.configuration):not(.user) > ha-icon,\n'
        '      ha-list-item-button:not(.configuration):not(.user) > ha-svg-icon {\n'
        '        display: flex;\n'
        '        align-items: center;\n'
        '        justify-content: center;\n'
        '        box-sizing: border-box;\n'
        '        min-width: 61px;\n'
        '        height: 100%;\n'
        '      }\n'
    )
    if anchor in text:
        return text.replace(anchor, anchor + fix, 1)


def postprocess_lcars_compat(text: str) -> str:
    """Repair cases where flattening creates CSS that is syntactically invalid or loses HA Jinja guards.

    This is deliberately conservative: it removes selectors that can never match
    because they combine :host(...) directly with a light-DOM ha-card/id, removes
    orphaned comment tails from malformed source comments, and restores the two
    standalone Home Assistant template guards used by lcars.yaml.
    """
    text = re.sub(r'^\s*\*[^\n]*\*/\s*\n', '', text, flags=re.M)

    kept: List[str] = []
    for line in text.splitlines(keepends=True):
        if re.search(r':host\([^)]*\)(?:ha-card|#[A-Za-z0-9_-])', line):
            continue
        kept.append(line)
    text = ''.join(kept)
    text = re.sub(r',\n(\s*\{)', r'\n\1', text)

    def find_block_end(source: str, start: int) -> int:
        i = source.find('{', start)
        if i < 0:
            return -1
        depth = 0
        quote: Optional[str] = None
        escaped = False
        while i < len(source):
            ch = source[i]
            if quote is not None:
                if escaped:
                    escaped = False
                elif ch == '\\':
                    escaped = True
                elif ch == quote:
                    quote = None
            else:
                if ch in ('"', "'"):
                    quote = ch
                elif ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        return i + 1
            i += 1
        return -1

    drawer_anchor = '  card-mod-drawer: |\n'
    drawer_index = text.find(drawer_anchor)
    if drawer_index >= 0 and "{% if not is_state('input_boolean.lcars_texture', 'off') %}" not in text[drawer_index:drawer_index + 400]:
        before_start = text.find('    :host::before {', drawer_index)
        if before_start >= 0:
            before_end = find_block_end(text, before_start)
            after_start = text.find('    :host::after {', before_end)
            if before_end >= 0 and after_start >= 0:
                after_end = find_block_end(text, after_start)
                if after_end >= 0:
                    segment = text[before_start:after_end]
                    wrapped = (
                        "    {% if not is_state('input_boolean.lcars_texture', 'off') %}\n"
                        + segment
                        + "\n    {% endif %}"
                    )
                    text = text[:before_start] + wrapped + text[after_end:]

    sound_pair = (
        '      .header {\n'
        '        --lcars-sound: false;\n'
        '      }\n\n'
        '      .header {\n'
        '        --lcars-sound: true;\n'
        '      }'
    )
    sound_guarded = (
        "      {% if not is_state('input_boolean.lcars_sound', 'on') %}\n"
        "      .header {\n"
        "        --lcars-sound: false;\n"
        "      }\n"
        "      {% else %}\n"
        "      .header {\n"
        "        --lcars-sound: true;\n"
        "      }\n"
        "      {% endif %}"
    )
    text = text.replace(sound_pair, sound_guarded)

    # Rewriting `:not(a,b,c)` to `:not(a):not(b):not(c)` is needed for
    # older selector engines, but it increases selector specificity. In the
    # header rules the common child reset then beats the later inner-radius
    # rule. Footer worked because the source already used !important there.
    # Make the corresponding header inner-radius declarations equally explicit.
    text = text.replace(
        'border-top-left-radius: var(--lcars-inner-radius);',
        'border-top-left-radius: var(--lcars-inner-radius) !important;',
    )
    text = text.replace(
        'border-top-right-radius: var(--lcars-inner-radius);',
        'border-top-right-radius: var(--lcars-inner-radius) !important;',
    )
    text = insert_legacy_sidebar_menu_icon_centering(text)
    return text

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flatten nested CSS inside Home Assistant theme YAML files."
    )
    parser.add_argument("input", type=Path, help="Input YAML file")
    parser.add_argument("-o", "--output", type=Path, help="Output YAML file")
    parser.add_argument("--in-place", action="store_true", help="Rewrite the input file in place")
    args = parser.parse_args()

    if args.in_place and args.output:
        parser.error("Use either --in-place or --output, not both.")

    source = args.input.read_text(encoding="utf-8")
    transformed = postprocess_lcars_compat(process_text(source))

    if args.in_place:
        args.input.write_text(transformed, encoding="utf-8")
        return 0

    output_path = args.output or args.input.with_name(args.input.stem + "_flattened" + args.input.suffix)
    output_path.write_text(transformed, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
