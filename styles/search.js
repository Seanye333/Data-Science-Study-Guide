/* search.js — homepage search across modules and topics.
 *
 *  • Module cards are filtered live by their visible text (works offline, no
 *    data needed) — covers all modules including the hand-maintained Pandas.
 *  • Topic-level results come from search_index.json (built by generate_all.py)
 *    and link straight to the section anchor. If the index can't be fetched
 *    (e.g. opened over file://), card filtering still works.
 */
(function () {
  "use strict";

  function injectStyles() {
    if (document.getElementById("search-styles")) return;
    var css =
      ".ho-search-wrap{max-width:680px;margin:0 auto 26px;position:relative}" +
      "#ho-search{width:100%;box-sizing:border-box;padding:13px 16px;border-radius:12px;" +
      "font-size:1rem;color:inherit;background:rgba(255,255,255,.06);" +
      "border:1px solid rgba(255,255,255,.14);outline:none;transition:border-color .15s,box-shadow .15s}" +
      "#ho-search:focus{border-color:var(--acc,#58a6ff);box-shadow:0 0 0 3px rgba(88,166,255,.18)}" +
      "body.light-mode #ho-search{background:rgba(0,0,0,.04)}" +
      ".ho-sr{margin-top:8px;border-radius:12px;overflow:hidden;display:none}" +
      ".ho-sr.show{display:block;border:1px solid rgba(255,255,255,.1);background:rgba(13,17,23,.6)}" +
      "body.light-mode .ho-sr.show{background:rgba(255,255,255,.7)}" +
      ".ho-sr a{display:flex;gap:10px;padding:9px 14px;text-decoration:none;color:inherit;" +
      "border-bottom:1px solid rgba(255,255,255,.06)}" +
      ".ho-sr a:last-child{border-bottom:0}" +
      ".ho-sr a:hover{background:rgba(88,166,255,.12)}" +
      ".ho-sr .m{color:var(--acc,#58a6ff);font-weight:600;white-space:nowrap}" +
      ".ho-sr .t{color:inherit;opacity:.9;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}" +
      ".ho-sr .none{padding:11px 14px;color:#8b949e}";
    var st = document.createElement("style");
    st.id = "search-styles";
    st.textContent = css;
    document.head.appendChild(st);
  }

  function init() {
    var input = document.getElementById("ho-search");
    if (!input) return;
    injectStyles();

    var results = document.getElementById("ho-search-results");
    var cards = [].slice.call(document.querySelectorAll(".grid .card"));
    var labels = [].slice.call(document.querySelectorAll(".section-label"));
    var index = null;

    fetch("search_index.json")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) { index = data; })
      .catch(function () { index = null; });

    function filterCards(q) {
      cards.forEach(function (c) {
        c.style.display = !q || c.textContent.toLowerCase().indexOf(q) !== -1 ? "" : "none";
      });
      // hide a section label if its following grid has no visible cards
      labels.forEach(function (lab) {
        var grid = lab.nextElementSibling;
        while (grid && !grid.classList.contains("grid")) grid = grid.nextElementSibling;
        if (!grid) return;
        var anyVisible = [].some.call(grid.querySelectorAll(".card"), function (c) {
          return c.style.display !== "none";
        });
        lab.style.display = anyVisible ? "" : "none";
      });
    }

    function topicResults(q) {
      if (!results) return;
      if (!index || q.length < 2) { results.className = "ho-sr"; results.innerHTML = ""; return; }
      var hits = [];
      for (var i = 0; i < index.length && hits.length < 24; i++) {
        var mod = index[i];
        for (var j = 0; j < mod.sections.length; j++) {
          if (mod.sections[j].t.toLowerCase().indexOf(q) !== -1) {
            hits.push({ m: mod.title, t: mod.sections[j].t, url: mod.url + "#" + mod.sections[j].a });
            if (hits.length >= 24) break;
          }
        }
      }
      if (!hits.length) { results.className = "ho-sr"; results.innerHTML = ""; return; }
      results.innerHTML = hits
        .map(function (h) {
          return '<a href="' + h.url + '"><span class="m">' + esc(h.m) +
            '</span><span class="t">' + esc(h.t) + "</span></a>";
        })
        .join("");
      results.className = "ho-sr show";
    }

    function esc(s) {
      return s.replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    }

    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      filterCards(q);
      topicResults(q);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
