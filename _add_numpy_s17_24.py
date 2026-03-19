"""Add sections 17-24 to gen_numpy.py."""
import sys
sys.path.insert(0, r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
from _inserter import insert_sections

FILE   = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_numpy.py"
MARKER = "]  # end SECTIONS"

def ec(code):
    return (code.replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace("'", "\\'"))

def make_np(num, title, desc, examples, rw_title, rw_scenario, rw_code, pt, pd_text, ps):
    ex_lines = []
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples) - 1 else ''
        ex_lines.append(
            f'        {{"label": "{ec(ex["label"])}", "code": "{ec(ex["code"])}"}}{comma}'
        )
    ex_block = '\n'.join(ex_lines)
    return (
        f'    {{\n'
        f'    "title": "{num}. {title}",\n'
        f'    "desc": "{ec(desc)}",\n'
        f'    "examples": [\n{ex_block}\n    ],\n'
        f'    "rw": {{\n'
        f'        "title": "{ec(rw_title)}",\n'
        f'        "scenario": "{ec(rw_scenario)}",\n'
        f'        "code": "{ec(rw_code)}"\n'
        f'    }},\n'
        f'    "practice": {{\n'
        f'        "title": "{ec(pt)}",\n'
        f'        "desc": "{ec(pd_text)}",\n'
        f'        "starter": "{ec(ps)}"\n'
        f'    }}\n'
        f'    }},\n\n'
    )

# ── Section 17: Sorting, Searching & Partitioning ───────────────────────────
s17 = make_np(17, "Sorting, Searching & Partitioning",
    "NumPy's sort, argsort, searchsorted, and partition give O(n log n) and O(n) ordering operations that operate on arrays without Python loops.",
    [
        {"label": "sort and argsort",
         "code":
"""import numpy as np

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# sort: returns sorted copy
sorted_arr = np.sort(arr)
print("sorted:", sorted_arr)

# argsort: indices that would sort the array
idx = np.argsort(arr)
print("argsort:", idx)
print("verify:", arr[idx])   # same as sorted_arr

# Sort along an axis (2D)
m = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])
print("row-wise sort:\\n", np.sort(m, axis=1))
print("col-wise sort:\\n", np.sort(m, axis=0))

# Stable sort for multi-key sorting
records = np.array([(2, 'b'), (1, 'a'), (2, 'a'), (1, 'b')],
                   dtype=[('key', int), ('val', 'U1')])
records.sort(order=['key', 'val'])
print("multi-key sort:", records)"""},
        {"label": "argmin, argmax, searchsorted",
         "code":
"""import numpy as np

data = np.array([10, 5, 8, 3, 15, 7, 2, 12])

print("min:", data.min(), "at index:", data.argmin())
print("max:", data.max(), "at index:", data.argmax())

# 2D: axis parameter
m = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])
print("argmin per row:", m.argmin(axis=1))   # [1, 0, 0]
print("argmax per col:", m.argmax(axis=0))   # [0, 2, 1]

# searchsorted: binary search in sorted array (O(log n))
sorted_data = np.array([1, 3, 5, 7, 9, 11, 13])
vals = np.array([0, 3, 6, 14])

# 'left': index where val would be inserted to keep sorted
left_idx  = np.searchsorted(sorted_data, vals, side='left')
right_idx = np.searchsorted(sorted_data, vals, side='right')
print("left insert positions:", left_idx)
print("right insert positions:", right_idx)

# Use case: check if value exists
def is_in_sorted(arr, vals):
    idx = np.searchsorted(arr, vals)
    return (idx < len(arr)) & (arr[np.minimum(idx, len(arr)-1)] == vals)

print("vals in array:", is_in_sorted(sorted_data, vals))"""},
        {"label": "partition and argpartition (O(n) top-k)",
         "code":
"""import numpy as np

np.random.seed(42)
scores = np.random.randint(0, 100, size=20)
print("Scores:", scores)

# partition: rearrange so k-th element is in sorted position
# Elements left of k are <= arr[k], right are >= arr[k]
k = 5
partitioned = np.partition(scores, k)
print(f"After partition(k={k}): {partitioned}")
print(f"Element at k={k}: {partitioned[k]} (this is the {k+1}th smallest)")

# Get top-5 scores (not sorted — just the 5 largest)
top5_idx  = np.argpartition(scores, -5)[-5:]
top5_vals = scores[top5_idx]
print(f"Top-5 values (unsorted): {top5_vals}")
print(f"Top-5 values (sorted):   {np.sort(top5_vals)[::-1]}")

# Bottom-5 (smallest)
bot5_idx  = np.argpartition(scores, 5)[:5]
bot5_vals = scores[bot5_idx]
print(f"Bottom-5 values: {np.sort(bot5_vals)}")

# Speed comparison concept: partition is O(n), sort is O(n log n)
# For finding top-k from 1M elements, argpartition is much faster"""}
    ],
    rw_title="Ranking Sales Reps",
    rw_scenario="A sales dashboard needs to rank 10,000 reps by revenue but only display the top 100, using argpartition for O(n) efficiency instead of a full sort.",
    rw_code=
"""import numpy as np

np.random.seed(42)
n_reps = 10_000
rep_ids = np.arange(n_reps)
revenues = np.random.lognormal(mean=10, sigma=1.5, size=n_reps)

K = 100  # top 100 reps

# Efficient: O(n) to get top-K indices, O(K log K) to sort only those
top_k_idx = np.argpartition(revenues, -K)[-K:]
top_k_sorted = top_k_idx[np.argsort(revenues[top_k_idx])[::-1]]

print("Top 10 reps:")
for rank, idx in enumerate(top_k_sorted[:10], 1):
    print(f"  Rank {rank:3d}: Rep #{rep_ids[idx]:5d} | Revenue: ${revenues[idx]:>12,.0f}")

# Percentile ranks using searchsorted
sorted_rev = np.sort(revenues)
sample_rev = np.array([50_000, 100_000, 500_000])
pct_ranks  = np.searchsorted(sorted_rev, sample_rev) / n_reps * 100
for rev, pct in zip(sample_rev, pct_ranks):
    print(f"  ${rev:>8,} is at the {pct:.1f}th percentile")""",
    pt="Top-K Selector",
    pd_text="Write a function top_k_products(sales, k) that takes a 2D array (rows=products, cols=days) and returns the indices of the k products with the highest total sales. Use argpartition for efficiency. Also write bottom_k_days(sales, k) that returns the k days (columns) with lowest average sales across all products.",
    ps=
"""import numpy as np

def top_k_products(sales, k):
    # Sum across days (axis=1), then use argpartition
    totals = sales.sum(axis=1)
    idx = np.argpartition(totals, -k)[-k:]
    return idx[np.argsort(totals[idx])[::-1]]

def bottom_k_days(sales, k):
    # Mean across products (axis=0), then argpartition
    daily_avg = sales.mean(axis=0)
    idx = np.argpartition(daily_avg, k)[:k]
    return idx[np.argsort(daily_avg[idx])]

np.random.seed(42)
sales = np.random.poisson(100, (50, 30))   # 50 products, 30 days
top3  = top_k_products(sales, 3)
bot3  = bottom_k_days(sales, 3)
print("Top 3 products (by total):", top3, "->", sales[top3].sum(axis=1))
print("Worst 3 days (by avg):   ", bot3, "->", sales[:, bot3].mean(axis=0).round(1))
"""
)

