import json, io
changes = {
    "key": "ratio-proportion-L03",
    "problems_fixed": [
        {"tier":"bronze","index":6,"what":"Retuned so its answer no longer duplicates B4 (both were 5). Kept it a bronze speed problem.","old":"A runner covers 400 m in 80 seconds -> 5 m/s","new":"A runner covers 420 m in 60 seconds -> 7 m/s"},
        {"tier":"bronze","index":7,"what":"Replaced duplicate Pressure=Force/Area problem (audit duplicate B4/B7) with a bronze formula-rearrangement (Force=Pressure x Area).","old":"A box weighs 90 N on 0.3 m^2 -> pressure 300 N/m^2","new":"A pressure of 8 N/m^2 acts over an area of 6 m^2 -> force 48 N"}
    ],
    "issues_resolved": 4,
    "opener_concept": "Sharing by division: 60 miles over 2 hours (miles per hour) and 12 kg over 3 tiles (kg per tile). Both are pure common-sense division, revealed as speed and pressure; all three compound measures are one total divided by how many units.",
    "notes": "Audit issues: (1) bronze bad_misconception_message and (2) silver bad_misconception_message -> every misconception message rewritten to NAME the student's likely error (multiply-vs-divide, formula inversion, unit-conversion direction, averaging speeds/densities) before showing the correct working; expects recomputed and verified to reproduce each error and to differ from the solution. (3) bronze B4/B7 duplicate skill -> B7 rebuilt as a Force=Pressure x Area rearrangement. (4) gold[2] display_error (6.32 alongside 6.3): live data already carried only [6.3], so no change needed. Also fixed a latent validator failure: bronze B4 and B6 both had solution 5 (duplicate values within tier) -> B6 retuned to 7. Removed em dashes from preserved method_card content and worked_examples labels ('Step 1 -' -> 'Step 1:'). Added top-level plain-text hint to all 20 bank problems. Added guided.opener, guided.teach (bronze/silver/gold, all problems outside the bank), tier_guides, tier descriptions, and guided_steps with a phase:'substitute' completion boundary on every bank problem. method_card slimmed to the section-8 budget. topic_links and related_videos preserved byte-for-byte. Validator PASS; PATCH returned 204 and readback is byte-identical."
}
json.dump(changes, io.open("changes_ratio-proportion-L03.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote changes file")
