#!/usr/bin/env python3
"""Generate Statistics with Python study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE   = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\11_statistics")
BASE.mkdir(parents=True, exist_ok=True)
ACCENT = "#58a6ff"
EMOJI  = "📊"
TITLE  = "Statistics with Python"

def make_html(sections):
    nav = "\n    ".join(
        f'<li><a href="#s{i}" onclick="act(this,event)">{esc(s["title"])}</a></li>'
        for i, s in enumerate(sections))
    cards = ""
    for i, s in enumerate(sections):
        blks = ""
        for j, ex in enumerate(s.get("examples", [])):
            cid = f"c{i}_{j}"
            blks += (f'<div class="code-block"><div class="ch"><span>{esc(ex.get("label","Example"))}</span>'
                     f'<button onclick="cp(\'{cid}\')">Copy</button></div>'
                     f'<pre><code id="{cid}" class="language-python">{esc(ex["code"])}</code></pre></div>')
        rw_scenario = s.get("rw_scenario", "")
        rw_code = s.get("rw_code", "")
        rw_html = ""
        if rw_scenario:
            rwid = f"rw{i}"
            rw_html = (f'<div class="rw"><div class="rh">&#x1F4BC; Real-World Scenario</div>'
                       f'<div class="rd">{esc(rw_scenario)}</div>'
                       f'<div class="code-block"><div class="ch"><span>Real-World Code</span>'
                       f'<button onclick="cp(\'{rwid}\')">Copy</button></div>'
                       f'<pre><code id="{rwid}" class="language-python">{esc(rw_code)}</code></pre></div></div>')
        practice = s.get("practice", {})
        practice_html = ""
        if practice:
            pid = f"p{i}"
            practice_html = (
                f'<div class="practice">'
                f'<div class="ph">&#x1F3CB;&#xFE0F; Practice: {esc(practice["title"])}</div>'
                f'<div class="pd">{esc(practice["desc"])}</div>'
                f'<div class="code-block"><div class="ch"><span>Starter Code</span>'
                f'<button onclick="cp(\'{pid}\')">Copy</button></div>'
                f'<pre><code id="{pid}" class="language-python">{esc(practice["starter"])}</code></pre></div>'
                f'</div>'
            )
        cards += (f'<div class="topic" id="s{i}"><div class="th" onclick="tog(this)"><span>{esc(s["title"])}</span>'
                  f'<span class="arr">&#9660;</span></div><div class="tb"><p class="desc">{esc(s.get("desc",""))}</p>'
                  f'{blks}{rw_html}{practice_html}</div></div>')
    n = len(sections)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE} Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>:root{{--bg:#0f1117;--sb:#161b22;--card:#1c2128;--brd:#30363d;--txt:#c9d1d9;--mut:#8b949e;--acc:{ACCENT}}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{display:flex;min-height:100vh;background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px}}
.sidebar{{width:260px;min-height:100vh;background:var(--sb);border-right:1px solid var(--brd);position:sticky;top:0;height:100vh;overflow-y:auto;flex-shrink:0}}
.sbh{{padding:20px;border-bottom:1px solid var(--brd)}}.sbh h2{{font-size:1.05rem;color:var(--acc)}}.sbh p{{font-size:.8rem;color:var(--mut);margin-top:3px}}
#q{{width:100%;padding:7px 10px;background:#0d1117;border:1px solid var(--brd);border-radius:6px;color:var(--txt);font-size:.84rem;margin-top:10px}}#q:focus{{outline:none;border-color:var(--acc)}}
.nav-list{{list-style:none;padding:6px 0}}.nav-list li a{{display:block;padding:7px 18px;color:var(--mut);text-decoration:none;font-size:.84rem;border-left:3px solid transparent;transition:.15s}}
.nav-list li a:hover,.nav-list li a.active{{color:var(--txt);border-left-color:var(--acc);background:rgba(255,255,255,.03)}}
.main{{flex:1;padding:32px 40px;max-width:880px}}.pt{{font-size:2rem;font-weight:700;color:var(--acc);margin-bottom:6px}}.ps{{color:var(--mut);margin-bottom:28px}}
.topic{{background:var(--card);border:1px solid var(--brd);border-radius:8px;margin-bottom:14px;overflow:hidden}}
.th{{display:flex;justify-content:space-between;align-items:center;padding:13px 18px;cursor:pointer;user-select:none}}.th:hover{{background:rgba(255,255,255,.04)}}
.th>span:first-child{{font-weight:600}}.arr{{color:var(--mut);transition:transform .2s}}.tb{{display:none;padding:18px;border-top:1px solid var(--brd)}}.tb.open{{display:block}}.arr.open{{transform:rotate(180deg)}}
.desc{{color:var(--mut);margin-bottom:14px;line-height:1.6;font-size:.92rem}}.code-block{{margin-bottom:14px;border:1px solid var(--brd);border-radius:6px;overflow:hidden}}
.ch{{display:flex;justify-content:space-between;padding:7px 12px;background:#161b22;font-size:.78rem;color:var(--mut)}}.ch button{{background:0;border:1px solid var(--brd);color:var(--mut);padding:2px 9px;border-radius:4px;cursor:pointer;font-size:.73rem}}.ch button:hover{{color:var(--txt);border-color:var(--acc)}}
pre{{margin:0}}pre code{{font-size:.83rem;padding:13px!important}}.rw{{background:#0d2818;border:1px solid #238636;border-radius:6px;padding:15px;margin-top:6px}}
.rh{{font-weight:600;color:#3fb950;margin-bottom:7px}}.rd{{color:#7ee787;font-size:.84rem;margin-bottom:11px;line-height:1.5}}
.practice{{background:#0d1b2a;border:1px solid #388bfd;border-radius:6px;padding:15px;margin-top:8px}}
.ph{{font-weight:600;color:#58a6ff;margin-bottom:7px}}
.pd{{color:#79c0ff;font-size:.84rem;margin-bottom:11px;line-height:1.5}}</style></head><body>
<aside class="sidebar"><div class="sbh"><h2>{EMOJI} {TITLE}</h2><p>Study Guide &bull; {n} topics</p>
<input id="q" placeholder="Search..." oninput="filt(this.value)"></div>
<ul class="nav-list" id="nl">{nav}</ul></aside>
<main class="main"><h1 class="pt">{EMOJI} {TITLE}</h1><p class="ps">{n} topics &bull; Click any card to expand</p>{cards}</main>
<script>hljs.highlightAll();
function tog(h){{var b=h.nextElementSibling,a=h.querySelector('.arr');b.classList.toggle('open');a.classList.toggle('open');}}
function act(el,e){{if(e)e.preventDefault();document.querySelectorAll('.nav-list a').forEach(a=>a.classList.remove('active'));el.classList.add('active');}}
function filt(q){{document.querySelectorAll('#nl li').forEach(li=>{{li.style.display=li.textContent.toLowerCase().includes(q.toLowerCase())?'':'none';}});}}
function cp(id){{navigator.clipboard.writeText(document.getElementById(id).innerText).catch(()=>{{}});}}
document.addEventListener('DOMContentLoaded',()=>{{var fh=document.querySelector('.th');if(fh)fh.click();var fa=document.querySelector('.nav-list a');if(fa)fa.classList.add('active');}});
</script></body></html>"""

def make_nb(sections):
    cells=[]; n=[0]
    def nid(): n[0]+=1; return f"{n[0]:04d}"
    def md(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"markdown","id":nid(),"metadata":{},"source":s}
    def code(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"code","execution_count":None,"id":nid(),"metadata":{},"outputs":[],"source":s}
    cells.append(md(f"# {TITLE} Study Guide\n\nHands-on statistics guide using numpy, scipy.stats, pandas, and statsmodels."))
    for i,s in enumerate(sections,1):
        cells.append(md(f"## {i}. {s['title']}\n\n{s.get('desc','')}"))
        for ex in s.get("examples",[]):
            if ex.get("label"): cells.append(md(f"**{ex['label']}**"))
            cells.append(code(ex["code"]))
        rw_scenario = s.get("rw_scenario","")
        rw_code = s.get("rw_code","")
        if rw_scenario:
            cells.append(md(f"### Real-World Scenario\n\n> {rw_scenario}"))
            cells.append(code(rw_code))
        practice = s.get("practice")
        if practice:
            cells.append(md(f"### Practice: {practice['title']}\n\n{practice['desc']}"))
            cells.append(code(practice["starter"]))
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.11.0"}},"nbformat":4,"nbformat_minor":5}


