#!/usr/bin/env python3
"""
Patch gen_matplotlib.py and gen_seaborn.py:
1. Update make_html() to render todos_html
2. Add "todos" list to every section dict
"""

import re

# ─────────────────────────────────────────────────────────────────────────────
# Helper: patch make_html() in a file string
# ─────────────────────────────────────────────────────────────────────────────
OLD_CARDS = (
    "        cards += (f'<div class=\"topic\" id=\"s{i}\"><div class=\"th\" onclick=\"tog(this)\"><span>{esc(s[\"title\"])}</span>'\n"
    "                  f'<span class=\"arr\">&#9660;</span></div><div class=\"tb\"><p class=\"desc\">{esc(s.get(\"desc\",\"\"))}</p>'\n"
    "                  f'{blks}{rw_html}{practice_html}</div></div>')"
)

NEW_CARDS = (
    "        todos = s.get(\"todos\", [])\n"
    "        todos_html = \"\"\n"
    "        if todos:\n"
    "            items = \"\\n\".join(\n"
    "                f'<li><label><input type=\"checkbox\"> {esc(t)}</label></li>'\n"
    "                for t in todos\n"
    "            )\n"
    "            todos_html = (\n"
    "                f'<div class=\"todo-list\">'\n"
    "                f'<div class=\"todo-head\">&#x2705; Practice Checklist</div>'\n"
    "                f'<ul>{items}</ul>'\n"
    "                f'</div>'\n"
    "            )\n"
    "        cards += (f'<div class=\"topic\" id=\"s{i}\"><div class=\"th\" onclick=\"tog(this)\"><span>{esc(s[\"title\"])}</span>'\n"
    "                  f'<span class=\"arr\">&#9660;</span></div><div class=\"tb\"><p class=\"desc\">{esc(s.get(\"desc\",\"\"))}</p>'\n"
    "                  f'{blks}{rw_html}{practice_html}{todos_html}</div></div>')"
)

