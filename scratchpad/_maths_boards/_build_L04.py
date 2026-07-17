# -*- coding: utf-8 -*-
"""Build the full guided-learning practice_data for maths-aqa number-L04
(Factors, Multiples & Primes). Loads the fresh live dump, preserves
worked_examples / topic_links / related_videos, rebuilds the bank with
guided_steps + honest misconceptions, adds guided + tier_guides, slims the
method_card, and fixes the two defects (silver duplicate 60, gold degenerate).
"""
import json, io

live = json.load(io.open("../_maths_guided/_L04_live_fresh.json", encoding="utf-8"))


def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {}
    if say is not None:
        d["say"] = say
    d["pre"] = pre
    if post != "":
        d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if phase is not None:
        d["phase"] = phase
    if done is not None:
        d["done"] = done
    return d


def sy(say):
    return {"say": say}


def mis(pattern, message, expect):
    return {"pattern": pattern, "message": message, "expect": expect,
            "note": "derived by committing the error"}

pd = dict(live)

# ---------------- descriptions ----------------
pb = pd["problem_bank"]
pb["bronze_description"] = "Work with one number at a time: list its factors, find a multiple, test whether it is prime, or break it into prime factors."
pb["silver_description"] = "Bring two or three numbers together: HCF and LCM by prime factorisation, plus reverse problems where a number is missing."
pb["gold_description"] = "Prime factors in index form, LCM in real contexts, and reasoning about how a number is built from its primes."

