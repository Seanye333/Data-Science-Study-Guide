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
{
"title": "17. Error Bars & Confidence Intervals",
"desc": "Visualize measurement uncertainty with errorbar(), fill_between() for confidence bands, and asymmetric errors.",
"examples": [
        {"label": "Basic symmetric error bars", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\nx = np.arange(1, 8)\ny = np.array([2.3, 3.1, 2.8, 4.5, 3.9, 5.2, 4.8])\nyerr = np.random.uniform(0.2, 0.6, len(x))\n\nfig, ax = plt.subplots(figsize=(8, 4))\nax.errorbar(x, y, yerr=yerr, fmt=\'o-\', color=\'steelblue\',\n            ecolor=\'lightsteelblue\', elinewidth=2, capsize=5,\n            capthick=2, label=\'Mean ± SD\')\nax.set_xlabel(\'Experiment\')\nax.set_ylabel(\'Value\')\nax.set_title(\'Error Bars — Symmetric\')\nax.legend()\nax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'errorbars_sym.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved errorbars_sym.png\')"},
        {"label": "Asymmetric error bars", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(1)\nx = np.arange(5)\ny = np.array([1.5, 2.8, 2.2, 3.6, 3.0])\nyerr_low  = np.array([0.3, 0.5, 0.4, 0.6, 0.3])\nyerr_high = np.array([0.5, 0.3, 0.6, 0.2, 0.7])\n\nfig, ax = plt.subplots(figsize=(7, 4))\nax.errorbar(x, y, yerr=[yerr_low, yerr_high],\n            fmt=\'s--\', color=\'tomato\', ecolor=\'lightcoral\',\n            elinewidth=2, capsize=6, label=\'Median [IQR]\')\nax.set_xticks(x)\nax.set_xticklabels([f\'Group {i+1}\' for i in x])\nax.set_title(\'Asymmetric Error Bars\')\nax.legend()\nax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'errorbars_asym.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved errorbars_asym.png\')"},
        {"label": "Confidence band with fill_between", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(2)\nx = np.linspace(0, 10, 100)\ny_true = np.sin(x)\nnoise = np.random.randn(100) * 0.3\ny_mean = y_true + noise * 0.2\ny_lower = y_mean - 1.96 * 0.3\ny_upper = y_mean + 1.96 * 0.3\n\nfig, ax = plt.subplots(figsize=(9, 4))\nax.plot(x, y_mean, color=\'steelblue\', linewidth=2, label=\'Mean\')\nax.fill_between(x, y_lower, y_upper, alpha=0.2, color=\'steelblue\',\n                label=\'95% CI\')\nax.plot(x, y_true, \'k--\', linewidth=1, alpha=0.6, label=\'True\')\nax.set_xlabel(\'x\')\nax.set_ylabel(\'y\')\nax.set_title(\'Confidence Interval Band\')\nax.legend()\nax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'conf_band.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved conf_band.png\')"},
        {"label": "Multiple series with shaded bands", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\nx = np.linspace(0, 5, 80)\ncolors = [\'steelblue\', \'tomato\', \'seagreen\']\nlabels = [\'Model A\', \'Model B\', \'Model C\']\noffsets = [0, 0.5, 1.0]\n\nfig, ax = plt.subplots(figsize=(9, 5))\nfor c, lab, off in zip(colors, labels, offsets):\n    mu = np.sin(x + off)\n    sd = 0.15 + 0.05 * np.abs(np.cos(x))\n    ax.plot(x, mu, color=c, linewidth=2, label=lab)\n    ax.fill_between(x, mu - sd, mu + sd, color=c, alpha=0.15)\nax.set_xlabel(\'Time\')\nax.set_ylabel(\'Score\')\nax.set_title(\'Model Comparison with Confidence Bands\')\nax.legend()\nax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'multi_band.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved multi_band.png\')"}
    ],
"rw": {
    "title": "Clinical Trial Results",
    "scenario": "Visualize drug-trial results with asymmetric confidence intervals for 4 dosage groups, a reference line at placebo, and significance brackets.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(7)\ngroups = [\'Placebo\', \'10mg\', \'25mg\', \'50mg\']\nmeans  = [0.0, 1.2, 2.8, 3.5]\nlow    = [0.0, 0.3, 0.5, 0.4]\nhigh   = [0.0, 0.5, 0.6, 0.8]\n\nfig, ax = plt.subplots(figsize=(7, 5))\nx = np.arange(len(groups))\nax.bar(x, means, color=[\'#aaa\',\'#5ab4d6\',\'#2171b5\',\'#084594\'],\n       alpha=0.85, width=0.5)\nax.errorbar(x, means, yerr=[low, high],\n            fmt=\'none\', ecolor=\'black\', elinewidth=2, capsize=8, capthick=2)\nax.axhline(0, color=\'gray\', linewidth=0.8, linestyle=\'--\')\nax.set_xticks(x); ax.set_xticklabels(groups)\nax.set_ylabel(\'Effect Size vs Baseline\')\nax.set_title(\'Clinical Trial: Dose-Response\', fontweight=\'bold\')\nfor xi, m, h in zip(x[1:], means[1:], high[1:]):\n    ax.text(xi, m + h + 0.05, \'*\' if m < 3 else \'***\',\n            ha=\'center\', fontsize=14, color=\'darkred\')\nfig.tight_layout()\nfig.savefig(\'clinical_trial.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved clinical_trial.png\')"
},
"practice": {
    "title": "Error Bar Practice",
    "desc": "Generate 6 groups with random means (2-8) and errors. Plot horizontal error bars (ax.errorbar with fmt=\'o\', xerr=...) with capsize=5. Color bars by quartile (low=green, mid=orange, high=red). Add a vertical reference line at x=5.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(10)\ngroups = [f\'Group {i}\' for i in range(1, 7)]\nmeans  = np.random.uniform(2, 8, 6)\nerrors = np.random.uniform(0.3, 1.2, 6)\n# TODO: horizontal errorbar plot\n# TODO: color by quartile\n# TODO: vertical reference line at x=5\n# TODO: save \'hbar_errors.png\'"
}
},

{
"title": "18. Box Plots & Violin Plots",
"desc": "Compare distributions across groups with boxplot() for quartile summaries and violinplot() for full density shapes. Combine both for richer insights.",
"examples": [
        {"label": "Side-by-side box plots", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\ndata = [np.random.normal(loc, 1.0, 80) for loc in [2, 3.5, 2.8, 4.2, 3.0]]\nlabels = [\'A\', \'B\', \'C\', \'D\', \'E\']\n\nfig, ax = plt.subplots(figsize=(8, 5))\nbp = ax.boxplot(data, labels=labels, patch_artist=True, notch=True,\n                medianprops=dict(color=\'white\', linewidth=2))\ncolors = [\'#4c72b0\',\'#dd8452\',\'#55a868\',\'#c44e52\',\'#8172b2\']\nfor patch, color in zip(bp[\'boxes\'], colors):\n    patch.set_facecolor(color)\n    patch.set_alpha(0.8)\nax.set_xlabel(\'Group\')\nax.set_ylabel(\'Value\')\nax.set_title(\'Notched Box Plots by Group\')\nax.grid(True, axis=\'y\', alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'boxplot.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved boxplot.png\')"},
        {"label": "Violin plot with overlaid box", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(1)\ndata = [np.concatenate([np.random.normal(0, 1, 60),\n                         np.random.normal(3, 0.5, 20)])\n        for _ in range(4)]\nlabels = [\'Q1\', \'Q2\', \'Q3\', \'Q4\']\n\nfig, ax = plt.subplots(figsize=(8, 5))\nparts = ax.violinplot(data, positions=range(1, 5), showmedians=True,\n                       showextrema=True)\nfor pc in parts[\'bodies\']:\n    pc.set_facecolor(\'#4c72b0\')\n    pc.set_alpha(0.7)\nax.boxplot(data, positions=range(1, 5), widths=0.1,\n           patch_artist=True,\n           boxprops=dict(facecolor=\'white\', linewidth=1),\n           medianprops=dict(color=\'red\', linewidth=2),\n           whiskerprops=dict(linewidth=1),\n           capprops=dict(linewidth=1),\n           flierprops=dict(markersize=3))\nax.set_xticks(range(1, 5)); ax.set_xticklabels(labels)\nax.set_title(\'Violin + Box Plot Overlay\')\nax.grid(True, axis=\'y\', alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'violin_box.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved violin_box.png\')"},
        {"label": "Grouped box plots with hue", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(2)\nn = 60\nmonths = [\'Jan\', \'Feb\', \'Mar\', \'Apr\']\ntreatments = [\'Control\', \'Treatment\']\nx_pos = np.array([0, 1, 2, 3])\nwidth = 0.35\n\nfig, ax = plt.subplots(figsize=(9, 5))\nfor i, (trt, color) in enumerate(zip(treatments, [\'#4c72b0\',\'#dd8452\'])):\n    data = [np.random.normal(2 + i * 0.8 + j * 0.3, 0.7, n) for j in range(4)]\n    bp = ax.boxplot(data, positions=x_pos + (i - 0.5) * width,\n                    widths=width * 0.85, patch_artist=True,\n                    medianprops=dict(color=\'white\', linewidth=2))\n    for patch in bp[\'boxes\']:\n        patch.set_facecolor(color); patch.set_alpha(0.75)\nax.set_xticks(x_pos); ax.set_xticklabels(months)\nax.set_xlabel(\'Month\'); ax.set_ylabel(\'Score\')\nax.set_title(\'Grouped Box Plots: Control vs Treatment\')\nhandles = [plt.Rectangle((0,0),1,1, color=c, alpha=0.75) for c in [\'#4c72b0\',\'#dd8452\']]\nax.legend(handles, treatments)\nax.grid(True, axis=\'y\', alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'grouped_box.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved grouped_box.png\')"},
        {"label": "Half-violin with jitter (raincloud style)", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\ngroups = [\'Low\', \'Mid\', \'High\']\ndata = [np.random.normal(m, 0.8, 80) for m in [1.5, 3.0, 4.5]]\ncolors = [\'#5ab4d6\', \'#f4a261\', \'#e76f51\']\n\nfig, ax = plt.subplots(figsize=(8, 5))\nfor i, (d, c) in enumerate(zip(data, colors)):\n    parts = ax.violinplot([d], positions=[i], showmedians=False,\n                          showextrema=False)\n    for pc in parts[\'bodies\']:\n        pc.set_facecolor(c); pc.set_alpha(0.6)\n        # half violin: mask right side\n        verts = pc.get_paths()[0].vertices\n        verts[:, 0] = np.clip(verts[:, 0], -np.inf, i)\n        pc.get_paths()[0].vertices = verts\n    # jitter\n    jitter = np.random.uniform(-0.05, 0.05, len(d))\n    ax.scatter(i + 0.05 + jitter, d, alpha=0.4, s=15, color=c)\n    ax.hlines(np.median(d), i - 0.3, i + 0.1, colors=\'black\', linewidth=2)\nax.set_xticks(range(3)); ax.set_xticklabels(groups)\nax.set_title(\'Raincloud Plot (Half Violin + Jitter)\')\nax.grid(True, axis=\'y\', alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'raincloud.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved raincloud.png\')"}
    ],
"rw": {
    "title": "Product Quality Distribution",
    "scenario": "QA team needs to compare defect rates across 5 production lines for 3 shifts. Use grouped notched box plots with color coding, outlier markers, and a horizontal threshold line.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(99)\nlines = [\'L1\',\'L2\',\'L3\',\'L4\',\'L5\']\nshifts = [\'Morning\',\'Afternoon\',\'Night\']\ncolors = [\'#2196f3\',\'#ff9800\',\'#9c27b0\']\nx_pos = np.arange(5)\nwidth = 0.25\n\nfig, ax = plt.subplots(figsize=(11, 5))\nfor si, (shift, col) in enumerate(zip(shifts, colors)):\n    data = [np.random.exponential(1 + si * 0.5 + li * 0.2, 50) for li in range(5)]\n    bp = ax.boxplot(data, positions=x_pos + (si-1)*width, widths=width*0.85,\n                    patch_artist=True, notch=True,\n                    medianprops=dict(color=\'white\', linewidth=2),\n                    flierprops=dict(marker=\'x\', color=col, markersize=5))\n    for patch in bp[\'boxes\']:\n        patch.set_facecolor(col); patch.set_alpha(0.75)\nax.axhline(3.0, color=\'red\', linestyle=\'--\', linewidth=1.5, label=\'Threshold\')\nax.set_xticks(x_pos); ax.set_xticklabels(lines)\nax.set_xlabel(\'Production Line\'); ax.set_ylabel(\'Defects per 100 units\')\nax.set_title(\'Quality Control: Defects by Line & Shift\', fontweight=\'bold\')\nhandles = [plt.Rectangle((0,0),1,1,color=c,alpha=0.75) for c in colors] +           [plt.Line2D([0],[0],color=\'red\',linestyle=\'--\')]\nax.legend(handles, shifts + [\'Threshold\'], ncol=4)\nax.grid(True, axis=\'y\', alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'qc_boxplot.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved qc_boxplot.png\')"
},
"practice": {
    "title": "Distribution Comparison Practice",
    "desc": "Create 4 groups of data: bimodal (two Gaussians mixed), right-skewed (exponential), uniform, and heavy-tailed (Student-t df=2). Plot violin plots in a 2x2 subplot grid. Add the mean as a diamond marker and IQR as a vertical line on each.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(5)\nbimodal  = np.concatenate([np.random.normal(-2,0.5,100), np.random.normal(2,0.5,100)])\nskewed   = np.random.exponential(1.5, 200)\nuniform  = np.random.uniform(-3, 3, 200)\nheavy    = np.random.standard_t(df=2, size=200)\ndatasets = [bimodal, skewed, uniform, heavy]\ntitles   = [\'Bimodal\', \'Right-Skewed\', \'Uniform\', \'Heavy-Tailed\']\n\nfig, axes = plt.subplots(2, 2, figsize=(9, 7))\nfor ax, d, title in zip(axes.flat, datasets, titles):\n    ax.violinplot([d], showmedians=True, showextrema=True)\n    # TODO: add mean as diamond marker\n    # TODO: label the title\n    pass\nfig.suptitle(\'Distribution Shapes Comparison\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'dist_shapes.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved dist_shapes.png\')"
}
},

{
"title": "19. Contour Plots",
"desc": "Use contour() for lines and contourf() for filled regions to display 2D scalar fields, decision boundaries, and topographic data.",
"examples": [
        {"label": "Basic contour and contourf", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = y = np.linspace(-3, 3, 200)\nX, Y = np.meshgrid(x, y)\nZ = np.sin(X) * np.cos(Y)\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))\n# Filled contour\ncf = ax1.contourf(X, Y, Z, levels=20, cmap=\'RdBu_r\')\nfig.colorbar(cf, ax=ax1, label=\'Z\')\nax1.set_title(\'contourf — filled\')\n\n# Line contour with labels\ncs = ax2.contour(X, Y, Z, levels=15, cmap=\'RdBu_r\')\nax2.clabel(cs, inline=True, fontsize=8, fmt=\'%.1f\')\nax2.set_title(\'contour — lines with labels\')\n\nfor ax in (ax1, ax2):\n    ax.set_xlabel(\'x\'); ax.set_ylabel(\'y\')\nfig.tight_layout()\nfig.savefig(\'contour_basic.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved contour_basic.png\')"},
        {"label": "Decision boundary visualization", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.colors import ListedColormap\n\nnp.random.seed(0)\nX_cls = np.random.randn(200, 2)\ny_cls = ((X_cls[:,0]**2 + X_cls[:,1]**2) < 1.5).astype(int)\n\nxx, yy = np.meshgrid(np.linspace(-3,3,300), np.linspace(-3,3,300))\nr = xx**2 + yy**2\nzz = (r < 1.5).astype(float)\n\nfig, ax = plt.subplots(figsize=(6, 5))\nax.contourf(xx, yy, zz, alpha=0.3, cmap=ListedColormap([\'#ff7f7f\',\'#7fbfff\']))\nax.contour(xx, yy, zz, colors=\'black\', linewidths=1.5)\ncolors_pt = [\'#cc0000\' if yi else \'#0055aa\' for yi in y_cls]\nax.scatter(X_cls[:,0], X_cls[:,1], c=colors_pt, s=30, edgecolors=\'k\', linewidths=0.5)\nax.set_title(\'Circular Decision Boundary\')\nax.set_xlabel(\'Feature 1\'); ax.set_ylabel(\'Feature 2\')\nfig.tight_layout()\nfig.savefig(\'decision_boundary.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved decision_boundary.png\')"},
        {"label": "Topographic map with hillshading", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.colors import LightSource\n\nx = y = np.linspace(0, 4*np.pi, 300)\nX, Y = np.meshgrid(x, y)\nZ = np.sin(X/2) * np.cos(Y/3) + 0.5*np.sin(X + Y)\n\nls = LightSource(azdeg=315, altdeg=45)\nhillshade = ls.hillshade(Z, vert_exag=1.5)\n\nfig, ax = plt.subplots(figsize=(8, 6))\nax.imshow(hillshade, cmap=\'gray\', origin=\'lower\', alpha=0.6)\ncf = ax.contourf(Z, levels=25, cmap=\'terrain\', alpha=0.7, origin=\'lower\')\ncs = ax.contour(Z, levels=10, colors=\'k\', linewidths=0.5, alpha=0.5, origin=\'lower\')\nfig.colorbar(cf, ax=ax, label=\'Elevation\')\nax.set_title(\'Topographic Map with Hillshading\')\nfig.tight_layout()\nfig.savefig(\'topo_map.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved topo_map.png\')"},
        {"label": "Contour overlay on scatter", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom scipy.stats import gaussian_kde\n\nnp.random.seed(3)\nx = np.concatenate([np.random.normal(0,1,150), np.random.normal(3,0.8,100)])\ny = np.concatenate([np.random.normal(0,1,150), np.random.normal(2,0.8,100)])\n\n# KDE over a grid\nxi = np.linspace(x.min()-1, x.max()+1, 150)\nyi = np.linspace(y.min()-1, y.max()+1, 150)\nXi, Yi = np.meshgrid(xi, yi)\nk = gaussian_kde(np.vstack([x, y]))\nZi = k(np.vstack([Xi.ravel(), Yi.ravel()])).reshape(Xi.shape)\n\nfig, ax = plt.subplots(figsize=(7, 6))\nax.scatter(x, y, s=15, alpha=0.4, color=\'steelblue\')\ncf = ax.contourf(Xi, Yi, Zi, levels=10, cmap=\'Blues\', alpha=0.5)\nax.contour(Xi, Yi, Zi, levels=10, colors=\'navy\', linewidths=0.8, alpha=0.7)\nfig.colorbar(cf, ax=ax, label=\'Density\')\nax.set_title(\'KDE Contour Overlay on Scatter\')\nfig.tight_layout()\nfig.savefig(\'kde_contour.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved kde_contour.png\')"}
    ],
"rw": {
    "title": "Loss Landscape Visualization",
    "scenario": "Plot the loss surface of a simplified neural network (Z = (X-1)^2 + 2*(Y+0.5)^2 + 0.5*sin(3X)) with a filled contour, gradient-descent path overlay, and start/end markers.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(-2, 3, 300)\ny = np.linspace(-2.5, 1.5, 300)\nX, Y = np.meshgrid(x, y)\nZ = (X-1)**2 + 2*(Y+0.5)**2 + 0.5*np.sin(3*X)\n\n# Simulated gradient-descent path\npath_x = [-1.5]\npath_y = [-2.0]\nlr = 0.1\nfor _ in range(40):\n    gx = 2*(path_x[-1]-1) + 1.5*np.cos(3*path_x[-1])\n    gy = 4*(path_y[-1]+0.5)\n    path_x.append(path_x[-1] - lr*gx)\n    path_y.append(path_y[-1] - lr*gy)\n\nfig, ax = plt.subplots(figsize=(8, 6))\ncf = ax.contourf(X, Y, Z, levels=30, cmap=\'viridis\')\nfig.colorbar(cf, ax=ax, label=\'Loss\')\nax.contour(X, Y, Z, levels=15, colors=\'white\', linewidths=0.5, alpha=0.4)\nax.plot(path_x, path_y, \'w-o\', markersize=4, linewidth=1.5, label=\'GD path\')\nax.plot(path_x[0], path_y[0], \'rs\', markersize=10, label=\'Start\')\nax.plot(path_x[-1], path_y[-1], \'r*\', markersize=14, label=\'End\')\nax.set_xlabel(\'w1\'); ax.set_ylabel(\'w2\')\nax.set_title(\'Loss Landscape & Gradient Descent\', fontweight=\'bold\')\nax.legend(facecolor=\'#222\')\nfig.tight_layout()\nfig.savefig(\'loss_landscape.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved loss_landscape.png\')"
},
"practice": {
    "title": "Contour Practice",
    "desc": "Create Z = cos(sqrt(X^2 + Y^2)) for X,Y in [-6,6]. Plot: (1) filled contour with \'plasma\' colormap, (2) white contour lines at 10 levels, (3) colorbar labeled \'Amplitude\'. Add a red star marker at (0,0) where the function is maximum.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = y = np.linspace(-6, 6, 300)\nX, Y = np.meshgrid(x, y)\nZ = np.cos(np.sqrt(X**2 + Y**2))\n\nfig, ax = plt.subplots(figsize=(7, 6))\n# TODO: contourf with plasma cmap\n# TODO: white contour lines, 10 levels\n# TODO: colorbar labeled \'Amplitude\'\n# TODO: red star marker at (0, 0)\n# TODO: save \'ripple.png\'\nplt.close()"
}
},

{
"title": "20. Polar Plots",
"desc": "Use polar projections for directional data, radar charts, and rose diagrams. Access the polar axes with subplot_kw={\'projection\':\'polar\'}.",
"examples": [
        {"label": "Basic polar line and fill", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\ntheta = np.linspace(0, 2*np.pi, 300)\nr = 1 + 0.5 * np.cos(3*theta)\n\nfig, ax = plt.subplots(figsize=(6, 6), subplot_kw={\'projection\': \'polar\'})\nax.plot(theta, r, color=\'steelblue\', linewidth=2)\nax.fill(theta, r, color=\'steelblue\', alpha=0.2)\nax.set_title(\'Rose Curve: 1 + 0.5·cos(3θ)\', pad=20)\nax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'polar_rose.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved polar_rose.png\')"},
        {"label": "Wind rose bar chart", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(5)\nn_dirs = 16\ntheta_bars = np.linspace(0, 2*np.pi, n_dirs, endpoint=False)\nradii = np.abs(np.random.randn(n_dirs)) * 10 + 5\nwidth = 2*np.pi / n_dirs\n\nfig, ax = plt.subplots(figsize=(7, 7), subplot_kw={\'projection\': \'polar\'})\nbars = ax.bar(theta_bars, radii, width=width, bottom=0,\n              color=plt.cm.hsv(theta_bars / (2*np.pi)), alpha=0.8, edgecolor=\'white\')\nax.set_theta_direction(-1)\nax.set_theta_zero_location(\'N\')\ndirs = [\'N\',\'NNE\',\'NE\',\'ENE\',\'E\',\'ESE\',\'SE\',\'SSE\',\n        \'S\',\'SSW\',\'SW\',\'WSW\',\'W\',\'WNW\',\'NW\',\'NNW\']\nax.set_xticks(theta_bars)\nax.set_xticklabels(dirs, fontsize=8)\nax.set_title(\'Wind Rose Diagram\', pad=20, fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'wind_rose.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved wind_rose.png\')"},
        {"label": "Radar / spider chart", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\ncategories = [\'Speed\',\'Strength\',\'Defense\',\'Agility\',\'Intelligence\',\'Stamina\']\nN = len(categories)\nangles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()\nangles += angles[:1]  # close the loop\n\nplayer_a = [8, 6, 7, 9, 5, 7]\nplayer_b = [5, 9, 8, 4, 7, 6]\nfor v in (player_a, player_b):\n    v.append(v[0])\n\nfig, ax = plt.subplots(figsize=(7, 7), subplot_kw={\'projection\': \'polar\'})\nax.plot(angles, player_a, \'o-\', color=\'steelblue\', linewidth=2, label=\'Player A\')\nax.fill(angles, player_a, color=\'steelblue\', alpha=0.2)\nax.plot(angles, player_b, \'s-\', color=\'tomato\', linewidth=2, label=\'Player B\')\nax.fill(angles, player_b, color=\'tomato\', alpha=0.2)\nax.set_xticks(angles[:-1])\nax.set_xticklabels(categories, fontsize=10)\nax.set_ylim(0, 10)\nax.set_title(\'Player Stats Radar Chart\', pad=20, fontweight=\'bold\')\nax.legend(loc=\'upper right\', bbox_to_anchor=(1.3, 1.1))\nfig.tight_layout()\nfig.savefig(\'radar.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved radar.png\')"},
        {"label": "Polar scatter with colormap", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(3)\nn = 200\ntheta = np.random.uniform(0, 2*np.pi, n)\nr = np.random.exponential(2, n)\nc = theta / (2*np.pi)\n\nfig, ax = plt.subplots(figsize=(7, 7), subplot_kw={\'projection\': \'polar\'})\nsc = ax.scatter(theta, r, c=c, cmap=\'hsv\', s=40, alpha=0.7)\nfig.colorbar(sc, ax=ax, label=\'Direction (normalized)\', pad=0.1)\nax.set_title(\'Polar Scatter — Exponential Radii\', pad=20)\nfig.tight_layout()\nfig.savefig(\'polar_scatter.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved polar_scatter.png\')"}
    ],
"rw": {
    "title": "Sales Direction Analysis",
    "scenario": "Visualize monthly sales volume by compass direction for a logistics company. Use a wind-rose style bar chart with bars colored by volume (viridis colormap) and annotated with top 3 directions.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(21)\nn_dirs = 12\nmonths = [\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\',\n          \'Jul\',\'Aug\',\'Sep\',\'Oct\',\'Nov\',\'Dec\']\ntheta_bars = np.linspace(0, 2*np.pi, n_dirs, endpoint=False)\nsales = np.abs(np.random.randn(n_dirs)) * 50 + 80\nwidth = 2*np.pi / n_dirs\n\nfig, ax = plt.subplots(figsize=(8, 8), subplot_kw={\'projection\': \'polar\'})\nnorm = plt.Normalize(sales.min(), sales.max())\ncolors = plt.cm.viridis(norm(sales))\nbars = ax.bar(theta_bars, sales, width=width, bottom=5,\n              color=colors, alpha=0.85, edgecolor=\'white\')\nax.set_theta_zero_location(\'N\')\nax.set_theta_direction(-1)\nax.set_xticks(theta_bars); ax.set_xticklabels(months, fontsize=9)\nax.set_title(\'Monthly Sales by Direction\', pad=20, fontweight=\'bold\')\n# annotate top 3\ntop3 = np.argsort(sales)[-3:]\nfor idx in top3:\n    ax.annotate(f\'{sales[idx]:.0f}\',\n                xy=(theta_bars[idx], sales[idx]+8),\n                ha=\'center\', fontsize=9, color=\'gold\', fontweight=\'bold\')\nsm = plt.cm.ScalarMappable(cmap=\'viridis\', norm=norm)\nfig.colorbar(sm, ax=ax, label=\'Sales Volume\', pad=0.1)\nfig.tight_layout()\nfig.savefig(\'sales_polar.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved sales_polar.png\')"
},
"practice": {
    "title": "Polar Plot Practice",
    "desc": "Create a radar chart with 8 categories (Communication, Analysis, Design, Coding, Testing, DevOps, Leadership, Creativity). Plot two engineers\' scores (randomly generated 1-10). Close the polygon, fill with alpha=0.2, and add a legend. Save as \'skills_radar.png\'.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\ncategories = [\'Communication\',\'Analysis\',\'Design\',\'Coding\',\n              \'Testing\',\'DevOps\',\'Leadership\',\'Creativity\']\nN = len(categories)\nnp.random.seed(42)\neng1 = np.random.randint(4, 10, N).tolist()\neng2 = np.random.randint(3, 10, N).tolist()\nangles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()\n# TODO: close the polygon (append first element to angles, eng1, eng2)\n# TODO: polar subplot\n# TODO: plot and fill both engineers\n# TODO: set tick labels to categories\n# TODO: save \'skills_radar.png\'"
}
},

{
"title": "21. Stacked Bar & Area Charts",
"desc": "Show part-to-whole relationships over categories or time with stacked bar charts and area plots using stackplot().",
"examples": [
        {"label": "Stacked bar chart", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\ncategories = [\'Q1\',\'Q2\',\'Q3\',\'Q4\']\nproduct_a = [120, 145, 160, 180]\nproduct_b = [90,  110, 95,  130]\nproduct_c = [60,  75,  80,  95]\nx = np.arange(len(categories))\ncolors = [\'#4c72b0\',\'#dd8452\',\'#55a868\']\n\nfig, ax = plt.subplots(figsize=(8, 5))\nax.bar(x, product_a, label=\'Product A\', color=colors[0], width=0.5)\nax.bar(x, product_b, bottom=product_a, label=\'Product B\', color=colors[1], width=0.5)\nbottom_c = [a+b for a,b in zip(product_a, product_b)]\nax.bar(x, product_c, bottom=bottom_c, label=\'Product C\', color=colors[2], width=0.5)\nax.set_xticks(x); ax.set_xticklabels(categories)\nax.set_ylabel(\'Revenue ($K)\')\nax.set_title(\'Quarterly Revenue by Product — Stacked\')\nax.legend(loc=\'upper left\')\nax.grid(True, axis=\'y\', alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'stacked_bar.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved stacked_bar.png\')"},
        {"label": "100% stacked bar (normalized)", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\ncategories = [\'North\',\'South\',\'East\',\'West\',\'Central\']\na = np.array([30, 45, 20, 60, 35])\nb = np.array([50, 30, 55, 25, 40])\nc = np.array([20, 25, 25, 15, 25])\ntotal = a + b + c\na_p, b_p, c_p = a/total*100, b/total*100, c/total*100\nx = np.arange(len(categories))\n\nfig, ax = plt.subplots(figsize=(9, 5))\nax.bar(x, a_p, label=\'Tier 1\', color=\'#4c72b0\', width=0.55)\nax.bar(x, b_p, bottom=a_p, label=\'Tier 2\', color=\'#dd8452\', width=0.55)\nax.bar(x, c_p, bottom=a_p+b_p, label=\'Tier 3\', color=\'#55a868\', width=0.55)\nfor xi, (ap, bp, cp) in enumerate(zip(a_p, b_p, c_p)):\n    ax.text(xi, ap/2, f\'{ap:.0f}%\', ha=\'center\', va=\'center\', fontsize=9, color=\'white\', fontweight=\'bold\')\n    ax.text(xi, ap+bp/2, f\'{bp:.0f}%\', ha=\'center\', va=\'center\', fontsize=9, color=\'white\', fontweight=\'bold\')\n    ax.text(xi, ap+bp+cp/2, f\'{cp:.0f}%\', ha=\'center\', va=\'center\', fontsize=9, fontweight=\'bold\')\nax.set_xticks(x); ax.set_xticklabels(categories)\nax.set_ylabel(\'Percentage\'); ax.set_ylim(0,100)\nax.set_title(\'100% Stacked Bar — Market Share by Region\')\nax.legend(loc=\'upper right\')\nfig.tight_layout()\nfig.savefig(\'stacked_100.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved stacked_100.png\')"},
        {"label": "Stack area chart with stackplot()", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\nmonths = np.arange(1, 13)\ndirect   = np.array([200,210,225,240,260,280,270,290,310,295,320,350])\norganic  = np.array([80, 95, 100,110,125,140,135,150,160,155,175,190])\nreferral = np.array([40, 45, 50, 55, 60, 65, 70, 68, 75, 72, 80, 90])\nlabels_s = [\'Direct\',\'Organic\',\'Referral\']\ncolors_s = [\'#4c72b0\',\'#55a868\',\'#dd8452\']\n\nfig, ax = plt.subplots(figsize=(9, 5))\nax.stackplot(months, direct, organic, referral,\n             labels=labels_s, colors=colors_s, alpha=0.8)\nax.set_xlabel(\'Month\'); ax.set_ylabel(\'Sessions (K)\')\nax.set_title(\'Website Traffic by Source — Stacked Area\')\nax.set_xticks(months)\nax.set_xticklabels([\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\',\n                    \'Jul\',\'Aug\',\'Sep\',\'Oct\',\'Nov\',\'Dec\'], rotation=30)\nax.legend(loc=\'upper left\'); ax.grid(True, alpha=0.2)\nfig.tight_layout()\nfig.savefig(\'stackplot.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved stackplot.png\')"},
        {"label": "Stream graph (centered stackplot)", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(7)\nx = np.linspace(0, 10, 100)\nn_series = 5\nys = [np.abs(np.random.randn(100)).cumsum() * 0.3 + np.random.uniform(1,3)\n      for _ in range(n_series)]\nbaseline = -np.array(ys).sum(axis=0) / 2  # center\n\nfig, ax = plt.subplots(figsize=(10, 5))\ncmap = plt.cm.Set2\nax.stackplot(x, *ys, baseline=\'sym\',\n             colors=[cmap(i/n_series) for i in range(n_series)],\n             alpha=0.85)\nax.set_title(\'Stream Graph (Symmetric Baseline)\')\nax.set_xlabel(\'Time\'); ax.set_ylabel(\'Magnitude\')\nax.grid(True, alpha=0.2)\nfig.tight_layout()\nfig.savefig(\'streamgraph.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved streamgraph.png\')"}
    ],
"rw": {
    "title": "Energy Mix Dashboard",
    "scenario": "Show a country\'s electricity generation mix (Solar, Wind, Hydro, Gas, Coal) over 12 months as a 100% stacked area chart. Annotate the month with highest renewable share.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(15)\nmonths = np.arange(12)\nsolar = 20 + 15*np.sin(np.linspace(0, np.pi, 12)) + np.random.randn(12)*2\nwind  = 18 + 8*np.cos(np.linspace(0, 2*np.pi, 12)) + np.random.randn(12)*2\nhydro = np.full(12, 22.0) + np.random.randn(12)\ngas   = 25 - 5*np.sin(np.linspace(0, np.pi, 12)) + np.random.randn(12)\ncoal  = 100 - solar - wind - hydro - gas\nsources = np.vstack([solar, wind, hydro, gas, coal])\nsources = np.clip(sources, 1, None)\npct = sources / sources.sum(axis=0) * 100\n\nfig, ax = plt.subplots(figsize=(10, 5))\nmnames = [\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\',\'Jul\',\'Aug\',\'Sep\',\'Oct\',\'Nov\',\'Dec\']\nax.stackplot(months, *pct,\n             labels=[\'Solar\',\'Wind\',\'Hydro\',\'Gas\',\'Coal\'],\n             colors=[\'#f9c74f\',\'#90be6d\',\'#43aa8b\',\'#f3722c\',\'#555\'],\n             alpha=0.9)\nren = pct[:3].sum(axis=0)\nbest = ren.argmax()\nax.annotate(f\'Peak renewable\n{ren[best]:.1f}%\',\n            xy=(best, 50), xytext=(best+1, 70),\n            arrowprops=dict(arrowstyle=\'->\', color=\'white\'),\n            fontsize=9, color=\'white\',\n            bbox=dict(boxstyle=\'round\', fc=\'#333\'))\nax.set_xticks(months); ax.set_xticklabels(mnames)\nax.set_ylim(0,100); ax.set_ylabel(\'Share (%)\')\nax.set_title(\'Energy Mix by Month\', fontweight=\'bold\')\nax.legend(loc=\'lower right\', ncol=5, fontsize=8)\nfig.tight_layout()\nfig.savefig(\'energy_mix.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved energy_mix.png\')"
},
"practice": {
    "title": "Stacked Chart Practice",
    "desc": "Create weekly budget allocation data for 5 weeks across categories: Rent, Food, Transport, Entertainment, Savings (make up reasonable values). Plot a stacked bar chart and below it a 100% stacked bar showing the proportion. Use a shared x-axis in a 2x1 subplot.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nweeks = [\'Wk1\',\'Wk2\',\'Wk3\',\'Wk4\',\'Wk5\']\nrent    = np.array([800, 800, 800, 800, 800])\nfood    = np.array([200, 220, 180, 240, 210])\ntransport = np.array([80, 90, 75, 85, 95])\nentertainment = np.array([100, 60, 120, 80, 50])\nsavings = np.array([150, 200, 180, 130, 220])\n\nfig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)\nx = np.arange(len(weeks))\n# TODO: stacked bar on ax1\n# TODO: 100% stacked bar on ax2\n# TODO: legend, labels, title\nfig.tight_layout()\nfig.savefig(\'budget_stacked.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved budget_stacked.png\')"
}
},

{
"title": "22. Step Plots & Eventplot",
"desc": "Use step() and drawstyle=\'steps-*\' for discrete/piecewise data, stairs() for histograms, and eventplot() for spike-train and event sequence data.",
"examples": [
        {"label": "step() and stairs() basics", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.arange(0, 10)\ny = np.array([2, 3, 3, 5, 4, 6, 5, 7, 6, 8])\n\nfig, axes = plt.subplots(1, 3, figsize=(12, 4))\nfor ax, where, title in zip(axes,\n                             [\'pre\',\'mid\',\'post\'],\n                             [\'steps-pre\',\'steps-mid\',\'steps-post\']):\n    ax.step(x, y, where=where, color=\'steelblue\', linewidth=2)\n    ax.scatter(x, y, color=\'steelblue\', zorder=5)\n    ax.set_title(title); ax.grid(True, alpha=0.3)\nfig.suptitle(\'Step Plot Variants\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'step_variants.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved step_variants.png\')"},
        {"label": "Cumulative step (ECDF-style)", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\ndata = np.sort(np.random.normal(5, 1.5, 200))\necdf_y = np.arange(1, len(data)+1) / len(data)\n\nfig, ax = plt.subplots(figsize=(8, 4))\nax.step(data, ecdf_y, where=\'post\', color=\'steelblue\', linewidth=2, label=\'ECDF\')\nax.axhline(0.5, color=\'red\', linestyle=\'--\', linewidth=1, label=\'Median\')\nax.axvline(np.median(data), color=\'red\', linestyle=\'--\', linewidth=1)\nax.set_xlabel(\'Value\'); ax.set_ylabel(\'Cumulative Probability\')\nax.set_title(\'Empirical CDF (step-post)\')\nax.legend(); ax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'ecdf_step.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved ecdf_step.png\')"},
        {"label": "Eventplot: neural spike trains", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(1)\nn_neurons = 5\nspike_trains = [np.sort(np.random.uniform(0, 1, np.random.randint(10, 30)))\n                for _ in range(n_neurons)]\ncolors_ev = plt.cm.tab10(np.linspace(0, 0.5, n_neurons))\n\nfig, ax = plt.subplots(figsize=(10, 4))\nax.eventplot(spike_trains, colors=colors_ev,\n             lineoffsets=range(1, n_neurons+1),\n             linelengths=0.7, linewidths=1.5)\nax.set_xlabel(\'Time (s)\')\nax.set_yticks(range(1, n_neurons+1))\nax.set_yticklabels([f\'Neuron {i}\' for i in range(1, n_neurons+1)])\nax.set_title(\'Neural Spike Train Raster Plot\')\nax.set_xlim(0, 1)\nax.grid(True, axis=\'x\', alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'spike_raster.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved spike_raster.png\')"},
        {"label": "Step with fill for discrete signal", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(2)\nt = np.arange(0, 50)\nsignal = np.where(np.random.rand(50) > 0.6, 1, 0)\nsignal[10:15] = 1; signal[30:38] = 1  # force some pulses\n\nfig, ax = plt.subplots(figsize=(10, 3))\nax.step(t, signal, where=\'post\', color=\'steelblue\', linewidth=1.5)\nax.fill_between(t, signal, step=\'post\', alpha=0.2, color=\'steelblue\')\nax.set_ylim(-0.1, 1.4)\nax.set_xlabel(\'Time (ms)\'); ax.set_ylabel(\'State\')\nax.set_title(\'Digital Signal — Step Fill\')\nax.set_yticks([0, 1]); ax.set_yticklabels([\'OFF\', \'ON\'])\nax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'digital_signal.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved digital_signal.png\')"}
    ],
"rw": {
    "title": "System Event Log Visualization",
    "scenario": "Visualize server events across 5 services over 60 seconds: each service fires random events. Use eventplot with different colors per service and add a shaded incident window (t=20–35).",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(8)\nservices = [\'API\',\'DB\',\'Cache\',\'Auth\',\'Queue\']\nevents = [np.sort(np.random.uniform(0, 60, np.random.randint(8, 25)))\n          for _ in services]\ncolors_svc = [\'#4c72b0\',\'#dd8452\',\'#55a868\',\'#c44e52\',\'#9467bd\']\n\nfig, ax = plt.subplots(figsize=(11, 4))\nax.eventplot(events, colors=colors_svc,\n             lineoffsets=range(1, len(services)+1),\n             linelengths=0.6, linewidths=2)\nax.axvspan(20, 35, color=\'red\', alpha=0.1, label=\'Incident window\')\nax.axvline(20, color=\'red\', linestyle=\'--\', linewidth=1)\nax.axvline(35, color=\'red\', linestyle=\'--\', linewidth=1)\nax.set_xlabel(\'Time (s)\'); ax.set_xlim(0, 60)\nax.set_yticks(range(1, len(services)+1)); ax.set_yticklabels(services)\nax.set_title(\'Service Event Log — 60s Window\', fontweight=\'bold\')\nax.legend(loc=\'upper right\')\nax.grid(True, axis=\'x\', alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'event_log.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved event_log.png\')"
},
"practice": {
    "title": "Step Plot Practice",
    "desc": "Simulate a 3-state machine (IDLE=0, RUNNING=1, ERROR=2) over 80 time steps using random transitions. Plot it with step(where=\'post\') and fill_between for each state using different colors. Add a legend for the three states.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(11)\nt = np.arange(80)\nstate = np.zeros(80, dtype=int)\nfor i in range(1, 80):\n    if np.random.rand() < 0.1:\n        state[i] = np.random.choice([0, 1, 2])\n    else:\n        state[i] = state[i-1]\n\nfig, ax = plt.subplots(figsize=(11, 3))\n# TODO: step plot with post\n# TODO: fill_between for state=0 (blue), 1 (green), 2 (red)\n# TODO: add legend, labels, title\n# TODO: save \'state_machine.png\'\nplt.close()"
}
},

{
"title": "23. Log Scale & Symlog",
"desc": "Use set_xscale/set_yscale with \'log\', \'symlog\', or \'logit\' to handle data spanning many orders of magnitude.",
"examples": [
        {"label": "Log-log plot: power-law relationship", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.logspace(0, 4, 100)\ny_power = 2.5 * x**1.7\nnoise = np.random.lognormal(0, 0.1, 100)\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))\nax1.plot(x, y_power * noise, \'o\', markersize=4, alpha=0.6, color=\'steelblue\')\nax1.set_title(\'Linear Scale\'); ax1.set_xlabel(\'x\'); ax1.set_ylabel(\'y\')\nax1.grid(True, alpha=0.3)\n\nax2.loglog(x, y_power * noise, \'o\', markersize=4, alpha=0.6, color=\'steelblue\')\nax2.loglog(x, y_power, \'r--\', linewidth=2, label=r\'y = 2.5 x^{1.7}\')\nax2.set_title(\'Log-Log Scale\'); ax2.set_xlabel(\'x\'); ax2.set_ylabel(\'y\')\nax2.legend(); ax2.grid(True, which=\'both\', alpha=0.3)\nfig.suptitle(\'Power-Law: Linear vs Log-Log\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'loglog.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved loglog.png\')"},
        {"label": "Semilog: exponential decay", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nt = np.linspace(0, 10, 200)\ndecay_fast = np.exp(-0.8 * t)\ndecay_slow = np.exp(-0.2 * t)\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))\nfor ax, scale, title in [(ax1, \'linear\', \'Linear Y\'), (ax2, \'log\', \'Log Y\')]:\n    ax.plot(t, decay_fast, label=\'Fast (k=0.8)\', linewidth=2)\n    ax.plot(t, decay_slow, label=\'Slow (k=0.2)\', linewidth=2, linestyle=\'--\')\n    ax.set_yscale(scale)\n    ax.set_xlabel(\'Time\'); ax.set_ylabel(\'Concentration\')\n    ax.set_title(title); ax.legend(); ax.grid(True, which=\'both\', alpha=0.3)\nfig.suptitle(\'Exponential Decay on Linear vs Semilog\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'semilog.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved semilog.png\')"},
        {"label": "Symlog: signed data spanning zero", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\nx = np.linspace(-1000, 1000, 500)\ny = x + np.random.randn(500) * 50\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))\nax1.scatter(x, y, s=8, alpha=0.5, color=\'steelblue\')\nax1.set_title(\'Linear Scale\')\n\nax2.scatter(x, y, s=8, alpha=0.5, color=\'steelblue\')\nax2.set_xscale(\'symlog\', linthresh=10)\nax2.set_yscale(\'symlog\', linthresh=10)\nax2.set_title(\'Symlog Scale (linthresh=10)\')\n\nfor ax in (ax1, ax2):\n    ax.axhline(0, color=\'gray\', linewidth=0.8)\n    ax.axvline(0, color=\'gray\', linewidth=0.8)\n    ax.grid(True, which=\'both\', alpha=0.3)\n    ax.set_xlabel(\'X\'); ax.set_ylabel(\'Y\')\nfig.tight_layout()\nfig.savefig(\'symlog.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved symlog.png\')"},
        {"label": "Log scale with minor grid and custom ticks", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nimport matplotlib.ticker as ticker\n\nf = np.logspace(1, 5, 300)  # 10 Hz to 100 kHz\ngain_db = -20 * np.log10(1 + (f/1000)**2)  # simple LP filter\n\nfig, ax = plt.subplots(figsize=(9, 4))\nax.semilogx(f, gain_db, color=\'steelblue\', linewidth=2)\nax.axhline(-3, color=\'red\', linestyle=\'--\', linewidth=1, label=\'-3 dB cutoff\')\nax.axvline(1000, color=\'red\', linestyle=\'--\', linewidth=1)\nax.set_xlabel(\'Frequency (Hz)\')\nax.set_ylabel(\'Gain (dB)\')\nax.set_title(\'Bode Plot — Low-Pass Filter\')\nax.grid(True, which=\'both\', alpha=0.3)\nax.xaxis.set_major_formatter(ticker.FuncFormatter(\n    lambda x, _: f\'{x/1000:.0f}k\' if x >= 1000 else f\'{x:.0f}\'))\nax.legend()\nfig.tight_layout()\nfig.savefig(\'bode.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved bode.png\')"}
    ],
"rw": {
    "title": "Server Response Time Analysis",
    "scenario": "Plot server response time distribution (lognormal data, 10k samples) on both linear and log-x histograms side by side. Overlay the theoretical lognormal PDF. Mark the 95th and 99th percentiles.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\nmu, sigma = 5.5, 0.8   # lognormal params\ndata = np.random.lognormal(mu, sigma, 10000)  # ms\n\np95, p99 = np.percentile(data, [95, 99])\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))\nbins = 80\n\nax1.hist(data, bins=bins, color=\'steelblue\', alpha=0.7, density=True)\nfor p, lab, col in [(p95,\'p95\',\'orange\'),(p99,\'p99\',\'red\')]:\n    ax1.axvline(p, color=col, linestyle=\'--\', linewidth=2, label=f\'{lab}: {p:.0f}ms\')\nax1.set_title(\'Linear Scale\'); ax1.legend(); ax1.grid(True, alpha=0.3)\n\nax2.hist(data, bins=np.logspace(np.log10(data.min()), np.log10(data.max()), bins),\n         color=\'steelblue\', alpha=0.7, density=True)\nx_pdf = np.logspace(np.log10(data.min()), np.log10(data.max()), 300)\npdf = (1/(x_pdf * sigma * np.sqrt(2*np.pi))) * np.exp(-(np.log(x_pdf)-mu)**2/(2*sigma**2))\nax2.plot(x_pdf, pdf, \'r-\', linewidth=2, label=\'Lognormal PDF\')\nax2.set_xscale(\'log\')\nfor p, lab, col in [(p95,\'p95\',\'orange\'),(p99,\'p99\',\'red\')]:\n    ax2.axvline(p, color=col, linestyle=\'--\', linewidth=2)\nax2.set_title(\'Log-X Scale\'); ax2.legend(); ax2.grid(True, which=\'both\', alpha=0.3)\n\nfor ax in (ax1, ax2):\n    ax.set_xlabel(\'Response Time (ms)\'); ax.set_ylabel(\'Density\')\nfig.suptitle(\'Server Response Time Distribution\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'response_time.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved response_time.png\')"
},
"practice": {
    "title": "Log Scale Practice",
    "desc": "Generate data: y = 3 * x^(-1.5) for x in [1, 10000] with lognormal noise. Plot on: (1) linear scale, (2) log-log scale with a fitted power-law line, (3) symlog scale. Arrange in a 1x3 figure. Use np.polyfit on log-transformed data to get the exponent.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(6)\nx = np.logspace(0, 4, 200)\ny = 3 * x**(-1.5) * np.random.lognormal(0, 0.15, 200)\n\nfig, axes = plt.subplots(1, 3, figsize=(13, 4))\ntitles = [\'Linear\', \'Log-Log\', \'Symlog\']\nscales = [(\'linear\',\'linear\'), (\'log\',\'log\'), (\'symlog\',\'symlog\')]\n\nfor ax, title, (xs, ys) in zip(axes, titles, scales):\n    ax.scatter(x, y, s=10, alpha=0.5)\n    ax.set_xscale(xs); ax.set_yscale(ys)\n    ax.set_title(title); ax.grid(True, which=\'both\', alpha=0.3)\n    # TODO: on log-log, add fitted power-law line using np.polyfit\n\nfig.suptitle(\'Power Law on Three Scales\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'powerlaw_scales.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved powerlaw_scales.png\')"
}
},

{
"title": "24. GridSpec & Complex Layouts",
"desc": "Go beyond plt.subplots() using GridSpec for unequal column/row spans, subplot_mosaic() for named panels, and add_axes() for insets.",
"examples": [
        {"label": "GridSpec: unequal column widths", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec\n\nnp.random.seed(0)\nfig = plt.figure(figsize=(11, 5))\ngs = GridSpec(2, 3, figure=fig, width_ratios=[2,1,1], hspace=0.4, wspace=0.3)\n\nax_main = fig.add_subplot(gs[:, 0])   # spans both rows, col 0\nax_tr   = fig.add_subplot(gs[0, 1])\nax_br   = fig.add_subplot(gs[1, 1])\nax_tall = fig.add_subplot(gs[:, 2])\n\nx = np.random.randn(200); y = np.random.randn(200)\nax_main.scatter(x, y, s=15, alpha=0.5, color=\'steelblue\')\nax_main.set_title(\'Main Scatter\')\nax_tr.hist(x, bins=20, color=\'steelblue\', alpha=0.7); ax_tr.set_title(\'X dist\')\nax_br.hist(y, bins=20, orientation=\'horizontal\', color=\'tomato\', alpha=0.7)\nax_br.set_title(\'Y dist\')\nax_tall.boxplot([x, y], labels=[\'X\',\'Y\'], patch_artist=True)\nax_tall.set_title(\'Box\')\n\nfig.suptitle(\'GridSpec Complex Layout\', fontweight=\'bold\')\nfig.savefig(\'gridspec.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved gridspec.png\')"},
        {"label": "subplot_mosaic: named panels", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(1)\nlayout = [[\'A\', \'A\', \'B\'],\n          [\'C\', \'D\', \'B\']]\n\nfig, axd = plt.subplot_mosaic(layout, figsize=(11, 6),\n                               gridspec_kw={\'hspace\':0.35,\'wspace\':0.3})\n\nx = np.linspace(0, 10, 100)\naxd[\'A\'].plot(x, np.sin(x), color=\'steelblue\'); axd[\'A\'].set_title(\'A: Wide Line\')\naxd[\'B\'].imshow(np.random.rand(20,20), cmap=\'viridis\', aspect=\'auto\'); axd[\'B\'].set_title(\'B: Tall Image\')\naxd[\'C\'].bar([\'x\',\'y\',\'z\'], [3,7,5], color=[\'#4c72b0\',\'#dd8452\',\'#55a868\']); axd[\'C\'].set_title(\'C: Bar\')\naxd[\'D\'].scatter(*np.random.randn(2,50), s=20, alpha=0.6); axd[\'D\'].set_title(\'D: Scatter\')\n\nfig.suptitle(\'subplot_mosaic — Named Panels\', fontweight=\'bold\')\nfig.savefig(\'mosaic.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved mosaic.png\')"},
        {"label": "Nested GridSpec for subgrid", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec\n\nnp.random.seed(2)\nfig = plt.figure(figsize=(11, 6))\nouter = GridSpec(1, 2, figure=fig, wspace=0.3)\n\n# Left: single scatter\nax_left = fig.add_subplot(outer[0])\nax_left.scatter(*np.random.randn(2, 80), s=20, alpha=0.5)\nax_left.set_title(\'Left Panel\')\n\n# Right: 2x2 subgrid\ninner = GridSpecFromSubplotSpec(2, 2, subplot_spec=outer[1], hspace=0.4, wspace=0.3)\nfor i in range(4):\n    ax = fig.add_subplot(inner[i])\n    ax.plot(np.random.randn(30).cumsum(), linewidth=1.5)\n    ax.set_title(f\'R{i+1}\', fontsize=9)\n\nfig.suptitle(\'Nested GridSpec\', fontweight=\'bold\')\nfig.savefig(\'nested_gs.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved nested_gs.png\')"},
        {"label": "Inset axis with add_axes", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(3)\nx = np.linspace(0, 10, 300)\ny = np.sin(x) * np.exp(-0.2*x) + np.random.randn(300)*0.05\n\nfig, ax = plt.subplots(figsize=(9, 5))\nax.plot(x, y, color=\'steelblue\', linewidth=1.5)\nax.set_xlabel(\'x\'); ax.set_ylabel(\'y\')\nax.set_title(\'Main Plot with Inset Zoom\')\n\n# Inset: zoom [0, 1.5]\nax_inset = ax.inset_axes([0.55, 0.55, 0.42, 0.38])\nax_inset.plot(x, y, color=\'steelblue\', linewidth=1.5)\nax_inset.set_xlim(0, 1.5); ax_inset.set_ylim(-0.1, 1.05)\nax_inset.set_title(\'Zoom [0,1.5]\', fontsize=8)\nax_inset.tick_params(labelsize=7)\n\nax.indicate_inset_zoom(ax_inset, edgecolor=\'black\')\nax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'inset_axis.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved inset_axis.png\')"}
    ],
"rw": {
    "title": "ML Model Comparison Dashboard",
    "scenario": "Build a 3-panel dashboard: (1) large training-curve plot (loss vs epoch for 3 models), (2) confusion-matrix heatmap, (3) ROC curve — using GridSpec with a 2:1 width ratio for the first column.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec\n\nnp.random.seed(42)\nfig = plt.figure(figsize=(13, 5))\ngs = GridSpec(2, 2, figure=fig, width_ratios=[1.8, 1], hspace=0.4, wspace=0.35)\n\nax_curve = fig.add_subplot(gs[:, 0])\nax_cm    = fig.add_subplot(gs[0, 1])\nax_roc   = fig.add_subplot(gs[1, 1])\n\n# Training curves\nepochs = np.arange(1, 31)\nfor name, color, offset in [(\'CNN\',\'#4c72b0\',0), (\'RNN\',\'#dd8452\',0.3), (\'MLP\',\'#55a868\',0.5)]:\n    loss = 2.5*np.exp(-0.15*epochs) + offset*np.exp(-0.1*epochs) + np.random.randn(30)*0.04\n    ax_curve.plot(epochs, loss, color=color, linewidth=2, label=name)\nax_curve.set_xlabel(\'Epoch\'); ax_curve.set_ylabel(\'Loss\')\nax_curve.set_title(\'Training Loss\'); ax_curve.legend(); ax_curve.grid(True, alpha=0.3)\n\n# Confusion matrix\ncm = np.array([[45,5,2],[3,38,4],[1,2,50]])\nim = ax_cm.imshow(cm, cmap=\'Blues\')\nfor i in range(3):\n    for j in range(3):\n        ax_cm.text(j, i, cm[i,j], ha=\'center\', va=\'center\',\n                   color=\'white\' if cm[i,j] > 30 else \'black\', fontsize=10)\nax_cm.set_title(\'Confusion Matrix\', fontsize=9)\n\n# ROC\nfpr = np.linspace(0, 1, 100)\ntpr = np.sqrt(fpr) * 0.92\nax_roc.plot(fpr, tpr, color=\'steelblue\', linewidth=2, label=\'AUC=0.92\')\nax_roc.plot([0,1],[0,1],\'k--\',linewidth=0.8)\nax_roc.set_xlabel(\'FPR\', fontsize=8); ax_roc.set_ylabel(\'TPR\', fontsize=8)\nax_roc.set_title(\'ROC Curve\', fontsize=9); ax_roc.legend(fontsize=8)\n\nfig.suptitle(\'ML Model Comparison Dashboard\', fontweight=\'bold\')\nfig.savefig(\'ml_dashboard.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved ml_dashboard.png\')"
},
"practice": {
    "title": "GridSpec Practice",
    "desc": "Create a 3x3 GridSpec layout where: cell (0,0) spans 2 columns (title/text placeholder), row 1 has 3 equal plots (sin, cos, tan clipped), and row 2 spans all 3 columns as a wide bar chart. Use fig.add_subplot() with appropriate slicing.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec\n\nfig = plt.figure(figsize=(12, 8))\ngs = GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.3)\nx = np.linspace(0, 2*np.pi, 200)\n\n# Row 0: spans 3 cols — title area\nax_title = fig.add_subplot(gs[0, :])\nax_title.text(0.5, 0.5, \'GridSpec Practice Dashboard\', ha=\'center\', va=\'center\',\n              fontsize=14, fontweight=\'bold\', transform=ax_title.transAxes)\nax_title.axis(\'off\')\n\n# TODO: Row 1: three plots (sin, cos, tan clipped to [-5,5])\n# TODO: Row 2: wide bar chart spanning all 3 cols\n# TODO: save \'gridspec_practice.png\'\nplt.close()"
}
},

{
"title": "25. Hexbin & 2D Density Plots",
"desc": "Use hexbin() for large scatter datasets, hist2d() for rectangular binning, and KDE-based density coloring to visualize joint distributions.",
"examples": [
        {"label": "hexbin with colorbar", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\nn = 5000\nx = np.random.normal(0, 1.5, n)\ny = 0.6*x + np.random.normal(0, 1, n)\n\nfig, ax = plt.subplots(figsize=(7, 5))\nhb = ax.hexbin(x, y, gridsize=40, cmap=\'YlOrRd\', mincnt=1)\ncb = fig.colorbar(hb, ax=ax, label=\'Count\')\nax.set_xlabel(\'X\'); ax.set_ylabel(\'Y\')\nax.set_title(\'Hexbin — 5000 Points\')\nfig.tight_layout()\nfig.savefig(\'hexbin.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved hexbin.png\')"},
        {"label": "2D histogram with hist2d", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(1)\nn = 3000\nx = np.concatenate([np.random.normal(-2, 0.8, n//2), np.random.normal(2, 0.8, n//2)])\ny = np.concatenate([np.random.normal(-1, 1.0, n//2), np.random.normal(1, 1.0, n//2)])\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))\nh, xedges, yedges, img = ax1.hist2d(x, y, bins=40, cmap=\'Blues\')\nfig.colorbar(img, ax=ax1, label=\'Count\')\nax1.set_title(\'hist2d\')\n\nh2, xe, ye, img2 = ax2.hist2d(x, y, bins=40, cmap=\'Blues\',\n                                norm=plt.matplotlib.colors.LogNorm())\nfig.colorbar(img2, ax=ax2, label=\'Log Count\')\nax2.set_title(\'hist2d (log scale)\')\n\nfor ax in (ax1, ax2):\n    ax.set_xlabel(\'X\'); ax.set_ylabel(\'Y\')\nfig.tight_layout()\nfig.savefig(\'hist2d.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved hist2d.png\')"},
        {"label": "Scatter colored by KDE density", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom scipy.stats import gaussian_kde\n\nnp.random.seed(2)\nn = 2000\nx = np.random.multivariate_normal([0,0], [[1,0.7],[0.7,1]], n)[:,0]\ny = np.random.multivariate_normal([0,0], [[1,0.7],[0.7,1]], n)[:,1]\n\nxy = np.vstack([x, y])\nkde = gaussian_kde(xy)\ndensity = kde(xy)\nidx = density.argsort()\n\nfig, ax = plt.subplots(figsize=(7, 6))\nsc = ax.scatter(x[idx], y[idx], c=density[idx], cmap=\'inferno\', s=10, alpha=0.8)\nfig.colorbar(sc, ax=ax, label=\'Density\')\nax.set_xlabel(\'X\'); ax.set_ylabel(\'Y\')\nax.set_title(\'Scatter Colored by KDE Density\')\nfig.tight_layout()\nfig.savefig(\'kde_scatter.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved kde_scatter.png\')"},
        {"label": "Marginal distributions with shared axes", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec\n\nnp.random.seed(3)\nn = 1000\nx = np.random.normal(0, 1, n)\ny = x * 0.8 + np.random.normal(0, 0.6, n)\n\nfig = plt.figure(figsize=(8, 8))\ngs = GridSpec(2, 2, width_ratios=[4,1], height_ratios=[1,4],\n              hspace=0.05, wspace=0.05)\nax_main = fig.add_subplot(gs[1, 0])\nax_top  = fig.add_subplot(gs[0, 0], sharex=ax_main)\nax_side = fig.add_subplot(gs[1, 1], sharey=ax_main)\n\nax_main.hexbin(x, y, gridsize=35, cmap=\'Blues\', mincnt=1)\nax_top.hist(x, bins=40, color=\'steelblue\', alpha=0.7)\nax_side.hist(y, bins=40, orientation=\'horizontal\', color=\'tomato\', alpha=0.7)\n\nplt.setp(ax_top.get_xticklabels(), visible=False)\nplt.setp(ax_side.get_yticklabels(), visible=False)\nax_main.set_xlabel(\'X\'); ax_main.set_ylabel(\'Y\')\nax_top.set_title(\'Hexbin with Marginal Distributions\', fontweight=\'bold\')\nfig.savefig(\'marginal.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved marginal.png\')"}
    ],
"rw": {
    "title": "Customer Purchase Patterns",
    "scenario": "Visualize 20,000 e-commerce transactions (basket_size vs revenue) using hexbin with log-color scale. Add marginal histograms on top and right for each axis. Annotate the high-density region.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec\n\nnp.random.seed(55)\nn = 20000\nbasket = np.random.lognormal(1.5, 0.6, n)\nrevenue = basket * np.random.uniform(15, 80, n) + np.random.normal(0, 20, n)\nrevenue = np.clip(revenue, 1, None)\n\nfig = plt.figure(figsize=(9, 9))\ngs = GridSpec(2, 2, width_ratios=[4,1], height_ratios=[1,4],\n              hspace=0.05, wspace=0.05)\nax = fig.add_subplot(gs[1,0])\nax_top = fig.add_subplot(gs[0,0], sharex=ax)\nax_side = fig.add_subplot(gs[1,1], sharey=ax)\n\nhb = ax.hexbin(basket, revenue, gridsize=50, cmap=\'YlOrRd\', mincnt=1,\n               norm=plt.matplotlib.colors.LogNorm())\nfig.colorbar(hb, ax=ax, label=\'Log Count\')\n\nax_top.hist(basket, bins=50, color=\'#f4a261\', alpha=0.8)\nax_side.hist(revenue, bins=50, orientation=\'horizontal\', color=\'#e76f51\', alpha=0.8)\nplt.setp(ax_top.get_xticklabels(), visible=False)\nplt.setp(ax_side.get_yticklabels(), visible=False)\n\nax.set_xlabel(\'Basket Size (items)\'); ax.set_ylabel(\'Revenue ($)\')\nax.annotate(\'Peak density\', xy=(5, 200), xytext=(12, 500),\n            arrowprops=dict(arrowstyle=\'->\', color=\'black\'),\n            fontsize=9, fontweight=\'bold\')\nax_top.set_title(\'Customer Purchase Patterns\', fontweight=\'bold\')\nfig.savefig(\'purchase_density.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved purchase_density.png\')"
},
"practice": {
    "title": "Density Plot Practice",
    "desc": "Generate 3000 points from a mixture of 3 bivariate Gaussians at (0,0), (3,3), (-2,3). Plot using hexbin (gridsize=30, cmap=\'plasma\'). Overlay contour lines from a KDE. Add a colorbar and axis labels.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom scipy.stats import gaussian_kde\n\nnp.random.seed(7)\ncenters = [(0,0), (3,3), (-2,3)]\nn_each = 1000\npts = np.vstack([np.random.multivariate_normal(c, np.eye(2), n_each) for c in centers])\nx, y = pts[:,0], pts[:,1]\n\nfig, ax = plt.subplots(figsize=(7, 6))\n# TODO: hexbin with plasma cmap\n# TODO: KDE contour overlay\n# TODO: colorbar, axis labels\n# TODO: save \'mixture_density.png\'\nplt.close()"
}
},

{
"title": "26. Patch Artists & Custom Shapes",
"desc": "Draw custom geometric shapes with matplotlib.patches: Rectangle, Circle, Ellipse, Polygon, FancyArrow, and Arc for annotations and diagrams.",
"examples": [
        {"label": "Basic patches: Rectangle, Circle, Ellipse", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nimport matplotlib.patches as mpatches\n\nfig, ax = plt.subplots(figsize=(8, 6))\nax.set_xlim(0, 10); ax.set_ylim(0, 8)\nax.set_aspect(\'equal\')\n\nrect = mpatches.Rectangle((1, 1), 2.5, 1.5, linewidth=2,\n                            edgecolor=\'steelblue\', facecolor=\'lightblue\', alpha=0.8)\ncirc = mpatches.Circle((6, 4), radius=1.5, linewidth=2,\n                         edgecolor=\'tomato\', facecolor=\'lightsalmon\', alpha=0.8)\nellip = mpatches.Ellipse((4, 6), width=3, height=1.2, angle=30,\n                           linewidth=2, edgecolor=\'seagreen\', facecolor=\'lightgreen\', alpha=0.8)\n\nfor patch in [rect, circ, ellip]:\n    ax.add_patch(patch)\n\nax.text(2.25, 1.75, \'Rectangle\', ha=\'center\', fontsize=9)\nax.text(6, 4, \'Circle\', ha=\'center\', fontsize=9)\nax.text(4, 6, \'Ellipse\', ha=\'center\', fontsize=9)\nax.set_title(\'Basic Patch Artists\')\nax.grid(True, alpha=0.2)\nfig.tight_layout()\nfig.savefig(\'patches_basic.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved patches_basic.png\')"},
        {"label": "Polygon and FancyArrow", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nimport matplotlib.patches as mpatches\n\nfig, ax = plt.subplots(figsize=(8, 6))\nax.set_xlim(0, 10); ax.set_ylim(0, 8)\nax.set_aspect(\'equal\')\n\n# Star polygon\nn = 5\nouter = np.array([[np.cos(2*np.pi*i/n - np.pi/2), np.sin(2*np.pi*i/n - np.pi/2)]\n                   for i in range(n)]) * 2.0 + [3, 4]\ninner = np.array([[np.cos(2*np.pi*i/n + np.pi/n - np.pi/2),\n                   np.sin(2*np.pi*i/n + np.pi/n - np.pi/2)]\n                   for i in range(n)]) * 0.8 + [3, 4]\nverts = np.empty((2*n, 2))\nverts[0::2] = outer; verts[1::2] = inner\nstar = mpatches.Polygon(verts, closed=True, facecolor=\'gold\', edgecolor=\'orange\', linewidth=2)\nax.add_patch(star)\n\narrow = mpatches.FancyArrow(5.5, 4, 2, 0, width=0.3,\n                              head_width=0.7, head_length=0.5,\n                              facecolor=\'steelblue\', edgecolor=\'navy\')\nax.add_patch(arrow)\n\narc = mpatches.Arc((8.5, 2), 2, 2, angle=0, theta1=30, theta2=270,\n                    color=\'tomato\', linewidth=2.5)\nax.add_patch(arc)\n\nax.set_title(\'Polygon, FancyArrow, Arc\')\nax.grid(True, alpha=0.2)\nfig.tight_layout()\nfig.savefig(\'patches_advanced.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved patches_advanced.png\')"},
        {"label": "Annotate with FancyBboxPatch callouts", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nimport matplotlib.patches as mpatches\n\nfig, ax = plt.subplots(figsize=(9, 5))\nnp.random.seed(0)\nx = np.linspace(0, 10, 100)\ny = np.sin(x) + np.random.randn(100)*0.1\nax.plot(x, y, color=\'steelblue\', linewidth=2)\n\n# Highlight a region\nhighlight = mpatches.FancyBboxPatch((3.0, -0.3), 2.0, 0.6,\n    boxstyle=\'round,pad=0.1\', linewidth=2,\n    edgecolor=\'gold\', facecolor=\'yellow\', alpha=0.3)\nax.add_patch(highlight)\nax.annotate(\'Peak region\', xy=(4, 0.8), xytext=(6.5, 1.3),\n            arrowprops=dict(arrowstyle=\'->\', color=\'darkred\', lw=2),\n            fontsize=11, color=\'darkred\', fontweight=\'bold\',\n            bbox=dict(boxstyle=\'round,pad=0.3\', facecolor=\'lightyellow\', edgecolor=\'gold\'))\n\nax.set_title(\'Annotations with FancyBboxPatch\')\nax.set_xlabel(\'x\'); ax.set_ylabel(\'y\')\nax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'fancy_annotate.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved fancy_annotate.png\')"},
        {"label": "Pipeline / flowchart diagram", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nimport matplotlib.patches as mpatches\n\nfig, ax = plt.subplots(figsize=(11, 4))\nax.set_xlim(0, 11); ax.set_ylim(0, 4)\nax.set_aspect(\'equal\'); ax.axis(\'off\')\n\nboxes = [\n    (0.5, 1.5, \'Data\nIngestion\', \'#4c72b0\'),\n    (3.0, 1.5, \'Clean &\nTransform\', \'#dd8452\'),\n    (5.5, 1.5, \'Feature\nEngineering\', \'#55a868\'),\n    (8.0, 1.5, \'Model\nTraining\', \'#c44e52\'),\n]\nfor x, y, label, color in boxes:\n    box = mpatches.FancyBboxPatch((x, y), 2, 1,\n        boxstyle=\'round,pad=0.1\', facecolor=color, edgecolor=\'white\',\n        linewidth=2, alpha=0.9)\n    ax.add_patch(box)\n    ax.text(x+1, y+0.5, label, ha=\'center\', va=\'center\',\n            color=\'white\', fontsize=9, fontweight=\'bold\')\n\nfor i in range(len(boxes)-1):\n    x_start = boxes[i][0] + 2\n    x_end   = boxes[i+1][0]\n    y_mid   = 2.0\n    ax.annotate(\'\', xy=(x_end, y_mid), xytext=(x_start, y_mid),\n                arrowprops=dict(arrowstyle=\'->\', color=\'gray\', lw=2))\n\nax.set_title(\'ML Pipeline Diagram\', fontsize=13, fontweight=\'bold\', y=0.95)\nfig.tight_layout()\nfig.savefig(\'pipeline.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved pipeline.png\')"}
    ],
"rw": {
    "title": "Architecture Diagram",
    "scenario": "Draw a 3-tier architecture diagram: Client (circle), Load Balancer (diamond/hexagon), 3 App Servers (rounded rectangles), Database (cylinder-style ellipse). Use FancyArrow for connections and add labels.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nimport matplotlib.patches as mpatches\n\nfig, ax = plt.subplots(figsize=(11, 6))\nax.set_xlim(0, 12); ax.set_ylim(0, 7)\nax.axis(\'off\')\n\n# Client\ncirc = mpatches.Circle((1, 3.5), 0.7, facecolor=\'#4c72b0\', edgecolor=\'white\', lw=2)\nax.add_patch(circ); ax.text(1, 3.5, \'Client\', ha=\'center\', va=\'center\', color=\'white\', fontsize=8, fontweight=\'bold\')\n\n# Load balancer\nlb = mpatches.FancyBboxPatch((2.8, 2.8), 2, 1.4, boxstyle=\'round,pad=0.15\',\n    facecolor=\'#dd8452\', edgecolor=\'white\', lw=2)\nax.add_patch(lb); ax.text(3.8, 3.5, \'Load\nBalancer\', ha=\'center\', va=\'center\', color=\'white\', fontsize=8, fontweight=\'bold\')\n\n# App servers\nfor i, (y, col) in enumerate(zip([1.2, 3.5, 5.8], [\'#55a868\',\'#55a868\',\'#55a868\'])):\n    srv = mpatches.FancyBboxPatch((6.5, y), 1.8, 1.0, boxstyle=\'round,pad=0.1\',\n        facecolor=col, edgecolor=\'white\', lw=2)\n    ax.add_patch(srv)\n    ax.text(7.4, y+0.5, f\'App {i+1}\', ha=\'center\', va=\'center\', color=\'white\', fontsize=8, fontweight=\'bold\')\n    ax.annotate(\'\', xy=(6.5, y+0.5), xytext=(4.8, 3.5),\n                arrowprops=dict(arrowstyle=\'->\', color=\'gray\', lw=1.5))\n\n# DB\ndb = mpatches.Ellipse((10.5, 3.5), 1.4, 0.9, facecolor=\'#c44e52\', edgecolor=\'white\', lw=2)\nax.add_patch(db); ax.text(10.5, 3.5, \'DB\', ha=\'center\', va=\'center\', color=\'white\', fontsize=9, fontweight=\'bold\')\nfor y in [1.7, 3.5, 6.3]:\n    ax.annotate(\'\', xy=(9.8, 3.5), xytext=(8.3, y+0.5 if y != 3.5 else y),\n                arrowprops=dict(arrowstyle=\'->\', color=\'gray\', lw=1.2))\n\nax.annotate(\'\', xy=(2.8, 3.5), xytext=(1.7, 3.5),\n            arrowprops=dict(arrowstyle=\'->\', color=\'gray\', lw=2))\nax.set_title(\'3-Tier Architecture Diagram\', fontsize=13, fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'architecture.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved architecture.png\')"
},
"practice": {
    "title": "Custom Shape Practice",
    "desc": "Draw a Venn diagram of 3 overlapping circles with labels A, B, C and intersection labels (A∩B, B∩C, A∩C, A∩B∩C). Use Circle patches with alpha=0.4 and contrasting colors. Place text annotations in each region.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nimport matplotlib.patches as mpatches\n\nfig, ax = plt.subplots(figsize=(7, 6))\nax.set_xlim(0, 7); ax.set_ylim(0, 7)\nax.set_aspect(\'equal\'); ax.axis(\'off\')\n\n# Three overlapping circles\ncircles = [\n    mpatches.Circle((2.8, 4.2), 2, facecolor=\'#4c72b0\', alpha=0.35, edgecolor=\'navy\', lw=2),\n    mpatches.Circle((4.2, 4.2), 2, facecolor=\'#dd8452\', alpha=0.35, edgecolor=\'darkred\', lw=2),\n    mpatches.Circle((3.5, 2.5), 2, facecolor=\'#55a868\', alpha=0.35, edgecolor=\'darkgreen\', lw=2),\n]\nfor c in circles: ax.add_patch(c)\n\n# TODO: add text labels A, B, C in non-overlapping regions\n# TODO: add intersection labels A∩B, B∩C, A∩C, A∩B∩C\n# TODO: add title and save \'venn3.png\'\nplt.close()"
}
},

{
"title": "27. Quiver & Streamplot",
"desc": "Visualize 2D vector fields with quiver() for arrow grids and streamplot() for continuous flow lines. Used for fluid dynamics, electric fields, and gradient maps.",
"examples": [
        {"label": "Basic quiver plot", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = y = np.linspace(-2, 2, 15)\nX, Y = np.meshgrid(x, y)\nU = -Y      # velocity components\nV =  X\n\nfig, ax = plt.subplots(figsize=(6, 6))\nq = ax.quiver(X, Y, U, V, np.sqrt(U**2+V**2),\n              cmap=\'coolwarm\', scale=30, pivot=\'mid\')\nfig.colorbar(q, ax=ax, label=\'Speed\')\nax.set_title(\'Rotational Vector Field\')\nax.set_xlabel(\'x\'); ax.set_ylabel(\'y\')\nax.set_aspect(\'equal\')\nax.grid(True, alpha=0.2)\nfig.tight_layout()\nfig.savefig(\'quiver_basic.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved quiver_basic.png\')"},
        {"label": "Streamplot with speed coloring", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(-3, 3, 100)\ny = np.linspace(-2, 2, 80)\nX, Y = np.meshgrid(x, y)\nU = 1 - X**2\nV = -Y\n\nspeed = np.sqrt(U**2 + V**2)\n\nfig, ax = plt.subplots(figsize=(9, 5))\nstrm = ax.streamplot(X, Y, U, V, color=speed, cmap=\'plasma\',\n                      linewidth=1.5, density=1.5, arrowsize=1.2)\nfig.colorbar(strm.lines, ax=ax, label=\'Speed\')\nax.set_xlabel(\'x\'); ax.set_ylabel(\'y\')\nax.set_title(\'Streamplot: Flow Field Colored by Speed\')\nax.set_aspect(\'equal\')\nax.grid(True, alpha=0.2)\nfig.tight_layout()\nfig.savefig(\'streamplot.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved streamplot.png\')"},
        {"label": "Gradient field of a scalar function", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = y = np.linspace(-3, 3, 50)\nX, Y = np.meshgrid(x, y)\nZ = np.exp(-(X**2 + Y**2)/2)  # 2D Gaussian\ndZdX, dZdY = np.gradient(Z, x, y)\n\nfig, axes = plt.subplots(1, 2, figsize=(12, 5))\ncf = axes[0].contourf(X, Y, Z, levels=20, cmap=\'viridis\')\nfig.colorbar(cf, ax=axes[0], label=\'f(x,y)\')\naxes[0].set_title(\'Scalar Field: 2D Gaussian\')\n\n# Subsample for quiver\nstep = 4\naxes[1].contourf(X, Y, Z, levels=20, cmap=\'viridis\', alpha=0.5)\naxes[1].quiver(X[::step,::step], Y[::step,::step],\n               dZdX[::step,::step], dZdY[::step,::step],\n               color=\'white\', scale=10, alpha=0.9)\naxes[1].set_title(\'Gradient Field (quiver)\')\n\nfor ax in axes:\n    ax.set_xlabel(\'x\'); ax.set_ylabel(\'y\'); ax.set_aspect(\'equal\')\nfig.tight_layout()\nfig.savefig(\'gradient_field.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved gradient_field.png\')"},
        {"label": "Electric dipole field with streamplot", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(-4, 4, 200)\ny = np.linspace(-3, 3, 150)\nX, Y = np.meshgrid(x, y)\n\n# Two point charges: +1 at (-1,0), -1 at (1,0)\ndef field(q, x0, y0, X, Y):\n    dx, dy = X - x0, Y - y0\n    r3 = (dx**2 + dy**2)**1.5\n    r3 = np.where(r3 < 0.1, 0.1, r3)\n    return q*dx/r3, q*dy/r3\n\nEx1, Ey1 = field(+1, -1, 0, X, Y)\nEx2, Ey2 = field(-1, +1, 0, X, Y)\nEx = Ex1 + Ex2; Ey = Ey1 + Ey2\nspeed = np.sqrt(Ex**2 + Ey**2)\n\nfig, ax = plt.subplots(figsize=(8, 6))\nstrm = ax.streamplot(X, Y, Ex, Ey, color=np.log1p(speed),\n                      cmap=\'coolwarm\', density=1.5, linewidth=1.2)\nax.plot(-1, 0, \'bo\', markersize=12, label=\'+q\')\nax.plot(+1, 0, \'r^\', markersize=12, label=\'-q\')\nfig.colorbar(strm.lines, ax=ax, label=\'log(|E|+1)\')\nax.set_xlim(-4,4); ax.set_ylim(-3,3)\nax.set_title(\'Electric Dipole Field Lines\')\nax.legend(); ax.set_aspect(\'equal\')\nfig.tight_layout()\nfig.savefig(\'dipole_field.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved dipole_field.png\')"}
    ],
"rw": {
    "title": "Ocean Current Visualization",
    "scenario": "Simulate a simplified ocean surface current field with a gyre (circular) pattern plus a northward drift. Plot streamlines colored by speed, add coastline patches, and label the gyre center.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(-5, 5, 150)\ny = np.linspace(-4, 4, 120)\nX, Y = np.meshgrid(x, y)\n\n# Gyre + drift\nU = -Y * np.exp(-(X**2 + Y**2)/8) + 0.2\nV =  X * np.exp(-(X**2 + Y**2)/8) + 0.05*np.cos(Y)\nspeed = np.sqrt(U**2 + V**2)\n\nfig, ax = plt.subplots(figsize=(10, 7))\nstrm = ax.streamplot(X, Y, U, V, color=speed, cmap=\'ocean_r\',\n                      density=2.0, linewidth=1.5, arrowsize=1.1)\nfig.colorbar(strm.lines, ax=ax, label=\'Current Speed (m/s)\')\n\n# Simulated coastline patches\nimport matplotlib.patches as mp\ncoast = mp.Rectangle((3.5,-4), 1.5, 8, facecolor=\'#c2a267\', edgecolor=\'none\', zorder=5)\nax.add_patch(coast)\nax.text(4.25, 0, \'Coast\', ha=\'center\', rotation=90, fontsize=10,\n        fontweight=\'bold\', color=\'#5a3e1b\', zorder=6)\n\nax.plot(0, 0, \'w*\', markersize=14, label=\'Gyre center\', zorder=7)\nax.set_xlim(-5,5); ax.set_ylim(-4,4)\nax.set_xlabel(\'Longitude\'); ax.set_ylabel(\'Latitude\')\nax.set_title(\'Ocean Surface Current Gyre\', fontweight=\'bold\')\nax.legend(loc=\'upper left\')\nfig.tight_layout()\nfig.savefig(\'ocean_current.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved ocean_current.png\')"
},
"practice": {
    "title": "Vector Field Practice",
    "desc": "Create a saddle-point vector field: U = X, V = -Y for X,Y in [-2,2]. Plot (1) quiver and (2) streamplot side by side. Color arrows/lines by speed. Mark the equilibrium point at (0,0) with a star. What type of fixed point is this?",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = y = np.linspace(-2, 2, 20)\nX, Y = np.meshgrid(x, y)\nU =  X\nV = -Y\nspeed = np.sqrt(U**2 + V**2)\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))\n# TODO: quiver on ax1, colored by speed\n# TODO: streamplot on ax2, colored by speed\n# TODO: mark (0,0) with a star on both\n# TODO: add colorbar, labels, titles\n# Hint: saddle point — unstable in x, stable in y\nfig.tight_layout()\nfig.savefig(\'saddle_field.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved saddle_field.png\')"
}
},

{
"title": "28. Broken Axis & Dual Axis",
"desc": "Handle datasets with extreme outliers using a broken y-axis (two subplots with different ylim), and compare two unrelated scales with twinx()/twiny().",
"examples": [
        {"label": "Broken y-axis with diagonal break markers", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\nx = np.arange(10)\ny = np.array([2, 3, 4, 3, 5, 4, 6, 5, 4, 3], dtype=float)\ny[4] = 95   # outlier\n\nfig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(8, 6),\n    sharex=True, gridspec_kw={\'hspace\': 0.08, \'height_ratios\': [1, 3]})\n\nax_top.bar(x, y, color=\'steelblue\', alpha=0.8)\nax_bot.bar(x, y, color=\'steelblue\', alpha=0.8)\n\nax_top.set_ylim(85, 100)\nax_bot.set_ylim(0, 10)\nax_top.spines[\'bottom\'].set_visible(False)\nax_bot.spines[\'top\'].set_visible(False)\nax_top.tick_params(bottom=False)\n\n# Break markers\nd = 0.015\nkwargs = dict(transform=ax_top.transAxes, color=\'k\', clip_on=False, linewidth=1.5)\nax_top.plot((-d, +d), (-d, +d), **kwargs)\nax_top.plot((1-d, 1+d), (-d, +d), **kwargs)\nkwargs.update(transform=ax_bot.transAxes)\nax_bot.plot((-d, +d), (1-d, 1+d), **kwargs)\nax_bot.plot((1-d, 1+d), (1-d, 1+d), **kwargs)\n\nax_bot.set_xlabel(\'Category\')\nfig.text(0.04, 0.5, \'Value\', va=\'center\', rotation=\'vertical\')\nfig.suptitle(\'Broken Y-Axis — Outlier Handling\', fontweight=\'bold\')\nfig.savefig(\'broken_axis.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved broken_axis.png\')"},
        {"label": "twinx: temperature and precipitation", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nmonths = np.arange(1, 13)\ntemp = np.array([2,3,8,14,19,24,27,26,20,14,7,3], dtype=float)\nprecip = np.array([60,50,55,45,55,70,95,110,80,65,70,65], dtype=float)\nmonth_labels = [\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\',\'Jul\',\'Aug\',\'Sep\',\'Oct\',\'Nov\',\'Dec\']\n\nfig, ax1 = plt.subplots(figsize=(10, 5))\nax2 = ax1.twinx()\n\nax1.bar(months, precip, color=\'steelblue\', alpha=0.5, label=\'Precipitation\')\nax2.plot(months, temp, \'ro-\', linewidth=2, markersize=6, label=\'Temperature\')\n\nax1.set_xlabel(\'Month\')\nax1.set_ylabel(\'Precipitation (mm)\', color=\'steelblue\')\nax2.set_ylabel(\'Temperature (°C)\', color=\'tomato\')\nax1.tick_params(axis=\'y\', labelcolor=\'steelblue\')\nax2.tick_params(axis=\'y\', labelcolor=\'tomato\')\nax1.set_xticks(months); ax1.set_xticklabels(month_labels, rotation=30)\n\nlines1, labels1 = ax1.get_legend_handles_labels()\nlines2, labels2 = ax2.get_legend_handles_labels()\nax1.legend(lines1+lines2, labels1+labels2, loc=\'upper left\')\nax1.set_title(\'Climate Chart — twinx()\', fontweight=\'bold\')\nax1.grid(True, alpha=0.2)\nfig.tight_layout()\nfig.savefig(\'twinx_climate.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved twinx_climate.png\')"},
        {"label": "twiny: two x-axes (Hz and ms)", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfreq = np.linspace(10, 1000, 200)   # Hz\nperiod_ms = 1000 / freq              # milliseconds\ngain = 1 / (1 + (freq/100)**2)\n\nfig, ax1 = plt.subplots(figsize=(9, 4))\nax2 = ax1.twiny()\n\nax1.semilogx(freq, gain, color=\'steelblue\', linewidth=2)\nax1.set_xlabel(\'Frequency (Hz)\', color=\'steelblue\')\nax1.tick_params(axis=\'x\', labelcolor=\'steelblue\')\nax1.set_ylabel(\'Gain\')\n\n# Top axis: period in ms (nonuniform tick positions in frequency space)\ntick_freq = [10, 20, 50, 100, 200, 500, 1000]\ntick_labels = [f\'{1000/f:.0f}\' for f in tick_freq]\nax2.set_xscale(\'log\')\nax2.set_xlim(ax1.get_xlim())\nax2.set_xticks(tick_freq)\nax2.set_xticklabels(tick_labels)\nax2.set_xlabel(\'Period (ms)\', color=\'tomato\')\nax2.tick_params(axis=\'x\', labelcolor=\'tomato\')\n\nax1.set_title(\'Low-Pass Filter — Dual Frequency / Period Axes\', fontweight=\'bold\', y=1.15)\nax1.grid(True, which=\'both\', alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'twiny_filter.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved twiny_filter.png\')"},
        {"label": "Multi-panel with broken and twin axes", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(5)\nt = np.arange(24)\nload = np.random.uniform(200, 400, 24)\nload[12] = 950  # midday spike\nprice = 20 + 0.05 * load + np.random.randn(24) * 3\n\nfig = plt.figure(figsize=(11, 7))\nax_t = fig.add_axes([0.1, 0.55, 0.8, 0.22])\nax_b = fig.add_axes([0.1, 0.10, 0.8, 0.40], sharex=ax_t)\nax_r = ax_b.twinx()\n\n# broken axis\nax_t.bar(t, load, color=\'tomato\', alpha=0.7); ax_t.set_ylim(800, 1050)\nax_b.bar(t, load, color=\'tomato\', alpha=0.7); ax_b.set_ylim(0, 500)\nax_t.spines[\'bottom\'].set_visible(False); ax_b.spines[\'top\'].set_visible(False)\nax_t.tick_params(bottom=False)\n\nax_r.plot(t, price, \'b-o\', markersize=4, linewidth=1.5)\nax_r.set_ylabel(\'Price ($/MWh)\', color=\'steelblue\')\nax_r.tick_params(axis=\'y\', labelcolor=\'steelblue\')\nax_b.set_xlabel(\'Hour of Day\')\nax_b.set_ylabel(\'Load (MW)\', color=\'tomato\')\nax_b.tick_params(axis=\'y\', labelcolor=\'tomato\')\nfig.suptitle(\'Grid Load & Price: Broken + Twin Axes\', fontweight=\'bold\', y=0.98)\nfig.savefig(\'broken_twin.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved broken_twin.png\')"}
    ],
"rw": {
    "title": "Stock Price & Volume Dashboard",
    "scenario": "Create a financial chart: top panel shows candlestick-style daily range (high-low as bar, open-close as body using broken axis to exclude an extreme day), bottom panel uses twinx for price (line) and volume (bar).",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(33)\ndays = np.arange(20)\nopens  = 100 + np.random.randn(20).cumsum()\ncloses = opens + np.random.randn(20) * 0.5\nhighs  = np.maximum(opens, closes) + np.abs(np.random.randn(20))*0.8\nlows   = np.minimum(opens, closes) - np.abs(np.random.randn(20))*0.8\nvolume = np.random.randint(100000, 500000, 20).astype(float)\nvolume[9] = 1800000  # volume spike\n\nfig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(11,6),\n    sharex=True, gridspec_kw={\'hspace\':0.1,\'height_ratios\':[2,1]})\nax_vol = ax_bot.twinx()\n\n# Candlestick style\nfor d in days:\n    color = \'seagreen\' if closes[d] >= opens[d] else \'tomato\'\n    ax_top.plot([d,d], [lows[d], highs[d]], color=\'gray\', linewidth=1)\n    ax_top.bar(d, abs(closes[d]-opens[d]), bottom=min(opens[d],closes[d]),\n               color=color, width=0.6, alpha=0.9)\n\nax_bot.bar(days, volume, color=\'steelblue\', alpha=0.5, label=\'Volume\')\nax_vol.plot(days, closes, \'k-\', linewidth=1.5, label=\'Close\')\nax_vol.set_ylabel(\'Price ($)\')\nax_bot.set_ylabel(\'Volume\')\nax_top.set_ylabel(\'Price ($)\')\nax_top.set_title(\'Stock Price & Volume Dashboard\', fontweight=\'bold\')\nax_bot.set_xlabel(\'Day\')\nfig.tight_layout()\nfig.savefig(\'stock_dashboard.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved stock_dashboard.png\')"
},
"practice": {
    "title": "Dual Axis Practice",
    "desc": "Simulate monthly website users (in thousands, growing from 10 to 80 over 12 months) and server costs (in $, growing from 500 to 2000). Plot users as a filled area (fill_between) on left axis and costs as a step line on right axis (twinx). Use contrasting colors and add a legend.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nmonths = np.arange(1, 13)\nusers = np.linspace(10, 80, 12) + np.random.randn(12)*3\ncosts = np.linspace(500, 2000, 12) + np.random.randn(12)*50\nmonth_labels = [\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\',\'Jul\',\'Aug\',\'Sep\',\'Oct\',\'Nov\',\'Dec\']\n\nfig, ax1 = plt.subplots(figsize=(10, 5))\nax2 = ax1.twinx()\n# TODO: fill_between for users on ax1\n# TODO: step line for costs on ax2\n# TODO: contrasting colors, labels, legend, title\n# TODO: save \'users_costs.png\'\nplt.close()"
}
},

{
"title": "29. Image Processing with imshow",
"desc": "Use imshow() for displaying arrays as images, applying colormaps, performing simple transformations, and visualizing feature maps from neural networks.",
"examples": [
        {"label": "Display and compare colormaps", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.colors import Normalize\n\nnp.random.seed(0)\nimg = np.random.randn(40, 40).cumsum(axis=1)\n\ncmaps_show = [\'gray\', \'viridis\', \'plasma\', \'RdBu_r\']\nfig, axes = plt.subplots(1, 4, figsize=(14, 3.5))\nfor ax, cmap in zip(axes, cmaps_show):\n    im = ax.imshow(img, cmap=cmap, aspect=\'auto\')\n    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)\n    ax.set_title(cmap, fontsize=10)\n    ax.axis(\'off\')\nfig.suptitle(\'Same Array — Different Colormaps\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'colormaps_compare.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved colormaps_compare.png\')"},
        {"label": "Image transformations: flip, rotate, crop", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(1)\nimg = np.random.rand(60, 80)\nimg[20:40, 30:60] = 0.85  # bright rectangle\n\ntransforms = {\n    \'Original\': img,\n    \'Flipped H\': np.fliplr(img),\n    \'Rotated 45\': np.rot90(img),\n    \'Cropped\': img[10:50, 20:70],\n}\n\nfig, axes = plt.subplots(1, 4, figsize=(14, 3.5))\nfor ax, (title, arr) in zip(axes, transforms.items()):\n    ax.imshow(arr, cmap=\'gray\', vmin=0, vmax=1)\n    ax.set_title(title, fontsize=10); ax.axis(\'off\')\nfig.suptitle(\'Image Transformations\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'img_transforms.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved img_transforms.png\')"},
        {"label": "Visualize CNN feature maps", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\nn_filters = 8\nfeature_maps = [np.random.randn(28, 28) for _ in range(n_filters)]\nfor i, fm in enumerate(feature_maps):\n    # Simulate different filter responses\n    x = y = np.linspace(-3, 3, 28)\n    X, Y = np.meshgrid(x, y)\n    feature_maps[i] = np.sin(X*(i+1)*0.5) * np.cos(Y*(i+1)*0.3) + np.random.randn(28,28)*0.2\n\nfig, axes = plt.subplots(2, 4, figsize=(12, 6))\nfor ax, fm in zip(axes.flat, feature_maps):\n    im = ax.imshow(fm, cmap=\'RdBu_r\', aspect=\'auto\')\n    plt.colorbar(im, ax=ax, fraction=0.046)\n    ax.axis(\'off\')\nfig.suptitle(\'CNN Feature Maps (Layer 1)\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'feature_maps.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved feature_maps.png\')"},
        {"label": "Overlay: masks, contours, and annotations", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(7)\nh, w = 60, 80\nbg = np.random.randn(h, w)\nsignal_x, signal_y = 50, 30\nfor dy in range(-10, 11):\n    for dx in range(-15, 16):\n        if dx**2/225 + dy**2/100 < 1:\n            bg[signal_y+dy, signal_x+dx] += 3.0\n\nfig, axes = plt.subplots(1, 3, figsize=(14, 4))\n# Raw image\naxes[0].imshow(bg, cmap=\'gray\'); axes[0].set_title(\'Raw\'); axes[0].axis(\'off\')\n\n# Thresholded mask\nmask = (bg > 2.0).astype(float)\naxes[1].imshow(bg, cmap=\'gray\')\naxes[1].imshow(mask, cmap=\'Reds\', alpha=0.5)\naxes[1].set_title(\'Overlay Mask\'); axes[1].axis(\'off\')\n\n# Contour overlay\naxes[2].imshow(bg, cmap=\'gray\')\naxes[2].contour(bg, levels=[1.5, 2.5], colors=[\'yellow\',\'red\'], linewidths=1.5)\naxes[2].annotate(\'Signal\', xy=(signal_x, signal_y), xytext=(signal_x+12, signal_y-12),\n                 arrowprops=dict(arrowstyle=\'->\', color=\'cyan\'),\n                 color=\'cyan\', fontsize=10, fontweight=\'bold\')\naxes[2].set_title(\'Contour Overlay\'); axes[2].axis(\'off\')\nfig.suptitle(\'Image Segmentation Visualization\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'img_overlay.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved img_overlay.png\')"}
    ],
"rw": {
    "title": "Medical Image Analysis Dashboard",
    "scenario": "Simulate a 2D MRI slice (layered Gaussians) and visualize it: (1) raw grayscale, (2) threshold mask in red overlay, (3) gradient magnitude for edge detection, (4) pseudo-color with contour at 50% max intensity.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom scipy.ndimage import gaussian_filter\n\nnp.random.seed(42)\nh, w = 80, 100\nimg = np.zeros((h, w))\nfor cx, cy, r, v in [(50,40,15,1.0),(35,30,8,0.7),(65,50,10,0.8),(45,60,6,0.6)]:\n    y_idx, x_idx = np.ogrid[:h,:w]\n    img += v * np.exp(-((x_idx-cx)**2 + (y_idx-cy)**2)/(2*r**2))\nimg = gaussian_filter(img + np.random.randn(h,w)*0.05, sigma=1.5)\n\nfig, axes = plt.subplots(1, 4, figsize=(14, 4))\n\naxes[0].imshow(img, cmap=\'gray\'); axes[0].set_title(\'Raw MRI Slice\'); axes[0].axis(\'off\')\n\nmask = img > img.max()*0.5\naxes[1].imshow(img, cmap=\'gray\')\naxes[1].imshow(np.ma.masked_where(~mask, img), cmap=\'Reds\', alpha=0.6, vmin=0, vmax=1)\naxes[1].set_title(\'Threshold Mask\'); axes[1].axis(\'off\')\n\ngy, gx = np.gradient(img)\ngrad_mag = np.sqrt(gx**2 + gy**2)\naxes[2].imshow(grad_mag, cmap=\'hot\'); axes[2].set_title(\'Gradient Magnitude\'); axes[2].axis(\'off\')\n\naxes[3].imshow(img, cmap=\'plasma\')\naxes[3].contour(img, levels=[img.max()*0.5], colors=\'white\', linewidths=2)\naxes[3].set_title(\'Pseudo-color + Contour\'); axes[3].axis(\'off\')\n\nfig.suptitle(\'MRI Analysis Dashboard\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'mri_dashboard.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved mri_dashboard.png\')"
},
"practice": {
    "title": "Image Processing Practice",
    "desc": "Create a 50x50 checkerboard pattern (alternating 0 and 1 in 5x5 blocks). Display it in a 1x3 subplot: (1) original with \'gray\' cmap, (2) with \'hot\' cmap and colorbar, (3) with a Gaussian blur applied (use np.convolve or loop-based blur). Add titles.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\n# Build checkerboard\nsize, block = 50, 5\nboard = np.zeros((size, size))\nfor i in range(0, size, block):\n    for j in range(0, size, block):\n        if (i//block + j//block) % 2 == 0:\n            board[i:i+block, j:j+block] = 1\n\nfig, axes = plt.subplots(1, 3, figsize=(11, 4))\n# TODO: original gray cmap\n# TODO: hot cmap with colorbar\n# TODO: blurred version (use gaussian_filter from scipy.ndimage)\n# TODO: add titles and axis(\'off\')\n# TODO: save \'checkerboard.png\'\nplt.close()"
}
},

{
"title": "30. Statistical Plots",
"desc": "Create publication-quality statistical visualizations: regression plots, residual diagnostics, Q-Q plots, correlation matrices, and bootstrapped confidence intervals.",
"examples": [
        {"label": "Scatter with linear regression and confidence band", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(0)\nn = 80\nx = np.linspace(0, 10, n)\ny = 2.5*x + 1.0 + np.random.randn(n)*3\n\n# Manual OLS\ncoeffs = np.polyfit(x, y, 1)\npoly = np.poly1d(coeffs)\ny_pred = poly(x)\nresiduals = y - y_pred\nse = np.std(residuals) * np.sqrt(1/n + (x - x.mean())**2 / ((x - x.mean())**2).sum())\nt_val = 1.99  # ~95% CI for n=80\n\nfig, ax = plt.subplots(figsize=(8, 5))\nax.scatter(x, y, s=25, alpha=0.6, color=\'steelblue\', label=\'Data\')\nax.plot(x, y_pred, \'r-\', linewidth=2, label=f\'y={coeffs[0]:.2f}x+{coeffs[1]:.2f}\')\nax.fill_between(x, y_pred - t_val*se, y_pred + t_val*se,\n                alpha=0.2, color=\'red\', label=\'95% CI\')\nax.set_xlabel(\'X\'); ax.set_ylabel(\'Y\')\nax.set_title(\'Linear Regression with Confidence Band\')\nax.legend(); ax.grid(True, alpha=0.3)\nfig.tight_layout()\nfig.savefig(\'regression_plot.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved regression_plot.png\')"},
        {"label": "Q-Q plot for normality check", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom scipy import stats\n\nnp.random.seed(1)\nfig, axes = plt.subplots(1, 3, figsize=(13, 4))\n\ndatasets = {\n    \'Normal\': np.random.normal(0, 1, 200),\n    \'Right-Skewed\': np.random.exponential(1, 200),\n    \'Heavy-Tailed\': np.random.standard_t(df=3, size=200),\n}\n\nfor ax, (name, data) in zip(axes, datasets.items()):\n    qq = stats.probplot(data, dist=\'norm\')\n    theo, sample = qq[0]\n    ax.scatter(theo, sample, s=15, alpha=0.6, color=\'steelblue\')\n    ax.plot(theo, theo * qq[1][0] + qq[1][1], \'r-\', linewidth=1.5, label=\'Ideal\')\n    ax.set_title(f\'Q-Q Plot: {name}\')\n    ax.set_xlabel(\'Theoretical Quantiles\')\n    ax.set_ylabel(\'Sample Quantiles\')\n    ax.grid(True, alpha=0.3); ax.legend(fontsize=8)\nfig.tight_layout()\nfig.savefig(\'qq_plots.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved qq_plots.png\')"},
        {"label": "Correlation matrix heatmap", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(2)\nn = 200\na = np.random.randn(n)\nb = 0.8*a + np.random.randn(n)*0.6\nc = -0.5*a + np.random.randn(n)*0.8\nd = np.random.randn(n)\ne = 0.6*b + 0.4*d + np.random.randn(n)*0.5\n\ndata_mat = np.vstack([a,b,c,d,e]).T\nlabels = [\'Feature A\',\'Feature B\',\'Feature C\',\'Feature D\',\'Feature E\']\ncorr = np.corrcoef(data_mat.T)\n\nfig, ax = plt.subplots(figsize=(7, 6))\nim = ax.imshow(corr, cmap=\'RdBu_r\', vmin=-1, vmax=1)\nplt.colorbar(im, ax=ax, label=\'Pearson r\')\nax.set_xticks(range(5)); ax.set_xticklabels(labels, rotation=30, ha=\'right\', fontsize=9)\nax.set_yticks(range(5)); ax.set_yticklabels(labels, fontsize=9)\nfor i in range(5):\n    for j in range(5):\n        c_val = corr[i,j]\n        ax.text(j, i, f\'{c_val:.2f}\', ha=\'center\', va=\'center\', fontsize=8,\n                color=\'white\' if abs(c_val) > 0.5 else \'black\')\nax.set_title(\'Correlation Matrix\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'corr_matrix.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved corr_matrix.png\')"},
        {"label": "Bootstrapped confidence interval", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(3)\ndata = np.random.exponential(2, 100)\n\nn_boot = 2000\nboot_means = [np.mean(np.random.choice(data, len(data), replace=True))\n              for _ in range(n_boot)]\n\nci_lo, ci_hi = np.percentile(boot_means, [2.5, 97.5])\ntrue_mean = np.mean(data)\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))\nax1.hist(data, bins=25, color=\'steelblue\', alpha=0.7, density=True)\nax1.axvline(true_mean, color=\'red\', linewidth=2, label=f\'Mean={true_mean:.2f}\')\nax1.set_title(\'Original Data (Exponential)\'); ax1.legend(); ax1.grid(True, alpha=0.3)\n\nax2.hist(boot_means, bins=40, color=\'seagreen\', alpha=0.7, density=True)\nax2.axvline(ci_lo, color=\'red\', linestyle=\'--\', linewidth=2, label=f\'95% CI [{ci_lo:.2f}, {ci_hi:.2f}]\')\nax2.axvline(ci_hi, color=\'red\', linestyle=\'--\', linewidth=2)\nax2.axvline(true_mean, color=\'black\', linewidth=2, label=\'Sample mean\')\nax2.set_title(\'Bootstrap Distribution of Mean\')\nax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)\nfig.suptitle(\'Bootstrapped 95% Confidence Interval\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'bootstrap_ci.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved bootstrap_ci.png\')"}
    ],
"rw": {
    "title": "Regression Diagnostics Panel",
    "scenario": "Fit a polynomial regression (degree 3) on noisy data. Show a 2x2 diagnostic panel: (1) fitted curve on data, (2) residuals vs fitted values, (3) Q-Q plot of residuals, (4) histogram of residuals with normal overlay.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom scipy import stats\n\nnp.random.seed(99)\nx = np.linspace(0, 10, 100)\ny_true = 0.2*x**3 - 3*x**2 + 10*x + 5\ny = y_true + np.random.randn(100)*5\n\ncoeffs = np.polyfit(x, y, 3)\npoly = np.poly1d(coeffs)\ny_hat = poly(x)\nresid = y - y_hat\n\nfig, axes = plt.subplots(2, 2, figsize=(11, 8))\n\n# Fitted curve\naxes[0,0].scatter(x, y, s=20, alpha=0.6, color=\'steelblue\', label=\'Data\')\naxes[0,0].plot(x, y_hat, \'r-\', linewidth=2, label=\'Poly-3 fit\')\naxes[0,0].set_title(\'Fitted Curve\'); axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3)\n\n# Residuals vs fitted\naxes[0,1].scatter(y_hat, resid, s=15, alpha=0.6, color=\'steelblue\')\naxes[0,1].axhline(0, color=\'red\', linestyle=\'--\', linewidth=1.5)\naxes[0,1].set_xlabel(\'Fitted\'); axes[0,1].set_ylabel(\'Residuals\')\naxes[0,1].set_title(\'Residuals vs Fitted\'); axes[0,1].grid(True, alpha=0.3)\n\n# Q-Q plot\nqq = stats.probplot(resid, dist=\'norm\')\ntheo, samp = qq[0]\naxes[1,0].scatter(theo, samp, s=15, alpha=0.6, color=\'steelblue\')\naxes[1,0].plot(theo, theo*qq[1][0]+qq[1][1], \'r-\', linewidth=1.5)\naxes[1,0].set_title(\'Q-Q Plot of Residuals\')\naxes[1,0].set_xlabel(\'Theoretical\'); axes[1,0].set_ylabel(\'Sample\')\naxes[1,0].grid(True, alpha=0.3)\n\n# Residual histogram\naxes[1,1].hist(resid, bins=20, density=True, color=\'steelblue\', alpha=0.7)\nrx = np.linspace(resid.min(), resid.max(), 100)\naxes[1,1].plot(rx, stats.norm.pdf(rx, resid.mean(), resid.std()), \'r-\', linewidth=2)\naxes[1,1].set_title(\'Residual Distribution\'); axes[1,1].grid(True, alpha=0.3)\n\nfig.suptitle(\'Regression Diagnostic Panel\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'regression_diagnostics.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved regression_diagnostics.png\')"
},
"practice": {
    "title": "Statistical Plots Practice",
    "desc": "Generate 5 groups of 50 samples each from distributions with means [1,2,3,4,5] and std=1. Create a 1x2 figure: (1) box plot of all 5 groups with mean markers (diamond), (2) violin plot overlaid with individual jitter points (alpha=0.3, s=15). Use matching colors across panels.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(20)\ngroups = [np.random.normal(mu, 1, 50) for mu in range(1, 6)]\nlabels = [f\'G{i}\' for i in range(1, 6)]\ncolors = [\'#4c72b0\',\'#dd8452\',\'#55a868\',\'#c44e52\',\'#9467bd\']\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))\n# TODO: boxplot on ax1 with mean diamond markers\n# TODO: violinplot on ax2 with jitter scatter overlay\n# TODO: matching colors, labels, titles\n# TODO: save \'group_stats.png\'\nplt.close()"
}
},

{
"title": "31. Multi-Figure Export & Backends",
"desc": "Export single figures at various DPIs, save multiple pages to PDF with PdfPages, create figure collections, and control backends for headless rendering.",
"examples": [
        {"label": "PdfPages: multi-page PDF report", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.backends.backend_pdf import PdfPages\n\nnp.random.seed(0)\npdf_path = \'multi_page_report.pdf\'\n\nwith PdfPages(pdf_path) as pdf:\n    # Page 1: line plot\n    fig, ax = plt.subplots(figsize=(8, 5))\n    x = np.linspace(0, 10, 200)\n    ax.plot(x, np.sin(x), color=\'steelblue\', linewidth=2)\n    ax.set_title(\'Page 1: Sine Wave\')\n    ax.grid(True, alpha=0.3)\n    fig.tight_layout()\n    pdf.savefig(fig); plt.close()\n\n    # Page 2: bar chart\n    fig, ax = plt.subplots(figsize=(8, 5))\n    vals = np.random.randint(10, 100, 8)\n    ax.bar(range(8), vals, color=\'tomato\', alpha=0.8)\n    ax.set_title(\'Page 2: Bar Chart\')\n    fig.tight_layout()\n    pdf.savefig(fig); plt.close()\n\n    # Page 3: scatter\n    fig, ax = plt.subplots(figsize=(8, 5))\n    ax.scatter(*np.random.randn(2, 200), s=20, alpha=0.5)\n    ax.set_title(\'Page 3: Scatter\')\n    fig.tight_layout()\n    pdf.savefig(fig); plt.close()\n\n    d = pdf.infodict()\n    d[\'Title\'] = \'Data Science Report\'\n    d[\'Author\'] = \'matplotlib\'\n\nprint(f\'Saved {pdf_path} (3 pages)\')"},
        {"label": "Export PNG at multiple DPIs", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(1)\nx = np.linspace(0, 2*np.pi, 200)\n\nfig, ax = plt.subplots(figsize=(6, 4))\nax.plot(x, np.sin(x), linewidth=2, color=\'steelblue\', label=\'sin\')\nax.plot(x, np.cos(x), linewidth=2, color=\'tomato\', linestyle=\'--\', label=\'cos\')\nax.legend(); ax.set_title(\'Multi-DPI Export Test\')\nax.grid(True, alpha=0.3)\nfig.tight_layout()\n\nfor dpi in [72, 150, 300]:\n    fname = f\'export_dpi{dpi}.png\'\n    fig.savefig(fname, dpi=dpi, bbox_inches=\'tight\')\n    print(f\'Saved {fname} at {dpi} DPI\')\nplt.close()"},
        {"label": "SVG export for web/vector graphics", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nimport matplotlib\nmatplotlib.rcParams[\'svg.fonttype\'] = \'none\'  # editable text in SVG\n\nnp.random.seed(2)\nfig, axes = plt.subplots(1, 2, figsize=(10, 4))\nx = np.linspace(-3, 3, 100)\naxes[0].plot(x, stats_curve := 1/(1+np.exp(-x)), color=\'steelblue\', linewidth=2)\naxes[0].axhline(0.5, color=\'red\', linestyle=\'--\', linewidth=1)\naxes[0].set_title(\'Sigmoid Function\'); axes[0].grid(True, alpha=0.3)\naxes[0].set_xlabel(\'x\'); axes[0].set_ylabel(\'sigma(x)\')\n\nnp.random.seed(2)\ndata = np.random.randn(100)\naxes[1].hist(data, bins=20, color=\'seagreen\', alpha=0.7, density=True)\naxes[1].set_title(\'Normal Distribution\'); axes[1].grid(True, alpha=0.3)\n\nfig.suptitle(\'SVG Export Example\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'vector_export.svg\', format=\'svg\', bbox_inches=\'tight\')\nfig.savefig(\'vector_export.png\', dpi=150, bbox_inches=\'tight\')\nprint(\'Saved vector_export.svg and vector_export.png\')\nplt.close()"},
        {"label": "Figure with custom metadata and tight layout", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(3)\nfig = plt.figure(figsize=(10, 7))\nfig.set_facecolor(\'#0f1117\')\n\nax1 = fig.add_subplot(2, 2, (1, 2))  # top row, spans both cols\nax2 = fig.add_subplot(2, 2, 3)\nax3 = fig.add_subplot(2, 2, 4)\n\nx = np.linspace(0, 10, 300)\nax1.plot(x, np.sin(x)*np.exp(-0.1*x), color=\'#58a6ff\', linewidth=2)\nax1.set_facecolor(\'#1c2128\'); ax1.tick_params(colors=\'white\')\nfor sp in ax1.spines.values(): sp.set_color(\'#30363d\')\nax1.set_title(\'Damped Oscillation\', color=\'white\')\n\nax2.hist(np.random.randn(500), bins=25, color=\'#79c0ff\', alpha=0.8)\nax2.set_facecolor(\'#1c2128\'); ax2.tick_params(colors=\'white\')\nfor sp in ax2.spines.values(): sp.set_color(\'#30363d\')\nax2.set_title(\'Distribution\', color=\'white\')\n\nax3.scatter(*np.random.randn(2,100), s=15, alpha=0.6, color=\'#ffa657\')\nax3.set_facecolor(\'#1c2128\'); ax3.tick_params(colors=\'white\')\nfor sp in ax3.spines.values(): sp.set_color(\'#30363d\')\nax3.set_title(\'Scatter\', color=\'white\')\n\nfig.suptitle(\'Dark Theme Dashboard\', color=\'white\', fontweight=\'bold\', fontsize=14)\nfig.tight_layout()\nfig.savefig(\'dark_dashboard.png\', dpi=150, bbox_inches=\'tight\',\n            facecolor=fig.get_facecolor())\nplt.close()\nprint(\'Saved dark_dashboard.png\')"}
    ],
"rw": {
    "title": "Automated Report Generation",
    "scenario": "Generate a 4-page PDF report: page 1 cover with title text and logo placeholder, page 2 multi-panel KPI summary, page 3 trend analysis, page 4 summary table rendered as a matplotlib table.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.backends.backend_pdf import PdfPages\n\nnp.random.seed(77)\n\nwith PdfPages(\'automated_report.pdf\') as pdf:\n    # Page 1: cover\n    fig = plt.figure(figsize=(8.5, 11))\n    fig.patch.set_facecolor(\'#1c2128\')\n    ax = fig.add_axes([0,0,1,1]); ax.axis(\'off\')\n    ax.text(0.5,0.65,\'Data Science\nQuarterly Report\', ha=\'center\', va=\'center\',\n            fontsize=28, color=\'white\', fontweight=\'bold\', transform=ax.transAxes)\n    ax.text(0.5,0.45,\'Q1 2025 | Generated by Matplotlib\', ha=\'center\',\n            fontsize=13, color=\'#8b949e\', transform=ax.transAxes)\n    pdf.savefig(fig, facecolor=fig.get_facecolor()); plt.close()\n\n    # Page 2: KPI panel\n    fig, axes = plt.subplots(1,3, figsize=(11,5))\n    kpis = [(\'Revenue\',\'$2.4M\',\'+12%\',\'#4c72b0\'),\n            (\'Users\',\'84K\',\'+8%\',\'#55a868\'),\n            (\'NPS\',\'72\',\'+5pt\',\'#dd8452\')]\n    for ax,(label,val,delta,col) in zip(axes,kpis):\n        ax.set_facecolor(col); ax.axis(\'off\')\n        ax.text(0.5,0.65,val,ha=\'center\',fontsize=28,fontweight=\'bold\',\n                color=\'white\',transform=ax.transAxes)\n        ax.text(0.5,0.35,f\'{label}\n{delta}\',ha=\'center\',fontsize=11,\n                color=\'white\',transform=ax.transAxes)\n    fig.suptitle(\'Key Performance Indicators\',fontweight=\'bold\')\n    fig.tight_layout(); pdf.savefig(fig); plt.close()\n\n    # Page 3: trends\n    fig, ax = plt.subplots(figsize=(10,5))\n    months = np.arange(12)\n    for i,(name,col) in enumerate([(\'Revenue\',\'#4c72b0\'),(\'Costs\',\'tomato\'),(\'Margin\',\'seagreen\')]):\n        y = np.cumsum(np.random.randn(12)*0.5) + 5 + i*1.5\n        ax.plot(months, y, color=col, linewidth=2, label=name, marker=\'o\', markersize=4)\n    ax.set_title(\'12-Month Trend Analysis\'); ax.legend(); ax.grid(True, alpha=0.3)\n    fig.tight_layout(); pdf.savefig(fig); plt.close()\n\n    # Page 4: table\n    fig, ax = plt.subplots(figsize=(10,4))\n    ax.axis(\'off\')\n    cols = [\'Region\',\'Q1\',\'Q2\',\'Q3\',\'Q4\',\'Total\']\n    rows = [[\'North\',\'$1.2M\',\'$1.4M\',\'$1.3M\',\'$1.6M\',\'$5.5M\'],\n            [\'South\',\'$0.9M\',\'$1.0M\',\'$1.1M\',\'$1.3M\',\'$4.3M\'],\n            [\'East\',\'$0.7M\',\'$0.8M\',\'$0.9M\',\'$1.0M\',\'$3.4M\'],\n            [\'West\',\'$1.1M\',\'$1.2M\',\'$1.4M\',\'$1.5M\',\'$5.2M\']]\n    tbl = ax.table(cellText=rows, colLabels=cols, loc=\'center\', cellLoc=\'center\')\n    tbl.auto_set_font_size(False); tbl.set_fontsize(10); tbl.scale(1.2,1.8)\n    ax.set_title(\'Regional Revenue Summary\', fontweight=\'bold\', pad=20)\n    fig.tight_layout(); pdf.savefig(fig); plt.close()\n\nprint(\'Saved automated_report.pdf (4 pages)\')"
},
"practice": {
    "title": "Export Practice",
    "desc": "Create a figure with 3 subplots (line, bar, scatter). Save it as: (1) PNG at 72 DPI, (2) PNG at 300 DPI, (3) SVG vector. Then use PdfPages to save it as a 2-page PDF where page 1 is the 3-panel figure and page 2 is just the scatter zoomed in with a title overlay.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.backends.backend_pdf import PdfPages\n\nnp.random.seed(8)\nx = np.linspace(0, 10, 100)\nfig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13, 4))\nax1.plot(x, np.sin(x)); ax1.set_title(\'Line\')\nax2.bar(range(5), np.random.randint(1,10,5)); ax2.set_title(\'Bar\')\nax3.scatter(*np.random.randn(2,50), s=20, alpha=0.6); ax3.set_title(\'Scatter\')\nfig.tight_layout()\n\n# TODO: save PNG at 72 DPI\n# TODO: save PNG at 300 DPI\n# TODO: save SVG\n# TODO: save 2-page PDF with PdfPages\nplt.close()\nprint(\'Done\')"
}
},

{
"title": "32. Dashboard Composition",
"desc": "Compose production-quality dashboards by combining GridSpec layouts, dual axes, custom patches, annotation, and multi-figure export. Design for clarity, color accessibility, and print quality.",
"examples": [
        {"label": "KPI summary dashboard with mixed chart types", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec\nimport matplotlib.patches as mpatches\n\nnp.random.seed(42)\nfig = plt.figure(figsize=(14, 9), facecolor=\'#0f1117\')\ngs = GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.4)\n\ndef dark_ax(ax, title=\'\'):\n    ax.set_facecolor(\'#1c2128\')\n    for sp in ax.spines.values(): sp.set_color(\'#30363d\')\n    ax.tick_params(colors=\'#c9d1d9\', labelsize=8)\n    if title: ax.set_title(title, color=\'white\', fontsize=9, fontweight=\'bold\')\n    return ax\n\n# Top row: KPI boxes (4 mini panels)\nkpis = [(\'Revenue\', \'$2.4M\', \'+12%\', \'#4c72b0\'),\n        (\'DAU\',     \'84K\',   \'+8%\',  \'#55a868\'),\n        (\'Conv%\',   \'3.7%\',  \'+0.3\', \'#dd8452\'),\n        (\'NPS\',     \'72\',    \'+5\',   \'#c44e52\')]\nfor col, (label, val, delta, color) in enumerate(kpis):\n    ax = fig.add_subplot(gs[0, col])\n    ax.set_facecolor(color); ax.axis(\'off\')\n    ax.text(0.5, 0.6, val, ha=\'center\', va=\'center\', fontsize=18,\n            fontweight=\'bold\', color=\'white\', transform=ax.transAxes)\n    ax.text(0.5, 0.2, f\'{label}  {delta}\', ha=\'center\', fontsize=9,\n            color=\'white\', transform=ax.transAxes)\n\n# Mid-left: trend line (spans 2 cols)\nax_trend = dark_ax(fig.add_subplot(gs[1, :2]), \'Monthly Revenue Trend\')\nmonths = np.arange(12)\nrev = 1.5 + np.cumsum(np.random.randn(12)*0.08) + np.linspace(0,0.9,12)\nax_trend.plot(months, rev, color=\'#58a6ff\', linewidth=2)\nax_trend.fill_between(months, rev.min(), rev, alpha=0.15, color=\'#58a6ff\')\nax_trend.set_xticks(months)\nax_trend.set_xticklabels([\'J\',\'F\',\'M\',\'A\',\'M\',\'J\',\'J\',\'A\',\'S\',\'O\',\'N\',\'D\'],\n                          color=\'#8b949e\', fontsize=7)\n\n# Mid-right: bar chart (spans 2 cols)\nax_bar = dark_ax(fig.add_subplot(gs[1, 2:]), \'Revenue by Region\')\nregions = [\'North\',\'South\',\'East\',\'West\']\nvals = [2.4, 1.8, 1.3, 2.1]\ncolors_r = [\'#4c72b0\',\'#55a868\',\'#dd8452\',\'#c44e52\']\nax_bar.bar(regions, vals, color=colors_r, alpha=0.85, width=0.6)\nfor i, (r, v) in enumerate(zip(regions, vals)):\n    ax_bar.text(i, v+0.05, f\'${v}M\', ha=\'center\', fontsize=8, color=\'white\')\n\n# Bottom: scatter + right-side donut\nax_scatter = dark_ax(fig.add_subplot(gs[2, :3]), \'User Engagement\')\nn = 300\nsessions = np.random.lognormal(1, 0.5, n)\nrevenue_pts = sessions * np.random.uniform(5, 30, n)\nsc = ax_scatter.scatter(sessions, revenue_pts, c=np.log(sessions),\n                         cmap=\'plasma\', s=20, alpha=0.6)\nax_scatter.set_xlabel(\'Sessions\', color=\'#8b949e\', fontsize=8)\nax_scatter.set_ylabel(\'Revenue ($)\', color=\'#8b949e\', fontsize=8)\n\nax_pie = dark_ax(fig.add_subplot(gs[2, 3]), \'Traffic Mix\')\nwedges, _ = ax_pie.pie([35,30,20,15], colors=[\'#4c72b0\',\'#55a868\',\'#dd8452\',\'#8172b2\'],\n                        startangle=90, wedgeprops=dict(width=0.5))\nax_pie.legend(wedges, [\'Direct\',\'Organic\',\'Paid\',\'Ref\'], loc=\'lower center\',\n              fontsize=7, labelcolor=\'white\', facecolor=\'#1c2128\',\n              bbox_to_anchor=(0.5,-0.15), ncol=2)\nax_pie.axis(\'off\'); ax_pie.set_facecolor(\'#1c2128\')\n\nfig.suptitle(\'Business Intelligence Dashboard\', color=\'white\',\n             fontsize=15, fontweight=\'bold\', y=0.98)\nfig.savefig(\'bi_dashboard.png\', dpi=150, bbox_inches=\'tight\',\n            facecolor=fig.get_facecolor())\nplt.close()\nprint(\'Saved bi_dashboard.png\')"},
        {"label": "Scientific dashboard: experiment results", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec\nfrom scipy import stats\n\nnp.random.seed(7)\nfig = plt.figure(figsize=(13, 8))\ngs = GridSpec(2, 3, hspace=0.38, wspace=0.35)\n\n# Time series with confidence band\nax1 = fig.add_subplot(gs[0, :2])\nt = np.linspace(0, 20, 200)\nsignal = np.sin(t) * np.exp(-0.1*t)\nnoise = np.random.randn(200)*0.15\nmeasured = signal + noise\nupper = signal + 0.3; lower = signal - 0.3\nax1.fill_between(t, lower, upper, alpha=0.2, color=\'steelblue\', label=\'95% CI\')\nax1.plot(t, signal, \'steelblue\', linewidth=2, label=\'True\')\nax1.plot(t, measured, \'k.\', markersize=3, alpha=0.4, label=\'Measured\')\nax1.set_title(\'Damped Oscillation — Experiment A\'); ax1.legend(fontsize=8)\nax1.set_xlabel(\'Time (s)\'); ax1.grid(True, alpha=0.3)\n\n# Q-Q\nax2 = fig.add_subplot(gs[0, 2])\nqq = stats.probplot(measured - signal)\nax2.scatter(qq[0][0], qq[0][1], s=10, alpha=0.6, color=\'steelblue\')\nax2.plot(qq[0][0], qq[0][0]*qq[1][0]+qq[1][1], \'r-\')\nax2.set_title(\'Residual Q-Q\'); ax2.grid(True, alpha=0.3)\n\n# Frequency spectrum\nax3 = fig.add_subplot(gs[1, :2])\nfft = np.abs(np.fft.rfft(measured))\nfreq = np.fft.rfftfreq(len(measured), d=t[1]-t[0])\nax3.semilogy(freq[1:], fft[1:], color=\'tomato\', linewidth=1.5)\nax3.axvline(1/(2*np.pi), color=\'navy\', linestyle=\'--\', linewidth=1.5,\n            label=f\'Fundamental {1/(2*np.pi):.3f} Hz\')\nax3.set_xlabel(\'Frequency (Hz)\'); ax3.set_ylabel(\'Amplitude\')\nax3.set_title(\'FFT Spectrum\'); ax3.legend(fontsize=8); ax3.grid(True, which=\'both\', alpha=0.3)\n\n# Phase portrait\nax4 = fig.add_subplot(gs[1, 2])\nvel = np.gradient(measured, t)\nax4.plot(measured, vel, \'purple\', alpha=0.6, linewidth=0.8)\nax4.set_xlabel(\'Displacement\'); ax4.set_ylabel(\'Velocity\')\nax4.set_title(\'Phase Portrait\'); ax4.grid(True, alpha=0.3)\n\nfig.suptitle(\'Experiment Dashboard — Damped Oscillator\', fontweight=\'bold\', fontsize=13)\nfig.savefig(\'science_dashboard.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved science_dashboard.png\')"},
        {"label": "Financial OHLC chart with indicators", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(21)\nn = 60\ndates = np.arange(n)\nclose = 100 + np.cumsum(np.random.randn(n)*1.2)\nhigh  = close + np.abs(np.random.randn(n))*1.5\nlow   = close - np.abs(np.random.randn(n))*1.5\nopens = close + np.random.randn(n)*0.5\nvolume = np.random.randint(500, 2000, n).astype(float)\n\nsma20 = np.convolve(close, np.ones(20)/20, mode=\'valid\')\nsma_x = dates[19:]\nbb_mid = sma20\nbb_std = np.array([close[i-20:i].std() for i in range(20, n)])\nbb_up = bb_mid + 2*bb_std; bb_lo = bb_mid - 2*bb_std\n\nfrom matplotlib.gridspec import GridSpec\nfig = plt.figure(figsize=(12, 8))\ngs = GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=0.12)\nax_price = fig.add_subplot(gs[0]); ax_vol = fig.add_subplot(gs[1], sharex=ax_price)\nax_rsi = fig.add_subplot(gs[2], sharex=ax_price)\n\nfor d in dates:\n    color = \'seagreen\' if close[d] >= opens[d] else \'tomato\'\n    ax_price.plot([d,d],[low[d],high[d]], color=\'gray\', linewidth=0.8)\n    ax_price.bar(d, abs(close[d]-opens[d]), bottom=min(close[d],opens[d]),\n                 color=color, width=0.6)\nax_price.plot(sma_x, sma20, \'navy\', linewidth=1.5, label=\'SMA20\')\nax_price.fill_between(sma_x, bb_lo, bb_up, alpha=0.1, color=\'blue\', label=\'BB±2σ\')\nax_price.set_ylabel(\'Price\'); ax_price.legend(fontsize=8)\nax_price.set_title(\'OHLC with Bollinger Bands\', fontweight=\'bold\')\n\nax_vol.bar(dates, volume, color=\'steelblue\', alpha=0.6)\nax_vol.set_ylabel(\'Volume\')\n\ndelta = np.diff(close); up = np.where(delta>0,delta,0); down = np.where(delta<0,-delta,0)\nrs = np.convolve(up,np.ones(14)/14,\'valid\') / (np.convolve(down,np.ones(14)/14,\'valid\')+1e-9)\nrsi = 100 - 100/(1+rs)\nax_rsi.plot(dates[14:], rsi, color=\'purple\', linewidth=1.5)\nax_rsi.axhline(70, color=\'red\', linestyle=\'--\', linewidth=1)\nax_rsi.axhline(30, color=\'green\', linestyle=\'--\', linewidth=1)\nax_rsi.fill_between(dates[14:], 30, 70, alpha=0.05, color=\'gray\')\nax_rsi.set_ylabel(\'RSI\'); ax_rsi.set_ylim(0,100)\nax_rsi.set_xlabel(\'Day\')\n\nplt.setp(ax_price.get_xticklabels(), visible=False)\nplt.setp(ax_vol.get_xticklabels(), visible=False)\nfig.savefig(\'financial_chart.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved financial_chart.png\')"},
        {"label": "Accessible dashboard: colorblind-safe palette", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\n# Colorblind-safe palette (Wong 2011)\nCB_COLORS = [\'#000000\',\'#E69F00\',\'#56B4E9\',\'#009E73\',\n             \'#F0E442\',\'#0072B2\',\'#D55E00\',\'#CC79A7\']\n\nnp.random.seed(99)\nfig, axes = plt.subplots(2, 2, figsize=(11, 8))\naxes = axes.flat\n\n# 1. Line plot\nax = axes[0]\nx = np.linspace(0, 10, 100)\nfor i, col in enumerate(CB_COLORS[:4]):\n    ax.plot(x, np.sin(x + i*np.pi/4), color=col, linewidth=2,\n            label=f\'Series {i+1}\', linestyle=[\'-\',\'--\',\'-.\',\':\'][i])\nax.set_title(\'Line Plot — CB Safe\'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)\n\n# 2. Bar chart\nax = axes[1]\nvals = np.random.uniform(2, 9, 5)\nax.bar(range(5), vals, color=CB_COLORS[:5], alpha=0.9, width=0.6,\n       hatch=[\'\', \'//\', \'xx\', \'..\', \'\\\\\'])  # hatch for print accessibility\nax.set_title(\'Bar with Hatch Patterns\'); ax.grid(True, axis=\'y\', alpha=0.3)\n\n# 3. Scatter\nax = axes[2]\nfor i in range(4):\n    pts = np.random.randn(30, 2)\n    ax.scatter(pts[:,0], pts[:,1], color=CB_COLORS[i+1], s=40, alpha=0.8,\n               marker=[\'o\',\'s\',\'^\',\'D\'][i], label=f\'Class {i+1}\')\nax.set_title(\'Scatter — Multiple Markers\'); ax.legend(fontsize=8)\n\n# 4. Filled area\nax = axes[3]\nx_a = np.linspace(0, 8, 80)\nfor i, col in enumerate(CB_COLORS[1:5]):\n    y = np.sin(x_a + i) + i*0.8\n    ax.plot(x_a, y, color=col, linewidth=2)\n    ax.fill_between(x_a, 0, y, color=col, alpha=0.15)\nax.set_title(\'Area Chart — CB Safe\'); ax.grid(True, alpha=0.3)\n\nfig.suptitle(\'Colorblind-Safe Dashboard (Wong Palette)\', fontweight=\'bold\', fontsize=13)\nfig.tight_layout()\nfig.savefig(\'accessible_dashboard.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved accessible_dashboard.png\')"}
    ],
"rw": {
    "title": "Executive Analytics Deck",
    "scenario": "Build a 5-panel executive dashboard: title banner, revenue trend with target line, geographic bar chart, user funnel (horizontal bars decreasing), and a summary table. Export at 200 DPI.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec\nimport matplotlib.patches as mpatches\n\nnp.random.seed(88)\nfig = plt.figure(figsize=(14, 10), facecolor=\'white\')\ngs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)\n\n# Banner\nax_banner = fig.add_subplot(gs[0, :])\nax_banner.set_facecolor(\'#1c2128\'); ax_banner.axis(\'off\')\nax_banner.text(0.5, 0.6, \'Executive Dashboard — Q4 2024\',\n               ha=\'center\', fontsize=18, fontweight=\'bold\', color=\'white\',\n               transform=ax_banner.transAxes)\nax_banner.text(0.5, 0.2, \'Prepared by Analytics Team | Confidential\',\n               ha=\'center\', fontsize=11, color=\'#8b949e\',\n               transform=ax_banner.transAxes)\n\n# Revenue trend\nax_rev = fig.add_subplot(gs[1, :2])\nmonths = np.arange(12)\nrev = 1.0 + np.cumsum(np.random.randn(12)*0.05) + np.linspace(0,0.8,12)\ntarget = np.linspace(1.0, 2.0, 12)\nax_rev.plot(months, rev, \'steelblue\', linewidth=2.5, marker=\'o\', markersize=5, label=\'Actual\')\nax_rev.plot(months, target, \'r--\', linewidth=1.5, label=\'Target\')\nax_rev.fill_between(months, rev, target, where=(rev>=target),\n                    alpha=0.15, color=\'green\', label=\'Ahead\')\nax_rev.fill_between(months, rev, target, where=(rev<target),\n                    alpha=0.15, color=\'red\', label=\'Behind\')\nax_rev.set_title(\'Monthly Revenue vs Target\', fontweight=\'bold\')\nax_rev.legend(fontsize=8); ax_rev.grid(True, alpha=0.3)\n\n# Regional bar\nax_geo = fig.add_subplot(gs[1, 2])\nregions = [\'APAC\',\'EMEA\',\'AMER\',\'LATAM\']\nrev_r = [4.2, 3.1, 5.8, 1.9]\nax_geo.barh(regions, rev_r, color=[\'#4c72b0\',\'#dd8452\',\'#55a868\',\'#c44e52\'], alpha=0.85)\nfor i,(r,v) in enumerate(zip(regions,rev_r)):\n    ax_geo.text(v+0.05, i, f\'${v}M\', va=\'center\', fontsize=9)\nax_geo.set_title(\'Revenue by Region\', fontweight=\'bold\')\nax_geo.grid(True, axis=\'x\', alpha=0.3)\n\n# Funnel\nax_funnel = fig.add_subplot(gs[2, :2])\nstages = [\'Visitors\',\'Signups\',\'Activated\',\'Paid\',\'Retained\']\ncounts = [100000, 18000, 9000, 2800, 1900]\ncolors_f = [\'#4c72b0\',\'#5e82c0\',\'#7498d0\',\'#8aaee0\',\'#a0c4f0\']\nax_funnel.barh(stages[::-1], counts[::-1], color=colors_f, alpha=0.85)\nfor i,(s,c) in enumerate(zip(stages[::-1],counts[::-1])):\n    ax_funnel.text(c+500, i, f\'{c:,}\', va=\'center\', fontsize=9)\nax_funnel.set_title(\'User Acquisition Funnel\', fontweight=\'bold\')\nax_funnel.grid(True, axis=\'x\', alpha=0.3)\n\n# Table\nax_tbl = fig.add_subplot(gs[2, 2])\nax_tbl.axis(\'off\')\ncols = [\'Metric\',\'Q3\',\'Q4\']\nrows = [[\'Revenue\',\'$18.2M\',\'$22.1M\'],\n        [\'Users\',\'76K\',\'84K\'],\n        [\'NPS\',\'67\',\'72\']]\ntbl = ax_tbl.table(cellText=rows, colLabels=cols, loc=\'center\', cellLoc=\'center\')\ntbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1.1,1.5)\nax_tbl.set_title(\'Summary\', fontweight=\'bold\', pad=15)\n\nfig.savefig(\'executive_deck.png\', dpi=200, bbox_inches=\'tight\',\n            facecolor=fig.get_facecolor())\nplt.close()\nprint(\'Saved executive_deck.png\')"
},
"practice": {
    "title": "Dashboard Practice",
    "desc": "Build your own 3-panel dashboard on a topic of your choice (e.g., fitness tracking, stock portfolio, weather). Requirements: (1) use GridSpec with at least one spanning panel, (2) include a dual-axis twinx or broken axis, (3) use at least 3 different chart types, (4) add a title banner, (5) save at 150 DPI.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom matplotlib.gridspec import GridSpec\n\nnp.random.seed(42)\nfig = plt.figure(figsize=(13, 9))\ngs = GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.35)\n\n# TODO: Banner row (gs[0, :])\n# TODO: Main chart spanning 2 cols (gs[1, :2])\n# TODO: Side chart (gs[1, 2])\n# TODO: Bottom-left chart (gs[2, :2])\n# TODO: Bottom-right chart or table (gs[2, 2])\n# TODO: At least one twinx or broken axis\n# TODO: Title and tight_layout\n# TODO: save \'my_dashboard.png\' at 150 DPI\nplt.close()\nprint(\'Dashboard saved!\')"
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
