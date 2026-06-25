#!/usr/bin/env python3
"""Generate APIs & Data Collection study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE = pathlib.Path(__file__).resolve().parent.parent / "modules" / "03_api"
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
            check_html = (
                f'<template class="ho-check">{esc(practice["check"])}</template>'
                if practice.get("check") else ""
            )
            practice_html = (
                f'<div class="practice">'
                f'<div class="ph">&#x1F3CB;&#xFE0F; Practice: {esc(practice["title"])}</div>'
                f'<div class="pd">{esc(practice["desc"])}</div>'
                f'<div class="code-block"><div class="ch"><span>Starter Code</span>'
                f'<button onclick="cp(\'{pid}\')">Copy</button></div>'
                f'<pre><code id="{pid}" class="language-python">{esc(practice["starter"])}</code></pre></div>'
                f'{check_html}'
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
<title>APIs &amp; Data Collection Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<link rel="stylesheet" href="../../styles/glass.css">
<style>:root{{--acc:#36bcf7}}</style>
</head><body class="page-module">
<aside class="sidebar">
  <div class="sbh"><h2>🌐 APIs &amp; Data Collection</h2><p>Study Guide &bull; {n} topics</p>
    <input id="q" placeholder="Search..." oninput="filt(this.value)">
  </div>
  <ul class="nav-list" id="nl">{nav}</ul>
</aside>
<main class="main">
  <h1 class="pt">🌐 APIs &amp; Data Collection</h1>
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

    cells.append(md("# APIs & Data Collection Study Guide\n\nA hands-on guide to consuming and building APIs with Python — from basic requests to production-ready data pipelines."))
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
"title": "1. How the Web Works — HTTP Fundamentals",
"desc": "Before consuming APIs you need to understand how HTTP works: requests, responses, methods, status codes, and headers. Every API call is just an HTTP request.",
"examples": [
{"label": "HTTP methods overview", "code":
"""# HTTP Methods (verbs) and their typical use
# GET    — Retrieve data           (read-only, safe, idempotent)
# POST   — Create a new resource   (not idempotent)
# PUT    — Replace a resource      (idempotent)
# PATCH  — Partially update        (not necessarily idempotent)
# DELETE — Remove a resource       (idempotent)

# Status Code Families
# 1xx — Informational (100 Continue)
# 2xx — Success       (200 OK, 201 Created, 204 No Content)
# 3xx — Redirection   (301 Moved, 304 Not Modified)
# 4xx — Client Error  (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests)
# 5xx — Server Error  (500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable)

print("Common status codes every developer should know:")
codes = {200: "OK", 201: "Created", 204: "No Content",
         400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
         404: "Not Found", 429: "Rate Limited", 500: "Server Error"}
for code, meaning in codes.items():
    print(f"  {code} — {meaning}")"""},
{"label": "Anatomy of a URL", "code":
"""from urllib.parse import urlparse, parse_qs

url = "https://api.example.com:8080/v2/users?page=1&limit=50#results"
parsed = urlparse(url)

print(f"Scheme:   {parsed.scheme}")     # https
print(f"Host:     {parsed.hostname}")    # api.example.com
print(f"Port:     {parsed.port}")        # 8080
print(f"Path:     {parsed.path}")        # /v2/users
print(f"Query:    {parsed.query}")       # page=1&limit=50
print(f"Fragment: {parsed.fragment}")    # results

# Parse query string into dict
params = parse_qs(parsed.query)
print(f"Params:   {params}")  # {'page': ['1'], 'limit': ['50']}"""},
{"label": "Headers — what metadata travels with requests", "code":
"""# Common request headers
headers_example = {
    "Content-Type": "application/json",    # What format the body is in
    "Accept": "application/json",          # What format you want back
    "Authorization": "Bearer <token>",     # Authentication
    "User-Agent": "MyApp/1.0",            # Identify your client
    "Cache-Control": "no-cache",          # Caching behavior
}

# Common response headers
# Content-Type      — format of response body
# X-RateLimit-Limit — max requests per window
# X-RateLimit-Remaining — requests left
# Retry-After      — seconds to wait (on 429)
# ETag             — version identifier for caching

for k, v in headers_example.items():
    print(f"  {k}: {v}")"""},
],
"rw": {
    "todos": [
    "Use urlparse to decompose a URL and print its scheme, host, path, and query string",
    "Build a URL manually using urlencode and verify it matches what requests would generate",
    "Send a request to https://httpbin.org/get and inspect every response header it returns",
    "Identify what HTTP status code means 'rate limited' and how you would detect it in code",
    "Write a dict of 5 HTTP status codes and their meanings without looking them up",
],
"title": "Debugging a Failed API Call",
    "scenario": "You're calling an API and getting mysterious errors. Understanding HTTP fundamentals helps you diagnose the issue by inspecting status codes, headers, and response bodies.",
    "code":
"""import requests

# Always inspect the full response, not just the body
def debug_request(url, **kwargs):
    resp = requests.get(url, **kwargs)

    print(f"Status:  {resp.status_code} {resp.reason}")
    print(f"URL:     {resp.url}")
    print(f"Time:    {resp.elapsed.total_seconds():.3f}s")
    print(f"Headers:")
    for k, v in resp.headers.items():
        print(f"  {k}: {v}")
    print(f"Body preview: {resp.text[:200]}")

    return resp

# Example: hit a public API
resp = debug_request("https://httpbin.org/get")
print(f"\\nJSON keys: {list(resp.json().keys())}")"""
},
"practice": {
    "title": "Parse & Classify URLs",
    "desc": "Write a function that takes a list of URLs and returns a dict grouping them by their hostname. Also identify which ones use HTTPS vs HTTP.",
    "starter":
"""from urllib.parse import urlparse

urls = [
    "https://api.github.com/users/octocat",
    "https://api.github.com/repos/python/cpython",
    "http://jsonplaceholder.typicode.com/posts/1",
    "https://httpbin.org/get",
    "http://httpbin.org/post",
]

def classify_urls(url_list):
    by_host = {}
    secure_count = 0
    insecure_count = 0
    # TODO: parse each URL, group by hostname, count https vs http
    return by_host, secure_count, insecure_count

result, secure, insecure = classify_urls(urls)
for host, links in result.items():
    print(f"{host}: {len(links)} URLs")
print(f"Secure: {secure}, Insecure: {insecure}")"""
}
},

{
"title": "2. Getting Started with requests",
"desc": "The requests library is the standard way to make HTTP calls in Python. It wraps urllib3 with a clean, human-friendly API. Install: pip install requests.",
"examples": [
{"label": "Your first GET request", "code":
"""import requests

# Simple GET — fetch a resource
resp = requests.get("https://httpbin.org/get")

print(f"Status: {resp.status_code}")      # 200
print(f"Content-Type: {resp.headers['Content-Type']}")
print(f"Encoding: {resp.encoding}")

# Parse JSON response
data = resp.json()
print(f"Origin IP: {data['origin']}")
print(f"URL: {data['url']}")"""},
{"label": "Query parameters", "code":
"""import requests

# Pass params as a dict — requests encodes them for you
params = {"q": "python data science", "page": 1, "per_page": 5}
resp = requests.get("https://httpbin.org/get", params=params)

print(f"Final URL: {resp.url}")
# https://httpbin.org/get?q=python+data+science&page=1&per_page=5

data = resp.json()
print(f"Server saw args: {data['args']}")"""},
{"label": "POST, PUT, PATCH, DELETE", "code":
"""import requests

BASE = "https://httpbin.org"

# POST — create (send JSON body)
resp = requests.post(f"{BASE}/post",
                     json={"name": "Alice", "role": "Data Scientist"})
print("POST:", resp.json()["json"])

# PUT — full replace
resp = requests.put(f"{BASE}/put",
                    json={"name": "Alice", "role": "ML Engineer"})
print("PUT:", resp.json()["json"])

# PATCH — partial update
resp = requests.patch(f"{BASE}/patch",
                      json={"role": "Senior ML Engineer"})
print("PATCH:", resp.json()["json"])

# DELETE
resp = requests.delete(f"{BASE}/delete")
print("DELETE status:", resp.status_code)"""},
{"label": "Custom headers and timeouts", "code":
"""import requests

headers = {
    "User-Agent": "DataScienceStudyGuide/1.0",
    "Accept": "application/json",
}

# Always set a timeout! Never let requests hang forever
try:
    resp = requests.get("https://httpbin.org/delay/1",
                        headers=headers,
                        timeout=5)      # 5 second timeout
    print(f"Success: {resp.status_code} in {resp.elapsed.total_seconds():.2f}s")
except requests.Timeout:
    print("Request timed out!")
except requests.ConnectionError:
    print("Could not connect!")

# Timeout can be a tuple: (connect_timeout, read_timeout)
resp = requests.get("https://httpbin.org/get", timeout=(3.05, 10))
print(f"With tuple timeout: {resp.status_code}")"""},
],
"rw": {
    "todos": [
    "Make a GET request to https://httpbin.org/get and print the response headers",
    "Add a custom User-Agent header to a request and verify the server received it",
    "Make a POST request with a JSON body to https://httpbin.org/post and check the echo",
    "Set a 3-second timeout and test it against https://httpbin.org/delay/5 to trigger a Timeout",
    "Catch requests.ConnectionError by pointing to a non-existent host and print the error",
],
"title": "Fetching Weather Data",
    "scenario": "A data team needs to collect daily weather data for their supply chain forecasting model. They use the Open-Meteo API (free, no API key needed) to fetch temperature and precipitation data.",
    "code":
"""import requests

def get_weather(lat, lon, days=7):
    \"\"\"Fetch weather forecast from Open-Meteo API.\"\"\"
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto",
            "forecast_days": days,
        },
        timeout=10,
    )
    resp.raise_for_status()  # Raise exception on 4xx/5xx
    return resp.json()

# New York City
data = get_weather(40.71, -74.01)

daily = data["daily"]
for date, tmax, tmin, rain in zip(
    daily["time"],
    daily["temperature_2m_max"],
    daily["temperature_2m_min"],
    daily["precipitation_sum"],
):
    print(f"{date}  High: {tmax}°C  Low: {tmin}°C  Rain: {rain}mm")"""
},
"practice": {
    "title": "Build a Multi-City Weather Fetcher",
    "desc": "Extend the weather example: fetch forecasts for 3 cities, compare their max temperatures, and find which city is warmest on average.",
    "starter":
"""import requests

cities = {
    "New York": (40.71, -74.01),
    "London":   (51.51, -0.13),
    "Tokyo":    (35.68, 139.69),
}

def fetch_forecasts(cities_dict, days=7):
    results = {}
    for city, (lat, lon) in cities_dict.items():
        # TODO: fetch weather for each city
        # Store the daily max temperatures
        pass
    return results

def find_warmest(results):
    # TODO: calculate average max temp per city
    # Return the city name with highest average
    pass

forecasts = fetch_forecasts(cities)
warmest = find_warmest(forecasts)
print(f"Warmest city on average: {warmest}")"""
}
},

