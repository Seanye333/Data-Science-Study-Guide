"""Add SQL sections 25-32 to gen_sql.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _inserter import insert_sections

FILE   = pathlib.Path(__file__).parent / "gen_sql.py"
MARKER = "]  # end SECTIONS"

SETUP = (
    "import sqlite3, contextlib\\n"
    "conn = sqlite3.connect(':memory:')\\n"
    "conn.execute('PRAGMA journal_mode=WAL')\\n"
    "def run(sql, params=()):\\n"
    "    with contextlib.closing(conn.cursor()) as cur:\\n"
    "        cur.execute(sql, params)\\n"
    "        if cur.description:\\n"
    "            return cur.fetchall()\\n"
    "        conn.commit()\\n"
    "        return cur.rowcount\\n"
    "def runmany(sql, rows):\\n"
    "    with contextlib.closing(conn.cursor()) as cur:\\n"
    "        cur.executemany(sql, rows)\\n"
    "        conn.commit()\\n"
)

def ec(s):
    return (s.replace('\\','\\\\').replace('"','\\"')
             .replace('\n','\\n').replace("'","\\'"))

def make_sql(num, title, desc, examples, rw_title, rw_scenario, rw_code, pt, pd_text, ps):
    ex_lines = []
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples) - 1 else ''
        ex_lines.append(
            f'        {{"label": "{ec(ex["label"])}", "code": "{ec(ex["code"])}"}}{comma}'
        )
    ex_block = '\n'.join(ex_lines)
    return (
        f'{{\n'
        f'"title": "{num}. {title}",\n'
        f'"desc": "{ec(desc)}",\n'
        f'"examples": [\n{ex_block}\n    ],\n'
        f'"rw": {{\n'
        f'    "title": "{ec(rw_title)}",\n'
        f'    "scenario": "{ec(rw_scenario)}",\n'
        f'    "code": "{ec(rw_code)}"\n'
        f'}},\n'
        f'"practice": {{\n'
        f'    "title": "{ec(pt)}",\n'
        f'    "desc": "{ec(pd_text)}",\n'
        f'    "starter": "{ec(ps)}"\n'
        f'}}\n'
        f'}},\n\n'
    )

# ── Section 25: Advanced Aggregations (FILTER, ROLLUP, GROUPING SETS) ──────────
s25_code1 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    region TEXT, product TEXT,
    amount REAL, q INTEGER)''')
runmany('INSERT INTO sales VALUES (?,?,?,?,?)', [
    (1,'North','A',100,1),(2,'North','B',200,1),
    (3,'South','A',150,2),(4,'South','B',250,2),
    (5,'North','A',120,3),(6,'South','B',300,3)])
# FILTER clause – conditional aggregation
rows = run('''
    SELECT
        region,
        SUM(amount) AS total,
        SUM(amount) FILTER(WHERE q=1) AS q1,
        SUM(amount) FILTER(WHERE q=2) AS q2
    FROM sales GROUP BY region''')
print(rows)
"""

s25_code2 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS sales2 (
    region TEXT, product TEXT, amount REAL)''')
runmany('INSERT INTO sales2 VALUES (?,?,?)', [
    ('North','A',100),('North','B',200),
    ('South','A',150),('South','B',250)])
# Emulate ROLLUP with UNION ALL
rows = run('''
    SELECT region, product, SUM(amount)
    FROM sales2 GROUP BY region, product
    UNION ALL
    SELECT region, NULL, SUM(amount)
    FROM sales2 GROUP BY region
    UNION ALL
    SELECT NULL, NULL, SUM(amount) FROM sales2
    ORDER BY 1,2''')
for r in rows: print(r)
"""

s25_code3 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS metrics (
    dept TEXT, month INTEGER, revenue REAL)''')
runmany('INSERT INTO metrics VALUES (?,?,?)', [
    ('Eng',1,5000),('Eng',2,6000),('HR',1,2000),('HR',2,2500)])
# PERCENT_RANK and CUME_DIST
rows = run('''
    SELECT dept, month, revenue,
        RANK() OVER (ORDER BY revenue) AS rnk,
        ROUND(100.0*RANK() OVER(ORDER BY revenue)/COUNT(*) OVER(),1) AS pct
    FROM metrics ORDER BY revenue''')
for r in rows: print(r)
"""

s25_code4 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY, customer TEXT,
    status TEXT, amount REAL)''')
runmany('INSERT INTO orders VALUES (?,?,?,?)', [
    (1,'Alice','paid',300),(2,'Bob','pending',150),
    (3,'Alice','paid',200),(4,'Bob','paid',400),(5,'Carol','refunded',100)])
# Multi-dimensional conditional aggregation
rows = run('''
    SELECT customer,
        COUNT(*) FILTER(WHERE status='paid') AS paid_cnt,
        SUM(amount) FILTER(WHERE status='paid') AS paid_sum,
        COUNT(*) FILTER(WHERE status='pending') AS pend_cnt
    FROM orders GROUP BY customer ORDER BY customer''')
for r in rows: print(r)
"""

s25 = make_sql(
    25, "Advanced Aggregations",
    "Use FILTER clauses for conditional aggregation, emulate ROLLUP with UNION ALL, and combine window functions for multi-dimensional analysis.",
    [
        {"label": "FILTER clause – conditional sums per quarter", "code": s25_code1},
        {"label": "Emulate ROLLUP with UNION ALL", "code": s25_code2},
        {"label": "RANK and percent-rank", "code": s25_code3},
        {"label": "Multi-dimensional conditional aggregation", "code": s25_code4},
    ],
    "E-commerce Revenue Breakdown",
    "An analytics team needs quarterly revenue by region, total rows, and a grand-total rollup — all in one query.",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS rev (
    region TEXT, q INTEGER, amount REAL)''')
runmany('INSERT INTO rev VALUES (?,?,?)', [
    ('North',1,500),('North',2,700),
    ('South',1,400),('South',2,600)])
rows = run('''
    SELECT region, q,
        SUM(amount) AS total,
        SUM(amount) FILTER(WHERE q=1) AS q1_total
    FROM rev GROUP BY region, q
    UNION ALL
    SELECT NULL, NULL, SUM(amount), NULL FROM rev''')
for r in rows: print(r)
""",
    "Conditional Aggregation Practice",
    "Create a 'transactions' table with columns (id, type TEXT, amount REAL). Write a query that returns total amount where type='credit', total where type='debit', and the net difference — all in one row.",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY, type TEXT, amount REAL)''')
