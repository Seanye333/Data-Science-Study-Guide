#!/usr/bin/env python3
"""Generate Time Series Analysis study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE   = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\12_time_series")
BASE.mkdir(parents=True, exist_ok=True)
ACCENT = "#fb923c"
EMOJI  = "📈"
TITLE  = "Time Series Analysis"

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
        rw_scenario = s.get("rw_scenario", "")
        rw_code = s.get("rw_code", "")
        rw_html = ""
        if rw_scenario:
            rwid = f"rw{i}"
            rw_html = (f'<div class="rw"><div class="rh">&#x1F4BC; Real-World Scenario</div>'
                       f'<div class="rd">{esc(rw_scenario)}</div>'
                       f'<div class="code-block"><div class="ch"><span>Real-World Code</span>'
                       f'<button onclick="cp(\'{rwid}\')">Copy</button></div>'
                       f'<pre><code id="{rwid}" class="language-python">{esc(rw_code)}</code></pre></div></div>')
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
    cells.append(md(f"# {TITLE} Study Guide\n\nHands-on time series guide using pandas, numpy, matplotlib, and statsmodels."))
    for i,s in enumerate(sections,1):
        cells.append(md(f"## {i}. {s['title']}\n\n{s.get('desc','')}"))
        for ex in s.get("examples",[]):
            if ex.get("label"): cells.append(md(f"**{ex['label']}**"))
            cells.append(code(ex["code"]))
        rw_scenario = s.get("rw_scenario","")
        rw_code = s.get("rw_code","")
        if rw_scenario:
            cells.append(md(f"### Real-World Scenario\n\n> {rw_scenario}"))
            cells.append(code(rw_code))
        practice = s.get("practice")
        if practice:
            cells.append(md(f"### Practice: {practice['title']}\n\n{practice['desc']}"))
            cells.append(code(practice["starter"]))
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.11.0"}},"nbformat":4,"nbformat_minor":5}


# ─── Content ──────────────────────────────────────────────────────────────────
SECTIONS = [

{
"title": "1. DateTime Indexing",
"desc": "Pandas DatetimeIndex enables powerful time-based selection, alignment, and operations. Use pd.to_datetime() to parse dates and set_index() to create a time series.",
"examples": [
{"label": "Creating a DatetimeIndex", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
dates = pd.date_range('2024-01-01', periods=10, freq='D')
s = pd.Series(rng.integers(100, 500, 10), index=dates)
print(s)
print('\\nIndex type:', type(s.index))
print('Freq:', s.index.freq)
print('First date:', s.index[0])
print('Last date:', s.index[-1])"""},
{"label": "Parsing and indexing with pd.to_datetime", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(7)
df = pd.DataFrame({
    'date':    ['2024-01-15', '2024-02-20', '2024-03-05', '2024-04-10'],
    'revenue': rng.integers(1000, 9999, 4),
    'units':   rng.integers(10, 200, 4),
})
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
print(df)
print('\\n.dt accessor on a column:')
df2 = df.reset_index()
df2['year']  = df2['date'].dt.year
df2['month'] = df2['date'].dt.month
df2['dow']   = df2['date'].dt.day_name()
print(df2[['date','year','month','dow']])"""},
{"label": "Time-based slicing and selection", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(0)
idx = pd.date_range('2023-01-01', '2024-12-31', freq='D')
ts = pd.Series(rng.normal(100, 15, len(idx)), index=idx)

# Slice by string
print('Jan 2024:', ts['2024-01'].shape)
print('Q1 2024:', ts['2024-01':'2024-03'].shape)
print('A specific week:', ts['2024-06-10':'2024-06-16'].values.round(2))

# Boolean mask
print('\\nDays with value > 130:', (ts > 130).sum())
print('Weekend values mean:', ts[ts.index.dayofweek >= 5].mean().round(2))"""},
{"label": "Time zones and date arithmetic", "code":
"""import pandas as pd
import numpy as np

# Create UTC series and convert timezone
idx = pd.date_range('2024-01-01 00:00', periods=6, freq='6h', tz='UTC')
ts = pd.Series(range(6), index=idx)
print('UTC:')
print(ts)

# Convert to US/Eastern
ts_eastern = ts.tz_convert('US/Eastern')
print('\\nUS/Eastern:')
print(ts_eastern)

# Date arithmetic
today = pd.Timestamp('2024-06-15')
print('\\n30 days later:', today + pd.Timedelta(days=30))
print('Next Monday:', today + pd.offsets.Week(weekday=0))
print('End of month:', today + pd.offsets.MonthEnd(0))

# Period vs Timestamp
period = pd.Period('2024-Q2', freq='Q')
print('\\nQ2 2024 start:', period.start_time)
print('Q2 2024 end:  ', period.end_time)"""},
],
"rw_scenario": "An e-commerce analyst needs to parse mixed-format sales timestamps, localize to UTC, and create a clean DatetimeIndex for downstream aggregation.",
"rw_code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
raw = pd.DataFrame({
    'timestamp': ['2024-01-15 09:32', '2024/02/20 14:05', 'March 5, 2024 11:00', '2024-04-10T08:45:00'],
    'store':     ['NYC', 'LA', 'CHI', 'HOU'],
    'amount':    rng.uniform(50, 500, 4).round(2),
})

# Parse mixed formats
raw['ts_parsed'] = pd.to_datetime(raw['timestamp'], infer_datetime_format=True)
raw = raw.set_index('ts_parsed').sort_index()
raw.index = raw.index.tz_localize('US/Eastern').tz_convert('UTC')

print('Cleaned time series:')
print(raw[['store', 'amount']])
print('\\nIndex timezone:', raw.index.tz)
print('Date range:', raw.index[0], 'to', raw.index[-1])""",
"practice": {
"title": "Custom DatetimeIndex",
"desc": "Create a DatetimeIndex for every Monday in 2024. Build a Series with random weekly sales (uniform 1000-5000). Print the total sales per quarter using .resample('QE').sum().",
"starter":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(0)
# TODO: create weekly DatetimeIndex (Mondays only) for 2024
# Hint: pd.date_range(..., freq='W-MON')

# TODO: create Series with random sales

# TODO: resample to quarterly and print
"""},
},

{
"title": "2. Resampling & Frequency Conversion",
"desc": "Resampling changes the time frequency of a series — downsampling aggregates to lower frequency, upsampling interpolates to higher frequency.",
"examples": [
{"label": "Downsampling with resample()", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=365, freq='D')
daily = pd.Series(rng.uniform(100, 500, 365), index=idx, name='sales')

# Downsample to different frequencies
print('Weekly sum (first 4):')
print(daily.resample('W').sum().head(4).round(2))

print('\\nMonthly stats:')
monthly = daily.resample('ME').agg(['sum','mean','max','min'])
print(monthly.round(2))

print('\\nQuarterly mean:')
print(daily.resample('QE').mean().round(2))"""},
{"label": "OHLC resampling for financial data", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(0)
idx = pd.date_range('2024-01-01', periods=365, freq='D')
price = 100 + np.cumsum(rng.normal(0, 1.5, 365))
ts = pd.Series(price, index=idx, name='price')

# OHLC aggregation
weekly_ohlc = ts.resample('W').ohlc()
print('Weekly OHLC (first 5):')
print(weekly_ohlc.head().round(2))

# Custom aggregation
monthly_custom = ts.resample('ME').agg(
    open  = ('first'),
    close = ('last'),
    high  = ('max'),
    low   = ('min'),
    range = (lambda x: x.max() - x.min()),
)
print('\\nMonthly custom agg:')
print(monthly_custom.round(2))"""},
{"label": "Upsampling and interpolation", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(7)
# Monthly data → daily via upsampling
monthly_idx = pd.date_range('2024-01-01', periods=6, freq='ME')
monthly = pd.Series([120, 135, 128, 142, 156, 149], index=monthly_idx, name='revenue')

# Forward fill
daily_ffill = monthly.resample('D').ffill()
# Linear interpolation
daily_interp = monthly.resample('D').interpolate('linear')
# Cubic interpolation
daily_cubic = monthly.resample('D').interpolate('cubic')

print('Monthly original:')
print(monthly)
print('\\nDaily (first 10, forward fill):')
print(daily_ffill.head(10).round(2))
print('\\nDaily (first 10, linear interp):')
print(daily_interp.head(10).round(2))"""},
{"label": "asfreq() vs resample() and timezone-aware resampling", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=24*7, freq='h', tz='UTC')
hourly = pd.Series(rng.uniform(10, 100, len(idx)), index=idx)

# asfreq — select existing values at new frequency (no aggregation)
every_6h = hourly.asfreq('6h')
print('asfreq every 6h (first 8):')
print(every_6h.head(8).round(2))

# Resample by time-of-day
hourly_mean = hourly.groupby(hourly.index.hour).mean()
print('\\nMean by hour of day:')
for h, v in hourly_mean.items():
    bar = '█' * int(v / 10)
    print(f'  {h:02d}h: {v:5.1f} {bar}')"""},
],
"rw_scenario": "A retail analyst has daily transaction data for 3 years and needs to compute weekly, monthly, and quarterly revenue summaries with growth rates for an executive report.",
"rw_code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2022-01-01', '2024-12-31', freq='D')
noise = rng.normal(0, 20, len(idx))
trend = np.linspace(500, 800, len(idx))
seasonal = 80 * np.sin(2 * np.pi * np.arange(len(idx)) / 365)
daily = pd.Series(trend + seasonal + noise, index=idx, name='revenue').clip(0)

# Aggregate
weekly  = daily.resample('W').sum()
monthly = daily.resample('ME').sum()
quarterly = daily.resample('QE').sum()

# Growth rates
monthly_growth = monthly.pct_change() * 100
quarterly_growth = quarterly.pct_change() * 100

print('Monthly revenue with MoM growth (last 6):')
report = pd.DataFrame({'revenue': monthly, 'mom_growth_%': monthly_growth}).tail(6)
print(report.round(2))
print('\\nQuarterly totals with QoQ growth:')
print(pd.DataFrame({'revenue': quarterly, 'qoq_%': quarterly_growth}).round(2))""",
"practice": {
"title": "Resample and Compare",
"desc": "Generate hourly temperature data for January 2024 (mean=5°C, std=8°C, with a sine wave daily cycle). Resample to daily min/mean/max. Find the coldest and warmest day.",
"starter":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', '2024-01-31 23:00', freq='h')
# TODO: create hourly temp with sine daily cycle + noise

# TODO: resample to daily min/mean/max

# TODO: print coldest and warmest day
"""},
},

{
"title": "3. Rolling & Expanding Windows",
"desc": "Rolling windows compute statistics over a sliding fixed-length window. Expanding windows grow from the start of the series. Both are essential for smoothing and feature engineering.",
"examples": [
{"label": "Rolling mean and standard deviation", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=30, freq='D')
ts = pd.Series(rng.normal(100, 15, 30), index=idx, name='value')

rm7  = ts.rolling(7).mean()
rm14 = ts.rolling(14).mean()
std7 = ts.rolling(7).std()

result = pd.DataFrame({'raw': ts, 'ma7': rm7, 'ma14': rm14, 'std7': std7})
print(result.tail(10).round(2))
print('\\nNaN count from rolling(7):', rm7.isna().sum())"""},
{"label": "Rolling min_periods and center", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(0)
ts = pd.Series(rng.normal(50, 10, 20), name='signal')

# min_periods: require at least 3 valid values
r_minp = ts.rolling(7, min_periods=3).mean()
# center=True: window centered on current observation
r_center = ts.rolling(7, center=True).mean()

print('Standard rolling(7): first 7 values')
print(ts.rolling(7).mean().head(7).round(2).tolist())
print('\\nWith min_periods=3: first 7 values')
print(r_minp.head(7).round(2).tolist())
print('\\nCentered rolling(7): first 7 values')
print(r_center.head(7).round(2).tolist())

# Rolling correlation between two series
s2 = pd.Series(rng.normal(50, 10, 20))
print('\\nRolling correlation (last 5):')
print(ts.rolling(5).corr(s2).tail().round(3).tolist())"""},
{"label": "Expanding windows and cumulative stats", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(7)
ts = pd.Series(rng.exponential(100, 20), name='revenue')

exp_mean = ts.expanding().mean()
exp_std  = ts.expanding().std()
exp_max  = ts.expanding().max()
cumsum   = ts.cumsum()

result = pd.DataFrame({
    'revenue':    ts.round(2),
    'cum_mean':   exp_mean.round(2),
    'cum_std':    exp_std.round(2),
    'cum_max':    exp_max.round(2),
    'cumsum':     cumsum.round(2),
})
print(result)"""},
{"label": "Exponentially weighted moving average (EWMA)", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=30, freq='D')
ts = pd.Series(rng.normal(100, 20, 30) + np.linspace(0, 30, 30), index=idx)

# EWM with different spans
ewm5  = ts.ewm(span=5,  adjust=False).mean()
ewm14 = ts.ewm(span=14, adjust=False).mean()
# EWM with alpha (decay factor directly)
ewm_a = ts.ewm(alpha=0.3, adjust=False).mean()

result = pd.DataFrame({'raw': ts, 'ewm5': ewm5, 'ewm14': ewm14, 'ewm_a0.3': ewm_a})
print(result.round(2))
print('\\nEWM vs SMA final values:')
print(f'  EWM(span=5):  {ewm5.iloc[-1]:.2f}')
print(f'  SMA(window=5):{ts.rolling(5).mean().iloc[-1]:.2f}')"""},
],
"rw_scenario": "A supply chain analyst needs to flag anomalous daily order volumes by computing a 14-day rolling mean and standard deviation, then marking any day beyond 2 standard deviations as an outlier.",
"rw_code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=90, freq='D')
orders = pd.Series(rng.normal(500, 60, 90), index=idx, name='orders')
# Inject anomalies
orders.iloc[15] = 950
orders.iloc[45] = 120
orders.iloc[72] = 880

roll = orders.rolling(14)
rm   = roll.mean()
rs   = roll.std()
upper = rm + 2 * rs
lower = rm - 2 * rs

anomalies = orders[(orders > upper) | (orders < lower)]
print(f'Total days: {len(orders)}, Anomalies detected: {len(anomalies)}')
print('\\nAnomalous days:')
for date, val in anomalies.items():
    print(f'  {date.date()}: {val:.0f} orders (mean={rm[date]:.0f}, '
          f'bounds=[{lower[date]:.0f}, {upper[date]:.0f}])')""",
"practice": {
"title": "Bollinger Bands",
"desc": "Generate 60 days of synthetic stock price data starting at $100 with daily returns from N(0.001, 0.02). Compute 20-day SMA and 2-std Bollinger Bands. Print the last 10 rows showing price, upper band, lower band, and whether the price is outside the bands.",
"starter":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=60, freq='B')
# TODO: create price series with cumulative returns

# TODO: compute 20-day SMA and Bollinger Bands

# TODO: flag days outside bands and print last 10 rows
"""},
},

{
"title": "4. Time Series Visualization",
"desc": "Visualizing time series reveals trends, seasonality, and anomalies. Key plots include line charts, seasonal decomposition, ACF/PACF correlograms, and lag plots.",
"examples": [
{"label": "Basic time series plot with annotations", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2023-01-01', periods=365, freq='D')
ts = pd.Series(
    100 + np.linspace(0, 50, 365) + 20 * np.sin(2*np.pi*np.arange(365)/365) + rng.normal(0, 5, 365),
    index=idx, name='sales'
)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(ts.index, ts.values, lw=1, color='steelblue', label='Daily')
ax.plot(ts.rolling(30).mean().index, ts.rolling(30).mean(), lw=2, color='tomato', label='30-day MA')
ax.axvline(pd.Timestamp('2023-06-21'), color='green', ls='--', lw=1.5, label='Summer Solstice')
ax.fill_between(ts.index, ts.rolling(30).mean() - ts.rolling(30).std(),
                ts.rolling(30).mean() + ts.rolling(30).std(), alpha=0.2, color='tomato')
ax.set(title='Sales Time Series with 30-Day Moving Average', xlabel='Date', ylabel='Sales')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('ts_basic.png', dpi=100)
plt.close()
print('Saved ts_basic.png')"""},
{"label": "Seasonal subseries plot", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

rng = np.random.default_rng(0)
idx = pd.date_range('2022-01-01', periods=36, freq='ME')
monthly = pd.Series(
    200 + 50*np.sin(2*np.pi*np.arange(36)/12) + rng.normal(0, 10, 36),
    index=idx, name='revenue'
)

fig, axes = plt.subplots(3, 4, figsize=(14, 8), sharey=True)
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for m in range(1, 13):
    ax = axes[(m-1)//4][(m-1)%4]
    data = monthly[monthly.index.month == m]
    ax.bar(range(len(data)), data.values, color='steelblue', alpha=0.7)
    ax.axhline(data.mean(), color='tomato', lw=2)
    ax.set_title(month_names[m-1], fontsize=10)
    ax.set_xticks([])
plt.suptitle('Seasonal Subseries Plot — Monthly Revenue', fontsize=13)
plt.tight_layout()
plt.savefig('ts_seasonal_sub.png', dpi=100)
plt.close()
print('Saved ts_seasonal_sub.png')"""},
{"label": "ACF and PACF correlograms", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

try:
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    rng = np.random.default_rng(42)
    # AR(2) process: y_t = 0.7*y_{t-1} - 0.3*y_{t-2} + noise
    n = 200
    y = np.zeros(n)
    eps = rng.normal(0, 1, n)
    for t in range(2, n):
        y[t] = 0.7*y[t-1] - 0.3*y[t-2] + eps[t]
    ts = pd.Series(y)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    plot_acf(ts, lags=20, ax=axes[0], title='ACF — AR(2) Process')
    plot_pacf(ts, lags=20, ax=axes[1], title='PACF — AR(2) Process', method='ywm')
    plt.tight_layout()
    plt.savefig('ts_acf.png', dpi=100)
    plt.close()
    print('Saved ts_acf.png')
    print('ACF at lag 1:', round(ts.autocorr(1), 3))
    print('ACF at lag 2:', round(ts.autocorr(2), 3))
except ImportError:
    print('statsmodels not installed — pip install statsmodels')
    import pandas as pd, numpy as np
    ts = pd.Series(np.random.randn(100))
    print('Manual ACF at lags 1-5:')
    for lag in range(1, 6):
        print(f'  lag {lag}: {ts.autocorr(lag):.3f}')"""},
{"label": "Lag plot and return distribution", "code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=100, freq='B')
price = 100 + np.cumsum(rng.normal(0, 1.5, 100))
ts = pd.Series(price, index=idx)
returns = ts.pct_change().dropna() * 100

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
# Lag plot
axes[0].scatter(ts.values[:-1], ts.values[1:], alpha=0.5, s=20, color='steelblue')
axes[0].set(title='Lag Plot (lag=1)', xlabel='Price(t)', ylabel='Price(t+1)')

# Return distribution
axes[1].hist(returns, bins=20, color='coral', edgecolor='white', alpha=0.8)
axes[1].set(title='Daily Return Distribution', xlabel='Return (%)', ylabel='Count')

# Rolling volatility
vol = returns.rolling(10).std()
axes[2].plot(vol.index, vol, color='purple', lw=1.5)
axes[2].set(title='10-Day Rolling Volatility', xlabel='Date', ylabel='Std Dev (%)')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('ts_lag_dist.png', dpi=100)
plt.close()
print('Saved ts_lag_dist.png')
print(f'Return stats: mean={returns.mean():.2f}%, std={returns.std():.2f}%, skew={returns.skew():.2f}')"""},
],
"rw_scenario": "A business analyst needs to visualize 2 years of weekly e-commerce sales showing trend, seasonality, rolling average, and year-over-year comparison in a single dashboard.",
"rw_code":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2023-01-02', periods=104, freq='W-MON')
trend = np.linspace(5000, 8000, 104)
seasonal = 1500 * np.sin(2*np.pi*np.arange(104)/52)
sales = pd.Series(trend + seasonal + rng.normal(0, 200, 104), index=idx, name='sales')

y2023 = sales['2023'].values
y2024 = sales['2024'].values[:len(y2023)]

fig, axes = plt.subplots(2, 1, figsize=(14, 8))
axes[0].plot(sales.index, sales, alpha=0.4, lw=1, color='steelblue', label='Weekly')
axes[0].plot(sales.rolling(8).mean().index, sales.rolling(8).mean(), lw=2, color='tomato', label='8-wk MA')
axes[0].set(title='Weekly E-Commerce Sales (2023-2024)', ylabel='Sales ($)')
axes[0].legend(); axes[0].grid(alpha=0.3)

weeks = range(1, min(len(y2023), len(y2024))+1)
axes[1].plot(weeks, y2023[:len(weeks)], label='2023', color='steelblue', lw=2)
axes[1].plot(weeks, y2024[:len(weeks)], label='2024', color='tomato', lw=2)
axes[1].set(title='Year-over-Year Comparison', xlabel='Week', ylabel='Sales ($)')
axes[1].legend(); axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('ts_dashboard.png', dpi=100)
plt.close()
print('Saved ts_dashboard.png')
yoy_growth = (y2024.mean() / y2023.mean() - 1) * 100
print(f'YoY growth: {yoy_growth:+.1f}%')""",
"practice": {
"title": "Multi-Series Time Plot",
"desc": "Generate 52 weeks of data for three products (A, B, C) with different trends and seasonalities. Plot all three on the same axis with a legend. Add a 4-week rolling average for each. Save as 'practice_ts.png'.",
"starter":
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=52, freq='W')
# TODO: create 3 product series with different patterns

# TODO: plot all 3 with rolling averages

plt.savefig('practice_ts.png', dpi=100)
plt.close()
print('Saved practice_ts.png')"""},
},

