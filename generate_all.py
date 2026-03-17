#!/usr/bin/env python3
"""Generate 9 Data Science study guides (notebook + HTML) + master hub page."""

import json, pathlib
from html import escape as esc

BASE = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
BASE.mkdir(parents=True, exist_ok=True)

# ─── HTML Generator ──────────────────────────────────────────────────────────
def make_html(title, emoji, accent, sections):
    nav = "\n    ".join(
        f'<li><a href="#s{i}" onclick="activate(this,event)">{esc(s["title"])}</a></li>'
        for i, s in enumerate(sections)
    )
    cards_html = ""
    for i, s in enumerate(sections):
        blocks_html = ""
        for j, ex in enumerate(s.get("examples", [])):
            cid = f"c{i}_{j}"
            blocks_html += (
                f'<div class="code-block">'
                f'<div class="code-header"><span>{esc(ex.get("label","Example"))}</span>'
                f'<button onclick="copyCode(\'{cid}\')">Copy</button></div>'
                f'<pre><code id="{cid}" class="language-python">{esc(ex["code"])}</code></pre>'
                f'</div>'
            )
        rw = s.get("rw")
        rw_html = ""
        if rw:
            rw_html = (
                f'<div class="rw-block">'
                f'<div class="rw-header">&#x1F4BC; Real-World: {esc(rw["title"])}</div>'
                f'<div class="rw-desc">{esc(rw["scenario"])}</div>'
                f'<pre><code class="language-python">{esc(rw["code"])}</code></pre>'
                f'</div>'
            )
        cards_html += (
            f'<div class="topic" id="s{i}">'
            f'<div class="topic-header" onclick="toggle(this)">'
            f'<span>{esc(s["title"])}</span><span class="arrow">&#9660;</span></div>'
            f'<div class="topic-body">'
            f'<p class="desc">{esc(s.get("desc",""))}</p>'
            f'{blocks_html}{rw_html}</div></div>'
        )
    n = len(sections)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{{--bg:#0f1117;--sb:#161b22;--card:#1c2128;--brd:#30363d;--txt:#c9d1d9;--mut:#8b949e;--acc:{accent}}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{display:flex;min-height:100vh;background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px}}
.sidebar{{width:260px;min-height:100vh;background:var(--sb);border-right:1px solid var(--brd);position:sticky;top:0;height:100vh;overflow-y:auto;flex-shrink:0}}
.sb-head{{padding:20px;border-bottom:1px solid var(--brd)}}
.sb-head h2{{font-size:1.05rem;color:var(--acc)}}
.sb-head p{{font-size:.8rem;color:var(--mut);margin-top:3px}}
#search{{width:100%;padding:7px 10px;background:#0d1117;border:1px solid var(--brd);border-radius:6px;color:var(--txt);font-size:.84rem;margin-top:10px}}
#search:focus{{outline:none;border-color:var(--acc)}}
.nav-list{{list-style:none;padding:6px 0}}
.nav-list li a{{display:block;padding:7px 18px;color:var(--mut);text-decoration:none;font-size:.84rem;border-left:3px solid transparent;transition:.15s}}
.nav-list li a:hover,.nav-list li a.active{{color:var(--txt);border-left-color:var(--acc);background:rgba(255,255,255,.03)}}
.main{{flex:1;padding:32px 40px;max-width:880px}}
.pg-title{{font-size:2rem;font-weight:700;color:var(--acc);margin-bottom:6px}}
.pg-sub{{color:var(--mut);margin-bottom:28px}}
.topic{{background:var(--card);border:1px solid var(--brd);border-radius:8px;margin-bottom:14px;overflow:hidden}}
.topic-header{{display:flex;justify-content:space-between;align-items:center;padding:13px 18px;cursor:pointer;user-select:none}}
.topic-header:hover{{background:rgba(255,255,255,.04)}}
.topic-header>span:first-child{{font-weight:600}}
.arrow{{color:var(--mut);transition:transform .2s}}
.topic-body{{display:none;padding:18px;border-top:1px solid var(--brd)}}
.topic-body.open{{display:block}}
.arrow.open{{transform:rotate(180deg)}}
.desc{{color:var(--mut);margin-bottom:14px;line-height:1.6;font-size:.92rem}}
.code-block{{margin-bottom:14px;border:1px solid var(--brd);border-radius:6px;overflow:hidden}}
.code-header{{display:flex;justify-content:space-between;padding:7px 12px;background:#161b22;font-size:.78rem;color:var(--mut)}}
.code-header button{{background:0;border:1px solid var(--brd);color:var(--mut);padding:2px 9px;border-radius:4px;cursor:pointer;font-size:.73rem}}
.code-header button:hover{{color:var(--txt);border-color:var(--acc)}}
pre{{margin:0}}pre code{{font-size:.83rem;padding:13px!important}}
.rw-block{{background:#0d2818;border:1px solid #238636;border-radius:6px;padding:15px;margin-top:6px}}
.rw-header{{font-weight:600;color:#3fb950;margin-bottom:7px}}
.rw-desc{{color:#7ee787;font-size:.84rem;margin-bottom:11px;line-height:1.5}}
</style></head><body>
<aside class="sidebar">
  <div class="sb-head"><h2>{emoji} {esc(title)}</h2><p>Study Guide &bull; {n} topics</p>
    <input id="search" placeholder="Search..." oninput="filterNav(this.value)">
  </div>
  <ul class="nav-list" id="navlist">{nav}</ul>
</aside>
<main class="main">
  <h1 class="pg-title">{emoji} {esc(title)}</h1>
  <p class="pg-sub">{n} topics &bull; Click any card to expand</p>
  {cards_html}
</main>
<script>
hljs.highlightAll();
function toggle(h){{var b=h.nextElementSibling,a=h.querySelector('.arrow');b.classList.toggle('open');a.classList.toggle('open');}}
function activate(el,e){{if(e)e.preventDefault();document.querySelectorAll('.nav-list a').forEach(a=>a.classList.remove('active'));el.classList.add('active');}}
function filterNav(q){{document.querySelectorAll('#navlist li').forEach(li=>{{li.style.display=li.textContent.toLowerCase().includes(q.toLowerCase())?'':'none';}});}}
function copyCode(id){{navigator.clipboard.writeText(document.getElementById(id).innerText).catch(()=>{{}});}}
document.addEventListener('DOMContentLoaded',()=>{{var fh=document.querySelector('.topic-header');if(fh)fh.click();var fa=document.querySelector('.nav-list a');if(fa)fa.classList.add('active');}});
</script></body></html>"""


# ─── Notebook Generator ───────────────────────────────────────────────────────
def make_notebook(title, sections):
    cells = []
    n = [0]
    def nid():
        n[0] += 1; return f"{n[0]:04d}"
    def md_cell(src):
        lines = src.split("\n")
        source = [l + "\n" for l in lines]
        if source: source[-1] = source[-1].rstrip("\n")
        return {"cell_type":"markdown","id":nid(),"metadata":{},"source":source}
    def code_cell(src):
        lines = src.split("\n")
        source = [l + "\n" for l in lines]
        if source: source[-1] = source[-1].rstrip("\n")
        return {"cell_type":"code","execution_count":None,"id":nid(),"metadata":{},"outputs":[],"source":source}

    cells.append(md_cell(f"# {title} Study Guide\n\nHands-on guide with practical examples and real-world use cases."))
    for i, s in enumerate(sections, 1):
        cells.append(md_cell(f"## {i}. {s['title']}\n\n{s.get('desc','')}"))
        for ex in s.get("examples", []):
            if ex.get("label"):
                cells.append(md_cell(f"**{ex['label']}**"))
            cells.append(code_cell(ex["code"]))
        rw = s.get("rw")
        if rw:
            cells.append(md_cell(f"### Real-World: {rw['title']}\n\n> {rw['scenario']}"))
            cells.append(code_cell(rw["code"]))
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name":"Python 3","language":"python","name":"python3"},
            "language_info": {"name":"python","version":"3.11.0"}
        },
        "nbformat": 4, "nbformat_minor": 5
    }


# ─── Topic Data ───────────────────────────────────────────────────────────────
GUIDES = [

# ══════════════════════════════════════════════════════════════════════════════
# 1. NumPy
# ══════════════════════════════════════════════════════════════════════════════
{
"name":"NumPy","folder":"01_numpy","emoji":"🔢","accent":"#79c0ff",
"sections":[
{
"title":"1. Array Creation",
"desc":"NumPy arrays are the core data structure for numerical computing. Create them from lists, ranges, or built-in functions.",
"examples":[
{"label":"From lists and special functions","code":
"""import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([[1, 2, 3], [4, 5, 6]])   # 2D array

zeros = np.zeros((3, 4))               # 3x4 of zeros
ones  = np.ones((2, 3))                # 2x3 of ones
eye   = np.eye(3)                      # 3x3 identity matrix
full  = np.full((2, 2), 7.0)           # fill with constant

print("1D:", a)
print("2D shape:", b.shape)
print("Identity:\n", eye)"""},
{"label":"Ranges and linspace","code":
"""import numpy as np

r   = np.arange(0, 20, 2)          # step by 2 → [0,2,4,...,18]
pts = np.linspace(0, 1, 5)         # 5 evenly-spaced points
log = np.logspace(0, 3, 4)         # [1, 10, 100, 1000]
rnd = np.random.rand(3, 3)         # uniform [0, 1)

print("arange:", r)
print("linspace:", pts)
print("logspace:", log)"""}
],
"rw":{
"title":"Feature Matrix for ML Preprocessing",
"scenario":"Build a normalized feature matrix from raw sensor data before feeding it to a machine learning model.",
"code":
"""import numpy as np

np.random.seed(42)
n_samples, n_features = 5000, 12
X = np.random.randn(n_samples, n_features)

# Add bias column (intercept term)
bias = np.ones((n_samples, 1))
X_b  = np.hstack([bias, X])

print(f"Feature matrix: {X_b.shape}")
print(f"Memory: {X_b.nbytes / 1024:.1f} KB")
print(f"Sample row: {X_b[0].round(3)}")"""}
},
{
"title":"2. Array Attributes & Inspection",
"desc":"Understanding shape, dtype, memory layout, and basic properties helps diagnose issues and optimize code.",
"examples":[
{"label":"Shape, dtype, ndim, size","code":
"""import numpy as np

a = np.array([[1.5, 2.0, 3.1],
              [4.0, 5.5, 6.2]], dtype=np.float32)

print("shape:   ", a.shape)
print("ndim:    ", a.ndim)
print("dtype:   ", a.dtype)
print("size:    ", a.size)
print("itemsize:", a.itemsize, "bytes")
print("nbytes:  ", a.nbytes, "bytes")
print("Transpose shape:", a.T.shape)"""},
{"label":"Type casting and reshape","code":
"""import numpy as np

a = np.arange(12)
r = a.reshape(3, 4)
print("Reshaped:\n", r)
print("Flattened:", r.flatten())
b = a.astype(np.float64)
print("float64 dtype:", b.dtype)
# -1 means infer that dimension
c = a.reshape(2, -1)
print("Auto-reshape:", c.shape)"""}
],
"rw":{
"title":"Memory Profiling Sensor Data",
"scenario":"A data engineer audits memory usage of sensor arrays before storing them in a time-series database.",
"code":
"""import numpy as np

sensor_arrays = {
    "temperature": np.random.uniform(15, 40, (10000, 24)),
    "pressure":    np.random.uniform(900, 1100, (10000, 24)),
    "humidity":    np.random.uniform(20, 90, (10000, 24)),
}

for name, arr in sensor_arrays.items():
    mb = arr.nbytes / 1e6
    arr32 = arr.astype(np.float32)
    print(f"{name:12s} float64={mb:.2f}MB  float32={arr32.nbytes/1e6:.2f}MB  "
          f"saved={mb - arr32.nbytes/1e6:.2f}MB")"""}
},
{
"title":"3. Indexing & Slicing",
"desc":"NumPy supports powerful indexing: basic, slice, fancy, and boolean — all without Python loops.",
"examples":[
{"label":"1D and 2D indexing","code":
"""import numpy as np

a = np.arange(10)
print(a[2])           # element at index 2
print(a[-1])          # last element
print(a[2:7])         # slice [2 3 4 5 6]
print(a[::2])         # every 2nd element
print(a[::-1])        # reversed

m = np.arange(12).reshape(3, 4)
print(m[1, 2])        # row 1, col 2 → 6
print(m[:, 1])        # column 1
print(m[0:2, 1:3])    # 2x2 sub-matrix"""},
{"label":"Fancy indexing","code":
"""import numpy as np

a = np.array([10, 20, 30, 40, 50])
idx = [0, 2, 4]
print("Fancy:", a[idx])           # [10 30 50]

m = np.arange(16).reshape(4, 4)
rows, cols = [0, 1, 2], [1, 2, 3]
print("Diagonal slice:", m[rows, cols])  # offset diagonal

# np.ix_ for cross-product selection
print("Sub-matrix:\n", m[np.ix_(rows, cols)])"""}
],
"rw":{
"title":"Time-Window Extraction for Anomaly Detection",
"scenario":"An IoT engineer extracts sliding windows from continuous sensor readings to detect anomalies.",
"code":
"""import numpy as np

# Simulate 30 days of hourly readings
time_series = np.random.randn(24 * 30) + 20   # ~20°C baseline
windows = np.lib.stride_tricks.sliding_window_view(time_series, window_shape=24)

print(f"Original: {time_series.shape}")
print(f"Windows:  {windows.shape}")  # (696, 24)

# Find the window with highest variability
stds = windows.std(axis=1)
peak_idx = np.argmax(stds)
print(f"Most variable 24h window starts at hour {peak_idx}")
print(f"  std = {stds[peak_idx]:.3f}, mean = {windows[peak_idx].mean():.2f}")"""}
},
{
"title":"4. Mathematical Operations",
"desc":"NumPy provides element-wise arithmetic and universal functions (ufuncs) that operate on entire arrays without loops.",
"examples":[
{"label":"Element-wise arithmetic and ufuncs","code":
"""import numpy as np

a = np.array([1.0, 4.0, 9.0, 16.0])
b = np.array([2.0, 2.0, 3.0,  4.0])

print("add:   ", a + b)
print("mul:   ", a * b)
print("power: ", a ** 0.5)       # same as np.sqrt(a)
print("sqrt:  ", np.sqrt(a))
print("log:   ", np.log(a).round(3))
print("clip:  ", np.clip(a, 2, 10))"""},
{"label":"Trigonometry and sign operations","code":
"""import numpy as np

x = np.linspace(-np.pi, np.pi, 5)
print("sin:", np.sin(x).round(2))
print("cos:", np.cos(x).round(2))

a = np.array([-3, -1, 0, 1, 3])
print("abs: ", np.abs(a))
print("sign:", np.sign(a))

# cumulative operations
arr = np.array([1, 2, 3, 4, 5])
print("cumsum:", np.cumsum(arr))
print("cumprod:", np.cumprod(arr))"""}
],
"rw":{
"title":"Daily Return & Volatility Calculation",
"scenario":"A quant analyst computes daily returns and annualized volatility from historical stock prices.",
"code":
"""import numpy as np

prices = np.array([100, 102, 98, 105, 103, 110, 108, 115, 112, 118])
# Percentage daily returns
pct_returns = np.diff(prices) / prices[:-1] * 100
print("Daily returns %:", pct_returns.round(2))

# Log returns (additive over time)
log_returns = np.diff(np.log(prices))
annualized_vol = log_returns.std() * np.sqrt(252)
print(f"Annualized volatility: {annualized_vol:.4f}")

# Sharpe-like metric (mean / std of returns)
sharpe = log_returns.mean() / log_returns.std() * np.sqrt(252)
print(f"Annualized Sharpe:    {sharpe:.3f}")"""}
},
{
"title":"5. Broadcasting",
"desc":"Broadcasting lets NumPy perform operations on arrays of different shapes without making copies of the data.",
"examples":[
{"label":"Scalar and row/column broadcasting","code":
"""import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])

print("+ scalar:\n", a + 10)
print("* row:\n",    a * np.array([1, 2, 3]))   # broadcast along cols

col = np.array([[10], [20]])
print("+ col:\n",    a + col)                    # broadcast along rows"""},
{"label":"Normalizing a dataset","code":
"""import numpy as np

X = np.random.randn(100, 5)          # 100 samples, 5 features
mean = X.mean(axis=0)                # shape (5,)
std  = X.std(axis=0)                 # shape (5,)

X_norm = (X - mean) / std           # (100,5) - (5,) / (5,)  ✓

print("Original mean:", X.mean(axis=0).round(2))
print("Normed mean: ", X_norm.mean(axis=0).round(8))
print("Normed std:  ", X_norm.std(axis=0).round(8))"""}
],
"rw":{
"title":"Batch Image Normalization for CNNs",
"scenario":"A computer vision engineer normalizes a batch of images using ImageNet channel statistics before inference.",
"code":
"""import numpy as np

# Simulate batch: (N, H, W, C)
images = np.random.randint(0, 256, (32, 64, 64, 3), dtype=np.uint8)

# ImageNet channel means/stds  (R, G, B)
mean_rgb = np.array([0.485, 0.456, 0.406])
std_rgb  = np.array([0.229, 0.224, 0.225])

normalized = (images.astype(np.float32) / 255.0 - mean_rgb) / std_rgb
# Broadcasting: (32,64,64,3) - (3,) / (3,)

print(f"Input:  {images.shape}, dtype={images.dtype}")
print(f"Output: {normalized.shape}, dtype={normalized.dtype}")
print(f"Value range: [{normalized.min():.2f}, {normalized.max():.2f}]")"""}
},
{
"title":"6. Linear Algebra",
"desc":"NumPy's linalg module provides matrix operations essential for machine learning, statistics, and scientific computing.",
"examples":[
{"label":"Matrix multiply, inverse, determinant","code":
"""import numpy as np

A = np.array([[2, 1], [1, 3]], dtype=float)
B = np.array([[1, 2], [3, 4]], dtype=float)

print("dot(A,B):\n", np.dot(A, B))
print("A @ B:\n", A @ B)                  # preferred syntax
print("inv(A):\n", np.linalg.inv(A))
print("det(A):", np.linalg.det(A))
print("Verify A @ inv(A):\n", (A @ np.linalg.inv(A)).round(10))"""},
{"label":"Eigenvalues and solving linear systems","code":
"""import numpy as np

A = np.array([[4, 2], [1, 3]], dtype=float)
vals, vecs = np.linalg.eig(A)
print("Eigenvalues:", vals)
print("Eigenvectors:\n", vecs.round(3))

# Solve Ax = b
b = np.array([10, 8], dtype=float)
x = np.linalg.solve(A, b)
print("Solution x:", x)
print("Verify:", np.allclose(A @ x, b))"""}
],
"rw":{
"title":"Minimum-Variance Portfolio Optimization",
"scenario":"A portfolio manager uses covariance matrix inversion to compute optimal minimum-variance weights.",
"code":
"""import numpy as np

np.random.seed(0)
returns = np.random.randn(252, 5) * 0.01   # 252 days, 5 assets
cov = np.cov(returns.T)                    # 5x5 covariance matrix
inv_cov = np.linalg.inv(cov)

ones = np.ones(5)
w_raw    = inv_cov @ ones
w_minvar = w_raw / w_raw.sum()            # normalize to sum=1

port_var = float(w_minvar @ cov @ w_minvar)
port_std = np.sqrt(port_var * 252)

print("Min-variance weights:", w_minvar.round(3))
print(f"Portfolio annualized vol: {port_std:.4f}")"""}
},
{
"title":"7. Statistical Functions",
"desc":"Compute descriptive statistics along any axis, with support for percentiles, cumulative ops, and covariance.",
"examples":[
{"label":"Descriptive statistics","code":
"""import numpy as np

data = np.array([4, 7, 13, 16, 21, 23, 24, 28, 30])
print("mean:   ", np.mean(data))
print("median: ", np.median(data))
print("std:    ", np.std(data).round(2))
print("min/max:", data.min(), data.max())
print("25th pct:", np.percentile(data, 25))
print("75th pct:", np.percentile(data, 75))
print("IQR:    ", np.percentile(data, 75) - np.percentile(data, 25))"""},
{"label":"Axis-wise stats on 2D arrays","code":
"""import numpy as np

matrix = np.random.randint(1, 10, (4, 5))
print("Matrix:\n", matrix)
print("Row means:", matrix.mean(axis=1).round(2))
print("Col sums: ", matrix.sum(axis=0))
print("Argmax row 0:", np.argmax(matrix[0]))
print("Cumsum row 0:", np.cumsum(matrix[0]))"""}
],
"rw":{
"title":"Manufacturing Quality Control — Outlier Detection",
"scenario":"A quality engineer uses Z-scores to flag defective units that exceed 3 standard deviations from the mean.",
"code":
"""import numpy as np

np.random.seed(42)
measurements = np.random.normal(50, 5, 10000)
# Inject a few anomalies
measurements[[100, 500, 2000]] = [85, 5, 90]

mean = np.mean(measurements)
std  = np.std(measurements)
z_scores = np.abs((measurements - mean) / std)

outliers = measurements[z_scores > 3]
outlier_idx = np.where(z_scores > 3)[0]

print(f"Total units:  {len(measurements)}")
print(f"Outliers:     {len(outliers)} ({len(outliers)/len(measurements):.2%})")
print(f"Outlier values: {outliers}")
print(f"At indices:   {outlier_idx}")"""}
},
{
"title":"8. Boolean Indexing & np.where",
"desc":"Filter and transform arrays using conditions — the foundation of vectorized data cleaning and feature engineering.",
"examples":[
{"label":"Boolean masks and filtering","code":
"""import numpy as np

a = np.array([10, 25, 3, 47, 18, 32, 5])
mask = a > 20
print("Mask:     ", mask)
print("Values>20:", a[mask])

# In-place modification
a[a < 10] = 0
print("After zero-out:", a)

# Multiple conditions
b = np.array([1, 5, 10, 15, 20, 25, 30])
filtered = b[(b >= 5) & (b <= 20)]
print("5 to 20:", filtered)"""},
{"label":"np.where and np.select","code":
"""import numpy as np

scores = np.array([45, 78, 55, 90, 33, 68, 82])
grade = np.where(scores >= 60, "Pass", "Fail")
print("Pass/Fail:", grade)

conditions = [scores >= 90, scores >= 70, scores >= 50]
choices    = ["A", "B", "C"]
letter = np.select(conditions, choices, default="D")
print("Letter grades:", letter)"""}
],
"rw":{
"title":"Energy Consumption Flagging — HDD/CDD Calculation",
"scenario":"A building energy analyst computes heating/cooling degree-hours and flags extreme temperature events.",
"code":
"""import numpy as np

np.random.seed(1)
temps = np.random.normal(22, 6, 8760)  # 1 year of hourly temps

heating_deg = np.where(temps < 16, 16 - temps, 0)
cooling_deg = np.where(temps > 24, temps - 24, 0)
extreme     = np.sum((temps < 0) | (temps > 38))

print(f"Heating degree-hours: {heating_deg.sum():.0f}")
print(f"Cooling degree-hours: {cooling_deg.sum():.0f}")
print(f"Extreme hours (<0 or >38°C): {extreme}")
print(f"Peak heat:  {temps.max():.1f}°C at hour {temps.argmax()}")
print(f"Peak cold:  {temps.min():.1f}°C at hour {temps.argmin()}")"""}
},
{
"title":"9. Array Manipulation",
"desc":"Reshape, stack, split, and transform arrays to prepare data for algorithms that expect specific shapes.",
"examples":[
{"label":"reshape, flatten, transpose","code":
"""import numpy as np

a = np.arange(24)
r = a.reshape(4, 6)
print("Reshaped (4,6):\n", r)

b = a.reshape(2, 3, 4)
print("3D shape:", b.shape)
print("Transposed:", b.T.shape)
print("Flattened:", r.flatten()[:8], "...")

# -1 auto-infers dimension
c = a.reshape(6, -1)
print("Auto:", c.shape)"""},
{"label":"stack, vstack, hstack, split","code":
"""import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("hstack:", np.hstack([a, b]))          # [1 2 3 4 5 6]
print("vstack:\n", np.vstack([a, b]))         # 2D
print("stack axis=1:\n", np.stack([a, b], axis=1))

arr = np.arange(12)
parts = np.split(arr, 3)
print("Split:", [p.tolist() for p in parts])"""}
],
"rw":{
"title":"Image Batch Preparation for Deep Learning",
"scenario":"A CV engineer reshapes image arrays and combines batches for a convolutional neural network training pipeline.",
"code":
"""import numpy as np

batch_size = 32
H, W, C = 64, 64, 3

images = np.random.rand(batch_size, H, W, C).astype(np.float32)

# Flatten spatial dims for dense layer
flat = images.reshape(batch_size, -1)
print(f"Original: {images.shape} → Flat: {flat.shape}")

# Combine two batches
batch2 = np.random.rand(batch_size, H, W, C).astype(np.float32)
combined = np.concatenate([images, batch2], axis=0)
print(f"Combined: {combined.shape}")

# Channels-first format (N, C, H, W) for PyTorch
chw = images.transpose(0, 3, 1, 2)
print(f"CHW format: {chw.shape}")"""}
},
{
"title":"10. Random Number Generation",
"desc":"NumPy's random module is essential for simulations, data augmentation, train/test splits, and reproducibility.",
"examples":[
{"label":"Random arrays and seeding","code":
"""import numpy as np

np.random.seed(42)                         # reproducibility

u = np.random.rand(3, 3)                   # uniform [0, 1)
n = np.random.randn(3, 3)                  # standard normal
i = np.random.randint(0, 100, size=5)      # integers
c = np.random.choice([10,20,30,40], size=3, replace=False)  # no-repeat

print("Uniform:\n", u.round(2))
print("Normal:\n", n.round(2))
print("Integers:", i)
print("Choice:", c)"""},
{"label":"Distributions","code":
"""import numpy as np

np.random.seed(0)
normal  = np.random.normal(loc=50, scale=10, size=1000)
uniform = np.random.uniform(low=0, high=100, size=1000)
binom   = np.random.binomial(n=10, p=0.3, size=1000)

for name, arr in [("normal", normal), ("uniform", uniform), ("binom", binom)]:
    print(f"{name:8s}: mean={arr.mean():.2f}, std={arr.std():.2f}, "
          f"min={arr.min():.1f}, max={arr.max():.1f}")"""}
],
"rw":{
"title":"Monte Carlo Stock Price Simulation",
"scenario":"A risk analyst uses Monte Carlo simulation to estimate the distribution of portfolio values at year-end.",
"code":
"""import numpy as np

np.random.seed(99)
n_sims   = 100_000
n_days   = 252
S0       = 100           # initial price
mu_day   = 0.0003        # daily drift
sig_day  = 0.015         # daily volatility

daily_ret = np.random.normal(mu_day, sig_day, (n_sims, n_days))
prices    = S0 * np.cumprod(1 + daily_ret, axis=1)
final     = prices[:, -1]

var_95  = np.percentile(final, 5)
cvar_95 = final[final <= var_95].mean()
print(f"Expected price:     ${final.mean():.2f}")
print(f"95% VaR loss:       ${S0 - var_95:.2f}")
print(f"95% CVaR loss:      ${S0 - cvar_95:.2f}")
print(f"P(loss):            {(final < S0).mean():.1%}")"""}
}
]},  # end NumPy

# ══════════════════════════════════════════════════════════════════════════════
# 2. SQL
# ══════════════════════════════════════════════════════════════════════════════
{
"name":"SQL with Python","folder":"02_sql","emoji":"🗄️","accent":"#f0883e",
"sections":[
{
"title":"1. Setup with sqlite3",
"desc":"Python's built-in sqlite3 module lets you create and query relational databases without any external server.",
"examples":[
{"label":"Connect, create table, insert rows","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")   # in-memory DB (no file)
cur  = conn.cursor()

cur.execute("""
    CREATE TABLE employees (
        id       INTEGER PRIMARY KEY,
        name     TEXT NOT NULL,
        dept     TEXT,
        salary   REAL,
        hire_date TEXT
    )
""")

data = [
    (1, "Alice", "Engineering", 95000, "2022-03-15"),
    (2, "Bob",   "Marketing",   72000, "2021-08-01"),
    (3, "Carol", "Engineering", 88000, "2023-01-10"),
]
cur.executemany("INSERT INTO employees VALUES (?,?,?,?,?)", data)
conn.commit()
print("Created and inserted:", cur.execute("SELECT COUNT(*) FROM employees").fetchone())
conn.close()"""},
{"label":"Using a file-based database","code":
"""import sqlite3, os

db_path = "sales_demo.db"
conn = sqlite3.connect(db_path)
conn.execute("CREATE TABLE IF NOT EXISTS products (id INT, name TEXT, price REAL)")
conn.execute("INSERT OR IGNORE INTO products VALUES (1, 'Widget', 9.99)")
conn.execute("INSERT OR IGNORE INTO products VALUES (2, 'Gadget', 49.99)")
conn.commit()

rows = conn.execute("SELECT * FROM products").fetchall()
for r in rows: print(r)
conn.close()

# Clean up demo file
if os.path.exists(db_path): os.remove(db_path)"""}
],
"rw":{
"title":"Building a Sales Transaction Database",
"scenario":"A startup data analyst creates an in-memory SQLite database to prototype reporting queries before moving to PostgreSQL.",
"code":
"""import sqlite3, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE sales (
    id INT, customer TEXT, product TEXT, amount REAL, sale_date TEXT
)""")

customers = ["Alice","Bob","Carol","Dave","Eve"]
products  = ["Widget","Gadget","Doohickey","Gizmo"]
base = datetime.date(2024, 1, 1)

records = [
    (i, random.choice(customers), random.choice(products),
     round(random.uniform(20, 500), 2),
     (base + datetime.timedelta(days=random.randint(0, 180))).isoformat())
    for i in range(1, 1001)
]
conn.executemany("INSERT INTO sales VALUES (?,?,?,?,?)", records)
conn.commit()

row = conn.execute("SELECT COUNT(*), SUM(amount), AVG(amount) FROM sales").fetchone()
print(f"Rows: {row[0]}, Total: ${row[1]:,.2f}, Avg: ${row[2]:.2f}")
conn.close()"""}
},
{
"title":"2. SELECT & WHERE",
"desc":"SELECT retrieves data. WHERE filters rows based on conditions. The foundation of every SQL query.",
"examples":[
{"label":"Basic SELECT and filtering","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (id INT, name TEXT, dept TEXT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?,?,?)", [
    (1,"Alice","Eng",95000),(2,"Bob","Marketing",72000),
    (3,"Carol","Eng",88000),(4,"Dave","HR",65000),(5,"Eve","Marketing",78000),
])

# Select all Engineering employees
rows = conn.execute(
    "SELECT name, salary FROM emp WHERE dept='Eng' ORDER BY salary DESC"
).fetchall()
for r in rows: print(r)
conn.close()"""},
{"label":"LIKE, IN, BETWEEN, IS NULL","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE products (name TEXT, price REAL, category TEXT)")
conn.executemany("INSERT INTO products VALUES (?,?,?)", [
    ("Apple",0.5,"Fruit"),("Avocado",1.5,"Fruit"),("Milk",2.99,"Dairy"),
    ("Butter",4.5,"Dairy"),("Bread",3.29,"Bakery"),("Cake",None,"Bakery"),
])

print(conn.execute("SELECT name FROM products WHERE name LIKE 'A%'").fetchall())
print(conn.execute("SELECT name FROM products WHERE category IN ('Dairy','Bakery')").fetchall())
print(conn.execute("SELECT name FROM products WHERE price BETWEEN 1 AND 4").fetchall())
print(conn.execute("SELECT name FROM products WHERE price IS NULL").fetchall())
conn.close()"""}
],
"rw":{
"title":"Customer Order Filtering for Fulfillment Team",
"scenario":"An e-commerce backend filters pending high-value orders for priority fulfillment processing.",
"code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE orders (
    id INT, customer TEXT, status TEXT, amount REAL, order_date TEXT
)""")
conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", [
    (1,"Alice","shipped",120.0,"2024-01-05"),
    (2,"Bob","pending",80.0,"2024-01-10"),
    (3,"Alice","delivered",250.0,"2024-01-12"),
    (4,"Carol","pending",450.0,"2024-01-15"),
    (5,"Bob","shipped",310.0,"2024-01-18"),
    (6,"Dave","cancelled",90.0,"2024-01-20"),
])

rows = conn.execute("""
    SELECT id, customer, amount, order_date
    FROM orders
    WHERE status IN ('pending','shipped')
      AND amount > 100
    ORDER BY amount DESC
""").fetchall()

print("Priority orders:")
for r in rows: print(f"  #{r[0]} {r[1]:8s} ${r[2]:6.2f} on {r[3]}")
conn.close()"""}
},
{
"title":"3. GROUP BY, Aggregates & HAVING",
"desc":"Aggregate functions (COUNT, SUM, AVG) with GROUP BY summarize data. HAVING filters groups after aggregation.",
"examples":[
{"label":"COUNT, SUM, AVG, MAX","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (region TEXT, rep TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    ("North","Alice",1000),("North","Bob",1500),
    ("South","Carol",800),("South","Dave",1200),
    ("East","Eve",2000),("East","Alice",900),
])

# Aggregates per region
rows = conn.execute("""
    SELECT region,
           COUNT(*)       as reps,
           SUM(amount)    as total,
           ROUND(AVG(amount),0) as avg_amt,
           MAX(amount)    as top
    FROM sales
    GROUP BY region
    ORDER BY total DESC
""").fetchall()
for r in rows: print(r)
conn.close()"""},
{"label":"HAVING to filter groups","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (dept TEXT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?)", [
    ("Eng",120000),("Eng",95000),("Eng",110000),
    ("HR",65000),
    ("Marketing",85000),("Marketing",90000),("Marketing",72000),
])

rows = conn.execute("""
    SELECT dept,
           COUNT(*) as headcount,
           ROUND(AVG(salary), 0) as avg_sal
    FROM emp
    GROUP BY dept
    HAVING COUNT(*) >= 2
    ORDER BY avg_sal DESC
""").fetchall()
for r in rows: print(r)
conn.close()"""}
],
"rw":{
"title":"Monthly Spend Dashboard",
"scenario":"A finance analyst builds a monthly category spending dashboard from raw transaction records.",
"code":
"""import sqlite3, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE txn (user_id INT, category TEXT, amount REAL, date TEXT)")

cats = ["Food","Transport","Shopping","Entertainment","Utilities"]
rows = [
    (random.randint(1,100), random.choice(cats),
     round(random.uniform(5,300),2),
     (datetime.date(2024,1,1)+datetime.timedelta(days=random.randint(0,89))).isoformat())
    for _ in range(2000)
]
conn.executemany("INSERT INTO txn VALUES (?,?,?,?)", rows)

report = conn.execute("""
    SELECT category,
           COUNT(*) as txns,
           ROUND(SUM(amount), 2) as total,
           ROUND(AVG(amount), 2) as avg_amt,
           ROUND(SUM(amount)*100.0 / (SELECT SUM(amount) FROM txn), 1) as pct
    FROM txn
    GROUP BY category
    ORDER BY total DESC
""").fetchall()

print(f"{'Category':15s} {'Txns':>5} {'Total':>10} {'Avg':>8} {'%':>6}")
print("-" * 50)
for r in report:
    print(f"{r[0]:15s} {r[1]:>5} ${r[2]:>9,.2f} ${r[3]:>7.2f} {r[4]:>5.1f}%")
conn.close()"""}
},
{
"title":"4. JOINs",
"desc":"JOINs combine rows from two or more tables. INNER keeps matches only; LEFT keeps all rows from the left table.",
"examples":[
{"label":"INNER JOIN and LEFT JOIN","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE dept (id INT, name TEXT)")
conn.execute("CREATE TABLE emp  (id INT, name TEXT, dept_id INT, salary REAL)")
conn.executemany("INSERT INTO dept VALUES (?,?)", [(1,"Eng"),(2,"HR"),(3,"Sales")])
conn.executemany("INSERT INTO emp VALUES (?,?,?,?)", [
    (1,"Alice",1,100000),(2,"Bob",2,65000),
    (3,"Carol",1,95000),(4,"Dave",3,80000),(5,"Eve",None,75000),
])

print("INNER JOIN (only matched):")
rows = conn.execute("""
    SELECT e.name, d.name as dept, e.salary
    FROM emp e INNER JOIN dept d ON e.dept_id = d.id
""").fetchall()
for r in rows: print(" ", r)

print("\nLEFT JOIN (all employees):")
rows = conn.execute("""
    SELECT e.name, COALESCE(d.name,'Unknown') as dept, e.salary
    FROM emp e LEFT JOIN dept d ON e.dept_id = d.id
""").fetchall()
for r in rows: print(" ", r)
conn.close()"""},
{"label":"Multi-table JOIN with aggregation","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (id INT, name TEXT, city TEXT)")
conn.execute("CREATE TABLE orders    (id INT, cust_id INT, amount REAL)")
conn.executemany("INSERT INTO customers VALUES (?,?,?)", [
    (1,"Alice","NYC"),(2,"Bob","LA"),(3,"Carol","NYC"),(4,"Dave","Chicago"),
])
conn.executemany("INSERT INTO orders VALUES (?,?,?)", [
    (1,1,150),(2,1,200),(3,2,80),(4,3,320),(5,3,100),
])

rows = conn.execute("""
    SELECT c.name, c.city,
           COUNT(o.id) as num_orders,
           COALESCE(SUM(o.amount), 0) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.id = o.cust_id
    GROUP BY c.id
    ORDER BY total_spent DESC
""").fetchall()
for r in rows: print(r)
conn.close()"""}
],
"rw":{
"title":"Inventory & Sales Cross-Reference Report",
"scenario":"A warehouse manager joins product, inventory, and sales tables to identify stock risk for top-selling items.",
"code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
for ddl in [
    "CREATE TABLE products   (id INT, name TEXT, category TEXT, price REAL)",
    "CREATE TABLE inventory  (product_id INT, warehouse TEXT, qty INT)",
    "CREATE TABLE sales_30d  (product_id INT, qty_sold INT)",
]:
    conn.execute(ddl)

conn.executemany("INSERT INTO products VALUES (?,?,?,?)", [
    (1,"Widget","Hardware",9.99),(2,"Gadget","Electronics",49.99),
    (3,"Doohickey","Hardware",19.99),(4,"Gizmo","Electronics",79.99),
])
conn.executemany("INSERT INTO inventory VALUES (?,?,?)", [
    (1,"East",500),(1,"West",300),(2,"East",80),(3,"West",200),(4,"East",50),
])
conn.executemany("INSERT INTO sales_30d VALUES (?,?)", [
    (1,420),(2,75),(3,60),(4,45),
])

rows = conn.execute("""
    SELECT p.name, p.category,
           SUM(i.qty) as stock,
           COALESCE(s.qty_sold, 0) as sold_30d,
           SUM(i.qty) - COALESCE(s.qty_sold, 0) as remaining,
           ROUND(SUM(i.qty) * 1.0 / NULLIF(COALESCE(s.qty_sold,0),0), 1) as weeks_cover
    FROM products p
    JOIN inventory i ON p.id = i.product_id
    LEFT JOIN sales_30d s ON p.id = s.product_id
    GROUP BY p.id, p.name, p.category
    ORDER BY weeks_cover ASC
""").fetchall()

print(f"{'Product':12s} {'Stock':>6} {'Sold':>6} {'Left':>6} {'Wks':>5}")
for r in rows:
    print(f"{r[0]:12s} {r[2]:>6} {r[3]:>6} {r[4]:>6} {str(r[5]):>5}")
conn.close()"""}
},
{
"title":"5. Subqueries & CTEs",
"desc":"Subqueries run a query inside another query. CTEs (WITH) make complex queries readable and reusable.",
"examples":[
{"label":"Correlated subquery and scalar subquery","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (name TEXT, dept TEXT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?,?)", [
    ("Alice","Eng",120000),("Bob","HR",65000),("Carol","Eng",95000),
    ("Dave","Mkt",80000),("Eve","Eng",110000),("Frank","HR",72000),
])

# Employees earning above company average
rows = conn.execute("""
    SELECT name, dept, salary
    FROM emp
    WHERE salary > (SELECT AVG(salary) FROM emp)
    ORDER BY salary DESC
""").fetchall()
print("Above avg salary:", rows)
conn.close()"""},
{"label":"CTE (Common Table Expression)","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INT, cust TEXT, amount REAL, month TEXT)")
conn.executemany("INSERT INTO orders VALUES (?,?,?,?)", [
    (1,"Alice",100,"Jan"),(2,"Bob",200,"Jan"),(3,"Alice",150,"Feb"),
    (4,"Carol",300,"Feb"),(5,"Bob",250,"Mar"),(6,"Alice",400,"Mar"),
])

rows = conn.execute("""
    WITH monthly_totals AS (
        SELECT month, SUM(amount) as total
        FROM orders
        GROUP BY month
    ),
    avg_total AS (
        SELECT AVG(total) as avg_monthly FROM monthly_totals
    )
    SELECT m.month, m.total,
           ROUND(m.total - a.avg_monthly, 2) as vs_avg
    FROM monthly_totals m, avg_total a
    ORDER BY m.month
""").fetchall()
for r in rows: print(r)
conn.close()"""}
],
"rw":{
"title":"Customer Conversion Funnel Analysis",
"scenario":"A product analyst uses CTEs and window functions to compute step-by-step funnel conversion rates.",
"code":
"""import sqlite3, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE user_events (user_id INT, event TEXT, ts TEXT)")

random.seed(5)
funnel = ["signup","view_product","add_to_cart","purchase"]
rows = []
for uid in range(1, 501):
    n = random.randint(1, 4)
    base = datetime.datetime(2024,1,1) + datetime.timedelta(days=random.randint(0,60))
    for ev in funnel[:n]:
        rows.append((uid, ev, (base + datetime.timedelta(hours=random.randint(1,48))).isoformat()))
        base += datetime.timedelta(days=random.randint(0,3))
conn.executemany("INSERT INTO user_events VALUES (?,?,?)", rows)

report = conn.execute("""
    WITH steps AS (
        SELECT event, COUNT(DISTINCT user_id) as users
        FROM user_events
        WHERE event IN ('signup','view_product','add_to_cart','purchase')
        GROUP BY event
    ),
    total AS (SELECT users as top FROM steps WHERE event='signup')
    SELECT event, users,
           ROUND(users * 100.0 / (SELECT top FROM total), 1) as pct_of_signups
    FROM steps
    ORDER BY users DESC
""").fetchall()

print("Conversion Funnel:")
for r in report: print(f"  {r[0]:16s} {r[1]:4d} users  ({r[2]}%)")
conn.close()"""}
},
{
"title":"6. Window Functions",
"desc":"Window functions compute values across a set of rows related to the current row — ranking, running totals, lag/lead.",
"examples":[
{"label":"RANK, ROW_NUMBER, SUM OVER","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (month TEXT, rep TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    ("Jan","Alice",5000),("Jan","Bob",4000),("Jan","Carol",6000),
    ("Feb","Alice",5500),("Feb","Bob",3800),("Feb","Carol",7000),
])

rows = conn.execute("""
    SELECT month, rep, amount,
           RANK()   OVER (PARTITION BY month ORDER BY amount DESC) as rank,
           SUM(amount) OVER (PARTITION BY month) as month_total,
           ROUND(amount * 100.0 / SUM(amount) OVER (PARTITION BY month), 1) as pct
    FROM sales ORDER BY month, rank
""").fetchall()
for r in rows: print(r)
conn.close()"""},
{"label":"LAG, LEAD, running average","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE revenue (week INT, store TEXT, rev REAL)")
conn.executemany("INSERT INTO revenue VALUES (?,?,?)", [
    (1,"A",10000),(2,"A",12000),(3,"A",9000),(4,"A",14000),(5,"A",11000),
    (1,"B",8000),(2,"B",9500),(3,"B",11000),(4,"B",10500),(5,"B",12000),
])

rows = conn.execute("""
    SELECT week, store, rev,
           LAG(rev) OVER (PARTITION BY store ORDER BY week) as prev_rev,
           rev - LAG(rev) OVER (PARTITION BY store ORDER BY week) as wow_change,
           AVG(rev) OVER (PARTITION BY store ORDER BY week
                          ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as ma3
    FROM revenue ORDER BY store, week
""").fetchall()
for r in rows: print(r)
conn.close()"""}
],
"rw":{
"title":"Trading Signal Generation with Price Windows",
"scenario":"A quant uses window functions to compute 3-period moving average and momentum signals for algorithmic trading.",
"code":
"""import sqlite3, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE prices (id INT, symbol TEXT, price REAL, vol INT, date TEXT)")

random.seed(10)
symbols = ["AAPL","GOOG","MSFT"]
rows = []
for sym in symbols:
    p = random.uniform(150, 400)
    for d in range(20):
        p *= (1 + random.gauss(0.001, 0.015))
        date = (datetime.date(2024,1,1)+datetime.timedelta(days=d)).isoformat()
        rows.append((len(rows)+1, sym, round(p,2), random.randint(1000,50000), date))
conn.executemany("INSERT INTO prices VALUES (?,?,?,?,?)", rows)

result = conn.execute("""
    SELECT symbol, date, price,
           ROUND(AVG(price) OVER (PARTITION BY symbol ORDER BY date
                                  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) as ma3,
           price > AVG(price) OVER (PARTITION BY symbol ORDER BY date
                                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as above_ma
    FROM prices
    WHERE symbol = 'AAPL'
    ORDER BY date
    LIMIT 10
""").fetchall()

print(f"{'Date':12s} {'Price':>8} {'MA3':>8} {'Above':>6}")
for r in result: print(f"{r[1]} {r[2]:>8.2f} {r[3]:>8.2f} {'Yes' if r[4] else 'No':>6}")
conn.close()"""}
},
{
"title":"7. UPDATE & DELETE",
"desc":"Modify existing data with UPDATE and remove records with DELETE. Always use WHERE to target specific rows.",
"examples":[
{"label":"UPDATE with conditions","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE inventory (id INT, item TEXT, qty INT, price REAL)")
conn.executemany("INSERT INTO inventory VALUES (?,?,?,?)", [
    (1,"Widget",100,9.99),(2,"Gadget",50,49.99),(3,"Doohickey",200,4.99),
])

# Raise price by 10% for items with qty < 100
conn.execute("UPDATE inventory SET price = ROUND(price * 1.1, 2) WHERE qty < 100")
conn.commit()

rows = conn.execute("SELECT * FROM inventory").fetchall()
for r in rows: print(r)
conn.close()"""},
{"label":"DELETE with subquery","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE logs (id INT, user TEXT, action TEXT, ts TEXT)")
conn.executemany("INSERT INTO logs VALUES (?,?,?,?)", [
    (1,"alice","login","2024-01-01"),(2,"bob","login","2023-06-01"),
    (3,"alice","logout","2024-01-01"),(4,"carol","login","2022-05-01"),
    (5,"bob","purchase","2024-02-01"),
])

# Delete logs older than 2024
conn.execute("DELETE FROM logs WHERE ts < '2024-01-01'")
conn.commit()

count = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
print(f"Remaining logs: {count}")
rows = conn.execute("SELECT * FROM logs").fetchall()
for r in rows: print(r)
conn.close()"""}
],
"rw":{
"title":"Subscription Lifecycle Management",
"scenario":"A SaaS platform automatically expires overdue subscriptions and applies discounts to loyal customers.",
"code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE subscriptions (
    id INT, user TEXT, plan TEXT, price REAL,
    start_date TEXT, end_date TEXT, status TEXT
)""")
conn.executemany("INSERT INTO subscriptions VALUES (?,?,?,?,?,?,?)", [
    (1,"Alice","basic",9.99,"2024-01-01","2024-12-31","active"),
    (2,"Bob","pro",29.99,"2023-01-01","2024-01-15","active"),
    (3,"Carol","basic",9.99,"2024-01-01","2024-06-30","active"),
    (4,"Dave","enterprise",99.99,"2022-01-01","2024-12-31","active"),
])

today = "2024-07-01"
# Expire overdue subscriptions
conn.execute("UPDATE subscriptions SET status='expired' WHERE end_date < ?", (today,))
# Discount loyal customers (>2 years)
conn.execute("""UPDATE subscriptions
               SET price = ROUND(price * 0.85, 2)
               WHERE status='active'
                 AND CAST(strftime('%Y', ?) AS INT) - CAST(strftime('%Y', start_date) AS INT) >= 2
""", (today,))
conn.commit()

rows = conn.execute("SELECT user, plan, price, status FROM subscriptions").fetchall()
print(f"{'User':8s} {'Plan':12s} {'Price':>8} {'Status':>8}")
for r in rows: print(f"{r[0]:8s} {r[1]:12s} ${r[2]:>7.2f} {r[3]:>8}")
conn.close()"""}
},
{
"title":"8. SQLite with Pandas",
"desc":"Pandas integrates seamlessly with SQLite: read SQL results into DataFrames, write DataFrames back to SQL tables.",
"examples":[
{"label":"read_sql and to_sql","code":
"""import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (date TEXT, region TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    ("2024-01-01","North",1200),("2024-01-01","South",800),
    ("2024-01-02","North",950),("2024-01-02","East",1100),
])

