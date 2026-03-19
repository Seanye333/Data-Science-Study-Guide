"""Add Matplotlib sections 17-24 to gen_matplotlib.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _inserter import insert_sections

FILE   = pathlib.Path(__file__).parent / "gen_matplotlib.py"
MARKER = "]  # end SECTIONS"

HDR = (
    "import matplotlib\n"
    "matplotlib.use('Agg')\n"
    "import matplotlib.pyplot as plt\n"
    "import numpy as np\n\n"
)

def ec(s):
    return (s.replace('\\','\\\\').replace('"','\\"')
             .replace('\n','\\n').replace("'","\\'"))

def make_mpl(num, title, desc, examples, rw_title, rw_scenario, rw_code, pt, pd_text, ps):
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

# ── Section 17: Error Bars & Confidence Intervals ─────────────────────────────
s17 = make_mpl(
    17, "Error Bars & Confidence Intervals",
    "Visualize measurement uncertainty with errorbar(), fill_between() for confidence bands, and asymmetric errors.",
    [
        {"label": "Basic symmetric error bars", "code": HDR + """\
np.random.seed(0)
x = np.arange(1, 8)
y = np.array([2.3, 3.1, 2.8, 4.5, 3.9, 5.2, 4.8])
yerr = np.random.uniform(0.2, 0.6, len(x))

fig, ax = plt.subplots(figsize=(8, 4))
ax.errorbar(x, y, yerr=yerr, fmt='o-', color='steelblue',
            ecolor='lightsteelblue', elinewidth=2, capsize=5,
            capthick=2, label='Mean ± SD')
ax.set_xlabel('Experiment')
ax.set_ylabel('Value')
ax.set_title('Error Bars — Symmetric')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('errorbars_sym.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved errorbars_sym.png')"""},
        {"label": "Asymmetric error bars", "code": HDR + """\
np.random.seed(1)
x = np.arange(5)
y = np.array([1.5, 2.8, 2.2, 3.6, 3.0])
yerr_low  = np.array([0.3, 0.5, 0.4, 0.6, 0.3])
yerr_high = np.array([0.5, 0.3, 0.6, 0.2, 0.7])

fig, ax = plt.subplots(figsize=(7, 4))
ax.errorbar(x, y, yerr=[yerr_low, yerr_high],
            fmt='s--', color='tomato', ecolor='lightcoral',
            elinewidth=2, capsize=6, label='Median [IQR]')
ax.set_xticks(x)
ax.set_xticklabels([f'Group {i+1}' for i in x])
ax.set_title('Asymmetric Error Bars')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('errorbars_asym.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved errorbars_asym.png')"""},
        {"label": "Confidence band with fill_between", "code": HDR + """\
np.random.seed(2)
x = np.linspace(0, 10, 100)
y_true = np.sin(x)
noise = np.random.randn(100) * 0.3
y_mean = y_true + noise * 0.2
y_lower = y_mean - 1.96 * 0.3
y_upper = y_mean + 1.96 * 0.3

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(x, y_mean, color='steelblue', linewidth=2, label='Mean')
ax.fill_between(x, y_lower, y_upper, alpha=0.2, color='steelblue',
                label='95% CI')
ax.plot(x, y_true, 'k--', linewidth=1, alpha=0.6, label='True')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Confidence Interval Band')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('conf_band.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved conf_band.png')"""},
        {"label": "Multiple series with shaded bands", "code": HDR + """\
np.random.seed(42)
x = np.linspace(0, 5, 80)
colors = ['steelblue', 'tomato', 'seagreen']
labels = ['Model A', 'Model B', 'Model C']
offsets = [0, 0.5, 1.0]

fig, ax = plt.subplots(figsize=(9, 5))
for c, lab, off in zip(colors, labels, offsets):
    mu = np.sin(x + off)
    sd = 0.15 + 0.05 * np.abs(np.cos(x))
    ax.plot(x, mu, color=c, linewidth=2, label=lab)
    ax.fill_between(x, mu - sd, mu + sd, color=c, alpha=0.15)
ax.set_xlabel('Time')
ax.set_ylabel('Score')
ax.set_title('Model Comparison with Confidence Bands')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('multi_band.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved multi_band.png')"""},
    ],
    "Clinical Trial Results",
    "Visualize drug-trial results with asymmetric confidence intervals for 4 dosage groups, a reference line at placebo, and significance brackets.",
    HDR + """\
np.random.seed(7)
groups = ['Placebo', '10mg', '25mg', '50mg']
means  = [0.0, 1.2, 2.8, 3.5]
low    = [0.0, 0.3, 0.5, 0.4]
high   = [0.0, 0.5, 0.6, 0.8]

fig, ax = plt.subplots(figsize=(7, 5))
x = np.arange(len(groups))
ax.bar(x, means, color=['#aaa','#5ab4d6','#2171b5','#084594'],
       alpha=0.85, width=0.5)
ax.errorbar(x, means, yerr=[low, high],
            fmt='none', ecolor='black', elinewidth=2, capsize=8, capthick=2)
ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax.set_xticks(x); ax.set_xticklabels(groups)
ax.set_ylabel('Effect Size vs Baseline')
ax.set_title('Clinical Trial: Dose-Response', fontweight='bold')
for xi, m, h in zip(x[1:], means[1:], high[1:]):
    ax.text(xi, m + h + 0.05, '*' if m < 3 else '***',
            ha='center', fontsize=14, color='darkred')
fig.tight_layout()
fig.savefig('clinical_trial.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved clinical_trial.png')""",
    "Error Bar Practice",
    "Generate 6 groups with random means (2-8) and errors. Plot horizontal error bars (ax.errorbar with fmt='o', xerr=...) with capsize=5. Color bars by quartile (low=green, mid=orange, high=red). Add a vertical reference line at x=5.",
    HDR + """\
np.random.seed(10)
groups = [f'Group {i}' for i in range(1, 7)]
means  = np.random.uniform(2, 8, 6)
errors = np.random.uniform(0.3, 1.2, 6)
# TODO: horizontal errorbar plot
# TODO: color by quartile
# TODO: vertical reference line at x=5
# TODO: save 'hbar_errors.png'"""
)

