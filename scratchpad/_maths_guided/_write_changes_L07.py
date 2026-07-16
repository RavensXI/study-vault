import json, io
disp = {
 "bronze":["x^2+5x+6=0","x^2+7x+10=0","x^2+8x+15=0","x^2+6x+8=0","x^2+9x+14=0","x^2+10x+21=0","x^2+11x+24=0","x^2+3x+2=0"],
 "silver":["x^2-3x-10=0","x^2+2x-15=0","x^2-x-12=0","x^2-7x+12=0","x^2-2x-8=0","x^2+x-20=0","x^2-9=0"],
 "gold":["x^2=5x-6","2x^2+6x=0","x^2-4x=5","3x^2-12x=0","x^2+x=6"],
}
pf=[]
for tier in ("bronze","silver","gold"):
    for i,d in enumerate(disp[tier]):
        dots = (tier=="silver" and d=="x^2-9=0")
        what=("removed bogus not_rearranged misconception; "
              + ("dropped the sign misconception (difference of two squares: negating gives the same unordered pair, no determinate distinct error); "
                 if dots else
                 "merged duplicate sign_swap + factors_not_solutions (identical expect) into one 'factor_pair_not_solved' entry; ")
              + "added guided_steps walk, per-problem hint")
        old=("misconceptions: [sign_swap, factors_not_solutions, one_correct, not_rearranged]; no hint; no guided_steps"
             if tier!="gold" else
             "misconceptions: [sign_swap, factors_not_solutions, one_correct, not_rearranged]; no guided_steps")
        new=("misconceptions: [one_correct]" if dots else "misconceptions: [factor_pair_not_solved, one_correct]") + "; hint added; guided_steps added"
        pf.append({"tier":tier,"index":i,"what":what,"old":old,"new":new})
out={
 "key":"algebra-L07",
 "problems_fixed":pf,
 "issues_resolved":2,
 "opener_concept":"Two common-sense number puzzles: (1) 'two numbers that multiply to 12 and add to 7' names factorising; (2) '5 times something = 0' names the zero product rule. Together they are the whole method.",
 "notes":"All 20 stored solutions were fresh-solved and already correct; no numeric/answer repairs needed. Both filed audit issues fixed across the whole bank: (1) duplicate sign_swap/factors_not_solutions merged (they produced identical wrong answers), (2) bogus not_rearranged removed everywhere (expect was always null so it never fired, and its message was factually wrong on bronze/silver and on the factor-out golds). input_type kept as two_solutions (unordered pair). Completion boundary (phase:substitute) set so the factor pair / brackets are pre-worked and the student applies the zero product rule (2+ live boxes) then checks. Style repair: em dashes in preserved worked_examples step labels replaced with colons to pass the no-em-dash gate. related_videos, topic_links preserved byte-for-byte; method_card slimmed to <140 words."
}
json.dump(out, io.open("changes_algebra-L07.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote changes_algebra-L07.json;", len(pf), "problems listed")