# SQL → DataFrame
df = pd.read_sql("SELECT * FROM sales", conn)
print(df)
print(df.groupby("region")["amount"].sum())
conn.close()"""},
{"label":"Write DataFrame to SQL","code":
"""import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect(":memory:")

df = pd.DataFrame({
    "date":     pd.date_range("2024-01-01", periods=30).astype(str),
    "value":    np.random.randn(30).cumsum() + 100,
    "category": np.random.choice(["A","B","C"], 30),
})
df.to_sql("timeseries", conn, index=False, if_exists="replace")

result = pd.read_sql("""
    SELECT category, COUNT(*) as n, ROUND(AVG(value),2) as avg_val
    FROM timeseries GROUP BY category ORDER BY avg_val DESC
""", conn)
print(result)
conn.close()"""}
],
"rw":{
"title":"Multi-Source Analytics Report",
"scenario":"A data analyst joins normalized SQL tables and loads the result into pandas for visualization and export.",
"code":
"""import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect(":memory:")

customers = pd.DataFrame({
    "id":      range(1, 101),
    "segment": np.random.choice(["retail","wholesale","online"], 100),
    "region":  np.random.choice(["North","South","East","West"], 100),
})
transactions = pd.DataFrame({
    "customer_id": np.random.randint(1, 101, 2000),
    "product":     np.random.choice(["A","B","C","D"], 2000),
    "amount":      np.random.uniform(10, 500, 2000).round(2),
})

