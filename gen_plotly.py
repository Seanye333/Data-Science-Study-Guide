#!/usr/bin/env python3
"""Generate Plotly study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE   = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\05_plotly")
BASE.mkdir(parents=True, exist_ok=True)
ACCENT = "#a78bfa"
EMOJI  = "📈"
TITLE  = "Plotly"

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
            pex_html = ""
            for k, pex in enumerate(practice.get("examples", [])):
                pcid = f"pe{i}_{k}"
                pex_html += (f'<div class="code-block"><div class="ch"><span>{esc(pex.get("label","Example"))}</span>'
                             f'<button onclick="cp(\'{pcid}\')">Copy</button></div>'
                             f'<pre><code id="{pcid}" class="language-python">{esc(pex["code"])}</code></pre></div>')
            practice_html = (
                f'<div class="practice">'
                f'<div class="ph">&#x1F3CB;&#xFE0F; Practice: {esc(practice["title"])}</div>'
                f'<div class="pd">{esc(practice["desc"])}</div>'
                f'{pex_html}'
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
    cells.append(md(f"# {TITLE} Study Guide\n\nInteractive charts for the web. Run in Jupyter — charts render inline with full interactivity."))
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
"title": "1. Plotly Express Basics",
"desc": "plotly.express (px) creates interactive charts in one line. Charts are HTML/JavaScript — hover, zoom, and pan by default.",
"examples": [
{"label": "First chart: px.scatter", "code":
"""import plotly.express as px

# Built-in dataset
df = px.data.gapminder().query("year == 2007")

fig = px.scatter(
    df, x='gdpPercap', y='lifeExp',
    size='pop', color='continent',
    hover_name='country',
    log_x=True,
    title='GDP per Capita vs Life Expectancy (2007)',
    labels={'gdpPercap': 'GDP per Capita (log)', 'lifeExp': 'Life Expectancy'}
)
fig.show()"""},
{"label": "px.line — time series", "code":
"""import plotly.express as px

df = px.data.gapminder().query("continent == 'Europe'")

fig = px.line(
    df, x='year', y='lifeExp',
    color='country',
    hover_name='country',
    title='Life Expectancy in Europe Over Time',
    labels={'lifeExp': 'Life Expectancy', 'year': 'Year'}
)
fig.update_layout(showlegend=False)   # too many countries for legend
fig.show()"""},
{"label": "px.line with hover_data and markers", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
months = pd.date_range('2024-01', periods=12, freq='MS')
df = pd.DataFrame({
    'month':   list(months) * 3,
    'revenue': np.concatenate([
        100 + np.cumsum(np.random.randn(12) * 5),
        80  + np.cumsum(np.random.randn(12) * 4),
        60  + np.cumsum(np.random.randn(12) * 3),
    ]),
    'region':  ['North']*12 + ['South']*12 + ['West']*12,
    'target':  np.concatenate([np.full(12, 110), np.full(12, 85), np.full(12, 65)]),
})
df['vs_target'] = (df['revenue'] - df['target']).round(1)

fig = px.line(
    df, x='month', y='revenue',
    color='region', markers=True,
    hover_data=['target', 'vs_target'],
    title='Monthly Revenue by Region with Target Context',
    labels={'revenue': 'Revenue ($K)', 'month': 'Month'},
    color_discrete_sequence=px.colors.qualitative.Bold,
)
fig.update_traces(marker=dict(size=8))
fig.update_layout(height=420, hovermode='x unified')
fig.show()"""},
{"label": "Range selector buttons and slider", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(7)
dates = pd.date_range('2020-01-01', periods=365*4, freq='D')
price = 100 + np.cumsum(np.random.randn(len(dates)) * 1.2)

df = pd.DataFrame({'date': dates, 'price': price.round(2)})

fig = px.line(
    df, x='date', y='price',
    title='Stock Price — Interactive Range Selector',
    labels={'price': 'Price ($)', 'date': 'Date'},
)
fig.update_traces(line=dict(color='#636EFA', width=1.5))

# Range selector buttons (1M, 3M, 6M, 1Y, All)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=[
            dict(count=1,  label='1M', step='month', stepmode='backward'),
            dict(count=3,  label='3M', step='month', stepmode='backward'),
            dict(count=6,  label='6M', step='month', stepmode='backward'),
            dict(count=1,  label='1Y', step='year',  stepmode='backward'),
            dict(step='all', label='All'),
        ]
    )
)
fig.update_layout(height=460, xaxis_rangeslider_thickness=0.05)
fig.show()
print("Trace type:", fig.data[0].type)
print("Date range:", df['date'].min().date(), "to", df['date'].max().date())"""},
{"label": "Faceted Box Plot with Outlier Annotations", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
n   = 300
df  = pd.DataFrame({
    'department': rng.choice(['Engineering','Sales','Marketing','Finance'], n),
    'level':      rng.choice(['Junior','Mid','Senior'], n),
    'salary':     rng.normal(85000, 20000, n).clip(40000, 180000),
})

fig = px.box(
    df, x='level', y='salary',
    facet_col='department', facet_col_wrap=2,
    color='level',
    color_discrete_sequence=px.colors.qualitative.Set2,
    points='outliers',
    title='Salary Distribution by Department & Level',
    labels={'salary': 'Annual Salary ($)', 'level': 'Level'},
    width=900, height=600,
    category_orders={'level': ['Junior', 'Mid', 'Senior']},
)
fig.update_traces(marker=dict(size=4, opacity=0.6))
fig.update_layout(showlegend=False, title_font_size=15)
fig.show()"""}
],
"practice": {
"title": "Multi-Line Chart with Hover Data",
"desc": "Using px.data.gapminder(), create a multi-line chart of life expectancy over time for exactly 5 countries of your choice. Add pop and gdpPercap as hover_data. Style the markers and use hovermode='x unified' so all lines show on hover.",
"starter":
"""import plotly.express as px

df = px.data.gapminder()

# Pick 5 countries
countries = ['United States', 'China', 'India', 'Brazil', 'Germany']
# TODO: filtered = df[df['country'].isin(countries)]

# TODO: fig = px.line(
#     filtered, x='year', y='lifeExp',
#     color='country', markers=True,
#     hover_data=['pop', 'gdpPercap'],
#     title='Life Expectancy Trends — 5 Countries',
# )
# TODO: fig.update_traces(marker=dict(size=8))
# TODO: fig.update_layout(hovermode='x unified', height=450)
# TODO: fig.show()""",
"examples": [
{"label": "Candlestick Chart with Volume", "code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
n   = 60
dates = pd.date_range('2024-01-01', periods=n, freq='B')
close = 100 + np.cumsum(rng.normal(0, 1.5, n))
high  = close + rng.uniform(0.5, 3, n)
low   = close - rng.uniform(0.5, 3, n)
open_ = close - rng.uniform(-1.5, 1.5, n)
vol   = rng.integers(500000, 2000000, n)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    row_heights=[0.7, 0.3],
                    vertical_spacing=0.03)

fig.add_trace(go.Candlestick(
    x=dates, open=open_, high=high, low=low, close=close,
    name='OHLC', increasing_line_color='#26a69a',
    decreasing_line_color='#ef5350'), row=1, col=1)

colors = ['#26a69a' if c >= o else '#ef5350'
          for c, o in zip(close, open_)]
fig.add_trace(go.Bar(x=dates, y=vol, marker_color=colors,
                     name='Volume', opacity=0.7), row=2, col=1)

# 10-day moving average
ma10 = pd.Series(close).rolling(10).mean()
fig.add_trace(go.Scatter(x=dates, y=ma10, mode='lines',
                         line=dict(color='orange', width=2, dash='dot'),
                         name='MA10'), row=1, col=1)

fig.update_layout(title='Stock OHLC + Volume', xaxis_rangeslider_visible=False,
                  height=550, template='plotly_dark',
                  hovermode='x unified')
fig.show()"""},
{"label": "Waterfall Chart for Revenue Analysis", "code":
"""import plotly.graph_objects as go

items  = ['Starting Revenue','Product A',  'Product B', 'Churn',
          'Upsell',          'Discounts',  'Net Revenue']
values = [1000, 250, 180, -120, 90, -60, 0]
values[-1] = sum(values[:-1])

measure = ['absolute'] + ['relative']*(len(items)-2) + ['total']

fig = go.Figure(go.Waterfall(
    name='Revenue',
    orientation='v',
    measure=measure,
    x=items,
    y=values,
    text=[f'${v:+,}' if v != 0 else f'${abs(values[-1]):,}' for v in values],
    textposition='outside',
    connector={'line': {'color': 'rgb(63, 63, 63)'}},
    increasing={'marker': {'color': '#26a69a'}},
    decreasing={'marker': {'color': '#ef5350'}},
    totals={'marker': {'color': '#7e57c2'}},
))

fig.update_layout(
    title='Annual Revenue Waterfall Analysis',
    title_font_size=16,
    yaxis_title='Revenue ($K)',
    waterfallgap=0.3,
    height=500,
    template='plotly_white',
    showlegend=False,
)
fig.show()"""},
]
},
"rw": {
"title": "Sales KPI Interactive Dashboard",
"scenario": "A product manager builds a quick interactive scatter to explore the relationship between marketing spend and revenue by market.",
"code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
markets = ['US','UK','DE','FR','JP','BR','IN','AU','CA','MX']
df = pd.DataFrame({
    'market':       markets,
    'ad_spend':     np.random.uniform(50, 500, 10).round(1),
    'revenue':      np.random.uniform(200, 2000, 10).round(1),
    'customers':    np.random.randint(500, 10000, 10),
    'region':       ['Americas','Europe','Europe','Europe',
                     'Asia','Americas','Asia','Pacific','Americas','Americas'],
})
df['roi'] = (df['revenue'] / df['ad_spend']).round(2)

fig = px.scatter(
    df, x='ad_spend', y='revenue',
    size='customers', color='region',
    text='market',
    hover_data=['roi', 'customers'],
    title='Marketing Spend vs Revenue by Market',
    labels={'ad_spend': 'Ad Spend ($K)', 'revenue': 'Revenue ($K)'},
    size_max=50
)
fig.update_traces(textposition='top center', textfont_size=10)
fig.update_layout(height=450)
fig.show()"""}
},

