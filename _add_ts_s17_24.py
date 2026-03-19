"""Add sections 17-24 to gen_time_series.py."""
import os, re

FILE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_time_series.py"

def ec(s):
    return (s.replace('\\','\\\\').replace('"','\\"')
             .replace('\n','\\n').replace("'","\\'"))

def make_s(num, title, desc, examples, rw_scenario, rw_code, pt, pd_text, ps):
    ex_lines = []
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples)-1 else ''
        ex_lines.append(f'        {{"label": "{ec(ex["label"])}", "code": "{ec(ex["code"])}"}}{comma}')
    ex_block = '\n'.join(ex_lines)
    return (
        f'{{\n"title": "{num}. {title}",\n"desc": "{ec(desc)}",\n'
        f'"examples": [\n{ex_block}\n    ],\n'
        f'"rw_scenario": "{ec(rw_scenario)}",\n"rw_code": "{ec(rw_code)}",\n'
        f'"practice": {{\n    "title": "{ec(pt)}",\n    "desc": "{ec(pd_text)}",\n'
        f'    "starter": "{ec(ps)}"\n}}\n}},\n\n'
    )

def insert_ts(filepath, new_str):
    content = open(filepath, encoding='utf-8').read()
    marker = '\n]\n\n# '
    idx = content.rfind(marker)
    if idx == -1:
        print("ERROR: marker not found"); return False
    before = content[:idx].rstrip()
    sep = ',\n\n' if before.endswith('}') and not before.endswith('},') else '\n'
    content = before + sep + new_str + content[idx:]
    open(filepath, 'w', encoding='utf-8').write(content)
    print(f"OK: inserted into {filepath}"); return True

