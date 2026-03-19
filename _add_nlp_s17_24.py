"""Add sections 17-24 to gen_nlp.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _inserter import insert_sections

FILE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_nlp.py"
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
        f'            "starter": "{ec(ps)}"\n'
        f'        }}\n'
        f'    }},\n\n    '
    )

# ── Section 17: Named Entity Recognition (NER) ────────────────────────────────
s17 = make_s(
    17, "Named Entity Recognition (NER)",
    "NER identifies and classifies named entities (persons, organizations, locations, dates) in text using spaCy or Transformers.",
    [
        ("spaCy NER", """\
import spacy
from collections import Counter

# Load spaCy model (run: python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Run: python -m spacy download en_core_web_sm")
    nlp = None

text = (
    "Apple Inc. CEO Tim Cook announced in San Francisco on January 15, 2024 "
    "that the company would invest $1 billion in AI research. "
    "The partnership with OpenAI and Microsoft was confirmed by Google."
)

if nlp:
    doc = nlp(text)
    print("Named Entities:")
    for ent in doc.ents:
        print(f"  {ent.text:<30} [{ent.label_}] - {spacy.explain(ent.label_)}")

    # Count entity types
    type_counts = Counter(ent.label_ for ent in doc.ents)
    print("\\nEntity type counts:", dict(type_counts))
else:
    # Simulate output structure
    entities = [
        ("Apple Inc.", "ORG", "Companies"), ("Tim Cook", "PERSON", "People"),
        ("San Francisco", "GPE", "Geo-political"), ("January 15, 2024", "DATE", "Dates"),
        ("$1 billion", "MONEY", "Monetary"), ("OpenAI", "ORG", "Companies"),
        ("Microsoft", "ORG", "Companies"), ("Google", "ORG", "Companies"),
    ]
    for text_ent, label, explain in entities:
        print(f"  {text_ent:<30} [{label}] - {explain}")
"""),
        ("Custom NER with spaCy Ruler", """\
import spacy
from spacy.language import Language

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = spacy.blank("en")

# Add EntityRuler for custom entities
ruler = nlp.add_pipe("entity_ruler", before="ner" if "ner" in nlp.pipe_names else "last")

# Define custom patterns
patterns = [
    {"label": "ML_MODEL", "pattern": "BERT"},
    {"label": "ML_MODEL", "pattern": "GPT-4"},
    {"label": "ML_MODEL", "pattern": "ResNet"},
    {"label": "ML_TASK", "pattern": "named entity recognition"},
    {"label": "ML_TASK", "pattern": "sentiment analysis"},
    {"label": "DATASET", "pattern": [{"LOWER": "imagenet"}]},
    {"label": "DATASET", "pattern": "CIFAR-10"},
]
ruler.add_patterns(patterns)

test_texts = [
    "BERT and GPT-4 are popular ML models for named entity recognition.",
    "ResNet was trained on ImageNet and CIFAR-10 datasets.",
    "sentiment analysis using BERT achieves state-of-the-art results.",
]

for text in test_texts:
    doc = nlp(text)
    ents = [(e.text, e.label_) for e in doc.ents]
    print(f"Text: {text[:50]}...")
    print(f"  Entities: {ents}\\n")
"""),
    ],
    "Your company processes thousands of customer support tickets daily. You need to extract product names, error codes, and customer IDs to route tickets automatically.",
    """\
import re
from collections import defaultdict

# Rule-based NER for support tickets (when spaCy not available)
PATTERNS = {
    "PRODUCT": [r"\\b(Model-[A-Z]\\d+|Product-\\w+|SKU-\\d+)\\b"],
    "ERROR_CODE": [r"\\bERR-?\\d{3,5}\\b", r"\\bError\\s+\\d{3,5}\\b"],
    "TICKET_ID": [r"\\b(TKT|TICKET)-?\\d{5,8}\\b"],
    "VERSION": [r"\\bv\\d+\\.\\d+(\\.\\d+)?\\b"],
}

def extract_entities(text):
    entities = defaultdict(list)
    for label, pats in PATTERNS.items():
        for pat in pats:
            matches = re.findall(pat, text, re.IGNORECASE)
            if matches:
                flat = [m if isinstance(m, str) else m[0] for m in matches]
                entities[label].extend(flat)
    return dict(entities)

tickets = [
    "TKT-123456: Customer reports ERR-4042 on Model-X9 running v2.3.1",
    "TICKET-99887: SKU-A2B3C4 throws Error 500 after upgrade to v3.0.0",
    "TKT00112233: Product-Premium shows ERR4001 and ERR4002 intermittently",
]

for ticket in tickets:
    ents = extract_entities(ticket)
    print(f"Ticket: {ticket}")
    print(f"  Entities: {ents}\\n")
""",
    "Extract entities from text",
    "Use re.findall with named patterns to extract PERSON, ORG, and DATE-like patterns from a text string.",
    """\
import re
text = "John Smith joined Acme Corp on 2024-01-15 and Microsoft on 2024-03-20."
dates = re.findall(r"\\d{4}-\\d{2}-\\d{2}", text)
names = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", text)
print("Dates:", dates)
print("Names:", names)
"""
)

# ── Section 18: Sentence Embeddings & Semantic Search ─────────────────────────
s18 = make_s(
    18, "Sentence Embeddings & Semantic Search",
    "Sentence embeddings convert text to dense vectors capturing semantic meaning, enabling similarity search beyond keyword matching.",
    [
        ("TF-IDF & Cosine Similarity", """\
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Document corpus
corpus = [
    "machine learning algorithms for classification",
    "deep learning neural networks for image recognition",
    "natural language processing text classification",
    "computer vision object detection algorithms",
    "transformer models for text generation",
    "reinforcement learning reward optimization",
]

# Build TF-IDF matrix
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(corpus)
print(f"TF-IDF matrix: {tfidf_matrix.shape}")