customers.to_sql("customers", conn, index=False)
transactions.to_sql("transactions", conn, index=False)

report = pd.read_sql("""
    SELECT c.segment, c.region,
           COUNT(DISTINCT t.customer_id) as customers,
           ROUND(SUM(t.amount), 2) as revenue,
           ROUND(AVG(t.amount), 2) as avg_order
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    GROUP BY c.segment, c.region
    ORDER BY revenue DESC
    LIMIT 8
""", conn)
print(report.to_string(index=False))
conn.close()"""}
},
{
"title":"9. Indexes & Performance",
"desc":"Indexes dramatically speed up queries on large tables by avoiding full table scans. Use them on WHERE and JOIN columns.",
"examples":[
{"label":"Creating and measuring index benefit","code":
"""import sqlite3, time

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE events (id INT, user_id INT, event_type TEXT, ts TEXT)")

import random
rows = [(i, random.randint(1,10000), random.choice(["click","view","buy"]),
         f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}")
        for i in range(200000)]
conn.executemany("INSERT INTO events VALUES (?,?,?,?)", rows)
conn.commit()

t0 = time.time()
conn.execute("SELECT COUNT(*) FROM events WHERE user_id=42").fetchone()
t_no_idx = time.time() - t0

conn.execute("CREATE INDEX idx_user ON events(user_id)")

