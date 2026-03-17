"""Add 3 sections each to gen_nlp.py and gen_mlops.py."""
import sys
sys.path.insert(0, '.')
from _inserter import insert_sections

BASE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path"

def ec(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace("'", "\\'")

def make_section(num, title, examples, rw_scenario, rw_code, p_title, p_desc, p_starter):
    lines = [f'    {{\n        "title": "{num}. {title}",\n        "examples": [']
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples)-1 else ''
        lines.append(f'            {{\n                "label": "{ex["label"]}",\n                "code": "{ec(ex["code"])}"\n            }}{comma}')
    lines.append(f'        ],\n        "rw_scenario": "{ec(rw_scenario)}",')
    lines.append(f'        "rw_code": "{ec(rw_code)}",')
    lines.append(f'        "practice": {{\n            "title": "{p_title}",\n            "desc": "{ec(p_desc)}",\n            "starter": "{ec(p_starter)}"\n        }}\n    }},')
    return '\n'.join(lines) + '\n'

# ═══════════════════════════════════════════════════════════════════
#  NLP SECTIONS
# ═══════════════════════════════════════════════════════════════════

nlp14_examples = [
    {
        "label": "Tokenization & Subword Encoding with HuggingFace",
        "code": """from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
texts = [
    "The stock market crashed on Monday.",
    "Transformers revolutionized NLP in 2017!"
]
encoded = tokenizer(texts, padding=True, truncation=True, max_length=32, return_tensors="pt")
print("Input IDs shape:", encoded["input_ids"].shape)
for i, text in enumerate(texts):
    tokens = tokenizer.convert_ids_to_tokens(encoded["input_ids"][i])
    tokens = [t for t in tokens if t != "[PAD]"]
    print(f"\\nText {i+1}: {tokens}")
print("\\nVocab size:", tokenizer.vocab_size)"""
    },
    {
        "label": "Sentiment Classification with Pre-trained BERT",
        "code": """from transformers import pipeline
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
reviews = [
    "This product exceeded all my expectations! Absolutely fantastic.",
    "Terrible quality. Broke after one day. Very disappointed.",
    "It is okay, nothing special but gets the job done.",
]
results = classifier(reviews)
for text, result in zip(reviews, results):
    label = result["label"]
    score = result["score"]
    print(f"[{label} {score:.3f}] {text[:50]}...")"""
    },
    {
        "label": "Zero-Shot Classification",
        "code": """from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
text = "The Federal Reserve raised interest rates by 25 basis points today."
candidate_labels = ["finance", "sports", "technology", "politics", "health"]
result = classifier(text, candidate_labels)
print("Text:", text[:70])
print("\\nClassification scores:")
for label, score in zip(result["labels"], result["scores"]):
    bar = "#" * int(score * 30)
    print(f"  {label:<12} {score:.4f}  {bar}")"""
    }
]

nlp14_rw = "Customer support triage: classify incoming support tickets into departments (billing, technical, returns, general) using zero-shot classification without any labeled training data."
nlp14_rw_code = """from transformers import pipeline
# Zero-shot ticket router
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
tickets = [
    "My credit card was charged twice for the same order.",
    "The app keeps crashing whenever I try to open settings.",
    "I want to return the shoes I bought last week. They don't fit.",
    "When will my order arrive? It's been two weeks.",
    "I forgot my password and the reset link doesn't work.",
]
departments = ["billing", "technical support", "returns & refunds", "shipping", "account access"]
print("Support Ticket Routing")
print("=" * 60)
for ticket in tickets:
    result = classifier(ticket, departments, multi_label=False)
    top_dept = result["labels"][0]
    top_score = result["scores"][0]
    print(f"Ticket: {ticket[:55]}...")
    print(f"  -> {top_dept} ({top_score:.3f})")
    print()"""
nlp14_pt = "News Article Classifier"
nlp14_pd = "Use zero-shot classification with 6 news categories (politics, sports, technology, science, entertainment, business). Classify 5 different news headlines. Then use a pre-trained sentiment pipeline on the same headlines and combine both outputs into a structured report showing category + sentiment for each article."
nlp14_ps = """from transformers import pipeline
# News headlines to classify
headlines = [
    "SpaceX successfully lands reusable rocket for 20th time.",
    "Champions League final set as Real Madrid beats Bayern Munich.",
    "Senate votes to pass new climate legislation bill.",
    "Apple unveils new M4 chip with enhanced neural processing.",
    "GDP growth slows to 1.2% amid rising inflation concerns.",
]
categories = ["politics", "sports", "technology", "science", "entertainment", "business"]
# TODO: Zero-shot classify each headline into categories
# TODO: Run sentiment analysis on each headline
# TODO: Print formatted table: headline | category | sentiment | scores
"""

