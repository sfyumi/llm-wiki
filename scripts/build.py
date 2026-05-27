#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown>=3.5"]
# ///
"""Build static HTML site from wiki/.

Renders all wiki/**/*.md to site/<same-path>.html with:
- [[wikilink]] / [[page|alias]] / [[page\\|alias]] / [[#anchor]] / [[page#anchor]] resolution
- Frontmatter card at top
- Backlinks footer
- GitHub-style heading anchors (matches existing [[#anchor]] usage in wiki)
- Code blocks shielded from wikilink interpretation

Run: ./scripts/build.py    (uv handles venv automatically)
Or:  uv run scripts/build.py
"""

import re
import shutil
import sys
import unicodedata
from collections import defaultdict
from html import escape
from pathlib import Path

import markdown

REPO = Path(__file__).resolve().parent.parent
WIKI = REPO / "wiki"
SITE = REPO / "site"
STYLE_SRC = Path(__file__).parent / "build_style.css"

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FENCED_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# ---------------------------------------------------------------------------
# slugify — must match GitHub anchor rules so existing [[#anchor]] resolves
# ---------------------------------------------------------------------------

def slugify(text: str, sep: str = "-") -> str:
    """Lowercase + drop punctuation/symbols + whitespace→hyphen + collapse."""
    text = text.strip().lower()
    # Drop everything that is not a Unicode word char, whitespace, or hyphen.
    # \w in Python 3 covers CJK ideographs; CJK punctuation 「（）、」 falls out.
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", sep, text)
    text = re.sub(rf"{re.escape(sep)}+", sep, text)
    return text.strip(sep)


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_after_frontmatter). Naive YAML — no nesting."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


# ---------------------------------------------------------------------------
# Wikilink resolution
# ---------------------------------------------------------------------------

def parse_wikilink(content: str) -> tuple[str, str, str | None]:
    """[[page#anchor|alias]] → (page, anchor, alias). Handles `\\|` table escape."""
    target_part = re.split(r"\\?\|", content, maxsplit=1)
    target = target_part[0]
    alias = target_part[1] if len(target_part) > 1 else None
    if "#" in target:
        page, _, anchor = target.partition("#")
    else:
        page, anchor = target, ""
    return page, anchor, alias


def render_wikilink(content: str, current_key: str, pages: dict, current_dir_depth: int) -> str:
    """Convert [[xxx]] payload to <a> or <span class='broken-link'>."""
    page, anchor, alias = parse_wikilink(content)

    # Display text: alias > last path segment > full content
    if alias is not None:
        display = alias
    elif page:
        display = page.rsplit("/", 1)[-1]
    else:
        display = "#" + anchor

    target_key = page if page else current_key

    if target_key not in pages:
        return f'<span class="broken-link" title="broken link: {escape(content)}">{escape(display)}</span>'

    # Compute relative path from current page to target
    href = relpath(current_key, target_key) + ".html"
    if anchor:
        href += "#" + anchor

    return f'<a class="wikilink" href="{escape(href)}">{escape(display)}</a>'


def relpath(from_key: str, to_key: str) -> str:
    """Relative href path from one page key to another. Both keys are slash-separated, no extension."""
    from_parts = from_key.split("/")
    to_parts = to_key.split("/")
    # The "from" key's directory depth determines how many `..` we need
    up = len(from_parts) - 1
    return "../" * up + "/".join(to_parts) if up else "/".join(to_parts) if "/" in to_key else to_parts[-1]


def shield_code_and_substitute(body: str, current_key: str, pages: dict) -> str:
    """Stash code regions so [[xxx]] inside them isn't interpreted, then resolve wikilinks."""
    stash: list[str] = []

    def stash_match(m: re.Match) -> str:
        stash.append(m.group(0))
        return f"\x00CODE{len(stash)-1}\x00"

    body = FENCED_RE.sub(stash_match, body)
    body = INLINE_CODE_RE.sub(stash_match, body)

    body = WIKILINK_RE.sub(
        lambda m: render_wikilink(m.group(1), current_key, pages, 0),
        body,
    )

    body = re.sub(r"\x00CODE(\d+)\x00", lambda m: stash[int(m.group(1))], body)
    return body


# ---------------------------------------------------------------------------
# Backlinks
# ---------------------------------------------------------------------------

