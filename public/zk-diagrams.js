// Diagrams (D2, rendered to SVG images at build time): each gets a frame and a "full screen" button.
// The full-screen view zooms with the wheel / +/- and moves by dragging.
(function () {
  function makeViewer(img) {
    var ov = document.createElement('div');
    ov.className = 'zk-viewer';
    ov.innerHTML = '<div class="zk-viewer-bar"><span>Колесо мыши — масштаб · перетаскивание — сдвиг · Esc — закрыть</span>' +
      '<div><button type="button" data-z="-1">−</button><button type="button" data-z="0">100%</button><button type="button" data-z="1">+</button>' +
      '<button type="button" data-close>Закрыть ✕</button></div></div><div class="zk-viewer-stage"><div class="zk-viewer-canvas"></div></div>';
    var canvas = ov.querySelector('.zk-viewer-canvas'), stage = ov.querySelector('.zk-viewer-stage');
    var w = +img.getAttribute('width') || img.naturalWidth, h = +img.getAttribute('height') || img.naturalHeight;
    var copy = new Image(); copy.src = img.currentSrc || img.src; copy.alt = img.alt; copy.width = w; copy.height = h; copy.draggable = false;
    canvas.appendChild(copy);
    document.body.appendChild(ov);
    document.documentElement.style.overflow = 'hidden';
    var s = Math.min((stage.clientWidth - 48) / w, (stage.clientHeight - 48) / h, 2), x = 0, y = 0;
    function fit() { x = (stage.clientWidth - w * s) / 2; y = Math.max(24, (stage.clientHeight - h * s) / 2); draw(); }
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
    document.querySelectorAll('.sl-markdown-content img[src*="/d2/"], .sl-markdown-content img[src*="/diagrams/"]').forEach(function (img) {
      if (img.closest('.zk-diagram')) return;
      var box = document.createElement('figure');
      box.className = 'zk-diagram';
      img.parentNode.insertBefore(box, img);
      var scroll = document.createElement('div'); scroll.className = 'zk-diagram-scroll';
      scroll.appendChild(img); box.appendChild(scroll);
      if (img.alt && img.alt !== 'Diagram') { var cap = document.createElement('figcaption'); cap.textContent = img.alt; box.appendChild(cap); }
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'zk-full'; b.textContent = '⤢ Во весь экран';
      b.addEventListener('click', function () { makeViewer(img); });
      box.appendChild(b);
      img.addEventListener('click', function () { makeViewer(img); });
    });
  }
  document.addEventListener('DOMContentLoaded', decorate);
  if (document.readyState !== 'loading') decorate();
})();