# ── Section 18: Set Operations on Arrays ────────────────────────────────────
s18 = make_np(18, "Set Operations on Arrays",
    "NumPy provides unique(), union1d(), intersect1d(), setdiff1d(), and in1d()/isin() for fast set-like operations on 1D arrays using sorted-array algorithms.",
    [
        {"label": "unique and value counts",
         "code":
"""import numpy as np

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])

# unique: sorted unique values
u = np.unique(arr)
print("unique:", u)

# return_counts: how many times each value appears
vals, counts = np.unique(arr, return_counts=True)
print("value counts:")
for v, c in zip(vals, counts):
    print(f"  {v}: {c}")

# return_index: first occurrence index
vals, idx = np.unique(arr, return_index=True)
print("first occurrence indices:", idx)

# return_inverse: reconstruct original from unique
vals, inv = np.unique(arr, return_inverse=True)
print("unique:", vals)
print("inverse:", inv)
print("reconstructed:", vals[inv])  # should match arr

# Most common value (mode-like)
mode_val = vals[np.argmax(counts)]
print(f"Mode: {mode_val} (appears {counts.max()} times)")"""},
        {"label": "union1d, intersect1d, setdiff1d, setxor1d",
         "code":
"""import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([3, 4, 5, 6, 7])

print("union (a | b):      ", np.union1d(a, b))
print("intersect (a & b):  ", np.intersect1d(a, b))
print("a - b (in a not b): ", np.setdiff1d(a, b))
print("b - a (in b not a): ", np.setdiff1d(b, a))
print("symmetric diff:     ", np.setxor1d(a, b))

# With return_indices for intersect
common, a_idx, b_idx = np.intersect1d(a, b, return_indices=True)
print("Common:", common, "at a:", a_idx, "at b:", b_idx)

# Practical: find new customers
old_customers = np.array([101, 102, 103, 104, 105])
new_customers = np.array([103, 104, 106, 107, 108])
returning = np.intersect1d(old_customers, new_customers)
brand_new = np.setdiff1d(new_customers, old_customers)
churned   = np.setdiff1d(old_customers, new_customers)
print(f"Returning: {returning}")
print(f"Brand new: {brand_new}")
print(f"Churned:   {churned}")"""},
        {"label": "isin / in1d for membership testing",
         "code":
"""import numpy as np

products = np.array(['apple', 'banana', 'cherry', 'date', 'elderberry'])
blacklist = np.array(['banana', 'date', 'fig'])

# isin: element-wise membership test
mask = np.isin(products, blacklist)
print("Is in blacklist:", mask)
print("Allowed products:", products[~mask])
print("Blocked products:", products[mask])

# Large-scale membership test (much faster than Python loops)
np.random.seed(42)
user_ids      = np.arange(1_000_000)
premium_users = np.random.choice(user_ids, size=50_000, replace=False)

# Check a sample of 1000 users
sample = np.random.choice(user_ids, size=1000, replace=False)
is_premium = np.isin(sample, premium_users)
print(f"Sample size: {len(sample)}, Premium users in sample: {is_premium.sum()}")

# in1d is equivalent (older API)
same_result = np.in1d(sample, premium_users)
print("isin == in1d:", np.all(is_premium == same_result))

# Invert: users NOT in premium
non_premium = sample[~is_premium]
print(f"Non-premium in sample: {len(non_premium)}")"""}
    ],
    rw_title="Inventory Reconciliation",
    rw_scenario="A warehouse system compares today's scan vs expected manifest using NumPy set operations to find missing, extra, and duplicate items instantly across 100K SKUs.",
    rw_code=
"""import numpy as np

np.random.seed(42)
manifest = np.random.choice(np.arange(200_000), size=100_000, replace=False)

# Simulate scanning: miss 500, add 300 unexpected
missed_idx   = np.random.choice(len(manifest), size=500, replace=False)
extra_skus   = np.random.randint(200_000, 201_000, size=300)
scanned      = np.concatenate([np.delete(manifest, missed_idx), extra_skus])

manifest_u = np.unique(manifest)
scanned_u  = np.unique(scanned)

missing      = np.setdiff1d(manifest_u, scanned_u)
unexpected   = np.setdiff1d(scanned_u, manifest_u)
confirmed    = np.intersect1d(manifest_u, scanned_u)

# Duplicates in scan
vals, counts = np.unique(scanned, return_counts=True)
duplicates   = vals[counts > 1]

print(f"Manifest:    {len(manifest_u):,} SKUs")
print(f"Scanned:     {len(scanned_u):,} unique SKUs")
print(f"Confirmed:   {len(confirmed):,} ({len(confirmed)/len(manifest_u):.1%})")
print(f"Missing:     {len(missing):,}")
print(f"Unexpected:  {len(unexpected):,}")
print(f"Duplicates:  {len(duplicates):,}")
print(f"Accuracy:    {len(confirmed)/len(manifest_u):.2%}")""",
    pt="Cohort Analysis",
    pd_text="Write a function cohort_analysis(cohorts: dict) where cohorts maps week labels to user_id arrays. For each week, compute: (1) new users (not seen in any previous week), (2) returning users (seen in at least one previous week), (3) churned from previous week. Return a list of dicts with these counts.",
    ps=
"""import numpy as np

def cohort_analysis(cohorts):
    results = []
    seen_so_far = np.array([], dtype=int)
    prev_week   = np.array([], dtype=int)

    for week, users in sorted(cohorts.items()):
        users = np.unique(users)
        new_users  = np.setdiff1d(users, seen_so_far)
        returning  = np.intersect1d(users, seen_so_far)
        churned    = np.setdiff1d(prev_week, users)

        results.append({
            "week": week, "total": len(users),
            "new": len(new_users), "returning": len(returning),
            "churned_from_prev": len(churned),
        })
        seen_so_far = np.union1d(seen_so_far, users)
        prev_week   = users
    return results

np.random.seed(42)
cohorts = {
    "W1": np.random.randint(0, 100, 50),
    "W2": np.random.randint(20, 120, 60),
    "W3": np.random.randint(40, 140, 55),
    "W4": np.random.randint(60, 160, 70),
}
for r in cohort_analysis(cohorts):
    print(r)
"""
)

