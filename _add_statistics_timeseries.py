"""Add 3 sections each to gen_statistics.py and gen_time_series.py."""
import re, sys
sys.path.insert(0, '.')
from _inserter import insert_sections

BASE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path"

def ec(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace("'", "\\'")

def make_section(num, title, examples, rw_scenario, rw_code, p_title, p_desc, p_starter):
    lines = [f'    {{\n        "title": "{num}. {title}",\n        "examples": [']
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples)-1 else ''
        lines.append(f'            {{\n                "label": "{ex["label"]}",\n                "code": "{ec(ex["code"])}"\n            }}{comma}')
    lines.append(f'        ],\n        "rw_scenario": "{ec(rw_scenario)}",')
    lines.append(f'        "rw_code": "{ec(rw_code)}",')
    lines.append(f'        "practice": {{\n            "title": "{p_title}",\n            "desc": "{ec(p_desc)}",\n            "starter": "{ec(p_starter)}"\n        }}\n    }},')
    return '\n'.join(lines) + '\n'

# ─── STATISTICS SECTIONS ──────────────────────────────────────────────────────

stat14_examples = [
    {
        "label": "Percentile Bootstrap CI",
        "code": """import numpy as np
np.random.seed(42)
data = np.random.exponential(scale=2, size=50)
B = 10000
boot_means = [np.mean(np.random.choice(data, size=len(data), replace=True)) for _ in range(B)]
ci = np.percentile(boot_means, [2.5, 97.5])
print(f"Sample mean: {np.mean(data):.4f}")
print(f"Bootstrap 95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]")"""
    },
    {
        "label": "BCa Bootstrap (Bias-Corrected)",
        "code": """import numpy as np
from scipy import stats
np.random.seed(7)
data = np.random.lognormal(0, 0.5, 80)
stat_obs = np.median(data)
B = 5000
boot_stats = [np.median(np.random.choice(data, size=len(data), replace=True)) for _ in range(B)]
# Bias correction
z0 = stats.norm.ppf(np.mean(np.array(boot_stats) < stat_obs))
# Acceleration (jackknife)
jk = [np.median(np.delete(data, i)) for i in range(len(data))]
jk_mean = np.mean(jk)
a = np.sum((jk_mean - np.array(jk))**3) / (6*np.sum((jk_mean - np.array(jk))**2)**1.5)
alpha = 0.05
z_lo = stats.norm.ppf(alpha/2); z_hi = stats.norm.ppf(1 - alpha/2)
p_lo = stats.norm.cdf(z0 + (z0+z_lo)/(1-a*(z0+z_lo)))
p_hi = stats.norm.cdf(z0 + (z0+z_hi)/(1-a*(z0+z_hi)))
ci = np.percentile(boot_stats, [p_lo*100, p_hi*100])
print(f"BCa 95% CI for median: [{ci[0]:.4f}, {ci[1]:.4f}]")"""
    },
    {
        "label": "Bootstrap Hypothesis Test (Permutation)",
        "code": """import numpy as np
np.random.seed(0)
group_a = np.random.normal(5.0, 1.5, 40)
group_b = np.random.normal(5.6, 1.5, 40)
obs_diff = np.mean(group_b) - np.mean(group_a)
combined = np.concatenate([group_a, group_b])
B = 10000
perm_diffs = []
for _ in range(B):
    perm = np.random.permutation(combined)
    perm_diffs.append(np.mean(perm[40:]) - np.mean(perm[:40]))
p_value = np.mean(np.abs(perm_diffs) >= np.abs(obs_diff))
print(f"Observed difference: {obs_diff:.4f}")
print(f"Permutation p-value: {p_value:.4f}")"""
    }
]

