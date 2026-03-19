#!/usr/bin/env python3
"""Generate Python Basics study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\00_python_basics")
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
        cards += (
            f'<div class="topic" id="s{i}">'
            f'<div class="th" onclick="tog(this)"><span>{esc(s["title"])}</span>'
            f'<span class="arr">&#9660;</span></div>'
            f'<div class="tb"><p class="desc">{esc(s.get("desc",""))}</p>'
            f'{blks}{rw_html}{practice_html}</div></div>'
        )
    n = len(sections)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Python Basics Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{{--bg:#0f1117;--sb:#161b22;--card:#1c2128;--brd:#30363d;--txt:#c9d1d9;--mut:#8b949e;--acc:#ffa657}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{display:flex;min-height:100vh;background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px}}
.sidebar{{width:260px;min-height:100vh;background:var(--sb);border-right:1px solid var(--brd);position:sticky;top:0;height:100vh;overflow-y:auto;flex-shrink:0}}
.sbh{{padding:20px;border-bottom:1px solid var(--brd)}}
.sbh h2{{font-size:1.05rem;color:var(--acc)}}
.sbh p{{font-size:.8rem;color:var(--mut);margin-top:3px}}
#q{{width:100%;padding:7px 10px;background:#0d1117;border:1px solid var(--brd);border-radius:6px;color:var(--txt);font-size:.84rem;margin-top:10px}}
#q:focus{{outline:none;border-color:var(--acc)}}
.nav-list{{list-style:none;padding:6px 0}}
.nav-list li a{{display:block;padding:7px 18px;color:var(--mut);text-decoration:none;font-size:.84rem;border-left:3px solid transparent;transition:.15s}}
.nav-list li a:hover,.nav-list li a.active{{color:var(--txt);border-left-color:var(--acc);background:rgba(255,255,255,.03)}}
.main{{flex:1;padding:32px 40px;max-width:880px}}
.pt{{font-size:2rem;font-weight:700;color:var(--acc);margin-bottom:6px}}
.ps{{color:var(--mut);margin-bottom:28px}}
.topic{{background:var(--card);border:1px solid var(--brd);border-radius:8px;margin-bottom:14px;overflow:hidden}}
.th{{display:flex;justify-content:space-between;align-items:center;padding:13px 18px;cursor:pointer;user-select:none}}
.th:hover{{background:rgba(255,255,255,.04)}}
.th>span:first-child{{font-weight:600}}
.arr{{color:var(--mut);transition:transform .2s}}
.tb{{display:none;padding:18px;border-top:1px solid var(--brd)}}
.tb.open{{display:block}}
.arr.open{{transform:rotate(180deg)}}
.desc{{color:var(--mut);margin-bottom:14px;line-height:1.6;font-size:.92rem}}
.code-block{{margin-bottom:14px;border:1px solid var(--brd);border-radius:6px;overflow:hidden}}
.ch{{display:flex;justify-content:space-between;padding:7px 12px;background:#161b22;font-size:.78rem;color:var(--mut)}}
.ch button{{background:0;border:1px solid var(--brd);color:var(--mut);padding:2px 9px;border-radius:4px;cursor:pointer;font-size:.73rem}}
.ch button:hover{{color:var(--txt);border-color:var(--acc)}}
pre{{margin:0}}pre code{{font-size:.83rem;padding:13px!important}}
.rw{{background:#0d2818;border:1px solid #238636;border-radius:6px;padding:15px;margin-top:6px}}
.rh{{font-weight:600;color:#3fb950;margin-bottom:7px}}
.rd{{color:#7ee787;font-size:.84rem;margin-bottom:11px;line-height:1.5}}
.practice{{background:#0d1b2a;border:1px solid #388bfd;border-radius:6px;padding:15px;margin-top:8px}}
.ph{{font-weight:600;color:#58a6ff;margin-bottom:7px}}
.pd{{color:#79c0ff;font-size:.84rem;margin-bottom:11px;line-height:1.5}}
</style></head><body>
<aside class="sidebar">
  <div class="sbh"><h2>🐍 Python Basics</h2><p>Study Guide &bull; {n} topics</p>
    <input id="q" placeholder="Search..." oninput="filt(this.value)">
  </div>
  <ul class="nav-list" id="nl">{nav}</ul>
</aside>
<main class="main">
  <h1 class="pt">🐍 Python Basics</h1>
  <p class="ps">{n} topics &bull; Click any card to expand</p>
  {cards}
</main>
<script>
hljs.highlightAll();
function tog(h){{var b=h.nextElementSibling,a=h.querySelector('.arr');b.classList.toggle('open');a.classList.toggle('open');}}
function act(el,e){{if(e)e.preventDefault();document.querySelectorAll('.nav-list a').forEach(a=>a.classList.remove('active'));el.classList.add('active');}}
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

    cells.append(md("# Python Basics Study Guide\n\nA hands-on guide covering all essential Python concepts with real-world examples."))
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
            cells.append(md(f"### 🏋️ Practice: {practice['title']}\n\n{practice['desc']}"))
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
"title": "1. Variables & Data Types",
"desc": "Python is dynamically typed — you don't declare types, Python infers them. The core types are int, float, str, bool, and NoneType.",
"examples": [
{"label": "Basic types and type checking", "code":
"""# Integers
age    = 25
year   = 2024

# Floats
price  = 9.99
pi     = 3.14159

# String
name   = "Alice"

# Boolean
active = True
done   = False

# NoneType
result = None

# Check types
print(type(age))       # <class 'int'>
print(type(price))     # <class 'float'>
print(type(name))      # <class 'str'>
print(type(active))    # <class 'bool'>
print(type(result))    # <class 'NoneType'>"""},
{"label": "Type conversion (casting)", "code":
"""# Convert between types
x = "42"
print(int(x) + 8)          # 50  (str → int)
print(float(x) * 1.5)      # 63.0

n = 3.9
print(int(n))              # 3   (truncates, not rounds)
print(round(n))            # 4   (rounds)

print(str(100) + " items") # "100 items"
print(bool(0))             # False
print(bool(""))            # False
print(bool("hello"))       # True
print(bool(42))            # True"""},
{"label": "Multiple assignment and augmented operators", "code":
"""# Multiple assignment
a, b, c = 10, 20, 30
x = y = z = 0
print(a, b, c)   # 10 20 30
print(x, y, z)   # 0 0 0

# Swap without temp variable
a, b = b, a
print(a, b)      # 20 10

# Augmented assignment operators
score = 100
score += 15    # 115
score -= 5     # 110
score *= 2     # 220
score //= 3    # 73
score **= 2    # 5329
print("Score:", score)

# Readable large numbers
population = 8_100_000_000
pi_approx  = 3.141_592_653
print(f"Population: {population:,}")"""},
{"label": "Complex numbers, None checks, and type introspection", "code":
"""# Complex numbers
z1 = 3 + 4j
z2 = complex(1, -2)
print(f"z1 = {z1},  real={z1.real}, imag={z1.imag}")
print(f"|z1| = {abs(z1)}")          # magnitude: 5.0
print(f"z1 + z2 = {z1 + z2}")
print(f"z1 * z2 = {z1 * z2}")

# None checks — always use 'is' / 'is not', never ==
result = None
if result is None:
    print("result is None")

data = [0, "", None, False, 42, "hello"]
for item in data:
    falsy = "falsy" if not item else "truthy"
    none_check = " (is None)" if item is None else ""
    print(f"  {str(item):8s} -> {falsy}{none_check}")

# isinstance — safer than type() ==
values = [42, 3.14, "hi", True, None, [1,2]]
for v in values:
    print(f"  {str(v):8s}  int={isinstance(v, int)}  "
          f"float={isinstance(v, float)}  str={isinstance(v, str)}")"""}
],
"practice": {
"title": "Variable Juggling",
"desc": "Create name (str), age (int), height (float). Swap age and height using tuple unpacking. Check if original age is between 18 and 65 (inclusive). Print a formatted f-string summary.",
"starter":
"""name   = "YOUR_NAME"
age    = 25          # set your age
height = 1.75        # set height in meters

# TODO: swap age and height using one line
# age, height = ???

# TODO: check if the original age (now stored in height) is 18-65
is_working_age = ???

# Expected: "Alice | Age: 1.75 | Height: 25m | Working age: True"
print(f"{name} | Age: {age} | Height: {height}m | Working age: {is_working_age}")"""
},
"rw": {
"title": "User Input Validation",
"scenario": "A CLI app reads user input and converts it to the correct type before processing.",
"code":
"""# Simulating user input processing
def parse_order(quantity_str, price_str, discount_str):
    try:
        quantity = int(quantity_str)
        price    = float(price_str)
        discount = float(discount_str) / 100
    except ValueError as e:
        return f"Invalid input: {e}"

    subtotal = quantity * price
    total    = subtotal * (1 - discount)
    return {
        "quantity": quantity,
        "price":    price,
        "discount": f"{discount:.0%}",
        "total":    round(total, 2)
    }

print(parse_order("3", "29.99", "10"))
print(parse_order("abc", "9.99", "5"))"""}
},

{
"title": "2. Strings",
"desc": "Strings are sequences of characters. Python provides rich built-in methods for slicing, formatting, searching, and transforming text.",
"examples": [
{"label": "String methods and slicing", "code":
"""text = "  Hello, World!  "

print(text.strip())           # remove whitespace
print(text.lower())           # lowercase
print(text.upper())           # uppercase
print(text.replace("World", "Python"))
print(text.strip().split(", "))  # ['Hello', 'World!']

# Slicing
s = "Python"
print(s[0])      # P
print(s[-1])     # n
print(s[1:4])    # yth
print(s[::-1])   # nohtyP  (reverse)
print(len(s))    # 6"""},
{"label": "f-strings and formatting", "code":
"""name  = "Alice"
score = 98.567
rank  = 1

# f-string (recommended)
print(f"Name: {name}, Score: {score:.2f}, Rank: #{rank}")

# Padding and alignment
for item, price in [("Apple", 0.5), ("Banana", 0.25), ("Cherry", 1.99)]:
    print(f"{item:<10} ${price:>6.2f}")

# Multi-line string
message = (
    f"Congratulations {name}!\n"
    f"Your score of {score:.1f} earned rank #{rank}."
)
print(message)"""},
{"label": "String searching, splitting, and joining", "code":
"""sentence = "Python is powerful, Python is readable, Python is fun"

print(sentence.count("Python"))       # 3
print(sentence.find("readable"))      # index of first match
print(sentence.startswith("Python"))  # True
print(sentence.endswith("fun"))       # True

# Split and join
parts    = sentence.split(", ")
rejoined = " | ".join(parts)
print(rejoined)

# strip variants
messy = "   hello world   "
print(repr(messy.strip()))    # 'hello world'

# partition — splits at first match only
before, sep, after = sentence.partition(" is ")
print(f"Before: '{before}'")
print(f"After:  '{after[:30]}...'")

# replace with count limit
print(sentence.replace("Python", "Ruby", 1))  # only first"""},
{"label": "f-string advanced: format spec, alignment, padding, expressions", "code":
"""import math

# Format spec: [[fill]align][sign][width][grouping][.precision][type]
pi = math.pi
print(f"{'pi':>12s}: {pi:>12.6f}")      # right-align, 6 decimals
print(f"{'pi':>12s}: {pi:>12.4e}")      # scientific notation
print(f"{'pi':>12s}: {pi:>12.2%}")      # as percentage

# Table with column alignment
header = f"{'Name':<15} {'Score':>8} {'Grade':>6} {'Bar':}"
print(header)
print("-" * 45)
students = [("Alice", 92.5), ("Bob", 74.3), ("Carol Marie", 88.0)]
for name, score in students:
    grade = "A" if score >= 90 else "B" if score >= 80 else "C"
    bar   = "#" * int(score // 10)
    print(f"{name:<15} {score:>8.1f} {grade:>6}  {bar}")

# Nested expressions inside f-strings
items = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"max={max(items)}, sum={sum(items)}, avg={sum(items)/len(items):.2f}")

# Debug format (Python 3.8+): variable=value
x = 42
print(f"{x=}, {x**2=}, {math.sqrt(x)=:.4f}")"""}
],
"practice": {
"title": "String Cleaning Pipeline",
"desc": "Given raw = '  super-pro Widget X200  ', clean it: strip whitespace, title-case it, replace hyphens with spaces, check if 'pro' appears (case-insensitive), and build a 6-char product code from the first 3 + last 3 chars (no spaces) uppercased.",
"starter":
"""raw = "  super-pro Widget X200  "

# 1. Strip whitespace and title-case
clean = raw.strip().title()

# 2. TODO: Replace hyphens with spaces
# clean = clean.replace(???)

# 3. TODO: Check 'pro' in original string (case-insensitive)
# has_pro = "pro" in raw.???()

# 4. TODO: Build 6-char code: first 3 + last 3 of clean (no spaces), uppercase
# no_spaces = clean.replace(" ", "")
# code = (no_spaces[:3] + ???).upper()

print(f"Clean: '{clean}'")
# print(f"Has pro: {has_pro}")
# print(f"Code: '{code}'")
# Expected: Clean='Super Pro Widget X200', Code='SUP200'"""
},
"rw": {
"title": "Log File Parser",
"scenario": "A DevOps engineer parses and formats structured log messages from an application server.",
"code":
"""import datetime

logs = [
    "[2024-01-15 09:23:11] ERROR   login_service: Invalid credentials for user bob@example.com",
    "[2024-01-15 09:24:55] INFO    auth_service:  Token issued for alice@example.com",
    "[2024-01-15 09:25:03] WARNING api_gateway:   Rate limit 80% for IP 192.168.1.42",
]

print(f"{'Time':9s} {'Level':8s} {'Service':15s} {'Message'}")
print("-" * 65)
for log in logs:
    # Parse: [datetime] LEVEL  service: message
    ts      = log[1:20]
    rest    = log[22:].strip()
    parts   = rest.split(None, 2)
    level   = parts[0]
    service = parts[1].rstrip(":")
    msg     = parts[2] if len(parts) > 2 else ""
    print(f"{ts[11:]:9s} {level:8s} {service:15s} {msg}")"""}
},

{
"title": "3. Lists",
"desc": "Lists are ordered, mutable sequences. They're the most commonly used Python container — used for collections, stacks, queues, and more.",
"examples": [
{"label": "Creating, accessing, modifying", "code":
"""fruits = ["apple", "banana", "cherry", "date"]

print(fruits[0])          # apple
print(fruits[-1])         # date
print(fruits[1:3])        # ['banana', 'cherry']

# Modify
fruits.append("elderberry")     # add to end
fruits.insert(1, "avocado")     # insert at index 1
fruits.remove("banana")         # remove by value
popped = fruits.pop()           # remove & return last
print(fruits)
print("Popped:", popped)
print("Length:", len(fruits))"""},
{"label": "List methods and list comprehension", "code":
"""nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

nums.sort()
print("Sorted:", nums)
print("Reversed:", nums[::-1])
print("Count of 5:", nums.count(5))
print("Index of 9:", nums.index(9))
print("Sum:", sum(nums))
print("Max:", max(nums), "Min:", min(nums))

# List comprehension
squares  = [x**2 for x in range(1, 6)]
evens    = [x for x in range(20) if x % 2 == 0]
print("Squares:", squares)
print("Evens:", evens)"""},
{"label": "Nested lists, map, filter, and any/all", "code":
"""# Nested list (2D matrix)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("Center:", matrix[1][1])   # 5

# Flatten nested list
flat = [x for row in matrix for x in row]
print("Flat:", flat)

# Transpose with comprehension
transposed = [[matrix[r][c] for r in range(3)] for c in range(3)]
print("Transposed[0]:", transposed[0])

# map and filter
nums = [1, -2, 3, -4, 5, -6]
doubled   = list(map(lambda x: x * 2, nums))
positives = list(filter(lambda x: x > 0, nums))
print("Doubled:  ", doubled)
print("Positives:", positives)

# any / all
print("any > 4:", any(x > 4 for x in nums))
print("all > 0:", all(x > 0 for x in nums))"""},
{"label": "sort vs sorted, key=, reverse, and bisect for sorted insertion", "code":
"""import bisect

# sort() mutates in place; sorted() returns a new list
nums = [5, 2, 8, 1, 9, 3]
new_sorted = sorted(nums)           # original unchanged
nums.sort()                         # in-place
print("sorted():", new_sorted)
print("sort() in-place:", nums)

# key= — sort by custom criteria
words = ["banana", "Apple", "cherry", "date", "FIG"]
print(sorted(words))                          # case-sensitive lexicographic
print(sorted(words, key=str.lower))           # case-insensitive
print(sorted(words, key=len))                 # by length
print(sorted(words, key=lambda w: (-len(w), w.lower())))  # len desc, alpha asc

# Sorting tuples: sort by 2nd element desc, then 1st asc
people = [("Bob",25), ("Alice",30), ("Carol",25), ("Dave",30)]
print(sorted(people, key=lambda p: (-p[1], p[0])))

# bisect — fast insertion point in a sorted list (binary search)
scores = [45, 58, 67, 74, 82, 88, 95]
new_score = 79
pos = bisect.bisect_left(scores, new_score)
bisect.insort(scores, new_score)   # inserts in sorted order
print(f"Inserted {new_score} at index {pos}: {scores}")
print(f"Rank from top: {len(scores) - pos} of {len(scores)}")"""}
],
"practice": {
"title": "Temperature Converter",
"desc": "Given temps_c = [22.5, 35.1, 18.0, 40.2, 28.7, 15.3, 33.8, 25.0], convert all to Fahrenheit (F = C*9/5+32) using a list comprehension. Filter hot days (>30°C). Sort descending. Find the min and max.",
"starter":
"""temps_c = [22.5, 35.1, 18.0, 40.2, 28.7, 15.3, 33.8, 25.0]

# 1. TODO: Convert to Fahrenheit using list comprehension
# temps_f = [??? for t in temps_c]

# 2. TODO: Filter days above 30°C
# hot_days = [??? for t in temps_c if ???]

# 3. TODO: Sort temps_c descending
# sorted_desc = sorted(???, reverse=True)

# 4. TODO: Min and max
# lo, hi = min(temps_c), max(temps_c)

print("Fahrenheit:", [round(f, 1) for f in temps_f])
print("Hot days:", sorted(hot_days))
print("Sorted desc:", sorted_desc)
print(f"Range: {lo}°C — {hi}°C")"""
},
"rw": {
"title": "Student Grade Processor",
"scenario": "A teacher processes a class grade list: compute stats, filter failing students, and build a ranking.",
"code":
"""students = [
    ("Alice", 92), ("Bob", 74), ("Carol", 88),
    ("Dave", 51), ("Eve", 96), ("Frank", 63),
    ("Grace", 85), ("Hank", 47), ("Iris", 79),
]

scores = [s[1] for s in students]
avg    = sum(scores) / len(scores)

passing = [(n, s) for n, s in students if s >= 60]
failing = [(n, s) for n, s in students if s  < 60]
ranked  = sorted(students, key=lambda x: x[1], reverse=True)

print(f"Class average: {avg:.1f}")
print(f"Passing ({len(passing)}): {[n for n,_ in passing]}")
print(f"Failing ({len(failing)}): {[(n,s) for n,s in failing]}")
print("Top 3:", ranked[:3])"""}
},

{
"title": "4. Tuples, Sets & Dictionaries",
"desc": "Tuples are immutable sequences; sets are unordered unique collections; dictionaries are key-value mappings.",
"examples": [
{"label": "Tuples and sets", "code":
"""# Tuple — immutable
point = (3, 7)
x, y  = point         # unpacking
print(f"x={x}, y={y}")

rgb   = (255, 128, 0)
print("Red channel:", rgb[0])

# Set — unique, unordered
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}
print("Union:       ", a | b)
print("Intersection:", a & b)
print("Difference:  ", a - b)

tags = ["python", "data", "python", "ml", "data"]
unique_tags = set(tags)
print("Unique tags:", unique_tags)"""},
{"label": "Dictionaries", "code":
"""person = {"name": "Alice", "age": 30, "city": "NYC"}

print(person["name"])                 # Alice
print(person.get("email", "N/A"))     # safe get with default

# Add / update
person["email"]  = "alice@example.com"
person["age"]    = 31
del person["city"]

print(person)
print("Keys:",   list(person.keys()))
print("Values:", list(person.values()))

# Iterate
for k, v in person.items():
    print(f"  {k}: {v}")"""},
{"label": "Dict comprehension and merging", "code":
"""# Dict comprehension from zip
students = ["Alice", "Bob", "Carol", "Dave"]
scores   = [92, 74, 88, 51]

grade_map = dict(zip(students, scores))
print("Grade map:", grade_map)

# Filter with dict comprehension
passing = {name: score for name, score in grade_map.items() if score >= 60}
print("Passing:", passing)

# Map scores to letter grades
def letter(s):
    return "A" if s >= 90 else "B" if s >= 80 else "C" if s >= 70 else "D" if s >= 60 else "F"

letters = {name: letter(score) for name, score in grade_map.items()}
print("Letters:", letters)

# Dict merging with ** operator (Python 3.5+)
defaults = {"timeout": 30, "retries": 3, "verbose": False}
overrides = {"retries": 5, "verbose": True}
config = {**defaults, **overrides}   # overrides wins on conflict
print("Config:", config)

# Python 3.9+ merge operator (| and |=)
# config = defaults | overrides"""},
{"label": "OrderedDict, ChainMap, dict views, and set update operations", "code":
"""from collections import OrderedDict, ChainMap

# OrderedDict — remembers insertion order (useful for LRU-style caches)
od = OrderedDict()
od["first"]  = 1
od["second"] = 2
od["third"]  = 3
od.move_to_end("first")           # move 'first' to the end
print("OrderedDict:", list(od.keys()))

# popitem(last=False) removes from the front (FIFO)
key, val = od.popitem(last=False)
print(f"Popped first: {key}={val}, remaining: {list(od.keys())}")

# ChainMap — single view over multiple dicts (first match wins)
defaults = {"color": "blue", "size": "M", "font": "Arial"}
user_prefs = {"color": "red", "size": "L"}
session = {"font": "Helvetica"}
merged = ChainMap(session, user_prefs, defaults)
print("color:", merged["color"])   # 'red'   (user_prefs wins)
print("font:",  merged["font"])    # 'Helvetica' (session wins)

# Dict views are live — they reflect changes
d = {"a": 1, "b": 2, "c": 3}
keys_view = d.keys()
d["d"] = 4
print("Live keys view:", list(keys_view))  # includes 'd'

# Set operations with update / intersection_update
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}
a.update({8, 9})                 # union in-place (|=)
print("After update:", sorted(a))
a.intersection_update(b | {8})   # keep only items in both (a &= ...)
print("After intersection_update:", sorted(a))"""}
],
"practice": {
"title": "Grade Book Manager",
"desc": "Create a grade book from two lists using zip, find failed students with a set comprehension, and map scores to letter grades with a dict comprehension.",
"starter":
"""students = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank"]
scores   = [92, 58, 76, 45, 88, 63]

# TODO: Build grade_book dict from zip(students, scores)
# grade_book = dict(???)

# TODO: Find failed students (score < 60) using a set comprehension
# failed = {name for name, score in ???.items() if ???}

# TODO: Map each student to a letter grade with dict comprehension
# Use: A>=90, B>=80, C>=70, D>=60, F otherwise
# Hint: define a helper or use nested ternary
# letter_grades = {name: ??? for name, score in grade_book.items()}

# TODO: Merge grade_book with a "class_info" dict using **
# class_info = {"class": "Python 101", "semester": "Spring 2024"}
# full_record = {**class_info, "grades": letter_grades}

print("Grade book:", grade_book)
print("Failed:", failed)
print("Letter grades:", letter_grades)"""
},
"rw": {
"title": "Inventory Tracking System",
"scenario": "A small shop tracks stock levels with a dictionary and uses sets to find products needing reorder.",
"code":
"""inventory = {
    "apple":   {"qty": 150, "price": 0.50, "min_stock": 50},
    "banana":  {"qty": 30,  "price": 0.25, "min_stock": 40},
    "milk":    {"qty": 10,  "price": 2.99, "min_stock": 20},
    "bread":   {"qty": 80,  "price": 3.49, "min_stock": 15},
    "cheese":  {"qty": 5,   "price": 5.99, "min_stock": 10},
}

reorder = {item for item, data in inventory.items()
           if data["qty"] < data["min_stock"]}

total_value = sum(d["qty"] * d["price"] for d in inventory.values())

print(f"Total inventory value: ${total_value:.2f}")
print(f"Items to reorder ({len(reorder)}): {reorder}")

for item in sorted(reorder):
    d = inventory[item]
    print(f"  {item:8s} qty={d['qty']:3d}  min={d['min_stock']:3d}  (order {d['min_stock']*2 - d['qty']} units)")"""}
},

{
"title": "5. Control Flow",
"desc": "if/elif/else controls which code runs. Python uses indentation (4 spaces) instead of curly braces to define blocks.",
"examples": [
{"label": "if / elif / else", "code":
"""# Basic if-elif-else
temperature = 28

if temperature > 35:
    status = "Heat warning"
elif temperature > 25:
    status = "Warm"
elif temperature > 15:
    status = "Comfortable"
elif temperature > 5:
    status = "Cool"
else:
    status = "Cold"

print(f"{temperature}°C → {status}")

# Ternary (one-liner)
label = "Pass" if temperature > 20 else "Fail"
print("Label:", label)

# Chained comparisons
x = 15
if 10 < x < 20:
    print(f"{x} is between 10 and 20")"""},
{"label": "Logical operators and truthiness", "code":
"""# and, or, not
age    = 22
income = 55000

eligible = age >= 18 and income >= 30000
print("Eligible:", eligible)

username = ""
display  = username or "Anonymous"
print("Display name:", display)

# in / not in
role = "editor"
allowed = ["admin", "editor", "moderator"]
if role in allowed:
    print(f"{role} has access")

# Walrus operator (Python 3.8+)
data = [1, 2, 3]
if n := len(data):
    print(f"List has {n} items")"""},
{"label": "match statement and password validator", "code":
"""# match statement (Python 3.10+) — structured pattern matching
def http_status(code):
    match code:
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 400:
            return "Bad Request"
        case 401 | 403:
            return "Auth error"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return f"Unknown ({code})"

for code in [200, 201, 403, 404, 418]:
    print(f"  {code} → {http_status(code)}")

# any() / all() for password strength
def check_password(pw):
    checks = {
        "length >= 8":  len(pw) >= 8,
        "has uppercase": any(c.isupper() for c in pw),
        "has digit":     any(c.isdigit() for c in pw),
        "has symbol":    any(c in "!@#$%^&*()" for c in pw),
    }
    for rule, ok in checks.items():
        print(f"  {'OK' if ok else 'FAIL':4s}  {rule}")
    return all(checks.values())

print("Strong:", check_password("Secure@9"))
print("Strong:", check_password("weakpass"))"""},
{"label": "Short-circuit evaluation, assert, and conditional imports", "code":
"""# Short-circuit evaluation
# 'and' stops at the first falsy value, 'or' stops at first truthy
def expensive():
    print("  [expensive() called]")
    return True

print("--- short-circuit AND ---")
result = False and expensive()    # expensive() never called
print("Result:", result)

print("--- short-circuit OR ---")
result = True or expensive()      # expensive() never called
print("Result:", result)

# Practical: safe attribute access via short-circuit
user = None
name = user and user.get("name", "")   # won't crash if user is None
print("Name:", name)                    # None (short-circuited)

user = {"name": "Alice", "role": "admin"}
name = user and user.get("name", "")
print("Name:", name)                    # "Alice"

# assert — for debugging invariants (disabled with python -O)
def divide(a, b):
    assert b != 0, f"Divisor must not be zero, got b={b}"
    return a / b

print(divide(10, 2))
try:
    divide(5, 0)
except AssertionError as e:
    print(f"AssertionError: {e}")

# Conditional import — try fast C lib, fall back to pure Python
try:
    import ujson as json_lib          # fast third-party JSON
    print("Using ujson")
except ImportError:
    import json as json_lib           # stdlib fallback
    print("Using stdlib json")

data = json_lib.dumps({"key": "value", "nums": [1, 2, 3]})
print("Encoded:", data)"""}
],
"practice": {
"title": "Traffic Light Simulator",
"desc": "Implement traffic_action(color, has_pedestrian, is_emergency) that returns the correct action string using if/elif/else logic.",
"starter":
"""def traffic_action(color, has_pedestrian=False, is_emergency=False):
    # TODO: if is_emergency, all lights should yield — return "All yield for emergency"

    # TODO: use if/elif/else on color:
    #   "green"  -> "Go" (but if has_pedestrian -> "Go, watch for pedestrians")
    #   "yellow" -> "Slow down" (but if has_pedestrian -> "Stop for pedestrians")
    #   "red"    -> "Stop" (but if has_pedestrian -> "Stop — pedestrians crossing")
    #   default  -> f"Unknown signal: {color}"
    pass

# Test cases
print(traffic_action("green"))                          # Go
print(traffic_action("green",  has_pedestrian=True))    # Go, watch for pedestrians
print(traffic_action("yellow"))                         # Slow down
print(traffic_action("red",    has_pedestrian=True))    # Stop — pedestrians crossing
print(traffic_action("red",    is_emergency=True))      # All yield for emergency
print(traffic_action("purple"))                         # Unknown signal: purple"""
},
"rw": {
"title": "Loan Eligibility Checker",
"scenario": "A fintech app determines loan eligibility and interest rate tier based on applicant data.",
"code":
"""def check_loan(age, income, credit_score, existing_debt):
    # Basic eligibility
    if age < 18:
        return "REJECTED", "Must be 18+"
    if income < 20000:
        return "REJECTED", "Minimum income $20,000"
    if credit_score < 580:
        return "REJECTED", "Credit score below 580"

    debt_to_income = existing_debt / income
    if debt_to_income > 0.5:
        return "REJECTED", f"Debt-to-income {debt_to_income:.0%} exceeds 50%"

    # Approved — determine tier
    if credit_score >= 750 and debt_to_income < 0.2:
        rate = 4.5
        tier = "Prime"
    elif credit_score >= 680:
        rate = 6.9
        tier = "Standard"
    else:
        rate = 11.5
        tier = "Subprime"

    return "APPROVED", f"{tier} rate: {rate}%"

applicants = [
    (25, 65000, 720, 5000),
    (17, 80000, 800, 0),
    (35, 90000, 760, 8000),
    (30, 25000, 620, 15000),
]
for a in applicants:
    status, msg = check_loan(*a)
    print(f"  Age={a[0]}, Income=${a[1]:,}, Score={a[2]} → {status}: {msg}")"""}
},

