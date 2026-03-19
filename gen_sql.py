#!/usr/bin/env python3
"""Generate SQL with Python study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE   = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\02_sql")
BASE.mkdir(parents=True, exist_ok=True)
ACCENT = "#f0883e"
EMOJI  = "🗄️"
TITLE  = "SQL with Python"

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
        rw = s.get("rw", {})
        rw_html = (f'<div class="rw"><div class="rh">&#x1F4BC; Real-World: {esc(rw["title"])}</div>'
                   f'<div class="rd">{esc(rw["scenario"])}</div>'
                   f'<pre><code class="language-python">{esc(rw["code"])}</code></pre></div>') if rw else ""
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
    cells.append(md(f"# {TITLE} Study Guide\n\nHands-on SQL guide using Python's built-in sqlite3 module."))
    for i,s in enumerate(sections,1):
        cells.append(md(f"## {i}. {s['title']}\n\n{s.get('desc','')}"))
        for ex in s.get("examples",[]):
            if ex.get("label"): cells.append(md(f"**{ex['label']}**"))
            cells.append(code(ex["code"]))
        rw=s.get("rw")
        if rw:
            cells.append(md(f"### Real-World: {rw['title']}\n\n> {rw['scenario']}"))
            cells.append(code(rw["code"]))
        practice = s.get("practice")
        if practice:
            cells.append(md(f"### 🏋️ Practice: {practice['title']}\n\n{practice['desc']}"))
            cells.append(code(practice["starter"]))
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.11.0"}},"nbformat":4,"nbformat_minor":5}


# ─── Content ──────────────────────────────────────────────────────────────────
SECTIONS = [

{
"title": "1. Setup with sqlite3",
"desc": "Python's built-in sqlite3 module connects to relational databases — no server needed. Use :memory: for prototyping.",
"examples": [
{"label": "Connect, create table, insert rows", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")   # in-memory DB
cur  = conn.cursor()

cur.execute(
    "CREATE TABLE employees ("
    "  id INTEGER PRIMARY KEY,"
    "  name TEXT NOT NULL,"
    "  dept TEXT,"
    "  salary REAL,"
    "  hire_date TEXT)"
)

data = [
    (1, "Alice", "Engineering", 95000, "2022-03-15"),
    (2, "Bob",   "Marketing",   72000, "2021-08-01"),
    (3, "Carol", "Engineering", 88000, "2023-01-10"),
]
cur.executemany("INSERT INTO employees VALUES (?,?,?,?,?)", data)
conn.commit()

count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
print(f"Inserted {count} rows.")
conn.close()"""},
{"label": "Row factory for dict-like access", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row           # rows behave like dicts

conn.execute("CREATE TABLE products (id INT, name TEXT, price REAL)")
conn.executemany("INSERT INTO products VALUES (?,?,?)", [
    (1,"Widget",9.99),(2,"Gadget",49.99),(3,"Doohickey",19.99),
])

for row in conn.execute("SELECT * FROM products"):
    print(f"  [{row['id']}] {row['name']:12s} ${row['price']:.2f}")
conn.close()"""},
{"label": "Context manager and executescript", "code":
"""import sqlite3

# 'with' ensures commit on success, rollback on exception
with sqlite3.connect(":memory:") as conn:
    conn.executescript(\"\"\"
        CREATE TABLE categories (id INT PRIMARY KEY, name TEXT);
        CREATE TABLE items (id INT, cat_id INT, name TEXT, qty INT);
        INSERT INTO categories VALUES (1,'Electronics'),(2,'Clothing');
        INSERT INTO items VALUES
            (1,1,'Laptop',10),(2,1,'Phone',25),
            (3,2,'T-Shirt',100),(4,2,'Jeans',50);
    \"\"\")

    rows = conn.execute(
        "SELECT c.name, COUNT(i.id) as items, SUM(i.qty) as total_qty "
        "FROM categories c JOIN items i ON c.id=i.cat_id "
        "GROUP BY c.id"
    ).fetchall()
    for r in rows:
        print(f"  {r[0]:14s} items={r[1]}  qty={r[2]}")"""},
{"label": "sqlite_master schema introspection", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript(\"\"\"
    CREATE TABLE employees (id INT PRIMARY KEY, name TEXT, dept TEXT, salary REAL);
    CREATE TABLE departments (id INT PRIMARY KEY, name TEXT, budget REAL);
    CREATE INDEX idx_dept ON employees(dept);
    CREATE INDEX idx_salary ON employees(salary);
\"\"\")

# Inspect all objects via sqlite_master
print("Schema objects:")
for row in conn.execute(
    "SELECT type, name, sql FROM sqlite_master ORDER BY type, name"
).fetchall():
    print(f"  [{row[0]:5s}] {row[1]}")

# List only tables
tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
).fetchall()
print("Tables:", [t[0] for t in tables])

# List columns of a table using PRAGMA
print("Columns in employees:")
for col in conn.execute("PRAGMA table_info(employees)").fetchall():
    print(f"  col#{col[0]} {col[1]:10s} type={col[2]:8s} notnull={col[3]} pk={col[5]}")

conn.close()"""}
],
"practice": {
"title": "Design a Library Table Schema",
"desc": "Create an in-memory SQLite database with two tables: 'books' (id, title, author, year, genre) and 'members' (id, name, email). Insert at least 5 books and 3 members. Then query all books published after 2000, ordered by year descending.",
"starter":
"""import sqlite3

conn = sqlite3.connect(":memory:")

# TODO: Create the 'books' table
# conn.execute("CREATE TABLE books (...)")

# TODO: Create the 'members' table
# conn.execute("CREATE TABLE members (...)")

# TODO: Insert at least 5 books
# conn.executemany("INSERT INTO books VALUES (?,?,?,?,?)", [...])

# TODO: Insert at least 3 members
# conn.executemany("INSERT INTO members VALUES (?,?,?)", [...])

conn.commit()

# TODO: Query all books published after 2000, ordered by year DESC
# rows = conn.execute("SELECT title, author, year FROM books WHERE ...").fetchall()
# for r in rows:
#     print(r)

conn.close()"""
},
"rw": {
"title": "Sales Transaction Database Setup",
"scenario": "A startup data analyst creates an in-memory SQLite database to prototype reporting queries before moving to PostgreSQL.",
"code":
"""import sqlite3, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE sales ("
    "  id INT, customer TEXT, product TEXT,"
    "  amount REAL, sale_date TEXT)"
)

customers = ["Alice","Bob","Carol","Dave","Eve"]
products  = ["Widget","Gadget","Doohickey","Gizmo"]
base      = datetime.date(2024, 1, 1)

records = [
    (i, random.choice(customers), random.choice(products),
     round(random.uniform(20, 500), 2),
     (base + datetime.timedelta(days=random.randint(0, 180))).isoformat())
    for i in range(1, 1001)
]
conn.executemany("INSERT INTO sales VALUES (?,?,?,?,?)", records)
conn.commit()

row = conn.execute(
    "SELECT COUNT(*), ROUND(SUM(amount),2), ROUND(AVG(amount),2) FROM sales"
).fetchone()
print(f"Rows: {row[0]}  Total: ${row[1]:,.2f}  Avg: ${row[2]:.2f}")
conn.close()"""}
},

{
"title": "2. SELECT & WHERE",
"desc": "SELECT retrieves columns. WHERE filters rows. Use LIKE, IN, BETWEEN, and IS NULL for flexible filtering.",
"examples": [
{"label": "Basic SELECT and WHERE", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (id INT, name TEXT, dept TEXT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?,?,?)", [
    (1,"Alice","Eng",95000),(2,"Bob","Marketing",72000),
    (3,"Carol","Eng",88000),(4,"Dave","HR",65000),(5,"Eve","Marketing",78000),
])

# All Engineering employees, sorted by salary
rows = conn.execute(
    "SELECT name, salary FROM emp WHERE dept='Eng' ORDER BY salary DESC"
).fetchall()
print("Engineering staff:")
for r in rows: print(f"  {r[0]:8s} ${r[1]:,}")
conn.close()"""},
{"label": "LIKE, IN, BETWEEN, IS NULL", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE products (name TEXT, price REAL, category TEXT)")
conn.executemany("INSERT INTO products VALUES (?,?,?)", [
    ("Apple",0.50,"Fruit"),("Avocado",1.50,"Fruit"),
    ("Milk",2.99,"Dairy"),("Cheese",4.50,"Dairy"),
    ("Bread",3.29,"Bakery"),("Cake",None,"Bakery"),
])

q = "SELECT name FROM products WHERE"
print(conn.execute(q + " name LIKE 'A%'").fetchall())
print(conn.execute(q + " category IN ('Dairy','Bakery')").fetchall())
print(conn.execute(q + " price BETWEEN 1 AND 4").fetchall())
print(conn.execute(q + " price IS NULL").fetchall())
conn.close()"""},
{"label": "ORDER BY, LIMIT, OFFSET and DISTINCT", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (name TEXT, dept TEXT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?,?)", [
    ("Alice","Eng",95000),("Bob","HR",65000),("Carol","Eng",88000),
    ("Dave","HR",70000),("Eve","Marketing",78000),("Frank","Eng",102000),
])

# Top 3 earners
print("Top 3 earners:")
for r in conn.execute(
    "SELECT name, salary FROM emp ORDER BY salary DESC LIMIT 3"
).fetchall():
    print(f"  {r[0]:8s} ${r[1]:,}")

# Page 2 (rows 3-4) when sorting by name
print("Page 2 by name:")
for r in conn.execute(
    "SELECT name FROM emp ORDER BY name LIMIT 2 OFFSET 2"
).fetchall():
    print(f"  {r[0]}")

# Distinct departments
depts = conn.execute("SELECT DISTINCT dept FROM emp ORDER BY dept").fetchall()
print("Departments:", [d[0] for d in depts])
conn.close()"""},
{"label": "CASE WHEN, COALESCE, NULLIF, IS NULL", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (name TEXT, dept TEXT, salary REAL, bonus REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?,?,?)", [
    ("Alice","Eng",95000,5000),("Bob","HR",65000,None),
    ("Carol","Eng",88000,3000),("Dave","Marketing",72000,None),
    ("Eve","Eng",110000,8000),("Frank","HR",60000,0),
])

rows = conn.execute(
    "SELECT name, dept, salary,"
    "       COALESCE(bonus, 0) as safe_bonus,"
    "       CASE "
    "         WHEN salary >= 100000 THEN 'Senior'"
    "         WHEN salary >= 80000  THEN 'Mid'"
    "         ELSE 'Junior'"
    "       END as band,"
    "       NULLIF(bonus, 0) as nonzero_bonus "
    "FROM emp ORDER BY salary DESC"
).fetchall()

print(f"{'Name':8s} {'Band':7s} {'Salary':>9s} {'Bonus':>7s} {'NZ Bonus':>10s}")
for r in rows:
    print(f"{r[0]:8s} {r[4]:7s} ${r[2]:>8,} ${r[3]:>6,.0f} {str(r[5]):>10s}")

# IS NULL / IS NOT NULL filter
missing = conn.execute(
    "SELECT name FROM emp WHERE bonus IS NULL OR bonus = 0"
).fetchall()
print("No effective bonus:", [m[0] for m in missing])
conn.close()"""}
],
"practice": {
"title": "SELECT with WHERE, ORDER BY, and LIMIT",
"desc": "Build an employees table with columns: id, name, department, salary, city. Insert 8+ rows. Then write three queries: 1) All employees in 'Engineering' earning over 80000, sorted by salary DESC. 2) Employees from 'NYC' or 'LA' using IN. 3) The top 3 earners company-wide using LIMIT.",
"starter":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE employees (id INT, name TEXT, department TEXT, salary REAL, city TEXT)")
conn.executemany("INSERT INTO employees VALUES (?,?,?,?,?)", [
    # TODO: add at least 8 rows across multiple departments and cities
    # (1, "Alice", "Engineering", 95000, "NYC"),
    # ...
])
conn.commit()

# TODO: Query 1 — Engineering employees earning > 80000, sorted by salary DESC
# rows = conn.execute("SELECT name, salary FROM employees WHERE ...").fetchall()
# print("Engineering >80k:")
# for r in rows: print(f"  {r[0]:10s} ${r[1]:,}")

# TODO: Query 2 — Employees in NYC or LA
# rows = conn.execute("SELECT name, city FROM employees WHERE city IN (...)").fetchall()
# print("NYC/LA staff:", rows)

# TODO: Query 3 — Top 3 earners company-wide
# rows = conn.execute("SELECT name, salary FROM employees ORDER BY ... LIMIT ...").fetchall()
# print("Top 3:", rows)

conn.close()"""
},
"rw": {
"title": "Priority Order Fulfillment Filter",
"scenario": "An e-commerce backend filters pending high-value orders for the fulfillment team's priority queue.",
"code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE orders ("
    "  id INT, customer TEXT, status TEXT, amount REAL, order_date TEXT)"
)
conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", [
    (1,"Alice","shipped",120.0,"2024-01-05"),
    (2,"Bob","pending",80.0,"2024-01-10"),
    (3,"Alice","delivered",250.0,"2024-01-12"),
    (4,"Carol","pending",450.0,"2024-01-15"),
    (5,"Bob","shipped",310.0,"2024-01-18"),
    (6,"Dave","cancelled",90.0,"2024-01-20"),
])

rows = conn.execute(
    "SELECT id, customer, amount, order_date "
    "FROM orders "
    "WHERE status IN ('pending','shipped') AND amount > 100 "
    "ORDER BY amount DESC"
).fetchall()

print("Priority orders:")
for r in rows:
    print(f"  #{r[0]} {r[1]:8s} ${r[2]:6.2f}  {r[3]}")
conn.close()"""}
},

{
"title": "3. GROUP BY, Aggregates & HAVING",
"desc": "Aggregate functions (COUNT, SUM, AVG, MAX) summarize groups. HAVING filters groups after aggregation — like WHERE but for groups.",
"examples": [
{"label": "COUNT, SUM, AVG per group", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (region TEXT, rep TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    ("North","Alice",1000),("North","Bob",1500),
    ("South","Carol",800),("South","Dave",1200),
    ("East","Eve",2000),("East","Alice",900),
])

rows = conn.execute(
    "SELECT region,"
    "       COUNT(*) as reps,"
    "       SUM(amount) as total,"
    "       ROUND(AVG(amount),0) as avg_amt,"
    "       MAX(amount) as top "
    "FROM sales GROUP BY region ORDER BY total DESC"
).fetchall()
print(f"{'Region':8s} {'Reps':>5} {'Total':>8} {'Avg':>8} {'Top':>8}")
for r in rows: print(f"{r[0]:8s} {r[1]:>5} {r[2]:>8} {r[3]:>8} {r[4]:>8}")
conn.close()"""},
{"label": "HAVING — filter groups by aggregate", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (dept TEXT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?)", [
    ("Eng",120000),("Eng",95000),("Eng",110000),
    ("HR",65000),
    ("Marketing",85000),("Marketing",90000),("Marketing",72000),
])

rows = conn.execute(
    "SELECT dept, COUNT(*) as headcount, ROUND(AVG(salary),0) as avg_sal "
    "FROM emp "
    "GROUP BY dept "
    "HAVING COUNT(*) >= 2 "
    "ORDER BY avg_sal DESC"
).fetchall()
for r in rows: print(r)
conn.close()"""},
{"label": "Multi-column GROUP BY and ROLLUP simulation", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (region TEXT, product TEXT, qty INT, revenue REAL)")
conn.executemany("INSERT INTO orders VALUES (?,?,?,?)", [
    ("North","Widget",10,500),("North","Gadget",5,250),
    ("South","Widget",8,400),("South","Widget",12,600),
    ("East","Gadget",20,1000),("East","Widget",3,150),
])

# Group by two columns
print("Region + Product breakdown:")
for r in conn.execute(
    "SELECT region, product, SUM(qty) as units, ROUND(SUM(revenue),2) as rev "
    "FROM orders GROUP BY region, product ORDER BY region, rev DESC"
).fetchall():
    print(f"  {r[0]:8s} {r[1]:8s}  units={r[2]}  rev=${r[3]:.2f}")

# Simulated ROLLUP: per-region total
print("Per-region totals:")
for r in conn.execute(
    "SELECT region, SUM(qty) as total_units, ROUND(SUM(revenue),2) as total_rev "
    "FROM orders GROUP BY region ORDER BY total_rev DESC"
).fetchall():
    print(f"  {r[0]:8s}  units={r[1]}  rev=${r[2]:.2f}")
conn.close()"""},
{"label": "Conditional aggregation with SUM(CASE WHEN)", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (rep TEXT, product TEXT, amount REAL, status TEXT)")
conn.executemany("INSERT INTO sales VALUES (?,?,?,?)", [
    ("Alice","Widget",1200,"won"),("Alice","Gadget",800,"lost"),
    ("Alice","Widget",500,"won"),("Bob","Gadget",1500,"won"),
    ("Bob","Widget",300,"lost"),("Bob","Gadget",900,"won"),
    ("Carol","Widget",2000,"won"),("Carol","Gadget",600,"lost"),
])

# Pivot-style: won vs lost amounts per rep in a single query
rows = conn.execute(
    "SELECT rep,"
    "       COUNT(*) as deals,"
    "       SUM(CASE WHEN status='won'  THEN amount ELSE 0 END) as won_amt,"
    "       SUM(CASE WHEN status='lost' THEN amount ELSE 0 END) as lost_amt,"
    "       ROUND(100.0 * SUM(CASE WHEN status='won' THEN 1 ELSE 0 END) / COUNT(*), 1) as win_pct "
    "FROM sales GROUP BY rep ORDER BY won_amt DESC"
).fetchall()

print(f"{'Rep':8s} {'Deals':>6} {'Won $':>8} {'Lost $':>8} {'Win%':>6}")
for r in rows:
    print(f"{r[0]:8s} {r[1]:>6} ${r[2]:>7,.0f} ${r[3]:>7,.0f} {r[4]:>5.1f}%")
conn.close()"""}
],
"practice": {
"title": "GROUP BY with HAVING Aggregation",
"desc": "Create a 'sales' table with columns: rep (TEXT), region (TEXT), amount (REAL). Insert 10+ rows. Write queries to: 1) Show total and average sales per region, ordered by total DESC. 2) Use HAVING to list only reps whose total sales exceed 3000. 3) Find the region with the single highest average sale amount.",
"starter":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (rep TEXT, region TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    # TODO: insert 10+ rows, vary reps and regions
    # ("Alice", "North", 1200), ...
])
conn.commit()

# TODO: Query 1 — total and avg per region, ORDER BY total DESC
# rows = conn.execute(
#     "SELECT region, SUM(amount) as total, ROUND(AVG(amount),2) as avg_amt "
#     "FROM sales GROUP BY region ORDER BY total DESC"
# ).fetchall()
# for r in rows: print(r)

# TODO: Query 2 — reps with total sales > 3000
# rows = conn.execute(
#     "SELECT rep, SUM(amount) as total FROM sales "
#     "GROUP BY rep HAVING total > 3000"
# ).fetchall()
# print("High performers:", rows)

# TODO: Query 3 — region with highest average sale
# row = conn.execute(
#     "SELECT region, ROUND(AVG(amount),2) as avg_amt FROM sales "
#     "GROUP BY region ORDER BY avg_amt DESC LIMIT 1"
# ).fetchone()
# print("Best avg region:", row)

conn.close()"""
},
"rw": {
"title": "Monthly Spend Dashboard",
"scenario": "A finance analyst builds a monthly category spending dashboard from raw transaction records.",
"code":
"""import sqlite3, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE txn (user_id INT, category TEXT, amount REAL, date TEXT)")

cats = ["Food","Transport","Shopping","Entertainment","Utilities"]
rows = [
    (random.randint(1,100), random.choice(cats),
     round(random.uniform(5,300),2),
     (datetime.date(2024,1,1)+datetime.timedelta(days=random.randint(0,89))).isoformat())
    for _ in range(2000)
]
conn.executemany("INSERT INTO txn VALUES (?,?,?,?)", rows)

report = conn.execute(
    "SELECT category, COUNT(*) as txns,"
    "       ROUND(SUM(amount),2) as total,"
    "       ROUND(AVG(amount),2) as avg_amt,"
    "       ROUND(SUM(amount)*100.0/(SELECT SUM(amount) FROM txn),1) as pct "
    "FROM txn GROUP BY category ORDER BY total DESC"
).fetchall()

print(f"{'Category':15s} {'Txns':>5} {'Total':>10} {'Avg':>8} {'%':>6}")
print("-" * 50)
for r in report:
    print(f"{r[0]:15s} {r[1]:>5} ${r[2]:>9,.2f} ${r[3]:>7.2f} {r[4]:>5.1f}%")
conn.close()"""}
},

{
"title": "4. JOINs",
"desc": "JOINs combine rows from multiple tables. INNER keeps only matches; LEFT keeps all rows from the left table even without a match.",
"examples": [
{"label": "INNER JOIN and LEFT JOIN", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE dept (id INT, name TEXT)")
conn.execute("CREATE TABLE emp  (id INT, name TEXT, dept_id INT, salary REAL)")
conn.executemany("INSERT INTO dept VALUES (?,?)", [(1,"Eng"),(2,"HR"),(3,"Sales")])
conn.executemany("INSERT INTO emp VALUES (?,?,?,?)", [
    (1,"Alice",1,100000),(2,"Bob",2,65000),
    (3,"Carol",1,95000),(4,"Dave",3,80000),(5,"Eve",None,75000),
])

print("INNER JOIN:")
for r in conn.execute(
    "SELECT e.name, d.name, e.salary "
    "FROM emp e INNER JOIN dept d ON e.dept_id=d.id"
).fetchall(): print(" ", r)

print("LEFT JOIN (all employees):")
for r in conn.execute(
    "SELECT e.name, COALESCE(d.name,'Unknown'), e.salary "
    "FROM emp e LEFT JOIN dept d ON e.dept_id=d.id"
).fetchall(): print(" ", r)
conn.close()"""},
{"label": "Multi-table JOIN with aggregation", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (id INT, name TEXT, city TEXT)")
conn.execute("CREATE TABLE orders    (id INT, cust_id INT, amount REAL)")
conn.executemany("INSERT INTO customers VALUES (?,?,?)", [
    (1,"Alice","NYC"),(2,"Bob","LA"),(3,"Carol","NYC"),(4,"Dave","Chicago"),
])
conn.executemany("INSERT INTO orders VALUES (?,?,?)", [
    (1,1,150),(2,1,200),(3,2,80),(4,3,320),(5,3,100),
])

rows = conn.execute(
    "SELECT c.name, c.city, COUNT(o.id) as orders, "
    "       COALESCE(SUM(o.amount),0) as spent "
    "FROM customers c LEFT JOIN orders o ON c.id=o.cust_id "
    "GROUP BY c.id ORDER BY spent DESC"
).fetchall()
for r in rows: print(r)
conn.close()"""},
{"label": "Self-JOIN and multiple LEFT JOINs", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
# Self-join: employee + their manager
conn.execute("CREATE TABLE emp (id INT, name TEXT, mgr_id INT, dept TEXT)")
conn.executemany("INSERT INTO emp VALUES (?,?,?,?)", [
    (1,"CEO",None,"Exec"),(2,"CTO",1,"Tech"),(3,"CFO",1,"Finance"),
    (4,"Dev Lead",2,"Tech"),(5,"Alice",4,"Tech"),(6,"Bob",4,"Tech"),
])

print("Employee -> Manager:")
for r in conn.execute(
    "SELECT e.name as employee, COALESCE(m.name,'—') as manager, e.dept "
    "FROM emp e LEFT JOIN emp m ON e.mgr_id=m.id "
    "ORDER BY e.id"
).fetchall():
    print(f"  {r[0]:10s}  manager={r[1]:10s}  dept={r[2]}")

# Three-table join
conn.execute("CREATE TABLE projects (id INT, name TEXT, lead_id INT)")
conn.executemany("INSERT INTO projects VALUES (?,?,?)", [
    (1,"Alpha",4),(2,"Beta",2),(3,"Gamma",3),
])

print("Projects with leads and their department:")
for r in conn.execute(
    "SELECT p.name, e.name as lead, e.dept "
    "FROM projects p JOIN emp e ON p.lead_id=e.id"
).fetchall():
    print(f"  {r[0]:8s}  lead={r[1]:10s}  dept={r[2]}")
conn.close()"""},
{"label": "CROSS JOIN for cartesian product", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")

# CROSS JOIN produces every combination of rows (cartesian product)
conn.execute("CREATE TABLE sizes  (size TEXT)")
conn.execute("CREATE TABLE colors (color TEXT)")
conn.executemany("INSERT INTO sizes  VALUES (?)", [("S",),("M",),("L",),("XL",)])
conn.executemany("INSERT INTO colors VALUES (?)", [("Red",),("Blue",),("Green",)])

print("All size/color combinations (CROSS JOIN):")
variants = conn.execute(
    "SELECT s.size, c.color FROM sizes s CROSS JOIN colors c ORDER BY s.size, c.color"
).fetchall()
for r in variants:
    print(f"  {r[0]:4s} / {r[1]}")
print(f"Total variants: {len(variants)}")

# Use CROSS JOIN to build a multiplication table
print("3x3 multiplication table:")
conn.execute("CREATE TABLE nums (n INT)")
conn.executemany("INSERT INTO nums VALUES (?)", [(1,),(2,),(3,)])
for r in conn.execute(
    "SELECT a.n, b.n, a.n * b.n as product "
    "FROM nums a CROSS JOIN nums b ORDER BY a.n, b.n"
).fetchall():
    print(f"  {r[0]} x {r[1]} = {r[2]}")
conn.close()"""}
],
"practice": {
"title": "INNER and LEFT JOIN Queries",
"desc": "Create two tables: 'students' (id, name, grade) and 'enrollments' (student_id, course, score). Insert 5 students and 8 enrollments (some students have no enrollment). Write: 1) An INNER JOIN to show each student's course and score. 2) A LEFT JOIN to include students with no enrollment (show NULL for course). 3) Add a GROUP BY to show each student's average score.",
"starter":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE students (id INT, name TEXT, grade TEXT)")
conn.execute("CREATE TABLE enrollments (student_id INT, course TEXT, score REAL)")

conn.executemany("INSERT INTO students VALUES (?,?,?)", [
    # TODO: 5 students, at least one with no enrollment
    # (1,"Alice","A"), ...
])
conn.executemany("INSERT INTO enrollments VALUES (?,?,?)", [
    # TODO: 8 enrollments across the enrolled students
    # (1,"Math",88), ...
])
conn.commit()

# TODO: INNER JOIN — student name, course, score
# rows = conn.execute(
#     "SELECT s.name, e.course, e.score "
#     "FROM students s INNER JOIN enrollments e ON s.id=e.student_id"
# ).fetchall()
# print("Enrolled:")
# for r in rows: print(" ", r)

# TODO: LEFT JOIN — all students (NULL course for unenrolled)
# rows = conn.execute(
#     "SELECT s.name, COALESCE(e.course,'—') as course "
#     "FROM students s LEFT JOIN enrollments e ON s.id=e.student_id"
# ).fetchall()
# print("All students:")
# for r in rows: print(" ", r)

# TODO: Average score per student
# rows = conn.execute(
#     "SELECT s.name, ROUND(AVG(e.score),1) as avg_score "
#     "FROM students s JOIN enrollments e ON s.id=e.student_id "
#     "GROUP BY s.id ORDER BY avg_score DESC"
# ).fetchall()
# print("Avg scores:", rows)

conn.close()"""
},
"rw": {
"title": "Inventory & Sales Cross-Reference",
"scenario": "A warehouse manager joins product, inventory, and sales tables to identify stock risk for top-selling items.",
"code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
for ddl in [
    "CREATE TABLE products  (id INT, name TEXT, category TEXT)",
    "CREATE TABLE inventory (product_id INT, warehouse TEXT, qty INT)",
    "CREATE TABLE sales_30d (product_id INT, qty_sold INT)",
]:
    conn.execute(ddl)

conn.executemany("INSERT INTO products VALUES (?,?,?)", [
    (1,"Widget","Hardware"),(2,"Gadget","Electronics"),
    (3,"Doohickey","Hardware"),(4,"Gizmo","Electronics"),
])
conn.executemany("INSERT INTO inventory VALUES (?,?,?)", [
    (1,"East",500),(1,"West",300),(2,"East",80),(3,"West",200),(4,"East",50),
])
conn.executemany("INSERT INTO sales_30d VALUES (?,?)", [
    (1,420),(2,75),(3,60),(4,45),
])

rows = conn.execute(
    "SELECT p.name, p.category, SUM(i.qty) as stock, "
    "       COALESCE(s.qty_sold,0) as sold_30d, "
    "       ROUND(SUM(i.qty)*1.0/NULLIF(COALESCE(s.qty_sold,0),0),1) as weeks "
    "FROM products p "
    "JOIN inventory i ON p.id=i.product_id "
    "LEFT JOIN sales_30d s ON p.id=s.product_id "
    "GROUP BY p.id ORDER BY weeks ASC"
).fetchall()
print(f"{'Product':12s} {'Category':12s} {'Stock':>6} {'Sold':>6} {'Weeks':>6}")
for r in rows:
    print(f"{r[0]:12s} {r[1]:12s} {r[2]:>6} {r[3]:>6} {str(r[4]):>6}")
conn.close()"""}
},

{
"title": "5. Subqueries & CTEs",
"desc": "Subqueries run a query inside another. CTEs (WITH clause) make complex logic readable and reusable — they're like named temp tables.",
"examples": [
{"label": "Scalar subquery and IN subquery", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (name TEXT, dept TEXT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?,?)", [
    ("Alice","Eng",120000),("Bob","HR",65000),("Carol","Eng",95000),
    ("Dave","Mkt",80000),("Eve","Eng",110000),("Frank","HR",72000),
])

# Employees earning more than the company average
rows = conn.execute(
    "SELECT name, dept, salary FROM emp "
    "WHERE salary > (SELECT AVG(salary) FROM emp) "
    "ORDER BY salary DESC"
).fetchall()
print("Above-average earners:")
for r in rows: print(f"  {r[0]:8s} {r[1]:5s} ${r[2]:,}")
conn.close()"""},
{"label": "CTE (WITH clause)", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INT, cust TEXT, amount REAL, month TEXT)")
conn.executemany("INSERT INTO orders VALUES (?,?,?,?)", [
    (1,"Alice",100,"Jan"),(2,"Bob",200,"Jan"),
    (3,"Alice",150,"Feb"),(4,"Carol",300,"Feb"),
    (5,"Bob",250,"Mar"),(6,"Alice",400,"Mar"),
])

