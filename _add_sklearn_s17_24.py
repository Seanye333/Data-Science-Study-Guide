"""Add sections 17-24 to gen_sklearn.py (code1/code2/code3/code4 format)."""
import os, re

BASE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path"
FILE = os.path.join(BASE, "gen_sklearn.py")

def ct(code, indent="            "):
    """Convert multi-line code string to tuple-concatenation format."""
    lines = code.split('\n')
    parts = []
    for line in lines:
        escaped = line.replace('\\', '\\\\').replace('"', '\\"')
        parts.append(f'{indent}"{escaped}\\n"')
    return "(\n" + "\n".join(parts) + "\n        )"

def make_section(num, title, desc,
                 c1t, c1, c2t, c2, c3t=None, c3=None, c4t=None, c4=None,
                 rw_scenario="", rw_code="",
                 pt="", pd_text="", ps=""):
    s  = f'    {{\n'
    s += f'        "title": "{num}. {title}",\n'
    s += f'        "desc": "{desc}",\n'
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
    s += f'        "rw_scenario": "{rw_scenario}",\n'
    s += f'        "rw_code": {ct(rw_code)},\n'
    s += f'        "practice": {{\n'
    s += f'            "title": "{pt}",\n'
    s += f'            "desc": "{pd_text}",\n'
    s += f'            "starter": {ct(ps)},\n'
    s += f'        }},\n'
    s += f'    }},\n'
    return s

def insert_before_make_html(filepath, new_sections_str):
    content = open(filepath, encoding='utf-8').read()
    marker = '\n]\n\n\ndef make_html'
    idx = content.find(marker)
    if idx == -1:
        print(f"ERROR: marker not found in {filepath}")
        return False
    before = content[:idx].rstrip()
    if before.endswith('}') and not before.endswith('},'):
        content = before + ',\n\n' + new_sections_str + content[idx:]
    else:
        content = content[:idx] + '\n' + new_sections_str + content[idx:]
    open(filepath, 'w', encoding='utf-8').write(content)
    print(f"OK: inserted sections into {filepath}")
    return True

# ── Section 17: Feature Engineering ─────────────────────────────────────────
s17 = make_section(17, "Feature Engineering",
    "Transform raw features into richer representations. PolynomialFeatures adds interactions and powers; FunctionTransformer applies any callable; custom transformers plug into Pipelines.",
    c1t="PolynomialFeatures and interaction terms",
    c1=
"""from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np

np.random.seed(42)
X, y = make_regression(n_samples=200, n_features=3, noise=10, random_state=42)
# Add a non-linear relationship
y += X[:, 0] ** 2 * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear model without features
lr = LinearRegression().fit(X_train, y_train)
print(f"Linear R2: {r2_score(y_test, lr.predict(X_test)):.4f}")

# Polynomial features (degree 2 adds x^2, x1*x2, etc.)
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_p = poly.fit_transform(X_train)
X_test_p  = poly.transform(X_test)

lr_poly = LinearRegression().fit(X_train_p, y_train)
print(f"Poly R2:   {r2_score(y_test, lr_poly.predict(X_test_p)):.4f}")
print(f"Features: {X_train.shape[1]} -> {X_train_p.shape[1]}")
print("Feature names:", poly.get_feature_names_out(['a','b','c'])[:6])""",
    c2t="FunctionTransformer for custom transformations",
    c2=
"""from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
import numpy as np, pandas as pd

np.random.seed(0)
n = 300
# Skewed feature — log-transform helps
X = np.column_stack([
    np.random.exponential(5, n),    # right-skewed
    np.random.normal(0, 1, n),      # already normal
    np.random.uniform(1, 100, n),   # uniform
])
y = 3 * np.log1p(X[:, 0]) + 2 * X[:, 1] + 0.1 * X[:, 2] + np.random.randn(n)

# FunctionTransformer: apply log1p to first column only
def log_transform(X):
    Xt = X.copy()
    Xt[:, 0] = np.log1p(np.abs(Xt[:, 0]))
    return Xt

log_pipe = Pipeline([
    ('log', FunctionTransformer(log_transform, validate=True)),
    ('ridge', Ridge(alpha=1.0)),
])

from sklearn.model_selection import cross_val_score
scores = cross_val_score(log_pipe, X, y, cv=5, scoring='r2')
print(f"Log-transform pipeline R2: {scores.mean():.4f} ± {scores.std():.4f}")""",
    c3t="Custom transformer with BaseEstimator and TransformerMixin",
    c3=
"""from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

class OutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, n_std=3.0):
        self.n_std = n_std

    def fit(self, X, y=None):
        self.mean_ = X.mean(axis=0)
        self.std_  = X.std(axis=0)
        return self

    def transform(self, X):
        lo = self.mean_ - self.n_std * self.std_
        hi = self.mean_ + self.n_std * self.std_
        return np.clip(X, lo, hi)

cancer = load_breast_cancer()
X_tr, X_te, y_tr, y_te = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42)

pipe = Pipeline([
    ('clip',    OutlierClipper(n_std=3.0)),
    ('scale',   StandardScaler()),
    ('clf',     LogisticRegression(max_iter=1000)),
])
pipe.fit(X_tr, y_tr)
print(f"Accuracy: {accuracy_score(y_te, pipe.predict(X_te)):.4f}")
print(f"Clipping params: mean={pipe['clip'].mean_[:3].round(2)}")""",
    c4t="ColumnTransformer for mixed-type data",
    c4=
"""from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np, pandas as pd

np.random.seed(42)
n = 400
df = pd.DataFrame({
    'age':     np.random.randint(18, 70, n).astype(float),
    'income':  np.random.exponential(40000, n),
    'score':   np.random.normal(600, 100, n),
    'region':  np.random.choice(['North','South','East','West'], n),
    'product': np.random.choice(['Basic','Premium','Enterprise'], n),
    'target':  np.random.choice([0, 1], n, p=[0.6, 0.4]),
})
# Inject some missing values
df.loc[df.sample(30).index, 'age'] = np.nan
df.loc[df.sample(20).index, 'income'] = np.nan

num_features = ['age', 'income', 'score']
cat_features = ['region', 'product']

num_pipe = Pipeline([
    ('impute', SimpleImputer(strategy='median')),
    ('scale',  StandardScaler()),
])
cat_pipe = Pipeline([
    ('impute', SimpleImputer(strategy='most_frequent')),
    ('ohe',    OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
])

preprocessor = ColumnTransformer([
    ('num', num_pipe, num_features),
    ('cat', cat_pipe, cat_features),
])

X = df.drop('target', axis=1)
y = df['target']

full_pipe = Pipeline([
    ('prep', preprocessor),
    ('clf',  RandomForestClassifier(n_estimators=100, random_state=42)),
])

scores = cross_val_score(full_pipe, X, y, cv=5, scoring='accuracy')
print(f"Mixed-type pipeline accuracy: {scores.mean():.4f} ± {scores.std():.4f}")
print(f"Input features: {X.shape[1]} | Encoded features: {preprocessor.fit_transform(X).shape[1]}")""",
    rw_scenario="E-Commerce: A churn prediction pipeline applies log-transform to purchase frequency, clips outliers in spending, one-hot encodes customer segment and region, then trains a classifier.",
    rw_code=
"""from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
import numpy as np, pandas as pd

np.random.seed(42)
n = 500
df = pd.DataFrame({
    'days_since_last': np.random.exponential(30, n),   # skewed
    'total_orders':    np.random.exponential(8, n),    # skewed
    'avg_order_val':   np.random.normal(85, 30, n).clip(10, 250),
    'support_tickets': np.random.poisson(1.5, n),
    'segment':         np.random.choice(['Bronze','Silver','Gold'], n),
    'country':         np.random.choice(['US','UK','DE','FR'], n),
    'churned':         np.random.choice([0,1], n, p=[0.75, 0.25]),
})

log_tf = FunctionTransformer(np.log1p)

num_pipe = Pipeline([
    ('log',   log_tf),
    ('scale', StandardScaler()),
])
cat_pipe = Pipeline([
    ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
])

prep = ColumnTransformer([
    ('num', num_pipe, ['days_since_last','total_orders','avg_order_val','support_tickets']),
    ('cat', cat_pipe, ['segment','country']),
])

pipe = Pipeline([
    ('prep', prep),
    ('clf',  GradientBoostingClassifier(n_estimators=100, random_state=42)),
])

X, y = df.drop('churned', axis=1), df['churned']
scores = cross_val_score(pipe, X, y, cv=5, scoring='roc_auc')
print(f"Churn ROC-AUC: {scores.mean():.4f} ± {scores.std():.4f}")""",
    pt="Price Prediction Feature Pipeline",
    pd_text="Build a feature engineering pipeline for house prices: (1) Apply log1p to 'sqft' and 'price' (target), (2) Add PolynomialFeatures(degree=2) on numerical features, (3) OneHotEncode 'neighborhood'. Use ColumnTransformer + Pipeline. Report R2 with 5-fold CV.",
    ps=
"""from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
import numpy as np, pandas as pd

np.random.seed(42)
n = 400
df = pd.DataFrame({
    'sqft':         np.random.exponential(1500, n).clip(500, 5000),
    'bedrooms':     np.random.randint(1, 6, n).astype(float),
    'bathrooms':    np.random.randint(1, 4, n).astype(float),
    'age':          np.random.randint(0, 50, n).astype(float),
    'neighborhood': np.random.choice(['A','B','C','D'], n),
    'price':        None,
})
df['price'] = (np.log1p(df['sqft']) * 50000 +
               df['bedrooms'] * 15000 +
               df['bathrooms'] * 10000 -
               df['age'] * 500 +
               np.random.randn(n) * 10000).clip(80000, 800000)

X = df.drop('price', axis=1)
y = np.log1p(df['price'])

num_features = ['sqft','bedrooms','bathrooms','age']
cat_features = ['neighborhood']

# TODO: build num_pipe (FunctionTransformer log1p + PolynomialFeatures + StandardScaler)
# TODO: build cat_pipe (OneHotEncoder)
# TODO: ColumnTransformer + Pipeline with Ridge
# TODO: cross_val_score with cv=5, scoring='r2'
""")

