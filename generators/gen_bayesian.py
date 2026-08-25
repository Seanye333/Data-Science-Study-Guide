#!/usr/bin/env python3
"""Generate Probability & Bayesian Thinking study guide — notebook + HTML."""

import json, pathlib
from html import escape as esc

BASE = pathlib.Path(__file__).resolve().parent.parent / "modules" / "17_bayesian"
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
            blks += (
                f'<div class="code-block">'
                f'<div class="ch"><span>{esc(ex.get("label","Example"))}</span>'
                f'<button onclick="cp(\'{cid}\')">Copy</button></div>'
                f'<pre><code id="{cid}" class="language-python">{esc(ex["code"])}</code></pre>'
                f'</div>'
            )
        rw = s.get("rw", {})
        rw_html = ""
        if rw:
            rw_html = (
                f'<div class="rw">'
                f'<div class="rh">&#x1F4BC; Real-World: {esc(rw["title"])}</div>'
                f'<div class="rd">{esc(rw["scenario"])}</div>'
                f'<pre><code class="language-python">{esc(rw["code"])}</code></pre>'
                f'</div>'
            )
        practices = list(s.get("practices") or [])
        if s.get("practice"):
            practices = [s["practice"]] + practices
        practice_html = ""
        for k, practice in enumerate(practices):
            pid = f"p{i}_{k}"
            check_html = (
                f'<template class="ho-check">{esc(practice["check"])}</template>'
                if practice.get("check") else ""
            )
            practice_html += (
                f'<div class="practice">'
                f'<div class="ph">&#x1F3CB;&#xFE0F; Practice: {esc(practice["title"])}</div>'
                f'<div class="pd">{esc(practice["desc"])}</div>'
                f'<div class="code-block"><div class="ch"><span>Starter Code</span>'
                f'<button onclick="cp(\'{pid}\')">Copy</button></div>'
                f'<pre><code id="{pid}" class="language-python">{esc(practice["starter"])}</code></pre></div>'
                f'{check_html}'
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
<title>Probability &amp; Bayesian Thinking Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<link rel="stylesheet" href="../../styles/glass.css">
<style>:root{{--acc:#a78bfa}}</style>
</head><body class="page-module">
<aside class="sidebar">
  <div class="sbh"><h2>🎲 Bayesian Thinking</h2><p>Study Guide &bull; {n} topics</p>
    <input id="q" placeholder="Search..." oninput="filt(this.value)">
  </div>
  <ul class="nav-list" id="nl">{nav}</ul>
</aside>
<main class="main">
  <h1 class="pt">🎲 Probability &amp; Bayesian Thinking</h1>
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

    cells.append(md("# Probability & Bayesian Thinking Study Guide\n\nFrom probability foundations to Bayesian inference — learn to think probabilistically and make better decisions under uncertainty."))
    for i, s in enumerate(sections, 1):
        cells.append(md(f"## {i}. {s['title']}\n\n{s.get('desc','')}"))
        for ex in s.get("examples", []):
            if ex.get("label"): cells.append(md(f"**{ex['label']}**"))
            cells.append(code(ex["code"]))
        rw = s.get("rw")
        if rw:
            cells.append(md(f"### Real-World: {rw['title']}\n\n> {rw['scenario']}"))
            cells.append(code(rw["code"]))
        practices = list(s.get("practices") or [])
        if s.get("practice"):
            practices = [s["practice"]] + practices
        for practice in practices:
            cells.append(md(f"### Practice: {practice['title']}\n\n{practice['desc']}"))
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
"title": "1. Probability Foundations Refresher",
"practices": [
{
"title": 'Joint Probability',
"desc": 'P(A and B) from P(A) and P(B|A).',
"starter": 'def joint_prob(pa, pb_given_a):\n    # TODO: multiply the two probabilities\n    return 0.0\n\nprint(joint_prob(0.5, 0.4))',
"check": 'assert joint_prob(0.5, 0.4) == 0.2\nprint("All checks passed \\u2713")',
},
],
"desc": "A quick refresher on core probability concepts: sample spaces, events, axioms, and the rules that everything else builds on.",
"examples": [
{"label": "Basic probability rules", "code":
"""import numpy as np

# Probability axioms:
# P(A) >= 0 for any event A
# P(sample space) = 1
# P(A or B) = P(A) + P(B) - P(A and B)

# Example: Rolling a fair die
n_sides = 6
P_even = 3 / n_sides       # {2, 4, 6}
P_gt4  = 2 / n_sides       # {5, 6}
P_even_and_gt4 = 1 / n_sides  # {6}

# Union rule
P_even_or_gt4 = P_even + P_gt4 - P_even_and_gt4
print(f"P(even) = {P_even:.4f}")
print(f"P(>4)   = {P_gt4:.4f}")
print(f"P(even OR >4) = {P_even_or_gt4:.4f}")
print(f"P(even AND >4) = {P_even_and_gt4:.4f}")

# Complement
P_not_even = 1 - P_even
print(f"P(odd)  = {P_not_even:.4f}")

# Simulation verification
rolls = np.random.randint(1, 7, 100000)
print(f"\\nSimulated P(even) = {np.mean(rolls % 2 == 0):.4f}")
print(f"Simulated P(even OR >4) = {np.mean((rolls % 2 == 0) | (rolls > 4)):.4f}")"""},
{"label": "Conditional probability", "code":
"""import numpy as np

# P(A|B) = P(A and B) / P(B)
# "Probability of A given that B has occurred"

# Example: Medical test
# 1% of population has disease
# Test: 95% sensitivity (true positive), 90% specificity (true negative)
P_disease = 0.01
sensitivity = 0.95    # P(positive | disease)
specificity = 0.90    # P(negative | no disease)

# What's P(disease | positive test)?
P_positive_given_disease = sensitivity
P_positive_given_no_disease = 1 - specificity  # false positive rate

# Total probability of positive test
P_positive = (P_positive_given_disease * P_disease +
              P_positive_given_no_disease * (1 - P_disease))

# Bayes' theorem!
P_disease_given_positive = (P_positive_given_disease * P_disease) / P_positive

print(f"P(disease)            = {P_disease:.4f}")
print(f"P(positive test)      = {P_positive:.4f}")
print(f"P(disease | positive) = {P_disease_given_positive:.4f}")
print(f"\\nSurprising! Even with a positive test, only {P_disease_given_positive:.1%}")
print("chance of actually having the disease (when prevalence is low).")"""},
{"label": "Independence and conditional independence", "code":
"""import numpy as np

# Two events are independent if: P(A and B) = P(A) * P(B)
# Equivalently: P(A|B) = P(A)

# Simulate: coin flips are independent
np.random.seed(42)
n = 100000
flip1 = np.random.choice(["H", "T"], n)
flip2 = np.random.choice(["H", "T"], n)

P_H1 = np.mean(flip1 == "H")
P_H2 = np.mean(flip2 == "H")
P_both_H = np.mean((flip1 == "H") & (flip2 == "H"))

print(f"P(H1) = {P_H1:.4f}")
print(f"P(H2) = {P_H2:.4f}")
print(f"P(H1)*P(H2) = {P_H1 * P_H2:.4f}")
print(f"P(H1 and H2) = {P_both_H:.4f}")
print(f"Independent? {abs(P_H1 * P_H2 - P_both_H) < 0.01}")

# NOT independent: drawing cards without replacement
# P(2nd ace | 1st ace) != P(2nd ace)
P_ace1 = 4/52
P_ace2_given_ace1 = 3/51
P_ace2 = 4/52  # unconditional
print(f"\\nCards: P(ace2|ace1) = {P_ace2_given_ace1:.4f} != P(ace2) = {P_ace2:.4f}")
print("Drawing without replacement → NOT independent")"""},
],
"rw": {
    "title": "Probability in Spam Filtering",
    "scenario": "A spam filter uses word probabilities to classify emails. Understanding conditional probability is key to how Naive Bayes classifiers work.",
    "code":
"""import numpy as np

# Simplified spam classifier using probability
# Training data statistics:
P_spam = 0.40       # 40% of emails are spam

# Word frequencies (simplified)
# P(word | spam) and P(word | ham)
word_probs = {
    "free":    {"spam": 0.60, "ham": 0.05},
    "meeting": {"spam": 0.02, "ham": 0.30},
    "winner":  {"spam": 0.45, "ham": 0.01},
    "project": {"spam": 0.01, "ham": 0.25},
    "click":   {"spam": 0.50, "ham": 0.03},
}

def classify_email(words, word_probs, P_spam):
    \"\"\"Naive Bayes classifier (assumes word independence).\"\"\"
    log_spam = np.log(P_spam)
    log_ham = np.log(1 - P_spam)

    for word in words:
        if word in word_probs:
            log_spam += np.log(word_probs[word]["spam"])
            log_ham += np.log(word_probs[word]["ham"])

    # Convert back from log space
    P_spam_given_words = np.exp(log_spam) / (np.exp(log_spam) + np.exp(log_ham))
    return P_spam_given_words

# Test emails
emails = [
    (["free", "click", "winner"], "Obvious spam"),
    (["meeting", "project"], "Likely ham"),
    (["free", "meeting"], "Ambiguous"),
]

for words, desc in emails:
    prob = classify_email(words, word_probs, P_spam)
    label = "SPAM" if prob > 0.5 else "HAM"
    print(f"  {desc:15s} words={words} → P(spam)={prob:.4f} [{label}]")"""
},
"todos": [
    "Compute P(A union B) and P(A intersection B) for two events using the addition rule — verify with simulation",
    "Calculate P(disease | positive test) for disease prevalences of 0.1%, 1%, 5%, and 10%",
    "Verify independence of two coin flips by checking P(H1 and H2) == P(H1) * P(H2) via simulation",
    "Implement a simple Naive Bayes classifier from scratch for 3 email categories",
    "Show that P(ace2 | ace1) differs from P(ace2) in a deck without replacement — calculate both",
],
},

{
"title": "2. Bayes' Theorem — The Foundation",
"practices": [
{
"title": 'Posterior (Binary Test)',
"desc": 'Compute P(disease | positive) from prior, sensitivity and specificity.',
"starter": 'def posterior_binary(prior, sens, spec):\n    fp = 1 - spec\n    # TODO: (sens*prior) / (sens*prior + fp*(1-prior))\n    return 0.0\n\nprint(round(posterior_binary(0.01, 0.99, 0.95), 4))',
"check": 'assert abs(posterior_binary(0.01, 0.99, 0.95) - 0.99*0.01/(0.99*0.01+0.05*0.99)) < 1e-9\nprint("All checks passed \\u2713")',
},
{
"title": 'To Odds',
"desc": 'Convert a probability to odds p/(1-p).',
"starter": 'def to_odds(p):\n    # TODO: p / (1 - p)\n    return 0.0\n\nprint(to_odds(0.5))',
"check": 'assert to_odds(0.5) == 1.0\nassert abs(to_odds(0.8) - 4.0) < 1e-9\nprint("All checks passed \\u2713")',
},
{
"title": 'Bayes Factor',
"desc": 'Ratio of likelihoods P(E|H) / P(E|not H).',
"starter": 'def bayes_factor(p_e_h, p_e_nh):\n    # TODO: ratio of the two likelihoods\n    return 0.0\n\nprint(bayes_factor(0.8, 0.2))',
"check": 'assert bayes_factor(0.8, 0.2) == 4.0\nprint("All checks passed \\u2713")',
},
{
"title": 'Update Odds',
"desc": 'Posterior odds = prior odds x Bayes factor.',
"starter": 'def update_odds(prior_odds, bf):\n    # TODO: multiply the prior odds by the Bayes factor\n    return 0.0\n\nprint(update_odds(1.0, 4.0))',
"check": 'assert update_odds(1.0, 4.0) == 4.0\nprint("All checks passed \\u2713")',
},
],
"desc": "Bayes' theorem is the mathematical framework for updating beliefs with evidence. It's the bridge from 'what we knew before' (prior) to 'what we know now' (posterior).",
"examples": [
{"label": "Bayes' theorem step by step", "code":
"""import numpy as np

# Bayes' Theorem:
# P(H|D) = P(D|H) * P(H) / P(D)
#
# P(H|D)  = posterior  — updated belief after seeing data
# P(H)    = prior      — belief before seeing data
# P(D|H)  = likelihood — probability of data given hypothesis
# P(D)    = evidence   — total probability of data

# Example: Cookie problem
# Bowl 1: 30 vanilla, 10 chocolate cookies
# Bowl 2: 20 vanilla, 20 chocolate cookies
# You randomly pick a bowl (50/50), then pick a vanilla cookie.
# What's the probability it came from Bowl 1?

P_bowl1 = 0.5          # prior: equal chance of each bowl
P_bowl2 = 0.5
P_vanilla_given_bowl1 = 30/40    # likelihood
P_vanilla_given_bowl2 = 20/40

# Total probability of vanilla (evidence)
P_vanilla = (P_vanilla_given_bowl1 * P_bowl1 +
             P_vanilla_given_bowl2 * P_bowl2)

# Posterior
P_bowl1_given_vanilla = (P_vanilla_given_bowl1 * P_bowl1) / P_vanilla

print(f"Prior P(Bowl1)             = {P_bowl1:.4f}")
print(f"Likelihood P(V|Bowl1)      = {P_vanilla_given_bowl1:.4f}")
print(f"Evidence P(V)              = {P_vanilla:.4f}")
print(f"Posterior P(Bowl1|V)       = {P_bowl1_given_vanilla:.4f}")
print(f"\\nAfter seeing vanilla, Bowl 1 is {P_bowl1_given_vanilla:.1%} likely (up from 50%)")"""},
{"label": "Sequential Bayesian updating", "code":
"""import numpy as np

# Bayesian updating: each new observation updates the posterior
# The posterior becomes the new prior!

# Is this coin fair? Start with no strong belief.
# Prior: P(fair) = 0.5
P_fair = 0.5

# Likelihoods
P_heads_if_fair = 0.5
P_heads_if_biased = 0.8  # biased coin: 80% heads

observations = "HHHTHHHHHH"  # 9 heads, 1 tail

print(f"{'Obs':>4} {'Prior(fair)':>12} {'Posterior(fair)':>15}")
print(f"{'':>4} {P_fair:>12.4f} {'':>15}")

for obs in observations:
    if obs == "H":
        likelihood_fair = P_heads_if_fair
        likelihood_biased = P_heads_if_biased
    else:
        likelihood_fair = 1 - P_heads_if_fair
        likelihood_biased = 1 - P_heads_if_biased

    # Evidence
    P_obs = likelihood_fair * P_fair + likelihood_biased * (1 - P_fair)

    # Update
    P_fair = (likelihood_fair * P_fair) / P_obs
    print(f"   {obs} {P_fair:>28.4f}")

print(f"\\nAfter {len(observations)} flips: P(fair) = {P_fair:.4f}")
print(f"P(biased) = {1 - P_fair:.4f}")"""},
{"label": "Bayes' theorem with multiple hypotheses", "code":
"""import numpy as np

# You have 3 possible models. Which is most likely given the data?
# Model A: coin is fair (P(H)=0.5)
# Model B: coin favors heads (P(H)=0.7)
# Model C: coin favors tails (P(H)=0.3)

models = {
    "Fair (0.5)": {"prior": 1/3, "p_heads": 0.5},
    "Heads (0.7)": {"prior": 1/3, "p_heads": 0.7},
    "Tails (0.3)": {"prior": 1/3, "p_heads": 0.3},
}

data = "HHTHHHTHHH"  # 8 heads, 2 tails

for obs in data:
    evidence = 0
    for name, m in models.items():
        p_obs = m["p_heads"] if obs == "H" else (1 - m["p_heads"])
        evidence += p_obs * m["prior"]

    for name, m in models.items():
        p_obs = m["p_heads"] if obs == "H" else (1 - m["p_heads"])
        m["prior"] = (p_obs * m["prior"]) / evidence

print("After observing:", data)
print(f"{'Model':<15} {'Posterior':>10}")
for name, m in models.items():
    bar = "#" * int(m["prior"] * 50)
    print(f"{name:<15} {m['prior']:>10.4f} {bar}")"""},
],
"rw": {
    "title": "Bayesian A/B Testing",
    "scenario": "An e-commerce company wants to know if a new checkout page (B) converts better than the original (A). Instead of frequentist p-values, they use Bayesian analysis to get a direct probability.",
    "code":
"""import numpy as np

def bayesian_ab_test(successes_a, trials_a, successes_b, trials_b, n_simulations=100000):
    \"\"\"Bayesian A/B test using Beta-Binomial model.\"\"\"
    # Beta(1,1) = uniform prior (no prior knowledge)
    # Posterior: Beta(1 + successes, 1 + failures)

    # Sample from posterior distributions
    samples_a = np.random.beta(1 + successes_a, 1 + trials_a - successes_a, n_simulations)
    samples_b = np.random.beta(1 + successes_b, 1 + trials_b - successes_b, n_simulations)

    # Direct probability that B > A
    prob_b_better = np.mean(samples_b > samples_a)

    # Expected lift
    lift = (samples_b - samples_a) / samples_a
    mean_lift = np.mean(lift)

    # Credible interval for the difference
    diff = samples_b - samples_a
    ci_low, ci_high = np.percentile(diff, [2.5, 97.5])

    return {
        "prob_b_better": prob_b_better,
        "mean_lift": mean_lift,
        "ci_95": (ci_low, ci_high),
        "mean_a": np.mean(samples_a),
        "mean_b": np.mean(samples_b),
    }

# Results: A had 120/1000 conversions, B had 145/1000
result = bayesian_ab_test(120, 1000, 145, 1000)

print("Bayesian A/B Test Results")
print("=" * 40)
print(f"Conversion A: {result['mean_a']:.4f}")
print(f"Conversion B: {result['mean_b']:.4f}")
print(f"P(B > A):     {result['prob_b_better']:.4f}")
print(f"Expected lift: {result['mean_lift']:.1%}")
print(f"95% CI for diff: ({result['ci_95'][0]:.4f}, {result['ci_95'][1]:.4f})")

# Decision
if result["prob_b_better"] > 0.95:
    print("\\nDecision: SHIP B (>95% probability it's better)")
elif result["prob_b_better"] < 0.05:
    print("\\nDecision: KEEP A (B is worse)")
else:
    print("\\nDecision: CONTINUE TESTING (inconclusive)")"""
},
"practice": {
    "title": "Bayesian Coin Classifier",
    "desc": "Write a function that takes a sequence of coin flips and computes the posterior probability distribution over possible bias values (0.0 to 1.0).",
    "starter":
"""import numpy as np

def bayesian_coin_analysis(flips, n_hypotheses=101):
    \"\"\"Compute posterior over possible coin biases.

    Args:
        flips: string of 'H' and 'T'
        n_hypotheses: number of bias values to test (0.0 to 1.0)

    Returns:
        biases: array of bias values
        posteriors: normalized posterior probabilities
    \"\"\"
    biases = np.linspace(0, 1, n_hypotheses)
    # Start with uniform prior
    priors = np.ones(n_hypotheses) / n_hypotheses

    # TODO: for each flip, update the prior → posterior
    # TODO: normalize posteriors after each update
    # Hint: P(H|bias=b) = b, P(T|bias=b) = 1-b

    return biases, priors

# Test
biases, posteriors = bayesian_coin_analysis("HHHHHTHH")

# Find MAP estimate
map_bias = biases[np.argmax(posteriors)]
print(f"MAP estimate of bias: {map_bias:.2f}")
print(f"Expected bias: {np.sum(biases * posteriors):.4f}")"""
},
"todos": [
    "Manually compute P(disease|positive test) for 1%, 5%, and 10% disease prevalence",
    "Update a prior belief sequentially with 5 coin flips — plot posterior after each",
    "Implement Bayes' theorem for 3 hypotheses and verify posteriors sum to 1",
    "Calculate how many observations are needed to overcome a strong prior",
    "Compare posterior means from uniform vs informative priors on the same data",
],
},

{
"title": "3. Prior Distributions — Encoding Beliefs",
"practices": [
{
"title": 'Beta Mean',
"desc": 'Mean of a Beta(a, b) prior.',
"starter": 'def beta_mean(a, b):\n    # TODO: a / (a + b)\n    return 0.0\n\nprint(beta_mean(2, 2))',
"check": 'assert beta_mean(2, 2) == 0.5\nassert beta_mean(8, 4) == 8/12\nprint("All checks passed \\u2713")',
},
{
"title": 'Beta Variance',
"desc": 'Variance of a Beta(a, b).',
"starter": 'def beta_var(a, b):\n    # TODO: a*b / ((a+b)**2 * (a+b+1))\n    return 0.0\n\nprint(round(beta_var(2, 2), 4))',
"check": 'from scipy import stats\nassert abs(beta_var(2, 2) - stats.beta(2, 2).var()) < 1e-9\nprint("All checks passed \\u2713")',
},
{
"title": 'Normal CDF',
"desc": 'P(X <= x) for a Normal(mu, sigma).',
"starter": 'import numpy as np\nfrom scipy import stats\n\ndef normal_cdf(x, mu, sigma):\n    # TODO: stats.norm.cdf(x, mu, sigma)\n    return 0.0\n\nprint(round(normal_cdf(0, 0, 1), 4))',
"check": 'from scipy import stats\nassert abs(normal_cdf(0, 0, 1) - 0.5) < 1e-9\nprint("All checks passed \\u2713")',
},
{
"title": 'Exponential Mean',
"desc": 'Mean of an Exponential(rate) prior.',
"starter": 'def exp_mean(rate):\n    # TODO: 1 / rate\n    return 0.0\n\nprint(exp_mean(2))',
"check": 'assert exp_mean(2) == 0.5\nprint("All checks passed \\u2713")',
},
{
"title": 'Uniform Density',
"desc": 'Density height of a Uniform(a, b).',
"starter": 'def uniform_pdf_height(a, b):\n    # TODO: 1 / (b - a)\n    return 0.0\n\nprint(uniform_pdf_height(0, 4))',
"check": 'assert uniform_pdf_height(0, 4) == 0.25\nprint("All checks passed \\u2713")',
},
],
"desc": "The prior distribution represents what you believe before seeing data. Choosing the right prior is part art, part science — it encodes domain knowledge and assumptions.",
"examples": [
{"label": "Common prior distributions", "code":
"""import numpy as np
from scipy import stats

# Beta distribution — for probabilities (0 to 1)
# Beta(1,1) = uniform (no preference)
# Beta(10,10) = believe ~0.5, moderately confident
# Beta(2,8) = believe ~0.2
x = np.linspace(0, 1, 100)

priors = {
    "Uniform Beta(1,1)": stats.beta(1, 1),
    "Informative Beta(10,10)": stats.beta(10, 10),
    "Skewed Beta(2,8)": stats.beta(2, 8),
}

for name, dist in priors.items():
    mean = dist.mean()
    std = dist.std()
    print(f"{name:30s} mean={mean:.3f}, std={std:.3f}")

# Normal distribution — for continuous parameters
# N(0, 1) = weakly informative
# N(100, 10) = centered at 100, fairly certain
priors_normal = {
    "Weak N(0,10)": stats.norm(0, 10),
    "Strong N(100,5)": stats.norm(100, 5),
}

for name, dist in priors_normal.items():
    ci = dist.interval(0.95)
    print(f"{name:30s} 95% CI: ({ci[0]:.1f}, {ci[1]:.1f})")"""},
{"label": "How priors affect posteriors", "code":
"""import numpy as np
from scipy import stats

# Same data, different priors → different posteriors
# Data: 7 heads out of 10 flips

successes, trials = 7, 10

# Prior 1: Uniform (no prior knowledge)
# Beta(1,1) + 7H,3T → Beta(8, 4)
post1 = stats.beta(1 + successes, 1 + trials - successes)

# Prior 2: Strong belief coin is fair
# Beta(50,50) + 7H,3T → Beta(57, 53)
post2 = stats.beta(50 + successes, 50 + trials - successes)

# Prior 3: Belief coin is biased toward heads
# Beta(8,2) + 7H,3T → Beta(15, 5)
post3 = stats.beta(8 + successes, 2 + trials - successes)

print("Data: 7 heads in 10 flips")
print(f"{'Prior':<30} {'Post Mean':>10} {'Post 95% CI':>25}")
print("-" * 65)
for name, post in [
    ("Uniform Beta(1,1)", post1),
    ("Fair-biased Beta(50,50)", post2),
    ("Heads-biased Beta(8,2)", post3),
]:
    ci = post.interval(0.95)
    print(f"{name:<30} {post.mean():>10.4f} ({ci[0]:.4f}, {ci[1]:.4f})")

print("\\nWith enough data, the prior matters less (posteriors converge).")"""},
{"label": "Conjugate priors — analytical solutions", "code":
"""import numpy as np
from scipy import stats

# Conjugate priors give closed-form posteriors:
# Likelihood     | Conjugate Prior | Posterior
# Binomial       | Beta            | Beta
# Poisson        | Gamma           | Gamma
# Normal (known var) | Normal      | Normal
# Normal (known mean)| Inv-Gamma   | Inv-Gamma

# Example: Estimating website conversion rate
# Prior: Beta(2, 8) — believe ~20% conversion rate
# Data: 15 conversions out of 80 visitors

alpha_prior, beta_prior = 2, 8
successes, failures = 15, 65

# Posterior is Beta(alpha_prior + successes, beta_prior + failures)
alpha_post = alpha_prior + successes
beta_post = beta_prior + failures
posterior = stats.beta(alpha_post, beta_post)

print(f"Prior:     Beta({alpha_prior}, {beta_prior})")
print(f"Data:      {successes} successes / {successes + failures} trials")
print(f"Posterior: Beta({alpha_post}, {beta_post})")
print(f"\\nPrior mean:     {stats.beta(alpha_prior, beta_prior).mean():.4f}")
print(f"MLE (data only): {successes / (successes + failures):.4f}")
print(f"Posterior mean:  {posterior.mean():.4f}")
print(f"Posterior mode:  {(alpha_post - 1) / (alpha_post + beta_post - 2):.4f}")
print(f"95% Credible:    ({posterior.ppf(0.025):.4f}, {posterior.ppf(0.975):.4f})")"""},
],
"rw": {
    "title": "Choosing Priors for Click-Through Rate",
    "scenario": "A marketing team launches a new ad campaign. They use historical CTR data from previous campaigns to set an informative prior, then update with new data.",
    "code":
"""import numpy as np
from scipy import stats

# Historical CTR data from 10 past campaigns
historical_ctrs = [0.02, 0.03, 0.025, 0.018, 0.035, 0.022, 0.028, 0.032, 0.015, 0.04]

# Fit a Beta prior from historical data (method of moments)
mean_ctr = np.mean(historical_ctrs)
var_ctr = np.var(historical_ctrs)

# Beta method of moments
alpha_0 = mean_ctr * (mean_ctr * (1 - mean_ctr) / var_ctr - 1)
beta_0 = (1 - mean_ctr) * (mean_ctr * (1 - mean_ctr) / var_ctr - 1)

print(f"Historical CTR: mean={mean_ctr:.4f}, var={var_ctr:.6f}")
print(f"Fitted prior: Beta({alpha_0:.1f}, {beta_0:.1f})")

# New campaign data comes in daily
daily_data = [(500, 12), (600, 18), (550, 15), (700, 25), (650, 20)]

alpha, beta = alpha_0, beta_0
print(f"\\n{'Day':>4} {'Shown':>6} {'Clicks':>7} {'Post Mean':>10} {'95% CI':>25}")
for day, (shown, clicks) in enumerate(daily_data, 1):
    alpha += clicks
    beta += shown - clicks
    post = stats.beta(alpha, beta)
    ci = post.interval(0.95)
    print(f"{day:>4} {shown:>6} {clicks:>7} {post.mean():>10.4f} ({ci[0]:.4f}, {ci[1]:.4f})")

print(f"\\nFinal estimate: CTR = {stats.beta(alpha, beta).mean():.4f}")
print(f"Compare to raw: {sum(c for _,c in daily_data)/sum(s for s,_ in daily_data):.4f}")"""
},
"todos": [
    "Create Beta(1,1), Beta(5,5), and Beta(2,8) distributions — print their means and 95% credible intervals",
    "Show that with 100 observations, a strong prior Beta(50,50) and a weak prior Beta(1,1) converge",
    "Update a Beta prior sequentially with daily conversion data — print the posterior mean each day",
    "Use the Beta conjugate update rule to compute the posterior after 15 successes in 80 trials",
    "Fit a Beta prior from historical data using method of moments — verify the mean matches the data mean",
],
},

{
"title": "4. Bayesian A/B Testing",
"practices": [
{
"title": 'Beta Posterior',
"desc": 'Update a Beta prior with successes out of trials.',
"starter": 'def beta_posterior(prior_a, prior_b, successes, trials):\n    # TODO: (prior_a + successes, prior_b + trials - successes)\n    return (prior_a, prior_b)\n\nprint(beta_posterior(1, 1, 7, 10))',
"check": 'assert beta_posterior(1, 1, 7, 10) == (8, 4)\nprint("All checks passed \\u2713")',
},
{
"title": 'Posterior Mean (A/B)',
"desc": 'Posterior mean conversion rate after observing data.',
"starter": 'def beta_posterior(prior_a, prior_b, successes, trials):\n    return (prior_a + successes, prior_b + trials - successes)\n\ndef posterior_mean_ab(prior_a, prior_b, s, n):\n    a, b = beta_posterior(prior_a, prior_b, s, n)\n    # TODO: a / (a + b)\n    return 0.0\n\nprint(round(posterior_mean_ab(1, 1, 7, 10), 4))',
"check": 'assert posterior_mean_ab(1, 1, 7, 10) == 8/12\nprint("All checks passed \\u2713")',
},
{
"title": 'P(B beats A)',
"desc": 'Monte-Carlo probability that variant B beats A.',
"starter": 'import numpy as np\n\ndef prob_b_better(a_s, a_n, b_s, b_n, seed=0, draws=20000):\n    rng = np.random.default_rng(seed)\n    a = rng.beta(1 + a_s, 1 + a_n - a_s, draws)\n    b = rng.beta(1 + b_s, 1 + b_n - b_s, draws)\n    # TODO: fraction of draws where b > a\n    return 0.0\n\nprint(round(prob_b_better(50, 100, 70, 100), 3))',
"check": 'assert prob_b_better(50, 100, 70, 100) > 0.9, "B is clearly better here"\nassert prob_b_better(50, 100, 50, 100) < 0.6, "a tie lands near 0.5"\nprint("All checks passed \\u2713")',
},
{
"title": 'Credible Interval',
"desc": 'Central credible interval of a Beta posterior.',
"starter": 'import numpy as np\nfrom scipy import stats\n\ndef credible_interval(a, b, conf=0.95):\n    d = stats.beta(a, b)\n    # TODO: return (float(lo), float(hi)) from d.interval(conf)\n    return (0.0, 1.0)\n\nprint([round(x, 3) for x in credible_interval(8, 4)])',
"check": 'lo, hi = credible_interval(8, 4)\nassert lo < 8/12 < hi, "the interval brackets the posterior mean"\nprint("All checks passed \\u2713")',
},
{
"title": 'Relative Lift',
"desc": 'Relative improvement (pb - pa) / pa.',
"starter": 'def lift(pa, pb):\n    # TODO: (pb - pa) / pa\n    return 0.0\n\nprint(round(lift(0.5, 0.6), 4))',
"check": 'assert abs(lift(0.5, 0.6) - 0.2) < 1e-9\nprint("All checks passed \\u2713")',
},
],
"desc": "Bayesian A/B testing gives you what you actually want: 'What's the probability that B is better than A?' — not a confusing p-value. It's intuitive, flexible, and allows early stopping.",
"examples": [
{"label": "Full Bayesian A/B test", "code":
"""import numpy as np
from scipy import stats

def bayesian_ab(control_success, control_total,
                treatment_success, treatment_total,
                prior_alpha=1, prior_beta=1, n_samples=200000):
    \"\"\"Complete Bayesian A/B test with actionable metrics.\"\"\"

    # Posterior distributions
    post_a = stats.beta(prior_alpha + control_success,
                        prior_beta + control_total - control_success)
    post_b = stats.beta(prior_alpha + treatment_success,
                        prior_beta + treatment_total - treatment_success)

    # Monte Carlo sampling
    samples_a = post_a.rvs(n_samples)
    samples_b = post_b.rvs(n_samples)

    # Key metrics
    prob_b_wins = np.mean(samples_b > samples_a)
    relative_lift = (samples_b - samples_a) / samples_a
    expected_loss_a = np.mean(np.maximum(samples_b - samples_a, 0))  # loss if we pick A
    expected_loss_b = np.mean(np.maximum(samples_a - samples_b, 0))  # loss if we pick B

    return {
        "P(B>A)": prob_b_wins,
        "E[lift]": np.mean(relative_lift),
        "lift_95ci": np.percentile(relative_lift, [2.5, 97.5]),
        "expected_loss_A": expected_loss_a,
        "expected_loss_B": expected_loss_b,
        "rate_A": post_a.mean(),
        "rate_B": post_b.mean(),
    }

# Test: Control 10% CR, Treatment 12% CR
result = bayesian_ab(100, 1000, 120, 1000)

print("Bayesian A/B Test")
print("=" * 45)
print(f"Control rate:   {result['rate_A']:.4f}")
print(f"Treatment rate: {result['rate_B']:.4f}")
print(f"P(B > A):       {result['P(B>A)']:.4f}")
print(f"Expected lift:  {result['E[lift]']:.1%}")
print(f"Lift 95% CI:    ({result['lift_95ci'][0]:.1%}, {result['lift_95ci'][1]:.1%})")
print(f"Expected loss if choose A: {result['expected_loss_A']:.5f}")
print(f"Expected loss if choose B: {result['expected_loss_B']:.5f}")"""},
{"label": "Multi-variant test (A/B/C/D)", "code":
"""import numpy as np

def bayesian_multivariate(variants, n_samples=200000):
    \"\"\"Test multiple variants simultaneously.\"\"\"
    # Sample from each variant's posterior
    samples = {}
    for name, (successes, trials) in variants.items():
        samples[name] = np.random.beta(1 + successes, 1 + trials - successes, n_samples)

    # Probability each variant is the best
    all_samples = np.column_stack(list(samples.values()))
    best_idx = np.argmax(all_samples, axis=1)
    names = list(variants.keys())

    results = {}
    for i, name in enumerate(names):
        results[name] = {
            "mean_rate": np.mean(samples[name]),
            "prob_best": np.mean(best_idx == i),
        }

    return results

variants = {
    "Control":    (100, 1000),   # 10.0%
    "Variant B":  (115, 1000),   # 11.5%
    "Variant C":  (125, 1000),   # 12.5%
    "Variant D":  (108, 1000),   # 10.8%
}

results = bayesian_multivariate(variants)
print(f"{'Variant':<15} {'Conv Rate':>10} {'P(Best)':>10}")
print("-" * 35)
for name, r in sorted(results.items(), key=lambda x: -x[1]["prob_best"]):
    print(f"{name:<15} {r['mean_rate']:>10.4f} {r['prob_best']:>10.4f}")"""},
{"label": "When to stop: expected loss threshold", "code":
"""import numpy as np

def should_stop_test(successes_a, trials_a, successes_b, trials_b,
                     loss_threshold=0.001, n_samples=100000):
    \"\"\"Decide whether to stop A/B test based on expected loss.\"\"\"
    samples_a = np.random.beta(1 + successes_a, 1 + trials_a - successes_a, n_samples)
    samples_b = np.random.beta(1 + successes_b, 1 + trials_b - successes_b, n_samples)

    # Expected loss of choosing each variant
    loss_a = np.mean(np.maximum(samples_b - samples_a, 0))
    loss_b = np.mean(np.maximum(samples_a - samples_b, 0))

    min_loss = min(loss_a, loss_b)
    winner = "A" if loss_a < loss_b else "B"

    return {
        "stop": min_loss < loss_threshold,
        "winner": winner,
        "loss_a": loss_a,
        "loss_b": loss_b,
    }

# Simulate daily results
np.random.seed(42)
sa, ta, sb, tb = 0, 0, 0, 0
true_rate_a, true_rate_b = 0.10, 0.12  # B is actually better

for day in range(1, 31):
    daily_visitors = 100
    sa += np.random.binomial(daily_visitors, true_rate_a)
    ta += daily_visitors
    sb += np.random.binomial(daily_visitors, true_rate_b)
    tb += daily_visitors

    result = should_stop_test(sa, ta, sb, tb)
    if day % 5 == 0 or result["stop"]:
        print(f"Day {day:2d}: A={sa}/{ta} B={sb}/{tb} | "
              f"loss_A={result['loss_a']:.5f} loss_B={result['loss_b']:.5f} | "
              f"{'STOP → '+result['winner'] if result['stop'] else 'continue'}")
    if result["stop"]:
        break"""},
],
"rw": {
    "title": "Production A/B Testing Framework",
    "scenario": "A product team runs A/B tests on website features. They need a dashboard-ready analysis that reports probability of improvement, expected revenue impact, and a clear recommendation.",
    "code":
"""import numpy as np

class ABTestAnalyzer:
    def __init__(self, revenue_per_conversion=50):
        self.rev = revenue_per_conversion

    def analyze(self, data, n_samples=200000):
        results = []
        samples = {}

        for name, (s, n) in data.items():
            post = np.random.beta(1 + s, 1 + n - s, n_samples)
            samples[name] = post
            results.append({"name": name, "rate": (s+1)/(n+2), "n": n})

        names = list(data.keys())
        control = names[0]

        print("A/B TEST REPORT")
        print("=" * 55)
        for name in names:
            s, n = data[name]
            print(f"  {name}: {s}/{n} conversions ({s/n:.2%})")

        print(f"\\n{'Variant':<12} {'vs Control':>12} {'P(Better)':>10} {'Rev Impact':>12}")
        print("-" * 50)

        for name in names[1:]:
            prob_better = np.mean(samples[name] > samples[control])
            lift = samples[name] - samples[control]
            monthly_impact = np.mean(lift) * 10000 * self.rev  # 10k monthly visitors

            print(f"{name:<12} {np.mean(lift):>+12.4f} {prob_better:>10.1%} ${monthly_impact:>11,.0f}/mo")

        return samples

data = {
    "Control":    (500, 5000),
    "New CTA":    (560, 5000),
    "New Layout": (540, 5000),
}

analyzer = ABTestAnalyzer(revenue_per_conversion=75)
analyzer.analyze(data)"""
},
"todos": [
    "Run a Bayesian A/B test where B has 120/1000 vs A's 100/1000 — compute P(B > A) and expected lift",
    "Extend the test to 4 variants (A/B/C/D) and compute the probability each variant is the best",
    "Simulate a 30-day test with a 2pp lift — track when the expected loss drops below 0.001",
    "Change the prior from Beta(1,1) to Beta(10,10) and observe how it slows down the posterior update",
    "Compute the 95% credible interval for the lift and interpret what it means for a business decision",
],
},

{
"title": "5. Monte Carlo Simulation",
"practices": [
{
"title": 'Estimate Pi',
"desc": 'Estimate pi by sampling points in the unit square.',
"starter": 'import numpy as np\n\ndef estimate_pi(n, seed=0):\n    rng = np.random.default_rng(seed)\n    x = rng.random(n); y = rng.random(n)\n    # TODO: 4 * fraction of points with x^2 + y^2 <= 1\n    return 0.0\n\nprint(round(estimate_pi(100000), 3))',
"check": 'assert abs(estimate_pi(100000) - 3.14159) < 0.05\nprint("All checks passed \\u2713")',
},
{
"title": 'MC Mean',
"desc": 'Monte-Carlo estimate of a standard-normal mean.',
"starter": 'import numpy as np\n\ndef mc_mean(n, seed=0):\n    rng = np.random.default_rng(seed)\n    # TODO: mean of n standard normal draws\n    return 0.0\n\nprint(round(mc_mean(100000), 4))',
"check": 'assert abs(mc_mean(100000)) < 0.02, "should sit near 0"\nprint("All checks passed \\u2713")',
},
{
"title": 'MC Integral',
"desc": 'Estimate the integral of x^2 over [0, 1].',
"starter": 'import numpy as np\n\ndef mc_integral(n, seed=0):\n    rng = np.random.default_rng(seed)\n    x = rng.random(n)\n    # TODO: mean of x^2 estimates the integral over [0,1]\n    return 0.0\n\nprint(round(mc_integral(100000), 4))',
"check": 'assert abs(mc_integral(100000) - 1/3) < 0.01, "the integral of x^2 on [0,1] is 1/3"\nprint("All checks passed \\u2713")',
},
{
"title": 'Coin Flip Rate',
"desc": 'Simulate the fraction of heads for a fair coin.',
"starter": 'import numpy as np\n\ndef coin_flip_prob(n, seed=0):\n    rng = np.random.default_rng(seed)\n    # TODO: fraction of rng.random(n) draws below 0.5\n    return 0.0\n\nprint(round(coin_flip_prob(100000), 4))',
"check": 'assert abs(coin_flip_prob(100000) - 0.5) < 0.02\nprint("All checks passed \\u2713")',
},
],
"desc": "When math gets hard, simulate! Monte Carlo methods use random sampling to approximate complex probabilities, integrals, and distributions.",
"examples": [
{"label": "Estimating probabilities by simulation", "code":
"""import numpy as np

np.random.seed(42)
n_simulations = 100000

# Birthday problem: P(at least 2 share a birthday) in group of n
def birthday_simulation(group_size, n_sims=100000):
    matches = 0
    for _ in range(n_sims):
        birthdays = np.random.randint(0, 365, group_size)
        if len(set(birthdays)) < group_size:  # at least one match
            matches += 1
    return matches / n_sims

for n in [10, 20, 23, 30, 50]:
    prob = birthday_simulation(n)
    print(f"Group of {n:2d}: P(shared birthday) = {prob:.4f}")

# Monty Hall problem
def monty_hall(switch, n_sims=100000):
    wins = 0
    for _ in range(n_sims):
        car = np.random.randint(3)        # car behind door 0, 1, or 2
        choice = np.random.randint(3)     # contestant picks
        # Host opens a door (not car, not choice)
        if switch:
            # Switch to the remaining unopened door
            wins += (choice != car)
        else:
            wins += (choice == car)
    return wins / n_sims

print(f"\\nMonty Hall (stay):   P(win) = {monty_hall(switch=False):.4f}")
print(f"Monty Hall (switch): P(win) = {monty_hall(switch=True):.4f}")"""},
{"label": "Monte Carlo integration", "code":
"""import numpy as np

# Estimate pi using Monte Carlo
np.random.seed(42)
n = 1000000

# Random points in unit square
x = np.random.uniform(0, 1, n)
y = np.random.uniform(0, 1, n)

# Count points inside quarter circle (x^2 + y^2 <= 1)
inside = (x**2 + y**2) <= 1
pi_estimate = 4 * np.mean(inside)
print(f"Pi estimate (n={n:,}): {pi_estimate:.6f}")
print(f"True pi:              {np.pi:.6f}")
print(f"Error:                {abs(pi_estimate - np.pi):.6f}")

# Estimate complex integral: integral of sin(x)*exp(-x) from 0 to inf
# True value = 0.5
n = 500000
x = np.random.exponential(1, n)  # sample from exp(1)
# Importance sampling: E[f(x)/g(x)] where g is the sampling distribution
estimate = np.mean(np.sin(x))  # sin(x) * exp(-x) / exp(-x) = sin(x)
print(f"\\nIntegral estimate: {estimate:.6f}")
print(f"True value:        0.500000")"""},
{"label": "Bootstrap confidence intervals", "code":
"""import numpy as np

np.random.seed(42)

# Sample data
data = np.random.exponential(50, size=100)  # skewed distribution

# Bootstrap: resample with replacement many times
n_bootstrap = 10000
boot_means = []
boot_medians = []

for _ in range(n_bootstrap):
    sample = np.random.choice(data, size=len(data), replace=True)
    boot_means.append(np.mean(sample))
    boot_medians.append(np.median(sample))

boot_means = np.array(boot_means)
boot_medians = np.array(boot_medians)

# Confidence intervals
mean_ci = np.percentile(boot_means, [2.5, 97.5])
median_ci = np.percentile(boot_medians, [2.5, 97.5])

print(f"Sample mean:   {np.mean(data):.2f}")
print(f"95% CI (mean): ({mean_ci[0]:.2f}, {mean_ci[1]:.2f})")
print(f"\\nSample median: {np.median(data):.2f}")
print(f"95% CI (median): ({median_ci[0]:.2f}, {median_ci[1]:.2f})")
print(f"\\nBootstrap std of mean:   {np.std(boot_means):.2f}")
print(f"Bootstrap std of median: {np.std(boot_medians):.2f}")"""},
],
"rw": {
    "title": "Risk Analysis with Monte Carlo",
    "scenario": "A startup estimates annual revenue by simulating uncertain variables: customer acquisition rate, churn, and average revenue per user.",
    "code":
"""import numpy as np

np.random.seed(42)
n_sims = 50000

# Uncertain inputs (distributions based on estimates)
initial_customers = 1000
monthly_new = np.random.normal(200, 50, (n_sims, 12)).clip(0)
monthly_churn_rate = np.random.beta(2, 20, (n_sims, 12))  # ~9% churn
arpu = np.random.lognormal(np.log(50), 0.3, n_sims)       # ~$50 ARPU

# Simulate 12 months
annual_revenue = np.zeros(n_sims)
for sim in range(n_sims):
    customers = initial_customers
    total_rev = 0
    for month in range(12):
        customers = customers * (1 - monthly_churn_rate[sim, month]) + monthly_new[sim, month]
        total_rev += customers * arpu[sim]
    annual_revenue[sim] = total_rev

# Results
print("Annual Revenue Forecast (Monte Carlo)")
print("=" * 45)
print(f"Mean:          ${np.mean(annual_revenue):>12,.0f}")
print(f"Median:        ${np.median(annual_revenue):>12,.0f}")
print(f"Std Dev:       ${np.std(annual_revenue):>12,.0f}")
print(f"5th pctile:    ${np.percentile(annual_revenue, 5):>12,.0f}")
print(f"95th pctile:   ${np.percentile(annual_revenue, 95):>12,.0f}")
print(f"P(rev > $1M):  {np.mean(annual_revenue > 1_000_000):>12.1%}")
print(f"P(rev > $2M):  {np.mean(annual_revenue > 2_000_000):>12.1%}")"""
},
"practice": {
    "title": "Monte Carlo Portfolio Simulator",
    "desc": "Simulate a stock portfolio's performance over 1 year. Model daily returns as normally distributed, compute the probability of different outcomes.",
    "starter":
"""import numpy as np

def simulate_portfolio(initial_value, mean_daily_return, daily_volatility,
                       n_days=252, n_simulations=10000):
    \"\"\"Simulate portfolio value over n_days trading days.\"\"\"
    # TODO: Generate random daily returns for each simulation
    # TODO: Compute cumulative portfolio value
    # TODO: Return final values for all simulations
    pass

# Parameters (typical S&P 500)
results = simulate_portfolio(
    initial_value=100000,
    mean_daily_return=0.0004,    # ~10% annual
    daily_volatility=0.012,      # ~19% annual vol
)

# TODO: Print statistics:
# - Mean final value
# - P(gain > 10%)
# - P(loss > 10%)
# - Value at Risk (5th percentile)
# - Best and worst case (1st and 99th percentile)"""
},
"todos": [
    "Simulate the birthday problem for group sizes 10 to 50 and verify the 23-person crossover at ~50%",
    "Estimate pi using Monte Carlo with 10k, 100k, and 1M samples — observe how error shrinks",
    "Compute bootstrap 95% CI for the median of a skewed distribution with n=50 samples",
    "Run a Monte Carlo revenue forecast with at least 3 uncertain inputs and compute P(revenue > target)",
    "Simulate the Monty Hall problem and confirm switching wins ~67% of the time",
],
},

{
"title": "6. Bayesian Linear Regression",
"practices": [
{
"title": 'Design Matrix',
"desc": 'Add a bias column of ones to x.',
"starter": 'import numpy as np\n\ndef design_matrix(x):\n    x = np.asarray(x, float)\n    # TODO: column-stack a ones column and x\n    return x\n\nprint(design_matrix([1, 2]).tolist())',
"check": 'assert design_matrix([1, 2]).tolist() == [[1, 1], [1, 2]]\nprint("All checks passed \\u2713")',
},
{
"title": 'Ridge Weights',
"desc": 'Solve (XtX + aI) w = Xt y for the weights.',
"starter": 'import numpy as np\n\ndef ridge_weights(X, y, alpha):\n    X = np.asarray(X, float); y = np.asarray(y, float)\n    # TODO: np.linalg.solve(X.T@X + alpha*np.eye(X.shape[1]), X.T@y)\n    return np.zeros(X.shape[1])\n\nX = np.column_stack([np.ones(3), [0, 1, 2]]); y = np.array([1.0, 3, 5])\nprint(ridge_weights(X, y, 1e-9).round(3).tolist())',
"check": 'import numpy as np\nX = np.column_stack([np.ones(3), [0, 1, 2]]); y = np.array([1.0, 3, 5])\nassert np.allclose(ridge_weights(X, y, 1e-9), [1, 2], atol=1e-4), "recovers y = 2x + 1"\nprint("All checks passed \\u2713")',
},
{
"title": 'Predict',
"desc": 'Linear prediction X @ w.',
"starter": 'import numpy as np\n\ndef predict_lin(X, w):\n    # TODO: X @ w\n    return np.zeros(len(X))\n\nprint(predict_lin([[1, 0], [1, 1]], [1, 2]).tolist())',
"check": 'assert predict_lin([[1, 0], [1, 1]], [1, 2]).tolist() == [1, 3]\nprint("All checks passed \\u2713")',
},
{
"title": 'RMSE',
"desc": 'Root mean squared error.',
"starter": 'import numpy as np\n\ndef rmse(y, yh):\n    y = np.asarray(y, float); yh = np.asarray(yh, float)\n    # TODO: sqrt(mean((y - yh)^2))\n    return 0.0\n\nprint(rmse([1, 2, 3], [1, 2, 3]))',
"check": 'assert abs(rmse([1, 2, 3], [1, 2, 3])) < 1e-12\nassert abs(rmse([0, 0], [1, 1]) - 1.0) < 1e-12\nprint("All checks passed \\u2713")',
},
{
"title": 'Posterior Precision',
"desc": 'alpha*I + beta*XtX.',
"starter": 'import numpy as np\n\ndef posterior_precision(X, alpha, beta):\n    X = np.asarray(X, float)\n    # TODO: alpha*np.eye(n_features) + beta*(X.T @ X)\n    return X\n\nprint(posterior_precision([[1, 0], [0, 1]], 1, 1).tolist())',
"check": 'assert posterior_precision([[1, 0], [0, 1]], 1, 1).tolist() == [[2, 0], [0, 2]]\nprint("All checks passed \\u2713")',
},
],
"desc": "Instead of single point estimates for coefficients, Bayesian regression gives you full distributions — capturing uncertainty in your model parameters.",
"examples": [
{"label": "Bayesian regression from scratch", "code":
"""import numpy as np

np.random.seed(42)

# Generate data: y = 2x + 1 + noise
n = 50
X = np.random.uniform(0, 10, n)
y = 2 * X + 1 + np.random.normal(0, 2, n)

# Bayesian Linear Regression (conjugate prior)
# Prior: w ~ N(0, sigma_prior^2 * I)
# Likelihood: y ~ N(Xw, sigma_noise^2 * I)

# Design matrix (add bias column)
Phi = np.column_stack([np.ones(n), X])

# Prior parameters
sigma_prior = 10      # vague prior
sigma_noise = 2       # assume known noise

# Posterior parameters (closed form!)
S_prior_inv = np.eye(2) / sigma_prior**2
S_post_inv = S_prior_inv + Phi.T @ Phi / sigma_noise**2
S_post = np.linalg.inv(S_post_inv)
mu_post = S_post @ (Phi.T @ y / sigma_noise**2)

print("Bayesian Linear Regression Results")
print(f"  Intercept: {mu_post[0]:.3f} +/- {np.sqrt(S_post[0,0]):.3f}")
print(f"  Slope:     {mu_post[1]:.3f} +/- {np.sqrt(S_post[1,1]):.3f}")

# Compare with frequentist OLS
from numpy.linalg import lstsq
w_ols = lstsq(Phi, y, rcond=None)[0]
print(f"\\n  OLS intercept: {w_ols[0]:.3f}")
print(f"  OLS slope:     {w_ols[1]:.3f}")
print("\\n  (Similar with vague prior — prior barely matters with enough data)")"""},
{"label": "Predictive distributions", "code":
"""import numpy as np

np.random.seed(42)

# Same model from above (simplified)
n = 50
X = np.random.uniform(0, 10, n)
y = 2 * X + 1 + np.random.normal(0, 2, n)
Phi = np.column_stack([np.ones(n), X])

sigma_noise = 2
S_prior_inv = np.eye(2) / 100
S_post_inv = S_prior_inv + Phi.T @ Phi / sigma_noise**2
S_post = np.linalg.inv(S_post_inv)
mu_post = S_post @ (Phi.T @ y / sigma_noise**2)

# Predict at new points
x_new = np.array([2.0, 5.0, 8.0])
Phi_new = np.column_stack([np.ones(len(x_new)), x_new])

# Predictive mean
y_pred_mean = Phi_new @ mu_post

# Predictive variance (includes both parameter and noise uncertainty)
y_pred_var = np.array([
    phi @ S_post @ phi + sigma_noise**2
    for phi in Phi_new
])

print("Bayesian Predictions (with uncertainty!)")
print(f"{'x':>5} {'Mean':>8} {'Std':>8} {'95% CI':>20}")
for x, m, v in zip(x_new, y_pred_mean, y_pred_var):
    std = np.sqrt(v)
    print(f"{x:>5.1f} {m:>8.3f} {std:>8.3f} ({m-1.96*std:>7.3f}, {m+1.96*std:>7.3f})")

print("\\nKey advantage: uncertainty GROWS as we extrapolate away from data!")"""},
],
"rw": {
    "title": "Bayesian Demand Forecasting",
    "scenario": "A retailer uses Bayesian regression to forecast product demand. The posterior uncertainty helps them set safety stock levels — wider uncertainty means more safety stock.",
    "code":
"""import numpy as np

np.random.seed(42)

# Historical demand data (with trend and noise)
weeks = np.arange(1, 53)
true_trend = 100 + 2 * weeks  # growing demand
demand = true_trend + np.random.normal(0, 15, 52)

# Bayesian regression
Phi = np.column_stack([np.ones(52), weeks])
sigma_noise = 15
S_prior_inv = np.eye(2) / 1000
S_post_inv = S_prior_inv + Phi.T @ Phi / sigma_noise**2
S_post = np.linalg.inv(S_post_inv)
mu_post = S_post @ (Phi.T @ demand / sigma_noise**2)

# Forecast next 4 weeks
future_weeks = np.array([53, 54, 55, 56])
Phi_future = np.column_stack([np.ones(4), future_weeks])

means = Phi_future @ mu_post
stds = np.array([
    np.sqrt(phi @ S_post @ phi + sigma_noise**2)
    for phi in Phi_future
])

print("4-Week Demand Forecast")
print("=" * 55)
print(f"{'Week':>5} {'Forecast':>10} {'Low (5%)':>10} {'High (95%)':>10} {'Safety Stock':>13}")
for w, m, s in zip(future_weeks, means, stds):
    low = m - 1.645 * s
    high = m + 1.645 * s
    safety = 1.645 * s  # extra stock to cover 95% of demand scenarios
    print(f"{w:>5} {m:>10.0f} {low:>10.0f} {high:>10.0f} {safety:>13.0f}")"""
},
"todos": [
    "Implement Bayesian linear regression from scratch and compare slope/intercept to OLS on the same data",
    "Vary the prior sigma from 0.1 to 100 and observe how much the posterior slope changes",
    "Compute the predictive distribution at x=0 vs x=20 and compare uncertainty widths",
    "Show that with 200 data points, a strong informative prior has little effect on the posterior",
    "Plot the 95% predictive interval at several x values and confirm it widens in extrapolation regions",
],
},

{
"title": "7. Markov Chain Monte Carlo (MCMC)",
"practices": [
{
"title": 'Acceptance Ratio',
"desc": 'Metropolis acceptance probability.',
"starter": 'import numpy as np\n\ndef mcmc_acceptance(cur, prop, logp):\n    # TODO: min(1, exp(logp(prop) - logp(cur))) as a float\n    return 0.0\n\nprint(mcmc_acceptance(0.0, 0.0, lambda x: -x*x))',
"check": 'assert abs(mcmc_acceptance(0.0, 0.0, lambda x: -x*x) - 1.0) < 1e-12, "equal density always accepts"\nassert mcmc_acceptance(0.0, 5.0, lambda x: -x*x) < 1e-6, "much worse proposals are rejected"\nprint("All checks passed \\u2713")',
},
],
"desc": "When posterior distributions don't have closed-form solutions, MCMC algorithms draw samples from the posterior by constructing a Markov chain. This enables Bayesian inference for complex models.",
"examples": [
{"label": "Metropolis-Hastings from scratch", "code":
"""import numpy as np

np.random.seed(42)

# Goal: sample from a posterior distribution
# Likelihood: data ~ Normal(mu, sigma=2) — we observe data
# Prior: mu ~ Normal(0, 10)
# Posterior: mu | data ~ ?

data = np.random.normal(5, 2, 30)  # true mu = 5

def log_posterior(mu, data, sigma=2, prior_mean=0, prior_std=10):
    # Log-likelihood
    log_lik = -0.5 * np.sum(((data - mu) / sigma) ** 2)
    # Log-prior
    log_prior = -0.5 * ((mu - prior_mean) / prior_std) ** 2
    return log_lik + log_prior

# Metropolis-Hastings algorithm
n_samples = 10000
samples = np.zeros(n_samples)
current = 0  # starting value
proposal_std = 0.5

accepted = 0
for i in range(n_samples):
    # Propose new value
    proposal = current + np.random.normal(0, proposal_std)

    # Accept/reject
    log_ratio = log_posterior(proposal, data) - log_posterior(current, data)
    if np.log(np.random.random()) < log_ratio:
        current = proposal
        accepted += 1

    samples[i] = current

# Discard burn-in
burn_in = 1000
samples = samples[burn_in:]

print(f"True mu:          5.000")
print(f"Sample mean:      {np.mean(data):.3f}")
print(f"MCMC posterior mean: {np.mean(samples):.3f}")
print(f"MCMC posterior std:  {np.std(samples):.3f}")
print(f"95% Credible:     ({np.percentile(samples, 2.5):.3f}, {np.percentile(samples, 97.5):.3f})")
print(f"Acceptance rate:   {accepted/n_samples:.1%}")"""},
{"label": "MCMC diagnostics", "code":
"""import numpy as np

def run_mcmc_chain(data, n_samples=5000, start=0, proposal_std=0.5, seed=None):
    if seed: np.random.seed(seed)

    def log_post(mu):
        return -0.5 * np.sum(((data - mu) / 2) ** 2) - 0.5 * (mu / 10) ** 2

    samples = np.zeros(n_samples)
    current = start
    for i in range(n_samples):
        proposal = current + np.random.normal(0, proposal_std)
        if np.log(np.random.random()) < log_post(proposal) - log_post(current):
            current = proposal
        samples[i] = current
    return samples

data = np.random.normal(5, 2, 30)

# Run multiple chains with different starting points
chains = [run_mcmc_chain(data, seed=i, start=s)
          for i, s in enumerate([0, 10, -10, 5])]

# Diagnostic 1: Trace plot statistics
for i, chain in enumerate(chains):
    print(f"Chain {i}: mean={np.mean(chain[1000:]):.3f}, std={np.std(chain[1000:]):.3f}")

# Diagnostic 2: R-hat (Gelman-Rubin statistic)
# Should be < 1.01 for convergence
chain_means = [np.mean(c[1000:]) for c in chains]
chain_vars = [np.var(c[1000:]) for c in chains]
n = len(chains[0]) - 1000
W = np.mean(chain_vars)  # within-chain variance
B = n * np.var(chain_means)  # between-chain variance
var_hat = (1 - 1/n) * W + B/n
R_hat = np.sqrt(var_hat / W)
print(f"\\nR-hat: {R_hat:.4f} ({'converged' if R_hat < 1.01 else 'NOT converged'})")

# Diagnostic 3: Effective sample size (approximate)
# Autocorrelation reduces effective samples
for i, chain in enumerate(chains):
    c = chain[1000:]
    autocorr = np.corrcoef(c[:-1], c[1:])[0, 1]
    ess = len(c) * (1 - autocorr) / (1 + autocorr)
    print(f"Chain {i}: autocorr={autocorr:.3f}, ESS≈{ess:.0f}")"""},
],
"rw": {
    "title": "Bayesian Parameter Estimation for A/B Testing",
    "scenario": "Using MCMC to estimate both conversion rate AND the difference between variants, giving rich posterior distributions for decision-making.",
    "code":
"""import numpy as np

np.random.seed(42)

# A/B test data
data_a = np.random.binomial(1, 0.10, 500)  # 10% true conversion
data_b = np.random.binomial(1, 0.13, 500)  # 13% true conversion

def log_posterior_ab(theta_a, theta_b, data_a, data_b):
    if not (0 < theta_a < 1 and 0 < theta_b < 1):
        return -np.inf
    log_lik_a = np.sum(data_a * np.log(theta_a) + (1-data_a) * np.log(1-theta_a))
    log_lik_b = np.sum(data_b * np.log(theta_b) + (1-data_b) * np.log(1-theta_b))
    # Uniform prior on (0,1) — log(1) = 0
    return log_lik_a + log_lik_b

# MCMC sampling
n_samples = 20000
samples_a = np.zeros(n_samples)
samples_b = np.zeros(n_samples)
current_a, current_b = 0.1, 0.1

for i in range(n_samples):
    prop_a = current_a + np.random.normal(0, 0.02)
    prop_b = current_b + np.random.normal(0, 0.02)

    log_ratio = (log_posterior_ab(prop_a, prop_b, data_a, data_b) -
                 log_posterior_ab(current_a, current_b, data_a, data_b))
    if np.log(np.random.random()) < log_ratio:
        current_a, current_b = prop_a, prop_b

    samples_a[i] = current_a
    samples_b[i] = current_b

# Burn-in
sa, sb = samples_a[5000:], samples_b[5000:]
diff = sb - sa

print("MCMC A/B Test Results")
print(f"theta_A: {np.mean(sa):.4f} ({np.percentile(sa, 2.5):.4f}, {np.percentile(sa, 97.5):.4f})")
print(f"theta_B: {np.mean(sb):.4f} ({np.percentile(sb, 2.5):.4f}, {np.percentile(sb, 97.5):.4f})")
print(f"diff:    {np.mean(diff):.4f} ({np.percentile(diff, 2.5):.4f}, {np.percentile(diff, 97.5):.4f})")
print(f"P(B>A):  {np.mean(diff > 0):.4f}")"""
},
"todos": [
    "Implement Metropolis-Hastings from scratch to sample from a Normal posterior — check acceptance rate",
    "Run 4 chains from different starting points and compute R-hat — verify it is below 1.01",
    "Vary the proposal standard deviation (0.01 vs 1.0 vs 5.0) and compare acceptance rates",
    "Discard burn-in of 100, 500, and 2000 samples — see how much the posterior mean changes",
    "Compute the effective sample size for a chain and compare it to the raw number of samples",
],
},

{
"title": "8. Probabilistic Programming with PyMC",
"practices": [
{
"title": 'Posterior Mean After Burn-in',
"desc": 'Average the trace after discarding burn-in.',
"starter": 'import numpy as np\n\ndef trace_mean(samples, burn):\n    s = np.asarray(samples, float)\n    # TODO: mean of the samples after the first burn entries\n    return 0.0\n\nprint(trace_mean([100, 1, 1, 1], 1))',
"check": 'assert trace_mean([100, 1, 1, 1], 1) == 1.0, "the burn-in sample is discarded"\nprint("All checks passed \\u2713")',
},
],
"desc": "PyMC (formerly PyMC3) lets you define Bayesian models in Python and automatically runs MCMC inference. It handles the hard sampling algorithms so you can focus on modeling.",
"examples": [
{"label": "Getting started with PyMC", "code":
"""# pip install pymc arviz
import numpy as np

# PyMC model syntax (conceptual — requires pymc installed)
# This shows the pattern; actual execution needs PyMC

np.random.seed(42)
data = np.random.normal(5, 2, 100)

print("PyMC Model Definition (install pymc to run):")
print(\"\"\"
import pymc as pm
import arviz as az

with pm.Model() as model:
    # Priors
    mu = pm.Normal("mu", mu=0, sigma=10)
    sigma = pm.HalfNormal("sigma", sigma=5)

    # Likelihood
    obs = pm.Normal("obs", mu=mu, sigma=sigma, observed=data)

    # Inference (NUTS sampler — automatic!)
    trace = pm.sample(2000, tune=1000, cores=2)

# Results
print(az.summary(trace))
az.plot_posterior(trace)
\"\"\")

# Without PyMC, we can do the same with scipy
from scipy import stats

# Analytical posterior for Normal-Normal model
n = len(data)
x_bar = np.mean(data)
sigma_known = 2
prior_mu, prior_sigma = 0, 10

post_var = 1 / (n/sigma_known**2 + 1/prior_sigma**2)
post_mean = post_var * (n * x_bar / sigma_known**2 + prior_mu / prior_sigma**2)
post_std = np.sqrt(post_var)

print(f"\\nAnalytical posterior: mu = {post_mean:.3f} +/- {post_std:.3f}")
print(f"95% CI: ({post_mean - 1.96*post_std:.3f}, {post_mean + 1.96*post_std:.3f})")"""},
{"label": "Bayesian logistic regression concept", "code":
"""import numpy as np
from scipy.special import expit  # sigmoid function

np.random.seed(42)

# Generate classification data
n = 200
X = np.random.normal(0, 1, (n, 2))
true_w = np.array([1.5, -2.0])
true_b = 0.5
probs = expit(X @ true_w + true_b)
y = np.random.binomial(1, probs)

print(f"Generated {n} samples, {y.sum()} positive")
print(f"True weights: {true_w}, bias: {true_b}")

# Bayesian approach: place priors on weights
# w ~ Normal(0, 2)
# b ~ Normal(0, 5)

# With PyMC:
print(\"\"\"
with pm.Model() as logistic_model:
    # Priors on weights
    w = pm.Normal("w", mu=0, sigma=2, shape=2)
    b = pm.Normal("b", mu=0, sigma=5)

    # Linear predictor
    logit_p = pm.math.dot(X, w) + b

    # Likelihood
    obs = pm.Bernoulli("obs", logit_p=logit_p, observed=y)

    # Sample posterior
    trace = pm.sample(2000, tune=1000)

# Now you have DISTRIBUTIONS over w and b, not just point estimates!
# This gives you uncertainty in predictions.
\"\"\")

# Quick frequentist comparison
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(C=1/4)  # C = 1/prior_var
lr.fit(X, y)
print(f"\\nFrequentist: w = {lr.coef_[0]}, b = {lr.intercept_[0]:.3f}")
print("(Bayesian gives distributions, not just point estimates)")"""},
],
"rw": {
    "title": "Bayesian Customer Lifetime Value",
    "scenario": "A subscription business models customer lifetime value (CLV) using Bayesian methods, giving not just an estimate but uncertainty bounds for financial planning.",
    "code":
"""import numpy as np
from scipy import stats

np.random.seed(42)

# Customer data: monthly churn rates observed over 12 months
monthly_churns = [15, 12, 10, 8, 11, 9, 7, 10, 8, 6, 9, 7]
monthly_active = [1000, 985, 973, 963, 955, 944, 935, 928, 918, 910, 904, 895]

# Bayesian estimation of churn rate
total_churns = sum(monthly_churns)
total_observations = sum(monthly_active)

# Beta posterior for monthly churn rate
alpha = 1 + total_churns
beta = 1 + total_observations - total_churns

# Sample churn rates from posterior
n_samples = 50000
churn_samples = np.random.beta(alpha, beta, n_samples)

# For each churn rate, compute CLV
monthly_revenue = 50  # $50/month subscription
discount_rate = 0.01  # monthly discount rate

# CLV = monthly_revenue / (churn_rate + discount_rate)
clv_samples = monthly_revenue / (churn_samples + discount_rate)

print("Bayesian CLV Analysis")
print("=" * 45)
print(f"Monthly churn rate: {np.mean(churn_samples):.4f} "
      f"({np.percentile(churn_samples, 2.5):.4f}, {np.percentile(churn_samples, 97.5):.4f})")
print(f"\\nCustomer Lifetime Value:")
print(f"  Mean:   ${np.mean(clv_samples):>10,.2f}")
print(f"  Median: ${np.median(clv_samples):>10,.2f}")
print(f"  5th %%:  ${np.percentile(clv_samples, 5):>10,.2f}")
print(f"  95th %%: ${np.percentile(clv_samples, 95):>10,.2f}")
print(f"\\nFor 1000 customers:")
total_clv = clv_samples * 1000
print(f"  Expected: ${np.mean(total_clv):>12,.0f}")
print(f"  Worst 5%%: ${np.percentile(total_clv, 5):>12,.0f}")
print(f"  Best 95%%: ${np.percentile(total_clv, 95):>12,.0f}")"""
},
"todos": [
    "Write out a PyMC model definition (as a comment/string) for a simple Normal likelihood problem",
    "Implement the analytical Normal-Normal posterior update and compare it to a Metropolis-Hastings estimate",
    "Compute a Bayesian CLV estimate from monthly churn data — report mean, 5th, and 95th percentile",
    "Model Bayesian logistic regression weights manually using MCMC and compare to sklearn's coefficients",
    "Interpret a PyMC trace summary — identify which parameters have converged vs are still uncertain",
],
},

{
"title": "9. Bayesian vs Frequentist — When to Use Which",
"practices": [
{
"title": 'Interpretation',
"desc": 'Which quantity each interval describes.',
"starter": 'def credible_vs_confidence(kind):\n    # TODO: "probability" for a credible interval, "coverage" otherwise\n    return ""\n\nprint(credible_vs_confidence("credible"), credible_vs_confidence("confidence"))',
"check": 'assert credible_vs_confidence("credible") == "probability"\nassert credible_vs_confidence("confidence") == "coverage"\nprint("All checks passed \\u2713")',
},
],
"desc": "Both approaches have strengths. Understanding the differences helps you choose the right tool for each problem.",
"examples": [
{"label": "Side-by-side comparison", "code":
"""import numpy as np
from scipy import stats

np.random.seed(42)
data = np.random.normal(5, 2, 30)

# ─── FREQUENTIST APPROACH ───
sample_mean = np.mean(data)
sample_se = stats.sem(data)
ci_freq = stats.t.interval(0.95, df=len(data)-1, loc=sample_mean, scale=sample_se)
p_value = stats.ttest_1samp(data, 0).pvalue

print("FREQUENTIST")
print(f"  Point estimate: {sample_mean:.3f}")
print(f"  95% CI: ({ci_freq[0]:.3f}, {ci_freq[1]:.3f})")
print(f"  p-value (mu=0): {p_value:.6f}")
print(f"  Interpretation: 'If we repeated this experiment,")
print(f"   95% of CIs would contain the true mean.'")

# ─── BAYESIAN APPROACH ───
# Prior: mu ~ Normal(0, 10)  (vague prior)
prior_mu, prior_sigma = 0, 10
sigma_known = 2
n = len(data)

post_var = 1 / (n/sigma_known**2 + 1/prior_sigma**2)
post_mean = post_var * (n * sample_mean / sigma_known**2 + prior_mu / prior_sigma**2)
post_std = np.sqrt(post_var)
ci_bayes = (post_mean - 1.96*post_std, post_mean + 1.96*post_std)
P_positive = 1 - stats.norm(post_mean, post_std).cdf(0)

print(f"\\nBAYESIAN")
print(f"  Posterior mean: {post_mean:.3f}")
print(f"  95% Credible: ({ci_bayes[0]:.3f}, {ci_bayes[1]:.3f})")
print(f"  P(mu > 0): {P_positive:.6f}")
print(f"  Interpretation: 'There is a {P_positive:.1%} probability")
print(f"   that the true mean is positive.'")"""},
{"label": "Decision guide", "code":
"""# When to use BAYESIAN methods:
# ✓ You have prior knowledge to incorporate
# ✓ You want probability statements about parameters
# ✓ You need uncertainty quantification
# ✓ Small sample sizes (prior helps regularize)
# ✓ A/B testing (direct P(B>A))
# ✓ Hierarchical/multilevel models
# ✓ Sequential updating (online learning)

# When to use FREQUENTIST methods:
# ✓ Large samples (results converge anyway)
# ✓ Regulatory/publication requirements (p-values expected)
# ✓ Simple hypothesis testing
# ✓ No strong prior knowledge
# ✓ Computational simplicity needed
# ✓ Objective analysis required (no prior debate)

import pandas as pd

comparison = pd.DataFrame({
    "Aspect": ["Probability meaning", "Parameters", "Data", "Uncertainty",
               "Prior needed", "Sample size", "Computation"],
    "Frequentist": ["Long-run frequency", "Fixed (unknown)", "Random",
                    "Confidence intervals", "No", "Needs large N", "Fast"],
    "Bayesian": ["Degree of belief", "Random variables", "Fixed (observed)",
                 "Credible intervals", "Yes", "Works with small N", "Can be slow"],
})
print(comparison.to_string(index=False))"""},
],
"todos": [
    "Compute a frequentist 95% CI and a Bayesian 95% credible interval on the same dataset — explain the difference",
    "Run a t-test and a Bayesian test on the same data — compare the p-value to P(mu > 0)",
    "Show that with n=5 samples, a strong prior substantially changes the posterior mean vs MLE",
    "Identify 3 real problems from your work where Bayesian thinking would be more appropriate than p-values",
    "Compute P(mu > 0) using a Bayesian posterior and interpret it as a probability statement",
],
},

{
"title": "10. Bayesian Optimization for Hyperparameter Tuning",
"practices": [
{
"title": 'Expected Improvement',
"desc": 'EI acquisition value at a candidate point.',
"starter": 'import numpy as np\nfrom scipy import stats\n\ndef expected_improvement(best, mu, sigma):\n    if sigma <= 0:\n        return 0.0\n    z = (mu - best) / sigma\n    # TODO: (mu - best)*norm.cdf(z) + sigma*norm.pdf(z)\n    return 0.0\n\nprint(round(expected_improvement(1.0, 1.5, 1.0), 4))',
"check": 'assert expected_improvement(1.0, 1.5, 1.0) > 0, "a promising point has positive EI"\nassert expected_improvement(1.0, 1.5, 0.0) == 0.0, "no uncertainty, no improvement"\nprint("All checks passed \\u2713")',
},
],
"desc": "Bayesian optimization uses a probabilistic model to smartly search hyperparameter space — much more efficient than grid or random search.",
"examples": [
{"label": "Bayesian optimization concept", "code":
"""import numpy as np

np.random.seed(42)

# Bayesian optimization builds a surrogate model (usually Gaussian Process)
# of the objective function and uses an acquisition function to decide
# where to sample next.

# Simulate optimizing a black-box function
def objective(x):
    \"\"\"Expensive function we want to maximize (e.g., model accuracy).\"\"\"
    return -(x - 3)**2 + 10 + np.random.normal(0, 0.1)

# Random search (baseline)
n_random = 20
random_x = np.random.uniform(0, 10, n_random)
random_y = [objective(x) for x in random_x]
best_random = random_x[np.argmax(random_y)]
print(f"Random search best: x={best_random:.3f}, y={max(random_y):.3f}")

# Simple Bayesian-inspired search (acquisition = upper confidence bound)
# In practice, use libraries like Optuna or scikit-optimize
evaluated_x = list(np.random.uniform(0, 10, 3))
evaluated_y = [objective(x) for x in evaluated_x]

for i in range(17):  # same budget as random search
    # Simplified: explore near best + some randomness
    best_so_far = evaluated_x[np.argmax(evaluated_y)]
    next_x = best_so_far + np.random.normal(0, 2 / (i + 1))
    next_x = np.clip(next_x, 0, 10)
    next_y = objective(next_x)
    evaluated_x.append(next_x)
    evaluated_y.append(next_y)

best_bayes = evaluated_x[np.argmax(evaluated_y)]
print(f"Bayesian search best: x={best_bayes:.3f}, y={max(evaluated_y):.3f}")
print(f"True optimum: x=3.000, y=10.000")"""},
{"label": "Optuna — practical Bayesian hyperparameter tuning", "code":
"""# pip install optuna
# Optuna uses Tree-structured Parzen Estimator (TPE) — a Bayesian method

import numpy as np

# Example: tuning a model (without optuna, showing the pattern)
print(\"\"\"
import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

def objective(trial):
    # Optuna suggests hyperparameters
    n_estimators = trial.suggest_int("n_estimators", 50, 500)
    max_depth = trial.suggest_int("max_depth", 3, 20)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)
    max_features = trial.suggest_categorical("max_features", ["sqrt", "log2"])

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        max_features=max_features,
        random_state=42,
    )

    score = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    return score.mean()

# Run optimization
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100)

print(f"Best accuracy: {study.best_value:.4f}")
print(f"Best params: {study.best_params}")
\"\"\")

# Key advantages of Bayesian optimization:
print("Advantages over Grid/Random Search:")
print("  1. Learns from previous evaluations")
print("  2. Focuses on promising regions")
print("  3. Typically finds better results in fewer trials")
print("  4. Handles conditional parameters naturally")
print("  5. Works well with expensive objective functions")"""},
],
"rw": {
    "title": "Bayesian Model Selection Pipeline",
    "scenario": "A data science team uses Bayesian optimization to efficiently search across both model types and hyperparameters, finding the best configuration in minimal compute time.",
    "code":
"""import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

np.random.seed(42)
X, y = make_classification(n_samples=500, n_features=20,
                           n_informative=10, random_state=42)

# Simple Bayesian-inspired model search
# (In production, use Optuna for this)
results = []

configs = [
    ("LR C=0.1", LogisticRegression(C=0.1, max_iter=1000)),
    ("LR C=1",   LogisticRegression(C=1.0, max_iter=1000)),
    ("LR C=10",  LogisticRegression(C=10, max_iter=1000)),
    ("RF n=50",  RandomForestClassifier(n_estimators=50, random_state=42)),
    ("RF n=200", RandomForestClassifier(n_estimators=200, random_state=42)),
    ("GB n=100", GradientBoostingClassifier(n_estimators=100, random_state=42)),
    ("GB n=200", GradientBoostingClassifier(n_estimators=200, learning_rate=0.05, random_state=42)),
]

print(f"{'Config':<12} {'Mean CV':>8} {'Std':>6}")
print("-" * 28)
for name, model in configs:
    scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    results.append((name, scores.mean(), scores.std()))
    print(f"{name:<12} {scores.mean():>8.4f} {scores.std():>6.4f}")

best = max(results, key=lambda x: x[1])
print(f"\\nBest: {best[0]} with accuracy {best[1]:.4f}")
print("\\nWith Optuna, this search is automated and more efficient!")"""
},
"todos": [
    "Implement a simple random search vs a greedy exploit-and-explore search on a 1D objective function",
    "Install Optuna and run a 20-trial study on a RandomForest — print best params and accuracy",
    "Compare 50-trial random search vs 50-trial Optuna TPE on the same model — which finds better params?",
    "Add early pruning to an Optuna study using a pruner and observe how it skips bad trials",
    "Use Optuna to tune both model type (RF vs GB) and hyperparameters in a single categorical study",
],
},

{
"title": "Practice Lab: Bayesian Updating",
"desc": "Hands-on Bayesian challenges (NumPy + SciPy, Pyodide-runnable). Press Run to try a snippet, then solve the exercise and press Check.",
"examples": [
    {"label": "Bayes' theorem: medical test", "code": '''# A test is 99% sensitive and 95% specific; the disease affects 1% of people.
p_disease = 0.01
p_pos_given_disease = 0.99           # sensitivity
p_pos_given_healthy = 0.05           # 1 - specificity

p_pos = p_pos_given_disease * p_disease + p_pos_given_healthy * (1 - p_disease)
posterior = p_pos_given_disease * p_disease / p_pos
print("P(disease | positive) =", round(posterior, 4))
print("Even after a positive test, the probability is only ~17%.")'''},
    {"label": "Beta-Binomial posterior", "code": '''from scipy import stats

# Prior Beta(2, 2); observe 8 heads in 10 flips
a0, b0, heads, n = 2, 2, 8, 10
post = stats.beta(a0 + heads, b0 + (n - heads))

print("posterior mean:", round(post.mean(), 4))
ci = post.interval(0.95)
print("95% credible interval:", [round(float(x), 3) for x in ci])'''},
],
"todos": [
    "Apply Bayes' theorem to the medical-test problem and explain the low posterior",
    "Update a Beta prior with observed heads/tails to get the posterior Beta",
    "Compute the posterior mean a / (a + b) of a Beta distribution",
    "Read a 95% credible interval from scipy.stats.beta(...).interval(0.95)",
],
"practice": {
    "title": "Beta Posterior Update",
    "desc": "Implement update_beta(prior_a, prior_b, heads, tails) returning the updated (a, b), and posterior_mean(a, b) returning a / (a + b). Fill in the functions, press Run, then press Check.",
    "starter": '''def update_beta(prior_a, prior_b, heads, tails):
    # TODO: a conjugate Beta prior updates by adding heads to a and tails to b
    return (prior_a, prior_b)

def posterior_mean(a, b):
    # TODO: return the mean of Beta(a, b)
    return 0.0

a, b = update_beta(1, 1, 7, 3)
pm = posterior_mean(a, b)
print("posterior:", (a, b), "mean:", round(pm, 4))''',
    "check": '''assert (a, b) == (8, 4), "Beta(1,1) updated with 7 heads, 3 tails is Beta(8,4)"
assert abs(pm - 8/12) < 1e-9, "posterior mean is a/(a+b) = 8/12"
print("All checks passed \\u2713")'''
}
},

{
"title": "Challenge: Normalize a Posterior",
"desc": "A discrete posterior is just proportional weights divided by their sum. Press Run, then solve and press Check.",
"examples": [
    {"label": "Weights to probabilities", "code": '''import numpy as np

weights = np.array([1, 1, 2], float)
probs = weights / weights.sum()
print("probs:", probs.tolist(), "sum:", probs.sum())'''},
],
"todos": [
    "Divide each weight by the total to get probabilities",
    "Confirm the probabilities sum to 1",
],
"practice": {
    "title": "Normalize",
    "desc": "Implement normalize(weights): return probabilities proportional to the weights that sum to 1. Fill in the function, press Run, then press Check.",
    "starter": '''import numpy as np

def normalize(weights):
    w = np.asarray(weights, float)
    # TODO: divide by the total so the result sums to 1
    return w

print(normalize([1, 1, 2]).tolist())''',
    "check": '''import numpy as np
p = normalize([1, 1, 2])
assert np.isclose(p.sum(), 1), "a probability vector sums to 1"
assert np.allclose(p, [0.25, 0.25, 0.5]), "proportional to the weights"
print("All checks passed \\u2713")'''
}
},

{
"title": "Challenge: Bayes Update",
"desc": "Posterior is proportional to prior times likelihood, then normalized. Press Run, then solve and press Check.",
"examples": [
    {"label": "Prior x likelihood", "code": '''import numpy as np

prior = np.array([0.5, 0.5])
likelihood = np.array([0.8, 0.4])
unnorm = prior * likelihood
posterior = unnorm / unnorm.sum()
print("posterior:", posterior.round(3).tolist())'''},
],
"todos": [
    "Multiply prior by likelihood elementwise",
    "Normalize the product so the posterior sums to 1",
],
"practice": {
    "title": "Posterior from Prior and Likelihood",
    "desc": "Implement bayes_update(priors, likelihoods): return the normalized posterior proportional to priors * likelihoods. Fill in the function, press Run, then press Check.",
    "starter": '''import numpy as np

def bayes_update(priors, likelihoods):
    p = np.asarray(priors, float)
    l = np.asarray(likelihoods, float)
    # TODO: posterior is proportional to p * l, normalized to sum to 1
    return p

post = bayes_update([0.5, 0.5], [0.8, 0.4])
print(post.round(3).tolist())''',
    "check": '''import numpy as np
post = bayes_update([0.5, 0.5], [0.8, 0.4])
assert np.isclose(post.sum(), 1), "posterior sums to 1"
assert np.isclose(post[0], 0.8 * 0.5 / (0.8 * 0.5 + 0.4 * 0.5)), "Bayes' rule for hypothesis 0"
assert post[0] > post[1], "the higher-likelihood hypothesis gets more posterior mass"
print("All checks passed \\u2713")'''
}
},

{
"title": "Challenge: Expected Value",
"desc": "The expected value of a discrete distribution is the probability-weighted average of its outcomes. Press Run, then solve and press Check.",
"examples": [
    {"label": "Weighted average", "code": '''import numpy as np

values = np.array([1, 2, 3])
probs = np.array([0.2, 0.3, 0.5])
print("E[X]:", float(values @ probs))'''},
],
"todos": [
    "E[X] = sum(value * probability)",
    "A dot product does this in one step",
],
"practice": {
    "title": "Expected Value",
    "desc": "Implement expected_value(values, probs): return the expected value of a discrete distribution. Fill in the function, press Run, then press Check.",
    "starter": '''import numpy as np

def expected_value(values, probs):
    # TODO: probability-weighted sum of the values
    return 0.0

print(expected_value([1, 2, 3], [0.2, 0.3, 0.5]))''',
    "check": '''assert abs(expected_value([1, 2, 3], [0.2, 0.3, 0.5]) - 2.3) < 1e-9, "0.2*1 + 0.3*2 + 0.5*3 = 2.3"
assert abs(expected_value([10, 20], [0.5, 0.5]) - 15.0) < 1e-9, "fair average of 10 and 20"
print("All checks passed \\u2713")'''
}
},

{
"title": "Challenge: Log-Odds",
"desc": "Log-odds (the logit) maps a probability to the real line — the link function behind logistic regression. Press Run, then solve and press Check.",
"examples": [
    {"label": "Probability to logit", "code": '''import numpy as np

for p in [0.25, 0.5, 0.75]:
    print(p, "->", round(float(np.log(p / (1 - p))), 3))'''},
],
"todos": [
    "Odds = p / (1 - p); log-odds is its natural log",
    "p = 0.5 gives log-odds 0; above 0.5 is positive",
],
"practice": {
    "title": "Logit",
    "desc": "Implement log_odds(p): return the natural log of the odds p / (1 - p). Fill in the function, press Run, then press Check.",
    "starter": '''import numpy as np

def log_odds(p):
    p = float(p)
    # TODO: return ln( p / (1 - p) )
    return 0.0

print(round(log_odds(0.75), 4))''',
    "check": '''import numpy as np
assert abs(log_odds(0.5)) < 1e-12, "p=0.5 -> log-odds 0"
assert log_odds(0.75) > 0, "p above 0.5 -> positive log-odds"
assert log_odds(0.25) < 0, "p below 0.5 -> negative log-odds"
assert abs(log_odds(0.8) - np.log(0.8 / 0.2)) < 1e-9, "matches ln(odds)"
print("All checks passed \\u2713")'''
}
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