# ── 17: STL Decomposition ─────────────────────────────────────────────────────
s17 = make_s(17, "Seasonal Decomposition & STL",
    "Time series decompose into Trend, Seasonality, and Residual components. STL (Seasonal-Trend decomposition using LOESS) is robust to outliers and handles arbitrary seasonality. Use it before forecasting to understand your signal.",
    [
        {"label": "Classical decomposition with statsmodels",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

np.random.seed(42)
periods = 120
dates = pd.date_range('2015-01', periods=periods, freq='MS')
trend = np.linspace(100, 160, periods)
seasonal = 15 * np.sin(2 * np.pi * np.arange(periods) / 12)
noise = np.random.normal(0, 5, periods)
ts = pd.Series(trend + seasonal + noise, index=dates)

result = seasonal_decompose(ts, model='additive', period=12)

print("Decomposition components:")
print(f"  Trend range:    [{result.trend.dropna().min():.1f}, {result.trend.dropna().max():.1f}]")
print(f"  Seasonal range: [{result.seasonal.min():.2f}, {result.seasonal.max():.2f}]")
print(f"  Residual std:   {result.resid.dropna().std():.3f}")

# Seasonal indices
seasonal_idx = result.seasonal[:12]
for month, val in zip(range(1, 13), seasonal_idx):
    print(f"  Month {month:2d}: {val:+.2f}")"""},
        {"label": "STL decomposition (robust, flexible seasonality)",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import STL

np.random.seed(0)
n = 156  # 13 years monthly
dates = pd.date_range('2010-01', periods=n, freq='MS')
trend = np.linspace(50, 120, n) + 0.3 * np.sin(np.linspace(0, 4*np.pi, n)) * 10
seasonal = 20 * np.sin(2 * np.pi * np.arange(n) / 12) + \
           8  * np.sin(2 * np.pi * np.arange(n) / 6)
# Inject outliers
noise = np.random.normal(0, 3, n)
outliers = np.zeros(n)
outliers[[30, 60, 90]] = 40
ts = pd.Series(trend + seasonal + noise + outliers, index=dates)

stl = STL(ts, period=12, robust=True)
res = stl.fit()

print(f"STL decomposition of {n}-period series:")
print(f"  Trend variance:    {res.trend.var():.2f}")
print(f"  Seasonal variance: {res.seasonal.var():.2f}")
print(f"  Residual variance: {res.resid.var():.2f}")
print(f"  Seasonal strength: {max(0, 1 - res.resid.var()/(res.seasonal+res.resid).var()):.3f}")
print(f"  Trend strength:    {max(0, 1 - res.resid.var()/(res.trend+res.resid).var()):.3f}")"""},
        {"label": "Trend strength, seasonality strength, and change points",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import STL

np.random.seed(7)
# Monthly retail sales with change point at month 60
n = 120
t = np.arange(n)
trend = np.where(t < 60, 100 + t*0.5, 130 + (t-60)*1.2)
seasonal = 25 * np.sin(2*np.pi*t/12)
noise = np.random.normal(0, 4, n)
ts = pd.Series(trend + seasonal + noise,
               index=pd.date_range('2014-01', periods=n, freq='MS'))

stl = STL(ts, period=12, robust=True)
res = stl.fit()

# Detect change point: where residuals spike
resid_rolling_std = pd.Series(res.resid).rolling(6).std()
change_pt = resid_rolling_std.idxmax()
print(f"Largest residual volatility at index: {change_pt}")

# Year-over-year growth from trend
yoy = pd.Series(res.trend).pct_change(12) * 100
print(f"\\nYear-over-year trend growth (last 3):")
for i in [-3, -2, -1]:
    print(f"  Month {n+i}: {yoy.iloc[i]:.2f}%")

# Identify peak and trough season
monthly_seasonal = [res.seasonal[i::12].mean() for i in range(12)]
peak   = np.argmax(monthly_seasonal) + 1
trough = np.argmin(monthly_seasonal) + 1
print(f"\\nPeak season: month {peak}, Trough: month {trough}")"""}
    ],
    rw_scenario="A retail analyst decomposes 5 years of monthly e-commerce sales using STL to isolate the holiday spike (seasonality) from long-term growth (trend) before building a forecast model.",
    rw_code="""import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import STL

np.random.seed(42)
n = 60
dates = pd.date_range('2019-01', periods=n, freq='MS')
trend    = 1000 + np.linspace(0, 500, n)
seasonal = 300 * np.sin(2*np.pi*np.arange(n)/12) + \
           100 * (np.arange(n) % 12 == 11)   # Dec spike
noise    = np.random.normal(0, 30, n)
sales    = pd.Series(trend + seasonal + noise, index=dates)

stl = STL(sales, period=12, robust=True)
res = stl.fit()

print("Retail Sales Decomposition:")
print(f"  Avg monthly trend growth: ${(res.trend.diff().dropna().mean()):.1f}")
print(f"  Peak seasonal boost: ${res.seasonal.max():.0f}")
print(f"  Residual RMSE: ${np.sqrt((res.resid**2).mean()):.1f}")

# Deseasonalized series for cleaner trend analysis
deseas = sales - res.seasonal
print(f"  Deseasonalized range: [{deseas.min():.0f}, {deseas.max():.0f}]")""",
    pt="Custom STL Pipeline",
    pd_text="Generate 5 years of weekly sales data (trend + two seasonalities: annual 52-week and quarterly 13-week + noise). Apply STL with period=52. Extract and print: (1) Overall trend slope (slope of linear fit to trend component), (2) Peak week of the year seasonally, (3) Percentage of variance explained by trend, seasonal, and residual components.",
    ps="""import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import STL
from scipy import stats as sp_stats

np.random.seed(42)
n = 260  # 5 years weekly
t = np.arange(n)
trend    = 500 + t * 0.8
seasonal = 80 * np.sin(2*np.pi*t/52) + 30 * np.sin(2*np.pi*t/13)
noise    = np.random.normal(0, 20, n)
ts = pd.Series(trend + seasonal + noise,
               index=pd.date_range('2019-01-07', periods=n, freq='W'))

stl = STL(ts, period=52, robust=True)
res = stl.fit()

# (1) trend slope via linear regression on trend component
# (2) peak week (argmax of first 52 seasonal values)
# (3) variance decomposition
total_var = ts.var()
# TODO: compute each component's share
"""
)

# ── 18: Stationarity & ARIMA Prep ─────────────────────────────────────────────
s18 = make_s(18, "Stationarity Testing & ARIMA Preparation",
    "ARIMA requires a stationary series (constant mean/variance). ADF and KPSS tests check stationarity. Differencing and log transforms achieve it. ACF/PACF plots reveal AR and MA orders.",
    [
        {"label": "ADF and KPSS stationarity tests",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

np.random.seed(42)
n = 200
t = np.arange(n)

series = {
    'Random Walk':    np.cumsum(np.random.randn(n)),            # non-stationary
    'Stationary AR1': np.zeros(n),                              # stationary
    'Trend + Noise':  2 + 0.05*t + np.random.randn(n),         # non-stationary (trend)
}
for i in range(1, n):
    series['Stationary AR1'][i] = 0.7*series['Stationary AR1'][i-1] + np.random.randn()

print(f"{'Series':16s}  {'ADF p':>8s}  {'ADF stat':>9s}  {'KPSS p':>8s}  {'Stationary?'}")
print('-' * 60)
for name, data in series.items():
    adf_stat, adf_p, *_ = adfuller(data, autolag='AIC')
    try:
        kpss_stat, kpss_p, *_ = kpss(data, regression='c', nlags='auto')
    except Exception:
        kpss_p = 0.01
    # Stationary: ADF rejects H0 (p<0.05) AND KPSS fails to reject H0 (p>0.05)
    is_stat = (adf_p < 0.05) and (kpss_p > 0.05)
    print(f"{name:16s}  {adf_p:8.4f}  {adf_stat:9.4f}  {kpss_p:8.4f}  {is_stat}")"""},
        {"label": "Differencing, log transform, and Box-Cox",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.stattools import adfuller
from scipy.stats import boxcox

np.random.seed(0)
n = 150
t = np.arange(n)

# Non-stationary: trending with heteroskedastic variance
ts = pd.Series(np.exp(0.02*t + np.cumsum(np.random.randn(n)*0.2)) * 100)

def adf_pvalue(x):
    return adfuller(x.dropna(), autolag='AIC')[1]

print(f"Original:            ADF p={adf_pvalue(ts):.4f} (non-stationary)")

# Log transform (stabilizes variance)
ts_log = np.log(ts)
print(f"Log transform:       ADF p={adf_pvalue(ts_log):.4f}")

# First difference (removes linear trend)
ts_diff1 = ts.diff()
print(f"First difference:    ADF p={adf_pvalue(ts_diff1):.4f}")

# Log + first difference (common for financial series)
ts_log_diff = ts_log.diff()
print(f"Log + diff:          ADF p={adf_pvalue(ts_log_diff):.4f}")

# Seasonal difference (lag=12 for monthly)
ts_sdiff = ts.diff(12)
print(f"Seasonal diff (12):  ADF p={adf_pvalue(ts_sdiff):.4f}")"""},
        {"label": "ACF, PACF, and identifying ARIMA order",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_process import ArmaProcess

np.random.seed(42)
n = 300

# Generate AR(2) process: phi1=0.6, phi2=-0.3
ar_params = np.array([1, -0.6, 0.3])   # AR coefficients (sign convention)
ma_params = np.array([1])
ar2_process = ArmaProcess(ar_params, ma_params)
ar2_data = ar2_process.generate_sample(nsample=n)

# Generate MA(1) process
ar_params2 = np.array([1])
ma_params2 = np.array([1, 0.8])
ma1_process = ArmaProcess(ar_params2, ma_params2)
ma1_data = ma1_process.generate_sample(nsample=n)

for name, data in [('AR(2)', ar2_data), ('MA(1)', ma1_data)]:
    acf_vals  = acf(data,  nlags=10, fft=True)[1:6]  # skip lag 0
    pacf_vals = pacf(data, nlags=10)[1:6]
    conf = 1.96 / np.sqrt(n)
    print(f"\\n{name} — PACF cutoff suggests AR order; ACF cutoff suggests MA order:")
    print(f"  ACF  lags 1-5: {acf_vals.round(3)}")
    print(f"  PACF lags 1-5: {pacf_vals.round(3)}")
    print(f"  95% conf band: ±{conf:.3f}")
    ar_order  = sum(abs(pacf_vals) > conf)
    ma_order  = sum(abs(acf_vals)  > conf)
    print(f"  Suggested: AR order={ar_order}, MA order={ma_order}")"""}
    ],
    rw_scenario="A commodity trader checks whether monthly aluminium prices are stationary before applying ARIMA. ADF fails to reject non-stationarity; first-differencing the log prices produces a stationary series with ACF suggesting MA(1).",
    rw_code="""import numpy as np, pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf

np.random.seed(10)
# Simulate commodity prices (random walk with drift)
n = 120
prices = pd.Series(
    np.exp(np.cumsum(np.random.normal(0.005, 0.04, n))) * 1800,
    index=pd.date_range('2014-01', periods=n, freq='MS'),
    name='Aluminium_USD_t')

def check_stationarity(series, name):
    adf_stat, adf_p, *_ = adfuller(series.dropna(), autolag='AIC')
    print(f"{name:25s}: ADF p={adf_p:.4f} {'[stationary]' if adf_p < 0.05 else '[non-stationary]'}")
    return adf_p < 0.05

check_stationarity(prices, 'Level prices')
check_stationarity(np.log(prices), 'Log prices')
log_diff = np.log(prices).diff().dropna()
check_stationarity(log_diff, 'Log-differenced')

acf_vals  = acf(log_diff,  nlags=8)[1:]
pacf_vals = pacf(log_diff, nlags=8)[1:]
conf = 1.96 / np.sqrt(len(log_diff))
print(f"\\nACF  lags 1-8: {acf_vals.round(3)}")
print(f"PACF lags 1-8: {pacf_vals.round(3)}")
print(f"Suggested ARIMA(p,1,q): p={sum(abs(pacf_vals[:4])>conf)}, q={sum(abs(acf_vals[:4])>conf)}")""",
    pt="Automated Stationarity Pipeline",
    pd_text="Write a function make_stationary(ts, max_diffs=2) that: (1) Tests ADF on the original series, (2) If non-stationary, applies log transform (if all positive) and re-tests, (3) If still non-stationary, applies first differencing, (4) Repeats up to max_diffs times, (5) Returns the stationary series, number of differences applied, and whether log was used.",
    ps="""import numpy as np, pandas as pd
from statsmodels.tsa.stattools import adfuller

def make_stationary(ts, max_diffs=2, alpha=0.05):
    result = ts.copy()
    log_used = False
    n_diffs  = 0
    # (1) check original
    # (2) try log if all positive
    # (3) difference up to max_diffs
    return result, n_diffs, log_used

np.random.seed(42)
ts_rw     = pd.Series(np.cumsum(np.random.randn(100)))
ts_exp    = pd.Series(np.exp(0.03*np.arange(100) + np.random.randn(100)*0.2)*100)
ts_stat   = pd.Series(np.random.randn(100))

for name, ts in [('Random Walk', ts_rw), ('Exponential Trend', ts_exp), ('Stationary', ts_stat)]:
    out, d, log = make_stationary(ts)
    print(f"{name}: diffs={d}, log={log}")
"""
)