t0 = time.time()
conn.execute("SELECT COUNT(*) FROM events WHERE user_id=42").fetchone()
t_with_idx = time.time() - t0

print(f"No index:   {t_no_idx*1000:.2f}ms")
print(f"With index: {t_with_idx*1000:.2f}ms")
print(f"Speedup:    {t_no_idx/max(t_with_idx,0.0001):.0f}x")
conn.close()"""},
{"label":"EXPLAIN QUERY PLAN","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INT, cust TEXT, status TEXT, amount REAL)")
conn.execute("CREATE INDEX idx_status ON orders(status)")
conn.execute("CREATE INDEX idx_cust   ON orders(cust)")

plan = conn.execute("""
    EXPLAIN QUERY PLAN
    SELECT cust, SUM(amount) FROM orders
    WHERE status='pending'
    GROUP BY cust
""").fetchall()
print("Query plan:")
for row in plan: print(" ", row)
conn.close()"""}
],
"rw":{
"title":"E-Commerce Order Analytics with Compound Indexes",
"scenario":"A backend engineer adds compound indexes to reduce report query time from seconds to milliseconds.",
"code":
"""import sqlite3, time, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE orders (
    id INT, customer_id INT, product_id INT,
    status TEXT, amount REAL, created_at TEXT
)""")
conn.execute("CREATE TABLE products (id INT PRIMARY KEY, name TEXT, category TEXT)")