# ---------------- BRONZE ----------------
bronze = [
    {  # B0 factors of 24 -> 8
        "display": "List all the factors of \\(24\\). How many factors does it have?",
        "solutions": [8], "calculator": False, "input_type": "single_value",
        "hint": "Pair up whole numbers that multiply to 24, then count them.",
        "misconceptions": [mis("miss_factor",
            "It is easy to miss a pair. Factors of 24: 1, 2, 3, 4, 6, 8, 12, 24, which is 8 factors.", 6)],
        "guided_steps": [
            sy("Find factors in pairs that multiply to 24."),
            box("24 ÷ 1 = ", 24, "The partner of 1."),
            box("24 ÷ 2 = ", 12, "The partner of 2."),
            box("24 ÷ 3 = ", 8, "The partner of 3."),
            box("24 ÷ 4 = ", 6, "The partner of 4."),
            sy("5 does not divide 24, and 6 is already partnered with 4, so the pairs are complete. The factors are 1, 2, 3, 4, 6, 8, 12, 24."),
            box("How many pairs did you find? ", 4, "The pairs are (1,24), (2,12), (3,8), (4,6).", phase="substitute"),
            box("Each pair is 2 factors, so the total is 4 × 2 = ", 8,
                "Four pairs, two numbers in each.", phase="substitute",
                done="24 has 8 factors."),
        ],
    },
    {  # B1 7th multiple of 6 -> 42
        "display": "What is the 7th multiple of \\(6\\)?",
        "solutions": [42], "calculator": False, "input_type": "single_value",
        "hint": "Multiply 6 by 7, not by 8.",
        "misconceptions": [mis("off_by_one",
            "The 7th multiple is 6 × 7 = 42. Using 6 × 8 = 48 counts one too far.", 48)],
        "guided_steps": [
            sy("The multiples of 6 are 6 × 1, 6 × 2, 6 × 3, and so on. The 7th multiple is 6 × 7."),
            box("6 × 5 = ", 30, "Six fives."),
            box("6 × 6 = ", 36, "Six sixes."),
            box("6 × 7 = ", 42, "One more 6 than 36: 36 + 6.", phase="substitute"),
            box("Check it is in the 6 times table: 42 ÷ 6 = ", 7,
                "42 shared into sixes.", phase="substitute",
                done="42 is exactly the 7th multiple of 6."),
        ],
    },
    {  # B2 is 51 prime -> 0
        "display": "Is \\(51\\) a prime number? Enter 1 for Yes, 0 for No.",
        "solutions": [0], "calculator": False, "input_type": "single_value",
        "hint": "Test whether any small prime divides 51 exactly.",
        "misconceptions": [mis("think_prime",
            "51 looks prime but 51 = 3 × 17, so it is NOT prime. Enter 0.", 1)],
        "guided_steps": [
            sy("A prime has no factors except 1 and itself. The digits of 51 add to 5 + 1 = 6, a multiple of 3, so test 3."),
            box("51 ÷ 3 = ", 17, "51 shared into threes."),
            sy("17 is a whole number, so 3 and 17 both divide 51. That is an extra factor, so 51 is composite, not prime."),
            box("Extra factors beyond 1 and 51: at least ", 2,
                "The factors 3 and 17.", phase="substitute"),
            box("So enter 0 for 'not prime': ", 0,
                "Not prime means 0.", phase="substitute",
                done="51 = 3 × 17, so it is not prime."),
        ],
    },
    {  # B3 60 prime factors, largest prime -> 5
        "display": "Write \\(60\\) as a product of prime factors. What is the largest prime factor?",
        "solutions": [5], "calculator": False, "input_type": "single_value",
        "hint": "Factor-tree 60, then pick the biggest prime you land on.",
        "misconceptions": [mis("not_prime",
            "15 is not prime (15 = 3 × 5). Keep going: 60 = 2² × 3 × 5, so the largest prime factor is 5.", 15)],
        "guided_steps": [
            sy("Divide 60 by the smallest prime each time."),
            box("60 ÷ 2 = ", 30, "Half of 60."),
            box("30 ÷ 2 = ", 15, "Half of 30."),
            sy("15 is odd, so move to the next prime, 3: 15 ÷ 3 = 5, and 5 is prime. So \\(60 = 2^2 \\times 3 \\times 5\\)."),
            box("The primes used are 2, 3 and 5. The largest is ", 5,
                "Biggest of 2, 3 and 5.", phase="substitute"),
            box("Check: 2² × 3 × 5 = 4 × 15 = ", 60,
                "Rebuild to confirm.", phase="substitute",
                done="Largest prime factor is 5."),
        ],
    },
    {  # B4 90 prime factors, how many 3s -> 2
        "display": "Write \\(90\\) as a product of prime factors. How many times does \\(3\\) appear?",
        "solutions": [2], "calculator": False, "input_type": "single_value",
        "hint": "Factor-tree 90 and count how many 3s appear.",
        "misconceptions": [mis("wrong_count",
            "The question asks how many 3s, not how many different primes. 90 = 2 × 3² × 5, so the prime 3 appears twice.", 3)],
        "guided_steps": [
            sy("Factor-tree 90 down to primes."),
            box("90 ÷ 2 = ", 45, "Half of 90."),
            sy("45 is odd, so move to 3."),
            box("45 ÷ 3 = ", 15, "45 shared into threes."),
            box("15 ÷ 3 = ", 5, "15 shared into threes."),
            sy("5 is prime, so stop. So \\(90 = 2 \\times 3 \\times 3 \\times 5 = 2 \\times 3^2 \\times 5\\)."),
            box("Count the 3s in 2 × 3 × 3 × 5: ", 2,
                "Two threes.", phase="substitute"),
            box("Check: 2 × 3² × 5 = 2 × 9 × 5 = ", 90,
                "Rebuild to confirm.", phase="substitute",
                done="The prime 3 appears twice."),
        ],
    },
    {  # B5 HCF(12,18) -> 6
        "display": "Find the HCF of \\(12\\) and \\(18\\)",
        "solutions": [6], "calculator": False, "input_type": "single_value",
        "hint": "Prime-factorise both, then multiply the shared primes at their lowest power.",
        "misconceptions": [mis("lcm_instead",
            "That is the LCM. The HCF is the highest common FACTOR: 12 = 2² × 3, 18 = 2 × 3², shared lowest powers 2 × 3 = 6.", 36)],
        "guided_steps": [
            sy("Prime-factorise both: \\(12 = 2^2 \\times 3\\) and \\(18 = 2 \\times 3^2\\). Take each shared prime at its lowest power."),
            box("Lowest power of 2 is 2¹ = ", 2, "12 has 2², 18 has 2¹; take the smaller, 2¹."),
            box("Lowest power of 3 is 3¹ = ", 3, "12 has 3¹, 18 has 3²; take the smaller, 3¹."),
            box("HCF = 2 × 3 = ", 6, "Multiply the shared lowest powers.", phase="substitute"),
            box("Check: 12 ÷ 6 = ", 2, "12 shared into sixes.", phase="substitute",
                done="6 divides 12 and 18, and nothing bigger does."),
        ],
    },
    {  # B6 LCM(4,6) -> 12
        "display": "Find the LCM of \\(4\\) and \\(6\\)",
        "solutions": [12], "calculator": False, "input_type": "single_value",
        "hint": "List multiples of 4 and of 6 until one matches.",
        "misconceptions": [mis("multiply",
            "The LCM is not always the product. Multiples of 4: 4, 8, 12; of 6: 6, 12. LCM = 12, not 24.", 24)],
        "guided_steps": [
            sy("List the multiples of each number until one appears in both lists."),
            box("Multiples of 4: 4, 8, ", 12, "Add 4 each time: 4, 8, then 12."),
            box("Multiples of 6: 6, ", 12, "Add 6: 6, then 12."),
            box("The first value in both lists is ", 12, "12 appears in both.", phase="substitute"),
            box("Check: 12 ÷ 6 = ", 2, "12 shared into sixes.", phase="substitute",
                done="12 is the lowest common multiple of 4 and 6."),
        ],
    },
    {  # B7 LCM(5,8) -> 40
        "display": "Find the LCM of \\(5\\) and \\(8\\)",
        "solutions": [40], "calculator": False, "input_type": "single_value",
        "hint": "5 and 8 share no factor, so multiply them.",
        "misconceptions": [mis("hcf_instead",
            "That is the HCF. Since 5 and 8 share no factor, the LCM is 5 × 8 = 40.", 1)],
        "guided_steps": [
            sy("5 and 8 share no common factor, so list multiples until they meet."),
            box("Multiples of 5: 5, 10, 15, 20, 25, 30, 35, ", 40,
                "Keep adding 5 until you reach a multiple of 8."),
            box("Multiples of 8: 8, 16, 24, 32, ", 40, "Add 8: 8, 16, 24, 32, 40."),
            box("First shared value: ", 40, "40 is in both lists.", phase="substitute"),
            box("Since 5 and 8 share no factor, LCM = 5 × 8 = ", 40,
                "Coprime numbers: just multiply.", phase="substitute",
                done="LCM of 5 and 8 is 40."),
        ],
    },
]