# ── Section 18: ROC Curves & Advanced Metrics ────────────────────────────────
s18 = make_section(18, "ROC Curves & Advanced Metrics",
    "ROC-AUC and Precision-Recall curves reveal classifier performance beyond accuracy. Use them to select thresholds, compare models, and diagnose class imbalance issues.",
    c1t="ROC curve and AUC with multiple models",
    c1=
"""from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

cancer = load_breast_cancer()
X_tr, X_te, y_tr, y_te = train_test_split(
    cancer.data, cancer.target, test_size=0.25, random_state=42, stratify=cancer.target)

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest':       RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting':   GradientBoostingClassifier(n_estimators=100, random_state=42),
}

for name, model in models.items():
    model.fit(X_tr, y_tr)
    proba = model.predict_proba(X_te)[:, 1]
    fpr, tpr, _ = roc_curve(y_te, proba)
    auc = roc_auc_score(y_te, proba)
    print(f"{name:25s}  AUC = {auc:.4f}")""",
    c2t="Precision-Recall curve and optimal threshold",
    c2=
"""from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve, average_precision_score, f1_score
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=1000, weights=[0.85, 0.15],
                            n_features=10, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                            stratify=y, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)
proba = model.predict_proba(X_te)[:, 1]

precision, recall, thresholds = precision_recall_curve(y_te, proba)
ap = average_precision_score(y_te, proba)
print(f"Average Precision: {ap:.4f}")

# Find threshold that maximizes F1
f1s = 2 * precision[:-1] * recall[:-1] / (precision[:-1] + recall[:-1] + 1e-9)
best_idx = np.argmax(f1s)
best_thresh = thresholds[best_idx]
print(f"Best F1 threshold: {best_thresh:.3f}  |  F1={f1s[best_idx]:.4f}")
print(f"At threshold {best_thresh:.3f}: precision={precision[best_idx]:.3f}, recall={recall[best_idx]:.3f}")

# Apply custom threshold
y_pred = (proba >= best_thresh).astype(int)
print(f"F1 with custom threshold: {f1_score(y_te, y_pred):.4f}")""",
    c3t="Confusion matrix, classification report, calibration",
    c3=
"""from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (confusion_matrix, classification_report,
                              ConfusionMatrixDisplay)
import numpy as np

digits = load_digits()
X_tr, X_te, y_tr, y_te = train_test_split(
    digits.data, digits.target, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)
y_pred = model.predict(X_te)

print("Classification Report:")
print(classification_report(y_te, y_pred, digits=3))

cm = confusion_matrix(y_te, y_pred)
# Find the most confused classes
np.fill_diagonal(cm, 0)  # zero out correct predictions
i, j = np.unravel_index(cm.argmax(), cm.shape)
print(f"Most confused: digit {i} predicted as {j} ({cm[i,j]} times)")""",
    c4t="Multi-class ROC with one-vs-rest",
    c4=
"""from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score
import numpy as np

iris = load_iris()
X_tr, X_te, y_tr, y_te = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42, stratify=iris.target)

model = LogisticRegression(multi_class='ovr', max_iter=200)
model.fit(X_tr, y_tr)
proba = model.predict_proba(X_te)

# One-vs-Rest AUC for each class
y_bin = label_binarize(y_te, classes=[0, 1, 2])
for i, name in enumerate(iris.target_names):
    auc = roc_auc_score(y_bin[:, i], proba[:, i])
    print(f"  {name:12s}  AUC = {auc:.4f}")

macro_auc = roc_auc_score(y_bin, proba, average='macro')
micro_auc = roc_auc_score(y_bin, proba, average='micro')
print(f"Macro AUC: {macro_auc:.4f}  |  Micro AUC: {micro_auc:.4f}")""",
    rw_scenario="Credit Risk: A bank compares ROC-AUC and PR-AUC for fraud detection models. They select the threshold maximizing recall at 90% while monitoring precision to minimize false positive customer blocks.",
    rw_code=
"""from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (roc_auc_score, average_precision_score,
                              precision_recall_curve, confusion_matrix)
import numpy as np

np.random.seed(42)
X, y = make_classification(
    n_samples=5000, n_features=15, n_informative=8,
    weights=[0.97, 0.03], flip_y=0.01, random_state=42)

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

gbc = GradientBoostingClassifier(n_estimators=200, max_depth=4,
                                  learning_rate=0.05, random_state=42)
gbc.fit(X_tr, y_tr)
proba = gbc.predict_proba(X_te)[:, 1]

print(f"ROC-AUC:          {roc_auc_score(y_te, proba):.4f}")
print(f"Avg Precision:    {average_precision_score(y_te, proba):.4f}")

# Find threshold for recall >= 0.90
precision, recall, thresholds = precision_recall_curve(y_te, proba)
high_recall_mask = recall[:-1] >= 0.90
if high_recall_mask.any():
    best_prec = precision[:-1][high_recall_mask].max()
    best_thr  = thresholds[high_recall_mask][precision[:-1][high_recall_mask].argmax()]
    print(f"At recall>=90%: threshold={best_thr:.3f}, precision={best_prec:.3f}")
    y_pred = (proba >= best_thr).astype(int)
    cm = confusion_matrix(y_te, y_pred)
    print(f"Confusion matrix:\\n{cm}")""",
    pt="Threshold Tuning for Recall",
    pd_text="Train a RandomForest on an imbalanced dataset (weights=[0.9,0.1], 2000 samples). Plot the precision-recall trade-off (print precision and recall at 10 evenly-spaced thresholds). Find and print the threshold that achieves recall >= 0.85 with the highest precision. Show the confusion matrix at that threshold.",
    ps=
"""from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve, confusion_matrix
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=2000, n_features=10, weights=[0.9,0.1],
                            random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                            stratify=y, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)
proba = model.predict_proba(X_te)[:, 1]

precision, recall, thresholds = precision_recall_curve(y_te, proba)

# TODO: print precision/recall at 10 evenly-spaced thresholds
# TODO: find threshold giving recall >= 0.85 with max precision
# TODO: print confusion matrix at that threshold
""")

