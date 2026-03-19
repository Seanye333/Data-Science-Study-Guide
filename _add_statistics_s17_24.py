"""Add sections 17-24 to gen_statistics.py."""
import sys
sys.path.insert(0, r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
from _inserter import insert_sections

FILE   = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_statistics.py"
MARKER = "]  # end SECTIONS"

def ec(s):
    return (s.replace('\\','\\\\').replace('"','\\"')
             .replace('\n','\\n').replace("'","\\'"))

def make_s(num, title, desc, examples, rw_scenario, rw_code, pt, pd_text, ps):
    ex_lines = []
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples)-1 else ''
        ex_lines.append(f'        {{"label": "{ec(ex["label"])}", "code": "{ec(ex["code"])}"}}{comma}')
    ex_block = '\n'.join(ex_lines)
    return (
        f'{{\n"title": "{num}. {title}",\n"desc": "{ec(desc)}",\n'
        f'"examples": [\n{ex_block}\n    ],\n'
        f'"rw_scenario": "{ec(rw_scenario)}",\n"rw_code": "{ec(rw_code)}",\n'
        f'"practice": {{\n    "title": "{ec(pt)}",\n    "desc": "{ec(pd_text)}",\n'
        f'    "starter": "{ec(ps)}"\n}}\n}},\n\n'
    )

# ── 17: Hypothesis Testing ────────────────────────────────────────────────────
s17 = make_s(17, "Hypothesis Testing (t-tests & z-tests)",
    "Hypothesis testing decides whether observed data supports a null hypothesis H0. One-sample, two-sample, and paired t-tests cover most practical scenarios. Always check assumptions: normality, equal variance.",
    [
        {"label": "One-sample and two-sample t-tests",
         "code": """from scipy import stats
import numpy as np

np.random.seed(42)

# One-sample t-test: is the mean different from a known value?
weights = np.random.normal(70, 8, 30)
t_stat, p_val = stats.ttest_1samp(weights, popmean=72)
print(f"One-sample t-test: t={t_stat:.3f}, p={p_val:.4f}")
print(f"  Reject H0 (mean=72)? {p_val < 0.05}")

# Two-sample t-test: do two groups have different means?
group_a = np.random.normal(75, 10, 40)
group_b = np.random.normal(80, 10, 40)
t2, p2 = stats.ttest_ind(group_a, group_b)
print(f"Two-sample t-test: t={t2:.3f}, p={p2:.4f}")
print(f"  Reject H0 (equal means)? {p2 < 0.05}")

# Welch's t-test (unequal variances — safer default)
group_c = np.random.normal(80, 20, 40)  # larger std
t3, p3 = stats.ttest_ind(group_a, group_c, equal_var=False)
print(f"Welch's t-test: t={t3:.3f}, p={p3:.4f}")
print(f"  Mean A={group_a.mean():.2f}, Mean C={group_c.mean():.2f}")"""},
        {"label": "Paired t-test and confidence intervals",
         "code": """from scipy import stats
import numpy as np

np.random.seed(0)
# Paired t-test: before/after measurements on same subjects
before = np.random.normal(130, 15, 25)   # blood pressure before treatment
after  = before - np.random.normal(8, 5, 25)  # treatment lowers BP

t, p = stats.ttest_rel(before, after)
diff = before - after
ci = stats.t.interval(0.95, df=len(diff)-1,
                       loc=diff.mean(), scale=stats.sem(diff))

print(f"Paired t-test: t={t:.3f}, p={p:.4f}")
print(f"Mean reduction: {diff.mean():.2f} mmHg")
print(f"95% CI: ({ci[0]:.2f}, {ci[1]:.2f})")
print(f"Significant reduction? {p < 0.05}")

# Manual CI for a mean
n, mean, se = len(before), before.mean(), stats.sem(before)
ci_manual = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
print(f"\\nCI for baseline BP mean {mean:.1f}: ({ci_manual[0]:.1f}, {ci_manual[1]:.1f})")"""},
        {"label": "Chi-square test and proportions z-test",
         "code": """from scipy import stats
import numpy as np

# Chi-square test for independence
# Question: Is treatment type independent of recovery?
observed = np.array([[45, 15],   # Drug A: recovered, not recovered
                      [30, 30],   # Drug B
                      [38, 22]])  # Placebo

chi2, p, dof, expected = stats.chi2_contingency(observed)
print(f"Chi-square: chi2={chi2:.3f}, p={p:.4f}, dof={dof}")
print(f"Association between treatment and recovery? {p < 0.05}")

# Two-proportion z-test
# Are conversion rates different between landing pages?
n_a, conv_a = 1000, 120   # page A
n_b, conv_b = 1000, 145   # page B

count = np.array([conv_a, conv_b])
nobs  = np.array([n_a, n_b])
z, p_prop = stats.proportions_ztest(count, nobs)
print(f"\\nProportions z-test: z={z:.3f}, p={p_prop:.4f}")
print(f"Rate A={conv_a/n_a:.1%}, Rate B={conv_b/n_b:.1%}")
print(f"Significantly different? {p_prop < 0.05}")"""}
    ],
    rw_scenario="A pharma company tests whether a new drug reduces cholesterol more than a placebo. Paired t-test on 50 patients (pre/post treatment) with a significance level of 0.05.",
    rw_code="""from scipy import stats
import numpy as np

np.random.seed(7)
n = 50
drug_group    = np.random.normal(200, 30, n)  # baseline cholesterol
placebo_group = np.random.normal(200, 30, n)

drug_post    = drug_group    - np.random.normal(25, 10, n)  # drug reduces ~25
placebo_post = placebo_group - np.random.normal(5,  10, n)  # placebo reduces ~5

drug_diff    = drug_group    - drug_post
placebo_diff = placebo_group - placebo_post

t_drug,    p_drug    = stats.ttest_rel(drug_group,    drug_post)
t_placebo, p_placebo = stats.ttest_rel(placebo_group, placebo_post)
t_compare, p_compare = stats.ttest_ind(drug_diff,     placebo_diff)

print(f"Drug group:    mean reduction={drug_diff.mean():.1f}, p={p_drug:.4f}")
print(f"Placebo group: mean reduction={placebo_diff.mean():.1f}, p={p_placebo:.4f}")
print(f"Drug vs Placebo: t={t_compare:.3f}, p={p_compare:.4f}")
print(f"Drug significantly better? {p_compare < 0.05}")""",
    pt="A/B Test Analysis",
    pd_text="Two email subject lines were tested: A sent to 800 users (92 opened), B to 800 users (117 opened). (1) Run a two-proportion z-test. (2) Compute the 95% CI for the difference in rates. (3) Calculate the lift (relative improvement). (4) Determine the minimum detectable effect if you want 80% power at alpha=0.05.",
    ps="""from scipy import stats
import numpy as np

n_a, open_a = 800, 92
n_b, open_b = 800, 117

# (1) two-proportion z-test
# (2) 95% CI for difference
# (3) lift = (rate_b - rate_a) / rate_a
# (4) minimum detectable effect hint: use stats.norm.isf for z-scores
rate_a = open_a / n_a
rate_b = open_b / n_b
print(f"Rate A: {rate_a:.3f}, Rate B: {rate_b:.3f}")
"""
)

