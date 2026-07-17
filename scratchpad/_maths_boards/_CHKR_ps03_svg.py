import json,re
live=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
s=json.dumps(live,ensure_ascii=False)
# find all svg text fills
texts=re.findall(r'<text[^>]*fill="([^"]+)"',s)
badtext=[f for f in texts if f!="currentColor"]
print("distinct text fills:",set(texts))
print("non-currentColor text fills:",set(badtext))
print("external refs (http/xlink/url):", bool(re.search(r'xlink:href|<image|href="http|url\(',s)))
print("<script in svg:", "<script" in s)
# region path fills without opacity
paths=re.findall(r'<(?:path|rect)[^>]*fill="(#[0-9a-fA-F]{3,6})"[^>]*?(fill-opacity="[^"]+")?\s*/?>',s)
noop=[p for p in paths if not p[1]]
print("region fills missing opacity count:",len(noop), noop[:5])