{
"title": "6. Loops",
"desc": "for iterates over any iterable (list, range, string, dict). while loops run while a condition is True. Use break, continue, and enumerate for control.",
"examples": [
{"label": "for loops", "code":
"""# Loop over list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Range
for i in range(1, 6):
    print(i, end=" ")
print()

# enumerate — get index + value
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip — loop two lists together
prices = [0.5, 0.25, 1.99]
for fruit, price in zip(fruits, prices):
    print(f"  {fruit}: ${price}")"""},
{"label": "while, break, continue", "code":
"""# while loop
count = 0
total = 0
while count < 5:
    total += count
    count += 1
print(f"Sum 0..4 = {total}")

# break — exit early
for n in range(100):
    if n * n > 50:
        print(f"First n where n²>50: {n}")
        break

# continue — skip current iteration
for n in range(10):
    if n % 2 == 0:
        continue      # skip even numbers
    print(n, end=" ")
print()

# else on for loop (runs if not broken)
for n in range(2, 10):
    if 7 % n == 0 and n != 7:
        print("7 is not prime"); break
else:
    print("7 is prime")"""},
{"label": "Nested loops and accumulator pattern", "code":
"""# Multiplication table using nested loops
print("Multiplication table (1-5):")
for i in range(1, 6):
    row = ""
    for j in range(1, 6):
        row += f"{i*j:4d}"
    print(row)

# itertools.product — Cartesian product (like nested loops)
import itertools
suits  = ["♠", "♥", "♦", "♣"]
values = ["A", "K", "Q"]
cards  = list(itertools.product(values, suits))
print(f"\\n{len(cards)} high cards:", cards[:4], "...")

# Running maximum accumulator pattern
readings = [12, 7, 25, 18, 30, 14, 42, 9, 36]
running_max = []
current_max = float("-inf")
for val in readings:
    if val > current_max:
        current_max = val
    running_max.append(current_max)
print("\\nReadings:    ", readings)
print("Running max: ", running_max)"""},
{"label": "itertools recipes: chain, islice, takewhile, dropwhile, groupby", "code":
"""import itertools

# chain — iterate multiple iterables as one
a = [1, 2, 3]
b = ("four", "five")
c = range(6, 9)
for item in itertools.chain(a, b, c):
    print(item, end=" ")
print()

# islice — lazy slice of an iterator (no list copy)
gen = (x**2 for x in itertools.count(1))   # infinite squares
first_10 = list(itertools.islice(gen, 10))
print("First 10 squares:", first_10)

# takewhile / dropwhile — conditional iteration
data = [2, 4, 6, 7, 8, 10, 12]
taken   = list(itertools.takewhile(lambda x: x % 2 == 0, data))
dropped = list(itertools.dropwhile(lambda x: x % 2 == 0, data))
print("takewhile even:", taken)    # [2, 4, 6] — stops at 7
print("dropwhile even:", dropped)  # [7, 8, 10, 12] — starts at 7

# groupby — group consecutive items by a key (data must be sorted by key first)
entries = [
    ("Alice", "Engineering"), ("Bob", "Engineering"),
    ("Carol", "Marketing"),   ("Dave", "Marketing"),
    ("Eve",   "Engineering"),
]
entries.sort(key=lambda e: e[1])   # sort by department first
for dept, group in itertools.groupby(entries, key=lambda e: e[1]):
    names = [name for name, _ in group]
    print(f"  {dept}: {names}")"""}
],
"practice": {
"title": "FizzBuzz Plus",
"desc": "Loop from 1 to 30. For each number: if divisible by 3 add 'Fizz', by 5 add 'Buzz', by 7 add 'Zap'. Print the composed string, or the number if none apply.",
"starter":
"""results = []

for n in range(1, 31):
    label = ""
    # TODO: if divisible by 3, add "Fizz" to label
    # if n % 3 == 0: label += ???

    # TODO: if divisible by 5, add "Buzz" to label

    # TODO: if divisible by 7, add "Zap" to label

    # TODO: if label is still empty, use the number itself
    # results.append(label if label else str(n))
    pass

# Print 10 per line
for i in range(0, 30, 10):
    print("  " + "  ".join(f"{v:8s}" for v in results[i:i+10]))

# Expected row 1: 1  2  Fizz  4  Buzz  Fizz  Zap  8  Fizz  Buzz"""
},
"rw": {
"title": "Sales Report Generator",
"scenario": "A sales manager loops through weekly data to compute running totals, find best weeks, and flag targets.",
"code":
"""weekly_sales = [42000, 38500, 51000, 47200, 29800, 55600, 48900, 61000, 39700, 52300]
target       = 45000
best_week    = 0
best_amount  = 0
total        = 0
above_target = 0

for week, sales in enumerate(weekly_sales, start=1):
    total += sales
    if sales > best_amount:
        best_amount = sales
        best_week   = week
    status = "✓" if sales >= target else "✗"
    if sales >= target:
        above_target += 1
    print(f"  Week {week:2d}: ${sales:>7,}  {status}")

avg = total / len(weekly_sales)
print(f"\nTotal:     ${total:>9,}")
print(f"Average:   ${avg:>9,.0f}")
print(f"Best week: Week {best_week} (${best_amount:,})")
print(f"On target: {above_target}/{len(weekly_sales)} weeks")"""}
},

{
"title": "7. Functions",
"desc": "Functions let you encapsulate reusable logic. Python supports default arguments, *args, **kwargs, and lambda (anonymous) functions.",
"examples": [
{"label": "Defining functions and default arguments", "code":
"""def greet(name, greeting="Hello"):
    # Returns a greeting string
    return f"{greeting}, {name}!"

print(greet("Alice"))
print(greet("Bob", "Hi"))
print(greet(name="Carol", greeting="Hey"))

# Multiple return values (returns a tuple)
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers)/len(numbers)

lo, hi, avg = stats([4, 8, 2, 9, 1, 7])
print(f"min={lo}, max={hi}, avg={avg:.2f}")"""},
{"label": "*args, **kwargs, lambda", "code":
"""# *args — variable positional arguments
def add_all(*args):
    return sum(args)

print(add_all(1, 2, 3))            # 6
print(add_all(10, 20, 30, 40))     # 100

# **kwargs — variable keyword arguments
def build_profile(**kwargs):
    return {k: v for k, v in kwargs.items()}

print(build_profile(name="Alice", age=30, role="admin"))

# Lambda (anonymous function)
square   = lambda x: x ** 2
multiply = lambda x, y: x * y

nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(nums))
print(sorted(nums, key=lambda x: -x))   # descending"""},
{"label": "Closures and decorators", "code":
"""import time, functools

# Closure — inner function captures outer variable
def make_counter(start=0):
    count = [start]  # mutable container so inner fn can modify
    def counter():
        count[0] += 1
        return count[0]
    return counter

c1 = make_counter()
c2 = make_counter(10)
print(c1(), c1(), c1())   # 1 2 3
print(c2(), c2())          # 11 12  (independent state)

# Decorator — wraps a function to add behaviour
def timer(func):
    @functools.wraps(func)   # preserves __name__, __doc__
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

total = slow_sum(1_000_000)
print(f"Sum = {total:,}")
print("Function name preserved:", slow_sum.__name__)"""},
{"label": "Type hints, functools.reduce, and inspect signatures", "code":
"""from typing import List, Dict, Optional, Union, Callable
import functools, inspect

# Type hints — document intent, checked by mypy (not enforced at runtime)
def calculate_total(
    prices: List[float],
    tax_rate: float = 0.08,
    discount: Optional[float] = None,
) -> Dict[str, float]:
    subtotal = sum(prices)
    disc_amt  = subtotal * discount if discount else 0.0
    taxable   = subtotal - disc_amt
    total     = taxable * (1 + tax_rate)
    return {"subtotal": round(subtotal, 2),
            "discount": round(disc_amt, 2),
            "tax":      round(taxable * tax_rate, 2),
            "total":    round(total, 2)}

result = calculate_total([9.99, 24.50, 4.99], discount=0.1)
for k, v in result.items():
    print(f"  {k:10s}: ${v:.2f}")

# functools.reduce — fold sequence into single value
from functools import reduce
factorial = reduce(lambda acc, x: acc * x, range(1, 8))  # 7! = 5040
print(f"7! = {factorial}")

running_totals = []
reduce(lambda acc, x: (running_totals.append(acc + x), acc + x)[1],
       [10, 20, 30, 40], 0)
print("Running totals:", running_totals)

# inspect — introspect function signatures at runtime
def my_func(a: int, b: float = 3.14, *args, keyword: str = "hi", **kwargs):
    pass

sig = inspect.signature(my_func)
for name, param in sig.parameters.items():
    kind    = str(param.kind).split(".")[-1]
    default = param.default if param.default is not inspect.Parameter.empty else "required"
    print(f"  {name:10s} [{kind:20s}] default={default}")"""}
],
"practice": {
"title": "Memoize Decorator",
"desc": "Write a memoize(func) decorator that caches results in a dict keyed by args. Then decorate a recursive fibonacci function and observe the speedup.",
"starter":
"""def memoize(func):
    cache = {}
    # TODO: define wrapper(*args) that:
    #   1. checks if args is already in cache
    #   2. if yes, returns cache[args]
    #   3. if no, calls func(*args), stores in cache, returns result
    # TODO: use functools.wraps(func) to preserve metadata
    # TODO: return wrapper
    pass

import functools

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Test: should complete instantly even for large n
print([fibonacci(i) for i in range(10)])  # [0,1,1,2,3,5,8,13,21,34]
print(fibonacci(35))                       # 9227465 — fast with memoize!"""
},
"rw": {
"title": "Data Cleaning Pipeline",
"scenario": "A data engineer writes a set of small, composable functions to clean and validate user records.",
"code":
"""def clean_name(name):
    return " ".join(w.capitalize() for w in name.strip().split())

def clean_email(email):
    return email.strip().lower()

def validate_age(age, min_age=0, max_age=120):
    try:
        a = int(age)
        return a if min_age <= a <= max_age else None
    except (ValueError, TypeError):
        return None

def clean_record(record):
    return {
        "name":  clean_name(record.get("name", "")),
        "email": clean_email(record.get("email", "")),
        "age":   validate_age(record.get("age")),
    }

raw_records = [
    {"name": "  alice SMITH ", "email": "Alice@Example.COM ", "age": "28"},
    {"name": "BOB jones",      "email": "bob@company.com",    "age": "abc"},
    {"name": "carol  White",   "email": "  CAROL@test.org",  "age": "200"},
]

for rec in raw_records:
    cleaned = clean_record(rec)
    valid = "OK" if cleaned["age"] is not None else "INVALID AGE"
    print(f"  {cleaned['name']:18s} | {cleaned['email']:25s} | age={cleaned['age']} {valid}")"""}
},

{
"title": "8. Classes & OOP",
"desc": "Classes define blueprints for objects. Python supports encapsulation, inheritance, and special (dunder) methods like __str__ and __repr__.",
"examples": [
{"label": "Defining a class with __init__ and methods", "code":
"""class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner   = owner
        self.balance = balance
        self._history = []        # convention: private

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._history.append(f"+{amount:.2f}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            self._history.append(f"-{amount:.2f}")

    def __str__(self):
        return f"Account({self.owner}, ${self.balance:.2f})"

acc = BankAccount("Alice", 1000)
acc.deposit(500)
acc.withdraw(200)
print(acc)
print("History:", acc._history)"""},
{"label": "Inheritance", "code":
"""class Animal:
    def __init__(self, name, sound):
        self.name  = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}!"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Woof")
        self.breed = breed

    def fetch(self, item):
        return f"{self.name} fetches the {item}!"

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "Meow")

    def purr(self):
        return f"{self.name} purrs..."

dog = Dog("Rex", "Labrador")
cat = Cat("Whiskers")
print(dog.speak(), dog.fetch("ball"))
print(cat.speak(), cat.purr())"""},
{"label": "Properties, classmethods, and dunder comparison methods", "code":
"""class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @classmethod
    def from_fahrenheit(cls, f):
        return cls((f - 32) * 5/9)

    def __repr__(self):
        return f"Temperature({self._celsius:.2f}°C / {self.fahrenheit:.2f}°F)"

    def __lt__(self, other):
        return self._celsius < other._celsius

    def __eq__(self, other):
        return self._celsius == other._celsius

    def __add__(self, other):
        return Temperature(self._celsius + other._celsius)

t1 = Temperature(100)
t2 = Temperature.from_fahrenheit(32)   # 0°C
t3 = t1 + t2

print(t1)                  # 100°C / 212°F
print(t2)                  # 0°C / 32°F
print(t3)                  # 100°C sum
print(t2 < t1)             # True
print(sorted([t1, t2, t3]))"""},
{"label": "Abstract base classes (ABC), dataclasses, and __slots__", "code":
"""from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import sys

# Abstract Base Class — define an interface that subclasses must implement
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...
    @abstractmethod
    def perimeter(self) -> float:
        ...
    def describe(self):
        return f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    def area(self):
        import math; return math.pi * self.radius ** 2
    def perimeter(self):
        import math; return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        self.w, self.h = w, h
    def area(self):      return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)

for shape in [Circle(5), Rectangle(4, 6)]:
    print(shape.describe())

# @dataclass — auto-generates __init__, __repr__, __eq__
@dataclass(order=True)
class Point:
    x: float
    y: float
    label: str = field(default="", compare=False)

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

p1 = Point(0, 0, "origin")
p2 = Point(3, 4, "target")
print(p1, p2)
print(f"Distance: {p1.distance_to(p2):.2f}")
print("Sorted:", sorted([p2, p1]))

# __slots__ — restrict attributes, save memory
class SlottedPoint:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y

sp = SlottedPoint(1, 2)
print(f"SlottedPoint: ({sp.x}, {sp.y})")
try:
    sp.z = 99    # can't add new attributes
except AttributeError as e:
    print(f"AttributeError: {e}")"""}
],
"practice": {
"title": "Build a Stack",
"desc": "Implement a Stack class with push, pop, peek, __len__, and __repr__. The stack should raise IndexError on pop/peek from an empty stack.",
"starter":
"""class Stack:
    def __init__(self):
        # TODO: initialise internal list self._data = []
        pass

    def push(self, item):
        # TODO: append item to self._data
        pass

    def pop(self):
        # TODO: raise IndexError("pop from empty stack") if empty
        # TODO: otherwise remove and return the top item
        pass

    def peek(self):
        # TODO: raise IndexError("peek from empty stack") if empty
        # TODO: otherwise return top item WITHOUT removing it
        pass

    def __len__(self):
        # TODO: return number of items
        pass

    def __repr__(self):
        # TODO: return something like Stack([1, 2, 3]) — top is rightmost
        pass

# Tests
s = Stack()
s.push(1); s.push(2); s.push(3)
print(s)            # Stack([1, 2, 3])
print(len(s))       # 3
print(s.peek())     # 3
print(s.pop())      # 3
print(s)            # Stack([1, 2])
try:
    Stack().pop()
except IndexError as e:
    print(f"Caught: {e}")"""
},
"rw": {
"title": "E-Commerce Cart System",
"scenario": "An online store uses OOP to model products and a shopping cart with discount logic.",
"code":
"""class Product:
    def __init__(self, name, price, category):
        self.name     = name
        self.price    = price
        self.category = category

    def __repr__(self):
        return f"{self.name} (${self.price:.2f})"


class Cart:
    def __init__(self, user):
        self.user  = user
        self.items = []

    def add(self, product, qty=1):
        self.items.append({"product": product, "qty": qty})

    def subtotal(self):
        return sum(i["product"].price * i["qty"] for i in self.items)

    def apply_discount(self, code):
        discounts = {"SAVE10": 0.10, "HALF50": 0.50, "VIP20": 0.20}
        return discounts.get(code.upper(), 0)

    def checkout(self, code=""):
        sub      = self.subtotal()
        discount = self.apply_discount(code)
        total    = sub * (1 - discount)
        print(f"Cart for {self.user}:")
        for i in self.items:
            print(f"  {i['product'].name:15s} x{i['qty']}  ${i['product'].price * i['qty']:.2f}")
        print(f"  Subtotal: ${sub:.2f}")
        if discount: print(f"  Discount: -{discount:.0%}")
        print(f"  Total:    ${total:.2f}")

cart = Cart("Alice")
cart.add(Product("Laptop",  999.99, "Electronics"), 1)
cart.add(Product("Mouse",    29.99, "Electronics"), 2)
cart.add(Product("Notebook",  5.99, "Stationery"),  3)
cart.checkout("SAVE10")"""}
},

{
"title": "9. Error Handling",
"desc": "Use try/except/finally to handle exceptions gracefully. Raise custom exceptions to signal application-level errors.",
"examples": [
{"label": "try / except / finally", "code":
"""# Basic exception handling
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Error: cannot divide by zero"
    except TypeError as e:
        return f"Error: {e}"
    else:
        return result              # runs if no exception
    finally:
        print("safe_divide() called")  # always runs

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("x", 2))"""},
{"label": "Multiple exceptions and custom exceptions", "code":
"""class InsufficientFundsError(Exception):
    def __init__(self, amount, balance):
        self.amount  = amount
        self.balance = balance
        super().__init__(f"Tried to withdraw ${amount:.2f}, only ${balance:.2f} available")

def withdraw(balance, amount):
    if not isinstance(amount, (int, float)):
        raise TypeError(f"Amount must be a number, got {type(amount).__name__}")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if amount > balance:
        raise InsufficientFundsError(amount, balance)
    return balance - amount

for args in [(100, 30), (100, 200), (100, -10), (100, "abc")]:
    try:
        new_bal = withdraw(*args)
        print(f"Withdrew {args[1]}, new balance: {new_bal}")
    except (InsufficientFundsError, ValueError, TypeError) as e:
        print(f"Error: {e}")"""},
{"label": "Context managers and exception chaining", "code":
"""import time

# Custom context manager using __enter__ / __exit__
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.6f}s")
        return False  # don't suppress exceptions

with Timer() as t:
    total = sum(range(500_000))
print(f"Sum = {total:,}")

# Exception chaining — raise X from Y
class DatabaseError(Exception):
    pass

def fetch_user(user_id, data):
    try:
        return data[user_id]
    except KeyError as e:
        raise DatabaseError(f"User {user_id} not found") from e

records = {"alice": {"age": 30}, "bob": {"age": 25}}

for uid in ["alice", "carol"]:
    try:
        user = fetch_user(uid, records)
        print(f"Found: {user}")
    except DatabaseError as e:
        print(f"DB Error: {e}")
        print(f"  Caused by: {e.__cause__}")"""},
{"label": "contextlib helpers and logging module basics", "code":
"""import logging
import io
from contextlib import suppress, redirect_stdout, contextmanager

# suppress — silently ignore specific exceptions (replaces try/except/pass)
with suppress(FileNotFoundError):
    open("nonexistent_file.txt")   # no error raised
print("suppress: FileNotFoundError silently ignored")

# redirect_stdout — capture print() output into a buffer
buffer = io.StringIO()
with redirect_stdout(buffer):
    print("This goes into the buffer, not the terminal")
    print("So does this line")
captured = buffer.getvalue()
print(f"Captured {len(captured.splitlines())} lines: {captured.splitlines()[0]!r}")

# @contextmanager — create a context manager with a generator
@contextmanager
def managed_resource(name):
    print(f"  [open]  {name}")
    try:
        yield name.upper()     # value bound to 'as' target
    except Exception as e:
        print(f"  [error] {e}")
        raise
    finally:
        print(f"  [close] {name}")

with managed_resource("database_connection") as res:
    print(f"  Using: {res}")

# logging module basics
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-8s %(name)s: %(message)s"
)
log = logging.getLogger("myapp")
log.debug("Debug-level detail (only shown at DEBUG+)")
log.info("Server started on port 8080")
log.warning("Disk usage at 85%%")
log.error("Failed to connect to database")"""}
],
"practice": {
"title": "Safe Data Parser",
"desc": "Write parse_record(line) that parses a CSV line like 'Alice,28,92.5' into a dict with name (str), age (int), score (float). Return None on any error.",
"starter":
"""def parse_record(line):
    # TODO: split line by ","
    # TODO: wrap in try/except to catch ValueError and IndexError
    # TODO: inside try:
    #   parts = line.split(",")
    #   name  = parts[0].strip()
    #   age   = int(parts[1].strip())     # may raise ValueError
    #   score = float(parts[2].strip())   # may raise ValueError
    #   return {"name": name, "age": age, "score": score}
    # TODO: on except, return None
    pass

# Test cases
test_lines = [
    "Alice,28,92.5",      # valid
    "Bob,thirty,88.0",    # bad age
    "Carol,22",           # missing score (IndexError)
    "Dave,19,invalid",    # bad score
    "",                   # empty
]

for line in test_lines:
    result = parse_record(line)
    print(f"  {line!r:25s} -> {result}")"""
},
"rw": {
"title": "Robust File & API Data Reader",
"scenario": "A data pipeline gracefully handles missing files, JSON parse errors, and unexpected data formats.",
"code":
"""import json

def read_config(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Config file not found: {filepath}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filepath}: {e}")
        return {}

def get_setting(config, key, default=None, required=False):
    value = config.get(key, default)
    if required and value is None:
        raise KeyError(f"Required setting '{key}' is missing from config")
    return value

# Simulate loading a config
sample_config = {"db_host": "localhost", "db_port": 5432, "debug": True}

try:
    host    = get_setting(sample_config, "db_host",    required=True)
    port    = get_setting(sample_config, "db_port",    required=True)
    timeout = get_setting(sample_config, "timeout",    default=30)
    api_key = get_setting(sample_config, "api_key",    required=True)
except KeyError as e:
    print(f"Configuration error: {e}")
    host, port, timeout = "localhost", 5432, 30
    print(f"Using defaults: {host}:{port}, timeout={timeout}s")"""}
},

