"""Add Seaborn sections 25-32 to gen_seaborn.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _inserter import insert_sections

FILE   = pathlib.Path(__file__).parent / "gen_seaborn.py"
MARKER = "]  # end SECTIONS"

HDR = (
    "import matplotlib\n"
    "matplotlib.use('Agg')\n"
    "import seaborn as sns\n"
    "import matplotlib.pyplot as plt\n"
    "import numpy as np\n"
    "import pandas as pd\n\n"
)

def ec(s):
    return (s.replace('\\','\\\\').replace('"','\\"')
             .replace('\n','\\n').replace("'","\\'"))

def make_sns(num, title, desc, examples, rw_title, rw_scenario, rw_code, pt, pd_text, ps):
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

# ── Section 25: Heatmap Advanced ──────────────────────────────────────────────
s25 = make_sns(
    25, "Heatmap Advanced",
    "Go beyond basic heatmaps: annotate with custom formats, apply diverging colormaps for signed values, mask upper triangles, and combine with matplotlib for multi-panel layouts.",
    [
        {"label": "Masked upper-triangle correlation heatmap", "code": HDR + """\
sns.set_theme(style='white')
np.random.seed(0)
n = 8
labels = [f'Var_{i}' for i in range(1, n+1)]
data = np.random.randn(200, n)
for i in range(n):
    for j in range(i):
        data[:, j] += data[:, i] * np.random.uniform(-0.5, 0.8)
corr = np.corrcoef(data.T)
df_corr = pd.DataFrame(corr, index=labels, columns=labels)

mask = np.triu(np.ones_like(corr, dtype=bool), k=1)  # mask upper

fig, ax = plt.subplots(figsize=(8, 7))
sns.heatmap(df_corr, mask=mask, cmap='RdBu_r', vmin=-1, vmax=1,
            annot=True, fmt='.2f', linewidths=0.5,
            ax=ax, square=True, cbar_kws={'label': 'Pearson r'})
ax.set_title('Lower-Triangle Correlation Matrix', fontweight='bold')
fig.tight_layout()
fig.savefig('corr_heatmap.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved corr_heatmap.png')"""},
        {"label": "Heatmap with custom fmt and colorbar", "code": HDR + """\
sns.set_theme(style='white')
np.random.seed(1)
days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
hours = [f'{h:02d}:00' for h in range(7, 23)]
traffic = np.random.poisson(50, (len(hours), len(days)))
traffic[:, 5:] = np.random.poisson(80, (len(hours), 2))
traffic[8:12, :] += 30
traffic[17:20, :] += 40

df = pd.DataFrame(traffic, index=hours, columns=days)
fig, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(df, cmap='YlOrRd', annot=True, fmt='d',
            linewidths=0.3, ax=ax,
            cbar_kws={'label': 'Page Views', 'shrink': 0.8})
ax.set_title('Website Traffic by Hour & Day', fontweight='bold')
ax.set_xlabel('Day of Week'); ax.set_ylabel('Hour')
fig.tight_layout()
fig.savefig('traffic_heatmap.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved traffic_heatmap.png')"""},
        {"label": "Heatmap with custom annotation text", "code": HDR + """\
sns.set_theme(style='white')
np.random.seed(2)
models = ['LR','RF','XGB','SVM','NN']
metrics = ['Accuracy','Precision','Recall','F1','AUC']
values = np.random.uniform(0.70, 0.98, (len(models), len(metrics)))
df = pd.DataFrame(values, index=models, columns=metrics)

# Custom annotations: highlight best per metric
annot = df.copy().applymap(lambda v: f'{v:.3f}')
best_rows = df.idxmax(axis=0)
highlights = pd.DataFrame('', index=df.index, columns=df.columns)
for metric in metrics:
    highlights.loc[best_rows[metric], metric] = f'★{df.loc[best_rows[metric],metric]:.3f}'

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(df, cmap='Blues', vmin=0.65, vmax=1.0, ax=ax,
            annot=df.round(3), fmt='', linewidths=0.5)
ax.set_title('Model Comparison Heatmap (★ = best per metric)', fontweight='bold')
fig.tight_layout()
fig.savefig('model_heatmap.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved model_heatmap.png')"""},
        {"label": "Diverging heatmap for signed changes", "code": HDR + """\
sns.set_theme(style='white')
np.random.seed(3)
products = [f'P{i:02d}' for i in range(1, 9)]
kpis = ['Revenue','Margin','Units','Traffic','Conv%','Retention']
changes = np.random.randn(len(products), len(kpis)) * 15
df = pd.DataFrame(changes, index=products, columns=kpis)

fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(df, cmap='RdYlGn', center=0,
            annot=True, fmt='.1f', linewidths=0.5, ax=ax,
            cbar_kws={'label': 'YoY Change (%)'})
ax.set_title('Product KPI Year-over-Year Change (%)', fontweight='bold')
fig.tight_layout()
fig.savefig('diverging_heatmap.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved diverging_heatmap.png')"""},
    ],
    "Confusion Matrix Dashboard",
    "Create a styled confusion matrix heatmap for a 5-class classifier. Normalize by true class (row), show counts in top-left and percentages in bottom-right of each cell, use Blues cmap.",
    HDR + """\
sns.set_theme(style='white')
np.random.seed(42)
classes = ['Cat','Dog','Bird','Fish','Horse']
n = 5
cm = np.array([
    [45, 3, 1, 0, 1],
    [2, 48, 0, 1, 0],
    [1, 0, 42, 3, 2],
    [0, 1, 4, 44, 1],
    [2, 0, 3, 1, 43]
])
cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)

# Build annotation: count + pct
annot = np.empty_like(cm, dtype=object)
for i in range(n):
    for j in range(n):
        annot[i,j] = f'{cm[i,j]}\n{cm_norm[i,j]*100:.1f}%'

fig, ax = plt.subplots(figsize=(8, 7))
sns.heatmap(cm_norm, annot=annot, fmt='', cmap='Blues',
            xticklabels=classes, yticklabels=classes,
            vmin=0, vmax=1, linewidths=0.5, ax=ax,
            cbar_kws={'label': 'Precision (row-normalized)'})
ax.set_title('5-Class Confusion Matrix', fontweight='bold', fontsize=13)
ax.set_xlabel('Predicted'); ax.set_ylabel('True')
fig.tight_layout()
fig.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved confusion_matrix.png')""",
    "Heatmap Practice",
    "Generate a 10x6 DataFrame of monthly sales by region (random integers 100-500). Create: (1) a standard heatmap with annot=True and YlGn cmap, (2) the same data as a diverging heatmap centered on the mean (RdYlGn), side by side in a 1x2 figure.",
    HDR + """\
sns.set_theme(style='white')
np.random.seed(9)
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][:10]
regions = ['North','South','East','West','Central','Pacific']
df = pd.DataFrame(np.random.randint(100,500,(10,6)), index=months, columns=regions)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
# TODO: standard heatmap YlGn on ax1, annot=True
# TODO: diverging heatmap RdYlGn centered at mean on ax2
# TODO: titles, tight_layout, save 'sales_heatmap.png'
plt.close()"""
)

