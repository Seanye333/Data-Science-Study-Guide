/* hands-on.js — turn each Practice block into an editable, runnable Python
 * window. Code runs entirely in the browser via Pyodide (CPython → WASM); the
 * runtime is lazy-loaded on the first Run so normal page loads stay light.
 * Progressive enhancement: if this script or Pyodide fails to load, the starter
 * code is still shown in the editor and can be copied. */
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
      ".ho-btn{cursor:pointer;border:1px solid rgba(255,255,255,.15);border-radius:8px;" +
      "padding:6px 14px;font-size:.82rem;font-weight:600;color:#e6edf3;" +
      "background:rgba(255,255,255,.06);transition:background .15s,border-color .15s}" +
      ".ho-btn:hover{background:rgba(255,255,255,.12)}" +
      ".ho-run{color:#0d1117;background:var(--acc,#58a6ff);border-color:transparent}" +
      ".ho-run:hover{filter:brightness(1.08);background:var(--acc,#58a6ff)}" +
      ".ho-btn[disabled]{opacity:.55;cursor:default}" +
      ".ho-status{font-size:.78rem;color:#8b949e;margin-left:auto}" +
      ".ho-out{margin:0;white-space:pre-wrap;word-break:break-word;" +
      "font:0.82rem/1.5 'SFMono-Regular',Consolas,Menlo,monospace;color:#c9d1d9;" +
      "background:rgba(13,17,23,.6);border:1px solid rgba(255,255,255,.08);border-radius:10px;" +
      "padding:11px 13px;max-height:340px;overflow:auto;display:none}" +
      ".ho-out.show{display:block}" +
      ".ho-err{color:#ff7b72}" +
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

  // ── run one editor's code, stream output into its console ───────────────────
  function runCode(code, out, status, runBtn) {
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
        py.setStdout({
          batched: function (s) {
            chunks.push(s + "\n");
            flush();
          },
        });
        py.setStderr({
          batched: function (s) {
            chunks.push(s + "\n");
            flush();
          },
        });
        return py
          .loadPackagesFromImports(code, {
            messageCallback: function () {},
            errorCallback: function () {},
          })
          .catch(function () {})
          .then(function () {
            return py.runPythonAsync(code);
          });
      })
      .then(function () {
        if (!chunks.length) {
          out.innerHTML = '<span class="ho-muted">(ran with no output)</span>';
        }
        status.textContent = "Done";
      })
      .catch(function (err) {
        var msg = (err && err.message ? err.message : String(err)).trim();
        var pre = document.createElement("span");
        pre.className = "ho-err";
        pre.textContent = (chunks.length ? "\n" : "") + msg;
        out.appendChild(pre);
        status.textContent = "Error";
      })
      .then(function () {
        runBtn.disabled = false;
      });
  }

  // ── enhance a single .practice block ───────────────────────────────────────
  function enhance(practice) {
    if (practice.dataset.hoReady) return;
    var pre = practice.querySelector("pre");
    if (!pre) return;
    var codeEl = pre.querySelector("code") || pre;
    var starter = codeEl.textContent.replace(/\s+$/, "");
    practice.dataset.hoReady = "1";

    // The starter <pre> sits in a wrapper that also holds a (now dead) Copy
    // button: .code-block/.ch in one generator template, .code-wrap/.copy-btn
    // in the other. Replace the whole wrapper so nothing is left orphaned.
    var container = pre.closest(".code-block, .code-wrap") || pre;

    var wrap = document.createElement("div");
    wrap.className = "ho";

    var editor = document.createElement("textarea");
    editor.className = "ho-editor";
    editor.spellcheck = false;
    editor.setAttribute("autocomplete", "off");
    editor.setAttribute("autocapitalize", "off");
    editor.value = starter;
    autoSize(editor);
    editor.addEventListener("input", function () {
      autoSize(editor);
    });
    editor.addEventListener("keydown", function (e) {
      if (e.key === "Tab") {
        e.preventDefault();
        var s = editor.selectionStart,
          en = editor.selectionEnd;
        editor.value =
          editor.value.slice(0, s) + "    " + editor.value.slice(en);
        editor.selectionStart = editor.selectionEnd = s + 4;
      }
    });

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
      runCode(editor.value, out, status, runBtn);
    });
    resetBtn.addEventListener("click", function () {
      editor.value = starter;
      autoSize(editor);
      out.classList.remove("show");
      status.textContent = "";
    });
    copyBtn.addEventListener("click", function () {
      navigator.clipboard &&
        navigator.clipboard.writeText(editor.value).then(function () {
          copyBtn.textContent = "Copied";
          setTimeout(function () {
            copyBtn.textContent = "Copy";
          }, 1200);
        });
    });

    bar.appendChild(runBtn);
    bar.appendChild(resetBtn);
    bar.appendChild(copyBtn);
    bar.appendChild(status);
    wrap.appendChild(editor);
    wrap.appendChild(bar);
    wrap.appendChild(out);

    container.replaceWith(wrap);
  }

  function autoSize(ta) {
    ta.style.height = "auto";
    ta.style.height = Math.min(Math.max(ta.scrollHeight, 120), 520) + "px";
  }

  function mkBtn(label, cls) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = cls;
    b.textContent = label;
    return b;
  }

  function init() {
    var blocks = document.querySelectorAll(".practice");
    if (!blocks.length) return;
    injectStyles();
    blocks.forEach(enhance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
