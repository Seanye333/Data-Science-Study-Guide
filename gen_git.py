#!/usr/bin/env python3
"""Generate Git & Version Control study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE = pathlib.Path(r"c:\Users\seany\Documents\All Codes\Data Science Study Path\15_git")
BASE.mkdir(parents=True, exist_ok=True)

# ─── HTML builder ─────────────────────────────────────────────────────────────
def make_html(sections):
    nav = "\n    ".join(
        f'<li><a href="#s{i}" onclick="act(this,event)">{esc(s["title"])}</a></li>'
        for i, s in enumerate(sections)
    )
    cards = ""
    for i, s in enumerate(sections):
        blks = ""
        for j, ex in enumerate(s.get("examples", [])):
            cid = f"c{i}_{j}"
            lang = ex.get("lang", "bash")
            blks += (
                f'<div class="code-block">'
                f'<div class="ch"><span>{esc(ex.get("label","Example"))}</span>'
                f'<button onclick="cp(\'{cid}\')">Copy</button></div>'
                f'<pre><code id="{cid}" class="language-{lang}">{esc(ex["code"])}</code></pre>'
                f'</div>'
            )
        rw = s.get("rw", {})
        rw_html = ""
        if rw:
            rw_lang = rw.get("lang", "bash")
            rw_html = (
                f'<div class="rw">'
                f'<div class="rh">&#x1F4BC; Real-World: {esc(rw["title"])}</div>'
                f'<div class="rd">{esc(rw["scenario"])}</div>'
                f'<pre><code class="language-{rw_lang}">{esc(rw["code"])}</code></pre>'
                f'</div>'
            )
        practice = s.get("practice", {})
        practice_html = ""
        if practice:
            pid = f"p{i}"
            p_lang = practice.get("lang", "bash")
            practice_html = (
                f'<div class="practice">'
                f'<div class="ph">&#x1F3CB;&#xFE0F; Practice: {esc(practice["title"])}</div>'
                f'<div class="pd">{esc(practice["desc"])}</div>'
                f'<div class="code-block"><div class="ch"><span>Starter Code</span>'
                f'<button onclick="cp(\'{pid}\')">Copy</button></div>'
                f'<pre><code id="{pid}" class="language-{p_lang}">{esc(practice["starter"])}</code></pre></div>'
                f'</div>'
            )
        todos = s.get("todos", [])
        todos_html = ""
        if todos:
            items = "\n".join(
                f'<li><label><input type="checkbox"> {esc(t)}</label></li>'
                for t in todos
            )
            todos_html = (
                f'<div class="todo-list">'
                f'<div class="todo-head">&#x2705; Practice Checklist</div>'
                f'<ul>{items}</ul>'
                f'</div>'
            )
        cards += (
            f'<div class="topic" id="s{i}">'
            f'<div class="th" onclick="tog(this)"><span>{esc(s["title"])}</span>'
            f'<span class="arr">&#9660;</span></div>'
            f'<div class="tb"><p class="desc">{esc(s.get("desc",""))}</p>'
            f'{blks}{rw_html}{practice_html}{todos_html}</div></div>'
        )
    n = len(sections)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Git &amp; Version Control Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>
<link rel="stylesheet" href="../styles/glass.css">
<style>:root{{--acc:#f78166}}</style>
</head><body class="page-module">
<aside class="sidebar">
  <div class="sbh"><h2>🔀 Git &amp; Version Control</h2><p>Study Guide &bull; {n} topics</p>
    <input id="q" placeholder="Search..." oninput="filt(this.value)">
  </div>
  <ul class="nav-list" id="nl">{nav}</ul>
</aside>
<main class="main">
  <h1 class="pt">🔀 Git &amp; Version Control</h1>
  <p class="ps">{n} topics &bull; Click any card to expand</p>
  {cards}
</main>
<script>
hljs.highlightAll();
function tog(h){{var b=h.nextElementSibling,a=h.querySelector('.arr');b.classList.toggle('open');a.classList.toggle('open');}}
function act(el,e){{if(e)e.preventDefault();document.querySelectorAll('.nav-list a').forEach(a=>a.classList.remove('active'));el.classList.add('active');document.querySelector(el.getAttribute('href')).scrollIntoView({{behavior:'smooth'}});}}
function filt(q){{document.querySelectorAll('#nl li').forEach(li=>{{li.style.display=li.textContent.toLowerCase().includes(q.toLowerCase())?'':'none';}});}}
function cp(id){{navigator.clipboard.writeText(document.getElementById(id).innerText).catch(()=>{{}});}}
document.addEventListener('DOMContentLoaded',()=>{{var fh=document.querySelector('.th');if(fh)fh.click();var fa=document.querySelector('.nav-list a');if(fa)fa.classList.add('active');}});
</script></body></html>"""


# ─── Notebook builder ─────────────────────────────────────────────────────────
def make_nb(sections):
    cells = []
    n = [0]
    def nid(): n[0]+=1; return f"{n[0]:04d}"
    def md(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"markdown","id":nid(),"metadata":{},"source":s}
    def code(src):
        lines=src.split("\n"); s=[l+"\n" for l in lines]
        if s: s[-1]=s[-1].rstrip("\n")
        return {"cell_type":"code","execution_count":None,"id":nid(),"metadata":{},"outputs":[],"source":s}

    cells.append(md("# Git & Version Control Study Guide\n\nA hands-on guide to Git — from basic commits to advanced branching strategies and collaboration workflows."))
    for i, s in enumerate(sections, 1):
        cells.append(md(f"## {i}. {s['title']}\n\n{s.get('desc','')}"))
        for ex in s.get("examples", []):
            if ex.get("label"): cells.append(md(f"**{ex['label']}**"))
            cells.append(code(ex["code"]))
        rw = s.get("rw")
        if rw:
            cells.append(md(f"### Real-World: {rw['title']}\n\n> {rw['scenario']}"))
            cells.append(code(rw["code"]))
        practice = s.get("practice")
        if practice:
            cells.append(md(f"### 🏋️ Practice: {practice['title']}\n\n{practice['desc']}"))
            cells.append(code(practice["starter"]))
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name":"Python 3","language":"python","name":"python3"},
            "language_info": {"name":"python","version":"3.11.0"}
        },
        "nbformat": 4, "nbformat_minor": 5
    }