# ---------------- SILVER ----------------
silver = [
    {  # S0 HCF(48,84) -> 12
        "display": "Find the HCF of \\(48\\) and \\(84\\)",
        "solutions": [12], "calculator": False, "input_type": "single_value",
        "hint": "Prime-factorise both, then take the shared primes at their lowest power.",
        "misconceptions": [mis("lcm_instead",
            "That is the LCM, not the HCF. HCF uses the LOWEST power of shared primes: 2² × 3 = 12.", 336)],
        "guided_steps": [
            sy("Prime-factorise both: \\(48 = 2^4 \\times 3\\) and \\(84 = 2^2 \\times 3 \\times 7\\). Shared primes are 2 and 3."),
            box("Lowest power of 2 is 2² = ", 4, "48 has 2⁴, 84 has 2²; take 2²."),
            box("Lowest power of 3 is 3¹ = ", 3, "Both have exactly one 3."),
            box("7 is only in 84, so ignore it. HCF = 4 × 3 = ", 12,
                "Multiply the shared lowest powers.", phase="substitute"),
            box("Check: 84 ÷ 12 = ", 7, "84 shared into twelves.", phase="substitute",
                done="12 divides 48 and 84, and nothing bigger does."),
        ],
    },
    {  # S1 LCM(15,20) -> 60
        "display": "Find the LCM of \\(15\\) and \\(20\\)",
        "solutions": [60], "calculator": False, "input_type": "single_value",
        "hint": "Prime-factorise both, then take every prime at its highest power.",
        "misconceptions": [mis("multiply",
            "The LCM is not the product. 15 = 3 × 5, 20 = 2² × 5, so LCM = 2² × 3 × 5 = 60, not 300.", 300)],
        "guided_steps": [
            sy("Prime-factorise both: \\(15 = 3 \\times 5\\) and \\(20 = 2^2 \\times 5\\). Take every prime at its highest power."),
            box("Highest power of 2 is 2² = ", 4, "Only 20 has 2s: 2²."),
            box("Highest power of 3 is 3¹ = ", 3, "Only 15 has a 3."),
            box("Highest power of 5 is 5¹. LCM = 4 × 3 × 5 = ", 60,
                "Multiply the highest powers.", phase="substitute"),
            box("Check: 60 ÷ 20 = ", 3, "60 shared into twenties.", phase="substitute",
                done="60 is the lowest number both 15 and 20 divide into."),
        ],
    },
    {  # S2 HCF(72,108) -> 36
        "display": "Find the HCF of \\(72\\) and \\(108\\)",
        "solutions": [36], "calculator": False, "input_type": "single_value",
        "hint": "Prime-factorise both, then take the shared primes at their lowest power.",
        "misconceptions": [mis("lcm_instead",
            "That is the LCM. HCF uses the LOWEST power of shared primes: 2² × 3² = 36.", 216)],
        "guided_steps": [
            sy("Prime-factorise both: \\(72 = 2^3 \\times 3^2\\) and \\(108 = 2^2 \\times 3^3\\). Shared primes are 2 and 3."),
            box("Lowest power of 2 is 2² = ", 4, "Smaller of 2³ and 2²."),
            box("Lowest power of 3 is 3² = ", 9, "Smaller of 3² and 3³."),
            box("HCF = 4 × 9 = ", 36, "Multiply the shared lowest powers.", phase="substitute"),
            box("Check: 108 ÷ 36 = ", 3, "108 shared into thirty-sixes.", phase="substitute",
                done="36 is the highest common factor of 72 and 108."),
        ],
    },
    {  # S3 FIXED: LCM(8,15,20) -> 120  (was duplicate 60)
        "display": "Find the LCM of \\(8\\), \\(15\\) and \\(20\\)",
        "solutions": [120], "calculator": False, "input_type": "single_value",
        "hint": "Prime-factorise all three, then take every prime at its highest power.",
        "misconceptions": [mis("two_only",
            "Include all three numbers. 8 = 2³, 15 = 3 × 5, 20 = 2² × 5, so LCM = 2³ × 3 × 5 = 120. Using only 15 and 20 gives 60.", 60)],
        "guided_steps": [
            sy("Prime-factorise all three: \\(8 = 2^3\\), \\(15 = 3 \\times 5\\), \\(20 = 2^2 \\times 5\\). Take every prime at its highest power."),
            box("Highest power of 2, from the 8, is 2³ = ", 8, "8 = 2³ beats 20's 2²."),
            sy("Highest power of 3 is 3¹ (from 15), and highest power of 5 is 5¹."),
            box("LCM = 8 × 3 × 5 = ", 120, "Multiply the highest powers.", phase="substitute"),
            box("Check: 120 ÷ 20 = ", 6, "120 shared into twenties.", phase="substitute",
                done="All three of 8, 15 and 20 divide 120, and nothing smaller works."),
        ],
    },
    {  # S4 HCF 6, LCM 90, one is 18 -> 30
        "display": "Two numbers have HCF 6 and LCM 90. One number is 18. Find the other.",
        "solutions": [30], "calculator": False, "input_type": "single_value",
        "hint": "Use HCF × LCM = the product of the two numbers.",
        "misconceptions": [mis("wrong_formula",
            "Use HCF × LCM = product. 6 × 90 = 540, and 540 ÷ 18 = 30, not 90 ÷ 18 = 5.", 5)],
        "guided_steps": [
            sy("For two numbers, HCF × LCM = the product of the numbers themselves."),
            box("HCF × LCM = 6 × 90 = ", 540, "6 × 90."),
            box("The two numbers multiply to 540 and one is 18, so the other = 540 ÷ 18 = ", 30,
                "540 shared into eighteens.", phase="substitute"),
            box("Check HCF of 18 and 30: 18 = 2 × 3², 30 = 2 × 3 × 5, shared 2 × 3 = ", 6,
                "Shared primes 2 and 3.", phase="substitute",
                done="HCF is 6 and LCM is 90, both matching the question."),
        ],
    },
    {  # S5 180 distinct primes -> 3
        "display": "Write \\(180\\) as a product of prime factors. How many distinct prime factors?",
        "solutions": [3], "calculator": False, "input_type": "single_value",
        "hint": "Factor-tree 180, then count the different primes.",
        "misconceptions": [mis("count_powers",
            "Distinct means different primes: 2, 3 and 5, so 3. Counting 2 × 2 × 3 × 3 × 5 with repeats gives 5, which is not what 'distinct' asks.", 5)],
        "guided_steps": [
            sy("Factor-tree 180 down to primes."),
            box("180 ÷ 2 = ", 90, "Half of 180."),
            box("90 ÷ 2 = ", 45, "Half of 90."),
            sy("45 is odd: 45 ÷ 3 = 15, 15 ÷ 3 = 5, and 5 is prime. So \\(180 = 2^2 \\times 3^2 \\times 5\\)."),
            box("The different primes are 2, 3 and 5, so the count of distinct primes is ", 3,
                "Count the different primes, not their powers.", phase="substitute"),
            box("Check: 2² × 3² × 5 = 4 × 9 × 5 = ", 180,
                "Rebuild to confirm.", phase="substitute",
                done="Three distinct primes: 2, 3 and 5."),
        ],
    },
    {  # S6 LCM 120, one is 24, other in (30,50) -> 40
        "display": "The LCM of two numbers is \\(120\\). One number is \\(24\\). The other is between \\(30\\) and \\(50\\). Find it.",
        "solutions": [40], "calculator": False, "input_type": "single_value",
        "hint": "The other number must supply the factor 5; test which value in range gives LCM 120.",
        "misconceptions": [mis("wrong_method",
            "Test the LCM, do not just pick any multiple of 5. LCM(24, 45) = 360, not 120. LCM(24, 40) = 120, so the answer is 40.", 45)],
        "guided_steps": [
            sy("Here \\(120 = 2^3 \\times 3 \\times 5\\) and \\(24 = 2^3 \\times 3\\). The other number must bring in the factor 5, and must divide 120."),
            box("Test 40: 120 ÷ 40 = ", 3, "120 shared into forties; a whole number means 40 divides 120."),
            box("40 = 2³ × 5. Check LCM(24, 40) = highest powers 2³ × 3 × 5 = ", 120,
                "2³ and 3 from 24, the 5 from 40.", phase="substitute"),
            box("120 is the target and 40 lies between 30 and 50, so the other number is ", 40,
                "The value that gave LCM 120.", phase="substitute",
                done="24 and 40 have LCM 120, and 40 is in range."),
        ],
    },
]

