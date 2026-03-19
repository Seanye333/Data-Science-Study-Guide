"""Add Matplotlib sections 25-32 to gen_matplotlib.py"""
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

# ── Section 25: Hexbin & 2D Density Plots ────────────────────────────────────
s25 = make_mpl(
    25, "Hexbin & 2D Density Plots",
    "Use hexbin() for large scatter datasets, hist2d() for rectangular binning, and KDE-based density coloring to visualize joint distributions.",
    [
        {"label": "hexbin with colorbar", "code": HDR + """\
np.random.seed(0)
n = 5000
x = np.random.normal(0, 1.5, n)
y = 0.6*x + np.random.normal(0, 1, n)

fig, ax = plt.subplots(figsize=(7, 5))
hb = ax.hexbin(x, y, gridsize=40, cmap='YlOrRd', mincnt=1)
cb = fig.colorbar(hb, ax=ax, label='Count')
ax.set_xlabel('X'); ax.set_ylabel('Y')
ax.set_title('Hexbin — 5000 Points')
fig.tight_layout()
fig.savefig('hexbin.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved hexbin.png')"""},
        {"label": "2D histogram with hist2d", "code": HDR + """\
np.random.seed(1)
n = 3000
x = np.concatenate([np.random.normal(-2, 0.8, n//2), np.random.normal(2, 0.8, n//2)])
y = np.concatenate([np.random.normal(-1, 1.0, n//2), np.random.normal(1, 1.0, n//2)])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
h, xedges, yedges, img = ax1.hist2d(x, y, bins=40, cmap='Blues')
fig.colorbar(img, ax=ax1, label='Count')
ax1.set_title('hist2d')

h2, xe, ye, img2 = ax2.hist2d(x, y, bins=40, cmap='Blues',
                                norm=plt.matplotlib.colors.LogNorm())
fig.colorbar(img2, ax=ax2, label='Log Count')
ax2.set_title('hist2d (log scale)')

for ax in (ax1, ax2):
    ax.set_xlabel('X'); ax.set_ylabel('Y')
fig.tight_layout()
fig.savefig('hist2d.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved hist2d.png')"""},
        {"label": "Scatter colored by KDE density", "code": HDR + """\
from scipy.stats import gaussian_kde

np.random.seed(2)
n = 2000
x = np.random.multivariate_normal([0,0], [[1,0.7],[0.7,1]], n)[:,0]
y = np.random.multivariate_normal([0,0], [[1,0.7],[0.7,1]], n)[:,1]

xy = np.vstack([x, y])
kde = gaussian_kde(xy)
density = kde(xy)
idx = density.argsort()

fig, ax = plt.subplots(figsize=(7, 6))
sc = ax.scatter(x[idx], y[idx], c=density[idx], cmap='inferno', s=10, alpha=0.8)
fig.colorbar(sc, ax=ax, label='Density')
ax.set_xlabel('X'); ax.set_ylabel('Y')
ax.set_title('Scatter Colored by KDE Density')
fig.tight_layout()
fig.savefig('kde_scatter.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved kde_scatter.png')"""},
        {"label": "Marginal distributions with shared axes", "code": HDR + """\
from matplotlib.gridspec import GridSpec

np.random.seed(3)
n = 1000
x = np.random.normal(0, 1, n)
y = x * 0.8 + np.random.normal(0, 0.6, n)

fig = plt.figure(figsize=(8, 8))
gs = GridSpec(2, 2, width_ratios=[4,1], height_ratios=[1,4],
              hspace=0.05, wspace=0.05)
ax_main = fig.add_subplot(gs[1, 0])
ax_top  = fig.add_subplot(gs[0, 0], sharex=ax_main)
ax_side = fig.add_subplot(gs[1, 1], sharey=ax_main)

ax_main.hexbin(x, y, gridsize=35, cmap='Blues', mincnt=1)
ax_top.hist(x, bins=40, color='steelblue', alpha=0.7)
ax_side.hist(y, bins=40, orientation='horizontal', color='tomato', alpha=0.7)

plt.setp(ax_top.get_xticklabels(), visible=False)
plt.setp(ax_side.get_yticklabels(), visible=False)
ax_main.set_xlabel('X'); ax_main.set_ylabel('Y')
ax_top.set_title('Hexbin with Marginal Distributions', fontweight='bold')
fig.savefig('marginal.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved marginal.png')"""},
    ],
    "Customer Purchase Patterns",
    "Visualize 20,000 e-commerce transactions (basket_size vs revenue) using hexbin with log-color scale. Add marginal histograms on top and right for each axis. Annotate the high-density region.",
    HDR + """\
from matplotlib.gridspec import GridSpec

np.random.seed(55)
n = 20000
basket = np.random.lognormal(1.5, 0.6, n)
revenue = basket * np.random.uniform(15, 80, n) + np.random.normal(0, 20, n)
revenue = np.clip(revenue, 1, None)

fig = plt.figure(figsize=(9, 9))
gs = GridSpec(2, 2, width_ratios=[4,1], height_ratios=[1,4],
              hspace=0.05, wspace=0.05)
ax = fig.add_subplot(gs[1,0])
ax_top = fig.add_subplot(gs[0,0], sharex=ax)
ax_side = fig.add_subplot(gs[1,1], sharey=ax)

hb = ax.hexbin(basket, revenue, gridsize=50, cmap='YlOrRd', mincnt=1,
               norm=plt.matplotlib.colors.LogNorm())
fig.colorbar(hb, ax=ax, label='Log Count')

ax_top.hist(basket, bins=50, color='#f4a261', alpha=0.8)
ax_side.hist(revenue, bins=50, orientation='horizontal', color='#e76f51', alpha=0.8)
plt.setp(ax_top.get_xticklabels(), visible=False)
plt.setp(ax_side.get_yticklabels(), visible=False)

ax.set_xlabel('Basket Size (items)'); ax.set_ylabel('Revenue ($)')
ax.annotate('Peak density', xy=(5, 200), xytext=(12, 500),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=9, fontweight='bold')
ax_top.set_title('Customer Purchase Patterns', fontweight='bold')
fig.savefig('purchase_density.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved purchase_density.png')""",
    "Density Plot Practice",
    "Generate 3000 points from a mixture of 3 bivariate Gaussians at (0,0), (3,3), (-2,3). Plot using hexbin (gridsize=30, cmap='plasma'). Overlay contour lines from a KDE. Add a colorbar and axis labels.",
    HDR + """\
from scipy.stats import gaussian_kde

np.random.seed(7)
centers = [(0,0), (3,3), (-2,3)]
n_each = 1000
pts = np.vstack([np.random.multivariate_normal(c, np.eye(2), n_each) for c in centers])
x, y = pts[:,0], pts[:,1]

fig, ax = plt.subplots(figsize=(7, 6))
# TODO: hexbin with plasma cmap
# TODO: KDE contour overlay
# TODO: colorbar, axis labels
# TODO: save 'mixture_density.png'
plt.close()"""
)