nlp15_examples = [
    {
        "label": "spaCy NER Pipeline",
        "code": """import spacy
nlp = spacy.load("en_core_web_sm")
texts = [
    "Apple Inc. CEO Tim Cook announced new products at WWDC in San Francisco.",
    "On March 14, 2023, the Fed raised rates by 25bps, affecting $4.5T in bonds.",
]
for text in texts:
    doc = nlp(text)
    print(f"Text: {text[:65]}...")
    print("Entities:")
    for ent in doc.ents:
        print(f"  [{ent.label_:<10}] '{ent.text}'")
    print()"""
    },
    {
        "label": "Custom NER with spaCy Patterns",
        "code": """import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
# Match product codes like "SKU-12345" or "PROD-ABC99"
pattern = [{"TEXT": {"REGEX": r"(SKU|PROD|ITEM)-[A-Z0-9]{3,8}"}}]
matcher.add("PRODUCT_CODE", [pattern])
texts = [
    "Customer ordered SKU-48291 and PROD-XR99 but ITEM-ZZ001 was out of stock.",
    "Return request for SKU-11100 received from warehouse.",
]
for text in texts:
    doc = nlp(text)
    matches = matcher(doc)
    codes = [doc[start:end].text for _, start, end in matches]
    print(f"Text: {text}")
    print(f"Product codes found: {codes}\\n")"""
    },
    {
        "label": "Relation Extraction with Dependency Parsing",
        "code": """import spacy
nlp = spacy.load("en_core_web_sm")
text = "Elon Musk founded SpaceX in 2002. Jeff Bezos started Amazon in 1994."
doc = nlp(text)
print("Subject-Verb-Object triples:")
for sent in doc.sents:
    for token in sent:
        if token.dep_ == "ROOT":
            subj = [c.text for c in token.children if c.dep_ in ("nsubj","nsubjpass")]
            obj  = [c.text for c in token.children if c.dep_ in ("dobj","attr","pobj")]
            if subj and obj:
                print(f"  ({subj[0]}) --[{token.text}]--> ({obj[0]})")
print("\\nNamed Entities:")
for ent in doc.ents:
    print(f"  {ent.text:<15} [{ent.label_}]")"""
    }
]

nlp15_rw = "Legal contract analysis: extract parties, dates, monetary amounts, and obligations from contract text to populate a structured database automatically."
nlp15_rw_code = """import spacy
import re
nlp = spacy.load("en_core_web_sm")
contract_text = \"\"\"
This Service Agreement is entered into on January 15, 2024, between
Acme Corporation, a Delaware company ("Client"), and TechSolutions LLC,
a California limited liability company ("Provider"). Client agrees to pay
Provider $12,500 per month for software development services. The agreement
terminates on December 31, 2024. Acme Corporation is headquartered in
New York, NY. Either party may terminate with 30 days written notice.
\"\"\"
doc = nlp(contract_text)
# Extract entities by type
parties = []
dates = []
money = []
for ent in doc.ents:
    if ent.label_ == "ORG":
        parties.append(ent.text)
    elif ent.label_ == "DATE":
        dates.append(ent.text)
    elif ent.label_ == "MONEY":
        money.append(ent.text)
print("Contract Extraction Report")
print(f"Parties:  {list(set(parties))}")
print(f"Dates:    {dates}")
print(f"Amounts:  {money}")
# Extract obligations with regex on sentence level
for sent in doc.sents:
    if any(w in sent.text.lower() for w in ["agrees", "shall", "must", "terminates"]):
        print(f"Obligation: {sent.text.strip()[:80]}")"""
nlp15_pt = "Resume Information Extractor"
nlp15_pd = "Given a sample resume text (3-4 sentences), use spaCy to extract: person name (PERSON), organizations (ORG), job titles (using custom Matcher patterns for 'Senior Engineer', 'Data Scientist', etc.), years of experience (CARDINAL + 'years'), and skills (custom pattern for capitalized tech terms). Output a structured JSON-like summary."
nlp15_ps = """import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")
resume = \"\"\"
John Smith is a Senior Data Scientist with 8 years of experience at Google and Microsoft.
He specializes in Python, TensorFlow, and SQL. Previously, he was a Machine Learning Engineer
at Amazon, where he led a team of 5 researchers. He holds a PhD from MIT in Computer Science.
\"\"\"
matcher = Matcher(nlp.vocab)
# TODO: Pattern for job titles (e.g., "Senior Data Scientist", "Machine Learning Engineer")
# TODO: Pattern for tech skills (capitalized 1-3 word terms)
# TODO: Extract PERSON, ORG, DATE, CARDINAL entities
# TODO: Output structured dict: name, companies, titles, skills, experience_years
"""

