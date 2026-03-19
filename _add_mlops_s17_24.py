"""Add sections 17-24 to gen_mlops.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _inserter import insert_sections

FILE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_mlops.py"
MARKER = "\n]\n\nif __name__"

def ec(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("'", "\\'")

def make_ex(label, code):
    return f'            {{\n        "label": "{ec(label)}",\n        "code": "{ec(code)}"\n            }}'

def make_s(num, title, desc, examples, rw_scenario, rw_code, pt, pd_text, ps):
    ex_block = ",\n".join(make_ex(l, c) for l, c in examples)
    return (
        f'{{\n'
        f'        "title": "{num}. {title}",\n'
        f'        "desc": "{ec(desc)}",\n'
        f'        "examples": [\n{ex_block}\n        ],\n'
        f'        "rw_scenario": "{ec(rw_scenario)}",\n'
        f'        "rw_code": "{ec(rw_code)}",\n'
        f'        "practice": {{\n'
        f'            "title": "{ec(pt)}",\n'
        f'            "desc": "{ec(pd_text)}",\n'
        f'            "solution": "{ec(ps)}"\n'
        f'        }}\n'
        f'    }},\n\n    '
    )

# ── Section 17: MLflow Experiment Tracking ────────────────────────────────────
s17 = make_s(
    17, "MLflow Experiment Tracking",
    "MLflow provides a unified platform to log parameters, metrics, and artifacts across ML experiments for reproducibility and comparison.",
    [
        ("Basic MLflow Logging", """\
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

mlflow.set_experiment("iris_classification")

with mlflow.start_run(run_name="rf_baseline"):
    n_estimators = 100
    max_depth = 5
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")
    print(f"Run logged. Accuracy: {acc:.4f}")
"""),
        ("MLflow Autolog & Compare Runs", """\
import mlflow
import mlflow.sklearn
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

mlflow.set_experiment("breast_cancer_comparison")

# autolog captures all params/metrics automatically
mlflow.sklearn.autolog()

models = {
    "random_forest": RandomForestClassifier(n_estimators=50, random_state=42),
    "gradient_boost": GradientBoostingClassifier(n_estimators=50, random_state=42)
}

for name, model in models.items():
    with mlflow.start_run(run_name=name):
        model.fit(X_train, y_train)
        print(f"{name}: {model.score(X_test, y_test):.4f}")

# Query runs
runs = mlflow.search_runs(experiment_names=["breast_cancer_comparison"])
print(runs[["run_id", "metrics.training_accuracy_score"]].head())
"""),
    ],
    "Your team is training multiple ML models with different hyperparameters daily. You need to track experiments, compare results, and reproduce the best model.",
    """\
import mlflow, mlflow.sklearn
from sklearn.svm import SVC
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

mlflow.set_experiment("wine_svm_tuning")
mlflow.sklearn.autolog()

for C in [0.1, 1.0, 10.0]:
    for kernel in ["rbf", "linear"]:
        with mlflow.start_run(run_name=f"svm_C{C}_{kernel}"):
            model = SVC(C=C, kernel=kernel)
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            model.fit(X_train, y_train)
            mlflow.log_param("C", C)
            mlflow.log_param("kernel", kernel)
            mlflow.log_metric("cv_mean", np.mean(cv_scores))
            mlflow.log_metric("cv_std", np.std(cv_scores))
            print(f"C={C}, kernel={kernel}: CV={np.mean(cv_scores):.4f}±{np.std(cv_scores):.4f}")

best = mlflow.search_runs(order_by=["metrics.cv_mean DESC"]).iloc[0]
print(f"Best run: {best['run_id']}, CV={best['metrics.cv_mean']:.4f}")
""",
    "Log experiment parameters and metrics",
    "Use mlflow.start_run() to log params, metrics, and models for multiple hyperparameter combinations.",
    """\
import mlflow
mlflow.set_experiment("practice")
with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("loss", 0.25)
    print("Logged!")
"""
)

# ── Section 18: Data Versioning with DVC ──────────────────────────────────────
s18 = make_s(
    18, "Data Versioning with DVC",
    "DVC (Data Version Control) tracks datasets and model files alongside Git, enabling reproducible ML pipelines and dataset sharing.",
    [
        ("DVC Pipeline Setup", """\
# DVC workflow (run in terminal, shown as subprocess here)
import subprocess, os

# Initialize DVC in a git repo
# subprocess.run(["dvc", "init"])

# Track a large dataset file
# subprocess.run(["dvc", "add", "data/train.csv"])
# This creates data/train.csv.dvc and adds data/train.csv to .gitignore