# ── Section 19: Numerical Stability, NaN & Inf Handling ─────────────────────
s19 = make_np(19, "Numerical Stability, NaN & Inf Handling",
    "Floating-point arithmetic has precision limits, NaN propagation, and overflow. NumPy provides tools to detect, mask, and safely handle these edge cases.",
    [
        {"label": "NaN detection and handling",
         "code":
"""import numpy as np

data = np.array([1.0, 2.0, np.nan, 4.0, np.nan, 6.0])

# Detection
print("isnan:", np.isnan(data))
print("Count NaNs:", np.isnan(data).sum())
print("Any NaN:", np.any(np.isnan(data)))

# NaN-safe aggregations
print("mean with NaN:", np.mean(data))          # nan
print("nanmean:", np.nanmean(data))              # 3.25
print("nansum:", np.nansum(data))               # 13.0
print("nanstd:", np.nanstd(data).round(4))
print("nanmin/nanmax:", np.nanmin(data), np.nanmax(data))

# Replace NaN
filled_mean = np.where(np.isnan(data), np.nanmean(data), data)
print("NaN -> mean:", filled_mean)

filled_zero = np.nan_to_num(data, nan=0.0)
print("NaN -> 0:   ", filled_zero)

# Forward fill (pandas-style, pure numpy)
def ffill(arr):
    mask = np.isnan(arr)
    idx = np.where(~mask, np.arange(len(arr)), 0)
    np.maximum.accumulate(idx, out=idx)
    return arr[idx]

print("Forward fill:", ffill(data))"""},
        {"label": "Inf, overflow, and finfo",
         "code":
"""import numpy as np

# Infinity
x = np.array([1.0, -1.0, 0.0, np.inf, -np.inf, np.nan])
print("isinf:", np.isinf(x))
print("isfinite:", np.isfinite(x))
print("isnan:", np.isnan(x))

# All-in-one
print("Any problem:", ~np.isfinite(x).all())

# Replace inf with large values
clean = np.nan_to_num(x, nan=0.0, posinf=1e9, neginf=-1e9)
print("Cleaned:", clean)

# Overflow
float32 = np.float32(1e38)
print("float32 * 100:", float32 * 100)     # inf
print("float32 dtype max:", np.finfo(np.float32).max)

# Machine epsilon
for dtype in [np.float16, np.float32, np.float64]:
    fi = np.finfo(dtype)
    print(f"{dtype.__name__:10s}: eps={fi.eps:.2e}, max={fi.max:.2e}")

# Division edge cases
print("0/0:", np.float64(0) / np.float64(0))  # nan
print("1/0:", np.float64(1) / np.float64(0))  # inf"""},
        {"label": "Numerical precision and stable computations",
         "code":
"""import numpy as np

# Floating-point is NOT exact
a = 0.1 + 0.2
print("0.1 + 0.2 ==  0.3:", a == 0.3)     # False!
print("value:", repr(a))
print("allclose:", np.isclose(a, 0.3))     # True (with tolerance)

# np.isclose with tolerances
x = np.array([1.0, 1.0 + 1e-8, 1.0 + 1e-5, 1.1])
print("isclose to 1.0:", np.isclose(x, 1.0, rtol=1e-5, atol=1e-8))

# Unstable: sum of large+small+large
big  = np.float32(1e8)
tiny = np.float32(1.0)
print("float32 (1e8 + 1 - 1e8):", big + tiny - big)  # may be 0!

# Kahan compensated summation is more stable
# np.sum uses pairwise summation which is better than naive
x = np.random.randn(1_000_000).astype(np.float32)
naive_sum = float(x[0])
for v in x[1:]:
    naive_sum += float(v)

np_sum = float(np.sum(x, dtype=np.float64))  # promote to float64
print(f"Naive float32 sum: {naive_sum:.4f}")
print(f"NumPy float64 sum: {np_sum:.4f}")

# Log-sum-exp trick for numerical stability (important in ML)
logits = np.array([1000.0, 1001.0, 999.0])  # would overflow exp()
lse = logits.max() + np.log(np.sum(np.exp(logits - logits.max())))
print(f"Log-sum-exp (stable): {lse:.6f}")"""}
    ],
    rw_title="Financial Return Calculator",
    rw_scenario="A risk system computes daily returns from price series that contain missing quotes (NaN), halted trading (0), and data errors (negative prices).",
    rw_code=
"""import numpy as np

np.random.seed(42)
n_days = 252
prices = 100 * np.exp(np.cumsum(np.random.randn(n_days) * 0.01))

# Inject data quality issues
prices[10]  = np.nan    # missing quote
prices[50]  = 0.0       # trading halt
prices[100] = -5.0      # data error

def clean_prices(prices):
    p = prices.copy()
    # Remove physically impossible values
    p[p <= 0] = np.nan
    # Forward-fill NaN
    mask = np.isnan(p)
    idx  = np.where(~mask, np.arange(len(p)), 0)
    np.maximum.accumulate(idx, out=idx)
    p = p[idx]
    return p

def daily_returns(prices):
    p = clean_prices(prices)
    rets = np.diff(p) / p[:-1]
    rets = rets[np.isfinite(rets)]
    return rets

rets = daily_returns(prices)
print(f"Days cleaned: {np.isnan(prices).sum() + (prices <= 0).sum()}")
print(f"Valid returns: {len(rets)}")
print(f"Mean return: {np.nanmean(rets):.4%}")
print(f"Volatility:  {np.nanstd(rets):.4%}")
print(f"Sharpe (approx): {np.nanmean(rets)/np.nanstd(rets)*np.sqrt(252):.2f}")""",
    pt="Stable Softmax",
    pd_text="Implement stable_softmax(x) that computes softmax using the log-sum-exp trick to avoid overflow. Implement log_softmax(x) using the same trick. Verify both give the same probabilities on x = [1000, 1001, 999] and x = [-1000, -999, -1001]. Compare against naive softmax to show instability.",
    ps=
"""import numpy as np

def naive_softmax(x):
    e = np.exp(x)
    return e / e.sum()

def stable_softmax(x):
    # TODO: subtract max(x) before exp, then normalize
    pass

def log_softmax(x):
    # TODO: return log of stable softmax (more numerically stable version)
    # hint: x - max(x) - log(sum(exp(x - max(x))))
    pass

for x in [np.array([1.0, 2.0, 3.0]),
          np.array([1000.0, 1001.0, 999.0]),
          np.array([-1000.0, -999.0, -1001.0])]:
    print(f"x = {x}")
    print(f"  naive:  {naive_softmax(x)}")
    print(f"  stable: {stable_softmax(x)}")
    print(f"  log:    {log_softmax(x)}")
    print(f"  exp(log) == stable: {np.allclose(np.exp(log_softmax(x)), stable_softmax(x))}")
"""
)