# ── Section 19: Gradient Boosting ────────────────────────────────────────────
s19 = make_section(19, "Gradient Boosting",
    "Gradient Boosting sequentially trains shallow trees, each correcting prior errors. sklearn offers GradientBoostingClassifier and the faster HistGradientBoosting (native categorical support, faster on large data).",
    c1t="GradientBoostingClassifier with learning rate tuning",
    c1=
"""from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score
import numpy as np

cancer = load_breast_cancer()
X_tr, X_te, y_tr, y_te = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42, stratify=cancer.target)

# Compare learning rates (lower rate = more trees needed but often better)
for lr in [0.3, 0.1, 0.05]:
    gbc = GradientBoostingClassifier(
        n_estimators=200, learning_rate=lr,
        max_depth=3, subsample=0.8,
        random_state=42
    )
    gbc.fit(X_tr, y_tr)
    auc = roc_auc_score(y_te, gbc.predict_proba(X_te)[:, 1])
    print(f"lr={lr:.2f}  n_est=200  AUC={auc:.4f}")

# Best model with early stopping via staged_predict
best = GradientBoostingClassifier(n_estimators=300, learning_rate=0.05,
                                   max_depth=3, subsample=0.8, random_state=42)
best.fit(X_tr, y_tr)
staged_aucs = [roc_auc_score(y_te, p[:, 1])
               for p in best.staged_predict_proba(X_te)]
best_n = int(np.argmax(staged_aucs)) + 1
print(f"Best n_estimators via staged: {best_n}  AUC={staged_aucs[best_n-1]:.4f}")""",
    c2t="HistGradientBoostingClassifier (faster, supports NaN)",
    c2=
"""from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=10000, n_features=20,
                            n_informative=12, random_state=42)

# Inject missing values (HistGB handles NaN natively!)
mask = np.random.random(X.shape) < 0.05
X[mask] = np.nan

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

hgb = HistGradientBoostingClassifier(
    max_iter=300,
    learning_rate=0.05,
    max_depth=5,
    min_samples_leaf=20,
    early_stopping=True,   # built-in early stopping
    validation_fraction=0.1,
    n_iter_no_change=20,
    random_state=42,
)
hgb.fit(X_tr, y_tr)

auc = roc_auc_score(y_te, hgb.predict_proba(X_te)[:, 1])
print(f"HistGB AUC: {auc:.4f}")
print(f"Iterations used: {hgb.n_iter_}  (early stopped from max 300)")
print(f"NaN features handled: {mask.sum()} missing values")""",
    c3t="Feature importances and partial dependence",
    c3=
"""from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.inspection import partial_dependence
import numpy as np

cancer = load_breast_cancer()
X_tr, X_te, y_tr, y_te = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42)

gbc = GradientBoostingClassifier(n_estimators=200, max_depth=3,
                                  learning_rate=0.1, random_state=42)
gbc.fit(X_tr, y_tr)

# Feature importances (mean impurity decrease)
importances = gbc.feature_importances_
top5_idx = np.argsort(importances)[-5:][::-1]
print("Top 5 features by importance:")
for idx in top5_idx:
    print(f"  [{idx:2d}] {cancer.feature_names[idx]:30s}  {importances[idx]:.4f}")

# Partial dependence for top feature
top_feat = top5_idx[0]
pdp = partial_dependence(gbc, X_tr, features=[top_feat], kind='average')
print(f"\nPartial dependence for '{cancer.feature_names[top_feat]}':")
vals = pdp['grid_values'][0]
avgs = pdp['average'][0]
for v, a in zip(vals[::5], avgs[::5]):
    print(f"  x={v:.2f}  ->  mean prediction={a:.4f}")""",
    c4t="GBM vs RF vs HistGB comparison",
    c4=
"""from sklearn.ensemble import (GradientBoostingClassifier,
                               RandomForestClassifier,
                               HistGradientBoostingClassifier)
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
import numpy as np, time

np.random.seed(42)
X, y = make_classification(n_samples=5000, n_features=20,
                            n_informative=10, random_state=42)

models = {
    'RandomForest':          RandomForestClassifier(n_estimators=200, random_state=42),
    'GradientBoosting':      GradientBoostingClassifier(n_estimators=200, random_state=42),
    'HistGradientBoosting':  HistGradientBoostingClassifier(max_iter=200, random_state=42),
}

print(f"{'Model':25s}  {'ROC-AUC':>8s}  {'Time(s)':>8s}")
print('-' * 48)
for name, model in models.items():
    t0 = time.time()
    scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
    elapsed = time.time() - t0
    print(f"{name:25s}  {scores.mean():.4f}    {elapsed:.2f}s")""",
    rw_scenario="Customer Lifetime Value: An e-commerce team trains a GBM to predict whether a customer will become high-LTV. They use staged_predict_proba for early stopping and inspect feature importances to guide feature engineering.",
    rw_code=
"""from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, classification_report
import numpy as np, pandas as pd

np.random.seed(42)
n = 3000
df = pd.DataFrame({
    'orders_6m':    np.random.poisson(3, n),
    'avg_value':    np.random.exponential(75, n),
    'days_active':  np.random.randint(1, 365, n),
    'support_calls':np.random.poisson(0.8, n),
    'email_opens':  np.random.binomial(20, 0.3, n),
    'category_pref':np.random.choice([0, 1, 2, 3], n),  # categorical
})
df['high_ltv'] = ((df['orders_6m'] > 4) &
                  (df['avg_value'] > 80) &
                  (df['days_active'] > 180)).astype(int)

X = df.drop('high_ltv', axis=1).values
y = df['high_ltv'].values
X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y,
                                            test_size=0.2, random_state=42)

# HistGB natively handles integers as potential categoricals
model = HistGradientBoostingClassifier(
    max_iter=500, learning_rate=0.05,
    max_depth=5, early_stopping=True,
    n_iter_no_change=25, random_state=42,
)
model.fit(X_tr, y_tr)
proba = model.predict_proba(X_te)[:, 1]

print(f"ROC-AUC: {roc_auc_score(y_te, proba):.4f}")
print(f"Iterations: {model.n_iter_}")
print(classification_report(y_te, model.predict(X_te)))""",
    pt="GBM Hyperparameter Grid Search",
    pd_text="Use GridSearchCV with GradientBoostingClassifier on the breast cancer dataset. Search over: n_estimators=[100,200], learning_rate=[0.05,0.1], max_depth=[2,3,4]. Use 5-fold CV with ROC-AUC. Print the best params, best score, and the top 5 parameter combinations.",
    ps=
"""from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import numpy as np

cancer = load_breast_cancer()
X_tr, X_te, y_tr, y_te = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42)

param_grid = {
    'n_estimators':  [100, 200],
    'learning_rate': [0.05, 0.1],
    'max_depth':     [2, 3, 4],
}

# TODO: create GridSearchCV with GradientBoostingClassifier, 5-fold, roc_auc scoring
# TODO: fit on X_tr, y_tr
# TODO: print best_params_, best_score_
# TODO: print top 5 parameter combinations from cv_results_
""")

