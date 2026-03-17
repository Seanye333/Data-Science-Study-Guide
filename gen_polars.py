import os, json

OUT = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\08_polars"
ACCENT = "#cd8b00"

SECTIONS = [
    {
        "title": "Setup & DataFrame Creation",
        "desc": "Install Polars and create DataFrames from dicts, lists, NumPy arrays, and ranges.",
        "code1_title": "Creating DataFrames",
        "code1": (
            "# pip install polars\n"
            "import polars as pl\n"
            "import numpy as np\n\n"
            "# From dict\n"
            "df = pl.DataFrame({\n"
            "    'name': ['Alice', 'Bob', 'Carol', 'Dave'],\n"
            "    'age': [25, 30, 35, 28],\n"
            "    'score': [92.5, 88.0, 95.1, 76.3],\n"
            "    'active': [True, False, True, True]\n"
            "})\n"
            "print(df)\n\n"
            "# Schema info\n"
            "print(df.schema)\n"
            "print(df.dtypes)\n"
            "print(df.shape)"
        ),
        "code2_title": "Series & Data Types",
        "code2": (
            "import polars as pl\n\n"
            "# Series\n"
            "s = pl.Series('values', [10, 20, 30, 40, 50])\n"
            "print(s)\n"
            "print('dtype:', s.dtype)\n"
            "print('mean:', s.mean())\n\n"
            "# Explicit dtypes\n"
            "df = pl.DataFrame({\n"
            "    'id': pl.Series([1, 2, 3], dtype=pl.Int32),\n"
            "    'price': pl.Series([9.99, 14.99, 4.99], dtype=pl.Float32),\n"
            "    'label': pl.Series(['a', 'b', 'c'], dtype=pl.Categorical),\n"
            "})\n"
            "print(df)\n"
            "print(df.schema)\n\n"
            "# Quick summary\n"
            "df2 = pl.DataFrame({'x': range(100), 'y': [i**2 for i in range(100)]})\n"
            "print(df2.describe())"
        ),
        "rw_scenario": "Data Engineering: Load 10M row transaction records — Polars is 5-10x faster than pandas for initial ingestion.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "# Simulate large transaction dataset\n"
            "np.random.seed(42)\n"
            "n = 500_000\n"
            "df = pl.DataFrame({\n"
            "    'transaction_id': range(n),\n"
            "    'user_id': np.random.randint(1000, 9999, n),\n"
            "    'amount': np.random.exponential(50, n).round(2),\n"
            "    'category': np.random.choice(['food','tech','travel','health'], n),\n"
            "    'status': np.random.choice(['completed','pending','failed'], n, p=[0.8,0.15,0.05])\n"
            "})\n\n"
            "print(f'Loaded {df.shape[0]:,} rows x {df.shape[1]} cols')\n"
            "print(df.schema)\n"
            "print(df.head())"
        ),
        "code3_title": "From CSV String & List of Dicts",
        "code3": (
            "import polars as pl\n"
            "import io\n\n"
            "# From a CSV string (in-memory)\n"
            "csv_data = 'name,age,score\\nAlice,25,92.5\\nBob,30,88.0\\nCarol,35,95.1'\n"
            "df_csv = pl.read_csv(io.StringIO(csv_data))\n"
            "print('From CSV string:')\n"
            "print(df_csv)\n\n"
            "# From list of dicts\n"
            "records = [\n"
            "    {'product': 'Widget', 'price': 9.99, 'qty': 100},\n"
            "    {'product': 'Gadget', 'price': 24.99, 'qty': 50},\n"
            "    {'product': 'Doohickey', 'price': 4.99, 'qty': 200},\n"
            "]\n"
            "df_dicts = pl.DataFrame(records)\n"
            "print('From list of dicts:')\n"
            "print(df_dicts)\n"
            "print('Schema:', df_dicts.schema)"
        ),
        "code4_title": "pl.from_records, pl.from_arrow & Schema Enforcement",
        "code4": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "# pl.from_records — list of tuples with explicit schema\n"
            "records = [(1, 'Alice', 92.5), (2, 'Bob', 88.0), (3, 'Carol', 95.1)]\n"
            "schema = {'id': pl.Int32, 'name': pl.Utf8, 'score': pl.Float32}\n"
            "df_rec = pl.from_records(records, schema=schema)\n"
            "print('from_records:')\n"
            "print(df_rec)\n"
            "print('dtypes:', df_rec.dtypes)\n\n"
            "# pl.from_arrow — zero-copy from PyArrow table\n"
            "try:\n"
            "    import pyarrow as pa\n"
            "    arrow_table = pa.table({'x': [10, 20, 30], 'y': [1.1, 2.2, 3.3]})\n"
            "    df_arrow = pl.from_arrow(arrow_table)\n"
            "    print('from_arrow:', df_arrow)\n"
            "except ImportError:\n"
            "    print('pyarrow not installed — skipping from_arrow demo')\n\n"
            "# Schema enforcement with dtypes dict\n"
            "np.random.seed(42)\n"
            "df_typed = pl.DataFrame(\n"
            "    {\n"
            "        'user_id': np.random.randint(1, 1000, 5).tolist(),\n"
            "        'amount': np.random.uniform(10, 500, 5).tolist(),\n"
            "        'category': ['food', 'tech', 'food', 'travel', 'tech'],\n"
            "    },\n"
            "    schema={'user_id': pl.Int32, 'amount': pl.Float64, 'category': pl.Categorical}\n"
            ")\n"
            "print('Schema-enforced DataFrame:')\n"
            "print(df_typed)\n"
            "print('Schema:', df_typed.schema)"
        ),
        "practice": {
            "title": "DataFrame Construction",
            "desc": "1) Create a DataFrame from a dict with columns: 'city' (5 cities), 'population' (ints), 'area_km2' (floats). 2) Create the same data from a list of dicts. 3) Parse a CSV string with 3 rows and verify the schema. 4) Add a 'density' column (population / area_km2) and print the result.",
            "starter": (
                "import polars as pl\n"
                "import io\n\n"
                "# 1. From dict\n"
                "# TODO: df = pl.DataFrame({\n"
                "#     'city': [...],\n"
                "#     'population': [...],\n"
                "#     'area_km2': [...]\n"
                "# })\n\n"
                "# 2. From list of dicts\n"
                "# TODO: records = [{'city': ..., 'population': ..., 'area_km2': ...}, ...]\n"
                "# TODO: df2 = pl.DataFrame(records)\n\n"
                "# 3. Parse CSV string\n"
                "csv_str = 'city,pop,area\\nTokyo,13960000,2194.0\\nParis,2161000,105.4\\nLondon,8982000,1572.0'\n"
                "# TODO: df3 = pl.read_csv(io.StringIO(csv_str))\n"
                "# TODO: print('Schema:', df3.schema)\n\n"
                "# 4. Add density column\n"
                "# TODO: df4 = df.with_columns(\n"
                "#     (pl.col('population') / pl.col('area_km2')).round(1).alias('density')\n"
                "# )\n"
                "# TODO: print(df4)"
            ),
        },
    },
    {
        "title": "Select, With Columns & Expressions",
        "desc": "Polars uses an expression API for column operations — composable, lazy-friendly, and fast.",
        "code1_title": "select() and with_columns()",
        "code1": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],\n"
            "    'salary': [60000, 75000, 90000, 55000, 110000],\n"
            "    'dept': ['Eng', 'Sales', 'Eng', 'HR', 'Eng'],\n"
            "    'years': [3, 5, 8, 2, 12]\n"
            "})\n\n"
            "# select: pick & transform columns\n"
            "print(df.select(['name', 'salary']))\n\n"
            "# with_columns: add new columns\n"
            "df2 = df.with_columns([\n"
            "    (pl.col('salary') * 1.1).alias('new_salary'),\n"
            "    (pl.col('salary') / pl.col('years')).alias('salary_per_year'),\n"
            "    pl.col('name').str.to_uppercase().alias('name_upper')\n"
            "])\n"
            "print(df2)"
        ),
        "code2_title": "Expressions: Arithmetic, Aliases & Chaining",
        "code2": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'x': [1, 2, 3, 4, 5],\n"
            "    'y': [10, 20, 30, 40, 50],\n"
            "    'label': ['a', 'b', 'a', 'b', 'a']\n"
            "})\n\n"
            "# Expression chaining\n"
            "result = df.select([\n"
            "    pl.col('x'),\n"
            "    pl.col('y'),\n"
            "    (pl.col('x') + pl.col('y')).alias('sum'),\n"
            "    (pl.col('y') / pl.col('x')).alias('ratio').round(2),\n"
            "    pl.col('x').pow(2).alias('x_squared'),\n"
            "    pl.col('label').is_in(['a']).alias('is_a')\n"
            "])\n"
            "print(result)\n\n"
            "# Horizontal operations\n"
            "df2 = df.with_columns(\n"
            "    pl.max_horizontal('x', 'y').alias('row_max'),\n"
            "    pl.sum_horizontal('x', 'y').alias('row_sum')\n"
            ")\n"
            "print(df2)"
        ),
        "rw_scenario": "E-commerce: Add derived columns — profit margin, discount flag, and revenue per unit — to a product catalog.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "n = 1000\n"
            "products = pl.DataFrame({\n"
            "    'product_id': range(n),\n"
            "    'cost': np.random.uniform(5, 200, n).round(2),\n"
            "    'price': np.random.uniform(10, 400, n).round(2),\n"
            "    'units_sold': np.random.randint(0, 500, n),\n"
            "    'category': np.random.choice(['Electronics','Clothing','Food','Books'], n)\n"
            "})\n\n"
            "enriched = products.with_columns([\n"
            "    ((pl.col('price') - pl.col('cost')) / pl.col('price') * 100)\n"
            "        .round(1).alias('margin_pct'),\n"
            "    (pl.col('price') * pl.col('units_sold')).alias('revenue'),\n"
            "    (pl.col('cost') > pl.col('price') * 0.8).alias('low_margin_flag')\n"
            "])\n\n"
            "print(enriched.filter(pl.col('low_margin_flag')).head(5))\n"
            "print('Low margin products:', enriched['low_margin_flag'].sum())"
        ),
        "code3_title": "pl.when / then / otherwise (Conditional Columns)",
        "code3": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],\n"
            "    'score': [92, 45, 78, 55, 88],\n"
            "    'attempts': [1, 3, 2, 4, 1]\n"
            "})\n\n"
            "# pl.when().then().otherwise() — like np.where but composable\n"
            "result = df.with_columns([\n"
            "    pl.when(pl.col('score') >= 90)\n"
            "      .then(pl.lit('A'))\n"
            "      .when(pl.col('score') >= 70)\n"
            "      .then(pl.lit('B'))\n"
            "      .when(pl.col('score') >= 55)\n"
            "      .then(pl.lit('C'))\n"
            "      .otherwise(pl.lit('F'))\n"
            "      .alias('grade'),\n"
            "    pl.when(pl.col('attempts') == 1)\n"
            "      .then(pl.lit('First try'))\n"
            "      .otherwise(pl.lit('Retried'))\n"
            "      .alias('attempt_label')\n"
            "])\n"
            "print(result)"
        ),
        "code4_title": "pl.struct, pl.concat_list, unnest & pl.col('*') Patterns",
        "code4": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'first': ['Alice', 'Bob', 'Carol'],\n"
            "    'last': ['Smith', 'Jones', 'White'],\n"
            "    'score_a': [85, 90, 78],\n"
            "    'score_b': [92, 88, 95],\n"
            "})\n\n"
            "# pl.struct — pack multiple cols into a struct column\n"
            "df2 = df.with_columns(\n"
            "    pl.struct(['first', 'last']).alias('full_name_struct'),\n"
            "    pl.struct(['score_a', 'score_b']).alias('scores_struct')\n"
            ")\n"
            "print('With struct columns:')\n"
            "print(df2.select(['full_name_struct', 'scores_struct']))\n\n"
            "# unnest — expand a struct back to individual columns\n"
            "df3 = df2.select('scores_struct').unnest('scores_struct')\n"
            "print('Unnested scores:')\n"
            "print(df3)\n\n"
            "# pl.concat_list — combine columns into a list column\n"
            "df4 = df.with_columns(\n"
            "    pl.concat_list(['score_a', 'score_b']).alias('all_scores')\n"
            ")\n"
            "print('concat_list result:')\n"
            "print(df4.select(['first', 'all_scores']))\n\n"
            "# pl.col('*') — select all columns at once\n"
            "df5 = df.select(pl.col('*').exclude(['first', 'last']))\n"
            "print('All numeric cols via col(*).exclude:')\n"
            "print(df5)"
        ),
        "practice": {
            "title": "Chained Expressions & Conditional Columns",
            "desc": "Create a DataFrame with columns: 'employee', 'base_salary', 'bonus_pct', 'years_exp'. 1) Add 'total_comp' = base_salary * (1 + bonus_pct/100). 2) Add 'level' using pl.when: 'Junior' if years_exp < 3, 'Mid' if < 7, 'Senior' otherwise. 3) Use pl.sum_horizontal to sum base_salary and a 10000 raise. 4) Filter to show only Senior employees.",
            "starter": (
                "import polars as pl\n\n"
                "df = pl.DataFrame({\n"
                "    'employee': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],\n"
                "    'base_salary': [55000, 72000, 95000, 48000, 110000],\n"
                "    'bonus_pct': [5.0, 8.0, 12.0, 3.0, 15.0],\n"
                "    'years_exp': [2, 5, 9, 1, 13]\n"
                "})\n\n"
                "# 1. Add total_comp\n"
                "# TODO: df = df.with_columns(\n"
                "#     (pl.col('base_salary') * (1 + pl.col('bonus_pct') / 100))\n"
                "#         .round(2).alias('total_comp')\n"
                "# )\n\n"
                "# 2. Add level with pl.when\n"
                "# TODO: df = df.with_columns(\n"
                "#     pl.when(pl.col('years_exp') < 3).then(pl.lit('Junior'))\n"
                "#       .when(pl.col('years_exp') < 7).then(pl.lit('Mid'))\n"
                "#       .otherwise(pl.lit('Senior'))\n"
                "#       .alias('level')\n"
                "# )\n\n"
                "# 3. Sum base_salary + 10000 raise using pl.sum_horizontal\n"
                "# TODO: df = df.with_columns(\n"
                "#     pl.sum_horizontal('base_salary', pl.lit(10000)).alias('salary_with_raise')\n"
                "# )\n\n"
                "# 4. Filter to Senior only\n"
                "# TODO: seniors = df.filter(pl.col('level') == 'Senior')\n"
                "# TODO: print(seniors)"
            ),
        },
    },
    {
        "title": "Filtering & Sorting",
        "desc": "Filter rows with Boolean expressions and sort by one or multiple columns.",
        "code1_title": "filter() with Boolean Expressions",
        "code1": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank'],\n"
            "    'age': [25, 42, 35, 19, 55, 30],\n"
            "    'city': ['NY', 'LA', 'NY', 'Chicago', 'LA', 'NY'],\n"
            "    'salary': [70000, 95000, 80000, 45000, 120000, 65000]\n"
            "})\n\n"
            "# Single condition\n"
            "print(df.filter(pl.col('age') > 30))\n\n"
            "# Multiple conditions (AND)\n"
            "print(df.filter(\n"
            "    (pl.col('city') == 'NY') & (pl.col('salary') > 65000)\n"
            "))\n\n"
            "# OR condition\n"
            "print(df.filter(\n"
            "    (pl.col('city') == 'LA') | (pl.col('age') < 25)\n"
            "))\n\n"
            "# is_in\n"
            "print(df.filter(pl.col('city').is_in(['NY', 'LA'])))"
        ),
        "code2_title": "sort() and top_k()",
        "code2": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'product': ['A', 'B', 'C', 'D', 'E'],\n"
            "    'sales': [300, 150, 450, 280, 100],\n"
            "    'region': ['East', 'West', 'East', 'West', 'East'],\n"
            "    'profit': [45.0, 30.0, 90.0, 55.0, 10.0]\n"
            "})\n\n"
            "# Sort single column\n"
            "print(df.sort('sales', descending=True))\n\n"
            "# Sort multiple columns\n"
            "print(df.sort(['region', 'sales'], descending=[False, True]))\n\n"
            "# top_k — faster than sort for large data\n"
            "print(df.top_k(3, by='profit'))\n\n"
            "# Null handling in sort\n"
            "df2 = pl.DataFrame({'val': [3, None, 1, None, 2]})\n"
            "print(df2.sort('val', nulls_last=True))"
        ),
        "rw_scenario": "Fraud Detection: Filter transactions over $10,000 AND from high-risk countries, sorted by amount descending.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "n = 100_000\n"
            "txns = pl.DataFrame({\n"
            "    'txn_id': range(n),\n"
            "    'amount': np.random.exponential(500, n).round(2),\n"
            "    'country': np.random.choice(['US','UK','NG','VN','BR','RU'], n,\n"
            "                                p=[0.5,0.2,0.1,0.05,0.1,0.05]),\n"
            "    'card_type': np.random.choice(['credit','debit'], n),\n"
            "    'hour': np.random.randint(0, 24, n)\n"
            "})\n\n"
            "HIGH_RISK = ['NG', 'VN', 'RU']\n\n"
            "suspects = txns.filter(\n"
            "    (pl.col('amount') > 10000) &\n"
            "    (pl.col('country').is_in(HIGH_RISK)) &\n"
            "    (pl.col('hour').is_between(0, 5))  # odd hours\n"
            ").sort('amount', descending=True)\n\n"
            "print(f'Suspicious transactions: {len(suspects):,}')\n"
            "print(suspects.head(10))"
        ),
        "code3_title": "Chained Filtering with is_between & str.contains",
        "code3": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'product': ['Widget Pro', 'Gadget Mini', 'Widget Lite', 'Super Gadget', 'Widget Max'],\n"
            "    'price': [29.99, 9.99, 14.99, 49.99, 39.99],\n"
            "    'rating': [4.5, 3.8, 4.1, 4.9, 4.3],\n"
            "    'in_stock': [True, False, True, True, False]\n"
            "})\n\n"
            "# Chain multiple filter conditions\n"
            "result = df.filter(\n"
            "    pl.col('product').str.contains('Widget') &\n"
            "    pl.col('price').is_between(10.0, 45.0) &\n"
            "    pl.col('in_stock') &\n"
            "    (pl.col('rating') >= 4.0)\n"
            ")\n"
            "print('Filtered:', result)\n\n"
            "# Negate a filter with ~\n"
            "not_widget = df.filter(~pl.col('product').str.contains('Widget'))\n"
            "print('Not Widget:', not_widget)"
        ),
        "code4_title": "is_between, top_k & Multi-Column Sort with nulls_last",
        "code4": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "df = pl.DataFrame({\n"
            "    'name': [f'Item_{i}' for i in range(10)],\n"
            "    'price': [12.5, None, 45.0, 8.99, None, 99.0, 34.5, 22.0, None, 67.0],\n"
            "    'rating': np.round(np.random.uniform(1.0, 5.0, 10), 1).tolist(),\n"
            "    'region': ['East','West','East','North','South','West','East','North','South','West'],\n"
            "})\n\n"
            "# is_between on a column with nulls (nulls excluded automatically)\n"
            "mid_range = df.filter(pl.col('price').is_between(10.0, 60.0))\n"
            "print('Price between 10 and 60:')\n"
            "print(mid_range)\n\n"
            "# top_k — fast partial sort (no need to sort the whole frame)\n"
            "print('Top 3 by rating (top_k):')\n"
            "print(df.top_k(3, by='rating'))\n\n"
            "# Sort by multiple cols with nulls_last=True\n"
            "print('Sort by region asc, price desc (nulls last):')\n"
            "print(df.sort(\n"
            "    ['region', 'price'],\n"
            "    descending=[False, True],\n"
            "    nulls_last=True\n"
            "))"
        ),
        "practice": {
            "title": "Chained Filter & Sort",
            "desc": "Create a DataFrame with 'employee', 'dept', 'salary', 'rating' (1.0-5.0), 'remote' (bool). 1) Filter: Engineering dept AND salary > 70000 AND rating >= 4.0. 2) Filter: NOT remote AND salary is_between 50000 and 90000. 3) Sort by dept ascending then salary descending. 4) Get the top-3 rated remote workers.",
            "starter": (
                "import polars as pl\n"
                "import numpy as np\n\n"
                "np.random.seed(42)\n"
                "n = 20\n"
                "df = pl.DataFrame({\n"
                "    'employee': [f'Emp_{i}' for i in range(n)],\n"
                "    'dept': np.random.choice(['Engineering','Sales','HR','Marketing'], n),\n"
                "    'salary': np.random.randint(45000, 130000, n),\n"
                "    'rating': np.round(np.random.uniform(2.5, 5.0, n), 1),\n"
                "    'remote': np.random.choice([True, False], n)\n"
                "})\n"
                "print(df)\n\n"
                "# 1. Engineering, salary > 70000, rating >= 4.0\n"
                "# TODO: result1 = df.filter(\n"
                "#     (pl.col('dept') == 'Engineering') &\n"
                "#     (pl.col('salary') > 70000) &\n"
                "#     (pl.col('rating') >= 4.0)\n"
                "# )\n"
                "# print('Filter 1:', result1)\n\n"
                "# 2. NOT remote AND salary between 50000 and 90000\n"
                "# TODO: result2 = df.filter(\n"
                "#     ~pl.col('remote') & pl.col('salary').is_between(50000, 90000)\n"
                "# )\n"
                "# print('Filter 2:', result2)\n\n"
                "# 3. Sort dept asc, salary desc\n"
                "# TODO: sorted_df = df.sort(['dept', 'salary'], descending=[False, True])\n"
                "# print('Sorted:', sorted_df)\n\n"
                "# 4. Top-3 rated remote workers\n"
                "# TODO: top_remote = df.filter(pl.col('remote')).top_k(3, by='rating')\n"
                "# print('Top remote:', top_remote)"
            ),
        },
    },
    {
        "title": "GroupBy & Aggregations",
        "desc": "Aggregate data by groups using Polars' expressive and parallel groupby engine.",
        "code1_title": "group_by().agg()",
        "code1": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'dept': ['Eng','Eng','Sales','Sales','HR','HR','Eng'],\n"
            "    'name': ['Alice','Bob','Carol','Dave','Eve','Frank','Grace'],\n"
            "    'salary': [90000, 85000, 70000, 65000, 55000, 58000, 95000],\n"
            "    'years': [5, 3, 7, 2, 8, 4, 6]\n"
            "})\n\n"
            "# Basic aggregation\n"
            "print(df.group_by('dept').agg([\n"
            "    pl.len().alias('headcount'),\n"
            "    pl.col('salary').mean().alias('avg_salary'),\n"
            "    pl.col('salary').max().alias('max_salary'),\n"
            "    pl.col('years').sum().alias('total_years')\n"
            "]))\n\n"
            "# Multiple groups\n"
            "print(df.group_by(['dept']).agg(\n"
            "    pl.col('salary').median().alias('median_salary')\n"
            ").sort('median_salary', descending=True))"
        ),
        "code2_title": "Advanced Aggregations",
        "code2": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "df = pl.DataFrame({\n"
            "    'category': np.random.choice(['A','B','C'], 1000),\n"
            "    'value': np.random.normal(100, 20, 1000),\n"
            "    'qty': np.random.randint(1, 50, 1000)\n"
            "})\n\n"
            "stats = df.group_by('category').agg([\n"
            "    pl.len().alias('count'),\n"
            "    pl.col('value').mean().round(2).alias('mean'),\n"
            "    pl.col('value').std().round(2).alias('std'),\n"
            "    pl.col('value').quantile(0.25).round(2).alias('q25'),\n"
            "    pl.col('value').quantile(0.75).round(2).alias('q75'),\n"
            "    pl.col('qty').sum().alias('total_qty'),\n"
            "    (pl.col('value') * pl.col('qty')).sum().round(2).alias('weighted_sum')\n"
            "]).sort('category')\n"
            "print(stats)"
        ),
        "rw_scenario": "Retail: Compute daily revenue, order count, and average basket size per store for weekly reporting.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n"
            "from datetime import date, timedelta\n\n"
            "np.random.seed(42)\n"
            "n = 50_000\n"
            "start = date(2024, 1, 1)\n"
            "orders = pl.DataFrame({\n"
            "    'order_id': range(n),\n"
            "    'store_id': np.random.choice(['S001','S002','S003','S004'], n),\n"
            "    'order_date': [str(start + timedelta(days=int(d)))\n"
            "                   for d in np.random.randint(0, 90, n)],\n"
            "    'amount': np.random.exponential(80, n).round(2),\n"
            "    'items': np.random.randint(1, 10, n)\n"
            "})\n\n"
            "daily = orders.group_by(['store_id', 'order_date']).agg([\n"
            "    pl.len().alias('order_count'),\n"
            "    pl.col('amount').sum().round(2).alias('revenue'),\n"
            "    pl.col('amount').mean().round(2).alias('avg_basket'),\n"
            "    pl.col('items').mean().round(1).alias('avg_items')\n"
            "]).sort(['store_id', 'order_date'])\n\n"
            "print(f'Daily summaries: {daily.shape}')\n"
            "print(daily.head(8))"
        ),
        "code3_title": "GroupBy with Expressions & Filtering Groups",
        "code3": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(0)\n"
            "df = pl.DataFrame({\n"
            "    'region': np.random.choice(['North','South','East','West'], 200),\n"
            "    'product': np.random.choice(['A','B','C'], 200),\n"
            "    'revenue': np.random.exponential(1000, 200).round(2),\n"
            "    'units': np.random.randint(1, 50, 200)\n"
            "})\n\n"
            "# Multi-column groupby with many aggregations\n"
            "summary = df.group_by(['region', 'product']).agg([\n"
            "    pl.len().alias('count'),\n"
            "    pl.col('revenue').sum().round(2).alias('total_revenue'),\n"
            "    pl.col('revenue').mean().round(2).alias('avg_revenue'),\n"
            "    pl.col('units').sum().alias('total_units'),\n"
            "    (pl.col('revenue').sum() / pl.col('units').sum()).round(2).alias('rev_per_unit')\n"
            "]).sort(['region', 'product'])\n"
            "print(summary)\n\n"
            "# Filter groups: only regions where total revenue > 20000\n"
            "high_rev = df.group_by('region').agg(\n"
            "    pl.col('revenue').sum().alias('total')\n"
            ").filter(pl.col('total') > 20000).sort('total', descending=True)\n"
            "print('High-revenue regions:', high_rev)"
        ),
        "code4_title": "group_by_dynamic for Time-Based Grouping & Rolling Aggregations",
        "code4": (
            "import polars as pl\n"
            "import numpy as np\n"
            "from datetime import datetime, timedelta\n\n"
            "np.random.seed(42)\n"
            "n = 500\n"
            "base = datetime(2024, 1, 1)\n"
            "# Build a time-series DataFrame with a proper Datetime column\n"
            "df = pl.DataFrame({\n"
            "    'ts': [base + timedelta(hours=int(h)) for h in np.random.uniform(0, 24*30, n)],\n"
            "    'sales': np.random.exponential(200, n).round(2),\n"
            "    'units': np.random.randint(1, 20, n),\n"
            "}).sort('ts')\n\n"
            "# group_by_dynamic — aggregate by calendar window (daily buckets)\n"
            "daily = df.group_by_dynamic('ts', every='1d').agg([\n"
            "    pl.col('sales').sum().round(2).alias('daily_revenue'),\n"
            "    pl.col('units').sum().alias('daily_units'),\n"
            "    pl.len().alias('transactions'),\n"
            "])\n"
            "print('Daily aggregation (first 7 days):')\n"
            "print(daily.head(7))\n\n"
            "# Rolling aggregation — 7-day rolling sum over the sorted frame\n"
            "rolling = df.with_columns(\n"
            "    pl.col('sales').rolling_sum(window_size=7, min_periods=1).alias('rolling_7d_sales')\n"
            ")\n"
            "print('Rolling 7-day sales sum (last 5 rows):')\n"
            "print(rolling.select(['ts', 'sales', 'rolling_7d_sales']).tail(5))"
        ),
        "practice": {
            "title": "Multi-Column GroupBy & Multiple Aggregations",
            "desc": "Generate a sales DataFrame with 'salesperson', 'region', 'product', 'amount', 'qty'. 1) Group by region AND product, compute count, total amount, avg amount, total qty. 2) Find the salesperson with the highest total sales per region. 3) Filter to only groups where count >= 5 and avg amount > 500.",
            "starter": (
                "import polars as pl\n"
                "import numpy as np\n\n"
                "np.random.seed(7)\n"
                "n = 150\n"
                "df = pl.DataFrame({\n"
                "    'salesperson': [f'Rep_{i%10}' for i in range(n)],\n"
                "    'region': np.random.choice(['North','South','East','West'], n),\n"
                "    'product': np.random.choice(['Widget','Gadget','Doohickey'], n),\n"
                "    'amount': np.random.exponential(800, n).round(2),\n"
                "    'qty': np.random.randint(1, 20, n)\n"
                "})\n\n"
                "# 1. GroupBy region + product\n"
                "# TODO: summary = df.group_by(['region', 'product']).agg([\n"
                "#     pl.len().alias('count'),\n"
                "#     pl.col('amount').sum().round(2).alias('total_amount'),\n"
                "#     pl.col('amount').mean().round(2).alias('avg_amount'),\n"
                "#     pl.col('qty').sum().alias('total_qty')\n"
                "# ]).sort(['region', 'product'])\n"
                "# print(summary)\n\n"
                "# 2. Top salesperson per region\n"
                "# TODO: top_reps = df.group_by(['region', 'salesperson']).agg(\n"
                "#     pl.col('amount').sum().round(2).alias('total_sales')\n"
                "# ).sort('total_sales', descending=True)\n"
                "# TODO: print(top_reps.group_by('region').first())\n\n"
                "# 3. Filter groups with count >= 5 and avg > 500\n"
                "# TODO: filtered = summary.filter(\n"
                "#     (pl.col('count') >= 5) & (pl.col('avg_amount') > 500)\n"
                "# )\n"
                "# print('Qualifying groups:', filtered)"
            ),
        },
    },
    {
        "title": "Joins",
        "desc": "Combine DataFrames with inner, left, outer, cross, and anti joins — all in parallel.",
        "code1_title": "inner, left & outer joins",
        "code1": (
            "import polars as pl\n\n"
            "customers = pl.DataFrame({\n"
            "    'id': [1, 2, 3, 4, 5],\n"
            "    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve']\n"
            "})\n"
            "orders = pl.DataFrame({\n"
            "    'order_id': [101, 102, 103, 104],\n"
            "    'cust_id': [1, 2, 2, 6],  # 6 has no customer\n"
            "    'amount': [250, 80, 120, 400]\n"
            "})\n\n"
            "# Inner join\n"
            "print('INNER:')\n"
            "print(customers.join(orders, left_on='id', right_on='cust_id', how='inner'))\n\n"
            "# Left join\n"
            "print('LEFT (all customers):')\n"
            "print(customers.join(orders, left_on='id', right_on='cust_id', how='left'))\n\n"
            "# Anti join — customers with NO orders\n"
            "print('ANTI (no orders):')\n"
            "print(customers.join(orders, left_on='id', right_on='cust_id', how='anti'))"
        ),
        "code2_title": "Semi Join & Concat",
        "code2": (
            "import polars as pl\n\n"
            "products = pl.DataFrame({\n"
            "    'sku': ['A', 'B', 'C', 'D', 'E'],\n"
            "    'price': [10.0, 25.0, 15.0, 8.0, 50.0]\n"
            "})\n"
            "sold = pl.DataFrame({'sku': ['A', 'C', 'E']})\n\n"
            "# Semi join — only rows with a match (no extra columns)\n"
            "print('SEMI (sold products):')\n"
            "print(products.join(sold, on='sku', how='semi'))\n\n"
            "# Vertical concat (stack rows)\n"
            "df1 = pl.DataFrame({'a': [1, 2], 'b': ['x', 'y']})\n"
            "df2 = pl.DataFrame({'a': [3, 4], 'b': ['z', 'w']})\n"
            "print('CONCAT vertical:')\n"
            "print(pl.concat([df1, df2]))\n\n"
            "# Horizontal concat (side by side)\n"
            "df3 = pl.DataFrame({'c': [10, 20], 'd': [30, 40]})\n"
            "print('CONCAT horizontal:')\n"
            "print(pl.concat([df1, df3], how='horizontal'))"
        ),
        "rw_scenario": "CRM: Enrich customer records with their most recent order and account tier from separate tables.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "customers = pl.DataFrame({\n"
            "    'cust_id': range(1000),\n"
            "    'name': [f'Customer_{i}' for i in range(1000)],\n"
            "    'signup_year': np.random.randint(2018, 2024, 1000)\n"
            "})\n"
            "tiers = pl.DataFrame({\n"
            "    'cust_id': range(1000),\n"
            "    'tier': np.random.choice(['Bronze','Silver','Gold','Platinum'], 1000)\n"
            "})\n"
            "last_orders = pl.DataFrame({\n"
            "    'cust_id': np.random.choice(range(900), 800, replace=False),  # 100 never ordered\n"
            "    'last_order_amount': np.random.exponential(200, 800).round(2)\n"
            "})\n\n"
            "enriched = (\n"
            "    customers\n"
            "    .join(tiers, on='cust_id', how='left')\n"
            "    .join(last_orders, on='cust_id', how='left')\n"
            ")\n"
            "print(f'Enriched: {enriched.shape}')\n"
            "print(enriched.head(5))\n"
            "print('Never ordered:', enriched['last_order_amount'].is_null().sum())"
        ),
        "code3_title": "Cross Join & Suffix Disambiguation",
        "code3": (
            "import polars as pl\n\n"
            "# Cross join — all combinations\n"
            "sizes = pl.DataFrame({'size': ['S', 'M', 'L', 'XL']})\n"
            "colors = pl.DataFrame({'color': ['Red', 'Blue', 'Green']})\n"
            "variants = sizes.join(colors, how='cross')\n"
            "print(f'Product variants ({len(variants)} rows):')\n"
            "print(variants)\n\n"
            "# Join with overlapping column names — use suffix\n"
            "orders = pl.DataFrame({\n"
            "    'order_id': [1, 2, 3],\n"
            "    'amount': [100, 200, 300],\n"
            "    'status': ['paid', 'pending', 'paid']\n"
            "})\n"
            "returns = pl.DataFrame({\n"
            "    'order_id': [2, 3],\n"
            "    'amount': [200, 150],  # refund amount\n"
            "    'status': ['approved', 'partial']\n"
            "})\n"
            "joined = orders.join(returns, on='order_id', how='left', suffix='_refund')\n"
            "print('With suffix disambiguation:')\n"
            "print(joined)"
        ),
        "code4_title": "Semi Join, join with on=, and Asof Join Concept",
        "code4": (
            "import polars as pl\n\n"
            "# --- Semi join: keep only left rows that have a match ---\n"
            "inventory = pl.DataFrame({\n"
            "    'sku': ['A001', 'B002', 'C003', 'D004', 'E005'],\n"
            "    'stock': [100, 0, 50, 200, 0]\n"
            "})\n"
            "ordered_skus = pl.DataFrame({'sku': ['A001', 'C003', 'E005']})\n\n"
            "in_stock_orders = inventory.join(ordered_skus, on='sku', how='semi')\n"
            "print('Semi join — ordered items in inventory:')\n"
            "print(in_stock_orders)\n\n"
            "# --- join with on= (same column name on both sides) ---\n"
            "employees = pl.DataFrame({\n"
            "    'dept_id': [1, 2, 3, 1],\n"
            "    'name': ['Alice', 'Bob', 'Carol', 'Dave']\n"
            "})\n"
            "departments = pl.DataFrame({\n"
            "    'dept_id': [1, 2, 3],\n"
            "    'dept_name': ['Engineering', 'Sales', 'HR']\n"
            "})\n"
            "joined = employees.join(departments, on='dept_id', how='inner')\n"
            "print('join with on= (shared key name):')\n"
            "print(joined)\n\n"
            "# --- Asof join concept: join on nearest key ---\n"
            "# Match each trade to the most recent quote before it\n"
            "quotes = pl.DataFrame({\n"
            "    'time': [1, 3, 5, 8, 12],\n"
            "    'bid': [100.0, 100.5, 101.0, 101.5, 102.0]\n"
            "})\n"
            "trades = pl.DataFrame({\n"
            "    'time': [2, 4, 9, 11],\n"
            "    'qty': [10, 5, 20, 8]\n"
            "})\n"
            "asof = trades.join_asof(quotes, on='time', strategy='backward')\n"
            "print('Asof join (each trade gets most recent bid):')\n"
            "print(asof)"
        ),
        "practice": {
            "title": "Left Join & Anti-Join",
            "desc": "Create 'students' (id, name, grade) and 'enrollments' (student_id, course, score) DataFrames. 1) Left join to show all students with their courses (nulls for unenrolled). 2) Anti-join to find students with no enrollments. 3) Inner join and compute avg score per student. 4) Cross join students with a list of 3 available courses to show all possible assignments.",
            "starter": (
                "import polars as pl\n\n"
                "students = pl.DataFrame({\n"
                "    'id': [1, 2, 3, 4, 5],\n"
                "    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],\n"
                "    'grade': ['A', 'B', 'A', 'C', 'B']\n"
                "})\n"
                "enrollments = pl.DataFrame({\n"
                "    'student_id': [1, 1, 2, 3, 3, 3],\n"
                "    'course': ['Math', 'Science', 'Math', 'English', 'Math', 'Art'],\n"
                "    'score': [92, 87, 75, 88, 95, 91]\n"
                "})\n\n"
                "# 1. Left join — all students with courses\n"
                "# TODO: left = students.join(enrollments, left_on='id', right_on='student_id', how='left')\n"
                "# TODO: print('Left join:', left)\n\n"
                "# 2. Anti join — students with no enrollments\n"
                "# TODO: no_courses = students.join(enrollments, left_on='id', right_on='student_id', how='anti')\n"
                "# TODO: print('No courses:', no_courses)\n\n"
                "# 3. Inner join + avg score per student\n"
                "# TODO: inner = students.join(enrollments, left_on='id', right_on='student_id', how='inner')\n"
                "# TODO: avg_scores = inner.group_by('name').agg(pl.col('score').mean().round(1).alias('avg_score'))\n"
                "# TODO: print('Avg scores:', avg_scores)\n\n"
                "# 4. Cross join: each student x each available course\n"
                "courses = pl.DataFrame({'available_course': ['Math', 'Science', 'Art']})\n"
                "# TODO: assignments = students.select('name').join(courses, how='cross')\n"
                "# TODO: print(f'All assignments ({len(assignments)} rows):', assignments)"
            ),
        },
    },
    {
        "title": "String & Date Operations",
        "desc": "Polars has a rich .str and .dt namespace for vectorized string and datetime manipulations.",
        "code1_title": "String Operations (.str)",
        "code1": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'email': ['alice@example.com', 'bob@test.org', 'carol@example.com'],\n"
            "    'full_name': ['Alice Smith', 'Bob Jones', 'Carol White'],\n"
            "    'code': ['  ABC-123  ', 'DEF-456', ' GHI-789 ']\n"
            "})\n\n"
            "result = df.with_columns([\n"
            "    pl.col('email').str.split('@').list.get(1).alias('domain'),\n"
            "    pl.col('email').str.contains('example').alias('is_example'),\n"
            "    pl.col('full_name').str.split(' ').list.get(0).alias('first_name'),\n"
            "    pl.col('full_name').str.to_lowercase().alias('name_lower'),\n"
            "    pl.col('code').str.strip_chars().alias('code_clean'),\n"
            "    pl.col('code').str.strip_chars().str.replace('-', '_').alias('code_underscore')\n"
            "])\n"
            "print(result)"
        ),
        "code2_title": "Date/Time Operations (.dt)",
        "code2": (
            "import polars as pl\n"
            "from datetime import date\n\n"
            "df = pl.DataFrame({\n"
            "    'date_str': ['2024-01-15', '2024-03-22', '2024-07-04', '2024-12-31'],\n"
            "    'event': ['Q1 Review', 'Sprint End', 'Holiday', 'Year End']\n"
            "})\n\n"
            "df2 = df.with_columns(\n"
            "    pl.col('date_str').str.to_date('%Y-%m-%d').alias('date')\n"
            ")\n\n"
            "result = df2.with_columns([\n"
            "    pl.col('date').dt.year().alias('year'),\n"
            "    pl.col('date').dt.month().alias('month'),\n"
            "    pl.col('date').dt.day().alias('day'),\n"
            "    pl.col('date').dt.weekday().alias('weekday'),  # Mon=1\n"
            "    pl.col('date').dt.quarter().alias('quarter'),\n"
            "    pl.col('date').dt.strftime('%B %d, %Y').alias('formatted')\n"
            "])\n"
            "print(result)"
        ),
                "code4_title": "str.extract with Regex, str.split_exact & dt.truncate",
        "code4": (
            "import polars as pl\n"
            "from datetime import date\n"
            "\n"
            "# String regex extraction\n"
            "df = pl.DataFrame({'log': [\n"
            "    '2024-01-15 ERROR db_pool Connection timeout after 30s',\n"
            "    '2024-01-16 INFO  auth_svc User alice logged in',\n"
            "    '2024-01-17 WARN  api_gw  Rate limit at 95%',\n"
            "]})\n"
            "\n"
            "result = df.with_columns([\n"
            "    pl.col('log').str.extract(r'(\\d{4}-\\d{2}-\\d{2})', 1).alias('date'),\n"
            "    pl.col('log').str.extract(r'\\d{4}-\\d{2}-\\d{2} (\\w+)', 1).alias('level'),\n"
            "    pl.col('log').str.extract(r'\\w+ \\w+\\s+(\\w+)\\s', 1).alias('service'),\n"
            "])\n"
            "print('Regex extraction:')\n"
            "print(result)\n"
            "\n"
            "# str.split_exact — fixed number of parts\n"
            "df2 = pl.DataFrame({'ts': ['2024-01-15', '2024-06-30', '2024-12-01']})\n"
            "split = df2.with_columns(\n"
            "    pl.col('ts').str.split_exact('-', 2).alias('parts')\n"
            ").unnest('parts').rename({'field_0':'year','field_1':'month','field_2':'day'})\n"
            "print('\\nSplit date parts:')\n"
            "print(split)\n"
            "\n"
            "# dt.truncate — round dates to month/week\n"
            "df3 = pl.DataFrame({'dt': pl.date_range(\n"
            "    pl.date(2024, 1, 1), pl.date(2024, 3, 31), interval='11d', eager=True\n"
            ")})\n"
            "df3 = df3.with_columns([\n"
            "    pl.col('dt').dt.truncate('1mo').alias('month_start'),\n"
            "    pl.col('dt').dt.truncate('1w').alias('week_start'),\n"
            "])\n"
            "print('\\nDate truncation:')\n"
            "print(df3.head(6))"
        ),
        "rw_scenario": "Analytics: Parse raw log timestamps, extract hour/day features, and flag weekend traffic spikes.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n"
            "from datetime import datetime, timedelta\n\n"
            "np.random.seed(42)\n"
            "n = 10_000\n"
            "base = datetime(2024, 1, 1)\n"
            "logs = pl.DataFrame({\n"
            "    'timestamp': [(base + timedelta(hours=int(h))).strftime('%Y-%m-%d %H:%M:%S')\n"
            "                  for h in np.random.uniform(0, 24*90, n)],\n"
            "    'user_id': np.random.randint(1, 1000, n),\n"
            "    'page': np.random.choice(['/home','/product','/cart','/checkout'], n),\n"
            "    'response_ms': np.random.exponential(200, n).round(1)\n"
            "})\n\n"
            "enriched = logs.with_columns(\n"
            "    pl.col('timestamp').str.to_datetime('%Y-%m-%d %H:%M:%S').alias('dt')\n"
            ").with_columns([\n"
            "    pl.col('dt').dt.hour().alias('hour'),\n"
            "    pl.col('dt').dt.weekday().alias('weekday'),\n"
            "    (pl.col('dt').dt.weekday() >= 6).alias('is_weekend')\n"
            "])\n\n"
            "hourly = enriched.group_by('hour').agg([\n"
            "    pl.len().alias('requests'),\n"
            "    pl.col('response_ms').mean().round(1).alias('avg_ms')\n"
            "]).sort('hour')\n"
            "print('Peak hour:', hourly.top_k(1, by='requests')['hour'][0], 'h')\n"
            "print('Weekend traffic:', enriched['is_weekend'].mean().__round__(1))"
        ),
        "code3_title": "str.contains, str.split, str.replace & Date Arithmetic",
        "code3": (
            "import polars as pl\n"
            "from datetime import date\n\n"
            "# String operations\n"
            "df = pl.DataFrame({\n"
            "    'url': ['https://example.com/product/123', 'https://example.com/cart', 'https://shop.io/item/456'],\n"
            "    'tags': ['python,data,science', 'ml,ai,deep-learning', 'stats,python,r'],\n"
            "})\n\n"
            "result = df.with_columns([\n"
            "    pl.col('url').str.contains('product').alias('is_product_page'),\n"
            "    pl.col('url').str.split('/').list.last().alias('path_end'),\n"
            "    pl.col('url').str.replace('https://', '').alias('url_no_scheme'),\n"
            "    pl.col('tags').str.split(',').list.len().alias('tag_count'),\n"
            "    pl.col('tags').str.contains('python').alias('has_python'),\n"
            "])\n"
            "print(result)\n\n"
            "# Date arithmetic\n"
            "df2 = pl.DataFrame({\n"
            "    'start': [date(2024, 1, 1), date(2024, 3, 15), date(2024, 6, 30)],\n"
            "    'end':   [date(2024, 4, 1), date(2024, 5, 20), date(2024, 12, 31)]\n"
            "})\n"
            "df3 = df2.with_columns([\n"
            "    pl.col('start').dt.strftime('%B %Y').alias('start_label'),\n"
            "    (pl.col('end') - pl.col('start')).dt.total_days().alias('duration_days'),\n"
            "    pl.col('start').dt.month().alias('start_month'),\n"
            "    pl.col('end').dt.year().alias('end_year'),\n"
            "])\n"
            "print(df3)"
        ),
        "practice": {
            "title": "String & DateTime Feature Engineering",
            "desc": "Create a DataFrame with 'email', 'signup_date' (str), 'username'. 1) Extract domain from email using str.split. 2) Flag emails from 'gmail.com' or 'yahoo.com' with str.contains. 3) Parse signup_date and extract year, month, weekday. 4) Use dt.strftime to create a formatted label. 5) Compute days since signup (use date(2025,1,1) as today).",
            "starter": (
                "import polars as pl\n"
                "from datetime import date\n\n"
                "df = pl.DataFrame({\n"
                "    'username': ['alice_99', 'bob.smith', 'carol123', 'dave_x', 'eve.m'],\n"
                "    'email': ['alice@gmail.com', 'bob@company.org', 'carol@yahoo.com', 'dave@outlook.com', 'eve@gmail.com'],\n"
                "    'signup_date': ['2023-03-15', '2022-11-01', '2024-01-20', '2021-07-04', '2023-09-30']\n"
                "})\n\n"
                "# 1. Extract domain\n"
                "# TODO: df = df.with_columns(\n"
                "#     pl.col('email').str.split('@').list.get(1).alias('domain')\n"
                "# )\n\n"
                "# 2. Flag gmail/yahoo\n"
                "# TODO: df = df.with_columns(\n"
                "#     pl.col('email').str.contains('gmail|yahoo').alias('is_free_email')\n"
                "# )\n\n"
                "# 3. Parse date and extract features\n"
                "# TODO: df = df.with_columns(\n"
                "#     pl.col('signup_date').str.to_date('%Y-%m-%d').alias('date')\n"
                "# ).with_columns([\n"
                "#     pl.col('date').dt.year().alias('year'),\n"
                "#     pl.col('date').dt.month().alias('month'),\n"
                "#     pl.col('date').dt.weekday().alias('weekday'),\n"
                "# ])\n\n"
                "# 4. Formatted label\n"
                "# TODO: df = df.with_columns(\n"
                "#     pl.col('date').dt.strftime('%b %Y').alias('signup_label')\n"
                "# )\n\n"
                "# 5. Days since signup\n"
                "today = date(2025, 1, 1)\n"
                "# TODO: df = df.with_columns(\n"
                "#     (pl.lit(today) - pl.col('date')).dt.total_days().alias('days_since_signup')\n"
                "# )\n"
                "# TODO: print(df)"
            ),
        },
    },
    {
        "title": "Lazy API & Query Optimization",
        "desc": "Use LazyFrame to build a query plan that Polars optimizes and executes in parallel — essential for large data.",
        "code1_title": "LazyFrame Basics",
        "code1": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "df = pl.DataFrame({\n"
            "    'id': range(1_000_000),\n"
            "    'value': np.random.randn(1_000_000),\n"
            "    'group': np.random.choice(['A','B','C','D'], 1_000_000),\n"
            "    'score': np.random.randint(0, 100, 1_000_000)\n"
            "})\n\n"
            "# Convert to LazyFrame\n"
            "result = (\n"
            "    df.lazy()                            # build query plan\n"
            "    .filter(pl.col('score') > 50)        # predicate pushdown\n"
            "    .with_columns(\n"
            "        (pl.col('value') * 2).alias('value2')\n"
            "    )\n"
            "    .group_by('group').agg(\n"
            "        pl.col('value2').mean().round(4).alias('mean_v2'),\n"
            "        pl.len().alias('count')\n"
            "    )\n"
            "    .sort('group')\n"
            ")\n\n"
            "# See the query plan\n"
            "print(result.explain())\n\n"
            "# Execute\n"
            "print(result.collect())"
        ),
        "code2_title": "scan_csv & Streaming",
        "code2": (
            "import polars as pl\n"
            "import tempfile, os, numpy as np\n\n"
            "# Write a sample CSV to scan\n"
            "np.random.seed(42)\n"
            "n = 100_000\n"
            "tmp = pl.DataFrame({\n"
            "    'a': np.random.randint(0, 100, n),\n"
            "    'b': np.random.randn(n),\n"
            "    'c': np.random.choice(['X','Y','Z'], n)\n"
            "})\n"
            "path = os.path.join(tempfile.gettempdir(), 'polars_demo.csv')\n"
            "tmp.write_csv(path)\n\n"
            "# scan_csv: reads lazily — only loads needed data\n"
            "result = (\n"
            "    pl.scan_csv(path)\n"
            "    .filter(pl.col('c') == 'X')\n"
            "    .filter(pl.col('a') > 90)\n"
            "    .select(['a', 'b'])\n"
            "    .collect()\n"
            ")\n"
            "print('Filtered result:', result.shape)\n"
            "print(result.head())"
        ),
                "code4_title": "Streaming Mode & LazyFrame Schema Inspection",
        "code4": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import tempfile, os\n"
            "\n"
            "np.random.seed(42)\n"
            "n = 500_000\n"
            "df = pl.DataFrame({\n"
            "    'id':       range(n),\n"
            "    'amount':   np.random.exponential(100, n).round(2),\n"
            "    'category': np.random.choice(['A','B','C','D'], n),\n"
            "    'flag':     np.random.choice([True, False], n),\n"
            "})\n"
            "pq_path = os.path.join(tempfile.gettempdir(), 'streaming_demo.parquet')\n"
            "df.write_parquet(pq_path)\n"
            "\n"
            "# LazyFrame schema inspection — no data loaded yet\n"
            "lf = pl.scan_parquet(pq_path)\n"
            "print('Schema (no data loaded):')\n"
            "print(lf.schema)\n"
            "print('Columns:', lf.columns)\n"
            "\n"
            "# Build a lazy query\n"
            "query = (\n"
            "    lf.filter(pl.col('flag') & (pl.col('amount') > 50))\n"
            "      .group_by('category')\n"
            "      .agg([\n"
            "          pl.col('amount').mean().round(2).alias('avg'),\n"
            "          pl.len().alias('count')\n"
            "      ])\n"
            "      .sort('avg', descending=True)\n"
            ")\n"
            "\n"
            "# Show the optimized query plan\n"
            "print('\\nOptimized plan:')\n"
            "query.explain(optimized=True)\n"
            "\n"
            "# Execute\n"
            "result = query.collect()\n"
            "print('\\nResult:')\n"
            "print(result)"
        ),
        "rw_scenario": "Pipeline optimization: Process 5GB of log files lazily — Polars scans, filters, and aggregates without loading everything into memory.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import tempfile, os\n\n"
            "# Simulate large dataset written to CSV\n"
            "np.random.seed(42)\n"
            "n = 200_000\n"
            "big_df = pl.DataFrame({\n"
            "    'ts': np.arange(n),\n"
            "    'user': np.random.randint(1, 10000, n),\n"
            "    'event': np.random.choice(['click','view','buy','exit'], n),\n"
            "    'duration_s': np.random.exponential(30, n).round(1),\n"
            "    'country': np.random.choice(['US','UK','DE','JP','BR'], n)\n"
            "})\n"
            "path = os.path.join(tempfile.gettempdir(), 'events.csv')\n"
            "big_df.write_csv(path)\n\n"
            "# Lazy pipeline — only loads relevant columns and rows\n"
            "summary = (\n"
            "    pl.scan_csv(path)\n"
            "    .filter(pl.col('event') == 'buy')\n"
            "    .filter(pl.col('duration_s') > 5)\n"
            "    .group_by('country').agg([\n"
            "        pl.len().alias('purchases'),\n"
            "        pl.col('duration_s').mean().round(2).alias('avg_duration'),\n"
            "        pl.col('user').n_unique().alias('unique_buyers')\n"
            "    ])\n"
            "    .sort('purchases', descending=True)\n"
            "    .collect()\n"
            ")\n"
            "print('Purchase summary by country:')\n"
            "print(summary)"
        ),
        "code3_title": "Lazy Pipeline: filter, select, groupby, collect",
        "code3": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "# Build a large DataFrame then use LazyFrame\n"
            "df = pl.DataFrame({\n"
            "    'user_id': np.random.randint(1, 500, 50_000),\n"
            "    'product': np.random.choice(['A','B','C','D','E'], 50_000),\n"
            "    'amount': np.random.exponential(100, 50_000).round(2),\n"
            "    'returned': np.random.choice([True, False], 50_000, p=[0.05, 0.95])\n"
            "})\n\n"
            "# Convert to lazy and build a multi-step pipeline\n"
            "lazy_result = (\n"
            "    df.lazy()\n"
            "    .filter(~pl.col('returned'))                   # exclude returns\n"
            "    .filter(pl.col('amount') > 10)                 # min order\n"
            "    .with_columns(\n"
            "        (pl.col('amount') * 1.1).alias('amount_with_tax')\n"
            "    )\n"
            "    .group_by(['user_id', 'product']).agg([\n"
            "        pl.len().alias('orders'),\n"
            "        pl.col('amount_with_tax').sum().round(2).alias('total_spent')\n"
            "    ])\n"
            "    .filter(pl.col('orders') >= 3)                 # frequent buyers\n"
            "    .sort('total_spent', descending=True)\n"
            ")\n\n"
            "# Execute\n"
            "result = lazy_result.collect()\n"
            "print(f'Frequent buyers: {len(result):,}')\n"
            "print(result.head(8))"
        ),
        "practice": {
            "title": "LazyFrame Pipeline with collect()",
            "desc": "Create a 100k-row DataFrame (in-memory) with 'customer_id', 'category', 'spend', 'is_member'. 1) Convert to lazy. 2) Filter: is_member=True AND spend > 20. 3) Add 'spend_after_discount' = spend * 0.9 for members. 4) GroupBy category: count, total spend, avg spend_after_discount. 5) Sort by total spend descending and collect(). Print the query plan with explain().",
            "starter": (
                "import polars as pl\n"
                "import numpy as np\n\n"
                "np.random.seed(0)\n"
                "n = 100_000\n"
                "df = pl.DataFrame({\n"
                "    'customer_id': np.random.randint(1, 5000, n),\n"
                "    'category': np.random.choice(['Food','Tech','Fashion','Home'], n),\n"
                "    'spend': np.random.exponential(60, n).round(2),\n"
                "    'is_member': np.random.choice([True, False], n, p=[0.4, 0.6])\n"
                "})\n\n"
                "# Build the lazy pipeline\n"
                "# TODO: lazy = df.lazy()\n"
                "# TODO: lazy = lazy.filter(pl.col('is_member') & (pl.col('spend') > 20))\n"
                "# TODO: lazy = lazy.with_columns(\n"
                "#     (pl.col('spend') * 0.9).round(2).alias('spend_after_discount')\n"
                "# )\n"
                "# TODO: lazy = lazy.group_by('category').agg([\n"
                "#     pl.len().alias('count'),\n"
                "#     pl.col('spend').sum().round(2).alias('total_spend'),\n"
                "#     pl.col('spend_after_discount').mean().round(2).alias('avg_discounted')\n"
                "# ])\n"
                "# TODO: lazy = lazy.sort('total_spend', descending=True)\n\n"
                "# Print query plan and execute\n"
                "# TODO: print(lazy.explain())\n"
                "# TODO: result = lazy.collect()\n"
                "# TODO: print(result)"
            ),
        },
    },
    {
        "title": "Reading & Writing Files",
        "desc": "Polars natively reads/writes CSV, JSON, Parquet, and Arrow — Parquet is the recommended format.",
        "code1_title": "CSV & JSON",
        "code1": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import tempfile, os\n\n"
            "np.random.seed(42)\n"
            "df = pl.DataFrame({\n"
            "    'id': range(100),\n"
            "    'name': [f'Item_{i}' for i in range(100)],\n"
            "    'value': np.random.randn(100).round(4),\n"
            "    'tag': np.random.choice(['A','B','C'], 100)\n"
            "})\n\n"
            "tmp = tempfile.gettempdir()\n\n"
            "# CSV\n"
            "csv_path = os.path.join(tmp, 'demo.csv')\n"
            "df.write_csv(csv_path)\n"
            "df_csv = pl.read_csv(csv_path)\n"
            "print('CSV roundtrip:', df_csv.shape)\n\n"
            "# JSON (newline-delimited)\n"
            "json_path = os.path.join(tmp, 'demo.ndjson')\n"
            "df.write_ndjson(json_path)\n"
            "df_json = pl.read_ndjson(json_path)\n"
            "print('NDJSON roundtrip:', df_json.shape)"
        ),
        "code2_title": "Parquet (Recommended Format)",
        "code2": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import tempfile, os\n\n"
            "np.random.seed(42)\n"
            "n = 500_000\n"
            "df = pl.DataFrame({\n"
            "    'id': range(n),\n"
            "    'amount': np.random.exponential(200, n).round(2),\n"
            "    'category': np.random.choice(['A','B','C','D'], n),\n"
            "    'flag': np.random.choice([True, False], n)\n"
            "})\n\n"
            "tmp = tempfile.gettempdir()\n"
            "pq_path = os.path.join(tmp, 'demo.parquet')\n\n"
            "# Write Parquet (compressed, columnar)\n"
            "df.write_parquet(pq_path, compression='zstd')\n"
            "size_mb = os.path.getsize(pq_path) / 1024 / 1024\n"
            "print(f'Parquet size: {size_mb:.2f} MB (for {n:,} rows)')\n\n"
            "# Read full\n"
            "df2 = pl.read_parquet(pq_path)\n"
            "print('Read back:', df2.shape)\n\n"
            "# Scan (lazy) — column pruning + predicate pushdown\n"
            "result = pl.scan_parquet(pq_path).filter(\n"
            "    pl.col('category') == 'A'\n"
            ").select(['id','amount']).collect()\n"
            "print('Filtered parquet:', result.shape)"
        ),
                "code4_title": "scan_csv with Schema Override & In-Memory Parquet",
        "code4": (
            "import polars as pl\n"
            "import io\n"
            "\n"
            "# scan_csv with explicit schema override\n"
            "csv_data = 'id,score,grade,active\\n1,92.5,A,true\\n2,78.0,B,false\\n3,85.5,A,true\\n'\n"
            "schema_override = {\n"
            "    'id':     pl.Int32,\n"
            "    'score':  pl.Float32,\n"
            "    'grade':  pl.Categorical,\n"
            "    'active': pl.Boolean,\n"
            "}\n"
            "df = pl.read_csv(io.StringIO(csv_data), schema_overrides=schema_override)\n"
            "print('With schema override:')\n"
            "print(df)\n"
            "print('Dtypes:', df.dtypes)\n"
            "\n"
            "# In-memory Parquet (BytesIO — no file system needed)\n"
            "import numpy as np\n"
            "np.random.seed(0)\n"
            "df2 = pl.DataFrame({\n"
            "    'x': np.random.randn(1000).astype('float32'),\n"
            "    'y': np.random.randint(0, 10, 1000),\n"
            "})\n"
            "buf = io.BytesIO()\n"
            "df2.write_parquet(buf, compression='zstd')\n"
            "buf.seek(0)\n"
            "size_kb = buf.getbuffer().nbytes / 1024\n"
            "df3 = pl.read_parquet(buf)\n"
            "print(f'\\nIn-memory Parquet: {df2.shape} → {size_kb:.1f} KB')\n"
            "print('Read back:', df3.shape)"
        ),
        "rw_scenario": "Data Lake: Store processed transaction data in Parquet partitioned by month — 10x smaller than CSV, 5x faster queries.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import tempfile, os\n"
            "from datetime import date, timedelta\n\n"
            "np.random.seed(42)\n"
            "n = 100_000\n"
            "start = date(2024, 1, 1)\n"
            "df = pl.DataFrame({\n"
            "    'txn_id': range(n),\n"
            "    'date': [str(start + timedelta(days=int(d))) for d in np.random.randint(0, 365, n)],\n"
            "    'amount': np.random.exponential(150, n).round(2),\n"
            "    'merchant': np.random.choice(['Amazon','Netflix','Uber','Spotify'], n)\n"
            "})\n\n"
            "# Add month column for partitioning\n"
            "df2 = df.with_columns(\n"
            "    pl.col('date').str.to_date('%Y-%m-%d').dt.month().alias('month')\n"
            ")\n\n"
            "tmp = tempfile.gettempdir()\n"
            "pq_path = os.path.join(tmp, 'transactions.parquet')\n"
            "df2.write_parquet(pq_path, compression='snappy')\n\n"
            "# Query Jan only — fast because of column pushdown\n"
            "jan = pl.scan_parquet(pq_path).filter(\n"
            "    pl.col('month') == 1\n"
            ").collect()\n"
            "print(f'January transactions: {len(jan):,}')\n"
            "print(f'Jan revenue: ${jan[\"amount\"].sum():,.2f}')"
        ),
        "code3_title": "IPC/Arrow Format and In-Memory Read",
        "code3": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import tempfile, os, io\n\n"
            "np.random.seed(42)\n"
            "df = pl.DataFrame({\n"
            "    'id': range(1000),\n"
            "    'value': np.random.randn(1000).round(4),\n"
            "    'category': np.random.choice(['A','B','C'], 1000)\n"
            "})\n\n"
            "tmp = tempfile.gettempdir()\n\n"
            "# IPC (Arrow) — fastest local I/O format\n"
            "ipc_path = os.path.join(tmp, 'demo.arrow')\n"
            "df.write_ipc(ipc_path)\n"
            "df_ipc = pl.read_ipc(ipc_path)\n"
            "size_ipc = os.path.getsize(ipc_path) / 1024\n"
            "print(f'IPC size: {size_ipc:.1f} KB, shape: {df_ipc.shape}')\n\n"
            "# In-memory CSV read from string\n"
            "csv_str = df.write_csv()\n"
            "df_str = pl.read_csv(io.StringIO(csv_str))\n"
            "print('From string CSV:', df_str.shape)\n\n"
            "# Column pruning on Parquet read\n"
            "pq_path = os.path.join(tmp, 'pruned_demo.parquet')\n"
            "df.write_parquet(pq_path)\n"
            "df_cols = pl.read_parquet(pq_path, columns=['id', 'category'])\n"
            "print('Column-pruned parquet:', df_cols.shape, df_cols.columns)"
        ),
        "practice": {
            "title": "CSV Round-Trip and Parquet Query",
            "desc": "Write a 10,000-row orders DataFrame to CSV and Parquet. Read the CSV back and verify shape. Use scan_parquet (LazyFrame) to filter one region and select specific columns, then collect.",
            "starter": (
                "import polars as pl\n"
                "import numpy as np\n"
                "import tempfile, os\n\n"
                "np.random.seed(42)\n"
                "n = 10_000\n"
                "df = pl.DataFrame({\n"
                "    'order_id': range(n),\n"
                "    'customer': [f'cust_{i % 500}' for i in range(n)],\n"
                "    'product': np.random.choice(['Widget','Gadget','Doohickey'], n),\n"
                "    'amount': np.random.exponential(100, n).round(2),\n"
                "    'region': np.random.choice(['North','South','East','West'], n),\n"
                "})\n\n"
                "tmp = tempfile.gettempdir()\n\n"
                "# TODO: Write df to CSV and read it back\n"
                "# csv_path = os.path.join(tmp, 'orders.csv')\n"
                "# df.write_csv(???)\n"
                "# df_csv = pl.read_csv(???)\n"
                "# print('CSV roundtrip:', df_csv.shape)\n\n"
                "# TODO: Write df to Parquet with 'zstd' compression\n"
                "# pq_path = os.path.join(tmp, 'orders.parquet')\n"
                "# df.write_parquet(???, compression='zstd')\n\n"
                "# TODO: Use scan_parquet (lazy) to filter region == 'North'\n"
                "# and select only ['order_id', 'customer', 'amount']\n"
                "# result = pl.scan_parquet(pq_path).filter(???).select(???).collect()\n"
                "# print('North orders:', result.shape)\n"
                "# print('North revenue: ${:.2f}'.format(result['amount'].sum()))"
            ),
        },
    },
    {
        "title": "Window Functions",
        "desc": "Compute rolling statistics, cumulative sums, and rank within groups using Polars window expressions.",
        "code1_title": "Rolling & Cumulative",
        "code1": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "df = pl.DataFrame({\n"
            "    'day': range(1, 31),\n"
            "    'sales': np.random.randint(50, 200, 30)\n"
            "})\n\n"
            "result = df.with_columns([\n"
            "    pl.col('sales').cum_sum().alias('cumulative_sales'),\n"
            "    pl.col('sales').rolling_mean(window_size=7).round(1).alias('7d_avg'),\n"
            "    pl.col('sales').rolling_max(window_size=7).alias('7d_max'),\n"
            "    pl.col('sales').rolling_std(window_size=7).round(2).alias('7d_std'),\n"
            "    pl.col('sales').pct_change().round(4).alias('pct_change')\n"
            "])\n"
            "print(result.tail(10))"
        ),
        "code2_title": "Group Window Expressions",
        "code2": (
            "import polars as pl\n\n"
            "df = pl.DataFrame({\n"
            "    'dept': ['Eng','Eng','Eng','Sales','Sales','HR','HR'],\n"
            "    'name': ['Alice','Bob','Carol','Dave','Eve','Frank','Grace'],\n"
            "    'salary': [90000, 85000, 95000, 70000, 65000, 55000, 58000]\n"
            "})\n\n"
            "result = df.with_columns([\n"
            "    pl.col('salary').rank('dense').over('dept').alias('rank_in_dept'),\n"
            "    pl.col('salary').mean().over('dept').round(0).alias('dept_avg'),\n"
            "    (pl.col('salary') - pl.col('salary').mean().over('dept'))\n"
            "        .round(0).alias('vs_dept_avg'),\n"
            "    pl.col('salary').max().over('dept').alias('dept_max')\n"
            "])\n"
            "print(result)"
        ),
                "code4_title": "ewm_mean (Exponential Weighted), rolling_quantile & map_elements",
        "code4": (
            "import polars as pl\n"
            "import numpy as np\n"
            "\n"
            "np.random.seed(42)\n"
            "df = pl.DataFrame({\n"
            "    'day':   range(1, 31),\n"
            "    'price': np.random.uniform(95, 105, 30).round(2),\n"
            "    'vol':   np.random.randint(1000, 5000, 30),\n"
            "})\n"
            "\n"
            "result = df.with_columns([\n"
            "    # Exponential weighted mean (recent values get more weight)\n"
            "    pl.col('price').ewm_mean(span=5).round(3).alias('ewm_5'),\n"
            "    # Rolling 7-day median (robust to outliers)\n"
            "    pl.col('price').rolling_median(window_size=7).round(3).alias('rolling_med_7'),\n"
            "    # Rolling 75th percentile\n"
            "    pl.col('vol').rolling_quantile(quantile=0.75, window_size=7).alias('vol_q75'),\n"
            "])\n"
            "print(result.head(10))\n"
            "\n"
            "# map_elements for custom per-element logic\n"
            "df2 = pl.DataFrame({'scores': [[85, 90, 78], [60, 70], [95, 88, 92, 80]]})\n"
            "result2 = df2.with_columns(\n"
            "    pl.col('scores').map_elements(\n"
            "        lambda lst: round(sum(lst) / len(lst), 2),\n"
            "        return_dtype=pl.Float64\n"
            "    ).alias('avg_score')\n"
            ")\n"
            "print('\\nCustom avg via map_elements:')\n"
            "print(result2)"
        ),
        "rw_scenario": "Finance: Compute 30-day rolling average revenue and rank salespeople within each region monthly.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n"
            "from datetime import date, timedelta\n\n"
            "np.random.seed(42)\n"
            "n = 500\n"
            "start = date(2024, 1, 1)\n"
            "df = pl.DataFrame({\n"
            "    'date': [str(start + timedelta(days=i)) for i in range(n)],\n"
            "    'region': np.random.choice(['North','South','East','West'], n),\n"
            "    'rep': [f'Rep_{np.random.randint(1,6)}' for _ in range(n)],\n"
            "    'revenue': np.random.exponential(5000, n).round(2)\n"
            "})\n\n"
            "result = df.sort('date').with_columns([\n"
            "    pl.col('revenue').rolling_mean(window_size=30).round(2).alias('30d_avg_rev'),\n"
            "    pl.col('revenue').cum_sum().alias('ytd_revenue'),\n"
            "    pl.col('revenue').rank('dense', descending=True).over('region').alias('region_rank')\n"
            "])\n\n"
            "# Top performer per region\n"
            "top = result.filter(pl.col('region_rank') == 1).group_by('region').agg(\n"
            "    pl.col('rep').first(),\n"
            "    pl.col('revenue').sum().round(2).alias('total_rev')\n"
            ").sort('total_rev', descending=True)\n"
            "print('Top reps by region:')\n"
            "print(top)"
        ),
        "code3_title": "Lead/Lag and Running Max",
        "code3": (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "df = pl.DataFrame({\n"
            "    'day': range(1, 21),\n"
            "    'sales': np.random.randint(100, 500, 20)\n"
            "})\n\n"
            "result = df.with_columns([\n"
            "    pl.col('sales').shift(1).alias('prev_day'),\n"
            "    pl.col('sales').shift(-1).alias('next_day'),\n"
            "    (pl.col('sales') - pl.col('sales').shift(1)).alias('day_delta'),\n"
            "    pl.col('sales').rolling_mean(window_size=3, min_periods=1).round(1).alias('3d_avg'),\n"
            "    pl.col('sales').cum_max().alias('running_max'),\n"
            "    (pl.col('sales') / pl.col('sales').max() * 100).round(1).alias('pct_of_max')\n"
            "])\n"
            "print(result)"
        ),
        "practice": {
            "title": "Sales Trend Analysis with Windows",
            "desc": "Given 90 days of daily sales data with product and revenue columns, add: (1) 7-day rolling mean of revenue, (2) cumulative units sold, (3) revenue as % of dataset max, (4) rank within each product group by revenue descending. Then print top 3 days per product.",
            "starter": (
                "import polars as pl\n"
                "import numpy as np\n"
                "from datetime import date, timedelta\n\n"
                "np.random.seed(42)\n"
                "n = 90\n"
                "df = pl.DataFrame({\n"
                "    'date': [str(date(2024, 1, 1) + timedelta(days=i)) for i in range(n)],\n"
                "    'product': np.random.choice(['Widget', 'Gadget', 'Doohickey'], n),\n"
                "    'units_sold': np.random.randint(10, 200, n),\n"
                "    'revenue': np.random.exponential(500, n).round(2),\n"
                "})\n\n"
                "# TODO: Sort by date and add window columns:\n"
                "# 1. rolling_mean of revenue (window=7, min_periods=1) -> 'rolling_7d'\n"
                "# 2. cum_sum of units_sold -> 'cumulative_units'\n"
                "# 3. revenue / max(revenue) * 100 -> 'pct_of_peak'\n"
                "# 4. rank of revenue within 'product' group (descending) -> 'product_rank'\n"
                "result = df  # TODO: replace\n\n"
                "# TODO: Filter product_rank <= 3 and print top days per product\n"
                "# top3 = result.filter(pl.col('product_rank') <= 3).sort(['product', 'product_rank'])\n"
                "# print(top3)"
            ),
        },
    },
    {
        "title": "Polars vs Pandas Migration",
        "desc": "Key differences and equivalents between Polars and Pandas — migrate your workflows efficiently.",
        "code1_title": "Side-by-Side Comparison",
        "code1": (
            "import polars as pl\n"
            "import pandas as pd\n\n"
            "# Creating a DataFrame\n"
            "# Pandas:\n"
            "pd_df = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6]})\n\n"
            "# Polars:\n"
            "pl_df = pl.DataFrame({'a': [1,2,3], 'b': [4,5,6]})\n\n"
            "# Filtering\n"
            "# Pandas: df[df['a'] > 1]\n"
            "# Polars:\n"
            "print(pl_df.filter(pl.col('a') > 1))\n\n"
            "# Adding column\n"
            "# Pandas: df['c'] = df['a'] + df['b']\n"
            "# Polars:\n"
            "pl_df2 = pl_df.with_columns((pl.col('a') + pl.col('b')).alias('c'))\n"
            "print(pl_df2)\n\n"
            "# GroupBy\n"
            "# Pandas: df.groupby('a')['b'].sum()\n"
            "# Polars:\n"
            "pl_df3 = pl.DataFrame({'a': ['x','x','y','y'], 'b': [1,2,3,4]})\n"
            "print(pl_df3.group_by('a').agg(pl.col('b').sum()))"
        ),
        "code2_title": "Converting Between Polars & Pandas",
        "code2": (
            "import polars as pl\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "# Start with Pandas\n"
            "pd_df = pd.DataFrame({\n"
            "    'name': ['Alice', 'Bob', 'Carol'],\n"
            "    'score': [92.5, 88.0, 95.1]\n"
            "})\n\n"
            "# Pandas -> Polars\n"
            "pl_df = pl.from_pandas(pd_df)\n"
            "print('From pandas:', pl_df)\n\n"
            "# Polars -> Pandas\n"
            "back_to_pd = pl_df.to_pandas()\n"
            "print('Back to pandas:', back_to_pd.dtypes)\n\n"
            "# Polars -> NumPy\n"
            "arr = pl_df['score'].to_numpy()\n"
            "print('NumPy array:', arr)\n\n"
            "# Apply pandas where Polars lacks support\n"
            "# e.g., complex visualization or sklearn pipelines\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "X = StandardScaler().fit_transform(pl_df.select('score').to_pandas())\n"
            "print('Scaled scores:', X.flatten().round(2))"
        ),
                "code4_title": "Arrow Zero-Copy Interchange & Categorical dtype",
        "code4": (
            "import polars as pl\n"
            "import pandas as pd\n"
            "import numpy as np\n"
            "\n"
            "# Categorical dtype in Polars (much more efficient than object)\n"
            "np.random.seed(42)\n"
            "n = 100_000\n"
            "df_pl = pl.DataFrame({\n"
            "    'product':  pl.Series(np.random.choice(['Widget','Gadget','Doohickey'], n)).cast(pl.Categorical),\n"
            "    'region':   pl.Series(np.random.choice(['North','South','East','West'], n)).cast(pl.Categorical),\n"
            "    'revenue':  np.random.exponential(200, n).round(2),\n"
            "})\n"
            "print('Categorical memory usage:')\n"
            "print(f'  estimated size: {df_pl.estimated_size(\"mb\"):.2f} MB')\n"
            "print(f'  product unique values: {df_pl[\"product\"].n_unique()}')\n"
            "\n"
            "# Zero-copy to pandas via Arrow\n"
            "df_pd = df_pl.to_pandas(use_pyarrow_extension_array=True)\n"
            "print('\\nArrow-backed pandas dtypes:')\n"
            "print(df_pd.dtypes)\n"
            "\n"
            "# from_pandas preserving categorical\n"
            "df_pd2 = pd.DataFrame({\n"
            "    'color': pd.Categorical(['red','blue','red','green','blue']),\n"
            "    'val':   [1, 2, 3, 4, 5]\n"
            "})\n"
            "df_pl2 = pl.from_pandas(df_pd2)\n"
            "print('\\nFrom pandas Categorical:')\n"
            "print(df_pl2)\n"
            "print('dtype:', df_pl2['color'].dtype)"
        ),
        "rw_scenario": "Migration: Rewrite a slow Pandas ETL pipeline in Polars — same logic, 8x faster on 10M rows.",
        "rw_code": (
            "import polars as pl\n"
            "import pandas as pd\n"
            "import numpy as np\n"
            "import time\n\n"
            "np.random.seed(42)\n"
            "n = 500_000\n"
            "data = {\n"
            "    'user_id': np.random.randint(1, 10000, n),\n"
            "    'amount': np.random.exponential(100, n),\n"
            "    'category': np.random.choice(['A','B','C'], n)\n"
            "}\n\n"
            "# PANDAS approach\n"
            "t0 = time.time()\n"
            "pd_df = pd.DataFrame(data)\n"
            "pd_result = (pd_df[pd_df['amount'] > 50]\n"
            "             .groupby('category')['amount']\n"
            "             .agg(['mean','sum','count'])\n"
            "             .reset_index())\n"
            "t_pd = time.time() - t0\n\n"
            "# POLARS approach\n"
            "t0 = time.time()\n"
            "pl_df = pl.DataFrame(data)\n"
            "pl_result = (pl_df.filter(pl.col('amount') > 50)\n"
            "             .group_by('category').agg([\n"
            "                 pl.col('amount').mean().round(4).alias('mean'),\n"
            "                 pl.col('amount').sum().round(2).alias('sum'),\n"
            "                 pl.len().alias('count')\n"
            "             ])\n"
            "             .sort('category'))\n"
            "t_pl = time.time() - t0\n\n"
            "print(f'Pandas:  {t_pd:.3f}s')\n"
            "print(f'Polars:  {t_pl:.3f}s')\n"
            "print(f'Speedup: {t_pd/t_pl:.1f}x')\n"
            "print(pl_result)"
        ),
        "code3_title": "Method Chaining Comparison",
        "code3": (
            "import polars as pl\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "n = 1000\n"
            "data = {\n"
            "    'dept': np.random.choice(['Eng', 'Sales', 'HR'], n),\n"
            "    'score': np.random.randint(0, 100, n),\n"
            "    'active': np.random.choice([True, False], n)\n"
            "}\n\n"
            "# Pandas: filter + conditional column + groupby\n"
            "pd_df = pd.DataFrame(data)\n"
            "pd_active = pd_df[pd_df['active']].copy()\n"
            "pd_active['grade'] = pd.cut(pd_active['score'], bins=[0,60,80,100], labels=['C','B','A'])\n"
            "pd_result = pd_active.groupby(['dept','grade'])['score'].mean().round(2).reset_index()\n"
            "print('Pandas:')\n"
            "print(pd_result.sort_values(['dept','grade']).head(6))\n\n"
            "# Polars equivalent — more explicit, no chained assignment\n"
            "pl_df = pl.DataFrame(data)\n"
            "pl_result = (\n"
            "    pl_df.filter(pl.col('active'))\n"
            "    .with_columns(\n"
            "        pl.when(pl.col('score') >= 80).then(pl.lit('A'))\n"
            "          .when(pl.col('score') >= 60).then(pl.lit('B'))\n"
            "          .otherwise(pl.lit('C')).alias('grade')\n"
            "    )\n"
            "    .group_by(['dept', 'grade'])\n"
            "    .agg(pl.col('score').mean().round(2).alias('avg_score'))\n"
            "    .sort(['dept', 'grade'])\n"
            ")\n"
            "print('\\nPolars:')\n"
            "print(pl_result.head(6))"
        ),
        "practice": {
            "title": "Rewrite a Pandas Pipeline in Polars",
            "desc": "A Pandas pipeline filters premium users with spend > $50, groups by product, and aggregates mean/sum/count. Rewrite the exact same logic in Polars using filter, group_by, agg, and sort.",
            "starter": (
                "import pandas as pd\n"
                "import polars as pl\n"
                "import numpy as np\n\n"
                "np.random.seed(42)\n"
                "n = 50_000\n"
                "data = {\n"
                "    'user_id': np.random.randint(1, 5000, n),\n"
                "    'product': np.random.choice(['A', 'B', 'C', 'D'], n),\n"
                "    'spend': np.random.exponential(75, n).round(2),\n"
                "    'is_premium': np.random.choice([True, False], n)\n"
                "}\n\n"
                "# Existing Pandas pipeline (working — do not modify)\n"
                "pd_df = pd.DataFrame(data)\n"
                "pd_result = (\n"
                "    pd_df[pd_df['is_premium'] & (pd_df['spend'] > 50)]\n"
                "    .groupby('product')['spend']\n"
                "    .agg(['mean', 'sum', 'count'])\n"
                "    .reset_index()\n"
                "    .sort_values('sum', ascending=False)\n"
                ")\n"
                "print('Pandas result:')\n"
                "print(pd_result)\n\n"
                "# TODO: Rewrite in Polars\n"
                "pl_df = pl.DataFrame(data)\n"
                "pl_result = (\n"
                "    pl_df\n"
                "    # TODO: .filter(is_premium AND spend > 50)\n"
                "    # TODO: .group_by('product').agg(mean, sum, count of 'spend')\n"
                "    # TODO: .sort('sum', descending=True)\n"
                ")\n"
                "print('\\nPolars result:')\n"
                "# print(pl_result)"
            ),
        },
    },
    {
        "title": "Lazy Evaluation & Streaming",
        "desc": "Use Polars LazyFrame to build query plans that are optimized before execution. Process datasets larger than RAM with streaming mode.",
        "code1_title": "LazyFrame vs DataFrame",
        "code1": (
            "import polars as pl\nimport numpy as np\n\n"
            "np.random.seed(42)\n"
            "data = {\n"
            "    'id':       range(100_000),\n"
            "    'category': np.random.choice(['A','B','C','D'], 100_000),\n"
            "    'value':    np.random.randn(100_000) * 100 + 500,\n"
            "    'qty':      np.random.randint(1, 100, 100_000),\n"
            "}\n\n"
            "# Eager DataFrame\n"
            "df = pl.DataFrame(data)\n\n"
            "# Lazy: nothing executes yet\n"
            "lf = pl.LazyFrame(data)\n"
            "plan = (\n"
            "    lf\n"
            "    .filter(pl.col('value') > 500)\n"
            "    .group_by('category')\n"
            "    .agg(\n"
            "        pl.col('value').mean().alias('avg_val'),\n"
            "        pl.col('qty').sum().alias('total_qty'),\n"
            "    )\n"
            "    .sort('avg_val', descending=True)\n"
            ")\n"
            "print('Lazy plan (before execution):')\n"
            "print(plan.explain())\n"
            "result = plan.collect()  # executes query\n"
            "print('\\nResult after .collect():')\n"
            "print(result)"
        ),
        "code2_title": "Query Optimization with LazyFrame",
        "code2": (
            "import polars as pl\nimport numpy as np\nimport time\n\n"
            "np.random.seed(0)\n"
            "n = 500_000\n"
            "df = pl.DataFrame({\n"
            "    'user_id': np.random.randint(1, 10000, n),\n"
            "    'product': np.random.choice(['laptop','phone','tablet','watch'], n),\n"
            "    'revenue': np.random.exponential(100, n),\n"
            "    'country': np.random.choice(['US','UK','DE','FR','JP'], n),\n"
            "})\n\n"
            "# Eager: no optimization\n"
            "t0 = time.perf_counter()\n"
            "eager = (\n"
            "    df\n"
            "    .filter(pl.col('country') == 'US')\n"
            "    .filter(pl.col('revenue') > 50)\n"
            "    .group_by('product')\n"
            "    .agg(pl.col('revenue').sum())\n"
            ")\n"
            "t_eager = time.perf_counter() - t0\n\n"
            "# Lazy: Polars merges filters and optimizes scan\n"
            "t0 = time.perf_counter()\n"
            "lazy = (\n"
            "    df.lazy()\n"
            "    .filter(pl.col('country') == 'US')\n"
            "    .filter(pl.col('revenue') > 50)\n"
            "    .group_by('product')\n"
            "    .agg(pl.col('revenue').sum())\n"
            "    .collect()\n"
            ")\n"
            "t_lazy = time.perf_counter() - t0\n"
            "print(f'Eager: {t_eager*1000:.1f}ms | Lazy: {t_lazy*1000:.1f}ms')\n"
            "print(lazy.sort('revenue', descending=True))"
        ),
        "code3_title": "scan_csv for Larger-than-RAM Processing",
        "code3": (
            "import polars as pl\nimport tempfile, os, numpy as np\n\n"
            "# Create a sample CSV file\n"
            "np.random.seed(42)\n"
            "rows = 200_000\n"
            "with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:\n"
            "    fname = f.name\n"
            "    f.write('id,category,value,qty\\n')\n"
            "    cats = np.random.choice(['A','B','C'], rows)\n"
            "    vals = np.random.randn(rows) * 50 + 200\n"
            "    qtys = np.random.randint(1, 50, rows)\n"
            "    for i in range(rows):\n"
            "        f.write(f'{i},{cats[i]},{vals[i]:.2f},{qtys[i]}\\n')\n\n"
            "# scan_csv = lazy: doesn't load file yet\n"
            "lf = pl.scan_csv(fname)\n"
            "print('Schema:', lf.schema)\n\n"
            "result = (\n"
            "    lf\n"
            "    .filter(pl.col('value') > 200)\n"
            "    .group_by('category')\n"
            "    .agg(\n"
            "        pl.col('value').mean().round(2).alias('avg_value'),\n"
            "        pl.col('qty').sum().alias('total_qty'),\n"
            "        pl.len().alias('count'),\n"
            "    )\n"
            "    .sort('avg_value', descending=True)\n"
            "    .collect(streaming=True)  # streaming=True for large files\n"
            ")\n"
            "print(result)\n"
            "os.unlink(fname)"
        ),
        "code4_title": "Sink to Parquet (streaming write)",
        "code4": (
            "import polars as pl\nimport numpy as np\nimport tempfile, os\n\n"
            "np.random.seed(42)\n"
            "n = 100_000\n"
            "df = pl.DataFrame({\n"
            "    'ts':       pl.date_range(\n"
            "                    pl.date(2024, 1, 1), pl.date(2024, 12, 31),\n"
            "                    interval='1h', eager=True\n"
            "                )[:n],\n"
            "    'sensor':   np.random.choice(['s1','s2','s3'], n),\n"
            "    'reading':  np.random.normal(25, 5, n),\n"
            "})\n\n"
            "tmpdir = tempfile.mkdtemp()\n"
            "out_path = os.path.join(tmpdir, 'out.parquet')\n\n"
            "# Write to parquet\n"
            "df.write_parquet(out_path)\n\n"
            "# Read back with scan_parquet (lazy)\n"
            "result = (\n"
            "    pl.scan_parquet(out_path)\n"
            "    .filter(pl.col('reading') > 25)\n"
            "    .group_by('sensor')\n"
            "    .agg(pl.col('reading').mean().alias('avg_reading'), pl.len().alias('n'))\n"
            "    .collect()\n"
            ")\n"
            "print(result)\n"
            "fsize = os.path.getsize(out_path)\n"
            "print(f'Parquet file size: {fsize/1024:.1f} KB for {n:,} rows')\n"
            "import shutil; shutil.rmtree(tmpdir)"
        ),
        "rw_scenario": "Process daily clickstream logs (5GB CSV files) to compute daily active users and top 10 products per region. Use scan_csv + LazyFrame to avoid loading the entire file into RAM.",
        "rw_code": (
            "import polars as pl\nimport numpy as np\nimport tempfile, os\n\n"
            "# Simulate a medium CSV log file\n"
            "np.random.seed(7)\n"
            "n = 500_000\n"
            "with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:\n"
            "    fname = f.name\n"
            "    f.write('user_id,region,product,event,ts\\n')\n"
            "    regions  = np.random.choice(['NA','EU','APAC'], n)\n"
            "    products = np.random.choice([f'p{i}' for i in range(20)], n)\n"
            "    events   = np.random.choice(['click','view','purchase'], n, p=[0.6,0.3,0.1])\n"
            "    users    = np.random.randint(1, 10000, n)\n"
            "    for i in range(n):\n"
            "        f.write(f'{users[i]},{regions[i]},{products[i]},{events[i]},2024-01-{(i%28)+1:02d}\\n')\n\n"
            "result = (\n"
            "    pl.scan_csv(fname)\n"
            "    .filter(pl.col('event') == 'purchase')\n"
            "    .group_by(['region', 'product'])\n"
            "    .agg(pl.len().alias('purchases'))\n"
            "    .sort('purchases', descending=True)\n"
            "    .collect(streaming=True)\n"
            ")\n"
            "print('Top purchases by region:')\n"
            "print(result.head(10))\n"
            "os.unlink(fname)"
        ),
        "practice": {
            "title": "Lazy Pipeline on Large Simulated Dataset",
            "desc": "Create a 1M-row DataFrame with columns: user_id, country, product_category, revenue. Using LazyFrame, compute: (1) total revenue per country, (2) top 3 categories per country by revenue. Use .explain() to view the query plan. Compare execution time of eager vs lazy.",
            "starter": (
                "import polars as pl\nimport numpy as np\nimport time\n\n"
                "np.random.seed(42)\n"
                "n = 1_000_000\n"
                "df = pl.DataFrame({\n"
                "    'user_id':          np.random.randint(1, 100000, n),\n"
                "    'country':          np.random.choice(['US','UK','DE','FR','JP','AU'], n),\n"
                "    'product_category': np.random.choice(['electronics','clothing','food','books'], n),\n"
                "    'revenue':          np.random.exponential(50, n),\n"
                "})\n\n"
                "# TODO: (1) Total revenue per country using LazyFrame\n"
                "# TODO: (2) Top 3 categories per country by revenue\n"
                "# TODO: Compare eager vs lazy execution time\n"
                "# TODO: print the query plan with .explain()\n"
            ),
        },
    },
    {
        "title": "Window Functions",
        "desc": "Compute rolling statistics, cumulative aggregates, rank-based features, and temporal calculations within groups using Polars window expressions.",
        "code1_title": "Rolling & Expanding Windows",
        "code1": (
            "import polars as pl\nimport numpy as np\n\n"
            "np.random.seed(42)\n"
            "dates = pl.date_range(pl.date(2024, 1, 1), pl.date(2024, 12, 31), interval='1d', eager=True)\n"
            "df = pl.DataFrame({\n"
            "    'date':  dates,\n"
            "    'sales': np.random.normal(1000, 200, len(dates)).round(2),\n"
            "})\n\n"
            "result = df.with_columns([\n"
            "    pl.col('sales').rolling_mean(window_size=7).alias('rolling_7d'),\n"
            "    pl.col('sales').rolling_mean(window_size=30).alias('rolling_30d'),\n"
            "    pl.col('sales').rolling_std(window_size=7).alias('rolling_std_7d'),\n"
            "    pl.col('sales').cum_sum().alias('cumulative_sales'),\n"
            "    pl.col('sales').rolling_max(window_size=7).alias('rolling_max_7d'),\n"
            "])\n"
            "print(result.head(35).tail(5))\n"
            "print(f'\\nTotal annual sales: {result[\"cumulative_sales\"][-1]:,.0f}')\n"
            "print(f'Peak 7-day avg: {result[\"rolling_7d\"].max():,.1f}')"
        ),
        "code2_title": "Rank and Dense Rank",
        "code2": (
            "import polars as pl\nimport numpy as np\n\n"
            "np.random.seed(0)\n"
            "df = pl.DataFrame({\n"
            "    'product':  np.random.choice(['A','B','C','D','E'], 50),\n"
            "    'region':   np.random.choice(['North','South','East'], 50),\n"
            "    'revenue':  np.random.exponential(1000, 50).round(2),\n"
            "})\n\n"
            "# Global rank\n"
            "ranked = df.with_columns([\n"
            "    pl.col('revenue').rank(method='dense', descending=True).alias('global_rank'),\n"
            "])\n\n"
            "# Rank within region\n"
            "regional = df.with_columns([\n"
            "    pl.col('revenue').rank(method='dense', descending=True)\n"
            "      .over('region').alias('region_rank'),\n"
            "    pl.col('revenue').rank(method='ordinal', descending=True)\n"
            "      .over('region').alias('region_ordinal_rank'),\n"
            "])\n\n"
            "print('Top 5 by revenue with global rank:')\n"
            "print(ranked.sort('global_rank').head())\n"
            "print('\\nTop 3 per region:')\n"
            "print(regional.filter(pl.col('region_rank') <= 3).sort(['region','region_rank']))"
        ),
        "code3_title": "Group-wise Aggregations with over()",
        "code3": (
            "import polars as pl\nimport numpy as np\n\n"
            "np.random.seed(42)\n"
            "n = 200\n"
            "df = pl.DataFrame({\n"
            "    'employee': [f'emp_{i}' for i in range(n)],\n"
            "    'dept':     np.random.choice(['Engineering','Marketing','Sales','HR'], n),\n"
            "    'salary':   np.random.normal(80000, 20000, n).round(0),\n"
            "    'yrs_exp':  np.random.randint(1, 20, n),\n"
            "})\n\n"
            "result = df.with_columns([\n"
            "    pl.col('salary').mean().over('dept').alias('dept_avg_salary'),\n"
            "    pl.col('salary').rank(method='dense', descending=True).over('dept').alias('dept_rank'),\n"
            "    (pl.col('salary') - pl.col('salary').mean().over('dept')).alias('salary_vs_dept_avg'),\n"
            "    pl.len().over('dept').alias('dept_size'),\n"
            "])\n\n"
            "print('Employees earning above dept average:')\n"
            "above_avg = result.filter(pl.col('salary_vs_dept_avg') > 0)\n"
            "print(above_avg.sort('dept').select(['employee','dept','salary','dept_avg_salary','dept_rank']).head(8))"
        ),
        "code4_title": "Shift & Lag Features for Time Series",
        "code4": (
            "import polars as pl\nimport numpy as np\n\n"
            "np.random.seed(7)\n"
            "dates = pl.date_range(pl.date(2024, 1, 1), pl.date(2024, 6, 30), interval='1d', eager=True)\n"
            "stocks = ['AAPL', 'GOOG']\n"
            "all_dfs = []\n"
            "for stock in stocks:\n"
            "    prices = 150 + np.cumsum(np.random.randn(len(dates)) * 2)\n"
            "    all_dfs.append(pl.DataFrame({'date': dates, 'stock': stock, 'close': prices.round(2)}))\n"
            "df = pl.concat(all_dfs).sort(['stock', 'date'])\n\n"
            "result = df.with_columns([\n"
            "    pl.col('close').shift(1).over('stock').alias('prev_close'),\n"
            "    pl.col('close').shift(7).over('stock').alias('close_7d_ago'),\n"
            "    pl.col('close').pct_change().over('stock').alias('daily_return'),\n"
            "    pl.col('close').rolling_mean(window_size=5).over('stock').alias('ma5'),\n"
            "    pl.col('close').rolling_mean(window_size=20).over('stock').alias('ma20'),\n"
            "])\n"
            "print(result.filter(pl.col('stock') == 'AAPL').tail(5))"
        ),
        "rw_scenario": "Compute a 30-day rolling average revenue and day-over-day growth rate per product category for a retail dashboard. Also rank categories within each month by revenue.",
        "rw_code": (
            "import polars as pl\nimport numpy as np\n\n"
            "np.random.seed(42)\n"
            "dates = pl.date_range(pl.date(2024, 1, 1), pl.date(2024, 12, 31), interval='1d', eager=True)\n"
            "cats  = ['Electronics', 'Clothing', 'Food']\n"
            "frames = []\n"
            "for cat in cats:\n"
            "    revenue = 5000 + np.cumsum(np.random.randn(len(dates)) * 200)\n"
            "    frames.append(pl.DataFrame({'date': dates, 'category': cat, 'revenue': revenue.round(2)}))\n"
            "df = pl.concat(frames).sort(['category','date'])\n\n"
            "result = df.with_columns([\n"
            "    pl.col('revenue').rolling_mean(window_size=30).over('category').alias('ma30'),\n"
            "    pl.col('revenue').pct_change().over('category').alias('dod_growth'),\n"
            "    pl.col('date').dt.month().alias('month'),\n"
            "])\n"
            "monthly = (\n"
            "    result\n"
            "    .group_by(['month','category'])\n"
            "    .agg(pl.col('revenue').sum().alias('monthly_rev'))\n"
            "    .with_columns(\n"
            "        pl.col('monthly_rev').rank(method='dense', descending=True).over('month').alias('rank')\n"
            "    )\n"
            "    .sort(['month','rank'])\n"
            ")\n"
            "print(monthly.head(9))"
        ),
        "practice": {
            "title": "Sales KPI Dashboard with Window Functions",
            "desc": "Given daily sales data for 5 products over 6 months, compute for each product: (1) 7-day and 30-day rolling averages, (2) week-over-week growth rate using shift(7), (3) cumulative sales, (4) rank within each week by daily sales. Output a summary showing each product's peak day and best weekly rank.",
            "starter": (
                "import polars as pl\nimport numpy as np\n\n"
                "np.random.seed(42)\n"
                "dates = pl.date_range(pl.date(2024, 1, 1), pl.date(2024, 6, 30), interval='1d', eager=True)\n"
                "prods = ['alpha','beta','gamma','delta','epsilon']\n"
                "frames = []\n"
                "for p in prods:\n"
                "    sales = np.abs(np.random.normal(500, 150, len(dates)))\n"
                "    frames.append(pl.DataFrame({'date': dates, 'product': p, 'sales': sales.round(2)}))\n"
                "df = pl.concat(frames).sort(['product','date'])\n\n"
                "# TODO: Add 7d and 30d rolling means per product\n"
                "# TODO: Add wow_growth = (sales - shift(7)) / shift(7) per product\n"
                "# TODO: Add cumulative sales per product\n"
                "# TODO: Add weekly rank within each week per product\n"
                "# TODO: Print peak day and best rank for each product\n"
            ),
        },
    },
    {
        "title": "Performance Tuning",
        "desc": "Maximize Polars performance through parallelism settings, predicate pushdown, schema optimization, and benchmarking against pandas.",
        "code1_title": "Polars vs Pandas Benchmark",
        "code1": (
            "import polars as pl\nimport pandas as pd\nimport numpy as np\nimport time\n\n"
            "np.random.seed(42)\n"
            "n = 1_000_000\n"
            "data = {\n"
            "    'id':       np.random.randint(1, 10000, n),\n"
            "    'category': np.random.choice(['A','B','C','D','E'], n),\n"
            "    'value':    np.random.randn(n) * 100,\n"
            "    'qty':      np.random.randint(1, 50, n),\n"
            "}\n\n"
            "df_pd = pd.DataFrame(data)\n"
            "df_pl = pl.DataFrame(data)\n\n"
            "def bench(fn, name, reps=3):\n"
            "    times = []\n"
            "    for _ in range(reps):\n"
            "        t0 = time.perf_counter()\n"
            "        fn()\n"
            "        times.append(time.perf_counter() - t0)\n"
            "    print(f'{name:<30} {min(times)*1000:.1f}ms (best of {reps})')\n\n"
            "bench(lambda: df_pd.groupby('category')['value'].agg(['mean','sum','std']), 'Pandas groupby')\n"
            "bench(lambda: df_pl.group_by('category').agg(pl.col('value').mean(), pl.col('value').sum(), pl.col('value').std()), 'Polars groupby')\n\n"
            "bench(lambda: df_pd.sort_values('value'), 'Pandas sort')\n"
            "bench(lambda: df_pl.sort('value'), 'Polars sort')"
        ),
        "code2_title": "Schema Optimization & Categorical Encoding",
        "code2": (
            "import polars as pl\nimport numpy as np\n\n"
            "np.random.seed(42)\n"
            "n = 500_000\n"
            "# Default dtype inference\n"
            "df_default = pl.DataFrame({\n"
            "    'user_id':  np.random.randint(1, 10000, n),\n"
            "    'country':  np.random.choice(['US','UK','DE','FR','JP'], n),\n"
            "    'product':  np.random.choice([f'prod_{i}' for i in range(100)], n),\n"
            "    'revenue':  np.random.exponential(50, n),\n"
            "    'quantity': np.random.randint(1, 20, n),\n"
            "})\n\n"
            "# Optimized dtypes\n"
            "df_opt = df_default.with_columns([\n"
            "    pl.col('user_id').cast(pl.UInt32),\n"
            "    pl.col('country').cast(pl.Categorical),\n"
            "    pl.col('product').cast(pl.Categorical),\n"
            "    pl.col('revenue').cast(pl.Float32),\n"
            "    pl.col('quantity').cast(pl.UInt8),\n"
            "])\n\n"
            "def mem_mb(df): return df.estimated_size('mb')\n\n"
            "print(f'Default schema: {mem_mb(df_default):.1f} MB')\n"
            "print(f'Optimized schema: {mem_mb(df_opt):.1f} MB')\n"
            "print(f'Reduction: {(1 - mem_mb(df_opt)/mem_mb(df_default))*100:.0f}%')\n"
            "print('\\nOptimized schema:')\n"
            "print(df_opt.schema)"
        ),
        "code3_title": "Parallelism & Thread Control",
        "code3": (
            "import polars as pl\nimport numpy as np\nimport time\n\n"
            "print(f'Polars version: {pl.__version__}')\n"
            "print(f'Available threads: {pl.thread_pool_size()}')\n\n"
            "np.random.seed(0)\n"
            "n = 2_000_000\n"
            "df = pl.DataFrame({\n"
            "    'g': np.random.randint(0, 100, n),\n"
            "    'v': np.random.randn(n),\n"
            "})\n\n"
            "# Polars uses multiple threads automatically\n"
            "# Demonstrate with a complex query\n"
            "t0 = time.perf_counter()\n"
            "result = (\n"
            "    df.lazy()\n"
            "    .group_by('g')\n"
            "    .agg([\n"
            "        pl.col('v').mean().alias('mean'),\n"
            "        pl.col('v').std().alias('std'),\n"
            "        pl.col('v').quantile(0.25).alias('q25'),\n"
            "        pl.col('v').quantile(0.75).alias('q75'),\n"
            "        pl.col('v').max() - pl.col('v').min(),\n"
            "    ])\n"
            "    .collect()\n"
            ")\n"
            "t = time.perf_counter() - t0\n"
            "print(f'\\n{n:,} rows, 100 groups, 5 aggs: {t*1000:.1f}ms')\n"
            "print(result.head())"
        ),
        "code4_title": "Predicate Pushdown & Column Pruning",
        "code4": (
            "import polars as pl\nimport numpy as np\n\n"
            "np.random.seed(42)\n"
            "n = 1_000_000\n"
            "df = pl.DataFrame({\n"
            "    'id':       np.arange(n),\n"
            "    'region':   np.random.choice(['NA','EU','APAC'], n),\n"
            "    'product':  np.random.choice(['A','B','C','D'], n),\n"
            "    'revenue':  np.random.exponential(200, n),\n"
            "    'cost':     np.random.exponential(80, n),\n"
            "    'quantity': np.random.randint(1, 100, n),\n"
            "    'discount': np.random.uniform(0, 0.3, n),\n"
            "})\n\n"
            "# Without optimization hints (eager)\n"
            "# Polars lazy plan shows predicate/column pushdown\n"
            "lf = df.lazy()\n"
            "plan = (\n"
            "    lf\n"
            "    .filter(pl.col('region') == 'EU')\n"
            "    .select(['product', 'revenue', 'quantity'])\n"
            "    .group_by('product')\n"
            "    .agg(\n"
            "        pl.col('revenue').sum().alias('total_rev'),\n"
            "        pl.col('quantity').mean().alias('avg_qty'),\n"
            "    )\n"
            ")\n"
            "print('Optimized query plan:')\n"
            "print(plan.explain(optimized=True))\n"
            "result = plan.collect()\n"
            "print('\\nResult:')\n"
            "print(result.sort('total_rev', descending=True))"
        ),
        "rw_scenario": "Optimize a slow daily analytics pipeline that reads a 10GB transaction CSV, computes 15 aggregations per region/product combination, and takes 4 hours. Use Polars lazy evaluation, schema optimization, and predicate pushdown to achieve sub-minute execution.",
        "rw_code": (
            "import polars as pl\nimport numpy as np\nimport time\n\n"
            "np.random.seed(0)\n"
            "n = 2_000_000\n"
            "df = pl.DataFrame({\n"
            "    'region':   np.random.choice(['NA','EU','APAC','LATAM'], n),\n"
            "    'product':  np.random.choice([f'p{i}' for i in range(50)], n),\n"
            "    'revenue':  np.random.exponential(100, n),\n"
            "    'cost':     np.random.exponential(40, n),\n"
            "    'quantity': np.random.randint(1, 100, n),\n"
            "    'returned': np.random.choice([True, False], n, p=[0.05, 0.95]),\n"
            "}).with_columns([\n"
            "    pl.col('region').cast(pl.Categorical),\n"
            "    pl.col('product').cast(pl.Categorical),\n"
            "    pl.col('revenue').cast(pl.Float32),\n"
            "    pl.col('cost').cast(pl.Float32),\n"
            "    pl.col('quantity').cast(pl.UInt16),\n"
            "])\n\n"
            "t0 = time.perf_counter()\n"
            "result = (\n"
            "    df.lazy()\n"
            "    .filter(~pl.col('returned'))\n"
            "    .group_by(['region', 'product'])\n"
            "    .agg([\n"
            "        pl.col('revenue').sum().alias('total_revenue'),\n"
            "        pl.col('cost').sum().alias('total_cost'),\n"
            "        pl.col('quantity').sum().alias('total_qty'),\n"
            "        (pl.col('revenue') - pl.col('cost')).mean().alias('avg_margin'),\n"
            "        pl.len().alias('transactions'),\n"
            "    ])\n"
            "    .with_columns((pl.col('total_revenue') - pl.col('total_cost')).alias('profit'))\n"
            "    .sort('profit', descending=True)\n"
            "    .collect()\n"
            ")\n"
            "t = time.perf_counter() - t0\n"
            "print(f'{n:,} rows processed in {t:.2f}s')\n"
            "print(result.head(5))"
        ),
        "practice": {
            "title": "Optimize a Slow Polars Pipeline",
            "desc": "Given a 1M-row DataFrame with columns (user_id, country, product, revenue, cost), write two versions of the same query: (1) eager, (2) lazy with schema optimization (cast categoricals, float32). The query: filter out cost>revenue rows, group by country+product, compute total profit and count. Benchmark both and report speedup.",
            "starter": (
                "import polars as pl\nimport numpy as np\nimport time\n\n"
                "np.random.seed(42)\n"
                "n = 1_000_000\n"
                "raw = pl.DataFrame({\n"
                "    'user_id': np.random.randint(1, 10000, n),\n"
                "    'country': np.random.choice(['US','UK','DE','FR'], n),\n"
                "    'product': np.random.choice([f'p{i}' for i in range(20)], n),\n"
                "    'revenue': np.random.exponential(100, n),\n"
                "    'cost':    np.random.exponential(60, n),\n"
                "})\n\n"
                "# TODO: (1) Eager version - filter, group_by, agg\n"
                "# TODO: (2) Lazy version with schema optimization\n"
                "# TODO: Benchmark both with time.perf_counter()\n"
                "# TODO: Print speedup ratio\n"
            ),
        },
    },
    {
        "title": "14. Polars LazyFrame & Streaming Optimization",
        "desc": "LazyFrame enables query optimization through predicate pushdown, projection pushdown, and streaming execution. Build full pipelines before calling .collect() to let Polars optimize the execution plan.",
        "code1_title": "LazyFrame with Query Plan Inspection",
        "code1": (
            "import polars as pl\n"
            "import numpy as np\n"
            "np.random.seed(0)\n"
            "n = 1_000_000\n"
            "# Build large lazy dataset\n"
            "lf = (\n"
            "    pl.LazyFrame({\n"
            "        \"id\":       np.arange(n),\n"
            "        \"category\": np.random.choice([\"A\",\"B\",\"C\",\"D\"], n),\n"
            "        \"value\":    np.random.normal(100, 20, n),\n"
            "        \"weight\":   np.random.uniform(0.5, 2.0, n),\n"
            "    })\n"
            "    .filter(pl.col(\"value\") > 60)\n"
            "    .with_columns([\n"
            "        (pl.col(\"value\") * pl.col(\"weight\")).alias(\"weighted_value\"),\n"
            "        pl.col(\"category\").cast(pl.Categorical),\n"
            "    ])\n"
            "    .group_by(\"category\")\n"
            "    .agg([\n"
            "        pl.col(\"weighted_value\").mean().alias(\"mean_wv\"),\n"
            "        pl.col(\"value\").std().alias(\"std_val\"),\n"
            "        pl.col(\"id\").count().alias(\"n\"),\n"
            "    ])\n"
            "    .sort(\"mean_wv\", descending=True)\n"
            ")\n"
            "# Show the query plan\n"
            "print(\"Query plan:\")\n"
            "print(lf.explain())\n"
            "result = lf.collect()\n"
            "print(result)\n"
        ),
        "code2_title": "Streaming Parquet Processing",
        "code2": (
            "import polars as pl\n"
            "import numpy as np\n"
            "np.random.seed(1)\n"
            "n = 500_000\n"
            "# Streaming scan simulation: process in chunks\n"
            "df = pl.DataFrame({\n"
            "    \"user_id\":   np.random.randint(1, 1000, n),\n"
            "    \"revenue\":   np.random.lognormal(3, 1, n),\n"
            "    \"product\":   np.random.choice([\"X\",\"Y\",\"Z\"], n),\n"
            "    \"is_premium\":np.random.randint(0, 2, n).astype(bool),\n"
            "})\n"
            "# Save and reload to test scan_parquet streaming\n"
            "import tempfile, os\n"
            "tmp = tempfile.mktemp(suffix=\".parquet\")\n"
            "df.write_parquet(tmp)\n"
            "# Streaming aggregation from parquet\n"
            "result = (\n"
            "    pl.scan_parquet(tmp)\n"
            "    .filter(pl.col(\"is_premium\"))\n"
            "    .group_by(\"product\")\n"
            "    .agg([\n"
            "        pl.col(\"revenue\").sum().alias(\"total_rev\"),\n"
            "        pl.col(\"user_id\").n_unique().alias(\"unique_users\"),\n"
            "        pl.col(\"revenue\").mean().alias(\"avg_rev\"),\n"
            "    ])\n"
            "    .sort(\"total_rev\", descending=True)\n"
            "    .collect(streaming=True)\n"
            ")\n"
            "os.unlink(tmp)\n"
            "print(result)\n"
        ),
        "code3_title": "Lazy vs Eager Benchmark",
        "code3": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import time\n"
            "np.random.seed(42)\n"
            "n = 200_000\n"
            "df = pl.DataFrame({\n"
            "    \"id\":    np.arange(n),\n"
            "    \"x\":     np.random.randn(n),\n"
            "    \"group\": np.random.choice([f\"G{i}\" for i in range(50)], n),\n"
            "})\n"
            "# Pattern 1: inefficient (multiple passes)\n"
            "t0 = time.perf_counter()\n"
            "for _ in range(3):\n"
            "    _ = df.filter(pl.col(\"x\") > 0).group_by(\"group\").agg(pl.col(\"x\").mean())\n"
            "t1 = time.perf_counter()\n"
            "# Pattern 2: single lazy pass with predicate pushdown\n"
            "t2 = time.perf_counter()\n"
            "for _ in range(3):\n"
            "    _ = (pl.LazyFrame(df)\n"
            "         .filter(pl.col(\"x\") > 0)\n"
            "         .group_by(\"group\")\n"
            "         .agg(pl.col(\"x\").mean())\n"
            "         .collect())\n"
            "t3 = time.perf_counter()\n"
            "print(f\"Eager repeated passes: {(t1-t0)*1000:.1f} ms\")\n"
            "print(f\"LazyFrame with pushdown: {(t3-t2)*1000:.1f} ms\")\n"
        ),
        "rw_scenario": "E-commerce analytics: process 10M order records from Parquet using LazyFrame with streaming=True to compute revenue by product category without loading all data into memory.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import tempfile, os\n"
            "np.random.seed(0)\n"
            "n = 500_000\n"
            "df = pl.DataFrame({\n"
            "    \"order_id\":  np.arange(n),\n"
            "    \"category\":  np.random.choice([\"Electronics\",\"Clothing\",\"Food\",\"Sports\",\"Books\"], n),\n"
            "    \"revenue\":   np.random.lognormal(4, 1, n),\n"
            "    \"is_returned\":np.random.binomial(1, 0.05, n).astype(bool),\n"
            "    \"customer_tier\":np.random.choice([\"gold\",\"silver\",\"bronze\"], n),\n"
            "})\n"
            "tmp = tempfile.mktemp(suffix=\".parquet\")\n"
            "df.write_parquet(tmp)\n"
            "result = (\n"
            "    pl.scan_parquet(tmp)\n"
            "    .filter(~pl.col(\"is_returned\"))\n"
            "    .group_by([\"category\",\"customer_tier\"])\n"
            "    .agg([\n"
            "        pl.col(\"revenue\").sum().alias(\"total_rev\"),\n"
            "        pl.col(\"revenue\").mean().alias(\"avg_rev\"),\n"
            "        pl.col(\"order_id\").count().alias(\"n_orders\"),\n"
            "    ])\n"
            "    .sort(\"total_rev\", descending=True)\n"
            "    .collect(streaming=True)\n"
            ")\n"
            "os.unlink(tmp)\n"
            "print(result.head(8))\n"
        ),
        "practice": {
            "title": "Fraud Transaction Pipeline",
            "desc": "Process 2M transaction records with LazyFrame: filter frauds, group by category+day_of_week, compute aggregate metrics. Show the query plan, benchmark eager vs lazy, and use streaming=True for collect. Save results to parquet and verify.",
            "starter": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import time\n"
            "np.random.seed(7)\n"
            "n = 2_000_000\n"
            "df = pl.DataFrame({\n"
            "    \"transaction_id\": np.arange(n),\n"
            "    \"customer_id\":    np.random.randint(1, 10000, n),\n"
            "    \"amount\":         np.random.lognormal(4, 1, n),\n"
            "    \"category\":       np.random.choice([\"food\",\"travel\",\"retail\",\"tech\",\"health\"], n),\n"
            "    \"is_fraud\":       np.random.binomial(1, 0.02, n).astype(bool),\n"
            "    \"day_of_week\":    np.random.randint(0, 7, n),\n"
            "})\n"
            "# TODO: Use LazyFrame to filter fraud transactions, group by category+day_of_week\n"
            "# TODO: Compute: sum(amount), count, fraud_rate per group\n"
            "# TODO: Show query plan with .explain()\n"
            "# TODO: Compare timing: eager vs lazy with collect(streaming=True)\n"
            "# TODO: Save result to parquet, reload with scan_parquet and verify row count\n"
            "\n"
        ),
        },
    },
    {
        "title": "15. Time Series Operations in Polars",
        "desc": "Polars provides high-performance time series operations: rolling aggregations, resampling with group_by_dynamic, and lag/shift features. Temporal operations run significantly faster than pandas for large datasets.",
        "code1_title": "Rolling Statistics & Time Features",
        "code1": (
            "import polars as pl\n"
            "import numpy as np\n"
            "np.random.seed(0)\n"
            "n = 1000\n"
            "dates = pl.date_range(\n"
            "    pl.date(2022, 1, 1), pl.date(2024, 9, 26), interval=\"1d\", eager=True\n"
            ")[:n]\n"
            "df = pl.DataFrame({\n"
            "    \"date\":  dates,\n"
            "    \"value\": 100 + np.cumsum(np.random.normal(0, 1, n)),\n"
            "    \"volume\":np.random.poisson(1000, n).astype(float),\n"
            "})\n"
            "result = (\n"
            "    df.with_columns([\n"
            "        pl.col(\"date\").dt.year().alias(\"year\"),\n"
            "        pl.col(\"date\").dt.month().alias(\"month\"),\n"
            "        pl.col(\"date\").dt.weekday().alias(\"dow\"),\n"
            "        pl.col(\"value\").rolling_mean(window_size=7).alias(\"ma7\"),\n"
            "        pl.col(\"value\").rolling_mean(window_size=30).alias(\"ma30\"),\n"
            "        pl.col(\"value\").pct_change().alias(\"return_1d\"),\n"
            "    ])\n"
            "    .filter(pl.col(\"ma7\").is_not_null())\n"
            ")\n"
            "print(result.select([\"date\",\"value\",\"ma7\",\"ma30\",\"return_1d\"]).head(5))\n"
            "print(result.select(pl.col(\"return_1d\").std()).item())\n"
        ),
        "code2_title": "Resampling: Weekly & Monthly OHLC",
        "code2": (
            "import polars as pl\n"
            "import numpy as np\n"
            "np.random.seed(1)\n"
            "n = 500\n"
            "dates = pl.date_range(pl.date(2023,1,1), pl.date(2024,5,14), interval=\"1d\", eager=True)[:n]\n"
            "df = pl.DataFrame({\n"
            "    \"date\":  dates,\n"
            "    \"price\": 50 + np.cumsum(np.random.normal(0, 0.5, n)),\n"
            "})\n"
            "# Resample to weekly and monthly\n"
            "weekly = (\n"
            "    df.group_by_dynamic(\"date\", every=\"1w\")\n"
            "    .agg([\n"
            "        pl.col(\"price\").first().alias(\"open\"),\n"
            "        pl.col(\"price\").max().alias(\"high\"),\n"
            "        pl.col(\"price\").min().alias(\"low\"),\n"
            "        pl.col(\"price\").last().alias(\"close\"),\n"
            "        pl.col(\"price\").mean().alias(\"avg\"),\n"
            "    ])\n"
            ")\n"
            "monthly = (\n"
            "    df.group_by_dynamic(\"date\", every=\"1mo\")\n"
            "    .agg([\n"
            "        pl.col(\"price\").last().alias(\"month_close\"),\n"
            "        pl.col(\"price\").std().alias(\"monthly_vol\"),\n"
            "    ])\n"
            ")\n"
            "print(\"Weekly OHLC:\"); print(weekly.head(4))\n"
            "print(\"Monthly volatility:\"); print(monthly.head(4))\n"
        ),
        "code3_title": "Lag Features & Rolling Metrics",
        "code3": (
            "import polars as pl\n"
            "import numpy as np\n"
            "np.random.seed(2)\n"
            "n = 300\n"
            "dates = pl.date_range(pl.date(2023,1,1), pl.date(2023,10,28), interval=\"1d\", eager=True)[:n]\n"
            "df = pl.DataFrame({\n"
            "    \"date\":  dates,\n"
            "    \"value\": 100 + np.cumsum(np.random.normal(0, 1.5, n)),\n"
            "})\n"
            "result = (\n"
            "    df.with_columns([\n"
            "        pl.col(\"value\").shift(1).alias(\"lag_1\"),\n"
            "        pl.col(\"value\").shift(7).alias(\"lag_7\"),\n"
            "        pl.col(\"value\").shift(30).alias(\"lag_30\"),\n"
            "        pl.col(\"value\").rolling_std(window_size=14).alias(\"vol_14\"),\n"
            "        (pl.col(\"value\") / pl.col(\"value\").shift(1) - 1).alias(\"return_1d\"),\n"
            "        pl.col(\"value\").rolling_max(window_size=52).alias(\"rolling_high_52\"),\n"
            "        pl.col(\"value\").rolling_min(window_size=52).alias(\"rolling_low_52\"),\n"
            "    ])\n"
            "    .with_columns([\n"
            "        ((pl.col(\"value\") - pl.col(\"rolling_low_52\")) /\n"
            "         (pl.col(\"rolling_high_52\") - pl.col(\"rolling_low_52\"))).alias(\"pct_rank_52w\"),\n"
            "    ])\n"
            "    .drop_nulls()\n"
            ")\n"
            "print(result.select([\"date\",\"value\",\"lag_1\",\"vol_14\",\"pct_rank_52w\"]).tail(5))\n"
            "print(f\"Rows after dropna: {len(result)}\")\n"
        ),
        "rw_scenario": "Retail analytics: compute 7-day and 30-day rolling sales averages, detect anomalies where daily sales deviate from the 30d mean by more than 2 std, and resample to weekly totals for reporting.",
        "rw_code": (
            "import polars as pl\n"
            "import numpy as np\n"
            "np.random.seed(1)\n"
            "n = 365\n"
            "dates = pl.date_range(pl.date(2023,1,1), pl.date(2023,12,31), interval=\"1d\", eager=True)[:n]\n"
            "sales = 1000 + 200*np.sin(2*np.pi*np.arange(n)/7) + np.random.normal(0, 80, n)\n"
            "sales[100] += 800  # spike anomaly\n"
            "df = pl.DataFrame({\"date\": dates, \"sales\": sales})\n"
            "result = (\n"
            "    df.with_columns([\n"
            "        pl.col(\"sales\").rolling_mean(window_size=7).alias(\"ma7\"),\n"
            "        pl.col(\"sales\").rolling_mean(window_size=30).alias(\"ma30\"),\n"
            "        pl.col(\"sales\").rolling_std(window_size=30).alias(\"std30\"),\n"
            "    ])\n"
            "    .with_columns([\n"
            "        ((pl.col(\"sales\") - pl.col(\"ma30\")) / pl.col(\"std30\")).alias(\"z_score\"),\n"
            "    ])\n"
            "    .with_columns([\n"
            "        (pl.col(\"z_score\").abs() > 2).alias(\"anomaly\"),\n"
            "    ])\n"
            ")\n"
            "anomalies = result.filter(pl.col(\"anomaly\"))\n"
            "print(f\"Anomalies detected: {len(anomalies)}\")\n"
            "print(anomalies.select([\"date\",\"sales\",\"ma30\",\"z_score\"]))\n"
            "weekly = df.group_by_dynamic(\"date\", every=\"1w\").agg(pl.col(\"sales\").sum().alias(\"weekly_total\"))\n"
            "print(weekly.head(5))\n"
        ),
        "practice": {
            "title": "Multi-Asset Portfolio Analysis",
            "desc": "Build a 2-year daily time series for 3 simulated stocks. Add rolling 20/50-day moving averages, daily returns, and 52-week high/low metrics. Resample AAPL to weekly OHLC. Compute monthly summary statistics (avg return, volatility) for all stocks using group_by_dynamic.",
            "starter": (
            "import polars as pl\n"
            "import numpy as np\n"
            "np.random.seed(99)\n"
            "n = 730  # 2 years daily\n"
            "dates = pl.date_range(pl.date(2022,1,1), pl.date(2023,12,31), interval=\"1d\", eager=True)[:n]\n"
            "# Multi-asset time series\n"
            "df = pl.DataFrame({\n"
            "    \"date\":  dates,\n"
            "    \"AAPL\":  100 + np.cumsum(np.random.normal(0.05, 1.2, n)),\n"
            "    \"MSFT\":  200 + np.cumsum(np.random.normal(0.08, 1.5, n)),\n"
            "    \"GOOG\":  90  + np.cumsum(np.random.normal(0.03, 1.0, n)),\n"
            "})\n"
            "# TODO: Add rolling 20d and 50d MA for each stock\n"
            "# TODO: Add daily returns for each stock\n"
            "# TODO: Resample to weekly OHLC for AAPL\n"
            "# TODO: Add 52-week high/low and % distance from 52w high\n"
            "# TODO: Monthly summary: avg return and volatility per stock\n"
            "\n"
        ),
        },
    },
    {
        "title": "16. Polars with Apache Arrow & Parquet",
        "desc": "Polars is built on Apache Arrow, enabling zero-copy interop with PyArrow, DuckDB, and other Arrow-native tools. Write partitioned Parquet files for efficient partial reads in production data pipelines.",
        "code1_title": "Polars <-> PyArrow Interoperability",
        "code1": (
            "import polars as pl\n"
            "import pyarrow as pa\n"
            "import numpy as np\n"
            "np.random.seed(0)\n"
            "n = 100_000\n"
            "# Create Polars DataFrame and convert to Arrow\n"
            "df = pl.DataFrame({\n"
            "    \"id\":      np.arange(n),\n"
            "    \"score\":   np.random.randn(n),\n"
            "    \"category\":np.random.choice([\"A\",\"B\",\"C\"], n),\n"
            "    \"amount\":  np.random.lognormal(4, 1, n),\n"
            "})\n"
            "# Polars -> Arrow -> Polars (zero-copy where possible)\n"
            "arrow_table = df.to_arrow()\n"
            "print(f\"Arrow schema: {arrow_table.schema}\")\n"
            "print(f\"Num chunks: {arrow_table.column('score').num_chunks}\")\n"
            "# Compute with pyarrow\n"
            "import pyarrow.compute as pc\n"
            "mean_score = pc.mean(arrow_table.column(\"score\"))\n"
            "print(f\"Mean score via pyarrow: {mean_score.as_py():.6f}\")\n"
            "# Back to Polars\n"
            "df2 = pl.from_arrow(arrow_table)\n"
            "print(f\"Roundtrip OK: {df.shape == df2.shape}\")\n"
        ),
        "code2_title": "Parquet vs CSV: Speed & Size Benchmark",
        "code2": (
            "import polars as pl\n"
            "import numpy as np\n"
            "import tempfile, os, time\n"
            "np.random.seed(1)\n"
            "n = 500_000\n"
            "df = pl.DataFrame({\n"
            "    \"id\":       np.arange(n),\n"
            "    \"group\":    np.random.choice([\"X\",\"Y\",\"Z\",\"W\"], n),\n"
            "    \"value\":    np.random.randn(n),\n"
            "    \"amount\":   np.random.lognormal(3, 1.5, n),\n"
            "    \"flag\":     np.random.randint(0, 2, n).astype(bool),\n"
            "})\n"
            "tmp_parquet = tempfile.mktemp(suffix=\".parquet\")\n"
            "tmp_csv     = tempfile.mktemp(suffix=\".csv\")\n"
            "# Write and read Parquet vs CSV\n"
            "t0 = time.perf_counter()\n"
            "df.write_parquet(tmp_parquet, compression=\"snappy\")\n"
            "t1 = time.perf_counter()\n"
            "df.write_csv(tmp_csv)\n"
            "t2 = time.perf_counter()\n"
            "df_pq = pl.read_parquet(tmp_parquet)\n"
            "t3 = time.perf_counter()\n"
            "df_csv = pl.read_csv(tmp_csv)\n"
            "t4 = time.perf_counter()\n"
            "pq_mb  = os.path.getsize(tmp_parquet) / 1e6\n"
            "csv_mb = os.path.getsize(tmp_csv) / 1e6\n"
            "print(f\"Parquet: write={t1-t0:.3f}s read={t3-t2:.3f}s size={pq_mb:.1f}MB\")\n"
            "print(f\"CSV:     write={t2-t1:.3f}s read={t4-t3:.3f}s size={csv_mb:.1f}MB\")\n"
            "for f in [tmp_parquet, tmp_csv]: os.unlink(f)\n"
        ),
        "code3_title": "Partitioned Parquet with PyArrow + Polars scan",
        "code3": (
            "import polars as pl\n"
            "import pyarrow as pa\n"
            "import pyarrow.parquet as pq\n"
            "import numpy as np\n"
            "import tempfile, os\n"
            "np.random.seed(2)\n"
            "n = 200_000\n"
            "df = pl.DataFrame({\n"
            "    \"year\":   np.random.choice([2021,2022,2023], n),\n"
            "    \"region\": np.random.choice([\"NA\",\"EU\",\"APAC\"], n),\n"
            "    \"product\":np.random.choice([\"A\",\"B\",\"C\",\"D\"], n),\n"
            "    \"revenue\":np.random.lognormal(5, 1, n),\n"
            "    \"units\":  np.random.poisson(50, n),\n"
            "})\n"
            "# Write partitioned parquet (by year+region) via pyarrow\n"
            "arrow_table = df.to_arrow()\n"
            "tmpdir = tempfile.mkdtemp()\n"
            "pq.write_to_dataset(arrow_table, root_path=tmpdir,\n"
            "                    partition_cols=[\"year\",\"region\"])\n"
            "# Read only 2023 NA partition with Polars scan\n"
            "result = (\n"
            "    pl.scan_parquet(f\"{tmpdir}/year=2023/region=NA/**/*.parquet\")\n"
            "    .group_by(\"product\")\n"
            "    .agg(pl.col(\"revenue\").sum(), pl.col(\"units\").sum())\n"
            "    .collect()\n"
            ")\n"
            "print(f\"2023 NA partition result:\"); print(result)\n"
            "import shutil; shutil.rmtree(tmpdir)\n"
        ),
        "rw_scenario": "Data lake pipeline: store 5 years of IoT sensor readings in Parquet partitioned by year+device_type, then query a single partition with pl.scan_parquet to compute hourly aggregates without reading the full dataset.",
        "rw_code": (
            "import polars as pl\n"
            "import pyarrow as pa\n"
            "import pyarrow.parquet as pq\n"
            "import numpy as np\n"
            "import tempfile, os, shutil\n"
            "np.random.seed(5)\n"
            "n = 200_000\n"
            "df = pl.DataFrame({\n"
            "    \"year\":        np.random.choice([2021,2022,2023], n),\n"
            "    \"device_type\": np.random.choice([\"sensor\",\"camera\",\"gateway\"], n),\n"
            "    \"timestamp_h\": np.random.randint(0, 24, n),\n"
            "    \"temperature\": np.random.normal(22, 5, n),\n"
            "    \"humidity\":    np.random.normal(60, 10, n),\n"
            "    \"power_kw\":    np.random.lognormal(1, 0.5, n),\n"
            "})\n"
            "tmpdir = tempfile.mkdtemp()\n"
            "pq.write_to_dataset(df.to_arrow(), root_path=tmpdir,\n"
            "                    partition_cols=[\"year\",\"device_type\"])\n"
            "# Read only 2023 sensors\n"
            "result = (\n"
            "    pl.scan_parquet(f\"{tmpdir}/year=2023/device_type=sensor/**/*.parquet\")\n"
            "    .group_by(\"timestamp_h\")\n"
            "    .agg([\n"
            "        pl.col(\"temperature\").mean().alias(\"avg_temp\"),\n"
            "        pl.col(\"power_kw\").sum().alias(\"total_power\"),\n"
            "        pl.col(\"humidity\").std().alias(\"hum_std\"),\n"
            "    ])\n"
            "    .sort(\"timestamp_h\")\n"
            "    .collect()\n"
            ")\n"
            "print(f\"2023 sensor hourly aggregates ({len(result)} hours):\")\n"
            "print(result.head(5))\n"
            "shutil.rmtree(tmpdir)\n"
        ),
        "practice": {
            "title": "1M-Row Partitioned Analytics",
            "desc": "Write 1M rows of sales data partitioned by date+country using PyArrow. Read only the 2024 US partition with pl.scan_parquet and compute margins. Benchmark whole-file read vs partitioned scan. Convert the result to Arrow and compute gross_margin using pyarrow.compute.",
            "starter": (
            "import polars as pl\n"
            "import pyarrow as pa\n"
            "import pyarrow.parquet as pq\n"
            "import numpy as np\n"
            "import tempfile, os, time\n"
            "np.random.seed(33)\n"
            "n = 1_000_000\n"
            "df = pl.DataFrame({\n"
            "    \"date\":       np.random.choice([\"2022\",\"2023\",\"2024\"], n),\n"
            "    \"country\":    np.random.choice([\"US\",\"UK\",\"DE\",\"FR\",\"JP\"], n),\n"
            "    \"category\":   np.random.choice([\"A\",\"B\",\"C\",\"D\",\"E\"], n),\n"
            "    \"sales\":      np.random.lognormal(4, 1.5, n),\n"
            "    \"cost\":       np.random.lognormal(3.5, 1.2, n),\n"
            "    \"units\":      np.random.poisson(100, n),\n"
            "})\n"
            "# TODO: Write partitioned parquet by date+country using pyarrow\n"
            "# TODO: Read only 2024 US partition using pl.scan_parquet\n"
            "# TODO: Compute: total sales, total cost, margin, units per category for 2024 US\n"
            "# TODO: Benchmark: read whole parquet vs partitioned scan for single partition\n"
            "# TODO: Convert to Arrow table and compute gross_margin with pyarrow.compute\n"
            "\n"
        ),
        },
    },

]


