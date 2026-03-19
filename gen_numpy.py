#!/usr/bin/env python3
"""Generate NumPy study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\01_numpy")
BASE.mkdir(parents=True, exist_ok=True)

ACCENT = "#79c0ff"
EMOJI  = "🔢"
TITLE  = "NumPy"

# ─── Reusable builders (same as python basics) ───────────────────────────────
def make_html(sections):
    nav = "\n    ".join(
        f'<li><a href="#s{i}" onclick="act(this,event)">{esc(s["title"])}</a></li>'
        for i, s in enumerate(sections)
    )
    cards = ""
    for i, s in enumerate(sections):
        blks = ""
        for j, ex in enumerate(s.get("examples", [])):
            cid = f"c{i}_{j}"
            blks += (
                f'<div class="code-block">'
                f'<div class="ch"><span>{esc(ex.get("label","Example"))}</span>'
                f'<button onclick="cp(\'{cid}\')">Copy</button></div>'
                f'<pre><code id="{cid}" class="language-python">{esc(ex["code"])}</code></pre>'
                f'</div>'
            )
        rw = s.get("rw", {})
        rw_html = ""
        if rw:
            rw_html = (
                f'<div class="rw">'
                f'<div class="rh">&#x1F4BC; Real-World: {esc(rw["title"])}</div>'
                f'<div class="rd">{esc(rw["scenario"])}</div>'
                f'<pre><code class="language-python">{esc(rw["code"])}</code></pre>'
                f'</div>'
            )
        practice = s.get("practice", {})
        practice_html = ""
        if practice:
            pid = f"p{i}"
            practice_html = (
                f'<div class="practice">'
                f'<div class="ph">&#x1F3CB;&#xFE0F; Practice: {esc(practice["title"])}</div>'
                f'<div class="pd">{esc(practice["desc"])}</div>'
                f'<div class="code-block"><div class="ch"><span>Starter Code</span>'
                f'<button onclick="cp(\'{pid}\')">Copy</button></div>'
                f'<pre><code id="{pid}" class="language-python">{esc(practice["starter"])}</code></pre></div>'
                f'</div>'
            )
        cards += (
            f'<div class="topic" id="s{i}">'
            f'<div class="th" onclick="tog(this)"><span>{esc(s["title"])}</span>'
            f'<span class="arr">&#9660;</span></div>'
            f'<div class="tb"><p class="desc">{esc(s.get("desc",""))}</p>'
            f'{blks}{rw_html}{practice_html}</div></div>'
        )
    n = len(sections)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE} Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{{--bg:#0f1117;--sb:#161b22;--card:#1c2128;--brd:#30363d;--txt:#c9d1d9;--mut:#8b949e;--acc:{ACCENT}}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{display:flex;min-height:100vh;background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px}}
.sidebar{{width:260px;min-height:100vh;background:var(--sb);border-right:1px solid var(--brd);position:sticky;top:0;height:100vh;overflow-y:auto;flex-shrink:0}}
.sbh{{padding:20px;border-bottom:1px solid var(--brd)}}
.sbh h2{{font-size:1.05rem;color:var(--acc)}}
.sbh p{{font-size:.8rem;color:var(--mut);margin-top:3px}}
#q{{width:100%;padding:7px 10px;background:#0d1117;border:1px solid var(--brd);border-radius:6px;color:var(--txt);font-size:.84rem;margin-top:10px}}
#q:focus{{outline:none;border-color:var(--acc)}}
.nav-list{{list-style:none;padding:6px 0}}
.nav-list li a{{display:block;padding:7px 18px;color:var(--mut);text-decoration:none;font-size:.84rem;border-left:3px solid transparent;transition:.15s}}
.nav-list li a:hover,.nav-list li a.active{{color:var(--txt);border-left-color:var(--acc);background:rgba(255,255,255,.03)}}
.main{{flex:1;padding:32px 40px;max-width:880px}}
.pt{{font-size:2rem;font-weight:700;color:var(--acc);margin-bottom:6px}}
.ps{{color:var(--mut);margin-bottom:28px}}
.topic{{background:var(--card);border:1px solid var(--brd);border-radius:8px;margin-bottom:14px;overflow:hidden}}
.th{{display:flex;justify-content:space-between;align-items:center;padding:13px 18px;cursor:pointer;user-select:none}}
.th:hover{{background:rgba(255,255,255,.04)}}
.th>span:first-child{{font-weight:600}}
.arr{{color:var(--mut);transition:transform .2s}}
.tb{{display:none;padding:18px;border-top:1px solid var(--brd)}}
.tb.open{{display:block}}
.arr.open{{transform:rotate(180deg)}}
.desc{{color:var(--mut);margin-bottom:14px;line-height:1.6;font-size:.92rem}}
.code-block{{margin-bottom:14px;border:1px solid var(--brd);border-radius:6px;overflow:hidden}}
.ch{{display:flex;justify-content:space-between;padding:7px 12px;background:#161b22;font-size:.78rem;color:var(--mut)}}
.ch button{{background:0;border:1px solid var(--brd);color:var(--mut);padding:2px 9px;border-radius:4px;cursor:pointer;font-size:.73rem}}
.ch button:hover{{color:var(--txt);border-color:var(--acc)}}
pre{{margin:0}}pre code{{font-size:.83rem;padding:13px!important}}
.rw{{background:#0d2818;border:1px solid #238636;border-radius:6px;padding:15px;margin-top:6px}}
.rh{{font-weight:600;color:#3fb950;margin-bottom:7px}}
.rd{{color:#7ee787;font-size:.84rem;margin-bottom:11px;line-height:1.5}}
.practice{{background:#0d1b2a;border:1px solid #388bfd;border-radius:6px;padding:15px;margin-top:8px}}
.ph{{font-weight:600;color:#58a6ff;margin-bottom:7px}}
.pd{{color:#79c0ff;font-size:.84rem;margin-bottom:11px;line-height:1.5}}
</style></head><body>
<aside class="sidebar">
  <div class="sbh"><h2>{EMOJI} {TITLE}</h2><p>Study Guide &bull; {n} topics</p>
    <input id="q" placeholder="Search..." oninput="filt(this.value)">
  </div>
  <ul class="nav-list" id="nl">{nav}</ul>
</aside>
<main class="main">
  <h1 class="pt">{EMOJI} {TITLE}</h1>
  <p class="ps">{n} topics &bull; Click any card to expand</p>
  {cards}
</main>
<script>
hljs.highlightAll();
function tog(h){{var b=h.nextElementSibling,a=h.querySelector('.arr');b.classList.toggle('open');a.classList.toggle('open');}}
function act(el,e){{if(e)e.preventDefault();document.querySelectorAll('.nav-list a').forEach(a=>a.classList.remove('active'));el.classList.add('active');}}
function filt(q){{document.querySelectorAll('#nl li').forEach(li=>{{li.style.display=li.textContent.toLowerCase().includes(q.toLowerCase())?'':'none';}});}}
function cp(id){{navigator.clipboard.writeText(document.getElementById(id).innerText).catch(()=>{{}});}}
document.addEventListener('DOMContentLoaded',()=>{{var fh=document.querySelector('.th');if(fh)fh.click();var fa=document.querySelector('.nav-list a');if(fa)fa.classList.add('active');}});
</script></body></html>"""


def make_nb(sections):
    cells = []
    n = [0]
    def nid(): n[0]+=1; return f"{n[0]:04d}"
    def md(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"markdown","id":nid(),"metadata":{},"source":s}
    def code(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"code","execution_count":None,"id":nid(),"metadata":{},"outputs":[],"source":s}

    cells.append(md(f"# {TITLE} Study Guide\n\nHands-on guide with practical examples and real-world use cases."))
    for i, s in enumerate(sections, 1):
        cells.append(md(f"## {i}. {s['title']}\n\n{s.get('desc','')}"))
        for ex in s.get("examples", []):
            if ex.get("label"): cells.append(md(f"**{ex['label']}**"))
            cells.append(code(ex["code"]))
        rw = s.get("rw")
        if rw:
            cells.append(md(f"### Real-World: {rw['title']}\n\n> {rw['scenario']}"))
            cells.append(code(rw["code"]))
        practice = s.get("practice")
        if practice:
            cells.append(md(f"### 🏋️ Practice: {practice['title']}\n\n{practice['desc']}"))
            cells.append(code(practice["starter"]))
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name":"Python 3","language":"python","name":"python3"},
            "language_info": {"name":"python","version":"3.11.0"}
        },
        "nbformat": 4, "nbformat_minor": 5
    }


