# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_number_L04.json", encoding="utf-8"))

def b(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {}
    if say is not None: d["say"] = say
    d["pre"] = pre
    d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def s(say):
    return {"say": say}

def mc(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

def dedash(obj):
    # Replace em dashes (U+2014) in preserved student-facing strings with a comma.
    if isinstance(obj, dict):
        return {k: dedash(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [dedash(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ", ").replace("—", ",")
    return obj

# ---------------- BRONZE ----------------
bronze = []

# B0: 36 -> a+b = 4
bronze.append({
 "display": "Write \\(36\\) as a product of prime factors. Give the answer as \\(2^a \\times 3^b\\). What is \\(a + b\\)?",
 "solutions": [4],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Prime factorise 36, then add the two powers.",
 "misconceptions": [
   mc("wrong_tree", None, "36 = 2² × 3². So a = 2, b = 2, and a + b = 4."),
   mc("not_prime", None, "Make sure every factor is prime. 36 = 4 × 9 is not fully factorised, keep splitting."),
 ],
 "guided_steps": [
   s("Build 36 from its prime building blocks. Split off the 2s first, then the 3s."),
   b("36 ÷ 2 = ", 18, "Halve 36."),
   b("18 ÷ 2 = ", 9, "Halve 18. After this 9 is odd, so no more 2s divide in."),
   b("9 ÷ 3 = ", 3, "9 = 3 × 3."),
   s("So 36 = 2 × 2 × 3 × 3 = \\(2^2 \\times 3^2\\). That gives a = 2 and b = 2."),
   b("a + b = 2 + 2 = ", 4, "Add the two powers.", phase="substitute"),
   b("Check the factorisation: 4 × 9 = ", 36, "Work out 2² × 3² = 4 × 9.", done="That rebuilds 36, so a + b = 4 is right."),
 ],
})

# B1: HCF(12,18) = 6   (changed from HCF(12,8)=4 to remove duplicate solution 4)
bronze.append({
 "display": "Find the HCF of \\(12\\) and \\(18\\)",
 "solutions": [6],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Factorise both, then multiply the shared primes at their lowest power.",
 "misconceptions": [
   mc("lcm_not_hcf", 36, "36 is the LCM. The HCF is the largest number that divides into both 12 and 18, which is 6."),
   mc("wrong_factor", 3, "3 is a common factor but not the highest. Both 12 and 18 also divide by 6."),
 ],
 "guided_steps": [
   s("Prime factors: \\(12 = 2^2 \\times 3\\) and \\(18 = 2 \\times 3^2\\). HCF multiplies the shared primes at their lowest power."),
   b("Shared power of 2, the lower of 2 and 1, is ", 1, "12 has two 2s, 18 has one. Take the lower."),
   b("Shared power of 3, the lower of 1 and 2, is ", 1, "12 has one 3, 18 has two. Take the lower."),
   s("So HCF = 2 × 3."),
   b("2 × 3 = ", 6, "Multiply the shared primes.", phase="substitute"),
   b("Check: 18 ÷ 6 = ", 3, "Does 6 divide 18?", done="6 divides both 12 and 18 exactly, so HCF = 6."),
 ],
})

# B2: LCM(6,10) = 30
bronze.append({
 "display": "Find the LCM of \\(6\\) and \\(10\\)",
 "solutions": [30],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Factorise both, then multiply each prime at its highest power.",
 "misconceptions": [
   mc("hcf_not_lcm", 2, "2 is the HCF, not the LCM. The LCM is the smallest number both 6 and 10 divide into: 30."),
   mc("multiply", 60, "6 × 10 = 60 is a common multiple, but not the lowest. LCM = 30."),
 ],
 "guided_steps": [
   s("Primes: \\(6 = 2 \\times 3\\) and \\(10 = 2 \\times 5\\). LCM uses every prime that appears, each at its highest power: here 2, 3 and 5."),
   b("First multiply the 2 and the 3: 2 × 3 = ", 6, "Multiply."),
   b("Now bring in the 5: 6 × 5 = ", 30, "Multiply by 5.", phase="substitute"),
   b("Check: 30 ÷ 10 = ", 3, "Does 10 go into 30?", done="30 divides by both 6 and 10 and is the smallest that does, so LCM = 30."),
 ],
})

# B3: HCF(15,25) = 5
bronze.append({
 "display": "Find the HCF of \\(15\\) and \\(25\\)",
 "solutions": [5],
 "calculator": False,
 "input_type": "single_value",
 "hint": "The only prime 15 and 25 share is 5.",
 "misconceptions": [
   mc("lcm_not_hcf", 75, "75 is the LCM. The HCF is the biggest number that goes into both 15 and 25, which is 5."),
   mc("wrong_factor", 1, "1 is always a common factor but not the highest here. Both numbers divide by 5."),
 ],
 "guided_steps": [
   s("Prime factors: \\(15 = 3 \\times 5\\) and \\(25 = 5^2\\). The only shared prime is 5, taken at the lower power."),
   b("How many 5s does 15 have? ", 1, "15 = 3 × 5, so one 5."),
   s("That is the lower count, so the HCF is one 5."),
   b("HCF = ", 5, "One shared 5 means HCF = 5.", phase="substitute"),
   b("Check: 25 ÷ 5 = ", 5, "Does 5 divide 25?", done="5 divides both 15 and 25 exactly and nothing bigger does, so HCF = 5."),
 ],
})

# B4: LCM(4,6) = 12
bronze.append({
 "display": "Find the LCM of \\(4\\) and \\(6\\)",
 "solutions": [12],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Take the highest power of each prime: 2² from 4, and 3 from 6.",
 "misconceptions": [
   mc("multiply", 24, "4 × 6 = 24, but 12 is a smaller common multiple. Use prime factors."),
   mc("hcf_not_lcm", 2, "2 is the HCF. The LCM is the smallest number both 4 and 6 divide into: 12."),
 ],
 "guided_steps": [
   s("Primes: \\(4 = 2^2\\) and \\(6 = 2 \\times 3\\). LCM takes the highest power of each prime: 2² from 4, and 3 from 6."),
   b("Work out the highest power of 2: 2² = ", 4, "2 × 2."),
   b("Multiply by the 3: 4 × 3 = ", 12, "Multiply by 3.", phase="substitute"),
   b("Check: 12 ÷ 6 = ", 2, "Does 6 go into 12?", done="12 divides by both 4 and 6 and is the smallest that does, so LCM = 12."),
 ],
})

# B5: prime factors of 30, how many different = 3
bronze.append({
 "display": "List the prime factors of \\(30\\). How many different prime factors are there?",
 "solutions": [3],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Factorise 30, then count the distinct primes.",
 "misconceptions": [
   mc("count_all", 8, "8 is the total number of factors of 30. The question asks for different PRIME factors: 2, 3 and 5, so 3."),
   mc("not_prime", None, "Count only prime factors: 30 = 2 × 3 × 5, three of them."),
 ],
 "guided_steps": [
   s("Break 30 into primes with a factor tree."),
   b("30 ÷ 2 = ", 15, "Halve 30."),
   b("15 ÷ 3 = ", 5, "3 into 15."),
   s("5 is prime, so 30 = 2 × 3 × 5. Now count the DIFFERENT primes: 2, 3 and 5."),
   b("Number of different prime factors = ", 3, "Count 2, 3 and 5.", phase="substitute"),
   b("Check: 2 × 3 × 5 = ", 30, "Multiply them back.", done="That rebuilds 30 from three different primes, so the answer is 3."),
 ],
})

# B6: HCF(20,30) = 10
bronze.append({
 "display": "Find the HCF of \\(20\\) and \\(30\\)",
 "solutions": [10],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Multiply the shared primes at their lowest power.",
 "misconceptions": [
   mc("lcm_not_hcf", 60, "60 is the LCM. For the HCF, multiply the shared primes at their lowest power: 2 × 5 = 10."),
   mc("wrong_factor", 5, "5 is a common factor but 10 is higher, since both 20 and 30 divide by 10."),
 ],
 "guided_steps": [
   s("Prime factors: \\(20 = 2^2 \\times 5\\) and \\(30 = 2 \\times 3 \\times 5\\). Shared primes: 2 and 5."),
   b("Shared power of 2, the lower of 2 and 1, is ", 1, "20 has two 2s, 30 has one. Take the lower."),
   s("They also share one 5 each. So HCF = 2 × 5."),
   b("2 × 5 = ", 10, "Multiply the shared primes.", phase="substitute"),
   b("Check: 30 ÷ 10 = ", 3, "Does 10 go into 30?", done="10 divides both 20 and 30 exactly, so HCF = 10."),
 ],
})

# B7: LCM(8,12) = 24
bronze.append({
 "display": "Find the LCM of \\(8\\) and \\(12\\)",
 "solutions": [24],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Highest power of 2 is 2³; then bring in the 3.",
 "misconceptions": [
   mc("multiply", 96, "8 × 12 = 96, but the LCM is smaller. Use primes: 8 = 2³, 12 = 2² × 3, so LCM = 2³ × 3 = 24."),
   mc("hcf_not_lcm", 4, "4 is the HCF. The LCM is 24."),
 ],
 "guided_steps": [
   s("Primes: \\(8 = 2^3\\) and \\(12 = 2^2 \\times 3\\). Highest power of 2 is 2³ = 8; then bring in the 3."),
   b("Work out 2³ = ", 8, "2 × 2 × 2."),
   b("Multiply by the 3: 8 × 3 = ", 24, "Multiply by 3.", phase="substitute"),
   b("Check: 24 ÷ 12 = ", 2, "Does 12 go into 24?", done="24 divides by both 8 and 12 and is the smallest that does, so LCM = 24."),
 ],
})

# ---------------- SILVER ----------------
silver = []

# S0: 180, how many 2s = 2
silver.append({
 "display": "Write \\(180\\) as a product of prime factors. How many 2s appear?",
 "solutions": [2],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Peel off 2s from 180 until an odd number is left, then count them.",
 "misconceptions": [
   mc("count_all", 5, "5 counts every prime factor. The question asks only how many 2s: 180 = 2² × 3² × 5, so two 2s."),
   mc("wrong_tree", None, "180 = 2² × 3² × 5. The power of 2 is 2, so two 2s appear."),
 ],
 "guided_steps": [
   s("Factor 180 down to primes. Peel off 2s first."),
   b("180 ÷ 2 = ", 90, "Halve 180."),
   b("90 ÷ 2 = ", 45, "Halve 90. After this 45 is odd, so no more 2s."),
   s("45 is odd, so the 2s stop here. 180 = 2 × 2 × 45 = \\(2^2 \\times 3^2 \\times 5\\)."),
   b("Number of 2s = ", 2, "Two 2s came out.", phase="substitute"),
   b("Check: 4 × 45 = ", 180, "2² = 4, times 45.", done="180 = 2² × 45, so exactly two 2s appear."),
 ],
})

# S1: HCF(36,84) = 12
silver.append({
 "display": "Find the HCF of \\(36\\) and \\(84\\)",
 "solutions": [12],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Shared primes at their lowest power: 2² and 3.",
 "misconceptions": [
   mc("wrong_factorisation", None, "36 = 2² × 3² and 84 = 2² × 3 × 7. Shared: 2² × 3 = 12."),
   mc("lcm_not_hcf", 252, "252 is the LCM. For the HCF, use the lowest power of the shared primes."),
 ],
 "guided_steps": [
   s("Prime factors: \\(36 = 2^2 \\times 3^2\\) and \\(84 = 2^2 \\times 3 \\times 7\\). Shared primes: 2 and 3."),
   b("Shared power of 2, the lower of 2 and 2, is ", 2, "Both have two 2s. Take that count, 2."),
   b("Shared power of 3, the lower of 2 and 1, is ", 1, "36 has two 3s, 84 has one. Take the lower."),
   s("So HCF = 2² × 3 = 4 × 3."),
   b("4 × 3 = ", 12, "Multiply.", phase="substitute"),
   b("Check: 84 ÷ 12 = ", 7, "Does 12 go into 84?", done="12 divides both 36 and 84 exactly, so HCF = 12."),
 ],
})

# S2: LCM(15,20) = 60
silver.append({
 "display": "Find the LCM of \\(15\\) and \\(20\\)",
 "solutions": [60],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Highest power of each prime: 2², 3, 5.",
 "misconceptions": [
   mc("multiply", 300, "15 × 20 = 300, but the LCM = 60. Use primes: 15 = 3 × 5, 20 = 2² × 5, so LCM = 2² × 3 × 5 = 60."),
   mc("hcf_not_lcm", 5, "5 is the HCF, not the LCM."),
 ],
 "guided_steps": [
   s("Primes: \\(15 = 3 \\times 5\\) and \\(20 = 2^2 \\times 5\\). Highest powers: 2² from 20, 3 from 15, 5 from either."),
   b("Work out 2² = ", 4, "2 × 2."),
   b("Multiply by the 3: 4 × 3 = ", 12, "Multiply."),
   b("Now bring in the 5: 12 × 5 = ", 60, "Multiply by 5.", phase="substitute"),
   b("Check: 60 ÷ 20 = ", 3, "Does 20 go into 60?", done="60 divides by both 15 and 20 and is the smallest that does, so LCM = 60."),
 ],
})

# S3: HCF(72,120) = 24
silver.append({
 "display": "Find the HCF of \\(72\\) and \\(120\\)",
 "solutions": [24],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Shared primes at their lowest power: 2³ and 3.",
 "misconceptions": [
   mc("wrong_factorisation", None, "72 = 2³ × 3² and 120 = 2³ × 3 × 5. Shared: 2³ × 3 = 24."),
   mc("lcm_not_hcf", 360, "360 is the LCM. The HCF uses the lowest powers of the shared primes."),
 ],
 "guided_steps": [
   s("Prime factors: \\(72 = 2^3 \\times 3^2\\) and \\(120 = 2^3 \\times 3 \\times 5\\). Shared primes: 2 and 3."),
   b("Shared power of 2, the lower of 3 and 3, is ", 3, "Both have three 2s. Take 3."),
   b("Shared power of 3, the lower of 2 and 1, is ", 1, "72 has two 3s, 120 has one. Take the lower."),
   s("So HCF = 2³ × 3 = 8 × 3."),
   b("8 × 3 = ", 24, "Multiply.", phase="substitute"),
   b("Check: 120 ÷ 24 = ", 5, "Does 24 go into 120?", done="24 divides both 72 and 120 exactly, so HCF = 24."),
 ],
})

# S4: LCM(18,24) = 72   (wrong_powers expect fixed to 6 per audit)
silver.append({
 "display": "Find the LCM of \\(18\\) and \\(24\\)",
 "solutions": [72],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Highest power of each prime: 2³ from 24 and 3² from 18.",
 "misconceptions": [
   mc("multiply", 432, "18 × 24 = 432, but the LCM is smaller. 18 = 2 × 3², 24 = 2³ × 3, so LCM = 2³ × 3² = 72."),
   mc("wrong_powers", 6, "6 is the HCF. For the LCM, use the highest power of each prime: 2³ from 24 and 3² from 18, giving 8 × 9 = 72."),
 ],
 "guided_steps": [
   s("Primes: \\(18 = 2 \\times 3^2\\) and \\(24 = 2^3 \\times 3\\). Highest powers: 2³ from 24, 3² from 18."),
   b("Work out 2³ = ", 8, "2 × 2 × 2."),
   b("Work out 3² = ", 9, "3 × 3."),
   b("Multiply them: 8 × 9 = ", 72, "Multiply.", phase="substitute"),
   b("Check: 72 ÷ 24 = ", 3, "Does 24 go into 72?", done="72 divides by both 18 and 24 and is the smallest that does, so LCM = 72."),
 ],
})

# S5: 1080, sum of indices = 7   (changed from 360, whose index-product equalled its index-sum)
silver.append({
 "display": "Write \\(1080\\) as a product of prime factors. What is the sum of all the index values?",
 "solutions": [7],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Factorise 1080, then ADD the powers.",
 "misconceptions": [
   mc("wrong_tree", None, "1080 = 2³ × 3³ × 5¹. Sum of indices: 3 + 3 + 1 = 7."),
   mc("multiply_indices", 9, "Add the index values, do not multiply them: 3 + 3 + 1 = 7 (multiplying gives 9)."),
 ],
 "guided_steps": [
   s("Factor 1080 into primes. Peel off 2s, then 3s, then what is left."),
   b("1080 ÷ 2 = ", 540, "Halve 1080."),
   b("540 ÷ 2 = ", 270, "Halve 540."),
   b("270 ÷ 2 = ", 135, "Halve 270. 135 is odd, so the 2s stop: three 2s."),
   s("135 = 3 × 3 × 3 × 5, so 1080 = \\(2^3 \\times 3^3 \\times 5^1\\). The indices are 3, 3 and 1."),
   b("Sum of the indices: 3 + 3 + 1 = ", 7, "Add the three powers.", phase="substitute"),
   b("Check: 8 × 27 × 5 = ", 1080, "2³ = 8, 3³ = 27, then × 5.", done="2³ × 3³ × 5 rebuilds 1080, so the index sum is 7."),
 ],
})

# S6: LCM(9,15) = 45
silver.append({
 "display": "Find the LCM of \\(9\\) and \\(15\\)",
 "solutions": [45],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Highest power of each prime: 3² from 9 and 5 from 15.",
 "misconceptions": [
   mc("multiply", 135, "9 × 15 = 135, but the LCM = 45. 9 = 3², 15 = 3 × 5, so LCM = 3² × 5 = 45."),
   mc("hcf_not_lcm", 3, "3 is the HCF. The LCM = 45."),
 ],
 "guided_steps": [
   s("Primes: \\(9 = 3^2\\) and \\(15 = 3 \\times 5\\). Highest powers: 3² from 9, and 5 from 15."),
   b("Work out 3² = ", 9, "3 × 3."),
   b("Multiply by the 5: 9 × 5 = ", 45, "Multiply by 5.", phase="substitute"),
   b("Check: 45 ÷ 15 = ", 3, "Does 15 go into 45?", done="45 divides by both 9 and 15 and is the smallest that does, so LCM = 45."),
 ],
})

# ---------------- GOLD ----------------
gold = []

# G0: HCF(48,180) = 12
gold.append({
 "display": "Find the HCF and LCM of \\(48\\) and \\(180\\). What is the HCF?",
 "solutions": [12],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Write both as products of primes: 48 = 2⁴ × 3, 180 = 2² × 3² × 5, then take shared lowest powers.",
 "misconceptions": [
   mc("wrong_factorisation", None, "48 = 2⁴ × 3 and 180 = 2² × 3² × 5. Shared: 2² × 3 = 12."),
   mc("lcm_not_hcf", 720, "720 is the LCM. The HCF = 12."),
 ],
 "guided_steps": [
   s("Prime factors: \\(48 = 2^4 \\times 3\\) and \\(180 = 2^2 \\times 3^2 \\times 5\\). Shared primes: 2 and 3."),
   b("Shared power of 2, the lower of 4 and 2, is ", 2, "48 has four 2s, 180 has two. Take the lower."),
   b("Shared power of 3, the lower of 1 and 2, is ", 1, "48 has one 3, 180 has two. Take the lower."),
   s("So HCF = 2² × 3 = 4 × 3."),
   b("4 × 3 = ", 12, "Multiply.", phase="substitute"),
   b("Check: 48 ÷ 12 = ", 4, "Does 12 go into 48?", done="12 divides both 48 and 180 exactly, so the HCF is 12."),
 ],
})

# G1: HCF 6, LCM 120, one number 24, find other = 30
gold.append({
 "display": "The HCF of two numbers is 6 and their LCM is 120. One number is 24. Find the other.",
 "solutions": [30],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Use HCF × LCM = the product of the two numbers.",
 "misconceptions": [
   mc("wrong_formula", None, "HCF × LCM = the product of the two numbers. So 6 × 120 = 24 × other, giving other = 30."),
   mc("product_is_lcm", 5, "That treats the LCM as the product of the numbers. It is not: HCF × LCM = 6 × 120 = 720 = 24 × other, so other = 720 ÷ 24 = 30."),
 ],
 "guided_steps": [
   s("Use the rule HCF × LCM = the product of the two numbers."),
   b("HCF × LCM = 6 × 120 = ", 720, "Multiply 6 by 120."),
   s("That product equals the two numbers multiplied: 24 × other = 720."),
   b("Other number = 720 ÷ 24 = ", 30, "Divide 720 by 24.", phase="substitute"),
   b("Check: 24 × 30 = ", 720, "Multiply 24 by 30.", done="24 × 30 = 720 = 6 × 120, so the other number is 30."),
 ],
})

# G2: 2^3 x 3 x 5^2 = 600  (multiply_indices duplicate removed; index_error kept with expect 180)
gold.append({
 "display": "Write \\(2^3 \\times 3 \\times 5^2\\) as a whole number",
 "solutions": [600],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Work out each prime power first, then multiply.",
 "misconceptions": [
   mc("index_error", 180, "You multiplied the base by the index instead of raising to a power. 2³ means 2 × 2 × 2 = 8 (not 2 × 3 = 6), and 5² means 5 × 5 = 25. So 8 × 3 × 25 = 600."),
 ],
 "guided_steps": [
   s("Work out each prime power first, then multiply. Remember 2³ means 2 × 2 × 2, not 2 × 3."),
   b("2³ = 2 × 2 × 2 = ", 8, "Double twice: 2, 4, 8."),
   b("5² = 5 × 5 = ", 25, "5 times 5."),
   s("The middle term is just 3, so the product is 8 × 3 × 25."),
   b("Multiply up: 8 × 3 × 25 = ", 600, "8 × 3 = 24, then 24 × 25 = 600.", phase="substitute"),
   b("Check by dividing back: 600 ÷ 25 = ", 24, "600 ÷ 25.", done="600 ÷ 25 = 24 = 8 × 3, which matches 2³ × 3, so 600 is right."),
 ],
})

# G3: LCM(12,18,30) = 180
gold.append({
 "display": "Find the LCM of \\(12\\), \\(18\\) and \\(30\\)",
 "solutions": [180],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Factorise all three, then take the highest power of each prime.",
 "misconceptions": [
   mc("pair_only", None, "Use all three numbers. Factorise each and take the highest power of every prime that appears: 2² × 3² × 5 = 180."),
   mc("multiply_all", 6480, "Do not just multiply all three (12 × 18 × 30 = 6480). Use prime factorisations with highest powers: 180."),
 ],
 "guided_steps": [
   s("Three numbers now. Factorise each: \\(12 = 2^2 \\times 3\\), \\(18 = 2 \\times 3^2\\), \\(30 = 2 \\times 3 \\times 5\\). LCM takes the highest power of every prime that appears: 2², 3², 5."),
   b("Highest power of 2 is 2² = ", 4, "12 has the most 2s: two of them, 2² = 4."),
   b("Highest power of 3 is 3² = ", 9, "18 has the most 3s: two, 3² = 9."),
   s("The highest power of 5 is just 5 (only 30 has it). So LCM = 4 × 9 × 5."),
   b("Multiply up: 4 × 9 × 5 = ", 180, "4 × 9 = 36, then × 5 = 180.", phase="substitute"),
   b("Check: 180 ÷ 30 = ", 6, "Does 30 go into 180?", done="180 divides by 12, 18 and 30, and is the smallest such number, so LCM = 180."),
 ],
})

# G4: buses LCM(12,18) = 36  (reworded to ask for minutes)
gold.append({
 "display": "Two buses leave a station at 9 am. Bus A runs every 12 minutes, Bus B every 18 minutes. How many minutes after 9 am do they next leave together?",
 "solutions": [36],
 "calculator": False,
 "input_type": "single_value",
 "hint": "Find the LCM of 12 and 18, which gives the number of minutes.",
 "misconceptions": [
   mc("hcf_not_lcm", 6, "6 is the HCF. You need the LCM, the first time they coincide: LCM(12, 18) = 36 minutes."),
   mc("multiply", 216, "12 × 18 = 216, but the LCM is 36. They next leave together after 36 minutes."),
 ],
 "guided_steps": [
   s("They leave together again after the Lowest Common Multiple of 12 and 18 minutes."),
   s("Primes: \\(12 = 2^2 \\times 3\\) and \\(18 = 2 \\times 3^2\\). Highest powers: 2² and 3²."),
   b("Work out 2² = ", 4, "2 × 2."),
   b("Work out 3² = ", 9, "3 × 3."),
   b("LCM = 4 × 9 = ", 36, "Multiply.", phase="substitute"),
   b("Check: 36 ÷ 12 = ", 3, "Does 12 go into 36?", done="36 ÷ 12 = 3 and 36 ÷ 18 = 2, both whole, so they next leave together after 36 minutes."),
 ],
})

# ---------------- assemble problem_bank ----------------
pb = {
 "gold": gold,
 "bronze": bronze,
 "silver": silver,
 "bronze_description": "Prime factorise small numbers and find the HCF or LCM of a simple pair by inspection.",
 "silver_description": "Factorise larger numbers in index form and pick HCF (lowest powers) or LCM (highest powers) correctly.",
 "gold_description": "Multi-number LCM, the HCF × LCM product rule, index-to-number expansion, and worded problems.",
}

# ---------------- tier_guides ----------------
def ex(question, steps):
    return {"question": question, "steps": steps}

tier_guides = {
 "bronze": {
  "title": "Bronze: prime factors and simple HCF/LCM",
  "steps": [
    "<strong>Prime factorise</strong> with a factor tree: keep splitting until every end is a prime, then write it in index form, e.g. \\(12 = 2^2 \\times 3\\).",
    "<strong>HCF</strong> (Highest Common Factor) is the biggest number that divides into both. <strong>LCM</strong> (Lowest Common Multiple) is the smallest number both divide into.",
    "For small numbers, spot the HCF by testing shared factors, and the LCM by listing multiples until they first match.",
  ],
  "example": ex("Find the LCM of 6 and 8", [
    {"label": "Prime factors", "content": "<p>\\(6 = 2 \\times 3\\) and \\(8 = 2^3\\)</p>"},
    {"label": "Highest powers", "content": "<p>Highest power of 2 is \\(2^3 = 8\\); highest power of 3 is 3.</p>"},
    {"label": "Check", "content": "<p>\\(8 \\times 3 = 24\\). And \\(24 \\div 6 = 4\\), \\(24 \\div 8 = 3\\), both whole.</p>"},
    {"label": "Answer", "content": "<p>LCM = <strong>24</strong></p>", "isAnswer": True, "is_answer": True},
  ]),
 },
 "silver": {
  "title": "Silver: index notation and choosing HCF vs LCM",
  "steps": [
    "Write bigger numbers as products of primes in <strong>index form</strong>, e.g. \\(180 = 2^2 \\times 3^2 \\times 5\\).",
    "<strong>HCF</strong>: multiply the shared primes at their <strong>lowest</strong> power. <strong>LCM</strong>: multiply every prime that appears at its <strong>highest</strong> power.",
    "Read the question carefully: HCF gives a factor (smaller), LCM gives a multiple (larger). Do not just multiply the two numbers unless they share no factors.",
  ],
  "example": ex("Find the HCF of 60 and 90", [
    {"label": "Prime factors", "content": "<p>\\(60 = 2^2 \\times 3 \\times 5\\) and \\(90 = 2 \\times 3^2 \\times 5\\)</p>"},
    {"label": "Shared primes, lowest powers", "content": "<p>Shared: 2, 3, 5. Lowest powers: \\(2^1\\), \\(3^1\\), \\(5^1\\).</p>"},
    {"label": "Check", "content": "<p>\\(2 \\times 3 \\times 5 = 30\\). And \\(60 \\div 30 = 2\\), \\(90 \\div 30 = 3\\), both whole.</p>"},
    {"label": "Answer", "content": "<p>HCF = <strong>30</strong></p>", "isAnswer": True, "is_answer": True},
  ]),
 },
 "gold": {
  "title": "Gold: multi-number LCM and the HCF × LCM rule",
  "steps": [
    "For three numbers, factorise all of them and take the <strong>highest power</strong> of every prime that appears in any of them.",
    "Use the shortcut <strong>HCF × LCM = the product of the two numbers</strong> to find a missing number.",
    "To turn index form into a whole number, work out each power first (\\(2^3 = 8\\), not \\(2 \\times 3\\)) then multiply.",
  ],
  "example": ex("Find the LCM of 8, 12 and 30", [
    {"label": "Prime factors", "content": "<p>\\(8 = 2^3\\), \\(12 = 2^2 \\times 3\\), \\(30 = 2 \\times 3 \\times 5\\)</p>"},
    {"label": "Highest powers", "content": "<p>\\(2^3\\) (from 8), \\(3^1\\) (from 12 or 30), \\(5^1\\) (from 30).</p>"},
    {"label": "Check", "content": "<p>\\(8 \\times 3 \\times 5 = 120\\). It divides by 8, 12 and 30.</p>"},
    {"label": "Answer", "content": "<p>LCM = <strong>120</strong></p>", "isAnswer": True, "is_answer": True},
  ]),
 },
}

# ---------------- guided (opener + teach) ----------------
guided = {
 "opener": {
  "label": "Before any method",
  "display": "12 red roses, 8 white roses<br>identical bunches, none left over",
  "steps": [
    s("Two quick puzzles, no method needed, just common sense."),
    b("Largest number of identical bunches = ", 4, "Try it: can you make 4 bunches? 12 ÷ 4 = 3 red and 8 ÷ 4 = 2 white each. Could you make more?"),
    s("That number, the biggest that divides BOTH amounts exactly, is the <strong>Highest Common Factor (HCF)</strong> of 12 and 8."),
    b("A lighthouse flashes every 4 seconds, a buoy every 6 seconds. They just flashed together. After how many seconds do they next flash together? ", 12, "List the times: lighthouse at 4, 8, 12; buoy at 6, 12. When do they first meet again?"),
    s("The flashes first line up again at the <strong>Lowest Common Multiple (LCM)</strong>. For small numbers you can just list them. For bigger numbers the fast route is to break each into its prime building blocks, e.g. \\(12 = 2^2 \\times 3\\), and that is exactly what this lesson trains."),
  ],
 },
 "teach": {
  "bronze": {
   "display": "Find the HCF of \\(8\\) and \\(20\\)",
   "label": "Together: your first one",
   "steps": [
     s("Break each number into its prime building blocks."),
     b("8 = 2 × 2 × 2, so the number of 2s in 8 is ", 3, "Count the 2s: 8 = 2 × 2 × 2."),
     b("20 = 2 × 2 × 5, so the number of 2s in 20 is ", 2, "20 = 4 × 5 = 2 × 2 × 5."),
     s("HCF takes each shared prime at its lower count. For 2, the lower of 3 and 2 is 2, so 2 × 2. There are no shared 5s, since only 20 has a 5."),
     b("2 × 2 = ", 4, "Multiply the two shared 2s."),
     b("Check: 20 ÷ 4 = ", 5, "Does 4 go into 20?", done="4 divides both 8 and 20 exactly, and nothing larger does. That was the whole point: match the shared primes."),
   ],
  },
  "silver": {
   "display": "Find the LCM of \\(24\\) and \\(36\\)",
   "label": "Together: the silver move",
   "steps": [
     s("Write each in index form: \\(24 = 2^3 \\times 3\\) and \\(36 = 2^2 \\times 3^2\\)."),
     b("Highest power of 2 is 2³. Work it out: 2³ = ", 8, "2 × 2 × 2."),
     b("Highest power of 3 is 3². Work it out: 3² = ", 9, "3 × 3."),
     s("The LCM multiplies those highest powers together."),
     b("8 × 9 = ", 72, "Multiply."),
     b("Check: 72 ÷ 24 = ", 3, "Does 24 go into 72?", done="72 ÷ 24 = 3 and 72 ÷ 36 = 2, both whole, so LCM = 72. The new move: choose the HIGHEST power of each prime."),
   ],
  },
  "gold": {
   "display": "The HCF of two numbers is \\(4\\) and their LCM is \\(60\\). One number is \\(12\\). Find the other.",
   "label": "Together: the gold move",
   "steps": [
     s("The new tool: HCF × LCM = the product of the two numbers."),
     b("HCF × LCM = 4 × 60 = ", 240, "Multiply 4 by 60."),
     s("So 12 × other = 240."),
     b("Other = 240 ÷ 12 = ", 20, "Divide 240 by 12."),
     s("Check it by factorising: \\(12 = 2^2 \\times 3\\) and \\(20 = 2^2 \\times 5\\)."),
     b("HCF is the shared 2² = ", 4, "Both have 2², nothing else shared."),
     b("LCM is 2² × 3 × 5 = ", 60, "4 × 3 × 5.", done="HCF 4 and LCM 60 both check out, so the other number is 20. That was the whole point: the product rule finds a missing number fast."),
   ],
  },
 },
}

# ---------------- method_card (slim) ----------------
method_card = {
 "title": "How to Find HCF, LCM and Prime Factorisations",
 "steps": live["method_card"]["steps"],
 "content": "<p><strong>Prime factorisation</strong> writes a number as a product of primes, e.g. \\(60 = 2^2 \\times 3 \\times 5\\). Use a factor tree and record it in index form.</p><p><strong>HCF</strong> (Highest Common Factor): factorise both numbers, then multiply the shared primes at their <em>lowest</em> power.</p><p><strong>LCM</strong> (Lowest Common Multiple): multiply every prime that appears in either number at its <em>highest</em> power.</p><p>Quick check: HCF × LCM = the product of the two numbers.</p>",
 "example": dedash(live["method_card"]["example"]),
}

# ---------------- final object ----------------
out = {
 "method_card": method_card,
 "topic_links": live["topic_links"],
 "problem_bank": pb,
 "tier_guides": tier_guides,
 "guided": guided,
 "related_videos": live["related_videos"],
 "worked_examples": dedash(live["worked_examples"]),
}

json.dump(out, io.open("lesson_number-L04.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_number-L04.json")

# quick self-checks
for tier, probs in (("bronze", bronze), ("silver", silver), ("gold", gold)):
    sols = [tuple(p["solutions"]) for p in probs]
    assert len(sols) == len(set(sols)), (tier, "DUPLICATE SOLUTION", sols)
print("no duplicate solutions within any tier")
print("counts bronze/silver/gold:", len(bronze), len(silver), len(gold))
