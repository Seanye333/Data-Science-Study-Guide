#!/usr/bin/env python3
"""Generate Data Cleaning & Feature Engineering study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\16_feature_engineering")
BASE.mkdir(parents=True, exist_ok=True)

# ─── HTML builder ─────────────────────────────────────────────────────────────
def make_html(sections):
    nav = "\n    ".join(
        f'<li><a href="#s{i}" onclick="act(this,event)">{esc(s["title"])}</a></li>'
        for i, s in enumerate(sections)
    )
    cards = ""
    for i, s in enumerate(sections):
        blks = ""
        for j, ex in enumerate(s.get("examples", [])):
            cid = f"c{i}_{j}"
            blks += (
                f'<div class="code-block">'
                f'<div class="ch"><span>{esc(ex.get("label","Example"))}</span>'
                f'<button onclick="cp(\'{cid}\')">Copy</button></div>'
                f'<pre><code id="{cid}" class="language-python">{esc(ex["code"])}</code></pre>'
                f'</div>'
            )
        rw = s.get("rw", {})
        rw_html = ""
        if rw:
            rw_html = (
                f'<div class="rw">'
                f'<div class="rh">&#x1F4BC; Real-World: {esc(rw["title"])}</div>'
                f'<div class="rd">{esc(rw["scenario"])}</div>'
                f'<pre><code class="language-python">{esc(rw["code"])}</code></pre>'
                f'</div>'
            )
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
        todos = s.get("todos", [])
        todos_html = ""
        if todos:
            items = "\n".join(
                f'<li><label><input type="checkbox"> {esc(t)}</label></li>'
                for t in todos
            )
            todos_html = (
                f'<div class="todo-list">'
                f'<div class="todo-head">&#x2705; Practice Checklist</div>'
                f'<ul>{items}</ul>'
                f'</div>'
            )
        cards += (
            f'<div class="topic" id="s{i}">'
            f'<div class="th" onclick="tog(this)"><span>{esc(s["title"])}</span>'
            f'<span class="arr">&#9660;</span></div>'
            f'<div class="tb"><p class="desc">{esc(s.get("desc",""))}</p>'
            f'{blks}{rw_html}{practice_html}{todos_html}</div></div>'
        )
    n = len(sections)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Data Cleaning &amp; Feature Engineering Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<link rel="stylesheet" href="../styles/glass.css">
<style>:root{{--acc:#f472b6}}</style>
</head><body class="page-module">
<aside class="sidebar">
  <div class="sbh"><h2>🧹 Cleaning &amp; Feature Engineering</h2><p>Study Guide &bull; {n} topics</p>
    <input id="q" placeholder="Search..." oninput="filt(this.value)">
  </div>
  <ul class="nav-list" id="nl">{nav}</ul>
</aside>
<main class="main">
  <h1 class="pt">🧹 Data Cleaning &amp; Feature Engineering</h1>
  <p class="ps">{n} topics &bull; Click any card to expand</p>
  {cards}
</main>
<script>
hljs.highlightAll();
function tog(h){{var b=h.nextElementSibling,a=h.querySelector('.arr');b.classList.toggle('open');a.classList.toggle('open');}}
function act(el,e){{if(e)e.preventDefault();document.querySelectorAll('.nav-list a').forEach(a=>a.classList.remove('active'));el.classList.add('active');document.querySelector(el.getAttribute('href')).scrollIntoView({{behavior:'smooth'}});}}
function filt(q){{document.querySelectorAll('#nl li').forEach(li=>{{li.style.display=li.textContent.toLowerCase().includes(q.toLowerCase())?'':'none';}});}}
function cp(id){{navigator.clipboard.writeText(document.getElementById(id).innerText).catch(()=>{{}});}}
document.addEventListener('DOMContentLoaded',()=>{{var fh=document.querySelector('.th');if(fh)fh.click();var fa=document.querySelector('.nav-list a');if(fa)fa.classList.add('active');}});
</script></body></html>"""


# ─── Notebook builder ─────────────────────────────────────────────────────────
def make_nb(sections):
    cells = []
    n = [0]
    def nid(): n[0]+=1; return f"{n[0]:04d}"
    def md(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"markdown","id":nid(),"metadata":{},"source":s}
    def code(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"code","execution_count":None,"id":nid(),"metadata":{},"outputs":[],"source":s}

    cells.append(md("# Data Cleaning & Feature Engineering Study Guide\n\nMaster the art of preparing data for ML — from handling messy real-world data to crafting features that boost model performance."))
    for i, s in enumerate(sections, 1):
        cells.append(md(f"## {i}. {s['title']}\n\n{s.get('desc','')}"))
        for ex in s.get("examples", []):
            if ex.get("label"): cells.append(md(f"**{ex['label']}**"))
            cells.append(code(ex["code"]))
        rw = s.get("rw")
        if rw:
            cells.append(md(f"### Real-World: {rw['title']}\n\n> {rw['scenario']}"))
            cells.append(code(rw["code"]))
        practice = s.get("practice")
        if practice:
            cells.append(md(f"### Practice: {practice['title']}\n\n{practice['desc']}"))
            cells.append(code(practice["starter"]))
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name":"Python 3","language":"python","name":"python3"},
            "language_info": {"name":"python","version":"3.11.0"}
        },
        "nbformat": 4, "nbformat_minor": 5
    }


