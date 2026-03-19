"""Add sections 27-34 to gen_python_basics.py."""
import sys
sys.path.insert(0, r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
from _inserter import insert_sections

FILE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_python_basics.py"
MARKER = "]  # end SECTIONS"

def ec(code):
    return (code.replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace("'", "\\'"))

def make_pb(num, title, desc, examples, rw_title, rw_scenario, rw_code,
            pt, pd_text, ps):
    ex_lines = []
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples) - 1 else ''
        ex_lines.append(
            f'        {{"label": "{ec(ex["label"])}", "code": "{ec(ex["code"])}"}}{comma}'
        )
    ex_block = '\n'.join(ex_lines)
    return (
        f'{{\n'
        f'"title": "{num}. {title}",\n'
        f'"desc": "{ec(desc)}",\n'
        f'"examples": [\n{ex_block}\n    ],\n'
        f'"rw": {{\n'
        f'    "title": "{ec(rw_title)}",\n'
        f'    "scenario": "{ec(rw_scenario)}",\n'
        f'    "code": "{ec(rw_code)}"\n'
        f'}},\n'
        f'"practice": {{\n'
        f'    "title": "{ec(pt)}",\n'
        f'    "desc": "{ec(pd_text)}",\n'
        f'    "starter": "{ec(ps)}"\n'
        f'}}\n'
        f'}},\n\n'
    )

# ── Section 27: Argparse & CLI Tools ────────────────────────────────────────
s27 = make_pb(27, "Argparse & CLI Tools",
    "argparse is Python's standard library for building command-line interfaces. It handles argument parsing, type validation, help generation, and subcommands.",
    [
        {"label": "Basic ArgumentParser with positional and optional args",
         "code":
"""import argparse

# Simulate command-line arguments (replace sys.argv for demo)
parser = argparse.ArgumentParser(
    description="Process a data file",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

# Positional argument (required)
parser.add_argument("filename", help="Input CSV file path")

# Optional arguments
parser.add_argument("-o", "--output",  default="output.csv", help="Output file")
parser.add_argument("-n", "--rows",    type=int, default=100, help="Number of rows")
parser.add_argument("-v", "--verbose", action="store_true",   help="Verbose output")
parser.add_argument("--format",        choices=["csv","json","parquet"], default="csv")

# Parse a fake argument list
args = parser.parse_args(["data.csv", "--rows", "500", "--verbose", "--format", "json"])

print(f"File:    {args.filename}")
print(f"Output:  {args.output}")
print(f"Rows:    {args.rows}")
print(f"Verbose: {args.verbose}")
print(f"Format:  {args.format}")"""},
        {"label": "Subcommands (subparsers)",
         "code":
"""import argparse

parser = argparse.ArgumentParser(prog="datool", description="Data pipeline tool")
subs   = parser.add_subparsers(dest="command", required=True)

# Subcommand: convert
convert = subs.add_parser("convert", help="Convert file format")
convert.add_argument("input",  help="Input file")
convert.add_argument("output", help="Output file")
convert.add_argument("--compression", choices=["none","gzip","snappy"], default="none")

# Subcommand: stats
stats = subs.add_parser("stats", help="Show file statistics")
stats.add_argument("file",  help="File to analyze")
stats.add_argument("--col", action="append", dest="cols", help="Column to analyze (repeatable)")

# Subcommand: validate
validate = subs.add_parser("validate", help="Validate schema")
validate.add_argument("file")
validate.add_argument("--schema", required=True)

# Demo: parse "convert" command
args = parser.parse_args(["convert", "input.csv", "output.parquet", "--compression", "snappy"])
print(f"Command:     {args.command}")
print(f"Input:       {args.input}")
print(f"Output:      {args.output}")
print(f"Compression: {args.compression}")

# Demo: parse "stats" command
args2 = parser.parse_args(["stats", "data.csv", "--col", "price", "--col", "qty"])
print(f"Stats cols:  {args2.cols}")"""},
        {"label": "Argument groups, mutual exclusion, and type validators",
         "code":
"""import argparse

parser = argparse.ArgumentParser(description="Model training CLI")

# Argument group for visual organization in --help
data_group = parser.add_argument_group("Data options")
data_group.add_argument("--train",  required=True, help="Training data path")
data_group.add_argument("--val",    required=True, help="Validation data path")
data_group.add_argument("--test",   help="Test data path")

# Argument group for model options
model_group = parser.add_argument_group("Model options")
model_group.add_argument("--lr",     type=float, default=0.001)
model_group.add_argument("--epochs", type=int,   default=10)

# Mutually exclusive: can't use --gpu and --cpu together
device = parser.add_mutually_exclusive_group()
device.add_argument("--gpu", action="store_true")
device.add_argument("--cpu", action="store_true")

# Custom type validator
def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} must be a positive integer")
    return ivalue

model_group.add_argument("--batch", type=positive_int, default=32)

args = parser.parse_args(["--train", "train.csv", "--val", "val.csv",
                          "--lr", "0.01", "--gpu", "--batch", "64"])
print(vars(args))"""}
    ],
    rw_title="ETL Pipeline CLI",
    rw_scenario="A data engineering team builds a CLI tool to run ETL jobs with configurable sources, targets, and options.",
    rw_code=
"""import argparse, sys

def run_etl(args):
    print(f"ETL Job: {args.job_name}")
    print(f"  Source:   {args.source} (format={args.format})")
    print(f"  Target:   {args.target}")
    print(f"  Batch:    {args.batch_size}")
    print(f"  Dry run:  {args.dry_run}")

    if args.dry_run:
        print("  [DRY RUN] No data written.")
        return 0
    print("  Writing data...")
    return 0

parser = argparse.ArgumentParser(description="ETL Pipeline Runner")
parser.add_argument("job_name",   help="Job identifier")
parser.add_argument("source",     help="Source connection string")
parser.add_argument("target",     help="Target connection string")
parser.add_argument("--format",   choices=["csv","json","parquet"], default="csv")
parser.add_argument("--batch-size", type=int, default=1000, dest="batch_size")
parser.add_argument("--dry-run",  action="store_true", dest="dry_run")

# Demo
args = parser.parse_args([
    "daily_sales", "s3://bucket/sales.parquet", "postgres://db/warehouse",
    "--format", "parquet", "--batch-size", "5000", "--dry-run"
])
sys.exit(run_etl(args))""",
    pt="File Processor CLI",
    pd_text="Build a CLI with two subcommands: (1) count — takes a filename, optional --pattern (regex), prints count of matching lines; (2) summary — takes a filename, --cols (repeatable), prints first/last/count for each column in a CSV. Use argparse with proper help strings and type validation.",
    ps=
"""import argparse, csv, re

parser = argparse.ArgumentParser(prog="fileproc")
subs = parser.add_subparsers(dest="cmd", required=True)

# count subcommand
count_p = subs.add_parser("count", help="Count lines matching pattern")
count_p.add_argument("file")
count_p.add_argument("--pattern", default=".*", help="Regex pattern")

# summary subcommand
sum_p = subs.add_parser("summary", help="Summarize CSV columns")
sum_p.add_argument("file")
sum_p.add_argument("--col", action="append", dest="cols")

def cmd_count(args):
    pattern = re.compile(args.pattern)
    # TODO: open args.file, count lines matching pattern
    pass

def cmd_summary(args):
    # TODO: open CSV, for each col in args.cols, print first/last/count
    pass

args = parser.parse_args(["count", "data.txt", "--pattern", "ERROR"])
if args.cmd == "count":
    cmd_count(args)
elif args.cmd == "summary":
    cmd_summary(args)
"""
)