nlp16_examples = [
    {
        "label": "Text Generation with GPT-2",
        "code": """from transformers import pipeline
generator = pipeline("text-generation", model="gpt2", max_new_tokens=60)
prompts = [
    "The future of artificial intelligence is",
    "In 2035, data scientists will",
]
for prompt in prompts:
    outputs = generator(prompt, num_return_sequences=2, temperature=0.8, do_sample=True)
    print(f"Prompt: {prompt}")
    for i, out in enumerate(outputs, 1):
        generated = out["generated_text"][len(prompt):]
        print(f"  [{i}] ...{generated[:80]}")
    print()"""
    },
    {
        "label": "Structured Prompting & Prompt Engineering",
        "code": """# Demonstrates prompt engineering patterns (no API key needed — shows templates)
import json

def build_extraction_prompt(text, fields):
    field_list = ", ".join(f'"{f}"' for f in fields)
    return f\"\"\"Extract the following fields from the text below.
Return ONLY valid JSON with keys: {field_list}.
If a field is not found, use null.

Text: {text}

JSON output:\"\"\"

texts = [
    "Order #4521 placed by Sarah Johnson on 2024-03-15 for $289.99. Ships to Chicago, IL.",
    "Meeting scheduled with Dr. Patel at Boston General Hospital on Tuesday at 2pm."
]
fields_order   = ["order_id", "customer_name", "date", "amount", "city"]
fields_meeting = ["person", "organization", "day", "time"]
for text, fields in zip(texts, [fields_order, fields_meeting]):
    prompt = build_extraction_prompt(text, fields)
    print("=== Prompt Template ===")
    print(prompt[:200])
    print("...")
    print()"""
    },
    {
        "label": "Summarization with BART",
        "code": """from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn",
                      max_length=60, min_length=20, do_sample=False)
article = \"\"\"
Scientists at MIT have developed a new AI system capable of predicting protein
folding structures with greater accuracy than any previous model. The breakthrough,
published in Nature, combines deep learning with molecular dynamics simulations.
Researchers tested the system on over 10,000 known protein structures and achieved
98.5% accuracy. This development could accelerate drug discovery by enabling
researchers to design proteins that target specific disease pathways. The team plans
to make the model open-source within the next six months.
\"\"\"
summary = summarizer(article.strip())[0]["summary_text"]
original_words = len(article.split())
summary_words  = len(summary.split())
print(f"Original: {original_words} words")
print(f"Summary ({summary_words} words):")
print(summary)"""
    }
]

nlp16_rw = "Content moderation pipeline: automatically detect and summarize problematic content, classify severity, and route to appropriate human reviewer with context."
nlp16_rw_code = """from transformers import pipeline
# Multi-stage NLP pipeline: classify -> summarize -> route
classifier  = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
zero_shot   = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
posts = [
    "This is an amazing product! I love the design and performance.",
    "I hate this company. They stole my money and won't respond.",
    "How do I reset my password? I can't log in to my account.",
    "WARNING: This is a scam. Do NOT buy from this seller!!",
]
severity_labels = ["urgent - requires immediate review", "moderate - review within 24h", "low - can be auto-resolved"]
print("Content Moderation Pipeline")
print("=" * 60)
for post in posts:
    sentiment = classifier(post)[0]
    severity  = zero_shot(post, severity_labels)["labels"][0]
    print(f"Post: {post[:55]}...")
    print(f"  Sentiment: {sentiment['label']} ({sentiment['score']:.2f})")
    print(f"  Severity:  {severity}")
    print()"""
nlp16_pt = "Multi-Document Summarization"
nlp16_pd = "Summarize 3 different news articles (each 100+ words, on the same topic) using BART. Then concatenate the summaries and summarize again to create a 'meta-summary'. Compare word counts at each stage and compute the compression ratio. Also extract key noun phrases from the meta-summary using spaCy."
nlp16_ps = """from transformers import pipeline
import spacy
nlp_sp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn",
                      max_length=80, min_length=30, do_sample=False)
article1 = \"\"\"[Article 1: 100+ words on climate change - fill in]\"\"\""
article2 = \"\"\"[Article 2: 100+ words on climate policy - fill in]\"\"\""
article3 = \"\"\"[Article 3: 100+ words on renewable energy - fill in]\"\"\""
articles = [article1, article2, article3]
# TODO: Summarize each article individually
# TODO: Concatenate summaries and create meta-summary
# TODO: Compute compression ratios at each stage
# TODO: Extract noun chunks from meta-summary with spaCy
"""