# ── Section 26: Patch Artists & Custom Shapes ─────────────────────────────────
s26 = make_mpl(
    26, "Patch Artists & Custom Shapes",
    "Draw custom geometric shapes with matplotlib.patches: Rectangle, Circle, Ellipse, Polygon, FancyArrow, and Arc for annotations and diagrams.",
    [
        {"label": "Basic patches: Rectangle, Circle, Ellipse", "code": HDR + """\
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10); ax.set_ylim(0, 8)
ax.set_aspect('equal')

rect = mpatches.Rectangle((1, 1), 2.5, 1.5, linewidth=2,
                            edgecolor='steelblue', facecolor='lightblue', alpha=0.8)
circ = mpatches.Circle((6, 4), radius=1.5, linewidth=2,
                         edgecolor='tomato', facecolor='lightsalmon', alpha=0.8)
ellip = mpatches.Ellipse((4, 6), width=3, height=1.2, angle=30,
                           linewidth=2, edgecolor='seagreen', facecolor='lightgreen', alpha=0.8)

for patch in [rect, circ, ellip]:
    ax.add_patch(patch)

ax.text(2.25, 1.75, 'Rectangle', ha='center', fontsize=9)
ax.text(6, 4, 'Circle', ha='center', fontsize=9)
ax.text(4, 6, 'Ellipse', ha='center', fontsize=9)
ax.set_title('Basic Patch Artists')
ax.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig('patches_basic.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved patches_basic.png')"""},
        {"label": "Polygon and FancyArrow", "code": HDR + """\
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10); ax.set_ylim(0, 8)
ax.set_aspect('equal')

# Star polygon
n = 5
outer = np.array([[np.cos(2*np.pi*i/n - np.pi/2), np.sin(2*np.pi*i/n - np.pi/2)]
                   for i in range(n)]) * 2.0 + [3, 4]
inner = np.array([[np.cos(2*np.pi*i/n + np.pi/n - np.pi/2),
                   np.sin(2*np.pi*i/n + np.pi/n - np.pi/2)]
                   for i in range(n)]) * 0.8 + [3, 4]
verts = np.empty((2*n, 2))
verts[0::2] = outer; verts[1::2] = inner
star = mpatches.Polygon(verts, closed=True, facecolor='gold', edgecolor='orange', linewidth=2)
ax.add_patch(star)

arrow = mpatches.FancyArrow(5.5, 4, 2, 0, width=0.3,
                              head_width=0.7, head_length=0.5,
                              facecolor='steelblue', edgecolor='navy')
ax.add_patch(arrow)

arc = mpatches.Arc((8.5, 2), 2, 2, angle=0, theta1=30, theta2=270,
                    color='tomato', linewidth=2.5)
ax.add_patch(arc)

ax.set_title('Polygon, FancyArrow, Arc')
ax.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig('patches_advanced.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved patches_advanced.png')"""},
        {"label": "Annotate with FancyBboxPatch callouts", "code": HDR + """\
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(9, 5))
np.random.seed(0)
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.randn(100)*0.1
ax.plot(x, y, color='steelblue', linewidth=2)

# Highlight a region
highlight = mpatches.FancyBboxPatch((3.0, -0.3), 2.0, 0.6,
    boxstyle='round,pad=0.1', linewidth=2,
    edgecolor='gold', facecolor='yellow', alpha=0.3)
ax.add_patch(highlight)
ax.annotate('Peak region', xy=(4, 0.8), xytext=(6.5, 1.3),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=2),
            fontsize=11, color='darkred', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gold'))

ax.set_title('Annotations with FancyBboxPatch')
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('fancy_annotate.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved fancy_annotate.png')"""},
        {"label": "Pipeline / flowchart diagram", "code": HDR + """\
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(11, 4))
ax.set_xlim(0, 11); ax.set_ylim(0, 4)
ax.set_aspect('equal'); ax.axis('off')

boxes = [
    (0.5, 1.5, 'Data\nIngestion', '#4c72b0'),
    (3.0, 1.5, 'Clean &\nTransform', '#dd8452'),
    (5.5, 1.5, 'Feature\nEngineering', '#55a868'),
    (8.0, 1.5, 'Model\nTraining', '#c44e52'),
]
for x, y, label, color in boxes:
    box = mpatches.FancyBboxPatch((x, y), 2, 1,
        boxstyle='round,pad=0.1', facecolor=color, edgecolor='white',
        linewidth=2, alpha=0.9)
    ax.add_patch(box)
    ax.text(x+1, y+0.5, label, ha='center', va='center',
            color='white', fontsize=9, fontweight='bold')

for i in range(len(boxes)-1):
    x_start = boxes[i][0] + 2
    x_end   = boxes[i+1][0]
    y_mid   = 2.0
    ax.annotate('', xy=(x_end, y_mid), xytext=(x_start, y_mid),
                arrowprops=dict(arrowstyle='->', color='gray', lw=2))

ax.set_title('ML Pipeline Diagram', fontsize=13, fontweight='bold', y=0.95)
fig.tight_layout()
fig.savefig('pipeline.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved pipeline.png')"""},
    ],
    "Architecture Diagram",
    "Draw a 3-tier architecture diagram: Client (circle), Load Balancer (diamond/hexagon), 3 App Servers (rounded rectangles), Database (cylinder-style ellipse). Use FancyArrow for connections and add labels.",
    HDR + """\
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(0, 12); ax.set_ylim(0, 7)
ax.axis('off')

# Client
circ = mpatches.Circle((1, 3.5), 0.7, facecolor='#4c72b0', edgecolor='white', lw=2)
ax.add_patch(circ); ax.text(1, 3.5, 'Client', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# Load balancer
lb = mpatches.FancyBboxPatch((2.8, 2.8), 2, 1.4, boxstyle='round,pad=0.15',
    facecolor='#dd8452', edgecolor='white', lw=2)
ax.add_patch(lb); ax.text(3.8, 3.5, 'Load\nBalancer', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# App servers
for i, (y, col) in enumerate(zip([1.2, 3.5, 5.8], ['#55a868','#55a868','#55a868'])):
    srv = mpatches.FancyBboxPatch((6.5, y), 1.8, 1.0, boxstyle='round,pad=0.1',
        facecolor=col, edgecolor='white', lw=2)
    ax.add_patch(srv)
    ax.text(7.4, y+0.5, f'App {i+1}', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
    ax.annotate('', xy=(6.5, y+0.5), xytext=(4.8, 3.5),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

# DB
db = mpatches.Ellipse((10.5, 3.5), 1.4, 0.9, facecolor='#c44e52', edgecolor='white', lw=2)
ax.add_patch(db); ax.text(10.5, 3.5, 'DB', ha='center', va='center', color='white', fontsize=9, fontweight='bold')
for y in [1.7, 3.5, 6.3]:
    ax.annotate('', xy=(9.8, 3.5), xytext=(8.3, y+0.5 if y != 3.5 else y),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.2))

ax.annotate('', xy=(2.8, 3.5), xytext=(1.7, 3.5),
            arrowprops=dict(arrowstyle='->', color='gray', lw=2))
ax.set_title('3-Tier Architecture Diagram', fontsize=13, fontweight='bold')
fig.tight_layout()
fig.savefig('architecture.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved architecture.png')""",
    "Custom Shape Practice",
    "Draw a Venn diagram of 3 overlapping circles with labels A, B, C and intersection labels (A∩B, B∩C, A∩C, A∩B∩C). Use Circle patches with alpha=0.4 and contrasting colors. Place text annotations in each region.",
    HDR + """\
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(7, 6))
ax.set_xlim(0, 7); ax.set_ylim(0, 7)
ax.set_aspect('equal'); ax.axis('off')

# Three overlapping circles
circles = [
    mpatches.Circle((2.8, 4.2), 2, facecolor='#4c72b0', alpha=0.35, edgecolor='navy', lw=2),
    mpatches.Circle((4.2, 4.2), 2, facecolor='#dd8452', alpha=0.35, edgecolor='darkred', lw=2),
    mpatches.Circle((3.5, 2.5), 2, facecolor='#55a868', alpha=0.35, edgecolor='darkgreen', lw=2),
]
for c in circles: ax.add_patch(c)

# TODO: add text labels A, B, C in non-overlapping regions
# TODO: add intersection labels A∩B, B∩C, A∩C, A∩B∩C
# TODO: add title and save 'venn3.png'
plt.close()"""
)

