"""Shared harness for the Jev (TypeSafe System One) experiments, 19 Sep 2026.

    from jev import ask, ledger, Choice, Score, Noul
    r = ask(state, {"q": Noul(instructions="...")})      # -> SystemOneResponse
    r.answers["q"].noul

Every call is logged to _ledger.jsonl (tokens, latency, experiment tag) so the night's
spend can be totted up: $0.042 per million input tokens, output free. Budget $3.
The key is Tom's user-level env var JEV_API_KEY (this shell predates it, so read the
registry when the process env lacks it).
"""
import io, json, os, sys, time, threading, winreg
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typesafe_sdk import TypeSafeClient, Choice, Score, Noul, RetryPolicy  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "_ledger.jsonl")
PRICE_PER_M = 0.042
BUDGET_USD = 3.0
_lock = threading.Lock()

def _key():
    k = os.environ.get("JEV_API_KEY") or os.environ.get("TYPESAFE_API_KEY")
    if k: return k
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as h:
        return winreg.QueryValueEx(h, "JEV_API_KEY")[0]

_client = None
def client():
    global _client
    if _client is None:
        _client = TypeSafeClient(api_key=_key(), retry=RetryPolicy(max_retries=4, backoff_max=8.0), timeout=60.0)
    return _client

def spent():
    """(usd, input_tokens, calls) so far across the night."""
    usd = toks = n = 0
    if os.path.exists(LEDGER):
        for line in io.open(LEDGER, encoding="utf-8"):
            try: r = json.loads(line)
            except Exception: continue
            toks += r.get("input_tokens", 0); n += 1
    return toks / 1e6 * PRICE_PER_M, toks, n

def ask(state, questions, tag="adhoc", model=None):
    usd, _, _ = spent()
    if usd >= BUDGET_USD:
        raise RuntimeError("Jev budget reached: $%.2f" % usd)
    t0 = time.time()
    r = client().system_one(state=state, questions=questions, model=model)
    dt = time.time() - t0
    u = getattr(r, "usage", None)
    toks = 0
    if u is not None:
        d = u.model_dump() if hasattr(u, "model_dump") else dict(u)
        toks = d.get("input_tokens") or d.get("prompt_tokens") or d.get("total_tokens") or 0
    with _lock:
        with io.open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps({"t": time.time(), "tag": tag, "input_tokens": toks, "ms": round(dt * 1000), "nq": len(questions)}) + "\n")
    return r

def ask_many(items, build, tag, workers=8):
    """items -> list of (item, response|None, error|None). build(item) -> (state, questions)."""
    def one(it):
        try:
            s, q = build(it)
            return (it, ask(s, q, tag=tag), None)
        except Exception as e:
            return (it, None, repr(e)[:200])
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(one, items))

def answers(r):
    """plain dict of the answers: {name: {choice|score|noul, confidence, probabilities}}"""
    out = {}
    for k, a in r.answers.items():
        d = a.model_dump() if hasattr(a, "model_dump") else dict(a)
        out[k] = d
    return out

def sb_get(path):
    import urllib.request
    U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    req = urllib.request.Request(U + "/rest/v1/" + path, headers={"apikey": K, "Authorization": "Bearer " + K})
    return json.loads(urllib.request.urlopen(req, timeout=180).read())

def sb_all(path, page=1000):
    out, off = [], 0
    sep = "&" if "?" in path else "?"
    while True:
        rows = sb_get(path + sep + "limit=%d&offset=%d" % (page, off))
        out += rows
        if len(rows) < page: return out
        off += page

def save(name, obj):
    p = os.path.join(HERE, "_results", name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8").write(json.dumps(obj, indent=1, ensure_ascii=False))
    return p