# ═══════════════════════════════════════════════════════════════════
#  MLOPS SECTIONS
# ═══════════════════════════════════════════════════════════════════

mlops14_examples = [
    {
        "label": "Data Drift Detection with Population Stability Index",
        "code": """import numpy as np
def psi(expected, actual, n_bins=10):
    # Population Stability Index between two distributions.
    bins = np.percentile(expected, np.linspace(0, 100, n_bins+1))
    bins[0] -= 1e-6; bins[-1] += 1e-6
    e_counts = np.histogram(expected, bins=bins)[0] / len(expected)
    a_counts = np.histogram(actual,   bins=bins)[0] / len(actual)
    e_counts = np.where(e_counts == 0, 1e-6, e_counts)
    a_counts = np.where(a_counts == 0, 1e-6, a_counts)
    psi_val = np.sum((a_counts - e_counts) * np.log(a_counts / e_counts))
    return psi_val
np.random.seed(42)
reference = np.random.normal(0, 1, 1000)
stable    = np.random.normal(0.1, 1.0, 500)   # slight shift
drifted   = np.random.normal(1.5, 1.5, 500)   # significant drift
print(f"PSI (stable):  {psi(reference, stable):.4f}  (<0.1: no drift)")
print(f"PSI (drifted): {psi(reference, drifted):.4f}  (>0.25: severe drift)")"""
    },
    {
        "label": "Model Performance Degradation Monitoring",
        "code": """import numpy as np
from sklearn.metrics import accuracy_score
np.random.seed(1)
def simulate_batch(shift=0.0, n=200):
    X = np.random.randn(n, 5) + shift
    y_true = (X[:, 0] + X[:, 1] > shift).astype(int)
    # Simulated model trained on no-shift data
    y_pred = (X[:, 0] + X[:, 1] > 0).astype(int)
    return accuracy_score(y_true, y_pred)
print("Model Monitoring Dashboard")
print(f"{'Week':<6} {'Accuracy':<10} {'Status'}")
print("-" * 30)
baseline_acc = simulate_batch(shift=0.0)
for week in range(1, 9):
    shift = (week - 1) * 0.15
    acc = simulate_batch(shift=shift)
    delta = acc - baseline_acc
    status = "OK" if abs(delta) < 0.05 else ("WARN" if abs(delta) < 0.10 else "ALERT")
    print(f"  {week:<4} {acc:.4f}    {status}")"""
    },
    {
        "label": "Kolmogorov-Smirnov Drift Test",
        "code": """import numpy as np
from scipy import stats
np.random.seed(5)
# Simulate feature distributions: train vs production batches
train_dist  = np.random.normal(50, 10, 2000)
prod_no_drift = np.random.normal(50.5, 10.2, 500)
prod_drift    = np.random.normal(58.0, 12.0, 500)
features = {
    "no_drift_batch": prod_no_drift,
    "drifted_batch":  prod_drift,
}
for name, prod in features.items():
    ks_stat, p_val = stats.ks_2samp(train_dist, prod)
    drift = "DRIFT DETECTED" if p_val < 0.05 else "stable"
    print(f"{name:<20}: KS={ks_stat:.4f}, p={p_val:.6f} -> {drift}")"""
    }
]

mlops14_rw = "Deployed ML model for loan approval: monitor weekly for data drift in applicant features (income, credit score, age) using PSI, and alert the ML team when any feature shows PSI > 0.25."
mlops14_rw_code = """import numpy as np
def psi(ref, curr, n_bins=10):
    bins = np.percentile(ref, np.linspace(0, 100, n_bins+1))
    bins[0] -= 1e-6; bins[-1] += 1e-6
    e = np.histogram(ref,  bins=bins)[0] / len(ref)
    a = np.histogram(curr, bins=bins)[0] / len(curr)
    e = np.where(e == 0, 1e-6, e)
    a = np.where(a == 0, 1e-6, a)
    return float(np.sum((a - e) * np.log(a / e)))
np.random.seed(99)
# Training distribution
train_income = np.random.lognormal(10.8, 0.4, 5000)
train_credit = np.random.normal(680, 50, 5000)
train_age    = np.random.normal(38, 12, 5000)
print("Loan Model Feature Drift Report")
print(f"{'Feature':<15} {'PSI':<8} {'Status'}")
print("-" * 35)
weeks_drift = [0, 0.05, 0.12, 0.22, 0.35]  # progressive drift scenario
for week, drift in enumerate(weeks_drift, 1):
    prod_income = np.random.lognormal(10.8 + drift, 0.4 + drift*0.1, 500)
    prod_credit = np.random.normal(680 - drift*40, 50, 500)
    prod_age    = np.random.normal(38 + drift*2, 12, 500)
    results = {
        "income": psi(train_income, prod_income),
        "credit_score": psi(train_credit, prod_credit),
        "age": psi(train_age, prod_age),
    }
    max_psi_feat = max(results, key=results.get)
    max_psi = results[max_psi_feat]
    status = "ALERT" if max_psi > 0.25 else ("WARN" if max_psi > 0.10 else "OK")
    print(f"Week {week}: {max_psi_feat:<12} PSI={max_psi:.3f}  [{status}]")"""