stat14_rw = "E-commerce A/B test: compare conversion rates between checkout designs using bootstrap CIs instead of assuming normality for small samples."
stat14_rw_code = """import numpy as np
np.random.seed(42)
# Simulated checkout conversion: design A=0.05, design B=0.065
n = 300
conv_a = np.random.binomial(1, 0.05, n).astype(float)
conv_b = np.random.binomial(1, 0.065, n).astype(float)
obs_diff = conv_b.mean() - conv_a.mean()
B = 20000
boot_diffs = [
    np.random.choice(conv_b, n, replace=True).mean() -
    np.random.choice(conv_a, n, replace=True).mean()
    for _ in range(B)
]
ci = np.percentile(boot_diffs, [2.5, 97.5])
p_val = np.mean(np.array(boot_diffs) <= 0)
print(f"Observed lift: {obs_diff:.4f} ({obs_diff/conv_a.mean():.1%} relative)")
print(f"95% Bootstrap CI: [{ci[0]:.4f}, {ci[1]:.4f}]")
print(f"One-sided p-value: {p_val:.4f}")
print("Significant at alpha=0.05:", ci[0] > 0)"""
stat14_pt = "Bootstrap Customer Lifetime Value"
stat14_pd = "You have 60 customer LTV values from a heavy-tailed distribution. Compute 90% and 95% percentile bootstrap CIs for the mean and the 75th percentile. Also run a two-sample permutation test comparing 'premium' vs 'standard' customers (30 each). Report p-values and effect sizes."
stat14_ps = """import numpy as np
np.random.seed(11)
ltv = np.random.pareto(2, 60) * 100 + 50
premium = ltv[:30]
standard = ltv[30:]
B = 10000
# TODO: Bootstrap 90% and 95% CIs for mean LTV
# TODO: Bootstrap CI for 75th percentile LTV
# TODO: Permutation test: premium vs standard mean LTV
# TODO: Report Cohen's d effect size
"""

stat15_examples = [
    {
        "label": "Bonferroni & Holm Corrections",
        "code": """import numpy as np
from scipy import stats
np.random.seed(42)
k = 20
# 18 nulls (no effect) + 2 true positives
p_values = np.concatenate([
    np.random.uniform(0, 1, 18),
    np.array([0.003, 0.011])
])
alpha = 0.05
bonferroni = p_values * k
reject_bon = bonferroni < alpha
# Holm correction
order = np.argsort(p_values)
holm = np.zeros(k)
for rank, idx in enumerate(order):
    holm[idx] = p_values[idx] * (k - rank)
reject_holm = holm < alpha
print(f"Bonferroni rejects: {reject_bon.sum()} tests")
print(f"Holm rejects:       {reject_holm.sum()} tests")"""
    },
    {
        "label": "Benjamini-Hochberg FDR Control",
        "code": """import numpy as np
np.random.seed(5)
k = 50
# 40 nulls + 10 true effects (small p-values)
p_values = np.concatenate([
    np.random.uniform(0.05, 1.0, 40),
    np.random.uniform(0, 0.02, 10)
])
alpha = 0.05
order = np.argsort(p_values)
sorted_p = p_values[order]
bh_threshold = (np.arange(1, k+1) / k) * alpha
reject_sorted = sorted_p <= bh_threshold
# All tests up to last rejection are rejected
last_reject = np.where(reject_sorted)[0]
if len(last_reject):
    cutoff = last_reject[-1]
    reject_bh = np.zeros(k, dtype=bool)
    reject_bh[order[:cutoff+1]] = True
else:
    reject_bh = np.zeros(k, dtype=bool)
print(f"BH FDR rejects: {reject_bh.sum()} of {k} tests")
print(f"Expected FDR ≤ {alpha}")"""
    },
    {
        "label": "Q-value (Storey's Method)",
        "code": """import numpy as np
np.random.seed(2)
k = 100
p_vals = np.concatenate([np.random.uniform(0,1,75), np.random.beta(0.5,5,25)])
# Estimate pi0 (proportion of true nulls)
lambdas = np.arange(0.05, 0.95, 0.05)
pi0_hat = [(p_vals >= l).sum() / (k * (1-l)) for l in lambdas]
pi0 = min(1.0, np.polyfit(lambdas, pi0_hat, 2)[2])  # smoother estimate
# Compute q-values
order = np.argsort(p_vals)
sorted_p = p_vals[order]
q = pi0 * k * sorted_p / (np.arange(1, k+1))
# Enforce monotonicity
for i in range(k-2, -1, -1):
    q[i] = min(q[i], q[i+1])
q_vals = np.empty(k); q_vals[order] = np.minimum(q, 1)
print(f"pi0 estimate: {pi0:.3f}")
print(f"Discoveries at FDR=0.05: {(q_vals <= 0.05).sum()}")"""
    }
]