# ── Section 28: JSON & Data Serialization ───────────────────────────────────
s28 = make_pb(28, "JSON & Data Serialization",
    "Python's json module handles serialization to/from JSON. For Python-specific objects, use pickle. For configuration, use configparser or tomllib.",
    [
        {"label": "json.dumps / loads with custom encoder",
         "code":
"""import json
from datetime import datetime, date
from decimal import Decimal

# Basic usage
data = {"name": "Alice", "scores": [95, 87, 92], "active": True}
text = json.dumps(data, indent=2)
print("JSON string:")
print(text)

loaded = json.loads(text)
print("Loaded back:", loaded)

# Custom encoder for non-serializable types
class AppEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, set):
            return sorted(list(obj))
        return super().default(obj)

record = {
    "created": datetime(2024, 1, 15, 9, 30),
    "price":   Decimal("29.99"),
    "tags":    {"python", "data", "tutorial"},
}

print(json.dumps(record, cls=AppEncoder, indent=2))"""},
        {"label": "Custom decoder and JSON schema validation pattern",
         "code":
"""import json
from datetime import datetime

# Custom decoder using object_hook
def decode_record(d):
    for key, val in d.items():
        # Auto-parse ISO datetime strings
        if isinstance(val, str) and len(val) >= 19 and "T" in val:
            try:
                d[key] = datetime.fromisoformat(val)
            except ValueError:
                pass
    return d

json_str = '''
{
    "id": 42,
    "name": "Order #42",
    "created_at": "2024-01-15T09:30:00",
    "updated_at": "2024-03-20T14:00:00",
    "amount": 299.99
}
'''

obj = json.loads(json_str, object_hook=decode_record)
print("Type of created_at:", type(obj["created_at"]))  # datetime
print("Year:", obj["created_at"].year)

# Simple schema validation pattern
def validate(data, schema):
    errors = []
    for field, expected_type in schema.items():
        if field not in data:
            errors.append(f"Missing: {field}")
        elif not isinstance(data[field], expected_type):
            errors.append(f"{field}: expected {expected_type.__name__}, got {type(data[field]).__name__}")
    return errors

schema = {"id": int, "name": str, "amount": float}
print("Errors:", validate(obj, schema) or "None")"""},
        {"label": "pickle, configparser, and tomllib",
         "code":
"""import pickle, configparser, io

# ─── pickle: serialize any Python object ───────────────────────────────────
class Model:
    def __init__(self, weights):
        self.weights = weights
    def predict(self, x):
        return sum(w * xi for w, xi in zip(self.weights, x))

model = Model([0.5, -0.3, 1.2])
buf = io.BytesIO()

pickle.dump(model, buf)
print("Pickled size:", buf.tell(), "bytes")

buf.seek(0)
loaded_model = pickle.load(buf)
print("Prediction:", loaded_model.predict([1.0, 2.0, 3.0]))

# ─── configparser: INI-format config files ─────────────────────────────────
config_text = '''
[database]
host = localhost
port = 5432
name = mydb

[app]
debug = true
workers = 4
log_level = INFO
'''
cfg = configparser.ConfigParser()
cfg.read_string(config_text)

print("DB host:", cfg["database"]["host"])
print("DB port:", cfg.getint("database", "port"))
print("Debug:  ", cfg.getboolean("app", "debug"))
print("Workers:", cfg.getint("app", "workers"))
print("Sections:", cfg.sections())"""}
    ],
    rw_title="API Response Cache",
    rw_scenario="A data ingestion service serializes API responses to JSON with metadata, then deserializes and validates them on re-read.",
    rw_code=
"""import json, hashlib
from datetime import datetime

class APICache:
    def __init__(self):
        self._store = {}  # in memory; use file I/O in production

    def _key(self, url, params):
        raw = json.dumps({"url": url, "params": params}, sort_keys=True)
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, url, params=None):
        k = self._key(url, params or {})
        if k in self._store:
            entry = json.loads(self._store[k])
            age = (datetime.now() - datetime.fromisoformat(entry["cached_at"])).seconds
            print(f"  [cache hit] age={age}s, key={k[:8]}")
            return entry["data"]
        return None

    def set(self, url, params, data):
        k = self._key(url, params or {})
        entry = {"data": data, "cached_at": datetime.now().isoformat(), "url": url}
        self._store[k] = json.dumps(entry)
        print(f"  [cache set] key={k[:8]}")

cache = APICache()
url = "https://api.example.com/prices"
params = {"symbol": "AAPL", "period": "1d"}

result = cache.get(url, params)
if result is None:
    data = {"symbol": "AAPL", "price": 195.50, "volume": 1_200_000}
    cache.set(url, params, data)
    result = data

print("Result:", result)
cache.get(url, params)  # should be cache hit""",
    pt="Config File Manager",
    pd_text="Write a ConfigManager class that loads from a JSON file (on init) and falls back to defaults if the file does not exist. Support get(key, default=None), set(key, value), and save() (writes back to JSON). Write a test that creates a temp file, sets values, saves, reloads, and verifies.",
    ps=
"""import json, pathlib

class ConfigManager:
    def __init__(self, path, defaults=None):
        self.path = pathlib.Path(path)
        self._data = dict(defaults or {})
        # TODO: if self.path exists, load and merge with self._data
        pass

    def get(self, key, default=None):
        # TODO: return self._data.get(key, default)
        pass

    def set(self, key, value):
        # TODO: update self._data[key] = value
        pass

    def save(self):
        # TODO: write self._data to self.path as JSON (indent=2)
        pass

# Test
import tempfile, os
with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
    json.dump({"theme": "dark"}, f)
    tmp = f.name

cfg = ConfigManager(tmp, defaults={"theme": "light", "font_size": 12})
print("theme:", cfg.get("theme"))      # dark (from file)
print("font:", cfg.get("font_size"))   # 12 (from defaults)
cfg.set("font_size", 14)
cfg.save()

cfg2 = ConfigManager(tmp)
print("reloaded font:", cfg2.get("font_size"))  # 14
os.unlink(tmp)
"""
)

