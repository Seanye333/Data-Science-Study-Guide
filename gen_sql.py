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
]  # end SECTIONS


# ─── Generate ─────────────────────────────────────────────────────────────────
html = make_html(SECTIONS)
nb   = make_nb(SECTIONS)
(BASE / "index.html").write_text(html, encoding="utf-8")
(BASE / "study_guide.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")
print(f"SQL guide created: {BASE}")
print(f"  index.html:        {(BASE/'index.html').stat().st_size/1024:.1f} KB")
print(f"  study_guide.ipynb: {len(nb['cells'])} cells")