# ─────────────────────────────────────────────────────────────────────────────
# Todos for gen_matplotlib.py (32 sections)
# ─────────────────────────────────────────────────────────────────────────────
MPL_TODOS = {
    "1. Line Plot": [
        "Plot sin(x) and cos(x) on the same axes with different colors and linestyles",
        "Add a fill_between() confidence band around a noisy signal",
        "Use errorbar() to show mean ± std for 6 data points",
        "Apply a 7-point moving average to a random walk and overlay both lines",
        "Save the figure as both PNG (dpi=150) and SVG, then compare file sizes",
    ],
    "2. Bar Chart": [
        "Create a vertical bar chart with value labels above each bar",
        "Build a grouped bar chart for 3 products across 4 quarters",
        "Make a horizontal bar chart sorted by value (largest at top)",
        "Add error bars to each bar using yerr= with random standard deviations",
        "Color bars conditionally: green if value ≥ 70, orange if ≥ 50, red otherwise",
    ],
    "3. Scatter Plot": [
        "Create a scatter plot of 200 points with color mapped to a third numeric variable",
        "Add a least-squares regression line using np.polyfit() and np.polyval()",
        "Build a bubble chart where marker size encodes a fourth variable",
        "Use hexbin() to handle overplotting for 5,000 points and add a colorbar",
        "Annotate the point with the highest y-value using ax.annotate() with an arrow",
    ],
    "4. Histogram": [
        "Plot a histogram with density=True and overlay the manually computed normal PDF",
        "Compare two overlapping histograms using alpha=0.6 and different colors",
        "Switch histtype between 'bar', 'step', and 'stepfilled' — observe the differences",
        "Plot a cumulative histogram and overlay the theoretical CDF for exponential data",
        "Add vertical dashed lines for the mean and ±1 standard deviation",
    ],
    "5. Subplots": [
        "Create a 2x2 subplot grid with four different chart types and a global suptitle",
        "Share x-axis across two vertically stacked subplots using sharex=True",
        "Use GridSpec to make one wide panel spanning the top row and three below",
        "Adjust spacing between subplots using plt.tight_layout() and subplots_adjust(hspace=)",
        "Save the multi-panel figure as both PNG and PDF using savefig()",
    ],
    "6. Figure Customization": [
        "Remove the top and right spines from a line plot for a cleaner look",
        "Format the y-axis as currency (e.g., '$42K') using matplotlib.ticker.FuncFormatter",
        "Annotate the peak value of a time series with an arrow using ax.annotate()",
        "Rotate x-axis tick labels 45 degrees using set_xticklabels with rotation=45",
        "Add color-shaded background regions for each quarter using axvspan()",
    ],
    "7. Pie & Donut Chart": [
        "Create a pie chart with 5 slices, explode the largest slice by 0.08",
        "Convert the pie to a donut by setting wedgeprops=dict(width=0.5)",
        "Add a center text label inside the donut showing the total value",
        "Build a nested (two-ring) donut chart for category and subcategory breakdowns",
        "Limit to 5 slices — group all others into an 'Other' slice to avoid clutter",
    ],
    "8. Heatmap with imshow/pcolor": [
        "Create a correlation heatmap using imshow with the 'coolwarm' colormap",
        "Annotate each cell with its value using ax.text() in a nested loop",
        "Use pcolormesh to show a 10x12 monthly returns matrix with a diverging colormap",
        "Build a GitHub-style activity calendar heatmap using a custom LinearSegmentedColormap",
        "Rotate x-axis tick labels 45 degrees and adjust alignment with ha='right'",
    ],
    "9. Twin Axes & Secondary Y-Axis": [
        "Create a dual-axis plot: bar chart for revenue on the left, line for margin% on the right",
        "Color each y-axis label to match its corresponding data series",
        "Combine legends from both axes into a single legend using get_legend_handles_labels()",
        "Add a shaded axvspan() event region that spans both y-axes simultaneously",
        "Use twinx() to overlay temperature (line) and humidity (dashed line) on a 24-hour plot",
    ],
    "10. Saving Figures & Style Sheets": [
        "Save a figure as PNG at 72, 150, and 300 DPI and compare file sizes",
        "Use plt.style.context('seaborn-v0_8-whitegrid') to apply a style to one figure only",
        "Export a figure as SVG with matplotlib.rcParams['svg.fonttype'] = 'none'",
        "Use PdfPages to save three plots as a 3-page PDF report",
        "Apply custom rcParams (font.size, axes.spines, grid.alpha) and reset with plt.rcParams.update(plt.rcParamsDefault)",
    ],
    "11. 3D Plotting": [
        "Create a 3D scatter plot of 100 random points with color mapped to the z-axis",
        "Plot the surface Z = sin(sqrt(X^2 + Y^2)) using plot_surface with a 'viridis' colormap",
        "Overlay a contour projection on the floor of a surface plot using contour(zdir='z')",
        "Draw a 3D helix using ax.plot() with x=sin(t), y=cos(t), z=t/(4π)",
        "Add axis labels and a colorbar, then save to PNG using savefig()",
    ],
    "12. Custom Styles & Themes": [
        "Apply three different built-in style sheets to the same chart and compare visually",
        "Define a custom dark theme by updating plt.rcParams with a dark background color",
        "Set a custom color cycle using matplotlib.cycler and confirm it applies to a 5-line chart",
        "Write a context manager that yields a configured (fig, ax) pair for reusable pub styling",
        "Reset all rcParams to defaults using plt.rcParams.update(plt.rcParamsDefault)",
    ],
    "13. Annotations & Text Elements": [
        "Annotate the maximum point on a curve with an arrow using ax.annotate()",
        "Add a text box with a 'round' boxstyle and custom facecolor using ax.text(bbox=...)",
        "Shade a 'crash period' on a time series chart using axvspan with alpha=0.15",
        "Write a LaTeX-formatted y-axis label using r'$f(x) = ...$' syntax",
        "Annotate three events on a price chart with colored vertical dashed lines and labels",
    ],
    "14. Animations & GIF Export": [
        "Create a FuncAnimation that updates a sine wave by shifting the phase each frame",
        "Animate 20 random-walk particles and save to a GIF using writer='pillow'",
        "Use ArtistAnimation to pre-render 10 histogram frames and play them back",
        "Add a frame counter text element that updates each frame using ax.text()",
        "Set blit=True and confirm the animation is faster than without it",
    ],
    "15. Publication-Quality Figures": [
        "Apply 'seaborn-v0_8-paper' style and export the figure at 300 DPI",
        "Use LaTeX math notation in axis labels and titles with r'$...$' strings",
        "Create a 2x3 shared-axis grid and add a common x-label using fig.text()",
        "Add an inset zoom panel using ax.inset_axes() and ax.indicate_inset_zoom()",
        "Switch font to 'serif' via rcParams and compare with the default sans-serif look",
    ],
    "16. Custom Colormaps & Color Science": [
        "Create a custom 4-color LinearSegmentedColormap and apply it to a heatmap",
        "Use TwoSlopeNorm to center a diverging colormap on zero with asymmetric bounds",
        "Build a discrete 5-level BoundaryNorm colormap and annotate each cell with its level label",
        "Compare viridis, plasma, inferno, and cividis on the same 2D data side-by-side",
        "Apply a corporate color palette as a ListedColormap with a custom colorbar legend",
    ],
    "17. Error Bars & Confidence Intervals": [
        "Plot symmetric error bars using ax.errorbar() with capsize=5 and elinewidth=2",
        "Add asymmetric error bars using yerr=[lower_array, upper_array]",
        "Draw a 95% confidence band with fill_between() around a regression line",
        "Overlay multiple confidence bands for three model variants on the same axes",
        "Annotate the error bar with significance stars ('*', '**', '***') using ax.text()",
    ],
    "18. Box Plots & Violin Plots": [
        "Create notched box plots for 5 groups using patch_artist=True and custom colors",
        "Overlay a violin plot and a narrow box plot on the same axes for comparison",
        "Build grouped box plots for two treatments across 4 months",
        "Create a raincloud plot: half-violin + jitter scatter + median line",
        "Color outlier markers differently using flierprops=dict(marker='x', color='red')",
    ],
    "19. Contour Plots": [
        "Plot a filled contour of Z = sin(X)*cos(Y) using contourf with 20 levels and a colorbar",
        "Add labeled contour lines on top of a filled contour using clabel(inline=True)",
        "Visualize a classifier's decision boundary over a 2D feature grid using contourf",
        "Overlay a KDE contour on a scatter plot of bimodal data using gaussian_kde",
        "Add hillshading to a topographic contour map using matplotlib.colors.LightSource",
    ],
    "20. Polar Plots": [
        "Plot a rose curve r = 1 + 0.5*cos(3θ) on a polar axis and fill with alpha=0.2",
        "Create a wind rose bar chart with 16 directions and color bars by magnitude",
        "Build a radar (spider) chart for 6 skills comparing two candidates",
        "Set theta_zero_location='N' and theta_direction=-1 for compass-style orientation",
        "Add a polar scatter plot with exponential radii and an HSV colormap",
    ],
    "21. Stacked Bar & Area Charts": [
        "Create a stacked bar chart for 4 quarters with 3 products using ax.bar() with bottom=",
        "Build a stacked area chart using ax.stackplot() with a custom color list",
        "Normalize a stacked bar to 100% to show share-of-total proportions",
        "Add value labels inside each stacked segment at its vertical midpoint",
        "Compare a stacked bar and 100%-stacked bar side-by-side in a 1x2 subplot",
    ],
    "22. Step Plots & Eventplot": [
        "Plot a step function with where='mid', 'pre', and 'post' side-by-side",
        "Use ax.eventplot() to visualize spike trains for 3 neuron channels",
        "Overlay a step plot on a regular bar chart to compare histogram styles",
        "Add fill_between() shading below a step function using step='mid'",
        "Plot a cumulative step function (ECDF) manually using np.sort() and np.arange()",
    ],
    "23. Log Scale & Symlog": [
        "Switch a plot to log scale using ax.set_yscale('log') and observe axis behavior",
        "Use log-log scale on a scatter plot to reveal a power-law relationship",
        "Apply symlog scale to handle data spanning positive and negative values",
        "Plot an exponential decay on linear and log scale side-by-side to compare",
        "Use np.logspace() to set meaningful tick positions on a log-scale axis",
    ],
    "24. GridSpec & Complex Layouts": [
        "Use GridSpec(2, 3) to create a wide top panel spanning all 3 columns",
        "Specify height_ratios=[3, 1] for a main chart and a smaller indicator below",
        "Use subplot2grid() to place 5 panels of varying sizes in one figure",
        "Add a colorbar axis manually using fig.add_axes([left, bottom, width, height])",
        "Adjust hspace and wspace to control spacing between panels",
    ],
    "25. Hexbin & 2D Density Plots": [
        "Create a hexbin plot of 5,000 points with gridsize=40 and a 'YlOrRd' colormap",
        "Set mincnt=1 to hide empty hexagons in sparse regions",
        "Overlay a hexbin with a scatter at low alpha to show the density gradient",
        "Use hist2d() as an alternative to hexbin and compare the visual output",
        "Add a colorbar labeled 'Count per bin' to the hexbin plot",
    ],
    "26. Patch Artists & Custom Shapes": [
        "Draw a Rectangle patch at (2, 3) with width=4, height=2, and a custom facecolor",
        "Add a Circle patch centered at (0, 0) with radius=1.5 to mark a region of interest",
        "Use FancyArrowPatch to draw a curved arrow between two plot elements",
        "Create a FancyBboxPatch with boxstyle='round,pad=0.1' as a callout annotation",
        "Loop over a list of (x, y, r) tuples and draw multiple Circle patches at once",
    ],
    "27. Quiver & Streamplot": [
        "Plot a 2D vector field using ax.quiver() over a meshgrid of X, Y",
        "Color quiver arrows by vector magnitude using c=np.sqrt(U**2+V**2)",
        "Use ax.streamplot() to visualize flow lines of a vector field",
        "Set linewidth proportional to speed in streamplot using linewidth=speed/speed.max()*2",
        "Normalize vectors before quivering to show direction only, not magnitude",
    ],
    "28. Broken Axis & Dual Axis": [
        "Simulate a broken y-axis using two stacked subplots and hiding the shared spines",
        "Add diagonal break marks (/ /) to signal the broken axis region",
        "Use twinx() to add a secondary y-axis on the right side of a chart",
        "Color both y-axis labels and ticks to match their respective data series",
        "Add a combined legend from both axes using ax1.get_legend_handles_labels()",
    ],
    "29. Image Processing with imshow": [
        "Display a grayscale image using ax.imshow(data, cmap='gray')",
        "Show an RGB image and annotate it with text at a specific pixel coordinate",
        "Apply a zoom inset to a specific region of an image using ax.inset_axes()",
        "Overlay a semi-transparent colormap heatmap on top of an image",
        "Compare the effect of different interpolation modes: 'nearest', 'bilinear', 'bicubic'",
    ],
    "30. Statistical Plots": [
        "Draw a vertical violin plot for 4 groups and add strip points on top",
        "Create a Q-Q plot using scipy.stats.probplot to assess normality",
        "Plot boxplots for 5 groups and annotate the median value above each box",
        "Use ax.violinplot() and customize the colors of the violin bodies manually",
        "Combine a histogram (density=True), a KDE line, and a rug plot on one axes",
    ],
    "31. Multi-Figure Export & Backends": [
        "Save three different charts to a single multi-page PDF using PdfPages",
        "Export a figure at 72, 150, and 300 DPI and print each file size",
        "Save a figure as SVG with svg.fonttype='none' for editable text in Inkscape",
        "Use plt.close('all') after batch export to free memory",
        "Write a loop that generates one chart per dataset and saves each as a named PNG",
    ],
    "32. Dashboard Composition": [
        "Use GridSpec to compose a dashboard with at least one spanning panel",
        "Add KPI 'tiles' as small colored axes with large text using ax.axis('off')",
        "Combine a trend line chart with a dual-axis overlay on one dashboard panel",
        "Apply a dark background theme to the entire figure using fig.set_facecolor()",
        "Export the dashboard at 200 DPI and verify readability at both screen and print sizes",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# Todos for gen_seaborn.py (32 sections)
# ─────────────────────────────────────────────────────────────────────────────
SNS_TODOS = {
    "1. Setup & Themes": [
        "Call sns.set_theme() with style='darkgrid' and palette='colorblind' at the top of a notebook",
        "Try all 5 style options ('darkgrid','whitegrid','dark','white','ticks') on the same bar chart",
        "Create a custom 5-color palette using hex codes and pass it to sns.barplot",
        "Use sns.despine() to remove the top and right spines from a box plot",
        "Override figure size via rc={'figure.figsize': (8,3)} inside sns.set_theme()",
    ],
    "2. Distribution Plots": [
        "Plot a histogram of a normally distributed sample and overlay a KDE curve",
        "Compare distributions of smokers vs non-smokers using sns.histplot with hue='smoker'",
        "Create a violin plot and interpret what the thick bar in the middle represents",
        "Use sns.ecdfplot to compare cumulative distributions of total_bill by day",
        "Add a rug plot under a KDE curve using sns.rugplot() to show individual data points",
    ],
    "3. Categorical Plots — Bar & Count": [
        "Create a grouped barplot of mean tip by day, colored by sex, with capsize=0.1",
        "Sort bars by value using the order= parameter to show highest to lowest",
        "Add value labels on top of each bar by iterating over ax.patches",
        "Use sns.countplot to show the frequency of meals per day, colored by time of day",
        "Switch the estimator to np.median in catplot and compare the result to the mean",
    ],
    "4. Box Plot & Violin Plot": [
        "Create side-by-side box plots of total_bill by day using the tips dataset",
        "Set inner='quartile' on a violin plot to show quartile lines inside the violin",
        "Overlay a narrow boxplot (width=0.12) on top of a violin plot for dual insight",
        "Add a stripplot layer on top of a boxenplot to show all individual data points",
        "Use split=True in violinplot to show male/female halves in the same shape",
    ],
    "5. Scatter & Regression Plots": [
        "Plot total_bill vs tip with hue='day' and size='size' to encode 3 variables",
        "Add a regression line using sns.regplot() with a shaded 95% confidence interval",
        "Use sns.lmplot() to draw separate regression lines for smokers vs non-smokers",
        "Set order=2 in regplot to fit a polynomial regression curve",
        "Use sns.relplot(kind='scatter') with col_wrap=3 to facet by channel",
    ],
    "6. Heatmap": [
        "Compute a correlation matrix for the tips dataset and plot it with sns.heatmap",
        "Set annot=True and fmt='.2f' to display correlation values inside each cell",
        "Mask the upper triangle using np.triu() to show only the lower diagonal",
        "Create a pivot table heatmap of mean revenue by region and month",
        "Use sns.clustermap() to hierarchically cluster rows and columns of a gene-expression matrix",
    ],
    "7. Pair Plot": [
        "Create a pairplot of the iris dataset with hue='species' and diag_kind='kde'",
        "Add kind='reg' to the pairplot to show regression lines in off-diagonal cells",
        "Use PairGrid to set scatter plots on the upper triangle and KDE contours on the lower",
        "Limit the columns to 3 features by passing vars=['col1','col2','col3'] to pairplot",
        "Set plot_kws=dict(alpha=0.4, s=20) to reduce overplotting in the scatter cells",
    ],
    "8. FacetGrid": [
        "Create a FacetGrid with col='time' and row='smoker' and map a histplot to each cell",
        "Use g.map_dataframe(sns.regplot, scatter=False) to add regression lines to all panels",
        "Set sharey=True to ensure all panels share the same y-axis range",
        "Use g.set_titles('{col_name} | {row_name}') for descriptive panel titles",
        "Use sns.catplot(kind='box') to wrap a box plot across facets with col='day'",
    ],
    "9. Time Series & Line Plot": [
        "Plot weekly sales for 3 regions using sns.lineplot with hue='region' and a CI band",
        "Use sns.relplot(kind='line') to facet monthly revenue by product with col_wrap=3",
        "Add an axvspan() shaded region to mark a promotion period on the line chart",
        "Annotate the peak revenue point with an arrow using ax.annotate()",
        "Format date tick labels using ax.xaxis.set_major_formatter with DateFormatter",
    ],
    "10. Customization & Matplotlib Integration": [
        "Access the Axes object returned by sns.boxplot() and add custom tick formatting",
        "Format the y-axis as currency using mticker.StrMethodFormatter('${x:.0f}')",
        "Layer violin + narrow boxplot + stripplot on the same axes for a complete view",
        "Use sns.plotting_context('paper') and ('talk') to compare font sizes",
        "Apply a dark background using plt.rc_context with custom facecolor and label colors",
    ],
    "11. FacetGrid & Multi-Plot Grids": [
        "Create a FacetGrid with col='region' and map a scatterplot of spend vs margin",
        "Use PairGrid with map_diag(sns.histplot), map_upper(scatter), map_lower(kdeplot)",
        "Wrap catplot(kind='box') across 4 days using col='day' and col_wrap=2",
        "Add a legend to a FacetGrid using g.add_legend(title='Category')",
        "Use relplot(kind='line') on the fmri dataset faceted by region with hue='event'",
    ],
    "12. Statistical Annotations": [
        "Add a barplot with errorbar='ci' to show 95% confidence intervals automatically",
        "Run a t-test between two groups and draw a significance bar using ax.plot + ax.text",
        "Annotate all pairwise comparisons between 3 groups using itertools.combinations",
        "Use sns.pointplot with errorbar='sd' and capsize=0.1 for standard deviation bars",
        "Display the effect size (Cohen's d) as a text annotation on the chart",
    ],
    "13. Regression & Distribution Plots": [
        "Use sns.lmplot with hue='neighborhood' to show per-group regression lines",
        "Plot regression residuals using sns.residplot and check for a horizontal band pattern",
        "Create a jointplot(kind='kde') to see the bivariate distribution of two variables",
        "Fit a polynomial regression (order=2) using sns.regplot and compare to linear",
        "Use sns.ecdfplot to compare price distributions across 3 categories on one axes",
    ],
    "14. FacetGrid & PairGrid": [
        "Build a FacetGrid histogram panel for 3 groups using g.map(sns.histplot, 'value')",
        "Create a PairGrid and assign different functions to upper, lower, and diagonal",
        "Use map_dataframe() instead of map() to pass the full DataFrame to each panel function",
        "Set diag_sharey=False in PairGrid to allow each diagonal plot its own y scale",
        "Save the FacetGrid figure using g.savefig('output.png', bbox_inches='tight')",
    ],
    "15. Statistical Visualization Deep Dive": [
        "Create a Q-Q plot using scipy.stats.probplot and overlay the theoretical line",
        "Plot a KDE and histogram together using stat='density' in sns.histplot",
        "Visualize a bivariate KDE contour on top of a scatter plot using kdeplot(fill=True)",
        "Use ecdfplot to compare the empirical CDF of two distributions and find the median crossing",
        "Apply log transformation to skewed data and compare histograms before and after",
    ],
    "16. Custom Seaborn Themes & Styling": [
        "Apply sns.set_theme(style='ticks') with rc overrides for spines and font scale",
        "Use sns.color_palette('husl', 8) and display the swatches with a for-loop barplot",
        "Apply sns.plotting_context('paper', font_scale=1.2) for a publication-ready chart",
        "Compare 'notebook', 'paper', 'talk', and 'poster' contexts side by side",
        "Use axes_style() as a context manager to apply a style to just one cell",
    ],
    "17. Strip Plot & Swarm Plot": [
        "Create a stripplot of total_bill by day with jitter=True and alpha=0.5",
        "Use swarmplot to show all points without overlap for a small dataset (n < 200)",
        "Layer a stripplot on top of a boxplot to see both summary and individual points",
        "Use hue='smoker' in swarmplot to color-code points by a third variable",
        "Adjust marker size using size=3 to prevent the swarm from becoming too wide",
    ],
    "18. Point Plot & Statistical Line Plots": [
        "Create a pointplot of mean tip by day with 95% CI using errorbar='ci'",
        "Set dodge=0.3 and hue='sex' to see male/female means side-by-side",
        "Use join=False to display points without connecting lines across days",
        "Compare pointplot (mean) vs barplot (mean) — notice the visual emphasis difference",
        "Add capsize=0.12 to show confidence interval caps on the point plot",
    ],
    "19. ECDF & Distribution Comparison": [
        "Plot ECDFs of total_bill for each day of the week on the same axes",
        "Use sns.ecdfplot with complementary=True to show the survival function",
        "Overlay median lines on an ECDF plot using ax.axvline for each group",
        "Compare ECDF vs KDE for the same data — note what each shows about shape",
        "Use stat='percent' in histplot alongside ecdfplot to verify percentile positions",
    ],
    "20. Cluster Map": [
        "Create a clustermap of the iris numeric columns to cluster features and samples",
        "Set method='ward' for hierarchical clustering and compare to 'average' linkage",
        "Normalize the data with standard_scale=1 before clustering to remove magnitude bias",
        "Add row_colors and col_colors to annotate clusters with colored side bars",
        "Set figsize=(10, 8) in clustermap and adjust cbar_pos for a clean colorbar layout",
    ],
    "21. Joint Plot Advanced": [
        "Create a jointplot(kind='scatter') with marginal KDE histograms on each axis",
        "Use kind='kde' to show the bivariate density as filled contours",
        "Add regression lines using kind='reg' and check if the CI band is narrow or wide",
        "Set joint_kws and marginal_kws to customize the central and marginal plots separately",
        "Use jointplot with hue='smoker' to show two groups' joint distributions overlaid",
    ],
    "22. catplot — Figure-Level Categorical": [
        "Use sns.catplot(kind='violin') to facet violin plots by time across 4 days",
        "Set col_wrap=2 so a 4-panel catplot displays in a 2x2 grid",
        "Pass order=['Thur','Fri','Sat','Sun'] to fix the x-axis category order",
        "Switch kind= from 'box' to 'strip' to 'swarm' and compare the visual output",
        "Use g.set_axis_labels() and g.set_titles() to rename axes and facet titles",
    ],
    "23. displot — Figure-Level Distributions": [
        "Use sns.displot(kind='hist', kde=True) to show histograms with KDE per group",
        "Facet by 'day' using col='day' to see separate distribution panels per day",
        "Switch kind='ecdf' to show cumulative distributions across groups in facets",
        "Use col_wrap=2 to arrange 4 day-panels in a 2-column grid",
        "Set bins=20 and height=3.5 to control bin count and panel height",
    ],
    "24. relplot — Figure-Level Relational": [
        "Use sns.relplot(kind='scatter') to facet scatter plots by channel with col='channel'",
        "Set col_wrap=3 to arrange 5 channel panels in two rows with 3 in the first",
        "Use hue='region' and style='region' to assign both color and marker shape per group",
        "Switch to kind='line' to show time series faceted by product across months",
        "Call g.add_legend(title='Region') to add a shared legend to the FacetGrid figure",
    ],
    "25. Heatmap Advanced": [
        "Apply a mask to show only the lower triangle of a correlation heatmap",
        "Use center=0 in sns.heatmap to center a diverging colormap at zero",
        "Create a significance marker heatmap by overlaying custom annotation strings",
        "Set linewidths=0.3 and linecolor='white' to add cell borders to the heatmap",
        "Use annot_kws=dict(size=8) to reduce annotation font size for dense heatmaps",
    ],
    "26. PairGrid Advanced": [
        "Set up a PairGrid with custom functions: upper=scatter, lower=kde, diag=hist",
        "Use map_lower(sns.kdeplot, fill=True, alpha=0.25) for filled KDE contours",
        "Add hue='species' and call g.add_legend() for a color-coded pair grid",
        "Use diag_sharey=False so each diagonal histogram scales independently",
        "Save the PairGrid figure using plt.savefig() after tight_layout()",
    ],
    "27. Residual & Regression Diagnostics": [
        "Use sns.residplot to plot residuals vs fitted values and look for patterns",
        "Set lowess=True to overlay a smoothed LOWESS trend on the residual plot",
        "Create a Q-Q plot of residuals using scipy.stats.probplot to check normality",
        "Compare linear vs quadratic regression residuals side-by-side using 1x2 subplots",
        "Annotate points with the largest residuals using ax.annotate()",
    ],
    "28. Mixed Seaborn + Matplotlib": [
        "Use sns.boxplot() then customize tick labels with ax.set_xticklabels() rotation",
        "Add significance brackets between groups using ax.plot() + ax.text() on a seaborn chart",
        "Format the y-axis as percent using mticker.PercentFormatter on a seaborn violin plot",
        "Annotate the median of each boxplot group using ax.text() in a for-loop",
        "Layer a matplotlib fill_between() shading on a seaborn lineplot to show a target range",
    ],
    "29. Seaborn with Real Datasets": [
        "Load the 'penguins' dataset, drop NaN rows, and create a pairplot by species",
        "Use the 'titanic' dataset to plot survival rate by class and sex with barplot",
        "Load 'flights' and pivot it, then plot a clustermap of monthly passengers by year",
        "Use the 'mpg' dataset to compare fuel efficiency by origin with a violin plot",
        "Load 'fmri' and use relplot(kind='line') to facet by region with hue='event'",
    ],
    "30. Object-Oriented Seaborn": [
        "Use the seaborn.objects (so) API to create a basic Dot plot with so.Plot()",
        "Chain .add(so.Bar()) and .add(so.Range()) to build an annotated bar chart",
        "Use .facet(col='day') in the objects API to create faceted panels",
        "Apply .scale(color=so.Nominal()) to map a categorical variable to colors",
        "Compare the objects API syntax to the classic sns.barplot call for the same chart",
    ],
    "31. Color Systems & Accessibility": [
        "Compare a red-green palette to the Wong colorblind-safe palette on the same chart",
        "Use the 'colorblind' palette in sns.set_theme and verify it with a 4-group bar chart",
        "Add hatch patterns ('//','xx','..') to bars as a secondary encoding for print accessibility",
        "Use different markers per group (o, s, ^, D) in addition to color for scatter plots",
        "Apply a sequential 'Blues' palette to a heatmap of ordered numerical data",
    ],
    "32. Seaborn Dashboard Composition": [
        "Use GridSpec to layout a 3-panel dashboard with a spanning top panel",
        "Combine sns.scatterplot, sns.violinplot, and sns.lineplot in a single figure",
        "Add a banner panel with ax.axis('off') and large title text for executive reports",
        "Set a consistent sns.set_theme at the top and verify all panels inherit the style",
        "Export the final dashboard at 150 DPI and verify readability at both print and screen sizes",
    ],
}


def patch_html(content):
    old = (
        "        cards += (f'<div class=\"topic\" id=\"s{i}\"><div class=\"th\" onclick=\"tog(this)\"><span>{esc(s[\"title\"])}</span>'\n"
        "                  f'<span class=\"arr\">&#9660;</span></div><div class=\"tb\"><p class=\"desc\">{esc(s.get(\"desc\",\"\"))}</p>'\n"
        "                  f'{blks}{rw_html}{practice_html}</div></div>')"
    )
    new = (
        "        todos = s.get(\"todos\", [])\n"
        "        todos_html = \"\"\n"
        "        if todos:\n"
        "            items = \"\\n\".join(\n"
        "                f'<li><label><input type=\"checkbox\"> {esc(t)}</label></li>'\n"
        "                for t in todos\n"
        "            )\n"
        "            todos_html = (\n"
        "                f'<div class=\"todo-list\">'\n"
        "                f'<div class=\"todo-head\">&#x2705; Practice Checklist</div>'\n"
        "                f'<ul>{items}</ul>'\n"
        "                f'</div>'\n"
        "            )\n"
        "        cards += (f'<div class=\"topic\" id=\"s{i}\"><div class=\"th\" onclick=\"tog(this)\"><span>{esc(s[\"title\"])}</span>'\n"
        "                  f'<span class=\"arr\">&#9660;</span></div><div class=\"tb\"><p class=\"desc\">{esc(s.get(\"desc\",\"\"))}</p>'\n"
        "                  f'{blks}{rw_html}{practice_html}{todos_html}</div></div>')"
    )
    assert old in content, "Could not find make_html cards block to patch!"
    return content.replace(old, new, 1)


def inject_todos(content, todos_map):
    """
    For each title in todos_map, find the section dict that starts with
    "title": "<title>" and inject a "todos": [...] key immediately after
    the closing quote of that title line.
    """
    for title, items in todos_map.items():
        # Build the todos block string
        items_str = ",\n        ".join(f'"{t}"' for t in items)
        todos_block = f'"todos": [\n        {items_str},\n    ],\n'

        # Pattern: find "title": "1. Line Plot", (with optional trailing content)
        # We look for the exact title value in a "title": "..." line
        pattern = re.compile(
            r'("title"\s*:\s*"' + re.escape(title) + r'")',
        )
        match = pattern.search(content)
        if not match:
            print(f"  WARNING: Could not find title: {title!r}")
            continue

        # Find the end of this line
        line_end = content.find('\n', match.end())
        if line_end == -1:
            line_end = len(content)

        # Check if todos already exist nearby (in next 200 chars)
        nearby = content[line_end:line_end + 200]
        if '"todos"' in nearby:
            print(f"  SKIP (already has todos): {title!r}")
            continue

        # Insert the todos block right after the title line
        insert_pos = line_end + 1
        content = content[:insert_pos] + todos_block + content[insert_pos:]
        print(f"  Injected todos: {title!r}")

    return content


# ─────────────────────────────────────────────────────────────────────────────
# Process gen_matplotlib.py
# ─────────────────────────────────────────────────────────────────────────────
mpl_path = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_matplotlib.py"
print("=== Patching gen_matplotlib.py ===")
with open(mpl_path, 'r', encoding='utf-8') as f:
    mpl_content = f.read()

mpl_content = patch_html(mpl_content)
mpl_content = inject_todos(mpl_content, MPL_TODOS)

with open(mpl_path, 'w', encoding='utf-8') as f:
    f.write(mpl_content)
print(f"Done. Sections targeted: {len(MPL_TODOS)}\n")

# ─────────────────────────────────────────────────────────────────────────────
# Process gen_seaborn.py
# ─────────────────────────────────────────────────────────────────────────────
sns_path = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_seaborn.py"
print("=== Patching gen_seaborn.py ===")
with open(sns_path, 'r', encoding='utf-8') as f:
    sns_content = f.read()

sns_content = patch_html(sns_content)
sns_content = inject_todos(sns_content, SNS_TODOS)

with open(sns_path, 'w', encoding='utf-8') as f:
    f.write(sns_content)
print(f"Done. Sections targeted: {len(SNS_TODOS)}\n")

print("=== All done! ===")
