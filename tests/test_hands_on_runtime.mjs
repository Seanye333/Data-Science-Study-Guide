// Runtime test for styles/hands-on.js — drives the Run / Check / error paths on
// a real generated page with a *mocked* Pyodide (seeded into window.__hoPyodide
// so ensurePyodide short-circuits and no CDN/WASM is needed). This guards the
// button wiring, stdout rendering, pass/fail reporting, and error handling that
// the DOM-contract test (test_hands_on.mjs) doesn't exercise.
//
// Run: npm test   (needs jsdom; see package.json)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SCRIPT = fs.readFileSync(path.join(ROOT, "styles/hands-on.js"), "utf8");
const PAGE = path.join(ROOT, "modules/00_python_basics/index.html");

const dom = new JSDOM(fs.readFileSync(PAGE, "utf8"), {
  runScripts: "outside-only",
  pretendToBeVisual: true,
});
const { window } = dom;
const doc = window.document;

// --- mocked Pyodide: records the executed code and emits canned stdout ---
let lastCode = null;
let failNext = false;
let stdoutCb = null;
window.__hoPyodide = {
  setStdout(o) { stdoutCb = o.batched; },
  setStderr() {},
  async loadPackagesFromImports() {},
  async runPythonAsync(code) {
    if (code.includes("__ho_figs")) return { toJs: () => [], destroy() {} };
    lastCode = code;
    if (failNext) {
      failNext = false;
      throw new Error("Traceback (most recent call last):\nValueError: boom");
    }
    if (stdoutCb) stdoutCb("hello from fake pyodide");
    return undefined;
  },
};

window.eval(SCRIPT);
doc.dispatchEvent(new window.Event("DOMContentLoaded"));

const practice = [...doc.querySelectorAll(".practice")].find(
  (p) =>
    p.querySelector(".ho-editor") &&
    [...p.querySelectorAll(".ho-btn")].some((b) => /Check/.test(b.textContent))
);
if (!practice) {
  console.error("✗ no auto-graded practice block found to drive");
  process.exit(1);
}
const runBtn = practice.querySelector(".ho-run");
const checkBtn = [...practice.querySelectorAll(".ho-btn")].find((b) => /Check/.test(b.textContent));
const out = practice.querySelector(".ho-out");
const status = practice.querySelector(".ho-status");

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
let failures = 0;
const check = (cond, msg) => { if (!cond) { console.error(`   ✗ ${msg}`); failures++; } };

(async () => {
  // Run → stdout rendered, status Done, panel shown
  runBtn.click();
  await wait(60);
  check(out.textContent.includes("hello from fake pyodide"), "Run renders stdout into the console");
  check(status.textContent === "Done", "status becomes Done after a clean run");
  check(out.classList.contains("show"), "output panel is shown");

  // Check → appends assertions, reports pass
  checkBtn.click();
  await wait(60);
  check(/All checks passed/.test(out.textContent), "Check reports pass on a clean run");
  check(status.textContent === "Passed", "status becomes Passed");
  check(lastCode && lastCode.includes("# --- checks ---"), "Check runs the user code plus the hidden assertions");

  // Error path → red error + status Error
  failNext = true;
  runBtn.click();
  await wait(60);
  check(!!out.querySelector(".ho-err"), "an exception renders in red (.ho-err)");
  check(/ValueError: boom/.test(out.textContent), "the traceback message is shown");
  check(status.textContent === "Error", "status becomes Error on an exception");

  if (failures) {
    console.error(`\n❌ ${failures} runtime assertion(s) failed`);
    process.exit(1);
  }
  console.log("✅ hands-on.js runtime wiring holds (Run, Check, error paths)");
})();