# ── Section 20: Regularized Regression ──────────────────────────────────────
s20 = make_section(20, "Regularized Regression",
    "Ridge (L2), Lasso (L1), and ElasticNet combine least squares with regularization penalties. Lasso performs feature selection by zeroing coefficients; Ridge shrinks them. Use CV variants to auto-select alpha.",
    c1t="Ridge vs Lasso vs ElasticNet comparison",
    c1=
"""from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.pipeline import Pipeline
import numpy as np

np.random.seed(42)
X, y, coef = make_regression(n_samples=200, n_features=50, n_informative=10,
                              noise=10, coef=True, random_state=42)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=42)

models = {
    'Ridge':     Ridge(alpha=1.0),
    'Lasso':     Lasso(alpha=1.0, max_iter=5000),
    'ElasticNet':ElasticNet(alpha=1.0, l1_ratio=0.5, max_iter=5000),
}

print(f"{'Model':12s}  {'R2':>7s}  {'RMSE':>8s}  {'Non-zero coefs':>14s}")
print('-' * 50)
for name, model in models.items():
    pipe = Pipeline([('scale', StandardScaler()), ('reg', model)])
    pipe.fit(X_tr, y_tr)
    y_pred = pipe.predict(X_te)
    r2   = r2_score(y_te, y_pred)
    rmse = mean_squared_error(y_te, y_pred, squared=False)
    nz   = (pipe['reg'].coef_ != 0).sum()
    print(f"{name:12s}  {r2:7.4f}  {rmse:8.2f}  {nz:>14d}")""",
    c2t="RidgeCV and LassoCV for automatic alpha selection",
    c2=
"""from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np

np.random.seed(42)
X, y = make_regression(n_samples=300, n_features=40, n_informative=12,
                        noise=15, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

alphas = np.logspace(-3, 3, 50)

for ModelCV, name in [(RidgeCV, 'RidgeCV'), (LassoCV, 'LassoCV')]:
    if name == 'LassoCV':
        pipe = Pipeline([('s', StandardScaler()),
                         ('m', ModelCV(alphas=alphas, cv=5, max_iter=5000))])
    else:
        pipe = Pipeline([('s', StandardScaler()),
                         ('m', ModelCV(alphas=alphas, cv=5))])
    pipe.fit(X_tr, y_tr)
    model = pipe['m']
    r2 = r2_score(y_te, pipe.predict(X_te))
    nz = (model.coef_ != 0).sum()
    print(f"{name:10s}  best alpha={model.alpha_:.4f}  R2={r2:.4f}  non-zero={nz}")""",
    c3t="Regularization path — how coefficients shrink",
    c3=
"""from sklearn.linear_model import lasso_path
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler
import numpy as np

diabetes = load_diabetes()
X = StandardScaler().fit_transform(diabetes.data)
y = diabetes.target

# Compute Lasso path
alphas, coefs, _ = lasso_path(X, y, eps=1e-3, n_alphas=100)

# Show which features survive at each regularization level
feature_names = diabetes.feature_names
checkpoints = [0, 25, 50, 75, 99]

print(f"{'Alpha':>10s}  {'Active features'}")
print('-' * 60)
for i in checkpoints:
    active = [feature_names[j] for j in range(len(feature_names))
              if abs(coefs[j, i]) > 1e-4]
    print(f"{alphas[i]:10.4f}  {active}")

# Feature that persists longest (most important)
last_active = np.argmax([(coefs[j] != 0).sum() for j in range(len(feature_names))])
print(f"\nMost robust feature: {feature_names[last_active]}")""",
    c4t="ElasticNet for correlated features",
    c4=
"""from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np

np.random.seed(42)
n, p = 200, 20
# Correlated features: add collinear pairs
X = np.random.randn(n, p // 2)
X = np.hstack([X, X + np.random.randn(n, p // 2) * 0.1])  # pairs of correlated features
true_coef = np.array([3, -2, 1.5, 0, 0] * (p // 10) + [0] * (p - p // 10 * 5))[:p]
y = X @ true_coef + np.random.randn(n) * 2

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

# Elastic net handles correlated features better than Lasso
# (Lasso tends to pick one from each correlated group arbitrarily)
l1_ratios = [0.1, 0.5, 0.9]  # 0=Ridge, 1=Lasso
enet = ElasticNetCV(l1_ratio=l1_ratios, alphas=np.logspace(-3, 1, 30),
                    cv=5, max_iter=5000)
pipe = Pipeline([('scale', StandardScaler()), ('enet', enet)])
pipe.fit(X_tr, y_tr)

r2 = r2_score(y_te, pipe.predict(X_te))
print(f"ElasticNetCV R2: {r2:.4f}")
print(f"Best alpha: {pipe['enet'].alpha_:.4f}")
print(f"Best l1_ratio: {pipe['enet'].l1_ratio_:.2f}")
print(f"Non-zero coefs: {(pipe['enet'].coef_ != 0).sum()} / {p}")""",
    rw_scenario="Genomics: A biostatistician uses Lasso to select predictive SNPs (genetic markers) from thousands of features for a disease outcome, leveraging sparsity to identify the most relevant markers.",
    rw_code=
"""from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np, pandas as pd

np.random.seed(42)
n_samples = 300
n_snps    = 500  # many features (SNPs), few truly predictive

# Simulate SNP data (binary 0/1/2 alleles)
X = np.random.choice([0, 1, 2], size=(n_samples, n_snps))

# Only 10 SNPs truly predict the outcome
true_snps = np.random.choice(n_snps, 10, replace=False)
true_coef = np.zeros(n_snps)
true_coef[true_snps] = np.random.randn(10) * 2

y = X @ true_coef + np.random.randn(n_samples) * 3
feature_names = [f'SNP_{i:04d}' for i in range(n_snps)]

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([
    ('scale', StandardScaler()),
    ('lasso', LassoCV(cv=5, max_iter=10000, n_alphas=50)),
])
pipe.fit(X_tr, y_tr)
lasso = pipe['lasso']

selected = np.where(lasso.coef_ != 0)[0]
true_found = len(set(selected) & set(true_snps))
print(f"R2: {r2_score(y_te, pipe.predict(X_te)):.4f}")
print(f"Best alpha: {lasso.alpha_:.4f}")
print(f"Selected {len(selected)} SNPs | True SNPs recovered: {true_found}/10")
print("Top selected:", [feature_names[i] for i in selected[:5]])""",
    pt="Regularization Strength Sweep",
    pd_text="Load the diabetes dataset. For Lasso with alpha in [0.01, 0.1, 1, 10, 100], print: alpha, R2 on test set, number of non-zero coefficients, and which features survive (by name). Do the same for Ridge. Conclude: which alpha gives the best test R2 for each method?",
    ps=
"""from sklearn.datasets import load_diabetes
from sklearn.linear_model import Lasso, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np

diabetes = load_diabetes()
X, y = diabetes.data, diabetes.target
names = diabetes.feature_names
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

alphas = [0.01, 0.1, 1, 10, 100]

print("=== Lasso ===")
for alpha in alphas:
    # TODO: Pipeline StandardScaler + Lasso(alpha, max_iter=5000)
    # TODO: fit, predict, r2, non-zero coefs, surviving feature names
    pass

print("\n=== Ridge ===")
for alpha in alphas:
    # TODO: same for Ridge
    pass
""")