{
"title": "10. File I/O",
"desc": "Read and write files using open(). Use the with statement to ensure files are always closed. Python handles text and binary files.",
"examples": [
{"label": "Reading and writing text files", "code":
"""import os

# Write a file
with open("demo.txt", "w") as f:
    f.write("Line 1: Hello World\n")
    f.write("Line 2: Python File I/O\n")
    f.writelines(["Line 3: data\n", "Line 4: more data\n"])

# Read entire file
with open("demo.txt", "r") as f:
    content = f.read()
print("Full content:\n", content)

# Read line by line
with open("demo.txt", "r") as f:
    for i, line in enumerate(f, 1):
        print(f"  [{i}] {line.rstrip()}")

os.remove("demo.txt")  # cleanup"""},
{"label": "Working with CSV and JSON", "code":
"""import json, csv, io

# JSON
data = {"name": "Alice", "scores": [95, 87, 91], "active": True}
json_str = json.dumps(data, indent=2)
print("JSON:\n", json_str)

loaded = json.loads(json_str)
print("Avg score:", sum(loaded["scores"]) / len(loaded["scores"]))

# CSV (using in-memory buffer)
output = io.StringIO()
writer = csv.writer(output)
writer.writerow(["name", "age", "city"])
writer.writerows([["Alice",30,"NYC"],["Bob",25,"LA"],["Carol",35,"Chicago"]])

output.seek(0)
reader = csv.DictReader(output)
for row in reader:
    print(dict(row))"""},
{"label": "pathlib and binary I/O", "code":
"""import pathlib, io, tempfile

# pathlib — modern, object-oriented path handling
p = pathlib.Path.home()
print("Home dir:", p)
print("Exists:", p.exists())

# Build paths with / operator
tmp = pathlib.Path(tempfile.gettempdir())
data_file = tmp / "demo_data.txt"

# Write and read with pathlib
data_file.write_text("Hello from pathlib!\\nLine 2\\nLine 3\\n", encoding="utf-8")
content = data_file.read_text(encoding="utf-8")
print("Read back:", content.splitlines())

# Inspect path parts
print("Name:     ", data_file.name)
print("Stem:     ", data_file.stem)
print("Suffix:   ", data_file.suffix)
print("Parent:   ", data_file.parent)

data_file.unlink()  # delete

# io.BytesIO — in-memory binary buffer (like a file but in RAM)
buf = io.BytesIO()
buf.write(b"\\x89PNG\\r\\n")   # fake PNG header bytes
buf.write(b"binary data here")
buf.seek(0)
header = buf.read(6)
print("Bytes header:", header)
print("Buffer size:", buf.getbuffer().nbytes, "bytes")"""},
{"label": "pathlib.Path advanced: glob, rglob, iterdir, and tempfile module", "code":
"""import pathlib, tempfile, os

# Create a temporary directory to experiment in
with tempfile.TemporaryDirectory() as tmpdir:
    root = pathlib.Path(tmpdir)

    # Create nested structure
    (root / "src").mkdir()
    (root / "src" / "utils").mkdir()
    (root / "data").mkdir()
    (root / "src" / "main.py").write_text("# main", encoding="utf-8")
    (root / "src" / "helper.py").write_text("# helper", encoding="utf-8")
    (root / "src" / "utils" / "tools.py").write_text("# tools", encoding="utf-8")
    (root / "data" / "report.csv").write_text("a,b,c", encoding="utf-8")
    (root / "data" / "notes.txt").write_text("notes", encoding="utf-8")
    (root / "README.md").write_text("# Project", encoding="utf-8")

    # iterdir() — immediate children only (non-recursive)
    print("Top-level items:")
    for item in sorted(root.iterdir()):
        kind = "DIR " if item.is_dir() else "FILE"
        print(f"  {kind}  {item.name}")

    # glob() — match pattern in direct children
    print("\\n*.md files (glob):", [p.name for p in root.glob("*.md")])

    # rglob() — recursive glob across all subdirectories
    print("All .py files (rglob):")
    for py in sorted(root.rglob("*.py")):
        print(f"  {py.relative_to(root)}")

    print("All files (rglob **):")
    all_files = sorted(root.rglob("*"))
    for f in all_files:
        if f.is_file():
            print(f"  {f.relative_to(root)}  ({f.stat().st_size} bytes)")

# tempfile — create named temp files that auto-delete
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tf:
    tf.write('{"status": "ok"}')
    tmp_path = pathlib.Path(tf.name)

print(f"\\nTemp file: {tmp_path.name}")
print("Content:", tmp_path.read_text(encoding="utf-8"))
tmp_path.unlink()   # manual cleanup since delete=False
print("Temp file deleted:", not tmp_path.exists())"""}
],
"practice": {
"title": "Log File Analyzer",
"desc": "Parse a multi-line log string (via io.StringIO), count occurrences of each log level, and collect all ERROR message lines.",
"starter":
"""import io

log_data = \"\"\"2024-01-15 INFO    Server started on port 8080
2024-01-15 DEBUG   Loading config file
2024-01-15 INFO    Database connected
2024-01-15 WARNING Disk usage at 80%
2024-01-15 ERROR   Failed to connect to cache: timeout
2024-01-15 INFO    Request received: GET /home
2024-01-15 ERROR   Database query failed: syntax error
2024-01-15 WARNING Memory usage high: 75%
2024-01-15 INFO    Request completed in 120ms
2024-01-15 CRITICAL Disk full — writes disabled\"\"\"

# TODO: create a file-like object from log_data using io.StringIO
# f = io.StringIO(???)

# TODO: iterate over lines, split each line to get the level (index 1)
# count level occurrences in a dict: level_counts = {}
# if the level is "ERROR", append the full line to error_lines list

# Expected output:
# Level counts: {'INFO': 4, 'DEBUG': 1, 'WARNING': 2, 'ERROR': 2, 'CRITICAL': 1}
# Error lines:
#   2024-01-15 ERROR   Failed to connect to cache: timeout
#   2024-01-15 ERROR   Database query failed: syntax error"""
},
"rw": {
"title": "Sales Report File Processor",
"scenario": "A business analyst reads daily sales CSV files, aggregates totals, and writes a JSON summary report.",
"code":
"""import csv, json, io

# Simulate CSV content
csv_data = "\n".join([
    "date,product,region,qty,price",
    "2024-01-01,Widget,North,10,9.99",
    "2024-01-01,Gadget,South,5,49.99",
    "2024-01-02,Widget,East,15,9.99",
    "2024-01-02,Doohickey,North,8,19.99",
    "2024-01-03,Gadget,East,3,49.99",
    "2024-01-03,Widget,South,12,9.99",
])

reader  = csv.DictReader(io.StringIO(csv_data))
summary = {}

for row in reader:
    revenue = float(row["qty"]) * float(row["price"])
    product = row["product"]
    region  = row["region"]

    if product not in summary:
        summary[product] = {"total_revenue": 0, "total_qty": 0, "regions": {}}
    summary[product]["total_revenue"] += revenue
    summary[product]["total_qty"]     += int(row["qty"])
    summary[product]["regions"][region] = summary[product]["regions"].get(region, 0) + revenue

report = {k: {"revenue": round(v["total_revenue"],2), "qty": v["total_qty"],
              "top_region": max(v["regions"], key=v["regions"].get)}
          for k, v in summary.items()}

print(json.dumps(report, indent=2))"""}
},

{
"title": "11. List Comprehensions & Generators",
"desc": "Comprehensions create lists, dicts, and sets concisely. Generators produce values lazily, saving memory for large sequences.",
"examples": [
{"label": "List, dict, and set comprehensions", "code":
"""# List comprehension
squares = [x**2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]
matrix  = [[i*j for j in range(1,4)] for i in range(1,4)]

print("Squares:", squares[:5])
print("Evens:", evens)
print("Matrix:", matrix)

# Dict comprehension
word   = "mississippi"
counts = {ch: word.count(ch) for ch in set(word)}
print("Char counts:", dict(sorted(counts.items())))

# Set comprehension
text  = ["hello", "world", "hello", "python"]
unique_upper = {w.upper() for w in text}
print("Unique upper:", unique_upper)"""},
{"label": "Generators and generator expressions", "code":
"""# Generator function (yields values lazily)
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

fibs = list(fibonacci(10))
print("Fibonacci:", fibs)

# Generator expression (lazy list comprehension)
big_squares = (x**2 for x in range(1_000_000))
print("First 5:", [next(big_squares) for _ in range(5)])

# sum() with generator — no list created in memory
total = sum(x**2 for x in range(1000))
print("Sum of squares 0..999:", total)"""},
{"label": "Generator pipeline", "code":
"""# Chain generators together — each processes values lazily

def read_numbers(data):
    \"\"\"Yield numbers one at a time from a list.\"\"\"
    for n in data:
        yield n

def filter_positive(numbers):
    \"\"\"Yield only positive numbers.\"\"\"
    for n in numbers:
        if n > 0:
            yield n

def square(numbers):
    \"\"\"Yield squares of numbers.\"\"\"
    for n in numbers:
        yield n * n

def running_total(numbers):
    \"\"\"Yield cumulative sum at each step.\"\"\"
    total = 0
    for n in numbers:
        total += n
        yield total

# Build the pipeline
raw      = [-3, 1, -1, 4, 5, -9, 2, 6]
pipeline = running_total(square(filter_positive(read_numbers(raw))))

print("Pipeline output:", list(pipeline))
# positives: 1,4,5,2,6  squares: 1,16,25,4,36  running: 1,17,42,46,82

# Nested comprehension — flatten a matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat   = [cell for row in matrix for cell in row]
print("Flat matrix:", flat)

# Nested comprehension — all pairs where i != j
pairs = [(i, j) for i in range(4) for j in range(4) if i != j]
print(f"Pairs (i!=j): {len(pairs)} pairs, first 4: {pairs[:4]}")"""},
{"label": "itertools.chain, zip_longest, and starmap", "code":
"""import itertools

# chain.from_iterable — flatten one level of nested iterables
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flat   = list(itertools.chain.from_iterable(nested))
print("chain.from_iterable:", flat)

# zip_longest — zip unequal-length iterables, filling with a default
names  = ["Alice", "Bob", "Carol"]
scores = [92, 85]
grades = ["A"]
for row in itertools.zip_longest(names, scores, grades, fillvalue="N/A"):
    print(f"  {row[0]:8s}  score={row[1]:>4}  grade={row[2]}")

# starmap — map with argument unpacking (like map but for tuple arguments)
pairs  = [(2, 10), (3, 4), (10, 2), (5, 3)]
powers = list(itertools.starmap(pow, pairs))
print("starmap(pow, pairs):", powers)   # [1024, 81, 100, 125]

# Practical: generate a multiplication table with starmap
import operator
combos = itertools.product(range(1, 4), range(1, 4))
table  = list(itertools.starmap(operator.mul, combos))
print("3x3 mul table (flat):", table)

# accumulate — running totals / cumulative operations
sales   = [1200, 850, 1400, 980, 1100]
running = list(itertools.accumulate(sales))
print("Running sales totals:", running)

running_max = list(itertools.accumulate(sales, max))
print("Running maximums:    ", running_max)"""}
],
"practice": {
"title": "Data Processing Pipeline",
"desc": "Implement three chained generators: csv_rows() yields raw lines, parse_sales() parses each to a dict, high_value() keeps only sales above a threshold.",
"starter":
"""import io

csv_data = \"\"\"date,product,qty,price
2024-01-01,Widget,10,9.99
2024-01-02,Gadget,5,49.99
2024-01-03,Widget,15,9.99
2024-01-04,SuperGadget,2,199.99
2024-01-05,Widget,8,9.99
2024-01-06,Gadget,3,49.99\"\"\"

def csv_rows(text):
    # TODO: use io.StringIO(text), skip the header line,
    # yield each remaining non-empty stripped line
    pass

def parse_sales(rows):
    # TODO: for each row, split by "," to get date, product, qty, price
    # yield dict: {"date": ..., "product": ..., "revenue": int(qty)*float(price)}
    pass

def high_value(sales, threshold=100):
    # TODO: yield only sales where revenue > threshold
    pass

# Chain the pipeline
pipeline = high_value(parse_sales(csv_rows(csv_data)))
for sale in pipeline:
    print(f"  {sale['date']}  {sale['product']:12s}  ${sale['revenue']:.2f}")"""
},
"rw": {
"title": "Log File Streaming Processor",
"scenario": "A data engineer uses generators to process large log files line-by-line without loading everything into memory.",
"code":
"""import io

# Simulate a large log file as a generator
def stream_logs(file_obj, min_level="WARNING"):
    levels = {"DEBUG":0, "INFO":1, "WARNING":2, "ERROR":3, "CRITICAL":4}
    min_n  = levels.get(min_level, 0)
    for line in file_obj:
        line = line.strip()
        if not line: continue
        parts = line.split(None, 3)
        if len(parts) < 4: continue
        level = parts[1]
        if levels.get(level, 0) >= min_n:
            yield {"ts": parts[0], "level": level, "service": parts[2], "msg": parts[3]}

sample_log = io.StringIO("\n".join([
    "2024-01-15 DEBUG   db_pool:      Connection acquired",
    "2024-01-15 INFO    auth_service: User login alice@co.com",
    "2024-01-15 WARNING api_gateway:  Rate limit 90% for 192.168.1.1",
    "2024-01-15 ERROR   payment_svc:  Timeout after 30s for order #8821",
    "2024-01-15 INFO    cache:        Cache miss for key user:42",
    "2024-01-15 CRITICAL db_pool:     Connection pool exhausted!",
]))

alerts = list(stream_logs(sample_log, min_level="WARNING"))
print(f"Found {len(alerts)} alerts:")
for a in alerts:
    print(f"  [{a['level']:8s}] {a['service']:12s} {a['msg']}")"""}
},

{
"title": "12. Modules & Useful Built-ins",
"desc": "Python's standard library is vast. Key modules: os, sys, datetime, math, random, collections, itertools. Use import to access them.",
"examples": [
{"label": "os, datetime, math", "code":
"""import os
import math
import datetime

# os — file system and environment
cwd = os.getcwd()
print("CWD:", cwd)
print("Home:", os.path.expanduser("~"))
print("Path exists:", os.path.exists(cwd))

# datetime
today = datetime.date.today()
now   = datetime.datetime.now()
delta = datetime.timedelta(days=30)
print("Today:", today)
print("In 30 days:", today + delta)
print("Day of week:", today.strftime("%A"))

# math
print("pi:",    round(math.pi, 4))
print("sqrt(2):", round(math.sqrt(2), 4))
print("log2(1024):", math.log2(1024))"""},
{"label": "collections and itertools", "code":
"""from collections import Counter, defaultdict, namedtuple
import itertools

# Counter
words = "the quick brown fox jumps over the lazy dog the".split()
c = Counter(words)
print("Most common:", c.most_common(3))

# defaultdict
from collections import defaultdict
group = defaultdict(list)
data  = [("fruit","apple"),("veg","carrot"),("fruit","banana"),("veg","pea")]
for category, item in data:
    group[category].append(item)
print(dict(group))

# namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 7)
print(f"Point: x={p.x}, y={p.y}")

# itertools
pairs = list(itertools.combinations("ABCD", 2))
print("Combinations:", pairs)"""},
{"label": "functools and secrets", "code":
"""import functools, random, secrets

# functools.reduce — fold a sequence into a single value
from functools import reduce
product = reduce(lambda acc, x: acc * x, range(1, 6))  # 5! = 120
print("5! =", product)

# functools.partial — fix some arguments of a function
def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
cube   = functools.partial(power, exponent=3)
print("Squares:", [square(x) for x in range(1, 6)])
print("Cubes:  ", [cube(x)   for x in range(1, 6)])

# functools.lru_cache — memoize automatically
@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

print("fib(35):", fib(35))
print("Cache info:", fib.cache_info())

# random vs secrets
# random — reproducible (seeded), for simulations
random.seed(42)
sample = random.sample(range(100), 5)
print("Random sample:", sample)

# secrets — cryptographically secure, for tokens/passwords
token = secrets.token_hex(16)     # 32-char hex string
print("Secure token:", token)
pin   = secrets.randbelow(10000)  # 0-9999
print("Secure PIN: ", str(pin).zfill(4))"""},
{"label": "importlib, sys.path, __name__ guard, and pprint", "code":
"""import sys
import importlib
import pprint

# sys.path — where Python searches for modules
print("sys.path entries (first 3):")
for p in sys.argv[0:1]:    # avoid printing too many paths
    pass
for path in sys.path[:3]:
    print(f"  {path!r}")

# sys.argv — command-line arguments
print(f"Script name: {sys.argv[0]!r}")

# sys.version / sys.platform — runtime info
print(f"Python {sys.version.split()[0]} on {sys.platform}")

# importlib — dynamic import by string name
math_mod = importlib.import_module("math")
print(f"math.tau = {math_mod.tau:.6f}")

json_mod = importlib.import_module("json")
encoded  = json_mod.dumps({"key": "value"})
print("Dynamic json.dumps:", encoded)

# __name__ == "__main__" pattern
# This block only runs when the script is executed directly,
# NOT when it is imported as a module.
if __name__ == "__main__":
    print("Running as main script — __name__:", __name__)

# pprint — pretty-print complex nested structures
data = {
    "users": [
        {"id": 1, "name": "Alice", "roles": ["admin", "editor"],
         "prefs": {"theme": "dark", "lang": "en"}},
        {"id": 2, "name": "Bob",   "roles": ["viewer"],
         "prefs": {"theme": "light", "lang": "fr"}},
    ],
    "meta": {"version": "2.1", "count": 2}
}
print("\\npprint output:")
pprint.pprint(data, width=60, sort_dicts=False)"""}
],
"practice": {
"title": "Analyze Dataset with Built-ins",
"desc": "Use the statistics module and built-in functions to compute mean/median/stdev, find top-5 and bottom-5 scores, and bin scores into letter grade counts with Counter.",
"starter":
"""import statistics
from collections import Counter

scores = [72, 88, 95, 63, 79, 91, 55, 84, 76, 90,
          67, 83, 58, 97, 71, 80, 89, 62, 75, 93]

# TODO: compute mean, median, stdev using statistics module
# mean   = statistics.mean(scores)
# median = statistics.median(scores)
# stdev  = statistics.stdev(scores)
# print(f"Mean: {mean:.1f}, Median: {median}, StdDev: {stdev:.1f}")

# TODO: use sorted() to get top_5 (highest) and bottom_5 (lowest)
# top_5    = sorted(scores, reverse=True)[:5]
# bottom_5 = sorted(scores)[:5]

# TODO: map each score to a letter grade bin
# def grade_bin(s): return "A" if s>=90 else "B" if s>=80 else "C" if s>=70 else "D" if s>=60 else "F"
# bins = Counter(grade_bin(s) for s in scores)
# print("Grade bins:", dict(sorted(bins.items())))

print("Top 5:   ", top_5)
print("Bottom 5:", bottom_5)"""
},
"rw": {
"title": "Web Request Log Analysis",
"scenario": "A backend engineer uses Counter and defaultdict to analyze HTTP access logs and detect suspicious patterns.",
"code":
"""from collections import Counter, defaultdict
import datetime

# Simulated access log entries: (ip, method, path, status, ts)
logs = [
    ("192.168.1.10", "GET",  "/home",     200, "2024-01-15 09:00:01"),
    ("10.0.0.5",     "POST", "/login",    401, "2024-01-15 09:00:03"),
    ("10.0.0.5",     "POST", "/login",    401, "2024-01-15 09:00:04"),
    ("10.0.0.5",     "POST", "/login",    401, "2024-01-15 09:00:05"),
    ("192.168.1.10", "GET",  "/products", 200, "2024-01-15 09:01:00"),
    ("172.16.0.1",   "GET",  "/admin",    403, "2024-01-15 09:01:30"),
    ("172.16.0.1",   "GET",  "/admin",    403, "2024-01-15 09:01:32"),
    ("192.168.1.20", "GET",  "/home",     200, "2024-01-15 09:02:00"),
    ("10.0.0.5",     "POST", "/login",    200, "2024-01-15 09:02:10"),
]

status_counts = Counter(entry[3] for entry in logs)
ip_requests   = Counter(entry[0] for entry in logs)
failures_by_ip = defaultdict(int)

for ip, method, path, status, ts in logs:
    if status in (401, 403):
        failures_by_ip[ip] += 1

print("Status codes:", dict(status_counts))
print("\nTop IPs:")
for ip, count in ip_requests.most_common():
    fails = failures_by_ip[ip]
    flag  = " ⚠️ SUSPICIOUS" if fails >= 2 else ""
    print(f"  {ip:16s} {count:3d} requests, {fails} failures{flag}")"""}
}