runmany('INSERT INTO transactions VALUES (?,?,?)', [
    (1,'credit',500),(2,'debit',200),(3,'credit',300),(4,'debit',150)])
# Write your FILTER aggregation query here
"""
)

# ── Section 26: Self-Joins & Non-Equi Joins ────────────────────────────────────
s26_code1 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY, name TEXT,
    manager_id INTEGER, salary REAL)''')
runmany('INSERT INTO employees VALUES (?,?,?,?)', [
    (1,'Alice',None,9000),(2,'Bob',1,7000),
    (3,'Carol',1,7500),(4,'Dave',2,5000),(5,'Eve',2,5500)])
# Self-join: each employee with their manager's name
rows = run('''
    SELECT e.name AS employee, m.name AS manager
    FROM employees e
    LEFT JOIN employees m ON e.manager_id = m.id
    ORDER BY e.id''')
for r in rows: print(r)
"""

s26_code2 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS employees2 (
    id INTEGER PRIMARY KEY, name TEXT, salary REAL, dept TEXT)''')
runmany('INSERT INTO employees2 VALUES (?,?,?,?)', [
    (1,'Alice',9000,'Eng'),(2,'Bob',7000,'Eng'),
    (3,'Carol',7500,'HR'),(4,'Dave',5000,'HR')])
# Non-equi join: employees earning more than others in same dept
rows = run('''
    SELECT a.name AS higher, b.name AS lower,
           a.salary - b.salary AS diff
    FROM employees2 a
    JOIN employees2 b
      ON a.dept = b.dept AND a.salary > b.salary
    ORDER BY diff DESC''')
for r in rows: print(r)
"""

s26_code3 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS prices (
    product TEXT, price REAL, valid_from TEXT, valid_to TEXT)''')
runmany('INSERT INTO prices VALUES (?,?,?,?)', [
    ('Widget',10.0,'2024-01-01','2024-03-31'),
    ('Widget',12.0,'2024-04-01','2024-12-31'),
    ('Gadget',25.0,'2024-01-01','2024-12-31')])
run('''CREATE TABLE IF NOT EXISTS orders3 (
    id INTEGER, product TEXT, order_date TEXT, qty INTEGER)''')
runmany('INSERT INTO orders3 VALUES (?,?,?,?)', [
    (1,'Widget','2024-02-15',3),(2,'Widget','2024-05-20',5),(3,'Gadget','2024-03-10',2)])
# Range join: match orders to the correct price band
rows = run('''
    SELECT o.id, o.product, o.order_date, p.price, o.qty*p.price AS total
    FROM orders3 o
    JOIN prices p
      ON o.product=p.product
     AND o.order_date BETWEEN p.valid_from AND p.valid_to
    ORDER BY o.id''')
for r in rows: print(r)
"""

s26_code4 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY, name TEXT,
    start TEXT, end TEXT)''')
runmany('INSERT INTO tasks VALUES (?,?,?,?)', [
    (1,'Deploy','2024-01-10','2024-01-15'),
    (2,'Test','2024-01-12','2024-01-18'),
    (3,'Review','2024-01-20','2024-01-25'),
    (4,'Release','2024-01-16','2024-01-22')])
# Find overlapping task pairs
rows = run('''
    SELECT a.name AS task1, b.name AS task2
    FROM tasks a JOIN tasks b
      ON a.id < b.id
     AND a.start <= b.end
     AND a.end >= b.start
    ORDER BY a.id''')
for r in rows: print(r)
"""

s26 = make_sql(
    26, "Self-Joins & Non-Equi Joins",
    "Use self-joins to query hierarchical data, non-equi joins for range matching, and interval joins to detect overlaps.",
    [
        {"label": "Self-join: employee-manager hierarchy", "code": s26_code1},
        {"label": "Non-equi join: salary comparisons within dept", "code": s26_code2},
        {"label": "Range join: match orders to price bands", "code": s26_code3},
        {"label": "Interval join: detect overlapping tasks", "code": s26_code4},
    ],
    "Org-Chart & Salary Reporting",
    "HR needs a report showing each employee, their direct manager, and whether they earn more than the average of their peer group.",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY, name TEXT,
    manager_id INTEGER, salary REAL, dept TEXT)''')
runmany('INSERT INTO staff VALUES (?,?,?,?,?)', [
    (1,'CEO',None,15000,'Exec'),(2,'CTO',1,12000,'Eng'),
    (3,'Dev1',2,8000,'Eng'),(4,'Dev2',2,7500,'Eng'),(5,'CHRO',1,11000,'HR')])
rows = run('''
    SELECT e.name, m.name AS mgr,
        e.salary,
        AVG(p.salary) OVER(PARTITION BY e.manager_id) AS peer_avg
    FROM staff e
    LEFT JOIN staff m ON e.manager_id=m.id
    ORDER BY e.id''')
for r in rows: print(r)
""",
    "Self-Join Practice",
    "Using the 'staff' table above, find all pairs of employees in the same department where one earns at least 20% more than the other.",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY, name TEXT,
    dept TEXT, salary REAL)''')
runmany('INSERT INTO staff VALUES (?,?,?,?)', [
    (1,'Alice','Eng',9000),(2,'Bob','Eng',7000),
    (3,'Carol','HR',8000),(4,'Dave','HR',6000)])
