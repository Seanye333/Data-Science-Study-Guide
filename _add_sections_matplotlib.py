"""Add 3 sections to gen_matplotlib.py"""

MARKER = "]  # end SECTIONS"
FILEPATH = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_matplotlib.py"

NEW_SECTIONS = '''    {
        "title": "14. Animations & GIF Export",
        "examples": [
            {
                "label": "FuncAnimation — rolling sine wave",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import matplotlib.animation as animation\\n"
                    "import numpy as np\\n\\n"
                    "fig, ax = plt.subplots(figsize=(7, 3))\\n"
                    "x = np.linspace(0, 2*np.pi, 200)\\n"
                    "line, = ax.plot(x, np.sin(x))\\n"
                    "ax.set_ylim(-1.3, 1.3)\\n\\n"
                    "def update(frame):\\n"
                    "    line.set_ydata(np.sin(x + frame * 0.15))\\n"
                    "    return line,\\n\\n"
                    "ani = animation.FuncAnimation(fig, update, frames=40, interval=60, blit=True)\\n"
                    "try:\\n"
                    "    ani.save('sine_anim.gif', writer='pillow', fps=15)\\n"
                    "    print('Saved sine_anim.gif')\\n"
                    "except Exception as e:\\n"
                    "    print(f'pillow not installed ({e}) — animation built ok')\\n"
                    "plt.close()"
                )
            },
            {
                "label": "Random walk particle animation",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import matplotlib.animation as animation\\n"
                    "import numpy as np\\n\\n"
                    "np.random.seed(42)\\n"
                    "n = 20\\n"
                    "pos = np.random.randn(n, 2)\\n"
                    "fig, ax = plt.subplots(figsize=(5, 5))\\n"
                    "sc = ax.scatter(pos[:, 0], pos[:, 1], c=range(n), cmap='hsv', s=50)\\n"
                    "ax.set_xlim(-5, 5); ax.set_ylim(-5, 5)\\n"
                    "ax.set_title('Random Walk Particles')\\n\\n"
                    "def update(frame):\\n"
                    "    global pos\\n"
                    "    pos += np.random.randn(n, 2) * 0.15\\n"
                    "    pos = np.clip(pos, -4.5, 4.5)\\n"
                    "    sc.set_offsets(pos)\\n"
                    "    return sc,\\n\\n"
                    "ani = animation.FuncAnimation(fig, update, frames=50, interval=80, blit=True)\\n"
                    "try:\\n"
                    "    ani.save('particles.gif', writer='pillow', fps=12)\\n"
                    "    print('Saved particles.gif')\\n"
                    "except Exception as e:\\n"
                    "    print(f'pillow not found ({e})')\\n"
                    "plt.close()"
                )
            },
            {
                "label": "Dual-subplot animation (sin & cos)",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import matplotlib.animation as animation\\n"
                    "import numpy as np\\n\\n"
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))\\n"
                    "x = np.linspace(0, 2*np.pi, 200)\\n"
                    "l1, = ax1.plot(x, np.sin(x), 'b-')\\n"
                    "l2, = ax2.plot(x, np.cos(x), 'r-')\\n"
                    "ax1.set_title('sin(x+t)'); ax2.set_title('cos(x-t)')\\n\\n"
                    "def update(frame):\\n"
                    "    t = frame * 0.12\\n"
                    "    l1.set_ydata(np.sin(x + t))\\n"
                    "    l2.set_ydata(np.cos(x - t))\\n"
                    "    return l1, l2\\n\\n"
                    "ani = animation.FuncAnimation(fig, update, frames=50, blit=True)\\n"
                    "try:\\n"
                    "    ani.save('dual_anim.gif', writer='pillow', fps=15)\\n"
                    "    print('Saved dual_anim.gif')\\n"
                    "except:\\n"
                    "    print('Animation created (pillow needed to save)')\\n"
                    "plt.close()"
                )
            },
            {
                "label": "ArtistAnimation with histogram frames",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import matplotlib.animation as animation\\n"
                    "import numpy as np\\n\\n"
                    "fig, ax = plt.subplots(figsize=(6, 4))\\n"
                    "np.random.seed(0)\\n"
                    "frames = []\\n"
                    "for i in range(10):\\n"
                    "    data = np.random.randn(50) + i * 0.5\\n"
                    "    hist = ax.hist(data, bins=20, range=(-3, 9),\\n"
                    "                  color=plt.cm.viridis(i/10), alpha=0.7)\\n"
                    "    title = ax.text(0.5, 1.01, f'Shift = {i*0.5:.1f}',\\n"
                    "                   transform=ax.transAxes, ha='center')\\n"
                    "    frames.append(hist[2].tolist() + [title])\\n"
                    "ani = animation.ArtistAnimation(fig, frames, interval=300, blit=True)\\n"
                    "try:\\n"
                    "    ani.save('hist_anim.gif', writer='pillow', fps=3)\\n"
                    "    print('Saved hist_anim.gif')\\n"
                    "except:\\n"
                    "    print('ArtistAnimation built (pillow needed to save)')\\n"
                    "plt.close()"
                )
            }
        ],
        "rw_scenario": "You need to create an animated training-progress chart for a model review, showing how train/val loss evolved over 60 epochs.",
        "rw_code": (
            "import matplotlib\\n"
            "matplotlib.use('Agg')\\n"
            "import matplotlib.pyplot as plt\\n"
            "import matplotlib.animation as animation\\n"
            "import numpy as np\\n\\n"
            "np.random.seed(42)\\n"
            "epochs = 60\\n"
            "train_loss = 2.5 * np.exp(-np.linspace(0, 3, epochs)) + np.random.randn(epochs)*0.05\\n"
            "val_loss   = 2.5 * np.exp(-np.linspace(0, 2.7, epochs)) + np.random.randn(epochs)*0.08\\n\\n"
            "fig, ax = plt.subplots(figsize=(8, 4))\\n"
            "ax.set_xlim(0, epochs); ax.set_ylim(0, 2.8)\\n"
            "ax.set_xlabel('Epoch'); ax.set_ylabel('Loss')\\n"
            "ax.set_title('Model Training Progress (animated)')\\n"
            "tl, = ax.plot([], [], 'b-', label='Train')\\n"
            "vl, = ax.plot([], [], 'r-', label='Val')\\n"
            "ax.legend()\\n\\n"
            "def update(frame):\\n"
            "    tl.set_data(range(frame+1), train_loss[:frame+1])\\n"
            "    vl.set_data(range(frame+1), val_loss[:frame+1])\\n"
            "    return tl, vl\\n\\n"
            "ani = animation.FuncAnimation(fig, update, frames=epochs, interval=60, blit=True)\\n"
            "try:\\n"
            "    ani.save('training_progress.gif', writer='pillow', fps=20)\\n"
            "    print('Saved training_progress.gif')\\n"
            "except Exception as e:\\n"
            "    print(f'Animation built ({e})')\\n"
            "plt.close()"
        ),
        "practice": {
            "title": "Bouncing Ball Animation",
            "desc": "Animate a ball under gravity (g=9.8). Start at y=5, vy=0. Update position each frame with dt=0.05. Reverse vy on bounce at y=0. Save 100 frames to 'bounce.gif'.",
            "starter": (
                "import matplotlib\\n"
                "matplotlib.use('Agg')\\n"
                "import matplotlib.pyplot as plt\\n"
                "import matplotlib.animation as animation\\n"
                "import numpy as np\\n\\n"
                "fig, ax = plt.subplots(figsize=(4, 6))\\n"
                "ax.set_xlim(0, 1); ax.set_ylim(-0.2, 5.5)\\n"
                "ball, = ax.plot([0.5], [5], 'bo', ms=15)\\n"
                "dt = 0.05; g = 9.8\\n"
                "y, vy = 5.0, 0.0\\n\\n"
                "# TODO: define update(frame) that applies gravity, reverses on bounce\\n"
                "# TODO: FuncAnimation for 100 frames\\n"
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
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import numpy as np\\n\\n"
                    "x = np.linspace(0, 4*np.pi, 200)\\n"
                    "styles = ['seaborn-v0_8-paper', 'ggplot', 'bmh']\\n"
                    "fig, axes = plt.subplots(1, 3, figsize=(13, 4))\\n"
                    "for ax, style in zip(axes, styles):\\n"
                    "    with plt.style.context(style):\\n"
                    "        ax.plot(x, np.sin(x), label='sin')\\n"
                    "        ax.plot(x, np.cos(x), label='cos')\\n"
                    "        ax.set_title(style.split('_')[-1])\\n"
                    "        ax.legend(fontsize=8)\\n"
                    "fig.tight_layout()\\n"
                    "fig.savefig('styles_compare.png', dpi=120, bbox_inches='tight')\\n"
                    "print('Saved styles_compare.png')\\n"
                    "plt.close()"
                )
            },
            {
                "label": "LaTeX math in axis labels and titles",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import numpy as np\\n\\n"
                    "fig, ax = plt.subplots(figsize=(6, 4))\\n"
                    "x = np.linspace(0.1, 3, 200)\\n"
                    "ax.plot(x, np.exp(-x**2), label=r'$f(x) = e^{-x^2}$', lw=2)\\n"
                    "ax.plot(x, 1/(1+x**2), label=r'$g(x) = \\\\frac{1}{1+x^2}$', lw=2, ls='--')\\n"
                    "ax.set_xlabel(r'$x$ (normalized)', fontsize=12)\\n"
                    "ax.set_ylabel(r'$f(x)$', fontsize=12)\\n"
                    "ax.set_title(r'Gaussian vs Lorentzian decay', fontsize=13)\\n"
                    "ax.legend(fontsize=11); ax.grid(True, alpha=0.3)\\n"
                    "fig.tight_layout()\\n"
                    "fig.savefig('latex_labels.png', dpi=150, bbox_inches='tight')\\n"
                    "print('Saved latex_labels.png')\\n"
                    "plt.close()"
                )
            },
            {
                "label": "Shared-axes multi-panel figure",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import numpy as np\\n\\n"
                    "np.random.seed(42)\\n"
                    "fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharex=True, sharey=True)\\n"
                    "for i, ax in enumerate(axes.flat):\\n"
                    "    data = np.random.normal(i, 1.2, 80)\\n"
                    "    ax.hist(data, bins=18, edgecolor='k', alpha=0.7)\\n"
                    "    ax.axvline(data.mean(), color='red', ls='--', lw=1.2)\\n"
                    "    ax.set_title(f'Group {i+1} (\\u03bc={i})', fontsize=10)\\n"
                    "fig.suptitle('Shared-Axis Multi-Panel', fontsize=14, fontweight='bold')\\n"
                    "fig.tight_layout()\\n"
                    "fig.savefig('multi_panel.png', dpi=120, bbox_inches='tight')\\n"
                    "print('Saved multi_panel.png')\\n"
                    "plt.close()"
                )
            },
            {
                "label": "High-DPI export with serif fonts",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import numpy as np\\n\\n"
                    "plt.rcParams.update({'font.family': 'serif', 'font.size': 10,\\n"
                    "                     'axes.linewidth': 1.2, 'xtick.major.width': 1.2})\\n"
                    "np.random.seed(42)\\n"
                    "groups = ['Control', 'Drug A', 'Drug B']\\n"
                    "means = [2.1, 3.4, 2.9]; stds = [0.3, 0.4, 0.35]\\n"
                    "fig, ax = plt.subplots(figsize=(4.5, 3.5))\\n"
                    "bars = ax.bar(groups, means, yerr=stds, capsize=5,\\n"
                    "              color=['#4878D0','#EE854A','#6ACC65'], edgecolor='k', lw=0.8)\\n"
                    "for b, m in zip(bars, means):\\n"
                    "    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.06,\\n"
                    "            f'{m:.1f}', ha='center', fontsize=9)\\n"
                    "ax.set_ylabel(r'Response ($\\u03bcmol/L)', fontsize=11)\\n"
                    "ax.set_title('Treatment Effect', fontsize=12)\\n"
                    "ax.spines[['top','right']].set_visible(False)\\n"
                    "fig.tight_layout()\\n"
                    "fig.savefig('publication_fig.png', dpi=300, bbox_inches='tight')\\n"
                    "print('Saved publication_fig.png at 300 DPI')\\n"
                    "plt.close()"
                )
            }
        ],
        "rw_scenario": "Your paper submission requires 300 DPI figures with serif fonts, LaTeX-formatted axes, and figures no wider than 5 inches with consistent styling.",
        "rw_code": (
            "import matplotlib\\n"
            "matplotlib.use('Agg')\\n"
            "import matplotlib.pyplot as plt\\n"
            "import numpy as np\\n\\n"
            "plt.style.use('seaborn-v0_8-paper')\\n"
            "plt.rcParams.update({'font.family':'serif','font.size':10,'axes.linewidth':1.2})\\n"
            "np.random.seed(42)\\n"
            "t = np.linspace(0, 10, 300)\\n"
            "models = {\\n"
            "    r'$\\\\alpha$-decay': np.exp(-0.3*t) + np.random.randn(300)*0.02,\\n"
            "    r'$\\\\beta$-decay':  np.exp(-0.5*t) + np.random.randn(300)*0.02,\\n"
            "    r'$\\\\gamma$-decay': np.exp(-0.8*t) + np.random.randn(300)*0.02,\\n"
            "}\\n"
            "fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))\\n"
            "for label, y in models.items():\\n"
            "    axes[0].plot(t, y, lw=1.5, label=label)\\n"
            "axes[0].set_xlabel(r'$t$ (s)'); axes[0].set_ylabel(r'$N(t)/N_0$')\\n"
            "axes[0].set_title('Linear Scale'); axes[0].legend(fontsize=9)\\n"
            "axes[0].spines[['top','right']].set_visible(False)\\n"
            "for label, y in models.items():\\n"
            "    axes[1].semilogy(t, np.clip(y, 1e-4, 2), lw=1.5, label=label)\\n"
            "axes[1].set_xlabel(r'$t$ (s)'); axes[1].set_ylabel(r'$\\\\log N/N_0$')\\n"
            "axes[1].set_title('Log Scale'); axes[1].legend(fontsize=9)\\n"
            "axes[1].spines[['top','right']].set_visible(False)\\n"
            "fig.suptitle(r'Radioactive Decay: $\\\\alpha$, $\\\\beta$, $\\\\gamma$', fontsize=13, fontweight='bold')\\n"
            "fig.tight_layout()\\n"
            "fig.savefig('journal_decay.png', dpi=300, bbox_inches='tight')\\n"
            "print('Saved journal_decay.png at 300 DPI')\\n"
            "plt.close()"
        ),
        "practice": {
            "title": "2-Panel with Inset Zoom",
            "desc": "Plot y = e^{-0.1t}*sin(2t) on linear and log scales. Add an inset zoom on t=[0,2] in the linear panel. Use seaborn-v0_8-paper style, serif fonts, and export at 300 DPI.",
            "starter": (
                "import matplotlib\\n"
                "matplotlib.use('Agg')\\n"
                "import matplotlib.pyplot as plt\\n"
                "from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset\\n"
                "import numpy as np\\n\\n"
                "t = np.linspace(0, 20, 500)\\n"
                "y = np.exp(-0.1*t) * np.sin(2*t)\\n"
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))\\n"
                "# TODO: ax1 linear plot + inset zoom t in [0,2]\\n"
                "# TODO: ax2 semilogy plot\\n"
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
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import matplotlib.colors as mcolors\\n"
                    "import numpy as np\\n\\n"
                    "colors = ['#1a1a2e','#16213e','#0f3460','#e94560']\\n"
                    "cmap = mcolors.LinearSegmentedColormap.from_list('dark_red', colors, N=256)\\n"
                    "np.random.seed(0)\\n"
                    "data = np.random.randn(40, 40).cumsum(axis=0)\\n"
                    "fig, ax = plt.subplots(figsize=(6, 4))\\n"
                    "im = ax.imshow(data, cmap=cmap, aspect='auto')\\n"
                    "plt.colorbar(im, ax=ax, label='Value')\\n"
                    "ax.set_title('Custom Dark-Red Colormap')\\n"
                    "fig.savefig('custom_cmap.png', dpi=120, bbox_inches='tight')\\n"
                    "print('Saved custom_cmap.png')\\n"
                    "plt.close()"
                )
            },
            {
                "label": "TwoSlopeNorm for asymmetric diverging maps",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import matplotlib.colors as mcolors\\n"
                    "import numpy as np\\n\\n"
                    "np.random.seed(42)\\n"
                    "data = np.random.randn(20, 20) * 3 + 1\\n"
                    "vmax = max(abs(data.min()), abs(data.max()))\\n"
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))\\n"
                    "im1 = ax1.imshow(data, cmap='RdBu_r', vmin=-vmax, vmax=vmax)\\n"
                    "ax1.set_title('Symmetric Norm'); plt.colorbar(im1, ax=ax1)\\n"
                    "norm = mcolors.TwoSlopeNorm(vmin=data.min(), vcenter=0, vmax=data.max())\\n"
                    "im2 = ax2.imshow(data, cmap='RdBu_r', norm=norm)\\n"
                    "ax2.set_title('TwoSlopeNorm'); plt.colorbar(im2, ax=ax2)\\n"
                    "fig.tight_layout()\\n"
                    "fig.savefig('diverging_norm.png', dpi=120, bbox_inches='tight')\\n"
                    "print('Saved diverging_norm.png')\\n"
                    "plt.close()"
                )
            },
            {
                "label": "Discrete colorbar with BoundaryNorm",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import matplotlib.colors as mcolors\\n"
                    "import numpy as np\\n\\n"
                    "bounds = [0, 1, 2, 3, 4, 5]\\n"
                    "cmap = plt.get_cmap('RdYlGn', len(bounds)-1)\\n"
                    "norm = mcolors.BoundaryNorm(bounds, cmap.N)\\n"
                    "levels = ['None','Low','Med','High','Max']\\n"
                    "np.random.seed(7)\\n"
                    "data = np.random.randint(0, 5, (8, 10))\\n"
                    "fig, ax = plt.subplots(figsize=(9, 5))\\n"
                    "im = ax.imshow(data, cmap=cmap, norm=norm)\\n"
                    "cbar = plt.colorbar(im, ax=ax, boundaries=bounds, ticks=[0.5,1.5,2.5,3.5,4.5])\\n"
                    "cbar.set_ticklabels(levels)\\n"
                    "for i in range(data.shape[0]):\\n"
                    "    for j in range(data.shape[1]):\\n"
                    "        ax.text(j, i, levels[data[i,j]][:3],\\n"
                    "                ha='center', va='center', fontsize=8)\\n"
                    "ax.set_title('Discrete Risk Heatmap')\\n"
                    "fig.savefig('discrete_cmap.png', dpi=120, bbox_inches='tight')\\n"
                    "print('Saved discrete_cmap.png')\\n"
                    "plt.close()"
                )
            },
            {
                "label": "Perceptually uniform colormap comparison",
                "code": (
                    "import matplotlib\\n"
                    "matplotlib.use('Agg')\\n"
                    "import matplotlib.pyplot as plt\\n"
                    "import numpy as np\\n\\n"
                    "cmaps = ['viridis', 'plasma', 'inferno', 'cividis']\\n"
                    "x = y = np.linspace(-np.pi, np.pi, 200)\\n"
                    "X, Y = np.meshgrid(x, y)\\n"
                    "Z = np.sin(X) * np.cos(Y)\\n"
                    "fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))\\n"
                    "for ax, cm in zip(axes, cmaps):\\n"
                    "    im = ax.imshow(Z, cmap=cm, aspect='auto')\\n"
                    "    ax.set_title(cm)\\n"
                    "    plt.colorbar(im, ax=ax, fraction=0.046)\\n"
                    "fig.suptitle('Perceptually Uniform Colormaps', fontsize=12)\\n"
                    "fig.tight_layout()\\n"
                    "fig.savefig('perceptual_cmaps.png', dpi=120, bbox_inches='tight')\\n"
                    "print('Saved perceptual_cmaps.png')\\n"
                    "plt.close()"
                )
            }
        ],
        "rw_scenario": "Your risk dashboard uses corporate colors and needs a discrete heatmap with 5 severity levels, text labels in each cell, and a custom colorbar legend.",
        "rw_code": (
            "import matplotlib\\n"
            "matplotlib.use('Agg')\\n"
            "import matplotlib.pyplot as plt\\n"
            "import matplotlib.colors as mcolors\\n"
            "import numpy as np\\n\\n"
            "CORP = ['#2ecc71','#f1c40f','#e67e22','#e74c3c','#8e44ad']\\n"
            "LEVELS = ['OK','Watch','Warn','Alert','Critical']\\n"
            "cmap = mcolors.ListedColormap(CORP)\\n"
            "norm = mcolors.BoundaryNorm(list(range(6)), cmap.N)\\n"
            "np.random.seed(42)\\n"
            "comps = [f'SVC-{i:02d}' for i in range(1, 11)]\\n"
            "times = [f'T+{i}h' for i in range(5)]\\n"
            "risk = np.random.randint(0, 5, (len(comps), len(times)))\\n"
            "fig, ax = plt.subplots(figsize=(8, 6))\\n"
            "im = ax.imshow(risk, cmap=cmap, norm=norm)\\n"
            "cbar = plt.colorbar(im, ax=ax, boundaries=list(range(6)), ticks=[0.5,1.5,2.5,3.5,4.5])\\n"
            "cbar.set_ticklabels(LEVELS); cbar.set_label('Risk Level')\\n"
            "ax.set_xticks(range(len(times))); ax.set_xticklabels(times)\\n"
            "ax.set_yticks(range(len(comps))); ax.set_yticklabels(comps)\\n"
            "for i in range(len(comps)):\\n"
            "    for j in range(len(times)):\\n"
            "        lvl = risk[i,j]\\n"
            "        ax.text(j, i, LEVELS[lvl], ha='center', va='center',\\n"
            "                fontsize=8, color='white' if lvl >= 2 else 'black')\\n"
            "ax.set_title('System Risk Dashboard', fontsize=13, fontweight='bold')\\n"
            "fig.tight_layout()\\n"
            "fig.savefig('risk_dashboard.png', dpi=150, bbox_inches='tight')\\n"
            "print('Saved risk_dashboard.png')\\n"
            "plt.close()"
        ),
        "practice": {
            "title": "Custom Terrain Colormap",
            "desc": "Create a colormap: blue → green → yellow → brown → white. Apply to a sin(X)*cos(Y) surface. Add a colorbar with 5 ticks labeled: Sea, Lowland, Hills, Mountain, Snow.",
            "starter": (
                "import matplotlib\\n"
                "matplotlib.use('Agg')\\n"
                "import matplotlib.pyplot as plt\\n"
                "import matplotlib.colors as mcolors\\n"
                "import numpy as np\\n\\n"
                "colors = ['#1a6b9a','#2ecc71','#f1c40f','#8b5e3c','#f5f5f5']\\n"
                "cmap = mcolors.LinearSegmentedColormap.from_list('terrain_custom', colors)\\n"
                "x = y = np.linspace(-3, 3, 100)\\n"
                "X, Y = np.meshgrid(x, y)\\n"
                "Z = np.sin(X) + np.cos(Y)\\n"
                "# TODO: imshow with custom cmap\\n"
                "# TODO: colorbar with 5 labeled ticks\\n"
                "# TODO: save 'terrain.png' at 150 DPI"
            )
        }
    },
'''

with open(FILEPATH, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.rfind(MARKER)
if idx == -1:
    print("ERROR: marker not found!")
else:
    new_content = content[:idx] + NEW_SECTIONS + content[idx:]
    with open(FILEPATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"SUCCESS: 3 sections inserted into {FILEPATH}")