# Semantic search function
def search(query, top_k=3):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, tfidf_matrix)[0]
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [(corpus[i], round(float(scores[i]), 4)) for i in top_idx]

queries = [
    "text classification with deep learning",
    "visual recognition algorithms",
]
for q in queries:
    print(f"\\nQuery: '{q}'")
    for doc, score in search(q):
        print(f"  [{score:.4f}] {doc}")
"""),
        ("Word2Vec-Style Embeddings", """\
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create co-occurrence matrix (simplified Word2Vec concept)
sentences = [
    "the cat sat on the mat",
    "the dog lay on the rug",
    "cats and dogs are pets",
    "machine learning models learn patterns",
    "deep learning uses neural networks",
    "neural networks learn representations",
]

# Build co-occurrence proxy via SVD on count matrix
vectorizer = CountVectorizer(min_df=1)
X = vectorizer.fit_transform(sentences)

# SVD to get dense embeddings (like word2vec)
svd = TruncatedSVD(n_components=8, random_state=42)
embeddings = svd.fit_transform(X)

print("Sentence embeddings shape:", embeddings.shape)

# Find similar sentences
def find_similar(idx, top_k=3):
    sims = cosine_similarity([embeddings[idx]], embeddings)[0]
    sims[idx] = -1  # exclude self
    top = np.argsort(sims)[::-1][:top_k]
    return [(sentences[i], round(float(sims[i]), 4)) for i in top]

for i in [0, 3]:
    print(f"\\nSimilar to: '{sentences[i]}'")
    for sent, sim in find_similar(i):
        print(f"  [{sim:.4f}] {sent}")
"""),
    ],
    "Your FAQ system returns irrelevant results because it uses keyword matching. You need semantic search that understands 'password reset' and 'forgot credentials' are similar.",
    """\
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# FAQ knowledge base
faqs = [
    ("How do I reset my password?", "Click Forgot Password on login page, enter email, check inbox."),
    ("How to change account email?", "Go to Settings > Account > Email and enter new address."),
    ("Why is my payment failing?", "Check card details, billing address, or try a different card."),
    ("How to cancel my subscription?", "Go to Settings > Billing > Cancel Subscription."),
    ("How do I download my invoice?", "Settings > Billing > Invoice History > Download PDF."),
    ("Account locked after failed logins?", "Wait 30 minutes or contact support@example.com."),
]

questions = [q for q, _ in faqs]
answers = [a for _, a in faqs]

vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
faq_matrix = vec.fit_transform(questions)

def answer_query(user_query, threshold=0.1):
    q_vec = vec.transform([user_query])
    scores = cosine_similarity(q_vec, faq_matrix)[0]
    best_idx = np.argmax(scores)
    if scores[best_idx] < threshold:
        return "I couldn't find a relevant answer. Please contact support."
    return f"[score={scores[best_idx]:.3f}] {answers[best_idx]}"

test_queries = [
    "forgot my credentials",
    "payment not working",
    "stop my plan",
    "get billing document",
]
for q in test_queries:
    print(f"Q: {q}")
    print(f"A: {answer_query(q)}\\n")
""",
    "Build a semantic search function",
    "Use TfidfVectorizer and cosine_similarity to find the most similar document to a query.",
    """\
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

docs = ["python programming", "machine learning python", "deep learning neural nets"]
vec = TfidfVectorizer()
X = vec.fit_transform(docs)
query = vec.transform(["python learning"])
scores = cosine_similarity(query, X)[0]
print("Best match:", docs[np.argmax(scores)])
"""
)

# ── Section 19: Hugging Face Transformers ─────────────────────────────────────
s19 = make_s(
    19, "Hugging Face Transformers",
    "Hugging Face Transformers provides thousands of pretrained models for text classification, generation, Q&A, and more via a unified API.",
    [
        ("Sentiment Analysis Pipeline", """\
# pip install transformers torch
# Using Hugging Face pipeline (simulated output shown)
try:
    from transformers import pipeline

    # Zero-shot classification (no fine-tuning needed)
    classifier = pipeline("zero-shot-classification",
                          model="facebook/bart-large-mnli")

    texts = [
        "The product quality is excellent and delivery was fast!",
        "Terrible service, waited 3 weeks and got wrong item.",
        "The item is okay, nothing special but works as expected.",
    ]

    candidate_labels = ["positive", "negative", "neutral"]

    for text in texts:
        result = classifier(text, candidate_labels)
        top_label = result["labels"][0]
        top_score = result["scores"][0]
        print(f"Text: {text[:50]}...")
        print(f"  -> {top_label} (score={top_score:.4f})")

except ImportError:
    # Simulate output structure
    results = [
        ("positive", 0.9823), ("negative", 0.9541), ("neutral", 0.7234)
    ]
    texts = ["Excellent product!", "Terrible service.", "Works okay."]
    for (text, (label, score)) in zip(texts, results):
        print(f"Text: {text}")
        print(f"  -> {label} (score={score:.4f})")
"""),
        ("Token Classification & Feature Extraction", """\
# Token classification and feature extraction patterns
try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    import torch

    # NER pipeline
    ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english",
                   aggregation_strategy="simple")
    text = "Apple CEO Tim Cook announced a deal with Microsoft in New York."
    entities = ner(text)
    for ent in entities:
        print(f"  {ent['word']:<20} {ent['entity_group']:<10} score={ent['score']:.4f}")