# Configure remote storage
# subprocess.run(["dvc", "remote", "add", "-d", "myremote", "s3://my-bucket/dvc"])

# Push data to remote
# subprocess.run(["dvc", "push"])

# Pull data on another machine
# subprocess.run(["dvc", "pull"])

# DVC pipeline in dvc.yaml:
pipeline_yaml = (
    "stages:\n"
    "  prepare:\n"
    "    cmd: python prepare.py\n"
    "    deps:\n"
    "      - data/raw.csv\n"
    "    outs:\n"
    "      - data/processed.csv\n"
    "  train:\n"
    "    cmd: python train.py\n"
    "    deps:\n"
    "      - data/processed.csv\n"
    "    outs:\n"
    "      - models/model.pkl\n"
    "    metrics:\n"
    "      - metrics.json\n"
)
print("DVC pipeline structure:")
print(pipeline_yaml)
"""),
        ("Python DVC API", """\
# Using DVC Python API for programmatic data management
# pip install dvc dvc-s3

import json, hashlib
from pathlib import Path

# Simulate DVC-style hash tracking
def compute_md5(filepath):
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

# Example: track dataset versions manually
import pandas as pd
import numpy as np

# Create sample datasets
df_v1 = pd.DataFrame(np.random.randn(1000, 5), columns=[f"f{i}" for i in range(5)])
df_v2 = pd.concat([df_v1, pd.DataFrame(np.random.randn(200, 5), columns=df_v1.columns)])

# Save versions
df_v1.to_csv("/tmp/data_v1.csv", index=False)
df_v2.to_csv("/tmp/data_v2.csv", index=False)

# Track metadata
meta = {
    "v1": {"rows": len(df_v1), "md5": compute_md5("/tmp/data_v1.csv")},
    "v2": {"rows": len(df_v2), "md5": compute_md5("/tmp/data_v2.csv")},
}
print(json.dumps(meta, indent=2))
print(f"Row delta v1→v2: +{meta['v2']['rows'] - meta['v1']['rows']}")
"""),
    ],
    "Your ML team uses the same datasets but different preprocessing steps. You need reproducible pipelines where changing the data version automatically reruns downstream stages.",
    """\
# Simulate DVC-style pipeline tracking
import hashlib, json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def md5(df):
    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()

# Stage 1: Raw data
np.random.seed(42)
raw = pd.DataFrame({"x1": np.random.randn(500), "x2": np.random.randn(500),
                     "y": np.random.randint(0, 2, 500)})

# Stage 2: Preprocessing
scaler = StandardScaler()
X = scaler.fit_transform(raw[["x1", "x2"]])
y = raw["y"]

# Stage 3: Train
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)
acc = accuracy_score(y_test, model.predict(X_test))

# Log pipeline metadata
pipeline_state = {
    "raw_hash": md5(raw),
    "n_samples": len(raw),
    "accuracy": round(acc, 4)
}
print(json.dumps(pipeline_state, indent=2))
""",
    "Create reproducible data pipeline",
    "Track dataset hash, preprocessing steps, and metrics together to ensure pipeline reproducibility.",
    """\
import hashlib, pandas as pd, numpy as np
df = pd.DataFrame({"x": np.random.randn(100), "y": np.random.randint(0,2,100)})
h = hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()
print(f"Dataset hash: {h}, rows: {len(df)}")
"""
)

# ── Section 19: Model Registry & Lifecycle Management ─────────────────────────
s19 = make_s(
    19, "Model Registry & Lifecycle Management",
    "A model registry tracks model versions, manages stage transitions (Staging → Production), and provides a central hub for model governance.",
    [
        ("MLflow Model Registry", """\
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from mlflow.tracking import MlflowClient

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

mlflow.set_experiment("registry_demo")
model_name = "IrisClassifier"

with mlflow.start_run() as run:
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model", registered_model_name=model_name)
    run_id = run.info.run_id

client = MlflowClient()
# Get latest version
versions = client.get_latest_versions(model_name)
for v in versions:
    print(f"Version {v.version}: stage={v.current_stage}, acc={acc:.4f}")
    # Transition to staging
    client.transition_model_version_stage(model_name, v.version, "Staging")
    print(f"Transitioned to Staging")
"""),
        ("Model Comparison & Promotion", """\
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd

client = MlflowClient()

# Search for best model runs across experiments
def get_best_model(experiment_name, metric="accuracy", higher_is_better=True):
    order = f"metrics.{metric} {'DESC' if higher_is_better else 'ASC'}"
    runs = mlflow.search_runs(
        experiment_names=[experiment_name],
        order_by=[order],
        max_results=5
    )
    if runs.empty:
        print(f"No runs found for {experiment_name}")
        return None

    best = runs.iloc[0]
    print(f"Best run: {best['run_id'][:8]}...")
    print(f"  {metric}: {best.get(f'metrics.{metric}', 'N/A')}")
    print(f"  params: {dict((k.replace('params.',''), v) for k,v in best.items() if k.startswith('params.'))}")
    return best