# Write a non-equi self-join here
"""
)

# ── Section 27: Analytical Functions Advanced (LEAD, LAG, NTILE, FIRST_VALUE) ─
s27_code1 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS stock (
    dt TEXT, ticker TEXT, close REAL)''')
runmany('INSERT INTO stock VALUES (?,?,?)', [
    ('2024-01-01','AAPL',185.0),('2024-01-02','AAPL',186.5),
    ('2024-01-03','AAPL',184.0),('2024-01-04','AAPL',188.0),
    ('2024-01-05','AAPL',190.0)])
# Daily return using LAG
rows = run('''
    SELECT dt, close,
        LAG(close) OVER(ORDER BY dt) AS prev,
        ROUND(close - LAG(close) OVER(ORDER BY dt), 2) AS change
    FROM stock ORDER BY dt''')
for r in rows: print(r)
"""

s27_code2 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS sales3 (
    month INTEGER, revenue REAL)''')
runmany('INSERT INTO sales3 VALUES (?,?)', [
    (1,5000),(2,5500),(3,4800),(4,6200),(5,6800),(6,7100)])
# Compare to next month with LEAD; running avg
rows = run('''
    SELECT month, revenue,
        LEAD(revenue) OVER(ORDER BY month) AS next_month,
        ROUND(AVG(revenue) OVER(
            ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) AS rolling3
    FROM sales3''')
for r in rows: print(r)
"""

s27_code3 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS scores (
    student TEXT, score INTEGER)''')
runmany('INSERT INTO scores VALUES (?,?)', [
    ('Alice',92),('Bob',75),('Carol',88),
    ('Dave',60),('Eve',95),('Frank',70)])
# NTILE: split into quartiles
rows = run('''
    SELECT student, score,
        NTILE(4) OVER(ORDER BY score) AS quartile
    FROM scores ORDER BY score''')
for r in rows: print(r)
"""

s27_code4 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS temps (
    city TEXT, day INTEGER, temp REAL)''')
runmany('INSERT INTO temps VALUES (?,?,?)', [
    ('NYC',1,5.0),('NYC',2,7.0),('NYC',3,4.0),
    ('LA',1,20.0),('LA',2,22.0),('LA',3,19.0)])
# FIRST_VALUE and LAST_VALUE per city
rows = run('''
    SELECT city, day, temp,
        FIRST_VALUE(temp) OVER(PARTITION BY city ORDER BY day) AS first_t,
        MAX(temp) OVER(PARTITION BY city) AS peak
    FROM temps ORDER BY city, day''')
for r in rows: print(r)
"""

s27 = make_sql(
    27, "Analytical Functions Advanced",
    "Go beyond basic ranking: use LAG/LEAD for period comparisons, NTILE for bucketing, FIRST_VALUE/LAST_VALUE for partition anchors, and rolling window frames.",
    [
        {"label": "LAG: daily price change", "code": s27_code1},
        {"label": "LEAD & rolling 3-period average", "code": s27_code2},
        {"label": "NTILE: quartile bucketing", "code": s27_code3},
        {"label": "FIRST_VALUE & MAX per partition", "code": s27_code4},
    ],
    "Sales Trend Analysis",
    "A business analyst wants to see month-over-month revenue change, the next month forecast gap, and each month's performance bucket (top 25%, etc.).",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS monthly (
    month INTEGER, revenue REAL)''')
runmany('INSERT INTO monthly VALUES (?,?)', [
    (1,4000),(2,4500),(3,4200),(4,5000),(5,5500),(6,6000)])
rows = run('''
    SELECT month, revenue,
        LAG(revenue) OVER(ORDER BY month) AS prev,
        ROUND(revenue - LAG(revenue) OVER(ORDER BY month),2) AS mom_change,
        NTILE(3) OVER(ORDER BY revenue) AS tier
    FROM monthly''')
for r in rows: print(r)
""",
    "Window Function Practice",
    "Using a 'visits' table with columns (user_id, visit_date TEXT, pages_viewed INTEGER), compute for each user: their previous visit date, the gap in days between visits, and their max pages_viewed.",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS visits (
    user_id INTEGER, visit_date TEXT, pages_viewed INTEGER)''')
runmany('INSERT INTO visits VALUES (?,?,?)', [
    (1,'2024-01-01',5),(1,'2024-01-05',8),(1,'2024-01-12',3),
    (2,'2024-01-02',10),(2,'2024-01-10',7)])
# Write LAG and MAX window functions here
"""
)

# ── Section 28: Database Design & Normalization ────────────────────────────────
s28_code1 = SETUP + """\
# 1NF: atomic values, no repeating groups
run('''CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL)''')
run('''CREATE TABLE IF NOT EXISTS contact_phones (
    contact_id INTEGER,
    phone TEXT NOT NULL,
    FOREIGN KEY(contact_id) REFERENCES contacts(id))''')
runmany('INSERT INTO contacts VALUES (?,?,?)', [
    (1,'Alice','alice@ex.com'),(2,'Bob','bob@ex.com')])
runmany('INSERT INTO contact_phones VALUES (?,?)', [
    (1,'555-0001'),(1,'555-0002'),(2,'555-0003')])
print(run('SELECT * FROM contacts'))
print(run('SELECT * FROM contact_phones'))
"""

s28_code2 = SETUP + """\
# 2NF: remove partial dependencies (composite key fix)
run('''CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    price REAL NOT NULL)''')
run('''CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER,
    product_id INTEGER,
    qty INTEGER NOT NULL,
    PRIMARY KEY(order_id, product_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id))''')
runmany('INSERT INTO products VALUES (?,?,?)', [
    (10,'Widget',9.99),(11,'Gadget',24.99)])
runmany('INSERT INTO order_items VALUES (?,?,?)', [
    (1,10,3),(1,11,1),(2,10,5)])
rows = run('''
    SELECT oi.order_id, p.product_name, oi.qty, p.price*oi.qty AS subtotal
    FROM order_items oi JOIN products p ON oi.product_id=p.product_id''')
