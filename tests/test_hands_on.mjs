// Contract test for styles/hands-on.js — runs the enhancer over real generated
// module pages (one from each generator HTML template) and asserts:
//   • every Practice block becomes an editable editor with a Run button
//   • the dead Copy button / static starter <pre> are removed
//   • every other Python snippet gets an inline Run+Edit toolbar
//   • nothing inside a Practice block gets the inline toolbar
//
// Run: npm test   (needs jsdom; see package.json)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SCRIPT = fs.readFileSync(path.join(ROOT, "styles/hands-on.js"), "utf8");

const CASES = [
  ["modules/01_numpy/index.html", "BASE template"],
  ["modules/07_sklearn/index.html", "OUT template"],
];

let failures = 0;
function check(cond, msg) {
  if (!cond) {
    console.error(`   ✗ ${msg}`);
    failures++;
  }
}

for (const [rel, label] of CASES) {
  const dom = new JSDOM(fs.readFileSync(path.join(ROOT, rel), "utf8"), {
    runScripts: "outside-only",
    pretendToBeVisual: true,
  });
  const { window } = dom;
  const doc = window.document;

  const practiceCount = doc.querySelectorAll(".practice").length;
  const snippetPres = [...doc.querySelectorAll("pre")].filter(
    (p) => p.querySelector("code.language-python") && !p.closest(".practice")
  ).length;

  window.eval(SCRIPT);
  doc.dispatchEvent(new window.Event("DOMContentLoaded"));

  console.log(`\n[${label}] ${rel}`);
  check(practiceCount > 0, "page has Practice blocks");
  check(snippetPres > 0, "page has runnable snippets");
  check(
    doc.querySelectorAll(".practice .ho-editor").length === practiceCount,
    `every Practice block got an editor (${practiceCount})`
  );
  check(
    doc.querySelectorAll(".practice .ho-run").length === practiceCount,
    "every Practice editor has a Run button"
  );
  check(
    [...doc.querySelectorAll(".practice button")].filter((b) =>
      /cp\(|copyCode\(/.test(b.getAttribute("onclick") || "")
    ).length === 0,
    "dead Copy buttons removed from Practice"
  );
  check(
    doc.querySelectorAll(".practice pre code.language-python").length === 0,
    "static starter <pre> replaced in Practice"
  );
  check(
    doc.querySelectorAll(".ho-bar.ho-inline").length === snippetPres,
    `every snippet got an inline toolbar (${snippetPres})`
  );
  check(
    doc.querySelectorAll(".practice .ho-inline").length === 0,
    "no inline toolbar inside a Practice block"
  );
  if (!failures) console.log("   ✓ all assertions passed");
}

if (failures) {
  console.error(`\n❌ ${failures} assertion(s) failed`);
  process.exit(1);
}
console.log("\n✅ hands-on.js contract holds on both templates");