# ---------------- GOLD ----------------
gold = [
    {  # G0 HCF index form -> 36
        "display": "Find the HCF of \\(2^3 \\times 3^2 \\times 5\\) and \\(2^2 \\times 3^4 \\times 7\\)",
        "solutions": [36], "calculator": False, "input_type": "single_value",
        "hint": "Read off the shared primes (2 and 3) at their lowest power.",
        "misconceptions": [mis("max_powers",
            "HCF uses the LOWEST power of shared primes: 2² × 3² = 36. Using the highest powers, 2³ × 3⁴ = 648, is the LCM-style move.", 648)],
        "guided_steps": [
            sy("Already in index form, so read straight off. Shared primes are 2 and 3, not 5 or 7. Take each at its lowest power."),
            box("Lowest power of 2 is 2² = ", 4, "min of 2³ and 2² is 2²."),
            box("Lowest power of 3 is 3² = ", 9, "min of 3² and 3⁴ is 3²."),
            box("HCF = 4 × 9 = ", 36, "Multiply the shared lowest powers.", phase="substitute"),
            box("Confirm the value of the HCF: ", 36,
                "The product 4 × 9.", phase="substitute",
                done="HCF = 36; 5 and 7 are not shared so they play no part."),
        ],
    },
    {  # G1 LCM index form -> 22680 (calculator)
        "display": "Find the LCM of \\(2^3 \\times 3^2 \\times 5\\) and \\(2^2 \\times 3^4 \\times 7\\)",
        "solutions": [22680], "calculator": True, "input_type": "single_value",
        "hint": "Take every prime at its highest power, then multiply.",
        "misconceptions": [mis("min_powers",
            "That is the HCF. The LCM uses the HIGHEST power of every prime: 2³ × 3⁴ × 5 × 7 = 22680.", 36)],
        "guided_steps": [
            sy("For the LCM take every prime at its highest power: 2³, 3⁴, 5 and 7."),
            box("2³ × 3⁴ = 8 × 81 = ", 648, "8 × 81."),
            box("now × 5: 648 × 5 = ", 3240, "648 × 5."),
            box("now × 7: 3240 × 7 = ", 22680, "3240 × 7.", phase="substitute"),
            box("Check it is a multiple of the first number: 22680 ÷ 360 = ", 63,
                "22680 ÷ (2³ × 3² × 5) = 22680 ÷ 360.", phase="substitute",
                done="63 = 3² × 7, a whole number, so 22680 is a valid LCM."),
        ],
    },
    {  # G2 consecutive integers proof + sum from 14 -> 45
        "display": "Prove that the sum of any three consecutive integers is always divisible by 3. What is the sum of three consecutive integers starting at \\(14\\)?",
        "solutions": [45], "calculator": False, "input_type": "single_value",
        "hint": "Add 14, 15 and 16.",
        "misconceptions": [mis("wrong_sum",
            "Start AT 14: the integers are 14, 15 and 16, summing to 45. Starting at 13 gives 42.", 42)],
        "guided_steps": [
            sy("Call the integers \\(n\\), \\(n+1\\), \\(n+2\\). Their sum is \\(n + (n+1) + (n+2) = 3n + 3 = 3(n+1)\\), which is 3 times a whole number, so always divisible by 3."),
            box("Now use n = 14, giving 14, 15, 16. First, 14 + 15 = ", 29, "Add the first two."),
            box("then + 16: 29 + 16 = ", 45, "Add the third.", phase="substitute"),
            box("Check it is divisible by 3: 45 ÷ 3 = ", 15,
                "45 shared into threes.", phase="substitute",
                done="45 = 3 × 15, and 15 = n + 1 = 15, matching 3(n+1)."),
        ],
    },
    {  # G3 pens 8, rulers 12, smallest equal -> 24
        "display": "Pens come in packs of \\(8\\). Rulers come in packs of \\(12\\). What is the smallest number of each you must buy to have equal numbers of pens and rulers?",
        "solutions": [24], "calculator": False, "input_type": "single_value",
        "hint": "Find the LCM of 8 and 12.",
        "misconceptions": [mis("wrong_method",
            "The smallest equal number is the LCM, not the product. LCM(8, 12) = 24, so 24 of each. 8 × 12 = 96 also works but is not the smallest.", 96)],
        "guided_steps": [
            sy("You want the smallest total that is a multiple of both 8 and 12: the LCM. \\(8 = 2^3\\) and \\(12 = 2^2 \\times 3\\)."),
            box("Highest power of 2, from the 8, is 2³ = ", 8, "Larger of 2³ and 2²."),
            box("Highest power of 3 is 3¹. LCM = 8 × 3 = ", 24,
                "Multiply the highest powers.", phase="substitute"),
            box("Check rulers: 24 ÷ 12 = ", 2, "24 shared into twelves.", phase="substitute",
                done="24 pens (3 packs) and 24 rulers (2 packs): equal, and the smallest such number."),
        ],
    },
    {  # G4 FIXED: exactly 12 factors, 100<n<200 -> 108 (was degenerate)
        "display": "\\(n = 2^a \\times 3^b\\). If \\(n\\) has exactly 12 factors and \\(100 < n < 200\\), find \\(n\\).",
        "solutions": [108], "calculator": False, "input_type": "single_value",
        "hint": "Use (a+1)(b+1) = 12 and keep the value between 100 and 200.",
        "misconceptions": [mis("wrong_count",
            "96 = 2⁵ × 3 also has 12 factors, but it is below 100. In the range 100 to 200 the only value is 108 = 2² × 3³.", 96)],
        "guided_steps": [
            sy("The number of factors of \\(2^a \\times 3^b\\) is \\((a+1)(b+1)\\). You need this to equal 12 with the value between 100 and 200."),
            box("Try a = 2, b = 3: (2+1)(3+1) = 3 × 4 = ", 12, "(a+1)(b+1)."),
            box("That value is 2² × 3³ = 4 × 27 = ", 108, "4 × 27."),
            sy("Is 108 between 100 and 200? Yes. The other factor pairs fall outside: (a,b) = (5,1) gives 96 (too small), (3,2) gives 72 (too small), (1,5) gives 486 (too big)."),
            box("So the only value between 100 and 200 is ", 108,
                "108 is the one in range.", phase="substitute"),
            box("Confirm its factor count: (2+1)(3+1) = ", 12,
                "3 × 4.", phase="substitute",
                done="n = 108 = 2² × 3³: exactly 12 factors, between 100 and 200."),
        ],
    },
]