# Simulate comparing runs
print("Searching for best model...")
# In practice: get_best_model("iris_classification", "accuracy")

# Mock comparison table
comparison = pd.DataFrame({
    "model": ["RandomForest", "GradientBoost", "SVM"],
    "accuracy": [0.9737, 0.9605, 0.9737],
    "train_time_s": [2.1, 4.5, 0.3],
    "stage": ["Production", "Staging", "Archived"]
})
print(comparison.to_string(index=False))
"""),
    ],
    "Your company has 5 versions of a fraud detection model. You need to track which version is in production, roll back when performance degrades, and promote new versions through staging.",
    """\
import mlflow, mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import numpy as np

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

model_name = "FraudDetector"
mlflow.set_experiment("fraud_detection_registry")

# Train multiple versions
for version_seed in [42, 123, 999]:
    with mlflow.start_run(run_name=f"v_seed{version_seed}"):
        np.random.seed(version_seed)
        model = LogisticRegression(C=np.random.choice([0.1, 1.0, 10.0]), max_iter=1000)
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_param("seed", version_seed)
        mlflow.sklearn.log_model(model, "model", registered_model_name=model_name)
        print(f"seed={version_seed}: accuracy={acc:.4f}")

# List all versions
client = MlflowClient()
versions = client.search_model_versions(f"name='{model_name}'")
for v in versions:
    print(f"Version {v.version}: {v.current_stage}")
""",
    "Register and stage a model version",
    "Log a model with mlflow.sklearn.log_model using registered_model_name, then use MlflowClient to transition its stage.",
    """\
import mlflow, mlflow.sklearn
from sklearn.dummy import DummyClassifier
from sklearn.datasets import load_iris
X, y = load_iris(return_X_y=True)
with mlflow.start_run():
    m = DummyClassifier().fit(X, y)
    mlflow.sklearn.log_model(m, "model", registered_model_name="DummyModel")
print("Registered!")
"""
)

# ── Section 20: Containerizing ML Models with Docker ──────────────────────────
s20 = make_s(
    20, "Containerizing ML Models with Docker",
    "Docker packages ML models with all dependencies into portable containers, ensuring consistent environments from development to production.",
    [
        ("Dockerfile for ML Model", """\
# Example Dockerfile for a scikit-learn model API
dockerfile_lines = [
    "FROM python:3.10-slim",
    "WORKDIR /app",
    "COPY requirements.txt .",
    "RUN pip install --no-cache-dir -r requirements.txt",
    "COPY model.pkl .",
    "COPY app.py .",
    "EXPOSE 8000",
    "HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8000/health || exit 1",
    'CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]',
]
print("Dockerfile:")
for line in dockerfile_lines:
    print("  " + line)

# FastAPI app.py content (as list to avoid nested triple-quotes)
app_lines = [
    "import pickle, numpy as np",
    "from fastapi import FastAPI",
    "from pydantic import BaseModel",
    "app = FastAPI()",
    'model = pickle.load(open("model.pkl", "rb"))',
    "class Features(BaseModel):",
    "    features: list[float]",
    "@app.get('/health')",
    "def health(): return {'status': 'ok'}",
    "@app.post('/predict')",
    "def predict(data: Features):",
    "    pred = model.predict([data.features])",
    "    return {'prediction': int(pred[0])}",
]
print("\\napp.py:")
for line in app_lines:
    print("  " + line)
"""),
        ("Docker Multi-Stage Build & MLflow Docker", """\
# Multi-stage Dockerfile for smaller images
multistage_lines = [
    "FROM python:3.10 AS builder",
    "WORKDIR /build",
    "COPY requirements.txt .",
    "RUN pip install --user --no-cache-dir -r requirements.txt",
    "FROM python:3.10-slim AS production",
    "WORKDIR /app",
    "COPY --from=builder /root/.local /root/.local",
    "COPY . .",
    "ENV PATH=/root/.local/bin:$PATH",
    'CMD ["python", "serve.py"]',
]
print("Multi-stage Dockerfile:")
for line in multistage_lines:
    print("  " + line)

