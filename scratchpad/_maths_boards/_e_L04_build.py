# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_e_L04_live.json", encoding="utf-8"))["practice_data"]

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def say(s): return {"say": s}

# ---- SVGs ----
OPENER_SVG = ('<svg viewBox="0 0 260 104" role="img" aria-label="Timeline: the 4-minute bus is due at 4, 8 and 12 minutes; the 6-minute bus at 6 and 12 minutes; they meet at 12 minutes">'
 '<text x="6" y="34" font-family="Inter, sans-serif" font-size="10" fill="currentColor">Bus 4</text>'
 '<text x="6" y="72" font-family="Inter, sans-serif" font-size="10" fill="currentColor">Bus 6</text>'
 '<line x1="44" y1="30" x2="244" y2="30" stroke="currentColor" stroke-width="1"/>'
 '<line x1="44" y1="68" x2="244" y2="68" stroke="currentColor" stroke-width="1"/>'
 '<circle cx="108" cy="30" r="5" fill="#60a5fa" fill-opacity="0.5" stroke="currentColor"/>'
 '<circle cx="172" cy="30" r="5" fill="#60a5fa" fill-opacity="0.5" stroke="currentColor"/>'
 '<circle cx="236" cy="30" r="6" fill="#34d399" fill-opacity="0.6" stroke="currentColor"/>'
 '<circle cx="140" cy="68" r="5" fill="#f59e0b" fill-opacity="0.5" stroke="currentColor"/>'
 '<circle cx="236" cy="68" r="6" fill="#34d399" fill-opacity="0.6" stroke="currentColor"/>'
 '<line x1="236" y1="30" x2="236" y2="68" stroke="#34d399" stroke-width="1.5" stroke-dasharray="2 2"/>'
 '<text x="108" y="18" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">4</text>'
 '<text x="172" y="18" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">8</text>'
 '<text x="236" y="18" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">12</text>'
 '<text x="140" y="86" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">6</text>'
 '<text x="236" y="86" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">12</text>'
 '</svg>')

VENN_SVG = ('<svg viewBox="0 0 260 150" role="img" aria-label="Venn diagram of prime factors: 18 on the left, 24 on the right; a shared 2 and 3 in the overlap, an extra 3 for 18, two extra 2s for 24">'
 '<circle cx="100" cy="82" r="62" fill="#60a5fa" fill-opacity="0.22" stroke="currentColor"/>'
 '<circle cx="160" cy="82" r="62" fill="#f59e0b" fill-opacity="0.22" stroke="currentColor"/>'
 '<text x="58" y="24" font-family="Inter, sans-serif" font-size="11" text-anchor="middle" fill="currentColor">18</text>'
 '<text x="202" y="24" font-family="Inter, sans-serif" font-size="11" text-anchor="middle" fill="currentColor">24</text>'
 '<text x="64" y="88" font-family="Inter, sans-serif" font-size="13" text-anchor="middle" fill="currentColor">3</text>'
 '<text x="130" y="74" font-family="Inter, sans-serif" font-size="12" text-anchor="middle" fill="currentColor">2</text>'
 '<text x="130" y="94" font-family="Inter, sans-serif" font-size="12" text-anchor="middle" fill="currentColor">3</text>'
 '<text x="196" y="88" font-family="Inter, sans-serif" font-size="13" text-anchor="middle" fill="currentColor">2, 2</text>'
 '</svg>')