# ── 19: ARIMA/SARIMA ──────────────────────────────────────────────────────────
s19 = make_s(19, "ARIMA & SARIMA Modeling",
    "ARIMA(p,d,q) models a stationary process as AutoRegressive + Integrated + Moving Average. SARIMA adds seasonal components (P,D,Q,m). Use AIC/BIC for order selection and residual diagnostics to validate.",
    [
        {"label": "Fitting ARIMA and forecasting",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.arima.model import ARIMA

np.random.seed(42)
n = 120
dates = pd.date_range('2014-01', periods=n, freq='MS')
trend = np.linspace(100, 150, n)
noise = np.cumsum(np.random.normal(0, 2, n))  # AR component
ts = pd.Series(trend + noise, index=dates)

# Fit ARIMA(1,1,1)
model = ARIMA(ts, order=(1, 1, 1))
fitted = model.fit()
print(fitted.summary().tables[1])

# Forecast 12 months ahead
forecast = fitted.get_forecast(steps=12)
pred_mean = forecast.predicted_mean
pred_ci   = forecast.conf_int(alpha=0.05)

print(f"\\n12-month forecast:")
for date, val, lo, hi in zip(pred_mean.index[:3], pred_mean[:3],
                              pred_ci.iloc[:3,0], pred_ci.iloc[:3,1]):
    print(f"  {date.strftime('%Y-%m')}: {val:.1f} [{lo:.1f}, {hi:.1f}]")
print(f"  ...")

# In-sample fit metrics
from sklearn.metrics import mean_squared_error
residuals = fitted.resid
print(f"\\nIn-sample RMSE: {np.sqrt((residuals**2).mean()):.3f}")
print(f"AIC: {fitted.aic:.2f}, BIC: {fitted.bic:.2f}")"""},
        {"label": "SARIMA for seasonal data",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings; warnings.filterwarnings('ignore')

np.random.seed(42)
n = 84  # 7 years monthly
dates = pd.date_range('2017-01', periods=n, freq='MS')
trend    = np.linspace(1000, 1600, n)
seasonal = 200 * np.sin(2*np.pi*np.arange(n)/12)
noise    = np.cumsum(np.random.normal(0, 20, n))
ts = pd.Series(trend + seasonal + noise, index=dates)

# SARIMA(1,1,1)(1,1,1,12)
model = SARIMAX(ts, order=(1,1,1), seasonal_order=(1,1,1,12),
                trend='n', enforce_stationarity=False,
                enforce_invertibility=False)
fitted = model.fit(disp=False)
print(f"SARIMA(1,1,1)(1,1,1,12): AIC={fitted.aic:.2f}, BIC={fitted.bic:.2f}")

# Compare AIC for different orders
for order, sorder in [((0,1,1),(0,1,1,12)), ((1,1,0),(1,1,0,12))]:
    m = SARIMAX(ts, order=order, seasonal_order=sorder,
                enforce_stationarity=False, enforce_invertibility=False)
    f = m.fit(disp=False)
    print(f"SARIMA{order}{sorder}: AIC={f.aic:.2f}")

forecast = fitted.get_forecast(12)
print(f"\\nForecast next month: {forecast.predicted_mean.iloc[0]:.1f}")"""},
        {"label": "Residual diagnostics and model validation",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from scipy import stats
import warnings; warnings.filterwarnings('ignore')

np.random.seed(0)
n = 150
ts = pd.Series(np.cumsum(np.random.normal(0.5, 2, n)) + np.random.randn(n),
               index=pd.date_range('2012-01', periods=n, freq='MS'))

model = ARIMA(ts, order=(1, 1, 1))
fitted = model.fit()
residuals = fitted.resid.dropna()

# Test 1: Ljung-Box (autocorrelation in residuals)
lb = acorr_ljungbox(residuals, lags=[10], return_df=True)
print(f"Ljung-Box p (lag 10): {lb['lb_pvalue'].iloc[0]:.4f}  (>0.05 = no autocorrelation = good)")

# Test 2: Normality of residuals
_, p_sw = stats.shapiro(residuals[:50])
print(f"Shapiro-Wilk p:       {p_sw:.4f}  (>0.05 = normal residuals = good)")

# Test 3: Heteroskedasticity (should be constant variance)
half = len(residuals) // 2
_, p_lev = stats.levene(residuals[:half], residuals[half:])
print(f"Levene p:             {p_lev:.4f}  (>0.05 = equal variance = good)")

print(f"\\nResidual stats: mean={residuals.mean():.4f}, std={residuals.std():.3f}")
print(f"AIC={fitted.aic:.2f}, model is {'adequate' if lb['lb_pvalue'].iloc[0]>0.05 else 'needs improvement'}")"""}
    ],
    rw_scenario="An energy company forecasts monthly natural gas demand for the next 6 months using SARIMA to capture both the yearly seasonal cycle and trend growth, with 95% prediction intervals for capacity planning.",
    rw_code="""import numpy as np, pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings; warnings.filterwarnings('ignore')

np.random.seed(5)
n = 96
dates = pd.date_range('2016-01', periods=n, freq='MS')
trend    = np.linspace(500, 700, n)
seasonal = 150 * np.cos(2*np.pi*np.arange(n)/12)  # peak in winter
noise    = np.cumsum(np.random.normal(0, 10, n))
demand   = pd.Series(trend + seasonal + noise, index=dates, name='Gas_MMcf')

train = demand[:-12]
test  = demand[-12:]

model = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,12),
                enforce_stationarity=False, enforce_invertibility=False)
fitted = model.fit(disp=False)

forecast = fitted.get_forecast(steps=12)
pred   = forecast.predicted_mean
ci     = forecast.conf_int()

from sklearn.metrics import mean_absolute_percentage_error
mape = mean_absolute_percentage_error(test, pred) * 100
rmse = np.sqrt(((test - pred)**2).mean())

print(f"SARIMA(1,1,1)(1,1,1,12) forecast metrics:")
print(f"  MAPE: {mape:.2f}%  RMSE: {rmse:.2f} MMcf")
print(f"  AIC: {fitted.aic:.1f}")
print(f"\\n6-month capacity forecast (MMcf):")
for i in range(6):
    print(f"  {pred.index[i].strftime('%Y-%m')}: {pred.iloc[i]:.0f} [{ci.iloc[i,0]:.0f}-{ci.iloc[i,1]:.0f}]")""",
    pt="Auto-ARIMA Order Selection",
    pd_text="Generate monthly sales data for 4 years with AR(2) dynamics and monthly seasonality. Write a function select_arima_order(ts, max_p=3, max_q=3, d=1) that tries all ARIMA(p,d,q) combinations and returns the order with the lowest AIC. Compare its forecast (12 months) RMSE to naive persistence forecast.",
    ps="""import numpy as np, pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings; warnings.filterwarnings('ignore')

np.random.seed(42)
n = 60
ts = pd.Series(
    100 + np.cumsum(np.random.normal(0, 2, n)) + 20*np.sin(2*np.pi*np.arange(n)/12),
    index=pd.date_range('2019-01', periods=n, freq='MS'))

def select_arima_order(ts, max_p=3, max_q=3, d=1):
    best_aic, best_order = np.inf, None
    for p in range(max_p+1):
        for q in range(max_q+1):
            if p == 0 and q == 0:
                continue
            try:
                m = ARIMA(ts, order=(p, d, q))
                f = m.fit()
                if f.aic < best_aic:
                    best_aic, best_order = f.aic, (p, d, q)
            except Exception:
                pass
    return best_order, best_aic

# TODO: call select_arima_order on train set (first 48 months)
# TODO: forecast last 12 months with best order
# TODO: compare RMSE to naive persistence (repeat last observed value)
"""
)

# ── 20: Exponential Smoothing ─────────────────────────────────────────────────
s20 = make_s(20, "Exponential Smoothing (ETS / Holt-Winters)",
    "Exponential smoothing methods weight recent observations more heavily. Simple ES handles level; Holt's double ES adds trend; Holt-Winters triple ES adds seasonality. The ETS framework unifies them with Error-Trend-Seasonality states.",
    [
        {"label": "Simple, Holt's double, and Holt-Winters",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing
import warnings; warnings.filterwarnings('ignore')

np.random.seed(42)
n = 60
dates = pd.date_range('2019-01', periods=n, freq='MS')
trend    = np.linspace(100, 160, n)
seasonal = 20 * np.sin(2*np.pi*np.arange(n)/12)
noise    = np.random.normal(0, 5, n)
ts = pd.Series(trend + seasonal + noise, index=dates)

train, test = ts[:-12], ts[-12:]

# Simple Exponential Smoothing (level only)
ses = SimpleExpSmoothing(train, initialization_method='estimated').fit()
ses_fc = ses.forecast(12)

# Holt's (trend)
holt = Holt(train, initialization_method='estimated').fit(
    optimized=True, smoothing_level=0.3, smoothing_trend=0.1)
holt_fc = holt.forecast(12)

# Holt-Winters (trend + seasonality)
hw = ExponentialSmoothing(train, trend='add', seasonal='add',
                           seasonal_periods=12,
                           initialization_method='estimated').fit(optimized=True)
hw_fc = hw.forecast(12)

from sklearn.metrics import mean_squared_error
for name, fc in [('SES', ses_fc), ("Holt's", holt_fc), ('Holt-Winters', hw_fc)]:
    rmse = np.sqrt(mean_squared_error(test, fc))
    print(f"{name:15s}: RMSE={rmse:.2f},  alpha={getattr(getattr(ses if name=='SES' else holt if 'Holt' in name and name!='Holt-Winters' else hw,'model',None),'params',{}).get('smoothing_level','N/A')}")"""},
        {"label": "ETS auto-selection and damped trend",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings; warnings.filterwarnings('ignore')

np.random.seed(0)
n = 84
dates = pd.date_range('2017-01', periods=n, freq='MS')
ts = pd.Series(
    np.linspace(200, 320, n) + 30*np.sin(2*np.pi*np.arange(n)/12) +
    np.random.normal(0, 8, n), index=dates)

train, test = ts[:-12], ts[-12:]

configs = [
    ('Additive trend + Additive seasonal',   'add', 'add',  False),
    ('Additive trend + Mult seasonal',        'add', 'mul',  False),
    ('Damped trend + Additive seasonal',      'add', 'add',  True),
]

print(f"{'Model':40s}  {'RMSE':>6s}  {'AIC':>8s}")
for name, trend, seasonal, damped in configs:
    m = ExponentialSmoothing(train, trend=trend, seasonal=seasonal,
                              seasonal_periods=12, damped_trend=damped,
                              initialization_method='estimated')
    fitted = m.fit(optimized=True)
    fc = fitted.forecast(12)
    rmse = np.sqrt(((test - fc)**2).mean())
    print(f"{name:40s}  {rmse:6.2f}  {fitted.aic:8.2f}")"""},
        {"label": "Smoothing parameters and state extraction",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings; warnings.filterwarnings('ignore')

np.random.seed(5)
n = 72
ts = pd.Series(
    150 + np.linspace(0, 50, n) + 25*np.sin(2*np.pi*np.arange(n)/12) +
    np.random.normal(0, 6, n),
    index=pd.date_range('2018-01', periods=n, freq='MS'))

hw = ExponentialSmoothing(ts, trend='add', seasonal='add',
                           seasonal_periods=12,
                           initialization_method='estimated').fit(optimized=True)

print("Optimal smoothing parameters:")
print(f"  alpha (level):    {hw.params['smoothing_level']:.4f}")
print(f"  beta  (trend):    {hw.params['smoothing_trend']:.4f}")
print(f"  gamma (seasonal): {hw.params['smoothing_seasonal']:.4f}")

# Extract level, trend, and seasonal states
level    = hw.level
trend_s  = hw.trend
seasonal = hw.season

print(f"\\nFinal state:")
print(f"  Level:    {level.iloc[-1]:.2f}")
print(f"  Trend:    {trend_s.iloc[-1]:.4f} per period")
print(f"  Seasonal indices (last 12): {seasonal.iloc[-12:].round(2).values}")

fc = hw.forecast(6)
print(f"\\n6-month forecast: {fc.round(1).values}")"""}
    ],
    rw_scenario="A retailer uses Holt-Winters with multiplicative seasonality to forecast weekly ice cream sales, capturing both trend growth and summer/winter seasonality for inventory planning.",
    rw_code="""import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings; warnings.filterwarnings('ignore')

np.random.seed(7)
n_weeks = 104  # 2 years weekly
t = np.arange(n_weeks)
trend_w    = 1000 + t * 3
seasonal_w = 400 * np.sin(2*np.pi*t/52) + 150 * (t % 52 > 44).astype(float)  # summer+holiday
noise_w    = np.random.normal(0, 40, n_weeks)
weekly_sales = pd.Series(
    (trend_w + seasonal_w + noise_w).clip(min=100),
    index=pd.date_range('2022-01-03', periods=n_weeks, freq='W'))

train_w = weekly_sales[:-8]
test_w  = weekly_sales[-8:]

# Try additive and multiplicative seasonal
for seas_type in ['add', 'mul']:
    hw = ExponentialSmoothing(
        train_w, trend='add', seasonal=seas_type,
        seasonal_periods=52, initialization_method='estimated').fit(optimized=True)
    fc = hw.forecast(8)
    rmse = np.sqrt(((test_w - fc)**2).mean())
    mape = (abs(test_w - fc) / test_w).mean() * 100
    print(f"Seasonal={seas_type}: RMSE={rmse:.1f}, MAPE={mape:.2f}%, AIC={hw.aic:.1f}")

# Reorder forecast for next 4 weeks
best_hw = ExponentialSmoothing(weekly_sales, trend='add', seasonal='add',
                                seasonal_periods=52, initialization_method='estimated').fit(optimized=True)
next4 = best_hw.forecast(4)
print(f"\\nNext 4 weeks inventory needs: {next4.round(0).values}")""",
    pt="ETS Grid Search",
    pd_text="Generate 5 years of monthly data with trend + seasonality. Write a grid_search_ets(train, test, h) function that tries all combinations of trend in [None, 'add'], seasonal in [None, 'add', 'mul'], damped in [True, False] (only when trend is not None). Return a DataFrame with columns: model_name, AIC, test_RMSE, test_MAPE. Sort by test_RMSE.",
    ps="""import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings; warnings.filterwarnings('ignore')

np.random.seed(42)
n = 72
ts = pd.Series(100 + np.linspace(0,60,n) + 25*np.sin(2*np.pi*np.arange(n)/12) + np.random.randn(n)*5,
               index=pd.date_range('2018-01', periods=n, freq='MS'))
train, test = ts[:-12], ts[-12:]

def grid_search_ets(train, test, h=12):
    results = []
    # TODO: iterate over trend, seasonal, damped combinations
    # TODO: fit ExponentialSmoothing, forecast h steps
    # TODO: compute AIC, RMSE, MAPE
    # TODO: append to results, return sorted DataFrame
    return pd.DataFrame(results)

print(grid_search_ets(train, test).head(5))
"""
)