{
"title": "3. Working with JSON Responses",
"desc": "Most modern APIs return JSON. Python's requests library auto-decodes it, and you can navigate nested structures, validate data, and convert to various formats.",
"examples": [
{"label": "Navigating nested JSON", "code":
"""import requests, json

# GitHub API returns deeply nested JSON
resp = requests.get("https://api.github.com/repos/python/cpython",
                     timeout=10)
repo = resp.json()

# Navigate nested structure
print(f"Name:       {repo['name']}")
print(f"Stars:      {repo['stargazers_count']:,}")
print(f"Language:   {repo['language']}")
print(f"Owner:      {repo['owner']['login']}")
print(f"Owner Type: {repo['owner']['type']}")

# Safe access with .get() for optional fields
license_name = repo.get("license", {}).get("name", "Unknown")
print(f"License:    {license_name}")"""},
{"label": "Pretty-printing and exploring JSON", "code":
"""import requests, json

resp = requests.get("https://api.github.com/users/octocat", timeout=10)
data = resp.json()

# Pretty print for exploration
print(json.dumps(data, indent=2)[:500])

# List all top-level keys
print(f"\\nKeys ({len(data)}): {list(data.keys())}")

# Find all string vs non-string fields
strings = [k for k, v in data.items() if isinstance(v, str)]
others  = [k for k, v in data.items() if not isinstance(v, str)]
print(f"String fields: {strings[:5]}...")
print(f"Other fields:  {others}")"""},
{"label": "JSON to Python objects and back", "code":
"""import json
from datetime import datetime

# Python dict → JSON string
event = {
    "name": "Model Training Complete",
    "timestamp": datetime.now().isoformat(),
    "metrics": {"accuracy": 0.95, "loss": 0.12},
    "tags": ["production", "v2.1"],
}

json_str = json.dumps(event, indent=2)
print("Serialized:")
print(json_str)

# JSON string → Python dict
parsed = json.loads(json_str)
print(f"\\nAccuracy: {parsed['metrics']['accuracy']}")

# Save to file
with open("event.json", "w") as f:
    json.dump(event, f, indent=2)

# Load from file
with open("event.json") as f:
    loaded = json.load(f)
print(f"Loaded: {loaded['name']}")

import os; os.remove("event.json")  # cleanup"""},
],
"rw": {
    "todos": [
    "Fetch https://api.github.com/users/octocat and safely access the 'company' field with .get()",
    "Pretty-print a JSON response using json.dumps(data, indent=2) to understand its structure",
    "Use json.dump to write a dict to a file, then json.load to read it back and verify",
    "Write a function that flattens one level of nesting from a list of dicts",
    "Use pd.json_normalize on a nested response with sep='_' and inspect the resulting columns",
],
"title": "Flattening Nested API Responses",
    "scenario": "An analytics pipeline receives deeply nested JSON from a CRM API. You need to flatten it into a tabular format suitable for a Pandas DataFrame.",
    "code":
"""import json

# Simulated nested API response (typical CRM data)
api_response = {
    "data": [
        {
            "id": 1,
            "name": "Acme Corp",
            "contact": {"email": "info@acme.com", "phone": "+1-555-0100"},
            "deals": [
                {"title": "Enterprise License", "value": 50000, "stage": "won"},
                {"title": "Support Plan", "value": 12000, "stage": "negotiation"},
            ],
        },
        {
            "id": 2,
            "name": "Globex Inc",
            "contact": {"email": "sales@globex.com", "phone": "+1-555-0200"},
            "deals": [
                {"title": "Starter Plan", "value": 5000, "stage": "won"},
            ],
        },
    ],
    "meta": {"total": 2, "page": 1},
}

def flatten_crm(response):
    rows = []
    for company in response["data"]:
        base = {
            "company_id": company["id"],
            "company_name": company["name"],
            "email": company["contact"]["email"],
            "phone": company["contact"]["phone"],
        }
        for deal in company.get("deals", []):
            row = {**base, **{f"deal_{k}": v for k, v in deal.items()}}
            rows.append(row)
    return rows

flat = flatten_crm(api_response)
for row in flat:
    print(f"  {row['company_name']:12s} | {row['deal_title']:20s} | ${row['deal_value']:>8,}")

print(f"\\nTotal rows: {len(flat)}")"""
},
"practice": {
    "title": "JSON Response Validator",
    "desc": "Write a function that validates an API response has the expected structure. Check for required keys, correct types, and non-null values.",
    "starter":
"""def validate_response(data, schema):
    \"\"\"Validate that data matches the expected schema.

    schema format: {"key": type, ...} e.g. {"name": str, "age": int}
    Returns (is_valid, errors_list)
    \"\"\"
    errors = []
    # TODO: check each key in schema exists in data
    # TODO: check types match
    # TODO: check values are not None
    return len(errors) == 0, errors

# Test
user_data = {"name": "Alice", "age": 30, "email": "alice@example.com", "score": None}
schema = {"name": str, "age": int, "email": str, "score": float}

valid, errors = validate_response(user_data, schema)
print(f"Valid: {valid}")
for e in errors:
    print(f"  - {e}")"""
}
},

{
"title": "4. JSON to Pandas DataFrame",
"desc": "The bridge between APIs and data analysis. Learn to convert JSON responses into clean DataFrames ready for analysis, handling nested structures and missing data.",
"examples": [
{"label": "Simple JSON list → DataFrame", "code":
"""import pandas as pd
import requests

# JSONPlaceholder — free fake API for testing
resp = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
users = resp.json()

# Direct conversion — works when JSON is a flat list of dicts
df = pd.DataFrame(users)
print(df[["id", "name", "email", "phone"]].head())
print(f"\\nShape: {df.shape}")
print(f"Columns: {list(df.columns)}")"""},
{"label": "Nested JSON → DataFrame with json_normalize", "code":
"""import pandas as pd

# Nested data (typical API response)
data = [
    {"id": 1, "name": "Alice",
     "address": {"city": "NYC", "zip": "10001"},
     "scores": {"math": 95, "science": 88}},
    {"id": 2, "name": "Bob",
     "address": {"city": "LA", "zip": "90001"},
     "scores": {"math": 82, "science": 91}},
]

# json_normalize flattens nested dicts
df = pd.json_normalize(data)
print(df)
# Columns: id, name, address.city, address.zip, scores.math, scores.science

# Custom separator
df2 = pd.json_normalize(data, sep="_")
print(f"\\nColumns with underscore sep: {list(df2.columns)}")"""},
{"label": "Handling paginated API → single DataFrame", "code":
"""import pandas as pd
import requests

def fetch_all_posts(limit=30):
    \"\"\"Fetch posts from JSONPlaceholder, simulating pagination.\"\"\"
    all_posts = []
    page_size = 10

    for start in range(0, limit, page_size):
        resp = requests.get(
            "https://jsonplaceholder.typicode.com/posts",
            params={"_start": start, "_limit": page_size},
            timeout=10,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        all_posts.extend(batch)
        print(f"  Fetched {len(batch)} posts (total: {len(all_posts)})")

    return pd.DataFrame(all_posts)

df = fetch_all_posts(30)
print(f"\\nDataFrame shape: {df.shape}")
print(df.groupby("userId")["id"].count().head())"""},
{"label": "Cleaning API data in a DataFrame", "code":
"""import pandas as pd

# Simulated messy API response
raw = [
    {"id": 1, "created_at": "2024-01-15T10:30:00Z", "amount": "1500.50", "status": "completed"},
    {"id": 2, "created_at": "2024-01-16T14:20:00Z", "amount": "2300.00", "status": "pending"},
    {"id": 3, "created_at": "2024-01-16T09:00:00Z", "amount": None,       "status": "failed"},
    {"id": 4, "created_at": "2024-01-17T16:45:00Z", "amount": "890.25",  "status": "completed"},
]

df = pd.DataFrame(raw)

# Convert types
df["created_at"] = pd.to_datetime(df["created_at"])
df["amount"]     = pd.to_numeric(df["amount"], errors="coerce")
df["status"]     = df["status"].astype("category")

# Add derived columns
df["date"]       = df["created_at"].dt.date
df["hour"]       = df["created_at"].dt.hour

print(df.dtypes)
print()
print(df)"""},
],
"rw": {
    "todos": [
    "Convert a flat JSON list from JSONPlaceholder directly to a DataFrame with pd.DataFrame()",
    "Use pd.json_normalize on a nested JSON list with sep='_' to flatten one level",
    "Fetch two paginated batches from an API and concatenate them into one DataFrame",
    "Convert an 'amount' column from string to float using pd.to_numeric(errors='coerce')",
    "Parse a 'created_at' timestamp column to datetime and extract the hour of day",
],
"title": "Building a Stock Price Dataset from API",
    "scenario": "A quant team collects daily stock data from Alpha Vantage's free API, cleans it, and stores it as a Parquet file for their backtesting pipeline.",
    "code":
"""import pandas as pd

# Simulated Alpha Vantage-style response (real API requires a free key)
api_data = {
    "Meta Data": {"2. Symbol": "AAPL", "3. Last Refreshed": "2024-01-17"},
    "Time Series (Daily)": {
        "2024-01-17": {"1. open": "182.16", "2. high": "184.26", "3. low": "180.93", "4. close": "183.63", "5. volume": "65076600"},
        "2024-01-16": {"1. open": "181.27", "2. high": "182.93", "3. low": "180.17", "4. close": "181.18", "5. volume": "51423800"},
        "2024-01-12": {"1. open": "183.92", "2. high": "185.15", "3. low": "182.73", "4. close": "185.59", "5. volume": "54321200"},
        "2024-01-11": {"1. open": "184.35", "2. high": "185.56", "3. low": "182.11", "4. close": "182.32", "5. volume": "49873600"},
        "2024-01-10": {"1. open": "184.10", "2. high": "185.60", "3. low": "183.62", "4. close": "185.14", "5. volume": "46792800"},
    },
}

def parse_stock_data(response):
    symbol = response["Meta Data"]["2. Symbol"]
    ts = response["Time Series (Daily)"]

    # Convert nested dict → DataFrame
    df = pd.DataFrame.from_dict(ts, orient="index")

    # Clean column names: "1. open" → "open"
    df.columns = [c.split(". ")[1] for c in df.columns]

    # Fix types
    df.index = pd.to_datetime(df.index)
    df.index.name = "date"
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])

    df = df.sort_index()
    df["symbol"] = symbol
    df["daily_return"] = df["close"].pct_change()
    return df

df = parse_stock_data(api_data)
print(df[["open", "high", "low", "close", "volume", "daily_return"]])
print(f"\\nAvg daily return: {df['daily_return'].mean():.4%}")"""
},
"practice": {
    "title": "API Response → Analytical DataFrame",
    "desc": "Fetch posts and users from JSONPlaceholder, merge them, and calculate which user writes the longest posts on average.",
    "starter":
"""import pandas as pd
import requests

# TODO: Fetch users from https://jsonplaceholder.typicode.com/users
# TODO: Fetch posts from https://jsonplaceholder.typicode.com/posts
# TODO: Create DataFrames for both
# TODO: Merge on userId
# TODO: Calculate average post body length per user
# TODO: Print top 3 users by average post length

# Your code here:
"""
}
},

