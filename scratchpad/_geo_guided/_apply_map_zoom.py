# -*- coding: utf-8 -*-
"""Replace the flat lightbox with a zoom/pan map viewer.

    python scratchpad/_geo_guided/_apply_map_zoom.py

The OS extracts are 1536x1302. On a phone the panel shows one at roughly 360px
and the old lightbox only stretched it to the viewport, so a 4x reduction of a
detailed map stayed unreadable: contour values, grid numbers and spot heights
are simply too small. The full resolution was already downloaded, just never
reachable. This adds pinch-zoom, wheel-zoom, drag-to-pan and a double-tap
toggle, so the detail that exists can actually be used.

Written as a file rather than a heredoc: the JS contains regex and escape
sequences that do not survive a shell heredoc.
"""
import io, sys

P = "practice.html"
s = io.open(P, encoding="utf-8").read()

OLD = """    function lightboxOpen(src) {
      var overlay = document.createElement('div');
      overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;cursor:zoom-out;padding:2rem;';
      overlay.onclick = function(){ document.body.removeChild(overlay); };
      var img = document.createElement('img');
      img.src = src;
      img.style.cssText = 'max-width:100%;max-height:100%;object-fit:contain;border-radius:8px;';
      overlay.appendChild(img);
      document.body.appendChild(overlay);
    }"""

NEW = r"""    /* Zoomable, pannable image viewer.
       The OS extracts are 1536px wide but a phone shows one at about 360px, and
       the old lightbox only stretched it to the viewport: still a 4x reduction
       of a map whose contour values and grid numbers are the whole point. The
       resolution was already downloaded, just unreachable. Pinch or wheel to
       zoom, drag to pan, double-tap to toggle between fit and 2x. */
    function lightboxOpen(src) {
      var overlay = document.createElement('div');
      overlay.className = 'lb-overlay';
      overlay.innerHTML =
        '<div class="lb-stage" id="lb-stage"><img class="lb-img" id="lb-img" alt="" draggable="false"></div>' +
        '<div class="lb-bar">' +
          '<button type="button" class="lb-btn" data-act="out" aria-label="Zoom out">&#8722;</button>' +
          '<span class="lb-level" id="lb-level">fit</span>' +
          '<button type="button" class="lb-btn" data-act="in" aria-label="Zoom in">+</button>' +
          '<button type="button" class="lb-btn" data-act="reset" aria-label="Reset zoom">Reset</button>' +
          '<button type="button" class="lb-btn lb-close" data-act="close" aria-label="Close">&#215;</button>' +
        '</div>' +
        '<div class="lb-hint" id="lb-hint">Pinch or scroll to zoom, drag to move</div>';
      document.body.appendChild(overlay);
      document.body.style.overflow = 'hidden';

      var stage = overlay.querySelector('#lb-stage');
      var img = overlay.querySelector('#lb-img');
      var level = overlay.querySelector('#lb-level');
      var scale = 1, tx = 0, ty = 0, minScale = 1, maxScale = 8;
      var pointers = {}, startDist = 0, startScale = 1, panning = false, sx = 0, sy = 0, moved = false;

      function apply() {
        img.style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + scale + ')';
        level.textContent = scale <= minScale * 1.02 ? 'fit' : (Math.round(scale / minScale * 10) / 10) + 'x';
      }
      function clamp() {
        // keep some of the image on screen at all times
        var r = stage.getBoundingClientRect();
        var w = img.naturalWidth * scale, h = img.naturalHeight * scale;
        var mx = Math.max(0, (w - r.width) / 2), my = Math.max(0, (h - r.height) / 2);
        tx = Math.max(-mx, Math.min(mx, tx));
        ty = Math.max(-my, Math.min(my, ty));
      }
      function fit() {
        var r = stage.getBoundingClientRect();
        if (!img.naturalWidth) return;
        minScale = Math.min(r.width / img.naturalWidth, r.height / img.naturalHeight);
        scale = minScale; tx = 0; ty = 0; apply();
      }
      function zoomTo(next, cx, cy) {
        var r = stage.getBoundingClientRect();
        var ox = (cx === undefined ? r.left + r.width / 2 : cx) - r.left - r.width / 2;
        var oy = (cy === undefined ? r.top + r.height / 2 : cy) - r.top - r.height / 2;
        var k = next / scale;
        tx = ox - (ox - tx) * k;
        ty = oy - (oy - ty) * k;
        scale = next; clamp(); apply();
      }

      img.onload = fit;
      img.src = src;
      window.addEventListener('resize', fit);

      overlay.addEventListener('wheel', function (e) {
        e.preventDefault();
        var next = Math.max(minScale, Math.min(maxScale * minScale, scale * (e.deltaY < 0 ? 1.18 : 1 / 1.18)));
        zoomTo(next, e.clientX, e.clientY);
      }, { passive: false });

      stage.addEventListener('pointerdown', function (e) {
        pointers[e.pointerId] = { x: e.clientX, y: e.clientY };
        var ids = Object.keys(pointers);
        if (ids.length === 1) { panning = true; moved = false; sx = e.clientX - tx; sy = e.clientY - ty; }
        if (ids.length === 2) {
          panning = false;
          var a = pointers[ids[0]], b = pointers[ids[1]];
          startDist = Math.hypot(a.x - b.x, a.y - b.y); startScale = scale;
        }
        try { stage.setPointerCapture(e.pointerId); } catch (err) {}
      });
      stage.addEventListener('pointermove', function (e) {
        if (!pointers[e.pointerId]) return;
        pointers[e.pointerId] = { x: e.clientX, y: e.clientY };
        var ids = Object.keys(pointers);
        if (ids.length === 2 && startDist) {
          var a = pointers[ids[0]], b = pointers[ids[1]];
          var d = Math.hypot(a.x - b.x, a.y - b.y);
          zoomTo(Math.max(minScale, Math.min(maxScale * minScale, startScale * (d / startDist))),
                 (a.x + b.x) / 2, (a.y + b.y) / 2);
          moved = true;
        } else if (panning) {
          tx = e.clientX - sx; ty = e.clientY - sy; moved = true; clamp(); apply();
        }
      });
      function release(e) {
        delete pointers[e.pointerId];
        if (Object.keys(pointers).length < 2) startDist = 0;
        if (!Object.keys(pointers).length) panning = false;
      }
      stage.addEventListener('pointerup', release);
      stage.addEventListener('pointercancel', release);

      stage.addEventListener('dblclick', function (e) {
        zoomTo(scale > minScale * 1.05 ? minScale : minScale * 2.5, e.clientX, e.clientY);
      });

      function close() {
        window.removeEventListener('resize', fit);
        document.body.style.overflow = '';
        if (overlay.parentNode) document.body.removeChild(overlay);
        document.removeEventListener('keydown', onKey);
      }
      function onKey(e) {
        if (e.key === 'Escape') close();
        if (e.key === '+' || e.key === '=') zoomTo(Math.min(maxScale * minScale, scale * 1.25));
        if (e.key === '-') zoomTo(Math.max(minScale, scale / 1.25));
        if (e.key === '0') fit();
      }
      document.addEventListener('keydown', onKey);

      overlay.querySelector('.lb-bar').addEventListener('click', function (e) {
        var b = e.target.closest('.lb-btn'); if (!b) return;
        e.stopPropagation();
        var act = b.getAttribute('data-act');
        if (act === 'in') zoomTo(Math.min(maxScale * minScale, scale * 1.3));
        else if (act === 'out') zoomTo(Math.max(minScale, scale / 1.3));
        else if (act === 'reset') fit();
        else close();
      });
      // a click on the backdrop closes, but not the drag that ended there
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay || (e.target === stage && !moved)) close();
      });
      setTimeout(function () {
        var h = overlay.querySelector('#lb-hint'); if (h) h.style.opacity = '0';
      }, 2600);
    }"""