# ── 18: ANOVA ─────────────────────────────────────────────────────────────────
s18 = make_s(18, "ANOVA & Post-hoc Tests",
    "One-way ANOVA tests whether means differ across 3+ groups in a single factor. Two-way ANOVA adds a second factor and interaction. Post-hoc tests (Tukey, Bonferroni) identify which pairs differ.",
    [
        {"label": "One-way ANOVA with post-hoc Tukey HSD",
         "code": """from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import numpy as np

np.random.seed(42)
# Crop yield under 4 fertilizer types
groups = {
    'Control':  np.random.normal(50, 8, 20),
    'FertA':    np.random.normal(58, 8, 20),
    'FertB':    np.random.normal(55, 8, 20),
    'FertC':    np.random.normal(62, 8, 20),
}

f_stat, p_val = stats.f_oneway(*groups.values())
print(f"One-way ANOVA: F={f_stat:.3f}, p={p_val:.4f}")
print(f"Significant difference exists? {p_val < 0.05}\\n")

# Tukey HSD post-hoc
import numpy as np as _np
all_data   = np.concatenate(list(groups.values()))
all_labels = np.repeat(list(groups.keys()), 20)

tukey = pairwise_tukeyhsd(endog=all_data, groups=all_labels, alpha=0.05)
print(tukey.summary())"""},
        {"label": "Two-way ANOVA with interaction",
         "code": """import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np, pandas as pd

np.random.seed(42)
n = 120
df = pd.DataFrame({
    'fertilizer': np.repeat(['A','B','C'], n//3),
    'irrigation': np.tile(['Low','High'], n//2),
    'yield': (np.random.normal(55, 8, n) +
              np.where(np.repeat(['A','B','C'], n//3)=='C', 8, 0) +
              np.where(np.tile(['Low','High'], n//2)=='High', 5, 0)),
})

model = ols('yield ~ C(fertilizer) + C(irrigation) + C(fertilizer):C(irrigation)',
            data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table.round(4))
print(f"\\nFertilizer effect: p={anova_table.loc['C(fertilizer)','PR(>F)']:.4f}")
print(f"Irrigation effect: p={anova_table.loc['C(irrigation)','PR(>F)']:.4f}")"""},
        {"label": "Kruskal-Wallis (non-parametric ANOVA) + Bonferroni",
         "code": """from scipy import stats
from statsmodels.stats.multitest import multipletests
import numpy as np
from itertools import combinations

np.random.seed(5)
# Non-normal data: response times across 3 UI designs
groups = {
    'Design A': np.random.exponential(2.0, 30),
    'Design B': np.random.exponential(1.5, 30),
    'Design C': np.random.exponential(2.5, 30),
}
names = list(groups.keys())
data  = list(groups.values())

# Kruskal-Wallis
H, p = stats.kruskal(*data)
print(f"Kruskal-Wallis: H={H:.3f}, p={p:.4f}")

# Pairwise Mann-Whitney U with Bonferroni correction
pairs = list(combinations(range(len(names)), 2))
raw_p = []
for i, j in pairs:
    _, pv = stats.mannwhitneyu(data[i], data[j], alternative='two-sided')
    raw_p.append(pv)

reject, p_adj, _, _ = multipletests(raw_p, method='bonferroni')
for (i,j), pv, pa, rej in zip(pairs, raw_p, p_adj, reject):
    print(f"  {names[i]} vs {names[j]}: raw_p={pv:.4f}, adj_p={pa:.4f}, reject={rej}")"""}
    ],
    rw_scenario="A UX researcher tests 3 onboarding flows on task completion time across 60 users. ANOVA reveals a significant difference; Tukey HSD pinpoints which flow pairs differ significantly.",
    rw_code="""from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import numpy as np, pandas as pd

np.random.seed(99)
flows = {'Flow 1': np.random.normal(45, 12, 20),
         'Flow 2': np.random.normal(38, 10, 20),
         'Flow 3': np.random.normal(52, 14, 20)}

f, p = stats.f_oneway(*flows.values())
print(f"ANOVA: F={f:.3f}, p={p:.4f}")

all_times  = np.concatenate(list(flows.values()))
all_labels = np.repeat(list(flows.keys()), 20)
tukey = pairwise_tukeyhsd(all_times, all_labels, alpha=0.05)
print(tukey.summary())

for name, times in flows.items():
    print(f"{name}: mean={times.mean():.1f}s, sd={times.std():.1f}s")""",
    pt="Marketing Channel ANOVA",
    pd_text="Generate sales data for 4 marketing channels (Email, Social, Search, Display) — 25 observations each with means 120, 135, 150, 110 and std=25. (1) Run one-way ANOVA. (2) If significant, run Tukey HSD to identify which channels differ. (3) Compute eta-squared (effect size = SS_between / SS_total).",
    ps="""from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import numpy as np

np.random.seed(42)
channels = {'Email':   np.random.normal(120, 25, 25),
            'Social':  np.random.normal(135, 25, 25),
            'Search':  np.random.normal(150, 25, 25),
            'Display': np.random.normal(110, 25, 25)}

# (1) One-way ANOVA
# (2) Tukey HSD if significant
# (3) eta-squared = SS_between / SS_total
# SS_total = sum of (xi - grand_mean)^2 across all observations
"""
)