# ── Section 27: Quiver & Streamplot ──────────────────────────────────────────
s27 = make_mpl(
    27, "Quiver & Streamplot",
    "Visualize 2D vector fields with quiver() for arrow grids and streamplot() for continuous flow lines. Used for fluid dynamics, electric fields, and gradient maps.",
    [
        {"label": "Basic quiver plot", "code": HDR + """\
x = y = np.linspace(-2, 2, 15)
X, Y = np.meshgrid(x, y)
U = -Y      # velocity components
V =  X

fig, ax = plt.subplots(figsize=(6, 6))
q = ax.quiver(X, Y, U, V, np.sqrt(U**2+V**2),
              cmap='coolwarm', scale=30, pivot='mid')
fig.colorbar(q, ax=ax, label='Speed')
ax.set_title('Rotational Vector Field')
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_aspect('equal')
ax.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig('quiver_basic.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved quiver_basic.png')"""},
        {"label": "Streamplot with speed coloring", "code": HDR + """\
x = np.linspace(-3, 3, 100)
y = np.linspace(-2, 2, 80)
X, Y = np.meshgrid(x, y)
U = 1 - X**2
V = -Y

speed = np.sqrt(U**2 + V**2)

fig, ax = plt.subplots(figsize=(9, 5))
strm = ax.streamplot(X, Y, U, V, color=speed, cmap='plasma',
                      linewidth=1.5, density=1.5, arrowsize=1.2)
fig.colorbar(strm.lines, ax=ax, label='Speed')
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_title('Streamplot: Flow Field Colored by Speed')
ax.set_aspect('equal')
ax.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig('streamplot.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved streamplot.png')"""},
        {"label": "Gradient field of a scalar function", "code": HDR + """\
x = y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2)/2)  # 2D Gaussian
dZdX, dZdY = np.gradient(Z, x, y)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
cf = axes[0].contourf(X, Y, Z, levels=20, cmap='viridis')
fig.colorbar(cf, ax=axes[0], label='f(x,y)')
axes[0].set_title('Scalar Field: 2D Gaussian')

# Subsample for quiver
step = 4
axes[1].contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.5)
axes[1].quiver(X[::step,::step], Y[::step,::step],
               dZdX[::step,::step], dZdY[::step,::step],
               color='white', scale=10, alpha=0.9)
axes[1].set_title('Gradient Field (quiver)')

for ax in axes:
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_aspect('equal')
fig.tight_layout()
fig.savefig('gradient_field.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved gradient_field.png')"""},
        {"label": "Electric dipole field with streamplot", "code": HDR + """\
x = np.linspace(-4, 4, 200)
y = np.linspace(-3, 3, 150)
X, Y = np.meshgrid(x, y)

# Two point charges: +1 at (-1,0), -1 at (1,0)
def field(q, x0, y0, X, Y):
    dx, dy = X - x0, Y - y0
    r3 = (dx**2 + dy**2)**1.5
    r3 = np.where(r3 < 0.1, 0.1, r3)
    return q*dx/r3, q*dy/r3

Ex1, Ey1 = field(+1, -1, 0, X, Y)
Ex2, Ey2 = field(-1, +1, 0, X, Y)
Ex = Ex1 + Ex2; Ey = Ey1 + Ey2
speed = np.sqrt(Ex**2 + Ey**2)

fig, ax = plt.subplots(figsize=(8, 6))
strm = ax.streamplot(X, Y, Ex, Ey, color=np.log1p(speed),
                      cmap='coolwarm', density=1.5, linewidth=1.2)
ax.plot(-1, 0, 'bo', markersize=12, label='+q')
ax.plot(+1, 0, 'r^', markersize=12, label='-q')
fig.colorbar(strm.lines, ax=ax, label='log(|E|+1)')
ax.set_xlim(-4,4); ax.set_ylim(-3,3)
ax.set_title('Electric Dipole Field Lines')
ax.legend(); ax.set_aspect('equal')
fig.tight_layout()
fig.savefig('dipole_field.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved dipole_field.png')"""},
    ],
    "Ocean Current Visualization",
    "Simulate a simplified ocean surface current field with a gyre (circular) pattern plus a northward drift. Plot streamlines colored by speed, add coastline patches, and label the gyre center.",
    HDR + """\
x = np.linspace(-5, 5, 150)
y = np.linspace(-4, 4, 120)
X, Y = np.meshgrid(x, y)

# Gyre + drift
U = -Y * np.exp(-(X**2 + Y**2)/8) + 0.2
V =  X * np.exp(-(X**2 + Y**2)/8) + 0.05*np.cos(Y)
speed = np.sqrt(U**2 + V**2)

fig, ax = plt.subplots(figsize=(10, 7))
strm = ax.streamplot(X, Y, U, V, color=speed, cmap='ocean_r',
                      density=2.0, linewidth=1.5, arrowsize=1.1)
fig.colorbar(strm.lines, ax=ax, label='Current Speed (m/s)')

# Simulated coastline patches
import matplotlib.patches as mp
coast = mp.Rectangle((3.5,-4), 1.5, 8, facecolor='#c2a267', edgecolor='none', zorder=5)
ax.add_patch(coast)
ax.text(4.25, 0, 'Coast', ha='center', rotation=90, fontsize=10,
        fontweight='bold', color='#5a3e1b', zorder=6)

ax.plot(0, 0, 'w*', markersize=14, label='Gyre center', zorder=7)
ax.set_xlim(-5,5); ax.set_ylim(-4,4)
ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude')
ax.set_title('Ocean Surface Current Gyre', fontweight='bold')
ax.legend(loc='upper left')
fig.tight_layout()
fig.savefig('ocean_current.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved ocean_current.png')""",
    "Vector Field Practice",
    "Create a saddle-point vector field: U = X, V = -Y for X,Y in [-2,2]. Plot (1) quiver and (2) streamplot side by side. Color arrows/lines by speed. Mark the equilibrium point at (0,0) with a star. What type of fixed point is this?",
    HDR + """\
x = y = np.linspace(-2, 2, 20)
X, Y = np.meshgrid(x, y)
U =  X
V = -Y
speed = np.sqrt(U**2 + V**2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
# TODO: quiver on ax1, colored by speed
# TODO: streamplot on ax2, colored by speed
# TODO: mark (0,0) with a star on both
# TODO: add colorbar, labels, titles
# Hint: saddle point — unstable in x, stable in y
fig.tight_layout()
fig.savefig('saddle_field.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved saddle_field.png')"""
)

# ── Section 28: Broken Axis & Dual Axis ───────────────────────────────────────
s28 = make_mpl(
    28, "Broken Axis & Dual Axis",
    "Handle datasets with extreme outliers using a broken y-axis (two subplots with different ylim), and compare two unrelated scales with twinx()/twiny().",
    [
        {"label": "Broken y-axis with diagonal break markers", "code": HDR + """\
np.random.seed(0)
x = np.arange(10)
y = np.array([2, 3, 4, 3, 5, 4, 6, 5, 4, 3], dtype=float)
y[4] = 95   # outlier

fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(8, 6),
    sharex=True, gridspec_kw={'hspace': 0.08, 'height_ratios': [1, 3]})

ax_top.bar(x, y, color='steelblue', alpha=0.8)
ax_bot.bar(x, y, color='steelblue', alpha=0.8)

ax_top.set_ylim(85, 100)
ax_bot.set_ylim(0, 10)
ax_top.spines['bottom'].set_visible(False)
ax_bot.spines['top'].set_visible(False)
ax_top.tick_params(bottom=False)

# Break markers
d = 0.015
kwargs = dict(transform=ax_top.transAxes, color='k', clip_on=False, linewidth=1.5)
ax_top.plot((-d, +d), (-d, +d), **kwargs)
ax_top.plot((1-d, 1+d), (-d, +d), **kwargs)
kwargs.update(transform=ax_bot.transAxes)
ax_bot.plot((-d, +d), (1-d, 1+d), **kwargs)
ax_bot.plot((1-d, 1+d), (1-d, 1+d), **kwargs)

ax_bot.set_xlabel('Category')
fig.text(0.04, 0.5, 'Value', va='center', rotation='vertical')
fig.suptitle('Broken Y-Axis — Outlier Handling', fontweight='bold')
fig.savefig('broken_axis.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved broken_axis.png')"""},
        {"label": "twinx: temperature and precipitation", "code": HDR + """\
months = np.arange(1, 13)
temp = np.array([2,3,8,14,19,24,27,26,20,14,7,3], dtype=float)
precip = np.array([60,50,55,45,55,70,95,110,80,65,70,65], dtype=float)
month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

ax1.bar(months, precip, color='steelblue', alpha=0.5, label='Precipitation')
ax2.plot(months, temp, 'ro-', linewidth=2, markersize=6, label='Temperature')

ax1.set_xlabel('Month')
ax1.set_ylabel('Precipitation (mm)', color='steelblue')
ax2.set_ylabel('Temperature (°C)', color='tomato')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax2.tick_params(axis='y', labelcolor='tomato')
ax1.set_xticks(months); ax1.set_xticklabels(month_labels, rotation=30)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='upper left')
ax1.set_title('Climate Chart — twinx()', fontweight='bold')
ax1.grid(True, alpha=0.2)
fig.tight_layout()
fig.savefig('twinx_climate.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved twinx_climate.png')"""},
        {"label": "twiny: two x-axes (Hz and ms)", "code": HDR + """\
freq = np.linspace(10, 1000, 200)   # Hz
period_ms = 1000 / freq              # milliseconds
gain = 1 / (1 + (freq/100)**2)

fig, ax1 = plt.subplots(figsize=(9, 4))
ax2 = ax1.twiny()

ax1.semilogx(freq, gain, color='steelblue', linewidth=2)
ax1.set_xlabel('Frequency (Hz)', color='steelblue')
ax1.tick_params(axis='x', labelcolor='steelblue')
ax1.set_ylabel('Gain')

# Top axis: period in ms (nonuniform tick positions in frequency space)
tick_freq = [10, 20, 50, 100, 200, 500, 1000]
tick_labels = [f'{1000/f:.0f}' for f in tick_freq]
ax2.set_xscale('log')
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(tick_freq)
ax2.set_xticklabels(tick_labels)
ax2.set_xlabel('Period (ms)', color='tomato')
ax2.tick_params(axis='x', labelcolor='tomato')

ax1.set_title('Low-Pass Filter — Dual Frequency / Period Axes', fontweight='bold', y=1.15)
ax1.grid(True, which='both', alpha=0.3)
fig.tight_layout()
fig.savefig('twiny_filter.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved twiny_filter.png')"""},
        {"label": "Multi-panel with broken and twin axes", "code": HDR + """\
np.random.seed(5)
t = np.arange(24)
load = np.random.uniform(200, 400, 24)
load[12] = 950  # midday spike
price = 20 + 0.05 * load + np.random.randn(24) * 3

fig = plt.figure(figsize=(11, 7))
ax_t = fig.add_axes([0.1, 0.55, 0.8, 0.22])
ax_b = fig.add_axes([0.1, 0.10, 0.8, 0.40], sharex=ax_t)
ax_r = ax_b.twinx()

# broken axis
ax_t.bar(t, load, color='tomato', alpha=0.7); ax_t.set_ylim(800, 1050)
ax_b.bar(t, load, color='tomato', alpha=0.7); ax_b.set_ylim(0, 500)
ax_t.spines['bottom'].set_visible(False); ax_b.spines['top'].set_visible(False)
ax_t.tick_params(bottom=False)

ax_r.plot(t, price, 'b-o', markersize=4, linewidth=1.5)
ax_r.set_ylabel('Price ($/MWh)', color='steelblue')
ax_r.tick_params(axis='y', labelcolor='steelblue')
ax_b.set_xlabel('Hour of Day')
ax_b.set_ylabel('Load (MW)', color='tomato')
ax_b.tick_params(axis='y', labelcolor='tomato')
fig.suptitle('Grid Load & Price: Broken + Twin Axes', fontweight='bold', y=0.98)
fig.savefig('broken_twin.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved broken_twin.png')"""},
    ],
    "Stock Price & Volume Dashboard",
    "Create a financial chart: top panel shows candlestick-style daily range (high-low as bar, open-close as body using broken axis to exclude an extreme day), bottom panel uses twinx for price (line) and volume (bar).",
    HDR + """\
np.random.seed(33)
days = np.arange(20)
opens  = 100 + np.random.randn(20).cumsum()
closes = opens + np.random.randn(20) * 0.5
highs  = np.maximum(opens, closes) + np.abs(np.random.randn(20))*0.8
lows   = np.minimum(opens, closes) - np.abs(np.random.randn(20))*0.8
volume = np.random.randint(100000, 500000, 20).astype(float)
volume[9] = 1800000  # volume spike

fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(11,6),
    sharex=True, gridspec_kw={'hspace':0.1,'height_ratios':[2,1]})
ax_vol = ax_bot.twinx()

# Candlestick style
for d in days:
    color = 'seagreen' if closes[d] >= opens[d] else 'tomato'
    ax_top.plot([d,d], [lows[d], highs[d]], color='gray', linewidth=1)
    ax_top.bar(d, abs(closes[d]-opens[d]), bottom=min(opens[d],closes[d]),
               color=color, width=0.6, alpha=0.9)

ax_bot.bar(days, volume, color='steelblue', alpha=0.5, label='Volume')
ax_vol.plot(days, closes, 'k-', linewidth=1.5, label='Close')
ax_vol.set_ylabel('Price ($)')
ax_bot.set_ylabel('Volume')
ax_top.set_ylabel('Price ($)')
ax_top.set_title('Stock Price & Volume Dashboard', fontweight='bold')
ax_bot.set_xlabel('Day')
fig.tight_layout()
fig.savefig('stock_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved stock_dashboard.png')""",
    "Dual Axis Practice",
    "Simulate monthly website users (in thousands, growing from 10 to 80 over 12 months) and server costs (in $, growing from 500 to 2000). Plot users as a filled area (fill_between) on left axis and costs as a step line on right axis (twinx). Use contrasting colors and add a legend.",
    HDR + """\
months = np.arange(1, 13)
users = np.linspace(10, 80, 12) + np.random.randn(12)*3
costs = np.linspace(500, 2000, 12) + np.random.randn(12)*50
month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
# TODO: fill_between for users on ax1
# TODO: step line for costs on ax2
# TODO: contrasting colors, labels, legend, title
# TODO: save 'users_costs.png'
plt.close()"""
)