rows = conn.execute(
    "WITH monthly AS ("
    "  SELECT month, SUM(amount) as total FROM orders GROUP BY month"
    "),"
    "avg_m AS (SELECT AVG(total) as avg_total FROM monthly) "
    "SELECT m.month, m.total, "
    "       ROUND(m.total - a.avg_total, 2) as vs_avg "
    "FROM monthly m, avg_m a ORDER BY m.month"
).fetchall()
for r in rows: print(r)
conn.close()"""},
{"label": "Correlated subquery and EXISTS", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (id INT, name TEXT, dept TEXT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?,?,?)", [
    (1,"Alice","Eng",120000),(2,"Bob","HR",65000),(3,"Carol","Eng",95000),
    (4,"Dave","Mkt",80000),(5,"Eve","Eng",110000),(6,"Frank","HR",72000),
])

# Correlated subquery: employees earning above their own dept average
print("Above dept average:")
for r in conn.execute(
    "SELECT name, dept, salary, "
    "       ROUND((SELECT AVG(salary) FROM emp e2 WHERE e2.dept=e1.dept),0) as dept_avg "
    "FROM emp e1 "
    "WHERE salary > (SELECT AVG(salary) FROM emp e2 WHERE e2.dept=e1.dept) "
    "ORDER BY dept, salary DESC"
).fetchall():
    print(f"  {r[0]:8s} {r[1]:5s} ${r[2]:,}  dept_avg=${r[3]:,}")

# EXISTS subquery: departments that have at least one employee over 100k
print("Depts with 100k+ earner:")
for r in conn.execute(
    "SELECT DISTINCT dept FROM emp e1 "
    "WHERE EXISTS (SELECT 1 FROM emp e2 WHERE e2.dept=e1.dept AND e2.salary>100000)"
).fetchall():
    print(f"  {r[0]}")
conn.close()"""},
{"label": "Scalar subquery in SELECT and multi-CTE chain", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INT, cust TEXT, product TEXT, amount REAL, month INT)")
conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", [
    (1,"Alice","Widget",200,1),(2,"Bob","Gadget",150,1),(3,"Alice","Gadget",300,2),
    (4,"Carol","Widget",450,2),(5,"Bob","Widget",120,3),(6,"Alice","Gizmo",500,3),
    (7,"Carol","Gadget",250,3),(8,"Dave","Widget",80,1),
])

# Scalar subquery in SELECT: show each order's % of grand total
print("Each order as % of grand total:")
for r in conn.execute(
    "SELECT cust, product, amount,"
    "       ROUND(amount * 100.0 / (SELECT SUM(amount) FROM orders), 1) as pct_of_total "
    "FROM orders ORDER BY amount DESC"
).fetchall():
    print(f"  {r[0]:8s} {r[1]:8s} ${r[2]:>6.0f}  ({r[3]}%)")

# Multi-CTE chain: monthly totals -> rank months -> show top 2
print("Top 2 months by revenue:")
for r in conn.execute(
    "WITH monthly AS ("
    "  SELECT month, SUM(amount) as total FROM orders GROUP BY month"
    "),"
    "ranked AS ("
    "  SELECT month, total, RANK() OVER (ORDER BY total DESC) as rnk FROM monthly"
    ") "
    "SELECT month, total, rnk FROM ranked WHERE rnk <= 2 ORDER BY rnk"
).fetchall():
    print(f"  Month {r[0]}  total=${r[1]:.0f}  rank={r[2]}")
conn.close()"""}
],
"practice": {
"title": "Subquery in WHERE and CTE",
"desc": "Using an 'orders' table (id, customer, product, amount, order_date): 1) Write a subquery in WHERE to find orders with amount above the overall average. 2) Write a subquery in FROM (derived table) to get the top customer by total spend. 3) Write a WITH clause CTE that computes monthly totals, then selects only months above the average monthly total.",
"starter":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INT, customer TEXT, product TEXT, amount REAL, order_date TEXT)")
conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", [
    (1,"Alice","Widget",150,"2024-01-05"),
    (2,"Bob","Gadget",80,"2024-01-10"),
    (3,"Alice","Gadget",220,"2024-02-03"),
    (4,"Carol","Widget",310,"2024-02-15"),
    (5,"Bob","Widget",95,"2024-03-01"),
    (6,"Alice","Gizmo",400,"2024-03-20"),
    (7,"Carol","Gadget",175,"2024-04-08"),
    (8,"Dave","Widget",60,"2024-04-12"),
])
conn.commit()

# TODO: 1. Orders above overall average amount
# rows = conn.execute(
#     "SELECT customer, amount FROM orders "
#     "WHERE amount > (SELECT AVG(amount) FROM orders) "
#     "ORDER BY amount DESC"
# ).fetchall()
# print("Above avg:", rows)

# TODO: 2. Top customer by total spend (subquery in FROM)
# row = conn.execute(
#     "SELECT customer, total FROM "
#     "  (SELECT customer, SUM(amount) as total FROM orders GROUP BY customer) "
#     "ORDER BY total DESC LIMIT 1"
# ).fetchone()
# print("Top customer:", row)

# TODO: 3. CTE — months above average monthly total
# rows = conn.execute(
#     "WITH monthly AS ( "
#     "  SELECT strftime('%Y-%m', order_date) as month, SUM(amount) as total "
#     "  FROM orders GROUP BY month "
#     ") "
#     "SELECT month, total FROM monthly "
#     "WHERE total > (SELECT AVG(total) FROM monthly) "
#     "ORDER BY total DESC"
# ).fetchall()
# print("Above-avg months:", rows)

conn.close()"""
},
"rw": {
"title": "Customer Conversion Funnel Analysis",
"scenario": "A product analyst uses CTEs to compute step-by-step conversion rates through the signup funnel.",
"code":
"""import sqlite3, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE events (user_id INT, event TEXT, ts TEXT)")

random.seed(5)
funnel = ["signup","view_product","add_to_cart","purchase"]
rows = []
for uid in range(1, 501):
    n = random.randint(1, 4)
    base = datetime.datetime(2024,1,1) + datetime.timedelta(days=random.randint(0,60))
    for ev in funnel[:n]:
        rows.append((uid, ev, (base+datetime.timedelta(hours=random.randint(1,48))).isoformat()))
        base += datetime.timedelta(days=random.randint(0,3))
conn.executemany("INSERT INTO events VALUES (?,?,?)", rows)

report = conn.execute(
    "WITH steps AS ("
    "  SELECT event, COUNT(DISTINCT user_id) as users "
    "  FROM events "
    "  WHERE event IN ('signup','view_product','add_to_cart','purchase') "
    "  GROUP BY event"
    "),"
    "top AS (SELECT users as n FROM steps WHERE event='signup') "
    "SELECT event, users, "
    "       ROUND(users*100.0/(SELECT n FROM top),1) as pct "
    "FROM steps ORDER BY users DESC"
).fetchall()

print("Conversion Funnel:")
for r in report: print(f"  {r[0]:16s} {r[1]:4d} users ({r[2]}%)")
conn.close()"""}
},

{
"title": "6. Window Functions",
"desc": "Window functions compute values across rows related to the current row — ranking, running totals, lag/lead — without collapsing groups.",
"examples": [
{"label": "RANK, SUM OVER, percent of total", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (month TEXT, rep TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    ("Jan","Alice",5000),("Jan","Bob",4000),("Jan","Carol",6000),
    ("Feb","Alice",5500),("Feb","Bob",3800),("Feb","Carol",7000),
])

rows = conn.execute(
    "SELECT month, rep, amount,"
    "       RANK() OVER (PARTITION BY month ORDER BY amount DESC) as rnk,"
    "       SUM(amount) OVER (PARTITION BY month) as month_total,"
    "       ROUND(amount*100.0/SUM(amount) OVER (PARTITION BY month),1) as pct "
    "FROM sales ORDER BY month, rnk"
).fetchall()
for r in rows: print(r)
conn.close()"""},
{"label": "LAG, LEAD, moving average", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE rev (week INT, store TEXT, rev REAL)")
conn.executemany("INSERT INTO rev VALUES (?,?,?)", [
    (1,"A",10000),(2,"A",12000),(3,"A",9000),(4,"A",14000),(5,"A",11000),
    (1,"B",8000),(2,"B",9500),(3,"B",11000),(4,"B",10500),(5,"B",12000),
])

rows = conn.execute(
    "SELECT week, store, rev,"
    "       LAG(rev) OVER (PARTITION BY store ORDER BY week) as prev,"
    "       rev - LAG(rev) OVER (PARTITION BY store ORDER BY week) as wow,"
    "       AVG(rev) OVER (PARTITION BY store ORDER BY week "
    "                      ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as ma3 "
    "FROM rev ORDER BY store, week"
).fetchall()
for r in rows: print(r)
conn.close()"""},
{"label": "ROW_NUMBER, NTILE, and running total", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE scores (student TEXT, subject TEXT, score INT)")
conn.executemany("INSERT INTO scores VALUES (?,?,?)", [
    ("Alice","Math",92),("Bob","Math",78),("Carol","Math",85),
    ("Dave","Math",91),("Eve","Math",67),
    ("Alice","Science",88),("Bob","Science",95),("Carol","Science",72),
])

# ROW_NUMBER and RANK per subject
print("Math rankings:")
for r in conn.execute(
    "SELECT student, score,"
    "       ROW_NUMBER() OVER (ORDER BY score DESC) as row_num,"
    "       RANK()       OVER (ORDER BY score DESC) as rnk "
    "FROM scores WHERE subject='Math'"
).fetchall():
    print(f"  {r[0]:8s}  score={r[1]}  row={r[2]}  rank={r[3]}")

# Running total
print("Running total (Math by score):")
for r in conn.execute(
    "SELECT student, score,"
    "       SUM(score) OVER (ORDER BY score DESC ROWS UNBOUNDED PRECEDING) as running_total "
    "FROM scores WHERE subject='Math' ORDER BY score DESC"
).fetchall():
    print(f"  {r[0]:8s}  score={r[1]}  running_total={r[2]}")
conn.close()"""},
{"label": "FIRST_VALUE, LAST_VALUE, and NTILE", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (rep TEXT, month TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    ("Alice","Jan",5000),("Alice","Feb",6200),("Alice","Mar",4800),
    ("Alice","Apr",7100),("Alice","May",5500),("Alice","Jun",6800),
    ("Bob","Jan",4200),("Bob","Feb",3800),("Bob","Mar",5100),
    ("Bob","Apr",4600),("Bob","May",5900),("Bob","Jun",4300),
])

# FIRST_VALUE and LAST_VALUE show best/worst months in the window
print("First and last month amount per rep (by month order):")
for r in conn.execute(
    "SELECT rep, month, amount,"
    "       FIRST_VALUE(amount) OVER (PARTITION BY rep ORDER BY month "
    "                                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as first_month,"
    "       LAST_VALUE(amount)  OVER (PARTITION BY rep ORDER BY month "
    "                                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_month "
    "FROM sales ORDER BY rep, month"
).fetchall():
    print(f"  {r[0]:6s} {r[1]:4s} ${r[2]:>6,.0f}  first=${r[3]:>6,.0f}  last=${r[4]:>6,.0f}")

# NTILE divides rows into N equal buckets (quartiles here)
print("NTILE(3) buckets for Alice:")
for r in conn.execute(
    "SELECT month, amount, NTILE(3) OVER (ORDER BY amount DESC) as bucket "
    "FROM sales WHERE rep='Alice' ORDER BY bucket, amount DESC"
).fetchall():
    print(f"  bucket={r[2]}  {r[0]}  ${r[1]:,.0f}")
conn.close()"""}
],
"practice": {
"title": "ROW_NUMBER and RANK Window Functions",
"desc": "Create a 'sales' table with columns rep (TEXT), month (TEXT), amount (REAL). Insert data for 3 reps across 4 months. Write a query using: 1) RANK() OVER (PARTITION BY month ORDER BY amount DESC) to rank reps each month. 2) SUM(amount) OVER (PARTITION BY rep ORDER BY month) for a running total per rep. 3) LAG(amount) to compute month-over-month change per rep.",
"starter":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (rep TEXT, month TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    ("Alice","Jan",5000),("Bob","Jan",4200),("Carol","Jan",6100),
    ("Alice","Feb",5500),("Bob","Feb",3900),("Carol","Feb",7200),
    ("Alice","Mar",4800),("Bob","Mar",5100),("Carol","Mar",6800),
    ("Alice","Apr",6000),("Bob","Apr",4600),("Carol","Apr",5900),
])
conn.commit()

# TODO: 1. Rank reps within each month by amount DESC
# rows = conn.execute(
#     "SELECT month, rep, amount, "
#     "       RANK() OVER (PARTITION BY month ORDER BY amount DESC) as rnk "
#     "FROM sales ORDER BY month, rnk"
# ).fetchall()
# for r in rows: print(r)

# TODO: 2. Running total of amount per rep, ordered by month
# rows = conn.execute(
#     "SELECT rep, month, amount, "
#     "       SUM(amount) OVER (PARTITION BY rep ORDER BY month "
#     "                         ROWS UNBOUNDED PRECEDING) as running_total "
#     "FROM sales ORDER BY rep, month"
# ).fetchall()
# for r in rows: print(r)

# TODO: 3. Month-over-month change per rep using LAG
# rows = conn.execute(
#     "SELECT rep, month, amount, "
#     "       LAG(amount) OVER (PARTITION BY rep ORDER BY month) as prev_month, "
#     "       amount - LAG(amount) OVER (PARTITION BY rep ORDER BY month) as change "
#     "FROM sales ORDER BY rep, month"
# ).fetchall()
# for r in rows: print(r)

conn.close()"""
},
"rw": {
"title": "Moving Average Trading Signals",
"scenario": "A quant uses window functions to flag days when price crosses above the 3-period moving average — a simple trend signal.",
"code":
"""import sqlite3, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE prices (id INT, symbol TEXT, price REAL, date TEXT)")

random.seed(10)
for sym in ["AAPL","GOOG"]:
    p = random.uniform(150, 400)
    for d in range(20):
        p *= (1 + random.gauss(0.001, 0.015))
        date = (datetime.date(2024,1,2)+datetime.timedelta(days=d)).isoformat()
        conn.execute("INSERT INTO prices VALUES (?,?,?,?)",
                     (d+1 if sym=="AAPL" else d+21, sym, round(p,2), date))
conn.commit()

result = conn.execute(
    "SELECT symbol, date, price,"
    "       ROUND(AVG(price) OVER (PARTITION BY symbol ORDER BY date "
    "                              ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) as ma3,"
    "       CASE WHEN price > AVG(price) OVER "
    "            (PARTITION BY symbol ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)"
    "            THEN 'BUY' ELSE 'HOLD' END as signal "
    "FROM prices WHERE symbol='AAPL' ORDER BY date LIMIT 8"
).fetchall()

print(f"{'Date':12s} {'Price':>8} {'MA3':>8} {'Signal':>7}")
for r in result:
    print(f"{r[1]} {r[2]:>8.2f} {r[3]:>8.2f} {r[4]:>7}")
conn.close()"""}
},

{
"title": "7. UPDATE & DELETE",
"desc": "UPDATE modifies existing rows. DELETE removes rows. Always use WHERE — without it you affect the entire table.",
"examples": [
{"label": "UPDATE with conditions", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE inventory (id INT, item TEXT, qty INT, price REAL)")
conn.executemany("INSERT INTO inventory VALUES (?,?,?,?)", [
    (1,"Widget",100,9.99),(2,"Gadget",50,49.99),(3,"Doohickey",200,4.99),
])

# Raise price 10% for low-stock items
conn.execute("UPDATE inventory SET price=ROUND(price*1.1,2) WHERE qty < 100")
# Discontinue very cheap items
conn.execute("DELETE FROM inventory WHERE price < 5")
conn.commit()

print("After update/delete:")
for r in conn.execute("SELECT * FROM inventory").fetchall():
    print(f"  {r[1]:12s} qty={r[2]:4d} price=${r[3]:.2f}")
conn.close()"""},
{"label": "UPSERT (INSERT OR REPLACE / ON CONFLICT)", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE config ("
    "  key TEXT PRIMARY KEY, value TEXT, updated_at TEXT)"
)

def upsert(key, value, ts):
    conn.execute(
        "INSERT INTO config VALUES (?,?,?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
        (key, value, ts)
    )
    conn.commit()

upsert("theme",     "dark",  "2024-01-01")
upsert("page_size", "25",    "2024-01-01")
upsert("theme",     "light", "2024-03-01")   # update existing

for r in conn.execute("SELECT * FROM config").fetchall():
    print(r)
conn.close()"""},
{"label": "Bulk UPDATE with JOIN-like subquery", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE products (id INT, name TEXT, category TEXT, price REAL)")
conn.execute("CREATE TABLE discounts (category TEXT, pct REAL)")

conn.executemany("INSERT INTO products VALUES (?,?,?,?)", [
    (1,"Widget","Hardware",10.00),(2,"Gadget","Electronics",50.00),
    (3,"Cable","Electronics",8.00),(4,"Hammer","Hardware",25.00),
    (5,"Phone","Electronics",600.00),
])
conn.executemany("INSERT INTO discounts VALUES (?,?)", [
    ("Electronics",0.10),("Hardware",0.05),
])
conn.commit()

# Apply per-category discount using subquery in SET
conn.execute(
    "UPDATE products SET price = ROUND(price * (1 - "
    "  (SELECT pct FROM discounts d WHERE d.category=products.category)), 2) "
    "WHERE category IN (SELECT category FROM discounts)"
)
conn.commit()

print("After category discounts:")
for r in conn.execute("SELECT name, category, price FROM products ORDER BY category, price").fetchall():
    print(f"  {r[0]:10s} {r[1]:14s} ${r[2]:.2f}")
conn.close()"""},
{"label": "INSERT OR IGNORE and INSERT OR REPLACE (UPSERT patterns)", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE page_views ("
    "  url TEXT PRIMARY KEY, views INT, last_seen TEXT)"
)

# INSERT OR IGNORE — skip if the primary key already exists
initial = [
    ("https://example.com/home",  100, "2024-01-01"),
    ("https://example.com/about",  40, "2024-01-01"),
    ("https://example.com/blog",   75, "2024-01-01"),
]
conn.executemany("INSERT OR IGNORE INTO page_views VALUES (?,?,?)", initial)
# Try to insert a duplicate — silently ignored
conn.execute("INSERT OR IGNORE INTO page_views VALUES (?,?,?)",
             ("https://example.com/home", 999, "2024-06-01"))

print("After INSERT OR IGNORE:")
for r in conn.execute("SELECT url, views FROM page_views").fetchall():
    print(f"  {r[0]:40s}  views={r[1]}")

# INSERT OR REPLACE — delete + re-insert if conflict (resets the whole row)
conn.execute("INSERT OR REPLACE INTO page_views VALUES (?,?,?)",
             ("https://example.com/home", 250, "2024-06-01"))

print("After INSERT OR REPLACE (home views updated to 250):")
for r in conn.execute("SELECT url, views, last_seen FROM page_views").fetchall():
    print(f"  {r[0]:40s}  views={r[1]}  last_seen={r[2]}")
conn.close()"""}
],
"practice": {
"title": "Transaction with Error Handling",
"desc": "Create an 'accounts' table (id, owner, balance). Insert 3 accounts. Write a transfer function that: 1) Checks the sender has sufficient balance. 2) DECREMENTs the sender's balance and INCREMENTs the receiver's balance inside a transaction. 3) Rolls back if any error occurs. Test both a successful transfer and a failing one (insufficient funds).",
"starter":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE accounts (id INT PRIMARY KEY, owner TEXT, balance REAL)")
conn.executemany("INSERT INTO accounts VALUES (?,?,?)", [
    (1, "Alice", 1000.0),
    (2, "Bob",    500.0),
    (3, "Carol",  250.0),
])
conn.commit()

def get_balance(conn, account_id):
    row = conn.execute("SELECT balance FROM accounts WHERE id=?", (account_id,)).fetchone()
    return row[0] if row else None

def transfer(conn, from_id, to_id, amount):
    # TODO: Check sender balance
    # balance = get_balance(conn, from_id)
    # if balance is None or balance < amount:
    #     print(f"Transfer failed: insufficient funds (balance={balance})")
    #     return False

    # TODO: Perform transfer in a transaction
    # try:
    #     conn.execute("UPDATE accounts SET balance=balance-? WHERE id=?", (amount, from_id))
    #     conn.execute("UPDATE accounts SET balance=balance+? WHERE id=?", (amount, to_id))
    #     conn.commit()
    #     print(f"Transferred ${amount} from account {from_id} to {to_id}")
    #     return True
    # except Exception as e:
    #     conn.rollback()
    #     print(f"Transfer error: {e}")
    #     return False
    pass

# TODO: Test successful transfer: Alice -> Bob, $200
# transfer(conn, 1, 2, 200)

# TODO: Test failing transfer: Carol -> Alice, $500 (Carol only has $250)
# transfer(conn, 3, 1, 500)

# TODO: Print final balances
# for r in conn.execute("SELECT owner, balance FROM accounts").fetchall():
#     print(f"  {r[0]:8s} ${r[1]:.2f}")

conn.close()"""
},
"rw": {
"title": "Subscription Lifecycle Automation",
"scenario": "A SaaS platform batch-expires overdue subscriptions and applies loyalty discounts to long-term customers.",
"code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE subs ("
    "  id INT, user TEXT, plan TEXT, price REAL,"
    "  start_date TEXT, end_date TEXT, status TEXT)"
)
conn.executemany("INSERT INTO subs VALUES (?,?,?,?,?,?,?)", [
    (1,"Alice","basic",  9.99,"2024-01-01","2024-12-31","active"),
    (2,"Bob",  "pro",   29.99,"2023-01-01","2024-01-15","active"),
    (3,"Carol","basic",  9.99,"2024-01-01","2024-06-30","active"),
    (4,"Dave", "ent",   99.99,"2022-01-01","2024-12-31","active"),
])

today = "2024-07-01"
# Expire overdue subscriptions
conn.execute("UPDATE subs SET status='expired' WHERE end_date < ?", (today,))
# 15% discount for customers active >= 2 years
conn.execute(
    "UPDATE subs SET price=ROUND(price*0.85,2) "
    "WHERE status='active' "
    "AND CAST(strftime('%Y',?) AS INT) - CAST(strftime('%Y',start_date) AS INT) >= 2",
    (today,)
)
conn.commit()

print(f"{'User':8s} {'Plan':6s} {'Price':>8} {'Status':>8}")
for r in conn.execute("SELECT user,plan,price,status FROM subs").fetchall():
    print(f"{r[0]:8s} {r[1]:6s} ${r[2]:>7.2f} {r[3]:>8}")
conn.close()"""}
},

{
"title": "8. Indexes & EXPLAIN",
"desc": "Indexes dramatically speed up queries on large tables. Use EXPLAIN QUERY PLAN to see whether SQLite uses your indexes.",
"examples": [
{"label": "Measure index speedup", "code":
"""import sqlite3, time, random

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE events (id INT, user_id INT, event_type TEXT, ts TEXT)")
rows = [(i, random.randint(1,10000), random.choice(["click","view","buy"]),
         f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}")
        for i in range(200000)]
conn.executemany("INSERT INTO events VALUES (?,?,?,?)", rows)
conn.commit()

t0 = time.perf_counter()
conn.execute("SELECT COUNT(*) FROM events WHERE user_id=42").fetchone()
no_idx = time.perf_counter() - t0

conn.execute("CREATE INDEX idx_user ON events(user_id)")

t0 = time.perf_counter()
conn.execute("SELECT COUNT(*) FROM events WHERE user_id=42").fetchone()
with_idx = time.perf_counter() - t0

print(f"No index:   {no_idx*1000:.2f}ms")
print(f"With index: {with_idx*1000:.2f}ms")
print(f"Speedup:    {no_idx/max(with_idx,1e-9):.0f}x")
conn.close()"""},
{"label": "EXPLAIN QUERY PLAN", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INT, cust TEXT, status TEXT, amount REAL)")
conn.execute("CREATE INDEX idx_status ON orders(status)")

plan = conn.execute(
    "EXPLAIN QUERY PLAN "
    "SELECT cust, SUM(amount) FROM orders "
    "WHERE status='pending' GROUP BY cust"
).fetchall()

print("Query plan:")
for row in plan: print(" ", row)
conn.close()"""},
{"label": "Partial index and UNIQUE index", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE users ("
    "  id INT PRIMARY KEY, email TEXT UNIQUE, role TEXT, active INT)"
)
conn.executemany("INSERT INTO users VALUES (?,?,?,?)", [
    (1,"alice@x.com","admin",1),(2,"bob@x.com","user",1),
    (3,"carol@x.com","user",0),(4,"dave@x.com","mod",1),
])

# UNIQUE index is implicit on email — test enforcement
try:
    conn.execute("INSERT INTO users VALUES (5,'alice@x.com','user',1)")
except Exception as e:
    print("UNIQUE violation caught:", e)

# Partial-like index: index only active users
conn.execute("CREATE INDEX idx_active_role ON users(role) WHERE active=1")

# Verify index is used
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM users WHERE role='admin' AND active=1"
).fetchall()
print("Query plan (with partial index):")
for row in plan: print(" ", row)

# Count using the index
n = conn.execute("SELECT COUNT(*) FROM users WHERE active=1").fetchone()[0]
print(f"Active users: {n}")
conn.close()"""},
{"label": "Covering index and EXPLAIN QUERY PLAN comparison", "code":
"""import sqlite3, time, random

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE orders ("
    "  id INT, cust_id INT, status TEXT, amount REAL, created TEXT)"
)
rows = [
    (i, random.randint(1, 500), random.choice(["pending","shipped","done"]),
     round(random.uniform(10, 1000), 2),
     f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}")
    for i in range(100000)
]
conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
conn.commit()

# Query that only needs (status, amount) — a covering index can satisfy it entirely
query = (
    "SELECT status, SUM(amount) as total "
    "FROM orders WHERE status='pending' GROUP BY status"
)

# Without covering index
plan_before = conn.execute("EXPLAIN QUERY PLAN " + query).fetchall()
t0 = time.perf_counter()
conn.execute(query).fetchall()
t_before = time.perf_counter() - t0

# Create a covering index — includes all columns touched by the query
conn.execute("CREATE INDEX idx_cover ON orders(status, amount)")

plan_after = conn.execute("EXPLAIN QUERY PLAN " + query).fetchall()
t0 = time.perf_counter()
conn.execute(query).fetchall()
t_after = time.perf_counter() - t0

print("Plan WITHOUT covering index:", plan_before[0][-1] if plan_before else "N/A")
print("Plan WITH covering index:   ", plan_after[0][-1]  if plan_after  else "N/A")
print(f"Time before: {t_before*1000:.2f}ms  after: {t_after*1000:.2f}ms")
conn.close()"""}
],
"practice": {
"title": "Create Appropriate Indexes",
"desc": "Create a 'log_events' table with 100,000 rows: columns id, user_id (1-1000), event_type ('login','logout','purchase','view'), created_at (date string). 1) Measure query time for SELECT WHERE user_id=42 without an index. 2) Create a single-column index on user_id and re-measure. 3) Create a compound index on (event_type, created_at) and verify with EXPLAIN QUERY PLAN.",
"starter":
"""import sqlite3, random, time, datetime

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE log_events (id INT, user_id INT, event_type TEXT, created_at TEXT)"
)

base = datetime.date(2024, 1, 1)
events = ["login", "logout", "purchase", "view"]
rows = [
    (i, random.randint(1, 1000), random.choice(events),
     (base + datetime.timedelta(days=random.randint(0, 180))).isoformat())
    for i in range(1, 100001)
]
conn.executemany("INSERT INTO log_events VALUES (?,?,?,?)", rows)
conn.commit()

# TODO: 1. Time query WITHOUT index
# t0 = time.perf_counter()
# conn.execute("SELECT COUNT(*) FROM log_events WHERE user_id=42").fetchone()
# print(f"No index: {(time.perf_counter()-t0)*1000:.2f}ms")

# TODO: 2. Create index on user_id and re-time
# conn.execute("CREATE INDEX idx_user_id ON log_events(user_id)")
# t0 = time.perf_counter()
# conn.execute("SELECT COUNT(*) FROM log_events WHERE user_id=42").fetchone()
# print(f"With index: {(time.perf_counter()-t0)*1000:.2f}ms")

# TODO: 3. Compound index on (event_type, created_at)
# conn.execute("CREATE INDEX idx_event_date ON log_events(event_type, created_at)")
# plan = conn.execute(
#     "EXPLAIN QUERY PLAN SELECT * FROM log_events "
#     "WHERE event_type='purchase' AND created_at >= '2024-06-01'"
# ).fetchall()
# print("Query plan:", plan)

conn.close()"""
},
"rw": {
"title": "E-Commerce Report with Compound Indexes",
"scenario": "A backend engineer adds compound indexes to cut a cross-table analytics report from seconds to milliseconds.",
"code":
"""import sqlite3, time, random, datetime

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE orders ("
    "  id INT, cust_id INT, product_id INT,"
    "  status TEXT, amount REAL, created TEXT)"
)
conn.execute("CREATE TABLE products (id INT PRIMARY KEY, name TEXT, category TEXT)")

conn.executemany("INSERT INTO products VALUES (?,?,?)", [
    (i, f"Prod{i}", random.choice(["Electronics","Food","Clothing","Hardware"]))
    for i in range(1, 201)
])
rows = [(i, random.randint(1,5000), random.randint(1,200),
         random.choice(["pending","shipped","delivered"]),
         round(random.uniform(10,1000),2),
         (datetime.date(2024,1,1)+datetime.timedelta(days=random.randint(0,90))).isoformat())
        for i in range(1,50001)]
conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", rows)

for idx in [
    "CREATE INDEX idx_status ON orders(status, created)",
    "CREATE INDEX idx_prod   ON orders(product_id)",
]:
    conn.execute(idx)

t0 = time.perf_counter()
result = conn.execute(
    "SELECT p.category, o.status, COUNT(*) as cnt, ROUND(SUM(o.amount),2) as rev "
    "FROM orders o JOIN products p ON o.product_id=p.id "
    "WHERE o.status != 'pending' "
    "GROUP BY p.category, o.status ORDER BY rev DESC LIMIT 8"
).fetchall()
print(f"Query: {(time.perf_counter()-t0)*1000:.1f}ms  ({len(result)} rows)")
for r in result[:4]:
    print(f"  {r[0]:14s} | {r[1]:10s} | {r[2]:>5d} | ${r[3]:>10,.2f}")
conn.close()"""}
},

{
"title": "9. SQLite with Pandas",
"desc": "Pandas integrates directly with SQLite: read query results into DataFrames with pd.read_sql(), write DataFrames back with .to_sql().",
"examples": [
{"label": "read_sql and to_sql", "code":
"""import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (date TEXT, region TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    ("2024-01-01","North",1200),("2024-01-01","South",800),
    ("2024-01-02","North",950),("2024-01-02","East",1100),
])

# SQL → DataFrame
df = pd.read_sql("SELECT * FROM sales", conn)
print(df)
print(df.groupby("region")["amount"].sum())
conn.close()"""},
{"label": "Write DataFrame to SQL and query back", "code":
"""import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect(":memory:")
df = pd.DataFrame({
    "date":     pd.date_range("2024-01-01", periods=30).astype(str),
    "value":    np.random.randn(30).cumsum() + 100,
    "category": np.random.choice(["A","B","C"], 30),
})
df.to_sql("ts", conn, index=False, if_exists="replace")