# ── 19: Correlation ───────────────────────────────────────────────────────────
s19 = make_s(19, "Correlation Analysis",
    "Pearson measures linear association between continuous variables. Spearman and Kendall are rank-based (robust to outliers and non-linearity). Point-biserial handles binary-continuous pairs.",
    [
        {"label": "Pearson, Spearman, Kendall correlation",
         "code": """from scipy import stats
import numpy as np

np.random.seed(42)
n = 100

# Pearson: linear relationship
x = np.random.randn(n)
y_linear = 2 * x + np.random.randn(n) * 0.5

r_p, p_p = stats.pearsonr(x, y_linear)
r_s, p_s = stats.spearmanr(x, y_linear)
r_k, p_k = stats.kendalltau(x, y_linear)
print("Linear relationship:")
print(f"  Pearson r={r_p:.4f}  Spearman r={r_s:.4f}  Kendall tau={r_k:.4f}")

# Spearman handles monotonic non-linear relationships
y_mono = np.exp(x) + np.random.randn(n) * 0.3
r_p2, _ = stats.pearsonr(x, y_mono)
r_s2, _ = stats.spearmanr(x, y_mono)
print(f"\\nMonotonic (non-linear):")
print(f"  Pearson r={r_p2:.4f}  Spearman r={r_s2:.4f}")

# With outliers: Spearman is robust
y_outlier = y_linear.copy()
y_outlier[[5, 10, 15]] = 100  # inject outliers
r_p3, _ = stats.pearsonr(x, y_outlier)
r_s3, _ = stats.spearmanr(x, y_outlier)
print(f"\\nWith outliers:")
print(f"  Pearson r={r_p3:.4f}  Spearman r={r_s3:.4f}  (Spearman more robust)")"""},
        {"label": "Correlation matrix and partial correlation",
         "code": """from scipy import stats
import numpy as np, pandas as pd

np.random.seed(42)
n = 200
# Confounding variable Z drives both X and Y
z = np.random.randn(n)
x = 0.7 * z + np.random.randn(n) * 0.5
y = 0.8 * z + np.random.randn(n) * 0.5
w = np.random.randn(n)  # unrelated

df = pd.DataFrame({'X': x, 'Y': y, 'Z': z, 'W': w})

print("Correlation matrix:")
print(df.corr(method='pearson').round(3))

# Partial correlation: X-Y controlling for Z
def partial_corr(x, y, z):
    # Regress out z from both x and y
    r_xz = np.corrcoef(x, z)[0,1]
    r_yz = np.corrcoef(y, z)[0,1]
    r_xy = np.corrcoef(x, y)[0,1]
    return (r_xy - r_xz*r_yz) / (np.sqrt(1-r_xz**2) * np.sqrt(1-r_yz**2))

pc = partial_corr(x, y, z)
print(f"\\nX-Y raw correlation:     {np.corrcoef(x,y)[0,1]:.4f}")
print(f"X-Y partial (given Z):   {pc:.4f}  (much lower — Z was confounding)")"""},
        {"label": "Point-biserial, phi coefficient, and significance testing",
         "code": """from scipy import stats
import numpy as np

np.random.seed(3)
n = 150

# Point-biserial: continuous vs binary
scores = np.random.normal(70, 10, n)
passed = (scores + np.random.randn(n)*5 > 68).astype(int)
r_pb, p_pb = stats.pointbiserialr(passed, scores)
print(f"Point-biserial r={r_pb:.4f}, p={p_pb:.4f}")

# Phi coefficient: binary vs binary
vaccinated = np.random.choice([0,1], n, p=[0.4,0.6])
infected   = np.where(vaccinated==1,
                       np.random.choice([0,1], n, p=[0.9,0.1]),
                       np.random.choice([0,1], n, p=[0.4,0.6]))
chi2, p_chi, _, _ = stats.chi2_contingency(
    np.array([[((vaccinated==0)&(infected==0)).sum(),
               ((vaccinated==0)&(infected==1)).sum()],
              [((vaccinated==1)&(infected==0)).sum(),
               ((vaccinated==1)&(infected==1)).sum()]]))
phi = np.sqrt(chi2 / n)
print(f"Phi coefficient={phi:.4f}, chi2_p={p_chi:.4f}")

# Testing significance of Pearson r
r = 0.35
n_test = 50
t = r * np.sqrt(n_test-2) / np.sqrt(1-r**2)
p = 2 * stats.t.sf(abs(t), df=n_test-2)
print(f"\\nr=0.35, n=50: t={t:.3f}, p={p:.4f}, significant={p<0.05}")"""}
    ],
    rw_scenario="A sports analyst computes Spearman correlations between athlete metrics (speed, strength, endurance, recovery) and competitive performance, then uses partial correlation to remove the confounding effect of age.",
    rw_code="""from scipy import stats
import numpy as np, pandas as pd

np.random.seed(10)
n = 80
age = np.random.uniform(18, 35, n)
speed      = -0.4*age + np.random.randn(n)*2 + 30
strength   =  0.1*age + np.random.randn(n)*3 + 20
endurance  = -0.3*age + np.random.randn(n)*2 + 25
performance= 0.5*speed + 0.3*strength + 0.4*endurance + np.random.randn(n)*2

df = pd.DataFrame({'age':age,'speed':speed,'strength':strength,
                   'endurance':endurance,'performance':performance})

print("Spearman correlations with performance:")
for col in ['age','speed','strength','endurance']:
    r, p = stats.spearmanr(df[col], df['performance'])
    print(f"  {col:12s}: r={r:.3f}, p={p:.4f}")

# Partial: speed-performance controlling for age
r_sp = np.corrcoef(speed, performance)[0,1]
r_sa = np.corrcoef(speed, age)[0,1]
r_pa = np.corrcoef(performance, age)[0,1]
pc = (r_sp - r_sa*r_pa) / (np.sqrt(1-r_sa**2)*np.sqrt(1-r_pa**2))
print(f"\\nSpeed-Perf raw r={r_sp:.3f}, partial (ctrl age)={pc:.3f}")""",
    pt="Feature Correlation Screening",
    pd_text="Generate 8 features for 300 samples (some correlated, some independent, one binary). (1) Compute and print the full Pearson correlation matrix. (2) Flag all feature pairs with |r| > 0.7 as highly correlated. (3) Compute point-biserial correlation of the binary feature with each continuous feature. (4) Test each correlation for significance.",
    ps="""from scipy import stats
import numpy as np, pandas as pd

np.random.seed(42)
n = 300
z = np.random.randn(n)
df = pd.DataFrame({
    'f1': z + np.random.randn(n)*0.3,
    'f2': -0.8*z + np.random.randn(n)*0.3,  # correlated with f1
    'f3': np.random.randn(n),
    'f4': np.random.randn(n),
    'f5': 0.9*z + np.random.randn(n)*0.1,   # highly correlated
    'f6': np.random.exponential(2, n),
    'f7': np.random.randn(n),
    'binary': (z > 0).astype(int),
})

# (1) correlation matrix
# (2) flag |r| > 0.7 pairs
# (3) point-biserial for binary vs continuous
# (4) test significance
"""
)