{
"title": "5. Authentication — API Keys & Tokens",
"desc": "Most real APIs require authentication. The three most common methods are API keys (in headers or query params), Bearer tokens (OAuth), and Basic auth (username/password).",
"examples": [
{"label": "API Key in headers", "code":
"""import requests

# Method 1: API key in header (most common)
headers = {"X-API-Key": "your-api-key-here"}
# resp = requests.get("https://api.example.com/data", headers=headers)

# Method 2: API key as query parameter
params = {"api_key": "your-api-key-here", "q": "python"}
# resp = requests.get("https://api.example.com/search", params=params)

# Example with httpbin (echoes back what you send)
resp = requests.get("https://httpbin.org/headers",
                     headers={"X-API-Key": "demo-key-12345"},
                     timeout=10)
print("Server received headers:")
for k, v in resp.json()["headers"].items():
    print(f"  {k}: {v}")"""},
{"label": "Bearer token authentication (OAuth2)", "code":
"""import requests

# Bearer tokens are the standard for OAuth2 APIs
token = "your-oauth-token-here"
headers = {"Authorization": f"Bearer {token}"}

# Example: GitHub API with personal access token
# (works without token too, but with lower rate limits)
resp = requests.get("https://api.github.com/user",
                     headers={"Authorization": "Bearer ghp_xxxx"},
                     timeout=10)
print(f"Status: {resp.status_code}")  # 401 with fake token

# Check rate limit headers
print(f"Rate limit: {resp.headers.get('X-RateLimit-Limit', 'N/A')}")
print(f"Remaining:  {resp.headers.get('X-RateLimit-Remaining', 'N/A')}")"""},
{"label": "Basic authentication", "code":
"""import requests
from requests.auth import HTTPBasicAuth

# Basic auth sends base64-encoded username:password
resp = requests.get("https://httpbin.org/basic-auth/user/passwd",
                     auth=HTTPBasicAuth("user", "passwd"),
                     timeout=10)
print(f"Status: {resp.status_code}")
print(f"Body:   {resp.json()}")

# Shorthand — tuple works too
resp = requests.get("https://httpbin.org/basic-auth/user/passwd",
                     auth=("user", "passwd"),
                     timeout=10)
print(f"Shorthand: {resp.json()}")"""},
{"label": "Storing credentials securely with environment variables", "code":
"""import os

# NEVER hardcode credentials in source code!
# Store them in environment variables

# Set in terminal first:
#   export API_KEY="your-secret-key"      (Linux/Mac)
#   set API_KEY=your-secret-key           (Windows)

# Or use a .env file with python-dotenv:
# pip install python-dotenv
# from dotenv import load_dotenv
# load_dotenv()  # loads from .env file

api_key = os.environ.get("API_KEY", "demo-fallback-key")
db_url  = os.environ.get("DATABASE_URL", "sqlite:///local.db")

print(f"API Key loaded: {'*' * len(api_key)}")  # Don't print actual key!
print(f"DB URL loaded:  {db_url[:20]}...")

# .env file format (add to .gitignore!):
# API_KEY=sk-abc123
# DATABASE_URL=postgresql://user:pass@host/db"""},
],
"rw": {
    "todos": [
    "Load an API key from an environment variable and use it in an Authorization Bearer header",
    "Send a request to https://httpbin.org/headers and confirm your custom header was received",
    "Test HTTPBasicAuth with https://httpbin.org/basic-auth/user/passwd",
    "Store credentials in a .env file (never committed to git) and load them with python-dotenv",
    "Write a function that raises a clear error if a required environment variable is missing",
],
"title": "Secure API Client with Key Rotation",
    "scenario": "A production data pipeline needs to authenticate with multiple APIs. Keys are loaded from environment variables and the client handles 401 (unauthorized) responses gracefully.",
    "code":
"""import os
import requests

class SecureAPIClient:
    def __init__(self, base_url, key_env_var):
        self.base_url = base_url
        self.api_key = os.environ.get(key_env_var, "")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "DataPipeline/1.0",
        })
        self.session.timeout = 15

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        resp = self.session.get(url, params=params)

        if resp.status_code == 401:
            print(f"[AUTH ERROR] Key expired or invalid for {url}")
            return None
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 60))
            print(f"[RATE LIMIT] Retry after {retry_after}s")
            return None

        resp.raise_for_status()
        return resp.json()

# Usage
client = SecureAPIClient("https://httpbin.org", "MY_API_KEY")
data = client.get("/get", params={"test": "hello"})
if data:
    print(f"Success! Got {len(data)} keys")"""
},
"practice": {
    "title": "Environment-Based Config Loader",
    "desc": "Build a config class that loads API credentials from environment variables with validation. It should warn about missing keys and support a .env fallback.",
    "starter":
"""import os

class APIConfig:
    REQUIRED_KEYS = ["API_KEY", "API_SECRET", "BASE_URL"]

    def __init__(self, prefix="MYAPP"):
        self.prefix = prefix
        self.config = {}
        self._load()

    def _load(self):
        # TODO: load each REQUIRED_KEY with prefix (e.g., MYAPP_API_KEY)
        # TODO: warn if any key is missing
        pass

    def get(self, key):
        # TODO: return config value, raise if missing
        pass

    def is_valid(self):
        # TODO: return True only if all required keys are present
        pass

# Test (set env vars first or test with defaults)
config = APIConfig("DEMO")
print(f"Config valid: {config.is_valid()}")"""
}
},

{
"title": "6. Sessions & Connection Pooling",
"desc": "requests.Session reuses the underlying TCP connection across requests, making repeated calls to the same host significantly faster. It also persists headers, cookies, and auth.",
"examples": [
{"label": "Basic session usage", "code":
"""import requests
import time

# WITHOUT session — new connection every time
start = time.time()
for _ in range(5):
    requests.get("https://httpbin.org/get", timeout=10)
no_session = time.time() - start

# WITH session — reuses connection
session = requests.Session()
start = time.time()
for _ in range(5):
    session.get("https://httpbin.org/get", timeout=10)
with_session = time.time() - start
session.close()

print(f"Without session: {no_session:.2f}s")
print(f"With session:    {with_session:.2f}s")
print(f"Speedup:         {no_session/with_session:.1f}x")"""},
{"label": "Persisting headers and auth across requests", "code":
"""import requests

session = requests.Session()

# Set default headers for ALL requests in this session
session.headers.update({
    "Authorization": "Bearer my-token",
    "Accept": "application/json",
    "User-Agent": "DataPipeline/2.0",
})

# These requests all include the headers above
r1 = session.get("https://httpbin.org/headers", timeout=10)
r2 = session.get("https://httpbin.org/get", timeout=10)

print("Headers sent automatically:")
for k, v in r1.json()["headers"].items():
    if k in ("Authorization", "Accept", "User-Agent"):
        print(f"  {k}: {v}")

# Override a header for one specific request
r3 = session.get("https://httpbin.org/headers",
                  headers={"Accept": "text/plain"},
                  timeout=10)
print(f"\\nOverridden Accept: {r3.json()['headers']['Accept']}")
session.close()"""},
{"label": "Session as context manager", "code":
"""import requests

# Automatically closes the session when done
with requests.Session() as s:
    s.headers["X-Request-Source"] = "study-guide"

    # Cookies persist across requests in a session
    s.get("https://httpbin.org/cookies/set/session_id/abc123", timeout=10)
    r = s.get("https://httpbin.org/cookies", timeout=10)
    print(f"Cookies: {r.json()['cookies']}")

    # Session tracks cookie jar
    print(f"Cookie jar: {dict(s.cookies)}")"""},
],
"rw": {
    "todos": [
    "Make 5 requests with and without a Session and print the time difference",
    "Set session-level default headers and verify they are sent with every request",
    "Use a Session as a context manager (with requests.Session() as s:) for automatic cleanup",
    "Mount a Retry adapter on a Session to auto-retry on 500 and 503 status codes",
    "Use session.cookies to inspect cookies that were set by a previous response",
],
"title": "Production API Client with Session",
    "scenario": "A data team builds a reusable API client class that uses sessions for performance, handles retries on transient errors, and logs request timing.",
    "code":
"""import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class RobustClient:
    def __init__(self, base_url, api_key, max_retries=3):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        })

        # Retry on 429, 500, 502, 503, 504
        retry = Retry(
            total=max_retries,
            backoff_factor=1,          # 1s, 2s, 4s...
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, endpoint, **kwargs):
        kwargs.setdefault("timeout", 15)
        resp = self.session.get(f"{self.base_url}/{endpoint}", **kwargs)
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self.session.close()

# Usage
client = RobustClient("https://httpbin.org", "demo-key")
data = client.get("get", params={"test": True})
print(f"Got response with {len(data)} keys")
client.close()"""
},
},

