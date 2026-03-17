"""Add 3 sections each to gen_sklearn.py and gen_polars.py (code1/code2/code3/code4 format)."""
import os, re

BASE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path"

def ec(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace("'", "\\'")

def ct(code, indent="            "):
    """Convert multi-line code to tuple-concatenation format with escaping."""
    lines = code.split('\n')
    parts = []
    for line in lines:
        escaped = line.replace('\\', '\\\\').replace('"', '\\"')
        parts.append(f'{indent}"{escaped}\\n"')
    return "(\n" + "\n".join(parts) + "\n        )"

def make_section4(num, title, desc,
                  c1t, c1, c2t, c2, c3t=None, c3=None, c4t=None, c4=None,
                  rw_scenario="", rw_code="",
                  pt="", pd="", ps=""):
    s = f'    {{\n'
    s += f'        "title": "{num}. {title}",\n'
    s += f'        "desc": "{ec(desc)}",\n'
    s += f'        "code1_title": "{c1t}",\n'
    s += f'        "code1": {ct(c1)},\n'
    s += f'        "code2_title": "{c2t}",\n'
    s += f'        "code2": {ct(c2)},\n'
    if c3t and c3:
        s += f'        "code3_title": "{c3t}",\n'
        s += f'        "code3": {ct(c3)},\n'
    if c4t and c4:
        s += f'        "code4_title": "{c4t}",\n'
        s += f'        "code4": {ct(c4)},\n'
    s += f'        "rw_scenario": "{ec(rw_scenario)}",\n'
    s += f'        "rw_code": {ct(rw_code)},\n'
    s += f'        "practice": {{\n'
    s += f'            "title": "{pt}",\n'
    s += f'            "desc": "{ec(pd)}",\n'
    s += f'            "starter": {ct(ps)},\n'
    s += f'        }},\n'
    s += f'    }},\n'
    return s

def insert_code4(filepath, new_sections_str):
    content = open(filepath, encoding='utf-8').read()
    marker = '\n]\n\n\ndef make_html'
    idx = content.find(marker)
    if idx == -1:
        print(f"ERROR: marker not found in {filepath}")
        return False
    # The content before the marker — check if last section has comma
    before = content[:idx].rstrip()
    # Last char should be ',' already since each section ends with '},
    insert_str = content[:idx] + '\n' + new_sections_str + content[idx:]
    open(filepath, 'w', encoding='utf-8').write(insert_str)
    print(f"OK: inserted sections into {filepath}")
    return True

# ═══════════════════════════════════════════════════════════════════
#  SKLEARN SECTIONS
# ═══════════════════════════════════════════════════════════════════

sk14_c1 = """import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import roc_auc_score

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Base learners: get out-of-fold predictions
rf   = RandomForestClassifier(n_estimators=100, random_state=0)
gbm  = GradientBoostingClassifier(n_estimators=100, random_state=1)
rf_oof  = cross_val_predict(rf,  X, y, cv=cv, method='predict_proba')[:, 1]
gbm_oof = cross_val_predict(gbm, X, y, cv=cv, method='predict_proba')[:, 1]

# Stack: meta-learner on OOF predictions
import numpy as np
X_meta = np.column_stack([rf_oof, gbm_oof])
meta = LogisticRegression()
meta_oof = cross_val_predict(meta, X_meta, y, cv=cv, method='predict_proba')[:, 1]

print(f"RF AUC:   {roc_auc_score(y, rf_oof):.4f}")
print(f"GBM AUC:  {roc_auc_score(y, gbm_oof):.4f}")
print(f"Stack AUC:{roc_auc_score(y, meta_oof):.4f}")"""

sk14_c2 = """import numpy as np
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

X, y = make_regression(n_samples=800, n_features=15, noise=20, random_state=42)
kf = KFold(n_splits=5, shuffle=True, random_state=0)

# Blending: single hold-out blend set
blend_idx = int(0.8 * len(X))
X_tr, X_bl = X[:blend_idx], X[blend_idx:]
y_tr, y_bl = y[:blend_idx], y[blend_idx:]

rf   = RandomForestRegressor(n_estimators=100, random_state=0).fit(X_tr, y_tr)
gbm  = GradientBoostingRegressor(n_estimators=100, random_state=1).fit(X_tr, y_tr)
rf_bl  = rf.predict(X_bl)
gbm_bl = gbm.predict(X_bl)

# Grid search blending weights
best_w, best_rmse = 0.5, float('inf')
for w in np.arange(0, 1.05, 0.05):
    blend = w * rf_bl + (1-w) * gbm_bl
    rmse = np.sqrt(mean_squared_error(y_bl, blend))
    if rmse < best_rmse:
        best_rmse, best_w = rmse, w

print(f"RF   RMSE: {np.sqrt(mean_squared_error(y_bl, rf_bl)):.4f}")
print(f"GBM  RMSE: {np.sqrt(mean_squared_error(y_bl, gbm_bl)):.4f}")
print(f"Best blend (w_rf={best_w:.2f}): RMSE={best_rmse:.4f}")"""

sk14_c3 = """import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
                               ExtraTreesClassifier, StackingClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=1000, n_features=20,
                            n_informative=12, random_state=42)
estimators = [
    ('rf',  RandomForestClassifier(n_estimators=100, random_state=0)),
    ('gbm', GradientBoostingClassifier(n_estimators=100, random_state=1)),
    ('et',  ExtraTreesClassifier(n_estimators=100, random_state=2)),
]
stack = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(),
    cv=5, passthrough=False
)
scores = cross_val_score(stack, X, y, cv=5, scoring='roc_auc')
print(f"Stacking AUC: {scores.mean():.4f} +/- {scores.std():.4f}")"""

sk14_c4 = """import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score

X, y = make_classification(n_samples=1000, n_features=20, random_state=7)

models = {
    "Single Tree":  DecisionTreeClassifier(max_depth=5),
    "Bagging":      BaggingClassifier(DecisionTreeClassifier(max_depth=5),
                                       n_estimators=50, random_state=0),
    "AdaBoost":     AdaBoostClassifier(n_estimators=100, random_state=1),
    "Random Forest":RandomForestClassifier(n_estimators=100, random_state=2),
}
print(f"{'Model':<20} {'AUC':>8} {'Std':>6}")
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
    print(f"{name:<20} {scores.mean():.4f}  {scores.std():.4f}")"""

sk14_ps = """import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
                               StackingClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

X, y = load_breast_cancer(return_X_y=True)
# TODO: Build a 3-model stacking ensemble (RF, GBM, SVM or LR)
# TODO: Use StratifiedKFold(5) for OOF generation
# TODO: Meta-learner: LogisticRegression
# TODO: Compare: base models AUC vs stacking AUC
# TODO: Add feature passthrough=True and compare again
"""

sk14 = make_section4(
    "14", "Ensemble Methods: Stacking & Blending",
    "Combine multiple base learners to build a stronger meta-model. Stacking uses out-of-fold predictions as features for a meta-learner; blending uses a single held-out set. Both reduce variance and capture complementary model strengths.",
    "Stacking with OOF Predictions", sk14_c1,
    "Blending with Weight Search", sk14_c2,
    "sklearn StackingClassifier", sk14_c3,
    "Ensemble Comparison", sk14_c4,
    rw_scenario="Insurance claim prediction: blend Random Forest, GBM, and Logistic Regression using OOF stacking to achieve better AUC than any single model for claims approval.",
    rw_code="""import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score
np.random.seed(42)
X, y = make_classification(n_samples=2000, n_features=25, n_informative=15, random_state=0)
estimators = [
    ("rf",  RandomForestClassifier(n_estimators=100, random_state=0)),
    ("gbm", GradientBoostingClassifier(n_estimators=100, random_state=1)),
]
stack = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression(), cv=5)
for name, clf in estimators + [("stack", stack)]:
    scores = cross_val_score(clf, X, y, cv=5, scoring="roc_auc")
    print(f"{name:<8}: AUC={scores.mean():.4f} +/- {scores.std():.4f}")""",
    pt="Breast Cancer Ensemble",
    pd="Build a 3-model stacking classifier on the breast cancer dataset. Compare individual model AUC vs stacking AUC with and without feature passthrough. Also try a weighted average blend and optimize weights by grid search. Report which combination gives the best result.",
    ps=sk14_ps
)

sk15_c1 = """import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

np.random.seed(42)
n = 500
dates = pd.date_range("2020-01-01", periods=n, freq="D")
trend  = np.arange(n) * 0.05
season = 2 * np.sin(2 * np.pi * np.arange(n) / 7)
noise  = np.random.normal(0, 0.5, n)
y = trend + season + noise

# Time-Series Split: expanding window
n_splits = 5
split_size = n // (n_splits + 1)
results = []
for fold in range(n_splits):
    train_end = split_size * (fold + 2)
    test_end  = train_end + split_size
    X_tr = np.column_stack([np.arange(train_end), np.sin(2*np.pi*np.arange(train_end)/7)])
    X_te = np.column_stack([np.arange(train_end, test_end),
                             np.sin(2*np.pi*np.arange(train_end, test_end)/7)])
    m = Ridge().fit(X_tr, y[:train_end])
    pred = m.predict(X_te)
    rmse = np.sqrt(mean_squared_error(y[train_end:test_end], pred))
    results.append(rmse)
    print(f"Fold {fold+1}: train={train_end}, test RMSE={rmse:.4f}")
print(f"Mean RMSE: {np.mean(results):.4f}")"""

sk15_c2 = """import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

np.random.seed(1)
n = 400
t = np.arange(n)
y = 3*np.sin(2*np.pi*t/30) + 0.02*t + np.random.normal(0, 0.3, n)

# Feature engineering: lag features + time features
def make_features(t_arr, y_arr, lag=5):
    X = np.column_stack([
        t_arr,
        np.sin(2*np.pi*t_arr/7),
        np.sin(2*np.pi*t_arr/30),
    ] + [np.roll(y_arr, l) for l in range(1, lag+1)])
    return X[lag:]

lag = 5
X = make_features(t, y, lag)
y_lagged = y[lag:]
tscv = TimeSeriesSplit(n_splits=5)
pipe = Pipeline([("scaler", StandardScaler()), ("ridge", Ridge(alpha=1.0))])
rmses = []
for tr, te in tscv.split(X):
    pipe.fit(X[tr], y_lagged[tr])
    pred = pipe.predict(X[te])
    rmses.append(np.sqrt(mean_squared_error(y_lagged[te], pred)))
    print(f"  RMSE: {rmses[-1]:.4f}")
print(f"TimeSeriesSplit CV RMSE: {np.mean(rmses):.4f} +/- {np.std(rmses):.4f}")"""

sk15_c3 = """import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

np.random.seed(5)
n = 600
t = np.arange(n)
# Piecewise trend with seasonality
y = np.where(t < 300, 0.03*t, 0.01*t + 6) + 2*np.sin(2*np.pi*t/52) + np.random.normal(0, 0.5, n)

def make_X(t_arr, y_arr, lag=10):
    features = [t_arr % 7, t_arr % 52]  # day-of-week, week-of-year
    for l in range(1, lag+1):
        features.append(np.roll(y_arr, l))
    X = np.column_stack(features)[lag:]
    return X

X = make_X(t, y, lag=10)
y_f = y[10:]
tscv = TimeSeriesSplit(n_splits=5, gap=10)
results = []
for fold, (tr, te) in enumerate(tscv.split(X)):
    m = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=0)
    m.fit(X[tr], y_f[tr])
    pred = m.predict(X[te])
    rmse = np.sqrt(mean_squared_error(y_f[te], pred))
    results.append(rmse)
    print(f"Fold {fold+1} (gap=10): RMSE={rmse:.4f}")
print(f"Mean RMSE: {np.mean(results):.4f}")"""

sk15_ps = """import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
np.random.seed(0)
n = 730
t = np.arange(n)
# Daily demand with weekly + annual seasonality + upward trend
demand = (100 + 0.1*t + 20*np.sin(2*np.pi*t/7) +
          10*np.sin(2*np.pi*t/365) + np.random.normal(0, 5, n))
# TODO: Create lag features (lag 1..14) + time features (dow, month)
# TODO: TimeSeriesSplit(n_splits=5, gap=7) walk-forward validation
# TODO: Compare Ridge, RF, GBM with CV RMSE
# TODO: Report per-fold RMSE and total mean RMSE for each model
"""

sk15 = make_section4(
    "15", "Time-Based Cross-Validation & Walk-Forward Validation",
    "Use TimeSeriesSplit for realistic CV that respects temporal ordering. Expanding-window and sliding-window strategies prevent future data leakage and simulate production deployment conditions.",
    "Expanding Window CV from Scratch", sk15_c1,
    "TimeSeriesSplit with sklearn Pipeline", sk15_c2,
    "Walk-Forward with Gap (prevents leakage)", sk15_c3,
    rw_scenario="Stock return prediction: use TimeSeriesSplit(n_splits=5, gap=5) to evaluate a GBM model on 3 years of daily data. Prevent look-ahead bias by ensuring a 5-day gap between train and test sets.",
    rw_code="""import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
np.random.seed(7)
n = 750
t = np.arange(n)
returns = np.random.normal(0.001, 0.02, n)
# Lag features
X = np.column_stack([np.roll(returns, l) for l in range(1, 11)])[10:]
y = returns[10:]
tscv = TimeSeriesSplit(n_splits=5, gap=5)
results = []
for fold, (tr, te) in enumerate(tscv.split(X)):
    m = GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=0)
    m.fit(X[tr], y[tr])
    pred = m.predict(X[te])
    rmse = np.sqrt(mean_squared_error(y[te], pred))
    results.append(rmse)
    print(f"Fold {fold+1}: test_size={len(te)}, RMSE={rmse:.6f}")
print(f"Mean RMSE: {np.mean(results):.6f}")""",
    pt="Demand Forecasting Walk-Forward",
    pd="Build a walk-forward validation pipeline for 730 days of demand data with weekly and annual seasonality. Compare Ridge, Random Forest, and GBM using TimeSeriesSplit(n_splits=5, gap=7). Report per-fold RMSE and select the best model. Use lag features (1-14 days) plus day-of-week and month features.",
    ps=sk15_ps
)

sk16_c1 = """import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
import shap

X, y = make_classification(n_samples=500, n_features=10,
                            n_informative=6, random_state=42)
feature_names = [f"feat_{i}" for i in range(10)]
model = RandomForestClassifier(n_estimators=100, random_state=0).fit(X, y)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X[:100])
# shap_values[1] = SHAP for class 1
print("Global feature importance (mean |SHAP|):")
mean_shap = np.abs(shap_values[1]).mean(axis=0)
for i in np.argsort(mean_shap)[::-1]:
    bar = "#" * int(mean_shap[i] * 100)
    print(f"  {feature_names[i]:<12} {mean_shap[i]:.4f}  {bar}")"""

sk16_c2 = """import numpy as np
from sklearn.datasets import make_regression
from sklearn.ensemble import GradientBoostingRegressor
import shap

X, y = make_regression(n_samples=400, n_features=8, noise=10, random_state=0)
feature_names = ["age","income","tenure","spend","logins","products","region","segment"]
model = GradientBoostingRegressor(n_estimators=200, random_state=0).fit(X, y)
explainer = shap.TreeExplainer(model)
shap_values = explainer(X[:50])

print("Individual explanation for sample 0:")
print(f"  Base value (expected prediction): {shap_values.base_values[0]:.3f}")
print(f"  Model output for sample 0:        {model.predict(X[:1])[0]:.3f}")
print("  Feature contributions:")
for feat, val in sorted(zip(feature_names, shap_values.values[0]),
                         key=lambda x: abs(x[1]), reverse=True):
    direction = "++" if val > 0 else "--"
    print(f"    {direction} {feat:<12}: {val:+.4f}")"""

sk16_c3 = """import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import shap

X, y = load_breast_cancer(return_X_y=True, as_frame=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
model = GradientBoostingClassifier(n_estimators=100, random_state=0).fit(X_tr, y_tr)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_te.values)

# Summary: top 5 most impactful features globally
mean_abs = np.abs(shap_values).mean(axis=0)
top5_idx = np.argsort(mean_abs)[::-1][:5]
print("Top 5 features by mean |SHAP| on test set:")
for i in top5_idx:
    feat = X.columns[i]
    print(f"  {feat:<35} mean|SHAP|={mean_abs[i]:.4f}")"""

sk16_ps = """import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import shap

housing = fetch_california_housing(as_frame=True)
X, y = housing.data, housing.target
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=0)
model.fit(X_tr, y_tr)
# TODO: Create SHAP TreeExplainer and compute shap_values for X_te[:200]
# TODO: Print global feature importance ranking (mean |SHAP|)
# TODO: Explain the 3 highest and 3 lowest predicted houses individually
# TODO: Check if SHAP values sum to model output - expected value (verify additivity)
"""

sk16 = make_section4(
    "16", "Interpretable ML: SHAP Values",
    "SHAP (SHapley Additive exPlanations) provides consistent, theoretically grounded feature attributions for any model. Use TreeExplainer for tree-based models for fast exact SHAP values.",
    "Global Feature Importance with SHAP", sk16_c1,
    "Individual Prediction Explanation", sk16_c2,
    "SHAP on Breast Cancer Dataset", sk16_c3,
    rw_scenario="Credit scoring: use SHAP to explain individual loan approval/rejection decisions to regulators and customers, identifying the top 3 features driving each decision.",
    rw_code="""import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import shap
np.random.seed(0)
n = 1000
X = np.random.randn(n, 8)
feature_names = ["credit_score","income","debt_ratio","employment_yrs",
                 "loan_amount","num_accounts","late_payments","collateral"]
# Simulate default probability
prob = 1 / (1 + np.exp(-(X[:,0]*0.8 - X[:,2]*0.6 + X[:,4]*0.4)))
y = np.random.binomial(1, prob)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
model = GradientBoostingClassifier(n_estimators=100, random_state=0).fit(X_tr, y_tr)
explainer = shap.TreeExplainer(model)
sv = explainer.shap_values(X_te)
print("Global importance (credit model):")
mean_abs = np.abs(sv).mean(axis=0)
for i in np.argsort(mean_abs)[::-1][:5]:
    print(f"  {feature_names[i]:<20}: {mean_abs[i]:.4f}")
print("\\nSample 0 explanation:")
for feat, val in sorted(zip(feature_names, sv[0]), key=lambda x: abs(x[1]), reverse=True)[:3]:
    print(f"  {feat}: {val:+.4f}")""",
    pt="California Housing SHAP Analysis",
    pd="Train a GBM on the California housing dataset and compute SHAP values for 200 test samples. Report global feature importance, explain the 3 highest and 3 lowest predicted houses, and verify SHAP additivity (SHAP values should sum to prediction - expected value).",
    ps=sk16_ps
)

# ═══════════════════════════════════════════════════════════════════
#  POLARS SECTIONS
# ═══════════════════════════════════════════════════════════════════

pl14_c1 = """import polars as pl
import numpy as np
np.random.seed(0)
n = 1_000_000
# Build large lazy dataset
lf = (
    pl.LazyFrame({
        "id":       np.arange(n),
        "category": np.random.choice(["A","B","C","D"], n),
        "value":    np.random.normal(100, 20, n),
        "weight":   np.random.uniform(0.5, 2.0, n),
    })
    .filter(pl.col("value") > 60)
    .with_columns([
        (pl.col("value") * pl.col("weight")).alias("weighted_value"),
        pl.col("category").cast(pl.Categorical),
    ])
    .group_by("category")
    .agg([
        pl.col("weighted_value").mean().alias("mean_wv"),
        pl.col("value").std().alias("std_val"),
        pl.col("id").count().alias("n"),
    ])
    .sort("mean_wv", descending=True)
)
# Show the query plan
print("Query plan:")
print(lf.explain())
result = lf.collect()
print(result)"""

pl14_c2 = """import polars as pl
import numpy as np
np.random.seed(1)
n = 500_000
# Streaming scan simulation: process in chunks
df = pl.DataFrame({
    "user_id":   np.random.randint(1, 1000, n),
    "revenue":   np.random.lognormal(3, 1, n),
    "product":   np.random.choice(["X","Y","Z"], n),
    "is_premium":np.random.randint(0, 2, n).astype(bool),
})
# Save and reload to test scan_parquet streaming
import tempfile, os
tmp = tempfile.mktemp(suffix=".parquet")
df.write_parquet(tmp)
# Streaming aggregation from parquet
result = (
    pl.scan_parquet(tmp)
    .filter(pl.col("is_premium"))
    .group_by("product")
    .agg([
        pl.col("revenue").sum().alias("total_rev"),
        pl.col("user_id").n_unique().alias("unique_users"),
        pl.col("revenue").mean().alias("avg_rev"),
    ])
    .sort("total_rev", descending=True)
    .collect(streaming=True)
)
os.unlink(tmp)
print(result)"""

pl14_c3 = """import polars as pl
import numpy as np
import time
np.random.seed(42)
n = 200_000
df = pl.DataFrame({
    "id":    np.arange(n),
    "x":     np.random.randn(n),
    "group": np.random.choice([f"G{i}" for i in range(50)], n),
})
# Pattern 1: inefficient (multiple passes)
t0 = time.perf_counter()
for _ in range(3):
    _ = df.filter(pl.col("x") > 0).group_by("group").agg(pl.col("x").mean())
t1 = time.perf_counter()
# Pattern 2: single lazy pass with predicate pushdown
t2 = time.perf_counter()
for _ in range(3):
    _ = (pl.LazyFrame(df)
         .filter(pl.col("x") > 0)
         .group_by("group")
         .agg(pl.col("x").mean())
         .collect())
t3 = time.perf_counter()
print(f"Eager repeated passes: {(t1-t0)*1000:.1f} ms")
print(f"LazyFrame with pushdown: {(t3-t2)*1000:.1f} ms")"""

pl14_ps = """import polars as pl
import numpy as np
import time
np.random.seed(7)
n = 2_000_000
df = pl.DataFrame({
    "transaction_id": np.arange(n),
    "customer_id":    np.random.randint(1, 10000, n),
    "amount":         np.random.lognormal(4, 1, n),
    "category":       np.random.choice(["food","travel","retail","tech","health"], n),
    "is_fraud":       np.random.binomial(1, 0.02, n).astype(bool),
    "day_of_week":    np.random.randint(0, 7, n),
})
# TODO: Use LazyFrame to filter fraud transactions, group by category+day_of_week
# TODO: Compute: sum(amount), count, fraud_rate per group
# TODO: Show query plan with .explain()
# TODO: Compare timing: eager vs lazy with collect(streaming=True)
# TODO: Save result to parquet, reload with scan_parquet and verify row count
"""

pl14 = make_section4(
    "14", "Polars LazyFrame & Streaming Optimization",
    "LazyFrame enables query optimization through predicate pushdown, projection pushdown, and streaming execution. Build full pipelines before calling .collect() to let Polars optimize the execution plan.",
    "LazyFrame with Query Plan Inspection", pl14_c1,
    "Streaming Parquet Processing", pl14_c2,
    "Lazy vs Eager Benchmark", pl14_c3,
    rw_scenario="E-commerce analytics: process 10M order records from Parquet using LazyFrame with streaming=True to compute revenue by product category without loading all data into memory.",
    rw_code="""import polars as pl
import numpy as np
import tempfile, os
np.random.seed(0)
n = 500_000
df = pl.DataFrame({
    "order_id":  np.arange(n),
    "category":  np.random.choice(["Electronics","Clothing","Food","Sports","Books"], n),
    "revenue":   np.random.lognormal(4, 1, n),
    "is_returned":np.random.binomial(1, 0.05, n).astype(bool),
    "customer_tier":np.random.choice(["gold","silver","bronze"], n),
})
tmp = tempfile.mktemp(suffix=".parquet")
df.write_parquet(tmp)
result = (
    pl.scan_parquet(tmp)
    .filter(~pl.col("is_returned"))
    .group_by(["category","customer_tier"])
    .agg([
        pl.col("revenue").sum().alias("total_rev"),
        pl.col("revenue").mean().alias("avg_rev"),
        pl.col("order_id").count().alias("n_orders"),
    ])
    .sort("total_rev", descending=True)
    .collect(streaming=True)
)
os.unlink(tmp)
print(result.head(8))""",
    pt="Fraud Transaction Pipeline",
    pd="Process 2M transaction records with LazyFrame: filter frauds, group by category+day_of_week, compute aggregate metrics. Show the query plan, benchmark eager vs lazy, and use streaming=True for collect. Save results to parquet and verify.",
    ps=pl14_ps
)

pl15_c1 = """import polars as pl
import numpy as np
np.random.seed(0)
n = 1000
dates = pl.date_range(
    pl.date(2022, 1, 1), pl.date(2024, 9, 26), interval="1d", eager=True
)[:n]
df = pl.DataFrame({
    "date":  dates,
    "value": 100 + np.cumsum(np.random.normal(0, 1, n)),
    "volume":np.random.poisson(1000, n).astype(float),
})
result = (
    df.with_columns([
        pl.col("date").dt.year().alias("year"),
        pl.col("date").dt.month().alias("month"),
        pl.col("date").dt.weekday().alias("dow"),
        pl.col("value").rolling_mean(window_size=7).alias("ma7"),
        pl.col("value").rolling_mean(window_size=30).alias("ma30"),
        pl.col("value").pct_change().alias("return_1d"),
    ])
    .filter(pl.col("ma7").is_not_null())
)
print(result.select(["date","value","ma7","ma30","return_1d"]).head(5))
print(result.select(pl.col("return_1d").std()).item())"""

pl15_c2 = """import polars as pl
import numpy as np
np.random.seed(1)
n = 500
dates = pl.date_range(pl.date(2023,1,1), pl.date(2024,5,14), interval="1d", eager=True)[:n]
df = pl.DataFrame({
    "date":  dates,
    "price": 50 + np.cumsum(np.random.normal(0, 0.5, n)),
})
# Resample to weekly and monthly
weekly = (
    df.group_by_dynamic("date", every="1w")
    .agg([
        pl.col("price").first().alias("open"),
        pl.col("price").max().alias("high"),
        pl.col("price").min().alias("low"),
        pl.col("price").last().alias("close"),
        pl.col("price").mean().alias("avg"),
    ])
)
monthly = (
    df.group_by_dynamic("date", every="1mo")
    .agg([
        pl.col("price").last().alias("month_close"),
        pl.col("price").std().alias("monthly_vol"),
    ])
)
print("Weekly OHLC:"); print(weekly.head(4))
print("Monthly volatility:"); print(monthly.head(4))"""

pl15_c3 = """import polars as pl
import numpy as np
np.random.seed(2)
n = 300
dates = pl.date_range(pl.date(2023,1,1), pl.date(2023,10,28), interval="1d", eager=True)[:n]
df = pl.DataFrame({
    "date":  dates,
    "value": 100 + np.cumsum(np.random.normal(0, 1.5, n)),
})
result = (
    df.with_columns([
        pl.col("value").shift(1).alias("lag_1"),
        pl.col("value").shift(7).alias("lag_7"),
        pl.col("value").shift(30).alias("lag_30"),
        pl.col("value").rolling_std(window_size=14).alias("vol_14"),
        (pl.col("value") / pl.col("value").shift(1) - 1).alias("return_1d"),
        pl.col("value").rolling_max(window_size=52).alias("rolling_high_52"),
        pl.col("value").rolling_min(window_size=52).alias("rolling_low_52"),
    ])
    .with_columns([
        ((pl.col("value") - pl.col("rolling_low_52")) /
         (pl.col("rolling_high_52") - pl.col("rolling_low_52"))).alias("pct_rank_52w"),
    ])
    .drop_nulls()
)
print(result.select(["date","value","lag_1","vol_14","pct_rank_52w"]).tail(5))
print(f"Rows after dropna: {len(result)}")"""

pl15_ps = """import polars as pl
import numpy as np
np.random.seed(99)
n = 730  # 2 years daily
dates = pl.date_range(pl.date(2022,1,1), pl.date(2023,12,31), interval="1d", eager=True)[:n]
# Multi-asset time series
df = pl.DataFrame({
    "date":  dates,
    "AAPL":  100 + np.cumsum(np.random.normal(0.05, 1.2, n)),
    "MSFT":  200 + np.cumsum(np.random.normal(0.08, 1.5, n)),
    "GOOG":  90  + np.cumsum(np.random.normal(0.03, 1.0, n)),
})
# TODO: Add rolling 20d and 50d MA for each stock
# TODO: Add daily returns for each stock
# TODO: Resample to weekly OHLC for AAPL
# TODO: Add 52-week high/low and % distance from 52w high
# TODO: Monthly summary: avg return and volatility per stock
"""

pl15 = make_section4(
    "15", "Time Series Operations in Polars",
    "Polars provides high-performance time series operations: rolling aggregations, resampling with group_by_dynamic, and lag/shift features. Temporal operations run significantly faster than pandas for large datasets.",
    "Rolling Statistics & Time Features", pl15_c1,
    "Resampling: Weekly & Monthly OHLC", pl15_c2,
    "Lag Features & Rolling Metrics", pl15_c3,
    rw_scenario="Retail analytics: compute 7-day and 30-day rolling sales averages, detect anomalies where daily sales deviate from the 30d mean by more than 2 std, and resample to weekly totals for reporting.",
    rw_code="""import polars as pl
import numpy as np
np.random.seed(1)
n = 365
dates = pl.date_range(pl.date(2023,1,1), pl.date(2023,12,31), interval="1d", eager=True)[:n]
sales = 1000 + 200*np.sin(2*np.pi*np.arange(n)/7) + np.random.normal(0, 80, n)
sales[100] += 800  # spike anomaly
df = pl.DataFrame({"date": dates, "sales": sales})
result = (
    df.with_columns([
        pl.col("sales").rolling_mean(window_size=7).alias("ma7"),
        pl.col("sales").rolling_mean(window_size=30).alias("ma30"),
        pl.col("sales").rolling_std(window_size=30).alias("std30"),
    ])
    .with_columns([
        ((pl.col("sales") - pl.col("ma30")) / pl.col("std30")).alias("z_score"),
    ])
    .with_columns([
        (pl.col("z_score").abs() > 2).alias("anomaly"),
    ])
)
anomalies = result.filter(pl.col("anomaly"))
print(f"Anomalies detected: {len(anomalies)}")
print(anomalies.select(["date","sales","ma30","z_score"]))
weekly = df.group_by_dynamic("date", every="1w").agg(pl.col("sales").sum().alias("weekly_total"))
print(weekly.head(5))""",
    pt="Multi-Asset Portfolio Analysis",
    pd="Build a 2-year daily time series for 3 simulated stocks. Add rolling 20/50-day moving averages, daily returns, and 52-week high/low metrics. Resample AAPL to weekly OHLC. Compute monthly summary statistics (avg return, volatility) for all stocks using group_by_dynamic.",
    ps=pl15_ps
)

pl16_c1 = """import polars as pl
import pyarrow as pa
import numpy as np
np.random.seed(0)
n = 100_000
# Create Polars DataFrame and convert to Arrow
df = pl.DataFrame({
    "id":      np.arange(n),
    "score":   np.random.randn(n),
    "category":np.random.choice(["A","B","C"], n),
    "amount":  np.random.lognormal(4, 1, n),
})
# Polars -> Arrow -> Polars (zero-copy where possible)
arrow_table = df.to_arrow()
print(f"Arrow schema: {arrow_table.schema}")
print(f"Num chunks: {arrow_table.column('score').num_chunks}")
# Compute with pyarrow
import pyarrow.compute as pc
mean_score = pc.mean(arrow_table.column("score"))
print(f"Mean score via pyarrow: {mean_score.as_py():.6f}")
# Back to Polars
df2 = pl.from_arrow(arrow_table)
print(f"Roundtrip OK: {df.shape == df2.shape}")"""

pl16_c2 = """import polars as pl
import numpy as np
import tempfile, os, time
np.random.seed(1)
n = 500_000
df = pl.DataFrame({
    "id":       np.arange(n),
    "group":    np.random.choice(["X","Y","Z","W"], n),
    "value":    np.random.randn(n),
    "amount":   np.random.lognormal(3, 1.5, n),
    "flag":     np.random.randint(0, 2, n).astype(bool),
})
tmp_parquet = tempfile.mktemp(suffix=".parquet")
tmp_csv     = tempfile.mktemp(suffix=".csv")
# Write and read Parquet vs CSV
t0 = time.perf_counter()
df.write_parquet(tmp_parquet, compression="snappy")
t1 = time.perf_counter()
df.write_csv(tmp_csv)
t2 = time.perf_counter()
df_pq = pl.read_parquet(tmp_parquet)
t3 = time.perf_counter()
df_csv = pl.read_csv(tmp_csv)
t4 = time.perf_counter()
pq_mb  = os.path.getsize(tmp_parquet) / 1e6
csv_mb = os.path.getsize(tmp_csv) / 1e6
print(f"Parquet: write={t1-t0:.3f}s read={t3-t2:.3f}s size={pq_mb:.1f}MB")
print(f"CSV:     write={t2-t1:.3f}s read={t4-t3:.3f}s size={csv_mb:.1f}MB")
for f in [tmp_parquet, tmp_csv]: os.unlink(f)"""

pl16_c3 = """import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import tempfile, os
np.random.seed(2)
n = 200_000
df = pl.DataFrame({
    "year":   np.random.choice([2021,2022,2023], n),
    "region": np.random.choice(["NA","EU","APAC"], n),
    "product":np.random.choice(["A","B","C","D"], n),
    "revenue":np.random.lognormal(5, 1, n),
    "units":  np.random.poisson(50, n),
})
# Write partitioned parquet (by year+region) via pyarrow
arrow_table = df.to_arrow()
tmpdir = tempfile.mkdtemp()
pq.write_to_dataset(arrow_table, root_path=tmpdir,
                    partition_cols=["year","region"])
# Read only 2023 NA partition with Polars scan
result = (
    pl.scan_parquet(f"{tmpdir}/year=2023/region=NA/**/*.parquet")
    .group_by("product")
    .agg(pl.col("revenue").sum(), pl.col("units").sum())
    .collect()
)
print(f"2023 NA partition result:"); print(result)
import shutil; shutil.rmtree(tmpdir)"""

pl16_ps = """import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import tempfile, os, time
np.random.seed(33)
n = 1_000_000
df = pl.DataFrame({
    "date":       np.random.choice(["2022","2023","2024"], n),
    "country":    np.random.choice(["US","UK","DE","FR","JP"], n),
    "category":   np.random.choice(["A","B","C","D","E"], n),
    "sales":      np.random.lognormal(4, 1.5, n),
    "cost":       np.random.lognormal(3.5, 1.2, n),
    "units":      np.random.poisson(100, n),
})
# TODO: Write partitioned parquet by date+country using pyarrow
# TODO: Read only 2024 US partition using pl.scan_parquet
# TODO: Compute: total sales, total cost, margin, units per category for 2024 US
# TODO: Benchmark: read whole parquet vs partitioned scan for single partition
# TODO: Convert to Arrow table and compute gross_margin with pyarrow.compute
"""

pl16 = make_section4(
    "16", "Polars with Apache Arrow & Parquet",
    "Polars is built on Apache Arrow, enabling zero-copy interop with PyArrow, DuckDB, and other Arrow-native tools. Write partitioned Parquet files for efficient partial reads in production data pipelines.",
    "Polars <-> PyArrow Interoperability", pl16_c1,
    "Parquet vs CSV: Speed & Size Benchmark", pl16_c2,
    "Partitioned Parquet with PyArrow + Polars scan", pl16_c3,
    rw_scenario="Data lake pipeline: store 5 years of IoT sensor readings in Parquet partitioned by year+device_type, then query a single partition with pl.scan_parquet to compute hourly aggregates without reading the full dataset.",
    rw_code="""import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import tempfile, os, shutil
np.random.seed(5)
n = 200_000
df = pl.DataFrame({
    "year":        np.random.choice([2021,2022,2023], n),
    "device_type": np.random.choice(["sensor","camera","gateway"], n),
    "timestamp_h": np.random.randint(0, 24, n),
    "temperature": np.random.normal(22, 5, n),
    "humidity":    np.random.normal(60, 10, n),
    "power_kw":    np.random.lognormal(1, 0.5, n),
})
tmpdir = tempfile.mkdtemp()
pq.write_to_dataset(df.to_arrow(), root_path=tmpdir,
                    partition_cols=["year","device_type"])
# Read only 2023 sensors
result = (
    pl.scan_parquet(f"{tmpdir}/year=2023/device_type=sensor/**/*.parquet")
    .group_by("timestamp_h")
    .agg([
        pl.col("temperature").mean().alias("avg_temp"),
        pl.col("power_kw").sum().alias("total_power"),
        pl.col("humidity").std().alias("hum_std"),
    ])
    .sort("timestamp_h")
    .collect()
)
print(f"2023 sensor hourly aggregates ({len(result)} hours):")
print(result.head(5))
shutil.rmtree(tmpdir)""",
    pt="1M-Row Partitioned Analytics",
    pd="Write 1M rows of sales data partitioned by date+country using PyArrow. Read only the 2024 US partition with pl.scan_parquet and compute margins. Benchmark whole-file read vs partitioned scan. Convert the result to Arrow and compute gross_margin using pyarrow.compute.",
    ps=pl16_ps
)

# ─── INSERT ──────────────────────────────────────────────────────────────────

sklearn_sections = sk14 + sk15 + sk16
polars_sections  = pl14 + pl15 + pl16

insert_code4(os.path.join(BASE, "gen_sklearn.py"), sklearn_sections)
insert_code4(os.path.join(BASE, "gen_polars.py"),  polars_sections)

print("Done!")