for r in rows: print(r)
"""

s28_code3 = SETUP + """\
# 3NF: remove transitive dependencies
run('''CREATE TABLE IF NOT EXISTS departments (
    dept_id INTEGER PRIMARY KEY, dept_name TEXT, location TEXT)''')
run('''CREATE TABLE IF NOT EXISTS staff2 (
    id INTEGER PRIMARY KEY, name TEXT,
    dept_id INTEGER,
    FOREIGN KEY(dept_id) REFERENCES departments(dept_id))''')
runmany('INSERT INTO departments VALUES (?,?,?)', [
    (1,'Engineering','Floor 3'),(2,'HR','Floor 1')])
runmany('INSERT INTO staff2 VALUES (?,?,?)', [
    (1,'Alice',1),(2,'Bob',1),(3,'Carol',2)])
rows = run('''
    SELECT s.name, d.dept_name, d.location
    FROM staff2 s JOIN departments d ON s.dept_id=d.dept_id''')
for r in rows: print(r)
"""

s28_code4 = SETUP + """\
# Schema inspection and FK checks
run('''CREATE TABLE IF NOT EXISTS parent (id INTEGER PRIMARY KEY, val TEXT)''')
run('''CREATE TABLE IF NOT EXISTS child (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    FOREIGN KEY(parent_id) REFERENCES parent(id))''')
run('''PRAGMA foreign_keys=ON''')
runmany('INSERT INTO parent VALUES (?,?)', [(1,'A'),(2,'B')])
runmany('INSERT INTO child VALUES (?,?)', [(10,1),(11,2)])
# List tables and schema
tables = run("SELECT name FROM sqlite_master WHERE type='table'")
print('Tables:', tables)
schema = run("SELECT sql FROM sqlite_master WHERE name='child'")
print(schema[0][0])
"""

s28 = make_sql(
    28, "Database Design & Normalization",
    "Apply 1NF, 2NF, and 3NF to eliminate redundancy, design proper primary and foreign keys, and inspect schemas with SQLite system tables.",
    [
        {"label": "1NF: atomic values and separate phone table", "code": s28_code1},
        {"label": "2NF: remove partial dependency with products table", "code": s28_code2},
        {"label": "3NF: move location to departments table", "code": s28_code3},
        {"label": "Schema inspection with PRAGMA and sqlite_master", "code": s28_code4},
    ],
    "Customer Orders Schema",
    "Design a normalized schema for customers, orders, and products. Ensure no partial or transitive dependencies, then write a JOIN query to get order summaries.",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
run('''CREATE TABLE IF NOT EXISTS products2 (
    id INTEGER PRIMARY KEY, name TEXT, price REAL)''')
run('''CREATE TABLE IF NOT EXISTS orders2 (
    id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT)''')
run('''CREATE TABLE IF NOT EXISTS order_lines (
    order_id INTEGER, product_id INTEGER, qty INTEGER,
    PRIMARY KEY(order_id, product_id))''')
runmany('INSERT INTO customers VALUES (?,?,?)', [(1,'Alice','a@ex.com')])
runmany('INSERT INTO products2 VALUES (?,?,?)', [(1,'Widget',10.0)])
runmany('INSERT INTO orders2 VALUES (?,?,?)', [(1,1,'2024-01-15')])
runmany('INSERT INTO order_lines VALUES (?,?,?)', [(1,1,3)])
rows = run('''
    SELECT c.name, o.order_date, p.name, ol.qty, p.price*ol.qty AS total
    FROM orders2 o
    JOIN customers c ON o.customer_id=c.id
    JOIN order_lines ol ON ol.order_id=o.id
    JOIN products2 p ON p.id=ol.product_id''')
for r in rows: print(r)
""",
    "Normalization Practice",
    "You have a denormalized table: orders_flat(order_id, customer_name, customer_email, product_name, price, qty). Identify the normal form violations and write CREATE TABLE statements for a 3NF schema.",
    SETUP + """\
# Denormalized (bad):
# orders_flat: order_id, customer_name, customer_email, product_name, price, qty
# Violates 2NF (price depends only on product) and 3NF if email depends on name.
# Write your normalized CREATE TABLE statements here:

# run('''CREATE TABLE customers ...''')
# run('''CREATE TABLE products ...''')
# run('''CREATE TABLE orders ...''')
# run('''CREATE TABLE order_items ...''')
"""
)

# ── Section 29: JSON in SQL ────────────────────────────────────────────────────
s29_code1 = SETUP + """\
import json
run('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    payload TEXT)''')  -- stored as JSON text
data = [
    (1, json.dumps({'user':'alice','action':'login','meta':{'ip':'1.2.3.4'}})),
    (2, json.dumps({'user':'bob','action':'purchase','meta':{'items':3,'total':59.99}})),
    (3, json.dumps({'user':'alice','action':'logout','meta':{'ip':'1.2.3.4'}})),
]
runmany('INSERT INTO events VALUES (?,?)', data)
# Extract top-level field with json_extract
rows = run("SELECT id, json_extract(payload,'$.user'), json_extract(payload,'$.action') FROM events")
for r in rows: print(r)
"""

s29_code2 = SETUP + """\
import json
run('''CREATE TABLE IF NOT EXISTS events2 (id INTEGER PRIMARY KEY, payload TEXT)''')
runmany('INSERT INTO events2 VALUES (?,?)', [
    (1, json.dumps({'user':'alice','tags':['sql','python'],'score':95})),
    (2, json.dumps({'user':'bob','tags':['ml','python'],'score':80})),
])
# Access nested and array elements
rows = run('''
    SELECT id,
        json_extract(payload, '$.user') AS user,
        json_extract(payload, '$.score') AS score,
        json_extract(payload, '$.tags[0]') AS first_tag
    FROM events2''')
for r in rows: print(r)
"""