{
"title": "7. Pagination — Fetching All the Data",
"desc": "APIs rarely return all data at once. Pagination splits results across multiple requests. Common patterns: page/per_page, offset/limit, and cursor-based.",
"examples": [
{"label": "Page-number pagination", "code":
"""import requests

def fetch_all_page_number(base_url, per_page=10, max_pages=50):
    \"\"\"Standard page-number pagination (page=1, page=2, ...).\"\"\"
    all_items = []

    for page in range(1, max_pages + 1):
        resp = requests.get(base_url, params={"_page": page, "_limit": per_page}, timeout=10)
        resp.raise_for_status()
        items = resp.json()

        if not items:  # Empty page = we've fetched everything
            break

        all_items.extend(items)
        print(f"  Page {page}: {len(items)} items (total: {len(all_items)})")

    return all_items

posts = fetch_all_page_number(
    "https://jsonplaceholder.typicode.com/posts",
    per_page=25,
)
print(f"\\nTotal posts fetched: {len(posts)}")"""},
{"label": "Offset/limit pagination", "code":
"""import requests

def fetch_all_offset(base_url, limit=20, max_items=100):
    \"\"\"Offset-based pagination (_start=0, _start=20, ...).\"\"\"
    all_items = []
    offset = 0

    while offset < max_items:
        resp = requests.get(
            base_url,
            params={"_start": offset, "_limit": limit},
            timeout=10,
        )
        resp.raise_for_status()
        batch = resp.json()

        if not batch:
            break

        all_items.extend(batch)
        offset += len(batch)
        print(f"  Offset {offset - len(batch)}→{offset}: got {len(batch)}")

    return all_items

comments = fetch_all_offset(
    "https://jsonplaceholder.typicode.com/comments",
    limit=100,
    max_items=500,
)
print(f"\\nTotal comments: {len(comments)}")"""},
{"label": "Cursor-based pagination (link header)", "code":
"""import requests

def fetch_all_cursor(url, per_page=30, max_pages=10):
    \"\"\"Cursor/link-based pagination — follow 'next' links.
    Used by GitHub, Slack, Stripe, and many modern APIs.\"\"\"
    all_items = []
    page = 0

    while url and page < max_pages:
        resp = requests.get(url, params={"per_page": per_page}, timeout=10)
        resp.raise_for_status()
        all_items.extend(resp.json())
        page += 1

        # Parse Link header for next page URL
        link = resp.headers.get("Link", "")
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip(" <>")
                break

        print(f"  Page {page}: {len(resp.json())} items | next={'yes' if url else 'no'}")

    return all_items

# GitHub repos use link-header pagination
repos = fetch_all_cursor(
    "https://api.github.com/users/octocat/repos",
    per_page=10,
    max_pages=3,
)
print(f"\\nTotal repos: {len(repos)}")"""},
],
"rw": {
    "todos": [
    "Fetch all 100 posts from JSONPlaceholder using page-number pagination (_page, _limit params)",
    "Implement offset-based pagination and print the total item count after all pages are fetched",
    "Parse the Link response header to extract the 'next' URL for cursor-based pagination",
    "Add a checkpoint mechanism that saves progress to a file every 5 pages",
    "Write a generator function that yields one page at a time from a paginated API",
],
"title": "Complete Data Extraction Pipeline",
    "scenario": "A data engineer needs to extract ALL records from a paginated API, handle rate limits, track progress, and save checkpoints in case of failure.",
    "code":
"""import requests
import json
import time

def extract_all(base_url, per_page=100, checkpoint_file="checkpoint.json"):
    \"\"\"Extract all records with progress tracking and checkpointing.\"\"\"
    # Resume from checkpoint if exists
    try:
        with open(checkpoint_file) as f:
            state = json.load(f)
        all_items = state["items"]
        page = state["next_page"]
        print(f"Resuming from page {page} ({len(all_items)} items cached)")
    except FileNotFoundError:
        all_items = []
        page = 1

    while True:
        resp = requests.get(
            base_url,
            params={"_page": page, "_limit": per_page},
            timeout=30,
        )

        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 60))
            print(f"  Rate limited. Waiting {wait}s...")
            time.sleep(wait)
            continue

        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break

        all_items.extend(batch)
        page += 1

        # Save checkpoint every 5 pages
        if page % 5 == 0:
            with open(checkpoint_file, "w") as f:
                json.dump({"items": all_items, "next_page": page}, f)
            print(f"  Checkpoint saved at page {page} ({len(all_items)} items)")

    print(f"Done! Extracted {len(all_items)} total items")
    return all_items

posts = extract_all("https://jsonplaceholder.typicode.com/posts", per_page=25)

import os
if os.path.exists("checkpoint.json"):
    os.remove("checkpoint.json")"""
},
"practice": {
    "title": "Generic Paginator Class",
    "desc": "Build a reusable Paginator class that supports both page-number and offset-based pagination. It should yield batches and track total items fetched.",
    "starter":
"""import requests

class Paginator:
    def __init__(self, base_url, mode="page", per_page=10, max_items=100):
        \"\"\"mode: 'page' for page-number, 'offset' for offset-based.\"\"\"
        self.base_url = base_url
        self.mode = mode
        self.per_page = per_page
        self.max_items = max_items
        self.total_fetched = 0

    def __iter__(self):
        # TODO: implement pagination logic
        # Yield each batch of items
        # Track self.total_fetched
        pass

# Test with page mode
print("Page mode:")
for batch in Paginator("https://jsonplaceholder.typicode.com/posts",
                       mode="page", per_page=25, max_items=50):
    print(f"  Got {len(batch)} items")

# Test with offset mode
print("\\nOffset mode:")
for batch in Paginator("https://jsonplaceholder.typicode.com/comments",
                       mode="offset", per_page=50, max_items=150):
    print(f"  Got {len(batch)} items")"""
}
},

{
"title": "8. Rate Limiting & Throttling",
"desc": "APIs enforce rate limits to prevent abuse. You need to respect these limits by reading response headers, implementing backoff strategies, and throttling your requests.",
"examples": [
{"label": "Reading rate limit headers", "code":
"""import requests

resp = requests.get("https://api.github.com/rate_limit", timeout=10)
limits = resp.json()["rate"]

print(f"Limit:     {limits['limit']} requests/hour")
print(f"Remaining: {limits['remaining']}")
print(f"Resets at: {limits['reset']} (unix timestamp)")

# Calculate wait time
import time
reset_time = limits["reset"]
wait_seconds = max(0, reset_time - time.time())
print(f"Resets in:  {wait_seconds:.0f} seconds")

# Common rate limit headers:
# X-RateLimit-Limit     — max requests per window
# X-RateLimit-Remaining — requests left in window
# X-RateLimit-Reset     — when the window resets (unix timestamp)
# Retry-After           — seconds to wait (sent with 429 status)"""},
{"label": "Simple throttle with time.sleep", "code":
"""import requests
import time

def throttled_fetch(urls, requests_per_second=2):
    \"\"\"Fetch URLs with a simple rate limiter.\"\"\"
    delay = 1.0 / requests_per_second
    results = []

    for i, url in enumerate(urls):
        if i > 0:
            time.sleep(delay)

        resp = requests.get(url, timeout=10)
        results.append(resp.json())
        print(f"  [{i+1}/{len(urls)}] {resp.status_code} in {resp.elapsed.total_seconds():.2f}s")

    return results

urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 6)]
data = throttled_fetch(urls, requests_per_second=3)
print(f"\\nFetched {len(data)} items")"""},
{"label": "Exponential backoff on errors", "code":
"""import requests
import time
import random

def fetch_with_backoff(url, max_retries=5, base_delay=1):
    \"\"\"Retry with exponential backoff + jitter.\"\"\"
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=10)

            if resp.status_code == 429:
                # Use Retry-After header if available
                wait = int(resp.headers.get("Retry-After", base_delay * (2 ** attempt)))
                jitter = random.uniform(0, wait * 0.1)
                print(f"  Rate limited. Waiting {wait + jitter:.1f}s (attempt {attempt + 1})")
                time.sleep(wait + jitter)
                continue

            if resp.status_code >= 500:
                wait = base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"  Server error {resp.status_code}. Retry in {wait:.1f}s")
                time.sleep(wait)
                continue

            resp.raise_for_status()
            return resp.json()

        except requests.ConnectionError:
            wait = base_delay * (2 ** attempt)
            print(f"  Connection failed. Retry in {wait:.1f}s")
            time.sleep(wait)

    raise Exception(f"Failed after {max_retries} retries: {url}")

data = fetch_with_backoff("https://httpbin.org/get")
print(f"Success: {list(data.keys())}")"""},
],
"rw": {
    "todos": [
    "Check the X-RateLimit-Remaining header from the GitHub API and print how many calls are left",
    "Write a throttled loop that makes no more than 3 requests per second using time.sleep",
    "Implement exponential backoff: on a 429, wait 1s, 2s, 4s, 8s before giving up",
    "Read the Retry-After header from a 429 response and sleep for that exact duration",
    "Build a token-bucket rate limiter class and test it with 10 requests at 5 req/sec",
],
"title": "Production Rate Limiter",
    "scenario": "A data collection service needs to respect API rate limits across multiple endpoints, track usage, and automatically pause when approaching limits.",
    "code":
"""import time
from collections import defaultdict

class RateLimiter:
    \"\"\"Token bucket rate limiter for API calls.\"\"\"

    def __init__(self, calls_per_second=5):
        self.rate = calls_per_second
        self.tokens = calls_per_second
        self.last_refill = time.time()
        self.total_calls = 0
        self.total_waits = 0

    def acquire(self):
        \"\"\"Wait until a token is available, then consume it.\"\"\"
        while self.tokens < 1:
            self._refill()
            if self.tokens < 1:
                sleep_time = (1 - self.tokens) / self.rate
                time.sleep(sleep_time)
                self.total_waits += 1
        self._refill()
        self.tokens -= 1
        self.total_calls += 1

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.rate, self.tokens + elapsed * self.rate)
        self.last_refill = now

    def stats(self):
        return f"Total calls: {self.total_calls}, Waits: {self.total_waits}"

# Usage
import requests

limiter = RateLimiter(calls_per_second=3)

start = time.time()
for i in range(6):
    limiter.acquire()
    resp = requests.get("https://httpbin.org/get", timeout=10)
    print(f"  Request {i+1}: {resp.status_code} at t={time.time()-start:.2f}s")

print(f"\\n{limiter.stats()}")"""
},
},

{
"title": "9. Error Handling & Resilience",
"desc": "Production API calls fail. Networks drop, servers error, responses are malformed. Robust code anticipates and handles every failure mode gracefully.",
"examples": [
{"label": "Comprehensive error handling", "code":
"""import requests

def safe_api_call(url, params=None, timeout=10):
    \"\"\"Make an API call with comprehensive error handling.\"\"\"
    try:
        resp = requests.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
        return {"ok": True, "data": resp.json(), "status": resp.status_code}

    except requests.Timeout:
        return {"ok": False, "error": "Request timed out", "status": None}
    except requests.ConnectionError:
        return {"ok": False, "error": "Could not connect", "status": None}
    except requests.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.response.status_code}", "status": e.response.status_code}
    except requests.JSONDecodeError:
        return {"ok": False, "error": "Invalid JSON response", "status": resp.status_code}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e), "status": None}

# Test with various scenarios
urls = [
    "https://httpbin.org/get",           # Success
    "https://httpbin.org/status/404",     # Not Found
    "https://httpbin.org/status/500",     # Server Error
    "https://httpbin.org/delay/30",       # Will timeout
]

for url in urls[:3]:  # skip slow timeout test
    result = safe_api_call(url, timeout=5)
    status = "OK" if result["ok"] else "FAIL"
    print(f"  [{status}] {url.split('/')[-1]:>10} → {result.get('error', 'success')}")"""},
{"label": "Retry decorator pattern", "code":
"""import requests
import time
import functools

def retry(max_attempts=3, backoff=2, exceptions=(requests.RequestException,)):
    \"\"\"Decorator that retries a function with exponential backoff.\"\"\"
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        wait = backoff ** attempt
                        print(f"  Attempt {attempt} failed: {e}. Retrying in {wait}s...")
                        time.sleep(wait)
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, backoff=1)
def fetch_data(url):
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()

data = fetch_data("https://httpbin.org/get")
print(f"Success: {list(data.keys())}")"""},
{"label": "Response validation", "code":
"""import requests

def validated_fetch(url, required_fields=None, timeout=10):
    \"\"\"Fetch and validate that response has expected structure.\"\"\"
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()

    if required_fields:
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"Response missing fields: {missing}")

    return data

# Validate GitHub user response has expected fields
user = validated_fetch(
    "https://api.github.com/users/octocat",
    required_fields=["login", "id", "avatar_url", "name"],
)
print(f"Valid user: {user['login']} (id={user['id']})")

# This would raise ValueError:
# validated_fetch("https://httpbin.org/get", required_fields=["nonexistent"])"""},
],
"rw": {
    "todos": [
    "Wrap a requests.get call to catch Timeout, ConnectionError, and HTTPError separately",
    "Write a retry decorator that re-attempts a failing function up to 3 times with backoff",
    "Use resp.raise_for_status() and catch HTTPError to log the status code on failure",
    "Write a validated_fetch function that raises ValueError if a required JSON key is missing",
    "Test your error handling by pointing to https://httpbin.org/status/500 and 404",
],
"title": "Resilient Multi-Source Data Collector",
    "scenario": "A data pipeline fetches from 3 different APIs. If one fails, it logs the error and continues with the others, then reports a summary of successes and failures.",
    "code":
"""import requests
import time

class DataCollector:
    def __init__(self):
        self.results = {}
        self.errors = {}

    def fetch(self, name, url, params=None, retries=3):
        for attempt in range(1, retries + 1):
            try:
                resp = requests.get(url, params=params, timeout=10)
                resp.raise_for_status()
                self.results[name] = resp.json()
                print(f"  [OK]   {name} — {len(str(resp.json()))} bytes")
                return
            except requests.RequestException as e:
                if attempt < retries:
                    time.sleep(2 ** attempt)
                else:
                    self.errors[name] = str(e)
                    print(f"  [FAIL] {name} — {e}")

    def summary(self):
        total = len(self.results) + len(self.errors)
        print(f"\\nResults: {len(self.results)}/{total} succeeded")
        if self.errors:
            print("Failures:")
            for name, err in self.errors.items():
                print(f"  - {name}: {err}")

# Collect from multiple sources
collector = DataCollector()
collector.fetch("users", "https://jsonplaceholder.typicode.com/users")
collector.fetch("posts", "https://jsonplaceholder.typicode.com/posts", params={"_limit": 5})
collector.fetch("broken", "https://httpbin.org/status/500")
collector.summary()"""
},
"practice": {
    "title": "Build a Circuit Breaker",
    "desc": "Implement a circuit breaker pattern: after N consecutive failures to an API, stop trying for a cooldown period. Track state: CLOSED (normal), OPEN (failing, skip calls), HALF-OPEN (try one request).",
    "starter":
"""import time
import requests

class CircuitBreaker:
    def __init__(self, failure_threshold=3, cooldown=10):
        self.failure_threshold = failure_threshold
        self.cooldown = cooldown
        self.failures = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = None

    def call(self, url, **kwargs):
        # TODO: if OPEN, check if cooldown has passed → HALF_OPEN
        # TODO: if OPEN and cooldown not passed, raise without calling
        # TODO: make the request
        # TODO: on success, reset to CLOSED
        # TODO: on failure, increment counter, maybe go to OPEN
        pass

# Test
cb = CircuitBreaker(failure_threshold=2, cooldown=5)
urls = [
    "https://httpbin.org/get",        # works
    "https://httpbin.org/status/500",  # fails
    "https://httpbin.org/status/500",  # fails → opens circuit
    "https://httpbin.org/get",         # should be blocked
]
for url in urls:
    try:
        data = cb.call(url, timeout=5)
        print(f"  OK:   {url.split('/')[-1]} | state={cb.state}")
    except Exception as e:
        print(f"  FAIL: {url.split('/')[-1]} | {e} | state={cb.state}")"""
}
},

