#!/usr/bin/env python3
"""Static integrity check for the site.

Walks every .html file and verifies that each local href/src (relative, not
http/mailto/anchor/data) resolves to a file that exists on disk. Catches broken
asset includes and dead module links before they ship.

Usage::

    python tools/check_site.py        # exits non-zero if anything is broken
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REF_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"')


def is_external(url: str) -> bool:
    return url.startswith(
        ("http://", "https://", "//", "mailto:", "data:", "#", "javascript:")
    )


def main() -> int:
    html_files = sorted(ROOT.rglob("*.html"))
    broken: list[str] = []
    checked = 0

    for html in html_files:
        text = html.read_text(encoding="utf-8", errors="surrogateescape")
        for ref in REF_RE.findall(text):
            url = ref.split("#", 1)[0].split("?", 1)[0].strip()
            if not url or is_external(ref):
                continue
            target = (html.parent / url).resolve()
            checked += 1
            if not target.exists():
                broken.append(f"{html.relative_to(ROOT)} → {ref}")

    if broken:
        print(f"✗ {len(broken)} broken local reference(s):")
        for b in broken:
            print(f"   {b}")
        return 1

    print(f"✓ {checked} local references across {len(html_files)} HTML files all resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