stat15_rw = "Genomics pipeline: after running 10,000 gene expression tests, apply BH correction to control FDR at 5% and identify truly differentially expressed genes."
stat15_rw_code = """import numpy as np
np.random.seed(99)
n_genes = 10000
n_de = 200  # truly differentially expressed
# Simulate p-values: most null (uniform), some true effects (beta)
p_null = np.random.uniform(0, 1, n_genes - n_de)
p_de   = np.random.beta(0.3, 10, n_de)
p_values = np.concatenate([p_null, p_de])
alpha = 0.05
# BH procedure
order = np.argsort(p_values)
sorted_p = p_values[order]
ranks = np.arange(1, n_genes+1)
bh_thresh = (ranks / n_genes) * alpha
last = np.where(sorted_p <= bh_thresh)[0]
if len(last):
    cutoff = last[-1]
    reject = np.zeros(n_genes, dtype=bool)
    reject[order[:cutoff+1]] = True
else:
    reject = np.zeros(n_genes, dtype=bool)
# True positive rate among real DE genes
tp = reject[-n_de:].sum()
fp = reject[:-n_de].sum()
print(f"Significant genes: {reject.sum()}")
print(f"True positives: {tp}/{n_de} ({tp/n_de:.1%} sensitivity)")
print(f"False positives: {fp} (FDR={fp/max(reject.sum(),1):.3f})")"""
stat15_pt = "Drug Trial Multiple Endpoints"
stat15_pd = "A clinical trial tests 12 endpoints (primary + secondary). Raw p-values are given. Apply Bonferroni, Holm, and BH corrections. Build a table showing which endpoints remain significant under each method. Discuss the tradeoff between FWER and FDR control in regulatory contexts."
stat15_ps = """import numpy as np
# 12 endpoint p-values from clinical trial
p_values = np.array([0.001, 0.008, 0.023, 0.046, 0.052, 0.071,
                     0.12, 0.18, 0.21, 0.34, 0.52, 0.74])
k = len(p_values)
alpha = 0.05
# TODO: Bonferroni correction + reject/accept
# TODO: Holm step-down correction + reject/accept
# TODO: BH FDR correction + reject/accept
# TODO: Print comparison table
# TODO: Discuss which method to use and why
"""

stat16_examples = [
    {
        "label": "PCA for Outlier Detection",
        "code": """import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
np.random.seed(0)
X = np.random.multivariate_normal([0,0,0], [[1,.7,.3],[.7,1,.2],[.3,.2,1]], 200)
X[5] += [4, 4, 4]  # inject outlier
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
pca = PCA(n_components=2)
scores = pca.fit_transform(Xs)
reconstruction = pca.inverse_transform(scores)
residuals = np.sum((Xs - reconstruction)**2, axis=1)
threshold = np.percentile(residuals, 97.5)
outliers = np.where(residuals > threshold)[0]
print(f"Explained variance: {pca.explained_variance_ratio_.cumsum()[-1]:.2%}")
print(f"Reconstruction outliers (index): {outliers}")"""
    },
    {
        "label": "t-SNE for Cluster Visualization",
        "code": """import numpy as np
from sklearn.manifold import TSNE
from sklearn.datasets import make_blobs
np.random.seed(42)
X, y = make_blobs(n_samples=300, centers=4, n_features=8, cluster_std=1.5)
tsne = TSNE(n_components=2, perplexity=30, n_iter=300, random_state=42)
X_2d = tsne.fit_transform(X)
for cls in np.unique(y):
    mask = y == cls
    print(f"Cluster {cls}: centroid ({X_2d[mask,0].mean():.2f}, {X_2d[mask,1].mean():.2f}), n={mask.sum()}")
print(f"KL divergence: {tsne.kl_divergence_:.4f}")"""
    },
    {
        "label": "UMAP + Statistical Tests on Components",
        "code": """import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats
np.random.seed(1)
# Two groups with different multivariate structure
g1 = np.random.multivariate_normal([0]*5, np.eye(5), 100)
g2 = np.random.multivariate_normal([0.5]*5, np.eye(5)*1.5, 100)
X = np.vstack([g1, g2])
labels = np.array([0]*100 + [1]*100)
pca = PCA(n_components=3)
Xp = pca.fit_transform(StandardScaler().fit_transform(X))
for i in range(3):
    t, p = stats.ttest_ind(Xp[labels==0, i], Xp[labels==1, i])
    print(f"PC{i+1}: t={t:.3f}, p={p:.4f} ({'significant' if p<0.05 else 'not sig'})")
print(f"Total variance explained: {pca.explained_variance_ratio_.sum():.2%}")"""
    }
]

