import json
key="algebra-L12"
changes={
 "key":key,
 "problems_fixed":[],
 "issues_resolved":0,
 "opener_concept":"Number machine multiplying (x-2)(x-6): test x=7 (both brackets positive, product positive) then x=4 (one positive, one negative, product negative), revealing the product is below zero only BETWEEN the roots 2 and 6.",
 "notes":"Fresh-solved all 20 problems (8 bronze, 7 silver, 5 gold): every stored solution correct (MC correct=index 0; gold single_value 4 and 3). No maths repairs needed. Added full guided layer: opener, teach walks bronze/silver/gold (fresh problems x^2-16<0, x^2-x-12>=0, 2x^2+3x-2<0, none in bank), tier_guides with worked examples, tier descriptions, per-problem plain-text hints, guided_steps on the two single_value gold problems with phase:substitute completion boundary. Rewrote every misconception message to student-facing prose and derived each expect by committing the error (MC expect = wrong option index; single_value expect = the wrong count). Trimmed method_card to slim reference. Preserved topic_links, related_videos, worked_examples byte-for-byte."
}
json.dump(changes,open("changes_maths-eduqas_algebra-L12.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)

dia={
 "key":key,
 "figures_added":[
  {"tier":"teach.bronze","index":0,"kind":"svg","what":"U-shaped parabola y=x^2-16 crossing at -4 and 4, region below axis between roots shaded (matches x^2-16<0 walk)."},
  {"tier":"teach.silver","index":0,"kind":"svg","what":"U-shaped parabola y=x^2-x-12 crossing at -3 and 4, regions above axis outside roots shaded (matches x^2-x-12>=0 walk)."},
  {"tier":"teach.gold","index":0,"kind":"svg","what":"U-shaped parabola y=2x^2+3x-2 crossing at -2 and 0.5, region below axis between roots shaded (matches 2x^2+3x-2<0 walk)."},
  {"tier":"gold","index":2,"kind":"svg","what":"Number line 0 to 5, closed circles at roots 1 and 4 (inclusive <=), integers 1,2,3,4 marked for the count question x^2-5x+4<=0."},
  {"tier":"gold","index":3,"kind":"svg","what":"Number line -2 to 5, open circles at roots -1 and 4 (strict), positive integers 1,2,3 marked for x^2<3x+4."}
 ],
 "opener_touched":False,
 "notes":"All figures generated programmatically from each problem's own roots; theme-safe (currentColor text/strokes, soft fill-opacity 0.3 regions, blue #60a5fa curves, amber band). MC solve-region problems left textual (exam prints no figure for these); figures added where the exam would show a parabola sketch or number line."
}
json.dump(dia,open("changes_maths-eduqas_algebra-L12_diagrams.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("changes files written")
