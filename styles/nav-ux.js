/* ============================================================
   Data Science Study Path — Navigation & UX enhancements
   Works on both Pattern A (.topic/.th/.tb) and
   Pattern C (.card/.card-header/.card-body) module pages
   ============================================================ */

(function () {
  'use strict';

  /* ── Helpers ─────────────────────────────────────────────── */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.from((ctx || document).querySelectorAll(sel)); }

  // Get all topic sections in order
  function getTopics() {
    var topics = $$('.topic[id], .card[id^="s"]');
    // filter to only section IDs like s0, s1 …
    return topics.filter(function (el) { return /^s\d+$/.test(el.id); });
  }

  // Get topic title text
  function getTopicTitle(topic) {
    var el = $('.th span:first-child', topic) ||
             $('.card-header span:first-child', topic) ||
             $('.th', topic) ||
             $('.card-header', topic);
    return el ? el.textContent.trim() : '';
  }

  // Get topic body element
  function getTopicBody(topic) {
    return $('.tb', topic) || $('.card-body', topic);
  }

  // Check if topic is expanded
  function isExpanded(topic) {
    var body = getTopicBody(topic);
    if (!body) return false;
    return body.style.display !== 'none' && !body.classList.contains('collapsed');
  }

  // Expand a topic
  function expandTopic(topic) {
    var th = $('.th', topic) || $('.card-header', topic);
    var body = getTopicBody(topic);
    if (!body) return;
    if (!isExpanded(topic)) {
      body.style.display = '';
      body.removeAttribute('hidden');
      if (th) th.classList.add('active');
    }
  }

  // Get module name
  function getModuleName() {
    var h = $('.pt') || $('header h1') || $('h1.pg-title');
    if (h) return h.textContent.replace(/\s+/g, ' ').trim().replace(/^[^\w]+/, '');
    return document.title.replace(' Study Guide', '').trim();
  }

  /* ── 1. BACK-TO-TOP BUTTON ───────────────────────────────── */
  var btt = document.createElement('button');
  btt.id = 'back-to-top';
  btt.innerHTML = '↑';
  btt.title = 'Back to top';
  btt.setAttribute('aria-label', 'Back to top');
  document.body.appendChild(btt);

  var scrollEl = $('main.main') || $('main') || $('div#main') || window;

  function getScrollTop() {
    if (scrollEl === window) return document.documentElement.scrollTop;
    return scrollEl.scrollTop;
  }

  function onScroll() {
    btt.classList.toggle('visible', getScrollTop() > 400);
    updateBreadcrumbFromScroll();
  }

  if (scrollEl === window) {
    window.addEventListener('scroll', onScroll, { passive: true });
  } else {
    scrollEl.addEventListener('scroll', onScroll, { passive: true });
  }

  btt.addEventListener('click', function () {
    if (scrollEl === window) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      scrollEl.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });

  /* ── 2. BREADCRUMB ───────────────────────────────────────── */
  var breadcrumb = document.createElement('div');
  breadcrumb.id = 'breadcrumb';
  breadcrumb.innerHTML =
    '<a href="../../index.html">🏠 Home</a>' +
    '<span class="bc-sep">›</span>' +
    '<span class="bc-module">' + getModuleName() + '</span>' +
    '<span class="bc-sep">›</span>' +
    '<span class="bc-topic" id="bc-topic">—</span>';

  // Insert into main content area before first topic
  var mainArea = $('main.main') || $('main') || $('#main');
  if (mainArea) {
    var firstChild = mainArea.firstElementChild;
    // Insert after h1 / header if present
    var insertAfter = $('h1', mainArea) || $('header', mainArea) || firstChild;
    if (insertAfter && insertAfter.nextSibling) {
      mainArea.insertBefore(breadcrumb, insertAfter.nextSibling);
    } else {
      mainArea.insertBefore(breadcrumb, firstChild);
    }
  }

  // Update breadcrumb current topic based on scroll
  var bcTopic = document.getElementById('bc-topic');
  var topicEls = [];

  function buildTopicList() {
    topicEls = getTopics();
  }

  function updateBreadcrumbFromScroll() {
    if (!topicEls.length || !bcTopic) return;
    var scrollTop = getScrollTop();
    var mainTop   = mainArea ? mainArea.getBoundingClientRect().top + window.scrollY : 0;

    var active = topicEls[0];
    for (var i = 0; i < topicEls.length; i++) {
      var offsetTop = topicEls[i].offsetTop + (mainArea && mainArea !== window ? 0 : 0);
      if (offsetTop - 120 <= scrollTop) active = topicEls[i];
      else break;
    }
    if (active) bcTopic.textContent = getTopicTitle(active) || '—';
  }

  /* ── 3. READING TIME ESTIMATES ───────────────────────────── */
  function estimateReadTime(topic) {
    var body = getTopicBody(topic);
    if (!body) return null;

    // Count prose words (non-code)
    var clone = body.cloneNode(true);
    $$('pre, code', clone).forEach(function (el) { el.remove(); });
    var proseWords = (clone.textContent || '').trim().split(/\s+/).filter(Boolean).length;

    // Count code lines
    var codeLines = 0;
    $$('pre code', body).forEach(function (el) {
      codeLines += (el.textContent || '').split('\n').length;
    });

    var mins = Math.ceil(proseWords / 200 + codeLines / 40);
    return Math.max(1, mins);
  }

  function addReadingTimes() {
    getTopics().forEach(function (topic) {
      var header = $('.th', topic) || $('.card-header', topic);
      if (!header || header.querySelector('.read-time')) return;

      var mins = estimateReadTime(topic);
      if (!mins) return;

      var badge = document.createElement('span');
      badge.className = 'read-time';
      badge.textContent = '~' + mins + ' min';
      badge.title = 'Estimated reading time';
      header.appendChild(badge);
    });
  }

  /* ── 4. KEYBOARD SHORTCUTS ───────────────────────────────── */
  var currentTopicIndex = 0;

  function getCurrentIndex() {
    // Find which topic is most visible
    var topics = getTopics();
    var scrollTop = getScrollTop();
    var best = 0;
    for (var i = 0; i < topics.length; i++) {
      if (topics[i].offsetTop - 160 <= scrollTop) best = i;
      else break;
    }
    return best;
  }

  function navigateToTopic(index) {
    var topics = getTopics();
    if (index < 0 || index >= topics.length) return;
    var topic = topics[index];
    expandTopic(topic);

    // Scroll topic into view
    var scrollTarget = topic.offsetTop - 80;
    if (scrollEl === window) {
      window.scrollTo({ top: scrollTarget, behavior: 'smooth' });
    } else {
      scrollEl.scrollTo({ top: scrollTarget, behavior: 'smooth' });
    }

    // Highlight nav link
    var navLink = $('a[href="#' + topic.id + '"]');
    if (navLink) {
      $$('.nav-list a, nav a[href^="#s"]').forEach(function (a) {
        a.classList.remove('active');
      });
      navLink.classList.add('active');
    }

    currentTopicIndex = index;
    if (bcTopic) bcTopic.textContent = getTopicTitle(topic) || '—';

    // Flash the shortcut hint
    showShortcutToast(index === 0 ? 'First topic' : (index === getTopics().length - 1 ? 'Last topic' : null));
  }

  function showShortcutToast(msg) {
    if (!msg) return;
    var toast = document.getElementById('shortcut-toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.classList.remove('show'); }, 1800);
  }

  // Show keyboard shortcut help overlay
  function showShortcutHelp() {
    var overlay = document.getElementById('shortcut-help');
    if (overlay) {
      overlay.classList.toggle('show');
    }
  }

  document.addEventListener('keydown', function (e) {
    // Ignore when typing in an input
    var tag = document.activeElement ? document.activeElement.tagName : '';
    var isInput = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT';

    // Escape: blur search or close overlay
    if (e.key === 'Escape') {
      if (isInput) document.activeElement.blur();
      var overlay = document.getElementById('shortcut-help');
      if (overlay) overlay.classList.remove('show');
      return;
    }

    // ? — show shortcut help
    if (e.key === '?' && !isInput) {
      e.preventDefault();
      showShortcutHelp();
      return;
    }

    // / or K — focus search box
    if ((e.key === '/' || (e.key === 'k' && (e.metaKey || e.ctrlKey))) && !isInput) {
      e.preventDefault();
      var search = document.getElementById('q') ||
                   document.getElementById('search') ||
                   document.getElementById('search-box');
      if (search) { search.focus(); search.select(); }
      return;
    }

    if (isInput) return;

    // → or ] — next topic
    if (e.key === 'ArrowRight' || e.key === ']') {
      e.preventDefault();
      navigateToTopic(getCurrentIndex() + 1);
      return;
    }

    // ← or [ — previous topic
    if (e.key === 'ArrowLeft' || e.key === '[') {
      e.preventDefault();
      navigateToTopic(getCurrentIndex() - 1);
      return;
    }
  });

  /* ── Shortcut help overlay ───────────────────────────────── */
  var helpOverlay = document.createElement('div');
  helpOverlay.id = 'shortcut-help';
  helpOverlay.innerHTML =
    '<div class="sh-card">' +
      '<div class="sh-title">⌨️ Keyboard Shortcuts</div>' +
      '<div class="sh-grid">' +
        '<kbd>/</kbd><span>Focus search</span>' +
        '<kbd>→</kbd><span>Next topic</span>' +
        '<kbd>←</kbd><span>Previous topic</span>' +
        '<kbd>?</kbd><span>Show this panel</span>' +
        '<kbd>Esc</kbd><span>Close / unfocus</span>' +
      '</div>' +
      '<button class="sh-close">Got it</button>' +
    '</div>';
  document.body.appendChild(helpOverlay);
  helpOverlay.querySelector('.sh-close').addEventListener('click', function () {
    helpOverlay.classList.remove('show');
  });
  helpOverlay.addEventListener('click', function (e) {
    if (e.target === helpOverlay) helpOverlay.classList.remove('show');
  });

  /* ── Shortcut toast (edge navigation message) ───────────── */
  var toast = document.createElement('div');
  toast.id = 'shortcut-toast';
  document.body.appendChild(toast);

  /* ── Shortcut hint button (bottom of page) ───────────────── */
  var hintBtn = document.createElement('button');
  hintBtn.id = 'shortcut-hint-btn';
  hintBtn.innerHTML = '⌨️';
  hintBtn.title = 'Keyboard shortcuts (?)';
  hintBtn.addEventListener('click', showShortcutHelp);
  document.body.appendChild(hintBtn);

  /* ── Init ────────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    buildTopicList();
    addReadingTimes();
    updateBreadcrumbFromScroll();
  });

  // Also run after a short delay to catch dynamically rendered content
  setTimeout(function () {
    buildTopicList();
    addReadingTimes();
    updateBreadcrumbFromScroll();
  }, 300);

})();
