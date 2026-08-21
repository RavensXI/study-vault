/* antibodies-dont-kill — "What happens next?"
 *
 * One idea: antibodies BIND to one matching antigen and tag, clump or
 * neutralise. They never destroy. Phagocytes engulf and digest; lymphocytes
 * make the antibodies; antibiotics are drugs that damage bacteria only.
 *
 * Every verdict comes out of resolve(scene) — the outcome is derived from the
 * scene's own facts (what pathogen, which antigen shape, which antibody shape,
 * is a phagocyte there, is a drug there, are there memory cells), never
 * hand-marked on an option.
 */
(function () {
  'use strict';

  /* ---------------------------------------------------------------- palette */
  var INK = '#2d2a26';
  var MUTED = '#8d8880';
  var SOFT = '#5b564e';
  var PF = '#efe8dc';     /* pathogen fill  */
  var PS = '#b8ad99';     /* pathogen stroke */
  var AG = '#6f6a62';     /* antigen        */
  var CF = '#f5f1ea';     /* cell / phagocyte fill */
  var CS = '#cfc6b6';

  /* ------------------------------------------------------------- geometry */
  /* An antigen sits on the pathogen's lower edge, base at yb, 9 deep.
     An antibody arm tip at (x, ty) carries a socket whose rim is at ty-9.
     They lock when ty = yb + 9, i.e. antibody fork cy = yb + 20.          */

  function antigen(shape, x, yb) {
    if (shape === 'tri') {
      return '<path d="M' + (x - 5) + ' ' + yb + ' L' + x + ' ' + (yb + 9) +
             ' L' + (x + 5) + ' ' + yb + ' Z" fill="' + AG + '"/>';
    }
    if (shape === 'knob') {
      return '<circle cx="' + x + '" cy="' + (yb + 4.5) + '" r="5" fill="' + AG + '"/>';
    }
    return '<rect x="' + (x - 4.5) + '" y="' + yb + '" width="9" height="9" rx="1.5" fill="' + AG + '"/>';
  }

  function socket(shape, x, ty, col) {
    var r = ty - 9, d;
    if (shape === 'tri') d = 'M' + (x - 5.4) + ' ' + r + ' L' + x + ' ' + (ty + 1) + ' L' + (x + 5.4) + ' ' + r;
    else if (shape === 'knob') d = 'M' + (x - 6.4) + ' ' + r + ' C' + (x - 6.4) + ' ' + (ty + 7) +
      ' ' + (x + 6.4) + ' ' + (ty + 7) + ' ' + (x + 6.4) + ' ' + r;
    else d = 'M' + (x - 6.4) + ' ' + r + ' L' + (x - 6.4) + ' ' + ty + ' L' + (x + 6.4) + ' ' + ty + ' L' + (x + 6.4) + ' ' + r;
    return '<path d="' + d + '" fill="none" stroke="' + col + '" stroke-width="2.6" ' +
           'stroke-linejoin="round" stroke-linecap="round"/>';
  }

  /* Y-shaped antibody. Origin is the fork; arms point "up" in local space,
     so rotate() swings the binding sites round to face a pathogen anywhere. */
  function ab(cx, cy, shape, col, rot, op) {
    return '<g transform="translate(' + cx + ',' + cy + ')' + (rot ? ' rotate(' + rot + ')' : '') +
           '" opacity="' + (op == null ? 1 : op) + '">' +
           '<path d="M0 0 L0 13 M0 0 L-10 -11 M0 0 L10 -11" fill="none" stroke="' + col +
           '" stroke-width="3" stroke-linecap="round"/>' +
           socket(shape, -10, -11, col) + socket(shape, 10, -11, col) + '</g>';
  }

  function rod(x, y, w, h) {
    return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + (h / 2) +
           '" fill="' + PF + '" stroke="' + PS + '" stroke-width="1.5"/>';
  }
  function rodDead(x, y, w, h) {
    return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + (h / 2) +
           '" fill="#f6f3ee" stroke="' + PS + '" stroke-width="1.5" stroke-dasharray="5 4" opacity=".75"/>' +
           '<path d="M' + (x + w * 0.34) + ' ' + (y + 2) + ' L' + (x + w * 0.44) + ' ' + (y + h - 2) +
           ' M' + (x + w * 0.62) + ' ' + (y + 1) + ' L' + (x + w * 0.55) + ' ' + (y + h - 1) +
           '" stroke="' + PS + '" stroke-width="1.4" fill="none"/>';
  }
  function virus(cx, cy) {
    return '<polygon points="' + (cx - 16) + ',' + (cy - 2) + ' ' + (cx - 9) + ',' + (cy - 14) + ' ' +
           (cx + 9) + ',' + (cy - 14) + ' ' + (cx + 16) + ',' + (cy - 2) + ' ' + (cx + 12) + ',' + (cy + 11) +
           ' ' + (cx - 12) + ',' + (cy + 11) + '" fill="' + PF + '" stroke="' + PS + '" stroke-width="1.5"/>';
  }
  function phago(cx, cy, r) {
    return '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="' + CF + '" stroke="' + CS +
           '" stroke-width="1.5"/>' +
           '<ellipse cx="' + (cx + r * 0.28) + '" cy="' + (cy - r * 0.2) + '" rx="' + (r * 0.34) +
           '" ry="' + (r * 0.26) + '" fill="#e6e0d4"/>';
  }
  function lympho(cx, cy, r) {
    return '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="' + CF + '" stroke="' + CS +
           '" stroke-width="1.5"/>' +
           '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r * 0.62) + '" fill="#e6e0d4"/>';
  }
  function capsule(cx, cy) {
    return '<g><rect x="' + (cx - 17) + '" y="' + (cy - 8) + '" width="34" height="16" rx="8" fill="#f6f3ee" ' +
           'stroke="' + CS + '" stroke-width="1.5"/>' +
           '<path d="M' + cx + ' ' + (cy - 8) + ' L' + cx + ' ' + (cy + 8) + '" stroke="' + CS + '" stroke-width="1.5"/>' +
           '<rect x="' + (cx - 17) + '" y="' + (cy - 8) + '" width="17" height="16" rx="8" fill="#e8e1d5" opacity=".85"/></g>';
  }
  function cellBox(x, y, w, h) {
    return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="10" fill="' + CF +
           '" stroke="' + CS + '" stroke-width="1.5"/>' +
           '<ellipse cx="' + (x + w * 0.5) + '" cy="' + (y + h * 0.55) + '" rx="' + (w * 0.2) +
           '" ry="' + (h * 0.24) + '" fill="#e6e0d4"/>';
  }
  function T(x, y, s, col, weight) {
    return '<text x="' + x + '" y="' + y + '" text-anchor="middle" font-size="12" ' +
           'font-family="Inter,system-ui,sans-serif" font-weight="' + (weight || 400) +
           '" fill="' + (col || MUTED) + '">' + s + '</text>';
  }

  /* --------------------------------------------------------------- scenes */
  /* Every scene is drawn twice: 'before' (the situation the student predicts
     from) and 'after' (what the model says actually happened).            */

  function scenery(s, phase, A) {
    var g = '', i;
    var yb = 50;                        /* pathogen lower edge            */
    var xs = [46, 66, 86, 106];         /* antigen positions, 20 apart    */
    var bind = yb + 20;                 /* fork y for a locked antibody   */

    if (s.id === 'tagEngulf' || s.id === 'noFit') {
      if (phase === 'after' && s.outcome === 'tag') {
        /* the whole sequence in one frame: tagged on the left, eaten on the right */
        g += rod(24, 28, 92, 24) + T(70, 22, 'bacterium', SOFT, 600);
        for (i = 0; i < 4; i++) g += antigen(s.antigen, 42 + i * 20, 52);
        g += ab(52, 72, s.abShape, A, 0) + ab(92, 72, s.abShape, A, 0);
        g += T(70, 106, 'tagged by antibodies', SOFT, 600);
        g += '<path d="M132 58 L162 58 M154 52 L162 58 L154 64" fill="none" stroke="' + CS +
             '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>';
        g += phago(232, 58, 40);
        g += rodDead(214, 50, 36, 15);
        g += T(232, 112, 'engulfed and digested', SOFT, 600);
        return g;
      }
      g += rod(30, 24, 88, 26);
      for (i = 0; i < 4; i++) g += antigen(s.antigen, xs[i], yb);
      g += T(74, 18, s.P === 'the virus' ? 'virus' : 'bacterium', SOFT, 600);
      if (phase === 'after' && s.outcome === 'noBind') {
        g += ab(54, bind + 15, s.abShape, A, -14);
        g += ab(98, bind + 15, s.abShape, A, 12);
        g += '<path d="M34 ' + (yb + 11) + ' L118 ' + (yb + 11) + '" stroke="' + CS +
             '" stroke-width="1.3" stroke-dasharray="3 4"/>';
        g += T(112, 112, 'no fit — different shapes', SOFT, 600);
      } else if (phase === 'after') {
        g += ab(56, bind, s.abShape, A, 0);
        g += ab(96, bind, s.abShape, A, 0);
      } else {
        g += ab(56, 92, s.abShape, A, 0);
        g += ab(100, 96, s.abShape, A, 0);
        g += T(78, 124, 'antibodies');
      }
      if (s.phagocyte) {
        g += phago(232, 70, 34) + T(232, 122, 'phagocyte');
      } else if (s.id === 'noFit') {
        g += lympho(236, 66, 22) + T(236, 108, 'lymphocyte');
        g += T(236, 122, 'takes days');
      }
      return g;
    }

    if (s.id === 'whichFits') {
      g += rod(112, 24, 76, 26) + T(150, 18, 'bacterium', SOFT, 600);
      g += antigen(s.antigen, 130, yb) + antigen(s.antigen, 150, yb);
      var cand = s.candidates, cx, rej = 0;
      if (phase === 'after') {
        for (i = 0; i < 3; i++) {
          if (cand[i].shape === s.antigen) {
            g += ab(140, bind, cand[i].shape, A, 0) + T(174, 80, cand[i].letter, INK, 700);
          } else {
            cx = rej++ === 0 ? 44 : 252;   /* the two rejected, one each side */
            g += ab(cx, 104, cand[i].shape, A, 0, 0.32) + T(cx, 78, cand[i].letter, MUTED, 700);
          }
        }
        g += T(150, 126, 'complementary shape — only one fits', SOFT, 600);
        return g;
      }
      /* the antigen enlarged, so the shape to match is unmistakable */
      g += '<g transform="translate(44,32) scale(1.9)">' + antigen(s.antigen, 0, 0) + '</g>' +
           T(44, 68, 'its antigen');
      for (i = 0; i < 3; i++) {
        cx = 62 + i * 88;
        g += ab(cx, 110, cand[i].shape, A, 0) + T(cx, 86, cand[i].letter, INK, 700);
      }
      return g;
    }

    if (s.id === 'clump') {
      if (phase === 'after') {
        for (i = 0; i < 3; i++) g += rod(20 + i * 42, 32, 42, 22);
        for (i = 0; i < 6; i++) g += antigen(s.antigen, 30 + i * 20, 54);
        /* each antibody grips one antigen on each of two bacteria */
        g += ab(60, 74, s.abShape, A, 0) + ab(100, 74, s.abShape, A, 0);
        g += T(83, 106, 'clumped — one mouthful', SOFT, 600);
        g += phago(232, 58, 40) + T(232, 112, 'phagocyte');
        return g;
      }
      var pos = [[14, 20], [124, 24], [60, 80]];
      for (i = 0; i < 3; i++) {
        g += rod(pos[i][0], pos[i][1], 46, 20);
        g += antigen(s.antigen, pos[i][0] + 13, pos[i][1] + 20) +
             antigen(s.antigen, pos[i][0] + 33, pos[i][1] + 20);
      }
      g += ab(190, 62, s.abShape, A, 0) + ab(124, 70, s.abShape, A, 0);
      g += T(150, 120, 'antibodies');
      g += phago(250, 52, 32) + T(250, 100, 'phagocyte');
      return g;
    }

    if (s.id === 'neutralise') {
      g += cellBox(178, 62, 112, 58) + T(234, 56, 'body cell', SOFT, 600);
      if (phase === 'after') {
        g += virus(104, 52) + T(104, 26, 'virus', SOFT, 600);
        g += ab(104, 52 + 31, s.antigen, A, 0) + ab(104 - 34, 52, s.antigen, A, 90) +
             ab(104 + 34, 52, s.antigen, A, -90);
        g += T(104, 126, 'coated — cannot attach', SOFT, 600);
        return g;
      }
      g += virus(120, 44) + T(120, 20, 'virus', SOFT, 600);
      g += antigen(s.antigen, 110, 55) + antigen(s.antigen, 130, 55);
      g += ab(60, 96, s.antigen, A, 0) + ab(104, 100, s.antigen, A, 0);
      g += T(80, 126, 'antibodies');
      return g;
    }

    if (s.id === 'drugVirus' || s.id === 'drugBacterium') {
      var isV = s.pathogen === 'virus';
      if (phase === 'after' && s.outcome === 'drugKills') {
        g += rodDead(48, 40, 84, 26) + T(90, 30, 'bacterium', SOFT, 600);
        g += T(90, 92, 'killed by the drug', SOFT, 600);
        g += capsule(232, 52) + T(232, 84, 'antibiotic');
        return g;
      }
      if (isV) { g += virus(90, 48) + T(90, 22, 'virus', SOFT, 600); }
      else { g += rod(48, 34, 84, 26) + T(90, 26, 'bacterium', SOFT, 600); }
      g += capsule(232, 52) + T(232, 84, 'antibiotic');
      if (phase === 'after') {
        g += '<path d="M200 52 L136 52" stroke="' + CS + '" stroke-width="1.6" stroke-dasharray="4 5"/>';
        g += T(150, 122, 'no effect — nothing for it to attack', SOFT, 600);
      }
      return g;
    }

    /* secondary */
    g += rod(30, 24, 82, 26) + T(71, 18, 'bacterium', SOFT, 600);
    g += antigen(s.antigen, 50, yb) + antigen(s.antigen, 70, yb) + antigen(s.antigen, 90, yb);
    if (phase === 'after') {
      g += ab(60, bind, s.antigen, A, 0);
      g += ab(140, 90, s.antigen, A, 14) + ab(174, 70, s.antigen, A, 26);
      g += lympho(240, 60, 24) + T(238, 104, 'memory lymphocyte');
      g += T(78, 122, 'antibody within hours', SOFT, 600);
    } else {
      g += lympho(240, 60, 24) + T(238, 104, 'memory lymphocyte');
      g += T(96, 122, 'no antibodies yet');
    }
    return g;
  }

  /* ---------------------------------------------------------------- model */

  /* The one place an outcome is decided. Options are only labels; this is
     what makes them right or wrong. */
  function resolve(s) {
    if (s.drug === 'antibiotic') return s.pathogen === 'bacterium' ? 'drugKills' : 'drugNone';
    if (s.ask === 'whichFits') {
      for (var i = 0; i < s.candidates.length; i++) {
        if (s.candidates[i].shape === s.antigen) return 'ab' + s.candidates[i].letter;
      }
      return 'anyFit';
    }
    if (s.memory) return 'secondary';
    if (s.abShape !== s.antigen) return 'noBind';
    if (s.count > 1) return 'clump';
    if (s.pathogen === 'virus') return 'neutralise';
    return 'tag';
  }

  var LABEL = {
    destroy: 'The antibodies destroy {P}.',
    tag: 'Antibodies tag {P}; the phagocyte digests it.',
    phagoMakes: 'The phagocyte makes antibodies to finish it off.',
    clump: 'Antibodies clump {P} together; a phagocyte engulfs the clump.',
    drift: 'Antibodies bind, but the bacteria stay apart and drift off.',
    neutralise: 'Antibodies coat {P} so it cannot enter the body cell.',
    enterCell: 'The antibodies follow the virus into the body cell.',
    noBind: 'Nothing binds — this antigen is a different shape.',
    shapeShift: 'The antibodies change shape to fit the new antigen.',
    bindAnyway: 'The antibodies bind and tag it anyway.',
    anyFit: 'Any of them — one antibody fits any antigen.',
    drugKills: 'The antibiotic kills {P}.',
    drugNone: 'The antibiotic has no effect on {P}.',
    drugAsAb: 'The antibiotic binds to the antigens, like an antibody.',
    drugMakesAb: 'The antibiotic makes the body produce antibodies.',
    secondary: 'Memory lymphocytes make the antibody within hours.',
    restart: 'The body starts from scratch, so it takes days again.'
  };

  var OUTCOME = {
    tag: 'The antibodies bind to the antigens and tag {P}, and the phagocyte engulfs it and digests it.',
    clump: 'Each antibody has two binding sites, so they hold the bacteria in a clump and one phagocyte engulfs the lot.',
    neutralise: 'The antibodies coat the antigens and neutralise the virus, so it cannot attach to the body cell. A phagocyte clears it later.',
    noBind: 'Nothing binds. These antibodies were made for a different antigen shape, so they cannot lock on.',
    drugKills: 'The antibiotic kills the bacteria by damaging structures only bacterial cells have.',
    drugNone: 'Nothing happens to the virus. It has none of the structures an antibiotic attacks, and it copies itself inside your own cells.',
    secondary: 'Memory lymphocytes recognise the antigen and make the matching antibody within hours, so it is tagged and cleared fast.'
  };

  var BEAT = {
    tag: 'The antibody marks; the phagocyte destroys.',
    clump: 'Clumping kills nothing — it makes one mouthful out of many.',
    neutralise: 'Neutralising blocks the virus; it does not break it apart.',
    noBind: 'One antibody fits one antigen — that is what specific means.',
    ab: 'One antibody fits one antigen, like a key cut for one lock.',
    drugKills: 'An antibiotic is a medicine you are given; an antibody is a protein your lymphocytes make.',
    drugNone: 'Antibodies can deal with a virus; antibiotics cannot.',
    secondary: 'The antibodies still only tag — phagocytes still do the destroying.'
  };

  var WHY = {
    destroy: 'An antibody is a protein, not a cell — it cannot break anything open. Binding is all it does, and that is what makes the pathogen easy prey.',
    phagoMakes: 'Phagocytes only engulf and digest. Lymphocytes make the antibodies. That split is the whole division of labour.',
    drift: 'An antibody has two binding sites, so one antibody can hold two bacteria at once — which is why they clump instead of drifting.',
    enterCell: 'Antibodies stay outside, in blood and tissue fluid. They cannot get inside a body cell, which is why blocking the virus first matters.',
    shapeShift: 'An antibody’s binding site is fixed. A new antigen needs a different lymphocyte making a different antibody — that takes days.',
    bindAnyway: 'Binding is not automatic. The binding site must be the complementary shape to that one antigen, so a different antigen is ignored.',
    anyFit: 'One antibody fits one antigen. The binding site is cut to that one shape, so the other two cannot lock on at all.',
    abWrong: 'Each binding site is cut for one antigen shape only, so the other two cannot lock on at all.',
    noBindWrong: 'These do fit — the binding site and the antigen are the same shape here, so they lock on.',
    tagWrong: 'They do bind and tag, but look again at who finishes the job.',
    drugKills: 'An antibiotic is not a general germ-killer. It is aimed at bacteria only, so a viral infection needs your own immune response.',
    drugNone: 'Antibiotics do kill bacteria — that is exactly what they are for. What they cannot touch is viruses.',
    drugAsAb: 'Three different things: the antigen is the marker on the pathogen, the antibody is a protein your lymphocytes make, the antibiotic is a drug.',
    drugMakesAb: 'That is what a vaccine does. An antibiotic damages bacterial cells directly and has nothing to do with making antibodies.',
    secondaryWrong: 'Memory lymphocytes are already there, so the antibody arrives in hours, not days.',
    restart: 'Memory lymphocytes from the first infection are still in your blood, so the second response is faster and bigger.',
    clumpWrong: 'Clumping is what happens when many antibodies meet many bacteria — but it still only holds them; something else eats them.',
    neutraliseWrong: 'Coating the virus blocks it from attaching; it does not destroy it.'
  };

  var SHAPES = ['tri', 'knob', 'tab'];
  var SHAPE_NAME = { tri: 'triangular', knob: 'round', tab: 'square' };

  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* ------------------------------------------------------------- rounds */
  var ROUNDS = {
    tagEngulf: function () {
      var sh = pick(SHAPES);
      return {
        id: 'tagEngulf', P: 'the bacterium', pathogen: 'bacterium', count: 1,
        antigen: sh, abShape: sh, phagocyte: true,
        frame: 'A bacterium is in the tissue fluid. Antibodies made for its antigen are drifting beside it, and a phagocyte is close by. What happens next?',
        opts: ['destroy', 'tag', 'phagoMakes']
      };
    },
    whichFits: function () {
      var sh = pick(SHAPES), order = shuffle(SHAPES);
      return {
        id: 'whichFits', P: 'the bacterium', pathogen: 'bacterium', count: 1,
        antigen: sh, ask: 'whichFits',
        candidates: [
          { letter: 'A', shape: order[0] }, { letter: 'B', shape: order[1] }, { letter: 'C', shape: order[2] }
        ],
        frame: 'Three kinds of antibody drift past this bacterium. Which one can bind to its antigen?',
        opts: ['abA', 'abB', 'abC', 'anyFit']
      };
    },
    noFit: function () {
      var a = pick(SHAPES), b = pick(SHAPES.filter(function (x) { return x !== a; }));
      return {
        id: 'noFit', P: 'the new bacterium', pathogen: 'bacterium', count: 1,
        antigen: a, abShape: b, phagocyte: false,
        frame: 'A bacterium you have never met arrives. The antibodies already in your blood were made for a different antigen. What happens next?',
        opts: ['destroy', 'bindAnyway', 'shapeShift', 'noBind']
      };
    },
    clump: function () {
      var sh = pick(SHAPES);
      return {
        id: 'clump', P: 'the bacteria', pathogen: 'bacterium', count: 3,
        antigen: sh, abShape: sh, phagocyte: true,
        frame: 'Several bacteria of the same kind are spread through the blood, with many antibodies for their antigen. What happens next?',
        opts: ['destroy', 'clump', 'drift']
      };
    },
    neutralise: function () {
      var sh = pick(SHAPES);
      return {
        id: 'neutralise', P: 'the virus', pathogen: 'virus', count: 1,
        antigen: sh, abShape: sh, phagocyte: false,
        frame: 'A virus is about to attach to a body cell. Antibodies for its antigen reach it first. What happens next?',
        opts: ['destroy', 'neutralise', 'enterCell']
      };
    },
    drugVirus: function () {
      return {
        id: 'drugVirus', P: 'the virus', pathogen: 'virus', count: 1,
        antigen: pick(SHAPES), drug: 'antibiotic',
        frame: 'A patient with a viral throat infection is given an antibiotic. What happens to the virus?',
        opts: ['drugKills', 'drugNone', 'drugAsAb', 'drugMakesAb']
      };
    },
    drugBacterium: function () {
      return {
        id: 'drugBacterium', P: 'the bacteria', pathogen: 'bacterium', count: 2,
        antigen: pick(SHAPES), drug: 'antibiotic',
        frame: 'A patient with a bacterial chest infection is given an antibiotic. What happens to the bacteria?',
        opts: ['drugKills', 'drugNone', 'drugAsAb']
      };
    },
    secondary: function () {
      var sh = pick(SHAPES);
      return {
        id: 'secondary', P: 'the bacterium', pathogen: 'bacterium', count: 1,
        antigen: sh, abShape: sh, memory: true, phagocyte: false,
        frame: 'This bacterium infected you a year ago. It is back, and memory lymphocytes for its antigen are in your blood. What happens next?',
        opts: ['destroy', 'secondary', 'restart']
      };
    }
  };

  function buildQueue() {
    var pairA = shuffle(['whichFits', 'noFit']);
    var pairB = shuffle(['drugVirus', 'drugBacterium']);
    var rest = shuffle(['clump', 'neutralise', 'secondary', pairA[1], pairB[1]]);
    return ['tagEngulf', pairA[0], pairB[0]].concat(rest);
  }

  /* Diagnostic for a wrong choice, given what actually happened. */
  function whyWrong(chosen, s) {
    if (chosen === 'destroy') return WHY.destroy;
    if (chosen === 'anyFit') return WHY.anyFit;
    if (chosen.slice(0, 2) === 'ab') return WHY.abWrong;
    if (chosen === 'drugKills') return WHY.drugKills;
    if (chosen === 'drugNone') return WHY.drugNone;
    if (chosen === 'noBind') return WHY.noBindWrong;
    if (chosen === 'tag') return WHY.tagWrong;
    if (chosen === 'clump') return WHY.clumpWrong;
    if (chosen === 'neutralise') return WHY.neutraliseWrong;
    if (chosen === 'secondary') return WHY.secondaryWrong;
    return WHY[chosen] || '';
  }

  /* ------------------------------------------------------------------ CSS */
  var CSS = [
    '.svw-adk{position:relative;box-sizing:border-box;background:#fff;border:1px solid #e8e3db;',
    'border-radius:16px;padding:1.05rem 1.05rem 1.1rem;color:#2d2a26;',
    'font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;max-width:100%;}',
    '.svw-adk *{box-sizing:border-box;}',
    '.svw-adk-kick{margin:0 0 .16rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--adk-a);}',
    '.svw-adk-title{margin:0 0 .3rem;font-family:"Source Serif 4",Georgia,serif;font-size:1.2rem;',
    'font-weight:600;line-height:1.2;letter-spacing:-.01em;}',
    '.svw-adk-frame{margin:0 0 .5rem;font-size:.85rem;line-height:1.4;color:#5b564e;}',
    '.svw-adk-stage{background:#faf8f5;border:1px solid #efe9e0;border-radius:12px;padding:.2rem;',
    'margin:0 0 .55rem;}',
    '.svw-adk-stage svg{display:block;width:100%;height:132px;}',
    '.svw-adk-opts{display:flex;flex-direction:column;gap:.3rem;margin:0 0 .5rem;}',
    '.svw-adk-opt{display:flex;align-items:center;gap:.5rem;width:100%;text-align:left;',
    'font-family:inherit;font-size:.8rem;font-weight:600;line-height:1.3;color:#2d2a26;',
    'background:#faf8f5;border:1px solid #ddd7cd;border-radius:10px;padding:.42rem .6rem;cursor:pointer;}',
    '.svw-adk-opt svg{flex:0 0 auto;}',
    '.svw-adk--wide .svw-adk-opts{display:grid;grid-template-columns:1fr 1fr;gap:.3rem;}',
    '.svw-adk--wide .svw-adk-opts>:last-child:nth-child(odd){grid-column:1/-1;}',
    '.svw-adk-opt[aria-pressed="true"]{background:#2d2a26;border-color:#2d2a26;color:#fff;}',
    '.svw-adk-row{display:flex;gap:.55rem;align-items:baseline;border:1px solid #ddd7cd;',
    'border-radius:10px;padding:.42rem .6rem;background:#faf8f5;}',
    '.svw-adk-row--ok{border-color:#4f7d63;}',
    '.svw-adk-lab{flex:0 0 auto;font-size:.66rem;font-weight:700;letter-spacing:.09em;',
    'text-transform:uppercase;color:#8d8880;}',
    '.svw-adk-row--ok .svw-adk-lab{color:#4f7d63;}',
    '.svw-adk-rtxt{font-size:.8rem;font-weight:600;line-height:1.3;}',
    '.svw-adk-go{display:block;width:100%;font-family:inherit;font-size:.82rem;font-weight:600;',
    'padding:.5rem .95rem;border-radius:10px;border:1px solid #2d2a26;background:#2d2a26;color:#fff;',
    'cursor:pointer;}',
    '.svw-adk-run{margin:.45rem 0 0;min-height:1.05rem;font-size:.76rem;color:#8d8880;',
    'font-variant-numeric:tabular-nums;}',
    '.svw-adk-cap{margin:.15rem 0 0;min-height:1.5rem;font-size:.83rem;line-height:1.45;color:#2d2a26;}',
    '.svw-adk-cap b{font-weight:700;}',
    '.svw-adk-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);',
    'white-space:nowrap;}',
    '.svw-adk--m .svw-adk-opt,.svw-adk--m .svw-adk-go{transition:background-color .12s ease,color .12s ease;}'
  ].join('');

  /* ---------------------------------------------------------------- mount */
  function mount(root, ctx) {
    ctx = ctx || {};
    var accent = ctx.accent ||
      (getComputedStyle(root).getPropertyValue('--accent') || '').trim() || '#b5713f';

    var wrap = document.createElement('div');
    wrap.className = 'svw-adk' + (ctx.reducedMotion ? '' : ' svw-adk--m');
    wrap.style.setProperty('--adk-a', accent);

    var style = document.createElement('style');
    style.textContent = CSS;
    wrap.appendChild(style);

    wrap.insertAdjacentHTML('beforeend',
      '<p class="svw-adk-kick">Immune response</p>' +
      '<h3 class="svw-adk-title">What happens next?</h3>' +
      '<p class="svw-adk-frame"></p>' +
      '<div class="svw-adk-stage"></div>' +
      '<div class="svw-adk-opts" role="group" aria-label="Predictions"></div>' +
      '<button type="button" class="svw-adk-go">Check</button>' +
      '<p class="svw-adk-run"></p>' +
      '<p class="svw-adk-cap"></p>' +
      '<p class="svw-adk-sr" aria-live="polite"></p>');
    root.appendChild(wrap);

    var elFrame = wrap.querySelector('.svw-adk-frame');
    var elStage = wrap.querySelector('.svw-adk-stage');
    var elOpts = wrap.querySelector('.svw-adk-opts');
    var elGo = wrap.querySelector('.svw-adk-go');
    var elRun = wrap.querySelector('.svw-adk-run');
    var elCap = wrap.querySelector('.svw-adk-cap');
    var elSr = wrap.querySelector('.svw-adk-sr');

    var queue = buildQueue();
    var qi = 0;
    var scene = null, picked = null, committed = false;
    var streak = 0, attempted = 0, mastered = false;

    function sizeStage() {
      var w = wrap.clientWidth || 360;
      var h = Math.max(112, Math.min(150, Math.round(w * 0.33)));
      var svg = elStage.querySelector('svg');
      if (svg) svg.style.height = h + 'px';
      /* two option columns once the card is wide enough for a full line each */
      if (w >= 520) wrap.classList.add('svw-adk--wide');
      else wrap.classList.remove('svw-adk--wide');
    }

    function text(key) {
      return (LABEL[key] || key).replace('{P}', scene.P);
    }

    function state(extra) {
      var o = { streak: streak, mastered: mastered, attempted: attempted, round: scene.id };
      if (picked) o.picked = picked;
      if (extra) for (var k in extra) o[k] = extra[k];
      root.dataset.svState = JSON.stringify(o);
    }

    /* the picture in words, for a screen reader */
    function stageAlt(phase) {
      if (phase === 'after') return 'What happened: ' + outcomeSentence();
      var kind = scene.pathogen === 'virus' ? 'A virus' : (scene.count > 1 ? 'Bacteria' : 'A bacterium');
      var t = kind + ' with ' + SHAPE_NAME[scene.antigen] + ' antigens';
      if (scene.ask === 'whichFits') {
        t += ', and three antibodies with ' + scene.candidates.map(function (c) {
          return c.letter + ' ' + SHAPE_NAME[c.shape];
        }).join(', ') + ' binding sites';
      } else if (scene.abShape) {
        t += ', and antibodies with ' + SHAPE_NAME[scene.abShape] + ' binding sites';
      }
      if (scene.phagocyte) t += ', and a phagocyte nearby';
      if (scene.memory) t += ', and a memory lymphocyte';
      if (scene.drug) t += ', and an antibiotic capsule';
      return t + '.';
    }

    function drawStage(phase) {
      elStage.innerHTML = '<svg viewBox="0 0 300 132" preserveAspectRatio="xMidYMid meet" ' +
        'role="img" aria-label="' + stageAlt(phase).replace(/"/g, '') + '">' +
        scenery(scene, phase, accent) + '</svg>';
      sizeStage();
    }

    function glyph(shape) {
      return '<svg viewBox="0 0 30 17" width="28" height="16" aria-hidden="true">' +
             socket(shape, 15, 14, 'currentColor') + '</svg>';
    }

    function renderOpts() {
      elOpts.innerHTML = '';
      scene.opts.forEach(function (key) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'svw-adk-opt';
        b.setAttribute('aria-pressed', 'false');
        b.setAttribute('data-key', key);
        if (key.slice(0, 2) === 'ab' && key.length === 3) {
          var c = scene.candidates[key.charCodeAt(2) - 65];
          b.innerHTML = glyph(c.shape) + '<span>Antibody ' + c.letter + '</span>';
        } else {
          b.textContent = text(key);
        }
        b.addEventListener('click', function () {
          if (committed) return;
          picked = key;
          var all = elOpts.querySelectorAll('.svw-adk-opt');
          for (var i = 0; i < all.length; i++) {
            all[i].setAttribute('aria-pressed', all[i] === b ? 'true' : 'false');
          }
          state();
          elSr.textContent = 'Chosen: ' + b.textContent;
        });
        elOpts.appendChild(b);
      });
    }

    function optionText(key) {
      if (key.slice(0, 2) === 'ab' && key.length === 3) return 'Antibody ' + key.charAt(2);
      return text(key);
    }

    function echo(key) {
      var t = optionText(key).replace(/\.$/, '');
      return t.charAt(0).toLowerCase() + t.slice(1);
    }

    function newRound() {
      if (qi >= queue.length) { queue = buildQueue(); qi = 0; }
      scene = ROUNDS[queue[qi++]]();
      scene.outcome = resolve(scene);
      if (scene.opts.indexOf(scene.outcome) === -1) scene.opts.push(scene.outcome);
      picked = null; committed = false;
      elFrame.textContent = scene.frame;
      drawStage('before');
      renderOpts();
      elGo.textContent = 'Check';
      elCap.innerHTML = '';
      state();
    }

    function outcomeSentence() {
      if (scene.outcome.slice(0, 2) === 'ab' && scene.outcome.length === 3) {
        var L = scene.outcome.charAt(2);
        return 'Only antibody ' + L + ' fits: its binding site is the complementary shape to the ' +
               SHAPE_NAME[scene.antigen] + ' antigen.';
      }
      return (OUTCOME[scene.outcome] || '').replace('{P}', scene.P);
    }

    function lc(t) { return t.charAt(0).toLowerCase() + t.slice(1); }

    function beat() {
      if (scene.outcome.slice(0, 2) === 'ab' && scene.outcome.length === 3) return BEAT.ab;
      return BEAT[scene.outcome] || '';
    }

    function showRows(right) {
      elOpts.innerHTML = '';
      function row(lab, txt, ok) {
        var d = document.createElement('div');
        d.className = 'svw-adk-row' + (ok ? ' svw-adk-row--ok' : '');
        d.innerHTML = '<span class="svw-adk-lab">' + lab + '</span>' +
                      '<span class="svw-adk-rtxt"></span>';
        d.querySelector('.svw-adk-rtxt').textContent = txt;
        elOpts.appendChild(d);
      }
      row('You said', optionText(picked), right);
      if (!right) row('Happens', optionText(scene.outcome), true);
    }

    function commit() {
      if (committed) {
        newRound();
        var first = elOpts.querySelector('.svw-adk-opt');
        if (first) first.focus();
        return;
      }
      if (!picked) {
        elCap.textContent = 'Choose one outcome first, then check it.';
        elSr.textContent = 'Choose one outcome first.';
        return;
      }
      committed = true;
      attempted++;
      var right = picked === scene.outcome;
      streak = right ? streak + 1 : 0;
      var justMastered = false;
      if (right && streak >= 3 && !mastered) { mastered = true; justMastered = true; }

      drawStage('after');
      showRows(right);

      var msg;
      if (right) msg = '<b>Right —</b> ' + lc(outcomeSentence()) + ' ' + beat();
      else msg = '<b>Not quite —</b> you said ' + echo(picked) + '. ' + outcomeSentence() + ' ' +
                 whyWrong(picked, scene);
      if (justMastered) {
        msg = '<b>Three in a row — you have it.</b> An antibody binds one matching antigen and tags, ' +
              'clumps or neutralises it; phagocytes engulf and digest; antibiotics are drugs that ' +
              'damage bacteria only.';
      }
      elCap.innerHTML = msg;
      elSr.textContent = (right ? 'Correct. ' : 'Wrong. ') + elCap.textContent;

      if (streak === 0) elRun.textContent =
        attempted === 1 ? 'Three in a row and you have it.' : 'Run back to zero.';
      else if (mastered) elRun.textContent = 'You have it. Keep going if you like.';
      else elRun.textContent = streak + ' right in a row' +
        (streak === 2 ? ' — one more and you have it.' : '.');

      elGo.textContent = mastered ? 'Another anyway' : 'Next';
      state({ correct: right, outcome: scene.outcome });
    }

    elGo.addEventListener('click', commit);

    if (typeof ResizeObserver === 'function') {
      var ro = new ResizeObserver(sizeStage);
      ro.observe(wrap);
    }

    newRound();
  }

  window.SVWidget = {
    meta: {
      id: 'antibodies-dont-kill',
      title: 'What happens next?',
      teaches: 'Antibodies bind to one matching antigen and tag, clump or neutralise the pathogen; phagocytes do the destroying, and antibiotics are drugs that kill bacteria only.'
    },
    mount: mount
  };
})();