,
{
    "title": "13. Context Managers",
    "desc": "Manage resources safely and cleanly with the with statement. Guarantee teardown even when exceptions occur.",
    "examples": [
        {
            "label": "File handling with context managers",
            "code":
"""import tempfile, pathlib, os

# Bad pattern: manual open/close risks resource leak
# f = open('data.txt')
# data = f.read()  # if this raises, f never closes
# f.close()

# Good pattern: with statement guarantees close()
tmp = pathlib.Path(tempfile.mktemp(suffix='.txt'))
tmp.write_text('line 1\\nline 2\\nline 3')

with open(tmp) as f:
    data = f.read()
print('Read:', repr(data))

# Write mode
with open(tmp, 'a') as f:
    f.write('\\nline 4')

# File is closed here even if an exception happened inside

# Reading line by line (memory-efficient for large files)
with open(tmp) as f:
    for i, line in enumerate(f, 1):
        print(f'  {i}: {line.rstrip()}')

tmp.unlink()"""
        },
        {
            "label": "Multiple context managers in one with",
            "code":
"""import tempfile, pathlib

src = pathlib.Path(tempfile.mktemp(suffix='.txt'))
dst = pathlib.Path(tempfile.mktemp(suffix='.txt'))
src.write_text('hello from source')

# Open multiple files in one with statement
with open(src) as fin, open(dst, 'w') as fout:
    for line in fin:
        fout.write(line.upper())

print('Copied and uppercased:', dst.read_text())
src.unlink(); dst.unlink()

# Also works for nested managers of different types
import io
with io.StringIO('a,b,c\\n1,2,3') as buf:
    print('StringIO:', buf.read())"""
        },
        {
            "label": "Custom context manager with __enter__ / __exit__",
            "code":
"""import time

class Timer:
    def __init__(self, name='block'):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self  # value bound to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f'[{self.name}] elapsed: {self.elapsed*1000:.2f} ms')
        # Return False (default) to re-raise any exception
        return False

with Timer('sum of squares') as t:
    result = sum(x**2 for x in range(1_000_000))

print(f'Result: {result:,}, time stored: {t.elapsed*1000:.2f} ms')

# Suppress specific exceptions by returning True from __exit__
class Suppress:
    def __init__(self, *exc_types):
        self.exc_types = exc_types
    def __enter__(self): return self
    def __exit__(self, exc_type, *_):
        return exc_type in self.exc_types

with Suppress(ZeroDivisionError):
    x = 1 / 0  # suppressed!
print('Continued after ZeroDivisionError')"""
        },
        {
            "label": "contextlib.contextmanager decorator",
            "code":
"""from contextlib import contextmanager, suppress
import tempfile, pathlib

@contextmanager
def temporary_file(suffix='.txt', content=''):
    \"\"\"Create a temp file, yield its path, delete on exit.\"\"\"
    path = pathlib.Path(tempfile.mktemp(suffix=suffix))
    path.write_text(content)
    try:
        yield path
    finally:
        if path.exists():
            path.unlink()
        print(f'Cleaned up {path.name}')

@contextmanager
def log_section(name):
    print(f'>>> START: {name}')
    try:
        yield
    except Exception as e:
        print(f'>>> ERROR in {name}: {e}')
        raise
    finally:
        print(f'>>> END: {name}')

with temporary_file(content='hello world') as tmp:
    data = tmp.read_text()
    print('File content:', data)
# File is deleted here

with log_section('data processing'):
    result = [x**2 for x in range(5)]
    print('Result:', result)

# contextlib.suppress replaces try/except for known ignorable errors
with suppress(FileNotFoundError):
    pathlib.Path('nonexistent.txt').unlink()
print('Suppressed FileNotFoundError cleanly')"""
        }
    ],
    "rw_scenario": "A data pipeline opens database connections, acquires file locks, and logs section timings — all resources must be released even when a step throws an exception.",
    "rw_code":
"""from contextlib import contextmanager
import time, sqlite3, pathlib, tempfile

@contextmanager
def db_transaction(db_path):
    \"\"\"Auto-commit on success, rollback on exception.\"\"\"
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
        print('Transaction committed')
    except Exception as e:
        conn.rollback()
        print(f'Rollback due to: {e}')
        raise
    finally:
        conn.close()

@contextmanager
def timed_step(name):
    t0 = time.perf_counter()
    print(f'[START] {name}')
    yield
    print(f'[DONE]  {name} ({(time.perf_counter()-t0)*1000:.1f} ms)')

tmp_db = pathlib.Path(tempfile.mktemp(suffix='.db'))
try:
    with timed_step('pipeline'):
        with db_transaction(tmp_db) as conn:
            conn.execute('CREATE TABLE logs (msg TEXT, ts REAL)')
            conn.execute('INSERT INTO logs VALUES (?, ?)', ('start', time.time()))
            conn.execute('INSERT INTO logs VALUES (?, ?)', ('end',   time.time()))
        with db_transaction(tmp_db) as conn:
            rows = conn.execute('SELECT * FROM logs').fetchall()
            for row in rows:
                print(' ', row)
finally:
    tmp_db.unlink(missing_ok=True)""",
    "practice": {
        "title": "Database Connection Manager",
        "desc": "Write a context manager class DatabaseConnection that simulates opening/closing a DB connection (print messages). It should auto-rollback (print 'rolling back') if an exception occurs inside the with block, and auto-commit otherwise.",
        "starter":
"""class DatabaseConnection:
    def __init__(self, url):
        self.url = url
        self.connected = False

    def __enter__(self):
        # TODO: set self.connected = True, print 'Connected to {url}'
        # TODO: return self
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: if exception, print 'Rolling back', else print 'Committed'
        # TODO: print 'Disconnected', set connected = False
        # TODO: return False to propagate exceptions
        pass

# Test: should commit
with DatabaseConnection('sqlite:///app.db') as db:
    print(f'  Using connection (connected={db.connected})')

# Test: should rollback
try:
    with DatabaseConnection('sqlite:///app.db') as db:
        raise ValueError('Oops!')
except ValueError:
    pass"""
    }
},
{
    "title": "14. Regular Expressions",
    "desc": "Pattern matching and text extraction with the re module — character classes, groups, lookaheads, and real-world parsing patterns.",
    "examples": [
        {
            "label": "Basic patterns — search, match, findall",
            "code":
"""import re

text = 'Contact us at support@example.com or sales@company.org for help.'

# re.search — find first match anywhere in string
match = re.search(r'[\\w.+-]+@[\\w-]+\\.[\\w.]+', text)
if match:
    print('First email:', match.group())

# re.findall — return all matches as list
emails = re.findall(r'[\\w.+-]+@[\\w-]+\\.[\\w.]+', text)
print('All emails:', emails)

# re.match — only matches at START of string
print('match at start:', re.match(r'Contact', text))    # matches
print('match at start:', re.match(r'support', text))   # None

# re.fullmatch — entire string must match
phone = '555-1234'
valid = re.fullmatch(r'\\d{3}-\\d{4}', phone)
print('Valid phone:', bool(valid))

# Flags: case-insensitive
print(re.findall(r'contact', text, re.IGNORECASE))"""
        },
        {
            "label": "Groups and named groups",
            "code":
"""import re

log_line = '2024-03-15 09:23:41 ERROR [auth] Login failed for user: alice'

# Named groups with (?P<name>...)
pattern = r'(?P<date>\\d{4}-\\d{2}-\\d{2}) (?P<time>\\d{2}:\\d{2}:\\d{2}) (?P<level>\\w+) \\[(?P<module>\\w+)\\] (?P<message>.+)'
m = re.match(pattern, log_line)
if m:
    print('Date:   ', m.group('date'))
    print('Level:  ', m.group('level'))
    print('Module: ', m.group('module'))
    print('Message:', m.group('message'))
    print('Dict:   ', m.groupdict())

# Non-capturing groups (?:...)
urls = ['http://example.com', 'https://secure.org', 'ftp://old.net']
for url in urls:
    m = re.match(r'(?:https?|ftp)://([\\w.-]+)', url)
    if m:
        print(f'  Domain: {m.group(1)}'  # group(1) = first capturing group"""
        },
        {
            "label": "Substitution, splitting, and compiling",
            "code":
"""import re

text = 'Call us at (555) 123-4567 or 555.987.6543 today!'

# re.sub — replace pattern
cleaned = re.sub(r'[()\\s.-]', '', text)
print('Cleaned:', cleaned)

# Replace with backreference
normalized = re.sub(r'[()\\s.-]+?(\\d{3})[)\\s.-]+(\\d{3})[.-](\\d{4})', r'\\1-\\2-\\3', text)
print('Normalized:', normalized)

# re.split — split on pattern
sentence = 'one, two;   three | four'
words = re.split(r'[,;|]\\s*', sentence)
print('Split:', words)

# Compile for reuse (faster in loops)
EMAIL_RE = re.compile(r'[\\w.+-]+@[\\w-]+\\.[\\w.]+', re.IGNORECASE)
texts = ['alice@example.com is admin', 'no email here', 'bob@test.org rocks']
for t in texts:
    found = EMAIL_RE.findall(t)
    if found:
        print(f'  Found in "{t}": {found}')"""
        },
        {
            "label": "Common patterns — email, URL, date, IP address",
            "code":
"""import re

PATTERNS = {
    'email':   r'[\\w.+-]+@[\\w-]+\\.[\\w.]{2,}',
    'url':     r'https?://[\\w/:%#\\$&\\?\\(\\)~\\.=\\+\\-]+',
    'date':    r'\\b(\\d{4})[-/](\\d{1,2})[-/](\\d{1,2})\\b',
    'phone':   r'\\b\\d{3}[-.]\\d{3}[-.]\\d{4}\\b',
    'ipv4':    r'\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b',
    'hashtag': r'#[\\w]+',
}

sample = '''
Email me at john.doe@example.com by 2024-03-15.
Visit https://example.com/page?id=42 for details.
Call 555-123-4567. Server IP: 192.168.1.100
Twitter: #DataScience #Python
'''

for name, pattern in PATTERNS.items():
    matches = re.findall(pattern, sample)
    if matches:
        print(f'{name:8s}: {matches}')"""
        }
    ],
    "rw_scenario": "A log analytics system parses millions of Apache access log lines to extract IPs, timestamps, HTTP methods, paths, and status codes using compiled regex patterns.",
    "rw_code":
"""import re
from collections import Counter

LOG_PATTERN = re.compile(
    r'(?P<ip>[\\d.]+) - - \\[(?P<dt>[^\\]]+)\\] '
    r'"(?P<method>\\w+) (?P<path>[^\\s]+) HTTP/[\\d.]+" '
    r'(?P<status>\\d{3}) (?P<size>\\d+|-)'
)

log_lines = [
    '192.168.1.10 - - [15/Mar/2024:09:01:00 +0000] "GET /home HTTP/1.1" 200 1234',
    '10.0.0.5 - - [15/Mar/2024:09:01:01 +0000] "POST /login HTTP/1.1" 401 512',
    '10.0.0.5 - - [15/Mar/2024:09:01:02 +0000] "POST /login HTTP/1.1" 200 256',
    '172.16.0.1 - - [15/Mar/2024:09:02:00 +0000] "GET /admin HTTP/1.1" 403 64',
    '192.168.1.20 - - [15/Mar/2024:09:02:01 +0000] "GET /api/data HTTP/1.1" 200 4096',
]

records = [m.groupdict() for line in log_lines if (m := LOG_PATTERN.match(line))]

status_counts = Counter(r['status'] for r in records)
top_ips = Counter(r['ip'] for r in records)
errors = [r for r in records if r['status'].startswith(('4', '5'))]

print('Status codes:', dict(status_counts))
print('Top IPs:', dict(top_ips.most_common(3)))
print('Error requests:')
for e in errors:
    print(f"  {e['ip']} -> {e['method']} {e['path']} [{e['status']}]")""",
    "practice": {
        "title": "Data Extractor",
        "desc": "Write regex patterns to extract all email addresses, US phone numbers (xxx-xxx-xxxx format), and dollar amounts (e.g. $1,234.56) from the sample text below.",
        "starter":
"""import re

text = '''
Please contact billing@company.com or support@help.org.
Call 555-123-4567 or 800-555-9999 for support.
Invoice total: $1,234.56. Discount applied: $50.00.
Admin: admin@internal.net | Helpdesk: 312-555-0100
'''

EMAIL_PATTERN = re.compile(r'')   # TODO
PHONE_PATTERN = re.compile(r'')   # TODO
MONEY_PATTERN = re.compile(r'')   # TODO

print('Emails:', EMAIL_PATTERN.findall(text))
print('Phones:', PHONE_PATTERN.findall(text))
print('Amounts:', MONEY_PATTERN.findall(text))"""
    }
},
{
    "title": "15. Type Hints & Dataclasses",
    "desc": "Write self-documenting, IDE-friendly code with type annotations and eliminate boilerplate from data containers with @dataclass.",
    "examples": [
        {
            "label": "Basic type hints for functions",
            "code":
"""from typing import Optional, Union, List

def greet(name: str, times: int = 1) -> str:
    return ('Hello, ' + name + '! ') * times

def parse_int(value: Union[str, int]) -> Optional[int]:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def process(items: List[Union[int, float]]) -> float:
    return sum(items) / len(items) if items else 0.0

print(greet('Alice'))
print(greet('Bob', 3))
print(parse_int('42'))
print(parse_int('abc'))   # returns None
print(process([1, 2.5, 3, 4]))

# Python 3.10+ union syntax: int | str instead of Union[int, str]
def modern(x: int | str) -> str:
    return str(x)
print(modern(42))"""
        },
        {
            "label": "Generic types — List, Dict, Tuple, Callable",
            "code":
"""from typing import Dict, List, Tuple, Callable, TypeVar

T = TypeVar('T')

def first(items: List[T]) -> Optional[T]:
    return items[0] if items else None

def apply_all(funcs: List[Callable[[int], int]], value: int) -> List[int]:
    return [f(value) for f in funcs]

def parse_config(raw: Dict[str, str]) -> Dict[str, int]:
    return {k: int(v) for k, v in raw.items() if v.isdigit()}

Point = Tuple[float, float]
def distance(p1: Point, p2: Point) -> float:
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) ** 0.5

from typing import Optional
print(first([1, 2, 3]))          # 1
print(first([]))                 # None
print(apply_all([lambda x: x*2, lambda x: x+1], 5))  # [10, 6]
print(parse_config({'a': '10', 'b': 'hello', 'c': '5'}))
print(distance((0.0, 0.0), (3.0, 4.0)))  # 5.0"""
        },
        {
            "label": "@dataclass basics — auto-generated methods",
            "code":
"""from dataclasses import dataclass, field
from typing import List

@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

@dataclass
class Product:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    in_stock: bool = True

    def __post_init__(self):
        if self.price < 0:
            raise ValueError(f'Price cannot be negative: {self.price}')

p1 = Point(0, 0)
p2 = Point(3, 4)
print(p1)               # Point(x=0, y=0)
print(p2)               # Point(x=3, y=4)
print(p1 == Point(0,0)) # True — __eq__ auto-generated
print(p1.distance_to(p2))  # 5.0

laptop = Product('Laptop', 999.99, ['electronics', 'computers'])
print(laptop)
print(laptop.tags)

try:
    Product('Bad', -1)
except ValueError as e:
    print('Caught:', e)"""
        },
        {
            "label": "Advanced dataclass — frozen, order, slots",
            "code":
"""from dataclasses import dataclass, field
from typing import List
import functools

@dataclass(frozen=True)   # immutable — can be used in sets/dict keys
class Version:
    major: int
    minor: int
    patch: int = 0

    def __str__(self) -> str:
        return f'{self.major}.{self.minor}.{self.patch}'

@dataclass(order=True)    # auto-generates __lt__, __le__, __gt__, __ge__
class Employee:
    sort_index: float = field(init=False, repr=False)
    name: str
    salary: float
    dept: str

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.salary) if False else None
        self.sort_index = self.salary  # used for ordering

v1 = Version(1, 2, 3)
v2 = Version(1, 2, 3)
print(v1 == v2)     # True
print(hash(v1))     # hashable because frozen

try:
    v1.major = 2    # raises FrozenInstanceError
except Exception as e:
    print(type(e).__name__, e)

employees = [Employee('Carol', 95000, 'Eng'), Employee('Bob', 80000, 'Sales'), Employee('Alice', 110000, 'Eng')]
employees.sort()
for e in employees:
    print(f'  {e.name}: ${e.salary:,.0f}')"""
        }
    ],
    "rw_scenario": "A data pipeline uses typed dataclasses for each record type — Order, Customer, Product — giving IDE autocomplete, type-checker validation, and zero-boilerplate equality/hashing.",
    "rw_code":
"""from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Address:
    street: str
    city: str
    country: str = 'US'

@dataclass
class Customer:
    customer_id: int
    name: str
    email: str
    address: Address
    orders: List['Order'] = field(default_factory=list)

    def add_order(self, order: 'Order') -> None:
        self.orders.append(order)

    @property
    def total_spent(self) -> float:
        return sum(o.total for o in self.orders)

@dataclass
class Order:
    order_id: int
    items: List[str]
    amounts: List[float]
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> float:
        return sum(self.amounts)

addr = Address('123 Main St', 'Springfield')
customer = Customer(1, 'Alice Smith', 'alice@example.com', addr)
customer.add_order(Order(101, ['Laptop', 'Mouse'], [999.99, 29.99]))
customer.add_order(Order(102, ['Monitor'], [399.99]))

print(f'Customer: {customer.name} ({customer.email})')
print(f'Address:  {customer.address.city}, {customer.address.country}')
print(f'Orders:   {len(customer.orders)}')
print(f'Total spent: ${customer.total_spent:.2f}')""",
    "practice": {
        "title": "Typed Address Book",
        "desc": "Create a Person dataclass (name: str, age: int, email: str, phone: Optional[str] = None). Create an AddressBook dataclass holding a List[Person]. Add methods: add(person), find_by_name(name) -> Optional[Person], adults() -> List[Person] (age >= 18).",
        "starter":
"""from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Person:
    name: str
    age: int
    email: str
    phone: Optional[str] = None

@dataclass
class AddressBook:
    contacts: List[Person] = field(default_factory=list)

    def add(self, person: Person) -> None:
        # TODO
        pass

    def find_by_name(self, name: str) -> Optional[Person]:
        # TODO
        pass

    def adults(self) -> List[Person]:
        # TODO
        pass

book = AddressBook()
book.add(Person('Alice', 30, 'alice@example.com', '555-1234'))
book.add(Person('Bob', 17, 'bob@example.com'))
book.add(Person('Carol', 25, 'carol@example.com', '555-5678'))

print(book.find_by_name('Alice'))
print('Adults:', [p.name for p in book.adults()])"""
    }
},
{
    "title": "16. Concurrency & Async",
    "desc": "Speed up I/O-bound tasks with threading and asyncio, CPU-bound tasks with multiprocessing, and understand the GIL. Use concurrent.futures for clean parallel execution.",
    "examples": [
        {
            "label": "Threading for I/O-bound tasks",
            "code": """import threading
import time
import random

results = {}
lock = threading.Lock()

def fetch_data(url_id):
    '''Simulate an I/O-bound network call.'''
    time.sleep(random.uniform(0.05, 0.15))  # simulate latency
    data = f'data_from_endpoint_{url_id}'
    with lock:
        results[url_id] = data

# Sequential (slow)
t0 = time.perf_counter()
for i in range(5):
    fetch_data(i)
t_seq = time.perf_counter() - t0
print(f'Sequential: {t_seq:.3f}s')

# Threaded (fast for I/O)
results.clear()
threads = [threading.Thread(target=fetch_data, args=(i,)) for i in range(5)]
t0 = time.perf_counter()
for th in threads: th.start()
for th in threads: th.join()
t_thread = time.perf_counter() - t0
print(f'Threaded:   {t_thread:.3f}s  ({t_seq/t_thread:.1f}x faster)')
print('Results:', list(results.keys()))"""
        },
        {
            "label": "concurrent.futures ThreadPool & ProcessPool",
            "code": """from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time, math

def cpu_task(n):
    '''CPU-bound: compute sum of first n primes.'''
    primes, count = [], 2
    while len(primes) < n:
        if all(count % p != 0 for p in primes): primes.append(count)
        count += 1
    return sum(primes)

def io_task(delay):
    time.sleep(delay)
    return f'done after {delay:.2f}s'

# ThreadPool for I/O
delays = [0.05, 0.08, 0.06, 0.07, 0.05]
t0 = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as ex:
    futures = {ex.submit(io_task, d): d for d in delays}
    for f in as_completed(futures):
        pass
print(f'ThreadPool I/O: {time.perf_counter()-t0:.3f}s (sum={sum(delays):.2f}s serial)')

# ProcessPool for CPU (bypasses GIL)
tasks = [50, 60, 55, 65, 45]
t0 = time.perf_counter()
with ProcessPoolExecutor(max_workers=4) as ex:
    results = list(ex.map(cpu_task, tasks))
print(f'ProcessPool CPU: {time.perf_counter()-t0:.2f}s')
print('Sum of primes results:', results[:3], '...')"""
        },
        {
            "label": "asyncio for async I/O",
            "code": """import asyncio
import time

async def fetch(session_id, delay):
    '''Simulate async HTTP request.'''
    await asyncio.sleep(delay)
    return f'response_{session_id}'

async def main():
    delays = [0.1, 0.05, 0.08, 0.12, 0.06]

    # Sequential async (still fast but ordered)
    t0 = time.perf_counter()
    results = []
    for i, d in enumerate(delays):
        r = await fetch(i, d)
        results.append(r)
    print(f'Sequential async: {time.perf_counter()-t0:.3f}s')

    # Concurrent async (all at once)
    t0 = time.perf_counter()
    tasks = [fetch(i, d) for i, d in enumerate(delays)]
    results = await asyncio.gather(*tasks)
    print(f'Concurrent async: {time.perf_counter()-t0:.3f}s')
    print('Results:', results)

asyncio.run(main())"""
        },
        {
            "label": "Queue-based producer-consumer",
            "code": """import threading
import queue
import time
import random

def producer(q, n_items):
    for i in range(n_items):
        item = f'item_{i}'
        q.put(item)
        time.sleep(random.uniform(0.01, 0.03))
    q.put(None)  # sentinel

def consumer(q, results):
    while True:
        item = q.get()
        if item is None:
            break
        # Simulate processing
        time.sleep(random.uniform(0.005, 0.015))
        results.append(item.upper())
        q.task_done()

q       = queue.Queue(maxsize=5)
results = []

t0 = time.perf_counter()
prod = threading.Thread(target=producer, args=(q, 10))
cons = threading.Thread(target=consumer, args=(q, results))
prod.start(); cons.start()
prod.join(); cons.join()
print(f'Processed {len(results)} items in {time.perf_counter()-t0:.3f}s')
print('Processed:', results[:5], '...')"""
        }
    ],
    "rw_scenario": "A data pipeline fetches stock prices from 20 API endpoints concurrently, processes them in parallel (CPU), and writes results to a queue for downstream consumption.",
    "rw_code": """from concurrent.futures import ThreadPoolExecutor, as_completed
import time, random

def fetch_price(ticker):
    '''Simulate API call.'''
    time.sleep(random.uniform(0.05, 0.2))
    return ticker, round(random.uniform(10, 500), 2)

def process_price(ticker, price):
    '''Compute simple moving average signal.'''
    history = [price * (1 + random.gauss(0, 0.01)) for _ in range(20)]
    ma = sum(history) / len(history)
    return {'ticker': ticker, 'price': price, 'ma20': round(ma, 2),
            'signal': 'BUY' if price < ma else 'SELL'}

tickers = [f'TICK{i}' for i in range(20)]

t0 = time.perf_counter()
signals = []
with ThreadPoolExecutor(max_workers=10) as ex:
    futures = {ex.submit(fetch_price, t): t for t in tickers}
    for future in as_completed(futures):
        ticker, price = future.result()
        signals.append(process_price(ticker, price))

t_total = time.perf_counter() - t0
print(f'Fetched & processed {len(signals)} tickers in {t_total:.2f}s')
buys  = [s for s in signals if s['signal'] == 'BUY']
sells = [s for s in signals if s['signal'] == 'SELL']
print(f'BUY: {len(buys)}, SELL: {len(sells)}')""",
    "practice": {
        "title": "Parallel Web Scraper Simulation",
        "desc": "Simulate fetching 15 URLs concurrently with ThreadPoolExecutor. Each 'fetch' sleeps for a random 0.05–0.3s and returns a fake HTML string. Collect results in order. Measure speedup vs sequential. Also implement a version using asyncio.gather. Report total time for both.",
        "starter": """from concurrent.futures import ThreadPoolExecutor
import asyncio, time, random

URLS = [f'https://example.com/page/{i}' for i in range(15)]

def sync_fetch(url):
    time.sleep(random.uniform(0.05, 0.3))
    return f'<html>{url}</html>'

async def async_fetch(url):
    await asyncio.sleep(random.uniform(0.05, 0.3))
    return f'<html>{url}</html>'

# TODO: (1) ThreadPoolExecutor: fetch all URLs, measure time
# TODO: (2) asyncio.gather: fetch all URLs, measure time
# TODO: (3) Print speedup vs sequential (sum of delays)
"""
    }
},
{
    "title": "17. Design Patterns",
    "desc": "Apply classic Gang-of-Four patterns in Python: Singleton, Factory, Observer, Strategy, and Decorator. Understand when and why to use each.",
    "examples": [
        {
            "label": "Singleton and Factory patterns",
            "code": """# Singleton: one instance per process
class DatabasePool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connections = []
            print('Creating new DatabasePool')
        return cls._instance

    def connect(self, host):
        self.connections.append(host)
        return f'Connected to {host}'

pool1 = DatabasePool()
pool2 = DatabasePool()
print('Same instance:', pool1 is pool2)
pool1.connect('db1.server.com')
print('Connections visible from pool2:', pool2.connections)

# Factory: create objects without knowing exact class
class Shape:
    def area(self): raise NotImplementedError

class Circle:
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r**2
    def __repr__(self): return f'Circle(r={self.r})'

class Rectangle:
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h
    def __repr__(self): return f'Rectangle({self.w}x{self.h})'

def shape_factory(kind, **kwargs):
    shapes = {'circle': Circle, 'rectangle': Rectangle}
    if kind not in shapes: raise ValueError(f'Unknown shape: {kind}')
    return shapes[kind](**kwargs)

for spec in [('circle', {'r': 5}), ('rectangle', {'w': 4, 'h': 6})]:
    s = shape_factory(spec[0], **spec[1])
    print(f'{s}: area={s.area():.2f}')"""
        },
        {
            "label": "Observer pattern (event system)",
            "code": """from typing import Callable, Dict, List

class EventBus:
    '''Simple publish-subscribe event system.'''
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event: str, handler: Callable):
        self._handlers.setdefault(event, []).append(handler)
        return self  # fluent API

    def publish(self, event: str, **data):
        for handler in self._handlers.get(event, []):
            handler(**data)

    def unsubscribe(self, event: str, handler: Callable):
        if event in self._handlers:
            self._handlers[event] = [h for h in self._handlers[event] if h != handler]

# Usage
bus = EventBus()

def on_order_placed(order_id, amount, user):
    print(f'[EMAIL]   Order #{order_id} placed by {user}: ${amount:.2f}')

def on_order_placed_analytics(order_id, amount, **_):
    print(f'[ANALYTICS] Recorded order #{order_id}, revenue=${amount:.2f}')

def on_order_placed_inventory(order_id, **_):
    print(f'[INVENTORY] Reducing stock for order #{order_id}')

bus.subscribe('order.placed', on_order_placed)
bus.subscribe('order.placed', on_order_placed_analytics)
bus.subscribe('order.placed', on_order_placed_inventory)

# Trigger event
bus.publish('order.placed', order_id=1042, amount=149.99, user='Alice')"""
        },
        {
            "label": "Strategy pattern",
            "code": """from abc import ABC, abstractmethod
from typing import List

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...

class BubbleSort(SortStrategy):
    def sort(self, data):
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

class MergeSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1: return data[:]
        mid = len(data) // 2
        L, R = self.sort(data[:mid]), self.sort(data[mid:])
        result, i, j = [], 0, 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: result.append(L[i]); i += 1
            else:             result.append(R[j]); j += 1
        return result + L[i:] + R[j:]

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)

import time, random
data = random.sample(range(1000), 20)
sorter = Sorter(BubbleSort())
print('Bubble:', sorter.sort(data)[:5], '...')

sorter.set_strategy(MergeSort())  # swap strategy at runtime
print('Merge: ', sorter.sort(data)[:5], '...')"""
        },
        {
            "label": "Decorator and Mixin patterns",
            "code": """import time, functools

# Function decorator: retry with backoff
def retry(max_attempts=3, delay=0.01):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts+1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    print(f'  Attempt {attempt} failed: {e}. Retrying...')
                    time.sleep(delay)
        return wrapper
    return decorator

import random
@retry(max_attempts=4)
def flaky_api_call():
    if random.random() < 0.6: raise ConnectionError('Timeout')
    return 'Success!'

random.seed(42)
print('Result:', flaky_api_call())

# Mixin pattern: add logging capability to any class
class LogMixin:
    def log(self, msg): print(f'[{self.__class__.__name__}] {msg}')

class TimeMixin:
    def timed(self, func, *args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        self.log(f'{func.__name__} took {(time.perf_counter()-t0)*1000:.2f}ms')
        return result

class DataProcessor(LogMixin, TimeMixin):
    def process(self, data):
        import math
        return [math.sqrt(abs(x)) for x in data]

p = DataProcessor()
p.log('Starting processing')
result = p.timed(p.process, list(range(-100, 100)))
print('Sample output:', [round(x,2) for x in result[:5]])"""
        }
    ],
    "rw_scenario": "A machine learning serving system uses Factory to create model objects (sklearn, pytorch, onnx), Observer to notify logging/monitoring services on predictions, and Strategy to swap preprocessing pipelines.",
    "rw_code": """from abc import ABC, abstractmethod

# Factory for ML models
class BaseModel(ABC):
    @abstractmethod
    def predict(self, X): ...

class SKLearnModel(BaseModel):
    def __init__(self, model_path):
        self.name = f'sklearn:{model_path}'
    def predict(self, X): return [f'sklearn_pred_{i}' for i in range(len(X))]

class ONNXModel(BaseModel):
    def __init__(self, model_path):
        self.name = f'onnx:{model_path}'
    def predict(self, X): return [f'onnx_pred_{i}' for i in range(len(X))]

def model_factory(runtime: str, path: str) -> BaseModel:
    models = {'sklearn': SKLearnModel, 'onnx': ONNXModel}
    if runtime not in models: raise ValueError(f'Unknown runtime: {runtime}')
    return models[runtime](path)

# Observer for monitoring
class PredictionMonitor:
    def on_predict(self, model_name, n_samples, **_):
        print(f'[MONITOR] {model_name}: {n_samples} samples')

class LatencyLogger:
    def on_predict(self, latency_ms, **_):
        print(f'[LATENCY] {latency_ms:.1f}ms')

handlers = [PredictionMonitor(), LatencyLogger()]
def publish(event, **data):
    [getattr(h, f'on_{event}')(**data) for h in handlers if hasattr(h, f'on_{event}')]

import time
model = model_factory('sklearn', 'fraud_v2.pkl')
X = [[1,2,3]] * 10
t0 = time.perf_counter()
preds = model.predict(X)
latency = (time.perf_counter()-t0)*1000
publish('predict', model_name=model.name, n_samples=len(X), latency_ms=latency)
print('Predictions:', preds[:3])""",
    "practice": {
        "title": "Plugin System with Factory + Observer",
        "desc": "Build a data export plugin system: (1) Factory creates exporter objects (CSV, JSON, Parquet) based on format string. Each implements export(data, path). (2) Observer pattern: attach at least 2 listeners (Logger, FileSizeChecker) that react to 'export_complete' events. Test with a list of 100 dicts as data.",
        "starter": """from abc import ABC, abstractmethod

class BaseExporter(ABC):
    @abstractmethod
    def export(self, data, path): ...

class CSVExporter(BaseExporter):
    def export(self, data, path):
        # TODO: write CSV using csv module or simple join
        pass

class JSONExporter(BaseExporter):
    def export(self, data, path):
        # TODO: write JSON using json module
        pass

def exporter_factory(fmt: str) -> BaseExporter:
    # TODO: return correct exporter based on fmt
    pass

# TODO: EventBus or simple list of observers
# TODO: Logger observer: print 'Exported N rows to path'
# TODO: FileSizeChecker observer: print file size

data = [{'id': i, 'value': i*2, 'name': f'item_{i}'} for i in range(100)]
# TODO: export to 'output.csv' and 'output.json', trigger events
"""
    }
},
{
    "title": "18. Testing with pytest",
    "desc": "Write unit tests, parametrized tests, fixtures, and mocks with pytest. Apply TDD principles and measure code coverage.",
    "examples": [
        {
            "label": "Basic pytest structure and assertions",
            "code": """# test_math_utils.py  (run with: pytest test_math_utils.py -v)
# Here we demonstrate by running inline
import traceback

def add(a, b): return a + b
def divide(a, b):
    if b == 0: raise ZeroDivisionError('Cannot divide by zero')
    return a / b
def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n**0.5)+1))

# --- Tests ---
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_divide():
    assert divide(10, 2) == 5.0
    assert abs(divide(1, 3) - 0.333) < 0.001

def test_divide_by_zero():
    try:
        divide(5, 0)
        assert False, 'Should have raised'
    except ZeroDivisionError:
        pass  # expected

def test_is_prime():
    primes     = [2, 3, 5, 7, 11, 13]
    non_primes = [0, 1, 4, 6, 9, 15]
    assert all(is_prime(p) for p in primes)
    assert not any(is_prime(n) for n in non_primes)

# Run all tests
tests = [test_add, test_divide, test_divide_by_zero, test_is_prime]
for t in tests:
    try: t(); print(f'PASS {t.__name__}')
    except AssertionError as e: print(f'FAIL {t.__name__}: {e}')"""
        },
        {
            "label": "Fixtures and parametrize",
            "code": """# Demonstrate pytest fixture and parametrize patterns
import os, tempfile

# === Fixture pattern ===
class FakeDB:
    def __init__(self):
        self.data = {}
    def insert(self, key, val): self.data[key] = val
    def get(self, key): return self.data.get(key)
    def count(self): return len(self.data)

# In pytest: @pytest.fixture
def db_fixture():
    '''Provide a fresh DB for each test.'''
    return FakeDB()

# === Parametrize pattern ===
# In pytest: @pytest.mark.parametrize('a,b,expected', [...])
def check_multiply(a, b, expected):
    assert a * b == expected, f'{a}*{b} should be {expected}'

params = [(2, 3, 6), (0, 100, 0), (-1, -1, 1), (7, 8, 56)]
for a, b, exp in params:
    try: check_multiply(a, b, exp); print(f'PASS multiply({a},{b})={exp}')
    except AssertionError as e: print(f'FAIL: {e}')

# === Fixture with temp file ===
def test_file_write():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('hello world')
        fname = f.name
    try:
        content = open(fname).read()
        assert content == 'hello world'
        print('PASS test_file_write')
    finally:
        os.unlink(fname)

db = db_fixture()
db.insert('user1', {'name': 'Alice'})
assert db.count() == 1
assert db.get('user1')['name'] == 'Alice'
print('PASS db fixture test')
test_file_write()"""
        },
        {
            "label": "Mocking with unittest.mock",
            "code": """from unittest.mock import patch, MagicMock, call
import json

# Function that depends on an external service
def fetch_user(user_id: int) -> dict:
    import urllib.request
    url = f'https://api.example.com/users/{user_id}'
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())

def process_user(user_id: int) -> str:
    user = fetch_user(user_id)
    return f'{user[\"name\"]} ({user[\"email\"]})'

# Test without hitting real API
mock_response = MagicMock()
mock_response.read.return_value = json.dumps({'name': 'Alice', 'email': 'alice@co.com'}).encode()
mock_response.__enter__ = lambda s: s
mock_response.__exit__ = MagicMock(return_value=False)

with patch('urllib.request.urlopen', return_value=mock_response):
    result = process_user(42)
    print(f'PASS: process_user(42) = {result!r}')

# Test exception handling
def robust_fetch(user_id):
    try:
        return fetch_user(user_id)
    except Exception as e:
        return {'error': str(e)}

with patch('urllib.request.urlopen', side_effect=ConnectionError('Network down')):
    r = robust_fetch(99)
    assert 'error' in r
    print(f'PASS: error handled: {r}')

# Verify mock was called correctly
mock_fn = MagicMock(return_value=42)
mock_fn(1, 2, key='val')
mock_fn(3, 4)
mock_fn.assert_called_with(3, 4)
print('PASS: mock call verification')"""
        },
        {
            "label": "Property-based testing with hypothesis",
            "code": """try:
    from hypothesis import given, strategies as st, settings

    # Property: sort is idempotent
    @given(st.lists(st.integers(), max_size=50))
    @settings(max_examples=200)
    def test_sort_idempotent(lst):
        sorted_once  = sorted(lst)
        sorted_twice = sorted(sorted_lst := sorted(lst))
        assert sorted_once == sorted_twice

    # Property: reversed reversed = original
    @given(st.lists(st.integers(), max_size=100))
    def test_reverse_involution(lst):
        assert list(reversed(list(reversed(lst)))) == lst

    # Property: split+join roundtrip
    @given(st.text(alphabet='abcdefghijklmnopqrstuvwxyz ', min_size=1, max_size=50))
    def test_split_join_roundtrip(s):
        words = s.split()
        rejoined = ' '.join(words)
        assert rejoined == ' '.join(s.split())

    test_sort_idempotent()
    test_reverse_involution()
    test_split_join_roundtrip()
    print('PASS: all hypothesis property tests')

except ImportError:
    print('pip install hypothesis')
    print('Hypothesis generates hundreds of random inputs automatically.')
    print('Properties to test: commutativity, idempotence, round-trips, invariants.')

    # Demo without hypothesis: manual property tests
    import random
    random.seed(42)
    for _ in range(100):
        lst = [random.randint(-100, 100) for _ in range(random.randint(0, 30))]
        assert sorted(sorted(lst)) == sorted(lst), 'Sort not idempotent!'
    print('PASS: manual sort idempotence test (100 random lists)')"""
        }
    ],
    "rw_scenario": "A data pipeline function clean_and_validate(df) drops nulls, clips outliers, and validates schema. Write a full pytest test suite with fixtures (sample DataFrames), parametrized edge cases, and mock for database writes.",
    "rw_code": """import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Function under test
def clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = {'id', 'value', 'category'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f'Missing columns: {required_cols - set(df.columns)}')
    df = df.dropna(subset=['value'])
    # Clip outliers (IQR method)
    q1, q3 = df['value'].quantile([0.25, 0.75])
    iqr = q3 - q1
    df = df[df['value'].between(q1 - 1.5*iqr, q3 + 1.5*iqr)].copy()
    return df

# --- Test suite ---
def make_sample_df(n=50, seed=42):
    np.random.seed(seed)
    return pd.DataFrame({
        'id':       range(n),
        'value':    np.random.randn(n),
        'category': np.random.choice(['A','B','C'], n),
    })

def test_drops_nulls():
    df = make_sample_df()
    df.loc[0, 'value'] = np.nan
    result = clean_and_validate(df)
    assert result['value'].isna().sum() == 0, 'Nulls remain'
    print('PASS test_drops_nulls')

def test_clips_outliers():
    df = make_sample_df()
    df.loc[0, 'value'] = 999  # extreme outlier
    result = clean_and_validate(df)
    assert result['value'].max() < 999, 'Outlier not removed'
    print('PASS test_clips_outliers')

def test_missing_columns():
    df = pd.DataFrame({'id': [1], 'value': [1.0]})  # missing 'category'
    try: clean_and_validate(df); print('FAIL: should raise')
    except ValueError as e: print(f'PASS test_missing_columns: {e}')

for test in [test_drops_nulls, test_clips_outliers, test_missing_columns]:
    test()""",
    "practice": {
        "title": "Test a Data Validation Class",
        "desc": "Implement and test a DataValidator class with methods: validate_types(df) checks column dtypes, validate_ranges(df, rules) checks min/max per column, validate_no_nulls(df, cols) checks specific columns. Write at least 6 tests covering: passing validation, each failure mode, and edge cases (empty df, single row).",
        "starter": """import pandas as pd
import numpy as np

class DataValidator:
    def validate_types(self, df: pd.DataFrame, expected: dict) -> list:
        '''Return list of (col, actual, expected) for mismatches.'''
        # TODO: compare df[col].dtype.kind vs expected type chars
        pass

    def validate_ranges(self, df: pd.DataFrame, rules: dict) -> list:
        '''rules = {col: (min, max)}. Return list of violations.'''
        # TODO: for each col, check if any values outside range
        pass

    def validate_no_nulls(self, df: pd.DataFrame, cols: list) -> list:
        '''Return cols that contain nulls.'''
        # TODO: check each column for nulls
        pass

# Test functions
def test_valid_types(): ...  # TODO
def test_invalid_type(): ...  # TODO
def test_range_pass(): ...   # TODO
def test_range_fail(): ...   # TODO
def test_no_nulls_pass(): ...  # TODO
def test_no_nulls_fail(): ...  # TODO

# Run all
for t in [test_valid_types, test_invalid_type, test_range_pass,
          test_range_fail, test_no_nulls_pass, test_no_nulls_fail]:
    t()
"""
    }
},

