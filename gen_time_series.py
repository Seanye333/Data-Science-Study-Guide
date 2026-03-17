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