# ================= BRONZE =================
bronze = [
 # B1 factors of 24 -> 8
 {"hint": "List them in factor pairs: 1 x 24, 2 x 12, 3 x 8, 4 x 6, then count.",
  "misc": [{"pattern": "exclude_ends", "expect": 6, "message": "Count 1 and the number itself too. 1, 2, 3, 4, 6, 8, 12, 24 gives 8 factors.", "note": "drop 1 and 24: 6"}],
  "steps": [
    say("Factors come in pairs that multiply to 24. Find each pair."),
    box("3 x ? = 24, so ? = ", 8, "24 divided by 3."),
    box("4 x ? = 24, so ? = ", 6, "24 divided by 4."),
    box("The pairs are 1x24, 2x12, 3x8, 4x6. Number of different factors = ", 8, "Two from each of the four pairs: 1, 2, 3, 4, 6, 8, 12, 24.", say="Now count every different number that appears.", phase="substitute"),
    box("Check: is 5 a factor of 24? Type 1 for yes, 0 for no: ", 0, "24 divided by 5 is not a whole number.", done="5 is not a factor, and the 8 we listed are all of them, so 8 is right.", phase="substitute"),
  ]},
 # B2 is 51 prime (mc)
 {"hint": "Test small primes: does 3 divide 51?",
  "misc": [{"pattern": "no_test", "expect": None, "message": "51 = 3 x 17, so it is not prime.", "note": "mc"}],
  "steps": None},
 # B3 4th multiple of 7 -> 28
 {"hint": "Count up in 7s: 7, 14, 21, then one more.",
  "misc": [{"pattern": "start_zero", "expect": 21, "message": "Multiples start at 7 x 1, not 0. They are 7, 14, 21, 28, so the 4th is 28.", "note": "0,7,14,21 -> 21"}],
  "steps": [
    say("Multiples are 7 times 1, 2, 3 and 4."),
    box("7 x 1 = ", 7, "The first multiple."),
    box("7 x 2 = ", 14, "The second multiple."),
    box("7 x 3 = ", 21, "The third multiple."),
    box("7 x 4 = ", 28, "The fourth multiple.", say="The 4th multiple is 7 x 4.", phase="substitute"),
    box("Check: 28 divided by 7 = ", 4, "Divide back by 7.", done="That is exactly 4 sevens, so the 4th multiple is 28.", phase="substitute"),
  ]},
 # B4 how many 2s in 60 -> 2
 {"hint": "Break 60 into primes: 60 = 2 x 30, 30 = 2 x 15, then 15 = 3 x 5.",
  "misc": [{"pattern": "count_all_primes", "expect": 4, "message": "60 = 2 x 2 x 3 x 5. That is four prime factors, but only two of them are 2s, so the answer is 2.", "note": "counts all 4 primes"}],
  "steps": [
    say("Split 60 into primes one step at a time."),
    box("60 = 2 x ? , so ? = ", 30, "60 divided by 2."),
    box("30 = 2 x ? , so ? = ", 15, "30 divided by 2."),
    box("15 = 3 x ? , so ? = ", 5, "15 divided by 3, and 5 is prime, so stop."),
    box("So 60 = 2 x 2 x 3 x 5. How many 2s? ", 2, "Count only the twos.", say="The primes are 2, 2, 3 and 5.", phase="substitute"),
    box("Check: 2 x 2 x 3 x 5 = ", 60, "Multiply the primes back together.", done="That rebuilds 60, and there are two 2s, so the answer is 2.", phase="substitute"),
  ]},
 # B5 HCF 12,18 -> 6
 {"hint": "List the factors of each, then pick the biggest number in both lists.",
  "misc": [{"pattern": "lcm_not_hcf", "expect": 36, "message": "That is the LCM. The HCF is the biggest number that divides BOTH 12 and 18, which is 6.", "note": "gives LCM"}],
  "steps": [
    say("List the factors of each, then find the biggest number they share."),
    box("Factors of 12: 1, 2, 3, 4, 6, 12. Is 12 a factor of 18? Type 1 or 0: ", 0, "18 divided by 12 is not whole."),
    box("Factors of 18: 1, 2, 3, 6, 9, 18. Is 9 a factor of 12? Type 1 or 0: ", 0, "12 divided by 9 is not whole."),
    box("The numbers in BOTH lists are 1, 2, 3, 6. The biggest is ", 6, "Largest shared factor.", say="Shared factors: 1, 2, 3, 6.", phase="substitute"),
    box("Check: 12 divided by 6 = ", 2, "12 divided by 6.", done="18 divided by 6 = 3 as well, so 6 divides both and nothing bigger does. HCF is 6.", phase="substitute"),
  ]},
 # B6 LCM 4,6 -> 12
 {"hint": "List multiples of each until a number appears in both.",
  "misc": [{"pattern": "hcf_not_lcm", "expect": 2, "message": "That is the HCF. The LCM is the smallest number BOTH 4 and 6 divide into, which is 12.", "note": "gives HCF"}],
  "steps": [
    say("List the multiples of each until they meet."),
    box("Multiples of 4: 4, 8, then next is ", 12, "Add 4 to the 8."),
    box("Multiples of 6: 6, then next is ", 12, "Add 6 to the 6."),
    box("The smallest number in BOTH lists is ", 12, "First shared multiple.", say="12 shows up in both lists.", phase="substitute"),
    box("Check: 12 divided by 4 = ", 3, "12 divided by 4.", done="12 divided by 6 = 2 too, so both divide 12. The LCM is 12.", phase="substitute"),
  ]},
 # B7 LCM 5,8 -> 40
 {"hint": "5 and 8 share no factor, so the LCM is just 5 x 8.",
  "misc": [
    {"pattern": "hcf_not_lcm", "expect": 1, "message": "That is the HCF: 5 and 8 share only 1. The LCM is the smallest number both divide, which is 40.", "note": "gives HCF"},
    {"pattern": "add_instead", "expect": 13, "message": "Do not add them. For two numbers with no shared factor, LCM = 5 x 8 = 40.", "note": "5+8"}],
  "steps": [
    say("5 and 8 share no factor except 1, so list multiples of the bigger one and test each."),
    box("Multiples of 8: 8, 16, 24, 32, 40. Is 8 a multiple of 5? Type 1 or 0: ", 0, "8 divided by 5 is not whole."),
    box("Is 16 a multiple of 5? Type 1 or 0: ", 0, "16 divided by 5 is not whole."),
    box("Is 24 a multiple of 5? Type 1 or 0: ", 0, "24 divided by 5 is not whole."),
    box("40 is 8 x 5, so it is a multiple of both. The LCM is ", 40, "The first shared multiple.", say="40 is the first multiple of 8 that 5 also divides.", phase="substitute"),
    box("Check: 40 divided by 5 = ", 8, "40 divided by 5.", done="40 divided by 8 = 5 too, and nothing smaller works, so the LCM is 40.", phase="substitute"),
  ]},
 # B8 HCF 20,30 -> 10
 {"hint": "List factors of each, then take the biggest shared one.",
  "misc": [{"pattern": "lcm_not_hcf", "expect": 60, "message": "That is the LCM. The HCF is the biggest number dividing BOTH 20 and 30, which is 10.", "note": "gives LCM"}],
  "steps": [
    say("List the factors of each and pick the biggest shared one."),
    box("Factors of 20: 1, 2, 4, 5, 10, 20. Is 20 a factor of 30? Type 1 or 0: ", 0, "30 divided by 20 is not whole."),
    box("Factors of 30: 1, 2, 3, 5, 6, 10, 15, 30. Is 4 a factor of 30? Type 1 or 0: ", 0, "30 divided by 4 is not whole."),
    box("Shared factors: 1, 2, 5, 10. The biggest is ", 10, "Largest shared factor.", say="Both lists contain 1, 2, 5 and 10.", phase="substitute"),
    box("Check: 20 divided by 10 = ", 2, "20 divided by 10.", done="30 divided by 10 = 3 too, so 10 divides both. HCF is 10.", phase="substitute"),
  ]},
]