stat16_rw = "Credit risk modelling: apply PCA to 20 correlated financial features, use the top components as inputs for logistic regression, and test if the components differ significantly between default and non-default customers."
stat16_rw_code = """import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from scipy import stats
np.random.seed(42)
n = 500
# 20 correlated features simulating financial metrics
cov = 0.4 * np.ones((20, 20)) + 0.6 * np.eye(20)
X_raw = np.random.multivariate_normal(np.zeros(20), cov, n)
# Default probability depends on first latent factor
latent = X_raw[:, :5].mean(axis=1)
prob = 1 / (1 + np.exp(-(latent - 0.3)))
y = np.random.binomial(1, prob, n)
scaler = StandardScaler()
X = scaler.fit_transform(X_raw)
pca = PCA(n_components=5)
X_pca = pca.fit_transform(X)
print(f"Variance explained: {pca.explained_variance_ratio_.cumsum()[-1]:.2%}")
for i in range(5):
    t, p = stats.ttest_ind(X_pca[y==0, i], X_pca[y==1, i])
    print(f"PC{i+1}: defaulters vs non-defaulters t={t:.2f}, p={p:.4f}")
clf = LogisticRegression()
scores = cross_val_score(clf, X_pca, y, cv=5, scoring='roc_auc')
print(f"Logistic Regression AUC (PCA features): {scores.mean():.3f} ± {scores.std():.3f}")"""
stat16_pt = "Customer Segmentation with Dimensionality Reduction"
stat16_pd = "Apply PCA then k-means (k=4) to a simulated customer dataset with 15 features. For each cluster, run one-way ANOVA on the top 3 PCs and 3 original features to test for between-cluster differences. Report F-statistics, p-values, and effect sizes (eta-squared). Visualize clusters in 2D PCA space."
stat16_ps = """import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats
np.random.seed(21)
X = np.random.randn(400, 15)
# Inject 4-cluster structure
for i in range(4):
    X[i*100:(i+1)*100, :5] += i * 1.2
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
# TODO: PCA to 2D and 5D
# TODO: KMeans(k=4) on 5D PCA
# TODO: ANOVA on top 3 PCs and 3 original features per cluster
# TODO: Report eta-squared effect sizes
# TODO: Plot 2D PCA colored by cluster
"""

# ─── TIME SERIES SECTIONS ────────────────────────────────────────────────────