# ── Section 29: Image Processing with imshow ──────────────────────────────────
s29 = make_mpl(
    29, "Image Processing with imshow",
    "Use imshow() for displaying arrays as images, applying colormaps, performing simple transformations, and visualizing feature maps from neural networks.",
    [
        {"label": "Display and compare colormaps", "code": HDR + """\
from matplotlib.colors import Normalize

np.random.seed(0)
img = np.random.randn(40, 40).cumsum(axis=1)

cmaps_show = ['gray', 'viridis', 'plasma', 'RdBu_r']
fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
for ax, cmap in zip(axes, cmaps_show):
    im = ax.imshow(img, cmap=cmap, aspect='auto')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title(cmap, fontsize=10)
    ax.axis('off')
fig.suptitle('Same Array — Different Colormaps', fontweight='bold')
fig.tight_layout()
fig.savefig('colormaps_compare.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved colormaps_compare.png')"""},
        {"label": "Image transformations: flip, rotate, crop", "code": HDR + """\
np.random.seed(1)
img = np.random.rand(60, 80)
img[20:40, 30:60] = 0.85  # bright rectangle

transforms = {
    'Original': img,
    'Flipped H': np.fliplr(img),
    'Rotated 45': np.rot90(img),
    'Cropped': img[10:50, 20:70],
}

fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
for ax, (title, arr) in zip(axes, transforms.items()):
    ax.imshow(arr, cmap='gray', vmin=0, vmax=1)
    ax.set_title(title, fontsize=10); ax.axis('off')
fig.suptitle('Image Transformations', fontweight='bold')
fig.tight_layout()
fig.savefig('img_transforms.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved img_transforms.png')"""},
        {"label": "Visualize CNN feature maps", "code": HDR + """\
np.random.seed(42)
n_filters = 8
feature_maps = [np.random.randn(28, 28) for _ in range(n_filters)]
for i, fm in enumerate(feature_maps):
    # Simulate different filter responses
    x = y = np.linspace(-3, 3, 28)
    X, Y = np.meshgrid(x, y)
    feature_maps[i] = np.sin(X*(i+1)*0.5) * np.cos(Y*(i+1)*0.3) + np.random.randn(28,28)*0.2

fig, axes = plt.subplots(2, 4, figsize=(12, 6))
for ax, fm in zip(axes.flat, feature_maps):
    im = ax.imshow(fm, cmap='RdBu_r', aspect='auto')
    plt.colorbar(im, ax=ax, fraction=0.046)
    ax.axis('off')
fig.suptitle('CNN Feature Maps (Layer 1)', fontweight='bold')
fig.tight_layout()
fig.savefig('feature_maps.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved feature_maps.png')"""},
        {"label": "Overlay: masks, contours, and annotations", "code": HDR + """\
np.random.seed(7)
h, w = 60, 80
bg = np.random.randn(h, w)
signal_x, signal_y = 50, 30
for dy in range(-10, 11):
    for dx in range(-15, 16):
        if dx**2/225 + dy**2/100 < 1:
            bg[signal_y+dy, signal_x+dx] += 3.0

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
# Raw image
axes[0].imshow(bg, cmap='gray'); axes[0].set_title('Raw'); axes[0].axis('off')

# Thresholded mask
mask = (bg > 2.0).astype(float)
axes[1].imshow(bg, cmap='gray')
axes[1].imshow(mask, cmap='Reds', alpha=0.5)
axes[1].set_title('Overlay Mask'); axes[1].axis('off')

# Contour overlay
axes[2].imshow(bg, cmap='gray')
axes[2].contour(bg, levels=[1.5, 2.5], colors=['yellow','red'], linewidths=1.5)
axes[2].annotate('Signal', xy=(signal_x, signal_y), xytext=(signal_x+12, signal_y-12),
                 arrowprops=dict(arrowstyle='->', color='cyan'),
                 color='cyan', fontsize=10, fontweight='bold')
axes[2].set_title('Contour Overlay'); axes[2].axis('off')
fig.suptitle('Image Segmentation Visualization', fontweight='bold')
fig.tight_layout()
fig.savefig('img_overlay.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved img_overlay.png')"""},
    ],
    "Medical Image Analysis Dashboard",
    "Simulate a 2D MRI slice (layered Gaussians) and visualize it: (1) raw grayscale, (2) threshold mask in red overlay, (3) gradient magnitude for edge detection, (4) pseudo-color with contour at 50% max intensity.",
    HDR + """\
from scipy.ndimage import gaussian_filter

np.random.seed(42)
h, w = 80, 100
img = np.zeros((h, w))
for cx, cy, r, v in [(50,40,15,1.0),(35,30,8,0.7),(65,50,10,0.8),(45,60,6,0.6)]:
    y_idx, x_idx = np.ogrid[:h,:w]
    img += v * np.exp(-((x_idx-cx)**2 + (y_idx-cy)**2)/(2*r**2))
img = gaussian_filter(img + np.random.randn(h,w)*0.05, sigma=1.5)

fig, axes = plt.subplots(1, 4, figsize=(14, 4))

axes[0].imshow(img, cmap='gray'); axes[0].set_title('Raw MRI Slice'); axes[0].axis('off')

mask = img > img.max()*0.5
axes[1].imshow(img, cmap='gray')
axes[1].imshow(np.ma.masked_where(~mask, img), cmap='Reds', alpha=0.6, vmin=0, vmax=1)
axes[1].set_title('Threshold Mask'); axes[1].axis('off')

gy, gx = np.gradient(img)
grad_mag = np.sqrt(gx**2 + gy**2)
axes[2].imshow(grad_mag, cmap='hot'); axes[2].set_title('Gradient Magnitude'); axes[2].axis('off')

axes[3].imshow(img, cmap='plasma')
axes[3].contour(img, levels=[img.max()*0.5], colors='white', linewidths=2)
axes[3].set_title('Pseudo-color + Contour'); axes[3].axis('off')

fig.suptitle('MRI Analysis Dashboard', fontweight='bold')
fig.tight_layout()
fig.savefig('mri_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved mri_dashboard.png')""",
    "Image Processing Practice",
    "Create a 50x50 checkerboard pattern (alternating 0 and 1 in 5x5 blocks). Display it in a 1x3 subplot: (1) original with 'gray' cmap, (2) with 'hot' cmap and colorbar, (3) with a Gaussian blur applied (use np.convolve or loop-based blur). Add titles.",
    HDR + """\
# Build checkerboard
size, block = 50, 5
board = np.zeros((size, size))
for i in range(0, size, block):
    for j in range(0, size, block):
        if (i//block + j//block) % 2 == 0:
            board[i:i+block, j:j+block] = 1

fig, axes = plt.subplots(1, 3, figsize=(11, 4))
# TODO: original gray cmap
# TODO: hot cmap with colorbar
# TODO: blurred version (use gaussian_filter from scipy.ndimage)
# TODO: add titles and axis('off')
# TODO: save 'checkerboard.png'
plt.close()"""
)

