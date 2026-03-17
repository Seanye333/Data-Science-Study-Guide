"""
Add 3 sections to each remaining generator file.
Uses escape_code() to properly escape multiline code strings.
"""
import sys, os
sys.path.insert(0, r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
from _inserter import insert_sections

BASE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path"

def ec(code):
    """Escape code string for insertion as a Python string literal."""
    return code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace("'", "\\'")

def make_section(num, title, examples, rw_scenario, rw_code, practice_title, practice_desc, practice_starter):
    """Build section text for examples-list format generators."""
    lines = [f'    {{\n        "title": "{num}. {title}",\n        "examples": [']
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples)-1 else ''
        lines.append(f'            {{\n                "label": "{ex["label"]}",\n                "code": "{ec(ex["code"])}"\n            }}{comma}')
    lines.append(f'        ],\n        "rw_scenario": "{ec(rw_scenario)}",')
    lines.append(f'        "rw_code": "{ec(rw_code)}",')
    lines.append(f'        "practice": {{\n            "title": "{practice_title}",\n            "desc": "{ec(practice_desc)}",\n            "starter": "{ec(practice_starter)}"\n        }}\n    }},')
    return '\n'.join(lines) + '\n'

def make_section_code4(num, title, desc, code1_title, code1, code2_title, code2, code3_title, code3, code4_title, code4, rw_scenario, rw_code, practice_title, practice_desc, practice_starter):
    """Build section text for code1/code2/code3/code4 format generators."""
    return f'''    {{
        "title": "{num}. {title}",
        "desc": "{ec(desc)}",
        "code1_title": "{code1_title}",
        "code1": "{ec(code1)}",
        "code2_title": "{code2_title}",
        "code2": "{ec(code2)}",
        "code3_title": "{code3_title}",
        "code3": "{ec(code3)}",
        "code4_title": "{code4_title}",
        "code4": "{ec(code4)}",
        "rw_scenario": "{ec(rw_scenario)}",
        "rw_code": "{ec(rw_code)}",
        "practice": {{
            "title": "{practice_title}",
            "desc": "{ec(practice_desc)}",
            "starter": "{ec(practice_starter)}"
        }}
    }},
'''

# ═══════════════════════════════════════════════════════════════════════════════
# SEABORN
# ═══════════════════════════════════════════════════════════════════════════════
sn14 = make_section(14, "FacetGrid & PairGrid",
    [
        {"label": "FacetGrid histogram per group",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
df = pd.DataFrame({'value': np.random.randn(300), 'group': np.repeat(['A','B','C'], 100)})
g = sns.FacetGrid(df, col='group', height=3.5, aspect=0.9)
g.map(sns.histplot, 'value', kde=True, bins=20)
g.set_titles(col_template='{col_name}')
g.figure.suptitle('FacetGrid by Group', y=1.02)
g.savefig('facetgrid_hist.png', dpi=100, bbox_inches='tight')
print('Saved facetgrid_hist.png')
plt.close('all')"""},
        {"label": "FacetGrid row x col (2D grid)",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

tips = sns.load_dataset('tips')
g = sns.FacetGrid(tips, row='sex', col='time', height=3, aspect=1.2, margin_titles=True)
g.map(sns.scatterplot, 'total_bill', 'tip', alpha=0.6)
g.add_legend()
g.savefig('facetgrid_2d.png', dpi=100, bbox_inches='tight')
print('Saved facetgrid_2d.png')
plt.close('all')"""},
        {"label": "PairGrid with mixed plot types",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

iris = sns.load_dataset('iris')
g = sns.PairGrid(iris, hue='species', vars=['sepal_length','petal_length','petal_width'])
g.map_upper(sns.scatterplot, alpha=0.6)
g.map_lower(sns.kdeplot, fill=True, alpha=0.4)
g.map_diag(sns.histplot, kde=True)
g.add_legend()
g.savefig('pairgrid_mixed.png', dpi=80, bbox_inches='tight')
print('Saved pairgrid_mixed.png')
plt.close('all')"""},
        {"label": "FacetGrid with custom mapping function",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def scatter_means(x, y, **kw):
    plt.scatter(x, y, alpha=0.5, **{k:v for k,v in kw.items() if k!='label'})
    plt.axhline(y.mean(), color='red', ls='--', lw=1.5)
    plt.axvline(x.mean(), color='blue', ls='--', lw=1.5)

np.random.seed(42)
df = pd.DataFrame({'x':np.random.randn(150),'y':np.random.randn(150),
                   'group':np.repeat(['G1','G2','G3'],50)})
g = sns.FacetGrid(df, col='group', height=3)
g.map(scatter_means, 'x', 'y')
g.figure.suptitle('Scatter with Group Means', y=1.02)
g.savefig('facetgrid_custom.png', dpi=100, bbox_inches='tight')
print('Saved facetgrid_custom.png')
plt.close('all')"""},
    ],
    rw_scenario="You have sales data across 3 regions and 4 products. You need a grid of scatter plots comparing revenue vs units sold for each region-product combination.",
    rw_code="""import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(42)
regions = ['North','South','East']
products = ['Electronics','Apparel','Food','Sports']
rows = []
for r in regions:
    for p in products:
        n = 25
        rows.append(pd.DataFrame({'region':r,'product':p,
                                   'revenue':np.random.exponential(500,n)+100,
                                   'units':np.random.randint(10,200,n)}))
df = pd.concat(rows, ignore_index=True)
g = sns.FacetGrid(df, row='region', col='product', height=2.2, aspect=1.1, margin_titles=True)
g.map(sns.scatterplot, 'units', 'revenue', alpha=0.5, s=20)
g.map(sns.regplot, 'units', 'revenue', scatter=False, color='red', ci=None)
g.set_titles(row_template='{row_name}', col_template='{col_name}')
g.figure.suptitle('Revenue vs Units by Region x Product', y=1.01, fontsize=12)
g.savefig('sales_facetgrid.png', dpi=100, bbox_inches='tight')
print('Saved sales_facetgrid.png')
plt.close('all')""",
    practice_title="Titanic FacetGrid",
    practice_desc="Load titanic. Create a FacetGrid with pclass as columns (3 panels). Show age histplot, colored by survived. Add legend and suptitle. Save to titanic_facet.png.",
    practice_starter="""import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

titanic = sns.load_dataset('titanic').dropna(subset=['age'])
# TODO: FacetGrid col='pclass', hue='survived', map histplot 'age'
# TODO: add_legend(), suptitle, save 'titanic_facet.png'"""
)

