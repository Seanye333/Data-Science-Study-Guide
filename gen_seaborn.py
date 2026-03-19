#!/usr/bin/env python3
"""Generate Seaborn study guide — notebook + HTML."""

import matplotlib
matplotlib.use('Agg')

import json, pathlib
from html import escape as esc

BASE   = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\04_seaborn")
BASE.mkdir(parents=True, exist_ok=True)
ACCENT = "#c084fc"
EMOJI  = "🎨"
TITLE  = "Seaborn"

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
    cells.append(md(f"# {TITLE} Study Guide\n\nStatistical visualization built on Matplotlib. Run cells in Jupyter to see plots."))
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
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.11.0"}},"nbformat":4,"nbformat_minor":5}


SECTIONS = [

{
"title": "1. Setup & Themes",
"desc": "Seaborn works with pandas DataFrames. Set a theme once at the top of your notebook and all plots inherit consistent styling.",
"examples": [
{"label": "sns.set_theme and built-in datasets", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

# Set global theme — do this once at the top
sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)

# Seaborn ships with practice datasets
tips  = sns.load_dataset('tips')
iris  = sns.load_dataset('iris')
titanic = sns.load_dataset('titanic')

print(tips.head())
print(f"\\ntips shape: {tips.shape}")
print(tips.dtypes)"""},
{"label": "Available styles and palettes", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

styles   = ['darkgrid','whitegrid','dark','white','ticks']
palettes = ['deep','muted','pastel','bright','dark','colorblind']

fig, axes = plt.subplots(2, 3, figsize=(12, 6))
for ax, style in zip(axes[0], styles[:3]):
    sns.barplot(x=['A','B','C'], y=[3,5,4], ax=ax, palette='deep')
    ax.set_title(f'style={style}')

for ax, pal in zip(axes[1], palettes[:3]):
    sns.barplot(x=['A','B','C'], y=[3,5,4], ax=ax, palette=pal)
    ax.set_title(f'palette={pal}')

plt.tight_layout()
plt.savefig('styles_palettes.png', dpi=80)
plt.close()"""},
{"label": "Custom color palettes and sns.color_palette", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Create and inspect custom palettes
blues   = sns.color_palette("Blues", 6)
custom  = sns.color_palette(["#e74c3c","#3498db","#2ecc71","#f39c12"])
husl    = sns.color_palette("husl", 8)

fig, axes = plt.subplots(1, 3, figsize=(12, 2))
sns.palplot(blues,  ax=axes[0] if hasattr(sns,'palplot') else None)
for ax, (pal, name) in zip(axes, [(blues,'Blues-6'),(custom,'Custom-4'),(husl,'HUSL-8')]):
    for j, c in enumerate(pal):
        ax.add_patch(plt.Rectangle((j, 0), 1, 1, color=c))
    ax.set_xlim(0, len(pal)); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(name)

plt.suptitle('Color Palette Examples', y=1.05)
plt.tight_layout()
plt.savefig('palettes_custom.png', dpi=80)
plt.close()
print("Blues palette (RGB):", [tuple(round(v,2) for v in c) for c in blues])"""},
{"label": "sns.despine and figure-level vs axes-level functions", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

# --- axes-level function: returns an Axes, fits into any subplot grid ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.boxplot(data=tips, x='day', y='total_bill', palette='pastel', ax=axes[0])
axes[0].set_title('Axes-level: sns.boxplot (axes[0])')
# sns.despine removes top/right spines for a cleaner look
sns.despine(ax=axes[0], offset=8, trim=True)

# A second axes-level call on the other subplot
sns.stripplot(data=tips, x='day', y='total_bill',
              color='steelblue', alpha=0.4, jitter=True, ax=axes[1])
axes[1].set_title('Axes-level: sns.stripplot (axes[1])')
sns.despine(ax=axes[1])

plt.suptitle('Axes-level functions — full subplot control', fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig('setup_despine_axes_level.png', dpi=80)
plt.close()

# --- figure-level function: creates its OWN figure / FacetGrid ---
# You cannot pass ax= to figure-level functions (displot, catplot, relplot, etc.)
g = sns.displot(data=tips, x='total_bill', col='time',
                kind='hist', kde=True, bins=20,
                height=3.5, aspect=1.1, palette='Set2')
g.set_titles('{col_name}')
g.figure.suptitle('Figure-level: sns.displot (owns its own Figure)', y=1.04)
plt.tight_layout()
plt.savefig('setup_despine_figure_level.png', dpi=80)
plt.close()
print("despine + figure-level vs axes-level demo saved.")"""}
],
"rw": {
"title": "Setting Up a Project-Wide Visual Style",
"scenario": "A data team standardizes all report charts with a single style config at the top of every notebook.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Team-wide style configuration
sns.set_theme(
    style='whitegrid',
    palette='colorblind',   # accessible to color-blind viewers
    font_scale=1.0,
    rc={
        'figure.figsize':    (9, 4),
        'axes.spines.top':   False,
        'axes.spines.right': False,
        'grid.linewidth':    0.5,
    }
)

# Quick sanity-check plot
np.random.seed(42)
df = pd.DataFrame({
    'quarter': ['Q1','Q2','Q3','Q4'] * 3,
    'region':  ['North']*4 + ['South']*4 + ['East']*4,
    'revenue': np.random.uniform(100, 500, 12).round(1),
})

sns.barplot(data=df, x='quarter', y='revenue', hue='region')
plt.title('Revenue by Quarter & Region')
plt.ylabel('Revenue ($K)')
plt.tight_layout()
plt.savefig('rw_setup_themes.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Switch Themes and Build a Custom Palette",
"desc": "1) Apply three different Seaborn styles ('darkgrid', 'white', 'ticks') to the same bar chart of [3,7,5,9,4] and save each. 2) Create a custom 5-color palette using hex codes of your choice and pass it to a barplot. 3) Use sns.set_theme with rc overrides to remove top/right spines and set figure size to (8, 3).",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

values = [3, 7, 5, 9, 4]
labels = ['A', 'B', 'C', 'D', 'E']

# 1. Apply three styles and save each
for style in ['darkgrid', 'white', 'ticks']:
    with sns.axes_style(style):
        fig, ax = plt.subplots(figsize=(6, 3))
        # TODO: sns.barplot(x=labels, y=values, ax=ax, palette='muted')
        # ax.set_title(f'Style: {style}')
        # plt.tight_layout()
        # plt.savefig(f'style_{style}.png', dpi=80)
        # plt.close()
        pass

# 2. Custom 5-color palette
my_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
# TODO: fig, ax = plt.subplots(figsize=(6, 3))
# TODO: sns.barplot(x=labels, y=values, palette=my_colors, ax=ax)
# TODO: ax.set_title('Custom Palette')
# TODO: plt.tight_layout(); plt.savefig('custom_palette.png', dpi=80); plt.close()

# 3. sns.set_theme with rc overrides
# TODO: sns.set_theme(style='whitegrid', rc={
# TODO:     'figure.figsize': (8, 3),
# TODO:     'axes.spines.top': False,
# TODO:     'axes.spines.right': False,
# TODO: })
# TODO: fig, ax = plt.subplots()
# TODO: sns.barplot(x=labels, y=values, palette='deep', ax=ax)
# TODO: plt.tight_layout(); plt.savefig('rc_override.png', dpi=80); plt.close()"""
},

},

{
"title": "2. Distribution Plots",
"desc": "histplot and kdeplot show how data is distributed. displot combines both into a faceted figure-level function.",
"examples": [
{"label": "histplot and kdeplot", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# Histogram with KDE overlay
sns.histplot(data=tips, x='total_bill', bins=25,
             kde=True, ax=axes[0], color='steelblue')
axes[0].set_title('Total Bill Distribution')

# KDE only — compare two groups
sns.kdeplot(data=tips, x='tip', hue='sex',
            fill=True, alpha=0.4, ax=axes[1])
axes[1].set_title('Tip Distribution by Gender')

plt.tight_layout()
plt.savefig('dist_hist_kde.png', dpi=80)
plt.close()"""},
{"label": "displot — faceted distributions", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

# Separate histogram per day, colored by sex
g = sns.displot(
    data=tips, x='total_bill', hue='sex',
    col='day', kind='hist', kde=True,
    bins=15, height=3.5, aspect=0.9,
    palette='Set2'
)
g.set_titles('{col_name}')
g.set_xlabels('Total Bill ($)')
plt.tight_layout()
plt.savefig('dist_displot.png', dpi=80)
plt.close()"""},
{"label": "ECDF and rug plot", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# ECDF — empirical cumulative distribution
sns.ecdfplot(data=tips, x='total_bill', hue='time',
             palette='Set1', linewidth=2, ax=axes[0])
axes[0].set_title('ECDF of Total Bill by Meal Time')
axes[0].set_xlabel('Total Bill ($)')

# Rug plot layered under KDE
sns.kdeplot(data=tips, x='total_bill', hue='smoker',
            fill=True, alpha=0.3, ax=axes[1])
sns.rugplot(data=tips, x='total_bill', hue='smoker',
            height=0.06, ax=axes[1])
axes[1].set_title('KDE + Rug: Total Bill by Smoker')

plt.tight_layout()
plt.savefig('dist_ecdf_rug.png', dpi=80)
plt.close()"""},
{"label": "Overlaid histograms with stat='density' and displot kind='ecdf'", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
sns.set_theme(style='whitegrid')

# Synthetic spend data for three customer tiers
tiers = {'Bronze': np.random.normal(30, 10, 300),
         'Silver': np.random.normal(70, 15, 200),
         'Gold':   np.random.normal(130, 25, 100)}
rows = []
for tier, vals in tiers.items():
    for v in vals.clip(0):
        rows.append({'tier': tier, 'spend': round(v, 2)})
df = pd.DataFrame(rows)

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# Left: overlaid histograms normalised to density so groups are comparable
for tier, color in [('Bronze','#cd7f32'),('Silver','#aaa9ad'),('Gold','#ffd700')]:
    subset = df[df['tier'] == tier]
    sns.histplot(data=subset, x='spend', stat='density',
                 bins=25, alpha=0.45, color=color, label=tier,
                 kde=True, ax=axes[0])
axes[0].set_title('Spend Distribution by Tier (stat=density)')
axes[0].set_xlabel('Monthly Spend ($)')
axes[0].legend(title='Tier')

# Right: displot with kind='ecdf' — figure-level, drawn into a fresh figure
plt.tight_layout()
plt.savefig('dist_density_overlay.png', dpi=80)
plt.close()

g = sns.displot(data=df, x='spend', hue='tier',
                kind='ecdf', linewidth=2.5,
                palette={'Bronze':'#cd7f32','Silver':'#aaa9ad','Gold':'#ffd700'},
                height=4, aspect=1.6)
g.set_axis_labels('Monthly Spend ($)', 'Proportion')
g.figure.suptitle('ECDF of Spend by Customer Tier (displot kind=ecdf)', y=1.03)
plt.tight_layout()
plt.savefig('dist_ecdf_displot.png', dpi=80)
plt.close()
print("Density overlay and ECDF displot saved.")"""}
],
"rw": {
"title": "Customer Spend Distribution by Segment",
"scenario": "A marketing analyst compares spend distributions across customer segments to set targeted promotional thresholds.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(42)
segments = {
    'VIP':       np.random.normal(350, 80,  200),
    'Regular':   np.random.normal(150, 50,  500),
    'Occasional':np.random.normal(60,  30,  300),
}

rows = []
for seg, vals in segments.items():
    for v in vals.clip(0):
        rows.append({'segment': seg, 'spend': round(v, 2)})
df = pd.DataFrame(rows)

sns.set_theme(style='whitegrid')
fig, ax = plt.subplots(figsize=(10, 4))
sns.kdeplot(data=df, x='spend', hue='segment',
            fill=True, alpha=0.3, linewidth=2,
            palette={'VIP':'#e74c3c','Regular':'#3498db','Occasional':'#2ecc71'})

# Threshold lines
for thresh, label in [(100,'Entry'), (250,'Mid'), (400,'Premium')]:
    ax.axvline(thresh, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    ax.text(thresh+3, ax.get_ylim()[1]*0.9, label, fontsize=8, color='gray')

ax.set_xlabel('Monthly Spend ($)')
ax.set_title('Customer Spend Distribution by Segment')
plt.tight_layout()
plt.savefig('rw_dist_spend.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Overlaid KDE for Two Groups",
"desc": "Load the 'tips' dataset. 1) Plot overlaid KDE curves for 'total_bill' split by 'smoker' (fill=True, alpha=0.35). 2) Add vertical lines at each group's median. 3) In a second axes, plot an ECDF of 'tip' split by 'day'. Save both as a single figure.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 1. Overlaid KDE for total_bill by smoker
# TODO: sns.kdeplot(data=tips, x='total_bill', hue='smoker',
# TODO:             fill=True, alpha=0.35, ax=axes[0])

# 2. Add vertical lines at each group's median
for smoker_val, color in [('Yes', '#e74c3c'), ('No', '#3498db')]:
    grp = tips[tips['smoker'] == smoker_val]['total_bill']
    # TODO: axes[0].axvline(grp.median(), color=color, linestyle='--', linewidth=1.5,
    # TODO:                 label=f'Median ({smoker_val}): ${grp.median():.1f}')
    pass
# TODO: axes[0].legend(); axes[0].set_title('Total Bill KDE by Smoker')

# 3. ECDF of tip by day
# TODO: sns.ecdfplot(data=tips, x='tip', hue='day', palette='tab10', ax=axes[1])
# TODO: axes[1].set_title('Tip ECDF by Day')

plt.tight_layout()
plt.savefig('practice_dist.png', dpi=80)
plt.close()
print("Saved practice_dist.png")"""
},

},

{
"title": "3. Categorical Plots — Bar & Count",
"desc": "barplot shows mean ± CI of a numeric variable by category. countplot shows frequency. Both accept hue for a third dimension.",
"examples": [
{"label": "barplot and countplot", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# Mean tip by day + confidence interval
sns.barplot(data=tips, x='day', y='tip',
            hue='sex', palette='Set2', ax=axes[0])
axes[0].set_title('Avg Tip by Day & Gender')
axes[0].set_ylabel('Mean Tip ($)')

# Count of meals per day
sns.countplot(data=tips, x='day', hue='time',
              palette='pastel', ax=axes[1])
axes[1].set_title('Meal Count by Day & Time')

plt.tight_layout()
plt.savefig('cat_bar_count.png', dpi=80)
plt.close()"""},
{"label": "Horizontal bar with order", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

# Compute mean tip per day — sort for readability
order = tips.groupby('day')['tip'].mean().sort_values(ascending=False).index

fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(data=tips, y='day', x='tip',
            order=order, palette='Blues_d', orient='h', ax=ax)
ax.set_xlabel('Average Tip ($)')
ax.set_title('Average Tip by Day of Week (sorted)')
plt.tight_layout()
plt.savefig('cat_hbar.png', dpi=80)
plt.close()"""},
{"label": "Grouped bar with error bars and value labels", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(7)
sns.set_theme(style='whitegrid')

# Simulated quarterly sales by product
products = ['Alpha', 'Beta', 'Gamma']
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
rows = []
for q in quarters:
    for p in products:
        base = {'Alpha': 120, 'Beta': 85, 'Gamma': 160}[p]
        rows.append({'quarter': q, 'product': p,
                     'sales': np.random.normal(base, 15)})
df = pd.DataFrame(rows)

fig, ax = plt.subplots(figsize=(9, 4))
sns.barplot(data=df, x='quarter', y='sales', hue='product',
            palette='Set2', capsize=0.08, ax=ax)

# Value labels on bars
for bar in ax.patches:
    if bar.get_height() > 0:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 1,
                f'{bar.get_height():.0f}',
                ha='center', va='bottom', fontsize=7)

ax.set_title('Quarterly Sales by Product (mean ± 95% CI)')
ax.set_ylabel('Sales ($K)')
plt.tight_layout()
plt.savefig('cat_grouped_bar.png', dpi=80)
plt.close()"""},
{"label": "sns.catplot, dodge=True grouped bars, estimator=median", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(21)
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

# --- catplot: figure-level wrapper for all categorical plot kinds ---
# kind='bar' with estimator=median and dodge=True (default) for grouped bars
g = sns.catplot(
    data=tips, x='day', y='total_bill', hue='time',
    kind='bar',
    estimator=np.median,       # use median instead of default mean
    errorbar=('ci', 95),       # 95 % bootstrap CI
    dodge=True,                # bars side-by-side (not stacked)
    palette='Set1',
    capsize=0.10,
    height=4, aspect=1.4,
    order=['Thur', 'Fri', 'Sat', 'Sun']
)
g.set_axis_labels('Day', 'Median Total Bill ($)')
g.set_titles('Tip vs Bill — median estimator')
g.figure.suptitle('catplot: Median Total Bill by Day & Meal Time (dodge=True)', y=1.03)
plt.tight_layout()
plt.savefig('cat_catplot_median_dodge.png', dpi=80)
plt.close()

# --- second figure: countplot with dodge to compare two binary variables ---
fig, ax = plt.subplots(figsize=(8, 4))
sns.countplot(data=tips, x='day', hue='smoker',
              dodge=True, palette='Dark2',
              order=['Thur', 'Fri', 'Sat', 'Sun'], ax=ax)
ax.set_title('Diner Count by Day & Smoker Status (dodge=True)')
ax.set_ylabel('Count')
plt.tight_layout()
plt.savefig('cat_count_dodge.png', dpi=80)
plt.close()
print("catplot (median, dodge) and countplot saved.")"""}
],
"rw": {
"title": "Product Return Rate by Category",
"scenario": "An operations analyst visualizes return rates across product categories to prioritize quality improvements.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(7)
categories = ['Electronics','Clothing','Books','Toys','Sports','Home','Beauty']
data = []
for cat in categories:
    base_rate = np.random.uniform(0.03, 0.18)
    for _ in range(200):
        data.append({
            'category': cat,
            'returned': int(np.random.random() < base_rate),
            'channel':  np.random.choice(['Online','In-store'], p=[0.7, 0.3]),
        })
df = pd.DataFrame(data)

order = (df.groupby('category')['returned']
           .mean()
           .sort_values(ascending=False)
           .index.tolist())

sns.set_theme(style='whitegrid')
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=df, x='category', y='returned',
            hue='channel', order=order,
            palette={'Online':'#3498db','In-store':'#e67e22'},
            capsize=0.08, ax=ax)

ax.axhline(df['returned'].mean(), color='red', linestyle='--',
           linewidth=1.5, label=f"Overall avg: {df['returned'].mean():.1%}")
ax.set_ylabel('Return Rate'); ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
ax.set_xlabel(''); ax.set_title('Product Return Rate by Category & Channel')
ax.legend(); plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('rw_cat_returns.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Grouped Bar with Error Bars",
"desc": "Using the 'tips' dataset: 1) Create a grouped barplot of mean 'total_bill' by 'day' with 'time' as hue (Lunch vs Dinner), using capsize=0.1 to show confidence intervals. 2) Sort the x-axis days in calendar order (Thur, Fri, Sat, Sun). 3) Add a horizontal dashed line at the overall mean. Save the figure.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, ax = plt.subplots(figsize=(8, 4))

day_order = ['Thur', 'Fri', 'Sat', 'Sun']

# 1 & 2. Grouped barplot sorted by calendar order
# TODO: sns.barplot(data=tips, x='day', y='total_bill', hue='time',
# TODO:             order=day_order, capsize=0.1, palette='Set2', ax=ax)

# 3. Overall mean reference line
overall_mean = tips['total_bill'].mean()
# TODO: ax.axhline(overall_mean, color='red', linestyle='--', linewidth=1.5,
# TODO:            label=f'Overall mean: ${overall_mean:.2f}')

# TODO: ax.set_title('Total Bill by Day and Meal Time')
# TODO: ax.set_ylabel('Mean Total Bill ($)')
# TODO: ax.legend()

plt.tight_layout()
plt.savefig('practice_bar.png', dpi=80)
plt.close()
print("Saved practice_bar.png")"""
},

},

{
"title": "4. Box Plot & Violin Plot",
"desc": "Box plots show the 5-number summary (min, Q1, median, Q3, max). Violin plots also show the distribution shape via KDE.",
"examples": [
{"label": "boxplot and violinplot", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.boxplot(data=tips, x='day', y='total_bill',
            hue='time', palette='Set3', ax=axes[0])
axes[0].set_title('Total Bill — Box Plot')

sns.violinplot(data=tips, x='day', y='total_bill',
               hue='time', split=True,
               palette='Set2', inner='quartile', ax=axes[1])
axes[1].set_title('Total Bill — Violin Plot')

plt.tight_layout()
plt.savefig('cat_box_violin.png', dpi=80)
plt.close()"""},
{"label": "boxenplot and stripplot overlay", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, ax = plt.subplots(figsize=(8, 5))

# Letter-value plot (boxenplot) for larger datasets
sns.boxenplot(data=tips, x='day', y='total_bill',
              palette='muted', ax=ax)

# Overlay raw points
sns.stripplot(data=tips, x='day', y='total_bill',
              color='black', size=3, alpha=0.3, ax=ax, jitter=True)

ax.set_title('Total Bill Distribution per Day (boxen + strip)')
ax.set_ylabel('Total Bill ($)')
plt.tight_layout()
plt.savefig('cat_boxen_strip.png', dpi=80)
plt.close()"""},
{"label": "Side-by-side violin plots with inner box", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(42)
sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: violin per species for petal_length
sns.violinplot(data=iris, x='species', y='petal_length',
               palette='Set2', inner='box', ax=axes[0])
axes[0].set_title('Petal Length by Species (inner=box)')
axes[0].set_ylabel('Petal Length (cm)')

# Right: layered — violin + box + strip
sns.violinplot(data=iris, x='species', y='sepal_width',
               palette='pastel', inner=None, ax=axes[1])
sns.boxplot(data=iris, x='species', y='sepal_width',
            width=0.12, fliersize=0,
            boxprops=dict(facecolor='white', zorder=2), ax=axes[1])
sns.stripplot(data=iris, x='species', y='sepal_width',
              color='black', size=2.5, alpha=0.4, jitter=True, ax=axes[1])
axes[1].set_title('Sepal Width: Violin + Box + Strip')
axes[1].set_ylabel('Sepal Width (cm)')

plt.tight_layout()
plt.savefig('cat_violin_layered.png', dpi=80)
plt.close()"""},
{"label": "swarmplot and pointplot", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(7)
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: swarmplot — all points plotted without overlap (small datasets)
sns.swarmplot(data=tips, x='day', y='total_bill',
              hue='sex', dodge=True,
              palette='Set2', size=4, ax=axes[0])
axes[0].set_title('swarmplot: Total Bill by Day & Sex')
axes[0].set_ylabel('Total Bill ($)')
axes[0].legend(title='Sex', loc='upper left')

# Right: pointplot — shows mean + CI as a connected dot plot
#   great for showing trends across ordered categories
sns.pointplot(data=tips, x='day', y='tip', hue='sex',
              dodge=0.3, linestyles=['--', '-'],
              markers=['o', 's'], palette='Set1',
              capsize=0.12, errorbar=('ci', 95),
              order=['Thur', 'Fri', 'Sat', 'Sun'],
              ax=axes[1])
axes[1].set_title('pointplot: Mean Tip by Day & Sex (95% CI)')
axes[1].set_ylabel('Mean Tip ($)')
axes[1].legend(title='Sex')

plt.tight_layout()
plt.savefig('cat_swarm_point.png', dpi=80)
plt.close()
print("swarmplot and pointplot saved.")"""}
],
"rw": {
"title": "Employee Salary Distribution by Department",
"scenario": "An HR analyst compares salary spreads across departments to detect pay equity issues before a compensation review.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(42)
depts = {
    'Engineering':  (120000, 25000, 80),
    'Sales':        (85000,  20000, 60),
    'Marketing':    (90000,  18000, 40),
    'HR':           (70000,  12000, 30),
    'Data Science': (130000, 22000, 50),
    'Operations':   (75000,  15000, 55),
}

rows = []
for dept, (mean, std, n) in depts.items():
    salaries = np.random.normal(mean, std, n).clip(50000, 200000)
    for s in salaries:
        rows.append({'dept': dept, 'salary': round(s, -2),
                     'level': np.random.choice(['Junior','Mid','Senior'],
                                               p=[0.3,0.45,0.25])})
df = pd.DataFrame(rows)

order = df.groupby('dept')['salary'].median().sort_values(ascending=False).index

sns.set_theme(style='whitegrid')
fig, ax = plt.subplots(figsize=(11, 5))
sns.violinplot(data=df, x='dept', y='salary', order=order,
               palette='muted', inner='quartile', ax=ax)
sns.stripplot(data=df, x='dept', y='salary', order=order,
              hue='level', palette='dark:black', size=2.5,
              alpha=0.35, dodge=False, ax=ax, legend=False)

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'${x/1000:.0f}K'))
ax.set_xlabel(''); ax.set_ylabel('Annual Salary')
ax.set_title('Salary Distribution by Department')
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig('rw_cat_salary.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Side-by-Side Violin Plots",
"desc": "Using the 'tips' dataset: 1) Create side-by-side violin plots of 'total_bill' for each 'day', split by 'sex' (use split=True and hue='sex'). 2) Set inner='quartile' to show quartile lines inside the violins. 3) In a second subplot, overlay a boxplot (width=0.15) and stripplot on the violin. Save both.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# 1 & 2. Split violin by sex with quartile lines
# TODO: sns.violinplot(data=tips, x='day', y='total_bill',
# TODO:                hue='sex', split=True, inner='quartile',
# TODO:                palette='Set2', ax=axes[0])
# TODO: axes[0].set_title('Total Bill by Day & Sex (split violin)')

# 3. Violin + box + strip overlay on axes[1]
# TODO: sns.violinplot(data=tips, x='day', y='total_bill',
# TODO:                palette='pastel', inner=None, ax=axes[1])
# TODO: sns.boxplot(data=tips, x='day', y='total_bill',
# TODO:             width=0.15, fliersize=0,
# TODO:             boxprops=dict(facecolor='white', zorder=2), ax=axes[1])
# TODO: sns.stripplot(data=tips, x='day', y='total_bill',
# TODO:               color='black', size=2.5, alpha=0.35, jitter=True, ax=axes[1])
# TODO: axes[1].set_title('Total Bill: Violin + Box + Strip')

plt.tight_layout()
plt.savefig('practice_violin.png', dpi=80)
plt.close()
print("Saved practice_violin.png")"""
},

},

{
"title": "5. Scatter & Regression Plots",
"desc": "scatterplot visualizes two numeric variables. regplot / lmplot adds a regression line with confidence interval automatically.",
"examples": [
{"label": "scatterplot with hue and size", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=tips, x='total_bill', y='tip',
    hue='time', size='size',
    sizes=(40, 200), alpha=0.7,
    palette='Set1', ax=ax
)
ax.set_title('Tip vs Total Bill (size = party size)')
ax.set_xlabel('Total Bill ($)'); ax.set_ylabel('Tip ($)')
plt.tight_layout()
plt.savefig('scatter_hue_size.png', dpi=80)
plt.close()"""},
{"label": "regplot and lmplot", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, ax = plt.subplots(figsize=(7, 4))

# regplot — single regression line
sns.regplot(data=tips, x='total_bill', y='tip',
            scatter_kws=dict(alpha=0.4, s=30),
            line_kws=dict(color='red', linewidth=2), ax=ax)
ax.set_title('regplot: Tip vs Bill')
plt.tight_layout()
plt.savefig('scatter_regplot.png', dpi=80)
plt.close()

# lmplot — regression per group (returns FacetGrid)
g = sns.lmplot(data=tips, x='total_bill', y='tip',
               hue='smoker', palette='Set1',
               scatter_kws=dict(alpha=0.4, s=25),
               height=4, aspect=1.4)
g.set_axis_labels('Total Bill ($)', 'Tip ($)')
g.figure.suptitle('lmplot: Tip vs Bill by Smoker', y=1.02)
plt.tight_layout()
plt.savefig('scatter_lmplot.png', dpi=80)
plt.close()"""},
{"label": "Scatter with hue, size, and style encoding", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(10)
sns.set_theme(style='whitegrid')

# Synthetic dataset with 3 categorical dimensions
n = 120
df = pd.DataFrame({
    'spend':    np.random.uniform(10, 500, n),
    'revenue':  np.random.uniform(50, 2000, n),
    'channel':  np.random.choice(['Search', 'Social', 'Email'], n),
    'region':   np.random.choice(['North', 'South', 'East'], n),
    'budget':   np.random.uniform(5, 50, n),
})

fig, ax = plt.subplots(figsize=(9, 5))
sns.scatterplot(
    data=df, x='spend', y='revenue',
    hue='channel',    # color
    size='budget',    # marker area
    style='region',   # marker shape
    sizes=(30, 250),
    alpha=0.75,
    palette='tab10',
    ax=ax
)
ax.set_title('Revenue vs Spend — hue=channel, size=budget, style=region')
ax.set_xlabel('Ad Spend ($)')
ax.set_ylabel('Revenue ($)')
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig('scatter_hue_size_style.png', dpi=80)
plt.close()"""},
{"label": "sns.relplot with col_wrap and per-hue marker styles", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(33)
sns.set_theme(style='whitegrid', font_scale=0.9)

# Synthetic multi-channel, multi-region dataset
channels = ['Search', 'Social', 'Email', 'Display', 'Affiliate']
regions  = ['North', 'South', 'East']
rows = []
for ch in channels:
    slope = {'Search': 4.0, 'Social': 2.5, 'Email': 5.5,
             'Display': 1.5, 'Affiliate': 3.2}[ch]
    for region in regions:
        n = 30
        spend = np.random.uniform(200, 8000, n)
        rev   = spend * slope + np.random.randn(n) * spend * 0.25
        for s, r in zip(spend, rev):
            rows.append({'channel': ch, 'region': region,
                         'spend': round(s, 0), 'revenue': round(r, 0)})
df = pd.DataFrame(rows)

# relplot with col=channel, col_wrap=3, hue+style=region
# Each hue level gets a distinct marker AND color automatically
g = sns.relplot(
    data=df, x='spend', y='revenue',
    col='channel', col_wrap=3,
    hue='region', style='region',     # different marker per region
    markers=['o', 's', '^'],          # explicit marker list
    palette='Set2',
    alpha=0.65, s=40,
    height=3, aspect=1.2,
    kind='scatter'
)
g.set_titles('{col_name}')
g.set_axis_labels('Ad Spend ($)', 'Revenue ($)')
g.figure.suptitle('relplot: Spend vs Revenue — col_wrap=3, marker per region', y=1.03)
g.add_legend(title='Region')
plt.tight_layout()
plt.savefig('scatter_relplot_colwrap_markers.png', dpi=80)
plt.close()
print("relplot col_wrap + marker styles saved.")"""}
],
"rw": {
"title": "Advertising Spend vs Revenue",
"scenario": "A marketing data scientist plots ad spend against revenue by channel to compare ROI and fit regression lines.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(5)
channels = ['Search','Social','Display','Email']
rows = []
for ch in channels:
    n      = 50
    spend  = np.random.uniform(500, 10000, n)
    slope  = {'Search':4.5,'Social':3.0,'Display':1.8,'Email':6.0}[ch]
    rev    = spend * slope + np.random.randn(n) * spend * 0.3
    for s, r in zip(spend, rev):
        rows.append({'channel':ch,'spend':round(s,0),'revenue':round(r,0)})
df = pd.DataFrame(rows)

sns.set_theme(style='whitegrid')
g = sns.lmplot(
    data=df, x='spend', y='revenue', hue='channel',
    col='channel', col_wrap=2,
    scatter_kws=dict(alpha=0.5, s=25),
    height=3.5, aspect=1.2,
    palette='tab10'
)
g.set_axis_labels('Ad Spend ($)', 'Revenue ($)')
g.set_titles('{col_name}')
g.figure.suptitle('Ad Spend vs Revenue by Channel', y=1.02, fontsize=13)

# Print ROI per channel
print("Estimated ROI (revenue/spend):")
for ch in channels:
    sub = df[df.channel==ch]
    roi = sub.revenue.sum() / sub.spend.sum()
    print(f"  {ch:8s}: {roi:.2f}x")
plt.tight_layout()
plt.savefig('rw_scatter_ads.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Scatter with hue, size, and style",
"desc": "Using the 'tips' dataset: 1) Create a scatterplot of 'total_bill' vs 'tip' using hue='day', size='size' (sizes=(30,200)), and style='smoker'. 2) In a second subplot, add a regression line using regplot for smokers vs non-smokers separately (two calls). 3) Label axes clearly. Save as a single wide figure.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Scatter with hue=day, size=size, style=smoker
# TODO: sns.scatterplot(
# TODO:     data=tips, x='total_bill', y='tip',
# TODO:     hue='day', size='size', style='smoker',
# TODO:     sizes=(30, 200), alpha=0.7, palette='tab10', ax=axes[0]
# TODO: )
# TODO: axes[0].set_title('Tip vs Bill — day/size/smoker encoded')

# 2. Regression lines for smokers vs non-smokers
for smoker_val, color in [('Yes', '#e74c3c'), ('No', '#3498db')]:
    subset = tips[tips['smoker'] == smoker_val]
    # TODO: sns.regplot(data=subset, x='total_bill', y='tip',
    # TODO:             scatter_kws=dict(alpha=0.3, s=20, color=color),
    # TODO:             line_kws=dict(color=color, linewidth=2, label=f'Smoker={smoker_val}'),
    # TODO:             ax=axes[1])
    pass
# TODO: axes[1].legend(); axes[1].set_title('Regression by Smoker Status')

plt.tight_layout()
plt.savefig('practice_scatter.png', dpi=80)
plt.close()
print("Saved practice_scatter.png")"""
},

},

{
"title": "6. Heatmap",
"desc": "sns.heatmap renders a matrix as color intensities. Ideal for correlation matrices, confusion matrices, and pivot table results.",
"examples": [
{"label": "Correlation heatmap with annotations", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_theme(style='white')
df = sns.load_dataset('tips')

# Select numeric columns
corr = df[['total_bill','tip','size']].corr()

fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r',
            vmin=-1, vmax=1, linewidths=0.5,
            square=True, ax=ax)
ax.set_title('Feature Correlation Matrix')
plt.tight_layout()
plt.savefig('heatmap_corr.png', dpi=80)
plt.close()"""},
{"label": "Pivot table heatmap", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(9)
months = ['Jan','Feb','Mar','Apr','May','Jun']
regions= ['North','South','East','West']
data   = pd.DataFrame({
    'month':   np.tile(months, 4),
    'region':  np.repeat(regions, 6),
    'revenue': np.random.uniform(50, 200, 24).round(1)
})

pivot = data.pivot(index='region', columns='month', values='revenue')

fig, ax = plt.subplots(figsize=(9, 4))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu',
            linewidths=0.4, ax=ax, cbar_kws=dict(label='Revenue ($K)'))
ax.set_title('Monthly Revenue by Region ($K)')
ax.set_xlabel(''); ax.set_ylabel('')
plt.tight_layout()
plt.savefig('heatmap_pivot.png', dpi=80)
plt.close()"""},
{"label": "Annotated confusion matrix heatmap", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
# Simulate a 4-class confusion matrix
classes = ['Cat', 'Dog', 'Bird', 'Fish']
# True labels and predicted labels
true_labels = np.random.choice(classes, 200, p=[0.3, 0.3, 0.2, 0.2])
# Add some misclassification noise
pred_labels = true_labels.copy()
noise_idx = np.random.choice(len(true_labels), 40, replace=False)
pred_labels[noise_idx] = np.random.choice(classes, 40)

# Build confusion matrix manually
cm = pd.crosstab(pd.Series(true_labels, name='Actual'),
                 pd.Series(pred_labels, name='Predicted'))
# Ensure all classes present
cm = cm.reindex(index=classes, columns=classes, fill_value=0)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Raw counts
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            linewidths=0.5, ax=axes[0])
axes[0].set_title('Confusion Matrix (counts)')

# Normalized (recall per class)
cm_norm = cm.div(cm.sum(axis=1), axis=0).round(2)
sns.heatmap(cm_norm, annot=True, fmt='.2f', cmap='YlOrRd',
            vmin=0, vmax=1, linewidths=0.5, ax=axes[1])
axes[1].set_title('Confusion Matrix (row-normalized recall)')

plt.tight_layout()
plt.savefig('heatmap_confusion.png', dpi=80)
plt.close()"""},
{"label": "sns.clustermap and triangular mask heatmap", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
sns.set_theme(style='white')

# --- Part 1: lower-triangle heatmap using the mask parameter ---
iris = sns.load_dataset('iris')
corr = iris[['sepal_length','sepal_width','petal_length','petal_width']].corr()

# mask=True hides that cell; np.triu masks upper triangle (keep lower + diagonal)
mask_upper = np.triu(np.ones_like(corr, dtype=bool), k=1)

fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(corr, mask=mask_upper, annot=True, fmt='.2f',
            cmap='coolwarm', vmin=-1, vmax=1,
            square=True, linewidths=0.5,
            cbar_kws=dict(shrink=0.7), ax=ax)
ax.set_title('Iris Correlation — lower triangle only (mask=triu)')
plt.tight_layout()
plt.savefig('heatmap_triangle_mask.png', dpi=80)
plt.close()

# --- Part 2: clustermap — hierarchically clusters rows AND columns ---
np.random.seed(7)
n_genes, n_samples = 20, 12
data = pd.DataFrame(
    np.random.randn(n_genes, n_samples),
    index=[f'Gene_{i:02d}' for i in range(n_genes)],
    columns=[f'S{j:02d}' for j in range(n_samples)]
)
# Add block structure so clustering is visible
data.iloc[:8,  :6]  += 2   # high block top-left
data.iloc[12:, 6:]  -= 2   # low block bottom-right

g = sns.clustermap(
    data,
    cmap='RdBu_r', center=0,
    figsize=(9, 7),
    dendrogram_ratio=(0.12, 0.12),
    cbar_pos=(0.02, 0.85, 0.03, 0.12),
    linewidths=0.3,
    method='ward'
)
g.figure.suptitle('clustermap: Hierarchical Clustering of Gene Expression', y=1.01)
plt.savefig('heatmap_clustermap.png', dpi=80, bbox_inches='tight')
plt.close()
print("Triangle mask heatmap and clustermap saved.")"""}
],
"rw": {
"title": "Churn Risk Feature Correlation",
"scenario": "A customer success team uses a heatmap to identify which features are most correlated with customer churn.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(3)
n = 500
df = pd.DataFrame({
    'tenure_months':    np.random.exponential(24, n).clip(1, 72),
    'monthly_spend':    np.random.normal(120, 40, n).clip(20),
    'support_tickets':  np.random.poisson(2, n),
    'logins_per_week':  np.random.normal(5, 3, n).clip(0),
    'nps_score':        np.random.normal(7, 2, n).clip(1, 10),
    'churned':          np.random.binomial(1, 0.25, n),
})
# Add realistic correlations
df['churned'] = (
    (df['support_tickets'] > 4).astype(int) * 0.4 +
    (df['logins_per_week'] < 2).astype(int) * 0.3 +
    (df['nps_score'] < 5).astype(int) * 0.3 +
    np.random.rand(n) * 0.3
) > 0.5

corr = df.corr(numeric_only=True)

sns.set_theme(style='white')
fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(
    corr, annot=True, fmt='.2f', cmap='coolwarm',
    vmin=-1, vmax=1, square=True, linewidths=0.5,
    ax=ax, annot_kws=dict(size=9)
)
ax.set_title('Customer Feature Correlation (churn focus)', pad=12)
plt.tight_layout()
plt.savefig('rw_heatmap_churn.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Annotated Correlation Heatmap",
"desc": "Load the 'iris' dataset. 1) Compute the Pearson correlation matrix for all 4 numeric columns. 2) Plot a heatmap with annotations (fmt='.2f'), cmap='coolwarm', vmin=-1, vmax=1, and square=True. 3) Mask the upper triangle so only the lower triangle and diagonal are shown. Save the figure.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme(style='white')
iris = sns.load_dataset('iris')

# 1. Compute correlation matrix
# TODO: corr = iris[['sepal_length','sepal_width','petal_length','petal_width']].corr()

# 2. Mask upper triangle
# TODO: mask = np.triu(np.ones_like(corr, dtype=bool))

fig, ax = plt.subplots(figsize=(6, 5))

# 3. Plot annotated heatmap with mask
# TODO: sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
# TODO:             vmin=-1, vmax=1, square=True, linewidths=0.5,
# TODO:             mask=mask, ax=ax)
# TODO: ax.set_title('Iris Feature Correlation (lower triangle)')

plt.tight_layout()
plt.savefig('practice_heatmap.png', dpi=80)
plt.close()
print("Saved practice_heatmap.png")"""
},

},

{
"title": "7. Pair Plot",
"desc": "pairplot creates a grid of scatter plots and distributions for all numeric column pairs — fast exploratory data analysis.",
"examples": [
{"label": "Basic pairplot with hue", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')

g = sns.pairplot(
    iris, hue='species',
    palette='Set2',
    plot_kws=dict(alpha=0.5, s=25),
    diag_kind='kde'
)
g.figure.suptitle('Iris Dataset — Pair Plot', y=1.02)
plt.tight_layout()
plt.savefig('pairplot_iris.png', dpi=80)
plt.close()"""},
{"label": "pairplot with regression and custom diag", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')
cols = ['total_bill', 'tip', 'size']

g = sns.pairplot(
    tips[cols + ['time']], hue='time',
    kind='reg',          # scatter + regression line
    diag_kind='hist',    # histogram on diagonal
    palette='Set1',
    plot_kws=dict(scatter_kws=dict(alpha=0.3, s=20),
                  line_kws=dict(linewidth=1.5))
)
g.figure.suptitle('Tips Dataset — Regression Pair Plot', y=1.02)
plt.tight_layout()
plt.savefig('pairplot_reg.png', dpi=80)
plt.close()"""},
{"label": "PairGrid with custom upper/lower/diagonal", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')
cols = ['sepal_length', 'sepal_width', 'petal_length']

g = sns.PairGrid(iris[cols + ['species']], hue='species',
                 palette='tab10', diag_sharey=False)

# Upper triangle: scatter
g.map_upper(sns.scatterplot, alpha=0.4, s=20)

# Lower triangle: KDE contours
g.map_lower(sns.kdeplot, fill=True, alpha=0.25, levels=4)

# Diagonal: histogram
g.map_diag(sns.histplot, kde=True, alpha=0.5)

g.add_legend()
g.figure.suptitle('PairGrid: Custom Upper/Lower/Diagonal', y=1.02)
plt.tight_layout()
plt.savefig('pairgrid_custom.png', dpi=80)
plt.close()"""},
{"label": "Residual Plot & Regression Diagnostics", "code":
"""import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from scipy import stats

sns.set_theme(style='whitegrid', font_scale=1.1)
rng = np.random.default_rng(7)

n = 200
df = pd.DataFrame({
    'market_cap':   rng.lognormal(8, 1.5, n),
    'pe_ratio':     rng.lognormal(3, 0.5, n),
    'debt_equity':  rng.exponential(1.2, n),
    'revenue_growth': rng.normal(0.15, 0.12, n),
    'return_1y':    rng.normal(0.08, 0.22, n),
})
# Add mild relationship
df['return_1y'] += 0.03 * np.log(df['market_cap']) - 0.02 * df['pe_ratio'] + rng.normal(0, 0.05, n)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. Residual plot
slope, intercept, r, p, se = stats.linregress(df['pe_ratio'], df['return_1y'])
residuals = df['return_1y'] - (slope * df['pe_ratio'] + intercept)
axes[0,0].scatter(df['pe_ratio'], residuals, alpha=0.5, color='steelblue', s=25)
axes[0,0].axhline(0, color='red', ls='--', lw=1.5)
axes[0,0].set(title='Residual Plot (PE vs Return)', xlabel='P/E Ratio', ylabel='Residual')
axes[0,0].text(0.05, 0.95, f'r={r:.3f}', transform=axes[0,0].transAxes,
               va='top', fontsize=10)

# 2. Q-Q plot for normality
(osm, osr), (slope2, intercept2, r2) = stats.probplot(df['return_1y'])
axes[0,1].scatter(osm, osr, alpha=0.5, color='coral', s=20)
axes[0,1].plot(osm, slope2*np.array(osm)+intercept2, 'r-', lw=2)
axes[0,1].set(title='Q-Q Plot: Return (1Y)', xlabel='Theoretical Quantiles', ylabel='Sample Quantiles')

# 3. Log transform effect
axes[1,0].hist(df['market_cap'], bins=30, color='seagreen', alpha=0.7, edgecolor='white')
axes[1,0].set(title='Market Cap (Raw)', xlabel='Market Cap')

axes[1,1].hist(np.log(df['market_cap']), bins=30, color='seagreen', alpha=0.7, edgecolor='white')
axes[1,1].set(title='Market Cap (Log-Transformed)', xlabel='log(Market Cap)')

plt.suptitle('Financial Feature Diagnostics', fontsize=14, y=1.01)
plt.tight_layout()
plt.savefig('financial_diagnostics.png', dpi=100)
plt.show()"""}
],
"rw": {
"title": "Financial Feature Exploration Before Modeling",
"scenario": "A quant analyst uses pairplot to explore relationships between financial metrics before selecting features for a predictive model.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(42)
n = 200
pe    = np.random.lognormal(2.8, 0.5, n)
eps   = np.random.normal(5, 2, n).clip(0.5)
rev_g = np.random.normal(0.12, 0.08, n)
roe   = np.random.normal(0.15, 0.07, n).clip(0)

df = pd.DataFrame({
    'P/E Ratio':   pe.round(2),
    'EPS ($)':     eps.round(2),
    'Rev Growth':  rev_g.round(3),
    'ROE':         roe.round(3),
    'sector':      np.random.choice(['Tech','Finance','Healthcare','Energy'], n),
})

sns.set_theme(style='whitegrid', font_scale=0.85)
g = sns.pairplot(
    df, hue='sector',
    vars=['P/E Ratio','EPS ($)','Rev Growth','ROE'],
    palette='tab10',
    plot_kws=dict(alpha=0.4, s=20),
    diag_kind='kde'
)
g.figure.suptitle('Financial Metrics — Pairplot by Sector', y=1.02)
plt.tight_layout()
plt.savefig('rw_pairplot_finance.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Pairplot with hue and custom diagonal",
"desc": "Load the 'penguins' dataset (sns.load_dataset('penguins')). Drop NaN rows. 1) Create a pairplot of bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g with hue='species', diag_kind='kde', kind='scatter'. 2) Then create a second PairGrid where the upper triangle shows scatterplots and the lower triangle shows KDE contours. Save both.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid', font_scale=0.9)
penguins = sns.load_dataset('penguins').dropna()
num_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']

# 1. pairplot with hue='species'
# TODO: g = sns.pairplot(
# TODO:     penguins[num_cols + ['species']], hue='species',
# TODO:     diag_kind='kde', palette='Set2',
# TODO:     plot_kws=dict(alpha=0.4, s=20)
# TODO: )
# TODO: g.figure.suptitle('Penguins Pairplot', y=1.02)
# TODO: plt.tight_layout(); plt.savefig('practice_pairplot.png', dpi=80); plt.close()

# 2. PairGrid: scatter upper, KDE lower
# TODO: g2 = sns.PairGrid(penguins[num_cols + ['species']], hue='species',
# TODO:                   palette='tab10', diag_sharey=False)
# TODO: g2.map_upper(sns.scatterplot, alpha=0.4, s=15)
# TODO: g2.map_lower(sns.kdeplot, fill=True, alpha=0.2, levels=3)
# TODO: g2.map_diag(sns.histplot, kde=True, alpha=0.5)
# TODO: g2.add_legend()
# TODO: g2.figure.suptitle('Penguins PairGrid', y=1.02)
# TODO: plt.tight_layout(); plt.savefig('practice_pairgrid.png', dpi=80); plt.close()

print("Practice pairplot complete")"""
},

},

{
"title": "8. FacetGrid",
"desc": "FacetGrid tiles the same plot across subsets of data defined by row, col, and hue — the most powerful Seaborn layout tool.",
"examples": [
{"label": "FacetGrid with map", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

g = sns.FacetGrid(tips, col='time', row='smoker',
                  height=3, aspect=1.2, margin_titles=True)
g.map_dataframe(sns.histplot, x='total_bill', bins=15, kde=True)
g.set_axis_labels('Total Bill ($)', 'Count')
g.set_titles(row_template='{row_name}', col_template='{col_name}')
g.figure.suptitle('Total Bill by Time & Smoker', y=1.03)
plt.tight_layout()
plt.savefig('facet_grid.png', dpi=80)
plt.close()"""},
{"label": "catplot — figure-level categorical plot", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

# catplot wraps barplot/boxplot/etc into a FacetGrid
g = sns.catplot(
    data=tips, x='day', y='tip',
    col='time', kind='box',
    palette='Set2',
    height=4, aspect=0.9
)
g.set_titles('{col_name}')
g.set_axis_labels('Day', 'Tip ($)')
g.figure.suptitle('Tip Distribution by Day & Meal Time', y=1.03)
plt.tight_layout()
plt.savefig('facet_catplot.png', dpi=80)
plt.close()"""},
{"label": "FacetGrid faceted scatter with custom formatting", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(5)
sns.set_theme(style='whitegrid', font_scale=0.85)

# Synthetic multi-group data
groups = ['A', 'B', 'C']
conditions = ['Low', 'High']
rows = []
for grp in groups:
    for cond in conditions:
        n = 40
        x = np.random.uniform(0, 100, n)
        slope = {'A': 1.5, 'B': 0.8, 'C': 2.2}[grp]
        offset = {'Low': 0, 'High': 50}[cond]
        y = x * slope + offset + np.random.randn(n) * 20
        rows.extend({'group': grp, 'condition': cond,
                     'x': round(xi, 1), 'y': round(yi, 1)}
                    for xi, yi in zip(x, y))
df = pd.DataFrame(rows)

g = sns.FacetGrid(df, col='group', row='condition',
                  height=3, aspect=1.2,
                  margin_titles=True, sharey=False)
g.map_dataframe(sns.scatterplot, x='x', y='y', alpha=0.5, s=20)
g.map_dataframe(sns.regplot, x='x', y='y',
                scatter=False,
                line_kws=dict(color='red', linewidth=1.5))
g.set_axis_labels('X', 'Y')
g.set_titles(col_template='{col_name}', row_template='{row_name}')
g.figure.suptitle('Faceted Scatter with Regression', y=1.03)
plt.tight_layout()
plt.savefig('facet_scatter_reg.png', dpi=80)
plt.close()"""},
{"label": "Grouped Heatmap with Significance Markers", "code":
"""import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from scipy import stats

sns.set_theme(style='white', font_scale=1.1)
rng = np.random.default_rng(42)

regions  = ['North','South','East','West','Central']
products = ['Widget','Gadget','Gizmo','Doohickey']
months   = ['Jan','Feb','Mar','Apr','May','Jun']

# Simulate monthly revenue per region/product
data = rng.uniform(50, 300, (len(regions), len(months)))
df = pd.DataFrame(data, index=regions, columns=months)

# Compute growth vs prior month
growth = df.pct_change(axis=1) * 100
growth.iloc[:, 0] = rng.uniform(-5, 20, len(regions))  # fill first month

# Significance test: is growth > 0?
sig_markers = pd.DataFrame('', index=regions, columns=months)
for region in regions:
    for month in months:
        g = growth.loc[region, month]
        sig_markers.loc[region, month] = '★' if g > 15 else ('▼' if g < -5 else '')

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.heatmap(df, annot=True, fmt='.0f', cmap='YlOrRd',
            linewidths=0.5, ax=axes[0], cbar_kws={'label': 'Revenue ($K)'})
axes[0].set_title('Monthly Revenue by Region', fontsize=12)

# Growth heatmap with significance markers
annot = growth.round(1).astype(str) + '%\n' + sig_markers
sns.heatmap(growth, annot=annot, fmt='', cmap='RdYlGn', center=0,
            linewidths=0.5, ax=axes[1], cbar_kws={'label': 'MoM Growth (%)'},
            annot_kws={'size': 9})
axes[1].set_title('Month-over-Month Growth\n★=High Growth ▼=Decline', fontsize=12)

plt.suptitle('Regional Sales Performance Analysis', fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig('grouped_heatmap.png', dpi=100)
plt.show()"""}
],
"rw": {
"title": "Multi-Region Sales Performance Tiles",
"scenario": "A BI engineer uses FacetGrid to generate one scatter panel per sales region, colored by product category.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(11)
regions    = ['North','South','East','West']
categories = ['Electronics','Clothing','Food','Sports']

rows = []
for region in regions:
    for cat in categories:
        n = 40
        spend   = np.random.uniform(100, 5000, n)
        margin  = np.random.uniform(0.05, 0.45, n)
        rows.extend({'region':region,'category':cat,
                     'spend':round(s,0),'margin':round(m,3)}
                    for s,m in zip(spend, margin))
df = pd.DataFrame(rows)

sns.set_theme(style='whitegrid', font_scale=0.85)
g = sns.FacetGrid(df, col='region', col_wrap=2,
                  height=3.5, aspect=1.3, sharey=True)
g.map_dataframe(sns.scatterplot, x='spend', y='margin',
                hue='category', palette='tab10', alpha=0.6, s=25)

g.add_legend(title='Category')
g.set_axis_labels('Spend ($)', 'Margin')
g.set_titles('{col_name} Region')
g.figure.suptitle('Spend vs Margin by Region & Category', y=1.03)
plt.tight_layout()
plt.savefig('rw_facet_sales.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Faceted Scatter Plots",
"desc": "Using the 'tips' dataset: 1) Build a FacetGrid with col='day' (4 panels) and map a scatterplot of 'total_bill' vs 'tip', colored by 'sex'. 2) Add a regression line to each panel using map_dataframe with sns.regplot (scatter=False). 3) Use sharey=True and set consistent axis labels. Save the figure.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='whitegrid', font_scale=0.9)
tips = sns.load_dataset('tips')

# 1 & 2. FacetGrid: col=day, scatter + regression
# TODO: g = sns.FacetGrid(tips, col='day', col_wrap=2,
# TODO:                   height=3.5, aspect=1.2, sharey=True)
# TODO: g.map_dataframe(sns.scatterplot, x='total_bill', y='tip',
# TODO:                 hue='sex', palette='Set1', alpha=0.6, s=30)
# TODO: g.map_dataframe(sns.regplot, x='total_bill', y='tip',
# TODO:                 scatter=False, line_kws=dict(color='black', linewidth=1.5))

# 3. Labels and title
# TODO: g.set_axis_labels('Total Bill ($)', 'Tip ($)')
# TODO: g.set_titles('{col_name}')
# TODO: g.figure.suptitle('Tip vs Bill by Day (colored by Sex)', y=1.03)
# TODO: g.add_legend(title='Sex')

plt.tight_layout()
plt.savefig('practice_facet.png', dpi=80)
plt.close()
print("Saved practice_facet.png")"""
},

},

{
"title": "9. Time Series & Line Plot",
"desc": "sns.lineplot handles time series naturally — it aggregates multiple observations per x-value and draws confidence intervals.",
"examples": [
{"label": "lineplot with hue and CI", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(5)
weeks   = list(range(1, 13))
regions = ['North','South','East']

rows = []
for region in regions:
    base = np.random.uniform(80, 120)
    trend= np.random.uniform(1, 5)
    for w in weeks:
        for _ in range(5):   # 5 reps per point → CI makes sense
            rows.append({
                'week':   w,
                'region': region,
                'sales':  base + trend * w + np.random.randn() * 15
            })
df = pd.DataFrame(rows)

sns.set_theme(style='whitegrid')
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=df, x='week', y='sales', hue='region',
             palette='Set2', linewidth=2.5, ax=ax)
ax.set_title('Weekly Sales by Region (with 95% CI)')
ax.set_xlabel('Week'); ax.set_ylabel('Sales ($K)')
plt.tight_layout()
plt.savefig('line_hue_ci.png', dpi=80)
plt.close()"""},
{"label": "relplot — faceted time series", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(9)
products = ['Widget','Gadget','Doohickey']
months   = pd.date_range('2024-01-01', periods=12, freq='MS')

rows = []
for prod in products:
    base = np.random.uniform(50, 200)
    vals = base + np.cumsum(np.random.randn(12) * 10)
    for m, v in zip(months, vals):
        rows.append({'month':m,'product':prod,'revenue':max(v,10)})
df = pd.DataFrame(rows)

g = sns.relplot(data=df, x='month', y='revenue',
                col='product', kind='line',
                height=3, aspect=1.3,
                marker='o', markersize=5)
g.set_titles('{col_name}')
for ax in g.axes.flat:
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
    ax.tick_params(axis='x', rotation=45)
g.figure.suptitle('Monthly Revenue by Product', y=1.03)
plt.tight_layout()
plt.savefig('line_relplot.png', dpi=80)
plt.close()"""},
{"label": "Multi-line with markers, annotations, and event shading", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(15)
sns.set_theme(style='whitegrid')

months = list(range(1, 13))
products = ['Alpha', 'Beta', 'Gamma']
rows = []
for prod in products:
    base = np.random.uniform(100, 300)
    vals = base + np.cumsum(np.random.randn(12) * 20)
    for m, v in zip(months, vals):
        rows.append({'month': m, 'product': prod, 'revenue': max(v, 10)})
df = pd.DataFrame(rows)

fig, ax = plt.subplots(figsize=(11, 4))
sns.lineplot(data=df, x='month', y='revenue', hue='product',
             marker='o', markersize=6, linewidth=2,
             palette='tab10', ax=ax)

# Shade a promotion period
ax.axvspan(5, 7, alpha=0.12, color='green', label='Promo period')

# Annotate peak revenue
peak = df.loc[df['revenue'].idxmax()]
ax.annotate(f"Peak: {peak['product']}\n${peak['revenue']:.0f}K",
            xy=(peak['month'], peak['revenue']),
            xytext=(peak['month'] + 0.5, peak['revenue'] - 30),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=8, color='red')

ax.set_title('Monthly Revenue with Event Shading')
ax.set_xlabel('Month'); ax.set_ylabel('Revenue ($K)')
ax.set_xticks(months)
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'], rotation=30)
ax.legend(loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig('line_annotated.png', dpi=80)
plt.close()"""},
{"label": "Anomaly Detection Overlay with Seaborn", "code":
"""import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np, pandas as pd

sns.set_theme(style='darkgrid', font_scale=1.0)
rng = np.random.default_rng(42)

n = 168  # 1 week of hourly data
t = pd.date_range('2024-01-01', periods=n, freq='h')
cpu    = 40 + 20*np.sin(np.linspace(0, 4*np.pi, n)) + rng.normal(0, 5, n)
memory = 60 + 10*np.sin(np.linspace(0, 2*np.pi, n)) + rng.normal(0, 3, n)
# Inject anomalies
cpu[[24, 72, 120, 145]] += rng.uniform(35, 50, 4)
memory[[36, 96, 130]]    += rng.uniform(25, 35, 3)

df = pd.DataFrame({'time': t, 'CPU': cpu.clip(0,100), 'Memory': memory.clip(0,100)})

# Detect anomalies via z-score
for col in ['CPU', 'Memory']:
    mu, sigma = df[col].mean(), df[col].std()
    df[f'{col}_anomaly'] = (df[col] - mu).abs() > 2.5 * sigma

fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

for ax, metric, color in zip(axes, ['CPU', 'Memory'], ['steelblue', 'seagreen']):
    sns.lineplot(data=df, x='time', y=metric, ax=ax, color=color, lw=1.5, label=metric)
    # Shade anomaly regions
    anomalies = df[df[f'{metric}_anomaly']]
    ax.scatter(anomalies['time'], anomalies[metric],
               color='red', s=60, zorder=5, label='Anomaly')
    ax.axhline(df[metric].mean() + 2.5*df[metric].std(),
               color='red', ls='--', lw=1, alpha=0.6, label='2.5sigma threshold')
    ax.set(ylabel=f'{metric} Usage (%)', title=f'{metric} Usage — Anomaly Detection')
    ax.legend(loc='upper right')

axes[-1].set_xlabel('Time')
plt.suptitle('Server Metrics Anomaly Dashboard', fontsize=13, y=1.01)
plt.tight_layout()
plt.savefig('anomaly_dashboard.png', dpi=100)
plt.show()"""}
],
"rw": {
"title": "Server Metrics Time Series Dashboard",
"scenario": "A DevOps engineer plots CPU and memory usage over 24 hours across multiple servers with confidence bands.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(20)
hours   = np.arange(24)
servers = [f'srv-{i:02d}' for i in range(1, 6)]

rows = []
for srv in servers:
    cpu_base  = np.random.uniform(20, 60)
    mem_base  = np.random.uniform(40, 70)
    for h in hours:
        spike = 30 if 9 <= h <= 17 else 0   # business hours spike
        rows.append({
            'hour':   h,
            'server': srv,
            'cpu':    (cpu_base + spike + np.random.randn()*8).clip(5,100),
            'memory': (mem_base + spike*0.3 + np.random.randn()*5).clip(10,95),
        })
df = pd.DataFrame(rows)

sns.set_theme(style='darkgrid')
fig, axes = plt.subplots(1, 2, figsize=(13, 4), sharey=False)

sns.lineplot(data=df, x='hour', y='cpu',    hue='server',
             palette='tab10', linewidth=1.5, alpha=0.7, ax=axes[0])
axes[0].set_title('CPU Usage % (24h)'); axes[0].set_xlabel('Hour')

sns.lineplot(data=df, x='hour', y='memory', hue='server',
             palette='tab10', linewidth=1.5, alpha=0.7, ax=axes[1])
axes[1].set_title('Memory Usage % (24h)'); axes[1].set_xlabel('Hour')
axes[1].get_legend().remove()

# Highlight business hours
for ax in axes:
    ax.axvspan(9, 17, alpha=0.07, color='yellow', label='Business hours')

plt.tight_layout()
plt.savefig('rw_line_servers.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Multi-Line Time Series with Annotations",
"desc": "Create a synthetic dataset of 4 products over 24 months of revenue. 1) Plot all 4 as line series with markers on a single axes using sns.lineplot with hue='product'. 2) Shade a recession period (months 10-14) with axvspan. 3) Annotate the single highest revenue point with an arrow. Save the figure.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(99)
sns.set_theme(style='whitegrid')

products = ['Alpha', 'Beta', 'Gamma', 'Delta']
months = list(range(1, 25))
rows = []
for prod in products:
    base = np.random.uniform(80, 250)
    vals = base + np.cumsum(np.random.randn(24) * 15)
    for m, v in zip(months, vals):
        rows.append({'month': m, 'product': prod, 'revenue': max(v, 5)})
df = pd.DataFrame(rows)

fig, ax = plt.subplots(figsize=(12, 4))

# 1. Line plot with hue and markers
# TODO: sns.lineplot(data=df, x='month', y='revenue', hue='product',
# TODO:              marker='o', markersize=5, linewidth=2, palette='tab10', ax=ax)

# 2. Shade recession period (months 10-14)
# TODO: ax.axvspan(10, 14, alpha=0.12, color='red', label='Recession')

# 3. Annotate peak
peak = df.loc[df['revenue'].idxmax()]
# TODO: ax.annotate(f"Peak: {peak['product']}\\n${peak['revenue']:.0f}K",
# TODO:             xy=(peak['month'], peak['revenue']),
# TODO:             xytext=(peak['month']+1, peak['revenue']-30),
# TODO:             arrowprops=dict(arrowstyle='->', color='darkred'),
# TODO:             fontsize=8, color='darkred')

# TODO: ax.set_title('Product Revenue Over 24 Months')
# TODO: ax.set_xlabel('Month'); ax.set_ylabel('Revenue ($K)')
# TODO: ax.legend(loc='upper left', fontsize=8)

plt.tight_layout()
plt.savefig('practice_lineplot.png', dpi=80)
plt.close()
print("Saved practice_lineplot.png")"""
},

},

{
"title": "10. Customization & Matplotlib Integration",
"desc": "Seaborn returns Axes objects you can modify with any Matplotlib method. Combine both libraries for full control.",
"examples": [
{"label": "Accessing and modifying the Axes", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(data=tips, x='day', y='total_bill', palette='pastel', ax=ax)

# Matplotlib customizations on top
ax.set_title('Total Bill by Day', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('')
ax.set_ylabel('Total Bill', fontsize=11)
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:.0f}'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add median annotations
medians = tips.groupby('day')['total_bill'].median()
for i, (day, med) in enumerate(medians.items()):
    ax.text(i, med + 0.5, f'${med:.0f}', ha='center', fontsize=9, color='darkred')

plt.tight_layout()
plt.savefig('custom_axes.png', dpi=80)
plt.close()"""},
{"label": "Combining multiple Seaborn plots", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')

fig, ax = plt.subplots(figsize=(7, 5))

# Layer 1: violin
sns.violinplot(data=iris, x='species', y='petal_length',
               palette='pastel', inner=None, ax=ax)
# Layer 2: box inside violin
sns.boxplot(data=iris, x='species', y='petal_length',
            width=0.15, fliersize=0,
            boxprops=dict(facecolor='white', zorder=2), ax=ax)
# Layer 3: points
sns.stripplot(data=iris, x='species', y='petal_length',
              color='black', size=2.5, alpha=0.4, jitter=True, ax=ax)

ax.set_title('Petal Length by Species')
ax.set_ylabel('Petal Length (cm)')
plt.tight_layout()
plt.savefig('custom_layered.png', dpi=80)
plt.close()"""},
{"label": "Custom themes, palettes, and publication-ready styling", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

np.random.seed(42)
sns.set_theme(style='ticks', palette='colorblind', font_scale=1.0)

# Synthetic dataset
df = pd.DataFrame({
    'method': np.repeat(['Baseline', 'Model A', 'Model B', 'Model C'], 50),
    'accuracy': np.concatenate([
        np.random.normal(0.72, 0.04, 50),
        np.random.normal(0.81, 0.03, 50),
        np.random.normal(0.78, 0.05, 50),
        np.random.normal(0.85, 0.03, 50),
    ])
})

fig, ax = plt.subplots(figsize=(8, 4))
order = df.groupby('method')['accuracy'].mean().sort_values().index

sns.violinplot(data=df, x='method', y='accuracy', order=order,
               palette='colorblind', inner='box', ax=ax)

ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.set_xlabel(''); ax.set_ylabel('Accuracy')
ax.set_title('Model Accuracy Comparison', fontsize=13, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Significance bracket
best_mean  = df[df['method']=='Model C']['accuracy'].mean()
base_mean  = df[df['method']=='Baseline']['accuracy'].mean()
ax.annotate(f'+{(best_mean-base_mean)*100:.1f}% vs Baseline',
            xy=(0.5, 0.96), xycoords='axes fraction',
            ha='center', fontsize=9, color='darkgreen',
            fontweight='bold')

plt.tight_layout()
plt.savefig('custom_publication.png', dpi=80)
plt.close()"""},
{"label": "rc_context for One-Off Style Overrides", "code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np, pandas as pd

rng = np.random.default_rng(7)
tips = sns.load_dataset('tips')

# Default style
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

sns.histplot(tips['total_bill'], kde=True, ax=axes[0])
axes[0].set_title('Default Style')

# Paper context — smaller for publications
with sns.plotting_context('paper', font_scale=1.2):
    sns.histplot(tips['total_bill'], kde=True, color='seagreen', ax=axes[1])
    axes[1].set_title('Paper Context')

# Talk context — larger for presentations
with sns.plotting_context('talk', font_scale=0.9):
    sns.histplot(tips['tip'], kde=True, color='coral', ax=axes[2])
    axes[2].set_title('Talk Context')

plt.suptitle('Seaborn Context Comparison', fontsize=12)
plt.tight_layout()
plt.savefig('context_comparison.png', dpi=100)
plt.close()

# Override with rc_context — dark background for a single plot
with sns.axes_style('darkgrid'):
    with plt.rc_context({'figure.facecolor': '#1e1e2e',
                         'axes.facecolor':   '#1e1e2e',
                         'axes.labelcolor':  'white',
                         'xtick.color':      'white',
                         'ytick.color':      'white',
                         'text.color':       'white'}):
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=tips, x='total_bill', y='tip',
                        hue='time', palette=['#ffa600','#58508d'],
                        alpha=0.8, s=60, ax=ax2)
        ax2.set_title('Dark Theme Override', color='white', fontsize=13)
        ax2.legend(labelcolor='white', facecolor='#2e2e3e')
        plt.tight_layout()
        plt.savefig('dark_theme.png', dpi=100, facecolor='#1e1e2e')
        plt.close()
print("Context comparison and dark theme override saved.")"""}
],
"rw": {
"title": "Publication-Ready A/B Test Results",
"scenario": "A product analyst creates a publication-ready figure comparing two experiment variants with statistical annotations.",
"code":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)
control  = np.random.normal(45.0, 12, 500)
variant  = np.random.normal(48.5, 11, 500)
df = pd.DataFrame({
    'group':      ['Control']*500 + ['Variant']*500,
    'revenue':    np.concatenate([control, variant]),
})

t_stat, p_val = stats.ttest_ind(control, variant)

sns.set_theme(style='whitegrid')
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# Left: violin + box + strip
sns.violinplot(data=df, x='group', y='revenue',
               palette={'Control':'#3498db','Variant':'#e74c3c'},
               inner=None, ax=axes[0])
sns.boxplot(data=df, x='group', y='revenue',
            width=0.1, fliersize=0,
            boxprops=dict(facecolor='white', zorder=2), ax=axes[0])
axes[0].set_title('Revenue Distribution'); axes[0].set_ylabel('Revenue ($)')

# Right: mean + CI bar chart
summary = df.groupby('group')['revenue'].agg(['mean','sem']).reset_index()
colors  = ['#3498db','#e74c3c']
bars    = axes[1].bar(summary['group'], summary['mean'],
                      yerr=summary['sem']*1.96, capsize=6,
                      color=colors, alpha=0.8, edgecolor='white', linewidth=1.5)
for bar, (_, row) in zip(bars, summary.iterrows()):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                 f"${row['mean']:.1f}", ha='center', fontsize=10, fontweight='bold')

sig = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'
axes[1].annotate(f'p={p_val:.4f} {sig}', xy=(0.5,0.95), xycoords='axes fraction',
                 ha='center', fontsize=10, color='darkgreen' if p_val<0.05 else 'gray')
axes[1].set_title('Mean Revenue ± 95% CI'); axes[1].set_ylabel('Mean Revenue ($)')

fig.suptitle('A/B Test Results — Revenue', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('rw_custom_ab_test.png', dpi=80)
plt.close()"""}
,
"practice": {
"title": "Switch Themes and Build a Custom Publication Plot",
"desc": "1) Apply sns.set_theme with style='ticks' and a custom rc dict that removes top/right spines and sets font_scale=1.1. 2) Plot a violin+strip chart of the 'iris' petal_length by species. 3) Add y-axis gridlines only (ax.yaxis.grid(True)), format the y-axis as cm, and add a bold title. 4) Try swapping to a 'husl' palette with 3 colors. Save the final figure.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Custom theme
# TODO: sns.set_theme(style='ticks', font_scale=1.1, rc={
# TODO:     'axes.spines.top':   False,
# TODO:     'axes.spines.right': False,
# TODO: })

iris = sns.load_dataset('iris')

fig, ax = plt.subplots(figsize=(7, 5))

# 2. Violin + strip with husl palette
my_palette = sns.color_palette('husl', 3)
# TODO: sns.violinplot(data=iris, x='species', y='petal_length',
# TODO:                palette=my_palette, inner=None, ax=ax)
# TODO: sns.stripplot(data=iris, x='species', y='petal_length',
# TODO:               color='black', size=2.5, alpha=0.4, jitter=True, ax=ax)

# 3. Gridlines, axis label, bold title
# TODO: ax.yaxis.grid(True, linewidth=0.7, alpha=0.7)
# TODO: ax.set_ylabel('Petal Length (cm)', fontsize=11)
# TODO: ax.set_xlabel('Species', fontsize=11)
# TODO: ax.set_title('Iris Petal Length by Species', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('practice_custom.png', dpi=80)
plt.close()
print("Saved practice_custom.png")"""
},

}

,
{
    "title": "11. FacetGrid & Multi-Plot Grids",
    "desc": "Create small multiples — the same visualization across data subsets — with FacetGrid, PairGrid, catplot, and relplot.",
    "examples": [
        {
            "label": "FacetGrid with col and hue",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\ntips = sns.load_dataset('tips')\ng = sns.FacetGrid(tips, col='time', hue='smoker', height=4, aspect=0.8)\ng.map(sns.scatterplot, 'total_bill', 'tip', alpha=0.7)\ng.add_legend(); g.set_axis_labels('Total Bill ($)', 'Tip ($)')\ng.set_titles(col_template='{col_name}')\ng.figure.suptitle('Tips by Time and Smoker Status', y=1.02)\nplt.savefig('facetgrid_tips.png', dpi=80, bbox_inches='tight'); plt.close()\nprint('Saved facetgrid_tips.png')"
        },
        {
            "label": "PairGrid for pairwise relationships",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\niris = sns.load_dataset('iris')\ng = sns.PairGrid(iris, hue='species')\ng.map_diag(sns.histplot, alpha=0.6)\ng.map_upper(sns.scatterplot, alpha=0.6)\ng.map_lower(sns.kdeplot)\ng.add_legend()\nplt.savefig('pairgrid_iris.png', dpi=80, bbox_inches='tight'); plt.close()\nprint('Saved pairgrid_iris.png')"
        },
        {
            "label": "catplot — FacetGrid wrapper for categorical",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\ntips = sns.load_dataset('tips')\ng = sns.catplot(data=tips, x='day', y='total_bill',\n                col='time', hue='sex',\n                kind='box', height=4, aspect=0.8)\ng.set_axis_labels('Day', 'Total Bill ($)')\ng.set_titles(col_template='{col_name}')\ng.figure.suptitle('Bills by Day, Time, and Sex', y=1.02)\nplt.savefig('catplot_tips.png', dpi=80, bbox_inches='tight'); plt.close()\nprint('Saved catplot_tips.png')"
        },
        {
            "label": "relplot — FacetGrid wrapper for relationships",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nfmri = sns.load_dataset('fmri')\ng = sns.relplot(data=fmri, x='timepoint', y='signal',\n               col='region', hue='event',\n               kind='line', height=4, aspect=0.9,\n               errorbar='se')\ng.set_titles(col_template='Region: {col_name}')\ng.figure.suptitle('fMRI Signal by Region and Event', y=1.02)\nplt.savefig('relplot_fmri.png', dpi=80, bbox_inches='tight'); plt.close()\nprint('Saved relplot_fmri.png')"
        }
    ],
    "rw_scenario": "A product team needs to compare funnel conversion rates across 4 regions x 3 user segments — FacetGrid creates 12 matching charts in one call.",
    "rw_code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\nregions = ['North','South','East','West']\nsegments = ['New','Returning','VIP']\nrows = []\nfor r in regions:\n    for s in segments:\n        base = {'New':0.05,'Returning':0.12,'VIP':0.25}[s]\n        for _ in range(50):\n            rows.append({'region':r,'segment':s,'converted':int(np.random.rand()<base),'spend':np.random.exponential(50)})\ndf = pd.DataFrame(rows)\n\ng = sns.FacetGrid(df, col='region', hue='segment', height=3.5, aspect=1)\ng.map(sns.barplot, 'segment', 'converted', alpha=0.8, errorbar='se')\ng.set_axis_labels('Segment', 'Conversion Rate')\ng.set_titles('{col_name}')\ng.add_legend(); g.figure.suptitle('Conversion by Region & Segment', y=1.02)\nplt.savefig('funnel_grid.png', dpi=80, bbox_inches='tight'); plt.close()\nprint('Saved funnel_grid.png')",
    "practice": {
        "title": "Multi-Segment Time Series",
        "desc": "Load the 'flights' dataset. Use relplot to create a FacetGrid with col='month' showing passenger count over years, hued by whether month is in summer (Jun-Aug) or not.",
        "starter": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nflights = sns.load_dataset('flights')\n# TODO: add 'season' column: 'Summer' if month in ['June','July','August'] else 'Other'\n# TODO: relplot with col='month', x='year', y='passengers', hue='season', kind='line'\n# TODO: save to 'flights_facet.png'"
    }
},
{
    "title": "12. Statistical Annotations",
    "desc": "Add significance stars, confidence intervals, and comparison markers to seaborn plots for publication-ready statistical charts.",
    "examples": [
        {
            "label": "Bootstrap CI with barplot errorbar",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\ntips = sns.load_dataset('tips')\nfig, ax = plt.subplots(figsize=(8, 5))\nsns.barplot(data=tips, x='day', y='total_bill', hue='sex',\n            errorbar='ci', capsize=0.1, alpha=0.85, ax=ax)\nax.set_title('Mean Total Bill with 95% CI')\nax.set_xlabel('Day'); ax.set_ylabel('Total Bill ($)')\nplt.tight_layout()\nplt.savefig('barplot_ci.png', dpi=80); plt.close()\nprint('Saved barplot_ci.png')"
        },
        {
            "label": "Adding significance stars between groups",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nfrom scipy import stats\n\nnp.random.seed(42)\ngroup_a = np.random.normal(42, 8, 50)\ngroup_b = np.random.normal(48, 9, 50)\nimport pandas as pd\ndf = pd.DataFrame({'value': np.concatenate([group_a, group_b]), 'group': ['A']*50+['B']*50})\n\nfig, ax = plt.subplots(figsize=(6, 5))\nsns.boxplot(data=df, x='group', y='value', ax=ax, palette='Set2')\n\n_, p = stats.ttest_ind(group_a, group_b)\nstars = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'\ny_max = df['value'].max() + 2\nax.plot([0, 0, 1, 1], [y_max, y_max+1, y_max+1, y_max], lw=1.5, color='black')\nax.text(0.5, y_max+1.2, stars, ha='center', va='bottom', fontsize=14)\nax.set_title(f'Group Comparison (p={p:.4f})')\nplt.tight_layout()\nplt.savefig('significance.png', dpi=80); plt.close()\nprint(f'Saved significance.png ({stars})')"
        },
        {
            "label": "Pointplot with SD error bars",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\ntips = sns.load_dataset('tips')\nfig, axes = plt.subplots(1, 2, figsize=(12, 5))\n\nsns.pointplot(data=tips, x='day', y='total_bill', hue='sex',\n              errorbar='sd', capsize=0.1, dodge=True, ax=axes[0])\naxes[0].set_title('Pointplot with SD error bars')\n\nsns.pointplot(data=tips, x='day', y='tip', hue='smoker',\n              errorbar='se', join=False, dodge=0.4, ax=axes[1])\naxes[1].set_title('Pointplot (no join) with SE')\nplt.tight_layout()\nplt.savefig('pointplot.png', dpi=80); plt.close()\nprint('Saved pointplot.png')"
        },
        {
            "label": "Multi-group significance annotations",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\nfrom itertools import combinations\n\nnp.random.seed(42)\ngroups = {'Control': np.random.normal(10,2,40), 'Drug A': np.random.normal(12,2,40), 'Drug B': np.random.normal(14,3,40)}\ndf = pd.DataFrame([(v, g) for g, vals in groups.items() for v in vals], columns=['response','group'])\n\nfig, ax = plt.subplots(figsize=(7, 6))\nsns.boxplot(data=df, x='group', y='response', ax=ax, palette='pastel')\n\npairs = list(combinations(groups.keys(), 2))\ny_max = df['response'].max()\nfor i, (g1, g2) in enumerate(pairs):\n    _, p = stats.ttest_ind(groups[g1], groups[g2])\n    stars = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'ns'\n    x1 = list(groups.keys()).index(g1)\n    x2 = list(groups.keys()).index(g2)\n    y = y_max + 1.5*(i+1)\n    ax.plot([x1, x1, x2, x2], [y, y+0.3, y+0.3, y], lw=1.2, color='black')\n    ax.text((x1+x2)/2, y+0.4, stars, ha='center', fontsize=12)\nax.set_title('Multi-Group Significance Test')\nplt.tight_layout()\nplt.savefig('multi_sig.png', dpi=80); plt.close()\nprint('Saved multi_sig.png')"
        }
    ],
    "rw_scenario": "A clinical trial report compares treatment outcomes across 3 drug groups with significance brackets and p-value stars between all pairs.",
    "rw_code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nnp.random.seed(42)\ndata = {'Placebo': np.random.normal(100, 15, 60),\n        'Low Dose': np.random.normal(108, 14, 60),\n        'High Dose': np.random.normal(118, 13, 60)}\ndf = pd.DataFrame([(v,g) for g,vals in data.items() for v in vals], columns=['bp_reduction','treatment'])\n\nfig, ax = plt.subplots(figsize=(8, 6))\nsns.violinplot(data=df, x='treatment', y='bp_reduction', inner='box', ax=ax, palette='muted')\n\n_, p_lh = stats.ttest_ind(data['Low Dose'], data['High Dose'])\n_, p_ph = stats.ttest_ind(data['Placebo'], data['High Dose'])\nfor i, (pair, p) in enumerate([(('Low Dose','High Dose'), p_lh), (('Placebo','High Dose'), p_ph)]):\n    x1 = list(data.keys()).index(pair[0])\n    x2 = list(data.keys()).index(pair[1])\n    y = df['bp_reduction'].max() + 5*(i+1)\n    stars = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'ns'\n    ax.plot([x1,x1,x2,x2],[y,y+1,y+1,y],lw=1.2,color='black')\n    ax.text((x1+x2)/2, y+1.5, stars, ha='center', fontsize=13)\nax.set_title('Blood Pressure Reduction by Treatment')\nax.set_ylabel('BP Reduction (mmHg)')\nplt.tight_layout()\nplt.savefig('clinical_trial.png', dpi=80); plt.close()\nprint('Saved clinical_trial.png')",
    "practice": {
        "title": "A/B Test Visualization",
        "desc": "Given two groups of purchase amounts (A: mean=$45, B: mean=$52), create a barplot with 95% CI. Run a t-test and add a significance star above the bars if p<0.05.",
        "starter": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nnp.random.seed(42)\ngroup_a = np.random.normal(45, 12, 80)\ngroup_b = np.random.normal(52, 14, 80)\ndf = pd.DataFrame({'amount': np.concatenate([group_a, group_b]), 'group': ['A']*80+['B']*80})\n# TODO: barplot with ci errorbar\n# TODO: t-test\n# TODO: significance annotation if p<0.05\n# TODO: save to 'ab_barplot.png'"
    }
},
{
    "title": "13. Regression & Distribution Plots",
    "desc": "Visualize statistical relationships and distributions with lmplot, residplot, jointplot, and ecdfplot for thorough exploratory analysis.",
    "examples": [
        {
            "label": "lmplot with grouping and confidence bands",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\ntips = sns.load_dataset('tips')\ng = sns.lmplot(data=tips, x='total_bill', y='tip', hue='smoker',\n               ci=95, scatter_kws={'alpha':0.5}, height=5, aspect=1.2)\ng.set_axis_labels('Total Bill ($)', 'Tip ($)')\ng.axes[0,0].set_title('Tip vs Bill by Smoker Status (95% CI)')\nplt.savefig('lmplot.png', dpi=80, bbox_inches='tight'); plt.close()\nprint('Saved lmplot.png')"
        },
        {
            "label": "Residual plot for regression diagnostics",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\ntips = sns.load_dataset('tips')\nfig, axes = plt.subplots(1, 2, figsize=(12, 5))\nsns.residplot(data=tips, x='total_bill', y='tip', lowess=True, ax=axes[0],\n              scatter_kws={'alpha':0.5}, line_kws={'color':'red','linewidth':2})\naxes[0].set_title('Residual Plot (lowess trend)')\naxes[0].axhline(0, color='gray', linestyle='--')\n\nsns.residplot(data=tips, x='size', y='total_bill', ax=axes[1],\n              scatter_kws={'alpha':0.5})\naxes[1].set_title('Residual Plot: size vs bill')\naxes[1].axhline(0, color='gray', linestyle='--')\nplt.tight_layout()\nplt.savefig('residplot.png', dpi=80); plt.close()\nprint('Saved residplot.png')"
        },
        {
            "label": "Joint distribution with marginals",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\ntips = sns.load_dataset('tips')\nfig, axes = plt.subplots(1, 3, figsize=(15, 5))\nfor ax, kind in zip(axes, ['scatter', 'kde', 'hex']):\n    g = sns.jointplot(data=tips, x='total_bill', y='tip', kind=kind, height=4)\n    g.set_axis_labels('Total Bill ($)', 'Tip ($)')\n    g.figure.suptitle(f'Joint Plot: {kind}', y=1.02)\n    g.savefig(f'joint_{kind}.png', dpi=80)\n    plt.close(g.figure)\n    print(f'Saved joint_{kind}.png')"
        },
        {
            "label": "Polynomial regression and ECDF",
            "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\ntips = sns.load_dataset('tips')\nfig, axes = plt.subplots(1, 2, figsize=(12, 5))\n\n# Polynomial regression\nsns.regplot(data=tips, x='total_bill', y='tip', order=2, ax=axes[0],\n            scatter_kws={'alpha':0.4}, line_kws={'color':'red','linewidth':2})\naxes[0].set_title('Polynomial Regression (degree=2)')\n\n# ECDF for comparing distributions\nfor day in ['Thur','Fri','Sat','Sun']:\n    subset = tips[tips['day']==day]\n    sns.ecdfplot(data=subset, x='total_bill', ax=axes[1], label=day)\naxes[1].set_title('ECDF of Total Bill by Day')\naxes[1].legend(); axes[1].set_xlabel('Total Bill ($)')\nplt.tight_layout()\nplt.savefig('regplot_ecdf.png', dpi=80); plt.close()\nprint('Saved regplot_ecdf.png')"
        }
    ],
    "rw_scenario": "A housing analyst explores how square footage predicts price across neighborhoods, checking residuals for heteroscedasticity and comparing price distributions with ECDF.",
    "rw_code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\nn = 150\ndf = pd.DataFrame({\n    'sqft':  np.random.uniform(500, 3000, n),\n    'price': None,\n    'neighborhood': np.random.choice(['Downtown','Suburbs','Uptown'], n),\n})\ndf['price'] = (df['sqft'] * 200 + np.random.choice([50000,80000,120000], n)\n               + np.random.randn(n) * 30000)\n\nfig, axes = plt.subplots(1, 2, figsize=(13, 5))\ng = sns.lmplot(data=df, x='sqft', y='price', hue='neighborhood', ci=90,\n               height=5, aspect=1.1, scatter_kws={'alpha':0.5})\ng.set_axis_labels('Sq Ft', 'Price ($)')\ng.figure.suptitle('Price vs SqFt by Neighborhood', y=1.02)\ng.savefig('housing_lm.png', dpi=80, bbox_inches='tight')\nplt.close(g.figure)\n\nfig, ax = plt.subplots(figsize=(7, 4))\nfor n_label in ['Downtown','Suburbs','Uptown']:\n    sns.ecdfplot(data=df[df['neighborhood']==n_label], x='price', ax=ax, label=n_label)\nax.set_title('Price Distribution by Neighborhood (ECDF)')\nax.set_xlabel('Price ($)'); ax.legend()\nplt.tight_layout()\nplt.savefig('housing_ecdf.png', dpi=80); plt.close()\nprint('Saved housing_lm.png and housing_ecdf.png')",
    "practice": {
        "title": "MPG Regression Analysis",
        "desc": "Using the mpg dataset: (1) create an lmplot of horsepower vs mpg grouped by origin with 90% CI. (2) Plot residuals. (3) Use jointplot(kind='kde') to show the joint distribution.",
        "starter": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nmpg = sns.load_dataset('mpg').dropna()\n# TODO: lmplot x='horsepower', y='mpg', hue='origin', ci=90 -> save 'mpg_lm.png'\n# TODO: residplot x='horsepower', y='mpg' -> save 'mpg_resid.png'\n# TODO: jointplot kind='kde' -> save 'mpg_joint.png'"
    }
},

    {
        "title": "14. FacetGrid & PairGrid",
        "examples": [
            {
                "label": "FacetGrid histogram per group",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({\'value\': np.random.randn(300), \'group\': np.repeat([\'A\',\'B\',\'C\'], 100)})\ng = sns.FacetGrid(df, col=\'group\', height=3.5, aspect=0.9)\ng.map(sns.histplot, \'value\', kde=True, bins=20)\ng.set_titles(col_template=\'{col_name}\')\ng.figure.suptitle(\'FacetGrid by Group\', y=1.02)\ng.savefig(\'facetgrid_hist.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved facetgrid_hist.png\')\nplt.close(\'all\')"
            },
            {
                "label": "FacetGrid row x col (2D grid)",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\n\ntips = sns.load_dataset(\'tips\')\ng = sns.FacetGrid(tips, row=\'sex\', col=\'time\', height=3, aspect=1.2, margin_titles=True)\ng.map(sns.scatterplot, \'total_bill\', \'tip\', alpha=0.6)\ng.add_legend()\ng.savefig(\'facetgrid_2d.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved facetgrid_2d.png\')\nplt.close(\'all\')"
            },
            {
                "label": "PairGrid with mixed plot types",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\n\niris = sns.load_dataset(\'iris\')\ng = sns.PairGrid(iris, hue=\'species\', vars=[\'sepal_length\',\'petal_length\',\'petal_width\'])\ng.map_upper(sns.scatterplot, alpha=0.6)\ng.map_lower(sns.kdeplot, fill=True, alpha=0.4)\ng.map_diag(sns.histplot, kde=True)\ng.add_legend()\ng.savefig(\'pairgrid_mixed.png\', dpi=80, bbox_inches=\'tight\')\nprint(\'Saved pairgrid_mixed.png\')\nplt.close(\'all\')"
            },
            {
                "label": "FacetGrid with custom mapping function",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\ndef scatter_means(x, y, **kw):\n    plt.scatter(x, y, alpha=0.5, **{k:v for k,v in kw.items() if k!=\'label\'})\n    plt.axhline(y.mean(), color=\'red\', ls=\'--\', lw=1.5)\n    plt.axvline(x.mean(), color=\'blue\', ls=\'--\', lw=1.5)\n\nnp.random.seed(42)\ndf = pd.DataFrame({\'x\':np.random.randn(150),\'y\':np.random.randn(150),\n                   \'group\':np.repeat([\'G1\',\'G2\',\'G3\'],50)})\ng = sns.FacetGrid(df, col=\'group\', height=3)\ng.map(scatter_means, \'x\', \'y\')\ng.figure.suptitle(\'Scatter with Group Means\', y=1.02)\ng.savefig(\'facetgrid_custom.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved facetgrid_custom.png\')\nplt.close(\'all\')"
            }
        ],
        "rw_scenario": "You have sales data across 3 regions and 4 products. You need a grid of scatter plots comparing revenue vs units sold for each region-product combination.",
        "rw_code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\nregions = [\'North\',\'South\',\'East\']\nproducts = [\'Electronics\',\'Apparel\',\'Food\',\'Sports\']\nrows = []\nfor r in regions:\n    for p in products:\n        n = 25\n        rows.append(pd.DataFrame({\'region\':r,\'product\':p,\n                                   \'revenue\':np.random.exponential(500,n)+100,\n                                   \'units\':np.random.randint(10,200,n)}))\ndf = pd.concat(rows, ignore_index=True)\ng = sns.FacetGrid(df, row=\'region\', col=\'product\', height=2.2, aspect=1.1, margin_titles=True)\ng.map(sns.scatterplot, \'units\', \'revenue\', alpha=0.5, s=20)\ng.map(sns.regplot, \'units\', \'revenue\', scatter=False, color=\'red\', ci=None)\ng.set_titles(row_template=\'{row_name}\', col_template=\'{col_name}\')\ng.figure.suptitle(\'Revenue vs Units by Region x Product\', y=1.01, fontsize=12)\ng.savefig(\'sales_facetgrid.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved sales_facetgrid.png\')\nplt.close(\'all\')",
        "practice": {
            "title": "Titanic FacetGrid",
            "desc": "Load titanic. Create a FacetGrid with pclass as columns (3 panels). Show age histplot, colored by survived. Add legend and suptitle. Save to titanic_facet.png.",
            "starter": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\n\ntitanic = sns.load_dataset(\'titanic\').dropna(subset=[\'age\'])\n# TODO: FacetGrid col=\'pclass\', hue=\'survived\', map histplot \'age\'\n# TODO: add_legend(), suptitle, save \'titanic_facet.png\'"
        }
    },
    {
        "title": "15. Statistical Visualization Deep Dive",
        "examples": [
            {
                "label": "Violin + swarmplot overlay",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\ndf = pd.DataFrame({\n    \'score\': np.concatenate([np.random.normal(70,10,80), np.random.normal(75,8,80), np.random.normal(65,12,80)]),\n    \'class\': [\'A\']*80 + [\'B\']*80 + [\'C\']*80\n})\nfig, ax = plt.subplots(figsize=(7, 5))\nsns.violinplot(data=df, x=\'class\', y=\'score\', inner=None, palette=\'muted\', alpha=0.7, ax=ax)\nsns.swarmplot(data=df, x=\'class\', y=\'score\', color=\'black\', size=2.5, alpha=0.6, ax=ax)\nax.set_title(\'Score Distribution by Class (Violin + Swarm)\')\nfig.savefig(\'violin_swarm.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved violin_swarm.png\')\nplt.close()"
            },
            {
                "label": "ECDF comparison across groups",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({\n    \'response_ms\': np.concatenate([np.random.exponential(200,300),\n                                   np.random.exponential(150,300),\n                                   np.random.exponential(300,300)]),\n    \'server\': [\'A\']*300 + [\'B\']*300 + [\'C\']*300\n})\nfig, ax = plt.subplots(figsize=(8, 5))\nsns.ecdfplot(data=df, x=\'response_ms\', hue=\'server\', ax=ax)\nax.axvline(200, color=\'gray\', ls=\':\', label=\'200ms target\')\nax.set_title(\'ECDF: Response Time by Server\')\nax.set_xlabel(\'Response Time (ms)\')\nax.legend()\nfig.savefig(\'ecdf_comparison.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved ecdf_comparison.png\')\nplt.close()"
            },
            {
                "label": "Residual plot for regression diagnostics",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\nx = np.linspace(0, 10, 100)\ny = 2*x + np.random.normal(0, 2, 100)\nfig, axes = plt.subplots(1, 2, figsize=(11, 4))\nsns.regplot(x=x, y=y, ax=axes[0])\naxes[0].set_title(\'Regression with CI\')\nsns.residplot(x=x, y=y, ax=axes[1])\naxes[1].axhline(0, color=\'red\', ls=\'--\')\naxes[1].set_title(\'Residuals vs Fitted\')\nfig.tight_layout()\nfig.savefig(\'residual_diagnostic.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved residual_diagnostic.png\')\nplt.close()"
            },
            {
                "label": "Box plot with significance bracket",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({\n    \'value\': np.concatenate([np.random.normal(5,1,50), np.random.normal(7,1.5,50), np.random.normal(6.2,1.2,50)]),\n    \'group\': [\'Control\']*50 + [\'Drug A\']*50 + [\'Drug B\']*50\n})\nfig, ax = plt.subplots(figsize=(7, 5))\nsns.boxplot(data=df, x=\'group\', y=\'value\', palette=\'Set2\', ax=ax)\ny_max = df[\'value\'].max() + 0.5\nax.plot([0, 1], [y_max, y_max], \'k-\', lw=1.5)\nax.text(0.5, y_max+0.1, \'***\', ha=\'center\', fontsize=14)\nax.set_title(\'Drug Effect with Significance Bracket\')\nfig.savefig(\'boxplot_sig.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved boxplot_sig.png\')\nplt.close()"
            }
        ],
        "rw_scenario": "You\'re presenting A/B test results for 3 landing page variants and need violin plots, ECDF comparison, and regression residuals for a comprehensive statistical report.",
        "rw_code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\nvariants = {\'Control\':(3.2,1.1),\'Variant A\':(3.8,1.3),\'Variant B\':(3.5,0.9)}\ndfs = [pd.DataFrame({\'conversion\':np.random.normal(mu,sig,200).clip(0,10),\'variant\':name})\n       for name,(mu,sig) in variants.items()]\ndf = pd.concat(dfs, ignore_index=True)\nfig, axes = plt.subplots(1, 3, figsize=(15, 5))\nsns.violinplot(data=df, x=\'variant\', y=\'conversion\', inner=\'quartile\', palette=\'muted\', ax=axes[0])\naxes[0].set_title(\'Violin Plot\')\nsns.ecdfplot(data=df, x=\'conversion\', hue=\'variant\', ax=axes[1])\naxes[1].axvline(3.5, color=\'gray\', ls=\'--\', alpha=0.7)\naxes[1].set_title(\'ECDF Comparison\')\nsns.boxplot(data=df, x=\'variant\', y=\'conversion\', palette=\'Set2\', ax=axes[2])\naxes[2].set_title(\'Box Plot\')\nfig.suptitle(\'A/B Test Analysis\', fontsize=14, fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'ab_test.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved ab_test.png\')\nplt.close()",
        "practice": {
            "title": "Multi-Stat Figure",
            "desc": "Create 3-panel figure: (1) stripplot of scores by group with means, (2) ECDF for 3 groups, (3) residual plot from regressing score on study_hours. Use whitegrid style.",
            "starter": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({\'score\':np.random.normal(70,15,150), \'group\':np.repeat([\'A\',\'B\',\'C\'],50), \'study_hours\':np.random.uniform(1,8,150)})\n# TODO: 3-panel: stripplot, ecdfplot, residplot\n# TODO: whitegrid style, save \'multi_stat.png\'"
        }
    },
    {
        "title": "16. Custom Seaborn Themes & Styling",
        "examples": [
            {
                "label": "Context comparison (paper/talk/poster)",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({\'x\':np.random.randn(100),\'y\':np.random.randn(100)})\nfig, axes = plt.subplots(2, 2, figsize=(12, 9))\nfor ax, ctx in zip(axes.flat, [\'paper\',\'notebook\',\'talk\',\'poster\']):\n    with sns.plotting_context(ctx):\n        sns.scatterplot(data=df, x=\'x\', y=\'y\', ax=ax, alpha=0.6)\n        ax.set_title(f\'Context: {ctx}\')\nfig.suptitle(\'Seaborn Contexts\', fontsize=14)\nfig.tight_layout()\nfig.savefig(\'contexts.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved contexts.png\')\nplt.close()"
            },
            {
                "label": "Custom set_theme with dark background",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'darkgrid\', palette=\'bright\', font_scale=1.1,\n              rc={\'axes.facecolor\':\'#1e1e2e\',\'figure.facecolor\':\'#1e1e2e\',\n                  \'text.color\':\'white\',\'axes.labelcolor\':\'white\',\n                  \'xtick.color\':\'white\',\'ytick.color\':\'white\'})\nnp.random.seed(42)\ndf = pd.DataFrame({\'x\':np.random.randn(200),\'y\':np.random.randn(200),\'g\':np.random.choice([\'A\',\'B\',\'C\'],200)})\nfig, ax = plt.subplots(figsize=(7,5))\nsns.scatterplot(data=df, x=\'x\', y=\'y\', hue=\'g\', alpha=0.7, ax=ax)\nax.set_title(\'Dark Mode Plot\')\nfig.savefig(\'dark_theme.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved dark_theme.png\')\nsns.set_theme()\nplt.close()"
            },
            {
                "label": "Custom color palettes",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\n\nfig, axes = plt.subplots(2, 2, figsize=(12, 8))\ntips = sns.load_dataset(\'tips\')\npals = [(\'Blues\',4), (\'husl\',4), (\'Set1\',4), ([\'#FF6B6B\',\'#4ECDC4\',\'#45B7D1\',\'#96CEB4\'],4)]\ntitles = [\'Blues (seq)\',\'HUSL (qual)\',\'Set1 (qual)\',\'Custom hex\']\nfor ax, (pal, _), title in zip(axes.flat, pals, titles):\n    with sns.axes_style(\'whitegrid\'):\n        sns.boxplot(data=tips, x=\'day\', y=\'total_bill\', palette=pal, ax=ax)\n        ax.set_title(title)\nfig.tight_layout()\nfig.savefig(\'palettes.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved palettes.png\')\nplt.close()"
            },
            {
                "label": "Despine and axis trimming",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({\'x\':np.repeat(range(5),30),\'y\':np.random.randn(150)+np.repeat([1,2,3,4,5],30)})\nfig, axes = plt.subplots(1, 2, figsize=(12,5))\nwith sns.axes_style(\'ticks\'):\n    sns.boxplot(data=df, x=\'x\', y=\'y\', ax=axes[0], palette=\'pastel\')\n    sns.despine(ax=axes[0], trim=True)\n    axes[0].set_title(\'Despined + trimmed\')\nwith sns.axes_style(\'whitegrid\'):\n    sns.violinplot(data=df, x=\'x\', y=\'y\', ax=axes[1], palette=\'muted\', inner=\'box\')\n    sns.despine(ax=axes[1], left=False, bottom=False, top=True, right=True)\n    axes[1].set_title(\'Whitegrid + partial despine\')\nfig.tight_layout()\nfig.savefig(\'despine_styles.png\', dpi=100, bbox_inches=\'tight\')\nprint(\'Saved despine_styles.png\')\nplt.close()"
            }
        ],
        "rw_scenario": "Your brand guide specifies 5 hex colors, no top/right borders, consistent font scale, and all reports must use the ticks style for a clean minimal look.",
        "rw_code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nBRAND = [\'#003366\',\'#0066CC\',\'#3399FF\',\'#66B2FF\',\'#99CCFF\']\nsns.set_theme(style=\'whitegrid\', palette=BRAND, font_scale=1.2,\n              rc={\'font.family\':\'sans-serif\',\'axes.spines.top\':False,\'axes.spines.right\':False})\nnp.random.seed(42)\ndepts = [\'Eng\',\'Sales\',\'Mktg\',\'Support\',\'HR\']\ndf = pd.DataFrame({\'dept\':np.repeat(depts,40),\n                   \'satisfaction\':np.random.normal(np.tile([7.5,6.8,7.2,6.5,7.8],40)[:200], 1.0)})\nfig, axes = plt.subplots(1, 2, figsize=(14,5))\nsns.barplot(data=df, x=\'dept\', y=\'satisfaction\', palette=BRAND, ax=axes[0])\naxes[0].set_title(\'Employee Satisfaction by Dept\', fontweight=\'bold\')\nsns.violinplot(data=df, x=\'dept\', y=\'satisfaction\', palette=BRAND, inner=\'box\', ax=axes[1])\naxes[1].set_title(\'Satisfaction Distribution\', fontweight=\'bold\')\nfig.suptitle(\'Q4 Employee Survey\', fontsize=16, fontweight=\'bold\', y=1.02)\nfig.tight_layout()\nfig.savefig(\'brand_report.png\', dpi=120, bbox_inches=\'tight\')\nprint(\'Saved brand_report.png\')\nsns.set_theme()\nplt.close()",
        "practice": {
            "title": "Night Mode Report",
            "desc": "Create a dark-themed 3-panel figure (histogram, scatter, bar). Use set_theme with dark facecolor and bright palette. Add suptitle and save at 150 DPI. Reset theme at the end.",
            "starter": "import seaborn as sns\nimport matplotlib\nmatplotlib.use(\'Agg\')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\n# TODO: set_theme dark background rc params\n# TODO: 3-panel: histplot, scatterplot, barplot\n# TODO: suptitle, tight_layout, save \'night_report.png\' 150 DPI\n# TODO: sns.set_theme() at end"
        }
    },
{
"title": "17. Strip Plot & Swarm Plot",
"desc": "Use stripplot() to show individual data points by category and swarmplot() to avoid overplotting by spacing points. Layer them over box or violin plots for richer displays.",
"examples": [
        {"label": "Basic strip and swarm comparison", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))\nsns.stripplot(data=tips, x=\'day\', y=\'total_bill\', ax=ax1,\n              palette=\'Set2\', jitter=True, alpha=0.7, size=5)\nax1.set_title(\'Strip Plot (jitter)\')\n\nsns.swarmplot(data=tips, x=\'day\', y=\'total_bill\', ax=ax2,\n              palette=\'Set2\', size=4)\nax2.set_title(\'Swarm Plot (no overlap)\')\n\nfor ax in (ax1, ax2):\n    ax.set_xlabel(\'Day\'); ax.set_ylabel(\'Total Bill ($)\')\nfig.tight_layout()\nfig.savefig(\'strip_swarm.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved strip_swarm.png\')"},
        {"label": "Strip plot layered over box plot", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\niris = sns.load_dataset(\'iris\')\n\nfig, ax = plt.subplots(figsize=(8, 5))\nsns.boxplot(data=iris, x=\'species\', y=\'sepal_length\', ax=ax,\n            palette=\'pastel\', width=0.5,\n            boxprops=dict(alpha=0.6))\nsns.stripplot(data=iris, x=\'species\', y=\'sepal_length\', ax=ax,\n              palette=\'Set2\', size=5, jitter=True, alpha=0.7,\n              linewidth=0.5, edgecolor=\'gray\')\nax.set_title(\'Box + Strip Plot Overlay\')\nax.set_xlabel(\'Species\'); ax.set_ylabel(\'Sepal Length (cm)\')\nfig.tight_layout()\nfig.savefig(\'box_strip.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved box_strip.png\')"},
        {"label": "Swarm layered over violin", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(0)\ndf = pd.DataFrame({\n    \'score\': np.concatenate([np.random.normal(m, 1, 60) for m in [5, 6.5, 8]]),\n    \'group\': np.repeat([\'Control\', \'Low Dose\', \'High Dose\'], 60)\n})\n\nfig, ax = plt.subplots(figsize=(8, 5))\nsns.violinplot(data=df, x=\'group\', y=\'score\', ax=ax,\n               palette=\'muted\', inner=None, alpha=0.6)\nsns.swarmplot(data=df, x=\'group\', y=\'score\', ax=ax,\n              color=\'black\', size=3, alpha=0.6)\nax.set_title(\'Violin + Swarm: Treatment Groups\')\nax.set_xlabel(\'Group\'); ax.set_ylabel(\'Score\')\nfig.tight_layout()\nfig.savefig(\'violin_swarm.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved violin_swarm.png\')"},
        {"label": "Strip plot with hue and dodge", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\nfig, ax = plt.subplots(figsize=(9, 5))\nsns.stripplot(data=tips, x=\'day\', y=\'total_bill\', hue=\'sex\',\n              dodge=True, jitter=True, alpha=0.7, size=5,\n              palette=\'Set1\', ax=ax)\nax.set_title(\'Strip Plot: Tip Amount by Day and Sex (Dodged)\')\nax.set_xlabel(\'Day\'); ax.set_ylabel(\'Total Bill ($)\')\nax.legend(title=\'Sex\', bbox_to_anchor=(1, 1))\nfig.tight_layout()\nfig.savefig(\'strip_hue.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved strip_hue.png\')"}
    ],
"rw": {
    "title": "Employee Salary Audit",
    "scenario": "HR needs to show individual salaries by department and gender on top of a violin plot to reveal outliers and within-group spread. Use dodge=True so genders are side by side.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(7)\ndepts = [\'Eng\', \'Sales\', \'Mktg\', \'HR\']\ndf = pd.DataFrame({\n    \'salary\': np.concatenate([\n        np.random.normal(m, s, 60)\n        for m, s in [(95,15),(70,12),(75,13),(65,10)] for _ in range(1)\n    ] * 2),\n    \'dept\': np.tile(np.repeat(depts, 60), 2),\n    \'gender\': np.repeat([\'Female\',\'Male\'], 240)\n})\n\nfig, ax = plt.subplots(figsize=(11, 6))\nsns.violinplot(data=df, x=\'dept\', y=\'salary\', hue=\'gender\',\n               split=True, inner=None, palette=\'pastel\', alpha=0.6, ax=ax)\nsns.stripplot(data=df, x=\'dept\', y=\'salary\', hue=\'gender\',\n              dodge=True, jitter=True, alpha=0.5, size=3,\n              palette=\'dark:#333333\', ax=ax, legend=False)\nax.set_title(\'Salary Distribution by Department & Gender\', fontweight=\'bold\')\nax.set_xlabel(\'Department\'); ax.set_ylabel(\'Salary ($K)\')\nhandles, labels = ax.get_legend_handles_labels()\nax.legend(handles[:2], labels[:2], title=\'Gender\')\nfig.tight_layout()\nfig.savefig(\'salary_audit.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved salary_audit.png\')"
},
"practice": {
    "title": "Strip/Swarm Practice",
    "desc": "Load the \'penguins\' dataset. Create a 1x2 subplot: (1) swarmplot of body_mass_g by species with hue=sex, (2) stripplot of flipper_length_mm by island with box overlay. Use palette=\'colorblind\' and whitegrid style.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\npenguins = sns.load_dataset(\'penguins\').dropna()\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))\n# TODO: swarmplot body_mass_g by species, hue=sex\n# TODO: boxplot + stripplot flipper_length_mm by island\n# TODO: colorblind palette, titles, labels\nfig.tight_layout()\nfig.savefig(\'penguin_points.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved penguin_points.png\')"
}
},

{
"title": "18. Point Plot & Statistical Line Plots",
"desc": "Use pointplot() to display means with confidence intervals for categorical variables. Use lineplot() with hue for multi-group time series with automatic CI shading.",
"examples": [
        {"label": "pointplot: means with CI by category", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))\nsns.pointplot(data=tips, x=\'day\', y=\'total_bill\', ax=ax1,\n              palette=\'Set2\', capsize=0.1, errwidth=2,\n              markers=\'o\', linestyles=\'-\')\nax1.set_title(\'Point Plot: Mean Bill by Day\')\n\nsns.pointplot(data=tips, x=\'day\', y=\'total_bill\', hue=\'sex\',\n              ax=ax2, palette=\'Set1\', dodge=True,\n              capsize=0.08, errwidth=1.5)\nax2.set_title(\'Point Plot: By Day and Sex\')\n\nfor ax in (ax1, ax2):\n    ax.set_xlabel(\'Day\'); ax.set_ylabel(\'Mean Total Bill ($)\')\nfig.tight_layout()\nfig.savefig(\'pointplot.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved pointplot.png\')"},
        {"label": "lineplot with confidence interval shading", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'darkgrid\')\nnp.random.seed(0)\nn = 50\ndf = pd.DataFrame({\n    \'t\': np.tile(np.arange(n), 3),\n    \'value\': np.concatenate([\n        np.cumsum(np.random.randn(n)) + 5,\n        np.cumsum(np.random.randn(n)) + 3,\n        np.cumsum(np.random.randn(n)) + 7,\n    ]),\n    \'model\': np.repeat([\'Model A\', \'Model B\', \'Model C\'], n)\n})\n\n# Add repeated measurements for CI\ndf_rep = pd.concat([df.assign(value=df.value + np.random.randn(len(df))*0.5)\n                    for _ in range(5)], ignore_index=True)\n\nfig, ax = plt.subplots(figsize=(10, 5))\nsns.lineplot(data=df_rep, x=\'t\', y=\'value\', hue=\'model\',\n             palette=\'Set2\', linewidth=2, ax=ax)\nax.set_title(\'lineplot with 95% CI Shading\')\nax.set_xlabel(\'Time Step\'); ax.set_ylabel(\'Value\')\nfig.tight_layout()\nfig.savefig(\'lineplot_ci.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved lineplot_ci.png\')"},
        {"label": "lineplot with markers and styles", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(1)\nmonths = list(range(1, 13))\ndf = pd.DataFrame({\n    \'month\': months * 3,\n    \'revenue\': (\n        [100 + i*8 + np.random.randn()*5 for i in range(12)] +\n        [80 + i*6 + np.random.randn()*4 for i in range(12)] +\n        [60 + i*10 + np.random.randn()*6 for i in range(12)]\n    ),\n    \'region\': [\'North\']*12 + [\'South\']*12 + [\'East\']*12\n})\n\nfig, ax = plt.subplots(figsize=(10, 5))\nsns.lineplot(data=df, x=\'month\', y=\'revenue\', hue=\'region\',\n             style=\'region\', markers=True, dashes=False,\n             palette=\'Set1\', linewidth=2, ax=ax)\nax.set_title(\'Monthly Revenue by Region\')\nax.set_xlabel(\'Month\'); ax.set_ylabel(\'Revenue ($K)\')\nax.legend(title=\'Region\')\nfig.tight_layout()\nfig.savefig(\'lineplot_markers.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved lineplot_markers.png\')"},
        {"label": "pointplot vs barplot comparison", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntitanic = sns.load_dataset(\'titanic\')\n\nfig, axes = plt.subplots(1, 3, figsize=(14, 5))\n# Bar: shows aggregated height\nsns.barplot(data=titanic, x=\'class\', y=\'survived\', hue=\'sex\',\n            palette=\'Set2\', ax=axes[0])\naxes[0].set_title(\'barplot: Mean Survival Rate\')\n\n# Point: cleaner for comparison\nsns.pointplot(data=titanic, x=\'class\', y=\'survived\', hue=\'sex\',\n              palette=\'Set1\', dodge=True, capsize=0.1, ax=axes[1])\naxes[1].set_title(\'pointplot: Same Data\')\n\n# Count the actual survivors\nsurv = titanic.groupby([\'class\',\'sex\'])[\'survived\'].mean().reset_index()\nsns.pointplot(data=surv, x=\'class\', y=\'survived\', hue=\'sex\',\n              palette=\'Set1\', dodge=True, capsize=0.1, ax=axes[2],\n              markers=[\'o\', \'s\'], linestyles=[\'-\',\'--\'])\naxes[2].set_title(\'pointplot: Precomputed\')\n\nfor ax in axes:\n    ax.set_ylim(0, 1); ax.set_ylabel(\'Survival Rate\')\nfig.tight_layout()\nfig.savefig(\'point_vs_bar.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved point_vs_bar.png\')"}
    ],
"rw": {
    "title": "Student Performance Tracking",
    "scenario": "Plot mean exam scores with 95% CI for 4 subjects across 3 school terms. Use pointplot with dodge for gender comparison and a lineplot showing term-over-term trend with shaded uncertainty.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(42)\nsubjects = [\'Math\', \'Science\', \'English\', \'History\']\nterms = [\'T1\', \'T2\', \'T3\']\nrows = []\nfor subj in subjects:\n    base = np.random.uniform(60, 85)\n    for term in terms:\n        for gender in [\'Female\', \'Male\']:\n            n = 30\n            offset = {\'T1\': 0, \'T2\': 3, \'T3\': 6}[term]\n            g_offset = 2 if gender == \'Female\' else 0\n            scores = np.random.normal(base + offset + g_offset, 8, n)\n            for s in scores:\n                rows.append({\'subject\': subj, \'term\': term, \'gender\': gender, \'score\': s})\ndf = pd.DataFrame(rows)\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\nsns.pointplot(data=df, x=\'subject\', y=\'score\', hue=\'gender\',\n              dodge=True, capsize=0.08, palette=\'Set1\',\n              markers=[\'o\',\'s\'], linestyles=[\'-\',\'--\'], ax=ax1)\nax1.set_title(\'Mean Score by Subject & Gender\', fontweight=\'bold\')\nax1.set_xlabel(\'Subject\'); ax1.set_ylabel(\'Mean Score\')\n\nterm_df = df.groupby([\'term\',\'subject\']).score.mean().reset_index()\nsns.lineplot(data=df, x=\'term\', y=\'score\', hue=\'subject\',\n             palette=\'tab10\', linewidth=2, markers=True, ax=ax2)\nax2.set_title(\'Score Trend by Term\', fontweight=\'bold\')\nax2.set_xlabel(\'Term\'); ax2.set_ylabel(\'Score\')\nax2.legend(title=\'Subject\', bbox_to_anchor=(1,1))\nfig.tight_layout()\nfig.savefig(\'student_performance.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved student_performance.png\')"
},
"practice": {
    "title": "Point/Line Plot Practice",
    "desc": "Load the \'fmri\' dataset from seaborn. Plot a lineplot of signal by timepoint, with hue=event and style=region. Add a pointplot below it showing mean signal per region. Use a 2x1 subplot with shared x-axis.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'darkgrid\')\nfmri = sns.load_dataset(\'fmri\')\n\nfig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=False)\n# TODO: lineplot signal by timepoint, hue=event, style=region\n# TODO: pointplot mean signal by region with capsize\n# TODO: titles, labels, tight_layout\nfig.savefig(\'fmri_plots.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved fmri_plots.png\')"
}
},

{
"title": "19. ECDF & Distribution Comparison",
"desc": "Use ecdfplot() for empirical CDFs, histplot() with multiple groups, and kdeplot() to compare distributions across categories without assuming a parametric form.",
"examples": [
        {"label": "ECDF plot for group comparison", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(0)\ndf = pd.DataFrame({\n    \'value\': np.concatenate([\n        np.random.normal(5, 1.5, 200),\n        np.random.normal(7, 1.0, 200),\n        np.random.exponential(2, 200) + 3,\n    ]),\n    \'group\': np.repeat([\'Normal(5,1.5)\', \'Normal(7,1)\', \'Exp+3\'], 200)\n})\n\nfig, ax = plt.subplots(figsize=(9, 5))\nsns.ecdfplot(data=df, x=\'value\', hue=\'group\', palette=\'Set2\', linewidth=2)\nax.axhline(0.5, color=\'gray\', linestyle=\'--\', linewidth=1, label=\'Median\')\nax.set_title(\'ECDF: Distribution Comparison\')\nax.set_xlabel(\'Value\'); ax.set_ylabel(\'Cumulative Proportion\')\nax.legend(title=\'Group\')\nfig.tight_layout()\nfig.savefig(\'ecdf.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved ecdf.png\')"},
        {"label": "Overlapping KDE comparison", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\niris = sns.load_dataset(\'iris\')\n\nfig, axes = plt.subplots(1, 2, figsize=(12, 5))\n# Separate feature distributions per species\nfor feat, ax in zip([\'sepal_length\', \'petal_length\'], axes):\n    sns.kdeplot(data=iris, x=feat, hue=\'species\',\n                fill=True, alpha=0.35, linewidth=2, palette=\'Set2\', ax=ax)\n    ax.set_title(f\'KDE: {feat.replace(\"_\",\" \").title()}\')\n    ax.set_xlabel(feat.replace(\'_\',\' \').title())\nfig.tight_layout()\nfig.savefig(\'kde_compare.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved kde_compare.png\')"},
        {"label": "histplot with stat=\'density\' and kde overlay", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(1)\ndf = pd.DataFrame({\n    \'response_ms\': np.concatenate([\n        np.random.lognormal(5, 0.5, 300),\n        np.random.lognormal(5.5, 0.4, 200),\n    ]),\n    \'endpoint\': np.repeat([\'/api/search\', \'/api/checkout\'], [300, 200])\n})\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))\nsns.histplot(data=df, x=\'response_ms\', hue=\'endpoint\',\n             stat=\'density\', kde=True, alpha=0.4, palette=\'Set1\',\n             common_norm=False, ax=ax1)\nax1.set_title(\'Histogram with KDE — Linear scale\')\nax1.set_xlabel(\'Response Time (ms)\')\n\nsns.histplot(data=df, x=\'response_ms\', hue=\'endpoint\',\n             stat=\'density\', kde=True, alpha=0.4, palette=\'Set1\',\n             common_norm=False, log_scale=True, ax=ax2)\nax2.set_title(\'Histogram with KDE — Log scale\')\nax2.set_xlabel(\'Response Time (ms)\')\nfig.tight_layout()\nfig.savefig(\'hist_kde_compare.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved hist_kde_compare.png\')"},
        {"label": "ECDF with percentile markers", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(2)\ndata = pd.DataFrame({\n    \'latency_ms\': np.random.lognormal(5, 0.7, 1000),\n    \'server\': np.random.choice([\'US-East\', \'EU-West\', \'AP-South\'], 1000)\n})\n\nfig, ax = plt.subplots(figsize=(9, 5))\nsns.ecdfplot(data=data, x=\'latency_ms\', hue=\'server\',\n             palette=\'tab10\', linewidth=2, ax=ax)\n\n# Mark p50, p95, p99\nfor pct, label, color in [(50,\'p50\',\'gray\'),(95,\'p95\',\'orange\'),(99,\'p99\',\'red\')]:\n    val = np.percentile(data[\'latency_ms\'], pct)\n    ax.axvline(val, color=color, linestyle=\'--\', linewidth=1.2, alpha=0.8)\n    ax.axhline(pct/100, color=color, linestyle=\':\', linewidth=0.8, alpha=0.5)\n    ax.text(val+50, pct/100-0.04, f\'{label}: {val:.0f}ms\',\n            fontsize=8, color=color)\n\nax.set_title(\'API Latency ECDF by Server Region\')\nax.set_xlabel(\'Latency (ms)\'); ax.set_ylabel(\'Cumulative Proportion\')\nfig.tight_layout()\nfig.savefig(\'ecdf_percentiles.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved ecdf_percentiles.png\')"}
    ],
"rw": {
    "title": "A/B Test Distribution Analysis",
    "scenario": "Compare three e-commerce funnel variants: show ECDF of conversion values, overlapping KDE of order sizes, and a combined histplot with p50/p90 markers for each variant.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(99)\nvariants = {\'Control\': (45, 12), \'Variant A\': (52, 14), \'Variant B\': (48, 10)}\ndfs = [pd.DataFrame({\'order_value\': np.random.normal(mu, sd, 300).clip(5), \'variant\': name})\n       for name, (mu, sd) in variants.items()]\ndf = pd.concat(dfs, ignore_index=True)\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))\nsns.ecdfplot(data=df, x=\'order_value\', hue=\'variant\',\n             palette=\'Set1\', linewidth=2, ax=ax1)\nfor pct, ls in [(50,\'--\'),(90,\':\')]:\n    ax1.axhline(pct/100, color=\'gray\', linestyle=ls, linewidth=1)\n    ax1.text(ax1.get_xlim()[0]+1, pct/100+0.01, f\'p{pct}\', fontsize=8, color=\'gray\')\nax1.set_title(\'ECDF of Order Value by Variant\', fontweight=\'bold\')\nax1.set_xlabel(\'Order Value ($)\')\n\nsns.kdeplot(data=df, x=\'order_value\', hue=\'variant\',\n            fill=True, alpha=0.3, linewidth=2, palette=\'Set1\',\n            common_norm=False, ax=ax2)\nax2.set_title(\'KDE: Order Value Distribution\', fontweight=\'bold\')\nax2.set_xlabel(\'Order Value ($)\')\nfig.tight_layout()\nfig.savefig(\'ab_distribution.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved ab_distribution.png\')"
},
"practice": {
    "title": "Distribution Comparison Practice",
    "desc": "Load the \'titanic\' dataset. Create a 1x3 figure: (1) ecdfplot of \'fare\' by \'class\', (2) kdeplot of \'age\' by \'survived\' (use hue), (3) histplot of \'fare\' with log_scale=True, hue=\'class\'. Drop NaN rows first.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntitanic = sns.load_dataset(\'titanic\').dropna(subset=[\'age\',\'fare\'])\n\nfig, axes = plt.subplots(1, 3, figsize=(15, 5))\n# TODO: ecdfplot fare by class\n# TODO: kdeplot age by survived\n# TODO: histplot fare log scale by class\nfig.tight_layout()\nfig.savefig(\'titanic_dist.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved titanic_dist.png\')"
}
},

{
"title": "20. Cluster Map",
"desc": "Use clustermap() to apply hierarchical clustering to rows and columns of a matrix, revealing natural groupings in correlation matrices, gene expression, or feature similarity data.",
"examples": [
        {"label": "Basic clustermap on iris correlation", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\niris = sns.load_dataset(\'iris\')\ncorr = iris.drop(\'species\', axis=1).corr()\n\ng = sns.clustermap(corr, cmap=\'RdBu_r\', vmin=-1, vmax=1,\n                   annot=True, fmt=\'.2f\', figsize=(7, 7),\n                   linewidths=0.5)\ng.ax_heatmap.set_title(\'Iris Feature Correlation Clustermap\', pad=50)\nplt.savefig(\'clustermap_iris.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved clustermap_iris.png\')"},
        {"label": "Clustermap with row/col color bars", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(0)\nn_genes, n_samples = 20, 12\ngroups = [\'A\',\'A\',\'A\',\'A\',\'B\',\'B\',\'B\',\'B\',\'C\',\'C\',\'C\',\'C\']\ndata = pd.DataFrame(\n    np.random.randn(n_genes, n_samples) +\n    np.array([np.sin(np.linspace(0,3,n_samples))*(i%3-1) for i in range(n_genes)]),\n    index=[f\'Gene_{i:02d}\' for i in range(n_genes)],\n    columns=[f\'S{i+1:02d}\' for i in range(n_samples)]\n)\npalette = {\'A\':\'#4c72b0\', \'B\':\'#dd8452\', \'C\':\'#55a868\'}\ncol_colors = pd.Series(groups, index=data.columns).map(palette)\n\ng = sns.clustermap(data, cmap=\'vlag\', figsize=(10, 8),\n                   col_colors=col_colors,\n                   row_cluster=True, col_cluster=True,\n                   z_score=0, linewidths=0.3)\ng.ax_heatmap.set_title(\'Gene Expression Clustermap\', pad=50)\nplt.savefig(\'clustermap_genes.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved clustermap_genes.png\')"},
        {"label": "Clustermap with standard_scale", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(1)\nfeatures = [\'Revenue\', \'Growth\', \'Margin\', \'CAC\', \'LTV\', \'Churn\']\ncompanies = [f\'Co{i:02d}\' for i in range(1, 16)]\ndata = pd.DataFrame(\n    np.random.randn(len(companies), len(features)),\n    index=companies, columns=features\n)\n# Add cluster structure\ndata.iloc[:5, :3] += 2\ndata.iloc[5:10, 3:] -= 2\ndata.iloc[10:, [0,2,4]] += 1.5\n\ng = sns.clustermap(data, cmap=\'coolwarm\', figsize=(8, 10),\n                   standard_scale=1,  # standardize each column\n                   linewidths=0.4, annot=False,\n                   dendrogram_ratio=(0.15, 0.2))\ng.ax_heatmap.set_title(\'Company KPI Clustermap\n(column-standardized)\', pad=50)\nplt.savefig(\'clustermap_kpi.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved clustermap_kpi.png\')"},
        {"label": "Clustermap method and metric options", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(2)\ndata = pd.DataFrame(\n    np.random.randn(15, 10),\n    index=[f\'R{i}\' for i in range(15)],\n    columns=[f\'C{j}\' for j in range(10)]\n)\ndata.iloc[:5, :4] += 2.5\ndata.iloc[10:, 6:] += 2.5\n\nfig, axes_list = plt.subplots(1, 2, figsize=(14, 6))\nfor ax, (method, metric) in zip(axes_list, [(\'ward\',\'euclidean\'),(\'average\',\'correlation\')]):\n    g = sns.clustermap(data, cmap=\'RdYlBu_r\', figsize=(6, 5),\n                       method=method, metric=metric,\n                       linewidths=0.3)\n    g.fig.suptitle(f\'method={method}, metric={metric}\', y=1.01, fontsize=10)\n    g.fig.savefig(f\'clustermap_{method}.png\', dpi=100, bbox_inches=\'tight\')\n    plt.close(g.fig)\nprint(\'Saved clustermap_ward.png and clustermap_average.png\')"}
    ],
"rw": {
    "title": "Customer Segment Heatmap",
    "scenario": "Build a clustermap of customer segments vs. behavioral features (purchase frequency, avg order, recency, CLV, support tickets). Use z_score=0, vlag colormap, and annotate row colors by segment.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(55)\nsegments = [\'Loyal\',\'At-Risk\',\'New\',\'Churned\',\'VIP\']\nfeatures = [\'Frequency\',\'Avg Order\',\'Recency\',\'CLV\',\'Tickets\']\nn_each = 15\nrows = []\ncentroids = {\n    \'Loyal\':   [8, 120, 5, 960, 1],\n    \'At-Risk\': [2, 80, 45, 160, 4],\n    \'New\':     [1, 95, 15, 95, 0],\n    \'Churned\': [0, 60, 120, 0, 6],\n    \'VIP\':     [12, 400, 3, 4800, 2],\n}\nfor seg, center in centroids.items():\n    noise = np.random.randn(n_each, len(features)) * np.array([1, 20, 10, 200, 1])\n    block = np.array(center) + noise\n    df_seg = pd.DataFrame(block, columns=features)\n    df_seg[\'segment\'] = seg\n    rows.append(df_seg)\ndf = pd.concat(rows, ignore_index=True)\nmatrix = df[features].values\nrow_labels = df[\'segment\']\npalette_seg = {\'Loyal\':\'#55a868\',\'At-Risk\':\'#dd8452\',\'New\':\'#4c72b0\',\n               \'Churned\':\'#c44e52\',\'VIP\':\'#9467bd\'}\nrow_colors = row_labels.map(palette_seg)\n\ndata_df = pd.DataFrame(matrix, columns=features,\n                        index=[f\'{seg}_{i}\' for seg, n in [(s, n_each) for s in segments]\n                               for i in range(n_each)])\ng = sns.clustermap(pd.DataFrame(matrix, columns=features),\n                   cmap=\'vlag\', z_score=0, figsize=(9, 11),\n                   row_colors=row_colors.values,\n                   linewidths=0.2, dendrogram_ratio=(0.2, 0.15))\ng.ax_heatmap.set_title(\'Customer Segment Behavioral Clustermap\', pad=50, fontsize=12)\nplt.savefig(\'customer_clustermap.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved customer_clustermap.png\')"
},
"practice": {
    "title": "Clustermap Practice",
    "desc": "Generate a 12x8 random matrix with 3 obvious block clusters (add +2 to block (0:4, 0:3), +(-2) to block (4:8, 3:6)). Plot a clustermap with method=\'ward\', cmap=\'RdBu_r\', and z_score=0. Annotate the values with fmt=\'.1f\'.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(3)\ndata = np.random.randn(12, 8)\ndata[:4, :3] += 2.5\ndata[4:8, 3:6] -= 2.5\ndata[8:, 5:] += 1.5\ndf = pd.DataFrame(data,\n                  index=[f\'R{i}\' for i in range(12)],\n                  columns=[f\'C{j}\' for j in range(8)])\n# TODO: clustermap method=\'ward\', cmap=\'RdBu_r\', z_score=0, annot=True\n# TODO: save \'block_clustermap.png\'"
}
},

{
"title": "21. Joint Plot Advanced",
"desc": "Use jointplot() to show the bivariate relationship alongside marginal univariate distributions. Explore kind=\'hex\', \'kde\', \'reg\', and custom marginal plots with JointGrid.",
"examples": [
        {"label": "jointplot: hex, kde, reg, scatter kinds", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\nkinds = [\'scatter\', \'hex\', \'kde\', \'reg\']\nfor kind in kinds:\n    g = sns.jointplot(data=tips, x=\'total_bill\', y=\'tip\',\n                      kind=kind, palette=\'Set2\', height=5,\n                      marginal_kws=dict(bins=25))\n    g.fig.suptitle(f\"kind=\'{kind}\'\", y=1.02)\n    g.fig.savefig(f\'joint_{kind}.png\', dpi=100, bbox_inches=\'tight\')\n    plt.close(g.fig)\nprint(\'Saved joint_scatter/hex/kde/reg.png\')"},
        {"label": "jointplot with hue", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\niris = sns.load_dataset(\'iris\')\n\ng = sns.jointplot(data=iris, x=\'sepal_length\', y=\'petal_length\',\n                  hue=\'species\', palette=\'Set2\',\n                  height=6, marginal_kws=dict(fill=True, alpha=0.4))\ng.fig.suptitle(\'Iris: Sepal vs Petal Length (hue=species)\', y=1.02)\ng.fig.savefig(\'joint_hue.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved joint_hue.png\')"},
        {"label": "JointGrid: custom marginals", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(42)\ndf = pd.DataFrame({\n    \'x\': np.random.lognormal(2, 0.5, 300),\n    \'y\': np.random.lognormal(1.5, 0.6, 300)\n})\n\ng = sns.JointGrid(data=df, x=\'x\', y=\'y\', height=6)\ng.plot_joint(sns.scatterplot, alpha=0.4, color=\'steelblue\', s=25)\ng.plot_joint(sns.kdeplot, levels=5, color=\'navy\', linewidths=1.0)\ng.plot_marginals(sns.histplot, kde=True, bins=25, color=\'steelblue\', alpha=0.6)\n\ng.ax_joint.set_xlabel(\'X (lognormal)\'); g.ax_joint.set_ylabel(\'Y (lognormal)\')\ng.fig.suptitle(\'JointGrid: Scatter + KDE + Histogram Marginals\', y=1.01)\ng.fig.savefig(\'joint_grid_custom.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved joint_grid_custom.png\')"},
        {"label": "jointplot with regression and stats", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(5)\nn = 150\nx = np.random.uniform(10, 100, n)\ny = 0.5*x + np.random.randn(n)*8 + 5\n\ndf = pd.DataFrame({\'x\': x, \'y\': y})\n\ng = sns.jointplot(data=df, x=\'x\', y=\'y\',\n                  kind=\'reg\', height=6,\n                  scatter_kws=dict(alpha=0.5, s=30, color=\'steelblue\'),\n                  line_kws=dict(color=\'red\', linewidth=2),\n                  marginal_kws=dict(bins=20, kde=True))\n# Compute and annotate correlation\nr = df.corr().iloc[0,1]\ng.ax_joint.text(0.05, 0.92, f\'r = {r:.3f}\', transform=g.ax_joint.transAxes,\n                fontsize=11, fontweight=\'bold\', color=\'red\')\ng.fig.suptitle(\'Joint Regression Plot with Correlation\', y=1.02)\ng.fig.savefig(\'joint_reg.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved joint_reg.png\')"}
    ],
"rw": {
    "title": "Height-Weight Bivariate Analysis",
    "scenario": "Show the joint distribution of height and weight across gender using JointGrid: central scatter colored by gender, marginal KDEs filled by gender, and a correlation annotation in the joint panel.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(77)\ndf = pd.DataFrame({\n    \'height_cm\': np.concatenate([\n        np.random.normal(165, 7, 200),\n        np.random.normal(178, 8, 200)]),\n    \'weight_kg\': np.concatenate([\n        np.random.normal(62, 9, 200),\n        np.random.normal(78, 11, 200)]),\n    \'gender\': np.repeat([\'Female\',\'Male\'], 200)\n})\n\ng = sns.JointGrid(data=df, x=\'height_cm\', y=\'weight_kg\', height=7)\npalette = {\'Female\':\'#dd8452\',\'Male\':\'#4c72b0\'}\nfor gender, grp in df.groupby(\'gender\'):\n    g.ax_joint.scatter(grp.height_cm, grp.weight_kg,\n                       alpha=0.4, s=20, color=palette[gender], label=gender)\n    sns.kdeplot(data=grp, x=\'height_cm\', ax=g.ax_marg_x,\n                fill=True, alpha=0.4, color=palette[gender], linewidth=1.5)\n    sns.kdeplot(data=grp, y=\'weight_kg\', ax=g.ax_marg_y,\n                fill=True, alpha=0.4, color=palette[gender], linewidth=1.5)\n\ng.ax_joint.legend(title=\'Gender\')\nr = df[[\'height_cm\',\'weight_kg\']].corr().iloc[0,1]\ng.ax_joint.text(0.05,0.92,f\'r = {r:.3f}\',transform=g.ax_joint.transAxes,\n                fontsize=11,fontweight=\'bold\',color=\'darkred\')\ng.ax_joint.set_xlabel(\'Height (cm)\'); g.ax_joint.set_ylabel(\'Weight (kg)\')\ng.fig.suptitle(\'Height-Weight Joint Distribution by Gender\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'height_weight_joint.png\', dpi=150, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved height_weight_joint.png\')"
},
"practice": {
    "title": "Joint Plot Practice",
    "desc": "Load the \'penguins\' dataset. Create a JointGrid for bill_length_mm vs bill_depth_mm: (1) scatter in the joint with hue=species and s=30, (2) boxplot in the marginals (ax_marg_x and ax_marg_y). Drop NaN rows first.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\npenguins = sns.load_dataset(\'penguins\').dropna()\n\ng = sns.JointGrid(data=penguins, x=\'bill_length_mm\', y=\'bill_depth_mm\', height=6)\n# TODO: scatterplot joint with hue=species, s=30\n# TODO: boxplot marginals for x and y\n# TODO: legend, labels, title\n# TODO: save \'penguin_joint.png\'"
}
},

{
"title": "22. catplot — Figure-Level Categorical",
"desc": "Use catplot() as a unified interface for all categorical plots. Control kind=\'strip\'|\'swarm\'|\'box\'|\'violin\'|\'bar\'|\'count\'|\'point\' and use col/row to create FacetGrid-powered small multiples.",
"examples": [
        {"label": "catplot with col splitting", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\ng = sns.catplot(data=tips, x=\'day\', y=\'total_bill\',\n                hue=\'sex\', col=\'time\',\n                kind=\'box\', palette=\'Set2\',\n                height=5, aspect=0.85,\n                order=[\'Thur\',\'Fri\',\'Sat\',\'Sun\'])\ng.set_axis_labels(\'Day\', \'Total Bill ($)\')\ng.set_titles(\'{col_name}\')\ng.fig.suptitle(\'Bill by Day, Sex, and Time (catplot col)\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'catplot_col.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved catplot_col.png\')"},
        {"label": "catplot kind=\'violin\' with row and col", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntitanic = sns.load_dataset(\'titanic\')\n\ng = sns.catplot(data=titanic, x=\'class\', y=\'age\',\n                col=\'survived\', hue=\'sex\',\n                kind=\'violin\', split=True, inner=\'quartile\',\n                palette=\'pastel\', height=5, aspect=0.9)\ng.set_axis_labels(\'Class\', \'Age\')\ng.set_titles(col_template=\'Survived: {col_name}\')\ng.fig.suptitle(\'Titanic Age by Class, Gender & Survival\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'catplot_violin.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved catplot_violin.png\')"},
        {"label": "catplot kind=\'count\' and \'bar\'", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\nfig, axes = plt.subplots(1, 2, figsize=(13, 5))\n# Count plot via catplot saved to file; replicate on axes\nsns.countplot(data=tips, x=\'day\', hue=\'sex\', palette=\'Set1\', ax=axes[0])\naxes[0].set_title(\"countplot: Visits by Day\")\n\nsns.barplot(data=tips, x=\'day\', y=\'tip\', hue=\'sex\',\n            palette=\'Set2\', capsize=0.08, ax=axes[1])\naxes[1].set_title(\"barplot: Mean Tip by Day\")\nfor ax in axes:\n    ax.set_xlabel(\'Day\')\nfig.tight_layout()\nfig.savefig(\'catplot_count_bar.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved catplot_count_bar.png\')"},
        {"label": "catplot kind=\'point\' with order control", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntitanic = sns.load_dataset(\'titanic\')\n\ng = sns.catplot(data=titanic, x=\'class\', y=\'survived\',\n                hue=\'sex\', col=\'embarked\',\n                kind=\'point\', dodge=True, capsize=0.1,\n                markers=[\'o\',\'s\'], linestyles=[\'-\',\'--\'],\n                palette=\'Set1\', height=4, aspect=0.85,\n                order=[\'First\',\'Second\',\'Third\'])\ng.set_axis_labels(\'Class\', \'Survival Rate\')\ng.set_titles(col_template=\'Embarked: {col_name}\')\ng.fig.suptitle(\'Survival Rate by Class, Sex & Port\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'catplot_point.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved catplot_point.png\')"}
    ],
"rw": {
    "title": "Product Feedback Dashboard",
    "scenario": "Use catplot to compare NPS scores across 4 product categories and 3 user segments. Show kind=\'box\' with col=category, hue=segment, and a separate catplot kind=\'point\' for mean scores.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(42)\ncategories = [\'Mobile App\',\'Web Platform\',\'API\',\'Support\']\nsegments = [\'Enterprise\',\'SMB\',\'Startup\']\nrows = []\nbases = {\'Mobile App\': 7.0,\'Web Platform\': 6.5,\'API\': 8.0,\'Support\': 5.5}\nseg_offsets = {\'Enterprise\': 0.5,\'SMB\': 0.0,\'Startup\': -0.3}\nfor cat in categories:\n    for seg in segments:\n        mu = bases[cat] + seg_offsets[seg]\n        scores = np.random.normal(mu, 1.5, 40).clip(0, 10)\n        for s in scores:\n            rows.append({\'category\': cat,\'segment\': seg,\'nps\': s})\ndf = pd.DataFrame(rows)\n\ng = sns.catplot(data=df, x=\'segment\', y=\'nps\', col=\'category\',\n                kind=\'box\', hue=\'segment\', palette=\'Set2\',\n                height=4, aspect=0.85, col_wrap=2,\n                order=segments, legend=False)\ng.set_axis_labels(\'Segment\', \'NPS Score\')\ng.set_titles(\'{col_name}\')\ng.fig.suptitle(\'Product NPS by Category & Segment\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'nps_catplot.png\', dpi=150, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved nps_catplot.png\')"
},
"practice": {
    "title": "catplot Practice",
    "desc": "Load the \'exercise\' dataset from seaborn. Use catplot with x=\'time\', y=\'pulse\', hue=\'kind\', col=\'diet\', kind=\'point\'. Then create a second catplot with kind=\'box\'. Add appropriate titles and labels.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nexercise = sns.load_dataset(\'exercise\')\n\n# TODO: catplot pointplot: x=time, y=pulse, hue=kind, col=diet\n# TODO: catplot boxplot: same variables\n# TODO: save \'exercise_catplot.png\'"
}
},

{
"title": "23. displot — Figure-Level Distributions",
"desc": "Use displot() as the figure-level interface for histplot, kdeplot, and ecdfplot. Add col/row faceting for small-multiple distribution comparisons.",
"examples": [
        {"label": "displot: hist, kde, ecdf kinds", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(0)\ndf = pd.DataFrame({\n    \'value\': np.concatenate([np.random.normal(0,1,300), np.random.normal(4,1.5,300)]),\n    \'group\': np.repeat([\'A\',\'B\'], 300)\n})\n\nfor kind in [\'hist\',\'kde\',\'ecdf\']:\n    g = sns.displot(data=df, x=\'value\', hue=\'group\',\n                    kind=kind, height=4, aspect=1.5, palette=\'Set2\',\n                    fill=(kind != \'ecdf\'), alpha=0.5, linewidth=2)\n    g.fig.suptitle(f\"displot kind=\'{kind}\'\", y=1.02)\n    g.fig.savefig(f\'displot_{kind}.png\', dpi=100, bbox_inches=\'tight\')\n    plt.close(g.fig)\nprint(\'Saved displot_hist/kde/ecdf.png\')"},
        {"label": "displot with col faceting", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntitanic = sns.load_dataset(\'titanic\').dropna(subset=[\'age\'])\n\ng = sns.displot(data=titanic, x=\'age\', col=\'class\',\n                hue=\'survived\', kind=\'hist\', stat=\'density\',\n                kde=True, alpha=0.5, palette=\'Set1\',\n                height=4, aspect=0.85, col_order=[\'First\',\'Second\',\'Third\'])\ng.set_axis_labels(\'Age\', \'Density\')\ng.set_titles(col_template=\'{col_name} Class\')\ng.fig.suptitle(\'Age Distribution by Class and Survival\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'displot_col.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved displot_col.png\')"},
        {"label": "displot with row and col", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(1)\nregions = [\'North\',\'South\']\nperiods = [\'Q1\',\'Q2\',\'Q3\',\'Q4\']\nrows = []\nfor region in regions:\n    base = 50 if region == \'North\' else 35\n    for period in periods:\n        offset = periods.index(period) * 5\n        vals = np.random.normal(base + offset, 12, 100)\n        for v in vals:\n            rows.append({\'region\': region, \'period\': period, \'sales\': v})\ndf = pd.DataFrame(rows)\n\ng = sns.displot(data=df, x=\'sales\', row=\'region\', col=\'period\',\n                kind=\'kde\', fill=True, alpha=0.5, palette=\'Set2\',\n                height=3, aspect=1.1, col_order=periods)\ng.set_axis_labels(\'Sales ($K)\', \'Density\')\ng.fig.suptitle(\'Sales Distribution by Region & Quarter\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'displot_grid.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved displot_grid.png\')"},
        {"label": "displot with rug and binwidth", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(2)\ndf = pd.DataFrame({\n    \'latency\': np.concatenate([\n        np.random.lognormal(3, 0.4, 500),\n        np.random.lognormal(4, 0.5, 200),\n    ]),\n    \'endpoint\': np.repeat([\'/fast\',\'/slow\'], [500,200])\n})\n\ng = sns.displot(data=df, x=\'latency\', hue=\'endpoint\',\n                kind=\'hist\', stat=\'density\', kde=True,\n                rug=True, rug_kws=dict(height=0.05, alpha=0.3),\n                log_scale=True, alpha=0.4, palette=\'Set1\',\n                height=5, aspect=1.6, binwidth=0.05)\ng.set_axis_labels(\'Latency (ms, log scale)\', \'Density\')\ng.fig.suptitle(\'Endpoint Latency Distribution with Rug\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'displot_rug.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved displot_rug.png\')"}
    ],
"rw": {
    "title": "Multi-Experiment Distribution Report",
    "scenario": "Use displot to compare test metric distributions across 3 ML experiments and 2 datasets (col=dataset, hue=experiment). Show kind=\'kde\' with fill=True. Then show kind=\'ecdf\' for cumulative comparison.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(88)\nexperiments = [\'Baseline\',\'DropoutReg\',\'AugData\']\ndatasets = [\'CIFAR-10\',\'ImageNet\']\nrows = []\nmeans = {\'Baseline\': (72,80), \'DropoutReg\': (75,83), \'AugData\': (77,85)}\nfor exp, (m1, m2) in means.items():\n    for ds, mu in zip(datasets, [m1, m2]):\n        vals = np.random.normal(mu, 3, 150)\n        for v in vals:\n            rows.append({\'experiment\': exp, \'dataset\': ds, \'accuracy\': v})\ndf = pd.DataFrame(rows)\n\ng = sns.displot(data=df, x=\'accuracy\', hue=\'experiment\', col=\'dataset\',\n                kind=\'kde\', fill=True, alpha=0.4, linewidth=2,\n                palette=\'Set2\', height=4, aspect=1.2, common_norm=False)\ng.set_axis_labels(\'Accuracy (%)\', \'Density\')\ng.set_titles(col_template=\'{col_name}\')\ng.fig.suptitle(\'Model Accuracy Distribution by Experiment & Dataset\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'experiment_displot.png\', dpi=150, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved experiment_displot.png\')"
},
"practice": {
    "title": "displot Practice",
    "desc": "Load the \'penguins\' dataset. Use displot to create: (1) hist kind with col=species, x=body_mass_g, hue=sex — set kde=True, (2) ecdf kind with same grouping on a new figure. Save both as separate PNGs.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\npenguins = sns.load_dataset(\'penguins\').dropna()\n\n# TODO: displot hist kind, col=species, x=body_mass_g, hue=sex, kde=True\n# TODO: save \'penguin_hist.png\'\n# TODO: displot ecdf kind, same grouping\n# TODO: save \'penguin_ecdf.png\'"
}
},

{
"title": "24. relplot — Figure-Level Relational",
"desc": "Use relplot() as the figure-level interface for scatterplot and lineplot. Use col, row, and hue to create multi-panel relational grids with consistent scaling.",
"examples": [
        {"label": "relplot scatter with col and hue", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\ng = sns.relplot(data=tips, x=\'total_bill\', y=\'tip\',\n                hue=\'sex\', col=\'time\', style=\'sex\',\n                palette=\'Set1\', s=60, alpha=0.7,\n                height=4, aspect=1.0)\ng.set_axis_labels(\'Total Bill ($)\', \'Tip ($)\')\ng.set_titles(col_template=\'{col_name}\')\ng.fig.suptitle(\'Tips: Scatter by Time and Sex (relplot)\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'relplot_scatter.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved relplot_scatter.png\')"},
        {"label": "relplot lineplot with col_wrap", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'darkgrid\')\nnp.random.seed(0)\nsubjects = [f\'Subject_{i:02d}\' for i in range(1, 7)]\ndf_list = []\nfor subj in subjects:\n    t = np.arange(20)\n    y = np.sin(t*0.3 + np.random.uniform(0,3)) + np.random.randn(20)*0.2\n    df_list.append(pd.DataFrame({\'time\':t,\'value\':y,\'subject\':subj}))\ndf = pd.concat(df_list, ignore_index=True)\n\ng = sns.relplot(data=df, x=\'time\', y=\'value\', col=\'subject\',\n                kind=\'line\', col_wrap=3, palette=\'tab10\',\n                height=3, aspect=1.3, linewidth=2)\ng.set_axis_labels(\'Time\', \'Signal\')\ng.set_titles(col_template=\'{col_name}\')\ng.fig.suptitle(\'Subject Time Series (relplot col_wrap=3)\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'relplot_line.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved relplot_line.png\')"},
        {"label": "relplot with size and style encoding", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(1)\nn = 200\ndf = pd.DataFrame({\n    \'x\': np.random.randn(n),\n    \'y\': np.random.randn(n),\n    \'size_var\': np.random.uniform(50, 300, n),\n    \'category\': np.random.choice([\'A\',\'B\',\'C\'], n),\n    \'quality\': np.random.choice([\'High\',\'Low\'], n)\n})\n\ng = sns.relplot(data=df, x=\'x\', y=\'y\',\n                hue=\'category\', size=\'size_var\', style=\'quality\',\n                palette=\'Set2\', sizes=(20, 300), alpha=0.7,\n                height=5, aspect=1.2)\ng.ax.set_title(\'Multi-Encoding Scatter: hue + size + style\', fontweight=\'bold\')\ng.fig.savefig(\'relplot_multi.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved relplot_multi.png\')"},
        {"label": "relplot row and col grid", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(2)\nconditions = [\'Fast\',\'Slow\']\ngroups = [\'Treatment\',\'Control\']\nrows = []\nfor cond in conditions:\n    for grp in groups:\n        mu = (4 if grp==\'Treatment\' else 2) + (1 if cond==\'Fast\' else 0)\n        t = np.arange(30)\n        y = mu + np.cumsum(np.random.randn(30)*0.3) + np.sin(t*0.2)\n        df_part = pd.DataFrame({\'time\':t,\'signal\':y,\n                                 \'condition\':cond,\'group\':grp})\n        rows.append(df_part)\ndf = pd.concat(rows, ignore_index=True)\n\ng = sns.relplot(data=df, x=\'time\', y=\'signal\',\n                row=\'group\', col=\'condition\',\n                kind=\'line\', palette=\'Set1\', hue=\'group\',\n                height=3.5, aspect=1.2, linewidth=2)\ng.set_axis_labels(\'Time\', \'Signal\')\ng.set_titles(row_template=\'{row_name}\', col_template=\'{col_name}\')\ng.fig.suptitle(\'Signal by Group × Condition (relplot grid)\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'relplot_grid.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved relplot_grid.png\')"}
    ],
"rw": {
    "title": "Marketing Campaign Performance",
    "scenario": "Plot click-through rate vs spend for 4 campaign types across 3 channels (col=channel). Use relplot kind=\'scatter\', size=impressions (scaled), hue=campaign_type. Add a regression line for each panel.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(66)\nchannels = [\'Search\',\'Social\',\'Display\']\ncampaigns = [\'Brand\',\'Retargeting\',\'Prospecting\',\'Seasonal\']\nrows = []\nfor ch in channels:\n    for camp in campaigns:\n        n = 40\n        spend = np.random.uniform(500, 5000, n)\n        ctr   = 0.02 + spend/100000 + np.random.randn(n)*0.005\n        ctr   = np.clip(ctr, 0.001, 0.15)\n        impr  = spend * np.random.uniform(100, 500, n)\n        for s, c, im in zip(spend, ctr, impr):\n            rows.append({\'channel\':ch,\'campaign\':camp,\'spend\':s,\'ctr\':c,\'impressions\':im})\ndf = pd.DataFrame(rows)\n\ng = sns.relplot(data=df, x=\'spend\', y=\'ctr\',\n                col=\'channel\', hue=\'campaign\', style=\'campaign\',\n                size=\'impressions\', sizes=(20, 200),\n                palette=\'tab10\', alpha=0.7, height=4, aspect=1.1)\n# Overlay regression line for each axis\nfor ax in g.axes.flat:\n    if ax is not None:\n        ch_data = df[df.channel == ax.get_title().strip()]\n        if len(ch_data):\n            m, b = np.polyfit(ch_data.spend, ch_data.ctr, 1)\n            x_line = np.linspace(ch_data.spend.min(), ch_data.spend.max(), 50)\n            ax.plot(x_line, m*x_line+b, \'r--\', linewidth=1.5, alpha=0.8)\ng.set_axis_labels(\'Spend ($)\', \'CTR\')\ng.set_titles(col_template=\'{col_name}\')\ng.fig.suptitle(\'Campaign CTR vs Spend by Channel\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'campaign_relplot.png\', dpi=150, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved campaign_relplot.png\')"
},
"practice": {
    "title": "relplot Practice",
    "desc": "Load the \'fmri\' dataset. Use relplot with kind=\'line\', x=\'timepoint\', y=\'signal\', hue=\'event\', col=\'region\'. Then create a second relplot kind=\'scatter\' with the same groupings and size=0.5. Save both.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'darkgrid\')\nfmri = sns.load_dataset(\'fmri\')\n\n# TODO: relplot line, x=timepoint, y=signal, hue=event, col=region\n# TODO: save \'fmri_line.png\'\n# TODO: relplot scatter, same grouping\n# TODO: save \'fmri_scatter.png\'"
}
},

{
"title": "25. Heatmap Advanced",
"desc": "Go beyond basic heatmaps: annotate with custom formats, apply diverging colormaps for signed values, mask upper triangles, and combine with matplotlib for multi-panel layouts.",
"examples": [
        {"label": "Masked upper-triangle correlation heatmap", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(0)\nn = 8\nlabels = [f\'Var_{i}\' for i in range(1, n+1)]\ndata = np.random.randn(200, n)\nfor i in range(n):\n    for j in range(i):\n        data[:, j] += data[:, i] * np.random.uniform(-0.5, 0.8)\ncorr = np.corrcoef(data.T)\ndf_corr = pd.DataFrame(corr, index=labels, columns=labels)\n\nmask = np.triu(np.ones_like(corr, dtype=bool), k=1)  # mask upper\n\nfig, ax = plt.subplots(figsize=(8, 7))\nsns.heatmap(df_corr, mask=mask, cmap=\'RdBu_r\', vmin=-1, vmax=1,\n            annot=True, fmt=\'.2f\', linewidths=0.5,\n            ax=ax, square=True, cbar_kws={\'label\': \'Pearson r\'})\nax.set_title(\'Lower-Triangle Correlation Matrix\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'corr_heatmap.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved corr_heatmap.png\')"},
        {"label": "Heatmap with custom fmt and colorbar", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(1)\ndays = [\'Mon\',\'Tue\',\'Wed\',\'Thu\',\'Fri\',\'Sat\',\'Sun\']\nhours = [f\'{h:02d}:00\' for h in range(7, 23)]\ntraffic = np.random.poisson(50, (len(hours), len(days)))\ntraffic[:, 5:] = np.random.poisson(80, (len(hours), 2))\ntraffic[8:12, :] += 30\ntraffic[17:20, :] += 40\n\ndf = pd.DataFrame(traffic, index=hours, columns=days)\nfig, ax = plt.subplots(figsize=(10, 7))\nsns.heatmap(df, cmap=\'YlOrRd\', annot=True, fmt=\'d\',\n            linewidths=0.3, ax=ax,\n            cbar_kws={\'label\': \'Page Views\', \'shrink\': 0.8})\nax.set_title(\'Website Traffic by Hour & Day\', fontweight=\'bold\')\nax.set_xlabel(\'Day of Week\'); ax.set_ylabel(\'Hour\')\nfig.tight_layout()\nfig.savefig(\'traffic_heatmap.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved traffic_heatmap.png\')"},
        {"label": "Heatmap with custom annotation text", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(2)\nmodels = [\'LR\',\'RF\',\'XGB\',\'SVM\',\'NN\']\nmetrics = [\'Accuracy\',\'Precision\',\'Recall\',\'F1\',\'AUC\']\nvalues = np.random.uniform(0.70, 0.98, (len(models), len(metrics)))\ndf = pd.DataFrame(values, index=models, columns=metrics)\n\n# Custom annotations: highlight best per metric\nannot = df.copy().applymap(lambda v: f\'{v:.3f}\')\nbest_rows = df.idxmax(axis=0)\nhighlights = pd.DataFrame(\'\', index=df.index, columns=df.columns)\nfor metric in metrics:\n    highlights.loc[best_rows[metric], metric] = f\'★{df.loc[best_rows[metric],metric]:.3f}\'\n\nfig, ax = plt.subplots(figsize=(9, 5))\nsns.heatmap(df, cmap=\'Blues\', vmin=0.65, vmax=1.0, ax=ax,\n            annot=df.round(3), fmt=\'\', linewidths=0.5)\nax.set_title(\'Model Comparison Heatmap (★ = best per metric)\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'model_heatmap.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved model_heatmap.png\')"},
        {"label": "Diverging heatmap for signed changes", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(3)\nproducts = [f\'P{i:02d}\' for i in range(1, 9)]\nkpis = [\'Revenue\',\'Margin\',\'Units\',\'Traffic\',\'Conv%\',\'Retention\']\nchanges = np.random.randn(len(products), len(kpis)) * 15\ndf = pd.DataFrame(changes, index=products, columns=kpis)\n\nfig, ax = plt.subplots(figsize=(9, 6))\nsns.heatmap(df, cmap=\'RdYlGn\', center=0,\n            annot=True, fmt=\'.1f\', linewidths=0.5, ax=ax,\n            cbar_kws={\'label\': \'YoY Change (%)\'})\nax.set_title(\'Product KPI Year-over-Year Change (%)\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'diverging_heatmap.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved diverging_heatmap.png\')"}
    ],
"rw": {
    "title": "Confusion Matrix Dashboard",
    "scenario": "Create a styled confusion matrix heatmap for a 5-class classifier. Normalize by true class (row), show counts in top-left and percentages in bottom-right of each cell, use Blues cmap.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(42)\nclasses = [\'Cat\',\'Dog\',\'Bird\',\'Fish\',\'Horse\']\nn = 5\ncm = np.array([\n    [45, 3, 1, 0, 1],\n    [2, 48, 0, 1, 0],\n    [1, 0, 42, 3, 2],\n    [0, 1, 4, 44, 1],\n    [2, 0, 3, 1, 43]\n])\ncm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)\n\n# Build annotation: count + pct\nannot = np.empty_like(cm, dtype=object)\nfor i in range(n):\n    for j in range(n):\n        annot[i,j] = f\'{cm[i,j]}\n{cm_norm[i,j]*100:.1f}%\'\n\nfig, ax = plt.subplots(figsize=(8, 7))\nsns.heatmap(cm_norm, annot=annot, fmt=\'\', cmap=\'Blues\',\n            xticklabels=classes, yticklabels=classes,\n            vmin=0, vmax=1, linewidths=0.5, ax=ax,\n            cbar_kws={\'label\': \'Precision (row-normalized)\'})\nax.set_title(\'5-Class Confusion Matrix\', fontweight=\'bold\', fontsize=13)\nax.set_xlabel(\'Predicted\'); ax.set_ylabel(\'True\')\nfig.tight_layout()\nfig.savefig(\'confusion_matrix.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved confusion_matrix.png\')"
},
"practice": {
    "title": "Heatmap Practice",
    "desc": "Generate a 10x6 DataFrame of monthly sales by region (random integers 100-500). Create: (1) a standard heatmap with annot=True and YlGn cmap, (2) the same data as a diverging heatmap centered on the mean (RdYlGn), side by side in a 1x2 figure.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(9)\nmonths = [\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\',\'Jul\',\'Aug\',\'Sep\',\'Oct\',\'Nov\',\'Dec\'][:10]\nregions = [\'North\',\'South\',\'East\',\'West\',\'Central\',\'Pacific\']\ndf = pd.DataFrame(np.random.randint(100,500,(10,6)), index=months, columns=regions)\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))\n# TODO: standard heatmap YlGn on ax1, annot=True\n# TODO: diverging heatmap RdYlGn centered at mean on ax2\n# TODO: titles, tight_layout, save \'sales_heatmap.png\'\nplt.close()"
}
},

{
"title": "26. PairGrid Advanced",
"desc": "Use PairGrid for full control over diagonal, upper, and lower triangle plots. Map different plot types per region and use hue for group-aware multi-variable comparison.",
"examples": [
        {"label": "PairGrid: hist diagonal, scatter off-diag", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\niris = sns.load_dataset(\'iris\')\n\ng = sns.PairGrid(iris, hue=\'species\', palette=\'Set2\',\n                 vars=[\'sepal_length\',\'sepal_width\',\'petal_length\',\'petal_width\'])\ng.map_diag(sns.histplot, kde=True, alpha=0.6)\ng.map_offdiag(sns.scatterplot, s=25, alpha=0.6)\ng.add_legend(title=\'Species\')\ng.fig.suptitle(\'PairGrid: Histogram Diagonal + Scatter\', y=1.01, fontweight=\'bold\')\ng.fig.savefig(\'pairgrid_hist.png\', dpi=100, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved pairgrid_hist.png\')"},
        {"label": "PairGrid: KDE diagonal, upper KDE, lower scatter", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\niris = sns.load_dataset(\'iris\')\nvars_ = [\'sepal_length\',\'sepal_width\',\'petal_length\',\'petal_width\']\n\ng = sns.PairGrid(iris, hue=\'species\', palette=\'Set1\', vars=vars_)\ng.map_diag(sns.kdeplot, fill=True, alpha=0.4, linewidth=1.5)\ng.map_upper(sns.kdeplot, levels=4, warn_singular=False)\ng.map_lower(sns.scatterplot, s=20, alpha=0.5)\ng.add_legend(title=\'Species\', fontsize=9)\ng.fig.suptitle(\'PairGrid: KDE + Scatter Split\', y=1.01, fontweight=\'bold\')\ng.fig.savefig(\'pairgrid_split.png\', dpi=100, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved pairgrid_split.png\')"},
        {"label": "PairGrid: boxplot on diagonal", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\niris = sns.load_dataset(\'iris\')\nvars_ = [\'sepal_length\',\'petal_length\',\'petal_width\']\n\ng = sns.PairGrid(iris, hue=\'species\', palette=\'Set2\', vars=vars_)\n\ndef diag_box(x, **kwargs):\n    ax = plt.gca()\n    data = kwargs.get(\'data\', x)\n    groups = x.groupby(level=0) if hasattr(x,\'groupby\') else None\n    ax.boxplot([x[x.index == i] for i in x.unique()], vert=True)\n\ng.map_diag(sns.kdeplot, fill=True, alpha=0.5)\ng.map_upper(sns.scatterplot, s=20, alpha=0.5)\ng.map_lower(sns.regplot, scatter_kws=dict(s=10,alpha=0.4),\n            line_kws=dict(linewidth=1.5))\ng.add_legend()\ng.fig.suptitle(\'PairGrid: KDE / Scatter / Regression\', y=1.01, fontweight=\'bold\')\ng.fig.savefig(\'pairgrid_reg.png\', dpi=100, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved pairgrid_reg.png\')"},
        {"label": "PairGrid with correlation annotation", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(0)\nn = 150\ndf = pd.DataFrame({\n    \'A\': np.random.randn(n),\n    \'B\': np.random.randn(n),\n    \'C\': np.random.randn(n),\n    \'group\': np.random.choice([\'X\',\'Y\'], n)\n})\ndf[\'B\'] += df[\'A\'] * 0.7\ndf[\'C\'] = df[\'A\'] * (-0.5) + np.random.randn(n) * 0.7\n\ndef corrfunc(x, y, **kwargs):\n    r = np.corrcoef(x, y)[0,1]\n    ax = plt.gca()\n    ax.annotate(f\'r = {r:.2f}\', xy=(0.5,0.5), xycoords=\'axes fraction\',\n                ha=\'center\', va=\'center\', fontsize=12,\n                color=\'darkred\' if abs(r) > 0.4 else \'gray\',\n                fontweight=\'bold\' if abs(r) > 0.4 else \'normal\')\n\ng = sns.PairGrid(df[[\'A\',\'B\',\'C\',\'group\']], hue=\'group\', palette=\'Set1\',\n                 vars=[\'A\',\'B\',\'C\'])\ng.map_diag(sns.kdeplot, fill=True, alpha=0.4)\ng.map_lower(sns.scatterplot, s=20, alpha=0.5)\ng.map_upper(corrfunc)\ng.add_legend()\ng.fig.suptitle(\'PairGrid: Lower=Scatter, Upper=Correlation\', y=1.01, fontweight=\'bold\')\ng.fig.savefig(\'pairgrid_corr.png\', dpi=100, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved pairgrid_corr.png\')"}
    ],
"rw": {
    "title": "Penguins Multi-Variable EDA",
    "scenario": "Create a PairGrid on the penguins dataset (4 numeric features, hue=species): diagonal = KDE filled, upper = KDE contour, lower = scatter. Annotate correlation values in each upper cell.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\npenguins = sns.load_dataset(\'penguins\').dropna()\nvars_ = [\'bill_length_mm\',\'bill_depth_mm\',\'flipper_length_mm\',\'body_mass_g\']\n\ndef upper_corr(x, y, **kwargs):\n    r = np.corrcoef(x, y)[0,1]\n    ax = plt.gca()\n    ax.annotate(f\'r={r:.2f}\', xy=(0.5,0.5), xycoords=\'axes fraction\',\n                ha=\'center\', va=\'center\', fontsize=10,\n                color=\'darkred\' if abs(r) > 0.5 else \'gray\',\n                fontweight=\'bold\')\n\ng = sns.PairGrid(penguins, hue=\'species\', palette=\'Set2\', vars=vars_)\ng.map_diag(sns.kdeplot, fill=True, alpha=0.5, linewidth=1.5)\ng.map_lower(sns.scatterplot, s=20, alpha=0.5)\ng.map_upper(upper_corr)\ng.add_legend(title=\'Species\')\ng.fig.suptitle(\'Penguins PairGrid EDA\', y=1.01, fontweight=\'bold\')\ng.fig.savefig(\'penguins_pairgrid.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved penguins_pairgrid.png\')"
},
"practice": {
    "title": "PairGrid Practice",
    "desc": "Load the \'mpg\' dataset. Create a PairGrid with vars=[\'mpg\',\'horsepower\',\'weight\',\'acceleration\'], hue=\'origin\'. Map: diagonal=histplot, upper=scatterplot, lower=regplot. Add legend and a suptitle.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nmpg = sns.load_dataset(\'mpg\').dropna()\nvars_ = [\'mpg\',\'horsepower\',\'weight\',\'acceleration\']\n\ng = sns.PairGrid(mpg, hue=\'origin\', palette=\'tab10\', vars=vars_)\n# TODO: map_diag histplot\n# TODO: map_upper scatterplot\n# TODO: map_lower regplot (scatter_kws, line_kws)\n# TODO: add_legend, suptitle\n# TODO: save \'mpg_pairgrid.png\'"
}
},

{
"title": "27. Residual & Regression Diagnostics",
"desc": "Use residplot() for visual residual checks, lmplot() for grouped regression, and regplot() with custom order for polynomial fits. Combine with matplotlib for full diagnostic panels.",
"examples": [
        {"label": "residplot: detect non-linearity", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(0)\nn = 150\nx = np.linspace(0, 10, n)\ny_linear  = 2*x + 1 + np.random.randn(n)*2\ny_nonlin  = 2*x + 0.3*x**2 + np.random.randn(n)*3\n\ndf = pd.DataFrame({\'x\':x,\'y_linear\':y_linear,\'y_nonlin\':y_nonlin})\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))\nsns.residplot(data=df, x=\'x\', y=\'y_linear\', lowess=True,\n              scatter_kws=dict(alpha=0.5, s=20),\n              line_kws=dict(color=\'red\', linewidth=2), ax=ax1)\nax1.set_title(\'Residuals: Linear Data (good fit)\')\nax1.axhline(0, color=\'gray\', linestyle=\'--\', linewidth=1)\n\nsns.residplot(data=df, x=\'x\', y=\'y_nonlin\', lowess=True,\n              scatter_kws=dict(alpha=0.5, s=20),\n              line_kws=dict(color=\'red\', linewidth=2), ax=ax2)\nax2.set_title(\'Residuals: Nonlinear Data (pattern visible)\')\nax2.axhline(0, color=\'gray\', linestyle=\'--\', linewidth=1)\n\nfig.suptitle(\'residplot — Lowess Smoother\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'residplot.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved residplot.png\')"},
        {"label": "lmplot: grouped regression per hue", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\ng = sns.lmplot(data=tips, x=\'total_bill\', y=\'tip\',\n               hue=\'sex\', palette=\'Set1\',\n               scatter_kws=dict(s=30, alpha=0.6),\n               line_kws=dict(linewidth=2),\n               height=5, aspect=1.3)\ng.set_axis_labels(\'Total Bill ($)\', \'Tip ($)\')\ng.fig.suptitle(\'lmplot: Regression by Sex\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'lmplot_hue.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved lmplot_hue.png\')"},
        {"label": "lmplot with col faceting", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\ng = sns.lmplot(data=tips, x=\'total_bill\', y=\'tip\',\n               col=\'time\', hue=\'smoker\',\n               palette=\'Set2\',\n               scatter_kws=dict(s=30, alpha=0.6),\n               height=4, aspect=1.1)\ng.set_axis_labels(\'Total Bill ($)\', \'Tip ($)\')\ng.set_titles(col_template=\'{col_name}\')\ng.fig.suptitle(\'lmplot: Regression by Time and Smoker\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'lmplot_col.png\', dpi=120, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved lmplot_col.png\')"},
        {"label": "Polynomial regression with regplot order", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(1)\nx = np.linspace(-3, 3, 100)\ny = 2*x**3 - x**2 + x + np.random.randn(100)*3\ndf = pd.DataFrame({\'x\':x,\'y\':y})\n\nfig, axes = plt.subplots(1, 3, figsize=(13, 4))\nfor ax, order, title in zip(axes, [1,2,3], [\'Linear (order=1)\',\'Quadratic (order=2)\',\'Cubic (order=3)\']):\n    sns.regplot(data=df, x=\'x\', y=\'y\', order=order,\n                scatter_kws=dict(s=15, alpha=0.5),\n                line_kws=dict(linewidth=2, color=\'tomato\'),\n                ax=ax)\n    ax.set_title(title)\n    ax.grid(True, alpha=0.3)\nfig.suptitle(\'Polynomial Regression Orders with regplot\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'poly_regplot.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved poly_regplot.png\')"}
    ],
"rw": {
    "title": "Housing Price Regression Diagnostics",
    "scenario": "Fit a linear regression of house price on size and show: (1) lmplot by neighborhood, (2) residplot of residuals, (3) regplot with CI band.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(33)\nhoods = [\'Downtown\',\'Suburbs\',\'Rural\']\nrows = []\nfor hood in hoods:\n    base = {\'Downtown\':300,\'Suburbs\':200,\'Rural\':120}[hood]\n    n = 80\n    size = np.random.uniform(50, 250, n)\n    price = base + 1.2*size + np.random.randn(n)*30\n    rows.append(pd.DataFrame({\'size_sqm\':size,\'price_k\':price,\'neighborhood\':hood}))\ndf = pd.concat(rows, ignore_index=True)\n\ng = sns.lmplot(data=df, x=\'size_sqm\', y=\'price_k\', col=\'neighborhood\',\n               hue=\'neighborhood\', palette=\'Set2\',\n               scatter_kws=dict(s=25, alpha=0.6),\n               line_kws=dict(linewidth=2),\n               height=4, aspect=1.0, legend=False)\ng.set_axis_labels(\'Size (sqm)\', \'Price ($K)\')\ng.set_titles(col_template=\'{col_name}\')\ng.fig.suptitle(\'Housing Price Regression by Neighborhood\', y=1.02, fontweight=\'bold\')\ng.fig.savefig(\'housing_regression.png\', dpi=150, bbox_inches=\'tight\')\nplt.close(g.fig)\nprint(\'Saved housing_regression.png\')"
},
"practice": {
    "title": "Regression Diagnostics Practice",
    "desc": "Generate 100 data points: x = linspace(0,10), y = sin(x) + noise. Use a 1x3 panel: (1) regplot order=1, (2) regplot order=3, (3) residplot for the order=3 fit. Use whitegrid style.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(4)\nx = np.linspace(0, 10, 100)\ny = np.sin(x) + np.random.randn(100)*0.4\ndf = pd.DataFrame({\'x\':x,\'y\':y})\n\nfig, axes = plt.subplots(1, 3, figsize=(14, 4))\n# TODO: regplot order=1 on axes[0]\n# TODO: regplot order=3 on axes[1]\n# TODO: residplot order=3 on axes[2]\nfig.suptitle(\'Regression & Residuals: sin(x)\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'sin_regression.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved sin_regression.png\')"
}
},

{
"title": "28. Mixed Seaborn + Matplotlib",
"desc": "Combine Seaborn plots with raw matplotlib artists: add reference lines, spans, custom patches, secondary axes, and annotations on top of seaborn outputs.",
"examples": [
        {"label": "Add reference line and span to seaborn plot", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(0)\ndf = pd.DataFrame({\n    \'score\': np.random.normal(72, 15, 200),\n    \'group\': np.random.choice([\'A\',\'B\',\'C\',\'D\'], 200)\n})\n\nfig, ax = plt.subplots(figsize=(9, 5))\nsns.boxplot(data=df, x=\'group\', y=\'score\', palette=\'Set2\', ax=ax)\n\n# Matplotlib overlays\nax.axhline(70, color=\'red\', linestyle=\'--\', linewidth=2, label=\'Target\')\nax.axhspan(0, 60, color=\'red\', alpha=0.07, label=\'Fail zone\')\nax.axhspan(90, 100, color=\'green\', alpha=0.07, label=\'Excellent\')\nax.set_title(\'Test Scores by Group with Reference Lines\', fontweight=\'bold\')\nax.legend()\nax.set_ylim(20, 110)\nfig.tight_layout()\nfig.savefig(\'sns_mpl_lines.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved sns_mpl_lines.png\')"},
        {"label": "Annotate outliers on seaborn plot", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(1)\ndf = pd.DataFrame({\n    \'revenue\': np.concatenate([np.random.normal(100, 20, 95), [220, 230, 240, 10, 5]]),\n    \'region\': np.random.choice([\'East\',\'West\'], 100)\n})\n\nfig, ax = plt.subplots(figsize=(9, 5))\nsns.stripplot(data=df, x=\'region\', y=\'revenue\', jitter=True,\n              palette=\'Set2\', size=6, alpha=0.7, ax=ax)\n\n# Annotate extreme outliers\nq1, q3 = df.revenue.quantile([0.25, 0.75])\niqr = q3 - q1\noutliers = df[df.revenue > q3 + 1.5*iqr]\nfor _, row in outliers.iterrows():\n    x_jit = {\'East\':0,\'West\':1}[row.region] + np.random.uniform(-0.1,0.1)\n    ax.annotate(f\'${row.revenue:.0f}K\',\n                xy=(x_jit, row.revenue),\n                xytext=(x_jit+0.2, row.revenue),\n                fontsize=8, color=\'darkred\',\n                arrowprops=dict(arrowstyle=\'->\', color=\'darkred\', lw=1))\n\nax.axhline(q3+1.5*iqr, color=\'red\', linestyle=\'--\', linewidth=1.2, label=\'Upper fence\')\nax.set_title(\'Revenue Distribution with Outlier Annotations\', fontweight=\'bold\')\nax.legend()\nfig.tight_layout()\nfig.savefig(\'sns_annotate_outliers.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved sns_annotate_outliers.png\')"},
        {"label": "seaborn heatmap + matplotlib patch overlay", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nimport matplotlib.patches as mpatches\n\nsns.set_theme(style=\'white\')\nnp.random.seed(2)\ndata = np.random.randn(8, 8)\ndata[2:4, 5:7] += 3  # hot cluster\n\nfig, ax = plt.subplots(figsize=(7, 6))\nsns.heatmap(data, cmap=\'RdBu_r\', center=0, ax=ax,\n            annot=True, fmt=\'.1f\', linewidths=0.3)\n\n# Highlight cluster with rectangle\nrect = mpatches.Rectangle((5, 2), 2, 2,\n    linewidth=3, edgecolor=\'gold\', facecolor=\'none\',\n    transform=ax.transData)\nax.add_patch(rect)\nax.text(6.5, 1.7, \'Hot cluster\', ha=\'center\', fontsize=10,\n        color=\'gold\', fontweight=\'bold\')\nax.set_title(\'Heatmap with Cluster Highlight\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'sns_heatmap_patch.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved sns_heatmap_patch.png\')"},
        {"label": "twinx on seaborn axes", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(3)\nmonths = list(range(1, 13))\ndf = pd.DataFrame({\n    \'month\': months,\n    \'revenue\': [80+i*5+np.random.randn()*4 for i in range(12)],\n    \'users\': [1000+i*80+np.random.randn()*50 for i in range(12)]\n})\n\nfig, ax1 = plt.subplots(figsize=(10, 5))\nax2 = ax1.twinx()\n\nsns.lineplot(data=df, x=\'month\', y=\'revenue\', color=\'steelblue\',\n             linewidth=2, marker=\'o\', label=\'Revenue ($K)\', ax=ax1)\nsns.lineplot(data=df, x=\'month\', y=\'users\', color=\'tomato\',\n             linewidth=2, marker=\'s\', linestyle=\'--\', label=\'Users\', ax=ax2)\n\nax1.set_ylabel(\'Revenue ($K)\', color=\'steelblue\')\nax2.set_ylabel(\'Users\', color=\'tomato\')\nax1.tick_params(axis=\'y\', labelcolor=\'steelblue\')\nax2.tick_params(axis=\'y\', labelcolor=\'tomato\')\nax1.set_xlabel(\'Month\')\n\nlines1, lab1 = ax1.get_legend_handles_labels()\nlines2, lab2 = ax2.get_legend_handles_labels()\nax1.legend(lines1+lines2, lab1+lab2, loc=\'upper left\')\nax1.get_legend().remove() if ax2.get_legend() else None\nax1.set_title(\'Revenue & Users (seaborn + twinx)\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'sns_twinx.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved sns_twinx.png\')"}
    ],
"rw": {
    "title": "Marketing KPI Report",
    "scenario": "Combine a seaborn barplot for monthly revenue with twinx for conversion rate, axhspan for target zones, and annotate bars that exceed the target with a star marker.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(88)\nmonths = [\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\',\'Jul\',\'Aug\',\'Sep\',\'Oct\',\'Nov\',\'Dec\']\nrevenue = [120+i*8+np.random.randn()*10 for i in range(12)]\nconv_rate = [3.2+i*0.1+np.random.randn()*0.2 for i in range(12)]\ntarget_rev = 160\n\ndf = pd.DataFrame({\'month\':months,\'revenue\':revenue,\'conv_rate\':conv_rate})\n\nfig, ax1 = plt.subplots(figsize=(12, 6))\nax2 = ax1.twinx()\n\nbar_colors = [\'seagreen\' if r >= target_rev else \'steelblue\' for r in revenue]\nbars = ax1.bar(months, revenue, color=bar_colors, alpha=0.7, width=0.6)\nax2.plot(months, conv_rate, \'ro-\', linewidth=2, markersize=6, label=\'Conv Rate (%)\')\n\nax1.axhline(target_rev, color=\'green\', linestyle=\'--\', linewidth=2, label=\'Revenue target\')\nax1.axhspan(target_rev, max(revenue)*1.05, color=\'green\', alpha=0.05)\n\n# Annotate exceeding months\nfor i,(m,r) in enumerate(zip(months,revenue)):\n    if r >= target_rev:\n        ax1.text(i, r+3, \'★\', ha=\'center\', fontsize=14, color=\'gold\')\n\nax1.set_ylabel(\'Revenue ($K)\', color=\'steelblue\')\nax2.set_ylabel(\'Conversion Rate (%)\', color=\'tomato\')\nax1.tick_params(axis=\'y\', labelcolor=\'steelblue\')\nax2.tick_params(axis=\'y\', labelcolor=\'tomato\')\nlines1, lab1 = ax1.get_legend_handles_labels()\nlines2, lab2 = ax2.get_legend_handles_labels()\nax1.legend(lines1+lines2, lab1+lab2, loc=\'upper left\')\nax1.set_title(\'Marketing KPI: Revenue vs Conversion Rate\', fontweight=\'bold\', fontsize=13)\nfig.tight_layout()\nfig.savefig(\'marketing_kpi.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved marketing_kpi.png\')"
},
"practice": {
    "title": "Mixed Plot Practice",
    "desc": "Create a seaborn violinplot of exam scores by subject (4 subjects). Overlay a horizontal line at the passing grade (60), a shaded band for distinction (85-100), and annotate the subject with highest median. Use whitegrid style.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(5)\nsubjects = [\'Math\',\'Science\',\'English\',\'History\']\ndf = pd.DataFrame({\n    \'score\': np.concatenate([np.random.normal(m, 15, 80) for m in [65,70,75,60]]).clip(0,100),\n    \'subject\': np.repeat(subjects, 80)\n})\n\nfig, ax = plt.subplots(figsize=(9, 5))\n# TODO: violinplot\n# TODO: axhline at 60 (passing)\n# TODO: axhspan 85-100 (distinction zone)\n# TODO: annotate highest median subject\n# TODO: save \'exam_violin.png\'\nplt.close()"
}
},

{
"title": "29. Seaborn with Real Datasets",
"desc": "Practice EDA workflows on seaborn\'s built-in datasets: titanic, penguins, diamonds, mpg, and fmri. Apply multiple plot types to reveal patterns, relationships, and anomalies.",
"examples": [
        {"label": "Titanic survival EDA", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ntitanic = sns.load_dataset(\'titanic\')\n\nfig, axes = plt.subplots(2, 2, figsize=(12, 9))\n# Survival by class\nsns.barplot(data=titanic, x=\'class\', y=\'survived\', hue=\'sex\',\n            palette=\'Set1\', capsize=0.08, ax=axes[0,0])\naxes[0,0].set_title(\'Survival Rate by Class & Sex\')\naxes[0,0].set_ylim(0,1)\n\n# Age distribution by survival\nsns.kdeplot(data=titanic.dropna(subset=[\'age\']), x=\'age\', hue=\'survived\',\n            fill=True, alpha=0.4, palette=\'Set2\', ax=axes[0,1])\naxes[0,1].set_title(\'Age Distribution by Survival\')\n\n# Fare vs survival (box)\nsns.boxplot(data=titanic, x=\'class\', y=\'fare\', hue=\'survived\',\n            palette=\'pastel\', ax=axes[1,0])\naxes[1,0].set_title(\'Fare Distribution by Class & Survival\')\n\n# Count by embarkation port\nsns.countplot(data=titanic, x=\'embarked\', hue=\'survived\',\n              palette=\'Set2\', ax=axes[1,1])\naxes[1,1].set_title(\'Counts by Port of Embarkation\')\n\nfig.suptitle(\'Titanic Dataset — EDA Dashboard\', fontweight=\'bold\', fontsize=13)\nfig.tight_layout()\nfig.savefig(\'titanic_eda.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved titanic_eda.png\')"},
        {"label": "Diamonds dataset analysis", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ndiamonds = sns.load_dataset(\'diamonds\')\nsample = diamonds.sample(2000, random_state=42)\n\nfig, axes = plt.subplots(1, 3, figsize=(14, 5))\n# Price by cut\nsns.violinplot(data=sample, x=\'cut\', y=\'price\', palette=\'Set2\',\n               inner=\'quartile\', ax=axes[0])\naxes[0].set_title(\'Price by Cut\')\n\n# Carat vs price scatter\nsns.scatterplot(data=sample, x=\'carat\', y=\'price\', hue=\'color\',\n                palette=\'RdYlGn\', s=15, alpha=0.5, ax=axes[1])\naxes[1].set_title(\'Carat vs Price by Color\')\n\n# Correlation heatmap of numeric cols\ncorr = sample[[\'carat\',\'depth\',\'table\',\'price\',\'x\',\'y\',\'z\']].corr()\nsns.heatmap(corr, annot=True, fmt=\'.2f\', cmap=\'coolwarm\',\n            center=0, linewidths=0.5, ax=axes[2])\naxes[2].set_title(\'Feature Correlation\')\n\nfig.suptitle(\'Diamonds EDA\', fontweight=\'bold\', fontsize=13)\nfig.tight_layout()\nfig.savefig(\'diamonds_eda.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved diamonds_eda.png\')"},
        {"label": "Penguins complete EDA", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\npenguins = sns.load_dataset(\'penguins\').dropna()\n\nfig, axes = plt.subplots(2, 2, figsize=(12, 9))\nsns.scatterplot(data=penguins, x=\'bill_length_mm\', y=\'bill_depth_mm\',\n                hue=\'species\', style=\'island\', s=60, alpha=0.7, ax=axes[0,0])\naxes[0,0].set_title(\'Bill Length vs Depth by Species & Island\')\n\nsns.violinplot(data=penguins, x=\'species\', y=\'body_mass_g\',\n               hue=\'sex\', split=True, palette=\'Set2\', inner=\'box\',\n               ax=axes[0,1])\naxes[0,1].set_title(\'Body Mass by Species & Sex\')\n\nsns.ecdfplot(data=penguins, x=\'flipper_length_mm\', hue=\'species\',\n             palette=\'Set1\', linewidth=2, ax=axes[1,0])\naxes[1,0].set_title(\'Flipper Length ECDF by Species\')\n\ncounts = penguins.groupby([\'species\',\'island\']).size().reset_index(name=\'count\')\nsns.barplot(data=counts, x=\'species\', y=\'count\', hue=\'island\',\n            palette=\'pastel\', ax=axes[1,1])\naxes[1,1].set_title(\'Population by Species & Island\')\n\nfig.suptitle(\'Penguins Complete EDA\', fontweight=\'bold\', fontsize=13)\nfig.tight_layout()\nfig.savefig(\'penguins_eda.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved penguins_eda.png\')"},
        {"label": "MPG fuel efficiency analysis", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nmpg = sns.load_dataset(\'mpg\').dropna()\n\nfig, axes = plt.subplots(1, 3, figsize=(14, 5))\n# MPG trend by model year and origin\nsns.lineplot(data=mpg, x=\'model_year\', y=\'mpg\', hue=\'origin\',\n             palette=\'Set1\', linewidth=2, markers=True, ax=axes[0])\naxes[0].set_title(\'MPG by Year & Origin\')\n\n# Weight vs MPG regression by cylinders\ncyl_order = sorted(mpg[\'cylinders\'].unique())\npal = sns.color_palette(\'coolwarm\', len(cyl_order))\nfor i, cyl in enumerate(cyl_order):\n    sub = mpg[mpg.cylinders == cyl]\n    axes[1].scatter(sub.weight, sub.mpg, s=20, alpha=0.5, color=pal[i], label=f\'{cyl}cyl\')\naxes[1].set_xlabel(\'Weight (lbs)\'); axes[1].set_ylabel(\'MPG\')\naxes[1].legend(title=\'Cylinders\', fontsize=8); axes[1].set_title(\'Weight vs MPG by Cylinders\')\n\n# Horsepower distribution by origin\nsns.boxplot(data=mpg, x=\'origin\', y=\'horsepower\', palette=\'Set2\', ax=axes[2])\naxes[2].set_title(\'Horsepower by Origin\')\n\nfig.suptitle(\'MPG Dataset — Fuel Efficiency EDA\', fontweight=\'bold\', fontsize=13)\nfig.tight_layout()\nfig.savefig(\'mpg_eda.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved mpg_eda.png\')"}
    ],
"rw": {
    "title": "Complete Data Story",
    "scenario": "Using the \'diamonds\' dataset: tell a 4-panel data story: (1) price distribution by cut (violin), (2) price vs carat regression by clarity, (3) ECDF of price by cut, (4) heatmap of median price by cut×color.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\ndiamonds = sns.load_dataset(\'diamonds\')\nsample = diamonds.sample(3000, random_state=7)\ncut_order = [\'Fair\',\'Good\',\'Very Good\',\'Premium\',\'Ideal\']\n\nfig, axes = plt.subplots(2, 2, figsize=(13, 10))\n\nsns.violinplot(data=sample, x=\'cut\', y=\'price\', palette=\'YlOrRd\',\n               inner=\'quartile\', order=cut_order, ax=axes[0,0])\naxes[0,0].set_title(\'Price by Cut\', fontweight=\'bold\')\naxes[0,0].set_xlabel(\'Cut\'); axes[0,0].set_ylabel(\'Price ($)\')\n\nclarity_order = [\'I1\',\'SI2\',\'SI1\',\'VS2\',\'VS1\',\'VVS2\',\'VVS1\',\'IF\']\nsns.scatterplot(data=sample, x=\'carat\', y=\'price\', hue=\'clarity\',\n                palette=\'RdYlGn\', s=15, alpha=0.5,\n                hue_order=clarity_order, ax=axes[0,1])\naxes[0,1].set_title(\'Carat vs Price by Clarity\', fontweight=\'bold\')\n\nsns.ecdfplot(data=sample, x=\'price\', hue=\'cut\', palette=\'YlOrRd\',\n             linewidth=2, hue_order=cut_order, ax=axes[1,0])\naxes[1,0].set_title(\'Price ECDF by Cut\', fontweight=\'bold\')\naxes[1,0].set_xlabel(\'Price ($)\')\n\npivot = diamonds.groupby([\'cut\',\'color\'])[\'price\'].median().unstack()\npivot = pivot.loc[cut_order]\nsns.heatmap(pivot, cmap=\'YlOrRd\', annot=True, fmt=\'.0f\',\n            linewidths=0.3, ax=axes[1,1])\naxes[1,1].set_title(\'Median Price: Cut × Color\', fontweight=\'bold\')\n\nfig.suptitle(\'Diamond Price Analysis — Complete Story\', fontweight=\'bold\', fontsize=14)\nfig.tight_layout()\nfig.savefig(\'diamond_story.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved diamond_story.png\')"
},
"practice": {
    "title": "Real Dataset EDA Practice",
    "desc": "Load the \'mpg\' dataset. Create a 2x2 EDA dashboard: (1) lmplot of mpg vs weight by origin, (2) pairplot of [mpg, horsepower, weight] with hue=origin (quick version), (3) boxplot of mpg by cylinders, (4) lineplot of mean mpg by model_year. Drop NaN first.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nmpg = sns.load_dataset(\'mpg\').dropna()\n\n# Pairplot separately (it creates its own figure)\ng = sns.pairplot(mpg[[\'mpg\',\'horsepower\',\'weight\',\'origin\']],\n                 hue=\'origin\', palette=\'Set2\', plot_kws=dict(s=15, alpha=0.5))\ng.fig.suptitle(\'MPG Pairplot\', y=1.01)\ng.fig.savefig(\'mpg_pairplot.png\', dpi=80, bbox_inches=\'tight\')\nplt.close(g.fig)\n\nfig, axes = plt.subplots(1, 3, figsize=(15, 5))\n# TODO: boxplot mpg by cylinders\n# TODO: lineplot mean mpg by model_year, hue=origin\n# TODO: scatterplot weight vs mpg, hue=origin, regplot overlay\nfig.tight_layout()\nfig.savefig(\'mpg_dashboard.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved mpg_dashboard.png\')"
}
},

{
"title": "30. Object-Oriented Seaborn",
"desc": "Use the modern Seaborn Figure API: create a Figure object, add Subplots with share axes, and chain .plot() calls. Use Figure.save() and Figure.show(). Available in Seaborn 0.12+.",
"examples": [
        {"label": "Seaborn objects API: basic scatter", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nimport seaborn.objects as so\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\np = (\n    so.Plot(tips, x=\'total_bill\', y=\'tip\', color=\'sex\')\n    .add(so.Dot(alpha=0.6, pointsize=5))\n    .add(so.Line(), so.PolyFit(order=1))\n    .label(x=\'Total Bill ($)\', y=\'Tip ($)\', color=\'Sex\',\n           title=\'Tips: Scatter + Regression (objects API)\')\n)\np.save(\'so_scatter.png\', dpi=120, bbox_inches=\'tight\')\nprint(\'Saved so_scatter.png\')"},
        {"label": "Seaborn objects: Bar plot with grouping", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nimport seaborn.objects as so\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\np = (\n    so.Plot(tips, x=\'day\', y=\'total_bill\', color=\'sex\')\n    .add(so.Bar(), so.Agg(\'mean\'), so.Dodge())\n    .label(x=\'Day\', y=\'Mean Total Bill ($)\', color=\'Sex\',\n           title=\'Mean Bill by Day & Sex (objects API)\')\n)\np.save(\'so_bar.png\', dpi=120, bbox_inches=\'tight\')\nprint(\'Saved so_bar.png\')"},
        {"label": "Seaborn objects: histogram with KDE", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nimport seaborn.objects as so\nsns.set_theme(style=\'whitegrid\')\niris = sns.load_dataset(\'iris\')\n\np = (\n    so.Plot(iris, x=\'petal_length\', color=\'species\')\n    .add(so.Bars(), so.Hist(binwidth=0.3), so.Norm(\'percent\'))\n    .add(so.Line(), so.KDE())\n    .label(x=\'Petal Length (cm)\', y=\'Percent\',\n           title=\'Petal Length Distribution (objects API)\')\n)\np.save(\'so_hist.png\', dpi=120, bbox_inches=\'tight\')\nprint(\'Saved so_hist.png\')"},
        {"label": "Seaborn objects: faceted grid", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nimport seaborn.objects as so\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\np = (\n    so.Plot(tips, x=\'total_bill\', y=\'tip\', color=\'sex\')\n    .facet(col=\'time\', row=\'smoker\')\n    .add(so.Dot(alpha=0.5, pointsize=4))\n    .label(x=\'Total Bill ($)\', y=\'Tip ($)\',\n           title=\'Tips: Faceted Grid (objects API)\')\n    .limit(x=(0, 55), y=(0, 11))\n)\np.save(\'so_faceted.png\', dpi=120, bbox_inches=\'tight\')\nprint(\'Saved so_faceted.png\')"}
    ],
"rw": {
    "title": "Modern API Visualization",
    "scenario": "Use the seaborn.objects API to create a 3-part analysis of the \'penguins\' dataset: (1) scatter bill_length vs bill_depth with color=species, (2) bar mean body_mass by species+sex with dodge, (3) line flipper_length trend — all using so.Plot.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nimport seaborn.objects as so\nsns.set_theme(style=\'whitegrid\')\npenguins = sns.load_dataset(\'penguins\').dropna()\n\np1 = (\n    so.Plot(penguins, x=\'bill_length_mm\', y=\'bill_depth_mm\', color=\'species\')\n    .add(so.Dot(alpha=0.6, pointsize=5))\n    .label(x=\'Bill Length (mm)\', y=\'Bill Depth (mm)\',\n           title=\'Bill Dimensions by Species\')\n)\np1.save(\'so_penguin_scatter.png\', dpi=120, bbox_inches=\'tight\')\n\np2 = (\n    so.Plot(penguins, x=\'species\', y=\'body_mass_g\', color=\'sex\')\n    .add(so.Bar(), so.Agg(\'mean\'), so.Dodge())\n    .label(x=\'Species\', y=\'Mean Body Mass (g)\',\n           title=\'Body Mass by Species & Sex\')\n)\np2.save(\'so_penguin_bar.png\', dpi=120, bbox_inches=\'tight\')\nprint(\'Saved so_penguin_scatter.png and so_penguin_bar.png\')"
},
"practice": {
    "title": "Objects API Practice",
    "desc": "Using the seaborn objects API (so.Plot), recreate a regression scatter of tips total_bill vs tip, color by day, with a PolyFit(order=1) line. Facet by time (col=\'time\'). Save as \'so_practice.png\'.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nimport seaborn.objects as so\nsns.set_theme(style=\'whitegrid\')\ntips = sns.load_dataset(\'tips\')\n\n# TODO: so.Plot with x=total_bill, y=tip, color=day\n# TODO: .add(so.Dot) + .add(so.Line, so.PolyFit(order=1))\n# TODO: .facet(col=\'time\')\n# TODO: .save(\'so_practice.png\', dpi=120)"
}
},

{
"title": "31. Color Systems & Accessibility",
"desc": "Choose colorblind-safe palettes, use perceptually uniform colormaps, distinguish sequential vs. diverging vs. qualitative palettes, and apply Seaborn color_palette utilities.",
"examples": [
        {"label": "Qualitative palettes for categorical data", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(0)\ndf = pd.DataFrame({\n    \'value\': np.random.randn(200),\n    \'group\': np.random.choice(list(\'ABCDE\'), 200)\n})\n\nqual_palettes = [\'Set1\',\'Set2\',\'Set3\',\'tab10\',\'colorblind\',\'deep\']\nfig, axes = plt.subplots(2, 3, figsize=(14, 8))\nfor ax, pal in zip(axes.flat, qual_palettes):\n    sns.boxplot(data=df, x=\'group\', y=\'value\', palette=pal, ax=ax)\n    ax.set_title(f\'palette=\"{pal}\"\')\nfig.suptitle(\'Qualitative Palettes Comparison\', fontweight=\'bold\', fontsize=13)\nfig.tight_layout()\nfig.savefig(\'qual_palettes.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved qual_palettes.png\')"},
        {"label": "Sequential palettes for ordered data", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(1)\nx = y = np.linspace(-3, 3, 60)\nX, Y = np.meshgrid(x, y)\nZ = np.sin(X) * np.cos(Y)\n\nseq_palettes = [\'Blues\',\'YlOrRd\',\'viridis\',\'magma\']\nfig, axes = plt.subplots(1, 4, figsize=(16, 4))\nfor ax, pal in zip(axes, seq_palettes):\n    im = ax.pcolormesh(X, Y, Z, cmap=pal)\n    fig.colorbar(im, ax=ax, shrink=0.8)\n    ax.set_title(f\'cmap=\"{pal}\"\')\n    ax.set_aspect(\'equal\')\nfig.suptitle(\'Sequential Palettes for Heatmap Data\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'seq_palettes.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved seq_palettes.png\')"},
        {"label": "Diverging palettes for signed values", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'white\')\nnp.random.seed(2)\ndata = np.random.randn(10, 8) * 2\ndf = pd.DataFrame(data,\n    index=[f\'Product {i}\' for i in range(1,11)],\n    columns=[f\'Q{q}\' for q in range(1,9)])\n\ndiv_palettes = [\'RdBu_r\',\'RdYlGn\',\'coolwarm\',\'PiYG\']\nfig, axes = plt.subplots(1, 4, figsize=(16, 4))\nfor ax, pal in zip(axes, div_palettes):\n    sns.heatmap(df, cmap=pal, center=0, ax=ax,\n                cbar_kws={\'shrink\':0.8}, xticklabels=True, yticklabels=False)\n    ax.set_title(f\'cmap=\"{pal}\"\')\nfig.suptitle(\'Diverging Palettes for Change Data\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'div_palettes.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved div_palettes.png\')"},
        {"label": "Colorblind-safe vs non-safe comparison", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(3)\ndf = pd.DataFrame({\n    \'x\': np.linspace(0, 10, 80),\n    \'A\': np.sin(np.linspace(0, 10, 80)) + np.random.randn(80)*0.2,\n    \'B\': np.cos(np.linspace(0, 10, 80)) + np.random.randn(80)*0.2,\n    \'C\': np.sin(np.linspace(0, 10, 80)*1.5) + np.random.randn(80)*0.2,\n})\n\nfig, axes = plt.subplots(1, 2, figsize=(13, 5))\n# Non-safe: red-green confusion\ncolors_bad = [\'#ff0000\',\'#00aa00\',\'#0000ff\']\nfor col, c in zip([\'A\',\'B\',\'C\'], colors_bad):\n    axes[0].plot(df.x, df[col], color=c, linewidth=2, label=col,\n                 linestyle=\'-\')\naxes[0].set_title(\'Non-colorblind-safe (avoid red/green)\')\naxes[0].legend()\n\n# Colorblind-safe (Wong palette) with markers\ncb_colors = [\'#0072B2\',\'#D55E00\',\'#009E73\']\nmarkers = [\'o\',\'s\',\'^\']\nfor col, c, m in zip([\'A\',\'B\',\'C\'], cb_colors, markers):\n    axes[1].plot(df.x, df[col], color=c, linewidth=2,\n                 label=col, marker=m, markevery=8, markersize=7)\naxes[1].set_title(\'Colorblind-safe (Wong palette + markers)\')\naxes[1].legend()\n\nfor ax in axes:\n    ax.set_xlabel(\'x\'); ax.set_ylabel(\'y\')\n    ax.grid(True, alpha=0.3)\nfig.suptitle(\'Accessibility: Color Choice Matters\', fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'colorblind_safe.png\', dpi=120, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved colorblind_safe.png\')"}
    ],
"rw": {
    "title": "Accessible Dashboard Design",
    "scenario": "Redesign a 4-panel report using only colorblind-safe palettes: use \'colorblind\' for categorical, \'Blues\' for sequential, \'RdBu_r\' for diverging, and add hatch patterns or markers as secondary encodings.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(42)\ndf_cat = pd.DataFrame({\n    \'group\': np.repeat([\'A\',\'B\',\'C\',\'D\'],60),\n    \'value\': np.concatenate([np.random.normal(m,1.2,60) for m in [3,5,4,6]])\n})\ndf_seq = pd.DataFrame(np.random.rand(8,6)*100,\n                       columns=[f\'M{i}\' for i in range(1,7)],\n                       index=[f\'R{i}\' for i in range(1,9)])\ndf_div = pd.DataFrame(np.random.randn(6,5)*20,\n                       columns=[\'Q1\',\'Q2\',\'Q3\',\'Q4\',\'Q5\'],\n                       index=[f\'P{i}\' for i in range(1,7)])\n\nfig, axes = plt.subplots(2, 2, figsize=(13, 10))\n\n# Categorical: colorblind + hatch\nbars = sns.barplot(data=df_cat, x=\'group\', y=\'value\',\n                   palette=\'colorblind\', capsize=0.1, ax=axes[0,0])\nhatches = [\'\',\'///\',\'xxx\',\'...\']\nfor bar, hatch in zip(axes[0,0].patches, hatches*10):\n    bar.set_hatch(hatch)\naxes[0,0].set_title(\'Categorical: colorblind + hatch\')\n\n# Sequential heatmap\nsns.heatmap(df_seq, cmap=\'Blues\', annot=False, ax=axes[0,1],\n            cbar_kws={\'label\':\'Value\'})\naxes[0,1].set_title(\'Sequential: Blues\')\n\n# Diverging heatmap\nsns.heatmap(df_div, cmap=\'RdBu_r\', center=0, annot=True, fmt=\'.0f\',\n            linewidths=0.3, ax=axes[1,0])\naxes[1,0].set_title(\'Diverging: RdBu_r\')\n\n# Line with markers\ncb_colors = [\'#0072B2\',\'#D55E00\',\'#009E73\',\'#CC79A7\']\nx = np.arange(12)\nfor i,(col,m) in enumerate(zip(cb_colors,[\'o\',\'s\',\'^\',\'D\'])):\n    y = np.cumsum(np.random.randn(12)*0.5) + i\n    axes[1,1].plot(x, y, color=col, marker=m, linewidth=2,\n                   markevery=3, markersize=7, label=f\'Series {i+1}\')\naxes[1,1].legend(fontsize=8); axes[1,1].set_title(\'Lines: Wong palette + markers\')\naxes[1,1].grid(True, alpha=0.3)\n\nfig.suptitle(\'Accessible Dashboard — Colorblind-Safe Design\', fontweight=\'bold\', fontsize=13)\nfig.tight_layout()\nfig.savefig(\'accessible_seaborn.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved accessible_seaborn.png\')"
},
"practice": {
    "title": "Color Accessibility Practice",
    "desc": "Create a 4-group comparison plot (your choice of data). First plot with the red/green palette (unsafe). Then create a duplicate using the \'colorblind\' palette with different markers per group. Save both as \'color_bad.png\' and \'color_good.png\'.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(6)\ngroups = [\'Control\',\'TreatmentA\',\'TreatmentB\',\'TreatmentC\']\ndf = pd.DataFrame({\n    \'value\': np.concatenate([np.random.normal(m,1.5,60) for m in [3,4.5,3.8,5.2]]),\n    \'group\': np.repeat(groups,60)\n})\n\n# TODO: barplot with non-safe red/green palette, save \'color_bad.png\'\n# TODO: barplot with colorblind palette + stripplot with markers, save \'color_good.png\'"
}
},

{
"title": "32. Seaborn Dashboard Composition",
"desc": "Combine multiple seaborn plot types, matplotlib GridSpec, annotation overlays, and consistent theming to produce publication-quality, multi-panel analytical dashboards.",
"examples": [
        {"label": "4-panel EDA dashboard", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nfrom matplotlib.gridspec import GridSpec\n\nsns.set_theme(style=\'whitegrid\', palette=\'Set2\', font_scale=0.95)\nnp.random.seed(42)\ndf = pd.DataFrame({\n    \'revenue\': np.random.lognormal(5, 0.5, 300),\n    \'spend\':   np.random.uniform(1000, 10000, 300),\n    \'channel\': np.random.choice([\'Search\',\'Social\',\'Email\',\'Direct\'], 300),\n    \'month\':   np.random.choice(range(1,13), 300)\n})\ndf[\'revenue\'] = df[\'spend\'] * np.random.uniform(0.1, 0.5, 300) + np.random.randn(300)*50\n\nfig = plt.figure(figsize=(14, 9))\ngs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)\n\nax1 = fig.add_subplot(gs[0, :2])\nax2 = fig.add_subplot(gs[0, 2])\nax3 = fig.add_subplot(gs[1, :])\n\nsns.scatterplot(data=df, x=\'spend\', y=\'revenue\', hue=\'channel\',\n                style=\'channel\', s=50, alpha=0.6, ax=ax1)\nax1.set_title(\'Revenue vs Spend by Channel\', fontweight=\'bold\')\n\nsns.violinplot(data=df, x=\'channel\', y=\'revenue\', palette=\'Set2\',\n               inner=\'quartile\', ax=ax2)\nax2.set_title(\'Revenue Distribution\', fontweight=\'bold\')\nax2.set_xticklabels(ax2.get_xticklabels(), rotation=20, ha=\'right\', fontsize=8)\n\nmonth_agg = df.groupby([\'month\',\'channel\'])[\'revenue\'].mean().reset_index()\nsns.lineplot(data=month_agg, x=\'month\', y=\'revenue\', hue=\'channel\',\n             palette=\'Set2\', linewidth=2, markers=True, ax=ax3)\nax3.set_title(\'Monthly Average Revenue by Channel\', fontweight=\'bold\')\nax3.set_xlabel(\'Month\')\n\nfig.suptitle(\'Marketing Revenue Dashboard\', fontsize=14, fontweight=\'bold\')\nfig.savefig(\'sns_dashboard.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved sns_dashboard.png\')"},
        {"label": "Statistical report: hypothesis testing visual", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nfrom scipy import stats\n\nsns.set_theme(style=\'whitegrid\')\nnp.random.seed(1)\ncontrol    = np.random.normal(70, 12, 100)\ntreatment  = np.random.normal(75, 11, 100)\nt_stat, p_val = stats.ttest_ind(control, treatment)\neffect_size = (treatment.mean() - control.mean()) / np.sqrt(\n    ((len(control)-1)*control.std()**2 + (len(treatment)-1)*treatment.std()**2) /\n    (len(control)+len(treatment)-2))\n\ndf = pd.DataFrame({\n    \'score\': np.concatenate([control, treatment]),\n    \'group\': np.repeat([\'Control\',\'Treatment\'], 100)\n})\n\nfig, axes = plt.subplots(1, 3, figsize=(14, 5))\nsns.histplot(data=df, x=\'score\', hue=\'group\', kde=True, alpha=0.4,\n             palette=\'Set1\', stat=\'density\', common_norm=False, ax=axes[0])\naxes[0].set_title(\'Score Distributions\')\n\nsns.violinplot(data=df, x=\'group\', y=\'score\', palette=\'Set1\',\n               inner=\'box\', ax=axes[1])\naxes[1].set_title(\'Violin Comparison\')\n\nsns.ecdfplot(data=df, x=\'score\', hue=\'group\', palette=\'Set1\',\n             linewidth=2, ax=axes[2])\naxes[2].set_title(\'ECDF Comparison\')\n\nfor ax in axes:\n    ax.set_xlabel(\'Score\')\n\nfig.suptitle(f\'A/B Test: t={t_stat:.2f}, p={p_val:.4f}, d={effect_size:.2f}\',\n             fontsize=13, fontweight=\'bold\')\nfig.tight_layout()\nfig.savefig(\'hypothesis_dashboard.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved hypothesis_dashboard.png\')"},
        {"label": "Full EDA report: penguins deep dive", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nfrom matplotlib.gridspec import GridSpec\n\nsns.set_theme(style=\'whitegrid\', palette=\'colorblind\')\npenguins = sns.load_dataset(\'penguins\').dropna()\n\nfig = plt.figure(figsize=(15, 10), facecolor=\'white\')\ngs = GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.4)\n\n# Banner\nax0 = fig.add_subplot(gs[0, :])\nax0.text(0.5, 0.6, \'Palmer Penguins — Deep Dive EDA\',\n         ha=\'center\', va=\'center\', fontsize=16, fontweight=\'bold\',\n         transform=ax0.transAxes)\nax0.text(0.5, 0.1, f\'n={len(penguins)} penguins | 3 species | 3 islands\',\n         ha=\'center\', va=\'center\', fontsize=11, color=\'gray\',\n         transform=ax0.transAxes)\nax0.axis(\'off\')\n\n# Scatter bill dimensions\nax1 = fig.add_subplot(gs[1, :2])\nsns.scatterplot(data=penguins, x=\'bill_length_mm\', y=\'bill_depth_mm\',\n                hue=\'species\', style=\'island\', s=60, alpha=0.7, ax=ax1)\nax1.set_title(\'Bill Dimensions by Species & Island\', fontweight=\'bold\')\n\n# Count by species\nax2 = fig.add_subplot(gs[1, 2])\nsns.countplot(data=penguins, x=\'species\', hue=\'sex\',\n              palette=\'Set2\', ax=ax2)\nax2.set_title(\'Counts by Species & Sex\', fontweight=\'bold\')\nax2.set_xlabel(\'Species\')\n\n# Body mass violin\nax3 = fig.add_subplot(gs[2, :2])\nsns.violinplot(data=penguins, x=\'species\', y=\'body_mass_g\',\n               hue=\'sex\', split=True, palette=\'pastel\', inner=\'box\', ax=ax3)\nax3.set_title(\'Body Mass Distribution\', fontweight=\'bold\')\n\n# Flipper ECDF\nax4 = fig.add_subplot(gs[2, 2])\nsns.ecdfplot(data=penguins, x=\'flipper_length_mm\', hue=\'species\',\n             palette=\'colorblind\', linewidth=2, ax=ax4)\nax4.set_title(\'Flipper Length ECDF\', fontweight=\'bold\')\nax4.set_xlabel(\'Flipper Length (mm)\')\n\nfig.savefig(\'penguins_deep_dive.png\', dpi=150, bbox_inches=\'tight\',\n            facecolor=fig.get_facecolor())\nplt.close()\nprint(\'Saved penguins_deep_dive.png\')"},
        {"label": "Time series analytics dashboard", "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nfrom matplotlib.gridspec import GridSpec\n\nsns.set_theme(style=\'darkgrid\', palette=\'Set2\')\nnp.random.seed(77)\nn_days = 90\ndates = pd.date_range(\'2024-01-01\', periods=n_days)\nproducts = [\'Widget\',\'Gadget\',\'Doohickey\']\nrows = []\nfor prod in products:\n    base = np.random.uniform(80, 150)\n    trend = np.cumsum(np.random.randn(n_days)*2) + base\n    for d, v in zip(dates, trend):\n        rows.append({\'date\':d,\'product\':prod,\'sales\':max(0,v),\n                     \'returns\':max(0,v*0.05+np.random.randn())})\ndf = pd.DataFrame(rows)\ndf[\'month\'] = df[\'date\'].dt.month\n\nfig = plt.figure(figsize=(14, 9))\ngs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)\n\nax1 = fig.add_subplot(gs[0, :])\nsns.lineplot(data=df, x=\'date\', y=\'sales\', hue=\'product\',\n             palette=\'Set2\', linewidth=2, ax=ax1)\nax1.set_title(\'Daily Sales Trend by Product\', fontweight=\'bold\')\nax1.set_xlabel(\'Date\'); ax1.set_ylabel(\'Sales ($)\')\n\nax2 = fig.add_subplot(gs[1, 0])\nmonth_df = df.groupby([\'month\',\'product\'])[\'sales\'].mean().reset_index()\nsns.barplot(data=month_df, x=\'month\', y=\'sales\', hue=\'product\',\n            palette=\'Set2\', ax=ax2)\nax2.set_title(\'Mean Monthly Sales\', fontweight=\'bold\')\nax2.set_xlabel(\'Month\')\n\nax3 = fig.add_subplot(gs[1, 1])\nsns.scatterplot(data=df, x=\'sales\', y=\'returns\', hue=\'product\',\n                palette=\'Set2\', s=20, alpha=0.4, ax=ax3)\n# Add regression per product\nfor prod, grp in df.groupby(\'product\'):\n    m,b = np.polyfit(grp.sales, grp.returns, 1)\n    x_l = np.linspace(grp.sales.min(), grp.sales.max(), 50)\n    ax3.plot(x_l, m*x_l+b, linewidth=1.5, alpha=0.8)\nax3.set_title(\'Sales vs Returns\', fontweight=\'bold\')\n\nfig.suptitle(\'Product Analytics Dashboard\', fontsize=14, fontweight=\'bold\')\nfig.savefig(\'time_series_dashboard.png\', dpi=150, bbox_inches=\'tight\')\nplt.close()\nprint(\'Saved time_series_dashboard.png\')"}
    ],
"rw": {
    "title": "Comprehensive Analysis Report",
    "scenario": "Design a 5-panel Seaborn+GridSpec report on the \'diamonds\' dataset: (1) banner with dataset stats, (2) price by cut violin, (3) carat vs price scatter by clarity, (4) price ECDF by cut, (5) heatmap of counts cut×color.",
    "code": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nfrom matplotlib.gridspec import GridSpec\n\nsns.set_theme(style=\'whitegrid\', palette=\'Set2\')\ndiamonds = sns.load_dataset(\'diamonds\')\nsample = diamonds.sample(2000, random_state=42)\ncut_order = [\'Fair\',\'Good\',\'Very Good\',\'Premium\',\'Ideal\']\n\nfig = plt.figure(figsize=(14, 11), facecolor=\'white\')\ngs = GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.4)\n\n# Banner\nax0 = fig.add_subplot(gs[0, :])\nax0.text(0.5, 0.6, \'Diamonds Dataset — Comprehensive Report\',\n         ha=\'center\', fontsize=15, fontweight=\'bold\', transform=ax0.transAxes)\nax0.text(0.5, 0.1, f\'{len(diamonds):,} diamonds | {diamonds.cut.nunique()} cuts | \'\n                   f\'Price: ${diamonds.price.min():,}–${diamonds.price.max():,}\',\n         ha=\'center\', fontsize=10, color=\'gray\', transform=ax0.transAxes)\nax0.axis(\'off\')\n\nax1 = fig.add_subplot(gs[1, :2])\nsns.violinplot(data=sample, x=\'cut\', y=\'price\', palette=\'YlOrRd\',\n               inner=\'quartile\', order=cut_order, ax=ax1)\nax1.set_title(\'Price by Cut\', fontweight=\'bold\')\n\nax2 = fig.add_subplot(gs[1, 2])\nclarity_order = [\'I1\',\'SI2\',\'SI1\',\'VS2\',\'VS1\',\'VVS2\',\'VVS1\',\'IF\']\nsns.scatterplot(data=sample, x=\'carat\', y=\'price\', hue=\'clarity\',\n                palette=\'RdYlGn\', s=10, alpha=0.4,\n                hue_order=clarity_order, ax=ax2, legend=False)\nax2.set_title(\'Carat vs Price\', fontweight=\'bold\')\n\nax3 = fig.add_subplot(gs[2, :2])\nsns.ecdfplot(data=sample, x=\'price\', hue=\'cut\', palette=\'YlOrRd\',\n             linewidth=2, hue_order=cut_order, ax=ax3)\nax3.set_title(\'Price ECDF by Cut\', fontweight=\'bold\')\n\nax4 = fig.add_subplot(gs[2, 2])\ncounts = diamonds.groupby([\'cut\',\'color\']).size().unstack().loc[cut_order]\nsns.heatmap(counts, cmap=\'Blues\', annot=True, fmt=\'d\',\n            linewidths=0.3, ax=ax4, cbar=False)\nax4.set_title(\'Count: Cut × Color\', fontweight=\'bold\')\n\nfig.suptitle(\'Diamond Market Analysis\', fontsize=15, fontweight=\'bold\', y=1.01)\nfig.savefig(\'diamonds_report.png\', dpi=150, bbox_inches=\'tight\',\n            facecolor=fig.get_facecolor())\nplt.close()\nprint(\'Saved diamonds_report.png\')"
},
"practice": {
    "title": "Dashboard Practice",
    "desc": "Build your own 4-panel seaborn dashboard using any dataset you prefer (tips, penguins, titanic, mpg, etc.). Requirements: (1) GridSpec layout with at least one spanning panel, (2) 4 different plot types, (3) consistent palette and theme, (4) suptitle banner, (5) save at 150 DPI.",
    "starter": "import matplotlib\nmatplotlib.use(\'Agg\')\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nfrom matplotlib.gridspec import GridSpec\n\nsns.set_theme(style=\'whitegrid\', palette=\'Set2\')\n# Choose your dataset\ntips = sns.load_dataset(\'tips\')\n\nfig = plt.figure(figsize=(13, 9))\ngs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)\n\n# TODO: Panel 1 — spanning top row (gs[0, :])\n# TODO: Panel 2 — bottom-left (gs[1, :2])\n# TODO: Panel 3 — bottom-right (gs[1, 2])\n# Pick 4 different plot types across panels\n# TODO: suptitle banner\n# TODO: save \'my_sns_dashboard.png\' at 150 DPI\nplt.close()\nprint(\'Dashboard saved!\')"
}
},

]  # end SECTIONS


html = make_html(SECTIONS)
nb   = make_nb(SECTIONS)
(BASE / "index.html").write_text(html, encoding="utf-8")
(BASE / "study_guide.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")
print(f"Seaborn guide created: {BASE}")
print(f"  index.html:        {(BASE/'index.html').stat().st_size/1024:.1f} KB")
print(f"  study_guide.ipynb: {len(nb['cells'])} cells")