conn.executemany("INSERT INTO products VALUES (?,?,?)", [
    (i, f"Product{i}", random.choice(["Electronics","Food","Clothing","Hardware"]))
    for i in range(1, 201)
])

rows = [(i, random.randint(1,5000), random.randint(1,200),
         random.choice(["pending","shipped","delivered"]),
         round(random.uniform(10,1000),2),
         (datetime.date(2024,1,1)+datetime.timedelta(days=random.randint(0,90))).isoformat())
        for i in range(1,50001)]
conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", rows)

# Add compound indexes
for idx in [
    "CREATE INDEX idx_status_date ON orders(status, created_at)",
    "CREATE INDEX idx_prod ON orders(product_id)",
]:
    conn.execute(idx)

t0 = time.time()
result = conn.execute("""
    SELECT p.category, o.status, COUNT(*) as cnt, ROUND(SUM(o.amount),2) as revenue
    FROM orders o JOIN products p ON o.product_id = p.id
    WHERE o.status != 'pending'
    GROUP BY p.category, o.status
    ORDER BY revenue DESC LIMIT 8
""").fetchall()
print(f"Query: {(time.time()-t0)*1000:.1f}ms  ({len(result)} rows)")
for r in result[:4]: print(f"  {r[0]:14s} | {r[1]:10s} | {r[2]:>5d} | ${r[3]:>10,.2f}")
conn.close()"""}
},
{
"title":"10. Recursive CTEs & Advanced Patterns",
"desc":"Recursive CTEs traverse hierarchical data (org charts, categories). Advanced patterns include UPSERT and JSON.",
"examples":[
{"label":"Recursive CTE for org hierarchy","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (id INT, name TEXT, mgr_id INT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?,?,?)", [
    (1,"CEO",None,300000),(2,"CTO",1,200000),(3,"CFO",1,190000),
    (4,"Dev Lead",2,130000),(5,"Dev1",4,100000),(6,"Dev2",4,95000),
    (7,"Finance1",3,80000),
])

rows = conn.execute("""
    WITH RECURSIVE org AS (
        SELECT id, name, mgr_id, 0 AS depth
        FROM emp WHERE mgr_id IS NULL
        UNION ALL
        SELECT e.id, e.name, e.mgr_id, o.depth + 1
        FROM emp e JOIN org o ON e.mgr_id = o.id
    )
    SELECT depth, name FROM org ORDER BY depth, name
