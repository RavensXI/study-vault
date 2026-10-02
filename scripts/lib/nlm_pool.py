"""
The shared Gemini Notebook (NotebookLM) allowance: how much the shorts may launch right now.

Since 11 Sep 2026 Google meters ONE pool shared by every video and audio job, refilled over a
rolling 5-hour window, with a weekly limit on top. Nothing reports the meter to us, so this
ledger reconstructs it from our own launch records and LEARNS the two limits from Google's
answers:

  * every create we fire is an event (kind, time) — shorts write here directly; explainers and
    podcasts are read from their own state files in the main checkout (launched_ts);
  * costs are in SHORT-EQUIVALENTS, from Tom's meter readings of 11 Sep 2026 (settings page %):
      window: short 1.65%, explainer 2.2%, podcast ~2%   -> short 1.0, explainer 1.33, podcast 1.2
      week:   5 explainers = 1%, 20 shorts = 2%          -> short 1.0, explainer 2.0,  podcast 1.5
  * budget now = min(window_cap - used in last 5 h,
                     day_pace   - used in last 24 h,       day_pace = week_cap / 7 (no stalls)
                     week_cap   - used in last 7 days)
  * learning:  RESOURCE_EXHAUSTED or a job Google has not started 90 min after launch is a
    "limit" signal. If it comes while the window is well used, the WINDOW cap was the limit and
    shrinks to what fitted; if it comes while the window is lightly used, the WEEKLY cap was the
    limit and shrinks to the week's use. A clean day in which the pace was used in full raises
    both caps a little, so they climb back to Google's real limits and stay just under them.

State: scripts/_nlm_pool.json (caps, our events, signals). Small; pruned to 8 days.
"""
import json
import os
import time

MAIN_SCRIPTS = r"C:\Users\tshau\Documents\Study Vault\scripts"               # explainer + podcast state live here
# ONE ledger for every stream (3 Oct 2026): the platform explainer job and the sandbox shorts job both
# import a copy of this module, so the state lives at a fixed path in the main checkout, never beside
# whichever copy was imported (it used to live in the sandbox worktree, which only the shorts read).
STATE = os.path.join(MAIN_SCRIPTS, "_nlm_pool.json")
OTHER_STREAMS = {"explainer": os.path.join(MAIN_SCRIPTS, "_batch_explainer_state.json"),
                 "podcast": os.path.join(MAIN_SCRIPTS, "_batch_podcast_state.json")}

WINDOW_S, DAY_S, WEEK_S = 5 * 3600, 24 * 3600, 7 * 24 * 3600
COST_WINDOW = {"short": 1.0, "explainer": 1.33, "podcast": 1.2}
COST_WEEK = {"short": 1.0, "explainer": 2.0, "podcast": 1.5}

# Starting caps (short-equivalents). The meter test put a window at ~60 shorts and the week at
# ~1,000; start a little under both and let the signals move them.
DEFAULTS = {"window_cap": 48.0, "week_cap": 900.0}
WINDOW_MIN, WINDOW_MAX = 16.0, 80.0
WEEK_MIN, WEEK_MAX = 300.0, 1600.0


def _load():
    try:
        with open(STATE, encoding="utf-8") as f:
            s = json.load(f)
    except (OSError, ValueError):
        s = {}
    s.setdefault("window_cap", DEFAULTS["window_cap"])
    s.setdefault("week_cap", DEFAULTS["week_cap"])
    s.setdefault("events", [])        # [{ts, kind}] our own launches (shorts)
    s.setdefault("signals", [])       # [{ts, what, window_used, week_used, note}]
    s.setdefault("last_grow", 0)
    return s


def _save(s):
    cutoff = time.time() - 8 * DAY_S
    s["events"] = [e for e in s["events"] if e["ts"] >= cutoff]
    s["signals"] = [g for g in s["signals"] if g["ts"] >= cutoff][-200:]
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=1)
    os.replace(tmp, STATE)


def _other_events(since):
    out = []
    for kind, path in OTHER_STREAMS.items():
        try:
            with open(path, encoding="utf-8") as f:
                jobs = (json.load(f) or {}).get("jobs", [])
        except (OSError, ValueError):
            continue
        out += [{"ts": j["launched_ts"], "kind": kind} for j in jobs if (j.get("launched_ts") or 0) >= since]
    return out