{
"title": "19. Functional Programming",
"desc": "Python supports functional programming with map(), filter(), reduce(), and functools. These let you transform data declaratively without explicit loops.",
"examples": [
        {"label": "map() and filter() for data transformation", "code": "nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n\n# map() applies a function to every element\nsquares = list(map(lambda x: x**2, nums))\nprint(\"Squares:\", squares)\n\n# filter() keeps elements where function returns True\nevens = list(filter(lambda x: x % 2 == 0, nums))\nprint(\"Evens:\", evens)\n\n# Chaining: square the even numbers\nresult = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))\nprint(\"Squared evens:\", result)\n\n# map with multiple iterables\na, b = [1, 2, 3], [10, 20, 30]\nsums = list(map(lambda x, y: x + y, a, b))\nprint(\"Pairwise sums:\", sums)"},
        {"label": "functools.reduce() and partial()", "code": "from functools import reduce, partial\n\nnums = [1, 2, 3, 4, 5]\n\n# reduce() accumulates a result across an iterable\ntotal = reduce(lambda acc, x: acc + x, nums)\nprint(\"Sum via reduce:\", total)\n\nproduct = reduce(lambda acc, x: acc * x, nums)\nprint(\"Product:\", product)\n\n# partial() freezes some arguments of a function\ndef power(base, exp):\n    return base ** exp\n\nsquare = partial(power, exp=2)\ncube   = partial(power, exp=3)\n\nprint(\"5 squared:\", square(5))\nprint(\"3 cubed:  \", cube(3))\n\n# partial with data processing\ndef scale(value, factor=1.0, offset=0.0):\n    return value * factor + offset\n\nnormalize = partial(scale, factor=0.1, offset=-0.5)\ndata = [0, 5, 10, 15, 20]\nprint(\"Normalized:\", list(map(normalize, data)))"},
        {"label": "Higher-order functions and function pipelines", "code": "from functools import reduce\n\n# A function that returns a function\ndef make_multiplier(n):\n    return lambda x: x * n\n\ndouble = make_multiplier(2)\ntriple = make_multiplier(3)\n\nprint(\"double(7):\", double(7))\nprint(\"triple(7):\", triple(7))\n\n# Build a pipeline of transformations\ndef pipeline(*funcs):\n    def apply(data):\n        return reduce(lambda v, f: f(v), funcs, data)\n    return apply\n\nprocess = pipeline(\n    lambda x: [v for v in x if v > 0],    # keep positives\n    lambda x: list(map(lambda v: v**0.5, x)),  # sqrt\n    lambda x: [round(v, 2) for v in x],   # round\n)\n\ndata = [-3, 4, 9, -1, 16, 25]\nprint(\"Input:\", data)\nprint(\"Output:\", process(data))"}
    ],
"rw": {
    "title": "Sales Data Cleaner",
    "scenario": "A data pipeline uses functional tools to clean and transform a list of raw sales records without mutating state.",
    "code": "from functools import reduce, partial\n\nrecords = [\n    {\"item\": \"apple\",  \"qty\": 3,  \"price\": 1.20, \"valid\": True},\n    {\"item\": \"banana\", \"qty\": -1, \"price\": 0.50, \"valid\": False},\n    {\"item\": \"cherry\", \"qty\": 10, \"price\": 2.00, \"valid\": True},\n]\n\n# Filter valid records\nvalid = list(filter(lambda r: r[\"valid\"] and r[\"qty\"] > 0, records))\n\n# Map to compute total\nwith_total = list(map(lambda r: {**r, \"total\": r[\"qty\"] * r[\"price\"]}, valid))\n\n# Reduce to grand total\ngrand = reduce(lambda acc, r: acc + r[\"total\"], with_total, 0.0)\n\nfor r in with_total:\n    print(f\'  {r[\"item\"]:8s}: ${r[\"total\"]:.2f}\')\nprint(f\"Grand total: ${grand:.2f}\")"
},
"practice": {
    "title": "Functional Data Processor",
    "desc": "Write a function process_data(numbers) that uses ONLY map(), filter(), and reduce() (no loops): remove negatives, multiply each by 3, return the sum. Then create a partial called process_small that pre-filters values below 100 before calling process_data.",
    "starter": "from functools import reduce, partial\n\ndef process_data(numbers):\n    # Step 1: filter out negatives with filter()\n    # Step 2: multiply each by 3 with map()\n    # Step 3: sum with reduce()\n    pass\n\n# Test\nprint(process_data([1, -2, 3, -4, 5]))  # expect 27\n\ndef keep_small(numbers, limit=100):\n    return [n for n in numbers if abs(n) < limit]\n\nprocess_small = partial(process_data, ...)  # TODO: use partial with keep_small\n"
}
},

{
"title": "20. Itertools in Depth",
"desc": "The itertools module provides fast, memory-efficient tools for working with iterables. Essential for combinatorics, grouping, and chaining data streams.",
"examples": [
        {"label": "chain, islice, cycle, repeat for sequence control", "code": "import itertools\n\n# chain: join multiple iterables\ncombined = list(itertools.chain([1, 2], [3, 4], [5]))\nprint(\"chain:\", combined)\n\n# islice: slice an iterable (works on generators too)\nfirst5 = list(itertools.islice(range(100), 5))\nprint(\"islice first 5:\", first5)\n\nskip3_take4 = list(itertools.islice(range(100), 3, 7))\nprint(\"islice [3:7]:\", skip3_take4)\n\n# cycle: repeat sequence infinitely — take 7\ncolors = list(itertools.islice(itertools.cycle([\'R\', \'G\', \'B\']), 7))\nprint(\"cycle 7:\", colors)\n\n# repeat: repeat a value n times\nzeros = list(itertools.repeat(0, 5))\nprint(\"repeat:\", zeros)\n\n# accumulate: running totals\nimport itertools\ndata = [1, 3, 2, 5, 4]\nrunning = list(itertools.accumulate(data))\nprint(\"accumulate (sum):\", running)"},
        {"label": "combinations, permutations, product", "code": "import itertools\n\nitems = [\'A\', \'B\', \'C\']\n\n# combinations: order does not matter, no repeats\ncombs = list(itertools.combinations(items, 2))\nprint(\"combinations(2):\", combs)\n\n# permutations: order matters\nperms = list(itertools.permutations(items, 2))\nprint(\"permutations(2):\", perms)\n\n# product: Cartesian product (like nested loops)\ncolors = [\'red\', \'blue\']\nsizes  = [\'S\', \'M\', \'L\']\nvariants = list(itertools.product(colors, sizes))\nprint(\"product:\", variants)\n\n# product with repeat: like rolling dice twice\ndice = list(itertools.product(range(1, 4), repeat=2))\nprint(\"dice pairs:\", dice[:6], \"...\")\n\nprint(f\"Combinations: {len(combs)}, Permutations: {len(perms)}, Product: {len(dice)}\")"},
        {"label": "groupby and takewhile/dropwhile", "code": "import itertools\n\n# groupby: group consecutive elements by a key\n# NOTE: input must be sorted by the key first!\ndata = [\n    {\"dept\": \"eng\",  \"name\": \"Alice\"},\n    {\"dept\": \"eng\",  \"name\": \"Bob\"},\n    {\"dept\": \"sales\",\"name\": \"Carol\"},\n    {\"dept\": \"sales\",\"name\": \"Dave\"},\n    {\"dept\": \"hr\",   \"name\": \"Eve\"},\n]\ndata.sort(key=lambda x: x[\"dept\"])\n\nfor dept, members in itertools.groupby(data, key=lambda x: x[\"dept\"]):\n    names = [m[\"name\"] for m in members]\n    print(f\"  {dept}: {names}\")\n\n# takewhile: take elements while condition is True\nnums = [2, 4, 6, 1, 8, 10]\ntaken = list(itertools.takewhile(lambda x: x % 2 == 0, nums))\nprint(\"takewhile even:\", taken)  # stops at 1\n\n# dropwhile: skip elements while condition is True\ndropped = list(itertools.dropwhile(lambda x: x % 2 == 0, nums))\nprint(\"dropwhile even:\", dropped)  # starts from 1"}
    ],
"rw": {
    "title": "Grid Search Parameter Iterator",
    "scenario": "A machine learning hyperparameter search uses itertools.product to enumerate all combinations of parameters without nested loops.",
    "code": "import itertools\n\nparam_grid = {\n    \"learning_rate\": [0.01, 0.1, 0.001],\n    \"max_depth\":     [3, 5, 7],\n    \"n_estimators\":  [50, 100],\n}\n\nkeys = list(param_grid.keys())\nvalues = list(param_grid.values())\n\nconfigs = list(itertools.product(*values))\nprint(f\"Total configs: {len(configs)}\")\n\nfor i, combo in enumerate(itertools.islice(configs, 3)):\n    cfg = dict(zip(keys, combo))\n    print(f\"  Config {i+1}: {cfg}\")\nprint(\"  ...\")"
},
"practice": {
    "title": "Itertools Combinatorics",
    "desc": "Write a function all_pairs(items) using itertools.combinations that returns all unique pairs. Write team_schedules(teams) using itertools.permutations(teams, 2) for home/away matchups. Write batch(iterable, n) using islice that yields chunks of size n.",
    "starter": "import itertools\n\ndef all_pairs(items):\n    # Return list of all unique 2-element combinations\n    pass\n\ndef team_schedules(teams):\n    # Return list of (home, away) tuples for all matchups\n    pass\n\ndef batch(iterable, n):\n    # Yield successive n-sized chunks from iterable\n    it = iter(iterable)\n    while True:\n        chunk = list(itertools.islice(it, n))\n        if not chunk:\n            break\n        yield chunk\n\n# Tests\nprint(all_pairs([\'A\',\'B\',\'C\',\'D\']))   # 6 pairs\nprint(len(team_schedules([\'X\',\'Y\',\'Z\'])))  # 6 matchups\nprint(list(batch(range(10), 3)))     # [[0,1,2],[3,4,5],[6,7,8],[9]]\n"
}
},

{
"title": "21. Closures & Scoping",
"desc": "Python resolves names using the LEGB rule (Local, Enclosing, Global, Built-in). Closures capture variables from enclosing scopes and are the foundation of decorators and factories.",
"examples": [
        {"label": "LEGB scoping rule", "code": "x = \"global\"\n\ndef outer():\n    x = \"enclosing\"\n\n    def inner():\n        x = \"local\"\n        print(\"inner sees:\", x)       # local\n\n    inner()\n    print(\"outer sees:\", x)           # enclosing\n\nouter()\nprint(\"module sees:\", x)              # global\n\n# Built-in scope: Python\'s built-in names (len, print, etc.)\nprint(\"built-in len:\", len([1,2,3]))  # 3\n\n# global keyword — modify a global from inside a function\ncounter = 0\ndef increment():\n    global counter\n    counter += 1\n\nincrement()\nincrement()\nprint(\"counter:\", counter)  # 2\n\n# nonlocal keyword — modify an enclosing variable\ndef make_counter():\n    count = 0\n    def inc():\n        nonlocal count\n        count += 1\n        return count\n    return inc\n\nc = make_counter()\nprint(c(), c(), c())  # 1 2 3"},
        {"label": "Closure factories", "code": "# A closure captures variables from its defining scope\n\ndef make_adder(n):\n    # n is captured in the closure\n    def add(x):\n        return x + n\n    return add\n\nadd5  = make_adder(5)\nadd10 = make_adder(10)\nprint(\"add5(3):\", add5(3))   # 8\nprint(\"add10(3):\", add10(3)) # 13\n\n# Each closure has its own cell\nprint(\"Different objects:\", add5 is not add10)  # True\n\n# Closure with mutable state\ndef make_accumulator():\n    total = 0\n    def accumulate(value):\n        nonlocal total\n        total += value\n        return total\n    return accumulate\n\nacc = make_accumulator()\nfor v in [10, 25, 5, 60]:\n    print(f\"  +{v} -> running total: {acc(v)}\")"},
        {"label": "Late binding and closure gotcha", "code": "# Common closure gotcha: late binding in loops\n# All closures share the SAME variable i\n\nfuncs_bad = [lambda: i for i in range(5)]\nprint(\"Late binding:\", [f() for f in funcs_bad])  # [4, 4, 4, 4, 4]!\n\n# Fix 1: capture current value as default argument\nfuncs_good = [lambda i=i: i for i in range(5)]\nprint(\"Default arg fix:\", [f() for f in funcs_good])  # [0, 1, 2, 3, 4]\n\n# Fix 2: use a factory function\ndef make_func(i):\n    def f():\n        return i\n    return f\n\nfuncs_factory = [make_func(i) for i in range(5)]\nprint(\"Factory fix:\", [f() for f in funcs_factory])  # [0, 1, 2, 3, 4]\n\n# Inspecting closure cells\nimport inspect\ndef outer(x):\n    def inner():\n        return x * 2\n    return inner\n\nfn = outer(7)\nprint(\"Closure cell value:\", fn.__closure__[0].cell_contents)  # 7"}
    ],
"rw": {
    "title": "Configurable Validator Factory",
    "scenario": "A data validation system uses closures to create reusable validators with baked-in limits, avoiding class overhead.",
    "code": "def make_range_validator(min_val, max_val, field=\"value\"):\n    def validate(x):\n        if not (min_val <= x <= max_val):\n            raise ValueError(f\"{field} {x} out of range [{min_val}, {max_val}]\")\n        return True\n    return validate\n\ndef make_str_validator(max_len, allowed_chars=None):\n    def validate(s):\n        if len(s) > max_len:\n            raise ValueError(f\"String too long: {len(s)} > {max_len}\")\n        if allowed_chars and not all(c in allowed_chars for c in s):\n            raise ValueError(f\"Invalid characters in: {s!r}\")\n        return True\n    return validate\n\nvalidate_age   = make_range_validator(0, 120, \"age\")\nvalidate_score = make_range_validator(0.0, 1.0, \"score\")\nvalidate_name  = make_str_validator(50, allowed_chars=\"abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ\")\n\ntests = [(validate_age, 25), (validate_score, 0.85), (validate_name, \"Alice Smith\")]\nfor validator, val in tests:\n    try:\n        print(f\"  OK: {val!r}\")\n        validator(val)\n    except ValueError as e:\n        print(f\"  FAIL: {e}\")"
},
"practice": {
    "title": "Memoize with Closure",
    "desc": "Write a function memoize(func) that returns a new function. The new function caches results in a dict (stored in a closure). It should handle any positional arguments as the cache key. Test it with a slow Fibonacci function and verify the cache speeds it up.",
    "starter": "def memoize(func):\n    cache = {}   # closure variable\n    def wrapper(*args):\n        # TODO: if args in cache, return cached result\n        # TODO: otherwise, call func(*args), store, return\n        pass\n    return wrapper\n\n@memoize\ndef fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)\n\nimport time\nt0 = time.time()\nprint(fib(35))     # should be fast after memoize\nprint(f\"Time: {time.time()-t0:.4f}s\")\n"
}
},

{
"title": "22. Decorators in Depth",
"desc": "Decorators wrap functions or classes to add behavior without modifying their source. Master stacked, parameterized, and class-based decorators.",
"examples": [
        {"label": "Stacked decorators and functools.wraps", "code": "import functools, time\n\ndef timer(func):\n    @functools.wraps(func)  # preserves __name__, __doc__\n    def wrapper(*args, **kwargs):\n        t0 = time.perf_counter()\n        result = func(*args, **kwargs)\n        print(f\"[timer] {func.__name__} took {(time.perf_counter()-t0)*1000:.2f}ms\")\n        return result\n    return wrapper\n\ndef logger(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f\"[logger] calling {func.__name__} with args={args}, kwargs={kwargs}\")\n        return func(*args, **kwargs)\n    return wrapper\n\n# Decorators apply bottom-up: logger wraps timer-wrapped function\n@logger\n@timer\ndef compute(n):\n    return sum(range(n))\n\nresult = compute(100_000)\nprint(\"Result:\", result)\nprint(\"Name preserved:\", compute.__name__)  # compute, not wrapper"},
        {"label": "Parameterized decorators (decorator factories)", "code": "import functools\n\ndef retry(times=3, exceptions=(Exception,)):\n    # Outer function receives decorator arguments\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            for attempt in range(1, times + 1):\n                try:\n                    return func(*args, **kwargs)\n                except exceptions as e:\n                    print(f\"  Attempt {attempt} failed: {e}\")\n                    if attempt == times:\n                        raise\n        return wrapper\n    return decorator\n\nattempt_count = 0\n\n@retry(times=3, exceptions=(ValueError,))\ndef unstable_fetch(url):\n    global attempt_count\n    attempt_count += 1\n    if attempt_count < 3:\n        raise ValueError(f\"Connection failed (attempt {attempt_count})\")\n    return f\"Data from {url}\"\n\nresult = unstable_fetch(\"https://api.example.com\")\nprint(\"Got:\", result)"},
        {"label": "Class-based decorators", "code": "import functools\n\nclass CallCounter:\n    # A class-based decorator that counts calls\n    def __init__(self, func):\n        functools.update_wrapper(self, func)\n        self.func  = func\n        self.count = 0\n\n    def __call__(self, *args, **kwargs):\n        self.count += 1\n        print(f\"[CallCounter] {self.func.__name__} called {self.count}x\")\n        return self.func(*args, **kwargs)\n\n@CallCounter\ndef add(a, b):\n    return a + b\n\nadd(1, 2)\nadd(3, 4)\nadd(5, 6)\nprint(\"Total calls:\", add.count)  # 3\n\n# Decorator that works on both functions and methods\nclass validate_positive:\n    def __init__(self, func):\n        functools.update_wrapper(self, func)\n        self.func = func\n\n    def __call__(self, *args, **kwargs):\n        for arg in args:\n            if isinstance(arg, (int, float)) and arg < 0:\n                raise ValueError(f\"Expected positive, got {arg}\")\n        return self.func(*args, **kwargs)\n\n@validate_positive\ndef sqrt(x):\n    return x ** 0.5\n\nprint(sqrt(9))   # 3.0\ntry:    sqrt(-1)\nexcept ValueError as e: print(\"Caught:\", e)"}
    ],
"rw": {
    "title": "Rate Limiter Decorator",
    "scenario": "A web scraper applies a rate-limiting decorator to avoid overloading target servers, with configurable calls-per-second.",
    "code": "import functools, time\n\ndef rate_limit(calls_per_second=1):\n    min_interval = 1.0 / calls_per_second\n    last_called = [0.0]  # mutable container to allow mutation in closure\n\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            elapsed = time.time() - last_called[0]\n            wait = min_interval - elapsed\n            if wait > 0:\n                print(f\"  Rate limit: waiting {wait:.2f}s\")\n                time.sleep(wait)\n            last_called[0] = time.time()\n            return func(*args, **kwargs)\n        return wrapper\n    return decorator\n\n@rate_limit(calls_per_second=2)\ndef fetch(url):\n    return f\"Response from {url}\"\n\nurls = [\"http://a.com\", \"http://b.com\", \"http://c.com\"]\nfor url in urls:\n    print(fetch(url))"
},
"practice": {
    "title": "Cache Decorator with TTL",
    "desc": "Write a parameterized decorator @cache(ttl=60) that caches function results for ttl seconds. After the TTL expires, re-call the function and refresh the cache. Use a dict with (args, timestamp) as cache entries. Test with a function that returns time.time() so you can observe expiry.",
    "starter": "import functools, time\n\ndef cache(ttl=60):\n    def decorator(func):\n        store = {}  # {args: (result, timestamp)}\n        @functools.wraps(func)\n        def wrapper(*args):\n            now = time.time()\n            if args in store:\n                result, ts = store[args]\n                if now - ts < ttl:\n                    print(f\"  [cache hit] age={now-ts:.1f}s\")\n                    return result\n            # TODO: call func, store result with timestamp, return result\n            pass\n        return wrapper\n    return decorator\n\n@cache(ttl=2)\ndef get_value(key):\n    return f\"{key}:{time.time():.2f}\"\n\nprint(get_value(\"x\"))\nprint(get_value(\"x\"))  # should be cache hit\ntime.sleep(2.1)\nprint(get_value(\"x\"))  # should re-fetch after TTL\n"
}
},

{
"title": "23. Abstract Base Classes & Protocols",
"desc": "ABCs enforce interface contracts at class creation time. Protocols (PEP 544) enable structural subtyping — duck typing with type-checker support.",
"examples": [
        {"label": "abc.ABC and @abstractmethod", "code": "from abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self) -> float:\n        pass\n\n    @abstractmethod\n    def perimeter(self) -> float:\n        pass\n\n    def describe(self):\n        # Concrete method shared by all subclasses\n        return f\"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}\"\n\nclass Circle(Shape):\n    def __init__(self, r): self.r = r\n    def area(self): return 3.14159 * self.r ** 2\n    def perimeter(self): return 2 * 3.14159 * self.r\n\nclass Rectangle(Shape):\n    def __init__(self, w, h): self.w, self.h = w, h\n    def area(self): return self.w * self.h\n    def perimeter(self): return 2 * (self.w + self.h)\n\nfor shape in [Circle(5), Rectangle(4, 6)]:\n    print(shape.describe())\n\n# Cannot instantiate ABC directly\ntry:\n    s = Shape()\nexcept TypeError as e:\n    print(\"Cannot instantiate:\", e)"},
        {"label": "typing.Protocol for structural subtyping", "code": "from typing import Protocol, runtime_checkable\n\n@runtime_checkable\nclass Drawable(Protocol):\n    def draw(self) -> str: ...\n    def get_color(self) -> str: ...\n\n# Any class with draw() and get_color() satisfies Drawable\n# No explicit inheritance required!\nclass Circle:\n    def draw(self): return \"O\"\n    def get_color(self): return \"red\"\n\nclass Square:\n    def draw(self): return \"[]\"\n    def get_color(self): return \"blue\"\n\nclass TextLabel:\n    def draw(self): return \"TEXT\"\n    def get_color(self): return \"black\"\n\ndef render(item: Drawable) -> str:\n    return f\"Drawing {item.draw()} in {item.get_color()}\"\n\nshapes = [Circle(), Square(), TextLabel()]\nfor s in shapes:\n    print(render(s))\n    print(f\"  isinstance check: {isinstance(s, Drawable)}\")"},
        {"label": "__subclasshook__ and virtual subclasses", "code": "from abc import ABC, abstractmethod\n\nclass Sized(ABC):\n    @abstractmethod\n    def __len__(self): ...\n\n    @classmethod\n    def __subclasshook__(cls, C):\n        # Automatically treat ANY class with __len__ as Sized\n        if cls is Sized:\n            if any(\"__len__\" in B.__dict__ for B in C.__mro__):\n                return True\n        return NotImplemented\n\n# list, dict, str all have __len__ — they are virtual subclasses\nprint(isinstance([], Sized))    # True\nprint(isinstance({}, Sized))    # True\nprint(isinstance(\"hi\", Sized))  # True\nprint(isinstance(42, Sized))    # False\n\n# Register a virtual subclass without inheritance\nclass SparseVector:\n    def __init__(self, data): self.data = data\n    def __len__(self): return len(self.data)\n\nprint(isinstance(SparseVector({0: 1.0}), Sized))  # True\nprint(issubclass(SparseVector, Sized))             # True"}
    ],
"rw": {
    "title": "Plugin Architecture with ABC",
    "scenario": "A data pipeline enforces that all data sources implement a common interface using ABC, then iterates over any registered source.",
    "code": "from abc import ABC, abstractmethod\nfrom typing import Iterator, Any\n\nclass DataSource(ABC):\n    @abstractmethod\n    def connect(self) -> bool: ...\n    @abstractmethod\n    def read(self) -> Iterator[Any]: ...\n    @abstractmethod\n    def close(self) -> None: ...\n\n    def stream(self):\n        if self.connect():\n            yield from self.read()\n            self.close()\n\nclass CSVSource(DataSource):\n    def __init__(self, rows):\n        self.rows = rows\n    def connect(self):\n        print(\"CSV: opening\"); return True\n    def read(self):\n        return iter(self.rows)\n    def close(self):\n        print(\"CSV: closed\")\n\nclass APISource(DataSource):\n    def __init__(self, data):\n        self.data = data\n    def connect(self):\n        print(\"API: authenticated\"); return True\n    def read(self):\n        return iter(self.data)\n    def close(self):\n        print(\"API: session ended\")\n\nfor src in [CSVSource([1,2,3]), APISource([\"a\",\"b\"])]:\n    for record in src.stream():\n        print(\" \", record)"
},
"practice": {
    "title": "Serializable Protocol",
    "desc": "Define a Protocol called Serializable with methods to_dict() -> dict and classmethod from_dict(cls, d: dict). Implement it on a Product(name, price, qty) class. Write a function save_all(items) that checks isinstance(item, Serializable) before converting each item to dict.",
    "starter": "from typing import Protocol, runtime_checkable\nfrom dataclasses import dataclass\n\n@runtime_checkable\nclass Serializable(Protocol):\n    def to_dict(self) -> dict: ...\n    # Note: classmethods in Protocols are tricky — just include to_dict for now\n\n@dataclass\nclass Product:\n    name: str\n    price: float\n    qty: int\n\n    def to_dict(self):\n        # TODO: return {\"name\": ..., \"price\": ..., \"qty\": ...}\n        pass\n\n    @classmethod\n    def from_dict(cls, d: dict):\n        # TODO: return cls(d[\"name\"], d[\"price\"], d[\"qty\"])\n        pass\n\ndef save_all(items):\n    results = []\n    for item in items:\n        if isinstance(item, Serializable):\n            results.append(item.to_dict())\n        else:\n            print(f\"Skipped: {item!r} is not Serializable\")\n    return results\n\nproducts = [Product(\"apple\", 1.2, 50), Product(\"banana\", 0.5, 200)]\nprint(save_all(products))\n"
}
},