# ─── Content ──────────────────────────────────────────────────────────────────
SECTIONS = [

{
"title": "1. Exploratory Data Profiling",
"desc": "Before cleaning, you need to understand your data. Profiling reveals data types, missing values, distributions, and anomalies — the roadmap for your entire cleaning pipeline.",
"examples": [
{"label": "Quick dataset overview", "code":
"""import pandas as pd
import numpy as np

# Create a realistic messy dataset
np.random.seed(42)
n = 500
df = pd.DataFrame({
    "age": np.random.normal(35, 12, n).astype(int),
    "income": np.random.lognormal(10.5, 0.8, n),
    "education": np.random.choice(["High School", "Bachelor", "Master", "PhD", None], n, p=[0.3, 0.35, 0.2, 0.1, 0.05]),
    "city": np.random.choice(["NYC", "LA", "Chicago", "Houston", "  NYC ", "nyc"], n),
    "signup_date": pd.date_range("2020-01-01", periods=n, freq="D").astype(str),
    "purchase_amount": np.where(np.random.random(n) > 0.9, np.nan, np.random.exponential(50, n)),
    "is_active": np.random.choice([True, False, "yes", "no", 1, 0], n),
})
# Inject some bad data
df.loc[10, "age"] = -5
df.loc[20, "age"] = 150
df.loc[30, "income"] = -1000

print(df.shape)
print(df.dtypes)
print(df.head())"""},
{"label": "Missing value analysis", "code":
"""import pandas as pd
import numpy as np

# Comprehensive missing value report
def missing_report(df):
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    dtypes = df.dtypes
    report = pd.DataFrame({
        "missing": missing,
        "pct_missing": pct,
        "dtype": dtypes,
        "nunique": df.nunique(),
    })
    return report[report["missing"] > 0].sort_values("pct_missing", ascending=False)

# Create sample data
df = pd.DataFrame({
    "A": [1, 2, np.nan, 4, 5],
    "B": [np.nan, np.nan, 3, 4, 5],
    "C": ["x", None, "z", "x", None],
    "D": [1.0, 2.0, 3.0, 4.0, 5.0],
})

print(missing_report(df))

# Visualize missing patterns
print("\\nMissing pattern (True = missing):")
print(df.isnull().astype(int))"""},
{"label": "Distribution and outlier detection", "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "salary": np.concatenate([np.random.normal(60000, 15000, 95), [250000, 300000, -5000, 0, 500000]]),
    "age": np.concatenate([np.random.normal(35, 10, 97), [200, -3, 0]]),
})

# Basic statistics
print(df.describe().round(2))

# IQR method for outlier detection
def detect_outliers_iqr(series, factor=1.5):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - factor * IQR
    upper = Q3 + factor * IQR
    outliers = series[(series < lower) | (series > upper)]
    return outliers, lower, upper

for col in df.columns:
    outliers, lo, hi = detect_outliers_iqr(df[col])
    print(f"\\n{col}: {len(outliers)} outliers (range: {lo:.0f} to {hi:.0f})")
    if len(outliers) > 0:
        print(f"  Values: {outliers.values}")"""},
],
"rw": {
    "title": "Automated Data Quality Report",
    "scenario": "A data team receives weekly CSV dumps from a partner. They need an automated profiling script that flags data quality issues before the data enters their pipeline.",
    "code":
"""import pandas as pd
import numpy as np

def data_quality_report(df, name="dataset"):
    print(f"{'='*60}")
    print(f"DATA QUALITY REPORT: {name}")
    print(f"{'='*60}")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Memory: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")

    # Missing values
    missing = df.isnull().sum()
    if missing.any():
        print(f"\\nMissing Values:")
        for col in missing[missing > 0].index:
            pct = missing[col] / len(df) * 100
            print(f"  {col}: {missing[col]} ({pct:.1f}%)")

    # Duplicates
    dupes = df.duplicated().sum()
    print(f"\\nDuplicate rows: {dupes} ({dupes/len(df)*100:.1f}%)")

    # Numeric outliers (Z-score > 3)
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        print(f"\\nNumeric outliers (|z| > 3):")
        for col in numeric.columns:
            z = (numeric[col] - numeric[col].mean()) / numeric[col].std()
            n_outliers = (z.abs() > 3).sum()
            if n_outliers > 0:
                print(f"  {col}: {n_outliers} outliers")

    # Cardinality check
    print(f"\\nColumn cardinality:")
    for col in df.columns:
        nuniq = df[col].nunique()
        ratio = nuniq / len(df)
        flag = " ← potential ID" if ratio > 0.95 else " ← low cardinality" if nuniq < 5 else ""
        print(f"  {col}: {nuniq} unique ({ratio:.1%}){flag}")

# Test
np.random.seed(42)
df = pd.DataFrame({
    "user_id": range(100),
    "age": np.concatenate([np.random.normal(35, 10, 97), [200, -3, 0]]),
    "category": np.random.choice(["A", "B", "C"], 100),
    "value": np.where(np.random.random(100) > 0.85, np.nan, np.random.exponential(50, 100)),
})
data_quality_report(df, "sample_data")"""
},
"todos": [
    "Write a missing_report() function that shows count, percent, and dtype for every column with NaNs",
    "Load a real CSV and run df.describe() — identify at least 2 suspicious values from the output",
    "Check cardinality of every column — find any that look like IDs (nearly all unique values)",
    "Compute IQR bounds for a numeric column and print all rows that fall outside the range",
    "Use df.isnull().corr() to check if missingness in one column correlates with another",
],
},

{
"title": "2. Handling Missing Data",
"desc": "Missing data is the most common data quality issue. The right strategy depends on WHY data is missing (MCAR, MAR, MNAR) and how much is missing.",
"examples": [
{"label": "Detecting and understanding missingness", "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "age": [25, np.nan, 35, 40, np.nan, 55, 30, np.nan, 45, 50],
    "income": [50000, 60000, np.nan, 80000, 45000, np.nan, 55000, 70000, np.nan, 90000],
    "education": ["BS", "MS", "BS", None, "PhD", "BS", None, "MS", "BS", "PhD"],
    "purchased": [1, 0, 1, 1, 0, 1, 0, 1, np.nan, 1],
})

# Check missingness
print("Missing per column:")
print(df.isnull().sum())

print("\\nMissing percentage:")
print((df.isnull().mean() * 100).round(1))

# Check if missingness is correlated
print("\\nMissing correlation matrix:")
print(df.isnull().corr().round(2))

# Types of missingness:
# MCAR: Missing Completely At Random (safe to drop or impute)
# MAR: Missing At Random (conditional on observed data)
# MNAR: Missing Not At Random (the value itself determines missingness)"""},
{"label": "Imputation strategies", "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "age": [25, np.nan, 35, 40, np.nan, 55, 30, np.nan, 45, 50],
    "salary": [50000, 60000, np.nan, 80000, np.nan, 120000, 55000, 70000, np.nan, 90000],
    "dept": ["Sales", "Eng", "Sales", None, "Eng", "Eng", None, "Sales", "Eng", "Sales"],
})

# Strategy 1: Drop rows with any missing values
df_dropped = df.dropna()
print(f"After dropna: {len(df_dropped)} rows (lost {len(df) - len(df_dropped)})")

# Strategy 2: Fill with constants
df["dept_filled"] = df["dept"].fillna("Unknown")

# Strategy 3: Mean/median/mode imputation
df["age_mean"] = df["age"].fillna(df["age"].mean())
df["age_median"] = df["age"].fillna(df["age"].median())
df["salary_median"] = df["salary"].fillna(df["salary"].median())

# Strategy 4: Group-based imputation (smarter!)
df["salary_by_dept"] = df.groupby("dept")["salary"].transform(
    lambda x: x.fillna(x.median())
)

# Strategy 5: Forward/backward fill (for time series)
df["age_ffill"] = df["age"].ffill()
df["age_bfill"] = df["age"].bfill()

print(df[["age", "age_mean", "age_median", "age_ffill"]].to_string())"""},
{"label": "Advanced imputation with sklearn", "code":
"""import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

np.random.seed(42)
X = np.array([
    [25, 50000], [30, 60000], [35, np.nan], [40, 80000],
    [np.nan, 45000], [55, 120000], [30, 55000], [np.nan, 70000],
])

# KNN Imputer — uses similar rows to estimate missing values
knn_imp = KNNImputer(n_neighbors=3)
X_knn = knn_imp.fit_transform(X)
print("KNN Imputed:")
print(X_knn.round(0))

# Iterative Imputer (MICE) — models each feature as a function of others
iter_imp = IterativeImputer(max_iter=10, random_state=42)
X_iter = iter_imp.fit_transform(X)
print("\\nIterative (MICE) Imputed:")
print(X_iter.round(0))

# Adding a missing indicator feature (useful for models!)
from sklearn.impute import MissingIndicator
indicator = MissingIndicator()
missing_flags = indicator.fit_transform(X)
print(f"\\nMissing indicator columns: {indicator.features_}")
print(missing_flags.astype(int))"""},
],
"rw": {
    "title": "Smart Imputation Pipeline",
    "scenario": "A health dataset has mixed missing patterns — age is MCAR, income is MAR (depends on employment), and diagnosis is MNAR. Each needs a different strategy.",
    "code":
"""import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

np.random.seed(42)
n = 200
df = pd.DataFrame({
    "age": np.where(np.random.random(n) > 0.9, np.nan, np.random.normal(45, 15, n)),
    "income": np.where(np.random.random(n) > 0.8, np.nan, np.random.lognormal(10.5, 0.7, n)),
    "employed": np.random.choice([1, 0], n, p=[0.7, 0.3]),
    "bmi": np.where(np.random.random(n) > 0.85, np.nan, np.random.normal(26, 5, n)),
})

print(f"Before: {df.isnull().sum().to_dict()}")

# 1. Age (MCAR) — median imputation is fine
df["age"] = df["age"].fillna(df["age"].median())

# 2. Income (MAR — depends on employment) — group-based
df["income"] = df.groupby("employed")["income"].transform(
    lambda x: x.fillna(x.median())
)
# Fill any remaining NaN (if a group was all NaN)
df["income"] = df["income"].fillna(df["income"].median())

# 3. BMI — KNN imputation (use correlated features)
knn = KNNImputer(n_neighbors=5)
df[["age", "income", "bmi"]] = knn.fit_transform(df[["age", "income", "bmi"]])

# 4. Add missing indicators for model features
df["income_was_missing"] = df["income"].isnull().astype(int)
df["bmi_was_missing"] = df["bmi"].isnull().astype(int)

print(f"After:  {df.isnull().sum().to_dict()}")
print(df.describe().round(1))"""
},
"practice": {
    "title": "Build a Missing Data Handler",
    "desc": "Create a class that analyzes missingness patterns and automatically selects the right imputation strategy based on the percentage missing and data type.",
    "starter":
"""import pandas as pd
import numpy as np

class SmartImputer:
    def __init__(self, numeric_strategy="median", categorical_strategy="mode",
                 high_missing_threshold=0.5):
        self.numeric_strategy = numeric_strategy
        self.categorical_strategy = categorical_strategy
        self.threshold = high_missing_threshold
        self.fill_values = {}

    def fit(self, df):
        for col in df.columns:
            pct_missing = df[col].isnull().mean()
            if pct_missing > self.threshold:
                self.fill_values[col] = "DROP"
            elif df[col].dtype in ["float64", "int64"]:
                # TODO: compute fill value based on numeric_strategy
                pass
            else:
                # TODO: compute fill value based on categorical_strategy
                pass
        return self

    def transform(self, df):
        df = df.copy()
        # TODO: apply fill_values, drop columns marked "DROP"
        return df