# ── Section 18: Box Plots & Violin Plots ──────────────────────────────────────
s18 = make_mpl(
    18, "Box Plots & Violin Plots",
    "Compare distributions across groups with boxplot() for quartile summaries and violinplot() for full density shapes. Combine both for richer insights.",
    [
        {"label": "Side-by-side box plots", "code": HDR + """\
np.random.seed(0)
data = [np.random.normal(loc, 1.0, 80) for loc in [2, 3.5, 2.8, 4.2, 3.0]]
labels = ['A', 'B', 'C', 'D', 'E']

fig, ax = plt.subplots(figsize=(8, 5))
bp = ax.boxplot(data, labels=labels, patch_artist=True, notch=True,
                medianprops=dict(color='white', linewidth=2))
colors = ['#4c72b0','#dd8452','#55a868','#c44e52','#8172b2']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)
ax.set_xlabel('Group')
ax.set_ylabel('Value')
ax.set_title('Notched Box Plots by Group')
ax.grid(True, axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig('boxplot.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved boxplot.png')"""},
        {"label": "Violin plot with overlaid box", "code": HDR + """\
np.random.seed(1)
data = [np.concatenate([np.random.normal(0, 1, 60),
                         np.random.normal(3, 0.5, 20)])
        for _ in range(4)]
labels = ['Q1', 'Q2', 'Q3', 'Q4']

fig, ax = plt.subplots(figsize=(8, 5))
parts = ax.violinplot(data, positions=range(1, 5), showmedians=True,
                       showextrema=True)
for pc in parts['bodies']:
    pc.set_facecolor('#4c72b0')
    pc.set_alpha(0.7)
ax.boxplot(data, positions=range(1, 5), widths=0.1,
           patch_artist=True,
           boxprops=dict(facecolor='white', linewidth=1),
           medianprops=dict(color='red', linewidth=2),
           whiskerprops=dict(linewidth=1),
           capprops=dict(linewidth=1),
           flierprops=dict(markersize=3))
ax.set_xticks(range(1, 5)); ax.set_xticklabels(labels)
ax.set_title('Violin + Box Plot Overlay')
ax.grid(True, axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig('violin_box.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved violin_box.png')"""},
        {"label": "Grouped box plots with hue", "code": HDR + """\
np.random.seed(2)
n = 60
months = ['Jan', 'Feb', 'Mar', 'Apr']
treatments = ['Control', 'Treatment']
x_pos = np.array([0, 1, 2, 3])
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5))
for i, (trt, color) in enumerate(zip(treatments, ['#4c72b0','#dd8452'])):
    data = [np.random.normal(2 + i * 0.8 + j * 0.3, 0.7, n) for j in range(4)]
    bp = ax.boxplot(data, positions=x_pos + (i - 0.5) * width,
                    widths=width * 0.85, patch_artist=True,
                    medianprops=dict(color='white', linewidth=2))
    for patch in bp['boxes']:
        patch.set_facecolor(color); patch.set_alpha(0.75)
ax.set_xticks(x_pos); ax.set_xticklabels(months)
ax.set_xlabel('Month'); ax.set_ylabel('Score')
ax.set_title('Grouped Box Plots: Control vs Treatment')
handles = [plt.Rectangle((0,0),1,1, color=c, alpha=0.75) for c in ['#4c72b0','#dd8452']]
ax.legend(handles, treatments)
ax.grid(True, axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig('grouped_box.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved grouped_box.png')"""},
        {"label": "Half-violin with jitter (raincloud style)", "code": HDR + """\
np.random.seed(42)
groups = ['Low', 'Mid', 'High']
data = [np.random.normal(m, 0.8, 80) for m in [1.5, 3.0, 4.5]]
colors = ['#5ab4d6', '#f4a261', '#e76f51']

fig, ax = plt.subplots(figsize=(8, 5))
for i, (d, c) in enumerate(zip(data, colors)):
    parts = ax.violinplot([d], positions=[i], showmedians=False,
                          showextrema=False)
    for pc in parts['bodies']:
        pc.set_facecolor(c); pc.set_alpha(0.6)
        # half violin: mask right side
        verts = pc.get_paths()[0].vertices
        verts[:, 0] = np.clip(verts[:, 0], -np.inf, i)
        pc.get_paths()[0].vertices = verts
    # jitter
    jitter = np.random.uniform(-0.05, 0.05, len(d))
    ax.scatter(i + 0.05 + jitter, d, alpha=0.4, s=15, color=c)
    ax.hlines(np.median(d), i - 0.3, i + 0.1, colors='black', linewidth=2)
ax.set_xticks(range(3)); ax.set_xticklabels(groups)
ax.set_title('Raincloud Plot (Half Violin + Jitter)')
ax.grid(True, axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig('raincloud.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved raincloud.png')"""},
    ],
    "Product Quality Distribution",
    "QA team needs to compare defect rates across 5 production lines for 3 shifts. Use grouped notched box plots with color coding, outlier markers, and a horizontal threshold line.",
    HDR + """\
np.random.seed(99)
lines = ['L1','L2','L3','L4','L5']
shifts = ['Morning','Afternoon','Night']
colors = ['#2196f3','#ff9800','#9c27b0']
x_pos = np.arange(5)
width = 0.25

fig, ax = plt.subplots(figsize=(11, 5))
for si, (shift, col) in enumerate(zip(shifts, colors)):
    data = [np.random.exponential(1 + si * 0.5 + li * 0.2, 50) for li in range(5)]
    bp = ax.boxplot(data, positions=x_pos + (si-1)*width, widths=width*0.85,
                    patch_artist=True, notch=True,
                    medianprops=dict(color='white', linewidth=2),
                    flierprops=dict(marker='x', color=col, markersize=5))
    for patch in bp['boxes']:
        patch.set_facecolor(col); patch.set_alpha(0.75)
ax.axhline(3.0, color='red', linestyle='--', linewidth=1.5, label='Threshold')
ax.set_xticks(x_pos); ax.set_xticklabels(lines)
ax.set_xlabel('Production Line'); ax.set_ylabel('Defects per 100 units')
ax.set_title('Quality Control: Defects by Line & Shift', fontweight='bold')
handles = [plt.Rectangle((0,0),1,1,color=c,alpha=0.75) for c in colors] + \
          [plt.Line2D([0],[0],color='red',linestyle='--')]
ax.legend(handles, shifts + ['Threshold'], ncol=4)
ax.grid(True, axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig('qc_boxplot.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved qc_boxplot.png')""",
    "Distribution Comparison Practice",
    "Create 4 groups of data: bimodal (two Gaussians mixed), right-skewed (exponential), uniform, and heavy-tailed (Student-t df=2). Plot violin plots in a 2x2 subplot grid. Add the mean as a diamond marker and IQR as a vertical line on each.",
    HDR + """\
np.random.seed(5)
bimodal  = np.concatenate([np.random.normal(-2,0.5,100), np.random.normal(2,0.5,100)])
skewed   = np.random.exponential(1.5, 200)
uniform  = np.random.uniform(-3, 3, 200)
heavy    = np.random.standard_t(df=2, size=200)
datasets = [bimodal, skewed, uniform, heavy]
titles   = ['Bimodal', 'Right-Skewed', 'Uniform', 'Heavy-Tailed']

fig, axes = plt.subplots(2, 2, figsize=(9, 7))
for ax, d, title in zip(axes.flat, datasets, titles):
    ax.violinplot([d], showmedians=True, showextrema=True)
    # TODO: add mean as diamond marker
    # TODO: label the title
    pass
fig.suptitle('Distribution Shapes Comparison', fontweight='bold')
fig.tight_layout()
fig.savefig('dist_shapes.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved dist_shapes.png')"""
)