ts14_examples = [
    {
        "label": "Discrete Wavelet Transform (DWT)",
        "code": """import numpy as np
import pywt
np.random.seed(0)
t = np.linspace(0, 8*np.pi, 512)
signal = (np.sin(t) + 0.5*np.sin(5*t) + np.random.normal(0, 0.2, 512))
wavelet = 'db4'
level = 4
coeffs = pywt.wavedec(signal, wavelet, level=level)
print(f"Decomposition levels: {len(coeffs)-1}")
print(f"Approximation coeff shape: {coeffs[0].shape}")
for i, c in enumerate(coeffs[1:], 1):
    print(f"  Detail level {i}: shape={c.shape}, energy={np.sum(c**2):.2f}")
# Denoise: zero out small detail coefficients
threshold = 0.3
coeffs_denoised = [coeffs[0]] + [pywt.threshold(c, threshold, mode='soft') for c in coeffs[1:]]
denoised = pywt.waverec(coeffs_denoised, wavelet)[:len(signal)]
mse = np.mean((signal - denoised)**2)
print(f"Denoising MSE: {mse:.4f}")"""
    },
    {
        "label": "Continuous Wavelet Transform (CWT) Scalogram",
        "code": """import numpy as np
import pywt
np.random.seed(1)
fs = 100  # Hz
t = np.arange(0, 4, 1/fs)
# Chirp: frequency increases from 5 to 20 Hz
freq = 5 + 15*t/4
signal = np.sin(2*np.pi*freq*t) + np.random.normal(0, 0.1, len(t))
widths = np.arange(1, 64)
cwt_matrix, freqs = pywt.cwt(signal, widths, 'morl', sampling_period=1/fs)
power = np.abs(cwt_matrix)**2
# Peak frequency at start vs end
t_start = slice(0, 50); t_end = slice(350, 400)
peak_freq_start = freqs[np.argmax(power[:, t_start].mean(axis=1))]
peak_freq_end   = freqs[np.argmax(power[:, t_end].mean(axis=1))]
print(f"Dominant frequency (start): {peak_freq_start:.1f} Hz")
print(f"Dominant frequency (end):   {peak_freq_end:.1f} Hz")"""
    },
    {
        "label": "Wavelet-Based Anomaly Detection",
        "code": """import numpy as np
import pywt
np.random.seed(42)
n = 1000
ts = np.sin(2*np.pi*np.arange(n)/50) + np.random.normal(0, 0.1, n)
# Inject anomalies
ts[300:310] += 3.0
ts[700] -= 4.0
# DWT anomaly detection via reconstruction error per window
coeffs = pywt.wavedec(ts, 'haar', level=3)
# Zero out detail at level 1 (high-freq noise)
coeffs[1] = np.zeros_like(coeffs[1])
reconstructed = pywt.waverec(coeffs, 'haar')[:n]
residuals = np.abs(ts - reconstructed)
threshold = residuals.mean() + 3*residuals.std()
anomaly_idx = np.where(residuals > threshold)[0]
print(f"Anomalies detected at indices: {anomaly_idx[:10]}")
print(f"True anomaly regions: 300-310, 700")"""
    }
]

ts14_rw = "Manufacturing: use wavelet decomposition to separate machine vibration signals by frequency band, detect bearing faults (high-frequency detail) while ignoring normal operational frequencies."
ts14_rw_code = """import numpy as np
import pywt
np.random.seed(7)
fs = 1000  # 1 kHz sampling
t = np.arange(0, 2, 1/fs)  # 2 seconds
# Normal operation: 10 Hz fundamental + harmonics
normal = (np.sin(2*np.pi*10*t) + 0.3*np.sin(2*np.pi*20*t) +
          np.random.normal(0, 0.05, len(t)))
# Fault: adds 150 Hz bearing frequency
fault  = normal + 0.5*np.sin(2*np.pi*150*t)
for label, sig in [('Normal', normal), ('Fault', fault)]:
    coeffs = pywt.wavedec(sig, 'db4', level=5)
    # Level 1 detail captures highest frequencies
    hf_energy = np.sum(coeffs[1]**2) / np.sum(sig**2)
    print(f"{label}: high-freq energy ratio = {hf_energy:.4f}")
    energies = [np.sum(c**2) / np.sum(sig**2) for c in coeffs]
    print(f"  Energy by level: " + ", ".join(f"L{i}={e:.3f}" for i, e in enumerate(energies)))"""
ts14_pt = "EEG Brainwave Analysis"
ts14_pd = "Given a simulated EEG signal (1-second, 256 Hz) with delta (1-4 Hz), alpha (8-13 Hz), and beta (13-30 Hz) components, use wavelet decomposition to extract each band. Report the relative power of each band. Inject a 50ms epileptic spike at t=0.5s and detect it using wavelet residuals."
ts14_ps = """import numpy as np
import pywt
fs = 256  # Hz
t = np.arange(0, 1, 1/fs)
# Multi-band EEG signal
delta = 0.5 * np.sin(2*np.pi*2*t)
alpha = 0.3 * np.sin(2*np.pi*10*t)
beta  = 0.2 * np.sin(2*np.pi*20*t)
noise = np.random.normal(0, 0.05, len(t))
eeg = delta + alpha + beta + noise
# Inject spike
spike_start = int(0.5 * fs)
eeg[spike_start:spike_start+13] += 3.0
# TODO: DWT decomposition with 'db4', level=5
# TODO: Identify which detail levels correspond to each EEG band
# TODO: Compute relative band powers
# TODO: Detect spike using reconstruction error
"""

