"""Add Seaborn sections 17-24 to gen_seaborn.py"""
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

# ── Section 17: Strip Plot & Swarm Plot ───────────────────────────────────────
s17 = make_sns(
    17, "Strip Plot & Swarm Plot",
    "Use stripplot() to show individual data points by category and swarmplot() to avoid overplotting by spacing points. Layer them over box or violin plots for richer displays.",
    [
        {"label": "Basic strip and swarm comparison", "code": HDR + """\
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
sns.stripplot(data=tips, x='day', y='total_bill', ax=ax1,
              palette='Set2', jitter=True, alpha=0.7, size=5)
ax1.set_title('Strip Plot (jitter)')

sns.swarmplot(data=tips, x='day', y='total_bill', ax=ax2,
              palette='Set2', size=4)
ax2.set_title('Swarm Plot (no overlap)')

for ax in (ax1, ax2):
    ax.set_xlabel('Day'); ax.set_ylabel('Total Bill ($)')
fig.tight_layout()
fig.savefig('strip_swarm.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved strip_swarm.png')"""},
        {"label": "Strip plot layered over box plot", "code": HDR + """\
sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=iris, x='species', y='sepal_length', ax=ax,
            palette='pastel', width=0.5,
            boxprops=dict(alpha=0.6))
sns.stripplot(data=iris, x='species', y='sepal_length', ax=ax,
              palette='Set2', size=5, jitter=True, alpha=0.7,
              linewidth=0.5, edgecolor='gray')
ax.set_title('Box + Strip Plot Overlay')
ax.set_xlabel('Species'); ax.set_ylabel('Sepal Length (cm)')
fig.tight_layout()
fig.savefig('box_strip.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved box_strip.png')"""},
        {"label": "Swarm layered over violin", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(0)
df = pd.DataFrame({
    'score': np.concatenate([np.random.normal(m, 1, 60) for m in [5, 6.5, 8]]),
    'group': np.repeat(['Control', 'Low Dose', 'High Dose'], 60)
})

fig, ax = plt.subplots(figsize=(8, 5))
sns.violinplot(data=df, x='group', y='score', ax=ax,
               palette='muted', inner=None, alpha=0.6)
sns.swarmplot(data=df, x='group', y='score', ax=ax,
              color='black', size=3, alpha=0.6)
ax.set_title('Violin + Swarm: Treatment Groups')
ax.set_xlabel('Group'); ax.set_ylabel('Score')
fig.tight_layout()
fig.savefig('violin_swarm.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved violin_swarm.png')"""},
        {"label": "Strip plot with hue and dodge", "code": HDR + """\
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, ax = plt.subplots(figsize=(9, 5))
sns.stripplot(data=tips, x='day', y='total_bill', hue='sex',
              dodge=True, jitter=True, alpha=0.7, size=5,
              palette='Set1', ax=ax)
ax.set_title('Strip Plot: Tip Amount by Day and Sex (Dodged)')
ax.set_xlabel('Day'); ax.set_ylabel('Total Bill ($)')
ax.legend(title='Sex', bbox_to_anchor=(1, 1))
fig.tight_layout()
fig.savefig('strip_hue.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved strip_hue.png')"""},
    ],
    "Employee Salary Audit",
    "HR needs to show individual salaries by department and gender on top of a violin plot to reveal outliers and within-group spread. Use dodge=True so genders are side by side.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(7)
depts = ['Eng', 'Sales', 'Mktg', 'HR']
df = pd.DataFrame({
    'salary': np.concatenate([
        np.random.normal(m, s, 60)
        for m, s in [(95,15),(70,12),(75,13),(65,10)] for _ in range(1)
    ] * 2),
    'dept': np.tile(np.repeat(depts, 60), 2),
    'gender': np.repeat(['Female','Male'], 240)
})

fig, ax = plt.subplots(figsize=(11, 6))
sns.violinplot(data=df, x='dept', y='salary', hue='gender',
               split=True, inner=None, palette='pastel', alpha=0.6, ax=ax)
sns.stripplot(data=df, x='dept', y='salary', hue='gender',
              dodge=True, jitter=True, alpha=0.5, size=3,
              palette='dark:#333333', ax=ax, legend=False)
ax.set_title('Salary Distribution by Department & Gender', fontweight='bold')
ax.set_xlabel('Department'); ax.set_ylabel('Salary ($K)')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[:2], labels[:2], title='Gender')
fig.tight_layout()
fig.savefig('salary_audit.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved salary_audit.png')""",
    "Strip/Swarm Practice",
    "Load the 'penguins' dataset. Create a 1x2 subplot: (1) swarmplot of body_mass_g by species with hue=sex, (2) stripplot of flipper_length_mm by island with box overlay. Use palette='colorblind' and whitegrid style.",
    HDR + """\
sns.set_theme(style='whitegrid')
penguins = sns.load_dataset('penguins').dropna()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
# TODO: swarmplot body_mass_g by species, hue=sex
# TODO: boxplot + stripplot flipper_length_mm by island
# TODO: colorblind palette, titles, labels
fig.tight_layout()
fig.savefig('penguin_points.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved penguin_points.png')"""
)

# ── Section 18: Point Plot & Statistical Line Plots ───────────────────────────
s18 = make_sns(
    18, "Point Plot & Statistical Line Plots",
    "Use pointplot() to display means with confidence intervals for categorical variables. Use lineplot() with hue for multi-group time series with automatic CI shading.",
    [
        {"label": "pointplot: means with CI by category", "code": HDR + """\
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
sns.pointplot(data=tips, x='day', y='total_bill', ax=ax1,
              palette='Set2', capsize=0.1, errwidth=2,
              markers='o', linestyles='-')
ax1.set_title('Point Plot: Mean Bill by Day')

sns.pointplot(data=tips, x='day', y='total_bill', hue='sex',
              ax=ax2, palette='Set1', dodge=True,
              capsize=0.08, errwidth=1.5)
ax2.set_title('Point Plot: By Day and Sex')

for ax in (ax1, ax2):
    ax.set_xlabel('Day'); ax.set_ylabel('Mean Total Bill ($)')
fig.tight_layout()
fig.savefig('pointplot.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved pointplot.png')"""},
        {"label": "lineplot with confidence interval shading", "code": HDR + """\
sns.set_theme(style='darkgrid')
np.random.seed(0)
n = 50
df = pd.DataFrame({
    't': np.tile(np.arange(n), 3),
    'value': np.concatenate([
        np.cumsum(np.random.randn(n)) + 5,
        np.cumsum(np.random.randn(n)) + 3,
        np.cumsum(np.random.randn(n)) + 7,
    ]),
    'model': np.repeat(['Model A', 'Model B', 'Model C'], n)
})

# Add repeated measurements for CI
df_rep = pd.concat([df.assign(value=df.value + np.random.randn(len(df))*0.5)
                    for _ in range(5)], ignore_index=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df_rep, x='t', y='value', hue='model',
             palette='Set2', linewidth=2, ax=ax)
ax.set_title('lineplot with 95% CI Shading')
ax.set_xlabel('Time Step'); ax.set_ylabel('Value')
fig.tight_layout()
fig.savefig('lineplot_ci.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved lineplot_ci.png')"""},
        {"label": "lineplot with markers and styles", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(1)
months = list(range(1, 13))
df = pd.DataFrame({
    'month': months * 3,
    'revenue': (
        [100 + i*8 + np.random.randn()*5 for i in range(12)] +
        [80 + i*6 + np.random.randn()*4 for i in range(12)] +
        [60 + i*10 + np.random.randn()*6 for i in range(12)]
    ),
    'region': ['North']*12 + ['South']*12 + ['East']*12
})

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df, x='month', y='revenue', hue='region',
             style='region', markers=True, dashes=False,
             palette='Set1', linewidth=2, ax=ax)
ax.set_title('Monthly Revenue by Region')
ax.set_xlabel('Month'); ax.set_ylabel('Revenue ($K)')
ax.legend(title='Region')
fig.tight_layout()
fig.savefig('lineplot_markers.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved lineplot_markers.png')"""},
        {"label": "pointplot vs barplot comparison", "code": HDR + """\
sns.set_theme(style='whitegrid')
titanic = sns.load_dataset('titanic')

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
# Bar: shows aggregated height
sns.barplot(data=titanic, x='class', y='survived', hue='sex',
            palette='Set2', ax=axes[0])
axes[0].set_title('barplot: Mean Survival Rate')

# Point: cleaner for comparison
sns.pointplot(data=titanic, x='class', y='survived', hue='sex',
              palette='Set1', dodge=True, capsize=0.1, ax=axes[1])
axes[1].set_title('pointplot: Same Data')

# Count the actual survivors
surv = titanic.groupby(['class','sex'])['survived'].mean().reset_index()
sns.pointplot(data=surv, x='class', y='survived', hue='sex',
              palette='Set1', dodge=True, capsize=0.1, ax=axes[2],
              markers=['o', 's'], linestyles=['-','--'])
axes[2].set_title('pointplot: Precomputed')

for ax in axes:
    ax.set_ylim(0, 1); ax.set_ylabel('Survival Rate')
fig.tight_layout()
fig.savefig('point_vs_bar.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved point_vs_bar.png')"""},
    ],
    "Student Performance Tracking",
    "Plot mean exam scores with 95% CI for 4 subjects across 3 school terms. Use pointplot with dodge for gender comparison and a lineplot showing term-over-term trend with shaded uncertainty.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(42)
subjects = ['Math', 'Science', 'English', 'History']
terms = ['T1', 'T2', 'T3']
rows = []
for subj in subjects:
    base = np.random.uniform(60, 85)
    for term in terms:
        for gender in ['Female', 'Male']:
            n = 30
            offset = {'T1': 0, 'T2': 3, 'T3': 6}[term]
            g_offset = 2 if gender == 'Female' else 0
            scores = np.random.normal(base + offset + g_offset, 8, n)
            for s in scores:
                rows.append({'subject': subj, 'term': term, 'gender': gender, 'score': s})
df = pd.DataFrame(rows)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
sns.pointplot(data=df, x='subject', y='score', hue='gender',
              dodge=True, capsize=0.08, palette='Set1',
              markers=['o','s'], linestyles=['-','--'], ax=ax1)
ax1.set_title('Mean Score by Subject & Gender', fontweight='bold')
ax1.set_xlabel('Subject'); ax1.set_ylabel('Mean Score')

term_df = df.groupby(['term','subject']).score.mean().reset_index()
sns.lineplot(data=df, x='term', y='score', hue='subject',
             palette='tab10', linewidth=2, markers=True, ax=ax2)
ax2.set_title('Score Trend by Term', fontweight='bold')
ax2.set_xlabel('Term'); ax2.set_ylabel('Score')
ax2.legend(title='Subject', bbox_to_anchor=(1,1))
fig.tight_layout()
fig.savefig('student_performance.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved student_performance.png')""",
    "Point/Line Plot Practice",
    "Load the 'fmri' dataset from seaborn. Plot a lineplot of signal by timepoint, with hue=event and style=region. Add a pointplot below it showing mean signal per region. Use a 2x1 subplot with shared x-axis.",
    HDR + """\
sns.set_theme(style='darkgrid')
fmri = sns.load_dataset('fmri')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=False)
# TODO: lineplot signal by timepoint, hue=event, style=region
# TODO: pointplot mean signal by region with capsize
# TODO: titles, labels, tight_layout
fig.savefig('fmri_plots.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved fmri_plots.png')"""
)

# ── Section 19: ECDF & Distribution Comparison ────────────────────────────────
s19 = make_sns(
    19, "ECDF & Distribution Comparison",
    "Use ecdfplot() for empirical CDFs, histplot() with multiple groups, and kdeplot() to compare distributions across categories without assuming a parametric form.",
    [
        {"label": "ECDF plot for group comparison", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(0)
df = pd.DataFrame({
    'value': np.concatenate([
        np.random.normal(5, 1.5, 200),
        np.random.normal(7, 1.0, 200),
        np.random.exponential(2, 200) + 3,
    ]),
    'group': np.repeat(['Normal(5,1.5)', 'Normal(7,1)', 'Exp+3'], 200)
})

fig, ax = plt.subplots(figsize=(9, 5))
sns.ecdfplot(data=df, x='value', hue='group', palette='Set2', linewidth=2)
ax.axhline(0.5, color='gray', linestyle='--', linewidth=1, label='Median')
ax.set_title('ECDF: Distribution Comparison')
ax.set_xlabel('Value'); ax.set_ylabel('Cumulative Proportion')
ax.legend(title='Group')
fig.tight_layout()
fig.savefig('ecdf.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved ecdf.png')"""},
        {"label": "Overlapping KDE comparison", "code": HDR + """\
sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# Separate feature distributions per species
for feat, ax in zip(['sepal_length', 'petal_length'], axes):
    sns.kdeplot(data=iris, x=feat, hue='species',
                fill=True, alpha=0.35, linewidth=2, palette='Set2', ax=ax)
    ax.set_title(f'KDE: {feat.replace("_"," ").title()}')
    ax.set_xlabel(feat.replace('_',' ').title())
fig.tight_layout()
fig.savefig('kde_compare.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved kde_compare.png')"""},
        {"label": "histplot with stat='density' and kde overlay", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(1)
df = pd.DataFrame({
    'response_ms': np.concatenate([
        np.random.lognormal(5, 0.5, 300),
        np.random.lognormal(5.5, 0.4, 200),
    ]),
    'endpoint': np.repeat(['/api/search', '/api/checkout'], [300, 200])
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
sns.histplot(data=df, x='response_ms', hue='endpoint',
             stat='density', kde=True, alpha=0.4, palette='Set1',
             common_norm=False, ax=ax1)
ax1.set_title('Histogram with KDE — Linear scale')
ax1.set_xlabel('Response Time (ms)')

sns.histplot(data=df, x='response_ms', hue='endpoint',
             stat='density', kde=True, alpha=0.4, palette='Set1',
             common_norm=False, log_scale=True, ax=ax2)
ax2.set_title('Histogram with KDE — Log scale')
ax2.set_xlabel('Response Time (ms)')
fig.tight_layout()
fig.savefig('hist_kde_compare.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved hist_kde_compare.png')"""},
        {"label": "ECDF with percentile markers", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(2)
data = pd.DataFrame({
    'latency_ms': np.random.lognormal(5, 0.7, 1000),
    'server': np.random.choice(['US-East', 'EU-West', 'AP-South'], 1000)
})

fig, ax = plt.subplots(figsize=(9, 5))
sns.ecdfplot(data=data, x='latency_ms', hue='server',
             palette='tab10', linewidth=2, ax=ax)

# Mark p50, p95, p99
for pct, label, color in [(50,'p50','gray'),(95,'p95','orange'),(99,'p99','red')]:
    val = np.percentile(data['latency_ms'], pct)
    ax.axvline(val, color=color, linestyle='--', linewidth=1.2, alpha=0.8)
    ax.axhline(pct/100, color=color, linestyle=':', linewidth=0.8, alpha=0.5)
    ax.text(val+50, pct/100-0.04, f'{label}: {val:.0f}ms',
            fontsize=8, color=color)

ax.set_title('API Latency ECDF by Server Region')
ax.set_xlabel('Latency (ms)'); ax.set_ylabel('Cumulative Proportion')
fig.tight_layout()
fig.savefig('ecdf_percentiles.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved ecdf_percentiles.png')"""},
    ],
    "A/B Test Distribution Analysis",
    "Compare three e-commerce funnel variants: show ECDF of conversion values, overlapping KDE of order sizes, and a combined histplot with p50/p90 markers for each variant.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(99)
variants = {'Control': (45, 12), 'Variant A': (52, 14), 'Variant B': (48, 10)}
dfs = [pd.DataFrame({'order_value': np.random.normal(mu, sd, 300).clip(5), 'variant': name})
       for name, (mu, sd) in variants.items()]
df = pd.concat(dfs, ignore_index=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
sns.ecdfplot(data=df, x='order_value', hue='variant',
             palette='Set1', linewidth=2, ax=ax1)
for pct, ls in [(50,'--'),(90,':')]:
    ax1.axhline(pct/100, color='gray', linestyle=ls, linewidth=1)
    ax1.text(ax1.get_xlim()[0]+1, pct/100+0.01, f'p{pct}', fontsize=8, color='gray')
ax1.set_title('ECDF of Order Value by Variant', fontweight='bold')
ax1.set_xlabel('Order Value ($)')

sns.kdeplot(data=df, x='order_value', hue='variant',
            fill=True, alpha=0.3, linewidth=2, palette='Set1',
            common_norm=False, ax=ax2)
ax2.set_title('KDE: Order Value Distribution', fontweight='bold')
ax2.set_xlabel('Order Value ($)')
fig.tight_layout()
fig.savefig('ab_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved ab_distribution.png')""",
    "Distribution Comparison Practice",
    "Load the 'titanic' dataset. Create a 1x3 figure: (1) ecdfplot of 'fare' by 'class', (2) kdeplot of 'age' by 'survived' (use hue), (3) histplot of 'fare' with log_scale=True, hue='class'. Drop NaN rows first.",
    HDR + """\
sns.set_theme(style='whitegrid')
titanic = sns.load_dataset('titanic').dropna(subset=['age','fare'])

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# TODO: ecdfplot fare by class
# TODO: kdeplot age by survived
# TODO: histplot fare log scale by class
fig.tight_layout()
fig.savefig('titanic_dist.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved titanic_dist.png')"""
)

# ── Section 20: Cluster Map ────────────────────────────────────────────────────
s20 = make_sns(
    20, "Cluster Map",
    "Use clustermap() to apply hierarchical clustering to rows and columns of a matrix, revealing natural groupings in correlation matrices, gene expression, or feature similarity data.",
    [
        {"label": "Basic clustermap on iris correlation", "code": HDR + """\
sns.set_theme(style='white')
iris = sns.load_dataset('iris')
corr = iris.drop('species', axis=1).corr()

g = sns.clustermap(corr, cmap='RdBu_r', vmin=-1, vmax=1,
                   annot=True, fmt='.2f', figsize=(7, 7),
                   linewidths=0.5)
g.ax_heatmap.set_title('Iris Feature Correlation Clustermap', pad=50)
plt.savefig('clustermap_iris.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved clustermap_iris.png')"""},
        {"label": "Clustermap with row/col color bars", "code": HDR + """\
sns.set_theme(style='white')
np.random.seed(0)
n_genes, n_samples = 20, 12
groups = ['A','A','A','A','B','B','B','B','C','C','C','C']
data = pd.DataFrame(
    np.random.randn(n_genes, n_samples) +
    np.array([np.sin(np.linspace(0,3,n_samples))*(i%3-1) for i in range(n_genes)]),
    index=[f'Gene_{i:02d}' for i in range(n_genes)],
    columns=[f'S{i+1:02d}' for i in range(n_samples)]
)
palette = {'A':'#4c72b0', 'B':'#dd8452', 'C':'#55a868'}
col_colors = pd.Series(groups, index=data.columns).map(palette)

g = sns.clustermap(data, cmap='vlag', figsize=(10, 8),
                   col_colors=col_colors,
                   row_cluster=True, col_cluster=True,
                   z_score=0, linewidths=0.3)
g.ax_heatmap.set_title('Gene Expression Clustermap', pad=50)
plt.savefig('clustermap_genes.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved clustermap_genes.png')"""},
        {"label": "Clustermap with standard_scale", "code": HDR + """\
sns.set_theme(style='white')
np.random.seed(1)
features = ['Revenue', 'Growth', 'Margin', 'CAC', 'LTV', 'Churn']
companies = [f'Co{i:02d}' for i in range(1, 16)]
data = pd.DataFrame(
    np.random.randn(len(companies), len(features)),
    index=companies, columns=features
)
# Add cluster structure
data.iloc[:5, :3] += 2
data.iloc[5:10, 3:] -= 2
data.iloc[10:, [0,2,4]] += 1.5

g = sns.clustermap(data, cmap='coolwarm', figsize=(8, 10),
                   standard_scale=1,  # standardize each column
                   linewidths=0.4, annot=False,
                   dendrogram_ratio=(0.15, 0.2))
g.ax_heatmap.set_title('Company KPI Clustermap\n(column-standardized)', pad=50)
plt.savefig('clustermap_kpi.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved clustermap_kpi.png')"""},
        {"label": "Clustermap method and metric options", "code": HDR + """\
sns.set_theme(style='white')
np.random.seed(2)
data = pd.DataFrame(
    np.random.randn(15, 10),
    index=[f'R{i}' for i in range(15)],
    columns=[f'C{j}' for j in range(10)]
)
data.iloc[:5, :4] += 2.5
data.iloc[10:, 6:] += 2.5

fig, axes_list = plt.subplots(1, 2, figsize=(14, 6))
for ax, (method, metric) in zip(axes_list, [('ward','euclidean'),('average','correlation')]):
    g = sns.clustermap(data, cmap='RdYlBu_r', figsize=(6, 5),
                       method=method, metric=metric,
                       linewidths=0.3)
    g.fig.suptitle(f'method={method}, metric={metric}', y=1.01, fontsize=10)
    g.fig.savefig(f'clustermap_{method}.png', dpi=100, bbox_inches='tight')
    plt.close(g.fig)
print('Saved clustermap_ward.png and clustermap_average.png')"""},
    ],
    "Customer Segment Heatmap",
    "Build a clustermap of customer segments vs. behavioral features (purchase frequency, avg order, recency, CLV, support tickets). Use z_score=0, vlag colormap, and annotate row colors by segment.",
    HDR + """\
sns.set_theme(style='white')
np.random.seed(55)
segments = ['Loyal','At-Risk','New','Churned','VIP']
features = ['Frequency','Avg Order','Recency','CLV','Tickets']
n_each = 15
rows = []
centroids = {
    'Loyal':   [8, 120, 5, 960, 1],
    'At-Risk': [2, 80, 45, 160, 4],
    'New':     [1, 95, 15, 95, 0],
    'Churned': [0, 60, 120, 0, 6],
    'VIP':     [12, 400, 3, 4800, 2],
}
for seg, center in centroids.items():
    noise = np.random.randn(n_each, len(features)) * np.array([1, 20, 10, 200, 1])
    block = np.array(center) + noise
    df_seg = pd.DataFrame(block, columns=features)
    df_seg['segment'] = seg
    rows.append(df_seg)
df = pd.concat(rows, ignore_index=True)
matrix = df[features].values
row_labels = df['segment']
palette_seg = {'Loyal':'#55a868','At-Risk':'#dd8452','New':'#4c72b0',
               'Churned':'#c44e52','VIP':'#9467bd'}
row_colors = row_labels.map(palette_seg)

data_df = pd.DataFrame(matrix, columns=features,
                        index=[f'{seg}_{i}' for seg, n in [(s, n_each) for s in segments]
                               for i in range(n_each)])
g = sns.clustermap(pd.DataFrame(matrix, columns=features),
                   cmap='vlag', z_score=0, figsize=(9, 11),
                   row_colors=row_colors.values,
                   linewidths=0.2, dendrogram_ratio=(0.2, 0.15))
g.ax_heatmap.set_title('Customer Segment Behavioral Clustermap', pad=50, fontsize=12)
plt.savefig('customer_clustermap.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved customer_clustermap.png')""",
    "Clustermap Practice",
    "Generate a 12x8 random matrix with 3 obvious block clusters (add +2 to block (0:4, 0:3), +(-2) to block (4:8, 3:6)). Plot a clustermap with method='ward', cmap='RdBu_r', and z_score=0. Annotate the values with fmt='.1f'.",
    HDR + """\
sns.set_theme(style='white')
np.random.seed(3)
data = np.random.randn(12, 8)
data[:4, :3] += 2.5
data[4:8, 3:6] -= 2.5
data[8:, 5:] += 1.5
df = pd.DataFrame(data,
                  index=[f'R{i}' for i in range(12)],
                  columns=[f'C{j}' for j in range(8)])
# TODO: clustermap method='ward', cmap='RdBu_r', z_score=0, annot=True
# TODO: save 'block_clustermap.png'"""
)

# ── Section 21: Joint Plot Advanced ───────────────────────────────────────────
s21 = make_sns(
    21, "Joint Plot Advanced",
    "Use jointplot() to show the bivariate relationship alongside marginal univariate distributions. Explore kind='hex', 'kde', 'reg', and custom marginal plots with JointGrid.",
    [
        {"label": "jointplot: hex, kde, reg, scatter kinds", "code": HDR + """\
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

kinds = ['scatter', 'hex', 'kde', 'reg']
for kind in kinds:
    g = sns.jointplot(data=tips, x='total_bill', y='tip',
                      kind=kind, palette='Set2', height=5,
                      marginal_kws=dict(bins=25))
    g.fig.suptitle(f"kind='{kind}'", y=1.02)
    g.fig.savefig(f'joint_{kind}.png', dpi=100, bbox_inches='tight')
    plt.close(g.fig)
print('Saved joint_scatter/hex/kde/reg.png')"""},
        {"label": "jointplot with hue", "code": HDR + """\
sns.set_theme(style='whitegrid')
iris = sns.load_dataset('iris')

g = sns.jointplot(data=iris, x='sepal_length', y='petal_length',
                  hue='species', palette='Set2',
                  height=6, marginal_kws=dict(fill=True, alpha=0.4))
g.fig.suptitle('Iris: Sepal vs Petal Length (hue=species)', y=1.02)
g.fig.savefig('joint_hue.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved joint_hue.png')"""},
        {"label": "JointGrid: custom marginals", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(42)
df = pd.DataFrame({
    'x': np.random.lognormal(2, 0.5, 300),
    'y': np.random.lognormal(1.5, 0.6, 300)
})

g = sns.JointGrid(data=df, x='x', y='y', height=6)
g.plot_joint(sns.scatterplot, alpha=0.4, color='steelblue', s=25)
g.plot_joint(sns.kdeplot, levels=5, color='navy', linewidths=1.0)
g.plot_marginals(sns.histplot, kde=True, bins=25, color='steelblue', alpha=0.6)

g.ax_joint.set_xlabel('X (lognormal)'); g.ax_joint.set_ylabel('Y (lognormal)')
g.fig.suptitle('JointGrid: Scatter + KDE + Histogram Marginals', y=1.01)
g.fig.savefig('joint_grid_custom.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved joint_grid_custom.png')"""},
        {"label": "jointplot with regression and stats", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(5)
n = 150
x = np.random.uniform(10, 100, n)
y = 0.5*x + np.random.randn(n)*8 + 5

df = pd.DataFrame({'x': x, 'y': y})

g = sns.jointplot(data=df, x='x', y='y',
                  kind='reg', height=6,
                  scatter_kws=dict(alpha=0.5, s=30, color='steelblue'),
                  line_kws=dict(color='red', linewidth=2),
                  marginal_kws=dict(bins=20, kde=True))
# Compute and annotate correlation
r = df.corr().iloc[0,1]
g.ax_joint.text(0.05, 0.92, f'r = {r:.3f}', transform=g.ax_joint.transAxes,
                fontsize=11, fontweight='bold', color='red')
g.fig.suptitle('Joint Regression Plot with Correlation', y=1.02)
g.fig.savefig('joint_reg.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved joint_reg.png')"""},
    ],
    "Height-Weight Bivariate Analysis",
    "Show the joint distribution of height and weight across gender using JointGrid: central scatter colored by gender, marginal KDEs filled by gender, and a correlation annotation in the joint panel.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(77)
df = pd.DataFrame({
    'height_cm': np.concatenate([
        np.random.normal(165, 7, 200),
        np.random.normal(178, 8, 200)]),
    'weight_kg': np.concatenate([
        np.random.normal(62, 9, 200),
        np.random.normal(78, 11, 200)]),
    'gender': np.repeat(['Female','Male'], 200)
})

g = sns.JointGrid(data=df, x='height_cm', y='weight_kg', height=7)
palette = {'Female':'#dd8452','Male':'#4c72b0'}
for gender, grp in df.groupby('gender'):
    g.ax_joint.scatter(grp.height_cm, grp.weight_kg,
                       alpha=0.4, s=20, color=palette[gender], label=gender)
    sns.kdeplot(data=grp, x='height_cm', ax=g.ax_marg_x,
                fill=True, alpha=0.4, color=palette[gender], linewidth=1.5)
    sns.kdeplot(data=grp, y='weight_kg', ax=g.ax_marg_y,
                fill=True, alpha=0.4, color=palette[gender], linewidth=1.5)

g.ax_joint.legend(title='Gender')
r = df[['height_cm','weight_kg']].corr().iloc[0,1]
g.ax_joint.text(0.05,0.92,f'r = {r:.3f}',transform=g.ax_joint.transAxes,
                fontsize=11,fontweight='bold',color='darkred')
g.ax_joint.set_xlabel('Height (cm)'); g.ax_joint.set_ylabel('Weight (kg)')
g.fig.suptitle('Height-Weight Joint Distribution by Gender', y=1.02, fontweight='bold')
g.fig.savefig('height_weight_joint.png', dpi=150, bbox_inches='tight')
plt.close(g.fig)
print('Saved height_weight_joint.png')""",
    "Joint Plot Practice",
    "Load the 'penguins' dataset. Create a JointGrid for bill_length_mm vs bill_depth_mm: (1) scatter in the joint with hue=species and s=30, (2) boxplot in the marginals (ax_marg_x and ax_marg_y). Drop NaN rows first.",
    HDR + """\
sns.set_theme(style='whitegrid')
penguins = sns.load_dataset('penguins').dropna()

g = sns.JointGrid(data=penguins, x='bill_length_mm', y='bill_depth_mm', height=6)
# TODO: scatterplot joint with hue=species, s=30
# TODO: boxplot marginals for x and y
# TODO: legend, labels, title
# TODO: save 'penguin_joint.png'"""
)

# ── Section 22: catplot — Figure-Level Categorical ────────────────────────────
s22 = make_sns(
    22, "catplot — Figure-Level Categorical",
    "Use catplot() as a unified interface for all categorical plots. Control kind='strip'|'swarm'|'box'|'violin'|'bar'|'count'|'point' and use col/row to create FacetGrid-powered small multiples.",
    [
        {"label": "catplot with col splitting", "code": HDR + """\
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

g = sns.catplot(data=tips, x='day', y='total_bill',
                hue='sex', col='time',
                kind='box', palette='Set2',
                height=5, aspect=0.85,
                order=['Thur','Fri','Sat','Sun'])
g.set_axis_labels('Day', 'Total Bill ($)')
g.set_titles('{col_name}')
g.fig.suptitle('Bill by Day, Sex, and Time (catplot col)', y=1.02, fontweight='bold')
g.fig.savefig('catplot_col.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved catplot_col.png')"""},
        {"label": "catplot kind='violin' with row and col", "code": HDR + """\
sns.set_theme(style='whitegrid')
titanic = sns.load_dataset('titanic')

g = sns.catplot(data=titanic, x='class', y='age',
                col='survived', hue='sex',
                kind='violin', split=True, inner='quartile',
                palette='pastel', height=5, aspect=0.9)
g.set_axis_labels('Class', 'Age')
g.set_titles(col_template='Survived: {col_name}')
g.fig.suptitle('Titanic Age by Class, Gender & Survival', y=1.02, fontweight='bold')
g.fig.savefig('catplot_violin.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved catplot_violin.png')"""},
        {"label": "catplot kind='count' and 'bar'", "code": HDR + """\
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
# Count plot via catplot saved to file; replicate on axes
sns.countplot(data=tips, x='day', hue='sex', palette='Set1', ax=axes[0])
axes[0].set_title("countplot: Visits by Day")

sns.barplot(data=tips, x='day', y='tip', hue='sex',
            palette='Set2', capsize=0.08, ax=axes[1])
axes[1].set_title("barplot: Mean Tip by Day")
for ax in axes:
    ax.set_xlabel('Day')
fig.tight_layout()
fig.savefig('catplot_count_bar.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved catplot_count_bar.png')"""},
        {"label": "catplot kind='point' with order control", "code": HDR + """\
sns.set_theme(style='whitegrid')
titanic = sns.load_dataset('titanic')

g = sns.catplot(data=titanic, x='class', y='survived',
                hue='sex', col='embarked',
                kind='point', dodge=True, capsize=0.1,
                markers=['o','s'], linestyles=['-','--'],
                palette='Set1', height=4, aspect=0.85,
                order=['First','Second','Third'])
g.set_axis_labels('Class', 'Survival Rate')
g.set_titles(col_template='Embarked: {col_name}')
g.fig.suptitle('Survival Rate by Class, Sex & Port', y=1.02, fontweight='bold')
g.fig.savefig('catplot_point.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved catplot_point.png')"""},
    ],
    "Product Feedback Dashboard",
    "Use catplot to compare NPS scores across 4 product categories and 3 user segments. Show kind='box' with col=category, hue=segment, and a separate catplot kind='point' for mean scores.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(42)
categories = ['Mobile App','Web Platform','API','Support']
segments = ['Enterprise','SMB','Startup']
rows = []
bases = {'Mobile App': 7.0,'Web Platform': 6.5,'API': 8.0,'Support': 5.5}
seg_offsets = {'Enterprise': 0.5,'SMB': 0.0,'Startup': -0.3}
for cat in categories:
    for seg in segments:
        mu = bases[cat] + seg_offsets[seg]
        scores = np.random.normal(mu, 1.5, 40).clip(0, 10)
        for s in scores:
            rows.append({'category': cat,'segment': seg,'nps': s})
df = pd.DataFrame(rows)

g = sns.catplot(data=df, x='segment', y='nps', col='category',
                kind='box', hue='segment', palette='Set2',
                height=4, aspect=0.85, col_wrap=2,
                order=segments, legend=False)
g.set_axis_labels('Segment', 'NPS Score')
g.set_titles('{col_name}')
g.fig.suptitle('Product NPS by Category & Segment', y=1.02, fontweight='bold')
g.fig.savefig('nps_catplot.png', dpi=150, bbox_inches='tight')
plt.close(g.fig)
print('Saved nps_catplot.png')""",
    "catplot Practice",
    "Load the 'exercise' dataset from seaborn. Use catplot with x='time', y='pulse', hue='kind', col='diet', kind='point'. Then create a second catplot with kind='box'. Add appropriate titles and labels.",
    HDR + """\
sns.set_theme(style='whitegrid')
exercise = sns.load_dataset('exercise')

# TODO: catplot pointplot: x=time, y=pulse, hue=kind, col=diet
# TODO: catplot boxplot: same variables
# TODO: save 'exercise_catplot.png'"""
)

# ── Section 23: displot — Figure-Level Distributions ─────────────────────────
s23 = make_sns(
    23, "displot — Figure-Level Distributions",
    "Use displot() as the figure-level interface for histplot, kdeplot, and ecdfplot. Add col/row faceting for small-multiple distribution comparisons.",
    [
        {"label": "displot: hist, kde, ecdf kinds", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(0)
df = pd.DataFrame({
    'value': np.concatenate([np.random.normal(0,1,300), np.random.normal(4,1.5,300)]),
    'group': np.repeat(['A','B'], 300)
})

for kind in ['hist','kde','ecdf']:
    g = sns.displot(data=df, x='value', hue='group',
                    kind=kind, height=4, aspect=1.5, palette='Set2',
                    fill=(kind != 'ecdf'), alpha=0.5, linewidth=2)
    g.fig.suptitle(f"displot kind='{kind}'", y=1.02)
    g.fig.savefig(f'displot_{kind}.png', dpi=100, bbox_inches='tight')
    plt.close(g.fig)
print('Saved displot_hist/kde/ecdf.png')"""},
        {"label": "displot with col faceting", "code": HDR + """\
sns.set_theme(style='whitegrid')
titanic = sns.load_dataset('titanic').dropna(subset=['age'])

g = sns.displot(data=titanic, x='age', col='class',
                hue='survived', kind='hist', stat='density',
                kde=True, alpha=0.5, palette='Set1',
                height=4, aspect=0.85, col_order=['First','Second','Third'])
g.set_axis_labels('Age', 'Density')
g.set_titles(col_template='{col_name} Class')
g.fig.suptitle('Age Distribution by Class and Survival', y=1.02, fontweight='bold')
g.fig.savefig('displot_col.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved displot_col.png')"""},
        {"label": "displot with row and col", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(1)
regions = ['North','South']
periods = ['Q1','Q2','Q3','Q4']
rows = []
for region in regions:
    base = 50 if region == 'North' else 35
    for period in periods:
        offset = periods.index(period) * 5
        vals = np.random.normal(base + offset, 12, 100)
        for v in vals:
            rows.append({'region': region, 'period': period, 'sales': v})
df = pd.DataFrame(rows)

g = sns.displot(data=df, x='sales', row='region', col='period',
                kind='kde', fill=True, alpha=0.5, palette='Set2',
                height=3, aspect=1.1, col_order=periods)
g.set_axis_labels('Sales ($K)', 'Density')
g.fig.suptitle('Sales Distribution by Region & Quarter', y=1.02, fontweight='bold')
g.fig.savefig('displot_grid.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved displot_grid.png')"""},
        {"label": "displot with rug and binwidth", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(2)
df = pd.DataFrame({
    'latency': np.concatenate([
        np.random.lognormal(3, 0.4, 500),
        np.random.lognormal(4, 0.5, 200),
    ]),
    'endpoint': np.repeat(['/fast','/slow'], [500,200])
})

g = sns.displot(data=df, x='latency', hue='endpoint',
                kind='hist', stat='density', kde=True,
                rug=True, rug_kws=dict(height=0.05, alpha=0.3),
                log_scale=True, alpha=0.4, palette='Set1',
                height=5, aspect=1.6, binwidth=0.05)
g.set_axis_labels('Latency (ms, log scale)', 'Density')
g.fig.suptitle('Endpoint Latency Distribution with Rug', y=1.02, fontweight='bold')
g.fig.savefig('displot_rug.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved displot_rug.png')"""},
    ],
    "Multi-Experiment Distribution Report",
    "Use displot to compare test metric distributions across 3 ML experiments and 2 datasets (col=dataset, hue=experiment). Show kind='kde' with fill=True. Then show kind='ecdf' for cumulative comparison.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(88)
experiments = ['Baseline','DropoutReg','AugData']
datasets = ['CIFAR-10','ImageNet']
rows = []
means = {'Baseline': (72,80), 'DropoutReg': (75,83), 'AugData': (77,85)}
for exp, (m1, m2) in means.items():
    for ds, mu in zip(datasets, [m1, m2]):
        vals = np.random.normal(mu, 3, 150)
        for v in vals:
            rows.append({'experiment': exp, 'dataset': ds, 'accuracy': v})
df = pd.DataFrame(rows)

g = sns.displot(data=df, x='accuracy', hue='experiment', col='dataset',
                kind='kde', fill=True, alpha=0.4, linewidth=2,
                palette='Set2', height=4, aspect=1.2, common_norm=False)
g.set_axis_labels('Accuracy (%)', 'Density')
g.set_titles(col_template='{col_name}')
g.fig.suptitle('Model Accuracy Distribution by Experiment & Dataset', y=1.02, fontweight='bold')
g.fig.savefig('experiment_displot.png', dpi=150, bbox_inches='tight')
plt.close(g.fig)
print('Saved experiment_displot.png')""",
    "displot Practice",
    "Load the 'penguins' dataset. Use displot to create: (1) hist kind with col=species, x=body_mass_g, hue=sex — set kde=True, (2) ecdf kind with same grouping on a new figure. Save both as separate PNGs.",
    HDR + """\
sns.set_theme(style='whitegrid')
penguins = sns.load_dataset('penguins').dropna()

# TODO: displot hist kind, col=species, x=body_mass_g, hue=sex, kde=True
# TODO: save 'penguin_hist.png'
# TODO: displot ecdf kind, same grouping
# TODO: save 'penguin_ecdf.png'"""
)

# ── Section 24: relplot — Figure-Level Relational ─────────────────────────────
s24 = make_sns(
    24, "relplot — Figure-Level Relational",
    "Use relplot() as the figure-level interface for scatterplot and lineplot. Use col, row, and hue to create multi-panel relational grids with consistent scaling.",
    [
        {"label": "relplot scatter with col and hue", "code": HDR + """\
sns.set_theme(style='whitegrid')
tips = sns.load_dataset('tips')

g = sns.relplot(data=tips, x='total_bill', y='tip',
                hue='sex', col='time', style='sex',
                palette='Set1', s=60, alpha=0.7,
                height=4, aspect=1.0)
g.set_axis_labels('Total Bill ($)', 'Tip ($)')
g.set_titles(col_template='{col_name}')
g.fig.suptitle('Tips: Scatter by Time and Sex (relplot)', y=1.02, fontweight='bold')
g.fig.savefig('relplot_scatter.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved relplot_scatter.png')"""},
        {"label": "relplot lineplot with col_wrap", "code": HDR + """\
sns.set_theme(style='darkgrid')
np.random.seed(0)
subjects = [f'Subject_{i:02d}' for i in range(1, 7)]
df_list = []
for subj in subjects:
    t = np.arange(20)
    y = np.sin(t*0.3 + np.random.uniform(0,3)) + np.random.randn(20)*0.2
    df_list.append(pd.DataFrame({'time':t,'value':y,'subject':subj}))
df = pd.concat(df_list, ignore_index=True)

g = sns.relplot(data=df, x='time', y='value', col='subject',
                kind='line', col_wrap=3, palette='tab10',
                height=3, aspect=1.3, linewidth=2)
g.set_axis_labels('Time', 'Signal')
g.set_titles(col_template='{col_name}')
g.fig.suptitle('Subject Time Series (relplot col_wrap=3)', y=1.02, fontweight='bold')
g.fig.savefig('relplot_line.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved relplot_line.png')"""},
        {"label": "relplot with size and style encoding", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(1)
n = 200
df = pd.DataFrame({
    'x': np.random.randn(n),
    'y': np.random.randn(n),
    'size_var': np.random.uniform(50, 300, n),
    'category': np.random.choice(['A','B','C'], n),
    'quality': np.random.choice(['High','Low'], n)
})

g = sns.relplot(data=df, x='x', y='y',
                hue='category', size='size_var', style='quality',
                palette='Set2', sizes=(20, 300), alpha=0.7,
                height=5, aspect=1.2)
g.ax.set_title('Multi-Encoding Scatter: hue + size + style', fontweight='bold')
g.fig.savefig('relplot_multi.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved relplot_multi.png')"""},
        {"label": "relplot row and col grid", "code": HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(2)
conditions = ['Fast','Slow']
groups = ['Treatment','Control']
rows = []
for cond in conditions:
    for grp in groups:
        mu = (4 if grp=='Treatment' else 2) + (1 if cond=='Fast' else 0)
        t = np.arange(30)
        y = mu + np.cumsum(np.random.randn(30)*0.3) + np.sin(t*0.2)
        df_part = pd.DataFrame({'time':t,'signal':y,
                                 'condition':cond,'group':grp})
        rows.append(df_part)
df = pd.concat(rows, ignore_index=True)

g = sns.relplot(data=df, x='time', y='signal',
                row='group', col='condition',
                kind='line', palette='Set1', hue='group',
                height=3.5, aspect=1.2, linewidth=2)
g.set_axis_labels('Time', 'Signal')
g.set_titles(row_template='{row_name}', col_template='{col_name}')
g.fig.suptitle('Signal by Group × Condition (relplot grid)', y=1.02, fontweight='bold')
g.fig.savefig('relplot_grid.png', dpi=120, bbox_inches='tight')
plt.close(g.fig)
print('Saved relplot_grid.png')"""},
    ],
    "Marketing Campaign Performance",
    "Plot click-through rate vs spend for 4 campaign types across 3 channels (col=channel). Use relplot kind='scatter', size=impressions (scaled), hue=campaign_type. Add a regression line for each panel.",
    HDR + """\
sns.set_theme(style='whitegrid')
np.random.seed(66)
channels = ['Search','Social','Display']
campaigns = ['Brand','Retargeting','Prospecting','Seasonal']
rows = []
for ch in channels:
    for camp in campaigns:
        n = 40
        spend = np.random.uniform(500, 5000, n)
        ctr   = 0.02 + spend/100000 + np.random.randn(n)*0.005
        ctr   = np.clip(ctr, 0.001, 0.15)
        impr  = spend * np.random.uniform(100, 500, n)
        for s, c, im in zip(spend, ctr, impr):
            rows.append({'channel':ch,'campaign':camp,'spend':s,'ctr':c,'impressions':im})
df = pd.DataFrame(rows)

g = sns.relplot(data=df, x='spend', y='ctr',
                col='channel', hue='campaign', style='campaign',
                size='impressions', sizes=(20, 200),
                palette='tab10', alpha=0.7, height=4, aspect=1.1)
# Overlay regression line for each axis
for ax in g.axes.flat:
    if ax is not None:
        ch_data = df[df.channel == ax.get_title().strip()]
        if len(ch_data):
            m, b = np.polyfit(ch_data.spend, ch_data.ctr, 1)
            x_line = np.linspace(ch_data.spend.min(), ch_data.spend.max(), 50)
            ax.plot(x_line, m*x_line+b, 'r--', linewidth=1.5, alpha=0.8)
g.set_axis_labels('Spend ($)', 'CTR')
g.set_titles(col_template='{col_name}')
g.fig.suptitle('Campaign CTR vs Spend by Channel', y=1.02, fontweight='bold')
g.fig.savefig('campaign_relplot.png', dpi=150, bbox_inches='tight')
plt.close(g.fig)
print('Saved campaign_relplot.png')""",
    "relplot Practice",
    "Load the 'fmri' dataset. Use relplot with kind='line', x='timepoint', y='signal', hue='event', col='region'. Then create a second relplot kind='scatter' with the same groupings and size=0.5. Save both.",
    HDR + """\
sns.set_theme(style='darkgrid')
fmri = sns.load_dataset('fmri')

# TODO: relplot line, x=timepoint, y=signal, hue=event, col=region
# TODO: save 'fmri_line.png'
# TODO: relplot scatter, same grouping
# TODO: save 'fmri_scatter.png'"""
)


# ── Assemble and insert ───────────────────────────────────────────────────────
all_sections = s17 + s18 + s19 + s20 + s21 + s22 + s23 + s24
result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: seaborn sections 17-24 added")
else:
    print("FAILED")
