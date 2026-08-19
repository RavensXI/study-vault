/* ============================================
   Generic host for generated lesson widgets.

   The widget supplies pure logic (initialState / apply / derive /
   regions) and a render function; the host supplies everything a
   browser needs — canvas sizing, sliders for declared controls, click
   routing through regions(), the caption, reset, keyboard access.

   Because interaction arrives ONLY as actions through apply(), any
   interaction a widget invents works here without the host knowing
   anything about it: matching, sorting, labelling, routing, dragging.
   ============================================ */
(function () {
  'use strict';

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function accOf(node) {
    var v = getComputedStyle(node).getPropertyValue('--accent').trim();
    return v || '#8a6a4f';
  }

  /* mount a widget module W into a container; returns a handle */
  window.SVWidgetHost = function (W, opts) {
    opts = opts || {};
    var height = opts.height || 320;
    var root = el('div', 'sv-widget');
    root.appendChild(el('div', 'svw-kicker', 'Interactive'));
    root.appendChild(el('h3', 'svw-title', (W.meta && W.meta.title) || 'Interactive'));

    var controlsEl = el('div', 'svw-controls');
    var wrap = el('div', 'svw-canvaswrap');
    var canvas = document.createElement('canvas');
    canvas.style.cursor = 'pointer';
    canvas.setAttribute('tabindex', '0');
    wrap.appendChild(canvas);
    var captionEl = el('div', 'svw-caption');
    root.appendChild(controlsEl);
    root.appendChild(wrap);
    root.appendChild(captionEl);

    var state = W.initialState();

    function dispatch(action) {
      if (!action) return;
      try {
        state = W.apply(state, action);
      } catch (e) {
        if (window.console) console.warn('widget apply failed', e);
        return;
      }
      draw();
    }

    /* declared controls become real sliders / toggles */
    (W.controls || []).forEach(function (c) {
      var f = el('div', 'svw-field');
      f.appendChild(el('label', null, c.label + (c.unit ? ' (' + c.unit + ')' : '')));
      var input = document.createElement('input');
      if (c.type === 'toggle') {
        input.type = 'checkbox';
        input.checked = !!c.value;
        input.addEventListener('change', function () {
          dispatch({ t: 'set', key: c.key, v: input.checked });
        });
      } else {
        input.type = 'range';
        input.min = c.min; input.max = c.max;
        input.step = c.step || 1; input.value = c.value;
        input.addEventListener('input', function () {
          dispatch({ t: 'set', key: c.key, v: parseFloat(input.value) });
        });
      }
      f.appendChild(input);
      if (c.min !== undefined) {
        f.appendChild(el('div', 'svw-ends',
          '<span>' + c.min + '</span><span>' + c.max + '</span>'));
      }
      controlsEl.appendChild(f);
    });

    var resetField = el('div', 'svw-field svw-field--fixed');
    resetField.appendChild(el('label', null, '&nbsp;'));
    var resetBtn = el('button', 'svw-btn', 'Start again');
    resetBtn.addEventListener('click', function () {
      state = W.initialState(); draw();
    });
    resetField.appendChild(resetBtn);
    controlsEl.appendChild(resetField);

    /* clicks route through the widget's own hit regions */
    function pointAction(ev) {
      var r = canvas.getBoundingClientRect();
      var x = ev.clientX - r.left, y = ev.clientY - r.top;
      var regions = [];
      try { regions = W.regions(state, r.width, height) || []; } catch (e) { return null; }
      for (var i = regions.length - 1; i >= 0; i--) {
        var g = regions[i];
        if (x >= g.x && x <= g.x + g.w && y >= g.y && y <= g.y + g.h) return g.action;
      }
      return null;
    }
    canvas.addEventListener('click', function (ev) { dispatch(pointAction(ev)); });
    /* keyboard: cycle the available regions and activate — canvas alone
       is unreachable without this */
    var kbIndex = -1;
    canvas.addEventListener('keydown', function (ev) {
      var regions = [];
      try { regions = W.regions(state, canvas.clientWidth, height) || []; } catch (e) { return; }
      if (!regions.length) return;
      if (ev.key === 'Tab' || ev.key === 'ArrowRight' || ev.key === 'ArrowDown') {
        kbIndex = (kbIndex + 1) % regions.length; ev.preventDefault(); draw();
      } else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowUp') {
        kbIndex = (kbIndex - 1 + regions.length) % regions.length; ev.preventDefault(); draw();
      } else if (ev.key === 'Enter' || ev.key === ' ') {
        if (kbIndex >= 0) { dispatch(regions[kbIndex].action); ev.preventDefault(); }
      }
    });

    function draw() {
      var cssW = wrap.clientWidth - 8;
      if (cssW < 50) return;
      var dpr = window.devicePixelRatio || 1;
      canvas.width = Math.round(cssW * dpr);
      canvas.height = Math.round(height * dpr);
      canvas.style.height = height + 'px';
      var ctx = canvas.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, cssW, height);
      var d;
      try { d = W.derive(state); } catch (e) { d = {}; }
      try {
        W.render(ctx, state, d, cssW, height, accOf(root));
      } catch (e) {
        ctx.fillStyle = '#9a3a25'; ctx.font = '13px Inter, sans-serif';
        ctx.fillText('This interactive failed to draw.', 12, 24);
        if (window.console) console.warn('widget render failed', e);
      }
      try { captionEl.innerHTML = W.caption(state, d) || ''; } catch (e) { captionEl.textContent = ''; }
    }

    if (window.ResizeObserver) new ResizeObserver(draw).observe(wrap);
    setTimeout(draw, 0);
    return { el: root, draw: draw, getState: function () { return state; } };
  };
})();