except ImportError:
    # Demonstrate the pipeline usage pattern
    import numpy as np
    print("Simulated NER output (install transformers for real results):")
    entities = [
        {"word": "Apple", "entity_group": "ORG", "score": 0.9987},
        {"word": "Tim Cook", "entity_group": "PER", "score": 0.9945},
        {"word": "Microsoft", "entity_group": "ORG", "score": 0.9978},
        {"word": "New York", "entity_group": "LOC", "score": 0.9923},
    ]
    for ent in entities:
        print(f"  {ent['word']:<20} {ent['entity_group']:<10} score={ent['score']:.4f}")

    # Simulate sentence embeddings
    print("\\nSimulating sentence embeddings (mean pooling over tokens):")
    batch_size, seq_len, hidden = 2, 128, 768
    token_embeddings = np.random.randn(batch_size, seq_len, hidden)
    sentence_embeddings = token_embeddings.mean(axis=1)
    print(f"  Input shape: {token_embeddings.shape}")
    print(f"  Sentence embedding shape: {sentence_embeddings.shape}")
"""),
    ],
    "Your customer feedback system processes 10,000 reviews daily. You need to classify sentiment, extract product aspects, and identify key topics without building models from scratch.",
    """\
# Using sklearn to simulate transformer-like text classification
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Simulated reviews dataset
reviews = [
    ("Great product, fast shipping, very satisfied!", "positive"),
    ("Amazing quality, exceeded expectations.", "positive"),
    ("Good value for money, would recommend.", "positive"),
    ("Works as described, happy with purchase.", "positive"),
    ("Terrible quality, broke after one day.", "negative"),
    ("Do not buy this, complete waste of money.", "negative"),
    ("Very disappointed, nothing like the description.", "negative"),
    ("Poor build quality, returned immediately.", "negative"),
    ("Item is okay, nothing special.", "neutral"),
    ("Average product, does the job.", "neutral"),
    ("Received the item, it works.", "neutral"),
    ("Product is fine, shipping was slow.", "neutral"),
]

texts, labels = zip(*reviews)
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.33, random_state=42)

# Pipeline (simulates HF pipeline interface)
clf = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
    ("model", LogisticRegression(max_iter=1000, random_state=42)),
])
clf.fit(X_train, y_train)
print(classification_report(y_test, clf.predict(X_test)))

# Batch prediction (like HF pipeline)
new_reviews = [
    "Absolutely love this product!",
    "Received damaged, very unhappy.",
    "It is what it is, does the job.",
]
for review in new_reviews:
    pred = clf.predict([review])[0]
    prob = max(clf.predict_proba([review])[0])
    print(f"  [{pred:>8}] ({prob:.3f}) {review}")
""",
    "Build a text classifier pipeline",
    "Use sklearn Pipeline with TfidfVectorizer and LogisticRegression to classify text into categories.",
    """\
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

texts = ["I love this", "I hate this", "This is great", "This is terrible"]
labels = ["pos", "neg", "pos", "neg"]
clf = Pipeline([("tfidf", TfidfVectorizer()), ("nb", MultinomialNB())])
clf.fit(texts, labels)
print(clf.predict(["This is amazing"]))
"""
)

# ── Section 20: Topic Modeling with LDA ───────────────────────────────────────
s20 = make_s(
    20, "Topic Modeling with LDA",
    "Latent Dirichlet Allocation (LDA) discovers hidden topics in a text corpus by modeling documents as mixtures of topics.",
    [
        ("LDA with Gensim", """\
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

# Sample corpus
documents = [
    "machine learning neural networks deep learning artificial intelligence",
    "python programming data science numpy pandas matplotlib",
    "stock market trading investment portfolio risk management",
    "climate change global warming carbon emissions renewable energy",
    "machine learning algorithms random forest gradient boosting",
    "python web development flask django rest api",
    "investment strategy hedge fund returns portfolio optimization",
    "solar wind energy renewable green sustainability climate",
    "deep learning computer vision image classification convolutional",
    "data analysis pandas visualization matplotlib seaborn statistics",
]

# Fit LDA
vectorizer = CountVectorizer(max_df=0.95, min_df=1, stop_words="english")
X = vectorizer.fit_transform(documents)
vocab = vectorizer.get_feature_names_out()

lda = LatentDirichletAllocation(n_components=3, random_state=42, max_iter=20)
lda.fit(X)

# Display top words per topic
print("Discovered Topics:")
for topic_id, topic in enumerate(lda.components_):
    top_words = [vocab[i] for i in topic.argsort()[:-8:-1]]
    print(f"  Topic {topic_id+1}: {', '.join(top_words)}")

# Document-topic distribution
doc_topics = lda.transform(X)
for i, doc in enumerate(documents[:3]):
    dominant = doc_topics[i].argmax() + 1
    print(f"\\nDoc {i+1}: Topic {dominant} dominant ({doc_topics[i].max():.3f})")
    print(f"  '{doc[:50]}'")
"""),
        ("Topic Coherence & NMF", """\
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

# Non-negative Matrix Factorization (often better coherence than LDA)
news_snippets = [
    "president signed new economic policy tax reform bill congress",
    "federal reserve interest rates inflation monetary policy",
    "championship game football team playoffs season victory",
    "basketball nba draft player trade contract signed",
    "covid vaccine efficacy clinical trial approval fda",
    "hospital treatment patient therapy drug clinical",
    "election campaign voter poll candidate debate",
    "tech company IPO stock shares market valuation",
    "championship trophy league season playoffs basketball",
    "interest rate hike federal bank economic growth",
]

vectorizer = TfidfVectorizer(max_df=0.95, min_df=1, stop_words="english")
tfidf = vectorizer.fit_transform(news_snippets)
vocab = vectorizer.get_feature_names_out()

# NMF topic modeling
nmf = NMF(n_components=4, random_state=42)
W = nmf.fit_transform(tfidf)  # document-topic
H = nmf.components_           # topic-word

print("NMF Topics (typically more coherent):")
topic_names = ["Politics", "Economy", "Sports", "Health"]
for i, (row, name) in enumerate(zip(H, topic_names)):
    top_words = [vocab[j] for j in row.argsort()[:-6:-1]]
    print(f"  Topic {i+1} ({name}): {', '.join(top_words)}")