# Test
np.random.seed(42)
df = pd.DataFrame({
    "A": [1, np.nan, 3, 4, np.nan],
    "B": [np.nan, np.nan, np.nan, np.nan, 5],  # 80% missing → should drop
    "C": ["x", None, "y", "x", "y"],
})

imputer = SmartImputer()
imputer.fit(df)
result = imputer.transform(df)
print(result)"""
},
"todos": [
    "Create a DataFrame with 20% missing values and plot the missingness pattern",
    "Compare mean vs median imputation on a skewed column — which is better?",
    "Use KNNImputer with k=3 and k=10 — check if the imputed values differ",
    "Add a binary 'was_missing' indicator column alongside imputed values",
    "Drop rows where more than 50% of columns are missing",
],
},

{
"title": "3. Handling Duplicates & Inconsistencies",
"desc": "Duplicate records and inconsistent formatting are silent data quality killers. A single city spelled three different ways will break your groupby analysis.",
"examples": [
{"label": "Finding and removing duplicates", "code":
"""import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Alice", "Carol", "Bob", "Alice"],
    "email": ["alice@co.com", "bob@co.com", "alice@co.com", "carol@co.com", "bob@co.com", "alice2@co.com"],
    "purchase": [100, 200, 100, 150, 250, 300],
})

# Find exact duplicates
print(f"Duplicate rows: {df.duplicated().sum()}")
print(df[df.duplicated(keep=False)])  # show ALL duplicates

# Duplicates based on subset of columns
print(f"\\nDuplicate names: {df.duplicated(subset=['name']).sum()}")
print(f"Duplicate name+email: {df.duplicated(subset=['name', 'email']).sum()}")

# Remove duplicates
df_clean = df.drop_duplicates()
print(f"\\nAfter dedup (exact): {len(df_clean)} rows")

# Keep last occurrence
df_clean = df.drop_duplicates(subset=["name", "email"], keep="last")
print(f"After dedup (name+email, keep last): {len(df_clean)} rows")"""},
{"label": "String cleaning and standardization", "code":
"""import pandas as pd

df = pd.DataFrame({
    "city": ["New York", "  new york  ", "NEW YORK", "nyc", "N.Y.C.", "Los Angeles", "LA", "los angeles"],
    "state": ["NY", "ny", " NY ", "NY", "NY", "CA", "ca", "CA"],
    "phone": ["555-1234", "(555) 123-4567", "5551234", "+1-555-123-4567", "555.123.4567", "N/A", "", None],
})

# Step 1: Strip whitespace and standardize case
df["city_clean"] = df["city"].str.strip().str.title()
df["state_clean"] = df["state"].str.strip().str.upper()

# Step 2: Map common variations
city_mapping = {
    "Nyc": "New York",
    "N.Y.C.": "New York",
    "La": "Los Angeles",
}
df["city_clean"] = df["city_clean"].replace(city_mapping)

# Step 3: Clean phone numbers (keep only digits)
df["phone_clean"] = df["phone"].fillna("").str.replace(r"[^\\d]", "", regex=True)
df["phone_clean"] = df["phone_clean"].replace("", None)

print(df[["city", "city_clean", "state", "state_clean"]].to_string())
print()
print(df[["phone", "phone_clean"]].to_string())"""},
{"label": "Data type fixes", "code":
"""import pandas as pd
import numpy as np

# Common type issues in real data
df = pd.DataFrame({
    "price": ["$10.99", "$24.50", "15.00", "$8.99", "N/A"],
    "date": ["2024-01-15", "01/16/2024", "Jan 17, 2024", "2024-01-18", "invalid"],
    "is_active": ["yes", "no", "True", "1", "false"],
    "rating": ["4.5", "3.8", "five", "4.2", "4.9"],
    "quantity": ["10", "20", "30.0", "forty", "50"],
})

# Fix prices: remove $ and convert
df["price_clean"] = df["price"].str.replace("$", "", regex=False)
df["price_clean"] = pd.to_numeric(df["price_clean"], errors="coerce")

# Fix dates: parse with mixed formats
df["date_clean"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")

# Fix booleans
bool_map = {"yes": True, "no": False, "true": True, "false": False, "1": True, "0": False}
df["active_clean"] = df["is_active"].str.lower().map(bool_map)

# Fix numerics with error coercion
df["rating_clean"] = pd.to_numeric(df["rating"], errors="coerce")
df["qty_clean"] = pd.to_numeric(df["quantity"], errors="coerce").astype("Int64")

print(df[["price", "price_clean", "date", "date_clean"]].to_string())
print()
print(df[["is_active", "active_clean", "rating", "rating_clean"]].to_string())"""},
],
"rw": {
    "title": "Cleaning a Messy Customer Database",
    "scenario": "A company merged data from 3 CRM systems. Names are inconsistent, emails duplicated, dates in different formats, and categorical fields use different codes.",
    "code":
"""import pandas as pd
import numpy as np

# Simulated messy merged data
df = pd.DataFrame({
    "name": ["John Smith", "john smith", "JOHN SMITH", "Jane Doe", "jane doe"],
    "email": ["john@co.com", "john@co.com", "john@co.com", "jane@co.com", "jane@co.com"],
    "signup": ["2023-01-15", "01/15/2023", "Jan 15, 2023", "2023-06-20", "06/20/2023"],
    "plan": ["premium", "PREMIUM", "Premium", "basic", "Basic"],
    "revenue": ["$1200", "1200.00", "$1,200.00", "$500", "500"],
})

def clean_customer_data(df):
    df = df.copy()

    # Standardize text fields
    df["name"] = df["name"].str.strip().str.title()
    df["email"] = df["email"].str.strip().str.lower()
    df["plan"] = df["plan"].str.strip().str.lower()

    # Parse dates
    df["signup"] = pd.to_datetime(df["signup"], format="mixed")

    # Clean revenue
    df["revenue"] = (df["revenue"].astype(str)
                     .str.replace("[$,]", "", regex=True))
    df["revenue"] = pd.to_numeric(df["revenue"])

    # Deduplicate (keep most recent)
    df = df.sort_values("signup").drop_duplicates(subset=["email"], keep="last")

    return df.reset_index(drop=True)

result = clean_customer_data(df)
print(result)
print(f"\\nReduced from {len(df)} to {len(result)} rows")"""
},
"todos": [
    "Create a DataFrame with city names spelled 4 different ways, then use .replace() to standardize them",
    "Find duplicate rows in a dataset using df.duplicated() and print only the rows that appear more than once",
    "Clean a 'price' column with '$' signs and commas using str.replace and pd.to_numeric(errors='coerce')",
    "Parse a column with 3 different date formats into a single datetime column using pd.to_datetime",
    "Use drop_duplicates(subset=['email'], keep='last') and verify only the most recent entry survives",
],
},

{
"title": "4. Outlier Detection & Treatment",
"desc": "Outliers can be legitimate extreme values or data errors. The right approach depends on context — sometimes you remove them, sometimes you keep them, sometimes you cap them.",
"examples": [
{"label": "Statistical outlier detection methods", "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
data = np.concatenate([np.random.normal(100, 15, 95), [200, 250, 10, 5, 300]])
df = pd.DataFrame({"value": data})

# Method 1: Z-score (assumes normal distribution)
df["z_score"] = (df["value"] - df["value"].mean()) / df["value"].std()
z_outliers = df[df["z_score"].abs() > 3]
print(f"Z-score outliers (|z| > 3): {len(z_outliers)}")

# Method 2: IQR (no distribution assumption)
Q1 = df["value"].quantile(0.25)
Q3 = df["value"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
iqr_outliers = df[(df["value"] < lower) | (df["value"] > upper)]
print(f"IQR outliers: {len(iqr_outliers)} (range: {lower:.1f} to {upper:.1f})")

# Method 3: Modified Z-score (uses median, more robust)
median = df["value"].median()
mad = (df["value"] - median).abs().median()
df["modified_z"] = 0.6745 * (df["value"] - median) / mad
mod_outliers = df[df["modified_z"].abs() > 3.5]
print(f"Modified Z-score outliers: {len(mod_outliers)}")"""},
{"label": "Outlier treatment strategies", "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "salary": np.concatenate([np.random.normal(60000, 15000, 95), [250000, 300000, -5000, 0, 500000]]),
})

# Strategy 1: Remove outliers
Q1 = df["salary"].quantile(0.25)
Q3 = df["salary"].quantile(0.75)
IQR = Q3 - Q1
mask = (df["salary"] >= Q1 - 1.5*IQR) & (df["salary"] <= Q3 + 1.5*IQR)
df_removed = df[mask]
print(f"Removed: {len(df)} → {len(df_removed)} rows")