sn15 = make_section(15, "Statistical Visualization Deep Dive",
    [
        {"label": "Violin + swarmplot overlay",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    'score': np.concatenate([np.random.normal(70,10,80), np.random.normal(75,8,80), np.random.normal(65,12,80)]),
    'class': ['A']*80 + ['B']*80 + ['C']*80
})
fig, ax = plt.subplots(figsize=(7, 5))
sns.violinplot(data=df, x='class', y='score', inner=None, palette='muted', alpha=0.7, ax=ax)
sns.swarmplot(data=df, x='class', y='score', color='black', size=2.5, alpha=0.6, ax=ax)
ax.set_title('Score Distribution by Class (Violin + Swarm)')
fig.savefig('violin_swarm.png', dpi=100, bbox_inches='tight')
print('Saved violin_swarm.png')
plt.close()"""},
        {"label": "ECDF comparison across groups",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
df = pd.DataFrame({
    'response_ms': np.concatenate([np.random.exponential(200,300),
                                   np.random.exponential(150,300),
                                   np.random.exponential(300,300)]),
    'server': ['A']*300 + ['B']*300 + ['C']*300
})
fig, ax = plt.subplots(figsize=(8, 5))
sns.ecdfplot(data=df, x='response_ms', hue='server', ax=ax)
ax.axvline(200, color='gray', ls=':', label='200ms target')
ax.set_title('ECDF: Response Time by Server')
ax.set_xlabel('Response Time (ms)')
ax.legend()
fig.savefig('ecdf_comparison.png', dpi=100, bbox_inches='tight')
print('Saved ecdf_comparison.png')
plt.close()"""},
        {"label": "Residual plot for regression diagnostics",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.linspace(0, 10, 100)
y = 2*x + np.random.normal(0, 2, 100)
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.regplot(x=x, y=y, ax=axes[0])
axes[0].set_title('Regression with CI')
sns.residplot(x=x, y=y, ax=axes[1])
axes[1].axhline(0, color='red', ls='--')
axes[1].set_title('Residuals vs Fitted')
fig.tight_layout()
fig.savefig('residual_diagnostic.png', dpi=100, bbox_inches='tight')
print('Saved residual_diagnostic.png')
plt.close()"""},
        {"label": "Box plot with significance bracket",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
df = pd.DataFrame({
    'value': np.concatenate([np.random.normal(5,1,50), np.random.normal(7,1.5,50), np.random.normal(6.2,1.2,50)]),
    'group': ['Control']*50 + ['Drug A']*50 + ['Drug B']*50
})
fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(data=df, x='group', y='value', palette='Set2', ax=ax)
y_max = df['value'].max() + 0.5
ax.plot([0, 1], [y_max, y_max], 'k-', lw=1.5)
ax.text(0.5, y_max+0.1, '***', ha='center', fontsize=14)
ax.set_title('Drug Effect with Significance Bracket')
fig.savefig('boxplot_sig.png', dpi=100, bbox_inches='tight')
print('Saved boxplot_sig.png')
plt.close()"""},
    ],
    rw_scenario="You're presenting A/B test results for 3 landing page variants and need violin plots, ECDF comparison, and regression residuals for a comprehensive statistical report.",
    rw_code="""import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
variants = {'Control':(3.2,1.1),'Variant A':(3.8,1.3),'Variant B':(3.5,0.9)}
dfs = [pd.DataFrame({'conversion':np.random.normal(mu,sig,200).clip(0,10),'variant':name})
       for name,(mu,sig) in variants.items()]
df = pd.concat(dfs, ignore_index=True)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
sns.violinplot(data=df, x='variant', y='conversion', inner='quartile', palette='muted', ax=axes[0])
axes[0].set_title('Violin Plot')
sns.ecdfplot(data=df, x='conversion', hue='variant', ax=axes[1])
axes[1].axvline(3.5, color='gray', ls='--', alpha=0.7)
axes[1].set_title('ECDF Comparison')
sns.boxplot(data=df, x='variant', y='conversion', palette='Set2', ax=axes[2])
axes[2].set_title('Box Plot')
fig.suptitle('A/B Test Analysis', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig('ab_test.png', dpi=100, bbox_inches='tight')
print('Saved ab_test.png')
plt.close()""",
    practice_title="Multi-Stat Figure",
    practice_desc="Create 3-panel figure: (1) stripplot of scores by group with means, (2) ECDF for 3 groups, (3) residual plot from regressing score on study_hours. Use whitegrid style.",
    practice_starter="""import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
df = pd.DataFrame({'score':np.random.normal(70,15,150), 'group':np.repeat(['A','B','C'],50), 'study_hours':np.random.uniform(1,8,150)})
# TODO: 3-panel: stripplot, ecdfplot, residplot
# TODO: whitegrid style, save 'multi_stat.png'"""
)