# Dominant topic per document
for i, doc in enumerate(news_snippets[:4]):
    dominant = W[i].argmax()
    print(f"\\nDoc: '{doc[:45]}...'")
    print(f"  Dominant topic: {topic_names[dominant]} ({W[i].max():.3f})")
"""),
    ],
    "Your news aggregation platform has 100,000 articles with no labels. You need to automatically discover and tag content themes to power category browsing.",
    """\
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF

articles = [
    "SpaceX launched new rocket to international space station moon mission",
    "NASA astronauts complete spacewalk satellite deployment orbital",
    "Python programming language machine learning framework scikit-learn",
    "JavaScript web development React frontend component library",
    "Olympic gold medal swimming athletics world record champion",
    "NBA basketball playoffs championship team finals victory",
    "AI language model chatbot GPT transformer neural network",
    "deep learning computer vision object detection classification",
    "marathon runner athletics world record broken championship",
    "rocket launch satellite orbit space exploration mission",
    "JavaScript TypeScript web app development framework React",
    "NBA finals championship basketball playoffs season",
]

# Compare LDA vs NMF
count_vec = CountVectorizer(max_df=0.95, min_df=1, stop_words="english")
tfidf_vec = TfidfVectorizer(max_df=0.95, min_df=1, stop_words="english")

X_count = count_vec.fit_transform(articles)
X_tfidf = tfidf_vec.fit_transform(articles)

n_topics = 3
models = {
    "LDA": (LatentDirichletAllocation(n_components=n_topics, random_state=42), count_vec),
    "NMF": (NMF(n_components=n_topics, random_state=42), tfidf_vec),
}

for model_name, (model, vec) in models.items():
    X = vec.transform(articles)
    W = model.fit_transform(X)
    vocab = vec.get_feature_names_out()
    H = model.components_

    print(f"\\n{model_name} Topics:")
    for i, row in enumerate(H):
        top_words = [vocab[j] for j in row.argsort()[:-5:-1]]
        print(f"  Topic {i+1}: {', '.join(top_words)}")

    # Assign articles to topics
    assignments = W.argmax(axis=1)
    for topic in range(n_topics):
        docs = [articles[j][:40] for j in range(len(articles)) if assignments[j] == topic]
        print(f"  Topic {topic+1} docs: {docs}")
""",
    "Discover topics in a corpus",
    "Apply LDA with CountVectorizer to find 3 topics and print the top 5 words per topic.",
    """\
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

docs = ["cats dogs pets animals", "python code programming", "market stocks trading",
        "dog cat pet animal friend", "code software developer", "stock market price"]
vec = CountVectorizer(stop_words="english")
X = vec.fit_transform(docs)
lda = LatentDirichletAllocation(n_components=3, random_state=42)
lda.fit(X)
vocab = vec.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    print(f"Topic {i+1}:", [vocab[j] for j in topic.argsort()[:-4:-1]])
"""
)

# ── Section 21: Text Summarization ────────────────────────────────────────────
s21 = make_s(
    21, "Text Summarization",
    "Text summarization condenses long documents into shorter summaries, using extractive (key sentence selection) or abstractive (generation) approaches.",
    [
        ("Extractive Summarization (TF-IDF)", """\
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def extractive_summarize(text, n_sentences=3):
    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\\s+", text.strip())
    if len(sentences) <= n_sentences:
        return text

    # Score sentences by TF-IDF importance
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf = vectorizer.fit_transform(sentences)
        scores = np.array(tfidf.sum(axis=1)).flatten()
    except ValueError:
        return " ".join(sentences[:n_sentences])

    # Select top sentences in original order
    top_idx = sorted(np.argsort(scores)[-n_sentences:])
    return " ".join(sentences[i] for i in top_idx)

article = (
    "Machine learning is a subset of artificial intelligence that gives systems the ability "
    "to automatically learn and improve from experience. "
    "It focuses on developing computer programs that can access data and use it to learn for themselves. "
    "Deep learning is part of machine learning based on artificial neural networks. "
    "These networks have multiple layers and can learn representations of data with multiple levels of abstraction. "
    "Natural language processing enables computers to understand human language. "
    "Applications include chatbots, translation, and sentiment analysis. "
    "Computer vision allows machines to interpret and understand visual information. "
    "This includes image classification, object detection, and facial recognition. "
    "Reinforcement learning trains agents through reward and penalty signals."
)

summary = extractive_summarize(article, n_sentences=3)
original_words = len(article.split())
summary_words = len(summary.split())
print(f"Original: {original_words} words")
print(f"Summary:  {summary_words} words ({summary_words/original_words*100:.0f}% compression)")
print(f"\\nSummary:\\n{summary}")
"""),
        ("TextRank Algorithm", """\
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def textrank_summarize(text, n_sentences=3, damping=0.85, iterations=50):
    sentences = re.split(r"(?<=[.!?])\\s+", text.strip())
    if len(sentences) <= n_sentences:
        return " ".join(sentences)

    # Build similarity matrix
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf = vectorizer.fit_transform(sentences)
        sim_matrix = cosine_similarity(tfidf)
    except ValueError:
        return " ".join(sentences[:n_sentences])

    np.fill_diagonal(sim_matrix, 0)

    # Row-normalize
    row_sums = sim_matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    sim_matrix = sim_matrix / row_sums

    # Power iteration (PageRank-style)
    n = len(sentences)
    scores = np.ones(n) / n
    for _ in range(iterations):
        scores = (1 - damping) / n + damping * sim_matrix.T @ scores

    top_idx = sorted(np.argsort(scores)[-n_sentences:])
    return " ".join(sentences[i] for i in top_idx)

text = (
    "Python is a high-level programming language known for its simplicity. "
    "It supports multiple programming paradigms including procedural, object-oriented, and functional. "
    "Python is widely used in data science, machine learning, and web development. "
    "The language has a rich ecosystem of libraries like NumPy, Pandas, and TensorFlow. "
    "Its syntax is designed to be readable and concise, making it beginner-friendly. "
    "Python runs on all major platforms and has an active open-source community."
)