# ================= SILVER =================
silver = [
 # S1 HCF 48,60 -> 12  (first silver: completion)
 {"hint": "Prime factorise both, then multiply the shared primes at their lowest powers.",
  "misc": [
    {"pattern": "lcm_not_hcf", "expect": 240, "message": "That is the LCM. The HCF uses the LOWEST power of each shared prime: 2² x 3 = 12.", "note": "LCM"},
    {"pattern": "shared_high", "expect": 48, "message": "For the HCF take the lower power of each shared prime, so 2² not 2⁴. HCF = 2² x 3 = 12.", "note": "used 2^4x3"}],
  "steps": [
    say("Prime factorise both, then take the shared primes at their lowest powers."),
    box("48 = 2⁴ x 3. The power of 2 in 48 is ", 4, "48 = 2 x 2 x 2 x 2 x 3."),
    box("60 = 2² x 3 x 5. The power of 2 in 60 is ", 2, "60 = 2 x 2 x 3 x 5."),
    box("Lowest power of 2 is 2² = 4. The shared 3 gives 3. HCF = 4 x 3 = ", 12, "Multiply 4 by 3. The 5 is only in 60, so drop it.", say="5 appears in 60 only, so it is not shared.", phase="substitute"),
    box("Check: 48 divided by 12 = ", 4, "48 divided by 12.", done="60 divided by 12 = 5 too, so 12 divides both. HCF is 12.", phase="substitute"),
  ]},
 # S2 LCM 12,20 -> 60
 {"hint": "Prime factorise both, then multiply every prime at its highest power.",
  "misc": [
    {"pattern": "multiply", "expect": 240, "message": "Do not just multiply: 12 and 20 share 2². LCM = 2² x 3 x 5 = 60.", "note": "12x20"},
    {"pattern": "hcf_not_lcm", "expect": 4, "message": "That is the HCF. The LCM uses the highest powers: 2² x 3 x 5 = 60.", "note": "HCF"}],
  "steps": [
    say("Prime factorise both, then take every prime at its highest power."),
    box("12 = 2² x 3 and 20 = 2² x 5. The shared 2² gives ", 4, "2 x 2."),
    box("The unshared primes are 3 (from 12) and 5 (from 20). 3 x 5 = ", 15, "Multiply the unshared primes."),
    box("LCM = 4 x 15 = ", 60, "Multiply 4 by 15.", say="That is 2² x 3 x 5.", phase="substitute"),
    box("Check: 60 divided by 12 = ", 5, "60 divided by 12.", done="60 divided by 20 = 3 too, so both divide 60. LCM is 60.", phase="substitute"),
  ]},
 # S3 HCF 36,90 -> 18
 {"hint": "Prime factorise both, then multiply shared primes at their lowest powers.",
  "misc": [
    {"pattern": "lcm_not_hcf", "expect": 180, "message": "That is the LCM. The HCF uses lowest shared powers: 2 x 3² = 18.", "note": "LCM"},
    {"pattern": "drop_power", "expect": 6, "message": "3 appears twice in both, so use 3². HCF = 2 x 3² = 18, not 6.", "note": "used 2x3"}],
  "steps": [
    say("Prime factorise both, then take the shared primes at their lowest powers."),
    box("36 = 2² x 3² and 90 = 2 x 3² x 5. Lowest power of 2 is 2¹ = ", 2, "The smaller power of 2, which is 1."),
    box("Lowest power of 3 is 3² = ", 9, "Both have two 3s: 3 x 3."),
    box("5 is only in 90, so drop it. HCF = 2 x 9 = ", 18, "Multiply 2 by 9.", say="Shared primes at their lowest powers: 2¹ and 3².", phase="substitute"),
    box("Check: 36 divided by 18 = ", 2, "36 divided by 18.", done="90 divided by 18 = 5 too, so 18 divides both. HCF is 18.", phase="substitute"),
  ]},
 # S4 LCM 9,15 -> 45
 {"hint": "Prime factorise both, then multiply every prime at its highest power.",
  "misc": [
    {"pattern": "multiply", "expect": 135, "message": "9 and 15 share a 3, so do not just multiply. LCM = 3² x 5 = 45.", "note": "9x15"},
    {"pattern": "hcf_not_lcm", "expect": 3, "message": "That is the HCF. The LCM = 3² x 5 = 45.", "note": "HCF"}],
  "steps": [
    say("Prime factorise both, then take each prime at its highest power."),
    box("9 = 3² and 15 = 3 x 5. The highest power of 3 is 3² = ", 9, "3 x 3."),
    box("5 appears only in 15, so bring it in. LCM = 9 x 5 = ", 45, "Multiply 9 by 5.", say="Every prime at its highest power: 3² and 5.", phase="substitute"),
    box("Check: 45 divided by 15 = ", 3, "45 divided by 15.", done="45 divided by 9 = 5 too, so both divide 45. LCM is 45.", phase="substitute"),
  ]},
 # S5 index of 3 in 180 -> 2
 {"hint": "Factor 180 down to primes, then count how many 3s appear.",
  "misc": [{"pattern": "count_error", "expect": None, "message": "180 = 2² x 3² x 5. Three appears twice, so its index is 2.", "note": "indeterminate"}],
  "steps": [
    say("Break 180 into primes, then count the 3s."),
    box("180 = 2 x 90, and 90 = 2 x 45, so far two 2s. 45 = 3 x ? , so ? = ", 15, "45 divided by 3."),
    box("15 = 3 x ? , so ? = ", 5, "15 divided by 3, and 5 is prime."),
    box("So 180 = 2² x 3 x 3 x 5. The number of 3s, the index of 3, is ", 2, "Count the 3s.", say="Two 3s appear.", phase="substitute"),
    box("Check: 2² x 3² x 5 = 4 x 9 x 5 = ", 180, "Multiply the primes back.", done="That rebuilds 180, and 3 appears twice, so its index is 2.", phase="substitute"),
  ]},
 # S6 buses 12,18 -> 36
 {"hint": "Find the LCM of 12 and 18: the first time both cycles line up.",
  "misc": [
    {"pattern": "hcf_not_lcm", "expect": 6, "message": "6 is the HCF. You need the LCM, the first shared multiple, which is 36 minutes.", "note": "HCF"},
    {"pattern": "add_times", "expect": 30, "message": "Do not add the times. Find the LCM of 12 and 18, which is 36 minutes.", "note": "12+18"}],
  "steps": [
    say("They line up at the LCM of 12 and 18. Prime factorise each."),
    box("12 = 2² x 3 and 18 = 2 x 3². The highest power of 2 is 2² = ", 4, "2 x 2."),
    box("The highest power of 3 is 3² = ", 9, "3 x 3."),
    box("LCM = 4 x 9 = ", 36, "Multiply 4 by 9.", say="That is 2² x 3².", phase="substitute"),
    box("Check: 36 divided by 12 = ", 3, "36 divided by 12.", done="36 divided by 18 = 2 too, so both buses are due at 36 minutes.", phase="substitute"),
  ]},
 # S7 HCF 56,84 -> 28
 {"hint": "Prime factorise both, then multiply shared primes at their lowest powers.",
  "misc": [
    {"pattern": "lcm_not_hcf", "expect": 168, "message": "That is the LCM. The HCF uses lowest shared powers: 2² x 7 = 28.", "note": "LCM"},
    {"pattern": "drop_prime", "expect": 4, "message": "56 and 84 also share a 7. HCF = 2² x 7 = 28, not just 4.", "note": "forgot 7"}],
  "steps": [
    say("Prime factorise both, then take the shared primes at their lowest powers."),
    box("56 = 2³ x 7 and 84 = 2² x 3 x 7. Lowest power of 2 is 2² = ", 4, "2 x 2."),
    box("7 is shared too, and 3 is only in 84, so drop it. HCF = 4 x 7 = ", 28, "Multiply 4 by 7.", say="Shared primes: 2² and 7.", phase="substitute"),
    box("Check: 56 divided by 28 = ", 2, "56 divided by 28.", done="84 divided by 28 = 3 too, so 28 divides both. HCF is 28.", phase="substitute"),
  ]},
]