# ── Section 20: Probability Distributions & Random Sampling ─────────────────
s20 = make_np(20, "Probability Distributions & Random Sampling",
    "NumPy's random module (Generator API) provides reproducible random sampling from dozens of distributions. Essential for simulations, bootstrapping, and synthetic data.",
    [
        {"label": "Generator API and reproducibility",
         "code":
"""import numpy as np

# Modern API: use default_rng (preferred over np.random.seed)
rng = np.random.default_rng(seed=42)

# Uniform
u = rng.uniform(low=0, high=10, size=5)
print("uniform:", u.round(2))

# Integers
dice = rng.integers(1, 7, size=10)
print("dice rolls:", dice)

# Shuffle and choice
items = np.arange(10)
rng.shuffle(items)
print("shuffled:", items)

sample = rng.choice(items, size=5, replace=False)
print("sample without replacement:", sample)

# Weighted choice
weights  = np.array([0.5, 0.3, 0.2])
outcomes = np.array(['A', 'B', 'C'])
draws    = rng.choice(outcomes, size=20, p=weights)
vals, counts = np.unique(draws, return_counts=True)
print("Weighted draws:", dict(zip(vals, counts)))

# Verify reproducibility
rng2 = np.random.default_rng(seed=42)
print("Same sequence:", np.all(rng2.uniform(size=5) == np.random.default_rng(42).uniform(size=5)))"""},
        {"label": "Statistical distributions",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Normal distribution
heights = rng.normal(loc=170, scale=10, size=10_000)
print(f"Normal(170, 10): mean={heights.mean():.2f}, std={heights.std():.2f}")

# Lognormal (for prices, incomes)
prices = rng.lognormal(mean=3.0, sigma=0.5, size=5000)
print(f"Lognormal: median={np.median(prices):.2f}, mean={prices.mean():.2f}")

# Exponential (wait times, inter-arrivals)
wait_times = rng.exponential(scale=5.0, size=1000)  # mean = 5 min
print(f"Exponential(lambda=0.2): mean={wait_times.mean():.2f}")

# Poisson (event counts)
requests_per_sec = rng.poisson(lam=30, size=60)  # 30 req/s for 1 min
print(f"Poisson(30): mean={requests_per_sec.mean():.1f}, std={requests_per_sec.std():.1f}")

# Binomial (successes in n trials)
successes = rng.binomial(n=100, p=0.35, size=1000)  # conversion rate
print(f"Binomial(100, 0.35): mean={successes.mean():.1f} (expected 35)")

# Beta (probabilities, proportions)
click_rates = rng.beta(a=2, b=5, size=1000)
print(f"Beta(2, 5): mean={click_rates.mean():.3f} (expected {2/(2+5):.3f})")"""},
        {"label": "Bootstrap sampling and Monte Carlo",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Bootstrap confidence interval
data = np.array([2.3, 4.1, 3.8, 5.2, 2.9, 4.7, 3.5, 6.1, 2.8, 4.4])

n_boot = 10_000
boot_means = np.array([
    rng.choice(data, size=len(data), replace=True).mean()
    for _ in range(n_boot)
])

ci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])
print(f"Sample mean: {data.mean():.3f}")
print(f"95% bootstrap CI: [{ci_low:.3f}, {ci_high:.3f}]")

# Monte Carlo Pi estimation
N = 1_000_000
x = rng.uniform(-1, 1, N)
y = rng.uniform(-1, 1, N)
inside = (x**2 + y**2) <= 1.0
pi_est = 4 * inside.mean()
print(f"Pi estimate (N={N:,}): {pi_est:.5f} (true: {np.pi:.5f})")

# Simulate portfolio returns (Monte Carlo)
n_assets, n_sims, n_days = 5, 10_000, 252
mu    = rng.uniform(0.0001, 0.001, n_assets)   # daily expected return
sigma = rng.uniform(0.01, 0.03, n_assets)       # daily vol
daily_rets = rng.normal(mu, sigma, (n_sims, n_days, n_assets))
port_rets  = daily_rets.mean(axis=2).sum(axis=1)  # equal weight
var_95 = np.percentile(port_rets, 5)
print(f"Portfolio annual return mean: {port_rets.mean():.2%}")
print(f"VaR 95%: {var_95:.2%}")"""}
    ],
    rw_title="A/B Test Simulation",
    rw_scenario="A product team uses bootstrap simulation to determine whether a 2-percentage-point conversion rate improvement is statistically significant given their sample sizes.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)

# Observed data
n_control    = 5000
n_treatment  = 5000
conv_control = 0.10   # 10% baseline
conv_treat   = 0.12   # 12% treatment (absolute +2pp)

# Sample from observed proportions
control   = rng.binomial(1, conv_control, n_control)
treatment = rng.binomial(1, conv_treat,   n_treatment)

obs_diff = treatment.mean() - control.mean()
print(f"Observed difference: {obs_diff:.4f} ({obs_diff:.2%})")

# Permutation test
N_PERM = 10_000
combined = np.concatenate([control, treatment])
perm_diffs = np.empty(N_PERM)
for i in range(N_PERM):
    rng.shuffle(combined)
    perm_diffs[i] = combined[:n_treatment].mean() - combined[n_treatment:].mean()

p_value = (np.abs(perm_diffs) >= np.abs(obs_diff)).mean()
print(f"Permutation test p-value: {p_value:.4f}")
print(f"Significant at alpha=0.05: {p_value < 0.05}")

ci = np.percentile(perm_diffs, [2.5, 97.5])
print(f"Null distribution 95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]")""",
    pt="Distribution Fitter",
    pd_text="Write fit_normal(data) that uses np.mean and np.std to estimate parameters, then generates n_samples from that distribution and computes the KS-like statistic (max absolute difference between sorted empirical CDF and normal CDF). Also write simulate_geometric_brownian(S0, mu, sigma, T, n_steps) for stock price simulation.",
    ps=
"""import numpy as np

def fit_normal(data, n_samples=1000, seed=42):
    rng = np.random.default_rng(seed)
    mu  = np.mean(data)
    std = np.std(data, ddof=1)
    # Generate from fitted distribution
    synthetic = rng.normal(mu, std, n_samples)
    # Empirical CDF comparison
    emp  = np.sort(data)
    emp_cdf = np.arange(1, len(emp)+1) / len(emp)
    # Normal CDF at emp points: use error function approximation
    from math import erf
    norm_cdf = np.array([0.5 * (1 + erf((x-mu)/(std*2**0.5))) for x in emp])
    ks_stat  = np.max(np.abs(emp_cdf - norm_cdf))
    return {"mu": mu, "std": std, "ks": ks_stat, "synthetic": synthetic}

def simulate_gbm(S0, mu, sigma, T, n_steps, seed=42):
    rng = np.random.default_rng(seed)
    dt  = T / n_steps
    Z   = rng.standard_normal(n_steps)
    # TODO: compute log returns and cumulative prices
    pass

rng = np.random.default_rng(42)
data = rng.normal(50, 10, 200)
result = fit_normal(data)
print(f"Fitted: mu={result['mu']:.2f}, std={result['std']:.2f}, KS={result['ks']:.4f}")
"""
)

# ── Section 21: Image Arrays & 2D Operations ─────────────────────────────────
s21 = make_np(21, "Image Arrays & 2D Operations",
    "Images are 2D (grayscale) or 3D (H x W x C) NumPy arrays. Understanding array operations on images builds intuition for convolutions, pooling, and data augmentation.",
    [
        {"label": "Image as array: channels and pixel operations",
         "code":
"""import numpy as np

# Images are (H, W) for grayscale, (H, W, C) for color
np.random.seed(42)
H, W = 64, 64

# Synthetic grayscale (0-255 uint8)
gray = np.random.randint(0, 256, (H, W), dtype=np.uint8)
print(f"Grayscale shape: {gray.shape}, dtype: {gray.dtype}")
print(f"Pixel range: [{gray.min()}, {gray.max()}]")

# Synthetic RGB image
rgb = np.random.randint(0, 256, (H, W, 3), dtype=np.uint8)
print(f"RGB shape: {rgb.shape}")

# Extract channels
R, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
print(f"R channel mean: {R.mean():.1f}")

# RGB to grayscale (luminosity formula)
gray_from_rgb = (0.2989 * R + 0.5870 * G + 0.1140 * B).astype(np.uint8)
print(f"Converted gray shape: {gray_from_rgb.shape}")

# Normalize to [0, 1] float
img_float = rgb.astype(np.float32) / 255.0
print(f"Normalized range: [{img_float.min():.3f}, {img_float.max():.3f}]")

# Crop a region
crop = rgb[10:40, 15:50, :]
print(f"Crop shape: {crop.shape}")

# Horizontal flip
flipped = rgb[:, ::-1, :]
print(f"Flipped shape: {flipped.shape}")"""},
        {"label": "Convolution and pooling with strides",
         "code":
"""import numpy as np

def convolve2d(img, kernel):
    H, W = img.shape
    kH, kW = kernel.shape
    pad_h, pad_w = kH // 2, kW // 2
    # Zero-pad
    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    output = np.zeros_like(img, dtype=float)
    for i in range(H):
        for j in range(W):
            output[i, j] = (padded[i:i+kH, j:j+kW] * kernel).sum()
    return output

# Faster with stride_tricks (no Python loop)
def convolve2d_fast(img, kernel):
    from numpy.lib.stride_tricks import sliding_window_view
    H, W = img.shape
    kH, kW = kernel.shape
    pad_h, pad_w = kH // 2, kW // 2
    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    windows = sliding_window_view(padded, (kH, kW))
    return (windows * kernel).sum(axis=(-2, -1))

img = np.random.rand(32, 32)
# Edge detection kernel (Sobel-like)
sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
edges = convolve2d_fast(img, sobel_x)
print(f"Edge response range: [{edges.min():.3f}, {edges.max():.3f}]")

# Max pooling (2x2)
def max_pool2d(img, size=2):
    H, W = img.shape
    pH, pW = H // size, W // size
    return img[:pH*size, :pW*size].reshape(pH, size, pW, size).max(axis=(1, 3))

pooled = max_pool2d(img, 2)
print(f"After 2x2 max pool: {img.shape} -> {pooled.shape}")"""},
        {"label": "Data augmentation with NumPy",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

def augment_batch(images, rng):
    # Augment a batch of images (N, H, W, C).
    batch = images.copy().astype(np.float32)

    # Random horizontal flip (50% chance per image)
    flip_mask = rng.random(len(batch)) > 0.5
    batch[flip_mask] = batch[flip_mask, :, ::-1, :]

    # Random brightness adjustment
    brightness = rng.uniform(0.8, 1.2, (len(batch), 1, 1, 1))
    batch = np.clip(batch * brightness, 0, 255)

    # Random crop and resize (simplified: just crop to 80% size)
    H, W = batch.shape[1:3]
    ch, cw = int(H * 0.8), int(W * 0.8)
    for i in range(len(batch)):
        y0 = rng.integers(0, H - ch)
        x0 = rng.integers(0, W - cw)
        # In real pipeline you would resize; here just show crop
        batch[i, :ch, :cw, :] = batch[i, y0:y0+ch, x0:x0+cw, :]

    # Gaussian noise
    noise = rng.normal(0, 5, batch.shape)
    batch = np.clip(batch + noise, 0, 255)

    return batch.astype(np.uint8)

# Demo
N, H, W, C = 8, 64, 64, 3
batch = rng.integers(50, 200, (N, H, W, C), dtype=np.uint8)
augmented = augment_batch(batch, rng)
print(f"Batch: {batch.shape} | Augmented: {augmented.shape}")
print(f"Orig mean: {batch.mean():.1f} | Aug mean: {augmented.mean():.1f}")"""}
    ],
    rw_title="Batch Preprocessing Pipeline",
    rw_scenario="A CNN training loop preprocesses a batch of 64x64 RGB images: normalize per-channel, apply random augmentation, and flatten into model input.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)
