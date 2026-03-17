#!/usr/bin/env python3
"""Generate NLP & Text Processing study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE   = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\13_nlp")
BASE.mkdir(parents=True, exist_ok=True)
ACCENT = "#a371f7"
EMOJI  = "🧠"
TITLE  = "NLP & Text Processing"

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
        "title": "1. Text Cleaning & Preprocessing",
        "desc": "Raw text is noisy. Learn to normalize case, remove punctuation, strip HTML, handle Unicode, and build reusable cleaning pipelines.",
        "examples": [
            {
                "label": "Basic text normalization",
                "code": (
                    "import re, string\n\n"
                    "text = '  Hello, World! This is NLP 101... Check <b>this</b> out!  '\n\n"
                    "# Lowercase\nclean = text.lower()\n"
                    "# Strip HTML tags\nclean = re.sub(r'<[^>]+>', '', clean)\n"
                    "# Remove punctuation\nclean = clean.translate(str.maketrans('', '', string.punctuation))\n"
                    "# Collapse whitespace\nclean = ' '.join(clean.split())\n"
                    "print(repr(clean))\n"
                    "# Output: 'hello world this is nlp 101 check this out'"
                )
            },
            {
                "label": "Regex-based cleaning patterns",
                "code": (
                    "import re\n\n"
                    "def clean_text(text):\n"
                    "    text = re.sub(r'http\\S+|www\\.\\S+', '', text)   # URLs\n"
                    "    text = re.sub(r'@\\w+', '', text)                 # @mentions\n"
                    "    text = re.sub(r'#\\w+', '', text)                 # hashtags\n"
                    "    text = re.sub(r'[^\\w\\s]', '', text)             # punctuation\n"
                    "    text = re.sub(r'\\d+', '', text)                  # digits\n"
                    "    text = re.sub(r'\\s+', ' ', text).strip()         # whitespace\n"
                    "    return text.lower()\n\n"
                    "tweet = 'Check out https://example.com #NLP @user! 123 Great stuff!!!'\n"
                    "print(clean_text(tweet))\n"
                    "# Output: 'check out  great stuff'"
                )
            },
            {
                "label": "Unicode normalization and encoding fixes",
                "code": (
                    "import unicodedata\n\n"
                    "text = 'Café naïve résumé — quotes \\u2018smart\\u2019'\n\n"
                    "# Normalize to ASCII (strip accents)\ndef to_ascii(text):\n"
                    "    nfkd = unicodedata.normalize('NFKD', text)\n"
                    "    return ''.join(c for c in nfkd if not unicodedata.combining(c))\n\n"
                    "# Normalize smart quotes to straight\ndef fix_quotes(text):\n"
                    "    replacements = {\\u2018: \"'\", \\u2019: \"'\", \\u201c: '\"', \\u201d: '\"',\n"
                    "                    \\u2013: '-', \\u2014: '-'}\n"
                    "    return ''.join(replacements.get(c, c) for c in text)\n\n"
                    "print(to_ascii(text))\n"
                    "print(fix_quotes(text))"
                )
            },
            {
                "label": "Building a reusable cleaning pipeline",
                "code": (
                    "import re, string\nfrom typing import List, Callable\n\n"
                    "def make_pipeline(*fns: Callable) -> Callable:\n"
                    "    def pipeline(text: str) -> str:\n"
                    "        for fn in fns:\n"
                    "            text = fn(text)\n"
                    "        return text\n"
                    "    return pipeline\n\n"
                    "lowercase       = str.lower\n"
                    "remove_urls     = lambda t: re.sub(r'http\\S+', '', t)\n"
                    "remove_punct    = lambda t: t.translate(str.maketrans('', '', string.punctuation))\n"
                    "collapse_spaces = lambda t: ' '.join(t.split())\n\n"
                    "clean = make_pipeline(lowercase, remove_urls, remove_punct, collapse_spaces)\n\n"
                    "texts = ['Visit https://ai.com for more!', 'Hello, World!!', '  PYTHON  NLP  ']\n"
                    "print([clean(t) for t in texts])"
                )
            },
        ],
        "rw_scenario": "A customer support team wants to preprocess thousands of support tickets before feeding them to a classifier. Tickets contain HTML, URLs, emojis, and inconsistent casing.",
        "rw_code": (
            "import re, string\n\n"
            "def preprocess_ticket(text: str) -> str:\n"
            "    text = re.sub(r'<[^>]+>', ' ', text)       # strip HTML\n"
            "    text = re.sub(r'http\\S+', '', text)        # remove URLs\n"
            "    text = text.encode('ascii', 'ignore').decode()  # strip emoji/unicode\n"
            "    text = text.lower()\n"
            "    text = re.sub(r'[^\\w\\s]', ' ', text)      # punctuation -> space\n"
            "    text = ' '.join(text.split())               # normalize whitespace\n"
            "    return text\n\n"
            "tickets = [\n"
            "    '<p>My <b>order</b> #12345 is LATE! See https://track.com/12345</p>',\n"
            "    'App crashed 😤 after update v2.1 — please fix ASAP!!!',\n"
            "]\n"
            "for t in tickets:\n"
            "    print(preprocess_ticket(t))"
        ),
        "practice": {
            "title": "Email Cleaner",
            "desc": "Write a function that strips email headers (From:, To:, Subject:), removes quoted lines starting with '>', and cleans leftover whitespace.",
            "starter": (
                "import re\n\n"
                "email = '''\n"
                "From: alice@example.com\n"
                "To: bob@example.com\n"
                "Subject: Project Update\n\n"
                "Hi Bob,\n\n"
                "> Thanks for the report\n"
                "> it was helpful\n\n"
                "Looks great! Let's sync tomorrow.\n"
                "'''\n\n"
                "def clean_email(text: str) -> str:\n"
                "    # TODO: Remove header lines (From:, To:, Subject:)\n"
                "    # TODO: Remove quoted lines (starting with >)\n"
                "    # TODO: Collapse blank lines\n"
                "    pass\n\n"
                "print(clean_email(email))"
            )
        }
    },
    {
        "title": "2. Tokenization & Stopword Removal",
        "desc": "Tokenization splits text into meaningful units. Stopword removal filters common words that carry little semantic weight.",
        "examples": [
            {
                "label": "Word and sentence tokenization with NLTK",
                "code": (
                    "import nltk\n"
                    "nltk.download('punkt', quiet=True)\n"
                    "nltk.download('punkt_tab', quiet=True)\n"
                    "from nltk.tokenize import word_tokenize, sent_tokenize\n\n"
                    "text = 'Dr. Smith said NLP is fun. It really is! Don\\'t you think?'\n\n"
                    "sentences = sent_tokenize(text)\n"
                    "print('Sentences:', sentences)\n\n"
                    "words = word_tokenize(text)\n"
                    "print('Words:', words)"
                )
            },
            {
                "label": "Stopword removal with NLTK",
                "code": (
                    "import nltk\n"
                    "nltk.download('stopwords', quiet=True)\n"
                    "nltk.download('punkt', quiet=True)\n"
                    "nltk.download('punkt_tab', quiet=True)\n"
                    "from nltk.corpus import stopwords\n"
                    "from nltk.tokenize import word_tokenize\n\n"
                    "stop_words = set(stopwords.words('english'))\n\n"
                    "text = 'The quick brown fox jumps over the lazy dog'\n"
                    "tokens = word_tokenize(text.lower())\n"
                    "filtered = [w for w in tokens if w.isalpha() and w not in stop_words]\n\n"
                    "print('Original tokens:', tokens)\n"
                    "print('Filtered:', filtered)"
                )
            },
            {
                "label": "Tokenization with spaCy",
                "code": (
                    "try:\n"
                    "    import spacy\n"
                    "    nlp = spacy.load('en_core_web_sm')\n"
                    "    text = 'Apple is looking at buying U.K. startup for $1 billion.'\n"
                    "    doc = nlp(text)\n"
                    "    tokens = [(t.text, t.pos_, t.is_stop) for t in doc]\n"
                    "    print('(token, POS, is_stop):')\n"
                    "    for tok in tokens:\n"
                    "        print(tok)\n"
                    "except OSError:\n"
                    "    print('Run: python -m spacy download en_core_web_sm')"
                )
            },
            {
                "label": "Subword tokenization with HuggingFace",
                "code": (
                    "try:\n"
                    "    from transformers import AutoTokenizer\n"
                    "    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')\n\n"
                    "    text = 'Tokenization handles out-of-vocabulary words cleverly.'\n"
                    "    tokens = tokenizer.tokenize(text)\n"
                    "    ids = tokenizer.encode(text)\n\n"
                    "    print('Subword tokens:', tokens)\n"
                    "    print('Token IDs:', ids)\n"
                    "    print('Decoded:', tokenizer.decode(ids))\n"
                    "except ImportError:\n"
                    "    print('pip install transformers')"
                )
            },
        ],
        "rw_scenario": "A search engine needs to index product reviews. Tokenize and filter stopwords to extract the keywords that matter for search relevance.",
        "rw_code": (
            "import nltk\n"
            "nltk.download('stopwords', quiet=True)\n"
            "nltk.download('punkt', quiet=True)\n"
            "nltk.download('punkt_tab', quiet=True)\n"
            "from nltk.corpus import stopwords\n"
            "from nltk.tokenize import word_tokenize\n"
            "from collections import Counter\n\n"
            "STOP = set(stopwords.words('english'))\n\n"
            "def extract_keywords(review: str, top_n: int = 5):\n"
            "    tokens = word_tokenize(review.lower())\n"
            "    keywords = [w for w in tokens if w.isalpha() and w not in STOP and len(w) > 2]\n"
            "    return Counter(keywords).most_common(top_n)\n\n"
            "review = 'The battery life is amazing. This phone has the best battery I have ever used. Great camera too.'\n"
            "print(extract_keywords(review))"
        ),
        "practice": {
            "title": "Custom Stopword Filter",
            "desc": "Extend the standard NLTK stopword list with domain-specific words (e.g., 'customer', 'product', 'order') and filter a list of reviews.",
            "starter": (
                "import nltk\n"
                "nltk.download('stopwords', quiet=True)\n"
                "nltk.download('punkt', quiet=True)\n"
                "nltk.download('punkt_tab', quiet=True)\n"
                "from nltk.corpus import stopwords\n"
                "from nltk.tokenize import word_tokenize\n\n"
                "DOMAIN_STOPS = {'customer', 'product', 'order', 'item', 'purchase'}\n\n"
                "def filter_tokens(text: str) -> list:\n"
                "    # TODO: combine NLTK stopwords + DOMAIN_STOPS\n"
                "    # TODO: tokenize, lowercase, filter\n"
                "    pass\n\n"
                "reviews = [\n"
                "    'Customer service was excellent, product quality amazing',\n"
                "    'Order arrived late but item was in perfect condition',\n"
                "]\n"
                "for r in reviews:\n"
                "    print(filter_tokens(r))"
            )
        }
    },
    {
        "title": "3. Stemming & Lemmatization",
        "desc": "Reduce words to their base forms. Stemming is fast but crude (running→run). Lemmatization is linguistically accurate (better→good).",
        "examples": [
            {
                "label": "Porter stemmer with NLTK",
                "code": (
                    "import nltk\n"
                    "from nltk.stem import PorterStemmer, SnowballStemmer\n\n"
                    "porter = PorterStemmer()\n"
                    "snowball = SnowballStemmer('english')\n\n"
                    "words = ['running', 'flies', 'happily', 'studies', 'beautiful', 'caring']\n\n"
                    "print(f'{'Word':<15} {'Porter':<15} {'Snowball':<15}')\n"
                    "for w in words:\n"
                    "    print(f'{w:<15} {porter.stem(w):<15} {snowball.stem(w):<15}')"
                )
            },
            {
                "label": "WordNet lemmatizer with POS tags",
                "code": (
                    "import nltk\n"
                    "nltk.download('wordnet', quiet=True)\n"
                    "nltk.download('omw-1.4', quiet=True)\n"
                    "from nltk.stem import WordNetLemmatizer\n"
                    "from nltk.corpus import wordnet\n\n"
                    "lemmatizer = WordNetLemmatizer()\n\n"
                    "# POS matters: 'better' as ADJ -> 'good', as VERB -> 'better'\n"
                    "examples = [\n"
                    "    ('better',  'a'),   # adjective\n"
                    "    ('running', 'v'),   # verb\n"
                    "    ('geese',   'n'),   # noun\n"
                    "    ('happily', 'r'),   # adverb\n"
                    "]\n"
                    "for word, pos in examples:\n"
                    "    lem = lemmatizer.lemmatize(word, pos=pos)\n"
                    "    print(f'{word} ({pos}) -> {lem}')"
                )
            },
            {
                "label": "Lemmatization with spaCy",
                "code": (
                    "try:\n"
                    "    import spacy\n"
                    "    nlp = spacy.load('en_core_web_sm')\n\n"
                    "    text = 'The children were running and the geese were flying'\n"
                    "    doc = nlp(text)\n\n"
                    "    print(f'{'Token':<15} {'Lemma':<15} {'POS':<10}')\n"
                    "    for token in doc:\n"
                    "        print(f'{token.text:<15} {token.lemma_:<15} {token.pos_:<10}')\n"
                    "except OSError:\n"
                    "    print('Run: python -m spacy download en_core_web_sm')"
                )
            },
            {
                "label": "Stemming vs Lemmatization comparison",
                "code": (
                    "import nltk\n"
                    "nltk.download('wordnet', quiet=True)\n"
                    "nltk.download('omw-1.4', quiet=True)\n"
                    "from nltk.stem import PorterStemmer, WordNetLemmatizer\n\n"
                    "stemmer = PorterStemmer()\n"
                    "lemmatizer = WordNetLemmatizer()\n\n"
                    "words = ['studies', 'studying', 'better', 'wolves', 'corpora', 'matrices']\n\n"
                    "print(f'{'Word':<12} {'Stem':<12} {'Lemma (n)':<12}')\n"
                    "for w in words:\n"
                    "    stem = stemmer.stem(w)\n"
                    "    lemma = lemmatizer.lemmatize(w, pos='n')\n"
                    "    print(f'{w:<12} {stem:<12} {lemma:<12}')"
                )
            },
        ],
        "rw_scenario": "A job board wants to match resumes to job postings regardless of tense or form — 'managed', 'manages', 'management' should all map to the same root concept.",
        "rw_code": (
            "import nltk\n"
            "nltk.download('wordnet', quiet=True)\n"
            "nltk.download('omw-1.4', quiet=True)\n"
            "nltk.download('stopwords', quiet=True)\n"
            "nltk.download('punkt', quiet=True)\n"
            "nltk.download('punkt_tab', quiet=True)\n"
            "from nltk.stem import WordNetLemmatizer\n"
            "from nltk.tokenize import word_tokenize\n"
            "from nltk.corpus import stopwords\n\n"
            "lem = WordNetLemmatizer()\n"
            "STOP = set(stopwords.words('english'))\n\n"
            "def normalize_skills(text: str) -> set:\n"
            "    tokens = word_tokenize(text.lower())\n"
            "    return {lem.lemmatize(w, 'v') for w in tokens if w.isalpha() and w not in STOP}\n\n"
            "job_req  = 'Managed budgets, leading teams, developed strategies'\n"
            "resume   = 'manages budgets, leads cross-functional teams, develop product strategy'\n\n"
            "job_kw  = normalize_skills(job_req)\n"
            "res_kw  = normalize_skills(resume)\n"
            "overlap = job_kw & res_kw\n"
            "print('Match score:', len(overlap) / len(job_kw))\n"
            "print('Matched keywords:', overlap)"
        ),
        "practice": {
            "title": "Search Term Normalizer",
            "desc": "Write a function that takes a search query and returns all lemma forms so a search for 'running shoes' also matches 'run' and 'shoe'.",
            "starter": (
                "import nltk\n"
                "nltk.download('wordnet', quiet=True)\n"
                "nltk.download('omw-1.4', quiet=True)\n"
                "nltk.download('punkt', quiet=True)\n"
                "nltk.download('punkt_tab', quiet=True)\n"
                "from nltk.stem import WordNetLemmatizer\n"
                "from nltk.tokenize import word_tokenize\n\n"
                "lem = WordNetLemmatizer()\n\n"
                "def normalize_query(query: str) -> list:\n"
                "    # TODO: tokenize, lemmatize as both noun and verb, deduplicate\n"
                "    pass\n\n"
                "queries = ['running shoes', 'buying products', 'managed accounts']\n"
                "for q in queries:\n"
                "    print(q, '->', normalize_query(q))"
            )
        }
    },
    {
        "title": "4. Named Entity Recognition (NER)",
        "desc": "NER identifies and classifies named entities (persons, organizations, locations, dates) in text — essential for information extraction.",
        "examples": [
            {
                "label": "NER with spaCy",
                "code": (
                    "try:\n"
                    "    import spacy\n"
                    "    nlp = spacy.load('en_core_web_sm')\n\n"
                    "    text = 'Apple Inc. was founded by Steve Jobs in Cupertino on April 1, 1976.'\n"
                    "    doc = nlp(text)\n\n"
                    "    print('Entities found:')\n"
                    "    for ent in doc.ents:\n"
                    "        print(f'  {ent.text:<25} {ent.label_:<12} {spacy.explain(ent.label_)}')\n"
                    "except OSError:\n"
                    "    print('Run: python -m spacy download en_core_web_sm')"
                )
            },
            {
                "label": "NER with NLTK chunking",
                "code": (
                    "import nltk\n"
                    "nltk.download('averaged_perceptron_tagger', quiet=True)\n"
                    "nltk.download('maxent_ne_chunker', quiet=True)\n"
                    "nltk.download('words', quiet=True)\n"
                    "nltk.download('punkt', quiet=True)\n"
                    "nltk.download('punkt_tab', quiet=True)\n"
                    "nltk.download('averaged_perceptron_tagger_eng', quiet=True)\n"
                    "from nltk import word_tokenize, pos_tag, ne_chunk\n"
                    "from nltk.tree import Tree\n\n"
                    "text = 'Barack Obama served as the 44th President of the United States.'\n"
                    "tokens = word_tokenize(text)\n"
                    "tagged = pos_tag(tokens)\n"
                    "chunks = ne_chunk(tagged)\n\n"
                    "for subtree in chunks:\n"
                    "    if isinstance(subtree, Tree):\n"
                    "        entity = ' '.join(word for word, tag in subtree.leaves())\n"
                    "        print(f'{entity}: {subtree.label()}')"
                )
            },
            {
                "label": "Visualizing entities with displacy",
                "code": (
                    "try:\n"
                    "    import spacy\n"
                    "    from spacy import displacy\n"
                    "    nlp = spacy.load('en_core_web_sm')\n\n"
                    "    text = 'Elon Musk founded SpaceX in Hawthorne, California in 2002.'\n"
                    "    doc = nlp(text)\n\n"
                    "    # In a Jupyter notebook this renders inline:\n"
                    "    # displacy.render(doc, style='ent')\n\n"
                    "    # Save to HTML:\n"
                    "    html = displacy.render(doc, style='ent', page=True)\n"
                    "    print(html[:200], '...')  # Show snippet\n"
                    "    print('\\nEntities:', [(e.text, e.label_) for e in doc.ents])\n"
                    "except OSError:\n"
                    "    print('Run: python -m spacy download en_core_web_sm')"
                )
            },
            {
                "label": "Custom NER with spaCy EntityRuler",
                "code": (
                    "try:\n"
                    "    import spacy\n"
                    "    nlp = spacy.load('en_core_web_sm')\n\n"
                    "    # Add custom entity patterns\n"
                    "    ruler = nlp.add_pipe('entity_ruler', before='ner')\n"
                    "    patterns = [\n"
                    "        {'label': 'TECH_STACK', 'pattern': 'Python'},\n"
                    "        {'label': 'TECH_STACK', 'pattern': 'TensorFlow'},\n"
                    "        {'label': 'TECH_STACK', 'pattern': [{'LOWER': 'scikit'}, {'LOWER': '-'}, {'LOWER': 'learn'}]},\n"
                    "    ]\n"
                    "    ruler.add_patterns(patterns)\n\n"
                    "    doc = nlp('We use Python and TensorFlow with scikit-learn for ML.')\n"
                    "    for ent in doc.ents:\n"
                    "        print(f'{ent.text}: {ent.label_}')\n"
                    "except OSError:\n"
                    "    print('Run: python -m spacy download en_core_web_sm')"
                )
            },
        ],
        "rw_scenario": "A financial news aggregator wants to automatically tag articles with mentioned companies, CEOs, and market figures to power a search index.",
        "rw_code": (
            "try:\n"
            "    import spacy\n"
            "    from collections import defaultdict\n"
            "    nlp = spacy.load('en_core_web_sm')\n\n"
            "    articles = [\n"
            "        'Tesla CEO Elon Musk announced record deliveries in Q4 2024.',\n"
            "        'Microsoft acquired Activision Blizzard for $68.7 billion.',\n"
            "        'Warren Buffett increased Berkshire Hathaway stake in Apple.',\n"
            "    ]\n\n"
            "    entity_index = defaultdict(list)\n"
            "    for i, art in enumerate(articles):\n"
            "        doc = nlp(art)\n"
            "        for ent in doc.ents:\n"
            "            if ent.label_ in ('ORG', 'PERSON', 'MONEY', 'DATE'):\n"
            "                entity_index[ent.text].append(i)\n\n"
            "    for entity, article_ids in entity_index.items():\n"
            "        print(f'{entity}: articles {article_ids}')\n"
            "except OSError:\n"
            "    print('Run: python -m spacy download en_core_web_sm')"
        ),
        "practice": {
            "title": "Entity Frequency Counter",
            "desc": "Process a list of news headlines, extract all PERSON and ORG entities, and return the top 5 most mentioned entities.",
            "starter": (
                "headlines = [\n"
                "    'Google CEO Sundar Pichai unveils new AI products at Google I/O',\n"
                "    'Apple and Google partner on health data standards',\n"
                "    'Jeff Bezos steps down as Amazon CEO',\n"
                "    'Amazon reports record profits under Andy Jassy',\n"
                "    'Sundar Pichai defends Google search monopoly in court',\n"
                "]\n\n"
                "def top_entities(texts, n=5):\n"
                "    # TODO: load spacy, extract PERSON + ORG entities\n"
                "    # TODO: count frequencies, return top n\n"
                "    pass\n\n"
                "print(top_entities(headlines))"
            )
        }
    },
    {
        "title": "5. Sentiment Analysis",
        "desc": "Determine whether text expresses positive, negative, or neutral sentiment. Learn rule-based (VADER), ML-based, and transformer approaches.",
        "examples": [
            {
                "label": "VADER sentiment (rule-based)",
                "code": (
                    "import nltk\n"
                    "nltk.download('vader_lexicon', quiet=True)\n"
                    "from nltk.sentiment.vader import SentimentIntensityAnalyzer\n\n"
                    "sia = SentimentIntensityAnalyzer()\n\n"
                    "texts = [\n"
                    "    'The food was absolutely amazing and the service was great!',\n"
                    "    'Terrible experience. Never going back.',\n"
                    "    'The product arrived on time.',\n"
                    "    'Not bad, but could be better.',\n"
                    "]\n\n"
                    "for text in texts:\n"
                    "    scores = sia.polarity_scores(text)\n"
                    "    label = 'POSITIVE' if scores['compound'] > 0.05 else 'NEGATIVE' if scores['compound'] < -0.05 else 'NEUTRAL'\n"
                    "    print(f'{label}: {text[:40]:<40} | compound={scores[\"compound\"]:.3f}')"
                )
            },
            {
                "label": "TextBlob sentiment",
                "code": (
                    "try:\n"
                    "    from textblob import TextBlob\n\n"
                    "    reviews = [\n"
                    "        'Absolutely love this product! Best purchase ever.',\n"
                    "        'Disappointed. Quality is poor and shipping was slow.',\n"
                    "        'It is okay. Nothing special.',\n"
                    "    ]\n\n"
                    "    for review in reviews:\n"
                    "        blob = TextBlob(review)\n"
                    "        pol = blob.sentiment.polarity       # -1 to 1\n"
                    "        sub = blob.sentiment.subjectivity   # 0 (objective) to 1 (subjective)\n"
                    "        print(f'Polarity: {pol:+.2f}  Subjectivity: {sub:.2f}  | {review[:40]}')\n"
                    "except ImportError:\n"
                    "    print('pip install textblob')"
                )
            },
            {
                "label": "Transformer-based sentiment with pipeline",
                "code": (
                    "try:\n"
                    "    from transformers import pipeline\n\n"
                    "    sentiment = pipeline('sentiment-analysis',\n"
                    "                         model='distilbert-base-uncased-finetuned-sst-2-english')\n\n"
                    "    texts = [\n"
                    "        'I love this movie so much!',\n"
                    "        'This is the worst product I have ever bought.',\n"
                    "        'The package arrived in reasonable time.',\n"
                    "    ]\n"
                    "    results = sentiment(texts)\n"
                    "    for text, result in zip(texts, results):\n"
                    "        print(f'{result[\"label\"]:<10} ({result[\"score\"]:.3f}): {text}')\n"
                    "except ImportError:\n"
                    "    print('pip install transformers torch')"
                )
            },
            {
                "label": "Aspect-based sentiment (simple rule approach)",
                "code": (
                    "import nltk\n"
                    "nltk.download('vader_lexicon', quiet=True)\n"
                    "from nltk.sentiment.vader import SentimentIntensityAnalyzer\n\n"
                    "sia = SentimentIntensityAnalyzer()\n\n"
                    "ASPECTS = {\n"
                    "    'battery': ['battery', 'charge', 'charging', 'power'],\n"
                    "    'camera':  ['camera', 'photo', 'picture', 'image'],\n"
                    "    'screen':  ['screen', 'display', 'resolution'],\n"
                    "}\n\n"
                    "def aspect_sentiment(review):\n"
                    "    results = {}\n"
                    "    sentences = nltk.sent_tokenize(review)\n"
                    "    for aspect, keywords in ASPECTS.items():\n"
                    "        relevant = [s for s in sentences if any(k in s.lower() for k in keywords)]\n"
                    "        if relevant:\n"
                    "            scores = [sia.polarity_scores(s)['compound'] for s in relevant]\n"
                    "            results[aspect] = sum(scores) / len(scores)\n"
                    "    return results\n\n"
                    "review = 'Battery life is excellent! But the camera quality is disappointing. The screen is stunning.'\n"
                    "print(aspect_sentiment(review))"
                )
            },
        ],
        "rw_scenario": "An e-commerce platform wants to automatically classify product reviews as positive/negative and flag negative ones for customer service follow-up.",
        "rw_code": (
            "import nltk\n"
            "nltk.download('vader_lexicon', quiet=True)\n"
            "from nltk.sentiment.vader import SentimentIntensityAnalyzer\n"
            "from dataclasses import dataclass\n"
            "from typing import List\n\n"
            "@dataclass\n"
            "class Review:\n"
            "    id: int\n"
            "    text: str\n"
            "    product_id: str\n\n"
            "sia = SentimentIntensityAnalyzer()\n\n"
            "def triage_reviews(reviews: List[Review]):\n"
            "    negative = []\n"
            "    for r in reviews:\n"
            "        score = sia.polarity_scores(r.text)['compound']\n"
            "        if score < -0.3:\n"
            "            negative.append((r, score))\n"
            "    return sorted(negative, key=lambda x: x[1])  # worst first\n\n"
            "reviews = [\n"
            "    Review(1, 'Love it! Works perfectly.', 'P001'),\n"
            "    Review(2, 'Completely broken. Total waste of money.', 'P002'),\n"
            "    Review(3, 'Item never arrived. Terrible service!', 'P003'),\n"
            "]\n"
            "flagged = triage_reviews(reviews)\n"
            "for review, score in flagged:\n"
            "    print(f'Review {review.id} (score={score:.3f}): {review.text}')"
        ),
        "practice": {
            "title": "Sentiment Dashboard",
            "desc": "Given a list of tweets, compute the daily average sentiment score and print a summary showing whether the day was overall positive or negative.",
            "starter": (
                "import nltk\n"
                "nltk.download('vader_lexicon', quiet=True)\n"
                "from nltk.sentiment.vader import SentimentIntensityAnalyzer\n\n"
                "tweets = [\n"
                "    ('2024-01-01', 'Great start to the new year! So excited!'),\n"
                "    ('2024-01-01', 'Traffic was awful this morning.'),\n"
                "    ('2024-01-02', 'Amazing concert last night!'),\n"
                "    ('2024-01-02', 'Concert tickets were overpriced but show was okay'),\n"
                "    ('2024-01-02', 'Best night ever, loved every minute!'),\n"
                "]\n\n"
                "def daily_sentiment(tweets):\n"
                "    sia = SentimentIntensityAnalyzer()\n"
                "    # TODO: group by date, average compound scores\n"
                "    # TODO: label each day as POSITIVE / NEGATIVE / NEUTRAL\n"
                "    pass\n\n"
                "daily_sentiment(tweets)"
            )
        }
    },
    {
        "title": "6. Text Similarity & Vectorization",
        "desc": "Convert text to numerical representations and measure similarity. Covers Bag-of-Words, TF-IDF, cosine similarity, and word embeddings.",
        "examples": [
            {
                "label": "TF-IDF vectorization with sklearn",
                "code": (
                    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                    "import pandas as pd\n\n"
                    "corpus = [\n"
                    "    'the cat sat on the mat',\n"
                    "    'the dog lay on the rug',\n"
                    "    'cats and dogs are both great pets',\n"
                    "]\n\n"
                    "vec = TfidfVectorizer(stop_words='english')\n"
                    "X = vec.fit_transform(corpus)\n\n"
                    "df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names_out())\n"
                    "print(df.round(3))"
                )
            },
            {
                "label": "Cosine similarity between documents",
                "code": (
                    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                    "from sklearn.metrics.pairwise import cosine_similarity\n"
                    "import numpy as np\n\n"
                    "docs = [\n"
                    "    'Python is great for data science',\n"
                    "    'Data science uses Python and R',\n"
                    "    'I love cooking Italian food',\n"
                    "    'Machine learning with Python and sklearn',\n"
                    "]\n\n"
                    "vec = TfidfVectorizer(stop_words='english')\n"
                    "X = vec.fit_transform(docs)\n"
                    "sim = cosine_similarity(X)\n\n"
                    "print('Similarity matrix:')\n"
                    "for i, row in enumerate(sim):\n"
                    "    print(f'Doc {i}: {[f\"{v:.2f}\" for v in row]}')"
                )
            },
            {
                "label": "Word2Vec embeddings with gensim",
                "code": (
                    "try:\n"
                    "    from gensim.models import Word2Vec\n"
                    "    import nltk\n"
                    "    nltk.download('punkt', quiet=True)\n"
                    "    nltk.download('punkt_tab', quiet=True)\n"
                    "    from nltk.tokenize import word_tokenize\n\n"
                    "    sentences = [\n"
                    "        'king is a powerful man',\n"
                    "        'queen is a powerful woman',\n"
                    "        'boy is a young man',\n"
                    "        'girl is a young woman',\n"
                    "    ]\n"
                    "    tokenized = [word_tokenize(s) for s in sentences]\n"
                    "    model = Word2Vec(tokenized, vector_size=50, window=3, min_count=1, epochs=100)\n\n"
                    "    # Classic word vector arithmetic\n"
                    "    result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'], topn=3)\n"
                    "    print('king + woman - man =', result)\n"
                    "    print('Similarity(king, queen):', model.wv.similarity('king', 'queen'))\n"
                    "except ImportError:\n"
                    "    print('pip install gensim')"
                )
            },
            {
                "label": "Sentence embeddings with sentence-transformers",
                "code": (
                    "try:\n"
                    "    from sentence_transformers import SentenceTransformer\n"
                    "    from sklearn.metrics.pairwise import cosine_similarity\n\n"
                    "    model = SentenceTransformer('all-MiniLM-L6-v2')\n\n"
                    "    sentences = [\n"
                    "        'A man is playing guitar.',\n"
                    "        'Someone is strumming a musical instrument.',\n"
                    "        'A cat is sitting on the couch.',\n"
                    "    ]\n\n"
                    "    embeddings = model.encode(sentences)\n"
                    "    sim = cosine_similarity(embeddings)\n\n"
                    "    print('Semantic similarity:')\n"
                    "    for i in range(len(sentences)):\n"
                    "        for j in range(i+1, len(sentences)):\n"
                    "            print(f'  [{i}] vs [{j}]: {sim[i,j]:.3f}')\n"
                    "except ImportError:\n"
                    "    print('pip install sentence-transformers')"
                )
            },
        ],
        "rw_scenario": "A legal tech company wants to find duplicate or near-duplicate contract clauses across thousands of documents to detect plagiarism.",
        "rw_code": (
            "from sklearn.feature_extraction.text import TfidfVectorizer\n"
            "from sklearn.metrics.pairwise import cosine_similarity\n"
            "import numpy as np\n\n"
            "clauses = [\n"
            "    'The contractor shall deliver all work by the agreed deadline.',\n"
            "    'All deliverables must be submitted by the agreed-upon deadline.',\n"
            "    'Payment shall be made within 30 days of invoice receipt.',\n"
            "    'The client agrees to pay within thirty days of receiving the invoice.',\n"
            "    'Confidential information must not be disclosed to third parties.',\n"
            "]\n\n"
            "vec = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')\n"
            "X = vec.fit_transform(clauses)\n"
            "sim = cosine_similarity(X)\n\n"
            "THRESHOLD = 0.5\n"
            "print('Near-duplicate pairs (similarity > 0.5):')\n"
            "for i in range(len(clauses)):\n"
            "    for j in range(i+1, len(clauses)):\n"
            "        if sim[i, j] > THRESHOLD:\n"
            "            print(f'  [{i}] & [{j}]: {sim[i,j]:.3f}')\n"
            "            print(f'    {clauses[i][:60]}')\n"
            "            print(f'    {clauses[j][:60]}')"
        ),
        "practice": {
            "title": "FAQ Matcher",
            "desc": "Build a simple FAQ bot: given a user question, find the most similar FAQ entry using TF-IDF cosine similarity.",
            "starter": (
                "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                "from sklearn.metrics.pairwise import cosine_similarity\n"
                "import numpy as np\n\n"
                "faqs = [\n"
                "    ('How do I reset my password?', 'Go to login page and click Forgot Password.'),\n"
                "    ('What payment methods are accepted?', 'We accept Visa, Mastercard and PayPal.'),\n"
                "    ('How long does shipping take?', 'Standard shipping takes 5-7 business days.'),\n"
                "    ('Can I return an item?', 'Yes, returns are accepted within 30 days.'),\n"
                "]\n\n"
                "def find_answer(question: str) -> str:\n"
                "    # TODO: vectorize FAQ questions + user question\n"
                "    # TODO: compute cosine similarity\n"
                "    # TODO: return answer for most similar FAQ\n"
                "    pass\n\n"
                "print(find_answer('How can I change my password?'))\n"
                "print(find_answer('Do you accept credit cards?'))"
            )
        }
    },
    {
        "title": "7. Topic Modeling",
        "desc": "Discover hidden thematic structure in document collections. Learn Latent Dirichlet Allocation (LDA) and Non-negative Matrix Factorization (NMF).",
        "examples": [
            {
                "label": "LDA topic modeling with sklearn",
                "code": (
                    "from sklearn.feature_extraction.text import CountVectorizer\n"
                    "from sklearn.decomposition import LatentDirichletAllocation\n"
                    "import numpy as np\n\n"
                    "docs = [\n"
                    "    'baseball team pitcher bat home run stadium',\n"
                    "    'football touchdown quarterback field goal referee',\n"
                    "    'stock market shares dividends portfolio investor',\n"
                    "    'bitcoin ethereum blockchain cryptocurrency wallet',\n"
                    "    'machine learning neural network deep learning AI',\n"
                    "    'python data science pandas numpy statistics',\n"
                    "]\n\n"
                    "vec = CountVectorizer(stop_words='english')\n"
                    "X = vec.fit_transform(docs)\n\n"
                    "lda = LatentDirichletAllocation(n_components=3, random_state=42)\n"
                    "lda.fit(X)\n\n"
                    "feature_names = vec.get_feature_names_out()\n"
                    "for i, topic in enumerate(lda.components_):\n"
                    "    top_words = [feature_names[j] for j in topic.argsort()[-6:][::-1]]\n"
                    "    print(f'Topic {i}: {top_words}')"
                )
            },
            {
                "label": "NMF topic modeling",
                "code": (
                    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                    "from sklearn.decomposition import NMF\n\n"
                    "docs = [\n"
                    "    'health fitness exercise gym workout training',\n"
                    "    'diet nutrition calories protein weight loss',\n"
                    "    'travel vacation flight hotel beach tourism',\n"
                    "    'passport visa travel destination adventure explore',\n"
                    "    'cooking recipe chef kitchen ingredients bake',\n"
                    "]\n\n"
                    "vec = TfidfVectorizer(stop_words='english', max_features=50)\n"
                    "X = vec.fit_transform(docs)\n\n"
                    "nmf = NMF(n_components=3, random_state=42)\n"
                    "W = nmf.fit_transform(X)\n"
                    "H = nmf.components_\n\n"
                    "feature_names = vec.get_feature_names_out()\n"
                    "for i, topic in enumerate(H):\n"
                    "    top_words = [feature_names[j] for j in topic.argsort()[-5:][::-1]]\n"
                    "    print(f'Topic {i}: {top_words}')\n\n"
                    "print('\\nDoc-topic assignments (W):')\n"
                    "for i, row in enumerate(W):\n"
                    "    print(f'Doc {i}: topic {row.argmax()}')"
                )
            },
            {
                "label": "Choosing number of topics with perplexity",
                "code": (
                    "from sklearn.feature_extraction.text import CountVectorizer\n"
                    "from sklearn.decomposition import LatentDirichletAllocation\n"
                    "import numpy as np\n\n"
                    "# Synthetic corpus\n"
                    "docs = (['python data science machine learning'] * 5 +\n"
                    "        ['football soccer game stadium team'] * 5 +\n"
                    "        ['stock market finance investment portfolio'] * 5)\n\n"
                    "vec = CountVectorizer(stop_words='english')\n"
                    "X = vec.fit_transform(docs)\n\n"
                    "perplexities = []\n"
                    "k_range = range(2, 7)\n"
                    "for k in k_range:\n"
                    "    lda = LatentDirichletAllocation(n_components=k, random_state=42, max_iter=20)\n"
                    "    lda.fit(X)\n"
                    "    perplexities.append(lda.perplexity(X))\n"
                    "    print(f'k={k}: perplexity={lda.perplexity(X):.2f}')\n\n"
                    "best_k = k_range[np.argmin(perplexities)]\n"
                    "print(f'Best k: {best_k}')"
                )
            },
            {
                "label": "Assigning topic labels to new documents",
                "code": (
                    "from sklearn.feature_extraction.text import CountVectorizer\n"
                    "from sklearn.decomposition import LatentDirichletAllocation\n"
                    "import numpy as np\n\n"
                    "train_docs = [\n"
                    "    'python programming code software developer',\n"
                    "    'machine learning model training dataset',\n"
                    "    'basketball players championship game team',\n"
                    "    'tennis grand slam tournament court player',\n"
                    "]\n"
                    "TOPIC_LABELS = {0: 'Technology', 1: 'Sports'}  # manual labels\n\n"
                    "vec = CountVectorizer(stop_words='english')\n"
                    "X_train = vec.fit_transform(train_docs)\n\n"
                    "lda = LatentDirichletAllocation(n_components=2, random_state=42)\n"
                    "lda.fit(X_train)\n\n"
                    "new_docs = [\n"
                    "    'neural network deep learning GPU training',\n"
                    "    'football touchdown quarterback Super Bowl',\n"
                    "]\n"
                    "X_new = vec.transform(new_docs)\n"
                    "topic_dist = lda.transform(X_new)\n"
                    "for doc, dist in zip(new_docs, topic_dist):\n"
                    "    label = TOPIC_LABELS.get(dist.argmax(), f'Topic {dist.argmax()}')\n"
                    "    print(f'{doc[:40]} -> {label} ({dist.max():.2f})')"
                )
            },
        ],
        "rw_scenario": "A news publisher wants to automatically tag and categorize thousands of articles by topic to power content recommendations.",
        "rw_code": (
            "from sklearn.feature_extraction.text import CountVectorizer\n"
            "from sklearn.decomposition import LatentDirichletAllocation\n"
            "import numpy as np\n\n"
            "articles = [\n"
            "    'The government announced new climate change policy and carbon tax.',\n"
            "    'Scientists discover breakthrough in quantum computing research.',\n"
            "    'Stock markets rally as tech earnings exceed expectations.',\n"
            "    'Premier League clubs prepare for summer transfer window.',\n"
            "    'AI startup raises $500M for large language model development.',\n"
            "    'Central bank raises interest rates to fight inflation.',\n"
            "]\n\n"
            "TOPIC_NAMES = ['Politics/Environment', 'Technology/Science', 'Finance', 'Sports']\n\n"
            "vec = CountVectorizer(stop_words='english', min_df=1)\n"
            "X = vec.fit_transform(articles)\n\n"
            "lda = LatentDirichletAllocation(n_components=4, random_state=42)\n"
            "lda.fit(X)\n\n"
            "topic_dist = lda.transform(X)\n"
            "for article, dist in zip(articles, topic_dist):\n"
            "    dominant = dist.argmax()\n"
            "    print(f'{TOPIC_NAMES[dominant]}: {article[:55]}')"
        ),
        "practice": {
            "title": "Customer Feedback Topics",
            "desc": "Apply LDA to a dataset of customer feedback comments and print the top 5 words for each discovered topic.",
            "starter": (
                "from sklearn.feature_extraction.text import CountVectorizer\n"
                "from sklearn.decomposition import LatentDirichletAllocation\n\n"
                "feedback = [\n"
                "    'Delivery was fast and packaging was excellent',\n"
                "    'Shipping took too long and package was damaged',\n"
                "    'Customer support was very helpful and responsive',\n"
                "    'Support team was rude and unhelpful',\n"
                "    'Product quality is amazing, well made and durable',\n"
                "    'The product broke after one week, poor quality',\n"
                "    'Price is reasonable for the quality you get',\n"
                "    'Very expensive for what it is, not worth the money',\n"
                "]\n\n"
                "def model_topics(docs, n_topics=3):\n"
                "    # TODO: CountVectorizer -> LDA -> print top words per topic\n"
                "    pass\n\n"
                "model_topics(feedback)"
            )
        }
    },
    {
        "title": "8. Text Classification",
        "desc": "Train models to classify text into categories. Covers Naive Bayes, Logistic Regression, and transformer-based fine-tuning pipelines.",
        "examples": [
            {
                "label": "Spam detection with Naive Bayes",
                "code": (
                    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                    "from sklearn.naive_bayes import MultinomialNB\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.metrics import classification_report\n\n"
                    "# Minimal spam dataset\n"
                    "texts = [\n"
                    "    'Win a FREE iPhone now! Click here!!!', 'URGENT: You have won $1000',\n"
                    "    'Claim your prize today, limited offer!', 'Hot singles in your area',\n"
                    "    'Meeting at 3pm in the conference room', 'Can you review my pull request?',\n"
                    "    'Lunch tomorrow? Let me know.', 'Project deadline is Friday.',\n"
                    "    'Budget report attached for your review', 'Hi, are you free this afternoon?',\n"
                    "]\n"
                    "labels = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]  # 1=spam, 0=ham\n\n"
                    "X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)\n\n"
                    "clf = Pipeline([('tfidf', TfidfVectorizer()), ('nb', MultinomialNB())])\n"
                    "clf.fit(X_train, y_train)\n"
                    "print(classification_report(y_test, clf.predict(X_test), target_names=['ham', 'spam']))"
                )
            },
            {
                "label": "Multi-class classification with Logistic Regression",
                "code": (
                    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "import numpy as np\n\n"
                    "texts = [\n"
                    "    'The stock market crashed today', 'Interest rates affect mortgages',\n"
                    "    'Champions League final tonight', 'NBA playoffs heating up',\n"
                    "    'New deep learning model released', 'Python 4.0 features announced',\n"
                    "    'Election results pending', 'Senate votes on new bill',\n"
                    "]\n"
                    "labels = ['finance','finance','sports','sports','tech','tech','politics','politics']\n\n"
                    "pipe = Pipeline([\n"
                    "    ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),\n"
                    "    ('lr',   LogisticRegression(max_iter=200))\n"
                    "])\n"
                    "scores = cross_val_score(pipe, texts, labels, cv=2, scoring='accuracy')\n"
                    "print(f'CV accuracy: {scores.mean():.2f} ± {scores.std():.2f}')\n\n"
                    "pipe.fit(texts, labels)\n"
                    "print(pipe.predict(['Bitcoin surges to all-time high']))"
                )
            },
            {
                "label": "Zero-shot classification with transformers",
                "code": (
                    "try:\n"
                    "    from transformers import pipeline\n\n"
                    "    classifier = pipeline('zero-shot-classification',\n"
                    "                          model='facebook/bart-large-mnli')\n\n"
                    "    texts = [\n"
                    "        'The Federal Reserve raises interest rates by 25 basis points.',\n"
                    "        'Team wins championship after dramatic overtime goal.',\n"
                    "        'New AI model achieves human-level performance on benchmark.',\n"
                    "    ]\n"
                    "    candidate_labels = ['finance', 'sports', 'technology', 'politics']\n\n"
                    "    for text in texts:\n"
                    "        result = classifier(text, candidate_labels)\n"
                    "        print(f'{result[\"labels\"][0]:12} ({result[\"scores\"][0]:.2f}): {text[:50]}')\n"
                    "except ImportError:\n"
                    "    print('pip install transformers torch')"
                )
            },
            {
                "label": "Feature importance for text classifiers",
                "code": (
                    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "import numpy as np\n\n"
                    "texts = [\n"
                    "    'stock market bull bear portfolio dividends',\n"
                    "    'goal touchdown home run stadium championship',\n"
                    "    'algorithm neural network training dataset model',\n"
                    "    'vote senator election campaign policy',\n"
                    "] * 3\n"
                    "labels = ['finance','sports','tech','politics'] * 3\n\n"
                    "pipe = Pipeline([('tfidf', TfidfVectorizer()), ('lr', LogisticRegression(max_iter=200))])\n"
                    "pipe.fit(texts, labels)\n\n"
                    "feature_names = pipe['tfidf'].get_feature_names_out()\n"
                    "classes = pipe['lr'].classes_\n\n"
                    "for cls, coef in zip(classes, pipe['lr'].coef_):\n"
                    "    top = [feature_names[i] for i in coef.argsort()[-5:][::-1]]\n"
                    "    print(f'{cls}: {top}')"
                )
            },
        ],
        "rw_scenario": "A news website wants to automatically route incoming press releases to the correct editorial desk (Finance, Sports, Tech, Politics) without human triage.",
        "rw_code": (
            "from sklearn.feature_extraction.text import TfidfVectorizer\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.pipeline import Pipeline\n\n"
            "training_data = [\n"
            "    ('Company reports record quarterly earnings', 'finance'),\n"
            "    ('Inflation rises as central bank meets', 'finance'),\n"
            "    ('National team advances to World Cup final', 'sports'),\n"
            "    ('Olympic gold medal for marathon runner', 'sports'),\n"
            "    ('New open-source large language model released', 'tech'),\n"
            "    ('Semiconductor company launches AI chip', 'tech'),\n"
            "    ('Prime minister announces cabinet reshuffle', 'politics'),\n"
            "    ('Senate approves infrastructure spending bill', 'politics'),\n"
            "]\n\n"
            "texts, labels = zip(*training_data)\n\n"
            "router = Pipeline([\n"
            "    ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),\n"
            "    ('lr',   LogisticRegression(max_iter=500))\n"
            "])\n"
            "router.fit(texts, labels)\n\n"
            "press_releases = [\n"
            "    'Startup raises $200M Series C for AI research',\n"
            "    'Tennis star wins fourth Grand Slam title',\n"
            "]\n"
            "for pr in press_releases:\n"
            "    desk = router.predict([pr])[0]\n"
            "    proba = router.predict_proba([pr]).max()\n"
            "    print(f'{desk.upper()} ({proba:.0%}): {pr}')"
        ),
        "practice": {
            "title": "Review Sentiment Classifier",
            "desc": "Train a TF-IDF + Logistic Regression classifier to predict star rating buckets (1-2=negative, 3=neutral, 4-5=positive) from review text.",
            "starter": (
                "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.pipeline import Pipeline\n"
                "from sklearn.model_selection import train_test_split\n\n"
                "reviews = [\n"
                "    ('Absolutely fantastic product, highly recommend!', 'positive'),\n"
                "    ('Life changing purchase, best I have ever made', 'positive'),\n"
                "    ('Pretty good but not perfect', 'neutral'),\n"
                "    ('Does the job, nothing special', 'neutral'),\n"
                "    ('Broken on arrival, terrible quality', 'negative'),\n"
                "    ('Complete waste of money, do not buy', 'negative'),\n"
                "    ('Great value for money, very happy', 'positive'),\n"
                "    ('Disappointed, expected much better', 'negative'),\n"
                "]\n\n"
                "texts, labels = zip(*reviews)\n"
                "X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)\n\n"
                "# TODO: build Pipeline with TfidfVectorizer + LogisticRegression\n"
                "# TODO: fit, predict, print classification_report"
            )
        }
    },
    {
        "title": "9. Language Models & Transformers",
        "desc": "Understand transformer architecture, use pre-trained BERT/GPT models for embeddings, question answering, and text generation.",
        "examples": [
            {
                "label": "BERT embeddings for semantic search",
                "code": (
                    "try:\n"
                    "    from transformers import AutoTokenizer, AutoModel\n"
                    "    import torch\n"
                    "    import torch.nn.functional as F\n\n"
                    "    model_name = 'bert-base-uncased'\n"
                    "    tokenizer = AutoTokenizer.from_pretrained(model_name)\n"
                    "    model = AutoModel.from_pretrained(model_name)\n\n"
                    "    def get_embedding(text):\n"
                    "        inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=128)\n"
                    "        with torch.no_grad():\n"
                    "            outputs = model(**inputs)\n"
                    "        return outputs.last_hidden_state[:, 0, :].squeeze()  # [CLS] token\n\n"
                    "    s1 = get_embedding('How do I reset my password?')\n"
                    "    s2 = get_embedding('Steps to change account password')\n"
                    "    s3 = get_embedding('Best pizza recipe')\n\n"
                    "    print('s1 vs s2:', F.cosine_similarity(s1.unsqueeze(0), s2.unsqueeze(0)).item())\n"
                    "    print('s1 vs s3:', F.cosine_similarity(s1.unsqueeze(0), s3.unsqueeze(0)).item())\n"
                    "except ImportError:\n"
                    "    print('pip install transformers torch')"
                )
            },
            {
                "label": "Question answering with a pipeline",
                "code": (
                    "try:\n"
                    "    from transformers import pipeline\n\n"
                    "    qa = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')\n\n"
                    "    context = '''\n"
                    "    Python was created by Guido van Rossum and first released in 1991.\n"
                    "    It was designed with an emphasis on code readability and simplicity.\n"
                    "    Python supports multiple programming paradigms including procedural,\n"
                    "    object-oriented, and functional programming.\n"
                    "    '''\n\n"
                    "    questions = [\n"
                    "        'Who created Python?',\n"
                    "        'When was Python first released?',\n"
                    "        'What paradigms does Python support?',\n"
                    "    ]\n"
                    "    for q in questions:\n"
                    "        answer = qa({'question': q, 'context': context})\n"
                    "        print(f'Q: {q}')\n"
                    "        print(f'A: {answer[\"answer\"]} (score: {answer[\"score\"]:.3f})\\n')\n"
                    "except ImportError:\n"
                    "    print('pip install transformers torch')"
                )
            },
            {
                "label": "Text generation with GPT-2",
                "code": (
                    "try:\n"
                    "    from transformers import pipeline\n\n"
                    "    generator = pipeline('text-generation', model='gpt2', max_new_tokens=80)\n\n"
                    "    prompts = [\n"
                    "        'The future of artificial intelligence is',\n"
                    "        'Data science has transformed the way we',\n"
                    "    ]\n"
                    "    for prompt in prompts:\n"
                    "        result = generator(prompt, num_return_sequences=1, do_sample=True, temperature=0.7)\n"
                    "        print(f'Prompt: {prompt}')\n"
                    "        print(f'Generated: {result[0][\"generated_text\"]}\\n')\n"
                    "except ImportError:\n"
                    "    print('pip install transformers torch')"
                )
            },
            {
                "label": "Fine-tuning BERT for classification (skeleton)",
                "code": (
                    "try:\n"
                    "    from transformers import AutoTokenizer, AutoModelForSequenceClassification\n"
                    "    from transformers import TrainingArguments, Trainer\n"
                    "    import torch\n\n"
                    "    model_name = 'distilbert-base-uncased'\n"
                    "    tokenizer = AutoTokenizer.from_pretrained(model_name)\n"
                    "    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)\n\n"
                    "    # Example: tokenize a batch\n"
                    "    texts = ['I love this product!', 'Terrible experience.']\n"
                    "    labels = [1, 0]\n"
                    "    encodings = tokenizer(texts, truncation=True, padding=True, return_tensors='pt')\n\n"
                    "    # In real fine-tuning, wrap in a Dataset and use Trainer:\n"
                    "    # training_args = TrainingArguments(output_dir='./results', num_train_epochs=3)\n"
                    "    # trainer = Trainer(model=model, args=training_args, ...)\n"
                    "    # trainer.train()\n\n"
                    "    print('Model ready for fine-tuning')\n"
                    "    print('Tokenized input_ids shape:', encodings['input_ids'].shape)\n"
                    "except ImportError:\n"
                    "    print('pip install transformers torch datasets')"
                )
            },
        ],
        "rw_scenario": "A SaaS company wants to build an internal knowledge base Q&A bot that finds answers from company documentation using semantic search.",
        "rw_code": (
            "try:\n"
            "    from sentence_transformers import SentenceTransformer\n"
            "    from sklearn.metrics.pairwise import cosine_similarity\n"
            "    import numpy as np\n\n"
            "    model = SentenceTransformer('all-MiniLM-L6-v2')\n\n"
            "    # Knowledge base documents\n"
            "    kb = [\n"
            "        {'q': 'How do I reset my password?',\n"
            "         'a': 'Go to Settings > Security > Reset Password and enter your email.'},\n"
            "        {'q': 'What is the refund policy?',\n"
            "         'a': 'Refunds are processed within 5-7 business days of approval.'},\n"
            "        {'q': 'How do I cancel my subscription?',\n"
            "         'a': 'Navigate to Billing > Subscription > Cancel Subscription.'},\n"
            "    ]\n\n"
            "    kb_embeddings = model.encode([item['q'] for item in kb])\n\n"
            "    def answer_question(user_q: str):\n"
            "        q_emb = model.encode([user_q])\n"
            "        sims = cosine_similarity(q_emb, kb_embeddings)[0]\n"
            "        best = sims.argmax()\n"
            "        return kb[best]['a'], sims[best]\n\n"
            "    for question in ['Change my account password', 'Get money back for purchase']:\n"
            "        answer, conf = answer_question(question)\n"
            "        print(f'Q: {question}')\n"
            "        print(f'A: {answer} (confidence: {conf:.2f})\\n')\n"
            "except ImportError:\n"
            "    print('pip install sentence-transformers')"
        ),
        "practice": {
            "title": "Summarizer Pipeline",
            "desc": "Use a HuggingFace summarization pipeline to condense a long article into a 2-sentence summary and compare the word count reduction.",
            "starter": (
                "try:\n"
                "    from transformers import pipeline\n\n"
                "    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')\n\n"
                "    article = '''\n"
                "    Artificial intelligence has made remarkable progress over the past decade.\n"
                "    Large language models like GPT-4 and Claude can now generate coherent text,\n"
                "    answer complex questions, write code, and even reason about abstract problems.\n"
                "    These models are trained on vast amounts of internet text using self-supervised\n"
                "    learning, allowing them to develop broad world knowledge. However, challenges\n"
                "    remain around hallucination, bias, and alignment with human values. Researchers\n"
                "    continue to work on making these systems safer and more reliable.\n"
                "    '''\n\n"
                "    # TODO: use summarizer to generate a short summary (max_length=60)\n"
                "    # TODO: print original word count vs summary word count\n\n"
                "except ImportError:\n"
                "    print('pip install transformers torch')"
            )
        }
    },
    {
        "title": "10. NLP Pipeline & Production",
        "desc": "Combine NLP components into production-ready pipelines. Learn batching, caching, serving NLP models via API, and evaluation metrics.",
        "examples": [
            {
                "label": "End-to-end spaCy text analysis pipeline",
                "code": (
                    "try:\n"
                    "    import spacy\n"
                    "    from collections import Counter\n"
                    "    nlp = spacy.load('en_core_web_sm')\n\n"
                    "    def analyze_text(text: str) -> dict:\n"
                    "        doc = nlp(text)\n"
                    "        return {\n"
                    "            'word_count': len([t for t in doc if not t.is_punct]),\n"
                    "            'sentences':  len(list(doc.sents)),\n"
                    "            'entities':   [(e.text, e.label_) for e in doc.ents],\n"
                    "            'top_nouns':  Counter(t.lemma_ for t in doc if t.pos_ == 'NOUN').most_common(3),\n"
                    "            'top_verbs':  Counter(t.lemma_ for t in doc if t.pos_ == 'VERB').most_common(3),\n"
                    "        }\n\n"
                    "    text = 'Elon Musk launched SpaceX rockets in 2020. Tesla reported record profits in Q4.'\n"
                    "    result = analyze_text(text)\n"
                    "    for k, v in result.items():\n"
                    "        print(f'{k}: {v}')\n"
                    "except OSError:\n"
                    "    print('Run: python -m spacy download en_core_web_sm')"
                )
            },
            {
                "label": "Batch processing with nlp.pipe for efficiency",
                "code": (
                    "try:\n"
                    "    import spacy\n"
                    "    import time\n"
                    "    nlp = spacy.load('en_core_web_sm')\n\n"
                    "    texts = [f'Document {i}: Apple and Google are tech giants in Silicon Valley.' for i in range(50)]\n\n"
                    "    # Sequential processing\n"
                    "    t0 = time.time()\n"
                    "    results_seq = [nlp(t) for t in texts]\n"
                    "    t_seq = time.time() - t0\n\n"
                    "    # Batch processing with nlp.pipe\n"
                    "    t0 = time.time()\n"
                    "    results_batch = list(nlp.pipe(texts, batch_size=16))\n"
                    "    t_batch = time.time() - t0\n\n"
                    "    print(f'Sequential: {t_seq:.3f}s')\n"
                    "    print(f'Batch pipe: {t_batch:.3f}s')\n"
                    "    print(f'Speedup: {t_seq/t_batch:.1f}x')\n"
                    "except OSError:\n"
                    "    print('Run: python -m spacy download en_core_web_sm')"
                )
            },
            {
                "label": "Serving NLP via FastAPI",
                "code": (
                    "# Run with: uvicorn app:app --reload\n"
                    "# pip install fastapi uvicorn\n\n"
                    "FASTAPI_APP = '''\n"
                    "from fastapi import FastAPI\n"
                    "from pydantic import BaseModel\n"
                    "import nltk\n"
                    "nltk.download(\"vader_lexicon\", quiet=True)\n"
                    "from nltk.sentiment.vader import SentimentIntensityAnalyzer\n\n"
                    "app = FastAPI()\n"
                    "sia = SentimentIntensityAnalyzer()\n\n"
                    "class TextRequest(BaseModel):\n"
                    "    text: str\n\n"
                    "@app.post(\"/sentiment\")\n"
                    "def analyze_sentiment(req: TextRequest):\n"
                    "    scores = sia.polarity_scores(req.text)\n"
                    "    label = \"positive\" if scores[\"compound\"] > 0.05 else \"negative\" if scores[\"compound\"] < -0.05 else \"neutral\"\n"
                    "    return {\"label\": label, \"scores\": scores}\n\n"
                    "@app.get(\"/health\")\n"
                    "def health():\n"
                    "    return {\"status\": \"ok\"}\n"
                    "'''\n\n"
                    "print(FASTAPI_APP)"
                )
            },
            {
                "label": "Evaluation: precision, recall, F1 for NER",
                "code": (
                    "from sklearn.metrics import precision_recall_fscore_support, classification_report\n\n"
                    "# BIO tagging evaluation example\n"
                    "# True entity spans vs predicted entity spans\n"
                    "true_entities = [\n"
                    "    {('Apple', 'ORG'), ('Tim Cook', 'PERSON'), ('Cupertino', 'GPE')},\n"
                    "    {('Google', 'ORG'), ('Sundar Pichai', 'PERSON')},\n"
                    "]\n"
                    "pred_entities = [\n"
                    "    {('Apple', 'ORG'), ('Tim Cook', 'PERSON')},     # missed Cupertino\n"
                    "    {('Google', 'ORG'), ('Sundar Pichai', 'PERSON'), ('Mountain View', 'GPE')},  # extra FP\n"
                    "]\n\n"
                    "def ner_metrics(true_list, pred_list):\n"
                    "    tp = sum(len(t & p) for t, p in zip(true_list, pred_list))\n"
                    "    fp = sum(len(p - t) for t, p in zip(true_list, pred_list))\n"
                    "    fn = sum(len(t - p) for t, p in zip(true_list, pred_list))\n"
                    "    prec = tp / (tp + fp) if tp + fp > 0 else 0\n"
                    "    rec  = tp / (tp + fn) if tp + fn > 0 else 0\n"
                    "    f1   = 2 * prec * rec / (prec + rec) if prec + rec > 0 else 0\n"
                    "    return {'precision': prec, 'recall': rec, 'f1': f1}\n\n"
                    "print(ner_metrics(true_entities, pred_entities))"
                )
            },
        ],
        "rw_scenario": "A media monitoring company processes 10,000+ news articles daily. They need a batch NLP pipeline that extracts entities, classifies topics, and stores results in a structured format.",
        "rw_code": (
            "try:\n"
            "    import spacy\n"
            "    from sklearn.feature_extraction.text import TfidfVectorizer\n"
            "    from sklearn.linear_model import LogisticRegression\n"
            "    from sklearn.pipeline import Pipeline\n"
            "    import json\n\n"
            "    nlp = spacy.load('en_core_web_sm')\n\n"
            "    # Train topic classifier\n"
            "    train_texts = [\n"
            "        'stock market profits earnings', 'championship game score',\n"
            "        'AI model research launch',    'election vote policy senator',\n"
            "    ]\n"
            "    train_labels = ['finance', 'sports', 'tech', 'politics']\n"
            "    topic_clf = Pipeline([('tfidf', TfidfVectorizer()), ('lr', LogisticRegression())])\n"
            "    topic_clf.fit(train_texts, train_labels)\n\n"
            "    def process_article(text: str) -> dict:\n"
            "        doc = nlp(text)\n"
            "        topic = topic_clf.predict([text])[0]\n"
            "        return {\n"
            "            'topic': topic,\n"
            "            'entities': [(e.text, e.label_) for e in doc.ents],\n"
            "            'word_count': len([t for t in doc if not t.is_punct]),\n"
            "        }\n\n"
            "    articles = [\n"
            "        'Tesla stock surges after record Q4 earnings report.',\n"
            "        'Manchester City wins Premier League with last-minute goal.',\n"
            "    ]\n"
            "    results = list(nlp.pipe(articles))  # batch NER\n"
            "    for text, doc in zip(articles, results):\n"
            "        topic = topic_clf.predict([text])[0]\n"
            "        print(json.dumps({'text': text[:40], 'topic': topic,\n"
            "                          'entities': [(e.text, e.label_) for e in doc.ents]}, indent=2))\n"
            "except OSError:\n"
            "    print('Run: python -m spacy download en_core_web_sm')"
        ),
        "practice": {
            "title": "Text Analytics Report",
            "desc": "Build a function that takes a list of documents and returns a JSON report with: total word count, unique entities, top 5 keywords (TF-IDF), and dominant sentiment.",
            "starter": (
                "import nltk\n"
                "nltk.download('vader_lexicon', quiet=True)\n"
                "from nltk.sentiment.vader import SentimentIntensityAnalyzer\n"
                "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                "import numpy as np, json\n\n"
                "documents = [\n"
                "    'Apple launches revolutionary new iPhone with AI features.',\n"
                "    'Google DeepMind achieves breakthrough in protein folding.',\n"
                "    'Microsoft Azure reports 40% growth in cloud services revenue.',\n"
                "]\n\n"
                "def analytics_report(docs: list) -> dict:\n"
                "    sia = SentimentIntensityAnalyzer()\n"
                "    # TODO: compute total word count\n"
                "    # TODO: extract top 5 TF-IDF keywords\n"
                "    # TODO: compute average sentiment label\n"
                "    # TODO: return as dict\n"
                "    pass\n\n"
                "print(json.dumps(analytics_report(documents), indent=2))"
            )
        }
    },
    {
        "title": "11. Information Extraction",
        "desc": "Extract structured facts from unstructured text: named entities, relations, events, and key-value pairs using rule-based and model-based approaches.",
        "examples": [
            {
                "label": "Regex-based relation extraction",
                "code": "import re\n\ntext = '''\nElon Musk founded SpaceX in 2002. Jeff Bezos founded Amazon in 1994.\nTim Cook joined Apple in 1998 and became CEO in 2011.\nSam Altman was appointed CEO of OpenAI in 2019.\n'''\n\n# Pattern: Person + founded/joined/became + Org + in + Year\nfounded_pat = re.compile(\n    r'([A-Z][a-z]+ [A-Z][a-z]+) (founded|joined|became \\w+) ([A-Z][a-zA-Z]+) in (\\d{4})'\n)\n\nrelations = []\nfor m in founded_pat.finditer(text):\n    relations.append({\n        'person': m.group(1),\n        'relation': m.group(2),\n        'org': m.group(3),\n        'year': m.group(4)\n    })\n\nfor r in relations:\n    print(f\"{r['person']} --[{r['relation']}]--> {r['org']} ({r['year']})\")"
            },
            {
                "label": "spaCy NER + dependency parsing for relations",
                "code": "try:\n    import spacy\n    nlp = spacy.load('en_core_web_sm')\n    text = 'Apple acquired Beats Electronics for 3 billion dollars in 2014. Google bought YouTube in 2006.'\n    doc = nlp(text)\n    print('Named Entities:')\n    for ent in doc.ents:\n        print(f'  {ent.text!r:25s} -> {ent.label_}')\n    print('\\nAcquisition relations (nsubj + dobj pattern):')\n    for token in doc:\n        if token.lemma_ in ('acquire', 'buy', 'purchase'):\n            subj = [t.text for t in token.lefts  if t.dep_ in ('nsubj', 'nsubjpass')]\n            obj  = [t.text for t in token.rights if t.dep_ in ('dobj', 'attr')]\n            if subj and obj:\n                print(f'  {subj[0]} --[{token.text}]--> {obj[0]}')\nexcept OSError:\n    print('Run: python -m spacy download en_core_web_sm')"
            },
            {
                "label": "Template-based information extraction with regex groups",
                "code": "import re\nfrom dataclasses import dataclass, field\nfrom typing import List\n\n@dataclass\nclass JobPosting:\n    title: str = ''\n    company: str = ''\n    location: str = ''\n    salary: str = ''\n    skills: List[str] = field(default_factory=list)\n\ndef extract_job_info(text: str) -> JobPosting:\n    job = JobPosting()\n    if m := re.search(r'(?:Title|Position|Role):\\s*(.+)', text, re.I): job.title = m.group(1).strip()\n    if m := re.search(r'Company:\\s*(.+)', text, re.I): job.company = m.group(1).strip()\n    if m := re.search(r'Location:\\s*(.+)', text, re.I): job.location = m.group(1).strip()\n    if m := re.search(r'Salary:\\s*(\\$[\\d,]+ ?- ?\\$[\\d,]+|\\$[\\d,]+)', text, re.I): job.salary = m.group(1)\n    skills_m = re.findall(r'\\b(Python|SQL|Java|TensorFlow|PyTorch|Docker|Kubernetes|AWS|GCP)\\b', text)\n    job.skills = list(set(skills_m))\n    return job\n\nposting = '''\nTitle: Senior Data Scientist\nCompany: TechCorp Inc.\nLocation: San Francisco, CA\nSalary: $150,000 - $200,000\nRequirements: Python, SQL, TensorFlow, Docker, AWS experience preferred.\n'''\njob = extract_job_info(posting)\nprint(f'Title:    {job.title}')\nprint(f'Company:  {job.company}')\nprint(f'Location: {job.location}')\nprint(f'Salary:   {job.salary}')\nprint(f'Skills:   {sorted(job.skills)}')"
            },
            {
                "label": "Event extraction with keyword triggers",
                "code": "import re\nfrom collections import defaultdict\n\n# Simple event extraction using trigger words\nEVENT_TRIGGERS = {\n    'acquisition': ['acquired', 'bought', 'purchased', 'merged with', 'took over'],\n    'funding':     ['raised', 'secured', 'received funding', 'closed round'],\n    'launch':      ['launched', 'released', 'unveiled', 'announced', 'introduced'],\n    'partnership': ['partnered', 'collaborated', 'teamed up', 'joined forces'],\n}\n\nMONEY_RE = re.compile(r'\\$[\\d.,]+[BMK]?\\s*(?:billion|million|thousand)?', re.I)\n\ndef extract_events(sentences):\n    events = []\n    for sent in sentences:\n        sent_lower = sent.lower()\n        for etype, triggers in EVENT_TRIGGERS.items():\n            for trig in triggers:\n                if trig in sent_lower:\n                    money = MONEY_RE.findall(sent)\n                    events.append({'type': etype, 'trigger': trig, 'money': money, 'text': sent[:80]})\n                    break\n    return events\n\nnews = [\n    'Google acquired DeepMind for $500 million in 2014.',\n    'OpenAI raised $6.6 billion in its latest funding round.',\n    'Apple launched its Vision Pro headset at WWDC 2023.',\n    'Meta and Microsoft partnered on enterprise AI solutions.',\n]\nfor ev in extract_events(news):\n    print(f\"[{ev['type'].upper()}] trigger='{ev['trigger']}' money={ev['money']}\")\n    print(f\"  {ev['text']}\")"
            }
        ],
        "rw_scenario": "A legal tech company needs to extract contract metadata (parties, dates, amounts, obligations) from thousands of PDF contracts to populate a contract management system automatically.",
        "rw_code": "import re\nfrom typing import Optional\n\ndef extract_contract_metadata(text: str) -> dict:\n    result = {}\n    # Party extraction: 'between X and Y'\n    party_m = re.search(r'between\\s+([^,]+?)\\s+and\\s+([^,\\.]+)', text, re.I)\n    if party_m:\n        result['party_1'] = party_m.group(1).strip()\n        result['party_2'] = party_m.group(2).strip()\n    # Date extraction\n    date_m = re.findall(r'\\b(\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \\d{1,2},? \\d{4})\\b', text, re.I)\n    result['dates'] = date_m[:3]\n    # Amount extraction\n    amounts = re.findall(r'\\$[\\d,]+(?:\\.\\d{2})?(?:\\s*(?:million|billion|thousand))?', text, re.I)\n    result['amounts'] = amounts\n    # Obligation keywords\n    obligations = re.findall(r'\\b(shall|must|will|agrees to|is required to)\\b', text, re.I)\n    result['obligation_count'] = len(obligations)\n    return result\n\ncontract = '''\nThis agreement is entered into between Acme Corporation and Beta Ltd.\nEffective January 15, 2024. The total value is $500,000.00.\nAcme shall deliver the software by March 31, 2024.\nBeta must pay within 30 days of invoice.\n'''\nprint(extract_contract_metadata(contract))",
        "practice": {
            "title": "Resume Information Extractor",
            "desc": "Write a function that extracts key resume fields from raw text: name (first line), email, phone, years of experience (parse 'X years' patterns), and programming languages mentioned from a predefined list. Test it on a sample resume string.",
            "starter": (
                "import re\n\n"
                "LANGUAGES = ['Python', 'Java', 'C++', 'JavaScript', 'SQL', 'R', 'Go', 'Rust', 'Scala']\n\n"
                "def extract_resume(text: str) -> dict:\n"
                "    # TODO: extract name (first non-empty line)\n"
                "    # TODO: extract email\n"
                "    # TODO: extract phone\n"
                "    # TODO: extract years of experience\n"
                "    # TODO: extract mentioned programming languages\n"
                "    pass\n\n"
                "resume = '''\n"
                "Jane Doe\n"
                "jane.doe@email.com | +1-555-123-4567\n"
                "5 years of experience in data engineering.\n"
                "Skills: Python, SQL, Scala, Apache Spark.\n"
                "'''\n"
                "print(extract_resume(resume))"
            )
        }
    },
    {
        "title": "12. Machine Translation & Seq2Seq",
        "desc": "Understand encoder-decoder architectures, attention mechanisms, and BLEU scoring. Implement simple character-level and word-level translation concepts.",
        "examples": [
            {
                "label": "BLEU score calculation from scratch",
                "code": "from collections import Counter\nimport math\n\ndef ngram_counts(tokens, n):\n    return Counter(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))\n\ndef bleu_score(reference: str, hypothesis: str, max_n: int = 4) -> float:\n    ref_tokens  = reference.lower().split()\n    hyp_tokens  = hypothesis.lower().split()\n    if not hyp_tokens:\n        return 0.0\n    # Brevity penalty\n    bp = min(1.0, math.exp(1 - len(ref_tokens)/len(hyp_tokens)))\n    scores = []\n    for n in range(1, max_n + 1):\n        ref_ng  = ngram_counts(ref_tokens, n)\n        hyp_ng  = ngram_counts(hyp_tokens, n)\n        clipped = sum(min(c, ref_ng[ng]) for ng, c in hyp_ng.items())\n        total   = sum(hyp_ng.values())\n        if total == 0:\n            scores.append(0.0)\n        else:\n            scores.append(clipped / total)\n    # Geometric mean of precisions\n    log_avg = sum(math.log(s) if s > 0 else -999 for s in scores) / max_n\n    bleu = bp * math.exp(log_avg)\n    print(f'Reference:  {reference}')\n    print(f'Hypothesis: {hypothesis}')\n    print(f'N-gram precisions: {[round(s,3) for s in scores]}')\n    print(f'BLEU-{max_n}: {bleu:.4f}')\n    return bleu\n\nbleu_score(\n    'The cat sat on the mat',\n    'The cat is on the mat'\n)\nbleu_score(\n    'The cat sat on the mat',\n    'A dog lay on a rug'\n)"
            },
            {
                "label": "Simple encoder-decoder concept with embeddings",
                "code": "import numpy as np\n\n# Demonstrate encoder-decoder idea without deep learning framework\nnp.random.seed(42)\n\n# Toy vocabulary\nvocab = {'<pad>': 0, '<sos>': 1, '<eos>': 2, 'hello': 3, 'world': 4,\n         'hola': 5, 'mundo': 6, 'bonjour': 7, 'monde': 8}\nidx2word = {v: k for k, v in vocab.items()}\n\n# Random embeddings (in practice: learned)\nEMB_DIM = 8\nembeddings = np.random.randn(len(vocab), EMB_DIM) * 0.1\n\ndef encode(sentence: str) -> np.ndarray:\n    tokens = [vocab.get(w, 0) for w in sentence.lower().split()]\n    vecs = [embeddings[t] for t in tokens]\n    return np.mean(vecs, axis=0)  # mean pooling = context vector\n\ndef cosine_sim(a, b):\n    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)\n\nsrc = encode('hello world')\nprint('Encoder output (context vector):', src.round(3))\n\n# In real seq2seq: decoder generates target tokens one by one\n# conditioned on context vector + previous generated token\nprint('\\nEncoder-Decoder flow:')\nprint('  Source: hello world')\nprint('  Encoder -> context vector (shape:', src.shape, ')')\nprint('  Decoder: <sos> -> hola -> mundo -> <eos>')\nprint('  At each step: P(word | context, prev_token)')"
            },
            {
                "label": "Attention mechanism visualization",
                "code": "import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n\n# Simulate attention weights for 'The cat sat on the mat' -> 'Le chat etait sur le tapis'\nnp.random.seed(42)\nsrc_words = ['The', 'cat', 'sat', 'on', 'the', 'mat']\ntgt_words = ['Le', 'chat', 'etait', 'sur', 'le', 'tapis']\n\n# Simulate attention weights (in practice: softmax(Q @ K.T / sqrt(d_k)))\n# Diagonal-dominant = good alignment\nraw = np.random.rand(6, 6)\n# Make it more diagonal (word alignments)\nfor i in range(6):\n    raw[i, i] += 2.0\nraw[0, 4] += 1.0  # 'the' aligns with 'le'\nattention = np.exp(raw) / np.exp(raw).sum(axis=1, keepdims=True)\n\nfig, ax = plt.subplots(figsize=(7, 5))\nim = ax.imshow(attention, cmap='Blues', vmin=0, vmax=1)\nax.set_xticks(range(6)); ax.set_xticklabels(src_words, rotation=45, ha='right')\nax.set_yticks(range(6)); ax.set_yticklabels(tgt_words)\nax.set_xlabel('Source'); ax.set_ylabel('Target')\nax.set_title('Attention Weights')\nplt.colorbar(im, ax=ax); plt.tight_layout()\nplt.savefig('attention_weights.png', dpi=80); plt.close()\nprint('Saved attention_weights.png')\nprint('Attention row sums:', attention.sum(axis=1).round(3))"
            },
            {
                "label": "Hugging Face translation pipeline",
                "code": "try:\n    from transformers import pipeline\n    # Zero-shot: use a pretrained translation model\n    translator = pipeline('translation_en_to_fr', model='Helsinki-NLP/opus-mt-en-fr')\n    sentences = [\n        'Machine learning is transforming healthcare.',\n        'The quick brown fox jumps over the lazy dog.',\n        'Data science requires statistics, programming, and domain knowledge.',\n    ]\n    for sent in sentences:\n        result = translator(sent, max_length=128)[0]['translation_text']\n        print(f'EN: {sent}')\n        print(f'FR: {result}\\n')\nexcept ImportError:\n    print('pip install transformers sentencepiece')\n    print('\\nExample output:')\n    print('EN: Machine learning is transforming healthcare.')\n    print('FR: L apprentissage automatique transforme les soins de sante.')"
            }
        ],
        "rw_scenario": "A global e-commerce platform needs to auto-translate product descriptions from English to 5 languages, validate translation quality with BLEU against professional translations, and flag low-quality translations for human review.",
        "rw_code": "from collections import Counter\nimport math\n\ndef simple_bleu(ref: str, hyp: str) -> float:\n    ref_t = ref.lower().split(); hyp_t = hyp.lower().split()\n    if not hyp_t: return 0.0\n    bp = min(1.0, math.exp(1 - len(ref_t)/len(hyp_t)))\n    scores = []\n    for n in range(1, 3):\n        ref_ng  = Counter(tuple(ref_t[i:i+n]) for i in range(len(ref_t)-n+1))\n        hyp_ng  = Counter(tuple(hyp_t[i:i+n]) for i in range(len(hyp_t)-n+1))\n        clip    = sum(min(c, ref_ng[ng]) for ng, c in hyp_ng.items())\n        total   = sum(hyp_ng.values()) or 1\n        scores.append(clip/total)\n    log_avg = sum(math.log(s) if s > 0 else -9 for s in scores) / 2\n    return bp * math.exp(log_avg)\n\n# Simulate auto-translations and quality check\npairs = [\n    ('Machine learning improves efficiency', 'L apprentissage automatique ameliore l efficacite'),\n    ('High quality product at low price', 'Produit cher mauvais qualite'),  # bad\n    ('Fast delivery guaranteed', 'Livraison rapide garantie'),\n]\nTHRESHOLD = 0.35\nfor en, fr in pairs:\n    score = simple_bleu(en, fr)\n    flag = 'REVIEW' if score < THRESHOLD else 'OK'\n    print(f'[{flag}] BLEU={score:.3f} | {fr[:50]}')",
        "practice": {
            "title": "BLEU Score Evaluator",
            "desc": "Implement a BLEU-1 and BLEU-2 evaluator. Given a list of (reference, hypothesis) pairs, compute per-pair BLEU scores and the corpus-level BLEU (average). Flag translations below 0.4 for human review. Test with at least 3 sentence pairs.",
            "starter": (
                "from collections import Counter\nimport math\n\n"
                "def bleu_n(ref: str, hyp: str, n: int) -> float:\n"
                "    # TODO: compute BLEU-n precision with clipping\n"
                "    pass\n\n"
                "def evaluate_translations(pairs):\n"
                "    # pairs: list of (reference, hypothesis) tuples\n"
                "    # TODO: compute BLEU-1 and BLEU-2 for each pair\n"
                "    # TODO: flag pairs below threshold 0.4\n"
                "    # TODO: print results and corpus average\n"
                "    pass\n\n"
                "test_pairs = [\n"
                "    ('The cat sat on the mat', 'The cat is on the mat'),\n"
                "    ('Hello world how are you', 'Hi earth what is up'),\n"
                "    ('Data science is exciting', 'Data science is fascinating and rewarding'),\n"
                "]\n"
                "evaluate_translations(test_pairs)"
            )
        }
    },
    {
        "title": "13. Document Search & RAG",
        "desc": "Build retrieval systems using TF-IDF, BM25, and dense vector search. Implement a basic Retrieval-Augmented Generation pipeline combining a retriever with a language model.",
        "examples": [
            {
                "label": "TF-IDF retrieval system",
                "code": "from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.metrics.pairwise import cosine_similarity\nimport numpy as np\n\ncorpus = [\n    'Python is a versatile programming language for data science and web development.',\n    'Machine learning models require large amounts of training data.',\n    'Neural networks are inspired by the structure of the human brain.',\n    'Natural language processing enables computers to understand human text.',\n    'Deep learning achieves state-of-the-art results on image classification tasks.',\n    'Reinforcement learning trains agents through rewards and penalties.',\n    'Transfer learning fine-tunes pre-trained models on new tasks.',\n    'Transformers use self-attention to process sequences in parallel.',\n]\n\nvectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))\ntfidf_matrix = vectorizer.fit_transform(corpus)\n\ndef search(query: str, top_k: int = 3) -> list:\n    q_vec = vectorizer.transform([query])\n    sims  = cosine_similarity(q_vec, tfidf_matrix).flatten()\n    top   = np.argsort(sims)[::-1][:top_k]\n    return [(corpus[i][:70], round(sims[i], 4)) for i in top]\n\nfor q in ['how do neural networks learn', 'NLP text processing', 'image recognition']:\n    print(f'Query: {q}')\n    for doc, score in search(q):\n        print(f'  [{score:.4f}] {doc}')\n    print()"
            },
            {
                "label": "BM25 retrieval from scratch",
                "code": "import numpy as np\nfrom collections import Counter\nimport math\n\nclass BM25:\n    def __init__(self, corpus, k1=1.5, b=0.75):\n        self.corpus  = [doc.lower().split() for doc in corpus]\n        self.k1, self.b = k1, b\n        self.n = len(self.corpus)\n        self.avgdl = np.mean([len(d) for d in self.corpus])\n        self.df = {}\n        for doc in self.corpus:\n            for term in set(doc):\n                self.df[term] = self.df.get(term, 0) + 1\n\n    def score(self, query: str, doc_id: int) -> float:\n        query_terms = query.lower().split()\n        doc = self.corpus[doc_id]\n        doc_len = len(doc)\n        tf = Counter(doc)\n        score = 0.0\n        for term in query_terms:\n            if term not in self.df: continue\n            idf = math.log((self.n - self.df[term] + 0.5) / (self.df[term] + 0.5) + 1)\n            freq = tf.get(term, 0)\n            tf_score = freq * (self.k1 + 1) / (freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl))\n            score += idf * tf_score\n        return score\n\n    def retrieve(self, query: str, top_k: int = 3):\n        scores = [(i, self.score(query, i)) for i in range(self.n)]\n        return sorted(scores, key=lambda x: -x[1])[:top_k]\n\ndocs = ['Python machine learning tutorial', 'Deep neural network architectures', 'Python web scraping guide', 'Transformer models for NLP', 'Data science with Python pandas']\nbm25 = BM25(docs)\nprint('BM25 results for \"Python NLP\":')\nfor idx, score in bm25.retrieve('Python NLP'):\n    print(f'  [{score:.3f}] {docs[idx]}')"
            },
            {
                "label": "Dense vector search with sentence embeddings",
                "code": "import numpy as np\nfrom sklearn.metrics.pairwise import cosine_similarity\n\n# Simulate sentence embeddings (in practice: use SentenceTransformer)\nnp.random.seed(42)\n\ndocs = [\n    'How to train a neural network',\n    'Python list comprehension tutorial',\n    'Best practices for REST API design',\n    'Introduction to gradient descent optimization',\n    'SQL window functions explained',\n    'Backpropagation algorithm explained',\n]\n\n# Simulate embeddings (normally: model.encode(docs))\n# Make 'neural network' and 'gradient descent' semantically similar\nEMB_DIM = 16\nbase_embs = np.random.randn(len(docs), EMB_DIM)\n# Make neural network docs cluster together\nfor i in [0, 3, 5]:\n    base_embs[i] += np.array([2]*4 + [0]*12)  # shared direction\nbase_embs /= np.linalg.norm(base_embs, axis=1, keepdims=True)\n\ndef dense_search(query_emb, doc_embs, top_k=3):\n    sims = cosine_similarity(query_emb.reshape(1,-1), doc_embs).flatten()\n    top  = np.argsort(sims)[::-1][:top_k]\n    return [(docs[i], sims[i]) for i in top]\n\n# Query embedding (similar to NN docs)\nquery_emb = base_embs[0] + np.random.randn(EMB_DIM) * 0.1\nquery_emb /= np.linalg.norm(query_emb)\nprint('Dense search results for [neural network query]:')\nfor doc, sim in dense_search(query_emb, base_embs):\n    print(f'  [{sim:.3f}] {doc}')"
            },
            {
                "label": "Minimal RAG pipeline (retrieve + generate)",
                "code": "from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.metrics.pairwise import cosine_similarity\nimport numpy as np\n\n# Knowledge base\nknowledge_base = [\n    'Python was created by Guido van Rossum in 1991.',\n    'NumPy provides N-dimensional array support and math functions.',\n    'Pandas is built on NumPy and provides DataFrame structures for data analysis.',\n    'Scikit-learn offers machine learning algorithms for classification, regression, and clustering.',\n    'Matplotlib is the most popular Python plotting library.',\n    'TensorFlow and PyTorch are the two leading deep learning frameworks.',\n]\n\nvect = TfidfVectorizer(stop_words='english')\nkb_matrix = vect.fit_transform(knowledge_base)\n\ndef retrieve(query: str, top_k: int = 2) -> list:\n    q_vec = vect.transform([query])\n    sims  = cosine_similarity(q_vec, kb_matrix).flatten()\n    top   = np.argsort(sims)[::-1][:top_k]\n    return [knowledge_base[i] for i in top]\n\ndef rag_answer(query: str) -> str:\n    \"\"\"Minimal RAG: retrieve context, then format answer.\"\"\"\n    context = retrieve(query)\n    context_str = ' '.join(context)\n    # In real RAG: pass context + query to LLM (e.g. Claude/GPT)\n    # Here: template-based answer simulation\n    answer = f'Based on retrieved context: {context_str[:120]}...'\n    return answer\n\nqueries = ['What is pandas?', 'Who created Python?', 'deep learning frameworks']\nfor q in queries:\n    print(f'Q: {q}')\n    print(f'Retrieved: {retrieve(q)[0][:60]}')\n    print()"
            }
        ],
        "rw_scenario": "Build an internal company knowledge base search that answers employee questions by retrieving relevant policy documents, FAQs, and procedure guides, then generating a concise answer using the retrieved context.",
        "rw_code": "from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.metrics.pairwise import cosine_similarity\nimport numpy as np\n\n# Company policy documents\ndocuments = {\n    'vacation':   'Employees are entitled to 20 days of paid vacation per year. Unused days can be carried over to the next year up to 5 days.',\n    'remote':     'Remote work is allowed up to 3 days per week. Core hours are 10am-3pm in the employee home timezone.',\n    'expenses':   'Business expenses must be submitted within 30 days with receipts. Meals are reimbursed up to $50 per day.',\n    'equipment':  'New employees receive a MacBook Pro and $500 equipment budget. Replacements require manager approval.',\n    'onboarding': 'New employees complete a 2-week onboarding program including security training and team introductions.',\n}\n\ndoc_texts = list(documents.values())\ndoc_keys  = list(documents.keys())\nvect = TfidfVectorizer(stop_words='english')\nmatrix = vect.fit_transform(doc_texts)\n\ndef answer_question(query: str, top_k: int = 2) -> str:\n    sims = cosine_similarity(vect.transform([query]), matrix).flatten()\n    top  = np.argsort(sims)[::-1][:top_k]\n    context = ' '.join(doc_texts[i] for i in top)\n    return f'[Context: {context[:200]}...]'\n\nfor q in ['How many vacation days do I get?', 'Can I work from home?', 'expense reimbursement policy']:\n    print(f'Q: {q}')\n    print(f'A: {answer_question(q)[:120]}')\n    print()",
        "practice": {
            "title": "FAQ Chatbot with TF-IDF Retrieval",
            "desc": "Build a simple FAQ chatbot. Given a list of (question, answer) pairs as your knowledge base, retrieve the most similar FAQ question to user input using TF-IDF + cosine similarity, and return its answer. Test with at least 5 FAQ entries and 3 user queries. Report similarity scores.",
            "starter": (
                "from sklearn.feature_extraction.text import TfidfVectorizer\n"
                "from sklearn.metrics.pairwise import cosine_similarity\nimport numpy as np\n\n"
                "faqs = [\n"
                "    ('What are your business hours?', 'We are open Monday to Friday, 9am to 6pm EST.'),\n"
                "    ('How do I reset my password?', 'Click Forgot Password on the login page and follow the email instructions.'),\n"
                "    ('What payment methods do you accept?', 'We accept Visa, Mastercard, PayPal, and bank transfers.'),\n"
                "    ('How long does shipping take?', 'Standard shipping takes 5-7 business days. Express ships in 2 days.'),\n"
                "    ('Can I return a product?', 'Yes, returns are accepted within 30 days with original packaging.'),\n"
                "]\n\n"
                "# TODO: Fit TfidfVectorizer on FAQ questions\n"
                "# TODO: For each user query, find most similar FAQ and return answer\n"
                "# TODO: Print query, matched question, similarity score, and answer\n\n"
                "user_queries = ['office hours', 'forgot my login', 'how to send back item']\n"
                "# TODO: process each query\n"
            )
        }
    },
    {
        "title": "14. Transformer Models & Pre-trained Pipelines",
        "examples": [
            {
                "label": "Tokenization & Subword Encoding with HuggingFace",
                "code": "from transformers import AutoTokenizer\ntokenizer = AutoTokenizer.from_pretrained(\"distilbert-base-uncased\")\ntexts = [\n    \"The stock market crashed on Monday.\",\n    \"Transformers revolutionized NLP in 2017!\"\n]\nencoded = tokenizer(texts, padding=True, truncation=True, max_length=32, return_tensors=\"pt\")\nprint(\"Input IDs shape:\", encoded[\"input_ids\"].shape)\nfor i, text in enumerate(texts):\n    tokens = tokenizer.convert_ids_to_tokens(encoded[\"input_ids\"][i])\n    tokens = [t for t in tokens if t != \"[PAD]\"]\n    print(f\"\\nText {i+1}: {tokens}\")\nprint(\"\\nVocab size:\", tokenizer.vocab_size)"
            },
            {
                "label": "Sentiment Classification with Pre-trained BERT",
                "code": "from transformers import pipeline\nclassifier = pipeline(\"sentiment-analysis\", model=\"distilbert-base-uncased-finetuned-sst-2-english\")\nreviews = [\n    \"This product exceeded all my expectations! Absolutely fantastic.\",\n    \"Terrible quality. Broke after one day. Very disappointed.\",\n    \"It is okay, nothing special but gets the job done.\",\n]\nresults = classifier(reviews)\nfor text, result in zip(reviews, results):\n    label = result[\"label\"]\n    score = result[\"score\"]\n    print(f\"[{label} {score:.3f}] {text[:50]}...\")"
            },
            {
                "label": "Zero-Shot Classification",
                "code": "from transformers import pipeline\nclassifier = pipeline(\"zero-shot-classification\",\n                      model=\"facebook/bart-large-mnli\")\ntext = \"The Federal Reserve raised interest rates by 25 basis points today.\"\ncandidate_labels = [\"finance\", \"sports\", \"technology\", \"politics\", \"health\"]\nresult = classifier(text, candidate_labels)\nprint(\"Text:\", text[:70])\nprint(\"\\nClassification scores:\")\nfor label, score in zip(result[\"labels\"], result[\"scores\"]):\n    bar = \"#\" * int(score * 30)\n    print(f\"  {label:<12} {score:.4f}  {bar}\")"
            }
        ],
        "rw_scenario": "Customer support triage: classify incoming support tickets into departments (billing, technical, returns, general) using zero-shot classification without any labeled training data.",
        "rw_code": "from transformers import pipeline\n# Zero-shot ticket router\nclassifier = pipeline(\"zero-shot-classification\",\n                      model=\"facebook/bart-large-mnli\")\ntickets = [\n    \"My credit card was charged twice for the same order.\",\n    \"The app keeps crashing whenever I try to open settings.\",\n    \"I want to return the shoes I bought last week. They don\'t fit.\",\n    \"When will my order arrive? It\'s been two weeks.\",\n    \"I forgot my password and the reset link doesn\'t work.\",\n]\ndepartments = [\"billing\", \"technical support\", \"returns & refunds\", \"shipping\", \"account access\"]\nprint(\"Support Ticket Routing\")\nprint(\"=\" * 60)\nfor ticket in tickets:\n    result = classifier(ticket, departments, multi_label=False)\n    top_dept = result[\"labels\"][0]\n    top_score = result[\"scores\"][0]\n    print(f\"Ticket: {ticket[:55]}...\")\n    print(f\"  -> {top_dept} ({top_score:.3f})\")\n    print()",
        "practice": {
            "title": "News Article Classifier",
            "desc": "Use zero-shot classification with 6 news categories (politics, sports, technology, science, entertainment, business). Classify 5 different news headlines. Then use a pre-trained sentiment pipeline on the same headlines and combine both outputs into a structured report showing category + sentiment for each article.",
            "starter": "from transformers import pipeline\n# News headlines to classify\nheadlines = [\n    \"SpaceX successfully lands reusable rocket for 20th time.\",\n    \"Champions League final set as Real Madrid beats Bayern Munich.\",\n    \"Senate votes to pass new climate legislation bill.\",\n    \"Apple unveils new M4 chip with enhanced neural processing.\",\n    \"GDP growth slows to 1.2% amid rising inflation concerns.\",\n]\ncategories = [\"politics\", \"sports\", \"technology\", \"science\", \"entertainment\", \"business\"]\n# TODO: Zero-shot classify each headline into categories\n# TODO: Run sentiment analysis on each headline\n# TODO: Print formatted table: headline | category | sentiment | scores\n"
        }
    },
    {
        "title": "15. Named Entity Recognition & Information Extraction",
        "examples": [
            {
                "label": "spaCy NER Pipeline",
                "code": "import spacy\nnlp = spacy.load(\"en_core_web_sm\")\ntexts = [\n    \"Apple Inc. CEO Tim Cook announced new products at WWDC in San Francisco.\",\n    \"On March 14, 2023, the Fed raised rates by 25bps, affecting $4.5T in bonds.\",\n]\nfor text in texts:\n    doc = nlp(text)\n    print(f\"Text: {text[:65]}...\")\n    print(\"Entities:\")\n    for ent in doc.ents:\n        print(f\"  [{ent.label_:<10}] \'{ent.text}\'\")\n    print()"
            },
            {
                "label": "Custom NER with spaCy Patterns",
                "code": "import spacy\nfrom spacy.matcher import Matcher\nnlp = spacy.load(\"en_core_web_sm\")\nmatcher = Matcher(nlp.vocab)\n# Match product codes like \"SKU-12345\" or \"PROD-ABC99\"\npattern = [{\"TEXT\": {\"REGEX\": r\"(SKU|PROD|ITEM)-[A-Z0-9]{3,8}\"}}]\nmatcher.add(\"PRODUCT_CODE\", [pattern])\ntexts = [\n    \"Customer ordered SKU-48291 and PROD-XR99 but ITEM-ZZ001 was out of stock.\",\n    \"Return request for SKU-11100 received from warehouse.\",\n]\nfor text in texts:\n    doc = nlp(text)\n    matches = matcher(doc)\n    codes = [doc[start:end].text for _, start, end in matches]\n    print(f\"Text: {text}\")\n    print(f\"Product codes found: {codes}\\n\")"
            },
            {
                "label": "Relation Extraction with Dependency Parsing",
                "code": "import spacy\nnlp = spacy.load(\"en_core_web_sm\")\ntext = \"Elon Musk founded SpaceX in 2002. Jeff Bezos started Amazon in 1994.\"\ndoc = nlp(text)\nprint(\"Subject-Verb-Object triples:\")\nfor sent in doc.sents:\n    for token in sent:\n        if token.dep_ == \"ROOT\":\n            subj = [c.text for c in token.children if c.dep_ in (\"nsubj\",\"nsubjpass\")]\n            obj  = [c.text for c in token.children if c.dep_ in (\"dobj\",\"attr\",\"pobj\")]\n            if subj and obj:\n                print(f\"  ({subj[0]}) --[{token.text}]--> ({obj[0]})\")\nprint(\"\\nNamed Entities:\")\nfor ent in doc.ents:\n    print(f\"  {ent.text:<15} [{ent.label_}]\")"
            }
        ],
        "rw_scenario": "Legal contract analysis: extract parties, dates, monetary amounts, and obligations from contract text to populate a structured database automatically.",
        "rw_code": "import spacy\nimport re\nnlp = spacy.load(\"en_core_web_sm\")\ncontract_text = \"\"\"\nThis Service Agreement is entered into on January 15, 2024, between\nAcme Corporation, a Delaware company (\"Client\"), and TechSolutions LLC,\na California limited liability company (\"Provider\"). Client agrees to pay\nProvider $12,500 per month for software development services. The agreement\nterminates on December 31, 2024. Acme Corporation is headquartered in\nNew York, NY. Either party may terminate with 30 days written notice.\n\"\"\"\ndoc = nlp(contract_text)\n# Extract entities by type\nparties = []\ndates = []\nmoney = []\nfor ent in doc.ents:\n    if ent.label_ == \"ORG\":\n        parties.append(ent.text)\n    elif ent.label_ == \"DATE\":\n        dates.append(ent.text)\n    elif ent.label_ == \"MONEY\":\n        money.append(ent.text)\nprint(\"Contract Extraction Report\")\nprint(f\"Parties:  {list(set(parties))}\")\nprint(f\"Dates:    {dates}\")\nprint(f\"Amounts:  {money}\")\n# Extract obligations with regex on sentence level\nfor sent in doc.sents:\n    if any(w in sent.text.lower() for w in [\"agrees\", \"shall\", \"must\", \"terminates\"]):\n        print(f\"Obligation: {sent.text.strip()[:80]}\")",
        "practice": {
            "title": "Resume Information Extractor",
            "desc": "Given a sample resume text (3-4 sentences), use spaCy to extract: person name (PERSON), organizations (ORG), job titles (using custom Matcher patterns for \'Senior Engineer\', \'Data Scientist\', etc.), years of experience (CARDINAL + \'years\'), and skills (custom pattern for capitalized tech terms). Output a structured JSON-like summary.",
            "starter": "import spacy\nfrom spacy.matcher import Matcher\nnlp = spacy.load(\"en_core_web_sm\")\nresume = \"\"\"\nJohn Smith is a Senior Data Scientist with 8 years of experience at Google and Microsoft.\nHe specializes in Python, TensorFlow, and SQL. Previously, he was a Machine Learning Engineer\nat Amazon, where he led a team of 5 researchers. He holds a PhD from MIT in Computer Science.\n\"\"\"\nmatcher = Matcher(nlp.vocab)\n# TODO: Pattern for job titles (e.g., \"Senior Data Scientist\", \"Machine Learning Engineer\")\n# TODO: Pattern for tech skills (capitalized 1-3 word terms)\n# TODO: Extract PERSON, ORG, DATE, CARDINAL entities\n# TODO: Output structured dict: name, companies, titles, skills, experience_years\n"
        }
    },
    {
        "title": "16. Text Generation, Summarization & Prompt Engineering",
        "examples": [
            {
                "label": "Text Generation with GPT-2",
                "code": "from transformers import pipeline\ngenerator = pipeline(\"text-generation\", model=\"gpt2\", max_new_tokens=60)\nprompts = [\n    \"The future of artificial intelligence is\",\n    \"In 2035, data scientists will\",\n]\nfor prompt in prompts:\n    outputs = generator(prompt, num_return_sequences=2, temperature=0.8, do_sample=True)\n    print(f\"Prompt: {prompt}\")\n    for i, out in enumerate(outputs, 1):\n        generated = out[\"generated_text\"][len(prompt):]\n        print(f\"  [{i}] ...{generated[:80]}\")\n    print()"
            },
            {
                "label": "Structured Prompting & Prompt Engineering",
                "code": "# Demonstrates prompt engineering patterns (no API key needed — shows templates)\nimport json\n\ndef build_extraction_prompt(text, fields):\n    field_list = \", \".join(f\'\"{f}\"\' for f in fields)\n    return f\"\"\"Extract the following fields from the text below.\nReturn ONLY valid JSON with keys: {field_list}.\nIf a field is not found, use null.\n\nText: {text}\n\nJSON output:\"\"\"\n\ntexts = [\n    \"Order #4521 placed by Sarah Johnson on 2024-03-15 for $289.99. Ships to Chicago, IL.\",\n    \"Meeting scheduled with Dr. Patel at Boston General Hospital on Tuesday at 2pm.\"\n]\nfields_order   = [\"order_id\", \"customer_name\", \"date\", \"amount\", \"city\"]\nfields_meeting = [\"person\", \"organization\", \"day\", \"time\"]\nfor text, fields in zip(texts, [fields_order, fields_meeting]):\n    prompt = build_extraction_prompt(text, fields)\n    print(\"=== Prompt Template ===\")\n    print(prompt[:200])\n    print(\"...\")\n    print()"
            },
            {
                "label": "Summarization with BART",
                "code": "from transformers import pipeline\nsummarizer = pipeline(\"summarization\", model=\"facebook/bart-large-cnn\",\n                      max_length=60, min_length=20, do_sample=False)\narticle = \"\"\"\nScientists at MIT have developed a new AI system capable of predicting protein\nfolding structures with greater accuracy than any previous model. The breakthrough,\npublished in Nature, combines deep learning with molecular dynamics simulations.\nResearchers tested the system on over 10,000 known protein structures and achieved\n98.5% accuracy. This development could accelerate drug discovery by enabling\nresearchers to design proteins that target specific disease pathways. The team plans\nto make the model open-source within the next six months.\n\"\"\"\nsummary = summarizer(article.strip())[0][\"summary_text\"]\noriginal_words = len(article.split())\nsummary_words  = len(summary.split())\nprint(f\"Original: {original_words} words\")\nprint(f\"Summary ({summary_words} words):\")\nprint(summary)"
            }
        ],
        "rw_scenario": "Content moderation pipeline: automatically detect and summarize problematic content, classify severity, and route to appropriate human reviewer with context.",
        "rw_code": "from transformers import pipeline\n# Multi-stage NLP pipeline: classify -> summarize -> route\nclassifier  = pipeline(\"text-classification\", model=\"distilbert-base-uncased-finetuned-sst-2-english\")\nzero_shot   = pipeline(\"zero-shot-classification\", model=\"facebook/bart-large-mnli\")\nposts = [\n    \"This is an amazing product! I love the design and performance.\",\n    \"I hate this company. They stole my money and won\'t respond.\",\n    \"How do I reset my password? I can\'t log in to my account.\",\n    \"WARNING: This is a scam. Do NOT buy from this seller!!\",\n]\nseverity_labels = [\"urgent - requires immediate review\", \"moderate - review within 24h\", \"low - can be auto-resolved\"]\nprint(\"Content Moderation Pipeline\")\nprint(\"=\" * 60)\nfor post in posts:\n    sentiment = classifier(post)[0]\n    severity  = zero_shot(post, severity_labels)[\"labels\"][0]\n    print(f\"Post: {post[:55]}...\")\n    print(f\"  Sentiment: {sentiment[\'label\']} ({sentiment[\'score\']:.2f})\")\n    print(f\"  Severity:  {severity}\")\n    print()",
        "practice": {
            "title": "Multi-Document Summarization",
            "desc": "Summarize 3 different news articles (each 100+ words, on the same topic) using BART. Then concatenate the summaries and summarize again to create a \'meta-summary\'. Compare word counts at each stage and compute the compression ratio. Also extract key noun phrases from the meta-summary using spaCy.",
            "starter": "from transformers import pipeline\nimport spacy\nnlp_sp = spacy.load(\"en_core_web_sm\")\nsummarizer = pipeline(\"summarization\", model=\"facebook/bart-large-cnn\",\n                      max_length=80, min_length=30, do_sample=False)\narticle1 = \"\"\"[Article 1: 100+ words on climate change - fill in]\"\"\"\"\narticle2 = \"\"\"[Article 2: 100+ words on climate policy - fill in]\"\"\"\"\narticle3 = \"\"\"[Article 3: 100+ words on renewable energy - fill in]\"\"\"\"\narticles = [article1, article2, article3]\n# TODO: Summarize each article individually\n# TODO: Concatenate summaries and create meta-summary\n# TODO: Compute compression ratios at each stage\n# TODO: Extract noun chunks from meta-summary with spaCy\n"
        }
    },
]

if __name__ == "__main__":
    html_out = BASE / "index.html"
    nb_out   = BASE / "study_guide.ipynb"
    html_out.write_text(make_html(SECTIONS), encoding="utf-8")
    nb_out.write_text(json.dumps(make_nb(SECTIONS), indent=1), encoding="utf-8")
    nb_cells = len(make_nb(SECTIONS)["cells"])
    print(f"NLP guide created: {BASE}")
    print(f"  index.html:        {html_out.stat().st_size/1024:.1f} KB")
    print(f"  study_guide.ipynb: {nb_cells} cells")
