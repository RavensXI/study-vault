# -*- coding: utf-8 -*-
"""Apply the checker findings by hand.

The fan-out's repair agents died on the session limit, but every finding was
specific enough to fix directly. Run with --apply to write the live rows.

L08 is the substantive one: two walks made contradictory claims about the same
point on isotherm-uk.png. I fetched and read that map, which neither the author
nor the checker could do. It carries ONLY 4/6/8 degree isotherms, Q sits between
4 and 6 (=5), and P sits SOUTH of the 8 line with no line beyond it. So:
  - bronze[2] invented a 10 degree line to estimate P as 9, then "checked" its
    answer against that same assumption. Rewritten to reason from the printed
    lines only, and to say plainly that P cannot be given a single number.
  - silver[5] placed P between 6 and 8 to make the stored difference of 2 come
    out. That contradicts bronze[2] and the map. Since P has no upper bound,
    the difference is not determinate, so the question is reposed to ask for the
    smallest possible difference (= 3), which is answerable and teaches that
    isolines give you bounds, not exact values.
"""
import io, json, os, sys

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
APPLY = "--apply" in sys.argv
log = []


def load(k):
    return json.load(io.open(os.path.join(HERE, "lesson_%s.json" % k), encoding="utf-8"))


def save(k, pd):
    io.open(os.path.join(HERE, "lesson_%s.json" % k), "w", encoding="utf-8").write(
        json.dumps(pd, ensure_ascii=False, indent=1))


def note(k, path, what):
    log.append((k, path, what))


# ---------------------------------------------------------------- L01
pd = load("L01")
m = pd["problem_bank"]["silver"][4]["misconceptions"][1]
m["pattern"] = "picked_the_smallest_fall"
m["message"] = ("That pair changes least of all, so it is the smallest fall rather "
                "than the biggest. Work out the size of every drop offered, then compare them.")
note("L01", "silver[4].misconceptions[1]",
     "message described 'picked the lowest point', which produces a different option; "
     "rewritten to describe the error that actually lands on this expect")

m = pd["problem_bank"]["silver"][0]["misconceptions"][1]
m["message"] = ("October does show a clear gap, but it is not the widest one offered. "
                "Measure the vertical distance between the two lines for each month in "
                "the list, then compare all four.")
note("L01", "silver[0].misconceptions[1]",
     "removed 'check the winter months', which uniquely identified the only winter option")
save("L01", pd)

# ---------------------------------------------------------------- L02
pd = load("L02")
m = pd["problem_bank"]["silver"][5]["misconceptions"][0]
m["expect"] = [2]
note("L02", "silver[5].misconceptions[0]",
     "expect 5 is not a printed axis value and IS the frequency of two real bars, so it "
     "misdiagnosed a plain misread; set to 2, the modal class width the message describes")
save("L02", pd)

# ---------------------------------------------------------------- L04
pd = load("L04")
m = pd["problem_bank"]["bronze"][5]["misconceptions"][0]
m["pattern"] = "read_base_as_wide"
m["message"] = ("This pyramid has a narrow base, so few children are coming through. "
                "Look again at which part of the pyramid is widest, and work out how old "
                "that group will be in twenty years.")
note("L04", "bronze[5].misconceptions[0]",
     "ageing the base gives young adults, not schoolchildren, so the old message accused "
     "the student of an error they had not made; rewritten to match this expect")

m = pd["problem_bank"]["silver"][6]["misconceptions"][1]
m["message"] = ("Women live longer than men almost everywhere, so this is not about women "
                "dying young. Notice the gap sits in one working age band only, and ask "
                "what could change the make up of just that band.")
note("L04", "silver[6].misconceptions[1]", "removed 'points at people arriving', which restated the correct option")

m = pd["problem_bank"]["silver"][4]["misconceptions"][1]
m["message"] = ("Migration in old age is rare and small, so it cannot account for a gap "
                "this size. Look at how the gap changes as you move further up the "
                "pyramid before choosing.")
note("L04", "silver[4].misconceptions[1]", "removed 'points at survival', which restated the correct option")
save("L04", pd)

# ---------------------------------------------------------------- L06
pd = load("L06")
st = pd["guided"]["teach"]["silver"]["steps"][6]
if "Q1 of that half" in st.get("pre", ""):
    st["pre"] = st["pre"].replace("Give Q1 of that half in the same way, which is Q3.",
                                  "Give the median of that half, which is Q3.")
    note("L06", "guided.teach.silver.steps[6]",
         "prompt asked for Q1 of the upper half but the stored answer is its median (the "
         "correct Q3); instruction renamed to match the maths")
else:
    note("L06", "guided.teach.silver.steps[6]", "SKIPPED: expected wording not found")
save("L06", pd)

# ---------------------------------------------------------------- L07
pd = load("L07")
p = pd["problem_bank"]["gold"][4]
if "decimal place" not in p["display"]:
    p["display"] = p["display"].rstrip() + " Give your answer to 1 decimal place."
    note("L07", "gold[4].display",
         "exact value is 20.8333..., stored 20.8, and the player matches within 0.01, so a "
         "student typing the mathematically correct 20.83 was marked wrong; precision now stated")