# ── Section 29: Pathlib & File System Ops ───────────────────────────────────
s29 = make_pb(29, "Pathlib & File System Ops",
    "pathlib.Path is the modern way to handle filesystem paths in Python. It's cross-platform, object-oriented, and integrates with all standard file operations.",
    [
        {"label": "Path manipulation and navigation",
         "code":
"""from pathlib import Path

# Create a Path object — cross-platform!
p = Path("/home/user/data/sales_2024.csv")

# Path components
print("name:       ", p.name)         # sales_2024.csv
print("stem:       ", p.stem)         # sales_2024
print("suffix:     ", p.suffix)       # .csv
print("suffixes:   ", Path("a.tar.gz").suffixes)  # ['.tar', '.gz']
print("parent:     ", p.parent)       # /home/user/data
print("parts:      ", p.parts)

# Building paths with / operator
base    = Path("/home/user")
data    = base / "data"
outfile = data / "reports" / "q1.xlsx"
print("Built path:", outfile)

# Resolve, absolute, relative_to
cwd = Path.cwd()
print("CWD:", cwd)
print("Home:", Path.home())

# Check existence
print("exists:", p.exists())
print("is_file:", p.is_file())
print("is_dir: ", p.is_dir())

# Change suffix
renamed = p.with_suffix(".parquet")
print("With new suffix:", renamed)"""},
        {"label": "Glob patterns and directory walking",
         "code":
"""import tempfile, pathlib

# Create a temp directory structure for demo
tmp = pathlib.Path(tempfile.mkdtemp())
(tmp / "data").mkdir()
(tmp / "data" / "sales.csv").write_text("a,b")
(tmp / "data" / "costs.csv").write_text("c,d")
(tmp / "reports").mkdir()
(tmp / "reports" / "q1.xlsx").write_text("x")
(tmp / "reports" / "q2.xlsx").write_text("y")
(tmp / "config.json").write_text("{}")

# glob: match in one directory
csvs = list(tmp.glob("data/*.csv"))
print("CSVs:", [f.name for f in csvs])

# rglob: recursive glob
all_files = list(tmp.rglob("*"))
print("All files:")
for f in sorted(all_files):
    print("  ", f.relative_to(tmp))

# Filter only files (not directories)
only_files = [f for f in tmp.rglob("*") if f.is_file()]
print("File count:", len(only_files))

# Cleanup
import shutil
shutil.rmtree(tmp)
print("Temp dir removed")"""},
        {"label": "Reading, writing, and file operations",
         "code":
"""import tempfile, pathlib, shutil

tmp = pathlib.Path(tempfile.mkdtemp())

# Write and read text
(tmp / "hello.txt").write_text("Hello, World!")
content = (tmp / "hello.txt").read_text()
print("read_text:", content)

# Write and read bytes
(tmp / "data.bin").write_bytes(b"\\x00\\x01\\x02\\x03")
raw = (tmp / "data.bin").read_bytes()
print("read_bytes:", raw.hex())

# Open with context manager for large files
log = tmp / "log.txt"
with log.open("w") as f:
    for i in range(5):
        f.write(f"line {i}\\n")

with log.open() as f:
    for line in f:
        print(" ", line.rstrip())

# stat: file metadata
s = log.stat()
print(f"Size: {s.st_size} bytes")

# mkdir, rename, unlink, shutil operations
(tmp / "subdir").mkdir(parents=True, exist_ok=True)
shutil.copy(log, tmp / "subdir" / "log_copy.txt")
print("Copied:", list((tmp / "subdir").iterdir()))

shutil.rmtree(tmp)
print("Done")"""}
    ],
    rw_title="Data File Organizer",
    rw_scenario="A data engineer uses pathlib to scan a raw data directory, classify files by type, and move them to organized subdirectories.",
    rw_code=
"""import tempfile, pathlib, shutil

# Setup demo files
src = pathlib.Path(tempfile.mkdtemp())
for name in ["sales.csv", "costs.csv", "model.pkl", "report.pdf",
             "config.json", "weights.pkl", "notes.txt"]:
    (src / name).write_text(f"content of {name}")

print("Input files:", [f.name for f in sorted(src.iterdir())])

# Classification map
TYPE_MAP = {
    ".csv":  "data",
    ".pkl":  "models",
    ".json": "config",
    ".pdf":  "reports",
    ".txt":  "misc",
}

moved = []
for file in src.iterdir():
    if not file.is_file():
        continue
    category = TYPE_MAP.get(file.suffix, "other")
    dest_dir = src / category
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / file.name
    shutil.move(str(file), dest)
    moved.append(f"{file.name} -> {category}/")

for m in moved:
    print(" ", m)

# Show final structure
for subdir in sorted(src.iterdir()):
    if subdir.is_dir():
        print(f"  {subdir.name}/:", [f.name for f in subdir.iterdir()])

shutil.rmtree(src)""",
    pt="Log File Archiver",
    pd_text="Write a function archive_logs(log_dir, archive_dir, days_old=7) that uses pathlib to: (1) find all .log files in log_dir older than days_old days, (2) compress each with shutil.make_archive (or just move for simplicity), (3) move them to archive_dir/YYYY-MM/ subfolders based on file modification date. Return a list of moved files.",
    ps=
"""import pathlib, shutil, tempfile
from datetime import datetime, timedelta

def archive_logs(log_dir, archive_dir, days_old=7):
    log_dir     = pathlib.Path(log_dir)
    archive_dir = pathlib.Path(archive_dir)
    cutoff      = datetime.now() - timedelta(days=days_old)
    moved       = []

    for log_file in log_dir.glob("*.log"):
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        if mtime < cutoff:
            # TODO: create archive_dir/YYYY-MM/ folder
            # TODO: move log_file there
            # TODO: append (log_file.name, dest) to moved
            pass

    return moved

# Demo setup
import os, time
tmp_logs    = pathlib.Path(tempfile.mkdtemp())
tmp_archive = pathlib.Path(tempfile.mkdtemp())

# Create fake old log files
for i in range(3):
    f = tmp_logs / f"app_{i}.log"
    f.write_text(f"log content {i}")
    # Make it 10 days old
    old_time = time.time() - 10 * 86400
    os.utime(f, (old_time, old_time))

(tmp_logs / "recent.log").write_text("recent")  # should NOT be archived

result = archive_logs(tmp_logs, tmp_archive, days_old=7)
print("Archived:", result)
shutil.rmtree(tmp_logs); shutil.rmtree(tmp_archive)
"""
)