{
"title": "10. Async API Calls with aiohttp",
"desc": "When you need to call many APIs concurrently, async IO is dramatically faster than sequential requests. aiohttp is the async equivalent of requests. Install: pip install aiohttp.",
"examples": [
{"label": "Basic async requests", "code":
"""import asyncio
import aiohttp
import time

async def fetch(session, url):
    async with session.get(url) as resp:
        data = await resp.json()
        return data

async def main():
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 11)]

    async with aiohttp.ClientSession() as session:
        # Sequential (slow)
        start = time.time()
        for url in urls:
            await fetch(session, url)
        seq_time = time.time() - start

        # Concurrent (fast!)
        start = time.time()
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        par_time = time.time() - start

    print(f"Sequential: {seq_time:.2f}s")
    print(f"Concurrent: {par_time:.2f}s")
    print(f"Speedup:    {seq_time/par_time:.1f}x")
    print(f"Fetched {len(results)} posts")

asyncio.run(main())"""},
{"label": "Bounded concurrency with semaphore", "code":
"""import asyncio
import aiohttp

async def fetch_bounded(session, url, semaphore):
    \"\"\"Fetch with concurrency limit to avoid overwhelming the server.\"\"\"
    async with semaphore:
        async with session.get(url) as resp:
            return await resp.json()

async def main():
    semaphore = asyncio.Semaphore(5)  # max 5 concurrent requests
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 21)]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_bounded(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = [r for r in results if not isinstance(r, Exception)]
    errors = [r for r in results if isinstance(r, Exception)]
    print(f"Success: {len(successes)}, Errors: {len(errors)}")

asyncio.run(main())"""},
{"label": "Async with error handling and timeout", "code":
"""import asyncio
import aiohttp

async def safe_fetch(session, url, timeout=10):
    \"\"\"Async fetch with error handling.\"\"\"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
            if resp.status != 200:
                return {"url": url, "error": f"HTTP {resp.status}"}
            return {"url": url, "data": await resp.json()}
    except asyncio.TimeoutError:
        return {"url": url, "error": "Timeout"}
    except aiohttp.ClientError as e:
        return {"url": url, "error": str(e)}

async def main():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/status/404",
        "https://httpbin.org/delay/1",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [safe_fetch(session, url, timeout=5) for url in urls]
        results = await asyncio.gather(*tasks)

    for r in results:
        status = "OK" if "data" in r else "FAIL"
        detail = r.get("error", "success")
        print(f"  [{status}] {r['url'].split('/')[-1]:>10} → {detail}")

asyncio.run(main())"""},
],
"rw": {
    "todos": [
    "Fetch 10 URLs concurrently with asyncio.gather and compare the time vs sequential requests",
    "Add a Semaphore(5) to limit concurrency and observe how it affects total time",
    "Handle errors in async gather using return_exceptions=True and filter out failed results",
    "Set a per-request timeout using aiohttp.ClientTimeout(total=5) in your async fetch",
    "Print the URL and status code for each response to confirm all requests completed",
],
"title": "Async Bulk Data Fetcher",
    "scenario": "A data pipeline needs to fetch 500 user profiles from an API. Doing this sequentially would take minutes; async with bounded concurrency finishes in seconds.",
    "code":
"""import asyncio
import aiohttp
import time

async def fetch_users(user_ids, concurrency=20):
    semaphore = asyncio.Semaphore(concurrency)
    results = []

    async def fetch_one(session, uid):
        async with semaphore:
            url = f"https://jsonplaceholder.typicode.com/users/{uid}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, uid) for uid in user_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    valid = [r for r in results if r and not isinstance(r, Exception)]
    return valid

start = time.time()
# JSONPlaceholder only has 10 users, but this pattern scales to thousands
users = asyncio.run(fetch_users(list(range(1, 11)) * 5, concurrency=10))
elapsed = time.time() - start

print(f"Fetched {len(users)} user records in {elapsed:.2f}s")
print(f"Sample: {users[0]['name']} ({users[0]['email']})")"""
},
"practice": {
    "title": "Async API Stress Tester",
    "desc": "Build an async function that measures API response times at different concurrency levels (1, 5, 10, 20) and prints a summary table.",
    "starter":
"""import asyncio
import aiohttp
import time

async def stress_test(url, total_requests=20, concurrency=5):
    \"\"\"Measure response times at a given concurrency level.\"\"\"
    semaphore = asyncio.Semaphore(concurrency)
    times = []

    async def timed_fetch(session):
        async with semaphore:
            start = time.time()
            # TODO: make request, record elapsed time
            pass

    async with aiohttp.ClientSession() as session:
        # TODO: create and gather tasks
        pass

    # TODO: return stats (min, max, avg, total)
    return {}

async def main():
    url = "https://httpbin.org/get"
    print(f"Stress testing: {url}")
    print(f"{'Concurrency':>12} {'Avg(ms)':>10} {'Min(ms)':>10} {'Max(ms)':>10} {'Total(s)':>10}")

    for c in [1, 5, 10, 20]:
        stats = await stress_test(url, total_requests=20, concurrency=c)
        # TODO: print formatted results
        pass

asyncio.run(main())"""
}
},

{
"title": "11. Working with REST API Patterns",
"desc": "REST (Representational State Transfer) APIs follow predictable URL patterns for CRUD operations. Understanding these patterns lets you work with any REST API quickly.",
"examples": [
{"label": "Standard REST CRUD pattern", "code":
"""import requests

BASE = "https://jsonplaceholder.typicode.com"

# CREATE — POST /resources
new_post = requests.post(f"{BASE}/posts", json={
    "title": "My Analysis Results",
    "body": "Model accuracy: 94.5%",
    "userId": 1,
}, timeout=10)
print(f"Created: id={new_post.json()['id']}, status={new_post.status_code}")

# READ — GET /resources and GET /resources/:id
all_posts = requests.get(f"{BASE}/posts", params={"_limit": 3}, timeout=10)
print(f"Listed: {len(all_posts.json())} posts")

one_post = requests.get(f"{BASE}/posts/1", timeout=10)
print(f"Single: '{one_post.json()['title'][:40]}...'")

# UPDATE — PUT /resources/:id (full replace)
updated = requests.put(f"{BASE}/posts/1", json={
    "title": "Updated Title",
    "body": "Updated body",
    "userId": 1,
}, timeout=10)
print(f"Updated: {updated.json()['title']}")

# DELETE — DELETE /resources/:id
deleted = requests.delete(f"{BASE}/posts/1", timeout=10)
print(f"Deleted: status={deleted.status_code}")"""},
{"label": "Nested resources and filtering", "code":
"""import requests

BASE = "https://jsonplaceholder.typicode.com"

# Nested resources — GET /resources/:id/sub-resources
# Get all comments for post 1
comments = requests.get(f"{BASE}/posts/1/comments", timeout=10).json()
print(f"Post 1 has {len(comments)} comments")
print(f"First comment by: {comments[0]['email']}")

# Filtering with query parameters
# Get all posts by user 1
user_posts = requests.get(f"{BASE}/posts", params={"userId": 1}, timeout=10).json()
print(f"\\nUser 1 has {len(user_posts)} posts")

# Get all todos that are completed
done = requests.get(f"{BASE}/todos", params={"completed": True, "_limit": 5}, timeout=10).json()
print(f"Completed todos (first 5): {len(done)}")
for t in done[:3]:
    print(f"  - {t['title'][:50]}")"""},
{"label": "Sending form data and file uploads", "code":
"""import requests

# Form-encoded data (like HTML form submission)
resp = requests.post("https://httpbin.org/post",
                     data={"username": "alice", "role": "data_scientist"},
                     timeout=10)
print("Form data received:")
print(f"  {resp.json()['form']}")

# File upload (multipart/form-data)
# In real usage: files={"file": open("data.csv", "rb")}
# Simulated with in-memory bytes:
import io
csv_content = b"name,score\\nAlice,95\\nBob,87"
files = {"file": ("results.csv", io.BytesIO(csv_content), "text/csv")}
resp = requests.post("https://httpbin.org/post", files=files, timeout=10)
print(f"\\nFile upload received: {list(resp.json()['files'].keys())}")"""},
],
"rw": {
    "todos": [
    "Send a POST request with a JSON body to JSONPlaceholder and print the created resource id",
    "Send a GET /resources/:id request and handle a 404 by printing a clear error message",
    "Send a PATCH request to partially update a resource and verify only the changed field updated",
    "Send a DELETE request and confirm the server returned a 200 status code",
    "Use nested resource URLs (e.g., /posts/1/comments) to fetch related records",
],
"title": "CRUD Client for a Data API",
    "scenario": "A data science team manages their experiment metadata through a REST API. They need a clean client to create, read, update, and delete experiment records.",
    "code":
"""import requests

class ExperimentClient:
    \"\"\"REST client for managing ML experiment metadata.\"\"\"

    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        self.base = base_url
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"
        self.session.timeout = 15

    def create(self, title, body, user_id=1):
        resp = self.session.post(f"{self.base}/posts",
                                  json={"title": title, "body": body, "userId": user_id})
        resp.raise_for_status()
        return resp.json()

    def get(self, experiment_id):
        resp = self.session.get(f"{self.base}/posts/{experiment_id}")
        resp.raise_for_status()
        return resp.json()

    def list_all(self, user_id=None, limit=10):
        params = {"_limit": limit}
        if user_id:
            params["userId"] = user_id
        resp = self.session.get(f"{self.base}/posts", params=params)
        resp.raise_for_status()
        return resp.json()

    def update(self, experiment_id, **fields):
        resp = self.session.patch(f"{self.base}/posts/{experiment_id}", json=fields)
        resp.raise_for_status()
        return resp.json()

    def delete(self, experiment_id):
        resp = self.session.delete(f"{self.base}/posts/{experiment_id}")
        resp.raise_for_status()
        return resp.status_code

# Usage
client = ExperimentClient()
exp = client.create("XGBoost v2", "accuracy=0.96, f1=0.94")
print(f"Created experiment: {exp['id']}")
print(f"Read back: {client.get(1)['title'][:40]}")
print(f"User 1 experiments: {len(client.list_all(user_id=1))}")"""
},
},