# ─── Content ──────────────────────────────────────────────────────────────────
SECTIONS = [

{
"title": "1. Descriptive Statistics",
"desc": "Descriptive statistics summarize and describe the main features of a dataset. Key measures include central tendency (mean, median, mode) and spread (std, variance, percentiles, IQR). NumPy and scipy.stats provide fast, vectorized implementations.",
"examples": [
{"label": "Mean, median, mode with numpy and scipy", "code":
"""import numpy as np
from scipy import stats

data = [23, 45, 12, 67, 34, 45, 89, 23, 45, 56, 78, 34, 23, 90, 12]

mean   = np.mean(data)
median = np.median(data)
mode   = stats.mode(data, keepdims=True)

print(f"Mean:   {mean:.2f}")
print(f"Median: {median:.2f}")
print(f"Mode:   {mode.mode[0]}  (count: {mode.count[0]})")"""},
{"label": "Standard deviation, variance, and IQR", "code":
"""import numpy as np
from scipy import stats

data = np.array([12, 15, 14, 10, 18, 21, 13, 16, 14, 15, 17, 20, 11, 19, 14])

std_pop  = np.std(data, ddof=0)   # population std
std_samp = np.std(data, ddof=1)   # sample std (Bessel's correction)
var_samp = np.var(data, ddof=1)

q1, q3 = np.percentile(data, [25, 75])
iqr = stats.iqr(data)

print(f"Population std:  {std_pop:.4f}")
print(f"Sample std:      {std_samp:.4f}")
print(f"Sample variance: {var_samp:.4f}")
print(f"Q1={q1}, Q3={q3}, IQR={iqr}")"""},
{"label": "Percentiles and summary statistics with pandas", "code":
"""import numpy as np
import pandas as pd

np.random.seed(42)
data = pd.Series(np.random.normal(loc=100, scale=15, size=200))

print("=== Summary Statistics ===")
print(data.describe())
print(f"\nSkewness:  {data.skew():.4f}")
print(f"Kurtosis:  {data.kurtosis():.4f}")
print(f"5th  pctl: {data.quantile(0.05):.2f}")
print(f"95th pctl: {data.quantile(0.95):.2f}")"""},
{"label": "Outlier detection using IQR fence", "code":
"""import numpy as np
from scipy import stats

np.random.seed(0)
data = np.concatenate([np.random.normal(50, 5, 95), [10, 200, 95, 105, -5]])

q1, q3 = np.percentile(data, [25, 75])
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

outliers = data[(data < lower_fence) | (data > upper_fence)]
z_scores  = np.abs(stats.zscore(data))

print(f"IQR fences: [{lower_fence:.2f}, {upper_fence:.2f}]")
print(f"Outliers (IQR): {sorted(outliers)}")
print(f"Outliers (|z|>3): {data[z_scores > 3].tolist()}")"""},
],
"rw_scenario": "A data scientist at a hospital needs to summarize patient blood pressure readings to report to clinicians. They must identify the typical range, spot extreme values, and present skewness of the distribution before modeling.",
"rw_code":
"""import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(7)
# Simulate systolic BP for 300 patients (some hypertensive outliers)
bp = np.concatenate([
    np.random.normal(120, 12, 270),   # normal range
    np.random.normal(170, 10, 30),    # hypertensive group
])
series = pd.Series(bp, name="Systolic_BP")

print("=== Blood Pressure Summary ===")
print(series.describe().round(2))

q1, q3 = np.percentile(bp, [25, 75])
iqr = q3 - q1
print(f"\nIQR:         {iqr:.2f} mmHg")
print(f"Skewness:    {series.skew():.3f}")

high_bp = bp[bp > 140]
print(f"Hypertensive (>140): {len(high_bp)} patients ({100*len(high_bp)/len(bp):.1f}%)")
""",
"practice": {
    "title": "Analyze a Sales Dataset",
    "desc": "Given a list of daily sales figures, compute mean, median, std, IQR, and identify any outliers using both the IQR fence and z-score methods. Report the percentage of days with sales above the 90th percentile.",
    "starter":
"""import numpy as np
from scipy import stats

np.random.seed(123)
daily_sales = np.concatenate([
    np.random.normal(5000, 800, 90),
    np.random.normal(12000, 500, 10),  # exceptional days
])

# TODO: Compute mean, median, std, IQR
# TODO: Find outliers using IQR fence
# TODO: Find outliers using z-score (|z| > 2)
# TODO: Report % of days above 90th percentile
"""
}
},

{
"title": "2. Probability Distributions",
"desc": "Probability distributions model the likelihood of outcomes. scipy.stats provides a unified interface for continuous distributions (normal, exponential) and discrete distributions (binomial, Poisson) with PDF/PMF, CDF, and random variates.",
"examples": [
{"label": "Normal distribution — PDF, CDF, PPF", "code":
"""import numpy as np
from scipy import stats

mu, sigma = 0, 1
dist = stats.norm(loc=mu, scale=sigma)

x_vals = [-2, -1, 0, 1, 2]
print("x     PDF       CDF")
for x in x_vals:
    print(f"{x:+.0f}  {dist.pdf(x):.6f}  {dist.cdf(x):.6f}")

# Percent-point function (inverse CDF)
print(f"\n95th percentile (PPF): {dist.ppf(0.95):.4f}")
print(f"P(-1 < X < 1):         {dist.cdf(1) - dist.cdf(-1):.4f}")
print(f"P(-2 < X < 2):         {dist.cdf(2) - dist.cdf(-2):.4f}")"""},
{"label": "Binomial distribution — PMF and CDF", "code":
"""import numpy as np
from scipy import stats

n, p = 20, 0.3   # 20 trials, 30% success rate
dist = stats.binom(n=n, p=p)

print(f"Binomial(n={n}, p={p})")
print(f"Mean: {dist.mean():.2f}, Std: {dist.std():.2f}")
print()
print("k    PMF        CDF")
for k in range(0, 11):
    print(f"{k:2d}   {dist.pmf(k):.6f}   {dist.cdf(k):.6f}")

# Probability of at least 8 successes
prob_ge8 = 1 - dist.cdf(7)
print(f"\nP(X >= 8): {prob_ge8:.4f}")"""},
{"label": "Poisson distribution — PMF and expected value", "code":
"""import numpy as np
from scipy import stats

lam = 4.5   # average events per interval
dist = stats.poisson(mu=lam)

print(f"Poisson(lambda={lam})")
print(f"Mean: {dist.mean()}, Variance: {dist.var()}")
print()
print("k   PMF")
for k in range(0, 13):
    bar = "#" * int(dist.pmf(k) * 100)
    print(f"{k:2d}  {dist.pmf(k):.5f}  {bar}")

print(f"\nP(X <= 3): {dist.cdf(3):.4f}")
print(f"P(X >= 8): {1 - dist.cdf(7):.4f}")"""},
{"label": "Exponential distribution — survival function", "code":
"""import numpy as np
from scipy import stats

# Scale = mean inter-arrival time (1/rate)
scale = 10.0    # average 10 minutes between events
dist = stats.expon(scale=scale)

print(f"Exponential(mean={scale})")
print(f"Mean: {dist.mean()}, Std: {dist.std():.4f}")
print()
# Survival function P(X > t)
for t in [5, 10, 15, 20, 30]:
    print(f"P(T > {t:2d} min) = {dist.sf(t):.4f}")

# Memoryless property check
p_gt10       = dist.sf(10)
p_gt20_gt10  = dist.sf(20) / dist.sf(10)
print(f"\nP(T>20|T>10) = {p_gt20_gt10:.4f}  (should equal P(T>10) = {p_gt10:.4f})")"""},
],
"rw_scenario": "An e-commerce platform wants to model the number of customer purchases per hour (Poisson) and the time between purchases (Exponential). They also need the normal approximation for total daily revenue and the probability of a marketing campaign achieving at least 50 conversions out of 200 email sends.",
"rw_code":
"""import numpy as np
from scipy import stats

# Poisson: purchases per hour
lam_hourly = 12
pois = stats.poisson(mu=lam_hourly)
print(f"Expected purchases/hour: {pois.mean()}")
print(f"P(>=15 purchases in 1hr): {1 - pois.cdf(14):.4f}")

# Exponential: minutes between purchases
minutes_between = stats.expon(scale=60/lam_hourly)
print(f"\nAvg time between purchases: {minutes_between.mean():.2f} min")
print(f"P(wait > 8 min): {minutes_between.sf(8):.4f}")

# Binomial: email campaign conversions
n_emails, p_conv = 200, 0.27
binom = stats.binom(n=n_emails, p=p_conv)
print(f"\nEmail campaign — n={n_emails}, p={p_conv}")
print(f"Expected conversions: {binom.mean():.1f}")
print(f"P(>=50 conversions): {1 - binom.cdf(49):.4f}")

# Normal: total daily revenue (CLT)
avg_order, std_order, n_orders = 85, 30, 150
rev_dist = stats.norm(loc=avg_order*n_orders, scale=std_order*np.sqrt(n_orders))
print(f"\nP(daily revenue > $14000): {rev_dist.sf(14000):.4f}")
""",
"practice": {
    "title": "Distribution Parameter Fitting",
    "desc": "Given a dataset of customer wait times, fit an exponential distribution using scipy.stats.expon.fit(), compute the fitted mean, and calculate the probability that a customer waits more than 5 minutes. Also compute the 90th percentile wait time.",
    "starter":
"""import numpy as np
from scipy import stats

np.random.seed(42)
# Simulate wait times (minutes) — true mean = 3 min
wait_times = np.random.exponential(scale=3.0, size=500)

# TODO: Fit exponential distribution with stats.expon.fit()
# TODO: Print fitted scale (mean wait time)
# TODO: Compute P(wait > 5 minutes) using fitted distribution
# TODO: Compute 90th percentile wait time
"""
}
},

{
"title": "3. Sampling & Central Limit Theorem",
"desc": "Random sampling draws a subset from a population. The Central Limit Theorem (CLT) states that the distribution of sample means approaches normality as sample size grows, regardless of population shape. Bootstrap resampling estimates sampling distributions empirically.",
"examples": [
{"label": "Simple random sampling with numpy", "code":
"""import numpy as np

np.random.seed(42)
# Skewed population (exponential)
population = np.random.exponential(scale=5, size=10000)

print(f"Population  — mean: {population.mean():.3f}, std: {population.std():.3f}")
print()

# Draw samples of different sizes
for n in [5, 30, 100, 500]:
    sample = np.random.choice(population, size=n, replace=False)
    print(f"n={n:4d} — sample mean: {sample.mean():.3f}, sample std: {sample.std(ddof=1):.3f}")"""},
{"label": "CLT demonstration — sampling distribution of the mean", "code":
"""import numpy as np
from scipy import stats

np.random.seed(0)
# Highly skewed population
population = np.random.exponential(scale=5, size=100000)
pop_mean, pop_std = population.mean(), population.std()

n_simulations = 3000
for n in [5, 10, 30, 100]:
    sample_means = [np.mean(np.random.choice(population, n, replace=False))
                    for _ in range(n_simulations)]
    sm = np.array(sample_means)
    # By CLT, sampling dist should be normal
    w_stat, p_val = stats.shapiro(sm[:200])
    print(f"n={n:3d}: mean of means={sm.mean():.3f}, "
          f"std={sm.std():.3f} (theory={pop_std/np.sqrt(n):.3f}), "
          f"Shapiro p={p_val:.4f}")"""},
{"label": "Bootstrap resampling — estimate sampling distribution", "code":
"""import numpy as np

np.random.seed(7)
sample = np.random.lognormal(mean=2, sigma=0.5, size=50)

n_boot = 5000
boot_means = np.array([
    np.mean(np.random.choice(sample, size=len(sample), replace=True))
    for _ in range(n_boot)
])

print(f"Original sample mean: {sample.mean():.4f}")
print(f"Bootstrap mean:       {boot_means.mean():.4f}")
print(f"Bootstrap std error:  {boot_means.std():.4f}")
print(f"Bootstrap 95% CI:     [{np.percentile(boot_means,2.5):.4f}, {np.percentile(boot_means,97.5):.4f}]")"""},
{"label": "Stratified sampling with pandas", "code":
"""import numpy as np
import pandas as pd

np.random.seed(1)
n = 1000
df = pd.DataFrame({
    "age_group": np.random.choice(["18-34","35-54","55+"], size=n, p=[0.4,0.35,0.25]),
    "score":     np.random.normal(70, 10, n),
})

# Proportional stratified sample (10%)
sample_rate = 0.10
stratified = (df.groupby("age_group", group_keys=False)
                .apply(lambda g: g.sample(frac=sample_rate, random_state=42)))

print("Stratified sample composition:")
print(stratified["age_group"].value_counts())
print(f"\nPop mean:    {df['score'].mean():.3f}")
print(f"Sample mean: {stratified['score'].mean():.3f}")"""},
],
"rw_scenario": "A polling firm surveys likely voters ahead of an election. They use stratified random sampling by region (North, South, East, West) to ensure representation, then apply bootstrap resampling to estimate the margin of error for their candidate preference estimate without assuming normality.",
"rw_code":
"""import numpy as np
import pandas as pd

np.random.seed(42)
true_props = {"North":0.52, "South":0.44, "East":0.55, "West":0.48}
region_sizes = {"North":3000, "South":4500, "East":2000, "West":2500}

# Simulate full voter database
rows = []
for region, size in region_sizes.items():
    votes = np.random.binomial(1, true_props[region], size)
    rows.extend(zip([region]*size, votes))
population = pd.DataFrame(rows, columns=["region","prefer_A"])

# Stratified sample: 100 per region
sample = (population.groupby("region", group_keys=False)
          .apply(lambda g: g.sample(n=100, random_state=42)))

overall_pct = sample["prefer_A"].mean()
print(f"Sample support for A: {overall_pct:.3f}")

# Bootstrap margin of error
n_boot = 4000
boot = [np.random.choice(sample["prefer_A"], size=len(sample), replace=True).mean()
        for _ in range(n_boot)]
boot = np.array(boot)
moe = np.percentile(boot, 97.5) - np.percentile(boot, 2.5)
print(f"Bootstrap 95% CI:     [{np.percentile(boot,2.5):.3f}, {np.percentile(boot,97.5):.3f}]")
print(f"Margin of error:      ±{moe/2:.3f}")
""",
"practice": {
    "title": "Verify CLT with a Uniform Distribution",
    "desc": "Draw 2000 samples of size n from a Uniform(0,1) population. For n in [2, 10, 30, 100], compute the mean of sample means, the empirical standard error, and the theoretical standard error (1/sqrt(12*n)). Show that they converge.",
    "starter":
"""import numpy as np

np.random.seed(99)
n_simulations = 2000
pop_std_uniform = np.sqrt(1/12)   # std of Uniform(0,1)

for n in [2, 10, 30, 100]:
    # TODO: Draw n_simulations samples of size n from Uniform(0,1)
    # TODO: Compute sample means array
    # TODO: Print mean of sample means, empirical SE, theoretical SE
    pass
"""
}
},

{
"title": "4. Confidence Intervals",
"desc": "A confidence interval (CI) gives a range of plausible values for a population parameter. A 95% CI means that if we repeated the study many times, 95% of the intervals would contain the true parameter. scipy.stats provides t-intervals; bootstrap CIs require no distributional assumptions.",
"examples": [
{"label": "CI for mean using scipy.stats.t.interval", "code":
"""import numpy as np
from scipy import stats

np.random.seed(42)
sample = np.random.normal(loc=50, scale=8, size=30)

n    = len(sample)
mean = sample.mean()
se   = stats.sem(sample)         # standard error of mean

# 90%, 95%, 99% confidence intervals
for conf in [0.90, 0.95, 0.99]:
    lo, hi = stats.t.interval(conf, df=n-1, loc=mean, scale=se)
    print(f"{int(conf*100)}% CI: ({lo:.3f}, {hi:.3f})  width={hi-lo:.3f}")"""},
{"label": "CI for proportion using normal approximation", "code":
"""import numpy as np
from scipy import stats

# 143 successes out of 250 trials
successes, n = 143, 250
p_hat = successes / n
se    = np.sqrt(p_hat * (1 - p_hat) / n)

for conf in [0.90, 0.95, 0.99]:
    z  = stats.norm.ppf((1 + conf) / 2)
    lo = p_hat - z * se
    hi = p_hat + z * se
    print(f"{int(conf*100)}% CI for proportion: ({lo:.4f}, {hi:.4f})")

# Wilson score interval (better for extreme p)
from scipy.stats import proportion_confint
lo_w, hi_w = proportion_confint(successes, n, alpha=0.05, method="wilson")
print(f"\nWilson 95% CI: ({lo_w:.4f}, {hi_w:.4f})")"""},
{"label": "Bootstrap CI — percentile and BCA methods", "code":
"""import numpy as np

np.random.seed(0)
data = np.random.lognormal(2, 0.8, size=80)

# Percentile bootstrap CI for the median
n_boot = 5000
boot_medians = np.array([
    np.median(np.random.choice(data, size=len(data), replace=True))
    for _ in range(n_boot)
])

lo_p, hi_p = np.percentile(boot_medians, [2.5, 97.5])
print(f"Sample median:       {np.median(data):.4f}")
print(f"Bootstrap 95% CI:    ({lo_p:.4f}, {hi_p:.4f})")
print(f"Bootstrap std error: {boot_medians.std():.4f}")"""},
{"label": "CI for difference of two means", "code":
"""import numpy as np
from scipy import stats

np.random.seed(5)
group_a = np.random.normal(75, 10, 40)
group_b = np.random.normal(70, 12, 35)

# Welch t-test gives CI for difference in means
t_stat, p_val = stats.ttest_ind(group_a, group_b, equal_var=False)
diff = group_a.mean() - group_b.mean()

# Manual CI for difference
se_diff = np.sqrt(group_a.var(ddof=1)/len(group_a) +
                  group_b.var(ddof=1)/len(group_b))
df = len(group_a) + len(group_b) - 2
lo, hi = diff - stats.t.ppf(0.975, df)*se_diff, diff + stats.t.ppf(0.975, df)*se_diff

print(f"Group A mean: {group_a.mean():.3f}")
print(f"Group B mean: {group_b.mean():.3f}")
print(f"Difference:   {diff:.3f}")
print(f"95% CI for diff: ({lo:.3f}, {hi:.3f})")
print(f"t={t_stat:.3f}, p={p_val:.4f}")"""},
],
"rw_scenario": "A pharmaceutical company runs a clinical trial measuring the reduction in blood pressure after a new drug. They need 95% confidence intervals for the mean reduction, a bootstrap CI that avoids normality assumptions for their small subgroup analysis, and a CI for the proportion of patients achieving >10 mmHg reduction.",
"rw_code":
"""import numpy as np
from scipy import stats
from scipy.stats import proportion_confint

np.random.seed(42)
# Reduction in systolic BP (mmHg) for 45 patients
reduction = np.random.normal(loc=11.5, scale=5.2, size=45)

mean_red = reduction.mean()
se       = stats.sem(reduction)
lo, hi   = stats.t.interval(0.95, df=len(reduction)-1, loc=mean_red, scale=se)
print(f"Mean reduction: {mean_red:.2f} mmHg")
print(f"95% t-CI:       ({lo:.2f}, {hi:.2f}) mmHg")

# Proportion achieving > 10 mmHg reduction
successes = np.sum(reduction > 10)
lo_w, hi_w = proportion_confint(successes, len(reduction), alpha=0.05, method="wilson")
print(f"\nResponders (>10 mmHg): {successes}/{len(reduction)} ({successes/len(reduction):.1%})")
print(f"Wilson 95% CI:         ({lo_w:.3f}, {hi_w:.3f})")

# Bootstrap CI for median reduction (subgroup)
boot_med = np.array([np.median(np.random.choice(reduction, len(reduction), replace=True))
                     for _ in range(4000)])
print(f"\nBootstrap 95% CI (median): ({np.percentile(boot_med,2.5):.2f}, {np.percentile(boot_med,97.5):.2f})")
""",
"practice": {
    "title": "Compare Confidence Intervals",
    "desc": "Generate two samples from Normal(60, 8) with n=20 and n=100. For each, compute the 95% t-CI for the mean. Then generate a skewed sample from Exponential(scale=5) with n=40 and compute both the t-CI and a bootstrap CI. Discuss which is more appropriate.",
    "starter":
"""import numpy as np
from scipy import stats

np.random.seed(77)

# TODO: Sample 1 (n=20) from Normal(60,8) — compute 95% t-CI
# TODO: Sample 2 (n=100) from Normal(60,8) — compute 95% t-CI
# TODO: Sample 3 (n=40) from Exponential(scale=5) — compute both t-CI and bootstrap CI
# TODO: Compare widths and discuss
"""
}
},

{
"title": "5. Hypothesis Testing",
"desc": "Hypothesis testing provides a framework for making statistical decisions. A null hypothesis (H0) is tested against an alternative. The p-value is the probability of observing data at least as extreme as the sample if H0 is true. scipy.stats provides t-tests, with significance typically judged at alpha=0.05.",
"examples": [
{"label": "One-sample t-test", "code":
"""import numpy as np
from scipy import stats

np.random.seed(42)
# H0: population mean = 100; H1: mean != 100
sample = np.random.normal(loc=103, scale=12, size=35)

t_stat, p_val = stats.ttest_1samp(sample, popmean=100)

print(f"Sample mean: {sample.mean():.4f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value:     {p_val:.4f}")
print()
alpha = 0.05
conclusion = "Reject H0" if p_val < alpha else "Fail to reject H0"
print(f"At alpha={alpha}: {conclusion}")
print(f"Evidence that mean != 100: {'Yes' if p_val < alpha else 'No'}")"""},
{"label": "Independent samples (two-sample) t-test", "code":
"""import numpy as np
from scipy import stats

np.random.seed(7)
control   = np.random.normal(50, 8, 40)
treatment = np.random.normal(55, 9, 38)

# Levene test for equal variances
lev_stat, lev_p = stats.levene(control, treatment)
equal_var = lev_p > 0.05

t_stat, p_val = stats.ttest_ind(control, treatment, equal_var=equal_var)

print(f"Control:   n={len(control)}, mean={control.mean():.3f}, std={control.std(ddof=1):.3f}")
print(f"Treatment: n={len(treatment)}, mean={treatment.mean():.3f}, std={treatment.std(ddof=1):.3f}")
print(f"\nLevene p={lev_p:.4f} → equal_var={equal_var}")
print(f"t={t_stat:.4f}, p={p_val:.4f}")
print(f"Result: {'Significant difference' if p_val < 0.05 else 'No significant difference'}")"""},
{"label": "Paired t-test — before vs after", "code":
"""import numpy as np
from scipy import stats

np.random.seed(3)
n = 25
before = np.random.normal(130, 10, n)
after  = before - np.random.normal(8, 5, n)   # intervention reduces by ~8

t_stat, p_val = stats.ttest_rel(before, after)
diff = before - after

print(f"Before: {before.mean():.2f} ± {before.std(ddof=1):.2f}")
print(f"After:  {after.mean():.2f} ± {after.std(ddof=1):.2f}")
print(f"Mean diff: {diff.mean():.2f} ± {diff.std(ddof=1):.2f}")
print(f"\nt={t_stat:.4f}, p={p_val:.6f}")
print(f"One-tailed p (before > after): {p_val/2:.6f}")"""},
{"label": "Type I and II errors — power calculation", "code":
"""import numpy as np
from scipy import stats

# Simulate Type I error rate (false positives under H0)
np.random.seed(0)
alpha = 0.05
n_simulations = 10000
n_per_group = 30

# Under H0: both groups have same mean
false_positives = 0
for _ in range(n_simulations):
    g1 = np.random.normal(50, 10, n_per_group)
    g2 = np.random.normal(50, 10, n_per_group)
    _, p = stats.ttest_ind(g1, g2)
    if p < alpha:
        false_positives += 1

print(f"Simulated Type I error rate: {false_positives/n_simulations:.4f} (expected ~{alpha})")

# Under H1: real effect of size 0.5 SD
true_positives = 0
for _ in range(n_simulations):
    g1 = np.random.normal(50, 10, n_per_group)
    g2 = np.random.normal(55, 10, n_per_group)
    _, p = stats.ttest_ind(g1, g2)
    if p < alpha:
        true_positives += 1
print(f"Simulated Power:             {true_positives/n_simulations:.4f}")"""},
],
"rw_scenario": "An online retailer A/B tests a redesigned checkout page. Conversion rates (number of sales per session) are measured for control (old page) and treatment (new page) groups. The team runs an independent t-test on session revenue values, checks assumptions with Levene's test, and interprets the p-value against their pre-specified alpha of 0.05.",
"rw_code":
"""import numpy as np
from scipy import stats

np.random.seed(42)
# Simulate session revenues (in $) for each group
n_ctrl, n_trt = 500, 500
control   = np.random.lognormal(mean=3.5, sigma=1.2, size=n_ctrl)
treatment = np.random.lognormal(mean=3.65, sigma=1.2, size=n_trt)

print("=== A/B Test: Checkout Page Revenue ===")
print(f"Control:   n={n_ctrl}, mean=${control.mean():.2f}, median=${np.median(control):.2f}")
print(f"Treatment: n={n_trt}, mean=${treatment.mean():.2f}, median=${np.median(treatment):.2f}")

# Variance equality
lev_stat, lev_p = stats.levene(control, treatment)
print(f"\nLevene test: F={lev_stat:.3f}, p={lev_p:.4f}")
equal_var = lev_p > 0.05

# Welch t-test
t_stat, p_val = stats.ttest_ind(control, treatment, equal_var=equal_var)
print(f"Welch t-test: t={t_stat:.3f}, p={p_val:.4f}")
print(f"Decision (alpha=0.05): {'Reject H0 — new page works' if p_val < 0.05 else 'Fail to reject H0'}")

uplift = (treatment.mean() - control.mean()) / control.mean() * 100
print(f"Revenue uplift: {uplift:.1f}%")
""",
"practice": {
    "title": "One-Sample and Two-Sample Tests",
    "desc": "A company claims their delivery time averages 3 days. You sample 40 recent deliveries. Run a one-sample t-test to check the claim. Then compare morning vs afternoon delivery times using an independent t-test. Report t-statistic, p-value, and conclusion at alpha=0.05.",
    "starter":
"""import numpy as np
from scipy import stats

np.random.seed(11)
deliveries = np.random.normal(loc=3.4, scale=0.8, size=40)
morning    = np.random.normal(loc=3.2, scale=0.7, size=25)
afternoon  = np.random.normal(loc=3.6, scale=0.9, size=25)

# TODO: One-sample t-test: H0: mean = 3.0 days
# TODO: Two-sample t-test: morning vs afternoon
# TODO: Print t, p, and conclusion for each
"""
}
},

{
"title": "6. ANOVA & Multiple Groups",
"desc": "ANOVA (Analysis of Variance) tests whether means differ across three or more groups simultaneously, avoiding inflated Type I errors from multiple pairwise t-tests. One-way ANOVA requires normality and equal variances; Kruskal-Wallis is the non-parametric alternative. Post-hoc tests identify which specific pairs differ.",
"examples": [
{"label": "One-way ANOVA with scipy.stats.f_oneway", "code":
"""import numpy as np
from scipy import stats

np.random.seed(42)
group_a = np.random.normal(20, 4, 30)
group_b = np.random.normal(24, 4, 30)
group_c = np.random.normal(22, 4, 30)
group_d = np.random.normal(20, 4, 30)

f_stat, p_val = stats.f_oneway(group_a, group_b, group_c, group_d)

for name, grp in zip("ABCD", [group_a,group_b,group_c,group_d]):
    print(f"Group {name}: mean={grp.mean():.3f}, std={grp.std(ddof=1):.3f}")

print(f"\nF-statistic: {f_stat:.4f}")
print(f"p-value:     {p_val:.4f}")
print(f"Result: {'Significant difference between groups' if p_val < 0.05 else 'No significant difference'}")"""},
{"label": "ANOVA assumptions — Levene and Shapiro-Wilk", "code":
"""import numpy as np
from scipy import stats

np.random.seed(0)
g1 = np.random.normal(10, 2, 25)
g2 = np.random.normal(12, 3, 25)
g3 = np.random.normal(11, 2, 25)

# Homogeneity of variance
lev_stat, lev_p = stats.levene(g1, g2, g3)
print(f"Levene test: F={lev_stat:.3f}, p={lev_p:.4f}")
print(f"  Equal variances assumed: {lev_p > 0.05}")

# Normality within each group
for i, g in enumerate([g1,g2,g3],1):
    w, p = stats.shapiro(g)
    print(f"Shapiro-Wilk Group {i}: W={w:.4f}, p={p:.4f} — {'Normal' if p>0.05 else 'Non-normal'}")"""},
{"label": "Kruskal-Wallis — non-parametric ANOVA", "code":
"""import numpy as np
from scipy import stats

np.random.seed(5)
# Skewed groups — ANOVA assumptions violated
g1 = np.random.exponential(2, 30)
g2 = np.random.exponential(3, 30)
g3 = np.random.exponential(2.5, 30)

kw_stat, kw_p = stats.kruskal(g1, g2, g3)
f_stat, f_p   = stats.f_oneway(g1, g2, g3)

print("Group medians:")
for i, g in enumerate([g1,g2,g3],1):
    print(f"  Group {i}: median={np.median(g):.3f}")

print(f"\nKruskal-Wallis: H={kw_stat:.4f}, p={kw_p:.4f}")
print(f"One-way ANOVA:  F={f_stat:.4f}, p={f_p:.4f}")"""},
{"label": "Post-hoc pairwise tests with Bonferroni correction", "code":
"""import numpy as np
from scipy import stats
from itertools import combinations

np.random.seed(9)
groups = {
    "Control":   np.random.normal(50, 8, 30),
    "Drug A":    np.random.normal(58, 8, 30),
    "Drug B":    np.random.normal(55, 8, 30),
    "Placebo":   np.random.normal(51, 8, 30),
}

f_stat, p_val = stats.f_oneway(*groups.values())
print(f"ANOVA: F={f_stat:.3f}, p={p_val:.4f}")

# Pairwise t-tests with Bonferroni correction
names = list(groups.keys())
pairs = list(combinations(names, 2))
alpha_corr = 0.05 / len(pairs)   # Bonferroni

print(f"\nBonferroni alpha: {alpha_corr:.4f} ({len(pairs)} comparisons)")
for n1, n2 in pairs:
    t, p = stats.ttest_ind(groups[n1], groups[n2])
    sig  = "*" if p < alpha_corr else ""
    print(f"  {n1} vs {n2}: p={p:.4f} {sig}")"""},
],
"rw_scenario": "A nutrition researcher compares weight loss across four diets (Mediterranean, Keto, Vegan, Low-Fat) over 12 weeks. One-way ANOVA tests whether any diet differs. Levene's test checks variance equality. Post-hoc pairwise tests with Bonferroni correction identify which specific diets differ significantly.",
"rw_code":
"""import numpy as np
from scipy import stats
from itertools import combinations

np.random.seed(42)
diets = {
    "Mediterranean": np.random.normal(5.2, 2.1, 35),
    "Keto":          np.random.normal(7.1, 2.5, 35),
    "Vegan":         np.random.normal(4.8, 1.9, 35),
    "Low-Fat":       np.random.normal(4.1, 2.0, 35),
}

print("=== Diet Weight Loss Study (kg) ===")
for diet, vals in diets.items():
    print(f"{diet:15s}: mean={vals.mean():.2f}, std={vals.std(ddof=1):.2f}")

f_stat, p_val = stats.f_oneway(*diets.values())
print(f"\nANOVA: F={f_stat:.3f}, p={p_val:.4f}")

if p_val < 0.05:
    print("Significant — running post-hoc tests")
    names = list(diets.keys())
    pairs = list(combinations(names, 2))
    bonf  = 0.05 / len(pairs)
    print(f"Bonferroni alpha: {bonf:.4f}")
    for n1, n2 in pairs:
        _, p = stats.ttest_ind(diets[n1], diets[n2])
        print(f"  {n1:15s} vs {n2:15s}: p={p:.4f} {'*' if p<bonf else ''}")
""",
"practice": {
    "title": "Compare Three Teaching Methods",
    "desc": "Simulate exam scores for students taught by three methods: Lecture (mean=72), Active Learning (mean=78), Online (mean=74), each with std=10 and n=30. Run one-way ANOVA. If significant, apply Bonferroni-corrected pairwise t-tests. Also run Kruskal-Wallis as a robustness check.",
    "starter":
"""import numpy as np
from scipy import stats
from itertools import combinations

np.random.seed(55)
lecture = np.random.normal(72, 10, 30)
active  = np.random.normal(78, 10, 30)
online  = np.random.normal(74, 10, 30)

# TODO: One-way ANOVA
# TODO: If significant, Bonferroni post-hoc
# TODO: Kruskal-Wallis test
# TODO: Compare ANOVA vs Kruskal-Wallis conclusions
"""
}
},

{
"title": "7. Chi-Square Tests",
"desc": "Chi-square tests assess relationships between categorical variables. The goodness-of-fit test checks if observed frequencies match expected. The test of independence checks if two categorical variables are related. scipy.stats.chi2_contingency handles contingency tables directly.",
"examples": [
{"label": "Chi-square goodness-of-fit test", "code":
"""import numpy as np
from scipy import stats

# Test if a die is fair (expected: equal frequency for each face)
observed = np.array([48, 55, 52, 60, 45, 40])   # 300 rolls
expected_freq = 300 / 6
expected = np.full(6, expected_freq)

chi2, p_val = stats.chisquare(f_obs=observed, f_exp=expected)
df = len(observed) - 1

print("Die Roll Test (300 rolls)")
print(f"Observed: {observed}")
print(f"Expected: {expected}")
print(f"\nChi2 statistic: {chi2:.4f}")
print(f"Degrees of freedom: {df}")
print(f"p-value: {p_val:.4f}")
print(f"Die is {'NOT fair' if p_val < 0.05 else 'fair (fail to reject H0)'}")"""},
{"label": "Chi-square test of independence — contingency table", "code":
"""import numpy as np
from scipy import stats
import pandas as pd

# Customer satisfaction by region
data = {
    "Satisfied":   {"North": 120, "South": 85, "East": 95, "West": 110},
    "Neutral":     {"North":  40, "South": 35, "East": 42, "West":  38},
    "Unsatisfied": {"North":  20, "South": 30, "East": 23, "West":  22},
}
table = pd.DataFrame(data).T
print("Contingency Table:")
print(table)

chi2, p_val, dof, expected = stats.chi2_contingency(table)
print(f"\nChi2={chi2:.4f}, df={dof}, p={p_val:.4f}")
print(f"Satisfaction independent of region: {p_val > 0.05}")"""},
{"label": "Cramer's V — effect size for chi-square", "code":
"""import numpy as np
from scipy import stats

# 2x2 contingency: Gender vs. Purchase
table = np.array([[230, 170],   # Male:   bought, did not buy
                  [195, 205]])  # Female: bought, did not buy

chi2, p_val, dof, expected = stats.chi2_contingency(table)
n = table.sum()
k = min(table.shape) - 1

cramers_v = np.sqrt(chi2 / (n * k))
print(f"Chi2={chi2:.4f}, df={dof}, p={p_val:.4f}")
print(f"n={n}, Cramer's V={cramers_v:.4f}")
print(f"Effect size: {'small' if cramers_v < 0.1 else 'medium' if cramers_v < 0.3 else 'large'}")"""},
{"label": "Expected frequency check and Fisher's exact test", "code":
"""import numpy as np
from scipy import stats

# Small sample — use Fisher's exact test
# Rare disease by treatment
table = np.array([[5, 15],
                  [2, 18]])

chi2, p_chi, dof, expected = stats.chi2_contingency(table)
oddsratio, p_fisher = stats.fisher_exact(table)

print("Observed:")
print(table)
print(f"\nExpected frequencies:")
print(expected.round(2))
print(f"\nChi2 p-value:   {p_chi:.4f}  (valid if all expected >= 5)")
print(f"Fisher p-value: {p_fisher:.4f}  (preferred for small samples)")
print(f"Odds ratio:     {oddsratio:.4f}")"""},
],
"rw_scenario": "A market research firm surveys 800 shoppers about their preferred payment method (Cash, Card, Mobile) segmented by age group (18-34, 35-54, 55+). They run a chi-square test of independence to determine if payment preference is associated with age, then compute Cramer's V to quantify the strength of association.",
"rw_code":
"""import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(42)
# Contingency table: age group vs payment method
table = np.array([
    [45, 130, 125],   # 18-34: Cash, Card, Mobile
    [80, 155,  65],   # 35-54
    [95, 120,  25],   # 55+
])
row_labels = ["18-34", "35-54", "55+"]
col_labels  = ["Cash", "Card", "Mobile"]

df_table = pd.DataFrame(table, index=row_labels, columns=col_labels)
print("Payment Method by Age Group:")
print(df_table)
print(f"\nRow totals: {df_table.sum(axis=1).values}")

chi2, p_val, dof, expected = stats.chi2_contingency(table)
n = table.sum()
cramers_v = np.sqrt(chi2 / (n * (min(table.shape)-1)))

print(f"\nChi2={chi2:.3f}, df={dof}, p={p_val:.4f}")
print(f"Cramer's V = {cramers_v:.4f} ({'small' if cramers_v<0.1 else 'medium' if cramers_v<0.3 else 'large'} effect)")
print(f"Association between age and payment method: {'Yes' if p_val<0.05 else 'No'}")
""",
"practice": {
    "title": "A/B Test with Chi-Square",
    "desc": "An A/B test shows 180 conversions out of 900 visitors (control) and 210 conversions out of 900 visitors (treatment). Build a 2x2 contingency table and run a chi-square test of independence to determine if the conversion rate differs significantly. Compute Cramer's V.",
    "starter":
"""import numpy as np
from scipy import stats

# Control:   180 converted, 720 did not
# Treatment: 210 converted, 690 did not
table = np.array([
    [180, 720],
    [210, 690],
])

# TODO: Run chi2_contingency
# TODO: Compute and interpret Cramer's V
# TODO: Also run Fisher's exact as a check
"""
}
},

{
"title": "8. Correlation & Regression",
"desc": "Correlation measures the linear (Pearson) or monotonic (Spearman) relationship between two variables, ranging from -1 to +1. Simple linear regression models one variable as a linear function of another. scipy.stats.linregress provides slope, intercept, r-value, and p-value for the slope.",
"examples": [
{"label": "Pearson and Spearman correlation", "code":
"""import numpy as np
from scipy import stats

np.random.seed(42)
x = np.random.uniform(0, 10, 50)
y = 2.5 * x + np.random.normal(0, 3, 50)   # linear + noise

pearson_r,  pearson_p  = stats.pearsonr(x, y)
spearman_r, spearman_p = stats.spearmanr(x, y)

print(f"Pearson r:  {pearson_r:.4f}  (p={pearson_p:.4f})")
print(f"Spearman r: {spearman_r:.4f}  (p={spearman_p:.4f})")

# Correlation matrix with pandas
import pandas as pd
df = pd.DataFrame({"x":x, "y":y, "z": y**0.5})
print("\nCorrelation matrix:")
print(df.corr(method="pearson").round(4))"""},
{"label": "Simple linear regression with scipy.stats.linregress", "code":
"""import numpy as np
from scipy import stats

np.random.seed(0)
hours_studied = np.random.uniform(1, 10, 60)
exam_score    = 50 + 4.5 * hours_studied + np.random.normal(0, 5, 60)

result = stats.linregress(hours_studied, exam_score)

print(f"slope:     {result.slope:.4f}")
print(f"intercept: {result.intercept:.4f}")
print(f"r-value:   {result.rvalue:.4f}")
print(f"r-squared: {result.rvalue**2:.4f}")
print(f"p-value:   {result.pvalue:.6f}")
print(f"std error: {result.stderr:.4f}")

# Prediction
pred_8hrs = result.slope * 8 + result.intercept
print(f"\nPredicted score for 8 hrs: {pred_8hrs:.2f}")"""},
{"label": "Multiple correlation using numpy polyfit", "code":
"""import numpy as np
from scipy import stats

np.random.seed(3)
x = np.linspace(0, 10, 80)
y = 3 + 2*x - 0.15*x**2 + np.random.normal(0, 2, 80)

# Linear fit
coef1 = np.polyfit(x, y, 1)
y_hat1 = np.polyval(coef1, x)
ss_res1 = np.sum((y - y_hat1)**2)
ss_tot  = np.sum((y - y.mean())**2)
r2_lin  = 1 - ss_res1/ss_tot

# Quadratic fit
coef2 = np.polyfit(x, y, 2)
y_hat2 = np.polyval(coef2, x)
ss_res2 = np.sum((y - y_hat2)**2)
r2_quad = 1 - ss_res2/ss_tot

print(f"Linear fit:    R² = {r2_lin:.4f}")
print(f"Quadratic fit: R² = {r2_quad:.4f}")
print(f"Quadratic coefficients: {coef2.round(4)}")"""},
{"label": "Residuals analysis and influential points", "code":
"""import numpy as np
from scipy import stats

np.random.seed(1)
x = np.random.uniform(0, 20, 50)
y = 5 + 1.8 * x + np.random.normal(0, 4, 50)

result = stats.linregress(x, y)
y_pred = result.slope * x + result.intercept
residuals = y - y_pred

# Standardized residuals
std_res = (residuals - residuals.mean()) / residuals.std(ddof=1)
outlier_mask = np.abs(std_res) > 2

print(f"n={len(x)}, R²={result.rvalue**2:.4f}")
print(f"Residual std: {residuals.std(ddof=1):.4f}")
print(f"Outliers (|std resid|>2): {outlier_mask.sum()}")
print(f"Expected outliers ~5%: {int(0.05*len(x))}")

# Durbin-Watson statistic (autocorrelation in residuals)
diffs = np.diff(residuals)
dw = np.sum(diffs**2) / np.sum(residuals**2)
print(f"Durbin-Watson: {dw:.4f}  (2=no autocorr, <2=positive, >2=negative)")"""},
],
"rw_scenario": "A real estate company models house prices using square footage. They compute Pearson correlation, fit a simple linear regression with scipy.stats.linregress, assess R-squared, and analyze residuals to check for linearity and homoscedasticity. They also identify outlier properties that deviate from the trend.",
"rw_code":
"""import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(42)
# Simulate house data
sqft  = np.random.uniform(800, 3500, 150)
price = 50000 + 180 * sqft + np.random.normal(0, 25000, 150)
# Add a few luxury outliers
price[:5] += 200000

df = pd.DataFrame({"sqft": sqft, "price": price})

pearson_r, pearson_p = stats.pearsonr(df["sqft"], df["price"])
print(f"Pearson r = {pearson_r:.4f} (p={pearson_p:.2e})")

result = stats.linregress(df["sqft"], df["price"])
print(f"\nRegression: price = {result.slope:.2f} * sqft + {result.intercept:,.0f}")
print(f"R² = {result.rvalue**2:.4f}")

# Predict 2000 sqft house
pred = result.slope * 2000 + result.intercept
print(f"Predicted price (2000 sqft): ${pred:,.0f}")

# Residual analysis
residuals = df["price"] - (result.slope * df["sqft"] + result.intercept)
std_res = (residuals - residuals.mean()) / residuals.std(ddof=1)
print(f"\nOutlier properties (|std resid|>2.5): {(np.abs(std_res)>2.5).sum()}")
""",
"practice": {
    "title": "Advertising Spend vs Sales Regression",
    "desc": "Given weekly advertising spend (x) ranging from $1000 to $10000 and weekly sales (y), fit a linear regression. Compute slope, intercept, R-squared, and predict sales for a $7500 spend. Compute both Pearson and Spearman correlations and compare them.",
    "starter":
"""import numpy as np
from scipy import stats

np.random.seed(88)
ad_spend = np.random.uniform(1000, 10000, 52)   # weekly ad spend
sales    = 2000 + 3.5 * ad_spend + np.random.normal(0, 3000, 52)

# TODO: Compute Pearson and Spearman correlations
# TODO: Fit linear regression with scipy.stats.linregress
# TODO: Print slope, intercept, R²
# TODO: Predict sales for $7500 ad spend
"""
}
},

{
"title": "9. Non-Parametric Tests",
"desc": "Non-parametric tests make no assumptions about the underlying distribution. They operate on ranks rather than raw values, making them robust to outliers and skewed data. Key tests include Mann-Whitney U (two independent groups), Wilcoxon signed-rank (paired), and Shapiro-Wilk (normality check).",
"examples": [
{"label": "Shapiro-Wilk normality test", "code":
"""import numpy as np
from scipy import stats

np.random.seed(42)
normal_data = np.random.normal(50, 10, 50)
skewed_data = np.random.exponential(scale=5, size=50)
uniform_data = np.random.uniform(0, 100, 50)

print("Shapiro-Wilk Normality Test")
print(f"{'Dataset':<15} {'W-stat':>8} {'p-value':>9} {'Normal?':>8}")
for name, data in [("Normal", normal_data), ("Exponential", skewed_data), ("Uniform", uniform_data)]:
    w, p = stats.shapiro(data)
    print(f"{name:<15} {w:>8.4f} {p:>9.4f} {str(p>0.05):>8}")"""},
{"label": "Mann-Whitney U test — two independent samples", "code":
"""import numpy as np
from scipy import stats

np.random.seed(7)
# Skewed distributions — t-test assumptions violated
group1 = np.random.exponential(scale=3, size=35)
group2 = np.random.exponential(scale=4, size=38)

# Parametric (t-test)
t_stat, t_p = stats.ttest_ind(group1, group2)
# Non-parametric
u_stat, mw_p = stats.mannwhitneyu(group1, group2, alternative="two-sided")

print(f"Group 1: median={np.median(group1):.3f}, mean={group1.mean():.3f}")
print(f"Group 2: median={np.median(group2):.3f}, mean={group2.mean():.3f}")
print(f"\nWelch t-test:     t={t_stat:.3f}, p={t_p:.4f}")
print(f"Mann-Whitney U:   U={u_stat:.1f},  p={mw_p:.4f}")

# Rank-biserial correlation (effect size)
r_rb = 1 - (2*u_stat) / (len(group1)*len(group2))
print(f"Rank-biserial r:  {r_rb:.4f}")"""},
{"label": "Wilcoxon signed-rank test — paired samples", "code":
"""import numpy as np
from scipy import stats

np.random.seed(3)
n = 30
before = np.random.exponential(scale=8, size=n)
after  = before * np.random.uniform(0.6, 0.95, n)   # improvement

# Parametric paired t-test
t_stat, t_p = stats.ttest_rel(before, after)
# Non-parametric
w_stat, w_p = stats.wilcoxon(before, after)

print(f"Before: median={np.median(before):.3f}")
print(f"After:  median={np.median(after):.3f}")
print(f"\nPaired t-test:          t={t_stat:.3f}, p={t_p:.4f}")
print(f"Wilcoxon signed-rank:   W={w_stat:.1f},  p={w_p:.4f}")"""},
{"label": "Kolmogorov-Smirnov and Anderson-Darling tests", "code":
"""import numpy as np
from scipy import stats

np.random.seed(0)
data = np.random.normal(5, 2, 100)

# KS test: compare to normal distribution
ks_stat, ks_p = stats.kstest(data, "norm", args=(data.mean(), data.std()))
print(f"K-S test vs Normal:  D={ks_stat:.4f}, p={ks_p:.4f}")

# Anderson-Darling test
ad_result = stats.anderson(data, dist="norm")
print(f"\nAnderson-Darling: statistic={ad_result.statistic:.4f}")
for sl, cv in zip(ad_result.significance_level, ad_result.critical_values):
    reject = ad_result.statistic > cv
    print(f"  alpha={sl:5.1f}%: critical={cv:.3f}, reject H0={reject}")

# Two-sample KS test
data2 = np.random.normal(5.5, 2, 100)
ks2_stat, ks2_p = stats.ks_2samp(data, data2)
print(f"\nTwo-sample KS test: D={ks2_stat:.4f}, p={ks2_p:.4f}")"""},
],
"rw_scenario": "A clinical researcher compares pain scores (highly skewed, 0-10 scale) before and after a new pain management protocol using the Wilcoxon signed-rank test. They also compare pain scores between two patient cohorts using Mann-Whitney U. Shapiro-Wilk normality tests confirm non-parametric methods are appropriate.",
"rw_code":
"""import numpy as np
from scipy import stats

np.random.seed(42)
n = 40
# Pain scores (0-10, skewed toward lower end)
before = np.random.beta(a=2, b=1.5, size=n) * 10
after  = before * np.random.uniform(0.4, 0.85, n)

# Normality check
wb, pb = stats.shapiro(before)
wa, pa = stats.shapiro(after)
print("Shapiro-Wilk normality test:")
print(f"  Before: W={wb:.4f}, p={pb:.4f} — {'Normal' if pb>0.05 else 'Non-normal'}")
print(f"  After:  W={wa:.4f}, p={pa:.4f} — {'Normal' if pa>0.05 else 'Non-normal'}")

# Wilcoxon signed-rank (paired, non-parametric)
w_stat, w_p = stats.wilcoxon(before, after)
print(f"\nWilcoxon signed-rank: W={w_stat:.1f}, p={w_p:.4f}")
print(f"Median reduction: {np.median(before-after):.2f} points")

# Independent cohort comparison
cohort_a = np.random.beta(2, 1.5, 40) * 10
cohort_b = np.random.beta(1.5, 2, 40) * 10
u_stat, mw_p = stats.mannwhitneyu(cohort_a, cohort_b, alternative="two-sided")
print(f"\nMann-Whitney U (cohort comparison): U={u_stat:.1f}, p={mw_p:.4f}")
""",
"practice": {
    "title": "Choose Parametric vs Non-Parametric",
    "desc": "Generate three datasets: (A) Normal(50,10) n=40, (B) Exponential(scale=5) n=40, (C) Uniform(0,100) n=40. For each pair, first run Shapiro-Wilk, then decide whether to use t-test or Mann-Whitney U. Run both and compare p-values.",
    "starter":
"""import numpy as np
from scipy import stats

np.random.seed(22)
group_a = np.random.normal(50, 10, 40)
group_b = np.random.exponential(scale=5, size=40)
group_c = np.random.uniform(0, 100, 40)

# TODO: Shapiro-Wilk for each group
# TODO: For A vs B: t-test and Mann-Whitney
# TODO: For A vs C: t-test and Mann-Whitney
# TODO: Discuss which test is appropriate for each pair
"""
}
},

{
"title": "10. Effect Size & Power Analysis",
"desc": "Effect size quantifies the practical significance of a result, independent of sample size. Cohen's d measures standardized mean differences. Statistical power (1 - beta) is the probability of detecting a true effect. Power analysis determines the sample size needed to achieve adequate power (typically 0.80).",
"examples": [
{"label": "Cohen's d — effect size for two groups", "code":
"""import numpy as np
from scipy import stats

np.random.seed(42)
group1 = np.random.normal(50, 10, 100)
group2 = np.random.normal(56, 10, 100)

# Pooled Cohen's d
mean_diff  = group1.mean() - group2.mean()
pooled_std = np.sqrt((group1.var(ddof=1) + group2.var(ddof=1)) / 2)
cohens_d   = abs(mean_diff) / pooled_std

print(f"Group 1 mean: {group1.mean():.3f}")
print(f"Group 2 mean: {group2.mean():.3f}")
print(f"Pooled std:   {pooled_std:.3f}")
print(f"Cohen's d:    {cohens_d:.4f}")

magnitude = ("small" if cohens_d < 0.2 else
             "small-medium" if cohens_d < 0.5 else
             "medium" if cohens_d < 0.8 else "large")
print(f"Effect size:  {magnitude}")

_, p_val = stats.ttest_ind(group1, group2)
print(f"p-value:      {p_val:.4f}")"""},
{"label": "Power analysis for one-sample t-test with statsmodels", "code":
"""from statsmodels.stats.power import TTestPower

analysis = TTestPower()

# Given: effect size d=0.5, alpha=0.05, power=0.80
n_needed = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.80, alternative="two-sided")
print(f"Sample size for d=0.5, power=0.80: n = {n_needed:.1f} → {int(np.ceil(n_needed))}")

# Power curve: how does power change with n?
import numpy as np
print("\nPower by sample size (d=0.5, alpha=0.05):")
for n in [10, 20, 30, 50, 80, 100, 150, 200]:
    pwr = analysis.solve_power(effect_size=0.5, nobs=n, alpha=0.05, alternative="two-sided")
    bar = "#" * int(pwr * 20)
    print(f"  n={n:4d}: power={pwr:.3f}  {bar}")"""},
{"label": "Power analysis for two-sample t-test", "code":
"""import numpy as np
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

# Sample sizes for various effect sizes
print("Required n per group (alpha=0.05, power=0.80):")
for d in [0.2, 0.3, 0.5, 0.8, 1.0, 1.5]:
    n = analysis.solve_power(effect_size=d, alpha=0.05, power=0.80, alternative="two-sided")
    print(f"  d={d}: n = {int(np.ceil(n))} per group  (total={int(np.ceil(n))*2})")

# How much power do we have with n=30 per group?
print("\nPower with n=30 per group (alpha=0.05):")
for d in [0.2, 0.5, 0.8]:
    pwr = analysis.solve_power(effect_size=d, nobs1=30, alpha=0.05, alternative="two-sided")
    print(f"  d={d}: power={pwr:.4f}")"""},
{"label": "Empirical power via simulation", "code":
"""import numpy as np
from scipy import stats

np.random.seed(0)
n_sim   = 5000
alpha   = 0.05
n       = 40
effect  = 0.5   # Cohen's d

# Empirical power
rejections = 0
for _ in range(n_sim):
    g1 = np.random.normal(0, 1, n)
    g2 = np.random.normal(effect, 1, n)
    _, p = stats.ttest_ind(g1, g2)
    if p < alpha:
        rejections += 1

emp_power = rejections / n_sim

# Analytical power for comparison
from statsmodels.stats.power import TTestIndPower
analytical = TTestIndPower().solve_power(effect_size=effect, nobs1=n, alpha=alpha)

print(f"n={n} per group, d={effect}, alpha={alpha}")
print(f"Empirical power:   {emp_power:.4f}")
print(f"Analytical power:  {analytical:.4f}")
print(f"Type II error (β): {1-emp_power:.4f}")"""},
],
"rw_scenario": "A product team plans an A/B test for a new onboarding flow. They estimate the current conversion rate maps to a Cohen's d of 0.35 for time-to-first-purchase. Using statsmodels TTestIndPower, they calculate the minimum sample size needed to achieve 80% power at alpha=0.05, and validate with a simulation study.",
"rw_code":
"""import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower

np.random.seed(42)

# Business context: expected improvement in days-to-purchase
current_mean, new_mean, common_std = 12.0, 10.5, 4.0
effect_d = (current_mean - new_mean) / common_std
print(f"=== A/B Test Power Planning ===")
print(f"Expected effect size (Cohen's d): {effect_d:.4f}")

analysis = TTestIndPower()
n_needed = analysis.solve_power(effect_size=effect_d, alpha=0.05, power=0.80)
print(f"Required n per arm: {int(np.ceil(n_needed))}")
print(f"Total sample size:  {int(np.ceil(n_needed))*2}")

# Simulate the actual experiment
n_actual = int(np.ceil(n_needed))
control   = np.random.normal(current_mean, common_std, n_actual)
treatment = np.random.normal(new_mean,     common_std, n_actual)

t_stat, p_val = stats.ttest_ind(control, treatment)
mean_diff  = control.mean() - treatment.mean()
pooled_std = np.sqrt((control.var(ddof=1) + treatment.var(ddof=1)) / 2)
obs_d      = mean_diff / pooled_std

print(f"\nSimulated experiment results:")
print(f"Observed Cohen's d: {obs_d:.4f}")
print(f"p-value:            {p_val:.4f}")
print(f"Decision: {'Reject H0 — new flow is better' if p_val<0.05 else 'Fail to reject H0'}")
""",
"practice": {
    "title": "Design a Clinical Trial Sample Size",
    "desc": "A new medication is expected to reduce symptom severity by 2 points (scale 0-20) with a pooled standard deviation of 5. Compute Cohen's d. Then use TTestIndPower to find the sample size needed for 80%, 85%, and 90% power at alpha=0.05. Finally, simulate 3000 trials with the recommended n and estimate empirical power.",
    "starter":
"""import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower

expected_diff = 2.0
pooled_std    = 5.0

# TODO: Compute Cohen's d
# TODO: TTestIndPower: find n for power = 0.80, 0.85, 0.90
# TODO: Simulate 3000 trials with n from 80% power calculation
# TODO: Report empirical power
"""
}
},
{
    "title": "11. Bayesian Inference",
    "desc": "Update beliefs with evidence using Bayes' theorem. Compute posterior distributions, credible intervals, and compare Bayesian vs frequentist approaches.",
    "examples": [
        {
            "label": "Bayes' theorem — coin flip posterior",
            "code": "import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\n# Prior: uniform (Beta(1,1)) -> update with 7 heads out of 10 flips\nheads, tails = 7, 3\ntheta = np.linspace(0, 1, 1000)\n\n# Prior: Beta(1,1) = uniform\nalpha_prior, beta_prior = 1, 1\n# Posterior: Beta(alpha+heads, beta+tails)\nalpha_post = alpha_prior + heads\nbeta_post  = beta_prior  + tails\n\nfrom scipy.stats import beta\nprior     = beta.pdf(theta, alpha_prior, beta_prior)\nlikelihood = theta**heads * (1-theta)**tails\nlikelihood /= likelihood.sum()  # normalize\nposterior  = beta.pdf(theta, alpha_post, beta_post)\n\nfig, ax = plt.subplots(figsize=(8, 5))\nax.plot(theta, prior,     label='Prior Beta(1,1)',      linestyle='--')\nax.plot(theta, likelihood*max(posterior)/max(likelihood), label='Likelihood (scaled)')\nax.plot(theta, posterior, label=f'Posterior Beta({alpha_post},{beta_post})', linewidth=2)\nax.axvline(alpha_post/(alpha_post+beta_post), color='red', linestyle=':', label='Posterior mean')\nax.set_xlabel('theta (P(heads))')\nax.set_title(f'Bayesian Update: {heads}H/{tails}T')\nax.legend(); plt.tight_layout()\nplt.savefig('bayesian_coin.png', dpi=80); plt.close()\nprint(f'Posterior mean: {alpha_post/(alpha_post+beta_post):.3f}')\nprint(f'95% credible interval: ({beta.ppf(0.025,alpha_post,beta_post):.3f}, {beta.ppf(0.975,alpha_post,beta_post):.3f})')"
        },
        {
            "label": "Bayesian A/B test with Beta-Binomial",
            "code": "import numpy as np\nfrom scipy.stats import beta\n\n# A: 120 conversions from 1000 visitors\n# B: 140 conversions from 1000 visitors\nnp.random.seed(42)\n\nalpha_a, beta_a = 1 + 120, 1 + 880\nalpha_b, beta_b = 1 + 140, 1 + 860\n\n# Sample from posteriors\nsamples_a = beta.rvs(alpha_a, beta_a, size=100000)\nsamples_b = beta.rvs(alpha_b, beta_b, size=100000)\n\nprob_b_better = (samples_b > samples_a).mean()\nexpected_lift = (samples_b - samples_a).mean()\n\nprint(f'Control A: rate = {120/1000:.1%}')\nprint(f'Variant B: rate = {140/1000:.1%}')\nprint(f'P(B > A):  {prob_b_better:.1%}')\nprint(f'Expected lift: +{expected_lift:.2%}')\nprint(f'95% CI for lift: ({np.percentile(samples_b-samples_a,2.5):.2%}, {np.percentile(samples_b-samples_a,97.5):.2%})')"
        },
        {
            "label": "Conjugate priors for different distributions",
            "code": "import numpy as np\nfrom scipy.stats import beta, gamma, norm\n\nnp.random.seed(42)\n\n# 1. Beta-Binomial: click-through rate estimation\nclicks, views = 45, 200\nalpha, beta_param = 1 + clicks, 1 + (views - clicks)\nprint('CTR posterior:')\nprint(f'  Mean: {alpha/(alpha+beta_param):.3f}')\nprint(f'  95% CI: ({beta.ppf(0.025,alpha,beta_param):.3f}, {beta.ppf(0.975,alpha,beta_param):.3f})')\n\n# 2. Normal-Normal: mean estimation (known variance)\ndata = np.random.normal(5.0, 2.0, 30)  # true mean=5\nprior_mean, prior_var = 0, 10  # weak prior\nlikelihood_var = 4 / len(data)  # sigma^2/n\nposterior_var  = 1 / (1/prior_var + 1/likelihood_var)\nposterior_mean = posterior_var * (prior_mean/prior_var + data.mean()/likelihood_var)\nprint(f'\\nNormal posterior mean: {posterior_mean:.3f} (true=5.0, sample mean={data.mean():.3f})')\n\n# 3. Gamma-Poisson: event rate estimation\nevents_per_day = [3, 5, 2, 4, 6, 3, 4]  # observed counts\nalpha_g, beta_g = 1 + sum(events_per_day), 1 + len(events_per_day)\nprint(f'\\nPoisson rate posterior mean: {alpha_g/beta_g:.3f} events/day')"
        },
        {
            "label": "Markov Chain Monte Carlo (MCMC) concept",
            "code": "import numpy as np\n\nnp.random.seed(42)\n\ndef log_posterior(theta, data, prior_std=2.0):\n    \"\"\"Log posterior for normal likelihood, normal prior.\"\"\"\n    log_prior = -0.5 * (theta / prior_std)**2\n    log_likelihood = -0.5 * np.sum((data - theta)**2)\n    return log_prior + log_likelihood\n\n# Simple Metropolis-Hastings\ndef metropolis(data, n_samples=5000, proposal_std=0.5):\n    samples = []\n    current = 0.0\n    for _ in range(n_samples):\n        proposed = current + np.random.normal(0, proposal_std)\n        log_alpha = log_posterior(proposed, data) - log_posterior(current, data)\n        if np.log(np.random.uniform()) < log_alpha:\n            current = proposed\n        samples.append(current)\n    return np.array(samples[500:])  # burn-in\n\n# True parameter = 3.0\ndata = np.random.normal(3.0, 1.0, 20)\nsamples = metropolis(data)\n\nprint(f'Data mean:        {data.mean():.3f}')\nprint(f'MCMC posterior mean: {samples.mean():.3f}')\nprint(f'MCMC 95% CI: ({np.percentile(samples,2.5):.3f}, {np.percentile(samples,97.5):.3f})')\nprint(f'Acceptance rate: {len(np.unique(samples.round(6)))/len(samples):.1%}')"
        }
    ],
    "rw_scenario": "A marketing team runs an A/B test for 2 weeks. Using a Bayesian Beta-Binomial model, they continuously estimate P(B>A) and stop early once confidence exceeds 95%.",
    "rw_code": "import numpy as np\nfrom scipy.stats import beta\n\nnp.random.seed(42)\n# Simulate daily data: A has 8% true rate, B has 10% true rate\ntrue_a, true_b = 0.08, 0.10\nn_days = 14\ndaily_visitors = 100\n\nalpha_a, beta_a = 1, 1  # uniform prior\nalpha_b, beta_b = 1, 1\n\nprint('Day | Visitors A/B | Conv A/B | P(B>A)')\nprint('-'*50)\nfor day in range(1, n_days+1):\n    conv_a = np.random.binomial(daily_visitors, true_a)\n    conv_b = np.random.binomial(daily_visitors, true_b)\n    alpha_a += conv_a; beta_a += (daily_visitors - conv_a)\n    alpha_b += conv_b; beta_b += (daily_visitors - conv_b)\n    samples = np.random.beta([alpha_a, alpha_b], [beta_a, beta_b], size=(100000, 2))\n    prob_b_better = (samples[:,1] > samples[:,0]).mean()\n    print(f' {day:2d} | {daily_visitors}/{daily_visitors}        | {conv_a:3d}/{conv_b:3d}    | {prob_b_better:.1%}')\n    if prob_b_better > 0.95:\n        print(f'>>> Declare B winner on day {day}! (P(B>A)={prob_b_better:.1%})')\n        break",
    "practice": {
        "title": "Bayesian Conversion Rate",
        "desc": "You observe 30 conversions from 200 visitors. Use a Beta(1,1) prior. Compute the posterior distribution, posterior mean, and 90% credible interval. Compare to the MLE estimate.",
        "starter": "from scipy.stats import beta\nimport numpy as np\n\nconversions = 30\nvisitors = 200\n\n# Prior: Beta(1, 1) = uniform\nalpha_prior, beta_prior = 1, 1\n\n# TODO: compute posterior parameters\n# TODO: compute posterior mean\n# TODO: compute 90% credible interval (5th and 95th percentile)\n# TODO: compute MLE estimate (conversions/visitors)\n# TODO: print comparison"
    }
},
{
    "title": "12. Survival Analysis",
    "desc": "Analyze time-to-event data — customer churn, equipment failure, clinical trials — with Kaplan-Meier curves and the log-rank test.",
    "examples": [
        {
            "label": "Kaplan-Meier survival curve from scratch",
            "code": "import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\n# (duration, event_occurred) — 0 = censored (still alive/active)\ndata = [(5,1),(8,0),(12,1),(14,1),(2,0),(20,1),(7,1),(18,0),(3,1),(25,1),\n        (11,1),(6,0),(15,1),(9,1),(22,0),(4,1),(16,1),(10,0),(13,1),(19,1)]\ntimes = sorted(set(d for d,e in data if e==1))\n\ndef km_estimator(data):\n    n = len(data)\n    at_risk = n\n    S = 1.0\n    result = [(0, 1.0)]\n    for t in sorted(set(d for d,e in data if e==1)):\n        events   = sum(1 for d,e in data if d==t and e==1)\n        censored = sum(1 for d,e in data if d==t and e==0)\n        S *= (1 - events/at_risk)\n        result.append((t, S))\n        at_risk -= (events + censored)\n    return result\n\nkm = km_estimator(data)\ntimes_km, surv_km = zip(*km)\n\nfig, ax = plt.subplots(figsize=(8, 5))\nax.step(times_km, surv_km, where='post', linewidth=2, color='steelblue', label='KM estimate')\nax.axhline(0.5, color='red', linestyle='--', label='Median survival')\nax.set_xlabel('Time'); ax.set_ylabel('Survival Probability')\nax.set_title('Kaplan-Meier Survival Curve'); ax.legend(); ax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.savefig('km_curve.png', dpi=80); plt.close()\nprint('Saved km_curve.png')\nmedian_idx = next(i for i,s in enumerate(surv_km) if s < 0.5)\nprint(f'Median survival: ~{times_km[median_idx]} units')"
        },
        {
            "label": "Customer churn survival analysis",
            "code": "import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nnp.random.seed(42)\nn = 200\n# Simulate customer tenures: plan A churns faster\nplan_a_times = np.random.exponential(8, n//2).clip(0, 24).round(0)\nplan_b_times = np.random.exponential(14, n//2).clip(0, 24).round(0)\nevents_a = (plan_a_times < 24).astype(int)  # 1=churned, 0=still active (censored)\nevents_b = (plan_b_times < 24).astype(int)\n\ndef km_curve(durations, events):\n    n = len(durations)\n    times = sorted(set(durations[events==1]))\n    S, at_risk = 1.0, n\n    curve = [(0, 1.0)]\n    for t in times:\n        d = sum((durations==t) & (events==1))\n        c = sum((durations==t) & (events==0))\n        S *= 1 - d/at_risk\n        curve.append((t, S)); at_risk -= d + c\n    return zip(*curve)\n\nfig, ax = plt.subplots(figsize=(9, 5))\nfor times, surv, label, color in [\n    (*km_curve(plan_a_times, events_a), 'Plan A (basic)', 'tomato'),\n    (*km_curve(plan_b_times, events_b), 'Plan B (premium)', 'steelblue'),\n]:\n    ax.step(list(times), list(surv), where='post', label=label, color=color, linewidth=2)\nax.set_xlabel('Months'); ax.set_ylabel('Retention Rate')\nax.set_title('Customer Retention: Plan A vs Plan B')\nax.legend(); ax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.savefig('churn_survival.png', dpi=80); plt.close()\nprint('Saved churn_survival.png')\nprint(f'Plan A 12-month retention: ~{plan_a_times[plan_a_times>=12].shape[0]/n*2:.0%}')\nprint(f'Plan B 12-month retention: ~{plan_b_times[plan_b_times>=12].shape[0]/n*2:.0%}')"
        },
        {
            "label": "Log-rank test for group comparison",
            "code": "import numpy as np\nfrom scipy.stats import chi2\n\nnp.random.seed(42)\n# Group 1: faster failure (mean=10)\n# Group 2: slower failure (mean=18)\ng1_times  = np.random.exponential(10, 50).clip(0,30)\ng1_events = (g1_times < 30).astype(int)\ng2_times  = np.random.exponential(18, 50).clip(0,30)\ng2_events = (g2_times < 30).astype(int)\n\ndef log_rank_test(t1, e1, t2, e2):\n    all_times = sorted(set(np.concatenate([t1[e1==1], t2[e2==1]])))\n    O1, E1, O2, E2 = 0, 0, 0, 0\n    n1, n2 = len(t1), len(t2)\n    for t in all_times:\n        d1 = ((t1==t) & (e1==1)).sum()\n        d2 = ((t2==t) & (e2==1)).sum()\n        d  = d1 + d2\n        n  = n1 + n2\n        if n > 0:\n            E1 += d * n1 / n\n            E2 += d * n2 / n\n        O1 += d1; O2 += d2\n        n1 -= ((t1<=t) & (e1==1)).sum() + ((t1<=t) & (e1==0)).sum()\n        n2 -= ((t2<=t) & (e2==1)).sum() + ((t2<=t) & (e2==0)).sum()\n        n1 = max(n1, 0); n2 = max(n2, 0)\n    chi2_stat = (O1 - E1)**2 / E1 + (O2 - E2)**2 / E2\n    p_value = 1 - chi2.cdf(chi2_stat, df=1)\n    return chi2_stat, p_value\n\nchi2_stat, p = log_rank_test(g1_times, g1_events, g2_times, g2_events)\nprint(f'Log-rank chi2: {chi2_stat:.3f}')\nprint(f'p-value: {p:.4f}')\nprint(f'Groups differ significantly: {p < 0.05}')"
        },
        {
            "label": "Hazard rate and hazard ratio",
            "code": "import numpy as np\n\nnp.random.seed(42)\n\n# Exponential distribution: constant hazard rate\nlambda_rate = 0.1  # hazard rate\ntime_points = np.arange(1, 21)\nsurvival    = np.exp(-lambda_rate * time_points)\nhazard      = np.full_like(time_points, lambda_rate, dtype=float)\n\nprint('Exponential survival (lambda=0.1):')\nprint(f'  Survival at t=5:  {np.exp(-0.1*5):.3f}')\nprint(f'  Survival at t=10: {np.exp(-0.1*10):.3f}')\nprint(f'  Median survival:  {np.log(2)/0.1:.1f} time units')\n\n# Hazard ratio: how much riskier is group A vs group B?\nlambda_a = 0.15  # higher hazard\nlambda_b = 0.08\nhr = lambda_a / lambda_b\nprint(f'\\nHazard Ratio (A vs B): {hr:.2f}')\nprint(f'Group A is {hr:.1f}x more likely to fail at any time point')\nprint(f'Group A median: {np.log(2)/lambda_a:.1f} | Group B median: {np.log(2)/lambda_b:.1f}')"
        }
    ],
    "rw_scenario": "A SaaS company tracks how long customers stay before canceling. Kaplan-Meier curves compare retention for free-trial vs. direct-purchase cohorts.",
    "rw_code": "import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nnp.random.seed(42)\n# Cohort 1: free trial then convert (longer retention)\n# Cohort 2: direct paid (shorter retention but committed)\ncohorts = {\n    'Free Trial': np.random.exponential(18, 150).clip(0, 36),\n    'Direct Paid': np.random.exponential(12, 100).clip(0, 36),\n}\nevents = {k: (v < 36).astype(int) for k, v in cohorts.items()}\n\ndef km_curve(durations, ev):\n    n = len(durations)\n    times = sorted(set(durations[ev==1]))\n    S, ar = 1.0, n\n    pts = [(0, 1.0)]\n    for t in times:\n        d = ((durations==t) & (ev==1)).sum()\n        c = ((durations==t) & (ev==0)).sum()\n        S *= 1 - d/ar; pts.append((t, S)); ar -= d + c\n    return zip(*pts)\n\nfig, ax = plt.subplots(figsize=(9, 5))\ncolors = ['#2196F3', '#F44336']\nfor (cohort, times_arr), color in zip(cohorts.items(), colors):\n    t_pts, s_pts = km_curve(times_arr, events[cohort])\n    ax.step(list(t_pts), list(s_pts), where='post', label=cohort, color=color, linewidth=2)\n    churned = events[cohort].sum()\n    print(f'{cohort}: n={len(times_arr)}, churned={churned} ({churned/len(times_arr):.0%}), avg tenure={times_arr.mean():.1f} months')\nax.axhline(0.5, color='gray', linestyle='--', linewidth=1)\nax.set_xlabel('Months Since Signup'); ax.set_ylabel('Retention Rate')\nax.set_title('Customer Retention by Acquisition Channel')\nax.legend(); ax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.savefig('retention_cohorts.png', dpi=80); plt.close()\nprint('Saved retention_cohorts.png')",
    "practice": {
        "title": "Equipment Failure Analysis",
        "desc": "Simulate failure times for two machine types (A: exponential mean=100 days, B: exponential mean=150 days, both n=80, max=200 days). Plot KM curves and run a log-rank test.",
        "starter": "import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nnp.random.seed(42)\n# TODO: generate failure times for A (mean=100) and B (mean=150), clip at 200\n# TODO: compute event flags (1 if failed < 200, 0 if censored)\n# TODO: implement km_curve function (or copy from examples)\n# TODO: plot both KM curves on same figure\n# TODO: compute and print log-rank test p-value\n# TODO: save to 'equipment_survival.png'"
    }
},
{
    "title": "13. Resampling & Simulation",
    "desc": "Use bootstrapping, permutation tests, and Monte Carlo simulation to estimate uncertainty and test hypotheses without distributional assumptions.",
    "examples": [
        {
            "label": "Bootstrap confidence intervals",
            "code": "import numpy as np\n\nnp.random.seed(42)\ndata = np.random.exponential(2.0, 50)  # skewed data\nprint(f'Sample mean: {data.mean():.4f}')\n\n# Bootstrap 95% CI for the mean\nn_boot = 10000\nboot_means = np.array([np.random.choice(data, len(data), replace=True).mean()\n                       for _ in range(n_boot)])\n\nci_lower, ci_upper = np.percentile(boot_means, [2.5, 97.5])\nprint(f'Bootstrap 95% CI: ({ci_lower:.4f}, {ci_upper:.4f})')\nprint(f'Bootstrap SE: {boot_means.std():.4f}')\n\n# Compare to normal approximation\nfrom scipy.stats import sem\nnorm_ci = data.mean() + np.array([-1.96, 1.96]) * sem(data)\nprint(f'Normal approx 95% CI: ({norm_ci[0]:.4f}, {norm_ci[1]:.4f})')"
        },
        {
            "label": "Permutation test for group difference",
            "code": "import numpy as np\n\nnp.random.seed(42)\n# Two groups — is the mean difference real or chance?\ngroup_a = np.random.normal(10.0, 3.0, 40)\ngroup_b = np.random.normal(11.5, 3.0, 40)\nobs_diff = group_b.mean() - group_a.mean()\n\ncombined = np.concatenate([group_a, group_b])\nn_a = len(group_a)\nn_perm = 10000\n\nperm_diffs = np.array([\n    np.random.permutation(combined)[:n_a].mean() - np.random.permutation(combined)[:n_a].mean()\n    for _ in range(n_perm)\n])\n\np_value = (np.abs(perm_diffs) >= np.abs(obs_diff)).mean()\nprint(f'Observed difference: {obs_diff:.4f}')\nprint(f'Permutation p-value: {p_value:.4f}')\nprint(f'Significant at 0.05: {p_value < 0.05}')"
        },
        {
            "label": "Monte Carlo simulation — Pi estimation",
            "code": "import numpy as np\n\nnp.random.seed(42)\nn_samples_list = [100, 1000, 10000, 100000, 1000000]\n\nprint(f'True pi: {np.pi:.6f}')\nprint(f\"{'N':>10} {'Pi estimate':>12} {'Error':>10}\")\nfor n in n_samples_list:\n    x, y = np.random.uniform(-1, 1, (2, n))\n    inside = (x**2 + y**2) <= 1.0\n    pi_est = 4 * inside.mean()\n    error = abs(pi_est - np.pi)\n    print(f'{n:>10,} {pi_est:>12.6f} {error:>10.6f}')"
        },
        {
            "label": "Bootstrap for median and other statistics",
            "code": "import numpy as np\n\nnp.random.seed(42)\nwages = np.array([35, 42, 28, 55, 38, 47, 31, 60, 44, 39,\n                  52, 36, 29, 48, 41, 65, 33, 57, 43, 37]) * 1000\n\ndef bootstrap_ci(data, stat_fn, n_boot=10000, ci=95):\n    boot_stats = [stat_fn(np.random.choice(data, len(data), replace=True))\n                  for _ in range(n_boot)]\n    lower = (100 - ci) / 2\n    return np.percentile(boot_stats, [lower, 100-lower])\n\nstats = {\n    'mean':   np.mean,\n    'median': np.median,\n    'std':    np.std,\n    'q75':    lambda x: np.percentile(x, 75),\n}\n\nfor name, fn in stats.items():\n    ci = bootstrap_ci(wages, fn)\n    print(f'{name:6s}: {fn(wages):>8,.0f}  95% CI: (${ci[0]:,.0f}, ${ci[1]:,.0f})')"
        }
    ],
    "rw_scenario": "An analyst needs confidence intervals for the median revenue per user, which is skewed. Bootstrap gives reliable CIs without assuming normality.",
    "rw_code": "import numpy as np\n\nnp.random.seed(42)\n# Simulated revenue per user (heavy-tailed)\nrevenue = np.random.lognormal(mean=3.5, sigma=1.2, size=500)\n\nprint(f'n={len(revenue)}')\nprint(f'Mean:   ${revenue.mean():,.2f}')\nprint(f'Median: ${np.median(revenue):,.2f}')\n\ndef bootstrap_stat(data, stat_fn, n_boot=10000):\n    boots = [stat_fn(np.random.choice(data, len(data), replace=True)) for _ in range(n_boot)]\n    return np.array(boots)\n\nmean_boots   = bootstrap_stat(revenue, np.mean)\nmedian_boots = bootstrap_stat(revenue, np.median)\n\nfor name, boots, obs in [('mean', mean_boots, revenue.mean()), ('median', median_boots, np.median(revenue))]:\n    ci = np.percentile(boots, [2.5, 97.5])\n    print(f'\\n{name.capitalize()} bootstrap:')\n    print(f'  Observed: ${obs:,.2f}')\n    print(f'  95% CI:   (${ci[0]:,.2f}, ${ci[1]:,.2f})')\n    print(f'  SE:       ${boots.std():,.2f}')",
    "practice": {
        "title": "A/B Test with Permutation",
        "desc": "Group A: 50 users, mean session time 4.2 min. Group B: 50 users, mean 4.8 min. Run a permutation test with 10,000 iterations. Report the p-value and whether the difference is significant.",
        "starter": "import numpy as np\n\nnp.random.seed(42)\ngroup_a = np.random.normal(4.2, 1.5, 50)\ngroup_b = np.random.normal(4.8, 1.5, 50)\n\n# TODO: compute observed difference\n# TODO: combine groups, run 10000 permutations\n# TODO: compute permutation p-value (two-tailed)\n# TODO: print results"
    }
},

    {
        "title": "14. Bootstrap Methods & Resampling",
        "examples": [
            {
                "label": "Percentile Bootstrap CI",
                "code": "import numpy as np\nnp.random.seed(42)\ndata = np.random.exponential(scale=2, size=50)\nB = 10000\nboot_means = [np.mean(np.random.choice(data, size=len(data), replace=True)) for _ in range(B)]\nci = np.percentile(boot_means, [2.5, 97.5])\nprint(f\"Sample mean: {np.mean(data):.4f}\")\nprint(f\"Bootstrap 95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]\")"
            },
            {
                "label": "BCa Bootstrap (Bias-Corrected)",
                "code": "import numpy as np\nfrom scipy import stats\nnp.random.seed(7)\ndata = np.random.lognormal(0, 0.5, 80)\nstat_obs = np.median(data)\nB = 5000\nboot_stats = [np.median(np.random.choice(data, size=len(data), replace=True)) for _ in range(B)]\n# Bias correction\nz0 = stats.norm.ppf(np.mean(np.array(boot_stats) < stat_obs))\n# Acceleration (jackknife)\njk = [np.median(np.delete(data, i)) for i in range(len(data))]\njk_mean = np.mean(jk)\na = np.sum((jk_mean - np.array(jk))**3) / (6*np.sum((jk_mean - np.array(jk))**2)**1.5)\nalpha = 0.05\nz_lo = stats.norm.ppf(alpha/2); z_hi = stats.norm.ppf(1 - alpha/2)\np_lo = stats.norm.cdf(z0 + (z0+z_lo)/(1-a*(z0+z_lo)))\np_hi = stats.norm.cdf(z0 + (z0+z_hi)/(1-a*(z0+z_hi)))\nci = np.percentile(boot_stats, [p_lo*100, p_hi*100])\nprint(f\"BCa 95% CI for median: [{ci[0]:.4f}, {ci[1]:.4f}]\")"
            },
            {
                "label": "Bootstrap Hypothesis Test (Permutation)",
                "code": "import numpy as np\nnp.random.seed(0)\ngroup_a = np.random.normal(5.0, 1.5, 40)\ngroup_b = np.random.normal(5.6, 1.5, 40)\nobs_diff = np.mean(group_b) - np.mean(group_a)\ncombined = np.concatenate([group_a, group_b])\nB = 10000\nperm_diffs = []\nfor _ in range(B):\n    perm = np.random.permutation(combined)\n    perm_diffs.append(np.mean(perm[40:]) - np.mean(perm[:40]))\np_value = np.mean(np.abs(perm_diffs) >= np.abs(obs_diff))\nprint(f\"Observed difference: {obs_diff:.4f}\")\nprint(f\"Permutation p-value: {p_value:.4f}\")"
            }
        ],
        "rw_scenario": "E-commerce A/B test: compare conversion rates between checkout designs using bootstrap CIs instead of assuming normality for small samples.",
        "rw_code": "import numpy as np\nnp.random.seed(42)\n# Simulated checkout conversion: design A=0.05, design B=0.065\nn = 300\nconv_a = np.random.binomial(1, 0.05, n).astype(float)\nconv_b = np.random.binomial(1, 0.065, n).astype(float)\nobs_diff = conv_b.mean() - conv_a.mean()\nB = 20000\nboot_diffs = [\n    np.random.choice(conv_b, n, replace=True).mean() -\n    np.random.choice(conv_a, n, replace=True).mean()\n    for _ in range(B)\n]\nci = np.percentile(boot_diffs, [2.5, 97.5])\np_val = np.mean(np.array(boot_diffs) <= 0)\nprint(f\"Observed lift: {obs_diff:.4f} ({obs_diff/conv_a.mean():.1%} relative)\")\nprint(f\"95% Bootstrap CI: [{ci[0]:.4f}, {ci[1]:.4f}]\")\nprint(f\"One-sided p-value: {p_val:.4f}\")\nprint(\"Significant at alpha=0.05:\", ci[0] > 0)",
        "practice": {
            "title": "Bootstrap Customer Lifetime Value",
            "desc": "You have 60 customer LTV values from a heavy-tailed distribution. Compute 90% and 95% percentile bootstrap CIs for the mean and the 75th percentile. Also run a two-sample permutation test comparing \'premium\' vs \'standard\' customers (30 each). Report p-values and effect sizes.",
            "starter": "import numpy as np\nnp.random.seed(11)\nltv = np.random.pareto(2, 60) * 100 + 50\npremium = ltv[:30]\nstandard = ltv[30:]\nB = 10000\n# TODO: Bootstrap 90% and 95% CIs for mean LTV\n# TODO: Bootstrap CI for 75th percentile LTV\n# TODO: Permutation test: premium vs standard mean LTV\n# TODO: Report Cohen\'s d effect size\n"
        }
    },
    {
        "title": "15. Multiple Testing & FDR Control",
        "examples": [
            {
                "label": "Bonferroni & Holm Corrections",
                "code": "import numpy as np\nfrom scipy import stats\nnp.random.seed(42)\nk = 20\n# 18 nulls (no effect) + 2 true positives\np_values = np.concatenate([\n    np.random.uniform(0, 1, 18),\n    np.array([0.003, 0.011])\n])\nalpha = 0.05\nbonferroni = p_values * k\nreject_bon = bonferroni < alpha\n# Holm correction\norder = np.argsort(p_values)\nholm = np.zeros(k)\nfor rank, idx in enumerate(order):\n    holm[idx] = p_values[idx] * (k - rank)\nreject_holm = holm < alpha\nprint(f\"Bonferroni rejects: {reject_bon.sum()} tests\")\nprint(f\"Holm rejects:       {reject_holm.sum()} tests\")"
            },
            {
                "label": "Benjamini-Hochberg FDR Control",
                "code": "import numpy as np\nnp.random.seed(5)\nk = 50\n# 40 nulls + 10 true effects (small p-values)\np_values = np.concatenate([\n    np.random.uniform(0.05, 1.0, 40),\n    np.random.uniform(0, 0.02, 10)\n])\nalpha = 0.05\norder = np.argsort(p_values)\nsorted_p = p_values[order]\nbh_threshold = (np.arange(1, k+1) / k) * alpha\nreject_sorted = sorted_p <= bh_threshold\n# All tests up to last rejection are rejected\nlast_reject = np.where(reject_sorted)[0]\nif len(last_reject):\n    cutoff = last_reject[-1]\n    reject_bh = np.zeros(k, dtype=bool)\n    reject_bh[order[:cutoff+1]] = True\nelse:\n    reject_bh = np.zeros(k, dtype=bool)\nprint(f\"BH FDR rejects: {reject_bh.sum()} of {k} tests\")\nprint(f\"Expected FDR ≤ {alpha}\")"
            },
            {
                "label": "Q-value (Storey's Method)",
                "code": "import numpy as np\nnp.random.seed(2)\nk = 100\np_vals = np.concatenate([np.random.uniform(0,1,75), np.random.beta(0.5,5,25)])\n# Estimate pi0 (proportion of true nulls)\nlambdas = np.arange(0.05, 0.95, 0.05)\npi0_hat = [(p_vals >= l).sum() / (k * (1-l)) for l in lambdas]\npi0 = min(1.0, np.polyfit(lambdas, pi0_hat, 2)[2])  # smoother estimate\n# Compute q-values\norder = np.argsort(p_vals)\nsorted_p = p_vals[order]\nq = pi0 * k * sorted_p / (np.arange(1, k+1))\n# Enforce monotonicity\nfor i in range(k-2, -1, -1):\n    q[i] = min(q[i], q[i+1])\nq_vals = np.empty(k); q_vals[order] = np.minimum(q, 1)\nprint(f\"pi0 estimate: {pi0:.3f}\")\nprint(f\"Discoveries at FDR=0.05: {(q_vals <= 0.05).sum()}\")"
            }
        ],
        "rw_scenario": "Genomics pipeline: after running 10,000 gene expression tests, apply BH correction to control FDR at 5% and identify truly differentially expressed genes.",
        "rw_code": "import numpy as np\nnp.random.seed(99)\nn_genes = 10000\nn_de = 200  # truly differentially expressed\n# Simulate p-values: most null (uniform), some true effects (beta)\np_null = np.random.uniform(0, 1, n_genes - n_de)\np_de   = np.random.beta(0.3, 10, n_de)\np_values = np.concatenate([p_null, p_de])\nalpha = 0.05\n# BH procedure\norder = np.argsort(p_values)\nsorted_p = p_values[order]\nranks = np.arange(1, n_genes+1)\nbh_thresh = (ranks / n_genes) * alpha\nlast = np.where(sorted_p <= bh_thresh)[0]\nif len(last):\n    cutoff = last[-1]\n    reject = np.zeros(n_genes, dtype=bool)\n    reject[order[:cutoff+1]] = True\nelse:\n    reject = np.zeros(n_genes, dtype=bool)\n# True positive rate among real DE genes\ntp = reject[-n_de:].sum()\nfp = reject[:-n_de].sum()\nprint(f\"Significant genes: {reject.sum()}\")\nprint(f\"True positives: {tp}/{n_de} ({tp/n_de:.1%} sensitivity)\")\nprint(f\"False positives: {fp} (FDR={fp/max(reject.sum(),1):.3f})\")",
        "practice": {
            "title": "Drug Trial Multiple Endpoints",
            "desc": "A clinical trial tests 12 endpoints (primary + secondary). Raw p-values are given. Apply Bonferroni, Holm, and BH corrections. Build a table showing which endpoints remain significant under each method. Discuss the tradeoff between FWER and FDR control in regulatory contexts.",
            "starter": "import numpy as np\n# 12 endpoint p-values from clinical trial\np_values = np.array([0.001, 0.008, 0.023, 0.046, 0.052, 0.071,\n                     0.12, 0.18, 0.21, 0.34, 0.52, 0.74])\nk = len(p_values)\nalpha = 0.05\n# TODO: Bonferroni correction + reject/accept\n# TODO: Holm step-down correction + reject/accept\n# TODO: BH FDR correction + reject/accept\n# TODO: Print comparison table\n# TODO: Discuss which method to use and why\n"
        }
    },
    {
        "title": "16. Dimensionality Reduction for Statistical Analysis",
        "examples": [
            {
                "label": "PCA for Outlier Detection",
                "code": "import numpy as np\nfrom sklearn.decomposition import PCA\nfrom sklearn.preprocessing import StandardScaler\nnp.random.seed(0)\nX = np.random.multivariate_normal([0,0,0], [[1,.7,.3],[.7,1,.2],[.3,.2,1]], 200)\nX[5] += [4, 4, 4]  # inject outlier\nscaler = StandardScaler()\nXs = scaler.fit_transform(X)\npca = PCA(n_components=2)\nscores = pca.fit_transform(Xs)\nreconstruction = pca.inverse_transform(scores)\nresiduals = np.sum((Xs - reconstruction)**2, axis=1)\nthreshold = np.percentile(residuals, 97.5)\noutliers = np.where(residuals > threshold)[0]\nprint(f\"Explained variance: {pca.explained_variance_ratio_.cumsum()[-1]:.2%}\")\nprint(f\"Reconstruction outliers (index): {outliers}\")"
            },
            {
                "label": "t-SNE for Cluster Visualization",
                "code": "import numpy as np\nfrom sklearn.manifold import TSNE\nfrom sklearn.datasets import make_blobs\nnp.random.seed(42)\nX, y = make_blobs(n_samples=300, centers=4, n_features=8, cluster_std=1.5)\ntsne = TSNE(n_components=2, perplexity=30, n_iter=300, random_state=42)\nX_2d = tsne.fit_transform(X)\nfor cls in np.unique(y):\n    mask = y == cls\n    print(f\"Cluster {cls}: centroid ({X_2d[mask,0].mean():.2f}, {X_2d[mask,1].mean():.2f}), n={mask.sum()}\")\nprint(f\"KL divergence: {tsne.kl_divergence_:.4f}\")"
            },
            {
                "label": "UMAP + Statistical Tests on Components",
                "code": "import numpy as np\nfrom sklearn.decomposition import PCA\nfrom sklearn.preprocessing import StandardScaler\nfrom scipy import stats\nnp.random.seed(1)\n# Two groups with different multivariate structure\ng1 = np.random.multivariate_normal([0]*5, np.eye(5), 100)\ng2 = np.random.multivariate_normal([0.5]*5, np.eye(5)*1.5, 100)\nX = np.vstack([g1, g2])\nlabels = np.array([0]*100 + [1]*100)\npca = PCA(n_components=3)\nXp = pca.fit_transform(StandardScaler().fit_transform(X))\nfor i in range(3):\n    t, p = stats.ttest_ind(Xp[labels==0, i], Xp[labels==1, i])\n    print(f\"PC{i+1}: t={t:.3f}, p={p:.4f} ({\'significant\' if p<0.05 else \'not sig\'})\")\nprint(f\"Total variance explained: {pca.explained_variance_ratio_.sum():.2%}\")"
            }
        ],
        "rw_scenario": "Credit risk modelling: apply PCA to 20 correlated financial features, use the top components as inputs for logistic regression, and test if the components differ significantly between default and non-default customers.",
        "rw_code": "import numpy as np\nfrom sklearn.decomposition import PCA\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.model_selection import cross_val_score\nfrom scipy import stats\nnp.random.seed(42)\nn = 500\n# 20 correlated features simulating financial metrics\ncov = 0.4 * np.ones((20, 20)) + 0.6 * np.eye(20)\nX_raw = np.random.multivariate_normal(np.zeros(20), cov, n)\n# Default probability depends on first latent factor\nlatent = X_raw[:, :5].mean(axis=1)\nprob = 1 / (1 + np.exp(-(latent - 0.3)))\ny = np.random.binomial(1, prob, n)\nscaler = StandardScaler()\nX = scaler.fit_transform(X_raw)\npca = PCA(n_components=5)\nX_pca = pca.fit_transform(X)\nprint(f\"Variance explained: {pca.explained_variance_ratio_.cumsum()[-1]:.2%}\")\nfor i in range(5):\n    t, p = stats.ttest_ind(X_pca[y==0, i], X_pca[y==1, i])\n    print(f\"PC{i+1}: defaulters vs non-defaulters t={t:.2f}, p={p:.4f}\")\nclf = LogisticRegression()\nscores = cross_val_score(clf, X_pca, y, cv=5, scoring=\'roc_auc\')\nprint(f\"Logistic Regression AUC (PCA features): {scores.mean():.3f} ± {scores.std():.3f}\")",
        "practice": {
            "title": "Customer Segmentation with Dimensionality Reduction",
            "desc": "Apply PCA then k-means (k=4) to a simulated customer dataset with 15 features. For each cluster, run one-way ANOVA on the top 3 PCs and 3 original features to test for between-cluster differences. Report F-statistics, p-values, and effect sizes (eta-squared). Visualize clusters in 2D PCA space.",
            "starter": "import numpy as np\nfrom sklearn.decomposition import PCA\nfrom sklearn.cluster import KMeans\nfrom sklearn.preprocessing import StandardScaler\nfrom scipy import stats\nnp.random.seed(21)\nX = np.random.randn(400, 15)\n# Inject 4-cluster structure\nfor i in range(4):\n    X[i*100:(i+1)*100, :5] += i * 1.2\nscaler = StandardScaler()\nXs = scaler.fit_transform(X)\n# TODO: PCA to 2D and 5D\n# TODO: KMeans(k=4) on 5D PCA\n# TODO: ANOVA on top 3 PCs and 3 original features per cluster\n# TODO: Report eta-squared effect sizes\n# TODO: Plot 2D PCA colored by cluster\n"
        }
    },
{
"title": "17. Hypothesis Testing (t-tests & z-tests)",
"desc": "Hypothesis testing decides whether observed data supports a null hypothesis H0. One-sample, two-sample, and paired t-tests cover most practical scenarios. Always check assumptions: normality, equal variance.",
"examples": [
        {"label": "One-sample and two-sample t-tests", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(42)\n\n# One-sample t-test: is the mean different from a known value?\nweights = np.random.normal(70, 8, 30)\nt_stat, p_val = stats.ttest_1samp(weights, popmean=72)\nprint(f\"One-sample t-test: t={t_stat:.3f}, p={p_val:.4f}\")\nprint(f\"  Reject H0 (mean=72)? {p_val < 0.05}\")\n\n# Two-sample t-test: do two groups have different means?\ngroup_a = np.random.normal(75, 10, 40)\ngroup_b = np.random.normal(80, 10, 40)\nt2, p2 = stats.ttest_ind(group_a, group_b)\nprint(f\"Two-sample t-test: t={t2:.3f}, p={p2:.4f}\")\nprint(f\"  Reject H0 (equal means)? {p2 < 0.05}\")\n\n# Welch\'s t-test (unequal variances — safer default)\ngroup_c = np.random.normal(80, 20, 40)  # larger std\nt3, p3 = stats.ttest_ind(group_a, group_c, equal_var=False)\nprint(f\"Welch\'s t-test: t={t3:.3f}, p={p3:.4f}\")\nprint(f\"  Mean A={group_a.mean():.2f}, Mean C={group_c.mean():.2f}\")"},
        {"label": "Paired t-test and confidence intervals", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(0)\n# Paired t-test: before/after measurements on same subjects\nbefore = np.random.normal(130, 15, 25)   # blood pressure before treatment\nafter  = before - np.random.normal(8, 5, 25)  # treatment lowers BP\n\nt, p = stats.ttest_rel(before, after)\ndiff = before - after\nci = stats.t.interval(0.95, df=len(diff)-1,\n                       loc=diff.mean(), scale=stats.sem(diff))\n\nprint(f\"Paired t-test: t={t:.3f}, p={p:.4f}\")\nprint(f\"Mean reduction: {diff.mean():.2f} mmHg\")\nprint(f\"95% CI: ({ci[0]:.2f}, {ci[1]:.2f})\")\nprint(f\"Significant reduction? {p < 0.05}\")\n\n# Manual CI for a mean\nn, mean, se = len(before), before.mean(), stats.sem(before)\nci_manual = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)\nprint(f\"\\nCI for baseline BP mean {mean:.1f}: ({ci_manual[0]:.1f}, {ci_manual[1]:.1f})\")"},
        {"label": "Chi-square test and proportions z-test", "code": "from scipy import stats\nimport numpy as np\n\n# Chi-square test for independence\n# Question: Is treatment type independent of recovery?\nobserved = np.array([[45, 15],   # Drug A: recovered, not recovered\n                      [30, 30],   # Drug B\n                      [38, 22]])  # Placebo\n\nchi2, p, dof, expected = stats.chi2_contingency(observed)\nprint(f\"Chi-square: chi2={chi2:.3f}, p={p:.4f}, dof={dof}\")\nprint(f\"Association between treatment and recovery? {p < 0.05}\")\n\n# Two-proportion z-test\n# Are conversion rates different between landing pages?\nn_a, conv_a = 1000, 120   # page A\nn_b, conv_b = 1000, 145   # page B\n\ncount = np.array([conv_a, conv_b])\nnobs  = np.array([n_a, n_b])\nz, p_prop = stats.proportions_ztest(count, nobs)\nprint(f\"\\nProportions z-test: z={z:.3f}, p={p_prop:.4f}\")\nprint(f\"Rate A={conv_a/n_a:.1%}, Rate B={conv_b/n_b:.1%}\")\nprint(f\"Significantly different? {p_prop < 0.05}\")"}
    ],
"rw_scenario": "A pharma company tests whether a new drug reduces cholesterol more than a placebo. Paired t-test on 50 patients (pre/post treatment) with a significance level of 0.05.",
"rw_code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(7)\nn = 50\ndrug_group    = np.random.normal(200, 30, n)  # baseline cholesterol\nplacebo_group = np.random.normal(200, 30, n)\n\ndrug_post    = drug_group    - np.random.normal(25, 10, n)  # drug reduces ~25\nplacebo_post = placebo_group - np.random.normal(5,  10, n)  # placebo reduces ~5\n\ndrug_diff    = drug_group    - drug_post\nplacebo_diff = placebo_group - placebo_post\n\nt_drug,    p_drug    = stats.ttest_rel(drug_group,    drug_post)\nt_placebo, p_placebo = stats.ttest_rel(placebo_group, placebo_post)\nt_compare, p_compare = stats.ttest_ind(drug_diff,     placebo_diff)\n\nprint(f\"Drug group:    mean reduction={drug_diff.mean():.1f}, p={p_drug:.4f}\")\nprint(f\"Placebo group: mean reduction={placebo_diff.mean():.1f}, p={p_placebo:.4f}\")\nprint(f\"Drug vs Placebo: t={t_compare:.3f}, p={p_compare:.4f}\")\nprint(f\"Drug significantly better? {p_compare < 0.05}\")",
"practice": {
    "title": "A/B Test Analysis",
    "desc": "Two email subject lines were tested: A sent to 800 users (92 opened), B to 800 users (117 opened). (1) Run a two-proportion z-test. (2) Compute the 95% CI for the difference in rates. (3) Calculate the lift (relative improvement). (4) Determine the minimum detectable effect if you want 80% power at alpha=0.05.",
    "starter": "from scipy import stats\nimport numpy as np\n\nn_a, open_a = 800, 92\nn_b, open_b = 800, 117\n\n# (1) two-proportion z-test\n# (2) 95% CI for difference\n# (3) lift = (rate_b - rate_a) / rate_a\n# (4) minimum detectable effect hint: use stats.norm.isf for z-scores\nrate_a = open_a / n_a\nrate_b = open_b / n_b\nprint(f\"Rate A: {rate_a:.3f}, Rate B: {rate_b:.3f}\")\n"
}
},

{
"title": "18. ANOVA & Post-hoc Tests",
"desc": "One-way ANOVA tests whether means differ across 3+ groups in a single factor. Two-way ANOVA adds a second factor and interaction. Post-hoc tests (Tukey, Bonferroni) identify which pairs differ.",
"examples": [
        {"label": "One-way ANOVA with post-hoc Tukey HSD", "code": "from scipy import stats\nfrom statsmodels.stats.multicomp import pairwise_tukeyhsd\nimport numpy as np\n\nnp.random.seed(42)\n# Crop yield under 4 fertilizer types\ngroups = {\n    \'Control\':  np.random.normal(50, 8, 20),\n    \'FertA\':    np.random.normal(58, 8, 20),\n    \'FertB\':    np.random.normal(55, 8, 20),\n    \'FertC\':    np.random.normal(62, 8, 20),\n}\n\nf_stat, p_val = stats.f_oneway(*groups.values())\nprint(f\"One-way ANOVA: F={f_stat:.3f}, p={p_val:.4f}\")\nprint(f\"Significant difference exists? {p_val < 0.05}\\n\")\n\n# Tukey HSD post-hoc\nimport numpy as np as _np\nall_data   = np.concatenate(list(groups.values()))\nall_labels = np.repeat(list(groups.keys()), 20)\n\ntukey = pairwise_tukeyhsd(endog=all_data, groups=all_labels, alpha=0.05)\nprint(tukey.summary())"},
        {"label": "Two-way ANOVA with interaction", "code": "import statsmodels.api as sm\nfrom statsmodels.formula.api import ols\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nn = 120\ndf = pd.DataFrame({\n    \'fertilizer\': np.repeat([\'A\',\'B\',\'C\'], n//3),\n    \'irrigation\': np.tile([\'Low\',\'High\'], n//2),\n    \'yield\': (np.random.normal(55, 8, n) +\n              np.where(np.repeat([\'A\',\'B\',\'C\'], n//3)==\'C\', 8, 0) +\n              np.where(np.tile([\'Low\',\'High\'], n//2)==\'High\', 5, 0)),\n})\n\nmodel = ols(\'yield ~ C(fertilizer) + C(irrigation) + C(fertilizer):C(irrigation)\',\n            data=df).fit()\nanova_table = sm.stats.anova_lm(model, typ=2)\nprint(anova_table.round(4))\nprint(f\"\\nFertilizer effect: p={anova_table.loc[\'C(fertilizer)\',\'PR(>F)\']:.4f}\")\nprint(f\"Irrigation effect: p={anova_table.loc[\'C(irrigation)\',\'PR(>F)\']:.4f}\")"},
        {"label": "Kruskal-Wallis (non-parametric ANOVA) + Bonferroni", "code": "from scipy import stats\nfrom statsmodels.stats.multitest import multipletests\nimport numpy as np\nfrom itertools import combinations\n\nnp.random.seed(5)\n# Non-normal data: response times across 3 UI designs\ngroups = {\n    \'Design A\': np.random.exponential(2.0, 30),\n    \'Design B\': np.random.exponential(1.5, 30),\n    \'Design C\': np.random.exponential(2.5, 30),\n}\nnames = list(groups.keys())\ndata  = list(groups.values())\n\n# Kruskal-Wallis\nH, p = stats.kruskal(*data)\nprint(f\"Kruskal-Wallis: H={H:.3f}, p={p:.4f}\")\n\n# Pairwise Mann-Whitney U with Bonferroni correction\npairs = list(combinations(range(len(names)), 2))\nraw_p = []\nfor i, j in pairs:\n    _, pv = stats.mannwhitneyu(data[i], data[j], alternative=\'two-sided\')\n    raw_p.append(pv)\n\nreject, p_adj, _, _ = multipletests(raw_p, method=\'bonferroni\')\nfor (i,j), pv, pa, rej in zip(pairs, raw_p, p_adj, reject):\n    print(f\"  {names[i]} vs {names[j]}: raw_p={pv:.4f}, adj_p={pa:.4f}, reject={rej}\")"}
    ],
"rw_scenario": "A UX researcher tests 3 onboarding flows on task completion time across 60 users. ANOVA reveals a significant difference; Tukey HSD pinpoints which flow pairs differ significantly.",
"rw_code": "from scipy import stats\nfrom statsmodels.stats.multicomp import pairwise_tukeyhsd\nimport numpy as np, pandas as pd\n\nnp.random.seed(99)\nflows = {\'Flow 1\': np.random.normal(45, 12, 20),\n         \'Flow 2\': np.random.normal(38, 10, 20),\n         \'Flow 3\': np.random.normal(52, 14, 20)}\n\nf, p = stats.f_oneway(*flows.values())\nprint(f\"ANOVA: F={f:.3f}, p={p:.4f}\")\n\nall_times  = np.concatenate(list(flows.values()))\nall_labels = np.repeat(list(flows.keys()), 20)\ntukey = pairwise_tukeyhsd(all_times, all_labels, alpha=0.05)\nprint(tukey.summary())\n\nfor name, times in flows.items():\n    print(f\"{name}: mean={times.mean():.1f}s, sd={times.std():.1f}s\")",
"practice": {
    "title": "Marketing Channel ANOVA",
    "desc": "Generate sales data for 4 marketing channels (Email, Social, Search, Display) — 25 observations each with means 120, 135, 150, 110 and std=25. (1) Run one-way ANOVA. (2) If significant, run Tukey HSD to identify which channels differ. (3) Compute eta-squared (effect size = SS_between / SS_total).",
    "starter": "from scipy import stats\nfrom statsmodels.stats.multicomp import pairwise_tukeyhsd\nimport numpy as np\n\nnp.random.seed(42)\nchannels = {\'Email\':   np.random.normal(120, 25, 25),\n            \'Social\':  np.random.normal(135, 25, 25),\n            \'Search\':  np.random.normal(150, 25, 25),\n            \'Display\': np.random.normal(110, 25, 25)}\n\n# (1) One-way ANOVA\n# (2) Tukey HSD if significant\n# (3) eta-squared = SS_between / SS_total\n# SS_total = sum of (xi - grand_mean)^2 across all observations\n"
}
},

{
"title": "19. Correlation Analysis",
"desc": "Pearson measures linear association between continuous variables. Spearman and Kendall are rank-based (robust to outliers and non-linearity). Point-biserial handles binary-continuous pairs.",
"examples": [
        {"label": "Pearson, Spearman, Kendall correlation", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(42)\nn = 100\n\n# Pearson: linear relationship\nx = np.random.randn(n)\ny_linear = 2 * x + np.random.randn(n) * 0.5\n\nr_p, p_p = stats.pearsonr(x, y_linear)\nr_s, p_s = stats.spearmanr(x, y_linear)\nr_k, p_k = stats.kendalltau(x, y_linear)\nprint(\"Linear relationship:\")\nprint(f\"  Pearson r={r_p:.4f}  Spearman r={r_s:.4f}  Kendall tau={r_k:.4f}\")\n\n# Spearman handles monotonic non-linear relationships\ny_mono = np.exp(x) + np.random.randn(n) * 0.3\nr_p2, _ = stats.pearsonr(x, y_mono)\nr_s2, _ = stats.spearmanr(x, y_mono)\nprint(f\"\\nMonotonic (non-linear):\")\nprint(f\"  Pearson r={r_p2:.4f}  Spearman r={r_s2:.4f}\")\n\n# With outliers: Spearman is robust\ny_outlier = y_linear.copy()\ny_outlier[[5, 10, 15]] = 100  # inject outliers\nr_p3, _ = stats.pearsonr(x, y_outlier)\nr_s3, _ = stats.spearmanr(x, y_outlier)\nprint(f\"\\nWith outliers:\")\nprint(f\"  Pearson r={r_p3:.4f}  Spearman r={r_s3:.4f}  (Spearman more robust)\")"},
        {"label": "Correlation matrix and partial correlation", "code": "from scipy import stats\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nn = 200\n# Confounding variable Z drives both X and Y\nz = np.random.randn(n)\nx = 0.7 * z + np.random.randn(n) * 0.5\ny = 0.8 * z + np.random.randn(n) * 0.5\nw = np.random.randn(n)  # unrelated\n\ndf = pd.DataFrame({\'X\': x, \'Y\': y, \'Z\': z, \'W\': w})\n\nprint(\"Correlation matrix:\")\nprint(df.corr(method=\'pearson\').round(3))\n\n# Partial correlation: X-Y controlling for Z\ndef partial_corr(x, y, z):\n    # Regress out z from both x and y\n    r_xz = np.corrcoef(x, z)[0,1]\n    r_yz = np.corrcoef(y, z)[0,1]\n    r_xy = np.corrcoef(x, y)[0,1]\n    return (r_xy - r_xz*r_yz) / (np.sqrt(1-r_xz**2) * np.sqrt(1-r_yz**2))\n\npc = partial_corr(x, y, z)\nprint(f\"\\nX-Y raw correlation:     {np.corrcoef(x,y)[0,1]:.4f}\")\nprint(f\"X-Y partial (given Z):   {pc:.4f}  (much lower — Z was confounding)\")"},
        {"label": "Point-biserial, phi coefficient, and significance testing", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(3)\nn = 150\n\n# Point-biserial: continuous vs binary\nscores = np.random.normal(70, 10, n)\npassed = (scores + np.random.randn(n)*5 > 68).astype(int)\nr_pb, p_pb = stats.pointbiserialr(passed, scores)\nprint(f\"Point-biserial r={r_pb:.4f}, p={p_pb:.4f}\")\n\n# Phi coefficient: binary vs binary\nvaccinated = np.random.choice([0,1], n, p=[0.4,0.6])\ninfected   = np.where(vaccinated==1,\n                       np.random.choice([0,1], n, p=[0.9,0.1]),\n                       np.random.choice([0,1], n, p=[0.4,0.6]))\nchi2, p_chi, _, _ = stats.chi2_contingency(\n    np.array([[((vaccinated==0)&(infected==0)).sum(),\n               ((vaccinated==0)&(infected==1)).sum()],\n              [((vaccinated==1)&(infected==0)).sum(),\n               ((vaccinated==1)&(infected==1)).sum()]]))\nphi = np.sqrt(chi2 / n)\nprint(f\"Phi coefficient={phi:.4f}, chi2_p={p_chi:.4f}\")\n\n# Testing significance of Pearson r\nr = 0.35\nn_test = 50\nt = r * np.sqrt(n_test-2) / np.sqrt(1-r**2)\np = 2 * stats.t.sf(abs(t), df=n_test-2)\nprint(f\"\\nr=0.35, n=50: t={t:.3f}, p={p:.4f}, significant={p<0.05}\")"}
    ],
"rw_scenario": "A sports analyst computes Spearman correlations between athlete metrics (speed, strength, endurance, recovery) and competitive performance, then uses partial correlation to remove the confounding effect of age.",
"rw_code": "from scipy import stats\nimport numpy as np, pandas as pd\n\nnp.random.seed(10)\nn = 80\nage = np.random.uniform(18, 35, n)\nspeed      = -0.4*age + np.random.randn(n)*2 + 30\nstrength   =  0.1*age + np.random.randn(n)*3 + 20\nendurance  = -0.3*age + np.random.randn(n)*2 + 25\nperformance= 0.5*speed + 0.3*strength + 0.4*endurance + np.random.randn(n)*2\n\ndf = pd.DataFrame({\'age\':age,\'speed\':speed,\'strength\':strength,\n                   \'endurance\':endurance,\'performance\':performance})\n\nprint(\"Spearman correlations with performance:\")\nfor col in [\'age\',\'speed\',\'strength\',\'endurance\']:\n    r, p = stats.spearmanr(df[col], df[\'performance\'])\n    print(f\"  {col:12s}: r={r:.3f}, p={p:.4f}\")\n\n# Partial: speed-performance controlling for age\nr_sp = np.corrcoef(speed, performance)[0,1]\nr_sa = np.corrcoef(speed, age)[0,1]\nr_pa = np.corrcoef(performance, age)[0,1]\npc = (r_sp - r_sa*r_pa) / (np.sqrt(1-r_sa**2)*np.sqrt(1-r_pa**2))\nprint(f\"\\nSpeed-Perf raw r={r_sp:.3f}, partial (ctrl age)={pc:.3f}\")",
"practice": {
    "title": "Feature Correlation Screening",
    "desc": "Generate 8 features for 300 samples (some correlated, some independent, one binary). (1) Compute and print the full Pearson correlation matrix. (2) Flag all feature pairs with |r| > 0.7 as highly correlated. (3) Compute point-biserial correlation of the binary feature with each continuous feature. (4) Test each correlation for significance.",
    "starter": "from scipy import stats\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nn = 300\nz = np.random.randn(n)\ndf = pd.DataFrame({\n    \'f1\': z + np.random.randn(n)*0.3,\n    \'f2\': -0.8*z + np.random.randn(n)*0.3,  # correlated with f1\n    \'f3\': np.random.randn(n),\n    \'f4\': np.random.randn(n),\n    \'f5\': 0.9*z + np.random.randn(n)*0.1,   # highly correlated\n    \'f6\': np.random.exponential(2, n),\n    \'f7\': np.random.randn(n),\n    \'binary\': (z > 0).astype(int),\n})\n\n# (1) correlation matrix\n# (2) flag |r| > 0.7 pairs\n# (3) point-biserial for binary vs continuous\n# (4) test significance\n"
}
},

{
"title": "20. Non-Parametric Tests",
"desc": "Non-parametric tests make no assumptions about distributions. Use them when data is ordinal, heavily skewed, or sample sizes are too small to verify normality. Wilcoxon, Mann-Whitney, and Kolmogorov-Smirnov are the workhorses.",
"examples": [
        {"label": "Normality tests: Shapiro-Wilk and D\'Agostino", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(42)\n\ndatasets = {\n    \'Normal\':      np.random.normal(50, 10, 50),\n    \'Skewed\':      np.random.exponential(5, 50),\n    \'Heavy-tailed\':np.random.standard_t(df=3, size=50),\n    \'Uniform\':     np.random.uniform(0, 100, 50),\n}\n\nprint(f\"{\'Dataset\':15s}  {\'Shapiro p\':>10s}  {\'D\\\'Agostino p\':>13s}  {\'Normal?\'}\")\nprint(\'-\' * 60)\nfor name, data in datasets.items():\n    _, p_sw  = stats.shapiro(data)\n    _, p_da  = stats.normaltest(data)\n    is_norm  = p_sw > 0.05 and p_da > 0.05\n    print(f\"{name:15s}  {p_sw:10.4f}  {p_da:13.4f}  {str(is_norm)}\")\n\n# Q-Q plot values (manual)\nnormal_data = datasets[\'Normal\']\ntheoretical, observed = stats.probplot(normal_data, dist=\'norm\')[0]\nr = np.corrcoef(theoretical, observed)[0,1]\nprint(f\"\\nQ-Q correlation for Normal: {r:.4f} (close to 1 = normal)\")"},
        {"label": "Wilcoxon signed-rank and Mann-Whitney U", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(7)\n# Wilcoxon signed-rank: paired non-parametric alternative to paired t-test\nbefore = np.random.exponential(2.0, 30)\nafter  = before * 0.7 + np.random.exponential(0.3, 30)\n\nstat_w, p_w = stats.wilcoxon(before, after)\nstat_t, p_t = stats.ttest_rel(before, after)\nprint(\"Paired comparison (before vs after):\")\nprint(f\"  Wilcoxon: stat={stat_w:.1f}, p={p_w:.4f}\")\nprint(f\"  t-test:   stat={stat_t:.3f}, p={p_t:.4f}\")\n\n# Mann-Whitney U: non-parametric two-sample test\ngroup1 = np.random.exponential(3.0, 40)\ngroup2 = np.random.exponential(4.5, 40)\n\nu_stat, p_u = stats.mannwhitneyu(group1, group2, alternative=\'two-sided\')\nt_stat, p_t2 = stats.ttest_ind(group1, group2)\nprint(f\"\\nTwo-group comparison:\")\nprint(f\"  Mann-Whitney: U={u_stat:.1f}, p={p_u:.4f}\")\nprint(f\"  t-test:       t={t_stat:.3f}, p={p_t2:.4f}\")\n\n# Effect size r = Z / sqrt(N) for Mann-Whitney\nn1, n2 = len(group1), len(group2)\nz = stats.norm.ppf(p_u/2)  # approximate z\nr_effect = abs(z) / np.sqrt(n1+n2)\nprint(f\"  Effect size r: {r_effect:.3f}\")"},
        {"label": "Kolmogorov-Smirnov and Anderson-Darling tests", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(0)\n\n# One-sample KS: does data come from a specified distribution?\ndata_normal = np.random.normal(0, 1, 100)\ndata_exp    = np.random.exponential(1, 100)\n\nfor name, data in [(\'Normal\', data_normal), (\'Exponential\', data_exp)]:\n    ks_n, p_n = stats.kstest(data, \'norm\', args=(data.mean(), data.std()))\n    ks_e, p_e = stats.kstest(data, \'expon\', args=(0, 1/data.mean()))\n    print(f\"{name}: KS vs Normal p={p_n:.4f}, KS vs Expon p={p_e:.4f}\")\n\n# Two-sample KS: do two samples come from the same distribution?\nsample_a = np.random.normal(0, 1, 100)\nsample_b = np.random.normal(0.5, 1, 100)  # slightly shifted\nks2, p2 = stats.ks_2samp(sample_a, sample_b)\nprint(f\"\\n2-sample KS: stat={ks2:.4f}, p={p2:.4f}\")\n\n# Anderson-Darling (more powerful than KS for normal testing)\nresult = stats.anderson(data_normal, dist=\'norm\')\nprint(f\"\\nAnderson-Darling statistic: {result.statistic:.4f}\")\nfor sl, cv in zip(result.significance_level, result.critical_values):\n    print(f\"  {sl}% significance level: crit={cv:.4f}, reject={result.statistic > cv}\")"}
    ],
"rw_scenario": "A clinical researcher compares pain scores (skewed, ordinal 1-10) between a drug and control group. Shapiro-Wilk confirms non-normality, so Mann-Whitney U is used instead of a t-test.",
"rw_code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(42)\n# Pain scores: skewed, bounded 1-10\ndrug_scores    = np.clip(np.random.exponential(2.5, 40) + 1, 1, 10).round()\ncontrol_scores = np.clip(np.random.exponential(4.0, 40) + 1, 1, 10).round()\n\n# Test normality first\n_, p_drug = stats.shapiro(drug_scores)\n_, p_ctrl = stats.shapiro(control_scores)\nprint(f\"Shapiro p-values: drug={p_drug:.4f}, control={p_ctrl:.4f}\")\nprint(f\"Use non-parametric: {p_drug < 0.05 or p_ctrl < 0.05}\")\n\n# Mann-Whitney U\nu, p = stats.mannwhitneyu(drug_scores, control_scores, alternative=\'less\')\nprint(f\"Mann-Whitney: U={u:.1f}, p={p:.4f}\")\nprint(f\"Drug reduces pain? {p < 0.05}\")\nprint(f\"Median drug={np.median(drug_scores):.1f}, control={np.median(control_scores):.1f}\")",
"practice": {
    "title": "Distribution Comparison Pipeline",
    "desc": "Write a function compare_groups(a, b) that: (1) Tests normality of both groups with Shapiro-Wilk, (2) If both normal, runs Levene\'s test for equal variances, then appropriate t-test (Welch or Student), (3) If either non-normal, runs Mann-Whitney U, (4) Returns a dict with test_used, statistic, p_value, significant. Test with normal and non-normal pairs.",
    "starter": "from scipy import stats\nimport numpy as np\n\ndef compare_groups(a, b, alpha=0.05):\n    result = {}\n    # (1) normality\n    _, p_a = stats.shapiro(a)\n    _, p_b = stats.shapiro(b)\n    both_normal = p_a > alpha and p_b > alpha\n    # (2) if normal: Levene then t-test\n    # (3) if not normal: Mann-Whitney\n    # (4) return dict\n    return result\n\nnp.random.seed(42)\nnormal_a = np.random.normal(10, 2, 30)\nnormal_b = np.random.normal(11, 2, 30)\nskewed_a = np.random.exponential(2, 30)\nskewed_b = np.random.exponential(3, 30)\n\nprint(compare_groups(normal_a, normal_b))\nprint(compare_groups(skewed_a, skewed_b))\n"
}
},

{
"title": "21. Bayesian Inference Basics",
"desc": "Bayesian inference updates prior beliefs with observed data to produce a posterior distribution. Beta-Binomial and Normal-Normal conjugates let you compute posteriors analytically. Compare to frequentist interpretation of the same data.",
"examples": [
        {"label": "Beta-Binomial: updating conversion rate beliefs", "code": "from scipy import stats\nimport numpy as np\n\n# Prior: Beta(alpha=2, beta=10) — we expect ~17% conversion\nprior_a, prior_b = 2, 10\n\n# Observed data: 45 conversions out of 200 visits\nobs_conv, obs_total = 45, 200\nobs_failures = obs_total - obs_conv\n\n# Posterior: Beta(alpha + successes, beta + failures) [conjugate]\npost_a = prior_a + obs_conv\npost_b = prior_b + obs_failures\n\nprior     = stats.beta(prior_a, prior_b)\nposterior = stats.beta(post_a, post_b)\n\nprint(f\"Prior:     mean={prior.mean():.3f}, 95% CI: ({prior.ppf(0.025):.3f}, {prior.ppf(0.975):.3f})\")\nprint(f\"Posterior: mean={posterior.mean():.3f}, 95% CI: ({posterior.ppf(0.025):.3f}, {posterior.ppf(0.975):.3f})\")\nprint(f\"MLE (freq): {obs_conv/obs_total:.3f}\")\n\n# Probability that conversion > 25%\nprob_above = 1 - posterior.cdf(0.25)\nprint(f\"P(conversion > 25%): {prob_above:.4f}\")\n\n# Posterior predictive: expected conversions in next 100\npp_mean  = posterior.mean() * 100\npp_sd    = np.sqrt(posterior.var() * 100)\nprint(f\"Expected conversions (next 100): {pp_mean:.1f} ± {pp_sd:.1f}\")"},
        {"label": "Bayesian A/B test: comparing two rates", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(42)\n\n# A/B test with conjugate Beta posteriors\nconv_a, n_a = 120, 1000   # page A\nconv_b, n_b = 145, 1000   # page B\n\n# Non-informative priors Beta(1,1) = Uniform\npost_a = stats.beta(1 + conv_a, 1 + n_a - conv_a)\npost_b = stats.beta(1 + conv_b, 1 + n_b - conv_b)\n\n# Monte Carlo estimate P(B > A)\nsamples_a = post_a.rvs(100_000)\nsamples_b = post_b.rvs(100_000)\np_b_wins  = (samples_b > samples_a).mean()\n\n# Expected lift\nlift_samples = (samples_b - samples_a) / samples_a\nlift_mean = lift_samples.mean()\nlift_ci = np.percentile(lift_samples, [2.5, 97.5])\n\nprint(f\"P(B > A) = {p_b_wins:.4f}\")\nprint(f\"Expected lift: {lift_mean:.1%}\")\nprint(f\"95% credible interval for lift: ({lift_ci[0]:.1%}, {lift_ci[1]:.1%})\")\nprint(f\"Posterior A: mean={post_a.mean():.4f}\")\nprint(f\"Posterior B: mean={post_b.mean():.4f}\")"},
        {"label": "Normal-Normal conjugate for mean estimation", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(0)\n# Estimating the true mean of a process\n# Prior: Normal(mu0=100, sigma0=20)  — prior belief about mean\n# Known measurement noise: sigma=15\n\nmu0, sigma0 = 100.0, 20.0   # prior\nsigma_obs   = 15.0            # known observation noise\n\n# Observe 30 measurements\ntrue_mean = 112.0\ndata = np.random.normal(true_mean, sigma_obs, 30)\nn, x_bar = len(data), data.mean()\n\n# Conjugate update\nprecision_prior = 1 / sigma0**2\nprecision_data  = n / sigma_obs**2\nprecision_post  = precision_prior + precision_data\n\nmu_post    = (precision_prior*mu0 + precision_data*x_bar) / precision_post\nsigma_post = np.sqrt(1 / precision_post)\n\nprior_dist = stats.norm(mu0, sigma0)\npost_dist  = stats.norm(mu_post, sigma_post)\n\nprint(f\"Prior:        mean={mu0:.1f},     95% CI: ({prior_dist.ppf(0.025):.1f}, {prior_dist.ppf(0.975):.1f})\")\nprint(f\"Likelihood:   mean={x_bar:.2f},  (n={n} obs, noise={sigma_obs})\")\nprint(f\"Posterior:    mean={mu_post:.2f}, 95% CI: ({post_dist.ppf(0.025):.2f}, {post_dist.ppf(0.975):.2f})\")\nprint(f\"True mean:    {true_mean}\")\nprint(f\"Posterior pulls toward prior when data is limited.\")"}
    ],
"rw_scenario": "An e-commerce platform uses Bayesian A/B testing for a checkout redesign. Instead of waiting for p<0.05, they monitor the posterior probability that variant B outperforms A and stop when P(B>A) > 0.95.",
"rw_code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(42)\n\n# Sequential Bayesian A/B test\ntrue_rate_a, true_rate_b = 0.10, 0.13\nn_per_day = 50\n\npost_a = stats.beta(1, 1)\npost_b = stats.beta(1, 1)\n\nalpha_a, beta_a = 1, 1\nalpha_b, beta_b = 1, 1\n\nprint(f\"{\'Day\':>5s}  {\'n_a\':>6s}  {\'n_b\':>6s}  {\'Rate A\':>8s}  {\'Rate B\':>8s}  {\'P(B>A)\':>8s}\")\nfor day in range(1, 31):\n    # New daily data\n    conv_a = np.random.binomial(n_per_day, true_rate_a)\n    conv_b = np.random.binomial(n_per_day, true_rate_b)\n    alpha_a += conv_a; beta_a += n_per_day - conv_a\n    alpha_b += conv_b; beta_b += n_per_day - conv_b\n\n    post_a = stats.beta(alpha_a, beta_a)\n    post_b = stats.beta(alpha_b, beta_b)\n    p_b_wins = (post_b.rvs(50000) > post_a.rvs(50000)).mean()\n    n_total = (alpha_a + beta_a - 2) + (alpha_b + beta_b - 2)\n\n    if day % 5 == 0 or p_b_wins > 0.95:\n        print(f\"{day:5d}  {n_total//2:6d}  {n_total//2:6d}  {post_a.mean():8.4f}  {post_b.mean():8.4f}  {p_b_wins:8.4f}\")\n    if p_b_wins > 0.95:\n        print(f\"  --> Stopping: P(B>A)={p_b_wins:.4f} > 0.95 on day {day}\")\n        break",
"practice": {
    "title": "Bayesian Coin Fairness",
    "desc": "A coin is flipped 100 times with 62 heads. (1) Start with a uniform prior Beta(1,1). (2) Update sequentially after every 10 flips. (3) Print posterior mean and 95% credible interval at each step. (4) Compare to the frequentist 95% CI at each step. (5) Compute P(p > 0.5) from the final posterior.",
    "starter": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(0)\nn_flips, n_heads = 100, 62\nflips = np.array([1]*n_heads + [0]*(n_flips - n_heads))\nnp.random.shuffle(flips)\n\na, b = 1, 1  # prior Beta(1,1)\n\nprint(f\"{\'Step\':>6s}  {\'Heads\':>6s}  {\'n\':>5s}  {\'Post mean\':>10s}  {\'95% Credible\':>20s}  {\'Freq 95% CI\':>20s}\")\nfor step in range(10, n_flips+1, 10):\n    chunk = flips[:step]\n    h = chunk.sum(); n = len(chunk)\n    a_post = a + h; b_post = b + n - h\n    post = stats.beta(a_post, b_post)\n    # TODO: compute posterior 95% CI from post\n    # TODO: compute frequentist 95% CI using stats.proportion_confint or normal approx\n    # TODO: print row\n    pass\n\n# (5) P(p > 0.5) from final posterior\n"
}
},

{
"title": "22. Effect Size & Statistical Power",
"desc": "Effect size quantifies the magnitude of a difference independently of sample size. Cohen\'s d, r, eta-squared measure effect for different tests. Power analysis determines the sample size needed to detect a given effect.",
"examples": [
        {"label": "Cohen\'s d and r for effect size", "code": "from scipy import stats\nimport numpy as np\n\ndef cohens_d(group1, group2):\n    n1, n2 = len(group1), len(group2)\n    s_pooled = np.sqrt(((n1-1)*group1.std()**2 + (n2-1)*group2.std()**2) / (n1+n2-2))\n    return (group1.mean() - group2.mean()) / s_pooled\n\nnp.random.seed(42)\nthresholds = [(\'Small\', 0.2), (\'Medium\', 0.5), (\'Large\', 0.8)]\n\nprint(f\"{\'Effect\':8s}  {\'Cohen d\':>8s}  {\'Interpretation\':>15s}  {\'p-value\':>8s}\")\nprint(\'-\' * 55)\nfor label, target_d in thresholds:\n    a = np.random.normal(0, 1, 50)\n    b = np.random.normal(target_d, 1, 50)\n    d = cohens_d(b, a)\n    _, p = stats.ttest_ind(a, b)\n    print(f\"{label:8s}  {d:8.3f}  {label:>15s}  {p:8.4f}\")\n\n# r from t-statistic\nt_stat = 3.2\nn_total = 80\nr = np.sqrt(t_stat**2 / (t_stat**2 + n_total - 2))\nprint(f\"\\nt={t_stat}, n={n_total} -> r effect size = {r:.3f}\")\n\n# Eta-squared from F (ANOVA)\nF, df_between, df_within = 8.5, 2, 60\neta2 = (F * df_between) / (F * df_between + df_within)\nprint(f\"F={F}, df_b={df_between}, df_w={df_within} -> eta²={eta2:.3f}\")"},
        {"label": "Sample size calculation for t-test", "code": "from scipy import stats\nimport numpy as np\n\ndef sample_size_ttest(effect_size_d, alpha=0.05, power=0.80, tail=2):\n    z_alpha = stats.norm.ppf(1 - alpha/tail)\n    z_beta  = stats.norm.ppf(power)\n    n = 2 * ((z_alpha + z_beta) / effect_size_d) ** 2\n    return int(np.ceil(n))\n\nprint(\"Required sample size per group (two-sample t-test):\")\nprint(f\"{\'Effect d\':>9s}  {\'α=0.05,80%\':>12s}  {\'α=0.05,90%\':>12s}  {\'α=0.01,80%\':>12s}\")\nprint(\'-\' * 52)\nfor d in [0.2, 0.3, 0.5, 0.8, 1.0]:\n    n1 = sample_size_ttest(d, 0.05, 0.80)\n    n2 = sample_size_ttest(d, 0.05, 0.90)\n    n3 = sample_size_ttest(d, 0.01, 0.80)\n    print(f\"{d:9.1f}  {n1:12d}  {n2:12d}  {n3:12d}\")\n\n# Using statsmodels TTestIndPower\nfrom statsmodels.stats.power import TTestIndPower\nanalysis = TTestIndPower()\nn = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.80)\nprint(f\"\\nstatsmodels: d=0.5, α=0.05, power=0.80 -> n={n:.1f} per group\")\n\n# Achieved power for given n and effect\npower = analysis.solve_power(effect_size=0.3, alpha=0.05, nobs1=100)\nprint(f\"d=0.3, n=100 per group -> achieved power={power:.3f}\")"},
        {"label": "Power curves and minimum detectable effect", "code": "from statsmodels.stats.power import TTestIndPower, ChiSquarePower\nimport numpy as np\n\nanalysis = TTestIndPower()\n\n# Power curve: power vs sample size for different effect sizes\nprint(\"Power by sample size and effect size:\")\nprint(f\"{\'n/grp\':>7s}\", end=\'\')\nfor d in [0.2, 0.3, 0.5, 0.8]:\n    print(f\"  d={d}\", end=\'\')\nprint()\nfor n in [20, 50, 100, 200, 500]:\n    print(f\"{n:7d}\", end=\'\')\n    for d in [0.2, 0.3, 0.5, 0.8]:\n        pwr = analysis.solve_power(effect_size=d, alpha=0.05, nobs1=n)\n        print(f\"  {pwr:.3f}\", end=\'\')\n    print()\n\n# Minimum detectable effect (MDE) given n and desired power\nmde = analysis.solve_power(alpha=0.05, power=0.80, nobs1=200)\nprint(f\"\\nMDE (d) for n=200/grp, power=80%: {mde:.3f}\")\n\n# Chi-square power\nchi_power = ChiSquarePower()\nn_chi = chi_power.solve_power(effect_size=0.3, alpha=0.05, power=0.80, k_bins=3)\nprint(f\"Chi-square: effect=0.3, k=3, power=80% -> n={n_chi:.1f}\")"}
    ],
"rw_scenario": "A product team wants to detect a 10% improvement in task completion rate (from 60% to 66%). They compute required sample size for 80% and 90% power, then run the test and report Cohen\'s h effect size.",
"rw_code": "from statsmodels.stats.power import NormalIndPower\nfrom scipy import stats\nimport numpy as np\n\n# Rate improvement: 60% -> 66%\nrate_a, rate_b = 0.60, 0.66\n\n# Cohen\'s h for proportions\nh = 2 * np.arcsin(np.sqrt(rate_b)) - 2 * np.arcsin(np.sqrt(rate_a))\nprint(f\"Cohen\'s h = {h:.4f}\")\n\n# Required sample size\nanalysis = NormalIndPower()\nfor power in [0.80, 0.90, 0.95]:\n    n = analysis.solve_power(effect_size=h, alpha=0.05, power=power)\n    print(f\"Power={power:.0%}: n={n:.0f} per group (total {2*n:.0f})\")\n\n# Simulate the test\nnp.random.seed(42)\nn_per = int(analysis.solve_power(effect_size=h, alpha=0.05, power=0.80)) + 1\nconv_a = np.random.binomial(n_per, rate_a)\nconv_b = np.random.binomial(n_per, rate_b)\n_, p = stats.proportions_ztest([conv_a, conv_b], [n_per, n_per])\nprint(f\"\\nSimulated test: A={conv_a/n_per:.3f}, B={conv_b/n_per:.3f}, p={p:.4f}\")",
"practice": {
    "title": "Power Analysis Dashboard",
    "desc": "For a two-sample t-test: (1) Compute required n for all combinations of effect_size in [0.2,0.5,0.8] and power in [0.70,0.80,0.90] at alpha=0.05. Print as a grid. (2) For n=150 per group and alpha=0.05, plot (print) a table of achieved power for effect sizes 0.1 to 0.8 in steps of 0.1. (3) Find the MDE for n=300 at 80% power.",
    "starter": "from statsmodels.stats.power import TTestIndPower\nimport numpy as np\n\nanalysis = TTestIndPower()\n\n# (1) n grid\nprint(\"Required n per group:\")\neffects = [0.2, 0.5, 0.8]\npowers  = [0.70, 0.80, 0.90]\n# TODO: print header and rows\n\n# (2) power table for n=150\nprint(\"\\nAchieved power for n=150 per group:\")\n# TODO\n\n# (3) MDE\nmde = analysis.solve_power(alpha=0.05, power=0.80, nobs1=300)\nprint(f\"\\nMDE for n=300: d={mde:.4f}\")\n"
}
},

{
"title": "23. Multiple Testing & FDR Corrections",
"desc": "Running many tests inflates the false positive rate. Bonferroni controls family-wise error rate (conservative). Benjamini-Hochberg (BH) controls the false discovery rate — preferred for exploratory studies with many hypotheses.",
"examples": [
        {"label": "Bonferroni and Holm-Bonferroni corrections", "code": "from statsmodels.stats.multitest import multipletests\nfrom scipy import stats\nimport numpy as np\n\nnp.random.seed(42)\nn_tests = 20\nn_per   = 50\n\n# 20 tests: 3 truly different (true positives), 17 null\ntrue_effect = [0, 0, 0, 0.8, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0.6, 0, 0, 0, 0]\nraw_p = []\nfor d in true_effect:\n    a = np.random.normal(0, 1, n_per)\n    b = np.random.normal(d, 1, n_per)\n    _, p = stats.ttest_ind(a, b)\n    raw_p.append(p)\n\nmethods = [\'bonferroni\', \'holm\', \'fdr_bh\', \'fdr_by\']\nprint(f\"{\'Method\':12s}  {\'Rejections\':>11s}  {\'True Pos\':>9s}  {\'False Pos\':>10s}\")\nfor method in methods:\n    reject, p_adj, _, _ = multipletests(raw_p, alpha=0.05, method=method)\n    n_reject = reject.sum()\n    true_pos  = sum(1 for r, d in zip(reject, true_effect) if r and d != 0)\n    false_pos = sum(1 for r, d in zip(reject, true_effect) if r and d == 0)\n    print(f\"{method:12s}  {n_reject:11d}  {true_pos:9d}  {false_pos:10d}\")\n\nprint(f\"\\nUncorrected (p<0.05): {sum(p < 0.05 for p in raw_p)} rejections\")"},
        {"label": "Benjamini-Hochberg step-by-step", "code": "from scipy import stats\nimport numpy as np\n\nnp.random.seed(1)\nn_hypotheses = 15\nalpha = 0.05\n\n# Simulate p-values (mix of true positives and nulls)\ntrue_effects = [0]*10 + [0.7, 0.9, 0.5, 1.2, 0.6]\nraw_p = []\nfor d in true_effects:\n    a = np.random.normal(0, 1, 40)\n    b = np.random.normal(d, 1, 40)\n    _, p = stats.ttest_ind(a, b)\n    raw_p.append(p)\n\n# BH procedure manually\nsorted_idx = np.argsort(raw_p)\nsorted_p   = np.array(raw_p)[sorted_idx]\n\nprint(f\"BH procedure (alpha={alpha}, m={n_hypotheses} tests):\")\nprint(f\"{\'Rank\':>5s}  {\'p-value\':>8s}  {\'BH thresh\':>10s}  {\'Reject?\'}\")\nbh_threshold = alpha * np.arange(1, n_hypotheses+1) / n_hypotheses\nlast_reject  = -1\nfor rank, (p, thr) in enumerate(zip(sorted_p, bh_threshold), 1):\n    if p <= thr:\n        last_reject = rank\n\nfor rank, (p, thr) in enumerate(zip(sorted_p[:8], bh_threshold[:8]), 1):\n    reject = rank <= last_reject\n    print(f\"{rank:5d}  {p:8.4f}  {thr:10.4f}  {reject}\")\nprint(f\"  ... ({n_hypotheses} total)\")\nprint(f\"\\nAll hypotheses with rank <= {last_reject} are rejected ({last_reject} total)\")"},
        {"label": "q-values and FDR estimation", "code": "from statsmodels.stats.multitest import multipletests\nfrom scipy import stats\nimport numpy as np\n\nnp.random.seed(7)\nm = 1000   # large-scale testing (genomics-like)\nn_true = 50\n\n# Generate p-values: 50 true effects + 950 nulls\np_true = np.array([stats.ttest_ind(\n    np.random.normal(0,1,30), np.random.normal(0.6,1,30))[1]\n    for _ in range(n_true)])\np_null = np.random.uniform(0, 1, m - n_true)  # null p-values ~ Uniform\nall_p  = np.concatenate([p_true, p_null])\ntrue_labels = np.array([True]*n_true + [False]*(m-n_true))\n\nresults = {}\nfor method in [\'bonferroni\', \'fdr_bh\']:\n    reject, _, _, _ = multipletests(all_p, alpha=0.05, method=method)\n    tp = (reject & true_labels).sum()\n    fp = (reject & ~true_labels).sum()\n    fn = (~reject & true_labels).sum()\n    fdr = fp / max(reject.sum(), 1)\n    power = tp / n_true\n    results[method] = (reject.sum(), tp, fp, fdr, power)\n    print(f\"{method:12s}: rejections={reject.sum():4d}  TP={tp:3d}  FP={fp:3d}  FDR={fdr:.3f}  Power={power:.3f}\")\n\nprint(f\"\\nSummary: Bonferroni is conservative; BH balances FDR and power\")"}
    ],
"rw_scenario": "A genomics researcher tests differential expression for 5000 genes. Raw analysis finds 450 significant genes (p<0.05); after BH correction at FDR=0.05, only 180 remain — avoiding a list of mostly false discoveries.",
"rw_code": "from statsmodels.stats.multitest import multipletests\nfrom scipy import stats\nimport numpy as np\n\nnp.random.seed(42)\nn_genes = 5000\nn_de    = 150  # truly differentially expressed\n\n# Group A and B expression levels\nexpr_a = np.random.normal(0, 1, (n_genes, 30))\nexpr_b = np.random.normal(0, 1, (n_genes, 30))\n# Inject true effects\neffects = np.random.normal(0.8, 0.3, n_de)\nexpr_b[:n_de] += effects[:, np.newaxis]\n\n# Compute p-values\np_vals = np.array([stats.ttest_ind(expr_a[i], expr_b[i])[1]\n                   for i in range(n_genes)])\n\nfor method in [\'none\', \'bonferroni\', \'fdr_bh\']:\n    if method == \'none\':\n        reject = p_vals < 0.05\n        adj_p  = p_vals\n    else:\n        reject, adj_p, _, _ = multipletests(p_vals, alpha=0.05, method=method)\n\n    tp = reject[:n_de].sum()\n    fp = reject[n_de:].sum()\n    print(f\"{method:12s}: significant={reject.sum():5d}  TP={tp:4d}  FP={fp:4d}  FDR={fp/max(reject.sum(),1):.3f}\")",
"practice": {
    "title": "Multi-Metric A/B Correction",
    "desc": "You ran an A/B test measuring 12 metrics simultaneously (CTR, bounce rate, time on page, conversions, etc.). Generate synthetic p-values for each metric (mix of some truly different and some null). Apply Bonferroni, Holm, BH corrections. For each method, print which metrics are significant. Discuss when you\'d prefer BH over Bonferroni.",
    "starter": "from statsmodels.stats.multitest import multipletests\nimport numpy as np\nfrom scipy import stats\n\nnp.random.seed(42)\nmetrics = [\'CTR\',\'BounceRate\',\'TimeOnPage\',\'Conversions\',\'PageViews\',\n           \'ScrollDepth\',\'CartAdds\',\'Checkout\',\'Revenue\',\'SignUps\',\'ReturnVisits\',\'NPS\']\n\n# Simulate p-values: some metrics truly affected, most not\ntrue_effects = [0.4, 0, 0, 0.6, 0, 0, 0.3, 0.5, 0, 0, 0, 0]\np_values = []\nfor d in true_effects:\n    a = np.random.normal(0, 1, 200)\n    b = np.random.normal(d, 1, 200)\n    _, p = stats.ttest_ind(a, b)\n    p_values.append(p)\n\n# TODO: apply all three corrections\n# TODO: print table showing which metrics are significant under each method\n# TODO: comment on when to prefer BH vs Bonferroni\n"
}
},

{
"title": "24. Bootstrap & Permutation Tests",
"desc": "Bootstrap resampling estimates confidence intervals for any statistic without distributional assumptions. Permutation tests provide exact p-values for two-sample comparisons by shuffling group labels.",
"examples": [
        {"label": "Bootstrap confidence intervals", "code": "import numpy as np\nfrom scipy import stats\n\nnp.random.seed(42)\ndata = np.random.exponential(scale=5, size=50)  # skewed data\n\ndef bootstrap_ci(data, statistic, n_boot=5000, ci=0.95):\n    boots = [statistic(np.random.choice(data, len(data), replace=True))\n             for _ in range(n_boot)]\n    alpha = (1 - ci) / 2\n    return np.percentile(boots, [alpha*100, (1-alpha)*100]), np.array(boots)\n\n# Bootstrap CI for mean, median, and std\nfor stat_name, fn in [(\'mean\', np.mean), (\'median\', np.median), (\'std\', np.std)]:\n    ci_boot, boots = bootstrap_ci(data, fn)\n    # Compare to analytical (where available)\n    print(f\"{stat_name:7s}: obs={fn(data):.3f}  boot_CI=({ci_boot[0]:.3f}, {ci_boot[1]:.3f})\")\n\n# Analytical CI for mean (t-interval)\nci_t = stats.t.interval(0.95, df=len(data)-1, loc=data.mean(), scale=stats.sem(data))\nprint(f\"\\nt-interval CI for mean: ({ci_t[0]:.3f}, {ci_t[1]:.3f})\")\nprint(f\"Boot CI for mean: above  (similar for large n, more robust for skewed)\")"},
        {"label": "Bootstrap for regression coefficients", "code": "import numpy as np\nfrom scipy import stats\n\nnp.random.seed(0)\nn = 80\nx = np.random.randn(n)\ny = 2.5 * x + 1.0 + np.random.randn(n) * 1.5\n\ndef ols(x, y):\n    slope, intercept, *_ = stats.linregress(x, y)\n    return slope, intercept\n\n# Bootstrap CI for slope\nn_boot = 5000\nslopes = []\nfor _ in range(n_boot):\n    idx = np.random.choice(n, n, replace=True)\n    s, _ = ols(x[idx], y[idx])\n    slopes.append(s)\n\nslopes = np.array(slopes)\nci_slope = np.percentile(slopes, [2.5, 97.5])\nobs_slope, obs_int = ols(x, y)\n\nprint(f\"Observed slope:      {obs_slope:.4f}\")\nprint(f\"Bootstrap CI slope:  ({ci_slope[0]:.4f}, {ci_slope[1]:.4f})\")\n\n# Analytical CI from linregress\nresult = stats.linregress(x, y)\nt_crit = stats.t.ppf(0.975, df=n-2)\nse_slope = result.stderr\nprint(f\"Analytical CI slope: ({obs_slope - t_crit*se_slope:.4f}, {obs_slope + t_crit*se_slope:.4f})\")\nprint(f\"Bootstrap SE of slope: {slopes.std():.4f}\")"},
        {"label": "Permutation test for two-sample comparison", "code": "import numpy as np\nfrom scipy import stats\n\nnp.random.seed(42)\n\ndef permutation_test(a, b, n_perm=10000, stat=\'mean_diff\'):\n    obs_stat = a.mean() - b.mean()\n    combined = np.concatenate([a, b])\n    n_a = len(a)\n    perm_stats = []\n    for _ in range(n_perm):\n        shuffled = np.random.permutation(combined)\n        perm_stats.append(shuffled[:n_a].mean() - shuffled[n_a:].mean())\n    perm_stats = np.array(perm_stats)\n    p_val = (np.abs(perm_stats) >= np.abs(obs_stat)).mean()\n    return obs_stat, p_val, perm_stats\n\n# Test on small sample with non-normal data\ngroup_a = np.random.exponential(3, 25)\ngroup_b = np.random.exponential(4, 25)\n\nobs, p_perm, perms = permutation_test(group_a, group_b)\n_, p_mann = stats.mannwhitneyu(group_a, group_b, alternative=\'two-sided\')\n_, p_t    = stats.ttest_ind(group_a, group_b)\n\nprint(f\"Observed mean diff: {obs:.3f}\")\nprint(f\"Permutation p-val:  {p_perm:.4f}\")\nprint(f\"Mann-Whitney p-val: {p_mann:.4f}\")\nprint(f\"t-test p-val:       {p_t:.4f}\")\nprint(f\"Percentile of obs in perm dist: {(perms < obs).mean():.3f}\")"}
    ],
"rw_scenario": "A data scientist bootstraps the median response time for two API versions (non-normal, heavy-tailed). The bootstrap CI for the difference excludes 0, providing strong evidence version B is faster.",
"rw_code": "import numpy as np\nfrom scipy import stats\n\nnp.random.seed(99)\n# API response times (heavy-tailed)\nversion_a = np.random.pareto(2.0, 200) * 100 + 50\nversion_b = np.random.pareto(2.5, 200) * 80  + 45\n\n# Bootstrap CI for difference in medians\nn_boot = 10000\nmedian_diffs = []\nfor _ in range(n_boot):\n    a_boot = np.random.choice(version_a, len(version_a), replace=True)\n    b_boot = np.random.choice(version_b, len(version_b), replace=True)\n    median_diffs.append(np.median(a_boot) - np.median(b_boot))\n\nci = np.percentile(median_diffs, [2.5, 97.5])\nobs_diff = np.median(version_a) - np.median(version_b)\n\nprint(f\"Median A: {np.median(version_a):.2f}ms\")\nprint(f\"Median B: {np.median(version_b):.2f}ms\")\nprint(f\"Observed difference: {obs_diff:.2f}ms\")\nprint(f\"Bootstrap 95% CI: ({ci[0]:.2f}, {ci[1]:.2f})ms\")\nprint(f\"CI excludes 0: {ci[0] > 0 or ci[1] < 0} -> B is {\'faster\' if obs_diff > 0 else \'slower\'}\")",
"practice": {
    "title": "Bootstrap vs Analytical CI Comparison",
    "desc": "Generate 3 datasets: (1) Normal n=30, (2) Exponential n=30, (3) Heavy-tailed Pareto n=30. For each: compute bootstrap 95% CI for the mean (5000 resamples), the analytical t-interval, and the bootstrap CI for the median. Print all three side-by-side. Observe how they differ for non-normal data.",
    "starter": "import numpy as np\nfrom scipy import stats\n\nnp.random.seed(42)\ndatasets = {\n    \'Normal\':    np.random.normal(10, 3, 30),\n    \'Exponential\': np.random.exponential(5, 30),\n    \'Pareto\':    np.random.pareto(1.5, 30) * 5 + 5,\n}\n\ndef bootstrap_ci(data, fn, n_boot=5000):\n    boots = [fn(np.random.choice(data, len(data), replace=True)) for _ in range(n_boot)]\n    return np.percentile(boots, [2.5, 97.5])\n\nfor name, data in datasets.items():\n    boot_mean   = bootstrap_ci(data, np.mean)\n    t_ci        = stats.t.interval(0.95, df=len(data)-1, loc=data.mean(), scale=stats.sem(data))\n    boot_median = bootstrap_ci(data, np.median)\n    print(f\"{name}:\")\n    print(f\"  Bootstrap mean CI:    ({boot_mean[0]:.3f}, {boot_mean[1]:.3f})\")\n    # TODO: print t-interval and bootstrap median CI\n"
}
},

]  # end SECTIONS


# ─── Build outputs ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # HTML
    html_path = BASE / "index.html"
    html_path.write_text(make_html(SECTIONS), encoding="utf-8")

    # Notebook
    nb_path = BASE / "study_guide.ipynb"
    nb = make_nb(SECTIONS)
    nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")

    n_cells = len(nb["cells"])
    print(f"Statistics guide created: {BASE}")
    print(f"  index.html:        {html_path.stat().st_size/1024:.1f} KB")
    print(f"  study_guide.ipynb: {n_cells} cells")
