#!/usr/bin/env python3
"""Wiki 健康检查脚本。

检测项目：
- 断链：[[wikilink]] 指向不存在的页面
- 孤立页：没有任何页面链接到它
- 缺失 frontmatter 字段
- 过时页面：超过指定天数未更新
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

WIKI_DIR = Path(__file__).parent.parent / "wiki"
STALE_DAYS = 90
REQUIRED_FIELDS = {"title", "tags", "created", "updated", "sources"}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm


def collect_pages() -> dict[str, Path]:
    """返回 {相对路径(无后缀): 绝对路径}"""
    pages = {}
    for p in WIKI_DIR.rglob("*.md"):
        rel = p.relative_to(WIKI_DIR)
        key = str(rel.with_suffix(""))
        pages[key] = p
    return pages


def extract_links(path: Path, current_key: str | None = None) -> list[str]:
    """提取 wikilink 目标，规范化为 page key。

    处理形态：
    - [[page]]              → page
    - [[page|alias]]        → page
    - [[page\\|alias]]       → page（表格内 `|` 必须转义才能正确渲染表格）
    - [[page#anchor]]       → page（#anchor 部分忽略）
    - [[#anchor]]           → current_key（同页锚点，需传入 current_key 才识别）
    """
    text = path.read_text(encoding="utf-8")
    # 剔除围栏/行内代码块——里面的 [[xxx]] 是引用 lint 输出 / 文档示例，不是真链接
    text = FENCED_CODE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    raw = WIKILINK_RE.findall(text)
    links = []
    for link in raw:
        # 切掉 alias：先按 `\|` 切，再按 `|` 切，取第一段
        target = re.split(r"\\?\|", link, maxsplit=1)[0]
        # 切掉 #anchor
        target = target.split("#", 1)[0]
        if not target:
            # 同页锚点：[[#xxx]]，target 为空字符串
            if current_key is not None:
                links.append(current_key)
            continue
        links.append(target)
    return links


def check_broken_links(pages: dict[str, Path]) -> list[str]:
    issues = []
    for key, path in pages.items():
        for link in extract_links(path, current_key=key):
            if link not in pages:
                issues.append(f"断链: {key}.md -> [[{link}]]（目标不存在）")
    return issues


def check_orphans(pages: dict[str, Path]) -> list[str]:
    linked: set[str] = set()
    for path in pages.values():
        # 不传 current_key——同页锚点不算"被外部页面引用"
        linked.update(extract_links(path))
    issues = []
    for key in pages:
        if key == "index" or key.startswith("journal/"):
            continue
        if key not in linked:
            issues.append(f"孤立页: {key}.md（没有任何页面链接到它）")
    return issues


def check_frontmatter(pages: dict[str, Path]) -> list[str]:
    issues = []
    for key, path in pages.items():
        if key == "index" or key.startswith("journal/"):
            continue
        fm = parse_frontmatter(path)
        missing = REQUIRED_FIELDS - set(fm.keys())
        if missing:
            issues.append(f"缺失字段: {key}.md 缺少 {', '.join(sorted(missing))}")
    return issues


def check_stale(pages: dict[str, Path]) -> list[str]:
    issues = []
    cutoff = datetime.now() - timedelta(days=STALE_DAYS)
    for key, path in pages.items():
        if key == "index" or key.startswith("journal/"):
            continue
        fm = parse_frontmatter(path)
        updated = fm.get("updated", "")
        if not updated:
            continue
        try:
            dt = datetime.strptime(updated, "%Y-%m-%d")
            if dt < cutoff:
                issues.append(f"过时: {key}.md（上次更新 {updated}，超过 {STALE_DAYS} 天）")
        except ValueError:
            issues.append(f"日期格式错误: {key}.md 的 updated 字段 '{updated}' 不是 YYYY-MM-DD")
    return issues


def main():
    if not WIKI_DIR.exists():
        print("错误: wiki/ 目录不存在")
        sys.exit(1)

    pages = collect_pages()
    if not pages:
        print("wiki/ 目录为空，没有页面需要检查。")
        return

    all_issues: list[str] = []
    all_issues.extend(check_broken_links(pages))
    all_issues.extend(check_orphans(pages))
    all_issues.extend(check_frontmatter(pages))
    all_issues.extend(check_stale(pages))

    if not all_issues:
        print(f"✓ Wiki 健康检查通过（共 {len(pages)} 个页面）")
    else:
        print(f"Wiki 健康检查发现 {len(all_issues)} 个问题：\n")
        for issue in sorted(all_issues):
            print(f"  • {issue}")
        print()
        print(f"共 {len(pages)} 个页面，{len(all_issues)} 个问题。")
        sys.exit(1)


if __name__ == "__main__":
    main()