# ── Section 30: String Formatting Mastery ───────────────────────────────────
s30 = make_pb(30, "String Formatting Mastery",
    "Master Python's string formatting mini-language: f-strings, format(), format spec DSL, textwrap, and Template strings for safe user-controlled formatting.",
    [
        {"label": "f-string advanced features and format spec",
         "code":
"""# Format spec: [[fill]align][sign][z][#][0][width][grouping][.precision][type]
pi = 3.14159265358979

# Width, precision, type
print(f"{pi:.2f}")        # 3.14
print(f"{pi:10.4f}")      # right-aligned in width 10
print(f"{pi:<10.4f}|")    # left-aligned
print(f"{pi:^10.4f}|")    # center-aligned
print(f"{pi:+.3f}")       # force + sign

# Integer formatting
n = 1_234_567
print(f"{n:,}")            # 1,234,567
print(f"{n:_}")            # 1_234_567
print(f"{n:>15,}")         # right-aligned width 15
print(f"{255:#x}")         # 0xff  hex with prefix
print(f"{255:08b}")        # 11111111  binary, zero-padded

# Percentage
print(f"{0.857:.1%}")      # 85.7%

# Datetime in f-string
from datetime import datetime
now = datetime(2024, 3, 15, 9, 5, 7)
print(f"{now:%Y-%m-%d %H:%M:%S}")  # 2024-03-15 09:05:07
print(f"{now:%B %d, %Y}")          # March 15, 2024

# Expression in f-string
data = [1, 2, 3, 4, 5]
print(f"Mean: {sum(data)/len(data):.2f}, Max: {max(data)}")

# Self-documenting expressions (Python 3.8+)
x = 42
print(f"{x=}")   # x=42"""},
        {"label": "textwrap, Template, and str methods",
         "code":
"""import textwrap
from string import Template

# textwrap.wrap / fill: wrap long text
long_text = ("Python is a high-level, interpreted, general-purpose programming language. "
             "Its design philosophy emphasizes code readability with the use of significant indentation.")

wrapped = textwrap.fill(long_text, width=50)
print(wrapped)
print()

# Dedent: remove common leading whitespace (useful after triple-quote strings)
indented = '''
    def foo():
        return 42
    '''
print(repr(textwrap.dedent(indented).strip()))

# Template: safe for user-provided format strings (no code execution risk)
tmpl = Template("Hello $name, your balance is $$${balance:.2f}")
print(tmpl.substitute(name="Alice", balance=1234.56))

# safe_substitute: does not raise for missing keys
tmpl2 = Template("Dear $name, ref: $ref_id")
print(tmpl2.safe_substitute(name="Bob"))  # $ref_id stays

# str methods useful for formatting
cols = ["id", "name", "price", "qty"]
print(" | ".join(c.ljust(10) for c in cols))
print("-" * 45)
row = [1, "apple", 1.20, 50]
print(" | ".join(str(v).ljust(10) for v in row))"""},
        {"label": "Building tables and reports with format()",
         "code":
"""# format() with the mini-language directly
print(format(3.14159, ".2f"))
print(format(1234567, ","))
print(format("hello", ">20"))

# Building a text table
headers = ["Product", "Qty", "Price", "Total"]
rows = [
    ("Apple",    50, 1.20, 60.00),
    ("Banana",  200, 0.50, 100.00),
    ("Cherry",   30, 2.00, 60.00),
    ("Durian",    5, 8.75, 43.75),
]

# Column widths
w = [12, 6, 8, 10]
fmt_h = "  ".join(f"{h:>{ww}}" for h, ww in zip(headers, w))
sep   = "  ".join("-"*ww for ww in w)
print(fmt_h)
print(sep)
for row in rows:
    vals = [f"{row[0]:<{w[0]}}", f"{row[1]:>{w[1]}",
            f"{row[2]:>{w[2]}.2f}", f"{row[3]:>{w[3]}.2f}"]
    print("  ".join(vals))

total = sum(r[3] for r in rows)
print(sep)
print(f"{'TOTAL':>{sum(w)+6}}: {total:.2f}")"""}
    ],
    rw_title="Report Generator",
    rw_scenario="A finance team generates formatted summary reports from sales data using f-strings and textwrap.",
    rw_code=
"""from datetime import date
import textwrap

def format_report(title, data, width=60):
    border  = "=" * width
    today   = date.today().strftime("%B %d, %Y")
    lines   = [border, f"  {title}".center(width), f"  Generated: {today}".center(width), border, ""]

    # Summary stats
    totals  = [r["revenue"] for r in data]
    lines  += [
        f"  {'Region':<15} {'Revenue':>12} {'Units':>8} {'Avg/Unit':>10}",
        "  " + "-" * (width - 2),
    ]

    for r in data:
        avg = r["revenue"] / r["units"] if r["units"] else 0
        lines.append(
            f"  {r['region']:<15} ${r['revenue']:>11,.0f} {r['units']:>8,} ${avg:>9.2f}"
        )

    lines += ["  " + "-" * (width - 2),
              f"  {'TOTAL':<15} ${sum(totals):>11,.0f}",
              "", border]
    return "\\n".join(lines)

data = [
    {"region": "North",  "revenue": 1_450_000, "units": 9_800},
    {"region": "South",  "revenue":   980_000, "units": 7_200},
    {"region": "East",   "revenue": 2_100_000, "units": 14_500},
    {"region": "West",   "revenue": 1_750_000, "units": 11_000},
]

print(format_report("Q1 2024 Sales Report", data))""",
    pt="Invoice Formatter",
    pd_text="Write a function format_invoice(company, items, tax_rate) where items is a list of (desc, qty, unit_price) tuples. Print a formatted invoice with: header (company name, date), line items table (description, qty, unit price, line total), subtotal, tax amount, and grand total. Use f-strings with format specs for alignment.",
    ps=
"""from datetime import date

def format_invoice(company, items, tax_rate=0.08):
    today    = date.today()
    subtotal = sum(qty * price for _, qty, price in items)
    tax      = subtotal * tax_rate
    total    = subtotal + tax

    w = 55
    print("=" * w)
    print(f"  {company}".center(w))
    print(f"  Invoice Date: {today}".center(w))
    print("=" * w)
    print(f"  {'Description':<22} {'Qty':>4} {'Unit':>8} {'Total':>10}")
    print("  " + "-" * (w-2))

    for desc, qty, price in items:
        # TODO: print each line with f-string formatting
        pass

    print("  " + "-" * (w-2))
    # TODO: print subtotal, tax, and grand total rows
    print("=" * w)

format_invoice("Acme Corp", [
    ("Python Training",  1, 2500.00),
    ("Jupyter Setup",    3,  150.00),
    ("Cloud Credits",   10,   49.99),
], tax_rate=0.09)
"""
)