# ── 21: ML for Time Series ─────────────────────────────────────────────────────
s21 = make_s(21, "ML Approach: Lag Features & Sklearn",
    "Transform any time series into a supervised ML problem by creating lag features, rolling statistics, and calendar features. This lets you use any sklearn regressor for forecasting.",
    [
        {"label": "Creating lag and rolling features",
         "code": """import numpy as np, pandas as pd

np.random.seed(42)
n = 200
ts = pd.Series(
    100 + np.cumsum(np.random.normal(0.3, 2, n)) +
    15 * np.sin(2*np.pi*np.arange(n)/12),
    index=pd.date_range('2007-01', periods=n, freq='MS'),
    name='sales')

def make_features(ts, lags=6, windows=[3, 6, 12]):
    df = pd.DataFrame({'y': ts})
    # Lag features
    for lag in range(1, lags+1):
        df[f'lag_{lag}'] = ts.shift(lag)
    # Rolling statistics
    for w in windows:
        df[f'roll_mean_{w}']  = ts.shift(1).rolling(w).mean()
        df[f'roll_std_{w}']   = ts.shift(1).rolling(w).std()
        df[f'roll_min_{w}']   = ts.shift(1).rolling(w).min()
    # Calendar features
    df['month']     = ts.index.month
    df['month_sin'] = np.sin(2*np.pi*ts.index.month/12)
    df['month_cos'] = np.cos(2*np.pi*ts.index.month/12)
    df['trend']     = np.arange(len(ts))
    return df.dropna()

features = make_features(ts)
print(f"Feature matrix: {features.shape}")
print(f"Features: {list(features.columns)}")
print(f"\\nSample row:\\n{features.iloc[0].round(3)}")"""},
        {"label": "Sklearn regressor for forecasting (walk-forward)",
         "code": """import numpy as np, pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_percentage_error
import warnings; warnings.filterwarnings('ignore')

np.random.seed(0)
n = 180
ts = pd.Series(
    100 + np.cumsum(np.random.normal(0.3, 1.5, n)) +
    20 * np.sin(2*np.pi*np.arange(n)/12),
    index=pd.date_range('2009-06', periods=n, freq='MS'))

def make_features(ts, lags=12):
    df = pd.DataFrame({'y': ts})
    for lag in range(1, lags+1):
        df[f'lag_{lag}'] = ts.shift(lag)
    df['roll_mean_6'] = ts.shift(1).rolling(6).mean()
    df['roll_std_6']  = ts.shift(1).rolling(6).std()
    df['month_sin']   = np.sin(2*np.pi*ts.index.month/12)
    df['month_cos']   = np.cos(2*np.pi*ts.index.month/12)
    return df.dropna()

data  = make_features(ts)
cutoff = len(data) - 24
X, y  = data.drop('y', axis=1), data['y']

X_tr, X_te = X.iloc[:cutoff], X.iloc[cutoff:]
y_tr, y_te = y.iloc[:cutoff], y.iloc[cutoff:]

model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
model.fit(X_tr, y_tr)
preds = model.predict(X_te)

rmse = np.sqrt(((y_te.values - preds)**2).mean())
mape = mean_absolute_percentage_error(y_te, preds) * 100
print(f"GBR Forecast: RMSE={rmse:.2f}, MAPE={mape:.2f}%")

# Feature importance
imp = pd.Series(model.feature_importances_, index=X.columns).nlargest(5)
print(f"Top features: {imp.round(3).to_dict()}")"""},
        {"label": "Recursive multi-step forecasting",
         "code": """import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor
import warnings; warnings.filterwarnings('ignore')

np.random.seed(42)
n = 150
ts = pd.Series(
    np.cumsum(np.random.normal(0.5, 2, n)) + 100 +
    15 * np.sin(2*np.pi*np.arange(n)/12),
    index=pd.date_range('2012-06', periods=n, freq='MS'))

lags = 6
data = pd.DataFrame({'y': ts})
for l in range(1, lags+1):
    data[f'lag_{l}'] = ts.shift(l)
data['month_sin'] = np.sin(2*np.pi*ts.index.month/12)
data['month_cos'] = np.cos(2*np.pi*ts.index.month/12)
data = data.dropna()

X, y = data.drop('y', axis=1), data['y']
X_tr, X_te = X.iloc[:-12], X.iloc[-12:]
y_tr, y_te = y.iloc[:-12], y.iloc[-12:]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)

# Recursive forecast: use predictions as future lags
history = list(y_tr.values[-lags:])
preds = []
future_idx = pd.date_range(X_te.index[0], periods=12, freq='MS')
for i, date in enumerate(future_idx):
    row = [history[-l] for l in range(1, lags+1)]
    row += [np.sin(2*np.pi*date.month/12), np.cos(2*np.pi*date.month/12)]
    pred = model.predict([row])[0]
    preds.append(pred)
    history.append(pred)

rmse = np.sqrt(((y_te.values - np.array(preds))**2).mean())
print(f"Recursive RF RMSE: {rmse:.2f}")
print(f"True last 3:  {y_te.values[-3:].round(1)}")
print(f"Pred last 3:  {np.array(preds[-3:]).round(1)}")"""}
    ],
    rw_scenario="A logistics company uses a LightGBM model with 24 lag features, rolling means, and one-hot encoded weekday/month to forecast daily parcel volume 7 days ahead, outperforming SARIMA by 30% MAPE.",
    rw_code="""import numpy as np, pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_percentage_error

np.random.seed(42)
n = 365 * 2  # 2 years daily
t = np.arange(n)
daily = pd.Series(
    1000 + 0.5*t +
    300 * np.sin(2*np.pi*t/365) +
    150 * np.sin(2*np.pi*t/7) +   # weekly pattern
    np.random.normal(0, 50, n),
    index=pd.date_range('2022-01-01', periods=n, freq='D'))

def build_features(ts, lags=14):
    df = pd.DataFrame({'y': ts})
    for l in range(1, lags+1):
        df[f'lag_{l}'] = ts.shift(l)
    for w in [7, 14, 30]:
        df[f'rm_{w}'] = ts.shift(1).rolling(w).mean()
    df['dow']        = ts.index.dayofweek
    df['month']      = ts.index.month
    df['week_sin']   = np.sin(2*np.pi*ts.index.dayofweek/7)
    df['week_cos']   = np.cos(2*np.pi*ts.index.dayofweek/7)
    df['annual_sin'] = np.sin(2*np.pi*ts.index.dayofyear/365)
    return df.dropna()

data = build_features(daily)
X, y = data.drop('y', axis=1), data['y']
split = len(data) - 90
X_tr, X_te, y_tr, y_te = X.iloc[:split], X.iloc[split:], y.iloc[:split], y.iloc[split:]

gbr = GradientBoostingRegressor(n_estimators=300, max_depth=5, learning_rate=0.05, random_state=42)
gbr.fit(X_tr, y_tr)
preds = gbr.predict(X_te)

mape = mean_absolute_percentage_error(y_te, preds) * 100
rmse = np.sqrt(((y_te.values - preds)**2).mean())
print(f"Daily volume forecast: MAPE={mape:.2f}%, RMSE={rmse:.1f}")
top5 = pd.Series(gbr.feature_importances_, index=X.columns).nlargest(5)
print(f"Top features: {top5.round(3).to_dict()}")""",
    pt="Feature Engineering for Weekly Data",
    pd_text="Generate 3 years of weekly store sales (trend + annual seasonality + weekly dip on off-season weeks). Create features: lags 1-8, rolling mean/std at 4 and 8 weeks, week-of-year sine/cosine, year indicator. Train RandomForest on first 2.5 years, test on last 6 months. Report RMSE and MAPE. Plot (print) actual vs predicted for the test period.",
    ps="""import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error

np.random.seed(42)
n = 156  # 3 years weekly
t = np.arange(n)
ts = pd.Series(
    5000 + 10*t + 800*np.sin(2*np.pi*t/52) + np.random.normal(0,150,n),
    index=pd.date_range('2021-01-04', periods=n, freq='W'))

# TODO: create lag + rolling + calendar features
# TODO: train/test split (last 26 weeks = test)
# TODO: train RandomForest
# TODO: report RMSE and MAPE
# TODO: print actual vs predicted for test
"""
)