result = pd.read_sql(
    "SELECT category, COUNT(*) as n, ROUND(AVG(value),2) as avg_val "
    "FROM ts GROUP BY category ORDER BY avg_val DESC",
    conn
)
print(result)
conn.close()"""},
{"label": "Parameterized queries and chunksize", "code":
"""import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect(":memory:")
np.random.seed(7)

# Build a large DataFrame and write in chunks
df = pd.DataFrame({
    "user_id":  np.random.randint(1, 201, 5000),
    "product":  np.random.choice(["A","B","C","D"], 5000),
    "amount":   np.round(np.random.uniform(5, 500, 5000), 2),
    "month":    np.random.choice(["Jan","Feb","Mar","Apr"], 5000),
})
df.to_sql("txn", conn, index=False, if_exists="replace", chunksize=1000)

# Parameterized SQL via pd.read_sql with params argument
month_filter = "Mar"
result = pd.read_sql(
    "SELECT product, COUNT(*) as sales, ROUND(SUM(amount),2) as revenue "
    "FROM txn WHERE month=? GROUP BY product ORDER BY revenue DESC",
    conn, params=(month_filter,)
)
print(f"Sales in {month_filter}:")
print(result.to_string(index=False))
conn.close()"""},
{"label": "to_sql if_exists modes and dtype mapping", "code":
"""import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect(":memory:")
np.random.seed(3)

base_df = pd.DataFrame({
    "id":     range(1, 11),
    "name":   [f"Product_{i}" for i in range(1, 11)],
    "price":  np.round(np.random.uniform(5, 200, 10), 2),
    "stock":  np.random.randint(0, 500, 10),
})

# First write: create the table
base_df.to_sql("products", conn, index=False, if_exists="replace")
print(f"Initial rows: {pd.read_sql('SELECT COUNT(*) as n FROM products', conn).iloc[0,0]}")

# Append new rows with if_exists='append'
new_rows = pd.DataFrame({
    "id": [11, 12], "name": ["Product_11","Product_12"],
    "price": [19.99, 34.99], "stock": [100, 50],
})
new_rows.to_sql("products", conn, index=False, if_exists="append")
print(f"After append:  {pd.read_sql('SELECT COUNT(*) as n FROM products', conn).iloc[0,0]}")

# Replace entirely with if_exists='replace'
replacement = base_df.head(3).copy()
replacement.to_sql("products", conn, index=False, if_exists="replace")
print(f"After replace: {pd.read_sql('SELECT COUNT(*) as n FROM products', conn).iloc[0,0]}")

# Read back with column type check
df_back = pd.read_sql("SELECT * FROM products", conn)
print(df_back.dtypes.to_string())
conn.close()"""}
],
"practice": {
"title": "Create a View for a Report Query",
"desc": "Create a 'transactions' table (id, customer, category, amount, txn_date) and populate it. Then: 1) CREATE VIEW monthly_summary AS a query grouping by month and category with totals. 2) SELECT from the view to display the report. 3) Use pd.read_sql() to load the view result into a DataFrame and show the top 3 rows by revenue.",
"starter":
"""import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect(":memory:")
np.random.seed(42)

conn.execute(
    "CREATE TABLE transactions "
    "(id INT, customer TEXT, category TEXT, amount REAL, txn_date TEXT)"
)
import datetime, random
base = datetime.date(2024, 1, 1)
cats = ["Food", "Electronics", "Clothing", "Sports"]
customers = ["Alice","Bob","Carol","Dave","Eve"]
rows = [
    (i, random.choice(customers), random.choice(cats),
     round(random.uniform(10, 300), 2),
     (base + datetime.timedelta(days=random.randint(0, 89))).isoformat())
    for i in range(1, 201)
]
conn.executemany("INSERT INTO transactions VALUES (?,?,?,?,?)", rows)
conn.commit()

# TODO: 1. Create a VIEW named 'monthly_summary'
# conn.execute(
#     "CREATE VIEW monthly_summary AS "
#     "SELECT strftime('%Y-%m', txn_date) as month, "
#     "       category, COUNT(*) as txns, ROUND(SUM(amount),2) as revenue "
#     "FROM transactions GROUP BY month, category"
# )

# TODO: 2. Query the view directly
# for r in conn.execute("SELECT * FROM monthly_summary ORDER BY revenue DESC LIMIT 5").fetchall():
#     print(r)

# TODO: 3. Load into DataFrame and show top 3 by revenue
# df = pd.read_sql("SELECT * FROM monthly_summary ORDER BY revenue DESC", conn)
# print(df.head(3).to_string(index=False))

conn.close()"""
},
"rw": {
"title": "Multi-Source Analytics Report",
"scenario": "A data analyst joins two normalized SQL tables via pandas to produce a segmented revenue report for stakeholders.",
"code":
"""import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect(":memory:")

customers = pd.DataFrame({
    "id":      range(1, 101),
    "segment": np.random.choice(["retail","wholesale","online"], 100),
    "region":  np.random.choice(["North","South","East","West"], 100),
})
transactions = pd.DataFrame({
    "customer_id": np.random.randint(1, 101, 2000),
    "product":     np.random.choice(["A","B","C","D"], 2000),
    "amount":      np.random.uniform(10, 500, 2000).round(2),
})

customers.to_sql("customers", conn, index=False)
transactions.to_sql("transactions", conn, index=False)

report = pd.read_sql(
    "SELECT c.segment, c.region, "
    "       COUNT(DISTINCT t.customer_id) as customers, "
    "       ROUND(SUM(t.amount),2) as revenue, "
    "       ROUND(AVG(t.amount),2) as avg_order "
    "FROM transactions t "
    "JOIN customers c ON t.customer_id=c.id "
    "GROUP BY c.segment, c.region "
    "ORDER BY revenue DESC LIMIT 8",
    conn
)
print(report.to_string(index=False))
conn.close()"""}
},

{
"title": "10. Recursive CTEs & Advanced Patterns",
"desc": "Recursive CTEs traverse hierarchical data (org charts, tree structures). CASE expressions and COALESCE handle conditional logic elegantly.",
"examples": [
{"label": "Recursive CTE — org hierarchy", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE emp (id INT, name TEXT, mgr_id INT, salary REAL)")
conn.executemany("INSERT INTO emp VALUES (?,?,?,?)", [
    (1,"CEO",None,300000),(2,"CTO",1,200000),(3,"CFO",1,190000),
    (4,"Dev Lead",2,130000),(5,"Dev1",4,100000),(6,"Dev2",4,95000),
    (7,"Finance1",3,80000),
])

rows = conn.execute(
    "WITH RECURSIVE org AS ("
    "  SELECT id, name, mgr_id, 0 AS depth FROM emp WHERE mgr_id IS NULL "
    "  UNION ALL "
    "  SELECT e.id, e.name, e.mgr_id, o.depth+1 "
    "  FROM emp e JOIN org o ON e.mgr_id=o.id"
    ") "
    "SELECT depth, name FROM org ORDER BY depth, name"
).fetchall()
for d, name in rows:
    print("  " * d + name)
conn.close()"""},
{"label": "CASE expression and COALESCE", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INT, amount REAL, status TEXT)")
conn.executemany("INSERT INTO orders VALUES (?,?,?)", [
    (1,500,"delivered"),(2,120,"pending"),(3,None,"cancelled"),
    (4,800,"delivered"),(5,200,"shipped"),(6,None,"pending"),
])