# ── Section 31: Performance Optimization & Caching ──────────────────────────
s31 = make_pb(31, "Performance Optimization & Caching",
    "Profile before optimizing. Use timeit for micro-benchmarks, functools.cache for memoization, __slots__ for memory, and algorithmic improvements for the biggest wins.",
    [
        {"label": "timeit for micro-benchmarking",
         "code":
"""import timeit

# Compare list comprehension vs map() vs for-loop
setup = "data = list(range(10_000))"

t_comp  = timeit.timeit("[x**2 for x in data]",      setup=setup, number=1000)
t_map   = timeit.timeit("list(map(lambda x: x**2, data))", setup=setup, number=1000)
t_loop  = timeit.timeit('''
result = []
for x in data:
    result.append(x**2)
''', setup=setup, number=1000)

print(f"List comprehension: {t_comp:.3f}s")
print(f"map(lambda):        {t_map:.3f}s")
print(f"for loop + append:  {t_loop:.3f}s")

# Compare string joining methods
setup2 = "parts = ['a'] * 1000"
t_join  = timeit.timeit("''.join(parts)",        setup=setup2, number=5000)
t_plus  = timeit.timeit("s=''\nfor p in parts: s += p", setup=setup2, number=5000)
print(f"join():     {t_join:.4f}s")
print(f"+=:         {t_plus:.4f}s")
print(f"join speedup: {t_plus/t_join:.1f}x")"""},
        {"label": "functools.cache and lru_cache",
         "code":
"""import functools, time

# lru_cache: memoize with a max size limit
@functools.lru_cache(maxsize=128)
def fib_lru(n):
    if n <= 1: return n
    return fib_lru(n-1) + fib_lru(n-2)

# functools.cache: unlimited cache (Python 3.9+)
@functools.cache
def fib_cache(n):
    if n <= 1: return n
    return fib_cache(n-1) + fib_cache(n-2)

t0 = time.perf_counter()
result = fib_lru(40)
print(f"fib(40) = {result}, lru_cache time: {(time.perf_counter()-t0)*1000:.2f}ms")
print("Cache info:", fib_lru.cache_info())

# cached_property: compute once, then return stored value
class DataStats:
    def __init__(self, data):
        self._data = data

    @functools.cached_property
    def mean(self):
        print("  (computing mean...)")
        return sum(self._data) / len(self._data)

    @functools.cached_property
    def std(self):
        print("  (computing std...)")
        m = self.mean
        return (sum((x-m)**2 for x in self._data) / len(self._data)) ** 0.5

ds = DataStats(list(range(1000)))
print("mean:", ds.mean)
print("mean:", ds.mean)  # no recompute
print("std: ", ds.std)"""},
        {"label": "Algorithmic improvements and built-in speed",
         "code":
"""import timeit, collections

# O(n) lookup with set vs list
data_list = list(range(10_000))
data_set  = set(data_list)

t_list = timeit.timeit("9999 in data_list", globals=locals(), number=100_000)
t_set  = timeit.timeit("9999 in data_set",  globals=locals(), number=100_000)
print(f"list 'in': {t_list:.4f}s")
print(f"set  'in': {t_set:.4f}s")
print(f"Set speedup: {t_list/t_set:.0f}x")

# Counter vs manual counting
words = "the quick brown fox jumps over the lazy dog the fox".split()

t_manual = timeit.timeit('''
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
''', globals={"words": words}, number=50_000)

t_counter = timeit.timeit("collections.Counter(words)",
                           globals={"collections": collections, "words": words},
                           number=50_000)
print(f"Manual count: {t_manual:.4f}s")
print(f"Counter:      {t_counter:.4f}s")

# Use sorted() key function instead of cmp
records = [{"name": n, "score": s} for n, s in [("Bob", 72), ("Alice", 95), ("Charlie", 88)]]
sorted_records = sorted(records, key=lambda r: r["score"], reverse=True)
for r in sorted_records:
    print(f"  {r['name']:10s}: {r['score']}")"""}
    ],
    rw_title="DataFrame-like Aggregator",
    rw_scenario="A custom data aggregation class uses caching and efficient data structures to compute statistics on large datasets without pandas.",
    rw_code=
"""import functools, collections, statistics

class FastAggregator:
    def __init__(self, records):
        self._records = records
        self._by_key  = None  # lazy

    def _ensure_index(self):
        if self._by_key is None:
            self._by_key = collections.defaultdict(list)
            for r in self._records:
                self._by_key[r["group"]].append(r["value"])

    @functools.cached_property
    def group_means(self):
        self._ensure_index()
        return {k: statistics.mean(v) for k, v in self._by_key.items()}

    @functools.cached_property
    def group_counts(self):
        self._ensure_index()
        return {k: len(v) for k, v in self._by_key.items()}

    @functools.cached_property
    def overall_mean(self):
        vals = [r["value"] for r in self._records]
        return statistics.mean(vals)

import random
random.seed(42)
records = [{"group": f"G{i%5}", "value": random.gauss(50, 10)} for i in range(10_000)]

agg = FastAggregator(records)
print("Group means:", {k: f"{v:.2f}" for k, v in agg.group_means.items()})
print("Group counts:", agg.group_counts)
print("Overall mean:", f"{agg.overall_mean:.2f}")
print("(Accessing again — no recompute):", f"{agg.overall_mean:.2f}")""",
    pt="Benchmark Challenge",
    pd_text="Write three versions of a function find_duplicates(lst) that returns a list of values appearing more than once: (1) brute_force using nested loops O(n^2), (2) sort_based by sorting first O(n log n), (3) hash_based using Counter O(n). Benchmark all three with timeit on a list of 10,000 integers. Report the speedups.",
    ps=
"""import timeit, collections, random

random.seed(42)
data = [random.randint(0, 500) for _ in range(10_000)]

def brute_force(lst):
    dups = set()
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]:
                dups.add(lst[i])
    return list(dups)

def sort_based(lst):
    # TODO: sort, then check adjacent equal elements
    pass

def hash_based(lst):
    # TODO: use collections.Counter, return keys with count > 1
    pass

# Only benchmark sort_based and hash_based (brute force is too slow)
for name, fn in [("sort_based", sort_based), ("hash_based", hash_based)]:
    t = timeit.timeit(lambda: fn(data), number=100)
    print(f"{name}: {t:.4f}s, found {len(fn(data))} duplicates")
"""
)