# ── 20: Non-Parametric Tests ─────────────────────────────────────────────────
s20 = make_s(20, "Non-Parametric Tests",
    "Non-parametric tests make no assumptions about distributions. Use them when data is ordinal, heavily skewed, or sample sizes are too small to verify normality. Wilcoxon, Mann-Whitney, and Kolmogorov-Smirnov are the workhorses.",
    [
        {"label": "Normality tests: Shapiro-Wilk and D'Agostino",
         "code": """from scipy import stats
import numpy as np

np.random.seed(42)

datasets = {
    'Normal':      np.random.normal(50, 10, 50),
    'Skewed':      np.random.exponential(5, 50),
    'Heavy-tailed':np.random.standard_t(df=3, size=50),
    'Uniform':     np.random.uniform(0, 100, 50),
}

print(f"{'Dataset':15s}  {'Shapiro p':>10s}  {'D\\'Agostino p':>13s}  {'Normal?'}")
print('-' * 60)
for name, data in datasets.items():
    _, p_sw  = stats.shapiro(data)
    _, p_da  = stats.normaltest(data)
    is_norm  = p_sw > 0.05 and p_da > 0.05
    print(f"{name:15s}  {p_sw:10.4f}  {p_da:13.4f}  {str(is_norm)}")

# Q-Q plot values (manual)
normal_data = datasets['Normal']
theoretical, observed = stats.probplot(normal_data, dist='norm')[0]
r = np.corrcoef(theoretical, observed)[0,1]
print(f"\\nQ-Q correlation for Normal: {r:.4f} (close to 1 = normal)")"""},
        {"label": "Wilcoxon signed-rank and Mann-Whitney U",
         "code": """from scipy import stats
import numpy as np

np.random.seed(7)
# Wilcoxon signed-rank: paired non-parametric alternative to paired t-test
before = np.random.exponential(2.0, 30)
after  = before * 0.7 + np.random.exponential(0.3, 30)

stat_w, p_w = stats.wilcoxon(before, after)
stat_t, p_t = stats.ttest_rel(before, after)
print("Paired comparison (before vs after):")
print(f"  Wilcoxon: stat={stat_w:.1f}, p={p_w:.4f}")
print(f"  t-test:   stat={stat_t:.3f}, p={p_t:.4f}")

# Mann-Whitney U: non-parametric two-sample test
group1 = np.random.exponential(3.0, 40)
group2 = np.random.exponential(4.5, 40)

u_stat, p_u = stats.mannwhitneyu(group1, group2, alternative='two-sided')
t_stat, p_t2 = stats.ttest_ind(group1, group2)
print(f"\\nTwo-group comparison:")
print(f"  Mann-Whitney: U={u_stat:.1f}, p={p_u:.4f}")
print(f"  t-test:       t={t_stat:.3f}, p={p_t2:.4f}")

# Effect size r = Z / sqrt(N) for Mann-Whitney
n1, n2 = len(group1), len(group2)
z = stats.norm.ppf(p_u/2)  # approximate z
r_effect = abs(z) / np.sqrt(n1+n2)
print(f"  Effect size r: {r_effect:.3f}")"""},
        {"label": "Kolmogorov-Smirnov and Anderson-Darling tests",
         "code": """from scipy import stats
import numpy as np

np.random.seed(0)

# One-sample KS: does data come from a specified distribution?
data_normal = np.random.normal(0, 1, 100)
data_exp    = np.random.exponential(1, 100)

for name, data in [('Normal', data_normal), ('Exponential', data_exp)]:
    ks_n, p_n = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
    ks_e, p_e = stats.kstest(data, 'expon', args=(0, 1/data.mean()))
    print(f"{name}: KS vs Normal p={p_n:.4f}, KS vs Expon p={p_e:.4f}")

# Two-sample KS: do two samples come from the same distribution?
sample_a = np.random.normal(0, 1, 100)
sample_b = np.random.normal(0.5, 1, 100)  # slightly shifted
ks2, p2 = stats.ks_2samp(sample_a, sample_b)
print(f"\\n2-sample KS: stat={ks2:.4f}, p={p2:.4f}")

# Anderson-Darling (more powerful than KS for normal testing)
result = stats.anderson(data_normal, dist='norm')
print(f"\\nAnderson-Darling statistic: {result.statistic:.4f}")
for sl, cv in zip(result.significance_level, result.critical_values):
    print(f"  {sl}% significance level: crit={cv:.4f}, reject={result.statistic > cv}")"""}
    ],
    rw_scenario="A clinical researcher compares pain scores (skewed, ordinal 1-10) between a drug and control group. Shapiro-Wilk confirms non-normality, so Mann-Whitney U is used instead of a t-test.",
    rw_code="""from scipy import stats
import numpy as np

np.random.seed(42)
# Pain scores: skewed, bounded 1-10
drug_scores    = np.clip(np.random.exponential(2.5, 40) + 1, 1, 10).round()
control_scores = np.clip(np.random.exponential(4.0, 40) + 1, 1, 10).round()

# Test normality first
_, p_drug = stats.shapiro(drug_scores)
_, p_ctrl = stats.shapiro(control_scores)
print(f"Shapiro p-values: drug={p_drug:.4f}, control={p_ctrl:.4f}")
print(f"Use non-parametric: {p_drug < 0.05 or p_ctrl < 0.05}")

# Mann-Whitney U
u, p = stats.mannwhitneyu(drug_scores, control_scores, alternative='less')
print(f"Mann-Whitney: U={u:.1f}, p={p:.4f}")
print(f"Drug reduces pain? {p < 0.05}")
print(f"Median drug={np.median(drug_scores):.1f}, control={np.median(control_scores):.1f}")""",
    pt="Distribution Comparison Pipeline",
    pd_text="Write a function compare_groups(a, b) that: (1) Tests normality of both groups with Shapiro-Wilk, (2) If both normal, runs Levene's test for equal variances, then appropriate t-test (Welch or Student), (3) If either non-normal, runs Mann-Whitney U, (4) Returns a dict with test_used, statistic, p_value, significant. Test with normal and non-normal pairs.",
    ps="""from scipy import stats
import numpy as np

def compare_groups(a, b, alpha=0.05):
    result = {}
    # (1) normality
    _, p_a = stats.shapiro(a)
    _, p_b = stats.shapiro(b)
    both_normal = p_a > alpha and p_b > alpha
    # (2) if normal: Levene then t-test
    # (3) if not normal: Mann-Whitney
    # (4) return dict
    return result

np.random.seed(42)
normal_a = np.random.normal(10, 2, 30)
normal_b = np.random.normal(11, 2, 30)
skewed_a = np.random.exponential(2, 30)
skewed_b = np.random.exponential(3, 30)

print(compare_groups(normal_a, normal_b))
print(compare_groups(skewed_a, skewed_b))
"""
)