else:
    note("L07", "gold[4].display", "SKIPPED: precision already stated")
save("L07", pd)

# ---------------------------------------------------------------- L08
pd = load("L08")

b2 = pd["problem_bank"]["bronze"][2]
b2["guided_steps"] = [
    {"say": "First place P against the printed lines, then work out which way the numbers run."},
    {"pre": "Type the value, in °C, of the isotherm that P sits just south of.",
     "answer": 8, "hint": "The question names it, and the label is printed on the line."},
    {"pre": "The isotherms on this map are labelled 4, 6 and 8. Type the gap, in °C, between one isotherm and the next.",
     "answer": 2, "hint": "Subtract one label from the next label along."},
    {"pre": "The 4°C line lies furthest north and the values rise going south. Type the value of the warmest isotherm printed on this map, in °C.",
     "answer": 8, "hint": "Look for the largest label on the map.", "phase": "substitute"},
    {"pre": "Check: type how many printed isotherms on this map are warmer than the line P sits south of.",
     "answer": 0, "hint": "Count the labels larger than 8.",
     "done": "None. P is beyond the warmest line the map draws."},
    {"say": "P is on the warm side of the warmest line printed, so P is <strong>warmer than 8°C</strong>. "
            "Because the map draws no line past 8°C, you can say which side of the line P is on but you cannot "
            "give P a single number."},
]
note("L08", "bronze[2].guided_steps",
     "walk invented a 10°C isotherm (the map has only 4, 6, 8), estimated P as 9 from it, then "
     "'checked' that estimate against the same assumption; rewritten to use printed lines only "
     "and to state honestly that P cannot be pinned to one value")

s5 = pd["problem_bank"]["silver"][5]
s5["display"] = ("Point P in southern England lies south of the 8°C isotherm, and Point Q in central "
                 "Scotland sits midway between the 4°C and 6°C isotherms. Using the isotherm map, what "
                 "is the smallest possible temperature difference between P and Q, in °C?")
s5["solutions"] = [3]
s5["hint"] = "Estimate Q exactly first, then use the coolest temperature P could possibly be."
s5["guided_steps"] = [
    {"say": "Estimate Q exactly, then work out the least P could be."},
    {"pre": "Type the value, in °C, of the cooler isotherm Q sits between.",
     "answer": 4, "hint": "Trace north from Q to the first printed line."},
    {"pre": "Type the value, in °C, of the warmer isotherm Q sits between.",
     "answer": 6, "hint": "Trace south from Q to the next printed line."},
    {"pre": "Q sits midway between them. Type your estimate for Q, in °C.",
     "answer": 5, "hint": "Add half the gap to the cooler line.", "phase": "substitute"},
    {"pre": "P lies south of the 8°C line, so P is warmer than 8. Type the lowest whole temperature P could be, in °C.",
     "answer": 8, "hint": "P cannot be cooler than the line it sits south of."},
    {"pre": "Take your estimate for Q away from that lowest value for P. Type the smallest possible difference, in °C.",
     "answer": 3, "hint": "Subtract the smaller value from the larger one."},
    {"pre": "Check: add that difference back onto your estimate for Q. Type the result, in °C.",
     "answer": 8, "hint": "A correct difference must rebuild the lowest value for P.",
     "done": "It rebuilds 8, so the difference is right. P could be warmer still, which is why this is the smallest possible difference."},
]
s5["misconceptions"] = [
    {"pattern": "subtracted_line_labels", "expect": 4,
     "message": "You subtracted two printed labels instead of using your estimate for Q. "
                "Estimate Q from its band first, then compare it with the lowest value P could take.",
     "note": "8 minus 4"},
    {"pattern": "added_instead_of_subtracted", "expect": 13,
     "message": "Those two values were added together. A difference is found by taking the "
                "smaller value away from the larger one.",
     "note": "5 plus 8"},
]
note("L08", "silver[5]",
     "walk placed P between the 6 and 8 isotherms to make the stored difference of 2 come out, "
     "contradicting bronze[2] and the map (P is SOUTH of 8, which is the warmest line drawn). "
     "P has no upper bound, so the difference is not determinate: question reposed to ask the "
     "smallest possible difference (3), which the map does answer")
save("L08", pd)

# ---------------------------------------------------------------- report
print("REPAIRS")
for k, path, what in log:
    print("  %-4s %-32s %s" % (k, path, what))
print("\n%d repairs written to lesson_*.json" % len(log))

if APPLY:
    import urllib.request
    KEY = os.environ["SUPABASE_SERVICE_KEY"]
    wl = {w["key"]: w["id"] for w in json.load(
        io.open(os.path.join(HERE, "_worklist.json"), encoding="utf-8"))}
    for k in sorted(set(x[0] for x in log)):
        pd = load(k)
        url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % wl[k]
        r = urllib.request.Request(
            url, data=json.dumps({"practice_data": pd}).encode("utf-8"),
            headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                     "Content-Type": "application/json", "Prefer": "return=minimal"},
            method="PATCH")
        urllib.request.urlopen(r, timeout=90)
        print("PATCHED", k)
else:
    print("(dry run: pass --apply to write the live rows)")
