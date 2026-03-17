import sys
sys.path.insert(0, r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
from _inserter import insert_sections

FILEPATH = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_seaborn.py"
MARKER = "]  # end SECTIONS"

SECTIONS = '''    {
        "title": "14. FacetGrid & PairGrid",
        "examples": [
            {
                "label": "FacetGrid with histogram per group",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({'value': np.random.randn(300), 'group': np.repeat(['A','B','C'], 100)})\ng = sns.FacetGrid(df, col='group', height=3.5, aspect=0.9)\ng.map(sns.histplot, 'value', kde=True, bins=20)\ng.set_titles(col_template='{col_name}')\ng.figure.suptitle('FacetGrid by Group', y=1.02)\ng.savefig('facetgrid_hist.png', dpi=100, bbox_inches='tight')\nprint('Saved facetgrid_hist.png')\nplt.close('all')"
            },
            {
                "label": "FacetGrid row x col (2D grid)",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\ntips = sns.load_dataset('tips')\ng = sns.FacetGrid(tips, row='sex', col='time', height=3, aspect=1.2, margin_titles=True)\ng.map(sns.scatterplot, 'total_bill', 'tip', alpha=0.6)\ng.add_legend()\ng.savefig('facetgrid_2d.png', dpi=100, bbox_inches='tight')\nprint('Saved facetgrid_2d.png')\nplt.close('all')"
            },
            {
                "label": "PairGrid with mixed plot types",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\niris = sns.load_dataset('iris')\ng = sns.PairGrid(iris, hue='species', vars=['sepal_length','petal_length','petal_width'])\ng.map_upper(sns.scatterplot, alpha=0.6)\ng.map_lower(sns.kdeplot, fill=True, alpha=0.4)\ng.map_diag(sns.histplot, kde=True)\ng.add_legend()\ng.savefig('pairgrid_mixed.png', dpi=80, bbox_inches='tight')\nprint('Saved pairgrid_mixed.png')\nplt.close('all')"
            },
            {
                "label": "FacetGrid with custom mapping function",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\ndef scatter_with_mean(x, y, **kwargs):\n    plt.scatter(x, y, alpha=0.5, **{k:v for k,v in kwargs.items() if k != 'label'})\n    plt.axhline(y.mean(), color='red', ls='--', lw=1.5)\n    plt.axvline(x.mean(), color='blue', ls='--', lw=1.5)\n\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.randn(150), 'y': np.random.randn(150),\n                   'group': np.repeat(['G1','G2','G3'], 50)})\ng = sns.FacetGrid(df, col='group', height=3)\ng.map(scatter_with_mean, 'x', 'y')\ng.figure.suptitle('Scatter with Group Means', y=1.02)\ng.savefig('facetgrid_custom_fn.png', dpi=100, bbox_inches='tight')\nprint('Saved facetgrid_custom_fn.png')\nplt.close('all')"
            }
        ],
        "rw_scenario": "You have sales data across 3 regions and 4 product lines. You need a grid of scatter plots comparing revenue vs units sold for each region-product combination.",
        "rw_code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\nregions = ['North','South','East']\nproducts = ['Electronics','Apparel','Food','Sports']\nrows = []\nfor r in regions:\n    for p in products:\n        n = 25\n        rows.append(pd.DataFrame({'region':r,'product':p,\n                                   'revenue':np.random.exponential(500,n)+100,\n                                   'units':np.random.randint(10,200,n)}))\ndf = pd.concat(rows, ignore_index=True)\ng = sns.FacetGrid(df, row='region', col='product', height=2.2, aspect=1.1, margin_titles=True)\ng.map(sns.scatterplot, 'units', 'revenue', alpha=0.5, s=20)\ng.map(sns.regplot, 'units', 'revenue', scatter=False, color='red', ci=None)\ng.set_titles(row_template='{row_name}', col_template='{col_name}')\ng.figure.suptitle('Revenue vs Units by Region x Product', y=1.01, fontsize=12)\ng.savefig('sales_facetgrid.png', dpi=100, bbox_inches='tight')\nprint('Saved sales_facetgrid.png')\nplt.close('all')",
        "practice": {
            "title": "Titanic FacetGrid",
            "desc": "Load the titanic dataset. Create a FacetGrid with pclass as columns (3 panels) showing age distribution using histplot. Color by survived using hue. Set appropriate titles and save.",
            "starter": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\ntitanic = sns.load_dataset('titanic').dropna(subset=['age'])\n# TODO: FacetGrid col='pclass', hue='survived', map histplot 'age'\n# TODO: add_legend, suptitle, save 'titanic_facet.png'"
        }
    },
    {
        "title": "15. Statistical Visualization Deep Dive",
        "examples": [
            {
                "label": "Violin + swarmplot overlay",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\ndf = pd.DataFrame({'score': np.concatenate([np.random.normal(70,10,80), np.random.normal(75,8,80), np.random.normal(65,12,80)]),\n                   'class': ['A']*80 + ['B']*80 + ['C']*80})\nfig, ax = plt.subplots(figsize=(7, 5))\nsns.violinplot(data=df, x='class', y='score', inner=None, palette='muted', alpha=0.7, ax=ax)\nsns.swarmplot(data=df, x='class', y='score', color='black', size=2.5, alpha=0.6, ax=ax)\nax.set_title('Score Distribution by Class (Violin + Swarm)')\nfig.savefig('violin_swarm.png', dpi=100, bbox_inches='tight')\nprint('Saved violin_swarm.png')\nplt.close()"
            },
            {
                "label": "ECDF comparison across groups",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({'response_ms': np.concatenate([np.random.exponential(200,300), np.random.exponential(150,300), np.random.exponential(300,300)]),\n                   'server': ['A']*300 + ['B']*300 + ['C']*300})\nfig, ax = plt.subplots(figsize=(8, 5))\nsns.ecdfplot(data=df, x='response_ms', hue='server', ax=ax)\nax.axvline(200, color='gray', ls=':', label='200ms target')\nax.set_title('ECDF: Response Time by Server')\nax.set_xlabel('Response Time (ms)')\nax.legend()\nfig.savefig('ecdf_comparison.png', dpi=100, bbox_inches='tight')\nprint('Saved ecdf_comparison.png')\nplt.close()"
            },
            {
                "label": "Residual plot for regression diagnostics",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nnp.random.seed(42)\nx = np.linspace(0, 10, 100)\ny = 2*x + np.random.normal(0, 2, 100)\nfig, axes = plt.subplots(1, 2, figsize=(11, 4))\nsns.regplot(x=x, y=y, ax=axes[0])\naxes[0].set_title('Regression with CI')\nsns.residplot(x=x, y=y, ax=axes[1])\naxes[1].axhline(0, color='red', ls='--')\naxes[1].set_title('Residuals vs Fitted')\nfig.tight_layout()\nfig.savefig('residual_diagnostic.png', dpi=100, bbox_inches='tight')\nprint('Saved residual_diagnostic.png')\nplt.close()"
            },
            {
                "label": "Box plot with significance annotations",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({'value': np.concatenate([np.random.normal(5,1,50), np.random.normal(7,1.5,50), np.random.normal(6.2,1.2,50)]),\n                   'group': ['Control']*50 + ['Drug A']*50 + ['Drug B']*50})\nfig, ax = plt.subplots(figsize=(7, 5))\nsns.boxplot(data=df, x='group', y='value', palette='Set2', ax=ax)\ny_max = df['value'].max() + 0.5\nax.plot([0, 1], [y_max, y_max], 'k-', lw=1.5)\nax.text(0.5, y_max+0.1, '***', ha='center', fontsize=14)\nax.set_title('Drug Effect (with significance bracket)')\nfig.savefig('boxplot_sig.png', dpi=100, bbox_inches='tight')\nprint('Saved boxplot_sig.png')\nplt.close()"
            }
        ],
        "rw_scenario": "You're presenting A/B test results for 3 landing page variants. Need violin plots, ECDF comparisons, and regression residuals for a comprehensive statistical report.",
        "rw_code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\nvariants = {'Control':(3.2,1.1),'Variant A':(3.8,1.3),'Variant B':(3.5,0.9)}\ndfs = [pd.DataFrame({'conversion':np.random.normal(mu,sig,200).clip(0,10),'variant':name})\n       for name,(mu,sig) in variants.items()]\ndf = pd.concat(dfs, ignore_index=True)\n\nfig, axes = plt.subplots(1, 3, figsize=(15, 5))\nsns.violinplot(data=df, x='variant', y='conversion', inner='quartile', palette='muted', ax=axes[0])\naxes[0].set_title('Violin Plot')\nsns.ecdfplot(data=df, x='conversion', hue='variant', ax=axes[1])\naxes[1].axvline(3.5, color='gray', ls='--', alpha=0.7)\naxes[1].set_title('ECDF Comparison')\nsns.boxplot(data=df, x='variant', y='conversion', palette='Set2', ax=axes[2])\naxes[2].set_title('Box Plot')\nfig.suptitle('A/B Test Analysis', fontsize=14, fontweight='bold')\nfig.tight_layout()\nfig.savefig('ab_test.png', dpi=100, bbox_inches='tight')\nprint('Saved ab_test.png')\nplt.close()",
        "practice": {
            "title": "Multi-Stat Figure",
            "desc": "Create a 3-panel figure: (1) strip plot of scores by group with means marked, (2) ECDF of scores for 3 groups, (3) residual plot from regressing score on study_hours. Use whitegrid style.",
            "starter": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({'score': np.random.normal(70, 15, 150), 'group': np.repeat(['A','B','C'], 50), 'study_hours': np.random.uniform(1, 8, 150)})\n# TODO: 3-panel figure with stripplot, ecdfplot, residplot\n# TODO: save to 'multi_stat.png'"
        }
    },
    {
        "title": "16. Custom Seaborn Themes & Styling",
        "examples": [
            {
                "label": "Context comparison (paper/notebook/talk/poster)",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})\nfig, axes = plt.subplots(2, 2, figsize=(12, 9))\nfor ax, ctx in zip(axes.flat, ['paper','notebook','talk','poster']):\n    with sns.plotting_context(ctx):\n        sns.scatterplot(data=df, x='x', y='y', ax=ax, alpha=0.6)\n        ax.set_title(f'Context: {ctx}')\nfig.suptitle('Seaborn Contexts', fontsize=14)\nfig.tight_layout()\nfig.savefig('contexts.png', dpi=100, bbox_inches='tight')\nprint('Saved contexts.png')\nplt.close()"
            },
            {
                "label": "Custom set_theme with dark background",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nsns.set_theme(style='darkgrid', palette='bright', font_scale=1.1,\n              rc={'axes.facecolor':'#1e1e2e','figure.facecolor':'#1e1e2e',\n                  'text.color':'white','axes.labelcolor':'white',\n                  'xtick.color':'white','ytick.color':'white',\n                  'grid.color':'#333355','axes.edgecolor':'#555577'})\nnp.random.seed(42)\ndf = pd.DataFrame({'x':np.random.randn(200),'y':np.random.randn(200),'g':np.random.choice(['A','B','C'],200)})\nfig, ax = plt.subplots(figsize=(7,5))\nsns.scatterplot(data=df, x='x', y='y', hue='g', alpha=0.7, ax=ax)\nax.set_title('Dark Mode Plot')\nfig.savefig('dark_theme.png', dpi=100, bbox_inches='tight')\nprint('Saved dark_theme.png')\nsns.set_theme()  # reset\nplt.close()"
            },
            {
                "label": "Custom color palettes (husl, cubehelix, custom)",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nfig, axes = plt.subplots(2, 2, figsize=(12, 8))\ntips = sns.load_dataset('tips')\npalettes = [('Blues',4), ('husl',4), ('Set1',4), (['#FF6B6B','#4ECDC4','#45B7D1','#96CEB4'],4)]\ntitles = ['Blues (seq)','HUSL (qual)','Set1 (qual)','Custom hex']\nfor ax, (pal, _), title in zip(axes.flat, palettes, titles):\n    with sns.axes_style('whitegrid'):\n        sns.boxplot(data=tips, x='day', y='total_bill', palette=pal, ax=ax)\n        ax.set_title(title)\nfig.tight_layout()\nfig.savefig('palettes.png', dpi=100, bbox_inches='tight')\nprint('Saved palettes.png')\nplt.close()"
            },
            {
                "label": "Despine and axis trimming",
                "code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nnp.random.seed(42)\ndf = pd.DataFrame({'x':np.repeat(range(5),30), 'y':np.random.randn(150)+np.repeat([1,2,3,4,5],30)})\nfig, axes = plt.subplots(1,2, figsize=(12,5))\nwith sns.axes_style('ticks'):\n    sns.boxplot(data=df, x='x', y='y', ax=axes[0], palette='pastel')\n    sns.despine(ax=axes[0], trim=True)\n    axes[0].set_title('Despined + trimmed')\nwith sns.axes_style('whitegrid'):\n    sns.violinplot(data=df, x='x', y='y', ax=axes[1], palette='muted', inner='box')\n    sns.despine(ax=axes[1], left=False, bottom=False, top=True, right=True)\n    axes[1].set_title('Whitegrid + partial despine')\nfig.tight_layout()\nfig.savefig('despine.png', dpi=100, bbox_inches='tight')\nprint('Saved despine.png')\nplt.close()"
            }
        ],
        "rw_scenario": "Your company's brand guide specifies 5 hex colors, no top/right chart borders, consistent font scale, and all reports must use the 'ticks' style.",
        "rw_code": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nBRAND = ['#003366','#0066CC','#3399FF','#66B2FF','#99CCFF']\nsns.set_theme(style='whitegrid', palette=BRAND, font_scale=1.2,\n              rc={'font.family':'sans-serif','axes.spines.top':False,'axes.spines.right':False})\nnp.random.seed(42)\ndepts = ['Eng','Sales','Mktg','Support','HR']\ndf = pd.DataFrame({'dept':np.repeat(depts,40), 'satisfaction':np.random.normal(np.tile([7.5,6.8,7.2,6.5,7.8],40).reshape(40,5).flatten()[:200], 1.0)})\nfig, axes = plt.subplots(1, 2, figsize=(14,5))\nsns.barplot(data=df, x='dept', y='satisfaction', palette=BRAND, ax=axes[0])\naxes[0].set_title('Employee Satisfaction by Dept', fontweight='bold')\nsns.violinplot(data=df, x='dept', y='satisfaction', palette=BRAND, inner='box', ax=axes[1])\naxes[1].set_title('Satisfaction Distribution', fontweight='bold')\nfig.suptitle('Q4 Employee Survey', fontsize=16, fontweight='bold', y=1.02)\nfig.tight_layout()\nfig.savefig('brand_report.png', dpi=120, bbox_inches='tight')\nprint('Saved brand_report.png')\nsns.set_theme()\nplt.close()",
        "practice": {
            "title": "Night Mode Report",
            "desc": "Create a dark-themed (set_theme with dark facecolor) 3-panel figure: histogram, scatter, and bar chart. Use a bright color palette. Add a figure title and save at 150 DPI.",
            "starter": "import seaborn as sns\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\n# TODO: set_theme with dark background rc params\n# TODO: 3-panel: histplot, scatterplot, barplot\n# TODO: suptitle, tight_layout, save 'night_report.png' 150 DPI\n# TODO: sns.set_theme() to reset at end"
        }
    },
'''

insert_sections(FILEPATH, MARKER, SECTIONS)
