import os, json, urllib.request
ID="5cfec765-3128-469b-9d6a-626f042d6161"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
back=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})))[0]["practice_data"]
open("_live_after_rp01.json","w",encoding="utf-8").write(json.dumps(back,indent=1,ensure_ascii=False))

changes={
 "key":"ratio-proportion-L01",
 "problems_fixed":[
  {"tier":"bronze","index":7,"what":"Duplicate answer within bronze (n=4 appeared in both bronze[5] and bronze[7]); changed simplify problem from 36:48 to 42:49 so the second part is 7, removing the collision.","old":"Simplify 36 : 48. Give the second part. (answer 4)","new":"Simplify 42 : 49. Give the second part. (answer 7)"}
 ],
 "issues_resolved":1,
 "opener_concept":"Sharing 12 sweets 1-for-you-2-for-friend by dealing them out; names it as splitting into parts, finding one part, multiplying. Inline SVG shows the 12 sweets.",
 "figures_added":[
  {"tier":"opener","index":0,"kind":"svg","what":"12 sweets (circles) to make the sharing concrete."},
  {"tier":"teach.bronze","index":0,"kind":"svg","what":"Bar model, 5 equal parts split 2 and 3, £30 total."},
  {"tier":"teach.silver","index":0,"kind":"svg","what":"Bar model, 8 equal parts split 3 and 5, £72 total."},
  {"tier":"teach.gold","index":0,"kind":"svg","what":"Bar model, 11 parts with the 4-part share marked £20 (reverse problem)."}
 ],
 "notes":"Fresh-solved all 20 bank problems (8 bronze / 7 silver / 5 gold): every stored solution was already correct. Only defect found was the bronze duplicate answer (fixed). Added guided (opener + 3 teach walks), tier_guides, per-problem guided_steps + hints, and slim method_card. Rewrote all misconceptions from bare worked-solutions into honest-diagnosis messages each with a derived, non-solution expect (single_value scalars; fraction 2-lists [14,1] and [1,3]). Preserved related_videos, worked_examples, topic_links byte-for-byte. Ratio bank problems left figure-free (exam-realism: GCSE ratio questions are textual); figures added only to opener/teach scaffolds."
}
open("changes_maths-aqa_ratio-proportion-L01.json","w",encoding="utf-8").write(json.dumps(changes,indent=1,ensure_ascii=False))
print("changes written")
