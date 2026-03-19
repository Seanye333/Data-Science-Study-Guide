"""Add sections 17-24 to gen_polars.py (code1/code2/code3 format)."""
import os

BASE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path"
FILE = os.path.join(BASE, "gen_polars.py")

def ct(code, indent="            "):
    lines = code.split('\n')
    parts = []
    for line in lines:
        escaped = line.replace('\\', '\\\\').replace('"', '\\"')
        parts.append(f'{indent}"{escaped}\\n"')
    return "(\n" + "\n".join(parts) + "\n        )"

def ec(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace("'", "\\'")

def make_section(num, title, desc, c1t, c1, c2t, c2, c3t=None, c3=None,
                 rw_scenario="", rw_code="", pt="", pd_text="", ps=""):
    s  = f'    {{\n'
    s += f'        "title": "{num}. {title}",\n'
    s += f'        "desc": "{ec(desc)}",\n'
    s += f'        "code1_title": "{c1t}",\n'
    s += f'        "code1": {ct(c1)},\n'
    s += f'        "code2_title": "{c2t}",\n'
    s += f'        "code2": {ct(c2)},\n'
    if c3t and c3:
        s += f'        "code3_title": "{c3t}",\n'
        s += f'        "code3": {ct(c3)},\n'
    s += f'        "rw_scenario": "{ec(rw_scenario)}",\n'
    s += f'        "rw_code": {ct(rw_code)},\n'
    s += f'        "practice": {{\n'
    s += f'            "title": "{ec(pt)}",\n'
    s += f'            "desc": "{ec(pd_text)}",\n'
    s += f'            "starter": {ct(ps)},\n'
    s += f'        }},\n'
    s += f'    }},\n'
    return s

def insert_before_make_html(filepath, new_sections_str):
    content = open(filepath, encoding='utf-8').read()
    marker = '\n]\n\n\ndef make_html'
    idx = content.rfind(marker)
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

# ── Section 17: LazyFrames & Query Optimization ───────────────────────────────
s17 = make_section(17, "LazyFrames & Query Optimization",
    "Polars LazyFrames build a query plan without executing it. Calling .collect() triggers optimized execution with predicate pushdown, projection pushdown, and parallel execution.",
    c1t="LazyFrame Basics",
    c1="""
import polars as pl
import numpy as np

np.random.seed(42)
n = 10_000

# Create a DataFrame
df = pl.DataFrame({
    "id": range(n),
    "category": np.random.choice(["A", "B", "C", "D"], n),
    "value": np.random.randn(n) * 100,
    "quantity": np.random.randint(1, 100, n),
    "active": np.random.choice([True, False], n),
})

# Eager (immediate execution)
eager_result = (df
    .filter(pl.col("active"))
    .filter(pl.col("value") > 0)
    .select(["category", "value", "quantity"])
    .group_by("category")
    .agg(pl.col("value").mean().alias("avg_value"),
         pl.col("quantity").sum().alias("total_qty"))
)
print("Eager result:")
print(eager_result.sort("category"))

# Lazy (deferred execution)
lazy_result = (df.lazy()
    .filter(pl.col("active"))
    .filter(pl.col("value") > 0)
    .select(["category", "value", "quantity"])
    .group_by("category")
    .agg(pl.col("value").mean().alias("avg_value"),
         pl.col("quantity").sum().alias("total_qty"))
    .collect()  # execute here
)
print("\\nLazy result (same output):")
print(lazy_result.sort("category"))
print(f"\\nResults match: {eager_result.sort('category').equals(lazy_result.sort('category'))}")
""".strip(),
    c2t="Query Plan & Optimization",
    c2="""
import polars as pl
import numpy as np

np.random.seed(42)
n = 50_000
df = pl.DataFrame({
    "user_id": range(n),
    "age": np.random.randint(18, 70, n),
    "country": np.random.choice(["US", "UK", "DE", "FR", "JP"], n),
    "purchase_amount": np.random.exponential(50, n),
    "is_premium": np.random.choice([True, False], n),
})

# Build lazy query
q = (df.lazy()
     .filter(pl.col("is_premium") & (pl.col("age") >= 25))
     .filter(pl.col("purchase_amount") > 20)
     .select(["user_id", "country", "purchase_amount", "age"])
     .group_by("country")
     .agg([
         pl.col("purchase_amount").mean().alias("avg_purchase"),
         pl.col("purchase_amount").max().alias("max_purchase"),
         pl.len().alias("n_users"),
     ])
     .sort("avg_purchase", descending=True)
)

# Inspect the query plan
print("Optimized query plan:")
print(q.explain(optimized=True))

# Execute
result = q.collect()
print("\\nResult:")
print(result)
""".strip(),
    c3t="Streaming Large Datasets",
    c3="""
import polars as pl
import numpy as np, tempfile, os

np.random.seed(42)

# Create a large CSV file for streaming demo
with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
    csv_path = f.name
    f.write("id,category,value,quantity\\n")
    for i in range(100_000):
        cat = np.random.choice(["X","Y","Z"])
        val = round(np.random.randn()*100, 2)
        qty = np.random.randint(1, 50)
        f.write(f"{i},{cat},{val},{qty}\\n")

# Stream processing: process without loading all data into memory
result = (
    pl.scan_csv(csv_path)  # scan_csv returns LazyFrame
    .filter(pl.col("value") > 0)
    .group_by("category")
    .agg([
        pl.col("value").sum().alias("total_value"),
        pl.col("quantity").mean().alias("avg_qty"),
        pl.len().alias("count"),
    ])
    .sort("total_value", descending=True)
    .collect(streaming=True)  # stream=True for memory-efficient processing
)

print(f"File size: {os.path.getsize(csv_path)/1024:.0f} KB")
print("Streaming result:")
print(result)
os.unlink(csv_path)
""".strip(),
    rw_scenario="You have a 10GB log file with 50M rows. Filter logs by status code, compute hourly request rates per endpoint, and find the top 10 slowest endpoints. Use LazyFrames for memory efficiency.",
    rw_code="""
import polars as pl
import numpy as np, tempfile, os

np.random.seed(42)
n = 50_000

# Simulate log data
endpoints = ["/api/users", "/api/orders", "/api/products", "/api/search", "/api/auth"]
logs = pl.DataFrame({
    "timestamp": pl.Series([f"2024-01-15 {h:02d}:{m:02d}:{s:02d}"
                            for h, m, s in zip(
                                np.random.randint(0, 24, n),
                                np.random.randint(0, 60, n),
                                np.random.randint(0, 60, n))]),
    "endpoint": np.random.choice(endpoints, n),
    "status_code": np.random.choice([200, 200, 200, 400, 404, 500], n),
    "response_ms": np.random.exponential(100, n),
    "user_id": np.random.randint(1, 10000, n),
})

# Process with LazyFrames
result = (logs.lazy()
    .filter(pl.col("status_code") < 400)  # only successful requests
    .with_columns(
        pl.col("timestamp").str.slice(11, 2).cast(pl.Int32).alias("hour")
    )
    .group_by(["endpoint", "hour"])
    .agg([
        pl.len().alias("request_count"),
        pl.col("response_ms").mean().round(2).alias("avg_ms"),
        pl.col("response_ms").quantile(0.95).round(2).alias("p95_ms"),
    ])
    .sort("avg_ms", descending=True)
    .collect()
)

print("Top slowest endpoint/hour combos:")
print(result.head(10))

# Top slowest endpoints overall
slowest = (logs.lazy()
    .group_by("endpoint")
    .agg(pl.col("response_ms").mean().round(2).alias("avg_ms"),
         pl.col("response_ms").quantile(0.99).round(2).alias("p99_ms"),
         pl.len().alias("total_requests"))
    .sort("avg_ms", descending=True)
    .collect())
print("\\nEndpoint Performance:")
print(slowest)
""".strip(),
    pt="LazyFrame Pipeline",
    pd_text="Build a LazyFrame pipeline that filters rows, adds a computed column, groups by a category, and collects the result. Check .explain() before collecting.",
    ps="""
import polars as pl
import numpy as np

np.random.seed(42)
df = pl.DataFrame({
    "category": np.random.choice(["A","B","C"], 1000),
    "x": np.random.randn(1000),
    "y": np.random.randint(1, 100, 1000),
})
# 1. df.lazy()
# 2. .filter(pl.col("x") > 0)
# 3. .with_columns((pl.col("x") * pl.col("y")).alias("xy"))
# 4. .group_by("category").agg(...)
# 5. print .explain() before .collect()
""".strip()
)

# ── Section 18: Advanced GroupBy & Aggregations ───────────────────────────────
s18 = make_section(18, "Advanced GroupBy & Aggregations",
    "Polars GroupBy supports parallel multi-aggregation, dynamic grouping, rolling windows, and complex expressions that outperform pandas groupby significantly.",
    c1t="Multi-Column & Complex Aggregations",
    c1="""
import polars as pl
import numpy as np

np.random.seed(42)
n = 5000
df = pl.DataFrame({
    "date": pl.date_range(pl.date(2024, 1, 1), pl.date(2024, 12, 31), "1d", eager=True)[:n % 366].extend(
        pl.date_range(pl.date(2024, 1, 1), pl.date(2024, 12, 31), "1d", eager=True)
    )[:n],
    "product": np.random.choice(["Widget", "Gadget", "Doohickey", "Thingamajig"], n),
    "region": np.random.choice(["North", "South", "East", "West"], n),
    "sales": np.random.exponential(100, n).round(2),
    "units": np.random.randint(1, 50, n),
    "returned": np.random.choice([True, False], n, p=[0.1, 0.9]),
})

# Multi-column groupby with complex aggregations
result = df.group_by(["product", "region"]).agg([
    pl.col("sales").sum().alias("total_sales"),
    pl.col("sales").mean().round(2).alias("avg_sale"),
    pl.col("sales").std().round(2).alias("std_sale"),
    pl.col("units").sum().alias("total_units"),
    pl.col("returned").mean().round(4).alias("return_rate"),
    pl.len().alias("n_transactions"),
    pl.col("sales").quantile(0.9).round(2).alias("p90_sale"),
]).sort(["product", "total_sales"], descending=[False, True])

print("Product x Region aggregation:")
print(result.head(8))
print(f"\\nTotal rows: {result.shape[0]}")
""".strip(),
    c2t="Rolling & Dynamic GroupBy",
    c2="""
import polars as pl
import numpy as np

np.random.seed(42)
n = 200
dates = pl.date_range(pl.date(2024, 1, 1), period=f"{n}d", interval="1d", eager=True)
df = pl.DataFrame({
    "date": dates,
    "value": np.cumsum(np.random.randn(n)) + 50,
    "volume": np.random.randint(100, 1000, n),
})

# Rolling aggregations (7-day moving average)
df_rolling = df.with_columns([
    pl.col("value").rolling_mean(window_size=7).alias("ma7"),
    pl.col("value").rolling_mean(window_size=30).alias("ma30"),
    pl.col("value").rolling_std(window_size=7).alias("std7"),
    pl.col("volume").rolling_sum(window_size=7).alias("vol7"),
])
print("Rolling aggregations:")
print(df_rolling.tail(5))

# Dynamic groupby (group by month)
df_monthly = (df
    .with_columns(pl.col("date").dt.month().alias("month"))
    .group_by("month")
    .agg([
        pl.col("value").mean().round(2).alias("avg_val"),
        pl.col("value").max().alias("max_val"),
        pl.col("volume").sum().alias("total_vol"),
    ])
    .sort("month")
)
print("\\nMonthly aggregation:")
print(df_monthly)
""".strip(),
    c3t="Conditional Aggregations & Pivot",
    c3="""
import polars as pl
import numpy as np

np.random.seed(42)
n = 1000
df = pl.DataFrame({
    "quarter": np.random.choice(["Q1","Q2","Q3","Q4"], n),
    "product": np.random.choice(["A","B","C"], n),
    "sales": np.random.exponential(100, n).round(2),
    "target": np.random.uniform(80, 120, n).round(2),
})

# Conditional aggregation: count by condition
result = df.group_by(["quarter", "product"]).agg([
    pl.col("sales").sum().alias("total_sales"),
    (pl.col("sales") > pl.col("target")).sum().alias("above_target"),
    pl.len().alias("n"),
    ((pl.col("sales") > pl.col("target")).sum() / pl.len()).round(3).alias("hit_rate"),
])
print("Conditional aggregation:")
print(result.sort(["quarter", "product"]).head(8))

# Pivot: reshape data (like pandas pivot_table)
pivot = (df.group_by(["quarter", "product"])
    .agg(pl.col("sales").sum().alias("total"))
    .pivot(index="quarter", on="product", values="total", aggregate_function="sum")
    .sort("quarter"))
print("\\nPivot table (quarter x product sales):")
print(pivot)
""".strip(),
    rw_scenario="Analyze e-commerce sales data: compute weekly revenue per product category, find categories with >20% week-over-week growth, and identify top customers by lifetime value with return rates.",
    rw_code="""
import polars as pl
import numpy as np

np.random.seed(42)
n = 10_000
dates = pl.date_range(pl.date(2024, 1, 1), pl.date(2024, 12, 31), "1d", eager=True)

df = pl.DataFrame({
    "order_date": np.random.choice(dates.to_list(), n),
    "customer_id": np.random.randint(1, 1000, n),
    "category": np.random.choice(["Electronics","Clothing","Books","Sports","Home"], n),
    "amount": np.random.exponential(80, n).round(2),
    "returned": np.random.choice([False, True], n, p=[0.88, 0.12]),
})

# Weekly revenue by category
weekly = (df.lazy()
    .with_columns(pl.col("order_date").dt.week().alias("week"))
    .filter(~pl.col("returned"))
    .group_by(["week", "category"])
    .agg(pl.col("amount").sum().round(2).alias("revenue"), pl.len().alias("orders"))
    .sort(["week", "category"])
    .collect()
)
print("Weekly revenue (first 10 rows):")
print(weekly.head(10))

# Customer lifetime value
clv = (df.lazy()
    .group_by("customer_id")
    .agg([
        pl.col("amount").sum().round(2).alias("ltv"),
        pl.len().alias("total_orders"),
        pl.col("returned").mean().round(3).alias("return_rate"),
        pl.col("amount").mean().round(2).alias("avg_order"),
    ])
    .sort("ltv", descending=True)
    .head(10)
    .collect()
)
print("\\nTop 10 Customers by LTV:")
print(clv)
""".strip(),
    pt="Advanced GroupBy",
    pd_text="Group a DataFrame by two columns, compute sum, mean, std, and a conditional count. Then pivot the result and sort by the total column.",
    ps="""
import polars as pl
import numpy as np

np.random.seed(42)
df = pl.DataFrame({
    "region": np.random.choice(["North","South","East","West"], 500),
    "product": np.random.choice(["A","B","C"], 500),
    "sales": np.random.exponential(100, 500).round(2),
    "returned": np.random.choice([True, False], 500),
})
# 1. group_by(["region", "product"])
# 2. agg sum, mean, std of sales + count of returned
# 3. Pivot to show product as columns
""".strip()
)

# ── Section 19: Joins & Set Operations ───────────────────────────────────────
s19 = make_section(19, "Joins & Set Operations",
    "Polars supports all join types (inner, left, outer, cross, semi, anti) with parallel execution. Join strategies (hash, sort-merge) are auto-selected based on data characteristics.",
    c1t="Inner, Left & Outer Joins",
    c1="""
import polars as pl
import numpy as np

np.random.seed(42)

# Customers table
customers = pl.DataFrame({
    "customer_id": range(1, 11),
    "name": [f"Customer_{i}" for i in range(1, 11)],
    "tier": np.random.choice(["Gold", "Silver", "Bronze"], 10),
})

# Orders table
orders = pl.DataFrame({
    "order_id": range(1, 21),
    "customer_id": np.random.choice(range(1, 14), 20),  # some customers missing
    "amount": np.random.exponential(100, 20).round(2),
    "status": np.random.choice(["completed", "pending", "cancelled"], 20),
})

# Inner join: only matching customers
inner = customers.join(orders, on="customer_id", how="inner")
print(f"Inner join: {len(inner)} rows (customers with orders)")

# Left join: all customers, NaN for missing orders
left = customers.join(orders, on="customer_id", how="left")
print(f"Left join:  {len(left)} rows (all customers)")
print(f"  Customers with no orders: {left.filter(pl.col('order_id').is_null()).shape[0]}")

# Full/outer join
outer = customers.join(orders, on="customer_id", how="full")
print(f"Full join:  {len(outer)} rows")

# Aggregation join: aggregate before joining
order_summary = (orders
    .group_by("customer_id")
    .agg([pl.col("amount").sum().alias("total_spend"),
          pl.len().alias("order_count")])
)
enriched = customers.join(order_summary, on="customer_id", how="left")
print("\\nCustomer enriched data:")
print(enriched.head(5))
""".strip(),
    c2t="Semi, Anti Joins & Asof Join",
    c2="""
import polars as pl
import numpy as np

np.random.seed(42)

# Product table
products = pl.DataFrame({
    "product_id": range(1, 21),
    "name": [f"Product_{i}" for i in range(1, 21)],
    "price": np.random.uniform(10, 200, 20).round(2),
    "category": np.random.choice(["Electronics","Clothing","Books"], 20),
})

# Sold products (subset)
sold = pl.DataFrame({
    "product_id": np.random.choice(range(1, 21), 12, replace=False),
    "units_sold": np.random.randint(5, 100, 12),
})

# Semi-join: products that have been sold (filtering join)
has_sold = products.join(sold, on="product_id", how="semi")
print(f"Products sold: {len(has_sold)}")

# Anti-join: products that have NOT been sold
never_sold = products.join(sold, on="product_id", how="anti")
print(f"Products never sold: {len(never_sold)}")
print(never_sold.select(["product_id", "name", "price"]).head(5))

# Cross join (cartesian product)
sizes = pl.DataFrame({"size": ["S", "M", "L", "XL"]})
colors = pl.DataFrame({"color": ["Red", "Blue", "Green"]})
variants = sizes.join(colors, how="cross")
print(f"\\nProduct variants (cross join): {len(variants)} combinations")
print(variants.head(6))
""".strip(),
    c3t="Join Performance Tips",
    c3="""
import polars as pl
import numpy as np, time

np.random.seed(42)
n = 100_000

# Large DataFrames for join performance demo
df_left = pl.DataFrame({
    "id": np.arange(n),
    "value_a": np.random.randn(n),
    "group": np.random.choice(list("ABCDE"), n),
})
df_right = pl.DataFrame({
    "id": np.random.randint(0, n, n),
    "value_b": np.random.randn(n),
    "score": np.random.uniform(0, 1, n),
})

# Standard join
t0 = time.time()
result = df_left.join(df_right, on="id", how="inner")
t1 = time.time()
print(f"Inner join ({len(result):,} rows): {(t1-t0)*1000:.1f}ms")

# Join with pre-filtering (reduce data first)
t0 = time.time()
left_filtered = df_left.filter(pl.col("group").is_in(["A", "B"]))
right_filtered = df_right.filter(pl.col("score") > 0.5)
result_filtered = left_filtered.join(right_filtered, on="id", how="inner")
t1 = time.time()
print(f"Pre-filtered join ({len(result_filtered):,} rows): {(t1-t0)*1000:.1f}ms")

# Multiple join keys
df_multi_left = pl.DataFrame({"key1": list("AABBC"), "key2": [1,2,1,2,1], "val": range(5)})
df_multi_right = pl.DataFrame({"key1": list("AABC"), "key2": [1,2,2,1], "label": list("WXYZ")})
multi_join = df_multi_left.join(df_multi_right, on=["key1", "key2"], how="left")
print("\\nMulti-key join:")
print(multi_join)
""".strip(),
    rw_scenario="Your data warehouse has separate tables: customers, orders, products, and reviews. Join them to build a customer 360-view with total spend, favorite category, and average review score.",
    rw_code="""
import polars as pl
import numpy as np

np.random.seed(42)
n_cust = 500

customers = pl.DataFrame({
    "customer_id": range(n_cust),
    "name": [f"Cust_{i}" for i in range(n_cust)],
    "join_date": pl.date_range(pl.date(2022,1,1), pl.date(2023,12,31), "1d", eager=True)[:n_cust],
})

orders = pl.DataFrame({
    "order_id": range(2000),
    "customer_id": np.random.randint(0, n_cust, 2000),
    "product_id": np.random.randint(0, 50, 2000),
    "amount": np.random.exponential(80, 2000).round(2),
})

products = pl.DataFrame({
    "product_id": range(50),
    "category": np.random.choice(["Electronics","Clothing","Books","Sports"], 50),
    "price": np.random.uniform(10, 500, 50).round(2),
})

reviews = pl.DataFrame({
    "customer_id": np.random.randint(0, n_cust, 1000),
    "rating": np.random.randint(1, 6, 1000),
})

# Build customer 360 view
order_stats = (orders.lazy()
    .join(products.lazy(), on="product_id")
    .group_by("customer_id")
    .agg([
        pl.col("amount").sum().round(2).alias("total_spend"),
        pl.len().alias("n_orders"),
        pl.col("category").mode().first().alias("fav_category"),
    ])
)

review_stats = (reviews.lazy()
    .group_by("customer_id")
    .agg(pl.col("rating").mean().round(2).alias("avg_rating"))
)

customer360 = (customers.lazy()
    .join(order_stats, on="customer_id", how="left")
    .join(review_stats, on="customer_id", how="left")
    .sort("total_spend", descending=True)
    .collect()
)
print("Customer 360 View (top 10):")
print(customer360.head(10))
""".strip(),
    pt="Multi-Table Joins",
    pd_text="Join three DataFrames using inner and left joins, then use an anti-join to find records in one table that have no match in another.",
    ps="""
import polars as pl
import numpy as np

np.random.seed(42)
users = pl.DataFrame({"user_id": range(10), "name": [f"U{i}" for i in range(10)]})
orders = pl.DataFrame({"order_id": range(15), "user_id": np.random.randint(0, 12, 15), "amount": np.random.randn(15)})
products = pl.DataFrame({"product_id": range(5), "category": list("AABBC")})
# 1. Inner join users and orders
# 2. Left join result with products (on a fake key)
# 3. Anti-join: find users with no orders
""".strip()
)

# ── Section 20: String & Regex Operations ────────────────────────────────────
s20 = make_section(20, "String & Regex Operations",
    "Polars string operations are vectorized and run in parallel. The .str namespace provides split, replace, extract, slice, strip, and regex operations optimized for large text columns.",
    c1t="String Manipulation",
    c1="""
import polars as pl
import numpy as np

# Sample text data
df = pl.DataFrame({
    "email": ["alice@example.com", "BOB.SMITH@Gmail.COM", "  charlie@test.org  ",
              "invalid-email", "diana.prince@hero.net"],
    "full_name": ["Alice Johnson", "Bob Smith", "Charlie Brown",
                  "Diana Prince", "Eve Williams"],
    "phone": ["(555) 123-4567", "555.234.5678", "1-555-345-6789",
              "5554567890", "555 456 7890"],
    "description": ["  Product is great! ", "NEEDS improvement",
                    "works as expected...", "  EXCELLENT quality  ", "good value"],
})

# String operations
result = df.with_columns([
    pl.col("email").str.to_lowercase().str.strip_chars().alias("email_clean"),
    pl.col("full_name").str.split(" ").list.first().alias("first_name"),
    pl.col("full_name").str.split(" ").list.last().alias("last_name"),
    pl.col("description").str.strip_chars().str.to_lowercase().alias("desc_clean"),
    pl.col("phone").str.replace_all(r"[^\\d]", "").alias("phone_digits"),
])

print("String operations result:")
print(result.select(["email_clean", "first_name", "last_name", "phone_digits", "desc_clean"]))

# String contains/starts_with/ends_with
email_check = df.with_columns([
    pl.col("email").str.contains("@").alias("has_at"),
    pl.col("email").str.ends_with(".com").alias("is_dotcom"),
    pl.col("email").str.contains("@").alias("is_valid"),
])
print("\\nEmail validation:")
print(email_check.select(["email", "has_at", "is_dotcom", "is_valid"]))
""".strip(),
    c2t="Regex Extraction & Pattern Matching",
    c2="""
import polars as pl

# Text data with structured patterns
df = pl.DataFrame({
    "log_entry": [
        "2024-01-15 10:23:45 ERROR user_id=123 msg=Login failed",
        "2024-01-15 10:24:01 INFO user_id=456 msg=Login success",
        "2024-01-15 10:25:12 WARN user_id=789 msg=Rate limit exceeded",
        "2024-01-15 10:26:33 ERROR user_id=101 msg=DB connection timeout",
        "2024-01-15 10:27:55 INFO user_id=202 msg=Profile updated",
    ]
})

# Extract structured data from log entries
result = df.with_columns([
    # Extract date and time
    pl.col("log_entry").str.extract(r"(\\d{4}-\\d{2}-\\d{2})", 1).alias("date"),
    pl.col("log_entry").str.extract(r"(\\d{2}:\\d{2}:\\d{2})", 1).alias("time"),
    # Extract log level
    pl.col("log_entry").str.extract(r"(ERROR|WARN|INFO|DEBUG)", 1).alias("level"),
    # Extract user_id
    pl.col("log_entry").str.extract(r"user_id=(\\d+)", 1).cast(pl.Int32).alias("user_id"),
    # Extract message
    pl.col("log_entry").str.extract(r"msg=(.+)$", 1).alias("message"),
])
print("Extracted log fields:")
print(result.drop("log_entry"))

# Count pattern matches
df2 = pl.DataFrame({
    "text": ["apple pie and apple juice", "banana split", "apple apple apple", "cherry"]
})
df2 = df2.with_columns(
    pl.col("text").str.count_matches("apple").alias("apple_count")
)
print("\\nPattern count:")
print(df2)
""".strip(),
    c3t="String Splitting & Parsing",
    c3="""
import polars as pl

df = pl.DataFrame({
    "csv_row": ["Alice,30,Engineer,New York",
                "Bob,25,Designer,Los Angeles",
                "Charlie,35,Manager,Chicago"],
    "tags": ["python|pandas|polars", "javascript|react|node", "python|sklearn|pytorch"],
    "path": ["/home/user/data/2024/jan/sales.csv",
             "/home/user/data/2024/feb/orders.parquet",
             "/home/user/data/2024/mar/logs.json"],
})

# Split CSV string into columns
parsed = (df
    .with_columns(pl.col("csv_row").str.split(",").alias("parts"))
    .with_columns([
        pl.col("parts").list.get(0).alias("name"),
        pl.col("parts").list.get(1).cast(pl.Int32).alias("age"),
        pl.col("parts").list.get(2).alias("role"),
        pl.col("parts").list.get(3).alias("city"),
    ])
    .drop(["parts", "csv_row"])
)
print("Parsed CSV columns:")
print(parsed)

# Tags: split and explode
tags_exploded = (df
    .with_columns(pl.col("tags").str.split("|"))
    .explode("tags")
    .rename({"tags": "tag"})
    .select(["tag"])
    .group_by("tag")
    .agg(pl.len().alias("count"))
    .sort("count", descending=True)
)
print("\\nTag frequency:")
print(tags_exploded)

# Extract filename from path
df_paths = df.with_columns(
    pl.col("path").str.split("/").list.last().alias("filename")
)
print("\\nFilenames:", df_paths["filename"].to_list())
""".strip(),
    rw_scenario="Your data team receives 100K free-text product descriptions. Extract brand names, model numbers, prices, and categories using regex. Build a structured product catalog from raw text.",
    rw_code="""
import polars as pl
import numpy as np

np.random.seed(42)

# Raw product descriptions
descriptions = [
    "Apple iPhone 15 Pro 256GB - Price: $999.99 | Category: Smartphones",
    "Samsung Galaxy S24 Ultra 512GB for $1199 in Electronics category",
    "Sony WH-1000XM5 Headphones - Electronics - USD 349.99",
    "Nike Air Max 2024 Running Shoes - Sports - Price $129.95",
    "Bosch Professional Drill Set - Tools - $89.99 - Model: GSR18V",
    "Canon EOS R50 Camera Body - Photography - Price: $679.00",
]

df = pl.DataFrame({"raw": descriptions * 100})  # simulate 600 products

result = df.with_columns([
    # Extract brand (first word, capitalized)
    pl.col("raw").str.extract(r"^([A-Z][a-zA-Z]+)", 1).alias("brand"),
    # Extract price
    pl.col("raw").str.extract(r"\\$([\\d,]+\\.\\d{2})", 1)
      .str.replace(",", "").cast(pl.Float64).alias("price"),
    # Extract category
    pl.col("raw").str.extract(
        r"(Smartphones|Electronics|Sports|Tools|Photography|Clothing)", 1
    ).alias("category"),
])

print("Extracted product data:")
print(result.drop("raw").head(6))
print("\\nPrice statistics by category:")
print(result.group_by("category").agg([
    pl.col("price").mean().round(2).alias("avg_price"),
    pl.col("price").min().alias("min_price"),
    pl.col("price").max().alias("max_price"),
    pl.len().alias("count"),
]).sort("avg_price", descending=True))
""".strip(),
    pt="String Extraction Pipeline",
    pd_text="Given a column of log lines, extract timestamp, severity level, and message into separate columns using .str.extract() with capture groups.",
    ps="""
import polars as pl

logs = pl.DataFrame({"line": [
    "2024-01-15 ERROR Something went wrong",
    "2024-01-16 INFO Process completed",
    "2024-01-17 WARN Memory usage high",
]})
# 1. Extract date with r"(\\d{4}-\\d{2}-\\d{2})"
# 2. Extract level with r"(ERROR|WARN|INFO)"
# 3. Extract message (everything after level)
# 4. Print result without original column
""".strip()
)

# ── Section 21: Date/Time Processing ─────────────────────────────────────────
s21 = make_section(21, "Date/Time Processing",
    "Polars .dt namespace provides fast datetime operations: extraction, arithmetic, truncation, and timezone handling. All operations are vectorized and work on Series natively.",
    c1t="Date Extraction & Arithmetic",
    c1="""
import polars as pl
import numpy as np
from datetime import date, timedelta

# Create datetime data
np.random.seed(42)
n = 200
start = date(2024, 1, 1)
dates = [start + timedelta(days=int(d)) for d in np.random.randint(0, 365, n)]

df = pl.DataFrame({
    "event_date": pl.Series(dates),
    "sales": np.random.exponential(100, n).round(2),
    "returns": np.random.randint(0, 5, n),
})

# Date component extraction
df_with_parts = df.with_columns([
    pl.col("event_date").dt.year().alias("year"),
    pl.col("event_date").dt.month().alias("month"),
    pl.col("event_date").dt.day().alias("day"),
    pl.col("event_date").dt.weekday().alias("weekday"),  # 0=Monday
    pl.col("event_date").dt.week().alias("week_num"),
    pl.col("event_date").dt.quarter().alias("quarter"),
])
print("Date components:")
print(df_with_parts.head(3))

# Date arithmetic
df_with_calc = df.with_columns([
    (pl.col("event_date") + pl.duration(days=30)).alias("due_date"),
    (pl.lit(date(2024, 12, 31)) - pl.col("event_date")).dt.total_days().alias("days_until_eoy"),
])
print("\\nDate arithmetic:")
print(df_with_calc.select(["event_date", "due_date", "days_until_eoy"]).head(3))

# Groupby month
monthly = df.group_by(pl.col("event_date").dt.month().alias("month")).agg(
    pl.col("sales").sum().round(2).alias("total_sales"),
    pl.len().alias("n_transactions")
).sort("month")
print("\\nMonthly summary:")
print(monthly)
""".strip(),
    c2t="Time Series Resampling & Windows",
    c2="""
import polars as pl
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n = 1000

# Minute-level timestamp data
start = datetime(2024, 1, 1, 0, 0, 0)
timestamps = [start + timedelta(minutes=i*5 + np.random.randint(0, 5)) for i in range(n)]

df = pl.DataFrame({
    "ts": pl.Series(timestamps).cast(pl.Datetime),
    "temp": 20 + np.cumsum(np.random.randn(n) * 0.5),
    "pressure": 1013 + np.cumsum(np.random.randn(n) * 0.2),
})

# Truncate to hourly resolution
df_hourly = df.with_columns(
    pl.col("ts").dt.truncate("1h").alias("hour")
).group_by("hour").agg([
    pl.col("temp").mean().round(2).alias("avg_temp"),
    pl.col("temp").min().alias("min_temp"),
    pl.col("temp").max().alias("max_temp"),
    pl.col("pressure").mean().round(2).alias("avg_pressure"),
    pl.len().alias("n_readings"),
]).sort("hour")

print("Hourly resampled data (first 5 hours):")
print(df_hourly.head(5))

# Daily summary
df_daily = df.with_columns(
    pl.col("ts").dt.date().alias("date")
).group_by("date").agg([
    pl.col("temp").mean().round(2).alias("daily_avg_temp"),
    pl.col("temp").std().round(3).alias("temp_std"),
]).sort("date")
print("\\nDaily summary (first 3 days):")
print(df_daily.head(3))
""".strip(),
    c3t="Timezone Handling & Duration",
    c3="""
import polars as pl
from datetime import datetime, timezone, timedelta

# Timezone-aware datetime operations
timestamps_utc = pl.Series([
    datetime(2024, 3, 15, 12, 0, 0),
    datetime(2024, 6, 15, 18, 30, 0),
    datetime(2024, 12, 1, 8, 45, 0),
]).cast(pl.Datetime).dt.replace_time_zone("UTC")

df = pl.DataFrame({
    "event_utc": timestamps_utc,
    "duration_sec": pl.Series([3600, 7200, 1800]),  # seconds
})

# Convert to different timezones
df_tz = df.with_columns([
    pl.col("event_utc").dt.convert_time_zone("America/New_York").alias("event_eastern"),
    pl.col("event_utc").dt.convert_time_zone("Europe/London").alias("event_london"),
    pl.col("event_utc").dt.convert_time_zone("Asia/Tokyo").alias("event_tokyo"),
])
print("Multi-timezone timestamps:")
print(df_tz.select(["event_utc", "event_eastern", "event_tokyo"]))

# Duration calculations
df_duration = df.with_columns([
    pl.duration(seconds=pl.col("duration_sec")).alias("duration"),
    (pl.col("event_utc") + pl.duration(hours=2)).alias("event_plus_2h"),
])
print("\\nDuration operations:")
print(df_duration.select(["event_utc", "duration", "event_plus_2h"]))

# Business day calculation (using weekday filter)
n_workdays = (pl.date_range(pl.date(2024, 1, 1), pl.date(2024, 1, 31), "1d", eager=True)
    .filter(pl.Series([d.weekday() < 5 for d in pl.date_range(
        pl.date(2024, 1, 1), pl.date(2024, 1, 31), "1d", eager=True).to_list()]))
    .len())
print(f"\\nWorkdays in January 2024: {n_workdays}")
""".strip(),
    rw_scenario="Process IoT sensor data with minute-level timestamps. Resample to hourly averages, detect anomalies (values >3 std from hourly mean), and compute time between consecutive anomalies.",
    rw_code="""
import polars as pl
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n = 2000
start = datetime(2024, 1, 1)
ts = [start + timedelta(minutes=i) for i in range(n)]

df = pl.DataFrame({
    "timestamp": pl.Series(ts).cast(pl.Datetime),
    "temperature": 25 + np.cumsum(np.random.randn(n)*0.3),
    "humidity": 60 + np.cumsum(np.random.randn(n)*0.2),
    "sensor_id": np.random.choice(["S1","S2","S3"], n),
})

# Add some anomalies
anomaly_idx = np.random.choice(n, 20, replace=False)
df = df.with_row_index().with_columns([
    pl.when(pl.col("index").is_in(anomaly_idx.tolist()))
      .then(pl.col("temperature") + 15)
      .otherwise(pl.col("temperature"))
      .alias("temperature")
]).drop("index")

# Hourly statistics
hourly = (df.with_columns(pl.col("timestamp").dt.truncate("1h").alias("hour"))
    .group_by(["hour", "sensor_id"])
    .agg([
        pl.col("temperature").mean().round(2).alias("avg_temp"),
        pl.col("temperature").std().round(3).alias("std_temp"),
        pl.col("humidity").mean().round(2).alias("avg_humidity"),
        pl.len().alias("n_readings"),
    ])
    .sort(["hour", "sensor_id"])
)
print("Hourly sensor statistics (first 6 rows):")
print(hourly.head(6))
""".strip(),
    pt="DateTime Resampling",
    pd_text="Create a DataFrame with minute-level timestamps, resample to daily averages using dt.date() and group_by, then extract year/month/weekday as new columns.",
    ps="""
import polars as pl
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n = 500
ts = [datetime(2024,1,1) + timedelta(minutes=i*10) for i in range(n)]
df = pl.DataFrame({
    "ts": pl.Series(ts).cast(pl.Datetime),
    "value": np.random.randn(n) * 10 + 50,
})
# 1. Extract day: pl.col("ts").dt.date()
# 2. Group by day, compute mean/min/max
# 3. Add year, month, weekday columns
""".strip()
)

# ── Section 22: Window Functions & Expressions ────────────────────────────────
s22 = make_section(22, "Window Functions & Expressions",
    "Polars window functions apply expressions over groups without collapsing rows. They enable rankings, cumulative sums, lag/lead features, and partition-based calculations in a single pass.",
    c1t="Ranking & Cumulative Window Functions",
    c1="""
import polars as pl
import numpy as np

np.random.seed(42)
df = pl.DataFrame({
    "date": pl.date_range(pl.date(2024, 1, 1), period="30d", interval="1d", eager=True),
    "product": np.tile(["A", "B", "C"], 10),
    "region": np.random.choice(["East", "West"], 30),
    "sales": np.random.exponential(100, 30).round(2),
})

# Ranking within groups (dense_rank)
df_ranked = df.with_columns([
    pl.col("sales").rank("dense", descending=True).over("product").alias("rank_in_product"),
    pl.col("sales").rank("ordinal", descending=True).over("region").alias("rank_in_region"),
])
print("Rankings:")
print(df_ranked.select(["product", "region", "sales", "rank_in_product", "rank_in_region"]).head(6))

# Cumulative sum and running stats
df_cumulative = df.sort("date").with_columns([
    pl.col("sales").cum_sum().over("product").alias("cumsum_by_product"),
    pl.col("sales").cum_mean().over("product").alias("cum_mean_by_product"),
])
print("\\nCumulative stats by product:")
print(df_cumulative.select(["date", "product", "sales",
                             "cumsum_by_product", "cum_mean_by_product"]).head(6))

# Group-level stats without collapsing
df_group_stats = df.with_columns([
    pl.col("sales").mean().over("product").alias("product_avg"),
    pl.col("sales").sum().over("region").alias("region_total"),
    (pl.col("sales") / pl.col("sales").sum().over("product")).alias("pct_of_product"),
])
print("\\nGroup stats (no collapse):")
print(df_group_stats.head(6))
""".strip(),
    c2t="Lag, Lead & Shift Features",
    c2="""
import polars as pl
import numpy as np

np.random.seed(42)
n = 60
df = pl.DataFrame({
    "date": pl.date_range(pl.date(2024, 1, 1), period=f"{n}d", interval="1d", eager=True),
    "product": ["A"]*(n//2) + ["B"]*(n//2),
    "sales": np.random.exponential(100, n).round(2),
})

# Sort before lag/lead
df = df.sort(["product", "date"])

# Lag/lead features for time series
df_features = df.with_columns([
    pl.col("sales").shift(1).over("product").alias("lag_1"),
    pl.col("sales").shift(7).over("product").alias("lag_7"),
    pl.col("sales").shift(-1).over("product").alias("lead_1"),
    # Difference from previous period
    (pl.col("sales") - pl.col("sales").shift(1).over("product")).alias("delta"),
    # Percent change
    ((pl.col("sales") - pl.col("sales").shift(1).over("product")) /
     pl.col("sales").shift(1).over("product")).round(4).alias("pct_change"),
    # Rolling mean (window function style)
    pl.col("sales").rolling_mean(window_size=7).over("product").alias("rolling_7"),
])

print("Lag/lead features:")
print(df_features.filter(pl.col("product")=="A").head(8))
""".strip(),
    c3t="Conditional Expressions & When/Then/Otherwise",
    c3="""
import polars as pl
import numpy as np

np.random.seed(42)
n = 500
df = pl.DataFrame({
    "customer_id": range(n),
    "age": np.random.randint(18, 75, n),
    "income": np.random.exponential(50000, n).round(0),
    "credit_score": np.random.randint(300, 850, n),
    "loan_amount": np.random.exponential(15000, n).round(0),
    "on_time_payments": np.random.randint(0, 60, n),
    "total_payments": np.random.randint(12, 60, n),
})

# Complex conditional expressions
df_scored = df.with_columns([
    # Age category
    pl.when(pl.col("age") < 25).then(pl.lit("Young"))
      .when(pl.col("age") < 45).then(pl.lit("Middle"))
      .otherwise(pl.lit("Senior")).alias("age_group"),

    # Credit tier
    pl.when(pl.col("credit_score") >= 750).then(pl.lit("Excellent"))
      .when(pl.col("credit_score") >= 650).then(pl.lit("Good"))
      .when(pl.col("credit_score") >= 550).then(pl.lit("Fair"))
      .otherwise(pl.lit("Poor")).alias("credit_tier"),

    # Payment ratio
    (pl.col("on_time_payments") / pl.col("total_payments")).round(3).alias("payment_ratio"),

    # Approval decision
    pl.when(
        (pl.col("credit_score") >= 650) &
        (pl.col("income") >= 30000) &
        (pl.col("loan_amount") <= pl.col("income") * 5)
    ).then(pl.lit("Approved")).otherwise(pl.lit("Denied")).alias("decision"),
])

print("Loan applications with features:")
print(df_scored.head(8))

# Summary by tier
print("\\nApproval by credit tier:")
print(df_scored.group_by("credit_tier").agg([
    pl.len().alias("n"),
    (pl.col("decision")=="Approved").mean().round(3).alias("approval_rate"),
]).sort("credit_tier"))
""".strip(),
    rw_scenario="Build ML features for a churn prediction model: compute 30/60/90-day rolling purchase counts, days since last purchase, rank within customer segment, and pct change in spending.",
    rw_code="""
import polars as pl
import numpy as np
from datetime import date, timedelta

np.random.seed(42)
n = 5000
customers = 500

purchase_dates = [date(2024,1,1) + timedelta(days=int(d))
                  for d in np.random.randint(0, 180, n)]

df = pl.DataFrame({
    "purchase_date": pl.Series(purchase_dates),
    "customer_id": np.random.randint(0, customers, n),
    "amount": np.random.exponential(60, n).round(2),
    "category": np.random.choice(["A","B","C"], n),
})

df = df.sort(["customer_id", "purchase_date"])

# Feature engineering with window functions
features = df.with_columns([
    # Cumulative spend per customer
    pl.col("amount").cum_sum().over("customer_id").alias("cumulative_spend"),

    # Rank by amount within customer
    pl.col("amount").rank("ordinal", descending=True).over("customer_id").alias("amount_rank"),

    # Rolling 30-day purchase count (using row-based rolling as proxy)
    pl.col("amount").rolling_mean(window_size=5).over("customer_id").alias("rolling_mean_5"),

    # Delta from previous purchase
    (pl.col("amount") - pl.col("amount").shift(1).over("customer_id")).alias("amount_delta"),
])

print("Feature matrix (first 10 rows):")
print(features.head(10))

# Customer-level summary
summary = features.group_by("customer_id").agg([
    pl.col("cumulative_spend").last().round(2).alias("total_spend"),
    pl.len().alias("n_purchases"),
    pl.col("purchase_date").max().alias("last_purchase"),
    pl.col("amount").std().round(2).alias("spend_volatility"),
]).sort("total_spend", descending=True)
print("\\nCustomer summary (top 5):")
print(summary.head(5))
""".strip(),
    pt="Window Functions",
    pd_text="Apply rank, cumulative sum, and lag-1 window functions over a group column. Verify the results have the same row count as the original DataFrame.",
    ps="""
import polars as pl
import numpy as np

np.random.seed(42)
df = pl.DataFrame({
    "group": np.random.choice(["A","B"], 20),
    "value": np.random.randn(20).round(2),
    "date": pl.date_range(pl.date(2024,1,1), period="20d", interval="1d", eager=True),
})
# 1. .sort(["group", "date"])
# 2. Add rank column: pl.col("value").rank("dense", descending=True).over("group")
# 3. Add cumsum: pl.col("value").cum_sum().over("group")
# 4. Add lag1: pl.col("value").shift(1).over("group")
# 5. Assert len(result) == len(df)
""".strip()
)

# ── Section 23: Performance & Polars vs Pandas ────────────────────────────────
s23 = make_section(23, "Performance: Polars vs Pandas",
    "Polars consistently outperforms pandas 5-100x due to Rust implementation, SIMD operations, parallel query execution, and memory-efficient Apache Arrow format.",
    c1t="Benchmark: GroupBy & Aggregation",
    c1="""
import polars as pl
import pandas as pd
import numpy as np
import time

np.random.seed(42)
n = 500_000

# Create test data
data = {
    "id": range(n),
    "category": np.random.choice(list("ABCDEFGHIJ"), n),
    "sub_cat": np.random.choice(list("XYZ"), n),
    "value1": np.random.randn(n) * 100,
    "value2": np.random.exponential(50, n),
    "count": np.random.randint(1, 100, n),
}

df_pd = pd.DataFrame(data)
df_pl = pl.DataFrame(data)

# Benchmark: complex groupby + aggregation
def pandas_groupby():
    return (df_pd
        .groupby(["category", "sub_cat"])
        .agg({"value1": ["mean", "std", "sum"], "value2": ["mean", "max"], "count": "sum"})
    )

def polars_groupby():
    return (df_pl.lazy()
        .group_by(["category", "sub_cat"])
        .agg([
            pl.col("value1").mean().alias("v1_mean"),
            pl.col("value1").std().alias("v1_std"),
            pl.col("value1").sum().alias("v1_sum"),
            pl.col("value2").mean().alias("v2_mean"),
            pl.col("value2").max().alias("v2_max"),
            pl.col("count").sum().alias("count_sum"),
        ])
        .collect()
    )

# Time both
for name, fn in [("Pandas", pandas_groupby), ("Polars", polars_groupby)]:
    times = []
    for _ in range(3):
        t0 = time.time()
        result = fn()
        times.append((time.time()-t0)*1000)
    print(f"{name}: avg={sum(times)/len(times):.1f}ms, min={min(times):.1f}ms")
""".strip(),
    c2t="Filter & Join Benchmark",
    c2="""
import polars as pl
import pandas as pd
import numpy as np
import time

np.random.seed(42)
n_main = 200_000
n_ref = 1_000

main_data = {
    "user_id": np.random.randint(0, n_ref, n_main),
    "product": np.random.choice(list("ABCDE"), n_main),
    "amount": np.random.exponential(50, n_main),
    "date": np.random.randint(0, 365, n_main),
}
ref_data = {
    "user_id": range(n_ref),
    "tier": np.random.choice(["Gold", "Silver", "Bronze"], n_ref),
    "discount": np.random.uniform(0, 0.3, n_ref).round(3),
}

df_pd_main = pd.DataFrame(main_data)
df_pd_ref = pd.DataFrame(ref_data)
df_pl_main = pl.DataFrame(main_data)
df_pl_ref = pl.DataFrame(ref_data)

def pandas_join_filter():
    merged = df_pd_main.merge(df_pd_ref, on="user_id", how="left")
    filtered = merged[(merged["tier"]=="Gold") & (merged["amount"] > 50)]
    return filtered.groupby("product")["amount"].agg(["sum","mean","count"])

def polars_join_filter():
    return (df_pl_main.lazy()
        .join(df_pl_ref.lazy(), on="user_id", how="left")
        .filter((pl.col("tier")=="Gold") & (pl.col("amount") > 50))
        .group_by("product")
        .agg([pl.col("amount").sum(), pl.col("amount").mean(), pl.len()])
        .collect())

for name, fn in [("Pandas", pandas_join_filter), ("Polars", polars_join_filter)]:
    t0 = time.time()
    result = fn()
    t1 = time.time()
    print(f"{name}: {(t1-t0)*1000:.1f}ms, rows={len(result)}")

print("\\nSpeedups are typically 5-50x for large datasets on multi-core machines.")
""".strip(),
    c3t="Memory Efficiency & Migration Tips",
    c3="""
import polars as pl
import pandas as pd
import numpy as np
import sys

np.random.seed(42)
n = 100_000

# Memory usage comparison
data = {
    "id": range(n),
    "name": [f"item_{i}" for i in range(n)],
    "value": np.random.randn(n),
    "category": np.random.choice(["A","B","C","D","E"], n),
    "flag": np.random.choice([True, False], n),
}

df_pd = pd.DataFrame(data)
df_pl = pl.DataFrame(data)

pd_memory = df_pd.memory_usage(deep=True).sum() / 1024**2
# Polars uses Arrow format - typically more efficient
print(f"Pandas memory: {pd_memory:.2f} MB")
print(f"Polars dtypes: {dict(zip(df_pl.columns, df_pl.dtypes))}")

# Pandas -> Polars migration cheatsheet
print("\\nPandas -> Polars Migration:")
migrations = [
    ("df.groupby('col').mean()", "df.group_by('col').agg(pl.all().mean())"),
    ("df[df['x'] > 0]",          "df.filter(pl.col('x') > 0)"),
    ("df['col'].apply(fn)",       "df.with_columns(pl.col('col').map_elements(fn))"),
    ("pd.merge(df1, df2, on='k')","df1.join(df2, on='k', how='inner')"),
    ("df.rename({'a':'b'},...)",  "df.rename({'a': 'b'})"),
    ("df.drop('col', axis=1)",   "df.drop('col')"),
    ("df.sort_values('col')",    "df.sort('col')"),
    ("df.head(10)",              "df.head(10)"),
]
for pandas_code, polars_code in migrations:
    print(f"  Pandas: {pandas_code}")
    print(f"  Polars: {polars_code}\\n")
""".strip(),
    rw_scenario="Migrate a pandas ETL pipeline to Polars. The pipeline reads a 5GB CSV, filters bad records, joins with a reference table, and computes aggregations. Measure speedup.",
    rw_code="""
import polars as pl
import pandas as pd
import numpy as np
import time, tempfile, os

np.random.seed(42)
n = 200_000

# Simulate writing a CSV (in-memory for demo)
data = {
    "transaction_id": range(n),
    "customer_id": np.random.randint(0, 10000, n),
    "product_id": np.random.randint(0, 500, n),
    "amount": np.random.exponential(80, n).round(2),
    "status": np.random.choice(["completed","pending","failed","cancelled"], n),
    "date": np.random.randint(0, 365, n),
}
with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
    csv_path = f.name
    import csv as csv_lib
    writer = csv_lib.DictWriter(f, fieldnames=data.keys())
    writer.writeheader()
    for i in range(n):
        writer.writerow({k: data[k][i] for k in data})

# Pandas pipeline
t0 = time.time()
df_pd = pd.read_csv(csv_path)
df_pd = df_pd[df_pd["status"] == "completed"]
result_pd = df_pd.groupby("product_id")["amount"].agg(["sum","mean","count"])
pd_time = (time.time()-t0)*1000

# Polars pipeline
t0 = time.time()
result_pl = (
    pl.scan_csv(csv_path)
    .filter(pl.col("status") == "completed")
    .group_by("product_id")
    .agg([pl.col("amount").sum(), pl.col("amount").mean(), pl.len()])
    .collect()
)
pl_time = (time.time()-t0)*1000

os.unlink(csv_path)
print(f"Pandas: {pd_time:.0f}ms ({len(result_pd)} rows)")
print(f"Polars: {pl_time:.0f}ms ({len(result_pl)} rows)")
print(f"Speedup: {pd_time/pl_time:.1f}x")
""".strip(),
    pt="Pandas to Polars Migration",
    pd_text="Convert a pandas pipeline (filter, groupby, merge) to Polars. Verify the results are equivalent and measure the speedup.",
    ps="""
import polars as pl
import pandas as pd
import numpy as np, time

np.random.seed(42)
n = 50_000
data = {"group": np.random.choice(list("ABCD"), n),
        "value": np.random.randn(n), "flag": np.random.choice([True, False], n)}
df_pd = pd.DataFrame(data)
df_pl = pl.DataFrame(data)

# Pandas version (given):
# result = df_pd[df_pd["flag"]].groupby("group")["value"].agg(["sum","mean","std"])

# TODO: Write the equivalent Polars version using .filter() and .group_by()
# Time both and print speedup
""".strip()
)

# ── Section 24: Polars Integration & Production Patterns ──────────────────────
s24 = make_section(24, "Polars Production Patterns",
    "Production Polars patterns include reading/writing Parquet, Arrow IPC, and cloud storage, integrating with ML pipelines, and building robust ETL pipelines with error handling.",
    c1t="Reading & Writing Parquet/Arrow",
    c1="""
import polars as pl
import numpy as np
import tempfile, os, time

np.random.seed(42)
n = 100_000

df = pl.DataFrame({
    "id": range(n),
    "category": np.random.choice(list("ABCDE"), n),
    "value": np.random.randn(n).round(4),
    "date": pl.date_range(pl.date(2024,1,1), period=f"{n}d", interval="1d", eager=True)[:n],
    "active": np.random.choice([True, False], n),
})

with tempfile.TemporaryDirectory() as tmpdir:
    # Write formats
    csv_path = os.path.join(tmpdir, "data.csv")
    parquet_path = os.path.join(tmpdir, "data.parquet")
    ipc_path = os.path.join(tmpdir, "data.arrow")

    df.write_csv(csv_path)
    df.write_parquet(parquet_path)
    df.write_ipc(ipc_path)

    sizes = {
        "CSV": os.path.getsize(csv_path),
        "Parquet": os.path.getsize(parquet_path),
        "Arrow IPC": os.path.getsize(ipc_path),
    }
    print("File sizes:")
    for fmt, size in sizes.items():
        print(f"  {fmt}: {size/1024:.1f} KB ({size/sizes['CSV']*100:.0f}% of CSV)")

    # Read speeds
    for fmt, read_fn, path in [
        ("CSV",     lambda: pl.read_csv(csv_path), csv_path),
        ("Parquet", lambda: pl.read_parquet(parquet_path), parquet_path),
        ("Arrow",   lambda: pl.read_ipc(ipc_path), ipc_path),
    ]:
        t0 = time.time()
        result = read_fn()
        t_ms = (time.time()-t0)*1000
        print(f"  {fmt} read: {t_ms:.1f}ms, shape={result.shape}")

print("\\nRecommendation: Use Parquet for storage (5-10x smaller + faster reads)")
""".strip(),
    c2t="Polars in ML Pipelines",
    c2="""
import polars as pl
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

np.random.seed(42)
n = 2000

# Create Polars DataFrame
df = pl.DataFrame({
    "age": np.random.randint(18, 70, n),
    "income": np.random.exponential(50000, n).round(0),
    "credit_score": np.random.randint(300, 850, n),
    "debt_ratio": np.random.uniform(0, 1, n).round(3),
    "employment_years": np.random.randint(0, 40, n),
    "category": np.random.choice(["A","B","C"], n),
})

# Feature engineering in Polars
df_features = df.with_columns([
    (pl.col("income") / (pl.col("age") + 1)).alias("income_per_age"),
    (pl.col("credit_score") / 850).alias("credit_norm"),
    pl.col("category").cast(pl.Categorical).cast(pl.Int8).alias("category_code"),
]).drop("category")

# Target
target = (df["credit_score"] > 650).cast(pl.Int32)

# Convert to numpy for sklearn
X = df_features.to_numpy()
y = target.to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_sc, y_train)
print(classification_report(y_test, model.predict(X_test_sc)))

# Feature importance back to Polars
importances = pl.DataFrame({
    "feature": df_features.columns,
    "importance": model.feature_importances_,
}).sort("importance", descending=True)
print("Feature importances:")
print(importances)
""".strip(),
    c3t="ETL Pipeline with Error Handling",
    c3="""
import polars as pl
import numpy as np
import tempfile, os

np.random.seed(42)
n = 1000

# Simulate messy input data
data_rows = []
for i in range(n):
    row = f"{i},{np.random.choice(['A','B','C'])},"
    val = np.random.randn()
    if np.random.random() < 0.05: row += "NULL"  # missing value
    elif np.random.random() < 0.02: row += "N/A"  # invalid
    else: row += f"{val:.4f}"
    row += f",{np.random.randint(1, 100)}"
    data_rows.append(row)

with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
    f.write("id,category,value,count\\n")
    f.write("\\n".join(data_rows))
    csv_path = f.name

def run_etl(path):
    df = pl.read_csv(path, null_values=["NULL", "N/A", ""])

    # Validate schema
    n_before = len(df)
    df = df.filter(pl.col("value").is_not_null())
    n_after = len(df)
    print(f"Removed {n_before - n_after} null rows ({(n_before-n_after)/n_before*100:.1f}%)")

    # Type casting and validation
    df = df.with_columns([
        pl.col("value").cast(pl.Float64),
        pl.col("count").cast(pl.Int32),
        pl.col("category").cast(pl.Categorical),
    ])

    # Remove outliers (|z-score| > 3)
    mean_val = df["value"].mean()
    std_val = df["value"].std()
    df = df.filter(((pl.col("value") - mean_val) / std_val).abs() <= 3)

    # Aggregate
    result = df.group_by("category").agg([
        pl.col("value").mean().round(4).alias("avg_value"),
        pl.col("count").sum().alias("total_count"),
        pl.len().alias("n_rows"),
    ]).sort("category")

    return df, result

clean_df, summary = run_etl(csv_path)
print("\\nETL Summary:")
print(summary)
os.unlink(csv_path)
""".strip(),
    rw_scenario="Build a production ETL pipeline: read messy CSV data, validate and clean it, join with reference tables, engineer features, and output to Parquet with data quality metrics.",
    rw_code="""
import polars as pl
import numpy as np
import tempfile, os, json

np.random.seed(42)
n = 5000

# Messy raw data
raw = pl.DataFrame({
    "customer_id": np.random.randint(0, 1000, n),
    "amount": np.where(np.random.random(n) < 0.03, None, np.random.exponential(80, n).round(2)),
    "category": np.random.choice(["Electronics","Clothing","Books",None,"Sports"], n),
    "date_str": [f"2024-{np.random.randint(1,13):02d}-{np.random.randint(1,29):02d}" for _ in range(n)],
    "status": np.random.choice(["COMPLETED","completed","Complete","FAILED","Cancelled"], n),
})

# Reference table
ref = pl.DataFrame({
    "customer_id": range(1000),
    "segment": np.random.choice(["Premium","Standard","Basic"], 1000),
})

def etl_pipeline(df, ref_df):
    metrics = {}
    n_input = len(df)

    # 1. Clean and validate
    df = (df
        .filter(pl.col("amount").is_not_null())
        .filter(pl.col("category").is_not_null())
        .with_columns([
            pl.col("status").str.to_uppercase().alias("status"),
            pl.col("date_str").str.to_date().alias("date"),
            pl.col("amount").clip(0, 10000),
        ])
        .filter(pl.col("status") == "COMPLETED")
    )
    metrics["n_after_clean"] = len(df)
    metrics["pct_kept"] = round(len(df)/n_input*100, 1)

    # 2. Join with reference
    df = df.join(ref_df, on="customer_id", how="left")

    # 3. Feature engineering
    df = df.with_columns([
        pl.col("date").dt.month().alias("month"),
        pl.col("date").dt.quarter().alias("quarter"),
    ])

    # 4. Aggregation
    summary = df.group_by(["segment", "quarter", "category"]).agg([
        pl.col("amount").sum().round(2).alias("total_revenue"),
        pl.len().alias("n_orders"),
        pl.col("amount").mean().round(2).alias("avg_order"),
    ]).sort(["segment", "quarter"])

    return df, summary, metrics

clean_df, summary, metrics = etl_pipeline(raw, ref)
print("ETL Metrics:", json.dumps(metrics, indent=2))
print("\\nRevenue Summary (top 10):")
print(summary.sort("total_revenue", descending=True).head(10))
""".strip(),
    pt="Production ETL Pipeline",
    pd_text="Write a Polars ETL function that reads a DataFrame, removes nulls, normalizes a string column to uppercase, joins with a lookup table, and returns aggregated results.",
    ps="""
import polars as pl
import numpy as np

np.random.seed(42)
raw = pl.DataFrame({
    "id": range(100),
    "group": np.random.choice(["A","B",None,"C"], 100),
    "value": np.where(np.random.random(100)<0.1, None, np.random.randn(100).round(2)),
    "status": np.random.choice(["active","ACTIVE","Inactive"], 100),
})
lookup = pl.DataFrame({"group": ["A","B","C"], "label": ["Alpha","Beta","Gamma"]})

def etl(df, lookup_df):
    # 1. Drop nulls
    # 2. Normalize status to uppercase
    # 3. Join with lookup on "group"
    # 4. Group by label, compute mean+count of value
    pass

print(etl(raw, lookup))
""".strip()
)

# ── Assemble ──────────────────────────────────────────────────────────────────
all_sections = s17 + s18 + s19 + s20 + s21 + s22 + s23 + s24
result = insert_before_make_html(FILE, all_sections)
print("SUCCESS" if result else "FAILED")