# ── Section 32: Virtual Environments & Package Management ───────────────────
s32 = make_pb(32, "Virtual Environments & Package Management",
    "Virtual environments isolate project dependencies. pip manages packages, and importlib enables dynamic imports at runtime — essential for building extensible systems.",
    [
        {"label": "venv and pip (commands and concepts)",
         "code":
"""# These commands are run in the terminal (not runnable as Python code)
# They are shown here as strings for educational purposes

venv_commands = '''
# Create a virtual environment
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\\\\Scripts\\\\activate

# Install packages
pip install requests pandas scikit-learn

# Install from requirements file
pip install -r requirements.txt

# Freeze current environment
pip freeze > requirements.txt

# Upgrade a package
pip install --upgrade numpy

# Show installed packages
pip list
pip show numpy

# Deactivate
deactivate
'''

# requirements.txt format:
req_txt = '''
# requirements.txt
numpy>=1.24,<2.0
pandas==2.1.0
scikit-learn>=1.3
requests>=2.31
matplotlib>=3.7; python_version >= "3.9"
'''

# pyproject.toml format (modern, preferred):
pyproject_toml = '''
[project]
name = "my-ml-project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.24",
    "pandas>=2.1",
    "scikit-learn>=1.3",
]

[project.optional-dependencies]
dev = ["pytest", "black", "mypy"]
'''

print("Common venv workflow:")
for cmd in ["python -m venv .venv", "source .venv/bin/activate", "pip install -r requirements.txt"]:
    print(f"  $ {cmd}")"""},
        {"label": "importlib: dynamic imports at runtime",
         "code":
"""import importlib, sys

# Basic dynamic import
math = importlib.import_module("math")
print("sqrt(16):", math.sqrt(16))

# Import a submodule
pprint = importlib.import_module("pprint")
pprint.pprint({"a": 1, "b": [2, 3]})

# Conditional import: use fast version if available
def import_or_fallback(preferred, fallback):
    try:
        return importlib.import_module(preferred)
    except ImportError:
        print(f"  {preferred} not found, using {fallback}")
        return importlib.import_module(fallback)

json_mod = import_or_fallback("ujson", "json")  # ujson is faster if installed
print("json module:", json_mod.__name__)

# importlib.util: check if a module is available without importing it
import importlib.util

for pkg in ["numpy", "pandas", "flask", "fastapi", "nonexistent_pkg"]:
    spec = importlib.util.find_spec(pkg)
    status = "installed" if spec else "NOT installed"
    print(f"  {pkg:<20} {status}")"""},
        {"label": "Package structure and __init__.py",
         "code":
"""import tempfile, pathlib, sys, importlib

# Create a minimal package structure in a temp directory
tmp = pathlib.Path(tempfile.mkdtemp())
pkg = tmp / "mypackage"
pkg.mkdir()

# Package init
(pkg / "__init__.py").write_text('''
__version__ = "1.0.0"
from mypackage.utils import add, multiply
''')

(pkg / "utils.py").write_text('''
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
''')

(pkg / "models.py").write_text('''
class LinearModel:
    def __init__(self, slope=1, intercept=0):
        self.slope = slope
        self.intercept = intercept

    def predict(self, x):
        return self.slope * x + self.intercept
''')

# Add tmp to path so Python can find our package
sys.path.insert(0, str(tmp))

# Import our package
mypackage = importlib.import_module("mypackage")
print("Version:", mypackage.__version__)
print("add:", mypackage.add(3, 4))
print("multiply:", mypackage.multiply(3, 4))

models = importlib.import_module("mypackage.models")
m = models.LinearModel(slope=2.5, intercept=-1)
print("predict(10):", m.predict(10))

sys.path.pop(0)
import shutil; shutil.rmtree(tmp)"""}
    ],
    rw_title="Plugin Loader System",
    rw_scenario="An application dynamically loads analysis plugins from a directory at startup using importlib, without hardcoding plugin names.",
    rw_code=
"""import importlib, importlib.util, pathlib, sys, tempfile, shutil

# Create plugin directory with two demo plugins
tmp = pathlib.Path(tempfile.mkdtemp())
plugin_dir = tmp / "plugins"
plugin_dir.mkdir()

(plugin_dir / "plugin_stats.py").write_text('''
def run(data):
    n = len(data)
    mean = sum(data) / n
    return {"plugin": "stats", "count": n, "mean": round(mean, 2)}
''')

(plugin_dir / "plugin_filter.py").write_text('''
def run(data):
    filtered = [x for x in data if x > 0]
    return {"plugin": "filter", "kept": len(filtered), "dropped": len(data)-len(filtered)}
''')

def load_plugins(plugin_dir):
    plugins = {}
    for path in sorted(pathlib.Path(plugin_dir).glob("plugin_*.py")):
        name = path.stem
        spec = importlib.util.spec_from_file_location(name, path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        plugins[name] = mod
        print(f"  Loaded: {name}")
    return plugins

sys.path.insert(0, str(plugin_dir))
plugins = load_plugins(plugin_dir)

data = [3, -1, 7, 0, -2, 5, 9]
for name, plugin in plugins.items():
    print(f"  {name}: {plugin.run(data)}")

sys.path.pop(0)
shutil.rmtree(tmp)""",
    pt="Dependency Checker",
    pd_text="Write a function check_dependencies(requirements) that takes a list of package names and uses importlib.util.find_spec() to check if each is installed. Return a dict with 'installed' and 'missing' lists. Write another function install_missing(missing) that prints the pip install command needed (don't actually run it — just print it).",
    ps=
"""import importlib.util

def check_dependencies(requirements):
    installed = []
    missing   = []
    for pkg in requirements:
        # Note: package names may differ from import names (e.g. scikit-learn -> sklearn)
        import_name = pkg.replace("-", "_").split(">=")[0].split("==")[0].strip()
        spec = importlib.util.find_spec(import_name)
        if spec:
            installed.append(pkg)
        else:
            missing.append(pkg)
    return {"installed": installed, "missing": missing}

def install_missing(missing):
    # TODO: print pip install command for each missing package
    pass

packages = ["numpy", "pandas", "requests", "flask", "nonexistent_lib", "anotherMissingPkg"]
result = check_dependencies(packages)
print("Installed:", result["installed"])
print("Missing:",   result["missing"])
install_missing(result["missing"])
"""
)

