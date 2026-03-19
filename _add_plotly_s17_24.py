"""Add sections 17-24 to gen_plotly.py."""
import sys
sys.path.insert(0, r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
from _inserter import insert_sections

FILE   = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_plotly.py"
MARKER = "]  # end SECTIONS"

def ec(code):
    return (code.replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace("'", "\\'"))

def make_pl(num, title, desc, examples, rw_title, rw_scenario, rw_code, pt, pd_text, ps):
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

# ── Section 17: Candlestick & Financial Charts ────────────────────────────────
s17 = make_pl(17, "Candlestick & Financial Charts",
    "Plotly's go.Candlestick and go.Ohlc render OHLC price data with interactive zoom, range slectors, and volume overlays — essential for financial dashboards.",
    [
        {"label": "Basic candlestick with volume overlay",
         "code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np, pandas as pd

np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=60, freq='B')
close = 100 + np.cumsum(np.random.randn(60) * 1.5)
open_ = close + np.random.randn(60) * 0.8
high  = np.maximum(open_, close) + np.abs(np.random.randn(60) * 0.5)
low   = np.minimum(open_, close) - np.abs(np.random.randn(60) * 0.5)
volume = np.random.randint(1_000_000, 5_000_000, 60)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.03, row_heights=[0.75, 0.25])

fig.add_trace(go.Candlestick(x=dates, open=open_, high=high,
                              low=low, close=close, name='OHLC',
                              increasing_line_color='#26a69a',
                              decreasing_line_color='#ef5350'), row=1, col=1)

colors = ['#26a69a' if c >= o else '#ef5350' for c, o in zip(close, open_)]
fig.add_trace(go.Bar(x=dates, y=volume, name='Volume',
                     marker_color=colors, opacity=0.7), row=2, col=1)

fig.update_layout(title='OHLC Price + Volume', xaxis_rangeslider_visible=False,
                  template='plotly_dark', height=500)
fig.update_yaxes(title_text='Price ($)', row=1)
fig.update_yaxes(title_text='Volume', row=2)
fig.write_html('candlestick.html')
print('Chart saved')"""},
        {"label": "Moving averages on candlestick",
         "code":
"""import plotly.graph_objects as go
import numpy as np, pandas as pd

np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=120, freq='B')
close = 150 + np.cumsum(np.random.randn(120) * 2)
open_ = close + np.random.randn(120)
high  = np.maximum(open_, close) + np.abs(np.random.randn(120))
low   = np.minimum(open_, close) - np.abs(np.random.randn(120))

s = pd.Series(close, index=dates)
ma20 = s.rolling(20).mean()
ma50 = s.rolling(50).mean()

fig = go.Figure()
fig.add_trace(go.Candlestick(x=dates, open=open_, high=high,
                              low=low, close=close, name='OHLC',
                              increasing_fillcolor='#26a69a',
                              decreasing_fillcolor='#ef5350'))
fig.add_trace(go.Scatter(x=dates, y=ma20, name='MA 20',
                          line=dict(color='orange', width=1.5)))
fig.add_trace(go.Scatter(x=dates, y=ma50, name='MA 50',
                          line=dict(color='cyan', width=1.5)))

fig.update_layout(title='Candlestick with Moving Averages',
                  template='plotly_dark', xaxis_rangeslider_visible=False,
                  hovermode='x unified', height=450)
fig.write_html('candlestick_ma.html')
print('Saved with MA20/MA50')"""},
        {"label": "Range selector buttons and OHLC bar chart",
         "code":
"""import plotly.graph_objects as go
import numpy as np, pandas as pd

np.random.seed(0)
dates = pd.date_range('2022-01-01', periods=250, freq='B')
close = 200 + np.cumsum(np.random.randn(250) * 2.5)
open_ = close + np.random.randn(250) * 1.2
high  = np.maximum(open_, close) + np.abs(np.random.randn(250))
low   = np.minimum(open_, close) - np.abs(np.random.randn(250))

fig = go.Figure(go.Ohlc(x=dates, open=open_, high=high,
                         low=low, close=close, name='OHLC Bars',
                         increasing_line_color='lime',
                         decreasing_line_color='red'))

fig.update_layout(
    title='OHLC with Range Selectors',
    template='plotly_dark',
    xaxis=dict(
        rangeselector=dict(
            buttons=[
                dict(count=1, label='1M', step='month', stepmode='backward'),
                dict(count=3, label='3M', step='month', stepmode='backward'),
                dict(count=6, label='6M', step='month', stepmode='backward'),
                dict(step='all', label='All'),
            ]
        ),
        rangeslider=dict(visible=True),
        type='date',
    ),
    height=450,
)
fig.write_html('ohlc_range.html')
print('OHLC chart with range selector saved')"""}
    ],
    rw_title="Stock Screener Dashboard",
    rw_scenario="A portfolio tracker shows daily OHLC for top 5 holdings, highlighting days where close > open in green and flagging high-volume days.",
    rw_code=
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np, pandas as pd

np.random.seed(7)
tickers = ['AAPL', 'MSFT', 'GOOG']
dates = pd.date_range('2024-01-01', periods=40, freq='B')

fig = make_subplots(rows=len(tickers), cols=1, shared_xaxes=True,
                    subplot_titles=tickers, vertical_spacing=0.06)

for row, ticker in enumerate(tickers, 1):
    c = 150 + row*20 + np.cumsum(np.random.randn(40)*2)
    o = c + np.random.randn(40)
    h = np.maximum(o,c) + np.abs(np.random.randn(40)*0.5)
    l = np.minimum(o,c) - np.abs(np.random.randn(40)*0.5)
    fig.add_trace(go.Candlestick(x=dates, open=o, high=h, low=l, close=c,
                                  name=ticker, showlegend=True), row=row, col=1)

fig.update_xaxes(rangeslider_visible=False)
fig.update_layout(title='Portfolio Overview', template='plotly_dark', height=700)
fig.write_html('portfolio.html')
print(f'Portfolio chart: {len(tickers)} tickers saved')""",
    pt="Bollinger Bands",
    pd_text="Generate 90 days of OHLC data (random walk starting at 100). Compute a 20-day rolling mean and ±2 std Bollinger Bands from the close price. Plot as a candlestick with the upper, middle, and lower bands as overlaid lines. Color the bands blue. Save as 'bollinger.html'.",
    ps=
"""import plotly.graph_objects as go
import numpy as np, pandas as pd

np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=90, freq='B')
close = 100 + np.cumsum(np.random.randn(90) * 1.5)
open_ = close + np.random.randn(90)
high  = np.maximum(open_, close) + np.abs(np.random.randn(90)*0.5)
low   = np.minimum(open_, close) - np.abs(np.random.randn(90)*0.5)

s = pd.Series(close, index=dates)
# TODO: compute ma = s.rolling(20).mean()
# TODO: std = s.rolling(20).std()
# TODO: upper = ma + 2*std, lower = ma - 2*std

fig = go.Figure()
# TODO: add Candlestick trace
# TODO: add Scatter traces for upper, middle (ma), lower bands
fig.update_layout(title='Bollinger Bands', template='plotly_dark',
                  xaxis_rangeslider_visible=False)
fig.write_html('bollinger.html')
"""
)