{
"title": "12. Web Scraping with requests + BeautifulSoup",
"desc": "When there's no API, you can extract data from web pages using requests to fetch HTML and BeautifulSoup to parse it. Install: pip install beautifulsoup4.",
"examples": [
{"label": "Fetching and parsing HTML", "code":
"""import requests
from bs4 import BeautifulSoup

# Fetch a page
resp = requests.get("https://httpbin.org/html", timeout=10)
soup = BeautifulSoup(resp.text, "html.parser")

# Find elements
heading = soup.find("h1")
paragraphs = soup.find_all("p")

print(f"Title: {heading.text if heading else 'No h1'}")
print(f"Paragraphs: {len(paragraphs)}")
for p in paragraphs[:2]:
    print(f"  {p.text[:80]}...")"""},
{"label": "Extracting tables from HTML into DataFrames", "code":
"""import pandas as pd

# pandas.read_html() parses HTML tables directly!
# It uses BeautifulSoup under the hood
html = \"\"\"
<table>
  <thead><tr><th>Name</th><th>Score</th><th>Grade</th></tr></thead>
  <tbody>
    <tr><td>Alice</td><td>95</td><td>A</td></tr>
    <tr><td>Bob</td><td>87</td><td>B+</td></tr>
    <tr><td>Carol</td><td>92</td><td>A-</td></tr>
  </tbody>
</table>
\"\"\"

# Parse HTML string
tables = pd.read_html(html)
df = tables[0]
print(df)
print(f"\\nMean score: {df['Score'].mean():.1f}")"""},
{"label": "CSS selectors for precise extraction", "code":
"""from bs4 import BeautifulSoup

html = \"\"\"
<div class="results">
  <div class="card" data-id="1">
    <h3 class="title">Machine Learning Basics</h3>
    <span class="author">Alice</span>
    <span class="rating">4.8</span>
  </div>
  <div class="card" data-id="2">
    <h3 class="title">Deep Learning with PyTorch</h3>
    <span class="author">Bob</span>
    <span class="rating">4.6</span>
  </div>
</div>
\"\"\"

soup = BeautifulSoup(html, "html.parser")

# CSS selectors
cards = soup.select(".card")
for card in cards:
    title  = card.select_one(".title").text
    author = card.select_one(".author").text
    rating = card.select_one(".rating").text
    data_id = card.get("data-id")
    print(f"  [{data_id}] {title} by {author} ({rating} stars)")"""},
],
"rw": {
    "todos": [
    "Fetch an HTML page with requests and parse it with BeautifulSoup using 'html.parser'",
    "Use soup.select('.classname') to extract all elements with a given CSS class",
    "Use pd.read_html(html_string) to extract an HTML table directly into a DataFrame",
    "Extract data-id attributes from cards using element.get('data-id')",
    "Handle a missing element gracefully using a conditional before calling .text",
],
"title": "Scraping Data Tables for Analysis",
    "scenario": "A research team needs historical data from a website that provides tables but no API. They scrape the table, clean it, and save as CSV.",
    "code":
"""import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table(url, table_index=0, headers=None):
    \"\"\"Scrape an HTML table and return a clean DataFrame.\"\"\"
    resp = requests.get(url, headers=headers or {
        "User-Agent": "Mozilla/5.0 (Research Bot)"
    }, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    tables = soup.find_all("table")

    if not tables:
        print("No tables found!")
        return pd.DataFrame()

    print(f"Found {len(tables)} tables on page")

    # Parse the target table
    rows = []
    table = tables[table_index]
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows[1:], columns=rows[0])
    print(f"Parsed table: {df.shape[0]} rows x {df.shape[1]} columns")
    return df

# Demo with httpbin's HTML (no table, just showing the pattern)
# In practice: df = scrape_table("https://en.wikipedia.org/wiki/...")
print("Pattern: scrape_table(url) → pd.DataFrame")
print("Always respect robots.txt and add delays between requests!")"""
},
"practice": {
    "title": "Build a Web Scraper Pipeline",
    "desc": "Write a scraper that extracts data from an HTML page, handles missing elements gracefully, and converts results to a DataFrame.",
    "starter":
"""import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_and_clean(html_content):
    \"\"\"Parse HTML and extract structured data.\"\"\"
    soup = BeautifulSoup(html_content, "html.parser")
    records = []

    # TODO: Find all cards/items
    # TODO: Extract fields (handle missing elements with .get_text(default="N/A"))
    # TODO: Append dict to records
    # TODO: Convert to DataFrame and clean types

    return pd.DataFrame(records)

# Test HTML
test_html = \"\"\"
<div class="results">
  <div class="item"><h3>Item A</h3><span class="price">$10.99</span></div>
  <div class="item"><h3>Item B</h3><span class="price">$24.50</span></div>
  <div class="item"><h3>Item C</h3></div>
</div>
\"\"\"

df = scrape_and_clean(test_html)
print(df)"""
}
},

{
"title": "13. Building APIs with FastAPI",
"desc": "FastAPI lets you build production-ready APIs in Python. It's fast, generates auto-docs, and uses type hints for validation. Install: pip install fastapi uvicorn.",
"examples": [
{"label": "Minimal FastAPI application", "code":
"""from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ML Prediction API", version="1.0")

# Data model with automatic validation
class PredictionRequest(BaseModel):
    features: list[float]
    model_name: str = "default"

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    model_name: str

@app.get("/")
def root():
    return {"message": "ML Prediction API", "status": "healthy"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    # Simulated prediction
    prediction = sum(req.features) / len(req.features)
    return PredictionResponse(
        prediction=round(prediction, 4),
        confidence=0.95,
        model_name=req.model_name,
    )

# Run with: uvicorn filename:app --reload
# Auto-docs at: http://localhost:8000/docs
print("FastAPI app defined!")
print("Run with: uvicorn script:app --reload")
print("Docs at:  http://localhost:8000/docs")"""},
{"label": "Path parameters, query parameters, and error handling", "code":
"""from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# In-memory "database"
experiments = {
    1: {"id": 1, "name": "Baseline", "accuracy": 0.85},
    2: {"id": 2, "name": "XGBoost v2", "accuracy": 0.92},
}

# Path parameter
@app.get("/experiments/{exp_id}")
def get_experiment(exp_id: int):
    if exp_id not in experiments:
        raise HTTPException(status_code=404, detail=f"Experiment {exp_id} not found")
    return experiments[exp_id]

# Query parameters with validation
@app.get("/experiments")
def list_experiments(
    min_accuracy: float = Query(0.0, ge=0, le=1, description="Minimum accuracy filter"),
    limit: int = Query(10, ge=1, le=100),
):
    filtered = [e for e in experiments.values() if e["accuracy"] >= min_accuracy]
    return filtered[:limit]

# POST with Pydantic validation
class NewExperiment(BaseModel):
    name: str
    accuracy: float
    tags: list[str] = []

@app.post("/experiments", status_code=201)
def create_experiment(exp: NewExperiment):
    new_id = max(experiments.keys()) + 1
    record = {"id": new_id, **exp.model_dump()}
    experiments[new_id] = record
    return record

print("Endpoints defined: GET /experiments, GET /experiments/{id}, POST /experiments")"""},
{"label": "Serving an ML model via API", "code":
"""from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Iris Classifier API")

# Simulated trained model (in production, load from file)
class SimpleModel:
    def predict(self, features):
        # Dummy classifier based on petal length
        x = np.array(features)
        if x[2] < 2.5:
            return 0, 0.95  # setosa
        elif x[2] < 4.8:
            return 1, 0.82  # versicolor
        else:
            return 2, 0.78  # virginica

model = SimpleModel()
CLASS_NAMES = ["setosa", "versicolor", "virginica"]

class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class IrisResponse(BaseModel):
    prediction: str
    class_id: int
    confidence: float

@app.post("/classify", response_model=IrisResponse)
def classify_iris(flower: IrisRequest):
    features = [flower.sepal_length, flower.sepal_width,
                flower.petal_length, flower.petal_width]
    class_id, confidence = model.predict(features)
    return IrisResponse(
        prediction=CLASS_NAMES[class_id],
        class_id=class_id,
        confidence=confidence,
    )

# Test locally
req = IrisRequest(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)
result = classify_iris(req)
print(f"Prediction: {result.prediction} (confidence: {result.confidence})")"""},
],
"rw": {
    "todos": [
    "Define a Pydantic BaseModel with 3 fields and test that it rejects invalid input",
    "Add a GET /health endpoint to your FastAPI app and call it with requests.get",
    "Create a POST endpoint that accepts a JSON body, runs a calculation, and returns a result",
    "Add a path parameter (e.g., /items/{item_id}) and raise HTTPException on missing items",
    "Serve a simple model prediction via a POST /predict endpoint using a dummy model",
],
"title": "Full ML Prediction Service",
    "scenario": "A team deploys their trained model as a FastAPI service with input validation, prediction logging, batch endpoints, and health checks.",
    "code":
"""from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from datetime import datetime
import numpy as np

app = FastAPI(title="Churn Prediction Service", version="2.0")

# Prediction log (in production → database)
prediction_log = []

class CustomerFeatures(BaseModel):
    tenure_months: int
    monthly_charges: float
    total_charges: float
    num_support_tickets: int
    contract_type: str  # "month-to-month", "one-year", "two-year"

    @field_validator("contract_type")
    @classmethod
    def valid_contract(cls, v):
        allowed = ["month-to-month", "one-year", "two-year"]
        if v not in allowed:
            raise ValueError(f"Must be one of {allowed}")
        return v

class BatchRequest(BaseModel):
    customers: list[CustomerFeatures]

@app.post("/predict")
def predict_churn(customer: CustomerFeatures):
    # Simulated model
    risk_score = (
        (1 - customer.tenure_months / 72) * 0.3
        + (customer.monthly_charges / 120) * 0.3
        + (customer.num_support_tickets / 10) * 0.2
        + (1 if customer.contract_type == "month-to-month" else 0) * 0.2
    )
    risk_score = max(0, min(1, risk_score))

    result = {
        "churn_probability": round(risk_score, 4),
        "risk_level": "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low",
        "timestamp": datetime.now().isoformat(),
    }
    prediction_log.append(result)
    return result

@app.post("/predict/batch")
def predict_batch(batch: BatchRequest):
    return [predict_churn(c) for c in batch.customers]

# Test
sample = CustomerFeatures(
    tenure_months=6, monthly_charges=89.99, total_charges=539.94,
    num_support_tickets=4, contract_type="month-to-month"
)
print(predict_churn(sample))"""
},
},

