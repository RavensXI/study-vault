"""Generate a single diagram using Gemini API.
Usage: python generate_diagram.py "prompt text" output_filename.jpg
"""
import sys, os, json, base64, urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set"); sys.exit(1)

prompt = sys.argv[1]
outfile = sys.argv[2]

model = os.environ.get("GEMINI_MODEL", "gemini-3-pro-image-preview")
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
}
req = urllib.request.Request(url, json.dumps(payload).encode(), {"Content-Type": "application/json"})
try:
    resp = urllib.request.urlopen(req, timeout=120)
    data = json.loads(resp.read())
    for part in data["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            img_bytes = base64.b64decode(part["inlineData"]["data"])
            with open(outfile, "wb") as f:
                f.write(img_bytes)
            size_kb = len(img_bytes) / 1024
            print(f"Saved {outfile} ({size_kb:.0f} KB)")
            sys.exit(0)
    print("ERROR: No image in response")
    print(json.dumps(data, indent=2)[:500])
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