mlops14_pt = "Multi-Feature Drift Dashboard"
mlops14_pd = "For a churn prediction model with 6 features (age, tenure, monthly_spend, num_products, is_active, region_encoded), simulate 8 weekly production batches where drift gradually increases in tenure and monthly_spend starting at week 4. Compute PSI and KS-test for each feature each week. Build a summary table and flag weeks where total PSI > 0.5."
mlops14_ps = """import numpy as np
from scipy import stats
def psi(ref, curr, n_bins=10):
    bins = np.percentile(ref, np.linspace(0, 100, n_bins+1))
    bins[0] -= 1e-6; bins[-1] += 1e-6
    e = np.histogram(ref,  bins=bins)[0] / len(ref)
    a = np.histogram(curr, bins=bins)[0] / len(curr)
    e = np.where(e == 0, 1e-6, e)
    a = np.where(a == 0, 1e-6, a)
    return float(np.sum((a - e) * np.log(a / e)))
np.random.seed(7)
n_train = 3000
features = {
    "age":           np.random.normal(35, 10, n_train),
    "tenure":        np.random.exponential(24, n_train),
    "monthly_spend": np.random.lognormal(4.5, 0.5, n_train),
    "num_products":  np.random.poisson(2.5, n_train).astype(float),
    "is_active":     np.random.binomial(1, 0.7, n_train).astype(float),
    "region":        np.random.randint(0, 5, n_train).astype(float),
}
# TODO: Generate 8 weekly batches of 300 samples (drift in tenure+spend from week 4)
# TODO: Compute PSI and KS-test p-value for each feature each week
# TODO: Flag weeks where total PSI > 0.5
# TODO: Print formatted weekly report table
"""

mlops15_examples = [
    {
        "label": "Feature Store Simulation with Feast-like API",
        "code": """import pandas as pd
import numpy as np
from datetime import datetime, timedelta
np.random.seed(42)
# Simulate a simple feature store
class SimpleFeatureStore:
    def __init__(self):
        self._store = {}
    def ingest(self, entity_id, features, timestamp):
        self._store[(entity_id, timestamp)] = features
    def get_historical(self, entity_ids, feature_names, as_of=None):
        results = []
        for eid in entity_ids:
            matching = {ts: feats for (e, ts), feats in self._store.items() if e == eid}
            if not matching: continue
            latest_ts = max(matching.keys())
            feats = matching[latest_ts]
            row = {"entity_id": eid, "timestamp": latest_ts}
            row.update({k: feats.get(k) for k in feature_names})
            results.append(row)
        return pd.DataFrame(results)
fs = SimpleFeatureStore()
# Ingest user features
for user_id in range(1, 6):
    fs.ingest(user_id, {"age": np.random.randint(20, 60),
                        "spend_30d": round(np.random.uniform(50, 500), 2),
                        "logins_7d": np.random.randint(1, 30)},
              datetime.now() - timedelta(hours=np.random.randint(1, 48)))
result = fs.get_historical([1, 2, 3], ["age", "spend_30d", "logins_7d"])
print(result.to_string(index=False))"""
    },
    {
        "label": "Data Pipeline with pandas + Validation",
        "code": """import pandas as pd
import numpy as np
np.random.seed(0)
# Raw data ingestion with quality checks
def build_training_pipeline(df_raw):
    report = {"input_rows": len(df_raw), "issues": []}
    # Null check
    null_pct = df_raw.isnull().mean()
    for col, pct in null_pct.items():
        if pct > 0.1:
            report["issues"].append(f"{col}: {pct:.1%} nulls")
    # Range validation
    if "age" in df_raw:
        invalid = ((df_raw["age"] < 0) | (df_raw["age"] > 120)).sum()
        if invalid: report["issues"].append(f"age: {invalid} out-of-range values")
    df = df_raw.dropna().copy()
    df = df[(df["age"].between(0, 120)) & (df["income"] > 0)]
    report["output_rows"] = len(df)
    report["drop_rate"] = 1 - len(df)/len(df_raw)
    return df, report
raw = pd.DataFrame({
    "age": np.random.choice([*np.random.randint(18,80,90), *[-1]*5, *[np.nan]*5], 100),
    "income": np.random.choice([*np.random.lognormal(10,0.5,85), *[np.nan]*15], 100),
})
clean, report = build_training_pipeline(raw)
print("Pipeline Report:", report)"""
    },
    {
        "label": "Training Data Versioning (DVC-style)",
        "code": """import hashlib, json, os
from datetime import datetime
class DataVersioner:
    # Simple data versioning inspired by DVC.
    def __init__(self, registry_path="data_registry.json"):
        self.registry_path = registry_path
        self.registry = {}
    def hash_data(self, data_str):
        return hashlib.md5(data_str.encode()).hexdigest()[:12]
    def register(self, name, data_str, metadata=None):
        version_id = self.hash_data(data_str)
        entry = {
            "name": name, "version": version_id,
            "timestamp": datetime.now().isoformat()[:19],
            "size_bytes": len(data_str),
            "metadata": metadata or {}
        }
        self.registry[version_id] = entry
        print(f"Registered: {name} v{version_id}")
        return version_id
    def lineage(self, version_id):
        entry = self.registry.get(version_id, {})
        print(f"Lineage for {version_id}: {json.dumps(entry, indent=2)}")
dv = DataVersioner()
v1 = dv.register("train_features", "col1,col2\\n1,2\\n3,4\\n5,6", {"n_rows": 3, "split": "train"})
v2 = dv.register("train_features", "col1,col2\\n1,2\\n3,4\\n5,6\\n7,8", {"n_rows": 4, "split": "train"})
dv.lineage(v1)"""
    }
]