pb["bronze"] = bronze
pb["silver"] = silver
pb["gold"] = gold

# ---------------- tier_guides ----------------
def ex(question, steps):
    return {"question": question, "steps": steps}

def st(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans:
        d["isAnswer"] = True
        d["is_answer"] = True
    return d

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one number at a time",
        "steps": [
            "A <strong>factor</strong> divides a number exactly; a <strong>multiple</strong> is that number times 1, 2, 3, and so on; a <strong>prime</strong> has exactly two factors, itself and 1.",
            "To break a number into primes, keep dividing by the smallest prime that fits (2, then 3, then 5, ...) until you reach a prime. Collect the primes you used.",
            "For small HCF and LCM, list them out: the HCF is the biggest number in both factor lists, the LCM the smallest number in both multiple lists.",
        ],
        "example": ex("Write 40 as a product of prime factors", [
            st("Divide by 2", "<p>40 ÷ 2 = 20, 20 ÷ 2 = 10, 10 ÷ 2 = 5.</p>"),
            st("Stop at a prime", "<p>5 is prime, so stop.</p>"),
            st("Check", "<p>2 × 2 × 2 × 5 = 40 ✓</p>"),
            st("Answer", "<p>\\(40 = 2^3 \\times 5\\)</p>", True),
        ]),
    },
    "silver": {
        "title": "Silver: combine numbers with prime factors",
        "steps": [
            "Write each number as a product of primes in index form (for example 48 = 2⁴ × 3).",
            "<strong>HCF</strong>: multiply the shared primes, each at its LOWEST power. <strong>LCM</strong>: multiply every prime that appears, each at its HIGHEST power.",
            "Reverse problems use HCF × LCM = the product of the two numbers, so a missing number is (HCF × LCM) ÷ the known one.",
        ],
        "example": ex("Find the HCF and LCM of 18 and 24", [
            st("Prime factorise", "<p>\\(18 = 2 \\times 3^2\\), \\(24 = 2^3 \\times 3\\).</p>"),
            st("HCF", "<p>Lowest powers: \\(2 \\times 3 = 6\\).</p>"),
            st("LCM", "<p>Highest powers: \\(2^3 \\times 3^2 = 72\\).</p>"),
            st("Check", "<p>6 × 72 = 432 = 18 × 24 ✓</p>"),
            st("Answer", "<p>HCF 6, LCM 72</p>", True),
        ]),
    },
    "gold": {
        "title": "Gold: index form and reasoning",
        "steps": [
            "When numbers are already in index form (like 2³ × 3² × 5), read HCF and LCM straight off: HCF takes each shared prime's lowest power, LCM takes every prime's highest power.",
            "Word problems asking 'when do they next line up?' or 'smallest equal number' are LCM; 'largest equal group' is HCF.",
            "The factor count of \\(2^a \\times 3^b\\) is \\((a+1)(b+1)\\): a useful check when reasoning about how a number is built.",
        ],
        "example": ex("Find the HCF and LCM of 2² × 3 × 5 and 2 × 3² × 5", [
            st("Shared primes", "<p>Both share 2, 3 and 5.</p>"),
            st("HCF", "<p>Lowest powers: \\(2 \\times 3 \\times 5 = 30\\).</p>"),
            st("LCM", "<p>Highest powers: \\(2^2 \\times 3^2 \\times 5 = 180\\).</p>"),
            st("Check", "<p>30 × 180 = 5400 = 60 × 90 ✓</p>"),
            st("Answer", "<p>HCF 30, LCM 180</p>", True),
        ]),
    },
}