# ── 22: Anomaly Detection in TS ───────────────────────────────────────────────
s22 = make_s(22, "Time Series Anomaly Detection",
    "Detect anomalous time points using statistical control limits, rolling z-scores, STL residuals, and IsolationForest. Different methods suit different anomaly types: spikes, level shifts, or trend changes.",
    [
        {"label": "Rolling z-score and IQR fences",
         "code": """import numpy as np, pandas as pd

np.random.seed(42)
n = 200
ts = pd.Series(
    50 + np.cumsum(np.random.normal(0.1, 1, n)),
    index=pd.date_range('2020-01-01', periods=n, freq='D'))

# Inject anomalies
anomaly_idx = [40, 90, 140, 170]
ts.iloc[anomaly_idx] += np.array([25, -30, 20, -25])

# Method 1: Rolling z-score
window = 20
roll_mean = ts.rolling(window, min_periods=1).mean()
roll_std  = ts.rolling(window, min_periods=1).std().fillna(1)
z_scores  = (ts - roll_mean) / roll_std

anomalies_z = ts[abs(z_scores) > 3]
print(f"Rolling z-score (|z|>3): {len(anomalies_z)} anomalies detected")
print(f"  True: {anomaly_idx}")
print(f"  Detected: {list(anomalies_z.index.strftime('%Y-%m-%d')[:5])}")

# Method 2: IQR fences on rolling window
q1 = ts.rolling(30).quantile(0.25)
q3 = ts.rolling(30).quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
anomalies_iqr = ts[(ts < lower) | (ts > upper)]
print(f"IQR fences: {len(anomalies_iqr)} anomalies detected")"""},
        {"label": "STL residuals for anomaly detection",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import STL

np.random.seed(0)
n = 120
ts = pd.Series(
    100 + np.linspace(0,30,n) + 20*np.sin(2*np.pi*np.arange(n)/12) +
    np.random.normal(0, 3, n),
    index=pd.date_range('2014-01', periods=n, freq='MS'))

# Inject anomalies at specific months
anom_idx = [24, 50, 85, 100]
ts.iloc[anom_idx] += [40, -35, 50, -40]

stl = STL(ts, period=12, robust=True)
res = stl.fit()
residuals = pd.Series(res.resid, index=ts.index)

# Flag residuals beyond 3 sigma (estimated robustly)
from scipy.stats import median_abs_deviation
mad  = median_abs_deviation(residuals.dropna())
robust_std = mad / 0.6745
threshold  = 3 * robust_std

flags = abs(residuals) > threshold
detected = ts[flags]
print(f"STL residual anomaly detection (threshold={threshold:.2f}):")
print(f"  Flagged {flags.sum()} points")
print(f"  True anomaly indices: {anom_idx}")
print(f"  Detected at: {list(detected.index.strftime('%Y-%m')[:6])}")

tp = sum(1 for i in anom_idx if flags.iloc[i])
fp = flags.sum() - tp
print(f"  TP={tp}, FP={fp}")"""},
        {"label": "IsolationForest on windowed features",
         "code": """import numpy as np, pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n = 365
ts = pd.Series(
    100 + 0.05*np.arange(n) + 20*np.sin(2*np.pi*np.arange(n)/365) +
    np.random.normal(0, 4, n),
    index=pd.date_range('2022-01-01', periods=n, freq='D'))

true_anomalies = [50, 120, 200, 280, 340]
ts.iloc[true_anomalies] += np.array([35, -40, 30, -45, 38])

# Build windowed features for each point
window = 7
features = pd.DataFrame({
    'value':      ts,
    'diff1':      ts.diff(),
    'roll_mean':  ts.rolling(window).mean(),
    'roll_std':   ts.rolling(window).std(),
    'z_score':    (ts - ts.rolling(window).mean()) / ts.rolling(window).std(),
}).dropna()

scaler = StandardScaler()
X = scaler.fit_transform(features)

iso = IsolationForest(contamination=len(true_anomalies)/n, random_state=42, n_estimators=200)
preds = iso.fit_predict(X)   # -1 = anomaly

detected_idx = features.index[preds == -1]
print(f"IsolationForest detected: {len(detected_idx)} anomalies")
true_dates = ts.index[true_anomalies]
tp = sum(1 for d in detected_idx if any(abs((d - t).days) <= 2 for t in true_dates))
print(f"True positives (within 2 days): {tp}/{len(true_anomalies)}")"""}
    ],
    rw_scenario="A server monitoring system flags CPU usage anomalies in real-time: rolling z-score catches sudden spikes, while STL residuals detect subtle level shifts that z-score misses after trend changes.",
    rw_code="""import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import STL
from scipy.stats import median_abs_deviation

np.random.seed(42)
n = 1440  # 24 hours × 60 min (1 day, minutely)
t = np.arange(n)
# CPU: daily cycle + trend
cpu = pd.Series(
    40 + 20*np.sin(2*np.pi*t/1440) + np.random.normal(0, 3, n),
    index=pd.date_range('2024-01-01', periods=n, freq='min'))

# Inject anomalies
cpu.iloc[200:210] += 35    # sustained spike
cpu.iloc[800]     += 60    # sudden spike
cpu.iloc[1200]    -= 25    # drop

# Method 1: Rolling z-score (fast, real-time friendly)
w = 60
z = (cpu - cpu.rolling(w).mean()) / cpu.rolling(w).std()
z_flags = (abs(z) > 3).fillna(False)

# Method 2: Hourly aggregation + STL
hourly = cpu.resample('H').mean()
stl = STL(hourly, period=24, robust=True)
resid = pd.Series(stl.fit().resid, index=hourly.index)
mad = median_abs_deviation(resid.dropna())
stl_flags = abs(resid) > 3 * mad / 0.6745

print(f"Rolling z-score flagged: {z_flags.sum()} minutes")
print(f"STL (hourly) flagged:    {stl_flags.sum()} hours")
print(f"Z-score alerts during spike period: {z_flags.iloc[195:215].sum()}")""",
    pt="Multi-Method Anomaly Ensemble",
    pd_text="Generate 2 years of daily temperature data (seasonal + trend + noise). Inject 6 anomalies (3 spikes, 3 drops). Implement 3 detectors: (1) rolling 30-day z-score threshold 3, (2) IQR fence on 30-day window, (3) STL residuals with 3-sigma MAD threshold. Print a table showing which detectors caught each injected anomaly (TP matrix).",
    ps="""import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import STL
from sklearn.ensemble import IsolationForest
from scipy.stats import median_abs_deviation

np.random.seed(42)
n = 730
t = np.arange(n)
ts = pd.Series(
    15 + 0.01*t + 10*np.sin(2*np.pi*t/365) + np.random.normal(0,1.5,n),
    index=pd.date_range('2022-01-01', periods=n, freq='D'),
    name='temperature')

anom_days = [60, 150, 250, 380, 500, 650]
deltas    = [12, -15, 10, -13, 11, -10]
for day, delta in zip(anom_days, deltas):
    ts.iloc[day] += delta

# TODO: implement 3 anomaly detectors
# TODO: print TP matrix for each injected anomaly
"""
)

# ── 23: Evaluation & Backtesting ──────────────────────────────────────────────
s23 = make_s(23, "Forecast Evaluation & Backtesting",
    "RMSE and MAPE are standard forecast metrics but have blind spots. SMAPE handles zeros; MASE benchmarks against naive. Walk-forward backtesting gives realistic performance estimates and detects overfitting to a single test window.",
    [
        {"label": "RMSE, MAPE, MASE, SMAPE",
         "code": """import numpy as np

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred)**2))