{
"title": "2. Bar & Pie Charts",
"desc": "px.bar for categorical comparisons; px.pie and px.sunburst for part-to-whole. All support hover, faceting, and animation.",
"examples": [
{"label": "px.bar with facets", "code":
"""import plotly.express as px

df = px.data.tips()

fig = px.bar(
    df, x='day', y='total_bill',
    color='sex', barmode='group',
    facet_col='time',
    title='Total Bill by Day, Gender, and Meal Time',
    labels={'total_bill': 'Total Bill ($)', 'day': 'Day'},
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig.update_layout(height=400)
fig.show()"""},
{"label": "px.pie and px.sunburst", "code":
"""import plotly.express as px
import pandas as pd

# Pie chart
df_pie = pd.DataFrame({
    'channel':  ['Organic', 'Paid Search', 'Social', 'Email', 'Direct'],
    'sessions': [35, 25, 20, 12, 8],
})
fig1 = px.pie(df_pie, names='channel', values='sessions',
              title='Traffic by Channel', hole=0.4)
fig1.show()

# Sunburst — hierarchical
df_sun = px.data.gapminder().query("year==2007 and continent in ['Europe','Americas']")
fig2 = px.sunburst(df_sun, path=['continent','country'],
                   values='pop', color='lifeExp',
                   color_continuous_scale='RdYlGn',
                   title='Population & Life Expectancy')
fig2.show()"""},
{"label": "Grouped and stacked bar comparison", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(7)
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
products = ['Widget', 'Gadget', 'Gizmo']

rows = []
for q in quarters:
    for p in products:
        rows.append({'quarter': q, 'product': p,
                     'revenue': round(np.random.uniform(40, 120), 1)})
df = pd.DataFrame(rows)

# Grouped bars
fig1 = px.bar(df, x='quarter', y='revenue', color='product',
              barmode='group',
              title='Quarterly Revenue — Grouped',
              color_discrete_sequence=px.colors.qualitative.Pastel)
fig1.update_layout(height=380)
fig1.show()

# Stacked bars (same data)
fig2 = px.bar(df, x='quarter', y='revenue', color='product',
              barmode='stack',
              title='Quarterly Revenue — Stacked',
              color_discrete_sequence=px.colors.qualitative.Pastel)
fig2.update_layout(height=380)
fig2.show()"""},
{"label": "Waterfall chart with go.Waterfall", "code":
"""import plotly.graph_objects as go

# P&L waterfall: starting revenue, additions, deductions, net
labels   = ['Gross Revenue', 'COGS', 'Gross Profit',
            'Operating Exp', 'EBITDA', 'D&A', 'Tax', 'Net Income']
measures = ['absolute', 'relative', 'total',
            'relative',  'total',   'relative', 'relative', 'total']
values   = [500, -180, None, -120, None, -30, -42, None]

fig = go.Figure(go.Waterfall(
    name='P&L 2024',
    orientation='v',
    measure=measures,
    x=labels,
    y=[500, -180, 0, -120, 0, -30, -42, 0],
    text=['+$500', '-$180', '$320', '-$120', '$200', '-$30', '-$42', '$128'],
    textposition='outside',
    connector=dict(line=dict(color='#444', width=1, dash='dot')),
    increasing=dict(marker=dict(color='#00CC96')),
    decreasing=dict(marker=dict(color='#EF553B')),
    totals=dict(marker=dict(color='#636EFA')),
))

fig.update_layout(
    title='2024 P&L Waterfall Chart',
    yaxis_title='Amount ($K)',
    height=450,
    showlegend=False,
    plot_bgcolor='#1a1a2e',
    paper_bgcolor='#16213e',
    font=dict(color='#e0e0e0'),
    yaxis=dict(gridcolor='#333'),
)
fig.show()
print("Waterfall traces:", len(fig.data))
print("Net Income: $128K")"""}
],
"practice": {
"title": "Sunburst Drill-Down Chart",
"desc": "Build a px.sunburst chart using a DataFrame with three levels: continent -> country -> city (invent 2-3 cities per country). Use population as the values column and color by a numeric metric (e.g. GDP). Add a meaningful title and set height=520.",
"starter":
"""import plotly.express as px
import pandas as pd

# Build a simple hierarchical dataset
rows = [
    # continent, country, city, population, gdp_index
    ('Americas', 'USA', 'New York',    8_000_000, 95),
    ('Americas', 'USA', 'Los Angeles', 4_000_000, 88),
    ('Americas', 'Brazil', 'Sao Paulo',12_000_000, 55),
    ('Americas', 'Brazil', 'Rio',       6_500_000, 50),
    ('Europe',   'Germany', 'Berlin',   3_600_000, 82),
    ('Europe',   'Germany', 'Munich',   1_500_000, 90),
    ('Europe',   'France',  'Paris',    2_100_000, 78),
    ('Europe',   'France',  'Lyon',       500_000, 70),
    ('Asia',     'Japan',   'Tokyo',   13_900_000, 87),
    ('Asia',     'Japan',   'Osaka',    2_700_000, 80),
    ('Asia',     'India',   'Mumbai',  20_000_000, 42),
    ('Asia',     'India',   'Delhi',   30_000_000, 38),
]
df = pd.DataFrame(rows, columns=['continent','country','city','population','gdp_index'])

# TODO: fig = px.sunburst(
#     df, path=['continent', 'country', 'city'],
#     values='population',
#     color='gdp_index',
#     color_continuous_scale='Blues',
#     title='Population Drill-Down: Continent -> Country -> City',
# )
# TODO: fig.update_layout(height=520)
# TODO: fig.show()"""
},
"rw": {
"title": "Revenue Breakdown by Product & Region",
"scenario": "A CFO uses an interactive sunburst chart to drill down from region → product category → SKU in the quarterly review.",
"code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(5)
regions    = ['North America', 'Europe', 'Asia Pacific']
categories = ['Electronics', 'Clothing', 'Home', 'Food']
skus_per   = 3

rows = []
for region in regions:
    for cat in categories:
        for sku_i in range(1, skus_per + 1):
            rows.append({
                'region':   region,
                'category': cat,
                'sku':      f'{cat[:3]}-{sku_i:03d}',
                'revenue':  round(np.random.uniform(50, 500), 1),
            })
df = pd.DataFrame(rows)

fig = px.sunburst(
    df, path=['region', 'category', 'sku'],
    values='revenue',
    color='revenue',
    color_continuous_scale='Blues',
    title='Q2 2024 Revenue Drill-Down (Region → Category → SKU)',
)
fig.update_layout(height=550, coloraxis_showscale=False)
fig.show()"""}
},

{
"title": "3. Histogram & Box Plot",
"desc": "px.histogram and px.box create interactive distribution charts. Hover shows exact statistics; click legend to toggle groups.",
"examples": [
{"label": "px.histogram with marginal", "code":
"""import plotly.express as px

df = px.data.tips()

fig = px.histogram(
    df, x='total_bill',
    color='time', barmode='overlay',
    marginal='box',       # adds mini box plot on top
    opacity=0.7,
    nbins=25,
    title='Total Bill Distribution by Meal Time',
    labels={'total_bill': 'Total Bill ($)'},
    color_discrete_sequence=['#636EFA','#EF553B']
)
fig.show()"""},
{"label": "px.box and px.violin", "code":
"""import plotly.express as px
import pandas as pd

df = px.data.tips()

fig1 = px.box(df, x='day', y='tip', color='smoker',
              notched=True,
              title='Tip Distribution — Box Plot (notched)',
              labels={'tip': 'Tip ($)'})
fig1.show()

fig2 = px.violin(df, x='day', y='total_bill', color='sex',
                 box=True, points='outliers',
                 title='Total Bill — Violin + Box',
                 labels={'total_bill': 'Total Bill ($)'})
fig2.show()"""},
{"label": "Faceted histogram across categories", "code":
"""import plotly.express as px
import numpy as np
import pandas as pd

np.random.seed(42)
groups = ['Group A', 'Group B', 'Group C']
rows = []
for g in groups:
    mean = {'Group A': 50, 'Group B': 65, 'Group C': 80}[g]
    vals = np.random.normal(mean, 12, 200)
    for v in vals:
        rows.append({'group': g, 'score': round(v, 1)})
df = pd.DataFrame(rows)

fig = px.histogram(
    df, x='score', facet_col='group',
    color='group', nbins=30,
    opacity=0.75,
    marginal='violin',
    title='Score Distribution Faceted by Group',
    labels={'score': 'Score'},
    color_discrete_sequence=px.colors.qualitative.Set1,
)
fig.update_layout(height=420, showlegend=False)
fig.show()"""},
{"label": "Notched box plot with strip overlay", "code":
"""import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

np.random.seed(42)
departments = ['Engineering', 'Sales', 'Marketing', 'Support']
rows = []
for dept in departments:
    base = {'Engineering': 95, 'Sales': 72, 'Marketing': 68, 'Support': 60}[dept]
    scores = np.random.normal(base, 10, 60).clip(0, 100)
    for s in scores:
        rows.append({'department': dept, 'score': round(s, 1)})
df = pd.DataFrame(rows)

# Notched violin with embedded box and all points
fig = px.violin(
    df, x='department', y='score',
    color='department',
    box=True,
    points='all',
    title='Performance Score Distribution by Department',
    labels={'score': 'Score', 'department': 'Department'},
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig.update_traces(
    meanline_visible=True,
    jitter=0.3,
    pointpos=-1.5,
    marker=dict(size=3, opacity=0.5),
)
fig.update_layout(height=480, showlegend=False)
fig.show()
for dept in departments:
    vals = df[df['department']==dept]['score']
    print(f"{dept}: median={vals.median():.1f}, std={vals.std():.1f}")"""}
],
"practice": {
"title": "Grouped Violin Plot",
"desc": "Using px.data.tips(), create a violin plot of total_bill grouped by day on the x-axis, colored by smoker (yes/no). Enable box=True and points='all'. Then add a second figure: a faceted histogram of tip amounts, faceted by time (Lunch/Dinner), with a 'rug' marginal.",
"starter":
"""import plotly.express as px

df = px.data.tips()

# 1. Grouped violin: total_bill by day, colored by smoker
# TODO: fig1 = px.violin(
#     df, x='day', y='total_bill', color='smoker',
#     box=True, points='all',
#     title='Total Bill Distribution by Day and Smoker Status',
# )
# TODO: fig1.update_layout(height=450)
# TODO: fig1.show()

# 2. Faceted histogram: tip by time with rug marginal
# TODO: fig2 = px.histogram(
#     df, x='tip', facet_col='time',
#     color='time', marginal='rug',
#     nbins=20, opacity=0.8,
#     title='Tip Distribution: Lunch vs Dinner',
# )
# TODO: fig2.update_layout(height=400)
# TODO: fig2.show()""",
"examples": [
{"label": "Parallel Coordinates Plot for Multivariate Exploration", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

rng = np.random.default_rng(0)
n   = 300
df  = pd.DataFrame({
    'tenure':       rng.exponential(24, n).clip(1, 120),
    'usage_rate':   rng.beta(5, 2, n) * 100,
    'support_calls':rng.poisson(3, n),
    'billing_score':rng.normal(75, 15, n).clip(0, 100),
    'monthly_spend':rng.lognormal(4, 0.5, n),
    'churn':        rng.choice([0, 1], n, p=[0.75, 0.25]),
})

fig = px.parallel_coordinates(
    df,
    color='churn',
    color_continuous_scale=px.colors.diverging.Tealrose,
    color_continuous_midpoint=0.5,
    dimensions=['tenure','usage_rate','support_calls','billing_score','monthly_spend'],
    labels={
        'tenure':        'Tenure (mo)',
        'usage_rate':    'Usage %',
        'support_calls': 'Support Calls',
        'billing_score': 'Billing Score',
        'monthly_spend': 'Monthly Spend',
    },
    title='Parallel Coordinates: Customer Churn Features',
)
fig.update_layout(height=450, title_font_size=15,
                  coloraxis_colorbar=dict(title='Churn Risk', tickvals=[0,1],
                                          ticktext=['Low','High']))
fig.show()"""},
{"label": "Radar / Spider Chart for Multi-Metric Comparison", "code":
"""import plotly.graph_objects as go
import numpy as np

categories = ['Speed', 'Accuracy', 'Recall', 'Precision', 'F1-Score', 'AUC-ROC']
models = {
    'Logistic Regression': [65, 72, 68, 75, 71, 74],
    'Random Forest':       [80, 85, 83, 87, 85, 88],
    'XGBoost':             [88, 90, 89, 91, 90, 92],
    'Neural Network':      [75, 88, 86, 89, 87, 90],
}
colors = ['#636EFA','#EF553B','#00CC96','#AB63FA']

fig = go.Figure()
for (model, values), color in zip(models.items(), colors):
    vals = values + [values[0]]  # close the polygon
    cats = categories + [categories[0]]
    fig.add_trace(go.Scatterpolar(
        r=vals, theta=cats, fill='toself',
        name=model, line_color=color,
        fillcolor=color, opacity=0.25,
        hovertemplate='%{theta}: %{r}<extra>' + model + '</extra>',
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[50, 100],
                                tickfont=dict(size=9))),
    title='Model Performance Radar Chart',
    title_font_size=15,
    legend=dict(x=1.05, y=0.5),
    height=500,
    template='plotly_white',
)
fig.show()"""},
]
},
"rw": {
"title": "A/B Test Distribution Explorer",
"scenario": "A data scientist uses interactive histograms to explore the full distribution of test results across experiment variants.",
"code":
"""import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)
control = np.random.normal(45.0, 12, 500)
variant = np.random.normal(49.5, 11, 500)

df = pd.DataFrame({
    'revenue':  np.concatenate([control, variant]),
    'group':    ['Control']*500 + ['Variant B']*500,
})

t, p = stats.ttest_ind(control, variant)

fig = px.histogram(
    df, x='revenue', color='group',
    barmode='overlay', opacity=0.65, nbins=35,
    marginal='violin',
    color_discrete_map={'Control':'#636EFA','Variant B':'#EF553B'},
    title=f'A/B Test Revenue Distribution  |  p-value={p:.4f} {"✓ Significant" if p<0.05 else "✗ Not significant"}',
    labels={'revenue': 'Revenue ($)'},
)
fig.add_vline(x=control.mean(), line_dash='dash', line_color='#636EFA',
              annotation_text=f'Control μ={control.mean():.1f}')
fig.add_vline(x=variant.mean(), line_dash='dash', line_color='#EF553B',
              annotation_text=f'Variant μ={variant.mean():.1f}')
fig.update_layout(height=450)
fig.show()"""}
},

{
"title": "4. Heatmap & Scatter Matrix",
"desc": "px.imshow renders 2D matrices as interactive heatmaps. px.scatter_matrix creates an interactive pairplot grid.",
"examples": [
{"label": "px.imshow — correlation heatmap", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
features = ['Revenue', 'Cost', 'Margin', 'Customers', 'NPS']
n = 200
data = np.random.randn(n, 5)
# Add correlations
data[:, 2] = 0.8*data[:,0] - 0.6*data[:,1] + np.random.randn(n)*0.3
data[:, 4] = 0.5*data[:,2] + np.random.randn(n)*0.7

df   = pd.DataFrame(data, columns=features)
corr = df.corr().round(2)

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    zmin=-1, zmax=1,
    title='Feature Correlation Matrix'
)
fig.update_layout(height=450)
fig.show()"""},
{"label": "px.scatter_matrix", "code":
"""import plotly.express as px

df = px.data.iris()

fig = px.scatter_matrix(
    df,
    dimensions=['sepal_length','sepal_width','petal_length','petal_width'],
    color='species',
    symbol='species',
    title='Iris Dataset — Interactive Scatter Matrix',
    labels={col: col.replace('_',' ') for col in df.columns}
)
fig.update_traces(diagonal_visible=False, showupperhalf=False)
fig.update_layout(height=600)
fig.show()"""},
{"label": "Annotated heatmap with go.Heatmap", "code":
"""import plotly.graph_objects as go
import numpy as np

np.random.seed(3)
days    = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
hours   = [f'{h:02d}:00' for h in range(9, 18)]
z_data  = np.random.poisson(5, (len(days), len(hours))).astype(float)
# Simulate peak hours mid-day
z_data[:, 2:6] += np.random.poisson(8, (len(days), 4))

# Build annotation text
annotations = []
for i, day in enumerate(days):
    for j, hr in enumerate(hours):
        annotations.append(dict(
            x=hr, y=day,
            text=str(int(z_data[i, j])),
            font=dict(color='white' if z_data[i, j] > 10 else 'black', size=11),
            showarrow=False,
        ))

fig = go.Figure(data=go.Heatmap(
    z=z_data, x=hours, y=days,
    colorscale='YlOrRd',
    hoverongaps=False,
))
fig.update_layout(
    title='Support Tickets: Day × Hour (with annotations)',
    annotations=annotations,
    height=380,
    xaxis_title='Hour', yaxis_title='Day',
)
fig.show()"""},
{"label": "Custom colorscale heatmap — monthly sales grid", "code":
"""import plotly.graph_objects as go
import numpy as np

np.random.seed(8)
products = ['Widget', 'Gadget', 'Gizmo', 'Doohickey', 'Thingamajig']
months   = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Simulate seasonal sales data
z = np.random.uniform(20, 100, (len(products), len(months)))
# Add seasonality: Q4 boost
z[:, 9:] *= 1.4
# Add product-specific trends
z[0, :] += np.linspace(0, 20, 12)
z = z.round(1)

# Custom discrete colorscale: red -> yellow -> green
custom_scale = [
    [0.0,  '#d73027'],
    [0.25, '#f46d43'],
    [0.5,  '#ffffbf'],
    [0.75, '#74add1'],
    [1.0,  '#313695'],
]

# Build cell annotations
annotations = []
for i, prod in enumerate(products):
    for j, mon in enumerate(months):
        annotations.append(dict(
            x=mon, y=prod,
            text=str(int(z[i, j])),
            showarrow=False,
            font=dict(size=9,
                      color='white' if z[i, j] > 75 or z[i, j] < 35 else 'black'),
        ))

fig = go.Figure(data=go.Heatmap(
    z=z, x=months, y=products,
    colorscale=custom_scale,
    colorbar=dict(title='Units Sold'),
    hovertemplate='Product: %{y}<br>Month: %{x}<br>Sales: %{z}<extra></extra>',
))
fig.update_layout(
    title='Monthly Sales Heatmap — Custom Colorscale',
    annotations=annotations,
    height=380,
    xaxis_title='Month',
    yaxis_title='Product',
)
fig.show()
print("Peak month:", months[int(z.sum(axis=0).argmax())])
print("Top product:", products[int(z.sum(axis=1).argmax())])"""}
],
"practice": {
"title": "Annotated Correlation Heatmap",
"desc": "Load px.data.iris() and compute the correlation matrix of the four numeric columns. Use px.imshow with text_auto='.2f', the RdBu_r colorscale, and zmin=-1/zmax=1. Then build a second heatmap using go.Heatmap directly, adding manual annotation text showing each correlation value. Compare the two approaches.",
"starter":
"""import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = px.data.iris()
cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
corr = df[cols].corr().round(2)

# 1. px.imshow version (easy)
# TODO: fig1 = px.imshow(
#     corr, text_auto='.2f',
#     color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
#     title='Iris Correlation Matrix (px.imshow)',
# )
# TODO: fig1.update_layout(height=420)
# TODO: fig1.show()

# 2. go.Heatmap version with manual annotations
z = corr.values
labels = corr.columns.tolist()
# TODO: annotations = []
# TODO: for i in range(len(labels)):
#     for j in range(len(labels)):
#         annotations.append(dict(
#             x=labels[j], y=labels[i],
#             text=str(z[i, j]),
#             showarrow=False,
#             font=dict(color='white' if abs(z[i,j]) > 0.5 else 'black'),
#         ))
# TODO: fig2 = go.Figure(data=go.Heatmap(
#     z=z, x=labels, y=labels,
#     colorscale='RdBu_r', zmin=-1, zmax=1,
# ))
# TODO: fig2.update_layout(title='Iris Correlation (go.Heatmap + annotations)',
#                          annotations=annotations, height=420)
# TODO: fig2.show()""",
"examples": [
{"label": "Interactive Treemap with Drill-Down", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
regions   = ['North America','Europe','Asia Pacific','Latin America']
countries = {
    'North America': ['USA','Canada','Mexico'],
    'Europe':        ['Germany','France','UK','Spain'],
    'Asia Pacific':  ['China','Japan','India','Australia'],
    'Latin America': ['Brazil','Argentina','Colombia'],
}
rows = []
for region, clist in countries.items():
    for country in clist:
        for product in ['Software','Hardware','Services']:
            rows.append({
                'region': region, 'country': country, 'product': product,
                'revenue': rng.uniform(50, 500),
                'growth':  rng.uniform(-10, 40),
            })

df = pd.DataFrame(rows)

fig = px.treemap(
    df,
    path=[px.Constant('Global'), 'region', 'country', 'product'],
    values='revenue',
    color='growth',
    color_continuous_scale='RdYlGn',
    color_continuous_midpoint=15,
    title='Global Revenue Treemap — Click to Drill Down',
    hover_data={'revenue': ':.1f', 'growth': ':.1f'},
)
fig.update_traces(textinfo='label+value+percent parent',
                  hovertemplate='<b>%{label}</b><br>Revenue: $%{value:.1f}M<br>Growth: %{color:.1f}%')
fig.update_layout(height=600, title_font_size=15,
                  coloraxis_colorbar=dict(title='Growth %'))
fig.show()"""},
{"label": "Sankey Diagram for Flow Analysis", "code":
"""import plotly.graph_objects as go

# Marketing funnel flow
labels = [
    'Website Visitors',  # 0
    'Ad Campaign',       # 1
    'Organic Search',    # 2
    'Social Media',      # 3
    'Product Page',      # 4
    'Add to Cart',       # 5
    'Checkout',          # 6
    'Purchased',         # 7
    'Abandoned',         # 8
]

source = [0, 0, 0, 1, 2, 3, 4, 5, 6]
target = [1, 2, 3, 4, 4, 4, 5, 6, 7]
value  = [3000, 5000, 2000, 2800, 4200, 1500, 4500, 2000, 2500]

link_colors = ['rgba(100,149,237,0.4)'] * len(source)
for i, t in enumerate(target):
    if t == 8:
        link_colors[i] = 'rgba(255,99,71,0.4)'

fig = go.Figure(go.Sankey(
    arrangement='snap',
    node=dict(
        pad=15, thickness=20,
        line=dict(color='white', width=0.5),
        label=labels,
        color=['#4a90d9','#5ab4ac','#d4b483','#8fc97e',
               '#feb24c','#f03b20','#43a2ca','#2ca25f','#ef5350'],
    ),
    link=dict(
        source=source, target=target, value=value,
        color=link_colors,
        hovertemplate='%{source.label} \u2192 %{target.label}: %{value:,}<extra></extra>',
    ),
))
fig.update_layout(title_text='Marketing Funnel \u2014 Sankey Diagram',
                  title_font_size=16, height=500, font_size=12,
                  template='plotly_white')
fig.show()"""},
{"label": "Bubble Chart with Time Slider", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
countries = ['USA','China','India','Germany','UK','France','Japan','Brazil','Canada','Australia']
years = range(2018, 2025)

rows = []
for country in countries:
    gdp   = rng.uniform(1000, 25000)
    pop   = rng.uniform(50, 1400)
    for year in years:
        rows.append({
            'country':    country,
            'year':       year,
            'gdp_growth': rng.normal(2.5, 1.5),
            'gdp_pc':     gdp * (1 + rng.normal(0.025, 0.01))**(year-2018),
            'population': pop + rng.normal(0, 2),
            'continent':  'Americas' if country in ['USA','Brazil','Canada'] else
                          'Europe'   if country in ['Germany','UK','France'] else
                          'Asia'     if country in ['China','India','Japan'] else 'Oceania',
        })

df = pd.DataFrame(rows)

fig = px.scatter(
    df, x='gdp_pc', y='gdp_growth',
    size='population', color='continent',
    animation_frame='year', animation_group='country',
    hover_name='country',
    log_x=True,
    size_max=55,
    color_discrete_sequence=px.colors.qualitative.Bold,
    title='GDP per Capita vs Growth Rate (2018\u20132024)',
    labels={'gdp_pc': 'GDP per Capita (USD, log)', 'gdp_growth': 'GDP Growth (%)'},
    range_x=[500, 40000], range_y=[-3, 8],
)
fig.update_layout(height=550, title_font_size=15)
fig.show()"""},
]
},
"rw": {
"title": "Operations Metrics Heatmap",
"scenario": "An operations manager visualizes a week × hour activity heatmap to identify peak load periods for staffing.",
"code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(7)
hours = list(range(24))
days  = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

# Simulate ticket volumes: high weekday business hours
data = np.random.poisson(3, (7, 24)).astype(float)
data[0:5, 9:18] += np.random.poisson(12, (5, 9))   # weekday 9-18
data[0:5, 0:6]  *= 0.3                              # overnight low
data[5:7, :]    *= 0.5                              # weekend lower

df = pd.DataFrame(data.round(0).astype(int),
                  index=days, columns=[f'{h:02d}:00' for h in hours])

fig = px.imshow(
    df,
    color_continuous_scale='YlOrRd',
    aspect='auto',
    title='Support Ticket Volume — Week × Hour Heatmap',
    labels=dict(x='Hour', y='Day', color='Tickets')
)
fig.update_xaxes(tickangle=45, tickmode='array',
                 tickvals=list(range(0,24,2)),
                 ticktext=[f'{h:02d}:00' for h in range(0,24,2)])
fig.update_layout(height=380)
fig.show()"""}
},

{
"title": "5. 3D Charts",
"desc": "Plotly renders true 3D scatter and surface plots in the browser. Drag to rotate, scroll to zoom.",
"examples": [
{"label": "3D scatter plot", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    'x':       np.random.randn(300),
    'y':       np.random.randn(300),
    'z':       np.random.randn(300),
    'cluster': np.random.choice(['A','B','C'], 300),
    'size':    np.random.uniform(5, 20, 300),
})
# Separate clusters
df.loc[df.cluster=='A','x'] += 2
df.loc[df.cluster=='B','y'] += 2
df.loc[df.cluster=='C','z'] += 2

fig = px.scatter_3d(df, x='x', y='y', z='z',
                    color='cluster', size='size',
                    opacity=0.7,
                    title='3D Cluster Visualization')
fig.update_layout(height=500)
fig.show()"""},
{"label": "3D surface plot", "code":
"""import plotly.graph_objects as go
import numpy as np

x = np.linspace(-3, 3, 60)
y = np.linspace(-3, 3, 60)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1*(X**2+Y**2))

fig = go.Figure(data=[
    go.Surface(z=Z, x=X, y=Y,
               colorscale='Viridis',
               contours=dict(z=dict(show=True, usecolormap=True,
                                    highlightcolor='white', project_z=True)))
])
fig.update_layout(
    title='3D Surface: Damped Sinc Function',
    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
    height=500
)
fig.show()"""},
{"label": "3D scatter with color scale and hover", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(99)
n = 500
# Spiral helix dataset
t = np.linspace(0, 4 * np.pi, n)
df = pd.DataFrame({
    'x':        np.cos(t) + np.random.randn(n) * 0.15,
    'y':        np.sin(t) + np.random.randn(n) * 0.15,
    'z':        t / (2 * np.pi),   # height increases with angle
    'intensity': np.sin(t) ** 2,
    'label':    [f'Point {i}' for i in range(n)],
})

fig = px.scatter_3d(
    df, x='x', y='y', z='z',
    color='intensity',
    color_continuous_scale='Plasma',
    hover_name='label',
    hover_data={'x': ':.2f', 'y': ':.2f', 'z': ':.2f'},
    opacity=0.75,
    title='3D Helix — Color by Intensity',
    size_max=6,
)
fig.update_traces(marker=dict(size=3))
fig.update_layout(height=520)
fig.show()"""},
{"label": "3D line plot and surface from meshgrid", "code":
"""import plotly.graph_objects as go
import numpy as np

# -- 3D line: double helix DNA-like structure --
t = np.linspace(0, 6 * np.pi, 300)
r = 1.5

fig = go.Figure()
# Strand 1
fig.add_trace(go.Scatter3d(
    x=r * np.cos(t), y=r * np.sin(t), z=t / np.pi,
    mode='lines',
    line=dict(color='#636EFA', width=5),
    name='Strand 1',
))
# Strand 2 (180 degrees offset)
fig.add_trace(go.Scatter3d(
    x=r * np.cos(t + np.pi), y=r * np.sin(t + np.pi), z=t / np.pi,
    mode='lines',
    line=dict(color='#EF553B', width=5),
    name='Strand 2',
))
# Rungs (every 15th point)
step = 15
for i in range(0, len(t), step):
    fig.add_trace(go.Scatter3d(
        x=[r*np.cos(t[i]), r*np.cos(t[i]+np.pi)],
        y=[r*np.sin(t[i]), r*np.sin(t[i]+np.pi)],
        z=[t[i]/np.pi, t[i]/np.pi],
        mode='lines',
        line=dict(color='#aaa', width=2),
        showlegend=False,
    ))

# -- 3D surface: saddle function z = x^2 - y^2 --
xs = np.linspace(-2, 2, 40)
ys = np.linspace(-2, 2, 40)
Xs, Ys = np.meshgrid(xs, ys)
Zs = Xs**2 - Ys**2

fig2 = go.Figure(data=[go.Surface(
    x=Xs, y=Ys, z=Zs,
    colorscale='RdBu',
    colorbar=dict(title='z = x²-y²'),
)])
fig2.update_layout(
    title='3D Saddle Surface (z = x² - y²)',
    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
    height=480,
)

fig.update_layout(
    title='3D Double Helix Line Plot',
    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Turn'),
    height=520,
    showlegend=True,
)
fig.show()
fig2.show()
print("Double helix: 2 strands, rungs every 15 points")
print("Saddle surface grid:", Xs.shape)"""}
],
"practice": {
"title": "3D Scatter with Size, Color, and Hover",
"desc": "Create a 3D scatter plot of 400 random points in three clusters separated along all three axes. Color by cluster label, size the markers by a 'confidence' column (random 5-20), and add meaningful hover_data. Print a summary of how many points are in each cluster.",
"starter":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
n_per = 133

# Build three clusters
def make_cluster(cx, cy, cz, label, n):
    return pd.DataFrame({
        'x': np.random.randn(n) + cx,
        'y': np.random.randn(n) + cy,
        'z': np.random.randn(n) + cz,
        'cluster': label,
        'confidence': np.random.uniform(5, 20, n).round(1),
    })

# TODO: df = pd.concat([
#     make_cluster(0, 0, 0, 'Alpha', n_per),
#     make_cluster(4, 0, 0, 'Beta',  n_per),
#     make_cluster(2, 4, 2, 'Gamma', n_per),
# ], ignore_index=True)

# Print cluster summary
# TODO: print(df.groupby('cluster')[['x','y','z']].mean().round(2))

# TODO: fig = px.scatter_3d(
#     df, x='x', y='y', z='z',
#     color='cluster', size='confidence',
#     hover_data={'confidence': True, 'x': ':.2f', 'y': ':.2f', 'z': ':.2f'},
#     opacity=0.75,
#     title='3D Cluster Scatter — Size by Confidence',
# )
# TODO: fig.update_layout(height=520)
# TODO: fig.show()"""
},
"rw": {
"title": "3D Risk Surface for Options Pricing",
"scenario": "A quant visualizes how an option's price changes with underlying price and time-to-expiry using a 3D surface.",
"code":
"""import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    # Avoid division by zero
    T = np.where(T < 1e-6, 1e-6, T)
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

K     = 100      # strike price
r     = 0.05     # risk-free rate
sigma = 0.20     # volatility

S_vals = np.linspace(70, 130, 50)   # underlying price
T_vals = np.linspace(0.02, 1.0, 50) # time to expiry (years)
S_grid, T_grid = np.meshgrid(S_vals, T_vals)
C_grid = black_scholes_call(S_grid, K, T_grid, r, sigma)

fig = go.Figure(data=[go.Surface(
    x=S_grid, y=T_grid, z=C_grid,
    colorscale='Plasma',
    colorbar=dict(title='Call Price ($)')
)])
fig.update_layout(
    title=f'Black-Scholes Call Option Price  (K={K}, σ={sigma})',
    scene=dict(
        xaxis_title='Underlying Price (S)',
        yaxis_title='Time to Expiry (T)',
        zaxis_title='Call Price ($)',
    ),
    height=520
)
fig.show()"""}
},

{
"title": "6. Subplots with make_subplots",
"desc": "make_subplots creates multi-panel figures. Mix chart types, share axes, and control spacing — all in one interactive figure.",
"examples": [
{"label": "2×2 subplot grid", "code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

np.random.seed(5)
x = np.linspace(0, 10, 100)

fig = make_subplots(rows=2, cols=2,
                    subplot_titles=['Line','Bar','Scatter','Histogram'])

fig.add_trace(go.Scatter(x=x, y=np.sin(x), name='sin'), row=1, col=1)
fig.add_trace(go.Bar(x=['A','B','C','D'], y=[4,7,3,8], name='bar'), row=1, col=2)
fig.add_trace(go.Scatter(x=np.random.randn(100), y=np.random.randn(100),
                         mode='markers', name='scatter',
                         marker=dict(opacity=0.5)), row=2, col=1)
fig.add_trace(go.Histogram(x=np.random.randn(500), name='hist'), row=2, col=2)

fig.update_layout(title='Multi-Type Dashboard', height=500, showlegend=False)
fig.show()"""},
{"label": "Shared x-axis — price + volume", "code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

np.random.seed(9)
dates  = pd.date_range('2024-01-01', periods=60, freq='B')
price  = 100 + np.cumsum(np.random.randn(60) * 1.5)
volume = np.random.randint(1000, 8000, 60)
colors = ['green' if price[i] >= price[i-1] else 'red' for i in range(len(price))]

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    row_heights=[0.7, 0.3],
                    vertical_spacing=0.03)

fig.add_trace(go.Scatter(x=dates, y=price, name='Price',
                         line=dict(color='royalblue', width=2)), row=1, col=1)
fig.add_trace(go.Bar(x=dates, y=volume, name='Volume',
                     marker_color=colors, opacity=0.7), row=2, col=1)

fig.update_layout(title='Stock Price & Volume', height=500, showlegend=False)
fig.update_xaxes(rangeslider_visible=False)
fig.show()"""},
{"label": "2×2 grid with mixed chart types and shared axes", "code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

np.random.seed(11)
x = np.linspace(0, 2 * np.pi, 80)
dates = pd.date_range('2024-01', periods=12, freq='MS')
revenue = 50 + np.cumsum(np.random.randn(12) * 4)
categories = ['Q1', 'Q2', 'Q3', 'Q4']
vals_a = [22, 35, 28, 41]
vals_b = [18, 29, 33, 37]

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=['Sine & Cosine Waves', 'Monthly Revenue',
                    'Grouped Bar by Quarter', 'Normal Distribution'],
    vertical_spacing=0.12, horizontal_spacing=0.1,
)

# Row 1, Col 1: Two line traces
fig.add_trace(go.Scatter(x=x, y=np.sin(x), name='sin',
                         line=dict(color='#636EFA')), row=1, col=1)
fig.add_trace(go.Scatter(x=x, y=np.cos(x), name='cos',
                         line=dict(color='#EF553B', dash='dash')), row=1, col=1)

# Row 1, Col 2: Area chart
fig.add_trace(go.Scatter(x=dates, y=revenue.round(1), fill='tozeroy',
                         line=dict(color='#00CC96'), name='Revenue'), row=1, col=2)

# Row 2, Col 1: Grouped bars
fig.add_trace(go.Bar(x=categories, y=vals_a, name='Product A',
                     marker_color='#AB63FA'), row=2, col=1)
fig.add_trace(go.Bar(x=categories, y=vals_b, name='Product B',
                     marker_color='#FFA15A'), row=2, col=1)

# Row 2, Col 2: Histogram
fig.add_trace(go.Histogram(x=np.random.randn(400), nbinsx=25,
                            marker_color='#19D3F3', name='Normal'), row=2, col=2)

fig.update_layout(title='Multi-Panel Dashboard', height=580,
                  barmode='group', showlegend=True,
                  legend=dict(orientation='h', y=-0.08))
fig.show()"""},
{"label": "Bar + Line + Scatter in shared-axis subplots", "code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

np.random.seed(17)
months = pd.date_range('2024-01', periods=12, freq='MS')
sales    = np.random.randint(30, 100, 12)
target   = np.full(12, 70)
cum_sales = sales.cumsum()
margin_pct = np.random.uniform(0.15, 0.45, 12).round(3)

# 3 rows: bar chart, line overlay, scatter — all share x-axis
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    row_heights=[0.5, 0.25, 0.25],
    vertical_spacing=0.05,
    subplot_titles=['Monthly Sales vs Target',
                    'Cumulative Sales',
                    'Margin %'],
)

# Row 1: Bar (actual) + Line (target)
bar_colors = ['#00CC96' if s >= 70 else '#EF553B' for s in sales]
fig.add_trace(go.Bar(x=months, y=sales, name='Actual',
                     marker_color=bar_colors), row=1, col=1)
fig.add_trace(go.Scatter(x=months, y=target, name='Target',
                         line=dict(color='white', dash='dash', width=2),
                         mode='lines'), row=1, col=1)

# Row 2: Cumulative area line
fig.add_trace(go.Scatter(x=months, y=cum_sales, fill='tozeroy',
                         name='Cumulative', line=dict(color='#636EFA')), row=2, col=1)

# Row 3: Scatter dots for margin
fig.add_trace(go.Scatter(x=months, y=(margin_pct * 100).round(1),
                         mode='markers+lines', name='Margin %',
                         marker=dict(color='#AB63FA', size=8),
                         line=dict(color='#AB63FA', width=1.5)), row=3, col=1)
fig.add_hline(y=30, line_dash='dot', line_color='gray',
              annotation_text='30% target', row=3, col=1)

fig.update_layout(
    title='Sales Performance — Bar + Line + Scatter Subplots',
    height=600, showlegend=True,
    legend=dict(orientation='h', y=-0.06),
    template='plotly_dark',
)
fig.update_xaxes(rangeslider_visible=False)
fig.show()
print("Traces:", [t.type for t in fig.data])
print("Total sales:", int(cum_sales[-1]))"""}
],
"practice": {
"title": "2×2 Subplot Grid",
"desc": "Build a 2x2 subplot figure using make_subplots. Panel (1,1): a scatter of random points colored by a third variable. Panel (1,2): a bar chart of 5 category totals. Panel (2,1): a line with fill='tozeroy' for a time series. Panel (2,2): a histogram of 300 normal values. Give each panel a subtitle and set overall height=550.",
"starter":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

np.random.seed(42)

# TODO: fig = make_subplots(
#     rows=2, cols=2,
#     subplot_titles=['Random Scatter', 'Category Totals',
#                     'Time Series', 'Distribution'],
# )

# Panel (1,1): scatter with color (use marker colorscale)
x1 = np.random.randn(100)
y1 = np.random.randn(100)
c1 = np.random.randn(100)
# TODO: fig.add_trace(go.Scatter(x=x1, y=y1, mode='markers',
#     marker=dict(color=c1, colorscale='Viridis', showscale=False),
#     name='scatter'), row=1, col=1)

# Panel (1,2): bar chart
cats = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
vals = np.random.randint(10, 80, 5)
# TODO: fig.add_trace(go.Bar(x=cats, y=vals, name='totals',
#     marker_color='#636EFA'), row=1, col=2)

# Panel (2,1): area line
dates = pd.date_range('2024-01', periods=24, freq='MS')
ts = 100 + np.cumsum(np.random.randn(24) * 3)
# TODO: fig.add_trace(go.Scatter(x=dates, y=ts.round(1), fill='tozeroy',
#     line=dict(color='#00CC96'), name='series'), row=2, col=1)

# Panel (2,2): histogram
# TODO: fig.add_trace(go.Histogram(x=np.random.randn(300), nbinsx=20,
#     marker_color='#EF553B', name='hist'), row=2, col=2)

# TODO: fig.update_layout(title='My 2x2 Dashboard', height=550, showlegend=False)
# TODO: fig.show()"""
},
"rw": {
"title": "Marketing Analytics Dashboard",
"scenario": "A growth team builds a 4-panel Plotly dashboard showing funnel, revenue trend, channel mix, and conversion by cohort.",
"code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

np.random.seed(3)
months  = pd.date_range('2024-01', periods=12, freq='MS')
revenue = 100 + np.cumsum(np.random.randn(12)*8) + np.arange(12)*5
sessions= np.random.randint(8000, 20000, 12)
cvr     = revenue / sessions * 100

channels = ['Organic','Paid','Social','Email','Direct']
ch_vals  = [35, 25, 18, 12, 10]

funnel_stages  = ['Visit','Sign Up','Trial','Paid']
funnel_vals    = [10000, 3200, 1100, 420]

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=['Revenue Trend ($K)', 'Traffic by Channel',
                    'Conversion Funnel', 'CVR vs Sessions'],
    specs=[[{},{}],[{},{}]]
)

# Revenue
fig.add_trace(go.Scatter(x=months, y=revenue.round(1), fill='tozeroy',
                         line=dict(color='#636EFA'), name='Revenue'), row=1, col=1)

# Channel pie — use domain trace
fig.add_trace(go.Pie(labels=channels, values=ch_vals, hole=0.35,
                     showlegend=False, textinfo='label+percent'), row=1, col=2)

# Funnel
fig.add_trace(go.Funnel(y=funnel_stages, x=funnel_vals,
                        marker_color=['#636EFA','#EF553B','#00CC96','#AB63FA'],
                        textinfo='value+percent initial'), row=2, col=1)

# CVR vs Sessions scatter
fig.add_trace(go.Scatter(x=sessions, y=cvr.round(3), mode='markers+text',
                         text=[m.strftime('%b') for m in months],
                         textposition='top center',
                         marker=dict(size=10, color='#FFA15A')), row=2, col=2)

fig.update_layout(title='Growth Dashboard — 2024', height=650)
fig.show()"""}
},

{
"title": "7. Customizing Layout & Traces",
"desc": "update_layout() controls the figure-level design. update_traces() modifies all traces at once. Both accept selector filtering.",
"examples": [
{"label": "update_layout — theme and fonts", "code":
"""import plotly.express as px
import plotly.graph_objects as go

df = px.data.gapminder().query("year == 2007 and continent == 'Europe'")

fig = px.scatter(df, x='gdpPercap', y='lifeExp',
                 size='pop', color='country',
                 hover_name='country', log_x=True)

fig.update_layout(
    title=dict(text='Europe 2007: GDP vs Life Expectancy',
               font=dict(size=16, color='white'), x=0.5),
    plot_bgcolor='#1a1a2e',
    paper_bgcolor='#16213e',
    font=dict(color='#e0e0e0'),
    xaxis=dict(gridcolor='#333', title='GDP per Capita (log)'),
    yaxis=dict(gridcolor='#333', title='Life Expectancy'),
    showlegend=False,
    height=450,
)
fig.show()"""},
{"label": "update_traces and add_shape", "code":
"""import plotly.express as px
import plotly.graph_objects as go
import numpy as np

np.random.seed(1)
x = np.arange(1, 13)
y = 80 + np.cumsum(np.random.randn(12) * 5)

fig = px.line(x=x, y=y, markers=True,
              title='Monthly Revenue with Target Zone')

# Customise the line trace
fig.update_traces(
    line=dict(color='#00CC96', width=3),
    marker=dict(size=9, color='white',
                line=dict(color='#00CC96', width=2))
)

# Add target band (rectangle shape)
fig.add_hrect(y0=90, y1=110, fillcolor='rgba(100,200,100,0.1)',
              line_width=0, annotation_text='Target range')
fig.add_hline(y=100, line_dash='dot', line_color='gray',
              annotation_text='Target')

fig.update_layout(xaxis_title='Month', yaxis_title='Revenue ($K)')
fig.show()"""},
{"label": "Custom color palette, annotations, and template", "code":
"""import plotly.graph_objects as go
import plotly.express as px
import numpy as np

np.random.seed(5)
categories = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
q1 = np.random.randint(30, 90, 5)
q2 = np.random.randint(30, 90, 5)

fig = go.Figure()
fig.add_trace(go.Bar(x=categories, y=q1, name='Q1',
                     marker_color='#636EFA'))
fig.add_trace(go.Bar(x=categories, y=q2, name='Q2',
                     marker_color='#EF553B'))

# Annotate the tallest Q2 bar
peak_idx = int(np.argmax(q2))
fig.add_annotation(
    x=categories[peak_idx], y=q2[peak_idx] + 4,
    text=f'Peak Q2: {q2[peak_idx]}',
    showarrow=True, arrowhead=2,
    font=dict(color='#EF553B', size=12),
)

# Reference line for target
fig.add_hline(y=70, line_dash='dash', line_color='gray',
              annotation_text='Target 70', annotation_position='right')

fig.update_layout(
    title='Q1 vs Q2 Sales by Product',
    barmode='group',
    template='plotly_dark',
    height=420,
    legend=dict(orientation='h', y=1.05),
    yaxis_title='Sales ($K)',
)
fig.show()"""},
{"label": "Interactive updatemenus — dropdown to switch chart view", "code":
"""import plotly.graph_objects as go
import numpy as np

np.random.seed(13)
categories = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta']
q1 = np.random.randint(20, 100, 6)
q2 = np.random.randint(20, 100, 6)
q3 = np.random.randint(20, 100, 6)
q4 = np.random.randint(20, 100, 6)

# All four quarter traces — only Q1 visible by default
quarters_data = [
    go.Bar(x=categories, y=q1, name='Q1', marker_color='#636EFA', visible=True),
    go.Bar(x=categories, y=q2, name='Q2', marker_color='#EF553B', visible=False),
    go.Bar(x=categories, y=q3, name='Q3', marker_color='#00CC96', visible=False),
    go.Bar(x=categories, y=q4, name='Q4', marker_color='#AB63FA', visible=False),
]
fig = go.Figure(data=quarters_data)

# Dropdown buttons — each shows only one quarter
buttons = []
for i, label in enumerate(['Q1', 'Q2', 'Q3', 'Q4']):
    vis = [j == i for j in range(4)]
    buttons.append(dict(
        label=label,
        method='update',
        args=[{'visible': vis},
              {'title': f'{label} Sales by Product',
               'yaxis': {'title': f'{label} Revenue ($K)'}}],
    ))

fig.update_layout(
    title='Q1 Sales by Product',
    yaxis_title='Q1 Revenue ($K)',
    height=420,
    template='plotly_dark',
    updatemenus=[dict(
        type='dropdown',
        direction='down',
        x=0.01, y=1.12, xanchor='left',
        showactive=True,
        buttons=buttons,
        bgcolor='#1e293b',
        bordercolor='#475569',
        font=dict(color='white'),
    )],
    annotations=[dict(text='Select Quarter:', x=0, y=1.16,
                      xref='paper', yref='paper',
                      showarrow=False, font=dict(color='#94a3b8'))],
)
fig.show()
print("Dropdown buttons:", len(buttons))
print("Available quarters: Q1, Q2, Q3, Q4")"""}
],
"practice": {
"title": "Branded Dark-Theme KPI Chart",
"desc": "Create a go.Figure with two traces: a Bar for actual monthly revenue (12 months, random 50-120) and a Scatter line for the monthly target (fixed at 80). Apply a full dark theme using update_layout (plot_bgcolor, paper_bgcolor, font color, grid color). Add an annotation at the month with the highest revenue. Add an add_hline for the target. Set a centered title.",
"starter":
"""import plotly.graph_objects as go
import numpy as np

np.random.seed(7)
months  = ['Jan','Feb','Mar','Apr','May','Jun',
           'Jul','Aug','Sep','Oct','Nov','Dec']
revenue = np.random.randint(50, 121, 12)
target  = np.full(12, 80)

fig = go.Figure()

# Bar trace for actual revenue
# TODO: fig.add_trace(go.Bar(
#     x=months, y=revenue, name='Actual',
#     marker_color=['#00CC96' if r >= 80 else '#EF553B' for r in revenue],
# ))

# Line trace for target
# TODO: fig.add_trace(go.Scatter(
#     x=months, y=target, name='Target',
#     line=dict(color='white', dash='dash', width=2), mode='lines',
# ))

# Annotation at peak month
# TODO: peak = int(np.argmax(revenue))
# TODO: fig.add_annotation(
#     x=months[peak], y=revenue[peak] + 3,
#     text=f'Peak: {revenue[peak]}',
#     showarrow=True, arrowhead=2,
#     font=dict(color='#00CC96', size=12),
# )

# Dark theme layout
# TODO: fig.update_layout(
#     title=dict(text='Monthly Revenue vs Target', x=0.5,
#                font=dict(size=15, color='white')),
#     plot_bgcolor='#111827', paper_bgcolor='#0f172a',
#     font=dict(color='#cbd5e1'),
#     xaxis=dict(gridcolor='#1e293b'),
#     yaxis=dict(gridcolor='#1e293b', title='Revenue ($K)'),
#     barmode='overlay', height=430,
# )
# TODO: fig.show()"""
},
"rw": {
"title": "Branded Executive KPI Chart",
"scenario": "A BI developer creates a dark-themed, branded interactive chart for the C-suite weekly review email.",
"code":
"""import plotly.graph_objects as go
import pandas as pd
import numpy as np

np.random.seed(42)
months  = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
revenue = np.array([4.2,3.8,5.1,5.8,6.2,7.0,6.5,7.8,8.1,7.5,9.2,10.4])
target  = np.full(12, 6.0)
prev_yr = revenue * np.random.uniform(0.75, 0.95, 12)

fig = go.Figure()

# Previous year (subtle background)
fig.add_trace(go.Bar(x=months, y=prev_yr, name='2023',
                     marker_color='rgba(100,100,180,0.3)', showlegend=True))

# Current year bars
fig.add_trace(go.Bar(x=months, y=revenue, name='2024',
                     marker_color=['#00CC96' if r>=t else '#EF553B'
                                   for r,t in zip(revenue, target)]))

# Target line
fig.add_trace(go.Scatter(x=months, y=target, name='Target',
                         line=dict(color='white', dash='dash', width=2),
                         mode='lines'))

# YoY growth annotations
for i, (m, r, p) in enumerate(zip(months, revenue, prev_yr)):
    yoy = (r-p)/p*100
    fig.add_annotation(x=m, y=r+0.15, text=f'+{yoy:.0f}%',
                       font=dict(size=8, color='#aaa'), showarrow=False)

fig.update_layout(
    title=dict(text='2024 Monthly Revenue ($M) vs Target & Prior Year',
               font=dict(size=15, color='white'), x=0.5),
    barmode='overlay',
    plot_bgcolor='#111827', paper_bgcolor='#0f172a',
    font=dict(color='#cbd5e1'),
    xaxis=dict(gridcolor='#1e293b'),
    yaxis=dict(gridcolor='#1e293b', title='Revenue ($M)'),
    legend=dict(orientation='h', y=1.08),
    height=460,
)
fig.show()"""}
},