# ================= GOLD =================
gold = [
 # G1 REPLACE: LCM 6,9,10 -> 90 (was LCM 12,15,20 = 60, duplicate of G2)
 {"replace_display": "Find the LCM of \\(6\\), \\(9\\) and \\(10\\).", "replace_solutions": [90],
  "hint": "Prime factorise all three, then multiply every prime at its highest power.",
  "misc": [
    {"pattern": "multiply_all", "expect": 540, "message": "Do not multiply all three: they share factors. LCM = 2 x 3² x 5 = 90.", "note": "6x9x10"},
    {"pattern": "drop_square", "expect": 30, "message": "9 = 3², so use 3². LCM = 2 x 3² x 5 = 90, not 30.", "note": "used 2x3x5"}],
  "steps": [
    say("Prime factorise all three, then take every prime at its highest power."),
    box("6 = 2 x 3, 9 = 3², 10 = 2 x 5. The highest power of 2 is 2¹ = ", 2, "Only one 2 appears anywhere."),
    box("The highest power of 3 is 3² = ", 9, "9 has two 3s."),
    box("5 appears once, in 10. LCM = 2 x 9 x 5 = ", 90, "Multiply 2 x 9 x 5.", say="Every prime at its highest power: 2, 3² and 5.", phase="substitute"),
    box("Check: 90 divided by 9 = ", 10, "90 divided by 9.", done="90 divided by 6 = 15 and 90 divided by 10 = 9 too, so 90 is the LCM.", phase="substitute"),
  ]},
 # G2 HCF from index forms -> 60
 {"hint": "For the HCF, take each shared prime at its LOWER power, then multiply.",
  "misc": [
    {"pattern": "use_higher", "expect": 1800, "message": "Those are the highest powers, giving the LCM. The HCF takes the LOWER power of each: 2² x 3 x 5 = 60.", "note": "gave LCM"},
    {"pattern": "drop_five", "expect": 12, "message": "5 is in both (power 1), so include it. HCF = 2² x 3 x 5 = 60, not 12.", "note": "forgot 5"}],
  "steps": [
    say("The HCF takes each shared prime at its lower power."),
    box("Power of 2: lower of 3 and 2 is 2, so 2² = ", 4, "The smaller power, min(3, 2) = 2."),
    box("Power of 3: lower of 1 and 2 is 1, so 3¹ = ", 3, "min(1, 2) = 1."),
    box("Power of 5: lower of 2 and 1 is 1, so 5¹ = ", 5, "min(2, 1) = 1."),
    box("HCF = 4 x 3 x 5 = ", 60, "Multiply the lower-power primes.", say="Multiply the lower powers together.", phase="substitute"),
    box("Check: 60 divided by 5 = ", 12, "60 divided by 5.", done="60 = 2² x 3 x 5, all the lower powers, and it divides both A and B. HCF is 60.", phase="substitute"),
  ]},
 # G3 LCM from index forms -> 1800
 {"hint": "For the LCM, take each prime at its HIGHER power, then multiply.",
  "misc": [
    {"pattern": "use_lower", "expect": 60, "message": "Those are the lower powers, giving the HCF. The LCM takes the HIGHER power of each: 2³ x 3² x 5² = 1800.", "note": "gave HCF"}],
  "steps": [
    say("The LCM takes each prime at its higher power."),
    box("Power of 2: higher of 3 and 2 is 3, so 2³ = ", 8, "max(3, 2) = 3."),
    box("Power of 3: higher of 1 and 2 is 2, so 3² = ", 9, "max(1, 2) = 2."),
    box("Power of 5: higher of 2 and 1 is 2, so 5² = ", 25, "max(2, 1) = 2."),
    box("LCM = 8 x 9 x 25 = ", 1800, "8 x 9 = 72, then times 25.", say="Multiply the higher powers together.", phase="substitute"),
    box("Check: 1800 divided by 25 = ", 72, "1800 divided by 25.", done="1800 = 2³ x 3² x 5², every prime at its highest power. LCM is 1800.", phase="substitute"),
  ]},
 # G4 product rule -> 30
 {"hint": "Use HCF x LCM = the product of the two numbers, then divide by the known one.",
  "misc": [
    {"pattern": "divide_lcm", "expect": 5, "message": "Use HCF x LCM = product. 6 x 120 = 720, then 720 divided by 24 = 30.", "note": "120/24"},
    {"pattern": "lcm_over_hcf", "expect": 20, "message": "That divides the LCM by the HCF. Instead: product = 6 x 120 = 720, so the other number = 720 divided by 24 = 30.", "note": "120/6"}],
  "steps": [
    say("For any two numbers, HCF x LCM equals their product. Use that."),
    box("Product of the two numbers = 6 x 120 = ", 720, "HCF times LCM."),
    box("One number is 24, so the other = 720 divided by 24 = ", 30, "Divide the product by 24.", say="Divide the product by the number you already know.", phase="substitute"),
    box("Check the HCF of 24 and 30: shared factors 1, 2, 3, 6, biggest is ", 6, "Largest factor of both 24 and 30.", done="HCF of 24 and 30 is 6 and their LCM is 120, both match, so the other number is 30.", phase="substitute"),
  ]},
 # G5 lights 8,12,18 -> 72
 {"hint": "Find the LCM of 8, 12 and 18: the first time all three cycles coincide.",
  "misc": [
    {"pattern": "multiply_all", "expect": 1728, "message": "Do not multiply all three. LCM = 2³ x 3² = 72 seconds.", "note": "8x12x18"},
    {"pattern": "hcf_not_lcm", "expect": 2, "message": "2 is the HCF. You need the LCM, the first shared multiple, which is 72 seconds.", "note": "HCF"}],
  "steps": [
    say("They coincide at the LCM of 8, 12 and 18. Prime factorise each."),
    box("8 = 2³, 12 = 2² x 3, 18 = 2 x 3². The highest power of 2 is 2³ = ", 8, "8 has three 2s."),
    box("The highest power of 3 is 3² = ", 9, "18 has two 3s."),
    box("No other primes appear. LCM = 8 x 9 = ", 72, "Multiply 8 by 9.", say="That is 2³ x 3².", phase="substitute"),
    box("Check: 72 divided by 18 = ", 4, "72 divided by 18.", done="72 divided by 8 = 9 and 72 divided by 12 = 6 too, so all three flash together at 72 seconds.", phase="substitute"),
  ]},
]