{
"title": "5. Trend & Seasonality Decomposition",
"desc": "Decomposition separates a time series into trend, seasonal, and residual components. Additive decomposition (Y = T + S + R) works for constant amplitude seasonality; multiplicative (Y = T × S × R) for growing amplitude.",
"examples": [
{"label": "Classical decomposition with statsmodels", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.seasonal import seasonal_decompose
    rng = np.random.default_rng(42)
    idx = pd.date_range('2021-01-01', periods=48, freq='ME')
    trend_comp = np.linspace(100, 180, 48)
    seasonal_comp = 20 * np.sin(2*np.pi*np.arange(48)/12)
    noise = rng.normal(0, 5, 48)
    ts = pd.Series(trend_comp + seasonal_comp + noise, index=idx)

    result = seasonal_decompose(ts, model='additive', period=12)
    print('Decomposition components (first 6 months):')
    df = pd.DataFrame({
        'observed': result.observed,
        'trend':    result.trend,
        'seasonal': result.seasonal,
        'resid':    result.resid,
    }).dropna()
    print(df.head(6).round(2))
    print(f'\\nTrend range: {result.trend.dropna().min():.1f} - {result.trend.dropna().max():.1f}')
    print(f'Seasonal amplitude: {result.seasonal.max():.1f}')
    print(f'Residual std: {result.resid.dropna().std():.2f}')
except ImportError:
    print('pip install statsmodels')"""},
{"label": "Additive vs multiplicative decomposition", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.seasonal import seasonal_decompose
    rng = np.random.default_rng(0)
    idx = pd.date_range('2020-01-01', periods=60, freq='ME')
    t = np.arange(60)
    trend = 100 + 2*t
    seasonal = 0.3 * np.sin(2*np.pi*t/12)  # proportional to trend

    additive_ts = pd.Series(trend + 20*np.sin(2*np.pi*t/12) + rng.normal(0,3,60), index=idx)
    multiplicative_ts = pd.Series(trend * (1 + seasonal) + rng.normal(0,3,60), index=idx)

    for name, ts, model in [('Additive TS', additive_ts, 'additive'),
                             ('Multiplicative TS', multiplicative_ts, 'multiplicative')]:
        dec = seasonal_decompose(ts, model=model, period=12)
        resid_std = dec.resid.dropna().std()
        print(f'{name} ({model}): residual std = {resid_std:.3f}')
        print(f'  Seasonal max = {dec.seasonal.max():.3f}')
except ImportError:
    print('pip install statsmodels')
    import numpy as np
    t = np.arange(60)
    ts = 100 + 2*t + 20*np.sin(2*np.pi*t/12) + np.random.normal(0,3,60)
    print('Manual trend (linear fit):')
    coeffs = np.polyfit(t, ts, 1)
    print(f'  slope={coeffs[0]:.2f}, intercept={coeffs[1]:.2f}')"""},
{"label": "STL decomposition (robust to outliers)", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.seasonal import STL
    rng = np.random.default_rng(42)
    idx = pd.date_range('2020-01-01', periods=60, freq='ME')
    ts = pd.Series(
        100 + np.linspace(0, 40, 60) + 15*np.sin(2*np.pi*np.arange(60)/12) + rng.normal(0, 4, 60),
        index=idx
    )
    # Add outlier
    ts.iloc[24] = 250

    stl = STL(ts, period=12, robust=True)
    result = stl.fit()
    print('STL Decomposition (robust=True):')
    df = pd.DataFrame({'trend': result.trend, 'seasonal': result.seasonal, 'resid': result.resid})
    print(df.tail(6).round(2))
    print(f'\\nMax residual (outlier detected at): {result.resid.abs().idxmax().date()}')
    print(f'Residual value: {result.resid.abs().max():.1f}')
except ImportError:
    print('pip install statsmodels')"""},
{"label": "Extracting and using trend for forecasting", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(7)
idx = pd.date_range('2022-01-01', periods=36, freq='ME')
t = np.arange(36)
ts = pd.Series(100 + 3*t + 15*np.sin(2*np.pi*t/12) + rng.normal(0, 5, 36), index=idx)

# Fit linear trend
coeffs = np.polyfit(t, ts, 1)
trend  = np.polyval(coeffs, t)
detrended = ts.values - trend

# Seasonal component (average over each month)
seasonal = np.zeros(12)
for m in range(12):
    seasonal[m] = detrended[m::12].mean()

# Reconstruct and forecast next 6 months
t_fut = np.arange(36, 42)
trend_fut    = np.polyval(coeffs, t_fut)
seasonal_fut = seasonal[t_fut % 12]
forecast     = trend_fut + seasonal_fut

print(f'Trend: slope={coeffs[0]:.2f}/month, intercept={coeffs[1]:.2f}')
print('\\nSeasonal pattern (monthly avg deviation):')
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for m, (name, val) in enumerate(zip(months, seasonal)):
    print(f'  {name}: {val:+.1f}')
print('\\nForecast (next 6 months):')
fut_idx = pd.date_range('2025-01-01', periods=6, freq='ME')
for d, v in zip(fut_idx, forecast):
    print(f'  {d.strftime(\"%b %Y\")}: {v:.1f}')"""},
],
"rw_scenario": "An energy analyst decomposes hourly electricity consumption data to isolate the weekly seasonal pattern, long-term trend, and irregular spikes for demand forecasting.",
"rw_code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.seasonal import STL
    rng = np.random.default_rng(42)
    idx = pd.date_range('2024-01-01', periods=52*7, freq='D')
    t = np.arange(len(idx))
    trend_comp   = 500 + 0.3 * t
    weekly_seas  = 80 * np.sin(2*np.pi*t/7)
    annual_seas  = 120 * np.sin(2*np.pi*t/365)
    consumption  = pd.Series(trend_comp + weekly_seas + annual_seas + rng.normal(0, 15, len(t)), index=idx)

    stl = STL(consumption, period=7, robust=True)
    res = stl.fit()

    weekly_pattern = pd.Series(res.seasonal).groupby(pd.date_range('2024-01-01', periods=len(idx), freq='D').dayofweek).mean()
    days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    print('Weekly consumption pattern (avg deviation from trend):')
    for d, v in zip(days, weekly_pattern.reindex(range(7))):
        bar = '█' * int(abs(v) / 10)
        print(f'  {d}: {v:+.1f} kWh {bar}')
    print(f'\\nOverall trend: +{(res.trend.iloc[-1] - res.trend.iloc[0]):.1f} kWh over the period')
    print(f'Residual std (noise): {res.resid.std():.1f} kWh')
except ImportError:
    print('pip install statsmodels')""",
"practice": {
"title": "Decompose and Evaluate",
"desc": "Generate 3 years of monthly sales data with an upward trend and strong December seasonality (add 200 to December values). Use seasonal_decompose with period=12. Print the seasonal indices for each month. Which month has the highest seasonal component?",
"starter":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2022-01-01', periods=36, freq='ME')
# TODO: create monthly sales with trend + December spike

# TODO: decompose

# TODO: print seasonal indices by month
"""},
},

{
"title": "6. Stationarity & Differencing",
"desc": "Stationarity means constant mean, variance, and autocorrelation over time. Most statistical forecasting models require stationary input. Use the ADF test to check, and differencing to achieve stationarity.",
"examples": [
{"label": "ADF test for stationarity", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.stattools import adfuller
    rng = np.random.default_rng(42)
    # Non-stationary: random walk
    rw = pd.Series(np.cumsum(rng.normal(0, 1, 100)))
    # Stationary: white noise
    wn = pd.Series(rng.normal(0, 1, 100))

    for name, ts in [('Random Walk', rw), ('White Noise', wn)]:
        result = adfuller(ts, autolag='AIC')
        print(f'{name}:')
        print(f'  ADF Statistic: {result[0]:.4f}')
        print(f'  p-value:       {result[1]:.4f}')
        print(f'  Critical 5%:   {result[4]["5%"]:.4f}')
        conclusion = 'STATIONARY' if result[1] < 0.05 else 'NON-STATIONARY'
        print(f'  Conclusion:    {conclusion}')
        print()
except ImportError:
    print('pip install statsmodels')
    import numpy as np
    rng = np.random.default_rng(42)
    ts = np.cumsum(rng.normal(0, 1, 100))
    # Simple manual check: variance of first vs second half
    print('Variance first half:', np.var(ts[:50]).round(2))
    print('Variance second half:', np.var(ts[50:]).round(2))"""},
{"label": "First and second differencing", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.stattools import adfuller
    rng = np.random.default_rng(0)
    idx = pd.date_range('2020-01-01', periods=60, freq='ME')
    # Trend + noise (non-stationary)
    ts = pd.Series(100 + 2*np.arange(60) + rng.normal(0, 5, 60), index=idx)

    diff1 = ts.diff().dropna()
    diff2 = ts.diff().diff().dropna()

    for name, series in [('Original', ts), ('1st Diff', diff1), ('2nd Diff', diff2)]:
        adf = adfuller(series, autolag='AIC')
        stat = 'STATIONARY' if adf[1] < 0.05 else 'NON-STATIONARY'
        print(f'{name:10s}: ADF={adf[0]:7.3f}, p={adf[1]:.4f} → {stat}')

    print('\\nDescriptive stats after 1st differencing:')
    print(diff1.describe().round(3))
except ImportError:
    print('pip install statsmodels')
    import numpy as np
    ts = np.cumsum(np.random.randn(60)) + np.arange(60)
    diff1 = np.diff(ts)
    print(f'Original mean: {ts.mean():.2f}, Diff mean: {diff1.mean():.2f}')
    print(f'Original std:  {ts.std():.2f}, Diff std:  {diff1.std():.2f}')"""},
{"label": "Log transform for variance stabilization", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2020-01-01', periods=48, freq='ME')
# Growing variance (multiplicative process)
t = np.arange(48)
ts = pd.Series(100 * np.exp(0.05*t + rng.normal(0, 0.1, 48)), index=idx)

log_ts  = np.log(ts)
diff_ts = ts.diff().dropna()
log_diff = log_ts.diff().dropna()  # log returns

print('Original series stats:')
print(f'  Std first half: {ts[:24].std():.2f}')
print(f'  Std second half: {ts[24:].std():.2f}')
print('\\nLog-transformed stats:')
print(f'  Std first half: {log_ts[:24].std():.4f}')
print(f'  Std second half: {log_ts[24:].std():.4f}')
print('\\nLog-differenced (log returns) first 5:')
print(log_diff.head().round(4))
print(f'Annualized log return: {log_diff.mean() * 12:.3f}')"""},
{"label": "Seasonal differencing", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.stattools import adfuller, kpss
    rng = np.random.default_rng(7)
    idx = pd.date_range('2020-01-01', periods=60, freq='ME')
    ts = pd.Series(
        100 + np.linspace(0, 20, 60) + 30*np.sin(2*np.pi*np.arange(60)/12) + rng.normal(0, 3, 60),
        index=idx
    )
    # Seasonal differencing (lag=12)
    seasonal_diff = ts.diff(12).dropna()
    # Then first difference to remove trend
    both_diff = seasonal_diff.diff().dropna()

    for name, s in [('Original', ts), ('Seasonal diff(12)', seasonal_diff), ('Both diffs', both_diff)]:
        adf_p = adfuller(s)[1]
        print(f'{name:20s}: ADF p={adf_p:.4f} → {"stationary" if adf_p < 0.05 else "non-stationary"}')
except ImportError:
    print('pip install statsmodels')
    import numpy as np
    ts = np.array([100 + 30*np.sin(2*np.pi*i/12) for i in range(60)])
    sdiff = ts[12:] - ts[:-12]
    print('Seasonal diff mean:', sdiff.mean().round(2))
    print('Seasonal diff std:', sdiff.std().round(2))"""},
],
"rw_scenario": "A data scientist needs to prepare monthly website traffic data for ARIMA modeling — check stationarity, apply appropriate transformations, and verify the result.",
"rw_code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.stattools import adfuller
    rng = np.random.default_rng(42)
    idx = pd.date_range('2021-01-01', periods=48, freq='ME')
    traffic = pd.Series(
        5000 * np.exp(0.02 * np.arange(48)) +
        2000 * np.sin(2*np.pi*np.arange(48)/12) +
        rng.normal(0, 300, 48),
        index=idx, name='visitors'
    )

    def check_stationarity(series, name):
        adf = adfuller(series.dropna())
        stationary = adf[1] < 0.05
        print(f'{name}: p={adf[1]:.4f} | {"✓ stationary" if stationary else "✗ non-stationary"}')
        return stationary

    # Step 1: check original
    check_stationarity(traffic, 'Original')
    # Step 2: log transform
    log_traffic = np.log(traffic)
    check_stationarity(log_traffic, 'Log-transformed')
    # Step 3: seasonal diff
    log_sdiff = log_traffic.diff(12)
    check_stationarity(log_sdiff, 'Log + seasonal diff(12)')
    # Step 4: regular diff
    log_sdiff_diff = log_sdiff.diff()
    check_stationarity(log_sdiff_diff, 'Log + sdiff + diff')
    print('\\nFinal series ready for ARIMA:')
    print(log_sdiff_diff.dropna().describe().round(4))
except ImportError:
    print('pip install statsmodels')""",
"practice": {
"title": "Make It Stationary",
"desc": "Generate 60 months of quarterly sales data: base=500, trend=+5/month, seasonal amplitude=100, noise std=20. Apply the minimum number of transformations to make it stationary (ADF p < 0.05). Print the ADF result at each step.",
"starter":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.stattools import adfuller
    rng = np.random.default_rng(0)
    idx = pd.date_range('2020-01-01', periods=60, freq='ME')
    # TODO: create series with trend + seasonality

    # TODO: apply transformations until stationary

    # TODO: print ADF result at each step
except ImportError:
    print('pip install statsmodels')"""},
},

{
"title": "7. ARIMA Modeling",
"desc": "ARIMA(p,d,q) combines AutoRegression (p lags), Integration (d differences for stationarity), and Moving Average (q lagged forecast errors). SARIMA extends this with seasonal components.",
"examples": [
{"label": "Fitting ARIMA with statsmodels", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.arima.model import ARIMA
    rng = np.random.default_rng(42)
    # AR(1) process
    n = 100
    y = np.zeros(n)
    eps = rng.normal(0, 1, n)
    for t in range(1, n):
        y[t] = 0.7 * y[t-1] + eps[t]
    ts = pd.Series(y)

    model = ARIMA(ts, order=(1, 0, 0))
    result = model.fit()
    print(result.summary().tables[1])
    print(f'\\nAIC: {result.aic:.2f}')
    print(f'BIC: {result.bic:.2f}')
    forecast = result.forecast(steps=5)
    print('\\nForecast (next 5 steps):')
    print(forecast.round(3).tolist())
except ImportError:
    print('pip install statsmodels')"""},
{"label": "Selecting ARIMA order with AIC", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.arima.model import ARIMA
    import warnings; warnings.filterwarnings('ignore')
    rng = np.random.default_rng(0)
    ts = pd.Series(np.cumsum(rng.normal(0, 1, 80)))  # random walk → d=1

    best_aic = float('inf')
    best_order = None
    results = []
    for p in range(3):
        for q in range(3):
            try:
                m = ARIMA(ts, order=(p, 1, q)).fit()
                results.append((p, 1, q, m.aic))
                if m.aic < best_aic:
                    best_aic, best_order = m.aic, (p, 1, q)
            except:
                pass
    results.sort(key=lambda x: x[3])
    print('Top 5 ARIMA orders by AIC:')
    for p, d, q, aic in results[:5]:
        mark = '<-- best' if (p,d,q) == best_order else ''
        print(f'  ARIMA({p},{d},{q}): AIC={aic:.2f} {mark}')
except ImportError:
    print('pip install statsmodels')"""},
{"label": "ARIMA forecast with confidence intervals", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.arima.model import ARIMA
    import warnings; warnings.filterwarnings('ignore')
    rng = np.random.default_rng(42)
    idx = pd.date_range('2023-01-01', periods=60, freq='ME')
    ts = pd.Series(
        50 + np.linspace(0, 20, 60) + rng.normal(0, 4, 60),
        index=idx
    )
    train, test = ts[:48], ts[48:]
    model  = ARIMA(train, order=(1, 1, 1)).fit()
    fc     = model.get_forecast(steps=12)
    fc_df  = fc.summary_frame(alpha=0.05)

    print('Forecast vs Actual (last 6 months):')
    comparison = pd.DataFrame({
        'actual':   test.values,
        'forecast': fc_df['mean'].values,
        'lower_95': fc_df['mean_ci_lower'].values,
        'upper_95': fc_df['mean_ci_upper'].values,
    }, index=test.index)
    print(comparison.round(2))
    from sklearn.metrics import mean_absolute_error
    mae = mean_absolute_error(test, fc_df['mean'])
    print(f'\\nMAE: {mae:.2f}')
except ImportError:
    print('pip install statsmodels scikit-learn')"""},
{"label": "SARIMA for seasonal data", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    import warnings; warnings.filterwarnings('ignore')
    rng = np.random.default_rng(7)
    idx = pd.date_range('2020-01-01', periods=48, freq='ME')
    ts = pd.Series(
        100 + np.linspace(0, 20, 48) + 25*np.sin(2*np.pi*np.arange(48)/12) + rng.normal(0, 4, 48),
        index=idx
    )
    train = ts[:36]
    # SARIMA(1,1,1)(1,1,0,12)
    model  = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,0,12)).fit(disp=False)
    fc     = model.forecast(steps=12)
    actual = ts[36:]

    print('SARIMA Forecast vs Actual:')
    for d, f, a in zip(fc.index, fc.values, actual.values):
        err = f - a
        print(f'  {d.strftime("%b %Y")}: forecast={f:.1f}, actual={a:.1f}, error={err:+.1f}')
    rmse = np.sqrt(np.mean((fc.values - actual.values)**2))
    print(f'\\nRMSE: {rmse:.2f}')
except ImportError:
    print('pip install statsmodels')"""},
],
"rw_scenario": "A demand planner needs to forecast next 3 months of product demand using historical monthly data. They fit SARIMA, evaluate on a holdout set, and report RMSE and MAPE.",
"rw_code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    import warnings; warnings.filterwarnings('ignore')
    rng = np.random.default_rng(42)
    idx = pd.date_range('2021-01-01', periods=36, freq='ME')
    demand = pd.Series(
        500 + np.linspace(0, 100, 36) +
        150 * np.sin(2*np.pi*np.arange(36)/12) +
        rng.normal(0, 20, 36),
        index=idx
    ).clip(0)

    train, test = demand[:30], demand[30:]
    model  = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,0,12)).fit(disp=False)
    fc     = model.forecast(steps=6)

    mape = np.mean(np.abs((test.values - fc.values) / test.values)) * 100
    rmse = np.sqrt(np.mean((test.values - fc.values)**2))
    print('3-Month Demand Forecast:')
    for d, f, a in zip(fc.index, fc.values, test.values):
        print(f'  {d.strftime("%b %Y")}: forecast={f:.0f}, actual={a:.0f}')
    print(f'\\nMAPE: {mape:.1f}%')
    print(f'RMSE: {rmse:.1f} units')
except ImportError:
    print('pip install statsmodels')""",
"practice": {
"title": "Fit and Forecast",
"desc": "Generate 48 months of AR(2) data: y_t = 0.6*y_{t-1} - 0.2*y_{t-2} + noise. Use ARIMA(2,0,0) on the first 36 months. Forecast the last 12 months and compute MAE. Print forecast vs actual.",
"starter":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.arima.model import ARIMA
    import warnings; warnings.filterwarnings('ignore')
    rng = np.random.default_rng(42)
    # TODO: generate AR(2) process

    # TODO: split train/test, fit ARIMA(2,0,0)

    # TODO: forecast and compute MAE
except ImportError:
    print('pip install statsmodels')"""},
},

