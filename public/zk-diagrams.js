// Every diagram gets a "full screen" button; the full-screen view zooms with the wheel / +/- and moves by dragging.
(function () {
  function makeViewer(svg) {
    var ov = document.createElement('div');
    ov.className = 'zk-viewer';
    ov.innerHTML = '<div class="zk-viewer-bar"><span>Колесо мыши — масштаб · перетаскивание — сдвиг · Esc — закрыть</span>' +
      '<div><button type="button" data-z="-1">−</button><button type="button" data-z="0">100%</button><button type="button" data-z="1">+</button>' +
      '<button type="button" data-close>Закрыть ✕</button></div></div><div class="zk-viewer-stage"><div class="zk-viewer-canvas"></div></div>';
    var canvas = ov.querySelector('.zk-viewer-canvas'), stage = ov.querySelector('.zk-viewer-stage');
    var copy = svg.cloneNode(true);
    copy.removeAttribute('style'); copy.style.maxWidth = 'none';
    var vb = (svg.getAttribute('viewBox') || '').split(/[\s,]+/).map(Number);
    var w = vb[2] || svg.getBoundingClientRect().width, h = vb[3] || svg.getBoundingClientRect().height;
    copy.setAttribute('width', w); copy.setAttribute('height', h);
    canvas.appendChild(copy);
    document.body.appendChild(ov);
    document.documentElement.style.overflow = 'hidden';
    var s = Math.min((stage.clientWidth - 40) / w, (stage.clientHeight - 40) / h, 2.5), x = 0, y = 0;
    function fit() { x = (stage.clientWidth - w * s) / 2; y = Math.max(20, (stage.clientHeight - h * s) / 2); draw(); }
    function draw() { canvas.style.transform = 'translate(' + x + 'px,' + y + 'px) scale(' + s + ')'; ov.querySelector('[data-z="0"]').textContent = Math.round(s * 100) + '%'; }
    function zoom(f, cx, cy) {
      var r = stage.getBoundingClientRect(); cx = cx == null ? r.width / 2 : cx - r.left; cy = cy == null ? r.height / 2 : cy - r.top;
      var ns = Math.max(0.2, Math.min(6, s * f)); x = cx - (cx - x) * ns / s; y = cy - (cy - y) * ns / s; s = ns; draw();
    }
    fit();
    stage.addEventListener('wheel', function (e) { e.preventDefault(); zoom(e.deltaY < 0 ? 1.15 : 1 / 1.15, e.clientX, e.clientY); }, { passive: false });
    var drag = null;
    stage.addEventListener('pointerdown', function (e) { drag = { px: e.clientX, py: e.clientY, x: x, y: y }; stage.setPointerCapture(e.pointerId); stage.classList.add('grab'); });
    stage.addEventListener('pointermove', function (e) { if (!drag) return; x = drag.x + e.clientX - drag.px; y = drag.y + e.clientY - drag.py; draw(); });
    stage.addEventListener('pointerup', function () { drag = null; stage.classList.remove('grab'); });
    ov.querySelectorAll('[data-z]').forEach(function (b) {
      b.addEventListener('click', function () { var z = +b.dataset.z; if (z === 0) { s = 1; fit(); } else zoom(z > 0 ? 1.25 : 0.8); });
    });
    function close() { ov.remove(); document.documentElement.style.overflow = ''; document.removeEventListener('keydown', key); }
    function key(e) { if (e.key === 'Escape') close(); if (e.key === '+' || e.key === '=') zoom(1.25); if (e.key === '-') zoom(0.8); }
    document.addEventListener('keydown', key);
    ov.querySelector('[data-close]').addEventListener('click', close);
  }
  function decorate() {
    document.querySelectorAll('pre.mermaid, div.mermaid').forEach(function (box) {
      var svg = box.querySelector('svg');
      if (!svg || box.querySelector(':scope > .zk-full')) return;   // mermaid may redraw the box: check for the button itself
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'zk-full'; b.innerHTML = '⤢ Во весь экран';
      b.addEventListener('click', function (e) { e.stopPropagation(); makeViewer(box.querySelector('svg')); });
      box.appendChild(b);
      if (!box.dataset.zkClick) { box.dataset.zkClick = '1'; box.addEventListener('click', function (e) { if (e.target.closest('svg')) makeViewer(box.querySelector('svg')); }); }
    });
  }
  new MutationObserver(decorate).observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener('DOMContentLoaded', decorate);
})();