s29_code3 = SETUP + """\
import json
run('''CREATE TABLE IF NOT EXISTS configs (
    id INTEGER PRIMARY KEY, settings TEXT)''')
run('''INSERT INTO configs VALUES (1, ?)''',
    (json.dumps({'theme':'dark','lang':'en','max_rows':100}),))
# Modify JSON with json_set, json_insert, json_remove
run('''UPDATE configs SET settings = json_set(settings, '$.theme', 'light') WHERE id=1''')
run('''UPDATE configs SET settings = json_set(settings, '$.debug', 1) WHERE id=1''')
row = run('SELECT settings FROM configs WHERE id=1')
print(json.loads(row[0][0]))
"""

s29_code4 = SETUP + """\
import json
run('''CREATE TABLE IF NOT EXISTS products3 (
    id INTEGER PRIMARY KEY, name TEXT, attributes TEXT)''')
runmany('INSERT INTO products3 VALUES (?,?,?)', [
    (1,'Widget', json.dumps({'color':'red','weight':0.5,'tags':['sale','new']})),
    (2,'Gadget', json.dumps({'color':'blue','weight':1.2,'tags':['new']})),
    (3,'Doohickey', json.dumps({'color':'red','weight':0.3,'tags':['sale']})),
])
# Filter on JSON field and aggregate
rows = run('''
    SELECT name,
        json_extract(attributes,'$.color') AS color,
        json_extract(attributes,'$.weight') AS weight
    FROM products3
    WHERE json_extract(attributes,'$.color')='red'
    ORDER BY weight''')
for r in rows: print(r)
"""

s29 = make_sql(
    29, "JSON in SQL",
    "Store, extract, modify, and filter JSON data in SQLite using json_extract, json_set, json_insert, and json_remove.",
    [
        {"label": "json_extract: read top-level fields", "code": s29_code1},
        {"label": "Nested and array element access", "code": s29_code2},
        {"label": "Modify JSON with json_set and json_insert", "code": s29_code3},
        {"label": "Filter rows by JSON field values", "code": s29_code4},
    ],
    "User Event Logging",
    "An app stores user events as JSON blobs. Query to find all purchase events, extract the total amount, and rank users by spend.",
    SETUP + """\
import json
run('''CREATE TABLE IF NOT EXISTS user_events (
    id INTEGER PRIMARY KEY, payload TEXT)''')
runmany('INSERT INTO user_events VALUES (?,?)', [
    (1,json.dumps({'user':'alice','action':'purchase','amount':49.99})),
    (2,json.dumps({'user':'bob','action':'view','amount':0})),
    (3,json.dumps({'user':'alice','action':'purchase','amount':29.99})),
    (4,json.dumps({'user':'carol','action':'purchase','amount':99.99})),
])
rows = run('''
    SELECT
        json_extract(payload,'$.user') AS user,
        SUM(CAST(json_extract(payload,'$.amount') AS REAL)) AS total_spend
    FROM user_events
    WHERE json_extract(payload,'$.action')='purchase'
    GROUP BY user ORDER BY total_spend DESC''')
for r in rows: print(r)
""",
    "JSON Querying Practice",
    "Create a 'logs' table with an id and a 'data' JSON column. Insert 3 log entries with fields: level (INFO/ERROR), message, and timestamp. Write a query to show only ERROR logs with their message and timestamp.",
    SETUP + """\
import json
run('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, data TEXT)''')
runmany('INSERT INTO logs VALUES (?,?)', [
    (1,json.dumps({'level':'INFO','message':'Started','timestamp':'2024-01-01T09:00:00'})),
    (2,json.dumps({'level':'ERROR','message':'Null ref','timestamp':'2024-01-01T09:05:00'})),
    (3,json.dumps({'level':'ERROR','message':'Timeout','timestamp':'2024-01-01T09:10:00'})),
])
# Write your json_extract filter query here
"""
)

# ── Section 30: Full-Text Search ───────────────────────────────────────────────
s30_code1 = SETUP + """\
# FTS5 virtual table for full-text search
run('''CREATE VIRTUAL TABLE IF NOT EXISTS articles
    USING fts5(title, body, tokenize='porter ascii')''')
runmany('INSERT INTO articles VALUES (?,?)', [
    ('SQL Basics','Learn the fundamentals of SQL queries and databases'),
    ('Python for Data','Python is great for data analysis and machine learning'),
    ('Advanced SQL','Window functions and CTEs are powerful SQL features'),
    ('NumPy Guide','NumPy provides fast array operations for numerical data'),
])
# Simple search
rows = run("SELECT title FROM articles WHERE articles MATCH 'SQL'")
for r in rows: print(r)
"""

s30_code2 = SETUP + """\
run('''CREATE VIRTUAL TABLE IF NOT EXISTS docs
    USING fts5(title, content)''')
runmany('INSERT INTO docs VALUES (?,?)', [
    ('Intro to ML','Machine learning uses statistical models to make predictions'),
    ('Deep Learning','Neural networks form the basis of deep learning systems'),
    ('SQL Mastery','Master SQL with window functions and query optimization'),
    ('Data Wrangling','Pandas and NumPy help with data cleaning and transformation'),
])
# Phrase search and column filter
rows = run("SELECT title FROM docs WHERE docs MATCH 'title:SQL'")
print('Title match:', rows)
rows = run("SELECT title, rank FROM docs WHERE docs MATCH 'data' ORDER BY rank")
for r in rows: print(r)
"""

s30_code3 = SETUP + """\
run('''CREATE VIRTUAL TABLE IF NOT EXISTS notes
    USING fts5(author, text)''')
runmany('INSERT INTO notes VALUES (?,?)', [
    ('Alice','Python decorators and closures are advanced features'),
    ('Bob','SQL joins and subqueries are essential for data analysis'),
    ('Alice','NumPy broadcasting makes array operations concise'),
    ('Bob','Window functions in SQL enable running totals and rankings'),
])
# Prefix search and boolean operators
rows = run("SELECT author, text FROM notes WHERE notes MATCH 'SQL AND data'")
print('AND:', rows)
rows = run("SELECT author, text FROM notes WHERE notes MATCH 'Python OR NumPy'")
print('OR:', [r[0] for r in rows])
"""