# Strategy 2: Winsorize (cap at percentiles)
lower = df["salary"].quantile(0.01)
upper = df["salary"].quantile(0.99)
df["salary_capped"] = df["salary"].clip(lower, upper)
print(f"\\nCapped range: {lower:.0f} to {upper:.0f}")

# Strategy 3: Log transform (reduces skew)
df["salary_log"] = np.log1p(df["salary"].clip(lower=0))

# Strategy 4: Flag outliers (keep them, but add indicator)
df["is_outlier"] = (~mask).astype(int)

print(f"\\nOriginal stats: mean={df['salary'].mean():.0f}, std={df['salary'].std():.0f}")
print(f"Capped stats:   mean={df['salary_capped'].mean():.0f}, std={df['salary_capped'].std():.0f}")"""},
],
"rw": {
    "title": "Outlier-Robust Feature Pipeline",
    "scenario": "A fraud detection system needs to handle extreme transaction amounts. Legitimate high-value transactions exist alongside errors and fraud — you can't simply remove all outliers.",
    "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000
df = pd.DataFrame({
    "amount": np.concatenate([
        np.random.lognormal(3, 1, 900),      # normal transactions
        np.random.lognormal(6, 0.5, 80),      # high-value legitimate
        np.array([0.01, 0.001, -50, 999999] * 5),  # errors/fraud
    ]),
    "is_fraud": np.concatenate([
        np.zeros(900), np.zeros(80), np.ones(20)
    ]),
})

# Strategy: Don't remove — create features from outlier signals
df["log_amount"] = np.log1p(df["amount"].clip(lower=0))
df["amount_zscore"] = (df["amount"] - df["amount"].mean()) / df["amount"].std()
df["is_negative"] = (df["amount"] < 0).astype(int)
df["is_extreme"] = (df["amount_zscore"].abs() > 3).astype(int)

# Percentile rank (robust to outliers)
df["amount_pctile"] = df["amount"].rank(pct=True)

print("Feature correlations with fraud:")
for col in ["log_amount", "amount_zscore", "is_negative", "is_extreme", "amount_pctile"]:
    corr = df[col].corr(df["is_fraud"])
    print(f"  {col:20s}: {corr:.3f}")"""
},
"todos": [
    "Detect outliers using Z-score and IQR on the same column — compare which flags more values",
    "Apply winsorization (clip at 1st and 99th percentile) and compare mean/std before and after",
    "Apply a log1p transform to a skewed column and compare the histogram shape",
    "Create an 'is_outlier' binary flag column instead of removing outliers — train a model with it",
    "Use the modified Z-score method on a column with extreme values and compare it to IQR results",
],
},

{
"title": "5. Encoding Categorical Variables",
"desc": "ML models need numbers, not strings. Encoding transforms categorical data into numerical features. The right encoding depends on the variable type and the model you're using.",
"examples": [
{"label": "Label encoding and one-hot encoding", "code":
"""import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

df = pd.DataFrame({
    "color": ["red", "blue", "green", "red", "blue"],
    "size": ["S", "M", "L", "XL", "M"],
    "quality": ["low", "medium", "high", "medium", "high"],
})

# Label Encoding — maps categories to integers
# Good for: ordinal variables, tree-based models
le = LabelEncoder()
df["color_label"] = le.fit_transform(df["color"])
print("Label encoded:")
print(df[["color", "color_label"]])

# One-Hot Encoding — creates binary columns
# Good for: nominal variables, linear models, neural nets
df_onehot = pd.get_dummies(df[["color"]], prefix="color", drop_first=False)
print("\\nOne-hot encoded:")
print(df_onehot)

# drop_first=True to avoid multicollinearity (for linear models)
df_onehot_drop = pd.get_dummies(df[["color"]], prefix="color", drop_first=True)
print("\\nWith drop_first:")
print(df_onehot_drop)"""},
{"label": "Ordinal encoding (preserving order)", "code":
"""import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

df = pd.DataFrame({
    "education": ["High School", "Bachelor", "Master", "PhD", "Bachelor"],
    "satisfaction": ["low", "medium", "high", "very high", "medium"],
})

# Ordinal encoding with explicit order
edu_order = ["High School", "Bachelor", "Master", "PhD"]
sat_order = ["low", "medium", "high", "very high"]

oe = OrdinalEncoder(categories=[edu_order, sat_order])
df[["edu_encoded", "sat_encoded"]] = oe.fit_transform(df[["education", "satisfaction"]])

print(df)
# High School=0, Bachelor=1, Master=2, PhD=3
# low=0, medium=1, high=2, very high=3"""},
{"label": "Target encoding and frequency encoding", "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "city": np.random.choice(["NYC", "LA", "Chicago", "Houston", "Phoenix"], 100),
    "price": np.random.normal(50, 15, 100),
})

# Frequency encoding — replace with occurrence count
freq = df["city"].value_counts()
df["city_freq"] = df["city"].map(freq)

# Target encoding — replace with mean of target variable
# IMPORTANT: use only training data to compute means (avoid leakage!)
target_means = df.groupby("city")["price"].mean()
df["city_target"] = df["city"].map(target_means)

print("Encoding comparison:")
print(df.groupby("city").agg(
    count=("city_freq", "first"),
    target_mean=("city_target", "first"),
).round(2))

# For production: use sklearn's TargetEncoder (handles leakage)
from sklearn.preprocessing import TargetEncoder
te = TargetEncoder(smooth="auto")
df["city_target_sklearn"] = te.fit_transform(
    df[["city"]], df["price"]
)"""},
],
"rw": {
    "title": "Encoding Pipeline for Mixed Data",
    "scenario": "A dataset has nominal, ordinal, and high-cardinality categorical features. Each needs a different encoding strategy for an XGBoost model.",
    "code":
"""import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, TargetEncoder
from sklearn.compose import ColumnTransformer

np.random.seed(42)
n = 500
df = pd.DataFrame({
    "color": np.random.choice(["red", "blue", "green"], n),            # nominal, low cardinality
    "size": np.random.choice(["XS", "S", "M", "L", "XL"], n),         # ordinal
    "zip_code": np.random.choice([f"{z:05d}" for z in range(10000, 10200)], n),  # high cardinality
    "price": np.random.normal(100, 30, n),                              # target
})

# Strategy per column type:
# 1. Nominal + low cardinality → One-hot
# 2. Ordinal → Ordinal encoding
# 3. High cardinality → Target encoding

# One-hot for color
color_dummies = pd.get_dummies(df["color"], prefix="color", drop_first=True)

# Ordinal for size
size_order = [["XS", "S", "M", "L", "XL"]]
oe = OrdinalEncoder(categories=size_order)
df["size_ord"] = oe.fit_transform(df[["size"]])

# Target encoding for zip_code
te = TargetEncoder(smooth="auto")
df["zip_target"] = te.fit_transform(df[["zip_code"]], df["price"])

# Combine
result = pd.concat([color_dummies, df[["size_ord", "zip_target", "price"]]], axis=1)
print(result.head())
print(f"\\nFinal shape: {result.shape}")"""
},
"todos": [
    "Apply one-hot encoding to a nominal column and confirm the resulting column count",
    "Use OrdinalEncoder with an explicit category order and verify the numbers follow the ranking",
    "Apply frequency encoding to a high-cardinality column and inspect the distribution of encoded values",
    "Apply target encoding only on the training set and use transform on the test set to avoid leakage",
    "Compare label encoding vs one-hot encoding in a logistic regression — which gives better accuracy?",
],
},

{
"title": "6. Feature Scaling & Normalization",
"desc": "Many ML algorithms (linear regression, SVM, KNN, neural nets) are sensitive to feature scale. Scaling puts features on comparable ranges so no single feature dominates.",
"examples": [
{"label": "StandardScaler, MinMaxScaler, RobustScaler", "code":
"""import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

np.random.seed(42)
df = pd.DataFrame({
    "age": np.random.normal(35, 10, 100),
    "income": np.random.lognormal(10.5, 0.8, 100),       # skewed
    "score": np.concatenate([np.random.normal(50, 10, 95), [200, 250, 0, 5, 300]]),  # with outliers
})

# StandardScaler: mean=0, std=1 (assumes normal distribution)
scaler_std = StandardScaler()
df_std = pd.DataFrame(scaler_std.fit_transform(df), columns=df.columns)

# MinMaxScaler: scales to [0, 1] (sensitive to outliers)
scaler_mm = MinMaxScaler()
df_mm = pd.DataFrame(scaler_mm.fit_transform(df), columns=df.columns)

# RobustScaler: uses median and IQR (robust to outliers)
scaler_rob = RobustScaler()
df_rob = pd.DataFrame(scaler_rob.fit_transform(df), columns=df.columns)

print("Original stats:")
print(df.describe().round(1).loc[["mean", "std", "min", "max"]])
print("\\nStandardScaler:")
print(df_std.describe().round(2).loc[["mean", "std", "min", "max"]])
print("\\nMinMaxScaler:")
print(df_mm.describe().round(2).loc[["mean", "std"]])
print("\\nRobustScaler:")
print(df_rob.describe().round(2).loc[["mean", "std"]])"""},
{"label": "When to use which scaler", "code":
"""# Decision guide:
#
# StandardScaler (Z-score normalization)
#   Use when: data is roughly normal, no extreme outliers
#   Models: Linear/Logistic Regression, SVM, PCA, Neural Nets
#   Formula: (x - mean) / std
#
# MinMaxScaler
#   Use when: you need bounded [0,1] range, no extreme outliers
#   Models: Neural networks (especially with sigmoid), KNN
#   Formula: (x - min) / (max - min)
#
# RobustScaler
#   Use when: data has outliers
#   Models: Any model sensitive to scale
#   Formula: (x - median) / IQR
#
# No scaling needed:
#   Models: Tree-based (Random Forest, XGBoost, LightGBM)
#   These are scale-invariant — scaling won't help or hurt

import pandas as pd

guide = pd.DataFrame({
    "Scaler": ["StandardScaler", "MinMaxScaler", "RobustScaler", "None"],
    "Best For": ["Normal data", "Bounded range", "Data with outliers", "Tree models"],
    "Outlier Robust": ["No", "No", "Yes", "N/A"],
    "Range": ["~(-3, 3)", "[0, 1]", "Centered at 0", "Original"],
})
print(guide.to_string(index=False))"""},
{"label": "IMPORTANT: fit on train, transform both", "code":
"""import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

np.random.seed(42)
X = np.random.normal(50, 15, (200, 3))
y = np.random.choice([0, 1], 200)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# CORRECT: fit on train, transform both
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit + transform
X_test_scaled = scaler.transform(X_test)          # transform only!

print(f"Train mean: {X_train_scaled.mean(axis=0).round(6)}")  # ~0
print(f"Test mean:  {X_test_scaled.mean(axis=0).round(2)}")    # close to 0, not exact

# WRONG: fitting on test data (data leakage!)
# scaler.fit_transform(X_test)  # NEVER DO THIS!
# This leaks test set statistics into your model"""},
],
"rw": {
    "title": "Scaling Pipeline with Column Transformer",
    "scenario": "A dataset has numeric features needing different scalers and categorical features needing encoding. Build a single sklearn pipeline that handles everything.",
    "code":
"""import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

np.random.seed(42)
df = pd.DataFrame({
    "age": np.random.normal(35, 10, 100),
    "income": np.concatenate([np.random.lognormal(10.5, 0.8, 95), [1e7]*5]),  # outliers
    "score": np.random.normal(500, 100, 100),
    "education": np.random.choice(["HS", "BS", "MS", "PhD"], 100),
    "target": np.random.choice([0, 1], 100),
})

# Define column groups
normal_cols = ["age", "score"]     # roughly normal → StandardScaler
skewed_cols = ["income"]           # skewed + outliers → RobustScaler
cat_cols = ["education"]           # categorical → OneHotEncoder

preprocessor = ColumnTransformer([
    ("normal", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), normal_cols),
    ("skewed", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", RobustScaler()),
    ]), skewed_cols),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(drop="first", sparse_output=False)),
    ]), cat_cols),
])

X = preprocessor.fit_transform(df.drop("target", axis=1))
print(f"Transformed shape: {X.shape}")
print(f"Feature names: {preprocessor.get_feature_names_out()}")"""
},
"todos": [
    "Apply StandardScaler, MinMaxScaler, and RobustScaler to the same column — print mean and std for each",
    "Train a KNN classifier on unscaled vs StandardScaler-scaled data and compare accuracy",
    "Demonstrate data leakage by fitting a scaler on the full dataset before splitting — check test set mean",
    "Build a ColumnTransformer that applies RobustScaler to one column and StandardScaler to another",
    "Confirm that tree-based models (RandomForest) give the same accuracy with and without scaling",
],
},