# ── Section 21: Model Persistence ────────────────────────────────────────────
s21 = make_section(21, "Model Persistence & Deployment",
    "Save trained models with joblib (recommended) or pickle. Version models with metadata, validate loaded models before serving, and use pipelines to ensure preprocessing is saved too.",
    c1t="joblib save/load and pipeline persistence",
    c1=
"""import joblib, os, tempfile
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

iris = load_iris()
X_tr, X_te, y_tr, y_te = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42)

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf',    RandomForestClassifier(n_estimators=100, random_state=42)),
])
pipe.fit(X_tr, y_tr)
acc_before = accuracy_score(y_te, pipe.predict(X_te))
print(f"Accuracy before save: {acc_before:.4f}")

# Save with joblib
model_path = os.path.join(tempfile.gettempdir(), 'iris_pipeline.joblib')
joblib.dump(pipe, model_path, compress=3)  # compress=3 reduces file size
size_kb = os.path.getsize(model_path) / 1024
print(f"Saved to: {model_path}  ({size_kb:.1f} KB)")

# Load and verify
loaded = joblib.load(model_path)
acc_after = accuracy_score(y_te, loaded.predict(X_te))
print(f"Accuracy after load: {acc_after:.4f}")
print(f"Models identical: {acc_before == acc_after}")
print(f"Loaded type: {type(loaded)}")""",
    c2t="Model versioning with metadata",
    c2=
"""import joblib, json, os, tempfile, hashlib
from datetime import datetime
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

cancer = load_breast_cancer()
X_tr, X_te, y_tr, y_te = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42)

model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)
auc = roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])

# Build a model bundle with metadata
bundle = {
    'model':    model,
    'metadata': {
        'version':          'v1.2.0',
        'trained_at':       datetime.now().isoformat(),
        'sklearn_version':  __import__('sklearn').__version__,
        'python_version':   __import__('sys').version.split()[0],
        'train_samples':    len(X_tr),
        'features':         list(cancer.feature_names),
        'target':           'malignant',
        'metrics': {
            'roc_auc_test': round(auc, 4),
        },
    },
}

path = os.path.join(tempfile.gettempdir(), 'model_v120.joblib')
joblib.dump(bundle, path)

# Reload and validate
loaded = joblib.load(path)
meta = loaded['metadata']
print(f"Version:   {meta['version']}")
print(f"Trained:   {meta['trained_at']}")
print(f"AUC:       {meta['metrics']['roc_auc_test']}")
print(f"Features:  {len(meta['features'])}")
print(f"Sklearn:   {meta['sklearn_version']}")""",
    c3t="Pickle protocol and cross-version safety checks",
    c3=
"""import pickle, os, tempfile, warnings
import sklearn
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

wine = load_wine()
X_tr, X_te, y_tr, y_te = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42)

pipe = Pipeline([('scaler', StandardScaler()), ('svc', SVC(probability=True))])
pipe.fit(X_tr, y_tr)

path = os.path.join(tempfile.gettempdir(), 'wine_svc.pkl')

# Save with highest protocol (fastest, most compact)
with open(path, 'wb') as f:
    pickle.dump({'model': pipe, 'sklearn_version': sklearn.__version__},
                f, protocol=pickle.HIGHEST_PROTOCOL)

size_kb = os.path.getsize(path) / 1024
print(f"Saved ({size_kb:.1f} KB, protocol {pickle.HIGHEST_PROTOCOL})")

# Load with version check
with open(path, 'rb') as f:
    data = pickle.load(f)

saved_ver = data['sklearn_version']
curr_ver  = sklearn.__version__
if saved_ver != curr_ver:
    warnings.warn(f"sklearn version mismatch: saved={saved_ver}, current={curr_ver}")
else:
    print(f"Version OK: {curr_ver}")

acc = accuracy_score(y_te, data['model'].predict(X_te))
print(f"Accuracy after reload: {acc:.4f}")""",
    rw_scenario="MLOps: A prediction service loads a versioned joblib bundle at startup, validates the sklearn version matches, logs the model metadata, and serves predictions with confidence scores.",
    rw_code=
"""import joblib, os, tempfile
from datetime import datetime
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# --- Training phase ---
iris = load_iris()
X_tr, X_te, y_tr, y_te = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42)

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf',    RandomForestClassifier(n_estimators=100, random_state=42)),
])
pipe.fit(X_tr, y_tr)

model_dir = tempfile.mkdtemp()
path = os.path.join(model_dir, 'model_v1.joblib')
joblib.dump({'model': pipe,
             'version': 'v1.0',
             'features': list(iris.feature_names),
             'classes':  list(iris.target_names),
             'trained_at': datetime.now().isoformat(),
             'test_accuracy': accuracy_score(y_te, pipe.predict(X_te))},
            path)
print(f"Model saved: {path}")

# --- Serving phase ---
def load_model(path):
    bundle = joblib.load(path)
    print(f"Loaded {bundle['version']} | acc={bundle['test_accuracy']:.4f}")
    print(f"Features: {bundle['features']}")
    return bundle

def predict(bundle, X):
    model   = bundle['model']
    classes = bundle['classes']
    preds   = model.predict(X)
    probas  = model.predict_proba(X)
    return [{'class': classes[p], 'confidence': float(probas[i].max())}
            for i, p in enumerate(preds)]

bundle = load_model(path)
samples = iris.data[:3]
results = predict(bundle, samples)
for i, r in enumerate(results):
    print(f"Sample {i+1}: {r['class']} (conf={r['confidence']:.3f})")""",
    pt="Save and Reload Comparison",
    pd_text="Train two models on wine dataset (RandomForest and GradientBoosting). Save both with joblib including metadata (accuracy, params, date). Write a function compare_models(paths) that loads all saved models and prints a comparison table (name, accuracy, train time, file size KB). Save as 'models/' directory.",
    ps=
"""import joblib, os, time, tempfile
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import datetime

wine = load_wine()
X_tr, X_te, y_tr, y_te = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42)

models_dir = os.path.join(tempfile.gettempdir(), 'models')
os.makedirs(models_dir, exist_ok=True)

model_configs = {
    'random_forest':     RandomForestClassifier(n_estimators=100, random_state=42),
    'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
}

for name, model in model_configs.items():
    # TODO: time the training, compute accuracy
    # TODO: save bundle with metadata (name, accuracy, params, trained_at)
    # TODO: save to models_dir/{name}.joblib
    pass

def compare_models(directory):
    # TODO: load all .joblib files, print comparison table
    pass

compare_models(models_dir)
""")

