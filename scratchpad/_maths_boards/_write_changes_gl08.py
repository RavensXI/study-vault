import io, json

base = {"key": "graphs-L08", "board": "maths-aqa",
        "lesson_id": "2ce07c9f-af5f-4162-ae95-544d91a71830",
        "title": "Gradients of Curves & Areas Under Graphs"}

changes = dict(base)
changes["problems_fixed"] = [
    {"tier": "bronze", "index": 7,
     "what": "Within-tier duplicate answer: gradient came out 2, identical to bronze[0]. Re-posed the tangent points so the gradient is 5, keeping it a clean non-calculator integer and distinct in the tier.",
     "old": {"display": "tangent at x=3 through (1,4) and (5,12)", "solution": 2},
     "new": {"display": "tangent at x=2 through (1,2) and (3,12)", "solution": 5}},
]
changes["issues_resolved"] = 1
changes["opener_concept"] = ("A car at a steady 20 m/s for 3 s: distance = speed x time = 60, "
    "and that 60 is exactly the AREA of the 3-by-20 rectangle under the speed-time graph. "
    "Names area-under-graph = distance, and gradient-of-graph = speed, before any formal method.")
changes["notes"] = (
    "Fresh-solved all 20 problems from their displays: every stored numeric solution and every "
    "MC option-index was already correct (no wrong answers, no degenerate/non-calculator-messy cases). "
    "Full guided conversion added: guided.opener (speed-time rectangle), guided.teach for all three "
    "tiers (rise/run; trapezium rule 3-strip; trapezium rule 5-strip on y=x^2), tier_guides for all "
    "three tiers, tier descriptions, per-problem hints, and guided_steps with a phase:substitute "
    "completion boundary on all 17 non-MC problems. "
    "REPAIRED misconceptions on every problem: the stored ones leaked internal thinking into "
    "student text ('Wait, recheck', 'let me verify'), used em dashes, and carried no expect field "
    "(validator now requires it). Rebuilt each as an honest-diagnosis message with a derived, "
    "committed-error expect value (swap rise/run, forgot the half, middles-not-doubled, no-half in "
    "trapezium rule, dropped rectangle, sign slip, wrong h). method_card trimmed to 4 steps within "
    "the 140-word budget. Preserved topic_links, related_videos, worked_examples byte-for-byte. "
    "Validator PASS; PATCH 204; round-trip verified.")
json.dump(changes, io.open("changes_maths-aqa_graphs-L08.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

dia = dict(base)
dia["figures_added"] = [
    {"tier": "opener", "index": 0, "kind": "svg",
     "what": "Speed-time graph: shaded rectangle 3 s wide, 20 m/s tall (area = distance = 60). currentColor axes/labels, soft blue fill-opacity 0.3."},
    {"tier": "bronze", "index": 2, "kind": "svg",
     "what": "Right-angled triangle labelled base = 6, height = 8, with right-angle square. 'Diagram not drawn accurately' caption."},
    {"tier": "bronze", "index": 3, "kind": "svg",
     "what": "Trapezium: top parallel side 4, bottom 10, height 3. Soft green fill."},
    {"tier": "bronze", "index": 4, "kind": "svg",
     "what": "Speed-time rectangle: width 5 s, height 12 m/s (area = distance)."},
    {"tier": "bronze", "index": 6, "kind": "svg",
     "what": "Speed-time triangle: base 10 s, height 20 m/s (area = distance)."},
    {"tier": "silver", "index": 2, "kind": "svg",
     "what": "Composite speed-time graph: 0 to 10 m/s by t=5, steady to t=15, down to 0 at t=20 (triangle+rectangle+triangle)."},
    {"tier": "silver", "index": 0, "kind": "chart",
     "what": "Curve through (0,0),(2,4),(4,12),(6,24) with filled area under: the region being estimated by the trapezium rule."},
    {"tier": "silver", "index": 1, "kind": "chart",
     "what": "Curve through x=0..3 with y-values 1,4,9,16, filled area under."},
    {"tier": "silver", "index": 3, "kind": "chart",
     "what": "y = x^2 with dashed tangent through (0,-4) and (3,8) touching at (2,4); gradient 4. Tangent line and touch-point both verified on the curve."},
    {"tier": "silver", "index": 4, "kind": "chart",
     "what": "Curve x=0..4, y-values 0,3,8,15,24, filled area under."},
    {"tier": "silver", "index": 5, "kind": "chart",
     "what": "Curve x=0,2,4,6 (h=2), y-values 0,6,8,6, filled area under."},
    {"tier": "gold", "index": 0, "kind": "chart",
     "what": "Curve x=0..5, y-values 1,2,5,10,17,26, filled area under (5-strip estimate)."},
    {"tier": "gold", "index": 2, "kind": "chart",
     "what": "y = x^3 with dashed tangent through (1,-4) and (3,20) touching at (2,8); gradient 12. Verified: line grad 12, curve point 2^3=8."},
    {"tier": "gold", "index": 3, "kind": "chart",
     "what": "y = x^2 (0 to 2) with y-values 0,0.25,1,2.25,4 at x=0,0.5,1,1.5,2, filled area under."},
]
dia["opener_touched"] = True
dia["notes"] = ("14 figures in one pass. Drawn wherever an AQA paper prints one: every named shape "
    "(triangle/trapezium/rectangle), every speed-time scene, every trapezium-rule region, and both "
    "tangent-on-curve gradient problems where the curve equation is given (y=x^2, y=x^3). Skipped "
    "figures on the pure read-off/interpretation MC items and the generic 'a curve' gradient items "
    "where no equation is stated. All labels cross-checked against problem text; all tangent points "
    "and plotted curve points recomputed to satisfy their equations. Theme-safe: text/strokes "
    "currentColor, region fills soft colours at fill-opacity 0.3, no external refs.")
json.dump(dia, io.open("changes_maths-aqa_graphs-L08_diagrams.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("wrote both changes files")