{
"title": "7. Creating New Features — Feature Engineering",
"desc": "Feature engineering is the art of creating new informative features from existing data. Good features can improve model performance more than better algorithms.",
"examples": [
{"label": "Mathematical transformations", "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "length": np.random.uniform(1, 10, 100),
    "width": np.random.uniform(1, 5, 100),
    "height": np.random.uniform(1, 3, 100),
    "price": np.random.lognormal(5, 1, 100),
    "quantity": np.random.randint(1, 100, 100),
})

# Ratios
df["aspect_ratio"] = df["length"] / df["width"]
df["price_per_unit"] = df["price"] / df["quantity"]

# Products (interaction features)
df["volume"] = df["length"] * df["width"] * df["height"]
df["surface_area"] = 2 * (df["length"]*df["width"] + df["width"]*df["height"] + df["length"]*df["height"])

# Log transforms (for skewed data)
df["log_price"] = np.log1p(df["price"])

# Power transforms
df["length_squared"] = df["length"] ** 2
df["sqrt_quantity"] = np.sqrt(df["quantity"])

# Binning
df["price_bin"] = pd.cut(df["price"], bins=5, labels=["very_low", "low", "medium", "high", "very_high"])
df["qty_bucket"] = pd.qcut(df["quantity"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])

print(df[["price", "log_price", "price_bin", "quantity", "qty_bucket"]].head(10))"""},
{"label": "Date/time feature extraction", "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=365, freq="D")
df = pd.DataFrame({
    "date": dates,
    "sales": np.random.poisson(100, 365) + np.sin(np.arange(365) / 365 * 2 * np.pi) * 30,
})

# Extract temporal features
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.dayofweek     # 0=Mon, 6=Sun
df["day_name"] = df["date"].dt.day_name()
df["quarter"] = df["date"].dt.quarter
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
df["is_month_end"] = df["date"].dt.is_month_end.astype(int)
df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

# Cyclical encoding (for models that don't understand periodicity)
df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)

print(df[["date", "month", "day_of_week", "is_weekend", "month_sin", "month_cos"]].head(10))"""},
{"label": "Text-derived features", "code":
"""import pandas as pd

df = pd.DataFrame({
    "review": [
        "Great product! Highly recommend!!",
        "Terrible quality. Broke after one day.",
        "It's okay. Nothing special.",
        "ABSOLUTELY AMAZING MUST BUY!!!",
        "Worst purchase ever. Total waste of money.",
    ],
})

# Length features
df["char_count"] = df["review"].str.len()
df["word_count"] = df["review"].str.split().str.len()
df["avg_word_len"] = df["char_count"] / df["word_count"]

# Punctuation features
df["exclamation_count"] = df["review"].str.count("!")
df["question_count"] = df["review"].str.count("\\?")

# Case features
df["upper_ratio"] = df["review"].apply(lambda x: sum(c.isupper() for c in x) / len(x))

# Sentiment proxy features (without NLP model)
positive_words = {"great", "amazing", "recommend", "love", "best", "excellent"}
negative_words = {"terrible", "worst", "broke", "waste", "bad", "awful"}

df["positive_count"] = df["review"].str.lower().apply(
    lambda x: sum(1 for w in x.split() if w.strip(".,!?") in positive_words)
)
df["negative_count"] = df["review"].str.lower().apply(
    lambda x: sum(1 for w in x.split() if w.strip(".,!?") in negative_words)
)

print(df[["review", "word_count", "exclamation_count", "upper_ratio", "positive_count", "negative_count"]].to_string())"""},
],
"rw": {
    "title": "Feature Engineering for E-commerce Churn",
    "scenario": "An e-commerce company wants to predict customer churn. Raw transaction data needs to be transformed into customer-level features that capture behavior patterns.",
    "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
n_transactions = 5000
n_customers = 200

transactions = pd.DataFrame({
    "customer_id": np.random.randint(1, n_customers + 1, n_transactions),
    "date": pd.date_range("2023-01-01", periods=n_transactions, freq="2h"),
    "amount": np.random.lognormal(3, 1, n_transactions),
    "category": np.random.choice(["electronics", "clothing", "food", "books"], n_transactions),
})

# Engineer customer-level features from transactions
def build_customer_features(txns):
    today = txns["date"].max()

    features = txns.groupby("customer_id").agg(
        total_transactions=("amount", "count"),
        total_spend=("amount", "sum"),
        avg_spend=("amount", "mean"),
        std_spend=("amount", "std"),
        max_spend=("amount", "max"),
        first_purchase=("date", "min"),
        last_purchase=("date", "max"),
        unique_categories=("category", "nunique"),
    )

    # Recency, Frequency, Monetary (RFM)
    features["recency_days"] = (today - features["last_purchase"]).dt.days
    features["tenure_days"] = (today - features["first_purchase"]).dt.days
    features["purchase_frequency"] = features["total_transactions"] / (features["tenure_days"] + 1) * 30

    # Coefficient of variation (spending consistency)
    features["spend_cv"] = features["std_spend"] / features["avg_spend"]

    # Category diversity ratio
    features["category_diversity"] = features["unique_categories"] / 4

    return features.drop(columns=["first_purchase", "last_purchase"])

customer_features = build_customer_features(transactions)
print(customer_features.describe().round(2))
print(f"\\nFeature count: {customer_features.shape[1]}")"""
},
"practice": {
    "title": "Feature Engineering Challenge",
    "desc": "Given raw sales data, create at least 10 meaningful features including ratios, time-based, and aggregation features. Explain why each feature might be predictive.",
    "starter":
"""import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "date": pd.date_range("2023-01-01", periods=1000, freq="D"),
    "store_id": np.random.choice(["A", "B", "C"], 1000),
    "product": np.random.choice(["widget", "gadget", "tool"], 1000),
    "quantity": np.random.poisson(10, 1000),
    "unit_price": np.random.uniform(5, 100, 1000).round(2),
    "discount_pct": np.random.choice([0, 5, 10, 15, 20], 1000),
})

