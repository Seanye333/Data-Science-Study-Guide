# Data Science Study Path

An interactive, self-paced study guide covering the full data science stack — from Python basics to MLOps and Bayesian thinking. Built as a static website with a glassmorphism UI, syntax-highlighted code examples, real-world scenarios, and practice checklists on every topic.

## Live Site

> [https://seanye333.github.io/Data-Science-Study-Guide/](https://seanye333.github.io/Data-Science-Study-Guide/)

---

## Modules

| # | Module | Topics |
|---|--------|--------|
| 00 | Python Basics | Variables, OOP, async, decorators, type hints |
| 01 | NumPy | Arrays, broadcasting, linear algebra, FFT |
| 02 | SQL | Joins, window functions, CTEs, optimization |
| 03 | REST APIs | Requests, FastAPI, auth, async clients |
| 03 | Pandas&nbsp;† | DataFrames, groupby, merge, time series |
| 04 | Matplotlib | Subplots, styling, animations, custom charts |
| 05 | Seaborn | Statistical plots, themes, FacetGrid |
| 06 | Plotly | Interactive charts, Dash, animations |
| 07 | Scikit-learn | Classification, regression, pipelines, tuning |
| 08 | Streamlit | Widgets, caching, auth, ML deployment |
| 09 | Polars | Lazy evaluation, expressions, large data |
| 10 | Deep Learning | CNNs, RNNs, transformers, training loops |
| 11 | Statistics | Distributions, hypothesis testing, regression |
| 12 | Time Series | ARIMA, forecasting, seasonality, Prophet |
| 13 | NLP | Tokenization, embeddings, transformers, LLMs |
| 14 | MLOps | Model serving, Docker, MLflow, CI/CD, drift |
| 15 | Git | Branching, rebase, GitHub Actions, workflows |
| 16 | Feature Engineering | Encoding, scaling, selection, pipelines |
| 17 | Bayesian Thinking | Bayes' theorem, priors, MCMC, PyMC |

> † **Pandas** is hand-maintained (it also ships extra `pandas_practice*.ipynb`
> notebooks) and has no generator, so it is the one module not rebuilt by
> `generate_all.py`. Edit its `index.html` directly.

---

## Features

- **Glassmorphism UI** — frosted glass cards, gradient backgrounds, smooth animations
- **Syntax highlighting** — via highlight.js with GitHub Dark theme
- **Practice Checklists** — 4–5 actionable todos on every topic
- **Real-world scenarios** — industry-style code examples per section
- **Practice exercises** — starter code with guided TODOs
- **Runnable practice** — edit and run each exercise right in the browser via [Pyodide](https://pyodide.org/) (CPython → WASM); the runtime lazy-loads on first Run, no setup or backend
- **Progress tracking** — completion state saved in localStorage
- **Searchable sidebar** — filter topics instantly
- **Responsive** — works on desktop and mobile
- **Jupyter notebooks** — every module ships a `.ipynb` you can run locally

---

## Project Structure

```
Data-Science-Study-Guide/
│
├── index.html              ← Home / module selector
├── overview.html           ← Roadmap & learning path
│
├── modules/                ← One folder per module
│   ├── 00_python_basics/
│   │   ├── index.html
│   │   └── study_guide.ipynb
│   └── ...
│
├── styles/
│   ├── glass.css           ← Shared glassmorphism stylesheet
│   ├── effects.js          ← Page loader & visual effects
│   ├── nav-ux.js           ← Sidebar / navigation behavior
│   ├── hands-on.js         ← In-browser Python runner for Practice blocks (Pyodide)
│   └── module_chrome.json  ← Shared chrome (theme toggle, loader, mobile nav, hands-on)
│
├── generators/             ← Python scripts that generate each module's content
│   ├── gen_python_basics.py
│   └── ...
│
└── generate_all.py         ← Build entry point: runs generators + injects chrome
```

---

## Running Locally

No build step needed — just open the HTML files in a browser:

```bash
# Clone the repo
git clone https://github.com/Seanye333/Data-Science-Study-Guide.git
cd Data-Science-Study-Guide

# Open in browser
open index.html          # macOS
start index.html         # Windows
```

Or serve with Python for proper relative paths:

```bash
python -m http.server 8080
# then visit http://localhost:8080
```

---

## Regenerating Modules

Each module's content lives in a generator under `generators/`, but the build
entry point is `generate_all.py` — it runs the generators **and** injects the
shared site chrome (theme toggle, page loader, mobile nav, `effects.js` /
`nav-ux.js`) defined in `styles/module_chrome.json`.

Rebuild everything:

```bash
python generate_all.py
```

Rebuild only specific modules (matched by name):

```bash
python generate_all.py numpy sql
```

> Run generators through `generate_all.py`, not directly — invoking a single
> `generators/gen_*.py` writes the base HTML **without** the chrome.

> Requires Python 3.10+. No external dependencies — uses only the standard library.

The CI workflow (`.github/workflows/build.yml`) runs this on every push and PR
and fails if the committed site no longer matches the generators. The one
exception is the hand-maintained **Pandas** module, which has no generator and
is therefore excluded from the reproducibility check.

---

## Tech Stack

- **Frontend:** Vanilla HTML/CSS/JS — no frameworks
- **Styling:** Custom glassmorphism CSS with CSS variables
- **Syntax highlighting:** [highlight.js](https://highlightjs.org/)
- **Notebooks:** Jupyter-compatible `.ipynb` (generated programmatically)
- **Hosting:** GitHub Pages

---

## License

Released under the [MIT License](LICENSE).