# ── Section 18: Treemap & Sunburst Charts ─────────────────────────────────────
s18 = make_pl(18, "Treemap & Sunburst Charts",
    "Treemaps and sunbursts visualize hierarchical data where area/angle encodes value. Use them for budget breakdowns, file system sizes, market cap, and org charts.",
    [
        {"label": "Treemap from flat DataFrame",
         "code":
"""import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'category': ['Electronics','Electronics','Electronics',
                 'Clothing','Clothing','Food','Food','Food','Food'],
    'subcategory': ['Phones','Laptops','Tablets',
                    'Shirts','Pants','Dairy','Bakery','Produce','Frozen'],
    'sales': [4500, 3200, 1800, 2100, 1600, 900, 750, 1200, 680],
    'profit': [900, 480, 270, 420, 240, 135, 112, 180, 102],
})

fig = px.treemap(df,
    path=['category', 'subcategory'],
    values='sales',
    color='profit',
    color_continuous_scale='RdYlGn',
    title='Sales Treemap by Category → Subcategory',
    hover_data={'profit': ':,.0f'},
)
fig.update_traces(textinfo='label+value+percent root')
fig.write_html('treemap_sales.html')
print(f'Treemap saved — {len(df)} rows')"""},
        {"label": "Sunburst for org/portfolio drilldown",
         "code":
"""import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'continent': ['Americas','Americas','Americas','Europe','Europe','Asia','Asia','Asia'],
    'country':   ['USA','Brazil','Canada','Germany','France','China','Japan','India'],
    'sector':    ['Tech','Finance','Mining','Auto','Pharma','Tech','Auto','IT'],
    'market_cap':[2800, 400, 350, 680, 520, 1900, 750, 420],
})

fig = px.sunburst(df,
    path=['continent', 'country', 'sector'],
    values='market_cap',
    color='market_cap',
    color_continuous_scale='Blues',
    title='Market Cap: Continent → Country → Sector ($ Bn)',
)
fig.update_traces(
    textinfo='label+percent parent',
    insidetextorientation='radial',
)
fig.update_layout(height=550)
fig.write_html('sunburst_portfolio.html')
print('Sunburst saved')"""},
        {"label": "Treemap with custom text and color",
         "code":
"""import plotly.graph_objects as go

labels  = ['Total','A Div','B Div','C Div','A1','A2','B1','B2','C1','C2','C3']
parents = ['',    'Total','Total','Total','A Div','A Div','B Div','B Div','C Div','C Div','C Div']
values  = [0,     0,      0,      0,      120,    80,     200,    150,    60,     90,     50]

fig = go.Figure(go.Treemap(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues='total',
    marker=dict(
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='Revenue'),
    ),
    texttemplate='<b>%{label}</b><br>$%{value}k',
    hovertemplate='<b>%{label}</b><br>Revenue: $%{value}k<br>Share: %{percentRoot:.1%}<extra></extra>',
))
fig.update_layout(title='Division Revenue Treemap', height=450)
fig.write_html('treemap_custom.html')
print('Custom treemap saved')"""}
    ],
    rw_title="IT Infrastructure Cost Treemap",
    rw_scenario="An IT manager visualizes cloud spending broken down by department > service > resource type to identify cost hotspots at a glance.",
    rw_code=
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(1)
depts = ['Engineering','Marketing','Operations']
services = ['Compute','Storage','Database','Network']
data = []
for d in depts:
    for svc in services:
        cost = np.random.randint(500, 8000)
        growth = np.random.uniform(-0.1, 0.3)
        data.append({'dept': d, 'service': svc, 'cost': cost, 'growth_pct': growth})

df = pd.DataFrame(data)
fig = px.treemap(df,
    path=['dept', 'service'],
    values='cost',
    color='growth_pct',
    color_continuous_scale='RdYlGn_r',
    color_continuous_midpoint=0,
    title='Cloud Cost by Dept → Service (color = MoM growth)',
    custom_data=['growth_pct'],
)
fig.update_traces(
    texttemplate='<b>%{label}</b><br>$%{value:,.0f}',
    hovertemplate='%{label}<br>Cost: $%{value:,.0f}<br>Growth: %{customdata[0]:.1%}<extra></extra>',
)
fig.write_html('it_cost_treemap.html')
print(f'IT cost treemap saved — {df.cost.sum():,} total spend')""",
    pt="File System Sunburst",
    pd_text="Build a sunburst showing a simulated file system: root → 3 folders (docs, src, data) → 2-3 files each with sizes (KB). Use go.Sunburst with branchvalues='total'. Color by size. Show label+percent parent as text. Save as 'filesystem.html'.",
    ps=
"""import plotly.graph_objects as go

labels  = ['root','docs','src','data',
           'report.pdf','slides.pptx',
           'main.py','utils.py','tests.py',
           'train.csv','test.csv']
parents = ['','root','root','root',
           'docs','docs',
           'src','src','src',
           'data','data']
values  = [0, 0, 0, 0,
           2048, 5120,
           45, 30, 22,
           10240, 4096]

# TODO: create go.Sunburst with branchvalues='total'
# TODO: color by values, add textinfo='label+percent parent'
fig = go.Figure()
fig.update_layout(title='File System Sunburst')
fig.write_html('filesystem.html')
"""
)

# ── Section 19: Violin & Strip Charts ────────────────────────────────────────
s19 = make_pl(19, "Violin & Strip Charts",
    "Violin plots combine a KDE curve with a box plot to show distribution shape. Strip/jitter plots show individual data points — great for small-to-medium datasets.",
    [
        {"label": "Violin with box and points overlay",
         "code":
"""import plotly.express as px
import numpy as np, pandas as pd

np.random.seed(42)
groups = ['Control', 'Treatment A', 'Treatment B']
data = pd.concat([
    pd.DataFrame({'group': g,
                  'score': np.random.normal(loc, 12, 80)})
    for g, loc in zip(groups, [50, 62, 71])
])

fig = px.violin(data, x='group', y='score', color='group',
                box=True, points='all',
                title='Score Distribution by Treatment Group',
                labels={'score': 'Test Score', 'group': 'Group'},
                color_discrete_sequence=px.colors.qualitative.Pastel)

fig.update_traces(meanline_visible=True, jitter=0.3, pointpos=-1.8,
                  marker=dict(size=4, opacity=0.5))
fig.update_layout(showlegend=False, height=450)
fig.write_html('violin_groups.html')
print('Violin chart saved')"""},
        {"label": "Side-by-side violin for before/after",
         "code":
"""import plotly.graph_objects as go
import numpy as np

np.random.seed(10)
before = np.random.normal(65, 15, 100)
after  = np.random.normal(72, 12, 100)

fig = go.Figure()
fig.add_trace(go.Violin(y=before, name='Before',
                         side='negative', line_color='#636EFA',
                         fillcolor='rgba(99,110,250,0.3)',
                         box_visible=True, meanline_visible=True))
fig.add_trace(go.Violin(y=after,  name='After',
                         side='positive', line_color='#EF553B',
                         fillcolor='rgba(239,85,59,0.3)',
                         box_visible=True, meanline_visible=True))

fig.update_layout(
    title='Before vs After Intervention (Split Violin)',
    violingap=0, violinmode='overlay',
    yaxis_title='Score',
    template='plotly_white',
    height=420,
)
fig.write_html('violin_split.html')
print(f'Before mean: {before.mean():.1f}  After mean: {after.mean():.1f}')"""},
        {"label": "Strip plot (jitter) with mean markers",
         "code":
"""import plotly.express as px
import numpy as np, pandas as pd

np.random.seed(5)
categories = ['Category A', 'Category B', 'Category C', 'Category D']
df = pd.concat([
    pd.DataFrame({'category': cat, 'value': np.random.exponential(scale, 50)})
    for cat, scale in zip(categories, [10, 20, 15, 25])
])

fig = px.strip(df, x='category', y='value', color='category',
               title='Strip Plot with Individual Data Points',
               stripmode='overlay',
               color_discrete_sequence=px.colors.qualitative.Set2)

# Add mean markers
for cat in categories:
    mean_val = df[df.category == cat]['value'].mean()
    fig.add_scatter(x=[cat], y=[mean_val], mode='markers',
                    marker=dict(symbol='line-ew', size=20, color='black', line_width=2),
                    showlegend=False, hovertemplate=f'Mean: {mean_val:.1f}')

fig.update_traces(jitter=0.4, marker_size=5, marker_opacity=0.6,
                  selector=dict(type='strip'))
fig.update_layout(showlegend=False, height=420)
fig.write_html('strip_plot.html')
print('Strip plot saved')"""}
    ],
    rw_title="A/B Test Distribution Comparison",
    rw_scenario="A data scientist uses split violins to compare conversion rates and session durations between two website variants, showing both distribution shape and individual data points.",
    rw_code=
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

np.random.seed(99)
metrics = {
    'Conversion Rate (%)': (np.random.beta(2, 20, 200)*100,
                            np.random.beta(3, 20, 200)*100),
    'Session Duration (s)': (np.random.exponential(120, 200),
                             np.random.exponential(145, 200)),
}

fig = make_subplots(rows=1, cols=2, subplot_titles=list(metrics.keys()))
colors = ['#636EFA', '#EF553B']

for col, (metric, (ctrl, var)) in enumerate(metrics.items(), 1):
    for data, name, side, color in [
        (ctrl, 'Control',  'negative', colors[0]),
        (var,  'Variant',  'positive', colors[1]),
    ]:
        fig.add_trace(
            go.Violin(y=data, name=name, side=side,
                      line_color=color, box_visible=True,
                      meanline_visible=True, showlegend=(col==1)),
            row=1, col=col
        )

fig.update_layout(title='A/B Test: Control vs Variant',
                  violinmode='overlay', template='plotly_white',
                  height=420)
fig.write_html('ab_test_violin.html')
for m, (c, v) in metrics.items():
    print(f'{m}: ctrl={c.mean():.1f} | var={v.mean():.1f} | lift={((v.mean()-c.mean())/c.mean())*100:.1f}%')""",
    pt="Multi-Group Violin",
    pd_text="Generate exam scores for 4 subjects (Math, Science, English, History) with 60 students each (different means: 72, 68, 75, 65; std=12). Create a violin plot with box=True, points='outliers'. Color by subject. Add a horizontal dashed line at score=70 (passing threshold). Save as 'exam_scores.html'.",
    ps=
"""import plotly.express as px
import plotly.graph_objects as go
import numpy as np, pandas as pd

np.random.seed(42)
subjects = ['Math','Science','English','History']
means    = [72, 68, 75, 65]

data = pd.concat([
    pd.DataFrame({'subject': s, 'score': np.random.normal(m, 12, 60)})
    for s, m in zip(subjects, means)
])
data['score'] = data['score'].clip(0, 100)

# TODO: create px.violin with box=True, points='outliers'
# TODO: add go.Scatter horizontal line at y=70 (passing threshold)
fig = go.Figure()
fig.update_layout(title='Exam Score Distributions', height=430)
fig.write_html('exam_scores.html')
"""
)

