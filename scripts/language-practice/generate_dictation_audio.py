"""
Generate Azure TTS audio for dictation problems in language practice lessons.
Reads practice_data from Supabase, generates audio for each dictation problem,
uploads to R2, and updates practice_data with audio_url.

Usage: python scripts/language-practice/generate_dictation_audio.py [--subject spanish|french|german] [--limit N] [--dry-run]
"""
import os, sys, json, argparse, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from supabase import create_client
from lib.narration import generate_audio_rest

try:
    import boto3
except ImportError:
    print("pip install boto3 required for R2 upload")
    sys.exit(1)

# Language → Azure voice mapping (multilingual voices for correct pronunciation)
LANG_VOICES = {
    "es": {"odd": "es-ES-AlvaroNeural", "even": "es-ES-ElviraNeural"},
    "fr": {"odd": "fr-FR-HenriNeural", "even": "fr-FR-DeniseNeural"},
    "de": {"odd": "de-DE-ConradNeural", "even": "de-DE-KatjaNeural"},
}

R2_BUCKET = "studyvault-audio"
R2_PUBLIC_URL = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev"

def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )

def generate_dictation_ssml(text, voice, lang_code):
    """Build SSML for dictation — speaks in target language only."""
    ssml = (
        f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' "
        f"xml:lang='{lang_code}'>"
        f"<voice name='{voice}'>"
        f"<prosody rate='-5%'>{text}</prosody>"
        f"</voice></speak>"
    )
    return ssml

def generate_audio_for_dictation(text, voice, lang_code):
    """Generate MP3 for a dictation sentence using Azure Speech."""
    import requests

    AZURE_KEY = os.environ.get("AZURE_SPEECH_KEY")
    AZURE_REGION = "uksouth"
    url = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

    ssml = generate_dictation_ssml(text, voice, lang_code)

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3",
    }

    for attempt in range(3):
        try:
            resp = requests.post(url, headers=headers, data=ssml.encode("utf-8"), timeout=60)
            if resp.status_code == 200:
                return resp.content
            elif resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 5))
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"    HTTP {resp.status_code}: {resp.text[:200]}")
                if attempt < 2:
                    time.sleep(2)
        except Exception as e:
            print(f"    Request error: {e}")
            if attempt < 2:
                time.sleep(2)

    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', choices=['spanish','french','german'])
    parser.add_argument('--limit', type=int, default=0, help='Max lessons to process (0 = all)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])
    r2 = None if args.dry_run else get_r2_client()

    lang_map = {"spanish": "es", "french": "fr", "german": "de"}
    subjects = [args.subject] if args.subject else ['spanish', 'french', 'german']

    for slug in subjects:
        lang = lang_map[slug]
        voices = LANG_VOICES[lang]
        lang_code = {"es": "es-ES", "fr": "fr-FR", "de": "de-DE"}[lang]

        # Get school-specific subject
        subj = sb.table('subjects').select('id').eq('slug', slug).not_.is_('school_id', 'null').execute().data
        if not subj:
            print(f"[SKIP] {slug} not found")
            continue
        sid = subj[0]['id']

        # Get all units + lessons
        units = sb.table('units').select('id, slug').eq('subject_id', sid).execute().data

        total_clips = 0
        for unit in units:
            lessons = sb.table('lessons').select('id, lesson_number, title, practice_data').eq('unit_id', unit['id']).order('lesson_number').execute().data

            if args.limit:
                lessons = lessons[:args.limit]

            for lesson in lessons:
                pd = lesson['practice_data']
                if not pd or not isinstance(pd, dict):
                    continue

                pb = pd.get('problem_bank', {})
                voice = voices['odd'] if lesson['lesson_number'] % 2 == 1 else voices['even']
                modified = False

                for tier_name in ['bronze', 'silver', 'gold']:
                    problems = pb.get(tier_name, [])
                    for i, problem in enumerate(problems):
                        if problem.get('input_type') != 'dictation':
                            continue
                        if problem.get('audio_url'):
                            continue  # Already has audio

                        audio_text = problem.get('audio_text') or problem.get('correct_text', '')
                        if not audio_text:
                            continue

                        r2_key = f"{slug}/dictation/L{lesson['lesson_number']:02d}_{tier_name}_{i}.mp3"
                        audio_url = f"{R2_PUBLIC_URL}/{r2_key}"

                        if args.dry_run:
                            print(f"  [DRY] {slug} L{lesson['lesson_number']:02d} {tier_name}[{i}]: {audio_text[:60]}...")
                            total_clips += 1
                            continue

                        print(f"  Generating: {slug} L{lesson['lesson_number']:02d} {tier_name}[{i}]: {audio_text[:50]}...")
                        mp3_bytes = generate_audio_for_dictation(audio_text, voice, lang_code)

                        if mp3_bytes:
                            r2.put_object(
                                Bucket=R2_BUCKET,
                                Key=r2_key,
                                Body=mp3_bytes,
                                ContentType="audio/mpeg",
                            )
                            problem['audio_url'] = audio_url
                            modified = True
                            total_clips += 1
                            print(f"    Uploaded: {r2_key} ({len(mp3_bytes)} bytes)")
                        else:
                            print(f"    FAILED to generate audio")

                        time.sleep(0.3)  # Rate limiting

                if modified and not args.dry_run:
                    sb.table('lessons').update({'practice_data': pd}).eq('id', lesson['id']).execute()
                    print(f"  Updated practice_data for L{lesson['lesson_number']:02d}")

        print(f"\n{slug}: {total_clips} dictation clips {'would be ' if args.dry_run else ''}generated")

if __name__ == '__main__':
    main()
