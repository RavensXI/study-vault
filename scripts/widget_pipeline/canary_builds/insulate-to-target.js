window.SVWidget = {
  meta: {
    id: 'insulate-to-target',
    title: 'Insulate the House to Hit 85% Efficiency',
    teaches: 'Increasing insulation thickness and choosing better materials reduces wasted thermal energy, raising efficiency toward (but never above) 100%, at a cost trade-off.'
  },
  mount: function (root, ctx) {
    const accent = (ctx && ctx.accent) || '#b5502f';
    const reduced = !!(ctx && ctx.reducedMotion);

    const style = document.createElement('style');
    style.textContent = `
      .iw-root { font-family: Inter, Arial, sans-serif; color: #2d2a26; background: #faf8f5;
        padding: 16px; border-radius: 14px; box-sizing: border-box; max-width: 900px; margin: 0 auto; }
      .iw-root * { box-sizing: border-box; }
      .iw-h { font-family: 'Source Serif 4', Georgia, serif; font-size: 1.3rem; margin: 0 0 4px 0; }
      .iw-sub { color: #8d8880; font-size: 0.9rem; margin: 0 0 14px 0; line-height:1.4; }
      .iw-layout { display: flex; gap: 20px; flex-wrap: wrap; align-items: flex-start; }
      .iw-controls { flex: 1 1 260px; min-width: 240px; display: flex; flex-direction: column; gap: 14px; }
      .iw-diagram-col { flex: 1 1 320px; min-width: 280px; display:flex; flex-direction:column; align-items:center; gap:10px;}
      .iw-card { background: #fff; border: 1px solid #e8e2d9; border-radius: 12px; padding: 12px; }
      .iw-label { font-weight: 600; font-size: 0.85rem; margin-bottom: 6px; display:block; }
      .iw-row { display:flex; justify-content: space-between; align-items:center; margin-bottom:4px;}
      .iw-val { font-variant-numeric: tabular-nums; color:#555; font-size:0.85rem; }
      input[type=range] { width: 100%; accent-color: ${accent}; }
      .iw-btngroup { display:flex; gap:6px; flex-wrap:wrap; }
      .iw-btn { flex:1 1 auto; padding: 8px 6px; border-radius: 10px; border: 1px solid #e8e2d9;
        background:#fff; cursor:pointer; font-size: 0.78rem; color:#2d2a26; text-align:center; line-height:1.2; }
      .iw-btn[aria-pressed="true"] { background: ${accent}; color:#fff; border-color: ${accent}; font-weight:600; }
      .iw-btn:focus-visible { outline: 2px solid ${accent}; outline-offset:1px; }
      .iw-meterwrap { display:flex; gap:14px; align-items:flex-end; }
      .iw-meter { position:relative; width: 46px; height: 200px; background:#efe9df; border-radius:8px; overflow:hidden; border:1px solid #e8e2d9;}
      .iw-meterfill { position:absolute; bottom:0; left:0; width:100%; background:${accent}; transition: ${reduced ? 'none' : 'height 0.35s ease, background 0.35s ease'}; }
      .iw-target-line { position:absolute; left:-4px; right:-4px; height:2px; background:#2d2a26; }
      .iw-target-label { position:absolute; left:52px; font-size:0.7rem; color:#2d2a26; white-space:nowrap; transform: translateY(-50%); }
      .iw-metertext { text-align:center; font-size:0.85rem; margin-top:6px; font-weight:600; }
      .iw-feedback { border-radius: 10px; padding: 10px 12px; font-size: 0.85rem; line-height:1.4; margin-top: 6px; }
      .iw-feedback.ok { background: #eef7ee; border: 1px solid #bfe3bf; color:#245c24; }
      .iw-feedback.no { background: #fbeeee; border: 1px solid #eec6c6; color:#7a2626; }
      .iw-coins { display:flex; flex-wrap:wrap; gap:3px; max-width:180px; justify-content:center; }
      .iw-coin { width:16px; height:16px; border-radius:50%; background: #d8a63f; border: 1px solid #a97e1f;
        display:flex; align-items:center; justify-content:center; font-size:9px; color:#5c4415; font-weight:700; }
      .iw-costline { font-size:0.85rem; text-align:center; }
      .iw-reset { margin-top: 4px; align-self:flex-start; background:#fff; border:1px solid #e8e2d9; border-radius:8px; padding:6px 10px; cursor:pointer; font-size:0.8rem;}
      .iw-reset:hover { border-color: ${accent}; }
      .iw-footnote { font-size: 0.75rem; color:#8d8880; margin-top:8px; line-height:1.4; }
      svg.iw-house { max-width: 100%; height: auto; }
      @media (max-width: 480px) {
        .iw-meterwrap { gap: 8px; }
        .iw-meter { width: 36px; }
      }
    `;
    root.appendChild(style);

    const wrap = document.createElement('div');
    wrap.className = 'iw-root';
    root.appendChild(wrap);

    wrap.innerHTML += `
      <h2 class="iw-h">Insulate the house — hit 85% efficiency</h2>
      <p class="iw-sub">The heater always delivers <strong>2000 W</strong> of input power — that energy is never lost, but it can be wasted as heat escaping through the loft, walls and windows. Adjust the insulation to raise efficiency to at least <strong>85%</strong>, for the lowest total cost.</p>
    `;

    const layout = document.createElement('div');
    layout.className = 'iw-layout';
    wrap.appendChild(layout);

    // ---- Controls column ----
    const controls = document.createElement('div');
    controls.className = 'iw-controls';
    layout.appendChild(controls);

    const loftCard = document.createElement('div');
    loftCard.className = 'iw-card';
    loftCard.innerHTML = `
      <span class="iw-label">Loft insulation thickness</span>
      <div class="iw-row"><span class="iw-val" id="iw-loft-val">100 mm</span></div>
      <input type="range" min="0" max="300" step="50" value="100" id="iw-loft-slider" aria-label="Loft insulation thickness in millimetres">
    `;
    controls.appendChild(loftCard);

    const wallCard = document.createElement('div');
    wallCard.className = 'iw-card';
    wallCard.innerHTML = `<span class="iw-label">Wall type</span>
      <div class="iw-btngroup" id="iw-wall-group">
        <button class="iw-btn" data-val="0" aria-pressed="true">None (bare wall)</button>
        <button class="iw-btn" data-val="1" aria-pressed="false">Cavity wall + insulation</button>
        <button class="iw-btn" data-val="2" aria-pressed="false">Solid wall, insulated</button>
      </div>`;
    controls.appendChild(wallCard);

    const glazeCard = document.createElement('div');
    glazeCard.className = 'iw-card';
    glazeCard.innerHTML = `<span class="iw-label">Glazing</span>
      <div class="iw-btngroup" id="iw-glaze-group">
        <button class="iw-btn" data-val="0" aria-pressed="true">Single glazing</button>
        <button class="iw-btn" data-val="1" aria-pressed="false">Double glazing</button>
      </div>`;
    controls.appendChild(glazeCard);

    const feedback = document.createElement('div');
    feedback.className = 'iw-feedback no';
    controls.appendChild(feedback);

    const resetBtn = document.createElement('button');
    resetBtn.className = 'iw-reset';
    resetBtn.textContent = 'Reset to defaults';
    controls.appendChild(resetBtn);

    const footnote = document.createElement('p');
    footnote.className = 'iw-footnote';
    footnote.textContent = 'Best £ cost found so far while meeting the 85% target: none yet.';
    controls.appendChild(footnote);

    // ---- Diagram column ----
    const diagCol = document.createElement('div');
    diagCol.className = 'iw-diagram-col';
    layout.appendChild(diagCol);

    const svgNS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(svgNS, 'svg');
    svg.setAttribute('viewBox', '0 0 300 230');
    svg.setAttribute('class', 'iw-house');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Cross-section of a house showing heat loss arrows from the loft, walls and window');

    svg.innerHTML = `
      <defs>
        <marker id="iw-arrowhead" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
          <path d="M0,0 L8,4 L0,8 Z" fill="#c0392b"/>
        </marker>
      </defs>
      <!-- sky -->
      <rect x="0" y="0" width="300" height="230" fill="#f5f1ea"/>
      <!-- roof -->
      <polygon id="iw-roof" points="150,20 60,90 240,90" fill="#8b5e3c" stroke="#5c3d26" stroke-width="2"/>
      <!-- loft insulation band -->
      <rect id="iw-loft-band" x="75" y="80" width="150" height="10" fill="${accent}" opacity="0.75"/>
      <!-- house body -->
      <rect x="70" y="90" width="160" height="100" fill="#efe6d8" stroke="#c9bfae" stroke-width="1"/>
      <!-- left wall insulation block -->
      <rect id="iw-wall-left" x="64" y="90" width="6" height="100" fill="#c9c2b8"/>
      <!-- right wall insulation block -->
      <rect id="iw-wall-right" x="230" y="90" width="6" height="100" fill="#c9c2b8"/>
      <!-- window -->
      <rect x="130" y="120" width="40" height="40" fill="#dcefff" stroke="#7fa8c9" stroke-width="2"/>
      <g id="iw-panes"></g>
      <!-- ground -->
      <rect x="0" y="190" width="300" height="40" fill="#e3ddce"/>
      <!-- arrows -->
      <line id="iw-arrow-roof" x1="150" y1="15" x2="150" y2="15" stroke="#c0392b" stroke-width="3" marker-end="url(#iw-arrowhead)"/>
      <line id="iw-arrow-left" x1="64" y1="140" x2="64" y2="140" stroke="#c0392b" stroke-width="3" marker-end="url(#iw-arrowhead)"/>
      <line id="iw-arrow-right" x1="236" y1="140" x2="236" y2="140" stroke="#c0392b" stroke-width="3" marker-end="url(#iw-arrowhead)"/>
      <line id="iw-arrow-window" x1="170" y1="140" x2="170" y2="140" stroke="#c0392b" stroke-width="3" marker-end="url(#iw-arrowhead)"/>
    `;
    diagCol.appendChild(svg);

    const meterWrap = document.createElement('div');
    meterWrap.className = 'iw-meterwrap';
    meterWrap.innerHTML = `
      <div>
        <div class="iw-meter" id="iw-meter">
          <div class="iw-target-line" style="bottom:85%;"></div>
          <div class="iw-target-label" style="bottom:85%;">85% target</div>
          <div class="iw-meterfill" id="iw-meterfill" style="height:0%;"></div>
        </div>
        <div class="iw-metertext" id="iw-metertext">0%</div>
      </div>
      <div>
        <div class="iw-coins" id="iw-coins"></div>
        <div class="iw-costline" id="iw-costline">£0</div>
      </div>
    `;
    diagCol.appendChild(meterWrap);

    // ---- State ----
    const params = { loftThickness: 100, wallChoice: 0, glazingChoice: 0 };
    let bestCostAtTarget = null;
    const INPUT_POWER = 2000;

    function computeDerived(p) {
      const loftLoss = 400 / (1 + p.loftThickness / 50);
      const wallLossArr = [400, 150, 50];
      const glazeLossArr = [300, 80];
      const wallLoss = wallLossArr[p.wallChoice];
      const glazeLoss = glazeLossArr[p.glazingChoice];
      const heatLossRate = loftLoss + wallLoss + glazeLoss;
      const efficiency = (INPUT_POWER - heatLossRate) / INPUT_POWER;
      const costLoft = p.loftThickness * 0.5;
      const costWallArr = [0, 400, 900];
      const costGlazeArr = [0, 600];
      const cost = costLoft + costWallArr[p.wallChoice] + costGlazeArr[p.glazingChoice];
      const hitTarget = efficiency >= 0.85;
      return { loftLoss, wallLoss, glazeLoss, heatLossRate, efficiency, cost, hitTarget };
    }

    const els = {
      loftVal: wrap.querySelector('#iw-loft-val'),
      loftSlider: wrap.querySelector('#iw-loft-slider'),
      wallGroup: wrap.querySelector('#iw-wall-group'),
      glazeGroup: wrap.querySelector('#iw-glaze-group'),
      loftBand: svg.querySelector('#iw-loft-band'),
      wallLeft: svg.querySelector('#iw-wall-left'),
      wallRight: svg.querySelector('#iw-wall-right'),
      panes: svg.querySelector('#iw-panes'),
      arrowRoof: svg.querySelector('#iw-arrow-roof'),
      arrowLeft: svg.querySelector('#iw-arrow-left'),
      arrowRight: svg.querySelector('#iw-arrow-right'),
      arrowWindow: svg.querySelector('#iw-arrow-window'),
      meterFill: wrap.querySelector('#iw-meterfill'),
      meterText: wrap.querySelector('#iw-metertext'),
      coins: wrap.querySelector('#iw-coins'),
      costLine: wrap.querySelector('#iw-costline'),
      feedback: feedback,
      footnote: footnote
    };

    function drawPanes() {
      els.panes.innerHTML = '';
      if (params.glazingChoice === 0) {
        const l = document.createElementNS(svgNS, 'line');
        l.setAttribute('x1', '150'); l.setAttribute('y1', '120');
        l.setAttribute('x2', '150'); l.setAttribute('y2', '160');
        l.setAttribute('stroke', '#7fa8c9'); l.setAttribute('stroke-width', '2');
        els.panes.appendChild(l);
      } else {
        [147, 153].forEach(x => {
          const l = document.createElementNS(svgNS, 'line');
          l.setAttribute('x1', String(x)); l.setAttribute('y1', '120');
          l.setAttribute('x2', String(x)); l.setAttribute('y2', '160');
          l.setAttribute('stroke', '#3f7aa8'); l.setAttribute('stroke-width', '2');
          els.panes.appendChild(l);
        });
      }
    }

    function setArrow(el, x, y, len, dir) {
      // dir: 'up','left','right'
      let x2 = x, y2 = y;
      if (dir === 'up') y2 = y - len;
      if (dir === 'left') x2 = x - len;
      if (dir === 'right') x2 = x + len;
      el.setAttribute('x1', x); el.setAttribute('y1', y);
      el.setAttribute('x2', x2); el.setAttribute('y2', y2);
      el.style.opacity = len < 2 ? '0.15' : '1';
    }

    function render() {
      const d = computeDerived(params);

      // loft slider display
      els.loftVal.textContent = params.loftThickness + ' mm';
      els.loftSlider.value = params.loftThickness;

      // wall/glaze buttons
      Array.from(els.wallGroup.children).forEach(btn => {
        btn.setAttribute('aria-pressed', String(Number(btn.dataset.val) === params.wallChoice));
      });
      Array.from(els.glazeGroup.children).forEach(btn => {
        btn.setAttribute('aria-pressed', String(Number(btn.dataset.val) === params.glazingChoice));
      });

      // loft band thickness (0-300mm -> 4-40 svg units), sits just above ceiling y=90
      const bandH = 4 + (params.loftThickness / 300) * 36;
      els.loftBand.setAttribute('height', bandH.toFixed(1));
      els.loftBand.setAttribute('y', (90 - bandH).toFixed(1));

      // wall thickness/colour
      const wallWidths = [6, 12, 20];
      const wallColors = ['#c9c2b8', '#a9c9d6', '#7a5a3a'];
      const ww = wallWidths[params.wallChoice];
      els.wallLeft.setAttribute('width', ww);
      els.wallLeft.setAttribute('x', 70 - ww);
      els.wallLeft.setAttribute('fill', wallColors[params.wallChoice]);
      els.wallRight.setAttribute('width', ww);
      els.wallRight.setAttribute('x', 230);
      els.wallRight.setAttribute('fill', wallColors[params.wallChoice]);

      drawPanes();

      // arrows: scale losses to lengths (max ~55 svg units)
      setArrow(els.arrowRoof, 150, 90 - bandH - 4, (d.loftLoss / 400) * 55, 'up');
      const leftX = 70 - ww;
      const rightX = 230 + ww;
      setArrow(els.arrowLeft, leftX, 140, (d.wallLoss / 400) * 45, 'left');
      setArrow(els.arrowRight, rightX, 140, (d.wallLoss / 400) * 45, 'right');
      setArrow(els.arrowWindow, 170, 140, (d.glazeLoss / 300) * 45, 'right');

      // meter
      const pct = Math.max(0, Math.min(100, d.efficiency * 100));
      els.meterFill.style.height = pct.toFixed(1) + '%';
      els.meterFill.style.background = d.hitTarget ? accent : '#c0392b';
      els.meterText.textContent = pct.toFixed(1) + '%';

      // coins / cost
      const coinCount = Math.min(20, Math.round(d.cost / 100));
      els.coins.innerHTML = '';
      for (let i = 0; i < coinCount; i++) {
        const c = document.createElement('div');
        c.className = 'iw-coin';
        c.textContent = '£';
        els.coins.appendChild(c);
      }
      els.costLine.textContent = '£' + Math.round(d.cost) + ' total spend';

      // feedback
      if (d.hitTarget) {
        if (bestCostAtTarget === null || d.cost < bestCostAtTarget) {
          bestCostAtTarget = d.cost;
        }
        els.feedback.className = 'iw-feedback ok';
        let verdict;
        if (d.cost <= 1150) verdict = 'Excellent — target met at low cost. This is close to the cheapest way to do it.';
        else if (d.cost <= 1600) verdict = 'Target met — but you may be able to reach 85% for less money. Try a cheaper combination.';
        else verdict = 'Target met, but at high cost. Some of this spending is not needed to reach 85%.';
        els.feedback.textContent = `Efficiency ${pct.toFixed(1)}% ≥ 85% target. ${verdict}`;
      } else {
        els.feedback.className = 'iw-feedback no';
        const needed = (2000 * 0.15) - d.heatLossRate + 2000 * 0.15; // just for phrasing, not shown numerically
        els.feedback.textContent = `Efficiency ${pct.toFixed(1)}% — below the 85% target. Too much energy (${Math.round(d.heatLossRate)} W) is still escaping. Try thicker loft insulation, a better wall type, or double glazing.`;
      }

      els.footnote.textContent = bestCostAtTarget === null
        ? 'Best £ cost found so far while meeting the 85% target: none yet.'
        : 'Best £ cost found so far while meeting the 85% target: £' + Math.round(bestCostAtTarget) + '.';

      root.dataset.svState = JSON.stringify({
        loftThickness: params.loftThickness,
        wallChoice: params.wallChoice,
        glazingChoice: params.glazingChoice,
        heatLossRate: Math.round(d.heatLossRate * 100) / 100,
        efficiency: Math.round(d.efficiency * 10000) / 10000,
        cost: Math.round(d.cost * 100) / 100,
        hitTarget: d.hitTarget,
        bestCostAtTarget: bestCostAtTarget === null ? null : Math.round(bestCostAtTarget * 100) / 100
      });
    }

    els.loftSlider.addEventListener('input', (e) => {
      params.loftThickness = Number(e.target.value);
      render();
    });

    Array.from(els.wallGroup.children).forEach(btn => {
      btn.addEventListener('click', () => {
        params.wallChoice = Number(btn.dataset.val);
        render();
      });
    });
    Array.from(els.glazeGroup.children).forEach(btn => {
      btn.addEventListener('click', () => {
        params.glazingChoice = Number(btn.dataset.val);
        render();
      });
    });

    resetBtn.addEventListener('click', () => {
      params.loftThickness = 100;
      params.wallChoice = 0;
      params.glazingChoice = 0;
      render();
    });

    render();
  }
};