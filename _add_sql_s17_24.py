"""Add sections 17-24 to gen_sql.py."""
import sys
sys.path.insert(0, r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
from _inserter import insert_sections

FILE   = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_sql.py"
MARKER = "]  # end SECTIONS"

def ec(code):
    return (code.replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace("'", "\\'"))

def make_sql(num, title, desc, examples, rw_title, rw_scenario, rw_code, pt, pd_text, ps):
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

SETUP = """import sqlite3, contextlib
conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA journal_mode=WAL')
def run(sql, params=()):
    with contextlib.closing(conn.cursor()) as cur:
        cur.execute(sql, params)
        if cur.description:
            return cur.fetchall()
        conn.commit()
        return cur.rowcount
def runmany(sql, rows):
    with contextlib.closing(conn.cursor()) as cur:
        cur.executemany(sql, rows)
        conn.commit()
"""

# ── Section 17: Subqueries in Depth ─────────────────────────────────────────
s17 = make_sql(17, "Subqueries in Depth",
    "Subqueries (nested SELECT) can appear in WHERE, FROM, SELECT, and HAVING clauses. Master scalar, column, table, and correlated subqueries for complex filtering and derived metrics.",
    [
        {"label": "Scalar and column subqueries in WHERE",
         "code": SETUP +
"""run('''CREATE TABLE sales (id INTEGER, rep TEXT, amount REAL, region TEXT)''')
runmany('INSERT INTO sales VALUES (?,?,?,?)', [
    (1,'Alice',1200,'North'),(2,'Bob',800,'South'),(3,'Carol',1500,'North'),
    (4,'Dave',600,'South'),(5,'Eve',2000,'North'),(6,'Frank',950,'East'),
])

# Scalar subquery: single value in WHERE
rows = run('''
    SELECT rep, amount FROM sales
    WHERE amount > (SELECT AVG(amount) FROM sales)
    ORDER BY amount DESC
''')
print("Above-average reps:")
for r in rows: print(f"  {r[0]}: ${r[1]:,.0f}")

# IN with subquery
rows = run('''
    SELECT rep, amount FROM sales
    WHERE region IN (SELECT DISTINCT region FROM sales WHERE amount > 1000)
    AND amount < 1000
    ORDER BY amount
''')
print("In high-value regions but low individual amount:")
for r in rows: print(f"  {r[0]}: ${r[1]:,.0f}")"""},
        {"label": "Correlated subqueries",
         "code": SETUP +
"""run('''CREATE TABLE employees (id INTEGER, name TEXT, dept TEXT, salary REAL)''')
runmany('INSERT INTO employees VALUES (?,?,?,?)', [
    (1,'Alice','Eng',90000),(2,'Bob','Eng',85000),(3,'Carol','Sales',70000),
    (4,'Dave','Sales',72000),(5,'Eve','HR',65000),(6,'Frank','Eng',95000),
    (7,'Grace','HR',68000),(8,'Henry','Sales',75000),
])

# Correlated subquery: runs ONCE PER ROW in outer query
# Find employees earning above their department average
rows = run('''
    SELECT e.name, e.dept, e.salary,
           ROUND((SELECT AVG(salary) FROM employees i WHERE i.dept = e.dept), 0) AS dept_avg
    FROM employees e
    WHERE e.salary > (SELECT AVG(salary) FROM employees i WHERE i.dept = e.dept)
    ORDER BY e.dept, e.salary DESC
''')
print("Above-department-average earners:")
for r in rows:
    print(f"  {r[0]} ({r[1]}): ${r[2]:,.0f} (dept avg ${r[3]:,.0f})")

# EXISTS: check for related rows
rows = run('''
    SELECT DISTINCT dept FROM employees e
    WHERE EXISTS (
        SELECT 1 FROM employees i
        WHERE i.dept = e.dept AND i.salary > 80000
    )
''')
print("Departments with at least one high earner:", [r[0] for r in rows])"""},
        {"label": "Derived tables (subquery in FROM)",
         "code": SETUP +
"""run('''CREATE TABLE orders (id INTEGER, cust_id INTEGER, total REAL, yr INTEGER)''')
runmany('INSERT INTO orders VALUES (?,?,?,?)', [
    (1,1,500,2023),(2,1,300,2023),(3,2,1200,2023),(4,2,800,2024),
    (5,3,200,2024),(6,1,900,2024),(7,3,600,2023),(8,2,400,2024),
])

# Derived table: aggregate first, then filter/join
rows = run('''
    SELECT cust_id, total_2023, total_2024,
           ROUND(total_2024 - total_2023, 0) AS growth
    FROM (
        SELECT cust_id,
               SUM(CASE WHEN yr=2023 THEN total ELSE 0 END) AS total_2023,
               SUM(CASE WHEN yr=2024 THEN total ELSE 0 END) AS total_2024
        FROM orders
        GROUP BY cust_id
    ) yearly
    ORDER BY growth DESC
''')
print("Year-over-year growth by customer:")
for r in rows:
    print(f"  Cust {r[0]}: 2023=${r[1]:,.0f} -> 2024=${r[2]:,.0f} ({r[3]:+,.0f})")

# Derived table with LIMIT for top-N analysis
rows = run('''
    SELECT cust_id, avg_order
    FROM (SELECT cust_id, AVG(total) AS avg_order FROM orders GROUP BY cust_id)
    WHERE avg_order > 500
''')
print("Customers with avg order > 500:", rows)"""}
    ],
    rw_title="Sales Ranking with Subqueries",
    rw_scenario="A sales ops team needs to find reps in each region who beat both their regional average AND the company average — combining correlated subqueries with derived tables.",
    rw_code= SETUP +
"""run('''CREATE TABLE sales (id INTEGER, rep TEXT, region TEXT, amount REAL, quarter INTEGER)''')
runmany('INSERT INTO sales VALUES (?,?,?,?,?)', [
    (1,'Alice','North',1200,1),(2,'Bob','North',800,1),(3,'Carol','South',1500,1),
    (4,'Dave','South',600,1),(5,'Eve','North',2000,2),(6,'Frank','South',950,2),
    (7,'Grace','East',1100,1),(8,'Henry','East',750,1),(9,'Iris','East',1300,2),
])
company_avg = run('SELECT AVG(amount) FROM sales')[0][0]
print(f"Company avg: ${company_avg:,.0f}")

rows = run(f'''
    SELECT s.rep, s.region, s.amount,
           ROUND(regional.avg_amount, 0) AS regional_avg
    FROM sales s
    JOIN (
        SELECT region, AVG(amount) AS avg_amount
        FROM sales GROUP BY region
    ) regional ON s.region = regional.region
    WHERE s.amount > regional.avg_amount
      AND s.amount > {company_avg}
    ORDER BY s.region, s.amount DESC
''')
print("Reps beating both regional AND company average:")
for r in rows:
    print(f"  {r[0]} ({r[1]}): ${r[2]:,.0f} > regional ${r[3]:,.0f}")""",
    pt="Self-referencing Subquery",
    pd_text="Create a products table (id, name, category, price, cost). Write: (1) A query using a scalar subquery to show each product with its category's avg price. (2) A correlated subquery to find the cheapest product in each category. (3) A derived table query to show categories where avg margin (price-cost)/price > 30%.",
    ps=SETUP +
"""run('''CREATE TABLE products (id INT, name TEXT, category TEXT, price REAL, cost REAL)''')
runmany('INSERT INTO products VALUES (?,?,?,?,?)', [
    (1,'Apple','Fruit',1.2,0.4),(2,'Banana','Fruit',0.5,0.15),(3,'Carrot','Veg',0.8,0.3),
    (4,'Potato','Veg',0.6,0.2),(5,'Milk','Dairy',1.5,0.8),(6,'Cheese','Dairy',4.0,1.5),
    (7,'Yogurt','Dairy',2.0,0.9),(8,'Broccoli','Veg',1.1,0.4),
])

# 1. Each product with its category avg price
print("=== Product vs Category Avg ===")
# TODO: write query with scalar correlated subquery for category avg

# 2. Cheapest product in each category
print("=== Cheapest per Category ===")
# TODO: use correlated subquery to find min price per category

# 3. Categories with avg margin > 30%
print("=== High-Margin Categories ===")
# TODO: derived table with margin calc, then filter
"""
)

# ── Section 18: String Functions & Pattern Matching ──────────────────────────
s18 = make_sql(18, "String Functions & Pattern Matching",
    "SQL provides rich string functions: UPPER/LOWER, SUBSTR, TRIM, REPLACE, LENGTH, INSTR, and LIKE/GLOB for pattern matching. Essential for cleaning and searching text data.",
    [
        {"label": "Core string functions",
         "code": SETUP +
"""run('''CREATE TABLE contacts (id INTEGER, name TEXT, email TEXT, phone TEXT)''')
runmany('INSERT INTO contacts VALUES (?,?,?,?)', [
    (1,'  Alice Smith  ','alice@EXAMPLE.com','(555) 123-4567'),
    (2,'Bob  Jones','bob.jones@mail.com','555.987.6543'),
    (3,'carol lee','CAROL@COMPANY.ORG','5551234567'),
    (4,'DAVE BROWN','dave@test.net','555-111-2222'),
])

rows = run('''
    SELECT
        id,
        TRIM(name)                              AS name_clean,
        LOWER(TRIM(name))                       AS name_lower,
        UPPER(SUBSTR(TRIM(name), 1, 1))         AS initial,
        LOWER(email)                            AS email_lower,
        LENGTH(TRIM(name))                      AS name_len,
        INSTR(TRIM(name), " ")                  AS space_pos,
        -- Extract first name (up to first space)
        SUBSTR(TRIM(name), 1, INSTR(TRIM(name)||" ", " ")-1) AS first_name
    FROM contacts
''')
for r in rows:
    print(f"  ID {r[0]}: '{r[1]}' | initial={r[2]} | fname={r[7]}")"""},
        {"label": "LIKE and GLOB pattern matching",
         "code": SETUP +
"""run('''CREATE TABLE products (id INTEGER, sku TEXT, name TEXT, category TEXT)''')
runmany('INSERT INTO products VALUES (?,?,?,?)', [
    (1,'FRUIT-APL-001','Apple (Red)','Fruit'),
    (2,'FRUIT-BAN-002','Banana','Fruit'),
    (3,'VEG-CAR-001','Carrot','Vegetable'),
    (4,'VEG-POT-002','Potato','Vegetable'),
    (5,'DAIRY-MLK-001','Whole Milk','Dairy'),
    (6,'FRUIT-APL-002','Apple (Green)','Fruit'),
    (7,'DAIRY-CHZ-001','Cheddar Cheese','Dairy'),
])

# LIKE: case-insensitive %, _ wildcards
rows = run("SELECT name FROM products WHERE name LIKE 'Apple%'")
print("Starts with 'Apple':", [r[0] for r in rows])

rows = run("SELECT name FROM products WHERE name LIKE '%e%'")
print("Contains 'e':", [r[0] for r in rows])

rows = run("SELECT sku FROM products WHERE sku LIKE 'FRUIT-___-___'")
print("SKUs matching FRUIT-???-???:", [r[0] for r in rows])

# GLOB: case-sensitive, uses * and ? (Unix-style)
rows = run("SELECT sku FROM products WHERE sku GLOB 'FRUIT-*'")
print("GLOB FRUIT-*:", [r[0] for r in rows])

rows = run("SELECT sku FROM products WHERE sku GLOB '*-001'")
print("GLOB *-001:", [r[0] for r in rows])

# NOT LIKE
rows = run("SELECT name FROM products WHERE name NOT LIKE '%Apple%'")
print("Not apple:", [r[0] for r in rows])"""},
        {"label": "String manipulation and cleaning",
         "code": SETUP +
"""run('''CREATE TABLE raw_data (id INTEGER, raw_phone TEXT, raw_email TEXT)''')
runmany('INSERT INTO raw_data VALUES (?,?,?)', [
    (1,'(555) 123-4567','  User@Example.COM  '),
    (2,'555.987.6543','bob.jones@MAIL.COM'),
    (3,'5551234567','CAROL@company.org'),
])

rows = run('''
    SELECT
        id,
        -- Normalize phone: keep only digits via REPLACE chain
        REPLACE(REPLACE(REPLACE(REPLACE(raw_phone, "(", ""), ")", ""), "-", ""), ".", "") AS phone_digits,
        -- Trim spaces and lowercase email
        LOWER(TRIM(raw_email)) AS email_clean,
        -- Extract domain from email
        SUBSTR(
            LOWER(TRIM(raw_email)),
            INSTR(LOWER(TRIM(raw_email)), "@") + 1
        ) AS domain,
        -- Check email format (has @ and .)
        CASE WHEN INSTR(raw_email, "@") > 0 AND INSTR(raw_email, ".") > 0
             THEN "valid" ELSE "invalid" END AS email_status
    FROM raw_data
''')
for r in rows:
    print(f"  ID {r[0]}: phone={r[1]}, email={r[2]}, domain={r[3]}, {r[4]}")

# REPLACE for data masking
rows = run('''
    SELECT id,
           SUBSTR(phone_digits, 1, 3) || "****" || SUBSTR(phone_digits, 8) AS masked
    FROM (SELECT id, REPLACE(REPLACE(REPLACE(raw_phone,"(",""),")",""),"-","") AS phone_digits
          FROM raw_data)
''')
print("Masked phones:", [(r[0], r[1]) for r in rows])"""}
    ],
    rw_title="Email Domain Analysis",
    rw_scenario="A marketing team analyzes which email domains their B2B customers use, normalizing inconsistent formatting before aggregating.",
    rw_code= SETUP +
"""run('''CREATE TABLE customers (id INTEGER, email TEXT, tier TEXT)''')
runmany('INSERT INTO customers VALUES (?,?,?)', [
    (1,'alice@ACME.COM','gold'),(2,'bob@tech.org','silver'),
    (3,'carol@acme.com','gold'),(4,'dave@STARTUP.IO','bronze'),
    (5,'eve@TECH.ORG','silver'),(6,'frank@enterprise.net','gold'),
    (7,'grace@startup.io','bronze'),(8,'henry@acme.com','silver'),
    (9,'iris@ENTERPRISE.NET','gold'),(10,'jack@freelance.dev','bronze'),
])

rows = run('''
    SELECT
        LOWER(SUBSTR(email, INSTR(email, "@") + 1)) AS domain,
        COUNT(*)                                      AS customers,
        SUM(CASE WHEN tier = "gold"   THEN 1 ELSE 0 END) AS gold,
        SUM(CASE WHEN tier = "silver" THEN 1 ELSE 0 END) AS silver,
        SUM(CASE WHEN tier = "bronze" THEN 1 ELSE 0 END) AS bronze
    FROM customers
    GROUP BY LOWER(SUBSTR(email, INSTR(email, "@") + 1))
    ORDER BY customers DESC
''')
print("Domain analysis:")
for r in rows:
    print(f"  {r[0]:<20} total={r[1]} gold={r[2]} silver={r[3]} bronze={r[4]}")""",
    pt="Name Formatter",
    pd_text="Create a people table (id, full_name, email). Write a query that produces: first_name (before first space), last_name (after last space), initials (first letter of each word), username (lowercase first_name + '.' + last 4 of email before @), and email_valid (1 if contains '@' and '.', else 0).",
    ps=SETUP +
"""run('''CREATE TABLE people (id INT, full_name TEXT, email TEXT)''')
runmany('INSERT INTO people VALUES (?,?,?)', [
    (1,'Alice Marie Smith','alice.smith@company.com'),
    (2,'Bob Jones','bob@mail.net'),
    (3,'Carol Ann Lee','carol.lee@invalid'),
    (4,'Dave','dave@x.io'),
])

rows = run('''
    SELECT
        id,
        -- first_name: text before first space
        SUBSTR(full_name, 1,
               CASE WHEN INSTR(full_name, " ") > 0
                    THEN INSTR(full_name, " ")-1
                    ELSE LENGTH(full_name) END) AS first_name,
        -- TODO: last_name (after last space, or full_name if no space)
        -- TODO: initials
        -- TODO: username (lower_first + . + last 4 chars before @)
        -- TODO: email_valid
        email
    FROM people
''')
for r in rows: print(r)
"""
)

# ── Section 19: Date & Time Functions ────────────────────────────────────────
s19 = make_sql(19, "Date & Time Functions",
    "SQL date functions compute differences, extract components, and format timestamps. In SQLite, dates are stored as TEXT (ISO), INTEGER (Unix epoch), or REAL (Julian day).",
    [
        {"label": "Date arithmetic and formatting (SQLite)",
         "code": SETUP +
"""# SQLite stores dates as text in ISO format: 'YYYY-MM-DD'
rows = run('''
    SELECT
        DATE('now')                           AS today,
        DATE('now', '+7 days')               AS next_week,
        DATE('now', '-30 days')              AS last_month,
        DATE('now', 'start of month')        AS month_start,
        DATE('now', 'start of year')         AS year_start,
        DATE('now', '+1 year', '-1 day')     AS end_of_next_year,
        DATETIME('now')                       AS now_dt,
        STRFTIME('%Y-%m-%d %H:%M', 'now')    AS formatted
''')
for key, val in zip(['today','next_week','last_month','month_start','year_start','eony','now_dt','fmt'], rows[0]):
    print(f"  {key}: {val}")"""},
        {"label": "Extracting date parts and calculating age",
         "code": SETUP +
"""run('''CREATE TABLE employees (id INTEGER, name TEXT, hire_date TEXT, birth_date TEXT)''')
runmany('INSERT INTO employees VALUES (?,?,?,?)', [
    (1,'Alice','2019-03-15','1990-07-22'),
    (2,'Bob','2021-11-01','1985-02-14'),
    (3,'Carol','2022-06-20','1995-09-08'),
    (4,'Dave','2018-01-10','1988-12-01'),
])

rows = run('''
    SELECT
        name,
        hire_date,
        -- Extract parts
        STRFTIME('%Y', hire_date)               AS hire_year,
        STRFTIME('%m', hire_date)               AS hire_month,
        STRFTIME('%d', hire_date)               AS hire_day,
        -- Days since hire
        CAST(JULIANDAY('now') - JULIANDAY(hire_date) AS INTEGER) AS days_employed,
        -- Years employed
        CAST((JULIANDAY('now') - JULIANDAY(hire_date)) / 365.25 AS INTEGER) AS years_employed,
        -- Age from birth_date
        CAST((JULIANDAY('now') - JULIANDAY(birth_date)) / 365.25 AS INTEGER) AS age
    FROM employees
    ORDER BY hire_date
''')
print("Employee tenure and age:")
for r in rows:
    print(f"  {r[0]}: hired {r[1]}, {r[7]} days ({r[8]} yrs), age {r[9]}")"""},
        {"label": "Time series date bucketing",
         "code": SETUP +
"""import datetime
run('''CREATE TABLE events (id INTEGER, ts TEXT, event TEXT, value REAL)''')
import random; random.seed(42)
events_data = []
for i in range(30):
    d = datetime.date(2024, 1, 1) + datetime.timedelta(days=i)
    for _ in range(random.randint(1, 5)):
        events_data.append((i*10+random.randint(1,9),
                            d.strftime('%Y-%m-%d'),
                            random.choice(['view','click','purchase']),
                            round(random.uniform(1, 100), 2)))
runmany('INSERT INTO events VALUES (?,?,?,?)', events_data)

# Group by week
rows = run('''
    SELECT
        STRFTIME('%Y-W%W', ts)         AS week,
        COUNT(*)                        AS events,
        SUM(CASE WHEN event="purchase" THEN 1 ELSE 0 END) AS purchases,
        ROUND(SUM(value), 2)            AS total_value
    FROM events
    GROUP BY week
    ORDER BY week
''')
print("Weekly breakdown:")
for r in rows: print(f"  {r[0]}: {r[1]} events, {r[2]} purchases, ${r[3]}")

# Days with no purchases
rows = run('''
    SELECT ts, COUNT(*) AS events
    FROM events
    WHERE event != "purchase"
    AND ts NOT IN (SELECT DISTINCT ts FROM events WHERE event = "purchase")
    GROUP BY ts
    ORDER BY ts
    LIMIT 3
''')
print("Days with no purchases (sample):", [(r[0],r[1]) for r in rows])"""}
    ],
    rw_title="Subscription Churn Analysis",
    rw_scenario="A SaaS company analyzes monthly churn by comparing subscription start/end dates, computing tenure, and flagging customers who churned within 90 days of signup.",
    rw_code= SETUP +
"""run('''CREATE TABLE subscriptions (id INT, cust_id INT, start_date TEXT, end_date TEXT, plan TEXT)''')
runmany('INSERT INTO subscriptions VALUES (?,?,?,?,?)', [
    (1,1,'2023-01-15','2024-01-15','annual'),
    (2,2,'2023-03-01','2023-05-15','monthly'),
    (3,3,'2023-06-01',None,'annual'),
    (4,4,'2023-09-10','2023-10-05','monthly'),
    (5,5,'2024-01-01',None,'monthly'),
    (6,6,'2023-02-14','2023-11-30','annual'),
])

rows = run('''
    SELECT
        cust_id, plan, start_date,
        COALESCE(end_date, DATE("now")) AS effective_end,
        CAST((JULIANDAY(COALESCE(end_date, DATE("now"))) -
              JULIANDAY(start_date)) AS INTEGER)         AS tenure_days,
        CASE WHEN end_date IS NOT NULL THEN "churned" ELSE "active" END AS status,
        CASE WHEN end_date IS NOT NULL
              AND JULIANDAY(end_date) - JULIANDAY(start_date) < 90
             THEN "early_churn" ELSE "ok" END AS churn_flag
    FROM subscriptions
    ORDER BY start_date
''')
print("Subscription analysis:")
for r in rows:
    print(f"  Cust {r[0]} ({r[1]}): {r[4]} days, {r[5]}, {r[6]}")""",
    pt="Date Range Queries",
    pd_text="Create a bookings table (id, room, check_in, check_out, guest). Write: (1) Find bookings overlapping a given date range ('2024-06-01' to '2024-06-10'). (2) Calculate avg stay length by month. (3) Find rooms that were booked more than 80% of days in Q2 2024. (4) Show guests with return visits within 6 months.",
    ps=SETUP +
"""run('''CREATE TABLE bookings (id INT, room TEXT, check_in TEXT, check_out TEXT, guest TEXT)''')
runmany('INSERT INTO bookings VALUES (?,?,?,?,?)', [
    (1,'101','2024-05-28','2024-06-03','Alice'),
    (2,'102','2024-06-05','2024-06-08','Bob'),
    (3,'101','2024-06-10','2024-06-15','Carol'),
    (4,'103','2024-06-01','2024-06-30','Dave'),
    (5,'102','2024-07-01','2024-07-05','Alice'),
    (6,'101','2024-08-01','2024-08-10','Bob'),
])

# 1. Overlapping bookings with date range
target_in, target_out = '2024-06-01', '2024-06-10'
print("=== Bookings overlapping Jun 1-10 ===")
rows = run(f'''
    SELECT room, guest, check_in, check_out
    FROM bookings
    WHERE check_in < "{target_out}" AND check_out > "{target_in}"
    ORDER BY check_in
''')
for r in rows: print(f"  {r}")

# 2. Avg stay length by month
print("=== Avg stay by month ===")
rows = run('''
    SELECT
        STRFTIME("%Y-%m", check_in) AS month,
        ROUND(AVG(JULIANDAY(check_out) - JULIANDAY(check_in)), 1) AS avg_nights,
        COUNT(*) AS bookings
    FROM bookings GROUP BY month ORDER BY month
''')
for r in rows: print(f"  {r}")

# 3. TODO: rooms booked > 80% of Q2 days
# 4. TODO: return visits within 6 months
"""
)

# ── Section 20: CASE WHEN & Conditional Logic ────────────────────────────────
s20 = make_sql(20, "CASE WHEN & Conditional Logic",
    "CASE WHEN is SQL's conditional expression. Use it for bucketing, pivoting, null handling, and complex conditional aggregations. Combined with COALESCE and NULLIF for robust null handling.",
    [
        {"label": "Simple and searched CASE",
         "code": SETUP +
"""run('''CREATE TABLE students (id INTEGER, name TEXT, score INTEGER, grade TEXT)''')
runmany('INSERT INTO students VALUES (?,?,?,?)', [
    (1,'Alice',95,None),(2,'Bob',72,None),(3,'Carol',88,None),
    (4,'Dave',61,None),(5,'Eve',79,None),(6,'Frank',55,None),
])

rows = run('''
    SELECT
        name, score,
        -- Searched CASE (most flexible)
        CASE
            WHEN score >= 90 THEN "A"
            WHEN score >= 80 THEN "B"
            WHEN score >= 70 THEN "C"
            WHEN score >= 60 THEN "D"
            ELSE "F"
        END AS letter_grade,
        -- Simple CASE (like switch)
        CASE ROUND(score/10)*10
            WHEN 100 THEN "Perfect"
            WHEN 90  THEN "Excellent"
            WHEN 80  THEN "Good"
            WHEN 70  THEN "Pass"
            ELSE "Fail"
        END AS band,
        -- Boolean expression
        CASE WHEN score >= 70 THEN 1 ELSE 0 END AS passed
    FROM students
    ORDER BY score DESC
''')
for r in rows:
    print(f"  {r[0]}: {r[1]} -> {r[2]} ({r[3]}) passed={r[4]}")"""},
        {"label": "CASE in aggregations (conditional counting)",
         "code": SETUP +
"""run('''CREATE TABLE orders (id INTEGER, status TEXT, region TEXT, total REAL)''')
runmany('INSERT INTO orders VALUES (?,?,?,?)', [
    (1,'completed','North',500),(2,'cancelled','South',300),(3,'completed','North',800),
    (4,'pending','East',200),(5,'completed','South',650),(6,'cancelled','North',400),
    (7,'completed','East',1200),(8,'pending','South',350),(9,'completed','East',900),
])

rows = run('''
    SELECT
        region,
        COUNT(*)                                              AS total_orders,
        SUM(CASE WHEN status = "completed" THEN 1 ELSE 0 END) AS completed,
        SUM(CASE WHEN status = "cancelled" THEN 1 ELSE 0 END) AS cancelled,
        SUM(CASE WHEN status = "pending"   THEN 1 ELSE 0 END) AS pending,
        ROUND(100.0 * SUM(CASE WHEN status="completed" THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_pct,
        ROUND(SUM(CASE WHEN status="completed" THEN total ELSE 0 END), 0) AS completed_revenue,
        ROUND(AVG(CASE WHEN status="completed" THEN total ELSE NULL END), 0) AS avg_completed
    FROM orders
    GROUP BY region
    ORDER BY completed_revenue DESC
''')
print("Order analysis by region:")
for r in rows:
    print(f"  {r[0]}: {r[1]} orders, {r[2]} completed ({r[5]}%), revenue=${r[6]}, avg=${r[7]}")"""},
        {"label": "COALESCE, NULLIF, and IIF",
         "code": SETUP +
"""run('''CREATE TABLE metrics (id INTEGER, name TEXT, q1 REAL, q2 REAL, q3 REAL, q4 REAL)''')
runmany('INSERT INTO metrics VALUES (?,?,?,?,?,?)', [
    (1,'Revenue',1000,None,1200,None),
    (2,'Costs',600,700,None,650),
    (3,'Users',500,520,None,None),
])

rows = run('''
    SELECT
        name,
        -- COALESCE: return first non-NULL value
        COALESCE(q1, 0)                    AS q1_safe,
        COALESCE(q2, q1, 0)               AS q2_or_q1,  -- fill q2 from q1
        COALESCE(q3, q2, q1, 0)           AS q3_fill,

        -- NULLIF: return NULL if two values are equal
        NULLIF(q1, 0)                      AS q1_null_if_zero,

        -- IIF (SQLite 3.32+): shorthand for simple CASE WHEN
        IIF(q4 IS NULL, "missing", "present") AS q4_status,

        -- Compute quarter growth (handles NULLs gracefully)
        CASE WHEN q1 IS NOT NULL AND q2 IS NOT NULL
             THEN ROUND((q2 - q1) / q1 * 100, 1)
             ELSE NULL END AS q1_q2_growth_pct
    FROM metrics
''')
print("Metric analysis:")
for r in rows:
    print(f"  {r[0]}: q1_safe={r[1]}, q2_or_q1={r[2]}, q3_fill={r[3]}, q4={r[5]}, growth={r[6]}")"""}
    ],
    rw_title="Customer Segmentation",
    rw_scenario="A CRM team segments customers by RFM score (Recency, Frequency, Monetary) using CASE WHEN on aggregated purchase data to assign Bronze/Silver/Gold/Platinum tiers.",
    rw_code= SETUP +
"""run('''CREATE TABLE purchases (id INT, cust_id INT, amount REAL, purchase_date TEXT)''')
runmany('INSERT INTO purchases VALUES (?,?,?,?)', [
    (1,1,150,'2024-01-10'),(2,1,200,'2024-02-15'),(3,1,180,'2024-03-01'),
    (4,2,500,'2024-03-20'),(5,2,300,'2024-03-25'),
    (6,3,50,'2023-12-01'),(7,4,1000,'2024-03-28'),(8,4,800,'2024-03-29'),
    (9,4,600,'2024-03-30'),
])

rows = run('''
    WITH rfm AS (
        SELECT
            cust_id,
            CAST(JULIANDAY("2024-04-01") - JULIANDAY(MAX(purchase_date)) AS INT) AS recency_days,
            COUNT(*) AS frequency,
            ROUND(SUM(amount), 0) AS monetary
        FROM purchases GROUP BY cust_id
    )
    SELECT
        cust_id, recency_days, frequency, monetary,
        CASE
            WHEN recency_days <= 7  AND frequency >= 3 AND monetary >= 500 THEN "Platinum"
            WHEN recency_days <= 30 AND frequency >= 2                      THEN "Gold"
            WHEN recency_days <= 60                                          THEN "Silver"
            ELSE "Bronze"
        END AS tier
    FROM rfm ORDER BY monetary DESC
''')
print("Customer RFM tiers:")
for r in rows:
    print(f"  Cust {r[0]}: recency={r[1]}d, freq={r[2]}, monetary=${r[3]} -> {r[4]}")""",
    pt="Score Bucketing",
    pd_text="Create a test_results table (student_id, subject, score). Write: (1) A pivot showing each subject's count of A/B/C/D/F grades using CASE in SUM. (2) A letter grade column + 'needs_review' flag (grade D or F). (3) Each student's weakest subject (lowest score). (4) Students who improved: passed all subjects (score >= 70).",
    ps=SETUP +
"""run('''CREATE TABLE test_results (student_id INT, subject TEXT, score INT)''')
runmany('INSERT INTO test_results VALUES (?,?,?)', [
    (1,'Math',85),(1,'English',72),(1,'Science',90),
    (2,'Math',60),(2,'English',88),(2,'Science',55),
    (3,'Math',95),(3,'English',91),(3,'Science',87),
    (4,'Math',70),(4,'English',65),(4,'Science',80),
])

# 1. Pivot: count of each grade per subject
print("=== Grade Distribution by Subject ===")
rows = run('''
    SELECT subject,
           SUM(CASE WHEN score >= 90 THEN 1 ELSE 0 END) AS A_count,
           SUM(CASE WHEN score >= 80 AND score < 90 THEN 1 ELSE 0 END) AS B_count,
           SUM(CASE WHEN score >= 70 AND score < 80 THEN 1 ELSE 0 END) AS C_count,
           SUM(CASE WHEN score < 70 THEN 1 ELSE 0 END) AS D_or_F_count
    FROM test_results GROUP BY subject
''')
for r in rows: print(f"  {r}")

# 2. TODO: letter grade + needs_review flag
# 3. TODO: weakest subject per student
# 4. TODO: students passing all subjects
"""
)

# ── Section 21: Set Operations ───────────────────────────────────────────────
s21 = make_sql(21, "Set Operations (UNION, INTERSECT, EXCEPT)",
    "SQL set operations combine results of multiple SELECT statements: UNION (all unique), UNION ALL (keep duplicates), INTERSECT (common rows), and EXCEPT/MINUS (rows in first but not second).",
    [
        {"label": "UNION and UNION ALL",
         "code": SETUP +
"""run('''CREATE TABLE customers_2023 (id INTEGER, name TEXT, email TEXT)''')
run('''CREATE TABLE customers_2024 (id INTEGER, name TEXT, email TEXT)''')
runmany('INSERT INTO customers_2023 VALUES (?,?,?)', [
    (1,'Alice','alice@mail.com'),(2,'Bob','bob@mail.com'),
    (3,'Carol','carol@mail.com'),(4,'Dave','dave@mail.com'),
])
runmany('INSERT INTO customers_2024 VALUES (?,?,?)', [
    (3,'Carol','carol@mail.com'),(4,'Dave','dave@mail.com'),
    (5,'Eve','eve@mail.com'),(6,'Frank','frank@mail.com'),
])

# UNION: unique rows only (deduplicates)
rows = run('''
    SELECT "2023" AS year, name FROM customers_2023
    UNION
    SELECT "2024" AS year, name FROM customers_2024
    ORDER BY name
''')
print(f"UNION (unique names): {len(rows)} rows")
for r in rows: print(f"  {r}")

# UNION ALL: keeps all rows including duplicates
rows = run('''
    SELECT "2023" AS cohort, name FROM customers_2023
    UNION ALL
    SELECT "2024" AS cohort, name FROM customers_2024
    ORDER BY name
''')
print(f"UNION ALL (all rows): {len(rows)} rows")

# Useful: combine logs from two tables
rows = run('''
    SELECT "new_customer" AS event, name, "2023" AS yr FROM customers_2023
    UNION ALL
    SELECT "new_customer", name, "2024" FROM customers_2024
    ORDER BY yr, name
''')
print("All customer events:", len(rows))"""},
        {"label": "INTERSECT and EXCEPT",
         "code": SETUP +
"""run('''CREATE TABLE eligible_2023 (cust_id INTEGER)''')
run('''CREATE TABLE eligible_2024 (cust_id INTEGER)''')
run('''CREATE TABLE opted_out (cust_id INTEGER)''')
runmany('INSERT INTO eligible_2023 VALUES (?)', [(i,) for i in [1,2,3,4,5,6]])
runmany('INSERT INTO eligible_2024 VALUES (?)', [(i,) for i in [3,4,5,6,7,8]])
runmany('INSERT INTO opted_out VALUES (?)', [(i,) for i in [2,5,8]])

# INTERSECT: rows that appear in BOTH queries
rows = run('''
    SELECT cust_id FROM eligible_2023
    INTERSECT
    SELECT cust_id FROM eligible_2024
    ORDER BY cust_id
''')
print("Eligible BOTH years:", [r[0] for r in rows])

# EXCEPT: rows in first but NOT in second
rows = run('''
    SELECT cust_id FROM eligible_2023
    EXCEPT
    SELECT cust_id FROM eligible_2024
''')
print("Only eligible in 2023:", [r[0] for r in rows])

# Combine: eligible both years, excluding opted-out
rows = run('''
    SELECT cust_id FROM eligible_2023
    INTERSECT
    SELECT cust_id FROM eligible_2024
    EXCEPT
    SELECT cust_id FROM opted_out
    ORDER BY cust_id
''')
print("Eligible both years AND not opted out:", [r[0] for r in rows])"""},
        {"label": "Set operations for data reconciliation",
         "code": SETUP +
"""run('''CREATE TABLE source_records (id INTEGER, value REAL, ts TEXT)''')
run('''CREATE TABLE target_records (id INTEGER, value REAL, ts TEXT)''')
runmany('INSERT INTO source_records VALUES (?,?,?)', [
    (1,100.0,'2024-01-01'),(2,200.0,'2024-01-02'),(3,300.0,'2024-01-03'),
    (4,400.0,'2024-01-04'),(5,500.0,'2024-01-05'),
])
runmany('INSERT INTO target_records VALUES (?,?,?)', [
    (1,100.0,'2024-01-01'),(2,201.0,'2024-01-02'),  # id=2 has wrong value
    (3,300.0,'2024-01-03'),                           # id=4,5 missing
    (6,600.0,'2024-01-06'),                           # id=6 is extra
])

# Records in source but not in target (missing)
missing = run('''
    SELECT id, value, "missing_from_target" AS issue FROM source_records
    EXCEPT
    SELECT id, value, "missing_from_target" FROM target_records
''')
print("Issues in reconciliation:")
for r in missing: print(f"  Source id={r[0]}, value={r[1]} not in target")

# Records in target but not in source (extra)
extra = run('''
    SELECT id, value FROM target_records
    EXCEPT
    SELECT id, value FROM source_records
''')
for r in extra: print(f"  Target id={r[0]}, value={r[1]} not in source")

# Exact matches
matched = run('''
    SELECT COUNT(*) FROM (
        SELECT id, value FROM source_records
        INTERSECT
        SELECT id, value FROM target_records
    )
''')
print(f"Exactly matched records: {matched[0][0]}")"""}
    ],
    rw_title="Data Migration Audit",
    rw_scenario="A data engineering team validates a migration by comparing source and destination tables using INTERSECT and EXCEPT to find missing, extra, and mismatched records.",
    rw_code= SETUP +
"""run('''CREATE TABLE source_customers (id INT, name TEXT, email TEXT, tier TEXT)''')
run('''CREATE TABLE migrated_customers (id INT, name TEXT, email TEXT, tier TEXT)''')
runmany('INSERT INTO source_customers VALUES (?,?,?,?)', [
    (1,'Alice','alice@a.com','gold'),(2,'Bob','bob@b.com','silver'),
    (3,'Carol','carol@c.com','bronze'),(4,'Dave','dave@d.com','gold'),
    (5,'Eve','eve@e.com','silver'),
])
runmany('INSERT INTO migrated_customers VALUES (?,?,?,?)', [
    (1,'Alice','alice@a.com','gold'),(2,'Bob','bob_new@b.com','silver'),
    (3,'Carol','carol@c.com','bronze'),(6,'Frank','frank@f.com','bronze'),
])

fully_matched = run('''
    SELECT COUNT(*) FROM (
        SELECT id,name,email,tier FROM source_customers
        INTERSECT
        SELECT id,name,email,tier FROM migrated_customers)''')[0][0]
missing_in_dest = run('''
    SELECT id, name FROM source_customers
    EXCEPT SELECT id, name FROM migrated_customers''')
extra_in_dest = run('''
    SELECT id, name FROM migrated_customers
    EXCEPT SELECT id, name FROM source_customers''')

print(f"Source: {run('SELECT COUNT(*) FROM source_customers')[0][0]} records")
print(f"Migrated: {run('SELECT COUNT(*) FROM migrated_customers')[0][0]} records")
print(f"Fully matched: {fully_matched}")
print(f"Missing from dest: {[(r[0],r[1]) for r in missing_in_dest]}")
print(f"Extra in dest: {[(r[0],r[1]) for r in extra_in_dest]}")""",
    pt="Set Operation Analytics",
    pd_text="Create active_users_jan, active_users_feb, active_users_mar tables (each with user_id). Write queries to find: (1) Users active all 3 months (INTERSECT x3). (2) Users active in Jan but NOT Feb (EXCEPT). (3) All unique users across 3 months (UNION). (4) Users active in exactly 2 of 3 months using INTERSECT/EXCEPT combinations.",
    ps=SETUP +
"""run('''CREATE TABLE active_jan (user_id INT)''')
run('''CREATE TABLE active_feb (user_id INT)''')
run('''CREATE TABLE active_mar (user_id INT)''')
runmany('INSERT INTO active_jan VALUES (?)', [(i,) for i in [1,2,3,4,5,6]])
runmany('INSERT INTO active_feb VALUES (?)', [(i,) for i in [2,3,4,5,7,8]])
runmany('INSERT INTO active_mar VALUES (?)', [(i,) for i in [3,4,5,6,8,9]])

# 1. All 3 months
rows = run('''
    SELECT user_id FROM active_jan
    INTERSECT SELECT user_id FROM active_feb
    INTERSECT SELECT user_id FROM active_mar
''')
print("Active all 3 months:", [r[0] for r in rows])

# 2. Jan but not Feb
rows = run('SELECT user_id FROM active_jan EXCEPT SELECT user_id FROM active_feb')
print("Jan but not Feb:", [r[0] for r in rows])

# 3. All unique
rows = run('''
    SELECT user_id FROM active_jan UNION
    SELECT user_id FROM active_feb UNION
    SELECT user_id FROM active_mar ORDER BY user_id
''')
print("All unique users:", [r[0] for r in rows])

# 4. TODO: Exactly 2 of 3 months
"""
)

# ── Section 22: Advanced CTEs ────────────────────────────────────────────────
s22 = make_sql(22, "Advanced CTEs & Chaining",
    "CTEs (WITH clauses) can be chained, referenced multiple times, and nested to build complex queries step by step. They replace temp tables in most cases and dramatically improve readability.",
    [
        {"label": "Multiple CTEs and chaining",
         "code": SETUP +
"""run('''CREATE TABLE transactions (id INT, cust_id INT, amount REAL, category TEXT, ts TEXT)''')
runmany('INSERT INTO transactions VALUES (?,?,?,?,?)', [
    (1,1,150,'food','2024-01-05'),(2,1,300,'tech','2024-01-10'),
    (3,2,200,'food','2024-01-08'),(4,2,100,'food','2024-01-12'),
    (5,3,500,'tech','2024-01-03'),(6,3,250,'clothing','2024-01-15'),
    (7,1,80,'food','2024-02-01'),(8,2,600,'tech','2024-02-05'),
    (9,3,120,'food','2024-02-10'),
])

rows = run('''
    WITH
    -- CTE 1: customer totals
    cust_totals AS (
        SELECT cust_id, SUM(amount) AS total_spend,
               COUNT(*) AS n_transactions, MAX(ts) AS last_purchase
        FROM transactions GROUP BY cust_id
    ),
    -- CTE 2: top category per customer
    top_cat AS (
        SELECT cust_id,
               category,
               SUM(amount) AS cat_total,
               ROW_NUMBER() OVER (PARTITION BY cust_id ORDER BY SUM(amount) DESC) AS rn
        FROM transactions GROUP BY cust_id, category
    ),
    -- CTE 3: combine using previous CTEs
    summary AS (
        SELECT ct.cust_id, ct.total_spend, ct.n_transactions, ct.last_purchase,
               tc.category AS top_category
        FROM cust_totals ct
        JOIN top_cat tc ON ct.cust_id = tc.cust_id AND tc.rn = 1
    )
    SELECT *, ROUND(total_spend / n_transactions, 2) AS avg_txn
    FROM summary ORDER BY total_spend DESC
''')
print("Customer summary:")
for r in rows:
    print(f"  Cust {r[0]}: ${r[1]} total, {r[2]} txns, top={r[4]}, avg=${r[5]}")"""},
        {"label": "Recursive CTE for hierarchies",
         "code": SETUP +
"""run('''CREATE TABLE org (id INT, name TEXT, manager_id INT, level INT)''')
runmany('INSERT INTO org VALUES (?,?,?,?)', [
    (1,'CEO',None,1),(2,'CTO',1,2),(3,'CFO',1,2),(4,'VP Eng',2,3),
    (5,'VP Data',2,3),(6,'Dir Finance',3,3),(7,'Sr Dev',4,4),
    (8,'Data Eng',5,4),(9,'Analyst',5,4),(10,'Accountant',6,4),
])

# Recursive CTE: traverse the org hierarchy
rows = run('''
    WITH RECURSIVE hierarchy AS (
        -- Base case: start from CEO (no manager)
        SELECT id, name, manager_id, 0 AS depth, name AS path
        FROM org WHERE manager_id IS NULL

        UNION ALL

        -- Recursive case: join to find reports
        SELECT o.id, o.name, o.manager_id,
               h.depth + 1,
               h.path || " -> " || o.name
        FROM org o
        JOIN hierarchy h ON o.manager_id = h.id
    )
    SELECT depth, name, path FROM hierarchy ORDER BY path
''')
for r in rows:
    indent = "  " * r[0]
    print(f"{indent}{r[1]}")

# Count reports under each manager
rows = run('''
    WITH RECURSIVE reports AS (
        SELECT id, manager_id FROM org
        UNION ALL
        SELECT r.id, o.manager_id FROM reports r JOIN org o ON o.id = r.manager_id
        WHERE o.manager_id IS NOT NULL
    )
    SELECT o.name, COUNT(*) AS total_reports
    FROM org o JOIN reports r ON r.manager_id = o.id
    GROUP BY o.id ORDER BY total_reports DESC LIMIT 5
''')
print("Managers by total reports:", [(r[0], r[1]) for r in rows])"""},
        {"label": "CTEs for multi-step data transformations",
         "code": SETUP +
"""run('''CREATE TABLE raw_sales (rep TEXT, product TEXT, amount REAL, region TEXT, sale_date TEXT)''')
import random; random.seed(42)
reps = ['Alice','Bob','Carol','Dave','Eve']
prods = ['Widget','Gadget','Gizmo']
regions = ['North','South','East']
rows_data = [(random.choice(reps), random.choice(prods),
              round(random.uniform(100,2000), 2),
              random.choice(regions),
              f"2024-0{random.randint(1,3)}-{random.randint(1,28):02d}")
             for _ in range(50)]
runmany('INSERT INTO raw_sales VALUES (?,?,?,?,?)', rows_data)

rows = run('''
    WITH
    -- Step 1: normalize and add month
    cleaned AS (
        SELECT rep, product, region, amount,
               STRFTIME("%Y-%m", sale_date) AS month
        FROM raw_sales WHERE amount > 0
    ),
    -- Step 2: rep-level monthly totals
    rep_monthly AS (
        SELECT rep, month, SUM(amount) AS monthly_total,
               COUNT(*) AS n_sales
        FROM cleaned GROUP BY rep, month
    ),
    -- Step 3: rank reps per month
    ranked AS (
        SELECT *, RANK() OVER (PARTITION BY month ORDER BY monthly_total DESC) AS rank
        FROM rep_monthly
    )
    -- Step 4: show top-2 per month
    SELECT month, rank, rep, ROUND(monthly_total, 0) AS total, n_sales
    FROM ranked WHERE rank <= 2
    ORDER BY month, rank
''')
print("Top 2 reps per month:")
for r in rows: print(f"  {r[0]} #{r[1]}: {r[2]} ${r[3]:,.0f} ({r[4]} sales)")"""}
    ],
    rw_title="Funnel Analysis",
    rw_scenario="A product team uses chained CTEs to compute a conversion funnel: impression -> click -> add_to_cart -> purchase, with drop-off rates at each stage.",
    rw_code= SETUP +
"""run('''CREATE TABLE funnel_events (user_id INT, event TEXT, ts TEXT)''')
import random; random.seed(42)
events_raw = []
for uid in range(1, 201):
    events_raw.append((uid,'impression','2024-01'))
    if random.random() < 0.6:   events_raw.append((uid,'click','2024-01'))
    if random.random() < 0.4:   events_raw.append((uid,'add_to_cart','2024-01'))
    if random.random() < 0.35:  events_raw.append((uid,'purchase','2024-01'))
runmany('INSERT INTO funnel_events VALUES (?,?,?)', events_raw)

rows = run('''
    WITH
    stage_counts AS (
        SELECT event,
               COUNT(DISTINCT user_id) AS users
        FROM funnel_events
        GROUP BY event
    ),
    ordered AS (
        SELECT event, users,
               CASE event
                   WHEN "impression"   THEN 1
                   WHEN "click"        THEN 2
                   WHEN "add_to_cart"  THEN 3
                   WHEN "purchase"     THEN 4
               END AS stage_order
        FROM stage_counts
    ),
    with_prev AS (
        SELECT event, users, stage_order,
               LAG(users) OVER (ORDER BY stage_order) AS prev_users
        FROM ordered
    )
    SELECT event, users,
           CASE WHEN prev_users IS NOT NULL
                THEN ROUND(100.0 * users / prev_users, 1)
                ELSE 100.0 END AS step_pct,
           ROUND(100.0 * users / MAX(users) OVER (), 1) AS overall_pct
    FROM with_prev ORDER BY stage_order
''')
print("Conversion funnel:")
for r in rows:
    bar = "#" * int(r[3] / 5)
    print(f"  {r[0]:15s}: {r[1]:>4d} users | step={r[2]:>5.1f}% | {bar}")""",
    pt="CTE Report Builder",
    pd_text="Build a multi-CTE query that: CTE1 computes monthly revenue per product from an orders table, CTE2 computes 3-month moving average per product (using LAG), CTE3 flags months where revenue dropped more than 20% vs the moving average. Return only flagged months with product, month, revenue, avg, and drop_pct.",
    ps=SETUP +
"""run('''CREATE TABLE monthly_orders (product TEXT, month TEXT, revenue REAL)''')
runmany('INSERT INTO monthly_orders VALUES (?,?,?)', [
    ('Widget','2024-01',1000),('Widget','2024-02',950),('Widget','2024-03',700),
    ('Widget','2024-04',980),('Gadget','2024-01',500),('Gadget','2024-02',520),
    ('Gadget','2024-03',480),('Gadget','2024-04',200),
])

rows = run('''
    WITH
    -- CTE2: 3-month moving average using LAG
    with_lags AS (
        SELECT product, month, revenue,
               LAG(revenue,1) OVER (PARTITION BY product ORDER BY month) AS prev1,
               LAG(revenue,2) OVER (PARTITION BY product ORDER BY month) AS prev2
        FROM monthly_orders
    ),
    moving_avg AS (
        SELECT product, month, revenue,
               ROUND((revenue + COALESCE(prev1,revenue) + COALESCE(prev2,revenue)) / 3.0, 1) AS ma3
        FROM with_lags
    ),
    -- CTE3: flag months with >20% drop vs moving avg
    flagged AS (
        SELECT product, month, revenue, ma3,
               ROUND((revenue - ma3) / ma3 * 100, 1) AS drop_pct
        FROM moving_avg
        WHERE revenue < ma3 * 0.8   -- more than 20% below MA
    )
    SELECT * FROM flagged ORDER BY drop_pct
''')
print("Revenue alerts (>20% below 3-month MA):")
for r in rows: print(f"  {r[0]} {r[1]}: ${r[2]} vs MA ${r[3]} ({r[4]}%)")
"""
)

# ── Section 23: Views & Database Objects ────────────────────────────────────
s23 = make_sql(23, "Views & Virtual Tables",
    "Views are saved SELECT statements that behave like tables. They simplify complex queries, enforce access control, and create stable interfaces over evolving schema.",
    [
        {"label": "Creating and using views",
         "code": SETUP +
"""run('''CREATE TABLE employees (id INT, name TEXT, dept TEXT, salary REAL, hire_date TEXT)''')
run('''CREATE TABLE departments (id INT, name TEXT, budget REAL)''')
runmany('INSERT INTO employees VALUES (?,?,?,?,?)', [
    (1,'Alice','Eng',90000,'2020-03-15'),(2,'Bob','Eng',85000,'2021-06-01'),
    (3,'Carol','Sales',70000,'2019-11-20'),(4,'Dave','Sales',72000,'2022-01-10'),
    (5,'Eve','HR',65000,'2020-08-05'),(6,'Frank','Eng',95000,'2018-04-22'),
])
runmany('INSERT INTO departments VALUES (?,?,?)', [
    (1,'Eng',500000),(2,'Sales',300000),(3,'HR',150000),
])

# Create a view
run('''
    CREATE VIEW emp_summary AS
    SELECT e.id, e.name, e.dept, e.salary,
           ROUND(100.0 * e.salary / d.budget, 2) AS salary_pct_budget,
           CAST((JULIANDAY("now") - JULIANDAY(e.hire_date)) / 365.25 AS INT) AS years
    FROM employees e
    JOIN departments d ON e.dept = d.name
''')

# Query the view like a table
rows = run('SELECT * FROM emp_summary ORDER BY salary DESC')
print("Employee summary (from view):")
for r in rows: print(f"  {r[1]} ({r[2]}): ${r[3]:,}, {r[4]:.2f}% of dept budget, {r[5]} yrs")

# View within query
rows = run('''
    SELECT dept, COUNT(*) AS n, ROUND(AVG(salary), 0) AS avg_sal
    FROM emp_summary
    GROUP BY dept ORDER BY avg_sal DESC
''')
for r in rows: print(f"  {r[0]}: {r[1]} employees, avg ${r[2]:,}")"""},
        {"label": "View updates and DROP",
         "code": SETUP +
"""run('''CREATE TABLE products (id INT, name TEXT, price REAL, active INT DEFAULT 1)''')
runmany('INSERT INTO products VALUES (?,?,?,?)', [
    (1,'Apple',1.2,1),(2,'Banana',0.5,1),(3,'Carrot',0.8,0),(4,'Date',2.0,1),
])

run('''CREATE VIEW active_products AS
       SELECT id, name, price FROM products WHERE active = 1''')

rows = run('SELECT * FROM active_products')
print("Active products:", rows)

# In SQLite, simple views can be updated using INSTEAD OF triggers
# But directly: INSERT INTO simple single-table view may work
run("INSERT INTO active_products VALUES (5, 'Elderberry', 3.5)")
rows = run('SELECT id, name, price, active FROM products WHERE id = 5')
print("Inserted via view:", rows)  # active defaults to 1

# DROP VIEW
run('DROP VIEW active_products')
print("View dropped. Tables unaffected.")
rows = run('SELECT COUNT(*) FROM products')
print("Products table still has:", rows[0][0], "rows")"""},
        {"label": "Materialized views (via tables) and virtual tables",
         "code": SETUP +
"""# SQLite doesn't have native materialized views
# Simulate with CREATE TABLE AS SELECT
run('''CREATE TABLE employees (id INT, dept TEXT, salary REAL)''')
runmany('INSERT INTO employees VALUES (?,?,?)', [
    (i, ['Eng','Sales','HR'][i%3], 60000 + i*5000) for i in range(12)
])

# Simulated materialized view (refresh manually)
run('''DROP TABLE IF EXISTS dept_stats_mv''')
run('''
    CREATE TABLE dept_stats_mv AS
    SELECT dept,
           COUNT(*) AS headcount,
           ROUND(AVG(salary), 0) AS avg_salary,
           MAX(salary) AS max_salary
    FROM employees GROUP BY dept
''')

rows = run('SELECT * FROM dept_stats_mv ORDER BY avg_salary DESC')
print("Materialized dept stats:")
for r in rows: print(f"  {r[0]}: {r[1]} people, avg ${r[2]:,}, max ${r[3]:,}")

# Refresh: insert more data, recreate
run('INSERT INTO employees VALUES (99, "Eng", 200000)')
run('DROP TABLE dept_stats_mv')
run('''
    CREATE TABLE dept_stats_mv AS
    SELECT dept, COUNT(*) AS headcount, ROUND(AVG(salary),0) AS avg_salary
    FROM employees GROUP BY dept
''')
rows = run('SELECT * FROM dept_stats_mv ORDER BY dept')
print("Refreshed stats:", rows)"""}
    ],
    rw_title="Reporting View Layer",
    rw_scenario="A BI team creates views for sales, customer, and product reporting so analysts never need to write complex JOINs — they just query well-named views.",
    rw_code= SETUP +
"""run('''CREATE TABLE orders (id INT, cust_id INT, product_id INT, amount REAL, order_date TEXT)''')
run('''CREATE TABLE customers (id INT, name TEXT, tier TEXT, region TEXT)''')
run('''CREATE TABLE products (id INT, name TEXT, category TEXT, cost REAL)''')
runmany('INSERT INTO orders VALUES (?,?,?,?,?)', [
    (1,1,1,500,'2024-01-10'),(2,1,2,300,'2024-01-15'),(3,2,1,800,'2024-02-05'),
    (4,2,3,200,'2024-02-20'),(5,3,2,600,'2024-03-01'),(6,1,3,400,'2024-03-10'),
])
runmany('INSERT INTO customers VALUES (?,?,?,?)', [
    (1,'Alice','gold','North'),(2,'Bob','silver','South'),(3,'Carol','bronze','East'),
])
runmany('INSERT INTO products VALUES (?,?,?,?)', [
    (1,'Widget','Hardware',200),(2,'Gadget','Electronics',100),(3,'Gizmo','Software',50),
])

run('''CREATE VIEW order_detail AS
    SELECT o.id AS order_id, c.name AS customer, c.tier, c.region,
           p.name AS product, p.category,
           o.amount, p.cost,
           ROUND(o.amount - p.cost, 2) AS margin,
           ROUND((o.amount - p.cost) / o.amount * 100, 1) AS margin_pct,
           o.order_date
    FROM orders o
    JOIN customers c ON c.id = o.cust_id
    JOIN products p ON p.id = o.product_id
''')

rows = run('SELECT customer, product, amount, margin_pct FROM order_detail ORDER BY margin_pct DESC')
print("Order detail (from view):")
for r in rows: print(f"  {r[0]} - {r[1]}: ${r[2]} ({r[3]}% margin)")

rows = run('SELECT category, ROUND(AVG(margin_pct),1) AS avg_margin FROM order_detail GROUP BY category')
print("Avg margin by category:", rows)""",
    pt="View-Based Dashboard",
    pd_text="Create a sales table (id, rep, product, amount, region, sale_date). Create: (1) A view rep_dashboard with each rep's total, count, avg, and rank. (2) A view regional_summary with region totals and % of grand total. (3) A view top_products showing the top 5 products by revenue. Query each view to confirm it works.",
    ps=SETUP +
"""run('''CREATE TABLE sales (id INT, rep TEXT, product TEXT, amount REAL, region TEXT, sale_date TEXT)''')
runmany('INSERT INTO sales VALUES (?,?,?,?,?,?)', [
    (1,'Alice','Widget',500,'North','2024-01-10'),
    (2,'Alice','Gadget',300,'North','2024-01-15'),
    (3,'Bob','Widget',800,'South','2024-02-01'),
    (4,'Bob','Gizmo',200,'South','2024-02-10'),
    (5,'Carol','Gadget',600,'East','2024-02-20'),
    (6,'Alice','Gizmo',400,'North','2024-03-01'),
    (7,'Carol','Widget',700,'East','2024-03-10'),
    (8,'Bob','Gadget',350,'South','2024-03-15'),
])

# 1. Rep dashboard view
run('''CREATE VIEW rep_dashboard AS
    SELECT rep, SUM(amount) AS total, COUNT(*) AS n_sales,
           ROUND(AVG(amount),0) AS avg_sale,
           RANK() OVER (ORDER BY SUM(amount) DESC) AS rank
    FROM sales GROUP BY rep
''')
print("=== Rep Dashboard ===")
for r in run('SELECT * FROM rep_dashboard ORDER BY rank'): print(f"  {r}")

# 2. Regional summary view
run('''CREATE VIEW regional_summary AS
    SELECT region, ROUND(SUM(amount),0) AS total,
           ROUND(100.0*SUM(amount)/SUM(SUM(amount)) OVER (), 1) AS pct_of_total
    FROM sales GROUP BY region
''')
print("=== Regional Summary ===")
for r in run('SELECT * FROM regional_summary ORDER BY total DESC'): print(f"  {r}")

# 3. TODO: top products view
"""
)

# ── Section 24: Data Integrity & Constraints ─────────────────────────────────
s24 = make_sql(24, "Data Integrity & Constraints",
    "Constraints (PRIMARY KEY, UNIQUE, NOT NULL, CHECK, FOREIGN KEY) enforce data quality at the database level — the last line of defense against bad data.",
    [
        {"label": "PRIMARY KEY, UNIQUE, NOT NULL, CHECK",
         "code": SETUP +
"""conn.execute('PRAGMA foreign_keys = ON')

run('''CREATE TABLE products (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    sku     TEXT    NOT NULL UNIQUE,
    name    TEXT    NOT NULL,
    price   REAL    NOT NULL CHECK (price > 0),
    stock   INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    category TEXT   CHECK (category IN ("food", "tech", "clothing"))
)''')

# Valid insert
run("INSERT INTO products (sku, name, price, stock, category) VALUES ('SKU-001', 'Apple', 1.5, 100, 'food')")
run("INSERT INTO products (sku, name, price, stock, category) VALUES ('SKU-002', 'Phone', 699.0, 50, 'tech')")
print("Inserted valid products:", run('SELECT id, sku, name, price FROM products'))

# Test constraint violations
import sqlite3 as _sqlite3
tests = [
    ("Duplicate SKU",       "INSERT INTO products (sku, name, price) VALUES ('SKU-001', 'Pear', 0.9)"),
    ("Negative price",      "INSERT INTO products (sku, name, price) VALUES ('SKU-003', 'X', -5.0)"),
    ("Negative stock",      "INSERT INTO products (sku, name, price, stock) VALUES ('SKU-004', 'Y', 1.0, -10)"),
    ("Invalid category",    "INSERT INTO products (sku, name, price, category) VALUES ('SKU-005', 'Z', 2.0, 'toys')"),
    ("NULL name",           "INSERT INTO products (sku, price) VALUES ('SKU-006', 3.0)"),
]
for label, sql in tests:
    try:
        run(sql)
        print(f"  FAIL: {label} should have been rejected!")
    except Exception as e:
        print(f"  OK: {label} rejected -> {str(e)[:50]}")"""},
        {"label": "FOREIGN KEY constraints",
         "code": SETUP +
"""conn.execute('PRAGMA foreign_keys = ON')
run('''CREATE TABLE categories (id INT PRIMARY KEY, name TEXT NOT NULL UNIQUE)''')
run('''CREATE TABLE products (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    cat_id INT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT ON UPDATE CASCADE
)''')
run('''CREATE TABLE orders (
    id INT PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE
)''')

runmany('INSERT INTO categories VALUES (?,?)', [(1,'Food'),(2,'Tech'),(3,'Clothing')])
runmany('INSERT INTO products VALUES (?,?,?)', [(1,'Apple',1),(2,'Phone',2),(3,'Shirt',3)])
runmany('INSERT INTO orders VALUES (?,?)', [(1,1),(2,1),(3,2)])

# Violate FK
import sqlite3 as _sqlite3
try:
    run('INSERT INTO products VALUES (4, "Widget", 99)')   # cat_id=99 doesn't exist
    print("FAIL: should have rejected")
except Exception as e:
    print("OK: FK rejected:", str(e)[:50])

# ON DELETE CASCADE: delete product -> orders cascade deleted
print("Orders before:", run('SELECT COUNT(*) FROM orders')[0][0])
run('DELETE FROM products WHERE id = 1')
print("Orders after deleting product 1:", run('SELECT COUNT(*) FROM orders')[0][0])

# ON DELETE RESTRICT: cannot delete category if products reference it
try:
    run('DELETE FROM categories WHERE id = 2')
    print("FAIL: should have rejected")
except Exception as e:
    print("OK: RESTRICT works:", str(e)[:50])"""},
        {"label": "ON CONFLICT and UPSERT",
         "code": SETUP +
"""run('''CREATE TABLE inventory (
    sku   TEXT PRIMARY KEY,
    name  TEXT NOT NULL,
    stock INT  NOT NULL DEFAULT 0 CHECK (stock >= 0)
)''')
runmany('INSERT INTO inventory VALUES (?,?,?)', [
    ('A001','Apple',100),('B002','Banana',200),
])

# ON CONFLICT IGNORE: skip duplicate inserts silently
run("INSERT OR IGNORE INTO inventory VALUES ('A001', 'Apple Updated', 150)")
print("After OR IGNORE:", run("SELECT stock FROM inventory WHERE sku='A001'")[0][0])  # still 100

# ON CONFLICT REPLACE: delete + re-insert
run("INSERT OR REPLACE INTO inventory VALUES ('A001', 'Apple Premium', 120)")
print("After OR REPLACE:", run("SELECT name, stock FROM inventory WHERE sku='A001'")[0])

# UPSERT (INSERT ... ON CONFLICT DO UPDATE) - SQLite 3.24+
run('''
    INSERT INTO inventory (sku, name, stock) VALUES ("C003", "Cherry", 50)
    ON CONFLICT(sku) DO UPDATE SET
        stock = stock + excluded.stock,
        name  = excluded.name
''')
run('''
    INSERT INTO inventory (sku, name, stock) VALUES ("C003", "Cherry Deluxe", 30)
    ON CONFLICT(sku) DO UPDATE SET
        stock = stock + excluded.stock,
        name  = excluded.name
''')
print("After UPSERT x2:", run("SELECT name, stock FROM inventory WHERE sku='C003'")[0])"""}
    ],
    rw_title="Inventory Management System",
    rw_scenario="An e-commerce warehouse uses FK constraints, CHECK constraints, and UPSERT to maintain data integrity across products, stock levels, and order fulfillment.",
    rw_code= SETUP +
"""conn.execute('PRAGMA foreign_keys = ON')
run('''CREATE TABLE warehouses (id INT PRIMARY KEY, location TEXT)''')
run('''CREATE TABLE products (id INT PRIMARY KEY, sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL, price REAL CHECK (price > 0))''')
run('''CREATE TABLE stock_levels (
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    warehouse_id INT REFERENCES warehouses(id),
    qty INT NOT NULL DEFAULT 0 CHECK (qty >= 0),
    PRIMARY KEY (product_id, warehouse_id)
)''')

runmany('INSERT INTO warehouses VALUES (?,?)', [(1,'NYC'),(2,'LA'),(3,'Chicago')])
runmany('INSERT INTO products VALUES (?,?,?,?)',
        [(1,'SKU-A','Widget',29.99),(2,'SKU-B','Gadget',49.99)])
runmany('INSERT INTO stock_levels VALUES (?,?,?)',
        [(1,1,500),(1,2,300),(2,1,200),(2,3,150)])

# UPSERT stock: add received quantity
def receive_stock(product_id, warehouse_id, qty):
    run(f'''
        INSERT INTO stock_levels (product_id, warehouse_id, qty)
        VALUES ({product_id}, {warehouse_id}, {qty})
        ON CONFLICT (product_id, warehouse_id) DO UPDATE SET qty = qty + {qty}
    ''')

receive_stock(1, 1, 100)
receive_stock(2, 2, 50)  # new location

rows = run('''
    SELECT p.name, w.location, sl.qty
    FROM stock_levels sl
    JOIN products p ON p.id = sl.product_id
    JOIN warehouses w ON w.id = sl.warehouse_id
    ORDER BY p.name, sl.qty DESC
''')
print("Current stock:")
for r in rows: print(f"  {r[0]} @ {r[1]}: {r[2]} units")""",
    pt="Bank Account Constraints",
    pd_text="Create an accounts table (id, holder, balance REAL CHECK >= 0, account_type CHECK IN list, opened_date). Create a transactions table (id, account_id FK, amount, type CHECK IN debit/credit, ts). Write: (1) Insert a debit that would go negative (should fail). (2) A trigger that auto-updates balance on transaction insert. (3) UPSERT to create or update account balance.",
    ps=SETUP +
"""conn.execute('PRAGMA foreign_keys = ON')
run('''CREATE TABLE accounts (
    id INT PRIMARY KEY,
    holder TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0 CHECK (balance >= 0),
    account_type TEXT CHECK (account_type IN ("checking", "savings")),
    opened_date TEXT DEFAULT (DATE("now"))
)''')
run('''CREATE TABLE txns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INT NOT NULL REFERENCES accounts(id),
    amount REAL NOT NULL CHECK (amount > 0),
    type TEXT NOT NULL CHECK (type IN ("debit","credit")),
    ts TEXT DEFAULT (DATETIME("now"))
)''')

run("INSERT INTO accounts VALUES (1,'Alice',1000,'checking','2024-01-01')")

# 1. Try to go negative via debit > balance
import sqlite3 as _sqlite3
try:
    run("INSERT INTO txns (account_id, amount, type) VALUES (1, 5000, 'debit')")
    # Without trigger, balance isn't auto-updated. Add trigger below.
except Exception as e:
    print("Error:", e)

# 2. TODO: CREATE TRIGGER after_txn AFTER INSERT ON txns
#    that updates accounts.balance = balance - amount WHERE type='debit'
#    or balance + amount WHERE type='credit'

# 3. TODO: UPSERT to create or update an account balance
print("Current balance:", run("SELECT balance FROM accounts WHERE id=1")[0][0])
"""
)

# ── Assemble and insert ──────────────────────────────────────────────────────
all_sections = s17 + s18 + s19 + s20 + s21 + s22 + s23 + s24
result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: sql sections 17-24 added")
else:
    print("FAILED")