{
"title": "24. Descriptors & Properties",
"desc": "Descriptors control attribute access via __get__, __set__, __delete__. The property() built-in is the most common descriptor. __slots__ reduces memory overhead.",
"examples": [
        {"label": "property getter, setter, deleter", "code": "class Temperature:\n    def __init__(self, celsius=0):\n        self._celsius = celsius  # private storage\n\n    @property\n    def celsius(self):\n        return self._celsius\n\n    @celsius.setter\n    def celsius(self, value):\n        if value < -273.15:\n            raise ValueError(f\"Temperature {value} below absolute zero!\")\n        self._celsius = value\n\n    @celsius.deleter\n    def celsius(self):\n        print(\"Resetting temperature to 0\")\n        self._celsius = 0\n\n    @property\n    def fahrenheit(self):\n        # Read-only computed property\n        return self._celsius * 9/5 + 32\n\nt = Temperature(25)\nprint(f\"{t.celsius}C = {t.fahrenheit}F\")\n\nt.celsius = 100\nprint(f\"Boiling: {t.celsius}C = {t.fahrenheit}F\")\n\ndel t.celsius\nprint(f\"Reset: {t.celsius}C\")\n\ntry:\n    t.celsius = -300\nexcept ValueError as e:\n    print(\"Caught:\", e)"},
        {"label": "Descriptor protocol (__get__, __set__, __delete__)", "code": "class Validated:\n    # A reusable descriptor for validated attributes\n    def __init__(self, min_val=None, max_val=None):\n        self.min_val = min_val\n        self.max_val = max_val\n        self.name = None  # set by __set_name__\n\n    def __set_name__(self, owner, name):\n        self.name = name  # called when class is defined\n\n    def __get__(self, obj, objtype=None):\n        if obj is None:\n            return self  # class-level access returns descriptor itself\n        return obj.__dict__.get(self.name, None)\n\n    def __set__(self, obj, value):\n        if self.min_val is not None and value < self.min_val:\n            raise ValueError(f\"{self.name} must be >= {self.min_val}, got {value}\")\n        if self.max_val is not None and value > self.max_val:\n            raise ValueError(f\"{self.name} must be <= {self.max_val}, got {value}\")\n        obj.__dict__[self.name] = value\n\nclass Person:\n    age    = Validated(min_val=0, max_val=150)\n    salary = Validated(min_val=0)\n\n    def __init__(self, name, age, salary):\n        self.name   = name\n        self.age    = age\n        self.salary = salary\n\np = Person(\"Alice\", 30, 75000)\nprint(f\"{p.name}: age={p.age}, salary={p.salary}\")\ntry:\n    p.age = -5\nexcept ValueError as e:\n    print(\"Caught:\", e)"},
        {"label": "__slots__ for memory efficiency", "code": "import sys\n\nclass PointNormal:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\nclass PointSlots:\n    __slots__ = (\'x\', \'y\')   # declare allowed attributes\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\nn = PointNormal(1.0, 2.0)\ns = PointSlots(1.0, 2.0)\n\nprint(f\"Without slots: {sys.getsizeof(n)} bytes, has __dict__: {hasattr(n, \'__dict__\')}\")\nprint(f\"With    slots: {sys.getsizeof(s)} bytes, has __dict__: {hasattr(s, \'__dict__\')}\")\n\n# Slots prevents adding arbitrary attributes\ntry:\n    s.z = 3.0\nexcept AttributeError as e:\n    print(\"Cannot add:\", e)\n\n# Memory comparison with many instances\nnormal_mem = sum(sys.getsizeof(PointNormal(i, i)) for i in range(1000))\nslots_mem  = sum(sys.getsizeof(PointSlots(i, i))  for i in range(1000))\nprint(f\"1000 objects — normal: {normal_mem} bytes, slots: {slots_mem} bytes\")\nprint(f\"Slots saves: {normal_mem - slots_mem} bytes ({(1-slots_mem/normal_mem)*100:.1f}%)\")"}
    ],
"rw": {
    "title": "Validated Configuration Class",
    "scenario": "A configuration system uses descriptors to validate settings when they are set, providing clear error messages without if-statement clutter in __init__.",
    "code": "class TypedAttr:\n    def __init__(self, expected_type, default=None):\n        self.expected_type = expected_type\n        self.default = default\n        self.name = None\n\n    def __set_name__(self, owner, name):\n        self.name = name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None: return self\n        return obj.__dict__.get(self.name, self.default)\n\n    def __set__(self, obj, value):\n        if not isinstance(value, self.expected_type):\n            raise TypeError(\n                f\"{self.name} must be {self.expected_type.__name__}, \"\n                f\"got {type(value).__name__}\"\n            )\n        obj.__dict__[self.name] = value\n\nclass AppConfig:\n    host     = TypedAttr(str, \"localhost\")\n    port     = TypedAttr(int, 8080)\n    debug    = TypedAttr(bool, False)\n    timeout  = TypedAttr(float, 30.0)\n\ncfg = AppConfig()\ncfg.host    = \"0.0.0.0\"\ncfg.port    = 443\ncfg.debug   = True\ncfg.timeout = 5.0\n\nprint(f\"Config: {cfg.host}:{cfg.port} debug={cfg.debug} timeout={cfg.timeout}s\")\n\ntry:\n    cfg.port = \"8080\"  # wrong type!\nexcept TypeError as e:\n    print(\"Caught:\", e)"
},
"practice": {
    "title": "Unit-Enforced Measurement",
    "desc": "Create a descriptor class UnitFloat(unit, min_val, max_val) that stores a float and records its unit. On __get__, return a namedtuple (value, unit). Create a class Measurement with descriptors for temperature (unit=\'C\', min=-273.15), pressure (unit=\'Pa\', min=0), and humidity (unit=\'%\', min=0, max=100).",
    "starter": "from collections import namedtuple\n\nclass UnitFloat:\n    Reading = namedtuple(\"Reading\", [\"value\", \"unit\"])\n\n    def __init__(self, unit, min_val=None, max_val=None):\n        self.unit    = unit\n        self.min_val = min_val\n        self.max_val = max_val\n        self.name    = None\n\n    def __set_name__(self, owner, name):\n        self.name = name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None: return self\n        val = obj.__dict__.get(self.name)\n        # TODO: return UnitFloat.Reading(val, self.unit) if val is not None else None\n        pass\n\n    def __set__(self, obj, value):\n        # TODO: validate type is float or int, validate min/max, store\n        pass\n\nclass Measurement:\n    temperature = UnitFloat(\"C\", min_val=-273.15)\n    pressure    = UnitFloat(\"Pa\", min_val=0)\n    humidity    = UnitFloat(\"%\", min_val=0, max_val=100)\n\nm = Measurement()\nm.temperature = 22.5\nm.pressure    = 101325.0\nm.humidity    = 65.0\nprint(m.temperature)  # Reading(value=22.5, unit=\'C\')\nprint(m.humidity)\n"
}
},

{
"title": "25. Memory Management & Profiling",
"desc": "Python manages memory via reference counting and a cyclic garbage collector. Use sys, gc, tracemalloc, and cProfile to find memory leaks and performance bottlenecks.",
"examples": [
        {"label": "sys.getsizeof, id(), and reference counting", "code": "import sys\n\n# Basic sizes\nfor obj in [0, 1, 255, 2**100, 3.14, \"hi\", \"hello world\", [], [1,2,3], {}, {\"a\":1}]:\n    print(f\"  {repr(obj):<25} {sys.getsizeof(obj):>6} bytes\")\n\n# id() returns memory address\na = [1, 2, 3]\nb = a          # same object\nc = a.copy()   # different object\n\nprint(\"a is b:\", a is b)  # True\nprint(\"a is c:\", a is c)  # False\nprint(\"id(a)==id(b):\", id(a) == id(b))  # True\n\n# Small integers are cached\nx, y = 100, 100\nprint(\"100 is 100:\", x is y)  # True (cached)\n\nx, y = 1000, 1000\nprint(\"1000 is 1000:\", x is y)  # False (not cached)\n\n# Nested containers: getsizeof is shallow!\nlst = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nprint(\"Shallow size:\", sys.getsizeof(lst))   # just the list object"},
        {"label": "gc module and reference cycles", "code": "import gc\n\nprint(\"GC enabled:\", gc.isenabled())\nprint(\"GC thresholds:\", gc.get_threshold())  # (700, 10, 10)\n\n# Reference cycle: a -> b -> a, both become unreachable\nclass Node:\n    def __init__(self, name):\n        self.name = name\n        self.ref = None\n\na = Node(\"A\")\nb = Node(\"B\")\na.ref = b  # a -> b\nb.ref = a  # b -> a (cycle!)\n\n# Delete our references\ndel a, b\n\nbefore = gc.collect(0)\nprint(f\"GC collected {before} objects in gen-0\")\n\n# Check what gc is tracking\ntracked = gc.get_count()\nprint(\"GC counts (gen0, gen1, gen2):\", tracked)\n\n# Use __del__ to observe collection\nclass Tracked:\n    def __del__(self):\n        print(f\"  {self!r} collected\")\n\nx = Tracked()\ndel x           # collected immediately (refcount -> 0)\ngc.collect()    # collect cycles"},
        {"label": "tracemalloc and cProfile", "code": "import tracemalloc, cProfile, io, pstats\n\n# --- tracemalloc: trace memory allocations ---\ntracemalloc.start()\n\nsnapshot1 = tracemalloc.take_snapshot()\nbig_list = [i**2 for i in range(10_000)]\nsnapshot2 = tracemalloc.take_snapshot()\n\nstats = snapshot2.compare_to(snapshot1, \"lineno\")\nfor stat in stats[:3]:\n    print(f\"  {stat}\")\n\ntracemalloc.stop()\ndel big_list\n\n# --- cProfile: find slow functions ---\ndef slow_sum(n):\n    return sum(i**2 for i in range(n))\n\ndef fast_sum(n):\n    return n * (n-1) * (2*n-1) // 6  # formula\n\npr = cProfile.Profile()\npr.enable()\nslow_sum(50_000)\nfast_sum(50_000)\npr.disable()\n\nsio = io.StringIO()\nps  = pstats.Stats(pr, stream=sio).sort_stats(\"cumulative\")\nps.print_stats(5)\nprint(sio.getvalue())"}
    ],
"rw": {
    "title": "Memory Leak Detector",
    "scenario": "A long-running service monitors its own memory usage between requests to detect leaks early.",
    "code": "import tracemalloc, sys\n\ndef deep_size(obj, seen=None):\n    # Recursively estimate size of a container\n    size = sys.getsizeof(obj)\n    if seen is None:\n        seen = set()\n    obj_id = id(obj)\n    if obj_id in seen:\n        return 0\n    seen.add(obj_id)\n    if isinstance(obj, dict):\n        size += sum(deep_size(v, seen) for v in obj.values())\n        size += sum(deep_size(k, seen) for k in obj.keys())\n    elif hasattr(obj, \'__iter__\') and not isinstance(obj, (str, bytes)):\n        size += sum(deep_size(i, seen) for i in obj)\n    return size\n\n# Simulate a request that leaks memory\ncache = {}\n\ndef handle_request(key, data):\n    cache[key] = data  # intentional \"leak\" into global cache\n    return len(data)\n\ntracemalloc.start()\nsnap1 = tracemalloc.take_snapshot()\n\nfor i in range(5):\n    handle_request(f\"req_{i}\", list(range(1000)))\n\nsnap2 = tracemalloc.take_snapshot()\ntop = snap2.compare_to(snap1, \"lineno\")[:2]\nfor stat in top:\n    print(f\"  Memory diff: {stat}\")\nprint(f\"Cache deep size: {deep_size(cache):,} bytes\")\ntracemalloc.stop()"
},
"practice": {
    "title": "Profile and Optimize",
    "desc": "Write two versions of a function that finds all prime numbers up to n: (1) trial_division(n) using a simple loop, (2) sieve(n) using the Sieve of Eratosthenes. Use timeit to benchmark both for n=10000. Use cProfile to show which lines of trial_division are slowest.",
    "starter": "import cProfile, timeit\n\ndef trial_division(n):\n    primes = []\n    for num in range(2, n+1):\n        if all(num % i != 0 for i in range(2, int(num**0.5)+1)):\n            primes.append(num)\n    return primes\n\ndef sieve(n):\n    is_prime = [True] * (n+1)\n    is_prime[0] = is_prime[1] = False\n    for i in range(2, int(n**0.5)+1):\n        if is_prime[i]:\n            for j in range(i*i, n+1, i):\n                is_prime[j] = False\n    return [i for i, p in enumerate(is_prime) if p]\n\nN = 10_000\n\n# Benchmark\nt1 = timeit.timeit(lambda: trial_division(N), number=3)\nt2 = timeit.timeit(lambda: sieve(N), number=3)\nprint(f\"trial_division: {t1:.3f}s\")\nprint(f\"sieve:          {t2:.3f}s\")\nprint(f\"Speedup: {t1/t2:.1f}x\")\n\n# Profile trial_division\ncProfile.run(\"trial_division(5000)\", sort=\"cumulative\")\n"
}
},

{
"title": "26. Logging Best Practices",
"desc": "Use the logging module instead of print() for production code. It supports levels, handlers, formatters, and log rotation — all configurable without code changes.",
"examples": [
        {"label": "Basic logging setup and levels", "code": "import logging\n\n# Configure root logger\nlogging.basicConfig(\n    level=logging.DEBUG,\n    format=\"%(asctime)s [%(levelname)-8s] %(name)s: %(message)s\",\n    datefmt=\"%H:%M:%S\",\n)\n\nlogger = logging.getLogger(\"myapp\")\n\n# Five standard levels (low to high)\nlogger.debug(\"Detailed info for debugging\")\nlogger.info(\"Normal operation: user logged in\")\nlogger.warning(\"Something unexpected but not fatal\")\nlogger.error(\"A failure occurred — function returned None\")\nlogger.critical(\"Service is down!\")\n\n# Log exceptions with traceback\ntry:\n    result = 1 / 0\nexcept ZeroDivisionError:\n    logger.exception(\"Division failed\")  # includes traceback\n\n# Extra context\nuser_id = 42\nlogger.info(\"Processing order\", extra={\"user\": user_id})\n\n# Check effective level\nprint(\"Effective level:\", logger.getEffectiveLevel())  # 10 = DEBUG"},
        {"label": "Multiple handlers and formatters", "code": "import logging, io\n\nlogger = logging.getLogger(\"pipeline\")\nlogger.setLevel(logging.DEBUG)\nlogger.handlers.clear()  # avoid duplicate handlers in notebooks\n\n# Handler 1: console with simple format\nch = logging.StreamHandler()\nch.setLevel(logging.WARNING)  # console only shows WARNING+\nch.setFormatter(logging.Formatter(\"%(levelname)s: %(message)s\"))\n\n# Handler 2: \"file\" (using StringIO here for demo)\nlog_buffer = io.StringIO()\nfh = logging.StreamHandler(log_buffer)\nfh.setLevel(logging.DEBUG)   # file gets everything\nfh.setFormatter(logging.Formatter(\n    \"%(asctime)s %(levelname)-8s [%(funcName)s:%(lineno)d] %(message)s\",\n    datefmt=\"%H:%M:%S\"\n))\n\nlogger.addHandler(ch)\nlogger.addHandler(fh)\n\ndef process(data):\n    logger.debug(\"Starting process with %d items\", len(data))\n    logger.info(\"Processing...\")\n    if not data:\n        logger.warning(\"Empty input\")\n    logger.debug(\"Done\")\n\nprocess([1, 2, 3])\nprocess([])\n\nprint(\"--- File log ---\")\nprint(log_buffer.getvalue())"},
        {"label": "Logger hierarchy and module-level loggers", "code": "import logging\n\n# Best practice: use __name__ as logger name\n# This creates a hierarchy: \"myapp\" -> \"myapp.db\" -> \"myapp.db.query\"\n\nroot = logging.getLogger()\napp  = logging.getLogger(\"myapp\")\ndb   = logging.getLogger(\"myapp.db\")\nqry  = logging.getLogger(\"myapp.db.query\")\n\n# Set up root handler for the demo\nlogging.basicConfig(\n    level=logging.DEBUG,\n    format=\"%(name)-20s %(levelname)s: %(message)s\"\n)\n\n# Child loggers propagate to parent by default\napp.setLevel(logging.INFO)\ndb.setLevel(logging.DEBUG)   # db subtree shows DEBUG\n\napp.info(\"App started\")\napp.debug(\"This won\'t show — app is INFO level\")\ndb.debug(\"DB connection established\")\nqry.debug(\"SELECT * FROM users\")\n\n# Disable propagation to avoid double-logging\n# child_logger.propagate = False\n\n# Silence noisy third-party libraries\nlogging.getLogger(\"urllib3\").setLevel(logging.WARNING)\nlogging.getLogger(\"boto3\").setLevel(logging.WARNING)\nprint(\"Third-party loggers silenced\")"}
    ],
"rw": {
    "title": "Pipeline Logger",
    "scenario": "A data processing pipeline uses structured logging to track progress, errors, and timing without print statements.",
    "code": "import logging, time, io\n\ndef setup_logger(name, level=logging.DEBUG):\n    log = logging.getLogger(name)\n    log.setLevel(level)\n    if not log.handlers:\n        h = logging.StreamHandler()\n        h.setFormatter(logging.Formatter(\n            \"%(asctime)s %(name)s %(levelname)-8s %(message)s\",\n            datefmt=\"%H:%M:%S\"\n        ))\n        log.addHandler(h)\n    return log\n\nlog = setup_logger(\"etl\")\n\ndef extract(source):\n    log.info(\"Extracting from %s\", source)\n    data = list(range(100))  # simulated data\n    log.debug(\"Extracted %d records\", len(data))\n    return data\n\ndef transform(data):\n    log.info(\"Transforming %d records\", len(data))\n    t0 = time.time()\n    result = [x * 2 for x in data if x % 5 != 0]\n    log.debug(\"Transform took %.3fs, %d records remain\", time.time()-t0, len(result))\n    return result\n\ndef load(data, target):\n    log.info(\"Loading %d records to %s\", len(data), target)\n    # Simulate occasional error\n    if len(data) > 70:\n        log.warning(\"Large batch — consider chunking\")\n    log.info(\"Load complete\")\n\ntry:\n    d = extract(\"sales.csv\")\n    d = transform(d)\n    load(d, \"warehouse\")\nexcept Exception:\n    log.exception(\"Pipeline failed\")"
},
"practice": {
    "title": "Log Analyzer",
    "desc": "Write a function parse_log_line(line) that extracts timestamp, level, and message from a log line like \'12:34:56 WARNING myapp: disk 90% full\'. Write analyze_logs(lines) that counts occurrences of each level and returns a dict like {\'WARNING\': 3, \'ERROR\': 1}. Use the logging module to emit a summary.",
    "starter": "import logging, re\nfrom collections import Counter\n\ndef parse_log_line(line):\n    # Pattern: HH:MM:SS LEVEL name: message\n    pattern = r\"(\\d{2}:\\d{2}:\\d{2}) (\\w+) (\\S+): (.+)\"\n    m = re.match(pattern, line)\n    if m:\n        return {\"time\": m.group(1), \"level\": m.group(2),\n                \"name\": m.group(3), \"msg\": m.group(4)}\n    return None\n\ndef analyze_logs(lines):\n    # TODO: parse each line, count levels, return Counter dict\n    pass\n\nsample_logs = [\n    \"12:00:01 INFO myapp: started\",\n    \"12:00:02 DEBUG myapp.db: query took 0.1s\",\n    \"12:00:03 WARNING myapp: memory 80% full\",\n    \"12:00:04 ERROR myapp: connection refused\",\n    \"12:00:05 WARNING myapp: retry 1/3\",\n]\n\ncounts = analyze_logs(sample_logs)\nprint(\"Level counts:\", counts)\n"
}
},

{
"title": "27. Argparse & CLI Tools",
"desc": "argparse is Python\'s standard library for building command-line interfaces. It handles argument parsing, type validation, help generation, and subcommands.",
"examples": [
        {"label": "Basic ArgumentParser with positional and optional args", "code": "import argparse\n\n# Simulate command-line arguments (replace sys.argv for demo)\nparser = argparse.ArgumentParser(\n    description=\"Process a data file\",\n    formatter_class=argparse.ArgumentDefaultsHelpFormatter\n)\n\n# Positional argument (required)\nparser.add_argument(\"filename\", help=\"Input CSV file path\")\n\n# Optional arguments\nparser.add_argument(\"-o\", \"--output\",  default=\"output.csv\", help=\"Output file\")\nparser.add_argument(\"-n\", \"--rows\",    type=int, default=100, help=\"Number of rows\")\nparser.add_argument(\"-v\", \"--verbose\", action=\"store_true\",   help=\"Verbose output\")\nparser.add_argument(\"--format\",        choices=[\"csv\",\"json\",\"parquet\"], default=\"csv\")\n\n# Parse a fake argument list\nargs = parser.parse_args([\"data.csv\", \"--rows\", \"500\", \"--verbose\", \"--format\", \"json\"])\n\nprint(f\"File:    {args.filename}\")\nprint(f\"Output:  {args.output}\")\nprint(f\"Rows:    {args.rows}\")\nprint(f\"Verbose: {args.verbose}\")\nprint(f\"Format:  {args.format}\")"},
        {"label": "Subcommands (subparsers)", "code": "import argparse\n\nparser = argparse.ArgumentParser(prog=\"datool\", description=\"Data pipeline tool\")\nsubs   = parser.add_subparsers(dest=\"command\", required=True)\n\n# Subcommand: convert\nconvert = subs.add_parser(\"convert\", help=\"Convert file format\")\nconvert.add_argument(\"input\",  help=\"Input file\")\nconvert.add_argument(\"output\", help=\"Output file\")\nconvert.add_argument(\"--compression\", choices=[\"none\",\"gzip\",\"snappy\"], default=\"none\")\n\n# Subcommand: stats\nstats = subs.add_parser(\"stats\", help=\"Show file statistics\")\nstats.add_argument(\"file\",  help=\"File to analyze\")\nstats.add_argument(\"--col\", action=\"append\", dest=\"cols\", help=\"Column to analyze (repeatable)\")\n\n# Subcommand: validate\nvalidate = subs.add_parser(\"validate\", help=\"Validate schema\")\nvalidate.add_argument(\"file\")\nvalidate.add_argument(\"--schema\", required=True)\n\n# Demo: parse \"convert\" command\nargs = parser.parse_args([\"convert\", \"input.csv\", \"output.parquet\", \"--compression\", \"snappy\"])\nprint(f\"Command:     {args.command}\")\nprint(f\"Input:       {args.input}\")\nprint(f\"Output:      {args.output}\")\nprint(f\"Compression: {args.compression}\")\n\n# Demo: parse \"stats\" command\nargs2 = parser.parse_args([\"stats\", \"data.csv\", \"--col\", \"price\", \"--col\", \"qty\"])\nprint(f\"Stats cols:  {args2.cols}\")"},
        {"label": "Argument groups, mutual exclusion, and type validators", "code": "import argparse\n\nparser = argparse.ArgumentParser(description=\"Model training CLI\")\n\n# Argument group for visual organization in --help\ndata_group = parser.add_argument_group(\"Data options\")\ndata_group.add_argument(\"--train\",  required=True, help=\"Training data path\")\ndata_group.add_argument(\"--val\",    required=True, help=\"Validation data path\")\ndata_group.add_argument(\"--test\",   help=\"Test data path\")\n\n# Argument group for model options\nmodel_group = parser.add_argument_group(\"Model options\")\nmodel_group.add_argument(\"--lr\",     type=float, default=0.001)\nmodel_group.add_argument(\"--epochs\", type=int,   default=10)\n\n# Mutually exclusive: can\'t use --gpu and --cpu together\ndevice = parser.add_mutually_exclusive_group()\ndevice.add_argument(\"--gpu\", action=\"store_true\")\ndevice.add_argument(\"--cpu\", action=\"store_true\")\n\n# Custom type validator\ndef positive_int(value):\n    ivalue = int(value)\n    if ivalue <= 0:\n        raise argparse.ArgumentTypeError(f\"{value} must be a positive integer\")\n    return ivalue\n\nmodel_group.add_argument(\"--batch\", type=positive_int, default=32)\n\nargs = parser.parse_args([\"--train\", \"train.csv\", \"--val\", \"val.csv\",\n                          \"--lr\", \"0.01\", \"--gpu\", \"--batch\", \"64\"])\nprint(vars(args))"}
    ],
"rw": {
    "title": "ETL Pipeline CLI",
    "scenario": "A data engineering team builds a CLI tool to run ETL jobs with configurable sources, targets, and options.",
    "code": "import argparse, sys\n\ndef run_etl(args):\n    print(f\"ETL Job: {args.job_name}\")\n    print(f\"  Source:   {args.source} (format={args.format})\")\n    print(f\"  Target:   {args.target}\")\n    print(f\"  Batch:    {args.batch_size}\")\n    print(f\"  Dry run:  {args.dry_run}\")\n\n    if args.dry_run:\n        print(\"  [DRY RUN] No data written.\")\n        return 0\n    print(\"  Writing data...\")\n    return 0\n\nparser = argparse.ArgumentParser(description=\"ETL Pipeline Runner\")\nparser.add_argument(\"job_name\",   help=\"Job identifier\")\nparser.add_argument(\"source\",     help=\"Source connection string\")\nparser.add_argument(\"target\",     help=\"Target connection string\")\nparser.add_argument(\"--format\",   choices=[\"csv\",\"json\",\"parquet\"], default=\"csv\")\nparser.add_argument(\"--batch-size\", type=int, default=1000, dest=\"batch_size\")\nparser.add_argument(\"--dry-run\",  action=\"store_true\", dest=\"dry_run\")\n\n# Demo\nargs = parser.parse_args([\n    \"daily_sales\", \"s3://bucket/sales.parquet\", \"postgres://db/warehouse\",\n    \"--format\", \"parquet\", \"--batch-size\", \"5000\", \"--dry-run\"\n])\nsys.exit(run_etl(args))"
},
"practice": {
    "title": "File Processor CLI",
    "desc": "Build a CLI with two subcommands: (1) count — takes a filename, optional --pattern (regex), prints count of matching lines; (2) summary — takes a filename, --cols (repeatable), prints first/last/count for each column in a CSV. Use argparse with proper help strings and type validation.",
    "starter": "import argparse, csv, re\n\nparser = argparse.ArgumentParser(prog=\"fileproc\")\nsubs = parser.add_subparsers(dest=\"cmd\", required=True)\n\n# count subcommand\ncount_p = subs.add_parser(\"count\", help=\"Count lines matching pattern\")\ncount_p.add_argument(\"file\")\ncount_p.add_argument(\"--pattern\", default=\".*\", help=\"Regex pattern\")\n\n# summary subcommand\nsum_p = subs.add_parser(\"summary\", help=\"Summarize CSV columns\")\nsum_p.add_argument(\"file\")\nsum_p.add_argument(\"--col\", action=\"append\", dest=\"cols\")\n\ndef cmd_count(args):\n    pattern = re.compile(args.pattern)\n    # TODO: open args.file, count lines matching pattern\n    pass\n\ndef cmd_summary(args):\n    # TODO: open CSV, for each col in args.cols, print first/last/count\n    pass\n\nargs = parser.parse_args([\"count\", \"data.txt\", \"--pattern\", \"ERROR\"])\nif args.cmd == \"count\":\n    cmd_count(args)\nelif args.cmd == \"summary\":\n    cmd_summary(args)\n"
}
},