ts15_examples = [
    {
        "label": "Vector Autoregression (VAR)",
        "code": """import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR
np.random.seed(42)
n = 200
e1, e2 = np.random.normal(0, 1, n), np.random.normal(0, 1, n)
y1, y2 = np.zeros(n), np.zeros(n)
for t in range(1, n):
    y1[t] = 0.6*y1[t-1] + 0.2*y2[t-1] + e1[t]
    y2[t] = 0.1*y1[t-1] + 0.7*y2[t-1] + e2[t]
df = pd.DataFrame({'y1': y1, 'y2': y2})
model = VAR(df)
results = model.fit(maxlags=4, ic='aic')
print(f"Selected lag order: {results.k_ar}")
forecast = results.forecast(df.values[-results.k_ar:], steps=5)
print("5-step forecast:"); print(forecast.round(3))"""
    },
    {
        "label": "Granger Causality Test",
        "code": """import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
np.random.seed(1)
n = 300
eps1 = np.random.normal(0, 1, n)
eps2 = np.random.normal(0, 1, n)
x = np.zeros(n); y = np.zeros(n)
for t in range(2, n):
    x[t] = 0.5*x[t-1] + eps1[t]
    y[t] = 0.4*x[t-1] + 0.3*y[t-1] + eps2[t]  # x Granger-causes y
df = pd.DataFrame({'y': y, 'x': x})
max_lag = 4
print("Granger causality (x -> y):")
res = grangercausalitytests(df[['y','x']], maxlag=max_lag, verbose=False)
for lag, r in res.items():
    f_stat = r[0]['ssr_ftest'][0]
    p_val  = r[0]['ssr_ftest'][1]
    print(f"  Lag {lag}: F={f_stat:.3f}, p={p_val:.4f}")"""
    },
    {
        "label": "Cointegration & Error Correction",
        "code": """import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
from statsmodels.regression.linear_model import OLS
np.random.seed(5)
n = 500
common_trend = np.cumsum(np.random.normal(0, 1, n))
y1 = common_trend + np.random.normal(0, 0.5, n)
y2 = 0.8 * common_trend + 1.2 + np.random.normal(0, 0.5, n)
score, pvalue, _ = coint(y1, y2)
print(f"Cointegration test: t={score:.4f}, p={pvalue:.4f}")
# Estimate cointegrating vector
beta = OLS(y1, np.column_stack([np.ones(n), y2])).fit().params
spread = y1 - beta[1]*y2 - beta[0]
z_spread = (spread - spread.mean()) / spread.std()
print(f"Spread mean-reversion: current z-score = {z_spread[-1]:.3f}")"""
    }
]

ts15_rw = "Macroeconomic forecasting: model GDP, inflation, and interest rates jointly using VAR to capture cross-variable dynamics and produce scenario forecasts for monetary policy analysis."
ts15_rw_code = """import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.stattools import grangercausalitytests
np.random.seed(10)
n = 120  # 10 years monthly
# Simulate: interest rate affects inflation with lag, both affect GDP
ir = np.cumsum(np.random.normal(0, 0.1, n)) + 3.0
inf = 0.5*np.roll(ir, 2) + np.cumsum(np.random.normal(0, 0.05, n)) + 2.0
gdp = -0.3*np.roll(ir, 3) + 0.4*np.roll(inf, 1) + np.cumsum(np.random.normal(0, 0.08, n)) + 2.5
df = pd.DataFrame({'gdp': gdp, 'inflation': inf, 'interest_rate': ir})
df = df.diff().dropna()  # difference to achieve stationarity
model = VAR(df)
res = model.fit(maxlags=6, ic='aic')
print(f"VAR lag order: {res.k_ar}")
forecast = res.forecast(df.values[-res.k_ar:], steps=12)
print(f"12-month GDP forecast range: {forecast[:,0].min():.3f} to {forecast[:,0].max():.3f}")
# Impulse response
irf = res.irf(10)
print(f"GDP response to interest shock at lag 3: {irf.orth_irfs[3, 0, 2]:.4f}")"""
ts15_pt = "Pairs Trading Signal"
ts15_pd = "Using two simulated stock price series that are cointegrated (sharing a common random walk), implement a pairs trading strategy: (1) verify cointegration with Engle-Granger test, (2) estimate the spread, (3) generate long/short signals when z-score > 2 or < -2, (4) backtest and report Sharpe ratio and max drawdown."
ts15_ps = """import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
from statsmodels.regression.linear_model import OLS
np.random.seed(3)
n = 500
common = np.cumsum(np.random.normal(0, 1, n))
price_a = common + np.random.normal(0, 0.5, n) + 50
price_b = 0.9*common + np.random.normal(0, 0.5, n) + 45
# TODO: Cointegration test
# TODO: Compute hedge ratio and spread
# TODO: Z-score of spread
# TODO: Generate trading signals (long A-short B when z<-2, vice versa)
# TODO: Compute daily P&L, Sharpe ratio, max drawdown
"""