# ---------------- guided (opener + teach) ----------------
pd["guided"] = {
    "opener": {
        "label": "Before any factor trees",
        "display": "\U0001F534 A red light flashes every 4 seconds.<br>\U0001F535 A blue light flashes every 6 seconds.<br>They both flash together right now.",
        "steps": [
            {
                "say": "No method yet, just count in your head. Red flashes at 4, 8, 12... seconds. Blue flashes at 6, 12... seconds.",
                "pre": "They next flash together at ",
                "post": " seconds",
                "answer": 12,
                "hint": "Find the first second in BOTH lists: 4, 8, 12 and 6, 12.",
            },
            {
                "say": "You found the first second that is in both counting lists. That number, 12, is the <strong>Lowest Common Multiple</strong> of 4 and 6. Every 'when do they line up again?' question is an LCM.",
                "pre": "By then the red light has flashed 12 ÷ 4 = ",
                "post": " times",
                "answer": 3,
                "hint": "12 seconds, one flash every 4 seconds.",
            },
            {
                "say": "So 12 is the 3rd <strong>multiple</strong> of 4, and also a multiple of 6. Behind every number sits a set of <strong>prime</strong> building blocks (2, 3, 5, 7...): a factor tree finds them, and those blocks build any HCF or LCM without listing.",
            },
        ],
    },
    "teach": {
        "bronze": {
            "display": "Write \\(72\\) as a product of its prime factors.",
            "label": "Together: your first factor tree",
            "steps": [
                sy("Keep dividing by the smallest prime that fits. Start with 2."),
                box("72 ÷ 2 = ", 36, "Half of 72."),
                box("36 ÷ 2 = ", 18, "Half of 36."),
                box("18 ÷ 2 = ", 9, "Half of 18."),
                sy("9 is odd, so 2 is finished. Move to the next prime, 3."),
                box("9 ÷ 3 = ", 3, "9 shared into threes."),
                sy("3 is prime, so stop. The primes you divided by are 2, 2, 2, 3, 3."),
                box("Count the 2s (2, 2, 2), so 2 to the power ", 3,
                    "Three of them.", post=", times 3²",
                    done="So 72 = 2³ × 3². That factor tree is the key to every HCF and LCM."),
            ],
        },
        "silver": {
            "display": "Find the HCF and LCM of \\(24\\) and \\(36\\).",
            "label": "Together: HCF and LCM from primes",
            "steps": [
                sy("First prime-factorise both: \\(24 = 2^3 \\times 3\\) and \\(36 = 2^2 \\times 3^2\\)."),
                box("HCF: lowest power of 2 is 2² = ", 4, "Smaller of 2³ and 2²."),
                box("lowest power of 3 is 3¹ = ", 3, "Smaller of 3¹ and 3²."),
                box("HCF = 4 × 3 = ", 12, "Multiply the shared lowest powers."),
                sy("Now the LCM: take the highest power of every prime."),
                box("highest power of 2 is 2³ = ", 8, "Larger of 2³ and 2²."),
                box("highest power of 3 is 3² = ", 9, "Larger of 3¹ and 3²."),
                box("LCM = 8 × 9 = ", 72, "Multiply the highest powers.",
                    done="Check: HCF × LCM = 12 × 72 = 864 = 24 × 36. ✓"),
            ],
        },
        "gold": {
            "display": "Find the HCF and LCM of \\(2^4 \\times 3^2 \\times 5\\) and \\(2^2 \\times 3^3 \\times 7\\).",
            "label": "Together: the gold move",
            "steps": [
                sy("Work straight from the index form, no expanding. The common primes are 2 and 3."),
                box("HCF: lowest power of 2 is 2² = ", 4, "min of 2⁴ and 2²."),
                box("lowest power of 3 is 3² = ", 9, "min of 3² and 3³."),
                box("HCF = 4 × 9 = ", 36, "Multiply the shared lowest powers."),
                sy("LCM: highest power of every prime, including the 5 and the 7."),
                box("highest powers of 2 and 3: 2⁴ × 3³ = 16 × 27 = ", 432, "16 × 27."),
                box("now × 5 × 7: 432 × 35 = ", 15120, "432 × 35.",
                    done="LCM = 2⁴ × 3³ × 5 × 7 = 15120. Index form does HCF and LCM with no listing at all."),
            ],
        },
    },
}