# MLflow built-in Docker packaging
mlflow_cmds = [
    "# Build Docker image from MLflow model (no Dockerfile needed!)",
    "mlflow models build-docker \\\\",
    '    --model-uri "models:/MyModel/Production" \\\\',
    '    --name "my-ml-model:latest"',
    "docker run -p 8080:8080 my-ml-model:latest",
    "curl -X POST http://localhost:8080/invocations \\\\",
    '    -H "Content-Type: application/json" \\\\',
    "    -d \\'{\"instances\": [[5.1, 3.5, 1.4, 0.2]]}\\'",
]
print("\\nMLflow Docker commands:")
for cmd in mlflow_cmds:
    print("  " + cmd)
"""),
    ],
    "Your data science team develops models locally but deployment always breaks due to package version mismatches. You need to containerize the model so it runs identically everywhere.",
    """\
import pickle, json, os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Train and save a model
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
acc = accuracy_score(y_test, model.predict(X_test))

# Save model artifact
model_path = "/tmp/iris_model.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)

# Generate deployment manifest
manifest = {
    "model": "RandomForestClassifier",
    "version": "1.0.0",
    "accuracy": round(acc, 4),
    "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
    "classes": ["setosa", "versicolor", "virginica"],
    "model_path": model_path,
    "docker_image": "iris-classifier:1.0.0",
    "port": 8000
}
print(json.dumps(manifest, indent=2))

# Simulate container health check
def health_check(model_pkl_path):
    with open(model_pkl_path, "rb") as f:
        m = pickle.load(f)
    test_input = np.array([[5.1, 3.5, 1.4, 0.2]])
    pred = m.predict(test_input)
    return {"status": "healthy", "test_prediction": int(pred[0])}

print("Health check:", health_check(model_path))
""",
    "Create a deployment manifest for a model",
    "Save a trained model and generate a JSON manifest with model metadata and deployment configuration.",
    """\
import pickle, json
from sklearn.dummy import DummyClassifier
from sklearn.datasets import load_iris
X, y = load_iris(return_X_y=True)
m = DummyClassifier().fit(X, y)
with open("/tmp/model.pkl", "wb") as f: pickle.dump(m, f)
print(json.dumps({"model": "DummyClassifier", "port": 8000}, indent=2))
"""
)

# ── Section 21: REST API Serving with FastAPI ──────────────────────────────────
s21 = make_s(
    21, "REST API Serving with FastAPI",
    "FastAPI provides a high-performance, async-ready framework for building ML model serving APIs with automatic validation and documentation.",
    [
        ("Basic FastAPI Model Server", """\
# FastAPI ML serving (run with: uvicorn app:app --reload)
# app.py structure:
fastapi_lines = [
    "from fastapi import FastAPI",
    "from pydantic import BaseModel, validator",
    "from typing import List, Optional",
    "import time, pickle, numpy as np",
    "",
    "app = FastAPI(title='ML Model API', version='1.0.0')",
    "model = None",
    "",
    "@app.on_event('startup')",
    "async def load_model():",
    "    global model",
    "    model = pickle.load(open('model.pkl', 'rb'))",
    "",
    "class PredictionRequest(BaseModel):",
    "    features: List[float]",
    "    model_version: Optional[str] = 'latest'",
    "",
    "@app.post('/predict')",
    "async def predict(request: PredictionRequest):",
    "    start = time.time()",
    "    pred = model.predict([request.features])",
    "    prob = model.predict_proba([request.features])",
    "    latency = (time.time() - start) * 1000",
    "    return {'prediction': int(pred[0]), 'probability': prob[0].tolist(), 'latency_ms': round(latency, 2)}",
    "",
    "@app.get('/health')",
    "async def health(): return {'status': 'ok'}",
]
print("FastAPI app.py:")
for line in fastapi_lines[:15]:
    print("  " + line)
print("  ...")
"""),
        ("Batch Prediction & Request Validation", """\
# Batch prediction endpoint + middleware
import numpy as np, time

# Simulate batch endpoint logic
def batch_predict(instances):
    X = np.array(instances)
    # predictions = model.predict(X)
    predictions = [0] * len(X)  # mock
    return {"predictions": predictions, "count": len(predictions)}

# Test batch
result = batch_predict([[5.1,3.5,1.4,0.2],[6.7,3.0,5.2,2.3],[4.9,3.0,1.4,0.2]])
print("Batch result:", result)

# Middleware pattern (request logging)
import functools, logging
def log_middleware(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start) * 1000
        logging.info(f"{func.__name__} completed in {duration:.2f}ms")
        return result
    return wrapper

@log_middleware
def predict_single(features):
    return {"prediction": 0, "latency_ms": 0.1}

res = predict_single([5.1, 3.5, 1.4, 0.2])
print("Single prediction:", res)

