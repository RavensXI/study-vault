"""Write the pupil answers behind the demo class's marked work.

scripts/_demo_class_history.py decides who wrote what and what mark the marker
gave it. This fills in the missing half: the answer itself, in a Year 11 voice,
at the quality that mark implies. Those answers are what the teacher screen's
weekly read quotes back ("what keeps coming up"), so template prose would show
straight away — every one is written against its own question.

Sonnet on the Batch API: this is synthetic pupil writing for a demo school, not
content a real student reads, so it is not an Opus job.

    python scripts/_demo_class_answers.py --submit      # send the batch
    python scripts/_demo_class_answers.py --collect ID  # fetch and save
"""
import io, json, os, sys, time
import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.join(HERE, "_demo_class_answer_specs.json")
OUT = os.path.join(HERE, "_demo_class_history_answers.json")
STATE = os.path.join(HERE, "_demo_class_answers_batch.json")
MODEL = "claude-sonnet-5"

SYSTEM = (
    "You write GCSE History answers as a Year 11 pupil would really write them, for a "
    "demonstration dataset. British English. No preamble, no headings, no mark scheme "
    "language, no self-commentary: only the answer itself, as the pupil typed it.\n\n"
    "The mark the answer was given is your brief. Write an answer that would honestly earn "
    "exactly that mark:\n"
    "  under 40% - short, mostly narrative or assertion, little or no specific detail, "
    "may drift off the question or answer a simpler version of it.\n"
    "  40-65% - relevant and mostly accurate with some specific support, but the points sit "
    "side by side without being weighed, and the conclusion is asserted rather than argued.\n"
    "  65-85% - two or three developed points with precise detail, a clear line of argument, "
    "a judgement that is explained but could go further.\n"
    "  over 85% - sustained argument, precise support, explicit weighing of factors, a "
    "judgement that answers the actual question.\n\n"
    "Pupil habits are what make this useful: a dropped date, a name half-remembered, one "
    "paragraph much stronger than the next, 'this shows that' used too often, a first "
    "sentence that restates the question. Use them at the weaker marks. Never use bullet "
    "points. Never mention marks, bands or the examiner."
)


def prompt(s):
    return (
        "QUESTION (%s, %s):\n%s\n\nTOPIC: %s\n\nTHE MARKER GAVE THIS ANSWER %d out of %d.\n\n"
        "Write that answer. %s words."
        % (s["type"], "AQA GCSE History", s["q"], s["unit"], s["got"], s["of"],
           "60 to 110" if s["of"] <= 8 else "130 to 220")
    )


def main():
    specs = json.load(io.open(SPECS, encoding="utf-8"))
    cl = anthropic.Anthropic()
    if "--submit" in sys.argv:
        reqs = [{"custom_id": "a%04d" % i,
                 "params": {"model": MODEL, "max_tokens": 900,
                            "system": SYSTEM,
                            "messages": [{"role": "user", "content": prompt(s)}]}}
                for i, s in enumerate(specs)]
        batch = cl.messages.batches.create(requests=reqs)
        io.open(STATE, "w", encoding="utf-8").write(json.dumps({"id": batch.id, "n": len(reqs)}))
        print("submitted", batch.id, len(reqs), "answers")
        return
    bid = (sys.argv[sys.argv.index("--collect") + 1] if "--collect" in sys.argv
           else json.load(io.open(STATE, encoding="utf-8"))["id"])
    b = cl.messages.batches.retrieve(bid)
    print("status:", b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    out = json.load(io.open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    n = 0
    for r in cl.messages.batches.results(bid):
        if r.result.type != "succeeded":
            print("  failed:", r.custom_id, r.result.type)
            continue
        i = int(r.custom_id[1:])
        text = "".join(bl.text for bl in r.result.message.content if bl.type == "text").strip()
        if not text:
            continue
        out[specs[i]["id"]] = text
        n += 1
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
    print("saved", n, "answers to", OUT)


if __name__ == "__main__":
    main()