s30_code4 = SETUP + """\
run('''CREATE VIRTUAL TABLE IF NOT EXISTS kb
    USING fts5(title, body)''')
runmany('INSERT INTO kb VALUES (?,?)', [
    ('Error Handling','Use try-except blocks to catch and handle Python exceptions gracefully'),
    ('Logging Best Practices','Configure logging with handlers, formatters and log levels'),
    ('Testing Strategies','Unit tests and integration tests ensure code reliability'),
    ('Code Review Tips','Peer code review improves code quality and knowledge sharing'),
])
# Snippet and highlight
rows = run('''
    SELECT title, snippet(kb, 1, '<b>', '</b>', '...', 8)
    FROM kb WHERE kb MATCH 'code'
    ORDER BY rank''')
for r in rows: print(r[0], '|', r[1])
"""

s30 = make_sql(
    30, "Full-Text Search",
    "Use SQLite's FTS5 virtual tables to perform keyword search, phrase matching, boolean operators, column-specific search, and ranked results with snippets.",
    [
        {"label": "Create FTS5 table and basic MATCH search", "code": s30_code1},
        {"label": "Column-specific search and ranked results", "code": s30_code2},
        {"label": "Prefix search and AND/OR boolean operators", "code": s30_code3},
        {"label": "Snippet extraction with highlighting", "code": s30_code4},
    ],
    "Knowledge Base Search",
    "A support team has a knowledge base table. Implement full-text search that returns articles matching a query, ranked by relevance, with a highlighted snippet.",
    SETUP + """\
run('''CREATE VIRTUAL TABLE IF NOT EXISTS support_kb
    USING fts5(title, content, tokenize='porter ascii')''')
runmany('INSERT INTO support_kb VALUES (?,?)', [
    ('Password Reset','To reset your password go to settings and click reset'),
    ('Billing FAQ','For billing questions contact support or view your invoice'),
    ('Account Setup','Set up your account by verifying your email address'),
    ('Password Policy','Passwords must be 8 characters with a mix of letters and numbers'),
])
query = 'password'
rows = run(f'''
    SELECT title,
        snippet(support_kb, 1, \'**\', \'**\', \'...\', 6) AS preview,
        rank
    FROM support_kb
    WHERE support_kb MATCH ?
    ORDER BY rank
''', (query,))
for r in rows: print(r[0], '|', r[1])
""",
    "FTS5 Practice",
    "Create an FTS5 table called 'recipes' with columns (name, ingredients, instructions). Insert 4 recipes. Write a query to find all recipes where the ingredients contain 'garlic' AND instructions contain 'stir'.",
    SETUP + """\
run('''CREATE VIRTUAL TABLE IF NOT EXISTS recipes
    USING fts5(name, ingredients, instructions)''')
runmany('INSERT INTO recipes VALUES (?,?,?)', [
    ('Pasta','flour eggs garlic olive oil','stir pasta in boiling water'),
    ('Soup','carrots garlic onion broth','simmer and stir until soft'),
    ('Salad','lettuce tomato cucumber','toss with dressing'),
    ('Stir Fry','garlic ginger soy sauce vegetables','stir fry on high heat'),
])
# Write your FTS5 AND query here
"""
)

# ── Section 31: Performance Tuning & EXPLAIN ──────────────────────────────────
s31_code1 = SETUP + """\
import time
run('''CREATE TABLE IF NOT EXISTS big (
    id INTEGER PRIMARY KEY, val INTEGER, cat TEXT)''')
# Insert sample data
import random; random.seed(42)
rows = [(i, random.randint(1,1000), random.choice(['A','B','C'])) for i in range(1,5001)]
runmany('INSERT INTO big VALUES (?,?,?)', rows)
# Query without index
t0 = time.perf_counter()
run('SELECT COUNT(*) FROM big WHERE val > 500')
t1 = time.perf_counter()
# Add index
run('CREATE INDEX IF NOT EXISTS idx_val ON big(val)')
t2 = time.perf_counter()
run('SELECT COUNT(*) FROM big WHERE val > 500')
t3 = time.perf_counter()
print(f'Without index: {(t1-t0)*1000:.2f}ms')
print(f'With index:    {(t3-t2)*1000:.2f}ms')
"""

s31_code2 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS orders4 (
    id INTEGER PRIMARY KEY, customer_id INTEGER,
    status TEXT, amount REAL)''')
import random; random.seed(0)
rows = [(i, random.randint(1,100), random.choice(['new','paid','shipped']),
         round(random.uniform(10,500),2)) for i in range(1,2001)]
runmany('INSERT INTO orders4 VALUES (?,?,?,?)', rows)
# EXPLAIN QUERY PLAN
plan = run('''EXPLAIN QUERY PLAN
    SELECT customer_id, SUM(amount)
    FROM orders4
    WHERE status='paid'
    GROUP BY customer_id''')
for p in plan: print(p)
# Add composite index
run('CREATE INDEX IF NOT EXISTS idx_status_cust ON orders4(status, customer_id)')
plan2 = run('''EXPLAIN QUERY PLAN
    SELECT customer_id, SUM(amount)
    FROM orders4 WHERE status='paid'
    GROUP BY customer_id''')
for p in plan2: print(p)
"""

s31_code3 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS logs2 (
    id INTEGER PRIMARY KEY,
    user_id INTEGER, event TEXT, ts TEXT)''')
import random, string; random.seed(1)
events = ['login','logout','purchase','view']
rows = [(i, random.randint(1,50),
         random.choice(events),
         f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}')
        for i in range(1,3001)]
runmany('INSERT INTO logs2 VALUES (?,?,?,?)', rows)
# Covering index: avoid table access for common query
run('CREATE INDEX IF NOT EXISTS idx_cov ON logs2(user_id, event, ts)')
plan = run('''EXPLAIN QUERY PLAN
    SELECT user_id, event, ts FROM logs2
    WHERE user_id=1 ORDER BY ts''')