# ── Section 19: Contour Plots ─────────────────────────────────────────────────
s19 = make_mpl(
    19, "Contour Plots",
    "Use contour() for lines and contourf() for filled regions to display 2D scalar fields, decision boundaries, and topographic data.",
    [
        {"label": "Basic contour and contourf", "code": HDR + """\
x = y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
# Filled contour
cf = ax1.contourf(X, Y, Z, levels=20, cmap='RdBu_r')
fig.colorbar(cf, ax=ax1, label='Z')
ax1.set_title('contourf — filled')

# Line contour with labels
cs = ax2.contour(X, Y, Z, levels=15, cmap='RdBu_r')
ax2.clabel(cs, inline=True, fontsize=8, fmt='%.1f')
ax2.set_title('contour — lines with labels')

for ax in (ax1, ax2):
    ax.set_xlabel('x'); ax.set_ylabel('y')
fig.tight_layout()
fig.savefig('contour_basic.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved contour_basic.png')"""},
        {"label": "Decision boundary visualization", "code": HDR + """\
from matplotlib.colors import ListedColormap

np.random.seed(0)
X_cls = np.random.randn(200, 2)
y_cls = ((X_cls[:,0]**2 + X_cls[:,1]**2) < 1.5).astype(int)

xx, yy = np.meshgrid(np.linspace(-3,3,300), np.linspace(-3,3,300))
r = xx**2 + yy**2
zz = (r < 1.5).astype(float)

fig, ax = plt.subplots(figsize=(6, 5))
ax.contourf(xx, yy, zz, alpha=0.3, cmap=ListedColormap(['#ff7f7f','#7fbfff']))
ax.contour(xx, yy, zz, colors='black', linewidths=1.5)
colors_pt = ['#cc0000' if yi else '#0055aa' for yi in y_cls]
ax.scatter(X_cls[:,0], X_cls[:,1], c=colors_pt, s=30, edgecolors='k', linewidths=0.5)
ax.set_title('Circular Decision Boundary')
ax.set_xlabel('Feature 1'); ax.set_ylabel('Feature 2')
fig.tight_layout()
fig.savefig('decision_boundary.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved decision_boundary.png')"""},
        {"label": "Topographic map with hillshading", "code": HDR + """\
from matplotlib.colors import LightSource

x = y = np.linspace(0, 4*np.pi, 300)
X, Y = np.meshgrid(x, y)
Z = np.sin(X/2) * np.cos(Y/3) + 0.5*np.sin(X + Y)

ls = LightSource(azdeg=315, altdeg=45)
hillshade = ls.hillshade(Z, vert_exag=1.5)

fig, ax = plt.subplots(figsize=(8, 6))
ax.imshow(hillshade, cmap='gray', origin='lower', alpha=0.6)
cf = ax.contourf(Z, levels=25, cmap='terrain', alpha=0.7, origin='lower')
cs = ax.contour(Z, levels=10, colors='k', linewidths=0.5, alpha=0.5, origin='lower')
fig.colorbar(cf, ax=ax, label='Elevation')
ax.set_title('Topographic Map with Hillshading')
fig.tight_layout()
fig.savefig('topo_map.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved topo_map.png')"""},
        {"label": "Contour overlay on scatter", "code": HDR + """\
from scipy.stats import gaussian_kde

np.random.seed(3)
x = np.concatenate([np.random.normal(0,1,150), np.random.normal(3,0.8,100)])
y = np.concatenate([np.random.normal(0,1,150), np.random.normal(2,0.8,100)])

# KDE over a grid
xi = np.linspace(x.min()-1, x.max()+1, 150)
yi = np.linspace(y.min()-1, y.max()+1, 150)
Xi, Yi = np.meshgrid(xi, yi)
k = gaussian_kde(np.vstack([x, y]))
Zi = k(np.vstack([Xi.ravel(), Yi.ravel()])).reshape(Xi.shape)

fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(x, y, s=15, alpha=0.4, color='steelblue')
cf = ax.contourf(Xi, Yi, Zi, levels=10, cmap='Blues', alpha=0.5)
ax.contour(Xi, Yi, Zi, levels=10, colors='navy', linewidths=0.8, alpha=0.7)
fig.colorbar(cf, ax=ax, label='Density')
ax.set_title('KDE Contour Overlay on Scatter')
fig.tight_layout()
fig.savefig('kde_contour.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved kde_contour.png')"""},
    ],
    "Loss Landscape Visualization",
    "Plot the loss surface of a simplified neural network (Z = (X-1)^2 + 2*(Y+0.5)^2 + 0.5*sin(3X)) with a filled contour, gradient-descent path overlay, and start/end markers.",
    HDR + """\
x = np.linspace(-2, 3, 300)
y = np.linspace(-2.5, 1.5, 300)
X, Y = np.meshgrid(x, y)
Z = (X-1)**2 + 2*(Y+0.5)**2 + 0.5*np.sin(3*X)

# Simulated gradient-descent path
path_x = [-1.5]
path_y = [-2.0]
lr = 0.1
for _ in range(40):
    gx = 2*(path_x[-1]-1) + 1.5*np.cos(3*path_x[-1])
    gy = 4*(path_y[-1]+0.5)
    path_x.append(path_x[-1] - lr*gx)
    path_y.append(path_y[-1] - lr*gy)

fig, ax = plt.subplots(figsize=(8, 6))
cf = ax.contourf(X, Y, Z, levels=30, cmap='viridis')
fig.colorbar(cf, ax=ax, label='Loss')
ax.contour(X, Y, Z, levels=15, colors='white', linewidths=0.5, alpha=0.4)
ax.plot(path_x, path_y, 'w-o', markersize=4, linewidth=1.5, label='GD path')
ax.plot(path_x[0], path_y[0], 'rs', markersize=10, label='Start')
ax.plot(path_x[-1], path_y[-1], 'r*', markersize=14, label='End')
ax.set_xlabel('w1'); ax.set_ylabel('w2')
ax.set_title('Loss Landscape & Gradient Descent', fontweight='bold')
ax.legend(facecolor='#222')
fig.tight_layout()
fig.savefig('loss_landscape.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved loss_landscape.png')""",
    "Contour Practice",
    "Create Z = cos(sqrt(X^2 + Y^2)) for X,Y in [-6,6]. Plot: (1) filled contour with 'plasma' colormap, (2) white contour lines at 10 levels, (3) colorbar labeled 'Amplitude'. Add a red star marker at (0,0) where the function is maximum.",
    HDR + """\
x = y = np.linspace(-6, 6, 300)
X, Y = np.meshgrid(x, y)
Z = np.cos(np.sqrt(X**2 + Y**2))

fig, ax = plt.subplots(figsize=(7, 6))
# TODO: contourf with plasma cmap
# TODO: white contour lines, 10 levels
# TODO: colorbar labeled 'Amplitude'
# TODO: red star marker at (0, 0)
# TODO: save 'ripple.png'
plt.close()"""
)

