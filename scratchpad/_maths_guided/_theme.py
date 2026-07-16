import json, re
d = json.load(open("_CHK_geomL01_live.json",encoding="utf-8"))
raw = json.dumps(d["practice_data"], ensure_ascii=False)
# external refs
for pat in ["http://","https://","xlink:href","<script","url(","<image"]:
    # allow https in related_videos etc - only care inside <svg>
    pass
svgs = re.findall(r"<svg.*?</svg>", raw, re.S)
print("SVG count:", len(svgs))
bad=[]
for s in svgs:
    for m in re.findall(r'fill="(#[0-9a-fA-F]{3,6})"', s):
        # find the tag; text fills must be currentColor
        pass
    # text tags with non-currentColor fill
    for tm in re.findall(r'<text[^>]*fill="([^"]+)"', s):
        if tm != "currentColor":
            bad.append(("TEXT-FILL", tm, s[:60]))
    # region polygon fills that are hex must have opacity - collect
    for pm in re.finditer(r'<polygon[^>]*fill="(#[0-9a-fA-F]{3,6})"[^>]*>', s):
        seg = pm.group(0)
        if "fill-opacity" not in seg:
            bad.append(("POLY-NO-OPACITY", pm.group(1), seg[:80]))
    if "http" in s or "<script" in s or "xlink" in s or "<image" in s:
        bad.append(("EXTERNAL", "", s[:80]))
    if "role=\"img\"" not in s:
        bad.append(("NO-ROLE", "", s[:80]))
    if "aria-label" not in s:
        bad.append(("NO-ARIA", "", s[:80]))
    if "viewBox" not in s:
        bad.append(("NO-VIEWBOX","",s[:80]))
print("ISSUES:", bad if bad else "NONE")
# em dash check across student-facing
em = raw.count("—")
print("EM-DASH count:", em)