# ─── Content ──────────────────────────────────────────────────────────────────
SECTIONS = [

{
"title": "1. What is Git & Why It Matters",
"desc": "Git is a distributed version control system that tracks changes to files. Every data scientist needs Git to version code, collaborate with teams, reproduce experiments, and never lose work.",
"examples": [
{"label": "Installing and configuring Git", "code":
"""# Check if Git is installed
git --version

# Configure your identity (required before first commit)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Useful defaults
git config --global init.defaultBranch main
git config --global core.autocrlf true    # Windows
git config --global pull.rebase false     # merge on pull

# View all config
git config --list"""},
{"label": "Initializing a repository", "code":
"""# Create a new project and initialize Git
mkdir my-ds-project
cd my-ds-project
git init

# What happened? A hidden .git folder was created
ls -la .git/
# HEAD        — points to current branch
# config      — repo-level settings
# objects/    — stores all file content and history
# refs/       — branch and tag pointers"""},
{"label": "The three areas of Git", "code":
"""# Git has 3 areas:
# 1. Working Directory — your actual files
# 2. Staging Area (Index) — files ready to be committed
# 3. Repository (.git) — committed history

# See the current state
git status

# The workflow:
# edit files → git add (stage) → git commit (save snapshot)

echo "# My Project" > README.md
git status              # README.md is "untracked"
git add README.md       # Move to staging area
git status              # README.md is "staged"
git commit -m "Initial commit: add README"
git status              # "nothing to commit, working tree clean" """},
],
"rw": {
    "title": "Setting Up a Data Science Project",
    "scenario": "You're starting a new ML project. Proper Git setup from day one saves hours of headaches later — especially when collaborating or reproducing results.",
    "code":
"""# Create project structure
mkdir ml-churn-prediction
cd ml-churn-prediction
git init

# Create standard DS project structure
mkdir -p data/raw data/processed notebooks src models reports

# Create .gitignore (critical for DS projects!)
cat > .gitignore << 'EOF'
# Data files (too large for Git)
data/raw/*
data/processed/*
*.csv
*.parquet
*.h5
!data/.gitkeep

# Model files
models/*.pkl
models/*.joblib
models/*.pt

# Notebooks checkpoints
.ipynb_checkpoints/

# Environment
.env
venv/
__pycache__/

# OS files
.DS_Store
Thumbs.db
EOF

# Keep empty directories with .gitkeep
touch data/raw/.gitkeep data/processed/.gitkeep models/.gitkeep

# Initial commit
git add .
git commit -m "Initial project structure with .gitignore"
git log --oneline"""
},
"practice": {
    "title": "Create Your Own DS Project Repo",
    "desc": "Initialize a Git repo for a data science project with proper structure, a .gitignore tailored for Python/DS, and an initial commit.",
    "starter":
"""# TODO: Create a directory called "practice-project"
# TODO: Initialize git
# TODO: Create folders: data/, notebooks/, src/, tests/
# TODO: Create a .gitignore that excludes:
#   - .csv, .parquet files
#   - __pycache__/
#   - .ipynb_checkpoints/
#   - .env
# TODO: Create a README.md with a project title
# TODO: Stage and commit everything
# TODO: Run git log to verify"""
},
"todos": [
    "Run git config --list and verify your name and email are set correctly",
    "Create a brand new directory, run git init, and confirm the .git folder was created",
    "Create a README.md, stage it, and commit it — then inspect git log --oneline",
    "Add a second file, check git status, then use git restore to discard it",
    "Create a .gitignore excluding __pycache__/ and *.pyc, then verify git status ignores them",
],
},

{
"title": "2. Basic Commands — add, commit, log, diff",
"desc": "The core Git workflow: make changes, stage them, commit with a message, and review history. These 4 commands are 80% of daily Git usage.",
"examples": [
{"label": "Staging and committing", "code":
"""# Stage specific files
git add file1.py file2.py

# Stage all changes in current directory
git add .

# Stage all tracked files (skip untracked)
git add -u

# Commit with a message
git commit -m "Add data loading and cleaning functions"

# Stage + commit tracked files in one step
git commit -am "Fix bug in feature extraction"

# Amend the last commit (fix message or add forgotten files)
git add forgotten_file.py
git commit --amend -m "Add data loading, cleaning, and forgotten_file" """},
{"label": "Viewing history with git log", "code":
"""# Basic log
git log

# Compact one-line format
git log --oneline

# Show last 5 commits
git log --oneline -5

# Show with graph (branch visualization)
git log --oneline --graph --all

# Show what changed in each commit
git log --oneline --stat

# Search commit messages
git log --grep="fix" --oneline

# Commits by a specific author
git log --author="Alice" --oneline

# Commits in a date range
git log --since="2024-01-01" --until="2024-02-01" --oneline"""},
{"label": "Comparing changes with git diff", "code":
"""# See unstaged changes (working dir vs staging)
git diff

# See staged changes (staging vs last commit)
git diff --staged

# Compare two commits
git diff abc123 def456

# Compare current branch with main
git diff main

# Show changes for a specific file
git diff -- src/model.py

# Show only file names that changed
git diff --name-only main

# Show word-level diff (great for text/notebooks)
git diff --word-diff"""},
{"label": "Undoing changes safely", "code":
"""# Unstage a file (keep changes in working dir)
git restore --staged file.py

# Discard changes in working directory (CAREFUL — irreversible!)
git restore file.py

# Undo last commit but keep changes staged
git reset --soft HEAD~1

# Undo last commit, unstage changes (keep in working dir)
git reset HEAD~1

# Create a new commit that reverses a previous one (safe!)
git revert abc123

# View what a file looked like in a past commit
git show HEAD~3:src/model.py"""},
],
"rw": {
    "title": "Clean Commit History for Code Review",
    "scenario": "Your team requires clean, descriptive commits for code review. Here's a real workflow showing how to write good commits while developing a feature.",
    "code":
"""# Good commit messages follow this pattern:
# <type>: <short description>
#
# Types: feat, fix, refactor, docs, test, chore

# Working on a feature — multiple small commits
git add src/preprocessing.py
git commit -m "feat: add missing value imputation for numerical columns"

git add src/preprocessing.py
git commit -m "feat: add categorical encoding with target encoder"

git add tests/test_preprocessing.py
git commit -m "test: add unit tests for preprocessing pipeline"

git add src/config.py
git commit -m "refactor: extract preprocessing params to config"

# View the clean history
git log --oneline -5
# abc1234 refactor: extract preprocessing params to config
# def5678 test: add unit tests for preprocessing pipeline
# ghi9012 feat: add categorical encoding with target encoder
# jkl3456 feat: add missing value imputation for numerical columns"""
},
"practice": {
    "title": "Build a Commit History",
    "desc": "Create a series of meaningful commits: create 3 Python files, commit each separately with descriptive messages, then use git log and git diff to explore the history.",
    "starter":
"""# TODO: Create src/load_data.py with a dummy function
# TODO: git add and commit with message "feat: add data loading module"
# TODO: Create src/clean_data.py with a dummy function
# TODO: git add and commit with message "feat: add data cleaning module"
# TODO: Modify src/load_data.py (add a new function)
# TODO: git diff to see the changes
# TODO: git add and commit with message "feat: add CSV validation to data loader"
# TODO: git log --oneline to see your 3 commits
# TODO: git log --stat to see files changed per commit"""
},
"todos": [
    "Create 3 files in sequence, committing each with a descriptive message following 'type: description' format",
    "Modify a committed file, then use git diff and git diff --staged to see the difference",
    "Practice git reset --soft HEAD~1 — undo a commit and recommit with a better message",
    "Use git log --grep='feat' to filter only feature commits in your history",
    "Try git revert on a specific commit and confirm the undo commit appears in git log",
],
},

{
"title": "3. Branching & Merging",
"desc": "Branches let you work on features, experiments, or fixes in isolation without affecting the main codebase. Merging combines branches back together.",
"examples": [
{"label": "Creating and switching branches", "code":
"""# List all branches (* = current)
git branch

# Create a new branch
git branch feature/add-model

# Switch to it
git switch feature/add-model
# or older syntax: git checkout feature/add-model

# Create AND switch in one command
git switch -c feature/add-model
# or: git checkout -b feature/add-model

# List all branches including remote
git branch -a

# Rename a branch
git branch -m old-name new-name

# Delete a merged branch
git branch -d feature/add-model

# Force delete an unmerged branch (CAREFUL!)
git branch -D experiment/failed-approach"""},
{"label": "Merging branches", "code":
"""# Merge feature branch into main
git switch main
git merge feature/add-model

# Three types of merge:
# 1. Fast-forward — main hasn't diverged, just moves pointer
#    (clean, linear history)
git merge feature/add-model  # fast-forward if possible

# 2. No fast-forward — always creates a merge commit
#    (preserves branch history)
git merge --no-ff feature/add-model

# 3. Squash — combines all branch commits into one
#    (clean main history)
git merge --squash feature/add-model
git commit -m "feat: add ML model training pipeline" """},
{"label": "Resolving merge conflicts", "code":
"""# When two branches modify the same lines, Git can't auto-merge
git merge feature/update-model
# CONFLICT (content): Merge conflict in src/model.py

# Open the file — Git marks conflicts like this:
# <<<<<<< HEAD
# model = RandomForestClassifier(n_estimators=100)
# =======
# model = XGBClassifier(n_estimators=200, learning_rate=0.1)
# >>>>>>> feature/update-model

# To resolve:
# 1. Edit the file — keep what you want, remove markers
# 2. Stage the resolved file
git add src/model.py
# 3. Complete the merge
git commit -m "merge: resolve model selection conflict, keep XGBoost"

# Abort a merge if things go wrong
git merge --abort"""},
{"label": "Common branching strategies", "code":
"""# Branch naming conventions:
# feature/   — new functionality
# fix/       — bug fixes
# experiment/— DS experiments (may be thrown away)
# hotfix/    — urgent production fixes
# docs/      — documentation updates

# Example: Data Science experiment workflow
git switch -c experiment/lstm-vs-transformer

# ... do your work, commit results ...
git add notebooks/lstm_experiment.ipynb
git commit -m "experiment: LSTM achieves 0.87 F1"

git add notebooks/transformer_experiment.ipynb
git commit -m "experiment: Transformer achieves 0.92 F1"

# Winner! Merge back
git switch main
git merge experiment/lstm-vs-transformer
git branch -d experiment/lstm-vs-transformer"""},
],
"rw": {
    "title": "Feature Branch Workflow for a DS Team",
    "scenario": "A 3-person data science team uses feature branches to work on different parts of a project simultaneously without stepping on each other's toes.",
    "code":
"""# Alice works on data preprocessing
git switch -c feature/preprocessing
# ... makes commits ...
git commit -m "feat: add outlier detection with IQR method"
git commit -m "feat: add feature scaling pipeline"

# Bob works on model training
git switch -c feature/model-training
# ... makes commits ...
git commit -m "feat: add XGBoost training with cross-validation"
git commit -m "feat: add hyperparameter search with Optuna"

# Carol works on evaluation
git switch -c feature/evaluation
# ... makes commits ...
git commit -m "feat: add classification report and confusion matrix"

# When ready, each person merges to main:
git switch main
git merge --no-ff feature/preprocessing
git merge --no-ff feature/model-training
git merge --no-ff feature/evaluation

# Clean up
git branch -d feature/preprocessing feature/model-training feature/evaluation

# View the branch history
git log --oneline --graph -10"""
},
"todos": [
    "Create a branch called 'experiment/test', make a commit, then delete it",
    "Practice a fast-forward merge and a no-ff merge — view git log --graph after each",
    "Deliberately create a merge conflict in a file, then resolve it manually",
    "Use git branch -a to list all local and remote branches",
    "Rename your current branch using git branch -m old-name new-name",
],
},

{
"title": "4. Remote Repositories — GitHub, GitLab, Bitbucket",
"desc": "Remote repos host your code in the cloud for backup, collaboration, and deployment. GitHub is the most popular platform for data science projects.",
"examples": [
{"label": "Connecting to a remote", "code":
"""# Add a remote (usually called 'origin')
git remote add origin https://github.com/username/my-project.git

# View remotes
git remote -v

# Push your code to the remote
git push -u origin main    # -u sets up tracking (first time only)

# Subsequent pushes
git push

# Clone an existing repo
git clone https://github.com/username/project.git
git clone https://github.com/username/project.git my-local-name

# Clone only the latest snapshot (faster for large repos)
git clone --depth 1 https://github.com/username/project.git"""},
{"label": "Pulling and fetching changes", "code":
"""# Fetch — download remote changes (doesn't modify your files)
git fetch origin

# See what changed on remote
git log origin/main --oneline -5

# Pull — fetch + merge (updates your files)
git pull origin main

# Pull with rebase (cleaner history)
git pull --rebase origin main

# If pull causes conflicts, resolve them then:
git add .
git rebase --continue   # if rebasing
# or
git commit              # if merging"""},
{"label": "Working with forks (open source contribution)", "code":
"""# 1. Fork a repo on GitHub (click Fork button)

# 2. Clone YOUR fork
git clone https://github.com/YOUR-USERNAME/project.git
cd project

# 3. Add the original repo as 'upstream'
git remote add upstream https://github.com/ORIGINAL-OWNER/project.git

# 4. Keep your fork updated
git fetch upstream
git switch main
git merge upstream/main
git push origin main

# 5. Create a branch for your contribution
git switch -c fix/typo-in-readme

# 6. Make changes, commit, push to YOUR fork
git commit -am "fix: correct typo in installation instructions"
git push origin fix/typo-in-readme

# 7. Open a Pull Request on GitHub (from your fork to original)"""},
],
"rw": {
    "title": "Setting Up a Team Repository",
    "scenario": "A data science team sets up a shared GitHub repo with branch protection, a good README, and collaboration rules.",
    "code":
"""# Team lead creates the repo
mkdir team-ml-project && cd team-ml-project
git init
git switch -c main

# Create essential files
cat > README.md << 'EOF'
# Churn Prediction Model

## Setup
pip install -r requirements.txt

## Project Structure
src/          — source code
notebooks/    — exploration notebooks
tests/        — unit tests
models/       — trained model artifacts (gitignored)
data/         — datasets (gitignored)

## Workflow
1. Create a branch: git switch -c feature/your-feature
2. Make changes and commit
3. Push and open a Pull Request
4. Get review, then merge
EOF

echo "pandas>=2.0\nscikit-learn>=1.3\nxgboost>=2.0" > requirements.txt

git add .
git commit -m "chore: initial project setup with README and requirements"

# Push to GitHub
git remote add origin https://github.com/team/churn-prediction.git
git push -u origin main

# On GitHub: Settings → Branches → Add rule for 'main':
#   ✓ Require pull request reviews
#   ✓ Require status checks to pass
#   ✓ No direct pushes to main"""
},
"practice": {
    "title": "Simulate a Collaboration Workflow",
    "desc": "Create a repo, simulate 2 developers by creating branches, making conflicting changes, and resolving the merge conflict.",
    "starter":
"""# TODO: Create a repo with a file src/config.py containing:
#   MODEL_TYPE = "random_forest"
#   N_ESTIMATORS = 100

# TODO: Create branch 'dev-alice', change MODEL_TYPE to "xgboost"
# TODO: Commit on dev-alice

# TODO: Switch back to main
# TODO: Create branch 'dev-bob', change MODEL_TYPE to "lightgbm"
# TODO: Commit on dev-bob

# TODO: Merge dev-alice into main (should work cleanly)
# TODO: Try to merge dev-bob into main (conflict!)
# TODO: Resolve the conflict, commit the merge
# TODO: git log --oneline --graph to see the result"""
},
"todos": [
    "Clone a public GitHub repo locally and inspect git remote -v",
    "Add a second remote called 'backup' pointing to a different URL, then remove it",
    "Use git fetch followed by git log origin/main --oneline -5 to preview remote changes",
    "Practice git pull --rebase and confirm your local commits sit on top of remote ones",
    "Fork a repo on GitHub, add the original as upstream, and sync your fork with upstream/main",
],
},

{
"title": "5. Pull Requests & Code Review",
"desc": "Pull requests (PRs) are how teams review and discuss code changes before merging. They're essential for quality, knowledge sharing, and catching bugs early.",
"examples": [
{"label": "Creating a pull request with GitHub CLI", "code":
"""# Install GitHub CLI: https://cli.github.com
# Authenticate
gh auth login

# Create a PR from current branch
gh pr create --title "feat: add feature engineering pipeline" \\
             --body "## Changes
- Added outlier detection
- Added feature scaling
- Added polynomial features

## Testing
- Unit tests pass
- Tested on sample dataset"

# Create a draft PR (not ready for review yet)
gh pr create --draft --title "WIP: experiment with LSTM model"

# List open PRs
gh pr list

# View PR details
gh pr view 42

# Check out someone's PR locally for testing
gh pr checkout 42"""},
{"label": "Reviewing a pull request", "code":
"""# View PR diff
gh pr diff 42

# Add a review comment
gh pr review 42 --comment --body "Looks good, but please add docstrings to the new functions"

# Approve a PR
gh pr review 42 --approve --body "LGTM! Great work on the preprocessing pipeline"

# Request changes
gh pr review 42 --request-changes --body "Please add error handling for missing columns"

# Merge a PR
gh pr merge 42 --merge    # regular merge commit
gh pr merge 42 --squash   # squash all commits into one
gh pr merge 42 --rebase   # rebase onto main"""},
{"label": "PR best practices for data science", "code":
"""# Good PR structure for DS projects:

# 1. Small, focused PRs (not 2000-line monsters)
# ✗ "Add entire ML pipeline" (1500 lines)
# ✓ "Add data preprocessing" → "Add model training" → "Add evaluation"

# 2. Clear description with context
# - What does this PR do?
# - Why is this change needed?
# - How was it tested?
# - Any metrics/results?

# 3. Include results for model changes
# "Model accuracy: 0.85 → 0.92 (+7pp)
#  F1 score: 0.82 → 0.89
#  Tested on holdout set (n=5,000)"

# 4. Don't include notebooks with outputs in PR
#   (outputs make diffs unreadable)
#   Clear outputs before committing:
jupyter nbconvert --clear-output --inplace notebook.ipynb"""},
],
"rw": {
    "title": "Complete PR Workflow",
    "scenario": "Walk through a complete pull request lifecycle — from creating a feature branch to merging after code review.",
    "code":
"""# 1. Start from updated main
git switch main
git pull origin main

# 2. Create feature branch
git switch -c feature/add-cross-validation

# 3. Make changes (multiple small commits)
git add src/evaluation.py
git commit -m "feat: add k-fold cross-validation function"

git add tests/test_evaluation.py
git commit -m "test: add CV tests with synthetic data"

git add src/config.py
git commit -m "chore: add CV_FOLDS parameter to config"

# 4. Push branch to remote
git push -u origin feature/add-cross-validation

# 5. Create PR
gh pr create --title "feat: add k-fold cross-validation" \\
  --body "## Summary
- Added stratified k-fold CV with configurable folds
- Default: 5 folds (set in config.py)
- Returns mean ± std for each metric

## Test Plan
- [x] Unit tests pass
- [x] Tested on iris dataset (accuracy: 0.96 ± 0.02)

## Metrics
| Metric | Before (holdout) | After (5-fold CV) |
|--------|------------------|--------------------|
| Accuracy | 0.94 | 0.96 ± 0.02 |"

# 6. After review and approval
gh pr merge --squash"""
},
"todos": [
    "Install GitHub CLI (gh) and authenticate with gh auth login",
    "Create a feature branch, push it, and open a PR using gh pr create",
    "Use gh pr checkout to check out a teammate's PR locally and run the tests",
    "Write a PR description that includes: what changed, why, and model metrics",
    "Practice merging a PR with --squash and verify git log shows a single clean commit",
],
},

{
"title": "6. .gitignore for Data Science",
"desc": "A well-crafted .gitignore prevents large data files, model artifacts, credentials, and OS junk from entering your repository. This is critical for DS projects.",
"examples": [
{"label": "Comprehensive DS .gitignore", "code":
"""# .gitignore for Data Science projects

# ─── Data files ─────────────────────────────
*.csv
*.tsv
*.parquet
*.feather
*.h5
*.hdf5
*.sqlite
*.db
data/raw/
data/processed/
data/external/

# ─── Model artifacts ────────────────────────
*.pkl
*.pickle
*.joblib
*.pt
*.pth
*.h5
*.onnx
*.pmml
models/

# ─── Notebooks ──────────────────────────────
.ipynb_checkpoints/
*/.ipynb_checkpoints/

# ─── Python ─────────────────────────────────
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
*.so

# ─── Environments ───────────────────────────
.env
.venv/
venv/
env/
*.env.local

# ─── IDE ────────────────────────────────────
.vscode/
.idea/
*.swp
*.swo
*~

# ─── OS ─────────────────────────────────────
.DS_Store
Thumbs.db
desktop.ini

# ─── Logs & temp ────────────────────────────
*.log
logs/
tmp/
.cache/
wandb/
mlruns/""", "lang": "text"},
{"label": "Useful .gitignore patterns", "code":
"""# Ignore everything in a directory, but keep the directory
data/raw/*
!data/raw/.gitkeep

# Ignore all CSVs except a specific one
*.csv
!reference_data.csv

# Ignore files only in root (not subdirectories)
/config.local.py

# Ignore by directory depth
**/logs/       # ignore 'logs' at any depth
debug/         # ignore 'debug' only at root

# Negate a pattern (un-ignore)
*.h5
!models/production_model.h5

# Check what's ignored
git status --ignored

# Check if a specific file is ignored
git check-ignore -v data/train.csv"""},
{"label": "Fixing accidentally committed files", "code":
"""# Oops! You committed a large CSV file
# Remove from Git tracking (keep the file locally)
git rm --cached data/large_dataset.csv
echo "data/large_dataset.csv" >> .gitignore
git add .gitignore
git commit -m "chore: remove large CSV from tracking, add to gitignore"

# Remove an entire directory from tracking
git rm -r --cached __pycache__/
git commit -m "chore: remove pycache from tracking"

# Nuclear option: remove file from ALL history (if it contained secrets)
# WARNING: rewrites history, coordinate with team!
git filter-branch --force --index-filter \\
  'git rm --cached --ignore-unmatch secrets.env' \\
  --prune-empty -- --all

# Better tool for history rewriting:
# pip install git-filter-repo
# git filter-repo --invert-paths --path secrets.env"""},
],
"rw": {
    "title": "Auditing a Repo for Sensitive Files",
    "scenario": "Before making a private repo public, you need to check for accidentally committed secrets, large files, and sensitive data.",
    "code":
"""# Check for large files in history
git rev-list --objects --all | \\
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \\
  awk '/^blob/ {print $3, $4}' | \\
  sort -rn | head -20

# Search for potential secrets in commit history
git log --all -p | grep -i "password\\|secret\\|api_key\\|token" | head -20

# List all file types ever committed
git log --all --diff-filter=A --name-only --pretty=format: | \\
  grep -o '\\.[^.]*$' | sort | uniq -c | sort -rn

# Check current gitignore coverage
git status --ignored --short

# Verify no .env files in history
git log --all --full-history -- "*.env" --oneline

# Verify no large files currently tracked
git ls-files | xargs -I{} git cat-file -s HEAD:{} 2>/dev/null | \\
  sort -rn | head -10"""
},
"todos": [
    "Create a .gitignore from scratch for a Python DS project covering data, models, envs, and OS files",
    "Accidentally commit a .csv file, then use git rm --cached to untrack it without deleting locally",
    "Use git check-ignore -v on several file paths to confirm they are properly ignored",
    "Use the !negation pattern to ignore all *.h5 files but keep one specific model file",
    "Run git status --ignored to audit what is currently being ignored in your repo",
],
},

{
"title": "7. Git Stash — Saving Work Temporarily",
"desc": "Stash lets you save uncommitted changes temporarily so you can switch branches, pull updates, or do other work, then come back to your changes later.",
"examples": [
{"label": "Basic stash operations", "code":
"""# Save current changes to stash
git stash

# Save with a description
git stash push -m "WIP: feature engineering experiments"

# List all stashes
git stash list
# stash@{0}: On feature/model: WIP: feature engineering experiments
# stash@{1}: On main: quick debug session

# Apply most recent stash (keep it in stash list)
git stash apply

# Apply and remove from stash list
git stash pop

# Apply a specific stash
git stash apply stash@{1}

# Remove a specific stash
git stash drop stash@{0}

# Clear all stashes
git stash clear"""},
{"label": "Advanced stash usage", "code":
"""# Stash including untracked files
git stash push -u -m "WIP: including new files"

# Stash only specific files
git stash push -m "stash only model.py" -- src/model.py

# View what's in a stash
git stash show stash@{0}         # summary
git stash show -p stash@{0}      # full diff

# Create a branch from a stash
git stash branch new-feature stash@{0}

# Common workflow: quick context switch
# You're working on feature A, need to fix urgent bug
git stash push -m "WIP: feature A halfway done"
git switch main
git switch -c hotfix/urgent-bug
# ... fix the bug, commit, merge ...
git switch feature-a
git stash pop  # back to where you were!"""},
],
"rw": {
    "title": "Stash Workflow for Interruptions",
    "scenario": "You're deep in model training code when a colleague needs an urgent bug fix on main. Stash saves your context so you can switch and return seamlessly.",
    "code":
"""# You're on feature/train-pipeline with uncommitted changes
git status
# Modified: src/train.py, src/metrics.py (not ready to commit)

# Urgent bug report! Stash everything
git stash push -u -m "WIP: training pipeline refactor"

# Fix the bug
git switch main
git pull
git switch -c hotfix/data-loader-crash
# ... fix the bug ...
git commit -am "fix: handle empty DataFrame in data loader"
git push -u origin hotfix/data-loader-crash
# ... create PR, get it merged ...

# Return to your work
git switch feature/train-pipeline
git stash pop
# Your changes are back exactly as you left them!
git status"""
},
"todos": [
    "Make some uncommitted edits, run git stash push -m 'my wip', then verify git status is clean",
    "Create two stashes, list them with git stash list, and apply each one selectively",
    "Use git stash show -p stash@{0} to inspect the full diff stored in a stash",
    "Stash only a single file using git stash push -- path/to/file.py",
    "Create a branch directly from a stash using git stash branch and confirm changes are there",
],
},

{
"title": "8. Tags & Releases",
"desc": "Tags mark specific points in history — typically used for version releases, model checkpoints, and experiment milestones. They create permanent bookmarks in your Git history.",
"examples": [
{"label": "Creating and managing tags", "code":
"""# Lightweight tag (just a pointer)
git tag v1.0.0

# Annotated tag (recommended — includes message, author, date)
git tag -a v1.0.0 -m "First production release"

# Tag a past commit
git tag -a v0.9.0 -m "Beta release" abc1234

# List tags
git tag
git tag -l "v1.*"    # filter by pattern

# View tag details
git show v1.0.0

# Push tags to remote
git push origin v1.0.0      # push one tag
git push origin --tags       # push all tags

# Delete a tag
git tag -d v0.1.0            # local
git push origin --delete v0.1.0  # remote"""},
{"label": "Semantic versioning for ML projects", "code":
"""# Semantic Versioning: MAJOR.MINOR.PATCH
# MAJOR — breaking changes (new model architecture, API change)
# MINOR — new features (added endpoint, new feature engineering)
# PATCH — bug fixes (fixed preprocessing bug, typo)

# ML-specific versioning strategy:
# v1.0.0 — first production model
# v1.1.0 — added new features to model
# v1.1.1 — fixed data preprocessing bug
# v2.0.0 — switched from RF to XGBoost (different model)

# Tag with model metrics
git tag -a v2.1.0 -m "XGBoost v2.1
Accuracy: 0.94
F1: 0.91
AUC: 0.97
Training data: 2024-01-01 to 2024-06-30
Features: 47 (added 5 new interaction features)"

# Create a GitHub release (includes downloadable assets)
gh release create v2.1.0 --title "Model v2.1.0" \\
  --notes "Improved model with 5 new interaction features.
  Accuracy: 0.94 (+2pp vs v2.0.0)"
"""},
],
"rw": {
    "title": "Release Workflow for ML Models",
    "scenario": "A team uses tags to version their ML model releases, making it easy to roll back to any previous model version in production.",
    "code":
"""# After model training and validation passes
git add src/ tests/ configs/
git commit -m "feat: XGBoost v2 with optimized hyperparameters"

# Tag the release with metrics
git tag -a model-v2.1.0 -m "Production model release
Model: XGBoost
Accuracy: 0.943 | F1: 0.912 | AUC: 0.971
Training samples: 150,000
Feature count: 47
Hyperparams: max_depth=6, lr=0.05, n_est=500"

# Push code and tag
git push origin main --tags

# Create GitHub release with model card
gh release create model-v2.1.0 \\
  --title "Model v2.1.0 — XGBoost Production" \\
  --notes-file RELEASE_NOTES.md

# Later: need to roll back to v2.0.0
git checkout model-v2.0.0 -- src/model.py configs/model_config.yaml
# This restores just the model files from the v2.0.0 tag"""
},
"todos": [
    "Create an annotated tag on your current commit with version, model metrics, and a short description",
    "Push your tag to a remote and verify it appears under Releases on GitHub",
    "Use git tag -l 'v*' to list all version tags and git show to inspect one",
    "Delete a local tag with git tag -d, recreate it on a different commit, then push --tags",
    "Use git checkout <tag> -- file.py to restore a single file from a specific tagged version",
],
},

{
"title": "9. Rebase & Interactive Rebase",
"desc": "Rebase replays your commits on top of another branch, creating a linear history. Interactive rebase lets you edit, squash, reorder, and clean up commits before sharing.",
"examples": [
{"label": "Basic rebase", "code":
"""# Instead of merging main into your branch (creates merge commit):
git switch feature/model
git merge main  # creates a merge commit

# Rebase puts your commits on TOP of main (linear history):
git switch feature/model
git rebase main

# After rebase, your branch looks like:
# main: A—B—C
# feature:     D—E—F  (your commits replayed on top of C)

# If conflicts occur during rebase:
git add resolved_file.py
git rebase --continue

# Abort if things go wrong
git rebase --abort"""},
{"label": "Interactive rebase — cleaning up commits", "code":
"""# Clean up last 4 commits before creating a PR
git rebase -i HEAD~4

# Opens editor with:
# pick abc1234 WIP: start model training
# pick def5678 fix typo
# pick ghi9012 more work on training
# pick jkl3456 finish model training

# Change to:
# pick abc1234 WIP: start model training
# squash def5678 fix typo              ← merge into previous
# squash ghi9012 more work on training ← merge into previous
# reword jkl3456 finish model training ← change message

# Commands:
# pick   — keep the commit as is
# squash — merge into previous commit
# fixup  — like squash but discard this commit's message
# reword — keep commit, edit message
# edit   — pause to amend the commit
# drop   — delete the commit"""},
{"label": "The golden rule of rebase", "code":
"""# NEVER rebase commits that have been pushed and shared with others!
# Rebase rewrites history — this will cause problems for collaborators

# Safe: rebase your LOCAL commits before pushing
git switch feature/my-work
git rebase main        # OK — only your local commits
git push               # push clean history

# DANGEROUS: rebase after pushing
git push origin feature/my-work
git rebase main        # Rewrites already-pushed commits!
git push --force       # Forces overwrite — breaks collaborators!

# If you must update after push, use merge instead:
git switch feature/my-work
git merge main         # Safe even after pushing"""},
],
"rw": {
    "title": "Cleaning Messy History Before PR",
    "scenario": "You made 8 messy commits during development (including 'WIP', 'fix typo', 'oops'). Clean them into 3 logical commits before requesting code review.",
    "code":
"""# Your messy history:
# abc1234 oops, forgot to save
# def5678 fix import
# ghi9012 WIP: add feature scaling
# jkl3456 fix bug in scaling
# mno7890 add model training
# pqr1234 fix typo in training
# stu5678 add evaluation metrics
# vwx9012 fix metric calculation

# Interactive rebase to clean up
git rebase -i HEAD~8

# Result after squashing related commits:
# pick ghi9012 feat: add feature scaling pipeline
# pick mno7890 feat: add model training with XGBoost
# pick stu5678 feat: add evaluation metrics (accuracy, F1, AUC)

# Now push the clean branch
git push origin feature/ml-pipeline

# Your PR will show 3 clean, logical commits instead of 8 messy ones"""
},
"todos": [
    "Make 4 small commits (including 'WIP' and 'fix typo'), then squash them into 1 with git rebase -i",
    "Use git rebase main on a feature branch and compare the log to a merge-based approach",
    "Practice the 'reword' command in interactive rebase to rename a commit message",
    "Use 'drop' in interactive rebase to delete a commit entirely and verify it's gone in git log",
    "Rebase a branch with a conflict — resolve it, then complete with git rebase --continue",
],
},

{
"title": "10. Git for Jupyter Notebooks",
"desc": "Notebooks are JSON files with embedded outputs, making them hard to diff and version. These techniques keep notebooks manageable in Git.",
"examples": [
{"label": "The notebook problem and solutions", "code":
"""# Jupyter notebooks (.ipynb) are JSON — diffs are messy:
# - Cell outputs (images, tables) bloat the repo
# - Execution counts change on every run
# - Cell metadata changes randomly
# - Merge conflicts are nearly impossible to resolve

# Solution 1: Clear outputs before committing
jupyter nbconvert --clear-output --inplace notebook.ipynb
git add notebook.ipynb
git commit -m "feat: add EDA notebook (outputs cleared)"

# Solution 2: Automate with pre-commit hook
# .pre-commit-config.yaml
# repos:
#   - repo: https://github.com/kynan/nbstripout
#     hooks:
#       - id: nbstripout

# Solution 3: Install nbstripout globally for a repo
pip install nbstripout
nbstripout --install         # adds Git filter
# Now outputs are automatically stripped on commit!""", "lang": "bash"},
{"label": "nbdime — better notebook diffs", "code":
"""# Install nbdime for human-readable notebook diffs
pip install nbdime

# Configure Git to use nbdime
nbdime config-git --enable --global

# Now 'git diff' shows notebook changes in a readable format
git diff notebook.ipynb
# Instead of raw JSON, you see:
# Cell 3 (code):
# -  model = RandomForestClassifier()
# +  model = XGBClassifier(n_estimators=200)

# Visual diff tool (opens in browser)
nbdime diff notebook_v1.ipynb notebook_v2.ipynb

# Merge tool for notebooks
nbdime merge base.ipynb local.ipynb remote.ipynb""", "lang": "bash"},
{"label": "Pairing notebooks with .py scripts", "code":
"""# Use jupytext to sync .ipynb with .py files
pip install jupytext

# Convert notebook to Python script
jupytext --to py:percent notebook.ipynb
# Creates notebook.py with # %% cell markers

# Sync both formats (edit either one)
jupytext --set-formats ipynb,py:percent notebook.ipynb

# In .gitignore, you can then ignore .ipynb and only track .py:
# *.ipynb    ← ignore notebooks
# !*.py      ← track Python scripts

# Or track both but strip outputs from .ipynb:
# Use nbstripout for .ipynb
# Track .py as the "source of truth" """, "lang": "bash"},
],
"rw": {
    "title": "Notebook Workflow for a DS Team",
    "scenario": "A team establishes a clean workflow for sharing Jupyter notebooks through Git without the usual pain of merge conflicts and bloated diffs.",
    "code":
"""# Team setup (run once)
pip install nbstripout nbdime jupytext

# In the project repo
nbstripout --install
nbdime config-git --enable

# Team convention:
# 1. Notebooks in notebooks/ directory
# 2. Outputs always stripped on commit (nbstripout)
# 3. Each notebook has a paired .py script (jupytext)
# 4. PRs review the .py diff (much cleaner)
# 5. Final notebooks with outputs go to reports/

# Example workflow
cd notebooks/
jupytext --set-formats ipynb,py:percent eda.ipynb

# Edit the notebook, run cells, then:
git add notebooks/eda.py          # clean Python diff
git add notebooks/eda.ipynb       # outputs auto-stripped
git commit -m "feat: add EDA notebook with correlation analysis"

# Reviewer sees clean diff in eda.py, not messy JSON"""
},
"practice": {
    "title": "Set Up Notebook-Friendly Git",
    "desc": "Configure a repo for clean notebook versioning: install nbstripout, create a .gitattributes for notebooks, and test that outputs are stripped on commit.",
    "starter":
"""# TODO: Create a test repo
# TODO: pip install nbstripout
# TODO: nbstripout --install (in the repo)
# TODO: Create a simple notebook with some output cells
# TODO: git add and commit the notebook
# TODO: Check that the committed version has no outputs:
#   git show HEAD:notebook.ipynb | python -c "
#   import json, sys
#   nb = json.load(sys.stdin)
#   outputs = sum(len(c.get('outputs',[])) for c in nb['cells'])
#   print(f'Outputs in committed notebook: {outputs}')
#   " """
},
"todos": [
    "Install nbstripout, run nbstripout --install in a repo, then commit a notebook and verify outputs are gone",
    "Install jupytext and convert a notebook to a .py:percent script — commit both and compare diffs",
    "Run nbdime config-git --enable then use git diff on a changed notebook to see the readable output",
    "Deliberately commit a notebook with outputs, then use git rm --cached to untrack and strip it",
    "Add .ipynb_checkpoints/ to .gitignore and confirm checkpoint folders no longer appear in git status",
],
},

{
"title": "11. Git Hooks & Automation",
"desc": "Git hooks are scripts that run automatically at specific points in the Git workflow — before commits, before pushes, etc. They automate code quality checks.",
"examples": [
{"label": "Common hooks for data science", "code":
"""# Hooks live in .git/hooks/ (local, not shared by default)
# Use pre-commit framework to share hooks with team

# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml in repo root
cat > .pre-commit-config.yaml << 'EOF'
repos:
  # Code formatting
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3

  # Import sorting
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  # Linting
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120]

  # Strip notebook outputs
  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks:
      - id: nbstripout

  # Check for secrets
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
EOF

# Install the hooks
pre-commit install

# Now these checks run automatically before every commit!
# To run manually on all files:
pre-commit run --all-files""", "lang": "bash"},
{"label": "Custom pre-commit hook", "code":
"""# Create a custom hook that checks for large files
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
# Prevent commits with files larger than 5MB

MAX_SIZE=5242880  # 5MB in bytes
EXIT_CODE=0

for file in $(git diff --cached --name-only); do
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        if [ "$size" -gt "$MAX_SIZE" ]; then
            echo "ERROR: $file is $(($size/1048576))MB (max 5MB)"
            echo "  Use Git LFS for large files: git lfs track '$file'"
            EXIT_CODE=1
        fi
    fi
done

exit $EXIT_CODE
HOOK

chmod +x .git/hooks/pre-commit""", "lang": "bash"},
],
"rw": {
    "title": "Automated Quality Gates for ML Projects",
    "scenario": "A team sets up pre-commit hooks that enforce code formatting, prevent secrets from being committed, and validate that model configs are valid JSON.",
    "code":
"""# .pre-commit-config.yaml with DS-specific hooks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: no-commit-to-branch
        args: [--branch, main]   # prevent direct commits to main

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks:
      - id: nbstripout

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]
EOF

pre-commit install
pre-commit run --all-files

# Now every commit is automatically checked!
# Team members just need to run: pre-commit install"""
},
"todos": [
    "Install pre-commit, create a .pre-commit-config.yaml with black, and run pre-commit install",
    "Run pre-commit run --all-files on a project and fix any formatting issues it reports",
    "Write a custom .git/hooks/pre-commit shell script that rejects commits with 'TODO' in staged files",
    "Add the check-added-large-files hook and verify it blocks a file larger than your threshold",
    "Add detect-secrets to your hooks and confirm it catches a fake API key you add to a test file",
],
},

{
"title": "12. Git LFS — Large File Storage",
"desc": "Git LFS stores large files (datasets, model weights, images) outside the Git repo while keeping references in your history. Essential for ML projects with large artifacts.",
"examples": [
{"label": "Setting up Git LFS", "code":
"""# Install Git LFS
git lfs install

# Track specific file types
git lfs track "*.csv"
git lfs track "*.parquet"
git lfs track "*.pkl"
git lfs track "*.pt"
git lfs track "*.h5"
git lfs track "data/**"

# This creates/updates .gitattributes
cat .gitattributes
# *.csv filter=lfs diff=lfs merge=lfs -text
# *.parquet filter=lfs diff=lfs merge=lfs -text

# IMPORTANT: commit .gitattributes first!
git add .gitattributes
git commit -m "chore: configure Git LFS for data and model files"

# Now add large files normally — LFS handles them
git add data/training_set.csv
git commit -m "data: add training dataset"
git push"""},
{"label": "Managing LFS files", "code":
"""# List tracked LFS patterns
git lfs track

# List actual LFS files in repo
git lfs ls-files

# Check LFS storage usage
git lfs env

# Pull LFS files (after clone)
git lfs pull

# Clone without downloading LFS files (faster)
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/user/project.git

# Download LFS files for specific patterns only
git lfs pull --include="data/train*"
git lfs pull --exclude="models/"

# Migrate existing files to LFS
git lfs migrate import --include="*.csv" --everything"""},
],
"rw": {
    "title": "LFS for ML Model Versioning",
    "scenario": "A team uses Git LFS to version model weights alongside code, so every tagged release includes the exact model binary that was deployed.",
    "code":
"""# Initial setup
git lfs install
git lfs track "models/*.pkl"
git lfs track "models/*.pt"
git lfs track "models/*.onnx"
git add .gitattributes
git commit -m "chore: track model files with Git LFS"

# After training a new model
cp trained_model.pkl models/churn_model.pkl
git add models/churn_model.pkl
git commit -m "model: XGBoost churn model v2.1 (F1=0.91)"
git tag -a model-v2.1.0 -m "Churn model v2.1.0, F1=0.91"
git push origin main --tags

# To reproduce: checkout the tag, model files are pulled automatically
git checkout model-v2.1.0
ls -la models/  # model file is there via LFS

# Check LFS storage
git lfs ls-files --size
# models/churn_model.pkl (245 MB)"""
},
"todos": [
    "Run git lfs install, track *.pkl files, commit .gitattributes, and add a dummy pkl file",
    "Use git lfs ls-files to confirm which files are stored via LFS in your repo",
    "Clone a repo using GIT_LFS_SKIP_SMUDGE=1 and verify LFS files are only pointers",
    "Use git lfs pull --include='data/train*' to selectively download only the files you need",
    "Check git lfs env to inspect your LFS storage quota and endpoint configuration",
],
},

{
"title": "13. Advanced Git — cherry-pick, bisect, reflog",
"desc": "Power-user Git commands for specific situations: applying individual commits across branches, finding which commit introduced a bug, and recovering lost work.",
"examples": [
{"label": "Cherry-pick — apply specific commits", "code":
"""# Copy a specific commit from another branch
git cherry-pick abc1234

# Cherry-pick without committing (stage changes only)
git cherry-pick --no-commit abc1234

# Cherry-pick a range of commits
git cherry-pick abc1234..def5678

# Use case: backport a bug fix from development to production
git switch production
git cherry-pick abc1234  # the fix commit from dev branch
git push

# If conflicts occur
git cherry-pick --continue  # after resolving
git cherry-pick --abort     # to cancel"""},
{"label": "Git bisect — find the bug-introducing commit", "code":
"""# Binary search through history to find which commit broke something
git bisect start

# Mark current commit as bad (bug is present)
git bisect bad

# Mark a known good commit (bug was NOT present)
git bisect good v1.0.0

# Git checks out a middle commit — test it!
# If the bug is present:
git bisect bad
# If the bug is NOT present:
git bisect good

# Repeat until Git finds the exact commit
# "abc1234 is the first bad commit"

# Done — go back to normal
git bisect reset

# Automated bisect with a test script:
git bisect start HEAD v1.0.0
git bisect run python -m pytest tests/test_model.py -x
# Git automatically finds the first failing commit!"""},
{"label": "Reflog — recover lost work", "code":
"""# Reflog tracks every HEAD movement — your safety net!
git reflog
# abc1234 HEAD@{0}: commit: add feature
# def5678 HEAD@{1}: checkout: moving from main to feature
# ghi9012 HEAD@{2}: commit: initial commit

# Accidentally deleted a branch? Recover it!
git branch -D important-branch  # oops!
git reflog  # find the last commit on that branch
git branch important-branch HEAD@{3}  # recovered!

# Accidentally ran git reset --hard? Recover!
git reset --hard HEAD~5  # oops, lost 5 commits!
git reflog  # find where HEAD was before
git reset --hard HEAD@{1}  # back to before the reset!

# Reflog entries expire after 90 days (default)
# Check expiry:
git config gc.reflogExpire"""},
],
"rw": {
    "title": "Debugging a Model Regression with Bisect",
    "scenario": "Your model's accuracy dropped from 0.94 to 0.87 somewhere in the last 20 commits. Use git bisect with an automated test to find exactly which commit caused the regression.",
    "code":
"""# Create a test script that checks model accuracy
cat > test_accuracy.sh << 'SCRIPT'
#!/bin/bash
# Returns 0 (good) if accuracy > 0.90, 1 (bad) otherwise
python -c "
from src.model import train_and_evaluate
accuracy = train_and_evaluate('data/test.csv')
print(f'Accuracy: {accuracy:.4f}')
exit(0 if accuracy > 0.90 else 1)
"
SCRIPT
chmod +x test_accuracy.sh

# Automated bisect
git bisect start
git bisect bad HEAD                    # current commit is bad
git bisect good HEAD~20                # 20 commits ago was good
git bisect run ./test_accuracy.sh      # automated testing!

# Output: "abc1234 is the first bad commit"
# commit abc1234
# Author: Bob <bob@company.com>
# Date: Mon Jan 15 14:30:00 2024
# "refactor: change feature scaling to min-max"

# Found it! The scaling change caused the regression
git bisect reset
rm test_accuracy.sh"""
},
"todos": [
    "Use git cherry-pick to copy a single bug-fix commit from one branch to another",
    "Run git bisect manually on a small repo — mark bad and good commits until Git finds the culprit",
    "Automate git bisect with a test script using git bisect run python -m pytest",
    "Accidentally delete a branch, then recover it using git reflog and git branch",
    "Run git reset --hard HEAD~2, then use git reflog to recover the two lost commits",
],
},

{
"title": "14. Git Workflows for Teams",
"desc": "Different teams use different branching strategies. Understanding these workflows helps you adapt to any team's Git practices.",
"examples": [
{"label": "GitHub Flow (simple, recommended for most teams)", "code":
"""# GitHub Flow — simple and effective
# Rules:
# 1. main is always deployable
# 2. Create feature branches from main
# 3. Open PRs for review
# 4. Merge to main after approval
# 5. Deploy from main

# Workflow:
git switch main
git pull
git switch -c feature/add-prediction-endpoint

# Work, commit, push
git commit -am "feat: add /predict endpoint"
git push -u origin feature/add-prediction-endpoint

# Create PR → Review → Merge → Delete branch
gh pr create
# After merge:
git switch main
git pull
git branch -d feature/add-prediction-endpoint"""},
{"label": "Git Flow (for versioned releases)", "code":
"""# Git Flow — more structured, good for versioned software
# Branches:
# main     — production releases only
# develop  — integration branch
# feature/ — new features (branch from develop)
# release/ — preparing a release (branch from develop)
# hotfix/  — urgent fixes (branch from main)

# Start a feature
git switch develop
git switch -c feature/new-model

# Finish feature — merge back to develop
git switch develop
git merge --no-ff feature/new-model
git branch -d feature/new-model

# Prepare release
git switch -c release/v2.0.0
# ... final testing, version bumps ...
git switch main
git merge --no-ff release/v2.0.0
git tag -a v2.0.0 -m "Release v2.0.0"
git switch develop
git merge --no-ff release/v2.0.0
git branch -d release/v2.0.0"""},
{"label": "Trunk-based development (for fast-moving teams)", "code":
"""# Trunk-based — everyone commits to main (or very short-lived branches)
# Rules:
# 1. Small, frequent commits to main
# 2. Feature flags instead of long-lived branches
# 3. Branches live < 1 day
# 4. CI/CD runs on every commit

# Short-lived branch (< 1 day)
git switch -c fix/null-check
git commit -am "fix: handle null values in preprocessing"
git push -u origin fix/null-check
gh pr create
# Get quick review, merge same day

# Feature flags for larger features
# In code:
# if feature_flags.is_enabled("new_model_v2"):
#     prediction = new_model.predict(features)
# else:
#     prediction = old_model.predict(features)"""},
],
"rw": {
    "title": "Choosing the Right Workflow",
    "scenario": "A data science team of 5 people needs to pick a Git workflow. Here's a decision framework based on team size, release cadence, and project type.",
    "code":
"""# Decision framework:

# Small team (2-5), continuous deployment → GitHub Flow
# - Simple, low overhead
# - Perfect for: web apps, APIs, dashboards
# - DS teams building Streamlit apps or APIs

# Medium team (5-15), versioned releases → Git Flow
# - Structured, parallel development
# - Perfect for: ML platforms, data products
# - DS teams shipping model versions

# Large team (15+), fast iteration → Trunk-based
# - Requires strong CI/CD
# - Perfect for: mature ML platforms
# - Feature flags replace branches

# For MOST data science teams, GitHub Flow is the best choice:
echo "Recommended: GitHub Flow"
echo "  ✓ Simple to learn"
echo "  ✓ Works well with PRs"
echo "  ✓ main is always deployable"
echo "  ✓ Low overhead for small teams"
echo "  ✓ GitHub/GitLab built around this workflow" """},
"todos": [
    "Implement a full GitHub Flow cycle: branch → commit → PR → merge → delete branch",
    "Set up a develop branch and practice the Git Flow feature branch → develop merge",
    "Create a hotfix branch from main, fix a bug, merge it to both main and develop",
    "Write down your team's current workflow and identify one improvement it could make",
    "Add a branch protection rule on main requiring PR review before any merge",
],
},

{
"title": "15. GitHub Actions for Data Science",
"desc": "Automate testing, linting, model validation, and deployment with GitHub Actions. CI/CD ensures your code always works and your models are validated before deployment.",
"examples": [
{"label": "Basic CI pipeline for a DS project", "code":
"""# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest flake8

      - name: Lint
        run: flake8 src/ --max-line-length=120

      - name: Run tests
        run: pytest tests/ -v --tb=short""", "lang": "yaml"},
{"label": "Model validation workflow", "code":
"""# .github/workflows/model-validation.yml
name: Model Validation

on:
  pull_request:
    paths:
      - 'src/model/**'
      - 'configs/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Train on test data
        run: python src/model/train.py --config configs/test.yaml

      - name: Validate metrics
        run: |
          python -c "
          import json
          with open('results/metrics.json') as f:
              m = json.load(f)
          assert m['accuracy'] > 0.85, f'Accuracy {m[\"accuracy\"]} below threshold'
          assert m['f1'] > 0.80, f'F1 {m[\"f1\"]} below threshold'
          print('Model validation passed!')
          print(f'Accuracy: {m[\"accuracy\"]:.4f}')
          print(f'F1: {m[\"f1\"]:.4f}')
          " """, "lang": "yaml"},
{"label": "Scheduled data pipeline", "code":
"""# .github/workflows/daily-data.yml
name: Daily Data Collection

on:
  schedule:
    - cron: '0 6 * * *'  # Run at 6 AM UTC daily
  workflow_dispatch:       # Allow manual trigger

jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Collect data
        env:
          API_KEY: ${{ secrets.DATA_API_KEY }}
        run: python scripts/collect_daily_data.py

      - name: Commit new data
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add data/daily/
          git diff --staged --quiet || git commit -m "data: daily collection $(date +%Y-%m-%d)"
          git push""", "lang": "yaml"},
],
"rw": {
    "title": "Full CI/CD for an ML Project",
    "scenario": "A team sets up GitHub Actions to automatically test code, validate model performance, build Docker images, and deploy to production on every merge to main.",
    "code":
"""# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: black --check src/
      - run: pytest tests/ -v

  model-check:
    needs: quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: python scripts/validate_model.py
      - name: Comment metrics on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const metrics = fs.readFileSync('results/metrics.txt', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '## Model Metrics\\n```\\n' + metrics + '\\n```'
            })""", "lang": "yaml"},
"todos": [
    "Create a .github/workflows/ci.yml that installs dependencies and runs pytest on every push",
    "Add a flake8 linting step to your CI workflow and make it fail on style violations",
    "Set up a workflow that only triggers on changes to src/model/ using the paths filter",
    "Store a fake API key as a GitHub Actions secret and reference it in a workflow as ${{ secrets.MY_KEY }}",
    "Use workflow_dispatch to add a manual trigger to an existing workflow and run it from the GitHub UI",
],
},

{
"title": "16. Git Best Practices Cheat Sheet",
"desc": "A collection of Git best practices, common pitfalls, and quick reference commands for daily use.",
"examples": [
{"label": "Daily workflow cheat sheet", "code":
"""# Morning: start fresh
git switch main
git pull origin main
git switch -c feature/todays-work

# During the day: small, frequent commits
git add src/module.py
git commit -m "feat: add data validation step"

# End of day: push your work
git push -u origin feature/todays-work

# Ready for review: create PR
gh pr create --title "feat: add data validation"

# After PR is merged: clean up
git switch main
git pull
git branch -d feature/todays-work"""},
{"label": "Common mistakes and fixes", "code":
"""# Mistake: committed to wrong branch
git switch correct-branch
git cherry-pick abc1234    # bring commit to correct branch
git switch wrong-branch
git reset HEAD~1           # remove from wrong branch

# Mistake: typo in last commit message
git commit --amend -m "correct message here"

# Mistake: forgot to add a file to last commit
git add forgotten_file.py
git commit --amend --no-edit

# Mistake: committed sensitive data
git reset --soft HEAD~1    # undo commit, keep changes staged
# remove the sensitive data, then recommit

# Mistake: git pull created ugly merge commits
git reset --hard HEAD~1    # undo the merge
git pull --rebase          # replay your commits on top

# Mistake: need to undo a pushed commit (safely)
git revert abc123         # creates a new "undo" commit
git push"""},
{"label": "Useful aliases for productivity", "code":
"""# Add these to your ~/.gitconfig [alias] section:
git config --global alias.st "status --short"
git config --global alias.co "checkout"
git config --global alias.sw "switch"
git config --global alias.br "branch"
git config --global alias.ci "commit"
git config --global alias.lg "log --oneline --graph --all -20"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "restore --staged"
git config --global alias.undo "reset HEAD~1"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.wip "commit -am 'WIP: work in progress'"

# Usage:
# git st          → short status
# git lg          → pretty graph log
# git last        → last commit details
# git unstage f   → unstage a file
# git undo        → undo last commit (keep changes)
# git amend       → add to last commit
# git wip         → quick WIP commit"""},
{"label": "Git command reference table", "code":
"""# ┌─────────────────────┬────────────────────────────────────┐
# │ Action               │ Command                            │
# ├─────────────────────┼────────────────────────────────────┤
# │ Init repo            │ git init                           │
# │ Clone repo           │ git clone <url>                    │
# │ Stage files          │ git add <files>                    │
# │ Commit               │ git commit -m "msg"                │
# │ Push                 │ git push origin <branch>           │
# │ Pull                 │ git pull origin <branch>           │
# │ Status               │ git status                         │
# │ Log                  │ git log --oneline                  │
# │ Diff                 │ git diff                           │
# │ Create branch        │ git switch -c <name>               │
# │ Switch branch        │ git switch <name>                  │
# │ Merge                │ git merge <branch>                 │
# │ Rebase               │ git rebase <branch>                │
# │ Stash                │ git stash push -m "msg"            │
# │ Tag                  │ git tag -a v1.0 -m "msg"           │
# │ Cherry-pick          │ git cherry-pick <hash>             │
# │ Bisect               │ git bisect start                   │
# │ Undo last commit     │ git reset HEAD~1                   │
# │ Revert commit        │ git revert <hash>                  │
# │ Recover lost work    │ git reflog                         │
# └─────────────────────┴────────────────────────────────────┘
echo "Bookmark this cheat sheet!" """},
],
"todos": [
    "Set up at least 5 git aliases (e.g., lg, st, undo, wip, amend) and use them for a day",
    "Deliberately commit to the wrong branch, then cherry-pick it to the correct branch and reset the wrong one",
    "Practice git commit --amend to add a forgotten file to your last commit without making a new commit",
    "Use git revert to safely undo a pushed commit and verify the history still contains the original commit",
    "Review the command reference table and write down 3 commands you haven't used yet — then try each one",
],
},

]


# ─── Generate ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    html = make_html(SECTIONS)
    (BASE / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote {BASE / 'index.html'}")

    nb = make_nb(SECTIONS)
    nb_path = BASE / "study_guide.ipynb"
    nb_path.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print(f"Wrote {nb_path} ({len(nb['cells'])} cells)")