# ── 21: Bayesian Basics ───────────────────────────────────────────────────────
s21 = make_s(21, "Bayesian Inference Basics",
    "Bayesian inference updates prior beliefs with observed data to produce a posterior distribution. Beta-Binomial and Normal-Normal conjugates let you compute posteriors analytically. Compare to frequentist interpretation of the same data.",
    [
        {"label": "Beta-Binomial: updating conversion rate beliefs",
         "code": """from scipy import stats
import numpy as np

# Prior: Beta(alpha=2, beta=10) — we expect ~17% conversion
prior_a, prior_b = 2, 10

# Observed data: 45 conversions out of 200 visits
obs_conv, obs_total = 45, 200
obs_failures = obs_total - obs_conv

# Posterior: Beta(alpha + successes, beta + failures) [conjugate]
post_a = prior_a + obs_conv
post_b = prior_b + obs_failures

prior     = stats.beta(prior_a, prior_b)
posterior = stats.beta(post_a, post_b)

print(f"Prior:     mean={prior.mean():.3f}, 95% CI: ({prior.ppf(0.025):.3f}, {prior.ppf(0.975):.3f})")
print(f"Posterior: mean={posterior.mean():.3f}, 95% CI: ({posterior.ppf(0.025):.3f}, {posterior.ppf(0.975):.3f})")
print(f"MLE (freq): {obs_conv/obs_total:.3f}")

# Probability that conversion > 25%
prob_above = 1 - posterior.cdf(0.25)
print(f"P(conversion > 25%): {prob_above:.4f}")

# Posterior predictive: expected conversions in next 100
pp_mean  = posterior.mean() * 100
pp_sd    = np.sqrt(posterior.var() * 100)
print(f"Expected conversions (next 100): {pp_mean:.1f} ± {pp_sd:.1f}")"""},
        {"label": "Bayesian A/B test: comparing two rates",
         "code": """from scipy import stats
import numpy as np

np.random.seed(42)

# A/B test with conjugate Beta posteriors
conv_a, n_a = 120, 1000   # page A
conv_b, n_b = 145, 1000   # page B

# Non-informative priors Beta(1,1) = Uniform
post_a = stats.beta(1 + conv_a, 1 + n_a - conv_a)
post_b = stats.beta(1 + conv_b, 1 + n_b - conv_b)

# Monte Carlo estimate P(B > A)
samples_a = post_a.rvs(100_000)
samples_b = post_b.rvs(100_000)
p_b_wins  = (samples_b > samples_a).mean()

# Expected lift
lift_samples = (samples_b - samples_a) / samples_a
lift_mean = lift_samples.mean()
lift_ci = np.percentile(lift_samples, [2.5, 97.5])

print(f"P(B > A) = {p_b_wins:.4f}")
print(f"Expected lift: {lift_mean:.1%}")
print(f"95% credible interval for lift: ({lift_ci[0]:.1%}, {lift_ci[1]:.1%})")
print(f"Posterior A: mean={post_a.mean():.4f}")
print(f"Posterior B: mean={post_b.mean():.4f}")"""},
        {"label": "Normal-Normal conjugate for mean estimation",
         "code": """from scipy import stats
import numpy as np

np.random.seed(0)
# Estimating the true mean of a process
# Prior: Normal(mu0=100, sigma0=20)  — prior belief about mean
# Known measurement noise: sigma=15

mu0, sigma0 = 100.0, 20.0   # prior
sigma_obs   = 15.0            # known observation noise

# Observe 30 measurements
true_mean = 112.0
data = np.random.normal(true_mean, sigma_obs, 30)
n, x_bar = len(data), data.mean()

# Conjugate update
precision_prior = 1 / sigma0**2
precision_data  = n / sigma_obs**2
precision_post  = precision_prior + precision_data

mu_post    = (precision_prior*mu0 + precision_data*x_bar) / precision_post
sigma_post = np.sqrt(1 / precision_post)

prior_dist = stats.norm(mu0, sigma0)
post_dist  = stats.norm(mu_post, sigma_post)

print(f"Prior:        mean={mu0:.1f},     95% CI: ({prior_dist.ppf(0.025):.1f}, {prior_dist.ppf(0.975):.1f})")
print(f"Likelihood:   mean={x_bar:.2f},  (n={n} obs, noise={sigma_obs})")
print(f"Posterior:    mean={mu_post:.2f}, 95% CI: ({post_dist.ppf(0.025):.2f}, {post_dist.ppf(0.975):.2f})")
print(f"True mean:    {true_mean}")
print(f"Posterior pulls toward prior when data is limited.")"""}
    ],
    rw_scenario="An e-commerce platform uses Bayesian A/B testing for a checkout redesign. Instead of waiting for p<0.05, they monitor the posterior probability that variant B outperforms A and stop when P(B>A) > 0.95.",
    rw_code="""from scipy import stats
import numpy as np

np.random.seed(42)

# Sequential Bayesian A/B test
true_rate_a, true_rate_b = 0.10, 0.13
n_per_day = 50

post_a = stats.beta(1, 1)
post_b = stats.beta(1, 1)

alpha_a, beta_a = 1, 1
alpha_b, beta_b = 1, 1

print(f"{'Day':>5s}  {'n_a':>6s}  {'n_b':>6s}  {'Rate A':>8s}  {'Rate B':>8s}  {'P(B>A)':>8s}")
for day in range(1, 31):
    # New daily data
    conv_a = np.random.binomial(n_per_day, true_rate_a)
    conv_b = np.random.binomial(n_per_day, true_rate_b)
    alpha_a += conv_a; beta_a += n_per_day - conv_a
    alpha_b += conv_b; beta_b += n_per_day - conv_b

    post_a = stats.beta(alpha_a, beta_a)
    post_b = stats.beta(alpha_b, beta_b)
    p_b_wins = (post_b.rvs(50000) > post_a.rvs(50000)).mean()
    n_total = (alpha_a + beta_a - 2) + (alpha_b + beta_b - 2)

    if day % 5 == 0 or p_b_wins > 0.95:
        print(f"{day:5d}  {n_total//2:6d}  {n_total//2:6d}  {post_a.mean():8.4f}  {post_b.mean():8.4f}  {p_b_wins:8.4f}")
    if p_b_wins > 0.95:
        print(f"  --> Stopping: P(B>A)={p_b_wins:.4f} > 0.95 on day {day}")
        break""",
    pt="Bayesian Coin Fairness",
    pd_text="A coin is flipped 100 times with 62 heads. (1) Start with a uniform prior Beta(1,1). (2) Update sequentially after every 10 flips. (3) Print posterior mean and 95% credible interval at each step. (4) Compare to the frequentist 95% CI at each step. (5) Compute P(p > 0.5) from the final posterior.",
    ps="""from scipy import stats
import numpy as np

np.random.seed(0)
n_flips, n_heads = 100, 62
flips = np.array([1]*n_heads + [0]*(n_flips - n_heads))
np.random.shuffle(flips)

a, b = 1, 1  # prior Beta(1,1)

print(f"{'Step':>6s}  {'Heads':>6s}  {'n':>5s}  {'Post mean':>10s}  {'95% Credible':>20s}  {'Freq 95% CI':>20s}")
for step in range(10, n_flips+1, 10):
    chunk = flips[:step]
    h = chunk.sum(); n = len(chunk)
    a_post = a + h; b_post = b + n - h
    post = stats.beta(a_post, b_post)
    # TODO: compute posterior 95% CI from post
    # TODO: compute frequentist 95% CI using stats.proportion_confint or normal approx
    # TODO: print row
    pass

# (5) P(p > 0.5) from final posterior
"""
)