ts16_examples = [
    {
        "label": "Online Learning with River",
        "code": """# pip install river
from river import linear_model, preprocessing, metrics, stream
import numpy as np
np.random.seed(0)
n = 1000
X_data = np.column_stack([np.random.randn(n), np.arange(n)/n])
y_data = 3*X_data[:,0] - 2*X_data[:,1] + 0.5 + np.random.normal(0, 0.3, n)
model = preprocessing.StandardScaler() | linear_model.LinearRegression()
metric = metrics.RMSE()
for i, (xi, yi) in enumerate(zip(X_data, y_data)):
    x_dict = {'f0': xi[0], 'f1': xi[1]}
    y_pred = model.predict_one(x_dict)
    if y_pred is not None:
        metric.update(yi, y_pred)
    model.learn_one(x_dict, yi)
    if i % 200 == 0 and y_pred is not None:
        print(f"  n={i}: running RMSE={metric.get():.4f}")
print(f"Final RMSE: {metric.get():.4f}")"""
    },
    {
        "label": "Concept Drift Detection (ADWIN)",
        "code": """# pip install river
from river import drift
import numpy as np
np.random.seed(7)
detector = drift.ADWIN()
stream = np.concatenate([
    np.random.normal(0, 1, 500),
    np.random.normal(3, 1, 500)  # sudden drift at t=500
])
drifts = []
for i, x in enumerate(stream):
    detector.update(x)
    if detector.drift_detected:
        drifts.append(i)
        detector = drift.ADWIN()  # reset
print(f"Drift detected at sample(s): {drifts}")"""
    },
    {
        "label": "Sliding Window Streaming Statistics",
        "code": """import numpy as np
from collections import deque
class StreamStats:
    def __init__(self, window=100):
        self.w = deque(maxlen=window)
        self.n = 0
    def update(self, x):
        self.w.append(x)
        self.n += 1
        return self.mean(), self.std()
    def mean(self): return np.mean(self.w)
    def std(self):  return np.std(self.w, ddof=1) if len(self.w) > 1 else 0.0
np.random.seed(1)
ss = StreamStats(window=50)
for i in range(300):
    val = np.random.normal(5 if i < 150 else 8, 1)
    mean, std = ss.update(val)
    if i % 50 == 49:
        print(f"  t={i+1}: window mean={mean:.3f}, std={std:.3f}")"""
    }
]

ts16_rw = "IoT sensor network: process a continuous stream of temperature readings at 10 Hz from 50 sensors, detect anomalies in real-time using sliding window statistics, and adapt the baseline when ADWIN detects environmental regime changes."
ts16_rw_code = """import numpy as np
from collections import deque
np.random.seed(42)
n_sensors, n_steps = 5, 1000
window = 60
baselines = [deque(maxlen=window) for _ in range(n_sensors)]
alerts = {i: [] for i in range(n_sensors)}
# Inject drift at step 600 for sensor 2
for t in range(n_steps):
    readings = np.random.normal(22, 0.5, n_sensors)
    if t >= 600:
        readings[2] += 4.0  # sensor 2 drifts
    for s in range(n_sensors):
        baselines[s].append(readings[s])
        if len(baselines[s]) >= 20:
            mu = np.mean(baselines[s])
            sigma = np.std(baselines[s], ddof=1)
            z = (readings[s] - mu) / max(sigma, 1e-6)
            if abs(z) > 3:
                alerts[s].append(t)
for s in range(n_sensors):
    if alerts[s]:
        print(f"Sensor {s}: {len(alerts[s])} alerts, first at t={alerts[s][0]}")
    else:
        print(f"Sensor {s}: no alerts")"""