def mape(y_true, y_pred):
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def smape(y_true, y_pred):
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2
    mask  = denom > 0
    return np.mean(np.abs(y_true[mask] - y_pred[mask]) / denom[mask]) * 100

def mase(y_true, y_pred, y_train, m=1):
    # Mean Absolute Scaled Error: normalized by naive seasonal forecast error
    naive_err = np.mean(np.abs(np.diff(y_train, n=m)))
    return np.mean(np.abs(y_true - y_pred)) / naive_err

np.random.seed(42)
y_true  = np.array([100, 150, 130, 200, 175, 220, 195, 210])
y_pred  = y_true + np.random.randn(len(y_true)) * 15
y_train = np.array([80, 90, 110, 95, 105, 120, 115, 130, 140] + list(y_true[:4]))

print(f"RMSE:  {rmse(y_true, y_pred):.3f}")
print(f"MAPE:  {mape(y_true, y_pred):.2f}%")
print(f"SMAPE: {smape(y_true, y_pred):.2f}%")
print(f"MASE:  {mase(y_true, y_pred, np.array(y_train)):.3f}  (< 1 = better than naive)")

# Bias and directional accuracy
bias = np.mean(y_pred - y_true)
da   = np.mean(np.sign(np.diff(y_true)) == np.sign(np.diff(y_pred))) * 100
print(f"Bias:  {bias:.3f} (positive = over-forecast)")
print(f"Directional accuracy: {da:.1f}%")"""},
        {"label": "Walk-forward cross-validation",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings; warnings.filterwarnings('ignore')

np.random.seed(42)
n = 84
ts = pd.Series(
    100 + np.linspace(0,50,n) + 20*np.sin(2*np.pi*np.arange(n)/12) +
    np.random.normal(0,5,n),
    index=pd.date_range('2017-01', periods=n, freq='MS'))

def walk_forward_cv(ts, min_train=24, step=6, h=6):
    errors = []
    starts = range(min_train, len(ts) - h + 1, step)
    for start in starts:
        train = ts[:start]
        test  = ts[start:start+h]
        try:
            hw = ExponentialSmoothing(train, trend='add', seasonal='add',
                                       seasonal_periods=12,
                                       initialization_method='estimated').fit(optimized=True)
            fc = hw.forecast(h)
            rmse = np.sqrt(((test.values - fc.values)**2).mean())
            errors.append({'fold': start, 'n_train': len(train),
                           'rmse': rmse, 'mape': (abs(test - fc)/test).mean()*100})
        except Exception:
            pass
    return pd.DataFrame(errors)

cv_results = walk_forward_cv(ts)
print(f"Walk-forward CV ({len(cv_results)} folds):")
print(cv_results.round(2).to_string(index=False))
print(f"\\nMean RMSE: {cv_results.rmse.mean():.3f} ± {cv_results.rmse.std():.3f}")
print(f"Mean MAPE: {cv_results.mape.mean():.2f}%")"""},
        {"label": "Naive benchmarks and Diebold-Mariano test",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings; warnings.filterwarnings('ignore')

np.random.seed(5)
n = 96
ts = pd.Series(
    200 + np.linspace(0,80,n) + 40*np.sin(2*np.pi*np.arange(n)/12) +
    np.random.normal(0,8,n),
    index=pd.date_range('2016-01', periods=n, freq='MS'))

train, test = ts[:-12], ts[-12:]

# Naive benchmarks
naive_persistence = pd.Series([train.iloc[-1]] * 12, index=test.index)  # last value
naive_seasonal    = train.iloc[-12:].values  # same season last year

hw = ExponentialSmoothing(train, trend='add', seasonal='add',
                           seasonal_periods=12, initialization_method='estimated').fit(optimized=True)
hw_fc = hw.forecast(12)

forecasts = {
    'Naive Persist': naive_persistence.values,
    'Naive Seasonal': naive_seasonal,
    'Holt-Winters':  hw_fc.values,
}

print(f"{'Model':18s}  {'RMSE':>7s}  {'MAPE':>7s}")
for name, fc in forecasts.items():
    rmse = np.sqrt(((test.values - fc)**2).mean())
    mape = (abs(test.values - fc) / test.values).mean() * 100
    print(f"{name:18s}  {rmse:7.2f}  {mape:7.2f}%")

# MASE relative to seasonal naive
naive_err = np.mean(np.abs(np.diff(train.values, n=12)))
hw_mase = np.mean(np.abs(test.values - hw_fc.values)) / naive_err
print(f"\\nHolt-Winters MASE vs seasonal naive: {hw_mase:.3f}")"""}
    ],
    rw_scenario="A demand planner evaluates 3 forecasting models (SARIMA, Holt-Winters, ML) using 5-fold walk-forward CV on 3 years of data. MASE relative to seasonal naive reveals which model truly adds value.",
    rw_code="""import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings; warnings.filterwarnings('ignore')

np.random.seed(42)
n = 72
ts = pd.Series(
    500 + np.linspace(0,200,n) + 100*np.sin(2*np.pi*np.arange(n)/12) +
    np.random.normal(0,15,n),
    index=pd.date_range('2018-01', periods=n, freq='MS'))

folds, h = 5, 6
fold_size = (len(ts) - 24) // folds
results = {m: [] for m in ['HW','SARIMA']}

for fold in range(folds):
    cutoff = 24 + fold * fold_size
    train = ts[:cutoff]
    test  = ts[cutoff:cutoff+h]
    if len(test) < h: break
    try:
        hw = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=12,
                                   initialization_method='estimated').fit(optimized=True)
        hw_fc = hw.forecast(h)
        results['HW'].append(np.sqrt(((test.values - hw_fc.values)**2).mean()))
    except: pass
    try:
        sm = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,12),
                     enforce_stationarity=False).fit(disp=False)
        sm_fc = sm.forecast(h)
        results['SARIMA'].append(np.sqrt(((test.values - sm_fc.values)**2).mean()))
    except: pass