# ── 22: Effect Size & Power ───────────────────────────────────────────────────
s22 = make_s(22, "Effect Size & Statistical Power",
    "Effect size quantifies the magnitude of a difference independently of sample size. Cohen's d, r, eta-squared measure effect for different tests. Power analysis determines the sample size needed to detect a given effect.",
    [
        {"label": "Cohen's d and r for effect size",
         "code": """from scipy import stats
import numpy as np

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    s_pooled = np.sqrt(((n1-1)*group1.std()**2 + (n2-1)*group2.std()**2) / (n1+n2-2))
    return (group1.mean() - group2.mean()) / s_pooled

np.random.seed(42)
thresholds = [('Small', 0.2), ('Medium', 0.5), ('Large', 0.8)]

print(f"{'Effect':8s}  {'Cohen d':>8s}  {'Interpretation':>15s}  {'p-value':>8s}")
print('-' * 55)
for label, target_d in thresholds:
    a = np.random.normal(0, 1, 50)
    b = np.random.normal(target_d, 1, 50)
    d = cohens_d(b, a)
    _, p = stats.ttest_ind(a, b)
    print(f"{label:8s}  {d:8.3f}  {label:>15s}  {p:8.4f}")

# r from t-statistic
t_stat = 3.2
n_total = 80
r = np.sqrt(t_stat**2 / (t_stat**2 + n_total - 2))
print(f"\\nt={t_stat}, n={n_total} -> r effect size = {r:.3f}")

# Eta-squared from F (ANOVA)
F, df_between, df_within = 8.5, 2, 60
eta2 = (F * df_between) / (F * df_between + df_within)
print(f"F={F}, df_b={df_between}, df_w={df_within} -> eta²={eta2:.3f}")"""},
        {"label": "Sample size calculation for t-test",
         "code": """from scipy import stats
import numpy as np

def sample_size_ttest(effect_size_d, alpha=0.05, power=0.80, tail=2):
    z_alpha = stats.norm.ppf(1 - alpha/tail)
    z_beta  = stats.norm.ppf(power)
    n = 2 * ((z_alpha + z_beta) / effect_size_d) ** 2
    return int(np.ceil(n))

print("Required sample size per group (two-sample t-test):")
print(f"{'Effect d':>9s}  {'α=0.05,80%':>12s}  {'α=0.05,90%':>12s}  {'α=0.01,80%':>12s}")
print('-' * 52)
for d in [0.2, 0.3, 0.5, 0.8, 1.0]:
    n1 = sample_size_ttest(d, 0.05, 0.80)
    n2 = sample_size_ttest(d, 0.05, 0.90)
    n3 = sample_size_ttest(d, 0.01, 0.80)
    print(f"{d:9.1f}  {n1:12d}  {n2:12d}  {n3:12d}")

# Using statsmodels TTestIndPower
from statsmodels.stats.power import TTestIndPower
analysis = TTestIndPower()
n = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.80)
print(f"\\nstatsmodels: d=0.5, α=0.05, power=0.80 -> n={n:.1f} per group")

# Achieved power for given n and effect
power = analysis.solve_power(effect_size=0.3, alpha=0.05, nobs1=100)
print(f"d=0.3, n=100 per group -> achieved power={power:.3f}")"""},
        {"label": "Power curves and minimum detectable effect",
         "code": """from statsmodels.stats.power import TTestIndPower, ChiSquarePower
import numpy as np

analysis = TTestIndPower()

# Power curve: power vs sample size for different effect sizes
print("Power by sample size and effect size:")
print(f"{'n/grp':>7s}", end='')
for d in [0.2, 0.3, 0.5, 0.8]:
    print(f"  d={d}", end='')
print()
for n in [20, 50, 100, 200, 500]:
    print(f"{n:7d}", end='')
    for d in [0.2, 0.3, 0.5, 0.8]:
        pwr = analysis.solve_power(effect_size=d, alpha=0.05, nobs1=n)
        print(f"  {pwr:.3f}", end='')
    print()

# Minimum detectable effect (MDE) given n and desired power
mde = analysis.solve_power(alpha=0.05, power=0.80, nobs1=200)
print(f"\\nMDE (d) for n=200/grp, power=80%: {mde:.3f}")

# Chi-square power
chi_power = ChiSquarePower()
n_chi = chi_power.solve_power(effect_size=0.3, alpha=0.05, power=0.80, k_bins=3)
print(f"Chi-square: effect=0.3, k=3, power=80% -> n={n_chi:.1f}")"""}
    ],
    rw_scenario="A product team wants to detect a 10% improvement in task completion rate (from 60% to 66%). They compute required sample size for 80% and 90% power, then run the test and report Cohen's h effect size.",
    rw_code="""from statsmodels.stats.power import NormalIndPower
from scipy import stats
import numpy as np

# Rate improvement: 60% -> 66%
rate_a, rate_b = 0.60, 0.66

# Cohen's h for proportions
h = 2 * np.arcsin(np.sqrt(rate_b)) - 2 * np.arcsin(np.sqrt(rate_a))
print(f"Cohen's h = {h:.4f}")

# Required sample size
analysis = NormalIndPower()
for power in [0.80, 0.90, 0.95]:
    n = analysis.solve_power(effect_size=h, alpha=0.05, power=power)
    print(f"Power={power:.0%}: n={n:.0f} per group (total {2*n:.0f})")

# Simulate the test
np.random.seed(42)
n_per = int(analysis.solve_power(effect_size=h, alpha=0.05, power=0.80)) + 1
conv_a = np.random.binomial(n_per, rate_a)
conv_b = np.random.binomial(n_per, rate_b)
_, p = stats.proportions_ztest([conv_a, conv_b], [n_per, n_per])
print(f"\\nSimulated test: A={conv_a/n_per:.3f}, B={conv_b/n_per:.3f}, p={p:.4f}")""",
    pt="Power Analysis Dashboard",
    pd_text="For a two-sample t-test: (1) Compute required n for all combinations of effect_size in [0.2,0.5,0.8] and power in [0.70,0.80,0.90] at alpha=0.05. Print as a grid. (2) For n=150 per group and alpha=0.05, plot (print) a table of achieved power for effect sizes 0.1 to 0.8 in steps of 0.1. (3) Find the MDE for n=300 at 80% power.",
    ps="""from statsmodels.stats.power import TTestIndPower
import numpy as np

analysis = TTestIndPower()

# (1) n grid
print("Required n per group:")
effects = [0.2, 0.5, 0.8]
powers  = [0.70, 0.80, 0.90]
# TODO: print header and rows

# (2) power table for n=150
print("\\nAchieved power for n=150 per group:")
# TODO

# (3) MDE
mde = analysis.solve_power(alpha=0.05, power=0.80, nobs1=300)
print(f"\\nMDE for n=300: d={mde:.4f}")
"""
)