N, H, W, C = 32, 64, 64, 3

# Simulate a batch
batch = rng.integers(0, 256, (N, H, W, C), dtype=np.uint8)

# ImageNet-style normalization (per-channel mean/std)
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD  = np.array([0.229, 0.224, 0.225], dtype=np.float32)

def preprocess(batch):
    x = batch.astype(np.float32) / 255.0  # [0,1]
    x = (x - MEAN) / STD                  # normalize
    x = x.transpose(0, 3, 1, 2)           # NHWC -> NCHW for PyTorch
    return x

# Random horizontal flip augmentation
def random_hflip(batch, rng, p=0.5):
    mask = rng.random(len(batch)) < p
    out  = batch.copy()
    out[mask] = batch[mask, :, ::-1, :]
    return out

processed = preprocess(random_hflip(batch, rng))
print(f"Input: {batch.shape} uint8")
print(f"Output: {processed.shape} float32")
print(f"Channel 0: mean={processed[:,0,:,:].mean():.3f}, std={processed[:,0,:,:].std():.3f}")""",
    pt="Image Statistics",
    pd_text="Write a function image_stats(img) that takes a (H,W,3) uint8 image and returns a dict with per-channel mean, std, min, max, and the percentage of 'near-white' pixels (all channels > 200) and 'near-black' pixels (all channels < 55). Also write normalize_contrast(img) that maps pixel values to [0,255] using min-max normalization per channel.",
    ps=
"""import numpy as np

def image_stats(img):
    # img is (H, W, 3) uint8
    stats = {}
    for c, name in enumerate(['R', 'G', 'B']):
        ch = img[:, :, c].astype(float)
        stats[name] = {"mean": ch.mean(), "std": ch.std(),
                       "min": int(ch.min()), "max": int(ch.max())}
    # Near white: all channels > 200
    near_white = (img > 200).all(axis=2)
    # Near black: all channels < 55
    near_black = (img < 55).all(axis=2)
    stats["near_white_pct"] = near_white.mean() * 100
    stats["near_black_pct"] = near_black.mean() * 100
    return stats

def normalize_contrast(img):
    # TODO: for each channel, map min->0, max->255
    out = np.empty_like(img, dtype=np.uint8)
    for c in range(3):
        ch = img[:, :, c].astype(float)
        lo, hi = ch.min(), ch.max()
        if hi > lo:
            out[:, :, c] = ((ch - lo) / (hi - lo) * 255).astype(np.uint8)
        else:
            out[:, :, c] = 0
    return out

rng = np.random.default_rng(42)
img = rng.integers(0, 256, (128, 128, 3), dtype=np.uint8)
stats = image_stats(img)
for k, v in stats.items():
    print(f"{k}: {v}")
normed = normalize_contrast(img)
print("Normalized range:", normed.min(), normed.max())
"""
)

# ── Section 22: Statistical Aggregations ─────────────────────────────────────
s22 = make_np(22, "Statistical Aggregations",
    "NumPy provides percentiles, histograms, correlation, and covariance for descriptive statistics. These underpin nearly all data analysis workflows.",
    [
        {"label": "Percentile, quantile, and descriptive stats",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)
data = rng.lognormal(mean=4.5, sigma=0.8, size=10_000)

# Percentiles and quantiles
p25, p50, p75 = np.percentile(data, [25, 50, 75])
print(f"Q1={p25:.1f}, Median={p50:.1f}, Q3={p75:.1f}")
print(f"IQR={p75-p25:.1f}")

# Quantile (equivalent but takes fractions 0-1)
q  = np.quantile(data, [0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1.0])
labels = ["0%", "25%", "50%", "75%", "90%", "95%", "99%", "100%"]
for l, v in zip(labels, q):
    print(f"  {l:>4s}: {v:>8.1f}")

# Outlier detection via IQR
iqr_mult = 1.5
lower = p25 - iqr_mult * (p75 - p25)
upper = p75 + iqr_mult * (p75 - p25)
outliers = data[(data < lower) | (data > upper)]
print(f"Outliers: {len(outliers)} ({len(outliers)/len(data):.1%})")

# 2D: percentile per column
m = rng.normal(0, 1, (100, 5))
col_medians = np.median(m, axis=0)
print("Col medians:", col_medians.round(2))"""},
        {"label": "Histogram and frequency analysis",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)
