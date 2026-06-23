#!/usr/bin/env python3
"""Regenerate every study module by running each generator in ``generators/``.

Each ``generators/gen_<topic>.py`` script writes the base
``modules/<NN>_<topic>/index.html`` and ``study_guide.ipynb``. This script is a
thin orchestrator: it discovers every generator, runs it in a subprocess (so one
failing generator can't abort the rest), then injects the shared site "chrome"
(theme toggle, page loader, mobile nav, ``effects.js``/``nav-ux.js``) into the
freshly written HTML. The chrome partials live in ``styles/module_chrome.json``
so the whole site is reproducible from this one command — no out-of-repo
post-processing step.

Usage::

    python generate_all.py              # rebuild all modules
    python generate_all.py numpy sql    # rebuild only matching generators

Requires Python 3.10+. No external dependencies — standard library only.
"""

import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
GEN_DIR = ROOT / "generators"
CHROME_FILE = ROOT / "styles" / "module_chrome.json"
SEARCH_INDEX = ROOT / "search_index.json"

_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
_SECTION_RE = re.compile(r'<a href="#(s\d+)"[^>]*>([^<]+)</a>')
_EMOJI_TITLE_RE = re.compile(r"^[^\w(]+")  # leading emoji/space before the name

# Matches the standardized output-folder token in every generator, e.g.
#   ... / "modules" / "01_numpy"     (pathlib form)
#   ... "modules", "07_sklearn")     (os.path form)
_FOLDER_RE = re.compile(r'"modules"\s*[/,]\s*"([^"]+)"')


def _target_folder(gen: pathlib.Path) -> str | None:
    """Return the modules/<folder> name a generator writes to, or None."""
    m = _FOLDER_RE.search(gen.read_text(encoding="utf-8", errors="surrogateescape"))
    return m.group(1) if m else None


def _load_chrome() -> dict | None:
    if not CHROME_FILE.exists():
        return None
    return json.loads(CHROME_FILE.read_text(encoding="utf-8"))


def apply_chrome(index_html: pathlib.Path, chrome: dict) -> bool:
    """Inject theme/loader/footer chrome into a base module index.html.

    Idempotent: a file that already contains the loader is left untouched.
    Handles both generator HTML templates (one writes ``</body></html>`` on a
    single trailing line, the other splits ``</body>\\n</html>``).
    """
    html = index_html.read_text(encoding="utf-8")
    if "page-loader" in html:
        return False  # already enhanced

    theme, loader, footer = chrome["theme_init"], chrome["loader"], chrome["footer"]

    glass = '<link rel="stylesheet" href="../../styles/glass.css">\n'
    body_open = '<body class="page-module">\n'
    if glass not in html or body_open not in html:
        raise ValueError(f"{index_html}: unexpected template (no head anchors)")

    html = html.replace(glass, glass + theme + "\n", 1)
    html = html.replace(body_open, body_open + loader + "\n", 1)

    if html.endswith("</script></body></html>"):          # single-line tail
        end = "</body></html>"
    elif html.endswith("</script>\n</body>\n</html>"):      # split tail
        end = "</body>\n</html>"
    else:
        raise ValueError(f"{index_html}: unexpected closing tags")
    html = html[: -len(end)] + "\n" + footer + "\n" + end

    index_html.write_text(html, encoding="utf-8")
    return True


def build_search_index() -> int:
    """Scan every module's index.html and write search_index.json — module
    titles plus their section topics/anchors — for the homepage search box.
    Modules without #sN anchors (the hand-maintained Pandas page) are listed
    without sections; the homepage card filter still covers them."""
    entries = []
    for idx in sorted(ROOT.glob("modules/*/index.html")):
        text = idx.read_text(encoding="utf-8", errors="surrogateescape")
        tm = _TITLE_RE.search(text)
        title = tm.group(1).strip() if tm else idx.parent.name
        title = re.sub(r"\s*Study Guide\s*$", "", title)
        title = _EMOJI_TITLE_RE.sub("", title).strip() or idx.parent.name
        seen, sections = set(), []
        for anchor, label in _SECTION_RE.findall(text):
            if anchor in seen:
                continue
            seen.add(anchor)
            sections.append({"t": html.unescape(label).strip(), "a": anchor})
        entries.append(
            {
                "module": idx.parent.name,
                "title": title,
                "url": "modules/" + idx.parent.name + "/index.html",
                "sections": sections,
            }
        )
    SEARCH_INDEX.write_text(
        json.dumps(entries, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    topics = sum(len(e["sections"]) for e in entries)
    print(f"→ search_index.json: {len(entries)} modules, {topics} topics")
    return 0


def main(argv: list[str]) -> int:
    gens = sorted(GEN_DIR.glob("gen_*.py"))
    if argv:
        wanted = [a.lower().removeprefix("gen_") for a in argv]
        gens = [g for g in gens if any(w in g.stem for w in wanted)]
        if not gens:
            print(f"No generators matched: {argv}")
            return 1

    chrome = _load_chrome()
    if chrome is None:
        print(f"⚠ {CHROME_FILE.name} missing — writing base HTML without chrome.")

    failures: list[str] = []
    for g in gens:
        print(f"→ {g.name}")
        res = subprocess.run(
            [sys.executable, str(g)], capture_output=True, text=True
        )
        if res.returncode != 0:
            failures.append(g.name)
            if res.stdout:
                print(res.stdout.rstrip())
            if res.stderr:
                print(res.stderr.rstrip())
            print(f"  ✗ {g.name} failed")
            continue

        last = res.stdout.strip().splitlines()
        print(f"  ✓ {last[-1] if last else 'done'}")

        if chrome is not None:
            folder = _target_folder(g)
            index_html = ROOT / "modules" / (folder or "") / "index.html"
            if folder and index_html.exists():
                if apply_chrome(index_html, chrome):
                    print("    + chrome applied")

    build_search_index()

    ok = len(gens) - len(failures)
    print(f"\n{ok}/{len(gens)} generators succeeded.")
    if failures:
        print("Failed:", ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