{
"title": "8. Exponential Smoothing",
"desc": "Exponential smoothing methods weight recent observations more heavily. Simple ES handles level; Holt's adds trend; Holt-Winters adds seasonality. These are fast, interpretable, and competitive with ARIMA.",
"examples": [
{"label": "Simple Exponential Smoothing", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.holtwinters import SimpleExpSmoothing
    rng = np.random.default_rng(42)
    ts = pd.Series(rng.normal(100, 10, 30))

    for alpha in [0.1, 0.3, 0.7]:
        model = SimpleExpSmoothing(ts, initialization_method='estimated').fit(smoothing_level=alpha, optimized=False)
        fc = model.forecast(3)
        print(f'alpha={alpha}: last fitted={model.fittedvalues.iloc[-1]:.2f}, forecast={fc.values.round(2).tolist()}')

    # Optimal alpha
    optimal = SimpleExpSmoothing(ts, initialization_method='estimated').fit(optimized=True)
    print(f'\\nOptimal alpha: {optimal.params["smoothing_level"]:.4f}')
    print(f'Optimal forecast: {optimal.forecast(3).values.round(2).tolist()}')
except ImportError:
    print('pip install statsmodels')"""},
{"label": "Holt's Linear Trend Method", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.holtwinters import Holt
    rng = np.random.default_rng(0)
    idx = pd.date_range('2024-01-01', periods=24, freq='ME')
    ts = pd.Series(50 + 2*np.arange(24) + rng.normal(0, 3, 24), index=idx)

    # Holt's with additive trend
    for trend in ['add', 'mul']:
        try:
            model = Holt(ts, exponential=(trend=='mul'), initialization_method='estimated').fit(optimized=True)
            fc    = model.forecast(6)
            print(f'Holt ({trend} trend):')
            print(f'  alpha={model.params["smoothing_level"]:.3f}, beta={model.params["smoothing_trend"]:.3f}')
            print(f'  Forecast: {fc.values.round(1).tolist()}')
        except:
            pass
    print('\\nActual last 3:', ts.tail(3).values.round(1).tolist())
except ImportError:
    print('pip install statsmodels')"""},
{"label": "Holt-Winters Triple Exponential Smoothing", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    import warnings; warnings.filterwarnings('ignore')
    rng = np.random.default_rng(42)
    idx = pd.date_range('2020-01-01', periods=48, freq='ME')
    ts = pd.Series(
        100 + np.linspace(0, 30, 48) + 25*np.sin(2*np.pi*np.arange(48)/12) + rng.normal(0, 4, 48),
        index=idx
    )
    train, test = ts[:36], ts[36:]

    model = ExponentialSmoothing(
        train, trend='add', seasonal='add', seasonal_periods=12,
        initialization_method='estimated'
    ).fit(optimized=True)

    fc = model.forecast(12)
    mape = np.mean(np.abs((test.values - fc.values) / test.values)) * 100
    rmse = np.sqrt(np.mean((test.values - fc.values)**2))
    print('Holt-Winters forecast:')
    print(f'  Alpha (level): {model.params["smoothing_level"]:.3f}')
    print(f'  Beta (trend):  {model.params["smoothing_trend"]:.3f}')
    print(f'  Gamma (season):{model.params["smoothing_seasonal"]:.3f}')
    print(f'\\nMAPE: {mape:.2f}%')
    print(f'RMSE: {rmse:.2f}')
except ImportError:
    print('pip install statsmodels')"""},
{"label": "Comparing ES methods on same data", "code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing
    import warnings; warnings.filterwarnings('ignore')
    rng = np.random.default_rng(7)
    idx = pd.date_range('2021-01-01', periods=36, freq='ME')
    ts = pd.Series(
        200 + np.linspace(0, 50, 36) + 30*np.sin(2*np.pi*np.arange(36)/12) + rng.normal(0, 8, 36),
        index=idx
    )
    train, test = ts[:30], ts[30:]
    n_fc = 6

    models = {
        'SES':   SimpleExpSmoothing(train, initialization_method='estimated').fit(optimized=True),
        'Holt':  Holt(train, initialization_method='estimated').fit(optimized=True),
        'HW':    ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=12,
                                      initialization_method='estimated').fit(optimized=True),
    }
    print(f'{"Method":<8} {"RMSE":>8} {"MAPE%":>8}')
    print('-' * 28)
    for name, m in models.items():
        fc  = m.forecast(n_fc)
        rmse = np.sqrt(np.mean((test.values - fc.values)**2))
        mape = np.mean(np.abs((test.values - fc.values) / test.values)) * 100
        print(f'{name:<8} {rmse:>8.2f} {mape:>8.2f}')
except ImportError:
    print('pip install statsmodels')"""},
],
"rw_scenario": "A retail company applies Holt-Winters to forecast daily store traffic for the next 30 days, accounting for weekly seasonality and a gradual upward trend.",
"rw_code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    import warnings; warnings.filterwarnings('ignore')
    rng = np.random.default_rng(42)
    idx = pd.date_range('2024-01-01', periods=90, freq='D')
    traffic = pd.Series(
        500 + np.linspace(0, 50, 90) +
        100 * np.sin(2*np.pi*np.arange(90)/7) +
        rng.normal(0, 20, 90),
        index=idx
    ).clip(0).round()

    train, test = traffic[:75], traffic[75:]
    model = ExponentialSmoothing(
        train, trend='add', seasonal='add', seasonal_periods=7,
        initialization_method='estimated'
    ).fit(optimized=True)

    fc = model.forecast(15)
    mae  = np.mean(np.abs(test.values - fc.values))
    mape = np.mean(np.abs((test.values - fc.values) / test.values)) * 100

    print('Holt-Winters Daily Traffic Forecast:')
    print(f'  Params: alpha={model.params["smoothing_level"]:.3f}, '
          f'beta={model.params["smoothing_trend"]:.3f}, '
          f'gamma={model.params["smoothing_seasonal"]:.3f}')
    print(f'\\nForecast (next 15 days):')
    days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    for d, f, a in zip(fc.index, fc.values, test.values):
        print(f'  {d.strftime("%a %b %d")}: forecast={f:.0f}, actual={a:.0f}')
    print(f'\\nMAE: {mae:.1f} | MAPE: {mape:.1f}%')
except ImportError:
    print('pip install statsmodels')""",
"practice": {
"title": "Holt-Winters Tuning",
"desc": "Generate 3 years of monthly retail sales with trend and seasonality. Compare Holt-Winters additive vs multiplicative seasonal on a 6-month holdout. Print RMSE for both. Which model wins?",
"starter":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    import warnings; warnings.filterwarnings('ignore')
    rng = np.random.default_rng(42)
    idx = pd.date_range('2021-01-01', periods=36, freq='ME')
    # TODO: create monthly sales with additive or multiplicative seasonality

    # TODO: split and fit both models

    # TODO: compare RMSE
except ImportError:
    print('pip install statsmodels')"""},
},

{
"title": "9. Feature Engineering for Time Series",
"desc": "Transforming raw time series into supervised learning features enables ML models (XGBoost, LightGBM) to forecast. Key features: lag values, rolling stats, calendar attributes, and cyclical encoding.",
"examples": [
{"label": "Lag features", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=30, freq='D')
ts = pd.Series(rng.normal(100, 10, 30), index=idx, name='demand')
df = ts.to_frame()

# Create lag features
for lag in [1, 2, 3, 7, 14]:
    df[f'lag_{lag}'] = df['demand'].shift(lag)

df.dropna(inplace=True)
print(f'Feature matrix shape: {df.shape}')
print(df.head(5).round(2))

# Correlation with target
corr = df.corr()['demand'].drop('demand')
print('\\nLag correlations with demand:')
print(corr.round(3))"""},
{"label": "Rolling statistical features", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(0)
idx = pd.date_range('2024-01-01', periods=60, freq='D')
ts = pd.Series(rng.normal(500, 80, 60) + np.linspace(0, 50, 60), index=idx, name='sales')
df = ts.to_frame()

# Rolling features
for w in [7, 14]:
    roll = ts.rolling(w)
    df[f'roll_{w}_mean'] = roll.mean()
    df[f'roll_{w}_std']  = roll.std()
    df[f'roll_{w}_min']  = roll.min()
    df[f'roll_{w}_max']  = roll.max()

# Expanding mean
df['expanding_mean'] = ts.expanding().mean()

df.dropna(inplace=True)
print(f'Feature shape: {df.shape}')
print(df.tail(5).round(1))"""},
{"label": "Calendar and cyclical features", "code":
"""import pandas as pd
import numpy as np

rng = np.random.default_rng(7)
idx = pd.date_range('2024-01-01', periods=365, freq='D')
df = pd.DataFrame({'sales': rng.normal(100, 15, 365)}, index=idx)

# Calendar features
df['day_of_week']  = df.index.dayofweek
df['day_of_month'] = df.index.day
df['month']        = df.index.month
df['quarter']      = df.index.quarter
df['is_weekend']   = (df.index.dayofweek >= 5).astype(int)
df['is_month_end'] = df.index.is_month_end.astype(int)

# Cyclical encoding (preserves periodicity)
df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
df['month_sin'] = np.sin(2 * np.pi * (df['month'] - 1) / 12)
df['month_cos'] = np.cos(2 * np.pi * (df['month'] - 1) / 12)

print('Feature matrix (first 5 rows):')
print(df.head(5).round(3))
print(f'\\nTotal features: {df.shape[1]-1}')
print('Weekend mean:', df[df['is_weekend']==1]['sales'].mean().round(2))
print('Weekday mean:', df[df['is_weekend']==0]['sales'].mean().round(2))"""},
{"label": "ML forecasting pipeline with lag features", "code":
"""import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

rng = np.random.default_rng(42)
idx = pd.date_range('2023-01-01', periods=200, freq='D')
ts = pd.Series(
    100 + np.linspace(0, 30, 200) + 20*np.sin(2*np.pi*np.arange(200)/7) + rng.normal(0, 5, 200),
    index=idx, name='demand'
)

df = ts.to_frame()
# Lag + rolling features
for lag in [1, 2, 3, 7]: df[f'lag_{lag}'] = ts.shift(lag)
df['roll7_mean'] = ts.rolling(7).mean()
df['roll7_std']  = ts.rolling(7).std()
df['dow'] = ts.index.dayofweek
df['dow_sin'] = np.sin(2*np.pi*df['dow']/7)
df['dow_cos'] = np.cos(2*np.pi*df['dow']/7)
df.dropna(inplace=True)

X = df.drop(columns='demand')
y = df['demand']
split = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

model = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)

mae  = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))
print(f'GBM Forecast: MAE={mae:.2f}, RMSE={rmse:.2f}')
print('\\nTop feature importances:')
fi = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
for feat, imp in fi.head(5).items():
    print(f'  {feat:15s}: {imp:.4f}')"""},
],
"rw_scenario": "A logistics company builds an ML forecasting model for package delivery volumes using lag features, rolling statistics, and calendar effects as inputs to a gradient boosting model.",
"rw_code":
"""import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

rng = np.random.default_rng(42)
idx = pd.date_range('2023-01-01', periods=365, freq='D')
volume = pd.Series(
    3000 + np.linspace(0, 500, 365) +
    800 * np.sin(2*np.pi*np.arange(365)/7) +
    500 * (idx.month == 12).astype(float) +  # December peak
    rng.normal(0, 100, 365),
    index=idx
).clip(0)

df = volume.to_frame(name='volume')
for lag in [1, 2, 3, 7, 14]: df[f'lag_{lag}'] = volume.shift(lag)
for w in [7, 14]: df[f'roll_{w}_mean'] = volume.rolling(w).mean()
df['dow']       = volume.index.dayofweek
df['month']     = volume.index.month
df['is_weekend']= (df['dow'] >= 5).astype(int)
df['dow_sin']   = np.sin(2*np.pi*df['dow']/7)
df['dow_cos']   = np.cos(2*np.pi*df['dow']/7)
df.dropna(inplace=True)

X, y = df.drop('volume', axis=1), df['volume']
split = 300
model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
model.fit(X.iloc[:split], y.iloc[:split])
preds = model.predict(X.iloc[split:])
mae = mean_absolute_error(y.iloc[split:], preds)
print(f'MAE: {mae:.0f} packages/day')
fi = pd.Series(model.feature_importances_, index=X.columns).nlargest(5)
print('\\nTop features:')
for f, v in fi.items():
    print(f'  {f}: {v:.4f}')""",
"practice": {
"title": "Build a Feature Matrix",
"desc": "Use the hourly energy dataset (simulate: 7 days × 24 hours = 168 hourly readings with daily cycle). Create: lag_1, lag_24 (same hour yesterday), roll_24_mean, hour_of_day, is_weekday. Train a LinearRegression model and print RMSE.",
"starter":
"""import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=168, freq='h')
# TODO: create hourly energy with daily cycle

# TODO: build feature matrix

# TODO: train LinearRegression and print RMSE
"""},
},