for p in plan: print(p)
"""

s31_code4 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)''')
import random; random.seed(5)
rows = [(i,f'item_{i}',round(random.uniform(1,100),2),random.randint(0,500)) for i in range(1,1001)]
runmany('INSERT INTO items VALUES (?,?,?,?)', rows)
# ANALYZE updates statistics for the query planner
run('ANALYZE')
# Partial index: only index in-stock items
run('CREATE INDEX IF NOT EXISTS idx_instock ON items(price) WHERE stock > 0')
plan = run('''EXPLAIN QUERY PLAN
    SELECT name, price FROM items
    WHERE stock > 0 AND price < 20
    ORDER BY price''')
for p in plan: print(p)
print(run('SELECT COUNT(*) FROM items WHERE stock>0'))
"""

s31 = make_sql(
    31, "Performance Tuning & EXPLAIN",
    "Use EXPLAIN QUERY PLAN to understand query execution, create regular, composite, covering, and partial indexes, and run ANALYZE to update planner statistics.",
    [
        {"label": "Index impact benchmark: with vs without", "code": s31_code1},
        {"label": "EXPLAIN QUERY PLAN before and after composite index", "code": s31_code2},
        {"label": "Covering index to avoid table scans", "code": s31_code3},
        {"label": "Partial index and ANALYZE", "code": s31_code4},
    ],
    "Slow Query Investigation",
    "A production query joining orders and customers is slow. Use EXPLAIN QUERY PLAN to find the bottleneck, add an appropriate index, and verify the improvement.",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS cust2 (id INTEGER PRIMARY KEY, name TEXT, tier TEXT)''')
run('''CREATE TABLE IF NOT EXISTS ord2 (
    id INTEGER PRIMARY KEY, cust_id INTEGER, amount REAL, status TEXT)''')
import random; random.seed(7)
runmany('INSERT INTO cust2 VALUES (?,?,?)', [(i,f'C{i}',random.choice(['gold','silver'])) for i in range(1,501)])
runmany('INSERT INTO ord2 VALUES (?,?,?,?)',
    [(i,random.randint(1,500),round(random.uniform(10,500),2),
      random.choice(['paid','pending'])) for i in range(1,2001)])
plan = run('''EXPLAIN QUERY PLAN
    SELECT c.name, SUM(o.amount)
    FROM ord2 o JOIN cust2 c ON o.cust_id=c.id
    WHERE o.status='paid' AND c.tier='gold'
    GROUP BY c.id''')
for p in plan: print(p)
run('CREATE INDEX IF NOT EXISTS idx_ord_status ON ord2(status, cust_id)')
run('CREATE INDEX IF NOT EXISTS idx_cust_tier ON cust2(tier)')
plan2 = run('''EXPLAIN QUERY PLAN
    SELECT c.name, SUM(o.amount)
    FROM ord2 o JOIN cust2 c ON o.cust_id=c.id
    WHERE o.status='paid' AND c.tier='gold'
    GROUP BY c.id''')
for p in plan2: print(p)
""",
    "Index Optimization Practice",
    "Create a 'transactions2' table (id, account_id INTEGER, type TEXT, amount REAL, created_at TEXT). Insert 500 rows. Use EXPLAIN QUERY PLAN to check a query filtering by account_id and type, then add the right index to make it efficient.",
    SETUP + """\
import random; random.seed(9)
run('''CREATE TABLE IF NOT EXISTS transactions2 (
    id INTEGER PRIMARY KEY, account_id INTEGER,
    type TEXT, amount REAL, created_at TEXT)''')
rows = [(i, random.randint(1,50), random.choice(['debit','credit']),
         round(random.uniform(1,1000),2), f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}')
        for i in range(1,501)]
runmany('INSERT INTO transactions2 VALUES (?,?,?,?,?)', rows)
# First check the plan, then add an index
plan = run('''EXPLAIN QUERY PLAN
    SELECT * FROM transactions2
    WHERE account_id=5 AND type='debit' ORDER BY created_at''')
for p in plan: print(p)
# Add your index here
"""
)

# ── Section 32: SQL for Data Analysis Workflow ─────────────────────────────────
s32_code1 = SETUP + """\
# End-to-end: ingest, clean, transform, analyze
run('''CREATE TABLE IF NOT EXISTS raw_sales (
    id INTEGER PRIMARY KEY,
    rep TEXT, region TEXT,
    amount TEXT,  -- stored as text (dirty data)
    sale_date TEXT)''')
runmany('INSERT INTO raw_sales VALUES (?,?,?,?,?)', [
    (1,'Alice','North','1,200.50','2024-01-15'),
    (2,'Bob','South','800','2024-01-20'),
    (3,'Alice','North','  950.00 ','2024-02-01'),
    (4,'Carol','East','','2024-02-10'),   -- missing amount
    (5,'Bob','South','1100.75','2024-02-20'),
])
# Clean: strip whitespace, handle empty, cast
rows = run('''
    SELECT rep, region,
        CASE WHEN TRIM(REPLACE(amount,',',''))='' THEN NULL
             ELSE CAST(TRIM(REPLACE(amount,',','')) AS REAL)
        END AS clean_amount,
        sale_date
    FROM raw_sales''')
for r in rows: print(r)
"""

s32_code2 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS cleaned_sales (
    rep TEXT, region TEXT, amount REAL, sale_date TEXT)''')
runmany('INSERT INTO cleaned_sales VALUES (?,?,?,?)', [
    ('Alice','North',1200.50,'2024-01-15'),
    ('Bob','South',800.00,'2024-01-20'),
    ('Alice','North',950.00,'2024-02-01'),
    ('Bob','South',1100.75,'2024-02-20'),
    ('Carol','East',750.00,'2024-03-05'),
    ('Alice','North',1350.00,'2024-03-10'),
])
# Monthly trend and running total
rows = run('''
    WITH monthly AS (
        SELECT SUBSTR(sale_date,1,7) AS month,
               rep, SUM(amount) AS total
        FROM cleaned_sales GROUP BY month, rep)
    SELECT month, rep, total,
        SUM(total) OVER(PARTITION BY rep ORDER BY month) AS running_total
    FROM monthly ORDER BY rep, month''')