# ── Section 30: Statistical Plots ────────────────────────────────────────────
s30 = make_mpl(
    30, "Statistical Plots",
    "Create publication-quality statistical visualizations: regression plots, residual diagnostics, Q-Q plots, correlation matrices, and bootstrapped confidence intervals.",
    [
        {"label": "Scatter with linear regression and confidence band", "code": HDR + """\
np.random.seed(0)
n = 80
x = np.linspace(0, 10, n)
y = 2.5*x + 1.0 + np.random.randn(n)*3

# Manual OLS
coeffs = np.polyfit(x, y, 1)
poly = np.poly1d(coeffs)
y_pred = poly(x)
residuals = y - y_pred
se = np.std(residuals) * np.sqrt(1/n + (x - x.mean())**2 / ((x - x.mean())**2).sum())
t_val = 1.99  # ~95% CI for n=80

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, s=25, alpha=0.6, color='steelblue', label='Data')
ax.plot(x, y_pred, 'r-', linewidth=2, label=f'y={coeffs[0]:.2f}x+{coeffs[1]:.2f}')
ax.fill_between(x, y_pred - t_val*se, y_pred + t_val*se,
                alpha=0.2, color='red', label='95% CI')
ax.set_xlabel('X'); ax.set_ylabel('Y')
ax.set_title('Linear Regression with Confidence Band')
ax.legend(); ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('regression_plot.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved regression_plot.png')"""},
        {"label": "Q-Q plot for normality check", "code": HDR + """\
from scipy import stats

np.random.seed(1)
fig, axes = plt.subplots(1, 3, figsize=(13, 4))

datasets = {
    'Normal': np.random.normal(0, 1, 200),
    'Right-Skewed': np.random.exponential(1, 200),
    'Heavy-Tailed': np.random.standard_t(df=3, size=200),
}

for ax, (name, data) in zip(axes, datasets.items()):
    qq = stats.probplot(data, dist='norm')
    theo, sample = qq[0]
    ax.scatter(theo, sample, s=15, alpha=0.6, color='steelblue')
    ax.plot(theo, theo * qq[1][0] + qq[1][1], 'r-', linewidth=1.5, label='Ideal')
    ax.set_title(f'Q-Q Plot: {name}')
    ax.set_xlabel('Theoretical Quantiles')
    ax.set_ylabel('Sample Quantiles')
    ax.grid(True, alpha=0.3); ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig('qq_plots.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved qq_plots.png')"""},
        {"label": "Correlation matrix heatmap", "code": HDR + """\
np.random.seed(2)
n = 200
a = np.random.randn(n)
b = 0.8*a + np.random.randn(n)*0.6
c = -0.5*a + np.random.randn(n)*0.8
d = np.random.randn(n)
e = 0.6*b + 0.4*d + np.random.randn(n)*0.5

data_mat = np.vstack([a,b,c,d,e]).T
labels = ['Feature A','Feature B','Feature C','Feature D','Feature E']
corr = np.corrcoef(data_mat.T)

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
plt.colorbar(im, ax=ax, label='Pearson r')
ax.set_xticks(range(5)); ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=9)
ax.set_yticks(range(5)); ax.set_yticklabels(labels, fontsize=9)
for i in range(5):
    for j in range(5):
        c_val = corr[i,j]
        ax.text(j, i, f'{c_val:.2f}', ha='center', va='center', fontsize=8,
                color='white' if abs(c_val) > 0.5 else 'black')
ax.set_title('Correlation Matrix', fontweight='bold')
fig.tight_layout()
fig.savefig('corr_matrix.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved corr_matrix.png')"""},
        {"label": "Bootstrapped confidence interval", "code": HDR + """\
np.random.seed(3)
data = np.random.exponential(2, 100)

n_boot = 2000
boot_means = [np.mean(np.random.choice(data, len(data), replace=True))
              for _ in range(n_boot)]

ci_lo, ci_hi = np.percentile(boot_means, [2.5, 97.5])
true_mean = np.mean(data)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.hist(data, bins=25, color='steelblue', alpha=0.7, density=True)
ax1.axvline(true_mean, color='red', linewidth=2, label=f'Mean={true_mean:.2f}')
ax1.set_title('Original Data (Exponential)'); ax1.legend(); ax1.grid(True, alpha=0.3)

ax2.hist(boot_means, bins=40, color='seagreen', alpha=0.7, density=True)
ax2.axvline(ci_lo, color='red', linestyle='--', linewidth=2, label=f'95% CI [{ci_lo:.2f}, {ci_hi:.2f}]')
ax2.axvline(ci_hi, color='red', linestyle='--', linewidth=2)
ax2.axvline(true_mean, color='black', linewidth=2, label='Sample mean')
ax2.set_title('Bootstrap Distribution of Mean')
ax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)
fig.suptitle('Bootstrapped 95% Confidence Interval', fontweight='bold')
fig.tight_layout()
fig.savefig('bootstrap_ci.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved bootstrap_ci.png')"""},
    ],
    "Regression Diagnostics Panel",
    "Fit a polynomial regression (degree 3) on noisy data. Show a 2x2 diagnostic panel: (1) fitted curve on data, (2) residuals vs fitted values, (3) Q-Q plot of residuals, (4) histogram of residuals with normal overlay.",
    HDR + """\
from scipy import stats

np.random.seed(99)
x = np.linspace(0, 10, 100)
y_true = 0.2*x**3 - 3*x**2 + 10*x + 5
y = y_true + np.random.randn(100)*5

coeffs = np.polyfit(x, y, 3)
poly = np.poly1d(coeffs)
y_hat = poly(x)
resid = y - y_hat

fig, axes = plt.subplots(2, 2, figsize=(11, 8))

# Fitted curve
axes[0,0].scatter(x, y, s=20, alpha=0.6, color='steelblue', label='Data')
axes[0,0].plot(x, y_hat, 'r-', linewidth=2, label='Poly-3 fit')
axes[0,0].set_title('Fitted Curve'); axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3)

# Residuals vs fitted
axes[0,1].scatter(y_hat, resid, s=15, alpha=0.6, color='steelblue')
axes[0,1].axhline(0, color='red', linestyle='--', linewidth=1.5)
axes[0,1].set_xlabel('Fitted'); axes[0,1].set_ylabel('Residuals')
axes[0,1].set_title('Residuals vs Fitted'); axes[0,1].grid(True, alpha=0.3)

# Q-Q plot
qq = stats.probplot(resid, dist='norm')
theo, samp = qq[0]
axes[1,0].scatter(theo, samp, s=15, alpha=0.6, color='steelblue')
axes[1,0].plot(theo, theo*qq[1][0]+qq[1][1], 'r-', linewidth=1.5)
axes[1,0].set_title('Q-Q Plot of Residuals')
axes[1,0].set_xlabel('Theoretical'); axes[1,0].set_ylabel('Sample')
axes[1,0].grid(True, alpha=0.3)

# Residual histogram
axes[1,1].hist(resid, bins=20, density=True, color='steelblue', alpha=0.7)
rx = np.linspace(resid.min(), resid.max(), 100)
axes[1,1].plot(rx, stats.norm.pdf(rx, resid.mean(), resid.std()), 'r-', linewidth=2)
axes[1,1].set_title('Residual Distribution'); axes[1,1].grid(True, alpha=0.3)

fig.suptitle('Regression Diagnostic Panel', fontweight='bold')
fig.tight_layout()
fig.savefig('regression_diagnostics.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved regression_diagnostics.png')""",
    "Statistical Plots Practice",
    "Generate 5 groups of 50 samples each from distributions with means [1,2,3,4,5] and std=1. Create a 1x2 figure: (1) box plot of all 5 groups with mean markers (diamond), (2) violin plot overlaid with individual jitter points (alpha=0.3, s=15). Use matching colors across panels.",
    HDR + """\
np.random.seed(20)
groups = [np.random.normal(mu, 1, 50) for mu in range(1, 6)]
labels = [f'G{i}' for i in range(1, 6)]
colors = ['#4c72b0','#dd8452','#55a868','#c44e52','#9467bd']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
# TODO: boxplot on ax1 with mean diamond markers
# TODO: violinplot on ax2 with jitter scatter overlay
# TODO: matching colors, labels, titles
# TODO: save 'group_stats.png'
plt.close()"""
)