data = np.concatenate([rng.normal(30, 5, 3000),   # young cohort
                       rng.normal(55, 8, 2000)])   # senior cohort

# Basic histogram
counts, edges = np.histogram(data, bins=20)
centers = (edges[:-1] + edges[1:]) / 2
print("Histogram (first 5 bins):")
for c, n in zip(centers[:5], counts[:5]):
    print(f"  {c:.1f}: {'#' * (n//50)} ({n})")

# Normalized (density)
density, _ = np.histogram(data, bins=20, density=True)
print(f"Density sums to: {density.sum() * np.diff(edges).mean():.4f}")  # ~1.0

# 2D histogram
x = rng.normal(0, 1, 5000)
y = 0.7 * x + rng.normal(0, 0.5, 5000)  # correlated
counts_2d, xedges, yedges = np.histogram2d(x, y, bins=10)
print(f"2D histogram shape: {counts_2d.shape}")
print(f"Peak bin count: {counts_2d.max():.0f}")

# Digitize: assign each value to a bin
salary_bins = np.array([0, 30_000, 60_000, 100_000, 200_000, np.inf])
labels = ['entry', 'junior', 'mid', 'senior', 'exec']
salaries = np.array([25000, 45000, 75000, 120000, 350000, 58000])
bin_idx  = np.digitize(salaries, salary_bins) - 1
print("Salary bands:", [labels[min(i, len(labels)-1)] for i in bin_idx])"""},
        {"label": "Correlation and covariance",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)
n = 200

# Generate correlated variables
x1 = rng.normal(0, 1, n)
x2 = 0.8 * x1 + rng.normal(0, 0.6, n)   # strong positive correlation
x3 = rng.normal(0, 1, n)                  # uncorrelated

data = np.column_stack([x1, x2, x3])

# Pearson correlation matrix
corr = np.corrcoef(data.T)  # data.T because corrcoef expects (n_vars, n_obs)
print("Correlation matrix:")
for row in corr:
    print("  ", " ".join(f"{v:+.3f}" for v in row))

# Covariance matrix
cov = np.cov(data.T)
print("Covariance matrix diagonal (variances):", np.diag(cov).round(3))

# Manual Pearson r for two variables
def pearson_r(a, b):
    a_c, b_c = a - a.mean(), b - b.mean()
    return (a_c * b_c).sum() / (np.sqrt((a_c**2).sum()) * np.sqrt((b_c**2).sum()))

r12 = pearson_r(x1, x2)
r13 = pearson_r(x1, x3)
print(f"Pearson r(x1,x2)={r12:.3f}, r(x1,x3)={r13:.3f}")

# Rolling correlation
window = 30
roll_corr = np.array([
    pearson_r(x1[i:i+window], x2[i:i+window])
    for i in range(n - window)
])
print(f"Rolling({window}) correlation: mean={roll_corr.mean():.3f}")"""}
    ],
    rw_title="Multi-Asset Risk Analysis",
    rw_scenario="A risk team computes the 1-day 99% VaR and expected shortfall for a 10-asset portfolio using historical simulation on 5 years of daily returns.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)
n_assets = 10
n_days   = 1260   # 5 trading years

# Simulate correlated returns
true_corr = 0.3 * np.ones((n_assets, n_assets)) + 0.7 * np.eye(n_assets)
L = np.linalg.cholesky(true_corr)
Z = rng.standard_normal((n_days, n_assets))
returns = (Z @ L.T) * 0.01  # ~1% daily vol

# Equal-weight portfolio returns
weights  = np.ones(n_assets) / n_assets
port_ret = returns @ weights

# Risk metrics
var_99   = np.percentile(port_ret, 1)
es_99    = port_ret[port_ret <= var_99].mean()
ann_vol  = port_ret.std() * np.sqrt(252)

print(f"Portfolio daily returns: mean={port_ret.mean():.4%}, vol={port_ret.std():.4%}")
print(f"Annualized vol:    {ann_vol:.2%}")
print(f"1-day VaR (99%):   {var_99:.4%}")
print(f"Expected Shortfall (CVaR 99%): {es_99:.4%}")

# Correlation matrix
corr = np.corrcoef(returns.T)
print(f"Avg pairwise correlation: {corr[np.triu_indices(n_assets, k=1)].mean():.3f}")""",
    pt="Weighted Statistics",
    pd_text="Implement weighted_mean(data, weights), weighted_std(data, weights, ddof=0), and weighted_percentile(data, weights, q) where weights represent observation frequencies. Verify weighted_mean on data=[1,2,3,4,5] with weights=[5,1,1,1,1] (mean should be close to 1 since 5 is heavily weighted).",
    ps=
"""import numpy as np

def weighted_mean(data, weights):
    data, weights = np.asarray(data, float), np.asarray(weights, float)
    # TODO: return sum(data * weights) / sum(weights)
    pass

def weighted_std(data, weights, ddof=0):
    mean = weighted_mean(data, weights)
    # TODO: compute weighted variance then sqrt
    # variance = sum(w * (x - mean)^2) / sum(w) for ddof=0
    pass

def weighted_percentile(data, weights, q):
    # Sort data by value, then compute cumulative weight fraction
    data, weights = np.asarray(data, float), np.asarray(weights, float)
    idx     = np.argsort(data)
    sdata   = data[idx]
    sweights = weights[idx]
    cumw    = np.cumsum(sweights) / sweights.sum()
    # TODO: interpolate to find value at quantile q (0-100)
    pass

data    = np.array([1, 2, 3, 4, 5], float)
weights = np.array([5, 1, 1, 1, 1], float)
print("Weighted mean:", weighted_mean(data, weights))   # should be ~1.5
print("Weighted std: ", weighted_std(data, weights))
print("Weighted 50th:", weighted_percentile(data, weights, 50))
"""
)

# ── Section 23: Array I/O ────────────────────────────────────────────────────
s23 = make_np(23, "Array I/O (save, load, text, memmap)",
    "NumPy supports binary (.npy, .npz), text (savetxt/genfromtxt), and memory-mapped file formats for efficient large array storage and loading.",
    [
        {"label": "np.save, np.load, np.savez",
         "code":
"""import numpy as np
import tempfile, pathlib

tmp = pathlib.Path(tempfile.mkdtemp())

# Save/load single array (.npy)
arr = np.arange(12).reshape(3, 4)
np.save(tmp / 'array.npy', arr)

loaded = np.load(tmp / 'array.npy')
print("Loaded:", loaded)
print("Same data:", np.array_equal(arr, loaded))
print("File size:", (tmp / 'array.npy').stat().st_size, "bytes")

# Save multiple arrays in one file (.npz = numpy zip)
x  = np.linspace(0, 10, 100)
y  = np.sin(x)
dy = np.cos(x)
np.savez(tmp / 'signals.npz', x=x, y=y, dy=dy)

data = np.load(tmp / 'signals.npz')
print("Keys in npz:", list(data.keys()))
print("x[0:3]:", data['x'][:3].round(3))