rows = conn.execute(
    "SELECT id,"
    "       COALESCE(amount, 0) as safe_amount,"
    "       CASE "
    "         WHEN amount > 500 THEN 'high'"
    "         WHEN amount > 100 THEN 'medium'"
    "         WHEN amount IS NULL THEN 'unknown'"
    "         ELSE 'low'"
    "       END as tier,"
    "       status "
    "FROM orders ORDER BY id"
).fetchall()
for r in rows: print(r)
conn.close()"""},
{"label": "Fibonacci sequence via recursive CTE", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")

# Generate Fibonacci numbers using a recursive CTE
rows = conn.execute(
    "WITH RECURSIVE fib(n, a, b) AS ("
    "  SELECT 1, 0, 1 "
    "  UNION ALL "
    "  SELECT n+1, b, a+b FROM fib WHERE n < 15"
    ") "
    "SELECT n, a as fib_value FROM fib"
).fetchall()
print("Fibonacci sequence:")
for n, v in rows:
    print(f"  F({n:2d}) = {v}")

# Generate a date series using recursive CTE
rows2 = conn.execute(
    "WITH RECURSIVE dates(d) AS ("
    "  SELECT '2024-01-01' "
    "  UNION ALL "
    "  SELECT date(d, '+1 day') FROM dates WHERE d < '2024-01-07'"
    ") "
    "SELECT d, strftime('%A', d) as weekday FROM dates"
).fetchall()
print("Week of 2024-01-01:")
for d, wd in rows2:
    print(f"  {d}  {wd}")
conn.close()"""},
{"label": "Updatable View & View with Parameters via CTE", "code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
c = conn.cursor()
c.executescript(
    "CREATE TABLE employees ("
    "    id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary REAL, hire_date TEXT"
    ");"
    "INSERT INTO employees VALUES"
    "    (1,'Alice','Engineering',95000,'2020-03-15'),"
    "    (2,'Bob','Marketing',72000,'2019-07-01'),"
    "    (3,'Carol','Engineering',105000,'2018-11-20'),"
    "    (4,'Dave','HR',65000,'2021-02-28'),"
    "    (5,'Eve','Marketing',78000,'2020-09-10'),"
    "    (6,'Frank','Engineering',88000,'2022-01-05');"
)

# View: department salary summary
c.execute(
    "CREATE VIEW dept_summary AS "
    "SELECT dept, COUNT(*) AS headcount, "
    "       ROUND(AVG(salary),2) AS avg_salary, "
    "       MAX(salary) AS max_salary, MIN(salary) AS min_salary "
    "FROM employees GROUP BY dept"
)

# View: employees with tenure
c.execute(
    "CREATE VIEW emp_tenure AS "
    "SELECT name, dept, salary, "
    "       ROUND((julianday('now') - julianday(hire_date)) / 365.25, 1) AS years_tenure "
    "FROM employees"
)

# Query the views
print("Department summary:")
c.execute("SELECT * FROM dept_summary ORDER BY avg_salary DESC")
for row in c.fetchall():
    print(f"  {row[0]:12s} headcount={row[1]}, avg=${row[2]:,.0f}, max=${row[3]:,.0f}")

print("\\nEmployee tenure:")
c.execute("SELECT * FROM emp_tenure WHERE years_tenure > 3 ORDER BY years_tenure DESC")
for row in c.fetchall():
    print(f"  {row[0]:6s} ({row[1]}) - {row[3]} years, ${row[2]:,.0f}")

# Drop view
c.execute("DROP VIEW emp_tenure")
print("\\nViews remaining:", [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='view'")])
conn.close()"""}
],
"practice": {
"title": "Write a WITH Clause (CTE) Query",
"desc": "Create a 'sales' table (rep, quarter, amount). Insert data for 3 reps over 4 quarters. Write a CTE query that: 1) Computes total sales per rep (CTE: rep_totals). 2) Computes the company-wide average rep total (CTE: company_avg). 3) Final SELECT shows each rep's total and whether they are 'above_avg', 'average', or 'below_avg' using CASE.",
"starter":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE sales (rep TEXT, quarter TEXT, amount REAL)")
conn.executemany("INSERT INTO sales VALUES (?,?,?)", [
    ("Alice","Q1",12000),("Alice","Q2",15000),("Alice","Q3",11000),("Alice","Q4",18000),
    ("Bob","Q1",9000),("Bob","Q2",10500),("Bob","Q3",12000),("Bob","Q4",8500),
    ("Carol","Q1",20000),("Carol","Q2",18500),("Carol","Q3",22000),("Carol","Q4",19000),
])
conn.commit()

# TODO: Write a CTE query
# rows = conn.execute(
#     "WITH rep_totals AS ( "
#     "  SELECT rep, SUM(amount) as total FROM sales GROUP BY rep "
#     "), "
#     "company_avg AS ( "
#     "  SELECT AVG(total) as avg_total FROM rep_totals "
#     ") "
#     "SELECT r.rep, r.total, "
#     "       CASE "
#     "         WHEN r.total > c.avg_total * 1.1 THEN 'above_avg' "
#     "         WHEN r.total < c.avg_total * 0.9 THEN 'below_avg' "
#     "         ELSE 'average' "
#     "       END as performance "
#     "FROM rep_totals r, company_avg c "
#     "ORDER BY r.total DESC"
# ).fetchall()
# for r in rows:
#     print(f"  {r[0]:8s}  total=${r[1]:,}  performance={r[2]}")

conn.close()"""
},
"rw": {
"title": "Product Category Breadcrumb Builder",
"scenario": "An e-commerce search indexer uses a recursive CTE to build full breadcrumb paths for every product category.",
"code":
"""import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE categories (id INT PRIMARY KEY, name TEXT, parent_id INT)")
conn.executemany("INSERT INTO categories VALUES (?,?,?)", [
    (1,"All",None),(2,"Electronics",1),(3,"Computers",2),
    (4,"Laptops",3),(5,"Gaming Laptops",4),(6,"Ultrabooks",4),
    (7,"Phones",2),(8,"Android",7),(9,"Clothing",1),(10,"Mens",9),
])

rows = conn.execute(
    "WITH RECURSIVE tree AS ("
    "  SELECT id, name, parent_id, CAST(name AS TEXT) as path, 0 as depth "
    "  FROM categories WHERE parent_id IS NULL "
    "  UNION ALL "
    "  SELECT c.id, c.name, c.parent_id, t.path||' > '||c.name, t.depth+1 "
    "  FROM categories c JOIN tree t ON c.parent_id=t.id"
    ") "
    "SELECT id, depth, path FROM tree ORDER BY path"
).fetchall()
for r in rows:
    print(f"  {'  '*r[1]}[{r[0]}] {r[2]}")
conn.close()"""}
}

,
{
    "title": "11. Common Table Expressions (CTEs)",
    "desc": "Write readable, modular SQL with WITH clauses. Break complex queries into named steps and use recursive CTEs for hierarchical data.",
    "examples": [
        {
            "label": "Basic CTE to simplify a complex query",
            "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE orders (order_id INT, customer_id INT, amount REAL, order_date TEXT);\nINSERT INTO orders VALUES\n  (1,101,250,'2024-01-05'),(2,102,80,'2024-01-10'),(3,101,120,'2024-01-15'),\n  (4,103,400,'2024-02-01'),(5,102,60,'2024-02-10'),(6,101,90,'2024-02-20'),\n  (7,104,300,'2024-03-01'),(8,103,150,'2024-03-05'),(9,102,200,'2024-03-15');\n\"\"\")\nquery = \"\"\"\nWITH customer_totals AS (\n    SELECT customer_id,\n           SUM(amount) AS total_spend,\n           COUNT(*) AS order_count,\n           AVG(amount) AS avg_order\n    FROM orders\n    GROUP BY customer_id\n),\nhigh_value AS (\n    SELECT * FROM customer_totals WHERE total_spend > 300\n)\nSELECT customer_id,\n       ROUND(total_spend, 2) AS total_spend,\n       order_count,\n       ROUND(avg_order, 2) AS avg_order\nFROM high_value\nORDER BY total_spend DESC;\n\"\"\"\nprint(pd.read_sql(query, conn).to_string(index=False))\nconn.close()"
        },
        {
            "label": "Multiple chained CTEs",
            "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE sales (sale_id INT, product TEXT, region TEXT, amount REAL, sale_date TEXT);\nINSERT INTO sales VALUES\n  (1,'Laptop','East',1200,'2024-01-10'),(2,'Mouse','West',30,'2024-01-15'),\n  (3,'Laptop','West',1100,'2024-01-20'),(4,'Monitor','East',400,'2024-02-05'),\n  (5,'Mouse','East',25,'2024-02-10'),(6,'Monitor','West',380,'2024-02-20'),\n  (7,'Laptop','East',1300,'2024-03-01'),(8,'Keyboard','East',80,'2024-03-10');\n\"\"\")\n\nquery = \"\"\"\nWITH regional_totals AS (\n    SELECT region, SUM(amount) AS regional_total FROM sales GROUP BY region\n),\nproduct_totals AS (\n    SELECT product, SUM(amount) AS product_total FROM sales GROUP BY product\n),\ncombined AS (\n    SELECT s.product, s.region, s.amount,\n           r.regional_total, p.product_total,\n           ROUND(s.amount * 100.0 / r.regional_total, 1) AS pct_of_region\n    FROM sales s\n    JOIN regional_totals r ON s.region = r.region\n    JOIN product_totals p ON s.product = p.product\n)\nSELECT product, region, amount, pct_of_region\nFROM combined\nORDER BY region, pct_of_region DESC;\n\"\"\"\nprint(pd.read_sql(query, conn).to_string(index=False))\nconn.close()"
        },
        {
            "label": "Recursive CTE for hierarchical org chart",
            "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE employees (id INT, name TEXT, manager_id INT);\nINSERT INTO employees VALUES\n  (1,'Alice',NULL),(2,'Bob',1),(3,'Carol',1),\n  (4,'Dave',2),(5,'Eve',2),(6,'Frank',3),(7,'Grace',3),(8,'Hank',4);\n\"\"\")\n\nquery = \"\"\"\nWITH RECURSIVE org_chart AS (\n    -- Base case: root (CEO)\n    SELECT id, name, manager_id, 0 AS depth, name AS path\n    FROM employees WHERE manager_id IS NULL\n    UNION ALL\n    -- Recursive step: employees who report to current level\n    SELECT e.id, e.name, e.manager_id, oc.depth + 1,\n           oc.path || ' -> ' || e.name\n    FROM employees e\n    JOIN org_chart oc ON e.manager_id = oc.id\n)\nSELECT id, depth, name, path FROM org_chart ORDER BY path;\n\"\"\"\ndf = pd.read_sql(query, conn)\nfor _, row in df.iterrows():\n    print('  ' * row['depth'] + f\"[{row['id']}] {row['name']}\")\nconn.close()"
        },
        {
            "label": "CTE vs subquery — readability comparison",
            "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE sales (product TEXT, amount REAL);\nINSERT INTO sales VALUES\n  ('A',100),('A',200),('B',50),('B',300),('C',150),('C',250),('C',100);\n\"\"\")\n\n# Subquery version (harder to read)\nq_sub = \"\"\"\nSELECT product, avg_amount\nFROM (\n    SELECT product, AVG(amount) AS avg_amount\n    FROM sales GROUP BY product\n) WHERE avg_amount > 100;\n\"\"\"\n\n# CTE version (same result, easier to read)\nq_cte = \"\"\"\nWITH product_avgs AS (\n    SELECT product, AVG(amount) AS avg_amount\n    FROM sales GROUP BY product\n)\nSELECT product, ROUND(avg_amount,2) AS avg_amount\nFROM product_avgs\nWHERE avg_amount > 100;\n\"\"\"\n\nprint('Subquery result:'); print(pd.read_sql(q_sub, conn).to_string(index=False))\nprint('CTE result:');      print(pd.read_sql(q_cte, conn).to_string(index=False))\nconn.close()"
        }
    ],
    "rw_scenario": "An HR system uses a recursive CTE to find all employees reporting up through an org tree to a given VP — unlimited hierarchy depth in one query.",
    "rw_code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE employees (id INT, name TEXT, dept TEXT, salary REAL, manager_id INT);\nINSERT INTO employees VALUES\n  (1,'CEO Alice','Exec',250000,NULL),(2,'VP Bob','Eng',180000,1),\n  (3,'VP Carol','Sales',160000,1),(4,'Mgr Dave','Eng',130000,2),\n  (5,'Mgr Eve','Eng',120000,2),(6,'Mgr Frank','Sales',110000,3),\n  (7,'Eng Grace','Eng',95000,4),(8,'Eng Hank','Eng',90000,4),\n  (9,'Eng Ivy','Eng',92000,5),(10,'Sales Jan','Sales',75000,6);\n\"\"\")\n\n# Find all reports under Bob (id=2)\nquery = \"\"\"\nWITH RECURSIVE reports AS (\n    SELECT id, name, dept, salary, manager_id, 0 AS depth\n    FROM employees WHERE id = 2\n    UNION ALL\n    SELECT e.id, e.name, e.dept, e.salary, e.manager_id, r.depth + 1\n    FROM employees e JOIN reports r ON e.manager_id = r.id\n)\nSELECT depth, name, dept, salary FROM reports ORDER BY depth, name;\n\"\"\"\ndf = pd.read_sql(query, conn)\nprint(df.to_string(index=False))\nprint(f\"Team size: {len(df)}, Total payroll: ${df['salary'].sum():,.0f}\")\nconn.close()",
    "practice": {
        "title": "Sales Pipeline CTE",
        "desc": "Using CTEs, write a query that: (1) computes monthly revenue, (2) adds a 3-month rolling average using LAG, (3) flags months where revenue fell below the rolling average.",
        "starter": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE orders (order_date TEXT, amount REAL)')\nimport random; random.seed(42)\nrows = [(f'2023-{m:02d}-15', random.uniform(10000, 50000)) for m in range(1,13)]\nconn.executemany('INSERT INTO orders VALUES (?,?)', rows)\nconn.commit()\n\nquery = \"\"\"\n-- TODO: CTE 1: monthly_revenue - SUM(amount) GROUP BY month\n-- TODO: CTE 2: with_prev - add prev1, prev2 using LAG()\n-- TODO: Final: add rolling_avg = (revenue+prev1+prev2)/3\n--              add below_avg = CASE WHEN revenue < rolling_avg THEN 1 ELSE 0 END\n\"\"\"\n# df = pd.read_sql(query, conn)\n# print(df.to_string(index=False))\nconn.close()"
    }
},
{
    "title": "12. Window Functions",
    "desc": "Perform calculations across related rows without collapsing them — rankings, running totals, lag/lead comparisons, and moving averages.",
    "examples": [
        {
            "label": "ROW_NUMBER, RANK, and DENSE_RANK",
            "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE scores (player TEXT, region TEXT, score INT);\nINSERT INTO scores VALUES\n  ('Alice','East',95),('Bob','East',88),('Carol','East',95),\n  ('Dave','West',78),('Eve','West',91),('Frank','West',85),\n  ('Grace','North',74),('Hank','North',80),('Ivy','North',80);\n\"\"\")\n\nquery = \"\"\"\nSELECT player, region, score,\n       ROW_NUMBER() OVER (PARTITION BY region ORDER BY score DESC) AS row_num,\n       RANK()       OVER (PARTITION BY region ORDER BY score DESC) AS rank,\n       DENSE_RANK() OVER (PARTITION BY region ORDER BY score DESC) AS dense_rank\nFROM scores\nORDER BY region, score DESC;\n\"\"\"\nprint(pd.read_sql(query, conn).to_string(index=False))\nconn.close()"
        },
        {
            "label": "Running totals and cumulative sums",
            "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE daily_sales (sale_date TEXT, revenue REAL);\nINSERT INTO daily_sales VALUES\n  ('2024-01-01',1200),('2024-01-02',800),('2024-01-03',1500),\n  ('2024-01-04',600),('2024-01-05',2000),('2024-01-06',900),\n  ('2024-01-07',1100);\n\"\"\")\n\nquery = \"\"\"\nSELECT sale_date, revenue,\n       SUM(revenue) OVER (ORDER BY sale_date\n                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,\n       AVG(revenue) OVER (ORDER BY sale_date\n                          ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3d,\n       SUM(revenue) OVER () AS grand_total,\n       ROUND(revenue * 100.0 / SUM(revenue) OVER (), 1) AS pct_of_total\nFROM daily_sales ORDER BY sale_date;\n\"\"\"\nprint(pd.read_sql(query, conn).to_string(index=False))\nconn.close()"
        },
        {
            "label": "LAG and LEAD for period-over-period comparison",
            "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE monthly_revenue (month TEXT, category TEXT, revenue REAL);\nINSERT INTO monthly_revenue VALUES\n  ('2024-01','Electronics',50000),('2024-02','Electronics',55000),\n  ('2024-03','Electronics',48000),('2024-04','Electronics',62000),\n  ('2024-01','Clothing',30000),('2024-02','Clothing',28000),\n  ('2024-03','Clothing',35000),('2024-04','Clothing',32000);\n\"\"\")\n\nquery = \"\"\"\nSELECT month, category, revenue,\n       LAG(revenue)  OVER (PARTITION BY category ORDER BY month) AS prev_month,\n       LEAD(revenue) OVER (PARTITION BY category ORDER BY month) AS next_month,\n       ROUND((revenue - LAG(revenue) OVER (PARTITION BY category ORDER BY month))\n             * 100.0 / LAG(revenue) OVER (PARTITION BY category ORDER BY month), 1) AS mom_pct\nFROM monthly_revenue\nORDER BY category, month;\n\"\"\"\nprint(pd.read_sql(query, conn).to_string(index=False))\nconn.close()"
        },
        {
            "label": "NTILE and percentile buckets",
            "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE customers (name TEXT, lifetime_value REAL);\nINSERT INTO customers VALUES\n  ('Alice',1200),('Bob',450),('Carol',3400),('Dave',890),('Eve',2100),\n  ('Frank',200),('Grace',4500),('Hank',700),('Ivy',1800),('Jake',350),\n  ('Kim',2800),('Leo',600),('Mia',950),('Ned',1100),('Ora',3100);\n\"\"\")\n\nquery = \"\"\"\nSELECT name, lifetime_value,\n       NTILE(4)  OVER (ORDER BY lifetime_value)       AS quartile,\n       NTILE(10) OVER (ORDER BY lifetime_value)       AS decile,\n       RANK()    OVER (ORDER BY lifetime_value DESC)  AS rank\nFROM customers\nORDER BY lifetime_value DESC;\n\"\"\"\ndf = pd.read_sql(query, conn)\nprint(df.to_string(index=False))\nprint('\\nQuartile summary:')\nprint(df.groupby('quartile')['lifetime_value'].agg(['min','max','mean']).round(0))\nconn.close()"
        }
    ],
    "rw_scenario": "An e-commerce team computes month-over-month revenue change and 3-month rolling average for each product category without any Python post-processing.",
    "rw_code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE orders (order_id INT, product_cat TEXT, amount REAL, order_date TEXT);\nINSERT INTO orders VALUES\n  (1,'Electronics',1200,'2024-01-05'),(2,'Clothing',80,'2024-01-12'),\n  (3,'Electronics',950,'2024-01-20'),(4,'Food',45,'2024-01-25'),\n  (5,'Clothing',120,'2024-02-03'),(6,'Electronics',1400,'2024-02-10'),\n  (7,'Food',60,'2024-02-15'),(8,'Clothing',95,'2024-02-22'),\n  (9,'Electronics',1100,'2024-03-01'),(10,'Food',55,'2024-03-08'),\n  (11,'Clothing',140,'2024-03-15'),(12,'Electronics',1350,'2024-03-22');\n\"\"\")\n\nquery = \"\"\"\nWITH monthly AS (\n    SELECT strftime('%Y-%m', order_date) AS month,\n           product_cat, SUM(amount) AS revenue\n    FROM orders GROUP BY 1, 2\n)\nSELECT month, product_cat,\n       ROUND(revenue,0) AS revenue,\n       ROUND(LAG(revenue) OVER w, 0) AS prev_revenue,\n       ROUND((revenue - LAG(revenue) OVER w) * 100.0 / LAG(revenue) OVER w, 1) AS mom_pct,\n       ROUND(AVG(revenue) OVER (PARTITION BY product_cat ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS roll3_avg,\n       DENSE_RANK() OVER (PARTITION BY month ORDER BY revenue DESC) AS rank_in_month\nFROM monthly\nWINDOW w AS (PARTITION BY product_cat ORDER BY month)\nORDER BY month, rank_in_month;\n\"\"\"\nprint(pd.read_sql(query, conn).to_string(index=False))\nconn.close()",
    "practice": {
        "title": "Sales Leaderboard",
        "desc": "Rank salespeople by total revenue within each region using DENSE_RANK. Show their revenue vs the region average and flag the top performer per region with 'CHAMPION'.",
        "starter": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE sales (salesperson TEXT, region TEXT, revenue REAL);\nINSERT INTO sales VALUES\n  ('Alice','East',95000),('Bob','East',88000),('Carol','East',102000),\n  ('Dave','West',78000),('Eve','West',91000),('Frank','West',85000),\n  ('Grace','North',67000),('Hank','North',74000);\n\"\"\")\nquery = \"\"\"\n-- TODO: DENSE_RANK within region by revenue desc\n-- TODO: AVG(revenue) OVER region\n-- TODO: revenue - avg as diff_from_avg\n-- TODO: CASE WHEN rank=1 THEN 'CHAMPION' ELSE '' END\n\"\"\"\n# df = pd.read_sql(query, conn)\n# print(df.to_string(index=False))\nconn.close()"
    }
},
{
    "title": "13. Query Optimization",
    "desc": "Write faster SQL — understand EXPLAIN QUERY PLAN, use indexes effectively, and rewrite slow patterns as efficient alternatives.",
    "examples": [
        {
            "label": "Creating and using indexes",
            "code": "import sqlite3, time\n\nconn = sqlite3.connect(':memory:')\nimport random; random.seed(42)\nn = 100000\nconn.execute('CREATE TABLE orders (order_id INT, customer_id INT, amount REAL, status TEXT)')\nconn.executemany('INSERT INTO orders VALUES (?,?,?,?)',\n    [(i, random.randint(1,1000), random.uniform(10,500), random.choice(['pending','shipped','done']))\n     for i in range(n)])\nconn.commit()\n\n# Query WITHOUT index\nt0 = time.perf_counter()\nconn.execute('SELECT * FROM orders WHERE customer_id = 42').fetchall()\nt1 = time.perf_counter()\nprint(f'Without index: {(t1-t0)*1000:.2f} ms')\n\n# Create index\nconn.execute('CREATE INDEX idx_customer ON orders(customer_id)')\n\nt0 = time.perf_counter()\nconn.execute('SELECT * FROM orders WHERE customer_id = 42').fetchall()\nt1 = time.perf_counter()\nprint(f'With index:    {(t1-t0)*1000:.2f} ms')\n\n# Composite index for common filter+sort\nconn.execute('CREATE INDEX idx_status_amount ON orders(status, amount DESC)')\nconn.close()"
        },
        {
            "label": "EXPLAIN QUERY PLAN to inspect execution",
            "code": "import sqlite3\n\nconn = sqlite3.connect(':memory:')\nimport random; random.seed(0)\nconn.execute('CREATE TABLE sales (id INT, region TEXT, amount REAL)')\nconn.executemany('INSERT INTO sales VALUES (?,?,?)',\n    [(i, random.choice(['East','West','North']), random.uniform(10,1000)) for i in range(10000)])\nconn.commit()\n\ndef explain(conn, query, label):\n    plan = conn.execute(f'EXPLAIN QUERY PLAN {query}').fetchall()\n    print(f'\\n--- {label} ---')\n    for row in plan:\n        print(' ', row)\n\nexplain(conn, 'SELECT * FROM sales WHERE region = \"East\"', 'No index')\nconn.execute('CREATE INDEX idx_region ON sales(region)')\nexplain(conn, 'SELECT * FROM sales WHERE region = \"East\"', 'With index')\nexplain(conn, 'SELECT region, SUM(amount) FROM sales GROUP BY region', 'Aggregation')\nconn.close()"
        },
        {
            "label": "EXISTS vs IN vs JOIN performance",
            "code": "import sqlite3, time\n\nconn = sqlite3.connect(':memory:')\nimport random; random.seed(42)\nconn.execute('CREATE TABLE customers (id INT PRIMARY KEY, name TEXT)')\nconn.execute('CREATE TABLE orders (id INT, customer_id INT, amount REAL)')\nconn.executemany('INSERT INTO customers VALUES (?,?)', [(i,f'C{i}') for i in range(1000)])\nconn.executemany('INSERT INTO orders VALUES (?,?,?)',\n    [(i, random.randint(1,1000), random.uniform(10,500)) for i in range(50000)])\nconn.commit()\nconn.execute('CREATE INDEX idx_oid ON orders(customer_id)')\n\nqueries = {\n    'IN subquery': 'SELECT * FROM customers WHERE id IN (SELECT DISTINCT customer_id FROM orders WHERE amount > 400)',\n    'EXISTS':      'SELECT * FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id=c.id AND o.amount>400)',\n    'JOIN':        'SELECT DISTINCT c.* FROM customers c JOIN orders o ON c.id=o.customer_id WHERE o.amount>400',\n}\nfor label, q in queries.items():\n    t0 = time.perf_counter()\n    rows = conn.execute(q).fetchall()\n    print(f'{label:15s}: {(time.perf_counter()-t0)*1000:.2f} ms, {len(rows)} rows')\nconn.close()"
        },
        {
            "label": "Avoiding N+1 queries with JOIN",
            "code": "import sqlite3, time\n\nconn = sqlite3.connect(':memory:')\nconn.executescript(\"\"\"\nCREATE TABLE authors (id INT, name TEXT);\nCREATE TABLE books (id INT, title TEXT, author_id INT, pages INT);\n\"\"\")\nimport random; random.seed(0)\nauthors = [(i, f'Author {i}') for i in range(50)]\nbooks   = [(i, f'Book {i}', random.randint(0,49), random.randint(100,600)) for i in range(500)]\nconn.executemany('INSERT INTO authors VALUES (?,?)', authors)\nconn.executemany('INSERT INTO books VALUES (?,?,?,?)', books)\nconn.commit()\n\n# N+1 pattern (BAD)\nt0 = time.perf_counter()\nall_books = conn.execute('SELECT * FROM books').fetchall()\nresults = []\nfor b in all_books:\n    auth = conn.execute('SELECT name FROM authors WHERE id=?', (b[2],)).fetchone()\n    results.append((b[1], auth[0] if auth else 'Unknown'))\nprint(f'N+1 queries: {(time.perf_counter()-t0)*1000:.2f} ms ({len(results)} results)')\n\n# Single JOIN (GOOD)\nt0 = time.perf_counter()\nresults2 = conn.execute('SELECT b.title, a.name FROM books b LEFT JOIN authors a ON b.author_id=a.id').fetchall()\nprint(f'Single JOIN: {(time.perf_counter()-t0)*1000:.2f} ms ({len(results2)} results)')\nconn.close()"
        }
    ],
    "rw_scenario": "A reporting query on 10M rows took 45 seconds. Adding the right composite index and rewriting a correlated subquery as a JOIN dropped it to 0.3 seconds.",
    "rw_code": "import sqlite3, time\n\nconn = sqlite3.connect(':memory:')\nimport random; random.seed(42)\nn = 200000\nconn.execute('CREATE TABLE transactions (id INT, account_id INT, tx_date TEXT, amount REAL, category TEXT)')\nconn.executemany('INSERT INTO transactions VALUES (?,?,?,?,?)',\n    [(i, random.randint(1,500),\n      f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}',\n      random.uniform(1, 5000),\n      random.choice(['Food','Travel','Tech','Retail']))\n     for i in range(n)])\nconn.commit()\n\nq = 'SELECT account_id, SUM(amount) FROM transactions WHERE category=\"Tech\" AND amount>100 GROUP BY account_id'\n\n# Slow (no index)\nt0 = time.perf_counter()\nconn.execute(q).fetchall()\nt_slow = time.perf_counter() - t0\n\n# Add composite index\nconn.execute('CREATE INDEX idx_cat_amt ON transactions(category, amount)')\n\nt0 = time.perf_counter()\nconn.execute(q).fetchall()\nt_fast = time.perf_counter() - t0\n\nprint(f'No index: {t_slow*1000:.1f} ms')\nprint(f'Indexed:  {t_fast*1000:.1f} ms')\nprint(f'Speedup:  {t_slow/t_fast:.1f}x')\nconn.close()",
    "practice": {
        "title": "Index Advisor",
        "desc": "Create a 100K-row orders table. Time a filter query on customer_id WITHOUT an index, add the index, re-run, and print the speedup factor. Also run EXPLAIN QUERY PLAN on both.",
        "starter": "import sqlite3, time\n\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE orders (id INT, customer_id INT, amount REAL, status TEXT)')\nimport random; random.seed(42)\nrows = [(i, random.randint(1,1000), random.uniform(10,500), random.choice(['pending','done'])) for i in range(100000)]\nconn.executemany('INSERT INTO orders VALUES (?,?,?,?)', rows)\nconn.commit()\n\nq = 'SELECT * FROM orders WHERE customer_id = 42'\n# TODO: time query without index\n# TODO: EXPLAIN QUERY PLAN before index\n# TODO: CREATE INDEX idx_cust ON orders(customer_id)\n# TODO: time query with index\n# TODO: EXPLAIN QUERY PLAN after index\n# TODO: print speedup factor\nconn.close()"
    }
},

    {
        "title": "14. Query Optimization & Indexing",
        "examples": [
            {
                "label": "EXPLAIN QUERY PLAN",
                "code": "import sqlite3\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER,\n                         amount REAL, status TEXT, order_date TEXT);\n    INSERT INTO orders SELECT value, (value%100)+1, RANDOM()*1000,\n        CASE value%3 WHEN 0 THEN \'pending\' WHEN 1 THEN \'completed\' ELSE \'cancelled\' END,\n        date(\'2024-01-01\', \'+\'||(value%365)||\' days\')\n    FROM generate_series(1, 10000);\n\'\'\')\nplan = conn.execute(\'\'\'\n    EXPLAIN QUERY PLAN\n    SELECT customer_id, COUNT(*), AVG(amount)\n    FROM orders WHERE status=\'completed\'\n    GROUP BY customer_id ORDER BY AVG(amount) DESC\n\'\'\').fetchall()\nprint(\'Query plan (no index):\')\nfor row in plan: print(\' \', row)\nconn.close()"
            },
            {
                "label": "Index speedup measurement",
                "code": "import sqlite3, time\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE sales (id INTEGER PRIMARY KEY, region TEXT, amount REAL, sale_date TEXT);\n    INSERT INTO sales SELECT value, CASE value%4 WHEN 0 THEN \'North\' WHEN 1 THEN \'South\'\n        WHEN 2 THEN \'East\' ELSE \'West\' END, RANDOM()*1000,\n        date(\'2024-01-01\', \'+\'||(value%365)||\' days\')\n    FROM generate_series(1, 100000);\n\'\'\')\nquery = \"SELECT region, AVG(amount) FROM sales WHERE sale_date > \'2024-06-01\' GROUP BY region\"\nt0 = time.time(); conn.execute(query).fetchall(); t_slow = time.time()-t0\nconn.execute(\'CREATE INDEX idx_date ON sales(sale_date)\')\nt0 = time.time(); conn.execute(query).fetchall(); t_fast = time.time()-t0\nprint(f\'Without index: {t_slow*1000:.1f}ms\')\nprint(f\'With index:    {t_fast*1000:.1f}ms\')\nprint(f\'Speedup: {t_slow/max(t_fast,0.001):.1f}x\')\nconn.close()"
            },
            {
                "label": "Avoiding N+1 with JOINs",
                "code": "import sqlite3\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary REAL);\n    CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT);\n    INSERT INTO departments VALUES (1,\'Engineering\'),(2,\'Sales\'),(3,\'HR\');\n    INSERT INTO employees SELECT v, \'Emp \'||v, (v%3)+1, 50000+RANDOM()*50000\n    FROM generate_series(1,30) v;\n\'\'\')\nprint(\'=== N+1 (avoid) ===\')\nfor eid,name,dept_id in conn.execute(\'SELECT id,name,dept_id FROM employees LIMIT 3\').fetchall():\n    dept = conn.execute(\'SELECT name FROM departments WHERE id=?\',(dept_id,)).fetchone()\n    print(f\'  {name} -> {dept[0]}\')\nprint(\'=== Single JOIN (preferred) ===\')\nfor row in conn.execute(\'SELECT e.name, d.name, e.salary FROM employees e JOIN departments d ON e.dept_id=d.id LIMIT 3\').fetchall():\n    print(f\'  {row[0]} | {row[1]} | ${row[2]:,.0f}\')\nconn.close()"
            },
            {
                "label": "CTE vs subquery readability",
                "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE transactions (id INTEGER PRIMARY KEY, user_id INTEGER,\n                               amount REAL, type TEXT, ts TEXT);\n    INSERT INTO transactions SELECT v, (v%50)+1, RANDOM()*500,\n        CASE v%3 WHEN 0 THEN \'purchase\' WHEN 1 THEN \'refund\' ELSE \'fee\' END,\n        date(\'2024-01-01\',\'+\'||(v%300)||\' days\') FROM generate_series(1,1000) v;\n\'\'\')\ncte_query = \'\'\'\n    WITH purchase_summary AS (\n        SELECT user_id, SUM(amount) total, COUNT(*) cnt\n        FROM transactions WHERE type=\'purchase\' GROUP BY user_id\n    ), avg_thresh AS (\n        SELECT AVG(amount)*5 threshold FROM transactions WHERE type=\'purchase\'\n    )\n    SELECT ps.user_id, ROUND(ps.total,2) total, ps.cnt\n    FROM purchase_summary ps, avg_thresh at WHERE ps.total > at.threshold\n    ORDER BY ps.total DESC LIMIT 5\n\'\'\'\ndf = pd.read_sql(cte_query, conn)\nprint(\'Top buyers via CTE:\')\nprint(df.to_string(index=False))\nconn.close()"
            }
        ],
        "rw_scenario": "Your analytics query on 500K rows takes 45 seconds. Use EXPLAIN QUERY PLAN to find bottlenecks and add composite indexes to get it under 1 second.",
        "rw_code": "import sqlite3, time\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE events (id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT,\n                         product_id INTEGER, revenue REAL, ts TEXT);\n    INSERT INTO events SELECT v, (v%10000)+1,\n        CASE v%5 WHEN 0 THEN \'view\' WHEN 1 THEN \'click\' WHEN 2 THEN \'add_cart\'\n                 WHEN 3 THEN \'purchase\' ELSE \'abandon\' END,\n        (v%1000)+1, CASE v%5 WHEN 3 THEN RANDOM()*200 ELSE 0 END,\n        datetime(\'2024-01-01\',\'+\'||(v%365)||\' days\',\'+\'||(v%86400)||\' seconds\')\n    FROM generate_series(1,200000) v;\n\'\'\')\nq = \"SELECT user_id, COUNT(DISTINCT product_id) prods, SUM(revenue) rev FROM events WHERE ts >= \'2024-06-01\' AND product_id BETWEEN 100 AND 200 GROUP BY user_id HAVING rev > 0 ORDER BY rev DESC LIMIT 20\"\nt0 = time.time(); conn.execute(q).fetchall(); t1 = time.time()-t0\nconn.execute(\'CREATE INDEX idx_ts ON events(ts)\')\nconn.execute(\'CREATE INDEX idx_comp ON events(ts, product_id, user_id)\')\nt0 = time.time(); res = conn.execute(q).fetchall(); t2 = time.time()-t0\nprint(f\'Without index: {t1*1000:.0f}ms | With: {t2*1000:.0f}ms | Speedup: {t1/max(t2,0.0001):.1f}x\')\nif res: print(f\'Top user: {res[0][0]} - Revenue: ${res[0][2]:.2f}\')\nconn.close()",
        "practice": {
            "title": "Index Advisor",
            "desc": "Create a 100K-row orders table. Time a customer_id filter query WITHOUT index, add the index, re-run, print speedup, and show EXPLAIN QUERY PLAN before vs after.",
            "starter": "import sqlite3, time\n\nconn = sqlite3.connect(\':memory:\')\n# TODO: create orders table with 100K rows (id, customer_id, amount, status)\n# TODO: time filter query on customer_id=42\n# TODO: EXPLAIN QUERY PLAN before index\n# TODO: CREATE INDEX idx_cust ON orders(customer_id)\n# TODO: time query with index, print speedup\nconn.close()"
        }
    },
    {
        "title": "15. Pivoting & Unpivoting",
        "examples": [
            {
                "label": "Pivot with CASE WHEN",
                "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE sales (year INTEGER, quarter TEXT, region TEXT, revenue REAL);\n    INSERT INTO sales VALUES\n        (2024,\'Q1\',\'North\',120000),(2024,\'Q2\',\'North\',135000),(2024,\'Q3\',\'North\',118000),(2024,\'Q4\',\'North\',145000),\n        (2024,\'Q1\',\'South\',98000),(2024,\'Q2\',\'South\',105000),(2024,\'Q3\',\'South\',112000),(2024,\'Q4\',\'South\',125000);\n\'\'\')\ndf = pd.read_sql(\'\'\'\n    SELECT region,\n        SUM(CASE WHEN quarter=\'Q1\' THEN revenue ELSE 0 END) Q1,\n        SUM(CASE WHEN quarter=\'Q2\' THEN revenue ELSE 0 END) Q2,\n        SUM(CASE WHEN quarter=\'Q3\' THEN revenue ELSE 0 END) Q3,\n        SUM(CASE WHEN quarter=\'Q4\' THEN revenue ELSE 0 END) Q4,\n        SUM(revenue) Total\n    FROM sales GROUP BY region ORDER BY Total DESC\n\'\'\', conn)\nprint(df.to_string(index=False))\nconn.close()"
            },
            {
                "label": "Unpivot (wide to long) with UNION ALL",
                "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE server_metrics (server TEXT, cpu_pct REAL, mem_pct REAL, disk_pct REAL, net_pct REAL);\n    INSERT INTO server_metrics VALUES (\'web-01\',72.5,65.2,45.0,30.1),\n        (\'web-02\',55.0,70.8,52.3,28.7),(\'db-01\',88.2,91.5,78.4,15.2);\n\'\'\')\ndf = pd.read_sql(\'\'\'\n    SELECT server,\'CPU\' metric, cpu_pct value FROM server_metrics\n    UNION ALL SELECT server,\'Memory\',mem_pct FROM server_metrics\n    UNION ALL SELECT server,\'Disk\',disk_pct FROM server_metrics\n    UNION ALL SELECT server,\'Network\',net_pct FROM server_metrics\n    ORDER BY server, metric\n\'\'\', conn)\nprint(df.to_string(index=False))\nconn.close()"
            },
            {
                "label": "Dynamic pivot with Python",
                "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE survey (respondent INTEGER, question TEXT, score INTEGER);\n    INSERT INTO survey VALUES (1,\'Q1\',4),(1,\'Q2\',5),(1,\'Q3\',3),(1,\'Q4\',4),\n        (2,\'Q1\',3),(2,\'Q2\',4),(2,\'Q3\',5),(2,\'Q4\',2),(3,\'Q1\',5),(3,\'Q2\',5),(3,\'Q3\',4),(3,\'Q4\',5);\n\'\'\')\nquestions = [r[0] for r in conn.execute(\'SELECT DISTINCT question FROM survey ORDER BY question\')]\ncases = \',\'.join(f\"MAX(CASE WHEN question=\'{q}\' THEN score END) AS {q}\" for q in questions)\ndf = pd.read_sql(f\'SELECT respondent, {cases}, ROUND(AVG(score),2) avg_score FROM survey GROUP BY respondent ORDER BY avg_score DESC\', conn)\nprint(df.to_string(index=False))\nconn.close()"
            },
            {
                "label": "Cross-tabulation with percentages",
                "code": "import sqlite3, pandas as pd\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE feedback (category TEXT, sentiment TEXT, count INTEGER);\n    INSERT INTO feedback VALUES\n        (\'Product\',\'Positive\',450),(\'Product\',\'Neutral\',120),(\'Product\',\'Negative\',80),\n        (\'Service\',\'Positive\',380),(\'Service\',\'Neutral\',95),(\'Service\',\'Negative\',125),\n        (\'Price\',\'Positive\',200),(\'Price\',\'Neutral\',180),(\'Price\',\'Negative\',220);\n\'\'\')\ndf = pd.read_sql(\'\'\'\n    SELECT category,\n        SUM(CASE WHEN sentiment=\'Positive\' THEN count ELSE 0 END) positive,\n        SUM(CASE WHEN sentiment=\'Neutral\' THEN count ELSE 0 END) neutral,\n        SUM(CASE WHEN sentiment=\'Negative\' THEN count ELSE 0 END) negative,\n        SUM(count) total,\n        ROUND(100.0*SUM(CASE WHEN sentiment=\'Positive\' THEN count ELSE 0 END)/SUM(count),1) pct_pos\n    FROM feedback GROUP BY category ORDER BY pct_pos DESC\n\'\'\', conn)\nprint(df.to_string(index=False))\nconn.close()"
            }
        ],
        "rw_scenario": "Your reporting team needs monthly revenue by 5 product categories as a pivot table. Categories come from data dynamically, so you build the query programmatically.",
        "rw_code": "import sqlite3, pandas as pd, numpy as np\n\nconn = sqlite3.connect(\':memory:\')\nnp.random.seed(42)\ncats = [\'Electronics\',\'Apparel\',\'Food\',\'Sports\',\'Books\']\nmonths = [\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\',\'Jul\',\'Aug\',\'Sep\',\'Oct\',\'Nov\',\'Dec\']\nrows = [(c,m,int(np.random.exponential(50000))) for c in cats for m in months]\nconn.executescript(\'CREATE TABLE monthly_sales (category TEXT, month TEXT, revenue INTEGER);\')\nconn.executemany(\'INSERT INTO monthly_sales VALUES (?,?,?)\', rows)\nmonth_order = {m:i for i,m in enumerate(months)}\nmonth_list = sorted([r[0] for r in conn.execute(\'SELECT DISTINCT month FROM monthly_sales\')],\n                     key=lambda m: month_order.get(m,99))\ncases = \',\'.join(f\"SUM(CASE WHEN month=\'{m}\' THEN revenue ELSE 0 END) [{m}]\" for m in month_list)\nquery = f\'SELECT category, {cases}, SUM(revenue) [Annual Total] FROM monthly_sales GROUP BY category ORDER BY [Annual Total] DESC\'\ndf = pd.read_sql(query, conn)\nprint(\'Monthly Revenue Pivot Table:\')\nprint(df.to_string(index=False))\nconn.close()",
        "practice": {
            "title": "Dynamic Sales Pivot",
            "desc": "Create a sales table with 5 reps and 4 quarters. Get distinct quarters from DB, build a CASE WHEN pivot query dynamically, and display as a DataFrame.",
            "starter": "import sqlite3, pandas as pd, numpy as np\n\nconn = sqlite3.connect(\':memory:\')\nnp.random.seed(42)\nreps = [\'Alice\',\'Bob\',\'Carol\',\'Dave\',\'Eve\']\nquarters = [\'Q1\',\'Q2\',\'Q3\',\'Q4\']\nrows = [(r,q,int(np.random.exponential(80000))) for r in reps for q in quarters]\nconn.executescript(\'CREATE TABLE rep_sales (rep TEXT, quarter TEXT, revenue INTEGER);\')\nconn.executemany(\'INSERT INTO rep_sales VALUES (?,?,?)\', rows)\n# TODO: get distinct quarters dynamically\n# TODO: build CASE WHEN pivot query\n# TODO: read to DataFrame and print\nconn.close()"
        }
    },
    {
        "title": "16. Triggers & Database Automation",
        "examples": [
            {
                "label": "Audit log trigger on price UPDATE",
                "code": "import sqlite3\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL);\n    CREATE TABLE price_audit (log_id INTEGER PRIMARY KEY AUTOINCREMENT,\n        product_id INTEGER, old_price REAL, new_price REAL,\n        changed_at DATETIME DEFAULT CURRENT_TIMESTAMP);\n    INSERT INTO products VALUES (1,\'Widget\',9.99),(2,\'Gadget\',24.99);\n    CREATE TRIGGER log_price AFTER UPDATE OF price ON products\n    BEGIN INSERT INTO price_audit(product_id,old_price,new_price)\n          VALUES(NEW.id,OLD.price,NEW.price); END;\n\'\'\')\nconn.execute(\'UPDATE products SET price=12.99 WHERE id=1\')\nconn.execute(\'UPDATE products SET price=29.99 WHERE id=2\')\nfor row in conn.execute(\'SELECT * FROM price_audit\').fetchall():\n    print(f\'Product {row[1]}: ${row[2]} -> ${row[3]}\')\nconn.close()"
            },
            {
                "label": "Business rule — prevent negative stock",
                "code": "import sqlite3\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE inventory (product_id INTEGER PRIMARY KEY, quantity INTEGER CHECK(quantity >= 0));\n    CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, qty INTEGER);\n    INSERT INTO inventory VALUES (1,100),(2,5);\n    CREATE TRIGGER decrement_stock AFTER INSERT ON orders\n    BEGIN UPDATE inventory SET quantity=quantity-NEW.qty WHERE product_id=NEW.product_id; END;\n\'\'\')\nconn.execute(\'INSERT INTO orders(product_id,qty) VALUES(1,30)\')\nprint(\'After ordering 30 of product 1:\')\nfor row in conn.execute(\'SELECT * FROM inventory\').fetchall():\n    print(f\'  Product {row[0]}: {row[1]} units\')\ntry:\n    conn.execute(\'INSERT INTO orders(product_id,qty) VALUES(2,10)\')\nexcept Exception as e:\n    print(f\'Order failed (CHECK constraint): {type(e).__name__}\')\nconn.close()"
            },
            {
                "label": "Transactional fund transfer (stored proc pattern)",
                "code": "import sqlite3\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance REAL);\n    CREATE TABLE transfers (id INTEGER PRIMARY KEY AUTOINCREMENT,\n        from_id INTEGER, to_id INTEGER, amount REAL, ts DATETIME DEFAULT CURRENT_TIMESTAMP);\n    INSERT INTO accounts VALUES (1,\'Alice\',5000),(2,\'Bob\',1500),(3,\'Carol\',3200);\n\'\'\')\n\ndef transfer(conn, from_id, to_id, amount):\n    bal = conn.execute(\'SELECT balance FROM accounts WHERE id=?\',(from_id,)).fetchone()\n    if not bal or bal[0] < amount:\n        print(f\'  FAILED: ${bal[0] if bal else 0:.2f} < ${amount:.2f}\')\n        return\n    conn.execute(\'BEGIN\')\n    conn.execute(\'UPDATE accounts SET balance=balance-? WHERE id=?\',(amount,from_id))\n    conn.execute(\'UPDATE accounts SET balance=balance+? WHERE id=?\',(amount,to_id))\n    conn.execute(\'INSERT INTO transfers(from_id,to_id,amount) VALUES(?,?,?)\',(from_id,to_id,amount))\n    conn.execute(\'COMMIT\')\n    print(f\'  OK: ${amount:.2f} from acct {from_id} to acct {to_id}\')\n\ntransfer(conn,1,2,500)\ntransfer(conn,2,3,3000)  # fails\nfor row in conn.execute(\'SELECT id,name,balance FROM accounts\').fetchall():\n    print(f\'{row[1]}: ${row[2]:.2f}\')\nconn.close()"
            },
            {
                "label": "INSTEAD OF trigger on a view",
                "code": "import sqlite3\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, salary REAL, dept TEXT);\n    INSERT INTO employees VALUES (1,\'Alice\',75000,\'Eng\'),(2,\'Bob\',68000,\'Sales\');\n    CREATE VIEW emp_view AS SELECT id, name, salary, dept FROM employees;\n    CREATE TRIGGER update_via_view INSTEAD OF UPDATE OF salary ON emp_view\n    BEGIN UPDATE employees SET salary=NEW.salary WHERE id=OLD.id; END;\n\'\'\')\nconn.execute(\"UPDATE emp_view SET salary=90000 WHERE name=\'Alice\'\")\nfor row in conn.execute(\'SELECT name, salary FROM employees\').fetchall():\n    print(f\'{row[0]}: ${row[1]:,.0f}\')\nconn.close()"
            }
        ],
        "rw_scenario": "Your e-commerce DB needs: (1) price change audit logs, (2) auto inventory deduction on orders, (3) transactional payment safety with rollback on failure.",
        "rw_code": "import sqlite3\n\nconn = sqlite3.connect(\':memory:\')\nconn.executescript(\'\'\'\n    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);\n    CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER,\n                         qty INTEGER, total REAL, status TEXT DEFAULT \'pending\');\n    CREATE TABLE price_audit (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER,\n                              old_price REAL, new_price REAL, pct_change REAL,\n                              ts DATETIME DEFAULT CURRENT_TIMESTAMP);\n    CREATE TABLE stock_alerts (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER,\n                               stock INTEGER, alert TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP);\n    INSERT INTO products VALUES (1,\'Laptop\',999.99,50),(2,\'Mouse\',29.99,200),(3,\'Keyboard\',79.99,8);\n    CREATE TRIGGER audit_price AFTER UPDATE OF price ON products\n    BEGIN INSERT INTO price_audit(product_id,old_price,new_price,pct_change)\n        VALUES(NEW.id,OLD.price,NEW.price,ROUND(100.0*(NEW.price-OLD.price)/OLD.price,2)); END;\n    CREATE TRIGGER low_stock AFTER UPDATE OF stock ON products WHEN NEW.stock < 10\n    BEGIN INSERT INTO stock_alerts(product_id,stock,alert)\n        VALUES(NEW.id,NEW.stock,CASE WHEN NEW.stock=0 THEN \'OUT_OF_STOCK\' ELSE \'LOW_STOCK\' END); END;\n\'\'\')\n\ndef place_order(conn, pid, qty):\n    row = conn.execute(\'SELECT stock,price,name FROM products WHERE id=?\',(pid,)).fetchone()\n    if not row or row[0] < qty:\n        print(f\'  FAILED: {row[0] if row else 0} in stock\'); return\n    conn.execute(\'INSERT INTO orders(product_id,qty,total,status) VALUES(?,?,?,\"completed\")\',(pid,qty,row[1]*qty))\n    conn.execute(\'UPDATE products SET stock=stock-? WHERE id=?\',(qty,pid))\n    print(f\'  Ordered {qty}x {row[2]} = ${row[1]*qty:.2f}\')\n\nconn.execute(\'UPDATE products SET price=899.99 WHERE id=1\')\nconn.execute(\'UPDATE products SET price=34.99 WHERE id=2\')\nplace_order(conn,1,5); place_order(conn,3,5); place_order(conn,2,250)\nprint(\'Price Audit:\')\nfor r in conn.execute(\'SELECT product_id,old_price,new_price,pct_change FROM price_audit\').fetchall():\n    print(f\'  Product {r[0]}: ${r[1]} -> ${r[2]} ({r[3]:+.1f}%)\')\nprint(\'Stock Alerts:\')\nfor r in conn.execute(\'SELECT product_id,stock,alert FROM stock_alerts\').fetchall():\n    print(f\'  Product {r[0]}: {r[2]} ({r[1]} units)\')\nconn.close()",
        "practice": {
            "title": "Banking Triggers",
            "desc": "Create accounts and transactions tables. Add triggers: (1) log withdrawals >$1000 to large_withdrawals, (2) prevent negative balances. Test with 5 transactions including one that should fail.",
            "starter": "import sqlite3\n\nconn = sqlite3.connect(\':memory:\')\n# TODO: CREATE TABLE accounts (id, name, balance)\n# TODO: CREATE TABLE large_withdrawals (id AUTOINCREMENT, account_id, amount, ts)\n# TODO: CREATE TRIGGER log_large after INSERT on transactions WHEN amount > 1000\n# TODO: enforce non-negative balance via CHECK or trigger\n# TODO: insert test transactions, show results\nconn.close()"
        }
    },
    {
    "title": "17. Subqueries in Depth",
    "desc": "Subqueries (nested SELECT) can appear in WHERE, FROM, SELECT, and HAVING clauses. Master scalar, column, table, and correlated subqueries for complex filtering and derived metrics.",
    "examples": [
        {"label": "Scalar and column subqueries in WHERE", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE sales (id INTEGER, rep TEXT, amount REAL, region TEXT)\'\'\')\nrunmany(\'INSERT INTO sales VALUES (?,?,?,?)\', [\n    (1,\'Alice\',1200,\'North\'),(2,\'Bob\',800,\'South\'),(3,\'Carol\',1500,\'North\'),\n    (4,\'Dave\',600,\'South\'),(5,\'Eve\',2000,\'North\'),(6,\'Frank\',950,\'East\'),\n])\n\n# Scalar subquery: single value in WHERE\nrows = run(\'\'\'\n    SELECT rep, amount FROM sales\n    WHERE amount > (SELECT AVG(amount) FROM sales)\n    ORDER BY amount DESC\n\'\'\')\nprint(\"Above-average reps:\")\nfor r in rows: print(f\"  {r[0]}: ${r[1]:,.0f}\")\n\n# IN with subquery\nrows = run(\'\'\'\n    SELECT rep, amount FROM sales\n    WHERE region IN (SELECT DISTINCT region FROM sales WHERE amount > 1000)\n    AND amount < 1000\n    ORDER BY amount\n\'\'\')\nprint(\"In high-value regions but low individual amount:\")\nfor r in rows: print(f\"  {r[0]}: ${r[1]:,.0f}\")"},
        {"label": "Correlated subqueries", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE employees (id INTEGER, name TEXT, dept TEXT, salary REAL)\'\'\')\nrunmany(\'INSERT INTO employees VALUES (?,?,?,?)\', [\n    (1,\'Alice\',\'Eng\',90000),(2,\'Bob\',\'Eng\',85000),(3,\'Carol\',\'Sales\',70000),\n    (4,\'Dave\',\'Sales\',72000),(5,\'Eve\',\'HR\',65000),(6,\'Frank\',\'Eng\',95000),\n    (7,\'Grace\',\'HR\',68000),(8,\'Henry\',\'Sales\',75000),\n])\n\n# Correlated subquery: runs ONCE PER ROW in outer query\n# Find employees earning above their department average\nrows = run(\'\'\'\n    SELECT e.name, e.dept, e.salary,\n           ROUND((SELECT AVG(salary) FROM employees i WHERE i.dept = e.dept), 0) AS dept_avg\n    FROM employees e\n    WHERE e.salary > (SELECT AVG(salary) FROM employees i WHERE i.dept = e.dept)\n    ORDER BY e.dept, e.salary DESC\n\'\'\')\nprint(\"Above-department-average earners:\")\nfor r in rows:\n    print(f\"  {r[0]} ({r[1]}): ${r[2]:,.0f} (dept avg ${r[3]:,.0f})\")\n\n# EXISTS: check for related rows\nrows = run(\'\'\'\n    SELECT DISTINCT dept FROM employees e\n    WHERE EXISTS (\n        SELECT 1 FROM employees i\n        WHERE i.dept = e.dept AND i.salary > 80000\n    )\n\'\'\')\nprint(\"Departments with at least one high earner:\", [r[0] for r in rows])"},
        {"label": "Derived tables (subquery in FROM)", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE orders (id INTEGER, cust_id INTEGER, total REAL, yr INTEGER)\'\'\')\nrunmany(\'INSERT INTO orders VALUES (?,?,?,?)\', [\n    (1,1,500,2023),(2,1,300,2023),(3,2,1200,2023),(4,2,800,2024),\n    (5,3,200,2024),(6,1,900,2024),(7,3,600,2023),(8,2,400,2024),\n])\n\n# Derived table: aggregate first, then filter/join\nrows = run(\'\'\'\n    SELECT cust_id, total_2023, total_2024,\n           ROUND(total_2024 - total_2023, 0) AS growth\n    FROM (\n        SELECT cust_id,\n               SUM(CASE WHEN yr=2023 THEN total ELSE 0 END) AS total_2023,\n               SUM(CASE WHEN yr=2024 THEN total ELSE 0 END) AS total_2024\n        FROM orders\n        GROUP BY cust_id\n    ) yearly\n    ORDER BY growth DESC\n\'\'\')\nprint(\"Year-over-year growth by customer:\")\nfor r in rows:\n    print(f\"  Cust {r[0]}: 2023=${r[1]:,.0f} -> 2024=${r[2]:,.0f} ({r[3]:+,.0f})\")\n\n# Derived table with LIMIT for top-N analysis\nrows = run(\'\'\'\n    SELECT cust_id, avg_order\n    FROM (SELECT cust_id, AVG(total) AS avg_order FROM orders GROUP BY cust_id)\n    WHERE avg_order > 500\n\'\'\')\nprint(\"Customers with avg order > 500:\", rows)"}
    ],
    "rw": {
        "title": "Sales Ranking with Subqueries",
        "scenario": "A sales ops team needs to find reps in each region who beat both their regional average AND the company average — combining correlated subqueries with derived tables.",
        "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE sales (id INTEGER, rep TEXT, region TEXT, amount REAL, quarter INTEGER)\'\'\')\nrunmany(\'INSERT INTO sales VALUES (?,?,?,?,?)\', [\n    (1,\'Alice\',\'North\',1200,1),(2,\'Bob\',\'North\',800,1),(3,\'Carol\',\'South\',1500,1),\n    (4,\'Dave\',\'South\',600,1),(5,\'Eve\',\'North\',2000,2),(6,\'Frank\',\'South\',950,2),\n    (7,\'Grace\',\'East\',1100,1),(8,\'Henry\',\'East\',750,1),(9,\'Iris\',\'East\',1300,2),\n])\ncompany_avg = run(\'SELECT AVG(amount) FROM sales\')[0][0]\nprint(f\"Company avg: ${company_avg:,.0f}\")\n\nrows = run(f\'\'\'\n    SELECT s.rep, s.region, s.amount,\n           ROUND(regional.avg_amount, 0) AS regional_avg\n    FROM sales s\n    JOIN (\n        SELECT region, AVG(amount) AS avg_amount\n        FROM sales GROUP BY region\n    ) regional ON s.region = regional.region\n    WHERE s.amount > regional.avg_amount\n      AND s.amount > {company_avg}\n    ORDER BY s.region, s.amount DESC\n\'\'\')\nprint(\"Reps beating both regional AND company average:\")\nfor r in rows:\n    print(f\"  {r[0]} ({r[1]}): ${r[2]:,.0f} > regional ${r[3]:,.0f}\")"
    },
    "practice": {
        "title": "Self-referencing Subquery",
        "desc": "Create a products table (id, name, category, price, cost). Write: (1) A query using a scalar subquery to show each product with its category\'s avg price. (2) A correlated subquery to find the cheapest product in each category. (3) A derived table query to show categories where avg margin (price-cost)/price > 30%.",
        "starter": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE products (id INT, name TEXT, category TEXT, price REAL, cost REAL)\'\'\')\nrunmany(\'INSERT INTO products VALUES (?,?,?,?,?)\', [\n    (1,\'Apple\',\'Fruit\',1.2,0.4),(2,\'Banana\',\'Fruit\',0.5,0.15),(3,\'Carrot\',\'Veg\',0.8,0.3),\n    (4,\'Potato\',\'Veg\',0.6,0.2),(5,\'Milk\',\'Dairy\',1.5,0.8),(6,\'Cheese\',\'Dairy\',4.0,1.5),\n    (7,\'Yogurt\',\'Dairy\',2.0,0.9),(8,\'Broccoli\',\'Veg\',1.1,0.4),\n])\n\n# 1. Each product with its category avg price\nprint(\"=== Product vs Category Avg ===\")\n# TODO: write query with scalar correlated subquery for category avg\n\n# 2. Cheapest product in each category\nprint(\"=== Cheapest per Category ===\")\n# TODO: use correlated subquery to find min price per category\n\n# 3. Categories with avg margin > 30%\nprint(\"=== High-Margin Categories ===\")\n# TODO: derived table with margin calc, then filter\n"
    }
    },

    {
    "title": "18. String Functions & Pattern Matching",
    "desc": "SQL provides rich string functions: UPPER/LOWER, SUBSTR, TRIM, REPLACE, LENGTH, INSTR, and LIKE/GLOB for pattern matching. Essential for cleaning and searching text data.",
    "examples": [
        {"label": "Core string functions", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE contacts (id INTEGER, name TEXT, email TEXT, phone TEXT)\'\'\')\nrunmany(\'INSERT INTO contacts VALUES (?,?,?,?)\', [\n    (1,\'  Alice Smith  \',\'alice@EXAMPLE.com\',\'(555) 123-4567\'),\n    (2,\'Bob  Jones\',\'bob.jones@mail.com\',\'555.987.6543\'),\n    (3,\'carol lee\',\'CAROL@COMPANY.ORG\',\'5551234567\'),\n    (4,\'DAVE BROWN\',\'dave@test.net\',\'555-111-2222\'),\n])\n\nrows = run(\'\'\'\n    SELECT\n        id,\n        TRIM(name)                              AS name_clean,\n        LOWER(TRIM(name))                       AS name_lower,\n        UPPER(SUBSTR(TRIM(name), 1, 1))         AS initial,\n        LOWER(email)                            AS email_lower,\n        LENGTH(TRIM(name))                      AS name_len,\n        INSTR(TRIM(name), \" \")                  AS space_pos,\n        -- Extract first name (up to first space)\n        SUBSTR(TRIM(name), 1, INSTR(TRIM(name)||\" \", \" \")-1) AS first_name\n    FROM contacts\n\'\'\')\nfor r in rows:\n    print(f\"  ID {r[0]}: \'{r[1]}\' | initial={r[2]} | fname={r[7]}\")"},
        {"label": "LIKE and GLOB pattern matching", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE products (id INTEGER, sku TEXT, name TEXT, category TEXT)\'\'\')\nrunmany(\'INSERT INTO products VALUES (?,?,?,?)\', [\n    (1,\'FRUIT-APL-001\',\'Apple (Red)\',\'Fruit\'),\n    (2,\'FRUIT-BAN-002\',\'Banana\',\'Fruit\'),\n    (3,\'VEG-CAR-001\',\'Carrot\',\'Vegetable\'),\n    (4,\'VEG-POT-002\',\'Potato\',\'Vegetable\'),\n    (5,\'DAIRY-MLK-001\',\'Whole Milk\',\'Dairy\'),\n    (6,\'FRUIT-APL-002\',\'Apple (Green)\',\'Fruit\'),\n    (7,\'DAIRY-CHZ-001\',\'Cheddar Cheese\',\'Dairy\'),\n])\n\n# LIKE: case-insensitive %, _ wildcards\nrows = run(\"SELECT name FROM products WHERE name LIKE \'Apple%\'\")\nprint(\"Starts with \'Apple\':\", [r[0] for r in rows])\n\nrows = run(\"SELECT name FROM products WHERE name LIKE \'%e%\'\")\nprint(\"Contains \'e\':\", [r[0] for r in rows])\n\nrows = run(\"SELECT sku FROM products WHERE sku LIKE \'FRUIT-___-___\'\")\nprint(\"SKUs matching FRUIT-???-???:\", [r[0] for r in rows])\n\n# GLOB: case-sensitive, uses * and ? (Unix-style)\nrows = run(\"SELECT sku FROM products WHERE sku GLOB \'FRUIT-*\'\")\nprint(\"GLOB FRUIT-*:\", [r[0] for r in rows])\n\nrows = run(\"SELECT sku FROM products WHERE sku GLOB \'*-001\'\")\nprint(\"GLOB *-001:\", [r[0] for r in rows])\n\n# NOT LIKE\nrows = run(\"SELECT name FROM products WHERE name NOT LIKE \'%Apple%\'\")\nprint(\"Not apple:\", [r[0] for r in rows])"},
        {"label": "String manipulation and cleaning", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE raw_data (id INTEGER, raw_phone TEXT, raw_email TEXT)\'\'\')\nrunmany(\'INSERT INTO raw_data VALUES (?,?,?)\', [\n    (1,\'(555) 123-4567\',\'  User@Example.COM  \'),\n    (2,\'555.987.6543\',\'bob.jones@MAIL.COM\'),\n    (3,\'5551234567\',\'CAROL@company.org\'),\n])\n\nrows = run(\'\'\'\n    SELECT\n        id,\n        -- Normalize phone: keep only digits via REPLACE chain\n        REPLACE(REPLACE(REPLACE(REPLACE(raw_phone, \"(\", \"\"), \")\", \"\"), \"-\", \"\"), \".\", \"\") AS phone_digits,\n        -- Trim spaces and lowercase email\n        LOWER(TRIM(raw_email)) AS email_clean,\n        -- Extract domain from email\n        SUBSTR(\n            LOWER(TRIM(raw_email)),\n            INSTR(LOWER(TRIM(raw_email)), \"@\") + 1\n        ) AS domain,\n        -- Check email format (has @ and .)\n        CASE WHEN INSTR(raw_email, \"@\") > 0 AND INSTR(raw_email, \".\") > 0\n             THEN \"valid\" ELSE \"invalid\" END AS email_status\n    FROM raw_data\n\'\'\')\nfor r in rows:\n    print(f\"  ID {r[0]}: phone={r[1]}, email={r[2]}, domain={r[3]}, {r[4]}\")\n\n# REPLACE for data masking\nrows = run(\'\'\'\n    SELECT id,\n           SUBSTR(phone_digits, 1, 3) || \"****\" || SUBSTR(phone_digits, 8) AS masked\n    FROM (SELECT id, REPLACE(REPLACE(REPLACE(raw_phone,\"(\",\"\"),\")\",\"\"),\"-\",\"\") AS phone_digits\n          FROM raw_data)\n\'\'\')\nprint(\"Masked phones:\", [(r[0], r[1]) for r in rows])"}
    ],
    "rw": {
        "title": "Email Domain Analysis",
        "scenario": "A marketing team analyzes which email domains their B2B customers use, normalizing inconsistent formatting before aggregating.",
        "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE customers (id INTEGER, email TEXT, tier TEXT)\'\'\')\nrunmany(\'INSERT INTO customers VALUES (?,?,?)\', [\n    (1,\'alice@ACME.COM\',\'gold\'),(2,\'bob@tech.org\',\'silver\'),\n    (3,\'carol@acme.com\',\'gold\'),(4,\'dave@STARTUP.IO\',\'bronze\'),\n    (5,\'eve@TECH.ORG\',\'silver\'),(6,\'frank@enterprise.net\',\'gold\'),\n    (7,\'grace@startup.io\',\'bronze\'),(8,\'henry@acme.com\',\'silver\'),\n    (9,\'iris@ENTERPRISE.NET\',\'gold\'),(10,\'jack@freelance.dev\',\'bronze\'),\n])\n\nrows = run(\'\'\'\n    SELECT\n        LOWER(SUBSTR(email, INSTR(email, \"@\") + 1)) AS domain,\n        COUNT(*)                                      AS customers,\n        SUM(CASE WHEN tier = \"gold\"   THEN 1 ELSE 0 END) AS gold,\n        SUM(CASE WHEN tier = \"silver\" THEN 1 ELSE 0 END) AS silver,\n        SUM(CASE WHEN tier = \"bronze\" THEN 1 ELSE 0 END) AS bronze\n    FROM customers\n    GROUP BY LOWER(SUBSTR(email, INSTR(email, \"@\") + 1))\n    ORDER BY customers DESC\n\'\'\')\nprint(\"Domain analysis:\")\nfor r in rows:\n    print(f\"  {r[0]:<20} total={r[1]} gold={r[2]} silver={r[3]} bronze={r[4]}\")"
    },
    "practice": {
        "title": "Name Formatter",
        "desc": "Create a people table (id, full_name, email). Write a query that produces: first_name (before first space), last_name (after last space), initials (first letter of each word), username (lowercase first_name + \'.\' + last 4 of email before @), and email_valid (1 if contains \'@\' and \'.\', else 0).",
        "starter": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE people (id INT, full_name TEXT, email TEXT)\'\'\')\nrunmany(\'INSERT INTO people VALUES (?,?,?)\', [\n    (1,\'Alice Marie Smith\',\'alice.smith@company.com\'),\n    (2,\'Bob Jones\',\'bob@mail.net\'),\n    (3,\'Carol Ann Lee\',\'carol.lee@invalid\'),\n    (4,\'Dave\',\'dave@x.io\'),\n])\n\nrows = run(\'\'\'\n    SELECT\n        id,\n        -- first_name: text before first space\n        SUBSTR(full_name, 1,\n               CASE WHEN INSTR(full_name, \" \") > 0\n                    THEN INSTR(full_name, \" \")-1\n                    ELSE LENGTH(full_name) END) AS first_name,\n        -- TODO: last_name (after last space, or full_name if no space)\n        -- TODO: initials\n        -- TODO: username (lower_first + . + last 4 chars before @)\n        -- TODO: email_valid\n        email\n    FROM people\n\'\'\')\nfor r in rows: print(r)\n"
    }
    },

    {
    "title": "19. Date & Time Functions",
    "desc": "SQL date functions compute differences, extract components, and format timestamps. In SQLite, dates are stored as TEXT (ISO), INTEGER (Unix epoch), or REAL (Julian day).",
    "examples": [
        {"label": "Date arithmetic and formatting (SQLite)", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\n# SQLite stores dates as text in ISO format: \'YYYY-MM-DD\'\nrows = run(\'\'\'\n    SELECT\n        DATE(\'now\')                           AS today,\n        DATE(\'now\', \'+7 days\')               AS next_week,\n        DATE(\'now\', \'-30 days\')              AS last_month,\n        DATE(\'now\', \'start of month\')        AS month_start,\n        DATE(\'now\', \'start of year\')         AS year_start,\n        DATE(\'now\', \'+1 year\', \'-1 day\')     AS end_of_next_year,\n        DATETIME(\'now\')                       AS now_dt,\n        STRFTIME(\'%Y-%m-%d %H:%M\', \'now\')    AS formatted\n\'\'\')\nfor key, val in zip([\'today\',\'next_week\',\'last_month\',\'month_start\',\'year_start\',\'eony\',\'now_dt\',\'fmt\'], rows[0]):\n    print(f\"  {key}: {val}\")"},
        {"label": "Extracting date parts and calculating age", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE employees (id INTEGER, name TEXT, hire_date TEXT, birth_date TEXT)\'\'\')\nrunmany(\'INSERT INTO employees VALUES (?,?,?,?)\', [\n    (1,\'Alice\',\'2019-03-15\',\'1990-07-22\'),\n    (2,\'Bob\',\'2021-11-01\',\'1985-02-14\'),\n    (3,\'Carol\',\'2022-06-20\',\'1995-09-08\'),\n    (4,\'Dave\',\'2018-01-10\',\'1988-12-01\'),\n])\n\nrows = run(\'\'\'\n    SELECT\n        name,\n        hire_date,\n        -- Extract parts\n        STRFTIME(\'%Y\', hire_date)               AS hire_year,\n        STRFTIME(\'%m\', hire_date)               AS hire_month,\n        STRFTIME(\'%d\', hire_date)               AS hire_day,\n        -- Days since hire\n        CAST(JULIANDAY(\'now\') - JULIANDAY(hire_date) AS INTEGER) AS days_employed,\n        -- Years employed\n        CAST((JULIANDAY(\'now\') - JULIANDAY(hire_date)) / 365.25 AS INTEGER) AS years_employed,\n        -- Age from birth_date\n        CAST((JULIANDAY(\'now\') - JULIANDAY(birth_date)) / 365.25 AS INTEGER) AS age\n    FROM employees\n    ORDER BY hire_date\n\'\'\')\nprint(\"Employee tenure and age:\")\nfor r in rows:\n    print(f\"  {r[0]}: hired {r[1]}, {r[7]} days ({r[8]} yrs), age {r[9]}\")"},
        {"label": "Time series date bucketing", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nimport datetime\nrun(\'\'\'CREATE TABLE events (id INTEGER, ts TEXT, event TEXT, value REAL)\'\'\')\nimport random; random.seed(42)\nevents_data = []\nfor i in range(30):\n    d = datetime.date(2024, 1, 1) + datetime.timedelta(days=i)\n    for _ in range(random.randint(1, 5)):\n        events_data.append((i*10+random.randint(1,9),\n                            d.strftime(\'%Y-%m-%d\'),\n                            random.choice([\'view\',\'click\',\'purchase\']),\n                            round(random.uniform(1, 100), 2)))\nrunmany(\'INSERT INTO events VALUES (?,?,?,?)\', events_data)\n\n# Group by week\nrows = run(\'\'\'\n    SELECT\n        STRFTIME(\'%Y-W%W\', ts)         AS week,\n        COUNT(*)                        AS events,\n        SUM(CASE WHEN event=\"purchase\" THEN 1 ELSE 0 END) AS purchases,\n        ROUND(SUM(value), 2)            AS total_value\n    FROM events\n    GROUP BY week\n    ORDER BY week\n\'\'\')\nprint(\"Weekly breakdown:\")\nfor r in rows: print(f\"  {r[0]}: {r[1]} events, {r[2]} purchases, ${r[3]}\")\n\n# Days with no purchases\nrows = run(\'\'\'\n    SELECT ts, COUNT(*) AS events\n    FROM events\n    WHERE event != \"purchase\"\n    AND ts NOT IN (SELECT DISTINCT ts FROM events WHERE event = \"purchase\")\n    GROUP BY ts\n    ORDER BY ts\n    LIMIT 3\n\'\'\')\nprint(\"Days with no purchases (sample):\", [(r[0],r[1]) for r in rows])"}
    ],
    "rw": {
        "title": "Subscription Churn Analysis",
        "scenario": "A SaaS company analyzes monthly churn by comparing subscription start/end dates, computing tenure, and flagging customers who churned within 90 days of signup.",
        "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE subscriptions (id INT, cust_id INT, start_date TEXT, end_date TEXT, plan TEXT)\'\'\')\nrunmany(\'INSERT INTO subscriptions VALUES (?,?,?,?,?)\', [\n    (1,1,\'2023-01-15\',\'2024-01-15\',\'annual\'),\n    (2,2,\'2023-03-01\',\'2023-05-15\',\'monthly\'),\n    (3,3,\'2023-06-01\',None,\'annual\'),\n    (4,4,\'2023-09-10\',\'2023-10-05\',\'monthly\'),\n    (5,5,\'2024-01-01\',None,\'monthly\'),\n    (6,6,\'2023-02-14\',\'2023-11-30\',\'annual\'),\n])\n\nrows = run(\'\'\'\n    SELECT\n        cust_id, plan, start_date,\n        COALESCE(end_date, DATE(\"now\")) AS effective_end,\n        CAST((JULIANDAY(COALESCE(end_date, DATE(\"now\"))) -\n              JULIANDAY(start_date)) AS INTEGER)         AS tenure_days,\n        CASE WHEN end_date IS NOT NULL THEN \"churned\" ELSE \"active\" END AS status,\n        CASE WHEN end_date IS NOT NULL\n              AND JULIANDAY(end_date) - JULIANDAY(start_date) < 90\n             THEN \"early_churn\" ELSE \"ok\" END AS churn_flag\n    FROM subscriptions\n    ORDER BY start_date\n\'\'\')\nprint(\"Subscription analysis:\")\nfor r in rows:\n    print(f\"  Cust {r[0]} ({r[1]}): {r[4]} days, {r[5]}, {r[6]}\")"
    },
    "practice": {
        "title": "Date Range Queries",
        "desc": "Create a bookings table (id, room, check_in, check_out, guest). Write: (1) Find bookings overlapping a given date range (\'2024-06-01\' to \'2024-06-10\'). (2) Calculate avg stay length by month. (3) Find rooms that were booked more than 80% of days in Q2 2024. (4) Show guests with return visits within 6 months.",
        "starter": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE bookings (id INT, room TEXT, check_in TEXT, check_out TEXT, guest TEXT)\'\'\')\nrunmany(\'INSERT INTO bookings VALUES (?,?,?,?,?)\', [\n    (1,\'101\',\'2024-05-28\',\'2024-06-03\',\'Alice\'),\n    (2,\'102\',\'2024-06-05\',\'2024-06-08\',\'Bob\'),\n    (3,\'101\',\'2024-06-10\',\'2024-06-15\',\'Carol\'),\n    (4,\'103\',\'2024-06-01\',\'2024-06-30\',\'Dave\'),\n    (5,\'102\',\'2024-07-01\',\'2024-07-05\',\'Alice\'),\n    (6,\'101\',\'2024-08-01\',\'2024-08-10\',\'Bob\'),\n])\n\n# 1. Overlapping bookings with date range\ntarget_in, target_out = \'2024-06-01\', \'2024-06-10\'\nprint(\"=== Bookings overlapping Jun 1-10 ===\")\nrows = run(f\'\'\'\n    SELECT room, guest, check_in, check_out\n    FROM bookings\n    WHERE check_in < \"{target_out}\" AND check_out > \"{target_in}\"\n    ORDER BY check_in\n\'\'\')\nfor r in rows: print(f\"  {r}\")\n\n# 2. Avg stay length by month\nprint(\"=== Avg stay by month ===\")\nrows = run(\'\'\'\n    SELECT\n        STRFTIME(\"%Y-%m\", check_in) AS month,\n        ROUND(AVG(JULIANDAY(check_out) - JULIANDAY(check_in)), 1) AS avg_nights,\n        COUNT(*) AS bookings\n    FROM bookings GROUP BY month ORDER BY month\n\'\'\')\nfor r in rows: print(f\"  {r}\")\n\n# 3. TODO: rooms booked > 80% of Q2 days\n# 4. TODO: return visits within 6 months\n"
    }
    },

    {
    "title": "20. CASE WHEN & Conditional Logic",
    "desc": "CASE WHEN is SQL\'s conditional expression. Use it for bucketing, pivoting, null handling, and complex conditional aggregations. Combined with COALESCE and NULLIF for robust null handling.",
    "examples": [
        {"label": "Simple and searched CASE", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE students (id INTEGER, name TEXT, score INTEGER, grade TEXT)\'\'\')\nrunmany(\'INSERT INTO students VALUES (?,?,?,?)\', [\n    (1,\'Alice\',95,None),(2,\'Bob\',72,None),(3,\'Carol\',88,None),\n    (4,\'Dave\',61,None),(5,\'Eve\',79,None),(6,\'Frank\',55,None),\n])\n\nrows = run(\'\'\'\n    SELECT\n        name, score,\n        -- Searched CASE (most flexible)\n        CASE\n            WHEN score >= 90 THEN \"A\"\n            WHEN score >= 80 THEN \"B\"\n            WHEN score >= 70 THEN \"C\"\n            WHEN score >= 60 THEN \"D\"\n            ELSE \"F\"\n        END AS letter_grade,\n        -- Simple CASE (like switch)\n        CASE ROUND(score/10)*10\n            WHEN 100 THEN \"Perfect\"\n            WHEN 90  THEN \"Excellent\"\n            WHEN 80  THEN \"Good\"\n            WHEN 70  THEN \"Pass\"\n            ELSE \"Fail\"\n        END AS band,\n        -- Boolean expression\n        CASE WHEN score >= 70 THEN 1 ELSE 0 END AS passed\n    FROM students\n    ORDER BY score DESC\n\'\'\')\nfor r in rows:\n    print(f\"  {r[0]}: {r[1]} -> {r[2]} ({r[3]}) passed={r[4]}\")"},
        {"label": "CASE in aggregations (conditional counting)", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE orders (id INTEGER, status TEXT, region TEXT, total REAL)\'\'\')\nrunmany(\'INSERT INTO orders VALUES (?,?,?,?)\', [\n    (1,\'completed\',\'North\',500),(2,\'cancelled\',\'South\',300),(3,\'completed\',\'North\',800),\n    (4,\'pending\',\'East\',200),(5,\'completed\',\'South\',650),(6,\'cancelled\',\'North\',400),\n    (7,\'completed\',\'East\',1200),(8,\'pending\',\'South\',350),(9,\'completed\',\'East\',900),\n])\n\nrows = run(\'\'\'\n    SELECT\n        region,\n        COUNT(*)                                              AS total_orders,\n        SUM(CASE WHEN status = \"completed\" THEN 1 ELSE 0 END) AS completed,\n        SUM(CASE WHEN status = \"cancelled\" THEN 1 ELSE 0 END) AS cancelled,\n        SUM(CASE WHEN status = \"pending\"   THEN 1 ELSE 0 END) AS pending,\n        ROUND(100.0 * SUM(CASE WHEN status=\"completed\" THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_pct,\n        ROUND(SUM(CASE WHEN status=\"completed\" THEN total ELSE 0 END), 0) AS completed_revenue,\n        ROUND(AVG(CASE WHEN status=\"completed\" THEN total ELSE NULL END), 0) AS avg_completed\n    FROM orders\n    GROUP BY region\n    ORDER BY completed_revenue DESC\n\'\'\')\nprint(\"Order analysis by region:\")\nfor r in rows:\n    print(f\"  {r[0]}: {r[1]} orders, {r[2]} completed ({r[5]}%), revenue=${r[6]}, avg=${r[7]}\")"},
        {"label": "COALESCE, NULLIF, and IIF", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE metrics (id INTEGER, name TEXT, q1 REAL, q2 REAL, q3 REAL, q4 REAL)\'\'\')\nrunmany(\'INSERT INTO metrics VALUES (?,?,?,?,?,?)\', [\n    (1,\'Revenue\',1000,None,1200,None),\n    (2,\'Costs\',600,700,None,650),\n    (3,\'Users\',500,520,None,None),\n])\n\nrows = run(\'\'\'\n    SELECT\n        name,\n        -- COALESCE: return first non-NULL value\n        COALESCE(q1, 0)                    AS q1_safe,\n        COALESCE(q2, q1, 0)               AS q2_or_q1,  -- fill q2 from q1\n        COALESCE(q3, q2, q1, 0)           AS q3_fill,\n\n        -- NULLIF: return NULL if two values are equal\n        NULLIF(q1, 0)                      AS q1_null_if_zero,\n\n        -- IIF (SQLite 3.32+): shorthand for simple CASE WHEN\n        IIF(q4 IS NULL, \"missing\", \"present\") AS q4_status,\n\n        -- Compute quarter growth (handles NULLs gracefully)\n        CASE WHEN q1 IS NOT NULL AND q2 IS NOT NULL\n             THEN ROUND((q2 - q1) / q1 * 100, 1)\n             ELSE NULL END AS q1_q2_growth_pct\n    FROM metrics\n\'\'\')\nprint(\"Metric analysis:\")\nfor r in rows:\n    print(f\"  {r[0]}: q1_safe={r[1]}, q2_or_q1={r[2]}, q3_fill={r[3]}, q4={r[5]}, growth={r[6]}\")"}
    ],
    "rw": {
        "title": "Customer Segmentation",
        "scenario": "A CRM team segments customers by RFM score (Recency, Frequency, Monetary) using CASE WHEN on aggregated purchase data to assign Bronze/Silver/Gold/Platinum tiers.",
        "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE purchases (id INT, cust_id INT, amount REAL, purchase_date TEXT)\'\'\')\nrunmany(\'INSERT INTO purchases VALUES (?,?,?,?)\', [\n    (1,1,150,\'2024-01-10\'),(2,1,200,\'2024-02-15\'),(3,1,180,\'2024-03-01\'),\n    (4,2,500,\'2024-03-20\'),(5,2,300,\'2024-03-25\'),\n    (6,3,50,\'2023-12-01\'),(7,4,1000,\'2024-03-28\'),(8,4,800,\'2024-03-29\'),\n    (9,4,600,\'2024-03-30\'),\n])\n\nrows = run(\'\'\'\n    WITH rfm AS (\n        SELECT\n            cust_id,\n            CAST(JULIANDAY(\"2024-04-01\") - JULIANDAY(MAX(purchase_date)) AS INT) AS recency_days,\n            COUNT(*) AS frequency,\n            ROUND(SUM(amount), 0) AS monetary\n        FROM purchases GROUP BY cust_id\n    )\n    SELECT\n        cust_id, recency_days, frequency, monetary,\n        CASE\n            WHEN recency_days <= 7  AND frequency >= 3 AND monetary >= 500 THEN \"Platinum\"\n            WHEN recency_days <= 30 AND frequency >= 2                      THEN \"Gold\"\n            WHEN recency_days <= 60                                          THEN \"Silver\"\n            ELSE \"Bronze\"\n        END AS tier\n    FROM rfm ORDER BY monetary DESC\n\'\'\')\nprint(\"Customer RFM tiers:\")\nfor r in rows:\n    print(f\"  Cust {r[0]}: recency={r[1]}d, freq={r[2]}, monetary=${r[3]} -> {r[4]}\")"
    },
    "practice": {
        "title": "Score Bucketing",
        "desc": "Create a test_results table (student_id, subject, score). Write: (1) A pivot showing each subject\'s count of A/B/C/D/F grades using CASE in SUM. (2) A letter grade column + \'needs_review\' flag (grade D or F). (3) Each student\'s weakest subject (lowest score). (4) Students who improved: passed all subjects (score >= 70).",
        "starter": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE test_results (student_id INT, subject TEXT, score INT)\'\'\')\nrunmany(\'INSERT INTO test_results VALUES (?,?,?)\', [\n    (1,\'Math\',85),(1,\'English\',72),(1,\'Science\',90),\n    (2,\'Math\',60),(2,\'English\',88),(2,\'Science\',55),\n    (3,\'Math\',95),(3,\'English\',91),(3,\'Science\',87),\n    (4,\'Math\',70),(4,\'English\',65),(4,\'Science\',80),\n])\n\n# 1. Pivot: count of each grade per subject\nprint(\"=== Grade Distribution by Subject ===\")\nrows = run(\'\'\'\n    SELECT subject,\n           SUM(CASE WHEN score >= 90 THEN 1 ELSE 0 END) AS A_count,\n           SUM(CASE WHEN score >= 80 AND score < 90 THEN 1 ELSE 0 END) AS B_count,\n           SUM(CASE WHEN score >= 70 AND score < 80 THEN 1 ELSE 0 END) AS C_count,\n           SUM(CASE WHEN score < 70 THEN 1 ELSE 0 END) AS D_or_F_count\n    FROM test_results GROUP BY subject\n\'\'\')\nfor r in rows: print(f\"  {r}\")\n\n# 2. TODO: letter grade + needs_review flag\n# 3. TODO: weakest subject per student\n# 4. TODO: students passing all subjects\n"
    }
    },

    {
    "title": "21. Set Operations (UNION, INTERSECT, EXCEPT)",
    "desc": "SQL set operations combine results of multiple SELECT statements: UNION (all unique), UNION ALL (keep duplicates), INTERSECT (common rows), and EXCEPT/MINUS (rows in first but not second).",
    "examples": [
        {"label": "UNION and UNION ALL", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE customers_2023 (id INTEGER, name TEXT, email TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE customers_2024 (id INTEGER, name TEXT, email TEXT)\'\'\')\nrunmany(\'INSERT INTO customers_2023 VALUES (?,?,?)\', [\n    (1,\'Alice\',\'alice@mail.com\'),(2,\'Bob\',\'bob@mail.com\'),\n    (3,\'Carol\',\'carol@mail.com\'),(4,\'Dave\',\'dave@mail.com\'),\n])\nrunmany(\'INSERT INTO customers_2024 VALUES (?,?,?)\', [\n    (3,\'Carol\',\'carol@mail.com\'),(4,\'Dave\',\'dave@mail.com\'),\n    (5,\'Eve\',\'eve@mail.com\'),(6,\'Frank\',\'frank@mail.com\'),\n])\n\n# UNION: unique rows only (deduplicates)\nrows = run(\'\'\'\n    SELECT \"2023\" AS year, name FROM customers_2023\n    UNION\n    SELECT \"2024\" AS year, name FROM customers_2024\n    ORDER BY name\n\'\'\')\nprint(f\"UNION (unique names): {len(rows)} rows\")\nfor r in rows: print(f\"  {r}\")\n\n# UNION ALL: keeps all rows including duplicates\nrows = run(\'\'\'\n    SELECT \"2023\" AS cohort, name FROM customers_2023\n    UNION ALL\n    SELECT \"2024\" AS cohort, name FROM customers_2024\n    ORDER BY name\n\'\'\')\nprint(f\"UNION ALL (all rows): {len(rows)} rows\")\n\n# Useful: combine logs from two tables\nrows = run(\'\'\'\n    SELECT \"new_customer\" AS event, name, \"2023\" AS yr FROM customers_2023\n    UNION ALL\n    SELECT \"new_customer\", name, \"2024\" FROM customers_2024\n    ORDER BY yr, name\n\'\'\')\nprint(\"All customer events:\", len(rows))"},
        {"label": "INTERSECT and EXCEPT", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE eligible_2023 (cust_id INTEGER)\'\'\')\nrun(\'\'\'CREATE TABLE eligible_2024 (cust_id INTEGER)\'\'\')\nrun(\'\'\'CREATE TABLE opted_out (cust_id INTEGER)\'\'\')\nrunmany(\'INSERT INTO eligible_2023 VALUES (?)\', [(i,) for i in [1,2,3,4,5,6]])\nrunmany(\'INSERT INTO eligible_2024 VALUES (?)\', [(i,) for i in [3,4,5,6,7,8]])\nrunmany(\'INSERT INTO opted_out VALUES (?)\', [(i,) for i in [2,5,8]])\n\n# INTERSECT: rows that appear in BOTH queries\nrows = run(\'\'\'\n    SELECT cust_id FROM eligible_2023\n    INTERSECT\n    SELECT cust_id FROM eligible_2024\n    ORDER BY cust_id\n\'\'\')\nprint(\"Eligible BOTH years:\", [r[0] for r in rows])\n\n# EXCEPT: rows in first but NOT in second\nrows = run(\'\'\'\n    SELECT cust_id FROM eligible_2023\n    EXCEPT\n    SELECT cust_id FROM eligible_2024\n\'\'\')\nprint(\"Only eligible in 2023:\", [r[0] for r in rows])\n\n# Combine: eligible both years, excluding opted-out\nrows = run(\'\'\'\n    SELECT cust_id FROM eligible_2023\n    INTERSECT\n    SELECT cust_id FROM eligible_2024\n    EXCEPT\n    SELECT cust_id FROM opted_out\n    ORDER BY cust_id\n\'\'\')\nprint(\"Eligible both years AND not opted out:\", [r[0] for r in rows])"},
        {"label": "Set operations for data reconciliation", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE source_records (id INTEGER, value REAL, ts TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE target_records (id INTEGER, value REAL, ts TEXT)\'\'\')\nrunmany(\'INSERT INTO source_records VALUES (?,?,?)\', [\n    (1,100.0,\'2024-01-01\'),(2,200.0,\'2024-01-02\'),(3,300.0,\'2024-01-03\'),\n    (4,400.0,\'2024-01-04\'),(5,500.0,\'2024-01-05\'),\n])\nrunmany(\'INSERT INTO target_records VALUES (?,?,?)\', [\n    (1,100.0,\'2024-01-01\'),(2,201.0,\'2024-01-02\'),  # id=2 has wrong value\n    (3,300.0,\'2024-01-03\'),                           # id=4,5 missing\n    (6,600.0,\'2024-01-06\'),                           # id=6 is extra\n])\n\n# Records in source but not in target (missing)\nmissing = run(\'\'\'\n    SELECT id, value, \"missing_from_target\" AS issue FROM source_records\n    EXCEPT\n    SELECT id, value, \"missing_from_target\" FROM target_records\n\'\'\')\nprint(\"Issues in reconciliation:\")\nfor r in missing: print(f\"  Source id={r[0]}, value={r[1]} not in target\")\n\n# Records in target but not in source (extra)\nextra = run(\'\'\'\n    SELECT id, value FROM target_records\n    EXCEPT\n    SELECT id, value FROM source_records\n\'\'\')\nfor r in extra: print(f\"  Target id={r[0]}, value={r[1]} not in source\")\n\n# Exact matches\nmatched = run(\'\'\'\n    SELECT COUNT(*) FROM (\n        SELECT id, value FROM source_records\n        INTERSECT\n        SELECT id, value FROM target_records\n    )\n\'\'\')\nprint(f\"Exactly matched records: {matched[0][0]}\")"}
    ],
    "rw": {
        "title": "Data Migration Audit",
        "scenario": "A data engineering team validates a migration by comparing source and destination tables using INTERSECT and EXCEPT to find missing, extra, and mismatched records.",
        "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE source_customers (id INT, name TEXT, email TEXT, tier TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE migrated_customers (id INT, name TEXT, email TEXT, tier TEXT)\'\'\')\nrunmany(\'INSERT INTO source_customers VALUES (?,?,?,?)\', [\n    (1,\'Alice\',\'alice@a.com\',\'gold\'),(2,\'Bob\',\'bob@b.com\',\'silver\'),\n    (3,\'Carol\',\'carol@c.com\',\'bronze\'),(4,\'Dave\',\'dave@d.com\',\'gold\'),\n    (5,\'Eve\',\'eve@e.com\',\'silver\'),\n])\nrunmany(\'INSERT INTO migrated_customers VALUES (?,?,?,?)\', [\n    (1,\'Alice\',\'alice@a.com\',\'gold\'),(2,\'Bob\',\'bob_new@b.com\',\'silver\'),\n    (3,\'Carol\',\'carol@c.com\',\'bronze\'),(6,\'Frank\',\'frank@f.com\',\'bronze\'),\n])\n\nfully_matched = run(\'\'\'\n    SELECT COUNT(*) FROM (\n        SELECT id,name,email,tier FROM source_customers\n        INTERSECT\n        SELECT id,name,email,tier FROM migrated_customers)\'\'\')[0][0]\nmissing_in_dest = run(\'\'\'\n    SELECT id, name FROM source_customers\n    EXCEPT SELECT id, name FROM migrated_customers\'\'\')\nextra_in_dest = run(\'\'\'\n    SELECT id, name FROM migrated_customers\n    EXCEPT SELECT id, name FROM source_customers\'\'\')\n\nprint(f\"Source: {run(\'SELECT COUNT(*) FROM source_customers\')[0][0]} records\")\nprint(f\"Migrated: {run(\'SELECT COUNT(*) FROM migrated_customers\')[0][0]} records\")\nprint(f\"Fully matched: {fully_matched}\")\nprint(f\"Missing from dest: {[(r[0],r[1]) for r in missing_in_dest]}\")\nprint(f\"Extra in dest: {[(r[0],r[1]) for r in extra_in_dest]}\")"
    },
    "practice": {
        "title": "Set Operation Analytics",
        "desc": "Create active_users_jan, active_users_feb, active_users_mar tables (each with user_id). Write queries to find: (1) Users active all 3 months (INTERSECT x3). (2) Users active in Jan but NOT Feb (EXCEPT). (3) All unique users across 3 months (UNION). (4) Users active in exactly 2 of 3 months using INTERSECT/EXCEPT combinations.",
        "starter": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE active_jan (user_id INT)\'\'\')\nrun(\'\'\'CREATE TABLE active_feb (user_id INT)\'\'\')\nrun(\'\'\'CREATE TABLE active_mar (user_id INT)\'\'\')\nrunmany(\'INSERT INTO active_jan VALUES (?)\', [(i,) for i in [1,2,3,4,5,6]])\nrunmany(\'INSERT INTO active_feb VALUES (?)\', [(i,) for i in [2,3,4,5,7,8]])\nrunmany(\'INSERT INTO active_mar VALUES (?)\', [(i,) for i in [3,4,5,6,8,9]])\n\n# 1. All 3 months\nrows = run(\'\'\'\n    SELECT user_id FROM active_jan\n    INTERSECT SELECT user_id FROM active_feb\n    INTERSECT SELECT user_id FROM active_mar\n\'\'\')\nprint(\"Active all 3 months:\", [r[0] for r in rows])\n\n# 2. Jan but not Feb\nrows = run(\'SELECT user_id FROM active_jan EXCEPT SELECT user_id FROM active_feb\')\nprint(\"Jan but not Feb:\", [r[0] for r in rows])\n\n# 3. All unique\nrows = run(\'\'\'\n    SELECT user_id FROM active_jan UNION\n    SELECT user_id FROM active_feb UNION\n    SELECT user_id FROM active_mar ORDER BY user_id\n\'\'\')\nprint(\"All unique users:\", [r[0] for r in rows])\n\n# 4. TODO: Exactly 2 of 3 months\n"
    }
    },

    {
    "title": "22. Advanced CTEs & Chaining",
    "desc": "CTEs (WITH clauses) can be chained, referenced multiple times, and nested to build complex queries step by step. They replace temp tables in most cases and dramatically improve readability.",
    "examples": [
        {"label": "Multiple CTEs and chaining", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE transactions (id INT, cust_id INT, amount REAL, category TEXT, ts TEXT)\'\'\')\nrunmany(\'INSERT INTO transactions VALUES (?,?,?,?,?)\', [\n    (1,1,150,\'food\',\'2024-01-05\'),(2,1,300,\'tech\',\'2024-01-10\'),\n    (3,2,200,\'food\',\'2024-01-08\'),(4,2,100,\'food\',\'2024-01-12\'),\n    (5,3,500,\'tech\',\'2024-01-03\'),(6,3,250,\'clothing\',\'2024-01-15\'),\n    (7,1,80,\'food\',\'2024-02-01\'),(8,2,600,\'tech\',\'2024-02-05\'),\n    (9,3,120,\'food\',\'2024-02-10\'),\n])\n\nrows = run(\'\'\'\n    WITH\n    -- CTE 1: customer totals\n    cust_totals AS (\n        SELECT cust_id, SUM(amount) AS total_spend,\n               COUNT(*) AS n_transactions, MAX(ts) AS last_purchase\n        FROM transactions GROUP BY cust_id\n    ),\n    -- CTE 2: top category per customer\n    top_cat AS (\n        SELECT cust_id,\n               category,\n               SUM(amount) AS cat_total,\n               ROW_NUMBER() OVER (PARTITION BY cust_id ORDER BY SUM(amount) DESC) AS rn\n        FROM transactions GROUP BY cust_id, category\n    ),\n    -- CTE 3: combine using previous CTEs\n    summary AS (\n        SELECT ct.cust_id, ct.total_spend, ct.n_transactions, ct.last_purchase,\n               tc.category AS top_category\n        FROM cust_totals ct\n        JOIN top_cat tc ON ct.cust_id = tc.cust_id AND tc.rn = 1\n    )\n    SELECT *, ROUND(total_spend / n_transactions, 2) AS avg_txn\n    FROM summary ORDER BY total_spend DESC\n\'\'\')\nprint(\"Customer summary:\")\nfor r in rows:\n    print(f\"  Cust {r[0]}: ${r[1]} total, {r[2]} txns, top={r[4]}, avg=${r[5]}\")"},
        {"label": "Recursive CTE for hierarchies", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE org (id INT, name TEXT, manager_id INT, level INT)\'\'\')\nrunmany(\'INSERT INTO org VALUES (?,?,?,?)\', [\n    (1,\'CEO\',None,1),(2,\'CTO\',1,2),(3,\'CFO\',1,2),(4,\'VP Eng\',2,3),\n    (5,\'VP Data\',2,3),(6,\'Dir Finance\',3,3),(7,\'Sr Dev\',4,4),\n    (8,\'Data Eng\',5,4),(9,\'Analyst\',5,4),(10,\'Accountant\',6,4),\n])\n\n# Recursive CTE: traverse the org hierarchy\nrows = run(\'\'\'\n    WITH RECURSIVE hierarchy AS (\n        -- Base case: start from CEO (no manager)\n        SELECT id, name, manager_id, 0 AS depth, name AS path\n        FROM org WHERE manager_id IS NULL\n\n        UNION ALL\n\n        -- Recursive case: join to find reports\n        SELECT o.id, o.name, o.manager_id,\n               h.depth + 1,\n               h.path || \" -> \" || o.name\n        FROM org o\n        JOIN hierarchy h ON o.manager_id = h.id\n    )\n    SELECT depth, name, path FROM hierarchy ORDER BY path\n\'\'\')\nfor r in rows:\n    indent = \"  \" * r[0]\n    print(f\"{indent}{r[1]}\")\n\n# Count reports under each manager\nrows = run(\'\'\'\n    WITH RECURSIVE reports AS (\n        SELECT id, manager_id FROM org\n        UNION ALL\n        SELECT r.id, o.manager_id FROM reports r JOIN org o ON o.id = r.manager_id\n        WHERE o.manager_id IS NOT NULL\n    )\n    SELECT o.name, COUNT(*) AS total_reports\n    FROM org o JOIN reports r ON r.manager_id = o.id\n    GROUP BY o.id ORDER BY total_reports DESC LIMIT 5\n\'\'\')\nprint(\"Managers by total reports:\", [(r[0], r[1]) for r in rows])"},
        {"label": "CTEs for multi-step data transformations", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE raw_sales (rep TEXT, product TEXT, amount REAL, region TEXT, sale_date TEXT)\'\'\')\nimport random; random.seed(42)\nreps = [\'Alice\',\'Bob\',\'Carol\',\'Dave\',\'Eve\']\nprods = [\'Widget\',\'Gadget\',\'Gizmo\']\nregions = [\'North\',\'South\',\'East\']\nrows_data = [(random.choice(reps), random.choice(prods),\n              round(random.uniform(100,2000), 2),\n              random.choice(regions),\n              f\"2024-0{random.randint(1,3)}-{random.randint(1,28):02d}\")\n             for _ in range(50)]\nrunmany(\'INSERT INTO raw_sales VALUES (?,?,?,?,?)\', rows_data)\n\nrows = run(\'\'\'\n    WITH\n    -- Step 1: normalize and add month\n    cleaned AS (\n        SELECT rep, product, region, amount,\n               STRFTIME(\"%Y-%m\", sale_date) AS month\n        FROM raw_sales WHERE amount > 0\n    ),\n    -- Step 2: rep-level monthly totals\n    rep_monthly AS (\n        SELECT rep, month, SUM(amount) AS monthly_total,\n               COUNT(*) AS n_sales\n        FROM cleaned GROUP BY rep, month\n    ),\n    -- Step 3: rank reps per month\n    ranked AS (\n        SELECT *, RANK() OVER (PARTITION BY month ORDER BY monthly_total DESC) AS rank\n        FROM rep_monthly\n    )\n    -- Step 4: show top-2 per month\n    SELECT month, rank, rep, ROUND(monthly_total, 0) AS total, n_sales\n    FROM ranked WHERE rank <= 2\n    ORDER BY month, rank\n\'\'\')\nprint(\"Top 2 reps per month:\")\nfor r in rows: print(f\"  {r[0]} #{r[1]}: {r[2]} ${r[3]:,.0f} ({r[4]} sales)\")"}
    ],
    "rw": {
        "title": "Funnel Analysis",
        "scenario": "A product team uses chained CTEs to compute a conversion funnel: impression -> click -> add_to_cart -> purchase, with drop-off rates at each stage.",
        "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE funnel_events (user_id INT, event TEXT, ts TEXT)\'\'\')\nimport random; random.seed(42)\nevents_raw = []\nfor uid in range(1, 201):\n    events_raw.append((uid,\'impression\',\'2024-01\'))\n    if random.random() < 0.6:   events_raw.append((uid,\'click\',\'2024-01\'))\n    if random.random() < 0.4:   events_raw.append((uid,\'add_to_cart\',\'2024-01\'))\n    if random.random() < 0.35:  events_raw.append((uid,\'purchase\',\'2024-01\'))\nrunmany(\'INSERT INTO funnel_events VALUES (?,?,?)\', events_raw)\n\nrows = run(\'\'\'\n    WITH\n    stage_counts AS (\n        SELECT event,\n               COUNT(DISTINCT user_id) AS users\n        FROM funnel_events\n        GROUP BY event\n    ),\n    ordered AS (\n        SELECT event, users,\n               CASE event\n                   WHEN \"impression\"   THEN 1\n                   WHEN \"click\"        THEN 2\n                   WHEN \"add_to_cart\"  THEN 3\n                   WHEN \"purchase\"     THEN 4\n               END AS stage_order\n        FROM stage_counts\n    ),\n    with_prev AS (\n        SELECT event, users, stage_order,\n               LAG(users) OVER (ORDER BY stage_order) AS prev_users\n        FROM ordered\n    )\n    SELECT event, users,\n           CASE WHEN prev_users IS NOT NULL\n                THEN ROUND(100.0 * users / prev_users, 1)\n                ELSE 100.0 END AS step_pct,\n           ROUND(100.0 * users / MAX(users) OVER (), 1) AS overall_pct\n    FROM with_prev ORDER BY stage_order\n\'\'\')\nprint(\"Conversion funnel:\")\nfor r in rows:\n    bar = \"#\" * int(r[3] / 5)\n    print(f\"  {r[0]:15s}: {r[1]:>4d} users | step={r[2]:>5.1f}% | {bar}\")"
    },
    "practice": {
        "title": "CTE Report Builder",
        "desc": "Build a multi-CTE query that: CTE1 computes monthly revenue per product from an orders table, CTE2 computes 3-month moving average per product (using LAG), CTE3 flags months where revenue dropped more than 20% vs the moving average. Return only flagged months with product, month, revenue, avg, and drop_pct.",
        "starter": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE monthly_orders (product TEXT, month TEXT, revenue REAL)\'\'\')\nrunmany(\'INSERT INTO monthly_orders VALUES (?,?,?)\', [\n    (\'Widget\',\'2024-01\',1000),(\'Widget\',\'2024-02\',950),(\'Widget\',\'2024-03\',700),\n    (\'Widget\',\'2024-04\',980),(\'Gadget\',\'2024-01\',500),(\'Gadget\',\'2024-02\',520),\n    (\'Gadget\',\'2024-03\',480),(\'Gadget\',\'2024-04\',200),\n])\n\nrows = run(\'\'\'\n    WITH\n    -- CTE2: 3-month moving average using LAG\n    with_lags AS (\n        SELECT product, month, revenue,\n               LAG(revenue,1) OVER (PARTITION BY product ORDER BY month) AS prev1,\n               LAG(revenue,2) OVER (PARTITION BY product ORDER BY month) AS prev2\n        FROM monthly_orders\n    ),\n    moving_avg AS (\n        SELECT product, month, revenue,\n               ROUND((revenue + COALESCE(prev1,revenue) + COALESCE(prev2,revenue)) / 3.0, 1) AS ma3\n        FROM with_lags\n    ),\n    -- CTE3: flag months with >20% drop vs moving avg\n    flagged AS (\n        SELECT product, month, revenue, ma3,\n               ROUND((revenue - ma3) / ma3 * 100, 1) AS drop_pct\n        FROM moving_avg\n        WHERE revenue < ma3 * 0.8   -- more than 20% below MA\n    )\n    SELECT * FROM flagged ORDER BY drop_pct\n\'\'\')\nprint(\"Revenue alerts (>20% below 3-month MA):\")\nfor r in rows: print(f\"  {r[0]} {r[1]}: ${r[2]} vs MA ${r[3]} ({r[4]}%)\")\n"
    }
    },

    {
    "title": "23. Views & Virtual Tables",
    "desc": "Views are saved SELECT statements that behave like tables. They simplify complex queries, enforce access control, and create stable interfaces over evolving schema.",
    "examples": [
        {"label": "Creating and using views", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE employees (id INT, name TEXT, dept TEXT, salary REAL, hire_date TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE departments (id INT, name TEXT, budget REAL)\'\'\')\nrunmany(\'INSERT INTO employees VALUES (?,?,?,?,?)\', [\n    (1,\'Alice\',\'Eng\',90000,\'2020-03-15\'),(2,\'Bob\',\'Eng\',85000,\'2021-06-01\'),\n    (3,\'Carol\',\'Sales\',70000,\'2019-11-20\'),(4,\'Dave\',\'Sales\',72000,\'2022-01-10\'),\n    (5,\'Eve\',\'HR\',65000,\'2020-08-05\'),(6,\'Frank\',\'Eng\',95000,\'2018-04-22\'),\n])\nrunmany(\'INSERT INTO departments VALUES (?,?,?)\', [\n    (1,\'Eng\',500000),(2,\'Sales\',300000),(3,\'HR\',150000),\n])\n\n# Create a view\nrun(\'\'\'\n    CREATE VIEW emp_summary AS\n    SELECT e.id, e.name, e.dept, e.salary,\n           ROUND(100.0 * e.salary / d.budget, 2) AS salary_pct_budget,\n           CAST((JULIANDAY(\"now\") - JULIANDAY(e.hire_date)) / 365.25 AS INT) AS years\n    FROM employees e\n    JOIN departments d ON e.dept = d.name\n\'\'\')\n\n# Query the view like a table\nrows = run(\'SELECT * FROM emp_summary ORDER BY salary DESC\')\nprint(\"Employee summary (from view):\")\nfor r in rows: print(f\"  {r[1]} ({r[2]}): ${r[3]:,}, {r[4]:.2f}% of dept budget, {r[5]} yrs\")\n\n# View within query\nrows = run(\'\'\'\n    SELECT dept, COUNT(*) AS n, ROUND(AVG(salary), 0) AS avg_sal\n    FROM emp_summary\n    GROUP BY dept ORDER BY avg_sal DESC\n\'\'\')\nfor r in rows: print(f\"  {r[0]}: {r[1]} employees, avg ${r[2]:,}\")"},
        {"label": "View updates and DROP", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE products (id INT, name TEXT, price REAL, active INT DEFAULT 1)\'\'\')\nrunmany(\'INSERT INTO products VALUES (?,?,?,?)\', [\n    (1,\'Apple\',1.2,1),(2,\'Banana\',0.5,1),(3,\'Carrot\',0.8,0),(4,\'Date\',2.0,1),\n])\n\nrun(\'\'\'CREATE VIEW active_products AS\n       SELECT id, name, price FROM products WHERE active = 1\'\'\')\n\nrows = run(\'SELECT * FROM active_products\')\nprint(\"Active products:\", rows)\n\n# In SQLite, simple views can be updated using INSTEAD OF triggers\n# But directly: INSERT INTO simple single-table view may work\nrun(\"INSERT INTO active_products VALUES (5, \'Elderberry\', 3.5)\")\nrows = run(\'SELECT id, name, price, active FROM products WHERE id = 5\')\nprint(\"Inserted via view:\", rows)  # active defaults to 1\n\n# DROP VIEW\nrun(\'DROP VIEW active_products\')\nprint(\"View dropped. Tables unaffected.\")\nrows = run(\'SELECT COUNT(*) FROM products\')\nprint(\"Products table still has:\", rows[0][0], \"rows\")"},
        {"label": "Materialized views (via tables) and virtual tables", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\n# SQLite doesn\'t have native materialized views\n# Simulate with CREATE TABLE AS SELECT\nrun(\'\'\'CREATE TABLE employees (id INT, dept TEXT, salary REAL)\'\'\')\nrunmany(\'INSERT INTO employees VALUES (?,?,?)\', [\n    (i, [\'Eng\',\'Sales\',\'HR\'][i%3], 60000 + i*5000) for i in range(12)\n])\n\n# Simulated materialized view (refresh manually)\nrun(\'\'\'DROP TABLE IF EXISTS dept_stats_mv\'\'\')\nrun(\'\'\'\n    CREATE TABLE dept_stats_mv AS\n    SELECT dept,\n           COUNT(*) AS headcount,\n           ROUND(AVG(salary), 0) AS avg_salary,\n           MAX(salary) AS max_salary\n    FROM employees GROUP BY dept\n\'\'\')\n\nrows = run(\'SELECT * FROM dept_stats_mv ORDER BY avg_salary DESC\')\nprint(\"Materialized dept stats:\")\nfor r in rows: print(f\"  {r[0]}: {r[1]} people, avg ${r[2]:,}, max ${r[3]:,}\")\n\n# Refresh: insert more data, recreate\nrun(\'INSERT INTO employees VALUES (99, \"Eng\", 200000)\')\nrun(\'DROP TABLE dept_stats_mv\')\nrun(\'\'\'\n    CREATE TABLE dept_stats_mv AS\n    SELECT dept, COUNT(*) AS headcount, ROUND(AVG(salary),0) AS avg_salary\n    FROM employees GROUP BY dept\n\'\'\')\nrows = run(\'SELECT * FROM dept_stats_mv ORDER BY dept\')\nprint(\"Refreshed stats:\", rows)"}
    ],
    "rw": {
        "title": "Reporting View Layer",
        "scenario": "A BI team creates views for sales, customer, and product reporting so analysts never need to write complex JOINs — they just query well-named views.",
        "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE orders (id INT, cust_id INT, product_id INT, amount REAL, order_date TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE customers (id INT, name TEXT, tier TEXT, region TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE products (id INT, name TEXT, category TEXT, cost REAL)\'\'\')\nrunmany(\'INSERT INTO orders VALUES (?,?,?,?,?)\', [\n    (1,1,1,500,\'2024-01-10\'),(2,1,2,300,\'2024-01-15\'),(3,2,1,800,\'2024-02-05\'),\n    (4,2,3,200,\'2024-02-20\'),(5,3,2,600,\'2024-03-01\'),(6,1,3,400,\'2024-03-10\'),\n])\nrunmany(\'INSERT INTO customers VALUES (?,?,?,?)\', [\n    (1,\'Alice\',\'gold\',\'North\'),(2,\'Bob\',\'silver\',\'South\'),(3,\'Carol\',\'bronze\',\'East\'),\n])\nrunmany(\'INSERT INTO products VALUES (?,?,?,?)\', [\n    (1,\'Widget\',\'Hardware\',200),(2,\'Gadget\',\'Electronics\',100),(3,\'Gizmo\',\'Software\',50),\n])\n\nrun(\'\'\'CREATE VIEW order_detail AS\n    SELECT o.id AS order_id, c.name AS customer, c.tier, c.region,\n           p.name AS product, p.category,\n           o.amount, p.cost,\n           ROUND(o.amount - p.cost, 2) AS margin,\n           ROUND((o.amount - p.cost) / o.amount * 100, 1) AS margin_pct,\n           o.order_date\n    FROM orders o\n    JOIN customers c ON c.id = o.cust_id\n    JOIN products p ON p.id = o.product_id\n\'\'\')\n\nrows = run(\'SELECT customer, product, amount, margin_pct FROM order_detail ORDER BY margin_pct DESC\')\nprint(\"Order detail (from view):\")\nfor r in rows: print(f\"  {r[0]} - {r[1]}: ${r[2]} ({r[3]}% margin)\")\n\nrows = run(\'SELECT category, ROUND(AVG(margin_pct),1) AS avg_margin FROM order_detail GROUP BY category\')\nprint(\"Avg margin by category:\", rows)"
    },
    "practice": {
        "title": "View-Based Dashboard",
        "desc": "Create a sales table (id, rep, product, amount, region, sale_date). Create: (1) A view rep_dashboard with each rep\'s total, count, avg, and rank. (2) A view regional_summary with region totals and % of grand total. (3) A view top_products showing the top 5 products by revenue. Query each view to confirm it works.",
        "starter": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE sales (id INT, rep TEXT, product TEXT, amount REAL, region TEXT, sale_date TEXT)\'\'\')\nrunmany(\'INSERT INTO sales VALUES (?,?,?,?,?,?)\', [\n    (1,\'Alice\',\'Widget\',500,\'North\',\'2024-01-10\'),\n    (2,\'Alice\',\'Gadget\',300,\'North\',\'2024-01-15\'),\n    (3,\'Bob\',\'Widget\',800,\'South\',\'2024-02-01\'),\n    (4,\'Bob\',\'Gizmo\',200,\'South\',\'2024-02-10\'),\n    (5,\'Carol\',\'Gadget\',600,\'East\',\'2024-02-20\'),\n    (6,\'Alice\',\'Gizmo\',400,\'North\',\'2024-03-01\'),\n    (7,\'Carol\',\'Widget\',700,\'East\',\'2024-03-10\'),\n    (8,\'Bob\',\'Gadget\',350,\'South\',\'2024-03-15\'),\n])\n\n# 1. Rep dashboard view\nrun(\'\'\'CREATE VIEW rep_dashboard AS\n    SELECT rep, SUM(amount) AS total, COUNT(*) AS n_sales,\n           ROUND(AVG(amount),0) AS avg_sale,\n           RANK() OVER (ORDER BY SUM(amount) DESC) AS rank\n    FROM sales GROUP BY rep\n\'\'\')\nprint(\"=== Rep Dashboard ===\")\nfor r in run(\'SELECT * FROM rep_dashboard ORDER BY rank\'): print(f\"  {r}\")\n\n# 2. Regional summary view\nrun(\'\'\'CREATE VIEW regional_summary AS\n    SELECT region, ROUND(SUM(amount),0) AS total,\n           ROUND(100.0*SUM(amount)/SUM(SUM(amount)) OVER (), 1) AS pct_of_total\n    FROM sales GROUP BY region\n\'\'\')\nprint(\"=== Regional Summary ===\")\nfor r in run(\'SELECT * FROM regional_summary ORDER BY total DESC\'): print(f\"  {r}\")\n\n# 3. TODO: top products view\n"
    }
    },

    {
    "title": "24. Data Integrity & Constraints",
    "desc": "Constraints (PRIMARY KEY, UNIQUE, NOT NULL, CHECK, FOREIGN KEY) enforce data quality at the database level — the last line of defense against bad data.",
    "examples": [
        {"label": "PRIMARY KEY, UNIQUE, NOT NULL, CHECK", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nconn.execute(\'PRAGMA foreign_keys = ON\')\n\nrun(\'\'\'CREATE TABLE products (\n    id      INTEGER PRIMARY KEY AUTOINCREMENT,\n    sku     TEXT    NOT NULL UNIQUE,\n    name    TEXT    NOT NULL,\n    price   REAL    NOT NULL CHECK (price > 0),\n    stock   INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),\n    category TEXT   CHECK (category IN (\"food\", \"tech\", \"clothing\"))\n)\'\'\')\n\n# Valid insert\nrun(\"INSERT INTO products (sku, name, price, stock, category) VALUES (\'SKU-001\', \'Apple\', 1.5, 100, \'food\')\")\nrun(\"INSERT INTO products (sku, name, price, stock, category) VALUES (\'SKU-002\', \'Phone\', 699.0, 50, \'tech\')\")\nprint(\"Inserted valid products:\", run(\'SELECT id, sku, name, price FROM products\'))\n\n# Test constraint violations\nimport sqlite3 as _sqlite3\ntests = [\n    (\"Duplicate SKU\",       \"INSERT INTO products (sku, name, price) VALUES (\'SKU-001\', \'Pear\', 0.9)\"),\n    (\"Negative price\",      \"INSERT INTO products (sku, name, price) VALUES (\'SKU-003\', \'X\', -5.0)\"),\n    (\"Negative stock\",      \"INSERT INTO products (sku, name, price, stock) VALUES (\'SKU-004\', \'Y\', 1.0, -10)\"),\n    (\"Invalid category\",    \"INSERT INTO products (sku, name, price, category) VALUES (\'SKU-005\', \'Z\', 2.0, \'toys\')\"),\n    (\"NULL name\",           \"INSERT INTO products (sku, price) VALUES (\'SKU-006\', 3.0)\"),\n]\nfor label, sql in tests:\n    try:\n        run(sql)\n        print(f\"  FAIL: {label} should have been rejected!\")\n    except Exception as e:\n        print(f\"  OK: {label} rejected -> {str(e)[:50]}\")"},
        {"label": "FOREIGN KEY constraints", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nconn.execute(\'PRAGMA foreign_keys = ON\')\nrun(\'\'\'CREATE TABLE categories (id INT PRIMARY KEY, name TEXT NOT NULL UNIQUE)\'\'\')\nrun(\'\'\'CREATE TABLE products (\n    id INT PRIMARY KEY,\n    name TEXT NOT NULL,\n    cat_id INT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT ON UPDATE CASCADE\n)\'\'\')\nrun(\'\'\'CREATE TABLE orders (\n    id INT PRIMARY KEY,\n    product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE\n)\'\'\')\n\nrunmany(\'INSERT INTO categories VALUES (?,?)\', [(1,\'Food\'),(2,\'Tech\'),(3,\'Clothing\')])\nrunmany(\'INSERT INTO products VALUES (?,?,?)\', [(1,\'Apple\',1),(2,\'Phone\',2),(3,\'Shirt\',3)])\nrunmany(\'INSERT INTO orders VALUES (?,?)\', [(1,1),(2,1),(3,2)])\n\n# Violate FK\nimport sqlite3 as _sqlite3\ntry:\n    run(\'INSERT INTO products VALUES (4, \"Widget\", 99)\')   # cat_id=99 doesn\'t exist\n    print(\"FAIL: should have rejected\")\nexcept Exception as e:\n    print(\"OK: FK rejected:\", str(e)[:50])\n\n# ON DELETE CASCADE: delete product -> orders cascade deleted\nprint(\"Orders before:\", run(\'SELECT COUNT(*) FROM orders\')[0][0])\nrun(\'DELETE FROM products WHERE id = 1\')\nprint(\"Orders after deleting product 1:\", run(\'SELECT COUNT(*) FROM orders\')[0][0])\n\n# ON DELETE RESTRICT: cannot delete category if products reference it\ntry:\n    run(\'DELETE FROM categories WHERE id = 2\')\n    print(\"FAIL: should have rejected\")\nexcept Exception as e:\n    print(\"OK: RESTRICT works:\", str(e)[:50])"},
        {"label": "ON CONFLICT and UPSERT", "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nrun(\'\'\'CREATE TABLE inventory (\n    sku   TEXT PRIMARY KEY,\n    name  TEXT NOT NULL,\n    stock INT  NOT NULL DEFAULT 0 CHECK (stock >= 0)\n)\'\'\')\nrunmany(\'INSERT INTO inventory VALUES (?,?,?)\', [\n    (\'A001\',\'Apple\',100),(\'B002\',\'Banana\',200),\n])\n\n# ON CONFLICT IGNORE: skip duplicate inserts silently\nrun(\"INSERT OR IGNORE INTO inventory VALUES (\'A001\', \'Apple Updated\', 150)\")\nprint(\"After OR IGNORE:\", run(\"SELECT stock FROM inventory WHERE sku=\'A001\'\")[0][0])  # still 100\n\n# ON CONFLICT REPLACE: delete + re-insert\nrun(\"INSERT OR REPLACE INTO inventory VALUES (\'A001\', \'Apple Premium\', 120)\")\nprint(\"After OR REPLACE:\", run(\"SELECT name, stock FROM inventory WHERE sku=\'A001\'\")[0])\n\n# UPSERT (INSERT ... ON CONFLICT DO UPDATE) - SQLite 3.24+\nrun(\'\'\'\n    INSERT INTO inventory (sku, name, stock) VALUES (\"C003\", \"Cherry\", 50)\n    ON CONFLICT(sku) DO UPDATE SET\n        stock = stock + excluded.stock,\n        name  = excluded.name\n\'\'\')\nrun(\'\'\'\n    INSERT INTO inventory (sku, name, stock) VALUES (\"C003\", \"Cherry Deluxe\", 30)\n    ON CONFLICT(sku) DO UPDATE SET\n        stock = stock + excluded.stock,\n        name  = excluded.name\n\'\'\')\nprint(\"After UPSERT x2:\", run(\"SELECT name, stock FROM inventory WHERE sku=\'C003\'\")[0])"}
    ],
    "rw": {
        "title": "Inventory Management System",
        "scenario": "An e-commerce warehouse uses FK constraints, CHECK constraints, and UPSERT to maintain data integrity across products, stock levels, and order fulfillment.",
        "code": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nconn.execute(\'PRAGMA foreign_keys = ON\')\nrun(\'\'\'CREATE TABLE warehouses (id INT PRIMARY KEY, location TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE products (id INT PRIMARY KEY, sku TEXT UNIQUE NOT NULL,\n    name TEXT NOT NULL, price REAL CHECK (price > 0))\'\'\')\nrun(\'\'\'CREATE TABLE stock_levels (\n    product_id INT REFERENCES products(id) ON DELETE CASCADE,\n    warehouse_id INT REFERENCES warehouses(id),\n    qty INT NOT NULL DEFAULT 0 CHECK (qty >= 0),\n    PRIMARY KEY (product_id, warehouse_id)\n)\'\'\')\n\nrunmany(\'INSERT INTO warehouses VALUES (?,?)\', [(1,\'NYC\'),(2,\'LA\'),(3,\'Chicago\')])\nrunmany(\'INSERT INTO products VALUES (?,?,?,?)\',\n        [(1,\'SKU-A\',\'Widget\',29.99),(2,\'SKU-B\',\'Gadget\',49.99)])\nrunmany(\'INSERT INTO stock_levels VALUES (?,?,?)\',\n        [(1,1,500),(1,2,300),(2,1,200),(2,3,150)])\n\n# UPSERT stock: add received quantity\ndef receive_stock(product_id, warehouse_id, qty):\n    run(f\'\'\'\n        INSERT INTO stock_levels (product_id, warehouse_id, qty)\n        VALUES ({product_id}, {warehouse_id}, {qty})\n        ON CONFLICT (product_id, warehouse_id) DO UPDATE SET qty = qty + {qty}\n    \'\'\')\n\nreceive_stock(1, 1, 100)\nreceive_stock(2, 2, 50)  # new location\n\nrows = run(\'\'\'\n    SELECT p.name, w.location, sl.qty\n    FROM stock_levels sl\n    JOIN products p ON p.id = sl.product_id\n    JOIN warehouses w ON w.id = sl.warehouse_id\n    ORDER BY p.name, sl.qty DESC\n\'\'\')\nprint(\"Current stock:\")\nfor r in rows: print(f\"  {r[0]} @ {r[1]}: {r[2]} units\")"
    },
    "practice": {
        "title": "Bank Account Constraints",
        "desc": "Create an accounts table (id, holder, balance REAL CHECK >= 0, account_type CHECK IN list, opened_date). Create a transactions table (id, account_id FK, amount, type CHECK IN debit/credit, ts). Write: (1) Insert a debit that would go negative (should fail). (2) A trigger that auto-updates balance on transaction insert. (3) UPSERT to create or update account balance.",
        "starter": "import sqlite3, contextlib\nconn = sqlite3.connect(\':memory:\')\nconn.execute(\'PRAGMA journal_mode=WAL\')\ndef run(sql, params=()):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.execute(sql, params)\n        if cur.description:\n            return cur.fetchall()\n        conn.commit()\n        return cur.rowcount\ndef runmany(sql, rows):\n    with contextlib.closing(conn.cursor()) as cur:\n        cur.executemany(sql, rows)\n        conn.commit()\nconn.execute(\'PRAGMA foreign_keys = ON\')\nrun(\'\'\'CREATE TABLE accounts (\n    id INT PRIMARY KEY,\n    holder TEXT NOT NULL,\n    balance REAL NOT NULL DEFAULT 0 CHECK (balance >= 0),\n    account_type TEXT CHECK (account_type IN (\"checking\", \"savings\")),\n    opened_date TEXT DEFAULT (DATE(\"now\"))\n)\'\'\')\nrun(\'\'\'CREATE TABLE txns (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    account_id INT NOT NULL REFERENCES accounts(id),\n    amount REAL NOT NULL CHECK (amount > 0),\n    type TEXT NOT NULL CHECK (type IN (\"debit\",\"credit\")),\n    ts TEXT DEFAULT (DATETIME(\"now\"))\n)\'\'\')\n\nrun(\"INSERT INTO accounts VALUES (1,\'Alice\',1000,\'checking\',\'2024-01-01\')\")\n\n# 1. Try to go negative via debit > balance\nimport sqlite3 as _sqlite3\ntry:\n    run(\"INSERT INTO txns (account_id, amount, type) VALUES (1, 5000, \'debit\')\")\n    # Without trigger, balance isn\'t auto-updated. Add trigger below.\nexcept Exception as e:\n    print(\"Error:\", e)\n\n# 2. TODO: CREATE TRIGGER after_txn AFTER INSERT ON txns\n#    that updates accounts.balance = balance - amount WHERE type=\'debit\'\n#    or balance + amount WHERE type=\'credit\'\n\n# 3. TODO: UPSERT to create or update an account balance\nprint(\"Current balance:\", run(\"SELECT balance FROM accounts WHERE id=1\")[0][0])\n"
    }
    },

{
"title": "25. Advanced Aggregations",
"desc": "Use FILTER clauses for conditional aggregation, emulate ROLLUP with UNION ALL, and combine window functions for multi-dimensional analysis.",
"examples": [
        {"label": "FILTER clause – conditional sums per quarter", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS sales (\n    id INTEGER PRIMARY KEY,\n    region TEXT, product TEXT,\n    amount REAL, q INTEGER)\'\'\')\nrunmany(\'INSERT INTO sales VALUES (?,?,?,?,?)\', [\n    (1,\'North\',\'A\',100,1),(2,\'North\',\'B\',200,1),\n    (3,\'South\',\'A\',150,2),(4,\'South\',\'B\',250,2),\n    (5,\'North\',\'A\',120,3),(6,\'South\',\'B\',300,3)])\n# FILTER clause – conditional aggregation\nrows = run(\'\'\'\n    SELECT\n        region,\n        SUM(amount) AS total,\n        SUM(amount) FILTER(WHERE q=1) AS q1,\n        SUM(amount) FILTER(WHERE q=2) AS q2\n    FROM sales GROUP BY region\'\'\')\nprint(rows)\n"},
        {"label": "Emulate ROLLUP with UNION ALL", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS sales2 (\n    region TEXT, product TEXT, amount REAL)\'\'\')\nrunmany(\'INSERT INTO sales2 VALUES (?,?,?)\', [\n    (\'North\',\'A\',100),(\'North\',\'B\',200),\n    (\'South\',\'A\',150),(\'South\',\'B\',250)])\n# Emulate ROLLUP with UNION ALL\nrows = run(\'\'\'\n    SELECT region, product, SUM(amount)\n    FROM sales2 GROUP BY region, product\n    UNION ALL\n    SELECT region, NULL, SUM(amount)\n    FROM sales2 GROUP BY region\n    UNION ALL\n    SELECT NULL, NULL, SUM(amount) FROM sales2\n    ORDER BY 1,2\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "RANK and percent-rank", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS metrics (\n    dept TEXT, month INTEGER, revenue REAL)\'\'\')\nrunmany(\'INSERT INTO metrics VALUES (?,?,?)\', [\n    (\'Eng\',1,5000),(\'Eng\',2,6000),(\'HR\',1,2000),(\'HR\',2,2500)])\n# PERCENT_RANK and CUME_DIST\nrows = run(\'\'\'\n    SELECT dept, month, revenue,\n        RANK() OVER (ORDER BY revenue) AS rnk,\n        ROUND(100.0*RANK() OVER(ORDER BY revenue)/COUNT(*) OVER(),1) AS pct\n    FROM metrics ORDER BY revenue\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "Multi-dimensional conditional aggregation", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS orders (\n    id INTEGER PRIMARY KEY, customer TEXT,\n    status TEXT, amount REAL)\'\'\')\nrunmany(\'INSERT INTO orders VALUES (?,?,?,?)\', [\n    (1,\'Alice\',\'paid\',300),(2,\'Bob\',\'pending\',150),\n    (3,\'Alice\',\'paid\',200),(4,\'Bob\',\'paid\',400),(5,\'Carol\',\'refunded\',100)])\n# Multi-dimensional conditional aggregation\nrows = run(\'\'\'\n    SELECT customer,\n        COUNT(*) FILTER(WHERE status=\'paid\') AS paid_cnt,\n        SUM(amount) FILTER(WHERE status=\'paid\') AS paid_sum,\n        COUNT(*) FILTER(WHERE status=\'pending\') AS pend_cnt\n    FROM orders GROUP BY customer ORDER BY customer\'\'\')\nfor r in rows: print(r)\n"}
    ],
"rw": {
    "title": "E-commerce Revenue Breakdown",
    "scenario": "An analytics team needs quarterly revenue by region, total rows, and a grand-total rollup — all in one query.",
    "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS rev (\n    region TEXT, q INTEGER, amount REAL)\'\'\')\nrunmany(\'INSERT INTO rev VALUES (?,?,?)\', [\n    (\'North\',1,500),(\'North\',2,700),\n    (\'South\',1,400),(\'South\',2,600)])\nrows = run(\'\'\'\n    SELECT region, q,\n        SUM(amount) AS total,\n        SUM(amount) FILTER(WHERE q=1) AS q1_total\n    FROM rev GROUP BY region, q\n    UNION ALL\n    SELECT NULL, NULL, SUM(amount), NULL FROM rev\'\'\')\nfor r in rows: print(r)\n"
},
"practice": {
    "title": "Conditional Aggregation Practice",
    "desc": "Create a \'transactions\' table with columns (id, type TEXT, amount REAL). Write a query that returns total amount where type=\'credit\', total where type=\'debit\', and the net difference — all in one row.",
    "starter": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS transactions (\n    id INTEGER PRIMARY KEY, type TEXT, amount REAL)\'\'\')\nrunmany(\'INSERT INTO transactions VALUES (?,?,?)\', [\n    (1,\'credit\',500),(2,\'debit\',200),(3,\'credit\',300),(4,\'debit\',150)])\n# Write your FILTER aggregation query here\n"
}
},

{
"title": "26. Self-Joins & Non-Equi Joins",
"desc": "Use self-joins to query hierarchical data, non-equi joins for range matching, and interval joins to detect overlaps.",
"examples": [
        {"label": "Self-join: employee-manager hierarchy", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS employees (\n    id INTEGER PRIMARY KEY, name TEXT,\n    manager_id INTEGER, salary REAL)\'\'\')\nrunmany(\'INSERT INTO employees VALUES (?,?,?,?)\', [\n    (1,\'Alice\',None,9000),(2,\'Bob\',1,7000),\n    (3,\'Carol\',1,7500),(4,\'Dave\',2,5000),(5,\'Eve\',2,5500)])\n# Self-join: each employee with their manager\'s name\nrows = run(\'\'\'\n    SELECT e.name AS employee, m.name AS manager\n    FROM employees e\n    LEFT JOIN employees m ON e.manager_id = m.id\n    ORDER BY e.id\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "Non-equi join: salary comparisons within dept", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS employees2 (\n    id INTEGER PRIMARY KEY, name TEXT, salary REAL, dept TEXT)\'\'\')\nrunmany(\'INSERT INTO employees2 VALUES (?,?,?,?)\', [\n    (1,\'Alice\',9000,\'Eng\'),(2,\'Bob\',7000,\'Eng\'),\n    (3,\'Carol\',7500,\'HR\'),(4,\'Dave\',5000,\'HR\')])\n# Non-equi join: employees earning more than others in same dept\nrows = run(\'\'\'\n    SELECT a.name AS higher, b.name AS lower,\n           a.salary - b.salary AS diff\n    FROM employees2 a\n    JOIN employees2 b\n      ON a.dept = b.dept AND a.salary > b.salary\n    ORDER BY diff DESC\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "Range join: match orders to price bands", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS prices (\n    product TEXT, price REAL, valid_from TEXT, valid_to TEXT)\'\'\')\nrunmany(\'INSERT INTO prices VALUES (?,?,?,?)\', [\n    (\'Widget\',10.0,\'2024-01-01\',\'2024-03-31\'),\n    (\'Widget\',12.0,\'2024-04-01\',\'2024-12-31\'),\n    (\'Gadget\',25.0,\'2024-01-01\',\'2024-12-31\')])\nrun(\'\'\'CREATE TABLE IF NOT EXISTS orders3 (\n    id INTEGER, product TEXT, order_date TEXT, qty INTEGER)\'\'\')\nrunmany(\'INSERT INTO orders3 VALUES (?,?,?,?)\', [\n    (1,\'Widget\',\'2024-02-15\',3),(2,\'Widget\',\'2024-05-20\',5),(3,\'Gadget\',\'2024-03-10\',2)])\n# Range join: match orders to the correct price band\nrows = run(\'\'\'\n    SELECT o.id, o.product, o.order_date, p.price, o.qty*p.price AS total\n    FROM orders3 o\n    JOIN prices p\n      ON o.product=p.product\n     AND o.order_date BETWEEN p.valid_from AND p.valid_to\n    ORDER BY o.id\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "Interval join: detect overlapping tasks", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS tasks (\n    id INTEGER PRIMARY KEY, name TEXT,\n    start TEXT, end TEXT)\'\'\')\nrunmany(\'INSERT INTO tasks VALUES (?,?,?,?)\', [\n    (1,\'Deploy\',\'2024-01-10\',\'2024-01-15\'),\n    (2,\'Test\',\'2024-01-12\',\'2024-01-18\'),\n    (3,\'Review\',\'2024-01-20\',\'2024-01-25\'),\n    (4,\'Release\',\'2024-01-16\',\'2024-01-22\')])\n# Find overlapping task pairs\nrows = run(\'\'\'\n    SELECT a.name AS task1, b.name AS task2\n    FROM tasks a JOIN tasks b\n      ON a.id < b.id\n     AND a.start <= b.end\n     AND a.end >= b.start\n    ORDER BY a.id\'\'\')\nfor r in rows: print(r)\n"}
    ],
"rw": {
    "title": "Org-Chart & Salary Reporting",
    "scenario": "HR needs a report showing each employee, their direct manager, and whether they earn more than the average of their peer group.",
    "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS staff (\n    id INTEGER PRIMARY KEY, name TEXT,\n    manager_id INTEGER, salary REAL, dept TEXT)\'\'\')\nrunmany(\'INSERT INTO staff VALUES (?,?,?,?,?)\', [\n    (1,\'CEO\',None,15000,\'Exec\'),(2,\'CTO\',1,12000,\'Eng\'),\n    (3,\'Dev1\',2,8000,\'Eng\'),(4,\'Dev2\',2,7500,\'Eng\'),(5,\'CHRO\',1,11000,\'HR\')])\nrows = run(\'\'\'\n    SELECT e.name, m.name AS mgr,\n        e.salary,\n        AVG(p.salary) OVER(PARTITION BY e.manager_id) AS peer_avg\n    FROM staff e\n    LEFT JOIN staff m ON e.manager_id=m.id\n    ORDER BY e.id\'\'\')\nfor r in rows: print(r)\n"
},
"practice": {
    "title": "Self-Join Practice",
    "desc": "Using the \'staff\' table above, find all pairs of employees in the same department where one earns at least 20% more than the other.",
    "starter": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS staff (\n    id INTEGER PRIMARY KEY, name TEXT,\n    dept TEXT, salary REAL)\'\'\')\nrunmany(\'INSERT INTO staff VALUES (?,?,?,?)\', [\n    (1,\'Alice\',\'Eng\',9000),(2,\'Bob\',\'Eng\',7000),\n    (3,\'Carol\',\'HR\',8000),(4,\'Dave\',\'HR\',6000)])\n# Write a non-equi self-join here\n"
}
},

{
"title": "27. Analytical Functions Advanced",
"desc": "Go beyond basic ranking: use LAG/LEAD for period comparisons, NTILE for bucketing, FIRST_VALUE/LAST_VALUE for partition anchors, and rolling window frames.",
"examples": [
        {"label": "LAG: daily price change", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS stock (\n    dt TEXT, ticker TEXT, close REAL)\'\'\')\nrunmany(\'INSERT INTO stock VALUES (?,?,?)\', [\n    (\'2024-01-01\',\'AAPL\',185.0),(\'2024-01-02\',\'AAPL\',186.5),\n    (\'2024-01-03\',\'AAPL\',184.0),(\'2024-01-04\',\'AAPL\',188.0),\n    (\'2024-01-05\',\'AAPL\',190.0)])\n# Daily return using LAG\nrows = run(\'\'\'\n    SELECT dt, close,\n        LAG(close) OVER(ORDER BY dt) AS prev,\n        ROUND(close - LAG(close) OVER(ORDER BY dt), 2) AS change\n    FROM stock ORDER BY dt\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "LEAD & rolling 3-period average", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS sales3 (\n    month INTEGER, revenue REAL)\'\'\')\nrunmany(\'INSERT INTO sales3 VALUES (?,?)\', [\n    (1,5000),(2,5500),(3,4800),(4,6200),(5,6800),(6,7100)])\n# Compare to next month with LEAD; running avg\nrows = run(\'\'\'\n    SELECT month, revenue,\n        LEAD(revenue) OVER(ORDER BY month) AS next_month,\n        ROUND(AVG(revenue) OVER(\n            ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) AS rolling3\n    FROM sales3\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "NTILE: quartile bucketing", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS scores (\n    student TEXT, score INTEGER)\'\'\')\nrunmany(\'INSERT INTO scores VALUES (?,?)\', [\n    (\'Alice\',92),(\'Bob\',75),(\'Carol\',88),\n    (\'Dave\',60),(\'Eve\',95),(\'Frank\',70)])\n# NTILE: split into quartiles\nrows = run(\'\'\'\n    SELECT student, score,\n        NTILE(4) OVER(ORDER BY score) AS quartile\n    FROM scores ORDER BY score\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "FIRST_VALUE & MAX per partition", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS temps (\n    city TEXT, day INTEGER, temp REAL)\'\'\')\nrunmany(\'INSERT INTO temps VALUES (?,?,?)\', [\n    (\'NYC\',1,5.0),(\'NYC\',2,7.0),(\'NYC\',3,4.0),\n    (\'LA\',1,20.0),(\'LA\',2,22.0),(\'LA\',3,19.0)])\n# FIRST_VALUE and LAST_VALUE per city\nrows = run(\'\'\'\n    SELECT city, day, temp,\n        FIRST_VALUE(temp) OVER(PARTITION BY city ORDER BY day) AS first_t,\n        MAX(temp) OVER(PARTITION BY city) AS peak\n    FROM temps ORDER BY city, day\'\'\')\nfor r in rows: print(r)\n"}
    ],
"rw": {
    "title": "Sales Trend Analysis",
    "scenario": "A business analyst wants to see month-over-month revenue change, the next month forecast gap, and each month\'s performance bucket (top 25%, etc.).",
    "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS monthly (\n    month INTEGER, revenue REAL)\'\'\')\nrunmany(\'INSERT INTO monthly VALUES (?,?)\', [\n    (1,4000),(2,4500),(3,4200),(4,5000),(5,5500),(6,6000)])\nrows = run(\'\'\'\n    SELECT month, revenue,\n        LAG(revenue) OVER(ORDER BY month) AS prev,\n        ROUND(revenue - LAG(revenue) OVER(ORDER BY month),2) AS mom_change,\n        NTILE(3) OVER(ORDER BY revenue) AS tier\n    FROM monthly\'\'\')\nfor r in rows: print(r)\n"
},
"practice": {
    "title": "Window Function Practice",
    "desc": "Using a \'visits\' table with columns (user_id, visit_date TEXT, pages_viewed INTEGER), compute for each user: their previous visit date, the gap in days between visits, and their max pages_viewed.",
    "starter": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS visits (\n    user_id INTEGER, visit_date TEXT, pages_viewed INTEGER)\'\'\')\nrunmany(\'INSERT INTO visits VALUES (?,?,?)\', [\n    (1,\'2024-01-01\',5),(1,\'2024-01-05\',8),(1,\'2024-01-12\',3),\n    (2,\'2024-01-02\',10),(2,\'2024-01-10\',7)])\n# Write LAG and MAX window functions here\n"
}
},

{
"title": "28. Database Design & Normalization",
"desc": "Apply 1NF, 2NF, and 3NF to eliminate redundancy, design proper primary and foreign keys, and inspect schemas with SQLite system tables.",
"examples": [
        {"label": "1NF: atomic values and separate phone table", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\n# 1NF: atomic values, no repeating groups\nrun(\'\'\'CREATE TABLE IF NOT EXISTS contacts (\n    id INTEGER PRIMARY KEY,\n    name TEXT NOT NULL,\n    email TEXT NOT NULL)\'\'\')\nrun(\'\'\'CREATE TABLE IF NOT EXISTS contact_phones (\n    contact_id INTEGER,\n    phone TEXT NOT NULL,\n    FOREIGN KEY(contact_id) REFERENCES contacts(id))\'\'\')\nrunmany(\'INSERT INTO contacts VALUES (?,?,?)\', [\n    (1,\'Alice\',\'alice@ex.com\'),(2,\'Bob\',\'bob@ex.com\')])\nrunmany(\'INSERT INTO contact_phones VALUES (?,?)\', [\n    (1,\'555-0001\'),(1,\'555-0002\'),(2,\'555-0003\')])\nprint(run(\'SELECT * FROM contacts\'))\nprint(run(\'SELECT * FROM contact_phones\'))\n"},
        {"label": "2NF: remove partial dependency with products table", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\n# 2NF: remove partial dependencies (composite key fix)\nrun(\'\'\'CREATE TABLE IF NOT EXISTS products (\n    product_id INTEGER PRIMARY KEY,\n    product_name TEXT NOT NULL,\n    price REAL NOT NULL)\'\'\')\nrun(\'\'\'CREATE TABLE IF NOT EXISTS order_items (\n    order_id INTEGER,\n    product_id INTEGER,\n    qty INTEGER NOT NULL,\n    PRIMARY KEY(order_id, product_id),\n    FOREIGN KEY(product_id) REFERENCES products(product_id))\'\'\')\nrunmany(\'INSERT INTO products VALUES (?,?,?)\', [\n    (10,\'Widget\',9.99),(11,\'Gadget\',24.99)])\nrunmany(\'INSERT INTO order_items VALUES (?,?,?)\', [\n    (1,10,3),(1,11,1),(2,10,5)])\nrows = run(\'\'\'\n    SELECT oi.order_id, p.product_name, oi.qty, p.price*oi.qty AS subtotal\n    FROM order_items oi JOIN products p ON oi.product_id=p.product_id\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "3NF: move location to departments table", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\n# 3NF: remove transitive dependencies\nrun(\'\'\'CREATE TABLE IF NOT EXISTS departments (\n    dept_id INTEGER PRIMARY KEY, dept_name TEXT, location TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE IF NOT EXISTS staff2 (\n    id INTEGER PRIMARY KEY, name TEXT,\n    dept_id INTEGER,\n    FOREIGN KEY(dept_id) REFERENCES departments(dept_id))\'\'\')\nrunmany(\'INSERT INTO departments VALUES (?,?,?)\', [\n    (1,\'Engineering\',\'Floor 3\'),(2,\'HR\',\'Floor 1\')])\nrunmany(\'INSERT INTO staff2 VALUES (?,?,?)\', [\n    (1,\'Alice\',1),(2,\'Bob\',1),(3,\'Carol\',2)])\nrows = run(\'\'\'\n    SELECT s.name, d.dept_name, d.location\n    FROM staff2 s JOIN departments d ON s.dept_id=d.dept_id\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "Schema inspection with PRAGMA and sqlite_master", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\n# Schema inspection and FK checks\nrun(\'\'\'CREATE TABLE IF NOT EXISTS parent (id INTEGER PRIMARY KEY, val TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE IF NOT EXISTS child (\n    id INTEGER PRIMARY KEY,\n    parent_id INTEGER,\n    FOREIGN KEY(parent_id) REFERENCES parent(id))\'\'\')\nrun(\'\'\'PRAGMA foreign_keys=ON\'\'\')\nrunmany(\'INSERT INTO parent VALUES (?,?)\', [(1,\'A\'),(2,\'B\')])\nrunmany(\'INSERT INTO child VALUES (?,?)\', [(10,1),(11,2)])\n# List tables and schema\ntables = run(\"SELECT name FROM sqlite_master WHERE type=\'table\'\")\nprint(\'Tables:\', tables)\nschema = run(\"SELECT sql FROM sqlite_master WHERE name=\'child\'\")\nprint(schema[0][0])\n"}
    ],
"rw": {
    "title": "Customer Orders Schema",
    "scenario": "Design a normalized schema for customers, orders, and products. Ensure no partial or transitive dependencies, then write a JOIN query to get order summaries.",
    "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS customers (\n    id INTEGER PRIMARY KEY, name TEXT, email TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE IF NOT EXISTS products2 (\n    id INTEGER PRIMARY KEY, name TEXT, price REAL)\'\'\')\nrun(\'\'\'CREATE TABLE IF NOT EXISTS orders2 (\n    id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE IF NOT EXISTS order_lines (\n    order_id INTEGER, product_id INTEGER, qty INTEGER,\n    PRIMARY KEY(order_id, product_id))\'\'\')\nrunmany(\'INSERT INTO customers VALUES (?,?,?)\', [(1,\'Alice\',\'a@ex.com\')])\nrunmany(\'INSERT INTO products2 VALUES (?,?,?)\', [(1,\'Widget\',10.0)])\nrunmany(\'INSERT INTO orders2 VALUES (?,?,?)\', [(1,1,\'2024-01-15\')])\nrunmany(\'INSERT INTO order_lines VALUES (?,?,?)\', [(1,1,3)])\nrows = run(\'\'\'\n    SELECT c.name, o.order_date, p.name, ol.qty, p.price*ol.qty AS total\n    FROM orders2 o\n    JOIN customers c ON o.customer_id=c.id\n    JOIN order_lines ol ON ol.order_id=o.id\n    JOIN products2 p ON p.id=ol.product_id\'\'\')\nfor r in rows: print(r)\n"
},
"practice": {
    "title": "Normalization Practice",
    "desc": "You have a denormalized table: orders_flat(order_id, customer_name, customer_email, product_name, price, qty). Identify the normal form violations and write CREATE TABLE statements for a 3NF schema.",
    "starter": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\n# Denormalized (bad):\n# orders_flat: order_id, customer_name, customer_email, product_name, price, qty\n# Violates 2NF (price depends only on product) and 3NF if email depends on name.\n# Write your normalized CREATE TABLE statements here:\n\n# run(\'\'\'CREATE TABLE customers ...\'\'\')\n# run(\'\'\'CREATE TABLE products ...\'\'\')\n# run(\'\'\'CREATE TABLE orders ...\'\'\')\n# run(\'\'\'CREATE TABLE order_items ...\'\'\')\n"
}
},

{
"title": "29. JSON in SQL",
"desc": "Store, extract, modify, and filter JSON data in SQLite using json_extract, json_set, json_insert, and json_remove.",
"examples": [
        {"label": "json_extract: read top-level fields", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nimport json\nrun(\'\'\'CREATE TABLE IF NOT EXISTS events (\n    id INTEGER PRIMARY KEY,\n    payload TEXT)\'\'\')  -- stored as JSON text\ndata = [\n    (1, json.dumps({\'user\':\'alice\',\'action\':\'login\',\'meta\':{\'ip\':\'1.2.3.4\'}})),\n    (2, json.dumps({\'user\':\'bob\',\'action\':\'purchase\',\'meta\':{\'items\':3,\'total\':59.99}})),\n    (3, json.dumps({\'user\':\'alice\',\'action\':\'logout\',\'meta\':{\'ip\':\'1.2.3.4\'}})),\n]\nrunmany(\'INSERT INTO events VALUES (?,?)\', data)\n# Extract top-level field with json_extract\nrows = run(\"SELECT id, json_extract(payload,\'$.user\'), json_extract(payload,\'$.action\') FROM events\")\nfor r in rows: print(r)\n"},
        {"label": "Nested and array element access", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nimport json\nrun(\'\'\'CREATE TABLE IF NOT EXISTS events2 (id INTEGER PRIMARY KEY, payload TEXT)\'\'\')\nrunmany(\'INSERT INTO events2 VALUES (?,?)\', [\n    (1, json.dumps({\'user\':\'alice\',\'tags\':[\'sql\',\'python\'],\'score\':95})),\n    (2, json.dumps({\'user\':\'bob\',\'tags\':[\'ml\',\'python\'],\'score\':80})),\n])\n# Access nested and array elements\nrows = run(\'\'\'\n    SELECT id,\n        json_extract(payload, \'$.user\') AS user,\n        json_extract(payload, \'$.score\') AS score,\n        json_extract(payload, \'$.tags[0]\') AS first_tag\n    FROM events2\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "Modify JSON with json_set and json_insert", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nimport json\nrun(\'\'\'CREATE TABLE IF NOT EXISTS configs (\n    id INTEGER PRIMARY KEY, settings TEXT)\'\'\')\nrun(\'\'\'INSERT INTO configs VALUES (1, ?)\'\'\',\n    (json.dumps({\'theme\':\'dark\',\'lang\':\'en\',\'max_rows\':100}),))\n# Modify JSON with json_set, json_insert, json_remove\nrun(\'\'\'UPDATE configs SET settings = json_set(settings, \'$.theme\', \'light\') WHERE id=1\'\'\')\nrun(\'\'\'UPDATE configs SET settings = json_set(settings, \'$.debug\', 1) WHERE id=1\'\'\')\nrow = run(\'SELECT settings FROM configs WHERE id=1\')\nprint(json.loads(row[0][0]))\n"},
        {"label": "Filter rows by JSON field values", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nimport json\nrun(\'\'\'CREATE TABLE IF NOT EXISTS products3 (\n    id INTEGER PRIMARY KEY, name TEXT, attributes TEXT)\'\'\')\nrunmany(\'INSERT INTO products3 VALUES (?,?,?)\', [\n    (1,\'Widget\', json.dumps({\'color\':\'red\',\'weight\':0.5,\'tags\':[\'sale\',\'new\']})),\n    (2,\'Gadget\', json.dumps({\'color\':\'blue\',\'weight\':1.2,\'tags\':[\'new\']})),\n    (3,\'Doohickey\', json.dumps({\'color\':\'red\',\'weight\':0.3,\'tags\':[\'sale\']})),\n])\n# Filter on JSON field and aggregate\nrows = run(\'\'\'\n    SELECT name,\n        json_extract(attributes,\'$.color\') AS color,\n        json_extract(attributes,\'$.weight\') AS weight\n    FROM products3\n    WHERE json_extract(attributes,\'$.color\')=\'red\'\n    ORDER BY weight\'\'\')\nfor r in rows: print(r)\n"}
    ],
"rw": {
    "title": "User Event Logging",
    "scenario": "An app stores user events as JSON blobs. Query to find all purchase events, extract the total amount, and rank users by spend.",
    "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nimport json\nrun(\'\'\'CREATE TABLE IF NOT EXISTS user_events (\n    id INTEGER PRIMARY KEY, payload TEXT)\'\'\')\nrunmany(\'INSERT INTO user_events VALUES (?,?)\', [\n    (1,json.dumps({\'user\':\'alice\',\'action\':\'purchase\',\'amount\':49.99})),\n    (2,json.dumps({\'user\':\'bob\',\'action\':\'view\',\'amount\':0})),\n    (3,json.dumps({\'user\':\'alice\',\'action\':\'purchase\',\'amount\':29.99})),\n    (4,json.dumps({\'user\':\'carol\',\'action\':\'purchase\',\'amount\':99.99})),\n])\nrows = run(\'\'\'\n    SELECT\n        json_extract(payload,\'$.user\') AS user,\n        SUM(CAST(json_extract(payload,\'$.amount\') AS REAL)) AS total_spend\n    FROM user_events\n    WHERE json_extract(payload,\'$.action\')=\'purchase\'\n    GROUP BY user ORDER BY total_spend DESC\'\'\')\nfor r in rows: print(r)\n"
},
"practice": {
    "title": "JSON Querying Practice",
    "desc": "Create a \'logs\' table with an id and a \'data\' JSON column. Insert 3 log entries with fields: level (INFO/ERROR), message, and timestamp. Write a query to show only ERROR logs with their message and timestamp.",
    "starter": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nimport json\nrun(\'\'\'CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, data TEXT)\'\'\')\nrunmany(\'INSERT INTO logs VALUES (?,?)\', [\n    (1,json.dumps({\'level\':\'INFO\',\'message\':\'Started\',\'timestamp\':\'2024-01-01T09:00:00\'})),\n    (2,json.dumps({\'level\':\'ERROR\',\'message\':\'Null ref\',\'timestamp\':\'2024-01-01T09:05:00\'})),\n    (3,json.dumps({\'level\':\'ERROR\',\'message\':\'Timeout\',\'timestamp\':\'2024-01-01T09:10:00\'})),\n])\n# Write your json_extract filter query here\n"
}
},

{
"title": "30. Full-Text Search",
"desc": "Use SQLite\'s FTS5 virtual tables to perform keyword search, phrase matching, boolean operators, column-specific search, and ranked results with snippets.",
"examples": [
        {"label": "Create FTS5 table and basic MATCH search", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\n# FTS5 virtual table for full-text search\nrun(\'\'\'CREATE VIRTUAL TABLE IF NOT EXISTS articles\n    USING fts5(title, body, tokenize=\'porter ascii\')\'\'\')\nrunmany(\'INSERT INTO articles VALUES (?,?)\', [\n    (\'SQL Basics\',\'Learn the fundamentals of SQL queries and databases\'),\n    (\'Python for Data\',\'Python is great for data analysis and machine learning\'),\n    (\'Advanced SQL\',\'Window functions and CTEs are powerful SQL features\'),\n    (\'NumPy Guide\',\'NumPy provides fast array operations for numerical data\'),\n])\n# Simple search\nrows = run(\"SELECT title FROM articles WHERE articles MATCH \'SQL\'\")\nfor r in rows: print(r)\n"},
        {"label": "Column-specific search and ranked results", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE VIRTUAL TABLE IF NOT EXISTS docs\n    USING fts5(title, content)\'\'\')\nrunmany(\'INSERT INTO docs VALUES (?,?)\', [\n    (\'Intro to ML\',\'Machine learning uses statistical models to make predictions\'),\n    (\'Deep Learning\',\'Neural networks form the basis of deep learning systems\'),\n    (\'SQL Mastery\',\'Master SQL with window functions and query optimization\'),\n    (\'Data Wrangling\',\'Pandas and NumPy help with data cleaning and transformation\'),\n])\n# Phrase search and column filter\nrows = run(\"SELECT title FROM docs WHERE docs MATCH \'title:SQL\'\")\nprint(\'Title match:\', rows)\nrows = run(\"SELECT title, rank FROM docs WHERE docs MATCH \'data\' ORDER BY rank\")\nfor r in rows: print(r)\n"},
        {"label": "Prefix search and AND/OR boolean operators", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE VIRTUAL TABLE IF NOT EXISTS notes\n    USING fts5(author, text)\'\'\')\nrunmany(\'INSERT INTO notes VALUES (?,?)\', [\n    (\'Alice\',\'Python decorators and closures are advanced features\'),\n    (\'Bob\',\'SQL joins and subqueries are essential for data analysis\'),\n    (\'Alice\',\'NumPy broadcasting makes array operations concise\'),\n    (\'Bob\',\'Window functions in SQL enable running totals and rankings\'),\n])\n# Prefix search and boolean operators\nrows = run(\"SELECT author, text FROM notes WHERE notes MATCH \'SQL AND data\'\")\nprint(\'AND:\', rows)\nrows = run(\"SELECT author, text FROM notes WHERE notes MATCH \'Python OR NumPy\'\")\nprint(\'OR:\', [r[0] for r in rows])\n"},
        {"label": "Snippet extraction with highlighting", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE VIRTUAL TABLE IF NOT EXISTS kb\n    USING fts5(title, body)\'\'\')\nrunmany(\'INSERT INTO kb VALUES (?,?)\', [\n    (\'Error Handling\',\'Use try-except blocks to catch and handle Python exceptions gracefully\'),\n    (\'Logging Best Practices\',\'Configure logging with handlers, formatters and log levels\'),\n    (\'Testing Strategies\',\'Unit tests and integration tests ensure code reliability\'),\n    (\'Code Review Tips\',\'Peer code review improves code quality and knowledge sharing\'),\n])\n# Snippet and highlight\nrows = run(\'\'\'\n    SELECT title, snippet(kb, 1, \'<b>\', \'</b>\', \'...\', 8)\n    FROM kb WHERE kb MATCH \'code\'\n    ORDER BY rank\'\'\')\nfor r in rows: print(r[0], \'|\', r[1])\n"}
    ],
"rw": {
    "title": "Knowledge Base Search",
    "scenario": "A support team has a knowledge base table. Implement full-text search that returns articles matching a query, ranked by relevance, with a highlighted snippet.",
    "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE VIRTUAL TABLE IF NOT EXISTS support_kb\n    USING fts5(title, content, tokenize=\'porter ascii\')\'\'\')\nrunmany(\'INSERT INTO support_kb VALUES (?,?)\', [\n    (\'Password Reset\',\'To reset your password go to settings and click reset\'),\n    (\'Billing FAQ\',\'For billing questions contact support or view your invoice\'),\n    (\'Account Setup\',\'Set up your account by verifying your email address\'),\n    (\'Password Policy\',\'Passwords must be 8 characters with a mix of letters and numbers\'),\n])\nquery = \'password\'\nrows = run(f\'\'\'\n    SELECT title,\n        snippet(support_kb, 1, \'**\', \'**\', \'...\', 6) AS preview,\n        rank\n    FROM support_kb\n    WHERE support_kb MATCH ?\n    ORDER BY rank\n\'\'\', (query,))\nfor r in rows: print(r[0], \'|\', r[1])\n"
},
"practice": {
    "title": "FTS5 Practice",
    "desc": "Create an FTS5 table called \'recipes\' with columns (name, ingredients, instructions). Insert 4 recipes. Write a query to find all recipes where the ingredients contain \'garlic\' AND instructions contain \'stir\'.",
    "starter": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE VIRTUAL TABLE IF NOT EXISTS recipes\n    USING fts5(name, ingredients, instructions)\'\'\')\nrunmany(\'INSERT INTO recipes VALUES (?,?,?)\', [\n    (\'Pasta\',\'flour eggs garlic olive oil\',\'stir pasta in boiling water\'),\n    (\'Soup\',\'carrots garlic onion broth\',\'simmer and stir until soft\'),\n    (\'Salad\',\'lettuce tomato cucumber\',\'toss with dressing\'),\n    (\'Stir Fry\',\'garlic ginger soy sauce vegetables\',\'stir fry on high heat\'),\n])\n# Write your FTS5 AND query here\n"
}
},

{
"title": "31. Performance Tuning & EXPLAIN",
"desc": "Use EXPLAIN QUERY PLAN to understand query execution, create regular, composite, covering, and partial indexes, and run ANALYZE to update planner statistics.",
"examples": [
        {"label": "Index impact benchmark: with vs without", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nimport time\nrun(\'\'\'CREATE TABLE IF NOT EXISTS big (\n    id INTEGER PRIMARY KEY, val INTEGER, cat TEXT)\'\'\')\n# Insert sample data\nimport random; random.seed(42)\nrows = [(i, random.randint(1,1000), random.choice([\'A\',\'B\',\'C\'])) for i in range(1,5001)]\nrunmany(\'INSERT INTO big VALUES (?,?,?)\', rows)\n# Query without index\nt0 = time.perf_counter()\nrun(\'SELECT COUNT(*) FROM big WHERE val > 500\')\nt1 = time.perf_counter()\n# Add index\nrun(\'CREATE INDEX IF NOT EXISTS idx_val ON big(val)\')\nt2 = time.perf_counter()\nrun(\'SELECT COUNT(*) FROM big WHERE val > 500\')\nt3 = time.perf_counter()\nprint(f\'Without index: {(t1-t0)*1000:.2f}ms\')\nprint(f\'With index:    {(t3-t2)*1000:.2f}ms\')\n"},
        {"label": "EXPLAIN QUERY PLAN before and after composite index", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS orders4 (\n    id INTEGER PRIMARY KEY, customer_id INTEGER,\n    status TEXT, amount REAL)\'\'\')\nimport random; random.seed(0)\nrows = [(i, random.randint(1,100), random.choice([\'new\',\'paid\',\'shipped\']),\n         round(random.uniform(10,500),2)) for i in range(1,2001)]\nrunmany(\'INSERT INTO orders4 VALUES (?,?,?,?)\', rows)\n# EXPLAIN QUERY PLAN\nplan = run(\'\'\'EXPLAIN QUERY PLAN\n    SELECT customer_id, SUM(amount)\n    FROM orders4\n    WHERE status=\'paid\'\n    GROUP BY customer_id\'\'\')\nfor p in plan: print(p)\n# Add composite index\nrun(\'CREATE INDEX IF NOT EXISTS idx_status_cust ON orders4(status, customer_id)\')\nplan2 = run(\'\'\'EXPLAIN QUERY PLAN\n    SELECT customer_id, SUM(amount)\n    FROM orders4 WHERE status=\'paid\'\n    GROUP BY customer_id\'\'\')\nfor p in plan2: print(p)\n"},
        {"label": "Covering index to avoid table scans", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS logs2 (\n    id INTEGER PRIMARY KEY,\n    user_id INTEGER, event TEXT, ts TEXT)\'\'\')\nimport random, string; random.seed(1)\nevents = [\'login\',\'logout\',\'purchase\',\'view\']\nrows = [(i, random.randint(1,50),\n         random.choice(events),\n         f\'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}\')\n        for i in range(1,3001)]\nrunmany(\'INSERT INTO logs2 VALUES (?,?,?,?)\', rows)\n# Covering index: avoid table access for common query\nrun(\'CREATE INDEX IF NOT EXISTS idx_cov ON logs2(user_id, event, ts)\')\nplan = run(\'\'\'EXPLAIN QUERY PLAN\n    SELECT user_id, event, ts FROM logs2\n    WHERE user_id=1 ORDER BY ts\'\'\')\nfor p in plan: print(p)\n"},
        {"label": "Partial index and ANALYZE", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS items (\n    id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)\'\'\')\nimport random; random.seed(5)\nrows = [(i,f\'item_{i}\',round(random.uniform(1,100),2),random.randint(0,500)) for i in range(1,1001)]\nrunmany(\'INSERT INTO items VALUES (?,?,?,?)\', rows)\n# ANALYZE updates statistics for the query planner\nrun(\'ANALYZE\')\n# Partial index: only index in-stock items\nrun(\'CREATE INDEX IF NOT EXISTS idx_instock ON items(price) WHERE stock > 0\')\nplan = run(\'\'\'EXPLAIN QUERY PLAN\n    SELECT name, price FROM items\n    WHERE stock > 0 AND price < 20\n    ORDER BY price\'\'\')\nfor p in plan: print(p)\nprint(run(\'SELECT COUNT(*) FROM items WHERE stock>0\'))\n"}
    ],
"rw": {
    "title": "Slow Query Investigation",
    "scenario": "A production query joining orders and customers is slow. Use EXPLAIN QUERY PLAN to find the bottleneck, add an appropriate index, and verify the improvement.",
    "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS cust2 (id INTEGER PRIMARY KEY, name TEXT, tier TEXT)\'\'\')\nrun(\'\'\'CREATE TABLE IF NOT EXISTS ord2 (\n    id INTEGER PRIMARY KEY, cust_id INTEGER, amount REAL, status TEXT)\'\'\')\nimport random; random.seed(7)\nrunmany(\'INSERT INTO cust2 VALUES (?,?,?)\', [(i,f\'C{i}\',random.choice([\'gold\',\'silver\'])) for i in range(1,501)])\nrunmany(\'INSERT INTO ord2 VALUES (?,?,?,?)\',\n    [(i,random.randint(1,500),round(random.uniform(10,500),2),\n      random.choice([\'paid\',\'pending\'])) for i in range(1,2001)])\nplan = run(\'\'\'EXPLAIN QUERY PLAN\n    SELECT c.name, SUM(o.amount)\n    FROM ord2 o JOIN cust2 c ON o.cust_id=c.id\n    WHERE o.status=\'paid\' AND c.tier=\'gold\'\n    GROUP BY c.id\'\'\')\nfor p in plan: print(p)\nrun(\'CREATE INDEX IF NOT EXISTS idx_ord_status ON ord2(status, cust_id)\')\nrun(\'CREATE INDEX IF NOT EXISTS idx_cust_tier ON cust2(tier)\')\nplan2 = run(\'\'\'EXPLAIN QUERY PLAN\n    SELECT c.name, SUM(o.amount)\n    FROM ord2 o JOIN cust2 c ON o.cust_id=c.id\n    WHERE o.status=\'paid\' AND c.tier=\'gold\'\n    GROUP BY c.id\'\'\')\nfor p in plan2: print(p)\n"
},
"practice": {
    "title": "Index Optimization Practice",
    "desc": "Create a \'transactions2\' table (id, account_id INTEGER, type TEXT, amount REAL, created_at TEXT). Insert 500 rows. Use EXPLAIN QUERY PLAN to check a query filtering by account_id and type, then add the right index to make it efficient.",
    "starter": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nimport random; random.seed(9)\nrun(\'\'\'CREATE TABLE IF NOT EXISTS transactions2 (\n    id INTEGER PRIMARY KEY, account_id INTEGER,\n    type TEXT, amount REAL, created_at TEXT)\'\'\')\nrows = [(i, random.randint(1,50), random.choice([\'debit\',\'credit\']),\n         round(random.uniform(1,1000),2), f\'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}\')\n        for i in range(1,501)]\nrunmany(\'INSERT INTO transactions2 VALUES (?,?,?,?,?)\', rows)\n# First check the plan, then add an index\nplan = run(\'\'\'EXPLAIN QUERY PLAN\n    SELECT * FROM transactions2\n    WHERE account_id=5 AND type=\'debit\' ORDER BY created_at\'\'\')\nfor p in plan: print(p)\n# Add your index here\n"
}
},

{
"title": "32. SQL for Data Analysis Workflow",
"desc": "Apply SQL as a full data analysis tool: ingest and clean dirty data, compute monthly trends with running totals, compare performance vs. group averages, and pivot long-format survey data.",
"examples": [
        {"label": "Ingest and clean dirty text amounts", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\n# End-to-end: ingest, clean, transform, analyze\nrun(\'\'\'CREATE TABLE IF NOT EXISTS raw_sales (\n    id INTEGER PRIMARY KEY,\n    rep TEXT, region TEXT,\n    amount TEXT,  -- stored as text (dirty data)\n    sale_date TEXT)\'\'\')\nrunmany(\'INSERT INTO raw_sales VALUES (?,?,?,?,?)\', [\n    (1,\'Alice\',\'North\',\'1,200.50\',\'2024-01-15\'),\n    (2,\'Bob\',\'South\',\'800\',\'2024-01-20\'),\n    (3,\'Alice\',\'North\',\'  950.00 \',\'2024-02-01\'),\n    (4,\'Carol\',\'East\',\'\',\'2024-02-10\'),   -- missing amount\n    (5,\'Bob\',\'South\',\'1100.75\',\'2024-02-20\'),\n])\n# Clean: strip whitespace, handle empty, cast\nrows = run(\'\'\'\n    SELECT rep, region,\n        CASE WHEN TRIM(REPLACE(amount,\',\',\'\'))=\'\' THEN NULL\n             ELSE CAST(TRIM(REPLACE(amount,\',\',\'\')) AS REAL)\n        END AS clean_amount,\n        sale_date\n    FROM raw_sales\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "Monthly trend with running total CTE", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS cleaned_sales (\n    rep TEXT, region TEXT, amount REAL, sale_date TEXT)\'\'\')\nrunmany(\'INSERT INTO cleaned_sales VALUES (?,?,?,?)\', [\n    (\'Alice\',\'North\',1200.50,\'2024-01-15\'),\n    (\'Bob\',\'South\',800.00,\'2024-01-20\'),\n    (\'Alice\',\'North\',950.00,\'2024-02-01\'),\n    (\'Bob\',\'South\',1100.75,\'2024-02-20\'),\n    (\'Carol\',\'East\',750.00,\'2024-03-05\'),\n    (\'Alice\',\'North\',1350.00,\'2024-03-10\'),\n])\n# Monthly trend and running total\nrows = run(\'\'\'\n    WITH monthly AS (\n        SELECT SUBSTR(sale_date,1,7) AS month,\n               rep, SUM(amount) AS total\n        FROM cleaned_sales GROUP BY month, rep)\n    SELECT month, rep, total,\n        SUM(total) OVER(PARTITION BY rep ORDER BY month) AS running_total\n    FROM monthly ORDER BY rep, month\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "Rep performance vs. regional average", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS sales_f (\n    rep TEXT, region TEXT, amount REAL, sale_date TEXT)\'\'\')\nrunmany(\'INSERT INTO sales_f VALUES (?,?,?,?)\', [\n    (\'Alice\',\'North\',1200,\'2024-01-15\'),(\'Bob\',\'South\',800,\'2024-01-20\'),\n    (\'Alice\',\'North\',950,\'2024-02-01\'),(\'Carol\',\'East\',750,\'2024-02-10\'),\n    (\'Bob\',\'South\',1100,\'2024-02-20\'),(\'Alice\',\'North\',1350,\'2024-03-10\'),\n    (\'Carol\',\'East\',900,\'2024-03-15\'),(\'Bob\',\'South\',1250,\'2024-03-20\'),\n])\n# Cohort-style: rep performance vs. regional average\nrows = run(\'\'\'\n    SELECT rep, region, ROUND(SUM(amount),2) AS rep_total,\n        ROUND(AVG(SUM(amount)) OVER(PARTITION BY region),2) AS region_avg,\n        ROUND(SUM(amount) - AVG(SUM(amount)) OVER(PARTITION BY region),2) AS vs_avg\n    FROM sales_f GROUP BY rep, region ORDER BY region, rep\'\'\')\nfor r in rows: print(r)\n"},
        {"label": "Pivot survey data with CASE WHEN", "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS survey (\n    respondent_id INTEGER, question TEXT, score INTEGER)\'\'\')\nrunmany(\'INSERT INTO survey VALUES (?,?,?)\', [\n    (1,\'Q1\',4),(1,\'Q2\',5),(1,\'Q3\',3),\n    (2,\'Q1\',2),(2,\'Q2\',3),(2,\'Q3\',4),\n    (3,\'Q1\',5),(3,\'Q2\',5),(3,\'Q3\',5),\n    (4,\'Q1\',3),(4,\'Q2\',2),(4,\'Q3\',3),\n])\n# Pivot: one row per respondent, one column per question\nrows = run(\'\'\'\n    SELECT respondent_id,\n        MAX(CASE WHEN question=\'Q1\' THEN score END) AS Q1,\n        MAX(CASE WHEN question=\'Q2\' THEN score END) AS Q2,\n        MAX(CASE WHEN question=\'Q3\' THEN score END) AS Q3,\n        ROUND(AVG(score),2) AS avg_score\n    FROM survey GROUP BY respondent_id ORDER BY respondent_id\'\'\')\nfor r in rows: print(r)\n"}
    ],
"rw": {
    "title": "Sales Dashboard Pipeline",
    "scenario": "Build a SQL pipeline: clean raw data, compute monthly totals, calculate month-over-month growth, and rank reps by total sales within their region.",
    "code": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS pipeline_sales (\n    rep TEXT, region TEXT, amount REAL, sale_date TEXT)\'\'\')\nrunmany(\'INSERT INTO pipeline_sales VALUES (?,?,?,?)\', [\n    (\'Alice\',\'North\',1200,\'2024-01-10\'),(\'Bob\',\'North\',950,\'2024-01-20\'),\n    (\'Alice\',\'North\',1400,\'2024-02-05\'),(\'Bob\',\'North\',1100,\'2024-02-15\'),\n    (\'Carol\',\'South\',800,\'2024-01-12\'),(\'Dave\',\'South\',900,\'2024-01-25\'),\n    (\'Carol\',\'South\',1050,\'2024-02-08\'),(\'Dave\',\'South\',750,\'2024-02-18\'),\n])\nrows = run(\'\'\'\n    WITH monthly AS (\n        SELECT rep, region, SUBSTR(sale_date,1,7) AS month,\n               SUM(amount) AS total\n        FROM pipeline_sales GROUP BY rep, region, month),\n    with_growth AS (\n        SELECT *,\n            LAG(total) OVER(PARTITION BY rep ORDER BY month) AS prev,\n            ROUND(100.0*(total - LAG(total) OVER(PARTITION BY rep ORDER BY month))\n                  / LAG(total) OVER(PARTITION BY rep ORDER BY month), 1) AS pct_growth\n        FROM monthly)\n    SELECT *, RANK() OVER(PARTITION BY region, month ORDER BY total DESC) AS region_rank\n    FROM with_growth ORDER BY region, month, region_rank\'\'\')\nfor r in rows: print(r)\n"
},
"practice": {
    "title": "End-to-End Analysis Practice",
    "desc": "Create a \'web_logs\' table with (session_id INTEGER, user_id INTEGER, page TEXT, duration_sec INTEGER, log_date TEXT). Insert 10 rows. Write a query that: (1) filters sessions over 30s, (2) counts sessions per user per day, and (3) shows each user\'s max daily sessions using a window function.",
    "starter": "import sqlite3, contextlib\\nconn = sqlite3.connect(\':memory:\')\\nconn.execute(\'PRAGMA journal_mode=WAL\')\\ndef run(sql, params=()):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.execute(sql, params)\\n        if cur.description:\\n            return cur.fetchall()\\n        conn.commit()\\n        return cur.rowcount\\ndef runmany(sql, rows):\\n    with contextlib.closing(conn.cursor()) as cur:\\n        cur.executemany(sql, rows)\\n        conn.commit()\\nrun(\'\'\'CREATE TABLE IF NOT EXISTS web_logs (\n    session_id INTEGER, user_id INTEGER,\n    page TEXT, duration_sec INTEGER, log_date TEXT)\'\'\')\nrunmany(\'INSERT INTO web_logs VALUES (?,?,?,?,?)\', [\n    (1,1,\'home\',45,\'2024-01-01\'),(2,1,\'about\',20,\'2024-01-01\'),\n    (3,2,\'home\',60,\'2024-01-01\'),(4,2,\'shop\',90,\'2024-01-01\'),\n    (5,1,\'home\',35,\'2024-01-02\'),(6,1,\'shop\',55,\'2024-01-02\'),\n    (7,3,\'home\',15,\'2024-01-01\'),(8,3,\'about\',40,\'2024-01-01\'),\n    (9,2,\'home\',80,\'2024-01-02\'),(10,3,\'shop\',50,\'2024-01-02\'),\n])\n# Write your query: filter >30s, count per user/day, window max\n"
}
},

]  # end SECTIONS


# ─── Generate ─────────────────────────────────────────────────────────────────
html = make_html(SECTIONS)
nb   = make_nb(SECTIONS)
(BASE / "index.html").write_text(html, encoding="utf-8")
(BASE / "study_guide.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")
print(f"SQL guide created: {BASE}")
print(f"  index.html:        {(BASE/'index.html').stat().st_size/1024:.1f} KB")
print(f"  study_guide.ipynb: {len(nb['cells'])} cells")