mlops15_rw = "Recommendation system: maintain a feature store with user engagement features (clicks_7d, purchase_30d, category_affinity) updated hourly, served to the model at inference time with <10ms latency."
mlops15_rw_code = """import pandas as pd
import numpy as np
from datetime import datetime, timedelta
np.random.seed(42)
# Simulate feature store for recommendation system
class RecoFeatureStore:
    def __init__(self):
        self.user_features = {}
        self.item_features = {}
    def update_user(self, user_id, features):
        self.user_features[user_id] = {**features, "updated_at": datetime.now().isoformat()}
    def update_item(self, item_id, features):
        self.item_features[item_id] = {**features, "updated_at": datetime.now().isoformat()}
    def get_feature_vector(self, user_id, item_id):
        u = self.user_features.get(user_id, {})
        i = self.item_features.get(item_id, {})
        return {
            "user_clicks_7d": u.get("clicks_7d", 0),
            "user_purchase_30d": u.get("purchase_30d", 0),
            "item_avg_rating": i.get("avg_rating", 3.0),
            "item_purchase_count": i.get("purchase_count", 0),
            "affinity": u.get("category_affinity", {}).get(i.get("category"), 0.0)
        }
fs = RecoFeatureStore()
# Populate store
for uid in range(1, 6):
    fs.update_user(uid, {
        "clicks_7d": np.random.randint(5, 100),
        "purchase_30d": np.random.randint(0, 10),
        "category_affinity": {"electronics": np.random.uniform(0,1),
                               "books": np.random.uniform(0,1)}
    })
for iid in range(1, 4):
    fs.update_item(iid, {"avg_rating": np.random.uniform(3,5),
                          "purchase_count": np.random.randint(10,1000),
                          "category": np.random.choice(["electronics","books"])})
print("Feature vectors for serving:")
for uid in [1, 2]:
    for iid in [1, 2, 3]:
        fv = fs.get_feature_vector(uid, iid)
        print(f"  user={uid}, item={iid}: {fv}")"""
mlops15_pt = "ETL Pipeline with Schema Validation"
mlops15_pd = "Build a data pipeline that: (1) generates synthetic raw customer data with intentional quality issues (nulls, wrong types, out-of-range values), (2) validates schema using pandas dtype checks and range assertions, (3) cleans and transforms, (4) logs each step with row counts, (5) outputs a data quality report with pass/fail for each check."
mlops15_ps = """import pandas as pd
import numpy as np
np.random.seed(33)
# Generate raw data with issues
n = 500
raw = pd.DataFrame({
    "customer_id": range(n),
    "age": np.random.choice([*np.random.randint(18,80,460), *[-5]*20, *[np.nan]*20], n),
    "revenue": np.random.choice([*np.random.lognormal(6,1,450), *[np.nan]*50], n),
    "segment": np.random.choice(["A","B","C","INVALID",None], n),
    "signup_date": pd.date_range("2020-01-01", periods=n, freq="D")
})
# TODO: Schema validation (dtypes, ranges, allowed values)
# TODO: Cleaning steps (impute/drop nulls, fix dtypes, filter invalid segments)
# TODO: Log each step with before/after row counts
# TODO: Output data quality report DataFrame
"""