if OLD not in s:
    sys.exit("lightboxOpen not found in its expected form")
s = s.replace(OLD, NEW, 1)

CSS_ANCHOR = "    /* ===== POP-OUT CALCULATOR ===== */"
CSS = """    /* ===== ZOOMABLE IMAGE VIEWER ===== */
    .lb-overlay {
      position: fixed; inset: 0; z-index: 9999;
      background: rgba(0,0,0,0.9);
      display: flex; align-items: center; justify-content: center;
    }
    .lb-stage {
      position: absolute; inset: 0;
      overflow: hidden;
      touch-action: none;               /* we own pinch and drag */
      cursor: grab;
      display: flex; align-items: center; justify-content: center;
    }
    .lb-stage:active { cursor: grabbing; }
    .lb-img {
      transform-origin: center center;
      will-change: transform;
      max-width: none; max-height: none;   /* scale is ours, not the browser's */
      user-select: none; -webkit-user-drag: none;
    }
    .lb-bar {
      position: absolute; bottom: max(1rem, env(safe-area-inset-bottom));
      left: 50%; transform: translateX(-50%);
      display: flex; align-items: center; gap: 0.3rem;
      padding: 0.35rem 0.45rem;
      background: rgba(28,26,24,0.92);
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 999px;
      box-shadow: 0 6px 22px rgba(0,0,0,0.4);
    }
    .lb-btn {
      min-width: 34px; height: 34px; padding: 0 0.6rem;
      border: none; border-radius: 999px;
      background: transparent; color: #f0ece4;
      font-family: inherit; font-size: 0.9rem; font-weight: 600;
      cursor: pointer; display: flex; align-items: center; justify-content: center;
    }
    .lb-btn:hover { background: rgba(255,255,255,0.14); }
    .lb-close { font-size: 1.15rem; }
    .lb-level {
      min-width: 2.6rem; text-align: center;
      color: #cfc7bb; font-size: 0.72rem; font-weight: 700;
      letter-spacing: 0.04em; text-transform: uppercase;
    }
    .lb-hint {
      position: absolute; top: max(1rem, env(safe-area-inset-top)); left: 50%;
      transform: translateX(-50%);
      padding: 0.4rem 0.8rem; border-radius: 999px;
      background: rgba(28,26,24,0.85); color: #e8e4df;
      font-size: 0.74rem; pointer-events: none;
      transition: opacity 0.6s ease;
    }

"""
if CSS_ANCHOR not in s:
    sys.exit("CSS anchor not found")
s = s.replace(CSS_ANCHOR, CSS + CSS_ANCHOR, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("map zoom/pan viewer installed")