def apply(problems, designs):
    for p, d in zip(problems, designs):
        if "replace_display" in d:
            p["display"] = d["replace_display"]
            p["solutions"] = d["replace_solutions"]
        p["hint"] = d["hint"]
        p["misconceptions"] = d["misc"]
        if d["steps"] is not None:
            p["guided_steps"] = d["steps"]
        else:
            p.pop("guided_steps", None)

apply(pd["problem_bank"]["bronze"], bronze)
apply(pd["problem_bank"]["silver"], silver)
apply(pd["problem_bank"]["gold"], gold)

pd["problem_bank"]["bronze_description"] = "Single facts and small numbers: count factors, spot primes and multiples, and find the HCF or LCM of small pairs by listing."
pd["problem_bank"]["silver_description"] = "Prime factorisation is the tool: write each number in index form, then combine shared primes at lowest powers for the HCF, or all primes at highest powers for the LCM."
pd["problem_bank"]["gold_description"] = "Bigger, multi-number problems: LCM and HCF of three numbers, working from given index forms, and the HCF x LCM = product relationship."

pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: factors, multiples and listing",
  "steps": [
    "A <strong>factor</strong> divides a number exactly; a <strong>multiple</strong> is that number times 1, 2, 3 and so on.",
    "The <strong>HCF</strong> is the highest number that divides both; the <strong>LCM</strong> is the lowest number both divide into.",
    "For small numbers, just list: factors in pairs, or multiples until they meet."],
  "example": {"question": "Find the HCF of 8 and 12", "steps": [
    {"label": "Factors of 8", "content": "1, 2, 4, 8"},
    {"label": "Factors of 12", "content": "1, 2, 3, 4, 6, 12"},
    {"label": "Biggest shared", "content": "4 is the largest in both lists"},
    {"label": "Check", "content": "8 ÷ 4 = 2 and 12 ÷ 4 = 3"},
    {"label": "Answer", "content": "4", "isAnswer": True, "is_answer": True}]}
 },
 "silver": {
  "title": "Silver: prime factorisation for HCF and LCM",
  "steps": [
    "Write each number as a product of primes in index form using a factor tree, e.g. \\(48 = 2^4 \\times 3\\).",
    "<strong>HCF</strong>: multiply the shared primes at their <strong>lowest</strong> powers.",
    "<strong>LCM</strong>: multiply every prime at its <strong>highest</strong> power."],
  "example": {"question": "Find the LCM of 8 and 12", "steps": [
    {"label": "Prime factors", "content": "8 = 2³, 12 = 2² × 3"},
    {"label": "Highest powers", "content": "2³ and 3"},
    {"label": "Multiply", "content": "8 × 3 = 24"},
    {"label": "Check", "content": "24 ÷ 8 = 3 and 24 ÷ 12 = 2"},
    {"label": "Answer", "content": "24", "isAnswer": True, "is_answer": True}]}
 },
 "gold": {
  "title": "Gold: three numbers and the product rule",
  "steps": [
    "For three numbers, prime factorise all three, then take each prime at its highest power for the LCM or lowest shared power for the HCF.",
    "From given index forms, compare the powers prime by prime.",
    "Handy rule for two numbers: <strong>HCF × LCM = the product of the two numbers</strong>."],
  "example": {"question": "HCF is 4, LCM is 60, one number is 12. Find the other.", "steps": [
    {"label": "Product", "content": "4 × 60 = 240"},
    {"label": "Divide", "content": "240 ÷ 12 = 20"},
    {"label": "Check", "content": "HCF(12, 20) = 4 and LCM(12, 20) = 60"},
    {"label": "Answer", "content": "20", "isAnswer": True, "is_answer": True}]}
 }
}