# ── Section 20: Polar Plots ───────────────────────────────────────────────────
s20 = make_mpl(
    20, "Polar Plots",
    "Use polar projections for directional data, radar charts, and rose diagrams. Access the polar axes with subplot_kw={'projection':'polar'}.",
    [
        {"label": "Basic polar line and fill", "code": HDR + """\
theta = np.linspace(0, 2*np.pi, 300)
r = 1 + 0.5 * np.cos(3*theta)

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
ax.plot(theta, r, color='steelblue', linewidth=2)
ax.fill(theta, r, color='steelblue', alpha=0.2)
ax.set_title('Rose Curve: 1 + 0.5·cos(3θ)', pad=20)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('polar_rose.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved polar_rose.png')"""},
        {"label": "Wind rose bar chart", "code": HDR + """\
np.random.seed(5)
n_dirs = 16
theta_bars = np.linspace(0, 2*np.pi, n_dirs, endpoint=False)
radii = np.abs(np.random.randn(n_dirs)) * 10 + 5
width = 2*np.pi / n_dirs

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={'projection': 'polar'})
bars = ax.bar(theta_bars, radii, width=width, bottom=0,
              color=plt.cm.hsv(theta_bars / (2*np.pi)), alpha=0.8, edgecolor='white')
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
dirs = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
        'S','SSW','SW','WSW','W','WNW','NW','NNW']
ax.set_xticks(theta_bars)
ax.set_xticklabels(dirs, fontsize=8)
ax.set_title('Wind Rose Diagram', pad=20, fontweight='bold')
fig.tight_layout()
fig.savefig('wind_rose.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved wind_rose.png')"""},
        {"label": "Radar / spider chart", "code": HDR + """\
categories = ['Speed','Strength','Defense','Agility','Intelligence','Stamina']
N = len(categories)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # close the loop

player_a = [8, 6, 7, 9, 5, 7]
player_b = [5, 9, 8, 4, 7, 6]
for v in (player_a, player_b):
    v.append(v[0])

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={'projection': 'polar'})
ax.plot(angles, player_a, 'o-', color='steelblue', linewidth=2, label='Player A')
ax.fill(angles, player_a, color='steelblue', alpha=0.2)
ax.plot(angles, player_b, 's-', color='tomato', linewidth=2, label='Player B')
ax.fill(angles, player_b, color='tomato', alpha=0.2)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10)
ax.set_ylim(0, 10)
ax.set_title('Player Stats Radar Chart', pad=20, fontweight='bold')
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
fig.tight_layout()
fig.savefig('radar.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved radar.png')"""},
        {"label": "Polar scatter with colormap", "code": HDR + """\
np.random.seed(3)
n = 200
theta = np.random.uniform(0, 2*np.pi, n)
r = np.random.exponential(2, n)
c = theta / (2*np.pi)

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={'projection': 'polar'})
sc = ax.scatter(theta, r, c=c, cmap='hsv', s=40, alpha=0.7)
fig.colorbar(sc, ax=ax, label='Direction (normalized)', pad=0.1)
ax.set_title('Polar Scatter — Exponential Radii', pad=20)
fig.tight_layout()
fig.savefig('polar_scatter.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved polar_scatter.png')"""},
    ],
    "Sales Direction Analysis",
    "Visualize monthly sales volume by compass direction for a logistics company. Use a wind-rose style bar chart with bars colored by volume (viridis colormap) and annotated with top 3 directions.",
    HDR + """\
np.random.seed(21)
n_dirs = 12
months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']
theta_bars = np.linspace(0, 2*np.pi, n_dirs, endpoint=False)
sales = np.abs(np.random.randn(n_dirs)) * 50 + 80
width = 2*np.pi / n_dirs

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
norm = plt.Normalize(sales.min(), sales.max())
colors = plt.cm.viridis(norm(sales))
bars = ax.bar(theta_bars, sales, width=width, bottom=5,
              color=colors, alpha=0.85, edgecolor='white')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks(theta_bars); ax.set_xticklabels(months, fontsize=9)
ax.set_title('Monthly Sales by Direction', pad=20, fontweight='bold')
# annotate top 3
top3 = np.argsort(sales)[-3:]
for idx in top3:
    ax.annotate(f'{sales[idx]:.0f}',
                xy=(theta_bars[idx], sales[idx]+8),
                ha='center', fontsize=9, color='gold', fontweight='bold')
sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
fig.colorbar(sm, ax=ax, label='Sales Volume', pad=0.1)
fig.tight_layout()
fig.savefig('sales_polar.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved sales_polar.png')""",
    "Polar Plot Practice",
    "Create a radar chart with 8 categories (Communication, Analysis, Design, Coding, Testing, DevOps, Leadership, Creativity). Plot two engineers' scores (randomly generated 1-10). Close the polygon, fill with alpha=0.2, and add a legend. Save as 'skills_radar.png'.",
    HDR + """\
categories = ['Communication','Analysis','Design','Coding',
              'Testing','DevOps','Leadership','Creativity']
N = len(categories)
np.random.seed(42)
eng1 = np.random.randint(4, 10, N).tolist()
eng2 = np.random.randint(3, 10, N).tolist()
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
# TODO: close the polygon (append first element to angles, eng1, eng2)
# TODO: polar subplot
# TODO: plot and fill both engineers
# TODO: set tick labels to categories
# TODO: save 'skills_radar.png'"""
)