# ── Section 20: Parallel Coordinates & Categories ────────────────────────────
s20 = make_pl(20, "Parallel Coordinates & Categories",
    "Parallel coordinates show multi-dimensional continuous data on parallel axes — each line is one observation. Parallel categories (Sankey-style) show flows between categorical variables.",
    [
        {"label": "Parallel coordinates for ML feature analysis",
         "code":
"""import plotly.express as px
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target  # 0, 1, 2

fig = px.parallel_coordinates(
    df,
    color='species',
    dimensions=iris.feature_names,
    color_continuous_scale=px.colors.diverging.Tealrose,
    color_continuous_midpoint=1,
    title='Iris Dataset — Parallel Coordinates',
    labels={n: n.replace(' (cm)', '') for n in iris.feature_names},
)
fig.update_layout(height=430)
fig.write_html('parallel_coords_iris.html')
print('Drag axes to filter! Saved.')"""},
        {"label": "Parallel coordinates with custom dimension ranges",
         "code":
"""import plotly.graph_objects as go
import numpy as np, pandas as pd

np.random.seed(42)
n = 200
df = pd.DataFrame({
    'age':     np.random.randint(22, 65, n),
    'income':  np.random.exponential(50000, n).clip(20000, 200000),
    'savings': np.random.exponential(30000, n).clip(0, 150000),
    'credit':  np.random.randint(300, 850, n),
    'loan':    np.random.choice([0, 1], n, p=[0.7, 0.3]),
})

fig = go.Figure(go.Parcoords(
    line=dict(color=df['loan'], colorscale='RdYlGn_r',
              showscale=True, colorbar=dict(title='Default')),
    dimensions=[
        dict(label='Age', values=df['age'], range=[22, 65]),
        dict(label='Income ($)', values=df['income'], range=[20000, 200000]),
        dict(label='Savings ($)', values=df['savings'], range=[0, 150000]),
        dict(label='Credit Score', values=df['credit'], range=[300, 850]),
    ],
))
fig.update_layout(title='Loan Default — Parallel Coordinates',
                  height=430, template='plotly_dark')
fig.write_html('parallel_loan.html')
print('Loan parallel coords saved')"""},
        {"label": "Parallel categories (categorical Sankey flow)",
         "code":
"""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(3)
n = 500
df = pd.DataFrame({
    'region':    np.random.choice(['North','South','East','West'], n),
    'segment':   np.random.choice(['SMB','Enterprise','Consumer'], n),
    'channel':   np.random.choice(['Online','Retail','Partner'], n),
    'outcome':   np.random.choice(['Won','Lost','Pending'], n, p=[0.4,0.4,0.2]),
})

fig = px.parallel_categories(
    df,
    dimensions=['region','segment','channel','outcome'],
    color=df['outcome'].map({'Won': 0, 'Pending': 0.5, 'Lost': 1}),
    color_continuous_scale='RdYlGn_r',
    title='Sales Pipeline Flow: Region → Segment → Channel → Outcome',
)
fig.update_layout(height=450)
fig.write_html('parallel_categories.html')
print('Parallel categories chart saved')"""}
    ],
    rw_title="Model Feature Explorer",
    rw_scenario="An ML team uses parallel coordinates on their validation set to interactively filter observations — dragging axes to isolate the feature ranges where the model underperforms.",
    rw_code=
"""import plotly.express as px
import numpy as np, pandas as pd
from sklearn.datasets import load_wine

wine = load_wine()
df = pd.DataFrame(wine.data, columns=wine.feature_names)
df['class'] = wine.target
df['error'] = np.random.choice([0, 1], len(df), p=[0.8, 0.2])

# Use only most informative features
top_features = ['alcohol', 'malic_acid', 'flavanoids',
                'color_intensity', 'proline']

fig = px.parallel_coordinates(
    df,
    color='class',
    dimensions=top_features + ['class'],
    color_continuous_scale=px.colors.sequential.Viridis,
    title='Wine Dataset — Feature Space by Class',
    labels={f: f.replace('_', ' ').title() for f in top_features},
)
fig.update_layout(height=430)
fig.write_html('wine_parallel.html')
print(f'Wine parallel coords: {len(df)} samples, {len(top_features)} features')""",
    pt="Car Dataset Explorer",
    pd_text="Using px.data.cars() (or generate synthetic data: mpg, cylinders, horsepower, weight, model_year), create a parallel coordinates chart colored by 'cylinders'. Add a second chart using px.parallel_categories with columns cylinders and origin. Save both as 'cars_parcoord.html' and 'cars_parcat.html'.",
    ps=
"""import plotly.express as px
import pandas as pd
import numpy as np

# Use built-in cars dataset
try:
    df = px.data.cars()
except Exception:
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        'mpg': np.random.normal(23, 7, n).clip(8, 46),
        'cylinders': np.random.choice([4, 6, 8], n, p=[0.5, 0.3, 0.2]),
        'horsepower': np.random.normal(100, 40, n).clip(40, 230),
        'weight': np.random.normal(2800, 700, n).clip(1600, 5000),
        'model_year': np.random.randint(70, 83, n),
        'origin': np.random.choice(['USA','Europe','Japan'], n),
    })

# TODO: parallel_coordinates colored by cylinders
# TODO: parallel_categories with cylinders and origin
"""
)