# ─── Content ──────────────────────────────────────────────────────────────────
SECTIONS = [

{
"title": "1. Array Creation",
"desc": "NumPy arrays are the foundation of scientific computing. Create them from lists, ranges, or built-in factory functions.",
"examples": [
{"label": "From lists and factory functions", "code":
"""import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([[1, 2, 3], [4, 5, 6]])   # 2D

zeros = np.zeros((3, 4))               # 3×4 of 0.0
ones  = np.ones((2, 3))                # 2×3 of 1.0
eye   = np.eye(3)                      # 3×3 identity
full  = np.full((2, 2), 7.0)           # filled with 7.0

print("1D:", a)
print("2D shape:", b.shape)
print("Identity:\\n", eye)"""},
{"label": "arange, linspace, logspace", "code":
"""import numpy as np

r   = np.arange(0, 20, 2)          # [0, 2, 4, ..., 18]
pts = np.linspace(0, 1, 5)         # 5 evenly-spaced in [0,1]
log = np.logspace(0, 3, 4)         # [1, 10, 100, 1000]

print("arange:", r)
print("linspace:", pts)
print("logspace:", log)

# Random arrays
rng = np.random.default_rng(42)    # recommended new API
u   = rng.random((3, 3))           # uniform [0,1)
n   = rng.standard_normal((3, 3))  # standard normal
print("Random normal:\\n", n.round(2))"""},
{"label": "np.tile, np.meshgrid, and np.empty", "code":
"""import numpy as np

# Checkerboard pattern using tile
unit = np.array([[0, 1], [1, 0]])
board = np.tile(unit, (4, 4))
print("Checkerboard (8x8):\\n", board)

# meshgrid — create coordinate grids
x = np.linspace(-2, 2, 5)
y = np.linspace(-1, 1, 3)
XX, YY = np.meshgrid(x, y)
print("XX shape:", XX.shape)   # (3, 5)
Z = np.sqrt(XX**2 + YY**2)    # distance from origin
print("Z:\\n", Z.round(2))

# np.empty — uninitialized (fast allocation)
buf = np.empty((3, 3), dtype=np.float64)
print("Empty (garbage values):", buf.shape, buf.dtype)"""},
{"label": "np.fromfunction and structured arrays", "code":
"""import numpy as np

# np.fromfunction — build array from index formula
# Creates a 5x5 multiplication table
mul_table = np.fromfunction(lambda i, j: (i + 1) * (j + 1), (5, 5), dtype=int)
print("Multiplication table:\\n", mul_table)

# Distance matrix from origin using fromfunction
dist = np.fromfunction(lambda i, j: np.sqrt(i**2 + j**2), (4, 4))
print("\\nDistance from (0,0):\\n", dist.round(2))

# Structured arrays — heterogeneous data like a database row
dt = np.dtype([('name', 'U10'), ('age', np.int32), ('score', np.float64)])
students = np.array([
    ('Alice', 23, 92.5),
    ('Bob',   25, 87.3),
    ('Carol', 22, 95.1),
], dtype=dt)
print("\\nStructured array:", students)
print("Names:", students['name'])
print("Top scorer:", students[np.argmax(students['score'])]['name'])"""}
],
"practice": {
"title": "Array Construction Challenge",
"desc": "1) Create a 6x6 checkerboard of 0s and 1s using np.tile. 2) Build a 5x5 identity matrix, then multiply its diagonal by [1,2,3,4,5]. 3) Generate 20 log-spaced points from 10 to 10000 and find the one closest to 500.",
"starter":
"""import numpy as np

# 1. 6x6 checkerboard using np.tile
unit = np.array([[0, 1], [1, 0]])
# TODO: board = np.tile(unit, ???)
# print("Checkerboard:\\n", board)

# 2. 5x5 identity * diagonal scale
eye = np.eye(5)
scale = np.array([1, 2, 3, 4, 5])
# TODO: scaled = eye * ???   (use broadcasting/diag)
# print("Scaled identity:\\n", scaled)

# 3. Log-spaced points, find closest to 500
pts = np.logspace(1, 4, 20)   # 10^1 to 10^4
# TODO: idx = np.argmin(np.abs(pts - 500))
# print(f"Closest to 500: {pts[idx]:.2f} at index {idx}")"""
},
"rw": {
"title": "Feature Matrix for Machine Learning",
"scenario": "A data scientist prepares a feature matrix with a bias column before training a linear model.",
"code":
"""import numpy as np

np.random.seed(42)
n_samples, n_features = 5000, 12
X = np.random.randn(n_samples, n_features)

# Add bias column (ones) for intercept term
bias = np.ones((n_samples, 1))
X_b  = np.hstack([bias, X])

print(f"Feature matrix shape: {X_b.shape}")
print(f"Memory: {X_b.nbytes / 1024:.1f} KB")
print(f"dtype: {X_b.dtype}")
print(f"Sample row[:5]: {X_b[0, :5].round(3)}")"""}
},

{
"title": "2. Array Attributes & Inspection",
"desc": "Every NumPy array carries metadata: shape, dtype, number of dimensions, and memory size. Understanding these prevents bugs.",
"examples": [
{"label": "shape, ndim, dtype, size, nbytes", "code":
"""import numpy as np

a = np.array([[1.5, 2.0, 3.1],
              [4.0, 5.5, 6.2]], dtype=np.float32)

print("shape:   ", a.shape)     # (2, 3)
print("ndim:    ", a.ndim)      # 2
print("dtype:   ", a.dtype)     # float32
print("size:    ", a.size)      # 6  (total elements)
print("itemsize:", a.itemsize)  # 4  (bytes per element)
print("nbytes:  ", a.nbytes)    # 24 (total bytes)
print("Transpose shape:", a.T.shape)"""},
{"label": "Type casting and auto reshape", "code":
"""import numpy as np

a = np.arange(12)           # [0..11]
r = a.reshape(3, 4)
print("Reshaped (3,4):\\n", r)

# -1 auto-infers the dimension
c = a.reshape(2, -1)        # (2, 6)
print("Auto reshape:", c.shape)

# Change dtype
b = a.astype(np.float32)
print("float32 dtype:", b.dtype)

# Flatten back to 1D
print("Flattened:", r.flatten())"""},
{"label": "View vs copy and np.shares_memory", "code":
"""import numpy as np

a = np.arange(10)

# Slice = VIEW (shares memory)
v = a[2:6]
v[0] = 99
print("After modifying view:", a)   # a is changed!

# .copy() = independent copy
c = a[2:6].copy()
c[0] = 0
print("After modifying copy:", a)   # a unchanged

print("View shares memory:", np.shares_memory(a, v))
print("Copy shares memory:", np.shares_memory(a, c))

# reshape also returns a view when possible
r = a.reshape(2, 5)
print("Reshape shares memory:", np.shares_memory(a, r))"""},
{"label": "Memory layout: strides, C vs F order, itemsize", "code":
"""import numpy as np

a = np.arange(12, dtype=np.float64).reshape(3, 4)

# Strides: bytes to step in each dimension
print("Shape:    ", a.shape)
print("Strides:  ", a.strides)   # (32, 8) — 4 float64s per row
print("Itemsize: ", a.itemsize)  # 8 bytes per float64

# C order (row-major, default): last index changes fastest
c_arr = np.ascontiguousarray(a, order='C')
print("\\nC-order strides:", c_arr.strides)   # (32, 8)
print("C contiguous:   ", c_arr.flags['C_CONTIGUOUS'])

# Fortran order (column-major): first index changes fastest
f_arr = np.asfortranarray(a, order='F')
print("\\nF-order strides:", f_arr.strides)   # (8, 24)
print("F contiguous:   ", f_arr.flags['F_CONTIGUOUS'])

# Transpose flips strides — still a view, not a copy
t = a.T
print("\\nTranspose strides:", t.strides)     # (8, 32)
print("Shares memory with original:", np.shares_memory(a, t))"""}
],
"practice": {
"title": "Array Attribute Inspector",
"desc": "Create three arrays of different dtypes (int8, float32, complex128), each shaped (4, 5). For each: print shape, ndim, dtype, itemsize, nbytes, and compute the memory saving vs float64. Then reshape one to (2, 2, 5) and verify shares_memory returns True.",
"starter":
"""import numpy as np

dtypes = [np.int8, np.float32, np.complex128]
base_bytes = np.zeros((4, 5), dtype=np.float64).nbytes

for dt in dtypes:
    arr = np.zeros((4, 5), dtype=dt)
    # TODO: print shape, ndim, dtype, itemsize, nbytes
    # TODO: compute saving vs float64 base_bytes
    print(f"dtype={arr.dtype}: shape={arr.shape}, "
          f"ndim=???, itemsize=???B, nbytes=???B, "
          f"vs float64: ???B saving")

# Reshape and verify view
a = np.arange(20, dtype=np.float32).reshape(4, 5)
# TODO: b = a.reshape(2, 2, 5)
# TODO: print("shares_memory:", np.shares_memory(a, b))"""
},
"rw": {
"title": "Memory Audit of Sensor Arrays",
"scenario": "An IoT engineer compares float64 vs float32 memory for large time-series sensor arrays before storing.",
"code":
"""import numpy as np

sensors = {
    "temperature": np.random.uniform(15, 40, (10000, 24)),
    "pressure":    np.random.uniform(900, 1100, (10000, 24)),
    "humidity":    np.random.uniform(20, 90, (10000, 24)),
}

print(f"{'Sensor':12s} {'float64 MB':>12} {'float32 MB':>12} {'Saved MB':>10}")
print("-" * 50)
for name, arr in sensors.items():
    mb64  = arr.nbytes / 1e6
    mb32  = arr.astype(np.float32).nbytes / 1e6
    print(f"{name:12s} {mb64:>12.3f} {mb32:>12.3f} {mb64-mb32:>10.3f}")"""}
},

{
"title": "3. Indexing & Slicing",
"desc": "NumPy supports element access, slices, fancy (list-based) indexing, and boolean masks — all without Python loops.",
"examples": [
{"label": "1D and 2D indexing", "code":
"""import numpy as np

a = np.arange(10)
print(a[2])           # 2
print(a[-1])          # 9
print(a[2:7])         # [2 3 4 5 6]
print(a[::2])         # every other → [0 2 4 6 8]
print(a[::-1])        # reversed

m = np.arange(12).reshape(3, 4)
print("m[1,2]:", m[1, 2])       # 6
print("col 1:", m[:, 1])        # [1 5 9]
print("sub-matrix:\\n", m[0:2, 1:3])"""},
{"label": "Fancy indexing and np.ix_", "code":
"""import numpy as np

a = np.array([10, 20, 30, 40, 50])
idx = [0, 2, 4]
print("Fancy:", a[idx])              # [10 30 50]

m = np.arange(16).reshape(4, 4)
rows = [0, 1, 2]
cols = [1, 2, 3]
print("Diagonal slice:", m[rows, cols])   # [1 6 11]

# np.ix_ — all row/col combinations
print("Sub-matrix:\\n", m[np.ix_(rows, cols)])"""},
{"label": "Advanced slicing: step, reverse, and np.take", "code":
"""import numpy as np

m = np.arange(25).reshape(5, 5)
print("Every 2nd row, every 2nd col:\\n", m[::2, ::2])
print("Last 2 rows reversed:\\n", m[-1::-2])

# np.take — fancy indexing along axis
data = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
order = [2, 0, 3, 1]   # reorder rows
print("Reordered rows:\\n", np.take(data, order, axis=0))

# Diagonal extraction
print("Main diagonal:", np.diag(m))
print("Offset diagonal:", np.diag(m, k=1))   # one above main

# Set values at fancy indices
arr = np.zeros(10, dtype=int)
arr[[1, 3, 5, 7, 9]] = 1
print("Odd positions set:", arr)"""},
{"label": "np.ix_ for cross-product indexing and scatter/gather", "code":
"""import numpy as np

m = np.arange(25).reshape(5, 5)
print("Matrix:\\n", m)

# np.ix_ — create open mesh for cross-product selection
rows = [0, 2, 4]
cols = [1, 3]
sub = m[np.ix_(rows, cols)]
print("\\nnp.ix_ sub-matrix (rows 0,2,4 x cols 1,3):\\n", sub)

# Scatter: write to all combinations of row/col indices
target = np.zeros((5, 5), dtype=int)
target[np.ix_(rows, cols)] = 9
print("\\nAfter scatter write:\\n", target)

# Gather: collect multiple blocks from a 3D array
batch = np.arange(60).reshape(3, 4, 5)  # 3 matrices of (4,5)
sample_rows = [0, 2]
sample_cols = [1, 3, 4]
# Extract a sub-block from each matrix in the batch
gathered = batch[:, np.ix_(sample_rows, sample_cols)[0],
                    np.ix_(sample_rows, sample_cols)[1]]
print("\\nBatch gather shape:", gathered.shape)  # (3, 2, 3)
print("First matrix block:\\n", gathered[0])"""}
],
"practice": {
"title": "Matrix Surgery",
"desc": "Create a 6x6 matrix from arange(36). Using only indexing (no loops): 1) Extract the 2x2 center block (rows 2-3, cols 2-3). 2) Extract the main diagonal. 3) Set all values > 25 to -1. 4) Extract every other element from the last row.",
"starter":
"""import numpy as np

m = np.arange(36).reshape(6, 6)
print("Original:\\n", m)

# 1. Extract 2x2 center block (rows 2-3, cols 2-3)
# TODO: center = m[???, ???]
# print("Center:\\n", center)

# 2. Main diagonal
# TODO: diag = np.diag(m)
# print("Diagonal:", diag)

# 3. Set all values > 25 to -1 (in-place boolean indexing)
m_copy = m.copy()
# TODO: m_copy[???] = -1
# print("After masking >25:\\n", m_copy)

# 4. Every other element from last row
# TODO: every_other = m[-1, ???]
# print("Every other (last row):", every_other)"""
},
"rw": {
"title": "Sliding Window for Anomaly Detection",
"scenario": "An IoT engineer extracts overlapping 24-hour windows from continuous sensor readings to detect anomalies.",
"code":
"""import numpy as np

# 30 days of hourly readings
time_series = np.random.randn(24 * 30) + 20.0   # ~20°C

windows = np.lib.stride_tricks.sliding_window_view(time_series, 24)
print(f"Series: {time_series.shape}  →  Windows: {windows.shape}")

# Find 24-hour window with highest standard deviation
stds     = windows.std(axis=1)
peak_idx = np.argmax(stds)

print(f"Most variable window starts at hour {peak_idx}")
print(f"  std  = {stds[peak_idx]:.3f}")
print(f"  mean = {windows[peak_idx].mean():.2f}°C")
print(f"  range [{windows[peak_idx].min():.1f}, {windows[peak_idx].max():.1f}]")"""}
},

{
"title": "4. Mathematical Operations & Ufuncs",
"desc": "NumPy ufuncs (universal functions) operate element-wise on entire arrays — far faster than Python loops.",
"examples": [
{"label": "Arithmetic and ufuncs", "code":
"""import numpy as np

a = np.array([1.0, 4.0, 9.0, 16.0])
b = np.array([2.0, 2.0, 3.0,  4.0])

print("a + b:", a + b)
print("a * b:", a * b)
print("a ** 2:", a ** 2)
print("sqrt:", np.sqrt(a))
print("log:", np.log(a).round(3))
print("exp:", np.exp([0, 1, 2]).round(3))
print("clip:", np.clip(a, 2, 10))"""},
{"label": "Cumulative and trigonometric ops", "code":
"""import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print("cumsum: ", np.cumsum(arr))
print("cumprod:", np.cumprod(arr))
print("diff:   ", np.diff(arr))

x = np.linspace(-np.pi, np.pi, 5)
print("sin:", np.sin(x).round(2))
print("cos:", np.cos(x).round(2))

a = np.array([-3, -1, 0, 1, 3])
print("abs: ", np.abs(a))
print("sign:", np.sign(a))"""},
{"label": "np.einsum and vectorized distance", "code":
"""import numpy as np

# einsum — Einstein summation notation
A = np.random.randn(3, 4)
B = np.random.randn(4, 5)

# Matrix multiply: 'ij,jk->ik'
C = np.einsum('ij,jk->ik', A, B)
print("einsum matmul:", C.shape)   # (3, 5)

# Trace (sum of diagonal): 'ii->'
sq = np.random.randn(4, 4)
print("trace:", np.einsum('ii->', sq), "==", np.trace(sq))

# Pairwise squared distances between points
points = np.array([[0,0],[1,0],[0,1],[1,1]], dtype=float)
diff = points[:, None, :] - points[None, :, :]  # (4,4,2)
dist = np.sqrt((diff**2).sum(axis=-1))
print("Distance matrix:\\n", dist.round(3))"""},
{"label": "np.vectorize, np.frompyfunc, and np.piecewise", "code":
"""import numpy as np

# np.vectorize — wrap a scalar Python function for array inputs
def classify(x):
    if x < 0:   return 'negative'
    if x == 0:  return 'zero'
    return 'positive'

v_classify = np.vectorize(classify)
data = np.array([-3, 0, 1, -1, 5])
print("vectorize:", v_classify(data))

# np.frompyfunc — similar but returns object arrays; useful for ufunc chaining
safe_log = np.frompyfunc(lambda x: np.log(x) if x > 0 else np.nan, 1, 1)
vals = np.array([-1.0, 0.0, 1.0, np.e, 10.0])
print("frompyfunc safe_log:", safe_log(vals).astype(float).round(3))

# np.piecewise — vectorized multi-branch function
x = np.linspace(-3, 3, 7)
y = np.piecewise(x,
    [x < -1, (x >= -1) & (x <= 1), x > 1],
    [lambda t: -t,   # x < -1:  y = -x
     lambda t: t**2, # -1<=x<=1: y = x^2
     lambda t: t])   # x > 1:  y = x
print("\\npiecewise input: ", x.round(2))
print("piecewise output:", y.round(2))"""}
],
"practice": {
"title": "Vectorized Math Challenge",
"desc": "1) Given angles in degrees [0, 30, 45, 60, 90, 120, 180], compute sin and cos without a loop. Verify sin²+cos²=1 for all. 2) Given a 1D price array, compute: % daily return, 5-day moving average (using np.convolve), and cumulative return. 3) Use np.clip to cap values between the 10th and 90th percentile.",
"starter":
"""import numpy as np

# 1. Trig on degree array
degrees = np.array([0, 30, 45, 60, 90, 120, 180], dtype=float)
# TODO: radians = degrees * np.pi / 180
# TODO: s, c = np.sin(radians), np.cos(radians)
# TODO: verify = np.allclose(s**2 + c**2, 1)
# print("sin²+cos²==1:", verify)

# 2. Price array stats
np.random.seed(42)
prices = np.cumprod(1 + np.random.normal(0.001, 0.02, 30)) * 100
# TODO: pct_ret = np.diff(prices) / prices[:-1] * 100
# TODO: ma5 = np.convolve(prices, np.ones(5)/5, mode='valid')
# TODO: cum_ret = prices[-1] / prices[0] - 1
# print(f"Cumulative return: {cum_ret:.2%}")

# 3. Winsorize to [p10, p90]
data = np.random.randn(100) * 10
# TODO: p10, p90 = np.percentile(data, [10, 90])
# TODO: clipped = np.clip(data, p10, p90)
# print(f"Original range: [{data.min():.1f}, {data.max():.1f}]")
# print(f"Clipped range:  [{clipped.min():.1f}, {clipped.max():.1f}]")"""
},
"rw": {
"title": "Daily Return & Volatility Calculation",
"scenario": "A quant analyst vectorizes stock return and volatility calculations across a price history array.",
"code":
"""import numpy as np

prices = np.array([100, 102, 98, 105, 103, 110, 108, 115, 112, 118],
                  dtype=np.float64)

# Percentage daily returns
pct_ret = np.diff(prices) / prices[:-1] * 100

# Log returns (additive, good for compounding)
log_ret = np.diff(np.log(prices))

# Annualized volatility (assuming 252 trading days)
ann_vol = log_ret.std() * np.sqrt(252)

# Sharpe-like ratio
sharpe = log_ret.mean() / log_ret.std() * np.sqrt(252)

print(f"Daily returns %: {pct_ret.round(2)}")
print(f"Annualized vol:  {ann_vol:.4f}")
print(f"Sharpe ratio:    {sharpe:.3f}")"""}
},

{
"title": "5. Broadcasting",
"desc": "Broadcasting lets NumPy perform operations on arrays of different shapes without copying data — memory-efficient and fast.",
"examples": [
{"label": "Scalar and vector broadcasting", "code":
"""import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])

print("a + 10:\\n",     a + 10)                      # scalar
print("a * [1,2,3]:\\n", a * np.array([1, 2, 3]))   # row
print("a + [[10],[20]]:\\n",
      a + np.array([[10], [20]]))                    # column"""},
{"label": "Min-max normalization via broadcasting", "code":
"""import numpy as np

X = np.random.randn(100, 5)          # 100 samples, 5 features

# Z-score normalization
mean = X.mean(axis=0)                # shape (5,) — per feature
std  = X.std(axis=0)
X_z  = (X - mean) / std             # (100,5) op (5,) → broadcasts

print("After normalization:")
print("  mean:", X_z.mean(axis=0).round(8))
print("  std: ", X_z.std(axis=0).round(8))

# Min-max normalization
X_mm = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
print("Min-max range:", X_mm.min(axis=0).round(2), "to", X_mm.max(axis=0).round(2))"""},
{"label": "Outer product and pairwise distance via broadcasting", "code":
"""import numpy as np

# Outer product without np.outer
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30])
outer = a[:, None] * b[None, :]    # (4,1) * (1,3) → (4,3)
print("Outer product:\\n", outer)

# All pairwise L2 distances between N points
rng = np.random.default_rng(0)
pts = rng.random((5, 2))           # 5 points in 2D
diff = pts[:, None, :] - pts[None, :, :]  # (5,5,2)
dist = np.sqrt((diff**2).sum(axis=-1))    # (5,5)
print("Distance matrix:\\n", dist.round(3))
print("Nearest neighbor of pt0:", np.argsort(dist[0])[1])"""},
{"label": "Batch matrix multiply with np.matmul and broadcasting rules", "code":
"""import numpy as np

rng = np.random.default_rng(7)

# Batch matrix multiply: (B, M, K) @ (B, K, N) -> (B, M, N)
B, M, K, N = 4, 3, 5, 2
A_batch = rng.random((B, M, K))
W_batch = rng.random((B, K, N))
C_batch = np.matmul(A_batch, W_batch)   # or A_batch @ W_batch
print("Batch matmul:", A_batch.shape, "@", W_batch.shape, "->", C_batch.shape)

# Broadcasting rule visualization: align shapes from the right
# (4, 1, 3) + (   3, 3) -> (4, 3, 3)  — rule: prepend 1s then stretch
x = rng.random((4, 1, 3))
y = rng.random((3, 3))
result = x + y
print("\\nBroadcast (4,1,3) + (3,3) ->", result.shape)

# Shared weight matrix across all batch items: (B,M,K) @ (K,N)
W_shared = rng.random((K, N))           # single weight matrix
C_shared = A_batch @ W_shared           # (4,3,5) @ (5,2) -> (4,3,2)
print("Shared-weight batch:", A_batch.shape, "@", W_shared.shape, "->", C_shared.shape)
print("All batch outputs equal?", False, "(each row of A_batch differs)")"""}
],
"practice": {
"title": "Broadcasting Workout",
"desc": "1) Add a bias column of 1s to a (50, 4) feature matrix using broadcasting/hstack. 2) Compute the softmax of a (3, 5) logit matrix row-wise: exp(x) / sum(exp(x)) — verify each row sums to 1. 3) Subtract the per-row mean from a (4, 6) matrix so each row has zero mean.",
"starter":
"""import numpy as np
np.random.seed(42)

# 1. Add bias column (column of 1s) to feature matrix
X = np.random.randn(50, 4)
# TODO: bias = np.ones((50, 1))
# TODO: X_b = np.hstack([bias, X])
# print("With bias:", X_b.shape)  # (50, 5)

# 2. Row-wise softmax
logits = np.random.randn(3, 5)
# TODO: exp_l = np.exp(logits)
# TODO: softmax = exp_l / exp_l.sum(axis=1, keepdims=True)
# print("Row sums:", softmax.sum(axis=1))  # should be [1. 1. 1.]

# 3. Zero-center each row
M = np.random.randn(4, 6)
# TODO: row_means = M.mean(axis=1, keepdims=True)
# TODO: M_centered = M - row_means
# print("Row means after centering:", M_centered.mean(axis=1).round(10))"""
},
"rw": {
"title": "Batch Image Normalization for CNNs",
"scenario": "A computer vision engineer normalizes a batch of RGB images using channel-wise ImageNet statistics.",
"code":
"""import numpy as np

# Simulate batch: (N=32, H=64, W=64, C=3)
images = np.random.randint(0, 256, (32, 64, 64, 3), dtype=np.uint8)

# ImageNet channel means and stds (R, G, B)
mean_rgb = np.array([0.485, 0.456, 0.406])
std_rgb  = np.array([0.229, 0.224, 0.225])

# Scale to [0,1] then normalize — broadcasting: (32,64,64,3) op (3,)
normalized = (images.astype(np.float32) / 255.0 - mean_rgb) / std_rgb

print(f"Input:  {images.shape}  dtype={images.dtype}")
print(f"Output: {normalized.shape}  dtype={normalized.dtype}")
print(f"Range:  [{normalized.min():.3f}, {normalized.max():.3f}]")
print(f"Per-channel mean: {normalized.mean(axis=(0,1,2)).round(3)}")"""}
},

{
"title": "6. Boolean Indexing & np.where",
"desc": "Filter arrays with boolean conditions. np.where and np.select let you apply transformations without explicit loops.",
"examples": [
{"label": "Boolean masks", "code":
"""import numpy as np

a = np.array([10, 25, 3, 47, 18, 32, 5])

mask = a > 20
print("Mask:     ", mask)
print("Values>20:", a[mask])

# Modify in-place
a[a < 10] = 0
print("After zero small:", a)

# Multiple conditions
b = np.arange(20)
print("5 to 15:", b[(b >= 5) & (b <= 15)])"""},
{"label": "np.where and np.select", "code":
"""import numpy as np

scores = np.array([45, 78, 55, 90, 33, 68, 82])

# np.where — binary choice
grade = np.where(scores >= 60, "Pass", "Fail")
print("Pass/Fail:", grade)

# np.select — multiple conditions
cond    = [scores >= 90, scores >= 70, scores >= 50]
choices = ["A",          "B",          "C"]
letter  = np.select(cond, choices, default="D")
print("Letter grades:", letter)

# np.where returns indices when given 1 arg
idx_fail = np.where(scores < 60)[0]
print("Failing indices:", idx_fail)"""},
{"label": "np.argwhere and masked operations", "code":
"""import numpy as np

rng = np.random.default_rng(7)
data = rng.normal(50, 15, 20).round(1)
print("Data:", data)

# argwhere — indices where condition is True
low = np.argwhere(data < 35)
print("Indices where < 35:", low.flatten())

# Replace outliers (>2 std) with median
mean, std = data.mean(), data.std()
median = np.median(data)
outlier_mask = np.abs(data - mean) > 2 * std
cleaned = np.where(outlier_mask, median, data)
print(f"Replaced {outlier_mask.sum()} outliers with median {median:.1f}")
print("Cleaned:", cleaned)"""},
{"label": "np.where with multiple conditions and np.select for multi-case logic", "code":
"""import numpy as np

rng = np.random.default_rng(3)
temps = rng.normal(20, 8, 12).round(1)   # 12 hourly readings
print("Temperatures:", temps)

# np.where with compound condition (AND)
comfortable = np.where((temps >= 18) & (temps <= 26), temps, np.nan)
print("Comfortable temps only:", comfortable)

# np.select — clean multi-case replacement for nested np.where
conditions = [
    temps < 5,
    (temps >= 5)  & (temps < 15),
    (temps >= 15) & (temps < 25),
    temps >= 25,
]
labels = ['freezing', 'cold', 'comfortable', 'hot']
category = np.select(conditions, labels, default='unknown')
print("Categories:", category)

# np.where returning indices (1-arg form) then using them
hot_idx = np.where(temps >= 25)[0]
print(f"Hot hours (index): {hot_idx}  values: {temps[hot_idx]}")

# Compound OR mask
extreme = np.where((temps < 5) | (temps >= 30), 'extreme', 'normal')
print("Extreme flag:", extreme)"""}
],
"practice": {
"title": "Boolean Filtering & Replacement",
"desc": "Generate 200 random normal values (mean=100, std=20). 1) Count values in each band: <70, 70-90, 90-110, 110-130, >130. 2) Use np.select to label them 'very_low','low','normal','high','very_high'. 3) Replace all values outside [60, 140] with the band boundary (clip). Verify no values remain outside [60, 140].",
"starter":
"""import numpy as np
np.random.seed(0)
data = np.random.normal(100, 20, 200)

# 1. Count per band
bands = [(None, 70), (70, 90), (90, 110), (110, 130), (130, None)]
labels = ['very_low', 'low', 'normal', 'high', 'very_high']
for label, (lo, hi) in zip(labels, bands):
    if lo is None:
        count = (data < hi).sum()
    elif hi is None:
        count = (data >= lo).sum()
    else:
        count = ((data >= lo) & (data < hi)).sum()
    print(f"  {label:10s}: {count}")

# 2. Label each value with np.select
conds = [
    data < 70,
    (data >= 70) & (data < 90),
    (data >= 90) & (data < 110),
    (data >= 110) & (data < 130),
]
# TODO: labeled = np.select(conds, labels[:4], default=labels[4])

# 3. Clip and verify
# TODO: clipped = np.clip(data, 60, 140)
# TODO: print("All in [60,140]:", np.all((clipped >= 60) & (clipped <= 140)))"""
},
"rw": {
"title": "Energy Consumption Flagging",
"scenario": "A building engineer computes heating/cooling degree-hours and flags extreme temperature events for HVAC optimization.",
"code":
"""import numpy as np

np.random.seed(1)
# 1 year of hourly outdoor temperatures (°C)
temps = np.random.normal(22, 7, 8760)

# Degree-hours for heating (< 16°C) and cooling (> 24°C)
heating = np.where(temps < 16, 16 - temps, 0)
cooling = np.where(temps > 24, temps - 24, 0)
extreme = (temps < 0) | (temps > 38)

print(f"Heating degree-hours:   {heating.sum():.0f}")
print(f"Cooling degree-hours:   {cooling.sum():.0f}")
print(f"Extreme hours (<0/>38): {extreme.sum()}")
print(f"Coldest: {temps.min():.1f}°C at hour {temps.argmin()}")
print(f"Hottest: {temps.max():.1f}°C at hour {temps.argmax()}")"""}
},

{
"title": "7. Statistical Functions",
"desc": "NumPy provides fast descriptive statistics along any axis, plus correlation, covariance, and percentile functions.",
"examples": [
{"label": "Descriptive stats and axis parameter", "code":
"""import numpy as np

data = np.array([4, 7, 13, 16, 21, 23, 24, 28, 30])
print("mean:   ", np.mean(data))
print("median: ", np.median(data))
print("std:    ", np.std(data).round(2))
print("25th:   ", np.percentile(data, 25))
print("75th:   ", np.percentile(data, 75))

# Axis-wise on 2D
m = np.random.randint(1, 10, (4, 5))
print("Row means:", m.mean(axis=1).round(2))
print("Col sums: ", m.sum(axis=0))"""},
{"label": "Correlation and covariance", "code":
"""import numpy as np

np.random.seed(42)
x = np.random.randn(100)
y = 0.8 * x + np.random.randn(100) * 0.5  # correlated
z = np.random.randn(100)                   # independent

# Pearson correlation matrix
data = np.vstack([x, y, z])
cov  = np.cov(data)
corr = np.corrcoef(data)

print("Covariance matrix:\\n", cov.round(2))
print("Correlation matrix:\\n", corr.round(2))"""},
{"label": "np.histogram and quantile functions", "code":
"""import numpy as np

rng = np.random.default_rng(42)
data = rng.normal(50, 10, 1000)

# Histogram
counts, edges = np.histogram(data, bins=10)
print("Bin edges:", edges.round(1))
print("Counts:   ", counts)

# Manual histogram display
for i, (lo, hi, c) in enumerate(zip(edges, edges[1:], counts)):
    bar = '#' * (c // 10)
    print(f"[{lo:5.1f}-{hi:5.1f}] {bar} ({c})")

# Quantile / percentile
q = np.quantile(data, [0.25, 0.5, 0.75])
print(f"Q1={q[0]:.1f}  Median={q[1]:.1f}  Q3={q[2]:.1f}  IQR={q[2]-q[0]:.1f}")

# nanmean — ignores NaN
a = np.array([1.0, 2.0, np.nan, 4.0, np.nan, 6.0])
print("nanmean:", np.nanmean(a), "  nanstd:", np.nanstd(a).round(3))"""},
{"label": "np.percentile vs np.quantile, np.corrcoef, and np.histogram2d", "code":
"""import numpy as np

rng = np.random.default_rng(99)
x = rng.normal(0, 1, 500)
y = 0.7 * x + rng.normal(0, 0.7, 500)   # correlated with x

# percentile (takes 0-100) vs quantile (takes 0.0-1.0) — same result
p = np.percentile(x, [25, 50, 75])
q = np.quantile(x,  [0.25, 0.50, 0.75])
print("percentile:", p.round(3))
print("quantile:  ", q.round(3))
print("identical: ", np.allclose(p, q))

# corrcoef — Pearson correlation matrix
corr = np.corrcoef(x, y)
print(f"\\nCorrelation x<->y: {corr[0,1]:.3f}")

# histogram2d — joint distribution of two variables
H, xedges, yedges = np.histogram2d(x, y, bins=5)
print("\\n2D histogram (counts):\\n", H.astype(int))
print("x edges:", xedges.round(2))
print("y edges:", yedges.round(2))
print("Most occupied bin count:", int(H.max()))"""}
],
"practice": {
"title": "Statistics on a 2D Dataset",
"desc": "Create a (10, 5) matrix of random student scores (int, 0-100). Compute: per-column mean, std, min, max. Find which column (subject) has the highest variance. Identify which rows (students) have an average below 50. Compute the correlation matrix between all 5 subjects.",
"starter":
"""import numpy as np
np.random.seed(1)

scores = np.random.randint(0, 101, (10, 5))
subjects = ['Math', 'Science', 'English', 'History', 'Art']
print("Scores:\\n", scores)

# 1. Per-column statistics
for j, subj in enumerate(subjects):
    col = scores[:, j]
    # TODO: print(f"{subj:8s}: mean={col.mean():.1f}, std={col.std():.1f}, min={col.min()}, max={col.max()}")
    pass

# 2. Subject with highest variance
# TODO: variances = scores.var(axis=0)
# TODO: hardest = subjects[np.argmax(variances)]
# print(f"Highest variance subject: {hardest}")

# 3. Students with average below 50
# TODO: row_means = scores.mean(axis=1)
# TODO: struggling = np.where(row_means < 50)[0]
# print(f"Students below avg 50: rows {struggling}")

# 4. Correlation matrix
# TODO: corr = np.corrcoef(scores.T)
# print("Correlation:\\n", corr.round(2))"""
},
"rw": {
"title": "Manufacturing QC Outlier Detection",
"scenario": "A quality engineer uses Z-scores to identify defective units exceeding 3 standard deviations from the process mean.",
"code":
"""import numpy as np

np.random.seed(42)
# 10,000 unit measurements (target: 50mm ± 5mm)
measurements = np.random.normal(50, 5, 10000)

# Inject artificial defects
measurements[[100, 500, 2000, 7500]] = [85, 4, 92, 7]

mean    = measurements.mean()
std     = measurements.std()
z_score = np.abs((measurements - mean) / std)

outlier_mask   = z_score > 3
outlier_vals   = measurements[outlier_mask]
outlier_idx    = np.where(outlier_mask)[0]

print(f"Process mean:  {mean:.2f}mm,  std: {std:.2f}mm")
print(f"Total units:   {len(measurements):,}")
print(f"Defects found: {outlier_mask.sum()} ({outlier_mask.mean():.2%})")
print(f"Defect values: {outlier_vals.round(1)}")
print(f"At indices:    {outlier_idx}")"""}
},

{
"title": "8. Linear Algebra",
"desc": "numpy.linalg provides matrix operations essential for machine learning, portfolio optimization, and scientific computing.",
"examples": [
{"label": "Matrix multiply, inverse, determinant", "code":
"""import numpy as np

A = np.array([[2, 1], [1, 3]], dtype=float)
B = np.array([[1, 2], [3, 4]], dtype=float)

print("A @ B:\\n",  A @ B)            # matmul (preferred)
print("inv(A):\\n", np.linalg.inv(A).round(3))
print("det(A):", np.linalg.det(A))
print("A @ inv(A):\\n",
      (A @ np.linalg.inv(A)).round(10))  # should be identity"""},
{"label": "Eigenvalues and solving Ax = b", "code":
"""import numpy as np

A = np.array([[4, 2], [1, 3]], dtype=float)
vals, vecs = np.linalg.eig(A)
print("Eigenvalues: ", vals)
print("Eigenvectors:\\n", vecs.round(3))

# Solve the linear system Ax = b
b = np.array([10.0, 8.0])
x = np.linalg.solve(A, b)
print("Solution x:", x)
print("Verify Ax==b:", np.allclose(A @ x, b))"""},
{"label": "SVD, QR decomposition, and matrix rank", "code":
"""import numpy as np

A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]], dtype=float)

# SVD decomposition: A = U @ diag(S) @ Vt
U, S, Vt = np.linalg.svd(A)
print("Singular values:", S.round(4))
print("Rank (non-zero SVs):", np.sum(S > 1e-10))

# QR decomposition
Q, R = np.linalg.qr(A)
print("Q shape:", Q.shape, "  R shape:", R.shape)
print("Reconstruct:", np.allclose(Q @ R, A))

# Norm and condition number
print("Frobenius norm:", np.linalg.norm(A, 'fro').round(3))
print("Condition number:", np.linalg.cond(A).round(1))"""},
{"label": "np.linalg.lstsq, np.linalg.eig, and condition number", "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Least-squares: fit a line y = m*x + b to noisy data
x = np.linspace(0, 10, 20)
y_true = 2.5 * x + 1.0
y = y_true + rng.normal(0, 1.5, 20)   # add noise

# Build design matrix [x, 1] for [m, b]
A = np.column_stack([x, np.ones(len(x))])
coeffs, residuals, rank, sv = np.linalg.lstsq(A, y, rcond=None)
print(f"lstsq fit:  m={coeffs[0]:.3f}  b={coeffs[1]:.3f}  (true: m=2.5, b=1.0)")

# Eigenvalues and eigenvectors
M = np.array([[3, 1], [0, 2]], dtype=float)
eigenvalues, eigenvectors = np.linalg.eig(M)
print(f"\\nEigenvalues: {eigenvalues}")
print(f"Eigenvectors:\\n{eigenvectors.round(3)}")
# Verify: M @ v = lambda * v for each eigenpair
for i in range(len(eigenvalues)):
    lhs = M @ eigenvectors[:, i]
    rhs = eigenvalues[i] * eigenvectors[:, i]
    print(f"  Mv == lv (col {i}): {np.allclose(lhs, rhs)}")

# Condition number — high means near-singular, numerically unstable
well = np.array([[2., 1.], [1., 3.]])
ill  = np.array([[1., 1.], [1., 1.0001]])
print(f"\\nCondition (well-conditioned): {np.linalg.cond(well):.2f}")
print(f"Condition (ill-conditioned):  {np.linalg.cond(ill):.0f}")"""}
],
"practice": {
"title": "Solve a 3x3 Linear System",
"desc": "Solve this system: 2x + y - z = 8, -3x - y + 2z = -11, -2x + y + 2z = -3. Set up as Ax=b, solve with np.linalg.solve, verify with np.allclose. Then compute det(A), inv(A), and confirm A @ inv(A) is the identity.",
"starter":
"""import numpy as np

# 2x + y - z  = 8
# -3x - y + 2z = -11
# -2x + y + 2z = -3
A = np.array([
    # TODO: fill in the coefficient matrix
], dtype=float)

b = np.array([8.0, -11.0, -3.0])

# TODO: x = np.linalg.solve(A, b)
# print("Solution: x={:.1f}, y={:.1f}, z={:.1f}".format(*x))
# print("Verify:", np.allclose(A @ x, b))

# TODO: det_A = np.linalg.det(A)
# print(f"det(A) = {det_A:.2f}")

# TODO: inv_A = np.linalg.inv(A)
# print("A @ inv(A) is identity:", np.allclose(A @ inv_A, np.eye(3)))"""
},
"rw": {
"title": "Minimum-Variance Portfolio Optimization",
"scenario": "A portfolio manager uses covariance matrix inversion to compute optimal minimum-variance asset weights.",
"code":
"""import numpy as np

np.random.seed(0)
# 252 trading days, 5 assets
returns = np.random.randn(252, 5) * 0.01
cov     = np.cov(returns.T)          # 5×5 covariance matrix

# Closed-form minimum-variance weights: w = inv(Cov)·1 / (1'·inv(Cov)·1)
inv_cov  = np.linalg.inv(cov)
ones     = np.ones(5)
w_raw    = inv_cov @ ones
w_minvar = w_raw / w_raw.sum()       # normalize to sum = 1

port_var = float(w_minvar @ cov @ w_minvar)
port_std = np.sqrt(port_var * 252)   # annualized

print("Min-variance weights:", w_minvar.round(4))
print(f"Sum of weights: {w_minvar.sum():.6f}")
print(f"Annualized portfolio vol: {port_std:.4f}")"""}
},

{
"title": "9. Array Manipulation",
"desc": "Reshape, stack, split, and transpose arrays to match the formats expected by algorithms and frameworks.",
"examples": [
{"label": "reshape, flatten, transpose", "code":
"""import numpy as np

a = np.arange(24)

r = a.reshape(4, 6)
print("(4,6):\\n", r)

b = a.reshape(2, 3, 4)
print("3D:", b.shape)

# -1 auto-infers
c = a.reshape(6, -1)
print("Auto (6,4):", c.shape)

print("Transpose:", r.T.shape)
print("Flatten:", r.flatten()[:8], "...")"""},
{"label": "stack, hstack, vstack, split", "code":
"""import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("hstack:", np.hstack([a, b]))
print("vstack:\\n", np.vstack([a, b]))
print("stack(axis=1):\\n", np.stack([a, b], axis=1))

# Split
arr = np.arange(12)
p1, p2, p3 = np.split(arr, 3)
print("Split:", p1, p2, p3)

# Concatenate 2D
m1 = np.ones((2, 3))
m2 = np.zeros((2, 3))
print("concat row:\\n", np.concatenate([m1, m2], axis=0))"""},
{"label": "np.repeat, np.pad, and np.roll", "code":
"""import numpy as np

a = np.array([1, 2, 3])

# repeat — repeat each element
print("repeat each 3x:", np.repeat(a, 3))    # [1 1 1 2 2 2 3 3 3]

# tile — repeat the whole array
print("tile 3x:", np.tile(a, 3))             # [1 2 3 1 2 3 1 2 3]

# pad — add border around array
m = np.ones((3, 3), dtype=int)
padded = np.pad(m, pad_width=1, mode='constant', constant_values=0)
print("Padded (zeros border):\\n", padded)

# roll — shift elements cyclically
arr = np.array([1, 2, 3, 4, 5])
print("roll right 2:", np.roll(arr, 2))      # [4 5 1 2 3]
print("roll left 2: ", np.roll(arr, -2))     # [3 4 5 1 2]"""},
{"label": "np.split, np.array_split, and np.concatenate along different axes", "code":
"""import numpy as np

data = np.arange(24).reshape(4, 6)
print("Original (4x6):\\n", data)

# np.split — equal-size splits (raises error if not divisible)
cols = np.split(data, 3, axis=1)      # 3 chunks of (4, 2)
print("\\nSplit into 3 col-chunks, each shape:", cols[0].shape)

# np.array_split — unequal splits are allowed
rows = np.array_split(data, 3, axis=0)  # chunks of sizes 2, 1, 1
print("array_split row shapes:", [c.shape for c in rows])

# np.concatenate along different axes
a = np.ones((3, 4))
b = np.zeros((3, 4))
row_join = np.concatenate([a, b], axis=0)  # (6, 4)
col_join = np.concatenate([a, b], axis=1)  # (3, 8)
print("\\nconcat axis=0 (row join):", row_join.shape)
print("concat axis=1 (col join):", col_join.shape)

# Round-trip: split then concatenate recovers original
chunks = np.array_split(data, [2, 3], axis=0)  # at rows 2 and 3
restored = np.concatenate(chunks, axis=0)
print("\\nRound-trip split->concat matches original:", np.array_equal(data, restored))"""}
],
"practice": {
"title": "Shape Manipulation Challenge",
"desc": "1) Start with np.arange(60), reshape to (3, 4, 5). Transpose axes to (5, 4, 3), then flatten. 2) Stack three (4, 3) matrices along a new axis 0 to get (3, 4, 3). 3) Split a (12, 8) matrix into 4 equal row-chunks and stack them along axis=2.",
"starter":
"""import numpy as np

# 1. Reshape, transpose, flatten
a = np.arange(60)
# TODO: r = a.reshape(3, 4, 5)
# TODO: t = r.transpose(2, 1, 0)  # axes order (5, 4, 3)
# TODO: flat = t.flatten()
# print("Original shape:", r.shape)
# print("Transposed:", t.shape)
# print("Flattened:", flat.shape)

# 2. Stack three matrices along new axis
m1 = np.ones((4, 3))
m2 = np.zeros((4, 3))
m3 = np.full((4, 3), 2.0)
# TODO: stacked = np.stack([m1, m2, m3], axis=0)
# print("Stacked shape:", stacked.shape)  # (3, 4, 3)

# 3. Split and re-stack
big = np.arange(96).reshape(12, 8)
# TODO: chunks = np.split(big, 4, axis=0)  # 4 chunks of (3, 8)
# TODO: result = np.stack(chunks, axis=2)  # (3, 8, 4)
# print("Result shape:", result.shape)"""
},
"rw": {
"title": "Image Batch Preparation for Deep Learning",
"scenario": "A computer vision engineer reshapes image batches into the correct formats for PyTorch (CHW) and TensorFlow (HWC) models.",
"code":
"""import numpy as np

# Simulate a batch of images: (N, H, W, C) — TensorFlow/HWC format
batch_size, H, W, C = 32, 64, 64, 3
images = np.random.rand(batch_size, H, W, C).astype(np.float32)

# Flatten spatial dims for dense layer input
flat = images.reshape(batch_size, -1)
print(f"HWC flat:   {images.shape} → {flat.shape}")

# Convert to CHW format for PyTorch: (N, C, H, W)
chw = images.transpose(0, 3, 1, 2)
print(f"CHW format: {chw.shape}")

# Stack two batches along batch axis
batch2   = np.random.rand(batch_size, H, W, C).astype(np.float32)
combined = np.concatenate([images, batch2], axis=0)
print(f"Combined:   {combined.shape}")"""}
},

{
"title": "10. Random Number Generation",
"desc": "NumPy's random module (use default_rng for new code) generates arrays from many distributions — key for simulations and augmentation.",
"examples": [
{"label": "Seeding and common distributions", "code":
"""import numpy as np

rng = np.random.default_rng(seed=42)   # recommended API

u   = rng.random((3, 3))               # uniform [0,1)
n   = rng.standard_normal((3, 3))      # N(0,1)
i   = rng.integers(0, 100, size=5)     # integers
c   = rng.choice([10,20,30,40], size=3, replace=False)

print("Uniform:\\n",  u.round(2))
print("Normal:\\n",   n.round(2))
print("Integers:", i)
print("Choice:  ", c)"""},
{"label": "Statistical distributions", "code":
"""import numpy as np

rng = np.random.default_rng(0)

normal  = rng.normal(loc=50, scale=10, size=1000)
uniform = rng.uniform(low=0, high=100, size=1000)
binom   = rng.binomial(n=10, p=0.3, size=1000)
poisson = rng.poisson(lam=5, size=1000)

for name, arr in [("normal",normal),("uniform",uniform),
                   ("binom",binom),("poisson",poisson)]:
    print(f"{name:8s}: mean={arr.mean():.2f}  std={arr.std():.2f}  "
          f"range=[{arr.min():.0f},{arr.max():.0f}]")"""},
{"label": "shuffle, permutation, and bootstrap sampling", "code":
"""import numpy as np

rng = np.random.default_rng(42)

arr = np.arange(10)

# permutation — returns NEW shuffled array
shuffled = rng.permutation(arr)
print("Original:  ", arr)
print("Permuted:  ", shuffled)

# shuffle — in-place
arr2 = arr.copy()
rng.shuffle(arr2)
print("In-place:  ", arr2)

# Bootstrap resampling
data = np.array([2.3, 4.1, 3.8, 5.0, 2.9, 4.4, 3.2, 4.7])
n_boot = 10000
boot_means = np.array([
    rng.choice(data, size=len(data), replace=True).mean()
    for _ in range(n_boot)
])
print(f"Bootstrap mean: {boot_means.mean():.3f}")
print(f"95% CI: [{np.percentile(boot_means,2.5):.3f}, "
      f"{np.percentile(boot_means,97.5):.3f}]")"""},
{"label": "New Generator API, seeded reproducibility, and normal vs uniform comparison", "code":
"""import numpy as np

# New-style Generator — preferred over np.random.seed / np.random.randn
rng1 = np.random.default_rng(seed=2024)
rng2 = np.random.default_rng(seed=2024)   # same seed → identical output

a = rng1.standard_normal(5)
b = rng2.standard_normal(5)
print("Seeded reproducibility (same seed):", np.allclose(a, b))

# Spawning independent sub-generators (safe for parallel work)
child_rngs = rng1.spawn(3)
print("Spawned", len(child_rngs), "independent generators")
print("Child 0 sample:", child_rngs[0].random(3).round(3))

# Compare normal vs uniform for same N
N = 100_000
rng = np.random.default_rng(0)
norm = rng.normal(loc=0.5, scale=0.15, size=N)   # bell-shaped
unif = rng.uniform(low=0.0, high=1.0,  size=N)   # flat

for name, arr in [("normal", norm), ("uniform", unif)]:
    print(f"{name:8s}: mean={arr.mean():.4f}  std={arr.std():.4f}  "
          f"min={arr.min():.3f}  max={arr.max():.3f}")

# Clamp normal to [0,1] range and compare coverage
norm_clipped = np.clip(norm, 0, 1)
print(f"\\nNormal values outside [0,1]: {((norm<0)|(norm>1)).sum()} / {N}")
print(f"Uniform values outside [0,1]: {((unif<0)|(unif>1)).sum()} / {N}")"""}
],
"practice": {
"title": "Monte Carlo Dice Simulation",
"desc": "Simulate 1,000,000 rolls of two 6-sided dice using NumPy (no Python loops). 1) Compute the frequency of each sum (2-12). 2) Compare to theoretical probability. 3) Find the empirical probability of rolling a sum of 7. 4) Simulate the 'Craps' first-roll win condition (sum 7 or 11).",
"starter":
"""import numpy as np
rng = np.random.default_rng(42)
N = 1_000_000

# Roll two dice, compute sums
die1 = rng.integers(1, 7, size=N)
die2 = rng.integers(1, 7, size=N)
# TODO: sums = die1 + die2

# 1. Frequency of each outcome (2-12)
print("Sum | Empirical | Theoretical")
for s in range(2, 13):
    # TODO: empirical = (sums == s).mean()
    ways = min(s-1, 13-s)  # number of ways to roll sum s
    theoretical = ways / 36
    # TODO: print(f"  {s:2d} | {empirical:.4f}    | {theoretical:.4f}")
    pass

# 2. Probability of sum == 7
# TODO: p7 = (sums == 7).mean()
# print(f"P(sum=7): empirical={p7:.4f}, theoretical={1/6:.4f}")

# 3. Craps win (7 or 11 on first roll)
# TODO: craps_win = ((sums == 7) | (sums == 11)).mean()
# print(f"Craps first-roll win: {craps_win:.4f} (expected 0.2222)")"""
},
"rw": {
"title": "Monte Carlo Stock Price Simulation",
"scenario": "A risk analyst simulates 100,000 price paths to estimate portfolio VaR and probability of loss at year-end.",
"code":
"""import numpy as np

rng      = np.random.default_rng(99)
n_sims   = 100_000
n_days   = 252
S0       = 100.0
mu_day   = 0.0003       # daily drift
sig_day  = 0.015        # daily volatility

# Geometric Brownian Motion
daily_ret = rng.normal(mu_day, sig_day, (n_sims, n_days))
paths     = S0 * np.cumprod(1 + daily_ret, axis=1)
final     = paths[:, -1]

var_95    = np.percentile(final, 5)
cvar_95   = final[final <= var_95].mean()
prob_loss = (final < S0).mean()

print(f"Expected year-end price:  ${final.mean():.2f}")
print(f"95% Value-at-Risk (loss): ${S0 - var_95:.2f}")
print(f"95% CVaR (expected loss): ${S0 - cvar_95:.2f}")
print(f"Probability of loss:      {prob_loss:.1%}")"""}
}

,
{
    "title": "11. Memory Layout & Strides",
    "desc": "Understand how NumPy stores data in memory — C vs Fortran order, strides, views vs copies, and how layout affects performance.",
    "examples": [
        {
            "label": "C-order vs Fortran-order arrays",
            "code": "import numpy as np\n\n# C-order: row-major (default)\nA = np.array([[1,2,3],[4,5,6]], order='C')\nB = np.array([[1,2,3],[4,5,6]], order='F')  # Fortran-order: column-major\n\nprint('C-order strides:', A.strides)   # (bytes per row, bytes per element)\nprint('F-order strides:', B.strides)   # (bytes per element, bytes per col)\nprint('C contiguous:', A.flags['C_CONTIGUOUS'])\nprint('F contiguous:', B.flags['F_CONTIGUOUS'])\n\n# Convert between orders\nA_f = np.asfortranarray(A)\nprint('After asfortranarray:', A_f.strides)"
        },
        {
            "label": "Views vs copies — when does NumPy copy?",
            "code": "import numpy as np\n\narr = np.arange(12).reshape(3, 4)\n\n# Slicing creates a VIEW (no copy)\nview = arr[::2, ::2]\nprint('Is view:', np.shares_memory(arr, view))  # True\nview[0, 0] = 999\nprint('Original changed:', arr[0, 0])  # 999 — shared memory!\n\n# Fancy indexing creates a COPY\ncopy = arr[[0, 2], :][:, [0, 2]]\nprint('Is copy:', not np.shares_memory(arr, copy))  # True\ncopy[0, 0] = -1\nprint('Original unchanged:', arr[0, 0])  # still 999\n\n# Force a copy explicitly\nexplicit_copy = arr.copy()\nprint('Explicit copy shares memory:', np.shares_memory(arr, explicit_copy))"
        },
        {
            "label": "Sliding window view with stride tricks",
            "code": "import numpy as np\n\n# Zero-copy rolling window using stride tricks\narr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])\nwindow_size = 4\n\nwindows = np.lib.stride_tricks.sliding_window_view(arr, window_size)\nprint('Windows shape:', windows.shape)  # (7, 4)\nprint('Windows:\\n', windows)\n\n# Rolling statistics without loops\nprint('Rolling mean:', windows.mean(axis=1).round(2))\nprint('Rolling max: ', windows.max(axis=1))\nprint('Rolling std: ', windows.std(axis=1).round(3))\n\n# 2D sliding window (e.g., image patches)\nimg = np.arange(25).reshape(5, 5)\npatches = np.lib.stride_tricks.sliding_window_view(img, (3, 3))\nprint('Image patches shape:', patches.shape)  # (3, 3, 3, 3)"
        },
        {
            "label": "In-place operations with out parameter",
            "code": "import numpy as np\n\na = np.random.rand(1_000_000)\nb = np.random.rand(1_000_000)\nresult = np.empty_like(a)\n\n# Avoid allocating a new array — write directly into result\nnp.add(a, b, out=result)          # result = a + b (no temp array)\nnp.sqrt(a, out=a)                 # in-place square root\nnp.multiply(result, 2.0, out=result)\n\nprint('result[:5]:', result[:5].round(4))\nprint('a[:5] (sqrt in-place):', a[:5].round(4))\n\n# Chain multiple ufunc operations with out\nx = np.linspace(0, np.pi, 6)\ntmp = np.empty_like(x)\nnp.sin(x, out=tmp)        # tmp = sin(x)\nnp.square(tmp, out=tmp)   # tmp = sin(x)^2 — still same memory\nprint('sin^2:', tmp.round(4))"
        }
    ],
    "rw_scenario": "A quant computing rolling volatility on 10M tick records needs zero-copy sliding windows — using stride tricks avoids allocating 40GB of intermediate arrays.",
    "rw_code": "import numpy as np\n\nnp.random.seed(42)\nprices = 100 * np.exp(np.cumsum(np.random.randn(500) * 0.01))\nreturns = np.diff(np.log(prices))\n\nwindow = 20  # 20-period rolling volatility\nroll_windows = np.lib.stride_tricks.sliding_window_view(returns, window)\nroll_vol = roll_windows.std(axis=1) * np.sqrt(252)  # annualized\n\nprint(f'Returns series: {len(returns)} points')\nprint(f'Rolling vol series: {len(roll_vol)} points')\nprint(f'Latest 20-day vol: {roll_vol[-1]:.2%}')\nprint(f'Max vol observed: {roll_vol.max():.2%}')\nprint(f'Min vol observed: {roll_vol.min():.2%}')",
    "practice": {
        "title": "Stride-Based Feature Matrix",
        "desc": "Given a 1D time series, use sliding_window_view to build a feature matrix where each row contains [t-3, t-2, t-1, t] values. Then compute the mean and std of each row as features.",
        "starter": "import numpy as np\n\nnp.random.seed(0)\nts = np.cumsum(np.random.randn(50))  # random walk\n\n# TODO: create sliding window view with window_size=4\n# TODO: compute mean and std of each window row\n# TODO: stack into feature matrix (n_samples x 3): [window_mean, window_std, last_value]\n# TODO: print shape and first 5 rows"
    }
},
{
    "title": "12. Structured Arrays",
    "desc": "Store heterogeneous data (mixed types) in a single NumPy array using structured dtypes — combine ints, floats, and strings like a lightweight in-memory table.",
    "examples": [
        {
            "label": "Creating structured arrays with named fields",
            "code": "import numpy as np\n\n# Define dtype with field names and types\ndtype = np.dtype([\n    ('name',  'U20'),   # Unicode string, max 20 chars\n    ('age',   'i4'),    # 32-bit integer\n    ('score', 'f8'),    # 64-bit float\n    ('grade', 'U2'),    # short string\n])\n\ndata = np.array([\n    ('Alice', 25, 92.5, 'A'),\n    ('Bob',   30, 78.3, 'B'),\n    ('Carol', 22, 95.1, 'A'),\n    ('Dave',  28, 65.0, 'C'),\n], dtype=dtype)\n\nprint('Array dtype:', data.dtype)\nprint('Names:', data['name'])\nprint('Scores:', data['score'])\nprint('Alice row:', data[0])"
        },
        {
            "label": "Filtering and sorting structured arrays",
            "code": "import numpy as np\n\ndtype = np.dtype([('name','U20'),('dept','U10'),('salary','f8'),('years','i4')])\nemployees = np.array([\n    ('Alice',  'Eng',   95000, 5),\n    ('Bob',    'Sales', 72000, 3),\n    ('Carol',  'Eng',   102000, 8),\n    ('Dave',   'HR',    68000, 2),\n    ('Eve',    'Eng',   88000, 4),\n    ('Frank',  'Sales', 76000, 6),\n], dtype=dtype)\n\n# Filter: engineers only\neng = employees[employees['dept'] == 'Eng']\nprint('Engineers:', eng['name'])\n\n# Sort by salary descending\nsorted_emp = np.sort(employees, order='salary')[::-1]\nprint('By salary:', sorted_emp[['name', 'salary']])\n\n# Boolean mask: high earners with 4+ years\nhigh = employees[(employees['salary'] > 80000) & (employees['years'] >= 4)]\nprint('High earners:', high['name'])"
        },
        {
            "label": "numpy.recarray for attribute-style access",
            "code": "import numpy as np\n\n# recarray lets you access fields as attributes (rec.name instead of rec['name'])\nstudents = np.rec.array([\n    ('Alice', 3.9, 'CS'),\n    ('Bob',   3.5, 'Math'),\n    ('Carol', 3.7, 'CS'),\n    ('Dave',  3.2, 'Physics'),\n], dtype=[('name','U20'),('gpa','f8'),('major','U10')])\n\nprint('Names (attr):', students.name)\nprint('GPAs  (attr):', students.gpa)\nprint('CS students:', students.name[students.major == 'CS'])\nprint('Top student:', students.name[students.gpa.argmax()])\n\n# recarray supports all standard numpy operations\nprint('Avg GPA:', students.gpa.mean().round(3))"
        },
        {
            "label": "Converting structured arrays to/from pandas",
            "code": "import numpy as np\nimport pandas as pd\n\ndtype = np.dtype([('product','U30'),('price','f8'),('qty','i4'),('in_stock','?')])\nproducts = np.array([\n    ('Laptop',  999.99, 15, True),\n    ('Mouse',    29.99, 80, True),\n    ('Monitor', 399.99,  5, False),\n    ('Keyboard', 79.99, 30, True),\n], dtype=dtype)\n\n# Structured array -> DataFrame\ndf = pd.DataFrame(products)\nprint('DataFrame:')\nprint(df)\n\n# DataFrame -> structured array\ndf2 = pd.DataFrame({'x': [1.0, 2.0], 'y': [3.0, 4.0], 'label': ['a', 'b']})\nrec = df2.to_records(index=False)\nprint('\\nRecord array:', rec)\nprint('x field:', rec['x'])"
        }
    ],
    "rw_scenario": "A sensor network logs readings from multiple instruments with different data types (device ID, timestamp, float values, status flags) into a single compact binary array for fast I/O.",
    "rw_code": "import numpy as np\n\n# Simulate sensor readings\nnp.random.seed(42)\nn = 1000\nsensor_dtype = np.dtype([\n    ('device_id', 'U8'),\n    ('timestamp', 'f8'),\n    ('temp_c',    'f4'),\n    ('pressure',  'f4'),\n    ('humidity',  'f4'),\n    ('alert',     '?'),\n])\n\ndevices = ['SEN-001', 'SEN-002', 'SEN-003']\ndata = np.array([\n    (np.random.choice(devices),\n     i * 60.0,\n     20 + np.random.randn() * 3,\n     1013 + np.random.randn() * 5,\n     50 + np.random.randn() * 10,\n     False)\n    for i in range(n)\n], dtype=sensor_dtype)\n\n# Flag temperature anomalies\nalert_mask = (data['temp_c'] > 25) | (data['temp_c'] < 15)\ndata['alert'] = alert_mask\n\nfor device in devices:\n    subset = data[data['device_id'] == device]\n    n_alerts = subset['alert'].sum()\n    print(f'{device}: {len(subset)} readings, {n_alerts} alerts, avg_temp={subset[\"temp_c\"].mean():.1f}°C')",
    "practice": {
        "title": "Student Records Sorter",
        "desc": "Create a structured array with fields: name (str), grade (int), gpa (float) for 6 students. Sort by gpa descending and print the top 3. Then compute average gpa per grade level.",
        "starter": "import numpy as np\n\ndtype = np.dtype([('name','U20'),('grade','i4'),('gpa','f8')])\nstudents = np.array([\n    ('Alice', 11, 3.9), ('Bob', 12, 3.4), ('Carol', 11, 3.7),\n    ('Dave', 12, 3.1), ('Eve', 10, 3.8), ('Frank', 10, 3.5),\n], dtype=dtype)\n\n# TODO: sort by gpa descending, print top 3\n# TODO: for each unique grade, compute and print average gpa"
    }
},
{
    "title": "13. Linear Algebra & Polynomial Fitting",
    "desc": "NumPy's linear algebra routines and polynomial tools — solve systems of equations, compute eigendecompositions, SVD, and fit curves to data.",
    "examples": [
        {
            "label": "Solving linear systems with np.linalg.solve",
            "code": "import numpy as np\n\n# Solve Ax = b\n# 3x + y = 9\n# x + 2y = 8\nA = np.array([[3, 1], [1, 2]], dtype=float)\nb = np.array([9, 8], dtype=float)\n\nx = np.linalg.solve(A, b)\nprint('Solution x:', x)               # [2. 3.]\nprint('Verify Ax == b:', np.allclose(A @ x, b))\n\n# Matrix inverse (prefer linalg.solve for stability)\nA_inv = np.linalg.inv(A)\nprint('Via inverse:', A_inv @ b)\n\n# Check if system is well-conditioned\nprint('Condition number:', np.linalg.cond(A))\n\n# Least-squares for overdetermined systems\nA_over = np.vstack([A, [2, 3]])\nb_over = np.append(b, 13)\nx_ls, _, _, _ = np.linalg.lstsq(A_over, b_over, rcond=None)\nprint('Least-squares solution:', x_ls.round(4))"
        },
        {
            "label": "Eigenvalues and eigenvectors",
            "code": "import numpy as np\n\nA = np.array([[4, 2], [1, 3]], dtype=float)\nvals, vecs = np.linalg.eig(A)\n\nprint('Eigenvalues: ', vals)    # [5. 2.]\nprint('Eigenvectors:\\n', vecs)  # columns are eigenvectors\n\n# Verify: A @ v = lambda * v\nfor lam, v in zip(vals, vecs.T):\n    print(f'lambda={lam:.1f}: A@v={A@v.round(4)}, lam*v={lam*v.round(4)}, match={np.allclose(A@v, lam*v)}')\n\n# Symmetric matrix has real eigenvalues — use eigh for efficiency\nS = np.array([[6, 2, 1], [2, 3, 1], [1, 1, 1]], dtype=float)\nvals_s, vecs_s = np.linalg.eigh(S)  # eigh for symmetric/Hermitian\nprint('Symmetric eigenvalues (sorted):', vals_s.round(3))"
        },
        {
            "label": "SVD decomposition and low-rank approximation",
            "code": "import numpy as np\n\n# SVD: M = U @ diag(s) @ Vt\nM = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10,11,12]], dtype=float)\nU, s, Vt = np.linalg.svd(M, full_matrices=False)\n\nprint('U shape:', U.shape, '| s:', s.round(3), '| Vt shape:', Vt.shape)\nprint('Reconstruct error:', np.allclose(M, U @ np.diag(s) @ Vt))\n\n# Low-rank approximation: keep top-k singular values\nk = 1\nM_approx = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]\nprint(f'Rank-{k} approx:\\n', M_approx.round(2))\nprint(f'Frobenius error: {np.linalg.norm(M - M_approx):.4f}')\nprint(f'Variance explained: {(s[:k]**2).sum()/(s**2).sum():.1%}')"
        },
        {
            "label": "Polynomial fitting with polyfit and polyval",
            "code": "import numpy as np\n\n# Generate noisy quadratic data\nnp.random.seed(42)\nx = np.linspace(-3, 3, 50)\ny_true = 2*x**2 - 3*x + 1\ny_noisy = y_true + np.random.randn(50) * 2\n\n# Fit polynomial of degree 2\ncoeffs = np.polyfit(x, y_noisy, deg=2)\nprint('Fitted coefficients:', coeffs.round(4))  # should be ~[2, -3, 1]\n\n# Evaluate the fitted polynomial\ny_fit = np.polyval(coeffs, x)\nrmse = np.sqrt(np.mean((y_fit - y_true)**2))\nprint(f'RMSE vs true: {rmse:.4f}')\n\n# Compare degrees\nfor deg in [1, 2, 3, 5]:\n    c = np.polyfit(x, y_noisy, deg)\n    y_hat = np.polyval(c, x)\n    print(f'Degree {deg}: train RMSE = {np.sqrt(np.mean((y_hat - y_noisy)**2)):.4f}')"
        }
    ],
    "rw_scenario": "A data scientist uses SVD to compress a document-term matrix — keeping only the top 50 singular values captures 85% of the variance while reducing memory 20×.",
    "rw_code": "import numpy as np\n\nnp.random.seed(42)\n# Simulate a document-term matrix (100 docs x 500 terms)\nn_docs, n_terms = 100, 500\nX = np.random.poisson(0.5, (n_docs, n_terms)).astype(float)\n\nU, s, Vt = np.linalg.svd(X, full_matrices=False)\n\ncumulative_var = np.cumsum(s**2) / (s**2).sum()\nfor k in [10, 20, 50, 100]:\n    X_k = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]\n    fro_err = np.linalg.norm(X - X_k, 'fro') / np.linalg.norm(X, 'fro')\n    mem_ratio = (n_docs*k + k + k*n_terms) / (n_docs*n_terms)\n    print(f'k={k:3d}: var_explained={cumulative_var[k-1]:.1%}, rel_error={fro_err:.3f}, memory={mem_ratio:.2%}')",
    "practice": {
        "title": "Curve Fitting & Residuals",
        "desc": "Generate 60 points of noisy sine data (y = sin(x) + noise). Fit polynomial degrees 1, 3, 5, and 7. For each, compute the RMSE and plot residuals. Identify the degree with best bias-variance tradeoff.",
        "starter": "import numpy as np\n\nnp.random.seed(42)\nx = np.linspace(0, 2*np.pi, 60)\ny = np.sin(x) + np.random.randn(60) * 0.2\n\n# TODO: for degrees [1, 3, 5, 7]:\n#   - fit np.polyfit\n#   - compute y_hat with np.polyval\n#   - compute RMSE\n#   - print results\n# TODO: print which degree has lowest RMSE"
    }
},
{
    "title": "14. Advanced Indexing & Fancy Indexing",
    "desc": "Use integer arrays, boolean masks, np.where, np.take, and advanced multi-dimensional indexing to select and modify array elements efficiently.",
    "examples": [
        {
            "label": "Integer array indexing",
            "code": "import numpy as np\n\nnp.random.seed(42)\narr = np.random.randint(0, 100, (5, 6))\nprint('Array:\\n', arr)\n\n# Select specific rows\nrow_idx = [0, 2, 4]\nprint('\\nRows 0, 2, 4:\\n', arr[row_idx])\n\n# Select specific (row, col) pairs\nrow_idx = [0, 1, 2, 3]\ncol_idx = [5, 4, 3, 2]\nprint('\\nDiagonal elements (row, col pairs):', arr[row_idx, col_idx])\n\n# Outer indexing: all combinations\nrows = np.array([0, 2])\ncols = np.array([1, 3, 5])\nprint('\\nOuter indexing (2 rows x 3 cols):\\n', arr[np.ix_(rows, cols)])\n\n# Assign values via fancy index\narr2 = arr.copy()\narr2[[1, 3], :] = -1\nprint('\\nAfter zeroing rows 1, 3:\\n', arr2)"
        },
        {
            "label": "Boolean masking & np.where",
            "code": "import numpy as np\n\nnp.random.seed(0)\ndata = np.random.randn(20)\nprint('Data:', data.round(2))\n\n# Boolean mask\nmask = data > 0.5\nprint(f'\\nValues > 0.5: {data[mask].round(2)}')\nprint(f'Count: {mask.sum()}')\n\n# np.where: conditional selection\nclipped = np.where(data > 0, data, 0)  # ReLU-style\nprint('\\nReLU output:', clipped.round(2))\n\n# Nested np.where: multi-condition\nlabels = np.where(data > 1, 'high', np.where(data < -1, 'low', 'mid'))\nprint('\\nLabels:', labels)\nfor cat in ['low', 'mid', 'high']:\n    print(f'  {cat}: {(labels == cat).sum()}')\n\n# np.where for index retrieval\nidx_high = np.where(data > 1)[0]\nprint('\\nIndices of high values:', idx_high)"
        },
        {
            "label": "np.take, np.put, and argsort tricks",
            "code": "import numpy as np\n\nnp.random.seed(42)\nscores = np.array([82, 45, 91, 67, 88, 55, 73, 96, 61, 79])\nnames  = np.array(['Alice','Bob','Carol','Dave','Eve','Frank','Grace','Hank','Iris','Jake'])\n\n# argsort: get ranking indices\nranking = np.argsort(scores)[::-1]  # descending\nprint('Top 5 students:')\nfor rank, idx in enumerate(ranking[:5], 1):\n    print(f'  {rank}. {names[idx]}: {scores[idx]}')\n\n# np.take: equivalent to fancy indexing but works on flattened axis\ntop3_scores = np.take(scores, ranking[:3])\nprint('\\nTop 3 scores:', top3_scores)\n\n# np.partition: O(n) top-k (faster than full sort)\ntop_k = 3\npartitioned = np.partition(scores, -top_k)[-top_k:]\nprint(f'Top {top_k} (unordered):', partitioned)\n\n# np.searchsorted: binary search on sorted array\nsorted_scores = np.sort(scores)\nthreshold = 80\ninsert_pos = np.searchsorted(sorted_scores, threshold)\nprint(f'\\nScores >= {threshold}: {sorted_scores[insert_pos:]}')"
        },
        {
            "label": "Multi-dimensional advanced indexing",
            "code": "import numpy as np\n\nnp.random.seed(42)\n# 3D array: (batch, height, width)\nimg_batch = np.random.randint(0, 256, (4, 8, 8), dtype=np.uint8)\nprint('Batch shape:', img_batch.shape)\n\n# Select specific pixel from each image in batch\nrows = [1, 2, 3, 4]  # row per image\ncols = [1, 2, 3, 4]  # col per image\nbatch_idx = [0, 1, 2, 3]\nselected_pixels = img_batch[batch_idx, rows, cols]\nprint('One pixel per image:', selected_pixels)\n\n# Vectorized update: zero out a 3x3 patch in all images\nimg_batch[:, 2:5, 2:5] = 0\nprint('After zeroing patch:', img_batch[0, 1:6, 1:6])\n\n# Use np.indices for meshgrid-style indexing\nH, W = 4, 4\nri, ci = np.indices((H, W))\ndist_from_center = np.sqrt((ri - H//2)**2 + (ci - W//2)**2)\nprint('\\nDistance from center:\\n', dist_from_center.round(2))"
        }
    ],
    "rw_scenario": "A computer vision pipeline needs to efficiently extract top-k confidence pixels from a batch of heatmaps, mask background pixels below a threshold, and assign class labels based on score ranges.",
    "rw_code": "import numpy as np\n\nnp.random.seed(7)\nbatch_size, H, W, n_classes = 8, 16, 16, 5\nheatmaps = np.random.rand(batch_size, H, W, n_classes).astype(np.float32)\n\n# Assign class = argmax across last axis\npred_class = np.argmax(heatmaps, axis=-1)  # (batch, H, W)\npred_conf  = np.max(heatmaps, axis=-1)     # (batch, H, W)\n\n# Mask low-confidence predictions\nthresh = 0.6\nmask = pred_conf >= thresh\nprint(f'High-conf pixels: {mask.sum()} / {mask.size} ({mask.mean():.1%})')\n\n# Class distribution for high-conf pixels\nfor batch_i in range(3):\n    hi_classes = pred_class[batch_i][mask[batch_i]]\n    counts = np.bincount(hi_classes, minlength=n_classes)\n    print(f'Batch {batch_i}: class counts = {counts}')\n\n# Top-5 confidence pixels per image\nfor batch_i in range(2):\n    flat_conf = pred_conf[batch_i].ravel()\n    top5_idx  = np.argpartition(flat_conf, -5)[-5:]\n    top5_rc   = np.unravel_index(top5_idx, (H, W))\n    print(f'Batch {batch_i} top-5 pixels: {list(zip(*top5_rc))}')",
    "practice": {
        "title": "Student Score Analyzer",
        "desc": "Given a 2D array of exam scores (30 students x 5 subjects), use advanced indexing to: (1) find each student's best and worst subject, (2) select the top 5 students by total score using np.argpartition, (3) assign letter grades (A>=90, B>=80, C>=70, D>=60, F<60) using np.where, (4) create a pass/fail mask where students need avg >= 70 in at least 3 subjects.",
        "starter": "import numpy as np\n\nnp.random.seed(42)\nscores = np.random.randint(40, 100, (30, 5))\nsubjects = ['Math', 'Science', 'English', 'History', 'Art']\nprint('Score matrix shape:', scores.shape)\n\n# TODO: (1) Find best and worst subject per student (argmax/argmin)\n# TODO: (2) Top 5 students by total score (np.argpartition)\n# TODO: (3) Assign letter grades A/B/C/D/F using np.where\n# TODO: (4) Pass/fail mask (avg >= 70 in at least 3 subjects)\n"
    }
},
{
    "title": "15. NumPy Performance & Vectorization",
    "desc": "Profile NumPy code, replace Python loops with vectorized operations, use einsum, out= parameters, and Numba JIT compilation for maximum speed.",
    "examples": [
        {
            "label": "Loop vs vectorized benchmark",
            "code": "import numpy as np\nimport time\n\nnp.random.seed(42)\nn = 1_000_000\nx = np.random.randn(n)\ny = np.random.randn(n)\n\n# Python loop (slow)\ndef dot_loop(a, b):\n    result = 0.0\n    for i in range(len(a)):\n        result += a[i] * b[i]\n    return result\n\n# NumPy vectorized (fast)\ndef dot_numpy(a, b):\n    return np.dot(a, b)\n\n# Benchmark (small n for loop)\nsmall_n = 10_000\nx_s, y_s = x[:small_n], y[:small_n]\n\nt0 = time.perf_counter()\nfor _ in range(5): dot_loop(x_s, y_s)\nloop_time = (time.perf_counter() - t0) / 5\n\nt0 = time.perf_counter()\nfor _ in range(100): dot_numpy(x, y)\nnp_time = (time.perf_counter() - t0) / 100\n\nprint(f'Loop (n={small_n:,}):   {loop_time*1000:.2f}ms')\nprint(f'NumPy (n={n:,}): {np_time*1000:.2f}ms')\nprint(f'NumPy processes {n/small_n:.0f}x more data in {loop_time/np_time:.0f}x less time')\nprint(f'Speedup: ~{loop_time*n/(np_time*small_n):.0f}x')"
        },
        {
            "label": "np.einsum for tensor contractions",
            "code": "import numpy as np\nimport time\n\nnp.random.seed(0)\nA = np.random.randn(50, 30)\nB = np.random.randn(30, 40)\nC = np.random.randn(50, 40)\n\n# Matrix multiplication\nresult1 = np.einsum('ij,jk->ik', A, B)         # same as A @ B\nresult2 = np.einsum('ij,ij->', A, A[:,:30])    # element-wise sum of squares (trace of A.T@A)\n\n# Batch matrix multiply: (batch, M, K) x (batch, K, N) -> (batch, M, N)\nbatch = 16\nX = np.random.randn(batch, 10, 8)\nW = np.random.randn(batch, 8, 6)\nbmm_einsum = np.einsum('bij,bjk->bik', X, W)\nbmm_loop   = np.array([x @ w for x, w in zip(X, W)])\n\nprint('einsum batch matmul shape:', bmm_einsum.shape)\nprint('Matches loop result:', np.allclose(bmm_einsum, bmm_loop))\n\n# Outer product\nv1, v2 = np.array([1,2,3]), np.array([4,5,6])\nouter = np.einsum('i,j->ij', v1, v2)\nprint('Outer product:\\n', outer)\n\n# Trace\nM = np.random.randn(4, 4)\nprint(f'Trace: einsum={np.einsum(\"ii\", M):.4f}, np.trace={np.trace(M):.4f}')"
        },
        {
            "label": "Memory-efficient operations with out=",
            "code": "import numpy as np\nimport time\n\nnp.random.seed(42)\nn = 5_000_000\nx = np.random.rand(n).astype(np.float32)\ny = np.random.rand(n).astype(np.float32)\n\n# Without out= (allocates new array each time)\ndef compute_no_out(x, y, n_iters=20):\n    result = np.empty_like(x)\n    for _ in range(n_iters):\n        result = np.sin(x) + np.cos(y)  # creates temporary arrays\n    return result\n\n# With out= (reuses pre-allocated buffers)\ndef compute_with_out(x, y, n_iters=20):\n    buf1   = np.empty_like(x)\n    buf2   = np.empty_like(x)\n    result = np.empty_like(x)\n    for _ in range(n_iters):\n        np.sin(x, out=buf1)         # no allocation\n        np.cos(y, out=buf2)\n        np.add(buf1, buf2, out=result)\n    return result\n\nt0 = time.perf_counter()\nr1 = compute_no_out(x, y)\nt1 = time.perf_counter() - t0\n\nt0 = time.perf_counter()\nr2 = compute_with_out(x, y)\nt2 = time.perf_counter() - t0\n\nprint(f'Without out=: {t1:.3f}s')\nprint(f'With    out=: {t2:.3f}s')\nprint(f'Speedup: {t1/t2:.2f}x')\nprint(f'Results match: {np.allclose(r1, r2)}')"
        },
        {
            "label": "Numba JIT acceleration",
            "code": "try:\n    import numba\n    from numba import njit\n    import numpy as np\n    import time\n\n    @njit\n    def pairwise_dist_numba(X):\n        n = X.shape[0]\n        D = np.empty((n, n), dtype=np.float64)\n        for i in range(n):\n            for j in range(i, n):\n                d = 0.0\n                for k in range(X.shape[1]):\n                    diff = X[i, k] - X[j, k]\n                    d += diff * diff\n                D[i, j] = D[j, i] = d**0.5\n        return D\n\n    np.random.seed(42)\n    X = np.random.randn(500, 10)\n\n    # Warm-up JIT\n    pairwise_dist_numba(X[:5])\n\n    t0 = time.perf_counter()\n    D_numba = pairwise_dist_numba(X)\n    t_numba = time.perf_counter() - t0\n\n    # NumPy equivalent\n    t0 = time.perf_counter()\n    from sklearn.metrics import pairwise_distances\n    D_np = pairwise_distances(X)\n    t_np = time.perf_counter() - t0\n\n    print(f'Numba: {t_numba*1000:.1f}ms')\n    print(f'sklearn pairwise: {t_np*1000:.1f}ms')\n    print(f'Match: {np.allclose(D_numba, D_np)}')\nexcept ImportError:\n    print('pip install numba')\n    print('Numba @njit: compiles Python+NumPy loops to LLVM machine code.')\n    print('Typical speedup: 10-100x for loop-heavy numeric code.')"
        }
    ],
    "rw_scenario": "A quantitative trading firm needs to compute a rolling 60-day correlation matrix for 200 stocks every second. Optimize using vectorized einsum operations and pre-allocated output buffers.",
    "rw_code": "import numpy as np\nimport time\n\nnp.random.seed(42)\nn_stocks, n_days = 200, 252\nreturns = np.random.randn(n_days, n_stocks).astype(np.float32)\n\ndef rolling_corr_slow(returns, window=60):\n    n = len(returns)\n    corrs = []\n    for i in range(window, n + 1):\n        window_data = returns[i-window:i]\n        corrs.append(np.corrcoef(window_data.T))\n    return np.array(corrs)\n\ndef rolling_corr_fast(returns, window=60):\n    n, m = returns.shape\n    out = np.empty((n - window + 1, m, m), dtype=np.float32)\n    for i in range(n - window + 1):\n        W = returns[i:i+window]\n        # Standardize\n        mu  = W.mean(0)\n        std = W.std(0) + 1e-8\n        W_std = (W - mu) / std\n        out[i] = (W_std.T @ W_std) / window\n    return out\n\nt0 = time.perf_counter()\nC_fast = rolling_corr_fast(returns)\nprint(f'Fast: {time.perf_counter()-t0:.3f}s | shape: {C_fast.shape}')\nprint(f'Avg diagonal (should be 1): {np.diagonal(C_fast, axis1=1, axis2=2).mean():.4f}')",
    "practice": {
        "title": "Vectorize a Distance Computation",
        "desc": "Given a matrix X of shape (1000, 5), compute the pairwise Euclidean distance matrix D[i,j] = ||x_i - x_j||. Implement three versions: (1) pure Python nested loop, (2) NumPy broadcasting (X[:,None,:] - X[None,:,:]), (3) using np.einsum or scipy.spatial.distance. Benchmark all three and report speedups.",
        "starter": "import numpy as np\nimport time\n\nnp.random.seed(42)\nX = np.random.randn(1000, 5)\n\n# TODO: (1) Python nested loop (test on X[:50] for speed)\n# TODO: (2) NumPy broadcasting: (n,1,d) - (1,n,d), then norm\n# TODO: (3) scipy or einsum approach\n# TODO: Benchmark all three and print speedups\n"
    }
},
{
    "title": "16. Signal Processing with NumPy",
    "desc": "Apply Fourier transforms, filtering, convolution, and spectral analysis to 1D and 2D signals using NumPy's FFT routines.",
    "examples": [
        {
            "label": "FFT and frequency spectrum",
            "code": "import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\n# Composite signal: 5Hz + 20Hz + noise\nfs = 500      # sampling rate\nt  = np.linspace(0, 1, fs, endpoint=False)\nsignal = (np.sin(2*np.pi*5*t) +\n          0.5*np.sin(2*np.pi*20*t) +\n          np.random.randn(fs)*0.3)\n\n# FFT\nfft_vals = np.fft.rfft(signal)\nfreqs    = np.fft.rfftfreq(fs, d=1/fs)\npower    = np.abs(fft_vals)**2\n\n# Find dominant frequencies\ntop_freq_idx = np.argsort(power)[::-1][:3]\nprint('Top frequencies (Hz):', freqs[top_freq_idx].round(1))\nprint('Corresponding power:', power[top_freq_idx].round(1))\n\nfig, axes = plt.subplots(2, 1, figsize=(10, 6))\naxes[0].plot(t[:100], signal[:100])\naxes[0].set_title('Signal (first 100 samples)'); axes[0].set_xlabel('Time (s)')\naxes[1].plot(freqs[:50], power[:50])\naxes[1].set_title('Power Spectrum'); axes[1].set_xlabel('Frequency (Hz)')\nplt.tight_layout(); plt.savefig('fft.png', dpi=80); plt.close(); print('Saved fft.png')"
        },
        {
            "label": "Low-pass filter with FFT",
            "code": "import numpy as np\n\n# Create noisy signal\nfs = 1000\nt  = np.linspace(0, 1, fs)\nclean  = np.sin(2*np.pi*10*t)           # 10 Hz signal\nnoisy  = clean + 0.5*np.random.randn(fs) + 0.3*np.sin(2*np.pi*200*t)\n\n# FFT-based low-pass filter\ndef lowpass_fft(signal, fs, cutoff_hz):\n    fft_sig  = np.fft.rfft(signal)\n    freqs    = np.fft.rfftfreq(len(signal), d=1/fs)\n    fft_sig[freqs > cutoff_hz] = 0  # zero out high frequencies\n    return np.fft.irfft(fft_sig)\n\nfiltered = lowpass_fft(noisy, fs, cutoff_hz=30)\n\nsnr_noisy    = 10*np.log10(np.var(clean) / np.var(noisy - clean))\nsnr_filtered = 10*np.log10(np.var(clean) / np.var(filtered[:len(clean)] - clean))\nprint(f'SNR (noisy):    {snr_noisy:.2f} dB')\nprint(f'SNR (filtered): {snr_filtered:.2f} dB')\nprint(f'Improvement:    {snr_filtered - snr_noisy:.2f} dB')\nprint(f'Correlation (filtered vs clean): {np.corrcoef(clean, filtered[:len(clean)])[0,1]:.4f}')"
        },
        {
            "label": "1D convolution and moving average",
            "code": "import numpy as np\n\nnp.random.seed(42)\nn = 200\nt = np.arange(n)\nsignal = np.sin(0.1*t) + np.random.randn(n)*0.5\n\n# Manual convolution = moving average\ndef moving_average(x, w):\n    kernel = np.ones(w) / w\n    return np.convolve(x, kernel, mode='same')\n\n# Gaussian smoothing kernel\ndef gaussian_kernel(size, sigma):\n    x = np.arange(-(size//2), size//2+1)\n    k = np.exp(-x**2 / (2*sigma**2))\n    return k / k.sum()\n\nma5  = moving_average(signal, 5)\nma20 = moving_average(signal, 20)\ngk   = gaussian_kernel(21, sigma=3)\ngauss_smooth = np.convolve(signal, gk, mode='same')\n\n# Derivative via convolution (finite difference kernel)\ndiff_kernel = np.array([1, 0, -1]) / 2\nderivative  = np.convolve(signal, diff_kernel, mode='same')\n\nprint(f'Signal length: {len(signal)}')\nprint(f'MA-5 smoothed std:    {ma5.std():.3f} (original: {signal.std():.3f})')\nprint(f'MA-20 smoothed std:   {ma20.std():.3f}')\nprint(f'Gaussian smooth std:  {gauss_smooth.std():.3f}')\nprint(f'Derivative range: [{derivative.min():.3f}, {derivative.max():.3f}]')"
        },
        {
            "label": "2D FFT for image frequency analysis",
            "code": "import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\n# Create a synthetic 2D image with patterns\nnp.random.seed(42)\nH, W = 64, 64\nx, y = np.meshgrid(np.arange(W), np.arange(H))\n\n# Low-freq + high-freq patterns + noise\nimage = (np.sin(2*np.pi*2*x/W) + np.sin(2*np.pi*5*y/H) +\n         0.3*np.random.randn(H, W))\n\n# 2D FFT\nfft2d   = np.fft.fft2(image)\nfft_mag = np.abs(np.fft.fftshift(fft2d))  # shift zero-freq to center\nlog_mag = np.log1p(fft_mag)                # log scale for visualization\n\n# Low-pass filter: zero out high-freq components\ncenter  = np.array([H//2, W//2])\nY, X    = np.ogrid[:H, :W]\ndist_from_center = np.sqrt((Y - H//2)**2 + (X - W//2)**2)\nmask    = dist_from_center <= 10\nfft_shift = np.fft.fftshift(fft2d)\nfft_shift *= mask\nfiltered = np.real(np.fft.ifft2(np.fft.ifftshift(fft_shift)))\n\nprint(f'Original image PSNR vs filtered: {10*np.log10(image.max()**2 / ((image-filtered)**2).mean()):.1f} dB')\nprint(f'Dominant frequency components in top 5% power: {(log_mag > np.percentile(log_mag, 95)).sum()}')\nfig, axes = plt.subplots(1, 3, figsize=(12, 4))\naxes[0].imshow(image, cmap='gray'); axes[0].set_title('Original')\naxes[1].imshow(log_mag, cmap='hot'); axes[1].set_title('2D Spectrum (log)')\naxes[2].imshow(filtered, cmap='gray'); axes[2].set_title('Low-pass Filtered')\nplt.tight_layout(); plt.savefig('fft2d.png', dpi=80); plt.close(); print('Saved fft2d.png')"
        }
    ],
    "rw_scenario": "An IoT sensor produces 1kHz vibration readings from industrial machinery. Detect bearing faults by identifying abnormal frequency peaks between 80-300Hz that exceed 3x the baseline RMS power in that band.",
    "rw_code": "import numpy as np\n\nnp.random.seed(42)\nfs = 1000\nt  = np.linspace(0, 5, 5*fs)  # 5 seconds\n\n# Normal vibration: low-freq mechanical\nnormal = np.sin(2*np.pi*15*t) + 0.2*np.random.randn(len(t))\n\n# Faulty vibration: adds bearing fault frequency at 120Hz\nfault_freq = 120\nfaulty = normal + 1.5*np.sin(2*np.pi*fault_freq*t)\n\ndef detect_fault(signal, fs, fault_band=(80,300), threshold=3.0):\n    fft_v  = np.fft.rfft(signal)\n    freqs  = np.fft.rfftfreq(len(signal), d=1/fs)\n    power  = np.abs(fft_v)**2\n    # Baseline: power outside fault band\n    base_mask = (freqs < fault_band[0]) | (freqs > fault_band[1])\n    fault_mask = (freqs >= fault_band[0]) & (freqs <= fault_band[1])\n    baseline_rms = np.sqrt(power[base_mask].mean())\n    fault_rms    = np.sqrt(power[fault_mask].mean())\n    ratio = fault_rms / (baseline_rms + 1e-8)\n    return ratio > threshold, ratio\n\nfor name, sig in [('Normal', normal), ('Faulty', faulty)]:\n    is_fault, ratio = detect_fault(sig, fs)\n    print(f'{name}: fault_band/baseline ratio={ratio:.2f} -> {\"FAULT\" if is_fault else \"OK\"}')",
    "practice": {
        "title": "Audio Denoising Pipeline",
        "desc": "Simulate an audio signal: 440Hz tone + 880Hz harmonic + white noise. (1) Compute FFT and plot the power spectrum. (2) Design a bandpass FFT filter that keeps only 400-950Hz. (3) Reconstruct the signal with ifft. (4) Compute SNR before and after filtering. (5) Also try a 21-point Gaussian smoothing kernel via np.convolve as an alternative.",
        "starter": "import numpy as np\n\nnp.random.seed(42)\nfs = 8000\nt  = np.linspace(0, 1, fs)\n\nclean = np.sin(2*np.pi*440*t) + 0.5*np.sin(2*np.pi*880*t)\nnoisy = clean + np.random.randn(fs) * 0.8\n\n# TODO: (1) FFT + power spectrum, find top frequency peaks\n# TODO: (2) Bandpass FFT filter (keep 400-950Hz)\n# TODO: (3) Reconstruct with ifft\n# TODO: (4) SNR before and after\n# TODO: (5) Compare with 21-pt Gaussian convolution\n"
    }
},

    {
    "title": "17. Sorting, Searching & Partitioning",
    "desc": "NumPy\'s sort, argsort, searchsorted, and partition give O(n log n) and O(n) ordering operations that operate on arrays without Python loops.",
    "examples": [
        {"label": "sort and argsort", "code": "import numpy as np\n\narr = np.array([3, 1, 4, 1, 5, 9, 2, 6])\n\n# sort: returns sorted copy\nsorted_arr = np.sort(arr)\nprint(\"sorted:\", sorted_arr)\n\n# argsort: indices that would sort the array\nidx = np.argsort(arr)\nprint(\"argsort:\", idx)\nprint(\"verify:\", arr[idx])   # same as sorted_arr\n\n# Sort along an axis (2D)\nm = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])\nprint(\"row-wise sort:\\n\", np.sort(m, axis=1))\nprint(\"col-wise sort:\\n\", np.sort(m, axis=0))\n\n# Stable sort for multi-key sorting\nrecords = np.array([(2, \'b\'), (1, \'a\'), (2, \'a\'), (1, \'b\')],\n                   dtype=[(\'key\', int), (\'val\', \'U1\')])\nrecords.sort(order=[\'key\', \'val\'])\nprint(\"multi-key sort:\", records)"},
        {"label": "argmin, argmax, searchsorted", "code": "import numpy as np\n\ndata = np.array([10, 5, 8, 3, 15, 7, 2, 12])\n\nprint(\"min:\", data.min(), \"at index:\", data.argmin())\nprint(\"max:\", data.max(), \"at index:\", data.argmax())\n\n# 2D: axis parameter\nm = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])\nprint(\"argmin per row:\", m.argmin(axis=1))   # [1, 0, 0]\nprint(\"argmax per col:\", m.argmax(axis=0))   # [0, 2, 1]\n\n# searchsorted: binary search in sorted array (O(log n))\nsorted_data = np.array([1, 3, 5, 7, 9, 11, 13])\nvals = np.array([0, 3, 6, 14])\n\n# \'left\': index where val would be inserted to keep sorted\nleft_idx  = np.searchsorted(sorted_data, vals, side=\'left\')\nright_idx = np.searchsorted(sorted_data, vals, side=\'right\')\nprint(\"left insert positions:\", left_idx)\nprint(\"right insert positions:\", right_idx)\n\n# Use case: check if value exists\ndef is_in_sorted(arr, vals):\n    idx = np.searchsorted(arr, vals)\n    return (idx < len(arr)) & (arr[np.minimum(idx, len(arr)-1)] == vals)\n\nprint(\"vals in array:\", is_in_sorted(sorted_data, vals))"},
        {"label": "partition and argpartition (O(n) top-k)", "code": "import numpy as np\n\nnp.random.seed(42)\nscores = np.random.randint(0, 100, size=20)\nprint(\"Scores:\", scores)\n\n# partition: rearrange so k-th element is in sorted position\n# Elements left of k are <= arr[k], right are >= arr[k]\nk = 5\npartitioned = np.partition(scores, k)\nprint(f\"After partition(k={k}): {partitioned}\")\nprint(f\"Element at k={k}: {partitioned[k]} (this is the {k+1}th smallest)\")\n\n# Get top-5 scores (not sorted — just the 5 largest)\ntop5_idx  = np.argpartition(scores, -5)[-5:]\ntop5_vals = scores[top5_idx]\nprint(f\"Top-5 values (unsorted): {top5_vals}\")\nprint(f\"Top-5 values (sorted):   {np.sort(top5_vals)[::-1]}\")\n\n# Bottom-5 (smallest)\nbot5_idx  = np.argpartition(scores, 5)[:5]\nbot5_vals = scores[bot5_idx]\nprint(f\"Bottom-5 values: {np.sort(bot5_vals)}\")\n\n# Speed comparison concept: partition is O(n), sort is O(n log n)\n# For finding top-k from 1M elements, argpartition is much faster"}
    ],
    "rw": {
        "title": "Ranking Sales Reps",
        "scenario": "A sales dashboard needs to rank 10,000 reps by revenue but only display the top 100, using argpartition for O(n) efficiency instead of a full sort.",
        "code": "import numpy as np\n\nnp.random.seed(42)\nn_reps = 10_000\nrep_ids = np.arange(n_reps)\nrevenues = np.random.lognormal(mean=10, sigma=1.5, size=n_reps)\n\nK = 100  # top 100 reps\n\n# Efficient: O(n) to get top-K indices, O(K log K) to sort only those\ntop_k_idx = np.argpartition(revenues, -K)[-K:]\ntop_k_sorted = top_k_idx[np.argsort(revenues[top_k_idx])[::-1]]\n\nprint(\"Top 10 reps:\")\nfor rank, idx in enumerate(top_k_sorted[:10], 1):\n    print(f\"  Rank {rank:3d}: Rep #{rep_ids[idx]:5d} | Revenue: ${revenues[idx]:>12,.0f}\")\n\n# Percentile ranks using searchsorted\nsorted_rev = np.sort(revenues)\nsample_rev = np.array([50_000, 100_000, 500_000])\npct_ranks  = np.searchsorted(sorted_rev, sample_rev) / n_reps * 100\nfor rev, pct in zip(sample_rev, pct_ranks):\n    print(f\"  ${rev:>8,} is at the {pct:.1f}th percentile\")"
    },
    "practice": {
        "title": "Top-K Selector",
        "desc": "Write a function top_k_products(sales, k) that takes a 2D array (rows=products, cols=days) and returns the indices of the k products with the highest total sales. Use argpartition for efficiency. Also write bottom_k_days(sales, k) that returns the k days (columns) with lowest average sales across all products.",
        "starter": "import numpy as np\n\ndef top_k_products(sales, k):\n    # Sum across days (axis=1), then use argpartition\n    totals = sales.sum(axis=1)\n    idx = np.argpartition(totals, -k)[-k:]\n    return idx[np.argsort(totals[idx])[::-1]]\n\ndef bottom_k_days(sales, k):\n    # Mean across products (axis=0), then argpartition\n    daily_avg = sales.mean(axis=0)\n    idx = np.argpartition(daily_avg, k)[:k]\n    return idx[np.argsort(daily_avg[idx])]\n\nnp.random.seed(42)\nsales = np.random.poisson(100, (50, 30))   # 50 products, 30 days\ntop3  = top_k_products(sales, 3)\nbot3  = bottom_k_days(sales, 3)\nprint(\"Top 3 products (by total):\", top3, \"->\", sales[top3].sum(axis=1))\nprint(\"Worst 3 days (by avg):   \", bot3, \"->\", sales[:, bot3].mean(axis=0).round(1))\n"
    }
    },

    {
    "title": "18. Set Operations on Arrays",
    "desc": "NumPy provides unique(), union1d(), intersect1d(), setdiff1d(), and in1d()/isin() for fast set-like operations on 1D arrays using sorted-array algorithms.",
    "examples": [
        {"label": "unique and value counts", "code": "import numpy as np\n\narr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])\n\n# unique: sorted unique values\nu = np.unique(arr)\nprint(\"unique:\", u)\n\n# return_counts: how many times each value appears\nvals, counts = np.unique(arr, return_counts=True)\nprint(\"value counts:\")\nfor v, c in zip(vals, counts):\n    print(f\"  {v}: {c}\")\n\n# return_index: first occurrence index\nvals, idx = np.unique(arr, return_index=True)\nprint(\"first occurrence indices:\", idx)\n\n# return_inverse: reconstruct original from unique\nvals, inv = np.unique(arr, return_inverse=True)\nprint(\"unique:\", vals)\nprint(\"inverse:\", inv)\nprint(\"reconstructed:\", vals[inv])  # should match arr\n\n# Most common value (mode-like)\nmode_val = vals[np.argmax(counts)]\nprint(f\"Mode: {mode_val} (appears {counts.max()} times)\")"},
        {"label": "union1d, intersect1d, setdiff1d, setxor1d", "code": "import numpy as np\n\na = np.array([1, 2, 3, 4, 5])\nb = np.array([3, 4, 5, 6, 7])\n\nprint(\"union (a | b):      \", np.union1d(a, b))\nprint(\"intersect (a & b):  \", np.intersect1d(a, b))\nprint(\"a - b (in a not b): \", np.setdiff1d(a, b))\nprint(\"b - a (in b not a): \", np.setdiff1d(b, a))\nprint(\"symmetric diff:     \", np.setxor1d(a, b))\n\n# With return_indices for intersect\ncommon, a_idx, b_idx = np.intersect1d(a, b, return_indices=True)\nprint(\"Common:\", common, \"at a:\", a_idx, \"at b:\", b_idx)\n\n# Practical: find new customers\nold_customers = np.array([101, 102, 103, 104, 105])\nnew_customers = np.array([103, 104, 106, 107, 108])\nreturning = np.intersect1d(old_customers, new_customers)\nbrand_new = np.setdiff1d(new_customers, old_customers)\nchurned   = np.setdiff1d(old_customers, new_customers)\nprint(f\"Returning: {returning}\")\nprint(f\"Brand new: {brand_new}\")\nprint(f\"Churned:   {churned}\")"},
        {"label": "isin / in1d for membership testing", "code": "import numpy as np\n\nproducts = np.array([\'apple\', \'banana\', \'cherry\', \'date\', \'elderberry\'])\nblacklist = np.array([\'banana\', \'date\', \'fig\'])\n\n# isin: element-wise membership test\nmask = np.isin(products, blacklist)\nprint(\"Is in blacklist:\", mask)\nprint(\"Allowed products:\", products[~mask])\nprint(\"Blocked products:\", products[mask])\n\n# Large-scale membership test (much faster than Python loops)\nnp.random.seed(42)\nuser_ids      = np.arange(1_000_000)\npremium_users = np.random.choice(user_ids, size=50_000, replace=False)\n\n# Check a sample of 1000 users\nsample = np.random.choice(user_ids, size=1000, replace=False)\nis_premium = np.isin(sample, premium_users)\nprint(f\"Sample size: {len(sample)}, Premium users in sample: {is_premium.sum()}\")\n\n# in1d is equivalent (older API)\nsame_result = np.in1d(sample, premium_users)\nprint(\"isin == in1d:\", np.all(is_premium == same_result))\n\n# Invert: users NOT in premium\nnon_premium = sample[~is_premium]\nprint(f\"Non-premium in sample: {len(non_premium)}\")"}
    ],
    "rw": {
        "title": "Inventory Reconciliation",
        "scenario": "A warehouse system compares today\'s scan vs expected manifest using NumPy set operations to find missing, extra, and duplicate items instantly across 100K SKUs.",
        "code": "import numpy as np\n\nnp.random.seed(42)\nmanifest = np.random.choice(np.arange(200_000), size=100_000, replace=False)\n\n# Simulate scanning: miss 500, add 300 unexpected\nmissed_idx   = np.random.choice(len(manifest), size=500, replace=False)\nextra_skus   = np.random.randint(200_000, 201_000, size=300)\nscanned      = np.concatenate([np.delete(manifest, missed_idx), extra_skus])\n\nmanifest_u = np.unique(manifest)\nscanned_u  = np.unique(scanned)\n\nmissing      = np.setdiff1d(manifest_u, scanned_u)\nunexpected   = np.setdiff1d(scanned_u, manifest_u)\nconfirmed    = np.intersect1d(manifest_u, scanned_u)\n\n# Duplicates in scan\nvals, counts = np.unique(scanned, return_counts=True)\nduplicates   = vals[counts > 1]\n\nprint(f\"Manifest:    {len(manifest_u):,} SKUs\")\nprint(f\"Scanned:     {len(scanned_u):,} unique SKUs\")\nprint(f\"Confirmed:   {len(confirmed):,} ({len(confirmed)/len(manifest_u):.1%})\")\nprint(f\"Missing:     {len(missing):,}\")\nprint(f\"Unexpected:  {len(unexpected):,}\")\nprint(f\"Duplicates:  {len(duplicates):,}\")\nprint(f\"Accuracy:    {len(confirmed)/len(manifest_u):.2%}\")"
    },
    "practice": {
        "title": "Cohort Analysis",
        "desc": "Write a function cohort_analysis(cohorts: dict) where cohorts maps week labels to user_id arrays. For each week, compute: (1) new users (not seen in any previous week), (2) returning users (seen in at least one previous week), (3) churned from previous week. Return a list of dicts with these counts.",
        "starter": "import numpy as np\n\ndef cohort_analysis(cohorts):\n    results = []\n    seen_so_far = np.array([], dtype=int)\n    prev_week   = np.array([], dtype=int)\n\n    for week, users in sorted(cohorts.items()):\n        users = np.unique(users)\n        new_users  = np.setdiff1d(users, seen_so_far)\n        returning  = np.intersect1d(users, seen_so_far)\n        churned    = np.setdiff1d(prev_week, users)\n\n        results.append({\n            \"week\": week, \"total\": len(users),\n            \"new\": len(new_users), \"returning\": len(returning),\n            \"churned_from_prev\": len(churned),\n        })\n        seen_so_far = np.union1d(seen_so_far, users)\n        prev_week   = users\n    return results\n\nnp.random.seed(42)\ncohorts = {\n    \"W1\": np.random.randint(0, 100, 50),\n    \"W2\": np.random.randint(20, 120, 60),\n    \"W3\": np.random.randint(40, 140, 55),\n    \"W4\": np.random.randint(60, 160, 70),\n}\nfor r in cohort_analysis(cohorts):\n    print(r)\n"
    }
    },

    {
    "title": "19. Numerical Stability, NaN & Inf Handling",
    "desc": "Floating-point arithmetic has precision limits, NaN propagation, and overflow. NumPy provides tools to detect, mask, and safely handle these edge cases.",
    "examples": [
        {"label": "NaN detection and handling", "code": "import numpy as np\n\ndata = np.array([1.0, 2.0, np.nan, 4.0, np.nan, 6.0])\n\n# Detection\nprint(\"isnan:\", np.isnan(data))\nprint(\"Count NaNs:\", np.isnan(data).sum())\nprint(\"Any NaN:\", np.any(np.isnan(data)))\n\n# NaN-safe aggregations\nprint(\"mean with NaN:\", np.mean(data))          # nan\nprint(\"nanmean:\", np.nanmean(data))              # 3.25\nprint(\"nansum:\", np.nansum(data))               # 13.0\nprint(\"nanstd:\", np.nanstd(data).round(4))\nprint(\"nanmin/nanmax:\", np.nanmin(data), np.nanmax(data))\n\n# Replace NaN\nfilled_mean = np.where(np.isnan(data), np.nanmean(data), data)\nprint(\"NaN -> mean:\", filled_mean)\n\nfilled_zero = np.nan_to_num(data, nan=0.0)\nprint(\"NaN -> 0:   \", filled_zero)\n\n# Forward fill (pandas-style, pure numpy)\ndef ffill(arr):\n    mask = np.isnan(arr)\n    idx = np.where(~mask, np.arange(len(arr)), 0)\n    np.maximum.accumulate(idx, out=idx)\n    return arr[idx]\n\nprint(\"Forward fill:\", ffill(data))"},
        {"label": "Inf, overflow, and finfo", "code": "import numpy as np\n\n# Infinity\nx = np.array([1.0, -1.0, 0.0, np.inf, -np.inf, np.nan])\nprint(\"isinf:\", np.isinf(x))\nprint(\"isfinite:\", np.isfinite(x))\nprint(\"isnan:\", np.isnan(x))\n\n# All-in-one\nprint(\"Any problem:\", ~np.isfinite(x).all())\n\n# Replace inf with large values\nclean = np.nan_to_num(x, nan=0.0, posinf=1e9, neginf=-1e9)\nprint(\"Cleaned:\", clean)\n\n# Overflow\nfloat32 = np.float32(1e38)\nprint(\"float32 * 100:\", float32 * 100)     # inf\nprint(\"float32 dtype max:\", np.finfo(np.float32).max)\n\n# Machine epsilon\nfor dtype in [np.float16, np.float32, np.float64]:\n    fi = np.finfo(dtype)\n    print(f\"{dtype.__name__:10s}: eps={fi.eps:.2e}, max={fi.max:.2e}\")\n\n# Division edge cases\nprint(\"0/0:\", np.float64(0) / np.float64(0))  # nan\nprint(\"1/0:\", np.float64(1) / np.float64(0))  # inf"},
        {"label": "Numerical precision and stable computations", "code": "import numpy as np\n\n# Floating-point is NOT exact\na = 0.1 + 0.2\nprint(\"0.1 + 0.2 ==  0.3:\", a == 0.3)     # False!\nprint(\"value:\", repr(a))\nprint(\"allclose:\", np.isclose(a, 0.3))     # True (with tolerance)\n\n# np.isclose with tolerances\nx = np.array([1.0, 1.0 + 1e-8, 1.0 + 1e-5, 1.1])\nprint(\"isclose to 1.0:\", np.isclose(x, 1.0, rtol=1e-5, atol=1e-8))\n\n# Unstable: sum of large+small+large\nbig  = np.float32(1e8)\ntiny = np.float32(1.0)\nprint(\"float32 (1e8 + 1 - 1e8):\", big + tiny - big)  # may be 0!\n\n# Kahan compensated summation is more stable\n# np.sum uses pairwise summation which is better than naive\nx = np.random.randn(1_000_000).astype(np.float32)\nnaive_sum = float(x[0])\nfor v in x[1:]:\n    naive_sum += float(v)\n\nnp_sum = float(np.sum(x, dtype=np.float64))  # promote to float64\nprint(f\"Naive float32 sum: {naive_sum:.4f}\")\nprint(f\"NumPy float64 sum: {np_sum:.4f}\")\n\n# Log-sum-exp trick for numerical stability (important in ML)\nlogits = np.array([1000.0, 1001.0, 999.0])  # would overflow exp()\nlse = logits.max() + np.log(np.sum(np.exp(logits - logits.max())))\nprint(f\"Log-sum-exp (stable): {lse:.6f}\")"}
    ],
    "rw": {
        "title": "Financial Return Calculator",
        "scenario": "A risk system computes daily returns from price series that contain missing quotes (NaN), halted trading (0), and data errors (negative prices).",
        "code": "import numpy as np\n\nnp.random.seed(42)\nn_days = 252\nprices = 100 * np.exp(np.cumsum(np.random.randn(n_days) * 0.01))\n\n# Inject data quality issues\nprices[10]  = np.nan    # missing quote\nprices[50]  = 0.0       # trading halt\nprices[100] = -5.0      # data error\n\ndef clean_prices(prices):\n    p = prices.copy()\n    # Remove physically impossible values\n    p[p <= 0] = np.nan\n    # Forward-fill NaN\n    mask = np.isnan(p)\n    idx  = np.where(~mask, np.arange(len(p)), 0)\n    np.maximum.accumulate(idx, out=idx)\n    p = p[idx]\n    return p\n\ndef daily_returns(prices):\n    p = clean_prices(prices)\n    rets = np.diff(p) / p[:-1]\n    rets = rets[np.isfinite(rets)]\n    return rets\n\nrets = daily_returns(prices)\nprint(f\"Days cleaned: {np.isnan(prices).sum() + (prices <= 0).sum()}\")\nprint(f\"Valid returns: {len(rets)}\")\nprint(f\"Mean return: {np.nanmean(rets):.4%}\")\nprint(f\"Volatility:  {np.nanstd(rets):.4%}\")\nprint(f\"Sharpe (approx): {np.nanmean(rets)/np.nanstd(rets)*np.sqrt(252):.2f}\")"
    },
    "practice": {
        "title": "Stable Softmax",
        "desc": "Implement stable_softmax(x) that computes softmax using the log-sum-exp trick to avoid overflow. Implement log_softmax(x) using the same trick. Verify both give the same probabilities on x = [1000, 1001, 999] and x = [-1000, -999, -1001]. Compare against naive softmax to show instability.",
        "starter": "import numpy as np\n\ndef naive_softmax(x):\n    e = np.exp(x)\n    return e / e.sum()\n\ndef stable_softmax(x):\n    # TODO: subtract max(x) before exp, then normalize\n    pass\n\ndef log_softmax(x):\n    # TODO: return log of stable softmax (more numerically stable version)\n    # hint: x - max(x) - log(sum(exp(x - max(x))))\n    pass\n\nfor x in [np.array([1.0, 2.0, 3.0]),\n          np.array([1000.0, 1001.0, 999.0]),\n          np.array([-1000.0, -999.0, -1001.0])]:\n    print(f\"x = {x}\")\n    print(f\"  naive:  {naive_softmax(x)}\")\n    print(f\"  stable: {stable_softmax(x)}\")\n    print(f\"  log:    {log_softmax(x)}\")\n    print(f\"  exp(log) == stable: {np.allclose(np.exp(log_softmax(x)), stable_softmax(x))}\")\n"
    }
    },

    {
    "title": "20. Probability Distributions & Random Sampling",
    "desc": "NumPy\'s random module (Generator API) provides reproducible random sampling from dozens of distributions. Essential for simulations, bootstrapping, and synthetic data.",
    "examples": [
        {"label": "Generator API and reproducibility", "code": "import numpy as np\n\n# Modern API: use default_rng (preferred over np.random.seed)\nrng = np.random.default_rng(seed=42)\n\n# Uniform\nu = rng.uniform(low=0, high=10, size=5)\nprint(\"uniform:\", u.round(2))\n\n# Integers\ndice = rng.integers(1, 7, size=10)\nprint(\"dice rolls:\", dice)\n\n# Shuffle and choice\nitems = np.arange(10)\nrng.shuffle(items)\nprint(\"shuffled:\", items)\n\nsample = rng.choice(items, size=5, replace=False)\nprint(\"sample without replacement:\", sample)\n\n# Weighted choice\nweights  = np.array([0.5, 0.3, 0.2])\noutcomes = np.array([\'A\', \'B\', \'C\'])\ndraws    = rng.choice(outcomes, size=20, p=weights)\nvals, counts = np.unique(draws, return_counts=True)\nprint(\"Weighted draws:\", dict(zip(vals, counts)))\n\n# Verify reproducibility\nrng2 = np.random.default_rng(seed=42)\nprint(\"Same sequence:\", np.all(rng2.uniform(size=5) == np.random.default_rng(42).uniform(size=5)))"},
        {"label": "Statistical distributions", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Normal distribution\nheights = rng.normal(loc=170, scale=10, size=10_000)\nprint(f\"Normal(170, 10): mean={heights.mean():.2f}, std={heights.std():.2f}\")\n\n# Lognormal (for prices, incomes)\nprices = rng.lognormal(mean=3.0, sigma=0.5, size=5000)\nprint(f\"Lognormal: median={np.median(prices):.2f}, mean={prices.mean():.2f}\")\n\n# Exponential (wait times, inter-arrivals)\nwait_times = rng.exponential(scale=5.0, size=1000)  # mean = 5 min\nprint(f\"Exponential(lambda=0.2): mean={wait_times.mean():.2f}\")\n\n# Poisson (event counts)\nrequests_per_sec = rng.poisson(lam=30, size=60)  # 30 req/s for 1 min\nprint(f\"Poisson(30): mean={requests_per_sec.mean():.1f}, std={requests_per_sec.std():.1f}\")\n\n# Binomial (successes in n trials)\nsuccesses = rng.binomial(n=100, p=0.35, size=1000)  # conversion rate\nprint(f\"Binomial(100, 0.35): mean={successes.mean():.1f} (expected 35)\")\n\n# Beta (probabilities, proportions)\nclick_rates = rng.beta(a=2, b=5, size=1000)\nprint(f\"Beta(2, 5): mean={click_rates.mean():.3f} (expected {2/(2+5):.3f})\")"},
        {"label": "Bootstrap sampling and Monte Carlo", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Bootstrap confidence interval\ndata = np.array([2.3, 4.1, 3.8, 5.2, 2.9, 4.7, 3.5, 6.1, 2.8, 4.4])\n\nn_boot = 10_000\nboot_means = np.array([\n    rng.choice(data, size=len(data), replace=True).mean()\n    for _ in range(n_boot)\n])\n\nci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])\nprint(f\"Sample mean: {data.mean():.3f}\")\nprint(f\"95% bootstrap CI: [{ci_low:.3f}, {ci_high:.3f}]\")\n\n# Monte Carlo Pi estimation\nN = 1_000_000\nx = rng.uniform(-1, 1, N)\ny = rng.uniform(-1, 1, N)\ninside = (x**2 + y**2) <= 1.0\npi_est = 4 * inside.mean()\nprint(f\"Pi estimate (N={N:,}): {pi_est:.5f} (true: {np.pi:.5f})\")\n\n# Simulate portfolio returns (Monte Carlo)\nn_assets, n_sims, n_days = 5, 10_000, 252\nmu    = rng.uniform(0.0001, 0.001, n_assets)   # daily expected return\nsigma = rng.uniform(0.01, 0.03, n_assets)       # daily vol\ndaily_rets = rng.normal(mu, sigma, (n_sims, n_days, n_assets))\nport_rets  = daily_rets.mean(axis=2).sum(axis=1)  # equal weight\nvar_95 = np.percentile(port_rets, 5)\nprint(f\"Portfolio annual return mean: {port_rets.mean():.2%}\")\nprint(f\"VaR 95%: {var_95:.2%}\")"}
    ],
    "rw": {
        "title": "A/B Test Simulation",
        "scenario": "A product team uses bootstrap simulation to determine whether a 2-percentage-point conversion rate improvement is statistically significant given their sample sizes.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Observed data\nn_control    = 5000\nn_treatment  = 5000\nconv_control = 0.10   # 10% baseline\nconv_treat   = 0.12   # 12% treatment (absolute +2pp)\n\n# Sample from observed proportions\ncontrol   = rng.binomial(1, conv_control, n_control)\ntreatment = rng.binomial(1, conv_treat,   n_treatment)\n\nobs_diff = treatment.mean() - control.mean()\nprint(f\"Observed difference: {obs_diff:.4f} ({obs_diff:.2%})\")\n\n# Permutation test\nN_PERM = 10_000\ncombined = np.concatenate([control, treatment])\nperm_diffs = np.empty(N_PERM)\nfor i in range(N_PERM):\n    rng.shuffle(combined)\n    perm_diffs[i] = combined[:n_treatment].mean() - combined[n_treatment:].mean()\n\np_value = (np.abs(perm_diffs) >= np.abs(obs_diff)).mean()\nprint(f\"Permutation test p-value: {p_value:.4f}\")\nprint(f\"Significant at alpha=0.05: {p_value < 0.05}\")\n\nci = np.percentile(perm_diffs, [2.5, 97.5])\nprint(f\"Null distribution 95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]\")"
    },
    "practice": {
        "title": "Distribution Fitter",
        "desc": "Write fit_normal(data) that uses np.mean and np.std to estimate parameters, then generates n_samples from that distribution and computes the KS-like statistic (max absolute difference between sorted empirical CDF and normal CDF). Also write simulate_geometric_brownian(S0, mu, sigma, T, n_steps) for stock price simulation.",
        "starter": "import numpy as np\n\ndef fit_normal(data, n_samples=1000, seed=42):\n    rng = np.random.default_rng(seed)\n    mu  = np.mean(data)\n    std = np.std(data, ddof=1)\n    # Generate from fitted distribution\n    synthetic = rng.normal(mu, std, n_samples)\n    # Empirical CDF comparison\n    emp  = np.sort(data)\n    emp_cdf = np.arange(1, len(emp)+1) / len(emp)\n    # Normal CDF at emp points: use error function approximation\n    from math import erf\n    norm_cdf = np.array([0.5 * (1 + erf((x-mu)/(std*2**0.5))) for x in emp])\n    ks_stat  = np.max(np.abs(emp_cdf - norm_cdf))\n    return {\"mu\": mu, \"std\": std, \"ks\": ks_stat, \"synthetic\": synthetic}\n\ndef simulate_gbm(S0, mu, sigma, T, n_steps, seed=42):\n    rng = np.random.default_rng(seed)\n    dt  = T / n_steps\n    Z   = rng.standard_normal(n_steps)\n    # TODO: compute log returns and cumulative prices\n    pass\n\nrng = np.random.default_rng(42)\ndata = rng.normal(50, 10, 200)\nresult = fit_normal(data)\nprint(f\"Fitted: mu={result[\'mu\']:.2f}, std={result[\'std\']:.2f}, KS={result[\'ks\']:.4f}\")\n"
    }
    },

    {
    "title": "21. Image Arrays & 2D Operations",
    "desc": "Images are 2D (grayscale) or 3D (H x W x C) NumPy arrays. Understanding array operations on images builds intuition for convolutions, pooling, and data augmentation.",
    "examples": [
        {"label": "Image as array: channels and pixel operations", "code": "import numpy as np\n\n# Images are (H, W) for grayscale, (H, W, C) for color\nnp.random.seed(42)\nH, W = 64, 64\n\n# Synthetic grayscale (0-255 uint8)\ngray = np.random.randint(0, 256, (H, W), dtype=np.uint8)\nprint(f\"Grayscale shape: {gray.shape}, dtype: {gray.dtype}\")\nprint(f\"Pixel range: [{gray.min()}, {gray.max()}]\")\n\n# Synthetic RGB image\nrgb = np.random.randint(0, 256, (H, W, 3), dtype=np.uint8)\nprint(f\"RGB shape: {rgb.shape}\")\n\n# Extract channels\nR, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]\nprint(f\"R channel mean: {R.mean():.1f}\")\n\n# RGB to grayscale (luminosity formula)\ngray_from_rgb = (0.2989 * R + 0.5870 * G + 0.1140 * B).astype(np.uint8)\nprint(f\"Converted gray shape: {gray_from_rgb.shape}\")\n\n# Normalize to [0, 1] float\nimg_float = rgb.astype(np.float32) / 255.0\nprint(f\"Normalized range: [{img_float.min():.3f}, {img_float.max():.3f}]\")\n\n# Crop a region\ncrop = rgb[10:40, 15:50, :]\nprint(f\"Crop shape: {crop.shape}\")\n\n# Horizontal flip\nflipped = rgb[:, ::-1, :]\nprint(f\"Flipped shape: {flipped.shape}\")"},
        {"label": "Convolution and pooling with strides", "code": "import numpy as np\n\ndef convolve2d(img, kernel):\n    H, W = img.shape\n    kH, kW = kernel.shape\n    pad_h, pad_w = kH // 2, kW // 2\n    # Zero-pad\n    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode=\'constant\')\n    output = np.zeros_like(img, dtype=float)\n    for i in range(H):\n        for j in range(W):\n            output[i, j] = (padded[i:i+kH, j:j+kW] * kernel).sum()\n    return output\n\n# Faster with stride_tricks (no Python loop)\ndef convolve2d_fast(img, kernel):\n    from numpy.lib.stride_tricks import sliding_window_view\n    H, W = img.shape\n    kH, kW = kernel.shape\n    pad_h, pad_w = kH // 2, kW // 2\n    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode=\'constant\')\n    windows = sliding_window_view(padded, (kH, kW))\n    return (windows * kernel).sum(axis=(-2, -1))\n\nimg = np.random.rand(32, 32)\n# Edge detection kernel (Sobel-like)\nsobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)\nedges = convolve2d_fast(img, sobel_x)\nprint(f\"Edge response range: [{edges.min():.3f}, {edges.max():.3f}]\")\n\n# Max pooling (2x2)\ndef max_pool2d(img, size=2):\n    H, W = img.shape\n    pH, pW = H // size, W // size\n    return img[:pH*size, :pW*size].reshape(pH, size, pW, size).max(axis=(1, 3))\n\npooled = max_pool2d(img, 2)\nprint(f\"After 2x2 max pool: {img.shape} -> {pooled.shape}\")"},
        {"label": "Data augmentation with NumPy", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\ndef augment_batch(images, rng):\n    # Augment a batch of images (N, H, W, C).\n    batch = images.copy().astype(np.float32)\n\n    # Random horizontal flip (50% chance per image)\n    flip_mask = rng.random(len(batch)) > 0.5\n    batch[flip_mask] = batch[flip_mask, :, ::-1, :]\n\n    # Random brightness adjustment\n    brightness = rng.uniform(0.8, 1.2, (len(batch), 1, 1, 1))\n    batch = np.clip(batch * brightness, 0, 255)\n\n    # Random crop and resize (simplified: just crop to 80% size)\n    H, W = batch.shape[1:3]\n    ch, cw = int(H * 0.8), int(W * 0.8)\n    for i in range(len(batch)):\n        y0 = rng.integers(0, H - ch)\n        x0 = rng.integers(0, W - cw)\n        # In real pipeline you would resize; here just show crop\n        batch[i, :ch, :cw, :] = batch[i, y0:y0+ch, x0:x0+cw, :]\n\n    # Gaussian noise\n    noise = rng.normal(0, 5, batch.shape)\n    batch = np.clip(batch + noise, 0, 255)\n\n    return batch.astype(np.uint8)\n\n# Demo\nN, H, W, C = 8, 64, 64, 3\nbatch = rng.integers(50, 200, (N, H, W, C), dtype=np.uint8)\naugmented = augment_batch(batch, rng)\nprint(f\"Batch: {batch.shape} | Augmented: {augmented.shape}\")\nprint(f\"Orig mean: {batch.mean():.1f} | Aug mean: {augmented.mean():.1f}\")"}
    ],
    "rw": {
        "title": "Batch Preprocessing Pipeline",
        "scenario": "A CNN training loop preprocesses a batch of 64x64 RGB images: normalize per-channel, apply random augmentation, and flatten into model input.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\nN, H, W, C = 32, 64, 64, 3\n\n# Simulate a batch\nbatch = rng.integers(0, 256, (N, H, W, C), dtype=np.uint8)\n\n# ImageNet-style normalization (per-channel mean/std)\nMEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)\nSTD  = np.array([0.229, 0.224, 0.225], dtype=np.float32)\n\ndef preprocess(batch):\n    x = batch.astype(np.float32) / 255.0  # [0,1]\n    x = (x - MEAN) / STD                  # normalize\n    x = x.transpose(0, 3, 1, 2)           # NHWC -> NCHW for PyTorch\n    return x\n\n# Random horizontal flip augmentation\ndef random_hflip(batch, rng, p=0.5):\n    mask = rng.random(len(batch)) < p\n    out  = batch.copy()\n    out[mask] = batch[mask, :, ::-1, :]\n    return out\n\nprocessed = preprocess(random_hflip(batch, rng))\nprint(f\"Input: {batch.shape} uint8\")\nprint(f\"Output: {processed.shape} float32\")\nprint(f\"Channel 0: mean={processed[:,0,:,:].mean():.3f}, std={processed[:,0,:,:].std():.3f}\")"
    },
    "practice": {
        "title": "Image Statistics",
        "desc": "Write a function image_stats(img) that takes a (H,W,3) uint8 image and returns a dict with per-channel mean, std, min, max, and the percentage of \'near-white\' pixels (all channels > 200) and \'near-black\' pixels (all channels < 55). Also write normalize_contrast(img) that maps pixel values to [0,255] using min-max normalization per channel.",
        "starter": "import numpy as np\n\ndef image_stats(img):\n    # img is (H, W, 3) uint8\n    stats = {}\n    for c, name in enumerate([\'R\', \'G\', \'B\']):\n        ch = img[:, :, c].astype(float)\n        stats[name] = {\"mean\": ch.mean(), \"std\": ch.std(),\n                       \"min\": int(ch.min()), \"max\": int(ch.max())}\n    # Near white: all channels > 200\n    near_white = (img > 200).all(axis=2)\n    # Near black: all channels < 55\n    near_black = (img < 55).all(axis=2)\n    stats[\"near_white_pct\"] = near_white.mean() * 100\n    stats[\"near_black_pct\"] = near_black.mean() * 100\n    return stats\n\ndef normalize_contrast(img):\n    # TODO: for each channel, map min->0, max->255\n    out = np.empty_like(img, dtype=np.uint8)\n    for c in range(3):\n        ch = img[:, :, c].astype(float)\n        lo, hi = ch.min(), ch.max()\n        if hi > lo:\n            out[:, :, c] = ((ch - lo) / (hi - lo) * 255).astype(np.uint8)\n        else:\n            out[:, :, c] = 0\n    return out\n\nrng = np.random.default_rng(42)\nimg = rng.integers(0, 256, (128, 128, 3), dtype=np.uint8)\nstats = image_stats(img)\nfor k, v in stats.items():\n    print(f\"{k}: {v}\")\nnormed = normalize_contrast(img)\nprint(\"Normalized range:\", normed.min(), normed.max())\n"
    }
    },

    {
    "title": "22. Statistical Aggregations",
    "desc": "NumPy provides percentiles, histograms, correlation, and covariance for descriptive statistics. These underpin nearly all data analysis workflows.",
    "examples": [
        {"label": "Percentile, quantile, and descriptive stats", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\ndata = rng.lognormal(mean=4.5, sigma=0.8, size=10_000)\n\n# Percentiles and quantiles\np25, p50, p75 = np.percentile(data, [25, 50, 75])\nprint(f\"Q1={p25:.1f}, Median={p50:.1f}, Q3={p75:.1f}\")\nprint(f\"IQR={p75-p25:.1f}\")\n\n# Quantile (equivalent but takes fractions 0-1)\nq  = np.quantile(data, [0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1.0])\nlabels = [\"0%\", \"25%\", \"50%\", \"75%\", \"90%\", \"95%\", \"99%\", \"100%\"]\nfor l, v in zip(labels, q):\n    print(f\"  {l:>4s}: {v:>8.1f}\")\n\n# Outlier detection via IQR\niqr_mult = 1.5\nlower = p25 - iqr_mult * (p75 - p25)\nupper = p75 + iqr_mult * (p75 - p25)\noutliers = data[(data < lower) | (data > upper)]\nprint(f\"Outliers: {len(outliers)} ({len(outliers)/len(data):.1%})\")\n\n# 2D: percentile per column\nm = rng.normal(0, 1, (100, 5))\ncol_medians = np.median(m, axis=0)\nprint(\"Col medians:\", col_medians.round(2))"},
        {"label": "Histogram and frequency analysis", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\ndata = np.concatenate([rng.normal(30, 5, 3000),   # young cohort\n                       rng.normal(55, 8, 2000)])   # senior cohort\n\n# Basic histogram\ncounts, edges = np.histogram(data, bins=20)\ncenters = (edges[:-1] + edges[1:]) / 2\nprint(\"Histogram (first 5 bins):\")\nfor c, n in zip(centers[:5], counts[:5]):\n    print(f\"  {c:.1f}: {\'#\' * (n//50)} ({n})\")\n\n# Normalized (density)\ndensity, _ = np.histogram(data, bins=20, density=True)\nprint(f\"Density sums to: {density.sum() * np.diff(edges).mean():.4f}\")  # ~1.0\n\n# 2D histogram\nx = rng.normal(0, 1, 5000)\ny = 0.7 * x + rng.normal(0, 0.5, 5000)  # correlated\ncounts_2d, xedges, yedges = np.histogram2d(x, y, bins=10)\nprint(f\"2D histogram shape: {counts_2d.shape}\")\nprint(f\"Peak bin count: {counts_2d.max():.0f}\")\n\n# Digitize: assign each value to a bin\nsalary_bins = np.array([0, 30_000, 60_000, 100_000, 200_000, np.inf])\nlabels = [\'entry\', \'junior\', \'mid\', \'senior\', \'exec\']\nsalaries = np.array([25000, 45000, 75000, 120000, 350000, 58000])\nbin_idx  = np.digitize(salaries, salary_bins) - 1\nprint(\"Salary bands:\", [labels[min(i, len(labels)-1)] for i in bin_idx])"},
        {"label": "Correlation and covariance", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\nn = 200\n\n# Generate correlated variables\nx1 = rng.normal(0, 1, n)\nx2 = 0.8 * x1 + rng.normal(0, 0.6, n)   # strong positive correlation\nx3 = rng.normal(0, 1, n)                  # uncorrelated\n\ndata = np.column_stack([x1, x2, x3])\n\n# Pearson correlation matrix\ncorr = np.corrcoef(data.T)  # data.T because corrcoef expects (n_vars, n_obs)\nprint(\"Correlation matrix:\")\nfor row in corr:\n    print(\"  \", \" \".join(f\"{v:+.3f}\" for v in row))\n\n# Covariance matrix\ncov = np.cov(data.T)\nprint(\"Covariance matrix diagonal (variances):\", np.diag(cov).round(3))\n\n# Manual Pearson r for two variables\ndef pearson_r(a, b):\n    a_c, b_c = a - a.mean(), b - b.mean()\n    return (a_c * b_c).sum() / (np.sqrt((a_c**2).sum()) * np.sqrt((b_c**2).sum()))\n\nr12 = pearson_r(x1, x2)\nr13 = pearson_r(x1, x3)\nprint(f\"Pearson r(x1,x2)={r12:.3f}, r(x1,x3)={r13:.3f}\")\n\n# Rolling correlation\nwindow = 30\nroll_corr = np.array([\n    pearson_r(x1[i:i+window], x2[i:i+window])\n    for i in range(n - window)\n])\nprint(f\"Rolling({window}) correlation: mean={roll_corr.mean():.3f}\")"}
    ],
    "rw": {
        "title": "Multi-Asset Risk Analysis",
        "scenario": "A risk team computes the 1-day 99% VaR and expected shortfall for a 10-asset portfolio using historical simulation on 5 years of daily returns.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\nn_assets = 10\nn_days   = 1260   # 5 trading years\n\n# Simulate correlated returns\ntrue_corr = 0.3 * np.ones((n_assets, n_assets)) + 0.7 * np.eye(n_assets)\nL = np.linalg.cholesky(true_corr)\nZ = rng.standard_normal((n_days, n_assets))\nreturns = (Z @ L.T) * 0.01  # ~1% daily vol\n\n# Equal-weight portfolio returns\nweights  = np.ones(n_assets) / n_assets\nport_ret = returns @ weights\n\n# Risk metrics\nvar_99   = np.percentile(port_ret, 1)\nes_99    = port_ret[port_ret <= var_99].mean()\nann_vol  = port_ret.std() * np.sqrt(252)\n\nprint(f\"Portfolio daily returns: mean={port_ret.mean():.4%}, vol={port_ret.std():.4%}\")\nprint(f\"Annualized vol:    {ann_vol:.2%}\")\nprint(f\"1-day VaR (99%):   {var_99:.4%}\")\nprint(f\"Expected Shortfall (CVaR 99%): {es_99:.4%}\")\n\n# Correlation matrix\ncorr = np.corrcoef(returns.T)\nprint(f\"Avg pairwise correlation: {corr[np.triu_indices(n_assets, k=1)].mean():.3f}\")"
    },
    "practice": {
        "title": "Weighted Statistics",
        "desc": "Implement weighted_mean(data, weights), weighted_std(data, weights, ddof=0), and weighted_percentile(data, weights, q) where weights represent observation frequencies. Verify weighted_mean on data=[1,2,3,4,5] with weights=[5,1,1,1,1] (mean should be close to 1 since 5 is heavily weighted).",
        "starter": "import numpy as np\n\ndef weighted_mean(data, weights):\n    data, weights = np.asarray(data, float), np.asarray(weights, float)\n    # TODO: return sum(data * weights) / sum(weights)\n    pass\n\ndef weighted_std(data, weights, ddof=0):\n    mean = weighted_mean(data, weights)\n    # TODO: compute weighted variance then sqrt\n    # variance = sum(w * (x - mean)^2) / sum(w) for ddof=0\n    pass\n\ndef weighted_percentile(data, weights, q):\n    # Sort data by value, then compute cumulative weight fraction\n    data, weights = np.asarray(data, float), np.asarray(weights, float)\n    idx     = np.argsort(data)\n    sdata   = data[idx]\n    sweights = weights[idx]\n    cumw    = np.cumsum(sweights) / sweights.sum()\n    # TODO: interpolate to find value at quantile q (0-100)\n    pass\n\ndata    = np.array([1, 2, 3, 4, 5], float)\nweights = np.array([5, 1, 1, 1, 1], float)\nprint(\"Weighted mean:\", weighted_mean(data, weights))   # should be ~1.5\nprint(\"Weighted std: \", weighted_std(data, weights))\nprint(\"Weighted 50th:\", weighted_percentile(data, weights, 50))\n"
    }
    },

    {
    "title": "23. Array I/O (save, load, text, memmap)",
    "desc": "NumPy supports binary (.npy, .npz), text (savetxt/genfromtxt), and memory-mapped file formats for efficient large array storage and loading.",
    "examples": [
        {"label": "np.save, np.load, np.savez", "code": "import numpy as np\nimport tempfile, pathlib\n\ntmp = pathlib.Path(tempfile.mkdtemp())\n\n# Save/load single array (.npy)\narr = np.arange(12).reshape(3, 4)\nnp.save(tmp / \'array.npy\', arr)\n\nloaded = np.load(tmp / \'array.npy\')\nprint(\"Loaded:\", loaded)\nprint(\"Same data:\", np.array_equal(arr, loaded))\nprint(\"File size:\", (tmp / \'array.npy\').stat().st_size, \"bytes\")\n\n# Save multiple arrays in one file (.npz = numpy zip)\nx  = np.linspace(0, 10, 100)\ny  = np.sin(x)\ndy = np.cos(x)\nnp.savez(tmp / \'signals.npz\', x=x, y=y, dy=dy)\n\ndata = np.load(tmp / \'signals.npz\')\nprint(\"Keys in npz:\", list(data.keys()))\nprint(\"x[0:3]:\", data[\'x\'][:3].round(3))\n\n# savez_compressed: gzip compression\nnp.savez_compressed(tmp / \'signals_compressed.npz\', **dict(data))\norig_size = (tmp / \'signals.npz\').stat().st_size\ncomp_size = (tmp / \'signals_compressed.npz\').stat().st_size\nprint(f\"Original: {orig_size} bytes, Compressed: {comp_size} bytes ({comp_size/orig_size:.0%})\")\n\nimport shutil; shutil.rmtree(tmp)"},
        {"label": "savetxt and genfromtxt", "code": "import numpy as np\nimport tempfile, pathlib\n\ntmp = pathlib.Path(tempfile.mkdtemp())\n\n# savetxt: write to CSV/TSV\ndata = np.array([[1, 2.5, 3.7], [4, 5.1, 6.8], [7, 8.3, 9.0]])\nnp.savetxt(tmp / \'data.csv\', data, delimiter=\',\', fmt=\'%.2f\',\n           header=\'col1,col2,col3\', comments=\'\')\n\n# Read it back\nloaded = np.genfromtxt(tmp / \'data.csv\', delimiter=\',\', skip_header=1)\nprint(\"Loaded from CSV:\\n\", loaded)\n\n# genfromtxt with mixed data and missing values\ncsv_content = \'\'\'id,temp,humidity,status\n1,22.5,65.0,OK\n2,nan,72.0,OK\n3,19.8,,WARN\n4,25.1,80.5,OK\'\'\'\n\n(tmp / \'sensors.csv\').write_text(csv_content)\nsensors = np.genfromtxt(\n    tmp / \'sensors.csv\',\n    delimiter=\',\',\n    names=True,         # use header row as field names\n    dtype=None,         # auto-detect dtypes\n    encoding=\'utf-8\',\n    filling_values=np.nan  # fill missing with nan\n)\nprint(\"dtype:\", sensors.dtype)\nprint(\"temps:\", sensors[\'temp\'])\nprint(\"humidity:\", sensors[\'humidity\'])\n\nimport shutil; shutil.rmtree(tmp)"},
        {"label": "Memory-mapped arrays (np.memmap)", "code": "import numpy as np\nimport tempfile, pathlib\n\ntmp = pathlib.Path(tempfile.mkdtemp())\nfpath = tmp / \'large_array.dat\'\n\n# Create a memory-mapped array (simulating large data)\nshape = (1000, 500)\n# \'w+\' = write+read, \'r+\' = read+write existing, \'r\' = read-only\nmm_write = np.memmap(fpath, dtype=\'float32\', mode=\'w+\', shape=shape)\n\n# Fill with data (only the modified pages are loaded into RAM)\nmm_write[:100, :] = np.random.randn(100, 500).astype(\'float32\')\nmm_write.flush()  # ensure data is written to disk\ndel mm_write\n\n# Read back without loading everything into memory\nmm_read = np.memmap(fpath, dtype=\'float32\', mode=\'r\', shape=shape)\nprint(f\"Array shape: {mm_read.shape}, dtype: {mm_read.dtype}\")\nprint(f\"First row (first 5): {mm_read[0, :5]}\")\nprint(f\"File size: {fpath.stat().st_size:,} bytes\")\nprint(f\"Expected: {shape[0]*shape[1]*4:,} bytes (float32 = 4 bytes)\")\n\n# Slice a subarray (still memory-mapped, not loaded)\nsub = mm_read[:50, :100]\nprint(f\"Subarray shape: {sub.shape}, mean={sub.mean():.4f}\")\n\ndel mm_read\nimport shutil; shutil.rmtree(tmp)"}
    ],
    "rw": {
        "title": "Model Checkpoint System",
        "scenario": "A deep learning workflow saves model weights and training history to compressed .npz files and reloads them for inference, logging the disk footprint.",
        "code": "import numpy as np, tempfile, pathlib, shutil\n\ntmp = pathlib.Path(tempfile.mkdtemp())\n\n# Simulate model weights for a small neural network\nrng = np.random.default_rng(42)\nweights = {\n    \"W1\": rng.standard_normal((784, 256)).astype(np.float32),\n    \"b1\": np.zeros(256, dtype=np.float32),\n    \"W2\": rng.standard_normal((256, 128)).astype(np.float32),\n    \"b2\": np.zeros(128, dtype=np.float32),\n    \"W3\": rng.standard_normal((128, 10)).astype(np.float32),\n    \"b3\": np.zeros(10, dtype=np.float32),\n}\nhistory = {\n    \"train_loss\": rng.uniform(0.5, 2.0, 50).cumsum() ** 0 * np.linspace(2, 0.2, 50),\n    \"val_loss\":   rng.uniform(0.5, 2.0, 50).cumsum() ** 0 * np.linspace(2.1, 0.25, 50),\n    \"epoch\":      np.arange(50),\n}\n\ndef save_checkpoint(path, weights, history, epoch):\n    np.savez_compressed(path, epoch=epoch, **weights, **history)\n    return path.stat().st_size\n\ndef load_checkpoint(path):\n    data = np.load(path)\n    epoch = int(data[\'epoch\'])\n    W = {k: data[k] for k in [\'W1\',\'b1\',\'W2\',\'b2\',\'W3\',\'b3\']}\n    H = {k: data[k] for k in [\'train_loss\',\'val_loss\',\'epoch\']}\n    return epoch, W, H\n\nckpt_path = tmp / \'checkpoint_ep50.npz\'\nsize = save_checkpoint(ckpt_path, weights, history, epoch=50)\nprint(f\"Checkpoint saved: {size:,} bytes ({size/1024:.1f} KB)\")\n\nep, W, H = load_checkpoint(ckpt_path)\nprint(f\"Loaded epoch {ep}, W1 shape: {W[\'W1\'].shape}\")\nprint(f\"Final train loss: {H[\'train_loss\'][-1]:.4f}\")\n\nshutil.rmtree(tmp)"
    },
    "practice": {
        "title": "Data Pipeline with npz Cache",
        "desc": "Write a DataCache class that saves a numpy array to disk as .npz if it doesn\'t exist, or loads it if it does. Add methods: cache_exists(key), save(key, **arrays), load(key), and delete(key). The cache directory should be configurable in __init__. Test by saving and loading a feature matrix and label array.",
        "starter": "import numpy as np, pathlib\n\nclass DataCache:\n    def __init__(self, cache_dir=\'./cache\'):\n        self.dir = pathlib.Path(cache_dir)\n        self.dir.mkdir(parents=True, exist_ok=True)\n\n    def _path(self, key):\n        return self.dir / f\"{key}.npz\"\n\n    def exists(self, key):\n        return self._path(key).exists()\n\n    def save(self, key, **arrays):\n        np.savez_compressed(self._path(key), **arrays)\n\n    def load(self, key):\n        if not self.exists(key):\n            raise FileNotFoundError(f\"Cache key {key!r} not found\")\n        return dict(np.load(self._path(key)))\n\n    def delete(self, key):\n        p = self._path(key)\n        if p.exists(): p.unlink()\n\nimport tempfile, shutil\ntmp = tempfile.mkdtemp()\ncache = DataCache(tmp)\n\nrng = np.random.default_rng(42)\nX = rng.standard_normal((1000, 20))\ny = rng.integers(0, 5, 1000)\n\ncache.save(\'features\', X=X, y=y)\nprint(\"Exists:\", cache.exists(\'features\'))\n\ndata = cache.load(\'features\')\nprint(\"Loaded X:\", data[\'X\'].shape, \"y:\", data[\'y\'].shape)\nprint(\"Data matches:\", np.allclose(X, data[\'X\']))\n\ncache.delete(\'features\')\nprint(\"After delete:\", cache.exists(\'features\'))\nshutil.rmtree(tmp)\n"
    }
    },

    {
    "title": "24. Datetime64 & Time Arithmetic",
    "desc": "NumPy\'s datetime64 and timedelta64 types enable vectorized date/time arithmetic without Python loops. Essential for time series alignment and resampling.",
    "examples": [
        {"label": "datetime64 basics and arithmetic", "code": "import numpy as np\n\n# Create datetime64 scalars and arrays\nd1 = np.datetime64(\'2024-01-15\')\nd2 = np.datetime64(\'2024-03-20\')\nprint(\"d1:\", d1, \"d2:\", d2)\n\n# Arithmetic\ndelta = d2 - d1\nprint(f\"Delta: {delta}\")               # timedelta64\nprint(f\"Days between: {delta.astype(\'timedelta64[D]\').astype(int)}\")\n\n# Add days\nd3 = d1 + np.timedelta64(30, \'D\')\nprint(f\"30 days after d1: {d3}\")\n\n# Date range\ndates = np.arange(\'2024-01\', \'2025-01\', dtype=\'datetime64[M]\')  # monthly\nprint(\"Monthly dates:\", dates)\nprint(\"Count:\", len(dates))\n\n# Different units\ndt_ns = np.datetime64(\'2024-01-15T09:30:00.000000000\', \'ns\')\ndt_s  = np.datetime64(\'2024-01-15T09:30:00\', \'s\')\nprint(\"Nanosecond precision:\", dt_ns)\nprint(\"Second precision:\", dt_s)\n\n# Year, month, day extraction via astype\nday_arr  = np.arange(\'2024-01-01\', \'2024-02-01\', dtype=\'datetime64[D]\')\nmonths   = day_arr.astype(\'datetime64[M]\').astype(int) % 12 + 1\ndom      = (day_arr - day_arr.astype(\'datetime64[M]\')).astype(int) + 1\nprint(\"Days of month:\", dom[:7])"},
        {"label": "Business day operations and calendar", "code": "import numpy as np\n\n# busdaycalendar: define which days are business days\n# Default: Mon-Fri, no holidays\nbdc = np.busdaycalendar()\n\n# busday_count: count business days between dates\nstart = np.datetime64(\'2024-01-01\')\nend   = np.datetime64(\'2024-12-31\')\nn_bdays = np.busday_count(start, end)\nprint(f\"Business days in 2024: {n_bdays}\")\n\n# is_busday: check if date is a business day\ndates = np.arange(\'2024-01-01\', \'2024-01-08\', dtype=\'datetime64[D]\')\nfor d in dates:\n    bd = np.is_busday(d)\n    print(f\"  {d} ({[\'Mon\',\'Tue\',\'Wed\',\'Thu\',\'Fri\',\'Sat\',\'Sun\'][(d.astype(\'datetime64[D]\').astype(int))%7]}): {\'Business\' if bd else \'Weekend\'}\")\n\n# offset_busdays: advance by N business days\nt_plus_5bd = np.busday_offset(\'2024-01-15\', 5, roll=\'forward\')\nprint(f\"5 business days after Jan 15: {t_plus_5bd}\")\n\n# Custom calendar with holidays\nholidays  = np.array([\'2024-01-01\', \'2024-12-25\'], dtype=\'datetime64[D]\')\nbdc_h = np.busdaycalendar(holidays=holidays)\n# Settlement: T+2 business days (like equity markets)\ntrade_dates = np.array([\'2024-01-03\', \'2024-12-24\', \'2024-12-26\'], dtype=\'datetime64\')\nsettlement  = np.busday_offset(trade_dates, 2, busdaycal=bdc_h)\nfor t, s in zip(trade_dates, settlement):\n    print(f\"  Trade {t} -> Settle {s}\")"},
        {"label": "Time series alignment and resampling", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Generate irregular timestamps (like real tick data)\nn = 200\nbase  = np.datetime64(\'2024-01-15T09:30:00\', \'s\')\ngaps  = rng.integers(1, 60, n).astype(\'timedelta64[s]\')   # 1-60 sec gaps\ntimes = base + np.cumsum(gaps)\n\nprices = 100 + np.cumsum(rng.normal(0, 0.05, n))\n\nprint(f\"First timestamp: {times[0]}\")\nprint(f\"Last timestamp:  {times[-1]}\")\nprint(f\"Total duration: {(times[-1] - times[0]).astype(int)} seconds\")\n\n# Bin into 1-minute buckets (OHLCV)\nminute_start = times.astype(\'datetime64[m]\')\nunique_mins  = np.unique(minute_start)\n\nprint(f\"Number of 1-minute bars: {len(unique_mins)}\")\n\n# OHLCV for each minute\nfor m in unique_mins[:3]:\n    mask = (minute_start == m)\n    bar_prices = prices[mask]\n    print(f\"  {m}: O={bar_prices[0]:.2f} H={bar_prices.max():.2f} \"\n          f\"L={bar_prices.min():.2f} C={bar_prices[-1]:.2f} V={mask.sum()}\")\n\n# Time-based filtering\nmorning = (times >= np.datetime64(\'2024-01-15T09:30:00\', \'s\')) & \\\n          (times <  np.datetime64(\'2024-01-15T10:00:00\', \'s\'))\nprint(f\"Ticks in first 30 min: {morning.sum()}\")"}
    ],
    "rw": {
        "title": "Market Hours Filter",
        "scenario": "A trading system filters raw tick data to keep only regular market hours (9:30-16:00 ET), exclude weekends and holidays, and compute daily OHLCV bars.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Simulate a week of irregular tick data\ndays = np.arange(\'2024-01-08\', \'2024-01-13\', dtype=\'datetime64[D]\')  # Mon-Fri\nall_times, all_prices = [], []\nprice = 100.0\nfor day in days:\n    open_ns  = day.astype(\'datetime64[s]\') + np.timedelta64(9*3600+30*60, \'s\')\n    close_ns = day.astype(\'datetime64[s]\') + np.timedelta64(16*3600, \'s\')\n    n_ticks  = rng.integers(50, 150)\n    t_offsets = rng.integers(0, int((close_ns - open_ns).astype(int)), n_ticks)\n    t_offsets.sort()\n    tick_times = open_ns + t_offsets.astype(\'timedelta64[s]\')\n    rets = rng.normal(0, 0.01, n_ticks)\n    tick_prices = price * np.exp(np.cumsum(rets))\n    price = tick_prices[-1]\n    all_times.extend(tick_times.tolist())\n    all_prices.extend(tick_prices.tolist())\n\ntimes  = np.array(all_times, dtype=\'datetime64[s]\')\nprices = np.array(all_prices)\n\n# OHLCV per day\nprint(\"Daily OHLCV:\")\nday_buckets = times.astype(\'datetime64[D]\')\nfor day in np.unique(day_buckets):\n    m = (day_buckets == day)\n    p = prices[m]\n    print(f\"  {day}: O={p[0]:.2f} H={p.max():.2f} L={p.min():.2f} C={p[-1]:.2f} V={m.sum()}\")"
    },
    "practice": {
        "title": "Holiday Calendar",
        "desc": "Write a function get_trading_days(start, end, holidays) that returns all business days between start and end (as datetime64 strings) excluding the given holidays. Write next_trading_day(date, holidays) that returns the next business day on or after date. Test with US holidays from 2024.",
        "starter": "import numpy as np\n\ndef get_trading_days(start, end, holidays=None):\n    start = np.datetime64(start, \'D\')\n    end   = np.datetime64(end, \'D\')\n    hols  = np.array(holidays or [], dtype=\'datetime64[D]\')\n    bdc   = np.busdaycalendar(holidays=hols)\n    # Generate all calendar days, filter to business days\n    all_days = np.arange(start, end, dtype=\'datetime64[D]\')\n    return all_days[np.is_busday(all_days, busdaycal=bdc)]\n\ndef next_trading_day(date, holidays=None):\n    date = np.datetime64(date, \'D\')\n    hols = np.array(holidays or [], dtype=\'datetime64[D]\')\n    bdc  = np.busdaycalendar(holidays=hols)\n    return np.busday_offset(date, 0, roll=\'forward\', busdaycal=bdc)\n\nus_holidays_2024 = [\n    \'2024-01-01\', \'2024-01-15\', \'2024-02-19\',\n    \'2024-05-27\', \'2024-07-04\', \'2024-09-02\',\n    \'2024-11-28\', \'2024-12-25\'\n]\ntrading_days = get_trading_days(\'2024-01-01\', \'2024-04-01\', us_holidays_2024)\nprint(f\"Trading days in Q1 2024: {len(trading_days)}\")\nprint(\"First 5:\", trading_days[:5])\nprint(\"Last 3: \", trading_days[-3:])\n\nprint(\"Next trading day after 2024-12-24:\", next_trading_day(\'2024-12-24\', us_holidays_2024))\n"
    }
    },

    {
    "title": "25. Meshgrid & Grid Operations",
    "desc": "np.meshgrid, np.ogrid, and np.mgrid create coordinate grids for evaluating functions over 2D/3D spaces — essential for plotting, distance fields, and convolutions.",
    "examples": [
        {"label": "np.meshgrid for 2D function evaluation", "code": "import numpy as np\n\n# meshgrid creates coordinate matrices\nx = np.linspace(-2, 2, 5)\ny = np.linspace(-1, 1, 4)\nX, Y = np.meshgrid(x, y)\n\nprint(\"x:\", x)\nprint(\"y:\", y)\nprint(\"X shape:\", X.shape, \"  Y shape:\", Y.shape)\nprint(\"X:\\n\", X)\nprint(\"Y:\\n\", Y)\n\n# Evaluate a 2D function over the grid\nZ = np.sin(X) * np.exp(-Y**2)\nprint(\"Z shape:\", Z.shape)\nprint(\"Z max:\", Z.max().round(4))\n\n# Find point closest to (1.0, 0.5)\ntarget_x, target_y = 1.0, 0.5\ndist = np.sqrt((X - target_x)**2 + (Y - target_y)**2)\niy, ix = np.unravel_index(dist.argmin(), dist.shape)\nprint(f\"Closest grid point to ({target_x}, {target_y}): ({X[iy,ix]:.1f}, {Y[iy,ix]:.1f})\")\n\n# \'ij\' indexing (matrix-style, transposed from default)\nX_ij, Y_ij = np.meshgrid(x, y, indexing=\'ij\')\nprint(\"With indexing=\'ij\': X shape:\", X_ij.shape)"},
        {"label": "ogrid and mgrid for memory-efficient grids", "code": "import numpy as np\n\n# ogrid: open grid — returns 1D arrays that broadcast\noy, ox = np.ogrid[-3:3:7j, -3:3:7j]   # 7 points from -3 to 3\nprint(\"ogrid ox shape:\", ox.shape, \" oy shape:\", oy.shape)  # (1,7) and (7,1)\n\n# Broadcasting creates the 2D result without full grid in memory\nZ = ox**2 + oy**2  # broadcasts to (7,7)\nprint(\"Z shape:\", Z.shape)\nprint(\"Radial distance from origin:\\n\", np.sqrt(Z).round(2))\n\n# mgrid: closed grid — returns full arrays\ny_grid, x_grid = np.mgrid[0:4, 0:5]  # like meshgrid but shorter syntax\nprint(\"mgrid shapes:\", x_grid.shape, y_grid.shape)\nprint(\"x_grid:\\n\", x_grid)\n\n# Useful: create coordinate pairs for all pixels\nH, W = 8, 8\nrows, cols = np.mgrid[0:H, 0:W]\ncenter = np.array([H/2, W/2])\ndist_from_center = np.sqrt((rows - center[0])**2 + (cols - center[1])**2)\ncircle_mask = dist_from_center <= 3\nprint(f\"Pixels within radius 3 of center: {circle_mask.sum()}\")\n\n# All coordinate pairs as (N, 2) array\ncoords = np.column_stack([rows.ravel(), cols.ravel()])\nprint(f\"All {H}x{W} pixel coordinates shape: {coords.shape}\")"},
        {"label": "Distance fields and spatial operations", "code": "import numpy as np\n\n# Create a distance field from a set of source points\nH, W = 20, 20\nrows, cols = np.mgrid[0:H, 0:W]\n\nsource_points = np.array([[3, 3], [10, 15], [17, 5]])\n\n# Distance to nearest source point\ndist_field = np.full((H, W), np.inf)\nfor pt in source_points:\n    d = np.sqrt((rows - pt[0])**2 + (cols - pt[1])**2)\n    dist_field = np.minimum(dist_field, d)\n\nprint(f\"Distance field shape: {dist_field.shape}\")\nprint(f\"Max distance: {dist_field.max():.2f}\")\nprint(f\"Pixels within 5 units of any source: {(dist_field <= 5).sum()}\")\n\n# Voronoi diagram: which source is closest to each pixel?\nlabels = np.zeros((H, W), dtype=int)\nfor k, pt in enumerate(source_points):\n    d = np.sqrt((rows - pt[0])**2 + (cols - pt[1])**2)\n    mask = d < dist_field  # strictly closer than current min\n    labels[mask] = k\n    dist_field = np.minimum(dist_field, d)\n\nfor k in range(len(source_points)):\n    print(f\"Region {k}: {(labels == k).sum()} pixels\")\n\n# Gaussian RBF kernel centered at each source\nsigma = 3.0\nrbf = sum(np.exp(-(((rows-pt[0])**2+(cols-pt[1])**2)/(2*sigma**2)))\n          for pt in source_points)\nprint(f\"RBF max: {rbf.max():.3f}, sum: {rbf.sum():.1f}\")"}
    ],
    "rw": {
        "title": "Heat Map Generator",
        "scenario": "A geographic data team generates a density heat map from GPS coordinates by evaluating a Gaussian kernel density estimate over a grid covering the study area.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n# Simulate GPS points (lat/lon in some area)\nn_points = 500\nlat = rng.normal(40.7, 0.05, n_points)   # NYC-like\nlon = rng.normal(-74.0, 0.08, n_points)\n\n# Create grid\nlat_grid, lon_grid = np.mgrid[\n    lat.min()-0.02 : lat.max()+0.02 : 50j,\n    lon.min()-0.02 : lon.max()+0.02 : 60j\n]\n\n# Gaussian KDE\ndef kde_density(lat_g, lon_g, lat_pts, lon_pts, bw=0.01):\n    density = np.zeros_like(lat_g)\n    for la, lo in zip(lat_pts, lon_pts):\n        d2 = (lat_g - la)**2 + (lon_g - lo)**2\n        density += np.exp(-d2 / (2 * bw**2))\n    return density / (len(lat_pts) * 2 * np.pi * bw**2)\n\ndensity = kde_density(lat_grid, lon_grid, lat, lon)\nprint(f\"Grid shape: {density.shape}\")\nprint(f\"Density range: [{density.min():.4f}, {density.max():.4f}]\")\nprint(f\"Peak density at: lat={lat_grid.ravel()[density.argmax()]:.4f}, \"\n      f\"lon={lon_grid.ravel()[density.argmax()]:.4f}\")\n\n# Hot spots: top 10% density cells\nthreshold = np.percentile(density, 90)\nhot_spots  = density > threshold\nprint(f\"Hot spot cells: {hot_spots.sum()} ({hot_spots.mean():.1%} of grid)\")"
    },
    "practice": {
        "title": "Bivariate Gaussian",
        "desc": "Write a function bivariate_gaussian(X, Y, mu_x, mu_y, sigma_x, sigma_y, rho) that evaluates the bivariate normal PDF at grid points (X, Y). Parameters: mu = means, sigma = std devs, rho = correlation. Use meshgrid to create a 50x50 grid over [-3, 3] x [-3, 3] and plot (print stats). Verify the PDF integrates to ~1.",
        "starter": "import numpy as np\n\ndef bivariate_gaussian(X, Y, mu_x=0, mu_y=0, sigma_x=1, sigma_y=1, rho=0):\n    z = ((X - mu_x)**2 / sigma_x**2\n         - 2*rho*(X - mu_x)*(Y - mu_y) / (sigma_x*sigma_y)\n         + (Y - mu_y)**2 / sigma_y**2)\n    coeff = 1 / (2 * np.pi * sigma_x * sigma_y * np.sqrt(1 - rho**2))\n    return coeff * np.exp(-z / (2 * (1 - rho**2)))\n\nx = np.linspace(-3, 3, 50)\ny = np.linspace(-3, 3, 50)\nX, Y = np.meshgrid(x, y)\ndx = x[1] - x[0]\ndy = y[1] - y[0]\n\n# Standard normal (rho=0)\nZ1 = bivariate_gaussian(X, Y)\nprint(f\"Standard: max={Z1.max():.4f}, integral={Z1.sum()*dx*dy:.4f}\")\n\n# Correlated (rho=0.7)\nZ2 = bivariate_gaussian(X, Y, mu_x=0.5, mu_y=-0.5, sigma_x=1.2, sigma_y=0.8, rho=0.7)\nprint(f\"Correlated: max={Z2.max():.4f}, integral={Z2.sum()*dx*dy:.4f}\")\nprint(f\"Peak at: ({X.ravel()[Z2.argmax()]:.2f}, {Y.ravel()[Z2.argmax()]:.2f})\")\n"
    }
    },

    {
    "title": "26. Advanced Broadcasting & Pairwise Operations",
    "desc": "Broadcasting rules let NumPy operate on arrays of different shapes without copying data. Master broadcasting for pairwise distances, outer products, and vectorized scoring.",
    "examples": [
        {"label": "Broadcasting rules and shape alignment", "code": "import numpy as np\n\n# Broadcasting rule: align shapes from the right,\n# size-1 dimensions are stretched to match\n\n# Example 1: add row vector to each row of a matrix\nm = np.ones((4, 3))\nv = np.array([10, 20, 30])         # shape (3,)\nprint(\"m + v:\", m + v)             # (4,3) + (3,) -> (4,3)\n\n# Example 2: add column vector to each column\ncol = np.array([[1], [2], [3], [4]])   # shape (4, 1)\nprint(\"m + col:\\n\", m + col)          # (4,3) + (4,1) -> (4,3)\n\n# Example 3: outer product via broadcasting\na = np.array([1, 2, 3])     # shape (3,)\nb = np.array([10, 20])      # shape (2,)\nouter = a[:, np.newaxis] * b[np.newaxis, :]  # (3,1) * (1,2) -> (3,2)\nprint(\"Outer product:\\n\", outer)\nprint(\"Same as np.outer:\", np.array_equal(outer, np.outer(a, b)))\n\n# Shape check\nshapes = [(3, 4, 5), (4, 5), (5,), (1,)]\nbase = np.zeros((3, 4, 5))\nfor s in shapes:\n    arr = np.ones(s)\n    print(f\"(3,4,5) + {s} = {(base + arr).shape}\")"},
        {"label": "Pairwise distances (no loops)", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Euclidean distance matrix: D[i,j] = dist(A[i], B[j])\ndef pairwise_euclidean(A, B):\n    # A: (m, d), B: (n, d) -> (m, n)\n    # ||a - b||^2 = ||a||^2 + ||b||^2 - 2 a.b\n    sq_A = (A**2).sum(axis=1, keepdims=True)  # (m, 1)\n    sq_B = (B**2).sum(axis=1, keepdims=True)  # (n, 1)\n    dot  = A @ B.T                            # (m, n)\n    return np.sqrt(np.maximum(sq_A + sq_B.T - 2*dot, 0))\n\nA = rng.standard_normal((50, 3))   # 50 query points\nB = rng.standard_normal((100, 3))  # 100 database points\n\nD = pairwise_euclidean(A, B)\nprint(f\"Distance matrix: {D.shape}\")\nprint(f\"Min dist: {D.min():.3f}, Max dist: {D.max():.3f}\")\n\n# Nearest neighbor for each query\nnn_idx = D.argmin(axis=1)\nnn_dist = D.min(axis=1)\nprint(f\"Query 0: nearest is B[{nn_idx[0]}] at distance {nn_dist[0]:.3f}\")\n\n# k-NN: top-k closest\nk = 3\nknn_idx = np.argpartition(D, k, axis=1)[:, :k]\nprint(f\"3-NN indices for query 0: {knn_idx[0]}\")\n\n# Cosine similarity matrix\ndef cosine_sim(A, B):\n    A_norm = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-9)\n    B_norm = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-9)\n    return A_norm @ B_norm.T\n\nC = cosine_sim(A, B)\nprint(f\"Cosine sim range: [{C.min():.3f}, {C.max():.3f}]\")"},
        {"label": "Vectorized scoring and ranking", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Multi-criteria scoring: score[i,j] = dot(weights, features[i,j])\n# items: (N, F) features, weights: (F,) -> scores: (N,)\nn_items, n_features = 1000, 10\nfeatures = rng.uniform(0, 1, (n_items, n_features))\nweights  = np.array([0.3, 0.2, 0.15, 0.1, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01])\n\nscores = features @ weights   # (N,F) @ (F,) -> (N,)\nprint(f\"Scores shape: {scores.shape}, range: [{scores.min():.3f}, {scores.max():.3f}]\")\n\n# Rank items (descending score)\nranks = np.argsort(scores)[::-1]\nprint(\"Top 5 items:\", ranks[:5], \"scores:\", scores[ranks[:5]].round(3))\n\n# Broadcasting for threshold matrix: flag (user, item) pairs\nn_users = 20\nuser_thresholds = rng.uniform(0.4, 0.7, n_users)     # (20,)\n# recommended[i,j] = True if scores[j] >= thresholds[i]\nrecommended = scores[np.newaxis, :] >= user_thresholds[:, np.newaxis]  # (20, 1000)\nprint(f\"Recommendation matrix: {recommended.shape}\")\nprint(f\"Avg recommendations per user: {recommended.sum(axis=1).mean():.1f}\")\n\n# Pairwise similarity between items (feature dot products)\nitem_sim = features @ features.T  # (N, N)\nprint(f\"Item similarity matrix: {item_sim.shape}\")\nprint(f\"Self-similarity range: [{np.diag(item_sim).min():.3f}, {np.diag(item_sim).max():.3f}]\")"}
    ],
    "rw": {
        "title": "Embedding Search Engine",
        "scenario": "A semantic search system finds the top-5 most similar documents to a query by computing cosine similarity between query embedding and 50,000 document embeddings using broadcasting.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Simulate document embeddings and a query\nn_docs, dim = 50_000, 128\ndocs  = rng.standard_normal((n_docs, dim))\ndocs /= np.linalg.norm(docs, axis=1, keepdims=True)  # L2 normalize\n\nquery = rng.standard_normal(dim)\nquery /= np.linalg.norm(query)\n\n# Cosine similarity: since both normalized, just dot product\nsims = docs @ query   # (50000,)\n\n# Top-5 results\ntop5_idx = np.argpartition(sims, -5)[-5:]\ntop5_idx = top5_idx[np.argsort(sims[top5_idx])[::-1]]\n\nprint(\"Top 5 similar documents:\")\nfor rank, idx in enumerate(top5_idx, 1):\n    print(f\"  Rank {rank}: doc_id={idx:5d}, similarity={sims[idx]:.4f}\")\n\n# Retrieval metrics: how many docs above threshold?\nthreshold = 0.1\nn_relevant = (sims >= threshold).sum()\nprint(f\"Docs with similarity >= {threshold}: {n_relevant} ({n_relevant/n_docs:.2%})\")\n\n# Batch queries\nn_queries = 100\nqueries = rng.standard_normal((n_queries, dim))\nqueries /= np.linalg.norm(queries, axis=1, keepdims=True)\nbatch_sims = queries @ docs.T   # (100, 50000)\nbatch_top1 = batch_sims.argmax(axis=1)\nprint(f\"Batch top-1 for {n_queries} queries: mean sim={batch_sims.max(axis=1).mean():.4f}\")"
    },
    "practice": {
        "title": "Attention Scores",
        "desc": "Implement scaled_dot_product_attention(Q, K, V) where Q, K have shape (seq_len, d_k) and V has shape (seq_len, d_v). Compute scores = softmax(Q @ K.T / sqrt(d_k)) @ V using only NumPy. Also implement multi_head_attention(Q, K, V, n_heads) that splits into n_heads, applies attention, and concatenates.",
        "starter": "import numpy as np\n\ndef softmax(x, axis=-1):\n    e = np.exp(x - x.max(axis=axis, keepdims=True))\n    return e / e.sum(axis=axis, keepdims=True)\n\ndef scaled_dot_product_attention(Q, K, V):\n    # Q: (seq, d_k), K: (seq, d_k), V: (seq, d_v)\n    d_k = Q.shape[-1]\n    # TODO: scores = softmax(Q @ K.T / sqrt(d_k))\n    # TODO: return scores @ V\n    pass\n\ndef multi_head_attention(Q, K, V, n_heads):\n    seq, d = Q.shape\n    d_k = d // n_heads\n    heads = []\n    for h in range(n_heads):\n        # TODO: slice Q[:,h*d_k:(h+1)*d_k], K, V similarly\n        # TODO: apply scaled_dot_product_attention, collect output\n        pass\n    # TODO: concatenate heads along last axis\n    pass\n\nrng = np.random.default_rng(42)\nseq, d = 10, 64\nQ = rng.standard_normal((seq, d))\nK = rng.standard_normal((seq, d))\nV = rng.standard_normal((seq, d))\n\nout1 = scaled_dot_product_attention(Q, K, V)\nprint(\"Single-head output shape:\", out1.shape)  # (10, 64)\n\nout2 = multi_head_attention(Q, K, V, n_heads=8)\nprint(\"Multi-head output shape:\", out2.shape)   # (10, 64)\n"
    }
    },

    {
    "title": "27. Universal Functions (ufuncs) in Depth",
    "desc": "Ufuncs are vectorized functions that operate element-wise on arrays. They support reduce, accumulate, outer, and reduceat — and you can create custom ufuncs with np.frompyfunc or Numba.",
    "examples": [
        {"label": "Built-in ufunc methods: reduce, accumulate, outer", "code": "import numpy as np\n\narr = np.array([1, 2, 3, 4, 5])\n\n# reduce: apply ufunc repeatedly to reduce array\nprint(\"np.add.reduce:\", np.add.reduce(arr))         # 15 (sum)\nprint(\"np.multiply.reduce:\", np.multiply.reduce(arr))  # 120 (product)\nprint(\"np.maximum.reduce:\", np.maximum.reduce(arr))  # 5\n\n# accumulate: like reduce but keeps intermediate results\nprint(\"np.add.accumulate:\", np.add.accumulate(arr))        # cumsum\nprint(\"np.multiply.accumulate:\", np.multiply.accumulate(arr))  # cumprod\nprint(\"np.maximum.accumulate:\", np.maximum.accumulate(arr))\n\n# outer: compute all pairs\na = np.array([1, 2, 3])\nb = np.array([10, 20, 30])\nprint(\"np.add.outer:\\n\", np.add.outer(a, b))\nprint(\"np.multiply.outer:\\n\", np.multiply.outer(a, b))\n\n# 2D reduce along axis\nm = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])\nprint(\"Row sums:\", np.add.reduce(m, axis=1))       # [6, 15, 24]\nprint(\"Col products:\", np.multiply.reduce(m, axis=0))  # [28, 80, 162]\n\n# reduceat: reduce in segments\ndata = np.arange(10)\n# Reduce segments: [0:3], [3:6], [6:10]\nresult = np.add.reduceat(data, [0, 3, 6])\nprint(\"Segment sums:\", result)   # [0+1+2, 3+4+5, 6+7+8+9]"},
        {"label": "Creating custom ufuncs", "code": "import numpy as np\n\n# np.frompyfunc: wrap a Python function as a ufunc\ndef clip_and_scale(x, lo=0, hi=1):\n    return min(max(x, lo), hi) * 100\n\n# frompyfunc returns object dtype by default\nufunc_cas = np.frompyfunc(lambda x: clip_and_scale(x), 1, 1)\ndata = np.array([-0.5, 0.0, 0.3, 0.7, 1.0, 1.5])\nprint(\"clip_and_scale:\", ufunc_cas(data).astype(float))\n\n# vectorize: more user-friendly, supports output dtype\nclip_pct = np.vectorize(clip_and_scale, otypes=[float])\nprint(\"vectorize:\", clip_pct(data))\n\n# Common ufuncs catalogue\nx = np.linspace(0.1, 2.0, 5)\nprint(\"exp:\", np.exp(x).round(3))\nprint(\"log:\", np.log(x).round(3))\nprint(\"log2:\", np.log2(x).round(3))\nprint(\"log10:\", np.log10(x).round(3))\nprint(\"sqrt:\", np.sqrt(x).round(3))\nprint(\"cbrt:\", np.cbrt(x).round(3))\n\n# Trigonometric\nangles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])\nprint(\"sin:\", np.sin(angles).round(3))\nprint(\"arcsin:\", np.arcsin(np.sin(angles)).round(3))"},
        {"label": "Ufunc performance and where argument", "code": "import numpy as np\nimport timeit\n\n# where argument: apply ufunc only to selected elements\nrng = np.random.default_rng(42)\ndata = rng.uniform(-5, 5, 1_000_000)\n\n# np.sqrt only where data > 0, else keep 0\nresult = np.zeros_like(data)\nnp.sqrt(data, out=result, where=data > 0)\nprint(f\"sqrt(data) where > 0: {result[:5].round(3)}\")\n\n# np.log1p (log(1+x)) is more numerically stable for small x\nsmall = np.array([1e-10, 1e-5, 0.001, 0.01, 0.1])\nprint(\"log(1+x):  \", np.log(1 + small))\nprint(\"log1p(x):  \", np.log1p(small))\n\n# Ufunc with out argument (in-place, avoids allocation)\na = np.random.rand(1_000_000)\nb = np.empty_like(a)\n\nt1 = timeit.timeit(lambda: np.exp(a), number=10)\nt2 = timeit.timeit(lambda: np.exp(a, out=b), number=10)\nprint(f\"exp(a) without out: {t1:.3f}s\")\nprint(f\"exp(a, out=b):      {t2:.3f}s\")\n\n# at: unbuffered in-place operation (useful for scatter operations)\narr = np.zeros(5)\nindices = np.array([0, 1, 0, 2, 1])\nvalues  = np.array([1.0, 2.0, 3.0, 4.0, 5.0])\nnp.add.at(arr, indices, values)\nprint(\"add.at result:\", arr)  # handles duplicate indices correctly"}
    ],
    "rw": {
        "title": "Vectorized Activation Functions",
        "scenario": "A neural network training loop applies activation functions to millions of neurons — using ufuncs with out= buffers halves memory allocation overhead.",
        "code": "import numpy as np\n\n# Pre-allocated buffers\nrng  = np.random.default_rng(42)\nN    = 1_000_000\nx    = rng.standard_normal(N).astype(np.float32)\nbuf  = np.empty_like(x)\n\ndef relu(x, out=None):\n    return np.maximum(x, 0, out=out)\n\ndef sigmoid(x, out=None):\n    out = np.empty_like(x) if out is None else out\n    np.negative(x, out=out)\n    np.exp(out, out=out)\n    out += 1\n    np.reciprocal(out, out=out)\n    return out\n\ndef gelu(x, out=None):\n    # Approximate GELU: x * sigmoid(1.702 * x)\n    s = sigmoid(1.702 * x)\n    return np.multiply(x, s, out=out)\n\ndef swish(x, out=None):\n    return np.multiply(x, sigmoid(x), out=out)\n\n# Compute and compare\nactivations = {\n    \"ReLU\":    relu(x, buf.copy()),\n    \"Sigmoid\": sigmoid(x, buf.copy()),\n    \"GELU\":    gelu(x, buf.copy()),\n    \"Swish\":   swish(x, buf.copy()),\n}\n\nfor name, act in activations.items():\n    print(f\"{name:8s}: mean={act.mean():.4f}, std={act.std():.4f}, \"\n          f\"range=[{act.min():.3f}, {act.max():.3f}]\")"
    },
    "practice": {
        "title": "Custom Ufunc",
        "desc": "Use np.frompyfunc to create a ufunc haversine_ufunc that computes the great-circle distance in km between a (lat1, lon1) and (lat2, lon2) point pair. Then use vectorize to wrap it into a function that accepts arrays of lat/lon pairs. Compute distances between New York and a grid of 100 cities.",
        "starter": "import numpy as np\n\ndef haversine_scalar(lat1, lon1, lat2, lon2):\n    R = 6371  # Earth radius in km\n    dlat = np.radians(lat2 - lat1)\n    dlon = np.radians(lon2 - lon1)\n    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2\n    return 2 * R * np.arcsin(np.sqrt(a))\n\n# Vectorize to work on arrays\nhaversine = np.vectorize(haversine_scalar, otypes=[float])\n\n# New York City\nny_lat, ny_lon = 40.7128, -74.0060\n\nrng = np.random.default_rng(42)\nn_cities = 100\ncity_lats = rng.uniform(-60, 70, n_cities)\ncity_lons = rng.uniform(-180, 180, n_cities)\n\ndistances = haversine(ny_lat, ny_lon, city_lats, city_lons)\nprint(f\"Distances computed: {len(distances)}\")\nprint(f\"Nearest city: {distances.min():.0f} km\")\nprint(f\"Farthest city: {distances.max():.0f} km\")\nprint(f\"Average distance from NYC: {distances.mean():.0f} km\")\n"
    }
    },

    {
    "title": "28. Masked Arrays (np.ma)",
    "desc": "np.ma.MaskedArray transparently handles missing data by maintaining a boolean mask alongside values. Useful for sensor data with gaps or any dataset with invalid entries.",
    "examples": [
        {"label": "Creating and using masked arrays", "code": "import numpy as np\n\n# Create masked array\ndata = np.array([1.0, 2.0, -999.0, 4.0, -999.0, 6.0])\nmask = data == -999.0\n\nma = np.ma.array(data, mask=mask)\nprint(\"Data:  \", ma)\nprint(\"Mask:  \", ma.mask)\nprint(\"Filled:\", ma.filled(fill_value=0))\n\n# Operations automatically skip masked values\nprint(\"Mean (excludes masked):\", ma.mean())   # (1+2+4+6)/4 = 3.25\nprint(\"Sum:\", ma.sum())                        # 13\nprint(\"Std:\", ma.std().round(4))\n\n# np.ma.masked_where\narr = np.array([10, 25, -5, 0, 8, -1, 15])\nma2 = np.ma.masked_where(arr <= 0, arr)\nprint(\"Masked non-positive:\", ma2)\nprint(\"Log (safe):\", np.log(ma2))   # no error for masked values\n\n# np.ma.masked_invalid: auto-mask NaN and Inf\ndirty = np.array([1.0, np.nan, 3.0, np.inf, 5.0, -np.inf])\nclean = np.ma.masked_invalid(dirty)\nprint(\"Masked invalid:\", clean)\nprint(\"Safe mean:\", clean.mean())"},
        {"label": "Masked array operations and conversions", "code": "import numpy as np\n\n# 2D masked array\ntemps = np.array([[15.2, 16.1, -999, 18.5],\n                  [-999, 14.8, 15.9, 16.7],\n                  [13.1, -999, -999, 15.3]])\nm = np.ma.masked_equal(temps, -999)\n\nprint(\"Masked temps:\\n\", m)\nprint(\"Row means (excl. missing):\", m.mean(axis=1))\nprint(\"Col means (excl. missing):\", m.mean(axis=0))\n\n# Fill with column means\ncol_means = m.mean(axis=0)\nfilled = m.filled(fill_value=col_means)  # broadcasts col_means\nprint(\"Filled temps:\\n\", filled.round(1))\n\n# Stacking masked arrays\na = np.ma.array([1, 2, 3, 4], mask=[0, 1, 0, 0])\nb = np.ma.array([5, 6, 7, 8], mask=[0, 0, 1, 0])\nstacked = np.ma.vstack([a, b])\nprint(\"Stacked:\\n\", stacked)\nprint(\"Column min (ignoring masks):\", stacked.min(axis=0))\n\n# Convert to/from regular arrays\narr = m.compressed()         # 1D array of valid values only\nprint(\"Compressed:\", arr)\narr2 = np.ma.filled(m, -1)  # replace mask with -1\nprint(\"Filled(-1):\\n\", arr2)"},
        {"label": "Masked array with statistics and aggregations", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\nN = 1000\n\n# Simulate sensor readings with random dropouts\nraw = rng.normal(20, 3, N)          # temperature readings\ndropout_mask = rng.random(N) < 0.15  # 15% missing\n\nsensor = np.ma.array(raw, mask=dropout_mask)\nprint(f\"Total readings: {N}\")\nprint(f\"Valid readings: {sensor.count()} ({sensor.count()/N:.1%})\")\nprint(f\"Masked readings: {sensor.mask.sum()}\")\n\n# Robust statistics (automatically use only valid data)\nprint(f\"Mean:   {sensor.mean():.3f}\")\nprint(f\"Median: {np.ma.median(sensor):.3f}\")\nprint(f\"Std:    {sensor.std():.3f}\")\nprint(f\"Min:    {sensor.min():.3f}\")\nprint(f\"Max:    {sensor.max():.3f}\")\n\n# Percentiles (need filled for np.percentile)\nfilled_for_pct = sensor.compressed()\nprint(f\"P25/P75: {np.percentile(filled_for_pct, [25,75]).round(2)}\")\n\n# Anomaly detection: flag values > 3 sigma (on top of existing mask)\nmean, std = sensor.mean(), sensor.std()\nanomaly_mask = (sensor < mean - 3*std) | (sensor > mean + 3*std)\nsensor_clean = np.ma.array(sensor.data, mask=sensor.mask | anomaly_mask.filled(False))\nprint(f\"After anomaly removal: {sensor_clean.count()} valid readings\")"}
    ],
    "rw": {
        "title": "Oceanographic Data Cleaner",
        "scenario": "A research station processes 5-year daily ocean temperature data with sensor failures (flagged as -9999) and physical impossibilities (<-2°C or >35°C), using masked arrays to compute clean statistics.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\nn_years = 5\nn_days  = n_years * 365\n\n# Simulate ocean temps with seasonal pattern\nt = np.linspace(0, n_years * 2 * np.pi, n_days)\nbase_temp = 15 + 10 * np.sin(t - np.pi/2)  # seasonal cycle\ntemps = base_temp + rng.normal(0, 1.5, n_days)\n\n# Inject data quality issues\nsensor_fail   = rng.random(n_days) < 0.08    # 8% sensor failures\nphysical_anom = rng.random(n_days) < 0.02    # 2% physical anomalies\ntemps[sensor_fail]   = -9999.0\ntemps[physical_anom] = rng.choice([-5.0, 40.0], physical_anom.sum())\n\n# Build mask: flag everything invalid\nmask = ((temps == -9999.0) |\n        (temps < -2.0) |\n        (temps > 35.0))\nclean = np.ma.array(temps, mask=mask)\n\nprint(f\"Data coverage: {clean.count()/n_days:.1%} valid ({clean.count()} of {n_days} days)\")\nprint(f\"Mean temperature: {clean.mean():.2f}°C\")\nprint(f\"Seasonal range: [{clean.min():.2f}, {clean.max():.2f}]°C\")\n\n# Annual stats (reshape to years x 365)\nannual = clean[:n_years*365].reshape(n_years, 365)\nfor y in range(n_years):\n    row = annual[y]\n    print(f\"  Year {y+1}: mean={row.mean():.2f}°C, valid={row.count()} days\")"
    },
    "practice": {
        "title": "Masked Correlation",
        "desc": "Write masked_corrcoef(X) that computes a pairwise correlation matrix for a 2D masked array X (shape n_obs x n_vars), where each pair of variables is correlated only using rows where BOTH are valid. Return a regular (n_vars x n_vars) ndarray. Test on a dataset where each column has independent random missing values.",
        "starter": "import numpy as np\n\ndef masked_corrcoef(X):\n    n_obs, n_vars = X.shape\n    corr = np.eye(n_vars)\n    for i in range(n_vars):\n        for j in range(i+1, n_vars):\n            # Rows valid for BOTH columns i and j\n            valid = (~X[:, i].mask) & (~X[:, j].mask)\n            if valid.sum() < 2:\n                corr[i, j] = corr[j, i] = np.nan\n                continue\n            xi = X[valid, i].data\n            xj = X[valid, j].data\n            r  = np.corrcoef(xi, xj)[0, 1]\n            corr[i, j] = corr[j, i] = r\n    return corr\n\nrng = np.random.default_rng(42)\nn, p = 200, 4\ndata = rng.standard_normal((n, p))\n# Create correlated structure\ndata[:, 1] = 0.7 * data[:, 0] + 0.3 * rng.standard_normal(n)\n\nmasks = rng.random((n, p)) < 0.2   # 20% missing per column\nX = np.ma.array(data, mask=masks)\n\ncorr = masked_corrcoef(X)\nprint(\"Pairwise correlations (with per-pair valid observations):\")\nprint(corr.round(3))\nprint(\"Expected corr(0,1) ~ 0.7:\", corr[0, 1].round(2))\n"
    }
    },

    {
    "title": "29. Memory Layout, Strides & Contiguity",
    "desc": "NumPy arrays store data in contiguous memory blocks. Understanding C/F order, strides, and views vs copies is critical for performance and interoperability with C/Fortran libraries.",
    "examples": [
        {"label": "C vs Fortran order, flags, and strides", "code": "import numpy as np\n\n# C order (row-major): last axis varies fastest (default)\narr_c = np.array([[1, 2, 3], [4, 5, 6]], order=\'C\')\nprint(\"C order strides:\", arr_c.strides)   # (12, 4) for float32\n\n# F order (column-major): first axis varies fastest\narr_f = np.array([[1, 2, 3], [4, 5, 6]], order=\'F\')\nprint(\"F order strides:\", arr_f.strides)   # (4, 8) for float32\n\n# Check flags\nprint(\"C-contiguous:\", arr_c.flags[\'C_CONTIGUOUS\'])   # True\nprint(\"F-contiguous:\", arr_c.flags[\'F_CONTIGUOUS\'])   # False\n\n# Transpose only changes strides, no data copy\nT = arr_c.T\nprint(\"Transposed strides:\", T.strides)\nprint(\"T is view:\", T.base is arr_c)   # True\n\n# ascontiguousarray: ensure C-contiguous copy\nT_c = np.ascontiguousarray(T)\nprint(\"After ascontiguousarray:\", T_c.flags[\'C_CONTIGUOUS\'])\n\n# Strides as bytes\narr = np.arange(24, dtype=np.float64).reshape(2, 3, 4)\nprint(f\"Shape: {arr.shape}, Strides (bytes): {arr.strides}\")\nprint(f\"Itemsize: {arr.itemsize} bytes\")\n# stride[k] = itemsize * product(shape[k+1:])"},
        {"label": "Views vs copies and memory sharing", "code": "import numpy as np\n\narr = np.arange(20, dtype=float)\n\n# Slice creates a VIEW (shares memory)\nview = arr[2:10:2]   # every 2nd element from 2 to 10\nprint(\"view:\", view)\nprint(\"view.base is arr:\", view.base is arr)\n\nview[0] = 999        # modifies arr!\nprint(\"arr after view[0]=999:\", arr[:12])\n\n# copy() creates an independent copy\narr2 = arr.copy()\narr2[0] = -1\nprint(\"Original arr[0] unchanged:\", arr[0])  # still 999 (from earlier)\n\n# Fancy indexing always copies\nfancy = arr[[0, 3, 7]]\nprint(\"fancy.base:\", fancy.base)   # None = not a view\n\n# reshape: usually a view if data is contiguous\narr3 = np.arange(12)\nreshaped = arr3.reshape(3, 4)\nprint(\"reshape is view:\", reshaped.base is arr3)\nreshaped[0, 0] = -1\nprint(\"arr3[0] changed:\", arr3[0])   # -1\n\n# np.shares_memory: robust check\na = np.arange(10)\nb = a[::2]\nc = a.copy()\nprint(\"a and b share memory:\", np.shares_memory(a, b))   # True\nprint(\"a and c share memory:\", np.shares_memory(a, c))   # False"},
        {"label": "Stride tricks for rolling windows", "code": "import numpy as np\nfrom numpy.lib.stride_tricks import sliding_window_view, as_strided\n\narr = np.arange(10, dtype=float)\n\n# sliding_window_view: safe way to get overlapping windows\nwindows = sliding_window_view(arr, window_shape=4)\nprint(\"Windows shape:\", windows.shape)   # (7, 4)\nprint(\"First 3 windows:\\n\", windows[:3])\n\n# Each window is a VIEW — no data copy!\nwindows[0, 0] = 999\nprint(\"arr[0] changed:\", arr[0])   # yes, 999\n\narr = np.arange(10, dtype=float)  # reset\n\n# 2D rolling windows (for image patches)\nimg = np.arange(16, dtype=float).reshape(4, 4)\npatches = sliding_window_view(img, window_shape=(2, 2))\nprint(\"2D patches shape:\", patches.shape)   # (3, 3, 2, 2)\nprint(\"Patch at [0,0]:\\n\", patches[0, 0])\n\n# as_strided: manual stride tricks (use with care!)\n# Rolling mean via strides\ndef rolling_mean_strided(arr, window):\n    w = sliding_window_view(arr, window)\n    return w.mean(axis=1)\n\nrolling = rolling_mean_strided(np.arange(10, dtype=float), 3)\nprint(\"Rolling mean (window=3):\", rolling)"}
    ],
    "rw": {
        "title": "Cache-Friendly Matrix Multiply",
        "scenario": "A performance-critical simulation avoids unnecessary transpositions and ensures arrays are contiguous before passing to BLAS-backed np.dot, cutting computation time significantly.",
        "code": "import numpy as np, timeit\n\nrng = np.random.default_rng(42)\n\nA = rng.standard_normal((500, 300))\nB = rng.standard_normal((300, 400))\n\n# C-contiguous vs non-contiguous performance\nB_T_F = np.asfortranarray(B.T)       # F-order, non-contiguous for @\nB_T_C = np.ascontiguousarray(B.T)    # C-contiguous copy\n\nprint(\"B.T C-contiguous:\", B.T.flags[\'C_CONTIGUOUS\'])      # False\nprint(\"B_T_C contiguous:\", B_T_C.flags[\'C_CONTIGUOUS\'])    # True\n\n# GEMM: A @ B (B is 300x400 C-contiguous)\nt1 = timeit.timeit(lambda: A @ B, number=100)\nt2 = timeit.timeit(lambda: A @ B_T_F.T, number=100)\nt3 = timeit.timeit(lambda: A @ B_T_C.T, number=100)\n\nprint(f\"A @ B (contiguous):      {t1:.4f}s\")\nprint(f\"A @ B_T_F.T (F-order):   {t2:.4f}s\")\nprint(f\"A @ B_T_C.T (C-order):   {t3:.4f}s\")\n\n# Verify results are the same\nC1 = A @ B\nC2 = A @ B_T_F.T\nprint(\"Results match:\", np.allclose(C1, C2))\n\n# Memory usage check\nimport sys\nprint(f\"B.T.copy() size: {sys.getsizeof(B.T.copy()):,} bytes\")\nprint(f\"B.T view size:   {sys.getsizeof(B.T):,} bytes (metadata only)\")"
    },
    "practice": {
        "title": "Stride Inspector",
        "desc": "Write inspect_array(arr) that prints: shape, dtype, strides, itemsize, nbytes, is_C_contiguous, is_F_contiguous, is_view (arr.base is not None), total elements. Then write reshape_safe(arr, shape) that reshapes arr to shape, ensuring the result is C-contiguous (copy only if needed). Test with various slices and transpositions.",
        "starter": "import numpy as np\n\ndef inspect_array(arr):\n    print(f\"Shape:           {arr.shape}\")\n    print(f\"dtype:           {arr.dtype}\")\n    print(f\"strides (bytes): {arr.strides}\")\n    print(f\"itemsize:        {arr.itemsize}\")\n    print(f\"nbytes:          {arr.nbytes:,}\")\n    print(f\"C-contiguous:    {arr.flags[\'C_CONTIGUOUS\']}\")\n    print(f\"F-contiguous:    {arr.flags[\'F_CONTIGUOUS\']}\")\n    print(f\"Is view:         {arr.base is not None}\")\n    print(f\"N elements:      {arr.size}\")\n\ndef reshape_safe(arr, shape):\n    if not arr.flags[\'C_CONTIGUOUS\']:\n        arr = np.ascontiguousarray(arr)\n    return arr.reshape(shape)\n\nbase = np.arange(24, dtype=np.float32).reshape(4, 6)\nprint(\"=== Base array ===\")\ninspect_array(base)\n\nprint(\"\\n=== Transposed ===\")\nT = base.T\ninspect_array(T)\n\nprint(\"\\n=== Slice (non-contiguous) ===\")\ns = base[::2, ::2]\ninspect_array(s)\n\nprint(\"\\n=== Reshape safe (from transposed) ===\")\nr = reshape_safe(T, (24,))\ninspect_array(r)\n"
    }
    },

    {
    "title": "30. Advanced Linear Algebra Operations",
    "desc": "Beyond basic dot products: matrix decompositions (SVD, QR, Cholesky), determinants, null spaces, pseudo-inverse, and Kronecker products for systems of equations and dimensionality reduction.",
    "examples": [
        {"label": "QR decomposition and least squares", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# QR decomposition: A = Q @ R\nA = rng.standard_normal((6, 4))\nQ, R = np.linalg.qr(A)\nprint(f\"A: {A.shape}, Q: {Q.shape}, R: {R.shape}\")\nprint(\"Q orthonormal:\", np.allclose(Q.T @ Q, np.eye(4)))\nprint(\"A = Q@R:\", np.allclose(A, Q @ R))\n\n# Least squares: solve Ax = b for overdetermined system\nm, n = 100, 5\nA = rng.standard_normal((m, n))\ntrue_x = rng.standard_normal(n)\nb = A @ true_x + rng.normal(0, 0.1, m)   # noisy measurements\n\n# lstsq: minimize ||Ax - b||^2\nx, residuals, rank, sv = np.linalg.lstsq(A, b, rcond=None)\nprint(f\"True x:   {true_x[:3].round(3)}\")\nprint(f\"Solved x: {x[:3].round(3)}\")\nprint(f\"Matrix rank: {rank}, condition number: {sv[0]/sv[-1]:.1f}\")\n\n# Via normal equations (less stable but educational)\nx_normal = np.linalg.solve(A.T @ A, A.T @ b)\nprint(\"Normal eq error:\", np.abs(x - x_normal).max())"},
        {"label": "Cholesky, determinant, and null space", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Cholesky decomposition: A = L @ L.T (for positive definite A)\n# Used for sampling multivariate normal and inverting covariance matrices\nn = 5\nA = rng.standard_normal((n, n))\nS = A.T @ A + n * np.eye(n)  # make it positive definite\n\nL = np.linalg.cholesky(S)\nprint(\"L shape:\", L.shape)\nprint(\"L @ L.T == S:\", np.allclose(L @ L.T, S))\nprint(\"L is lower triangular:\", np.allclose(L, np.tril(L)))\n\n# Sample from multivariate normal using Cholesky\nmu  = np.zeros(n)\ncov = S / S.max()   # scale to reasonable range\nL   = np.linalg.cholesky(cov)\nsamples = mu + rng.standard_normal((1000, n)) @ L.T\nprint(f\"Sample covariance matches target: {np.allclose(np.cov(samples.T), cov, atol=0.1)}\")\n\n# Determinant (log for numerical stability)\nlogdet_sign, logdet = np.linalg.slogdet(S)\nprint(f\"logdet(S): {logdet:.3f}, sign: {logdet_sign}\")\nprint(f\"det(S) = exp({logdet:.1f}) ~ {np.exp(logdet):.2e}\")\n\n# Pseudo-inverse (Moore-Penrose)\nm = np.array([[1, 2], [3, 4], [5, 6]])\npinv = np.linalg.pinv(m)\nprint(\"Pseudo-inverse shape:\", pinv.shape)\nprint(\"m @ pinv @ m == m:\", np.allclose(m @ pinv @ m, m))"},
        {"label": "Eigendecomposition and PCA from scratch", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Eigendecomposition: A v = lambda v\nA = np.array([[4, -2], [1,  1]])\neigenvalues, eigenvectors = np.linalg.eig(A)\nprint(\"Eigenvalues:\", eigenvalues)\nprint(\"Eigenvectors:\\n\", eigenvectors)\n\n# Verify: A @ v = lambda * v\nfor i in range(len(eigenvalues)):\n    v = eigenvectors[:, i]\n    print(f\"  A @ v{i} == {eigenvalues[i]:.1f} * v{i}: {np.allclose(A @ v, eigenvalues[i] * v)}\")\n\n# Symmetric matrix: use eigh (more stable, guaranteed real eigenvalues)\nS = np.array([[3, 1], [1, 3]])\nw, v = np.linalg.eigh(S)\nprint(\"Symmetric eigs:\", w)\n\n# PCA from scratch using SVD\nn, d = 200, 5\nX = rng.standard_normal((n, d))\nX[:, 1] = 0.8 * X[:, 0] + 0.6 * X[:, 1]  # create correlation\n\n# Center data\nX_c = X - X.mean(axis=0)\n\n# SVD of centered data\nU, s, Vt = np.linalg.svd(X_c, full_matrices=False)\nexplained = s**2 / (s**2).sum()\nprint(\"Explained variance ratio:\", explained.round(3))\nprint(\"Cumulative:\", explained.cumsum().round(3))\n\n# Project to 2 components\nX_2d = X_c @ Vt[:2].T\nprint(f\"PCA 2D shape: {X_2d.shape}\")"}
    ],
    "rw": {
        "title": "Recommender via Matrix Factorization",
        "scenario": "A collaborative filtering system factorizes a user-item rating matrix using SVD to find latent factors and predict missing ratings.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\nn_users, n_items, n_factors = 100, 200, 10\n\n# Simulate a low-rank rating matrix (most entries unknown)\nU_true = rng.standard_normal((n_users, n_factors))\nV_true = rng.standard_normal((n_items, n_factors))\nR_true = U_true @ V_true.T + rng.normal(0, 0.5, (n_users, n_items))\nR_true = np.clip(R_true, 1, 5)\n\n# Only observe 20% of ratings\nobserved_mask = rng.random((n_users, n_items)) < 0.2\nR_obs = np.where(observed_mask, R_true, 0.0)\n\n# Truncated SVD on observed (imperfect but illustrative)\nU, s, Vt = np.linalg.svd(R_obs, full_matrices=False)\nk = n_factors\nR_hat = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]\nR_hat = np.clip(R_hat, 1, 5)\n\n# RMSE on observed entries\nobserved_pred = R_hat[observed_mask]\nobserved_true = R_true[observed_mask]\nrmse = np.sqrt(np.mean((observed_pred - observed_true)**2))\nprint(f\"RMSE on observed ratings: {rmse:.3f}\")\n\n# Top-5 recommendations for user 0\nuser0_scores = R_hat[0]\nuser0_unseen = ~observed_mask[0]\ntop5 = np.argsort(user0_scores * user0_unseen)[::-1][:5]\nprint(f\"Top-5 recommendations for user 0: items {top5} with scores {user0_scores[top5].round(2)}\")"
    },
    "practice": {
        "title": "System of Equations Solver",
        "desc": "Write solve_system(A, b) that checks if the system Ax=b is (1) well-determined (use rank), (2) overdetermined (least squares), or (3) underdetermined (minimum-norm solution via pinv), and solves accordingly with a label. Also write condition_number(A) and show how ill-conditioned matrices cause solution instability.",
        "starter": "import numpy as np\n\ndef solve_system(A, b):\n    m, n = A.shape\n    rank = np.linalg.matrix_rank(A)\n    if m == n and rank == n:\n        label = \"well-determined\"\n        x = np.linalg.solve(A, b)\n    elif m > n:\n        label = \"overdetermined (least squares)\"\n        x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)\n    else:\n        label = \"underdetermined (min-norm)\"\n        x = np.linalg.pinv(A) @ b\n    return x, label\n\ndef condition_number(A):\n    s = np.linalg.svd(A, compute_uv=False)\n    return s[0] / s[-1] if s[-1] > 0 else np.inf\n\n# Test cases\nrng = np.random.default_rng(42)\n\n# Well-determined 3x3\nA1 = rng.standard_normal((3, 3))\nb1 = rng.standard_normal(3)\nx1, lbl1 = solve_system(A1, b1)\nprint(f\"{lbl1}: cond={condition_number(A1):.1f}, error={np.linalg.norm(A1@x1-b1):.2e}\")\n\n# Overdetermined 10x3\nA2 = rng.standard_normal((10, 3))\nb2 = rng.standard_normal(10)\nx2, lbl2 = solve_system(A2, b2)\nprint(f\"{lbl2}: cond={condition_number(A2):.1f}, residual={np.linalg.norm(A2@x2-b2):.4f}\")\n\n# Ill-conditioned\nA3 = np.array([[1, 1], [1, 1+1e-10]])\nb3 = np.array([2.0, 2.0])\nx3, lbl3 = solve_system(A3, b3)\nprint(f\"{lbl3}: cond={condition_number(A3):.2e}\")\n"
    }
    },

    {
    "title": "31. Numerical Differentiation & Optimization",
    "desc": "Finite differences approximate gradients of black-box functions. Combined with np.gradient, they enable sensitivity analysis, gradient checking, and simple optimization without symbolic math.",
    "examples": [
        {"label": "Finite differences: forward, backward, central", "code": "import numpy as np\n\n# First derivative via finite differences\ndef forward_diff(f, x, h=1e-5):\n    return (f(x + h) - f(x)) / h\n\ndef backward_diff(f, x, h=1e-5):\n    return (f(x) - f(x - h)) / h\n\ndef central_diff(f, x, h=1e-5):\n    return (f(x + h) - f(x - h)) / (2 * h)\n\ndef second_diff(f, x, h=1e-5):\n    return (f(x + h) - 2*f(x) + f(x - h)) / h**2\n\n# Test on f(x) = sin(x), f\'(x) = cos(x)\nf = np.sin\nx = np.pi / 4\ntrue_deriv = np.cos(x)\n\nprint(f\"True f\'(pi/4) = {true_deriv:.10f}\")\nprint(f\"Forward:   {forward_diff(f, x):.10f}  err={abs(forward_diff(f,x)-true_deriv):.2e}\")\nprint(f\"Backward:  {backward_diff(f, x):.10f}  err={abs(backward_diff(f,x)-true_deriv):.2e}\")\nprint(f\"Central:   {central_diff(f, x):.10f}  err={abs(central_diff(f,x)-true_deriv):.2e}\")\nprint(f\"Second:    {second_diff(f, x):.10f}  true=-sin(pi/4)={-np.sin(x):.10f}\")\n\n# Vectorized on array\nx_arr = np.linspace(0, 2*np.pi, 100)\nderiv_arr = central_diff(np.sin, x_arr)\nerror = np.abs(deriv_arr - np.cos(x_arr))\nprint(f\"Max error over array: {error.max():.2e}\")"},
        {"label": "np.gradient for array derivatives", "code": "import numpy as np\n\n# np.gradient: uses central differences internally, handles edges with one-sided\nx = np.linspace(0, 2*np.pi, 100)\ny = np.sin(x)\n\ndydx = np.gradient(y, x)   # pass x for proper spacing\ntrue  = np.cos(x)\nprint(f\"Max error vs cos(x): {np.abs(dydx - true).max():.4e}\")\n\n# Partial derivatives of 2D function\nnx, ny = 50, 60\nx_1d = np.linspace(0, 2, nx)\ny_1d = np.linspace(0, 3, ny)\nX, Y = np.meshgrid(x_1d, y_1d)\n\nZ = np.sin(X) * np.cos(Y)\n\n# gradient returns [dZ/dy, dZ/dx] for 2D (row, col ordering)\ndZ_dy, dZ_dx = np.gradient(Z, y_1d, x_1d)\n\ntrue_dZ_dx = np.cos(X) * np.cos(Y)\ntrue_dZ_dy = -np.sin(X) * np.sin(Y)\n\nprint(f\"dZ/dx error: {np.abs(dZ_dx - true_dZ_dx).max():.4e}\")\nprint(f\"dZ/dy error: {np.abs(dZ_dy - true_dZ_dy).max():.4e}\")\n\n# Gradient magnitude (for edge detection in images)\nmag = np.sqrt(dZ_dx**2 + dZ_dy**2)\nprint(f\"Gradient magnitude: min={mag.min():.3f}, max={mag.max():.3f}\")"},
        {"label": "Gradient descent with NumPy", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Optimize f(x, y) = (x-3)^2 + 2*(y+1)^2 (minimum at (3, -1))\ndef f(params):\n    x, y = params\n    return (x - 3)**2 + 2*(y + 1)**2\n\ndef grad_f(params):\n    x, y = params\n    return np.array([2*(x - 3), 4*(y + 1)])\n\n# Gradient descent\nparams  = np.array([0.0, 0.0])\nlr      = 0.1\nhistory = [params.copy()]\n\nfor i in range(50):\n    g = grad_f(params)\n    params = params - lr * g\n    history.append(params.copy())\n    if i % 10 == 9:\n        print(f\"  iter {i+1:3d}: f={f(params):.6f}, params=({params[0]:.3f}, {params[1]:.3f})\")\n\nprint(f\"True minimum: (3, -1), found: ({params[0]:.4f}, {params[1]:.4f})\")\n\n# Numerical gradient check (compare analytic vs finite diff)\ntest_pt = rng.standard_normal(2)\nanalytic = grad_f(test_pt)\nh = 1e-6\nnumeric  = np.array([(f(test_pt + h*e) - f(test_pt - h*e)) / (2*h)\n                      for e in np.eye(2)])\nprint(f\"Gradient check: analytic={analytic.round(4)}, numeric={numeric.round(4)}\")\nprint(f\"Max error: {np.abs(analytic - numeric).max():.2e}\")"}
    ],
    "rw": {
        "title": "Gradient-Based Calibration",
        "scenario": "A financial model calibrates parameters to match observed option prices by minimizing a loss function using gradient descent with numerical gradients.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Simulate: find mu, sigma that best fit observed log returns\nn_obs = 500\ntrue_mu, true_sigma = 0.001, 0.02\nobserved = rng.normal(true_mu, true_sigma, n_obs)\n\ndef neg_log_likelihood(params, data):\n    mu, log_sigma = params\n    sigma = np.exp(log_sigma)  # log parameterization ensures sigma > 0\n    return 0.5 * np.sum(np.log(2*np.pi*sigma**2) + ((data - mu)/sigma)**2)\n\ndef numerical_gradient(f, params, h=1e-6):\n    grad = np.zeros_like(params)\n    for i in range(len(params)):\n        e = np.zeros_like(params)\n        e[i] = h\n        grad[i] = (f(params + e) - f(params - e)) / (2 * h)\n    return grad\n\nparams = np.array([0.0, np.log(0.01)])  # initial guess\nlr = 1e-4\n\nfor epoch in range(500):\n    loss = neg_log_likelihood(params, observed)\n    grad = numerical_gradient(lambda p: neg_log_likelihood(p, observed), params)\n    params -= lr * grad\n\nmu_hat    = params[0]\nsigma_hat = np.exp(params[1])\nprint(f\"True:      mu={true_mu:.4f}, sigma={true_sigma:.4f}\")\nprint(f\"Estimated: mu={mu_hat:.4f}, sigma={sigma_hat:.4f}\")\nprint(f\"Error:     mu={abs(mu_hat-true_mu):.2e}, sigma={abs(sigma_hat-true_sigma):.2e}\")"
    },
    "practice": {
        "title": "Jacobian Checker",
        "desc": "Write jacobian(f, x, h=1e-6) that computes the Jacobian matrix of a vector-valued function f: R^n -> R^m using central differences. Then write gradient_check(f, grad_f, x) that compares the numerical Jacobian with the analytic gradient and reports the relative error. Test with f(x) = [sin(x0)*x1, x0^2 + exp(x1)].",
        "starter": "import numpy as np\n\ndef jacobian(f, x, h=1e-6):\n    x  = np.asarray(x, float)\n    f0 = np.asarray(f(x), float)\n    m  = f0.size\n    n  = x.size\n    J  = np.zeros((m, n))\n    for j in range(n):\n        dx    = np.zeros(n)\n        dx[j] = h\n        J[:, j] = (np.asarray(f(x + dx)) - np.asarray(f(x - dx))) / (2 * h)\n    return J\n\ndef gradient_check(f, grad_f, x, h=1e-6):\n    J_num = jacobian(f, x, h)\n    J_ana = np.asarray(grad_f(x))\n    err   = np.abs(J_num - J_ana)\n    rel   = err / (np.abs(J_ana) + 1e-8)\n    return {\"max_abs_err\": err.max(), \"max_rel_err\": rel.max(), \"ok\": rel.max() < 1e-4}\n\n# Test function: f(x) = [sin(x0)*x1, x0^2 + exp(x1)]\ndef f_vec(x):\n    return [np.sin(x[0])*x[1], x[0]**2 + np.exp(x[1])]\n\ndef df_vec(x):\n    return np.array([\n        [np.cos(x[0])*x[1], np.sin(x[0])],\n        [2*x[0],              np.exp(x[1])],\n    ])\n\nx0 = np.array([0.5, 1.2])\nresult = gradient_check(f_vec, df_vec, x0)\nprint(\"Jacobian check:\", result)\nprint(\"Numerical J:\\n\", jacobian(f_vec, x0).round(6))\nprint(\"Analytic J:\\n\",  df_vec(x0).round(6))\n"
    }
    },

    {
    "title": "32. NumPy in Data Science Workflows",
    "desc": "NumPy integrates tightly with pandas, scikit-learn, PyTorch, and SciPy. Understanding these bridges — arrays, dtypes, memory sharing — makes you faster at the whole pipeline.",
    "examples": [
        {"label": "NumPy <-> Pandas integration", "code": "import numpy as np\n\n# Simulate what pandas does under the hood\n# A DataFrame is essentially a dict of 1D NumPy arrays\n\n# From numpy to structured array (pandas-like)\nn = 5\nids    = np.arange(1, n+1)\nnames  = np.array([\'Alice\', \'Bob\', \'Carol\', \'Dave\', \'Eve\'])\nscores = np.array([92.5, 78.3, 88.1, 95.0, 70.2])\ngrades = np.where(scores >= 90, \'A\', np.where(scores >= 80, \'B\', \'C\'))\n\n# Operations you\'d do in pandas, using only NumPy\nmean_score = scores.mean()\ntop_scorers = names[scores >= 90]\npassing     = names[scores >= 75]\n\nprint(\"Mean score:\", mean_score.round(2))\nprint(\"Top scorers (A grade):\", top_scorers)\nprint(\"Passing (>=75):\", passing)\n\n# Group by grade\nfor grade in np.unique(grades):\n    mask = grades == grade\n    print(f\"Grade {grade}: {names[mask].tolist()}, avg={scores[mask].mean():.1f}\")\n\n# NumPy array -> pandas DataFrame conversion info\ntry:\n    import pandas as pd\n    df = pd.DataFrame({\'id\': ids, \'name\': names, \'score\': scores, \'grade\': grades})\n    # df.values returns numpy array (may copy depending on dtypes)\n    arr = df[[\'id\', \'score\']].to_numpy()\n    print(\"DataFrame to numpy:\", arr.shape, arr.dtype)\nexcept ImportError:\n    print(\"(pandas not available, but the pattern works)\")"},
        {"label": "NumPy for feature engineering", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\nn, d = 1000, 5\n\nX = rng.standard_normal((n, d))\n\n# 1. Normalization\ndef z_score(X):\n    return (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)\n\ndef min_max(X):\n    lo, hi = X.min(axis=0), X.max(axis=0)\n    return (X - lo) / (hi - lo + 1e-8)\n\nXz = z_score(X)\nXm = min_max(X)\nprint(f\"Z-score: mean={Xz.mean(axis=0).round(2)}, std={Xz.std(axis=0).round(2)}\")\nprint(f\"MinMax: [{Xm.min():.3f}, {Xm.max():.3f}]\")\n\n# 2. Polynomial features (degree 2, first 3 columns)\nXp = np.column_stack([X[:, :3], X[:, :3]**2,\n                       X[:, 0:1]*X[:, 1:2], X[:, 1:2]*X[:, 2:3]])\nprint(f\"Polynomial features: {X.shape} -> {Xp.shape}\")\n\n# 3. One-hot encoding\ncats = rng.integers(0, 4, n)   # 4 categories\nohe  = (cats[:, np.newaxis] == np.arange(4)[np.newaxis, :]).astype(float)\nprint(f\"OHE: shape={ohe.shape}, sum per row all 1: {np.all(ohe.sum(axis=1)==1)}\")\n\n# 4. Interaction features (outer product per row)\na = X[:, :3]   # 3 features\n# Row-wise outer: shape (n, 3, 3) -> upper triangle -> (n, 6) interaction terms\ncombos = np.einsum(\'ni,nj->nij\', a, a)\ntriu_idx = np.triu_indices(3, k=0)\ninteractions = combos[:, triu_idx[0], triu_idx[1]]\nprint(f\"Interaction features shape: {interactions.shape}\")"},
        {"label": "NumPy in ML inference", "code": "import numpy as np\n\nrng = np.random.default_rng(42)\n\n# Manually implement a 2-layer neural network forward pass\ndef relu(x): return np.maximum(0, x)\ndef softmax(x):\n    e = np.exp(x - x.max(axis=1, keepdims=True))\n    return e / e.sum(axis=1, keepdims=True)\n\n# Simulated trained weights (normally loaded from file)\nn_in, n_hidden, n_out = 784, 256, 10\nW1 = rng.standard_normal((n_in, n_hidden)) * 0.01\nb1 = np.zeros(n_hidden)\nW2 = rng.standard_normal((n_hidden, n_out)) * 0.01\nb2 = np.zeros(n_out)\n\ndef forward(X):\n    h1  = relu(X @ W1 + b1)\n    out = softmax(X @ W1 @ W2 + b2)  # simplified\n    return out\n\n# Batch inference\nbatch_size = 64\nX_batch = rng.standard_normal((batch_size, n_in)).astype(np.float32)\nprobs = forward(X_batch)\npreds = probs.argmax(axis=1)\nconf  = probs.max(axis=1)\n\nprint(f\"Batch: {X_batch.shape} -> probs: {probs.shape}\")\nprint(f\"Predictions: {preds[:10]}\")\nprint(f\"Confidence: min={conf.min():.3f}, max={conf.max():.3f}, mean={conf.mean():.3f}\")\n\n# Top-3 predictions per sample\ntop3 = np.argsort(probs, axis=1)[:, -3:][:, ::-1]\nprint(f\"Top-3 class indices for sample 0: {top3[0]}\")"}
    ],
    "rw": {
        "title": "End-to-End ML Pipeline",
        "scenario": "A data scientist implements a complete train/eval cycle using only NumPy: feature normalization, train/val/test split, logistic regression with gradient descent, and evaluation metrics.",
        "code": "import numpy as np\n\nrng = np.random.default_rng(42)\nN, D = 1000, 10\n\n# Synthetic binary classification data\nX = rng.standard_normal((N, D))\ntrue_w = rng.standard_normal(D)\ny = (X @ true_w + rng.normal(0, 0.5, N) > 0).astype(float)\n\n# Train/val/test split (70/15/15)\nidx = rng.permutation(N)\nn_train = int(0.7*N); n_val = int(0.15*N)\ntr, va, te = idx[:n_train], idx[n_train:n_train+n_val], idx[n_train+n_val:]\n\ndef normalize(X_tr, X_te):\n    mu, std = X_tr.mean(0), X_tr.std(0) + 1e-8\n    return (X_tr-mu)/std, (X_te-mu)/std\n\nX_tr, X_te = normalize(X[tr], X[te])\nX_tr, X_va = normalize(X[tr], X[va])\n\n# Logistic regression with SGD\ndef sigmoid(z): return 1 / (1 + np.exp(-np.clip(z, -100, 100)))\n\nw = np.zeros(D)\nlr, n_epochs, bs = 0.1, 20, 32\nfor epoch in range(n_epochs):\n    perm = rng.permutation(len(tr))\n    for i in range(0, len(tr), bs):\n        xi = X_tr[perm[i:i+bs]]\n        yi = y[tr][perm[i:i+bs]]\n        pred = sigmoid(xi @ w)\n        grad = xi.T @ (pred - yi) / len(yi)\n        w -= lr * grad\n\ndef accuracy(X, y_true, w):\n    return ((sigmoid(X @ w) >= 0.5) == y_true.astype(bool)).mean()\n\nprint(f\"Train acc: {accuracy(X_tr, y[tr], w):.3f}\")\nprint(f\"Val   acc: {accuracy(X_va, y[va], w):.3f}\")\nprint(f\"Test  acc: {accuracy(X_te, y[te], w):.3f}\")"
    },
    "practice": {
        "title": "Cross-Validation",
        "desc": "Implement k_fold_cv(X, y, model_fn, k=5, seed=42) where model_fn(X_train, y_train, X_val) returns predictions. Split data into k folds, train on k-1 folds, predict on the held-out fold, compute accuracy for each fold, and return mean and std. Test with a simple threshold classifier.",
        "starter": "import numpy as np\n\ndef k_fold_cv(X, y, model_fn, k=5, seed=42):\n    rng  = np.random.default_rng(seed)\n    idx  = rng.permutation(len(y))\n    fold_size = len(y) // k\n    scores = []\n    for fold in range(k):\n        val_idx   = idx[fold*fold_size:(fold+1)*fold_size]\n        train_idx = np.concatenate([idx[:fold*fold_size], idx[(fold+1)*fold_size:]])\n        X_tr, y_tr = X[train_idx], y[train_idx]\n        X_va, y_va = X[val_idx],   y[val_idx]\n        preds = model_fn(X_tr, y_tr, X_va)\n        scores.append((preds == y_va).mean())\n    return {\"mean\": np.mean(scores), \"std\": np.std(scores), \"folds\": scores}\n\n# Threshold classifier: predict 1 if feature 0 > median\ndef threshold_model(X_tr, y_tr, X_va):\n    threshold = np.median(X_tr[:, 0])\n    return (X_va[:, 0] > threshold).astype(int)\n\nrng = np.random.default_rng(42)\nN, D = 500, 5\nX = rng.standard_normal((N, D))\ny = (X[:, 0] + 0.5 * X[:, 1] > 0).astype(int)\n\nresult = k_fold_cv(X, y, threshold_model, k=5)\nprint(f\"5-fold CV: {result[\'mean\']:.3f} ± {result[\'std\']:.3f}\")\nprint(f\"Per-fold: {[round(s,3) for s in result[\'folds\']]}\")\n"
    }
    },

]  # end SECTIONS


# ─── Generate files ───────────────────────────────────────────────────────────
html = make_html(SECTIONS)
nb   = make_nb(SECTIONS)

(BASE / "index.html").write_text(html, encoding="utf-8")
(BASE / "study_guide.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")

print(f"NumPy guide created: {BASE}")
print(f"  index.html:        {(BASE/'index.html').stat().st_size/1024:.1f} KB")
print(f"  study_guide.ipynb: {len(nb['cells'])} cells")