# ── Section 21: Stacked Bar & Area Charts ─────────────────────────────────────
s21 = make_mpl(
    21, "Stacked Bar & Area Charts",
    "Show part-to-whole relationships over categories or time with stacked bar charts and area plots using stackplot().",
    [
        {"label": "Stacked bar chart", "code": HDR + """\
categories = ['Q1','Q2','Q3','Q4']
product_a = [120, 145, 160, 180]
product_b = [90,  110, 95,  130]
product_c = [60,  75,  80,  95]
x = np.arange(len(categories))
colors = ['#4c72b0','#dd8452','#55a868']

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x, product_a, label='Product A', color=colors[0], width=0.5)
ax.bar(x, product_b, bottom=product_a, label='Product B', color=colors[1], width=0.5)
bottom_c = [a+b for a,b in zip(product_a, product_b)]
ax.bar(x, product_c, bottom=bottom_c, label='Product C', color=colors[2], width=0.5)
ax.set_xticks(x); ax.set_xticklabels(categories)
ax.set_ylabel('Revenue ($K)')
ax.set_title('Quarterly Revenue by Product — Stacked')
ax.legend(loc='upper left')
ax.grid(True, axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig('stacked_bar.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved stacked_bar.png')"""},
        {"label": "100% stacked bar (normalized)", "code": HDR + """\
categories = ['North','South','East','West','Central']
a = np.array([30, 45, 20, 60, 35])
b = np.array([50, 30, 55, 25, 40])
c = np.array([20, 25, 25, 15, 25])
total = a + b + c
a_p, b_p, c_p = a/total*100, b/total*100, c/total*100
x = np.arange(len(categories))

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x, a_p, label='Tier 1', color='#4c72b0', width=0.55)
ax.bar(x, b_p, bottom=a_p, label='Tier 2', color='#dd8452', width=0.55)
ax.bar(x, c_p, bottom=a_p+b_p, label='Tier 3', color='#55a868', width=0.55)
for xi, (ap, bp, cp) in enumerate(zip(a_p, b_p, c_p)):
    ax.text(xi, ap/2, f'{ap:.0f}%', ha='center', va='center', fontsize=9, color='white', fontweight='bold')
    ax.text(xi, ap+bp/2, f'{bp:.0f}%', ha='center', va='center', fontsize=9, color='white', fontweight='bold')
    ax.text(xi, ap+bp+cp/2, f'{cp:.0f}%', ha='center', va='center', fontsize=9, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(categories)
ax.set_ylabel('Percentage'); ax.set_ylim(0,100)
ax.set_title('100% Stacked Bar — Market Share by Region')
ax.legend(loc='upper right')
fig.tight_layout()
fig.savefig('stacked_100.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved stacked_100.png')"""},
        {"label": "Stack area chart with stackplot()", "code": HDR + """\
np.random.seed(0)
months = np.arange(1, 13)
direct   = np.array([200,210,225,240,260,280,270,290,310,295,320,350])
organic  = np.array([80, 95, 100,110,125,140,135,150,160,155,175,190])
referral = np.array([40, 45, 50, 55, 60, 65, 70, 68, 75, 72, 80, 90])
labels_s = ['Direct','Organic','Referral']
colors_s = ['#4c72b0','#55a868','#dd8452']

fig, ax = plt.subplots(figsize=(9, 5))
ax.stackplot(months, direct, organic, referral,
             labels=labels_s, colors=colors_s, alpha=0.8)
ax.set_xlabel('Month'); ax.set_ylabel('Sessions (K)')
ax.set_title('Website Traffic by Source — Stacked Area')
ax.set_xticks(months)
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'], rotation=30)
ax.legend(loc='upper left'); ax.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig('stackplot.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved stackplot.png')"""},
        {"label": "Stream graph (centered stackplot)", "code": HDR + """\
np.random.seed(7)
x = np.linspace(0, 10, 100)
n_series = 5
ys = [np.abs(np.random.randn(100)).cumsum() * 0.3 + np.random.uniform(1,3)
      for _ in range(n_series)]
baseline = -np.array(ys).sum(axis=0) / 2  # center

fig, ax = plt.subplots(figsize=(10, 5))
cmap = plt.cm.Set2
ax.stackplot(x, *ys, baseline='sym',
             colors=[cmap(i/n_series) for i in range(n_series)],
             alpha=0.85)
ax.set_title('Stream Graph (Symmetric Baseline)')
ax.set_xlabel('Time'); ax.set_ylabel('Magnitude')
ax.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig('streamgraph.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved streamgraph.png')"""},
    ],
    "Energy Mix Dashboard",
    "Show a country's electricity generation mix (Solar, Wind, Hydro, Gas, Coal) over 12 months as a 100% stacked area chart. Annotate the month with highest renewable share.",
    HDR + """\
np.random.seed(15)
months = np.arange(12)
solar = 20 + 15*np.sin(np.linspace(0, np.pi, 12)) + np.random.randn(12)*2
wind  = 18 + 8*np.cos(np.linspace(0, 2*np.pi, 12)) + np.random.randn(12)*2
hydro = np.full(12, 22.0) + np.random.randn(12)
gas   = 25 - 5*np.sin(np.linspace(0, np.pi, 12)) + np.random.randn(12)
coal  = 100 - solar - wind - hydro - gas
sources = np.vstack([solar, wind, hydro, gas, coal])
sources = np.clip(sources, 1, None)
pct = sources / sources.sum(axis=0) * 100

fig, ax = plt.subplots(figsize=(10, 5))
mnames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
ax.stackplot(months, *pct,
             labels=['Solar','Wind','Hydro','Gas','Coal'],
             colors=['#f9c74f','#90be6d','#43aa8b','#f3722c','#555'],
             alpha=0.9)
ren = pct[:3].sum(axis=0)
best = ren.argmax()
ax.annotate(f'Peak renewable\n{ren[best]:.1f}%',
            xy=(best, 50), xytext=(best+1, 70),
            arrowprops=dict(arrowstyle='->', color='white'),
            fontsize=9, color='white',
            bbox=dict(boxstyle='round', fc='#333'))
ax.set_xticks(months); ax.set_xticklabels(mnames)
ax.set_ylim(0,100); ax.set_ylabel('Share (%)')
ax.set_title('Energy Mix by Month', fontweight='bold')
ax.legend(loc='lower right', ncol=5, fontsize=8)
fig.tight_layout()
fig.savefig('energy_mix.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved energy_mix.png')""",
    "Stacked Chart Practice",
    "Create weekly budget allocation data for 5 weeks across categories: Rent, Food, Transport, Entertainment, Savings (make up reasonable values). Plot a stacked bar chart and below it a 100% stacked bar showing the proportion. Use a shared x-axis in a 2x1 subplot.",
    HDR + """\
weeks = ['Wk1','Wk2','Wk3','Wk4','Wk5']
rent    = np.array([800, 800, 800, 800, 800])
food    = np.array([200, 220, 180, 240, 210])
transport = np.array([80, 90, 75, 85, 95])
entertainment = np.array([100, 60, 120, 80, 50])
savings = np.array([150, 200, 180, 130, 220])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
x = np.arange(len(weeks))
# TODO: stacked bar on ax1
# TODO: 100% stacked bar on ax2
# TODO: legend, labels, title
fig.tight_layout()
fig.savefig('budget_stacked.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved budget_stacked.png')"""
)

