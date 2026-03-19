"""Add sections 17-24 to gen_streamlit.py (code1/code2/code3 required format)."""
import os

BASE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path"
FILE = os.path.join(BASE, "gen_streamlit.py")

def ct(code, indent="            "):
    lines = code.split('\n')
    parts = []
    for line in lines:
        escaped = line.replace('\\', '\\\\').replace('"', '\\"')
        parts.append(f'{indent}"{escaped}\\n"')
    return "(\n" + "\n".join(parts) + "\n        )"

def ec(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace("'", "\\'")

def make_section(num, title, desc, c1t, c1, c2t, c2, c3t, c3,
                 rw_scenario="", rw_code="", pt="", pd_text="", ps=""):
    s  = f'    {{\n'
    s += f'        "title": "{num}. {title}",\n'
    s += f'        "desc": "{ec(desc)}",\n'
    s += f'        "code1_title": "{c1t}",\n'
    s += f'        "code1": {ct(c1)},\n'
    s += f'        "code2_title": "{c2t}",\n'
    s += f'        "code2": {ct(c2)},\n'
    s += f'        "code3_title": "{c3t}",\n'
    s += f'        "code3": {ct(c3)},\n'
    s += f'        "rw_scenario": "{ec(rw_scenario)}",\n'
    s += f'        "rw_code": {ct(rw_code)},\n'
    s += f'        "practice": {{\n'
    s += f'            "title": "{ec(pt)}",\n'
    s += f'            "desc": "{ec(pd_text)}",\n'
    s += f'            "starter": {ct(ps)},\n'
    s += f'        }},\n'
    s += f'    }},\n'
    return s

def insert_before_make_html(filepath, new_sections_str):
    content = open(filepath, encoding='utf-8').read()
    marker = '\n]\n\n\ndef make_html'
    idx = content.rfind(marker)
    if idx == -1:
        print(f"ERROR: marker not found in {filepath}")
        return False
    before = content[:idx].rstrip()
    if before.endswith('}') and not before.endswith('},'):
        content = before + ',\n\n' + new_sections_str + content[idx:]
    else:
        content = content[:idx] + '\n' + new_sections_str + content[idx:]
    open(filepath, 'w', encoding='utf-8').write(content)
    print(f"OK: inserted sections into {filepath}")
    return True

# ── Section 17: Plotly & Altair Charts ───────────────────────────────────────
s17 = make_section(17, "Plotly & Altair Integration",
    "Streamlit natively supports Plotly, Altair, Matplotlib, and Bokeh charts. st.plotly_chart() and st.altair_chart() render interactive visualizations with hover, zoom, and click events.",
    c1t="Interactive Plotly Charts",
    c1="""
# streamlit_plotly_demo.py
# Run: streamlit run streamlit_plotly_demo.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.title("Interactive Plotly Charts in Streamlit")

# Sample data
np.random.seed(42)
n = 200
df = pd.DataFrame({
    "x": np.random.randn(n),
    "y": np.random.randn(n),
    "category": np.random.choice(["A", "B", "C"], n),
    "size": np.random.uniform(5, 20, n),
    "value": np.random.randn(n) * 100,
})

# Sidebar controls
st.sidebar.header("Chart Controls")
chart_type = st.sidebar.selectbox("Chart Type", ["Scatter", "Bar", "Histogram", "Box"])
color_col = st.sidebar.selectbox("Color By", ["category"])
selected_cats = st.sidebar.multiselect("Categories", ["A", "B", "C"], default=["A", "B", "C"])

filtered_df = df[df["category"].isin(selected_cats)]

if chart_type == "Scatter":
    fig = px.scatter(filtered_df, x="x", y="y", color=color_col,
                     size="size", hover_data=["value"],
                     title="Scatter Plot")
elif chart_type == "Bar":
    bar_data = filtered_df.groupby("category")["value"].mean().reset_index()
    fig = px.bar(bar_data, x="category", y="value",
                 color="category", title="Mean Value by Category")
elif chart_type == "Histogram":
    fig = px.histogram(filtered_df, x="value", color=color_col,
                       nbins=30, title="Value Distribution")
else:
    fig = px.box(filtered_df, x="category", y="value",
                 color=color_col, title="Value Distribution by Category")

st.plotly_chart(fig, use_container_width=True)
st.dataframe(filtered_df.describe(), use_container_width=True)
""".strip(),
    c2t="Altair Charts",
    c2="""
# streamlit_altair_demo.py
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.title("Altair Charts in Streamlit")

np.random.seed(42)
n = 300

# Time series data
dates = pd.date_range("2024-01-01", periods=n, freq="D")
df = pd.DataFrame({
    "date": dates,
    "value_A": np.cumsum(np.random.randn(n)) + 50,
    "value_B": np.cumsum(np.random.randn(n)) + 45,
})
df_melt = df.melt(id_vars="date", value_vars=["value_A", "value_B"],
                   var_name="series", value_name="value")

# Altair line chart with selection
selection = alt.selection_point(fields=["series"], bind="legend")

chart = (alt.Chart(df_melt)
    .mark_line()
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", title="Value"),
        color=alt.Color("series:N"),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    )
    .add_params(selection)
    .properties(width="container", height=300, title="Interactive Time Series")
)

st.altair_chart(chart, use_container_width=True)

# Heatmap
heatmap_data = pd.DataFrame(
    np.random.randn(10, 10),
    columns=[f"F{i}" for i in range(10)]
).reset_index().melt(id_vars="index", var_name="feature", value_name="corr")

heatmap = (alt.Chart(heatmap_data)
    .mark_rect()
    .encode(
        x="feature:N",
        y=alt.Y("index:O"),
        color=alt.Color("corr:Q", scale=alt.Scale(scheme="redblue")),
        tooltip=["feature", "index", "corr"],
    )
    .properties(height=200, title="Feature Correlation Heatmap")
)
st.altair_chart(heatmap, use_container_width=True)
""".strip(),
    c3t="Combined Dashboard Layout",
    c3="""
# streamlit_dashboard_demo.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Sales Dashboard")
st.title("Sales Performance Dashboard")

np.random.seed(42)
n = 500
df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=n, freq="D")[:n % 365 + 1].tolist() * (n // 365 + 1),
    "product": np.random.choice(["Widget", "Gadget", "Doohickey"], n),
    "region": np.random.choice(["North", "South", "East", "West"], n),
    "revenue": np.random.exponential(500, n).round(2),
    "units": np.random.randint(1, 50, n),
})
df["date"] = pd.date_range("2024-01-01", periods=n, freq="D")[:n]

# KPI row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}", "+12%")
col2.metric("Total Units", f"{df['units'].sum():,}", "+8%")
col3.metric("Avg Order Value", f"${df['revenue'].mean():.2f}", "+4%")
col4.metric("Active Products", "3", "0")

st.divider()

# Two-column chart layout
col_left, col_right = st.columns(2)
with col_left:
    monthly = df.groupby(df["date"].dt.month)["revenue"].sum().reset_index()
    monthly.columns = ["month", "revenue"]
    fig1 = px.bar(monthly, x="month", y="revenue", title="Monthly Revenue")
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    by_region = df.groupby("region")["revenue"].sum().reset_index()
    fig2 = px.pie(by_region, names="region", values="revenue", title="Revenue by Region")
    st.plotly_chart(fig2, use_container_width=True)

# Data table with search
st.subheader("Raw Data")
search = st.text_input("Search product:", "")
filtered = df[df["product"].str.contains(search, case=False)] if search else df
st.dataframe(filtered.head(20), use_container_width=True)
""".strip(),
    rw_scenario="Build a sales analytics dashboard with Plotly charts, date range filters, metric cards showing KPIs, and a downloadable data table. Include a line chart with 30-day moving average.",
    rw_code="""
# streamlit_sales_rw.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide", page_title="Sales Analytics")
st.title("Sales Analytics Dashboard")

# Generate sample data
np.random.seed(42)
n = 365
df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=n),
    "product": np.random.choice(["Product A", "Product B", "Product C"], n),
    "region": np.random.choice(["North", "South", "East", "West"], n),
    "revenue": np.random.exponential(500, n).round(2),
    "units": np.random.randint(1, 100, n),
})

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Date Range",
    value=(df["date"].min(), df["date"].max()),
    min_value=df["date"].min(), max_value=df["date"].max())
selected_products = st.sidebar.multiselect("Products", df["product"].unique(), default=df["product"].unique())

# Filter
mask = ((df["date"] >= pd.Timestamp(date_range[0])) &
        (df["date"] <= pd.Timestamp(date_range[1])) &
        (df["product"].isin(selected_products)))
filtered = df[mask]

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"${filtered['revenue'].sum():,.0f}")
c2.metric("Total Units", f"{filtered['units'].sum():,}")
c3.metric("Orders", f"{len(filtered):,}")

# Line chart with MA
daily = filtered.groupby("date")["revenue"].sum().reset_index()
daily["MA30"] = daily["revenue"].rolling(30).mean()

fig = go.Figure()
fig.add_trace(go.Scatter(x=daily["date"], y=daily["revenue"], name="Daily Revenue", opacity=0.5))
fig.add_trace(go.Scatter(x=daily["date"], y=daily["MA30"], name="30-day MA", line=dict(width=3)))
fig.update_layout(title="Daily Revenue with Moving Average")
st.plotly_chart(fig, use_container_width=True)

# Download
csv_buffer = filtered.to_csv(index=False).encode()
st.download_button("Download Data", csv_buffer, "sales_data.csv", "text/csv")
""".strip(),
    pt="Interactive Chart with Filter",
    pd_text="Build a Streamlit app with a selectbox to choose chart type (bar/scatter/histogram), filter data by a multiselect widget, and display the chart with st.plotly_chart().",
    ps="""
# my_chart_app.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "category": np.random.choice(["A","B","C"], 200),
    "x": np.random.randn(200),
    "y": np.random.randn(200),
    "value": np.random.randn(200) * 100,
})

st.title("My Chart App")
# 1. Add selectbox for chart type
# 2. Add multiselect for categories
# 3. Filter df by selected categories
# 4. Create plotly figure based on chart type
# 5. st.plotly_chart(fig, use_container_width=True)
""".strip()
)

# ── Section 18: Session State Management ─────────────────────────────────────
s18 = make_section(18, "Session State Management",
    "Streamlit reruns the script on every interaction. Session state (st.session_state) persists data across reruns, enabling counters, multi-step forms, authentication, and conversation history.",
    c1t="Counter & Persistent Data",
    c1="""
# streamlit_session_state.py
import streamlit as st
import pandas as pd
import numpy as np

st.title("Session State Examples")

# Example 1: Counter
st.header("Counter (persists across reruns)")

if "count" not in st.session_state:
    st.session_state.count = 0
if "history" not in st.session_state:
    st.session_state.history = []

col1, col2, col3 = st.columns(3)
if col1.button("Increment"):
    st.session_state.count += 1
    st.session_state.history.append(st.session_state.count)
if col2.button("Decrement"):
    st.session_state.count -= 1
    st.session_state.history.append(st.session_state.count)
if col3.button("Reset"):
    st.session_state.count = 0
    st.session_state.history = []

st.metric("Current Count", st.session_state.count)
if st.session_state.history:
    st.line_chart(pd.DataFrame({"count": st.session_state.history}))

# Example 2: Shopping cart
st.header("Shopping Cart")

PRODUCTS = {"Widget": 9.99, "Gadget": 24.99, "Doohickey": 4.99}

if "cart" not in st.session_state:
    st.session_state.cart = {}

col_a, col_b = st.columns(2)
with col_a:
    product = st.selectbox("Add to cart:", list(PRODUCTS.keys()))
    qty = st.number_input("Quantity:", min_value=1, max_value=10, value=1)
    if st.button("Add"):
        st.session_state.cart[product] = st.session_state.cart.get(product, 0) + qty
        st.success(f"Added {qty}x {product}")

with col_b:
    if st.session_state.cart:
        st.write("Cart:")
        total = 0
        for item, qty in st.session_state.cart.items():
            cost = PRODUCTS[item] * qty
            total += cost
            st.write(f"  - {item} x{qty}: ${cost:.2f}")
        st.write(f"**Total: ${total:.2f}**")
        if st.button("Clear Cart"):
            st.session_state.cart = {}
    else:
        st.info("Cart is empty")
""".strip(),
    c2t="Multi-Step Wizard",
    c2="""
# streamlit_wizard.py
import streamlit as st

st.title("Multi-Step Form Wizard")

# Initialize wizard state
if "step" not in st.session_state:
    st.session_state.step = 1
if "data" not in st.session_state:
    st.session_state.data = {}

# Progress bar
progress = (st.session_state.step - 1) / 3
st.progress(progress, text=f"Step {st.session_state.step} of 3")

# Step 1: Personal Info
if st.session_state.step == 1:
    st.subheader("Step 1: Personal Information")
    name = st.text_input("Full Name", value=st.session_state.data.get("name", ""))
    email = st.text_input("Email", value=st.session_state.data.get("email", ""))
    age = st.number_input("Age", min_value=18, max_value=120,
                          value=st.session_state.data.get("age", 25))
    if st.button("Next"):
        if name and email:
            st.session_state.data.update({"name": name, "email": email, "age": age})
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Please fill all required fields")

# Step 2: Preferences
elif st.session_state.step == 2:
    st.subheader("Step 2: Preferences")
    interests = st.multiselect("Interests",
        ["Python", "Data Science", "Machine Learning", "Web Dev", "Cloud"],
        default=st.session_state.data.get("interests", []))
    experience = st.select_slider("Experience Level",
        options=["Beginner", "Intermediate", "Advanced", "Expert"],
        value=st.session_state.data.get("experience", "Intermediate"))
    col1, col2 = st.columns(2)
    if col1.button("Back"):
        st.session_state.step = 1; st.rerun()
    if col2.button("Next"):
        st.session_state.data.update({"interests": interests, "experience": experience})
        st.session_state.step = 3; st.rerun()

# Step 3: Review & Submit
elif st.session_state.step == 3:
    st.subheader("Step 3: Review & Submit")
    st.write("Summary:")
    for key, val in st.session_state.data.items():
        st.write(f"  **{key.title()}:** {val}")
    col1, col2 = st.columns(2)
    if col1.button("Back"): st.session_state.step = 2; st.rerun()
    if col2.button("Submit"):
        st.success("Registration complete!")
        st.balloons()
        st.session_state.step = 1; st.session_state.data = {}
""".strip(),
    c3t="Chatbot with Conversation History",
    c3="""
# streamlit_chatbot.py
import streamlit as st

st.title("Chatbot with Conversation History")
st.caption("Session state preserves chat history across reruns")

# Initialize conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]
if "user_count" not in st.session_state:
    st.session_state.user_count = 0

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Type a message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_count += 1

    # Generate response (mock - replace with real LLM call)
    response = f"You said: '{prompt}' (message #{st.session_state.user_count})"

    # Keyword-based mock responses
    prompt_lower = prompt.lower()
    if "hello" in prompt_lower or "hi" in prompt_lower:
        response = "Hi there! Great to meet you!"
    elif "help" in prompt_lower:
        response = "I can help with data science, Python, and ML questions!"
    elif "python" in prompt_lower:
        response = "Python is great for data science! Try libraries like pandas, sklearn, and torch."
    elif "reset" in prompt_lower:
        st.session_state.messages = []
        st.session_state.user_count = 0
        st.rerun()

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Sidebar stats
with st.sidebar:
    st.metric("Messages", len(st.session_state.messages))
    st.metric("User messages", st.session_state.user_count)
    if st.button("Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Chat cleared. How can I help?"}]
        st.session_state.user_count = 0
        st.rerun()
""".strip(),
    rw_scenario="Build a multi-step data analysis wizard: Step 1 uploads a CSV, Step 2 selects columns and chart type, Step 3 shows the chart with a download button. Use session state to pass data between steps.",
    rw_code="""
# streamlit_wizard_rw.py
import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

st.title("Data Analysis Wizard")

if "step" not in st.session_state: st.session_state.step = 1
if "df" not in st.session_state: st.session_state.df = None
if "config" not in st.session_state: st.session_state.config = {}

st.progress((st.session_state.step - 1) / 2, text=f"Step {st.session_state.step}/3")

if st.session_state.step == 1:
    st.subheader("Step 1: Upload Data")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        st.session_state.df = pd.read_csv(uploaded)
        st.write(f"Loaded {len(st.session_state.df)} rows, {len(st.session_state.df.columns)} columns")
        st.dataframe(st.session_state.df.head(3))
    else:
        # Demo data
        import numpy as np
        np.random.seed(42)
        st.session_state.df = pd.DataFrame({
            "category": np.random.choice(["A","B","C"], 100),
            "x": np.random.randn(100), "y": np.random.randn(100),
            "value": np.random.exponential(50, 100).round(2),
        })
        st.info("Using demo data (upload CSV to use your own data)")
    if st.button("Next -> Configure"):
        st.session_state.step = 2; st.rerun()

elif st.session_state.step == 2:
    df = st.session_state.df
    st.subheader("Step 2: Configure Chart")
    chart_type = st.selectbox("Chart Type", ["scatter", "bar", "histogram", "box"])
    cols = df.columns.tolist()
    x_col = st.selectbox("X Axis", cols)
    y_col = st.selectbox("Y Axis", [c for c in cols if c != x_col])
    color_col = st.selectbox("Color By (optional)", ["None"] + cols)
    color_col = None if color_col == "None" else color_col
    st.session_state.config = {"chart_type": chart_type, "x": x_col, "y": y_col, "color": color_col}
    col1, col2 = st.columns(2)
    if col1.button("Back"): st.session_state.step = 1; st.rerun()
    if col2.button("Next -> View Chart"): st.session_state.step = 3; st.rerun()

elif st.session_state.step == 3:
    df = st.session_state.df; cfg = st.session_state.config
    st.subheader("Step 3: Analysis Results")
    px_fns = {"scatter": px.scatter, "bar": px.bar, "histogram": px.histogram, "box": px.box}
    fig = px_fns[cfg["chart_type"]](df, x=cfg["x"], y=cfg["y"], color=cfg["color"])
    st.plotly_chart(fig, use_container_width=True)
    csv = df.to_csv(index=False).encode()
    st.download_button("Download Data", csv, "results.csv", "text/csv")
    if st.button("Start Over"): st.session_state.step = 1; st.session_state.config = {}; st.rerun()
""".strip(),
    pt="Session State Counter",
    pd_text="Build a Streamlit app with session state that tracks a counter, shows the history as a line chart, and has increment/decrement/reset buttons.",
    ps="""
# session_counter.py
import streamlit as st
import pandas as pd

st.title("Session State Counter")

# 1. Initialize session_state.count = 0 and session_state.history = []
# 2. Add three columns with Increment, Decrement, Reset buttons
# 3. Update count and append to history on each button click
# 4. Show st.metric for current count
# 5. Show st.line_chart of history if it exists
""".strip()
)

# ── Section 19: Caching & Performance ────────────────────────────────────────
s19 = make_section(19, "Caching & Performance",
    "Streamlit reruns the entire script on every interaction. @st.cache_data caches function outputs by input arguments. @st.cache_resource caches singleton objects like ML models and DB connections.",
    c1t="@st.cache_data for Data Loading",
    c1="""
# streamlit_caching.py
import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Caching Demo")

# @st.cache_data: caches DataFrames, arrays, and serializable objects
@st.cache_data
def load_data(n_rows=1000):
    st.write("(Loading data... this message only appears once)")
    time.sleep(0.5)  # simulate slow loading
    np.random.seed(42)
    return pd.DataFrame({
        "id": range(n_rows),
        "category": np.random.choice(list("ABCDE"), n_rows),
        "value": np.random.randn(n_rows) * 100,
        "date": pd.date_range("2024-01-01", periods=n_rows, freq="h"),
    })

@st.cache_data(ttl=300)  # expire after 5 minutes
def expensive_computation(df, agg_col):
    time.sleep(0.3)  # simulate expensive computation
    return df.groupby(agg_col)["value"].agg(["mean", "std", "sum", "count"])

# Load data (cached after first load)
n = st.slider("Number of rows", 100, 5000, 1000)
t0 = time.time()
df = load_data(n)
t1 = time.time()

st.success(f"Data loaded in {(t1-t0)*1000:.1f}ms (cached after first load)")
st.write(f"Shape: {df.shape}")

# Computation (cached per column selection)
agg_col = st.selectbox("Group by", ["category"])
t0 = time.time()
result = expensive_computation(df, agg_col)
t1 = time.time()
st.write(f"Computation time: {(t1-t0)*1000:.1f}ms")
st.dataframe(result)

# Cache info
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache cleared!")
""".strip(),
    c2t="@st.cache_resource for Models & Connections",
    c2="""
# streamlit_cache_resource.py
import streamlit as st
import pickle
import numpy as np
import time

st.title("Cache Resource: ML Models & Connections")

# @st.cache_resource: for singletons (models, DB connections)
# NOT re-created on every rerun - shared across all sessions

@st.cache_resource
def load_ml_model():
    # Simulate loading a large ML model
    st.write("(Loading model... only once per session)")
    time.sleep(1.0)

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris
    X, y = load_iris(return_X_y=True)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

@st.cache_resource
def get_feature_names():
    from sklearn.datasets import load_iris
    return load_iris().feature_names

# Load model (shared across all users)
st.info("The model loads once and is shared across all users")
t0 = time.time()
model = load_ml_model()
feature_names = get_feature_names()
t1 = time.time()
st.success(f"Model loaded in {(t1-t0)*1000:.1f}ms (instant if cached)")

# Prediction interface
st.subheader("Iris Classifier")
col_inputs = st.columns(4)
values = []
for i, (col, fname) in enumerate(zip(col_inputs, feature_names)):
    v = col.number_input(fname, min_value=0.0, max_value=10.0,
                          value=[5.1, 3.5, 1.4, 0.2][i], step=0.1)
    values.append(v)

if st.button("Predict"):
    pred = model.predict([values])[0]
    prob = model.predict_proba([values])[0]
    classes = ["setosa", "versicolor", "virginica"]
    st.write(f"Prediction: **{classes[pred]}** ({prob[pred]*100:.1f}% confidence)")
    st.bar_chart({classes[i]: float(p) for i, p in enumerate(prob)})
""".strip(),
    c3t="Performance Tips & Lazy Loading",
    c3="""
# streamlit_performance_tips.py
import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Performance Best Practices")

st.header("1. Use st.empty() and placeholders for updates")
placeholder = st.empty()

if st.button("Simulate Real-time Updates"):
    for i in range(5):
        with placeholder.container():
            st.metric("Progress", f"{i*20}%")
            st.progress(i / 4)
        time.sleep(0.3)
    with placeholder.container():
        st.success("Done!")

st.header("2. Fragment for partial reruns (Streamlit 1.33+)")
st.code('''
@st.fragment
def update_chart():
    # Only this fragment reruns when its widgets change
    data = st.slider("Data points", 10, 100, 50)
    chart_data = pd.DataFrame(np.random.randn(data, 2), columns=["A", "B"])
    st.line_chart(chart_data)

update_chart()
''')

st.header("3. Batch state updates with callbacks")
def increment():
    st.session_state.fast_count = st.session_state.get("fast_count", 0) + 1

if "fast_count" not in st.session_state:
    st.session_state.fast_count = 0

st.button("Fast Increment", on_click=increment)
st.write(f"Count: {st.session_state.fast_count}")

st.header("4. Performance tips")
tips = [
    "Use @st.cache_data for data loading (TTL to auto-refresh)",
    "Use @st.cache_resource for ML models, DB connections",
    "Avoid heavy computation in the main script body",
    "Use st.fragment for partial reruns (avoids full re-render)",
    "Use on_click callbacks instead of manual state checks",
    "Limit st.dataframe to <10K rows for performance",
]
for tip in tips:
    st.write(f"- {tip}")
""".strip(),
    rw_scenario="Your dashboard loads a 500MB dataset and runs a slow ML prediction on every user interaction. Cache the data load (TTL=10 minutes) and model (resource cache). Measure the speedup.",
    rw_code="""
# streamlit_caching_rw.py
import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Optimized Dashboard with Caching")

@st.cache_data(ttl=600)  # 10-minute TTL
def load_large_dataset(seed=42):
    np.random.seed(seed)
    n = 50_000  # simulate large dataset
    time.sleep(0.2)  # simulate I/O delay
    return pd.DataFrame({
        "date": pd.date_range("2023-01-01", periods=n, freq="h"),
        "product": np.random.choice(["A","B","C","D","E"], n),
        "region": np.random.choice(["North","South","East","West"], n),
        "revenue": np.random.exponential(100, n).round(2),
        "units": np.random.randint(1, 50, n),
    })

@st.cache_resource
def load_model():
    from sklearn.ensemble import RandomForestRegressor
    time.sleep(0.5)  # simulate model loading
    np.random.seed(42)
    X = np.random.randn(1000, 5)
    y = X.sum(axis=1) + np.random.randn(1000) * 0.1
    return RandomForestRegressor(n_estimators=50, random_state=42).fit(X, y)

# Timing
t0 = time.time()
df = load_large_dataset()
load_time = (time.time()-t0)*1000

t0 = time.time()
model = load_model()
model_time = (time.time()-t0)*1000

st.success(f"Data loaded: {load_time:.1f}ms | Model loaded: {model_time:.1f}ms")
st.info("Reload the page - both should be ~0ms on second load (cached!)")

# Dashboard
c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
c2.metric("Total Units", f"{df['units'].sum():,}")
c3.metric("Data Points", f"{len(df):,}")

product = st.selectbox("Product", df["product"].unique())
filtered = df[df["product"] == product]
st.bar_chart(filtered.groupby(filtered["date"].dt.month)["revenue"].sum())

# Prediction
features = np.random.randn(1, 5)
pred = model.predict(features)[0]
st.metric("Predicted Revenue (Random)", f"${pred:.2f}")
""".strip(),
    pt="Cached Data Loader",
    pd_text="Create a @st.cache_data function that generates a large DataFrame (simulates a slow database query with time.sleep). Show that the second call is instantaneous.",
    ps="""
# cache_demo.py
import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Define load_data() with @st.cache_data
#    - time.sleep(1) to simulate slow loading
#    - Returns pd.DataFrame with 10K rows

# 2. Call load_data() and time it with time.time()
# 3. Show st.metric("Load time", f"{elapsed:.0f}ms")
# 4. Note: first call is slow, subsequent calls are ~0ms
""".strip()
)

# ── Section 20: Forms & Input Validation ─────────────────────────────────────
s20 = make_section(20, "Forms & Input Validation",
    "st.form() groups widgets and defers Streamlit reruns until the form is submitted. This prevents partial state updates and improves UX for multi-field inputs like search or settings panels.",
    c1t="st.form() Basics",
    c1="""
# streamlit_forms.py
import streamlit as st
import pandas as pd
import numpy as np

st.title("Forms & Input Validation")

# Without form: every widget change triggers a rerun
st.subheader("Without Form (instant reruns)")
name_no_form = st.text_input("Name (no form)", "Alice")
age_no_form = st.number_input("Age (no form)", 18, 120, 25)
st.write(f"Name: {name_no_form}, Age: {age_no_form}")

st.divider()

# With form: batch inputs, rerun only on submit
st.subheader("With Form (batched submit)")

with st.form("user_profile_form"):
    st.write("Fill in your profile:")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", "Alice Johnson")
        email = st.text_input("Email", "alice@example.com")
        age = st.number_input("Age", min_value=18, max_value=120, value=30)
    with col2:
        role = st.selectbox("Role", ["Data Scientist", "ML Engineer", "Analyst", "Manager"])
        experience = st.slider("Years of Experience", 0, 30, 5)
        skills = st.multiselect("Skills", ["Python", "SQL", "R", "ML", "DL", "Cloud"])

    newsletter = st.checkbox("Subscribe to newsletter", value=True)
    submitted = st.form_submit_button("Save Profile", use_container_width=True)

if submitted:
    profile = {
        "name": name, "email": email, "age": age,
        "role": role, "experience": experience,
        "skills": skills, "newsletter": newsletter
    }
    st.success("Profile saved!")
    st.json(profile)
""".strip(),
    c2t="Input Validation with Forms",
    c2="""
# streamlit_validation.py
import streamlit as st
import re
import pandas as pd
import numpy as np

st.title("Form Input Validation")

# Validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    digits = re.sub(r'[^\\d]', '', phone)
    return len(digits) == 10

def validate_age(age):
    return 18 <= age <= 120

with st.form("validated_form"):
    st.subheader("Registration Form")
    name = st.text_input("Full Name *")
    email = st.text_input("Email *")
    phone = st.text_input("Phone (10 digits)")
    age = st.number_input("Age *", min_value=0, max_value=150, value=25)
    password = st.text_input("Password *", type="password")
    confirm_pw = st.text_input("Confirm Password *", type="password")

    submitted = st.form_submit_button("Register")

if submitted:
    errors = []

    if not name.strip():
        errors.append("Full name is required")

    if not validate_email(email):
        errors.append(f"Invalid email: {email}")

    if phone and not validate_phone(phone):
        errors.append(f"Invalid phone number (need 10 digits)")

    if not validate_age(age):
        errors.append(f"Age must be between 18 and 120")

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    if password != confirm_pw:
        errors.append("Passwords do not match")

    if errors:
        for err in errors:
            st.error(err)
    else:
        st.success(f"Welcome, {name}! Registration successful.")
        st.balloons()
""".strip(),
    c3t="Search & Filter Form",
    c3="""
# streamlit_search_form.py
import streamlit as st
import pandas as pd
import numpy as np

st.title("Search & Filter Interface")

np.random.seed(42)
n = 1000
df = pd.DataFrame({
    "product_id": range(1, n+1),
    "name": [f"Product_{i}" for i in range(1, n+1)],
    "category": np.random.choice(["Electronics","Clothing","Books","Sports","Food"], n),
    "price": np.random.exponential(50, n).round(2),
    "rating": np.random.uniform(1, 5, n).round(1),
    "in_stock": np.random.choice([True, False], n, p=[0.8, 0.2]),
})

# Search form (no reruns until Search is clicked)
with st.form("search_form"):
    st.subheader("Filter Products")
    col1, col2, col3 = st.columns(3)
    with col1:
        search_text = st.text_input("Search by name")
        categories = st.multiselect("Category",
            df["category"].unique().tolist(),
            default=df["category"].unique().tolist())
    with col2:
        min_price, max_price = st.slider("Price Range ($)",
            0.0, float(df["price"].max()), (0.0, 100.0))
        min_rating = st.slider("Minimum Rating", 1.0, 5.0, 3.0, 0.5)
    with col3:
        in_stock_only = st.checkbox("In Stock Only", value=False)
        sort_by = st.selectbox("Sort By", ["rating", "price", "name"])
        sort_desc = st.checkbox("Sort Descending", value=True)

    searched = st.form_submit_button("Search", use_container_width=True)

if searched or True:  # show all initially
    filtered = df[
        (df["category"].isin(categories)) &
        (df["price"] >= min_price) & (df["price"] <= max_price) &
        (df["rating"] >= min_rating)
    ]
    if search_text:
        filtered = filtered[filtered["name"].str.contains(search_text, case=False)]
    if in_stock_only:
        filtered = filtered[filtered["in_stock"]]
    filtered = filtered.sort_values(sort_by, ascending=not sort_desc)

    st.write(f"Found {len(filtered)} products")
    st.dataframe(filtered.head(20), use_container_width=True)
""".strip(),
    rw_scenario="Build a data analysis form with file upload, column selection, validation (check numeric columns exist), and display results. Show meaningful error messages for invalid inputs.",
    rw_code="""
# streamlit_analysis_form.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("Dataset Analysis Form")

# Generate sample or upload
uploaded = st.file_uploader("Upload CSV (optional)", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    np.random.seed(42)
    df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=200, freq="D"),
        "region": np.random.choice(["North","South","East","West"], 200),
        "sales": np.random.exponential(500, 200).round(2),
        "units": np.random.randint(1, 100, 200),
        "cost": np.random.exponential(200, 200).round(2),
    })
    st.info("Using demo data")

st.write(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")

with st.form("analysis_form"):
    st.subheader("Configure Analysis")
    numeric_cols = df.select_dtypes("number").columns.tolist()
    cat_cols = df.select_dtypes("object").columns.tolist()

    x_col = st.selectbox("X Column", df.columns.tolist())
    y_col = st.selectbox("Y Column", numeric_cols)
    group_col = st.selectbox("Group By", ["(none)"] + cat_cols)
    chart_type = st.radio("Chart Type", ["bar", "scatter", "line"], horizontal=True)
    submitted = st.form_submit_button("Analyze")

if submitted:
    errors = []
    if y_col not in numeric_cols:
        errors.append(f"{y_col} must be a numeric column")
    if x_col == y_col:
        errors.append("X and Y columns must be different")

    if errors:
        for e in errors: st.error(e)
    else:
        group = None if group_col == "(none)" else group_col
        if chart_type == "bar":
            fig = px.bar(df, x=x_col, y=y_col, color=group, title=f"{y_col} by {x_col}")
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col, color=group, title=f"{y_col} vs {x_col}")
        else:
            fig = px.line(df, x=x_col, y=y_col, color=group, title=f"{y_col} over {x_col}")
        st.plotly_chart(fig, use_container_width=True)
""".strip(),
    pt="Validated Registration Form",
    pd_text="Build a st.form() with name, email, age fields. Validate that name is non-empty, email matches a regex, and age is between 18-120. Show errors or a success message on submit.",
    ps="""
# validated_form.py
import streamlit as st
import re

st.title("Registration Form")

with st.form("register"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", 0, 150, 25)
    submitted = st.form_submit_button("Submit")

if submitted:
    errors = []
    # 1. Validate name is not empty
    # 2. Validate email with regex r'^[\\w.]+@[\\w]+\\.[a-z]{2,}$'
    # 3. Validate age is 18-120
    # 4. Show errors or st.success("Welcome!")
""".strip()
)

# ── Section 21: File Upload & Download ───────────────────────────────────────
s21 = make_section(21, "File Upload & Download",
    "st.file_uploader() accepts CSV, Excel, images, and arbitrary files. st.download_button() provides one-click download of DataFrames, plots, or any binary content.",
    c1t="File Upload & CSV Processing",
    c1="""
# streamlit_file_upload.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO, StringIO

st.title("File Upload & Processing")

# Upload CSV
st.header("CSV Upload & Analysis")
uploaded_csv = st.file_uploader("Upload a CSV file", type=["csv", "xlsx"])

if uploaded_csv is not None:
    # Read file
    if uploaded_csv.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_csv)
    else:
        df = pd.read_csv(uploaded_csv)

    st.success(f"Loaded: {len(df)} rows x {len(df.columns)} columns")

    col1, col2 = st.columns(2)
    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))

    st.subheader("Preview")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Data Types")
    st.dataframe(pd.DataFrame({"dtype": df.dtypes, "non_null": df.count(),
                                "null_count": df.isnull().sum()}))

    st.subheader("Statistics")
    st.dataframe(df.describe(), use_container_width=True)

    # Auto chart for numeric columns
    numeric_cols = df.select_dtypes("number").columns.tolist()
    if numeric_cols:
        col = st.selectbox("Histogram of:", numeric_cols)
        fig = px.histogram(df, x=col, title=f"Distribution of {col}")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Upload a CSV file to get started")

    # Show demo
    with st.expander("Try with demo data"):
        np.random.seed(42)
        demo_df = pd.DataFrame({
            "name": [f"Item_{i}" for i in range(20)],
            "value": np.random.randn(20) * 100,
            "category": np.random.choice(["A","B","C"], 20),
        })
        st.dataframe(demo_df)
""".strip(),
    c2t="Download Buttons & Export",
    c2="""
# streamlit_download.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.title("Data Download Examples")

np.random.seed(42)
df = pd.DataFrame({
    "product": [f"Item_{i}" for i in range(50)],
    "category": np.random.choice(["A","B","C"], 50),
    "sales": np.random.exponential(1000, 50).round(2),
    "units": np.random.randint(10, 500, 50),
    "rating": np.random.uniform(1, 5, 50).round(1),
})
st.dataframe(df.head(10), use_container_width=True)

st.subheader("Download Options")

col1, col2, col3 = st.columns(3)

# 1. Download as CSV
csv_data = df.to_csv(index=False).encode("utf-8")
col1.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="sales_data.csv",
    mime="text/csv",
    use_container_width=True,
)

# 2. Download as Excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
        summary = df.groupby("category")["sales"].sum().reset_index()
        summary.to_excel(writer, index=False, sheet_name="Summary")
    return output.getvalue()

excel_data = to_excel(df)
col2.download_button(
    label="Download Excel",
    data=excel_data,
    file_name="sales_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True,
)

# 3. Download chart as HTML
fig = px.bar(df.groupby("category")["sales"].sum().reset_index(),
             x="category", y="sales", title="Sales by Category")
st.plotly_chart(fig, use_container_width=True)

chart_html = fig.to_html()
col3.download_button(
    label="Download Chart",
    data=chart_html.encode("utf-8"),
    file_name="sales_chart.html",
    mime="text/html",
    use_container_width=True,
)
""".strip(),
    c3t="Image Upload & Processing",
    c3="""
# streamlit_image_upload.py
import streamlit as st
import numpy as np
from io import BytesIO

st.title("Image Upload & Processing")

uploaded_img = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_img is not None:
    # Display original
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_img, caption="Original", use_container_width=True)

    try:
        from PIL import Image, ImageFilter, ImageEnhance
        img = Image.open(uploaded_img)
        st.write(f"Size: {img.size}, Mode: {img.mode}")

        # Processing options
        effect = st.selectbox("Effect", ["None", "Grayscale", "Blur", "Sharpen", "Rotate"])

        if effect == "Grayscale":
            processed = img.convert("L")
        elif effect == "Blur":
            radius = st.slider("Blur Radius", 1, 10, 3)
            processed = img.filter(ImageFilter.GaussianBlur(radius))
        elif effect == "Sharpen":
            processed = img.filter(ImageFilter.SHARPEN)
        elif effect == "Rotate":
            angle = st.slider("Angle", 0, 360, 90)
            processed = img.rotate(angle)
        else:
            processed = img

        with col2:
            st.image(processed, caption=f"Processed ({effect})", use_container_width=True)

        # Download processed image
        buf = BytesIO()
        processed.save(buf, format="PNG")
        st.download_button("Download Processed Image", buf.getvalue(),
                          "processed.png", "image/png")
    except ImportError:
        st.warning("Install Pillow for image processing: pip install Pillow")
else:
    st.info("Upload an image to process it")
    st.write("Supported effects: Grayscale, Blur, Sharpen, Rotate")
""".strip(),
    rw_scenario="Build a data cleaning tool: upload messy CSV, show data quality report (nulls, duplicates, outliers), let user configure cleaning options, and download the clean dataset.",
    rw_code="""
# streamlit_data_cleaner.py
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.title("Data Cleaning Tool")

@st.cache_data
def generate_messy_data():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        "id": range(n),
        "name": [f"Item_{i}" if np.random.random() > 0.03 else None for i in range(n)],
        "price": np.where(np.random.random(n) < 0.05, None,
                          np.where(np.random.random(n) < 0.02, -99.99,
                                   np.random.exponential(50, n).round(2))),
        "category": np.random.choice(["A","B","C",None], n, p=[0.35,0.35,0.25,0.05]),
        "quantity": np.random.randint(-5, 100, n),  # some negatives
    })
    # Add duplicates
    df = pd.concat([df, df.sample(50, random_state=42)]).reset_index(drop=True)
    return df

uploaded = st.file_uploader("Upload CSV", type="csv")
df = pd.read_csv(uploaded) if uploaded else generate_messy_data()

st.subheader("Data Quality Report")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rows", len(df))
col2.metric("Null Values", df.isnull().sum().sum())
col3.metric("Duplicates", df.duplicated().sum())

st.dataframe(pd.DataFrame({
    "nulls": df.isnull().sum(),
    "null_pct": (df.isnull().mean()*100).round(1),
    "dtype": df.dtypes,
}), use_container_width=True)

st.subheader("Cleaning Options")
col_a, col_b = st.columns(2)
drop_nulls = col_a.checkbox("Drop rows with nulls", value=True)
drop_dupes = col_b.checkbox("Remove duplicates", value=True)

if st.button("Clean Data"):
    clean_df = df.copy()
    n_before = len(clean_df)
    if drop_dupes: clean_df = clean_df.drop_duplicates()
    if drop_nulls: clean_df = clean_df.dropna()
    # Remove negative quantities
    if "quantity" in clean_df.columns:
        clean_df = clean_df[clean_df["quantity"] >= 0]
    n_after = len(clean_df)
    st.success(f"Cleaned: {n_before} -> {n_after} rows ({n_before-n_after} removed)")
    st.dataframe(clean_df.head(10), use_container_width=True)
    csv = clean_df.to_csv(index=False).encode()
    st.download_button("Download Clean Data", csv, "clean_data.csv", "text/csv")
""".strip(),
    pt="Upload, Process & Download",
    pd_text="Build a Streamlit app that accepts a CSV upload, shows summary stats, lets user select a numeric column to filter by a minimum threshold, and provides a download button for filtered results.",
    ps="""
# upload_filter_download.py
import streamlit as st
import pandas as pd
import numpy as np

st.title("Upload, Filter & Download")

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    # 1. Show df.shape and df.describe()
    # 2. Select numeric column with st.selectbox
    # 3. Add st.slider for min threshold
    # 4. Filter df where col >= threshold
    # 5. st.dataframe for filtered result
    # 6. st.download_button for filtered CSV
""".strip()
)

# ── Section 22: Multi-page Apps ───────────────────────────────────────────────
s22 = make_section(22, "Multi-page Apps",
    "Streamlit natively supports multi-page apps using the pages/ folder structure. st.navigation() (new API) or the legacy pages/ directory enables organized, scalable applications.",
    c1t="pages/ Directory Structure",
    c1="""
# Multi-page app structure:
# my_app/
#   app.py          (main entry, shown as Home)
#   pages/
#     1_Dashboard.py
#     2_Analytics.py
#     3_Settings.py

# app.py (main page / Home)
import streamlit as st

st.set_page_config(
    page_title="My Data App",
    page_icon="DATA",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Home - Data Analytics Platform")
st.write("Welcome to the multi-page data app!")

# Shared sidebar content (appears on all pages)
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
             width=150)
    st.write("Navigation: Use the links above")

st.write("---")
col1, col2, col3 = st.columns(3)
col1.info("Dashboard\\nView key metrics and charts")
col2.info("Analytics\\nDeep-dive analysis tools")
col3.info("Settings\\nConfigure your preferences")

# Shared state across pages
if "shared_data" not in st.session_state:
    st.session_state.shared_data = {"user": "Guest", "theme": "light"}

st.write(f"Logged in as: **{st.session_state.shared_data['user']}**")
new_name = st.text_input("Change username:")
if new_name:
    st.session_state.shared_data["user"] = new_name
    st.success(f"Username updated to: {new_name}")
""".strip(),
    c2t="Programmatic Navigation with st.navigation()",
    c2="""
# Modern multi-page app using st.navigation() (Streamlit >= 1.36)
# app_modern.py

import streamlit as st
import pandas as pd
import numpy as np

# Define pages programmatically
def home_page():
    st.title("Home")
    st.write("Welcome to the modern multi-page app!")
    st.metric("Total Users", "1,234", "+15%")
    st.metric("Daily Active", "456", "+8%")

def dashboard_page():
    st.title("Dashboard")
    np.random.seed(42)
    data = pd.DataFrame(np.random.randn(50, 3), columns=["A", "B", "C"])
    st.line_chart(data)
    st.dataframe(data.describe())

def settings_page():
    st.title("Settings")
    if "settings" not in st.session_state:
        st.session_state.settings = {"theme": "light", "language": "en"}

    theme = st.selectbox("Theme", ["light", "dark"])
    language = st.selectbox("Language", ["en", "fr", "de", "es"])

    if st.button("Save Settings"):
        st.session_state.settings = {"theme": theme, "language": language}
        st.success("Settings saved!")

# Usage (Streamlit >= 1.36):
# pg = st.navigation({
#     "App": [
#         st.Page(home_page, title="Home", icon="HOME"),
#         st.Page(dashboard_page, title="Dashboard", icon="CHART"),
#         st.Page(settings_page, title="Settings", icon="GEAR"),
#     ]
# })
# pg.run()

# For compatibility, show the structure:
page = st.selectbox("Simulate Navigation", ["Home", "Dashboard", "Settings"])
if page == "Home": home_page()
elif page == "Dashboard": dashboard_page()
else: settings_page()
""".strip(),
    c3t="Shared State & Authentication",
    c3="""
# pages/shared_state_auth.py
import streamlit as st
import pandas as pd
import numpy as np

# Simulated authentication system
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "viewer"},
}

def login_page():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
    if submitted:
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials")

def protected_page():
    st.title(f"Protected Dashboard")
    st.write(f"Role: **{st.session_state.get('role', 'unknown')}**")

    if st.session_state.get("role") == "admin":
        st.success("Admin access: full data visible")
        np.random.seed(42)
        df = pd.DataFrame({
            "user_id": range(10),
            "revenue": np.random.exponential(1000, 10).round(2),
            "secret_field": np.random.randint(0, 100, 10),  # admin-only
        })
        st.dataframe(df)
    else:
        st.info("Viewer access: limited data")
        df = pd.DataFrame({"product": ["A","B","C"], "revenue": [1000, 2000, 1500]})
        st.dataframe(df)

    if st.sidebar.button("Logout"):
        for key in ["logged_in", "username", "role"]:
            st.session_state.pop(key, None)
        st.rerun()

# Main logic
if not st.session_state.get("logged_in", False):
    login_page()
else:
    protected_page()
""".strip(),
    rw_scenario="Build a 3-page analytics platform: Home (overview KPIs), Analysis (interactive charts with filters), and Export (download reports). Share filtered data between pages via session state.",
    rw_code="""
# streamlit_multipage_rw.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Analytics Platform", layout="wide")

# Initialize shared state
if "df" not in st.session_state:
    np.random.seed(42)
    n = 500
    st.session_state.df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=n, freq="D"),
        "product": np.random.choice(["A","B","C","D"], n),
        "region": np.random.choice(["North","South","East","West"], n),
        "revenue": np.random.exponential(500, n).round(2),
        "units": np.random.randint(1, 100, n),
    })
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = st.session_state.df.copy()

# Sidebar navigation
page = st.sidebar.selectbox("Page", ["Home", "Analysis", "Export"])
df = st.session_state.df

if page == "Home":
    st.title("Overview Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
    c2.metric("Total Units", f"{df['units'].sum():,}")
    c3.metric("Products", df["product"].nunique())
    c4.metric("Days", df["date"].nunique())
    st.plotly_chart(px.line(df.groupby("date")["revenue"].sum().reset_index(),
                            x="date", y="revenue", title="Daily Revenue"), use_container_width=True)

elif page == "Analysis":
    st.title("Interactive Analysis")
    with st.sidebar:
        products = st.multiselect("Products", df["product"].unique(), default=df["product"].unique())
        regions = st.multiselect("Regions", df["region"].unique(), default=df["region"].unique())
    filtered = df[df["product"].isin(products) & df["region"].isin(regions)]
    st.session_state.filtered_df = filtered
    st.write(f"Filtered: {len(filtered)} rows")
    chart = st.selectbox("Chart", ["Revenue by Product", "Revenue by Region", "Scatter"])
    if chart == "Revenue by Product":
        st.plotly_chart(px.bar(filtered.groupby("product")["revenue"].sum().reset_index(), x="product", y="revenue"), use_container_width=True)
    elif chart == "Revenue by Region":
        st.plotly_chart(px.pie(filtered.groupby("region")["revenue"].sum().reset_index(), names="region", values="revenue"), use_container_width=True)
    else:
        st.plotly_chart(px.scatter(filtered, x="units", y="revenue", color="product"), use_container_width=True)

elif page == "Export":
    st.title("Export Reports")
    filtered = st.session_state.filtered_df
    st.write(f"Exporting {len(filtered)} filtered rows")
    st.download_button("Download CSV", filtered.to_csv(index=False).encode(), "report.csv", "text/csv")
""".strip(),
    pt="Multi-Page Navigation",
    pd_text="Create a Streamlit app that simulates 3 pages using a selectbox in the sidebar. Each page shows different content and shares data via session_state.",
    ps="""
# multipage_sim.py
import streamlit as st
import numpy as np

# Initialize shared state
if "shared_value" not in st.session_state:
    st.session_state.shared_value = 0

page = st.sidebar.selectbox("Navigate to", ["Page 1", "Page 2", "Page 3"])

if page == "Page 1":
    # 1. Show title "Page 1: Input"
    # 2. st.number_input -> update st.session_state.shared_value
    pass
elif page == "Page 2":
    # 3. Show title "Page 2: View"
    # 4. Show st.session_state.shared_value as st.metric
    pass
else:
    # 5. Show title "Page 3: Analysis"
    # 6. Show chart using st.session_state.shared_value
    pass
""".strip()
)

# ── Section 23: Custom CSS & Theming ─────────────────────────────────────────
s23 = make_section(23, "Custom CSS & Theming",
    "Streamlit supports custom CSS via st.markdown() with unsafe_allow_html=True, config.toml themes, and custom components for advanced UI needs.",
    c1t="Custom CSS with st.markdown()",
    c1="""
# streamlit_custom_css.py
import streamlit as st
import pandas as pd
import numpy as np

st.title("Custom CSS & Styling")

# Inject custom CSS
st.markdown('''
<style>
    /* Custom card styling */
    .custom-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.2);
    }
    .card-title {
        color: #00d4ff;
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .card-value {
        color: #ffffff;
        font-size: 2em;
        font-weight: bold;
    }
    .card-delta {
        color: #4caf50;
        font-size: 0.9em;
    }
    /* Custom button */
    .stButton > button {
        background: linear-gradient(90deg, #0077ff, #00d4ff);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 8px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 119, 255, 0.4);
    }
    /* Custom metric */
    .highlight-box {
        background: #0d1117;
        border-left: 4px solid #00d4ff;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
</style>
''', unsafe_allow_html=True)

# Custom cards
col1, col2, col3 = st.columns(3)
metrics = [
    ("Revenue", "$124,500", "+12.3%"),
    ("Users", "8,421", "+5.7%"),
    ("Conversion", "3.8%", "+0.4%"),
]
for col, (title, value, delta) in zip([col1, col2, col3], metrics):
    col.markdown(f'''
    <div class="custom-card">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
        <div class="card-delta">↑ {delta}</div>
    </div>
    ''', unsafe_allow_html=True)

# Highlighted boxes
for item in ["Tip: Use st.markdown() with unsafe_allow_html=True for custom HTML",
             "Tip: Define CSS in a single st.markdown() at the top of your app",
             "Tip: Use class names to target specific Streamlit elements"]:
    st.markdown(f'<div class="highlight-box">{item}</div>', unsafe_allow_html=True)
""".strip(),
    c2t="Theming via config.toml",
    c2="""
# .streamlit/config.toml - controls app-wide theme
config_toml = '''
[theme]
primaryColor = "#00d4ff"
backgroundColor = "#0d1117"
secondaryBackgroundColor = "#161b22"
textColor = "#e6edf3"
font = "sans serif"

[server]
port = 8501
headless = true
maxUploadSize = 200

[browser]
gatherUsageStats = false

[runner]
fastReruns = true
'''

# streamlit_theming_demo.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.title("Theming Demo")
st.caption("Themes defined in .streamlit/config.toml")

# Display config structure
st.code(config_toml, language="toml")

# Programmatic theming tips
st.subheader("Dynamic Theming Tricks")

# Custom color palette for charts
COLORS = {
    "dark": {"bg": "#0d1117", "text": "#e6edf3", "accent": "#00d4ff"},
    "light": {"bg": "#ffffff", "text": "#0d1117", "accent": "#0077ff"},
}

theme = st.radio("Preview Theme", ["dark", "light"], horizontal=True)
colors = COLORS[theme]

# Apply to Plotly chart
np.random.seed(42)
df = pd.DataFrame({"x": range(20), "y": np.cumsum(np.random.randn(20))})
fig = px.line(df, x="x", y="y", title="Themed Chart")
fig.update_layout(
    paper_bgcolor=colors["bg"],
    plot_bgcolor=colors["bg"],
    font_color=colors["text"],
)
fig.update_traces(line_color=colors["accent"])
st.plotly_chart(fig, use_container_width=True)
""".strip(),
    c3t="Styled Components & HTML Templates",
    c3="""
# streamlit_styled_components.py
import streamlit as st
import pandas as pd
import numpy as np

st.title("Styled HTML Components")

# Progress bar with custom styling
def styled_progress(label, value, max_val=100, color="#00d4ff"):
    pct = int(value / max_val * 100)
    st.markdown(f'''
    <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #e6edf3;">{label}</span>
            <span style="color: {color}; font-weight: bold;">{value}/{max_val} ({pct}%)</span>
        </div>
        <div style="background: #161b22; border-radius: 8px; height: 12px; overflow: hidden;">
            <div style="width: {pct}%; height: 100%; background: linear-gradient(90deg, {color}, {color}88);
                        border-radius: 8px; transition: width 0.5s ease;"></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

st.subheader("Custom Progress Bars")
styled_progress("Model Accuracy", 92, 100, "#4caf50")
styled_progress("Training Progress", 67, 100, "#00d4ff")
styled_progress("Data Quality", 78, 100, "#ff9800")

# Status badges
def badge(text, color="blue"):
    colors = {"blue": "#0077ff", "green": "#4caf50", "red": "#f44336",
              "yellow": "#ff9800", "purple": "#9c27b0"}
    c = colors.get(color, colors["blue"])
    return f'<span style="background:{c}22;color:{c};border:1px solid {c};border-radius:12px;padding:2px 10px;font-size:0.82em;font-weight:600;">{text}</span>'

st.subheader("Status Badges")
statuses = [("Production", "green"), ("Beta", "blue"), ("Deprecated", "red"),
            ("Warning", "yellow"), ("Experimental", "purple")]
badges_html = " ".join(badge(name, color) for name, color in statuses)
st.markdown(badges_html, unsafe_allow_html=True)

# Notification cards
def notify(message, type_="info"):
    icons = {"info": "INFO", "success": "DONE", "warning": "WARN", "error": "ERR"}
    bg_colors = {"info": "#0077ff", "success": "#4caf50", "warning": "#ff9800", "error": "#f44336"}
    st.markdown(f'''
    <div style="display:flex;align-items:center;padding:10px 15px;
                border-radius:8px;background:{bg_colors[type_]}22;
                border-left:4px solid {bg_colors[type_]};margin:6px 0;">
        <span style="font-weight:bold;color:{bg_colors[type_]};margin-right:8px;">{icons[type_]}</span>
        <span style="color:#e6edf3;">{message}</span>
    </div>''', unsafe_allow_html=True)

st.subheader("Custom Notifications")
notify("Model training completed successfully!", "success")
notify("Dataset has 5% missing values. Consider imputation.", "warning")
notify("API rate limit approaching: 850/1000 requests used.", "info")
notify("Database connection failed. Using cached data.", "error")
""".strip(),
    rw_scenario="Style a ML dashboard with custom CSS: gradient sidebar, animated metric cards, colored status badges for model health, and a custom-styled data table with row highlighting.",
    rw_code="""
# streamlit_styled_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide", page_title="ML Dashboard")

# Custom CSS
st.markdown('''
<style>
.metric-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #0f3460;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
}
.metric-label { color: #8b949e; font-size: 0.85em; }
.metric-value { color: #e6edf3; font-size: 1.8em; font-weight: bold; }
.metric-delta { color: #4caf50; font-size: 0.9em; }
.status-badge {
    display: inline-block;
    padding: 2px 12px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: 600;
}
</style>
''', unsafe_allow_html=True)

st.title("ML Model Health Dashboard")

# Model status
np.random.seed(42)
models = [
    {"name": "Fraud Detector", "accuracy": 0.947, "status": "Production", "drift": 0.03},
    {"name": "Churn Predictor", "accuracy": 0.823, "status": "Warning", "drift": 0.18},
    {"name": "Recommender", "accuracy": 0.891, "status": "Production", "drift": 0.05},
    {"name": "Price Model", "accuracy": 0.712, "status": "Degraded", "drift": 0.31},
]

st.subheader("Model Status")
cols = st.columns(len(models))
status_colors = {"Production": "#4caf50", "Warning": "#ff9800", "Degraded": "#f44336"}

for col, model in zip(cols, models):
    color = status_colors.get(model["status"], "#0077ff")
    col.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">{model["name"]}</div>
        <div class="metric-value">{model["accuracy"]:.1%}</div>
        <div><span class="status-badge" style="background:{color}22;color:{color};border:1px solid {color};">
            {model["status"]}</span></div>
        <div class="metric-delta">Drift: {model["drift"]:.0%}</div>
    </div>''', unsafe_allow_html=True)
""".strip(),
    pt="Custom Styled Component",
    pd_text="Build a Streamlit app with a custom CSS-styled progress bar for 3 metrics and colored badges for status labels (Active=green, Inactive=red, Pending=yellow).",
    ps="""
# styled_component.py
import streamlit as st

st.title("Custom Styled Components")

# 1. Add CSS via st.markdown() with unsafe_allow_html=True
# 2. Create a styled_progress(label, value, color) function using HTML
# 3. Create a badge(text, color) function that returns an HTML span
# 4. Render 3 progress bars with different colors and 3 status badges

metrics = [("Accuracy", 92), ("F1 Score", 87), ("AUC", 95)]
statuses = [("Active", "green"), ("Inactive", "red"), ("Pending", "yellow")]
""".strip()
)

# ── Section 24: Deployment ────────────────────────────────────────────────────
s24 = make_section(24, "Deployment: Cloud, Docker & CI/CD",
    "Deploy Streamlit apps to Streamlit Cloud (free), Docker containers, AWS/GCP, or Heroku. Production deployments need proper secret management, health checks, and logging.",
    c1t="Streamlit Cloud Deployment",
    c1="""
# Complete deployment package for Streamlit Cloud
# File structure:
# my_app/
#   app.py
#   requirements.txt
#   .streamlit/
#     config.toml
#     secrets.toml  (git-ignored)

# requirements.txt
requirements = '''
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
scikit-learn>=1.4.0
numpy>=1.26.0
'''

# .streamlit/config.toml
config = '''
[server]
maxUploadSize = 200
headless = true
port = 8501

[theme]
primaryColor = "#0077ff"
backgroundColor = "#0d1117"
secondaryBackgroundColor = "#161b22"
textColor = "#e6edf3"
'''

# .streamlit/secrets.toml (local dev only, add to .gitignore)
secrets_example = '''
# .streamlit/secrets.toml (DO NOT COMMIT)
DATABASE_URL = "postgresql://user:pass@host:5432/db"
API_KEY = "your-api-key-here"
'''

# app.py - access secrets
import streamlit as st

st.title("Production-Ready Streamlit App")

# Access secrets (set in Streamlit Cloud dashboard or secrets.toml)
# api_key = st.secrets["API_KEY"]
# db_url = st.secrets["DATABASE_URL"]

# Show deployment info
st.info("Deployment: Streamlit Cloud")
st.code(requirements, language="text")
st.write("Deploy steps:")
steps = [
    "1. Push code to GitHub",
    "2. Go to share.streamlit.io",
    "3. Connect GitHub repository",
    "4. Set app.py as main file",
    "5. Add secrets in the cloud dashboard",
    "6. Click Deploy!",
]
for step in steps:
    st.write(step)
""".strip(),
    c2t="Docker Deployment",
    c2="""
# Docker deployment for Streamlit

# Dockerfile
dockerfile = '''
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run app
ENTRYPOINT ["streamlit", "run", "app.py", \\
            "--server.port=8501", \\
            "--server.address=0.0.0.0", \\
            "--server.headless=true"]
'''

# docker-compose.yml
docker_compose = '''
version: '3.8'
services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - API_KEY=${API_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
'''

import streamlit as st

st.title("Docker Deployment Guide")
st.subheader("Dockerfile")
st.code(dockerfile, language="docker")
st.subheader("docker-compose.yml")
st.code(docker_compose, language="yaml")

st.write("Build and run:")
st.code('''
# Build image
docker build -t my-streamlit-app .

# Run container
docker run -p 8501:8501 my-streamlit-app

# With docker-compose
docker-compose up -d
docker-compose logs -f streamlit
''', language="bash")
""".strip(),
    c3t="Production Best Practices",
    c3="""
import streamlit as st
import pandas as pd
import numpy as np
import logging
import time
from functools import wraps

st.title("Production Best Practices")

# 1. Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Error handling
def safe_execute(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"Error: {e}")
            logger.exception(f"Error in {func.__name__}")
            return None
    return wrapper

@safe_execute
def load_data_safely(source="demo"):
    if source == "demo":
        np.random.seed(42)
        return pd.DataFrame({
            "product": np.random.choice(["A","B","C"], 100),
            "revenue": np.random.exponential(500, 100).round(2),
        })
    raise ValueError(f"Unknown source: {source}")

# 3. Performance monitoring
def timed(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            elapsed = (time.time() - t0) * 1000
            logger.info(f"{name}: {elapsed:.0f}ms")
            return result
        return wrapper
    return decorator

@timed("data_load")
@st.cache_data(ttl=300)
def get_dashboard_data():
    return load_data_safely("demo")

df = get_dashboard_data()
if df is not None:
    st.success(f"Data loaded: {len(df)} rows")
    st.dataframe(df.head())

# 4. Health check endpoint pattern
st.subheader("Health Check Pattern")
st.code('''
# Add to app.py for health monitoring
@st.cache_data(ttl=60)
def health_status():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "db_connected": check_db_connection(),
        "cache_size": len(st.session_state),
    }

# Show in sidebar
with st.sidebar:
    if st.button("Health Check"):
        st.json(health_status())
''')

# 5. Production checklist
st.subheader("Deployment Checklist")
checklist = [
    ("Add .streamlit/secrets.toml to .gitignore", True),
    ("Set all secrets via cloud dashboard or env vars", True),
    ("Pin dependency versions in requirements.txt", True),
    ("Add @st.cache_data to all data-loading functions", True),
    ("Test with st run app.py --server.headless=true", True),
    ("Set up health check endpoint", True),
    ("Configure error monitoring (Sentry, DataDog)", False),
    ("Set up CI/CD pipeline for auto-deployment", False),
]
for item, done in checklist:
    icon = "CHECK" if done else "PENDING"
    st.write(f"  [{icon}] {item}")
""".strip(),
    rw_scenario="Deploy a production ML dashboard: set up Docker container, configure secrets, add health check endpoint, implement error boundaries, and create a GitHub Actions CI/CD pipeline for auto-deploy.",
    rw_code="""
# streamlit_production_app.py
import streamlit as st
import pandas as pd
import numpy as np
import logging
import time
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Production ML Dashboard",
    page_icon="CHART",
    layout="wide",
)

# Global error handler
def handle_error(e, context=""):
    logger.error(f"Error in {context}: {e}")
    st.error(f"An error occurred: {e}")
    if st.button("Show Error Details"):
        st.exception(e)

# Health check
@st.cache_data(ttl=30)
def get_health():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "session_vars": len(st.session_state),
    }

# Model loading
@st.cache_resource
def load_model():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris
    logger.info("Loading ML model")
    X, y = load_iris(return_X_y=True)
    return RandomForestClassifier(n_estimators=50, random_state=42).fit(X, y)

# Data loading with caching
@st.cache_data(ttl=300)
def load_dashboard_data():
    logger.info("Loading dashboard data")
    np.random.seed(42)
    n = 1000
    return pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=n, freq="D")[:n],
        "product": np.random.choice(["A","B","C"], n),
        "revenue": np.random.exponential(500, n).round(2),
        "units": np.random.randint(1, 100, n),
    })

# Main app
try:
    model = load_model()
    df = load_dashboard_data()

    st.title("Production ML Dashboard")

    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
    c2.metric("Total Units", f"{df['units'].sum():,}")
    c3.metric("Model Status", "Healthy")

    # Chart
    monthly = df.groupby(df["date"].dt.month)["revenue"].sum()
    st.bar_chart(monthly)

    # Health sidebar
    with st.sidebar:
        st.title("System Health")
        health = get_health()
        st.json(health)
        logger.info("Dashboard rendered successfully")

except Exception as e:
    handle_error(e, "main app")
""".strip(),
    pt="Deployable Streamlit App",
    pd_text="Write a production-ready Streamlit app with: @st.cache_data for data loading, @st.cache_resource for a model, a try/except error handler, and a sidebar health check button.",
    ps="""
# production_app.py
import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Production App")

# 1. @st.cache_data(ttl=300) - load_data() returns a DataFrame
# 2. @st.cache_resource - load_model() returns a trained sklearn model
# 3. try/except wrapper around main app logic
# 4. Sidebar with "Health Check" button that shows:
#    {"status": "healthy", "data_rows": len(df), "model": type(model).__name__}
""".strip()
)

# ── Assemble ──────────────────────────────────────────────────────────────────
all_sections = s17 + s18 + s19 + s20 + s21 + s22 + s23 + s24
result = insert_before_make_html(FILE, all_sections)
print("SUCCESS" if result else "FAILED")