def make_html(sections):
    cards = ""
    nav_links = ""
    for i, s in enumerate(sections):
        sid = f"s{i}"
        nav_links += f'<a href="#{sid}">{s["title"]}</a>\n'
        if s.get("code3_title"):
            code3_html = (
                f'<h4>{s["code3_title"]}</h4>'
                f'<div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>'
                f'<pre><code class="language-python">{s["code3"]}</code></pre></div>'
            )
        else:
            code3_html = ""
        if s.get("code4_title"):
            code4_html = (
                f'<h4>{s["code4_title"]}</h4>'
                f'<div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>'
                f'<pre><code class="language-python">{s["code4"]}</code></pre></div>'
            )
        else:
            code4_html = ""
        practice = s.get("practice", {})
        if practice:
            pid = f"p{i}"
            practice_html = (
                f'<div class="practice">'
                f'<div class="ph">&#x1F3CB;&#xFE0F; Practice: {practice["title"]}</div>'
                f'<div class="pd">{practice["desc"]}</div>'
                f'<div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>'
                f'<pre><code id="{pid}" class="language-python">{practice["starter"]}</code></pre></div>'
                f'</div>'
            )
        else:
            practice_html = ""
        cards += f"""
<div class="card" id="{sid}">
  <div class="card-header" onclick="toggle('{sid}')">
    <span>{i+1}. {s["title"]}</span>
    <span class="arrow" id="arr-{sid}">&#9654;</span>
  </div>
  <div class="card-body" id="body-{sid}" style="display:none">
    <p class="desc">{s["desc"]}</p>
    <h4>{s["code1_title"]}</h4>
    <div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>
    <pre><code class="language-python">{s["code1"]}</code></pre></div>
    <h4>{s["code2_title"]}</h4>
    <div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>
    <pre><code class="language-python">{s["code2"]}</code></pre></div>
    {code3_html}
    {code4_html}
    <div class="rw">
      <div class="rh">Real-World Use Case</div>
      <div class="rd">{s["rw_scenario"]}</div>
      <div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>
      <pre><code class="language-python">{s["rw_code"]}</code></pre></div>
    </div>
    {practice_html}
  </div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Polars Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{{--accent:{ACCENT};--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;display:flex;min-height:100vh;}}
nav{{width:240px;min-height:100vh;background:var(--card);border-right:1px solid var(--border);padding:20px 0;position:sticky;top:0;overflow-y:auto;flex-shrink:0;}}
nav h2{{padding:0 16px 12px;font-size:.85rem;color:var(--accent);text-transform:uppercase;letter-spacing:.08em;}}
nav input{{width:calc(100% - 32px);margin:0 16px 12px;padding:6px 10px;background:#0d1117;border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:.8rem;}}
nav a{{display:block;padding:6px 16px;color:var(--muted);text-decoration:none;font-size:.82rem;border-left:2px solid transparent;transition:.2s;}}
nav a:hover{{color:var(--accent);border-left-color:var(--accent);background:rgba(205,139,0,.07);}}
main{{flex:1;padding:32px;max-width:900px;}}
header{{margin-bottom:32px;}}
header h1{{font-size:2rem;font-weight:700;}}
header h1 span{{color:var(--accent);}}
header p{{color:var(--muted);margin-top:6px;}}
.badge{{display:inline-block;padding:3px 10px;border-radius:20px;font-size:.75rem;font-weight:600;background:rgba(205,139,0,.15);color:var(--accent);border:1px solid rgba(205,139,0,.3);margin-top:8px;}}
.card{{border:1px solid var(--border);border-radius:10px;margin-bottom:16px;overflow:hidden;}}
.card-header{{padding:14px 18px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;background:var(--card);font-weight:600;transition:.2s;}}
.card-header:hover{{background:#1c2128;color:var(--accent);}}
.arrow{{transition:transform .25s;color:var(--accent);}}
.card-body{{padding:18px;background:#0d1117;border-top:1px solid var(--border);}}
.desc{{color:var(--muted);margin-bottom:14px;line-height:1.6;}}
h4{{font-size:.85rem;color:var(--accent);margin:14px 0 6px;text-transform:uppercase;letter-spacing:.06em;}}
.code-wrap{{position:relative;border-radius:8px;overflow:hidden;margin-bottom:12px;}}
pre{{margin:0;overflow-x:auto;}}
pre code{{font-size:.82rem;padding:14px!important;}}
.copy-btn{{position:absolute;top:6px;right:6px;padding:3px 10px;background:#30363d;color:#e6edf3;border:none;border-radius:5px;font-size:.72rem;cursor:pointer;z-index:10;}}
.copy-btn:hover{{background:var(--accent);color:#000;}}
.rw{{background:rgba(205,139,0,.06);border:1px solid rgba(205,139,0,.25);border-radius:8px;padding:14px;margin-top:16px;}}
.rh{{font-weight:700;color:var(--accent);margin-bottom:6px;font-size:.85rem;}}
.rd{{color:var(--muted);margin-bottom:10px;font-size:.85rem;line-height:1.5;}}
.practice{{background:#0d1b2a;border:1px solid #388bfd;border-radius:8px;padding:14px;margin-top:16px;}}
.ph{{font-weight:700;color:#58a6ff;margin-bottom:6px;font-size:.85rem;}}
.pd{{color:#79c0ff;font-size:.84rem;margin-bottom:10px;line-height:1.5;}}
@media(max-width:700px){{nav{{display:none;}}main{{padding:16px;}}}}
</style>
</head>
<body>
<nav>
  <h2>Polars</h2>
  <input type="text" id="search" placeholder="Search topics..." oninput="filterNav(this.value)">
  {nav_links}
</nav>
<main>
<header>
  <h1>Po<span>lars</span> Study Guide</h1>
  <p>Blazing-fast DataFrame library — Rust-powered, lazy execution, built for big data.</p>
  <span class="badge">10 Topics &bull; High-Performance DataFrames</span>
</header>
{cards}
</main>
<script>
hljs.highlightAll();
function toggle(id){{
  var b=document.getElementById('body-'+id),a=document.getElementById('arr-'+id);
  if(b.style.display==='none'){{b.style.display='block';a.style.transform='rotate(90deg)';}}
  else{{b.style.display='none';a.style.transform='';}}
}}
function copyCode(btn){{
  var code=btn.nextElementSibling.querySelector('code');
  navigator.clipboard.writeText(code.innerText).then(function(){{
    btn.textContent='Copied!';setTimeout(function(){{btn.textContent='Copy';}},1500);
  }});
}}
function filterNav(q){{
  document.querySelectorAll('nav a').forEach(function(a){{
    a.style.display=a.textContent.toLowerCase().includes(q.toLowerCase())?'block':'none';
  }});
}}
</script>
</body>
</html>"""