# ── Section 22: Text Classification Pipeline ─────────────────────────────────
s22 = make_section(22, "Text Classification Pipeline",
    "sklearn's TfidfVectorizer and CountVectorizer convert text to numerical features. Combine them in a Pipeline with classifiers to build spam detectors, sentiment analyzers, and topic classifiers.",
    c1t="TF-IDF + Logistic Regression for text classification",
    c1=
"""from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
import numpy as np

# Simulate sentiment dataset
positive = [
    "I love this product! It works great.",
    "Excellent quality and fast delivery.",
    "Best purchase ever, highly recommend.",
    "Amazing service, very satisfied.",
    "Outstanding performance, exceeded expectations.",
    "Wonderful experience, will buy again.",
    "Perfect product, exactly as described.",
    "Fantastic value for money.",
] * 15

negative = [
    "Terrible product, broke after one day.",
    "Very disappointed, not as advertised.",
    "Waste of money, poor quality.",
    "Awful experience, do not buy.",
    "Horrible customer service.",
    "Complete junk, returned immediately.",
    "Worst purchase ever made.",
    "Very poor quality, falls apart.",
] * 15

texts  = positive + negative
labels = [1] * len(positive) + [0] * len(negative)

X_tr, X_te, y_tr, y_te = train_test_split(texts, labels, test_size=0.2,
                                            random_state=42, stratify=labels)
pipe = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_features=5000,
                               sublinear_tf=True, min_df=2)),
    ('clf',   LogisticRegression(C=1.0, max_iter=1000)),
])
pipe.fit(X_tr, y_tr)
print(classification_report(y_te, pipe.predict(X_te),
                             target_names=['Negative','Positive']))

# Feature importance: top words per class
vocab = pipe['tfidf'].vocabulary_
coef  = pipe['clf'].coef_[0]
top_pos = sorted(vocab, key=lambda w: -coef[vocab[w]])[:5]
top_neg = sorted(vocab, key=lambda w:  coef[vocab[w]])[:5]
print("Top positive words:", top_pos)
print("Top negative words:", top_neg)""",
    c2t="CountVectorizer + Multinomial Naive Bayes (fast baseline)",
    c2=
"""from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.datasets import fetch_20newsgroups
import numpy as np

# Load a subset of 20 newsgroups (4 categories)
categories = ['sci.space', 'rec.sport.hockey', 'talk.politics.guns', 'comp.graphics']
data = fetch_20newsgroups(subset='all', categories=categories,
                          remove=('headers', 'footers', 'quotes'),
                          random_state=42)

pipe = Pipeline([
    ('cv',    CountVectorizer(stop_words='english', max_features=20000, min_df=2)),
    ('tfidf', TfidfTransformer(sublinear_tf=True)),
    ('nb',    MultinomialNB(alpha=0.1)),
])

scores = cross_val_score(pipe, data.data, data.target, cv=5, scoring='accuracy')
print(f"Multinomial NB accuracy: {scores.mean():.4f} ± {scores.std():.4f}")
print(f"Categories: {categories}")
print(f"Dataset: {len(data.data)} documents")

# Quick prediction demo
pipe.fit(data.data, data.target)
test_texts = [
    "NASA launched a new rocket to Mars last week",
    "The hockey team won the championship finals",
]
preds = pipe.predict(test_texts)
for text, pred in zip(test_texts, preds):
    print(f"  '{text[:45]}...' -> {data.target_names[pred]}")""",
    c3t="TF-IDF with GridSearch for hyperparameter tuning",
    c3=
"""from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import fetch_20newsgroups
import numpy as np

categories = ['sci.med', 'sci.space', 'comp.graphics']
data = fetch_20newsgroups(subset='train', categories=categories,
                          remove=('headers','footers','quotes'))

pipe = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('svc',   LinearSVC(max_iter=2000)),
])

param_grid = {
    'tfidf__max_features': [5000, 20000],
    'tfidf__ngram_range':  [(1,1), (1,2)],
    'tfidf__sublinear_tf': [True, False],
    'svc__C':              [0.1, 1.0, 10.0],
}

gs = GridSearchCV(pipe, param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=0)
gs.fit(data.data, data.target)

print(f"Best accuracy: {gs.best_score_:.4f}")
print("Best params:")
for k, v in gs.best_params_.items():
    print(f"  {k}: {v}")""",
    rw_scenario="Spam Filtering: An email system trains a TF-IDF + Logistic Regression classifier on 10K labeled emails. It uses feature inspection to identify top spam keywords and achieves >99% accuracy on a held-out test set.",
    rw_code=
"""from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

np.random.seed(42)

spam_keywords    = ['buy now', 'click here', 'free offer', 'earn money fast',
                    'limited time', 'act now', 'winner', 'prize', 'congratulations',
                    'no cost', 'guaranteed', 'risk free', 'million dollars']
ham_phrases      = ['meeting tomorrow', 'project update', 'please review',
                    'attached report', 'schedule call', 'thanks for your time',
                    'budget review', 'team standup', 'quarterly results']

def gen_email(is_spam, n):
    emails = []
    for _ in range(n):
        if is_spam:
            base = np.random.choice(spam_keywords, np.random.randint(3,7), replace=True)
            filler = ['you', 'the', 'for', 'is', 'a', 'to', 'in']
            text = ' '.join(list(base) + list(np.random.choice(filler, 10)))
        else:
            base = np.random.choice(ham_phrases, np.random.randint(2,5), replace=True)
            text = ' '.join(base)
        emails.append(text)
    return emails

spam = gen_email(True, 500)
ham  = gen_email(False, 1000)
texts  = spam + ham
labels = [1]*len(spam) + [0]*len(ham)

X_tr, X_te, y_tr, y_te = train_test_split(texts, labels, test_size=0.2,
                                            stratify=labels, random_state=42)
pipe = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2), sublinear_tf=True,
                               max_features=10000, min_df=1)),
    ('clf',   LogisticRegression(C=5.0, max_iter=1000, class_weight='balanced')),
])
pipe.fit(X_tr, y_tr)
y_pred = pipe.predict(X_te)
print(classification_report(y_te, y_pred, target_names=['Ham','Spam']))
print("Confusion matrix:")
print(confusion_matrix(y_te, y_pred))""",
    pt="Multi-Class News Classifier",
    pd_text="Use fetch_20newsgroups with 5 categories of your choice. Build a Pipeline: TfidfVectorizer (max_features=15000, ngram_range=(1,2), sublinear_tf=True) + LinearSVC(C=1.0). Evaluate with cross_val_score (5-fold, accuracy). Print the top-5 most informative words per class using the SVC coef_ attribute.",
    ps=
"""from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import numpy as np

categories = ['sci.space', 'rec.sport.hockey', 'comp.graphics',
              'talk.politics.guns', 'sci.med']
data = fetch_20newsgroups(subset='all', categories=categories,
                          remove=('headers','footers','quotes'), random_state=42)

pipe = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=15000, ngram_range=(1,2),
                               sublinear_tf=True, stop_words='english')),
    ('svc',   LinearSVC(C=1.0, max_iter=2000)),
])

# TODO: cross_val_score with 5-fold accuracy
# TODO: fit on all data
# TODO: for each class, find top-5 words (largest coef_ values)
""")

