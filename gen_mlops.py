#!/usr/bin/env python3
"""Generate MLOps & Model Deployment study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE   = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\14_mlops")
BASE.mkdir(parents=True, exist_ok=True)
ACCENT = "#f78166"
EMOJI  = "🚀"
TITLE  = "MLOps & Model Deployment"

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
function act(a,e){{e.preventDefault();document.querySelectorAll('#nl a').forEach(x=>x.classList.remove('active'));a.classList.add('active');document.querySelector(a.getAttribute('href')).scrollIntoView({{behavior:'smooth'}});}}
function cp(id){{navigator.clipboard.writeText(document.getElementById(id).innerText);}}
function filt(v){{var lv=v.toLowerCase();document.querySelectorAll('#nl li').forEach(li=>{{li.style.display=li.querySelector('a').textContent.toLowerCase().includes(lv)?'':'none';}});}}
</script></body></html>"""

def make_nb(sections):
    cells = []
    def md(src): cells.append({"cell_type":"markdown","metadata":{},"source":src})
    def code(src): cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":src})
    md(f"# {EMOJI} {TITLE}\n\nA hands-on study guide covering {len(sections)} core topics.")
    for s in sections:
        md(f"## {s['title']}\n\n{s.get('desc','')}")
        for ex in s.get("examples", []):
            md(f"**{ex.get('label','Example')}**")
            code(ex["code"])
        if s.get("rw_scenario"):
            md(f"### Real-World Scenario\n\n{s['rw_scenario']}")
            code(s["rw_code"])
        if s.get("practice"):
            p = s["practice"]
            md(f"### Practice: {p['title']}\n\n{p['desc']}")
            code(p["starter"])
    return {"nbformat":4,"nbformat_minor":5,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.11.0"}},"cells":cells}

SECTIONS = [
    {
        "title": "1. Saving & Loading Models",
        "desc": "Persist trained models to disk for reuse, versioning, and deployment. Covers pickle, joblib, and framework-native formats.",
        "examples": [
            {
                "label": "Save/load sklearn model with joblib",
                "code": (
                    "import joblib\n"
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "from sklearn.datasets import load_iris\n\n"
                    "X, y = load_iris(return_X_y=True)\n"
                    "model = RandomForestClassifier(n_estimators=50, random_state=42)\n"
                    "model.fit(X, y)\n\n"
                    "# Save\n"
                    "joblib.dump(model, 'iris_rf.joblib')\n"
                    "print('Model saved.')\n\n"
                    "# Load and predict\n"
                    "loaded = joblib.load('iris_rf.joblib')\n"
                    "preds = loaded.predict(X[:5])\n"
                    "print('Predictions:', preds)\n"
                    "print('Expected:   ', y[:5])"
                )
            },
            {
                "label": "Save full sklearn pipeline",
                "code": (
                    "import joblib\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.datasets import load_breast_cancer\n\n"
                    "X, y = load_breast_cancer(return_X_y=True)\n\n"
                    "pipe = Pipeline([\n"
                    "    ('scaler', StandardScaler()),\n"
                    "    ('clf',   LogisticRegression(max_iter=1000))\n"
                    "])\n"
                    "pipe.fit(X, y)\n\n"
                    "# Save the entire pipeline — preprocessor + model\n"
                    "joblib.dump(pipe, 'cancer_pipeline.joblib')\n\n"
                    "loaded_pipe = joblib.load('cancer_pipeline.joblib')\n"
                    "print('Pipeline accuracy:', loaded_pipe.score(X, y))\n"
                    "print('Steps:', [name for name, _ in loaded_pipe.steps])"
                )
            },
            {
                "label": "Save/load PyTorch model",
                "code": (
                    "try:\n"
                    "    import torch\n"
                    "    import torch.nn as nn\n\n"
                    "    class SimpleNet(nn.Module):\n"
                    "        def __init__(self):\n"
                    "            super().__init__()\n"
                    "            self.fc = nn.Linear(4, 3)\n"
                    "        def forward(self, x):\n"
                    "            return self.fc(x)\n\n"
                    "    model = SimpleNet()\n\n"
                    "    # Best practice: save state_dict only\n"
                    "    torch.save(model.state_dict(), 'simple_net.pt')\n\n"
                    "    # Load\n"
                    "    loaded = SimpleNet()\n"
                    "    loaded.load_state_dict(torch.load('simple_net.pt', weights_only=True))\n"
                    "    loaded.eval()\n\n"
                    "    x = torch.randn(2, 4)\n"
                    "    print('Output:', loaded(x))\n"
                    "except ImportError:\n"
                    "    print('pip install torch')"
                )
            },
            {
                "label": "Model versioning with metadata",
                "code": (
                    "import joblib, json, hashlib, time\n"
                    "from sklearn.ensemble import GradientBoostingClassifier\n"
                    "from sklearn.datasets import load_iris\n\n"
                    "X, y = load_iris(return_X_y=True)\n"
                    "model = GradientBoostingClassifier(n_estimators=50, random_state=42)\n"
                    "model.fit(X, y)\n\n"
                    "# Save model\n"
                    "model_path = 'model_v1.joblib'\n"
                    "joblib.dump(model, model_path)\n\n"
                    "# Save metadata alongside\n"
                    "with open(model_path, 'rb') as f:\n"
                    "    checksum = hashlib.md5(f.read()).hexdigest()\n\n"
                    "metadata = {\n"
                    "    'model_class': type(model).__name__,\n"
                    "    'params': model.get_params(),\n"
                    "    'train_accuracy': model.score(X, y),\n"
                    "    'trained_at': time.strftime('%Y-%m-%dT%H:%M:%S'),\n"
                    "    'checksum': checksum,\n"
                    "}\n"
                    "with open('model_v1_meta.json', 'w') as f:\n"
                    "    json.dump(metadata, f, indent=2)\n\n"
                    "print(json.dumps(metadata, indent=2))"
                )
            },
        ],
        "rw_scenario": "A data science team trains a fraud detection model weekly. They need to save each version with metadata so they can roll back if a new model underperforms in production.",
        "rw_code": (
            "import joblib, json, time, pathlib\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.datasets import make_classification\n\n"
            "MODEL_DIR = pathlib.Path('model_registry')\n"
            "MODEL_DIR.mkdir(exist_ok=True)\n\n"
            "def save_model_version(model, version: str, metrics: dict):\n"
            "    model_path = MODEL_DIR / f'model_{version}.joblib'\n"
            "    meta_path  = MODEL_DIR / f'model_{version}_meta.json'\n"
            "    joblib.dump(model, model_path)\n"
            "    meta = {'version': version, 'trained_at': time.strftime('%Y-%m-%dT%H:%M:%S'),\n"
            "            'model_class': type(model).__name__, **metrics}\n"
            "    meta_path.write_text(json.dumps(meta, indent=2))\n"
            "    print(f'Saved {model_path}')\n"
            "    return meta\n\n"
            "X, y = make_classification(n_samples=500, random_state=42)\n"
            "model = RandomForestClassifier(n_estimators=100, random_state=42)\n"
            "model.fit(X, y)\n"
            "meta = save_model_version(model, 'v1.0', {'train_acc': model.score(X, y)})\n"
            "print(json.dumps(meta, indent=2))"
        ),
        "practice": {
            "title": "Model Registry",
            "desc": "Create a ModelRegistry class that tracks saved model versions, can list all versions, load a specific version, and return the best-performing one by accuracy.",
            "starter": (
                "import joblib, json, pathlib\n\n"
                "class ModelRegistry:\n"
                "    def __init__(self, registry_dir='registry'):\n"
                "        self.dir = pathlib.Path(registry_dir)\n"
                "        self.dir.mkdir(exist_ok=True)\n\n"
                "    def save(self, model, version: str, accuracy: float):\n"
                "        # TODO: save model and metadata json\n"
                "        pass\n\n"
                "    def list_versions(self) -> list:\n"
                "        # TODO: return list of dicts with version + accuracy\n"
                "        pass\n\n"
                "    def load(self, version: str):\n"
                "        # TODO: load and return model by version string\n"
                "        pass\n\n"
                "    def best(self):\n"
                "        # TODO: return model with highest accuracy\n"
                "        pass\n\n"
                "# Test it\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.datasets import load_iris\n"
                "X, y = load_iris(return_X_y=True)\n"
                "reg = ModelRegistry()\n"
                "m = LogisticRegression(max_iter=200).fit(X, y)\n"
                "reg.save(m, 'v1', m.score(X, y))\n"
                "print(reg.list_versions())"
            )
        }
    },
    {
        "title": "2. FastAPI Model Serving",
        "desc": "Wrap ML models in REST APIs using FastAPI. Serve predictions, handle requests, add input validation with Pydantic, and test endpoints.",
        "examples": [
            {
                "label": "Minimal FastAPI prediction endpoint",
                "code": (
                    "# Save this as app.py and run: uvicorn app:app --reload\n"
                    "# pip install fastapi uvicorn scikit-learn joblib\n\n"
                    "APP_CODE = '''\n"
                    "from fastapi import FastAPI\n"
                    "from pydantic import BaseModel\n"
                    "import joblib, numpy as np\n\n"
                    "app = FastAPI(title='Iris Classifier')\n"
                    "model = joblib.load('iris_rf.joblib')  # load saved model\n\n"
                    "class IrisFeatures(BaseModel):\n"
                    "    sepal_length: float\n"
                    "    sepal_width:  float\n"
                    "    petal_length: float\n"
                    "    petal_width:  float\n\n"
                    "@app.post('/predict')\n"
                    "def predict(features: IrisFeatures):\n"
                    "    X = np.array([[features.sepal_length, features.sepal_width,\n"
                    "                   features.petal_length, features.petal_width]])\n"
                    "    pred = model.predict(X)[0]\n"
                    "    proba = model.predict_proba(X).max()\n"
                    "    return {'prediction': int(pred), 'confidence': float(proba)}\n"
                    "'''\n"
                    "print(APP_CODE)"
                )
            },
            {
                "label": "Batch prediction endpoint",
                "code": (
                    "BATCH_API = '''\n"
                    "from fastapi import FastAPI\n"
                    "from pydantic import BaseModel\n"
                    "from typing import List\n"
                    "import numpy as np, joblib\n\n"
                    "app = FastAPI()\n"
                    "model = joblib.load('iris_rf.joblib')\n\n"
                    "class SingleSample(BaseModel):\n"
                    "    features: List[float]\n\n"
                    "class BatchRequest(BaseModel):\n"
                    "    samples: List[SingleSample]\n\n"
                    "@app.post('/predict/batch')\n"
                    "def batch_predict(batch: BatchRequest):\n"
                    "    X = np.array([s.features for s in batch.samples])\n"
                    "    preds = model.predict(X).tolist()\n"
                    "    probas = model.predict_proba(X).max(axis=1).tolist()\n"
                    "    return [\n"
                    "        {'prediction': p, 'confidence': round(c, 4)}\n"
                    "        for p, c in zip(preds, probas)\n"
                    "    ]\n"
                    "'''\n"
                    "print(BATCH_API)"
                )
            },
            {
                "label": "Testing API with requests",
                "code": (
                    "# Run your FastAPI server first, then test it:\n"
                    "try:\n"
                    "    import requests\n\n"
                    "    BASE_URL = 'http://localhost:8000'\n\n"
                    "    # Single prediction\n"
                    "    payload = {\n"
                    "        'sepal_length': 5.1, 'sepal_width': 3.5,\n"
                    "        'petal_length': 1.4, 'petal_width': 0.2\n"
                    "    }\n"
                    "    response = requests.post(f'{BASE_URL}/predict', json=payload, timeout=5)\n"
                    "    print('Status:', response.status_code)\n"
                    "    print('Response:', response.json())\n\n"
                    "    # Health check\n"
                    "    health = requests.get(f'{BASE_URL}/health', timeout=5)\n"
                    "    print('Health:', health.json())\n"
                    "except Exception as e:\n"
                    "    print(f'Server not running: {e}')\n"
                    "    print('Start with: uvicorn app:app --reload')"
                )
            },
            {
                "label": "FastAPI with model hot-reload and health check",
                "code": (
                    "ADVANCED_API = '''\n"
                    "from fastapi import FastAPI, HTTPException\n"
                    "from pydantic import BaseModel\n"
                    "import joblib, numpy as np, time, pathlib\n\n"
                    "app = FastAPI()\n"
                    "MODEL_PATH = 'iris_rf.joblib'\n"
                    "state = {'model': None, 'loaded_at': None}\n\n"
                    "def load_model():\n"
                    "    state['model'] = joblib.load(MODEL_PATH)\n"
                    "    state['loaded_at'] = time.strftime(\"%Y-%m-%dT%H:%M:%S\")\n\n"
                    "@app.on_event('startup')\n"
                    "def startup():\n"
                    "    load_model()\n\n"
                    "@app.post('/reload')\n"
                    "def reload_model():\n"
                    "    load_model()\n"
                    "    return {'status': 'reloaded', 'at': state['loaded_at']}\n\n"
                    "@app.get('/health')\n"
                    "def health():\n"
                    "    return {'status': 'ok', 'model_loaded': state['model'] is not None,\n"
                    "            'loaded_at': state['loaded_at']}\n\n"
                    "@app.post('/predict')\n"
                    "def predict(x: list):\n"
                    "    if state['model'] is None:\n"
                    "        raise HTTPException(503, 'Model not loaded')\n"
                    "    return {'prediction': int(state['model'].predict([x])[0])}\n"
                    "'''\n"
                    "print(ADVANCED_API)"
                )
            },
        ],
        "rw_scenario": "A retail company wants to serve their churn prediction model as a REST API so their CRM system can call it in real time to flag at-risk customers.",
        "rw_code": (
            "# Churn prediction API skeleton\n"
            "CHURN_API = '''\n"
            "from fastapi import FastAPI\n"
            "from pydantic import BaseModel, Field\n"
            "from typing import Optional\n"
            "import joblib, numpy as np\n\n"
            "app = FastAPI(title='Churn Prediction API', version='1.0')\n"
            "model = joblib.load('churn_model.joblib')\n\n"
            "class CustomerFeatures(BaseModel):\n"
            "    tenure_months:     int   = Field(..., ge=0, le=120)\n"
            "    monthly_charges:   float = Field(..., ge=0)\n"
            "    total_charges:     float = Field(..., ge=0)\n"
            "    num_products:      int   = Field(..., ge=1, le=10)\n"
            "    has_support_calls: bool\n\n"
            "@app.post('/predict/churn')\n"
            "def predict_churn(customer: CustomerFeatures):\n"
            "    X = np.array([[\n"
            "        customer.tenure_months, customer.monthly_charges,\n"
            "        customer.total_charges, customer.num_products,\n"
            "        int(customer.has_support_calls)\n"
            "    ]])\n"
            "    churn_prob = float(model.predict_proba(X)[0, 1])\n"
            "    return {\n"
            "        'churn_probability': round(churn_prob, 4),\n"
            "        'risk_level': 'HIGH' if churn_prob > 0.7 else 'MEDIUM' if churn_prob > 0.4 else 'LOW'\n"
            "    }\n"
            "'''\n"
            "print(CHURN_API)"
        ),
        "practice": {
            "title": "Sentiment API",
            "desc": "Write a complete FastAPI app that accepts a text string and returns its VADER sentiment label and compound score. Include a /health endpoint.",
            "starter": (
                "# Save as sentiment_api.py\n"
                "# Run: uvicorn sentiment_api:app --reload\n\n"
                "SENTIMENT_API = '''\n"
                "from fastapi import FastAPI\n"
                "from pydantic import BaseModel\n"
                "import nltk\n"
                "nltk.download('vader_lexicon', quiet=True)\n"
                "from nltk.sentiment.vader import SentimentIntensityAnalyzer\n\n"
                "app = FastAPI()\n"
                "# TODO: create SentimentIntensityAnalyzer instance\n\n"
                "class TextRequest(BaseModel):\n"
                "    text: str\n\n"
                "# TODO: POST /analyze -> return label + compound score\n"
                "# TODO: GET /health -> return {'status': 'ok'}\n"
                "'''\n"
                "print(SENTIMENT_API)"
            )
        }
    },
    {
        "title": "3. Experiment Tracking with MLflow",
        "desc": "Track experiments, log parameters and metrics, compare runs, and register models for deployment using MLflow.",
        "examples": [
            {
                "label": "Log a training run with MLflow",
                "code": (
                    "try:\n"
                    "    import mlflow\n"
                    "    from sklearn.ensemble import RandomForestClassifier\n"
                    "    from sklearn.datasets import load_iris\n"
                    "    from sklearn.model_selection import train_test_split\n"
                    "    from sklearn.metrics import accuracy_score, f1_score\n\n"
                    "    X, y = load_iris(return_X_y=True)\n"
                    "    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
                    "    mlflow.set_experiment('iris-classification')\n\n"
                    "    with mlflow.start_run(run_name='random-forest-v1'):\n"
                    "        params = {'n_estimators': 100, 'max_depth': 5, 'random_state': 42}\n"
                    "        mlflow.log_params(params)\n\n"
                    "        model = RandomForestClassifier(**params)\n"
                    "        model.fit(X_train, y_train)\n"
                    "        preds = model.predict(X_test)\n\n"
                    "        mlflow.log_metric('accuracy', accuracy_score(y_test, preds))\n"
                    "        mlflow.log_metric('f1',       f1_score(y_test, preds, average='weighted'))\n"
                    "        mlflow.sklearn.log_model(model, 'model')\n\n"
                    "    print('Run logged. View: mlflow ui')\n"
                    "except ImportError:\n"
                    "    print('pip install mlflow')"
                )
            },
            {
                "label": "Comparing multiple runs",
                "code": (
                    "try:\n"
                    "    import mlflow\n"
                    "    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
                    "    from sklearn.linear_model import LogisticRegression\n"
                    "    from sklearn.datasets import load_iris\n"
                    "    from sklearn.model_selection import train_test_split\n"
                    "    from sklearn.metrics import accuracy_score\n\n"
                    "    X, y = load_iris(return_X_y=True)\n"
                    "    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
                    "    mlflow.set_experiment('iris-comparison')\n\n"
                    "    models = [\n"
                    "        ('LogisticRegression', LogisticRegression(max_iter=200)),\n"
                    "        ('RandomForest',       RandomForestClassifier(n_estimators=50, random_state=42)),\n"
                    "        ('GradientBoosting',   GradientBoostingClassifier(n_estimators=50, random_state=42)),\n"
                    "    ]\n\n"
                    "    for name, clf in models:\n"
                    "        with mlflow.start_run(run_name=name):\n"
                    "            clf.fit(X_train, y_train)\n"
                    "            acc = accuracy_score(y_test, clf.predict(X_test))\n"
                    "            mlflow.log_metric('accuracy', acc)\n"
                    "            mlflow.log_param('model_type', name)\n"
                    "            print(f'{name}: {acc:.4f}')\n"
                    "except ImportError:\n"
                    "    print('pip install mlflow')"
                )
            },
            {
                "label": "Autolog with sklearn",
                "code": (
                    "try:\n"
                    "    import mlflow\n"
                    "    import mlflow.sklearn\n"
                    "    from sklearn.ensemble import GradientBoostingClassifier\n"
                    "    from sklearn.datasets import load_breast_cancer\n"
                    "    from sklearn.model_selection import train_test_split\n\n"
                    "    mlflow.sklearn.autolog()  # auto-logs params, metrics, model\n\n"
                    "    X, y = load_breast_cancer(return_X_y=True)\n"
                    "    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\n"
                    "    with mlflow.start_run(run_name='autolog-demo'):\n"
                    "        model = GradientBoostingClassifier(n_estimators=100)\n"
                    "        model.fit(X_train, y_train)\n"
                    "        print('Autolog complete — everything captured automatically!')\n"
                    "        print('Accuracy:', model.score(X_test, y_test))\n"
                    "except ImportError:\n"
                    "    print('pip install mlflow')"
                )
            },
            {
                "label": "Load a logged model from MLflow registry",
                "code": (
                    "try:\n"
                    "    import mlflow\n\n"
                    "    # After running an experiment, load the best run's model:\n"
                    "    # Option 1: by run_id\n"
                    "    # model = mlflow.sklearn.load_model('runs:/<run_id>/model')\n\n"
                    "    # Option 2: from Model Registry (after registering)\n"
                    "    # model = mlflow.sklearn.load_model('models:/IrisClassifier/Production')\n\n"
                    "    # Option 3: query best run programmatically\n"
                    "    client = mlflow.tracking.MlflowClient()\n"
                    "    experiment = client.get_experiment_by_name('iris-comparison')\n"
                    "    if experiment:\n"
                    "        runs = client.search_runs(\n"
                    "            experiment_ids=[experiment.experiment_id],\n"
                    "            order_by=['metrics.accuracy DESC'],\n"
                    "            max_results=1\n"
                    "        )\n"
                    "        if runs:\n"
                    "            best = runs[0]\n"
                    "            print(f'Best run: {best.info.run_id}')\n"
                    "            print(f'Accuracy: {best.data.metrics[\"accuracy\"]:.4f}')\n"
                    "            # model = mlflow.sklearn.load_model(f'runs:/{best.info.run_id}/model')\n"
                    "        else:\n"
                    "            print('No runs found — run the comparison example first.')\n"
                    "    else:\n"
                    "        print('Experiment not found — run the comparison example first.')\n"
                    "except ImportError:\n"
                    "    print('pip install mlflow')"
                )
            },
        ],
        "rw_scenario": "A team of data scientists is running hyperparameter sweeps for a credit scoring model. They need to track every experiment and promote the best model to production.",
        "rw_code": (
            "try:\n"
            "    import mlflow\n"
            "    from sklearn.ensemble import GradientBoostingClassifier\n"
            "    from sklearn.datasets import make_classification\n"
            "    from sklearn.model_selection import train_test_split\n"
            "    from sklearn.metrics import roc_auc_score\n"
            "    import itertools\n\n"
            "    X, y = make_classification(n_samples=1000, random_state=42)\n"
            "    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\n"
            "    mlflow.set_experiment('credit-scoring-sweep')\n\n"
            "    param_grid = list(itertools.product([50, 100], [3, 5], [0.05, 0.1]))\n"
            "    best_auc, best_run_id = 0, None\n\n"
            "    for n_est, depth, lr in param_grid:\n"
            "        with mlflow.start_run():\n"
            "            model = GradientBoostingClassifier(n_estimators=n_est, max_depth=depth, learning_rate=lr)\n"
            "            model.fit(X_train, y_train)\n"
            "            auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])\n"
            "            mlflow.log_params({'n_estimators': n_est, 'max_depth': depth, 'learning_rate': lr})\n"
            "            mlflow.log_metric('roc_auc', auc)\n"
            "            mlflow.sklearn.log_model(model, 'model')\n"
            "            if auc > best_auc:\n"
            "                best_auc = auc\n"
            "                best_run_id = mlflow.active_run().info.run_id\n\n"
            "    print(f'Best AUC: {best_auc:.4f} | Run: {best_run_id}')\n"
            "except ImportError:\n"
            "    print('pip install mlflow scikit-learn')"
        ),
        "practice": {
            "title": "Hyperparameter Sweep Logger",
            "desc": "Run a grid search over n_estimators=[10,50,100] and max_depth=[3,5] for a RandomForest on the iris dataset, log each run to MLflow, then print the best run_id and accuracy.",
            "starter": (
                "try:\n"
                "    import mlflow\n"
                "    from sklearn.ensemble import RandomForestClassifier\n"
                "    from sklearn.datasets import load_iris\n"
                "    from sklearn.model_selection import train_test_split\n"
                "    from sklearn.metrics import accuracy_score\n\n"
                "    X, y = load_iris(return_X_y=True)\n"
                "    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\n"
                "    mlflow.set_experiment('iris-sweep')\n\n"
                "    # TODO: loop over n_estimators and max_depth\n"
                "    # TODO: log params and accuracy in each run\n"
                "    # TODO: track best_accuracy and best_run_id\n"
                "    # TODO: print winner\n\n"
                "except ImportError:\n"
                "    print('pip install mlflow')"
            )
        }
    },
    {
        "title": "4. Docker for ML Models",
        "desc": "Package ML models and APIs in Docker containers for reproducible, portable deployment. Learn Dockerfiles, image building, and running containers.",
        "examples": [
            {
                "label": "Minimal Dockerfile for a FastAPI ML app",
                "code": (
                    "DOCKERFILE = '''\n"
                    "# Dockerfile\n"
                    "FROM python:3.11-slim\n\n"
                    "WORKDIR /app\n\n"
                    "# Install dependencies first for layer caching\n"
                    "COPY requirements.txt .\n"
                    "RUN pip install --no-cache-dir -r requirements.txt\n\n"
                    "# Copy application code\n"
                    "COPY app.py .\n"
                    "COPY iris_rf.joblib .\n\n"
                    "# Expose port\n"
                    "EXPOSE 8000\n\n"
                    "# Start server\n"
                    "CMD [\"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
                    "'''\n\n"
                    "REQUIREMENTS = '''\n"
                    "fastapi==0.111.0\n"
                    "uvicorn==0.30.0\n"
                    "scikit-learn==1.5.0\n"
                    "joblib==1.4.2\n"
                    "numpy==1.26.4\n"
                    "'''\n\n"
                    "print('Dockerfile:')\n"
                    "print(DOCKERFILE)\n"
                    "print('requirements.txt:')\n"
                    "print(REQUIREMENTS)"
                )
            },
            {
                "label": "Docker build and run commands",
                "code": (
                    "# Build and run Docker commands (run these in your terminal)\n\n"
                    "COMMANDS = '''\n"
                    "# Build image\n"
                    "docker build -t iris-api:v1 .\n\n"
                    "# Run container\n"
                    "docker run -d -p 8000:8000 --name iris-api iris-api:v1\n\n"
                    "# Test it\n"
                    "curl -X POST http://localhost:8000/predict \\\n"
                    "  -H 'Content-Type: application/json' \\\n"
                    "  -d '{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}'\n\n"
                    "# View logs\n"
                    "docker logs iris-api\n\n"
                    "# Stop and remove\n"
                    "docker stop iris-api && docker rm iris-api\n\n"
                    "# Push to Docker Hub\n"
                    "docker tag iris-api:v1 yourusername/iris-api:v1\n"
                    "docker push yourusername/iris-api:v1\n"
                    "'''\n"
                    "print(COMMANDS)"
                )
            },
            {
                "label": "Multi-stage Docker build (smaller image)",
                "code": (
                    "MULTISTAGE_DOCKERFILE = '''\n"
                    "# Stage 1: build dependencies\n"
                    "FROM python:3.11-slim AS builder\n"
                    "WORKDIR /app\n"
                    "COPY requirements.txt .\n"
                    "RUN pip install --no-cache-dir --prefix=/install -r requirements.txt\n\n"
                    "# Stage 2: lean runtime image\n"
                    "FROM python:3.11-slim\n"
                    "WORKDIR /app\n"
                    "COPY --from=builder /install /usr/local\n"
                    "COPY app.py iris_rf.joblib ./\n\n"
                    "# Non-root user for security\n"
                    "RUN useradd -m appuser\n"
                    "USER appuser\n\n"
                    "EXPOSE 8000\n"
                    "CMD [\"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
                    "'''\n"
                    "print(MULTISTAGE_DOCKERFILE)"
                )
            },
            {
                "label": "docker-compose for API + model server",
                "code": (
                    "COMPOSE_YAML = '''\n"
                    "# docker-compose.yml\n"
                    "version: \"3.9\"\n\n"
                    "services:\n"
                    "  api:\n"
                    "    build: .\n"
                    "    ports:\n"
                    "      - \"8000:8000\"\n"
                    "    environment:\n"
                    "      - MODEL_PATH=/models/iris_rf.joblib\n"
                    "    volumes:\n"
                    "      - ./models:/models:ro\n"
                    "    restart: unless-stopped\n"
                    "    healthcheck:\n"
                    "      test: [\"CMD\", \"curl\", \"-f\", \"http://localhost:8000/health\"]\n"
                    "      interval: 30s\n"
                    "      timeout: 10s\n"
                    "      retries: 3\n\n"
                    "  mlflow:\n"
                    "    image: ghcr.io/mlflow/mlflow:latest\n"
                    "    ports:\n"
                    "      - \"5000:5000\"\n"
                    "    command: mlflow server --host 0.0.0.0\n"
                    "    volumes:\n"
                    "      - mlflow_data:/mlflow\n\n"
                    "volumes:\n"
                    "  mlflow_data:\n"
                    "'''\n"
                    "print(COMPOSE_YAML)"
                )
            },
        ],
        "rw_scenario": "A startup wants to deploy their recommendation model to AWS. They containerize it with Docker so it runs identically in dev, staging, and production.",
        "rw_code": (
            "import pathlib\n\n"
            "# Generate project structure for a dockerized ML API\n"
            "files = {\n"
            "    'Dockerfile': '''\n"
            "FROM python:3.11-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt .\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY . .\n"
            "EXPOSE 8000\n"
            "CMD [\"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
            "''',\n"
            "    'requirements.txt': 'fastapi\\nuvicorn\\nscikit-learn\\njoblib\\nnumpy\\n',\n"
            "    '.dockerignore': '__pycache__\\n*.pyc\\n.git\\n*.ipynb\\n',\n"
            "    'app.py': '''\n"
            "from fastapi import FastAPI\n"
            "from pydantic import BaseModel\n"
            "import joblib, numpy as np, os\n\n"
            "app = FastAPI()\n"
            "model = joblib.load(os.getenv('MODEL_PATH', 'model.joblib'))\n\n"
            "class Request(BaseModel):\n"
            "    features: list\n\n"
            "@app.post('/predict')\n"
            "def predict(req: Request):\n"
            "    return {'prediction': int(model.predict([req.features])[0])}\n\n"
            "@app.get('/health')\n"
            "def health():\n"
            "    return {'status': 'ok'}\n"
            "''',\n"
            "}\n\n"
            "proj = pathlib.Path('ml_docker_project')\n"
            "proj.mkdir(exist_ok=True)\n"
            "for fname, content in files.items():\n"
            "    (proj / fname).write_text(content.strip())\n"
            "    print(f'Created: {proj / fname}')"
        ),
        "practice": {
            "title": "Dockerfile Generator",
            "desc": "Write a Python function that generates a Dockerfile string given a list of pip packages, a Python version, and an entrypoint command.",
            "starter": (
                "def generate_dockerfile(packages: list, python_version: str = '3.11', entrypoint: str = 'python app.py') -> str:\n"
                "    # TODO: generate FROM, WORKDIR, COPY requirements.txt, RUN pip install, COPY ., CMD\n"
                "    pass\n\n"
                "dockerfile = generate_dockerfile(\n"
                "    packages=['fastapi', 'uvicorn', 'scikit-learn', 'joblib'],\n"
                "    python_version='3.11',\n"
                "    entrypoint='uvicorn app:app --host 0.0.0.0 --port 8000'\n"
                ")\n"
                "print(dockerfile)"
            )
        }
    },
    {
        "title": "5. Model Monitoring & Data Drift",
        "desc": "Monitor deployed models for performance degradation and data drift. Detect distribution shifts between training and production data.",
        "examples": [
            {
                "label": "Monitoring prediction distribution over time",
                "code": (
                    "import numpy as np\n"
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n\n"
                    "# Simulate production predictions over time\n"
                    "np.random.seed(42)\n"
                    "weeks = 8\n"
                    "# Week 1-4: stable; Week 5-8: drift\n"
                    "pred_probs = [\n"
                    "    np.random.beta(2, 5, 1000) for _ in range(4)  # stable\n"
                    "] + [\n"
                    "    np.random.beta(5, 2, 1000) for _ in range(4)  # drifted\n"
                    "]\n\n"
                    "mean_preds = [p.mean() for p in pred_probs]\n"
                    "print('Weekly mean prediction probabilities:')\n"
                    "for w, m in enumerate(mean_preds, 1):\n"
                    "    drift_flag = ' *** DRIFT DETECTED ***' if m > 0.5 else ''\n"
                    "    print(f'  Week {w}: {m:.3f}{drift_flag}')"
                )
            },
            {
                "label": "KS test for feature distribution drift",
                "code": (
                    "from scipy import stats\n"
                    "import numpy as np\n\n"
                    "# Training data distribution\n"
                    "np.random.seed(42)\n"
                    "train_data = {\n"
                    "    'age':    np.random.normal(35, 10, 1000),\n"
                    "    'income': np.random.lognormal(10, 0.5, 1000),\n"
                    "}\n\n"
                    "# Production data (age drifted, income stable)\n"
                    "prod_data = {\n"
                    "    'age':    np.random.normal(45, 12, 500),  # shifted mean\n"
                    "    'income': np.random.lognormal(10, 0.5, 500),  # same\n"
                    "}\n\n"
                    "print('Kolmogorov-Smirnov Drift Test:')\n"
                    "for feature in train_data:\n"
                    "    ks_stat, p_value = stats.ks_2samp(train_data[feature], prod_data[feature])\n"
                    "    drift = 'DRIFT' if p_value < 0.05 else 'OK'\n"
                    "    print(f'  {feature}: KS={ks_stat:.3f}, p={p_value:.4f} -> {drift}')"
                )
            },
            {
                "label": "Population Stability Index (PSI)",
                "code": (
                    "import numpy as np\n\n"
                    "def psi(expected, actual, bins=10):\n"
                    "    \"\"\"Population Stability Index. PSI < 0.1 = stable, 0.1-0.25 = slight shift, > 0.25 = major shift.\"\"\"\n"
                    "    breakpoints = np.percentile(expected, np.linspace(0, 100, bins + 1))\n"
                    "    breakpoints = np.unique(breakpoints)\n"
                    "    exp_counts = np.histogram(expected, bins=breakpoints)[0]\n"
                    "    act_counts = np.histogram(actual,   bins=breakpoints)[0]\n"
                    "    # Avoid division by zero\n"
                    "    exp_pct = np.where(exp_counts == 0, 0.0001, exp_counts / len(expected))\n"
                    "    act_pct = np.where(act_counts == 0, 0.0001, act_counts / len(actual))\n"
                    "    return np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct))\n\n"
                    "np.random.seed(42)\n"
                    "train_scores = np.random.beta(2, 5, 1000)\n"
                    "stable_prod  = np.random.beta(2, 5, 500)     # same distribution\n"
                    "drifted_prod = np.random.beta(5, 2, 500)     # different distribution\n\n"
                    "print(f'PSI stable:  {psi(train_scores, stable_prod):.4f}')   # expect < 0.1\n"
                    "print(f'PSI drifted: {psi(train_scores, drifted_prod):.4f}')  # expect > 0.25"
                )
            },
            {
                "label": "Alerting on accuracy degradation",
                "code": (
                    "import numpy as np\n"
                    "from collections import deque\n\n"
                    "class ModelMonitor:\n"
                    "    def __init__(self, window=100, threshold=0.05):\n"
                    "        self.window = window\n"
                    "        self.threshold = threshold\n"
                    "        self.baseline_acc = None\n"
                    "        self.recent = deque(maxlen=window)\n"
                    "        self.alerts = []\n\n"
                    "    def set_baseline(self, accuracy):\n"
                    "        self.baseline_acc = accuracy\n\n"
                    "    def log_prediction(self, pred, true_label):\n"
                    "        self.recent.append(int(pred == true_label))\n"
                    "        if len(self.recent) == self.window:\n"
                    "            current_acc = sum(self.recent) / self.window\n"
                    "            drop = self.baseline_acc - current_acc\n"
                    "            if drop > self.threshold:\n"
                    "                alert = f'ALERT: accuracy dropped {drop:.1%} (current={current_acc:.3f})'\n"
                    "                self.alerts.append(alert)\n"
                    "                print(alert)\n\n"
                    "np.random.seed(42)\n"
                    "monitor = ModelMonitor(window=50, threshold=0.05)\n"
                    "monitor.set_baseline(0.95)\n\n"
                    "# Good predictions, then degradation\n"
                    "for _ in range(100):\n"
                    "    monitor.log_prediction(1, 1 if np.random.rand() > 0.05 else 0)\n"
                    "for _ in range(100):\n"
                    "    monitor.log_prediction(1, 1 if np.random.rand() > 0.20 else 0)  # degraded"
                )
            },
        ],
        "rw_scenario": "A bank's credit risk model needs continuous monitoring after deployment. Any significant accuracy drop or feature distribution shift should trigger a retraining alert.",
        "rw_code": (
            "import numpy as np\n"
            "from scipy import stats\n"
            "from dataclasses import dataclass, field\n"
            "from typing import Dict, List\n\n"
            "@dataclass\n"
            "class DriftReport:\n"
            "    feature: str\n"
            "    ks_stat: float\n"
            "    p_value: float\n"
            "    drifted: bool\n\n"
            "class MLMonitor:\n"
            "    def __init__(self, reference_data: Dict[str, np.ndarray], alpha: float = 0.05):\n"
            "        self.reference = reference_data\n"
            "        self.alpha = alpha\n\n"
            "    def check_drift(self, current_data: Dict[str, np.ndarray]) -> List[DriftReport]:\n"
            "        reports = []\n"
            "        for feature, ref_vals in self.reference.items():\n"
            "            if feature not in current_data:\n"
            "                continue\n"
            "            ks, p = stats.ks_2samp(ref_vals, current_data[feature])\n"
            "            reports.append(DriftReport(feature, round(ks, 4), round(p, 4), p < self.alpha))\n"
            "        return reports\n\n"
            "np.random.seed(42)\n"
            "reference = {'credit_score': np.random.normal(680, 80, 1000),\n"
            "             'income':       np.random.lognormal(11, 0.4, 1000)}\n"
            "current   = {'credit_score': np.random.normal(630, 90, 300),   # drifted\n"
            "             'income':       np.random.lognormal(11, 0.4, 300)} # stable\n\n"
            "monitor = MLMonitor(reference)\n"
            "for report in monitor.check_drift(current):\n"
            "    status = 'DRIFT' if report.drifted else 'OK'\n"
            "    print(f'{report.feature}: KS={report.ks_stat}, p={report.p_value} -> {status}')"
        ),
        "practice": {
            "title": "Drift Dashboard",
            "desc": "Compute PSI for 3 features between training and production data, print a table with PSI values and stability labels (stable/warning/critical).",
            "starter": (
                "import numpy as np\n\n"
                "def psi(expected, actual, bins=10):\n"
                "    breakpoints = np.unique(np.percentile(expected, np.linspace(0, 100, bins + 1)))\n"
                "    exp_c = np.histogram(expected, bins=breakpoints)[0]\n"
                "    act_c = np.histogram(actual,   bins=breakpoints)[0]\n"
                "    e = np.where(exp_c == 0, 1e-4, exp_c / len(expected))\n"
                "    a = np.where(act_c == 0, 1e-4, act_c / len(actual))\n"
                "    return float(np.sum((a - e) * np.log(a / e)))\n\n"
                "np.random.seed(42)\n"
                "train = {'age': np.random.normal(35, 10, 1000),\n"
                "         'income': np.random.lognormal(10, 0.5, 1000),\n"
                "         'score': np.random.beta(2, 5, 1000)}\n"
                "prod  = {'age': np.random.normal(45, 12, 500),   # drifted\n"
                "         'income': np.random.lognormal(10, 0.5, 500),\n"
                "         'score': np.random.beta(5, 2, 500)}      # drifted\n\n"
                "# TODO: compute PSI for each feature\n"
                "# TODO: print table: feature | PSI | stability label"
            )
        }
    },
    {
        "title": "6. CI/CD for ML Pipelines",
        "desc": "Automate model training, testing, and deployment with CI/CD. Learn to write GitHub Actions workflows and automated model validation.",
        "examples": [
            {
                "label": "Automated model validation script",
                "code": (
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "from sklearn.datasets import load_iris\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "import numpy as np, sys\n\n"
                    "ACCURACY_THRESHOLD = 0.95\n"
                    "F1_THRESHOLD = 0.94\n\n"
                    "def validate_model(model, X, y):\n"
                    "    \"\"\"Return True if model passes all quality gates.\"\"\"\n"
                    "    acc_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')\n"
                    "    f1_scores  = cross_val_score(model, X, y, cv=5, scoring='f1_weighted')\n\n"
                    "    print(f'Accuracy: {acc_scores.mean():.4f} ± {acc_scores.std():.4f}')\n"
                    "    print(f'F1:       {f1_scores.mean():.4f} ± {f1_scores.std():.4f}')\n\n"
                    "    passed = acc_scores.mean() >= ACCURACY_THRESHOLD and f1_scores.mean() >= F1_THRESHOLD\n"
                    "    print('PASSED' if passed else 'FAILED')\n"
                    "    return passed\n\n"
                    "X, y = load_iris(return_X_y=True)\n"
                    "model = RandomForestClassifier(n_estimators=100, random_state=42)\n"
                    "if not validate_model(model, X, y):\n"
                    "    sys.exit(1)  # Fail CI pipeline"
                )
            },
            {
                "label": "GitHub Actions workflow for ML",
                "code": (
                    "GITHUB_ACTIONS_YAML = '''\n"
                    "# .github/workflows/ml_pipeline.yml\n"
                    "name: ML Pipeline\n\n"
                    "on:\n"
                    "  push:\n"
                    "    branches: [main]\n"
                    "  pull_request:\n"
                    "    branches: [main]\n\n"
                    "jobs:\n"
                    "  train-and-validate:\n"
                    "    runs-on: ubuntu-latest\n"
                    "    steps:\n"
                    "      - uses: actions/checkout@v4\n\n"
                    "      - name: Set up Python\n"
                    "        uses: actions/setup-python@v5\n"
                    "        with:\n"
                    "          python-version: '3.11'\n\n"
                    "      - name: Install dependencies\n"
                    "        run: pip install -r requirements.txt\n\n"
                    "      - name: Train model\n"
                    "        run: python train.py\n\n"
                    "      - name: Validate model\n"
                    "        run: python validate.py\n\n"
                    "      - name: Upload model artifact\n"
                    "        uses: actions/upload-artifact@v4\n"
                    "        with:\n"
                    "          name: trained-model\n"
                    "          path: model.joblib\n"
                    "'''\n"
                    "print(GITHUB_ACTIONS_YAML)"
                )
            },
            {
                "label": "Automated test suite for ML code",
                "code": (
                    "# tests/test_model.py (run with: pytest tests/)\n"
                    "import pytest, numpy as np\n"
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "from sklearn.datasets import load_iris\n\n"
                    "TEST_CODE = '''\n"
                    "import pytest, numpy as np, joblib\n"
                    "from sklearn.datasets import load_iris\n\n"
                    "@pytest.fixture\n"
                    "def model():\n"
                    "    return joblib.load('iris_rf.joblib')\n\n"
                    "@pytest.fixture\n"
                    "def iris_data():\n"
                    "    X, y = load_iris(return_X_y=True)\n"
                    "    return X, y\n\n"
                    "def test_model_accuracy(model, iris_data):\n"
                    "    X, y = iris_data\n"
                    "    assert model.score(X, y) >= 0.95\n\n"
                    "def test_model_output_shape(model, iris_data):\n"
                    "    X, _ = iris_data\n"
                    "    preds = model.predict(X[:10])\n"
                    "    assert preds.shape == (10,)\n\n"
                    "def test_model_classes(model):\n"
                    "    assert len(model.classes_) == 3\n\n"
                    "def test_prediction_valid_class(model, iris_data):\n"
                    "    X, _ = iris_data\n"
                    "    preds = model.predict(X)\n"
                    "    assert set(preds).issubset({0, 1, 2})\n"
                    "'''\n"
                    "print(TEST_CODE)"
                )
            },
            {
                "label": "Pre-deployment model comparison",
                "code": (
                    "import joblib\n"
                    "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
                    "from sklearn.datasets import load_iris\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.metrics import accuracy_score, f1_score\n\n"
                    "X, y = load_iris(return_X_y=True)\n"
                    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
                    "def evaluate(model, X_test, y_test):\n"
                    "    preds = model.predict(X_test)\n"
                    "    return {'accuracy': accuracy_score(y_test, preds),\n"
                    "            'f1': f1_score(y_test, preds, average='weighted')}\n\n"
                    "# Champion: currently deployed model\n"
                    "champion = RandomForestClassifier(n_estimators=50, random_state=42).fit(X_train, y_train)\n"
                    "# Challenger: new candidate\n"
                    "challenger = GradientBoostingClassifier(n_estimators=50, random_state=42).fit(X_train, y_train)\n\n"
                    "champ_metrics = evaluate(champion, X_test, y_test)\n"
                    "chall_metrics = evaluate(challenger, X_test, y_test)\n\n"
                    "print(f'Champion:   {champ_metrics}')\n"
                    "print(f'Challenger: {chall_metrics}')\n"
                    "promote = chall_metrics['f1'] > champ_metrics['f1']\n"
                    "print(f'Promote challenger: {promote}')"
                )
            },
        ],
        "rw_scenario": "A team wants every pull request to automatically train and validate a model. If the model's F1 drops below 0.90, the PR is blocked from merging.",
        "rw_code": (
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.datasets import load_breast_cancer\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import f1_score, classification_report\n"
            "import sys, joblib\n\n"
            "F1_GATE = 0.90\n\n"
            "def train(X_train, y_train):\n"
            "    model = RandomForestClassifier(n_estimators=100, random_state=42)\n"
            "    model.fit(X_train, y_train)\n"
            "    return model\n\n"
            "def gate_check(model, X_test, y_test):\n"
            "    preds = model.predict(X_test)\n"
            "    f1 = f1_score(y_test, preds, average='weighted')\n"
            "    print(classification_report(y_test, preds))\n"
            "    if f1 < F1_GATE:\n"
            "        print(f'FAILED: F1={f1:.4f} < threshold {F1_GATE}')\n"
            "        sys.exit(1)\n"
            "    print(f'PASSED: F1={f1:.4f}')\n"
            "    return model\n\n"
            "X, y = load_breast_cancer(return_X_y=True)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "model = train(X_train, y_train)\n"
            "validated_model = gate_check(model, X_test, y_test)\n"
            "joblib.dump(validated_model, 'validated_model.joblib')\n"
            "print('Model saved — ready for deployment.')"
        ),
        "practice": {
            "title": "Quality Gate Script",
            "desc": "Write a validate.py script that loads a saved model, evaluates it against a test set, and exits with code 1 if accuracy < 0.92 or precision < 0.90.",
            "starter": (
                "import joblib, sys\n"
                "from sklearn.datasets import load_iris\n"
                "from sklearn.model_selection import train_test_split\n"
                "from sklearn.metrics import accuracy_score, precision_score\n\n"
                "ACCURACY_GATE  = 0.92\n"
                "PRECISION_GATE = 0.90\n\n"
                "def validate(model_path: str):\n"
                "    # TODO: load model from model_path\n"
                "    # TODO: load iris, split 80/20\n"
                "    # TODO: compute accuracy and weighted precision\n"
                "    # TODO: print results\n"
                "    # TODO: sys.exit(1) if below thresholds\n"
                "    pass\n\n"
                "validate('iris_rf.joblib')"
            )
        }
    },
    {
        "title": "7. Feature Stores & Pipelines",
        "desc": "Build reproducible feature engineering pipelines. Use sklearn Pipeline, ColumnTransformer, and custom transformers for production-ready preprocessing.",
        "examples": [
            {
                "label": "ColumnTransformer for mixed data",
                "code": (
                    "import pandas as pd\n"
                    "import numpy as np\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.compose import ColumnTransformer\n"
                    "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
                    "from sklearn.impute import SimpleImputer\n\n"
                    "df = pd.DataFrame({\n"
                    "    'age':    [25, np.nan, 35, 42, 28],\n"
                    "    'income': [50000, 75000, np.nan, 90000, 62000],\n"
                    "    'city':   ['NYC', 'LA', 'NYC', 'Chicago', 'LA'],\n"
                    "    'gender': ['M', 'F', 'F', 'M', np.nan],\n"
                    "})\n\n"
                    "num_features = ['age', 'income']\n"
                    "cat_features = ['city', 'gender']\n\n"
                    "num_pipe = Pipeline([('impute', SimpleImputer(strategy='median')),\n"
                    "                     ('scale',  StandardScaler())])\n"
                    "cat_pipe = Pipeline([('impute', SimpleImputer(strategy='most_frequent')),\n"
                    "                     ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])\n\n"
                    "preprocessor = ColumnTransformer([\n"
                    "    ('num', num_pipe, num_features),\n"
                    "    ('cat', cat_pipe, cat_features),\n"
                    "])\n\n"
                    "X = preprocessor.fit_transform(df)\n"
                    "print('Transformed shape:', X.shape)\n"
                    "print('First row:', X[0].round(3))"
                )
            },
            {
                "label": "Custom transformer with BaseEstimator",
                "code": (
                    "import numpy as np\n"
                    "import pandas as pd\n"
                    "from sklearn.base import BaseEstimator, TransformerMixin\n"
                    "from sklearn.pipeline import Pipeline\n\n"
                    "class LogTransformer(BaseEstimator, TransformerMixin):\n"
                    "    def __init__(self, offset=1):\n"
                    "        self.offset = offset\n\n"
                    "    def fit(self, X, y=None):\n"
                    "        return self\n\n"
                    "    def transform(self, X):\n"
                    "        return np.log(X + self.offset)\n\n"
                    "class OutlierClipper(BaseEstimator, TransformerMixin):\n"
                    "    def fit(self, X, y=None):\n"
                    "        self.lower_ = np.percentile(X, 1, axis=0)\n"
                    "        self.upper_ = np.percentile(X, 99, axis=0)\n"
                    "        return self\n\n"
                    "    def transform(self, X):\n"
                    "        return np.clip(X, self.lower_, self.upper_)\n\n"
                    "X = np.array([[1, 1000], [5, 5000], [100, 100000], [1, 50]])\n"
                    "pipe = Pipeline([('clip', OutlierClipper()), ('log', LogTransformer())])\n"
                    "print('Original:\\n', X)\n"
                    "print('Transformed:\\n', pipe.fit_transform(X).round(3))"
                )
            },
            {
                "label": "Feature selection in pipeline",
                "code": (
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.feature_selection import SelectKBest, f_classif\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from sklearn.model_selection import cross_val_score\n\n"
                    "X, y = load_breast_cancer(return_X_y=True)\n"
                    "print(f'Original features: {X.shape[1]}')\n\n"
                    "pipe = Pipeline([\n"
                    "    ('scaler',  StandardScaler()),\n"
                    "    ('select',  SelectKBest(f_classif, k=10)),\n"
                    "    ('clf',     RandomForestClassifier(n_estimators=100, random_state=42)),\n"
                    "])\n\n"
                    "scores = cross_val_score(pipe, X, y, cv=5, scoring='accuracy')\n"
                    "print(f'CV accuracy (10 features): {scores.mean():.4f} ± {scores.std():.4f}')\n\n"
                    "pipe.fit(X, y)\n"
                    "selected = pipe['select'].get_support()\n"
                    "print(f'Selected feature indices: {selected.nonzero()[0]}')"
                )
            },
            {
                "label": "Persisting and reusing a fitted pipeline",
                "code": (
                    "import joblib\n"
                    "import pandas as pd\n"
                    "import numpy as np\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.compose import ColumnTransformer\n"
                    "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
                    "from sklearn.impute import SimpleImputer\n"
                    "from sklearn.linear_model import LogisticRegression\n\n"
                    "# Training data\n"
                    "train = pd.DataFrame({'age': [25,35,45,55], 'city': ['NYC','LA','NYC','LA'], 'target': [0,1,0,1]})\n"
                    "X_train = train.drop('target', axis=1)\n"
                    "y_train = train['target']\n\n"
                    "preprocessor = ColumnTransformer([\n"
                    "    ('num', StandardScaler(), ['age']),\n"
                    "    ('cat', OneHotEncoder(sparse_output=False), ['city']),\n"
                    "])\n"
                    "pipe = Pipeline([('prep', preprocessor), ('clf', LogisticRegression())])\n"
                    "pipe.fit(X_train, y_train)\n\n"
                    "# Save entire pipeline (includes fitted scaler + encoder)\n"
                    "joblib.dump(pipe, 'full_pipeline.joblib')\n\n"
                    "# Load and predict new data\n"
                    "loaded = joblib.load('full_pipeline.joblib')\n"
                    "new_data = pd.DataFrame({'age': [30, 50], 'city': ['LA', 'NYC']})\n"
                    "print('Predictions:', loaded.predict(new_data))"
                )
            },
        ],
        "rw_scenario": "An insurance company needs to preprocess complex customer data (mixed types, missing values, categorical variables) reproducibly in both training and production serving.",
        "rw_code": (
            "import pandas as pd\n"
            "import numpy as np\n"
            "import joblib\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
            "from sklearn.impute import SimpleImputer\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "np.random.seed(42)\n"
            "n = 500\n"
            "df = pd.DataFrame({\n"
            "    'age':        np.random.randint(18, 80, n).astype(float),\n"
            "    'income':     np.random.lognormal(10, 0.5, n),\n"
            "    'region':     np.random.choice(['North', 'South', 'East', 'West'], n),\n"
            "    'vehicle_age':np.random.randint(0, 20, n).astype(float),\n"
            "    'claim':      np.random.binomial(1, 0.15, n),\n"
            "})\n"
            "# Inject missing values\n"
            "df.loc[np.random.choice(n, 30), 'age'] = np.nan\n"
            "df.loc[np.random.choice(n, 20), 'region'] = np.nan\n\n"
            "X = df.drop('claim', axis=1)\n"
            "y = df['claim']\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "num_pipe = Pipeline([('imp', SimpleImputer(strategy='median')), ('scl', StandardScaler())])\n"
            "cat_pipe = Pipeline([('imp', SimpleImputer(strategy='most_frequent')),\n"
            "                     ('enc', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])\n\n"
            "prep = ColumnTransformer([\n"
            "    ('num', num_pipe, ['age', 'income', 'vehicle_age']),\n"
            "    ('cat', cat_pipe, ['region']),\n"
            "])\n"
            "full_pipe = Pipeline([('prep', prep), ('clf', GradientBoostingClassifier(random_state=42))])\n"
            "full_pipe.fit(X_train, y_train)\n\n"
            "print(f'Test accuracy: {full_pipe.score(X_test, y_test):.4f}')\n"
            "joblib.dump(full_pipe, 'insurance_pipeline.joblib')\n"
            "print('Pipeline saved.')"
        ),
        "practice": {
            "title": "Reusable Preprocessing Pipeline",
            "desc": "Build a ColumnTransformer pipeline for a dataset with numeric columns (impute median + scale) and categorical columns (impute mode + one-hot encode), then save and reload it.",
            "starter": (
                "import pandas as pd, numpy as np, joblib\n"
                "from sklearn.pipeline import Pipeline\n"
                "from sklearn.compose import ColumnTransformer\n"
                "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
                "from sklearn.impute import SimpleImputer\n\n"
                "data = pd.DataFrame({\n"
                "    'tenure':   [12, np.nan, 36, 24, 6],\n"
                "    'charges':  [50.0, 75.0, np.nan, 90.0, 45.0],\n"
                "    'plan':     ['basic', 'premium', 'basic', np.nan, 'premium'],\n"
                "    'country':  ['US', 'UK', 'US', 'CA', 'UK'],\n"
                "})\n\n"
                "# TODO: define num_pipe and cat_pipe\n"
                "# TODO: combine with ColumnTransformer\n"
                "# TODO: fit_transform data\n"
                "# TODO: save and reload with joblib\n"
                "# TODO: print transformed shape"
            )
        }
    },
    {
        "title": "8. A/B Testing for ML Models",
        "desc": "Safely roll out new models by running controlled experiments. Compare champion vs challenger using statistical tests to decide which to promote.",
        "examples": [
            {
                "label": "Traffic splitting for A/B model serving",
                "code": (
                    "import numpy as np\n"
                    "from dataclasses import dataclass\n"
                    "from typing import Any\n\n"
                    "@dataclass\n"
                    "class ABRouter:\n"
                    "    champion: Any\n"
                    "    challenger: Any\n"
                    "    challenger_pct: float = 0.1  # 10% traffic to challenger\n\n"
                    "    def predict(self, X):\n"
                    "        route = 'challenger' if np.random.rand() < self.challenger_pct else 'champion'\n"
                    "        model = self.challenger if route == 'challenger' else self.champion\n"
                    "        pred = model.predict([X])[0]\n"
                    "        return {'prediction': pred, 'model': route}\n\n"
                    "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
                    "from sklearn.datasets import load_iris\n\n"
                    "X, y = load_iris(return_X_y=True)\n"
                    "champion   = RandomForestClassifier(n_estimators=50, random_state=42).fit(X, y)\n"
                    "challenger = GradientBoostingClassifier(n_estimators=50, random_state=42).fit(X, y)\n\n"
                    "router = ABRouter(champion, challenger, challenger_pct=0.2)\n"
                    "for _ in range(5):\n"
                    "    result = router.predict(X[0])\n"
                    "    print(f'Model: {result[\"model\"]:12} | Prediction: {result[\"prediction\"]}')"
                )
            },
            {
                "label": "Collecting and comparing A/B results",
                "code": (
                    "import numpy as np\n"
                    "from collections import defaultdict\n"
                    "from scipy import stats\n\n"
                    "# Simulate A/B experiment: collect correct/incorrect per model\n"
                    "np.random.seed(42)\n"
                    "n_requests = 1000\n\n"
                    "results = defaultdict(list)\n"
                    "for _ in range(n_requests):\n"
                    "    group = 'challenger' if np.random.rand() < 0.2 else 'champion'\n"
                    "    # Simulated accuracy: champion=0.92, challenger=0.95\n"
                    "    accuracy = 0.95 if group == 'challenger' else 0.92\n"
                    "    correct = int(np.random.rand() < accuracy)\n"
                    "    results[group].append(correct)\n\n"
                    "for group, outcomes in results.items():\n"
                    "    print(f'{group}: n={len(outcomes)}, accuracy={np.mean(outcomes):.4f}')\n\n"
                    "# Two-proportion z-test\n"
                    "champ = results['champion']\n"
                    "chall = results['challenger']\n"
                    "_, p = stats.ttest_ind(champ, chall)\n"
                    "print(f'p-value: {p:.4f} -> {\"significant\" if p < 0.05 else \"not significant\"}')"
                )
            },
            {
                "label": "Statistical significance with chi-squared test",
                "code": (
                    "import numpy as np\n"
                    "from scipy import stats\n\n"
                    "# Confusion matrix style: correct vs incorrect per model\n"
                    "champion_results   = {'correct': 460, 'incorrect': 40}   # n=500, 92%\n"
                    "challenger_results = {'correct': 190, 'incorrect': 10}   # n=200, 95%\n\n"
                    "# Chi-squared contingency test\n"
                    "observed = np.array([\n"
                    "    [champion_results['correct'],   champion_results['incorrect']],\n"
                    "    [challenger_results['correct'], challenger_results['incorrect']],\n"
                    "])\n\n"
                    "chi2, p, dof, expected = stats.chi2_contingency(observed)\n"
                    "print(f'Chi2: {chi2:.4f}')\n"
                    "print(f'p-value: {p:.4f}')\n"
                    "print(f'Significant at alpha=0.05: {p < 0.05}')\n"
                    "if p < 0.05:\n"
                    "    champ_acc = champion_results['correct'] / sum(champion_results.values())\n"
                    "    chall_acc = challenger_results['correct'] / sum(challenger_results.values())\n"
                    "    winner = 'challenger' if chall_acc > champ_acc else 'champion'\n"
                    "    print(f'Promote: {winner}')"
                )
            },
            {
                "label": "Shadow mode deployment (no live impact)",
                "code": (
                    "import numpy as np\n"
                    "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
                    "from sklearn.datasets import load_iris\n"
                    "from sklearn.metrics import accuracy_score\n\n"
                    "X, y = load_iris(return_X_y=True)\n"
                    "champion   = RandomForestClassifier(n_estimators=50, random_state=42).fit(X, y)\n"
                    "challenger = GradientBoostingClassifier(n_estimators=50, random_state=42).fit(X, y)\n\n"
                    "shadow_log = []\n\n"
                    "def serve_with_shadow(X_sample, true_label=None):\n"
                    "    \"\"\"Serve champion, silently log challenger — no impact on users.\"\"\"\n"
                    "    champ_pred = champion.predict([X_sample])[0]\n"
                    "    chall_pred = challenger.predict([X_sample])[0]  # shadow\n"
                    "    shadow_log.append({'champion': champ_pred, 'challenger': chall_pred,\n"
                    "                       'true': true_label})\n"
                    "    return champ_pred  # only champion's prediction served\n\n"
                    "for xi, yi in zip(X[:20], y[:20]):\n"
                    "    serve_with_shadow(xi, yi)\n\n"
                    "champ_acc = np.mean([l['champion'] == l['true'] for l in shadow_log])\n"
                    "chall_acc = np.mean([l['challenger'] == l['true'] for l in shadow_log])\n"
                    "print(f'Shadow test: champion={champ_acc:.2f}, challenger={chall_acc:.2f}')"
                )
            },
        ],
        "rw_scenario": "An e-commerce company wants to test a new recommendation model against the current one. 10% of traffic goes to the new model; after 2 weeks they compare click-through rates statistically.",
        "rw_code": (
            "import numpy as np\n"
            "from scipy import stats\n"
            "from dataclasses import dataclass, field\n"
            "from typing import List\n\n"
            "@dataclass\n"
            "class ABExperiment:\n"
            "    name: str\n"
            "    challenger_pct: float = 0.1\n"
            "    champion_outcomes: List[float] = field(default_factory=list)\n"
            "    challenger_outcomes: List[float] = field(default_factory=list)\n\n"
            "    def log(self, reward: float):\n"
            "        group = 'challenger' if np.random.rand() < self.challenger_pct else 'champion'\n"
            "        (self.challenger_outcomes if group == 'challenger' else self.champion_outcomes).append(reward)\n\n"
            "    def report(self):\n"
            "        champ = np.array(self.champion_outcomes)\n"
            "        chall = np.array(self.challenger_outcomes)\n"
            "        _, p = stats.ttest_ind(chall, champ)\n"
            "        return {\n"
            "            'champion_mean':   round(champ.mean(), 4),\n"
            "            'challenger_mean': round(chall.mean(), 4),\n"
            "            'p_value':         round(p, 4),\n"
            "            'significant':     p < 0.05,\n"
            "            'promote':         p < 0.05 and chall.mean() > champ.mean(),\n"
            "        }\n\n"
            "np.random.seed(42)\n"
            "exp = ABExperiment('recommendation-v2', challenger_pct=0.1)\n"
            "for _ in range(10000):\n"
            "    # Simulate CTR: champion=5%, challenger=6%\n"
            "    reward = np.random.binomial(1, 0.06) if np.random.rand() < 0.1 else np.random.binomial(1, 0.05)\n"
            "    exp.log(reward)\n\n"
            "import json\n"
            "print(json.dumps(exp.report(), indent=2))"
        ),
        "practice": {
            "title": "A/B Test Analyzer",
            "desc": "Given two lists of binary outcomes (0=failure, 1=success) for model A and model B, compute conversion rates, run a chi-squared test, and print whether to promote model B.",
            "starter": (
                "import numpy as np\n"
                "from scipy import stats\n\n"
                "np.random.seed(42)\n"
                "model_a = np.random.binomial(1, 0.08, 5000)  # 8% conversion\n"
                "model_b = np.random.binomial(1, 0.10, 1000)  # 10% conversion\n\n"
                "def analyze_ab_test(a_outcomes, b_outcomes, alpha=0.05):\n"
                "    # TODO: compute conversion rates\n"
                "    # TODO: chi-squared test\n"
                "    # TODO: print results and promote/keep decision\n"
                "    pass\n\n"
                "analyze_ab_test(model_a, model_b)"
            )
        }
    },
    {
        "title": "9. Model Explainability",
        "desc": "Make black-box models interpretable. Use SHAP values, permutation importance, and LIME to explain individual predictions and global feature importance.",
        "examples": [
            {
                "label": "Permutation feature importance",
                "code": (
                    "import numpy as np\n"
                    "import pandas as pd\n"
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "from sklearn.inspection import permutation_importance\n"
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from sklearn.model_selection import train_test_split\n\n"
                    "data = load_breast_cancer()\n"
                    "X, y = data.data, data.target\n"
                    "X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\n"
                    "model = RandomForestClassifier(n_estimators=100, random_state=42)\n"
                    "model.fit(X_train, y_train)\n\n"
                    "result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)\n\n"
                    "importance_df = pd.DataFrame({\n"
                    "    'feature':   data.feature_names,\n"
                    "    'importance': result.importances_mean,\n"
                    "    'std':        result.importances_std,\n"
                    "}).sort_values('importance', ascending=False)\n\n"
                    "print(importance_df.head(10).to_string(index=False))"
                )
            },
            {
                "label": "SHAP values for tree models",
                "code": (
                    "try:\n"
                    "    import shap\n"
                    "    from sklearn.ensemble import GradientBoostingClassifier\n"
                    "    from sklearn.datasets import load_breast_cancer\n"
                    "    from sklearn.model_selection import train_test_split\n\n"
                    "    data = load_breast_cancer()\n"
                    "    X_train, X_test, y_train, y_test = train_test_split(\n"
                    "        data.data, data.target, random_state=42)\n\n"
                    "    model = GradientBoostingClassifier(n_estimators=100, random_state=42)\n"
                    "    model.fit(X_train, y_train)\n\n"
                    "    explainer = shap.TreeExplainer(model)\n"
                    "    shap_values = explainer.shap_values(X_test[:5])\n\n"
                    "    print('SHAP values for first test sample:')\n"
                    "    for feat, val in sorted(zip(data.feature_names, shap_values[0]),\n"
                    "                            key=lambda x: abs(x[1]), reverse=True)[:5]:\n"
                    "        print(f'  {feat:<35} {val:+.4f}')\n"
                    "except ImportError:\n"
                    "    print('pip install shap')"
                )
            },
            {
                "label": "LIME for individual prediction explanation",
                "code": (
                    "try:\n"
                    "    import lime\n"
                    "    from lime.lime_tabular import LimeTabularExplainer\n"
                    "    from sklearn.ensemble import RandomForestClassifier\n"
                    "    from sklearn.datasets import load_breast_cancer\n"
                    "    from sklearn.model_selection import train_test_split\n\n"
                    "    data = load_breast_cancer()\n"
                    "    X_train, X_test, y_train, y_test = train_test_split(\n"
                    "        data.data, data.target, random_state=42)\n\n"
                    "    model = RandomForestClassifier(n_estimators=100, random_state=42)\n"
                    "    model.fit(X_train, y_train)\n\n"
                    "    explainer = LimeTabularExplainer(\n"
                    "        X_train, feature_names=data.feature_names,\n"
                    "        class_names=data.target_names, mode='classification')\n\n"
                    "    exp = explainer.explain_instance(X_test[0], model.predict_proba, num_features=5)\n"
                    "    print('Prediction:', model.predict([X_test[0]])[0], '->', data.target_names[model.predict([X_test[0]])[0]])\n"
                    "    print('\\nTop contributing features:')\n"
                    "    for feat, weight in exp.as_list():\n"
                    "        print(f'  {feat[:45]:<45} {weight:+.4f}')\n"
                    "except ImportError:\n"
                    "    print('pip install lime')"
                )
            },
            {
                "label": "Partial dependence plots (sklearn)",
                "code": (
                    "import matplotlib\n"
                    "matplotlib.use('Agg')\n"
                    "import matplotlib.pyplot as plt\n"
                    "from sklearn.ensemble import GradientBoostingClassifier\n"
                    "from sklearn.inspection import PartialDependenceDisplay\n"
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from sklearn.model_selection import train_test_split\n\n"
                    "data = load_breast_cancer()\n"
                    "X_train, X_test, y_train, _ = train_test_split(data.data, data.target, random_state=42)\n\n"
                    "model = GradientBoostingClassifier(n_estimators=100, random_state=42)\n"
                    "model.fit(X_train, y_train)\n\n"
                    "# Plot partial dependence for top 2 features\n"
                    "fig, ax = plt.subplots(figsize=(10, 4))\n"
                    "PartialDependenceDisplay.from_estimator(\n"
                    "    model, X_train, features=[0, 1],\n"
                    "    feature_names=data.feature_names, ax=ax)\n"
                    "plt.tight_layout()\n"
                    "plt.savefig('pdp.png', dpi=80)\n"
                    "plt.close()\n"
                    "print('PDP saved to pdp.png')\n"
                    "print(f'Feature 0: {data.feature_names[0]}')\n"
                    "print(f'Feature 1: {data.feature_names[1]}')"
                )
            },
        ],
        "rw_scenario": "A mortgage lender must explain why a loan was denied. They use SHAP to generate a plain-English explanation of the top factors for each decision.",
        "rw_code": (
            "try:\n"
            "    import shap\n"
            "    import numpy as np\n"
            "    from sklearn.ensemble import GradientBoostingClassifier\n"
            "    from sklearn.model_selection import train_test_split\n\n"
            "    np.random.seed(42)\n"
            "    n = 500\n"
            "    feature_names = ['credit_score', 'income', 'debt_ratio', 'loan_amount', 'employment_years']\n"
            "    X = np.column_stack([\n"
            "        np.random.normal(680, 80, n),\n"
            "        np.random.lognormal(11, 0.5, n),\n"
            "        np.random.beta(2, 5, n),\n"
            "        np.random.lognormal(12, 0.3, n),\n"
            "        np.random.uniform(0, 30, n),\n"
            "    ])\n"
            "    y = (X[:, 0] > 700).astype(int) ^ (X[:, 2] > 0.4).astype(int)\n\n"
            "    X_train, X_test = train_test_split(X, random_state=42)\n"
            "    y_train, y_test = train_test_split(y, random_state=42)\n\n"
            "    model = GradientBoostingClassifier(n_estimators=100, random_state=42)\n"
            "    model.fit(X_train, y_train)\n\n"
            "    explainer = shap.TreeExplainer(model)\n"
            "    shap_vals = explainer.shap_values(X_test[:3])\n\n"
            "    for i, (sv, pred) in enumerate(zip(shap_vals, model.predict(X_test[:3]))):\n"
            "        decision = 'APPROVED' if pred == 1 else 'DENIED'\n"
            "        print(f'Application {i+1}: {decision}')\n"
            "        factors = sorted(zip(feature_names, sv), key=lambda x: abs(x[1]), reverse=True)[:3]\n"
            "        for feat, val in factors:\n"
            "            direction = 'increased' if val > 0 else 'decreased'\n"
            "            print(f'  {feat} {direction} approval chance by {abs(val):.4f}')\n"
            "        print()\n"
            "except ImportError:\n"
            "    print('pip install shap')"
        ),
        "practice": {
            "title": "Feature Importance Report",
            "desc": "Train a GradientBoostingClassifier on the iris dataset, compute permutation importance, and print a ranked table of features with their mean importance ± std.",
            "starter": (
                "from sklearn.ensemble import GradientBoostingClassifier\n"
                "from sklearn.inspection import permutation_importance\n"
                "from sklearn.datasets import load_iris\n"
                "from sklearn.model_selection import train_test_split\n"
                "import pandas as pd\n\n"
                "data = load_iris()\n"
                "X_train, X_test, y_train, y_test = train_test_split(\n"
                "    data.data, data.target, test_size=0.2, random_state=42)\n\n"
                "# TODO: train GradientBoostingClassifier\n"
                "# TODO: compute permutation_importance on X_test\n"
                "# TODO: create DataFrame with feature, importance, std\n"
                "# TODO: sort by importance descending and print"
            )
        }
    },
    {
        "title": "10. End-to-End ML Project Structure",
        "desc": "Organize a full ML project with proper structure, configuration management, reproducible training scripts, and a deployment-ready layout.",
        "examples": [
            {
                "label": "Standard ML project layout",
                "code": (
                    "PROJECT_STRUCTURE = '''\n"
                    "ml_project/\n"
                    "├── data/\n"
                    "│   ├── raw/          # Original, immutable data\n"
                    "│   ├── processed/    # Cleaned and feature-engineered data\n"
                    "│   └── external/     # Third-party data\n"
                    "├── notebooks/        # Jupyter notebooks for exploration\n"
                    "├── src/\n"
                    "│   ├── __init__.py\n"
                    "│   ├── data.py       # Data loading and preprocessing\n"
                    "│   ├── features.py   # Feature engineering\n"
                    "│   ├── train.py      # Model training\n"
                    "│   ├── evaluate.py   # Model evaluation\n"
                    "│   └── predict.py    # Inference functions\n"
                    "├── models/           # Saved model artifacts\n"
                    "├── tests/            # Unit and integration tests\n"
                    "├── api/\n"
                    "│   └── app.py        # FastAPI serving\n"
                    "├── config.yaml       # Configuration file\n"
                    "├── requirements.txt\n"
                    "├── Dockerfile\n"
                    "├── Makefile\n"
                    "└── README.md\n"
                    "'''\n"
                    "print(PROJECT_STRUCTURE)"
                )
            },
            {
                "label": "Configuration management with YAML",
                "code": (
                    "try:\n"
                    "    import yaml\n"
                    "    from dataclasses import dataclass\n\n"
                    "    CONFIG_YAML = '''\n"
                    "model:\n"
                    "  type: GradientBoostingClassifier\n"
                    "  params:\n"
                    "    n_estimators: 100\n"
                    "    max_depth: 5\n"
                    "    learning_rate: 0.1\n"
                    "    random_state: 42\n\n"
                    "data:\n"
                    "  train_path: data/processed/train.csv\n"
                    "  test_path:  data/processed/test.csv\n"
                    "  target_col: label\n"
                    "  test_size:  0.2\n\n"
                    "training:\n"
                    "  experiment_name: fraud-detection-v2\n"
                    "  cross_val_folds: 5\n"
                    "  metrics: [accuracy, f1_weighted, roc_auc]\n\n"
                    "serving:\n"
                    "  host: 0.0.0.0\n"
                    "  port: 8000\n"
                    "  model_path: models/best_model.joblib\n"
                    "'''\n\n"
                    "    config = yaml.safe_load(CONFIG_YAML)\n"
                    "    print('Model type:', config['model']['type'])\n"
                    "    print('n_estimators:', config['model']['params']['n_estimators'])\n"
                    "    print('Experiment:', config['training']['experiment_name'])\n"
                    "except ImportError:\n"
                    "    print('pip install pyyaml')"
                )
            },
            {
                "label": "Reproducible training script",
                "code": (
                    "# src/train.py pattern\n"
                    "TRAIN_SCRIPT = '''\n"
                    "import argparse, joblib, json, time, pathlib\n"
                    "from sklearn.ensemble import GradientBoostingClassifier\n"
                    "from sklearn.datasets import load_breast_cancer\n"
                    "from sklearn.model_selection import train_test_split, cross_val_score\n"
                    "from sklearn.metrics import classification_report\n\n"
                    "def parse_args():\n"
                    "    p = argparse.ArgumentParser()\n"
                    "    p.add_argument('--n-estimators', type=int, default=100)\n"
                    "    p.add_argument('--max-depth',    type=int, default=5)\n"
                    "    p.add_argument('--lr',           type=float, default=0.1)\n"
                    "    p.add_argument('--output-dir',   default='models')\n"
                    "    return p.parse_args()\n\n"
                    "def main():\n"
                    "    args = parse_args()\n"
                    "    X, y = load_breast_cancer(return_X_y=True)\n"
                    "    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n"
                    "    model = GradientBoostingClassifier(\n"
                    "        n_estimators=args.n_estimators, max_depth=args.max_depth,\n"
                    "        learning_rate=args.lr, random_state=42)\n"
                    "    model.fit(X_train, y_train)\n"
                    "    preds = model.predict(X_test)\n"
                    "    print(classification_report(y_test, preds))\n"
                    "    out = pathlib.Path(args.output_dir)\n"
                    "    out.mkdir(exist_ok=True)\n"
                    "    joblib.dump(model, out / 'model.joblib')\n"
                    "    print(f'Model saved to {out}/model.joblib')\n\n"
                    "if __name__ == \"__main__\":\n"
                    "    main()\n"
                    "'''\n"
                    "print(TRAIN_SCRIPT)"
                )
            },
            {
                "label": "Makefile for ML workflows",
                "code": (
                    "MAKEFILE = '''\n"
                    "# Makefile\n"
                    ".PHONY: install train test serve docker-build docker-run\n\n"
                    "install:\n"
                    "\\tpip install -r requirements.txt\n\n"
                    "train:\n"
                    "\\tpython src/train.py --n-estimators 100 --max-depth 5\n\n"
                    "validate:\n"
                    "\\tpython src/validate.py --model-path models/model.joblib\n\n"
                    "test:\n"
                    "\\tpytest tests/ -v --cov=src --cov-report=term-missing\n\n"
                    "serve:\n"
                    "\\tuvicorn api.app:app --host 0.0.0.0 --port 8000 --reload\n\n"
                    "docker-build:\n"
                    "\\tdocker build -t ml-api:latest .\n\n"
                    "docker-run:\n"
                    "\\tdocker run -p 8000:8000 ml-api:latest\n\n"
                    "clean:\n"
                    "\\tfind . -name __pycache__ -exec rm -rf {} + 2>/dev/null; true\n"
                    "\\trm -f models/*.joblib\n"
                    "'''\n"
                    "print(MAKEFILE)"
                )
            },
        ],
        "rw_scenario": "A team onboarding a new ML engineer needs a fully scaffolded project with training scripts, config files, tests, and a Makefile so they can reproduce results with one command.",
        "rw_code": (
            "import pathlib, json\n\n"
            "def scaffold_ml_project(name: str):\n"
            "    \"\"\"Generate a reproducible ML project skeleton.\"\"\"\n"
            "    root = pathlib.Path(name)\n"
            "    dirs = ['data/raw', 'data/processed', 'notebooks', 'src', 'models', 'tests', 'api']\n"
            "    for d in dirs:\n"
            "        (root / d).mkdir(parents=True, exist_ok=True)\n\n"
            "    files = {\n"
            "        'src/__init__.py': '',\n"
            "        'tests/__init__.py': '',\n"
            "        'requirements.txt': 'scikit-learn\\njoblib\\nfastapi\\nuvicorn\\nmlflow\\npyyaml\\npytest\\n',\n"
            "        'config.yaml': 'model:\\n  type: RandomForestClassifier\\n  params:\\n    n_estimators: 100\\n',\n"
            "        'src/train.py': '# Training script\\nif __name__ == \"__main__\":\\n    print(\"Train model here\")\\n',\n"
            "        'api/app.py': 'from fastapi import FastAPI\\napp = FastAPI()\\n@app.get(\"/health\")\\ndef health():\\n    return {\"status\": \"ok\"}\\n',\n"
            "        '.gitignore': '__pycache__/\\n*.joblib\\n.env\\nmlruns/\\n',\n"
            "    }\n"
            "    for fpath, content in files.items():\n"
            "        (root / fpath).write_text(content)\n\n"
            "    print(f'Project {name!r} scaffolded:')\n"
            "    for p in sorted(root.rglob('*')):\n"
            "        indent = '  ' * (len(p.relative_to(root).parts) - 1)\n"
            "        print(f'{indent}{p.name}{\"\" if p.is_file() else \"/\"}')\n\n"
            "scaffold_ml_project('my_ml_project')"
        ),
        "practice": {
            "title": "Project Scaffolder",
            "desc": "Extend the scaffold_ml_project function to also generate a Dockerfile, a Makefile with install/train/test/serve targets, and a src/evaluate.py stub.",
            "starter": (
                "import pathlib\n\n"
                "def scaffold_ml_project(name: str):\n"
                "    root = pathlib.Path(name)\n"
                "    dirs = ['data/raw', 'data/processed', 'src', 'tests', 'models', 'api']\n"
                "    for d in dirs:\n"
                "        (root / d).mkdir(parents=True, exist_ok=True)\n\n"
                "    # TODO: add Dockerfile content\n"
                "    # TODO: add Makefile with install/train/test/serve targets\n"
                "    # TODO: add src/evaluate.py with a validate() stub\n"
                "    # TODO: write all files and print the directory tree\n"
                "    pass\n\n"
                "scaffold_ml_project('demo_project')"
            )
        }
    },
    {
        "title": "11. Model Compression & Optimization",
        "desc": "Reduce model size and latency through quantization, pruning, knowledge distillation, and ONNX export for production deployment.",
        "examples": [
            {
                "label": "Post-training quantization concept",
                "code": "import numpy as np\n\n# Simulate 32-bit float weights -> 8-bit integer quantization\nnp.random.seed(42)\nweights_f32 = np.random.randn(64, 64).astype(np.float32)\n\ndef quantize_int8(tensor):\n    scale = (tensor.max() - tensor.min()) / 255\n    zero_point = int(-tensor.min() / scale)\n    q = np.clip(np.round(tensor / scale + zero_point), 0, 255).astype(np.uint8)\n    return q, scale, zero_point\n\ndef dequantize(q_tensor, scale, zero_point):\n    return scale * (q_tensor.astype(np.float32) - zero_point)\n\nq, scale, zp = quantize_int8(weights_f32)\nrecovered = dequantize(q, scale, zp)\n\nf32_bytes = weights_f32.nbytes\nint8_bytes = q.nbytes\nerr = np.abs(weights_f32 - recovered).mean()\n\nprint(f'Original (float32): {f32_bytes:,} bytes')\nprint(f'Quantized (int8):   {int8_bytes:,} bytes')\nprint(f'Compression ratio:  {f32_bytes/int8_bytes:.1f}x')\nprint(f'Mean absolute error: {err:.6f}')\nprint(f'Relative error:      {err/np.abs(weights_f32).mean():.2%}')"
            },
            {
                "label": "Weight pruning with magnitude threshold",
                "code": "import numpy as np\n\nnp.random.seed(0)\nweight_matrix = np.random.randn(128, 64)\n\ndef prune_weights(weights, sparsity=0.5):\n    \"\"\"Zero out smallest abs-value weights to achieve target sparsity.\"\"\"\n    flat   = np.abs(weights).flatten()\n    thresh = np.percentile(flat, sparsity * 100)\n    mask   = np.abs(weights) > thresh\n    pruned = weights * mask\n    actual_sparsity = 1 - mask.mean()\n    return pruned, mask, actual_sparsity\n\nfor target in [0.3, 0.5, 0.7, 0.9]:\n    pruned, mask, actual = prune_weights(weight_matrix, sparsity=target)\n    nnz      = mask.sum()\n    orig_err = np.linalg.norm(weight_matrix - pruned, 'fro')\n    print(f'Sparsity {target:.0%}: {nnz:,} non-zero, '\n          f'Frobenius error={orig_err:.3f}, '\n          f'Memory reduction={actual:.1%}')\n\nprint('\\nNote: sparse storage (CSR/COO) needed to realize memory savings.')\nprint('Effective with magnitude-based unstructured pruning + sparse matmul.')"
            },
            {
                "label": "Knowledge distillation: teacher -> student",
                "code": "import numpy as np\nfrom sklearn.datasets import make_classification\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\n\nnp.random.seed(42)\nX, y = make_classification(n_samples=2000, n_features=20, random_state=42)\nsplit = 1600\nX_tr, X_te = X[:split], X[split:]\ny_tr, y_te = y[:split], y[split:]\n\n# Teacher: large GBM\nteacher = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)\nteacher.fit(X_tr, y_tr)\nteacher_acc = accuracy_score(y_te, teacher.predict(X_te))\n\n# Soft labels (temperature scaling)\nsoft_labels = teacher.predict_proba(X_tr)[:, 1]\n# Binarize with threshold 0.5 (soft to hard for sklearn student)\nsoft_hard = (soft_labels > 0.5).astype(int)\n\n# Student: shallow decision tree trained on soft labels\nstudent_distill = DecisionTreeClassifier(max_depth=4, random_state=42)\nstudent_distill.fit(X_tr, soft_hard)\n\nstudent_direct = DecisionTreeClassifier(max_depth=4, random_state=42)\nstudent_direct.fit(X_tr, y_tr)\n\nprint(f'Teacher (GBM 100 trees): {teacher_acc:.3f}')\nprint(f'Student (distilled):     {accuracy_score(y_te, student_distill.predict(X_te)):.3f}')\nprint(f'Student (direct):        {accuracy_score(y_te, student_direct.predict(X_te)):.3f}')\nprint(f'\\nTeacher params: ~{100*5**5:,} nodes est.')\nprint(f'Student params: ~{2**4:,} leaves')"
            },
            {
                "label": "ONNX export and inference simulation",
                "code": "import numpy as np\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.datasets import make_classification\nimport json\n\nnp.random.seed(0)\nX, y = make_classification(n_samples=500, n_features=10, random_state=0)\nmodel = LogisticRegression(max_iter=200).fit(X, y)\n\n# Simulate ONNX export by serializing model parameters\ndef export_to_dict(model, feature_names=None):\n    return {\n        'type': 'LogisticRegression',\n        'coef': model.coef_.tolist(),\n        'intercept': model.intercept_.tolist(),\n        'classes': model.classes_.tolist(),\n        'n_features': model.n_features_in_,\n    }\n\ndef infer_from_dict(model_dict, X):\n    coef      = np.array(model_dict['coef'])\n    intercept = np.array(model_dict['intercept'])\n    logit = X @ coef.T + intercept\n    proba = 1 / (1 + np.exp(-logit))\n    return (proba > 0.5).astype(int).flatten()\n\nexported = export_to_dict(model)\nprint('Exported model (JSON):') ; print(json.dumps({k: str(v)[:40] for k, v in exported.items()}, indent=2))\npred_orig   = model.predict(X[:5])\npred_onnx   = infer_from_dict(exported, X[:5])\nprint(f'\\nOriginal predictions: {pred_orig}')\nprint(f'Simulated inference:  {pred_onnx}')\nprint(f'Match: {np.all(pred_orig == pred_onnx)}')"
            }
        ],
        "rw_scenario": "Deploy a fraud detection model to edge devices with 512MB RAM. The original XGBoost model is 80MB and takes 50ms per prediction. Apply pruning and quantization to reduce size to under 10MB with <10ms latency while maintaining >95% of original AUC.",
        "rw_code": "import numpy as np\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.datasets import make_classification\nfrom sklearn.metrics import roc_auc_score\nimport time\n\nnp.random.seed(1)\nX, y = make_classification(n_samples=5000, n_features=30, random_state=1)\nsplit = 4000\nX_tr, X_te = X[:split], X[split:]\ny_tr, y_te = y[:split], y[split:]\n\n# Teacher\nteacher = GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=1)\nteacher.fit(X_tr, y_tr)\nt0 = time.perf_counter()\nteacher_proba = teacher.predict_proba(X_te)[:,1]\nt_teacher = (time.perf_counter() - t0) * 1000\n\n# Student (distilled)\nsoft = (teacher.predict_proba(X_tr)[:,1] > 0.5).astype(int)\nstudent = DecisionTreeClassifier(max_depth=6, random_state=1).fit(X_tr, soft)\nt0 = time.perf_counter()\nstudent_proba = student.predict_proba(X_te)[:,1]\nt_student = (time.perf_counter() - t0) * 1000\n\nprint(f'Teacher AUC: {roc_auc_score(y_te, teacher_proba):.4f} | Time: {t_teacher:.1f}ms')\nprint(f'Student AUC: {roc_auc_score(y_te, student_proba):.4f} | Time: {t_student:.1f}ms')\nprint(f'Speed-up: {t_teacher/max(t_student,0.001):.1f}x')",
        "practice": {
            "title": "Benchmark Quantization Trade-offs",
            "desc": "Implement int4 quantization (4-bit) and int8 quantization for a random 256x256 weight matrix. For each, compute: compression ratio, mean absolute reconstruction error, and max error. Plot a bar chart comparing compression ratios. Discuss which is better for accuracy-sensitive vs memory-sensitive deployments.",
            "starter": (
                "import numpy as np\n\n"
                "np.random.seed(42)\n"
                "W = np.random.randn(256, 256).astype(np.float32)\n\n"
                "def quantize(tensor, bits):\n"
                "    # TODO: quantize to `bits`-bit unsigned integer\n"
                "    # levels = 2**bits\n"
                "    # Compute scale and zero_point, quantize, dequantize\n"
                "    pass\n\n"
                "for bits in [4, 8, 16]:\n"
                "    recovered, compression = quantize(W, bits)\n"
                "    # TODO: print bits, compression ratio, MAE, max error\n"
                "    pass\n"
            )
        }
    },
    {
        "title": "12. Feature Stores & Data Pipelines",
        "desc": "Design and implement feature stores, data versioning, and reproducible pipelines for consistent feature serving between training and inference.",
        "examples": [
            {
                "label": "In-memory feature store implementation",
                "code": "import pandas as pd\nimport numpy as np\nfrom datetime import datetime\nfrom typing import List\n\nclass FeatureStore:\n    def __init__(self):\n        self._store = {}  # entity_id -> {feature_name: (value, timestamp)}\n\n    def write(self, entity_id: str, features: dict, timestamp=None):\n        if timestamp is None:\n            timestamp = datetime.utcnow()\n        if entity_id not in self._store:\n            self._store[entity_id] = {}\n        for k, v in features.items():\n            self._store[entity_id][k] = (v, timestamp)\n\n    def read(self, entity_id: str, feature_names: List[str]) -> dict:\n        if entity_id not in self._store:\n            return {f: None for f in feature_names}\n        return {\n            f: self._store[entity_id].get(f, (None, None))[0]\n            for f in feature_names\n        }\n\n    def get_training_dataset(self, entities: List[str], features: List[str]) -> pd.DataFrame:\n        rows = [{'entity_id': eid, **self.read(eid, features)} for eid in entities]\n        return pd.DataFrame(rows)\n\n# Usage\nfs = FeatureStore()\nfor uid, feats in [\n    ('user_1', {'age': 28, 'spend_30d': 150.0, 'logins_7d': 5}),\n    ('user_2', {'age': 35, 'spend_30d': 400.0, 'logins_7d': 12}),\n    ('user_3', {'age': 22, 'spend_30d': 50.0,  'logins_7d': 1}),\n]:\n    fs.write(uid, feats)\n\ndf = fs.get_training_dataset(['user_1', 'user_2', 'user_3'], ['age', 'spend_30d', 'logins_7d'])\nprint(df.to_string(index=False))\nprint('\\nPoint lookup:', fs.read('user_2', ['spend_30d', 'logins_7d']))"
            },
            {
                "label": "Reproducible pipeline with pandas and hashing",
                "code": "import pandas as pd\nimport numpy as np\nimport hashlib, json\n\nclass ReproduciblePipeline:\n    def __init__(self, steps: list, params: dict):\n        self.steps  = steps\n        self.params = params\n        self._history = []\n\n    def run(self, df: pd.DataFrame) -> pd.DataFrame:\n        self._history = []\n        for name, fn in self.steps:\n            df = fn(df, self.params)\n            self._history.append({'step': name, 'rows': len(df), 'cols': list(df.columns)})\n        return df\n\n    def fingerprint(self) -> str:\n        blob = json.dumps({'params': self.params, 'steps': [s[0] for s in self.steps]}, sort_keys=True)\n        return hashlib.md5(blob.encode()).hexdigest()[:12]\n\n# Define pipeline steps\ndef drop_nulls(df, params): return df.dropna()\ndef filter_age(df, params): return df[df['age'] >= params['min_age']]\ndef add_feature(df, params): df = df.copy(); df['age_squared'] = df['age']**2; return df\n\nnp.random.seed(42)\ndf_raw = pd.DataFrame({'age': np.random.randint(16, 70, 100), 'spend': np.random.rand(100)*1000})\ndf_raw.loc[[5, 23, 67], 'age'] = np.nan\n\npipeline = ReproduciblePipeline(\n    steps=[('drop_nulls', drop_nulls), ('filter_age', filter_age), ('add_feature', add_feature)],\n    params={'min_age': 21}\n)\nresult = pipeline.run(df_raw)\nprint(f'Pipeline fingerprint: {pipeline.fingerprint()}')\nprint(f'Input rows: {len(df_raw)}, Output rows: {len(result)}')\nfor step in pipeline._history:\n    print(f'  After {step[\"step\"]}: {step[\"rows\"]} rows, {len(step[\"cols\"])} cols')"
            },
            {
                "label": "Data versioning with checksums",
                "code": "import pandas as pd\nimport numpy as np\nimport hashlib, json\nfrom datetime import datetime\n\nclass DataVersion:\n    registry = []\n\n    @classmethod\n    def snapshot(cls, df: pd.DataFrame, name: str, metadata: dict = None) -> str:\n        checksum = hashlib.md5(pd.util.hash_pandas_object(df).values.tobytes()).hexdigest()[:12]\n        version  = {'name': name, 'checksum': checksum, 'shape': df.shape,\n                    'timestamp': str(datetime.utcnow())[:19],\n                    'columns': list(df.columns), 'metadata': metadata or {}}\n        cls.registry.append(version)\n        return checksum\n\n    @classmethod\n    def show_lineage(cls):\n        for v in cls.registry:\n            print(f\"{v['timestamp']} | {v['name']:<20} | {str(v['shape']):<12} | cksum={v['checksum']}\")\n\nnp.random.seed(7)\ndf_v1 = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randint(0,2,100)})\nDataVersion.snapshot(df_v1, 'raw_data', {'source': 'sensor_A'})\n\ndf_v2 = df_v1.dropna()\nDataVersion.snapshot(df_v2, 'cleaned', {'action': 'dropna'})\n\ndf_v3 = df_v2.copy(); df_v3['x_scaled'] = (df_v3['x'] - df_v3['x'].mean()) / df_v3['x'].std()\nDataVersion.snapshot(df_v3, 'features_v1', {'scaler': 'standard'})\n\nDataVersion.show_lineage()"
            },
            {
                "label": "Train/serve skew detection",
                "code": "import numpy as np\nfrom scipy import stats\n\n# Detect distribution shift between training features and production features\nnp.random.seed(42)\n\n# Training distribution\ntrain_features = {\n    'age':     np.random.normal(35, 10, 1000),\n    'income':  np.random.lognormal(10, 0.5, 1000),\n    'score':   np.random.beta(2, 5, 1000),\n}\n\n# Production (simulated drift)\nprod_features = {\n    'age':    np.random.normal(35, 10, 500),    # same\n    'income': np.random.lognormal(10.3, 0.5, 500),  # shifted\n    'score':  np.random.beta(3, 3, 500),          # different shape\n}\n\nprint('Train/Serve Skew Detection (KS Test):')\nprint(f'{\"Feature\":<12} {\"KS stat\":>10} {\"p-value\":>10} {\"Drifted?\":>10}')\nprint('-' * 48)\nfor feat in train_features:\n    ks_stat, p_val = stats.ks_2samp(train_features[feat], prod_features[feat])\n    drifted = 'YES' if p_val < 0.05 else 'no'\n    print(f'{feat:<12} {ks_stat:>10.4f} {p_val:>10.4f} {drifted:>10}')"
            }
        ],
        "rw_scenario": "An ML team at a fintech company needs to ensure that the 30+ features used at training time are identical to those served at inference time. Build a feature registry that validates feature schemas, detects train/serve skew, and logs feature versions.",
        "rw_code": "import pandas as pd\nimport numpy as np\nfrom scipy import stats\n\nclass FeatureRegistry:\n    def __init__(self):\n        self._schemas  = {}   # name -> {'dtype', 'mean', 'std'}\n        self._versions = []\n\n    def register(self, name: str, series: pd.Series):\n        self._schemas[name] = {\n            'dtype': str(series.dtype),\n            'mean':  float(series.mean()),\n            'std':   float(series.std()),\n            'min':   float(series.min()),\n            'max':   float(series.max()),\n        }\n        self._versions.append({'name': name, 'n': len(series)})\n\n    def validate(self, name: str, series: pd.Series, alpha: float = 0.05):\n        if name not in self._schemas:\n            raise ValueError(f'Feature {name!r} not registered.')\n        ref = self._schemas[name]\n        issues = []\n        if str(series.dtype) != ref['dtype']:\n            issues.append(f'dtype mismatch: {series.dtype} vs {ref[\"dtype\"]}')\n        z = abs(series.mean() - ref['mean']) / max(ref['std'], 1e-6)\n        if z > 3:\n            issues.append(f'mean shift: z={z:.2f}')\n        return issues or ['OK']\n\nnp.random.seed(5)\nreg = FeatureRegistry()\nfor feat, vals in [('age', pd.Series(np.random.normal(35,10,1000))),\n                   ('income', pd.Series(np.random.lognormal(10,0.5,1000)))]:\n    reg.register(feat, vals)\n\n# Serve time validation\nprod_age    = pd.Series(np.random.normal(35, 10, 200))\nprod_income = pd.Series(np.random.lognormal(10.8, 0.5, 200))  # drifted\nprint('age validation:   ', reg.validate('age', prod_age))\nprint('income validation:', reg.validate('income', prod_income))",
        "practice": {
            "title": "Build a Feature Pipeline with Drift Monitoring",
            "desc": "Create a FeatureStore class that: (1) stores training feature distributions (mean, std, min, max), (2) at serve time detects distribution drift using Z-score on mean (threshold: |z| > 2), (3) logs a warning for drifted features. Test with 3 features where one has significant drift.",
            "starter": (
                "import numpy as np\nimport pandas as pd\n\n"
                "class MonitoredFeatureStore:\n"
                "    def __init__(self):\n"
                "        self.train_stats = {}  # feature -> {mean, std, min, max}\n\n"
                "    def fit(self, df: pd.DataFrame):\n"
                "        # TODO: compute and store stats for each column\n"
                "        pass\n\n"
                "    def validate(self, df: pd.DataFrame, z_threshold: float = 2.0) -> dict:\n"
                "        # TODO: compare serve-time stats to training stats\n"
                "        # Return dict: {feature: 'OK' or 'DRIFT (z=X.X)'}\n"
                "        pass\n\n"
                "np.random.seed(0)\n"
                "train = pd.DataFrame({'age': np.random.normal(30,8,1000), 'salary': np.random.normal(60000,10000,1000), 'score': np.random.beta(2,5,1000)})\n"
                "serve = pd.DataFrame({'age': np.random.normal(30,8,200),  'salary': np.random.normal(75000,10000,200),  'score': np.random.beta(2,5,200)})\n"
                "store = MonitoredFeatureStore()\n"
                "store.fit(train)\n"
                "print(store.validate(serve))\n"
            )
        }
    },
    {
        "title": "13. AutoML & Hyperparameter Optimization",
        "desc": "Automate model selection and hyperparameter tuning using grid search, random search, Bayesian optimization (Optuna), and automated feature engineering.",
        "examples": [
            {
                "label": "Grid search vs random search comparison",
                "code": "import numpy as np\nfrom sklearn.datasets import make_classification\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import GridSearchCV, RandomizedSearchCV\nfrom sklearn.metrics import f1_score\nimport time\n\nnp.random.seed(42)\nX, y = make_classification(n_samples=1000, n_features=20, random_state=42)\n\nparam_grid = {\n    'n_estimators': [50, 100, 200],\n    'max_depth':    [3, 5, 7, None],\n    'min_samples_split': [2, 5, 10],\n    'max_features': ['sqrt', 'log2'],\n}\n\n# Grid search: exhaustive\nt0 = time.perf_counter()\ngs = GridSearchCV(RandomForestClassifier(random_state=0), param_grid, cv=3, scoring='f1', n_jobs=-1)\ngs.fit(X, y)\ngrid_time = time.perf_counter() - t0\n\n# Random search: n_iter combinations\nt0 = time.perf_counter()\nrs = RandomizedSearchCV(RandomForestClassifier(random_state=0), param_grid, n_iter=10, cv=3, scoring='f1', n_jobs=-1, random_state=42)\nrs.fit(X, y)\nrand_time = time.perf_counter() - t0\n\nprint(f'Grid Search:   {gs.best_score_:.4f} | {3*4*3*2} combos | {grid_time:.1f}s')\nprint(f'Random Search: {rs.best_score_:.4f} | 10 combos  | {rand_time:.1f}s')\nprint(f'Speed-up: {grid_time/rand_time:.1f}x')\nprint(f'Best (random): {rs.best_params_}')"
            },
            {
                "label": "Bayesian optimization with Optuna",
                "code": "try:\n    import optuna\n    import numpy as np\n    from sklearn.datasets import make_classification\n    from sklearn.ensemble import GradientBoostingClassifier\n    from sklearn.model_selection import cross_val_score\n\n    optuna.logging.set_verbosity(optuna.logging.WARNING)\n    np.random.seed(42)\n    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)\n\n    def objective(trial):\n        n_est   = trial.suggest_int('n_estimators', 50, 300)\n        depth   = trial.suggest_int('max_depth', 2, 8)\n        lr      = trial.suggest_float('learning_rate', 0.01, 0.3, log=True)\n        subsamp = trial.suggest_float('subsample', 0.5, 1.0)\n        model   = GradientBoostingClassifier(n_estimators=n_est, max_depth=depth, learning_rate=lr, subsample=subsamp, random_state=0)\n        scores  = cross_val_score(model, X, y, cv=3, scoring='f1')\n        return scores.mean()\n\n    study = optuna.create_study(direction='maximize')\n    study.optimize(objective, n_trials=20)\n    print(f'Best F1:     {study.best_value:.4f}')\n    print(f'Best params: {study.best_params}')\n    print(f'Total trials: {len(study.trials)}')\nexcept ImportError:\n    print('pip install optuna')\n    print('Optuna uses Tree-structured Parzen Estimator (TPE) to model')\n    print('P(x|good) and P(x|bad) and samples from P(x|good) region.')"
            },
            {
                "label": "Automated feature engineering with polynomial features",
                "code": "import numpy as np\nfrom sklearn.datasets import make_regression\nfrom sklearn.preprocessing import PolynomialFeatures\nfrom sklearn.linear_model import Ridge\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.model_selection import cross_val_score\n\nnp.random.seed(42)\nX, y = make_regression(n_samples=500, n_features=5, noise=10, random_state=42)\n\nbest_score, best_degree = -np.inf, 1\nresults = []\nfor degree in [1, 2, 3]:\n    pipe = Pipeline([\n        ('poly', PolynomialFeatures(degree=degree, include_bias=False)),\n        ('ridge', Ridge(alpha=1.0))\n    ])\n    scores = cross_val_score(pipe, X, y, cv=5, scoring='r2')\n    results.append((degree, scores.mean(), pipe.named_steps['poly'].fit_transform(X).shape[1]))\n    if scores.mean() > best_score:\n        best_score, best_degree = scores.mean(), degree\n\nprint('Polynomial Feature Engineering Results:')\nprint(f'{\"Degree\":<10} {\"R2 (CV)\":<12} {\"Features\":<10}')\nfor deg, r2, n_feat in results:\n    star = ' <-- best' if deg == best_degree else ''\n    print(f'{deg:<10} {r2:<12.4f} {n_feat:<10}{star}')\nprint(f'\\nOriginal features: {X.shape[1]} -> Best: {results[best_degree-1][2]}')"
            },
            {
                "label": "Early stopping and learning curve analysis",
                "code": "import numpy as np\nfrom sklearn.datasets import make_classification\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import f1_score\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\nnp.random.seed(42)\nX, y = make_classification(n_samples=2000, n_features=20, random_state=42)\nX_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=42)\n\n# Train with staged prediction to simulate early stopping\ngbm = GradientBoostingClassifier(n_estimators=200, max_depth=3, learning_rate=0.05, random_state=0)\ngbm.fit(X_tr, y_tr)\n\ntrain_scores, val_scores = [], []\nfor y_pred_tr, y_pred_val in zip(\n    gbm.staged_predict(X_tr), gbm.staged_predict(X_val)\n):\n    train_scores.append(f1_score(y_tr, y_pred_tr))\n    val_scores.append(f1_score(y_val, y_pred_val))\n\nbest_iter = np.argmax(val_scores)\nprint(f'Best iteration: {best_iter+1} (val F1={val_scores[best_iter]:.4f})')\nprint(f'Final iteration val F1: {val_scores[-1]:.4f}')\nfig, ax = plt.subplots(figsize=(9, 4))\nax.plot(train_scores, label='Train')\nax.plot(val_scores, label='Validation')\nax.axvline(best_iter, color='red', linestyle='--', label=f'Best iter={best_iter+1}')\nax.set_xlabel('Boosting rounds'); ax.set_ylabel('F1 Score')\nax.set_title('Learning Curves + Early Stopping')\nax.legend(); plt.tight_layout()\nplt.savefig('learning_curves.png', dpi=80); plt.close(); print('Saved learning_curves.png')"
            }
        ],
        "rw_scenario": "An ML team wants to find the best model for a churn prediction task without manually tuning. Run Bayesian HPO over 3 model types (Logistic Regression, Random Forest, GBM) with 30 total Optuna trials. Return the best model, params, and cross-val AUC.",
        "rw_code": "import numpy as np\nfrom sklearn.datasets import make_classification\nfrom sklearn.model_selection import cross_val_score\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n\nnp.random.seed(0)\nX, y = make_classification(n_samples=2000, n_features=25, random_state=0)\n\n# Manual multi-model search (Optuna-style pseudocode)\nbest_score, best_config = -np.inf, None\nnp.random.seed(99)\nfor trial in range(30):\n    model_type = np.random.choice(['lr', 'rf', 'gbm'])\n    if model_type == 'lr':\n        C   = np.random.choice([0.01, 0.1, 1.0, 10.0])\n        clf = LogisticRegression(C=C, max_iter=200)\n        cfg = {'type': 'lr', 'C': C}\n    elif model_type == 'rf':\n        n   = np.random.choice([50, 100, 200])\n        d   = np.random.choice([3, 5, None])\n        clf = RandomForestClassifier(n_estimators=n, max_depth=d, random_state=0)\n        cfg = {'type': 'rf', 'n_estimators': n, 'max_depth': d}\n    else:\n        lr  = np.random.choice([0.05, 0.1, 0.2])\n        clf = GradientBoostingClassifier(learning_rate=lr, random_state=0)\n        cfg = {'type': 'gbm', 'lr': lr}\n    score = cross_val_score(clf, X, y, cv=3, scoring='roc_auc').mean()\n    if score > best_score:\n        best_score, best_config = score, cfg\n\nprint(f'Best AUC: {best_score:.4f}')\nprint(f'Best config: {best_config}')",
        "practice": {
            "title": "AutoML Model Selection with Optuna",
            "desc": "Using make_classification (1000 samples, 15 features), implement a 20-trial Optuna study that searches over: (1) model type (RF or GBM), (2) n_estimators (50-200), (3) max_depth (2-8), (4) learning_rate for GBM (0.01-0.3 log scale). Maximize 3-fold CV ROC-AUC. Report best trial and params.",
            "starter": (
                "import numpy as np\n"
                "from sklearn.datasets import make_classification\n"
                "from sklearn.model_selection import cross_val_score\n"
                "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n\n"
                "try:\n"
                "    import optuna; optuna.logging.set_verbosity(optuna.logging.WARNING)\nexcept ImportError:\n"
                "    print('pip install optuna'); exit()\n\n"
                "np.random.seed(42)\n"
                "X, y = make_classification(n_samples=1000, n_features=15, random_state=42)\n\n"
                "def objective(trial):\n"
                "    # TODO: suggest model_type (categorical: 'rf' or 'gbm')\n"
                "    # TODO: suggest n_estimators, max_depth\n"
                "    # TODO: if gbm, suggest learning_rate (log scale)\n"
                "    # TODO: return 3-fold CV ROC-AUC\n"
                "    pass\n\n"
                "study = optuna.create_study(direction='maximize')\n"
                "study.optimize(objective, n_trials=20)\n"
                "print('Best AUC:', study.best_value)\n"
                "print('Best params:', study.best_params)\n"
            )
        }
    },
    {
        "title": "14. Model Monitoring & Data Drift Detection",
        "examples": [
            {
                "label": "Data Drift Detection with Population Stability Index",
                "code": "import numpy as np\ndef psi(expected, actual, n_bins=10):\n    # Population Stability Index between two distributions.\n    bins = np.percentile(expected, np.linspace(0, 100, n_bins+1))\n    bins[0] -= 1e-6; bins[-1] += 1e-6\n    e_counts = np.histogram(expected, bins=bins)[0] / len(expected)\n    a_counts = np.histogram(actual,   bins=bins)[0] / len(actual)\n    e_counts = np.where(e_counts == 0, 1e-6, e_counts)\n    a_counts = np.where(a_counts == 0, 1e-6, a_counts)\n    psi_val = np.sum((a_counts - e_counts) * np.log(a_counts / e_counts))\n    return psi_val\nnp.random.seed(42)\nreference = np.random.normal(0, 1, 1000)\nstable    = np.random.normal(0.1, 1.0, 500)   # slight shift\ndrifted   = np.random.normal(1.5, 1.5, 500)   # significant drift\nprint(f\"PSI (stable):  {psi(reference, stable):.4f}  (<0.1: no drift)\")\nprint(f\"PSI (drifted): {psi(reference, drifted):.4f}  (>0.25: severe drift)\")"
            },
            {
                "label": "Model Performance Degradation Monitoring",
                "code": "import numpy as np\nfrom sklearn.metrics import accuracy_score\nnp.random.seed(1)\ndef simulate_batch(shift=0.0, n=200):\n    X = np.random.randn(n, 5) + shift\n    y_true = (X[:, 0] + X[:, 1] > shift).astype(int)\n    # Simulated model trained on no-shift data\n    y_pred = (X[:, 0] + X[:, 1] > 0).astype(int)\n    return accuracy_score(y_true, y_pred)\nprint(\"Model Monitoring Dashboard\")\nprint(f\"{\'Week\':<6} {\'Accuracy\':<10} {\'Status\'}\")\nprint(\"-\" * 30)\nbaseline_acc = simulate_batch(shift=0.0)\nfor week in range(1, 9):\n    shift = (week - 1) * 0.15\n    acc = simulate_batch(shift=shift)\n    delta = acc - baseline_acc\n    status = \"OK\" if abs(delta) < 0.05 else (\"WARN\" if abs(delta) < 0.10 else \"ALERT\")\n    print(f\"  {week:<4} {acc:.4f}    {status}\")"
            },
            {
                "label": "Kolmogorov-Smirnov Drift Test",
                "code": "import numpy as np\nfrom scipy import stats\nnp.random.seed(5)\n# Simulate feature distributions: train vs production batches\ntrain_dist  = np.random.normal(50, 10, 2000)\nprod_no_drift = np.random.normal(50.5, 10.2, 500)\nprod_drift    = np.random.normal(58.0, 12.0, 500)\nfeatures = {\n    \"no_drift_batch\": prod_no_drift,\n    \"drifted_batch\":  prod_drift,\n}\nfor name, prod in features.items():\n    ks_stat, p_val = stats.ks_2samp(train_dist, prod)\n    drift = \"DRIFT DETECTED\" if p_val < 0.05 else \"stable\"\n    print(f\"{name:<20}: KS={ks_stat:.4f}, p={p_val:.6f} -> {drift}\")"
            }
        ],
        "rw_scenario": "Deployed ML model for loan approval: monitor weekly for data drift in applicant features (income, credit score, age) using PSI, and alert the ML team when any feature shows PSI > 0.25.",
        "rw_code": "import numpy as np\ndef psi(ref, curr, n_bins=10):\n    bins = np.percentile(ref, np.linspace(0, 100, n_bins+1))\n    bins[0] -= 1e-6; bins[-1] += 1e-6\n    e = np.histogram(ref,  bins=bins)[0] / len(ref)\n    a = np.histogram(curr, bins=bins)[0] / len(curr)\n    e = np.where(e == 0, 1e-6, e)\n    a = np.where(a == 0, 1e-6, a)\n    return float(np.sum((a - e) * np.log(a / e)))\nnp.random.seed(99)\n# Training distribution\ntrain_income = np.random.lognormal(10.8, 0.4, 5000)\ntrain_credit = np.random.normal(680, 50, 5000)\ntrain_age    = np.random.normal(38, 12, 5000)\nprint(\"Loan Model Feature Drift Report\")\nprint(f\"{\'Feature\':<15} {\'PSI\':<8} {\'Status\'}\")\nprint(\"-\" * 35)\nweeks_drift = [0, 0.05, 0.12, 0.22, 0.35]  # progressive drift scenario\nfor week, drift in enumerate(weeks_drift, 1):\n    prod_income = np.random.lognormal(10.8 + drift, 0.4 + drift*0.1, 500)\n    prod_credit = np.random.normal(680 - drift*40, 50, 500)\n    prod_age    = np.random.normal(38 + drift*2, 12, 500)\n    results = {\n        \"income\": psi(train_income, prod_income),\n        \"credit_score\": psi(train_credit, prod_credit),\n        \"age\": psi(train_age, prod_age),\n    }\n    max_psi_feat = max(results, key=results.get)\n    max_psi = results[max_psi_feat]\n    status = \"ALERT\" if max_psi > 0.25 else (\"WARN\" if max_psi > 0.10 else \"OK\")\n    print(f\"Week {week}: {max_psi_feat:<12} PSI={max_psi:.3f}  [{status}]\")",
        "practice": {
            "title": "Multi-Feature Drift Dashboard",
            "desc": "For a churn prediction model with 6 features (age, tenure, monthly_spend, num_products, is_active, region_encoded), simulate 8 weekly production batches where drift gradually increases in tenure and monthly_spend starting at week 4. Compute PSI and KS-test for each feature each week. Build a summary table and flag weeks where total PSI > 0.5.",
            "starter": "import numpy as np\nfrom scipy import stats\ndef psi(ref, curr, n_bins=10):\n    bins = np.percentile(ref, np.linspace(0, 100, n_bins+1))\n    bins[0] -= 1e-6; bins[-1] += 1e-6\n    e = np.histogram(ref,  bins=bins)[0] / len(ref)\n    a = np.histogram(curr, bins=bins)[0] / len(curr)\n    e = np.where(e == 0, 1e-6, e)\n    a = np.where(a == 0, 1e-6, a)\n    return float(np.sum((a - e) * np.log(a / e)))\nnp.random.seed(7)\nn_train = 3000\nfeatures = {\n    \"age\":           np.random.normal(35, 10, n_train),\n    \"tenure\":        np.random.exponential(24, n_train),\n    \"monthly_spend\": np.random.lognormal(4.5, 0.5, n_train),\n    \"num_products\":  np.random.poisson(2.5, n_train).astype(float),\n    \"is_active\":     np.random.binomial(1, 0.7, n_train).astype(float),\n    \"region\":        np.random.randint(0, 5, n_train).astype(float),\n}\n# TODO: Generate 8 weekly batches of 300 samples (drift in tenure+spend from week 4)\n# TODO: Compute PSI and KS-test p-value for each feature each week\n# TODO: Flag weeks where total PSI > 0.5\n# TODO: Print formatted weekly report table\n"
        }
    },
    {
        "title": "15. Feature Stores & Data Engineering Pipelines",
        "examples": [
            {
                "label": "Feature Store Simulation with Feast-like API",
                "code": "import pandas as pd\nimport numpy as np\nfrom datetime import datetime, timedelta\nnp.random.seed(42)\n# Simulate a simple feature store\nclass SimpleFeatureStore:\n    def __init__(self):\n        self._store = {}\n    def ingest(self, entity_id, features, timestamp):\n        self._store[(entity_id, timestamp)] = features\n    def get_historical(self, entity_ids, feature_names, as_of=None):\n        results = []\n        for eid in entity_ids:\n            matching = {ts: feats for (e, ts), feats in self._store.items() if e == eid}\n            if not matching: continue\n            latest_ts = max(matching.keys())\n            feats = matching[latest_ts]\n            row = {\"entity_id\": eid, \"timestamp\": latest_ts}\n            row.update({k: feats.get(k) for k in feature_names})\n            results.append(row)\n        return pd.DataFrame(results)\nfs = SimpleFeatureStore()\n# Ingest user features\nfor user_id in range(1, 6):\n    fs.ingest(user_id, {\"age\": np.random.randint(20, 60),\n                        \"spend_30d\": round(np.random.uniform(50, 500), 2),\n                        \"logins_7d\": np.random.randint(1, 30)},\n              datetime.now() - timedelta(hours=np.random.randint(1, 48)))\nresult = fs.get_historical([1, 2, 3], [\"age\", \"spend_30d\", \"logins_7d\"])\nprint(result.to_string(index=False))"
            },
            {
                "label": "Data Pipeline with pandas + Validation",
                "code": "import pandas as pd\nimport numpy as np\nnp.random.seed(0)\n# Raw data ingestion with quality checks\ndef build_training_pipeline(df_raw):\n    report = {\"input_rows\": len(df_raw), \"issues\": []}\n    # Null check\n    null_pct = df_raw.isnull().mean()\n    for col, pct in null_pct.items():\n        if pct > 0.1:\n            report[\"issues\"].append(f\"{col}: {pct:.1%} nulls\")\n    # Range validation\n    if \"age\" in df_raw:\n        invalid = ((df_raw[\"age\"] < 0) | (df_raw[\"age\"] > 120)).sum()\n        if invalid: report[\"issues\"].append(f\"age: {invalid} out-of-range values\")\n    df = df_raw.dropna().copy()\n    df = df[(df[\"age\"].between(0, 120)) & (df[\"income\"] > 0)]\n    report[\"output_rows\"] = len(df)\n    report[\"drop_rate\"] = 1 - len(df)/len(df_raw)\n    return df, report\nraw = pd.DataFrame({\n    \"age\": np.random.choice([*np.random.randint(18,80,90), *[-1]*5, *[np.nan]*5], 100),\n    \"income\": np.random.choice([*np.random.lognormal(10,0.5,85), *[np.nan]*15], 100),\n})\nclean, report = build_training_pipeline(raw)\nprint(\"Pipeline Report:\", report)"
            },
            {
                "label": "Training Data Versioning (DVC-style)",
                "code": "import hashlib, json, os\nfrom datetime import datetime\nclass DataVersioner:\n    # Simple data versioning inspired by DVC.\n    def __init__(self, registry_path=\"data_registry.json\"):\n        self.registry_path = registry_path\n        self.registry = {}\n    def hash_data(self, data_str):\n        return hashlib.md5(data_str.encode()).hexdigest()[:12]\n    def register(self, name, data_str, metadata=None):\n        version_id = self.hash_data(data_str)\n        entry = {\n            \"name\": name, \"version\": version_id,\n            \"timestamp\": datetime.now().isoformat()[:19],\n            \"size_bytes\": len(data_str),\n            \"metadata\": metadata or {}\n        }\n        self.registry[version_id] = entry\n        print(f\"Registered: {name} v{version_id}\")\n        return version_id\n    def lineage(self, version_id):\n        entry = self.registry.get(version_id, {})\n        print(f\"Lineage for {version_id}: {json.dumps(entry, indent=2)}\")\ndv = DataVersioner()\nv1 = dv.register(\"train_features\", \"col1,col2\\n1,2\\n3,4\\n5,6\", {\"n_rows\": 3, \"split\": \"train\"})\nv2 = dv.register(\"train_features\", \"col1,col2\\n1,2\\n3,4\\n5,6\\n7,8\", {\"n_rows\": 4, \"split\": \"train\"})\ndv.lineage(v1)"
            }
        ],
        "rw_scenario": "Recommendation system: maintain a feature store with user engagement features (clicks_7d, purchase_30d, category_affinity) updated hourly, served to the model at inference time with <10ms latency.",
        "rw_code": "import pandas as pd\nimport numpy as np\nfrom datetime import datetime, timedelta\nnp.random.seed(42)\n# Simulate feature store for recommendation system\nclass RecoFeatureStore:\n    def __init__(self):\n        self.user_features = {}\n        self.item_features = {}\n    def update_user(self, user_id, features):\n        self.user_features[user_id] = {**features, \"updated_at\": datetime.now().isoformat()}\n    def update_item(self, item_id, features):\n        self.item_features[item_id] = {**features, \"updated_at\": datetime.now().isoformat()}\n    def get_feature_vector(self, user_id, item_id):\n        u = self.user_features.get(user_id, {})\n        i = self.item_features.get(item_id, {})\n        return {\n            \"user_clicks_7d\": u.get(\"clicks_7d\", 0),\n            \"user_purchase_30d\": u.get(\"purchase_30d\", 0),\n            \"item_avg_rating\": i.get(\"avg_rating\", 3.0),\n            \"item_purchase_count\": i.get(\"purchase_count\", 0),\n            \"affinity\": u.get(\"category_affinity\", {}).get(i.get(\"category\"), 0.0)\n        }\nfs = RecoFeatureStore()\n# Populate store\nfor uid in range(1, 6):\n    fs.update_user(uid, {\n        \"clicks_7d\": np.random.randint(5, 100),\n        \"purchase_30d\": np.random.randint(0, 10),\n        \"category_affinity\": {\"electronics\": np.random.uniform(0,1),\n                               \"books\": np.random.uniform(0,1)}\n    })\nfor iid in range(1, 4):\n    fs.update_item(iid, {\"avg_rating\": np.random.uniform(3,5),\n                          \"purchase_count\": np.random.randint(10,1000),\n                          \"category\": np.random.choice([\"electronics\",\"books\"])})\nprint(\"Feature vectors for serving:\")\nfor uid in [1, 2]:\n    for iid in [1, 2, 3]:\n        fv = fs.get_feature_vector(uid, iid)\n        print(f\"  user={uid}, item={iid}: {fv}\")",
        "practice": {
            "title": "ETL Pipeline with Schema Validation",
            "desc": "Build a data pipeline that: (1) generates synthetic raw customer data with intentional quality issues (nulls, wrong types, out-of-range values), (2) validates schema using pandas dtype checks and range assertions, (3) cleans and transforms, (4) logs each step with row counts, (5) outputs a data quality report with pass/fail for each check.",
            "starter": "import pandas as pd\nimport numpy as np\nnp.random.seed(33)\n# Generate raw data with issues\nn = 500\nraw = pd.DataFrame({\n    \"customer_id\": range(n),\n    \"age\": np.random.choice([*np.random.randint(18,80,460), *[-5]*20, *[np.nan]*20], n),\n    \"revenue\": np.random.choice([*np.random.lognormal(6,1,450), *[np.nan]*50], n),\n    \"segment\": np.random.choice([\"A\",\"B\",\"C\",\"INVALID\",None], n),\n    \"signup_date\": pd.date_range(\"2020-01-01\", periods=n, freq=\"D\")\n})\n# TODO: Schema validation (dtypes, ranges, allowed values)\n# TODO: Cleaning steps (impute/drop nulls, fix dtypes, filter invalid segments)\n# TODO: Log each step with before/after row counts\n# TODO: Output data quality report DataFrame\n"
        }
    },
    {
        "title": "16. A/B Testing & Canary Deployments for ML",
        "examples": [
            {
                "label": "A/B Test Significance Calculator",
                "code": "import numpy as np\nfrom scipy import stats\ndef ab_test(control_conv, control_n, treat_conv, treat_n, alpha=0.05):\n    # Two-proportion z-test for A/B testing.\n    p_c = control_conv / control_n\n    p_t = treat_conv  / treat_n\n    p_pool = (control_conv + treat_conv) / (control_n + treat_n)\n    se = np.sqrt(p_pool * (1-p_pool) * (1/control_n + 1/treat_n))\n    z = (p_t - p_c) / se\n    p_value = 2 * (1 - stats.norm.cdf(abs(z)))\n    ci = (p_t - p_c) + np.array([-1, 1]) * stats.norm.ppf(1-alpha/2) * se\n    lift = (p_t - p_c) / p_c\n    return {\"z\": z, \"p_value\": p_value, \"lift\": lift, \"ci_95\": ci,\n            \"significant\": p_value < alpha}\nresult = ab_test(control_conv=120, control_n=2000, treat_conv=155, treat_n=2000)\nprint(f\"Conversion: control={120/2000:.3f}, treat={155/2000:.3f}\")\nprint(f\"Lift: {result[\'lift\']:+.2%}\")\nprint(f\"p-value: {result[\'p_value\']:.4f}\")\nprint(f\"95% CI: [{result[\'ci_95\'][0]:.4f}, {result[\'ci_95\'][1]:.4f}]\")\nprint(f\"Significant: {result[\'significant\']}\")"
            },
            {
                "label": "Canary Deployment Traffic Routing",
                "code": "import numpy as np\nnp.random.seed(42)\nclass CanaryRouter:\n    def __init__(self, canary_pct=0.10):\n        self.canary_pct = canary_pct\n        self.metrics = {\"control\": [], \"canary\": []}\n    def route(self):\n        return \"canary\" if np.random.random() < self.canary_pct else \"control\"\n    def record(self, model, latency_ms, error=False):\n        self.metrics[model].append({\"latency\": latency_ms, \"error\": error})\n    def report(self):\n        for model, records in self.metrics.items():\n            latencies = [r[\"latency\"] for r in records]\n            errors = [r[\"error\"] for r in records]\n            print(f\"{model:<8}: n={len(records):4d}, avg_lat={np.mean(latencies):.1f}ms, \"\n                  f\"p99={np.percentile(latencies,99):.1f}ms, err_rate={np.mean(errors):.3f}\")\nrouter = CanaryRouter(canary_pct=0.10)\nfor _ in range(2000):\n    m = router.route()\n    lat = np.random.lognormal(3.5 if m==\"control\" else 3.3, 0.4)\n    err = np.random.random() < (0.02 if m==\"control\" else 0.025)\n    router.record(m, lat, err)\nrouter.report()"
            },
            {
                "label": "Multi-Armed Bandit for Continuous Optimization",
                "code": "import numpy as np\nnp.random.seed(7)\n# Thompson Sampling for online model selection\nclass ThompsonBandit:\n    def __init__(self, n_arms):\n        self.alpha = np.ones(n_arms)\n        self.beta  = np.ones(n_arms)\n    def select(self):\n        return np.argmax(np.random.beta(self.alpha, self.beta))\n    def update(self, arm, reward):\n        self.alpha[arm] += reward\n        self.beta[arm]  += (1 - reward)\n# 3 model versions with different true conversion rates\ntrue_rates = [0.05, 0.08, 0.06]\nbandit = ThompsonBandit(n_arms=3)\ncounts = np.zeros(3, dtype=int)\nrewards_total = 0\nfor t in range(5000):\n    arm = bandit.select()\n    reward = int(np.random.random() < true_rates[arm])\n    bandit.update(arm, reward)\n    counts[arm] += 1\n    rewards_total += reward\nprint(f\"Total conversions: {rewards_total} / 5000 = {rewards_total/5000:.4f}\")\nfor i in range(3):\n    print(f\"  Model {i+1} (true={true_rates[i]:.2f}): selected {counts[i]:4d} times ({counts[i]/5000:.1%})\")"
            }
        ],
        "rw_scenario": "ML-powered pricing engine: run A/B tests comparing new pricing model (15% canary) vs current model, with Thompson Sampling auto-routing more traffic to the better performer after statistical significance is reached.",
        "rw_code": "import numpy as np\nfrom scipy import stats\nnp.random.seed(21)\n# Combined: Canary + statistical testing + bandit\ntrue_revenue_control = 45.0   # $45 avg order value\ntrue_revenue_canary  = 47.5   # $47.5 with new pricing\nclass PricingExperiment:\n    def __init__(self, canary_pct=0.15):\n        self.canary_pct = canary_pct\n        self.control_revenues = []\n        self.canary_revenues  = []\n        self.alpha = np.array([1.0, 1.0])  # Thompson beta params\n        self.beta  = np.array([1.0, 1.0])\n    def route(self):\n        # Start as pure A/B, shift to bandit after significance\n        if len(self.control_revenues) < 200:\n            return \"canary\" if np.random.random() < self.canary_pct else \"control\"\n        return \"canary\" if np.argmax(np.random.beta(self.alpha, self.beta)) == 1 else \"control\"\n    def observe(self, model):\n        if model == \"control\":\n            rev = np.random.normal(true_revenue_control, 12)\n            self.control_revenues.append(rev)\n            self.alpha[0] += max(rev/100, 0); self.beta[0] += max(1-rev/100, 0)\n        else:\n            rev = np.random.normal(true_revenue_canary, 12)\n            self.canary_revenues.append(rev)\n            self.alpha[1] += max(rev/100, 0); self.beta[1] += max(1-rev/100, 0)\n    def check_significance(self):\n        if len(self.control_revenues) < 30 or len(self.canary_revenues) < 30:\n            return None\n        t, p = stats.ttest_ind(self.canary_revenues, self.control_revenues)\n        return p\nexp = PricingExperiment()\nfor i in range(3000):\n    m = exp.route()\n    exp.observe(m)\n    if i % 500 == 499:\n        p = exp.check_significance()\n        print(f\"t={i+1}: control=${np.mean(exp.control_revenues):.2f}, \"\n              f\"canary=${np.mean(exp.canary_revenues):.2f}, p={p:.4f}\")",
        "practice": {
            "title": "Online Experiment Platform",
            "desc": "Build a complete A/B testing framework that: (1) assigns users to control/treatment with hash-based deterministic routing, (2) collects metrics (conversion, revenue) per variant, (3) computes p-values and confidence intervals daily, (4) auto-declares a winner when p<0.05 and min_sample=500/arm, (5) logs results to a DataFrame. Simulate 10,000 user sessions over 14 days.",
            "starter": "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nnp.random.seed(55)\n# Experiment settings\nTRUE_CONV_CONTROL = 0.04\nTRUE_CONV_TREAT   = 0.048\nTRUE_REV_CONTROL  = 30.0\nTRUE_REV_TREAT    = 31.5\nMIN_SAMPLE = 500\ndef assign(user_id):\n    # Deterministic hash-based assignment\n    return \"treatment\" if hash(f\"exp1_{user_id}\") % 2 == 0 else \"control\"\n# TODO: Simulate 10,000 users over 14 days (approx 714/day)\n# TODO: Track conversion and revenue per variant per day\n# TODO: Daily significance check with two-proportion z-test\n# TODO: Auto-declare winner when p<0.05 and n>=500/arm\n# TODO: Log results to DataFrame with columns: day, n_control, n_treat, p_value, winner\n"
        }
    },{
        "title": "17. MLflow Experiment Tracking",
        "desc": "MLflow provides a unified platform to log parameters, metrics, and artifacts across ML experiments for reproducibility and comparison.",
        "examples": [
            {
        "label": "Basic MLflow Logging",
        "code": "import mlflow\nimport mlflow.sklearn\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\n\nX, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\nmlflow.set_experiment(\"iris_classification\")\n\nwith mlflow.start_run(run_name=\"rf_baseline\"):\n    n_estimators = 100\n    max_depth = 5\n    mlflow.log_param(\"n_estimators\", n_estimators)\n    mlflow.log_param(\"max_depth\", max_depth)\n\n    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)\n    model.fit(X_train, y_train)\n\n    acc = accuracy_score(y_test, model.predict(X_test))\n    mlflow.log_metric(\"accuracy\", acc)\n    mlflow.sklearn.log_model(model, \"model\")\n    print(f\"Run logged. Accuracy: {acc:.4f}\")\n"
            },
            {
        "label": "MLflow Autolog & Compare Runs",
        "code": "import mlflow\nimport mlflow.sklearn\nfrom sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier\nfrom sklearn.datasets import load_breast_cancer\nfrom sklearn.model_selection import train_test_split\n\nX, y = load_breast_cancer(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\nmlflow.set_experiment(\"breast_cancer_comparison\")\n\n# autolog captures all params/metrics automatically\nmlflow.sklearn.autolog()\n\nmodels = {\n    \"random_forest\": RandomForestClassifier(n_estimators=50, random_state=42),\n    \"gradient_boost\": GradientBoostingClassifier(n_estimators=50, random_state=42)\n}\n\nfor name, model in models.items():\n    with mlflow.start_run(run_name=name):\n        model.fit(X_train, y_train)\n        print(f\"{name}: {model.score(X_test, y_test):.4f}\")\n\n# Query runs\nruns = mlflow.search_runs(experiment_names=[\"breast_cancer_comparison\"])\nprint(runs[[\"run_id\", \"metrics.training_accuracy_score\"]].head())\n"
            }
        ],
        "rw_scenario": "Your team is training multiple ML models with different hyperparameters daily. You need to track experiments, compare results, and reproduce the best model.",
        "rw_code": "import mlflow, mlflow.sklearn\nfrom sklearn.svm import SVC\nfrom sklearn.datasets import load_wine\nfrom sklearn.model_selection import train_test_split, cross_val_score\nimport numpy as np\n\nX, y = load_wine(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\nmlflow.set_experiment(\"wine_svm_tuning\")\nmlflow.sklearn.autolog()\n\nfor C in [0.1, 1.0, 10.0]:\n    for kernel in [\"rbf\", \"linear\"]:\n        with mlflow.start_run(run_name=f\"svm_C{C}_{kernel}\"):\n            model = SVC(C=C, kernel=kernel)\n            cv_scores = cross_val_score(model, X_train, y_train, cv=5)\n            model.fit(X_train, y_train)\n            mlflow.log_param(\"C\", C)\n            mlflow.log_param(\"kernel\", kernel)\n            mlflow.log_metric(\"cv_mean\", np.mean(cv_scores))\n            mlflow.log_metric(\"cv_std\", np.std(cv_scores))\n            print(f\"C={C}, kernel={kernel}: CV={np.mean(cv_scores):.4f}±{np.std(cv_scores):.4f}\")\n\nbest = mlflow.search_runs(order_by=[\"metrics.cv_mean DESC\"]).iloc[0]\nprint(f\"Best run: {best[\'run_id\']}, CV={best[\'metrics.cv_mean\']:.4f}\")\n",
        "practice": {
            "title": "Log experiment parameters and metrics",
            "desc": "Use mlflow.start_run() to log params, metrics, and models for multiple hyperparameter combinations.",
            "starter": "import mlflow\nmlflow.set_experiment(\"practice\")\nwith mlflow.start_run():\n    mlflow.log_param(\"learning_rate\", 0.01)\n    mlflow.log_metric(\"loss\", 0.25)\n    print(\"Logged!\")\n"
        }
    },

    {
        "title": "18. Data Versioning with DVC",
        "desc": "DVC (Data Version Control) tracks datasets and model files alongside Git, enabling reproducible ML pipelines and dataset sharing.",
        "examples": [
            {
        "label": "DVC Pipeline Setup",
        "code": "# DVC workflow (run in terminal, shown as subprocess here)\nimport subprocess, os\n\n# Initialize DVC in a git repo\n# subprocess.run([\"dvc\", \"init\"])\n\n# Track a large dataset file\n# subprocess.run([\"dvc\", \"add\", \"data/train.csv\"])\n# This creates data/train.csv.dvc and adds data/train.csv to .gitignore\n\n# Configure remote storage\n# subprocess.run([\"dvc\", \"remote\", \"add\", \"-d\", \"myremote\", \"s3://my-bucket/dvc\"])\n\n# Push data to remote\n# subprocess.run([\"dvc\", \"push\"])\n\n# Pull data on another machine\n# subprocess.run([\"dvc\", \"pull\"])\n\n# DVC pipeline in dvc.yaml:\npipeline_yaml = (\n    \"stages:\n\"\n    \"  prepare:\n\"\n    \"    cmd: python prepare.py\n\"\n    \"    deps:\n\"\n    \"      - data/raw.csv\n\"\n    \"    outs:\n\"\n    \"      - data/processed.csv\n\"\n    \"  train:\n\"\n    \"    cmd: python train.py\n\"\n    \"    deps:\n\"\n    \"      - data/processed.csv\n\"\n    \"    outs:\n\"\n    \"      - models/model.pkl\n\"\n    \"    metrics:\n\"\n    \"      - metrics.json\n\"\n)\nprint(\"DVC pipeline structure:\")\nprint(pipeline_yaml)\n"
            },
            {
        "label": "Python DVC API",
        "code": "# Using DVC Python API for programmatic data management\n# pip install dvc dvc-s3\n\nimport json, hashlib\nfrom pathlib import Path\n\n# Simulate DVC-style hash tracking\ndef compute_md5(filepath):\n    h = hashlib.md5()\n    with open(filepath, \"rb\") as f:\n        h.update(f.read())\n    return h.hexdigest()\n\n# Example: track dataset versions manually\nimport pandas as pd\nimport numpy as np\n\n# Create sample datasets\ndf_v1 = pd.DataFrame(np.random.randn(1000, 5), columns=[f\"f{i}\" for i in range(5)])\ndf_v2 = pd.concat([df_v1, pd.DataFrame(np.random.randn(200, 5), columns=df_v1.columns)])\n\n# Save versions\ndf_v1.to_csv(\"/tmp/data_v1.csv\", index=False)\ndf_v2.to_csv(\"/tmp/data_v2.csv\", index=False)\n\n# Track metadata\nmeta = {\n    \"v1\": {\"rows\": len(df_v1), \"md5\": compute_md5(\"/tmp/data_v1.csv\")},\n    \"v2\": {\"rows\": len(df_v2), \"md5\": compute_md5(\"/tmp/data_v2.csv\")},\n}\nprint(json.dumps(meta, indent=2))\nprint(f\"Row delta v1→v2: +{meta[\'v2\'][\'rows\'] - meta[\'v1\'][\'rows\']}\")\n"
            }
        ],
        "rw_scenario": "Your ML team uses the same datasets but different preprocessing steps. You need reproducible pipelines where changing the data version automatically reruns downstream stages.",
        "rw_code": "# Simulate DVC-style pipeline tracking\nimport hashlib, json\nimport pandas as pd\nimport numpy as np\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\n\ndef md5(df):\n    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()\n\n# Stage 1: Raw data\nnp.random.seed(42)\nraw = pd.DataFrame({\"x1\": np.random.randn(500), \"x2\": np.random.randn(500),\n                     \"y\": np.random.randint(0, 2, 500)})\n\n# Stage 2: Preprocessing\nscaler = StandardScaler()\nX = scaler.fit_transform(raw[[\"x1\", \"x2\"]])\ny = raw[\"y\"]\n\n# Stage 3: Train\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\nmodel = LogisticRegression()\nmodel.fit(X_train, y_train)\nacc = accuracy_score(y_test, model.predict(X_test))\n\n# Log pipeline metadata\npipeline_state = {\n    \"raw_hash\": md5(raw),\n    \"n_samples\": len(raw),\n    \"accuracy\": round(acc, 4)\n}\nprint(json.dumps(pipeline_state, indent=2))\n",
        "practice": {
            "title": "Create reproducible data pipeline",
            "desc": "Track dataset hash, preprocessing steps, and metrics together to ensure pipeline reproducibility.",
            "starter": "import hashlib, pandas as pd, numpy as np\ndf = pd.DataFrame({\"x\": np.random.randn(100), \"y\": np.random.randint(0,2,100)})\nh = hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()\nprint(f\"Dataset hash: {h}, rows: {len(df)}\")\n"
        }
    },

    {
        "title": "19. Model Registry & Lifecycle Management",
        "desc": "A model registry tracks model versions, manages stage transitions (Staging → Production), and provides a central hub for model governance.",
        "examples": [
            {
        "label": "MLflow Model Registry",
        "code": "import mlflow\nimport mlflow.sklearn\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom mlflow.tracking import MlflowClient\n\nX, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\nmlflow.set_experiment(\"registry_demo\")\nmodel_name = \"IrisClassifier\"\n\nwith mlflow.start_run() as run:\n    model = RandomForestClassifier(n_estimators=100, random_state=42)\n    model.fit(X_train, y_train)\n    acc = model.score(X_test, y_test)\n    mlflow.log_metric(\"accuracy\", acc)\n    mlflow.sklearn.log_model(model, \"model\", registered_model_name=model_name)\n    run_id = run.info.run_id\n\nclient = MlflowClient()\n# Get latest version\nversions = client.get_latest_versions(model_name)\nfor v in versions:\n    print(f\"Version {v.version}: stage={v.current_stage}, acc={acc:.4f}\")\n    # Transition to staging\n    client.transition_model_version_stage(model_name, v.version, \"Staging\")\n    print(f\"Transitioned to Staging\")\n"
            },
            {
        "label": "Model Comparison & Promotion",
        "code": "import mlflow\nfrom mlflow.tracking import MlflowClient\nimport pandas as pd\n\nclient = MlflowClient()\n\n# Search for best model runs across experiments\ndef get_best_model(experiment_name, metric=\"accuracy\", higher_is_better=True):\n    order = f\"metrics.{metric} {\'DESC\' if higher_is_better else \'ASC\'}\"\n    runs = mlflow.search_runs(\n        experiment_names=[experiment_name],\n        order_by=[order],\n        max_results=5\n    )\n    if runs.empty:\n        print(f\"No runs found for {experiment_name}\")\n        return None\n\n    best = runs.iloc[0]\n    print(f\"Best run: {best[\'run_id\'][:8]}...\")\n    print(f\"  {metric}: {best.get(f\'metrics.{metric}\', \'N/A\')}\")\n    print(f\"  params: {dict((k.replace(\'params.\',\'\'), v) for k,v in best.items() if k.startswith(\'params.\'))}\")\n    return best\n\n# Simulate comparing runs\nprint(\"Searching for best model...\")\n# In practice: get_best_model(\"iris_classification\", \"accuracy\")\n\n# Mock comparison table\ncomparison = pd.DataFrame({\n    \"model\": [\"RandomForest\", \"GradientBoost\", \"SVM\"],\n    \"accuracy\": [0.9737, 0.9605, 0.9737],\n    \"train_time_s\": [2.1, 4.5, 0.3],\n    \"stage\": [\"Production\", \"Staging\", \"Archived\"]\n})\nprint(comparison.to_string(index=False))\n"
            }
        ],
        "rw_scenario": "Your company has 5 versions of a fraud detection model. You need to track which version is in production, roll back when performance degrades, and promote new versions through staging.",
        "rw_code": "import mlflow, mlflow.sklearn\nfrom mlflow.tracking import MlflowClient\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.datasets import load_breast_cancer\nfrom sklearn.model_selection import train_test_split\nimport numpy as np\n\nX, y = load_breast_cancer(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\nmodel_name = \"FraudDetector\"\nmlflow.set_experiment(\"fraud_detection_registry\")\n\n# Train multiple versions\nfor version_seed in [42, 123, 999]:\n    with mlflow.start_run(run_name=f\"v_seed{version_seed}\"):\n        np.random.seed(version_seed)\n        model = LogisticRegression(C=np.random.choice([0.1, 1.0, 10.0]), max_iter=1000)\n        model.fit(X_train, y_train)\n        acc = model.score(X_test, y_test)\n        mlflow.log_metric(\"accuracy\", acc)\n        mlflow.log_param(\"seed\", version_seed)\n        mlflow.sklearn.log_model(model, \"model\", registered_model_name=model_name)\n        print(f\"seed={version_seed}: accuracy={acc:.4f}\")\n\n# List all versions\nclient = MlflowClient()\nversions = client.search_model_versions(f\"name=\'{model_name}\'\")\nfor v in versions:\n    print(f\"Version {v.version}: {v.current_stage}\")\n",
        "practice": {
            "title": "Register and stage a model version",
            "desc": "Log a model with mlflow.sklearn.log_model using registered_model_name, then use MlflowClient to transition its stage.",
            "starter": "import mlflow, mlflow.sklearn\nfrom sklearn.dummy import DummyClassifier\nfrom sklearn.datasets import load_iris\nX, y = load_iris(return_X_y=True)\nwith mlflow.start_run():\n    m = DummyClassifier().fit(X, y)\n    mlflow.sklearn.log_model(m, \"model\", registered_model_name=\"DummyModel\")\nprint(\"Registered!\")\n"
        }
    },

    {
        "title": "20. Containerizing ML Models with Docker",
        "desc": "Docker packages ML models with all dependencies into portable containers, ensuring consistent environments from development to production.",
        "examples": [
            {
        "label": "Dockerfile for ML Model",
        "code": "# Example Dockerfile for a scikit-learn model API\ndockerfile_lines = [\n    \"FROM python:3.10-slim\",\n    \"WORKDIR /app\",\n    \"COPY requirements.txt .\",\n    \"RUN pip install --no-cache-dir -r requirements.txt\",\n    \"COPY model.pkl .\",\n    \"COPY app.py .\",\n    \"EXPOSE 8000\",\n    \"HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8000/health || exit 1\",\n    \'CMD [\"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\',\n]\nprint(\"Dockerfile:\")\nfor line in dockerfile_lines:\n    print(\"  \" + line)\n\n# FastAPI app.py content (as list to avoid nested triple-quotes)\napp_lines = [\n    \"import pickle, numpy as np\",\n    \"from fastapi import FastAPI\",\n    \"from pydantic import BaseModel\",\n    \"app = FastAPI()\",\n    \'model = pickle.load(open(\"model.pkl\", \"rb\"))\',\n    \"class Features(BaseModel):\",\n    \"    features: list[float]\",\n    \"@app.get(\'/health\')\",\n    \"def health(): return {\'status\': \'ok\'}\",\n    \"@app.post(\'/predict\')\",\n    \"def predict(data: Features):\",\n    \"    pred = model.predict([data.features])\",\n    \"    return {\'prediction\': int(pred[0])}\",\n]\nprint(\"\\napp.py:\")\nfor line in app_lines:\n    print(\"  \" + line)\n"
            },
            {
        "label": "Docker Multi-Stage Build & MLflow Docker",
        "code": "# Multi-stage Dockerfile for smaller images\nmultistage_lines = [\n    \"FROM python:3.10 AS builder\",\n    \"WORKDIR /build\",\n    \"COPY requirements.txt .\",\n    \"RUN pip install --user --no-cache-dir -r requirements.txt\",\n    \"FROM python:3.10-slim AS production\",\n    \"WORKDIR /app\",\n    \"COPY --from=builder /root/.local /root/.local\",\n    \"COPY . .\",\n    \"ENV PATH=/root/.local/bin:$PATH\",\n    \'CMD [\"python\", \"serve.py\"]\',\n]\nprint(\"Multi-stage Dockerfile:\")\nfor line in multistage_lines:\n    print(\"  \" + line)\n\n# MLflow built-in Docker packaging\nmlflow_cmds = [\n    \"# Build Docker image from MLflow model (no Dockerfile needed!)\",\n    \"mlflow models build-docker \\\\\",\n    \'    --model-uri \"models:/MyModel/Production\" \\\\\',\n    \'    --name \"my-ml-model:latest\"\',\n    \"docker run -p 8080:8080 my-ml-model:latest\",\n    \"curl -X POST http://localhost:8080/invocations \\\\\",\n    \'    -H \"Content-Type: application/json\" \\\\\',\n    \"    -d \\\'{\"instances\": [[5.1, 3.5, 1.4, 0.2]]}\\\'\",\n]\nprint(\"\\nMLflow Docker commands:\")\nfor cmd in mlflow_cmds:\n    print(\"  \" + cmd)\n"
            }
        ],
        "rw_scenario": "Your data science team develops models locally but deployment always breaks due to package version mismatches. You need to containerize the model so it runs identically everywhere.",
        "rw_code": "import pickle, json, os\nimport numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\n\n# Train and save a model\nX, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\nmodel = RandomForestClassifier(n_estimators=100, random_state=42)\nmodel.fit(X_train, y_train)\nacc = accuracy_score(y_test, model.predict(X_test))\n\n# Save model artifact\nmodel_path = \"/tmp/iris_model.pkl\"\nwith open(model_path, \"wb\") as f:\n    pickle.dump(model, f)\n\n# Generate deployment manifest\nmanifest = {\n    \"model\": \"RandomForestClassifier\",\n    \"version\": \"1.0.0\",\n    \"accuracy\": round(acc, 4),\n    \"features\": [\"sepal_length\", \"sepal_width\", \"petal_length\", \"petal_width\"],\n    \"classes\": [\"setosa\", \"versicolor\", \"virginica\"],\n    \"model_path\": model_path,\n    \"docker_image\": \"iris-classifier:1.0.0\",\n    \"port\": 8000\n}\nprint(json.dumps(manifest, indent=2))\n\n# Simulate container health check\ndef health_check(model_pkl_path):\n    with open(model_pkl_path, \"rb\") as f:\n        m = pickle.load(f)\n    test_input = np.array([[5.1, 3.5, 1.4, 0.2]])\n    pred = m.predict(test_input)\n    return {\"status\": \"healthy\", \"test_prediction\": int(pred[0])}\n\nprint(\"Health check:\", health_check(model_path))\n",
        "practice": {
            "title": "Create a deployment manifest for a model",
            "desc": "Save a trained model and generate a JSON manifest with model metadata and deployment configuration.",
            "starter": "import pickle, json\nfrom sklearn.dummy import DummyClassifier\nfrom sklearn.datasets import load_iris\nX, y = load_iris(return_X_y=True)\nm = DummyClassifier().fit(X, y)\nwith open(\"/tmp/model.pkl\", \"wb\") as f: pickle.dump(m, f)\nprint(json.dumps({\"model\": \"DummyClassifier\", \"port\": 8000}, indent=2))\n"
        }
    },

    {
        "title": "21. REST API Serving with FastAPI",
        "desc": "FastAPI provides a high-performance, async-ready framework for building ML model serving APIs with automatic validation and documentation.",
        "examples": [
            {
        "label": "Basic FastAPI Model Server",
        "code": "# FastAPI ML serving (run with: uvicorn app:app --reload)\n# app.py structure:\nfastapi_lines = [\n    \"from fastapi import FastAPI\",\n    \"from pydantic import BaseModel, validator\",\n    \"from typing import List, Optional\",\n    \"import time, pickle, numpy as np\",\n    \"\",\n    \"app = FastAPI(title=\'ML Model API\', version=\'1.0.0\')\",\n    \"model = None\",\n    \"\",\n    \"@app.on_event(\'startup\')\",\n    \"async def load_model():\",\n    \"    global model\",\n    \"    model = pickle.load(open(\'model.pkl\', \'rb\'))\",\n    \"\",\n    \"class PredictionRequest(BaseModel):\",\n    \"    features: List[float]\",\n    \"    model_version: Optional[str] = \'latest\'\",\n    \"\",\n    \"@app.post(\'/predict\')\",\n    \"async def predict(request: PredictionRequest):\",\n    \"    start = time.time()\",\n    \"    pred = model.predict([request.features])\",\n    \"    prob = model.predict_proba([request.features])\",\n    \"    latency = (time.time() - start) * 1000\",\n    \"    return {\'prediction\': int(pred[0]), \'probability\': prob[0].tolist(), \'latency_ms\': round(latency, 2)}\",\n    \"\",\n    \"@app.get(\'/health\')\",\n    \"async def health(): return {\'status\': \'ok\'}\",\n]\nprint(\"FastAPI app.py:\")\nfor line in fastapi_lines[:15]:\n    print(\"  \" + line)\nprint(\"  ...\")\n"
            },
            {
        "label": "Batch Prediction & Request Validation",
        "code": "# Batch prediction endpoint + middleware\nimport numpy as np, time\n\n# Simulate batch endpoint logic\ndef batch_predict(instances):\n    X = np.array(instances)\n    # predictions = model.predict(X)\n    predictions = [0] * len(X)  # mock\n    return {\"predictions\": predictions, \"count\": len(predictions)}\n\n# Test batch\nresult = batch_predict([[5.1,3.5,1.4,0.2],[6.7,3.0,5.2,2.3],[4.9,3.0,1.4,0.2]])\nprint(\"Batch result:\", result)\n\n# Middleware pattern (request logging)\nimport functools, logging\ndef log_middleware(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        duration = (time.time() - start) * 1000\n        logging.info(f\"{func.__name__} completed in {duration:.2f}ms\")\n        return result\n    return wrapper\n\n@log_middleware\ndef predict_single(features):\n    return {\"prediction\": 0, \"latency_ms\": 0.1}\n\nres = predict_single([5.1, 3.5, 1.4, 0.2])\nprint(\"Single prediction:\", res)\n\n# FastAPI batch endpoint structure (key lines)\nbatch_endpoint_code = [\n    \"class BatchRequest(BaseModel):\",\n    \"    instances: List[List[float]] = Field(..., min_items=1, max_items=1000)\",\n    \"@app.post(\'/predict/batch\')\",\n    \"async def batch_predict(request: BatchRequest):\",\n    \"    X = np.array(request.instances)\",\n    \"    predictions = model.predict(X)\",\n    \"    return {\'predictions\': predictions.tolist(), \'count\': len(predictions)}\",\n]\nprint(\"\\nBatch endpoint structure:\")\nfor line in batch_endpoint_code: print(\"  \" + line)\n"
            }
        ],
        "rw_scenario": "Your ML model needs to serve predictions via an API that can handle 1000 requests/second with <50ms latency, validate inputs, and return probabilities with predictions.",
        "rw_code": "# Simulate FastAPI prediction pipeline\nimport numpy as np\nimport pickle\nimport time\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\n\n# Train model\nX, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\nmodel = RandomForestClassifier(n_estimators=50, random_state=42)\nmodel.fit(X_train, y_train)\n\n# Simulate API prediction function\ndef predict_api(features: list) -> dict:\n    if len(features) != 4:\n        return {\"error\": f\"Expected 4 features, got {len(features)}\"}\n\n    start = time.time()\n    X = np.array([features])\n    pred = model.predict(X)\n    prob = model.predict_proba(X)\n    latency_ms = (time.time() - start) * 1000\n\n    return {\n        \"prediction\": int(pred[0]),\n        \"probability\": [round(p, 4) for p in prob[0]],\n        \"latency_ms\": round(latency_ms, 3)\n    }\n\n# Test single prediction\nresult = predict_api([5.1, 3.5, 1.4, 0.2])\nprint(\"Single prediction:\", result)\n\n# Simulate batch prediction\nbatch = [[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3], [4.9, 3.0, 1.4, 0.2]]\nstart = time.time()\nbatch_results = [predict_api(f) for f in batch]\ntotal_ms = (time.time() - start) * 1000\nprint(f\"Batch of {len(batch)}: {total_ms:.2f}ms total\")\nfor i, r in enumerate(batch_results):\n    print(f\"  [{i}] pred={r[\'prediction\']}, prob_max={max(r[\'probability\']):.4f}\")\n",
        "practice": {
            "title": "Build a prediction function that validates input",
            "desc": "Create a function that checks input length, runs prediction, and returns prediction + probabilities.",
            "starter": "import numpy as np\nfrom sklearn.dummy import DummyClassifier\nfrom sklearn.datasets import load_iris\nX, y = load_iris(return_X_y=True)\nmodel = DummyClassifier().fit(X, y)\ndef predict(features):\n    if len(features) != 4: return {\"error\": \"need 4 features\"}\n    pred = model.predict([features])\n    return {\"prediction\": int(pred[0])}\nprint(predict([5.1, 3.5, 1.4, 0.2]))\n"
        }
    },

    {
        "title": "22. Model Monitoring & Drift Detection",
        "desc": "Production ML models degrade over time due to data drift and concept drift. Monitoring detects these shifts before they cause silent failures.",
        "examples": [
            {
        "label": "Statistical Drift Detection",
        "code": "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nfrom sklearn.datasets import load_iris\n\n# Load reference (training) data\nX, y = load_iris(return_X_y=True)\nref_data = pd.DataFrame(X, columns=[\"sepal_l\", \"sepal_w\", \"petal_l\", \"petal_w\"])\n\n# Simulate production data with drift\nnp.random.seed(42)\n# Normal production (no drift)\nprod_normal = ref_data + np.random.normal(0, 0.05, ref_data.shape)\n\n# Drifted production (mean shift)\nprod_drift = ref_data + np.random.normal(0.5, 0.2, ref_data.shape)\n\ndef detect_drift_ks(reference, current, alpha=0.05):\n    # Kolmogorov-Smirnov test for distribution drift per feature\n    results = {}\n    for col in reference.columns:\n        stat, p_val = stats.ks_2samp(reference[col], current[col])\n        results[col] = {\n            \"ks_stat\": round(stat, 4),\n            \"p_value\": round(p_val, 4),\n            \"drift_detected\": p_val < alpha\n        }\n    return results\n\nprint(\"=== No Drift Scenario ===\")\nfor feat, res in detect_drift_ks(ref_data, prod_normal).items():\n    flag = \"DRIFT\" if res[\"drift_detected\"] else \"OK\"\n    print(f\"  {feat}: {flag} (p={res[\'p_value\']:.4f})\")\n\nprint(\"\\n=== Drift Scenario ===\")\nfor feat, res in detect_drift_ks(ref_data, prod_drift).items():\n    flag = \"DRIFT\" if res[\"drift_detected\"] else \"OK\"\n    print(f\"  {feat}: {flag} (p={res[\'p_value\']:.4f})\")\n"
            },
            {
        "label": "PSI & Model Performance Monitoring",
        "code": "import numpy as np\nimport pandas as pd\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\n\ndef psi(expected, actual, buckets=10):\n    # Population Stability Index: PSI > 0.2 = significant drift\n    def scale_range(arr, min_val, max_val):\n        arr = np.clip(arr, min_val, max_val)\n        return arr\n\n    min_val = min(expected.min(), actual.min())\n    max_val = max(expected.max(), actual.max())\n\n    breakpoints = np.linspace(min_val, max_val, buckets + 1)\n    expected_perc = np.histogram(expected, bins=breakpoints)[0] / len(expected) + 1e-10\n    actual_perc = np.histogram(actual, bins=breakpoints)[0] / len(actual) + 1e-10\n\n    psi_val = np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc))\n    return round(psi_val, 4)\n\n# Train model\nX, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, random_state=42)\nmodel = RandomForestClassifier(n_estimators=50, random_state=42).fit(X_train, y_train)\n\n# Reference predictions (training)\nref_probs = model.predict_proba(X_train)[:, 1]\n\n# Simulated production prediction scores\nprod_stable = model.predict_proba(X_test)[:, 1]\nprod_drifted = np.clip(prod_stable + np.random.normal(0.3, 0.1, len(prod_stable)), 0, 1)\n\nprint(f\"PSI (stable):  {psi(ref_probs, prod_stable):.4f}  {\'OK\' if psi(ref_probs, prod_stable) < 0.1 else \'DRIFT\'}\")\nprint(f\"PSI (drifted): {psi(ref_probs, prod_drifted):.4f}  {\'OK\' if psi(ref_probs, prod_drifted) < 0.1 else \'DRIFT\'}\")\nprint(\"\\nPSI thresholds: <0.1 = stable, 0.1-0.2 = slight change, >0.2 = significant drift\")\n"
            }
        ],
        "rw_scenario": "Your credit scoring model was accurate at launch but F1 dropped from 0.92 to 0.71 over 6 months. You need to detect data drift early and trigger retraining alerts.",
        "rw_code": "import numpy as np\nimport pandas as pd\nfrom scipy import stats\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import load_breast_cancer\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import f1_score\n\nX, y = load_breast_cancer(return_X_y=True)\nfeat_names = load_breast_cancer().feature_names\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\nmodel = RandomForestClassifier(n_estimators=100, random_state=42)\nmodel.fit(X_train, y_train)\nbaseline_f1 = f1_score(y_test, model.predict(X_test))\nprint(f\"Baseline F1: {baseline_f1:.4f}\")\n\n# Simulate monthly production windows with increasing drift\nmonths = 6\nresults = []\nfor month in range(1, months + 1):\n    drift_level = month * 0.1\n    X_prod = X_test + np.random.normal(drift_level, 0.05, X_test.shape)\n    y_prod = model.predict(X_prod)\n\n    # KS test on top 3 features\n    drift_counts = sum(\n        stats.ks_2samp(X_train[:, i], X_prod[:, i])[1] < 0.05\n        for i in range(3)\n    )\n\n    # If we had labels, compute F1\n    simulated_errors = (drift_level * np.random.randn(len(y_test))).astype(bool)\n    y_labels = np.where(simulated_errors, 1 - y_test, y_test)\n    f1 = f1_score(y_labels, model.predict(X_prod))\n\n    results.append({\"month\": month, \"f1\": round(f1, 4), \"drifted_features\": drift_counts})\n    alert = \"ALERT\" if f1 < baseline_f1 * 0.9 or drift_counts >= 2 else \"OK\"\n    print(f\"Month {month}: F1={f1:.4f}, drift_features={drift_counts} [{alert}]\")\n",
        "practice": {
            "title": "Implement KS drift detection",
            "desc": "Compare training and production data distributions using KS test and flag features with p-value < 0.05.",
            "starter": "import numpy as np\nfrom scipy import stats\nref = np.random.normal(0, 1, 1000)\nprod = np.random.normal(0.5, 1, 1000)  # drifted\nstat, p = stats.ks_2samp(ref, prod)\nprint(f\"KS stat={stat:.4f}, p={p:.4f}, drift={\'YES\' if p<0.05 else \'NO\'}\")\n"
        }
    },

    {
        "title": "23. CI/CD for ML Pipelines",
        "desc": "CI/CD for ML automates testing, validation, and deployment of models, ensuring quality gates before any model reaches production.",
        "examples": [
            {
        "label": "GitHub Actions ML Pipeline",
        "code": "# .github/workflows/ml_pipeline.yml structure\nyaml_lines = [\n    \"name: ML Pipeline CI/CD\",\n    \"on:\",\n    \"  push:\",\n    \"    branches: [main]\",\n    \"jobs:\",\n    \"  test-and-validate:\",\n    \"    runs-on: ubuntu-latest\",\n    \"    steps:\",\n    \"    - uses: actions/checkout@v3\",\n    \"    - name: Set up Python\",\n    \"      uses: actions/setup-python@v4\",\n    \"      with:\",\n    \"        python-version: \'3.10\'\",\n    \"    - name: Install dependencies\",\n    \"      run: pip install -r requirements.txt\",\n    \"    - name: Run unit tests\",\n    \"      run: pytest tests/ --cov=src\",\n    \"    - name: Train model\",\n    \"      run: python train.py\",\n    \"    - name: Evaluate model (quality gate)\",\n    \"      run: python evaluate.py --threshold 0.90\",\n    \"    - name: Build Docker image\",\n    \"      if: github.ref == \'refs/heads/main\'\",\n    \"      run: docker build -t my-model:latest .\",\n]\nprint(\".github/workflows/ml_pipeline.yml:\")\nfor line in yaml_lines:\n    print(\"  \" + line)\n"
            },
            {
        "label": "Model Quality Gates",
        "code": "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split, cross_val_score\nfrom sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score\nimport json, sys\n\ndef evaluate_model(model, X_train, X_test, y_train, y_test, thresholds):\n    # Quality gate: fail CI if model doesn\'t meet thresholds\n    model.fit(X_train, y_train)\n    y_pred = model.predict(X_test)\n    cv_scores = cross_val_score(model, X_train, y_train, cv=5)\n\n    metrics = {\n        \"accuracy\": round(accuracy_score(y_test, y_pred), 4),\n        \"f1_macro\": round(f1_score(y_test, y_pred, average=\"macro\"), 4),\n        \"cv_mean\": round(cv_scores.mean(), 4),\n        \"cv_std\": round(cv_scores.std(), 4),\n    }\n\n    passed = all(metrics.get(k, 0) >= v for k, v in thresholds.items())\n    return metrics, passed\n\n# Define quality gates\nTHRESHOLDS = {\"accuracy\": 0.90, \"f1_macro\": 0.88, \"cv_mean\": 0.89}\n\nX, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\nmodel = RandomForestClassifier(n_estimators=100, random_state=42)\n\nmetrics, passed = evaluate_model(model, X_train, X_test, y_train, y_test, THRESHOLDS)\nprint(json.dumps(metrics, indent=2))\nprint(f\"\\nQuality Gate: {\'PASSED ✓\' if passed else \'FAILED ✗\'}\")\nif not passed:\n    print(\"Failed thresholds:\", {k: v for k, v in THRESHOLDS.items() if metrics.get(k, 0) < v})\n    # sys.exit(1)  # Uncomment in real CI to fail the pipeline\n"
            }
        ],
        "rw_scenario": "Your team deploys new models manually, causing production incidents when untested code reaches users. You need automated testing, model quality gates, and staged deployment.",
        "rw_code": "import numpy as np\nfrom sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\nfrom sklearn.datasets import load_breast_cancer\nfrom sklearn.model_selection import train_test_split, cross_val_score\nfrom sklearn.metrics import f1_score\nimport json\n\nX, y = load_breast_cancer(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\nTHRESHOLDS = {\"accuracy\": 0.95, \"f1\": 0.94, \"cv_mean\": 0.94}\n\ndef ci_pipeline(model, model_name):\n    model.fit(X_train, y_train)\n    y_pred = model.predict(X_test)\n    cv = cross_val_score(model, X_train, y_train, cv=5)\n\n    metrics = {\n        \"model\": model_name,\n        \"accuracy\": round(model.score(X_test, y_test), 4),\n        \"f1\": round(f1_score(y_test, y_pred), 4),\n        \"cv_mean\": round(cv.mean(), 4),\n        \"cv_std\": round(cv.std(), 4),\n    }\n\n    failures = [k for k in [\"accuracy\", \"f1\", \"cv_mean\"] if metrics[k] < THRESHOLDS[k]]\n    metrics[\"status\"] = \"PASSED\" if not failures else f\"FAILED: {failures}\"\n    return metrics\n\nfor model, name in [\n    (RandomForestClassifier(n_estimators=100, random_state=42), \"RandomForest\"),\n    (GradientBoostingClassifier(n_estimators=50, random_state=42), \"GradientBoost\"),\n]:\n    result = ci_pipeline(model, name)\n    print(json.dumps(result, indent=2))\n",
        "practice": {
            "title": "Implement a model quality gate",
            "desc": "Write a function that evaluates a model against metric thresholds and returns pass/fail.",
            "starter": "from sklearn.dummy import DummyClassifier\nfrom sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nX, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y)\nm = DummyClassifier().fit(X_train, y_train)\nacc = m.score(X_test, y_test)\npassed = acc >= 0.30\nprint(f\"Accuracy={acc:.4f}, gate={\'PASSED\' if passed else \'FAILED\'}\")\n"
        }
    },

    {
        "title": "24. Feature Stores & ML Platforms",
        "desc": "Feature stores centralize, version, and serve ML features consistently across training and serving, eliminating training-serving skew.",
        "examples": [
            {
        "label": "Feature Store with Feast",
        "code": "# Feature store concepts using pandas (Feast-like workflow)\nimport pandas as pd\nimport numpy as np\nfrom datetime import datetime, timedelta\n\n# Simulate a feature store\nclass SimpleFeatureStore:\n    def __init__(self):\n        self._features = {}\n        self._entity_df = None\n\n    def ingest(self, feature_view_name, df, entity_col=\"entity_id\"):\n        # Register feature data\n        self._features[feature_view_name] = df.set_index(entity_col)\n        print(f\"Ingested \'{feature_view_name}\': {len(df)} rows, {len(df.columns)-1} features\")\n\n    def get_historical_features(self, entity_ids, feature_views):\n        # Retrieve features for training\n        dfs = [self._features[fv].loc[entity_ids] for fv in feature_views if fv in self._features]\n        return pd.concat(dfs, axis=1).reset_index()\n\n    def get_online_features(self, entity_id, feature_views):\n        # Low-latency single-entity lookup for serving\n        result = {\"entity_id\": entity_id}\n        for fv in feature_views:\n            if fv in self._features and entity_id in self._features[fv].index:\n                result.update(self._features[fv].loc[entity_id].to_dict())\n        return result\n\n# Setup\nstore = SimpleFeatureStore()\nnp.random.seed(42)\nn = 1000\n\n# User behavioral features\nuser_features = pd.DataFrame({\n    \"entity_id\": range(n),\n    \"avg_spend\": np.random.exponential(50, n),\n    \"days_active\": np.random.randint(1, 365, n),\n    \"n_transactions\": np.random.poisson(10, n),\n})\nstore.ingest(\"user_activity\", user_features)\n\n# User demographic features\nuser_demo = pd.DataFrame({\n    \"entity_id\": range(n),\n    \"age\": np.random.randint(18, 70, n),\n    \"credit_score\": np.random.randint(300, 850, n),\n})\nstore.ingest(\"user_demographics\", user_demo)\n\n# Historical features for training\ntrain_features = store.get_historical_features(\n    entity_ids=list(range(100)),\n    feature_views=[\"user_activity\", \"user_demographics\"]\n)\nprint(\"Training features shape:\", train_features.shape)\nprint(train_features.head(3).to_string())\n\n# Online features for serving\nonline = store.get_online_features(42, [\"user_activity\", \"user_demographics\"])\nprint(\"\\nOnline features for entity 42:\", online)\n"
            },
            {
        "label": "Training-Serving Skew Prevention",
        "code": "import pandas as pd\nimport numpy as np\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nimport pickle\n\n# Anti-pattern: inline preprocessing (causes training-serving skew)\ndef bad_preprocess(df):\n    df[\"feature_ratio\"] = df[\"f1\"] / (df[\"f2\"] + 1e-8)\n    df[\"log_f3\"] = np.log1p(df[\"f3\"])\n    return df[[\"feature_ratio\", \"log_f3\", \"f4\"]].values\n\n# Good pattern: encapsulate ALL preprocessing in a sklearn Pipeline\nfrom sklearn.base import BaseEstimator, TransformerMixin\n\nclass FeatureEngineer(BaseEstimator, TransformerMixin):\n    def fit(self, X, y=None): return self\n    def transform(self, X):\n        X = pd.DataFrame(X, columns=[\"f1\", \"f2\", \"f3\", \"f4\"])\n        return np.column_stack([\n            X[\"f1\"] / (X[\"f2\"] + 1e-8),   # ratio feature\n            np.log1p(X[\"f3\"]),              # log transform\n            X[\"f4\"]                          # passthrough\n        ])\n\n# Generate data\nnp.random.seed(42)\nn = 1000\nX = pd.DataFrame(np.abs(np.random.randn(n, 4)), columns=[\"f1\", \"f2\", \"f3\", \"f4\"])\ny = (X[\"f1\"] > X[\"f2\"]).astype(int)\nX_train, X_test, y_train, y_test = train_test_split(X.values, y, random_state=42)\n\n# Full pipeline: preprocessing + model\nfull_pipeline = Pipeline([\n    (\"engineer\", FeatureEngineer()),\n    (\"scaler\", StandardScaler()),\n    (\"model\", RandomForestClassifier(n_estimators=50, random_state=42))\n])\n\nfull_pipeline.fit(X_train, y_train)\nacc = full_pipeline.score(X_test, y_test)\nprint(f\"Pipeline accuracy: {acc:.4f}\")\n\n# Save entire pipeline (same logic used in training AND serving)\nwith open(\"/tmp/full_pipeline.pkl\", \"wb\") as f:\n    pickle.dump(full_pipeline, f)\n\n# Serving: load and predict (ZERO skew risk)\nwith open(\"/tmp/full_pipeline.pkl\", \"rb\") as f:\n    serving_pipeline = pickle.load(f)\n\npred = serving_pipeline.predict(X_test[:5])\nprint(\"Serving predictions:\", pred)\nprint(\"Training-serving skew: ELIMINATED (same pipeline object)\")\n"
            }
        ],
        "rw_scenario": "Your churn model uses 50 features computed differently during training (pandas) and serving (SQL). This training-serving skew causes 8% accuracy loss in production.",
        "rw_code": "import pandas as pd\nimport numpy as np\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import StandardScaler, FunctionTransformer\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import classification_report\nimport pickle\n\nnp.random.seed(42)\nn = 2000\n\n# Simulate customer churn features\ndf = pd.DataFrame({\n    \"tenure_months\": np.random.randint(1, 72, n),\n    \"monthly_charges\": np.random.uniform(20, 120, n),\n    \"total_charges\": np.random.uniform(20, 8000, n),\n    \"n_support_calls\": np.random.poisson(2, n),\n    \"last_login_days\": np.random.exponential(30, n),\n})\n\n# Target: churn if high charges + short tenure + many support calls\ndf[\"churn\"] = (\n    (df[\"monthly_charges\"] > 80) &\n    (df[\"tenure_months\"] < 12) |\n    (df[\"n_support_calls\"] > 4)\n).astype(int)\n\nX = df.drop(\"churn\", axis=1).values\ny = df[\"churn\"].values\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)\n\n# Feature engineering + model in one pipeline\ndef add_features(X):\n    X = np.copy(X)\n    # charge_per_month = total / tenure\n    charge_ratio = X[:, 2] / (X[:, 0] + 1)\n    # recency_support_interaction\n    recency_support = X[:, 3] * np.log1p(X[:, 4])\n    return np.column_stack([X, charge_ratio, recency_support])\n\npipeline = Pipeline([\n    (\"engineer\", FunctionTransformer(add_features)),\n    (\"scaler\", StandardScaler()),\n    (\"model\", GradientBoostingClassifier(n_estimators=100, random_state=42))\n])\n\npipeline.fit(X_train, y_train)\nprint(\"Churn model pipeline accuracy:\", round(pipeline.score(X_test, y_test), 4))\nprint(classification_report(y_test, pipeline.predict(X_test)))\n\n# Single-entity serving prediction\ncustomer = np.array([[24, 95.0, 2500.0, 3, 45.0]])\npred = pipeline.predict(customer)\nprob = pipeline.predict_proba(customer)\nprint(f\"Customer churn prediction: {\'CHURN\' if pred[0] else \'RETAIN\'} (prob={prob[0][1]:.4f})\")\n",
        "practice": {
            "title": "Build a feature engineering pipeline",
            "desc": "Use sklearn Pipeline with FunctionTransformer for feature engineering to prevent training-serving skew.",
            "starter": "import numpy as np\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import FunctionTransformer, StandardScaler\nfrom sklearn.dummy import DummyClassifier\n\ndef add_feat(X): return np.column_stack([X, X[:, 0] / (X[:, 1] + 1)])\npipe = Pipeline([(\"eng\", FunctionTransformer(add_feat)), (\"sc\", StandardScaler()), (\"m\", DummyClassifier())])\nX = np.random.randn(100, 3); y = np.random.randint(0, 2, 100)\npipe.fit(X, y)\nprint(\"Pipeline works:\", pipe.predict(X[:3]))\n"
        }
    },

    
]

if __name__ == "__main__":
    html_out = BASE / "index.html"
    nb_out   = BASE / "study_guide.ipynb"
    html_out.write_text(make_html(SECTIONS), encoding="utf-8")
    nb_out.write_text(json.dumps(make_nb(SECTIONS), indent=1), encoding="utf-8")
    nb_cells = len(make_nb(SECTIONS)["cells"])
    print(f"MLOps guide created: {BASE}")
    print(f"  index.html:        {html_out.stat().st_size/1024:.1f} KB")
    print(f"  study_guide.ipynb: {nb_cells} cells")