# ── Section 22: Step Plots & Eventplot ────────────────────────────────────────
s22 = make_mpl(
    22, "Step Plots & Eventplot",
    "Use step() and drawstyle='steps-*' for discrete/piecewise data, stairs() for histograms, and eventplot() for spike-train and event sequence data.",
    [
        {"label": "step() and stairs() basics", "code": HDR + """\
x = np.arange(0, 10)
y = np.array([2, 3, 3, 5, 4, 6, 5, 7, 6, 8])

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, where, title in zip(axes,
                             ['pre','mid','post'],
                             ['steps-pre','steps-mid','steps-post']):
    ax.step(x, y, where=where, color='steelblue', linewidth=2)
    ax.scatter(x, y, color='steelblue', zorder=5)
    ax.set_title(title); ax.grid(True, alpha=0.3)
fig.suptitle('Step Plot Variants', fontweight='bold')
fig.tight_layout()
fig.savefig('step_variants.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved step_variants.png')"""},
        {"label": "Cumulative step (ECDF-style)", "code": HDR + """\
np.random.seed(0)
data = np.sort(np.random.normal(5, 1.5, 200))
ecdf_y = np.arange(1, len(data)+1) / len(data)

fig, ax = plt.subplots(figsize=(8, 4))
ax.step(data, ecdf_y, where='post', color='steelblue', linewidth=2, label='ECDF')
ax.axhline(0.5, color='red', linestyle='--', linewidth=1, label='Median')
ax.axvline(np.median(data), color='red', linestyle='--', linewidth=1)
ax.set_xlabel('Value'); ax.set_ylabel('Cumulative Probability')
ax.set_title('Empirical CDF (step-post)')
ax.legend(); ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('ecdf_step.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved ecdf_step.png')"""},
        {"label": "Eventplot: neural spike trains", "code": HDR + """\
np.random.seed(1)
n_neurons = 5
spike_trains = [np.sort(np.random.uniform(0, 1, np.random.randint(10, 30)))
                for _ in range(n_neurons)]
colors_ev = plt.cm.tab10(np.linspace(0, 0.5, n_neurons))

fig, ax = plt.subplots(figsize=(10, 4))
ax.eventplot(spike_trains, colors=colors_ev,
             lineoffsets=range(1, n_neurons+1),
             linelengths=0.7, linewidths=1.5)
ax.set_xlabel('Time (s)')
ax.set_yticks(range(1, n_neurons+1))
ax.set_yticklabels([f'Neuron {i}' for i in range(1, n_neurons+1)])
ax.set_title('Neural Spike Train Raster Plot')
ax.set_xlim(0, 1)
ax.grid(True, axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig('spike_raster.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved spike_raster.png')"""},
        {"label": "Step with fill for discrete signal", "code": HDR + """\
np.random.seed(2)
t = np.arange(0, 50)
signal = np.where(np.random.rand(50) > 0.6, 1, 0)
signal[10:15] = 1; signal[30:38] = 1  # force some pulses

fig, ax = plt.subplots(figsize=(10, 3))
ax.step(t, signal, where='post', color='steelblue', linewidth=1.5)
ax.fill_between(t, signal, step='post', alpha=0.2, color='steelblue')
ax.set_ylim(-0.1, 1.4)
ax.set_xlabel('Time (ms)'); ax.set_ylabel('State')
ax.set_title('Digital Signal — Step Fill')
ax.set_yticks([0, 1]); ax.set_yticklabels(['OFF', 'ON'])
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('digital_signal.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved digital_signal.png')"""},
    ],
    "System Event Log Visualization",
    "Visualize server events across 5 services over 60 seconds: each service fires random events. Use eventplot with different colors per service and add a shaded incident window (t=20–35).",
    HDR + """\
np.random.seed(8)
services = ['API','DB','Cache','Auth','Queue']
events = [np.sort(np.random.uniform(0, 60, np.random.randint(8, 25)))
          for _ in services]
colors_svc = ['#4c72b0','#dd8452','#55a868','#c44e52','#9467bd']

fig, ax = plt.subplots(figsize=(11, 4))
ax.eventplot(events, colors=colors_svc,
             lineoffsets=range(1, len(services)+1),
             linelengths=0.6, linewidths=2)
ax.axvspan(20, 35, color='red', alpha=0.1, label='Incident window')
ax.axvline(20, color='red', linestyle='--', linewidth=1)
ax.axvline(35, color='red', linestyle='--', linewidth=1)
ax.set_xlabel('Time (s)'); ax.set_xlim(0, 60)
ax.set_yticks(range(1, len(services)+1)); ax.set_yticklabels(services)
ax.set_title('Service Event Log — 60s Window', fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig('event_log.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved event_log.png')""",
    "Step Plot Practice",
    "Simulate a 3-state machine (IDLE=0, RUNNING=1, ERROR=2) over 80 time steps using random transitions. Plot it with step(where='post') and fill_between for each state using different colors. Add a legend for the three states.",
    HDR + """\
np.random.seed(11)
t = np.arange(80)
state = np.zeros(80, dtype=int)
for i in range(1, 80):
    if np.random.rand() < 0.1:
        state[i] = np.random.choice([0, 1, 2])
    else:
        state[i] = state[i-1]

fig, ax = plt.subplots(figsize=(11, 3))
# TODO: step plot with post
# TODO: fill_between for state=0 (blue), 1 (green), 2 (red)
# TODO: add legend, labels, title
# TODO: save 'state_machine.png'
plt.close()"""
)

