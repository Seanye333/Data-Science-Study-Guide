import sys, io, json, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = pathlib.Path(r"C:/Users/seany/Documents/All Codes/Data Science Study Path")

with open(BASE / "_stats_sections.json", encoding="utf-8") as f:
    sections = json.load(f)

def section_to_py(s):
    lines = []
    lines.append("{")
    lines.append("    " + chr(34) + "title" + chr(34) + ": " + json.dumps(s["title"]) + ",")
    lines.append("    " + chr(34) + "examples" + chr(34) + ": [")
    for ex in s["examples"]:
        lines.append("        {")
        lines.append("            " + chr(34) + "label" + chr(34) + ": " + json.dumps(ex["label"]) + ",")
        lines.append("            " + chr(34) + "code" + chr(34) + ": " + json.dumps(ex["code"]))
        lines.append("        },")
    lines.append("    ],")
    for key in ("rw_scenario", "rw_code", "practice"):
        if key in s:
            lines.append("    " + json.dumps(key) + ": " + json.dumps(s[key]) + ",")
    lines.append("}")
    return "
".join(lines)

new_py = ",
".join(section_to_py(s) for s in sections) + ",
"

target = BASE / "gen_statistics.py"
content = target.read_text(encoding="utf-8")
marker = "]  # end SECTIONS"
assert content.count(marker) == 1
new_content = content.replace(marker, new_py + marker)
target.write_text(new_content, encoding="utf-8")
print(f"Done. gen_statistics.py is now {len(new_content)} chars")