mlops16_examples = [
    {
        "label": "A/B Test Significance Calculator",
        "code": """import numpy as np
from scipy import stats
def ab_test(control_conv, control_n, treat_conv, treat_n, alpha=0.05):
    # Two-proportion z-test for A/B testing.
    p_c = control_conv / control_n
    p_t = treat_conv  / treat_n
    p_pool = (control_conv + treat_conv) / (control_n + treat_n)
    se = np.sqrt(p_pool * (1-p_pool) * (1/control_n + 1/treat_n))
    z = (p_t - p_c) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    ci = (p_t - p_c) + np.array([-1, 1]) * stats.norm.ppf(1-alpha/2) * se
    lift = (p_t - p_c) / p_c
    return {"z": z, "p_value": p_value, "lift": lift, "ci_95": ci,
            "significant": p_value < alpha}
result = ab_test(control_conv=120, control_n=2000, treat_conv=155, treat_n=2000)
print(f"Conversion: control={120/2000:.3f}, treat={155/2000:.3f}")
print(f"Lift: {result['lift']:+.2%}")
print(f"p-value: {result['p_value']:.4f}")
print(f"95% CI: [{result['ci_95'][0]:.4f}, {result['ci_95'][1]:.4f}]")
print(f"Significant: {result['significant']}")"""
    },
    {
        "label": "Canary Deployment Traffic Routing",
        "code": """import numpy as np
np.random.seed(42)
class CanaryRouter:
    def __init__(self, canary_pct=0.10):
        self.canary_pct = canary_pct
        self.metrics = {"control": [], "canary": []}
    def route(self):
        return "canary" if np.random.random() < self.canary_pct else "control"
    def record(self, model, latency_ms, error=False):
        self.metrics[model].append({"latency": latency_ms, "error": error})
    def report(self):
        for model, records in self.metrics.items():
            latencies = [r["latency"] for r in records]
            errors = [r["error"] for r in records]
            print(f"{model:<8}: n={len(records):4d}, avg_lat={np.mean(latencies):.1f}ms, "
                  f"p99={np.percentile(latencies,99):.1f}ms, err_rate={np.mean(errors):.3f}")
router = CanaryRouter(canary_pct=0.10)
for _ in range(2000):
    m = router.route()
    lat = np.random.lognormal(3.5 if m=="control" else 3.3, 0.4)
    err = np.random.random() < (0.02 if m=="control" else 0.025)
    router.record(m, lat, err)
router.report()"""
    },
    {
        "label": "Multi-Armed Bandit for Continuous Optimization",
        "code": """import numpy as np
np.random.seed(7)
# Thompson Sampling for online model selection
class ThompsonBandit:
    def __init__(self, n_arms):
        self.alpha = np.ones(n_arms)
        self.beta  = np.ones(n_arms)
    def select(self):
        return np.argmax(np.random.beta(self.alpha, self.beta))
    def update(self, arm, reward):
        self.alpha[arm] += reward
        self.beta[arm]  += (1 - reward)
# 3 model versions with different true conversion rates
true_rates = [0.05, 0.08, 0.06]
bandit = ThompsonBandit(n_arms=3)
counts = np.zeros(3, dtype=int)
rewards_total = 0
for t in range(5000):
    arm = bandit.select()
    reward = int(np.random.random() < true_rates[arm])
    bandit.update(arm, reward)
    counts[arm] += 1
    rewards_total += reward
print(f"Total conversions: {rewards_total} / 5000 = {rewards_total/5000:.4f}")
for i in range(3):
    print(f"  Model {i+1} (true={true_rates[i]:.2f}): selected {counts[i]:4d} times ({counts[i]/5000:.1%})")"""
    }
]