def extract_targets(body: str) -> set[str]:
    """Return set of page keys referenced from body (excluding code blocks, anchors)."""
    text = FENCED_RE.sub("", body)
    text = INLINE_CODE_RE.sub("", text)
    out: set[str] = set()
    for m in WIKILINK_RE.finditer(text):
        page, _, _ = parse_wikilink(m.group(1))
        if page:
            out.add(page)
    return out


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{css_href}">
</head>
<body>
<div class="layout">
<header class="topbar">
{breadcrumb}
</header>
<article>
{frontmatter_html}
{body_html}
</article>
{backlinks_html}
</div>
</body>
</html>
"""


def render_frontmatter_card(fm: dict) -> str:
    if not fm:
        return ""
    rows = []
    for key in ("tags", "created", "updated", "status", "type", "version", "repo", "sources", "related_concepts"):
        if key in fm and fm[key]:
            rows.append(f"<dt>{escape(key)}</dt><dd>{escape(fm[key])}</dd>")
    if not rows:
        return ""
    return f'<div class="frontmatter"><dl>{"".join(rows)}</dl></div>'


def render_breadcrumb(key: str, pages: dict) -> str:
    """`projects/example` → home › projects › example"""
    parts = key.split("/")
    if key == "index":
        return '<a href="index.html">🏠 home</a>'
    depth = len(parts) - 1
    home_href = "../" * depth + "index.html" if depth else "index.html"
    crumbs = [f'<a href="{escape(home_href)}">🏠 home</a>']
    for i, part in enumerate(parts[:-1]):
        crumbs.append("›")
        crumbs.append(escape(part))
    crumbs.append("›")
    crumbs.append(f"<strong>{escape(parts[-1])}</strong>")
    return " ".join(crumbs)


def render_backlinks(key: str, backlinks: dict, pages: dict) -> str:
    refs = sorted(backlinks.get(key, []))
    if not refs:
        body = '<span class="none">（暂无回链）</span>'
    else:
        items = []
        for src in refs:
            href = relpath(key, src) + ".html"
            title_text = pages[src]["title"] or src.rsplit("/", 1)[-1]
            items.append(
                f'<li><a class="wikilink" href="{escape(href)}">{escape(src)}</a> — {escape(title_text)}</li>'
            )
        body = f"<ul>{''.join(items)}</ul>"
    return f'<footer class="backlinks"><h2>← Backlinks</h2>{body}</footer>'


def make_md_renderer():
    """Markdown renderer with TOC (heading anchors using GitHub-style slugify)."""
    return markdown.Markdown(
        extensions=["extra", "tables", "fenced_code", "toc", "sane_lists"],
        extension_configs={
            "toc": {
                "slugify": lambda value, sep: slugify(value, sep),
                "permalink": "¶",
                "permalink_class": "anchor",
                "permalink_title": "",
            }
        },
        output_format="html5",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def collect_pages() -> dict[str, dict]:
    pages: dict[str, dict] = {}
    for p in WIKI.rglob("*.md"):
        rel = p.relative_to(WIKI)
        key = str(rel.with_suffix("")).replace("\\", "/")
        text = p.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        pages[key] = {
            "path": p,
            "frontmatter": fm,
            "raw_body": body,
            "title": fm.get("title", "") or key.rsplit("/", 1)[-1],
        }
    return pages


def build():
    if not WIKI.exists():
        print("error: wiki/ not found", file=sys.stderr)
        sys.exit(1)

    pages = collect_pages()
    print(f"Loaded {len(pages)} pages.")

    # Build backlinks index
    backlinks: dict[str, list[str]] = defaultdict(list)
    for src_key, page in pages.items():
        for tgt in extract_targets(page["raw_body"]):
            if tgt in pages and tgt != src_key:
                backlinks[tgt].append(src_key)

    # Clean output
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    # Copy CSS
    shutil.copy(STYLE_SRC, SITE / "style.css")

    md = make_md_renderer()

    for key, page in pages.items():
        out_path = SITE / (key + ".html")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        depth = key.count("/")
        css_href = "../" * depth + "style.css" if depth else "style.css"

        # Resolve wikilinks (shielding code blocks), then render markdown
        body_with_links = shield_code_and_substitute(page["raw_body"], key, pages)
        md.reset()
        body_html = md.convert(body_with_links)

        html = PAGE_TEMPLATE.format(
            title=escape(page["title"]),
            css_href=escape(css_href),
            breadcrumb=render_breadcrumb(key, pages),
            frontmatter_html=render_frontmatter_card(page["frontmatter"]),
            body_html=body_html,
            backlinks_html=render_backlinks(key, backlinks, pages),
        )
        out_path.write_text(html, encoding="utf-8")

    print(f"✓ Built {len(pages)} pages → {SITE.relative_to(REPO)}/")
    print(f"  open {SITE.relative_to(REPO)}/index.html")


if __name__ == "__main__":
    build()