pd["guided"] = {
 "opener": {
  "steps": [
    say("Two buses leave the stop together at 9:00. The number 4 bus comes every 4 minutes; the number 6 bus comes every 6 minutes. The timeline shows when each is next due.<br>" + OPENER_SVG),
    box("Reading the timeline, the first time BOTH buses are due together is at ? minutes: ", 12, "Find the first tick that lands on both rows."),
    say("You just found the <strong>Lowest Common Multiple</strong> of 4 and 6. 12 is the smallest number that both 4 and 6 divide into. That is the LCM."),
    box("Now a different job. A ribbon 12 cm long and a ribbon 18 cm long are each cut into equal whole-centimetre pieces, using the same length, with none left over. The longest piece that works is ? cm: ", 6, "The piece length must divide both 12 and 18. What is the biggest number that does?"),
    say("The biggest length dividing both 12 and 18 is 6. That is the <strong>Highest Common Factor</strong>. This lesson builds both ideas: the LCM (when cycles line up) and the HCF (the biggest shared divisor), using prime factors to handle bigger numbers.")
  ]
 },
 "teach": {
  "bronze": {
   "display": "Work out the LCM of \\(6\\) and \\(8\\)",
   "steps": [
     say("List the multiples of each until a number appears in both."),
     box("Multiples of 6: 6, 12, 18, and the 4th is 6 x 4 = ", 24, "6, 12, 18, then add 6 again."),
     box("Multiples of 8: 8, 16, and the 3rd is 8 x 3 = ", 24, "8, 16, then add 8 again."),
     box("The smallest number in BOTH lists is ", 24, "It shows up in both."),
     box("Check: 24 divided by 6 = ", 4, "24 divided by 6."),
     box("And 24 divided by 8 = ", 3, "24 divided by 8.", done="24 divides by both 6 and 8, and nothing smaller does. Listing multiples until they meet was the whole point.")
   ]
  },
  "silver": {
   "display": VENN_SVG + " Work out the HCF and LCM of \\(18\\) and \\(24\\)",
   "steps": [
     say("18 = 2 x 3² and 24 = 2³ x 3. The Venn shows this: the shared primes sit in the overlap, and the extras sit outside."),
     box("Power of 2 in the overlap = lower of 1 and 3 = 1, so 2¹ = ", 2, "18 has one 2, 24 has three."),
     box("Power of 3 in the overlap = lower of 2 and 1 = 1, so 3¹ = ", 3, "18 has two 3s, 24 has one."),
     box("HCF = the overlap product = 2 x 3 = ", 6, "Multiply the overlap."),
     box("LCM = everything at highest power = 2³ x 3² = 8 x 9 = ", 72, "Highest power of each: 2³ and 3²."),
     box("Check: 6 x 72 = ", 432, "HCF x LCM should equal 18 x 24.", done="6 x 72 = 432 = 18 x 24, so the HCF is 6 and the LCM is 72. Prime factors handled it.")
   ]
  },
  "gold": {
   "display": "The HCF of two numbers is \\(4\\) and their LCM is \\(60\\). One number is \\(12\\). Find the other.",
   "steps": [
     say("For any two numbers, HCF x LCM equals their product. Use that."),
     box("Product of the two numbers = 4 x 60 = ", 240, "HCF times LCM."),
     box("The other number = 240 divided by 12 = ", 20, "Divide the product by 12."),
     box("Check the HCF of 12 and 20: shared factors 1, 2, 4, so HCF = ", 4, "Largest factor of both 12 and 20."),
     box("Check the LCM of 12 and 20: 12 = 2² x 3, 20 = 2² x 5, LCM = 2² x 3 x 5 = ", 60, "Every prime at its highest power.", done="HCF 4 and LCM 60 both match, so the other number is 20. The product rule was the whole point.")
   ]
  }
 }
}

json.dump(pd, io.open("lesson_maths-eduqas_number-L04.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written. top keys:", list(pd.keys()))