for r in rows: print(r)
"""

s32_code3 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS sales_f (
    rep TEXT, region TEXT, amount REAL, sale_date TEXT)''')
runmany('INSERT INTO sales_f VALUES (?,?,?,?)', [
    ('Alice','North',1200,'2024-01-15'),('Bob','South',800,'2024-01-20'),
    ('Alice','North',950,'2024-02-01'),('Carol','East',750,'2024-02-10'),
    ('Bob','South',1100,'2024-02-20'),('Alice','North',1350,'2024-03-10'),
    ('Carol','East',900,'2024-03-15'),('Bob','South',1250,'2024-03-20'),
])
# Cohort-style: rep performance vs. regional average
rows = run('''
    SELECT rep, region, ROUND(SUM(amount),2) AS rep_total,
        ROUND(AVG(SUM(amount)) OVER(PARTITION BY region),2) AS region_avg,
        ROUND(SUM(amount) - AVG(SUM(amount)) OVER(PARTITION BY region),2) AS vs_avg
    FROM sales_f GROUP BY rep, region ORDER BY region, rep''')
for r in rows: print(r)
"""

s32_code4 = SETUP + """\
run('''CREATE TABLE IF NOT EXISTS survey (
    respondent_id INTEGER, question TEXT, score INTEGER)''')
runmany('INSERT INTO survey VALUES (?,?,?)', [
    (1,'Q1',4),(1,'Q2',5),(1,'Q3',3),
    (2,'Q1',2),(2,'Q2',3),(2,'Q3',4),
    (3,'Q1',5),(3,'Q2',5),(3,'Q3',5),
    (4,'Q1',3),(4,'Q2',2),(4,'Q3',3),
])
# Pivot: one row per respondent, one column per question
rows = run('''
    SELECT respondent_id,
        MAX(CASE WHEN question='Q1' THEN score END) AS Q1,
        MAX(CASE WHEN question='Q2' THEN score END) AS Q2,
        MAX(CASE WHEN question='Q3' THEN score END) AS Q3,
        ROUND(AVG(score),2) AS avg_score
    FROM survey GROUP BY respondent_id ORDER BY respondent_id''')
for r in rows: print(r)
"""

s32 = make_sql(
    32, "SQL for Data Analysis Workflow",
    "Apply SQL as a full data analysis tool: ingest and clean dirty data, compute monthly trends with running totals, compare performance vs. group averages, and pivot long-format survey data.",
    [
        {"label": "Ingest and clean dirty text amounts", "code": s32_code1},
        {"label": "Monthly trend with running total CTE", "code": s32_code2},
        {"label": "Rep performance vs. regional average", "code": s32_code3},
        {"label": "Pivot survey data with CASE WHEN", "code": s32_code4},
    ],
    "Sales Dashboard Pipeline",
    "Build a SQL pipeline: clean raw data, compute monthly totals, calculate month-over-month growth, and rank reps by total sales within their region.",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS pipeline_sales (
    rep TEXT, region TEXT, amount REAL, sale_date TEXT)''')
runmany('INSERT INTO pipeline_sales VALUES (?,?,?,?)', [
    ('Alice','North',1200,'2024-01-10'),('Bob','North',950,'2024-01-20'),
    ('Alice','North',1400,'2024-02-05'),('Bob','North',1100,'2024-02-15'),
    ('Carol','South',800,'2024-01-12'),('Dave','South',900,'2024-01-25'),
    ('Carol','South',1050,'2024-02-08'),('Dave','South',750,'2024-02-18'),
])
rows = run('''
    WITH monthly AS (
        SELECT rep, region, SUBSTR(sale_date,1,7) AS month,
               SUM(amount) AS total
        FROM pipeline_sales GROUP BY rep, region, month),
    with_growth AS (
        SELECT *,
            LAG(total) OVER(PARTITION BY rep ORDER BY month) AS prev,
            ROUND(100.0*(total - LAG(total) OVER(PARTITION BY rep ORDER BY month))
                  / LAG(total) OVER(PARTITION BY rep ORDER BY month), 1) AS pct_growth
        FROM monthly)
    SELECT *, RANK() OVER(PARTITION BY region, month ORDER BY total DESC) AS region_rank
    FROM with_growth ORDER BY region, month, region_rank''')
for r in rows: print(r)
""",
    "End-to-End Analysis Practice",
    "Create a 'web_logs' table with (session_id INTEGER, user_id INTEGER, page TEXT, duration_sec INTEGER, log_date TEXT). Insert 10 rows. Write a query that: (1) filters sessions over 30s, (2) counts sessions per user per day, and (3) shows each user's max daily sessions using a window function.",
    SETUP + """\
run('''CREATE TABLE IF NOT EXISTS web_logs (
    session_id INTEGER, user_id INTEGER,
    page TEXT, duration_sec INTEGER, log_date TEXT)''')
runmany('INSERT INTO web_logs VALUES (?,?,?,?,?)', [
    (1,1,'home',45,'2024-01-01'),(2,1,'about',20,'2024-01-01'),
    (3,2,'home',60,'2024-01-01'),(4,2,'shop',90,'2024-01-01'),
    (5,1,'home',35,'2024-01-02'),(6,1,'shop',55,'2024-01-02'),
    (7,3,'home',15,'2024-01-01'),(8,3,'about',40,'2024-01-01'),
    (9,2,'home',80,'2024-01-02'),(10,3,'shop',50,'2024-01-02'),
])
# Write your query: filter >30s, count per user/day, window max
"""
)

# ── Assemble and insert ───────────────────────────────────────────────────────
all_sections = s25 + s26 + s27 + s28 + s29 + s30 + s31 + s32
result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: sql sections 25-32 added")
else:
    print("FAILED")