for model, rmses in results.items():
    if rmses:
        print(f"{model:8s}: mean RMSE={np.mean(rmses):.2f} ± {np.std(rmses):.2f} ({len(rmses)} folds)")""",
    pt="Comprehensive Forecast Tournament",
    pd_text="Generate 5 years of monthly data. Implement a forecast_tournament(ts, h=12) function that: (1) Runs walk-forward CV (4 folds) on SARIMA, Holt-Winters, and a naive seasonal benchmark, (2) Returns a summary DataFrame with model, mean_RMSE, std_RMSE, mean_MAPE, (3) Declares a winner. Test it on your generated data.",
    ps="""import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings; warnings.filterwarnings('ignore')

def forecast_tournament(ts, h=12, n_folds=4):
    # TODO: implement walk-forward CV for each model
    # TODO: return DataFrame: model, mean_RMSE, std_RMSE, mean_MAPE
    pass

np.random.seed(42)
n = 72
ts = pd.Series(
    300 + np.linspace(0,100,n) + 60*np.sin(2*np.pi*np.arange(n)/12) + np.random.randn(n)*10,
    index=pd.date_range('2018-01', periods=n, freq='MS'))

results = forecast_tournament(ts, h=6, n_folds=4)
print(results)
"""
)

# ── 24: Multivariate & Prophet ────────────────────────────────────────────────
s24 = make_s(24, "Multivariate Time Series & Prophet",
    "VAR models multiple related time series jointly. Granger causality tests whether one series predicts another. Facebook Prophet is a user-friendly forecaster for business time series with holidays and change points.",
    [
        {"label": "Vector Autoregression (VAR)",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.stattools import adfuller

np.random.seed(42)
n = 120
# Two co-moving series: temperature and ice cream sales
temp  = pd.Series(20 + 10*np.sin(2*np.pi*np.arange(n)/12) + np.random.randn(n)*2)
sales = 0.8*temp.shift(1).fillna(0) + np.random.randn(n)*5 + 50

df = pd.DataFrame({'temp': temp, 'sales': sales})
# Difference to achieve stationarity
df_diff = df.diff().dropna()

model = VAR(df_diff)
result = model.fit(maxlags=4, ic='aic')
print(f"VAR({result.k_ar}) fitted. AIC={result.aic:.2f}")
print(f"\\nGranger causality test (temp -> sales):")

lag_order = result.k_ar
test = result.test_causality('sales', 'temp', kind='f')
print(f"  F-stat={test.test_statistic:.3f}, p={test.pvalue:.4f}")
print(f"  Temp Granger-causes sales? {test.pvalue < 0.05}")

fc = result.forecast(df_diff.values[-lag_order:], steps=6)
print(f"\\n6-step forecast (differences):\\n{pd.DataFrame(fc, columns=['temp_d','sales_d']).round(2)}")"""},
        {"label": "Granger causality and cross-correlation",
         "code": """import numpy as np, pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests, ccf

np.random.seed(0)
n = 200
# advertising spend leads to sales with 2-period lag
ad_spend  = pd.Series(np.random.normal(100, 20, n))
sales     = 0.7 * ad_spend.shift(2).fillna(0) + np.random.randn(n) * 15 + 200
web_visits = 0.5 * ad_spend.shift(1).fillna(0) + np.random.randn(n) * 10

df = pd.DataFrame({'sales': sales.diff(), 'ad_spend': ad_spend.diff(),
                   'web': web_visits.diff()}).dropna()

print("Granger causality: ad_spend -> sales (maxlag=5):")
gc = grangercausalitytests(df[['sales','ad_spend']], maxlag=3, verbose=False)
for lag, res in gc.items():
    p = res[0]['ssr_ftest'][1]
    print(f"  lag {lag}: F-p={p:.4f}  {'*' if p<0.05 else ''}")

# Cross-correlation function
cc = ccf(df['ad_spend'], df['sales'], alpha=0.05, unbiased=True)
print(f"\\nCross-correlation (ad_spend, sales) at lags 0-5:")
for lag, r in enumerate(cc[0][:6]):
    print(f"  lag {lag}: r={r:.3f}")"""},
        {"label": "Facebook Prophet forecasting",
         "code": """import numpy as np, pandas as pd
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False
    print("Install: pip install prophet")

if HAS_PROPHET:
    np.random.seed(42)
    n = 180
    dates = pd.date_range('2018-01-01', periods=n, freq='MS')
    trend    = np.linspace(1000, 2000, n)
    seasonal = 300 * np.sin(2*np.pi*np.arange(n)/12)
    noise    = np.random.normal(0, 50, n)
    df = pd.DataFrame({'ds': dates, 'y': trend + seasonal + noise})

    m = Prophet(yearly_seasonality=True, weekly_seasonality=False,
                daily_seasonality=False, changepoint_prior_scale=0.05)
    m.fit(df)

    future = m.make_future_dataframe(periods=24, freq='MS')
    forecast = m.predict(future)

    print(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail(6).round(1).to_string())
    print(f"\\nTrend at end: {forecast['trend'].iloc[-1]:.1f}")
else:
    print("Prophet demo: requires 'pip install prophet'")
    print("Prophet uses additive model: y = trend + seasonality + holidays + error")
    print("Key params: changepoint_prior_scale, seasonality_prior_scale, holidays")"""}
    ],
    rw_scenario="A macroeconomist builds a VAR model on monthly GDP, unemployment, and inflation data to forecast 6 months ahead, using Granger causality to confirm which indicators lead others.",
    rw_code="""import numpy as np, pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR
import warnings; warnings.filterwarnings('ignore')

np.random.seed(7)
n = 120
t = np.arange(n)

# Simulated macro indicators (stationary after differencing)
gdp_growth    = pd.Series(0.5 + 0.3*np.sin(2*np.pi*t/24) + np.random.randn(n)*0.8)
unemployment  = pd.Series(5.0 - 0.4*gdp_growth.shift(1).fillna(5) + np.random.randn(n)*0.3)
inflation     = pd.Series(2.0 + 0.2*gdp_growth.shift(2).fillna(2) + np.random.randn(n)*0.4)

df = pd.DataFrame({'gdp': gdp_growth, 'unemp': unemployment, 'inflation': inflation})

model = VAR(df)
fitted = model.fit(maxlags=6, ic='aic')
print(f"VAR({fitted.k_ar}) AIC={fitted.aic:.2f}")

for caused in ['unemp','inflation']:
    test = fitted.test_causality(caused, 'gdp', kind='f')
    print(f"GDP -> {caused}: p={test.pvalue:.4f} {'(significant)' if test.pvalue<0.05 else ''}")

fc = pd.DataFrame(
    fitted.forecast(df.values[-fitted.k_ar:], steps=6),
    columns=['gdp','unemp','inflation'])
print(f"\\n6-month forecast:\\n{fc.round(3).to_string()}")""",
    pt="Multivariate Forecasting Pipeline",
    pd_text="Generate 3 correlated time series (temp, humidity, energy_demand) where energy = 0.7*temp_lag1 + 0.4*humidity + noise. (1) Test stationarity, difference if needed. (2) Fit VAR, select lag order by AIC. (3) Test Granger causality of temp -> energy and humidity -> energy. (4) Forecast 6 steps and compare to actual using RMSE.",
    ps="""import numpy as np, pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
import warnings; warnings.filterwarnings('ignore')

np.random.seed(42)
n = 120
temp     = pd.Series(20 + 10*np.sin(2*np.pi*np.arange(n)/12) + np.random.randn(n)*2)
humidity = pd.Series(60 + 15*np.sin(2*np.pi*(np.arange(n)-3)/12) + np.random.randn(n)*4)
energy   = pd.Series(0.7*temp.shift(1).fillna(temp.mean()) + 0.4*humidity + np.random.randn(n)*5 + 20)

df = pd.DataFrame({'temp':temp, 'humidity':humidity, 'energy':energy})

# (1) Test stationarity and difference
# (2) Fit VAR with lag selection
# (3) Granger causality
# (4) Forecast and RMSE
"""
)

# ── Assemble ──────────────────────────────────────────────────────────────────
all_sections = s17+s18+s19+s20+s21+s22+s23+s24
result = insert_ts(FILE, all_sections)
print("SUCCESS" if result else "FAILED")