# savez_compressed: gzip compression
np.savez_compressed(tmp / 'signals_compressed.npz', **dict(data))
orig_size = (tmp / 'signals.npz').stat().st_size
comp_size = (tmp / 'signals_compressed.npz').stat().st_size
print(f"Original: {orig_size} bytes, Compressed: {comp_size} bytes ({comp_size/orig_size:.0%})")

import shutil; shutil.rmtree(tmp)"""},
        {"label": "savetxt and genfromtxt",
         "code":
"""import numpy as np
import tempfile, pathlib

tmp = pathlib.Path(tempfile.mkdtemp())

# savetxt: write to CSV/TSV
data = np.array([[1, 2.5, 3.7], [4, 5.1, 6.8], [7, 8.3, 9.0]])
np.savetxt(tmp / 'data.csv', data, delimiter=',', fmt='%.2f',
           header='col1,col2,col3', comments='')

# Read it back
loaded = np.genfromtxt(tmp / 'data.csv', delimiter=',', skip_header=1)
print("Loaded from CSV:\\n", loaded)

# genfromtxt with mixed data and missing values
csv_content = '''id,temp,humidity,status
1,22.5,65.0,OK
2,nan,72.0,OK
3,19.8,,WARN
4,25.1,80.5,OK'''

(tmp / 'sensors.csv').write_text(csv_content)
sensors = np.genfromtxt(
    tmp / 'sensors.csv',
    delimiter=',',
    names=True,         # use header row as field names
    dtype=None,         # auto-detect dtypes
    encoding='utf-8',
    filling_values=np.nan  # fill missing with nan
)
print("dtype:", sensors.dtype)
print("temps:", sensors['temp'])
print("humidity:", sensors['humidity'])

import shutil; shutil.rmtree(tmp)"""},
        {"label": "Memory-mapped arrays (np.memmap)",
         "code":
"""import numpy as np
import tempfile, pathlib

tmp = pathlib.Path(tempfile.mkdtemp())
fpath = tmp / 'large_array.dat'

# Create a memory-mapped array (simulating large data)
shape = (1000, 500)
# 'w+' = write+read, 'r+' = read+write existing, 'r' = read-only
mm_write = np.memmap(fpath, dtype='float32', mode='w+', shape=shape)

# Fill with data (only the modified pages are loaded into RAM)
mm_write[:100, :] = np.random.randn(100, 500).astype('float32')
mm_write.flush()  # ensure data is written to disk
del mm_write

# Read back without loading everything into memory
mm_read = np.memmap(fpath, dtype='float32', mode='r', shape=shape)
print(f"Array shape: {mm_read.shape}, dtype: {mm_read.dtype}")
print(f"First row (first 5): {mm_read[0, :5]}")
print(f"File size: {fpath.stat().st_size:,} bytes")
print(f"Expected: {shape[0]*shape[1]*4:,} bytes (float32 = 4 bytes)")

# Slice a subarray (still memory-mapped, not loaded)
sub = mm_read[:50, :100]
print(f"Subarray shape: {sub.shape}, mean={sub.mean():.4f}")

del mm_read
import shutil; shutil.rmtree(tmp)"""}
    ],
    rw_title="Model Checkpoint System",
    rw_scenario="A deep learning workflow saves model weights and training history to compressed .npz files and reloads them for inference, logging the disk footprint.",
    rw_code=
"""import numpy as np, tempfile, pathlib, shutil

tmp = pathlib.Path(tempfile.mkdtemp())

# Simulate model weights for a small neural network
rng = np.random.default_rng(42)
weights = {
    "W1": rng.standard_normal((784, 256)).astype(np.float32),
    "b1": np.zeros(256, dtype=np.float32),
    "W2": rng.standard_normal((256, 128)).astype(np.float32),
    "b2": np.zeros(128, dtype=np.float32),
    "W3": rng.standard_normal((128, 10)).astype(np.float32),
    "b3": np.zeros(10, dtype=np.float32),
}
history = {
    "train_loss": rng.uniform(0.5, 2.0, 50).cumsum() ** 0 * np.linspace(2, 0.2, 50),
    "val_loss":   rng.uniform(0.5, 2.0, 50).cumsum() ** 0 * np.linspace(2.1, 0.25, 50),
    "epoch":      np.arange(50),
}

def save_checkpoint(path, weights, history, epoch):
    np.savez_compressed(path, epoch=epoch, **weights, **history)
    return path.stat().st_size

def load_checkpoint(path):
    data = np.load(path)
    epoch = int(data['epoch'])
    W = {k: data[k] for k in ['W1','b1','W2','b2','W3','b3']}
    H = {k: data[k] for k in ['train_loss','val_loss','epoch']}
    return epoch, W, H

ckpt_path = tmp / 'checkpoint_ep50.npz'
size = save_checkpoint(ckpt_path, weights, history, epoch=50)
print(f"Checkpoint saved: {size:,} bytes ({size/1024:.1f} KB)")

ep, W, H = load_checkpoint(ckpt_path)
print(f"Loaded epoch {ep}, W1 shape: {W['W1'].shape}")
print(f"Final train loss: {H['train_loss'][-1]:.4f}")

shutil.rmtree(tmp)""",
    pt="Data Pipeline with npz Cache",
    pd_text="Write a DataCache class that saves a numpy array to disk as .npz if it doesn't exist, or loads it if it does. Add methods: cache_exists(key), save(key, **arrays), load(key), and delete(key). The cache directory should be configurable in __init__. Test by saving and loading a feature matrix and label array.",
    ps=
"""import numpy as np, pathlib