# ── Section 33: Introspection & Metaprogramming ──────────────────────────────
s33 = make_pb(33, "Introspection & Metaprogramming",
    "Python's runtime lets you inspect and modify objects, classes, and functions dynamically. Use inspect, dir(), getattr(), and metaclasses for powerful abstractions.",
    [
        {"label": "dir(), type(), getattr(), hasattr(), inspect",
         "code":
"""import inspect

class Rectangle:
    width: float
    height: float

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

r = Rectangle(4, 6)

# dir() lists all attributes and methods
attrs = [a for a in dir(r) if not a.startswith("_")]
print("Public attrs:", attrs)

# type() and isinstance()
print("type:", type(r).__name__)
print("isinstance(r, Rectangle):", isinstance(r, Rectangle))
print("isinstance(r, object):   ", isinstance(r, object))

# getattr / setattr / hasattr / delattr
for method in ["area", "perimeter", "nonexistent"]:
    if hasattr(r, method):
        fn = getattr(r, method)
        print(f"{method}(): {fn()}")
    else:
        print(f"{method}: not found")

# inspect module
print("Source file:", inspect.getfile(Rectangle))
sig = inspect.signature(Rectangle.__init__)
print("Signature:", sig)
print("Parameters:", list(sig.parameters.keys()))"""},
        {"label": "__dict__, __class__, MRO, and vars()",
         "code":
"""class Animal:
    kingdom = "Animalia"

    def __init__(self, name, species):
        self.name    = name
        self.species = species

    def speak(self):
        return "..."

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Canis lupus familiaris")

    def speak(self):
        return "Woof!"

class GoldenRetriever(Dog):
    breed = "Golden Retriever"

g = GoldenRetriever("Buddy")

# Instance __dict__: instance attributes only
print("Instance __dict__:", g.__dict__)

# Class __dict__: class attributes only
print("Class __dict__ keys:", list(GoldenRetriever.__dict__.keys()))

# vars(): same as __dict__ for objects
print("vars(g):", vars(g))

# Method Resolution Order (MRO)
print("MRO:", [c.__name__ for c in GoldenRetriever.__mro__])

# Class attributes vs instance attributes
print("Class attr 'kingdom':", g.kingdom)  # inherited from Animal
g.kingdom = "override"                      # creates instance attr
print("Instance attr 'kingdom':", g.__dict__["kingdom"])
print("Class still has:", Animal.kingdom)"""},
        {"label": "Metaclasses and __init_subclass__",
         "code":
"""# Metaclass: controls how classes are created

class SingletonMeta(type):
    # Ensure only one instance per class
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class AppConfig(metaclass=SingletonMeta):
    def __init__(self):
        self.debug = False
        self.host  = "localhost"

c1 = AppConfig()
c2 = AppConfig()
c1.debug = True

print("Same object:", c1 is c2)  # True
print("c2.debug:", c2.debug)     # True — same instance!

# __init_subclass__: called when a subclass is defined
class PluginBase:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__.lower()
        PluginBase._registry[name] = cls
        print(f"Registered plugin: {name!r}")

class CSVPlugin(PluginBase, plugin_name="csv"):
    def run(self): return "csv output"

class JSONPlugin(PluginBase, plugin_name="json"):
    def run(self): return "json output"

print("Registry:", list(PluginBase._registry.keys()))
plugin = PluginBase._registry["csv"]()
print("CSV plugin run:", plugin.run())"""}
    ],
    rw_title="Auto-Documented API",
    rw_scenario="A REST API framework uses introspection to auto-generate documentation from function signatures and docstrings.",
    rw_code=
"""import inspect

class APIRouter:
    def __init__(self):
        self.routes = {}

    def route(self, path, method="GET"):
        def decorator(func):
            sig    = inspect.signature(func)
            doc    = inspect.getdoc(func) or "No description"
            params = {
                name: {"annotation": str(p.annotation.__name__ if p.annotation is not inspect.Parameter.empty else "any"),
                       "default": str(p.default) if p.default is not inspect.Parameter.empty else "required"}
                for name, p in list(sig.parameters.items())[1:]  # skip 'self'
            }
            self.routes[f"{method} {path}"] = {
                "handler": func.__name__,
                "doc":     doc,
                "params":  params,
            }
            return func
        return decorator

    def docs(self):
        for endpoint, info in self.routes.items():
            print(f"\\n{endpoint} -> {info['handler']}")
            print(f"  {info['doc']}")
            for p, meta in info["params"].items():
                print(f"  - {p}: {meta['annotation']} (default={meta['default']})")

router = APIRouter()

@router.route("/users", "GET")
def list_users(limit: int = 20, offset: int = 0):
    # Return paginated list of users.
    pass

@router.route("/users/{id}", "GET")
def get_user(user_id: int, include_meta: bool = False):
    # Fetch a single user by ID.
    pass

router.docs()""",
    pt="Class Inspector",
    pd_text="Write a function inspect_class(cls) that returns a dict with: 'name' (class name), 'bases' (list of base class names), 'mro' (list of names), 'class_attrs' (non-dunder class-level attributes), 'methods' (public methods with their signatures as strings). Test it on a class you define with inheritance.",
    ps=
"""import inspect

def inspect_class(cls):
    result = {
        "name":        cls.__name__,
        "bases":       [b.__name__ for b in cls.__bases__],
        "mro":         [c.__name__ for c in cls.__mro__],
        "class_attrs": {},
        "methods":     {},
    }

    for name, val in cls.__dict__.items():
        if name.startswith("_"):
            continue
        if callable(val):
            sig = inspect.signature(val)
            result["methods"][name] = str(sig)
        else:
            result["class_attrs"][name] = repr(val)

    return result

class Vehicle:
    wheels = 4
    fuel   = "gasoline"

    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

    def drive(self, distance: float) -> float:
        return distance / self.speed

class ElectricCar(Vehicle):
    fuel = "electric"

    def charge(self, hours: int) -> str:
        return f"Charging for {hours}h"

for cls in [Vehicle, ElectricCar]:
    info = inspect_class(cls)
    print(f"\\n{info['name']}:")
    print(f"  bases: {info['bases']}")
    print(f"  attrs: {info['class_attrs']}")
    print(f"  methods: {info['methods']}")
"""
)