mlops16_rw = "ML-powered pricing engine: run A/B tests comparing new pricing model (15% canary) vs current model, with Thompson Sampling auto-routing more traffic to the better performer after statistical significance is reached."
mlops16_rw_code = """import numpy as np
from scipy import stats
np.random.seed(21)
# Combined: Canary + statistical testing + bandit
true_revenue_control = 45.0   # $45 avg order value
true_revenue_canary  = 47.5   # $47.5 with new pricing
class PricingExperiment:
    def __init__(self, canary_pct=0.15):
        self.canary_pct = canary_pct
        self.control_revenues = []
        self.canary_revenues  = []
        self.alpha = np.array([1.0, 1.0])  # Thompson beta params
        self.beta  = np.array([1.0, 1.0])
    def route(self):
        # Start as pure A/B, shift to bandit after significance
        if len(self.control_revenues) < 200:
            return "canary" if np.random.random() < self.canary_pct else "control"
        return "canary" if np.argmax(np.random.beta(self.alpha, self.beta)) == 1 else "control"
    def observe(self, model):
        if model == "control":
            rev = np.random.normal(true_revenue_control, 12)
            self.control_revenues.append(rev)
            self.alpha[0] += max(rev/100, 0); self.beta[0] += max(1-rev/100, 0)
        else:
            rev = np.random.normal(true_revenue_canary, 12)
            self.canary_revenues.append(rev)
            self.alpha[1] += max(rev/100, 0); self.beta[1] += max(1-rev/100, 0)
    def check_significance(self):
        if len(self.control_revenues) < 30 or len(self.canary_revenues) < 30:
            return None
        t, p = stats.ttest_ind(self.canary_revenues, self.control_revenues)
        return p
exp = PricingExperiment()
for i in range(3000):
    m = exp.route()
    exp.observe(m)
    if i % 500 == 499:
        p = exp.check_significance()
        print(f"t={i+1}: control=${np.mean(exp.control_revenues):.2f}, "
              f"canary=${np.mean(exp.canary_revenues):.2f}, p={p:.4f}")"""
mlops16_pt = "Online Experiment Platform"
mlops16_pd = "Build a complete A/B testing framework that: (1) assigns users to control/treatment with hash-based deterministic routing, (2) collects metrics (conversion, revenue) per variant, (3) computes p-values and confidence intervals daily, (4) auto-declares a winner when p<0.05 and min_sample=500/arm, (5) logs results to a DataFrame. Simulate 10,000 user sessions over 14 days."
mlops16_ps = """import numpy as np
import pandas as pd
from scipy import stats
np.random.seed(55)
# Experiment settings
TRUE_CONV_CONTROL = 0.04
TRUE_CONV_TREAT   = 0.048
TRUE_REV_CONTROL  = 30.0
TRUE_REV_TREAT    = 31.5
MIN_SAMPLE = 500
def assign(user_id):
    # Deterministic hash-based assignment
    return "treatment" if hash(f"exp1_{user_id}") % 2 == 0 else "control"
# TODO: Simulate 10,000 users over 14 days (approx 714/day)
# TODO: Track conversion and revenue per variant per day
# TODO: Daily significance check with two-proportion z-test
# TODO: Auto-declare winner when p<0.05 and n>=500/arm
# TODO: Log results to DataFrame with columns: day, n_control, n_treat, p_value, winner
"""

# ─── BUILD & INSERT ───────────────────────────────────────────────────────────
import os

nlp_sections = (
    make_section("14", "Transformer Models & Pre-trained Pipelines",
                 nlp14_examples, nlp14_rw, nlp14_rw_code, nlp14_pt, nlp14_pd, nlp14_ps) +
    make_section("15", "Named Entity Recognition & Information Extraction",
                 nlp15_examples, nlp15_rw, nlp15_rw_code, nlp15_pt, nlp15_pd, nlp15_ps) +
    make_section("16", "Text Generation, Summarization & Prompt Engineering",
                 nlp16_examples, nlp16_rw, nlp16_rw_code, nlp16_pt, nlp16_pd, nlp16_ps)
)

mlops_sections = (
    make_section("14", "Model Monitoring & Data Drift Detection",
                 mlops14_examples, mlops14_rw, mlops14_rw_code, mlops14_pt, mlops14_pd, mlops14_ps) +
    make_section("15", "Feature Stores & Data Engineering Pipelines",
                 mlops15_examples, mlops15_rw, mlops15_rw_code, mlops15_pt, mlops15_pd, mlops15_ps) +
    make_section("16", "A/B Testing & Canary Deployments for ML",
                 mlops16_examples, mlops16_rw, mlops16_rw_code, mlops16_pt, mlops16_pd, mlops16_ps)
)

nlp_path   = os.path.join(BASE, "gen_nlp.py")
mlops_path = os.path.join(BASE, "gen_mlops.py")

insert_sections(nlp_path,   "]  # end SECTIONS", nlp_sections)
insert_sections(mlops_path, "]  # end SECTIONS", mlops_sections)

print("Done!")