for n in [2, 3]:
    summary = textrank_summarize(text, n_sentences=n)
    ratio = len(summary.split()) / len(text.split()) * 100
    print(f"TextRank ({n} sentences, {ratio:.0f}% of original):")
    print(f"  {summary}\\n")
"""),
    ],
    "Legal documents average 50 pages. Your system needs to auto-generate executive summaries for lawyers to review before the full read, cutting review time by 80%.",
    """\
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def hybrid_summarize(text, ratio=0.3):
    sentences = re.split(r"(?<=[.!?])\\s+", text.strip())
    n = max(1, int(len(sentences) * ratio))

    vec = TfidfVectorizer(stop_words="english")
    try:
        X = vec.fit_transform(sentences)
    except ValueError:
        return sentences[0] if sentences else ""

    # TF-IDF sentence scores
    tfidf_scores = np.array(X.sum(axis=1)).flatten()

    # Position scores (penalize later sentences slightly)
    pos_scores = np.linspace(1.0, 0.5, len(sentences))

    # Diversity: penalize similar sentences
    sim = cosine_similarity(X)
    diversity_scores = np.ones(len(sentences))
    selected = []

    final_scores = tfidf_scores * pos_scores
    ranked = np.argsort(final_scores)[::-1]

    for idx in ranked:
        if len(selected) >= n:
            break
        # Check diversity
        if not selected or all(sim[idx][s] < 0.7 for s in selected):
            selected.append(idx)

    selected_sorted = sorted(selected)
    summary = " ".join(sentences[i] for i in selected_sorted)
    return summary

# Simulate a legal document excerpt
legal_text = (
    "This agreement is entered into between Party A and Party B on the date first written above. "
    "Party A agrees to provide software development services as described in Schedule A. "
    "Party B agrees to pay the fees outlined in Schedule B within 30 days of invoice. "
    "All intellectual property developed under this agreement shall belong to Party B. "
    "Party A warrants that services will be performed in a professional and workmanlike manner. "
    "This agreement shall be governed by the laws of the State of California. "
    "Either party may terminate this agreement with 30 days written notice. "
    "Confidentiality obligations shall survive termination for a period of 2 years. "
    "Any disputes shall be resolved through binding arbitration in San Francisco. "
    "This agreement constitutes the entire understanding between the parties."
)

summary = hybrid_summarize(legal_text, ratio=0.4)
print(f"Original: {len(legal_text.split())} words, {len(legal_text.split('. '))} sentences")
print(f"Summary:  {len(summary.split())} words")
print(f"\\n{summary}")
""",
    "Implement extractive summarization",
    "Write a function that scores sentences by word frequency and returns the top N sentences.",
    """\
import re
from collections import Counter

def summarize(text, n=2):
    sents = re.split(r"[.!?]+", text)
    sents = [s.strip() for s in sents if s.strip()]
    words = Counter(text.lower().split())
    scores = [sum(words[w.lower()] for w in s.split()) for s in sents]
    top = sorted(range(len(sents)), key=lambda i: scores[i], reverse=True)[:n]
    return ". ".join(sents[i] for i in sorted(top))

text = "Python is great. It is used in AI. AI is transforming industry. Python is simple."
print(summarize(text, 2))
"""
)

# ── Section 22: Question Answering ────────────────────────────────────────────
s22 = make_s(
    22, "Question Answering",
    "QA systems find answers to questions within a context passage using span extraction, retrieval-augmented generation (RAG), or knowledge bases.",
    [
        ("Extractive QA with TF-IDF", """\
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ExtractiveQA:
    def __init__(self, passage_size=2):
        self.passage_size = passage_size
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.passages = []
        self.passage_matrix = None

    def index(self, text):
        # Split into overlapping passages
        sentences = re.split(r"(?<=[.!?])\\s+", text.strip())
        passages = []
        for i in range(0, len(sentences), self.passage_size):
            chunk = " ".join(sentences[i:i+self.passage_size])
            if chunk.strip():
                passages.append(chunk)
        self.passages = passages
        self.passage_matrix = self.vectorizer.fit_transform(passages)

    def answer(self, question, top_k=1):
        q_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(q_vec, self.passage_matrix)[0]
        top_idx = np.argsort(scores)[::-1][:top_k]
        return [(self.passages[i], round(float(scores[i]), 4)) for i in top_idx]

context = (
    "Python was created by Guido van Rossum in 1991. "
    "The language emphasizes code readability and simplicity. "
    "Python 3.0 was released in 2008 with major changes from Python 2. "
    "NumPy was created by Travis Oliphant in 2005. "
    "Pandas was developed by Wes McKinney in 2008 for data manipulation. "
    "Scikit-learn was released in 2007 and provides machine learning tools. "
    "TensorFlow was developed by Google Brain team and released in 2015. "
    "PyTorch was released by Facebook AI Research in 2016."
)

qa = ExtractiveQA(passage_size=2)
qa.index(context)

questions = [
    "When was Python created?",
    "Who created pandas?",
    "When was TensorFlow released?",
]
for q in questions:
    answer, score = qa.answer(q)[0]
    print(f"Q: {q}")
    print(f"A: {answer} [score={score}]\\n")
"""),
        ("RAG-Style: Retrieve + Generate", """\
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Simulated knowledge base (RAG knowledge store)
KB = {
    "python_history": "Python was created by Guido van Rossum, first released in 1991. Python 3 was released in 2008.",
    "ml_libraries": "Scikit-learn (2007), TensorFlow (2015), PyTorch (2016) are major ML libraries.",
    "numpy_info": "NumPy provides N-dimensional array objects. It was created by Travis Oliphant in 2005.",
    "pandas_info": "Pandas was created by Wes McKinney in 2008. It provides DataFrames for data manipulation.",
    "deep_learning": "Deep learning uses neural networks with many layers. CNNs are used for images, RNNs for sequences.",
    "transformers": "Transformers use attention mechanisms. BERT (2018) and GPT (2018) are key transformer models.",
}