{
"title": "8. Animated Charts",
"desc": "animation_frame adds a play button to animate over a variable (e.g. year, month). Great for showing trends over time.",
"examples": [
{"label": "Animated bubble chart", "code":
"""import plotly.express as px

# Classic animated gapminder chart
df = px.data.gapminder()

fig = px.scatter(
    df, x='gdpPercap', y='lifeExp',
    animation_frame='year',
    animation_group='country',
    size='pop', color='continent',
    hover_name='country',
    log_x=True, size_max=55,
    range_x=[100, 100000], range_y=[25, 90],
    title='World Development 1952–2007',
    labels={'gdpPercap': 'GDP per Capita', 'lifeExp': 'Life Expectancy'},
)
fig.update_layout(height=520)
fig.show()"""},
{"label": "Animated bar chart race", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
products = ['Widget', 'Gadget', 'Doohickey', 'Gizmo', 'Thingamajig']
quarters = ['Q1','Q2','Q3','Q4']

rows = []
sales = {p: np.random.uniform(50, 200) for p in products}
for q in quarters:
    for p in products:
        sales[p] += np.random.uniform(-20, 40)
        rows.append({'quarter': q, 'product': p, 'sales': max(sales[p], 10)})
df = pd.DataFrame(rows)

fig = px.bar(df, x='sales', y='product',
             animation_frame='quarter',
             orientation='h',
             color='product',
             range_x=[0, 400],
             title='Product Sales Race by Quarter',
             labels={'sales': 'Cumulative Sales ($K)'},
             color_discrete_sequence=px.colors.qualitative.Bold)
fig.update_layout(showlegend=False, height=380)
fig.show()"""},
{"label": "Animated scatter with custom transition speed", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(3)
years = list(range(2015, 2026))
regions = ['North', 'South', 'East', 'West']

rows = []
for region in regions:
    revenue = np.random.uniform(80, 120)
    customers = np.random.randint(500, 2000)
    for yr in years:
        revenue    += np.random.uniform(-5, 12)
        customers  += np.random.randint(-50, 150)
        rows.append({
            'year':      yr,
            'region':    region,
            'revenue':   round(revenue, 1),
            'customers': max(customers, 100),
            'margin':    round(np.random.uniform(0.1, 0.4), 2),
        })
df = pd.DataFrame(rows)

fig = px.scatter(
    df, x='customers', y='revenue',
    animation_frame='year', animation_group='region',
    color='region', size='margin', size_max=40,
    hover_name='region', hover_data=['margin'],
    range_x=[0, 4000], range_y=[50, 250],
    title='Revenue vs Customers by Region (Animated 2015-2025)',
    labels={'revenue': 'Revenue ($K)', 'customers': 'Active Customers'},
)
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 400
fig.update_layout(height=480)
fig.show()"""},
{"label": "Animated line chart with frames and sliders", "code":
"""import plotly.graph_objects as go
import numpy as np

np.random.seed(22)
n_frames = 20
x = np.linspace(0, 4 * np.pi, 200)

# Each frame reveals more of the wave, with noise that changes each step
frames = []
for k in range(1, n_frames + 1):
    end = int(len(x) * k / n_frames)
    noise = np.random.randn(end) * 0.15
    y = np.sin(x[:end]) * np.exp(-x[:end] * 0.08) + noise
    frames.append(go.Frame(
        data=[go.Scatter(x=x[:end], y=y,
                         mode='lines',
                         line=dict(color='#636EFA', width=2))],
        name=str(k),
        layout=go.Layout(title_text=f'Damped Wave — Step {k}/{n_frames}'),
    ))

# Initial trace (first frame)
y0 = np.sin(x[:1]) * np.exp(-x[:1] * 0.08)
fig = go.Figure(
    data=[go.Scatter(x=x[:1], y=y0, mode='lines',
                     line=dict(color='#636EFA', width=2))],
    frames=frames,
)

# Play/Pause buttons + slider
fig.update_layout(
    title='Animated Damped Wave — Frames & Slider',
    xaxis=dict(range=[0, 4*np.pi], title='x'),
    yaxis=dict(range=[-1.3, 1.3], title='Amplitude'),
    height=460,
    updatemenus=[dict(
        type='buttons', showactive=False,
        y=1.05, x=0, xanchor='left',
        buttons=[
            dict(label='Play',
                 method='animate',
                 args=[None, {'frame': {'duration': 120, 'redraw': True},
                              'fromcurrent': True}]),
            dict(label='Pause',
                 method='animate',
                 args=[[None], {'frame': {'duration': 0},
                                'mode': 'immediate'}]),
        ],
    )],
    sliders=[dict(
        steps=[dict(method='animate', args=[[str(k)],
               {'mode': 'immediate', 'frame': {'duration': 120}}],
               label=str(k)) for k in range(1, n_frames+1)],
        transition=dict(duration=80),
        x=0, y=0, len=1.0,
        currentvalue=dict(prefix='Step: ', visible=True),
    )],
)
fig.show()
print(f"Total frames: {len(fig.frames)}")"""}
],
"practice": {
"title": "Animated Geographic Scatter",
"desc": "Using px.data.gapminder(), create an animated choropleth map (px.choropleth) with animation_frame='year', coloring countries by lifeExp. Set range_color=[30, 85], use the RdYlGn colorscale, and add hover_data for gdpPercap and pop. Print the number of unique years in the animation.",
"starter":
"""import plotly.express as px

df = px.data.gapminder()

# Print unique years that will be animation frames
# TODO: years = sorted(df['year'].unique())
# TODO: print(f"Animation frames: {len(years)} years from {years[0]} to {years[-1]}")

# Build animated choropleth
# TODO: fig = px.choropleth(
#     df,
#     locations='iso_alpha',
#     color='lifeExp',
#     hover_name='country',
#     hover_data=['gdpPercap', 'pop'],
#     animation_frame='year',
#     color_continuous_scale='RdYlGn',
#     range_color=[30, 85],
#     title='World Life Expectancy 1952-2007 (Animated)',
#     labels={'lifeExp': 'Life Expectancy'},
# )
# TODO: fig.update_layout(height=500,
#     coloraxis_colorbar=dict(title='Life Exp (years)'))
# TODO: fig.show()"""
},
"rw": {
"title": "Global CO2 Emissions Animation",
"scenario": "An environmental analyst animates per-capita CO2 emissions vs GDP across countries and decades for a policy presentation.",
"code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(10)
countries  = ['US','China','India','Germany','Brazil','UK','Japan','France','Canada','Australia']
continents = ['Americas','Asia','Asia','Europe','Americas','Europe','Asia','Europe','Americas','Oceania']
years      = list(range(1990, 2025, 5))

rows = []
for i, (c, cont) in enumerate(zip(countries, continents)):
    gdp  = np.random.uniform(5000, 60000)
    co2  = np.random.uniform(2, 16)
    pop  = np.random.uniform(20, 1400)
    for yr in years:
        gdp  *= np.random.uniform(1.01, 1.05)
        co2  *= np.random.uniform(0.97, 1.02)
        rows.append({'country':c,'continent':cont,'year':yr,
                     'gdp_pc':round(gdp,0),'co2_pc':round(co2,2),'pop':round(pop,1)})

df = pd.DataFrame(rows)

fig = px.scatter(
    df, x='gdp_pc', y='co2_pc',
    animation_frame='year', animation_group='country',
    size='pop', color='continent',
    hover_name='country',
    log_x=True, size_max=45,
    range_x=[3000, 120000], range_y=[0, 20],
    title='CO2 Emissions vs GDP per Capita (1990–2024)',
    labels={'gdp_pc': 'GDP per Capita ($, log)', 'co2_pc': 'CO2 per Capita (tonnes)'},
)
fig.update_layout(height=520)
fig.show()"""}
},

{
"title": "9. Maps & Geographic Charts",
"desc": "px.choropleth and px.scatter_geo create world or country-level maps. px.scatter_mapbox uses tile maps for city-level data.",
"examples": [
{"label": "Choropleth world map", "code":
"""import plotly.express as px

df = px.data.gapminder().query("year == 2007")

fig = px.choropleth(
    df, locations='iso_alpha',
    color='lifeExp',
    hover_name='country',
    hover_data=['gdpPercap', 'pop'],
    color_continuous_scale='RdYlGn',
    range_color=[40, 85],
    title='Life Expectancy by Country (2007)',
    labels={'lifeExp': 'Life Expectancy'}
)
fig.update_layout(height=480, coloraxis_colorbar=dict(title='Years'))
fig.show()"""},
{"label": "Scatter map — US cities", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(7)
cities = pd.DataFrame({
    'city':    ['New York','Los Angeles','Chicago','Houston','Phoenix',
                'Philadelphia','San Antonio','San Diego','Dallas','San Jose'],
    'lat':     [40.71,34.05,41.88,29.76,33.45,39.95,29.42,32.72,32.78,37.34],
    'lon':     [-74.01,-118.24,-87.63,-95.37,-112.07,-75.16,-98.49,-117.16,-96.80,-121.89],
    'revenue': np.random.uniform(50, 500, 10).round(1),
    'customers':np.random.randint(1000, 50000, 10),
})

fig = px.scatter_geo(cities, lat='lat', lon='lon',
                     size='revenue', color='revenue',
                     hover_name='city',
                     hover_data=['customers'],
                     color_continuous_scale='Reds',
                     scope='usa',
                     title='US Market Revenue by City')
fig.update_layout(height=430)
fig.show()"""},
{"label": "Bubble map on a natural earth projection", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(21)
# Major world cities with lat/lon
cities = pd.DataFrame({
    'city':    ['New York','London','Tokyo','Sydney','Sao Paulo',
                'Mumbai','Cairo','Lagos','Moscow','Beijing'],
    'country': ['USA','UK','Japan','Australia','Brazil',
                'India','Egypt','Nigeria','Russia','China'],
    'lat':     [40.71, 51.51, 35.68, -33.87, -23.55,
                19.08, 30.04,  6.52,  55.75,  39.91],
    'lon':     [-74.01, -0.13, 139.69, 151.21, -46.63,
                 72.88,  31.24,  3.40,  37.62, 116.41],
    'gdp_bn':  np.random.uniform(100, 800, 10).round(1),
    'pop_m':   np.random.uniform(5, 35, 10).round(1),
})

fig = px.scatter_geo(
    cities, lat='lat', lon='lon',
    size='gdp_bn', color='gdp_bn',
    hover_name='city', hover_data=['country', 'pop_m'],
    color_continuous_scale='Plasma',
    projection='natural earth',
    title='World City GDP — Bubble Map',
    labels={'gdp_bn': 'GDP ($B)'},
    size_max=40,
)
fig.update_layout(height=450)
fig.show()"""},
{"label": "px.scatter_mapbox — open-street tile map", "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(33)
# Sample delivery locations across a city (centred on Chicago)
n = 60
lat_center, lon_center = 41.88, -87.63
deliveries = pd.DataFrame({
    'id':       [f'DEL-{i:03d}' for i in range(n)],
    'lat':      lat_center + np.random.randn(n) * 0.08,
    'lon':      lon_center + np.random.randn(n) * 0.12,
    'status':   np.random.choice(['Delivered', 'In Transit', 'Failed'], n,
                                  p=[0.65, 0.25, 0.10]),
    'packages': np.random.randint(1, 20, n),
    'duration': np.random.uniform(5, 60, n).round(1),
})

color_map = {'Delivered': '#00CC96', 'In Transit': '#636EFA', 'Failed': '#EF553B'}

fig = px.scatter_mapbox(
    deliveries,
    lat='lat', lon='lon',
    color='status',
    size='packages',
    size_max=20,
    hover_name='id',
    hover_data={'packages': True, 'duration': ':.1f', 'lat': False, 'lon': False},
    color_discrete_map=color_map,
    zoom=11,
    center={'lat': lat_center, 'lon': lon_center},
    title='Delivery Status Map — Chicago (Open-Street Tiles)',
    mapbox_style='open-street-map',
)
fig.update_layout(height=520, legend_title_text='Status')
fig.show()
status_counts = deliveries['status'].value_counts()
print("Delivery summary:")
for status, count in status_counts.items():
    print(f"  {status}: {count}")"""}
],
"practice": {
"title": "Geographic Scatter Plot",
"desc": "Build a px.scatter_geo bubble map of at least 8 world cities. Each bubble should represent a metric of your choice (e.g., revenue, population). Color by a second numeric column, add hover_name and hover_data, and use projection='natural earth'. Print the city with the highest metric value.",
"starter":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(55)

cities = pd.DataFrame({
    'city':    ['New York', 'London', 'Tokyo', 'Sydney',
                'Dubai', 'Singapore', 'Toronto', 'Paris'],
    'lat':     [40.71, 51.51, 35.68, -33.87, 25.20,  1.35, 43.65, 48.85],
    'lon':     [-74.01, -0.13, 139.69, 151.21, 55.27, 103.82, -79.38,  2.35],
    'revenue': np.random.uniform(100, 900, 8).round(1),
    'customers': np.random.randint(5000, 50000, 8),
})

# Print highest revenue city
# TODO: top = cities.loc[cities['revenue'].idxmax(), 'city']
# TODO: print(f"Highest revenue city: {top} (${cities['revenue'].max():.1f}M)")

# TODO: fig = px.scatter_geo(
#     cities, lat='lat', lon='lon',
#     size='revenue', color='customers',
#     hover_name='city',
#     hover_data=['revenue', 'customers'],
#     color_continuous_scale='Viridis',
#     projection='natural earth',
#     title='Global City Revenue & Customer Base',
#     size_max=40,
# )
# TODO: fig.update_layout(height=460)
# TODO: fig.show()"""
},
"rw": {
"title": "Global Sales Heatmap by Country",
"scenario": "A VP of Sales uses a choropleth to present YTD revenue performance by country and flag underperforming markets.",
"code":
"""import plotly.express as px
import pandas as pd
import numpy as np

# ISO codes and country names
data = {
    'iso_alpha': ['USA','GBR','DEU','FRA','JPN','BRA','IND','AUS','CAN','MEX',
                  'CHN','KOR','SGP','ZAF','NLD','SWE','NOR','CHE','ITA','ESP'],
    'country':   ['US','UK','Germany','France','Japan','Brazil','India','Australia',
                  'Canada','Mexico','China','S.Korea','Singapore','S.Africa',
                  'Netherlands','Sweden','Norway','Switzerland','Italy','Spain'],
    'target':    [1000,300,280,220,350,150,200,180,260,120,
                  500,180,90,80,130,110,100,120,160,140],
}
np.random.seed(42)
df = pd.DataFrame(data)
df['actual']  = (df['target'] * np.random.uniform(0.6, 1.3, len(df))).round(0)
df['vs_target'] = ((df['actual'] - df['target']) / df['target'] * 100).round(1)

fig = px.choropleth(
    df, locations='iso_alpha',
    color='vs_target',
    hover_name='country',
    hover_data={'actual': True, 'target': True, 'vs_target': True},
    color_continuous_scale='RdYlGn',
    range_color=[-40, 40],
    title='YTD Revenue vs Target by Country (%)',
    labels={'vs_target': 'vs Target (%)'}
)
fig.update_layout(
    height=480,
    coloraxis_colorbar=dict(title='vs Target %', ticksuffix='%')
)
fig.show()"""}
},

