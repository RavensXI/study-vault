"""Helper: Send a matplotlib diagram + prompt to Gemini and save the result.

Usage:
    python gemini_regen.py <matplotlib_backup_path> <output_path> <prompt_file>

The prompt is read from a text file so agents can write custom prompts.
"""

import os
import sys
import json
import base64
import urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: Set GEMINI_API_KEY environment variable")
    sys.exit(1)

MODEL = "gemini-3.1-flash-image-preview"


def main():
    if len(sys.argv) != 4:
        print("Usage: python gemini_regen.py <input_img> <output_img> <prompt_file>")
        sys.exit(1)

    input_img = sys.argv[1]
    output_img = sys.argv[2]
    prompt_file = sys.argv[3]

    with open(input_img, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"parts": [
            {"text": prompt_text},
            {"inlineData": {"mimeType": "image/jpeg", "data": img_data}}
        ]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }

    print(f"Sending to Gemini ({MODEL})...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"HTTP {e.code}: {body[:500]}")
        sys.exit(1)

    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                with open(output_img, "wb") as f:
                    f.write(img_bytes)
                print(f"OK — saved {output_img} ({len(img_bytes) / 1024:.0f} KB)")
                return
            elif "text" in part:
                txt = part["text"].strip()
                if txt:
                    print(f"Gemini note: {txt[:200]}")

    print("FAIL — no image returned")
    sys.exit(1)


if __name__ == "__main__":
    main()