# Build retrieval index
vectorizer = TfidfVectorizer(stop_words="english")
docs = list(KB.values())
keys = list(KB.keys())
index = vectorizer.fit_transform(docs)

def rag_answer(question, top_k=2):
    q_vec = vectorizer.transform([question])
    scores = cosine_similarity(q_vec, index)[0]
    top_idx = np.argsort(scores)[::-1][:top_k]

    context = " ".join(docs[i] for i in top_idx)
    retrieved_keys = [keys[i] for i in top_idx]

    # Simple extraction: find sentence most similar to question
    sents = re.split(r"(?<=[.])\\s+", context)
    if not sents:
        return "No answer found."

    sent_vecs = vectorizer.transform(sents)
    sent_scores = cosine_similarity(q_vec, sent_vecs)[0]
    best_sent = sents[sent_scores.argmax()]

    return {"answer": best_sent, "sources": retrieved_keys, "context": context[:100]}

questions = ["Who created NumPy?", "What is deep learning?", "When was BERT released?"]
for q in questions:
    result = rag_answer(q)
    print(f"Q: {q}")
    print(f"  Answer: {result['answer']}")
    print(f"  Sources: {result['sources']}\\n")
"""),
    ],
    "Your internal knowledge base has 5,000 policy documents. Employees waste hours searching for specific policy answers. Build a QA system to answer HR questions instantly.",
    """\
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# HR Policy knowledge base
hr_policies = {
    "vacation": "Employees receive 15 vacation days per year. Unused days roll over up to 5 days. Request via HR portal.",
    "sick_leave": "12 sick days per year. Doctor certificate required for absences over 3 consecutive days.",
    "remote_work": "Employees may work remotely up to 3 days per week with manager approval. Core hours: 10am-3pm.",
    "expense_claims": "Submit expenses within 30 days of incurrence. Receipts required for amounts over $25.",
    "performance_review": "Annual reviews in December. Mid-year check-ins in June. Ratings: Exceeds, Meets, Below expectations.",
    "parental_leave": "16 weeks paid parental leave for primary caregivers. 4 weeks for secondary caregivers.",
    "training_budget": "Each employee receives $1,500 annual training budget. Approval from manager required.",
    "overtime": "Overtime must be pre-approved. Compensated at 1.5x rate for hours over 40/week.",
}

keys = list(hr_policies.keys())
docs = list(hr_policies.values())

vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
index = vec.fit_transform(docs)

def hr_qa(question, threshold=0.05):
    q_vec = vec.transform([question])
    scores = cosine_similarity(q_vec, index)[0]
    best = scores.argmax()
    if scores[best] < threshold:
        return "Policy not found. Please contact HR directly."
    policy_name = keys[best].replace("_", " ").title()
    return f"[{policy_name}] {docs[best]}"

questions = [
    "How many vacation days do I get?",
    "Can I work from home?",
    "How do I claim expenses?",
    "How much training budget do I have?",
    "What is the parental leave policy?",
]
for q in questions:
    print(f"Q: {q}")
    print(f"A: {hr_qa(q)}\\n")
""",
    "Build a simple QA retriever",
    "Index a list of passages with TF-IDF and return the most relevant passage for a question.",
    """\
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

passages = ["Python is easy to learn.", "NumPy is for arrays.", "Pandas is for data."]
vec = TfidfVectorizer()
X = vec.fit_transform(passages)
q = vec.transform(["What is NumPy?"])
scores = cosine_similarity(q, X)[0]
print("Answer:", passages[np.argmax(scores)])
"""
)

# ── Section 23: Text Generation & Language Models ─────────────────────────────
s23 = make_s(
    23, "Text Generation & Language Models",
    "Text generation produces fluent text continuations, completions, or creative content using n-gram models, Markov chains, or pretrained LLMs.",
    [
        ("N-gram Language Model", """\
import random
from collections import defaultdict, Counter
import re

class NgramLM:
    def __init__(self, n=2):
        self.n = n
        self.ngrams = defaultdict(Counter)

    def train(self, texts):
        for text in texts:
            tokens = text.lower().split()
            tokens = ["<s>"] * (self.n-1) + tokens + ["</s>"]
            for i in range(len(tokens) - self.n + 1):
                context = tuple(tokens[i:i+self.n-1])
                next_token = tokens[i+self.n-1]
                self.ngrams[context][next_token] += 1

    def generate(self, max_len=20, seed=None):
        if seed:
            random.seed(seed)
        context = ("<s>",) * (self.n-1)
        tokens = []
        for _ in range(max_len):
            if context not in self.ngrams:
                break
            candidates = list(self.ngrams[context].items())
            next_tok = random.choices(
                [w for w, _ in candidates],
                weights=[c for _, c in candidates]
            )[0]
            if next_tok == "</s>":
                break
            tokens.append(next_tok)
            context = context[1:] + (next_tok,)
        return " ".join(tokens)

corpus = [
    "the cat sat on the mat and the dog sat on the rug",
    "machine learning models learn from data and improve over time",
    "deep learning uses neural networks with many layers",
    "natural language processing handles text and speech data",
    "data science involves statistics machine learning and programming",
]

model = NgramLM(n=3)
model.train(corpus)
print("Generated text (trigram LM):")
for i in range(4):
    print(f"  {i+1}: {model.generate(max_len=12, seed=i)}")
"""),
        ("Markov Chain Text Generator", """\
