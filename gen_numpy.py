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

]  # end SECTIONS


# ─── Generate files ───────────────────────────────────────────────────────────
html = make_html(SECTIONS)
nb   = make_nb(SECTIONS)

(BASE / "index.html").write_text(html, encoding="utf-8")
(BASE / "study_guide.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")

print(f"NumPy guide created: {BASE}")
print(f"  index.html:        {(BASE/'index.html').stat().st_size/1024:.1f} KB")
print(f"  study_guide.ipynb: {len(nb['cells'])} cells")
