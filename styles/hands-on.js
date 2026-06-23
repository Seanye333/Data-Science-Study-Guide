/* hands-on.js — make code on every module page runnable in the browser.
 *
 *  • Practice blocks      → a full editable editor (Run / Reset / Copy + output)
 *  • Example / real-world → a compact "Run" + "Edit" toolbar under the snippet
 *
 * Code runs entirely client-side via Pyodide (CPython → WASM). The runtime is
 * lazy-loaded on the first Run anywhere on the page, so normal page loads stay
 * light and there is no backend. Progressive enhancement: if this script or
 * Pyodide fails to load, the original code is still shown and copyable. */
(function () {
  "use strict";

  var PYODIDE_VERSION = "0.26.4";
  var PYODIDE_URL =
    "https://cdn.jsdelivr.net/pyodide/v" + PYODIDE_VERSION + "/full/pyodide.js";

  // ── one-time styles ────────────────────────────────────────────────────────
  function injectStyles() {
    if (document.getElementById("ho-styles")) return;
    var css =
      ".ho{margin-top:12px}" +
      ".ho-editor{width:100%;box-sizing:border-box;min-height:120px;resize:vertical;" +
      "font:0.83rem/1.5 'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;" +
      "color:#e6edf3;background:rgba(13,17,23,.85);border:1px solid rgba(255,255,255,.12);" +
      "border-radius:10px;padding:13px;tab-size:4;white-space:pre;overflow-wrap:normal;" +
      "overflow-x:auto;outline:none}" +
      ".ho-editor:focus{border-color:var(--acc,#58a6ff);box-shadow:0 0 0 2px rgba(88,166,255,.25)}" +
      ".ho-bar{display:flex;align-items:center;gap:8px;margin:8px 0}" +
      ".ho-bar.ho-inline{margin:6px 0 2px}" +
      ".ho-btn{cursor:pointer;border:1px solid rgba(255,255,255,.15);border-radius:8px;" +
      "padding:6px 14px;font-size:.82rem;font-weight:600;color:#e6edf3;" +
      "background:rgba(255,255,255,.06);transition:background .15s,border-color .15s}" +
      ".ho-btn:hover{background:rgba(255,255,255,.12)}" +
      ".ho-btn.ho-sm{padding:3px 11px;font-size:.76rem}" +
      ".ho-run{color:#0d1117;background:var(--acc,#58a6ff);border-color:transparent}" +
      ".ho-run:hover{filter:brightness(1.08);background:var(--acc,#58a6ff)}" +
      ".ho-btn[disabled]{opacity:.55;cursor:default}" +
      ".ho-status{font-size:.78rem;color:#8b949e;margin-left:auto}" +
      ".ho-out{margin:6px 0 0;white-space:pre-wrap;word-break:break-word;" +
      "font:0.82rem/1.5 'SFMono-Regular',Consolas,Menlo,monospace;color:#c9d1d9;" +
      "background:rgba(13,17,23,.6);border:1px solid rgba(255,255,255,.08);border-radius:10px;" +
      "padding:11px 13px;max-height:340px;overflow:auto;display:none}" +
      ".ho-out.show{display:block}" +
      ".ho-out img{max-width:100%;display:block;margin:8px 0;border-radius:8px}" +
      ".ho-err{color:#ff7b72}" +
      ".ho-ok{color:#3fb950;font-weight:600;margin-top:6px}" +
      ".ho-muted{color:#8b949e}" +
      "body.light-mode .ho-editor{color:#1f2328;background:rgba(255,255,255,.75)}" +
      "body.light-mode .ho-out{color:#1f2328;background:rgba(255,255,255,.6)}";
    var st = document.createElement("style");
    st.id = "ho-styles";
    st.textContent = css;
    document.head.appendChild(st);
  }

  // ── lazy Pyodide loader (shared across all blocks on the page) ──────────────
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = function () {
        reject(new Error("Failed to load " + src));
      };
      document.head.appendChild(s);
    });
  }

  // Python epilogue: grab any open matplotlib figures as base64 PNGs so plots
  // from matplotlib / seaborn show up in the output (Pyodide has no screen).
  var FIG_CAPTURE =
    "def __ho_figs():\n" +
    "    import sys\n" +
    "    if 'matplotlib' not in sys.modules:\n" +
    "        return []\n" +
    "    try:\n" +
    "        import matplotlib.pyplot as plt, io, base64\n" +
    "    except Exception:\n" +
    "        return []\n" +
    "    out = []\n" +
    "    for n in plt.get_fignums():\n" +
    "        buf = io.BytesIO()\n" +
    "        try:\n" +
    "            plt.figure(n).savefig(buf, format='png', bbox_inches='tight', dpi=100)\n" +
    "            out.append(base64.b64encode(buf.getvalue()).decode())\n" +
    "        except Exception:\n" +
    "            pass\n" +
    "    plt.close('all')\n" +
    "    return out\n" +
    "__ho_figs()\n";

  function appendFigures(py, out) {
    return py
      .runPythonAsync(FIG_CAPTURE)
      .then(function (res) {
        if (!res) return;
        var figs = res.toJs ? res.toJs() : res;
        if (res.destroy) res.destroy();
        (figs || []).forEach(function (b64) {
          var img = document.createElement("img");
          img.src = "data:image/png;base64," + b64;
          img.alt = "matplotlib figure";
          out.appendChild(img);
          out.classList.add("show");
        });
      })
      .catch(function () {});
  }

  function ensurePyodide() {
    if (window.__hoPyodide) return Promise.resolve(window.__hoPyodide);
    if (window.__hoPyodideLoading) return window.__hoPyodideLoading;
    window.__hoPyodideLoading = loadScript(PYODIDE_URL)
      .then(function () {
        return window.loadPyodide();
      })
      .then(function (py) {
        window.__hoPyodide = py;
        return py;
      });
    return window.__hoPyodideLoading;
  }

  // ── run code, stream stdout/stderr into an output console ───────────────────
  function runCode(getCode, out, status, runBtn) {
    var code = getCode();
    out.classList.add("show");
    out.textContent = "";
    status.textContent = window.__hoPyodide
      ? "Running…"
      : "Loading Python… (first run downloads the runtime)";
    runBtn.disabled = true;

    var chunks = [];
    function flush() {
      out.textContent = chunks.join("");
    }

    return ensurePyodide()
      .then(function (py) {
        status.textContent = "Running…";
        py.setStdout({ batched: function (s) { chunks.push(s + "\n"); flush(); } });
        py.setStderr({ batched: function (s) { chunks.push(s + "\n"); flush(); } });
        return py
          .loadPackagesFromImports(code, {
            messageCallback: function () {},
            errorCallback: function () {},
          })
          .catch(function () {})
          .then(function () {
            return py.runPythonAsync(code);
          })
          .then(function () {
            return appendFigures(py, out);
          });
      })
      .then(function () {
        if (!chunks.length && !out.querySelector("img")) {
          out.innerHTML = '<span class="ho-muted">(ran with no output)</span>';
        }
        status.textContent = "Done";
      })
      .catch(function (err) {
        var msg = (err && err.message ? err.message : String(err)).trim();
        var span = document.createElement("span");
        span.className = "ho-err";
        span.textContent = (chunks.length ? "\n" : "") + msg;
        out.appendChild(span);
        status.textContent = "Error";
      })
      .then(function () {
        runBtn.disabled = false;
      });
  }

  // Run the learner's code followed by the hidden assertions; a clean run means
  // all checks passed, an exception (e.g. AssertionError) is shown in red.
  function runCheck(userCode, checkSrc, out, status, btn) {
    var combined = userCode + "\n\n# --- checks ---\n" + checkSrc;
    return runCode(function () { return combined; }, out, status, btn).then(
      function () {
        if (status.textContent === "Done") {
          var ok = document.createElement("div");
          ok.className = "ho-ok";
          ok.textContent = "✓ All checks passed";
          out.appendChild(ok);
          out.classList.add("show");
          status.textContent = "Passed";
        }
      }
    );
  }

  function autoSize(ta) {
    ta.style.height = "auto";
    ta.style.height = Math.min(Math.max(ta.scrollHeight, 120), 520) + "px";
  }

  function makeEditor(value) {
    var ed = document.createElement("textarea");
    ed.className = "ho-editor";
    ed.spellcheck = false;
    ed.setAttribute("autocomplete", "off");
    ed.setAttribute("autocapitalize", "off");
    ed.value = value;
    ed.addEventListener("input", function () { autoSize(ed); });
    ed.addEventListener("keydown", function (e) {
      if (e.key === "Tab") {
        e.preventDefault();
        var s = ed.selectionStart, en = ed.selectionEnd;
        ed.value = ed.value.slice(0, s) + "    " + ed.value.slice(en);
        ed.selectionStart = ed.selectionEnd = s + 4;
      }
    });
    return ed;
  }

  function mkBtn(label, cls) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = cls;
    b.textContent = label;
    return b;
  }

  // ── Practice block → permanent editable editor ──────────────────────────────
  function enhancePractice(practice) {
    if (practice.dataset.hoReady) return;
    var pre = practice.querySelector("pre");
    if (!pre) return;
    var codeEl = pre.querySelector("code") || pre;
    var starter = codeEl.textContent.replace(/\s+$/, "");
    practice.dataset.hoReady = "1";

    // Optional auto-grading: a hidden <template class="ho-check"> holds
    // assertions that run after the learner's code (adds a "Check" button).
    var checkTpl = practice.querySelector("template.ho-check");
    var checkSrc = checkTpl ? checkTpl.content.textContent : null;

    // Replace the whole starter wrapper (.code-block/.ch or .code-wrap/.copy-btn)
    // so the now-dead Copy button isn't left orphaned.
    var container = pre.closest(".code-block, .code-wrap") || pre;

    var wrap = document.createElement("div");
    wrap.className = "ho";
    var editor = makeEditor(starter);
    var bar = document.createElement("div");
    bar.className = "ho-bar";
    var runBtn = mkBtn("▶ Run", "ho-btn ho-run");
    var resetBtn = mkBtn("Reset", "ho-btn");
    var copyBtn = mkBtn("Copy", "ho-btn");
    var status = document.createElement("span");
    status.className = "ho-status";
    var out = document.createElement("pre");
    out.className = "ho-out";

    runBtn.addEventListener("click", function () {
      runCode(function () { return editor.value; }, out, status, runBtn);
    });
    resetBtn.addEventListener("click", function () {
      editor.value = starter;
      autoSize(editor);
      out.classList.remove("show");
      status.textContent = "";
    });
    copyBtn.addEventListener("click", function () {
      copyToClipboard(editor.value, copyBtn);
    });

    bar.appendChild(runBtn);
    if (checkSrc) {
      var checkBtn = mkBtn("✓ Check", "ho-btn");
      checkBtn.addEventListener("click", function () {
        runCheck(editor.value, checkSrc, out, status, checkBtn);
      });
      bar.appendChild(checkBtn);
    }
    bar.appendChild(resetBtn);
    bar.appendChild(copyBtn);
    bar.appendChild(status);
    wrap.appendChild(editor);
    wrap.appendChild(bar);
    wrap.appendChild(out);
    autoSize(editor);
    container.replaceWith(wrap);
  }

  // ── Example / real-world snippet → Run + Edit toolbar under the code ─────────
  function enhanceSnippet(pre) {
    if (pre.dataset.hoReady) return;
    if (!pre.isConnected) return; // a Practice starter <pre> already detached
    if (pre.closest(".practice")) return; // handled by enhancePractice
    var codeEl = pre.querySelector("code.language-python");
    if (!codeEl) return;
    pre.dataset.hoReady = "1";

    var bar = document.createElement("div");
    bar.className = "ho-bar ho-inline";
    var runBtn = mkBtn("▶ Run", "ho-btn ho-run ho-sm");
    var editBtn = mkBtn("Edit", "ho-btn ho-sm");
    var status = document.createElement("span");
    status.className = "ho-status";
    var out = document.createElement("pre");
    out.className = "ho-out";

    var editor = null; // created on first Edit
    function getCode() {
      return editor ? editor.value : codeEl.textContent;
    }

    runBtn.addEventListener("click", function () {
      runCode(getCode, out, status, runBtn);
    });
    editBtn.addEventListener("click", function () {
      if (!editor) {
        editor = makeEditor(codeEl.textContent.replace(/\s+$/, ""));
        pre.style.display = "none";
        pre.parentNode.insertBefore(editor, pre.nextSibling);
        autoSize(editor);
        editBtn.textContent = "Hide editor";
        editor.focus();
      } else {
        var shown = editor.style.display !== "none";
        editor.style.display = shown ? "none" : "";
        pre.style.display = shown ? "" : "none";
        editBtn.textContent = shown ? "Edit" : "Hide editor";
      }
    });

    bar.appendChild(runBtn);
    bar.appendChild(editBtn);
    bar.appendChild(status);
    // insert toolbar + output right after the <pre>
    pre.parentNode.insertBefore(out, pre.nextSibling);
    pre.parentNode.insertBefore(bar, pre.nextSibling);
  }

  function copyToClipboard(text, btn) {
    if (!navigator.clipboard) return;
    navigator.clipboard.writeText(text).then(function () {
      var old = btn.textContent;
      btn.textContent = "Copied";
      setTimeout(function () { btn.textContent = old; }, 1200);
    });
  }

  function init() {
    var practice = document.querySelectorAll(".practice");
    var snippets = document.querySelectorAll("pre");
    if (!practice.length && !snippets.length) return;
    injectStyles();
    practice.forEach(enhancePractice);
    snippets.forEach(enhanceSnippet);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