# FastAPI batch endpoint structure (key lines)
batch_endpoint_code = [
    "class BatchRequest(BaseModel):",
    "    instances: List[List[float]] = Field(..., min_items=1, max_items=1000)",
    "@app.post('/predict/batch')",
    "async def batch_predict(request: BatchRequest):",
    "    X = np.array(request.instances)",
    "    predictions = model.predict(X)",
    "    return {'predictions': predictions.tolist(), 'count': len(predictions)}",
]
print("\\nBatch endpoint structure:")
for line in batch_endpoint_code: print("  " + line)
"""),
    ],
    "Your ML model needs to serve predictions via an API that can handle 1000 requests/second with <50ms latency, validate inputs, and return probabilities with predictions.",
    """\
# Simulate FastAPI prediction pipeline
import numpy as np
import pickle
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Train model
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Simulate API prediction function
def predict_api(features: list) -> dict:
    if len(features) != 4:
        return {"error": f"Expected 4 features, got {len(features)}"}

    start = time.time()
    X = np.array([features])
    pred = model.predict(X)
    prob = model.predict_proba(X)
    latency_ms = (time.time() - start) * 1000

    return {
        "prediction": int(pred[0]),
        "probability": [round(p, 4) for p in prob[0]],
        "latency_ms": round(latency_ms, 3)
    }

# Test single prediction
result = predict_api([5.1, 3.5, 1.4, 0.2])
print("Single prediction:", result)

# Simulate batch prediction
batch = [[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3], [4.9, 3.0, 1.4, 0.2]]
start = time.time()
batch_results = [predict_api(f) for f in batch]
total_ms = (time.time() - start) * 1000
print(f"Batch of {len(batch)}: {total_ms:.2f}ms total")
for i, r in enumerate(batch_results):
    print(f"  [{i}] pred={r['prediction']}, prob_max={max(r['probability']):.4f}")
""",
    "Build a prediction function that validates input",
    "Create a function that checks input length, runs prediction, and returns prediction + probabilities.",
    """\
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.datasets import load_iris
X, y = load_iris(return_X_y=True)
model = DummyClassifier().fit(X, y)
def predict(features):
    if len(features) != 4: return {"error": "need 4 features"}
    pred = model.predict([features])
    return {"prediction": int(pred[0])}
print(predict([5.1, 3.5, 1.4, 0.2]))
"""
)

# ── Section 22: Model Monitoring & Drift Detection ────────────────────────────
s22 = make_s(
    22, "Model Monitoring & Drift Detection",
    "Production ML models degrade over time due to data drift and concept drift. Monitoring detects these shifts before they cause silent failures.",
    [
        ("Statistical Drift Detection", """\
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.datasets import load_iris

# Load reference (training) data
X, y = load_iris(return_X_y=True)
ref_data = pd.DataFrame(X, columns=["sepal_l", "sepal_w", "petal_l", "petal_w"])

# Simulate production data with drift
np.random.seed(42)
# Normal production (no drift)
prod_normal = ref_data + np.random.normal(0, 0.05, ref_data.shape)

# Drifted production (mean shift)
prod_drift = ref_data + np.random.normal(0.5, 0.2, ref_data.shape)

def detect_drift_ks(reference, current, alpha=0.05):
    # Kolmogorov-Smirnov test for distribution drift per feature
    results = {}
    for col in reference.columns:
        stat, p_val = stats.ks_2samp(reference[col], current[col])
        results[col] = {
            "ks_stat": round(stat, 4),
            "p_value": round(p_val, 4),
            "drift_detected": p_val < alpha
        }
    return results

print("=== No Drift Scenario ===")
for feat, res in detect_drift_ks(ref_data, prod_normal).items():
    flag = "DRIFT" if res["drift_detected"] else "OK"
    print(f"  {feat}: {flag} (p={res['p_value']:.4f})")

print("\\n=== Drift Scenario ===")
for feat, res in detect_drift_ks(ref_data, prod_drift).items():
    flag = "DRIFT" if res["drift_detected"] else "OK"
    print(f"  {feat}: {flag} (p={res['p_value']:.4f})")
"""),
        ("PSI & Model Performance Monitoring", """\
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def psi(expected, actual, buckets=10):
    # Population Stability Index: PSI > 0.2 = significant drift
    def scale_range(arr, min_val, max_val):
        arr = np.clip(arr, min_val, max_val)
        return arr

    min_val = min(expected.min(), actual.min())
    max_val = max(expected.max(), actual.max())

    breakpoints = np.linspace(min_val, max_val, buckets + 1)
    expected_perc = np.histogram(expected, bins=breakpoints)[0] / len(expected) + 1e-10
    actual_perc = np.histogram(actual, bins=breakpoints)[0] / len(actual) + 1e-10

    psi_val = np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc))
    return round(psi_val, 4)