# ---------------- method_card (slim) ----------------
pd["method_card"] = {
    "title": "How to Find Factors, Multiples, HCF and LCM",
    "steps": [
        "Write each number as a product of prime factors (factor tree or repeated division).",
        "HCF: multiply the primes shared by both, each at its lowest power.",
        "LCM: multiply every prime that appears, each at its highest power.",
        "Check: HCF × LCM should equal the product of the two numbers.",
    ],
    "content": "<p><strong>Factors</strong> divide a number exactly; <strong>multiples</strong> are its times table; a <strong>prime</strong> has exactly two factors, 1 and itself. Note 1 is not prime.</p><p><strong>Prime factorisation</strong> writes a number as a product of primes, for example \\(60 = 2^2 \\times 3 \\times 5\\).</p><p>The <strong>HCF</strong> is the largest number dividing into two numbers; the <strong>LCM</strong> is the smallest number both divide into. From prime factors: HCF multiplies shared primes at their lowest powers; LCM multiplies all primes at their highest powers.</p>",
    "example": "<p><strong>Find the HCF and LCM of 36 and 60</strong></p><p><strong>Step 1:</strong> \\(36 = 2^2 \\times 3^2\\) and \\(60 = 2^2 \\times 3 \\times 5\\)</p><p><strong>Step 2, HCF:</strong> shared primes, lowest powers: \\(2^2 \\times 3 = 12\\)</p><p><strong>Step 3, LCM:</strong> all primes, highest powers: \\(2^2 \\times 3^2 \\times 5 = 180\\)</p><p><strong>Check:</strong> \\(12 \\times 180 = 2160 = 36 \\times 60\\) ✔</p>",
}

# preserved untouched: topic_links, related_videos, worked_examples

out = "lesson_maths-aqa_number-L04.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("preserved worked_examples:", len(pd["worked_examples"]))
print("preserved topic_links:", pd["topic_links"])
print("related_videos:", pd["related_videos"])
