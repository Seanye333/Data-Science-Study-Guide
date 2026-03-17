#!/usr/bin/env python3
"""Generate Matplotlib study guide — notebook + HTML."""

import matplotlib
matplotlib.use('Agg')

import json, pathlib
from html import escape as esc

BASE   = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\03_matplotlib")
BASE.mkdir(parents=True, exist_ok=True)
ACCENT = "#58a6ff"
EMOJI  = "📊"
TITLE  = "Matplotlib"

def make_html(sections):
    nav = "\n    ".join(
        f'<li><a href="#s{i}" onclick="act(this,event)">{esc(s["title"])}</a></li>'
        for i, s in enumerate(sections))
    cards = ""
    for i, s in enumerate(sections):
        blks = ""
        for j, ex in enumerate(s.get("examples", [])):
            cid = f"c{i}_{j}"
            blks += (f'<div class="code-block"><div class="ch"><span>{esc(ex.get("label","Example"))}</span>'
                     f'<button onclick="cp(\'{cid}\')">Copy</button></div>'
                     f'<pre><code id="{cid}" class="language-python">{esc(ex["code"])}</code></pre></div>')
        rw = s.get("rw", {})
        rw_html = (f'<div class="rw"><div class="rh">&#x1F4BC; Real-World: {esc(rw["title"])}</div>'
                   f'<div class="rd">{esc(rw["scenario"])}</div>'
                   f'<pre><code class="language-python">{esc(rw["code"])}</code></pre></div>') if rw else ""
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
        cards += (f'<div class="topic" id="s{i}"><div class="th" onclick="tog(this)"><span>{esc(s["title"])}</span>'
                  f'<span class="arr">&#9660;</span></div><div class="tb"><p class="desc">{esc(s.get("desc",""))}</p>'
                  f'{blks}{rw_html}{practice_html}</div></div>')
    n = len(sections)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE} Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>:root{{--bg:#0f1117;--sb:#161b22;--card:#1c2128;--brd:#30363d;--txt:#c9d1d9;--mut:#8b949e;--acc:{ACCENT}}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{display:flex;min-height:100vh;background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px}}
.sidebar{{width:260px;min-height:100vh;background:var(--sb);border-right:1px solid var(--brd);position:sticky;top:0;height:100vh;overflow-y:auto;flex-shrink:0}}
.sbh{{padding:20px;border-bottom:1px solid var(--brd)}}.sbh h2{{font-size:1.05rem;color:var(--acc)}}.sbh p{{font-size:.8rem;color:var(--mut);margin-top:3px}}
#q{{width:100%;padding:7px 10px;background:#0d1117;border:1px solid var(--brd);border-radius:6px;color:var(--txt);font-size:.84rem;margin-top:10px}}#q:focus{{outline:none;border-color:var(--acc)}}
.nav-list{{list-style:none;padding:6px 0}}.nav-list li a{{display:block;padding:7px 18px;color:var(--mut);text-decoration:none;font-size:.84rem;border-left:3px solid transparent;transition:.15s}}
.nav-list li a:hover,.nav-list li a.active{{color:var(--txt);border-left-color:var(--acc);background:rgba(255,255,255,.03)}}
.main{{flex:1;padding:32px 40px;max-width:880px}}.pt{{font-size:2rem;font-weight:700;color:var(--acc);margin-bottom:6px}}.ps{{color:var(--mut);margin-bottom:28px}}
.topic{{background:var(--card);border:1px solid var(--brd);border-radius:8px;margin-bottom:14px;overflow:hidden}}
.th{{display:flex;justify-content:space-between;align-items:center;padding:13px 18px;cursor:pointer;user-select:none}}.th:hover{{background:rgba(255,255,255,.04)}}
.th>span:first-child{{font-weight:600}}.arr{{color:var(--mut);transition:transform .2s}}.tb{{display:none;padding:18px;border-top:1px solid var(--brd)}}.tb.open{{display:block}}.arr.open{{transform:rotate(180deg)}}
.desc{{color:var(--mut);margin-bottom:14px;line-height:1.6;font-size:.92rem}}.code-block{{margin-bottom:14px;border:1px solid var(--brd);border-radius:6px;overflow:hidden}}
.ch{{display:flex;justify-content:space-between;padding:7px 12px;background:#161b22;font-size:.78rem;color:var(--mut)}}.ch button{{background:0;border:1px solid var(--brd);color:var(--mut);padding:2px 9px;border-radius:4px;cursor:pointer;font-size:.73rem}}.ch button:hover{{color:var(--txt);border-color:var(--acc)}}
pre{{margin:0}}pre code{{font-size:.83rem;padding:13px!important}}.rw{{background:#0d2818;border:1px solid #238636;border-radius:6px;padding:15px;margin-top:6px}}
.rh{{font-weight:600;color:#3fb950;margin-bottom:7px}}.rd{{color:#7ee787;font-size:.84rem;margin-bottom:11px;line-height:1.5}}
.practice{{background:#0d1b2a;border:1px solid #388bfd;border-radius:6px;padding:15px;margin-top:8px}}
.ph{{font-weight:600;color:#58a6ff;margin-bottom:7px}}
.pd{{color:#79c0ff;font-size:.84rem;margin-bottom:11px;line-height:1.5}}</style></head><body>
<aside class="sidebar"><div class="sbh"><h2>{EMOJI} {TITLE}</h2><p>Study Guide &bull; {n} topics</p>
<input id="q" placeholder="Search..." oninput="filt(this.value)"></div>
<ul class="nav-list" id="nl">{nav}</ul></aside>
<main class="main"><h1 class="pt">{EMOJI} {TITLE}</h1><p class="ps">{n} topics &bull; Click any card to expand</p>{cards}</main>
<script>hljs.highlightAll();
function tog(h){{var b=h.nextElementSibling,a=h.querySelector('.arr');b.classList.toggle('open');a.classList.toggle('open');}}
function act(el,e){{if(e)e.preventDefault();document.querySelectorAll('.nav-list a').forEach(a=>a.classList.remove('active'));el.classList.add('active');}}
function filt(q){{document.querySelectorAll('#nl li').forEach(li=>{{li.style.display=li.textContent.toLowerCase().includes(q.toLowerCase())?'':'none';}});}}
function cp(id){{navigator.clipboard.writeText(document.getElementById(id).innerText).catch(()=>{{}});}}
document.addEventListener('DOMContentLoaded',()=>{{var fh=document.querySelector('.th');if(fh)fh.click();var fa=document.querySelector('.nav-list a');if(fa)fa.classList.add('active');}});
</script></body></html>"""

def make_nb(sections):
    cells=[]; n=[0]
    def nid(): n[0]+=1; return f"{n[0]:04d}"
    def md(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"markdown","id":nid(),"metadata":{},"source":s}
    def code(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"code","execution_count":None,"id":nid(),"metadata":{},"outputs":[],"source":s}
    cells.append(md(f"# {TITLE} Study Guide\n\nHands-on visualization guide. Run cells in Jupyter to see the plots."))
    for i,s in enumerate(sections,1):
        cells.append(md(f"## {i}. {s['title']}\n\n{s.get('desc','')}"))
        for ex in s.get("examples",[]):
            if ex.get("label"): cells.append(md(f"**{ex['label']}**"))
            cells.append(code(ex["code"]))
        rw=s.get("rw")
        if rw:
            cells.append(md(f"### Real-World: {rw['title']}\n\n> {rw['scenario']}"))
            cells.append(code(rw["code"]))
        practice = s.get("practice")
        if practice:
            cells.append(md(f"### 🏋️ Practice: {practice['title']}\n\n{practice['desc']}"))
            cells.append(code(practice["starter"]))
            for ex in practice.get("examples", []):
                if ex.get("label"): cells.append(md(f"**{ex['label']}**"))
                cells.append(code(ex["code"]))
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.11.0"}},"nbformat":4,"nbformat_minor":5}


SECTIONS = [

{
"title": "1. Line Plot",
"desc": "The most basic Matplotlib plot. Use plt.plot() for time series, trends, and continuous data. Always label axes and add a title.",
"examples": [
{"label": "Simple line plot", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y, color='steelblue', linewidth=2, label='sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Sine Wave')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('line_simple.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved line_simple.png')"""},
{"label": "Multiple lines", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)

plt.figure(figsize=(8, 4))
plt.plot(x, np.sin(x),     label='sin(x)',    linewidth=2)
plt.plot(x, np.cos(x),     label='cos(x)',    linewidth=2, linestyle='--')
plt.plot(x, np.sin(2 * x), label='sin(2x)',   linewidth=1, alpha=0.7)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Trig Functions')
plt.legend()
plt.axhline(0, color='gray', linewidth=0.8)
plt.tight_layout()
plt.savefig('line_multi.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved line_multi.png')"""},
{"label": "Line styles, markers, and fill_between", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
x = np.linspace(0, 10, 50)
y1 = np.sin(x) + np.random.randn(50) * 0.1
y2 = np.cos(x) + np.random.randn(50) * 0.1
err = np.abs(np.random.randn(50) * 0.15)

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(x, y1, 'o-', color='steelblue', markersize=4, linewidth=1.5, label='Signal A')
ax.plot(x, y2, 's--', color='tomato', markersize=4, linewidth=1.5, label='Signal B')
# Confidence band around Signal A
ax.fill_between(x, y1 - err, y1 + err, alpha=0.2, color='steelblue', label='±1σ band')
ax.axhline(0, color='gray', linewidth=0.7, linestyle=':')
ax.set_xlabel('Time'); ax.set_ylabel('Amplitude')
ax.set_title('Line Styles, Markers & Confidence Band')
ax.legend(fontsize=9); ax.grid(True, alpha=0.25)
plt.tight_layout()
plt.savefig('line_styles.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved line_styles.png')"""},
{"label": "Step plot and errorbar", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(4)
x = np.arange(1, 13)
y = np.array([5, 8, 6, 10, 13, 11, 15, 14, 17, 16, 20, 22], dtype=float)
yerr = np.random.uniform(0.5, 2.0, 12)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Step plot — useful for histograms, digital signals, and discrete data
ax1.step(x, y, where='mid', color='steelblue', linewidth=2, label='Step (mid)')
ax1.step(x, y + 3, where='post', color='tomato', linewidth=2,
         linestyle='--', label='Step (post)')
ax1.fill_between(x, y, step='mid', alpha=0.15, color='steelblue')
ax1.set_xlabel('Month'); ax1.set_ylabel('Value')
ax1.set_title('Step Plot Variants')
ax1.legend(fontsize=9); ax1.grid(True, alpha=0.25)

# Errorbar plot — shows measurement uncertainty
ax2.errorbar(x, y, yerr=yerr, fmt='o-', color='#2ecc71', ecolor='gray',
             elinewidth=1.5, capsize=4, capthick=1.5, linewidth=2,
             markersize=6, markerfacecolor='white', markeredgewidth=2,
             label='Mean ± std')
ax2.set_xlabel('Month'); ax2.set_ylabel('Measurement')
ax2.set_title('Errorbar Plot')
ax2.legend(fontsize=9); ax2.grid(True, alpha=0.25)

plt.tight_layout()
plt.savefig('line_step_errorbar.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved line_step_errorbar.png')"""}
],
"practice": {
"title": "Multiple Lines with Different Styles",
"desc": "Plot sin(x), sin(2x), and sin(3x) on the same axes over [0, 2π]. Each line should use a different color, linestyle, and marker. Add a legend, axis labels, title, and a horizontal dashed line at y=0. Save the figure as 'practice_lines.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)

fig, ax = plt.subplots(figsize=(9, 4))

# TODO: plot sin(x) — solid line, circle markers, steelblue
# ax.plot(x, np.sin(x), ...)

# TODO: plot sin(2x) — dashed line, square markers, tomato
# ax.plot(x, np.sin(2*x), ...)

# TODO: plot sin(3x) — dotted line, triangle markers, green
# ax.plot(x, np.sin(3*x), ...)

# TODO: add horizontal dashed line at y=0
# ax.axhline(...)

# TODO: labels, title, legend, grid
ax.set_xlabel('x')
ax.set_ylabel('y')
# ax.set_title(...)
# ax.legend()
# ax.grid(...)

plt.tight_layout()
# TODO: plt.savefig('practice_lines.png', dpi=100, bbox_inches='tight')
plt.close()
print('Done')"""
},
"rw": {
"title": "Website Traffic Trend",
"scenario": "A marketing analyst plots 30-day daily visitor counts with a 7-day moving average to spot trends.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
days    = np.arange(1, 31)
traffic = 1000 + np.cumsum(np.random.randn(30) * 50) + np.random.randn(30) * 80
ma7     = np.convolve(traffic, np.ones(7)/7, mode='same')

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(days, traffic, alpha=0.4, color='steelblue', label='Daily visitors')
ax.plot(days, ma7,     color='steelblue', linewidth=2.5, label='7-day MA')
ax.fill_between(days, traffic, alpha=0.1, color='steelblue')
ax.set_xlabel('Day of Month')
ax.set_ylabel('Visitors')
ax.set_title('Website Traffic — January 2024')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('traffic_trend.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved traffic_trend.png')"""}
},

{
"title": "2. Bar Chart",
"desc": "Bar charts compare discrete categories. Use plt.bar() for vertical and plt.barh() for horizontal. Add value labels for clarity.",
"examples": [
{"label": "Vertical bar chart", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

categories = ['Python', 'JavaScript', 'Java', 'C++', 'Rust']
values     = [67.4, 63.6, 35.4, 24.1, 13.2]
colors     = ['#4C72B0','#DD8452','#55A868','#C44E52','#8172B2']

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=0.5)

# Add value labels on top
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val}%', ha='center', va='bottom', fontsize=9)

ax.set_ylabel('Popularity (%)')
ax.set_title('Most Popular Programming Languages 2024')
ax.set_ylim(0, 80)
ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('bar_vertical.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved bar_vertical.png')"""},
{"label": "Grouped and stacked bar chart", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

quarters = ['Q1', 'Q2', 'Q3', 'Q4']
product_a = [120, 150, 180, 210]
product_b = [80,  95,  110, 130]
x = np.arange(len(quarters))
w = 0.35

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Grouped
axes[0].bar(x - w/2, product_a, w, label='Product A', color='#4C72B0')
axes[0].bar(x + w/2, product_b, w, label='Product B', color='#DD8452')
axes[0].set_xticks(x); axes[0].set_xticklabels(quarters)
axes[0].set_title('Grouped'); axes[0].legend()

# Stacked
axes[1].bar(quarters, product_a, label='Product A', color='#4C72B0')
axes[1].bar(quarters, product_b, bottom=product_a, label='Product B', color='#DD8452')
axes[1].set_title('Stacked'); axes[1].legend()

plt.tight_layout()
plt.savefig('bar_grouped_stacked.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved bar_grouped_stacked.png')"""},
{"label": "Horizontal bar chart with value labels", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

skills  = ['Python', 'SQL', 'Machine Learning', 'Data Viz', 'Statistics', 'Deep Learning']
scores  = [92, 85, 78, 70, 65, 55]
colors  = ['#4C72B0' if s >= 80 else '#DD8452' if s >= 65 else '#C44E52' for s in scores]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(skills, scores, color=colors, edgecolor='white', linewidth=0.5)

for bar, val in zip(bars, scores):
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val}%', va='center', fontsize=9)

ax.set_xlabel('Proficiency Score (%)')
ax.set_title('Data Science Skill Assessment')
ax.set_xlim(0, 105)
ax.axvline(80, color='gray', linestyle='--', linewidth=1, alpha=0.6, label='Expert threshold')
ax.legend(fontsize=9); ax.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('bar_horizontal.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved bar_horizontal.png')"""},
{"label": "Bar chart with error bars and significance markers", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(21)
conditions = ['Control', 'Treatment A', 'Treatment B', 'Treatment C']
means  = np.array([45.2, 52.7, 61.3, 58.9])
errors = np.array([3.1,  4.2,  3.8,  4.5])   # standard deviations
colors = ['#8172B2', '#4C72B0', '#55A868', '#DD8452']

fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(conditions))

bars = ax.bar(x, means, yerr=errors, color=colors, edgecolor='white',
              linewidth=0.5, capsize=6, error_kw=dict(elinewidth=1.5, ecolor='black'))

# Add significance stars between bars
pairs = [(0, 2, '***'), (1, 2, '*')]   # (bar_i, bar_j, label)
y_max = (means + errors).max()
for i, j, sig in pairs:
    y = y_max + 4 + pairs.index((i, j, sig)) * 5
    ax.annotate('', xy=(j, y), xytext=(i, y),
                arrowprops=dict(arrowstyle='-', color='black', lw=1.2))
    ax.text((i + j) / 2, y + 0.3, sig, ha='center', va='bottom', fontsize=11)

# Value labels above each bar
for bar, m, e in zip(bars, means, errors):
    ax.text(bar.get_x() + bar.get_width()/2, m + e + 0.8,
            f'{m:.1f}', ha='center', va='bottom', fontsize=9)

ax.set_xticks(x); ax.set_xticklabels(conditions)
ax.set_ylabel('Response Score'); ax.set_title('Experimental Results with Error Bars')
ax.set_ylim(0, y_max + 18); ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('bar_errorbars.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved bar_errorbars.png')"""}
],
"practice": {
"title": "Grouped Bar Chart",
"desc": "Create a grouped bar chart comparing sales of 3 products (A, B, C) across 4 quarters (Q1-Q4). Use distinct colors per product, offset the bars within each group, add value labels on top, and include a legend. Save as 'practice_grouped_bar.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

quarters  = ['Q1', 'Q2', 'Q3', 'Q4']
product_a = [45, 60, 55, 80]
product_b = [30, 45, 70, 65]
product_c = [20, 35, 40, 55]

x = np.arange(len(quarters))
w = 0.25   # bar width

fig, ax = plt.subplots(figsize=(9, 5))

# TODO: plot three groups of bars, offset by -w, 0, +w
# bars_a = ax.bar(x - w, product_a, w, label='Product A', color='#4C72B0')
# bars_b = ax.bar(x,     product_b, w, label='Product B', color='#DD8452')
# bars_c = ax.bar(x + w, product_c, w, label='Product C', color='#55A868')

# TODO: add value labels on top of each bar
# for bars in [bars_a, bars_b, bars_c]:
#     for bar in bars:
#         ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
#                 str(int(bar.get_height())), ha='center', va='bottom', fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels(quarters)
# TODO: ax.set_xlabel(...), ax.set_ylabel(...), ax.set_title(...)
# TODO: ax.legend()
ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
# TODO: plt.savefig('practice_grouped_bar.png', dpi=100, bbox_inches='tight')
plt.close()
print('Done')"""
},
"rw": {
"title": "Quarterly Sales by Region",
"scenario": "A sales director compares quarterly revenue across four regions with a horizontal bar chart for a board presentation.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

regions = ['APAC', 'EMEA', 'LATAM', 'North America']
q1 = [2.1, 3.4, 1.2, 5.6]
q2 = [2.5, 3.8, 1.5, 6.1]
y  = np.arange(len(regions))
h  = 0.35

fig, ax = plt.subplots(figsize=(9, 4))
b1 = ax.barh(y + h/2, q1, h, label='Q1 2024', color='#4C72B0')
b2 = ax.barh(y - h/2, q2, h, label='Q2 2024', color='#55A868')

for bar in list(b1) + list(b2):
    w = bar.get_width()
    ax.text(w + 0.05, bar.get_y() + bar.get_height()/2,
            f'${w:.1f}M', va='center', fontsize=8)

ax.set_yticks(y); ax.set_yticklabels(regions)
ax.set_xlabel('Revenue (USD millions)')
ax.set_title('Q1 vs Q2 2024 Revenue by Region')
ax.legend(); ax.grid(True, axis='x', alpha=0.3)
ax.set_xlim(0, 8)
plt.tight_layout()
plt.savefig('bar_region.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved bar_region.png')"""}
},

{
"title": "3. Scatter Plot",
"desc": "Scatter plots reveal relationships between two numeric variables. Control color, size, and alpha to encode extra dimensions.",
"examples": [
{"label": "Basic scatter and color mapping", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.random.randn(200)
y = 0.7 * x + np.random.randn(200) * 0.6

fig, ax = plt.subplots(figsize=(6, 5))
sc = ax.scatter(x, y, c=y, cmap='RdYlGn', alpha=0.7, edgecolors='white', linewidth=0.3)
plt.colorbar(sc, label='y value')

# Trend line
m, b = np.polyfit(x, y, 1)
xline = np.linspace(x.min(), x.max(), 100)
ax.plot(xline, m * xline + b, 'k--', linewidth=1.5, label=f'y={m:.2f}x+{b:.2f}')

ax.set_xlabel('X'); ax.set_ylabel('Y')
ax.set_title('Scatter with Trend Line')
ax.legend()
plt.tight_layout()
plt.savefig('scatter_basic.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved scatter_basic.png')"""},
{"label": "Bubble chart (size as 3rd dimension)", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(7)
n = 20
x    = np.random.uniform(10, 100, n)
y    = np.random.uniform(5, 50, n)
size = np.random.uniform(50, 800, n)   # bubble size
color= np.random.rand(n)

fig, ax = plt.subplots(figsize=(7, 5))
sc = ax.scatter(x, y, s=size, c=color, cmap='viridis', alpha=0.6,
                edgecolors='white', linewidth=0.5)
plt.colorbar(sc, label='Category')
ax.set_xlabel('Revenue ($K)'); ax.set_ylabel('Profit Margin (%)')
ax.set_title('Product Portfolio — Bubble Chart')
plt.tight_layout()
plt.savefig('scatter_bubble.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved scatter_bubble.png')"""},
{"label": "Color-mapped scatter with categorical legend", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(3)
n_per_class = 80
classes = ['Class A', 'Class B', 'Class C']
centers = [(-2, -2), (0, 2), (3, 0)]
colors  = ['#e74c3c', '#3498db', '#2ecc71']

fig, ax = plt.subplots(figsize=(7, 6))
for cls, center, color in zip(classes, centers, colors):
    x = np.random.randn(n_per_class) * 0.8 + center[0]
    y = np.random.randn(n_per_class) * 0.8 + center[1]
    ax.scatter(x, y, c=color, label=cls, alpha=0.65,
               edgecolors='white', linewidth=0.4, s=50)

ax.set_xlabel('Feature 1'); ax.set_ylabel('Feature 2')
ax.set_title('Multi-Class Scatter Plot')
ax.legend(title='Class', framealpha=0.8)
ax.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig('scatter_classes.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved scatter_classes.png')"""},
{"label": "Hexbin density plot with colorbar and size scaling", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(17)
n = 5000
# Two overlapping Gaussian clusters
x = np.concatenate([np.random.randn(n) * 1.2 - 1,
                    np.random.randn(n) * 0.8 + 2])
y = np.concatenate([np.random.randn(n) * 1.5 + 0.5,
                    np.random.randn(n) * 1.0 - 1])

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Hexbin — handles large datasets where individual points overlap
hb = axes[0].hexbin(x, y, gridsize=40, cmap='YlOrRd', mincnt=1)
plt.colorbar(hb, ax=axes[0], label='Count per bin')
axes[0].set_xlabel('X'); axes[0].set_ylabel('Y')
axes[0].set_title('Hexbin Density (gridsize=40)')

# Scatter with size proportional to local density (estimated via 2D hist)
H, xedges, yedges = np.histogram2d(x, y, bins=30)
xi = np.searchsorted(xedges, x, side='right').clip(1, H.shape[0]) - 1
yi = np.searchsorted(yedges, y, side='right').clip(1, H.shape[1]) - 1
density = H[xi, yi]

sc = axes[1].scatter(x[::5], y[::5], c=density[::5], s=density[::5] * 0.4 + 4,
                     cmap='plasma', alpha=0.5, edgecolors='none')
plt.colorbar(sc, ax=axes[1], label='Local density')
axes[1].set_xlabel('X'); axes[1].set_ylabel('Y')
axes[1].set_title('Scatter: Size & Color = Density')

plt.tight_layout()
plt.savefig('scatter_hexbin_density.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved scatter_hexbin_density.png')"""}
],
"practice": {
"title": "Color-Mapped Scatter with Colorbar",
"desc": "Generate 300 random (x, y) points where y = 0.5*x + noise. Color each point by its distance from the origin (sqrt(x²+y²)) using the 'plasma' colormap. Add a colorbar labeled 'Distance from origin', a regression line, axis labels, and a title. Save as 'practice_scatter.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.random.randn(300)
y = 0.5 * x + np.random.randn(300) * 0.8

# TODO: compute distance from origin for each point
# dist = np.sqrt(x**2 + y**2)

fig, ax = plt.subplots(figsize=(7, 6))

# TODO: scatter with c=dist, cmap='plasma', alpha=0.7, edgecolors='white'
# sc = ax.scatter(x, y, c=dist, ...)
# TODO: plt.colorbar(sc, label='Distance from origin')

# TODO: fit and plot regression line
# m, b = np.polyfit(x, y, 1)
# xline = np.linspace(x.min(), x.max(), 100)
# ax.plot(xline, m * xline + b, 'k--', linewidth=1.5, label=f'fit')

ax.set_xlabel('X')
ax.set_ylabel('Y')
# TODO: ax.set_title(...)
# TODO: ax.legend()
plt.tight_layout()
# TODO: plt.savefig('practice_scatter.png', dpi=100, bbox_inches='tight')
plt.close()
print('Done')"""
},
"rw": {
"title": "Housing Price vs. Square Footage",
"scenario": "A real estate analyst visualizes the relationship between house size and price, coloring by neighborhood.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(10)
neighborhoods = ['Downtown', 'Suburbs', 'Rural']
colors_map    = {'Downtown': '#e74c3c', 'Suburbs': '#3498db', 'Rural': '#2ecc71'}

fig, ax = plt.subplots(figsize=(9, 5))

for nbhd in neighborhoods:
    n    = 60
    sqft = np.random.normal({'Downtown':1200,'Suburbs':1800,'Rural':2500}[nbhd], 200, n)
    base = {'Downtown':600000,'Suburbs':350000,'Rural':180000}[nbhd]
    price= base + sqft * np.random.uniform(150,250) + np.random.randn(n) * 30000
    ax.scatter(sqft, price/1000, label=nbhd, alpha=0.6,
               color=colors_map[nbhd], edgecolors='white', linewidth=0.3, s=40)

ax.set_xlabel('Square Footage')
ax.set_ylabel('Price ($K)')
ax.set_title('House Price vs. Size by Neighborhood')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('scatter_housing.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved scatter_housing.png')"""}
},

{
"title": "4. Histogram",
"desc": "Histograms show the distribution of a single variable. Control bins and density to compare distributions or estimate PDFs.",
"examples": [
{"label": "Basic histogram with density", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.normal(170, 10, 1000)   # heights in cm

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(data, bins=30, density=True, color='steelblue',
        edgecolor='white', linewidth=0.4, alpha=0.7, label='Data')

# Overlay normal PDF manually (no scipy needed)
xr = np.linspace(data.min(), data.max(), 200)
pdf = (1 / (data.std() * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xr - data.mean()) / data.std())**2)
ax.plot(xr, pdf, color='navy', linewidth=2, label='Normal PDF')

ax.axvline(data.mean(), color='red', linestyle='--', label=f'Mean={data.mean():.1f}')
ax.set_xlabel('Height (cm)'); ax.set_ylabel('Density')
ax.set_title('Height Distribution'); ax.legend()
plt.tight_layout()
plt.savefig('hist_basic.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved hist_basic.png')"""},
{"label": "Overlapping histograms for comparison", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
group_a = np.random.normal(100, 15, 500)
group_b = np.random.normal(115, 12, 500)

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(group_a, bins=30, alpha=0.6, label='Group A', color='steelblue', edgecolor='white')
ax.hist(group_b, bins=30, alpha=0.6, label='Group B', color='tomato',    edgecolor='white')
ax.axvline(group_a.mean(), color='steelblue', linestyle='--', linewidth=1.5)
ax.axvline(group_b.mean(), color='tomato',    linestyle='--', linewidth=1.5)
ax.set_xlabel('Score'); ax.set_ylabel('Count')
ax.set_title('Score Distribution by Group')
ax.legend()
plt.tight_layout()
plt.savefig('hist_compare.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved hist_compare.png')"""},
{"label": "Histogram with cumulative distribution", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(5)
data = np.random.exponential(scale=2.0, size=800)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

# Regular histogram
ax1.hist(data, bins=35, color='#DD8452', edgecolor='white', linewidth=0.4, alpha=0.8)
ax1.set_xlabel('Value'); ax1.set_ylabel('Count')
ax1.set_title('Exponential Distribution')
ax1.grid(True, axis='y', alpha=0.3)

# Cumulative histogram (ECDF style)
ax2.hist(data, bins=35, cumulative=True, density=True,
         color='#4C72B0', edgecolor='white', linewidth=0.4, alpha=0.7, label='ECDF')
# Overlay theoretical CDF: 1 - exp(-x/scale)
xr = np.linspace(0, data.max(), 200)
ax2.plot(xr, 1 - np.exp(-xr / 2.0), 'r-', linewidth=2, label='Theoretical CDF')
ax2.set_xlabel('Value'); ax2.set_ylabel('Cumulative Probability')
ax2.set_title('Cumulative Distribution')
ax2.legend(); ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('hist_cumulative.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved hist_cumulative.png')"""},
{"label": "Step histogram and density=True comparison", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(13)
data_a = np.random.normal(60, 12, 600)
data_b = np.random.normal(75, 10, 600)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Filled histogram (counts)
axes[0].hist(data_a, bins=30, alpha=0.6, color='steelblue',
             edgecolor='white', label='Group A')
axes[0].hist(data_b, bins=30, alpha=0.6, color='tomato',
             edgecolor='white', label='Group B')
axes[0].set_title('Filled — Count'); axes[0].legend()
axes[0].set_xlabel('Value'); axes[0].set_ylabel('Count')
axes[0].grid(True, axis='y', alpha=0.3)

# Step histogram (unfilled outline)
axes[1].hist(data_a, bins=30, histtype='step', linewidth=2,
             color='steelblue', label='Group A')
axes[1].hist(data_b, bins=30, histtype='step', linewidth=2,
             color='tomato', label='Group B')
axes[1].set_title('Step — Count'); axes[1].legend()
axes[1].set_xlabel('Value'); axes[1].set_ylabel('Count')
axes[1].grid(True, axis='y', alpha=0.3)

# Density=True — normalised to probability density
axes[2].hist(data_a, bins=30, density=True, histtype='stepfilled',
             alpha=0.5, color='steelblue', edgecolor='steelblue',
             linewidth=1.5, label='Group A')
axes[2].hist(data_b, bins=30, density=True, histtype='stepfilled',
             alpha=0.5, color='tomato', edgecolor='tomato',
             linewidth=1.5, label='Group B')
# Overlay normal PDFs
for data, col in [(data_a, 'steelblue'), (data_b, 'tomato')]:
    xr = np.linspace(data.min(), data.max(), 200)
    pdf = (1 / (data.std() * np.sqrt(2*np.pi))) * np.exp(
          -0.5 * ((xr - data.mean()) / data.std())**2)
    axes[2].plot(xr, pdf, color=col, linewidth=2.5)
axes[2].set_title('Step-Filled — Density'); axes[2].legend()
axes[2].set_xlabel('Value'); axes[2].set_ylabel('Probability Density')
axes[2].grid(True, axis='y', alpha=0.3)

plt.suptitle('Histogram Style Comparison', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('hist_styles_comparison.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved hist_styles_comparison.png')"""}
],
"practice": {
"title": "Histogram with Density Curve",
"desc": "Generate 1000 samples from a normal distribution (mean=50, std=12). Plot a histogram with density=True (30 bins, steelblue). Overlay a manually computed normal PDF curve (no scipy). Add vertical lines for mean and ±1 std. Label axes, add title and legend. Save as 'practice_hist.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(7)
data = np.random.normal(50, 12, 1000)

fig, ax = plt.subplots(figsize=(8, 4))

# TODO: plot histogram with density=True, bins=30, steelblue
# ax.hist(data, bins=30, density=True, ...)

# TODO: compute and overlay normal PDF
# xr = np.linspace(data.min(), data.max(), 200)
# mu, sigma = data.mean(), data.std()
# pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xr - mu) / sigma)**2)
# ax.plot(xr, pdf, color='navy', linewidth=2, label='Normal PDF')

# TODO: add vertical lines for mean and ±1 std
# ax.axvline(mu, color='red', linestyle='--', label=f'Mean={mu:.1f}')
# ax.axvline(mu - sigma, color='orange', linestyle=':', label='-1σ')
# ax.axvline(mu + sigma, color='orange', linestyle=':', label='+1σ')

ax.set_xlabel('Value')
ax.set_ylabel('Density')
# TODO: ax.set_title(...)
# TODO: ax.legend()
plt.tight_layout()
# TODO: plt.savefig('practice_hist.png', dpi=100, bbox_inches='tight')
plt.close()
print('Done')""",
"examples": [
{"label": "Stacked Histogram Comparison", "code":
"""import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
group_a = rng.normal(65, 10, 200)
group_b = rng.normal(75, 12, 200)
group_c = rng.normal(55, 8,  200)

fig, ax = plt.subplots(figsize=(9, 5))
bins = np.linspace(20, 120, 25)
ax.hist([group_a, group_b, group_c], bins=bins,
        label=['Group A', 'Group B', 'Group C'],
        color=['steelblue', 'tomato', 'seagreen'],
        alpha=0.7, edgecolor='white', stacked=False)
ax.axvline(group_a.mean(), color='steelblue', lw=2, ls='--', label=f'A mean={group_a.mean():.1f}')
ax.axvline(group_b.mean(), color='tomato',    lw=2, ls='--', label=f'B mean={group_b.mean():.1f}')
ax.axvline(group_c.mean(), color='seagreen',  lw=2, ls='--', label=f'C mean={group_c.mean():.1f}')
ax.set(title='Score Distribution by Group', xlabel='Score', ylabel='Count')
ax.legend()
plt.tight_layout()
plt.savefig('hist_comparison.png', dpi=100)
plt.show()"""},
{"label": "Log-Scale Histogram for Skewed Data", "code":
"""import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
data = rng.exponential(scale=500, size=2000)  # heavy right tail

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
bins = np.logspace(np.log10(data.min()+1), np.log10(data.max()), 30)

# Linear scale
axes[0].hist(data, bins=30, color='coral', edgecolor='white', alpha=0.8)
axes[0].set(title='Linear Scale', xlabel='Value', ylabel='Count')

# Log-log scale
axes[1].hist(data, bins=bins, color='teal', edgecolor='white', alpha=0.8)
axes[1].set_xscale('log')
axes[1].set_yscale('log')
axes[1].set(title='Log-Log Scale', xlabel='Value (log)', ylabel='Count (log)')

for ax in axes:
    ax.axvline(np.median(data), color='red', ls='--', lw=1.5, label=f'Median={np.median(data):.0f}')
    ax.legend()

plt.suptitle('Right-Skewed Distribution', fontsize=13, y=1.01)
plt.tight_layout()
plt.savefig('hist_logscale.png', dpi=100)
plt.show()"""},
{"label": "2D Histogram (Density Plot)", "code":
"""import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
n = 3000
x = rng.normal(0, 1, n)
y = 0.5 * x + rng.normal(0, 0.8, n)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# 2D histogram
h = axes[0].hist2d(x, y, bins=30, cmap='Blues')
fig.colorbar(h[3], ax=axes[0], label='Count')
axes[0].set(title='hist2d', xlabel='x', ylabel='y')

# Hexbin
hb = axes[1].hexbin(x, y, gridsize=20, cmap='YlOrRd', mincnt=1)
fig.colorbar(hb, ax=axes[1], label='Count')
axes[1].set(title='hexbin', xlabel='x', ylabel='y')

# Scatter with alpha
axes[2].scatter(x, y, alpha=0.15, s=8, color='navy')
axes[2].set(title='Scatter (alpha=0.15)', xlabel='x', ylabel='y')

plt.suptitle('2D Distribution Comparison', fontsize=12)
plt.tight_layout()
plt.savefig('hist2d.png', dpi=100)
plt.show()"""},
]
},
"rw": {
"title": "Loan Application Risk Distribution",
"scenario": "A credit risk analyst plots the distribution of applicant credit scores to set approval thresholds.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(3)
# Simulate credit score distribution (skewed left — more mid/high scores)
approved = np.random.normal(700, 60, 800).clip(580, 850)
rejected = np.random.normal(580, 50, 400).clip(300, 680)

fig, ax = plt.subplots(figsize=(9, 4))
ax.hist(approved, bins=30, alpha=0.6, color='#2ecc71', label='Approved', edgecolor='white')
ax.hist(rejected, bins=30, alpha=0.6, color='#e74c3c', label='Rejected', edgecolor='white')

# Threshold line
ax.axvline(620, color='black', linestyle='--', linewidth=2, label='Threshold: 620')
ax.set_xlabel('Credit Score'); ax.set_ylabel('Applicants')
ax.set_title('Credit Score Distribution by Decision')
ax.legend(); ax.grid(True, axis='y', alpha=0.3)

# Annotation
ax.annotate('High risk zone', xy=(550, 30), fontsize=9, color='#e74c3c')
ax.annotate('Low risk zone',  xy=(720, 60), fontsize=9, color='#2ecc71')
plt.tight_layout()
plt.savefig('hist_credit.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved hist_credit.png')"""}
},

{
"title": "5. Subplots",
"desc": "plt.subplots() creates a grid of axes in a single figure. Essential for dashboards and side-by-side comparisons.",
"examples": [
{"label": "2×2 subplot grid", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.linspace(0, 10, 200)

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0,0].plot(x, np.sin(x), color='steelblue')
axes[0,0].set_title('Line: sin(x)')

axes[0,1].bar(['A','B','C','D'], [23,45,12,67], color='#DD8452')
axes[0,1].set_title('Bar Chart')

axes[1,0].scatter(np.random.randn(100), np.random.randn(100), alpha=0.5)
axes[1,0].set_title('Scatter')

axes[1,1].hist(np.random.randn(500), bins=25, color='#55A868')
axes[1,1].set_title('Histogram')

# Global title and spacing
fig.suptitle('Dashboard Overview', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('subplots_2x2.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved subplots_2x2.png')"""},
{"label": "Shared axes and different sizes", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(5)
dates  = np.arange(30)
price  = 100 + np.cumsum(np.random.randn(30))
volume = np.random.randint(1000, 5000, 30)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6),
                                 sharex=True,
                                 gridspec_kw={'height_ratios': [3, 1]})
ax1.plot(dates, price, color='steelblue', linewidth=2)
ax1.set_ylabel('Price ($)'); ax1.set_title('Stock Price & Volume')
ax1.grid(True, alpha=0.3)

ax2.bar(dates, volume, color='gray', alpha=0.5)
ax2.set_ylabel('Volume'); ax2.set_xlabel('Day')

plt.tight_layout()
plt.savefig('subplots_shared.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved subplots_shared.png')"""},
{"label": "GridSpec for irregular subplot layouts", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

np.random.seed(8)
fig = plt.figure(figsize=(11, 7))
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)

# Wide top plot spanning all 3 columns
ax_top = fig.add_subplot(gs[0, :])
x = np.linspace(0, 10, 200)
ax_top.plot(x, np.sin(x) * np.exp(-0.1*x), color='steelblue', linewidth=2)
ax_top.set_title('Wide Top: Damped Sine'); ax_top.grid(True, alpha=0.25)

# Three smaller bottom plots
for col, (title, color) in enumerate([('Scatter','#DD8452'),('Bar','#55A868'),('Hist','#8172B2')]):
    ax = fig.add_subplot(gs[1, col])
    if title == 'Scatter':
        ax.scatter(np.random.randn(50), np.random.randn(50), color=color, alpha=0.6, s=25)
    elif title == 'Bar':
        ax.bar(['A','B','C'], [4, 7, 5], color=color)
    else:
        ax.hist(np.random.randn(200), bins=20, color=color, edgecolor='white', linewidth=0.4)
    ax.set_title(title)

fig.suptitle('GridSpec Layout', fontsize=13, fontweight='bold')
plt.savefig('subplots_gridspec.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved subplots_gridspec.png')"""},
{"label": "subplot2grid for asymmetric dashboard layouts", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(22)
fig = plt.figure(figsize=(12, 7))

# subplot2grid(shape, loc, rowspan, colspan) — place cells in a grid manually
ax_main  = plt.subplot2grid((3, 4), (0, 0), rowspan=2, colspan=3)  # big left
ax_right = plt.subplot2grid((3, 4), (0, 3), rowspan=3, colspan=1)  # tall right
ax_bot1  = plt.subplot2grid((3, 4), (2, 0), rowspan=1, colspan=1)  # bottom row
ax_bot2  = plt.subplot2grid((3, 4), (2, 1), rowspan=1, colspan=1)
ax_bot3  = plt.subplot2grid((3, 4), (2, 2), rowspan=1, colspan=1)

# Main panel — time series
t = np.linspace(0, 4 * np.pi, 300)
ax_main.plot(t, np.sin(t), color='steelblue', linewidth=2, label='sin')
ax_main.plot(t, np.cos(t), color='tomato', linewidth=2, linestyle='--', label='cos')
ax_main.fill_between(t, np.sin(t), np.cos(t), alpha=0.08, color='gray')
ax_main.set_title('Main — Trig Functions'); ax_main.legend(fontsize=8)
ax_main.grid(True, alpha=0.25)

# Tall right panel — horizontal bars (KPIs)
kpis   = ['KPI A', 'KPI B', 'KPI C', 'KPI D', 'KPI E']
values = np.random.uniform(40, 95, 5)
colors = ['#2ecc71' if v >= 70 else '#e74c3c' for v in values]
ax_right.barh(kpis, values, color=colors, edgecolor='white', linewidth=0.5)
ax_right.set_xlim(0, 100)
ax_right.axvline(70, color='gray', linestyle='--', linewidth=0.8)
ax_right.set_title('KPIs', fontsize=9)
ax_right.tick_params(labelsize=7)

# Bottom three mini-panels
for ax, title, color in zip([ax_bot1, ax_bot2, ax_bot3],
                              ['Alpha', 'Beta', 'Gamma'],
                              ['#4C72B0', '#DD8452', '#55A868']):
    data = np.random.randn(120)
    ax.hist(data, bins=15, color=color, edgecolor='white', linewidth=0.3, alpha=0.8)
    ax.set_title(title, fontsize=8); ax.tick_params(labelsize=6)
    ax.grid(True, axis='y', alpha=0.3)

fig.suptitle('subplot2grid — Asymmetric Dashboard', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('subplots_subplot2grid.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved subplots_subplot2grid.png')"""}
],
"practice": {
"title": "2x2 Subplot Grid",
"desc": "Create a 2x2 subplot figure. Top-left: line plot of cos(x) over [0, 4π]. Top-right: scatter of 100 random points colored by angle. Bottom-left: bar chart of 5 random categories. Bottom-right: histogram of 500 standard normal samples. Add individual titles, a global suptitle, and save as 'practice_subplots.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Top-left: line plot of cos(x)
x = np.linspace(0, 4 * np.pi, 300)
# TODO: axes[0,0].plot(x, np.cos(x), ...)
# TODO: axes[0,0].set_title('...')

# Top-right: scatter of 100 random points, colored by angle
pts = np.random.randn(100, 2)
angles = np.arctan2(pts[:, 1], pts[:, 0])
# TODO: sc = axes[0,1].scatter(pts[:,0], pts[:,1], c=angles, cmap='hsv', alpha=0.7)
# TODO: plt.colorbar(sc, ax=axes[0,1])
# TODO: axes[0,1].set_title('...')

# Bottom-left: bar chart of 5 categories
cats   = ['A', 'B', 'C', 'D', 'E']
values = np.random.randint(10, 80, 5)
# TODO: axes[1,0].bar(cats, values, ...)
# TODO: axes[1,0].set_title('...')

# Bottom-right: histogram of 500 normal samples
data = np.random.randn(500)
# TODO: axes[1,1].hist(data, bins=25, ...)
# TODO: axes[1,1].set_title('...')

# TODO: fig.suptitle('2x2 Dashboard', fontsize=14, fontweight='bold')
plt.tight_layout()
# TODO: plt.savefig('practice_subplots.png', dpi=100, bbox_inches='tight')
plt.close()
print('Done')""",
"examples": [
{"label": "Shared Axes with Different Plot Types", "code":
"""import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(7)
t = np.linspace(0, 2*np.pi, 200)

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=False, sharey=False)

# Sine wave
axes[0,0].plot(t, np.sin(t), 'b-', lw=2)
axes[0,0].set(title='Sine Wave', xlabel='t', ylabel='sin(t)')
axes[0,0].fill_between(t, np.sin(t), alpha=0.2)

# Random walk
walk = np.cumsum(rng.normal(0, 1, 200))
axes[0,1].plot(walk, color='tomato', lw=1.5)
axes[0,1].axhline(0, color='gray', ls='--', lw=1)
axes[0,1].set(title='Random Walk', xlabel='Step', ylabel='Position')

# Bar chart
cats = ['Mon','Tue','Wed','Thu','Fri']
vals = rng.integers(20, 100, 5)
bars = axes[1,0].bar(cats, vals, color='steelblue', edgecolor='white')
axes[1,0].bar_label(bars, padding=3)
axes[1,0].set(title='Weekly Sales', ylabel='Units')

# Scatter
x, y = rng.normal(0,1,80), rng.normal(0,1,80)
axes[1,1].scatter(x, y, c=np.hypot(x,y), cmap='viridis', alpha=0.7, s=40)
axes[1,1].set(title='Scatter by Distance', xlabel='x', ylabel='y')

plt.suptitle('Mixed Plot Types — 2x2 Grid', fontsize=13, y=1.01)
plt.tight_layout()
plt.savefig('subplot_mixed.png', dpi=100)
plt.show()"""},
{"label": "GridSpec for Custom Layout", "code":
"""import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

rng = np.random.default_rng(0)
data = rng.normal(size=500)
x = np.linspace(-3, 3, 200)

fig = plt.figure(figsize=(12, 8))
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)

# Large plot spanning top-left 2 columns
ax_main = fig.add_subplot(gs[0, :2])
ax_main.plot(data[:100], color='steelblue', lw=1.5, label='Series A')
ax_main.plot(data[100:200]-1, color='tomato', lw=1.5, label='Series B')
ax_main.legend(); ax_main.set_title('Main Time Series')

# Top-right: histogram
ax_hist = fig.add_subplot(gs[0, 2])
ax_hist.hist(data, bins=20, color='plum', edgecolor='white')
ax_hist.set_title('Distribution')

# Bottom row: 3 equal plots
for col, (label, color) in enumerate(zip(['Box','Violin','Normal PDF'],
                                          ['coral','seagreen','royalblue'])):
    ax = fig.add_subplot(gs[1, col])
    if col == 0:
        ax.boxplot(data, patch_artist=True, boxprops=dict(facecolor=color, alpha=0.6))
    elif col == 1:
        ax.violinplot(data, showmedians=True)
    else:
        from scipy import stats
        ax.plot(x, stats.norm.pdf(x), color=color, lw=2)
        ax.fill_between(x, stats.norm.pdf(x), alpha=0.2, color=color)
    ax.set_title(label)

plt.suptitle('GridSpec Custom Layout', fontsize=14, y=1.02)
plt.savefig('gridspec_layout.png', dpi=100)
plt.show()"""},
{"label": "Inset Axes & Zoom Effect", "code":
"""import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

rng = np.random.default_rng(42)
t  = np.linspace(0, 10, 500)
y  = np.sin(t) * np.exp(-0.1 * t) + rng.normal(0, 0.05, 500)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, y, color='steelblue', lw=1.5, label='Damped Oscillation')
ax.set(title='Main View', xlabel='Time', ylabel='Amplitude')
ax.legend()

# Inset axes zoomed into t=3..5
axins = ax.inset_axes([0.60, 0.45, 0.35, 0.45])
axins.plot(t, y, color='steelblue', lw=1.5)
axins.set_xlim(3, 5); axins.set_ylim(-0.8, 0.8)
axins.set_xticklabels([]); axins.set_yticklabels([])
axins.set_title('Zoomed: t=3-5', fontsize=9)

# Draw rectangle on main axis + connecting lines
ax.indicate_inset_zoom(axins, edgecolor='tomato', lw=1.5)

plt.tight_layout()
plt.savefig('subplot_inset.png', dpi=100)
plt.show()"""},
]
},
"rw": {
"title": "ML Model Evaluation Dashboard",
"scenario": "A data scientist creates a 4-panel figure showing loss curves, accuracy, confusion matrix, and prediction distribution.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
epochs    = np.arange(1, 51)
train_loss= 1.5 * np.exp(-0.06 * epochs) + np.random.randn(50) * 0.02
val_loss  = 1.5 * np.exp(-0.05 * epochs) + 0.05 + np.random.randn(50) * 0.03
train_acc = 1 - train_loss / 1.5 + 0.3
val_acc   = 1 - val_loss   / 1.5 + 0.28

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Loss curves
axes[0].plot(epochs, train_loss, label='Train',  color='steelblue')
axes[0].plot(epochs, val_loss,   label='Val',    color='tomato', linestyle='--')
axes[0].set_title('Loss'); axes[0].set_xlabel('Epoch')
axes[0].legend(); axes[0].grid(True, alpha=0.3)

# Accuracy curves
axes[1].plot(epochs, train_acc.clip(0,1), label='Train', color='steelblue')
axes[1].plot(epochs, val_acc.clip(0,1),   label='Val',   color='tomato', linestyle='--')
axes[1].set_title('Accuracy'); axes[1].set_xlabel('Epoch')
axes[1].legend(); axes[1].grid(True, alpha=0.3)

# Prediction histogram
preds = np.random.beta(2, 2, 500)
axes[2].hist(preds, bins=25, color='#55A868', edgecolor='white')
axes[2].axvline(0.5, color='red', linestyle='--', label='Threshold')
axes[2].set_title('Prediction Scores'); axes[2].set_xlabel('Score')
axes[2].legend()

fig.suptitle('Model Evaluation Dashboard', fontweight='bold')
plt.tight_layout()
plt.savefig('subplots_ml_dashboard.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved subplots_ml_dashboard.png')"""}
},

{
"title": "6. Figure Customization",
"desc": "Control colors, line styles, markers, fonts, spines, and tick formatting. Good styling makes charts publication-ready.",
"examples": [
{"label": "Markers, styles, colors, spines", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

x  = np.arange(1, 8)
y1 = [3, 7, 5, 9, 6, 8, 10]
y2 = [1, 4, 3, 6, 4, 7, 8]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y1, 'o-', color='steelblue', markersize=8,
        linewidth=2, markerfacecolor='white', markeredgewidth=2, label='Series A')
ax.plot(x, y2, 's--', color='tomato',    markersize=7,
        linewidth=2, markerfacecolor='white', markeredgewidth=2, label='Series B')

# Remove top/right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks(x)
ax.set_xticklabels([f'Day {i}' for i in x], rotation=30, ha='right')
ax.set_title('Weekly Performance', fontsize=13, fontweight='bold', pad=12)
ax.legend(frameon=False); ax.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig('custom_markers.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved custom_markers.png')"""},
{"label": "Annotations and text", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(1)
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-0.1 * x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, color='steelblue', linewidth=2)

# Peak annotation
peak_idx = np.argmax(y)
ax.annotate(f'Peak ({x[peak_idx]:.1f}, {y[peak_idx]:.2f})',
            xy=(x[peak_idx], y[peak_idx]),
            xytext=(x[peak_idx]+1.5, y[peak_idx]+0.1),
            arrowprops=dict(arrowstyle='->', color='red'),
            color='red', fontsize=9)

ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax.fill_between(x, y, where=(y > 0), alpha=0.15, color='steelblue')
ax.fill_between(x, y, where=(y < 0), alpha=0.15, color='tomato')
ax.set_title('Damped Sine Wave'); ax.set_xlabel('x')
plt.tight_layout()
plt.savefig('custom_annotations.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved custom_annotations.png')"""},
{"label": "Tick formatting and color-coded regions", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

np.random.seed(2)
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
revenue = np.array([42, 38, 51, 47, 59, 65, 70, 62, 55, 68, 75, 88]) * 1000

fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(range(12), revenue, 'o-', color='#1a73e8', linewidth=2.5,
        markersize=7, markerfacecolor='white', markeredgewidth=2)
ax.fill_between(range(12), revenue, alpha=0.1, color='#1a73e8')

# Format y-axis as currency
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))

# Color background by quarter
colors = ['#fff9f0','#f0fff4','#f0f4ff','#fff0f4']
for q, color in enumerate(colors):
    ax.axvspan(q*3 - 0.5, q*3 + 2.5, alpha=0.25, color=color, zorder=0)

# Annotate max
best_idx = int(np.argmax(revenue))
ax.annotate(f'Best: ${revenue[best_idx]/1000:.0f}K', xy=(best_idx, revenue[best_idx]),
            xytext=(best_idx - 2, revenue[best_idx] + 4000),
            arrowprops=dict(arrowstyle='->', color='green'), color='green', fontsize=9)

ax.set_xticks(range(12)); ax.set_xticklabels(months)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.set_title('Monthly Revenue with Quarter Shading', fontsize=13, fontweight='bold')
ax.grid(True, axis='y', alpha=0.25)
plt.tight_layout()
plt.savefig('custom_tick_format.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved custom_tick_format.png')"""}
],
"practice": {
"title": "Full Professional Chart",
"desc": "Plot monthly sales data for two products over 12 months. Customize: remove top/right spines, use circle and square markers with white fill, format y-axis as dollars (e.g. '$42K'), rotate x-tick labels, add an annotation arrow pointing to the peak month, and a shaded region between the two lines. Save as 'practice_custom.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

months   = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
sales_a  = np.array([42, 38, 51, 47, 59, 65, 70, 62, 55, 68, 75, 88]) * 1000
sales_b  = np.array([30, 35, 40, 38, 45, 50, 55, 52, 48, 58, 62, 70]) * 1000
x        = np.arange(12)

fig, ax = plt.subplots(figsize=(11, 5))

# TODO: plot sales_a with 'o-' markers, steelblue, markerfacecolor='white'
# ax.plot(x, sales_a, 'o-', ...)

# TODO: plot sales_b with 's--' markers, tomato, markerfacecolor='white'
# ax.plot(x, sales_b, 's--', ...)

# TODO: shade region between the two lines
# ax.fill_between(x, sales_a, sales_b, alpha=0.1, color='gray')

# TODO: remove top/right spines
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

# TODO: format y-axis as '$XK'
# ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))

# TODO: annotate peak of sales_a with arrow
# best = int(np.argmax(sales_a))
# ax.annotate(...)

ax.set_xticks(x)
ax.set_xticklabels(months, rotation=30, ha='right')
# TODO: ax.set_title(...), ax.legend(), ax.grid(...)
plt.tight_layout()
# TODO: plt.savefig('practice_custom.png', dpi=100, bbox_inches='tight')
plt.close()
print('Done')""",
"examples": [
{"label": "Annotated Stock-Style OHLC Chart", "code":
"""import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

rng = np.random.default_rng(42)
n = 30
dates = np.arange(n)
close = 100 + np.cumsum(rng.normal(0, 1.5, n))
high  = close + rng.uniform(0.5, 3, n)
low   = close - rng.uniform(0.5, 3, n)
open_ = close - rng.uniform(-1.5, 1.5, n)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7),
                                 gridspec_kw={'height_ratios': [3, 1]},
                                 sharex=True)

# OHLC bars
for i in range(n):
    color = 'seagreen' if close[i] >= open_[i] else 'tomato'
    ax1.plot([dates[i], dates[i]], [low[i], high[i]], color=color, lw=1.5)
    ax1.add_patch(mpatches.Rectangle(
        (dates[i]-0.3, min(open_[i], close[i])),
        0.6, abs(close[i]-open_[i]),
        fc=color, ec=color, alpha=0.85))

# Moving average
ma5 = np.convolve(close, np.ones(5)/5, mode='valid')
ax1.plot(dates[4:], ma5, color='royalblue', lw=2, ls='--', label='5-day MA')
ax1.set(title='30-Day OHLC Chart', ylabel='Price ($)')
ax1.legend(); ax1.grid(alpha=0.3)

# Volume bars
volume = rng.integers(100, 1000, n)
colors = ['seagreen' if close[i] >= open_[i] else 'tomato' for i in range(n)]
ax2.bar(dates, volume, color=colors, alpha=0.7, width=0.6)
ax2.set(xlabel='Day', ylabel='Volume')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('ohlc_chart.png', dpi=100)
plt.show()"""},
]
},
"rw": {
"title": "Executive KPI Summary Chart",
"scenario": "A BI developer creates a polished, publication-ready monthly KPI chart with branded colors and annotations.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

months  = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
revenue = [4.2, 3.8, 5.1, 5.8, 6.2, 7.0, 6.5, 7.8, 8.1, 7.5, 9.2, 10.4]
target  = [5.0] * 12

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(months, revenue, 'o-', color='#1a73e8', linewidth=2.5,
        markersize=7, markerfacecolor='white', markeredgewidth=2.5, label='Actual Revenue')
ax.plot(months, target, '--', color='#ea4335', linewidth=1.5,
        alpha=0.7, label='Monthly Target ($5M)')
ax.fill_between(months, revenue, target,
                where=[r >= t for r, t in zip(revenue, target)],
                alpha=0.1, color='green', label='Above target')
ax.fill_between(months, revenue, target,
                where=[r < t for r, t in zip(revenue, target)],
                alpha=0.1, color='red', label='Below target')

# Annotate best month
best = months[revenue.index(max(revenue))]
ax.annotate(f'Best: ${max(revenue):.1f}M', xy=(best, max(revenue)),
            xytext=(best, max(revenue)+0.4),
            ha='center', fontsize=9, color='green', fontweight='bold')

ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.set_ylabel('Revenue (USD millions)'); ax.set_title('2024 Monthly Revenue vs Target',
                                                       fontsize=14, fontweight='bold')
ax.legend(frameon=False, loc='upper left'); ax.grid(True, axis='y', alpha=0.2)
plt.tight_layout()
plt.savefig('custom_kpi.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved custom_kpi.png')"""}
},

{
"title": "7. Pie & Donut Chart",
"desc": "Pie charts show part-to-whole relationships. Donut charts are a modern alternative. Avoid too many slices — use 5 or fewer.",
"examples": [
{"label": "Pie chart with explode", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

labels  = ['Python', 'JavaScript', 'Java', 'C++', 'Other']
sizes   = [30, 25, 20, 15, 10]
explode = [0.05, 0, 0, 0, 0]   # pull out the first slice
colors  = ['#4C72B0','#DD8452','#55A868','#C44E52','#8172B2']

fig, ax = plt.subplots(figsize=(7, 5))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, explode=explode, colors=colors,
    autopct='%1.1f%%', startangle=140,
    wedgeprops=dict(edgecolor='white', linewidth=2)
)
for t in autotexts: t.set_fontsize(9)
ax.set_title('Language Market Share')
plt.tight_layout()
plt.savefig('pie_basic.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved pie_basic.png')"""},
{"label": "Donut chart", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

labels = ['Organic', 'Paid Search', 'Social', 'Email', 'Direct']
sizes  = [35, 25, 20, 12, 8]
colors = ['#2ecc71','#3498db','#e74c3c','#f39c12','#9b59b6']

fig, ax = plt.subplots(figsize=(7, 5))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, colors=colors,
    autopct='%1.0f%%', startangle=90,
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2)   # donut!
)
for t in autotexts: t.set_fontsize(9)
ax.text(0, 0, 'Traffic\\nSources', ha='center', va='center',
        fontsize=11, fontweight='bold')
ax.set_title('Website Traffic Sources')
plt.tight_layout()
plt.savefig('pie_donut.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved pie_donut.png')"""},
{"label": "Nested donut / ring chart", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Outer ring: main categories
outer_labels = ['Engineering', 'Sales', 'Marketing', 'Other']
outer_sizes  = [40, 30, 20, 10]
outer_colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']

# Inner ring: sub-breakdown for Engineering and Sales only (simplified)
inner_labels = ['FE', 'BE', 'DevOps', 'Inside', 'Field', 'Mkt-A', 'Mkt-B', 'Misc']
inner_sizes  = [15, 15, 10, 18, 12, 12, 8, 10]
inner_colors = ['#6B9BE8', '#8BB2F0', '#AACCFF',
                '#F0A875', '#F5C49A',
                '#7DC88A', '#A5DDB0',
                '#E88A8A']

fig, ax = plt.subplots(figsize=(8, 7))
ax.pie(outer_sizes, labels=outer_labels, colors=outer_colors,
       radius=1.0, startangle=90,
       wedgeprops=dict(width=0.35, edgecolor='white', linewidth=2),
       autopct='%1.0f%%', pctdistance=0.82)
ax.pie(inner_sizes, colors=inner_colors,
       radius=0.65, startangle=90,
       wedgeprops=dict(width=0.35, edgecolor='white', linewidth=1))
ax.set_title('Headcount — Nested Donut', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('pie_nested.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved pie_nested.png')"""},
{"label": "Waffle chart with matplotlib patches", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

categories = ['Completed', 'In Progress', 'Blocked', 'Not Started']
values     = [45, 30, 10, 15]
colors     = ['#2e7d32', '#1565c0', '#b71c1c', '#9e9e9e']

total   = sum(values)
squares = [round(v / total * 100) for v in values]
squares[-1] += 100 - sum(squares)

grid = []
for color, count in zip(colors, squares):
    grid.extend([color] * count)

fig, ax = plt.subplots(figsize=(8, 8))
for i, color in enumerate(grid):
    row, col = divmod(i, 10)
    ax.add_patch(mpatches.FancyBboxPatch(
        (col * 1.1, (9 - row) * 1.1), 1.0, 1.0,
        boxstyle='round,pad=0.05', fc=color, ec='white', lw=2))

ax.set_xlim(-0.1, 11.1); ax.set_ylim(-0.1, 11.1)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Project Task Status (Waffle Chart)', fontsize=13, pad=15)

legend_patches = [mpatches.Patch(fc=c, label=f'{l} ({v}%)')
                  for c, l, v in zip(colors, categories, squares)]
ax.legend(handles=legend_patches, loc='lower center',
          ncol=2, frameon=False, fontsize=11,
          bbox_to_anchor=(0.5, -0.05))
plt.tight_layout()
plt.savefig('waffle_chart.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved waffle_chart.png')"""}
],
"practice": {
"title": "Donut Chart",
"desc": "Create a donut chart (width=0.45) showing 5 product categories: Electronics 35%, Clothing 25%, Food 20%, Books 12%, Other 8%. Use a custom color palette, display percentages inside the wedges, add a center label showing 'Sales\\n2024', and a title. Save as 'practice_donut.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

labels = ['Electronics', 'Clothing', 'Food', 'Books', 'Other']
sizes  = [35, 25, 20, 12, 8]
# TODO: choose 5 colors
colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B2']

fig, ax = plt.subplots(figsize=(7, 6))

# TODO: create donut chart using ax.pie with wedgeprops=dict(width=0.45, ...)
# wedges, texts, autotexts = ax.pie(
#     sizes, labels=labels, colors=colors,
#     autopct='%1.0f%%', startangle=90,
#     wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
# )

# TODO: resize autopct text
# for t in autotexts: t.set_fontsize(9)

# TODO: add center label
# ax.text(0, 0, 'Sales\\n2024', ha='center', va='center', fontsize=12, fontweight='bold')

# TODO: ax.set_title(...)
plt.tight_layout()
# TODO: plt.savefig('practice_donut.png', dpi=100, bbox_inches='tight')
plt.close()
print('Done')"""
},
"rw": {
"title": "Budget Allocation Dashboard",
"scenario": "A CFO uses a donut chart to present department budget allocation for a board presentation.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

depts  = ['Engineering', 'Sales', 'Marketing', 'Operations', 'HR', 'R&D']
budget = [32, 22, 18, 12, 8, 8]
colors = ['#1a73e8','#34a853','#fbbc04','#ea4335','#9c27b0','#00bcd4']
total  = sum(budget)

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    budget, labels=depts, colors=colors,
    autopct=lambda p: f'${p*total/100:.0f}M\\n({p:.0f}%)',
    startangle=120,
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2)
)
for t in autotexts: t.set_fontsize(8)
ax.text(0, 0, f'Total\\n${total}M', ha='center', va='center',
        fontsize=12, fontweight='bold')
ax.set_title('FY2024 Budget Allocation by Department',
             fontsize=13, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('pie_budget.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved pie_budget.png')"""}
},

{
"title": "8. Heatmap with imshow/pcolor",
"desc": "Heatmaps encode a 2D matrix as color intensities. Great for correlation matrices, confusion matrices, and time×metric data.",
"examples": [
{"label": "Correlation heatmap", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.randn(100, 5)
labels = ['Age', 'Income', 'Score', 'Tenure', 'Spend']

corr = np.corrcoef(data.T)

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
plt.colorbar(im, ax=ax)

ax.set_xticks(range(5)); ax.set_yticks(range(5))
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_yticklabels(labels)

# Annotate values
for i in range(5):
    for j in range(5):
        ax.text(j, i, f'{corr[i,j]:.2f}', ha='center', va='center',
                fontsize=8, color='black' if abs(corr[i,j]) < 0.6 else 'white')

ax.set_title('Feature Correlation Matrix')
plt.tight_layout()
plt.savefig('heatmap_corr.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved heatmap_corr.png')"""},
{"label": "Calendar heatmap (day × hour)", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(7)
# 7 days × 24 hours activity matrix
activity = np.random.poisson(lam=5, size=(7, 24)).astype(float)
activity[1:5, 9:17] += 15   # weekday work hours spike

days  = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
hours = [f'{h:02d}:00' for h in range(24)]

fig, ax = plt.subplots(figsize=(14, 4))
im = ax.imshow(activity, cmap='YlOrRd', aspect='auto')
plt.colorbar(im, label='Requests/hr')
ax.set_yticks(range(7)); ax.set_yticklabels(days)
ax.set_xticks(range(0, 24, 2)); ax.set_xticklabels(hours[::2], rotation=45, ha='right')
ax.set_title('API Request Heatmap — Weekday vs Weekend')
plt.tight_layout()
plt.savefig('heatmap_calendar.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved heatmap_calendar.png')"""},
{"label": "pcolormesh with diverging colormap", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(3)
# 10 assets x 12 months return matrix (%)
n_assets, n_months = 10, 12
returns = np.random.randn(n_assets, n_months) * 5   # % monthly returns
asset_names = [f'Asset {i+1}' for i in range(n_assets)]
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, ax = plt.subplots(figsize=(13, 5))
mesh = ax.pcolormesh(returns, cmap='RdYlGn', vmin=-12, vmax=12)
plt.colorbar(mesh, label='Monthly Return (%)', ax=ax)

# Annotate cells
for i in range(n_assets):
    for j in range(n_months):
        color = 'white' if abs(returns[i, j]) > 8 else 'black'
        ax.text(j + 0.5, i + 0.5, f'{returns[i,j]:+.1f}',
                ha='center', va='center', fontsize=7, color=color)

ax.set_xticks(np.arange(n_months) + 0.5); ax.set_xticklabels(month_names)
ax.set_yticks(np.arange(n_assets) + 0.5); ax.set_yticklabels(asset_names)
ax.set_title('Asset Monthly Returns Heatmap (%)', fontweight='bold')
plt.tight_layout()
plt.savefig('heatmap_pcolormesh.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved heatmap_pcolormesh.png')"""},
{"label": "Calendar heatmap (GitHub-style)", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import datetime

rng   = np.random.default_rng(42)
days  = 365
start = datetime.date(2024, 1, 1)
counts = rng.integers(0, 20, days)
for i in range(days):
    if (start + datetime.timedelta(i)).weekday() >= 5:
        counts[i] = max(0, int(counts[i] * 0.3))

padding = (start.weekday() + 1) % 7
padded  = np.concatenate([np.zeros(padding, dtype=int), counts])
n_pad   = 7 - len(padded) % 7 if len(padded) % 7 else 0
padded  = np.concatenate([padded, np.zeros(n_pad)])
grid    = padded.reshape(-1, 7).T

cmap = mcolors.LinearSegmentedColormap.from_list(
    'gh', ['#ebedf0','#9be9a8','#40c463','#30a14e','#216e39'])

fig, ax = plt.subplots(figsize=(16, 3))
im = ax.imshow(grid, cmap=cmap, aspect='auto', vmin=0, vmax=counts.max())
ax.set_yticks(range(7))
ax.set_yticklabels(['Sun','Mon','Tue','Wed','Thu','Fri','Sat'], fontsize=9)
ax.set_xticks([]); ax.set_title('2024 Activity Calendar', fontsize=12)
fig.colorbar(im, ax=ax, orientation='horizontal', fraction=0.02,
             pad=0.15, label='Activity count')
plt.tight_layout()
plt.savefig('calendar_heatmap.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved calendar_heatmap.png')"""}
],
"practice": {
"title": "Correlation Matrix Heatmap",
"desc": "Generate a (200, 6) random dataset with manually introduced correlations between columns. Compute the 6x6 correlation matrix, display it as a heatmap using imshow with the 'coolwarm' colormap (vmin=-1, vmax=1), annotate each cell with its correlation value (2 decimal places), and rotate x-tick labels 45 degrees. Save as 'practice_heatmap.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
n = 200
# Build correlated dataset
x1 = np.random.randn(n)
x2 = 0.8 * x1 + np.random.randn(n) * 0.4       # correlated with x1
x3 = -0.5 * x1 + np.random.randn(n) * 0.7      # negatively correlated
x4 = np.random.randn(n)                          # independent
x5 = 0.6 * x2 + np.random.randn(n) * 0.5       # correlated with x2
x6 = np.random.randn(n)                          # independent

data   = np.column_stack([x1, x2, x3, x4, x5, x6])
labels = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6']

# TODO: corr = np.corrcoef(data.T)

fig, ax = plt.subplots(figsize=(7, 6))

# TODO: im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
# TODO: plt.colorbar(im, ax=ax)

# TODO: set tick labels (rotated 45 for x-axis)
# ax.set_xticks(range(6)); ax.set_xticklabels(labels, rotation=45, ha='right')
# ax.set_yticks(range(6)); ax.set_yticklabels(labels)

# TODO: annotate each cell with corr value
# for i in range(6):
#     for j in range(6):
#         color = 'white' if abs(corr[i,j]) > 0.6 else 'black'
#         ax.text(j, i, f'{corr[i,j]:.2f}', ha='center', va='center', fontsize=8, color=color)

# TODO: ax.set_title(...)
plt.tight_layout()
# TODO: plt.savefig('practice_heatmap.png', dpi=100, bbox_inches='tight')
plt.close()
print('Done')"""
},
"rw": {
"title": "Confusion Matrix Visualization",
"scenario": "A ML engineer visualizes the confusion matrix of a multi-class classifier to identify which classes are most confused.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Simulated confusion matrix: 5 classes
classes = ['Cat','Dog','Bird','Fish','Rabbit']
cm = np.array([
    [85,  5,  3,  2,  5],
    [ 4, 88,  2,  1,  5],
    [ 3,  2, 82,  8,  5],
    [ 1,  2,  6, 89,  2],
    [ 6,  4,  3,  2, 85],
])

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(cm, cmap='Blues')
plt.colorbar(im, ax=ax)

ax.set_xticks(range(5)); ax.set_yticks(range(5))
ax.set_xticklabels(classes, rotation=45, ha='right')
ax.set_yticklabels(classes)
ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
ax.set_title('Confusion Matrix — Animal Classifier')

for i in range(5):
    for j in range(5):
        color = 'white' if cm[i,j] > 50 else 'black'
        ax.text(j, i, str(cm[i,j]), ha='center', va='center',
                fontsize=11, color=color, fontweight='bold')

# Overall accuracy
acc = cm.diagonal().sum() / cm.sum()
ax.set_xlabel(f'Predicted    (Accuracy: {acc:.1%})', fontsize=10)
plt.tight_layout()
plt.savefig('heatmap_confusion.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved heatmap_confusion.png')"""}
},

{
"title": "9. Twin Axes & Secondary Y-Axis",
"desc": "twinx() creates a second y-axis sharing the same x-axis — essential when two variables have different scales.",
"examples": [
{"label": "Dual y-axis line + bar", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

months  = ['Jan','Feb','Mar','Apr','May','Jun']
revenue = [120, 135, 128, 155, 162, 180]
margin  = [22.1, 21.5, 23.0, 24.2, 23.8, 25.5]

fig, ax1 = plt.subplots(figsize=(9, 4))
ax2 = ax1.twinx()

bars = ax1.bar(months, revenue, color='steelblue', alpha=0.7, label='Revenue ($K)')
line = ax2.plot(months, margin, 'o-', color='tomato', linewidth=2.5,
                markersize=7, markerfacecolor='white', markeredgewidth=2, label='Margin %')

ax1.set_ylabel('Revenue ($K)',    color='steelblue')
ax2.set_ylabel('Gross Margin (%)', color='tomato')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax2.tick_params(axis='y', labelcolor='tomato')

lines  = line
labels = [l.get_label() for l in lines]
ax1.legend(bars, ['Revenue ($K)'], loc='upper left')
ax2.legend(lines, labels, loc='lower right')

ax1.set_title('Revenue & Gross Margin')
plt.tight_layout()
plt.savefig('twin_bar_line.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved twin_bar_line.png')"""},
{"label": "Temperature and humidity dual axis", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(9)
hours    = np.arange(24)
temp     = 20 + 8 * np.sin((hours - 6) * np.pi / 12) + np.random.randn(24)
humidity = 60 - 20 * np.sin((hours - 6) * np.pi / 12) + np.random.randn(24) * 3

fig, ax1 = plt.subplots(figsize=(10, 4))
ax2 = ax1.twinx()

ax1.plot(hours, temp, color='#e74c3c', linewidth=2, label='Temp (°C)')
ax1.fill_between(hours, temp, alpha=0.1, color='#e74c3c')
ax2.plot(hours, humidity, color='#3498db', linewidth=2,
         linestyle='--', label='Humidity (%)')

ax1.set_xlabel('Hour of Day'); ax1.set_ylabel('Temperature (°C)', color='#e74c3c')
ax2.set_ylabel('Humidity (%)', color='#3498db')
ax1.set_title('24-Hour Weather Profile')
ax1.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig('twin_weather.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved twin_weather.png')"""},
{"label": "Three-axis plot with twiny and twinx", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(11)
months   = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
x        = np.arange(12)
revenue  = np.array([42, 38, 51, 47, 59, 65, 70, 62, 55, 68, 75, 88])
cost     = np.array([30, 29, 36, 34, 41, 44, 48, 43, 40, 46, 51, 59])
margin   = (revenue - cost) / revenue * 100

fig, ax1 = plt.subplots(figsize=(11, 5))
ax2 = ax1.twinx()

# Stacked area (revenue, cost on ax1)
ax1.fill_between(x, cost,    alpha=0.35, color='#C44E52', label='Cost ($K)')
ax1.fill_between(x, revenue, cost, alpha=0.35, color='#55A868', label='Profit ($K)')
ax1.plot(x, revenue, 'o-', color='#4C72B0', linewidth=2,
         markersize=5, markerfacecolor='white', markeredgewidth=1.5, label='Revenue ($K)')

# Margin % on secondary axis
ax2.plot(x, margin, 's--', color='#DD8452', linewidth=1.8,
         markersize=6, markerfacecolor='white', markeredgewidth=1.5, label='Margin %')
ax2.set_ylabel('Gross Margin (%)', color='#DD8452')
ax2.tick_params(axis='y', labelcolor='#DD8452')
ax2.set_ylim(0, 50)

ax1.set_xticks(x); ax1.set_xticklabels(months, rotation=30, ha='right')
ax1.set_ylabel('Amount ($K)', color='#4C72B0')
ax1.tick_params(axis='y', labelcolor='#4C72B0')
ax1.set_title('Revenue, Cost & Margin — Full Year', fontweight='bold')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)
ax1.grid(True, axis='y', alpha=0.2)
plt.tight_layout()
plt.savefig('twin_three_axis.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved twin_three_axis.png')"""},
{"label": "Event annotation with axvspan and annotate", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
t   = np.linspace(0, 365, 365)
revenue = 1000 + 2*t + 150*np.sin(2*np.pi*t/365) + rng.normal(0, 30, 365)
traffic = 5000 + 10*t + rng.normal(0, 200, 365)

fig, ax1 = plt.subplots(figsize=(12, 5))
ax2 = ax1.twinx()

l1, = ax1.plot(t, revenue, color='steelblue', lw=1.5, label='Revenue ($)')
l2, = ax2.plot(t, traffic, color='tomato',    lw=1.2, alpha=0.7, label='Traffic')

# Highlight events
events = [(90,  120, '#ffffcc', 'Summer\\nPromo'),
          (200, 220, '#e8f5e9', 'Product\\nLaunch'),
          (300, 340, '#fce4ec', 'Holiday\\nSale')]
for start, end, color, label in events:
    ax1.axvspan(start, end, alpha=0.4, color=color)
    ax1.annotate(label, xy=((start+end)/2, revenue.max()*0.95),
                 ha='center', fontsize=9, fontweight='bold')

ax1.set(xlabel='Day of Year', ylabel='Revenue ($)', title='Revenue & Traffic with Event Annotations')
ax2.set_ylabel('Daily Traffic', color='tomato')
ax2.tick_params(axis='y', labelcolor='tomato')
ax1.legend(handles=[l1, l2], loc='upper left')
plt.tight_layout()
plt.savefig('twin_annotated.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved twin_annotated.png')"""}
],
"practice": {
"title": "Dual-Axis Sales & Growth Rate Chart",
"desc": "Create a dual-axis chart for 12 months of data: bar chart of monthly revenue on the left y-axis (steelblue bars), and a line of month-over-month growth rate (%) on the right y-axis (tomato line with markers). Color-code the left y-axis label steelblue and right y-axis label tomato. Add legends for both axes. Save as 'practice_twin.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

months  = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
revenue = np.array([42, 38, 51, 47, 59, 65, 70, 62, 55, 68, 75, 88])
# TODO: compute MoM growth rate (%)
# growth = np.concatenate([[0], np.diff(revenue) / revenue[:-1] * 100])

fig, ax1 = plt.subplots(figsize=(11, 5))
ax2 = ax1.twinx()

# TODO: ax1.bar(months, revenue, color='steelblue', alpha=0.7, label='Revenue ($K)')
# TODO: ax2.plot(months, growth, 'o-', color='tomato', ...)

# TODO: color y-axis labels
# ax1.set_ylabel('Revenue ($K)', color='steelblue')
# ax2.set_ylabel('MoM Growth (%)', color='tomato')
# ax1.tick_params(axis='y', labelcolor='steelblue')
# ax2.tick_params(axis='y', labelcolor='tomato')

# TODO: add a horizontal dashed line at growth=0 on ax2
# ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8)

# TODO: legends for both axes
ax1.set_title('Monthly Revenue & Growth Rate')
plt.tight_layout()
# TODO: plt.savefig('practice_twin.png', dpi=100, bbox_inches='tight')
plt.close()
print('Done')"""
},
"rw": {
"title": "E-Commerce Sales & Conversion Rate",
"scenario": "A growth analyst overlays daily order volume and conversion rate to find days where traffic didn't convert well.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(12)
days     = np.arange(1, 31)
orders   = (500 + np.cumsum(np.random.randn(30)*20) +
            np.random.randn(30)*30).clip(400, 900).astype(int)
cvr      = (3.5 + np.random.randn(30)*0.4 +
            np.sin(days/5) * 0.3).clip(2.5, 5.0)

fig, ax1 = plt.subplots(figsize=(12, 4))
ax2 = ax1.twinx()

ax1.bar(days, orders, color='#4C72B0', alpha=0.5, label='Orders')
ax2.plot(days, cvr, 'o-', color='#DD8452', linewidth=2,
         markersize=5, markerfacecolor='white', markeredgewidth=1.5,
         label='Conversion Rate (%)')

# Flag low-CVR days
low_cvr = days[cvr < 3.0]
for d in low_cvr:
    ax1.axvspan(d-0.5, d+0.5, color='red', alpha=0.1)

ax1.set_xlabel('Day of Month')
ax1.set_ylabel('Orders', color='#4C72B0')
ax2.set_ylabel('Conversion Rate (%)', color='#DD8452')
ax1.set_title('January 2024 — Orders & Conversion Rate')
ax1.legend(loc='upper left', frameon=False)
ax2.legend(loc='upper right', frameon=False)
plt.tight_layout()
plt.savefig('twin_ecommerce.png', dpi=100, bbox_inches='tight')
plt.close()
print('Saved twin_ecommerce.png')"""}
},

{
"title": "10. Saving Figures & Style Sheets",
"desc": "Save plots as PNG, PDF, SVG, or EPS with savefig(). Use plt.style.use() or rcParams to apply consistent styling across all charts.",
"examples": [
{"label": "Saving figures with savefig", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

fig, ax = plt.subplots(figsize=(8, 4))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), linewidth=2)
ax.set_title('Saved Figure Example')
ax.set_xlabel('x'); ax.set_ylabel('sin(x)')

# Save as PNG (high DPI for print)
fig.savefig('plot.png', dpi=150, bbox_inches='tight', facecolor='white')
# Save as PDF (vector — best for papers)
fig.savefig('plot.pdf', bbox_inches='tight')
# Save as SVG (scalable for web)
fig.savefig('plot.svg', bbox_inches='tight')

print('Saved: plot.png, plot.pdf, plot.svg')
plt.close()

for f in ['plot.png','plot.pdf','plot.svg']:
    if os.path.exists(f): os.remove(f)
print('Cleaned up.')"""},
{"label": "Style sheets and rcParams", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

print("Available styles (first 5):", plt.style.available[:5], "...")

# Apply a style
with plt.style.context('seaborn-v0_8-whitegrid'):
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x), linewidth=2, label='sin(x)')
    ax.plot(x, np.cos(x), linewidth=2, label='cos(x)')
    ax.set_title('Seaborn Whitegrid Style')
    ax.legend()
    plt.tight_layout()
    fig.savefig('style_whitegrid.png', dpi=100, bbox_inches='tight')
    plt.close()
    print('Saved style_whitegrid.png')

# Custom rcParams for global defaults
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'figure.facecolor': 'white',
})
print('rcParams updated.')"""},
{"label": "Batch export: saving multiple figures to files", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams.update({
    'font.size': 10,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'grid.alpha': 0.3,
})

np.random.seed(42)
datasets = {
    'alpha': np.random.randn(300) * 2 + 5,
    'beta':  np.random.exponential(2, 300),
    'gamma': np.random.uniform(0, 10, 300),
}

saved = []
for name, data in datasets.items():
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))

    axes[0].hist(data, bins=25, color='steelblue', edgecolor='white', linewidth=0.4)
    axes[0].set_title(f'{name.capitalize()} — Histogram')
    axes[0].axvline(data.mean(), color='red', linestyle='--', linewidth=1.2, label=f'mean={data.mean():.2f}')
    axes[0].legend(fontsize=8)

    axes[1].boxplot(data, vert=True, patch_artist=True,
                    boxprops=dict(facecolor='steelblue', alpha=0.5))
    axes[1].set_title(f'{name.capitalize()} — Boxplot')
    axes[1].set_ylabel('Value')

    fname = f'report_{name}.png'
    fig.tight_layout()
    fig.savefig(fname, dpi=120, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    saved.append(fname)
    print(f'  Saved {fname}  ({os.path.getsize(fname)//1024} KB)')

# Clean up
for f in saved:
    if os.path.exists(f): os.remove(f)
print('Batch export complete.')"""},
{"label": "Animation with FuncAnimation (bouncing ball)", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots(figsize=(6, 5))
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.set_aspect('equal'); ax.set_title('Bouncing Ball Animation')
ax.set_facecolor('#1a1a2e')

ball, = ax.plot([], [], 'o', color='#ffa600', ms=18)
trail_x, trail_y = [], []
trail, = ax.plot([], [], '-', color='#ffa600', alpha=0.3, lw=2)

x, y = 5.0, 8.0
vx, vy = 0.15, -0.12

def init():
    ball.set_data([], []); trail.set_data([], [])
    return ball, trail

def update(frame):
    global x, y, vx, vy
    x += vx; y += vy
    vy -= 0.005          # gravity
    if x <= 0 or x >= 10: vx *= -1
    if y <= 0: vy = abs(vy) * 0.92; y = 0
    trail_x.append(x); trail_y.append(y)
    if len(trail_x) > 40:
        trail_x.pop(0); trail_y.pop(0)
    ball.set_data([x], [y])
    trail.set_data(trail_x, trail_y)
    return ball, trail

ani = animation.FuncAnimation(fig, update, frames=80, init_func=init,
                               interval=40, blit=True)
ani.save('bouncing_ball.gif', writer='pillow', fps=25, dpi=80)
plt.close()
print('Saved bouncing_ball.gif')"""}
],
"practice": {
"title": "Saving to PNG and SVG",
"desc": "Create a figure with two subplots side-by-side: (left) a line plot of sin(x) styled with 'seaborn-v0_8-whitegrid', and (right) a bar chart of 5 categories. Apply rcParams to set font.size=11. Save the figure as both 'practice_output.png' (dpi=150) and 'practice_output.svg'. Print the file sizes. Then clean up both files.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# TODO: update rcParams (font.size=11, figure.facecolor='white')
# plt.rcParams.update({...})

x      = np.linspace(0, 2 * np.pi, 200)
cats   = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 17, 38, 29]

# TODO: use plt.style.context('seaborn-v0_8-whitegrid') to create the figure
# with plt.style.context('seaborn-v0_8-whitegrid'):
#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
#
#     # left: line plot of sin(x)
#     ax1.plot(x, np.sin(x), color='steelblue', linewidth=2)
#     ax1.set_title('sin(x)'); ax1.set_xlabel('x'); ax1.set_ylabel('y')
#
#     # right: bar chart
#     ax2.bar(cats, values, color='#DD8452', edgecolor='white')
#     ax2.set_title('Category Values'); ax2.set_ylabel('Count')
#
#     plt.tight_layout()
#
#     # TODO: save as PNG and SVG
#     # fig.savefig('practice_output.png', dpi=150, bbox_inches='tight', facecolor='white')
#     # fig.savefig('practice_output.svg', bbox_inches='tight')
#     plt.close()

# TODO: print file sizes
# for f in ['practice_output.png', 'practice_output.svg']:
#     print(f'{f}: {os.path.getsize(f)//1024} KB')

# TODO: clean up both files
# for f in ['practice_output.png', 'practice_output.svg']:
#     if os.path.exists(f): os.remove(f)
print('Done')"""
},
"rw": {
"title": "Automated Report Figure Export",
"scenario": "A data engineering pipeline generates standardized PNG charts nightly and attaches them to an email report.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# Apply consistent branding
plt.rcParams.update({
    'font.family':      'DejaVu Sans',
    'font.size':        10,
    'axes.titlesize':   12,
    'axes.titleweight': 'bold',
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'grid.alpha':       0.3,
})

def save_kpi_chart(metric, values, labels, filename, color='steelblue'):
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(range(len(values)), values, 'o-', color=color,
            linewidth=2, markersize=6, markerfacecolor='white', markeredgewidth=2)
    ax.fill_between(range(len(values)), values, alpha=0.1, color=color)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha='right')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${x:,.0f}'))
    ax.set_title(metric); ax.grid(True)
    fig.tight_layout()
    fig.savefig(filename, dpi=120, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved {filename}  ({os.path.getsize(filename)//1024} KB)')

months = ['Jan','Feb','Mar','Apr','May','Jun']
rev    = [42000, 38500, 51000, 47200, 59800, 65600]
save_kpi_chart('Monthly Revenue', rev, months, 'revenue_report.png')

if os.path.exists('revenue_report.png'):
    os.remove('revenue_report.png')
    print('Cleaned up.')"""}
}

,
{
    "title": "11. 3D Plotting",
    "desc": "Create 3D visualizations with Axes3D — surface plots, wireframes, 3D scatter plots, and line trajectories that reveal multi-dimensional structure.",
    "examples": [
        {
            "label": "3D scatter plot with color mapping",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nfrom mpl_toolkits.mplot3d import Axes3D\nimport numpy as np\n\nnp.random.seed(42)\nx, y, z = np.random.randn(3, 100)\nfig = plt.figure(figsize=(8, 6))\nax = fig.add_subplot(111, projection='3d')\nsc = ax.scatter(x, y, z, c=z, cmap='plasma', s=50)\nplt.colorbar(sc, ax=ax, label='Z value')\nax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')\nax.set_title('3D Scatter Plot')\nplt.tight_layout()\nplt.savefig('3d_scatter.png', dpi=80); plt.close()\nprint('Saved 3d_scatter.png')"
        },
        {
            "label": "Surface plot with meshgrid",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nfrom mpl_toolkits.mplot3d import Axes3D\nimport numpy as np\n\nx = np.linspace(-3, 3, 50)\ny = np.linspace(-3, 3, 50)\nX, Y = np.meshgrid(x, y)\nZ = np.sin(np.sqrt(X**2 + Y**2))\n\nfig = plt.figure(figsize=(8, 6))\nax = fig.add_subplot(111, projection='3d')\nsurf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9)\nplt.colorbar(surf, ax=ax, shrink=0.5, label='sin(r)')\nax.set_title('3D Surface: sin(sqrt(x^2+y^2))')\nplt.tight_layout()\nplt.savefig('surface3d.png', dpi=80); plt.close()\nprint('Saved surface3d.png')"
        },
        {
            "label": "Wireframe and contour overlay",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nfrom mpl_toolkits.mplot3d import Axes3D\nimport numpy as np\n\nx = np.linspace(-2, 2, 30)\ny = np.linspace(-2, 2, 30)\nX, Y = np.meshgrid(x, y)\nZ = X**2 - Y**2\n\nfig = plt.figure(figsize=(12, 5))\nax1 = fig.add_subplot(121, projection='3d')\nax1.plot_wireframe(X, Y, Z, rstride=3, cstride=3, color='teal', linewidth=0.5)\nax1.set_title('Wireframe: x^2 - y^2')\n\nax2 = fig.add_subplot(122, projection='3d')\nax2.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.7)\nax2.contour(X, Y, Z, zdir='z', offset=Z.min(), cmap='coolwarm')\nax2.set_title('Surface + Contour')\nplt.tight_layout()\nplt.savefig('wireframe3d.png', dpi=80); plt.close()\nprint('Saved wireframe3d.png')"
        },
        {
            "label": "3D line trajectory",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nfrom mpl_toolkits.mplot3d import Axes3D\nimport numpy as np\n\nt = np.linspace(0, 4*np.pi, 300)\nx = np.sin(t)\ny = np.cos(t)\nz = t / (4*np.pi)\n\nfig = plt.figure(figsize=(7, 6))\nax = fig.add_subplot(111, projection='3d')\nfor i in range(len(t)-1):\n    ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=plt.cm.plasma(z[i]), linewidth=2)\nax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Height')\nax.set_title('3D Helix Trajectory')\nplt.tight_layout()\nplt.savefig('helix3d.png', dpi=80); plt.close()\nprint('Saved helix3d.png')"
        }
    ],
    "rw_scenario": "A materials scientist visualizes how temperature and pressure affect product yield across a 3D response surface to find the optimal operating conditions.",
    "rw_code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nfrom mpl_toolkits.mplot3d import Axes3D\nimport numpy as np\n\ntemp = np.linspace(100, 300, 40)\npressure = np.linspace(1, 10, 40)\nT, P = np.meshgrid(temp, pressure)\nYield = 80 * np.exp(-((T-200)**2/5000 + (P-5)**2/10))\n\nfig = plt.figure(figsize=(10, 6))\nax = fig.add_subplot(111, projection='3d')\nsurf = ax.plot_surface(T, P, Yield, cmap='YlOrRd', alpha=0.9)\nplt.colorbar(surf, ax=ax, label='Yield %')\nax.set_xlabel('Temperature (C)'); ax.set_ylabel('Pressure (bar)'); ax.set_zlabel('Yield %')\nax.set_title('Process Optimization Surface')\noptimal = np.unravel_index(Yield.argmax(), Yield.shape)\nprint(f'Optimal: T={T[optimal]:.0f}C, P={P[optimal]:.1f}bar, Yield={Yield[optimal]:.1f}%')\nplt.tight_layout()\nplt.savefig('process_surface.png', dpi=80); plt.close()\nprint('Saved process_surface.png')",
    "practice": {
        "title": "Rosenbrock Surface",
        "desc": "Plot the Rosenbrock function f(x,y)=(1-x)^2 + 100(y-x^2)^2 as a 3D surface (clipped at 2500). Overlay a contour at z=0. Mark the global minimum at (1,1,0) with a red dot.",
        "starter": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nfrom mpl_toolkits.mplot3d import Axes3D\nimport numpy as np\n\nx = np.linspace(-2, 2, 100)\ny = np.linspace(-1, 3, 100)\nX, Y = np.meshgrid(x, y)\nZ = np.clip((1-X)**2 + 100*(Y-X**2)**2, 0, 2500)\n\n# TODO: create 3D surface plot\n# TODO: mark minimum at (1, 1, 0)\n# TODO: save to 'rosenbrock.png'"
    }
},
{
    "title": "12. Custom Styles & Themes",
    "desc": "Make publication-quality figures with style sheets, rcParams, custom color cycles, and reusable theming functions.",
    "examples": [
        {
            "label": "Built-in style sheets",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nprint('Available styles (sample):', plt.style.available[:8])\n\nstyles = ['seaborn-v0_8-darkgrid', 'ggplot', 'bmh']\nx = np.linspace(0, 2*np.pi, 100)\n\nfig, axes = plt.subplots(1, 3, figsize=(15, 4))\nfor ax, style in zip(axes, styles):\n    with plt.style.context(style):\n        for i in range(3):\n            ax.plot(x, np.sin(x + i*np.pi/3))\n        ax.set_title(style.split('-')[-1])\nplt.tight_layout()\nplt.savefig('styles.png', dpi=80); plt.close()\nprint('Saved styles.png')"
        },
        {
            "label": "Custom rcParams dark theme",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\ncustom = {\n    'figure.facecolor': '#1e1e2e', 'axes.facecolor': '#1e1e2e',\n    'axes.edgecolor': '#6e6e8e', 'axes.labelcolor': '#cdd6f4',\n    'xtick.color': '#cdd6f4', 'ytick.color': '#cdd6f4',\n    'text.color': '#cdd6f4', 'grid.color': '#313244',\n    'axes.prop_cycle': matplotlib.cycler('color', ['#89b4fa','#f38ba8','#a6e3a1','#fab387']),\n    'font.size': 12,\n}\nplt.rcParams.update(custom)\nx = np.linspace(0, 4*np.pi, 200)\nfig, ax = plt.subplots(figsize=(9, 5))\nfor i, label in enumerate(['sin', 'cos', 'sin2']):\n    y = np.sin(x)*np.sin(x) if i==2 else (np.sin(x) if i==0 else np.cos(x))\n    ax.plot(x, y, linewidth=2, label=label)\nax.legend(facecolor='#313244'); ax.set_title('Dark Theme'); ax.grid(True)\nplt.tight_layout()\nplt.savefig('dark_theme.png', dpi=80, facecolor=fig.get_facecolor()); plt.close()\nplt.rcParams.update(plt.rcParamsDefault)\nprint('Saved dark_theme.png')"
        },
        {
            "label": "Custom color cycles and grouped charts",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nPALETTE = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00']\nplt.rcParams['axes.prop_cycle'] = matplotlib.cycler('color', PALETTE)\n\nfig, axes = plt.subplots(1, 2, figsize=(12, 4))\ncategories = ['A','B','C','D']; x = np.arange(len(categories)); width=0.25\nfor i, grp in enumerate(['G1','G2','G3']):\n    axes[0].bar(x+i*width, np.random.randint(10,50,4), width, label=grp)\naxes[0].set_xticks(x+width); axes[0].set_xticklabels(categories)\naxes[0].legend(); axes[0].set_title('Custom Colors — Bars')\n\nt = np.linspace(0,10,200)\nfor i in range(5):\n    axes[1].plot(t, np.sin(t+i)*np.exp(-0.1*t), label=f'S{i+1}')\naxes[1].legend(fontsize=8); axes[1].set_title('Custom Colors — Lines')\nplt.tight_layout()\nplt.savefig('colors.png', dpi=80); plt.close()\nplt.rcParams.update(plt.rcParamsDefault)\nprint('Saved colors.png')"
        },
        {
            "label": "Reusable publication-style context manager",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nfrom contextlib import contextmanager\n\n@contextmanager\ndef pub_style(w=8, h=5):\n    params = {\n        'font.size': 12, 'axes.titlesize': 14, 'axes.labelsize': 12,\n        'lines.linewidth': 2, 'axes.spines.top': False, 'axes.spines.right': False,\n    }\n    with plt.style.context('seaborn-v0_8-whitegrid'):\n        plt.rcParams.update(params)\n        fig, ax = plt.subplots(figsize=(w, h))\n        yield fig, ax\n        plt.tight_layout()\n\nx = np.linspace(0, 10, 200)\nwith pub_style() as (fig, ax):\n    ax.plot(x, np.sin(x), label='sin(x)')\n    ax.plot(x, np.cos(x), '--', label='cos(x)')\n    ax.set_xlabel('x'); ax.set_ylabel('Amplitude')\n    ax.set_title('Publication-Ready Figure'); ax.legend()\n    fig.savefig('publication.png', bbox_inches='tight')\nplt.close()\nprint('Saved publication.png')"
        }
    ],
    "rw_scenario": "A research team requires all paper figures to share the same serif font, color scheme, and spine style. They ship a shared lab_style module that every script imports.",
    "rw_code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nLAB_STYLE = {\n    'font.family': 'serif', 'font.size': 11,\n    'axes.titlesize': 13, 'axes.spines.top': False, 'axes.spines.right': False,\n    'axes.prop_cycle': matplotlib.cycler('color', ['#2196F3','#F44336','#4CAF50','#FF9800']),\n    'lines.linewidth': 1.8,\n}\n\ndef lab_figure(nrows=1, ncols=1, **kw):\n    with plt.rc_context(LAB_STYLE):\n        return plt.subplots(nrows, ncols, **kw)\n\nx = np.linspace(0, 5, 100)\nfig, axes = lab_figure(1, 2, figsize=(10, 4))\nfor i, ax in enumerate(axes):\n    for j in range(3):\n        ax.plot(x, np.sin(x*(i+1)+j*np.pi/3), label=f'Signal {j+1}')\n    ax.set_title(f'Experiment {i+1}'); ax.legend(fontsize=8)\nplt.tight_layout()\nplt.savefig('lab_style.png', dpi=80); plt.close()\nprint('Saved lab_style.png')",
    "practice": {
        "title": "Themed Dashboard",
        "desc": "Create a 2x2 subplot figure with a dark background. Include: scatter (colored by magnitude), multi-line chart, bar chart, and histogram. Use a consistent 4-color palette.",
        "starter": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\n# TODO: set dark rcParams\n# TODO: 2x2 subplots\n# TODO: top-left: scatter (x,y normal, color=magnitude)\n# TODO: top-right: 3 sine waves\n# TODO: bottom-left: 12-bar monthly sales\n# TODO: bottom-right: histogram 500 samples, 30 bins\n# TODO: suptitle and save to 'dark_dashboard.png'"
    }
},
{
    "title": "13. Annotations & Text Elements",
    "desc": "Add rich annotations — arrows, text boxes, spans, and LaTeX math expressions — to communicate insights directly on the plot.",
    "examples": [
        {
            "label": "Arrow and text annotations",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(0, 4*np.pi, 300)\ny = np.sin(x)\nfig, ax = plt.subplots(figsize=(10, 5))\nax.plot(x, y, 'steelblue', linewidth=2)\n\n# Annotate maximum\nmax_idx = y.argmax()\nax.annotate('Global Max', xy=(x[max_idx], y[max_idx]),\n            xytext=(x[max_idx]+1, 0.6),\n            arrowprops=dict(arrowstyle='->', color='red', lw=2),\n            fontsize=11, color='red', fontweight='bold')\n\n# Annotate minimum\nmin_idx = y.argmin()\nax.annotate('Global Min', xy=(x[min_idx], y[min_idx]),\n            xytext=(x[min_idx]-1.5, -0.6),\n            arrowprops=dict(arrowstyle='->', color='orange', lw=2),\n            fontsize=11, color='orange')\n\nax.set_title('sin(x) with Annotations'); ax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.savefig('annotated_sine.png', dpi=80); plt.close()\nprint('Saved annotated_sine.png')"
        },
        {
            "label": "Text boxes and callout styles",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(0, 10, 200)\nfig, ax = plt.subplots(figsize=(9, 5))\nax.plot(x, np.exp(-0.3*x)*np.sin(x*2), linewidth=2)\n\nbox_styles = [('round,pad=0.3', 'lightblue', 'navy'),\n              ('round4,pad=0.4', 'lightyellow', 'darkorange'),\n              ('sawtooth,pad=0.3', 'lightgreen', 'darkgreen')]\n\nfor i, (style, fc, ec) in enumerate(box_styles):\n    ax.text(2+i*3, 0.5-i*0.3, f'Style: {style.split(\",\")[0]}',\n            fontsize=10, ha='center',\n            bbox=dict(boxstyle=style, facecolor=fc, edgecolor=ec, alpha=0.9))\n\nax.set_title('Text Box Styles'); ax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.savefig('textboxes.png', dpi=80); plt.close()\nprint('Saved textboxes.png')"
        },
        {
            "label": "axvspan and axhspan for region highlighting",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\ndates = np.arange(60)\nprices = 100 + np.cumsum(np.random.randn(60))\n\nfig, ax = plt.subplots(figsize=(11, 5))\nax.plot(dates, prices, 'steelblue', linewidth=1.5)\n\n# Shade event regions\nax.axvspan(10, 20, color='red',   alpha=0.15, label='Crash period')\nax.axvspan(35, 45, color='green', alpha=0.15, label='Recovery period')\nax.axhline(prices.mean(), color='gray', linestyle='--', linewidth=1, label='Mean price')\n\n# Annotate events\nax.text(15, ax.get_ylim()[1]*0.98, 'Crash', ha='center', color='darkred', fontsize=10)\nax.text(40, ax.get_ylim()[1]*0.98, 'Recovery', ha='center', color='darkgreen', fontsize=10)\n\nax.legend(); ax.set_xlabel('Day'); ax.set_ylabel('Price')\nax.set_title('Price Series with Event Annotations')\nplt.tight_layout()\nplt.savefig('event_regions.png', dpi=80); plt.close()\nprint('Saved event_regions.png')"
        },
        {
            "label": "LaTeX math in labels and annotations",
            "code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(-3, 3, 300)\nmu, sigma = 0, 1\ny = (1/(sigma*np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mu)/sigma)**2)\n\nfig, ax = plt.subplots(figsize=(8, 5))\nax.plot(x, y, 'steelblue', linewidth=2.5)\nax.fill_between(x, y, where=(x>=-1)&(x<=1), alpha=0.3, color='steelblue', label=r'$\\pm 1\\sigma$ (68.3%)')\n\n# LaTeX in axis labels\nax.set_xlabel(r'$x$', fontsize=14)\nax.set_ylabel(r'$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x-\\mu}{\\sigma}\\right)^2}$', fontsize=11)\nax.set_title(r'Normal Distribution $\\mathcal{N}(\\mu=0, \\sigma=1)$', fontsize=13)\n\n# LaTeX annotation\nax.annotate(r'$\\mu = 0$', xy=(0, y.max()), xytext=(1.2, y.max()*0.9),\n            arrowprops=dict(arrowstyle='->'), fontsize=12)\nax.legend(fontsize=11)\nplt.tight_layout()\nplt.savefig('latex_plot.png', dpi=80); plt.close()\nprint('Saved latex_plot.png')"
        }
    ],
    "rw_scenario": "A market analyst annotates key macro events (rate hike, earnings beat, market crash) on a price chart with colored spans, arrows, and labeled callout boxes.",
    "rw_code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\ndays = np.arange(252)\nprice = 100 * np.exp(np.cumsum(np.random.randn(252) * 0.01))\n\nevents = [\n    (30,  'Rate Hike',    'red',   -8),\n    (80,  'Earnings Beat','green',  8),\n    (130, 'Market Crash', 'red',  -20),\n    (180, 'Fed Pivot',    'blue',   5),\n]\n\nfig, ax = plt.subplots(figsize=(12, 5))\nax.plot(days, price, color='#1f77b4', linewidth=1.5)\n\nfor day, label, color, offset in events:\n    ax.axvline(day, color=color, linestyle='--', alpha=0.6, linewidth=1)\n    ax.annotate(label, xy=(day, price[day]),\n                xytext=(day+3, price[day]+offset),\n                arrowprops=dict(arrowstyle='->', color=color),\n                color=color, fontsize=9, fontweight='bold')\n\nax.set_xlabel('Trading Day'); ax.set_ylabel('Price ($)')\nax.set_title('Stock Price with Key Events')\nax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.savefig('market_events.png', dpi=80); plt.close()\nprint('Saved market_events.png')",
    "practice": {
        "title": "Annotated Confidence Interval",
        "desc": "Plot a regression line y=2x+1 with noise. Add shaded 95% confidence band, annotate the slope with an arrow and LaTeX label, and shade the extrapolation region (x>8) in red.",
        "starter": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\nx = np.linspace(0, 10, 50)\ny = 2*x + 1 + np.random.randn(50) * 2\nx_fit = np.linspace(0, 12, 200)\ny_fit = 2*x_fit + 1\n\nfig, ax = plt.subplots(figsize=(9, 5))\nax.scatter(x, y, alpha=0.6, label='Data')\nax.plot(x_fit, y_fit, 'r-', label='Fit')\n# TODO: add shaded CI band (y_fit +/- 2 units)\n# TODO: shade extrapolation x>8 with axvspan\n# TODO: annotate slope with arrow and r'$\\hat{\\beta}_1 = 2$'\n# TODO: save to 'ci_plot.png'"
    }
},

    {
        "title": "14. Animations & GIF Export",
        "examples": [
            {
                "label": "FuncAnimation — rolling sine wave",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import matplotlib.animation as animation\n"
                    "import numpy as np\n\n"
                    "fig, ax = plt.subplots(figsize=(7, 3))\n"
                    "x = np.linspace(0, 2*np.pi, 200)\n"
                    "line, = ax.plot(x, np.sin(x))\n"
                    "ax.set_ylim(-1.3, 1.3)\n\n"
                    "def update(frame):\n"
                    "    line.set_ydata(np.sin(x + frame * 0.15))\n"
                    "    return line,\n\n"
                    "ani = animation.FuncAnimation(fig, update, frames=40, interval=60, blit=True)\n"
                    "try:\n"
                    "    ani.save('sine_anim.gif', writer='pillow', fps=15)\n"
                    "    print('Saved sine_anim.gif')\n"
                    "except Exception as e:\n"
                    "    print(f'pillow not installed ({e}) — animation built ok')\n"
                    "plt.close()"
                )
            },
            {
                "label": "Random walk particle animation",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import matplotlib.animation as animation\n"
                    "import numpy as np\n\n"
                    "np.random.seed(42)\n"
                    "n = 20\n"
                    "pos = np.random.randn(n, 2)\n"
                    "fig, ax = plt.subplots(figsize=(5, 5))\n"
                    "sc = ax.scatter(pos[:, 0], pos[:, 1], c=range(n), cmap='hsv', s=50)\n"
                    "ax.set_xlim(-5, 5); ax.set_ylim(-5, 5)\n"
                    "ax.set_title('Random Walk Particles')\n\n"
                    "def update(frame):\n"
                    "    global pos\n"
                    "    pos += np.random.randn(n, 2) * 0.15\n"
                    "    pos = np.clip(pos, -4.5, 4.5)\n"
                    "    sc.set_offsets(pos)\n"
                    "    return sc,\n\n"
                    "ani = animation.FuncAnimation(fig, update, frames=50, interval=80, blit=True)\n"
                    "try:\n"
                    "    ani.save('particles.gif', writer='pillow', fps=12)\n"
                    "    print('Saved particles.gif')\n"
                    "except Exception as e:\n"
                    "    print(f'pillow not found ({e})')\n"
                    "plt.close()"
                )
            },
            {
                "label": "Dual-subplot animation (sin & cos)",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import matplotlib.animation as animation\n"
                    "import numpy as np\n\n"
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))\n"
                    "x = np.linspace(0, 2*np.pi, 200)\n"
                    "l1, = ax1.plot(x, np.sin(x), 'b-')\n"
                    "l2, = ax2.plot(x, np.cos(x), 'r-')\n"
                    "ax1.set_title('sin(x+t)'); ax2.set_title('cos(x-t)')\n\n"
                    "def update(frame):\n"
                    "    t = frame * 0.12\n"
                    "    l1.set_ydata(np.sin(x + t))\n"
                    "    l2.set_ydata(np.cos(x - t))\n"
                    "    return l1, l2\n\n"
                    "ani = animation.FuncAnimation(fig, update, frames=50, blit=True)\n"
                    "try:\n"
                    "    ani.save('dual_anim.gif', writer='pillow', fps=15)\n"
                    "    print('Saved dual_anim.gif')\n"
                    "except:\n"
                    "    print('Animation created (pillow needed to save)')\n"
                    "plt.close()"
                )
            },
            {
                "label": "ArtistAnimation with histogram frames",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import matplotlib.animation as animation\n"
                    "import numpy as np\n\n"
                    "fig, ax = plt.subplots(figsize=(6, 4))\n"
                    "np.random.seed(0)\n"
                    "frames = []\n"
                    "for i in range(10):\n"
                    "    data = np.random.randn(50) + i * 0.5\n"
                    "    hist = ax.hist(data, bins=20, range=(-3, 9),\n"
                    "                  color=plt.cm.viridis(i/10), alpha=0.7)\n"
                    "    title = ax.text(0.5, 1.01, f'Shift = {i*0.5:.1f}',\n"
                    "                   transform=ax.transAxes, ha='center')\n"
                    "    frames.append(hist[2].tolist() + [title])\n"
                    "ani = animation.ArtistAnimation(fig, frames, interval=300, blit=True)\n"
                    "try:\n"
                    "    ani.save('hist_anim.gif', writer='pillow', fps=3)\n"
                    "    print('Saved hist_anim.gif')\n"
                    "except:\n"
                    "    print('ArtistAnimation built (pillow needed to save)')\n"
                    "plt.close()"
                )
            }
        ],
        "rw_scenario": "You need to create an animated training-progress chart for a model review, showing how train/val loss evolved over 60 epochs.",
        "rw_code": (
            "import matplotlib\n"
            "matplotlib.use('Agg')\n"
            "import matplotlib.pyplot as plt\n"
            "import matplotlib.animation as animation\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "epochs = 60\n"
            "train_loss = 2.5 * np.exp(-np.linspace(0, 3, epochs)) + np.random.randn(epochs)*0.05\n"
            "val_loss   = 2.5 * np.exp(-np.linspace(0, 2.7, epochs)) + np.random.randn(epochs)*0.08\n\n"
            "fig, ax = plt.subplots(figsize=(8, 4))\n"
            "ax.set_xlim(0, epochs); ax.set_ylim(0, 2.8)\n"
            "ax.set_xlabel('Epoch'); ax.set_ylabel('Loss')\n"
            "ax.set_title('Model Training Progress (animated)')\n"
            "tl, = ax.plot([], [], 'b-', label='Train')\n"
            "vl, = ax.plot([], [], 'r-', label='Val')\n"
            "ax.legend()\n\n"
            "def update(frame):\n"
            "    tl.set_data(range(frame+1), train_loss[:frame+1])\n"
            "    vl.set_data(range(frame+1), val_loss[:frame+1])\n"
            "    return tl, vl\n\n"
            "ani = animation.FuncAnimation(fig, update, frames=epochs, interval=60, blit=True)\n"
            "try:\n"
            "    ani.save('training_progress.gif', writer='pillow', fps=20)\n"
            "    print('Saved training_progress.gif')\n"
            "except Exception as e:\n"
            "    print(f'Animation built ({e})')\n"
            "plt.close()"
        ),
        "practice": {
            "title": "Bouncing Ball Animation",
            "desc": "Animate a ball under gravity (g=9.8). Start at y=5, vy=0. Update position each frame with dt=0.05. Reverse vy on bounce at y=0. Save 100 frames to 'bounce.gif'.",
            "starter": (
                "import matplotlib\n"
                "matplotlib.use('Agg')\n"
                "import matplotlib.pyplot as plt\n"
                "import matplotlib.animation as animation\n"
                "import numpy as np\n\n"
                "fig, ax = plt.subplots(figsize=(4, 6))\n"
                "ax.set_xlim(0, 1); ax.set_ylim(-0.2, 5.5)\n"
                "ball, = ax.plot([0.5], [5], 'bo', ms=15)\n"
                "dt = 0.05; g = 9.8\n"
                "y, vy = 5.0, 0.0\n\n"
                "# TODO: define update(frame) that applies gravity, reverses on bounce\n"
                "# TODO: FuncAnimation for 100 frames\n"
                "# TODO: save to 'bounce.gif' with pillow"
            )
        }
    },
    {
        "title": "15. Publication-Quality Figures",
        "examples": [
            {
                "label": "Style sheets comparison",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import numpy as np\n\n"
                    "x = np.linspace(0, 4*np.pi, 200)\n"
                    "styles = ['seaborn-v0_8-paper', 'ggplot', 'bmh']\n"
                    "fig, axes = plt.subplots(1, 3, figsize=(13, 4))\n"
                    "for ax, style in zip(axes, styles):\n"
                    "    with plt.style.context(style):\n"
                    "        ax.plot(x, np.sin(x), label='sin')\n"
                    "        ax.plot(x, np.cos(x), label='cos')\n"
                    "        ax.set_title(style.split('_')[-1])\n"
                    "        ax.legend(fontsize=8)\n"
                    "fig.tight_layout()\n"
                    "fig.savefig('styles_compare.png', dpi=120, bbox_inches='tight')\n"
                    "print('Saved styles_compare.png')\n"
                    "plt.close()"
                )
            },
            {
                "label": "LaTeX math in axis labels and titles",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import numpy as np\n\n"
                    "fig, ax = plt.subplots(figsize=(6, 4))\n"
                    "x = np.linspace(0.1, 3, 200)\n"
                    "ax.plot(x, np.exp(-x**2), label=r'$f(x) = e^{-x^2}$', lw=2)\n"
                    "ax.plot(x, 1/(1+x**2), label=r'$g(x) = \\frac{1}{1+x^2}$', lw=2, ls='--')\n"
                    "ax.set_xlabel(r'$x$ (normalized)', fontsize=12)\n"
                    "ax.set_ylabel(r'$f(x)$', fontsize=12)\n"
                    "ax.set_title(r'Gaussian vs Lorentzian decay', fontsize=13)\n"
                    "ax.legend(fontsize=11); ax.grid(True, alpha=0.3)\n"
                    "fig.tight_layout()\n"
                    "fig.savefig('latex_labels.png', dpi=150, bbox_inches='tight')\n"
                    "print('Saved latex_labels.png')\n"
                    "plt.close()"
                )
            },
            {
                "label": "Shared-axes multi-panel figure",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import numpy as np\n\n"
                    "np.random.seed(42)\n"
                    "fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharex=True, sharey=True)\n"
                    "for i, ax in enumerate(axes.flat):\n"
                    "    data = np.random.normal(i, 1.2, 80)\n"
                    "    ax.hist(data, bins=18, edgecolor='k', alpha=0.7)\n"
                    "    ax.axvline(data.mean(), color='red', ls='--', lw=1.2)\n"
                    "    ax.set_title(f'Group {i+1} (\u03bc={i})', fontsize=10)\n"
                    "fig.suptitle('Shared-Axis Multi-Panel', fontsize=14, fontweight='bold')\n"
                    "fig.tight_layout()\n"
                    "fig.savefig('multi_panel.png', dpi=120, bbox_inches='tight')\n"
                    "print('Saved multi_panel.png')\n"
                    "plt.close()"
                )
            },
            {
                "label": "High-DPI export with serif fonts",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import numpy as np\n\n"
                    "plt.rcParams.update({'font.family': 'serif', 'font.size': 10,\n"
                    "                     'axes.linewidth': 1.2, 'xtick.major.width': 1.2})\n"
                    "np.random.seed(42)\n"
                    "groups = ['Control', 'Drug A', 'Drug B']\n"
                    "means = [2.1, 3.4, 2.9]; stds = [0.3, 0.4, 0.35]\n"
                    "fig, ax = plt.subplots(figsize=(4.5, 3.5))\n"
                    "bars = ax.bar(groups, means, yerr=stds, capsize=5,\n"
                    "              color=['#4878D0','#EE854A','#6ACC65'], edgecolor='k', lw=0.8)\n"
                    "for b, m in zip(bars, means):\n"
                    "    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.06,\n"
                    "            f'{m:.1f}', ha='center', fontsize=9)\n"
                    "ax.set_ylabel(r'Response ($\u03bcmol/L)', fontsize=11)\n"
                    "ax.set_title('Treatment Effect', fontsize=12)\n"
                    "ax.spines[['top','right']].set_visible(False)\n"
                    "fig.tight_layout()\n"
                    "fig.savefig('publication_fig.png', dpi=300, bbox_inches='tight')\n"
                    "print('Saved publication_fig.png at 300 DPI')\n"
                    "plt.close()"
                )
            }
        ],
        "rw_scenario": "Your paper submission requires 300 DPI figures with serif fonts, LaTeX-formatted axes, and figures no wider than 5 inches with consistent styling.",
        "rw_code": (
            "import matplotlib\n"
            "matplotlib.use('Agg')\n"
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "plt.style.use('seaborn-v0_8-paper')\n"
            "plt.rcParams.update({'font.family':'serif','font.size':10,'axes.linewidth':1.2})\n"
            "np.random.seed(42)\n"
            "t = np.linspace(0, 10, 300)\n"
            "models = {\n"
            "    r'$\\alpha$-decay': np.exp(-0.3*t) + np.random.randn(300)*0.02,\n"
            "    r'$\\beta$-decay':  np.exp(-0.5*t) + np.random.randn(300)*0.02,\n"
            "    r'$\\gamma$-decay': np.exp(-0.8*t) + np.random.randn(300)*0.02,\n"
            "}\n"
            "fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))\n"
            "for label, y in models.items():\n"
            "    axes[0].plot(t, y, lw=1.5, label=label)\n"
            "axes[0].set_xlabel(r'$t$ (s)'); axes[0].set_ylabel(r'$N(t)/N_0$')\n"
            "axes[0].set_title('Linear Scale'); axes[0].legend(fontsize=9)\n"
            "axes[0].spines[['top','right']].set_visible(False)\n"
            "for label, y in models.items():\n"
            "    axes[1].semilogy(t, np.clip(y, 1e-4, 2), lw=1.5, label=label)\n"
            "axes[1].set_xlabel(r'$t$ (s)'); axes[1].set_ylabel(r'$\\log N/N_0$')\n"
            "axes[1].set_title('Log Scale'); axes[1].legend(fontsize=9)\n"
            "axes[1].spines[['top','right']].set_visible(False)\n"
            "fig.suptitle(r'Radioactive Decay: $\\alpha$, $\\beta$, $\\gamma$', fontsize=13, fontweight='bold')\n"
            "fig.tight_layout()\n"
            "fig.savefig('journal_decay.png', dpi=300, bbox_inches='tight')\n"
            "print('Saved journal_decay.png at 300 DPI')\n"
            "plt.close()"
        ),
        "practice": {
            "title": "2-Panel with Inset Zoom",
            "desc": "Plot y = e^{-0.1t}*sin(2t) on linear and log scales. Add an inset zoom on t=[0,2] in the linear panel. Use seaborn-v0_8-paper style, serif fonts, and export at 300 DPI.",
            "starter": (
                "import matplotlib\n"
                "matplotlib.use('Agg')\n"
                "import matplotlib.pyplot as plt\n"
                "from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset\n"
                "import numpy as np\n\n"
                "t = np.linspace(0, 20, 500)\n"
                "y = np.exp(-0.1*t) * np.sin(2*t)\n"
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))\n"
                "# TODO: ax1 linear plot + inset zoom t in [0,2]\n"
                "# TODO: ax2 semilogy plot\n"
                "# TODO: seaborn-v0_8-paper style, 300 DPI export"
            )
        }
    },
    {
        "title": "16. Custom Colormaps & Color Science",
        "examples": [
            {
                "label": "LinearSegmentedColormap from color list",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import matplotlib.colors as mcolors\n"
                    "import numpy as np\n\n"
                    "colors = ['#1a1a2e','#16213e','#0f3460','#e94560']\n"
                    "cmap = mcolors.LinearSegmentedColormap.from_list('dark_red', colors, N=256)\n"
                    "np.random.seed(0)\n"
                    "data = np.random.randn(40, 40).cumsum(axis=0)\n"
                    "fig, ax = plt.subplots(figsize=(6, 4))\n"
                    "im = ax.imshow(data, cmap=cmap, aspect='auto')\n"
                    "plt.colorbar(im, ax=ax, label='Value')\n"
                    "ax.set_title('Custom Dark-Red Colormap')\n"
                    "fig.savefig('custom_cmap.png', dpi=120, bbox_inches='tight')\n"
                    "print('Saved custom_cmap.png')\n"
                    "plt.close()"
                )
            },
            {
                "label": "TwoSlopeNorm for asymmetric diverging maps",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import matplotlib.colors as mcolors\n"
                    "import numpy as np\n\n"
                    "np.random.seed(42)\n"
                    "data = np.random.randn(20, 20) * 3 + 1\n"
                    "vmax = max(abs(data.min()), abs(data.max()))\n"
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))\n"
                    "im1 = ax1.imshow(data, cmap='RdBu_r', vmin=-vmax, vmax=vmax)\n"
                    "ax1.set_title('Symmetric Norm'); plt.colorbar(im1, ax=ax1)\n"
                    "norm = mcolors.TwoSlopeNorm(vmin=data.min(), vcenter=0, vmax=data.max())\n"
                    "im2 = ax2.imshow(data, cmap='RdBu_r', norm=norm)\n"
                    "ax2.set_title('TwoSlopeNorm'); plt.colorbar(im2, ax=ax2)\n"
                    "fig.tight_layout()\n"
                    "fig.savefig('diverging_norm.png', dpi=120, bbox_inches='tight')\n"
                    "print('Saved diverging_norm.png')\n"
                    "plt.close()"
                )
            },
            {
                "label": "Discrete colorbar with BoundaryNorm",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import matplotlib.colors as mcolors\n"
                    "import numpy as np\n\n"
                    "bounds = [0, 1, 2, 3, 4, 5]\n"
                    "cmap = plt.get_cmap('RdYlGn', len(bounds)-1)\n"
                    "norm = mcolors.BoundaryNorm(bounds, cmap.N)\n"
                    "levels = ['None','Low','Med','High','Max']\n"
                    "np.random.seed(7)\n"
                    "data = np.random.randint(0, 5, (8, 10))\n"
                    "fig, ax = plt.subplots(figsize=(9, 5))\n"
                    "im = ax.imshow(data, cmap=cmap, norm=norm)\n"
                    "cbar = plt.colorbar(im, ax=ax, boundaries=bounds, ticks=[0.5,1.5,2.5,3.5,4.5])\n"
                    "cbar.set_ticklabels(levels)\n"
                    "for i in range(data.shape[0]):\n"
                    "    for j in range(data.shape[1]):\n"
                    "        ax.text(j, i, levels[data[i,j]][:3],\n"
                    "                ha='center', va='center', fontsize=8)\n"
                    "ax.set_title('Discrete Risk Heatmap')\n"
                    "fig.savefig('discrete_cmap.png', dpi=120, bbox_inches='tight')\n"
                    "print('Saved discrete_cmap.png')\n"
                    "plt.close()"
                )
            },
            {
                "label": "Perceptually uniform colormap comparison",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "import numpy as np\n\n"
                    "cmaps = ['viridis', 'plasma', 'inferno', 'cividis']\n"
                    "x = y = np.linspace(-np.pi, np.pi, 200)\n"
                    "X, Y = np.meshgrid(x, y)\n"
                    "Z = np.sin(X) * np.cos(Y)\n"
                    "fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))\n"
                    "for ax, cm in zip(axes, cmaps):\n"
                    "    im = ax.imshow(Z, cmap=cm, aspect='auto')\n"
                    "    ax.set_title(cm)\n"
                    "    plt.colorbar(im, ax=ax, fraction=0.046)\n"
                    "fig.suptitle('Perceptually Uniform Colormaps', fontsize=12)\n"
                    "fig.tight_layout()\n"
                    "fig.savefig('perceptual_cmaps.png', dpi=120, bbox_inches='tight')\n"
                    "print('Saved perceptual_cmaps.png')\n"
                    "plt.close()"
                )
            }
        ],
        "rw_scenario": "Your risk dashboard uses corporate colors and needs a discrete heatmap with 5 severity levels, text labels in each cell, and a custom colorbar legend.",
        "rw_code": (
            "import matplotlib\n"
            "matplotlib.use('Agg')\n"
            "import matplotlib.pyplot as plt\n"
            "import matplotlib.colors as mcolors\n"
            "import numpy as np\n\n"
            "CORP = ['#2ecc71','#f1c40f','#e67e22','#e74c3c','#8e44ad']\n"
            "LEVELS = ['OK','Watch','Warn','Alert','Critical']\n"
            "cmap = mcolors.ListedColormap(CORP)\n"
            "norm = mcolors.BoundaryNorm(list(range(6)), cmap.N)\n"
            "np.random.seed(42)\n"
            "comps = [f'SVC-{i:02d}' for i in range(1, 11)]\n"
            "times = [f'T+{i}h' for i in range(5)]\n"
            "risk = np.random.randint(0, 5, (len(comps), len(times)))\n"
            "fig, ax = plt.subplots(figsize=(8, 6))\n"
            "im = ax.imshow(risk, cmap=cmap, norm=norm)\n"
            "cbar = plt.colorbar(im, ax=ax, boundaries=list(range(6)), ticks=[0.5,1.5,2.5,3.5,4.5])\n"
            "cbar.set_ticklabels(LEVELS); cbar.set_label('Risk Level')\n"
            "ax.set_xticks(range(len(times))); ax.set_xticklabels(times)\n"
            "ax.set_yticks(range(len(comps))); ax.set_yticklabels(comps)\n"
            "for i in range(len(comps)):\n"
            "    for j in range(len(times)):\n"
            "        lvl = risk[i,j]\n"
            "        ax.text(j, i, LEVELS[lvl], ha='center', va='center',\n"
            "                fontsize=8, color='white' if lvl >= 2 else 'black')\n"
            "ax.set_title('System Risk Dashboard', fontsize=13, fontweight='bold')\n"
            "fig.tight_layout()\n"
            "fig.savefig('risk_dashboard.png', dpi=150, bbox_inches='tight')\n"
            "print('Saved risk_dashboard.png')\n"
            "plt.close()"
        ),
        "practice": {
            "title": "Custom Terrain Colormap",
            "desc": "Create a colormap: blue → green → yellow → brown → white. Apply to a sin(X)*cos(Y) surface. Add a colorbar with 5 ticks labeled: Sea, Lowland, Hills, Mountain, Snow.",
            "starter": (
                "import matplotlib\n"
                "matplotlib.use('Agg')\n"
                "import matplotlib.pyplot as plt\n"
                "import matplotlib.colors as mcolors\n"
                "import numpy as np\n\n"
                "colors = ['#1a6b9a','#2ecc71','#f1c40f','#8b5e3c','#f5f5f5']\n"
                "cmap = mcolors.LinearSegmentedColormap.from_list('terrain_custom', colors)\n"
                "x = y = np.linspace(-3, 3, 100)\n"
                "X, Y = np.meshgrid(x, y)\n"
                "Z = np.sin(X) + np.cos(Y)\n"
                "# TODO: imshow with custom cmap\n"
                "# TODO: colorbar with 5 labeled ticks\n"
                "# TODO: save 'terrain.png' at 150 DPI"
            )
        }
    },
]  # end SECTIONS


html = make_html(SECTIONS)
nb   = make_nb(SECTIONS)
(BASE / "index.html").write_text(html, encoding="utf-8")
(BASE / "study_guide.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")
print(f"Matplotlib guide created: {BASE}")
print(f"  index.html:        {(BASE/'index.html').stat().st_size/1024:.1f} KB")
print(f"  study_guide.ipynb: {len(nb['cells'])} cells")