# ── Section 23: Log Scale & Symlog ────────────────────────────────────────────
s23 = make_mpl(
    23, "Log Scale & Symlog",
    "Use set_xscale/set_yscale with 'log', 'symlog', or 'logit' to handle data spanning many orders of magnitude.",
    [
        {"label": "Log-log plot: power-law relationship", "code": HDR + """\
x = np.logspace(0, 4, 100)
y_power = 2.5 * x**1.7
noise = np.random.lognormal(0, 0.1, 100)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(x, y_power * noise, 'o', markersize=4, alpha=0.6, color='steelblue')
ax1.set_title('Linear Scale'); ax1.set_xlabel('x'); ax1.set_ylabel('y')
ax1.grid(True, alpha=0.3)

ax2.loglog(x, y_power * noise, 'o', markersize=4, alpha=0.6, color='steelblue')
ax2.loglog(x, y_power, 'r--', linewidth=2, label=r'y = 2.5 x^{1.7}')
ax2.set_title('Log-Log Scale'); ax2.set_xlabel('x'); ax2.set_ylabel('y')
ax2.legend(); ax2.grid(True, which='both', alpha=0.3)
fig.suptitle('Power-Law: Linear vs Log-Log', fontweight='bold')
fig.tight_layout()
fig.savefig('loglog.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved loglog.png')"""},
        {"label": "Semilog: exponential decay", "code": HDR + """\
t = np.linspace(0, 10, 200)
decay_fast = np.exp(-0.8 * t)
decay_slow = np.exp(-0.2 * t)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
for ax, scale, title in [(ax1, 'linear', 'Linear Y'), (ax2, 'log', 'Log Y')]:
    ax.plot(t, decay_fast, label='Fast (k=0.8)', linewidth=2)
    ax.plot(t, decay_slow, label='Slow (k=0.2)', linewidth=2, linestyle='--')
    ax.set_yscale(scale)
    ax.set_xlabel('Time'); ax.set_ylabel('Concentration')
    ax.set_title(title); ax.legend(); ax.grid(True, which='both', alpha=0.3)
fig.suptitle('Exponential Decay on Linear vs Semilog', fontweight='bold')
fig.tight_layout()
fig.savefig('semilog.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved semilog.png')"""},
        {"label": "Symlog: signed data spanning zero", "code": HDR + """\
np.random.seed(0)
x = np.linspace(-1000, 1000, 500)
y = x + np.random.randn(500) * 50

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.scatter(x, y, s=8, alpha=0.5, color='steelblue')
ax1.set_title('Linear Scale')

ax2.scatter(x, y, s=8, alpha=0.5, color='steelblue')
ax2.set_xscale('symlog', linthresh=10)
ax2.set_yscale('symlog', linthresh=10)
ax2.set_title('Symlog Scale (linthresh=10)')

for ax in (ax1, ax2):
    ax.axhline(0, color='gray', linewidth=0.8)
    ax.axvline(0, color='gray', linewidth=0.8)
    ax.grid(True, which='both', alpha=0.3)
    ax.set_xlabel('X'); ax.set_ylabel('Y')
fig.tight_layout()
fig.savefig('symlog.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved symlog.png')"""},
        {"label": "Log scale with minor grid and custom ticks", "code": HDR + """\
import matplotlib.ticker as ticker

f = np.logspace(1, 5, 300)  # 10 Hz to 100 kHz
gain_db = -20 * np.log10(1 + (f/1000)**2)  # simple LP filter

fig, ax = plt.subplots(figsize=(9, 4))
ax.semilogx(f, gain_db, color='steelblue', linewidth=2)
ax.axhline(-3, color='red', linestyle='--', linewidth=1, label='-3 dB cutoff')
ax.axvline(1000, color='red', linestyle='--', linewidth=1)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Gain (dB)')
ax.set_title('Bode Plot — Low-Pass Filter')
ax.grid(True, which='both', alpha=0.3)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(
    lambda x, _: f'{x/1000:.0f}k' if x >= 1000 else f'{x:.0f}'))
ax.legend()
fig.tight_layout()
fig.savefig('bode.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved bode.png')"""},
    ],
    "Server Response Time Analysis",
    "Plot server response time distribution (lognormal data, 10k samples) on both linear and log-x histograms side by side. Overlay the theoretical lognormal PDF. Mark the 95th and 99th percentiles.",
    HDR + """\
np.random.seed(42)
mu, sigma = 5.5, 0.8   # lognormal params
data = np.random.lognormal(mu, sigma, 10000)  # ms

p95, p99 = np.percentile(data, [95, 99])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
bins = 80

ax1.hist(data, bins=bins, color='steelblue', alpha=0.7, density=True)
for p, lab, col in [(p95,'p95','orange'),(p99,'p99','red')]:
    ax1.axvline(p, color=col, linestyle='--', linewidth=2, label=f'{lab}: {p:.0f}ms')
ax1.set_title('Linear Scale'); ax1.legend(); ax1.grid(True, alpha=0.3)

ax2.hist(data, bins=np.logspace(np.log10(data.min()), np.log10(data.max()), bins),
         color='steelblue', alpha=0.7, density=True)
x_pdf = np.logspace(np.log10(data.min()), np.log10(data.max()), 300)
pdf = (1/(x_pdf * sigma * np.sqrt(2*np.pi))) * np.exp(-(np.log(x_pdf)-mu)**2/(2*sigma**2))
ax2.plot(x_pdf, pdf, 'r-', linewidth=2, label='Lognormal PDF')
ax2.set_xscale('log')
for p, lab, col in [(p95,'p95','orange'),(p99,'p99','red')]:
    ax2.axvline(p, color=col, linestyle='--', linewidth=2)
ax2.set_title('Log-X Scale'); ax2.legend(); ax2.grid(True, which='both', alpha=0.3)

for ax in (ax1, ax2):
    ax.set_xlabel('Response Time (ms)'); ax.set_ylabel('Density')
fig.suptitle('Server Response Time Distribution', fontweight='bold')
fig.tight_layout()
fig.savefig('response_time.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved response_time.png')""",
    "Log Scale Practice",
    "Generate data: y = 3 * x^(-1.5) for x in [1, 10000] with lognormal noise. Plot on: (1) linear scale, (2) log-log scale with a fitted power-law line, (3) symlog scale. Arrange in a 1x3 figure. Use np.polyfit on log-transformed data to get the exponent.",
    HDR + """\
np.random.seed(6)
x = np.logspace(0, 4, 200)
y = 3 * x**(-1.5) * np.random.lognormal(0, 0.15, 200)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
titles = ['Linear', 'Log-Log', 'Symlog']
scales = [('linear','linear'), ('log','log'), ('symlog','symlog')]

for ax, title, (xs, ys) in zip(axes, titles, scales):
    ax.scatter(x, y, s=10, alpha=0.5)
    ax.set_xscale(xs); ax.set_yscale(ys)
    ax.set_title(title); ax.grid(True, which='both', alpha=0.3)
    # TODO: on log-log, add fitted power-law line using np.polyfit

fig.suptitle('Power Law on Three Scales', fontweight='bold')
fig.tight_layout()
fig.savefig('powerlaw_scales.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved powerlaw_scales.png')"""
)