# ── Section 21: Funnel & Waterfall Charts ────────────────────────────────────
s21 = make_pl(21, "Funnel & Waterfall Charts",
    "Funnel charts show sequential stage drop-off (sales pipelines, conversion funnels). Waterfall charts show cumulative effects of positive and negative values — perfect for P&L statements.",
    [
        {"label": "Sales funnel with conversion rates",
         "code":
"""import plotly.graph_objects as go

stages = ['Website Visits', 'Product Views', 'Add to Cart',
          'Checkout Started', 'Purchase Completed']
counts = [10000, 5200, 2100, 980, 420]

conversion = [f'{counts[i]/counts[i-1]:.0%}' if i > 0 else '100%'
              for i in range(len(counts))]

fig = go.Figure(go.Funnel(
    y=stages,
    x=counts,
    textposition='inside',
    textinfo='value+percent previous',
    opacity=0.85,
    marker=dict(
        color=['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A'],
        line=dict(width=2, color='white'),
    ),
    connector=dict(line=dict(color='#888', width=1)),
))
fig.update_layout(
    title='E-Commerce Conversion Funnel',
    template='plotly_white',
    height=420,
    margin=dict(l=200),
)
fig.write_html('sales_funnel.html')
print(f'Overall conversion: {counts[-1]/counts[0]:.1%}')"""},
        {"label": "Waterfall chart for P&L statement",
         "code":
"""import plotly.graph_objects as go

items   = ['Revenue','COGS','Gross Profit','R&D',
           'S&M','G&A','EBITDA','D&A','EBIT']
values  = [1000, -380, None, -150, -120, -80, None, -45, None]
measure = ['absolute','relative','total','relative',
           'relative','relative','total','relative','total']
text    = [f'${abs(v):,}' if v else '' for v in values]

fig = go.Figure(go.Waterfall(
    orientation='v',
    measure=measure,
    x=items,
    y=values,
    text=text,
    textposition='outside',
    increasing=dict(marker_color='#26a69a'),
    decreasing=dict(marker_color='#ef5350'),
    totals=dict(marker_color='#636EFA'),
    connector=dict(line=dict(color='#999', width=1, dash='dot')),
))
fig.update_layout(
    title='P&L Waterfall — Q4 2024',
    yaxis_title='$ Thousands',
    template='plotly_white',
    height=450,
    showlegend=False,
)
fig.write_html('pnl_waterfall.html')
print('P&L waterfall saved')"""},
        {"label": "Funnel area and horizontal funnel",
         "code":
"""import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

stages = ['Awareness','Interest','Consideration','Intent','Purchase']
values = [50000, 22000, 8500, 3200, 980]

fig = make_subplots(rows=1, cols=2,
                    subplot_titles=['Standard Funnel', 'Funnel Area'],
                    specs=[[{'type':'funnel'}, {'type':'funnelarea'}]])

fig.add_trace(
    go.Funnel(y=stages, x=values, textinfo='value+percent initial',
              marker_color=px.colors.sequential.Blues_r[1:]),
    row=1, col=1)

fig.add_trace(
    go.Funnelarea(labels=stages, values=values,
                  textinfo='label+percent',
                  marker_colors=px.colors.sequential.Greens_r[1:]),
    row=1, col=2)

fig.update_layout(title='Marketing Funnel Comparison', height=420)
fig.write_html('funnel_comparison.html')
print(f'Top-of-funnel to purchase: {values[-1]/values[0]:.1%}')"""}
    ],
    rw_title="SaaS Revenue Waterfall",
    rw_scenario="A CFO presents monthly recurring revenue changes: starting ARR, new business, expansions, contractions, and churn — visualized as a waterfall to show net revenue change.",
    rw_code=
"""import plotly.graph_objects as go
import numpy as np

months = ['Jan','Feb','Mar','Apr','May','Jun']
starting_arr = 500

data_rows = []
for m in months:
    new_biz    = np.random.randint(15, 40)
    expansion  = np.random.randint(5, 20)
    contraction= -np.random.randint(2, 10)
    churn      = -np.random.randint(5, 20)
    data_rows.append((m, new_biz, expansion, contraction, churn))

items   = ['Start']
values  = [starting_arr]
measure = ['absolute']

for month, new, exp, con, churn in data_rows:
    items   += [f'{month} New', f'{month} Exp', f'{month} Con', f'{month} Churn']
    values  += [new, exp, con, churn]
    measure += ['relative','relative','relative','relative']

items.append('End ARR')
values.append(None)
measure.append('total')

fig = go.Figure(go.Waterfall(
    x=items, y=values, measure=measure,
    increasing=dict(marker_color='#26a69a'),
    decreasing=dict(marker_color='#ef5350'),
    totals=dict(marker_color='#636EFA'),
    textposition='outside', texttemplate='%{y:+.0f}',
))
fig.update_layout(title='SaaS ARR Waterfall (H1 2024)', height=450,
                  template='plotly_white', xaxis_tickangle=45)
fig.write_html('saas_waterfall.html')
print('SaaS waterfall saved')""",
    pt="Budget Variance Waterfall",
    pd_text="Create a waterfall chart showing budget vs actuals for 5 departments: start with 'Budget Total' at 1,000,000. Show each department as a relative bar (some over, some under). End with 'Actual Total' as a total bar. Color over-budget red, under-budget green. Save as 'budget_variance.html'.",
    ps=
"""import plotly.graph_objects as go

departments = ['Engineering','Marketing','Sales','Operations','HR']
budget_each = [200000, 150000, 180000, 120000, 100000]  # sums to 750k; rest is overhead
variances   = [+15000, -8000, +22000, -5000, +3000]      # actual - budget per dept

items   = ['Budget Total'] + departments + ['Overhead', 'Actual Total']
# TODO: set up values list (budget_total=750000, then variances, then overhead=250000, total=None)
# TODO: set up measure list
# TODO: create go.Waterfall with increasing green, decreasing red
fig = go.Figure()
fig.update_layout(title='Budget Variance Waterfall', height=430)
fig.write_html('budget_variance.html')
"""
)