# ── 23: Multiple Testing Corrections ─────────────────────────────────────────
s23 = make_s(23, "Multiple Testing & FDR Corrections",
    "Running many tests inflates the false positive rate. Bonferroni controls family-wise error rate (conservative). Benjamini-Hochberg (BH) controls the false discovery rate — preferred for exploratory studies with many hypotheses.",
    [
        {"label": "Bonferroni and Holm-Bonferroni corrections",
         "code": """from statsmodels.stats.multitest import multipletests
from scipy import stats
import numpy as np

np.random.seed(42)
n_tests = 20
n_per   = 50

# 20 tests: 3 truly different (true positives), 17 null
true_effect = [0, 0, 0, 0.8, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0.6, 0, 0, 0, 0]
raw_p = []
for d in true_effect:
    a = np.random.normal(0, 1, n_per)
    b = np.random.normal(d, 1, n_per)
    _, p = stats.ttest_ind(a, b)
    raw_p.append(p)

methods = ['bonferroni', 'holm', 'fdr_bh', 'fdr_by']
print(f"{'Method':12s}  {'Rejections':>11s}  {'True Pos':>9s}  {'False Pos':>10s}")
for method in methods:
    reject, p_adj, _, _ = multipletests(raw_p, alpha=0.05, method=method)
    n_reject = reject.sum()
    true_pos  = sum(1 for r, d in zip(reject, true_effect) if r and d != 0)
    false_pos = sum(1 for r, d in zip(reject, true_effect) if r and d == 0)
    print(f"{method:12s}  {n_reject:11d}  {true_pos:9d}  {false_pos:10d}")

print(f"\\nUncorrected (p<0.05): {sum(p < 0.05 for p in raw_p)} rejections")"""},
        {"label": "Benjamini-Hochberg step-by-step",
         "code": """from scipy import stats
import numpy as np

np.random.seed(1)
n_hypotheses = 15
alpha = 0.05

# Simulate p-values (mix of true positives and nulls)
true_effects = [0]*10 + [0.7, 0.9, 0.5, 1.2, 0.6]
raw_p = []
for d in true_effects:
    a = np.random.normal(0, 1, 40)
    b = np.random.normal(d, 1, 40)
    _, p = stats.ttest_ind(a, b)
    raw_p.append(p)

# BH procedure manually
sorted_idx = np.argsort(raw_p)
sorted_p   = np.array(raw_p)[sorted_idx]

print(f"BH procedure (alpha={alpha}, m={n_hypotheses} tests):")
print(f"{'Rank':>5s}  {'p-value':>8s}  {'BH thresh':>10s}  {'Reject?'}")
bh_threshold = alpha * np.arange(1, n_hypotheses+1) / n_hypotheses
last_reject  = -1
for rank, (p, thr) in enumerate(zip(sorted_p, bh_threshold), 1):
    if p <= thr:
        last_reject = rank

for rank, (p, thr) in enumerate(zip(sorted_p[:8], bh_threshold[:8]), 1):
    reject = rank <= last_reject
    print(f"{rank:5d}  {p:8.4f}  {thr:10.4f}  {reject}")
print(f"  ... ({n_hypotheses} total)")
print(f"\\nAll hypotheses with rank <= {last_reject} are rejected ({last_reject} total)")"""},
        {"label": "q-values and FDR estimation",
         "code": """from statsmodels.stats.multitest import multipletests
from scipy import stats
import numpy as np

np.random.seed(7)
m = 1000   # large-scale testing (genomics-like)
n_true = 50

# Generate p-values: 50 true effects + 950 nulls
p_true = np.array([stats.ttest_ind(
    np.random.normal(0,1,30), np.random.normal(0.6,1,30))[1]
    for _ in range(n_true)])
p_null = np.random.uniform(0, 1, m - n_true)  # null p-values ~ Uniform
all_p  = np.concatenate([p_true, p_null])
true_labels = np.array([True]*n_true + [False]*(m-n_true))

results = {}
for method in ['bonferroni', 'fdr_bh']:
    reject, _, _, _ = multipletests(all_p, alpha=0.05, method=method)
    tp = (reject & true_labels).sum()
    fp = (reject & ~true_labels).sum()
    fn = (~reject & true_labels).sum()
    fdr = fp / max(reject.sum(), 1)
    power = tp / n_true
    results[method] = (reject.sum(), tp, fp, fdr, power)
    print(f"{method:12s}: rejections={reject.sum():4d}  TP={tp:3d}  FP={fp:3d}  FDR={fdr:.3f}  Power={power:.3f}")

print(f"\\nSummary: Bonferroni is conservative; BH balances FDR and power")"""}
    ],
    rw_scenario="A genomics researcher tests differential expression for 5000 genes. Raw analysis finds 450 significant genes (p<0.05); after BH correction at FDR=0.05, only 180 remain — avoiding a list of mostly false discoveries.",
    rw_code="""from statsmodels.stats.multitest import multipletests
from scipy import stats
import numpy as np

np.random.seed(42)
n_genes = 5000
n_de    = 150  # truly differentially expressed

# Group A and B expression levels
expr_a = np.random.normal(0, 1, (n_genes, 30))
expr_b = np.random.normal(0, 1, (n_genes, 30))
# Inject true effects
effects = np.random.normal(0.8, 0.3, n_de)
expr_b[:n_de] += effects[:, np.newaxis]

# Compute p-values
p_vals = np.array([stats.ttest_ind(expr_a[i], expr_b[i])[1]
                   for i in range(n_genes)])

for method in ['none', 'bonferroni', 'fdr_bh']:
    if method == 'none':
        reject = p_vals < 0.05
        adj_p  = p_vals
    else:
        reject, adj_p, _, _ = multipletests(p_vals, alpha=0.05, method=method)

    tp = reject[:n_de].sum()
    fp = reject[n_de:].sum()
    print(f"{method:12s}: significant={reject.sum():5d}  TP={tp:4d}  FP={fp:4d}  FDR={fp/max(reject.sum(),1):.3f}")""",
    pt="Multi-Metric A/B Correction",
    pd_text="You ran an A/B test measuring 12 metrics simultaneously (CTR, bounce rate, time on page, conversions, etc.). Generate synthetic p-values for each metric (mix of some truly different and some null). Apply Bonferroni, Holm, BH corrections. For each method, print which metrics are significant. Discuss when you'd prefer BH over Bonferroni.",
    ps="""from statsmodels.stats.multitest import multipletests
import numpy as np
from scipy import stats

np.random.seed(42)
metrics = ['CTR','BounceRate','TimeOnPage','Conversions','PageViews',
           'ScrollDepth','CartAdds','Checkout','Revenue','SignUps','ReturnVisits','NPS']

# Simulate p-values: some metrics truly affected, most not
true_effects = [0.4, 0, 0, 0.6, 0, 0, 0.3, 0.5, 0, 0, 0, 0]
p_values = []
for d in true_effects:
    a = np.random.normal(0, 1, 200)
    b = np.random.normal(d, 1, 200)
    _, p = stats.ttest_ind(a, b)
    p_values.append(p)

# TODO: apply all three corrections
# TODO: print table showing which metrics are significant under each method
# TODO: comment on when to prefer BH vs Bonferroni
"""
)

