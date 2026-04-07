/* ============================================================
   Data Science Study Path — Shared Visual Effects
   Loaded by every page: loading screen, theme toggle,
   page transitions, confetti
   ============================================================ */

(function () {
  /* ── 1. LOADING SCREEN ───────────────────────────────────── */
  var loader = document.getElementById('page-loader');
  if (loader) {
    window.addEventListener('load', function () {
      setTimeout(function () { loader.classList.add('hidden'); }, 600);
    });
  }

  /* ── 2. THEME TOGGLE ─────────────────────────────────────── */
  var THEME_KEY = 'ds_theme';
  var btn = document.getElementById('theme-toggle');

  function applyTheme(mode) {
    if (mode === 'light') {
      document.body.classList.add('light-mode');
      if (btn) btn.textContent = '☀️';
    } else {
      document.body.classList.remove('light-mode');
      if (btn) btn.textContent = '🌙';
    }
  }

  // Apply saved theme immediately (before paint)
  var saved = localStorage.getItem(THEME_KEY) || 'dark';
  applyTheme(saved);

  if (btn) {
    btn.addEventListener('click', function () {
      var next = document.body.classList.contains('light-mode') ? 'dark' : 'light';
      localStorage.setItem(THEME_KEY, next);
      applyTheme(next);
    });
  }

  /* ── 3. PAGE TRANSITIONS ─────────────────────────────────── */
  document.addEventListener('click', function (e) {
    var anchor = e.target.closest('a[href]');
    if (!anchor) return;

    var href = anchor.getAttribute('href');
    // Only internal relative links, not anchors (#), not external
    if (!href || href.startsWith('#') || href.startsWith('http') ||
        href.startsWith('mailto') || anchor.target === '_blank') return;

    e.preventDefault();
    document.body.classList.add('page-transitioning');

    setTimeout(function () {
      window.location.href = href;
    }, 250);
  });

  /* ── 4. CONFETTI + COMPLETION MODAL ─────────────────────── */
  window.triggerConfetti = function () {
    var canvas = document.getElementById('confetti-canvas');
    var modal  = document.getElementById('complete-modal');
    if (!canvas) return;

    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    var ctx = canvas.getContext('2d');

    var colors = ['#58a6ff','#c084fc','#f97316','#3fb950','#f78166','#ffa657','#4ec9a0'];
    var pieces = [];

    for (var i = 0; i < 160; i++) {
      pieces.push({
        x:    Math.random() * canvas.width,
        y:    Math.random() * canvas.height - canvas.height,
        w:    Math.random() * 10 + 5,
        h:    Math.random() * 6  + 3,
        color: colors[Math.floor(Math.random() * colors.length)],
        rot:  Math.random() * 360,
        vx:   (Math.random() - 0.5) * 3,
        vy:   Math.random() * 4 + 2,
        vr:   (Math.random() - 0.5) * 6,
        alpha: 1
      });
    }

    var startTime = null;
    var duration  = 4000;

    function drawFrame(ts) {
      if (!startTime) startTime = ts;
      var elapsed = ts - startTime;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      var allGone = true;
      pieces.forEach(function (p) {
        p.x  += p.vx;
        p.y  += p.vy;
        p.rot += p.vr;
        if (elapsed > duration * 0.6) p.alpha -= 0.012;
        p.alpha = Math.max(0, p.alpha);
        if (p.alpha > 0) allGone = false;

        ctx.save();
        ctx.globalAlpha = p.alpha;
        ctx.translate(p.x + p.w / 2, p.y + p.h / 2);
        ctx.rotate(p.rot * Math.PI / 180);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
        ctx.restore();
      });

      if (!allGone && elapsed < duration + 1000) {
        requestAnimationFrame(drawFrame);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    }

    requestAnimationFrame(drawFrame);

    // Show completion modal
    if (modal) {
      modal.classList.add('show');
      var closeBtn = modal.querySelector('.complete-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', function () {
          modal.classList.remove('show');
        });
      }
      modal.addEventListener('click', function (e) {
        if (e.target === modal) modal.classList.remove('show');
      });
    }
  };

})();