{
"title": "28. JSON & Data Serialization",
"desc": "Python\'s json module handles serialization to/from JSON. For Python-specific objects, use pickle. For configuration, use configparser or tomllib.",
"examples": [
        {"label": "json.dumps / loads with custom encoder", "code": "import json\nfrom datetime import datetime, date\nfrom decimal import Decimal\n\n# Basic usage\ndata = {\"name\": \"Alice\", \"scores\": [95, 87, 92], \"active\": True}\ntext = json.dumps(data, indent=2)\nprint(\"JSON string:\")\nprint(text)\n\nloaded = json.loads(text)\nprint(\"Loaded back:\", loaded)\n\n# Custom encoder for non-serializable types\nclass AppEncoder(json.JSONEncoder):\n    def default(self, obj):\n        if isinstance(obj, (datetime, date)):\n            return obj.isoformat()\n        if isinstance(obj, Decimal):\n            return float(obj)\n        if isinstance(obj, set):\n            return sorted(list(obj))\n        return super().default(obj)\n\nrecord = {\n    \"created\": datetime(2024, 1, 15, 9, 30),\n    \"price\":   Decimal(\"29.99\"),\n    \"tags\":    {\"python\", \"data\", \"tutorial\"},\n}\n\nprint(json.dumps(record, cls=AppEncoder, indent=2))"},
        {"label": "Custom decoder and JSON schema validation pattern", "code": "import json\nfrom datetime import datetime\n\n# Custom decoder using object_hook\ndef decode_record(d):\n    for key, val in d.items():\n        # Auto-parse ISO datetime strings\n        if isinstance(val, str) and len(val) >= 19 and \"T\" in val:\n            try:\n                d[key] = datetime.fromisoformat(val)\n            except ValueError:\n                pass\n    return d\n\njson_str = \'\'\'\n{\n    \"id\": 42,\n    \"name\": \"Order #42\",\n    \"created_at\": \"2024-01-15T09:30:00\",\n    \"updated_at\": \"2024-03-20T14:00:00\",\n    \"amount\": 299.99\n}\n\'\'\'\n\nobj = json.loads(json_str, object_hook=decode_record)\nprint(\"Type of created_at:\", type(obj[\"created_at\"]))  # datetime\nprint(\"Year:\", obj[\"created_at\"].year)\n\n# Simple schema validation pattern\ndef validate(data, schema):\n    errors = []\n    for field, expected_type in schema.items():\n        if field not in data:\n            errors.append(f\"Missing: {field}\")\n        elif not isinstance(data[field], expected_type):\n            errors.append(f\"{field}: expected {expected_type.__name__}, got {type(data[field]).__name__}\")\n    return errors\n\nschema = {\"id\": int, \"name\": str, \"amount\": float}\nprint(\"Errors:\", validate(obj, schema) or \"None\")"},
        {"label": "pickle, configparser, and tomllib", "code": "import pickle, configparser, io\n\n# ─── pickle: serialize any Python object ───────────────────────────────────\nclass Model:\n    def __init__(self, weights):\n        self.weights = weights\n    def predict(self, x):\n        return sum(w * xi for w, xi in zip(self.weights, x))\n\nmodel = Model([0.5, -0.3, 1.2])\nbuf = io.BytesIO()\n\npickle.dump(model, buf)\nprint(\"Pickled size:\", buf.tell(), \"bytes\")\n\nbuf.seek(0)\nloaded_model = pickle.load(buf)\nprint(\"Prediction:\", loaded_model.predict([1.0, 2.0, 3.0]))\n\n# ─── configparser: INI-format config files ─────────────────────────────────\nconfig_text = \'\'\'\n[database]\nhost = localhost\nport = 5432\nname = mydb\n\n[app]\ndebug = true\nworkers = 4\nlog_level = INFO\n\'\'\'\ncfg = configparser.ConfigParser()\ncfg.read_string(config_text)\n\nprint(\"DB host:\", cfg[\"database\"][\"host\"])\nprint(\"DB port:\", cfg.getint(\"database\", \"port\"))\nprint(\"Debug:  \", cfg.getboolean(\"app\", \"debug\"))\nprint(\"Workers:\", cfg.getint(\"app\", \"workers\"))\nprint(\"Sections:\", cfg.sections())"}
    ],
"rw": {
    "title": "API Response Cache",
    "scenario": "A data ingestion service serializes API responses to JSON with metadata, then deserializes and validates them on re-read.",
    "code": "import json, hashlib\nfrom datetime import datetime\n\nclass APICache:\n    def __init__(self):\n        self._store = {}  # in memory; use file I/O in production\n\n    def _key(self, url, params):\n        raw = json.dumps({\"url\": url, \"params\": params}, sort_keys=True)\n        return hashlib.md5(raw.encode()).hexdigest()\n\n    def get(self, url, params=None):\n        k = self._key(url, params or {})\n        if k in self._store:\n            entry = json.loads(self._store[k])\n            age = (datetime.now() - datetime.fromisoformat(entry[\"cached_at\"])).seconds\n            print(f\"  [cache hit] age={age}s, key={k[:8]}\")\n            return entry[\"data\"]\n        return None\n\n    def set(self, url, params, data):\n        k = self._key(url, params or {})\n        entry = {\"data\": data, \"cached_at\": datetime.now().isoformat(), \"url\": url}\n        self._store[k] = json.dumps(entry)\n        print(f\"  [cache set] key={k[:8]}\")\n\ncache = APICache()\nurl = \"https://api.example.com/prices\"\nparams = {\"symbol\": \"AAPL\", \"period\": \"1d\"}\n\nresult = cache.get(url, params)\nif result is None:\n    data = {\"symbol\": \"AAPL\", \"price\": 195.50, \"volume\": 1_200_000}\n    cache.set(url, params, data)\n    result = data\n\nprint(\"Result:\", result)\ncache.get(url, params)  # should be cache hit"
},
"practice": {
    "title": "Config File Manager",
    "desc": "Write a ConfigManager class that loads from a JSON file (on init) and falls back to defaults if the file does not exist. Support get(key, default=None), set(key, value), and save() (writes back to JSON). Write a test that creates a temp file, sets values, saves, reloads, and verifies.",
    "starter": "import json, pathlib\n\nclass ConfigManager:\n    def __init__(self, path, defaults=None):\n        self.path = pathlib.Path(path)\n        self._data = dict(defaults or {})\n        # TODO: if self.path exists, load and merge with self._data\n        pass\n\n    def get(self, key, default=None):\n        # TODO: return self._data.get(key, default)\n        pass\n\n    def set(self, key, value):\n        # TODO: update self._data[key] = value\n        pass\n\n    def save(self):\n        # TODO: write self._data to self.path as JSON (indent=2)\n        pass\n\n# Test\nimport tempfile, os\nwith tempfile.NamedTemporaryFile(suffix=\".json\", delete=False, mode=\"w\") as f:\n    json.dump({\"theme\": \"dark\"}, f)\n    tmp = f.name\n\ncfg = ConfigManager(tmp, defaults={\"theme\": \"light\", \"font_size\": 12})\nprint(\"theme:\", cfg.get(\"theme\"))      # dark (from file)\nprint(\"font:\", cfg.get(\"font_size\"))   # 12 (from defaults)\ncfg.set(\"font_size\", 14)\ncfg.save()\n\ncfg2 = ConfigManager(tmp)\nprint(\"reloaded font:\", cfg2.get(\"font_size\"))  # 14\nos.unlink(tmp)\n"
}
},

{
"title": "29. Pathlib & File System Ops",
"desc": "pathlib.Path is the modern way to handle filesystem paths in Python. It\'s cross-platform, object-oriented, and integrates with all standard file operations.",
"examples": [
        {"label": "Path manipulation and navigation", "code": "from pathlib import Path\n\n# Create a Path object — cross-platform!\np = Path(\"/home/user/data/sales_2024.csv\")\n\n# Path components\nprint(\"name:       \", p.name)         # sales_2024.csv\nprint(\"stem:       \", p.stem)         # sales_2024\nprint(\"suffix:     \", p.suffix)       # .csv\nprint(\"suffixes:   \", Path(\"a.tar.gz\").suffixes)  # [\'.tar\', \'.gz\']\nprint(\"parent:     \", p.parent)       # /home/user/data\nprint(\"parts:      \", p.parts)\n\n# Building paths with / operator\nbase    = Path(\"/home/user\")\ndata    = base / \"data\"\noutfile = data / \"reports\" / \"q1.xlsx\"\nprint(\"Built path:\", outfile)\n\n# Resolve, absolute, relative_to\ncwd = Path.cwd()\nprint(\"CWD:\", cwd)\nprint(\"Home:\", Path.home())\n\n# Check existence\nprint(\"exists:\", p.exists())\nprint(\"is_file:\", p.is_file())\nprint(\"is_dir: \", p.is_dir())\n\n# Change suffix\nrenamed = p.with_suffix(\".parquet\")\nprint(\"With new suffix:\", renamed)"},
        {"label": "Glob patterns and directory walking", "code": "import tempfile, pathlib\n\n# Create a temp directory structure for demo\ntmp = pathlib.Path(tempfile.mkdtemp())\n(tmp / \"data\").mkdir()\n(tmp / \"data\" / \"sales.csv\").write_text(\"a,b\")\n(tmp / \"data\" / \"costs.csv\").write_text(\"c,d\")\n(tmp / \"reports\").mkdir()\n(tmp / \"reports\" / \"q1.xlsx\").write_text(\"x\")\n(tmp / \"reports\" / \"q2.xlsx\").write_text(\"y\")\n(tmp / \"config.json\").write_text(\"{}\")\n\n# glob: match in one directory\ncsvs = list(tmp.glob(\"data/*.csv\"))\nprint(\"CSVs:\", [f.name for f in csvs])\n\n# rglob: recursive glob\nall_files = list(tmp.rglob(\"*\"))\nprint(\"All files:\")\nfor f in sorted(all_files):\n    print(\"  \", f.relative_to(tmp))\n\n# Filter only files (not directories)\nonly_files = [f for f in tmp.rglob(\"*\") if f.is_file()]\nprint(\"File count:\", len(only_files))\n\n# Cleanup\nimport shutil\nshutil.rmtree(tmp)\nprint(\"Temp dir removed\")"},
        {"label": "Reading, writing, and file operations", "code": "import tempfile, pathlib, shutil\n\ntmp = pathlib.Path(tempfile.mkdtemp())\n\n# Write and read text\n(tmp / \"hello.txt\").write_text(\"Hello, World!\")\ncontent = (tmp / \"hello.txt\").read_text()\nprint(\"read_text:\", content)\n\n# Write and read bytes\n(tmp / \"data.bin\").write_bytes(b\"\\x00\\x01\\x02\\x03\")\nraw = (tmp / \"data.bin\").read_bytes()\nprint(\"read_bytes:\", raw.hex())\n\n# Open with context manager for large files\nlog = tmp / \"log.txt\"\nwith log.open(\"w\") as f:\n    for i in range(5):\n        f.write(f\"line {i}\\n\")\n\nwith log.open() as f:\n    for line in f:\n        print(\" \", line.rstrip())\n\n# stat: file metadata\ns = log.stat()\nprint(f\"Size: {s.st_size} bytes\")\n\n# mkdir, rename, unlink, shutil operations\n(tmp / \"subdir\").mkdir(parents=True, exist_ok=True)\nshutil.copy(log, tmp / \"subdir\" / \"log_copy.txt\")\nprint(\"Copied:\", list((tmp / \"subdir\").iterdir()))\n\nshutil.rmtree(tmp)\nprint(\"Done\")"}
    ],
"rw": {
    "title": "Data File Organizer",
    "scenario": "A data engineer uses pathlib to scan a raw data directory, classify files by type, and move them to organized subdirectories.",
    "code": "import tempfile, pathlib, shutil\n\n# Setup demo files\nsrc = pathlib.Path(tempfile.mkdtemp())\nfor name in [\"sales.csv\", \"costs.csv\", \"model.pkl\", \"report.pdf\",\n             \"config.json\", \"weights.pkl\", \"notes.txt\"]:\n    (src / name).write_text(f\"content of {name}\")\n\nprint(\"Input files:\", [f.name for f in sorted(src.iterdir())])\n\n# Classification map\nTYPE_MAP = {\n    \".csv\":  \"data\",\n    \".pkl\":  \"models\",\n    \".json\": \"config\",\n    \".pdf\":  \"reports\",\n    \".txt\":  \"misc\",\n}\n\nmoved = []\nfor file in src.iterdir():\n    if not file.is_file():\n        continue\n    category = TYPE_MAP.get(file.suffix, \"other\")\n    dest_dir = src / category\n    dest_dir.mkdir(exist_ok=True)\n    dest = dest_dir / file.name\n    shutil.move(str(file), dest)\n    moved.append(f\"{file.name} -> {category}/\")\n\nfor m in moved:\n    print(\" \", m)\n\n# Show final structure\nfor subdir in sorted(src.iterdir()):\n    if subdir.is_dir():\n        print(f\"  {subdir.name}/:\", [f.name for f in subdir.iterdir()])\n\nshutil.rmtree(src)"
},
"practice": {
    "title": "Log File Archiver",
    "desc": "Write a function archive_logs(log_dir, archive_dir, days_old=7) that uses pathlib to: (1) find all .log files in log_dir older than days_old days, (2) compress each with shutil.make_archive (or just move for simplicity), (3) move them to archive_dir/YYYY-MM/ subfolders based on file modification date. Return a list of moved files.",
    "starter": "import pathlib, shutil, tempfile\nfrom datetime import datetime, timedelta\n\ndef archive_logs(log_dir, archive_dir, days_old=7):\n    log_dir     = pathlib.Path(log_dir)\n    archive_dir = pathlib.Path(archive_dir)\n    cutoff      = datetime.now() - timedelta(days=days_old)\n    moved       = []\n\n    for log_file in log_dir.glob(\"*.log\"):\n        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)\n        if mtime < cutoff:\n            # TODO: create archive_dir/YYYY-MM/ folder\n            # TODO: move log_file there\n            # TODO: append (log_file.name, dest) to moved\n            pass\n\n    return moved\n\n# Demo setup\nimport os, time\ntmp_logs    = pathlib.Path(tempfile.mkdtemp())\ntmp_archive = pathlib.Path(tempfile.mkdtemp())\n\n# Create fake old log files\nfor i in range(3):\n    f = tmp_logs / f\"app_{i}.log\"\n    f.write_text(f\"log content {i}\")\n    # Make it 10 days old\n    old_time = time.time() - 10 * 86400\n    os.utime(f, (old_time, old_time))\n\n(tmp_logs / \"recent.log\").write_text(\"recent\")  # should NOT be archived\n\nresult = archive_logs(tmp_logs, tmp_archive, days_old=7)\nprint(\"Archived:\", result)\nshutil.rmtree(tmp_logs); shutil.rmtree(tmp_archive)\n"
}
},

{
"title": "30. String Formatting Mastery",
"desc": "Master Python\'s string formatting mini-language: f-strings, format(), format spec DSL, textwrap, and Template strings for safe user-controlled formatting.",
"examples": [
        {"label": "f-string advanced features and format spec", "code": "# Format spec: [[fill]align][sign][z][#][0][width][grouping][.precision][type]\npi = 3.14159265358979\n\n# Width, precision, type\nprint(f\"{pi:.2f}\")        # 3.14\nprint(f\"{pi:10.4f}\")      # right-aligned in width 10\nprint(f\"{pi:<10.4f}|\")    # left-aligned\nprint(f\"{pi:^10.4f}|\")    # center-aligned\nprint(f\"{pi:+.3f}\")       # force + sign\n\n# Integer formatting\nn = 1_234_567\nprint(f\"{n:,}\")            # 1,234,567\nprint(f\"{n:_}\")            # 1_234_567\nprint(f\"{n:>15,}\")         # right-aligned width 15\nprint(f\"{255:#x}\")         # 0xff  hex with prefix\nprint(f\"{255:08b}\")        # 11111111  binary, zero-padded\n\n# Percentage\nprint(f\"{0.857:.1%}\")      # 85.7%\n\n# Datetime in f-string\nfrom datetime import datetime\nnow = datetime(2024, 3, 15, 9, 5, 7)\nprint(f\"{now:%Y-%m-%d %H:%M:%S}\")  # 2024-03-15 09:05:07\nprint(f\"{now:%B %d, %Y}\")          # March 15, 2024\n\n# Expression in f-string\ndata = [1, 2, 3, 4, 5]\nprint(f\"Mean: {sum(data)/len(data):.2f}, Max: {max(data)}\")\n\n# Self-documenting expressions (Python 3.8+)\nx = 42\nprint(f\"{x=}\")   # x=42"},
        {"label": "textwrap, Template, and str methods", "code": "import textwrap\nfrom string import Template\n\n# textwrap.wrap / fill: wrap long text\nlong_text = (\"Python is a high-level, interpreted, general-purpose programming language. \"\n             \"Its design philosophy emphasizes code readability with the use of significant indentation.\")\n\nwrapped = textwrap.fill(long_text, width=50)\nprint(wrapped)\nprint()\n\n# Dedent: remove common leading whitespace (useful after triple-quote strings)\nindented = \'\'\'\n    def foo():\n        return 42\n    \'\'\'\nprint(repr(textwrap.dedent(indented).strip()))\n\n# Template: safe for user-provided format strings (no code execution risk)\ntmpl = Template(\"Hello $name, your balance is $$${balance:.2f}\")\nprint(tmpl.substitute(name=\"Alice\", balance=1234.56))\n\n# safe_substitute: does not raise for missing keys\ntmpl2 = Template(\"Dear $name, ref: $ref_id\")\nprint(tmpl2.safe_substitute(name=\"Bob\"))  # $ref_id stays\n\n# str methods useful for formatting\ncols = [\"id\", \"name\", \"price\", \"qty\"]\nprint(\" | \".join(c.ljust(10) for c in cols))\nprint(\"-\" * 45)\nrow = [1, \"apple\", 1.20, 50]\nprint(\" | \".join(str(v).ljust(10) for v in row))"},
        {"label": "Building tables and reports with format()", "code": "# format() with the mini-language directly\nprint(format(3.14159, \".2f\"))\nprint(format(1234567, \",\"))\nprint(format(\"hello\", \">20\"))\n\n# Building a text table\nheaders = [\"Product\", \"Qty\", \"Price\", \"Total\"]\nrows = [\n    (\"Apple\",    50, 1.20, 60.00),\n    (\"Banana\",  200, 0.50, 100.00),\n    (\"Cherry\",   30, 2.00, 60.00),\n    (\"Durian\",    5, 8.75, 43.75),\n]\n\n# Column widths\nw = [12, 6, 8, 10]\nfmt_h = \"  \".join(f\"{h:>{ww}}\" for h, ww in zip(headers, w))\nsep   = \"  \".join(\"-\"*ww for ww in w)\nprint(fmt_h)\nprint(sep)\nfor row in rows:\n    vals = [f\"{row[0]:<{w[0]}}\", f\"{row[1]:>{w[1]}\",\n            f\"{row[2]:>{w[2]}.2f}\", f\"{row[3]:>{w[3]}.2f}\"]\n    print(\"  \".join(vals))\n\ntotal = sum(r[3] for r in rows)\nprint(sep)\nprint(f\"{\'TOTAL\':>{sum(w)+6}}: {total:.2f}\")"}
    ],
"rw": {
    "title": "Report Generator",
    "scenario": "A finance team generates formatted summary reports from sales data using f-strings and textwrap.",
    "code": "from datetime import date\nimport textwrap\n\ndef format_report(title, data, width=60):\n    border  = \"=\" * width\n    today   = date.today().strftime(\"%B %d, %Y\")\n    lines   = [border, f\"  {title}\".center(width), f\"  Generated: {today}\".center(width), border, \"\"]\n\n    # Summary stats\n    totals  = [r[\"revenue\"] for r in data]\n    lines  += [\n        f\"  {\'Region\':<15} {\'Revenue\':>12} {\'Units\':>8} {\'Avg/Unit\':>10}\",\n        \"  \" + \"-\" * (width - 2),\n    ]\n\n    for r in data:\n        avg = r[\"revenue\"] / r[\"units\"] if r[\"units\"] else 0\n        lines.append(\n            f\"  {r[\'region\']:<15} ${r[\'revenue\']:>11,.0f} {r[\'units\']:>8,} ${avg:>9.2f}\"\n        )\n\n    lines += [\"  \" + \"-\" * (width - 2),\n              f\"  {\'TOTAL\':<15} ${sum(totals):>11,.0f}\",\n              \"\", border]\n    return \"\\n\".join(lines)\n\ndata = [\n    {\"region\": \"North\",  \"revenue\": 1_450_000, \"units\": 9_800},\n    {\"region\": \"South\",  \"revenue\":   980_000, \"units\": 7_200},\n    {\"region\": \"East\",   \"revenue\": 2_100_000, \"units\": 14_500},\n    {\"region\": \"West\",   \"revenue\": 1_750_000, \"units\": 11_000},\n]\n\nprint(format_report(\"Q1 2024 Sales Report\", data))"
},
"practice": {
    "title": "Invoice Formatter",
    "desc": "Write a function format_invoice(company, items, tax_rate) where items is a list of (desc, qty, unit_price) tuples. Print a formatted invoice with: header (company name, date), line items table (description, qty, unit price, line total), subtotal, tax amount, and grand total. Use f-strings with format specs for alignment.",
    "starter": "from datetime import date\n\ndef format_invoice(company, items, tax_rate=0.08):\n    today    = date.today()\n    subtotal = sum(qty * price for _, qty, price in items)\n    tax      = subtotal * tax_rate\n    total    = subtotal + tax\n\n    w = 55\n    print(\"=\" * w)\n    print(f\"  {company}\".center(w))\n    print(f\"  Invoice Date: {today}\".center(w))\n    print(\"=\" * w)\n    print(f\"  {\'Description\':<22} {\'Qty\':>4} {\'Unit\':>8} {\'Total\':>10}\")\n    print(\"  \" + \"-\" * (w-2))\n\n    for desc, qty, price in items:\n        # TODO: print each line with f-string formatting\n        pass\n\n    print(\"  \" + \"-\" * (w-2))\n    # TODO: print subtotal, tax, and grand total rows\n    print(\"=\" * w)\n\nformat_invoice(\"Acme Corp\", [\n    (\"Python Training\",  1, 2500.00),\n    (\"Jupyter Setup\",    3,  150.00),\n    (\"Cloud Credits\",   10,   49.99),\n], tax_rate=0.09)\n"
}
},

{
"title": "31. Performance Optimization & Caching",
"desc": "Profile before optimizing. Use timeit for micro-benchmarks, functools.cache for memoization, __slots__ for memory, and algorithmic improvements for the biggest wins.",
"examples": [
        {"label": "timeit for micro-benchmarking", "code": "import timeit\n\n# Compare list comprehension vs map() vs for-loop\nsetup = \"data = list(range(10_000))\"\n\nt_comp  = timeit.timeit(\"[x**2 for x in data]\",      setup=setup, number=1000)\nt_map   = timeit.timeit(\"list(map(lambda x: x**2, data))\", setup=setup, number=1000)\nt_loop  = timeit.timeit(\'\'\'\nresult = []\nfor x in data:\n    result.append(x**2)\n\'\'\', setup=setup, number=1000)\n\nprint(f\"List comprehension: {t_comp:.3f}s\")\nprint(f\"map(lambda):        {t_map:.3f}s\")\nprint(f\"for loop + append:  {t_loop:.3f}s\")\n\n# Compare string joining methods\nsetup2 = \"parts = [\'a\'] * 1000\"\nt_join  = timeit.timeit(\"\'\'.join(parts)\",        setup=setup2, number=5000)\nt_plus  = timeit.timeit(\"s=\'\'\nfor p in parts: s += p\", setup=setup2, number=5000)\nprint(f\"join():     {t_join:.4f}s\")\nprint(f\"+=:         {t_plus:.4f}s\")\nprint(f\"join speedup: {t_plus/t_join:.1f}x\")"},
        {"label": "functools.cache and lru_cache", "code": "import functools, time\n\n# lru_cache: memoize with a max size limit\n@functools.lru_cache(maxsize=128)\ndef fib_lru(n):\n    if n <= 1: return n\n    return fib_lru(n-1) + fib_lru(n-2)\n\n# functools.cache: unlimited cache (Python 3.9+)\n@functools.cache\ndef fib_cache(n):\n    if n <= 1: return n\n    return fib_cache(n-1) + fib_cache(n-2)\n\nt0 = time.perf_counter()\nresult = fib_lru(40)\nprint(f\"fib(40) = {result}, lru_cache time: {(time.perf_counter()-t0)*1000:.2f}ms\")\nprint(\"Cache info:\", fib_lru.cache_info())\n\n# cached_property: compute once, then return stored value\nclass DataStats:\n    def __init__(self, data):\n        self._data = data\n\n    @functools.cached_property\n    def mean(self):\n        print(\"  (computing mean...)\")\n        return sum(self._data) / len(self._data)\n\n    @functools.cached_property\n    def std(self):\n        print(\"  (computing std...)\")\n        m = self.mean\n        return (sum((x-m)**2 for x in self._data) / len(self._data)) ** 0.5\n\nds = DataStats(list(range(1000)))\nprint(\"mean:\", ds.mean)\nprint(\"mean:\", ds.mean)  # no recompute\nprint(\"std: \", ds.std)"},
        {"label": "Algorithmic improvements and built-in speed", "code": "import timeit, collections\n\n# O(n) lookup with set vs list\ndata_list = list(range(10_000))\ndata_set  = set(data_list)\n\nt_list = timeit.timeit(\"9999 in data_list\", globals=locals(), number=100_000)\nt_set  = timeit.timeit(\"9999 in data_set\",  globals=locals(), number=100_000)\nprint(f\"list \'in\': {t_list:.4f}s\")\nprint(f\"set  \'in\': {t_set:.4f}s\")\nprint(f\"Set speedup: {t_list/t_set:.0f}x\")\n\n# Counter vs manual counting\nwords = \"the quick brown fox jumps over the lazy dog the fox\".split()\n\nt_manual = timeit.timeit(\'\'\'\ncounts = {}\nfor w in words:\n    counts[w] = counts.get(w, 0) + 1\n\'\'\', globals={\"words\": words}, number=50_000)\n\nt_counter = timeit.timeit(\"collections.Counter(words)\",\n                           globals={\"collections\": collections, \"words\": words},\n                           number=50_000)\nprint(f\"Manual count: {t_manual:.4f}s\")\nprint(f\"Counter:      {t_counter:.4f}s\")\n\n# Use sorted() key function instead of cmp\nrecords = [{\"name\": n, \"score\": s} for n, s in [(\"Bob\", 72), (\"Alice\", 95), (\"Charlie\", 88)]]\nsorted_records = sorted(records, key=lambda r: r[\"score\"], reverse=True)\nfor r in sorted_records:\n    print(f\"  {r[\'name\']:10s}: {r[\'score\']}\")"}
    ],
"rw": {
    "title": "DataFrame-like Aggregator",
    "scenario": "A custom data aggregation class uses caching and efficient data structures to compute statistics on large datasets without pandas.",
    "code": "import functools, collections, statistics\n\nclass FastAggregator:\n    def __init__(self, records):\n        self._records = records\n        self._by_key  = None  # lazy\n\n    def _ensure_index(self):\n        if self._by_key is None:\n            self._by_key = collections.defaultdict(list)\n            for r in self._records:\n                self._by_key[r[\"group\"]].append(r[\"value\"])\n\n    @functools.cached_property\n    def group_means(self):\n        self._ensure_index()\n        return {k: statistics.mean(v) for k, v in self._by_key.items()}\n\n    @functools.cached_property\n    def group_counts(self):\n        self._ensure_index()\n        return {k: len(v) for k, v in self._by_key.items()}\n\n    @functools.cached_property\n    def overall_mean(self):\n        vals = [r[\"value\"] for r in self._records]\n        return statistics.mean(vals)\n\nimport random\nrandom.seed(42)\nrecords = [{\"group\": f\"G{i%5}\", \"value\": random.gauss(50, 10)} for i in range(10_000)]\n\nagg = FastAggregator(records)\nprint(\"Group means:\", {k: f\"{v:.2f}\" for k, v in agg.group_means.items()})\nprint(\"Group counts:\", agg.group_counts)\nprint(\"Overall mean:\", f\"{agg.overall_mean:.2f}\")\nprint(\"(Accessing again — no recompute):\", f\"{agg.overall_mean:.2f}\")"
},
"practice": {
    "title": "Benchmark Challenge",
    "desc": "Write three versions of a function find_duplicates(lst) that returns a list of values appearing more than once: (1) brute_force using nested loops O(n^2), (2) sort_based by sorting first O(n log n), (3) hash_based using Counter O(n). Benchmark all three with timeit on a list of 10,000 integers. Report the speedups.",
    "starter": "import timeit, collections, random\n\nrandom.seed(42)\ndata = [random.randint(0, 500) for _ in range(10_000)]\n\ndef brute_force(lst):\n    dups = set()\n    for i in range(len(lst)):\n        for j in range(i+1, len(lst)):\n            if lst[i] == lst[j]:\n                dups.add(lst[i])\n    return list(dups)\n\ndef sort_based(lst):\n    # TODO: sort, then check adjacent equal elements\n    pass\n\ndef hash_based(lst):\n    # TODO: use collections.Counter, return keys with count > 1\n    pass\n\n# Only benchmark sort_based and hash_based (brute force is too slow)\nfor name, fn in [(\"sort_based\", sort_based), (\"hash_based\", hash_based)]:\n    t = timeit.timeit(lambda: fn(data), number=100)\n    print(f\"{name}: {t:.4f}s, found {len(fn(data))} duplicates\")\n"
}
},