# Train model
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, random_state=42)
model = RandomForestClassifier(n_estimators=50, random_state=42).fit(X_train, y_train)

# Reference predictions (training)
ref_probs = model.predict_proba(X_train)[:, 1]

# Simulated production prediction scores
prod_stable = model.predict_proba(X_test)[:, 1]
prod_drifted = np.clip(prod_stable + np.random.normal(0.3, 0.1, len(prod_stable)), 0, 1)

print(f"PSI (stable):  {psi(ref_probs, prod_stable):.4f}  {'OK' if psi(ref_probs, prod_stable) < 0.1 else 'DRIFT'}")
print(f"PSI (drifted): {psi(ref_probs, prod_drifted):.4f}  {'OK' if psi(ref_probs, prod_drifted) < 0.1 else 'DRIFT'}")
print("\\nPSI thresholds: <0.1 = stable, 0.1-0.2 = slight change, >0.2 = significant drift")
"""),
    ],
    "Your credit scoring model was accurate at launch but F1 dropped from 0.92 to 0.71 over 6 months. You need to detect data drift early and trigger retraining alerts.",
    """\
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

X, y = load_breast_cancer(return_X_y=True)
feat_names = load_breast_cancer().feature_names
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
baseline_f1 = f1_score(y_test, model.predict(X_test))
print(f"Baseline F1: {baseline_f1:.4f}")

# Simulate monthly production windows with increasing drift
months = 6
results = []
for month in range(1, months + 1):
    drift_level = month * 0.1
    X_prod = X_test + np.random.normal(drift_level, 0.05, X_test.shape)
    y_prod = model.predict(X_prod)

    # KS test on top 3 features
    drift_counts = sum(
        stats.ks_2samp(X_train[:, i], X_prod[:, i])[1] < 0.05
        for i in range(3)
    )

    # If we had labels, compute F1
    simulated_errors = (drift_level * np.random.randn(len(y_test))).astype(bool)
    y_labels = np.where(simulated_errors, 1 - y_test, y_test)
    f1 = f1_score(y_labels, model.predict(X_prod))

    results.append({"month": month, "f1": round(f1, 4), "drifted_features": drift_counts})
    alert = "ALERT" if f1 < baseline_f1 * 0.9 or drift_counts >= 2 else "OK"
    print(f"Month {month}: F1={f1:.4f}, drift_features={drift_counts} [{alert}]")
""",
    "Implement KS drift detection",
    "Compare training and production data distributions using KS test and flag features with p-value < 0.05.",
    """\
import numpy as np
from scipy import stats
ref = np.random.normal(0, 1, 1000)
prod = np.random.normal(0.5, 1, 1000)  # drifted
stat, p = stats.ks_2samp(ref, prod)
print(f"KS stat={stat:.4f}, p={p:.4f}, drift={'YES' if p<0.05 else 'NO'}")
"""
)

# ── Section 23: CI/CD for ML Pipelines ────────────────────────────────────────
s23 = make_s(
    23, "CI/CD for ML Pipelines",
    "CI/CD for ML automates testing, validation, and deployment of models, ensuring quality gates before any model reaches production.",
    [
        ("GitHub Actions ML Pipeline", """\
# .github/workflows/ml_pipeline.yml structure
yaml_lines = [
    "name: ML Pipeline CI/CD",
    "on:",
    "  push:",
    "    branches: [main]",
    "jobs:",
    "  test-and-validate:",
    "    runs-on: ubuntu-latest",
    "    steps:",
    "    - uses: actions/checkout@v3",
    "    - name: Set up Python",
    "      uses: actions/setup-python@v4",
    "      with:",
    "        python-version: '3.10'",
    "    - name: Install dependencies",
    "      run: pip install -r requirements.txt",
    "    - name: Run unit tests",
    "      run: pytest tests/ --cov=src",
    "    - name: Train model",
    "      run: python train.py",
    "    - name: Evaluate model (quality gate)",
    "      run: python evaluate.py --threshold 0.90",
    "    - name: Build Docker image",
    "      if: github.ref == 'refs/heads/main'",
    "      run: docker build -t my-model:latest .",
]
print(".github/workflows/ml_pipeline.yml:")
for line in yaml_lines:
    print("  " + line)
"""),
        ("Model Quality Gates", """\
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import json, sys

def evaluate_model(model, X_train, X_test, y_train, y_test, thresholds):
    # Quality gate: fail CI if model doesn't meet thresholds
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "f1_macro": round(f1_score(y_test, y_pred, average="macro"), 4),
        "cv_mean": round(cv_scores.mean(), 4),
        "cv_std": round(cv_scores.std(), 4),
    }

    passed = all(metrics.get(k, 0) >= v for k, v in thresholds.items())
    return metrics, passed