def usage(now=None):
    """Short-equivalents used in the last 5 h, 24 h and 7 days, across all three streams."""
    now = now or time.time()
    s = _load()
    events = [e for e in s["events"] if e["ts"] >= now - WEEK_S] + _other_events(now - WEEK_S)
    win = sum(COST_WINDOW[e["kind"]] for e in events if e["ts"] >= now - WINDOW_S)
    day = sum(COST_WEEK[e["kind"]] for e in events if e["ts"] >= now - DAY_S)
    week = sum(COST_WEEK[e["kind"]] for e in events)
    return {"window": win, "day": day, "week": week}


def budget():
    """How many SHORTS may launch now (whole number, >= 0), and the reasoning."""
    s, u = _load(), usage()
    pace = s["week_cap"] / 7.0
    room = {"window": s["window_cap"] - u["window"], "day": pace - u["day"], "week": s["week_cap"] - u["week"]}
    # a weekly-limit signal in the last 12 h holds launches: the window has not reset for that one
    held = any(g["what"] == "week" and g["ts"] >= time.time() - 12 * 3600 for g in s["signals"])
    n = 0 if held else max(0, int(min(room.values())))
    why = (f"window {u['window']:.0f}/{s['window_cap']:.0f}, day {u['day']:.0f}/{pace:.0f}, "
           f"week {u['week']:.0f}/{s['week_cap']:.0f}" + (" - HELD after a weekly-limit signal" if held else ""))
    return n, why


def explainer_budget():
    """How many EXPLAINERS may launch now (whole number, >= 0), and the reasoning (3 Oct 2026).
    Explainers keep first claim on the allowance (Tom, 10 Sep 2026: the shorts job stands aside
    while explainers have work), but they still have to fit Google's window and week, or Google
    queues them past the run's polling. An explainer costs 1.33 in the window and 2.0 in the week."""
    s, u = _load(), usage()
    pace = s["week_cap"] / 7.0
    held = any(g["what"] == "week" and g["ts"] >= time.time() - 12 * 3600 for g in s["signals"])
    room = min((s["window_cap"] - u["window"]) / COST_WINDOW["explainer"],
               (pace - u["day"]) / COST_WEEK["explainer"],
               (s["week_cap"] - u["week"]) / COST_WEEK["explainer"])
    n = 0 if held else max(0, int(room))
    why = (f"window {u['window']:.0f}/{s['window_cap']:.0f}, day {u['day']:.0f}/{pace:.0f}, "
           f"week {u['week']:.0f}/{s['week_cap']:.0f} (short-equivalents)" + (" - HELD after a weekly-limit signal" if held else ""))
    return n, why


def record_launch(kind="short", n=1):
    s = _load()
    now = time.time()
    s["events"] += [{"ts": now, "kind": kind} for _ in range(n)]
    _save(s)


def record_limit(note=""):
    """Google refused (RESOURCE_EXHAUSTED) or held a job back. Decide which limit it was and
    shrink that cap to what fitted. Returns 'window' or 'week'."""
    s, u = _load(), usage()
    if u["window"] >= 0.6 * s["window_cap"]:
        what = "window"
        s["window_cap"] = max(WINDOW_MIN, min(s["window_cap"], u["window"]) - 2)
    else:
        what = "week"
        s["week_cap"] = max(WEEK_MIN, min(s["week_cap"], u["week"]) - 10)
    s["signals"].append({"ts": time.time(), "what": what, "window_used": round(u["window"], 1),
                         "week_used": round(u["week"], 1), "note": note[:120]})
    _save(s)
    return what


def maybe_grow():
    """Once a day: if the last 24 h used the day's pace in full with no limit signal, raise the
    caps a step (window +4 = one lesson; week +5%). Returns a note, or ''."""
    s, u = _load(), usage()
    now = time.time()
    if now - s["last_grow"] < DAY_S:
        return ""
    s["last_grow"] = now
    recent = [g for g in s["signals"] if g["ts"] >= now - DAY_S]
    pace = s["week_cap"] / 7.0
    note = ""
    if not recent and u["day"] >= 0.9 * pace:
        s["window_cap"] = min(WINDOW_MAX, s["window_cap"] + 4)
        s["week_cap"] = min(WEEK_MAX, s["week_cap"] * 1.05)
        note = f"caps raised: window {s['window_cap']:.0f}, week {s['week_cap']:.0f}"
    _save(s)
    return note


def summary():
    s, u = _load(), usage()
    n, why = budget()
    return {"window_cap": s["window_cap"], "week_cap": s["week_cap"], "usage": u, "budget": n, "why": why,
            "signals_24h": [g for g in s["signals"] if g["ts"] >= time.time() - DAY_S]}


if __name__ == "__main__":
    print(json.dumps(summary(), indent=1))