# ── Section 34: Advanced Type Hints ─────────────────────────────────────────
s34 = make_pb(34, "Advanced Type Hints",
    "Python's typing module enables static analysis with TypeVar, Generic, Protocol, overload, and Literal. Well-typed code is self-documenting and catches bugs before runtime.",
    [
        {"label": "TypeVar and Generic classes",
         "code":
"""from typing import TypeVar, Generic, Iterable, Optional

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# Generic function: type-safe identity
def first(items: list[T]) -> Optional[T]:
    return items[0] if items else None

print(first([1, 2, 3]))        # int
print(first(["a", "b"]))       # str
print(first([]))               # None

# Generic class: type-safe stack
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Optional[T]:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)

int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
int_stack.push(3)
print("peek:", int_stack.peek())  # 3
print("pop: ", int_stack.pop())   # 3
print("len: ", len(int_stack))    # 2"""},
        {"label": "Union, Optional, Literal, Final, TypeAlias",
         "code":
"""from typing import Union, Optional, Literal, Final
import sys

# Union: accepts multiple types (Python 3.10+: int | str)
def process(value: Union[int, str, float]) -> str:
    return f"Got {type(value).__name__}: {value}"

print(process(42))
print(process("hello"))
print(process(3.14))

# Optional[T] is shorthand for Union[T, None]
def find_user(user_id: int) -> Optional[dict]:
    db = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return db.get(user_id)

user = find_user(1)
if user:
    print("Found:", user["name"])

# Literal: restrict to specific values
Mode = Literal["read", "write", "append"]

def open_file(path: str, mode: Mode) -> str:
    return f"Opening {path} in {mode} mode"

print(open_file("data.csv", "read"))

# Final: constant that cannot be reassigned
MAX_RETRIES: Final = 3
API_URL:     Final[str] = "https://api.example.com"

# TypeAlias (Python 3.10+)
if sys.version_info >= (3, 10):
    from typing import TypeAlias
    Vector: TypeAlias = list[float]
    Matrix: TypeAlias = list[list[float]]

print(f"MAX_RETRIES: {MAX_RETRIES}")"""},
        {"label": "@overload for multiple signatures",
         "code":
"""from typing import overload, Union

# @overload allows multiple type signatures for the same function
# Only the implementation signature uses the body

@overload
def parse(value: str) -> int: ...
@overload
def parse(value: bytes) -> float: ...
@overload
def parse(value: int) -> str: ...

def parse(value: Union[str, bytes, int]) -> Union[int, float, str]:
    if isinstance(value, str):
        return int(value)
    elif isinstance(value, bytes):
        return float(value.decode())
    else:
        return str(value)

print(parse("42"))    # int
print(parse(b"3.14")) # float
print(parse(100))     # str

# TypedDict: dict with typed keys
from typing import TypedDict, NotRequired

class UserRecord(TypedDict):
    id:    int
    name:  str
    email: str
    age:   NotRequired[int]  # optional key

def create_user(data: UserRecord) -> str:
    return f"User {data['name']} ({data['email']})"

user: UserRecord = {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30}
print(create_user(user))

user2: UserRecord = {"id": 2, "name": "Bob", "email": "bob@example.com"}
print(create_user(user2))  # age is optional"""}
    ],
    rw_title="Typed Data Pipeline",
    rw_scenario="A production data pipeline uses TypedDict, Generic, and Union to enforce type contracts across stages, catching mismatches early.",
    rw_code=
"""from typing import TypedDict, Generic, TypeVar, Optional, Callable
from dataclasses import dataclass, field

T = TypeVar("T")
R = TypeVar("R")

class RawRecord(TypedDict):
    id:    int
    name:  str
    value: float
    valid: bool

class CleanRecord(TypedDict):
    id:    int
    name:  str
    value: float

@dataclass
class Pipeline(Generic[T, R]):
    steps: list[Callable[[T], R]] = field(default_factory=list)

    def add_step(self, fn: Callable) -> "Pipeline":
        self.steps.append(fn)
        return self

    def run(self, data: list[T]) -> list:
        result = data
        for step in self.steps:
            result = [step(r) for r in result if r is not None]
        return result

def filter_valid(r: RawRecord) -> Optional[RawRecord]:
    return r if r["valid"] and r["value"] > 0 else None

def normalize(r: RawRecord) -> CleanRecord:
    return {"id": r["id"], "name": r["name"].strip().title(), "value": round(r["value"], 2)}

records: list[RawRecord] = [
    {"id": 1, "name": "alice smith",  "value": 129.5,  "valid": True},
    {"id": 2, "name": "BOB JONES",    "value": -5.0,   "valid": False},
    {"id": 3, "name": "  carol lee ", "value": 89.99,  "valid": True},
]

pipeline: Pipeline[RawRecord, CleanRecord] = Pipeline()
pipeline.add_step(filter_valid).add_step(normalize)
result = pipeline.run(records)
for r in result:
    print(f"  {r}")""",
    pt="Generic Result Type",
    pd_text="Implement a generic Result[T, E] class (inspired by Rust) with two states: Ok(value: T) and Err(error: E). Add methods: is_ok(), is_err(), unwrap() (returns value or raises), unwrap_or(default), map(fn) (applies fn to value if Ok, returns new Result). Write tests using Result[int, str].",
    ps=
"""from typing import Generic, TypeVar, Callable, Optional
from dataclasses import dataclass

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")

@dataclass
class Result(Generic[T, E]):
    _value: Optional[T] = None
    _error: Optional[E] = None

    @classmethod
    def ok(cls, value: T) -> "Result[T, E]":
        return cls(_value=value)

    @classmethod
    def err(cls, error: E) -> "Result[T, E]":
        return cls(_error=error)

    def is_ok(self) -> bool:
        return self._error is None

    def is_err(self) -> bool:
        return self._error is not None

    def unwrap(self) -> T:
        if self.is_err():
            raise ValueError(f"Called unwrap on Err: {self._error}")
        return self._value

    def unwrap_or(self, default: T) -> T:
        # TODO: return value if ok, else default
        pass

    def map(self, fn: Callable[[T], U]) -> "Result[U, E]":
        # TODO: if ok, return Result.ok(fn(self._value)), else return self
        pass

# Tests
r1 = Result.ok(42)
r2 = Result.err("not found")

print(r1.is_ok(), r1.unwrap())
print(r2.is_err(), r2.unwrap_or(-1))
print(r1.map(lambda x: x * 2).unwrap())
try:    r2.unwrap()
except ValueError as e: print("Caught:", e)
"""
)

# ── Assemble and insert ──────────────────────────────────────────────────────
all_sections = s27 + s28 + s29 + s30 + s31 + s32 + s33 + s34

result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: sections 27-34 added to gen_python_basics.py")
else:
    print("FAILED: check marker and file")