# ── Section 24: GridSpec & Complex Layouts ────────────────────────────────────
s24 = make_mpl(
    24, "GridSpec & Complex Layouts",
    "Go beyond plt.subplots() using GridSpec for unequal column/row spans, subplot_mosaic() for named panels, and add_axes() for insets.",
    [
        {"label": "GridSpec: unequal column widths", "code": HDR + """\
from matplotlib.gridspec import GridSpec

np.random.seed(0)
fig = plt.figure(figsize=(11, 5))
gs = GridSpec(2, 3, figure=fig, width_ratios=[2,1,1], hspace=0.4, wspace=0.3)

ax_main = fig.add_subplot(gs[:, 0])   # spans both rows, col 0
ax_tr   = fig.add_subplot(gs[0, 1])
ax_br   = fig.add_subplot(gs[1, 1])
ax_tall = fig.add_subplot(gs[:, 2])

x = np.random.randn(200); y = np.random.randn(200)
ax_main.scatter(x, y, s=15, alpha=0.5, color='steelblue')
ax_main.set_title('Main Scatter')
ax_tr.hist(x, bins=20, color='steelblue', alpha=0.7); ax_tr.set_title('X dist')
ax_br.hist(y, bins=20, orientation='horizontal', color='tomato', alpha=0.7)
ax_br.set_title('Y dist')
ax_tall.boxplot([x, y], labels=['X','Y'], patch_artist=True)
ax_tall.set_title('Box')

fig.suptitle('GridSpec Complex Layout', fontweight='bold')
fig.savefig('gridspec.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved gridspec.png')"""},
        {"label": "subplot_mosaic: named panels", "code": HDR + """\
np.random.seed(1)
layout = [['A', 'A', 'B'],
          ['C', 'D', 'B']]

fig, axd = plt.subplot_mosaic(layout, figsize=(11, 6),
                               gridspec_kw={'hspace':0.35,'wspace':0.3})

x = np.linspace(0, 10, 100)
axd['A'].plot(x, np.sin(x), color='steelblue'); axd['A'].set_title('A: Wide Line')
axd['B'].imshow(np.random.rand(20,20), cmap='viridis', aspect='auto'); axd['B'].set_title('B: Tall Image')
axd['C'].bar(['x','y','z'], [3,7,5], color=['#4c72b0','#dd8452','#55a868']); axd['C'].set_title('C: Bar')
axd['D'].scatter(*np.random.randn(2,50), s=20, alpha=0.6); axd['D'].set_title('D: Scatter')

fig.suptitle('subplot_mosaic — Named Panels', fontweight='bold')
fig.savefig('mosaic.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved mosaic.png')"""},
        {"label": "Nested GridSpec for subgrid", "code": HDR + """\
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

np.random.seed(2)
fig = plt.figure(figsize=(11, 6))
outer = GridSpec(1, 2, figure=fig, wspace=0.3)

# Left: single scatter
ax_left = fig.add_subplot(outer[0])
ax_left.scatter(*np.random.randn(2, 80), s=20, alpha=0.5)
ax_left.set_title('Left Panel')

# Right: 2x2 subgrid
inner = GridSpecFromSubplotSpec(2, 2, subplot_spec=outer[1], hspace=0.4, wspace=0.3)
for i in range(4):
    ax = fig.add_subplot(inner[i])
    ax.plot(np.random.randn(30).cumsum(), linewidth=1.5)
    ax.set_title(f'R{i+1}', fontsize=9)

fig.suptitle('Nested GridSpec', fontweight='bold')
fig.savefig('nested_gs.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved nested_gs.png')"""},
        {"label": "Inset axis with add_axes", "code": HDR + """\
np.random.seed(3)
x = np.linspace(0, 10, 300)
y = np.sin(x) * np.exp(-0.2*x) + np.random.randn(300)*0.05

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(x, y, color='steelblue', linewidth=1.5)
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_title('Main Plot with Inset Zoom')

# Inset: zoom [0, 1.5]
ax_inset = ax.inset_axes([0.55, 0.55, 0.42, 0.38])
ax_inset.plot(x, y, color='steelblue', linewidth=1.5)
ax_inset.set_xlim(0, 1.5); ax_inset.set_ylim(-0.1, 1.05)
ax_inset.set_title('Zoom [0,1.5]', fontsize=8)
ax_inset.tick_params(labelsize=7)

ax.indicate_inset_zoom(ax_inset, edgecolor='black')
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('inset_axis.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved inset_axis.png')"""},
    ],
    "ML Model Comparison Dashboard",
    "Build a 3-panel dashboard: (1) large training-curve plot (loss vs epoch for 3 models), (2) confusion-matrix heatmap, (3) ROC curve — using GridSpec with a 2:1 width ratio for the first column.",
    HDR + """\
from matplotlib.gridspec import GridSpec

np.random.seed(42)
fig = plt.figure(figsize=(13, 5))
gs = GridSpec(2, 2, figure=fig, width_ratios=[1.8, 1], hspace=0.4, wspace=0.35)

ax_curve = fig.add_subplot(gs[:, 0])
ax_cm    = fig.add_subplot(gs[0, 1])
ax_roc   = fig.add_subplot(gs[1, 1])

# Training curves
epochs = np.arange(1, 31)
for name, color, offset in [('CNN','#4c72b0',0), ('RNN','#dd8452',0.3), ('MLP','#55a868',0.5)]:
    loss = 2.5*np.exp(-0.15*epochs) + offset*np.exp(-0.1*epochs) + np.random.randn(30)*0.04
    ax_curve.plot(epochs, loss, color=color, linewidth=2, label=name)
ax_curve.set_xlabel('Epoch'); ax_curve.set_ylabel('Loss')
ax_curve.set_title('Training Loss'); ax_curve.legend(); ax_curve.grid(True, alpha=0.3)

# Confusion matrix
cm = np.array([[45,5,2],[3,38,4],[1,2,50]])
im = ax_cm.imshow(cm, cmap='Blues')
for i in range(3):
    for j in range(3):
        ax_cm.text(j, i, cm[i,j], ha='center', va='center',
                   color='white' if cm[i,j] > 30 else 'black', fontsize=10)
ax_cm.set_title('Confusion Matrix', fontsize=9)

# ROC
fpr = np.linspace(0, 1, 100)
tpr = np.sqrt(fpr) * 0.92
ax_roc.plot(fpr, tpr, color='steelblue', linewidth=2, label='AUC=0.92')
ax_roc.plot([0,1],[0,1],'k--',linewidth=0.8)
ax_roc.set_xlabel('FPR', fontsize=8); ax_roc.set_ylabel('TPR', fontsize=8)
ax_roc.set_title('ROC Curve', fontsize=9); ax_roc.legend(fontsize=8)

fig.suptitle('ML Model Comparison Dashboard', fontweight='bold')
fig.savefig('ml_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved ml_dashboard.png')""",
    "GridSpec Practice",
    "Create a 3x3 GridSpec layout where: cell (0,0) spans 2 columns (title/text placeholder), row 1 has 3 equal plots (sin, cos, tan clipped), and row 2 spans all 3 columns as a wide bar chart. Use fig.add_subplot() with appropriate slicing.",
    HDR + """\
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.3)
x = np.linspace(0, 2*np.pi, 200)

# Row 0: spans 3 cols — title area
ax_title = fig.add_subplot(gs[0, :])
ax_title.text(0.5, 0.5, 'GridSpec Practice Dashboard', ha='center', va='center',
              fontsize=14, fontweight='bold', transform=ax_title.transAxes)
ax_title.axis('off')

# TODO: Row 1: three plots (sin, cos, tan clipped to [-5,5])
# TODO: Row 2: wide bar chart spanning all 3 cols
# TODO: save 'gridspec_practice.png'
plt.close()"""
)


# ── Assemble and insert ───────────────────────────────────────────────────────
all_sections = s17 + s18 + s19 + s20 + s21 + s22 + s23 + s24
result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: matplotlib sections 17-24 added")
else:
    print("FAILED")