def make_nb(sections):
    cells = []

    def md(src):
        return {"cell_type": "markdown", "metadata": {}, "source": [src]}

    def code(src):
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [src],
        }

    cells.append(md("# Polars Study Guide\n\nBlazing-fast DataFrame library — Rust-powered, lazy execution, built for big data.\n\n**Topics:** Setup, Select & Expressions, Filter & Sort, GroupBy, Joins, String & Date Ops, Lazy API, File I/O, Window Functions, Polars vs Pandas"))

    for s in sections:
        cells.append(md(f"## {s['title']}\n\n{s['desc']}"))
        cells.append(md(f"### {s['code1_title']}"))
        cells.append(code(s["code1"]))
        cells.append(md(f"### {s['code2_title']}"))
        cells.append(code(s["code2"]))
        if s.get("code3_title"):
            cells.append(md(f"### {s['code3_title']}"))
            cells.append(code(s["code3"]))
        if s.get("code4_title"):
            cells.append(md(f"### {s['code4_title']}"))
            cells.append(code(s["code4"]))
        cells.append(md(f"### Real-World Use Case\n\n**Scenario:** {s['rw_scenario']}"))
        cells.append(code(s["rw_code"]))
        practice = s.get("practice")
        if practice:
            cells.append(md(f"### Practice: {practice['title']}\n\n{practice['desc']}"))
            cells.append(code(practice["starter"]))

    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.0"},
        },
        "cells": cells,
    }


os.makedirs(OUT, exist_ok=True)
html_path = os.path.join(OUT, "index.html")
nb_path = os.path.join(OUT, "study_guide.ipynb")

html = make_html(SECTIONS)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

nb = make_nb(SECTIONS)
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

nb_cells = len(nb["cells"])
html_kb = os.path.getsize(html_path) / 1024
print(f"Polars guide created: {OUT}")
print(f"  index.html:        {html_kb:.1f} KB")
print(f"  study_guide.ipynb: {nb_cells} cells")