# TODO: Create at least 10 features:
# 1. Revenue = quantity * unit_price * (1 - discount_pct/100)
# 2. Is weekend
# 3. Month, quarter
# 4. Discount flag (any discount or not)
# 5. Revenue per unit
# 6. Rolling 7-day average revenue per store
# 7. Days since last purchase per product
# 8. Store-level average price
# 9. Product popularity rank
# 10. Your own creative feature!

# Show the final DataFrame with all features
"""
},
"todos": [
    "Create ratio features (price_per_unit, aspect_ratio) and check their correlation with a target",
    "Extract 5 datetime features (month, day_of_week, is_weekend, quarter, is_month_end) from a date column",
    "Build RFM (Recency, Frequency, Monetary) features from a transactions DataFrame",
    "Apply cyclical encoding (sin/cos) to month and day_of_week and confirm Dec and Jan are close together",
    "Create at least 3 text-derived features from a review column (length, exclamation count, upper ratio)",
],
},

{
"title": "8. Polynomial & Interaction Features",
"desc": "Polynomial features capture non-linear relationships, while interaction features capture how two variables together affect the target differently than each alone.",
"examples": [
{"label": "Creating polynomial features", "code":
"""import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

# Simple example
X = np.array([[2, 3], [4, 5], [6, 7]])

# Degree 2 polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

print("Original features: [a, b]")
print("Polynomial features:", poly.get_feature_names_out())
print(pd.DataFrame(X_poly, columns=poly.get_feature_names_out()))

# Interaction only (no powers)
inter = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_inter = inter.fit_transform(X)
print("\\nInteraction only:", inter.get_feature_names_out())
print(pd.DataFrame(X_inter, columns=inter.get_feature_names_out()))"""},
{"label": "When polynomial features help", "code":
"""import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

# Data with non-linear relationship
np.random.seed(42)
X = np.random.uniform(0, 10, 100).reshape(-1, 1)
y = 3 * X.ravel()**2 - 2 * X.ravel() + 5 + np.random.normal(0, 10, 100)

# Linear model (poor fit for quadratic data)
lr = LinearRegression()
lr.fit(X, y)
print(f"Linear R2: {r2_score(y, lr.predict(X)):.4f}")

# Polynomial features + linear model = polynomial regression!
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
lr_poly = LinearRegression()
lr_poly.fit(X_poly, y)
print(f"Poly(2) R2: {r2_score(y, lr_poly.predict(X_poly)):.4f}")

# Degree 3
poly3 = PolynomialFeatures(degree=3, include_bias=False)
X_poly3 = poly3.fit_transform(X)
lr_poly3 = LinearRegression()
lr_poly3.fit(X_poly3, y)
print(f"Poly(3) R2: {r2_score(y, lr_poly3.predict(X_poly3)):.4f}")

# WARNING: too many features with high degree
for d in [2, 3, 4, 5]:
    poly = PolynomialFeatures(degree=d, include_bias=False)
    print(f"Degree {d}: {poly.fit_transform(np.zeros((1, 5))).shape[1]} features from 5 inputs")"""},
],
"todos": [
    "Apply PolynomialFeatures(degree=2) to a 2-column dataset and list all generated feature names",
    "Fit a linear model on raw features vs degree-2 polynomial features — compare R2 scores",
    "Use interaction_only=True to create only interaction terms and check the feature count difference",
    "Show how feature count explodes with high degree — print feature counts for degrees 2 through 6",
    "Fit polynomial regression of degrees 1–5 on a curved dataset and plot train vs test error",
],
},

{
"title": "9. Handling Imbalanced Data",
"desc": "When one class dominates (e.g., 99% non-fraud, 1% fraud), models tend to predict the majority class. Resampling and weighting techniques fix this.",
"examples": [
{"label": "Understanding imbalance", "code":
"""import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

# Create imbalanced dataset (95% class 0, 5% class 1)
X, y = make_classification(n_samples=2000, n_features=10,
                           weights=[0.95, 0.05], random_state=42)

print(f"Class distribution:")
print(pd.Series(y).value_counts().sort_index())
print(f"\\nImbalance ratio: {sum(y==0)/sum(y==1):.0f}:1")

# Naive model always predicts majority class
naive_accuracy = sum(y==0) / len(y)
print(f"Naive accuracy (always predict 0): {naive_accuracy:.1%}")
print("← This looks great but catches 0% of the minority class!")"""},
{"label": "Resampling: SMOTE and undersampling", "code":
"""import numpy as np
from sklearn.datasets import make_classification
from collections import Counter

# pip install imbalanced-learn
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek

X, y = make_classification(n_samples=2000, n_features=10,
                           weights=[0.95, 0.05], random_state=42)
print(f"Original: {Counter(y)}")

# Random oversampling (duplicate minority samples)
ros = RandomOverSampler(random_state=42)
X_ros, y_ros = ros.fit_resample(X, y)
print(f"Random oversample: {Counter(y_ros)}")

# SMOTE (create synthetic minority samples)
smote = SMOTE(random_state=42)
X_smote, y_smote = smote.fit_resample(X, y)
print(f"SMOTE: {Counter(y_smote)}")

# Random undersampling (remove majority samples)
rus = RandomUnderSampler(random_state=42)
X_rus, y_rus = rus.fit_resample(X, y)
print(f"Random undersample: {Counter(y_rus)}")

# SMOTE + Tomek links (combined approach)
smt = SMOTETomek(random_state=42)
X_smt, y_smt = smt.fit_resample(X, y)
print(f"SMOTE+Tomek: {Counter(y_smt)}")"""},
{"label": "Class weights in models", "code":
"""import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=2000, n_features=10,
                           weights=[0.95, 0.05], random_state=42)

# Without class weights
lr = LogisticRegression(max_iter=1000)
scores = cross_val_score(lr, X, y, cv=5, scoring="f1")
print(f"LogReg (no weights)  F1: {scores.mean():.3f}")

# With class_weight='balanced' (automatically adjusts)
lr_bal = LogisticRegression(class_weight="balanced", max_iter=1000)
scores_bal = cross_val_score(lr_bal, X, y, cv=5, scoring="f1")
print(f"LogReg (balanced)    F1: {scores_bal.mean():.3f}")

# Random Forest with class weights
rf = RandomForestClassifier(n_estimators=100, random_state=42)
scores_rf = cross_val_score(rf, X, y, cv=5, scoring="f1")
print(f"RF (no weights)      F1: {scores_rf.mean():.3f}")

rf_bal = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
scores_rf_bal = cross_val_score(rf_bal, X, y, cv=5, scoring="f1")
print(f"RF (balanced)        F1: {scores_rf_bal.mean():.3f}")"""},
],
"rw": {
    "title": "Fraud Detection with Imbalanced Data",
    "scenario": "A bank has 0.5% fraud rate in transactions. Build a pipeline that handles the extreme imbalance while maximizing fraud detection without too many false alarms.",
    "code":
"""import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