{
"title": "32. Virtual Environments & Package Management",
"desc": "Virtual environments isolate project dependencies. pip manages packages, and importlib enables dynamic imports at runtime — essential for building extensible systems.",
"examples": [
        {"label": "venv and pip (commands and concepts)", "code": "# These commands are run in the terminal (not runnable as Python code)\n# They are shown here as strings for educational purposes\n\nvenv_commands = \'\'\'\n# Create a virtual environment\npython -m venv .venv\n\n# Activate (macOS/Linux)\nsource .venv/bin/activate\n\n# Activate (Windows)\n.venv\\\\Scripts\\\\activate\n\n# Install packages\npip install requests pandas scikit-learn\n\n# Install from requirements file\npip install -r requirements.txt\n\n# Freeze current environment\npip freeze > requirements.txt\n\n# Upgrade a package\npip install --upgrade numpy\n\n# Show installed packages\npip list\npip show numpy\n\n# Deactivate\ndeactivate\n\'\'\'\n\n# requirements.txt format:\nreq_txt = \'\'\'\n# requirements.txt\nnumpy>=1.24,<2.0\npandas==2.1.0\nscikit-learn>=1.3\nrequests>=2.31\nmatplotlib>=3.7; python_version >= \"3.9\"\n\'\'\'\n\n# pyproject.toml format (modern, preferred):\npyproject_toml = \'\'\'\n[project]\nname = \"my-ml-project\"\nversion = \"0.1.0\"\nrequires-python = \">=3.10\"\ndependencies = [\n    \"numpy>=1.24\",\n    \"pandas>=2.1\",\n    \"scikit-learn>=1.3\",\n]\n\n[project.optional-dependencies]\ndev = [\"pytest\", \"black\", \"mypy\"]\n\'\'\'\n\nprint(\"Common venv workflow:\")\nfor cmd in [\"python -m venv .venv\", \"source .venv/bin/activate\", \"pip install -r requirements.txt\"]:\n    print(f\"  $ {cmd}\")"},
        {"label": "importlib: dynamic imports at runtime", "code": "import importlib, sys\n\n# Basic dynamic import\nmath = importlib.import_module(\"math\")\nprint(\"sqrt(16):\", math.sqrt(16))\n\n# Import a submodule\npprint = importlib.import_module(\"pprint\")\npprint.pprint({\"a\": 1, \"b\": [2, 3]})\n\n# Conditional import: use fast version if available\ndef import_or_fallback(preferred, fallback):\n    try:\n        return importlib.import_module(preferred)\n    except ImportError:\n        print(f\"  {preferred} not found, using {fallback}\")\n        return importlib.import_module(fallback)\n\njson_mod = import_or_fallback(\"ujson\", \"json\")  # ujson is faster if installed\nprint(\"json module:\", json_mod.__name__)\n\n# importlib.util: check if a module is available without importing it\nimport importlib.util\n\nfor pkg in [\"numpy\", \"pandas\", \"flask\", \"fastapi\", \"nonexistent_pkg\"]:\n    spec = importlib.util.find_spec(pkg)\n    status = \"installed\" if spec else \"NOT installed\"\n    print(f\"  {pkg:<20} {status}\")"},
        {"label": "Package structure and __init__.py", "code": "import tempfile, pathlib, sys, importlib\n\n# Create a minimal package structure in a temp directory\ntmp = pathlib.Path(tempfile.mkdtemp())\npkg = tmp / \"mypackage\"\npkg.mkdir()\n\n# Package init\n(pkg / \"__init__.py\").write_text(\'\'\'\n__version__ = \"1.0.0\"\nfrom mypackage.utils import add, multiply\n\'\'\')\n\n(pkg / \"utils.py\").write_text(\'\'\'\ndef add(a, b):\n    return a + b\n\ndef multiply(a, b):\n    return a * b\n\'\'\')\n\n(pkg / \"models.py\").write_text(\'\'\'\nclass LinearModel:\n    def __init__(self, slope=1, intercept=0):\n        self.slope = slope\n        self.intercept = intercept\n\n    def predict(self, x):\n        return self.slope * x + self.intercept\n\'\'\')\n\n# Add tmp to path so Python can find our package\nsys.path.insert(0, str(tmp))\n\n# Import our package\nmypackage = importlib.import_module(\"mypackage\")\nprint(\"Version:\", mypackage.__version__)\nprint(\"add:\", mypackage.add(3, 4))\nprint(\"multiply:\", mypackage.multiply(3, 4))\n\nmodels = importlib.import_module(\"mypackage.models\")\nm = models.LinearModel(slope=2.5, intercept=-1)\nprint(\"predict(10):\", m.predict(10))\n\nsys.path.pop(0)\nimport shutil; shutil.rmtree(tmp)"}
    ],
"rw": {
    "title": "Plugin Loader System",
    "scenario": "An application dynamically loads analysis plugins from a directory at startup using importlib, without hardcoding plugin names.",
    "code": "import importlib, importlib.util, pathlib, sys, tempfile, shutil\n\n# Create plugin directory with two demo plugins\ntmp = pathlib.Path(tempfile.mkdtemp())\nplugin_dir = tmp / \"plugins\"\nplugin_dir.mkdir()\n\n(plugin_dir / \"plugin_stats.py\").write_text(\'\'\'\ndef run(data):\n    n = len(data)\n    mean = sum(data) / n\n    return {\"plugin\": \"stats\", \"count\": n, \"mean\": round(mean, 2)}\n\'\'\')\n\n(plugin_dir / \"plugin_filter.py\").write_text(\'\'\'\ndef run(data):\n    filtered = [x for x in data if x > 0]\n    return {\"plugin\": \"filter\", \"kept\": len(filtered), \"dropped\": len(data)-len(filtered)}\n\'\'\')\n\ndef load_plugins(plugin_dir):\n    plugins = {}\n    for path in sorted(pathlib.Path(plugin_dir).glob(\"plugin_*.py\")):\n        name = path.stem\n        spec = importlib.util.spec_from_file_location(name, path)\n        mod  = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(mod)\n        plugins[name] = mod\n        print(f\"  Loaded: {name}\")\n    return plugins\n\nsys.path.insert(0, str(plugin_dir))\nplugins = load_plugins(plugin_dir)\n\ndata = [3, -1, 7, 0, -2, 5, 9]\nfor name, plugin in plugins.items():\n    print(f\"  {name}: {plugin.run(data)}\")\n\nsys.path.pop(0)\nshutil.rmtree(tmp)"
},
"practice": {
    "title": "Dependency Checker",
    "desc": "Write a function check_dependencies(requirements) that takes a list of package names and uses importlib.util.find_spec() to check if each is installed. Return a dict with \'installed\' and \'missing\' lists. Write another function install_missing(missing) that prints the pip install command needed (don\'t actually run it — just print it).",
    "starter": "import importlib.util\n\ndef check_dependencies(requirements):\n    installed = []\n    missing   = []\n    for pkg in requirements:\n        # Note: package names may differ from import names (e.g. scikit-learn -> sklearn)\n        import_name = pkg.replace(\"-\", \"_\").split(\">=\")[0].split(\"==\")[0].strip()\n        spec = importlib.util.find_spec(import_name)\n        if spec:\n            installed.append(pkg)\n        else:\n            missing.append(pkg)\n    return {\"installed\": installed, \"missing\": missing}\n\ndef install_missing(missing):\n    # TODO: print pip install command for each missing package\n    pass\n\npackages = [\"numpy\", \"pandas\", \"requests\", \"flask\", \"nonexistent_lib\", \"anotherMissingPkg\"]\nresult = check_dependencies(packages)\nprint(\"Installed:\", result[\"installed\"])\nprint(\"Missing:\",   result[\"missing\"])\ninstall_missing(result[\"missing\"])\n"
}
},

{
"title": "33. Introspection & Metaprogramming",
"desc": "Python\'s runtime lets you inspect and modify objects, classes, and functions dynamically. Use inspect, dir(), getattr(), and metaclasses for powerful abstractions.",
"examples": [
        {"label": "dir(), type(), getattr(), hasattr(), inspect", "code": "import inspect\n\nclass Rectangle:\n    width: float\n    height: float\n\n    def __init__(self, w, h):\n        self.width = w\n        self.height = h\n\n    def area(self):\n        return self.width * self.height\n\n    def perimeter(self):\n        return 2 * (self.width + self.height)\n\nr = Rectangle(4, 6)\n\n# dir() lists all attributes and methods\nattrs = [a for a in dir(r) if not a.startswith(\"_\")]\nprint(\"Public attrs:\", attrs)\n\n# type() and isinstance()\nprint(\"type:\", type(r).__name__)\nprint(\"isinstance(r, Rectangle):\", isinstance(r, Rectangle))\nprint(\"isinstance(r, object):   \", isinstance(r, object))\n\n# getattr / setattr / hasattr / delattr\nfor method in [\"area\", \"perimeter\", \"nonexistent\"]:\n    if hasattr(r, method):\n        fn = getattr(r, method)\n        print(f\"{method}(): {fn()}\")\n    else:\n        print(f\"{method}: not found\")\n\n# inspect module\nprint(\"Source file:\", inspect.getfile(Rectangle))\nsig = inspect.signature(Rectangle.__init__)\nprint(\"Signature:\", sig)\nprint(\"Parameters:\", list(sig.parameters.keys()))"},
        {"label": "__dict__, __class__, MRO, and vars()", "code": "class Animal:\n    kingdom = \"Animalia\"\n\n    def __init__(self, name, species):\n        self.name    = name\n        self.species = species\n\n    def speak(self):\n        return \"...\"\n\nclass Dog(Animal):\n    def __init__(self, name):\n        super().__init__(name, \"Canis lupus familiaris\")\n\n    def speak(self):\n        return \"Woof!\"\n\nclass GoldenRetriever(Dog):\n    breed = \"Golden Retriever\"\n\ng = GoldenRetriever(\"Buddy\")\n\n# Instance __dict__: instance attributes only\nprint(\"Instance __dict__:\", g.__dict__)\n\n# Class __dict__: class attributes only\nprint(\"Class __dict__ keys:\", list(GoldenRetriever.__dict__.keys()))\n\n# vars(): same as __dict__ for objects\nprint(\"vars(g):\", vars(g))\n\n# Method Resolution Order (MRO)\nprint(\"MRO:\", [c.__name__ for c in GoldenRetriever.__mro__])\n\n# Class attributes vs instance attributes\nprint(\"Class attr \'kingdom\':\", g.kingdom)  # inherited from Animal\ng.kingdom = \"override\"                      # creates instance attr\nprint(\"Instance attr \'kingdom\':\", g.__dict__[\"kingdom\"])\nprint(\"Class still has:\", Animal.kingdom)"},
        {"label": "Metaclasses and __init_subclass__", "code": "# Metaclass: controls how classes are created\n\nclass SingletonMeta(type):\n    # Ensure only one instance per class\n    _instances = {}\n\n    def __call__(cls, *args, **kwargs):\n        if cls not in cls._instances:\n            cls._instances[cls] = super().__call__(*args, **kwargs)\n        return cls._instances[cls]\n\nclass AppConfig(metaclass=SingletonMeta):\n    def __init__(self):\n        self.debug = False\n        self.host  = \"localhost\"\n\nc1 = AppConfig()\nc2 = AppConfig()\nc1.debug = True\n\nprint(\"Same object:\", c1 is c2)  # True\nprint(\"c2.debug:\", c2.debug)     # True — same instance!\n\n# __init_subclass__: called when a subclass is defined\nclass PluginBase:\n    _registry = {}\n\n    def __init_subclass__(cls, plugin_name=None, **kwargs):\n        super().__init_subclass__(**kwargs)\n        name = plugin_name or cls.__name__.lower()\n        PluginBase._registry[name] = cls\n        print(f\"Registered plugin: {name!r}\")\n\nclass CSVPlugin(PluginBase, plugin_name=\"csv\"):\n    def run(self): return \"csv output\"\n\nclass JSONPlugin(PluginBase, plugin_name=\"json\"):\n    def run(self): return \"json output\"\n\nprint(\"Registry:\", list(PluginBase._registry.keys()))\nplugin = PluginBase._registry[\"csv\"]()\nprint(\"CSV plugin run:\", plugin.run())"}
    ],
"rw": {
    "title": "Auto-Documented API",
    "scenario": "A REST API framework uses introspection to auto-generate documentation from function signatures and docstrings.",
    "code": "import inspect\n\nclass APIRouter:\n    def __init__(self):\n        self.routes = {}\n\n    def route(self, path, method=\"GET\"):\n        def decorator(func):\n            sig    = inspect.signature(func)\n            doc    = inspect.getdoc(func) or \"No description\"\n            params = {\n                name: {\"annotation\": str(p.annotation.__name__ if p.annotation is not inspect.Parameter.empty else \"any\"),\n                       \"default\": str(p.default) if p.default is not inspect.Parameter.empty else \"required\"}\n                for name, p in list(sig.parameters.items())[1:]  # skip \'self\'\n            }\n            self.routes[f\"{method} {path}\"] = {\n                \"handler\": func.__name__,\n                \"doc\":     doc,\n                \"params\":  params,\n            }\n            return func\n        return decorator\n\n    def docs(self):\n        for endpoint, info in self.routes.items():\n            print(f\"\\n{endpoint} -> {info[\'handler\']}\")\n            print(f\"  {info[\'doc\']}\")\n            for p, meta in info[\"params\"].items():\n                print(f\"  - {p}: {meta[\'annotation\']} (default={meta[\'default\']})\")\n\nrouter = APIRouter()\n\n@router.route(\"/users\", \"GET\")\ndef list_users(limit: int = 20, offset: int = 0):\n    # Return paginated list of users.\n    pass\n\n@router.route(\"/users/{id}\", \"GET\")\ndef get_user(user_id: int, include_meta: bool = False):\n    # Fetch a single user by ID.\n    pass\n\nrouter.docs()"
},
"practice": {
    "title": "Class Inspector",
    "desc": "Write a function inspect_class(cls) that returns a dict with: \'name\' (class name), \'bases\' (list of base class names), \'mro\' (list of names), \'class_attrs\' (non-dunder class-level attributes), \'methods\' (public methods with their signatures as strings). Test it on a class you define with inheritance.",
    "starter": "import inspect\n\ndef inspect_class(cls):\n    result = {\n        \"name\":        cls.__name__,\n        \"bases\":       [b.__name__ for b in cls.__bases__],\n        \"mro\":         [c.__name__ for c in cls.__mro__],\n        \"class_attrs\": {},\n        \"methods\":     {},\n    }\n\n    for name, val in cls.__dict__.items():\n        if name.startswith(\"_\"):\n            continue\n        if callable(val):\n            sig = inspect.signature(val)\n            result[\"methods\"][name] = str(sig)\n        else:\n            result[\"class_attrs\"][name] = repr(val)\n\n    return result\n\nclass Vehicle:\n    wheels = 4\n    fuel   = \"gasoline\"\n\n    def __init__(self, brand, speed):\n        self.brand = brand\n        self.speed = speed\n\n    def drive(self, distance: float) -> float:\n        return distance / self.speed\n\nclass ElectricCar(Vehicle):\n    fuel = \"electric\"\n\n    def charge(self, hours: int) -> str:\n        return f\"Charging for {hours}h\"\n\nfor cls in [Vehicle, ElectricCar]:\n    info = inspect_class(cls)\n    print(f\"\\n{info[\'name\']}:\")\n    print(f\"  bases: {info[\'bases\']}\")\n    print(f\"  attrs: {info[\'class_attrs\']}\")\n    print(f\"  methods: {info[\'methods\']}\")\n"
}
},

{
"title": "34. Advanced Type Hints",
"desc": "Python\'s typing module enables static analysis with TypeVar, Generic, Protocol, overload, and Literal. Well-typed code is self-documenting and catches bugs before runtime.",
"examples": [
        {"label": "TypeVar and Generic classes", "code": "from typing import TypeVar, Generic, Iterable, Optional\n\nT = TypeVar(\"T\")\nK = TypeVar(\"K\")\nV = TypeVar(\"V\")\n\n# Generic function: type-safe identity\ndef first(items: list[T]) -> Optional[T]:\n    return items[0] if items else None\n\nprint(first([1, 2, 3]))        # int\nprint(first([\"a\", \"b\"]))       # str\nprint(first([]))               # None\n\n# Generic class: type-safe stack\nclass Stack(Generic[T]):\n    def __init__(self) -> None:\n        self._items: list[T] = []\n\n    def push(self, item: T) -> None:\n        self._items.append(item)\n\n    def pop(self) -> T:\n        if not self._items:\n            raise IndexError(\"pop from empty stack\")\n        return self._items.pop()\n\n    def peek(self) -> Optional[T]:\n        return self._items[-1] if self._items else None\n\n    def __len__(self) -> int:\n        return len(self._items)\n\nint_stack: Stack[int] = Stack()\nint_stack.push(1)\nint_stack.push(2)\nint_stack.push(3)\nprint(\"peek:\", int_stack.peek())  # 3\nprint(\"pop: \", int_stack.pop())   # 3\nprint(\"len: \", len(int_stack))    # 2"},
        {"label": "Union, Optional, Literal, Final, TypeAlias", "code": "from typing import Union, Optional, Literal, Final\nimport sys\n\n# Union: accepts multiple types (Python 3.10+: int | str)\ndef process(value: Union[int, str, float]) -> str:\n    return f\"Got {type(value).__name__}: {value}\"\n\nprint(process(42))\nprint(process(\"hello\"))\nprint(process(3.14))\n\n# Optional[T] is shorthand for Union[T, None]\ndef find_user(user_id: int) -> Optional[dict]:\n    db = {1: {\"name\": \"Alice\"}, 2: {\"name\": \"Bob\"}}\n    return db.get(user_id)\n\nuser = find_user(1)\nif user:\n    print(\"Found:\", user[\"name\"])\n\n# Literal: restrict to specific values\nMode = Literal[\"read\", \"write\", \"append\"]\n\ndef open_file(path: str, mode: Mode) -> str:\n    return f\"Opening {path} in {mode} mode\"\n\nprint(open_file(\"data.csv\", \"read\"))\n\n# Final: constant that cannot be reassigned\nMAX_RETRIES: Final = 3\nAPI_URL:     Final[str] = \"https://api.example.com\"\n\n# TypeAlias (Python 3.10+)\nif sys.version_info >= (3, 10):\n    from typing import TypeAlias\n    Vector: TypeAlias = list[float]\n    Matrix: TypeAlias = list[list[float]]\n\nprint(f\"MAX_RETRIES: {MAX_RETRIES}\")"},
        {"label": "@overload for multiple signatures", "code": "from typing import overload, Union\n\n# @overload allows multiple type signatures for the same function\n# Only the implementation signature uses the body\n\n@overload\ndef parse(value: str) -> int: ...\n@overload\ndef parse(value: bytes) -> float: ...\n@overload\ndef parse(value: int) -> str: ...\n\ndef parse(value: Union[str, bytes, int]) -> Union[int, float, str]:\n    if isinstance(value, str):\n        return int(value)\n    elif isinstance(value, bytes):\n        return float(value.decode())\n    else:\n        return str(value)\n\nprint(parse(\"42\"))    # int\nprint(parse(b\"3.14\")) # float\nprint(parse(100))     # str\n\n# TypedDict: dict with typed keys\nfrom typing import TypedDict, NotRequired\n\nclass UserRecord(TypedDict):\n    id:    int\n    name:  str\n    email: str\n    age:   NotRequired[int]  # optional key\n\ndef create_user(data: UserRecord) -> str:\n    return f\"User {data[\'name\']} ({data[\'email\']})\"\n\nuser: UserRecord = {\"id\": 1, \"name\": \"Alice\", \"email\": \"alice@example.com\", \"age\": 30}\nprint(create_user(user))\n\nuser2: UserRecord = {\"id\": 2, \"name\": \"Bob\", \"email\": \"bob@example.com\"}\nprint(create_user(user2))  # age is optional"}
    ],
"rw": {
    "title": "Typed Data Pipeline",
    "scenario": "A production data pipeline uses TypedDict, Generic, and Union to enforce type contracts across stages, catching mismatches early.",
    "code": "from typing import TypedDict, Generic, TypeVar, Optional, Callable\nfrom dataclasses import dataclass, field\n\nT = TypeVar(\"T\")\nR = TypeVar(\"R\")\n\nclass RawRecord(TypedDict):\n    id:    int\n    name:  str\n    value: float\n    valid: bool\n\nclass CleanRecord(TypedDict):\n    id:    int\n    name:  str\n    value: float\n\n@dataclass\nclass Pipeline(Generic[T, R]):\n    steps: list[Callable[[T], R]] = field(default_factory=list)\n\n    def add_step(self, fn: Callable) -> \"Pipeline\":\n        self.steps.append(fn)\n        return self\n\n    def run(self, data: list[T]) -> list:\n        result = data\n        for step in self.steps:\n            result = [step(r) for r in result if r is not None]\n        return result\n\ndef filter_valid(r: RawRecord) -> Optional[RawRecord]:\n    return r if r[\"valid\"] and r[\"value\"] > 0 else None\n\ndef normalize(r: RawRecord) -> CleanRecord:\n    return {\"id\": r[\"id\"], \"name\": r[\"name\"].strip().title(), \"value\": round(r[\"value\"], 2)}\n\nrecords: list[RawRecord] = [\n    {\"id\": 1, \"name\": \"alice smith\",  \"value\": 129.5,  \"valid\": True},\n    {\"id\": 2, \"name\": \"BOB JONES\",    \"value\": -5.0,   \"valid\": False},\n    {\"id\": 3, \"name\": \"  carol lee \", \"value\": 89.99,  \"valid\": True},\n]\n\npipeline: Pipeline[RawRecord, CleanRecord] = Pipeline()\npipeline.add_step(filter_valid).add_step(normalize)\nresult = pipeline.run(records)\nfor r in result:\n    print(f\"  {r}\")"
},
"practice": {
    "title": "Generic Result Type",
    "desc": "Implement a generic Result[T, E] class (inspired by Rust) with two states: Ok(value: T) and Err(error: E). Add methods: is_ok(), is_err(), unwrap() (returns value or raises), unwrap_or(default), map(fn) (applies fn to value if Ok, returns new Result). Write tests using Result[int, str].",
    "starter": "from typing import Generic, TypeVar, Callable, Optional\nfrom dataclasses import dataclass\n\nT = TypeVar(\"T\")\nE = TypeVar(\"E\")\nU = TypeVar(\"U\")\n\n@dataclass\nclass Result(Generic[T, E]):\n    _value: Optional[T] = None\n    _error: Optional[E] = None\n\n    @classmethod\n    def ok(cls, value: T) -> \"Result[T, E]\":\n        return cls(_value=value)\n\n    @classmethod\n    def err(cls, error: E) -> \"Result[T, E]\":\n        return cls(_error=error)\n\n    def is_ok(self) -> bool:\n        return self._error is None\n\n    def is_err(self) -> bool:\n        return self._error is not None\n\n    def unwrap(self) -> T:\n        if self.is_err():\n            raise ValueError(f\"Called unwrap on Err: {self._error}\")\n        return self._value\n\n    def unwrap_or(self, default: T) -> T:\n        # TODO: return value if ok, else default\n        pass\n\n    def map(self, fn: Callable[[T], U]) -> \"Result[U, E]\":\n        # TODO: if ok, return Result.ok(fn(self._value)), else return self\n        pass\n\n# Tests\nr1 = Result.ok(42)\nr2 = Result.err(\"not found\")\n\nprint(r1.is_ok(), r1.unwrap())\nprint(r2.is_err(), r2.unwrap_or(-1))\nprint(r1.map(lambda x: x * 2).unwrap())\ntry:    r2.unwrap()\nexcept ValueError as e: print(\"Caught:\", e)\n"
}
},

]  # end SECTIONS


# ─── Generate ──────────────────────────────────────────────────────────────────
html = make_html(SECTIONS)
nb   = make_nb(SECTIONS)

(BASE / "index.html").write_text(html, encoding="utf-8")
(BASE / "study_guide.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")

html_size = (BASE / "index.html").stat().st_size / 1024
nb_cells  = len(nb["cells"])
print(f"Python Basics guide created in: {BASE}")
print(f"  index.html:       {html_size:.1f} KB")
print(f"  study_guide.ipynb: {nb_cells} cells")
