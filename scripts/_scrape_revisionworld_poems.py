"""Scrape full poem texts from revisionworld.com for AQA + Edexcel anthologies.

For each poem URL: HTTP GET, find the marker `<p><strong>{Title} by {Poet}</strong></p>`,
collect subsequent `<p>` blocks until we hit an analysis/structure marker.
Replace `<br>` with newlines, strip HTML tags, decode entities.
"""
import html as html_lib
import re
import time
import urllib.request
from pathlib import Path

OUT_BASE = Path("data/canonical_poems")
BASE_URL = "https://revisionworld.com"

# (title, poet, url_path, anthology_slug)
POEMS = [
    # AQA Love & Relationships
    ("Before You Were Mine", "Carol Ann Duffy", "/a2-level-level-revision/english-literature-gcse-level/poetry/carol-ann-duffy/you-were-mine", "aqa-love-and-relationships"),
    ("Climbing My Grandfather", "Andrew Waterhouse", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/climbing-my-grandfather-andrew", "aqa-love-and-relationships"),
    ("Eden Rock", "Charles Causley", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/eden-rock-charles-causley", "aqa-love-and-relationships"),
    ("The Farmer's Bride", "Charlotte Mew", "/level-revision/english-literature-gcse-level/poetry/charlotte-mew/farmers-bride-charlotte-mew", "aqa-love-and-relationships"),
    ("Follower", "Seamus Heaney", "/a2-level-level-revision/english-literature-gcse-level/poetry/seamus-heaney/follower", "aqa-love-and-relationships"),
    ("Letters from Yorkshire", "Maura Dooley", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/letters-yorkshire-maura-dooley", "aqa-love-and-relationships"),
    ("Love's Philosophy", "Percy Bysshe Shelley", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/percy-bysshe-shelley/loves", "aqa-love-and-relationships"),
    ("Mother, Any Distance", "Simon Armitage", "/a2-level-level-revision/english-literature-gcse-level/poetry/simon-armitage/mother-any-distance", "aqa-love-and-relationships"),
    ("Neutral Tones", "Thomas Hardy", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/thomas-hardy/neutral-tones", "aqa-love-and-relationships"),
    ("Porphyria's Lover", "Robert Browning", "/level-revision/english-literature-gcse-level/poetry/robert-browning/porphyrias-lover-robert", "aqa-love-and-relationships"),
    ("Singh Song!", "Daljit Nagra", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/singh-song-daljit-nagra", "aqa-love-and-relationships"),
    ('Sonnet 29 "I think of thee,"', "Elizabeth Barrett Browning", "/level-revision/english-literature-gcse-level/poetry/elizabeth-barrett-browning/sonnet-29-i-think", "aqa-love-and-relationships"),
    ("Walking Away", "C. Day Lewis", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/walking-away-cecil-day-lewis", "aqa-love-and-relationships"),
    ("When We Two Parted", "Lord Byron", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/lord-byron/when-we-two-parted", "aqa-love-and-relationships"),
    ("Winter Swans", "Owen Sheers", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/winter-swans-owen-sheers", "aqa-love-and-relationships"),

    # AQA Power and Conflict
    ("Bayonet Charge", "Ted Hughes", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/bayonet-charge-ted-hughes", "aqa-power-and-conflict"),
    ("The Charge of the Light Brigade", "Alfred, Lord Tennyson", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/charge-light-brigade-alfred-lord", "aqa-power-and-conflict"),
    ("Checking Out Me History", "John Agard", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/john-agard/checking-out-me", "aqa-power-and-conflict"),
    ("The Emigrée", "Carol Rumens", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/emigree-carol-rumens", "aqa-power-and-conflict"),
    ("Exposure", "Wilfred Owen", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/exposure-wilfred-owen", "aqa-power-and-conflict"),
    ("Kamikaze", "Beatrice Garland", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/kamikaze-beatrice-garland", "aqa-power-and-conflict"),
    ("London", "William Blake", "/a2-level-level-revision/english-literature-gcse-level/poetry/william-blake/london", "aqa-power-and-conflict"),
    ("My Last Duchess", "Robert Browning", "/a2-level-level-revision/english-literature-gcse-level/poetry/pre-1914-poems/my-last-duchess-robert-browning", "aqa-power-and-conflict"),
    ("Ozymandias", "Percy Bysshe Shelley", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/percy-bysshe-shelley/ozymandias", "aqa-power-and-conflict"),
    ("Poppies", "Jane Weir", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/poppies-jane-weir", "aqa-power-and-conflict"),
    ("The Prelude", "William Wordsworth", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/william-wordsworth/prelude", "aqa-power-and-conflict"),
    ("Remains", "Simon Armitage", "/level-revision/english-literature-gcse-level/poetry/simon-armitage/remains-simon-armitage", "aqa-power-and-conflict"),
    ("Storm on the Island", "Seamus Heaney", "/a2-level-level-revision/english-literature-gcse-level/poetry/seamus-heaney/storm-island", "aqa-power-and-conflict"),
    ("Tissue", "Imtiaz Dharker", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/imtiaz-dharker/tissue", "aqa-power-and-conflict"),
    ("War Photographer", "Carol Ann Duffy", "/level-revision/english-literature-gcse-level/poetry/carol-ann-duffy/war-photographer-carole-ann", "aqa-power-and-conflict"),

    # AQA Worlds and Lives
    ("Lines Written in Early Spring", "William Wordsworth", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/william-wordsworth/lines-written", "aqa-worlds-and-lives"),
    ("England in 1819", "Percy Bysshe Shelley", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/percy-bysshe-shelley/england", "aqa-worlds-and-lives"),
    ("Shall Earth no More Inspire Thee", "Emily Brontë", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/emily-bronte/shall-earth-no-more", "aqa-worlds-and-lives"),
    ("In a London Drawingroom", "George Eliot", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/london-drawingroom-george-eliot", "aqa-worlds-and-lives"),
    ("Afternoon Train from Purley to Victoria, 1955", "James Berry", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/afternoon-train-purley", "aqa-worlds-and-lives"),
    ("Name Journeys", "Raman Mundair", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/name-journeys-raman", "aqa-worlds-and-lives"),
    ("Pot", "Shamshad Khan", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/pot-shamshad-khan", "aqa-worlds-and-lives"),
    ("A Wider View", "Seni Seneviratne", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/wider-view-seni", "aqa-worlds-and-lives"),
    ("Homing", "Liz Berry", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/homing-liz-berry", "aqa-worlds-and-lives"),
    ("A Century Later", "Imtiaz Dharker", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/imtiaz-dharker/century", "aqa-worlds-and-lives"),
    ("The Jewellery Maker", "Louisa Adjoa Parker", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/jewellery-maker-louisa-adjoa", "aqa-worlds-and-lives"),
    ("With Birds You're Never Lonely", "Raymond Antrobus", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/raymond-antrobus/birds-youre", "aqa-worlds-and-lives"),
    ("A Portable Paradise", "Roger Robinson", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/portable-paradise-roger", "aqa-worlds-and-lives"),
    ("Like an Heiress", "Grace Nichols", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/grace-nichols/heiress", "aqa-worlds-and-lives"),
    ("Thirteen", "Caleb Femi", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/thirteen-caleb-femi", "aqa-worlds-and-lives"),

    # Edexcel Belonging
    ("Captain Cook (To My Brother)", "Letitia Elizabeth Landon", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/captain-cook-my-brother-letitia", "edexcel-belonging"),
    ("Clear and Gentle Stream", "Robert Bridges", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/clear-and-gentle-stream-robert", "edexcel-belonging"),
    ("In Wales, Wanting to be Italian", "Imtiaz Dharker", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/imtiaz-dharker/wales", "edexcel-belonging"),
    ("I Remember, I Remember", "Thomas Hood", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/i-remember-i-remember-thomas", "edexcel-belonging"),
    ("Island Man", "Grace Nichols", "/a2-level-level-revision/english-literature-gcse-level/poetry/poems-other-cultures-traditions/island-man-grace-nichols", "edexcel-belonging"),
    ("Jamaican British", "Raymond Antrobus", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/raymond-antrobus/jamaican", "edexcel-belonging"),
    ("Kumukanda", "Kayo Chingonyi", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/kumukanda-kayo-chingonyi", "edexcel-belonging"),
    ("Mild the Mist Upon the Hill", "Emily Brontë", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/emily-bronte/mild-mist-upon-hill", "edexcel-belonging"),
    ("My Mother's Kitchen", "Choman Hardi", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/my-mothers-kitchen-choman", "edexcel-belonging"),
    ("Peckham Rye Lane", "K Blakemore", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/peckham-rye-lane-k-blakemore", "edexcel-belonging"),
    ("To My Sister", "William Wordsworth", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/william-wordsworth/my-sister", "edexcel-belonging"),
    ("The Emigr", "Carol Rumens", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/emigree-carol-rumens", "edexcel-belonging"),
    ("Sunday Dip", "John Clare", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/sunday-dip-john-clare", "edexcel-belonging"),
    ("Us", "Zaffar Kunial", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/us-zaffar-kunial", "edexcel-belonging"),
    ("We Refugees", "Benjamin Zephaniah", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/benjamin-zephaniah/we-refugees", "edexcel-belonging"),

    # Edexcel Conflict
    ("A Poison Tree", "William Blake", "/level-revision/english-literature-gcse-level/poetry/william-blake/poison-tree-william-blake", "edexcel-conflict"),
    ("Belfast Confetti", "Ciaran Carson", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/belfast-confetti-ciaran-carson", "edexcel-conflict"),
    ("Catrin", "Gillian Clarke", "/a2-level-level-revision/english-literature-gcse-level/poetry/gillian-clarke/catrin", "edexcel-conflict"),
    ("The Charge of the Light Brigade", "Alfred, Lord Tennyson", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/charge-light-brigade-alfred-lord", "edexcel-conflict"),
    ("The Class Game", "Mary Casey", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/class-game-mary-casey", "edexcel-conflict"),
    ("Cousin Kate", "Christina Rossetti", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/cousin-kate-christina-rossetti", "edexcel-conflict"),
    ("The Destruction of Sennacherib", "Lord Byron", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/lord-byron/destruction", "edexcel-conflict"),
    ("Exposure", "Wilfred Owen", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/exposure-wilfred-owen", "edexcel-conflict"),
    ("Half-Caste", "John Agard", "/a2-level-level-revision/english-literature-gcse-level/poetry/poems-other-cultures-traditions/half-caste-john-agard", "edexcel-conflict"),
    ("The Man He Killed", "Thomas Hardy", "/a2-level-level-revision/english-literature-gcse-level/poetry/pre-1914-poems/man-he-killed-thomas-hardy", "edexcel-conflict"),
    ("No Problem", "Benjamin Zephaniah", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/benjamin-zephaniah/no-problem", "edexcel-conflict"),
    ("Poppies", "Jane Weir", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/poppies-jane-weir", "edexcel-conflict"),
    ("The Prelude", "William Wordsworth", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/william-wordsworth/prelude", "edexcel-conflict"),
    ("War Photographer", "Carole Satyamurti", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/war-photographer-carole", "edexcel-conflict"),
    ("What Were They Like?", "Denise Levertov", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/what-were-they-denise-levertov", "edexcel-conflict"),

    # Edexcel Relationships
    ("1st Date - She", "Wendy Cope", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/1st-date-she-and-1st-date-he", "edexcel-relationships"),
    ("A Child to his Sick Grandfather", "Joanna Baillie", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/child-his-sick-grandfather", "edexcel-relationships"),
    ("A Complaint", "William Wordsworth", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/william-wordsworth/complaint", "edexcel-relationships"),
    ("i wanna be yours", "John Cooper Clarke", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/i-wanna-be-yours-john-cooper", "edexcel-relationships"),
    ("La Belle Dame Sans Merci", "John Keats", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/john-keats/la-belle-dame-sans", "edexcel-relationships"),
    ("Love's Dog", "Jen Hadfield", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/loves-dog-jen-hadfield", "edexcel-relationships"),
    ("Nettles", "Vernon Scannell", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/nettles-vernon-scannell", "edexcel-relationships"),
    ("Neutral Tones", "Thomas Hardy", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/thomas-hardy/neutral-tones", "edexcel-relationships"),
    ("The Manhunt", "Simon Armitage", "/level-revision/english-literature-gcse-level/poetry/simon-armitage/manhunt-simon-armitage", "edexcel-relationships"),
    ("My Father Would Not Show Us", "Ingrid de Kok", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/my-father-would-not-show-us", "edexcel-relationships"),
    ("My Last Duchess", "Robert Browning", "/a2-level-level-revision/english-literature-gcse-level/poetry/pre-1914-poems/my-last-duchess-robert-browning", "edexcel-relationships"),
    ("One Flesh", "Elizabeth Jennings", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/elizabeth-jennings/one-flesh", "edexcel-relationships"),
    ("She Walks in Beauty", "Lord Byron", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/lord-byron/she-walks-beauty-lord", "edexcel-relationships"),
    ("Sonnet 43", "Elizabeth Barrett Browning", "/level-revision/english-literature-gcse-level/poetry/elizabeth-barrett-browning/sonnet-43-elizabeth", "edexcel-relationships"),
    ("Valentine", "Carol Ann Duffy", "/level-revision/english-literature-gcse-level/poetry/carol-ann-duffy/valentine-carol-ann-duffy", "edexcel-relationships"),

    # Edexcel Time and Place
    ("Absence", "Elizabeth Jennings", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/elizabeth-jennings/absence", "edexcel-time-and-place"),
    ("Adlestrop", "Edward Thomas", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/adlestrop-edward-thomas", "edexcel-time-and-place"),
    ("Composed upon Westminster Bridge", "William Wordsworth", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/william-wordsworth/composed-upon", "edexcel-time-and-place"),
    ("First Flight", "U. A. Fanthorpe", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/first-flight-u-fanthorpe", "edexcel-time-and-place"),
    ("Home Thoughts, from Abroad", "Robert Browning", "/a2-level-level-revision/english-literature-gcse-level/poetry/robert-browning/home-thoughts-abroad", "edexcel-time-and-place"),
    ("Hurricane Hits England", "Grace Nichols", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/grace-nichols/hurricane", "edexcel-time-and-place"),
    ("In Romney Marsh", "John Davidson", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/romney-marsh-john-davidson", "edexcel-time-and-place"),
    ("I Started Early - Took my Dog", "Emily Dickinson", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/i-started-early-took-my-dog", "edexcel-time-and-place"),
    ("London", "William Blake", "/a2-level-level-revision/english-literature-gcse-level/poetry/william-blake/london", "edexcel-time-and-place"),
    ("Nothing's Changed", "Tatamkhulu Afrika", "/a2-level-level-revision/english-literature-gcse-level/poetry/poems-other-cultures-traditions/nothings-changed-tatamkhulu-afrika", "edexcel-time-and-place"),
    ("Postcard from a Travel Snob", "Sophie Hannah", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/postcard-travel-snob-sophie", "edexcel-time-and-place"),
    ("Presents from my Aunts in Pakistan", "Moniza Alvi", "/level-revision/english-literature-gcse-level/poetry/poems-other-cultures/presents-my-aunts-pakistan", "edexcel-time-and-place"),
    ("Stewart Island", "Fleur Adcock", "/level-revision/english-literature-gcse-level/poetry/post-1914-poems/stewart-island-fleur-adcock", "edexcel-time-and-place"),
    ("To Autumn", "John Keats", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/john-keats/autumn-john-keats", "edexcel-time-and-place"),
    ("Where the Picnic Was", "Thomas Hardy", "/level-revision/english-literature-gcse-level/poetry/pre-1914-poems/thomas-hardy/where-picnic-was", "edexcel-time-and-place"),
]


# Stop markers — when we see these, the poem text has ended and analysis begins
STOP_MARKERS = [
    "<strong>analysis", "<strong>structure", "<strong>themes",
    "<strong>language", "<strong>form", "<strong>context",
    "<strong>tone", "<strong>meaning", "<strong>summary",
    "<strong>commentary", "<strong>key", "<strong>about",
    "<strong>poem analysis", "<h2", "<h3",
]


def slugify(s: str) -> str:
    s = s.lower().strip()
    # Strip leading "the " for cleaner slugs (optional)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (StudyVault audit)"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_html(s: str) -> str:
    """Convert <br> to \\n, decode entities, strip remaining tags."""
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</p>", "\n\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", "", s)
    s = html_lib.unescape(s)
    s = s.replace("\xa0", " ")
    return s


def normalise(s: str) -> str:
    """Normalise quotes/dashes/accents for matching."""
    repl = {
        "'": "'", "'": "'", "‘": "'", "’": "'",
        '"': '"', '"': '"', "“": '"', "”": '"',
        "—": "-", "–": "-", "‐": "-", "−": "-",
        "é": "e", "è": "e", "ê": "e", "É": "E", "È": "E",
        "ó": "o", "ô": "o", "ö": "o",
        "&apos;": "'", "&#39;": "'", "&rsquo;": "'", "&lsquo;": "'",
        "&mdash;": "-", "&ndash;": "-",
        "&amp;": "&", "&quot;": '"',
    }
    out = s
    for k, v in repl.items():
        out = out.replace(k, v)
    return out.lower()


def extract_poem_body(html: str, title: str, poet: str) -> str | None:
    """Find the poem text within the HTML using ORIGINAL-position regexes
    (not normalised) so slicing offsets stay valid."""
    # Build patterns with character classes that tolerate quote/dash variants.
    def relaxed(s: str) -> str:
        # Escape regex metachars, then loosen quotes / dashes / spaces
        out = re.escape(s)
        out = out.replace(r"\ ", r"[\s\xa0&nbsp;]+")
        out = (out.replace(r"'", r"['’‘&#39;&apos;]")
                  .replace(r"\-", r"[\-—–&mdash;&ndash;]")
                  .replace(r"\.", r"\.?"))  # title may or may not have period
        return out

    title_pat = relaxed(title)
    poet_pat = relaxed(poet)

    patterns = [
        re.compile(r"<strong>\s*" + title_pat + r"\s*by\s*" + poet_pat + r"[\s\.&;a-z\xa0]*</strong>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<strong>\s*" + title_pat + r"\s*</strong>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<b>\s*" + title_pat + r"\s*by\s*" + poet_pat + r"[\s\.&;a-z\xa0]*</b>", re.IGNORECASE | re.DOTALL),
    ]

    marker_pos = None
    for pat in patterns:
        m = pat.search(html)
        if m:
            marker_pos = m.end()
            break

    if marker_pos is None:
        # Fallback: any <strong>...</strong> that contains title-prefix + poet surname
        title_lower = title.lower()
        poet_lower = poet.lower()
        title_prefix = re.split(r"[\(\"\']", title_lower)[0].strip()[:25]
        poet_surname = poet_lower.split()[-1]
        for m in re.finditer(r"<strong>([^<]{1,300})</strong>", html, re.IGNORECASE):
            content = m.group(1).lower()
            if title_prefix in content and poet_surname in content:
                marker_pos = m.end()
                break

    if marker_pos is None:
        return None

    # Find stop marker AFTER the title (case-insensitive search in original html)
    html_lower = html.lower()
    stop_pos = len(html)
    for stop in STOP_MARKERS:
        i = html_lower.find(stop, marker_pos)
        if i != -1 and i < stop_pos:
            stop_pos = i

    raw = html[marker_pos:stop_pos]

    # Convert to plain text
    text = strip_html(raw)

    # Clean up: collapse runs of >2 newlines to exactly 2; trim
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    return text


def main():
    OUT_BASE.mkdir(parents=True, exist_ok=True)
    for cluster in {p[3] for p in POEMS}:
        (OUT_BASE / cluster).mkdir(parents=True, exist_ok=True)

    ok = []
    failed = []
    for i, (title, poet, path, anth) in enumerate(POEMS, 1):
        url = BASE_URL + path
        try:
            html = fetch(url)
        except Exception as e:
            print(f"  [{i:3d}/{len(POEMS)}] FAIL fetch — {anth}/{title}: {e}")
            failed.append((title, poet, anth, "fetch error"))
            continue

        body = extract_poem_body(html, title, poet)
        if not body or len(body) < 30:
            print(f"  [{i:3d}/{len(POEMS)}] FAIL parse — {anth}/{title}")
            failed.append((title, poet, anth, "parse error"))
            continue

        slug = slugify(title)
        out_path = OUT_BASE / anth / f"{slug}.txt"
        out_path.write_text(
            f"# {title}\n# {poet}\n\n{body}\n",
            encoding="utf-8",
        )
        line_count = len([L for L in body.split("\n") if L.strip()])
        print(f"  [{i:3d}/{len(POEMS)}] OK   {anth}/{slug:50s} ({line_count} lines)")
        ok.append((title, poet, anth))

        # Be polite to the server
        time.sleep(0.4)

    print(f"\n{len(ok)} OK, {len(failed)} failed")
    for t, p, a, why in failed:
        print(f"  FAIL  {a}/{t} — {why}")


if __name__ == "__main__":
    main()