sn16 = make_section(16, "Custom Seaborn Themes & Styling",
    [
        {"label": "Context comparison (paper/talk/poster)",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
df = pd.DataFrame({'x':np.random.randn(100),'y':np.random.randn(100)})
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
for ax, ctx in zip(axes.flat, ['paper','notebook','talk','poster']):
    with sns.plotting_context(ctx):
        sns.scatterplot(data=df, x='x', y='y', ax=ax, alpha=0.6)
        ax.set_title(f'Context: {ctx}')
fig.suptitle('Seaborn Contexts', fontsize=14)
fig.tight_layout()
fig.savefig('contexts.png', dpi=100, bbox_inches='tight')
print('Saved contexts.png')
plt.close()"""},
        {"label": "Custom set_theme with dark background",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sns.set_theme(style='darkgrid', palette='bright', font_scale=1.1,
              rc={'axes.facecolor':'#1e1e2e','figure.facecolor':'#1e1e2e',
                  'text.color':'white','axes.labelcolor':'white',
                  'xtick.color':'white','ytick.color':'white'})
np.random.seed(42)
df = pd.DataFrame({'x':np.random.randn(200),'y':np.random.randn(200),'g':np.random.choice(['A','B','C'],200)})
fig, ax = plt.subplots(figsize=(7,5))
sns.scatterplot(data=df, x='x', y='y', hue='g', alpha=0.7, ax=ax)
ax.set_title('Dark Mode Plot')
fig.savefig('dark_theme.png', dpi=100, bbox_inches='tight')
print('Saved dark_theme.png')
sns.set_theme()
plt.close()"""},
        {"label": "Custom color palettes",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
tips = sns.load_dataset('tips')
pals = [('Blues',4), ('husl',4), ('Set1',4), (['#FF6B6B','#4ECDC4','#45B7D1','#96CEB4'],4)]
titles = ['Blues (seq)','HUSL (qual)','Set1 (qual)','Custom hex']
for ax, (pal, _), title in zip(axes.flat, pals, titles):
    with sns.axes_style('whitegrid'):
        sns.boxplot(data=tips, x='day', y='total_bill', palette=pal, ax=ax)
        ax.set_title(title)
fig.tight_layout()
fig.savefig('palettes.png', dpi=100, bbox_inches='tight')
print('Saved palettes.png')
plt.close()"""},
        {"label": "Despine and axis trimming",
         "code": """import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
df = pd.DataFrame({'x':np.repeat(range(5),30),'y':np.random.randn(150)+np.repeat([1,2,3,4,5],30)})
fig, axes = plt.subplots(1, 2, figsize=(12,5))
with sns.axes_style('ticks'):
    sns.boxplot(data=df, x='x', y='y', ax=axes[0], palette='pastel')
    sns.despine(ax=axes[0], trim=True)
    axes[0].set_title('Despined + trimmed')
with sns.axes_style('whitegrid'):
    sns.violinplot(data=df, x='x', y='y', ax=axes[1], palette='muted', inner='box')
    sns.despine(ax=axes[1], left=False, bottom=False, top=True, right=True)
    axes[1].set_title('Whitegrid + partial despine')
fig.tight_layout()
fig.savefig('despine_styles.png', dpi=100, bbox_inches='tight')
print('Saved despine_styles.png')
plt.close()"""},
    ],
    rw_scenario="Your brand guide specifies 5 hex colors, no top/right borders, consistent font scale, and all reports must use the ticks style for a clean minimal look.",
    rw_code="""import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BRAND = ['#003366','#0066CC','#3399FF','#66B2FF','#99CCFF']
sns.set_theme(style='whitegrid', palette=BRAND, font_scale=1.2,
              rc={'font.family':'sans-serif','axes.spines.top':False,'axes.spines.right':False})
np.random.seed(42)
depts = ['Eng','Sales','Mktg','Support','HR']
df = pd.DataFrame({'dept':np.repeat(depts,40),
                   'satisfaction':np.random.normal(np.tile([7.5,6.8,7.2,6.5,7.8],40)[:200], 1.0)})
fig, axes = plt.subplots(1, 2, figsize=(14,5))
sns.barplot(data=df, x='dept', y='satisfaction', palette=BRAND, ax=axes[0])
axes[0].set_title('Employee Satisfaction by Dept', fontweight='bold')
sns.violinplot(data=df, x='dept', y='satisfaction', palette=BRAND, inner='box', ax=axes[1])
axes[1].set_title('Satisfaction Distribution', fontweight='bold')
fig.suptitle('Q4 Employee Survey', fontsize=16, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig('brand_report.png', dpi=120, bbox_inches='tight')
print('Saved brand_report.png')
sns.set_theme()
plt.close()""",
    practice_title="Night Mode Report",
    practice_desc="Create a dark-themed 3-panel figure (histogram, scatter, bar). Use set_theme with dark facecolor and bright palette. Add suptitle and save at 150 DPI. Reset theme at the end.",
    practice_starter="""import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# TODO: set_theme dark background rc params
# TODO: 3-panel: histplot, scatterplot, barplot
# TODO: suptitle, tight_layout, save 'night_report.png' 150 DPI
# TODO: sns.set_theme() at end"""
)

seaborn_text = sn14 + sn15 + sn16
insert_sections(os.path.join(BASE, 'gen_seaborn.py'), ']  # end SECTIONS', seaborn_text)

# ═══════════════════════════════════════════════════════════════════════════════
# PLOTLY
# ═══════════════════════════════════════════════════════════════════════════════
pl14 = make_section(14, "Plotly Dash Fundamentals",
    [
        {"label": "Dash app structure (code pattern)",
         "code": """# Dash apps run as web servers - this shows the code pattern
print('Dash app structure:')
print('''
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard"),
    dcc.Dropdown(id="metric", options=["Revenue","Users"], value="Revenue"),
    dcc.Graph(id="chart"),
])

@app.callback(Output("chart","figure"), Input("metric","value"))
def update(metric):
    import numpy as np, pandas as pd
    df = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=30),
                        metric: 100 + np.cumsum(np.random.randn(30))})
    return px.line(df, x="date", y=metric, title=f"{metric} over Time")

if __name__ == "__main__":
    app.run_server(debug=True)
''')
print("Run with: python app.py")"""},
        {"label": "Plotly figure for Dash callback",
         "code": """import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

def make_dashboard_fig(category='All'):
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=90, freq='D')
    cats = ['Electronics','Apparel','Food']
    dfs = [pd.DataFrame({'date':dates,'revenue':np.random.exponential(1000,90),'cat':c}) for c in cats]
    df = pd.concat(dfs)
    if category != 'All':
        df = df[df.cat == category]
    fig = px.area(df.groupby(['date','cat'])['revenue'].sum().reset_index(),
                  x='date', y='revenue', color='cat',
                  title=f'Revenue: {category}', template='plotly_white')
    fig.update_layout(hovermode='x unified', height=400)
    return fig

fig = make_dashboard_fig('Electronics')
fig.write_html('dash_callback_fig.html')
print(f'Dashboard figure saved - traces: {len(fig.data)}')"""},
        {"label": "DataTable interactive grid pattern",
         "code": """# Dash DataTable pattern
print('DataTable pattern:')
print('''
from dash import dash_table
import pandas as pd

df = pd.read_csv("data.csv")
table = dash_table.DataTable(
    data=df.to_dict("records"),
    columns=[{"name": c, "id": c} for c in df.columns],
    filter_action="native",
    sort_action="native",
    page_size=10,
    export_format="csv",
    style_data_conditional=[{
        "if": {"filter_query": "{revenue} > 1000"},
        "backgroundColor": "#d4edda",
    }],
)
''')
print('Key features: filter_action, sort_action, export_format, conditional styling')"""},
        {"label": "Multi-page Dash routing",
         "code": """# Multi-page Dash 2.x pattern
print('Multi-page Dash pattern:')
print('''
# pages/home.py
import dash
dash.register_page(__name__, path="/")
layout = html.Div([html.H2("Home")])

# pages/analytics.py
dash.register_page(__name__, path="/analytics")
layout = html.Div([dcc.Graph(figure=create_fig())])

# app.py
app = Dash(__name__, use_pages=True)
app.layout = html.Div([
    html.Nav([
        dcc.Link("Home", href="/"),
        dcc.Link("Analytics", href="/analytics"),
    ]),
    dash.page_container
])
''')
print('Each page: dash.register_page(__name__, path="/route")')"""},
    ],
    rw_scenario="You're building an internal analytics dashboard where users filter by date/category, charts update automatically, and data can be exported as CSV.",
    rw_code="""import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=180, freq='D')
cats = ['Electronics','Apparel','Food']
fig = go.Figure()
for cat in cats:
    rev = np.random.exponential(1000, 180).cumsum()
    fig.add_trace(go.Scatter(x=dates, y=rev, name=cat, mode='lines'))
fig.update_layout(title='Revenue Dashboard Preview', xaxis_title='Date', yaxis_title='Revenue ($)',
                  template='plotly_white', hovermode='x unified',
                  legend=dict(orientation='h', y=-0.2))
fig.write_html('dashboard_preview.html')
print(f'Dashboard saved - {len(fig.data)} traces, {len(dates)} days')""",
    practice_title="Filter Callback",
    practice_desc="Write a function make_fig(year, continent) that filters gapminder data and returns a scatter of GDP vs life expectancy. Call it for (1952,'Asia'), (2007,'Europe'), (2007,'All'). Save each as HTML.",
    practice_starter="""import plotly.express as px

gap = px.data.gapminder()

def make_fig(year, continent):
    # TODO: filter by year and continent ('All' = no continent filter)
    # TODO: return px.scatter size='pop', color='country', log_x=True
    pass

for year, cont in [(1952,'Asia'), (2007,'Europe'), (2007,'All')]:
    fig = make_fig(year, cont)
    if fig:
        fig.write_html(f'gap_{year}_{cont}.html')"""
)

pl15 = make_section(15, "Map Visualizations",
    [
        {"label": "Choropleth world map",
         "code": """import plotly.express as px

df = px.data.gapminder().query("year == 2007")
fig = px.choropleth(df, locations='iso_alpha', color='gdpPercap',
                    hover_name='country', color_continuous_scale='Viridis',
                    range_color=[0, 50000], title='GDP per Capita (2007)',
                    labels={'gdpPercap': 'GDP per Capita'})
fig.update_layout(geo=dict(showframe=False, showcoastlines=True))
fig.write_html('choropleth_world.html')
print(f'Choropleth saved - {len(df)} countries')"""},
        {"label": "Scatter geo map (USA)",
         "code": """import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({'lat':np.random.uniform(25,50,80),'lon':np.random.uniform(-125,-65,80),
                   'city':[f'City_{i}' for i in range(80)],
                   'sales':np.random.exponential(500,80),
                   'category':np.random.choice(['A','B','C'],80)})
fig = px.scatter_geo(df, lat='lat', lon='lon', size='sales', color='category',
                     hover_name='city', scope='usa', title='Sales Distribution USA', size_max=20)
fig.write_html('scatter_map.html')
print(f'Scatter geo saved - {len(df)} points')"""},
        {"label": "Animated choropleth over time",
         "code": """import plotly.express as px

df = px.data.gapminder()
fig = px.choropleth(df, locations='iso_alpha', color='lifeExp',
                    hover_name='country', animation_frame='year',
                    color_continuous_scale='RdYlGn', range_color=[30, 90],
                    title='Life Expectancy Over Time')
fig.update_layout(geo=dict(showframe=False))
fig.write_html('choropleth_animated.html')
print(f'Animated choropleth - {df.year.nunique()} frames')"""},
        {"label": "Density mapbox heatmap",
         "code": """import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({'lat':np.random.normal(40.7128,0.05,400),
                   'lon':np.random.normal(-74.006,0.05,400),
                   'intensity':np.random.exponential(1,400)})
fig = px.density_mapbox(df, lat='lat', lon='lon', z='intensity', radius=15,
                         center=dict(lat=40.7128,lon=-74.006), zoom=10,
                         mapbox_style='open-street-map',
                         title='Event Density (NYC Area)', color_continuous_scale='Inferno')
fig.write_html('density_map.html')
print(f'Density map saved - {len(df)} events')"""},
    ],
    rw_scenario="You need to visualize global customer distribution with bubble sizes for revenue and colors for satisfaction score, animated across 4 quarters.",
    rw_code="""import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
coords = {'USA':(37.09,-95.71),'DEU':(51.16,10.45),'GBR':(55.37,-3.44),
          'JPN':(36.20,138.25),'BRA':(-14.23,-51.92),'IND':(20.59,78.96)}
rows = []
for q in ['Q1','Q2','Q3','Q4']:
    for country,(lat,lon) in coords.items():
        rows.append({'quarter':q,'country':country,'lat':lat+np.random.randn()*0.5,
                     'lon':lon+np.random.randn()*0.5,'revenue':np.random.exponential(500000),
                     'satisfaction':np.random.uniform(3,5)})
df = pd.DataFrame(rows)
fig = px.scatter_geo(df, lat='lat', lon='lon', size='revenue', color='satisfaction',
                     hover_name='country', animation_frame='quarter',
                     color_continuous_scale='RdYlGn', range_color=[3,5], size_max=40,
                     title='Global Customer Revenue & Satisfaction')
fig.write_html('global_map.html')
print(f'Global map saved - {len(df)} records, {df.quarter.nunique()} frames')""",
    practice_title="US State Choropleth",
    practice_desc="Create a choropleth of US states using locationmode='USA-states'. Assign random performance_score (0-100) to each state abbreviation. Color with RdYlGn. Save as HTML.",
    practice_starter="""import plotly.express as px
import pandas as pd
import numpy as np

states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA',
          'KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
          'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT',
          'VA','WA','WV','WI','WY']
np.random.seed(42)
df = pd.DataFrame({'state':states,'score':np.random.uniform(40,100,len(states))})
# TODO: px.choropleth locationmode='USA-states', color='score', scope='usa'
# TODO: color_continuous_scale='RdYlGn'
# TODO: save 'us_choropleth.html'"""
)

pl16 = make_section(16, "3D Plots & Surface Visualizations",
    [
        {"label": "3D surface with contour projections",
         "code": """import plotly.graph_objects as go
import numpy as np

x = y = np.linspace(-3, 3, 60)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))
fig = go.Figure(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis',
                             contours={'z':{'show':True,'start':-1,'end':1,'size':0.25}}))
fig.update_layout(title='3D Surface: sin(sqrt(x2+y2))',
                  scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
                             camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))),
                  width=700, height=500)
fig.write_html('surface_3d.html')
print('3D surface saved')"""},
        {"label": "3D scatter with cluster colors",
         "code": """import plotly.express as px
import numpy as np

np.random.seed(42)
n = 300
x = np.random.randn(n); y = np.random.randn(n)
z = x**2 + y**2 + np.random.randn(n) * 0.5
cats = ['Inner' if v < 2 else 'Middle' if v < 5 else 'Outer' for v in z]
fig = px.scatter_3d(x=x, y=y, z=z, color=cats, symbol=cats,
                    color_discrete_sequence=px.colors.qualitative.Set1,
                    title='3D Scatter by Distance from Origin')
fig.update_traces(marker=dict(size=4, opacity=0.7))
fig.write_html('scatter_3d.html')
print(f'3D scatter saved - {n} points')"""},
        {"label": "3D spiral trajectory",
         "code": """import plotly.graph_objects as go
import numpy as np

t = np.linspace(0, 8*np.pi, 500)
x = np.cos(t)*np.exp(-t/20); y = np.sin(t)*np.exp(-t/20); z = t/(4*np.pi)
fig = go.Figure()
fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines',
                            line=dict(color=t, colorscale='Plasma', width=4), name='Trajectory'))
fig.add_trace(go.Scatter3d(x=[x[0]], y=[y[0]], z=[z[0]], mode='markers',
                            marker=dict(size=8, color='green'), name='Start'))
fig.add_trace(go.Scatter3d(x=[x[-1]], y=[y[-1]], z=[z[-1]], mode='markers',
                            marker=dict(size=8, color='red'), name='End'))
fig.update_layout(title='3D Spiral Trajectory',
                  scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Height'))
fig.write_html('trajectory_3d.html')
print('3D trajectory saved')"""},
        {"label": "Loss landscape with gradient descent",
         "code": """import plotly.graph_objects as go
import numpy as np

x = y = np.linspace(-3, 3, 60)
X, Y = np.meshgrid(x, y)
Z = (np.sin(X*2)*np.cos(Y*2)*0.5 + (X**2+Y**2)*0.1 + np.exp(-((X-1)**2+(Y-1)**2))*(-1.5))
Z = (Z - Z.min()) / (Z.max() - Z.min()) * 3

px_path, py_path, pz_path = [2.5], [-2.5], [float(Z[0,-1])]
lr = 0.08
for _ in range(60):
    ix = int(np.argmin(np.abs(x - px_path[-1])))
    iy = int(np.argmin(np.abs(y - py_path[-1])))
    gx = (Z[iy, min(ix+1,59)] - Z[iy, max(ix-1,0)]) / 2
    gy = (Z[min(iy+1,59), ix] - Z[max(iy-1,0), ix]) / 2
    nx, ny = float(np.clip(px_path[-1]-lr*gx,-3,3)), float(np.clip(py_path[-1]-lr*gy,-3,3))
    px_path.append(nx); py_path.append(ny)
    pz_path.append(float(Z[int(np.argmin(np.abs(y-ny))), int(np.argmin(np.abs(x-nx)))]))

fig = go.Figure([go.Surface(x=X, y=Y, z=Z, colorscale='RdYlGn_r', opacity=0.85),
                  go.Scatter3d(x=px_path, y=py_path, z=pz_path, mode='lines+markers',
                               line=dict(color='blue', width=5), marker=dict(size=3),
                               name='GD Path')])
fig.update_layout(title='Loss Landscape + Gradient Descent', width=750, height=550)
fig.write_html('loss_landscape.html')
print(f'Loss landscape saved - final loss: {pz_path[-1]:.3f}')"""},
    ],
    rw_scenario="You need to visualize a model's loss surface in 3D to understand convergence and identify local minima during hyperparameter search.",
    rw_code="""import plotly.graph_objects as go
import numpy as np

x = y = np.linspace(-3, 3, 60)
X, Y = np.meshgrid(x, y)
np.random.seed(42)
Z = (np.sin(X*1.5)*np.cos(Y*1.5)*0.8 + (X**2+Y**2)*0.15 +
     np.exp(-((X+1)**2+(Y+1)**2))*(-2) + np.random.randn(*X.shape)*0.05)
Z = (Z - Z.min()) / (Z.max() - Z.min()) * 4

best_iy, best_ix = np.unravel_index(Z.argmin(), Z.shape)
fig = go.Figure([
    go.Surface(x=X, y=Y, z=Z, colorscale='RdYlGn_r', opacity=0.85,
               colorbar=dict(title='Loss')),
    go.Scatter3d(x=[x[best_ix]], y=[y[best_iy]], z=[Z.min()],
                 mode='markers', marker=dict(size=12, color='gold', symbol='diamond'),
                 name='Global Min')
])
fig.update_layout(title='Hyperparameter Loss Surface',
                  scene=dict(xaxis_title='param_1', yaxis_title='param_2', zaxis_title='Loss'),
                  width=750, height=550)
fig.write_html('hyperparam_surface.html')
print(f'Surface saved - min loss: {Z.min():.4f} at ({x[best_ix]:.2f}, {y[best_iy]:.2f})')""",
    practice_title="3D Cluster Scatter",
    practice_desc="Generate 3 Gaussian clusters at (0,0,0), (3,3,0), (0,3,3) in 3D. Create a 3D scatter with each cluster in a different color. Add axis labels and save as 'clusters_3d.html'.",
    practice_starter="""import plotly.graph_objects as go
import numpy as np

np.random.seed(42)
centers = [(0,0,0),(3,3,0),(0,3,3)]
colors = ['blue','red','green']
fig = go.Figure()
for i,(cx,cy,cz) in enumerate(centers):
    n = 50
    x = np.random.randn(n)+cx; y = np.random.randn(n)+cy; z = np.random.randn(n)+cz
    # TODO: add Scatter3d trace
    pass
# TODO: update_layout with title, axis labels
# TODO: fig.write_html('clusters_3d.html')"""
)

plotly_text = pl14 + pl15 + pl16
insert_sections(os.path.join(BASE, 'gen_plotly.py'), ']  # end SECTIONS', plotly_text)

# ═══════════════════════════════════════════════════════════════════════════════
# SQL
# ═══════════════════════════════════════════════════════════════════════════════
sq14 = make_section(14, "Query Optimization & Indexing",
    [
        {"label": "EXPLAIN QUERY PLAN",
         "code": """import sqlite3

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER,
                         amount REAL, status TEXT, order_date TEXT);
    INSERT INTO orders SELECT value, (value%100)+1, RANDOM()*1000,
        CASE value%3 WHEN 0 THEN 'pending' WHEN 1 THEN 'completed' ELSE 'cancelled' END,
        date('2024-01-01', '+'||(value%365)||' days')
    FROM generate_series(1, 10000);
''')
plan = conn.execute('''
    EXPLAIN QUERY PLAN
    SELECT customer_id, COUNT(*), AVG(amount)
    FROM orders WHERE status='completed'
    GROUP BY customer_id ORDER BY AVG(amount) DESC
''').fetchall()
print('Query plan (no index):')
for row in plan: print(' ', row)
conn.close()"""},
        {"label": "Index speedup measurement",
         "code": """import sqlite3, time

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE sales (id INTEGER PRIMARY KEY, region TEXT, amount REAL, sale_date TEXT);
    INSERT INTO sales SELECT value, CASE value%4 WHEN 0 THEN 'North' WHEN 1 THEN 'South'
        WHEN 2 THEN 'East' ELSE 'West' END, RANDOM()*1000,
        date('2024-01-01', '+'||(value%365)||' days')
    FROM generate_series(1, 100000);
''')
query = "SELECT region, AVG(amount) FROM sales WHERE sale_date > '2024-06-01' GROUP BY region"
t0 = time.time(); conn.execute(query).fetchall(); t_slow = time.time()-t0
conn.execute('CREATE INDEX idx_date ON sales(sale_date)')
t0 = time.time(); conn.execute(query).fetchall(); t_fast = time.time()-t0
print(f'Without index: {t_slow*1000:.1f}ms')
print(f'With index:    {t_fast*1000:.1f}ms')
print(f'Speedup: {t_slow/max(t_fast,0.001):.1f}x')
conn.close()"""},
        {"label": "Avoiding N+1 with JOINs",
         "code": """import sqlite3

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary REAL);
    CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT);
    INSERT INTO departments VALUES (1,'Engineering'),(2,'Sales'),(3,'HR');
    INSERT INTO employees SELECT v, 'Emp '||v, (v%3)+1, 50000+RANDOM()*50000
    FROM generate_series(1,30) v;
''')
print('=== N+1 (avoid) ===')
for eid,name,dept_id in conn.execute('SELECT id,name,dept_id FROM employees LIMIT 3').fetchall():
    dept = conn.execute('SELECT name FROM departments WHERE id=?',(dept_id,)).fetchone()
    print(f'  {name} -> {dept[0]}')
print('=== Single JOIN (preferred) ===')
for row in conn.execute('SELECT e.name, d.name, e.salary FROM employees e JOIN departments d ON e.dept_id=d.id LIMIT 3').fetchall():
    print(f'  {row[0]} | {row[1]} | ${row[2]:,.0f}')
conn.close()"""},
        {"label": "CTE vs subquery readability",
         "code": """import sqlite3, pandas as pd

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE transactions (id INTEGER PRIMARY KEY, user_id INTEGER,
                               amount REAL, type TEXT, ts TEXT);
    INSERT INTO transactions SELECT v, (v%50)+1, RANDOM()*500,
        CASE v%3 WHEN 0 THEN 'purchase' WHEN 1 THEN 'refund' ELSE 'fee' END,
        date('2024-01-01','+'||(v%300)||' days') FROM generate_series(1,1000) v;
''')
cte_query = '''
    WITH purchase_summary AS (
        SELECT user_id, SUM(amount) total, COUNT(*) cnt
        FROM transactions WHERE type='purchase' GROUP BY user_id
    ), avg_thresh AS (
        SELECT AVG(amount)*5 threshold FROM transactions WHERE type='purchase'
    )
    SELECT ps.user_id, ROUND(ps.total,2) total, ps.cnt
    FROM purchase_summary ps, avg_thresh at WHERE ps.total > at.threshold
    ORDER BY ps.total DESC LIMIT 5
'''
df = pd.read_sql(cte_query, conn)
print('Top buyers via CTE:')
print(df.to_string(index=False))
conn.close()"""},
    ],
    rw_scenario="Your analytics query on 500K rows takes 45 seconds. Use EXPLAIN QUERY PLAN to find bottlenecks and add composite indexes to get it under 1 second.",
    rw_code="""import sqlite3, time

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE events (id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT,
                         product_id INTEGER, revenue REAL, ts TEXT);
    INSERT INTO events SELECT v, (v%10000)+1,
        CASE v%5 WHEN 0 THEN 'view' WHEN 1 THEN 'click' WHEN 2 THEN 'add_cart'
                 WHEN 3 THEN 'purchase' ELSE 'abandon' END,
        (v%1000)+1, CASE v%5 WHEN 3 THEN RANDOM()*200 ELSE 0 END,
        datetime('2024-01-01','+'||(v%365)||' days','+'||(v%86400)||' seconds')
    FROM generate_series(1,200000) v;
''')
q = "SELECT user_id, COUNT(DISTINCT product_id) prods, SUM(revenue) rev FROM events WHERE ts >= '2024-06-01' AND product_id BETWEEN 100 AND 200 GROUP BY user_id HAVING rev > 0 ORDER BY rev DESC LIMIT 20"
t0 = time.time(); conn.execute(q).fetchall(); t1 = time.time()-t0
conn.execute('CREATE INDEX idx_ts ON events(ts)')
conn.execute('CREATE INDEX idx_comp ON events(ts, product_id, user_id)')
t0 = time.time(); res = conn.execute(q).fetchall(); t2 = time.time()-t0
print(f'Without index: {t1*1000:.0f}ms | With: {t2*1000:.0f}ms | Speedup: {t1/max(t2,0.0001):.1f}x')
if res: print(f'Top user: {res[0][0]} - Revenue: ${res[0][2]:.2f}')
conn.close()""",
    practice_title="Index Advisor",
    practice_desc="Create a 100K-row orders table. Time a customer_id filter query WITHOUT index, add the index, re-run, print speedup, and show EXPLAIN QUERY PLAN before vs after.",
    practice_starter="""import sqlite3, time

conn = sqlite3.connect(':memory:')
# TODO: create orders table with 100K rows (id, customer_id, amount, status)
# TODO: time filter query on customer_id=42
# TODO: EXPLAIN QUERY PLAN before index
# TODO: CREATE INDEX idx_cust ON orders(customer_id)
# TODO: time query with index, print speedup
conn.close()"""
)

sq15 = make_section(15, "Pivoting & Unpivoting",
    [
        {"label": "Pivot with CASE WHEN",
         "code": """import sqlite3, pandas as pd

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE sales (year INTEGER, quarter TEXT, region TEXT, revenue REAL);
    INSERT INTO sales VALUES
        (2024,'Q1','North',120000),(2024,'Q2','North',135000),(2024,'Q3','North',118000),(2024,'Q4','North',145000),
        (2024,'Q1','South',98000),(2024,'Q2','South',105000),(2024,'Q3','South',112000),(2024,'Q4','South',125000);
''')
df = pd.read_sql('''
    SELECT region,
        SUM(CASE WHEN quarter='Q1' THEN revenue ELSE 0 END) Q1,
        SUM(CASE WHEN quarter='Q2' THEN revenue ELSE 0 END) Q2,
        SUM(CASE WHEN quarter='Q3' THEN revenue ELSE 0 END) Q3,
        SUM(CASE WHEN quarter='Q4' THEN revenue ELSE 0 END) Q4,
        SUM(revenue) Total
    FROM sales GROUP BY region ORDER BY Total DESC
''', conn)
print(df.to_string(index=False))
conn.close()"""},
        {"label": "Unpivot (wide to long) with UNION ALL",
         "code": """import sqlite3, pandas as pd

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE server_metrics (server TEXT, cpu_pct REAL, mem_pct REAL, disk_pct REAL, net_pct REAL);
    INSERT INTO server_metrics VALUES ('web-01',72.5,65.2,45.0,30.1),
        ('web-02',55.0,70.8,52.3,28.7),('db-01',88.2,91.5,78.4,15.2);
''')
df = pd.read_sql('''
    SELECT server,'CPU' metric, cpu_pct value FROM server_metrics
    UNION ALL SELECT server,'Memory',mem_pct FROM server_metrics
    UNION ALL SELECT server,'Disk',disk_pct FROM server_metrics
    UNION ALL SELECT server,'Network',net_pct FROM server_metrics
    ORDER BY server, metric
''', conn)
print(df.to_string(index=False))
conn.close()"""},
        {"label": "Dynamic pivot with Python",
         "code": """import sqlite3, pandas as pd

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE survey (respondent INTEGER, question TEXT, score INTEGER);
    INSERT INTO survey VALUES (1,'Q1',4),(1,'Q2',5),(1,'Q3',3),(1,'Q4',4),
        (2,'Q1',3),(2,'Q2',4),(2,'Q3',5),(2,'Q4',2),(3,'Q1',5),(3,'Q2',5),(3,'Q3',4),(3,'Q4',5);
''')
questions = [r[0] for r in conn.execute('SELECT DISTINCT question FROM survey ORDER BY question')]
cases = ','.join(f"MAX(CASE WHEN question='{q}' THEN score END) AS {q}" for q in questions)
df = pd.read_sql(f'SELECT respondent, {cases}, ROUND(AVG(score),2) avg_score FROM survey GROUP BY respondent ORDER BY avg_score DESC', conn)
print(df.to_string(index=False))
conn.close()"""},
        {"label": "Cross-tabulation with percentages",
         "code": """import sqlite3, pandas as pd

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE feedback (category TEXT, sentiment TEXT, count INTEGER);
    INSERT INTO feedback VALUES
        ('Product','Positive',450),('Product','Neutral',120),('Product','Negative',80),
        ('Service','Positive',380),('Service','Neutral',95),('Service','Negative',125),
        ('Price','Positive',200),('Price','Neutral',180),('Price','Negative',220);
''')
df = pd.read_sql('''
    SELECT category,
        SUM(CASE WHEN sentiment='Positive' THEN count ELSE 0 END) positive,
        SUM(CASE WHEN sentiment='Neutral' THEN count ELSE 0 END) neutral,
        SUM(CASE WHEN sentiment='Negative' THEN count ELSE 0 END) negative,
        SUM(count) total,
        ROUND(100.0*SUM(CASE WHEN sentiment='Positive' THEN count ELSE 0 END)/SUM(count),1) pct_pos
    FROM feedback GROUP BY category ORDER BY pct_pos DESC
''', conn)
print(df.to_string(index=False))
conn.close()"""},
    ],
    rw_scenario="Your reporting team needs monthly revenue by 5 product categories as a pivot table. Categories come from data dynamically, so you build the query programmatically.",
    rw_code="""import sqlite3, pandas as pd, numpy as np

conn = sqlite3.connect(':memory:')
np.random.seed(42)
cats = ['Electronics','Apparel','Food','Sports','Books']
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
rows = [(c,m,int(np.random.exponential(50000))) for c in cats for m in months]
conn.executescript('CREATE TABLE monthly_sales (category TEXT, month TEXT, revenue INTEGER);')
conn.executemany('INSERT INTO monthly_sales VALUES (?,?,?)', rows)
month_order = {m:i for i,m in enumerate(months)}
month_list = sorted([r[0] for r in conn.execute('SELECT DISTINCT month FROM monthly_sales')],
                     key=lambda m: month_order.get(m,99))
cases = ','.join(f"SUM(CASE WHEN month='{m}' THEN revenue ELSE 0 END) [{m}]" for m in month_list)
query = f'SELECT category, {cases}, SUM(revenue) [Annual Total] FROM monthly_sales GROUP BY category ORDER BY [Annual Total] DESC'
df = pd.read_sql(query, conn)
print('Monthly Revenue Pivot Table:')
print(df.to_string(index=False))
conn.close()""",
    practice_title="Dynamic Sales Pivot",
    practice_desc="Create a sales table with 5 reps and 4 quarters. Get distinct quarters from DB, build a CASE WHEN pivot query dynamically, and display as a DataFrame.",
    practice_starter="""import sqlite3, pandas as pd, numpy as np

conn = sqlite3.connect(':memory:')
np.random.seed(42)
reps = ['Alice','Bob','Carol','Dave','Eve']
quarters = ['Q1','Q2','Q3','Q4']
rows = [(r,q,int(np.random.exponential(80000))) for r in reps for q in quarters]
conn.executescript('CREATE TABLE rep_sales (rep TEXT, quarter TEXT, revenue INTEGER);')
conn.executemany('INSERT INTO rep_sales VALUES (?,?,?)', rows)
# TODO: get distinct quarters dynamically
# TODO: build CASE WHEN pivot query
# TODO: read to DataFrame and print
conn.close()"""
)

sq16 = make_section(16, "Triggers & Database Automation",
    [
        {"label": "Audit log trigger on price UPDATE",
         "code": """import sqlite3

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL);
    CREATE TABLE price_audit (log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER, old_price REAL, new_price REAL,
        changed_at DATETIME DEFAULT CURRENT_TIMESTAMP);
    INSERT INTO products VALUES (1,'Widget',9.99),(2,'Gadget',24.99);
    CREATE TRIGGER log_price AFTER UPDATE OF price ON products
    BEGIN INSERT INTO price_audit(product_id,old_price,new_price)
          VALUES(NEW.id,OLD.price,NEW.price); END;
''')
conn.execute('UPDATE products SET price=12.99 WHERE id=1')
conn.execute('UPDATE products SET price=29.99 WHERE id=2')
for row in conn.execute('SELECT * FROM price_audit').fetchall():
    print(f'Product {row[1]}: ${row[2]} -> ${row[3]}')
conn.close()"""},
        {"label": "Business rule — prevent negative stock",
         "code": """import sqlite3

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE inventory (product_id INTEGER PRIMARY KEY, quantity INTEGER CHECK(quantity >= 0));
    CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, qty INTEGER);
    INSERT INTO inventory VALUES (1,100),(2,5);
    CREATE TRIGGER decrement_stock AFTER INSERT ON orders
    BEGIN UPDATE inventory SET quantity=quantity-NEW.qty WHERE product_id=NEW.product_id; END;
''')
conn.execute('INSERT INTO orders(product_id,qty) VALUES(1,30)')
print('After ordering 30 of product 1:')
for row in conn.execute('SELECT * FROM inventory').fetchall():
    print(f'  Product {row[0]}: {row[1]} units')
try:
    conn.execute('INSERT INTO orders(product_id,qty) VALUES(2,10)')
except Exception as e:
    print(f'Order failed (CHECK constraint): {type(e).__name__}')
conn.close()"""},
        {"label": "Transactional fund transfer (stored proc pattern)",
         "code": """import sqlite3

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance REAL);
    CREATE TABLE transfers (id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INTEGER, to_id INTEGER, amount REAL, ts DATETIME DEFAULT CURRENT_TIMESTAMP);
    INSERT INTO accounts VALUES (1,'Alice',5000),(2,'Bob',1500),(3,'Carol',3200);
''')

def transfer(conn, from_id, to_id, amount):
    bal = conn.execute('SELECT balance FROM accounts WHERE id=?',(from_id,)).fetchone()
    if not bal or bal[0] < amount:
        print(f'  FAILED: ${bal[0] if bal else 0:.2f} < ${amount:.2f}')
        return
    conn.execute('BEGIN')
    conn.execute('UPDATE accounts SET balance=balance-? WHERE id=?',(amount,from_id))
    conn.execute('UPDATE accounts SET balance=balance+? WHERE id=?',(amount,to_id))
    conn.execute('INSERT INTO transfers(from_id,to_id,amount) VALUES(?,?,?)',(from_id,to_id,amount))
    conn.execute('COMMIT')
    print(f'  OK: ${amount:.2f} from acct {from_id} to acct {to_id}')

transfer(conn,1,2,500)
transfer(conn,2,3,3000)  # fails
for row in conn.execute('SELECT id,name,balance FROM accounts').fetchall():
    print(f'{row[1]}: ${row[2]:.2f}')
conn.close()"""},
        {"label": "INSTEAD OF trigger on a view",
         "code": """import sqlite3

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, salary REAL, dept TEXT);
    INSERT INTO employees VALUES (1,'Alice',75000,'Eng'),(2,'Bob',68000,'Sales');
    CREATE VIEW emp_view AS SELECT id, name, salary, dept FROM employees;
    CREATE TRIGGER update_via_view INSTEAD OF UPDATE OF salary ON emp_view
    BEGIN UPDATE employees SET salary=NEW.salary WHERE id=OLD.id; END;
''')
conn.execute("UPDATE emp_view SET salary=90000 WHERE name='Alice'")
for row in conn.execute('SELECT name, salary FROM employees').fetchall():
    print(f'{row[0]}: ${row[1]:,.0f}')
conn.close()"""},
    ],
    rw_scenario="Your e-commerce DB needs: (1) price change audit logs, (2) auto inventory deduction on orders, (3) transactional payment safety with rollback on failure.",
    rw_code="""import sqlite3

conn = sqlite3.connect(':memory:')
conn.executescript('''
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);
    CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER,
                         qty INTEGER, total REAL, status TEXT DEFAULT 'pending');
    CREATE TABLE price_audit (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER,
                              old_price REAL, new_price REAL, pct_change REAL,
                              ts DATETIME DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE stock_alerts (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER,
                               stock INTEGER, alert TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP);
    INSERT INTO products VALUES (1,'Laptop',999.99,50),(2,'Mouse',29.99,200),(3,'Keyboard',79.99,8);
    CREATE TRIGGER audit_price AFTER UPDATE OF price ON products
    BEGIN INSERT INTO price_audit(product_id,old_price,new_price,pct_change)
        VALUES(NEW.id,OLD.price,NEW.price,ROUND(100.0*(NEW.price-OLD.price)/OLD.price,2)); END;
    CREATE TRIGGER low_stock AFTER UPDATE OF stock ON products WHEN NEW.stock < 10
    BEGIN INSERT INTO stock_alerts(product_id,stock,alert)
        VALUES(NEW.id,NEW.stock,CASE WHEN NEW.stock=0 THEN 'OUT_OF_STOCK' ELSE 'LOW_STOCK' END); END;
''')

def place_order(conn, pid, qty):
    row = conn.execute('SELECT stock,price,name FROM products WHERE id=?',(pid,)).fetchone()
    if not row or row[0] < qty:
        print(f'  FAILED: {row[0] if row else 0} in stock'); return
    conn.execute('INSERT INTO orders(product_id,qty,total,status) VALUES(?,?,?,\"completed\")',(pid,qty,row[1]*qty))
    conn.execute('UPDATE products SET stock=stock-? WHERE id=?',(qty,pid))
    print(f'  Ordered {qty}x {row[2]} = ${row[1]*qty:.2f}')

conn.execute('UPDATE products SET price=899.99 WHERE id=1')
conn.execute('UPDATE products SET price=34.99 WHERE id=2')
place_order(conn,1,5); place_order(conn,3,5); place_order(conn,2,250)
print('Price Audit:')
for r in conn.execute('SELECT product_id,old_price,new_price,pct_change FROM price_audit').fetchall():
    print(f'  Product {r[0]}: ${r[1]} -> ${r[2]} ({r[3]:+.1f}%)')
print('Stock Alerts:')
for r in conn.execute('SELECT product_id,stock,alert FROM stock_alerts').fetchall():
    print(f'  Product {r[0]}: {r[2]} ({r[1]} units)')
conn.close()""",
    practice_title="Banking Triggers",
    practice_desc="Create accounts and transactions tables. Add triggers: (1) log withdrawals >$1000 to large_withdrawals, (2) prevent negative balances. Test with 5 transactions including one that should fail.",
    practice_starter="""import sqlite3

conn = sqlite3.connect(':memory:')
# TODO: CREATE TABLE accounts (id, name, balance)
# TODO: CREATE TABLE large_withdrawals (id AUTOINCREMENT, account_id, amount, ts)
# TODO: CREATE TRIGGER log_large after INSERT on transactions WHEN amount > 1000
# TODO: enforce non-negative balance via CHECK or trigger
# TODO: insert test transactions, show results
conn.close()"""
)

sql_text = sq14 + sq15 + sq16
insert_sections(os.path.join(BASE, 'gen_sql.py'), ']  # end SECTIONS', sql_text)

print("\nAll 3 files done! Run generators to verify.")