import random
from collections import defaultdict
import re

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.chain = defaultdict(list)
        self.starts = []

    def train(self, text):
        words = re.findall(r"\\w+[.,!?]?", text.lower())
        if len(words) < self.order + 1:
            return
        self.starts.append(tuple(words[:self.order]))
        for i in range(len(words) - self.order):
            key = tuple(words[i:i+self.order])
            self.chain[key].append(words[i+self.order])

    def generate(self, n_words=30, seed=42):
        random.seed(seed)
        if not self.starts:
            return ""
        state = random.choice(self.starts)
        result = list(state)
        for _ in range(n_words - self.order):
            if state not in self.chain:
                break
            next_word = random.choice(self.chain[state])
            result.append(next_word)
            state = tuple(result[-self.order:])
        return " ".join(result).capitalize()

mc = MarkovChain(order=2)
training_data = [
    "Data science combines statistics, machine learning, and domain expertise to extract insights from data.",
    "Machine learning models learn patterns from training data and generalize to new examples.",
    "Deep learning architectures with many layers can learn hierarchical representations.",
    "Natural language processing techniques enable machines to understand and generate human language.",
]
for text in training_data:
    mc.train(text)

print("Markov Chain Generated Text:")
for seed in [1, 2, 3]:
    print(f"  Seed {seed}: {mc.generate(n_words=20, seed=seed)}")
"""),
    ],
    "Your game studio needs procedurally generated quest descriptions and item names. You need a text generator that produces diverse, thematic text without a large model.",
    """\
import random
from collections import defaultdict
import re

# Template-based + Markov hybrid generator for game content
class GameTextGenerator:
    def __init__(self, order=2):
        self.order = order
        self.chain = defaultdict(list)
        self.starts = []
        self.templates = {
            "quest": [
                "Retrieve the {item} from {location} and return to {npc}.",
                "Defeat the {enemy} that threatens {location}.",
                "Escort {npc} safely through {location} to {destination}.",
                "Discover the secrets of {location} by finding {item}.",
            ],
            "item": [
                "Ancient {adj} {noun} of {attribute}",
                "{adj} {noun} Forged in {location}",
                "The {npc}'s Sacred {noun}",
            ]
        }
        self.vocab = {
            "item": ["Sword", "Amulet", "Tome", "Crystal", "Shield", "Ring"],
            "location": ["Dark Forest", "Mountain Peak", "Sunken Temple", "Iron Citadel"],
            "npc": ["Elder Mage", "Village Chief", "Wandering Merchant", "Oracle"],
            "enemy": ["Shadow Drake", "Corrupted Knight", "Ancient Golem", "Bandit Lord"],
            "adj": ["Cursed", "Sacred", "Ancient", "Enchanted", "Forgotten"],
            "noun": ["Blade", "Tome", "Relic", "Seal", "Chalice"],
            "attribute": ["Fire", "Ice", "Lightning", "Void", "Light"],
            "destination": ["Capital City", "Hidden Sanctuary", "Mountain Fortress"],
        }

    def generate_from_template(self, template_type, seed=None):
        if seed is not None:
            random.seed(seed)
        template = random.choice(self.templates[template_type])
        result = template
        for key, options in self.vocab.items():
            placeholder = "{" + key + "}"
            if placeholder in result:
                result = result.replace(placeholder, random.choice(options))
        return result

random.seed(42)
gen = GameTextGenerator()
print("Generated Quests:")
for i in range(4):
    print(f"  Quest {i+1}: {gen.generate_from_template('quest', seed=i)}")
print("\\nGenerated Items:")
for i in range(4):
    print(f"  Item {i+1}: {gen.generate_from_template('item', seed=i+10)}")
""",
    "Build a Markov chain text generator",
    "Train a bigram Markov chain on sample text and generate 3 different sentences.",
    """\
import random
from collections import defaultdict

chain = defaultdict(list)
text = "the cat sat on the mat the cat ate the rat the rat ran away"
words = text.split()
for i in range(len(words)-1):
    chain[words[i]].append(words[i+1])

random.seed(42)
word = "the"
result = [word]
for _ in range(10):
    if word not in chain: break
    word = random.choice(chain[word])
    result.append(word)
print(" ".join(result))
"""
)

# ── Section 24: NLP Pipeline & Production Deployment ──────────────────────────
s24 = make_s(
    24, "NLP Pipeline & Production Deployment",
    "A production NLP pipeline integrates preprocessing, vectorization, modeling, and post-processing into a reliable, scalable system.",
    [
        ("End-to-End NLP Pipeline", """\
import re
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
from sklearn.base import BaseEstimator, TransformerMixin

class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, lowercase=True, remove_punct=True, remove_numbers=False):
        self.lowercase = lowercase
        self.remove_punct = remove_punct
        self.remove_numbers = remove_numbers

    def preprocess(self, text):
        if self.lowercase:
            text = text.lower()
        if self.remove_punct:
            text = re.sub(r"[^\\w\\s]", " ", text)
        if self.remove_numbers:
            text = re.sub(r"\\d+", "", text)
        text = re.sub(r"\\s+", " ", text).strip()
        return text

    def fit(self, X, y=None): return self
    def transform(self, X): return [self.preprocess(t) for t in X]

# Sample dataset
texts = [
    "Great product, fast shipping, very satisfied!",
    "Terrible quality, broke after one week.",
    "Average item, nothing special.",
    "Excellent! Exceeded all expectations!",
    "Disappointed with the purchase.",
    "Does the job, no complaints.",
    "Best purchase I have made this year!",
    "Waste of money, poor customer service.",
]
labels = ["pos", "neg", "neu", "pos", "neg", "neu", "pos", "neg"]

X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.25, random_state=42)

pipeline = Pipeline([
    ("preprocessor", TextPreprocessor(lowercase=True, remove_punct=True)),
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
    ("classifier", LogisticRegression(C=1.0, max_iter=1000, random_state=42)),
])