# ── Section 23: Anomaly Detection ────────────────────────────────────────────
s23 = make_section(23, "Anomaly Detection",
    "Anomaly detection finds outliers without labeled examples. IsolationForest uses random splits; LocalOutlierFactor compares density to neighbors; OneClassSVM learns a boundary around normal data.",
    c1t="IsolationForest for fraud detection",
    c1=
"""from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
# Simulate normal transactions
n_normal = 1000
n_fraud  = 30

normal = np.random.multivariate_normal(
    mean=[100, 50, 10],
    cov=[[400, 50, 5], [50, 100, 2], [5, 2, 4]],
    size=n_normal
)
fraud = np.random.multivariate_normal(
    mean=[500, 200, 100],
    cov=[[10000, 0, 0], [0, 5000, 0], [0, 0, 1000]],
    size=n_fraud
)

X = np.vstack([normal, fraud])
true_labels = np.array([1]*n_normal + [-1]*n_fraud)  # 1=normal, -1=anomaly

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

iso = IsolationForest(n_estimators=200, contamination=n_fraud/(n_normal+n_fraud),
                      random_state=42)
preds = iso.fit_predict(X_scaled)   # 1=normal, -1=anomaly
scores = iso.score_samples(X_scaled)

# Evaluate
tp = ((preds == -1) & (true_labels == -1)).sum()
fp = ((preds == -1) & (true_labels ==  1)).sum()
fn = ((preds ==  1) & (true_labels == -1)).sum()
precision = tp / (tp + fp) if (tp+fp) > 0 else 0
recall    = tp / (tp + fn) if (tp+fn) > 0 else 0
print(f"IsolationForest: TP={tp}, FP={fp}, FN={fn}")
print(f"Precision={precision:.3f}  Recall={recall:.3f}")
print(f"Anomaly score range: [{scores.min():.3f}, {scores.max():.3f}]")""",
    c2t="LocalOutlierFactor and OneClassSVM comparison",
    c2=
"""from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(0)
# 2D dataset for intuition
n_normal, n_anom = 300, 20
X_normal = np.random.randn(n_normal, 2)
X_anom   = np.random.uniform(low=-5, high=5, size=(n_anom, 2))
X        = np.vstack([X_normal, X_anom])
y_true   = np.array([1]*n_normal + [-1]*n_anom)

scaler = StandardScaler()
X_s    = scaler.fit_transform(X)

contamination = n_anom / len(X)

detectors = {
    'IsolationForest': IsolationForest(contamination=contamination, random_state=0),
    'LocalOutlierFactor': LocalOutlierFactor(contamination=contamination, n_neighbors=20),
    'OneClassSVM':     OneClassSVM(nu=contamination, kernel='rbf', gamma='scale'),
}

print(f"{'Detector':22s}  {'TP':>4s}  {'FP':>4s}  {'FN':>4s}  {'Precision':>10s}  {'Recall':>7s}")
for name, det in detectors.items():
    if name == 'LocalOutlierFactor':
        preds = det.fit_predict(X_s)
    else:
        det.fit(X_s[y_true == 1])  # train on normal only for OC-SVM/IF
        preds = det.predict(X_s)
    tp = ((preds==-1)&(y_true==-1)).sum()
    fp = ((preds==-1)&(y_true== 1)).sum()
    fn = ((preds== 1)&(y_true==-1)).sum()
    prec = tp/(tp+fp) if (tp+fp) else 0
    rec  = tp/(tp+fn) if (tp+fn) else 0
    print(f"{name:22s}  {tp:4d}  {fp:4d}  {fn:4d}  {prec:10.3f}  {rec:7.3f}")""",
    c3t="Anomaly scores and threshold tuning",
    c3=
"""from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_curve, roc_auc_score
import numpy as np

np.random.seed(42)
# Multi-modal normal distribution + sparse anomalies
n_normal = 2000
n_anom   = 50

X_normal = np.vstack([
    np.random.multivariate_normal([0, 0], [[1,0.5],[0.5,1]], n_normal//2),
    np.random.multivariate_normal([5, 5], [[1,-0.3],[-0.3,1]], n_normal//2),
])
X_anom = np.random.uniform(-8, 12, (n_anom, 2))
X = np.vstack([X_normal, X_anom])
y_true = np.array([0]*n_normal + [1]*n_anom)  # 1 = anomaly

iso = IsolationForest(n_estimators=300, contamination='auto', random_state=42)
iso.fit(X_normal)  # fit on normal data only
scores = -iso.score_samples(X)  # negate: higher = more anomalous

auc = roc_auc_score(y_true, scores)
print(f"ROC-AUC: {auc:.4f}")

# Find threshold at precision >= 0.8
precision, recall, thresholds = precision_recall_curve(y_true, scores)
high_prec = precision[:-1] >= 0.80
if high_prec.any():
    best_recall = recall[:-1][high_prec].max()
    best_thr    = thresholds[high_prec][recall[:-1][high_prec].argmax()]
    print(f"At precision>=80%: threshold={best_thr:.4f}, recall={best_recall:.3f}")
    flagged = (scores >= best_thr).sum()
    print(f"Flagged {flagged} anomalies ({flagged/len(X):.1%} of data)")""",
    rw_scenario="Manufacturing QC: A sensor monitoring system uses IsolationForest trained on normal operating conditions. Any reading with anomaly score above a threshold triggers an alert — reducing false positives by 60% vs. threshold-based rules.",
    rw_code=
"""from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np, pandas as pd

np.random.seed(42)
n = 5000

# Simulate sensor readings (temperature, pressure, vibration)
normal = pd.DataFrame({
    'temperature': np.random.normal(70, 5, n),
    'pressure':    np.random.normal(100, 3, n),
    'vibration':   np.random.normal(0.5, 0.1, n),
    'flow_rate':   np.random.normal(50, 4, n),
})

# Inject anomalies: sudden spikes
n_anom = 50
anom_idx = np.random.choice(n, n_anom, replace=False)
anomalies = normal.copy()
anomalies.loc[anom_idx, 'temperature'] += np.random.uniform(30, 60, n_anom)
anomalies.loc[anom_idx, 'vibration']   += np.random.uniform(1, 3, n_anom)

scaler = StandardScaler()
X_normal   = scaler.fit_transform(normal.values)
X_all      = scaler.transform(anomalies.values)

# Train only on normal data
iso = IsolationForest(n_estimators=300, contamination=n_anom/n, random_state=42)
iso.fit(X_normal)
scores = -iso.score_samples(X_all)

# Dynamic threshold: mean + 3*std of normal scores
normal_scores = -iso.score_samples(X_normal)
threshold = normal_scores.mean() + 3 * normal_scores.std()

alerts = np.where(scores > threshold)[0]
true_pos = len(set(alerts) & set(anom_idx))
print(f"Threshold: {threshold:.4f}")
print(f"Alerts: {len(alerts)} | True anomalies: {n_anom}")
print(f"True Positives: {true_pos} | Recall: {true_pos/n_anom:.2%}")""",
    pt="Network Intrusion Detection",
    pd_text="Generate a dataset with 800 normal network connections (3 features: packet_size normal(512,100), duration normal(0.5,0.2), port uniform(0,1024)) and 20 intrusion attempts (packet_size~5000, duration~0.01, port~random). Train IsolationForest, LocalOutlierFactor, and OneClassSVM. Compare precision and recall. Which performs best?",
    ps=
"""from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
n_normal, n_intrusion = 800, 20

# TODO: generate normal connections (packet_size, duration, port)
# TODO: generate intrusion attempts
# TODO: stack into X, create y_true labels

# TODO: for each detector, compute TP, FP, FN, precision, recall
# (fit on normal-only data for IsolationForest and OneClassSVM)
# LocalOutlierFactor.fit_predict on full X
""")

