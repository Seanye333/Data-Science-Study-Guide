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