{
"title": "14. Testing API Calls with unittest.mock",
"desc": "Never hit real APIs in unit tests — they're slow, flaky, and may cost money. Use mocking to simulate API responses and test your code's logic in isolation.",
"examples": [
{"label": "Mocking requests.get with unittest.mock", "code":
"""from unittest.mock import patch, MagicMock
import requests

def get_user_name(user_id):
    \"\"\"Fetch user name from API.\"\"\"
    resp = requests.get(f"https://api.example.com/users/{user_id}", timeout=10)
    resp.raise_for_status()
    return resp.json()["name"]

# Mock the API call
with patch("requests.get") as mock_get:
    # Configure the mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Alice"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Call the function — it uses our mock, not the real API
    name = get_user_name(1)
    print(f"Got name: {name}")

    # Verify the right URL was called
    mock_get.assert_called_once_with("https://api.example.com/users/1", timeout=10)
    print("Mock verified: correct URL called")"""},
{"label": "Testing error handling with mocks", "code":
"""from unittest.mock import patch, MagicMock
import requests

def safe_fetch(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return {"ok": True, "data": resp.json()}
    except requests.HTTPError:
        return {"ok": False, "error": "HTTP error"}
    except requests.Timeout:
        return {"ok": False, "error": "Timeout"}
    except requests.ConnectionError:
        return {"ok": False, "error": "Connection failed"}

# Test success
with patch("requests.get") as mock:
    mock.return_value = MagicMock(status_code=200, json=lambda: {"key": "value"})
    mock.return_value.raise_for_status = MagicMock()
    result = safe_fetch("https://api.example.com/data")
    print(f"Success test: {result}")

# Test timeout
with patch("requests.get") as mock:
    mock.side_effect = requests.Timeout("Connection timed out")
    result = safe_fetch("https://api.example.com/data")
    print(f"Timeout test: {result}")

# Test HTTP error
with patch("requests.get") as mock:
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = requests.HTTPError("404")
    mock.return_value = mock_resp
    result = safe_fetch("https://api.example.com/data")
    print(f"HTTP error test: {result}")"""},
{"label": "Using responses library for cleaner mocking", "code":
"""# pip install responses
# The 'responses' library provides a cleaner API for mocking requests

# Here's the pattern (requires: pip install responses)
\"\"\"
import responses
import requests

@responses.activate
def test_user_fetch():
    # Register a mock response
    responses.add(
        responses.GET,
        "https://api.example.com/users/1",
        json={"id": 1, "name": "Alice"},
        status=200,
    )

    # Now requests.get hits the mock
    resp = requests.get("https://api.example.com/users/1")
    assert resp.json()["name"] == "Alice"
    assert len(responses.calls) == 1

test_user_fetch()
\"\"\"

# Without installing responses, here's a reusable mock context manager:
from unittest.mock import patch, MagicMock
from contextlib import contextmanager

@contextmanager
def mock_api_response(url, json_data, status=200):
    with patch("requests.get") as mock:
        resp = MagicMock()
        resp.status_code = status
        resp.json.return_value = json_data
        resp.raise_for_status = MagicMock()
        if status >= 400:
            resp.raise_for_status.side_effect = Exception(f"HTTP {status}")
        mock.return_value = resp
        yield mock

# Usage
import requests
with mock_api_response("https://api.example.com/data", {"result": 42}):
    resp = requests.get("https://api.example.com/data")
    print(f"Mocked response: {resp.json()}")"""},
],
"rw": {
    "todos": [
    "Use patch('requests.get') to mock an API call and verify your function uses the mocked data",
    "Configure a mock response to raise requests.Timeout and confirm your code handles it",
    "Use mock_get.assert_called_once_with to verify the correct URL was called",
    "Test an HTTP error (404) by setting raise_for_status.side_effect to requests.HTTPError",
    "Write a test that verifies your transformation logic produces the correct output from mocked data",
],
"title": "Testing a Data Pipeline's API Layer",
    "scenario": "A data pipeline fetches from an external API, transforms the data, and saves it. Tests mock the API layer to verify transformation logic without network calls.",
    "code":
"""from unittest.mock import patch, MagicMock

# The pipeline code
class DataPipeline:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_and_transform(self):
        import requests
        resp = requests.get(self.api_url, timeout=10)
        resp.raise_for_status()
        raw = resp.json()

        # Transform: extract, clean, aggregate
        records = raw.get("data", [])
        return {
            "count": len(records),
            "names": [r["name"].strip().title() for r in records],
            "total_value": sum(r.get("value", 0) for r in records),
        }

# Test the transformation logic without hitting the API
with patch("requests.get") as mock_get:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "data": [
            {"name": " alice ", "value": 100},
            {"name": "BOB", "value": 250},
            {"name": "  carol  ", "value": 175},
        ]
    }
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    pipeline = DataPipeline("https://api.example.com/records")
    result = pipeline.fetch_and_transform()

    assert result["count"] == 3
    assert result["names"] == ["Alice", "Bob", "Carol"]
    assert result["total_value"] == 525
    print(f"All assertions passed!")
    print(f"Result: {result}")"""
},
},

{
"title": "15. Public APIs for Data Science Projects",
"desc": "A curated list of free APIs perfect for data science practice — no API key required for most. These are great for portfolio projects and learning.",
"examples": [
{"label": "JSONPlaceholder — fake REST API for testing", "code":
"""import requests
import pandas as pd

# https://jsonplaceholder.typicode.com
# Fake data for: posts, comments, albums, photos, todos, users

# Fetch all users and their post counts
users = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10).json()
posts = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10).json()

df_users = pd.DataFrame(users)[["id", "name", "email"]]
df_posts = pd.DataFrame(posts)
post_counts = df_posts.groupby("userId").size().reset_index(name="num_posts")

result = df_users.merge(post_counts, left_on="id", right_on="userId")
print(result[["name", "email", "num_posts"]].to_string(index=False))"""},
{"label": "Open-Meteo — free weather API (no key needed)", "code":
"""import requests
import pandas as pd

# https://open-meteo.com — free weather data
resp = requests.get("https://api.open-meteo.com/v1/forecast", params={
    "latitude": 40.71,
    "longitude": -74.01,
    "hourly": "temperature_2m,precipitation",
    "timezone": "America/New_York",
    "forecast_days": 3,
}, timeout=10)

data = resp.json()
df = pd.DataFrame({
    "time": pd.to_datetime(data["hourly"]["time"]),
    "temp_c": data["hourly"]["temperature_2m"],
    "precip_mm": data["hourly"]["precipitation"],
})
print(df.head(10))
print(f"\\nAvg temp: {df['temp_c'].mean():.1f}°C")
print(f"Max precip: {df['precip_mm'].max():.1f}mm")"""},
{"label": "REST Countries, Universities, and more", "code":
"""import requests
import pandas as pd

# REST Countries — country data
countries = requests.get("https://restcountries.com/v3.1/region/europe",
                          params={"fields": "name,population,area,capital"},
                          timeout=10).json()
df = pd.DataFrame([{
    "name": c["name"]["common"],
    "population": c.get("population", 0),
    "area_km2": c.get("area", 0),
    "capital": c.get("capital", ["N/A"])[0] if c.get("capital") else "N/A",
} for c in countries])
df["density"] = (df["population"] / df["area_km2"]).round(1)
print("Top 5 European countries by population density:")
print(df.nlargest(5, "density")[["name", "population", "density"]].to_string(index=False))

# Universities API
unis = requests.get("http://universities.hipolabs.com/search",
                     params={"country": "United States", "name": "MIT"},
                     timeout=10).json()
print(f"\\nMIT results: {len(unis)}")
for u in unis[:3]:
    print(f"  {u['name']} — {u.get('web_pages', ['N/A'])[0]}")"""},
],
"rw": {
    "todos": [
    "Fetch users and posts from JSONPlaceholder, merge them, and count posts per user",
    "Query Open-Meteo for 3-day forecast of your city and print the daily max temperatures",
    "Use the REST Countries API to fetch all European countries and sort by population density",
    "Build a DataFrame combining weather data for 3 cities and identify the warmest one",
    "Fetch data from 2 different free APIs and join the results on a common field",
],
"title": "Multi-API Dashboard Dataset",
    "scenario": "Build a dataset combining weather, country, and economic data from multiple free APIs for a Streamlit dashboard project.",
    "code":
"""import requests
import pandas as pd

def build_city_dataset():
    \"\"\"Combine data from multiple APIs into one analytical dataset.\"\"\"
    cities = [
        {"name": "New York",  "lat": 40.71, "lon": -74.01, "country": "US"},
        {"name": "London",    "lat": 51.51, "lon": -0.13,  "country": "GB"},
        {"name": "Tokyo",     "lat": 35.68, "lon": 139.69, "country": "JP"},
        {"name": "Sydney",    "lat": -33.87,"lon": 151.21, "country": "AU"},
        {"name": "Sao Paulo", "lat": -23.55,"lon": -46.63, "country": "BR"},
    ]

    rows = []
    for city in cities:
        # Weather data
        weather = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": city["lat"], "longitude": city["lon"],
            "current_weather": True,
        }, timeout=10).json()

        current = weather.get("current_weather", {})
        rows.append({
            "city": city["name"],
            "country": city["country"],
            "temp_c": current.get("temperature"),
            "wind_kmh": current.get("windspeed"),
            "lat": city["lat"],
            "lon": city["lon"],
        })

    return pd.DataFrame(rows)

df = build_city_dataset()
print(df.to_string(index=False))
print(f"\\nWarmest: {df.loc[df['temp_c'].idxmax(), 'city']}")
print(f"Windiest: {df.loc[df['wind_kmh'].idxmax(), 'city']}")"""
},
},