# ── Section 24: Advanced Clustering ──────────────────────────────────────────
s24 = make_section(24, "Advanced Clustering",
    "Beyond KMeans: AgglomerativeClustering builds hierarchies (no k needed upfront); GaussianMixture models soft assignments with probabilistic clusters; silhouette and Calinski-Harabasz scores evaluate cluster quality.",
    c1t="AgglomerativeClustering with linkage strategies",
    c1=
"""from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score, silhouette_score
import numpy as np

np.random.seed(42)
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=42)
X = StandardScaler().fit_transform(X)

linkages = ['ward', 'complete', 'average', 'single']

print(f"{'Linkage':10s}  {'ARI':>6s}  {'Silhouette':>10s}")
print('-' * 32)
for link in linkages:
    agg = AgglomerativeClustering(n_clusters=4, linkage=link)
    labels = agg.fit_predict(X)
    ari = adjusted_rand_score(y_true, labels)
    sil = silhouette_score(X, labels)
    print(f"{link:10s}  {ari:6.4f}  {sil:10.4f}")

# Connectivity constraints (useful for spatial data)
from sklearn.neighbors import kneighbors_graph
connectivity = kneighbors_graph(X, n_neighbors=10, include_self=False)
agg_conn = AgglomerativeClustering(n_clusters=4, linkage='ward',
                                    connectivity=connectivity)
labels_conn = agg_conn.fit_predict(X)
print(f"\nWith connectivity: ARI={adjusted_rand_score(y_true, labels_conn):.4f}")""",
    c2t="Gaussian Mixture Models — soft assignments",
    c2=
"""from sklearn.mixture import GaussianMixture
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score
import numpy as np

np.random.seed(42)
X, y_true = make_blobs(n_samples=400, centers=3, cluster_std=[1.0, 0.5, 1.5],
                        random_state=42)
X = StandardScaler().fit_transform(X)

# Compare covariance types
for cov_type in ['full', 'tied', 'diag', 'spherical']:
    gm = GaussianMixture(n_components=3, covariance_type=cov_type,
                          random_state=42, n_init=5)
    gm.fit(X)
    labels = gm.predict(X)
    ari  = adjusted_rand_score(y_true, labels)
    bic  = gm.bic(X)
    aic  = gm.aic(X)
    print(f"{cov_type:12s}  ARI={ari:.4f}  BIC={bic:.1f}  AIC={aic:.1f}")

# Soft assignments (probabilities)
gm_best = GaussianMixture(n_components=3, covariance_type='full',
                            random_state=42, n_init=5)
gm_best.fit(X)
proba = gm_best.predict_proba(X)
print(f"\nSample soft assignments (first 5):")
for row in proba[:5]:
    print(f"  {row.round(3)}")  # probability of each cluster""",
    c3t="BIC/AIC model selection and silhouette analysis",
    c3=
"""from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.9, random_state=42)
X = StandardScaler().fit_transform(X)

# Select k via BIC (GaussianMixture) and silhouette (KMeans)
print("=== GaussianMixture BIC/AIC ===")
print(f"{'k':>3s}  {'BIC':>10s}  {'AIC':>10s}")
for k in range(2, 8):
    gm = GaussianMixture(n_components=k, n_init=5, random_state=42)
    gm.fit(X)
    print(f"{k:3d}  {gm.bic(X):10.1f}  {gm.aic(X):10.1f}")

print("\n=== KMeans Cluster Quality ===")
print(f"{'k':>3s}  {'Silhouette':>11s}  {'Calinski-H':>12s}  {'Davies-B':>10s}")
for k in range(2, 8):
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(X)
    sil = silhouette_score(X, labels)
    ch  = calinski_harabasz_score(X, labels)
    db  = davies_bouldin_score(X, labels)
    print(f"{k:3d}  {sil:11.4f}  {ch:12.1f}  {db:10.4f}")""",
    c4t="HDBSCAN-style with DBSCAN density-based clustering",
    c4=
"""from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_blobs
from sklearn.metrics import adjusted_rand_score
import numpy as np

np.random.seed(42)

# Non-convex clusters (DBSCAN handles; KMeans fails)
X_moons, y_moons = make_moons(n_samples=300, noise=0.08, random_state=42)
X_moons = StandardScaler().fit_transform(X_moons)

# Tune eps
print("=== DBSCAN on Moons (non-convex) ===")
for eps in [0.1, 0.2, 0.3, 0.5]:
    db = DBSCAN(eps=eps, min_samples=5)
    labels = db.fit_predict(X_moons)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise    = (labels == -1).sum()
    if n_clusters > 0:
        try:
            ari = adjusted_rand_score(y_moons, labels)
        except Exception:
            ari = 0
        print(f"  eps={eps:.1f}  clusters={n_clusters}  noise={n_noise}  ARI={ari:.4f}")

# DBSCAN is also good for identifying outliers
X_blobs, y_blobs = make_blobs(n_samples=200, centers=3, random_state=42)
X_blobs = StandardScaler().fit_transform(X_blobs)
db_best = DBSCAN(eps=0.5, min_samples=8)
labels = db_best.fit_predict(X_blobs)
print(f"\nBlobs: {(labels==-1).sum()} noise points identified as outliers")""",
    rw_scenario="Customer Segmentation: A retail analytics team uses GaussianMixture to segment customers into soft groups — allowing borderline customers to have membership probabilities across multiple segments for targeted marketing.",
    rw_code=
"""from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import numpy as np, pandas as pd

np.random.seed(42)
n = 800
df = pd.DataFrame({
    'recency':    np.random.exponential(30, n),    # days since last purchase
    'frequency':  np.random.poisson(5, n) + 1,     # orders per year
    'monetary':   np.random.exponential(150, n),   # avg order value $
    'tenure':     np.random.randint(1, 60, n),     # months as customer
})

X = StandardScaler().fit_transform(df.values)

# Select k via BIC
bic_scores = []
for k in range(2, 8):
    gm = GaussianMixture(n_components=k, n_init=5, random_state=42)
    gm.fit(X)
    bic_scores.append((k, gm.bic(X)))

best_k = min(bic_scores, key=lambda t: t[1])[0]
print(f"Best k by BIC: {best_k}")

gm = GaussianMixture(n_components=best_k, covariance_type='full',
                      n_init=10, random_state=42)
gm.fit(X)
df['segment']    = gm.predict(X)
df['confidence'] = gm.predict_proba(X).max(axis=1)

print("\nSegment profiles:")
print(df.groupby('segment')[['recency','frequency','monetary','tenure']].mean().round(1))
print(f"\nAvg confidence: {df.confidence.mean():.3f}")
low_conf = (df.confidence < 0.6).sum()
print(f"Low-confidence assignments (<60%): {low_conf} ({low_conf/len(df):.1%})")""",
    pt="Hierarchical vs GMM Comparison",
    pd_text="Generate 3 clusters with varying density (n=100 each): dense circle at origin std=0.3, spread at (5,5) std=1.5, elongated at (2,-3) with cov [[4,2],[2,1]]). Compare: AgglomerativeClustering(ward, k=3), GaussianMixture(full, k=3), KMeans(k=3). Print ARI and silhouette for each. Which handles the elongated cluster best?",
    ps=
"""from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score, silhouette_score
import numpy as np

np.random.seed(42)
c1 = np.random.multivariate_normal([0, 0], [[0.09,0],[0,0.09]], 100)
c2 = np.random.multivariate_normal([5, 5], [[2.25,0],[0,2.25]], 100)
c3 = np.random.multivariate_normal([2,-3], [[4,2],[2,1]],        100)
X = np.vstack([c1, c2, c3])
y_true = np.array([0]*100 + [1]*100 + [2]*100)

X_s = StandardScaler().fit_transform(X)

models = {
    'AgglomerativeClustering': AgglomerativeClustering(n_clusters=3, linkage='ward'),
    'GaussianMixture':         GaussianMixture(n_components=3, covariance_type='full',
                                               n_init=5, random_state=42),
    'KMeans':                  KMeans(n_clusters=3, n_init=10, random_state=42),
}

# TODO: for each model, fit, predict, print ARI and silhouette
""")

# ── Assemble and insert ───────────────────────────────────────────────────────
all_sections = s17 + s18 + s19 + s20 + s21 + s22 + s23 + s24

result = insert_before_make_html(FILE, all_sections)
if result:
    print("SUCCESS: sections 17-24 added to gen_sklearn.py")
else:
    print("FAILED: check marker and file")