# Simulated fraud data (0.5% fraud rate)
X, y = make_classification(n_samples=10000, n_features=15,
                           weights=[0.995, 0.005],
                           n_informative=10, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# Pipeline: SMOTE + Random Forest
pipeline = ImbPipeline([
    ("smote", SMOTE(sampling_strategy=0.3, random_state=42)),  # 30% minority ratio
    ("clf", RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced_subsample",
        random_state=42,
    )),
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print("Fraud Detection Results:")
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Fraud"]))"""
},
"todos": [
    "Create a 95/5 imbalanced dataset and show that a naive model achieves high accuracy but zero recall",
    "Apply SMOTE and print the class distribution before and after — confirm minority class is upsampled",
    "Train a LogisticRegression with class_weight='balanced' and compare F1 to the default version",
    "Use stratify=y in train_test_split to preserve class ratios and verify the test set distribution",
    "Try SMOTE vs random oversampling vs undersampling — compare their F1 scores using cross-validation",
],
},

{
"title": "10. Feature Selection",
"desc": "Not all features help your model. Feature selection removes irrelevant or redundant features, improving model performance, interpretability, and training speed.",
"examples": [
{"label": "Filter methods: correlation and variance", "code":
"""import pandas as pd
import numpy as np

np.random.seed(42)
n = 500
df = pd.DataFrame({
    "useful_1": np.random.normal(0, 1, n),
    "useful_2": np.random.normal(0, 1, n),
    "correlated": None,  # will correlate with useful_1
    "constant": 5.0,      # zero variance — useless
    "near_constant": np.where(np.random.random(n) > 0.99, 1, 0),  # almost constant
    "random_noise": np.random.normal(0, 1, n),
})
df["correlated"] = df["useful_1"] * 0.9 + np.random.normal(0, 0.1, n)
df["target"] = 2 * df["useful_1"] + 3 * df["useful_2"] + np.random.normal(0, 0.5, n)

# Remove zero/near-zero variance
from sklearn.feature_selection import VarianceThreshold
selector = VarianceThreshold(threshold=0.01)
cols_before = df.drop("target", axis=1).columns.tolist()
X_var = selector.fit_transform(df.drop("target", axis=1))
cols_after = [c for c, keep in zip(cols_before, selector.get_support()) if keep]
print(f"Variance filter: {len(cols_before)} → {len(cols_after)} features")
print(f"Removed: {set(cols_before) - set(cols_after)}")

# Remove highly correlated features
corr = df[cols_after].corr().abs()
upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
to_drop = [c for c in upper.columns if any(upper[c] > 0.85)]
print(f"\\nHighly correlated (>0.85): {to_drop}")

# Correlation with target
target_corr = df[cols_after].corrwith(df["target"]).abs().sort_values(ascending=False)
print(f"\\nCorrelation with target:")
print(target_corr)"""},
{"label": "Wrapper methods: RFE and model-based", "code":
"""import numpy as np
from sklearn.datasets import make_classification
from sklearn.feature_selection import RFE, SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LassoCV

X, y = make_classification(n_samples=500, n_features=20,
                           n_informative=5, n_redundant=5,
                           random_state=42)

# Recursive Feature Elimination (RFE)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rfe = RFE(rf, n_features_to_select=5)
rfe.fit(X, y)
print(f"RFE selected features: {np.where(rfe.support_)[0]}")
print(f"Feature ranking: {rfe.ranking_}")

# SelectFromModel with Random Forest importance
sfm = SelectFromModel(rf, max_features=5)
sfm.fit(X, y)
print(f"\\nRF importance selected: {np.where(sfm.get_support())[0]}")

# Lasso regularization (automatic feature selection)
from sklearn.preprocessing import StandardScaler
X_scaled = StandardScaler().fit_transform(X)
lasso = LassoCV(cv=5, random_state=42)
lasso.fit(X_scaled, y)
important = np.where(np.abs(lasso.coef_) > 0.01)[0]
print(f"\\nLasso selected ({len(important)} features): {important}")"""},
],
"rw": {
    "title": "Automated Feature Selection Pipeline",
    "scenario": "A dataset has 200 features after engineering. Systematically reduce to the most predictive subset using multiple methods and cross-validation.",
    "code":
"""import numpy as np
from sklearn.datasets import make_classification
from sklearn.feature_selection import mutual_info_classif, SelectKBest
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=1000, n_features=50,
                           n_informative=10, n_redundant=15,
                           random_state=42)

# Method 1: Mutual Information
mi = mutual_info_classif(X, y, random_state=42)
top_mi = np.argsort(mi)[-10:]
print(f"Top 10 by mutual info: {sorted(top_mi)}")

# Method 2: Random Forest importance
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X, y)
top_rf = np.argsort(rf.feature_importances_)[-10:]
print(f"Top 10 by RF importance: {sorted(top_rf)}")

# Method 3: Consensus — features selected by both methods
consensus = set(top_mi) & set(top_rf)
print(f"\\nConsensus features: {sorted(consensus)}")

# Compare performance
for name, features in [("All 50", list(range(50))), ("MI top 10", top_mi),
                        ("RF top 10", top_rf), ("Consensus", list(consensus))]:
    scores = cross_val_score(rf, X[:, features], y, cv=5, scoring="accuracy")
    print(f"  {name:15s}: {scores.mean():.4f} (+/- {scores.std():.4f})")"""
},
"todos": [
    "Use VarianceThreshold to remove constant and near-constant columns from a dataset",
    "Build a correlation matrix and drop one feature from each pair with correlation > 0.9",
    "Run RFE with n_features_to_select=5 and print the ranking of all remaining features",
    "Compare mutual_info_classif rankings vs RandomForest feature_importances_ — how much do they agree?",
    "Run cross-validation with all features vs top-10 selected features and compare accuracy",
],
},

{
"title": "11. Preventing Data Leakage",
"desc": "Data leakage is when information from the test set or the future leaks into training, giving unrealistically good results that fail in production. It's the #1 mistake in ML projects.",
"examples": [
{"label": "Common leakage sources", "code":
"""import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
X = np.random.normal(0, 1, (1000, 5))
y = (X[:, 0] + X[:, 1] > 0).astype(int)

# LEAK 1: Scaling before splitting
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # fit on ALL data including test!
X_train, X_test = train_test_split(X_scaled, test_size=0.2)
# Fix: split first, then fit_transform on train only

# LEAK 2: Feature selection on all data
from sklearn.feature_selection import SelectKBest, f_classif
selector = SelectKBest(f_classif, k=3)
X_selected = selector.fit_transform(X, y)  # uses ALL labels!
# Fix: select features using only training data

# LEAK 3: Target encoding on all data
df = pd.DataFrame({"cat": np.random.choice(["A", "B"], 1000), "target": y})
df["cat_encoded"] = df.groupby("cat")["target"].transform("mean")
# This uses the test set's target values in the encoding!
# Fix: encode using only training fold values

print("Common leakage sources:")
print("1. Scaling/normalizing before train-test split")
print("2. Feature selection using full dataset")
print("3. Target encoding using full dataset")
print("4. Using future data to predict the past (time series)")
print("5. Including features derived from the target")"""},
{"label": "The correct way: sklearn Pipelines", "code":
"""import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

np.random.seed(42)
X = np.random.normal(0, 1, (500, 20))
y = (X[:, 0] + X[:, 1] + X[:, 2] > 0).astype(int)

# Pipeline ensures each step fits ONLY on training data
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("selector", SelectKBest(f_classif, k=5)),
    ("model", LogisticRegression()),
])

# cross_val_score handles the split correctly:
# For each fold: fit scaler → fit selector → fit model on TRAIN
# Then: transform test → select features → predict on TEST
scores = cross_val_score(pipe, X, y, cv=5, scoring="accuracy")
print(f"Pipeline CV accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")
print("Each fold's scaler and selector were fit ONLY on training data!")"""},
{"label": "Time series leakage", "code":
"""import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=365, freq="D")
df = pd.DataFrame({
    "date": dates,
    "value": np.cumsum(np.random.normal(0, 1, 365)) + 100,
})

# WRONG: random split shuffles time
# train_test_split would mix future data into training!

# CORRECT: TimeSeriesSplit preserves temporal order
tss = TimeSeriesSplit(n_splits=5)
for i, (train_idx, test_idx) in enumerate(tss.split(df)):
    train_end = df.iloc[train_idx[-1]]["date"].date()
    test_start = df.iloc[test_idx[0]]["date"].date()
    print(f"Fold {i+1}: Train ends {train_end}, Test starts {test_start} ({len(test_idx)} days)")

# WRONG: using future-derived features
# df["next_day_value"] = df["value"].shift(-1)  # LEAK!
# df["rolling_mean"] = df["value"].rolling(7).mean()  # OK if no shift

# CORRECT: only use past data
df["lag_1"] = df["value"].shift(1)     # yesterday's value
df["lag_7"] = df["value"].shift(7)     # last week's value
df["rolling_7_mean"] = df["value"].shift(1).rolling(7).mean()  # shift first!
print(df[["date", "value", "lag_1", "rolling_7_mean"]].head(10))"""},
],
"rw": {
    "title": "Leakage Audit Checklist",
    "scenario": "Before deploying a model, audit the entire pipeline for potential data leakage using this systematic checklist.",
    "code":
"""def leakage_audit(pipeline_description):
    \"\"\"Run through a data leakage audit checklist.\"\"\"
    checks = [
        ("Train-test split happens BEFORE any preprocessing", True),
        ("Scaler fit only on training data", True),
        ("Feature selection uses only training data", True),
        ("Target encoding uses only training fold", True),
        ("No future data used in features (time series)", True),
        ("No features derived directly from target", True),
        ("Cross-validation uses Pipeline (not manual steps)", True),
        ("Time series uses TimeSeriesSplit (not random)", True),
        ("Imputation statistics from training data only", True),
        ("Outlier thresholds computed on training data only", True),
    ]

    print("DATA LEAKAGE AUDIT")
    print("=" * 50)
    all_pass = True
    for check, expected in checks:
        status = "PASS" if expected else "FAIL"
        if not expected:
            all_pass = False
        print(f"  [{status}] {check}")

    print(f"\\nResult: {'ALL CLEAR' if all_pass else 'LEAKAGE DETECTED'}")

leakage_audit("example pipeline")

# Key rule of thumb:
# If your model performs MUCH better in dev than production,
# you probably have data leakage somewhere.
print("\\nRule: If dev performance >> production performance = LEAKAGE")"""
},
"todos": [
    "Deliberately scale data before splitting, then after splitting — compare test set accuracy both ways",
    "Show that fitting a SelectKBest selector on the full dataset inflates CV accuracy vs using a Pipeline",
    "Add a target encoding step outside vs inside a Pipeline and observe the accuracy difference",
    "Use TimeSeriesSplit on a time-indexed dataset and confirm test folds are always in the future",
    "Audit one of your existing projects against the 10-point leakage checklist above",
],
},