ts16_pt = "Real-Time Fraud Score Streaming"
ts16_pd = "Simulate a stream of 2000 credit card transactions (amount, time_since_last, is_weekend). Use online logistic regression (River) trained incrementally. At t=1000, inject a concept drift (fraudsters change behavior). Detect drift using ADWIN on prediction errors. Report AUC before and after drift, and adaptation speed."
ts16_ps = """# pip install river
from river import linear_model, preprocessing, metrics, drift, stream as rv_stream
import numpy as np
np.random.seed(99)
n = 2000
# Generate transactions
amounts = np.random.exponential(50, n)
gaps = np.random.exponential(10, n)
is_weekend = np.random.randint(0, 2, n)
# Fraud rule: changes at t=1000
fraud_prob_before = 1 / (1 + np.exp(-(amounts/100 - 0.5)))
fraud_prob_after  = 1 / (1 + np.exp(-(gaps/5 - 1.0)))  # different pattern
y = np.array([
    np.random.binomial(1, fraud_prob_before[i]) if i < 1000
    else np.random.binomial(1, fraud_prob_after[i])
    for i in range(n)
])
# TODO: Online logistic regression with River
# TODO: ADWIN drift detection on binary prediction errors
# TODO: Report AUC in windows before drift, at drift, after adaptation
"""

# ─── BUILD SECTIONS STRINGS ──────────────────────────────────────────────────

stat_sections = (
    make_section("14", "Bootstrap Methods & Resampling",
                 stat14_examples, stat14_rw, stat14_rw_code,
                 stat14_pt, stat14_pd, stat14_ps) +
    make_section("15", "Multiple Testing & FDR Control",
                 stat15_examples, stat15_rw, stat15_rw_code,
                 stat15_pt, stat15_pd, stat15_ps) +
    make_section("16", "Dimensionality Reduction for Statistical Analysis",
                 stat16_examples, stat16_rw, stat16_rw_code,
                 stat16_pt, stat16_pd, stat16_ps)
)

ts_sections = (
    make_section("14", "Wavelet Analysis for Time Series",
                 ts14_examples, ts14_rw, ts14_rw_code,
                 ts14_pt, ts14_pd, ts14_ps) +
    make_section("15", "Multivariate Time Series & VAR Models",
                 ts15_examples, ts15_rw, ts15_rw_code,
                 ts15_pt, ts15_pd, ts15_ps) +
    make_section("16", "Real-Time Streaming & Online Learning",
                 ts16_examples, ts16_rw, ts16_rw_code,
                 ts16_pt, ts16_pd, ts16_ps)
)

# ─── INSERT ──────────────────────────────────────────────────────────────────

import os

stat_path = os.path.join(BASE, "gen_statistics.py")
ts_path   = os.path.join(BASE, "gen_time_series.py")

insert_sections(stat_path, "]  # end SECTIONS", stat_sections)

# time_series uses ]\n\n# ─── as its section terminator
# Use rfind on custom marker
content = open(ts_path, encoding='utf-8').read()
marker = "]\n\n# \u2500\u2500\u2500 Output"
idx = content.find(marker)
if idx == -1:
    print("ERROR: time_series marker not found")
else:
    before = content[:idx].rstrip()
    if before.endswith('}') and not before.endswith('},'):
        insert_str = before + ',\n\n' + ts_sections + content[idx:]
    else:
        insert_str = content[:idx] + ts_sections + content[idx:]
    open(ts_path, 'w', encoding='utf-8').write(insert_str)
    print(f"OK: inserted sections into {ts_path}")

print("Done!")
