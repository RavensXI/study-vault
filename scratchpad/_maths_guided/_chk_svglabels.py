import json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
pd = json.load(open("_CHK_L03_NOW.json", encoding="utf-8"))
pb = pd["problem_bank"]
tiers = ["bronze","silver","gold"]

def analyze(tag, disp):
    m = re.search(r"<svg.*?</svg>", disp, re.S)
    if not m:
        print(f"{tag}: NO SVG"); return
    svg = m.group(0)
    # text labels
    texts = re.findall(r"<text[^>]*>(.*?)</text>", svg, re.S)
    texts = [re.sub(r"<[^>]+>","",t).strip() for t in texts]
    # aria
    aria = re.search(r'aria-label="([^"]*)"', svg)
    # external refs
    ext = re.findall(r'(href\s*=|url\(|xlink:href|<script|<image)', svg)
    # hardcoded dark text fills
    darkfills = re.findall(r'<text[^>]*fill="([^"]*)"', svg)
    print(f"\n{tag}")
    print("  aria:", aria.group(1) if aria else None)
    print("  labels:", texts)
    print("  text-fills:", set(darkfills))
    if ext: print("  !! EXTERNAL:", ext)
    print("  size:", len(svg), "bytes")

for t in tiers:
    for i,p in enumerate(pb.get(t,[])):
        analyze(f"[{t}[{i}]] {re.sub(chr(60)+'svg.*?'+chr(60)+'/svg>','',p['display'],flags=re.S)[:80]}", p["display"])