{
"title": "12. Building Complete Preprocessing Pipelines",
"desc": "Combine all cleaning and feature engineering steps into a single reproducible sklearn Pipeline. This ensures consistent preprocessing in training and production.",
"examples": [
{"label": "Full preprocessing pipeline", "code":
"""import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

np.random.seed(42)
n = 500
df = pd.DataFrame({
    "age": np.where(np.random.random(n) > 0.9, np.nan, np.random.normal(35, 10, n)),
    "income": np.random.lognormal(10.5, 0.8, n),
    "score": np.random.normal(500, 100, n),
    "education": np.random.choice(["HS", "BS", "MS", "PhD", None], n),
    "city": np.random.choice(["NYC", "LA", "Chicago", "Houston"], n),
    "target": np.random.choice([0, 1], n),
})

num_features = ["age", "income", "score"]
ord_features = ["education"]
cat_features = ["city"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("impute", KNNImputer(n_neighbors=5)),
        ("scale", StandardScaler()),
    ]), num_features),
    ("ord", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OrdinalEncoder(categories=[["HS", "BS", "MS", "PhD"]])),
    ]), ord_features),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(drop="first", sparse_output=False)),
    ]), cat_features),
])

# Full pipeline: preprocess → select → model
full_pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("select", SelectKBest(f_classif, k=5)),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42)),
])

X = df.drop("target", axis=1)
y = df["target"]
scores = cross_val_score(full_pipeline, X, y, cv=5, scoring="accuracy")
print(f"Pipeline CV accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")"""},
{"label": "Saving and loading pipelines", "code":
"""import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

# Build and train pipeline
np.random.seed(42)
X_train = np.random.normal(0, 1, (200, 5))
y_train = (X_train[:, 0] > 0).astype(int)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression()),
])
pipe.fit(X_train, y_train)

# Save entire pipeline (preprocessing + model)
joblib.dump(pipe, "model_pipeline.pkl")
print("Pipeline saved!")

# Load in production
loaded_pipe = joblib.load("model_pipeline.pkl")
X_new = np.random.normal(0, 1, (5, 5))
predictions = loaded_pipe.predict(X_new)
print(f"Predictions: {predictions}")

# The loaded pipeline includes the fitted scaler!
# No need to separately save/load preprocessing steps
import os; os.remove("model_pipeline.pkl")"""},
],
"rw": {
    "title": "Production-Grade ML Pipeline",
    "scenario": "Build a complete pipeline that handles the messy reality of production data — mixed types, missing values, outliers, encoding, scaling, and feature selection.",
    "code":
"""import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score

# Custom transformer for outlier capping
class OutlierCapper(BaseEstimator, TransformerMixin):
    def __init__(self, lower_pct=0.01, upper_pct=0.99):
        self.lower_pct = lower_pct
        self.upper_pct = upper_pct

    def fit(self, X, y=None):
        self.lower_ = np.nanpercentile(X, self.lower_pct * 100, axis=0)
        self.upper_ = np.nanpercentile(X, self.upper_pct * 100, axis=0)
        return self

    def transform(self, X):
        X = np.array(X, dtype=float)
        return np.clip(X, self.lower_, self.upper_)

# Sample data
np.random.seed(42)
n = 1000
df = pd.DataFrame({
    "age": np.where(np.random.random(n) > 0.9, np.nan, np.random.normal(35, 10, n)),
    "income": np.concatenate([np.random.lognormal(10.5, 0.8, 980), [1e8]*20]),
    "tenure": np.random.exponential(3, n),
    "plan": np.random.choice(["basic", "premium", "enterprise", None], n),
    "churned": np.random.choice([0, 1], n, p=[0.85, 0.15]),
})

num_cols = ["age", "income", "tenure"]
cat_cols = ["plan"]

pipeline = Pipeline([
    ("preprocess", ColumnTransformer([
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("cap", OutlierCapper()),
            ("scale", RobustScaler()),
        ]), num_cols),
        ("cat", Pipeline([
            ("impute", SimpleImputer(strategy="constant", fill_value="unknown")),
            ("encode", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")),
        ]), cat_cols),
    ])),
    ("model", GradientBoostingClassifier(n_estimators=100, random_state=42)),
])

X = df.drop("churned", axis=1)
y = df["churned"]
scores = cross_val_score(pipeline, X, y, cv=5, scoring="f1")
print(f"Full pipeline F1: {scores.mean():.4f} (+/- {scores.std():.4f})")"""
},
"practice": {
    "title": "Build Your Own Preprocessing Pipeline",
    "desc": "Create a complete sklearn pipeline for a messy dataset: handle missing values, encode categoricals, scale numerics, and train a model. Use cross-validation to evaluate.",
    "starter":
"""import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

np.random.seed(42)
df = pd.DataFrame({
    "feature_1": np.where(np.random.random(300) > 0.85, np.nan, np.random.normal(0, 1, 300)),
    "feature_2": np.random.lognormal(2, 1, 300),
    "feature_3": np.random.choice(["A", "B", "C", None], 300),
    "feature_4": np.random.choice(["low", "medium", "high"], 300),
    "target": np.random.choice([0, 1], 300),
})

# TODO: Define numeric and categorical columns
# TODO: Build preprocessor with ColumnTransformer
# TODO: Build full pipeline with preprocessor + model
# TODO: Evaluate with cross_val_score
# TODO: Print results
"""
},
"todos": [
    "Build a ColumnTransformer that applies KNNImputer + StandardScaler to numeric cols and OHE to cat cols",
    "Wrap the ColumnTransformer and a classifier into a single Pipeline and run cross_val_score",
    "Save the trained pipeline with joblib.dump and reload it — confirm predictions are identical",
    "Write a custom BaseEstimator transformer (e.g., OutlierCapper) and insert it into a Pipeline step",
    "Add a SelectKBest step after preprocessing in the Pipeline and compare accuracy with/without it",
],
},

]


# ─── Generate ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    html = make_html(SECTIONS)
    (BASE / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote {BASE / 'index.html'}")

    nb = make_nb(SECTIONS)
    nb_path = BASE / "study_guide.ipynb"
    nb_path.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print(f"Wrote {nb_path} ({len(nb['cells'])} cells)")
