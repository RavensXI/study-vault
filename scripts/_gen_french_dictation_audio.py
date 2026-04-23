"""
Generate French dictation TTS audio for free-tier French (slug 'french-aqa', school_id NULL).
Adapted from scripts/language-practice/generate_dictation_audio.py.
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client
import boto3
import requests

VOICES = {"odd": "fr-FR-HenriNeural", "even": "fr-FR-DeniseNeural"}
LANG_CODE = "fr-FR"

R2_BUCKET = "studyvault-audio"
R2_PUBLIC_URL = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev"


def get_r2():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )


def gen_audio(text, voice):
    AZURE_KEY = os.environ["AZURE_SPEECH_KEY"]
    url = "https://uksouth.tts.speech.microsoft.com/cognitiveservices/v1"
    ssml = (
        f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{LANG_CODE}'>"
        f"<voice name='{voice}'><prosody rate='-5%'>{text}</prosody></voice></speak>"
    )
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3",
        "User-Agent": "studyvault-dictation",
    }
    for attempt in range(3):
        try:
            r = requests.post(url, data=ssml.encode("utf-8"), headers=headers, timeout=30)
            if r.status_code == 200:
                return r.content
            print(f"    Azure {r.status_code}: {r.text[:200]}")
            time.sleep(2)
        except requests.RequestException as e:
            print(f"    {e}")
            time.sleep(2)
    return None


def main():
    sb = get_client()
    r2 = get_r2()

    subj = sb.table("subjects").select("id").eq("slug", "french-aqa").is_("school_id", "null").single().execute().data
    sid = subj["id"]
    units = sb.table("units").select("id,slug").eq("subject_id", sid).execute().data

    total_generated = 0
    for unit in units:
        lessons = sb.table("lessons").select("id,lesson_number,practice_data").eq("unit_id", unit["id"]).order("lesson_number").execute().data
        for lesson in lessons:
            pd = lesson["practice_data"]
            if not pd:
                continue
            pb = pd.get("problem_bank", {}) or {}
            voice = VOICES["odd"] if lesson["lesson_number"] % 2 == 1 else VOICES["even"]
            modified = False
            for tier in ["bronze", "silver", "gold"]:
                for i, p in enumerate(pb.get(tier, [])):
                    if p.get("input_type") != "dictation":
                        continue
                    if p.get("audio_url"):
                        continue
                    text = p.get("audio_text") or p.get("correct_text", "")
                    if not text:
                        continue
                    r2_key = f"french-aqa/dictation/{unit['slug']}_L{lesson['lesson_number']:02d}_{tier}_{i}.mp3"
                    audio_url = f"{R2_PUBLIC_URL}/{r2_key}"
                    print(f"  L{lesson['lesson_number']:02d} {tier}[{i}] ({voice.split('-')[-1][:6]}): {text[:60]}")
                    mp3 = gen_audio(text, voice)
                    if mp3:
                        r2.put_object(Bucket=R2_BUCKET, Key=r2_key, Body=mp3, ContentType="audio/mpeg")
                        p["audio_url"] = audio_url
                        modified = True
                        total_generated += 1
                    time.sleep(0.25)
            if modified:
                sb.table("lessons").update({"practice_data": pd}).eq("id", lesson["id"]).execute()
                print(f"    [updated] L{lesson['lesson_number']:02d} — {total_generated} clips total so far")

    print(f"\n[DONE] Generated {total_generated} dictation clips.")


if __name__ == "__main__":
    main()