pipeline.fit(X_train, y_train)
print("Test accuracy:", round(pipeline.score(X_test, y_test), 4))
print(classification_report(y_test, pipeline.predict(X_test), zero_division=0))

# New predictions
new_texts = ["Amazing value!", "Completely broken on arrival.", "It works."]
for text, pred in zip(new_texts, pipeline.predict(new_texts)):
    print(f"  [{pred}] {text}")
"""),
        ("NLP Monitoring & Input Validation", """\
import re
import numpy as np
from collections import deque
from datetime import datetime

class NLPProductionSystem:
    def __init__(self, model, vectorizer):
        self.model = model
        self.vectorizer = vectorizer
        self.request_log = deque(maxlen=1000)
        self.prediction_counts = {}
        self.error_rate = 0.0

    def validate_input(self, text):
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        if len(text.strip()) < 3:
            raise ValueError("Input too short (minimum 3 chars)")
        if len(text) > 10000:
            raise ValueError("Input too long (maximum 10000 chars)")
        # Check for injection-like patterns
        if re.search(r"[<>{}|\\\\]", text):
            text = re.sub(r"[<>{}|\\\\]", " ", text)
        return text.strip()

    def predict(self, text):
        ts = datetime.now().isoformat()
        try:
            clean_text = self.validate_input(text)
            # Simulate prediction
            features = self.vectorizer.transform([clean_text])
            pred = self.model.predict(features)[0]
            prob = self.model.predict_proba(features).max()

            # Log request
            log_entry = {"ts": ts, "text_len": len(clean_text), "pred": pred, "prob": round(float(prob), 4)}
            self.request_log.append(log_entry)

            # Track prediction distribution
            self.prediction_counts[pred] = self.prediction_counts.get(pred, 0) + 1

            return {"prediction": pred, "confidence": round(float(prob), 4), "status": "ok"}

        except Exception as e:
            self.error_rate = (self.error_rate * len(self.request_log) + 1) / (len(self.request_log) + 1)
            return {"error": str(e), "status": "error"}

    def health_report(self):
        total = len(self.request_log)
        return {
            "total_requests": total,
            "prediction_distribution": self.prediction_counts,
            "error_rate": round(self.error_rate, 4),
            "avg_text_length": round(np.mean([r["text_len"] for r in self.request_log]) if self.request_log else 0, 1)
        }

# Setup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

vec = TfidfVectorizer(ngram_range=(1,2))
texts = ["great product", "terrible quality", "okay item", "excellent service",
         "bad experience", "good value", "poor quality", "fantastic result"]
labels = ["pos","neg","neu","pos","neg","pos","neg","pos"]
vec.fit(texts)
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(vec.transform(texts), labels)

system = NLPProductionSystem(model, vec)

test_inputs = ["Amazing product!", "", "a", "Works great!", "Very poor quality...", "It is fine I guess"]
for text in test_inputs:
    result = system.predict(text)
    print(f"  Input: {repr(text):<40} -> {result}")

print("\\nHealth Report:", system.health_report())
"""),
    ],
    "Your company needs a production NLP API serving 50,000 requests/day for customer intent classification. It must handle malformed inputs, log predictions, and detect when the model is underperforming.",
    """\
import re
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import json

# Intent classification dataset
intents = [
    ("I want to buy a new laptop", "purchase"),
    ("Can I get a refund for my order?", "refund"),
    ("How do I track my package?", "tracking"),
    ("I want to cancel my subscription", "cancel"),
    ("What is your return policy?", "policy"),
    ("Add item to my shopping cart", "purchase"),
    ("My order has not arrived yet", "tracking"),
    ("I would like my money back", "refund"),
    ("Stop my monthly plan", "cancel"),
    ("What are your shipping rules?", "policy"),
    ("Buy now and save 20%", "purchase"),
    ("Request a full refund please", "refund"),
    ("Where is my delivery?", "tracking"),
    ("I want to end my account", "cancel"),
    ("Tell me about your privacy policy", "policy"),
]

texts, labels = zip(*intents)

# Production pipeline
clf = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), sublinear_tf=True, max_features=5000)),
    ("lr", LogisticRegression(C=1.0, max_iter=1000, random_state=42)),
])

# Cross-validate (small dataset, so use all data for demo)
clf.fit(texts, labels)

# Test on new inputs
test_inputs = [
    "I need to return this product",
    "Where is my shipment?",
    "Cancel my account immediately",
    "I want to purchase this item",
    "What are the terms of service?",
]

print("Intent Classification Results:")
for text in test_inputs:
    pred = clf.predict([text])[0]
    probs = clf.predict_proba([text])[0]
    classes = clf.classes_
    confidence = max(probs)
    print(f"  [{pred:<10}] ({confidence:.3f}) {text}")

# Prediction audit log
audit = []
for text in test_inputs:
    pred = clf.predict([text])[0]
    conf = float(max(clf.predict_proba([text])[0]))
    needs_review = conf < 0.7
    audit.append({"text": text[:30], "intent": pred, "confidence": round(conf, 3), "review": needs_review})

print("\\nAudit Log:")
print(json.dumps(audit, indent=2))
""",
    "Build a text classification pipeline",
    "Create an sklearn Pipeline with TfidfVectorizer + LogisticRegression, train it on intent examples, and classify new inputs.",
    """\
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

train = [("buy now", "purchase"), ("cancel plan", "cancel"), ("track order", "tracking")]
texts, labels = zip(*train)
clf = Pipeline([("tfidf", TfidfVectorizer()), ("lr", LogisticRegression(max_iter=100))])
clf.fit(texts, labels)
print(clf.predict(["I want to stop my subscription"]))
"""
)

# ── Assemble ──────────────────────────────────────────────────────────────────
all_sections = s17+s18+s19+s20+s21+s22+s23+s24
result = insert_sections(FILE, MARKER, all_sections)
print("SUCCESS" if result else "FAILED")