{
"title": "10. Forecasting Evaluation",
"desc": "Proper evaluation of time series forecasts requires time-ordered splits (no leakage), multiple metrics (MAE, RMSE, MAPE), and ideally walk-forward validation to simulate real deployment.",
"examples": [
{"label": "MAE, RMSE, MAPE, and SMAPE", "code":
"""import numpy as np

actual   = np.array([100, 120, 130, 115, 140, 125, 160, 155, 170, 180])
forecast = np.array([105, 115, 135, 110, 145, 130, 150, 160, 165, 185])

mae   = np.mean(np.abs(actual - forecast))
mse   = np.mean((actual - forecast)**2)
rmse  = np.sqrt(mse)
mape  = np.mean(np.abs((actual - forecast) / actual)) * 100
smape = np.mean(2 * np.abs(actual - forecast) / (np.abs(actual) + np.abs(forecast))) * 100
# R-squared
ss_res = np.sum((actual - forecast)**2)
ss_tot = np.sum((actual - actual.mean())**2)
r2 = 1 - ss_res / ss_tot

print(f'MAE:   {mae:.2f}')
print(f'RMSE:  {rmse:.2f}')
print(f'MAPE:  {mape:.2f}%')
print(f'sMAPE: {smape:.2f}%')
print(f'R²:    {r2:.4f}')
print(f'\\nBias (mean error): {(forecast - actual).mean():.2f}')"""},
{"label": "Train/test split for time series", "code":
"""import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge

rng = np.random.default_rng(42)
idx = pd.date_range('2023-01-01', periods=200, freq='D')
ts  = pd.Series(100 + np.linspace(0,30,200) + rng.normal(0, 8, 200), index=idx)

df = ts.to_frame(name='y')
for lag in [1, 7, 14]: df[f'lag_{lag}'] = ts.shift(lag)
df.dropna(inplace=True)

X = df.drop('y', axis=1).values
y = df['y'].values

# Time-ordered split (NEVER random split for time series!)
n = len(X)
split = int(n * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

model = Ridge().fit(X_train, y_train)
preds = model.predict(X_test)
mae   = np.mean(np.abs(y_test - preds))
rmse  = np.sqrt(np.mean((y_test - preds)**2))
print(f'Train size: {split}, Test size: {n - split}')
print(f'MAE:  {mae:.2f}')
print(f'RMSE: {rmse:.2f}')
print('\\nNEVER use random train_test_split for time series!')
print('This leaks future information into training data.')"""},
{"label": "Walk-forward (expanding window) validation", "code":
"""import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge

rng = np.random.default_rng(42)
n   = 120
ts  = pd.Series(100 + np.linspace(0, 20, n) + rng.normal(0, 6, n))

df = ts.to_frame(name='y')
for lag in [1, 2, 3, 7]: df[f'lag_{lag}'] = ts.shift(lag)
df.dropna(inplace=True)

X = df.drop('y', axis=1).values
y = df['y'].values

# Walk-forward validation
min_train = 30
step = 5
errors = []
for test_start in range(min_train, len(X) - step + 1, step):
    X_train, y_train = X[:test_start], y[:test_start]
    X_test,  y_test  = X[test_start:test_start+step], y[test_start:test_start+step]
    model = Ridge().fit(X_train, y_train)
    preds = model.predict(X_test)
    errors.extend(np.abs(y_test - preds).tolist())

print(f'Walk-forward CV ({len(errors)} predictions):')
print(f'  MAE:  {np.mean(errors):.2f}')
print(f'  RMSE: {np.sqrt(np.mean(np.array(errors)**2)):.2f}')
print(f'  Std:  {np.std(errors):.2f}')"""},
{"label": "TimeSeriesSplit cross-validation with sklearn", "code":
"""import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor

rng = np.random.default_rng(42)
n   = 200
ts  = pd.Series(100 + np.linspace(0,40,n) + rng.normal(0,8,n))

df = ts.to_frame(name='y')
for lag in [1,2,3,7]: df[f'lag_{lag}'] = ts.shift(lag)
df['roll7'] = ts.rolling(7).mean()
df.dropna(inplace=True)

X = df.drop('y', axis=1)
y = df['y']

tscv = TimeSeriesSplit(n_splits=5, gap=0)
model = GradientBoostingRegressor(n_estimators=50, max_depth=3, random_state=42)
scores = cross_val_score(model, X, y, cv=tscv, scoring='neg_mean_absolute_error')
maes = -scores

print('TimeSeriesSplit CV results (5 folds):')
for i, (mae, (tr, te)) in enumerate(zip(maes, tscv.split(X)), 1):
    print(f'  Fold {i}: train={len(tr)}, test={len(te)}, MAE={mae:.2f}')
print(f'\\nMean MAE: {maes.mean():.2f} ± {maes.std():.2f}')"""},
],
"rw_scenario": "A data science team evaluates three forecasting models (ARIMA, Holt-Winters, GBM) on 1 year of daily data using walk-forward validation to select the production model.",
"rw_code":
"""import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.tsa.arima.model import ARIMA
    from sklearn.ensemble import GradientBoostingRegressor
    import warnings; warnings.filterwarnings('ignore')

    rng = np.random.default_rng(42)
    n   = 200
    idx = pd.date_range('2024-01-01', periods=n, freq='D')
    ts  = pd.Series(
        300 + np.linspace(0,50,n) + 60*np.sin(2*np.pi*np.arange(n)/7) + rng.normal(0,15,n),
        index=idx
    )

    train, test = ts[:160], ts[160:]
    results = {}

    # Holt-Winters
    hw = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=7, initialization_method='estimated').fit(optimized=True)
    results['Holt-Winters'] = hw.forecast(40)

    # GBM with lag features
    df = ts.to_frame(name='y')
    for lag in [1,2,7]: df[f'lag_{lag}'] = ts.shift(lag)
    df.dropna(inplace=True)
    X, y = df.drop('y',axis=1), df['y']
    split = len(train) - 7  # adjust for lag
    gbm = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gbm.fit(X.iloc[:split], y.iloc[:split])
    results['GBM'] = pd.Series(gbm.predict(X.iloc[split:split+40]), index=test.index[:40])

    actual = test.values[:40]
    print('Model Comparison (40-day holdout):')
    print(f'{"Model":<15} {"MAE":>7} {"RMSE":>7} {"MAPE%":>7}')
    print('-' * 38)
    for name, fc in results.items():
        fc_v = fc.values[:40]
        mae  = np.mean(np.abs(actual - fc_v))
        rmse = np.sqrt(np.mean((actual - fc_v)**2))
        mape = np.mean(np.abs((actual - fc_v)/actual))*100
        print(f'{name:<15} {mae:>7.1f} {rmse:>7.1f} {mape:>7.1f}')
except ImportError:
    print('pip install statsmodels scikit-learn')""",
"practice": {
"title": "Cross-Validate a Forecast",
"desc": "Generate 180 days of daily demand data with weekly seasonality. Use TimeSeriesSplit with 5 folds on lag features. Test Ridge, GradientBoosting, and a naive (last value) baseline. Print mean MAE per model.",
"starter":
"""import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor

rng = np.random.default_rng(42)
idx = pd.date_range('2024-01-01', periods=180, freq='D')
# TODO: create demand series

# TODO: create feature matrix

# TODO: cross-validate all three models
"""},
},
{
    "title": "11. Prophet Forecasting",
    "desc": "Use Facebook Prophet for additive time series forecasting with automatic trend, seasonality, and holiday effects. Handle changepoints and produce uncertainty intervals.",
    "examples": [
        {
            "label": "Basic Prophet fit and forecast",
            "code": "import pandas as pd\nimport numpy as np\n\n# Simulate daily data with trend + weekly seasonality (Prophet-ready format)\nnp.random.seed(42)\ndates = pd.date_range('2022-01-01', periods=365, freq='D')\ntrend = np.linspace(100, 200, 365)\nweekly = 10 * np.sin(2 * np.pi * np.arange(365) / 7)\nnoise = np.random.normal(0, 5, 365)\ny = trend + weekly + noise\n\ndf = pd.DataFrame({'ds': dates, 'y': y})\nprint('Prophet input format:')\nprint(df.head())\nprint(f'\\nShape: {df.shape}')\nprint(f'Date range: {df.ds.min().date()} to {df.ds.max().date()}')\nprint(f'y stats: mean={df.y.mean():.1f}, std={df.y.std():.1f}')\n\n# Without Prophet installed, demonstrate the workflow:\nprint('\\nProphet workflow:')\nprint('  from prophet import Prophet')\nprint('  m = Prophet(yearly_seasonality=False, weekly_seasonality=True)')\nprint('  m.fit(df)')\nprint('  future = m.make_future_dataframe(periods=30)')\nprint('  forecast = m.predict(future)')\nprint('  m.plot(forecast)')"
        },
        {
            "label": "Manual additive decomposition as Prophet substitute",
            "code": "import pandas as pd\nimport numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nnp.random.seed(42)\ndates = pd.date_range('2022-01-01', periods=365, freq='D')\ntrend = np.linspace(100, 200, 365)\nweekly = 8 * np.sin(2 * np.pi * np.arange(365) / 7)\nnoise = np.random.normal(0, 5, 365)\ny = trend + weekly + noise\n\ndf = pd.DataFrame({'ds': dates, 'y': y})\ndf['dow'] = df['ds'].dt.dayofweek\n\n# Fit trend with linear regression\nfrom sklearn.linear_model import LinearRegression\nt = np.arange(len(df)).reshape(-1, 1)\nlr = LinearRegression().fit(t, df['y'])\ndf['trend_fit'] = lr.predict(t)\n\n# Fit weekly seasonality as day-of-week means on residuals\ndf['resid'] = df['y'] - df['trend_fit']\ndow_effect = df.groupby('dow')['resid'].mean()\ndf['seasonal'] = df['dow'].map(dow_effect)\ndf['yhat'] = df['trend_fit'] + df['seasonal']\n\nmse = ((df['y'] - df['yhat'])**2).mean()**0.5\nprint(f'RMSE (train): {mse:.2f}')\nfig, axes = plt.subplots(3, 1, figsize=(10, 8))\naxes[0].plot(df['ds'], df['y'], alpha=0.5, label='actual'); axes[0].plot(df['ds'], df['yhat'], label='fit'); axes[0].legend(); axes[0].set_title('Additive Model Fit')\naxes[1].plot(df['ds'], df['trend_fit']); axes[1].set_title('Trend Component')\naxes[2].bar(range(7), dow_effect.values); axes[2].set_xticks(range(7)); axes[2].set_xticklabels(['Mon','Tue','Wed','Thu','Fri','Sat','Sun']); axes[2].set_title('Weekly Seasonality')\nplt.tight_layout(); plt.savefig('prophet_decomp.png', dpi=80); plt.close(); print('Saved prophet_decomp.png')"
        },
        {
            "label": "Changepoint detection with PELT algorithm",
            "code": "import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\n# Simulate series with structural breaks\nnp.random.seed(42)\nn = 300\nt = np.arange(n)\n# Three regimes: flat, upward, downward\ny = np.concatenate([\n    np.random.normal(10, 2, 100),\n    np.random.normal(25, 2, 100),\n    np.random.normal(15, 2, 100)\n])\n\n# Simple CUSUM-based changepoint detection\ndef cusum_changepoints(series, threshold=10):\n    mu = series.mean()\n    cusum_pos = np.zeros(len(series))\n    cusum_neg = np.zeros(len(series))\n    changepoints = []\n    for i in range(1, len(series)):\n        cusum_pos[i] = max(0, cusum_pos[i-1] + series[i] - mu - 0.5)\n        cusum_neg[i] = max(0, cusum_neg[i-1] - series[i] + mu - 0.5)\n        if cusum_pos[i] > threshold or cusum_neg[i] > threshold:\n            changepoints.append(i)\n            cusum_pos[i] = cusum_neg[i] = 0\n    return changepoints\n\ncps = cusum_changepoints(y, threshold=15)\nprint(f'Detected changepoints at indices: {cps}')\nfig, ax = plt.subplots(figsize=(10, 4))\nax.plot(t, y, alpha=0.7)\nfor cp in cps:\n    ax.axvline(cp, color='red', linestyle='--', linewidth=2, label=f'CP at {cp}' if cp == cps[0] else '')\nax.set_title('CUSUM Changepoint Detection'); ax.legend()\nplt.tight_layout(); plt.savefig('changepoints.png', dpi=80); plt.close(); print('Saved changepoints.png')"
        },
        {
            "label": "Cross-validation for forecasting (walk-forward)",
            "code": "import pandas as pd\nimport numpy as np\nfrom sklearn.linear_model import Ridge\n\nnp.random.seed(42)\ndates = pd.date_range('2022-01-01', periods=200, freq='D')\ntrend = np.linspace(0, 50, 200)\nweekly = 5 * np.sin(2 * np.pi * np.arange(200) / 7)\nnoise = np.random.normal(0, 3, 200)\ny = trend + weekly + noise\n\ndf = pd.DataFrame({'ds': dates, 'y': y})\ndf['t'] = np.arange(len(df))\ndf['dow'] = df['ds'].dt.dayofweek\n# Encode day-of-week as dummies\nfor d in range(7):\n    df[f'dow_{d}'] = (df['dow'] == d).astype(int)\n\nfeat_cols = ['t'] + [f'dow_{d}' for d in range(7)]\nX = df[feat_cols].values\n\n# Walk-forward validation: train on first 60%, then expand\ninitial = 120; horizon = 7; errors = []\nfor start in range(initial, len(df) - horizon, horizon):\n    X_tr, y_tr = X[:start], y[:start]\n    X_te, y_te = X[start:start+horizon], y[start:start+horizon]\n    m = Ridge().fit(X_tr, y_tr)\n    preds = m.predict(X_te)\n    errors.append(np.sqrt(((y_te - preds)**2).mean()))\n\nprint(f'Walk-forward validation ({len(errors)} folds):')\nprint(f'  Mean RMSE: {np.mean(errors):.2f}')\nprint(f'  Std  RMSE: {np.std(errors):.2f}')\nprint(f'  Min  RMSE: {min(errors):.2f}, Max: {max(errors):.2f}')"
        }
    ],
    "rw_scenario": "Forecast retail store daily sales for next 30 days using historical 2 years of data. The data has weekly patterns (lower on Mondays, peak on weekends), a monthly pay-cycle boost, and a gradual upward trend. Produce point forecasts and 80% prediction intervals.",
    "rw_code": "import pandas as pd\nimport numpy as np\nfrom sklearn.linear_model import Ridge\nfrom sklearn.preprocessing import StandardScaler\n\nnp.random.seed(0)\ndates = pd.date_range('2022-01-01', periods=730, freq='D')\ntrend = np.linspace(500, 700, 730)\nweekly = 40 * np.sin(2 * np.pi * np.arange(730) / 7 - np.pi)\nmonthly = 30 * np.sin(2 * np.pi * np.arange(730) / 30)\nnoise = np.random.normal(0, 15, 730)\ny = trend + weekly + monthly + noise\n\ndf = pd.DataFrame({'ds': dates, 'y': y})\ndf['t'] = np.arange(len(df))\ndf['dow'] = df['ds'].dt.dayofweek\ndf['dom'] = df['ds'].dt.day\nfor d in range(7): df[f'dow_{d}'] = (df['dow'] == d).astype(int)\n\nfeat_cols = ['t'] + [f'dow_{d}' for d in range(7)] + ['dom']\nX = df[feat_cols].values\ntrain = df[df['ds'] < '2023-07-01']; test = df[df['ds'] >= '2023-07-01']\nidx_tr = df['ds'] < '2023-07-01'\n\nsc = StandardScaler().fit(X[idx_tr])\nm = Ridge(alpha=1.0).fit(sc.transform(X[idx_tr]), y[idx_tr])\n\nresid = y[idx_tr] - m.predict(sc.transform(X[idx_tr]))\npred = m.predict(sc.transform(X[~idx_tr]))\nprint(f'Forecast RMSE: {np.sqrt(((y[~idx_tr]-pred)**2).mean()):.2f}')\nprint(f'80% PI: ±{1.28*resid.std():.2f}')",
    "practice": {
        "title": "Forecast Weekly Revenue with Confidence Intervals",
        "desc": "Given 2 years of weekly revenue data with trend and seasonality, build a feature-based Ridge model (lag features + time index + month dummies). Perform walk-forward validation with 4-week horizons. Report average RMSE and generate 80% prediction intervals using residual std.",
        "starter": "import pandas as pd\nimport numpy as np\nfrom sklearn.linear_model import Ridge\n\nnp.random.seed(7)\nweeks = pd.date_range('2022-01-03', periods=104, freq='W')\ntrend = np.linspace(10000, 15000, 104)\nseasonality = 1500 * np.sin(2 * np.pi * np.arange(104) / 52)\nnoise = np.random.normal(0, 300, 104)\ny = trend + seasonality + noise\ndf = pd.DataFrame({'ds': weeks, 'revenue': y})\n\n# TODO: Create features (t index, month dummies, lag-1)\n# TODO: Walk-forward cross-validation with 4-week horizon\n# TODO: Report average RMSE and 80% PI width\n"
    }
},
{
    "title": "12. Anomaly Detection in Time Series",
    "desc": "Detect outliers and anomalies in sequential data using statistical thresholds, isolation forests, and autoencoder-style reconstruction errors.",
    "examples": [
        {
            "label": "Z-score and IQR rolling anomaly detection",
            "code": "import pandas as pd\nimport numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nnp.random.seed(42)\ndates = pd.date_range('2024-01-01', periods=100, freq='D')\ny = np.sin(np.arange(100) * 0.3) * 10 + np.random.normal(0, 1, 100) + 50\n# Inject anomalies\ny[[20, 45, 70, 85]] += [25, -20, 30, -15]\n\ndf = pd.DataFrame({'ds': dates, 'y': y})\n\n# Rolling z-score\nwin = 14\ndf['roll_mean'] = df['y'].rolling(win, min_periods=1).mean()\ndf['roll_std']  = df['y'].rolling(win, min_periods=1).std().fillna(1)\ndf['zscore']    = (df['y'] - df['roll_mean']) / df['roll_std']\ndf['anomaly_z'] = df['zscore'].abs() > 2.5\n\nprint(f'Z-score anomalies: {df[\"anomaly_z\"].sum()} detected')\nprint(df[df['anomaly_z']][['ds','y','zscore']].to_string())\nfig, ax = plt.subplots(figsize=(12, 4))\nax.plot(df['ds'], df['y'], label='series')\nax.scatter(df[df['anomaly_z']]['ds'], df[df['anomaly_z']]['y'],\n           color='red', s=80, zorder=5, label='anomaly')\nax.set_title('Rolling Z-score Anomaly Detection'); ax.legend()\nplt.tight_layout(); plt.savefig('anomaly_zscore.png', dpi=80); plt.close(); print('Saved anomaly_zscore.png')"
        },
        {
            "label": "Isolation Forest for multivariate anomalies",
            "code": "import pandas as pd\nimport numpy as np\nfrom sklearn.ensemble import IsolationForest\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nnp.random.seed(42)\nn = 200\ndates = pd.date_range('2024-01-01', periods=n, freq='H')\ncpu    = np.random.normal(40, 10, n)\nmemory = cpu * 1.5 + np.random.normal(0, 5, n)\n# Inject anomalies\ncpu[[50, 100, 150]] = [95, 5, 98]\nmemory[[50, 100, 150]] = [30, 120, 25]\n\ndf = pd.DataFrame({'ds': dates, 'cpu': cpu, 'memory': memory})\nX = df[['cpu', 'memory']].values\n\niso = IsolationForest(contamination=0.05, random_state=42)\ndf['anomaly'] = iso.fit_predict(X) == -1\ndf['score']   = iso.score_samples(X)\n\nprint(f'Anomalies detected: {df[\"anomaly\"].sum()}')\nprint(df[df['anomaly']][['ds','cpu','memory','score']].to_string())\nfig, axes = plt.subplots(2, 1, figsize=(12, 6))\nfor i, col in enumerate(['cpu', 'memory']):\n    axes[i].plot(df['ds'], df[col], alpha=0.7)\n    axes[i].scatter(df[df['anomaly']]['ds'], df[df['anomaly']][col],\n                    color='red', s=60, zorder=5)\n    axes[i].set_ylabel(col)\nplt.suptitle('Isolation Forest Anomaly Detection'); plt.tight_layout()\nplt.savefig('anomaly_iforest.png', dpi=80); plt.close(); print('Saved anomaly_iforest.png')"
        },
        {
            "label": "LSTM autoencoder reconstruction error",
            "code": "import numpy as np\n\nnp.random.seed(42)\n# Simulate normal signal\nt = np.linspace(0, 20*np.pi, 500)\nnormal = np.sin(t) + 0.1 * np.random.randn(500)\n# Inject anomaly window\nanom = normal.copy()\nanom[200:220] += 5  # spike\n\n# Simple threshold-based reconstruction error (PCA substitute)\nfrom sklearn.decomposition import PCA\nfrom sklearn.preprocessing import StandardScaler\n\n# Create sliding windows\ndef make_windows(x, w=20):\n    return np.array([x[i:i+w] for i in range(len(x)-w)])\n\nX = make_windows(normal, 20)\nX_anom = make_windows(anom, 20)\n\nsc = StandardScaler().fit(X)\nX_sc = sc.transform(X)\nX_anom_sc = sc.transform(X_anom)\n\npca = PCA(n_components=5).fit(X_sc)\nrec = pca.inverse_transform(pca.transform(X_anom_sc))\nerrors = ((X_anom_sc - rec)**2).mean(axis=1)\n\nthreshold = np.percentile(errors, 95)\nprint(f'Reconstruction error threshold (95th pct): {threshold:.4f}')\nprint(f'Anomaly windows detected: {(errors > threshold).sum()}')\nprint(f'Max error at index: {errors.argmax()} (injected at 200:220)')"
        },
        {
            "label": "STL-based anomaly detection",
            "code": "import pandas as pd\nimport numpy as np\nfrom statsmodels.tsa.seasonal import STL\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nnp.random.seed(42)\ndates = pd.date_range('2023-01-01', periods=365, freq='D')\ntrend = np.linspace(0, 30, 365)\nseasonal = 10 * np.sin(2 * np.pi * np.arange(365) / 7)\nnoise = np.random.normal(0, 2, 365)\ny = trend + seasonal + noise\n\n# Inject point anomalies\ninjected = [80, 160, 250, 320]\ny_anom = y.copy()\nfor idx in injected:\n    y_anom[idx] += np.random.choice([-25, 25])\n\nseries = pd.Series(y_anom, index=dates)\nstl = STL(series, period=7, robust=True)\nresult = stl.fit()\nresidual = result.resid\n\nthresh = 3 * residual.std()\nanomalies = series[residual.abs() > thresh]\nprint(f'STL anomalies detected: {len(anomalies)}')\nprint(f'Injected at: {injected}')\nprint(f'Detected at: {list(anomalies.index.dayofyear)}')\nfig, axes = plt.subplots(2, 1, figsize=(12, 6))\naxes[0].plot(series.index, series, alpha=0.6); axes[0].scatter(anomalies.index, anomalies, color='red', s=60, zorder=5, label='anomaly'); axes[0].legend(); axes[0].set_title('STL Anomaly Detection')\naxes[1].plot(residual.index, residual); axes[1].axhline(thresh, color='r', linestyle='--'); axes[1].axhline(-thresh, color='r', linestyle='--'); axes[1].set_title('STL Residual')\nplt.tight_layout(); plt.savefig('stl_anomaly.png', dpi=80); plt.close(); print('Saved stl_anomaly.png')"
        }
    ],
    "rw_scenario": "Monitor server CPU usage (sampled every 5 minutes) to automatically alert when anomalies occur. The signal has daily patterns (low at night, high during business hours). You must detect both sudden spikes and sustained elevated periods while minimizing false alarms.",
    "rw_code": "import pandas as pd\nimport numpy as np\nfrom sklearn.ensemble import IsolationForest\n\nnp.random.seed(1)\n# 2 weeks of 5-min samples = 4032 points\nt = np.arange(4032)\ndaily = 20 * np.sin(2*np.pi*t / 288 - np.pi/2) + 50  # 288 samples/day\nnoise = np.random.normal(0, 3, 4032)\ncpu = np.clip(daily + noise, 5, 100)\n# Inject anomalies\ncpu[500:510]  += 40  # spike\ncpu[1200:1230] += 30  # sustained high\n\ntimes = pd.date_range('2024-01-01', periods=4032, freq='5min')\ndf = pd.DataFrame({'time': times, 'cpu': cpu})\ndf['hour'] = df['time'].dt.hour\ndf['roll_mean'] = df['cpu'].rolling(12).mean().fillna(method='bfill')\ndf['roll_std']  = df['cpu'].rolling(12).std().fillna(1)\n\n# Isolation Forest on features\nX = df[['cpu', 'hour', 'roll_mean', 'roll_std']].values\niso = IsolationForest(contamination=0.01, random_state=42)\ndf['anomaly'] = iso.fit_predict(X) == -1\nprint(f'Anomalies detected: {df[\"anomaly\"].sum()} of {len(df)} points ({df[\"anomaly\"].mean():.1%})')\nprint(df[df['anomaly']].groupby(df[df['anomaly']]['time'].dt.date)['anomaly'].count())",
    "practice": {
        "title": "Detect Order Volume Anomalies",
        "desc": "Given hourly e-commerce order counts with weekly seasonality, detect anomalies using rolling z-score (window=24h, threshold=3). Also apply Isolation Forest on (count, hour, day_of_week) features. Compare which method catches more of the injected spikes (3 injected anomalies) with fewer false positives.",
        "starter": "import pandas as pd\nimport numpy as np\nfrom sklearn.ensemble import IsolationForest\n\nnp.random.seed(99)\nhours = pd.date_range('2024-01-01', periods=336, freq='H')  # 2 weeks\nbase = 100 + 50 * np.sin(2*np.pi*np.arange(336)/24 - np.pi)\nnoise = np.random.normal(0, 8, 336)\norders = np.clip(base + noise, 0, None)\norders[[100, 200, 280]] += [150, -80, 200]  # inject anomalies\ndf = pd.DataFrame({'time': hours, 'orders': orders})\n\n# TODO: Rolling z-score anomaly detection (window=24, thresh=3)\n# TODO: Isolation Forest on (orders, hour, dayofweek)\n# TODO: Compare detected anomaly counts and false positive rates\n"
    }
},
{
    "title": "13. Neural Forecasting Fundamentals",
    "desc": "Apply LSTM, Temporal Convolutional Networks (TCN), and N-BEATS-style architectures using PyTorch or Keras for sequence forecasting tasks.",
    "examples": [
        {
            "label": "Univariate LSTM forecasting (NumPy / PyTorch-free)",
            "code": "import numpy as np\nfrom sklearn.linear_model import Ridge\nfrom sklearn.preprocessing import StandardScaler\n\n# Demonstrate the lag-feature approach that underlies RNN forecasting\nnp.random.seed(42)\nn = 300\nt = np.arange(n)\ny = np.sin(0.2*t) * 10 + 0.1*t + np.random.normal(0, 1, n)\n\ndef make_supervised(series, lags=10):\n    X, Y = [], []\n    for i in range(lags, len(series)):\n        X.append(series[i-lags:i])\n        Y.append(series[i])\n    return np.array(X), np.array(Y)\n\nX, Y = make_supervised(y, lags=20)\nsplit = int(0.8 * len(X))\nX_tr, X_te = X[:split], X[split:]\nY_tr, Y_te = Y[:split], Y[split:]\n\nsc_x = StandardScaler().fit(X_tr)\nsc_y = StandardScaler().fit(Y_tr.reshape(-1,1))\n\nmodel = Ridge(alpha=0.1)\nmodel.fit(sc_x.transform(X_tr), sc_y.transform(Y_tr.reshape(-1,1)).ravel())\n\npred_sc = model.predict(sc_x.transform(X_te))\npred = sc_y.inverse_transform(pred_sc.reshape(-1,1)).ravel()\n\nrmse = np.sqrt(((Y_te - pred)**2).mean())\nprint(f'Lag-20 linear model RMSE: {rmse:.3f}')\nprint(f'Baseline (mean) RMSE:     {np.sqrt(((Y_te - Y_tr.mean())**2).mean()):.3f}')\nprint('This is the feature-engineering equivalent of an LSTM cell state.')"
        },
        {
            "label": "Sequence-to-sequence multi-step forecasting",
            "code": "import numpy as np\nfrom sklearn.multioutput import MultiOutputRegressor\nfrom sklearn.ensemble import GradientBoostingRegressor\n\nnp.random.seed(42)\nn = 400\nt = np.arange(n)\ny = 20 * np.sin(0.1*t) + 0.05*t + np.random.normal(0, 2, n)\n\ndef make_seq2seq(series, lookback=30, horizon=7):\n    X, Y = [], []\n    for i in range(lookback, len(series) - horizon + 1):\n        X.append(series[i-lookback:i])\n        Y.append(series[i:i+horizon])\n    return np.array(X), np.array(Y)\n\nX, Y = make_seq2seq(y, lookback=30, horizon=7)\nsplit = int(0.8 * len(X))\nX_tr, X_te = X[:split], X[split:]\nY_tr, Y_te = Y[:split], Y[split:]\n\n# Multi-output regression (equivalent to decoder in seq2seq)\nmodel = MultiOutputRegressor(GradientBoostingRegressor(n_estimators=50, random_state=0))\nmodel.fit(X_tr, Y_tr)\npred = model.predict(X_te)\n\nrmse_by_step = np.sqrt(((Y_te - pred)**2).mean(axis=0))\nprint('RMSE by forecast horizon step:')\nfor step, r in enumerate(rmse_by_step, 1):\n    print(f'  Step {step}: {r:.3f}')\nprint(f'Overall RMSE: {rmse_by_step.mean():.3f}')"
        },
        {
            "label": "Attention-weighted feature importance for time series",
            "code": "import numpy as np\n\nnp.random.seed(42)\nn = 500\nt = np.arange(n)\ny = 15*np.sin(0.15*t) + 5*np.sin(0.05*t) + np.random.normal(0, 1, n)\n\ndef make_windows(series, w=20):\n    X = np.array([series[i-w:i] for i in range(w, len(series))])\n    Y = series[w:]\n    return X, Y\n\nX, Y = make_windows(y, 20)\n\n# Simulate attention: weight lags by their correlation with target\nfrom sklearn.linear_model import Ridge\nfrom sklearn.preprocessing import StandardScaler\n\nsc_x = StandardScaler().fit(X)\nsc_y = StandardScaler().fit(Y.reshape(-1,1))\nX_sc = sc_x.transform(X)\nY_sc = sc_y.transform(Y.reshape(-1,1)).ravel()\n\n# Attention weights = absolute Ridge coefficients (softmax)\nmodel = Ridge(alpha=0.01).fit(X_sc, Y_sc)\nraw_weights = np.abs(model.coef_)\nattention = raw_weights / raw_weights.sum()  # softmax-like\n\nprint('Attention weights by lag (most recent = lag 1):')\nfor lag in range(1, 6):\n    print(f'  Lag {lag:2d}: {attention[-lag]:.4f} ({\"high\" if attention[-lag] > attention.mean() else \"low\"})')\nprint(f'Top-3 most attended lags: {(-attention).argsort()[:3] + 1}')"
        },
        {
            "label": "N-BEATS-inspired basis expansion forecasting",
            "code": "import numpy as np\nfrom sklearn.linear_model import Ridge\n\nnp.random.seed(0)\nn = 300\nt = np.arange(n)\ny = 10*np.sin(0.2*t) + 0.1*t + np.random.normal(0, 1.5, n)\n\n# N-BEATS idea: decompose into trend + seasonality bases\ndef trend_basis(T, degree=3):\n    \"\"\"Polynomial trend basis for N-BEATS trend block.\"\"\"\n    t_norm = np.linspace(0, 1, T)\n    return np.column_stack([t_norm**k for k in range(degree+1)])\n\ndef fourier_basis(T, harmonics=5):\n    \"\"\"Fourier seasonality basis for N-BEATS seasonality block.\"\"\"\n    t = np.linspace(0, 2*np.pi, T)\n    cols = []\n    for k in range(1, harmonics+1):\n        cols.extend([np.cos(k*t), np.sin(k*t)])\n    return np.column_stack(cols)\n\nLB = 30  # lookback\nX, Y = [], []\nfor i in range(LB, n - 7):\n    window = y[i-LB:i]\n    trend_feats  = trend_basis(LB, degree=2).T @ window / LB\n    season_feats = fourier_basis(LB, harmonics=3).T @ window / LB\n    X.append(np.concatenate([trend_feats, season_feats]))\n    Y.append(y[i:i+7].mean())\nX, Y = np.array(X), np.array(Y)\n\nsplit = int(0.8*len(X))\nmodel = Ridge(alpha=0.1).fit(X[:split], Y[:split])\npred  = model.predict(X[split:])\nrmse  = np.sqrt(((Y[split:] - pred)**2).mean())\nprint(f'N-BEATS basis expansion RMSE: {rmse:.3f}')\nprint(f'Trend features: {trend_basis(LB, 2).shape[1]}, Fourier features: {fourier_basis(LB, 3).shape[1]}')"
        }
    ],
    "rw_scenario": "Build a multi-step electricity demand forecasting system that predicts next 24 hours (hourly) using the previous 7 days of data. Features include lagged values, hour-of-day, day-of-week, temperature. Compare gradient boosting seq2seq vs naive persistence baseline.",
    "rw_code": "import numpy as np\nimport pandas as pd\nfrom sklearn.multioutput import MultiOutputRegressor\nfrom sklearn.ensemble import GradientBoostingRegressor\n\nnp.random.seed(5)\nhours = pd.date_range('2023-01-01', periods=8760, freq='H')\ndaily = 500 + 200*np.sin(2*np.pi*np.arange(8760)/24 - np.pi)\nweekly= 50 *np.sin(2*np.pi*np.arange(8760)/(24*7))\nnoise = np.random.normal(0, 20, 8760)\ndemand = daily + weekly + noise\n\ndf = pd.DataFrame({'time': hours, 'demand': demand, 'hour': hours.hour, 'dow': hours.dayofweek})\n\nLB, H = 24*7, 24  # 7-day lookback, 24h horizon\nX, Y = [], []\nfor i in range(LB, len(df)-H):\n    feats = list(df['demand'].values[i-LB:i])\n    feats += [df['hour'].iloc[i], df['dow'].iloc[i]]\n    X.append(feats)\n    Y.append(df['demand'].values[i:i+H])\nX, Y = np.array(X), np.array(Y)\n\nsplit = int(0.85*len(X))\nmodel = MultiOutputRegressor(GradientBoostingRegressor(n_estimators=30, random_state=0), n_jobs=-1)\nmodel.fit(X[:split], Y[:split])\npred = model.predict(X[split:])\nrmse = np.sqrt(((Y[split:]-pred)**2).mean())\nbaseline = np.sqrt(((Y[split:]-Y[split-1:-1])**2).mean())  # persistence\nprint(f'GBM RMSE: {rmse:.2f}, Persistence RMSE: {baseline:.2f}')\nprint(f'Improvement: {(baseline-rmse)/baseline:.1%}')",
    "practice": {
        "title": "Seq2Seq Solar Power Forecasting",
        "desc": "Using 1 year of hourly solar generation data (sinusoidal with daily pattern, zero at night), build a seq2seq GBM model with 48-hour lookback and 12-hour horizon. Compare RMSE for the first 4 steps vs last 4 steps. Also implement a simple attention weighting by computing per-lag correlations with the target.",
        "starter": "import numpy as np\nimport pandas as pd\nfrom sklearn.multioutput import MultiOutputRegressor\nfrom sklearn.ensemble import GradientBoostingRegressor\n\nnp.random.seed(3)\nhours = pd.date_range('2023-01-01', periods=8760, freq='H')\nraw = np.maximum(0, np.sin(2*np.pi*np.arange(8760)/24 - np.pi/2))\nsolar = raw * 1000 + np.random.normal(0, 30, 8760)\ndf = pd.DataFrame({'time': hours, 'solar': solar})\n\nLB, H = 48, 12\n# TODO: Build (X, Y) windows with lookback=48, horizon=12\n# TODO: Train GBM MultiOutputRegressor\n# TODO: Report RMSE for steps 1-4 vs steps 9-12\n# TODO: Compute attention weights via per-lag correlation\n"
    }
},

    {
        "title": "14. Wavelet Analysis for Time Series",
        "examples": [
            {
                "label": "Discrete Wavelet Transform (DWT)",
                "code": "import numpy as np\nimport pywt\nnp.random.seed(0)\nt = np.linspace(0, 8*np.pi, 512)\nsignal = (np.sin(t) + 0.5*np.sin(5*t) + np.random.normal(0, 0.2, 512))\nwavelet = \'db4\'\nlevel = 4\ncoeffs = pywt.wavedec(signal, wavelet, level=level)\nprint(f\"Decomposition levels: {len(coeffs)-1}\")\nprint(f\"Approximation coeff shape: {coeffs[0].shape}\")\nfor i, c in enumerate(coeffs[1:], 1):\n    print(f\"  Detail level {i}: shape={c.shape}, energy={np.sum(c**2):.2f}\")\n# Denoise: zero out small detail coefficients\nthreshold = 0.3\ncoeffs_denoised = [coeffs[0]] + [pywt.threshold(c, threshold, mode=\'soft\') for c in coeffs[1:]]\ndenoised = pywt.waverec(coeffs_denoised, wavelet)[:len(signal)]\nmse = np.mean((signal - denoised)**2)\nprint(f\"Denoising MSE: {mse:.4f}\")"
            },
            {
                "label": "Continuous Wavelet Transform (CWT) Scalogram",
                "code": "import numpy as np\nimport pywt\nnp.random.seed(1)\nfs = 100  # Hz\nt = np.arange(0, 4, 1/fs)\n# Chirp: frequency increases from 5 to 20 Hz\nfreq = 5 + 15*t/4\nsignal = np.sin(2*np.pi*freq*t) + np.random.normal(0, 0.1, len(t))\nwidths = np.arange(1, 64)\ncwt_matrix, freqs = pywt.cwt(signal, widths, \'morl\', sampling_period=1/fs)\npower = np.abs(cwt_matrix)**2\n# Peak frequency at start vs end\nt_start = slice(0, 50); t_end = slice(350, 400)\npeak_freq_start = freqs[np.argmax(power[:, t_start].mean(axis=1))]\npeak_freq_end   = freqs[np.argmax(power[:, t_end].mean(axis=1))]\nprint(f\"Dominant frequency (start): {peak_freq_start:.1f} Hz\")\nprint(f\"Dominant frequency (end):   {peak_freq_end:.1f} Hz\")"
            },
            {
                "label": "Wavelet-Based Anomaly Detection",
                "code": "import numpy as np\nimport pywt\nnp.random.seed(42)\nn = 1000\nts = np.sin(2*np.pi*np.arange(n)/50) + np.random.normal(0, 0.1, n)\n# Inject anomalies\nts[300:310] += 3.0\nts[700] -= 4.0\n# DWT anomaly detection via reconstruction error per window\ncoeffs = pywt.wavedec(ts, \'haar\', level=3)\n# Zero out detail at level 1 (high-freq noise)\ncoeffs[1] = np.zeros_like(coeffs[1])\nreconstructed = pywt.waverec(coeffs, \'haar\')[:n]\nresiduals = np.abs(ts - reconstructed)\nthreshold = residuals.mean() + 3*residuals.std()\nanomaly_idx = np.where(residuals > threshold)[0]\nprint(f\"Anomalies detected at indices: {anomaly_idx[:10]}\")\nprint(f\"True anomaly regions: 300-310, 700\")"
            }
        ],
        "rw_scenario": "Manufacturing: use wavelet decomposition to separate machine vibration signals by frequency band, detect bearing faults (high-frequency detail) while ignoring normal operational frequencies.",
        "rw_code": "import numpy as np\nimport pywt\nnp.random.seed(7)\nfs = 1000  # 1 kHz sampling\nt = np.arange(0, 2, 1/fs)  # 2 seconds\n# Normal operation: 10 Hz fundamental + harmonics\nnormal = (np.sin(2*np.pi*10*t) + 0.3*np.sin(2*np.pi*20*t) +\n          np.random.normal(0, 0.05, len(t)))\n# Fault: adds 150 Hz bearing frequency\nfault  = normal + 0.5*np.sin(2*np.pi*150*t)\nfor label, sig in [(\'Normal\', normal), (\'Fault\', fault)]:\n    coeffs = pywt.wavedec(sig, \'db4\', level=5)\n    # Level 1 detail captures highest frequencies\n    hf_energy = np.sum(coeffs[1]**2) / np.sum(sig**2)\n    print(f\"{label}: high-freq energy ratio = {hf_energy:.4f}\")\n    energies = [np.sum(c**2) / np.sum(sig**2) for c in coeffs]\n    print(f\"  Energy by level: \" + \", \".join(f\"L{i}={e:.3f}\" for i, e in enumerate(energies)))",
        "practice": {
            "title": "EEG Brainwave Analysis",
            "desc": "Given a simulated EEG signal (1-second, 256 Hz) with delta (1-4 Hz), alpha (8-13 Hz), and beta (13-30 Hz) components, use wavelet decomposition to extract each band. Report the relative power of each band. Inject a 50ms epileptic spike at t=0.5s and detect it using wavelet residuals.",
            "starter": "import numpy as np\nimport pywt\nfs = 256  # Hz\nt = np.arange(0, 1, 1/fs)\n# Multi-band EEG signal\ndelta = 0.5 * np.sin(2*np.pi*2*t)\nalpha = 0.3 * np.sin(2*np.pi*10*t)\nbeta  = 0.2 * np.sin(2*np.pi*20*t)\nnoise = np.random.normal(0, 0.05, len(t))\neeg = delta + alpha + beta + noise\n# Inject spike\nspike_start = int(0.5 * fs)\neeg[spike_start:spike_start+13] += 3.0\n# TODO: DWT decomposition with \'db4\', level=5\n# TODO: Identify which detail levels correspond to each EEG band\n# TODO: Compute relative band powers\n# TODO: Detect spike using reconstruction error\n"
        }
    },
    {
        "title": "15. Multivariate Time Series & VAR Models",
        "examples": [
            {
                "label": "Vector Autoregression (VAR)",
                "code": "import numpy as np\nimport pandas as pd\nfrom statsmodels.tsa.vector_ar.var_model import VAR\nnp.random.seed(42)\nn = 200\ne1, e2 = np.random.normal(0, 1, n), np.random.normal(0, 1, n)\ny1, y2 = np.zeros(n), np.zeros(n)\nfor t in range(1, n):\n    y1[t] = 0.6*y1[t-1] + 0.2*y2[t-1] + e1[t]\n    y2[t] = 0.1*y1[t-1] + 0.7*y2[t-1] + e2[t]\ndf = pd.DataFrame({\'y1\': y1, \'y2\': y2})\nmodel = VAR(df)\nresults = model.fit(maxlags=4, ic=\'aic\')\nprint(f\"Selected lag order: {results.k_ar}\")\nforecast = results.forecast(df.values[-results.k_ar:], steps=5)\nprint(\"5-step forecast:\"); print(forecast.round(3))"
            },
            {
                "label": "Granger Causality Test",
                "code": "import numpy as np\nimport pandas as pd\nfrom statsmodels.tsa.stattools import grangercausalitytests\nnp.random.seed(1)\nn = 300\neps1 = np.random.normal(0, 1, n)\neps2 = np.random.normal(0, 1, n)\nx = np.zeros(n); y = np.zeros(n)\nfor t in range(2, n):\n    x[t] = 0.5*x[t-1] + eps1[t]\n    y[t] = 0.4*x[t-1] + 0.3*y[t-1] + eps2[t]  # x Granger-causes y\ndf = pd.DataFrame({\'y\': y, \'x\': x})\nmax_lag = 4\nprint(\"Granger causality (x -> y):\")\nres = grangercausalitytests(df[[\'y\',\'x\']], maxlag=max_lag, verbose=False)\nfor lag, r in res.items():\n    f_stat = r[0][\'ssr_ftest\'][0]\n    p_val  = r[0][\'ssr_ftest\'][1]\n    print(f\"  Lag {lag}: F={f_stat:.3f}, p={p_val:.4f}\")"
            },
            {
                "label": "Cointegration & Error Correction",
                "code": "import numpy as np\nimport pandas as pd\nfrom statsmodels.tsa.stattools import coint\nfrom statsmodels.regression.linear_model import OLS\nnp.random.seed(5)\nn = 500\ncommon_trend = np.cumsum(np.random.normal(0, 1, n))\ny1 = common_trend + np.random.normal(0, 0.5, n)\ny2 = 0.8 * common_trend + 1.2 + np.random.normal(0, 0.5, n)\nscore, pvalue, _ = coint(y1, y2)\nprint(f\"Cointegration test: t={score:.4f}, p={pvalue:.4f}\")\n# Estimate cointegrating vector\nbeta = OLS(y1, np.column_stack([np.ones(n), y2])).fit().params\nspread = y1 - beta[1]*y2 - beta[0]\nz_spread = (spread - spread.mean()) / spread.std()\nprint(f\"Spread mean-reversion: current z-score = {z_spread[-1]:.3f}\")"
            }
        ],
        "rw_scenario": "Macroeconomic forecasting: model GDP, inflation, and interest rates jointly using VAR to capture cross-variable dynamics and produce scenario forecasts for monetary policy analysis.",
        "rw_code": "import numpy as np\nimport pandas as pd\nfrom statsmodels.tsa.vector_ar.var_model import VAR\nfrom statsmodels.tsa.stattools import grangercausalitytests\nnp.random.seed(10)\nn = 120  # 10 years monthly\n# Simulate: interest rate affects inflation with lag, both affect GDP\nir = np.cumsum(np.random.normal(0, 0.1, n)) + 3.0\ninf = 0.5*np.roll(ir, 2) + np.cumsum(np.random.normal(0, 0.05, n)) + 2.0\ngdp = -0.3*np.roll(ir, 3) + 0.4*np.roll(inf, 1) + np.cumsum(np.random.normal(0, 0.08, n)) + 2.5\ndf = pd.DataFrame({\'gdp\': gdp, \'inflation\': inf, \'interest_rate\': ir})\ndf = df.diff().dropna()  # difference to achieve stationarity\nmodel = VAR(df)\nres = model.fit(maxlags=6, ic=\'aic\')\nprint(f\"VAR lag order: {res.k_ar}\")\nforecast = res.forecast(df.values[-res.k_ar:], steps=12)\nprint(f\"12-month GDP forecast range: {forecast[:,0].min():.3f} to {forecast[:,0].max():.3f}\")\n# Impulse response\nirf = res.irf(10)\nprint(f\"GDP response to interest shock at lag 3: {irf.orth_irfs[3, 0, 2]:.4f}\")",
        "practice": {
            "title": "Pairs Trading Signal",
            "desc": "Using two simulated stock price series that are cointegrated (sharing a common random walk), implement a pairs trading strategy: (1) verify cointegration with Engle-Granger test, (2) estimate the spread, (3) generate long/short signals when z-score > 2 or < -2, (4) backtest and report Sharpe ratio and max drawdown.",
            "starter": "import numpy as np\nimport pandas as pd\nfrom statsmodels.tsa.stattools import coint\nfrom statsmodels.regression.linear_model import OLS\nnp.random.seed(3)\nn = 500\ncommon = np.cumsum(np.random.normal(0, 1, n))\nprice_a = common + np.random.normal(0, 0.5, n) + 50\nprice_b = 0.9*common + np.random.normal(0, 0.5, n) + 45\n# TODO: Cointegration test\n# TODO: Compute hedge ratio and spread\n# TODO: Z-score of spread\n# TODO: Generate trading signals (long A-short B when z<-2, vice versa)\n# TODO: Compute daily P&L, Sharpe ratio, max drawdown\n"
        }
    },
    {
        "title": "16. Real-Time Streaming & Online Learning",
        "examples": [
            {
                "label": "Online Learning with River",
                "code": "# pip install river\nfrom river import linear_model, preprocessing, metrics, stream\nimport numpy as np\nnp.random.seed(0)\nn = 1000\nX_data = np.column_stack([np.random.randn(n), np.arange(n)/n])\ny_data = 3*X_data[:,0] - 2*X_data[:,1] + 0.5 + np.random.normal(0, 0.3, n)\nmodel = preprocessing.StandardScaler() | linear_model.LinearRegression()\nmetric = metrics.RMSE()\nfor i, (xi, yi) in enumerate(zip(X_data, y_data)):\n    x_dict = {\'f0\': xi[0], \'f1\': xi[1]}\n    y_pred = model.predict_one(x_dict)\n    if y_pred is not None:\n        metric.update(yi, y_pred)\n    model.learn_one(x_dict, yi)\n    if i % 200 == 0 and y_pred is not None:\n        print(f\"  n={i}: running RMSE={metric.get():.4f}\")\nprint(f\"Final RMSE: {metric.get():.4f}\")"
            },
            {
                "label": "Concept Drift Detection (ADWIN)",
                "code": "# pip install river\nfrom river import drift\nimport numpy as np\nnp.random.seed(7)\ndetector = drift.ADWIN()\nstream = np.concatenate([\n    np.random.normal(0, 1, 500),\n    np.random.normal(3, 1, 500)  # sudden drift at t=500\n])\ndrifts = []\nfor i, x in enumerate(stream):\n    detector.update(x)\n    if detector.drift_detected:\n        drifts.append(i)\n        detector = drift.ADWIN()  # reset\nprint(f\"Drift detected at sample(s): {drifts}\")"
            },
            {
                "label": "Sliding Window Streaming Statistics",
                "code": "import numpy as np\nfrom collections import deque\nclass StreamStats:\n    def __init__(self, window=100):\n        self.w = deque(maxlen=window)\n        self.n = 0\n    def update(self, x):\n        self.w.append(x)\n        self.n += 1\n        return self.mean(), self.std()\n    def mean(self): return np.mean(self.w)\n    def std(self):  return np.std(self.w, ddof=1) if len(self.w) > 1 else 0.0\nnp.random.seed(1)\nss = StreamStats(window=50)\nfor i in range(300):\n    val = np.random.normal(5 if i < 150 else 8, 1)\n    mean, std = ss.update(val)\n    if i % 50 == 49:\n        print(f\"  t={i+1}: window mean={mean:.3f}, std={std:.3f}\")"
            }
        ],
        "rw_scenario": "IoT sensor network: process a continuous stream of temperature readings at 10 Hz from 50 sensors, detect anomalies in real-time using sliding window statistics, and adapt the baseline when ADWIN detects environmental regime changes.",
        "rw_code": "import numpy as np\nfrom collections import deque\nnp.random.seed(42)\nn_sensors, n_steps = 5, 1000\nwindow = 60\nbaselines = [deque(maxlen=window) for _ in range(n_sensors)]\nalerts = {i: [] for i in range(n_sensors)}\n# Inject drift at step 600 for sensor 2\nfor t in range(n_steps):\n    readings = np.random.normal(22, 0.5, n_sensors)\n    if t >= 600:\n        readings[2] += 4.0  # sensor 2 drifts\n    for s in range(n_sensors):\n        baselines[s].append(readings[s])\n        if len(baselines[s]) >= 20:\n            mu = np.mean(baselines[s])\n            sigma = np.std(baselines[s], ddof=1)\n            z = (readings[s] - mu) / max(sigma, 1e-6)\n            if abs(z) > 3:\n                alerts[s].append(t)\nfor s in range(n_sensors):\n    if alerts[s]:\n        print(f\"Sensor {s}: {len(alerts[s])} alerts, first at t={alerts[s][0]}\")\n    else:\n        print(f\"Sensor {s}: no alerts\")",
        "practice": {
            "title": "Real-Time Fraud Score Streaming",
            "desc": "Simulate a stream of 2000 credit card transactions (amount, time_since_last, is_weekend). Use online logistic regression (River) trained incrementally. At t=1000, inject a concept drift (fraudsters change behavior). Detect drift using ADWIN on prediction errors. Report AUC before and after drift, and adaptation speed.",
            "starter": "# pip install river\nfrom river import linear_model, preprocessing, metrics, drift, stream as rv_stream\nimport numpy as np\nnp.random.seed(99)\nn = 2000\n# Generate transactions\namounts = np.random.exponential(50, n)\ngaps = np.random.exponential(10, n)\nis_weekend = np.random.randint(0, 2, n)\n# Fraud rule: changes at t=1000\nfraud_prob_before = 1 / (1 + np.exp(-(amounts/100 - 0.5)))\nfraud_prob_after  = 1 / (1 + np.exp(-(gaps/5 - 1.0)))  # different pattern\ny = np.array([\n    np.random.binomial(1, fraud_prob_before[i]) if i < 1000\n    else np.random.binomial(1, fraud_prob_after[i])\n    for i in range(n)\n])\n# TODO: Online logistic regression with River\n# TODO: ADWIN drift detection on binary prediction errors\n# TODO: Report AUC in windows before drift, at drift, after adaptation\n"
        }
    },
{
"title": "17. Seasonal Decomposition & STL",
"desc": "Time series decompose into Trend, Seasonality, and Residual components. STL (Seasonal-Trend decomposition using LOESS) is robust to outliers and handles arbitrary seasonality. Use it before forecasting to understand your signal.",
"examples": [
        {"label": "Classical decomposition with statsmodels", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.seasonal import seasonal_decompose\n\nnp.random.seed(42)\nperiods = 120\ndates = pd.date_range(\'2015-01\', periods=periods, freq=\'MS\')\ntrend = np.linspace(100, 160, periods)\nseasonal = 15 * np.sin(2 * np.pi * np.arange(periods) / 12)\nnoise = np.random.normal(0, 5, periods)\nts = pd.Series(trend + seasonal + noise, index=dates)\n\nresult = seasonal_decompose(ts, model=\'additive\', period=12)\n\nprint(\"Decomposition components:\")\nprint(f\"  Trend range:    [{result.trend.dropna().min():.1f}, {result.trend.dropna().max():.1f}]\")\nprint(f\"  Seasonal range: [{result.seasonal.min():.2f}, {result.seasonal.max():.2f}]\")\nprint(f\"  Residual std:   {result.resid.dropna().std():.3f}\")\n\n# Seasonal indices\nseasonal_idx = result.seasonal[:12]\nfor month, val in zip(range(1, 13), seasonal_idx):\n    print(f\"  Month {month:2d}: {val:+.2f}\")"},
        {"label": "STL decomposition (robust, flexible seasonality)", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.seasonal import STL\n\nnp.random.seed(0)\nn = 156  # 13 years monthly\ndates = pd.date_range(\'2010-01\', periods=n, freq=\'MS\')\ntrend = np.linspace(50, 120, n) + 0.3 * np.sin(np.linspace(0, 4*np.pi, n)) * 10\nseasonal = 20 * np.sin(2 * np.pi * np.arange(n) / 12) +            8  * np.sin(2 * np.pi * np.arange(n) / 6)\n# Inject outliers\nnoise = np.random.normal(0, 3, n)\noutliers = np.zeros(n)\noutliers[[30, 60, 90]] = 40\nts = pd.Series(trend + seasonal + noise + outliers, index=dates)\n\nstl = STL(ts, period=12, robust=True)\nres = stl.fit()\n\nprint(f\"STL decomposition of {n}-period series:\")\nprint(f\"  Trend variance:    {res.trend.var():.2f}\")\nprint(f\"  Seasonal variance: {res.seasonal.var():.2f}\")\nprint(f\"  Residual variance: {res.resid.var():.2f}\")\nprint(f\"  Seasonal strength: {max(0, 1 - res.resid.var()/(res.seasonal+res.resid).var()):.3f}\")\nprint(f\"  Trend strength:    {max(0, 1 - res.resid.var()/(res.trend+res.resid).var()):.3f}\")"},
        {"label": "Trend strength, seasonality strength, and change points", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.seasonal import STL\n\nnp.random.seed(7)\n# Monthly retail sales with change point at month 60\nn = 120\nt = np.arange(n)\ntrend = np.where(t < 60, 100 + t*0.5, 130 + (t-60)*1.2)\nseasonal = 25 * np.sin(2*np.pi*t/12)\nnoise = np.random.normal(0, 4, n)\nts = pd.Series(trend + seasonal + noise,\n               index=pd.date_range(\'2014-01\', periods=n, freq=\'MS\'))\n\nstl = STL(ts, period=12, robust=True)\nres = stl.fit()\n\n# Detect change point: where residuals spike\nresid_rolling_std = pd.Series(res.resid).rolling(6).std()\nchange_pt = resid_rolling_std.idxmax()\nprint(f\"Largest residual volatility at index: {change_pt}\")\n\n# Year-over-year growth from trend\nyoy = pd.Series(res.trend).pct_change(12) * 100\nprint(f\"\\nYear-over-year trend growth (last 3):\")\nfor i in [-3, -2, -1]:\n    print(f\"  Month {n+i}: {yoy.iloc[i]:.2f}%\")\n\n# Identify peak and trough season\nmonthly_seasonal = [res.seasonal[i::12].mean() for i in range(12)]\npeak   = np.argmax(monthly_seasonal) + 1\ntrough = np.argmin(monthly_seasonal) + 1\nprint(f\"\\nPeak season: month {peak}, Trough: month {trough}\")"}
    ],
"rw_scenario": "A retail analyst decomposes 5 years of monthly e-commerce sales using STL to isolate the holiday spike (seasonality) from long-term growth (trend) before building a forecast model.",
"rw_code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.seasonal import STL\n\nnp.random.seed(42)\nn = 60\ndates = pd.date_range(\'2019-01\', periods=n, freq=\'MS\')\ntrend    = 1000 + np.linspace(0, 500, n)\nseasonal = 300 * np.sin(2*np.pi*np.arange(n)/12) +            100 * (np.arange(n) % 12 == 11)   # Dec spike\nnoise    = np.random.normal(0, 30, n)\nsales    = pd.Series(trend + seasonal + noise, index=dates)\n\nstl = STL(sales, period=12, robust=True)\nres = stl.fit()\n\nprint(\"Retail Sales Decomposition:\")\nprint(f\"  Avg monthly trend growth: ${(res.trend.diff().dropna().mean()):.1f}\")\nprint(f\"  Peak seasonal boost: ${res.seasonal.max():.0f}\")\nprint(f\"  Residual RMSE: ${np.sqrt((res.resid**2).mean()):.1f}\")\n\n# Deseasonalized series for cleaner trend analysis\ndeseas = sales - res.seasonal\nprint(f\"  Deseasonalized range: [{deseas.min():.0f}, {deseas.max():.0f}]\")",
"practice": {
    "title": "Custom STL Pipeline",
    "desc": "Generate 5 years of weekly sales data (trend + two seasonalities: annual 52-week and quarterly 13-week + noise). Apply STL with period=52. Extract and print: (1) Overall trend slope (slope of linear fit to trend component), (2) Peak week of the year seasonally, (3) Percentage of variance explained by trend, seasonal, and residual components.",
    "starter": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.seasonal import STL\nfrom scipy import stats as sp_stats\n\nnp.random.seed(42)\nn = 260  # 5 years weekly\nt = np.arange(n)\ntrend    = 500 + t * 0.8\nseasonal = 80 * np.sin(2*np.pi*t/52) + 30 * np.sin(2*np.pi*t/13)\nnoise    = np.random.normal(0, 20, n)\nts = pd.Series(trend + seasonal + noise,\n               index=pd.date_range(\'2019-01-07\', periods=n, freq=\'W\'))\n\nstl = STL(ts, period=52, robust=True)\nres = stl.fit()\n\n# (1) trend slope via linear regression on trend component\n# (2) peak week (argmax of first 52 seasonal values)\n# (3) variance decomposition\ntotal_var = ts.var()\n# TODO: compute each component\'s share\n"
}
},

{
"title": "18. Stationarity Testing & ARIMA Preparation",
"desc": "ARIMA requires a stationary series (constant mean/variance). ADF and KPSS tests check stationarity. Differencing and log transforms achieve it. ACF/PACF plots reveal AR and MA orders.",
"examples": [
        {"label": "ADF and KPSS stationarity tests", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.stattools import adfuller, kpss\n\nnp.random.seed(42)\nn = 200\nt = np.arange(n)\n\nseries = {\n    \'Random Walk\':    np.cumsum(np.random.randn(n)),            # non-stationary\n    \'Stationary AR1\': np.zeros(n),                              # stationary\n    \'Trend + Noise\':  2 + 0.05*t + np.random.randn(n),         # non-stationary (trend)\n}\nfor i in range(1, n):\n    series[\'Stationary AR1\'][i] = 0.7*series[\'Stationary AR1\'][i-1] + np.random.randn()\n\nprint(f\"{\'Series\':16s}  {\'ADF p\':>8s}  {\'ADF stat\':>9s}  {\'KPSS p\':>8s}  {\'Stationary?\'}\")\nprint(\'-\' * 60)\nfor name, data in series.items():\n    adf_stat, adf_p, *_ = adfuller(data, autolag=\'AIC\')\n    try:\n        kpss_stat, kpss_p, *_ = kpss(data, regression=\'c\', nlags=\'auto\')\n    except Exception:\n        kpss_p = 0.01\n    # Stationary: ADF rejects H0 (p<0.05) AND KPSS fails to reject H0 (p>0.05)\n    is_stat = (adf_p < 0.05) and (kpss_p > 0.05)\n    print(f\"{name:16s}  {adf_p:8.4f}  {adf_stat:9.4f}  {kpss_p:8.4f}  {is_stat}\")"},
        {"label": "Differencing, log transform, and Box-Cox", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.stattools import adfuller\nfrom scipy.stats import boxcox\n\nnp.random.seed(0)\nn = 150\nt = np.arange(n)\n\n# Non-stationary: trending with heteroskedastic variance\nts = pd.Series(np.exp(0.02*t + np.cumsum(np.random.randn(n)*0.2)) * 100)\n\ndef adf_pvalue(x):\n    return adfuller(x.dropna(), autolag=\'AIC\')[1]\n\nprint(f\"Original:            ADF p={adf_pvalue(ts):.4f} (non-stationary)\")\n\n# Log transform (stabilizes variance)\nts_log = np.log(ts)\nprint(f\"Log transform:       ADF p={adf_pvalue(ts_log):.4f}\")\n\n# First difference (removes linear trend)\nts_diff1 = ts.diff()\nprint(f\"First difference:    ADF p={adf_pvalue(ts_diff1):.4f}\")\n\n# Log + first difference (common for financial series)\nts_log_diff = ts_log.diff()\nprint(f\"Log + diff:          ADF p={adf_pvalue(ts_log_diff):.4f}\")\n\n# Seasonal difference (lag=12 for monthly)\nts_sdiff = ts.diff(12)\nprint(f\"Seasonal diff (12):  ADF p={adf_pvalue(ts_sdiff):.4f}\")"},
        {"label": "ACF, PACF, and identifying ARIMA order", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.stattools import acf, pacf\nfrom statsmodels.tsa.arima_process import ArmaProcess\n\nnp.random.seed(42)\nn = 300\n\n# Generate AR(2) process: phi1=0.6, phi2=-0.3\nar_params = np.array([1, -0.6, 0.3])   # AR coefficients (sign convention)\nma_params = np.array([1])\nar2_process = ArmaProcess(ar_params, ma_params)\nar2_data = ar2_process.generate_sample(nsample=n)\n\n# Generate MA(1) process\nar_params2 = np.array([1])\nma_params2 = np.array([1, 0.8])\nma1_process = ArmaProcess(ar_params2, ma_params2)\nma1_data = ma1_process.generate_sample(nsample=n)\n\nfor name, data in [(\'AR(2)\', ar2_data), (\'MA(1)\', ma1_data)]:\n    acf_vals  = acf(data,  nlags=10, fft=True)[1:6]  # skip lag 0\n    pacf_vals = pacf(data, nlags=10)[1:6]\n    conf = 1.96 / np.sqrt(n)\n    print(f\"\\n{name} — PACF cutoff suggests AR order; ACF cutoff suggests MA order:\")\n    print(f\"  ACF  lags 1-5: {acf_vals.round(3)}\")\n    print(f\"  PACF lags 1-5: {pacf_vals.round(3)}\")\n    print(f\"  95% conf band: ±{conf:.3f}\")\n    ar_order  = sum(abs(pacf_vals) > conf)\n    ma_order  = sum(abs(acf_vals)  > conf)\n    print(f\"  Suggested: AR order={ar_order}, MA order={ma_order}\")"}
    ],
"rw_scenario": "A commodity trader checks whether monthly aluminium prices are stationary before applying ARIMA. ADF fails to reject non-stationarity; first-differencing the log prices produces a stationary series with ACF suggesting MA(1).",
"rw_code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.stattools import adfuller, kpss, acf, pacf\n\nnp.random.seed(10)\n# Simulate commodity prices (random walk with drift)\nn = 120\nprices = pd.Series(\n    np.exp(np.cumsum(np.random.normal(0.005, 0.04, n))) * 1800,\n    index=pd.date_range(\'2014-01\', periods=n, freq=\'MS\'),\n    name=\'Aluminium_USD_t\')\n\ndef check_stationarity(series, name):\n    adf_stat, adf_p, *_ = adfuller(series.dropna(), autolag=\'AIC\')\n    print(f\"{name:25s}: ADF p={adf_p:.4f} {\'[stationary]\' if adf_p < 0.05 else \'[non-stationary]\'}\")\n    return adf_p < 0.05\n\ncheck_stationarity(prices, \'Level prices\')\ncheck_stationarity(np.log(prices), \'Log prices\')\nlog_diff = np.log(prices).diff().dropna()\ncheck_stationarity(log_diff, \'Log-differenced\')\n\nacf_vals  = acf(log_diff,  nlags=8)[1:]\npacf_vals = pacf(log_diff, nlags=8)[1:]\nconf = 1.96 / np.sqrt(len(log_diff))\nprint(f\"\\nACF  lags 1-8: {acf_vals.round(3)}\")\nprint(f\"PACF lags 1-8: {pacf_vals.round(3)}\")\nprint(f\"Suggested ARIMA(p,1,q): p={sum(abs(pacf_vals[:4])>conf)}, q={sum(abs(acf_vals[:4])>conf)}\")",
"practice": {
    "title": "Automated Stationarity Pipeline",
    "desc": "Write a function make_stationary(ts, max_diffs=2) that: (1) Tests ADF on the original series, (2) If non-stationary, applies log transform (if all positive) and re-tests, (3) If still non-stationary, applies first differencing, (4) Repeats up to max_diffs times, (5) Returns the stationary series, number of differences applied, and whether log was used.",
    "starter": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.stattools import adfuller\n\ndef make_stationary(ts, max_diffs=2, alpha=0.05):\n    result = ts.copy()\n    log_used = False\n    n_diffs  = 0\n    # (1) check original\n    # (2) try log if all positive\n    # (3) difference up to max_diffs\n    return result, n_diffs, log_used\n\nnp.random.seed(42)\nts_rw     = pd.Series(np.cumsum(np.random.randn(100)))\nts_exp    = pd.Series(np.exp(0.03*np.arange(100) + np.random.randn(100)*0.2)*100)\nts_stat   = pd.Series(np.random.randn(100))\n\nfor name, ts in [(\'Random Walk\', ts_rw), (\'Exponential Trend\', ts_exp), (\'Stationary\', ts_stat)]:\n    out, d, log = make_stationary(ts)\n    print(f\"{name}: diffs={d}, log={log}\")\n"
}
},

{
"title": "19. ARIMA & SARIMA Modeling",
"desc": "ARIMA(p,d,q) models a stationary process as AutoRegressive + Integrated + Moving Average. SARIMA adds seasonal components (P,D,Q,m). Use AIC/BIC for order selection and residual diagnostics to validate.",
"examples": [
        {"label": "Fitting ARIMA and forecasting", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.arima.model import ARIMA\n\nnp.random.seed(42)\nn = 120\ndates = pd.date_range(\'2014-01\', periods=n, freq=\'MS\')\ntrend = np.linspace(100, 150, n)\nnoise = np.cumsum(np.random.normal(0, 2, n))  # AR component\nts = pd.Series(trend + noise, index=dates)\n\n# Fit ARIMA(1,1,1)\nmodel = ARIMA(ts, order=(1, 1, 1))\nfitted = model.fit()\nprint(fitted.summary().tables[1])\n\n# Forecast 12 months ahead\nforecast = fitted.get_forecast(steps=12)\npred_mean = forecast.predicted_mean\npred_ci   = forecast.conf_int(alpha=0.05)\n\nprint(f\"\\n12-month forecast:\")\nfor date, val, lo, hi in zip(pred_mean.index[:3], pred_mean[:3],\n                              pred_ci.iloc[:3,0], pred_ci.iloc[:3,1]):\n    print(f\"  {date.strftime(\'%Y-%m\')}: {val:.1f} [{lo:.1f}, {hi:.1f}]\")\nprint(f\"  ...\")\n\n# In-sample fit metrics\nfrom sklearn.metrics import mean_squared_error\nresiduals = fitted.resid\nprint(f\"\\nIn-sample RMSE: {np.sqrt((residuals**2).mean()):.3f}\")\nprint(f\"AIC: {fitted.aic:.2f}, BIC: {fitted.bic:.2f}\")"},
        {"label": "SARIMA for seasonal data", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.statespace.sarimax import SARIMAX\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(42)\nn = 84  # 7 years monthly\ndates = pd.date_range(\'2017-01\', periods=n, freq=\'MS\')\ntrend    = np.linspace(1000, 1600, n)\nseasonal = 200 * np.sin(2*np.pi*np.arange(n)/12)\nnoise    = np.cumsum(np.random.normal(0, 20, n))\nts = pd.Series(trend + seasonal + noise, index=dates)\n\n# SARIMA(1,1,1)(1,1,1,12)\nmodel = SARIMAX(ts, order=(1,1,1), seasonal_order=(1,1,1,12),\n                trend=\'n\', enforce_stationarity=False,\n                enforce_invertibility=False)\nfitted = model.fit(disp=False)\nprint(f\"SARIMA(1,1,1)(1,1,1,12): AIC={fitted.aic:.2f}, BIC={fitted.bic:.2f}\")\n\n# Compare AIC for different orders\nfor order, sorder in [((0,1,1),(0,1,1,12)), ((1,1,0),(1,1,0,12))]:\n    m = SARIMAX(ts, order=order, seasonal_order=sorder,\n                enforce_stationarity=False, enforce_invertibility=False)\n    f = m.fit(disp=False)\n    print(f\"SARIMA{order}{sorder}: AIC={f.aic:.2f}\")\n\nforecast = fitted.get_forecast(12)\nprint(f\"\\nForecast next month: {forecast.predicted_mean.iloc[0]:.1f}\")"},
        {"label": "Residual diagnostics and model validation", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.arima.model import ARIMA\nfrom statsmodels.stats.diagnostic import acorr_ljungbox\nfrom scipy import stats\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(0)\nn = 150\nts = pd.Series(np.cumsum(np.random.normal(0.5, 2, n)) + np.random.randn(n),\n               index=pd.date_range(\'2012-01\', periods=n, freq=\'MS\'))\n\nmodel = ARIMA(ts, order=(1, 1, 1))\nfitted = model.fit()\nresiduals = fitted.resid.dropna()\n\n# Test 1: Ljung-Box (autocorrelation in residuals)\nlb = acorr_ljungbox(residuals, lags=[10], return_df=True)\nprint(f\"Ljung-Box p (lag 10): {lb[\'lb_pvalue\'].iloc[0]:.4f}  (>0.05 = no autocorrelation = good)\")\n\n# Test 2: Normality of residuals\n_, p_sw = stats.shapiro(residuals[:50])\nprint(f\"Shapiro-Wilk p:       {p_sw:.4f}  (>0.05 = normal residuals = good)\")\n\n# Test 3: Heteroskedasticity (should be constant variance)\nhalf = len(residuals) // 2\n_, p_lev = stats.levene(residuals[:half], residuals[half:])\nprint(f\"Levene p:             {p_lev:.4f}  (>0.05 = equal variance = good)\")\n\nprint(f\"\\nResidual stats: mean={residuals.mean():.4f}, std={residuals.std():.3f}\")\nprint(f\"AIC={fitted.aic:.2f}, model is {\'adequate\' if lb[\'lb_pvalue\'].iloc[0]>0.05 else \'needs improvement\'}\")"}
    ],
"rw_scenario": "An energy company forecasts monthly natural gas demand for the next 6 months using SARIMA to capture both the yearly seasonal cycle and trend growth, with 95% prediction intervals for capacity planning.",
"rw_code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.statespace.sarimax import SARIMAX\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(5)\nn = 96\ndates = pd.date_range(\'2016-01\', periods=n, freq=\'MS\')\ntrend    = np.linspace(500, 700, n)\nseasonal = 150 * np.cos(2*np.pi*np.arange(n)/12)  # peak in winter\nnoise    = np.cumsum(np.random.normal(0, 10, n))\ndemand   = pd.Series(trend + seasonal + noise, index=dates, name=\'Gas_MMcf\')\n\ntrain = demand[:-12]\ntest  = demand[-12:]\n\nmodel = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,12),\n                enforce_stationarity=False, enforce_invertibility=False)\nfitted = model.fit(disp=False)\n\nforecast = fitted.get_forecast(steps=12)\npred   = forecast.predicted_mean\nci     = forecast.conf_int()\n\nfrom sklearn.metrics import mean_absolute_percentage_error\nmape = mean_absolute_percentage_error(test, pred) * 100\nrmse = np.sqrt(((test - pred)**2).mean())\n\nprint(f\"SARIMA(1,1,1)(1,1,1,12) forecast metrics:\")\nprint(f\"  MAPE: {mape:.2f}%  RMSE: {rmse:.2f} MMcf\")\nprint(f\"  AIC: {fitted.aic:.1f}\")\nprint(f\"\\n6-month capacity forecast (MMcf):\")\nfor i in range(6):\n    print(f\"  {pred.index[i].strftime(\'%Y-%m\')}: {pred.iloc[i]:.0f} [{ci.iloc[i,0]:.0f}-{ci.iloc[i,1]:.0f}]\")",
"practice": {
    "title": "Auto-ARIMA Order Selection",
    "desc": "Generate monthly sales data for 4 years with AR(2) dynamics and monthly seasonality. Write a function select_arima_order(ts, max_p=3, max_q=3, d=1) that tries all ARIMA(p,d,q) combinations and returns the order with the lowest AIC. Compare its forecast (12 months) RMSE to naive persistence forecast.",
    "starter": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.arima.model import ARIMA\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(42)\nn = 60\nts = pd.Series(\n    100 + np.cumsum(np.random.normal(0, 2, n)) + 20*np.sin(2*np.pi*np.arange(n)/12),\n    index=pd.date_range(\'2019-01\', periods=n, freq=\'MS\'))\n\ndef select_arima_order(ts, max_p=3, max_q=3, d=1):\n    best_aic, best_order = np.inf, None\n    for p in range(max_p+1):\n        for q in range(max_q+1):\n            if p == 0 and q == 0:\n                continue\n            try:\n                m = ARIMA(ts, order=(p, d, q))\n                f = m.fit()\n                if f.aic < best_aic:\n                    best_aic, best_order = f.aic, (p, d, q)\n            except Exception:\n                pass\n    return best_order, best_aic\n\n# TODO: call select_arima_order on train set (first 48 months)\n# TODO: forecast last 12 months with best order\n# TODO: compare RMSE to naive persistence (repeat last observed value)\n"
}
},

{
"title": "20. Exponential Smoothing (ETS / Holt-Winters)",
"desc": "Exponential smoothing methods weight recent observations more heavily. Simple ES handles level; Holt\'s double ES adds trend; Holt-Winters triple ES adds seasonality. The ETS framework unifies them with Error-Trend-Seasonality states.",
"examples": [
        {"label": "Simple, Holt\'s double, and Holt-Winters", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(42)\nn = 60\ndates = pd.date_range(\'2019-01\', periods=n, freq=\'MS\')\ntrend    = np.linspace(100, 160, n)\nseasonal = 20 * np.sin(2*np.pi*np.arange(n)/12)\nnoise    = np.random.normal(0, 5, n)\nts = pd.Series(trend + seasonal + noise, index=dates)\n\ntrain, test = ts[:-12], ts[-12:]\n\n# Simple Exponential Smoothing (level only)\nses = SimpleExpSmoothing(train, initialization_method=\'estimated\').fit()\nses_fc = ses.forecast(12)\n\n# Holt\'s (trend)\nholt = Holt(train, initialization_method=\'estimated\').fit(\n    optimized=True, smoothing_level=0.3, smoothing_trend=0.1)\nholt_fc = holt.forecast(12)\n\n# Holt-Winters (trend + seasonality)\nhw = ExponentialSmoothing(train, trend=\'add\', seasonal=\'add\',\n                           seasonal_periods=12,\n                           initialization_method=\'estimated\').fit(optimized=True)\nhw_fc = hw.forecast(12)\n\nfrom sklearn.metrics import mean_squared_error\nfor name, fc in [(\'SES\', ses_fc), (\"Holt\'s\", holt_fc), (\'Holt-Winters\', hw_fc)]:\n    rmse = np.sqrt(mean_squared_error(test, fc))\n    print(f\"{name:15s}: RMSE={rmse:.2f},  alpha={getattr(getattr(ses if name==\'SES\' else holt if \'Holt\' in name and name!=\'Holt-Winters\' else hw,\'model\',None),\'params\',{}).get(\'smoothing_level\',\'N/A\')}\")"},
        {"label": "ETS auto-selection and damped trend", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.holtwinters import ExponentialSmoothing\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(0)\nn = 84\ndates = pd.date_range(\'2017-01\', periods=n, freq=\'MS\')\nts = pd.Series(\n    np.linspace(200, 320, n) + 30*np.sin(2*np.pi*np.arange(n)/12) +\n    np.random.normal(0, 8, n), index=dates)\n\ntrain, test = ts[:-12], ts[-12:]\n\nconfigs = [\n    (\'Additive trend + Additive seasonal\',   \'add\', \'add\',  False),\n    (\'Additive trend + Mult seasonal\',        \'add\', \'mul\',  False),\n    (\'Damped trend + Additive seasonal\',      \'add\', \'add\',  True),\n]\n\nprint(f\"{\'Model\':40s}  {\'RMSE\':>6s}  {\'AIC\':>8s}\")\nfor name, trend, seasonal, damped in configs:\n    m = ExponentialSmoothing(train, trend=trend, seasonal=seasonal,\n                              seasonal_periods=12, damped_trend=damped,\n                              initialization_method=\'estimated\')\n    fitted = m.fit(optimized=True)\n    fc = fitted.forecast(12)\n    rmse = np.sqrt(((test - fc)**2).mean())\n    print(f\"{name:40s}  {rmse:6.2f}  {fitted.aic:8.2f}\")"},
        {"label": "Smoothing parameters and state extraction", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.holtwinters import ExponentialSmoothing\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(5)\nn = 72\nts = pd.Series(\n    150 + np.linspace(0, 50, n) + 25*np.sin(2*np.pi*np.arange(n)/12) +\n    np.random.normal(0, 6, n),\n    index=pd.date_range(\'2018-01\', periods=n, freq=\'MS\'))\n\nhw = ExponentialSmoothing(ts, trend=\'add\', seasonal=\'add\',\n                           seasonal_periods=12,\n                           initialization_method=\'estimated\').fit(optimized=True)\n\nprint(\"Optimal smoothing parameters:\")\nprint(f\"  alpha (level):    {hw.params[\'smoothing_level\']:.4f}\")\nprint(f\"  beta  (trend):    {hw.params[\'smoothing_trend\']:.4f}\")\nprint(f\"  gamma (seasonal): {hw.params[\'smoothing_seasonal\']:.4f}\")\n\n# Extract level, trend, and seasonal states\nlevel    = hw.level\ntrend_s  = hw.trend\nseasonal = hw.season\n\nprint(f\"\\nFinal state:\")\nprint(f\"  Level:    {level.iloc[-1]:.2f}\")\nprint(f\"  Trend:    {trend_s.iloc[-1]:.4f} per period\")\nprint(f\"  Seasonal indices (last 12): {seasonal.iloc[-12:].round(2).values}\")\n\nfc = hw.forecast(6)\nprint(f\"\\n6-month forecast: {fc.round(1).values}\")"}
    ],
"rw_scenario": "A retailer uses Holt-Winters with multiplicative seasonality to forecast weekly ice cream sales, capturing both trend growth and summer/winter seasonality for inventory planning.",
"rw_code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.holtwinters import ExponentialSmoothing\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(7)\nn_weeks = 104  # 2 years weekly\nt = np.arange(n_weeks)\ntrend_w    = 1000 + t * 3\nseasonal_w = 400 * np.sin(2*np.pi*t/52) + 150 * (t % 52 > 44).astype(float)  # summer+holiday\nnoise_w    = np.random.normal(0, 40, n_weeks)\nweekly_sales = pd.Series(\n    (trend_w + seasonal_w + noise_w).clip(min=100),\n    index=pd.date_range(\'2022-01-03\', periods=n_weeks, freq=\'W\'))\n\ntrain_w = weekly_sales[:-8]\ntest_w  = weekly_sales[-8:]\n\n# Try additive and multiplicative seasonal\nfor seas_type in [\'add\', \'mul\']:\n    hw = ExponentialSmoothing(\n        train_w, trend=\'add\', seasonal=seas_type,\n        seasonal_periods=52, initialization_method=\'estimated\').fit(optimized=True)\n    fc = hw.forecast(8)\n    rmse = np.sqrt(((test_w - fc)**2).mean())\n    mape = (abs(test_w - fc) / test_w).mean() * 100\n    print(f\"Seasonal={seas_type}: RMSE={rmse:.1f}, MAPE={mape:.2f}%, AIC={hw.aic:.1f}\")\n\n# Reorder forecast for next 4 weeks\nbest_hw = ExponentialSmoothing(weekly_sales, trend=\'add\', seasonal=\'add\',\n                                seasonal_periods=52, initialization_method=\'estimated\').fit(optimized=True)\nnext4 = best_hw.forecast(4)\nprint(f\"\\nNext 4 weeks inventory needs: {next4.round(0).values}\")",
"practice": {
    "title": "ETS Grid Search",
    "desc": "Generate 5 years of monthly data with trend + seasonality. Write a grid_search_ets(train, test, h) function that tries all combinations of trend in [None, \'add\'], seasonal in [None, \'add\', \'mul\'], damped in [True, False] (only when trend is not None). Return a DataFrame with columns: model_name, AIC, test_RMSE, test_MAPE. Sort by test_RMSE.",
    "starter": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.holtwinters import ExponentialSmoothing\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(42)\nn = 72\nts = pd.Series(100 + np.linspace(0,60,n) + 25*np.sin(2*np.pi*np.arange(n)/12) + np.random.randn(n)*5,\n               index=pd.date_range(\'2018-01\', periods=n, freq=\'MS\'))\ntrain, test = ts[:-12], ts[-12:]\n\ndef grid_search_ets(train, test, h=12):\n    results = []\n    # TODO: iterate over trend, seasonal, damped combinations\n    # TODO: fit ExponentialSmoothing, forecast h steps\n    # TODO: compute AIC, RMSE, MAPE\n    # TODO: append to results, return sorted DataFrame\n    return pd.DataFrame(results)\n\nprint(grid_search_ets(train, test).head(5))\n"
}
},

{
"title": "21. ML Approach: Lag Features & Sklearn",
"desc": "Transform any time series into a supervised ML problem by creating lag features, rolling statistics, and calendar features. This lets you use any sklearn regressor for forecasting.",
"examples": [
        {"label": "Creating lag and rolling features", "code": "import numpy as np, pandas as pd\n\nnp.random.seed(42)\nn = 200\nts = pd.Series(\n    100 + np.cumsum(np.random.normal(0.3, 2, n)) +\n    15 * np.sin(2*np.pi*np.arange(n)/12),\n    index=pd.date_range(\'2007-01\', periods=n, freq=\'MS\'),\n    name=\'sales\')\n\ndef make_features(ts, lags=6, windows=[3, 6, 12]):\n    df = pd.DataFrame({\'y\': ts})\n    # Lag features\n    for lag in range(1, lags+1):\n        df[f\'lag_{lag}\'] = ts.shift(lag)\n    # Rolling statistics\n    for w in windows:\n        df[f\'roll_mean_{w}\']  = ts.shift(1).rolling(w).mean()\n        df[f\'roll_std_{w}\']   = ts.shift(1).rolling(w).std()\n        df[f\'roll_min_{w}\']   = ts.shift(1).rolling(w).min()\n    # Calendar features\n    df[\'month\']     = ts.index.month\n    df[\'month_sin\'] = np.sin(2*np.pi*ts.index.month/12)\n    df[\'month_cos\'] = np.cos(2*np.pi*ts.index.month/12)\n    df[\'trend\']     = np.arange(len(ts))\n    return df.dropna()\n\nfeatures = make_features(ts)\nprint(f\"Feature matrix: {features.shape}\")\nprint(f\"Features: {list(features.columns)}\")\nprint(f\"\\nSample row:\\n{features.iloc[0].round(3)}\")"},
        {"label": "Sklearn regressor for forecasting (walk-forward)", "code": "import numpy as np, pandas as pd\nfrom sklearn.ensemble import GradientBoostingRegressor\nfrom sklearn.metrics import mean_absolute_percentage_error\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(0)\nn = 180\nts = pd.Series(\n    100 + np.cumsum(np.random.normal(0.3, 1.5, n)) +\n    20 * np.sin(2*np.pi*np.arange(n)/12),\n    index=pd.date_range(\'2009-06\', periods=n, freq=\'MS\'))\n\ndef make_features(ts, lags=12):\n    df = pd.DataFrame({\'y\': ts})\n    for lag in range(1, lags+1):\n        df[f\'lag_{lag}\'] = ts.shift(lag)\n    df[\'roll_mean_6\'] = ts.shift(1).rolling(6).mean()\n    df[\'roll_std_6\']  = ts.shift(1).rolling(6).std()\n    df[\'month_sin\']   = np.sin(2*np.pi*ts.index.month/12)\n    df[\'month_cos\']   = np.cos(2*np.pi*ts.index.month/12)\n    return df.dropna()\n\ndata  = make_features(ts)\ncutoff = len(data) - 24\nX, y  = data.drop(\'y\', axis=1), data[\'y\']\n\nX_tr, X_te = X.iloc[:cutoff], X.iloc[cutoff:]\ny_tr, y_te = y.iloc[:cutoff], y.iloc[cutoff:]\n\nmodel = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)\nmodel.fit(X_tr, y_tr)\npreds = model.predict(X_te)\n\nrmse = np.sqrt(((y_te.values - preds)**2).mean())\nmape = mean_absolute_percentage_error(y_te, preds) * 100\nprint(f\"GBR Forecast: RMSE={rmse:.2f}, MAPE={mape:.2f}%\")\n\n# Feature importance\nimp = pd.Series(model.feature_importances_, index=X.columns).nlargest(5)\nprint(f\"Top features: {imp.round(3).to_dict()}\")"},
        {"label": "Recursive multi-step forecasting", "code": "import numpy as np, pandas as pd\nfrom sklearn.ensemble import RandomForestRegressor\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(42)\nn = 150\nts = pd.Series(\n    np.cumsum(np.random.normal(0.5, 2, n)) + 100 +\n    15 * np.sin(2*np.pi*np.arange(n)/12),\n    index=pd.date_range(\'2012-06\', periods=n, freq=\'MS\'))\n\nlags = 6\ndata = pd.DataFrame({\'y\': ts})\nfor l in range(1, lags+1):\n    data[f\'lag_{l}\'] = ts.shift(l)\ndata[\'month_sin\'] = np.sin(2*np.pi*ts.index.month/12)\ndata[\'month_cos\'] = np.cos(2*np.pi*ts.index.month/12)\ndata = data.dropna()\n\nX, y = data.drop(\'y\', axis=1), data[\'y\']\nX_tr, X_te = X.iloc[:-12], X.iloc[-12:]\ny_tr, y_te = y.iloc[:-12], y.iloc[-12:]\n\nmodel = RandomForestRegressor(n_estimators=100, random_state=42)\nmodel.fit(X_tr, y_tr)\n\n# Recursive forecast: use predictions as future lags\nhistory = list(y_tr.values[-lags:])\npreds = []\nfuture_idx = pd.date_range(X_te.index[0], periods=12, freq=\'MS\')\nfor i, date in enumerate(future_idx):\n    row = [history[-l] for l in range(1, lags+1)]\n    row += [np.sin(2*np.pi*date.month/12), np.cos(2*np.pi*date.month/12)]\n    pred = model.predict([row])[0]\n    preds.append(pred)\n    history.append(pred)\n\nrmse = np.sqrt(((y_te.values - np.array(preds))**2).mean())\nprint(f\"Recursive RF RMSE: {rmse:.2f}\")\nprint(f\"True last 3:  {y_te.values[-3:].round(1)}\")\nprint(f\"Pred last 3:  {np.array(preds[-3:]).round(1)}\")"}
    ],
"rw_scenario": "A logistics company uses a LightGBM model with 24 lag features, rolling means, and one-hot encoded weekday/month to forecast daily parcel volume 7 days ahead, outperforming SARIMA by 30% MAPE.",
"rw_code": "import numpy as np, pandas as pd\nfrom sklearn.ensemble import GradientBoostingRegressor\nfrom sklearn.metrics import mean_absolute_percentage_error\n\nnp.random.seed(42)\nn = 365 * 2  # 2 years daily\nt = np.arange(n)\ndaily = pd.Series(\n    1000 + 0.5*t +\n    300 * np.sin(2*np.pi*t/365) +\n    150 * np.sin(2*np.pi*t/7) +   # weekly pattern\n    np.random.normal(0, 50, n),\n    index=pd.date_range(\'2022-01-01\', periods=n, freq=\'D\'))\n\ndef build_features(ts, lags=14):\n    df = pd.DataFrame({\'y\': ts})\n    for l in range(1, lags+1):\n        df[f\'lag_{l}\'] = ts.shift(l)\n    for w in [7, 14, 30]:\n        df[f\'rm_{w}\'] = ts.shift(1).rolling(w).mean()\n    df[\'dow\']        = ts.index.dayofweek\n    df[\'month\']      = ts.index.month\n    df[\'week_sin\']   = np.sin(2*np.pi*ts.index.dayofweek/7)\n    df[\'week_cos\']   = np.cos(2*np.pi*ts.index.dayofweek/7)\n    df[\'annual_sin\'] = np.sin(2*np.pi*ts.index.dayofyear/365)\n    return df.dropna()\n\ndata = build_features(daily)\nX, y = data.drop(\'y\', axis=1), data[\'y\']\nsplit = len(data) - 90\nX_tr, X_te, y_tr, y_te = X.iloc[:split], X.iloc[split:], y.iloc[:split], y.iloc[split:]\n\ngbr = GradientBoostingRegressor(n_estimators=300, max_depth=5, learning_rate=0.05, random_state=42)\ngbr.fit(X_tr, y_tr)\npreds = gbr.predict(X_te)\n\nmape = mean_absolute_percentage_error(y_te, preds) * 100\nrmse = np.sqrt(((y_te.values - preds)**2).mean())\nprint(f\"Daily volume forecast: MAPE={mape:.2f}%, RMSE={rmse:.1f}\")\ntop5 = pd.Series(gbr.feature_importances_, index=X.columns).nlargest(5)\nprint(f\"Top features: {top5.round(3).to_dict()}\")",
"practice": {
    "title": "Feature Engineering for Weekly Data",
    "desc": "Generate 3 years of weekly store sales (trend + annual seasonality + weekly dip on off-season weeks). Create features: lags 1-8, rolling mean/std at 4 and 8 weeks, week-of-year sine/cosine, year indicator. Train RandomForest on first 2.5 years, test on last 6 months. Report RMSE and MAPE. Plot (print) actual vs predicted for the test period.",
    "starter": "import numpy as np, pandas as pd\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.metrics import mean_absolute_percentage_error\n\nnp.random.seed(42)\nn = 156  # 3 years weekly\nt = np.arange(n)\nts = pd.Series(\n    5000 + 10*t + 800*np.sin(2*np.pi*t/52) + np.random.normal(0,150,n),\n    index=pd.date_range(\'2021-01-04\', periods=n, freq=\'W\'))\n\n# TODO: create lag + rolling + calendar features\n# TODO: train/test split (last 26 weeks = test)\n# TODO: train RandomForest\n# TODO: report RMSE and MAPE\n# TODO: print actual vs predicted for test\n"
}
},

{
"title": "22. Time Series Anomaly Detection",
"desc": "Detect anomalous time points using statistical control limits, rolling z-scores, STL residuals, and IsolationForest. Different methods suit different anomaly types: spikes, level shifts, or trend changes.",
"examples": [
        {"label": "Rolling z-score and IQR fences", "code": "import numpy as np, pandas as pd\n\nnp.random.seed(42)\nn = 200\nts = pd.Series(\n    50 + np.cumsum(np.random.normal(0.1, 1, n)),\n    index=pd.date_range(\'2020-01-01\', periods=n, freq=\'D\'))\n\n# Inject anomalies\nanomaly_idx = [40, 90, 140, 170]\nts.iloc[anomaly_idx] += np.array([25, -30, 20, -25])\n\n# Method 1: Rolling z-score\nwindow = 20\nroll_mean = ts.rolling(window, min_periods=1).mean()\nroll_std  = ts.rolling(window, min_periods=1).std().fillna(1)\nz_scores  = (ts - roll_mean) / roll_std\n\nanomalies_z = ts[abs(z_scores) > 3]\nprint(f\"Rolling z-score (|z|>3): {len(anomalies_z)} anomalies detected\")\nprint(f\"  True: {anomaly_idx}\")\nprint(f\"  Detected: {list(anomalies_z.index.strftime(\'%Y-%m-%d\')[:5])}\")\n\n# Method 2: IQR fences on rolling window\nq1 = ts.rolling(30).quantile(0.25)\nq3 = ts.rolling(30).quantile(0.75)\niqr = q3 - q1\nlower = q1 - 1.5 * iqr\nupper = q3 + 1.5 * iqr\nanomalies_iqr = ts[(ts < lower) | (ts > upper)]\nprint(f\"IQR fences: {len(anomalies_iqr)} anomalies detected\")"},
        {"label": "STL residuals for anomaly detection", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.seasonal import STL\n\nnp.random.seed(0)\nn = 120\nts = pd.Series(\n    100 + np.linspace(0,30,n) + 20*np.sin(2*np.pi*np.arange(n)/12) +\n    np.random.normal(0, 3, n),\n    index=pd.date_range(\'2014-01\', periods=n, freq=\'MS\'))\n\n# Inject anomalies at specific months\nanom_idx = [24, 50, 85, 100]\nts.iloc[anom_idx] += [40, -35, 50, -40]\n\nstl = STL(ts, period=12, robust=True)\nres = stl.fit()\nresiduals = pd.Series(res.resid, index=ts.index)\n\n# Flag residuals beyond 3 sigma (estimated robustly)\nfrom scipy.stats import median_abs_deviation\nmad  = median_abs_deviation(residuals.dropna())\nrobust_std = mad / 0.6745\nthreshold  = 3 * robust_std\n\nflags = abs(residuals) > threshold\ndetected = ts[flags]\nprint(f\"STL residual anomaly detection (threshold={threshold:.2f}):\")\nprint(f\"  Flagged {flags.sum()} points\")\nprint(f\"  True anomaly indices: {anom_idx}\")\nprint(f\"  Detected at: {list(detected.index.strftime(\'%Y-%m\')[:6])}\")\n\ntp = sum(1 for i in anom_idx if flags.iloc[i])\nfp = flags.sum() - tp\nprint(f\"  TP={tp}, FP={fp}\")"},
        {"label": "IsolationForest on windowed features", "code": "import numpy as np, pandas as pd\nfrom sklearn.ensemble import IsolationForest\nfrom sklearn.preprocessing import StandardScaler\n\nnp.random.seed(42)\nn = 365\nts = pd.Series(\n    100 + 0.05*np.arange(n) + 20*np.sin(2*np.pi*np.arange(n)/365) +\n    np.random.normal(0, 4, n),\n    index=pd.date_range(\'2022-01-01\', periods=n, freq=\'D\'))\n\ntrue_anomalies = [50, 120, 200, 280, 340]\nts.iloc[true_anomalies] += np.array([35, -40, 30, -45, 38])\n\n# Build windowed features for each point\nwindow = 7\nfeatures = pd.DataFrame({\n    \'value\':      ts,\n    \'diff1\':      ts.diff(),\n    \'roll_mean\':  ts.rolling(window).mean(),\n    \'roll_std\':   ts.rolling(window).std(),\n    \'z_score\':    (ts - ts.rolling(window).mean()) / ts.rolling(window).std(),\n}).dropna()\n\nscaler = StandardScaler()\nX = scaler.fit_transform(features)\n\niso = IsolationForest(contamination=len(true_anomalies)/n, random_state=42, n_estimators=200)\npreds = iso.fit_predict(X)   # -1 = anomaly\n\ndetected_idx = features.index[preds == -1]\nprint(f\"IsolationForest detected: {len(detected_idx)} anomalies\")\ntrue_dates = ts.index[true_anomalies]\ntp = sum(1 for d in detected_idx if any(abs((d - t).days) <= 2 for t in true_dates))\nprint(f\"True positives (within 2 days): {tp}/{len(true_anomalies)}\")"}
    ],
"rw_scenario": "A server monitoring system flags CPU usage anomalies in real-time: rolling z-score catches sudden spikes, while STL residuals detect subtle level shifts that z-score misses after trend changes.",
"rw_code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.seasonal import STL\nfrom scipy.stats import median_abs_deviation\n\nnp.random.seed(42)\nn = 1440  # 24 hours × 60 min (1 day, minutely)\nt = np.arange(n)\n# CPU: daily cycle + trend\ncpu = pd.Series(\n    40 + 20*np.sin(2*np.pi*t/1440) + np.random.normal(0, 3, n),\n    index=pd.date_range(\'2024-01-01\', periods=n, freq=\'min\'))\n\n# Inject anomalies\ncpu.iloc[200:210] += 35    # sustained spike\ncpu.iloc[800]     += 60    # sudden spike\ncpu.iloc[1200]    -= 25    # drop\n\n# Method 1: Rolling z-score (fast, real-time friendly)\nw = 60\nz = (cpu - cpu.rolling(w).mean()) / cpu.rolling(w).std()\nz_flags = (abs(z) > 3).fillna(False)\n\n# Method 2: Hourly aggregation + STL\nhourly = cpu.resample(\'H\').mean()\nstl = STL(hourly, period=24, robust=True)\nresid = pd.Series(stl.fit().resid, index=hourly.index)\nmad = median_abs_deviation(resid.dropna())\nstl_flags = abs(resid) > 3 * mad / 0.6745\n\nprint(f\"Rolling z-score flagged: {z_flags.sum()} minutes\")\nprint(f\"STL (hourly) flagged:    {stl_flags.sum()} hours\")\nprint(f\"Z-score alerts during spike period: {z_flags.iloc[195:215].sum()}\")",
"practice": {
    "title": "Multi-Method Anomaly Ensemble",
    "desc": "Generate 2 years of daily temperature data (seasonal + trend + noise). Inject 6 anomalies (3 spikes, 3 drops). Implement 3 detectors: (1) rolling 30-day z-score threshold 3, (2) IQR fence on 30-day window, (3) STL residuals with 3-sigma MAD threshold. Print a table showing which detectors caught each injected anomaly (TP matrix).",
    "starter": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.seasonal import STL\nfrom sklearn.ensemble import IsolationForest\nfrom scipy.stats import median_abs_deviation\n\nnp.random.seed(42)\nn = 730\nt = np.arange(n)\nts = pd.Series(\n    15 + 0.01*t + 10*np.sin(2*np.pi*t/365) + np.random.normal(0,1.5,n),\n    index=pd.date_range(\'2022-01-01\', periods=n, freq=\'D\'),\n    name=\'temperature\')\n\nanom_days = [60, 150, 250, 380, 500, 650]\ndeltas    = [12, -15, 10, -13, 11, -10]\nfor day, delta in zip(anom_days, deltas):\n    ts.iloc[day] += delta\n\n# TODO: implement 3 anomaly detectors\n# TODO: print TP matrix for each injected anomaly\n"
}
},

{
"title": "23. Forecast Evaluation & Backtesting",
"desc": "RMSE and MAPE are standard forecast metrics but have blind spots. SMAPE handles zeros; MASE benchmarks against naive. Walk-forward backtesting gives realistic performance estimates and detects overfitting to a single test window.",
"examples": [
        {"label": "RMSE, MAPE, MASE, SMAPE", "code": "import numpy as np\n\ndef rmse(y_true, y_pred):\n    return np.sqrt(np.mean((y_true - y_pred)**2))\n\ndef mape(y_true, y_pred):\n    mask = y_true != 0\n    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100\n\ndef smape(y_true, y_pred):\n    denom = (np.abs(y_true) + np.abs(y_pred)) / 2\n    mask  = denom > 0\n    return np.mean(np.abs(y_true[mask] - y_pred[mask]) / denom[mask]) * 100\n\ndef mase(y_true, y_pred, y_train, m=1):\n    # Mean Absolute Scaled Error: normalized by naive seasonal forecast error\n    naive_err = np.mean(np.abs(np.diff(y_train, n=m)))\n    return np.mean(np.abs(y_true - y_pred)) / naive_err\n\nnp.random.seed(42)\ny_true  = np.array([100, 150, 130, 200, 175, 220, 195, 210])\ny_pred  = y_true + np.random.randn(len(y_true)) * 15\ny_train = np.array([80, 90, 110, 95, 105, 120, 115, 130, 140] + list(y_true[:4]))\n\nprint(f\"RMSE:  {rmse(y_true, y_pred):.3f}\")\nprint(f\"MAPE:  {mape(y_true, y_pred):.2f}%\")\nprint(f\"SMAPE: {smape(y_true, y_pred):.2f}%\")\nprint(f\"MASE:  {mase(y_true, y_pred, np.array(y_train)):.3f}  (< 1 = better than naive)\")\n\n# Bias and directional accuracy\nbias = np.mean(y_pred - y_true)\nda   = np.mean(np.sign(np.diff(y_true)) == np.sign(np.diff(y_pred))) * 100\nprint(f\"Bias:  {bias:.3f} (positive = over-forecast)\")\nprint(f\"Directional accuracy: {da:.1f}%\")"},
        {"label": "Walk-forward cross-validation", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.holtwinters import ExponentialSmoothing\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(42)\nn = 84\nts = pd.Series(\n    100 + np.linspace(0,50,n) + 20*np.sin(2*np.pi*np.arange(n)/12) +\n    np.random.normal(0,5,n),\n    index=pd.date_range(\'2017-01\', periods=n, freq=\'MS\'))\n\ndef walk_forward_cv(ts, min_train=24, step=6, h=6):\n    errors = []\n    starts = range(min_train, len(ts) - h + 1, step)\n    for start in starts:\n        train = ts[:start]\n        test  = ts[start:start+h]\n        try:\n            hw = ExponentialSmoothing(train, trend=\'add\', seasonal=\'add\',\n                                       seasonal_periods=12,\n                                       initialization_method=\'estimated\').fit(optimized=True)\n            fc = hw.forecast(h)\n            rmse = np.sqrt(((test.values - fc.values)**2).mean())\n            errors.append({\'fold\': start, \'n_train\': len(train),\n                           \'rmse\': rmse, \'mape\': (abs(test - fc)/test).mean()*100})\n        except Exception:\n            pass\n    return pd.DataFrame(errors)\n\ncv_results = walk_forward_cv(ts)\nprint(f\"Walk-forward CV ({len(cv_results)} folds):\")\nprint(cv_results.round(2).to_string(index=False))\nprint(f\"\\nMean RMSE: {cv_results.rmse.mean():.3f} ± {cv_results.rmse.std():.3f}\")\nprint(f\"Mean MAPE: {cv_results.mape.mean():.2f}%\")"},
        {"label": "Naive benchmarks and Diebold-Mariano test", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.holtwinters import ExponentialSmoothing\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(5)\nn = 96\nts = pd.Series(\n    200 + np.linspace(0,80,n) + 40*np.sin(2*np.pi*np.arange(n)/12) +\n    np.random.normal(0,8,n),\n    index=pd.date_range(\'2016-01\', periods=n, freq=\'MS\'))\n\ntrain, test = ts[:-12], ts[-12:]\n\n# Naive benchmarks\nnaive_persistence = pd.Series([train.iloc[-1]] * 12, index=test.index)  # last value\nnaive_seasonal    = train.iloc[-12:].values  # same season last year\n\nhw = ExponentialSmoothing(train, trend=\'add\', seasonal=\'add\',\n                           seasonal_periods=12, initialization_method=\'estimated\').fit(optimized=True)\nhw_fc = hw.forecast(12)\n\nforecasts = {\n    \'Naive Persist\': naive_persistence.values,\n    \'Naive Seasonal\': naive_seasonal,\n    \'Holt-Winters\':  hw_fc.values,\n}\n\nprint(f\"{\'Model\':18s}  {\'RMSE\':>7s}  {\'MAPE\':>7s}\")\nfor name, fc in forecasts.items():\n    rmse = np.sqrt(((test.values - fc)**2).mean())\n    mape = (abs(test.values - fc) / test.values).mean() * 100\n    print(f\"{name:18s}  {rmse:7.2f}  {mape:7.2f}%\")\n\n# MASE relative to seasonal naive\nnaive_err = np.mean(np.abs(np.diff(train.values, n=12)))\nhw_mase = np.mean(np.abs(test.values - hw_fc.values)) / naive_err\nprint(f\"\\nHolt-Winters MASE vs seasonal naive: {hw_mase:.3f}\")"}
    ],
"rw_scenario": "A demand planner evaluates 3 forecasting models (SARIMA, Holt-Winters, ML) using 5-fold walk-forward CV on 3 years of data. MASE relative to seasonal naive reveals which model truly adds value.",
"rw_code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.holtwinters import ExponentialSmoothing\nfrom statsmodels.tsa.statespace.sarimax import SARIMAX\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(42)\nn = 72\nts = pd.Series(\n    500 + np.linspace(0,200,n) + 100*np.sin(2*np.pi*np.arange(n)/12) +\n    np.random.normal(0,15,n),\n    index=pd.date_range(\'2018-01\', periods=n, freq=\'MS\'))\n\nfolds, h = 5, 6\nfold_size = (len(ts) - 24) // folds\nresults = {m: [] for m in [\'HW\',\'SARIMA\']}\n\nfor fold in range(folds):\n    cutoff = 24 + fold * fold_size\n    train = ts[:cutoff]\n    test  = ts[cutoff:cutoff+h]\n    if len(test) < h: break\n    try:\n        hw = ExponentialSmoothing(train, trend=\'add\', seasonal=\'add\', seasonal_periods=12,\n                                   initialization_method=\'estimated\').fit(optimized=True)\n        hw_fc = hw.forecast(h)\n        results[\'HW\'].append(np.sqrt(((test.values - hw_fc.values)**2).mean()))\n    except: pass\n    try:\n        sm = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,12),\n                     enforce_stationarity=False).fit(disp=False)\n        sm_fc = sm.forecast(h)\n        results[\'SARIMA\'].append(np.sqrt(((test.values - sm_fc.values)**2).mean()))\n    except: pass\n\nfor model, rmses in results.items():\n    if rmses:\n        print(f\"{model:8s}: mean RMSE={np.mean(rmses):.2f} ± {np.std(rmses):.2f} ({len(rmses)} folds)\")",
"practice": {
    "title": "Comprehensive Forecast Tournament",
    "desc": "Generate 5 years of monthly data. Implement a forecast_tournament(ts, h=12) function that: (1) Runs walk-forward CV (4 folds) on SARIMA, Holt-Winters, and a naive seasonal benchmark, (2) Returns a summary DataFrame with model, mean_RMSE, std_RMSE, mean_MAPE, (3) Declares a winner. Test it on your generated data.",
    "starter": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.holtwinters import ExponentialSmoothing\nfrom statsmodels.tsa.statespace.sarimax import SARIMAX\nimport warnings; warnings.filterwarnings(\'ignore\')\n\ndef forecast_tournament(ts, h=12, n_folds=4):\n    # TODO: implement walk-forward CV for each model\n    # TODO: return DataFrame: model, mean_RMSE, std_RMSE, mean_MAPE\n    pass\n\nnp.random.seed(42)\nn = 72\nts = pd.Series(\n    300 + np.linspace(0,100,n) + 60*np.sin(2*np.pi*np.arange(n)/12) + np.random.randn(n)*10,\n    index=pd.date_range(\'2018-01\', periods=n, freq=\'MS\'))\n\nresults = forecast_tournament(ts, h=6, n_folds=4)\nprint(results)\n"
}
},

{
"title": "24. Multivariate Time Series & Prophet",
"desc": "VAR models multiple related time series jointly. Granger causality tests whether one series predicts another. Facebook Prophet is a user-friendly forecaster for business time series with holidays and change points.",
"examples": [
        {"label": "Vector Autoregression (VAR)", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.vector_ar.var_model import VAR\nfrom statsmodels.tsa.stattools import adfuller\n\nnp.random.seed(42)\nn = 120\n# Two co-moving series: temperature and ice cream sales\ntemp  = pd.Series(20 + 10*np.sin(2*np.pi*np.arange(n)/12) + np.random.randn(n)*2)\nsales = 0.8*temp.shift(1).fillna(0) + np.random.randn(n)*5 + 50\n\ndf = pd.DataFrame({\'temp\': temp, \'sales\': sales})\n# Difference to achieve stationarity\ndf_diff = df.diff().dropna()\n\nmodel = VAR(df_diff)\nresult = model.fit(maxlags=4, ic=\'aic\')\nprint(f\"VAR({result.k_ar}) fitted. AIC={result.aic:.2f}\")\nprint(f\"\\nGranger causality test (temp -> sales):\")\n\nlag_order = result.k_ar\ntest = result.test_causality(\'sales\', \'temp\', kind=\'f\')\nprint(f\"  F-stat={test.test_statistic:.3f}, p={test.pvalue:.4f}\")\nprint(f\"  Temp Granger-causes sales? {test.pvalue < 0.05}\")\n\nfc = result.forecast(df_diff.values[-lag_order:], steps=6)\nprint(f\"\\n6-step forecast (differences):\\n{pd.DataFrame(fc, columns=[\'temp_d\',\'sales_d\']).round(2)}\")"},
        {"label": "Granger causality and cross-correlation", "code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.stattools import grangercausalitytests, ccf\n\nnp.random.seed(0)\nn = 200\n# advertising spend leads to sales with 2-period lag\nad_spend  = pd.Series(np.random.normal(100, 20, n))\nsales     = 0.7 * ad_spend.shift(2).fillna(0) + np.random.randn(n) * 15 + 200\nweb_visits = 0.5 * ad_spend.shift(1).fillna(0) + np.random.randn(n) * 10\n\ndf = pd.DataFrame({\'sales\': sales.diff(), \'ad_spend\': ad_spend.diff(),\n                   \'web\': web_visits.diff()}).dropna()\n\nprint(\"Granger causality: ad_spend -> sales (maxlag=5):\")\ngc = grangercausalitytests(df[[\'sales\',\'ad_spend\']], maxlag=3, verbose=False)\nfor lag, res in gc.items():\n    p = res[0][\'ssr_ftest\'][1]\n    print(f\"  lag {lag}: F-p={p:.4f}  {\'*\' if p<0.05 else \'\'}\")\n\n# Cross-correlation function\ncc = ccf(df[\'ad_spend\'], df[\'sales\'], alpha=0.05, unbiased=True)\nprint(f\"\\nCross-correlation (ad_spend, sales) at lags 0-5:\")\nfor lag, r in enumerate(cc[0][:6]):\n    print(f\"  lag {lag}: r={r:.3f}\")"},
        {"label": "Facebook Prophet forecasting", "code": "import numpy as np, pandas as pd\ntry:\n    from prophet import Prophet\n    HAS_PROPHET = True\nexcept ImportError:\n    HAS_PROPHET = False\n    print(\"Install: pip install prophet\")\n\nif HAS_PROPHET:\n    np.random.seed(42)\n    n = 180\n    dates = pd.date_range(\'2018-01-01\', periods=n, freq=\'MS\')\n    trend    = np.linspace(1000, 2000, n)\n    seasonal = 300 * np.sin(2*np.pi*np.arange(n)/12)\n    noise    = np.random.normal(0, 50, n)\n    df = pd.DataFrame({\'ds\': dates, \'y\': trend + seasonal + noise})\n\n    m = Prophet(yearly_seasonality=True, weekly_seasonality=False,\n                daily_seasonality=False, changepoint_prior_scale=0.05)\n    m.fit(df)\n\n    future = m.make_future_dataframe(periods=24, freq=\'MS\')\n    forecast = m.predict(future)\n\n    print(forecast[[\'ds\',\'yhat\',\'yhat_lower\',\'yhat_upper\']].tail(6).round(1).to_string())\n    print(f\"\\nTrend at end: {forecast[\'trend\'].iloc[-1]:.1f}\")\nelse:\n    print(\"Prophet demo: requires \'pip install prophet\'\")\n    print(\"Prophet uses additive model: y = trend + seasonality + holidays + error\")\n    print(\"Key params: changepoint_prior_scale, seasonality_prior_scale, holidays\")"}
    ],
"rw_scenario": "A macroeconomist builds a VAR model on monthly GDP, unemployment, and inflation data to forecast 6 months ahead, using Granger causality to confirm which indicators lead others.",
"rw_code": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.vector_ar.var_model import VAR\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(7)\nn = 120\nt = np.arange(n)\n\n# Simulated macro indicators (stationary after differencing)\ngdp_growth    = pd.Series(0.5 + 0.3*np.sin(2*np.pi*t/24) + np.random.randn(n)*0.8)\nunemployment  = pd.Series(5.0 - 0.4*gdp_growth.shift(1).fillna(5) + np.random.randn(n)*0.3)\ninflation     = pd.Series(2.0 + 0.2*gdp_growth.shift(2).fillna(2) + np.random.randn(n)*0.4)\n\ndf = pd.DataFrame({\'gdp\': gdp_growth, \'unemp\': unemployment, \'inflation\': inflation})\n\nmodel = VAR(df)\nfitted = model.fit(maxlags=6, ic=\'aic\')\nprint(f\"VAR({fitted.k_ar}) AIC={fitted.aic:.2f}\")\n\nfor caused in [\'unemp\',\'inflation\']:\n    test = fitted.test_causality(caused, \'gdp\', kind=\'f\')\n    print(f\"GDP -> {caused}: p={test.pvalue:.4f} {\'(significant)\' if test.pvalue<0.05 else \'\'}\")\n\nfc = pd.DataFrame(\n    fitted.forecast(df.values[-fitted.k_ar:], steps=6),\n    columns=[\'gdp\',\'unemp\',\'inflation\'])\nprint(f\"\\n6-month forecast:\\n{fc.round(3).to_string()}\")",
"practice": {
    "title": "Multivariate Forecasting Pipeline",
    "desc": "Generate 3 correlated time series (temp, humidity, energy_demand) where energy = 0.7*temp_lag1 + 0.4*humidity + noise. (1) Test stationarity, difference if needed. (2) Fit VAR, select lag order by AIC. (3) Test Granger causality of temp -> energy and humidity -> energy. (4) Forecast 6 steps and compare to actual using RMSE.",
    "starter": "import numpy as np, pandas as pd\nfrom statsmodels.tsa.vector_ar.var_model import VAR\nfrom statsmodels.tsa.stattools import adfuller, grangercausalitytests\nimport warnings; warnings.filterwarnings(\'ignore\')\n\nnp.random.seed(42)\nn = 120\ntemp     = pd.Series(20 + 10*np.sin(2*np.pi*np.arange(n)/12) + np.random.randn(n)*2)\nhumidity = pd.Series(60 + 15*np.sin(2*np.pi*(np.arange(n)-3)/12) + np.random.randn(n)*4)\nenergy   = pd.Series(0.7*temp.shift(1).fillna(temp.mean()) + 0.4*humidity + np.random.randn(n)*5 + 20)\n\ndf = pd.DataFrame({\'temp\':temp, \'humidity\':humidity, \'energy\':energy})\n\n# (1) Test stationarity and difference\n# (2) Fit VAR with lag selection\n# (3) Granger causality\n# (4) Forecast and RMSE\n"
}
},


]

# ─── Output ───────────────────────────────────────────────────────────────────
html  = make_html(SECTIONS)
nb    = make_nb(SECTIONS)
(BASE / "index.html").write_text(html, encoding="utf-8")
(BASE / "study_guide.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

n_cells = len(nb["cells"])
print(f"Time Series guide created: {BASE}")
print(f"  index.html:        {(BASE/'index.html').stat().st_size//1024:.1f} KB")
print(f"  study_guide.ipynb: {n_cells} cells")