# Define quality gates
THRESHOLDS = {"accuracy": 0.90, "f1_macro": 0.88, "cv_mean": 0.89}

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)

metrics, passed = evaluate_model(model, X_train, X_test, y_train, y_test, THRESHOLDS)
print(json.dumps(metrics, indent=2))
print(f"\\nQuality Gate: {'PASSED ✓' if passed else 'FAILED ✗'}")
if not passed:
    print("Failed thresholds:", {k: v for k, v in THRESHOLDS.items() if metrics.get(k, 0) < v})
    # sys.exit(1)  # Uncomment in real CI to fail the pipeline
"""),
    ],
    "Your team deploys new models manually, causing production incidents when untested code reaches users. You need automated testing, model quality gates, and staged deployment.",
    """\
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score
import json

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

THRESHOLDS = {"accuracy": 0.95, "f1": 0.94, "cv_mean": 0.94}

def ci_pipeline(model, model_name):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    cv = cross_val_score(model, X_train, y_train, cv=5)

    metrics = {
        "model": model_name,
        "accuracy": round(model.score(X_test, y_test), 4),
        "f1": round(f1_score(y_test, y_pred), 4),
        "cv_mean": round(cv.mean(), 4),
        "cv_std": round(cv.std(), 4),
    }

    failures = [k for k in ["accuracy", "f1", "cv_mean"] if metrics[k] < THRESHOLDS[k]]
    metrics["status"] = "PASSED" if not failures else f"FAILED: {failures}"
    return metrics

for model, name in [
    (RandomForestClassifier(n_estimators=100, random_state=42), "RandomForest"),
    (GradientBoostingClassifier(n_estimators=50, random_state=42), "GradientBoost"),
]:
    result = ci_pipeline(model, name)
    print(json.dumps(result, indent=2))
""",
    "Implement a model quality gate",
    "Write a function that evaluates a model against metric thresholds and returns pass/fail.",
    """\
from sklearn.dummy import DummyClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y)
m = DummyClassifier().fit(X_train, y_train)
acc = m.score(X_test, y_test)
passed = acc >= 0.30
print(f"Accuracy={acc:.4f}, gate={'PASSED' if passed else 'FAILED'}")
"""
)

# ── Section 24: Feature Stores & ML Platforms ─────────────────────────────────
s24 = make_s(
    24, "Feature Stores & ML Platforms",
    "Feature stores centralize, version, and serve ML features consistently across training and serving, eliminating training-serving skew.",
    [
        ("Feature Store with Feast", """\
# Feature store concepts using pandas (Feast-like workflow)
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Simulate a feature store
class SimpleFeatureStore:
    def __init__(self):
        self._features = {}
        self._entity_df = None

    def ingest(self, feature_view_name, df, entity_col="entity_id"):
        # Register feature data
        self._features[feature_view_name] = df.set_index(entity_col)
        print(f"Ingested '{feature_view_name}': {len(df)} rows, {len(df.columns)-1} features")

    def get_historical_features(self, entity_ids, feature_views):
        # Retrieve features for training
        dfs = [self._features[fv].loc[entity_ids] for fv in feature_views if fv in self._features]
        return pd.concat(dfs, axis=1).reset_index()

    def get_online_features(self, entity_id, feature_views):
        # Low-latency single-entity lookup for serving
        result = {"entity_id": entity_id}
        for fv in feature_views:
            if fv in self._features and entity_id in self._features[fv].index:
                result.update(self._features[fv].loc[entity_id].to_dict())
        return result

# Setup
store = SimpleFeatureStore()
np.random.seed(42)
n = 1000

# User behavioral features
user_features = pd.DataFrame({
    "entity_id": range(n),
    "avg_spend": np.random.exponential(50, n),
    "days_active": np.random.randint(1, 365, n),
    "n_transactions": np.random.poisson(10, n),
})
store.ingest("user_activity", user_features)

# User demographic features
user_demo = pd.DataFrame({
    "entity_id": range(n),
    "age": np.random.randint(18, 70, n),
    "credit_score": np.random.randint(300, 850, n),
})
store.ingest("user_demographics", user_demo)

# Historical features for training
train_features = store.get_historical_features(
    entity_ids=list(range(100)),
    feature_views=["user_activity", "user_demographics"]
)
print("Training features shape:", train_features.shape)
print(train_features.head(3).to_string())