# ── Section 31: Multi-figure PDF & PNG Export ────────────────────────────────
s31 = make_mpl(
    31, "Multi-Figure Export & Backends",
    "Export single figures at various DPIs, save multiple pages to PDF with PdfPages, create figure collections, and control backends for headless rendering.",
    [
        {"label": "PdfPages: multi-page PDF report", "code": HDR + """\
from matplotlib.backends.backend_pdf import PdfPages

np.random.seed(0)
pdf_path = 'multi_page_report.pdf'

with PdfPages(pdf_path) as pdf:
    # Page 1: line plot
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, 10, 200)
    ax.plot(x, np.sin(x), color='steelblue', linewidth=2)
    ax.set_title('Page 1: Sine Wave')
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    pdf.savefig(fig); plt.close()

    # Page 2: bar chart
    fig, ax = plt.subplots(figsize=(8, 5))
    vals = np.random.randint(10, 100, 8)
    ax.bar(range(8), vals, color='tomato', alpha=0.8)
    ax.set_title('Page 2: Bar Chart')
    fig.tight_layout()
    pdf.savefig(fig); plt.close()

    # Page 3: scatter
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(*np.random.randn(2, 200), s=20, alpha=0.5)
    ax.set_title('Page 3: Scatter')
    fig.tight_layout()
    pdf.savefig(fig); plt.close()

    d = pdf.infodict()
    d['Title'] = 'Data Science Report'
    d['Author'] = 'matplotlib'

print(f'Saved {pdf_path} (3 pages)')"""},
        {"label": "Export PNG at multiple DPIs", "code": HDR + """\
np.random.seed(1)
x = np.linspace(0, 2*np.pi, 200)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, np.sin(x), linewidth=2, color='steelblue', label='sin')
ax.plot(x, np.cos(x), linewidth=2, color='tomato', linestyle='--', label='cos')
ax.legend(); ax.set_title('Multi-DPI Export Test')
ax.grid(True, alpha=0.3)
fig.tight_layout()

for dpi in [72, 150, 300]:
    fname = f'export_dpi{dpi}.png'
    fig.savefig(fname, dpi=dpi, bbox_inches='tight')
    print(f'Saved {fname} at {dpi} DPI')
plt.close()"""},
        {"label": "SVG export for web/vector graphics", "code": HDR + """\
import matplotlib
matplotlib.rcParams['svg.fonttype'] = 'none'  # editable text in SVG

np.random.seed(2)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
x = np.linspace(-3, 3, 100)
axes[0].plot(x, stats_curve := 1/(1+np.exp(-x)), color='steelblue', linewidth=2)
axes[0].axhline(0.5, color='red', linestyle='--', linewidth=1)
axes[0].set_title('Sigmoid Function'); axes[0].grid(True, alpha=0.3)
axes[0].set_xlabel('x'); axes[0].set_ylabel('sigma(x)')

np.random.seed(2)
data = np.random.randn(100)
axes[1].hist(data, bins=20, color='seagreen', alpha=0.7, density=True)
axes[1].set_title('Normal Distribution'); axes[1].grid(True, alpha=0.3)

fig.suptitle('SVG Export Example', fontweight='bold')
fig.tight_layout()
fig.savefig('vector_export.svg', format='svg', bbox_inches='tight')
fig.savefig('vector_export.png', dpi=150, bbox_inches='tight')
print('Saved vector_export.svg and vector_export.png')
plt.close()"""},
        {"label": "Figure with custom metadata and tight layout", "code": HDR + """\
np.random.seed(3)
fig = plt.figure(figsize=(10, 7))
fig.set_facecolor('#0f1117')

ax1 = fig.add_subplot(2, 2, (1, 2))  # top row, spans both cols
ax2 = fig.add_subplot(2, 2, 3)
ax3 = fig.add_subplot(2, 2, 4)

x = np.linspace(0, 10, 300)
ax1.plot(x, np.sin(x)*np.exp(-0.1*x), color='#58a6ff', linewidth=2)
ax1.set_facecolor('#1c2128'); ax1.tick_params(colors='white')
for sp in ax1.spines.values(): sp.set_color('#30363d')
ax1.set_title('Damped Oscillation', color='white')

ax2.hist(np.random.randn(500), bins=25, color='#79c0ff', alpha=0.8)
ax2.set_facecolor('#1c2128'); ax2.tick_params(colors='white')
for sp in ax2.spines.values(): sp.set_color('#30363d')
ax2.set_title('Distribution', color='white')

ax3.scatter(*np.random.randn(2,100), s=15, alpha=0.6, color='#ffa657')
ax3.set_facecolor('#1c2128'); ax3.tick_params(colors='white')
for sp in ax3.spines.values(): sp.set_color('#30363d')
ax3.set_title('Scatter', color='white')

fig.suptitle('Dark Theme Dashboard', color='white', fontweight='bold', fontsize=14)
fig.tight_layout()
fig.savefig('dark_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print('Saved dark_dashboard.png')"""},
    ],
    "Automated Report Generation",
    "Generate a 4-page PDF report: page 1 cover with title text and logo placeholder, page 2 multi-panel KPI summary, page 3 trend analysis, page 4 summary table rendered as a matplotlib table.",
    HDR + """\
from matplotlib.backends.backend_pdf import PdfPages

np.random.seed(77)

with PdfPages('automated_report.pdf') as pdf:
    # Page 1: cover
    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor('#1c2128')
    ax = fig.add_axes([0,0,1,1]); ax.axis('off')
    ax.text(0.5,0.65,'Data Science\nQuarterly Report', ha='center', va='center',
            fontsize=28, color='white', fontweight='bold', transform=ax.transAxes)
    ax.text(0.5,0.45,'Q1 2025 | Generated by Matplotlib', ha='center',
            fontsize=13, color='#8b949e', transform=ax.transAxes)
    pdf.savefig(fig, facecolor=fig.get_facecolor()); plt.close()

    # Page 2: KPI panel
    fig, axes = plt.subplots(1,3, figsize=(11,5))
    kpis = [('Revenue','$2.4M','+12%','#4c72b0'),
            ('Users','84K','+8%','#55a868'),
            ('NPS','72','+5pt','#dd8452')]
    for ax,(label,val,delta,col) in zip(axes,kpis):
        ax.set_facecolor(col); ax.axis('off')
        ax.text(0.5,0.65,val,ha='center',fontsize=28,fontweight='bold',
                color='white',transform=ax.transAxes)
        ax.text(0.5,0.35,f'{label}\n{delta}',ha='center',fontsize=11,
                color='white',transform=ax.transAxes)
    fig.suptitle('Key Performance Indicators',fontweight='bold')
    fig.tight_layout(); pdf.savefig(fig); plt.close()

    # Page 3: trends
    fig, ax = plt.subplots(figsize=(10,5))
    months = np.arange(12)
    for i,(name,col) in enumerate([('Revenue','#4c72b0'),('Costs','tomato'),('Margin','seagreen')]):
        y = np.cumsum(np.random.randn(12)*0.5) + 5 + i*1.5
        ax.plot(months, y, color=col, linewidth=2, label=name, marker='o', markersize=4)
    ax.set_title('12-Month Trend Analysis'); ax.legend(); ax.grid(True, alpha=0.3)
    fig.tight_layout(); pdf.savefig(fig); plt.close()

    # Page 4: table
    fig, ax = plt.subplots(figsize=(10,4))
    ax.axis('off')
    cols = ['Region','Q1','Q2','Q3','Q4','Total']
    rows = [['North','$1.2M','$1.4M','$1.3M','$1.6M','$5.5M'],
            ['South','$0.9M','$1.0M','$1.1M','$1.3M','$4.3M'],
            ['East','$0.7M','$0.8M','$0.9M','$1.0M','$3.4M'],
            ['West','$1.1M','$1.2M','$1.4M','$1.5M','$5.2M']]
    tbl = ax.table(cellText=rows, colLabels=cols, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False); tbl.set_fontsize(10); tbl.scale(1.2,1.8)
    ax.set_title('Regional Revenue Summary', fontweight='bold', pad=20)
    fig.tight_layout(); pdf.savefig(fig); plt.close()

print('Saved automated_report.pdf (4 pages)')""",
    "Export Practice",
    "Create a figure with 3 subplots (line, bar, scatter). Save it as: (1) PNG at 72 DPI, (2) PNG at 300 DPI, (3) SVG vector. Then use PdfPages to save it as a 2-page PDF where page 1 is the 3-panel figure and page 2 is just the scatter zoomed in with a title overlay.",
    HDR + """\
from matplotlib.backends.backend_pdf import PdfPages

np.random.seed(8)
x = np.linspace(0, 10, 100)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13, 4))
ax1.plot(x, np.sin(x)); ax1.set_title('Line')
ax2.bar(range(5), np.random.randint(1,10,5)); ax2.set_title('Bar')
ax3.scatter(*np.random.randn(2,50), s=20, alpha=0.6); ax3.set_title('Scatter')
fig.tight_layout()

# TODO: save PNG at 72 DPI
# TODO: save PNG at 300 DPI
# TODO: save SVG
# TODO: save 2-page PDF with PdfPages
plt.close()
print('Done')"""
)