# ── Section 26: PairGrid Advanced ─────────────────────────────────────────────
s26 = make_sns(
    26, "PairGrid Advanced",
    "Use PairGrid for full control over diagonal, upper, and lower triangle plots. Map different plot types per region and use hue for group-aware multi-variable comparison.",
    [
        {"label": "PairGrid: hist diagonal, scatter off-diag", "code": HDR + """\
sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')

g = sns.PairGrid(iris, hue='species', palette='Set2',
                 vars=['sepal_length','sepal_width','petal_length','petal_width'])
g.map_diag(sns.histplot, kde=True, alpha=0.6)
g.map_offdiag(sns.scatterplot, s=25, alpha=0.6)
g.add_legend(title='Species')
g.fig.suptitle('PairGrid: Histogram Diagonal + Scatter', y=1.01, fontweight='bold')
g.fig.savefig('pairgrid_hist.png', dpi=100, bbox_inches='tight')
plt.close(g.fig)
print('Saved pairgrid_hist.png')"""},
        {"label": "PairGrid: KDE diagonal, upper KDE, lower scatter", "code": HDR + """\
sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')
vars_ = ['sepal_length','sepal_width','petal_length','petal_width']

g = sns.PairGrid(iris, hue='species', palette='Set1', vars=vars_)
g.map_diag(sns.kdeplot, fill=True, alpha=0.4, linewidth=1.5)
g.map_upper(sns.kdeplot, levels=4, warn_singular=False)
g.map_lower(sns.scatterplot, s=20, alpha=0.5)
g.add_legend(title='Species', fontsize=9)
g.fig.suptitle('PairGrid: KDE + Scatter Split', y=1.01, fontweight='bold')
g.fig.savefig('pairgrid_split.png', dpi=100, bbox_inches='tight')
plt.close(g.fig)
print('Saved pairgrid_split.png')"""},
        {"label": "PairGrid: boxplot on diagonal", "code": HDR + """\
sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')
vars_ = ['sepal_length','petal_length','petal_width']

g = sns.PairGrid(iris, hue='species', palette='Set2', vars=vars_)

def diag_box(x, **kwargs):
    ax = plt.gca()
    data = kwargs.get('data', x)
    groups = x.groupby(level=0) if hasattr(x,'groupby') else None
    ax.boxplot([x[x.index == i] for i in x.unique()], vert=True)

g.map_diag(sns.kdeplot, fill=True, alpha=0.5)
g.map_upper(sns.scatterplot, s=20, alpha=0.5)
g.map_lower(sns.regplot, scatter_kws=dict(s=10,alpha=0.4),
            line_kws=dict(linewidth=1.5))
g.add_legend()
g.fig.suptitle('PairGrid: KDE / Scatter / Regression', y=1.01, fontweight='bold')
g.fig.savefig('pairgrid_reg.png', dpi=100, bbox_inches='tight')
plt.close(g.fig)
print('Saved pairgrid_reg.png')"""},
        {"label": "PairGrid with correlation annotation", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(0)
n = 150
df = pd.DataFrame({
    'A': np.random.randn(n),
    'B': np.random.randn(n),
    'C': np.random.randn(n),
    'group': np.random.choice(['X','Y'], n)
})
df['B'] += df['A'] * 0.7
df['C'] = df['A'] * (-0.5) + np.random.randn(n) * 0.7

def corrfunc(x, y, **kwargs):
    r = np.corrcoef(x, y)[0,1]
    ax = plt.gca()
    ax.annotate(f'r = {r:.2f}', xy=(0.5,0.5), xycoords='axes fraction',
                ha='center', va='center', fontsize=12,
                color='darkred' if abs(r) > 0.4 else 'gray',
                fontweight='bold' if abs(r) > 0.4 else 'normal')

g = sns.PairGrid(df[['A','B','C','group']], hue='group', palette='Set1',
                 vars=['A','B','C'])
g.map_diag(sns.kdeplot, fill=True, alpha=0.4)
g.map_lower(sns.scatterplot, s=20, alpha=0.5)
g.map_upper(corrfunc)
g.add_legend()
g.fig.suptitle('PairGrid: Lower=Scatter, Upper=Correlation', y=1.01, fontweight='bold')
g.fig.savefig('pairgrid_corr.png', dpi=100, bbox_inches='tight')
plt.close(g.fig)
print('Saved pairgrid_corr.png')"""},
    ],
    "Penguins Multi-Variable EDA",
    "Create a PairGrid on the penguins dataset (4 numeric features, hue=species): diagonal = KDE filled, upper = KDE contour, lower = scatter. Annotate correlation values in each upper cell.",
    HDR + """\
sns.set_theme(style='whitegrid')
penguins = sns.load_dataset('penguins').dropna()
vars_ = ['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g']

def upper_corr(x, y, **kwargs):
    r = np.corrcoef(x, y)[0,1]
    ax = plt.gca()
    ax.annotate(f'r={r:.2f}', xy=(0.5,0.5), xycoords='axes fraction',
                ha='center', va='center', fontsize=10,
                color='darkred' if abs(r) > 0.5 else 'gray',
                fontweight='bold')

g = sns.PairGrid(penguins, hue='species', palette='Set2', vars=vars_)
g.map_diag(sns.kdeplot, fill=True, alpha=0.5, linewidth=1.5)
g.map_lower(sns.scatterplot, s=20, alpha=0.5)
g.map_upper(upper_corr)
g.add_legend(title='Species')
g.fig.suptitle('Penguins PairGrid EDA', y=1.01, fontweight='bold')
g.fig.savefig('penguins_pairgrid.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved penguins_pairgrid.png')""",
    "PairGrid Practice",
    "Load the 'mpg' dataset. Create a PairGrid with vars=['mpg','horsepower','weight','acceleration'], hue='origin'. Map: diagonal=histplot, upper=scatterplot, lower=regplot. Add legend and a suptitle.",
    HDR + """\
sns.set_theme(style='whitegrid')
mpg = sns.load_dataset('mpg').dropna()
vars_ = ['mpg','horsepower','weight','acceleration']

g = sns.PairGrid(mpg, hue='origin', palette='tab10', vars=vars_)
# TODO: map_diag histplot
# TODO: map_upper scatterplot
# TODO: map_lower regplot (scatter_kws, line_kws)
# TODO: add_legend, suptitle
# TODO: save 'mpg_pairgrid.png'"""
)

# ── Section 27: Residual & Regression Diagnostics ────────────────────────────
s27 = make_sns(
    27, "Residual & Regression Diagnostics",
    "Use residplot() for visual residual checks, lmplot() for grouped regression, and regplot() with custom order for polynomial fits. Combine with matplotlib for full diagnostic panels.",
    [
        {"label": "residplot: detect non-linearity", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(0)
n = 150
x = np.linspace(0, 10, n)
y_linear  = 2*x + 1 + np.random.randn(n)*2
y_nonlin  = 2*x + 0.3*x**2 + np.random.randn(n)*3

df = pd.DataFrame({'x':x,'y_linear':y_linear,'y_nonlin':y_nonlin})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
sns.residplot(data=df, x='x', y='y_linear', lowess=True,
              scatter_kws=dict(alpha=0.5, s=20),
              line_kws=dict(color='red', linewidth=2), ax=ax1)
ax1.set_title('Residuals: Linear Data (good fit)')
ax1.axhline(0, color='gray', linestyle='--', linewidth=1)

sns.residplot(data=df, x='x', y='y_nonlin', lowess=True,
              scatter_kws=dict(alpha=0.5, s=20),
              line_kws=dict(color='red', linewidth=2), ax=ax2)
ax2.set_title('Residuals: Nonlinear Data (pattern visible)')
ax2.axhline(0, color='gray', linestyle='--', linewidth=1)

fig.suptitle('residplot — Lowess Smoother', fontweight='bold')
fig.tight_layout()
fig.savefig('residplot.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved residplot.png')"""},
        {"label": "lmplot: grouped regression per hue", "code": HDR + """\
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

g = sns.lmplot(data=tips, x='total_bill', y='tip',
               hue='sex', palette='Set1',
               scatter_kws=dict(s=30, alpha=0.6),
               line_kws=dict(linewidth=2),
               height=5, aspect=1.3)
g.set_axis_labels('Total Bill ($)', 'Tip ($)')
g.fig.suptitle('lmplot: Regression by Sex', y=1.02, fontweight='bold')
g.fig.savefig('lmplot_hue.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved lmplot_hue.png')"""},
        {"label": "lmplot with col faceting", "code": HDR + """\
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

g = sns.lmplot(data=tips, x='total_bill', y='tip',
               col='time', hue='smoker',
               palette='Set2',
               scatter_kws=dict(s=30, alpha=0.6),
               height=4, aspect=1.1)
g.set_axis_labels('Total Bill ($)', 'Tip ($)')
g.set_titles(col_template='{col_name}')
g.fig.suptitle('lmplot: Regression by Time and Smoker', y=1.02, fontweight='bold')
g.fig.savefig('lmplot_col.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved lmplot_col.png')"""},
        {"label": "Polynomial regression with regplot order", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(1)
x = np.linspace(-3, 3, 100)
y = 2*x**3 - x**2 + x + np.random.randn(100)*3
df = pd.DataFrame({'x':x,'y':y})

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
for ax, order, title in zip(axes, [1,2,3], ['Linear (order=1)','Quadratic (order=2)','Cubic (order=3)']):
    sns.regplot(data=df, x='x', y='y', order=order,
                scatter_kws=dict(s=15, alpha=0.5),
                line_kws=dict(linewidth=2, color='tomato'),
                ax=ax)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
fig.suptitle('Polynomial Regression Orders with regplot', fontweight='bold')
fig.tight_layout()
fig.savefig('poly_regplot.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved poly_regplot.png')"""},
    ],
    "Housing Price Regression Diagnostics",
    "Fit a linear regression of house price on size and show: (1) lmplot by neighborhood, (2) residplot of residuals, (3) regplot with CI band.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(33)
hoods = ['Downtown','Suburbs','Rural']
rows = []
for hood in hoods:
    base = {'Downtown':300,'Suburbs':200,'Rural':120}[hood]
    n = 80
    size = np.random.uniform(50, 250, n)
    price = base + 1.2*size + np.random.randn(n)*30
    rows.append(pd.DataFrame({'size_sqm':size,'price_k':price,'neighborhood':hood}))
df = pd.concat(rows, ignore_index=True)

g = sns.lmplot(data=df, x='size_sqm', y='price_k', col='neighborhood',
               hue='neighborhood', palette='Set2',
               scatter_kws=dict(s=25, alpha=0.6),
               line_kws=dict(linewidth=2),
               height=4, aspect=1.0, legend=False)
g.set_axis_labels('Size (sqm)', 'Price ($K)')
g.set_titles(col_template='{col_name}')
g.fig.suptitle('Housing Price Regression by Neighborhood', y=1.02, fontweight='bold')
g.fig.savefig('housing_regression.png', dpi=150, bbox_inches='tight')
plt.close(g.fig)
print('Saved housing_regression.png')""",
    "Regression Diagnostics Practice",
    "Generate 100 data points: x = linspace(0,10), y = sin(x) + noise. Use a 1x3 panel: (1) regplot order=1, (2) regplot order=3, (3) residplot for the order=3 fit. Use whitegrid style.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(4)
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.randn(100)*0.4
df = pd.DataFrame({'x':x,'y':y})

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
# TODO: regplot order=1 on axes[0]
# TODO: regplot order=3 on axes[1]
# TODO: residplot order=3 on axes[2]
fig.suptitle('Regression & Residuals: sin(x)', fontweight='bold')
fig.tight_layout()
fig.savefig('sin_regression.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved sin_regression.png')"""
)

# ── Section 28: Mixed Seaborn + Matplotlib ────────────────────────────────────
s28 = make_sns(
    28, "Mixed Seaborn + Matplotlib",
    "Combine Seaborn plots with raw matplotlib artists: add reference lines, spans, custom patches, secondary axes, and annotations on top of seaborn outputs.",
    [
        {"label": "Add reference line and span to seaborn plot", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(0)
df = pd.DataFrame({
    'score': np.random.normal(72, 15, 200),
    'group': np.random.choice(['A','B','C','D'], 200)
})

fig, ax = plt.subplots(figsize=(9, 5))
sns.boxplot(data=df, x='group', y='score', palette='Set2', ax=ax)

# Matplotlib overlays
ax.axhline(70, color='red', linestyle='--', linewidth=2, label='Target')
ax.axhspan(0, 60, color='red', alpha=0.07, label='Fail zone')
ax.axhspan(90, 100, color='green', alpha=0.07, label='Excellent')
ax.set_title('Test Scores by Group with Reference Lines', fontweight='bold')
ax.legend()
ax.set_ylim(20, 110)
fig.tight_layout()
fig.savefig('sns_mpl_lines.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved sns_mpl_lines.png')"""},
        {"label": "Annotate outliers on seaborn plot", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(1)
df = pd.DataFrame({
    'revenue': np.concatenate([np.random.normal(100, 20, 95), [220, 230, 240, 10, 5]]),
    'region': np.random.choice(['East','West'], 100)
})

fig, ax = plt.subplots(figsize=(9, 5))
sns.stripplot(data=df, x='region', y='revenue', jitter=True,
              palette='Set2', size=6, alpha=0.7, ax=ax)

# Annotate extreme outliers
q1, q3 = df.revenue.quantile([0.25, 0.75])
iqr = q3 - q1
outliers = df[df.revenue > q3 + 1.5*iqr]
for _, row in outliers.iterrows():
    x_jit = {'East':0,'West':1}[row.region] + np.random.uniform(-0.1,0.1)
    ax.annotate(f'${row.revenue:.0f}K',
                xy=(x_jit, row.revenue),
                xytext=(x_jit+0.2, row.revenue),
                fontsize=8, color='darkred',
                arrowprops=dict(arrowstyle='->', color='darkred', lw=1))

ax.axhline(q3+1.5*iqr, color='red', linestyle='--', linewidth=1.2, label='Upper fence')
ax.set_title('Revenue Distribution with Outlier Annotations', fontweight='bold')
ax.legend()
fig.tight_layout()
fig.savefig('sns_annotate_outliers.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved sns_annotate_outliers.png')"""},
        {"label": "seaborn heatmap + matplotlib patch overlay", "code": HDR + """\
import matplotlib.patches as mpatches

sns.set_theme(style='white')
np.random.seed(2)
data = np.random.randn(8, 8)
data[2:4, 5:7] += 3  # hot cluster

fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(data, cmap='RdBu_r', center=0, ax=ax,
            annot=True, fmt='.1f', linewidths=0.3)

# Highlight cluster with rectangle
rect = mpatches.Rectangle((5, 2), 2, 2,
    linewidth=3, edgecolor='gold', facecolor='none',
    transform=ax.transData)
ax.add_patch(rect)
ax.text(6.5, 1.7, 'Hot cluster', ha='center', fontsize=10,
        color='gold', fontweight='bold')
ax.set_title('Heatmap with Cluster Highlight', fontweight='bold')
fig.tight_layout()
fig.savefig('sns_heatmap_patch.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved sns_heatmap_patch.png')"""},
        {"label": "twinx on seaborn axes", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(3)
months = list(range(1, 13))
df = pd.DataFrame({
    'month': months,
    'revenue': [80+i*5+np.random.randn()*4 for i in range(12)],
    'users': [1000+i*80+np.random.randn()*50 for i in range(12)]
})

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

sns.lineplot(data=df, x='month', y='revenue', color='steelblue',
             linewidth=2, marker='o', label='Revenue ($K)', ax=ax1)
sns.lineplot(data=df, x='month', y='users', color='tomato',
             linewidth=2, marker='s', linestyle='--', label='Users', ax=ax2)

ax1.set_ylabel('Revenue ($K)', color='steelblue')
ax2.set_ylabel('Users', color='tomato')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax2.tick_params(axis='y', labelcolor='tomato')
ax1.set_xlabel('Month')

lines1, lab1 = ax1.get_legend_handles_labels()
lines2, lab2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, lab1+lab2, loc='upper left')
ax1.get_legend().remove() if ax2.get_legend() else None
ax1.set_title('Revenue & Users (seaborn + twinx)', fontweight='bold')
fig.tight_layout()
fig.savefig('sns_twinx.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved sns_twinx.png')"""},
    ],
    "Marketing KPI Report",
    "Combine a seaborn barplot for monthly revenue with twinx for conversion rate, axhspan for target zones, and annotate bars that exceed the target with a star marker.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(88)
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
revenue = [120+i*8+np.random.randn()*10 for i in range(12)]
conv_rate = [3.2+i*0.1+np.random.randn()*0.2 for i in range(12)]
target_rev = 160

df = pd.DataFrame({'month':months,'revenue':revenue,'conv_rate':conv_rate})

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

bar_colors = ['seagreen' if r >= target_rev else 'steelblue' for r in revenue]
bars = ax1.bar(months, revenue, color=bar_colors, alpha=0.7, width=0.6)
ax2.plot(months, conv_rate, 'ro-', linewidth=2, markersize=6, label='Conv Rate (%)')

ax1.axhline(target_rev, color='green', linestyle='--', linewidth=2, label='Revenue target')
ax1.axhspan(target_rev, max(revenue)*1.05, color='green', alpha=0.05)

# Annotate exceeding months
for i,(m,r) in enumerate(zip(months,revenue)):
    if r >= target_rev:
        ax1.text(i, r+3, '★', ha='center', fontsize=14, color='gold')

ax1.set_ylabel('Revenue ($K)', color='steelblue')
ax2.set_ylabel('Conversion Rate (%)', color='tomato')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax2.tick_params(axis='y', labelcolor='tomato')
lines1, lab1 = ax1.get_legend_handles_labels()
lines2, lab2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, lab1+lab2, loc='upper left')
ax1.set_title('Marketing KPI: Revenue vs Conversion Rate', fontweight='bold', fontsize=13)
fig.tight_layout()
fig.savefig('marketing_kpi.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved marketing_kpi.png')""",
    "Mixed Plot Practice",
    "Create a seaborn violinplot of exam scores by subject (4 subjects). Overlay a horizontal line at the passing grade (60), a shaded band for distinction (85-100), and annotate the subject with highest median. Use whitegrid style.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(5)
subjects = ['Math','Science','English','History']
df = pd.DataFrame({
    'score': np.concatenate([np.random.normal(m, 15, 80) for m in [65,70,75,60]]).clip(0,100),
    'subject': np.repeat(subjects, 80)
})

fig, ax = plt.subplots(figsize=(9, 5))
# TODO: violinplot
# TODO: axhline at 60 (passing)
# TODO: axhspan 85-100 (distinction zone)
# TODO: annotate highest median subject
# TODO: save 'exam_violin.png'
plt.close()"""
)

# ── Section 29: Seaborn with Real Datasets ────────────────────────────────────
s29 = make_sns(
    29, "Seaborn with Real Datasets",
    "Practice EDA workflows on seaborn's built-in datasets: titanic, penguins, diamonds, mpg, and fmri. Apply multiple plot types to reveal patterns, relationships, and anomalies.",
    [
        {"label": "Titanic survival EDA", "code": HDR + """\
sns.set_theme(style='whitegrid')
titanic = sns.load_dataset('titanic')

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
# Survival by class
sns.barplot(data=titanic, x='class', y='survived', hue='sex',
            palette='Set1', capsize=0.08, ax=axes[0,0])
axes[0,0].set_title('Survival Rate by Class & Sex')
axes[0,0].set_ylim(0,1)

# Age distribution by survival
sns.kdeplot(data=titanic.dropna(subset=['age']), x='age', hue='survived',
            fill=True, alpha=0.4, palette='Set2', ax=axes[0,1])
axes[0,1].set_title('Age Distribution by Survival')

# Fare vs survival (box)
sns.boxplot(data=titanic, x='class', y='fare', hue='survived',
            palette='pastel', ax=axes[1,0])
axes[1,0].set_title('Fare Distribution by Class & Survival')

# Count by embarkation port
sns.countplot(data=titanic, x='embarked', hue='survived',
              palette='Set2', ax=axes[1,1])
axes[1,1].set_title('Counts by Port of Embarkation')

fig.suptitle('Titanic Dataset — EDA Dashboard', fontweight='bold', fontsize=13)
fig.tight_layout()
fig.savefig('titanic_eda.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved titanic_eda.png')"""},
        {"label": "Diamonds dataset analysis", "code": HDR + """\
sns.set_theme(style='whitegrid')
diamonds = sns.load_dataset('diamonds')
sample = diamonds.sample(2000, random_state=42)

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
# Price by cut
sns.violinplot(data=sample, x='cut', y='price', palette='Set2',
               inner='quartile', ax=axes[0])
axes[0].set_title('Price by Cut')

# Carat vs price scatter
sns.scatterplot(data=sample, x='carat', y='price', hue='color',
                palette='RdYlGn', s=15, alpha=0.5, ax=axes[1])
axes[1].set_title('Carat vs Price by Color')

# Correlation heatmap of numeric cols
corr = sample[['carat','depth','table','price','x','y','z']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, linewidths=0.5, ax=axes[2])
axes[2].set_title('Feature Correlation')

fig.suptitle('Diamonds EDA', fontweight='bold', fontsize=13)
fig.tight_layout()
fig.savefig('diamonds_eda.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved diamonds_eda.png')"""},
        {"label": "Penguins complete EDA", "code": HDR + """\
sns.set_theme(style='whitegrid')
penguins = sns.load_dataset('penguins').dropna()

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
sns.scatterplot(data=penguins, x='bill_length_mm', y='bill_depth_mm',
                hue='species', style='island', s=60, alpha=0.7, ax=axes[0,0])
axes[0,0].set_title('Bill Length vs Depth by Species & Island')

sns.violinplot(data=penguins, x='species', y='body_mass_g',
               hue='sex', split=True, palette='Set2', inner='box',
               ax=axes[0,1])
axes[0,1].set_title('Body Mass by Species & Sex')

sns.ecdfplot(data=penguins, x='flipper_length_mm', hue='species',
             palette='Set1', linewidth=2, ax=axes[1,0])
axes[1,0].set_title('Flipper Length ECDF by Species')

counts = penguins.groupby(['species','island']).size().reset_index(name='count')
sns.barplot(data=counts, x='species', y='count', hue='island',
            palette='pastel', ax=axes[1,1])
axes[1,1].set_title('Population by Species & Island')

fig.suptitle('Penguins Complete EDA', fontweight='bold', fontsize=13)
fig.tight_layout()
fig.savefig('penguins_eda.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved penguins_eda.png')"""},
        {"label": "MPG fuel efficiency analysis", "code": HDR + """\
sns.set_theme(style='whitegrid')
mpg = sns.load_dataset('mpg').dropna()

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
# MPG trend by model year and origin
sns.lineplot(data=mpg, x='model_year', y='mpg', hue='origin',
             palette='Set1', linewidth=2, markers=True, ax=axes[0])
axes[0].set_title('MPG by Year & Origin')

# Weight vs MPG regression by cylinders
cyl_order = sorted(mpg['cylinders'].unique())
pal = sns.color_palette('coolwarm', len(cyl_order))
for i, cyl in enumerate(cyl_order):
    sub = mpg[mpg.cylinders == cyl]
    axes[1].scatter(sub.weight, sub.mpg, s=20, alpha=0.5, color=pal[i], label=f'{cyl}cyl')
axes[1].set_xlabel('Weight (lbs)'); axes[1].set_ylabel('MPG')
axes[1].legend(title='Cylinders', fontsize=8); axes[1].set_title('Weight vs MPG by Cylinders')

# Horsepower distribution by origin
sns.boxplot(data=mpg, x='origin', y='horsepower', palette='Set2', ax=axes[2])
axes[2].set_title('Horsepower by Origin')

fig.suptitle('MPG Dataset — Fuel Efficiency EDA', fontweight='bold', fontsize=13)
fig.tight_layout()
fig.savefig('mpg_eda.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved mpg_eda.png')"""},
    ],
    "Complete Data Story",
    "Using the 'diamonds' dataset: tell a 4-panel data story: (1) price distribution by cut (violin), (2) price vs carat regression by clarity, (3) ECDF of price by cut, (4) heatmap of median price by cut×color.",
    HDR + """\
sns.set_theme(style='whitegrid')
diamonds = sns.load_dataset('diamonds')
sample = diamonds.sample(3000, random_state=7)
cut_order = ['Fair','Good','Very Good','Premium','Ideal']

fig, axes = plt.subplots(2, 2, figsize=(13, 10))

sns.violinplot(data=sample, x='cut', y='price', palette='YlOrRd',
               inner='quartile', order=cut_order, ax=axes[0,0])
axes[0,0].set_title('Price by Cut', fontweight='bold')
axes[0,0].set_xlabel('Cut'); axes[0,0].set_ylabel('Price ($)')

clarity_order = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
sns.scatterplot(data=sample, x='carat', y='price', hue='clarity',
                palette='RdYlGn', s=15, alpha=0.5,
                hue_order=clarity_order, ax=axes[0,1])
axes[0,1].set_title('Carat vs Price by Clarity', fontweight='bold')

sns.ecdfplot(data=sample, x='price', hue='cut', palette='YlOrRd',
             linewidth=2, hue_order=cut_order, ax=axes[1,0])
axes[1,0].set_title('Price ECDF by Cut', fontweight='bold')
axes[1,0].set_xlabel('Price ($)')

pivot = diamonds.groupby(['cut','color'])['price'].median().unstack()
pivot = pivot.loc[cut_order]
sns.heatmap(pivot, cmap='YlOrRd', annot=True, fmt='.0f',
            linewidths=0.3, ax=axes[1,1])
axes[1,1].set_title('Median Price: Cut × Color', fontweight='bold')

fig.suptitle('Diamond Price Analysis — Complete Story', fontweight='bold', fontsize=14)
fig.tight_layout()
fig.savefig('diamond_story.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved diamond_story.png')""",
    "Real Dataset EDA Practice",
    "Load the 'mpg' dataset. Create a 2x2 EDA dashboard: (1) lmplot of mpg vs weight by origin, (2) pairplot of [mpg, horsepower, weight] with hue=origin (quick version), (3) boxplot of mpg by cylinders, (4) lineplot of mean mpg by model_year. Drop NaN first.",
    HDR + """\
sns.set_theme(style='whitegrid')
mpg = sns.load_dataset('mpg').dropna()

# Pairplot separately (it creates its own figure)
g = sns.pairplot(mpg[['mpg','horsepower','weight','origin']],
                 hue='origin', palette='Set2', plot_kws=dict(s=15, alpha=0.5))
g.fig.suptitle('MPG Pairplot', y=1.01)
g.fig.savefig('mpg_pairplot.png', dpi=80, bbox_inches='tight')
plt.close(g.fig)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# TODO: boxplot mpg by cylinders
# TODO: lineplot mean mpg by model_year, hue=origin
# TODO: scatterplot weight vs mpg, hue=origin, regplot overlay
fig.tight_layout()
fig.savefig('mpg_dashboard.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved mpg_dashboard.png')"""
)

# ── Section 30: Object-Oriented Seaborn (Figure API) ─────────────────────────
s30 = make_sns(
    30, "Object-Oriented Seaborn",
    "Use the modern Seaborn Figure API: create a Figure object, add Subplots with share axes, and chain .plot() calls. Use Figure.save() and Figure.show(). Available in Seaborn 0.12+.",
    [
        {"label": "Seaborn objects API: basic scatter", "code": HDR + """\
import seaborn.objects as so
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

p = (
    so.Plot(tips, x='total_bill', y='tip', color='sex')
    .add(so.Dot(alpha=0.6, pointsize=5))
    .add(so.Line(), so.PolyFit(order=1))
    .label(x='Total Bill ($)', y='Tip ($)', color='Sex',
           title='Tips: Scatter + Regression (objects API)')
)
p.save('so_scatter.png', dpi=120, bbox_inches='tight')
print('Saved so_scatter.png')"""},
        {"label": "Seaborn objects: Bar plot with grouping", "code": HDR + """\
import seaborn.objects as so
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

p = (
    so.Plot(tips, x='day', y='total_bill', color='sex')
    .add(so.Bar(), so.Agg('mean'), so.Dodge())
    .label(x='Day', y='Mean Total Bill ($)', color='Sex',
           title='Mean Bill by Day & Sex (objects API)')
)
p.save('so_bar.png', dpi=120, bbox_inches='tight')
print('Saved so_bar.png')"""},
        {"label": "Seaborn objects: histogram with KDE", "code": HDR + """\
import seaborn.objects as so
sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')

p = (
    so.Plot(iris, x='petal_length', color='species')
    .add(so.Bars(), so.Hist(binwidth=0.3), so.Norm('percent'))
    .add(so.Line(), so.KDE())
    .label(x='Petal Length (cm)', y='Percent',
           title='Petal Length Distribution (objects API)')
)
p.save('so_hist.png', dpi=120, bbox_inches='tight')
print('Saved so_hist.png')"""},
        {"label": "Seaborn objects: faceted grid", "code": HDR + """\
import seaborn.objects as so
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

p = (
    so.Plot(tips, x='total_bill', y='tip', color='sex')
    .facet(col='time', row='smoker')
    .add(so.Dot(alpha=0.5, pointsize=4))
    .label(x='Total Bill ($)', y='Tip ($)',
           title='Tips: Faceted Grid (objects API)')
    .limit(x=(0, 55), y=(0, 11))
)
p.save('so_faceted.png', dpi=120, bbox_inches='tight')
print('Saved so_faceted.png')"""},
    ],
    "Modern API Visualization",
    "Use the seaborn.objects API to create a 3-part analysis of the 'penguins' dataset: (1) scatter bill_length vs bill_depth with color=species, (2) bar mean body_mass by species+sex with dodge, (3) line flipper_length trend — all using so.Plot.",
    HDR + """\
import seaborn.objects as so
sns.set_theme(style='whitegrid')
penguins = sns.load_dataset('penguins').dropna()

p1 = (
    so.Plot(penguins, x='bill_length_mm', y='bill_depth_mm', color='species')
    .add(so.Dot(alpha=0.6, pointsize=5))
    .label(x='Bill Length (mm)', y='Bill Depth (mm)',
           title='Bill Dimensions by Species')
)
p1.save('so_penguin_scatter.png', dpi=120, bbox_inches='tight')

p2 = (
    so.Plot(penguins, x='species', y='body_mass_g', color='sex')
    .add(so.Bar(), so.Agg('mean'), so.Dodge())
    .label(x='Species', y='Mean Body Mass (g)',
           title='Body Mass by Species & Sex')
)
p2.save('so_penguin_bar.png', dpi=120, bbox_inches='tight')
print('Saved so_penguin_scatter.png and so_penguin_bar.png')""",
    "Objects API Practice",
    "Using the seaborn objects API (so.Plot), recreate a regression scatter of tips total_bill vs tip, color by day, with a PolyFit(order=1) line. Facet by time (col='time'). Save as 'so_practice.png'.",
    HDR + """\
import seaborn.objects as so
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

# TODO: so.Plot with x=total_bill, y=tip, color=day
# TODO: .add(so.Dot) + .add(so.Line, so.PolyFit(order=1))
# TODO: .facet(col='time')
# TODO: .save('so_practice.png', dpi=120)"""
)

# ── Section 31: Color Systems & Accessibility ─────────────────────────────────
s31 = make_sns(
    31, "Color Systems & Accessibility",
    "Choose colorblind-safe palettes, use perceptually uniform colormaps, distinguish sequential vs. diverging vs. qualitative palettes, and apply Seaborn color_palette utilities.",
    [
        {"label": "Qualitative palettes for categorical data", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(0)
df = pd.DataFrame({
    'value': np.random.randn(200),
    'group': np.random.choice(list('ABCDE'), 200)
})

qual_palettes = ['Set1','Set2','Set3','tab10','colorblind','deep']
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
for ax, pal in zip(axes.flat, qual_palettes):
    sns.boxplot(data=df, x='group', y='value', palette=pal, ax=ax)
    ax.set_title(f'palette="{pal}"')
fig.suptitle('Qualitative Palettes Comparison', fontweight='bold', fontsize=13)
fig.tight_layout()
fig.savefig('qual_palettes.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved qual_palettes.png')"""},
        {"label": "Sequential palettes for ordered data", "code": HDR + """\
sns.set_theme(style='white')
np.random.seed(1)
x = y = np.linspace(-3, 3, 60)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

seq_palettes = ['Blues','YlOrRd','viridis','magma']
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, pal in zip(axes, seq_palettes):
    im = ax.pcolormesh(X, Y, Z, cmap=pal)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title(f'cmap="{pal}"')
    ax.set_aspect('equal')
fig.suptitle('Sequential Palettes for Heatmap Data', fontweight='bold')
fig.tight_layout()
fig.savefig('seq_palettes.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved seq_palettes.png')"""},
        {"label": "Diverging palettes for signed values", "code": HDR + """\
sns.set_theme(style='white')
np.random.seed(2)
data = np.random.randn(10, 8) * 2
df = pd.DataFrame(data,
    index=[f'Product {i}' for i in range(1,11)],
    columns=[f'Q{q}' for q in range(1,9)])

div_palettes = ['RdBu_r','RdYlGn','coolwarm','PiYG']
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, pal in zip(axes, div_palettes):
    sns.heatmap(df, cmap=pal, center=0, ax=ax,
                cbar_kws={'shrink':0.8}, xticklabels=True, yticklabels=False)
    ax.set_title(f'cmap="{pal}"')
fig.suptitle('Diverging Palettes for Change Data', fontweight='bold')
fig.tight_layout()
fig.savefig('div_palettes.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved div_palettes.png')"""},
        {"label": "Colorblind-safe vs non-safe comparison", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(3)
df = pd.DataFrame({
    'x': np.linspace(0, 10, 80),
    'A': np.sin(np.linspace(0, 10, 80)) + np.random.randn(80)*0.2,
    'B': np.cos(np.linspace(0, 10, 80)) + np.random.randn(80)*0.2,
    'C': np.sin(np.linspace(0, 10, 80)*1.5) + np.random.randn(80)*0.2,
})

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
# Non-safe: red-green confusion
colors_bad = ['#ff0000','#00aa00','#0000ff']
for col, c in zip(['A','B','C'], colors_bad):
    axes[0].plot(df.x, df[col], color=c, linewidth=2, label=col,
                 linestyle='-')
axes[0].set_title('Non-colorblind-safe (avoid red/green)')
axes[0].legend()

# Colorblind-safe (Wong palette) with markers
cb_colors = ['#0072B2','#D55E00','#009E73']
markers = ['o','s','^']
for col, c, m in zip(['A','B','C'], cb_colors, markers):
    axes[1].plot(df.x, df[col], color=c, linewidth=2,
                 label=col, marker=m, markevery=8, markersize=7)
axes[1].set_title('Colorblind-safe (Wong palette + markers)')
axes[1].legend()

for ax in axes:
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.grid(True, alpha=0.3)
fig.suptitle('Accessibility: Color Choice Matters', fontweight='bold')
fig.tight_layout()
fig.savefig('colorblind_safe.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved colorblind_safe.png')"""},
    ],
    "Accessible Dashboard Design",
    "Redesign a 4-panel report using only colorblind-safe palettes: use 'colorblind' for categorical, 'Blues' for sequential, 'RdBu_r' for diverging, and add hatch patterns or markers as secondary encodings.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(42)
df_cat = pd.DataFrame({
    'group': np.repeat(['A','B','C','D'],60),
    'value': np.concatenate([np.random.normal(m,1.2,60) for m in [3,5,4,6]])
})
df_seq = pd.DataFrame(np.random.rand(8,6)*100,
                       columns=[f'M{i}' for i in range(1,7)],
                       index=[f'R{i}' for i in range(1,9)])
df_div = pd.DataFrame(np.random.randn(6,5)*20,
                       columns=['Q1','Q2','Q3','Q4','Q5'],
                       index=[f'P{i}' for i in range(1,7)])

fig, axes = plt.subplots(2, 2, figsize=(13, 10))

# Categorical: colorblind + hatch
bars = sns.barplot(data=df_cat, x='group', y='value',
                   palette='colorblind', capsize=0.1, ax=axes[0,0])
hatches = ['','///','xxx','...']
for bar, hatch in zip(axes[0,0].patches, hatches*10):
    bar.set_hatch(hatch)
axes[0,0].set_title('Categorical: colorblind + hatch')

# Sequential heatmap
sns.heatmap(df_seq, cmap='Blues', annot=False, ax=axes[0,1],
            cbar_kws={'label':'Value'})
axes[0,1].set_title('Sequential: Blues')

# Diverging heatmap
sns.heatmap(df_div, cmap='RdBu_r', center=0, annot=True, fmt='.0f',
            linewidths=0.3, ax=axes[1,0])
axes[1,0].set_title('Diverging: RdBu_r')

# Line with markers
cb_colors = ['#0072B2','#D55E00','#009E73','#CC79A7']
x = np.arange(12)
for i,(col,m) in enumerate(zip(cb_colors,['o','s','^','D'])):
    y = np.cumsum(np.random.randn(12)*0.5) + i
    axes[1,1].plot(x, y, color=col, marker=m, linewidth=2,
                   markevery=3, markersize=7, label=f'Series {i+1}')
axes[1,1].legend(fontsize=8); axes[1,1].set_title('Lines: Wong palette + markers')
axes[1,1].grid(True, alpha=0.3)

fig.suptitle('Accessible Dashboard — Colorblind-Safe Design', fontweight='bold', fontsize=13)
fig.tight_layout()
fig.savefig('accessible_seaborn.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved accessible_seaborn.png')""",
    "Color Accessibility Practice",
    "Create a 4-group comparison plot (your choice of data). First plot with the red/green palette (unsafe). Then create a duplicate using the 'colorblind' palette with different markers per group. Save both as 'color_bad.png' and 'color_good.png'.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(6)
groups = ['Control','TreatmentA','TreatmentB','TreatmentC']
df = pd.DataFrame({
    'value': np.concatenate([np.random.normal(m,1.5,60) for m in [3,4.5,3.8,5.2]]),
    'group': np.repeat(groups,60)
})

# TODO: barplot with non-safe red/green palette, save 'color_bad.png'
# TODO: barplot with colorblind palette + stripplot with markers, save 'color_good.png'"""
)

# ── Section 32: Seaborn Dashboard Composition ─────────────────────────────────
s32 = make_sns(
    32, "Seaborn Dashboard Composition",
    "Combine multiple seaborn plot types, matplotlib GridSpec, annotation overlays, and consistent theming to produce publication-quality, multi-panel analytical dashboards.",
    [
        {"label": "4-panel EDA dashboard", "code": HDR + """\
from matplotlib.gridspec import GridSpec

sns.set_theme(style='whitegrid', palette='Set2', font_scale=0.95)
np.random.seed(42)
df = pd.DataFrame({
    'revenue': np.random.lognormal(5, 0.5, 300),
    'spend':   np.random.uniform(1000, 10000, 300),
    'channel': np.random.choice(['Search','Social','Email','Direct'], 300),
    'month':   np.random.choice(range(1,13), 300)
})
df['revenue'] = df['spend'] * np.random.uniform(0.1, 0.5, 300) + np.random.randn(300)*50

fig = plt.figure(figsize=(14, 9))
gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

ax1 = fig.add_subplot(gs[0, :2])
ax2 = fig.add_subplot(gs[0, 2])
ax3 = fig.add_subplot(gs[1, :])

sns.scatterplot(data=df, x='spend', y='revenue', hue='channel',
                style='channel', s=50, alpha=0.6, ax=ax1)
ax1.set_title('Revenue vs Spend by Channel', fontweight='bold')

sns.violinplot(data=df, x='channel', y='revenue', palette='Set2',
               inner='quartile', ax=ax2)
ax2.set_title('Revenue Distribution', fontweight='bold')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=20, ha='right', fontsize=8)

month_agg = df.groupby(['month','channel'])['revenue'].mean().reset_index()
sns.lineplot(data=month_agg, x='month', y='revenue', hue='channel',
             palette='Set2', linewidth=2, markers=True, ax=ax3)
ax3.set_title('Monthly Average Revenue by Channel', fontweight='bold')
ax3.set_xlabel('Month')

fig.suptitle('Marketing Revenue Dashboard', fontsize=14, fontweight='bold')
fig.savefig('sns_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved sns_dashboard.png')"""},
        {"label": "Statistical report: hypothesis testing visual", "code": HDR + """\
from scipy import stats

sns.set_theme(style='whitegrid')
np.random.seed(1)
control    = np.random.normal(70, 12, 100)
treatment  = np.random.normal(75, 11, 100)
t_stat, p_val = stats.ttest_ind(control, treatment)
effect_size = (treatment.mean() - control.mean()) / np.sqrt(
    ((len(control)-1)*control.std()**2 + (len(treatment)-1)*treatment.std()**2) /
    (len(control)+len(treatment)-2))

df = pd.DataFrame({
    'score': np.concatenate([control, treatment]),
    'group': np.repeat(['Control','Treatment'], 100)
})

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
sns.histplot(data=df, x='score', hue='group', kde=True, alpha=0.4,
             palette='Set1', stat='density', common_norm=False, ax=axes[0])
axes[0].set_title('Score Distributions')

sns.violinplot(data=df, x='group', y='score', palette='Set1',
               inner='box', ax=axes[1])
axes[1].set_title('Violin Comparison')

sns.ecdfplot(data=df, x='score', hue='group', palette='Set1',
             linewidth=2, ax=axes[2])
axes[2].set_title('ECDF Comparison')

for ax in axes:
    ax.set_xlabel('Score')

fig.suptitle(f'A/B Test: t={t_stat:.2f}, p={p_val:.4f}, d={effect_size:.2f}',
             fontsize=13, fontweight='bold')
fig.tight_layout()
fig.savefig('hypothesis_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved hypothesis_dashboard.png')"""},
        {"label": "Full EDA report: penguins deep dive", "code": HDR + """\
from matplotlib.gridspec import GridSpec

sns.set_theme(style='whitegrid', palette='colorblind')
penguins = sns.load_dataset('penguins').dropna()

fig = plt.figure(figsize=(15, 10), facecolor='white')
gs = GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.4)

# Banner
ax0 = fig.add_subplot(gs[0, :])
ax0.text(0.5, 0.6, 'Palmer Penguins — Deep Dive EDA',
         ha='center', va='center', fontsize=16, fontweight='bold',
         transform=ax0.transAxes)
ax0.text(0.5, 0.1, f'n={len(penguins)} penguins | 3 species | 3 islands',
         ha='center', va='center', fontsize=11, color='gray',
         transform=ax0.transAxes)
ax0.axis('off')

# Scatter bill dimensions
ax1 = fig.add_subplot(gs[1, :2])
sns.scatterplot(data=penguins, x='bill_length_mm', y='bill_depth_mm',
                hue='species', style='island', s=60, alpha=0.7, ax=ax1)
ax1.set_title('Bill Dimensions by Species & Island', fontweight='bold')

# Count by species
ax2 = fig.add_subplot(gs[1, 2])
sns.countplot(data=penguins, x='species', hue='sex',
              palette='Set2', ax=ax2)
ax2.set_title('Counts by Species & Sex', fontweight='bold')
ax2.set_xlabel('Species')

# Body mass violin
ax3 = fig.add_subplot(gs[2, :2])
sns.violinplot(data=penguins, x='species', y='body_mass_g',
               hue='sex', split=True, palette='pastel', inner='box', ax=ax3)
ax3.set_title('Body Mass Distribution', fontweight='bold')

# Flipper ECDF
ax4 = fig.add_subplot(gs[2, 2])
sns.ecdfplot(data=penguins, x='flipper_length_mm', hue='species',
             palette='colorblind', linewidth=2, ax=ax4)
ax4.set_title('Flipper Length ECDF', fontweight='bold')
ax4.set_xlabel('Flipper Length (mm)')

fig.savefig('penguins_deep_dive.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print('Saved penguins_deep_dive.png')"""},
        {"label": "Time series analytics dashboard", "code": HDR + """\
from matplotlib.gridspec import GridSpec

sns.set_theme(style='darkgrid', palette='Set2')
np.random.seed(77)
n_days = 90
dates = pd.date_range('2024-01-01', periods=n_days)
products = ['Widget','Gadget','Doohickey']
rows = []
for prod in products:
    base = np.random.uniform(80, 150)
    trend = np.cumsum(np.random.randn(n_days)*2) + base
    for d, v in zip(dates, trend):
        rows.append({'date':d,'product':prod,'sales':max(0,v),
                     'returns':max(0,v*0.05+np.random.randn())})
df = pd.DataFrame(rows)
df['month'] = df['date'].dt.month

fig = plt.figure(figsize=(14, 9))
gs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

ax1 = fig.add_subplot(gs[0, :])
sns.lineplot(data=df, x='date', y='sales', hue='product',
             palette='Set2', linewidth=2, ax=ax1)
ax1.set_title('Daily Sales Trend by Product', fontweight='bold')
ax1.set_xlabel('Date'); ax1.set_ylabel('Sales ($)')

ax2 = fig.add_subplot(gs[1, 0])
month_df = df.groupby(['month','product'])['sales'].mean().reset_index()
sns.barplot(data=month_df, x='month', y='sales', hue='product',
            palette='Set2', ax=ax2)
ax2.set_title('Mean Monthly Sales', fontweight='bold')
ax2.set_xlabel('Month')

ax3 = fig.add_subplot(gs[1, 1])
sns.scatterplot(data=df, x='sales', y='returns', hue='product',
                palette='Set2', s=20, alpha=0.4, ax=ax3)
# Add regression per product
for prod, grp in df.groupby('product'):
    m,b = np.polyfit(grp.sales, grp.returns, 1)
    x_l = np.linspace(grp.sales.min(), grp.sales.max(), 50)
    ax3.plot(x_l, m*x_l+b, linewidth=1.5, alpha=0.8)
ax3.set_title('Sales vs Returns', fontweight='bold')

fig.suptitle('Product Analytics Dashboard', fontsize=14, fontweight='bold')
fig.savefig('time_series_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved time_series_dashboard.png')"""},
    ],
    "Comprehensive Analysis Report",
    "Design a 5-panel Seaborn+GridSpec report on the 'diamonds' dataset: (1) banner with dataset stats, (2) price by cut violin, (3) carat vs price scatter by clarity, (4) price ECDF by cut, (5) heatmap of counts cut×color.",
    HDR + """\
from matplotlib.gridspec import GridSpec

sns.set_theme(style='whitegrid', palette='Set2')
diamonds = sns.load_dataset('diamonds')
sample = diamonds.sample(2000, random_state=42)
cut_order = ['Fair','Good','Very Good','Premium','Ideal']

fig = plt.figure(figsize=(14, 11), facecolor='white')
gs = GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.4)

# Banner
ax0 = fig.add_subplot(gs[0, :])
ax0.text(0.5, 0.6, 'Diamonds Dataset — Comprehensive Report',
         ha='center', fontsize=15, fontweight='bold', transform=ax0.transAxes)
ax0.text(0.5, 0.1, f'{len(diamonds):,} diamonds | {diamonds.cut.nunique()} cuts | '
                   f'Price: ${diamonds.price.min():,}–${diamonds.price.max():,}',
         ha='center', fontsize=10, color='gray', transform=ax0.transAxes)
ax0.axis('off')

ax1 = fig.add_subplot(gs[1, :2])
sns.violinplot(data=sample, x='cut', y='price', palette='YlOrRd',
               inner='quartile', order=cut_order, ax=ax1)
ax1.set_title('Price by Cut', fontweight='bold')

ax2 = fig.add_subplot(gs[1, 2])
clarity_order = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
sns.scatterplot(data=sample, x='carat', y='price', hue='clarity',
                palette='RdYlGn', s=10, alpha=0.4,
                hue_order=clarity_order, ax=ax2, legend=False)
ax2.set_title('Carat vs Price', fontweight='bold')

ax3 = fig.add_subplot(gs[2, :2])
sns.ecdfplot(data=sample, x='price', hue='cut', palette='YlOrRd',
             linewidth=2, hue_order=cut_order, ax=ax3)
ax3.set_title('Price ECDF by Cut', fontweight='bold')

ax4 = fig.add_subplot(gs[2, 2])
counts = diamonds.groupby(['cut','color']).size().unstack().loc[cut_order]
sns.heatmap(counts, cmap='Blues', annot=True, fmt='d',
            linewidths=0.3, ax=ax4, cbar=False)
ax4.set_title('Count: Cut × Color', fontweight='bold')

fig.suptitle('Diamond Market Analysis', fontsize=15, fontweight='bold', y=1.01)
fig.savefig('diamonds_report.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print('Saved diamonds_report.png')""",
    "Dashboard Practice",
    "Build your own 4-panel seaborn dashboard using any dataset you prefer (tips, penguins, titanic, mpg, etc.). Requirements: (1) GridSpec layout with at least one spanning panel, (2) 4 different plot types, (3) consistent palette and theme, (4) suptitle banner, (5) save at 150 DPI.",
    HDR + """\
from matplotlib.gridspec import GridSpec

sns.set_theme(style='whitegrid', palette='Set2')
# Choose your dataset
tips = sns.load_dataset('tips')

fig = plt.figure(figsize=(13, 9))
gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

# TODO: Panel 1 — spanning top row (gs[0, :])
# TODO: Panel 2 — bottom-left (gs[1, :2])
# TODO: Panel 3 — bottom-right (gs[1, 2])
# Pick 4 different plot types across panels
# TODO: suptitle banner
# TODO: save 'my_sns_dashboard.png' at 150 DPI
plt.close()
print('Dashboard saved!')"""
)


# ── Assemble and insert ───────────────────────────────────────────────────────
all_sections = s25 + s26 + s27 + s28 + s29 + s30 + s31 + s32
result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: seaborn sections 25-32 added")
else:
    print("FAILED")