class DataCache:
    def __init__(self, cache_dir='./cache'):
        self.dir = pathlib.Path(cache_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _path(self, key):
        return self.dir / f"{key}.npz"

    def exists(self, key):
        return self._path(key).exists()

    def save(self, key, **arrays):
        np.savez_compressed(self._path(key), **arrays)

    def load(self, key):
        if not self.exists(key):
            raise FileNotFoundError(f"Cache key {key!r} not found")
        return dict(np.load(self._path(key)))

    def delete(self, key):
        p = self._path(key)
        if p.exists(): p.unlink()

import tempfile, shutil
tmp = tempfile.mkdtemp()
cache = DataCache(tmp)

rng = np.random.default_rng(42)
X = rng.standard_normal((1000, 20))
y = rng.integers(0, 5, 1000)

cache.save('features', X=X, y=y)
print("Exists:", cache.exists('features'))

data = cache.load('features')
print("Loaded X:", data['X'].shape, "y:", data['y'].shape)
print("Data matches:", np.allclose(X, data['X']))

cache.delete('features')
print("After delete:", cache.exists('features'))
shutil.rmtree(tmp)
"""
)

# ── Section 24: Datetime64 & Time Arithmetic ─────────────────────────────────
s24 = make_np(24, "Datetime64 & Time Arithmetic",
    "NumPy's datetime64 and timedelta64 types enable vectorized date/time arithmetic without Python loops. Essential for time series alignment and resampling.",
    [
        {"label": "datetime64 basics and arithmetic",
         "code":
"""import numpy as np

# Create datetime64 scalars and arrays
d1 = np.datetime64('2024-01-15')
d2 = np.datetime64('2024-03-20')
print("d1:", d1, "d2:", d2)

# Arithmetic
delta = d2 - d1
print(f"Delta: {delta}")               # timedelta64
print(f"Days between: {delta.astype('timedelta64[D]').astype(int)}")

# Add days
d3 = d1 + np.timedelta64(30, 'D')
print(f"30 days after d1: {d3}")

# Date range
dates = np.arange('2024-01', '2025-01', dtype='datetime64[M]')  # monthly
print("Monthly dates:", dates)
print("Count:", len(dates))

# Different units
dt_ns = np.datetime64('2024-01-15T09:30:00.000000000', 'ns')
dt_s  = np.datetime64('2024-01-15T09:30:00', 's')
print("Nanosecond precision:", dt_ns)
print("Second precision:", dt_s)

# Year, month, day extraction via astype
day_arr  = np.arange('2024-01-01', '2024-02-01', dtype='datetime64[D]')
months   = day_arr.astype('datetime64[M]').astype(int) % 12 + 1
dom      = (day_arr - day_arr.astype('datetime64[M]')).astype(int) + 1
print("Days of month:", dom[:7])"""},
        {"label": "Business day operations and calendar",
         "code":
"""import numpy as np

# busdaycalendar: define which days are business days
# Default: Mon-Fri, no holidays
bdc = np.busdaycalendar()

# busday_count: count business days between dates
start = np.datetime64('2024-01-01')
end   = np.datetime64('2024-12-31')
n_bdays = np.busday_count(start, end)
print(f"Business days in 2024: {n_bdays}")

# is_busday: check if date is a business day
dates = np.arange('2024-01-01', '2024-01-08', dtype='datetime64[D]')
for d in dates:
    bd = np.is_busday(d)
    print(f"  {d} ({['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][(d.astype('datetime64[D]').astype(int))%7]}): {'Business' if bd else 'Weekend'}")

# offset_busdays: advance by N business days
t_plus_5bd = np.busday_offset('2024-01-15', 5, roll='forward')
print(f"5 business days after Jan 15: {t_plus_5bd}")

# Custom calendar with holidays
holidays  = np.array(['2024-01-01', '2024-12-25'], dtype='datetime64[D]')
bdc_h = np.busdaycalendar(holidays=holidays)
# Settlement: T+2 business days (like equity markets)
trade_dates = np.array(['2024-01-03', '2024-12-24', '2024-12-26'], dtype='datetime64')
settlement  = np.busday_offset(trade_dates, 2, busdaycal=bdc_h)
for t, s in zip(trade_dates, settlement):
    print(f"  Trade {t} -> Settle {s}")"""},
        {"label": "Time series alignment and resampling",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Generate irregular timestamps (like real tick data)
n = 200
base  = np.datetime64('2024-01-15T09:30:00', 's')
gaps  = rng.integers(1, 60, n).astype('timedelta64[s]')   # 1-60 sec gaps
times = base + np.cumsum(gaps)

prices = 100 + np.cumsum(rng.normal(0, 0.05, n))

print(f"First timestamp: {times[0]}")
print(f"Last timestamp:  {times[-1]}")
print(f"Total duration: {(times[-1] - times[0]).astype(int)} seconds")

# Bin into 1-minute buckets (OHLCV)
minute_start = times.astype('datetime64[m]')
unique_mins  = np.unique(minute_start)

print(f"Number of 1-minute bars: {len(unique_mins)}")

# OHLCV for each minute
for m in unique_mins[:3]:
    mask = (minute_start == m)
    bar_prices = prices[mask]
    print(f"  {m}: O={bar_prices[0]:.2f} H={bar_prices.max():.2f} "
          f"L={bar_prices.min():.2f} C={bar_prices[-1]:.2f} V={mask.sum()}")

# Time-based filtering
morning = (times >= np.datetime64('2024-01-15T09:30:00', 's')) & \\
          (times <  np.datetime64('2024-01-15T10:00:00', 's'))
print(f"Ticks in first 30 min: {morning.sum()}")"""}
    ],
    rw_title="Market Hours Filter",
    rw_scenario="A trading system filters raw tick data to keep only regular market hours (9:30-16:00 ET), exclude weekends and holidays, and compute daily OHLCV bars.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)

# Simulate a week of irregular tick data
days = np.arange('2024-01-08', '2024-01-13', dtype='datetime64[D]')  # Mon-Fri
all_times, all_prices = [], []
price = 100.0
for day in days:
    open_ns  = day.astype('datetime64[s]') + np.timedelta64(9*3600+30*60, 's')
    close_ns = day.astype('datetime64[s]') + np.timedelta64(16*3600, 's')
    n_ticks  = rng.integers(50, 150)
    t_offsets = rng.integers(0, int((close_ns - open_ns).astype(int)), n_ticks)
    t_offsets.sort()
    tick_times = open_ns + t_offsets.astype('timedelta64[s]')
    rets = rng.normal(0, 0.01, n_ticks)
    tick_prices = price * np.exp(np.cumsum(rets))
    price = tick_prices[-1]
    all_times.extend(tick_times.tolist())
    all_prices.extend(tick_prices.tolist())

times  = np.array(all_times, dtype='datetime64[s]')
prices = np.array(all_prices)

# OHLCV per day
print("Daily OHLCV:")
day_buckets = times.astype('datetime64[D]')
for day in np.unique(day_buckets):
    m = (day_buckets == day)
    p = prices[m]
    print(f"  {day}: O={p[0]:.2f} H={p.max():.2f} L={p.min():.2f} C={p[-1]:.2f} V={m.sum()}")""",
    pt="Holiday Calendar",
    pd_text="Write a function get_trading_days(start, end, holidays) that returns all business days between start and end (as datetime64 strings) excluding the given holidays. Write next_trading_day(date, holidays) that returns the next business day on or after date. Test with US holidays from 2024.",
    ps=
"""import numpy as np

def get_trading_days(start, end, holidays=None):
    start = np.datetime64(start, 'D')
    end   = np.datetime64(end, 'D')
    hols  = np.array(holidays or [], dtype='datetime64[D]')
    bdc   = np.busdaycalendar(holidays=hols)
    # Generate all calendar days, filter to business days
    all_days = np.arange(start, end, dtype='datetime64[D]')
    return all_days[np.is_busday(all_days, busdaycal=bdc)]

def next_trading_day(date, holidays=None):
    date = np.datetime64(date, 'D')
    hols = np.array(holidays or [], dtype='datetime64[D]')
    bdc  = np.busdaycalendar(holidays=hols)
    return np.busday_offset(date, 0, roll='forward', busdaycal=bdc)

us_holidays_2024 = [
    '2024-01-01', '2024-01-15', '2024-02-19',
    '2024-05-27', '2024-07-04', '2024-09-02',
    '2024-11-28', '2024-12-25'
]
trading_days = get_trading_days('2024-01-01', '2024-04-01', us_holidays_2024)
print(f"Trading days in Q1 2024: {len(trading_days)}")
print("First 5:", trading_days[:5])
print("Last 3: ", trading_days[-3:])

print("Next trading day after 2024-12-24:", next_trading_day('2024-12-24', us_holidays_2024))
"""
)

# ── Assemble and insert ──────────────────────────────────────────────────────
all_sections = s17 + s18 + s19 + s20 + s21 + s22 + s23 + s24
result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: numpy sections 17-24 added")
else:
    print("FAILED")