{
"title": "10. Exporting & Sharing",
"desc": "Save charts as interactive HTML, static PNG/PDF/SVG (requires kaleido), or embed in web apps via fig.to_json().",
"examples": [
{"label": "Export to HTML and JSON", "code":
"""import plotly.express as px
import os

df  = px.data.iris()
fig = px.scatter(df, x='sepal_length', y='sepal_width',
                 color='species', title='Iris — Export Demo')

# ── Standalone HTML (fully self-contained, shareable) ──
fig.write_html('iris_chart.html', include_plotlyjs='cdn')
print(f"HTML: {os.path.getsize('iris_chart.html') / 1024:.1f} KB")

# ── JSON (for embedding in web apps) ──
json_str = fig.to_json()
print(f"JSON length: {len(json_str):,} chars")

# ── Show in browser / Jupyter ──
fig.show()

# Cleanup
os.remove('iris_chart.html')"""},
{"label": "Export as PNG/PDF with kaleido", "code":
"""import plotly.express as px
import os

# Note: requires  pip install kaleido
df  = px.data.tips()
fig = px.box(df, x='day', y='total_bill', color='time',
             title='Total Bill by Day')

try:
    fig.write_image('chart.png', width=800, height=500, scale=2)
    fig.write_image('chart.pdf')
    fig.write_image('chart.svg')
    print("Saved PNG, PDF, SVG")
    for f in ['chart.png','chart.pdf','chart.svg']:
        if os.path.exists(f): os.remove(f)
except Exception as e:
    print(f"kaleido not installed: {e}")
    print("Install with:  pip install kaleido")

fig.show()"""},
{"label": "Embed multiple charts in a single HTML report", "code":
"""import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

np.random.seed(42)

# Build two figures
df_iris = px.data.iris()
fig1 = px.scatter(df_iris, x='sepal_length', y='petal_length',
                  color='species', title='Iris Scatter')

months = list(range(1, 13))
revenue = 100 + np.cumsum(np.random.randn(12) * 5)
fig2 = px.line(x=months, y=revenue, markers=True,
               title='Monthly Revenue',
               labels={'x': 'Month', 'y': 'Revenue ($K)'})

# Combine into one HTML file manually
html_parts = [
    '<html><head><meta charset="UTF-8"><title>Combined Report</title></head><body>',
    '<h1 style="font-family:sans-serif;padding:20px">Multi-Chart Report</h1>',
    fig1.to_html(full_html=False, include_plotlyjs='cdn'),
    fig2.to_html(full_html=False, include_plotlyjs=False),
    '</body></html>',
]
combined_html = '\\n'.join(html_parts)

out = 'combined_report.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(combined_html)

print(f"Combined report: {out} ({os.path.getsize(out)/1024:.1f} KB)")
print("Contains 2 fully interactive charts in one file.")
os.remove(out)"""},
{"label": "Export to PDF and static image with kaleido", "code":
"""import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

rng = np.random.default_rng(42)
df  = pd.DataFrame({
    'month':   pd.date_range('2024-01-01', periods=12, freq='ME').strftime('%b'),
    'revenue': np.cumsum(rng.uniform(50, 200, 12)) + 500,
    'target':  np.linspace(600, 1800, 12),
})

fig = go.Figure()
fig.add_trace(go.Bar(x=df['month'], y=df['revenue'], name='Revenue',
                     marker_color='steelblue', opacity=0.85))
fig.add_trace(go.Scatter(x=df['month'], y=df['target'], name='Target',
                         line=dict(color='tomato', width=2, dash='dash'),
                         mode='lines+markers', marker_size=7))
fig.update_layout(
    title='Monthly Revenue vs Target', title_font_size=16,
    xaxis_title='Month', yaxis_title='Revenue ($K)',
    legend=dict(x=0.01, y=0.99), height=450,
    template='plotly_white',
)

# Export as PNG (requires kaleido: pip install kaleido)
try:
    fig.write_image('revenue_chart.png', width=900, height=450, scale=2)
    size = os.path.getsize('revenue_chart.png')
    print(f'PNG exported: revenue_chart.png ({size/1024:.1f} KB)')
    os.remove('revenue_chart.png')
except Exception as e:
    print(f'PNG export requires kaleido: pip install kaleido ({e})')

# Export as interactive HTML
html_str = fig.to_html(full_html=True, include_plotlyjs='cdn')
with open('revenue_chart.html', 'w') as f:
    f.write(html_str)
size = os.path.getsize('revenue_chart.html')
print(f'HTML exported: revenue_chart.html ({size/1024:.1f} KB)')
os.remove('revenue_chart.html')

# Export figure dict (JSON-serializable)
fig_dict = fig.to_dict()
print(f'Figure dict keys: {list(fig_dict.keys())}')
print(f'Number of traces: {len(fig_dict[\"data\"])}')"""}
],
"practice": {
"title": "Multi-Chart HTML Report",
"desc": "Build three separate figures (a scatter, a bar chart, and a line chart) using any px datasets. Export each with fig.to_html(full_html=False, include_plotlyjs='cdn' for the first, include_plotlyjs=False for the rest). Stitch them together with a custom HTML wrapper and write to 'my_report.html'. Print the file size and then remove it.",
"starter":
"""import plotly.express as px
import os

# Figure 1: scatter
df_gap = px.data.gapminder().query("year == 2007")
# TODO: fig1 = px.scatter(df_gap, x='gdpPercap', y='lifeExp',
#     size='pop', color='continent', log_x=True,
#     title='GDP vs Life Expectancy 2007')

# Figure 2: bar — top 10 countries by population
# TODO: top10 = df_gap.nlargest(10, 'pop')
# TODO: fig2 = px.bar(top10, x='country', y='pop',
#     color='continent', title='Top 10 Countries by Population')

# Figure 3: line — Europe average life exp over time
# TODO: eur = px.data.gapminder().query("continent == 'Europe'")
# TODO: avg = eur.groupby('year')['lifeExp'].mean().reset_index()
# TODO: fig3 = px.line(avg, x='year', y='lifeExp', markers=True,
#     title='Europe Average Life Expectancy Over Time')

# Combine and save
# TODO: html_body = '\\n'.join([
#     '<html><head><meta charset="UTF-8"><title>My Report</title></head><body>',
#     '<h1 style="font-family:sans-serif;padding:16px">My Plotly Report</h1>',
#     fig1.to_html(full_html=False, include_plotlyjs='cdn'),
#     fig2.to_html(full_html=False, include_plotlyjs=False),
#     fig3.to_html(full_html=False, include_plotlyjs=False),
#     '</body></html>',
# ])
# TODO: out = 'my_report.html'
# TODO: with open(out, 'w', encoding='utf-8') as f:
#     f.write(html_body)
# TODO: print(f"Report saved: {out} ({os.path.getsize(out)/1024:.1f} KB)")
# TODO: os.remove(out)"""
},
"rw": {
"title": "Automated Interactive Report Generator",
"scenario": "A data engineer generates a self-contained HTML report with multiple charts embedded as a single shareable file.",
"code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import numpy as np
import os

np.random.seed(42)
months  = pd.date_range('2024-01', periods=12, freq='MS')
revenue = 100 + np.cumsum(np.random.randn(12) * 8) + np.arange(12) * 4
cac     = np.random.uniform(30, 80, 12)
churn   = np.random.uniform(0.02, 0.08, 12)

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=['Monthly Revenue ($K)', 'Customer Acquisition Cost ($)',
                    'Churn Rate (%)', 'Revenue vs CAC'],
    specs=[[{},{}],[{},{}]]
)

fig.add_trace(go.Scatter(x=months, y=revenue.round(1),
                         fill='tozeroy', line=dict(color='#636EFA')), row=1, col=1)
fig.add_trace(go.Bar(x=months, y=cac.round(1),
                     marker_color='#EF553B'), row=1, col=2)
fig.add_trace(go.Scatter(x=months, y=(churn*100).round(2),
                         mode='lines+markers', line=dict(color='#AB63FA')), row=2, col=1)
fig.add_trace(go.Scatter(x=cac, y=revenue,
                         mode='markers', text=[m.strftime('%b') for m in months],
                         textposition='top center',
                         marker=dict(color='#00CC96', size=9)), row=2, col=2)

fig.update_layout(title='SaaS KPI Report — 2024', height=600,
                  showlegend=False, template='plotly_dark')

# Export as standalone HTML
out = 'saas_report.html'
fig.write_html(out, include_plotlyjs='cdn', full_html=True)
size_kb = os.path.getsize(out) / 1024
print(f"Report saved: {out} ({size_kb:.0f} KB)")
print("Open in any browser — fully interactive, no server needed.")
fig.show()
os.remove(out)"""}
}

,
{
    "title": "11. 3D Charts",
    "desc": "Create interactive 3D visualizations — scatter plots, surface plots, and line trajectories — that users can rotate and zoom in the browser.",
    "examples": [
        {
            "label": "3D scatter plot with color mapping",
            "code": "import plotly.graph_objects as go\nimport numpy as np\n\nnp.random.seed(42)\nx, y, z = np.random.randn(3, 200)\nfig = go.Figure(data=[go.Scatter3d(\n    x=x, y=y, z=z, mode='markers',\n    marker=dict(size=5, color=z, colorscale='Viridis', showscale=True,\n                colorbar=dict(title='Z value'))\n)])\nfig.update_layout(title='3D Scatter Plot',\n    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))\nfig.write_html('scatter3d.html')\nprint('Saved scatter3d.html')"
        },
        {
            "label": "Interactive 3D surface plot",
            "code": "import plotly.graph_objects as go\nimport numpy as np\n\nx = np.linspace(-3, 3, 50)\ny = np.linspace(-3, 3, 50)\nX, Y = np.meshgrid(x, y)\nZ = np.sin(np.sqrt(X**2 + Y**2))\nfig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='RdBu')])\nfig.update_layout(\n    title='3D Surface: sin(sqrt(x^2+y^2))',\n    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='sin(r)'),\n    width=700, height=600\n)\nfig.write_html('surface3d.html')\nprint('Saved surface3d.html')"
        },
        {
            "label": "3D line trajectory colored by progress",
            "code": "import plotly.graph_objects as go\nimport numpy as np\n\nt = np.linspace(0, 10*np.pi, 500)\nx = np.sin(t)\ny = np.cos(t)\nz = t / (10*np.pi)\nfig = go.Figure(data=[go.Scatter3d(\n    x=x, y=y, z=z, mode='lines',\n    line=dict(color=t, colorscale='Plasma', width=4)\n)])\nfig.update_layout(\n    title='3D Spiral Trajectory',\n    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Height')\n)\nfig.write_html('spiral3d.html')\nprint('Saved spiral3d.html')"
        },
        {
            "label": "Side-by-side 3D subplots",
            "code": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\nimport numpy as np\n\nnp.random.seed(42)\nfig = make_subplots(rows=1, cols=2,\n                    specs=[[{'type':'scatter3d'},{'type':'surface'}]],\n                    subplot_titles=['Scatter3D', 'Surface'])\n\nx, y, z = np.random.randn(3, 100)\nfig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers',\n              marker=dict(size=4, color=z, colorscale='Viridis')), row=1, col=1)\n\nt = np.linspace(-2, 2, 30)\nX, Y = np.meshgrid(t, t)\nZ = np.sin(X) * np.cos(Y)\nfig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Plasma', showscale=False), row=1, col=2)\nfig.update_layout(title='3D Subplots', height=500)\nfig.write_html('3d_subplots.html')\nprint('Saved 3d_subplots.html')"
        }
    ],
    "rw_scenario": "A bioinformatics team visualizes protein coordinates in 3D, colored by amino acid type, with interactive rotation to inspect binding sites.",
    "rw_code": "import plotly.graph_objects as go\nimport numpy as np\n\nnp.random.seed(42)\nn = 150\namino_types = ['Polar', 'Nonpolar', 'Charged']\ntype_labels = np.random.choice(amino_types, n)\ncoords = np.random.randn(3, n)\n\ncolor_map = {'Polar':'#2196F3','Nonpolar':'#FF9800','Charged':'#F44336'}\nfig = go.Figure()\nfor aa_type in amino_types:\n    mask = type_labels == aa_type\n    fig.add_trace(go.Scatter3d(\n        x=coords[0,mask], y=coords[1,mask], z=coords[2,mask],\n        mode='markers', name=aa_type,\n        marker=dict(size=6, color=color_map[aa_type], opacity=0.8)\n    ))\nfig.update_layout(\n    title='Protein Structure — Amino Acid Types',\n    scene=dict(xaxis_title='X (Ang)', yaxis_title='Y (Ang)', zaxis_title='Z (Ang)')\n)\nfig.write_html('protein_3d.html')\nprint('Saved protein_3d.html')",
    "practice": {
        "title": "3D Sales Globe",
        "desc": "Create a 3D scatter plot with x=region_id (1-5), y=quarter (1-4), z=revenue. Color points by product category and size them by profit margin. Save to globe_sales.html.",
        "starter": "import plotly.graph_objects as go\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nn = 100\ndf = pd.DataFrame({\n    'region':   np.random.randint(1, 6, n).astype(float),\n    'quarter':  np.random.randint(1, 5, n).astype(float),\n    'revenue':  np.random.exponential(50000, n),\n    'margin':   np.random.uniform(0.05, 0.40, n),\n    'category': np.random.choice(['Electronics','Clothing','Food'], n),\n})\n# TODO: 3D scatter with color by category, size by margin\n# TODO: save to 'globe_sales.html'"
    }
},
{
    "title": "12. Geographic Maps",
    "desc": "Visualize spatial data with choropleth maps, scatter geo, and mapbox — pinpoint patterns across countries, US states, and cities.",
    "examples": [
        {
            "label": "US choropleth map by state",
            "code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\nstates = ['CA','TX','NY','FL','IL','PA','OH','GA','NC','MI',\n          'WA','AZ','MA','TN','IN','MO','MD','CO','WI','MN']\ndf = pd.DataFrame({'state': states, 'value': np.random.randint(100, 10000, len(states))})\nfig = px.choropleth(df, locations='state', color='value',\n                    locationmode='USA-states', scope='usa',\n                    color_continuous_scale='Blues',\n                    title='Simulated Metric by US State')\nfig.write_html('us_choropleth.html')\nprint('Saved us_choropleth.html')"
        },
        {
            "label": "World choropleth with country data",
            "code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\ncountries = ['USA','CHN','IND','BRA','RUS','AUS','CAN','DEU','GBR','FRA',\n             'JPN','KOR','MEX','IDN','NGA','EGY','ZAF','ARG','SAU','TUR']\nnp.random.seed(42)\ndf = pd.DataFrame({'country': countries, 'gdp_per_capita': np.random.uniform(5000, 65000, len(countries))})\nfig = px.choropleth(df, locations='country', color='gdp_per_capita',\n                    color_continuous_scale='Plasma',\n                    title='Simulated GDP Per Capita by Country')\nfig.write_html('world_choropleth.html')\nprint('Saved world_choropleth.html')"
        },
        {
            "label": "Scatter geo — city bubble map",
            "code": "import plotly.express as px\nimport pandas as pd\n\ncities = pd.DataFrame({\n    'city': ['New York','Los Angeles','Chicago','Houston','Phoenix',\n             'Philadelphia','San Antonio','San Diego','Dallas','San Jose'],\n    'lat':  [40.71, 34.05, 41.85, 29.76, 33.45, 39.95, 29.42, 32.72, 32.78, 37.34],\n    'lon':  [-74.01,-118.24,-87.65,-95.37,-112.07,-75.17,-98.49,-117.16,-96.80,-121.89],\n    'pop':  [8336817,3979576,2693976,2320268,1608139,1603797,1434625,1386932,1304379,1035317],\n    'region': ['NE','West','MW','South','West','NE','South','West','South','West'],\n})\nfig = px.scatter_geo(cities, lat='lat', lon='lon', size='pop', color='region',\n                     hover_name='city', scope='usa', size_max=40,\n                     title='Top 10 US Cities by Population')\nfig.write_html('city_bubble.html')\nprint('Saved city_bubble.html')"
        },
        {
            "label": "Mapbox scatter map with open tiles",
            "code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'lat':   np.random.uniform(25, 49, 50),\n    'lon':   np.random.uniform(-125, -67, 50),\n    'value': np.random.uniform(10, 100, 50),\n    'label': [f'Site {i}' for i in range(50)],\n})\nfig = px.scatter_mapbox(df, lat='lat', lon='lon', size='value',\n                        color='value', color_continuous_scale='Reds',\n                        hover_name='label', zoom=3,\n                        mapbox_style='open-street-map',\n                        title='Random Sites across the US')\nfig.write_html('mapbox_scatter.html')\nprint('Saved mapbox_scatter.html')"
        }
    ],
    "rw_scenario": "A logistics company maps delivery volumes by state — high-volume states appear dark red, enabling instant identification of overloaded regions.",
    "rw_code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\nstates = ['CA','TX','NY','FL','IL','PA','OH','GA','NC','MI',\n          'WA','AZ','MA','TN','IN','MO','MD','CO','WI','MN',\n          'AL','SC','KY','OR','OK','CT','UT','IA','NV','AR']\ndf = pd.DataFrame({\n    'state': states,\n    'deliveries': np.random.randint(5000, 120000, len(states)),\n    'on_time_pct': np.random.uniform(0.82, 0.99, len(states)),\n})\n\nfig = px.choropleth(df, locations='state', color='deliveries',\n                    locationmode='USA-states', scope='usa',\n                    color_continuous_scale='Reds',\n                    hover_data=['on_time_pct'],\n                    title='Delivery Volume by State')\nfig.write_html('delivery_map.html')\nprint('Saved delivery_map.html')\nprint(f'State with most deliveries: {df.loc[df.deliveries.idxmax(), \"state\"]}')",
    "practice": {
        "title": "Global Temperature Map",
        "desc": "Create a world choropleth showing average temperature by country (simulated). Use a RdBu_r diverging colorscale centered at 15 degrees. Save to world_temp.html.",
        "starter": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\ncountries = ['USA','CHN','IND','BRA','RUS','AUS','CAN','DEU','GBR','FRA',\n             'JPN','KOR','MEX','IDN','NGA','EGY','ZAF','ARG','SAU','TUR']\nnp.random.seed(42)\ndf = pd.DataFrame({'country': countries, 'avg_temp': np.random.uniform(5, 30, len(countries))})\n# TODO: choropleth with locations='country', color='avg_temp'\n# TODO: colorscale='RdBu_r', color midpoint=15\n# TODO: save to 'world_temp.html'"
    }
},
{
    "title": "13. Animations",
    "desc": "Bring data to life with Plotly animations — animated scatter plots, bar chart races, and frame-by-frame time-lapse visualizations.",
    "examples": [
        {
            "label": "Animated scatter with animation_frame",
            "code": "import plotly.express as px\n\ntry:\n    gapminder = px.data.gapminder()\n    fig = px.scatter(gapminder, x='gdpPercap', y='lifeExp',\n                     animation_frame='year', animation_group='country',\n                     size='pop', color='continent', hover_name='country',\n                     log_x=True, size_max=55,\n                     range_x=[100, 100000], range_y=[25, 90],\n                     title='Gapminder: GDP vs Life Expectancy over Time')\n    fig.write_html('gapminder_animation.html')\n    print('Saved gapminder_animation.html')\nexcept Exception as e:\n    print(f'Note: {e}')"
        },
        {
            "label": "Animated bar chart race",
            "code": "import plotly.graph_objects as go\nimport numpy as np\n\nnp.random.seed(42)\ncategories = ['A','B','C','D','E']\nyears = list(range(2018, 2024))\ndata = {cat: np.cumsum(np.random.randint(5,20,len(years))) for cat in categories}\n\nframes = []\nfor i, year in enumerate(years):\n    vals = [data[c][i] for c in categories]\n    order = sorted(range(len(vals)), key=lambda x: vals[x])\n    frames.append(go.Frame(\n        data=[go.Bar(x=[vals[j] for j in order], y=[categories[j] for j in order],\n                     orientation='h', marker_color='steelblue')],\n        name=str(year)\n    ))\n\nfig = go.Figure(frames=frames, data=frames[0].data)\nfig.update_layout(\n    title='Bar Chart Race', xaxis_title='Cumulative Value',\n    updatemenus=[dict(type='buttons', showactive=False,\n                      buttons=[dict(label='Play', method='animate',\n                                   args=[None, dict(frame=dict(duration=800))])])]\n)\nfig.write_html('bar_race.html')\nprint('Saved bar_race.html')"
        },
        {
            "label": "Animated line chart over time",
            "code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\nmonths = pd.date_range('2022-01', periods=24, freq='ME')\ncategories = ['Electronics','Clothing','Food']\nrows = []\nfor cat in categories:\n    base = {'Electronics':5000,'Clothing':3000,'Food':7000}[cat]\n    for m in months:\n        rows.append({'month': m.strftime('%Y-%m'), 'category': cat,\n                     'revenue': base + np.random.randint(-500, 1500)})\ndf = pd.DataFrame(rows)\ndf = df.sort_values('month')\n\nfig = px.line(df, x='month', y='revenue', color='category',\n              animation_frame='month',\n              range_y=[df.revenue.min()-200, df.revenue.max()+200],\n              title='Monthly Revenue Animation')\nfig.write_html('animated_line.html')\nprint('Saved animated_line.html')"
        },
        {
            "label": "Slider-controlled visualization",
            "code": "import plotly.graph_objects as go\nimport numpy as np\n\nx = np.linspace(0, 2*np.pi, 200)\nsteps = []\nfigs_data = []\nfor freq in np.linspace(1, 5, 20):\n    figs_data.append(go.Scatter(x=x, y=np.sin(freq*x), mode='lines',\n                                name=f'f={freq:.1f}'))\n\nsteps = [dict(method='update', args=[{'y': [np.sin(f*x)], 'name': [f'f={f:.1f}']}],\n              label=f'{f:.1f}') for f in np.linspace(1, 5, 20)]\n\nfig = go.Figure(data=[figs_data[0]])\nfig.update_layout(\n    title='Interactive Slider: sin(f*x)',\n    sliders=[dict(active=0, steps=steps, currentvalue=dict(prefix='Frequency: '))],\n    xaxis_title='x', yaxis_title='sin(f*x)', yaxis_range=[-1.2, 1.2]\n)\nfig.write_html('slider_sine.html')\nprint('Saved slider_sine.html')"
        }
    ],
    "rw_scenario": "A development economist animates 50 years of GDP per capita vs life expectancy across countries, revealing how global health and wealth co-evolved.",
    "rw_code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\ntry:\n    gapminder = px.data.gapminder()\n    fig = px.scatter(gapminder[gapminder.continent.isin(['Asia','Europe','Americas'])],\n                     x='gdpPercap', y='lifeExp',\n                     animation_frame='year', animation_group='country',\n                     size='pop', color='continent', hover_name='country',\n                     log_x=True, size_max=45,\n                     range_x=[200,80000], range_y=[30,90],\n                     title='Development over 50 Years')\n    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 600\n    fig.write_html('dev_animation.html')\n    print('Saved dev_animation.html')\nexcept Exception as e:\n    print(f'Note: {e}')",
    "practice": {
        "title": "Population Growth Animation",
        "desc": "Create an animated bar chart showing population by continent (in billions) from 2000 to 2023. Each frame = one year. Add a play button. Save to population_animation.html.",
        "starter": "import plotly.graph_objects as go\nimport numpy as np\n\ncontinents = ['Africa','Asia','Europe','Americas','Oceania']\nyears = list(range(2000, 2024))\nnp.random.seed(42)\nbase = [0.8, 3.7, 0.7, 0.9, 0.03]\ngrowth = [0.03, 0.01, 0.002, 0.01, 0.015]\n\n# TODO: build frames list (one per year)\n# TODO: each frame: go.Frame with go.Bar showing populations\n# TODO: fig with play button in updatemenus\n# TODO: save to 'population_animation.html'"
    }
},

    {
        "title": "14. Plotly Dash Fundamentals",
        "examples": [
            {
                "label": "Dash app structure (code pattern)",
                "code": "# Dash apps run as web servers - this shows the code pattern\nprint(\'Dash app structure:\')\nprint(\'\'\'\nfrom dash import Dash, dcc, html\nfrom dash.dependencies import Input, Output\nimport plotly.express as px\n\napp = Dash(__name__)\napp.layout = html.Div([\n    html.H1(\"Dashboard\"),\n    dcc.Dropdown(id=\"metric\", options=[\"Revenue\",\"Users\"], value=\"Revenue\"),\n    dcc.Graph(id=\"chart\"),\n])\n\n@app.callback(Output(\"chart\",\"figure\"), Input(\"metric\",\"value\"))\ndef update(metric):\n    import numpy as np, pandas as pd\n    df = pd.DataFrame({\"date\": pd.date_range(\"2024-01-01\", periods=30),\n                        metric: 100 + np.cumsum(np.random.randn(30))})\n    return px.line(df, x=\"date\", y=metric, title=f\"{metric} over Time\")\n\nif __name__ == \"__main__\":\n    app.run_server(debug=True)\n\'\'\')\nprint(\"Run with: python app.py\")"
            },
            {
                "label": "Plotly figure for Dash callback",
                "code": "import plotly.graph_objects as go\nimport plotly.express as px\nimport numpy as np\nimport pandas as pd\n\ndef make_dashboard_fig(category=\'All\'):\n    np.random.seed(42)\n    dates = pd.date_range(\'2024-01-01\', periods=90, freq=\'D\')\n    cats = [\'Electronics\',\'Apparel\',\'Food\']\n    dfs = [pd.DataFrame({\'date\':dates,\'revenue\':np.random.exponential(1000,90),\'cat\':c}) for c in cats]\n    df = pd.concat(dfs)\n    if category != \'All\':\n        df = df[df.cat == category]\n    fig = px.area(df.groupby([\'date\',\'cat\'])[\'revenue\'].sum().reset_index(),\n                  x=\'date\', y=\'revenue\', color=\'cat\',\n                  title=f\'Revenue: {category}\', template=\'plotly_white\')\n    fig.update_layout(hovermode=\'x unified\', height=400)\n    return fig\n\nfig = make_dashboard_fig(\'Electronics\')\nfig.write_html(\'dash_callback_fig.html\')\nprint(f\'Dashboard figure saved - traces: {len(fig.data)}\')"
            },
            {
                "label": "DataTable interactive grid pattern",
                "code": "# Dash DataTable pattern\nprint(\'DataTable pattern:\')\nprint(\'\'\'\nfrom dash import dash_table\nimport pandas as pd\n\ndf = pd.read_csv(\"data.csv\")\ntable = dash_table.DataTable(\n    data=df.to_dict(\"records\"),\n    columns=[{\"name\": c, \"id\": c} for c in df.columns],\n    filter_action=\"native\",\n    sort_action=\"native\",\n    page_size=10,\n    export_format=\"csv\",\n    style_data_conditional=[{\n        \"if\": {\"filter_query\": \"{revenue} > 1000\"},\n        \"backgroundColor\": \"#d4edda\",\n    }],\n)\n\'\'\')\nprint(\'Key features: filter_action, sort_action, export_format, conditional styling\')"
            },
            {
                "label": "Multi-page Dash routing",
                "code": "# Multi-page Dash 2.x pattern\nprint(\'Multi-page Dash pattern:\')\nprint(\'\'\'\n# pages/home.py\nimport dash\ndash.register_page(__name__, path=\"/\")\nlayout = html.Div([html.H2(\"Home\")])\n\n# pages/analytics.py\ndash.register_page(__name__, path=\"/analytics\")\nlayout = html.Div([dcc.Graph(figure=create_fig())])\n\n# app.py\napp = Dash(__name__, use_pages=True)\napp.layout = html.Div([\n    html.Nav([\n        dcc.Link(\"Home\", href=\"/\"),\n        dcc.Link(\"Analytics\", href=\"/analytics\"),\n    ]),\n    dash.page_container\n])\n\'\'\')\nprint(\'Each page: dash.register_page(__name__, path=\"/route\")\')"
            }
        ],
        "rw_scenario": "You\'re building an internal analytics dashboard where users filter by date/category, charts update automatically, and data can be exported as CSV.",
        "rw_code": "import plotly.graph_objects as go\nimport plotly.express as px\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndates = pd.date_range(\'2024-01-01\', periods=180, freq=\'D\')\ncats = [\'Electronics\',\'Apparel\',\'Food\']\nfig = go.Figure()\nfor cat in cats:\n    rev = np.random.exponential(1000, 180).cumsum()\n    fig.add_trace(go.Scatter(x=dates, y=rev, name=cat, mode=\'lines\'))\nfig.update_layout(title=\'Revenue Dashboard Preview\', xaxis_title=\'Date\', yaxis_title=\'Revenue ($)\',\n                  template=\'plotly_white\', hovermode=\'x unified\',\n                  legend=dict(orientation=\'h\', y=-0.2))\nfig.write_html(\'dashboard_preview.html\')\nprint(f\'Dashboard saved - {len(fig.data)} traces, {len(dates)} days\')",
        "practice": {
            "title": "Filter Callback",
            "desc": "Write a function make_fig(year, continent) that filters gapminder data and returns a scatter of GDP vs life expectancy. Call it for (1952,\'Asia\'), (2007,\'Europe\'), (2007,\'All\'). Save each as HTML.",
            "starter": "import plotly.express as px\n\ngap = px.data.gapminder()\n\ndef make_fig(year, continent):\n    # TODO: filter by year and continent (\'All\' = no continent filter)\n    # TODO: return px.scatter size=\'pop\', color=\'country\', log_x=True\n    pass\n\nfor year, cont in [(1952,\'Asia\'), (2007,\'Europe\'), (2007,\'All\')]:\n    fig = make_fig(year, cont)\n    if fig:\n        fig.write_html(f\'gap_{year}_{cont}.html\')"
        }
    },
    {
        "title": "15. Map Visualizations",
        "examples": [
            {
                "label": "Choropleth world map",
                "code": "import plotly.express as px\n\ndf = px.data.gapminder().query(\"year == 2007\")\nfig = px.choropleth(df, locations=\'iso_alpha\', color=\'gdpPercap\',\n                    hover_name=\'country\', color_continuous_scale=\'Viridis\',\n                    range_color=[0, 50000], title=\'GDP per Capita (2007)\',\n                    labels={\'gdpPercap\': \'GDP per Capita\'})\nfig.update_layout(geo=dict(showframe=False, showcoastlines=True))\nfig.write_html(\'choropleth_world.html\')\nprint(f\'Choropleth saved - {len(df)} countries\')"
            },
            {
                "label": "Scatter geo map (USA)",
                "code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\ndf = pd.DataFrame({\'lat\':np.random.uniform(25,50,80),\'lon\':np.random.uniform(-125,-65,80),\n                   \'city\':[f\'City_{i}\' for i in range(80)],\n                   \'sales\':np.random.exponential(500,80),\n                   \'category\':np.random.choice([\'A\',\'B\',\'C\'],80)})\nfig = px.scatter_geo(df, lat=\'lat\', lon=\'lon\', size=\'sales\', color=\'category\',\n                     hover_name=\'city\', scope=\'usa\', title=\'Sales Distribution USA\', size_max=20)\nfig.write_html(\'scatter_map.html\')\nprint(f\'Scatter geo saved - {len(df)} points\')"
            },
            {
                "label": "Animated choropleth over time",
                "code": "import plotly.express as px\n\ndf = px.data.gapminder()\nfig = px.choropleth(df, locations=\'iso_alpha\', color=\'lifeExp\',\n                    hover_name=\'country\', animation_frame=\'year\',\n                    color_continuous_scale=\'RdYlGn\', range_color=[30, 90],\n                    title=\'Life Expectancy Over Time\')\nfig.update_layout(geo=dict(showframe=False))\nfig.write_html(\'choropleth_animated.html\')\nprint(f\'Animated choropleth - {df.year.nunique()} frames\')"
            },
            {
                "label": "Density mapbox heatmap",
                "code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\ndf = pd.DataFrame({\'lat\':np.random.normal(40.7128,0.05,400),\n                   \'lon\':np.random.normal(-74.006,0.05,400),\n                   \'intensity\':np.random.exponential(1,400)})\nfig = px.density_mapbox(df, lat=\'lat\', lon=\'lon\', z=\'intensity\', radius=15,\n                         center=dict(lat=40.7128,lon=-74.006), zoom=10,\n                         mapbox_style=\'open-street-map\',\n                         title=\'Event Density (NYC Area)\', color_continuous_scale=\'Inferno\')\nfig.write_html(\'density_map.html\')\nprint(f\'Density map saved - {len(df)} events\')"
            }
        ],
        "rw_scenario": "You need to visualize global customer distribution with bubble sizes for revenue and colors for satisfaction score, animated across 4 quarters.",
        "rw_code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\ncoords = {\'USA\':(37.09,-95.71),\'DEU\':(51.16,10.45),\'GBR\':(55.37,-3.44),\n          \'JPN\':(36.20,138.25),\'BRA\':(-14.23,-51.92),\'IND\':(20.59,78.96)}\nrows = []\nfor q in [\'Q1\',\'Q2\',\'Q3\',\'Q4\']:\n    for country,(lat,lon) in coords.items():\n        rows.append({\'quarter\':q,\'country\':country,\'lat\':lat+np.random.randn()*0.5,\n                     \'lon\':lon+np.random.randn()*0.5,\'revenue\':np.random.exponential(500000),\n                     \'satisfaction\':np.random.uniform(3,5)})\ndf = pd.DataFrame(rows)\nfig = px.scatter_geo(df, lat=\'lat\', lon=\'lon\', size=\'revenue\', color=\'satisfaction\',\n                     hover_name=\'country\', animation_frame=\'quarter\',\n                     color_continuous_scale=\'RdYlGn\', range_color=[3,5], size_max=40,\n                     title=\'Global Customer Revenue & Satisfaction\')\nfig.write_html(\'global_map.html\')\nprint(f\'Global map saved - {len(df)} records, {df.quarter.nunique()} frames\')",
        "practice": {
            "title": "US State Choropleth",
            "desc": "Create a choropleth of US states using locationmode=\'USA-states\'. Assign random performance_score (0-100) to each state abbreviation. Color with RdYlGn. Save as HTML.",
            "starter": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nstates = [\'AL\',\'AK\',\'AZ\',\'AR\',\'CA\',\'CO\',\'CT\',\'DE\',\'FL\',\'GA\',\'HI\',\'ID\',\'IL\',\'IN\',\'IA\',\n          \'KS\',\'KY\',\'LA\',\'ME\',\'MD\',\'MA\',\'MI\',\'MN\',\'MS\',\'MO\',\'MT\',\'NE\',\'NV\',\'NH\',\'NJ\',\n          \'NM\',\'NY\',\'NC\',\'ND\',\'OH\',\'OK\',\'OR\',\'PA\',\'RI\',\'SC\',\'SD\',\'TN\',\'TX\',\'UT\',\'VT\',\n          \'VA\',\'WA\',\'WV\',\'WI\',\'WY\']\nnp.random.seed(42)\ndf = pd.DataFrame({\'state\':states,\'score\':np.random.uniform(40,100,len(states))})\n# TODO: px.choropleth locationmode=\'USA-states\', color=\'score\', scope=\'usa\'\n# TODO: color_continuous_scale=\'RdYlGn\'\n# TODO: save \'us_choropleth.html\'"
        }
    },
    {
        "title": "16. 3D Plots & Surface Visualizations",
        "examples": [
            {
                "label": "3D surface with contour projections",
                "code": "import plotly.graph_objects as go\nimport numpy as np\n\nx = y = np.linspace(-3, 3, 60)\nX, Y = np.meshgrid(x, y)\nZ = np.sin(np.sqrt(X**2 + Y**2))\nfig = go.Figure(go.Surface(x=X, y=Y, z=Z, colorscale=\'Viridis\',\n                             contours={\'z\':{\'show\':True,\'start\':-1,\'end\':1,\'size\':0.25}}))\nfig.update_layout(title=\'3D Surface: sin(sqrt(x2+y2))\',\n                  scene=dict(xaxis_title=\'X\', yaxis_title=\'Y\', zaxis_title=\'Z\',\n                             camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))),\n                  width=700, height=500)\nfig.write_html(\'surface_3d.html\')\nprint(\'3D surface saved\')"
            },
            {
                "label": "3D scatter with cluster colors",
                "code": "import plotly.express as px\nimport numpy as np\n\nnp.random.seed(42)\nn = 300\nx = np.random.randn(n); y = np.random.randn(n)\nz = x**2 + y**2 + np.random.randn(n) * 0.5\ncats = [\'Inner\' if v < 2 else \'Middle\' if v < 5 else \'Outer\' for v in z]\nfig = px.scatter_3d(x=x, y=y, z=z, color=cats, symbol=cats,\n                    color_discrete_sequence=px.colors.qualitative.Set1,\n                    title=\'3D Scatter by Distance from Origin\')\nfig.update_traces(marker=dict(size=4, opacity=0.7))\nfig.write_html(\'scatter_3d.html\')\nprint(f\'3D scatter saved - {n} points\')"
            },
            {
                "label": "3D spiral trajectory",
                "code": "import plotly.graph_objects as go\nimport numpy as np\n\nt = np.linspace(0, 8*np.pi, 500)\nx = np.cos(t)*np.exp(-t/20); y = np.sin(t)*np.exp(-t/20); z = t/(4*np.pi)\nfig = go.Figure()\nfig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode=\'lines\',\n                            line=dict(color=t, colorscale=\'Plasma\', width=4), name=\'Trajectory\'))\nfig.add_trace(go.Scatter3d(x=[x[0]], y=[y[0]], z=[z[0]], mode=\'markers\',\n                            marker=dict(size=8, color=\'green\'), name=\'Start\'))\nfig.add_trace(go.Scatter3d(x=[x[-1]], y=[y[-1]], z=[z[-1]], mode=\'markers\',\n                            marker=dict(size=8, color=\'red\'), name=\'End\'))\nfig.update_layout(title=\'3D Spiral Trajectory\',\n                  scene=dict(xaxis_title=\'X\', yaxis_title=\'Y\', zaxis_title=\'Height\'))\nfig.write_html(\'trajectory_3d.html\')\nprint(\'3D trajectory saved\')"
            },
            {
                "label": "Loss landscape with gradient descent",
                "code": "import plotly.graph_objects as go\nimport numpy as np\n\nx = y = np.linspace(-3, 3, 60)\nX, Y = np.meshgrid(x, y)\nZ = (np.sin(X*2)*np.cos(Y*2)*0.5 + (X**2+Y**2)*0.1 + np.exp(-((X-1)**2+(Y-1)**2))*(-1.5))\nZ = (Z - Z.min()) / (Z.max() - Z.min()) * 3\n\npx_path, py_path, pz_path = [2.5], [-2.5], [float(Z[0,-1])]\nlr = 0.08\nfor _ in range(60):\n    ix = int(np.argmin(np.abs(x - px_path[-1])))\n    iy = int(np.argmin(np.abs(y - py_path[-1])))\n    gx = (Z[iy, min(ix+1,59)] - Z[iy, max(ix-1,0)]) / 2\n    gy = (Z[min(iy+1,59), ix] - Z[max(iy-1,0), ix]) / 2\n    nx, ny = float(np.clip(px_path[-1]-lr*gx,-3,3)), float(np.clip(py_path[-1]-lr*gy,-3,3))\n    px_path.append(nx); py_path.append(ny)\n    pz_path.append(float(Z[int(np.argmin(np.abs(y-ny))), int(np.argmin(np.abs(x-nx)))]))\n\nfig = go.Figure([go.Surface(x=X, y=Y, z=Z, colorscale=\'RdYlGn_r\', opacity=0.85),\n                  go.Scatter3d(x=px_path, y=py_path, z=pz_path, mode=\'lines+markers\',\n                               line=dict(color=\'blue\', width=5), marker=dict(size=3),\n                               name=\'GD Path\')])\nfig.update_layout(title=\'Loss Landscape + Gradient Descent\', width=750, height=550)\nfig.write_html(\'loss_landscape.html\')\nprint(f\'Loss landscape saved - final loss: {pz_path[-1]:.3f}\')"
            }
        ],
        "rw_scenario": "You need to visualize a model\'s loss surface in 3D to understand convergence and identify local minima during hyperparameter search.",
        "rw_code": "import plotly.graph_objects as go\nimport numpy as np\n\nx = y = np.linspace(-3, 3, 60)\nX, Y = np.meshgrid(x, y)\nnp.random.seed(42)\nZ = (np.sin(X*1.5)*np.cos(Y*1.5)*0.8 + (X**2+Y**2)*0.15 +\n     np.exp(-((X+1)**2+(Y+1)**2))*(-2) + np.random.randn(*X.shape)*0.05)\nZ = (Z - Z.min()) / (Z.max() - Z.min()) * 4\n\nbest_iy, best_ix = np.unravel_index(Z.argmin(), Z.shape)\nfig = go.Figure([\n    go.Surface(x=X, y=Y, z=Z, colorscale=\'RdYlGn_r\', opacity=0.85,\n               colorbar=dict(title=\'Loss\')),\n    go.Scatter3d(x=[x[best_ix]], y=[y[best_iy]], z=[Z.min()],\n                 mode=\'markers\', marker=dict(size=12, color=\'gold\', symbol=\'diamond\'),\n                 name=\'Global Min\')\n])\nfig.update_layout(title=\'Hyperparameter Loss Surface\',\n                  scene=dict(xaxis_title=\'param_1\', yaxis_title=\'param_2\', zaxis_title=\'Loss\'),\n                  width=750, height=550)\nfig.write_html(\'hyperparam_surface.html\')\nprint(f\'Surface saved - min loss: {Z.min():.4f} at ({x[best_ix]:.2f}, {y[best_iy]:.2f})\')",
        "practice": {
            "title": "3D Cluster Scatter",
            "desc": "Generate 3 Gaussian clusters at (0,0,0), (3,3,0), (0,3,3) in 3D. Create a 3D scatter with each cluster in a different color. Add axis labels and save as \'clusters_3d.html\'.",
            "starter": "import plotly.graph_objects as go\nimport numpy as np\n\nnp.random.seed(42)\ncenters = [(0,0,0),(3,3,0),(0,3,3)]\ncolors = [\'blue\',\'red\',\'green\']\nfig = go.Figure()\nfor i,(cx,cy,cz) in enumerate(centers):\n    n = 50\n    x = np.random.randn(n)+cx; y = np.random.randn(n)+cy; z = np.random.randn(n)+cz\n    # TODO: add Scatter3d trace\n    pass\n# TODO: update_layout with title, axis labels\n# TODO: fig.write_html(\'clusters_3d.html\')"
        }
    },
{
"title": "17. Candlestick & Financial Charts",
"desc": "Plotly\'s go.Candlestick and go.Ohlc render OHLC price data with interactive zoom, range slectors, and volume overlays — essential for financial dashboards.",
"examples": [
        {"label": "Basic candlestick with volume overlay", "code": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\ndates = pd.date_range(\'2024-01-01\', periods=60, freq=\'B\')\nclose = 100 + np.cumsum(np.random.randn(60) * 1.5)\nopen_ = close + np.random.randn(60) * 0.8\nhigh  = np.maximum(open_, close) + np.abs(np.random.randn(60) * 0.5)\nlow   = np.minimum(open_, close) - np.abs(np.random.randn(60) * 0.5)\nvolume = np.random.randint(1_000_000, 5_000_000, 60)\n\nfig = make_subplots(rows=2, cols=1, shared_xaxes=True,\n                    vertical_spacing=0.03, row_heights=[0.75, 0.25])\n\nfig.add_trace(go.Candlestick(x=dates, open=open_, high=high,\n                              low=low, close=close, name=\'OHLC\',\n                              increasing_line_color=\'#26a69a\',\n                              decreasing_line_color=\'#ef5350\'), row=1, col=1)\n\ncolors = [\'#26a69a\' if c >= o else \'#ef5350\' for c, o in zip(close, open_)]\nfig.add_trace(go.Bar(x=dates, y=volume, name=\'Volume\',\n                     marker_color=colors, opacity=0.7), row=2, col=1)\n\nfig.update_layout(title=\'OHLC Price + Volume\', xaxis_rangeslider_visible=False,\n                  template=\'plotly_dark\', height=500)\nfig.update_yaxes(title_text=\'Price ($)\', row=1)\nfig.update_yaxes(title_text=\'Volume\', row=2)\nfig.write_html(\'candlestick.html\')\nprint(\'Chart saved\')"},
        {"label": "Moving averages on candlestick", "code": "import plotly.graph_objects as go\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\ndates = pd.date_range(\'2023-01-01\', periods=120, freq=\'B\')\nclose = 150 + np.cumsum(np.random.randn(120) * 2)\nopen_ = close + np.random.randn(120)\nhigh  = np.maximum(open_, close) + np.abs(np.random.randn(120))\nlow   = np.minimum(open_, close) - np.abs(np.random.randn(120))\n\ns = pd.Series(close, index=dates)\nma20 = s.rolling(20).mean()\nma50 = s.rolling(50).mean()\n\nfig = go.Figure()\nfig.add_trace(go.Candlestick(x=dates, open=open_, high=high,\n                              low=low, close=close, name=\'OHLC\',\n                              increasing_fillcolor=\'#26a69a\',\n                              decreasing_fillcolor=\'#ef5350\'))\nfig.add_trace(go.Scatter(x=dates, y=ma20, name=\'MA 20\',\n                          line=dict(color=\'orange\', width=1.5)))\nfig.add_trace(go.Scatter(x=dates, y=ma50, name=\'MA 50\',\n                          line=dict(color=\'cyan\', width=1.5)))\n\nfig.update_layout(title=\'Candlestick with Moving Averages\',\n                  template=\'plotly_dark\', xaxis_rangeslider_visible=False,\n                  hovermode=\'x unified\', height=450)\nfig.write_html(\'candlestick_ma.html\')\nprint(\'Saved with MA20/MA50\')"},
        {"label": "Range selector buttons and OHLC bar chart", "code": "import plotly.graph_objects as go\nimport numpy as np, pandas as pd\n\nnp.random.seed(0)\ndates = pd.date_range(\'2022-01-01\', periods=250, freq=\'B\')\nclose = 200 + np.cumsum(np.random.randn(250) * 2.5)\nopen_ = close + np.random.randn(250) * 1.2\nhigh  = np.maximum(open_, close) + np.abs(np.random.randn(250))\nlow   = np.minimum(open_, close) - np.abs(np.random.randn(250))\n\nfig = go.Figure(go.Ohlc(x=dates, open=open_, high=high,\n                         low=low, close=close, name=\'OHLC Bars\',\n                         increasing_line_color=\'lime\',\n                         decreasing_line_color=\'red\'))\n\nfig.update_layout(\n    title=\'OHLC with Range Selectors\',\n    template=\'plotly_dark\',\n    xaxis=dict(\n        rangeselector=dict(\n            buttons=[\n                dict(count=1, label=\'1M\', step=\'month\', stepmode=\'backward\'),\n                dict(count=3, label=\'3M\', step=\'month\', stepmode=\'backward\'),\n                dict(count=6, label=\'6M\', step=\'month\', stepmode=\'backward\'),\n                dict(step=\'all\', label=\'All\'),\n            ]\n        ),\n        rangeslider=dict(visible=True),\n        type=\'date\',\n    ),\n    height=450,\n)\nfig.write_html(\'ohlc_range.html\')\nprint(\'OHLC chart with range selector saved\')"}
    ],
"rw": {
    "title": "Stock Screener Dashboard",
    "scenario": "A portfolio tracker shows daily OHLC for top 5 holdings, highlighting days where close > open in green and flagging high-volume days.",
    "code": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\nimport numpy as np, pandas as pd\n\nnp.random.seed(7)\ntickers = [\'AAPL\', \'MSFT\', \'GOOG\']\ndates = pd.date_range(\'2024-01-01\', periods=40, freq=\'B\')\n\nfig = make_subplots(rows=len(tickers), cols=1, shared_xaxes=True,\n                    subplot_titles=tickers, vertical_spacing=0.06)\n\nfor row, ticker in enumerate(tickers, 1):\n    c = 150 + row*20 + np.cumsum(np.random.randn(40)*2)\n    o = c + np.random.randn(40)\n    h = np.maximum(o,c) + np.abs(np.random.randn(40)*0.5)\n    l = np.minimum(o,c) - np.abs(np.random.randn(40)*0.5)\n    fig.add_trace(go.Candlestick(x=dates, open=o, high=h, low=l, close=c,\n                                  name=ticker, showlegend=True), row=row, col=1)\n\nfig.update_xaxes(rangeslider_visible=False)\nfig.update_layout(title=\'Portfolio Overview\', template=\'plotly_dark\', height=700)\nfig.write_html(\'portfolio.html\')\nprint(f\'Portfolio chart: {len(tickers)} tickers saved\')"
},
"practice": {
    "title": "Bollinger Bands",
    "desc": "Generate 90 days of OHLC data (random walk starting at 100). Compute a 20-day rolling mean and ±2 std Bollinger Bands from the close price. Plot as a candlestick with the upper, middle, and lower bands as overlaid lines. Color the bands blue. Save as \'bollinger.html\'.",
    "starter": "import plotly.graph_objects as go\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\ndates = pd.date_range(\'2024-01-01\', periods=90, freq=\'B\')\nclose = 100 + np.cumsum(np.random.randn(90) * 1.5)\nopen_ = close + np.random.randn(90)\nhigh  = np.maximum(open_, close) + np.abs(np.random.randn(90)*0.5)\nlow   = np.minimum(open_, close) - np.abs(np.random.randn(90)*0.5)\n\ns = pd.Series(close, index=dates)\n# TODO: compute ma = s.rolling(20).mean()\n# TODO: std = s.rolling(20).std()\n# TODO: upper = ma + 2*std, lower = ma - 2*std\n\nfig = go.Figure()\n# TODO: add Candlestick trace\n# TODO: add Scatter traces for upper, middle (ma), lower bands\nfig.update_layout(title=\'Bollinger Bands\', template=\'plotly_dark\',\n                  xaxis_rangeslider_visible=False)\nfig.write_html(\'bollinger.html\')\n"
}
},

{
"title": "18. Treemap & Sunburst Charts",
"desc": "Treemaps and sunbursts visualize hierarchical data where area/angle encodes value. Use them for budget breakdowns, file system sizes, market cap, and org charts.",
"examples": [
        {"label": "Treemap from flat DataFrame", "code": "import plotly.express as px\nimport pandas as pd\n\ndf = pd.DataFrame({\n    \'category\': [\'Electronics\',\'Electronics\',\'Electronics\',\n                 \'Clothing\',\'Clothing\',\'Food\',\'Food\',\'Food\',\'Food\'],\n    \'subcategory\': [\'Phones\',\'Laptops\',\'Tablets\',\n                    \'Shirts\',\'Pants\',\'Dairy\',\'Bakery\',\'Produce\',\'Frozen\'],\n    \'sales\': [4500, 3200, 1800, 2100, 1600, 900, 750, 1200, 680],\n    \'profit\': [900, 480, 270, 420, 240, 135, 112, 180, 102],\n})\n\nfig = px.treemap(df,\n    path=[\'category\', \'subcategory\'],\n    values=\'sales\',\n    color=\'profit\',\n    color_continuous_scale=\'RdYlGn\',\n    title=\'Sales Treemap by Category → Subcategory\',\n    hover_data={\'profit\': \':,.0f\'},\n)\nfig.update_traces(textinfo=\'label+value+percent root\')\nfig.write_html(\'treemap_sales.html\')\nprint(f\'Treemap saved — {len(df)} rows\')"},
        {"label": "Sunburst for org/portfolio drilldown", "code": "import plotly.express as px\nimport pandas as pd\n\ndf = pd.DataFrame({\n    \'continent\': [\'Americas\',\'Americas\',\'Americas\',\'Europe\',\'Europe\',\'Asia\',\'Asia\',\'Asia\'],\n    \'country\':   [\'USA\',\'Brazil\',\'Canada\',\'Germany\',\'France\',\'China\',\'Japan\',\'India\'],\n    \'sector\':    [\'Tech\',\'Finance\',\'Mining\',\'Auto\',\'Pharma\',\'Tech\',\'Auto\',\'IT\'],\n    \'market_cap\':[2800, 400, 350, 680, 520, 1900, 750, 420],\n})\n\nfig = px.sunburst(df,\n    path=[\'continent\', \'country\', \'sector\'],\n    values=\'market_cap\',\n    color=\'market_cap\',\n    color_continuous_scale=\'Blues\',\n    title=\'Market Cap: Continent → Country → Sector ($ Bn)\',\n)\nfig.update_traces(\n    textinfo=\'label+percent parent\',\n    insidetextorientation=\'radial\',\n)\nfig.update_layout(height=550)\nfig.write_html(\'sunburst_portfolio.html\')\nprint(\'Sunburst saved\')"},
        {"label": "Treemap with custom text and color", "code": "import plotly.graph_objects as go\n\nlabels  = [\'Total\',\'A Div\',\'B Div\',\'C Div\',\'A1\',\'A2\',\'B1\',\'B2\',\'C1\',\'C2\',\'C3\']\nparents = [\'\',    \'Total\',\'Total\',\'Total\',\'A Div\',\'A Div\',\'B Div\',\'B Div\',\'C Div\',\'C Div\',\'C Div\']\nvalues  = [0,     0,      0,      0,      120,    80,     200,    150,    60,     90,     50]\n\nfig = go.Figure(go.Treemap(\n    labels=labels,\n    parents=parents,\n    values=values,\n    branchvalues=\'total\',\n    marker=dict(\n        colorscale=\'Viridis\',\n        showscale=True,\n        colorbar=dict(title=\'Revenue\'),\n    ),\n    texttemplate=\'<b>%{label}</b><br>$%{value}k\',\n    hovertemplate=\'<b>%{label}</b><br>Revenue: $%{value}k<br>Share: %{percentRoot:.1%}<extra></extra>\',\n))\nfig.update_layout(title=\'Division Revenue Treemap\', height=450)\nfig.write_html(\'treemap_custom.html\')\nprint(\'Custom treemap saved\')"}
    ],
"rw": {
    "title": "IT Infrastructure Cost Treemap",
    "scenario": "An IT manager visualizes cloud spending broken down by department > service > resource type to identify cost hotspots at a glance.",
    "code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(1)\ndepts = [\'Engineering\',\'Marketing\',\'Operations\']\nservices = [\'Compute\',\'Storage\',\'Database\',\'Network\']\ndata = []\nfor d in depts:\n    for svc in services:\n        cost = np.random.randint(500, 8000)\n        growth = np.random.uniform(-0.1, 0.3)\n        data.append({\'dept\': d, \'service\': svc, \'cost\': cost, \'growth_pct\': growth})\n\ndf = pd.DataFrame(data)\nfig = px.treemap(df,\n    path=[\'dept\', \'service\'],\n    values=\'cost\',\n    color=\'growth_pct\',\n    color_continuous_scale=\'RdYlGn_r\',\n    color_continuous_midpoint=0,\n    title=\'Cloud Cost by Dept → Service (color = MoM growth)\',\n    custom_data=[\'growth_pct\'],\n)\nfig.update_traces(\n    texttemplate=\'<b>%{label}</b><br>$%{value:,.0f}\',\n    hovertemplate=\'%{label}<br>Cost: $%{value:,.0f}<br>Growth: %{customdata[0]:.1%}<extra></extra>\',\n)\nfig.write_html(\'it_cost_treemap.html\')\nprint(f\'IT cost treemap saved — {df.cost.sum():,} total spend\')"
},
"practice": {
    "title": "File System Sunburst",
    "desc": "Build a sunburst showing a simulated file system: root → 3 folders (docs, src, data) → 2-3 files each with sizes (KB). Use go.Sunburst with branchvalues=\'total\'. Color by size. Show label+percent parent as text. Save as \'filesystem.html\'.",
    "starter": "import plotly.graph_objects as go\n\nlabels  = [\'root\',\'docs\',\'src\',\'data\',\n           \'report.pdf\',\'slides.pptx\',\n           \'main.py\',\'utils.py\',\'tests.py\',\n           \'train.csv\',\'test.csv\']\nparents = [\'\',\'root\',\'root\',\'root\',\n           \'docs\',\'docs\',\n           \'src\',\'src\',\'src\',\n           \'data\',\'data\']\nvalues  = [0, 0, 0, 0,\n           2048, 5120,\n           45, 30, 22,\n           10240, 4096]\n\n# TODO: create go.Sunburst with branchvalues=\'total\'\n# TODO: color by values, add textinfo=\'label+percent parent\'\nfig = go.Figure()\nfig.update_layout(title=\'File System Sunburst\')\nfig.write_html(\'filesystem.html\')\n"
}
},

{
"title": "19. Violin & Strip Charts",
"desc": "Violin plots combine a KDE curve with a box plot to show distribution shape. Strip/jitter plots show individual data points — great for small-to-medium datasets.",
"examples": [
        {"label": "Violin with box and points overlay", "code": "import plotly.express as px\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\ngroups = [\'Control\', \'Treatment A\', \'Treatment B\']\ndata = pd.concat([\n    pd.DataFrame({\'group\': g,\n                  \'score\': np.random.normal(loc, 12, 80)})\n    for g, loc in zip(groups, [50, 62, 71])\n])\n\nfig = px.violin(data, x=\'group\', y=\'score\', color=\'group\',\n                box=True, points=\'all\',\n                title=\'Score Distribution by Treatment Group\',\n                labels={\'score\': \'Test Score\', \'group\': \'Group\'},\n                color_discrete_sequence=px.colors.qualitative.Pastel)\n\nfig.update_traces(meanline_visible=True, jitter=0.3, pointpos=-1.8,\n                  marker=dict(size=4, opacity=0.5))\nfig.update_layout(showlegend=False, height=450)\nfig.write_html(\'violin_groups.html\')\nprint(\'Violin chart saved\')"},
        {"label": "Side-by-side violin for before/after", "code": "import plotly.graph_objects as go\nimport numpy as np\n\nnp.random.seed(10)\nbefore = np.random.normal(65, 15, 100)\nafter  = np.random.normal(72, 12, 100)\n\nfig = go.Figure()\nfig.add_trace(go.Violin(y=before, name=\'Before\',\n                         side=\'negative\', line_color=\'#636EFA\',\n                         fillcolor=\'rgba(99,110,250,0.3)\',\n                         box_visible=True, meanline_visible=True))\nfig.add_trace(go.Violin(y=after,  name=\'After\',\n                         side=\'positive\', line_color=\'#EF553B\',\n                         fillcolor=\'rgba(239,85,59,0.3)\',\n                         box_visible=True, meanline_visible=True))\n\nfig.update_layout(\n    title=\'Before vs After Intervention (Split Violin)\',\n    violingap=0, violinmode=\'overlay\',\n    yaxis_title=\'Score\',\n    template=\'plotly_white\',\n    height=420,\n)\nfig.write_html(\'violin_split.html\')\nprint(f\'Before mean: {before.mean():.1f}  After mean: {after.mean():.1f}\')"},
        {"label": "Strip plot (jitter) with mean markers", "code": "import plotly.express as px\nimport numpy as np, pandas as pd\n\nnp.random.seed(5)\ncategories = [\'Category A\', \'Category B\', \'Category C\', \'Category D\']\ndf = pd.concat([\n    pd.DataFrame({\'category\': cat, \'value\': np.random.exponential(scale, 50)})\n    for cat, scale in zip(categories, [10, 20, 15, 25])\n])\n\nfig = px.strip(df, x=\'category\', y=\'value\', color=\'category\',\n               title=\'Strip Plot with Individual Data Points\',\n               stripmode=\'overlay\',\n               color_discrete_sequence=px.colors.qualitative.Set2)\n\n# Add mean markers\nfor cat in categories:\n    mean_val = df[df.category == cat][\'value\'].mean()\n    fig.add_scatter(x=[cat], y=[mean_val], mode=\'markers\',\n                    marker=dict(symbol=\'line-ew\', size=20, color=\'black\', line_width=2),\n                    showlegend=False, hovertemplate=f\'Mean: {mean_val:.1f}\')\n\nfig.update_traces(jitter=0.4, marker_size=5, marker_opacity=0.6,\n                  selector=dict(type=\'strip\'))\nfig.update_layout(showlegend=False, height=420)\nfig.write_html(\'strip_plot.html\')\nprint(\'Strip plot saved\')"}
    ],
"rw": {
    "title": "A/B Test Distribution Comparison",
    "scenario": "A data scientist uses split violins to compare conversion rates and session durations between two website variants, showing both distribution shape and individual data points.",
    "code": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\nimport numpy as np\n\nnp.random.seed(99)\nmetrics = {\n    \'Conversion Rate (%)\': (np.random.beta(2, 20, 200)*100,\n                            np.random.beta(3, 20, 200)*100),\n    \'Session Duration (s)\': (np.random.exponential(120, 200),\n                             np.random.exponential(145, 200)),\n}\n\nfig = make_subplots(rows=1, cols=2, subplot_titles=list(metrics.keys()))\ncolors = [\'#636EFA\', \'#EF553B\']\n\nfor col, (metric, (ctrl, var)) in enumerate(metrics.items(), 1):\n    for data, name, side, color in [\n        (ctrl, \'Control\',  \'negative\', colors[0]),\n        (var,  \'Variant\',  \'positive\', colors[1]),\n    ]:\n        fig.add_trace(\n            go.Violin(y=data, name=name, side=side,\n                      line_color=color, box_visible=True,\n                      meanline_visible=True, showlegend=(col==1)),\n            row=1, col=col\n        )\n\nfig.update_layout(title=\'A/B Test: Control vs Variant\',\n                  violinmode=\'overlay\', template=\'plotly_white\',\n                  height=420)\nfig.write_html(\'ab_test_violin.html\')\nfor m, (c, v) in metrics.items():\n    print(f\'{m}: ctrl={c.mean():.1f} | var={v.mean():.1f} | lift={((v.mean()-c.mean())/c.mean())*100:.1f}%\')"
},
"practice": {
    "title": "Multi-Group Violin",
    "desc": "Generate exam scores for 4 subjects (Math, Science, English, History) with 60 students each (different means: 72, 68, 75, 65; std=12). Create a violin plot with box=True, points=\'outliers\'. Color by subject. Add a horizontal dashed line at score=70 (passing threshold). Save as \'exam_scores.html\'.",
    "starter": "import plotly.express as px\nimport plotly.graph_objects as go\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nsubjects = [\'Math\',\'Science\',\'English\',\'History\']\nmeans    = [72, 68, 75, 65]\n\ndata = pd.concat([\n    pd.DataFrame({\'subject\': s, \'score\': np.random.normal(m, 12, 60)})\n    for s, m in zip(subjects, means)\n])\ndata[\'score\'] = data[\'score\'].clip(0, 100)\n\n# TODO: create px.violin with box=True, points=\'outliers\'\n# TODO: add go.Scatter horizontal line at y=70 (passing threshold)\nfig = go.Figure()\nfig.update_layout(title=\'Exam Score Distributions\', height=430)\nfig.write_html(\'exam_scores.html\')\n"
}
},

{
"title": "20. Parallel Coordinates & Categories",
"desc": "Parallel coordinates show multi-dimensional continuous data on parallel axes — each line is one observation. Parallel categories (Sankey-style) show flows between categorical variables.",
"examples": [
        {"label": "Parallel coordinates for ML feature analysis", "code": "import plotly.express as px\nfrom sklearn.datasets import load_iris\nimport pandas as pd\n\niris = load_iris()\ndf = pd.DataFrame(iris.data, columns=iris.feature_names)\ndf[\'species\'] = iris.target  # 0, 1, 2\n\nfig = px.parallel_coordinates(\n    df,\n    color=\'species\',\n    dimensions=iris.feature_names,\n    color_continuous_scale=px.colors.diverging.Tealrose,\n    color_continuous_midpoint=1,\n    title=\'Iris Dataset — Parallel Coordinates\',\n    labels={n: n.replace(\' (cm)\', \'\') for n in iris.feature_names},\n)\nfig.update_layout(height=430)\nfig.write_html(\'parallel_coords_iris.html\')\nprint(\'Drag axes to filter! Saved.\')"},
        {"label": "Parallel coordinates with custom dimension ranges", "code": "import plotly.graph_objects as go\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nn = 200\ndf = pd.DataFrame({\n    \'age\':     np.random.randint(22, 65, n),\n    \'income\':  np.random.exponential(50000, n).clip(20000, 200000),\n    \'savings\': np.random.exponential(30000, n).clip(0, 150000),\n    \'credit\':  np.random.randint(300, 850, n),\n    \'loan\':    np.random.choice([0, 1], n, p=[0.7, 0.3]),\n})\n\nfig = go.Figure(go.Parcoords(\n    line=dict(color=df[\'loan\'], colorscale=\'RdYlGn_r\',\n              showscale=True, colorbar=dict(title=\'Default\')),\n    dimensions=[\n        dict(label=\'Age\', values=df[\'age\'], range=[22, 65]),\n        dict(label=\'Income ($)\', values=df[\'income\'], range=[20000, 200000]),\n        dict(label=\'Savings ($)\', values=df[\'savings\'], range=[0, 150000]),\n        dict(label=\'Credit Score\', values=df[\'credit\'], range=[300, 850]),\n    ],\n))\nfig.update_layout(title=\'Loan Default — Parallel Coordinates\',\n                  height=430, template=\'plotly_dark\')\nfig.write_html(\'parallel_loan.html\')\nprint(\'Loan parallel coords saved\')"},
        {"label": "Parallel categories (categorical Sankey flow)", "code": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(3)\nn = 500\ndf = pd.DataFrame({\n    \'region\':    np.random.choice([\'North\',\'South\',\'East\',\'West\'], n),\n    \'segment\':   np.random.choice([\'SMB\',\'Enterprise\',\'Consumer\'], n),\n    \'channel\':   np.random.choice([\'Online\',\'Retail\',\'Partner\'], n),\n    \'outcome\':   np.random.choice([\'Won\',\'Lost\',\'Pending\'], n, p=[0.4,0.4,0.2]),\n})\n\nfig = px.parallel_categories(\n    df,\n    dimensions=[\'region\',\'segment\',\'channel\',\'outcome\'],\n    color=df[\'outcome\'].map({\'Won\': 0, \'Pending\': 0.5, \'Lost\': 1}),\n    color_continuous_scale=\'RdYlGn_r\',\n    title=\'Sales Pipeline Flow: Region → Segment → Channel → Outcome\',\n)\nfig.update_layout(height=450)\nfig.write_html(\'parallel_categories.html\')\nprint(\'Parallel categories chart saved\')"}
    ],
"rw": {
    "title": "Model Feature Explorer",
    "scenario": "An ML team uses parallel coordinates on their validation set to interactively filter observations — dragging axes to isolate the feature ranges where the model underperforms.",
    "code": "import plotly.express as px\nimport numpy as np, pandas as pd\nfrom sklearn.datasets import load_wine\n\nwine = load_wine()\ndf = pd.DataFrame(wine.data, columns=wine.feature_names)\ndf[\'class\'] = wine.target\ndf[\'error\'] = np.random.choice([0, 1], len(df), p=[0.8, 0.2])\n\n# Use only most informative features\ntop_features = [\'alcohol\', \'malic_acid\', \'flavanoids\',\n                \'color_intensity\', \'proline\']\n\nfig = px.parallel_coordinates(\n    df,\n    color=\'class\',\n    dimensions=top_features + [\'class\'],\n    color_continuous_scale=px.colors.sequential.Viridis,\n    title=\'Wine Dataset — Feature Space by Class\',\n    labels={f: f.replace(\'_\', \' \').title() for f in top_features},\n)\nfig.update_layout(height=430)\nfig.write_html(\'wine_parallel.html\')\nprint(f\'Wine parallel coords: {len(df)} samples, {len(top_features)} features\')"
},
"practice": {
    "title": "Car Dataset Explorer",
    "desc": "Using px.data.cars() (or generate synthetic data: mpg, cylinders, horsepower, weight, model_year), create a parallel coordinates chart colored by \'cylinders\'. Add a second chart using px.parallel_categories with columns cylinders and origin. Save both as \'cars_parcoord.html\' and \'cars_parcat.html\'.",
    "starter": "import plotly.express as px\nimport pandas as pd\nimport numpy as np\n\n# Use built-in cars dataset\ntry:\n    df = px.data.cars()\nexcept Exception:\n    np.random.seed(42)\n    n = 200\n    df = pd.DataFrame({\n        \'mpg\': np.random.normal(23, 7, n).clip(8, 46),\n        \'cylinders\': np.random.choice([4, 6, 8], n, p=[0.5, 0.3, 0.2]),\n        \'horsepower\': np.random.normal(100, 40, n).clip(40, 230),\n        \'weight\': np.random.normal(2800, 700, n).clip(1600, 5000),\n        \'model_year\': np.random.randint(70, 83, n),\n        \'origin\': np.random.choice([\'USA\',\'Europe\',\'Japan\'], n),\n    })\n\n# TODO: parallel_coordinates colored by cylinders\n# TODO: parallel_categories with cylinders and origin\n"
}
},

{
"title": "21. Funnel & Waterfall Charts",
"desc": "Funnel charts show sequential stage drop-off (sales pipelines, conversion funnels). Waterfall charts show cumulative effects of positive and negative values — perfect for P&L statements.",
"examples": [
        {"label": "Sales funnel with conversion rates", "code": "import plotly.graph_objects as go\n\nstages = [\'Website Visits\', \'Product Views\', \'Add to Cart\',\n          \'Checkout Started\', \'Purchase Completed\']\ncounts = [10000, 5200, 2100, 980, 420]\n\nconversion = [f\'{counts[i]/counts[i-1]:.0%}\' if i > 0 else \'100%\'\n              for i in range(len(counts))]\n\nfig = go.Figure(go.Funnel(\n    y=stages,\n    x=counts,\n    textposition=\'inside\',\n    textinfo=\'value+percent previous\',\n    opacity=0.85,\n    marker=dict(\n        color=[\'#636EFA\',\'#EF553B\',\'#00CC96\',\'#AB63FA\',\'#FFA15A\'],\n        line=dict(width=2, color=\'white\'),\n    ),\n    connector=dict(line=dict(color=\'#888\', width=1)),\n))\nfig.update_layout(\n    title=\'E-Commerce Conversion Funnel\',\n    template=\'plotly_white\',\n    height=420,\n    margin=dict(l=200),\n)\nfig.write_html(\'sales_funnel.html\')\nprint(f\'Overall conversion: {counts[-1]/counts[0]:.1%}\')"},
        {"label": "Waterfall chart for P&L statement", "code": "import plotly.graph_objects as go\n\nitems   = [\'Revenue\',\'COGS\',\'Gross Profit\',\'R&D\',\n           \'S&M\',\'G&A\',\'EBITDA\',\'D&A\',\'EBIT\']\nvalues  = [1000, -380, None, -150, -120, -80, None, -45, None]\nmeasure = [\'absolute\',\'relative\',\'total\',\'relative\',\n           \'relative\',\'relative\',\'total\',\'relative\',\'total\']\ntext    = [f\'${abs(v):,}\' if v else \'\' for v in values]\n\nfig = go.Figure(go.Waterfall(\n    orientation=\'v\',\n    measure=measure,\n    x=items,\n    y=values,\n    text=text,\n    textposition=\'outside\',\n    increasing=dict(marker_color=\'#26a69a\'),\n    decreasing=dict(marker_color=\'#ef5350\'),\n    totals=dict(marker_color=\'#636EFA\'),\n    connector=dict(line=dict(color=\'#999\', width=1, dash=\'dot\')),\n))\nfig.update_layout(\n    title=\'P&L Waterfall — Q4 2024\',\n    yaxis_title=\'$ Thousands\',\n    template=\'plotly_white\',\n    height=450,\n    showlegend=False,\n)\nfig.write_html(\'pnl_waterfall.html\')\nprint(\'P&L waterfall saved\')"},
        {"label": "Funnel area and horizontal funnel", "code": "import plotly.express as px\nimport plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\n\nstages = [\'Awareness\',\'Interest\',\'Consideration\',\'Intent\',\'Purchase\']\nvalues = [50000, 22000, 8500, 3200, 980]\n\nfig = make_subplots(rows=1, cols=2,\n                    subplot_titles=[\'Standard Funnel\', \'Funnel Area\'],\n                    specs=[[{\'type\':\'funnel\'}, {\'type\':\'funnelarea\'}]])\n\nfig.add_trace(\n    go.Funnel(y=stages, x=values, textinfo=\'value+percent initial\',\n              marker_color=px.colors.sequential.Blues_r[1:]),\n    row=1, col=1)\n\nfig.add_trace(\n    go.Funnelarea(labels=stages, values=values,\n                  textinfo=\'label+percent\',\n                  marker_colors=px.colors.sequential.Greens_r[1:]),\n    row=1, col=2)\n\nfig.update_layout(title=\'Marketing Funnel Comparison\', height=420)\nfig.write_html(\'funnel_comparison.html\')\nprint(f\'Top-of-funnel to purchase: {values[-1]/values[0]:.1%}\')"}
    ],
"rw": {
    "title": "SaaS Revenue Waterfall",
    "scenario": "A CFO presents monthly recurring revenue changes: starting ARR, new business, expansions, contractions, and churn — visualized as a waterfall to show net revenue change.",
    "code": "import plotly.graph_objects as go\nimport numpy as np\n\nmonths = [\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\']\nstarting_arr = 500\n\ndata_rows = []\nfor m in months:\n    new_biz    = np.random.randint(15, 40)\n    expansion  = np.random.randint(5, 20)\n    contraction= -np.random.randint(2, 10)\n    churn      = -np.random.randint(5, 20)\n    data_rows.append((m, new_biz, expansion, contraction, churn))\n\nitems   = [\'Start\']\nvalues  = [starting_arr]\nmeasure = [\'absolute\']\n\nfor month, new, exp, con, churn in data_rows:\n    items   += [f\'{month} New\', f\'{month} Exp\', f\'{month} Con\', f\'{month} Churn\']\n    values  += [new, exp, con, churn]\n    measure += [\'relative\',\'relative\',\'relative\',\'relative\']\n\nitems.append(\'End ARR\')\nvalues.append(None)\nmeasure.append(\'total\')\n\nfig = go.Figure(go.Waterfall(\n    x=items, y=values, measure=measure,\n    increasing=dict(marker_color=\'#26a69a\'),\n    decreasing=dict(marker_color=\'#ef5350\'),\n    totals=dict(marker_color=\'#636EFA\'),\n    textposition=\'outside\', texttemplate=\'%{y:+.0f}\',\n))\nfig.update_layout(title=\'SaaS ARR Waterfall (H1 2024)\', height=450,\n                  template=\'plotly_white\', xaxis_tickangle=45)\nfig.write_html(\'saas_waterfall.html\')\nprint(\'SaaS waterfall saved\')"
},
"practice": {
    "title": "Budget Variance Waterfall",
    "desc": "Create a waterfall chart showing budget vs actuals for 5 departments: start with \'Budget Total\' at 1,000,000. Show each department as a relative bar (some over, some under). End with \'Actual Total\' as a total bar. Color over-budget red, under-budget green. Save as \'budget_variance.html\'.",
    "starter": "import plotly.graph_objects as go\n\ndepartments = [\'Engineering\',\'Marketing\',\'Sales\',\'Operations\',\'HR\']\nbudget_each = [200000, 150000, 180000, 120000, 100000]  # sums to 750k; rest is overhead\nvariances   = [+15000, -8000, +22000, -5000, +3000]      # actual - budget per dept\n\nitems   = [\'Budget Total\'] + departments + [\'Overhead\', \'Actual Total\']\n# TODO: set up values list (budget_total=750000, then variances, then overhead=250000, total=None)\n# TODO: set up measure list\n# TODO: create go.Waterfall with increasing green, decreasing red\nfig = go.Figure()\nfig.update_layout(title=\'Budget Variance Waterfall\', height=430)\nfig.write_html(\'budget_variance.html\')\n"
}
},

{
"title": "22. Indicator & Gauge Charts",
"desc": "go.Indicator renders KPI numbers, delta comparisons, and gauge/speedometer charts. Combine them in subplots to build executive dashboards without any extra libraries.",
"examples": [
        {"label": "KPI indicators with delta", "code": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\n\nfig = make_subplots(rows=1, cols=4,\n                    specs=[[{\'type\':\'indicator\'}]*4])\n\nkpis = [\n    (\'Revenue\',  \'1.24M\',  1_240_000, 1_100_000),\n    (\'Users\',    \'48.3K\',  48_300,    45_100),\n    (\'Churn %\',  \'2.1%\',   2.1,       2.8),\n    (\'NPS\',      \'67\',     67,        61),\n]\n\nfor col, (name, num_str, val, ref) in enumerate(kpis, 1):\n    better_if_lower = \'churn\' in name.lower()\n    fig.add_trace(go.Indicator(\n        mode=\'number+delta\',\n        value=val,\n        title=dict(text=name, font=dict(size=14)),\n        delta=dict(\n            reference=ref,\n            increasing=dict(color=\'red\' if better_if_lower else \'green\'),\n            decreasing=dict(color=\'green\' if better_if_lower else \'red\'),\n            valueformat=\'.1%\' if \'%\' in num_str else None,\n        ),\n        number=dict(\n            prefix=\'$\' if \'M\' in num_str else \'\',\n            suffix=\'%\' if \'%\' in num_str else \'\',\n        ),\n    ), row=1, col=col)\n\nfig.update_layout(title=\'Business KPI Dashboard\', height=200,\n                  template=\'plotly_dark\', margin=dict(t=50, b=20))\nfig.write_html(\'kpi_indicators.html\')\nprint(\'KPI dashboard saved\')"},
        {"label": "Gauge / speedometer chart", "code": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\n\nfig = make_subplots(rows=1, cols=3,\n                    specs=[[{\'type\':\'indicator\'}]*3])\n\ngauges = [\n    (\'CPU Usage\', 73, \'%\', \'red\', [(0,40,\'green\'),(40,70,\'yellow\'),(70,100,\'red\')]),\n    (\'Memory\',    58, \'%\', \'orange\', [(0,60,\'green\'),(60,80,\'orange\'),(80,100,\'red\')]),\n    (\'SLA Score\', 96.5, \'%\', \'green\', [(0,90,\'red\'),(90,95,\'yellow\'),(95,100,\'green\')]),\n]\n\nfor col, (name, val, suffix, color, steps) in enumerate(gauges, 1):\n    fig.add_trace(go.Indicator(\n        mode=\'gauge+number+delta\',\n        value=val,\n        title=dict(text=name, font=dict(size=14)),\n        delta=dict(reference=80 if \'SLA\' not in name else 95),\n        number=dict(suffix=suffix),\n        gauge=dict(\n            axis=dict(range=[0, 100]),\n            bar=dict(color=color, thickness=0.25),\n            steps=[dict(range=[lo, hi], color=c) for lo, hi, c in steps],\n            threshold=dict(line=dict(color=\'white\', width=3),\n                           thickness=0.75, value=val),\n        ),\n    ), row=1, col=col)\n\nfig.update_layout(title=\'Infrastructure Gauges\', height=280,\n                  template=\'plotly_dark\', margin=dict(t=60, b=10))\nfig.write_html(\'gauges.html\')\nprint(\'Gauge dashboard saved\')"},
        {"label": "Bullet chart style indicator", "code": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\n\nmetrics = [\n    (\'Q1 Revenue\',   1.15, 1.25, \'M$\'),\n    (\'Q1 Leads\',     430,  500,  \'\'),\n    (\'Avg Deal ($)\', 22500, 20000, \'$\'),\n    (\'Win Rate\',     42,   40,   \'%\'),\n]\n\nfig = make_subplots(rows=len(metrics), cols=1,\n                    specs=[[{\'type\':\'indicator\'}]] * len(metrics),\n                    vertical_spacing=0.0)\n\nfor row, (name, actual, target, unit) in enumerate(metrics, 1):\n    color = \'green\' if actual >= target else \'red\'\n    fig.add_trace(go.Indicator(\n        mode=\'number+gauge+delta\',\n        value=actual,\n        title=dict(text=name, font=dict(size=12)),\n        delta=dict(reference=target,\n                   relative=True,\n                   increasing=dict(color=\'green\'),\n                   decreasing=dict(color=\'red\')),\n        number=dict(prefix=unit if unit==\'$\' else \'\',\n                    suffix=unit if unit!=\'$\' else \'\'),\n        gauge=dict(\n            shape=\'bullet\',\n            axis=dict(range=[0, target*1.5]),\n            threshold=dict(value=target,\n                           line=dict(color=\'black\', width=2),\n                           thickness=0.75),\n            bar=dict(color=color),\n        ),\n    ), row=row, col=1)\n\nfig.update_layout(title=\'Q1 Performance vs Target\',\n                  height=360, template=\'plotly_white\',\n                  margin=dict(l=160, t=60, b=20))\nfig.write_html(\'bullet_chart.html\')\nprint(\'Bullet chart saved\')"}
    ],
"rw": {
    "title": "Executive SaaS Dashboard",
    "scenario": "A SaaS company\'s weekly executive report shows ARR, MRR growth, churn rate, and NPS as KPI indicators with week-over-week deltas and color coding.",
    "code": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\nimport numpy as np\n\n# Simulate current vs previous week metrics\nnp.random.seed(42)\nmetrics = {\n    \'ARR ($M)\':    (4.82,  4.71,  False),\n    \'MRR Growth%\': (3.2,   2.8,   False),\n    \'Churn %\':     (1.8,   2.1,   True),   # lower is better\n    \'NPS\':         (71,    68,    False),\n    \'CAC ($)\':     (1250,  1380,  True),    # lower is better\n    \'LTV/CAC\':     (4.8,   4.2,   False),\n}\n\nn = len(metrics)\nfig = make_subplots(rows=2, cols=3,\n                    specs=[[{\'type\':\'indicator\'}]*3]*2)\n\nfor idx, (name, (curr, prev, lower_better)) in enumerate(metrics.items()):\n    row, col = divmod(idx, 3)\n    fig.add_trace(go.Indicator(\n        mode=\'number+delta\',\n        value=curr,\n        title=dict(text=name, font=dict(size=13)),\n        delta=dict(\n            reference=prev,\n            relative=True,\n            increasing=dict(color=\'red\' if lower_better else \'green\'),\n            decreasing=dict(color=\'green\' if lower_better else \'red\'),\n        ),\n    ), row=row+1, col=col+1)\n\nfig.update_layout(title=\'SaaS Weekly KPI Report\',\n                  height=320, template=\'plotly_dark\',\n                  margin=dict(t=60, b=20))\nfig.write_html(\'saas_kpi.html\')\nprint(\'SaaS KPI report saved\')"
},
"practice": {
    "title": "OKR Progress Gauges",
    "desc": "Create 4 gauge indicators in a 2x2 subplot grid, one per OKR: (1) Revenue Target: 85% achieved (target 100), (2) Customer Satisfaction: 4.2/5, (3) Bug Backlog: 23 (target <30, lower is better), (4) Feature Delivery: 7/10 shipped. Use colored gauge steps (red/yellow/green). Save as \'okr_gauges.html\'.",
    "starter": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\n\nfig = make_subplots(rows=2, cols=2,\n                    specs=[[{\'type\':\'indicator\'}]*2]*2)\n\nokrs = [\n    (\'Revenue Target\',      85,   100,  \'%\',  [(0,60,\'red\'),(60,80,\'yellow\'),(80,100,\'green\')]),\n    (\'Cust. Satisfaction\',  4.2,  5,    \'/5\', [(0,3,\'red\'),(3,4,\'yellow\'),(4,5,\'green\')]),\n    (\'Bug Backlog\',         23,   30,   \'\',   [(0,15,\'green\'),(15,25,\'yellow\'),(25,30,\'red\')]),\n    (\'Feature Delivery\',    7,    10,   \'/10\',[(0,5,\'red\'),(5,7,\'yellow\'),(7,10,\'green\')]),\n]\n\nfor idx, (name, val, max_val, suffix, steps) in enumerate(okrs):\n    row, col = divmod(idx, 2)\n    # TODO: add go.Indicator with mode=\'gauge+number\', gauge steps, threshold at target\n    pass\n\nfig.update_layout(title=\'OKR Progress Gauges\', height=480, template=\'plotly_dark\')\nfig.write_html(\'okr_gauges.html\')\n"
}
},

{
"title": "23. Animated Bar Chart Race & Timelines",
"desc": "Plotly animations use frames and sliders to animate data over time. Bar chart races, animated scatter plots, and timeline maps reveal how data evolves.",
"examples": [
        {"label": "Bar chart race with animation frames", "code": "import plotly.graph_objects as go\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\ncompanies = [\'Alpha\',\'Beta\',\'Gamma\',\'Delta\',\'Epsilon\',\'Zeta\']\nyears = list(range(2015, 2025))\n\n# Generate cumulative revenue data\nrevenues = {c: np.cumsum(np.random.exponential(10, len(years))) * (1 + 0.1 * i)\n            for i, c in enumerate(companies)}\ndf = pd.DataFrame(revenues, index=years)\n\nframes = []\nfor year in years:\n    row = df.loc[year].sort_values(ascending=True)\n    frames.append(go.Frame(\n        data=[go.Bar(x=row.values, y=row.index,\n                     orientation=\'h\',\n                     marker_color=px_colors := [\n                         \'#636EFA\',\'#EF553B\',\'#00CC96\',\'#AB63FA\',\n                         \'#FFA15A\',\'#19D3F3\'][:len(row)],\n                     text=[f\'${v:.0f}B\' for v in row.values],\n                     textposition=\'outside\')],\n        name=str(year),\n        layout=go.Layout(title_text=f\'Company Revenue Race — {year}\')\n    ))\n\nfirst = df.loc[years[0]].sort_values(ascending=True)\nfig = go.Figure(\n    data=[go.Bar(x=first.values, y=first.index, orientation=\'h\',\n                 marker_color=[\'#636EFA\',\'#EF553B\',\'#00CC96\',\n                               \'#AB63FA\',\'#FFA15A\',\'#19D3F3\'][:len(first)],\n                 text=[f\'${v:.0f}B\' for v in first.values],\n                 textposition=\'outside\')],\n    frames=frames,\n    layout=go.Layout(\n        title=f\'Company Revenue Race — {years[0]}\',\n        xaxis=dict(range=[0, df.values.max()*1.15], title=\'Revenue ($B)\'),\n        updatemenus=[dict(type=\'buttons\', showactive=False,\n                          buttons=[dict(label=\'Play\',\n                                       method=\'animate\',\n                                       args=[None, dict(frame=dict(duration=600, redraw=True),\n                                                        fromcurrent=True)])])],\n        sliders=[dict(steps=[dict(method=\'animate\', args=[[str(y)]], label=str(y))\n                             for y in years],\n                      currentvalue=dict(prefix=\'Year: \'))],\n        height=450, template=\'plotly_dark\',\n    )\n)\nfig.write_html(\'bar_race.html\')\nprint(\'Bar chart race saved\')"},
        {"label": "Animated scatter over time", "code": "import plotly.express as px\n\ndf = px.data.gapminder()\n\nfig = px.scatter(\n    df, x=\'gdpPercap\', y=\'lifeExp\',\n    animation_frame=\'year\',\n    animation_group=\'country\',\n    size=\'pop\', color=\'continent\',\n    hover_name=\'country\',\n    log_x=True,\n    size_max=55,\n    range_x=[100, 100_000],\n    range_y=[25, 90],\n    title=\'Gapminder: GDP vs Life Expectancy (1952-2007)\',\n    labels={\'gdpPercap\': \'GDP per Capita\', \'lifeExp\': \'Life Expectancy\'},\n    template=\'plotly_white\',\n)\nfig.update_layout(height=500)\nfig.write_html(\'gapminder_animation.html\')\nprint(f\'Animated scatter: {df.year.nunique()} frames, {df.country.nunique()} countries\')"},
        {"label": "Animated choropleth map", "code": "import plotly.express as px\n\ndf = px.data.gapminder()\n\nfig = px.choropleth(\n    df,\n    locations=\'iso_alpha\',\n    color=\'lifeExp\',\n    hover_name=\'country\',\n    animation_frame=\'year\',\n    color_continuous_scale=\'RdYlGn\',\n    range_color=[25, 90],\n    title=\'World Life Expectancy Over Time (1952-2007)\',\n    labels={\'lifeExp\': \'Life Expectancy\'},\n    projection=\'natural earth\',\n)\nfig.update_layout(\n    coloraxis_colorbar=dict(title=\'Life Exp.\', x=1.0),\n    height=480,\n    geo=dict(showframe=False, showcoastlines=False),\n)\nfig.write_html(\'choropleth_animated.html\')\nprint(\'Animated choropleth saved\')"}
    ],
"rw": {
    "title": "Market Share Race",
    "scenario": "A market analyst builds a bar chart race showing quarterly market share shifts between 5 smartphone brands over 3 years, helping executives spot disruption trends.",
    "code": "import plotly.graph_objects as go\nimport numpy as np, pandas as pd\n\nnp.random.seed(7)\nbrands  = [\'AlphaPhone\',\'BetaMobile\',\'GammaDevice\',\'DeltaTech\',\'EpsilonX\']\nquarters= [f\'Q{q} {y}\' for y in range(2021,2025) for q in range(1,5)]\n\n# Market share that sums to 100% each quarter\nraw = np.random.dirichlet(np.ones(len(brands)), len(quarters)) * 100\ndf  = pd.DataFrame(raw, columns=brands, index=quarters)\n\nframes = []\nfor q in quarters:\n    row = df.loc[q].sort_values(ascending=True)\n    frames.append(go.Frame(\n        data=[go.Bar(x=row.values, y=row.index, orientation=\'h\',\n                     text=[f\'{v:.1f}%\' for v in row.values],\n                     textposition=\'outside\',\n                     marker_color=[\'#636EFA\',\'#EF553B\',\'#00CC96\',\'#AB63FA\',\'#FFA15A\'][:len(row)])],\n        name=q,\n        layout=go.Layout(title_text=f\'Smartphone Market Share — {q}\')\n    ))\n\nfirst = df.iloc[0].sort_values(ascending=True)\nfig = go.Figure(\n    data=[go.Bar(x=first.values, y=first.index, orientation=\'h\',\n                 text=[f\'{v:.1f}%\' for v in first.values], textposition=\'outside\',\n                 marker_color=[\'#636EFA\',\'#EF553B\',\'#00CC96\',\'#AB63FA\',\'#FFA15A\'])],\n    frames=frames,\n    layout=go.Layout(\n        title=f\'Smartphone Market Share — {quarters[0]}\',\n        xaxis=dict(range=[0, 45], title=\'Market Share (%)\'),\n        updatemenus=[dict(type=\'buttons\', showactive=False,\n                          buttons=[dict(label=\'▶ Play\', method=\'animate\',\n                                        args=[None, dict(frame=dict(duration=700))])])],\n        sliders=[dict(steps=[dict(method=\'animate\', args=[[q]], label=q) for q in quarters],\n                      currentvalue=dict(prefix=\'Quarter: \'))],\n        template=\'plotly_dark\', height=450,\n    )\n)\nfig.write_html(\'market_share_race.html\')\nprint(f\'Race saved: {len(quarters)} quarters\')"
},
"practice": {
    "title": "Population Pyramid Animation",
    "desc": "Generate synthetic population data for age groups (0-9, 10-19, ..., 70+) across 5 decades (1980-2020). Build an animated horizontal bar chart race where each frame is a decade. Use negative values for female population to create a butterfly/pyramid effect. Save as \'population_pyramid.html\'.",
    "starter": "import plotly.graph_objects as go\nimport numpy as np\n\nage_groups = [\'0-9\',\'10-19\',\'20-29\',\'30-39\',\'40-49\',\'50-59\',\'60-69\',\'70+\']\ndecades = [1980, 1990, 2000, 2010, 2020]\n\nnp.random.seed(42)\nframes = []\nfor decade in decades:\n    # Generate male/female populations (in millions)\n    base = np.random.exponential(5, len(age_groups)) + 2\n    male   =  base + np.random.randn(len(age_groups))\n    female = -(base + np.random.randn(len(age_groups)))\n    frames.append(go.Frame(\n        data=[\n            go.Bar(y=age_groups, x=male,   orientation=\'h\', name=\'Male\'),\n            # TODO: add female Bar trace with negative values\n        ],\n        name=str(decade),\n        layout=go.Layout(title_text=f\'Population Pyramid — {decade}\')\n    ))\n\n# TODO: create fig with first frame data, frames, updatemenus, sliders\nfig = go.Figure()\nfig.update_layout(title=\'Population Pyramid\', barmode=\'overlay\',\n                  xaxis_title=\'Population (M)\', height=450)\nfig.write_html(\'population_pyramid.html\')\n"
}
},

{
"title": "24. Custom Templates & Styling",
"desc": "Plotly templates define default colors, fonts, backgrounds, and axis styles. Create reusable brand templates with pio.templates and apply them globally or per-chart.",
"examples": [
        {"label": "Creating and applying a custom template", "code": "import plotly.graph_objects as go\nimport plotly.io as pio\nimport plotly.express as px\n\n# Define a brand template\nbrand_template = go.layout.Template(\n    layout=go.Layout(\n        font=dict(family=\'Arial\', size=13, color=\'#2c2c2c\'),\n        paper_bgcolor=\'#f8f9fa\',\n        plot_bgcolor=\'#ffffff\',\n        colorway=[\'#005A9E\',\'#E63946\',\'#06D6A0\',\'#FFB703\',\'#8338EC\'],\n        title=dict(font=dict(size=18, color=\'#005A9E\', family=\'Arial Bold\')),\n        xaxis=dict(gridcolor=\'#e9ecef\', linecolor=\'#dee2e6\', zeroline=False),\n        yaxis=dict(gridcolor=\'#e9ecef\', linecolor=\'#dee2e6\', zeroline=False),\n        legend=dict(bgcolor=\'rgba(255,255,255,0.8)\',\n                    bordercolor=\'#dee2e6\', borderwidth=1),\n        hoverlabel=dict(bgcolor=\'white\', font_size=12,\n                        bordercolor=\'#dee2e6\'),\n    )\n)\n\n# Register the template\npio.templates[\'brand\'] = brand_template\npio.templates.default = \'brand\'   # set as global default\n\nimport numpy as np, pandas as pd\nnp.random.seed(42)\ndf = pd.DataFrame({\n    \'month\': pd.date_range(\'2024-01\', periods=12, freq=\'MS\'),\n    \'product_a\': np.cumsum(np.random.randn(12)*5) + 100,\n    \'product_b\': np.cumsum(np.random.randn(12)*4) + 80,\n})\n\nfig = px.line(df, x=\'month\', y=[\'product_a\',\'product_b\'],\n              title=\'Monthly Sales — Brand Template\',\n              labels={\'value\':\'Revenue ($K)\', \'variable\':\'Product\'})\nfig.write_html(\'brand_template.html\')\nprint(\'Brand template chart saved\')\n\n# Reset to default\npio.templates.default = \'plotly\'"},
        {"label": "Dark theme with custom accent colors", "code": "import plotly.graph_objects as go\nimport plotly.io as pio\nimport numpy as np, pandas as pd\n\ndark_template = go.layout.Template(\n    layout=dict(\n        paper_bgcolor=\'#0d1117\',\n        plot_bgcolor=\'#0d1117\',\n        font=dict(color=\'#c9d1d9\', family=\'JetBrains Mono, monospace\'),\n        colorway=[\'#79c0ff\',\'#ff7b72\',\'#56d364\',\'#d2a8ff\',\'#ffa657\',\'#39c5cf\'],\n        xaxis=dict(gridcolor=\'#30363d\', linecolor=\'#30363d\',\n                   tickcolor=\'#8b949e\', title_font_color=\'#8b949e\'),\n        yaxis=dict(gridcolor=\'#30363d\', linecolor=\'#30363d\',\n                   tickcolor=\'#8b949e\', title_font_color=\'#8b949e\'),\n        title=dict(font=dict(color=\'#79c0ff\', size=17)),\n        legend=dict(bgcolor=\'#161b22\', bordercolor=\'#30363d\', borderwidth=1),\n        hoverlabel=dict(bgcolor=\'#161b22\', bordercolor=\'#30363d\',\n                        font=dict(color=\'#c9d1d9\')),\n    )\n)\npio.templates[\'github_dark\'] = dark_template\n\nnp.random.seed(42)\ncategories = [\'Q1\',\'Q2\',\'Q3\',\'Q4\']\nproducts   = [\'Widget\',\'Gadget\',\'Gizmo\']\nfig = go.Figure()\nfor p in products:\n    fig.add_trace(go.Bar(name=p, x=categories,\n                          y=np.random.randint(50, 200, 4),\n                          text=np.random.randint(50, 200, 4),\n                          texttemplate=\'%{text}\',\n                          textposition=\'outside\'))\nfig.update_layout(title=\'Quarterly Sales — GitHub Dark Theme\',\n                  template=\'github_dark\', barmode=\'group\', height=430)\nfig.write_html(\'dark_theme.html\')\nprint(\'Dark theme chart saved\')"},
        {"label": "Per-trace styling and annotations", "code": "import plotly.graph_objects as go\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nx = pd.date_range(\'2024-01\', periods=52, freq=\'W\')\nactual   = 100 + np.cumsum(np.random.randn(52) * 3)\nforecast = actual[-1] + np.cumsum(np.random.randn(12) * 2.5)\nupper_ci = forecast + 1.96 * np.arange(1, 13) * 0.8\nlower_ci = forecast - 1.96 * np.arange(1, 13) * 0.8\nfuture_x = pd.date_range(x[-1], periods=13, freq=\'W\')[1:]\n\nfig = go.Figure()\n\n# Actual data\nfig.add_trace(go.Scatter(x=x, y=actual, name=\'Actual\',\n                          line=dict(color=\'#636EFA\', width=2.5)))\n\n# Forecast with confidence interval fill\nfig.add_trace(go.Scatter(x=future_x, y=upper_ci, name=\'Upper CI 95%\',\n                          line=dict(color=\'rgba(255,127,14,0)\', width=0),\n                          showlegend=False))\nfig.add_trace(go.Scatter(x=future_x, y=lower_ci, name=\'Lower CI 95%\',\n                          line=dict(color=\'rgba(255,127,14,0)\', width=0),\n                          fill=\'tonexty\', fillcolor=\'rgba(255,127,14,0.2)\',\n                          showlegend=False))\nfig.add_trace(go.Scatter(x=future_x, y=forecast, name=\'Forecast\',\n                          line=dict(color=\'#FF7F0E\', width=2, dash=\'dash\')))\n\n# Annotation for forecast start\nfig.add_vline(x=x[-1], line_dash=\'dot\', line_color=\'gray\', opacity=0.7)\nfig.add_annotation(x=x[-1], y=actual[-1], text=\'Forecast begins\',\n                    showarrow=True, arrowhead=2, bgcolor=\'rgba(0,0,0,0.6)\',\n                    font=dict(color=\'white\'))\n\nfig.update_layout(title=\'Revenue Actual + 12-Week Forecast with CI\',\n                  xaxis_title=\'Date\', yaxis_title=\'Revenue ($K)\',\n                  template=\'plotly_dark\', height=430, hovermode=\'x unified\')\nfig.write_html(\'forecast_styled.html\')\nprint(\'Styled forecast chart saved\')"}
    ],
"rw": {
    "title": "Branded Marketing Report",
    "scenario": "A marketing team builds a reusable company-branded Plotly template with corporate fonts and colors, then applies it to all quarterly charts for consistent reporting.",
    "code": "import plotly.graph_objects as go\nimport plotly.io as pio\nimport plotly.express as px\nimport numpy as np, pandas as pd\n\n# Corporate brand template\npio.templates[\'corporate\'] = go.layout.Template(\n    layout=dict(\n        font=dict(family=\'Helvetica Neue, sans-serif\', size=13),\n        paper_bgcolor=\'#FFFFFF\',\n        plot_bgcolor=\'#FAFAFA\',\n        colorway=[\'#1A237E\',\'#283593\',\'#3949AB\',\'#5C6BC0\',\'#7986CB\'],\n        title=dict(font=dict(size=16, color=\'#1A237E\', family=\'Helvetica Neue Bold\')),\n        xaxis=dict(gridcolor=\'#EEEEEE\', linecolor=\'#BDBDBD\'),\n        yaxis=dict(gridcolor=\'#EEEEEE\', linecolor=\'#BDBDBD\'),\n        legend=dict(bgcolor=\'rgba(255,255,255,0.9)\'),\n    )\n)\n\nnp.random.seed(5)\nmonths = pd.date_range(\'2024-01\', periods=12, freq=\'MS\')\nchannels = [\'Organic\',\'Paid\',\'Email\',\'Social\']\ndata = {c: np.random.randint(200, 800, 12) for c in channels}\ndf = pd.DataFrame(data, index=months).reset_index().rename(columns={\'index\':\'month\'})\ndf_melt = df.melt(\'month\', var_name=\'channel\', value_name=\'leads\')\n\nfig = px.area(df_melt, x=\'month\', y=\'leads\', color=\'channel\',\n              title=\'Marketing Leads by Channel — Corporate Theme\',\n              template=\'corporate\')\nfig.update_traces(opacity=0.8)\nfig.write_html(\'corporate_report.html\')\nprint(f\'Corporate report saved — {df_melt.leads.sum():,} total leads\')"
},
"practice": {
    "title": "Dashboard Layout",
    "desc": "Create a 2x2 subplot dashboard using make_subplots: (top-left) line chart of weekly sales, (top-right) bar chart of sales by region, (bottom-left) scatter of spend vs revenue, (bottom-right) pie chart of channel mix. Apply a consistent dark template. Add a main title. Save as \'dashboard.html\'.",
    "starter": "import plotly.graph_objects as go\nfrom plotly.subplots import make_subplots\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nweeks   = pd.date_range(\'2024-01\', periods=20, freq=\'W\')\nsales   = 100 + np.cumsum(np.random.randn(20)*5)\nregions = [\'North\',\'South\',\'East\',\'West\']\nreg_sales = np.random.randint(200, 600, 4)\nspend   = np.random.uniform(10, 100, 50)\nrevenue = spend * 3 + np.random.randn(50) * 20\nchannels = [\'Organic\',\'Paid\',\'Email\',\'Social\']\nchannel_mix = [40, 30, 20, 10]\n\nfig = make_subplots(rows=2, cols=2,\n                    subplot_titles=[\'Weekly Sales\',\'Sales by Region\',\n                                    \'Spend vs Revenue\',\'Channel Mix\'],\n                    specs=[[{},{}],[{},{\'type\':\'pie\'}]])\n\n# TODO: add go.Scatter for weekly sales (row=1,col=1)\n# TODO: add go.Bar for regions (row=1,col=2)\n# TODO: add go.Scatter mode=\'markers\' for spend vs revenue (row=2,col=1)\n# TODO: add go.Pie for channels (row=2,col=2)\n\nfig.update_layout(title=\'Sales Dashboard\', template=\'plotly_dark\',\n                  height=600, showlegend=False)\nfig.write_html(\'dashboard.html\')\n"
}
},

]  # end SECTIONS


html = make_html(SECTIONS)
nb   = make_nb(SECTIONS)
(BASE / "index.html").write_text(html, encoding="utf-8")
(BASE / "study_guide.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")
print(f"Plotly guide created: {BASE}")
print(f"  index.html:        {(BASE/'index.html').stat().st_size/1024:.1f} KB")
print(f"  study_guide.ipynb: {len(nb['cells'])} cells")