# ── Section 32: Putting It All Together — Dashboard Composition ───────────────
s32 = make_mpl(
    32, "Dashboard Composition",
    "Compose production-quality dashboards by combining GridSpec layouts, dual axes, custom patches, annotation, and multi-figure export. Design for clarity, color accessibility, and print quality.",
    [
        {"label": "KPI summary dashboard with mixed chart types", "code": HDR + """\
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches

np.random.seed(42)
fig = plt.figure(figsize=(14, 9), facecolor='#0f1117')
gs = GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.4)

def dark_ax(ax, title=''):
    ax.set_facecolor('#1c2128')
    for sp in ax.spines.values(): sp.set_color('#30363d')
    ax.tick_params(colors='#c9d1d9', labelsize=8)
    if title: ax.set_title(title, color='white', fontsize=9, fontweight='bold')
    return ax

# Top row: KPI boxes (4 mini panels)
kpis = [('Revenue', '$2.4M', '+12%', '#4c72b0'),
        ('DAU',     '84K',   '+8%',  '#55a868'),
        ('Conv%',   '3.7%',  '+0.3', '#dd8452'),
        ('NPS',     '72',    '+5',   '#c44e52')]
for col, (label, val, delta, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, col])
    ax.set_facecolor(color); ax.axis('off')
    ax.text(0.5, 0.6, val, ha='center', va='center', fontsize=18,
            fontweight='bold', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.2, f'{label}  {delta}', ha='center', fontsize=9,
            color='white', transform=ax.transAxes)

# Mid-left: trend line (spans 2 cols)
ax_trend = dark_ax(fig.add_subplot(gs[1, :2]), 'Monthly Revenue Trend')
months = np.arange(12)
rev = 1.5 + np.cumsum(np.random.randn(12)*0.08) + np.linspace(0,0.9,12)
ax_trend.plot(months, rev, color='#58a6ff', linewidth=2)
ax_trend.fill_between(months, rev.min(), rev, alpha=0.15, color='#58a6ff')
ax_trend.set_xticks(months)
ax_trend.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'],
                          color='#8b949e', fontsize=7)

# Mid-right: bar chart (spans 2 cols)
ax_bar = dark_ax(fig.add_subplot(gs[1, 2:]), 'Revenue by Region')
regions = ['North','South','East','West']
vals = [2.4, 1.8, 1.3, 2.1]
colors_r = ['#4c72b0','#55a868','#dd8452','#c44e52']
ax_bar.bar(regions, vals, color=colors_r, alpha=0.85, width=0.6)
for i, (r, v) in enumerate(zip(regions, vals)):
    ax_bar.text(i, v+0.05, f'${v}M', ha='center', fontsize=8, color='white')

# Bottom: scatter + right-side donut
ax_scatter = dark_ax(fig.add_subplot(gs[2, :3]), 'User Engagement')
n = 300
sessions = np.random.lognormal(1, 0.5, n)
revenue_pts = sessions * np.random.uniform(5, 30, n)
sc = ax_scatter.scatter(sessions, revenue_pts, c=np.log(sessions),
                         cmap='plasma', s=20, alpha=0.6)
ax_scatter.set_xlabel('Sessions', color='#8b949e', fontsize=8)
ax_scatter.set_ylabel('Revenue ($)', color='#8b949e', fontsize=8)

ax_pie = dark_ax(fig.add_subplot(gs[2, 3]), 'Traffic Mix')
wedges, _ = ax_pie.pie([35,30,20,15], colors=['#4c72b0','#55a868','#dd8452','#8172b2'],
                        startangle=90, wedgeprops=dict(width=0.5))
ax_pie.legend(wedges, ['Direct','Organic','Paid','Ref'], loc='lower center',
              fontsize=7, labelcolor='white', facecolor='#1c2128',
              bbox_to_anchor=(0.5,-0.15), ncol=2)
ax_pie.axis('off'); ax_pie.set_facecolor('#1c2128')

fig.suptitle('Business Intelligence Dashboard', color='white',
             fontsize=15, fontweight='bold', y=0.98)
fig.savefig('bi_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print('Saved bi_dashboard.png')"""},
        {"label": "Scientific dashboard: experiment results", "code": HDR + """\
from matplotlib.gridspec import GridSpec
from scipy import stats

np.random.seed(7)
fig = plt.figure(figsize=(13, 8))
gs = GridSpec(2, 3, hspace=0.38, wspace=0.35)

# Time series with confidence band
ax1 = fig.add_subplot(gs[0, :2])
t = np.linspace(0, 20, 200)
signal = np.sin(t) * np.exp(-0.1*t)
noise = np.random.randn(200)*0.15
measured = signal + noise
upper = signal + 0.3; lower = signal - 0.3
ax1.fill_between(t, lower, upper, alpha=0.2, color='steelblue', label='95% CI')
ax1.plot(t, signal, 'steelblue', linewidth=2, label='True')
ax1.plot(t, measured, 'k.', markersize=3, alpha=0.4, label='Measured')
ax1.set_title('Damped Oscillation — Experiment A'); ax1.legend(fontsize=8)
ax1.set_xlabel('Time (s)'); ax1.grid(True, alpha=0.3)

# Q-Q
ax2 = fig.add_subplot(gs[0, 2])
qq = stats.probplot(measured - signal)
ax2.scatter(qq[0][0], qq[0][1], s=10, alpha=0.6, color='steelblue')
ax2.plot(qq[0][0], qq[0][0]*qq[1][0]+qq[1][1], 'r-')
ax2.set_title('Residual Q-Q'); ax2.grid(True, alpha=0.3)

# Frequency spectrum
ax3 = fig.add_subplot(gs[1, :2])
fft = np.abs(np.fft.rfft(measured))
freq = np.fft.rfftfreq(len(measured), d=t[1]-t[0])
ax3.semilogy(freq[1:], fft[1:], color='tomato', linewidth=1.5)
ax3.axvline(1/(2*np.pi), color='navy', linestyle='--', linewidth=1.5,
            label=f'Fundamental {1/(2*np.pi):.3f} Hz')
ax3.set_xlabel('Frequency (Hz)'); ax3.set_ylabel('Amplitude')
ax3.set_title('FFT Spectrum'); ax3.legend(fontsize=8); ax3.grid(True, which='both', alpha=0.3)

# Phase portrait
ax4 = fig.add_subplot(gs[1, 2])
vel = np.gradient(measured, t)
ax4.plot(measured, vel, 'purple', alpha=0.6, linewidth=0.8)
ax4.set_xlabel('Displacement'); ax4.set_ylabel('Velocity')
ax4.set_title('Phase Portrait'); ax4.grid(True, alpha=0.3)

fig.suptitle('Experiment Dashboard — Damped Oscillator', fontweight='bold', fontsize=13)
fig.savefig('science_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved science_dashboard.png')"""},
        {"label": "Financial OHLC chart with indicators", "code": HDR + """\
np.random.seed(21)
n = 60
dates = np.arange(n)
close = 100 + np.cumsum(np.random.randn(n)*1.2)
high  = close + np.abs(np.random.randn(n))*1.5
low   = close - np.abs(np.random.randn(n))*1.5
opens = close + np.random.randn(n)*0.5
volume = np.random.randint(500, 2000, n).astype(float)

sma20 = np.convolve(close, np.ones(20)/20, mode='valid')
sma_x = dates[19:]
bb_mid = sma20
bb_std = np.array([close[i-20:i].std() for i in range(20, n)])
bb_up = bb_mid + 2*bb_std; bb_lo = bb_mid - 2*bb_std

from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=0.12)
ax_price = fig.add_subplot(gs[0]); ax_vol = fig.add_subplot(gs[1], sharex=ax_price)
ax_rsi = fig.add_subplot(gs[2], sharex=ax_price)

for d in dates:
    color = 'seagreen' if close[d] >= opens[d] else 'tomato'
    ax_price.plot([d,d],[low[d],high[d]], color='gray', linewidth=0.8)
    ax_price.bar(d, abs(close[d]-opens[d]), bottom=min(close[d],opens[d]),
                 color=color, width=0.6)
ax_price.plot(sma_x, sma20, 'navy', linewidth=1.5, label='SMA20')
ax_price.fill_between(sma_x, bb_lo, bb_up, alpha=0.1, color='blue', label='BB±2σ')
ax_price.set_ylabel('Price'); ax_price.legend(fontsize=8)
ax_price.set_title('OHLC with Bollinger Bands', fontweight='bold')

ax_vol.bar(dates, volume, color='steelblue', alpha=0.6)
ax_vol.set_ylabel('Volume')

delta = np.diff(close); up = np.where(delta>0,delta,0); down = np.where(delta<0,-delta,0)
rs = np.convolve(up,np.ones(14)/14,'valid') / (np.convolve(down,np.ones(14)/14,'valid')+1e-9)
rsi = 100 - 100/(1+rs)
ax_rsi.plot(dates[14:], rsi, color='purple', linewidth=1.5)
ax_rsi.axhline(70, color='red', linestyle='--', linewidth=1)
ax_rsi.axhline(30, color='green', linestyle='--', linewidth=1)
ax_rsi.fill_between(dates[14:], 30, 70, alpha=0.05, color='gray')
ax_rsi.set_ylabel('RSI'); ax_rsi.set_ylim(0,100)
ax_rsi.set_xlabel('Day')

plt.setp(ax_price.get_xticklabels(), visible=False)
plt.setp(ax_vol.get_xticklabels(), visible=False)
fig.savefig('financial_chart.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved financial_chart.png')"""},
        {"label": "Accessible dashboard: colorblind-safe palette", "code": HDR + """\
# Colorblind-safe palette (Wong 2011)
CB_COLORS = ['#000000','#E69F00','#56B4E9','#009E73',
             '#F0E442','#0072B2','#D55E00','#CC79A7']

np.random.seed(99)
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
axes = axes.flat

# 1. Line plot
ax = axes[0]
x = np.linspace(0, 10, 100)
for i, col in enumerate(CB_COLORS[:4]):
    ax.plot(x, np.sin(x + i*np.pi/4), color=col, linewidth=2,
            label=f'Series {i+1}', linestyle=['-','--','-.',':'][i])
ax.set_title('Line Plot — CB Safe'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

# 2. Bar chart
ax = axes[1]
vals = np.random.uniform(2, 9, 5)
ax.bar(range(5), vals, color=CB_COLORS[:5], alpha=0.9, width=0.6,
       hatch=['', '//', 'xx', '..', '\\\\'])  # hatch for print accessibility
ax.set_title('Bar with Hatch Patterns'); ax.grid(True, axis='y', alpha=0.3)

# 3. Scatter
ax = axes[2]
for i in range(4):
    pts = np.random.randn(30, 2)
    ax.scatter(pts[:,0], pts[:,1], color=CB_COLORS[i+1], s=40, alpha=0.8,
               marker=['o','s','^','D'][i], label=f'Class {i+1}')
ax.set_title('Scatter — Multiple Markers'); ax.legend(fontsize=8)

# 4. Filled area
ax = axes[3]
x_a = np.linspace(0, 8, 80)
for i, col in enumerate(CB_COLORS[1:5]):
    y = np.sin(x_a + i) + i*0.8
    ax.plot(x_a, y, color=col, linewidth=2)
    ax.fill_between(x_a, 0, y, color=col, alpha=0.15)
ax.set_title('Area Chart — CB Safe'); ax.grid(True, alpha=0.3)

fig.suptitle('Colorblind-Safe Dashboard (Wong Palette)', fontweight='bold', fontsize=13)
fig.tight_layout()
fig.savefig('accessible_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved accessible_dashboard.png')"""},
    ],
    "Executive Analytics Deck",
    "Build a 5-panel executive dashboard: title banner, revenue trend with target line, geographic bar chart, user funnel (horizontal bars decreasing), and a summary table. Export at 200 DPI.",
    HDR + """\
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches

np.random.seed(88)
fig = plt.figure(figsize=(14, 10), facecolor='white')
gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# Banner
ax_banner = fig.add_subplot(gs[0, :])
ax_banner.set_facecolor('#1c2128'); ax_banner.axis('off')
ax_banner.text(0.5, 0.6, 'Executive Dashboard — Q4 2024',
               ha='center', fontsize=18, fontweight='bold', color='white',
               transform=ax_banner.transAxes)
ax_banner.text(0.5, 0.2, 'Prepared by Analytics Team | Confidential',
               ha='center', fontsize=11, color='#8b949e',
               transform=ax_banner.transAxes)

# Revenue trend
ax_rev = fig.add_subplot(gs[1, :2])
months = np.arange(12)
rev = 1.0 + np.cumsum(np.random.randn(12)*0.05) + np.linspace(0,0.8,12)
target = np.linspace(1.0, 2.0, 12)
ax_rev.plot(months, rev, 'steelblue', linewidth=2.5, marker='o', markersize=5, label='Actual')
ax_rev.plot(months, target, 'r--', linewidth=1.5, label='Target')
ax_rev.fill_between(months, rev, target, where=(rev>=target),
                    alpha=0.15, color='green', label='Ahead')
ax_rev.fill_between(months, rev, target, where=(rev<target),
                    alpha=0.15, color='red', label='Behind')
ax_rev.set_title('Monthly Revenue vs Target', fontweight='bold')
ax_rev.legend(fontsize=8); ax_rev.grid(True, alpha=0.3)

# Regional bar
ax_geo = fig.add_subplot(gs[1, 2])
regions = ['APAC','EMEA','AMER','LATAM']
rev_r = [4.2, 3.1, 5.8, 1.9]
ax_geo.barh(regions, rev_r, color=['#4c72b0','#dd8452','#55a868','#c44e52'], alpha=0.85)
for i,(r,v) in enumerate(zip(regions,rev_r)):
    ax_geo.text(v+0.05, i, f'${v}M', va='center', fontsize=9)
ax_geo.set_title('Revenue by Region', fontweight='bold')
ax_geo.grid(True, axis='x', alpha=0.3)

# Funnel
ax_funnel = fig.add_subplot(gs[2, :2])
stages = ['Visitors','Signups','Activated','Paid','Retained']
counts = [100000, 18000, 9000, 2800, 1900]
colors_f = ['#4c72b0','#5e82c0','#7498d0','#8aaee0','#a0c4f0']
ax_funnel.barh(stages[::-1], counts[::-1], color=colors_f, alpha=0.85)
for i,(s,c) in enumerate(zip(stages[::-1],counts[::-1])):
    ax_funnel.text(c+500, i, f'{c:,}', va='center', fontsize=9)
ax_funnel.set_title('User Acquisition Funnel', fontweight='bold')
ax_funnel.grid(True, axis='x', alpha=0.3)

# Table
ax_tbl = fig.add_subplot(gs[2, 2])
ax_tbl.axis('off')
cols = ['Metric','Q3','Q4']
rows = [['Revenue','$18.2M','$22.1M'],
        ['Users','76K','84K'],
        ['NPS','67','72']]
tbl = ax_tbl.table(cellText=rows, colLabels=cols, loc='center', cellLoc='center')
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1.1,1.5)
ax_tbl.set_title('Summary', fontweight='bold', pad=15)

fig.savefig('executive_deck.png', dpi=200, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print('Saved executive_deck.png')""",
    "Dashboard Practice",
    "Build your own 3-panel dashboard on a topic of your choice (e.g., fitness tracking, stock portfolio, weather). Requirements: (1) use GridSpec with at least one spanning panel, (2) include a dual-axis twinx or broken axis, (3) use at least 3 different chart types, (4) add a title banner, (5) save at 150 DPI.",
    HDR + """\
from matplotlib.gridspec import GridSpec

np.random.seed(42)
fig = plt.figure(figsize=(13, 9))
gs = GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.35)

# TODO: Banner row (gs[0, :])
# TODO: Main chart spanning 2 cols (gs[1, :2])
# TODO: Side chart (gs[1, 2])
# TODO: Bottom-left chart (gs[2, :2])
# TODO: Bottom-right chart or table (gs[2, 2])
# TODO: At least one twinx or broken axis
# TODO: Title and tight_layout
# TODO: save 'my_dashboard.png' at 150 DPI
plt.close()
print('Dashboard saved!')"""
)


# ── Assemble and insert ───────────────────────────────────────────────────────
all_sections = s25 + s26 + s27 + s28 + s29 + s30 + s31 + s32
result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: matplotlib sections 25-32 added")
else:
    print("FAILED")