# ── 24: Bootstrap & Permutation Tests ────────────────────────────────────────
s24 = make_s(24, "Bootstrap & Permutation Tests",
    "Bootstrap resampling estimates confidence intervals for any statistic without distributional assumptions. Permutation tests provide exact p-values for two-sample comparisons by shuffling group labels.",
    [
        {"label": "Bootstrap confidence intervals",
         "code": """import numpy as np
from scipy import stats

np.random.seed(42)
data = np.random.exponential(scale=5, size=50)  # skewed data

def bootstrap_ci(data, statistic, n_boot=5000, ci=0.95):
    boots = [statistic(np.random.choice(data, len(data), replace=True))
             for _ in range(n_boot)]
    alpha = (1 - ci) / 2
    return np.percentile(boots, [alpha*100, (1-alpha)*100]), np.array(boots)

# Bootstrap CI for mean, median, and std
for stat_name, fn in [('mean', np.mean), ('median', np.median), ('std', np.std)]:
    ci_boot, boots = bootstrap_ci(data, fn)
    # Compare to analytical (where available)
    print(f"{stat_name:7s}: obs={fn(data):.3f}  boot_CI=({ci_boot[0]:.3f}, {ci_boot[1]:.3f})")

# Analytical CI for mean (t-interval)
ci_t = stats.t.interval(0.95, df=len(data)-1, loc=data.mean(), scale=stats.sem(data))
print(f"\\nt-interval CI for mean: ({ci_t[0]:.3f}, {ci_t[1]:.3f})")
print(f"Boot CI for mean: above  (similar for large n, more robust for skewed)")"""},
        {"label": "Bootstrap for regression coefficients",
         "code": """import numpy as np
from scipy import stats

np.random.seed(0)
n = 80
x = np.random.randn(n)
y = 2.5 * x + 1.0 + np.random.randn(n) * 1.5

def ols(x, y):
    slope, intercept, *_ = stats.linregress(x, y)
    return slope, intercept

# Bootstrap CI for slope
n_boot = 5000
slopes = []
for _ in range(n_boot):
    idx = np.random.choice(n, n, replace=True)
    s, _ = ols(x[idx], y[idx])
    slopes.append(s)

slopes = np.array(slopes)
ci_slope = np.percentile(slopes, [2.5, 97.5])
obs_slope, obs_int = ols(x, y)

print(f"Observed slope:      {obs_slope:.4f}")
print(f"Bootstrap CI slope:  ({ci_slope[0]:.4f}, {ci_slope[1]:.4f})")

# Analytical CI from linregress
result = stats.linregress(x, y)
t_crit = stats.t.ppf(0.975, df=n-2)
se_slope = result.stderr
print(f"Analytical CI slope: ({obs_slope - t_crit*se_slope:.4f}, {obs_slope + t_crit*se_slope:.4f})")
print(f"Bootstrap SE of slope: {slopes.std():.4f}")"""},
        {"label": "Permutation test for two-sample comparison",
         "code": """import numpy as np
from scipy import stats

np.random.seed(42)

def permutation_test(a, b, n_perm=10000, stat='mean_diff'):
    obs_stat = a.mean() - b.mean()
    combined = np.concatenate([a, b])
    n_a = len(a)
    perm_stats = []
    for _ in range(n_perm):
        shuffled = np.random.permutation(combined)
        perm_stats.append(shuffled[:n_a].mean() - shuffled[n_a:].mean())
    perm_stats = np.array(perm_stats)
    p_val = (np.abs(perm_stats) >= np.abs(obs_stat)).mean()
    return obs_stat, p_val, perm_stats

# Test on small sample with non-normal data
group_a = np.random.exponential(3, 25)
group_b = np.random.exponential(4, 25)

obs, p_perm, perms = permutation_test(group_a, group_b)
_, p_mann = stats.mannwhitneyu(group_a, group_b, alternative='two-sided')
_, p_t    = stats.ttest_ind(group_a, group_b)

print(f"Observed mean diff: {obs:.3f}")
print(f"Permutation p-val:  {p_perm:.4f}")
print(f"Mann-Whitney p-val: {p_mann:.4f}")
print(f"t-test p-val:       {p_t:.4f}")
print(f"Percentile of obs in perm dist: {(perms < obs).mean():.3f}")"""}
    ],
    rw_scenario="A data scientist bootstraps the median response time for two API versions (non-normal, heavy-tailed). The bootstrap CI for the difference excludes 0, providing strong evidence version B is faster.",
    rw_code="""import numpy as np
from scipy import stats

np.random.seed(99)
# API response times (heavy-tailed)
version_a = np.random.pareto(2.0, 200) * 100 + 50
version_b = np.random.pareto(2.5, 200) * 80  + 45

# Bootstrap CI for difference in medians
n_boot = 10000
median_diffs = []
for _ in range(n_boot):
    a_boot = np.random.choice(version_a, len(version_a), replace=True)
    b_boot = np.random.choice(version_b, len(version_b), replace=True)
    median_diffs.append(np.median(a_boot) - np.median(b_boot))

ci = np.percentile(median_diffs, [2.5, 97.5])
obs_diff = np.median(version_a) - np.median(version_b)

print(f"Median A: {np.median(version_a):.2f}ms")
print(f"Median B: {np.median(version_b):.2f}ms")
print(f"Observed difference: {obs_diff:.2f}ms")
print(f"Bootstrap 95% CI: ({ci[0]:.2f}, {ci[1]:.2f})ms")
print(f"CI excludes 0: {ci[0] > 0 or ci[1] < 0} -> B is {'faster' if obs_diff > 0 else 'slower'}")""",
    pt="Bootstrap vs Analytical CI Comparison",
    pd_text="Generate 3 datasets: (1) Normal n=30, (2) Exponential n=30, (3) Heavy-tailed Pareto n=30. For each: compute bootstrap 95% CI for the mean (5000 resamples), the analytical t-interval, and the bootstrap CI for the median. Print all three side-by-side. Observe how they differ for non-normal data.",
    ps="""import numpy as np
from scipy import stats

np.random.seed(42)
datasets = {
    'Normal':    np.random.normal(10, 3, 30),
    'Exponential': np.random.exponential(5, 30),
    'Pareto':    np.random.pareto(1.5, 30) * 5 + 5,
}

def bootstrap_ci(data, fn, n_boot=5000):
    boots = [fn(np.random.choice(data, len(data), replace=True)) for _ in range(n_boot)]
    return np.percentile(boots, [2.5, 97.5])

for name, data in datasets.items():
    boot_mean   = bootstrap_ci(data, np.mean)
    t_ci        = stats.t.interval(0.95, df=len(data)-1, loc=data.mean(), scale=stats.sem(data))
    boot_median = bootstrap_ci(data, np.median)
    print(f"{name}:")
    print(f"  Bootstrap mean CI:    ({boot_mean[0]:.3f}, {boot_mean[1]:.3f})")
    # TODO: print t-interval and bootstrap median CI
"""
)

# ── Assemble ──────────────────────────────────────────────────────────────────
all_sections = s17+s18+s19+s20+s21+s22+s23+s24
result = insert_sections(FILE, MARKER, all_sections)
print("SUCCESS" if result else "FAILED")
