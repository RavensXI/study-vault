"""Gemini image generation — call Gemini API with optional input image.

Extracted from gemini_regen.py and generate_drama_diagrams.py.
"""

import base64
import json
import os
import sys
import urllib.request


API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-3.1-flash-image-preview"


def call_gemini_image(prompt, input_image_path=None, output_path=None, timeout=180):
    """Send a prompt (and optional input image) to Gemini, return image bytes.

    Args:
        prompt: Text prompt for Gemini.
        input_image_path: Optional path to a reference/matplotlib image to include.
        output_path: If provided, save the returned image to this path.
        timeout: Request timeout in seconds.

    Returns:
        (image_bytes, gemini_text) tuple. image_bytes is None if no image returned.
    """
    if not API_KEY:
        print("ERROR: Set GEMINI_API_KEY environment variable")
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

    parts = [{"text": prompt}]

    if input_image_path:
        with open(input_image_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")
        # Detect mime type from extension
        ext = os.path.splitext(input_image_path)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        parts.append({"inlineData": {"mimeType": mime, "data": img_data}})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"Gemini HTTP {e.code}: {body[:500]}")
        return None, f"HTTP {e.code}"

    image_bytes = None
    gemini_text = ""

    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                image_bytes = base64.b64decode(part["inlineData"]["data"])
            elif "text" in part:
                txt = part["text"].strip()
                if txt:
                    gemini_text += txt + "\n"

    if image_bytes and output_path:
        with open(output_path, "wb") as f:
            f.write(image_bytes)

    return image_bytes, gemini_text.strip()