# ── Section 22: Indicator & Gauge Charts ─────────────────────────────────────
s22 = make_pl(22, "Indicator & Gauge Charts",
    "go.Indicator renders KPI numbers, delta comparisons, and gauge/speedometer charts. Combine them in subplots to build executive dashboards without any extra libraries.",
    [
        {"label": "KPI indicators with delta",
         "code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=4,
                    specs=[[{'type':'indicator'}]*4])

kpis = [
    ('Revenue',  '1.24M',  1_240_000, 1_100_000),
    ('Users',    '48.3K',  48_300,    45_100),
    ('Churn %',  '2.1%',   2.1,       2.8),
    ('NPS',      '67',     67,        61),
]

for col, (name, num_str, val, ref) in enumerate(kpis, 1):
    better_if_lower = 'churn' in name.lower()
    fig.add_trace(go.Indicator(
        mode='number+delta',
        value=val,
        title=dict(text=name, font=dict(size=14)),
        delta=dict(
            reference=ref,
            increasing=dict(color='red' if better_if_lower else 'green'),
            decreasing=dict(color='green' if better_if_lower else 'red'),
            valueformat='.1%' if '%' in num_str else None,
        ),
        number=dict(
            prefix='$' if 'M' in num_str else '',
            suffix='%' if '%' in num_str else '',
        ),
    ), row=1, col=col)

fig.update_layout(title='Business KPI Dashboard', height=200,
                  template='plotly_dark', margin=dict(t=50, b=20))
fig.write_html('kpi_indicators.html')
print('KPI dashboard saved')"""},
        {"label": "Gauge / speedometer chart",
         "code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=3,
                    specs=[[{'type':'indicator'}]*3])

gauges = [
    ('CPU Usage', 73, '%', 'red', [(0,40,'green'),(40,70,'yellow'),(70,100,'red')]),
    ('Memory',    58, '%', 'orange', [(0,60,'green'),(60,80,'orange'),(80,100,'red')]),
    ('SLA Score', 96.5, '%', 'green', [(0,90,'red'),(90,95,'yellow'),(95,100,'green')]),
]

for col, (name, val, suffix, color, steps) in enumerate(gauges, 1):
    fig.add_trace(go.Indicator(
        mode='gauge+number+delta',
        value=val,
        title=dict(text=name, font=dict(size=14)),
        delta=dict(reference=80 if 'SLA' not in name else 95),
        number=dict(suffix=suffix),
        gauge=dict(
            axis=dict(range=[0, 100]),
            bar=dict(color=color, thickness=0.25),
            steps=[dict(range=[lo, hi], color=c) for lo, hi, c in steps],
            threshold=dict(line=dict(color='white', width=3),
                           thickness=0.75, value=val),
        ),
    ), row=1, col=col)

fig.update_layout(title='Infrastructure Gauges', height=280,
                  template='plotly_dark', margin=dict(t=60, b=10))
fig.write_html('gauges.html')
print('Gauge dashboard saved')"""},
        {"label": "Bullet chart style indicator",
         "code":
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots

metrics = [
    ('Q1 Revenue',   1.15, 1.25, 'M$'),
    ('Q1 Leads',     430,  500,  ''),
    ('Avg Deal ($)', 22500, 20000, '$'),
    ('Win Rate',     42,   40,   '%'),
]

fig = make_subplots(rows=len(metrics), cols=1,
                    specs=[[{'type':'indicator'}]] * len(metrics),
                    vertical_spacing=0.0)

for row, (name, actual, target, unit) in enumerate(metrics, 1):
    color = 'green' if actual >= target else 'red'
    fig.add_trace(go.Indicator(
        mode='number+gauge+delta',
        value=actual,
        title=dict(text=name, font=dict(size=12)),
        delta=dict(reference=target,
                   relative=True,
                   increasing=dict(color='green'),
                   decreasing=dict(color='red')),
        number=dict(prefix=unit if unit=='$' else '',
                    suffix=unit if unit!='$' else ''),
        gauge=dict(
            shape='bullet',
            axis=dict(range=[0, target*1.5]),
            threshold=dict(value=target,
                           line=dict(color='black', width=2),
                           thickness=0.75),
            bar=dict(color=color),
        ),
    ), row=row, col=1)

fig.update_layout(title='Q1 Performance vs Target',
                  height=360, template='plotly_white',
                  margin=dict(l=160, t=60, b=20))
fig.write_html('bullet_chart.html')
print('Bullet chart saved')"""}
    ],
    rw_title="Executive SaaS Dashboard",
    rw_scenario="A SaaS company's weekly executive report shows ARR, MRR growth, churn rate, and NPS as KPI indicators with week-over-week deltas and color coding.",
    rw_code=
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Simulate current vs previous week metrics
np.random.seed(42)
metrics = {
    'ARR ($M)':    (4.82,  4.71,  False),
    'MRR Growth%': (3.2,   2.8,   False),
    'Churn %':     (1.8,   2.1,   True),   # lower is better
    'NPS':         (71,    68,    False),
    'CAC ($)':     (1250,  1380,  True),    # lower is better
    'LTV/CAC':     (4.8,   4.2,   False),
}

n = len(metrics)
fig = make_subplots(rows=2, cols=3,
                    specs=[[{'type':'indicator'}]*3]*2)

for idx, (name, (curr, prev, lower_better)) in enumerate(metrics.items()):
    row, col = divmod(idx, 3)
    fig.add_trace(go.Indicator(
        mode='number+delta',
        value=curr,
        title=dict(text=name, font=dict(size=13)),
        delta=dict(
            reference=prev,
            relative=True,
            increasing=dict(color='red' if lower_better else 'green'),
            decreasing=dict(color='green' if lower_better else 'red'),
        ),
    ), row=row+1, col=col+1)

fig.update_layout(title='SaaS Weekly KPI Report',
                  height=320, template='plotly_dark',
                  margin=dict(t=60, b=20))
fig.write_html('saas_kpi.html')
print('SaaS KPI report saved')""",
    pt="OKR Progress Gauges",
    pd_text="Create 4 gauge indicators in a 2x2 subplot grid, one per OKR: (1) Revenue Target: 85% achieved (target 100), (2) Customer Satisfaction: 4.2/5, (3) Bug Backlog: 23 (target <30, lower is better), (4) Feature Delivery: 7/10 shipped. Use colored gauge steps (red/yellow/green). Save as 'okr_gauges.html'.",
    ps=
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2,
                    specs=[[{'type':'indicator'}]*2]*2)

okrs = [
    ('Revenue Target',      85,   100,  '%',  [(0,60,'red'),(60,80,'yellow'),(80,100,'green')]),
    ('Cust. Satisfaction',  4.2,  5,    '/5', [(0,3,'red'),(3,4,'yellow'),(4,5,'green')]),
    ('Bug Backlog',         23,   30,   '',   [(0,15,'green'),(15,25,'yellow'),(25,30,'red')]),
    ('Feature Delivery',    7,    10,   '/10',[(0,5,'red'),(5,7,'yellow'),(7,10,'green')]),
]

for idx, (name, val, max_val, suffix, steps) in enumerate(okrs):
    row, col = divmod(idx, 2)
    # TODO: add go.Indicator with mode='gauge+number', gauge steps, threshold at target
    pass

fig.update_layout(title='OKR Progress Gauges', height=480, template='plotly_dark')
fig.write_html('okr_gauges.html')
"""
)

# ── Section 23: Animated Bar Chart Race ──────────────────────────────────────
s23 = make_pl(23, "Animated Bar Chart Race & Timelines",
    "Plotly animations use frames and sliders to animate data over time. Bar chart races, animated scatter plots, and timeline maps reveal how data evolves.",
    [
        {"label": "Bar chart race with animation frames",
         "code":
"""import plotly.graph_objects as go
import numpy as np, pandas as pd

np.random.seed(42)
companies = ['Alpha','Beta','Gamma','Delta','Epsilon','Zeta']
years = list(range(2015, 2025))

# Generate cumulative revenue data
revenues = {c: np.cumsum(np.random.exponential(10, len(years))) * (1 + 0.1 * i)
            for i, c in enumerate(companies)}
df = pd.DataFrame(revenues, index=years)

frames = []
for year in years:
    row = df.loc[year].sort_values(ascending=True)
    frames.append(go.Frame(
        data=[go.Bar(x=row.values, y=row.index,
                     orientation='h',
                     marker_color=px_colors := [
                         '#636EFA','#EF553B','#00CC96','#AB63FA',
                         '#FFA15A','#19D3F3'][:len(row)],
                     text=[f'${v:.0f}B' for v in row.values],
                     textposition='outside')],
        name=str(year),
        layout=go.Layout(title_text=f'Company Revenue Race — {year}')
    ))

first = df.loc[years[0]].sort_values(ascending=True)
fig = go.Figure(
    data=[go.Bar(x=first.values, y=first.index, orientation='h',
                 marker_color=['#636EFA','#EF553B','#00CC96',
                               '#AB63FA','#FFA15A','#19D3F3'][:len(first)],
                 text=[f'${v:.0f}B' for v in first.values],
                 textposition='outside')],
    frames=frames,
    layout=go.Layout(
        title=f'Company Revenue Race — {years[0]}',
        xaxis=dict(range=[0, df.values.max()*1.15], title='Revenue ($B)'),
        updatemenus=[dict(type='buttons', showactive=False,
                          buttons=[dict(label='Play',
                                       method='animate',
                                       args=[None, dict(frame=dict(duration=600, redraw=True),
                                                        fromcurrent=True)])])],
        sliders=[dict(steps=[dict(method='animate', args=[[str(y)]], label=str(y))
                             for y in years],
                      currentvalue=dict(prefix='Year: '))],
        height=450, template='plotly_dark',
    )
)
fig.write_html('bar_race.html')
print('Bar chart race saved')"""},
        {"label": "Animated scatter over time",
         "code":
"""import plotly.express as px

df = px.data.gapminder()

fig = px.scatter(
    df, x='gdpPercap', y='lifeExp',
    animation_frame='year',
    animation_group='country',
    size='pop', color='continent',
    hover_name='country',
    log_x=True,
    size_max=55,
    range_x=[100, 100_000],
    range_y=[25, 90],
    title='Gapminder: GDP vs Life Expectancy (1952-2007)',
    labels={'gdpPercap': 'GDP per Capita', 'lifeExp': 'Life Expectancy'},
    template='plotly_white',
)
fig.update_layout(height=500)
fig.write_html('gapminder_animation.html')
print(f'Animated scatter: {df.year.nunique()} frames, {df.country.nunique()} countries')"""},
        {"label": "Animated choropleth map",
         "code":
"""import plotly.express as px

df = px.data.gapminder()

fig = px.choropleth(
    df,
    locations='iso_alpha',
    color='lifeExp',
    hover_name='country',
    animation_frame='year',
    color_continuous_scale='RdYlGn',
    range_color=[25, 90],
    title='World Life Expectancy Over Time (1952-2007)',
    labels={'lifeExp': 'Life Expectancy'},
    projection='natural earth',
)
fig.update_layout(
    coloraxis_colorbar=dict(title='Life Exp.', x=1.0),
    height=480,
    geo=dict(showframe=False, showcoastlines=False),
)
fig.write_html('choropleth_animated.html')
print('Animated choropleth saved')"""}
    ],
    rw_title="Market Share Race",
    rw_scenario="A market analyst builds a bar chart race showing quarterly market share shifts between 5 smartphone brands over 3 years, helping executives spot disruption trends.",
    rw_code=
"""import plotly.graph_objects as go
import numpy as np, pandas as pd

np.random.seed(7)
brands  = ['AlphaPhone','BetaMobile','GammaDevice','DeltaTech','EpsilonX']
quarters= [f'Q{q} {y}' for y in range(2021,2025) for q in range(1,5)]

# Market share that sums to 100% each quarter
raw = np.random.dirichlet(np.ones(len(brands)), len(quarters)) * 100
df  = pd.DataFrame(raw, columns=brands, index=quarters)

frames = []
for q in quarters:
    row = df.loc[q].sort_values(ascending=True)
    frames.append(go.Frame(
        data=[go.Bar(x=row.values, y=row.index, orientation='h',
                     text=[f'{v:.1f}%' for v in row.values],
                     textposition='outside',
                     marker_color=['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A'][:len(row)])],
        name=q,
        layout=go.Layout(title_text=f'Smartphone Market Share — {q}')
    ))

first = df.iloc[0].sort_values(ascending=True)
fig = go.Figure(
    data=[go.Bar(x=first.values, y=first.index, orientation='h',
                 text=[f'{v:.1f}%' for v in first.values], textposition='outside',
                 marker_color=['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A'])],
    frames=frames,
    layout=go.Layout(
        title=f'Smartphone Market Share — {quarters[0]}',
        xaxis=dict(range=[0, 45], title='Market Share (%)'),
        updatemenus=[dict(type='buttons', showactive=False,
                          buttons=[dict(label='▶ Play', method='animate',
                                        args=[None, dict(frame=dict(duration=700))])])],
        sliders=[dict(steps=[dict(method='animate', args=[[q]], label=q) for q in quarters],
                      currentvalue=dict(prefix='Quarter: '))],
        template='plotly_dark', height=450,
    )
)
fig.write_html('market_share_race.html')
print(f'Race saved: {len(quarters)} quarters')""",
    pt="Population Pyramid Animation",
    pd_text="Generate synthetic population data for age groups (0-9, 10-19, ..., 70+) across 5 decades (1980-2020). Build an animated horizontal bar chart race where each frame is a decade. Use negative values for female population to create a butterfly/pyramid effect. Save as 'population_pyramid.html'.",
    ps=
"""import plotly.graph_objects as go
import numpy as np

age_groups = ['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70+']
decades = [1980, 1990, 2000, 2010, 2020]

np.random.seed(42)
frames = []
for decade in decades:
    # Generate male/female populations (in millions)
    base = np.random.exponential(5, len(age_groups)) + 2
    male   =  base + np.random.randn(len(age_groups))
    female = -(base + np.random.randn(len(age_groups)))
    frames.append(go.Frame(
        data=[
            go.Bar(y=age_groups, x=male,   orientation='h', name='Male'),
            # TODO: add female Bar trace with negative values
        ],
        name=str(decade),
        layout=go.Layout(title_text=f'Population Pyramid — {decade}')
    ))

# TODO: create fig with first frame data, frames, updatemenus, sliders
fig = go.Figure()
fig.update_layout(title='Population Pyramid', barmode='overlay',
                  xaxis_title='Population (M)', height=450)
fig.write_html('population_pyramid.html')
"""
)

# ── Section 24: Custom Templates & Styling ───────────────────────────────────
s24 = make_pl(24, "Custom Templates & Styling",
    "Plotly templates define default colors, fonts, backgrounds, and axis styles. Create reusable brand templates with pio.templates and apply them globally or per-chart.",
    [
        {"label": "Creating and applying a custom template",
         "code":
"""import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

# Define a brand template
brand_template = go.layout.Template(
    layout=go.Layout(
        font=dict(family='Arial', size=13, color='#2c2c2c'),
        paper_bgcolor='#f8f9fa',
        plot_bgcolor='#ffffff',
        colorway=['#005A9E','#E63946','#06D6A0','#FFB703','#8338EC'],
        title=dict(font=dict(size=18, color='#005A9E', family='Arial Bold')),
        xaxis=dict(gridcolor='#e9ecef', linecolor='#dee2e6', zeroline=False),
        yaxis=dict(gridcolor='#e9ecef', linecolor='#dee2e6', zeroline=False),
        legend=dict(bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='#dee2e6', borderwidth=1),
        hoverlabel=dict(bgcolor='white', font_size=12,
                        bordercolor='#dee2e6'),
    )
)

# Register the template
pio.templates['brand'] = brand_template
pio.templates.default = 'brand'   # set as global default

import numpy as np, pandas as pd
np.random.seed(42)
df = pd.DataFrame({
    'month': pd.date_range('2024-01', periods=12, freq='MS'),
    'product_a': np.cumsum(np.random.randn(12)*5) + 100,
    'product_b': np.cumsum(np.random.randn(12)*4) + 80,
})

fig = px.line(df, x='month', y=['product_a','product_b'],
              title='Monthly Sales — Brand Template',
              labels={'value':'Revenue ($K)', 'variable':'Product'})
fig.write_html('brand_template.html')
print('Brand template chart saved')

# Reset to default
pio.templates.default = 'plotly'"""},
        {"label": "Dark theme with custom accent colors",
         "code":
"""import plotly.graph_objects as go
import plotly.io as pio
import numpy as np, pandas as pd

dark_template = go.layout.Template(
    layout=dict(
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font=dict(color='#c9d1d9', family='JetBrains Mono, monospace'),
        colorway=['#79c0ff','#ff7b72','#56d364','#d2a8ff','#ffa657','#39c5cf'],
        xaxis=dict(gridcolor='#30363d', linecolor='#30363d',
                   tickcolor='#8b949e', title_font_color='#8b949e'),
        yaxis=dict(gridcolor='#30363d', linecolor='#30363d',
                   tickcolor='#8b949e', title_font_color='#8b949e'),
        title=dict(font=dict(color='#79c0ff', size=17)),
        legend=dict(bgcolor='#161b22', bordercolor='#30363d', borderwidth=1),
        hoverlabel=dict(bgcolor='#161b22', bordercolor='#30363d',
                        font=dict(color='#c9d1d9')),
    )
)
pio.templates['github_dark'] = dark_template

np.random.seed(42)
categories = ['Q1','Q2','Q3','Q4']
products   = ['Widget','Gadget','Gizmo']
fig = go.Figure()
for p in products:
    fig.add_trace(go.Bar(name=p, x=categories,
                          y=np.random.randint(50, 200, 4),
                          text=np.random.randint(50, 200, 4),
                          texttemplate='%{text}',
                          textposition='outside'))
fig.update_layout(title='Quarterly Sales — GitHub Dark Theme',
                  template='github_dark', barmode='group', height=430)
fig.write_html('dark_theme.html')
print('Dark theme chart saved')"""},
        {"label": "Per-trace styling and annotations",
         "code":
"""import plotly.graph_objects as go
import numpy as np, pandas as pd

np.random.seed(42)
x = pd.date_range('2024-01', periods=52, freq='W')
actual   = 100 + np.cumsum(np.random.randn(52) * 3)
forecast = actual[-1] + np.cumsum(np.random.randn(12) * 2.5)
upper_ci = forecast + 1.96 * np.arange(1, 13) * 0.8
lower_ci = forecast - 1.96 * np.arange(1, 13) * 0.8
future_x = pd.date_range(x[-1], periods=13, freq='W')[1:]

fig = go.Figure()

# Actual data
fig.add_trace(go.Scatter(x=x, y=actual, name='Actual',
                          line=dict(color='#636EFA', width=2.5)))

# Forecast with confidence interval fill
fig.add_trace(go.Scatter(x=future_x, y=upper_ci, name='Upper CI 95%',
                          line=dict(color='rgba(255,127,14,0)', width=0),
                          showlegend=False))
fig.add_trace(go.Scatter(x=future_x, y=lower_ci, name='Lower CI 95%',
                          line=dict(color='rgba(255,127,14,0)', width=0),
                          fill='tonexty', fillcolor='rgba(255,127,14,0.2)',
                          showlegend=False))
fig.add_trace(go.Scatter(x=future_x, y=forecast, name='Forecast',
                          line=dict(color='#FF7F0E', width=2, dash='dash')))

# Annotation for forecast start
fig.add_vline(x=x[-1], line_dash='dot', line_color='gray', opacity=0.7)
fig.add_annotation(x=x[-1], y=actual[-1], text='Forecast begins',
                    showarrow=True, arrowhead=2, bgcolor='rgba(0,0,0,0.6)',
                    font=dict(color='white'))

fig.update_layout(title='Revenue Actual + 12-Week Forecast with CI',
                  xaxis_title='Date', yaxis_title='Revenue ($K)',
                  template='plotly_dark', height=430, hovermode='x unified')
fig.write_html('forecast_styled.html')
print('Styled forecast chart saved')"""}
    ],
    rw_title="Branded Marketing Report",
    rw_scenario="A marketing team builds a reusable company-branded Plotly template with corporate fonts and colors, then applies it to all quarterly charts for consistent reporting.",
    rw_code=
"""import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import numpy as np, pandas as pd

# Corporate brand template
pio.templates['corporate'] = go.layout.Template(
    layout=dict(
        font=dict(family='Helvetica Neue, sans-serif', size=13),
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FAFAFA',
        colorway=['#1A237E','#283593','#3949AB','#5C6BC0','#7986CB'],
        title=dict(font=dict(size=16, color='#1A237E', family='Helvetica Neue Bold')),
        xaxis=dict(gridcolor='#EEEEEE', linecolor='#BDBDBD'),
        yaxis=dict(gridcolor='#EEEEEE', linecolor='#BDBDBD'),
        legend=dict(bgcolor='rgba(255,255,255,0.9)'),
    )
)

np.random.seed(5)
months = pd.date_range('2024-01', periods=12, freq='MS')
channels = ['Organic','Paid','Email','Social']
data = {c: np.random.randint(200, 800, 12) for c in channels}
df = pd.DataFrame(data, index=months).reset_index().rename(columns={'index':'month'})
df_melt = df.melt('month', var_name='channel', value_name='leads')

fig = px.area(df_melt, x='month', y='leads', color='channel',
              title='Marketing Leads by Channel — Corporate Theme',
              template='corporate')
fig.update_traces(opacity=0.8)
fig.write_html('corporate_report.html')
print(f'Corporate report saved — {df_melt.leads.sum():,} total leads')""",
    pt="Dashboard Layout",
    pd_text="Create a 2x2 subplot dashboard using make_subplots: (top-left) line chart of weekly sales, (top-right) bar chart of sales by region, (bottom-left) scatter of spend vs revenue, (bottom-right) pie chart of channel mix. Apply a consistent dark template. Add a main title. Save as 'dashboard.html'.",
    ps=
"""import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np, pandas as pd

np.random.seed(42)
weeks   = pd.date_range('2024-01', periods=20, freq='W')
sales   = 100 + np.cumsum(np.random.randn(20)*5)
regions = ['North','South','East','West']
reg_sales = np.random.randint(200, 600, 4)
spend   = np.random.uniform(10, 100, 50)
revenue = spend * 3 + np.random.randn(50) * 20
channels = ['Organic','Paid','Email','Social']
channel_mix = [40, 30, 20, 10]

fig = make_subplots(rows=2, cols=2,
                    subplot_titles=['Weekly Sales','Sales by Region',
                                    'Spend vs Revenue','Channel Mix'],
                    specs=[[{},{}],[{},{'type':'pie'}]])

# TODO: add go.Scatter for weekly sales (row=1,col=1)
# TODO: add go.Bar for regions (row=1,col=2)
# TODO: add go.Scatter mode='markers' for spend vs revenue (row=2,col=1)
# TODO: add go.Pie for channels (row=2,col=2)

fig.update_layout(title='Sales Dashboard', template='plotly_dark',
                  height=600, showlegend=False)
fig.write_html('dashboard.html')
"""
)

# ── Assemble and insert ───────────────────────────────────────────────────────
all_sections = s17 + s18 + s19 + s20 + s21 + s22 + s23 + s24

result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: sections 17-24 added to gen_plotly.py")
else:
    print("FAILED: check marker and file")