{
"title": "16. Data Collection Project — End-to-End Pipeline",
"desc": "Putting it all together: a complete data collection pipeline that fetches from APIs, handles errors, paginates, caches results, transforms data, and exports to multiple formats.",
"examples": [
{"label": "Complete pipeline architecture", "code":
"""import requests
import pandas as pd
import json
import time
from pathlib import Path
from datetime import datetime

class DataPipeline:
    \"\"\"End-to-end API data collection pipeline.\"\"\"

    def __init__(self, name, cache_dir="cache"):
        self.name = name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers["User-Agent"] = f"DataPipeline-{name}/1.0"
        self.stats = {"requests": 0, "cached": 0, "errors": 0}

    def fetch(self, url, params=None, cache_key=None, ttl=3600):
        \"\"\"Fetch with caching support.\"\"\"
        # Check cache
        if cache_key:
            cache_file = self.cache_dir / f"{cache_key}.json"
            if cache_file.exists():
                age = time.time() - cache_file.stat().st_mtime
                if age < ttl:
                    self.stats["cached"] += 1
                    return json.loads(cache_file.read_text())

        # Fetch from API
        resp = self.session.get(url, params=params, timeout=15)
        resp.raise_for_status()
        self.stats["requests"] += 1
        data = resp.json()

        # Save to cache
        if cache_key:
            cache_file.write_text(json.dumps(data))

        return data

    def fetch_paginated(self, url, per_page=100, max_pages=10):
        \"\"\"Fetch all pages from a paginated API.\"\"\"
        all_items = []
        for page in range(1, max_pages + 1):
            data = self.fetch(url, params={"_page": page, "_limit": per_page},
                            cache_key=f"{self.name}_page{page}")
            if not data:
                break
            all_items.extend(data)
        return all_items

    def summary(self):
        print(f"Pipeline '{self.name}': {self.stats}")

# Usage
pipeline = DataPipeline("demo")
data = pipeline.fetch("https://jsonplaceholder.typicode.com/users", cache_key="users")
print(f"Fetched {len(data)} users")
pipeline.summary()

# Cleanup
import shutil
shutil.rmtree("cache", ignore_errors=True)"""},
{"label": "Transform and export", "code":
"""import requests
import pandas as pd
from pathlib import Path

def collect_and_export():
    \"\"\"Full pipeline: collect → transform → export.\"\"\"

    # 1. COLLECT
    print("1. Collecting data...")
    users = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10).json()
    posts = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10).json()
    comments = requests.get("https://jsonplaceholder.typicode.com/comments",
                            params={"_limit": 100}, timeout=10).json()

    # 2. TRANSFORM
    print("2. Transforming...")
    df_users = pd.DataFrame(users)[["id", "name", "email", "company"]]
    df_users["company_name"] = df_users["company"].apply(lambda c: c["name"])
    df_users = df_users.drop(columns=["company"])

    df_posts = pd.DataFrame(posts)[["id", "userId", "title", "body"]]
    df_posts["title_length"] = df_posts["title"].str.len()
    df_posts["body_length"] = df_posts["body"].str.len()

    df_comments = pd.DataFrame(comments)[["postId", "email", "body"]]

    # 3. ANALYZE
    print("3. Analyzing...")
    user_stats = (
        df_posts.groupby("userId")
        .agg(num_posts=("id", "count"),
             avg_title_len=("title_length", "mean"),
             avg_body_len=("body_length", "mean"))
        .round(1)
    )

    result = df_users.merge(user_stats, left_on="id", right_index=True)
    print(result[["name", "company_name", "num_posts", "avg_body_len"]].to_string(index=False))

    # 4. EXPORT
    print("\\n4. Export formats available:")
    print("   result.to_csv('user_analytics.csv')")
    print("   result.to_parquet('user_analytics.parquet')")
    print("   result.to_json('user_analytics.json', orient='records')")

    return result

df = collect_and_export()"""},
],
"rw": {
    "todos": [
    "Build a pipeline that fetches, transforms, and exports data to CSV in a single run function",
    "Add a data quality check that flags rows with null values or out-of-range numbers",
    "Implement a file-based cache so the pipeline skips fetching if fresh data already exists",
    "Add error handling so one failing source does not abort the entire pipeline",
    "Print a final summary report showing records fetched, errors, and time elapsed per source",
],
"title": "Production-Grade Data Collection Service",
    "scenario": "A data engineering team builds a scheduled data collection service that pulls from multiple APIs nightly, validates data quality, and alerts on issues.",
    "code":
"""import requests
import pandas as pd
from datetime import datetime

class ProductionCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.errors = []
        self.metrics = {}

    def collect_source(self, name, url, params=None, validator=None):
        \"\"\"Collect from a single source with validation.\"\"\"
        start = datetime.now()
        try:
            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

            # Validate
            if validator:
                issues = validator(data)
                if issues:
                    self.errors.append({"source": name, "issues": issues})

            elapsed = (datetime.now() - start).total_seconds()
            self.metrics[name] = {
                "records": len(data) if isinstance(data, list) else 1,
                "time_s": elapsed,
                "status": "ok",
            }
            return data

        except Exception as e:
            self.errors.append({"source": name, "error": str(e)})
            self.metrics[name] = {"records": 0, "status": "failed"}
            return None

    def report(self):
        print(f"\\n{'='*50}")
        print(f"Collection Report — {datetime.now():%Y-%m-%d %H:%M}")
        print(f"{'='*50}")
        for name, m in self.metrics.items():
            print(f"  {name:15s} | {m['records']:>5} records | {m.get('time_s',0):.2f}s | {m['status']}")
        if self.errors:
            print(f"\\nErrors ({len(self.errors)}):")
            for e in self.errors:
                print(f"  - {e}")

# Run collection
collector = ProductionCollector()

# Source 1: Users
users = collector.collect_source(
    "users",
    "https://jsonplaceholder.typicode.com/users",
    validator=lambda d: [] if len(d) > 0 else ["No users returned"],
)

# Source 2: Posts
posts = collector.collect_source(
    "posts",
    "https://jsonplaceholder.typicode.com/posts",
    params={"_limit": 50},
)

# Source 3: Intentionally broken
collector.collect_source("broken", "https://httpbin.org/status/500")

collector.report()"""
},
"practice": {
    "title": "Build Your Own Data Collection Pipeline",
    "desc": "Create a complete pipeline that: (1) fetches data from 2+ free APIs, (2) merges them into a single DataFrame, (3) adds derived columns, (4) handles errors gracefully, and (5) prints a quality report.",
    "starter":
"""import requests
import pandas as pd

class MyPipeline:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 15

    def collect(self):
        # TODO: Fetch from at least 2 APIs
        # Suggestions:
        #   - JSONPlaceholder (users + posts)
        #   - Open-Meteo (weather for multiple cities)
        #   - REST Countries + Universities
        pass

    def transform(self, raw_data):
        # TODO: Clean, merge, and add derived columns
        pass

    def quality_check(self, df):
        # TODO: Check for nulls, duplicates, expected row counts
        pass

    def run(self):
        print("Starting pipeline...")
        raw = self.collect()
        df = self.transform(raw)
        self.quality_check(df)
        print(f"\\nFinal dataset: {df.shape}")
        print(df.head())
        return df

pipeline = MyPipeline()
result = pipeline.run()"""
}
},

{
"title": "Practice Lab: Requests & FastAPI",
"desc": "Hands-on REST patterns. These depend on the network and web frameworks, so run them in a local Python environment (the in-page runner has no network). Read, copy, and adapt them.",
"examples": [
    {"label": "GET with params, timeout & error handling", "code": '''import requests

def fetch_repo(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        r = requests.get(url, params={"per_page": 1}, timeout=5)
        r.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e)}
    data = r.json()
    return {"name": data["full_name"], "stars": data["stargazers_count"]}

print(fetch_repo("python", "cpython"))'''},
    {"label": "Minimal FastAPI endpoint", "code": '''from fastapi import FastAPI, HTTPException

app = FastAPI()
ITEMS = {1: "apple", 2: "banana"}

@app.get("/items/{item_id}")
def read_item(item_id: int, upper: bool = False):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="item not found")
    name = ITEMS[item_id]
    return {"id": item_id, "name": name.upper() if upper else name}

# Run with:  uvicorn app:app --reload'''},
],
"todos": [
    "Send a GET request with query params, a timeout, and raise_for_status()",
    "Handle requests.RequestException and return a clean error dict",
    "Define a FastAPI path parameter (item_id: int) and a query parameter (upper: bool)",
    "Return a 404 with HTTPException when a resource is missing",
],
"practice": {
    "title": "Resilient API Client",
    "desc": "Write get_json(url, params=None, retries=3) that performs a GET with a 5s timeout, retries on failure with a short backoff, raises for HTTP errors, and returns parsed JSON (or None after exhausting retries). Run it locally against a real endpoint.",
    "starter": '''import requests, time

def get_json(url, params=None, retries=3):
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            # TODO: back off (e.g. time.sleep(2 ** attempt)) and retry; return None if out of attempts
            pass
    return None

print(get_json("https://api.github.com/repos/python/cpython"))'''
}
},

{
"title": "Challenge: Authenticated POST",
"desc": "Sending JSON with an auth header is the core of writing to an API. Run this in a local Python environment (the in-page runner has no network).",
"examples": [
    {"label": "POST JSON with a bearer token", "code": '''import requests, os

def create_item(name, token):
    r = requests.post(
        "https://httpbin.org/post",
        json={"name": name},
        headers={"Authorization": f"Bearer {token}"},
        timeout=5,
    )
    r.raise_for_status()
    return r.json()["json"]

print(create_item("widget", os.environ.get("API_TOKEN", "demo")))'''},
],
"todos": [
    "POST a JSON body with the json= argument (requests sets the content-type)",
    "Send an Authorization: Bearer <token> header",
    "Raise on error with raise_for_status()",
],
"practice": {
    "title": "Authenticated POST",
    "desc": "Write post_json(url, payload, token) that POSTs `payload` as JSON with a bearer token, a 5s timeout, raises for HTTP errors, and returns the parsed response. Run it locally.",
    "starter": '''import requests

def post_json(url, payload, token):
    # TODO: requests.post with json=payload, an Authorization bearer header,
    #       a timeout, raise_for_status(), then return r.json()
    pass

print(post_json("https://httpbin.org/post", {"name": "widget"}, "demo"))'''
}
},

{
"title": "Challenge: Pagination",
"desc": "APIs return data in pages; collecting all of it means looping until a page is empty or there is no next link. Run locally.",
"examples": [
    {"label": "Follow page numbers", "code": '''import requests

def fetch_all(base_url, per_page=100):
    items, page = [], 1
    while True:
        r = requests.get(base_url, params={"page": page, "per_page": per_page}, timeout=5)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        page += 1
    return items

# items = fetch_all("https://api.github.com/repos/python/cpython/issues")'''},
],
"todos": [
    "Loop incrementing the page number until a page comes back empty",
    "Accumulate items across pages into one list",
    "Pass a sensible per_page to reduce the number of requests",
],
"practice": {
    "title": "Fetch All Pages",
    "desc": "Write fetch_all(base_url, per_page=100) that pages through a list endpoint (page=1, 2, ...) until an empty page, accumulating and returning every item. Run it locally against a real paginated API.",
    "starter": '''import requests

def fetch_all(base_url, per_page=100):
    items, page = [], 1
    while True:
        r = requests.get(base_url, params={"page": page, "per_page": per_page}, timeout=5)
        r.raise_for_status()
        batch = r.json()
        # TODO: stop when batch is empty; otherwise extend items and go to the next page
        break
    return items

print(len(fetch_all("https://api.github.com/repos/python/cpython/labels")))'''
}
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