# Online features for serving
online = store.get_online_features(42, ["user_activity", "user_demographics"])
print("\\nOnline features for entity 42:", online)
"""),
        ("Training-Serving Skew Prevention", """\
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Anti-pattern: inline preprocessing (causes training-serving skew)
def bad_preprocess(df):
    df["feature_ratio"] = df["f1"] / (df["f2"] + 1e-8)
    df["log_f3"] = np.log1p(df["f3"])
    return df[["feature_ratio", "log_f3", "f4"]].values

# Good pattern: encapsulate ALL preprocessing in a sklearn Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self
    def transform(self, X):
        X = pd.DataFrame(X, columns=["f1", "f2", "f3", "f4"])
        return np.column_stack([
            X["f1"] / (X["f2"] + 1e-8),   # ratio feature
            np.log1p(X["f3"]),              # log transform
            X["f4"]                          # passthrough
        ])

# Generate data
np.random.seed(42)
n = 1000
X = pd.DataFrame(np.abs(np.random.randn(n, 4)), columns=["f1", "f2", "f3", "f4"])
y = (X["f1"] > X["f2"]).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X.values, y, random_state=42)

# Full pipeline: preprocessing + model
full_pipeline = Pipeline([
    ("engineer", FeatureEngineer()),
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(n_estimators=50, random_state=42))
])

full_pipeline.fit(X_train, y_train)
acc = full_pipeline.score(X_test, y_test)
print(f"Pipeline accuracy: {acc:.4f}")

# Save entire pipeline (same logic used in training AND serving)
with open("/tmp/full_pipeline.pkl", "wb") as f:
    pickle.dump(full_pipeline, f)

# Serving: load and predict (ZERO skew risk)
with open("/tmp/full_pipeline.pkl", "rb") as f:
    serving_pipeline = pickle.load(f)

pred = serving_pipeline.predict(X_test[:5])
print("Serving predictions:", pred)
print("Training-serving skew: ELIMINATED (same pipeline object)")
"""),
    ],
    "Your churn model uses 50 features computed differently during training (pandas) and serving (SQL). This training-serving skew causes 8% accuracy loss in production.",
    """\
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

np.random.seed(42)
n = 2000

# Simulate customer churn features
df = pd.DataFrame({
    "tenure_months": np.random.randint(1, 72, n),
    "monthly_charges": np.random.uniform(20, 120, n),
    "total_charges": np.random.uniform(20, 8000, n),
    "n_support_calls": np.random.poisson(2, n),
    "last_login_days": np.random.exponential(30, n),
})

# Target: churn if high charges + short tenure + many support calls
df["churn"] = (
    (df["monthly_charges"] > 80) &
    (df["tenure_months"] < 12) |
    (df["n_support_calls"] > 4)
).astype(int)

X = df.drop("churn", axis=1).values
y = df["churn"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Feature engineering + model in one pipeline
def add_features(X):
    X = np.copy(X)
    # charge_per_month = total / tenure
    charge_ratio = X[:, 2] / (X[:, 0] + 1)
    # recency_support_interaction
    recency_support = X[:, 3] * np.log1p(X[:, 4])
    return np.column_stack([X, charge_ratio, recency_support])

pipeline = Pipeline([
    ("engineer", FunctionTransformer(add_features)),
    ("scaler", StandardScaler()),
    ("model", GradientBoostingClassifier(n_estimators=100, random_state=42))
])

pipeline.fit(X_train, y_train)
print("Churn model pipeline accuracy:", round(pipeline.score(X_test, y_test), 4))
print(classification_report(y_test, pipeline.predict(X_test)))

# Single-entity serving prediction
customer = np.array([[24, 95.0, 2500.0, 3, 45.0]])
pred = pipeline.predict(customer)
prob = pipeline.predict_proba(customer)
print(f"Customer churn prediction: {'CHURN' if pred[0] else 'RETAIN'} (prob={prob[0][1]:.4f})")
""",
    "Build a feature engineering pipeline",
    "Use sklearn Pipeline with FunctionTransformer for feature engineering to prevent training-serving skew.",
    """\
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.dummy import DummyClassifier

def add_feat(X): return np.column_stack([X, X[:, 0] / (X[:, 1] + 1)])
pipe = Pipeline([("eng", FunctionTransformer(add_feat)), ("sc", StandardScaler()), ("m", DummyClassifier())])
X = np.random.randn(100, 3); y = np.random.randint(0, 2, 100)
pipe.fit(X, y)
print("Pipeline works:", pipe.predict(X[:3]))
"""
)

# ── Assemble ──────────────────────────────────────────────────────────────────
all_sections = s17+s18+s19+s20+s21+s22+s23+s24
result = insert_sections(FILE, MARKER, all_sections)
print("SUCCESS" if result else "FAILED")