""").fetchall()
for d, name in rows: print("  " * d + name)
conn.close()"""},
{"label":"UPSERT (INSERT OR REPLACE)","code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TEXT
)""")

def upsert(key, value, ts):
    conn.execute("""
        INSERT INTO config (key, value, updated_at) VALUES (?,?,?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
    """, (key, value, ts))
    conn.commit()

upsert("theme",      "dark",      "2024-01-01")
upsert("page_size",  "25",        "2024-01-01")
upsert("theme",      "light",     "2024-03-01")  # update existing

rows = conn.execute("SELECT * FROM config").fetchall()
for r in rows: print(r)
conn.close()"""}
],
"rw":{
"title":"Product Category Tree Navigation",
"scenario":"An e-commerce platform uses a recursive CTE to build a full category breadcrumb path for search indexing.",
"code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE categories (id INT PRIMARY KEY, name TEXT, parent_id INT)")
conn.executemany("INSERT INTO categories VALUES (?,?,?)", [
    (1,"All",None),(2,"Electronics",1),(3,"Computers",2),
    (4,"Laptops",3),(5,"Gaming Laptops",4),(6,"Ultrabooks",4),
    (7,"Phones",2),(8,"Android",7),(9,"Clothing",1),(10,"Men",9),
])

rows = conn.execute("""
    WITH RECURSIVE tree AS (
        SELECT id, name, parent_id,
               CAST(name AS TEXT) as path, 0 as depth
        FROM categories WHERE parent_id IS NULL
        UNION ALL
        SELECT c.id, c.name, c.parent_id,
               t.path || ' > ' || c.name, t.depth + 1
        FROM categories c JOIN tree t ON c.parent_id = t.id
    )
    SELECT id, depth, path
    FROM tree
    ORDER BY path
""").fetchall()

for r in rows:
    print(f"  {'  '*r[1]}[{r[0]}] {r[2]}")
conn.close()"""}
}
]},  # end SQL

]  # end GUIDES (partial — continued in part 2)


# ─── Write partial guides, then extend in generate_part2.py ──────────────────
print(f"Loaded {len(GUIDES)} guides so far...")
