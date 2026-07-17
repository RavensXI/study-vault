# -*- coding: utf-8 -*-
import json, io

# ---------- opener figure: 12 cupcakes in 4 rows of 3 ----------
xs = [40, 90, 140]
ys = [35, 80, 125, 170]
circ = ""
for y in ys:
    for x in xs:
        circ += ('<circle cx="%d" cy="%d" r="16" fill="#f59e0b" fill-opacity="0.3" '
                 'stroke="currentColor" stroke-width="1.5"/>') % (x, y)
opener_svg = ('<svg viewBox="0 0 180 205" role="img" aria-label="Twelve cupcakes '
              'arranged in four rows of three">' + circ + '</svg>')

def box(pre, answer, hint, phase=None, done=None, say=None, post=""):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase: d["phase"] = phase
    if done: d["done"] = done
    if say: d["say"] = say
    return d
def say(s): return {"say": s}

# ============================ PROBLEM BANK ============================
bronze = [
 {"display":"How many factors does 12 have?","solutions":[6],"calculator":False,
  "input_type":"single_value",
  "hint":"List every factor pair of 12 and count them all, including 1 and 12.",
  "misconceptions":[{"pattern":"drop_ends","message":"Include 1 and the number itself. The factors of 12 are 1, 2, 3, 4, 6 and 12, which is 6 factors.","expect":4,"note":"student drops 1 and 12"}],
  "guided_steps":[
    say("Factors come in pairs that multiply to 12. Find every pair."),
    box("The first pair is 1 × 12. The next pair starts with 2, and 12 ÷ 2 = ",6,"Divide 12 by 2."),
    box("The next factor to try is 3, and 12 ÷ 3 = ",4,"Divide 12 by 3."),
    say("4 was already found (in 3 × 4), so the pairs stop: 1×12, 2×6, 3×4."),
    box("Count all the distinct factors 1, 2, 3, 4, 6, 12. That is ",6,"Count the six numbers.",phase="substitute"),
    box("Check they pair up: 3 pairs, so 3 × 2 = ",6,"Three pairs, two each.",done="Three factor pairs give six factors, so 12 has 6 factors.")]},
 {"display":"What is the 7th multiple of 6?","solutions":[42],"calculator":False,
  "input_type":"single_value",
  "hint":"The nth multiple of 6 is 6 × n, so use 6 × 7.",
  "misconceptions":[{"pattern":"off_by_one","message":"The 7th multiple is 6 × 7 = 42. 6 × 6 = 36 is only the 6th multiple.","expect":36}],
  "guided_steps":[
    say("A multiple of 6 is 6 times a whole number. The 7th one uses 7."),
    box("Write the multiplication: the 7th multiple is 6 × ",7,"The 7th multiple uses 7."),
    box("Work it out: 6 × 7 = ",42,"Seven sixes.",phase="substitute"),
    box("Check by counting in sixes to the 7th: 6, 12, 18, 24, 30, 36, then ",42,"One more six after 36.",done="The 7th number in the six times table is 42.")]},
 {"display":"Is 29 prime? Enter 1 for yes, 0 for no.","solutions":[1],"calculator":False,
  "input_type":"single_value",
  "hint":"Test whether 29 divides by 2, 3 or 5; if none work, it is prime.",
  "misconceptions":[{"pattern":"not_prime","message":"29 has no factors except 1 and 29 (it is not divisible by 2, 3 or 5), so it is prime: enter 1.","expect":0}],
  "guided_steps":[
    say("A prime has exactly two factors, 1 and itself. Test 29 against small primes."),
    box("Does 2 divide 29 exactly? Enter 1 for yes, 0 for no: ",0,"29 is odd, so 2 does not divide it."),
    box("Does 3 divide 29? The digit sum 2+9 = 11 is not a multiple of 3. Enter 1 or 0: ",0,"11 is not in the 3 times table.",phase="substitute"),
    box("Does 5 divide 29? Enter 1 or 0: ",0,"29 does not end in 0 or 5."),
    say("We only need primes up to \\(\\sqrt{29}\\approx 5.4\\), so 2, 3 and 5 are enough."),
    box("No prime divides it, so 29 is prime. Enter 1: ",1,"No factors found means prime.",done="No prime up to \\(\\sqrt{29}\\) divides it, so 29 is prime.")]},
 {"display":"Find the HCF of 8 and 12","solutions":[4],"calculator":False,
  "input_type":"single_value",
  "hint":"List the factors of each number and pick the largest they share.",
  "misconceptions":[{"pattern":"use_lcm","message":"That is the LCM. The HCF is the largest shared factor: factors of 8 are 1, 2, 4, 8 and of 12 are 1, 2, 3, 4, 6, 12, so HCF = 4.","expect":24}],
  "guided_steps":[
    say("List the factors of each number, then find the biggest they share."),
    box("The factors of 8 are 1, 2, 4 and ",8,"8 divides itself."),
    box("The factors of 12 are 1, 2, 3, 4, 6 and ",12,"12 divides itself."),
    say("Shared factors are 1, 2 and 4."),
    box("The highest shared factor is ",4,"The biggest number in both lists.",phase="substitute"),
    box("Check 4 divides both: 8 ÷ 4 = 2 and 12 ÷ 4 = ",3,"12 shared into fours.",done="4 divides both and nothing larger does, so HCF = 4.")]},
 {"display":"Find the LCM of 4 and 6","solutions":[12],"calculator":False,
  "input_type":"single_value",
  "hint":"List multiples of 4 and of 6, then take the first one in both lists.",
  "misconceptions":[{"pattern":"multiply","message":"The LCM is not always the product. Multiples of 4 are 4, 8, 12; of 6 are 6, 12. The first shared one is 12, not 24.","expect":24}],
  "guided_steps":[
    say("List the multiples of each until one appears in both lists."),
    box("The first four multiples of 4 are 4, 8, 12 and ",16,"Add 4 to 12."),
    box("The first three multiples of 6 are 6, 12 and ",18,"Add 6 to 12."),
    box("The smallest number in both lists is ",12,"The earliest shared multiple.",phase="substitute"),
    box("Check 12 is in both tables: 12 ÷ 4 = 3 and 12 ÷ 6 = ",2,"12 shared into sixes.",done="12 is the first common multiple, so LCM = 12.")]},
 {"display":"Express 36 as a product of prime factors. How many times does 2 appear?","solutions":[2],"calculator":False,
  "input_type":"single_value",
  "hint":"Split 36 into primes and count only the 2s.",
  "misconceptions":[{"pattern":"count_all","message":"Count only the 2s. 36 = 2 × 2 × 3 × 3, so 2 appears twice, even though there are four prime factors in all.","expect":4}],
  "guided_steps":[
    say("Break 36 down with a factor tree, splitting off primes."),
    box("Start: 36 = 2 × ",18,"36 ÷ 2."),
    box("18 = 2 × ",9,"18 ÷ 2."),
    say("9 = 3 × 3, both prime, so 36 = 2 × 2 × 3 × 3 = \\(2^2\\times 3^2\\)."),
    box("Count how many 2s are in 2 × 2 × 3 × 3: ",2,"Two 2s.",phase="substitute"),
    box("Check the product rebuilds 36: 2 × 2 × 3 × 3 = ",36,"4 × 9.",done="36 = \\(2^2\\times 3^2\\), so 2 appears twice.")]},
 {"display":"Find the HCF of 15 and 20","solutions":[5],"calculator":False,
  "input_type":"single_value",
  "hint":"List the factors of 15 and 20 and take the biggest shared one.",
  "misconceptions":[{"pattern":"use_lcm","message":"That is the LCM. The shared factors of 15 and 20 are 1 and 5, so the HCF is 5.","expect":60}],
  "guided_steps":[
    say("List factors of each and take the largest shared one."),
    box("The factors of 15 are 1, 3, 5 and ",15,"15 divides itself."),
    box("The factors of 20 are 1, 2, 4, 5, 10 and ",20,"20 divides itself."),
    say("The only shared factors are 1 and 5."),
    box("The highest shared factor is ",5,"The bigger of 1 and 5.",phase="substitute"),
    box("Check: 15 ÷ 5 = 3 and 20 ÷ 5 = ",4,"20 shared into fives.",done="5 divides both and nothing larger does, so HCF = 5.")]},
 {"display":"Find the LCM of 3 and 5","solutions":[15],"calculator":False,
  "input_type":"single_value",
  "hint":"3 and 5 share no factors, so multiply them for the LCM.",
  "misconceptions":[{"pattern":"use_hcf","message":"That is the HCF. 3 and 5 share no factors, so the LCM is their product, 3 × 5 = 15.","expect":1}],
  "guided_steps":[
    say("3 and 5 share no common factor, so their LCM is simply their product."),
    box("List multiples of 3 up to 15: 3, 6, 9, 12 and ",15,"Add 3 to 12."),
    box("List multiples of 5 up to 15: 5, 10 and ",15,"Add 5 to 10."),
    box("The first value in both lists is ",15,"The earliest shared multiple.",phase="substitute"),
    box("Since 3 and 5 share no factors, LCM = 3 × 5 = ",15,"Multiply them.",done="15 is the first common multiple and equals 3 × 5.")]},
]

silver = [
 {"display":"Find the HCF of 48 and 60","solutions":[12],"calculator":False,
  "input_type":"single_value",
  "hint":"Prime factorise both, then multiply the shared primes at their lowest powers.",
  "misconceptions":[{"pattern":"use_lcm","message":"That is the LCM. For the HCF take the shared primes at their lowest powers: \\(2^2\\times 3 = 12\\).","expect":240}],
  "guided_steps":[
    say("Prime factorise both, then take shared primes at their lowest powers."),
    box("48 = \\(2^4\\times 3\\), so the power of 2 in 48 is ",4,"48 = 2×2×2×2×3."),
    box("60 = \\(2^2\\times 3\\times 5\\), so the power of 2 in 60 is ",2,"60 = 2×2×3×5."),
    say("For HCF take each shared prime at its lower power: \\(2^2\\) (the smaller) and 3 (in both)."),
    box("Multiply the shared primes: \\(2^2\\times 3\\) = ",12,"4 × 3.",phase="substitute"),
    box("Check 12 divides both: 48 ÷ 12 = 4 and 60 ÷ 12 = ",5,"60 shared into twelves.",done="12 uses the lowest shared powers, so HCF = 12.")]},
 {"display":"Find the LCM of 8 and 14","solutions":[56],"calculator":False,
  "input_type":"single_value",
  "hint":"Prime factorise both, then multiply every prime at its highest power.",
  "misconceptions":[{"pattern":"multiply","message":"Do not just multiply. 8 = \\(2^3\\) and 14 = 2 × 7 share a 2, so LCM = \\(2^3\\times 7 = 56\\), not 112.","expect":112}],
  "guided_steps":[
    say("Prime factorise both, then take every prime at its highest power."),
    box("8 = \\(2^3\\), so the power of 2 in 8 is ",3,"8 = 2×2×2."),
    box("14 = 2 × 7. The new prime that 8 did not have is ",7,"14 = 2 × 7."),
    say("Highest powers: \\(2^3\\) (from 8) and 7 (from 14)."),
    box("Multiply: \\(2^3\\times 7\\) = ",56,"8 × 7.",phase="substitute"),
    box("Check both divide 56: 56 ÷ 8 = 7 and 56 ÷ 14 = ",4,"56 shared into fourteens.",done="56 uses the highest powers, so LCM = 56.")]},
 {"display":"Find the LCM of 12 and 18","solutions":[36],"calculator":False,
  "input_type":"single_value",
  "hint":"Prime factorise both, then take each prime at its highest power.",
  "misconceptions":[{"pattern":"multiply","message":"Multiplying gives 216, but they share factors. 12 = \\(2^2\\times 3\\) and 18 = \\(2\\times 3^2\\), so LCM = \\(2^2\\times 3^2 = 36\\).","expect":216}],
  "guided_steps":[
    say("Prime factorise both, then take each prime at its highest power."),
    box("12 = \\(2^2\\times 3\\), so the power of 2 in 12 is ",2,"12 = 2×2×3."),
    box("18 = \\(2\\times 3^2\\), so the power of 3 in 18 is ",2,"18 = 2×3×3."),
    say("Highest powers: \\(2^2\\) (from 12) and \\(3^2\\) (from 18)."),
    box("Multiply: \\(2^2\\times 3^2\\) = ",36,"4 × 9.",phase="substitute"),
    box("Check both divide 36: 36 ÷ 12 = 3 and 36 ÷ 18 = ",2,"36 shared into eighteens.",done="36 uses the highest powers, so LCM = 36.")]},
 {"display":"Express 180 as a product of prime factors. What is the sum of all distinct primes used?","solutions":[10],"calculator":False,
  "input_type":"single_value",
  "hint":"Prime factorise 180, then add the different primes (do not multiply).",
  "misconceptions":[
    {"pattern":"product","message":"Add, do not multiply. The distinct primes 2, 3 and 5 sum to 10, not 30.","expect":30},
    {"pattern":"count_repeats","message":"Use distinct primes only. 180 = \\(2^2\\times 3^2\\times 5\\), so add 2 + 3 + 5 = 10, not the repeats.","expect":15}],
  "guided_steps":[
    say("Prime factorise 180, then add the different primes."),
    box("180 ÷ 2 = 90 and 90 ÷ 2 = 45, so 180 = \\(2^2\\times 45\\). Now 45 ÷ 9 = ",5,"45 = 9 × 5."),
    say("So 45 = \\(3^2\\times 5\\), giving 180 = \\(2^2\\times 3^2\\times 5\\). Distinct primes: 2, 3, 5."),
    box("Add the first two distinct primes: 2 + 3 = ",5,"2 plus 3."),
    box("Add the last: 5 + 5 = ",10,"Add the final 5.",phase="substitute"),
    box("Check the factorisation: \\(2^2\\times 3^2\\times 5\\) = 4 × 9 × 5 = ",180,"36 × 5.",done="Distinct primes 2, 3, 5 sum to 10.")]},
 {"display":"Find the HCF of 36 and 90","solutions":[18],"calculator":False,
  "input_type":"single_value",
  "hint":"Prime factorise both, then multiply the shared primes at their lowest powers.",
  "misconceptions":[{"pattern":"use_lcm","message":"That is the LCM. The HCF uses the lowest shared powers: \\(2\\times 3^2 = 18\\).","expect":180}],
  "guided_steps":[
    say("Prime factorise both, then take shared primes at their lowest powers."),
    box("36 = \\(2^2\\times 3^2\\), so the power of 3 in 36 is ",2,"36 = 2×2×3×3."),
    box("90 = \\(2\\times 3^2\\times 5\\), so the power of 2 in 90 is ",1,"90 = 2×3×3×5, one 2."),
    say("Shared primes at lowest powers: \\(2^1\\) (lower than \\(2^2\\)) and \\(3^2\\) (in both)."),
    box("Multiply: \\(2\\times 3^2\\) = ",18,"2 × 9.",phase="substitute"),
    box("Check 18 divides both: 36 ÷ 18 = 2 and 90 ÷ 18 = ",5,"90 shared into eighteens.",done="18 uses the lowest shared powers, so HCF = 18.")]},
 {"display":"Two buses leave a station together. One returns every 12 minutes, the other every 15 minutes. How many minutes until they're both at the station together?","solutions":[60],"calculator":False,
  "input_type":"single_value",
  "hint":"They meet again at the LCM of 12 and 15, not the HCF.",
  "misconceptions":[{"pattern":"use_hcf","message":"The next time together is the LCM, not the HCF. LCM(12, 15) = 60 minutes, not 3.","expect":3}],
  "guided_steps":[
    say("They meet again at the LCM of their intervals, 12 and 15."),
    box("12 = \\(2^2\\times 3\\), so the power of 2 in 12 is ",2,"12 = 2×2×3."),
    box("15 = 3 × 5. The new prime that 12 did not have is ",5,"15 = 3 × 5."),
    say("Highest powers across both: \\(2^2\\) (from 12), 3 (in both), 5 (from 15)."),
    box("Multiply: \\(2^2\\times 3\\times 5\\) = ",60,"4 × 15.",phase="substitute"),
    box("Check both intervals divide 60: 60 ÷ 12 = 5 and 60 ÷ 15 = ",4,"60 shared into fifteens.",done="60 is the first shared minute, so they meet after 60 minutes.")]},
 {"display":"Find the HCF of 24, 40 and 56","solutions":[8],"calculator":False,
  "input_type":"single_value",
  "hint":"Prime factorise all three, then take the primes shared by all at their lowest powers.",
  "misconceptions":[{"pattern":"use_lcm","message":"That is the LCM. The HCF is the primes shared by all three at lowest powers: \\(2^3 = 8\\).","expect":840}],
  "guided_steps":[
    say("Prime factorise all three, then take primes shared by all at their lowest powers."),
    box("24 = \\(2^3\\times 3\\), so the power of 2 in 24 is ",3,"24 = 2×2×2×3."),
    box("40 = \\(2^3\\times 5\\) and 56 = \\(2^3\\times 7\\). The power of 2 shared by all three is ",3,"All three have exactly three 2s."),
    say("Only 2 is common to all three (3, 5, 7 each appear once), and its lowest power is \\(2^3\\)."),
    box("So the HCF is \\(2^3\\) = ",8,"2 × 2 × 2.",phase="substitute"),
    box("Check 8 divides all: 24 ÷ 8 = 3, 40 ÷ 8 = 5, 56 ÷ 8 = ",7,"56 shared into eights.",done="8 divides all three and nothing larger does, so HCF = 8.")]},
]

gold = [
 {"display":"The HCF of two numbers is 6 and their LCM is 180. One number is 36. What is the other?","solutions":[30],"calculator":False,
  "input_type":"single_value",
  "hint":"Use HCF × LCM = the product of the two numbers.",
  "misconceptions":[{"pattern":"divide_lcm","message":"Use HCF × LCM = the product of the numbers. 6 × 180 = 1080, so the other is 1080 ÷ 36 = 30, not 180 ÷ 36 = 5.","expect":5}],
  "guided_steps":[
    say("Use the rule HCF × LCM = the product of the two numbers."),
    box("Multiply HCF × LCM: 6 × 180 = ",1080,"6 × 180."),
    say("This equals the two numbers multiplied: 36 × other = 1080."),
    box("So the other number is 1080 ÷ 36 = ",30,"1080 shared into 36s.",phase="substitute"),
    box("Check the HCF of 36 and 30: both share 2 × 3 = ",6,"36 = \\(2^2\\times 3^2\\), 30 = 2×3×5, shared 2×3.",done="HCF(36, 30) = 6 and LCM = 180, so the other number is 30.")]},
 {"display":"Find the LCM of 24, 36 and 40","solutions":[360],"calculator":False,
  "input_type":"single_value",
  "hint":"Prime factorise all three, then take every prime at its highest power.",
  "misconceptions":[{"pattern":"pair_only","message":"Include all three numbers. LCM(24, 36) = 72 ignores the 40. Using \\(2^3\\times 3^2\\times 5\\) gives 360.","expect":72}],
  "guided_steps":[
    say("Prime factorise all three, then take every prime at its highest power."),
    box("24 = \\(2^3\\times 3\\), so the power of 2 in 24 is ",3,"24 = 2×2×2×3."),
    box("36 = \\(2^2\\times 3^2\\), so the power of 3 in 36 is ",2,"36 = 2×2×3×3."),
    say("40 = \\(2^3\\times 5\\) adds the prime 5. Highest powers overall: \\(2^3\\), \\(3^2\\), 5."),
    box("Multiply: \\(2^3\\times 3^2\\times 5\\) = 8 × 9 × 5 = ",360,"72 × 5.",phase="substitute"),
    box("Check all divide 360: 360 ÷ 24 = 15, 360 ÷ 36 = 10, 360 ÷ 40 = ",9,"360 shared into forties.",done="360 uses the highest powers, so LCM = 360.")]},
 {"display":"Write 2520 as a product of primes in index form. What is the index of 2?","solutions":[3],"calculator":False,
  "input_type":"single_value",
  "hint":"Divide 2520 by 2 repeatedly and count how many times you can.",
  "misconceptions":[{"pattern":"count_primes","message":"The index of 2 counts how many 2s multiply, not the number of different primes. 2520 = \\(2^3\\times 3^2\\times 5\\times 7\\), so the index of 2 is 3, not 4.","expect":4}],
  "guided_steps":[
    say("Divide 2520 by 2 repeatedly and count how many 2s come out."),
    box("2520 ÷ 2 = ",1260,"Halve 2520."),
    box("1260 ÷ 2 = ",630,"Halve 1260."),
    box("630 ÷ 2 = ",315,"Halve 630."),
    say("315 is odd, so no more 2s. We divided by 2 three times."),
    box("The index of 2 is the number of halvings: ",3,"Count the three halvings.",phase="substitute"),
    box("Check: \\(2^3 = 8\\) and 2520 ÷ 8 = 315, which is odd, so the power of 2 is exactly ",3,"2520 = \\(2^3\\times 315\\).",done="2520 = \\(2^3\\times 3^2\\times 5\\times 7\\), so the index of 2 is 3.")]},
 {"display":"The LCM of two numbers is 60. Their HCF is 4. One number is 20. What is the other?","solutions":[12],"calculator":False,
  "input_type":"single_value",
  "hint":"Use HCF × LCM = the product of the two numbers.",
  "misconceptions":[{"pattern":"divide_lcm","message":"Use HCF × LCM = the product of the numbers. 4 × 60 = 240, so the other is 240 ÷ 20 = 12, not 60 ÷ 20 = 3.","expect":3}],
  "guided_steps":[
    say("Use HCF × LCM = the product of the two numbers."),
    box("Multiply HCF × LCM: 4 × 60 = ",240,"4 × 60."),
    say("This equals the two numbers multiplied: 20 × other = 240."),
    box("So the other number is 240 ÷ 20 = ",12,"240 shared into 20s.",phase="substitute"),
    box("Check LCM of 20 and 12: 20 = \\(2^2\\times 5\\), 12 = \\(2^2\\times 3\\), LCM = \\(2^2\\times 3\\times 5\\) = ",60,"4 × 15.",done="HCF(20, 12) = 4 and LCM = 60, so the other number is 12.")]},
 {"display":"Three lights flash at intervals of 4, 6 and 10 seconds. They all flash together. After how many seconds do they next all flash together?","solutions":[60],"calculator":False,
  "input_type":"single_value",
  "hint":"Find the LCM of 4, 6 and 10; that is when they next coincide.",
  "misconceptions":[{"pattern":"multiply_all","message":"They coincide at the LCM, not the product. 4 = \\(2^2\\), 6 = 2×3, 10 = 2×5, so LCM = \\(2^2\\times 3\\times 5\\) = 60, not 240.","expect":240}],
  "guided_steps":[
    say("They coincide again at the LCM of 4, 6 and 10."),
    box("4 = \\(2^2\\), so the power of 2 in 4 is ",2,"4 = 2 × 2."),
    box("6 = 2 × 3 and 10 = 2 × 5. The two new primes these add are 3 and ",5,"10 = 2 × 5."),
    say("Highest powers overall: \\(2^2\\) (from 4), 3 (from 6), 5 (from 10)."),
    box("Multiply: \\(2^2\\times 3\\times 5\\) = ",60,"4 × 15.",phase="substitute"),
    box("Check all divide 60: 60 ÷ 4 = 15, 60 ÷ 6 = 10, 60 ÷ 10 = ",6,"60 shared into tens.",done="60 seconds is the first shared moment, so they next flash together at 60.")]},
]

# ============================ TIER GUIDES ============================
def ex(q, steps): return {"question": q, "steps": steps}
def st(label, content, ans=False):
    d={"label":label,"content":content}
    if ans: d["isAnswer"]=True; d["is_answer"]=True
    return d

tier_guides = {
 "bronze":{"title":"Bronze: factors, multiples and primes by hand","steps":[
   "<strong>Factors</strong> divide a number exactly; find them in pairs (1×12, 2×6, 3×4). <strong>Multiples</strong> are its times table.",
   "A <strong>prime</strong> has exactly two factors, 1 and itself. Test small numbers by dividing by 2, 3, 5 and 7.",
   "The <strong>HCF</strong> is the largest factor two numbers share; the <strong>LCM</strong> is the first multiple they share."],
   "example":ex("Find the HCF of 8 and 12",[
     st("List","<p>Factors of 8: 1, 2, 4, 8. Factors of 12: 1, 2, 3, 4, 6, 12.</p>"),
     st("Share","<p>Common factors: 1, 2, 4.</p>"),
     st("Check","<p>4 divides 8 and 12 exactly, and nothing bigger does.</p>"),
     st("Answer","<p>HCF = 4</p>",True)])},
 "silver":{"title":"Silver: prime factors for HCF and LCM","steps":[
   "Break each number into <strong>prime factors</strong> in index form, e.g. 48 = \\(2^4\\times 3\\).",
   "<strong>HCF</strong>: multiply the shared primes at their <strong>lowest</strong> powers.",
   "<strong>LCM</strong>: multiply all primes at their <strong>highest</strong> powers. A worded 'next time together' question is an LCM."],
   "example":ex("Find the LCM of 8 and 14",[
     st("Factorise","<p>8 = \\(2^3\\), 14 = 2 × 7.</p>"),
     st("Highest powers","<p>Take \\(2^3\\) and 7.</p>"),
     st("Check","<p>56 ÷ 8 = 7 and 56 ÷ 14 = 4.</p>"),
     st("Answer","<p>LCM = 56</p>",True)])},
 "gold":{"title":"Gold: multi-number and reverse problems","steps":[
   "For three numbers, list every prime that appears, then take each at its highest power (LCM) or lowest shared power (HCF).",
   "Given the HCF and LCM, use <strong>HCF × LCM = the product of the two numbers</strong> to find a missing one.",
   "For a big number, divide by each prime repeatedly and count the powers."],
   "example":ex("HCF of two numbers is 6, LCM is 180, one is 36. Find the other.",[
     st("Product","<p>6 × 180 = 1080.</p>"),
     st("Divide","<p>1080 ÷ 36 = 30.</p>"),
     st("Check","<p>HCF(36, 30) = 6 and LCM = 180.</p>"),
     st("Answer","<p>30</p>",True)])},
}

# ============================ GUIDED ============================
guided = {
 "opener":{
   "label":"Before any rules",
   "display": opener_svg + "<strong>12 cupcakes</strong> are shared into equal rows with none left over. Above they sit in 4 rows of 3.",
   "steps":[
     box("Look at the array: 12 cupcakes in equal rows of 3. How many rows are there? ",4,"12 shared into threes."),
     box("You could also line them up in rows of 4. How many rows then? ",3,"12 shared into fours."),
     box("Try rows of 5: does 12 split into equal rows of 5 with none left over? Enter 1 for yes, 0 for no: ",0,"12 ÷ 5 leaves 2 over, so no."),
     say("The numbers that divide 12 into equal rows with none left over, 1, 2, 3, 4, 6 and 12, are its <strong>factors</strong>. 5 is not a factor. A number like 7 has only two arrangements, 1 row of 7 or 7 rows of 1, so 7 is <strong>prime</strong>. Finding factors, multiples and primes is this whole lesson.")]},
 "teach":{
   "bronze":{"display":"Find the HCF of 6 and 8","label":"Together: your first one","steps":[
     box("Factors of 6 are 1, 2, 3 and ",6,"6 divides itself.",say="List the factors of each number."),
     box("Factors of 8 are 1, 2, 4 and ",8,"8 divides itself."),
     box("The shared factors are 1 and 2, so the highest is ",2,"The bigger of 1 and 2.",phase="substitute"),
     box("Check: 6 ÷ 2 = 3 and 8 ÷ 2 = ",4,"8 shared into twos.",done="2 divides both, so HCF = 2. That was the whole move.")]},
   "silver":{"display":"Find the LCM of 10 and 15","label":"Together: your first one","steps":[
     box("10 = 2 × 5, so the primes in 10 are 2 and ",5,"10 = 2 × 5.",say="Prime factorise each number."),
     box("15 = 3 × 5, adding the new prime ",3,"15 = 3 × 5."),
     box("Take every prime at its highest power: 2 × 3 × 5 = ",30,"6 × 5.",phase="substitute"),
     box("Check: 30 ÷ 10 = 3 and 30 ÷ 15 = ",2,"30 shared into fifteens.",done="30 is a multiple of both, so LCM = 30. That was the whole move.")]},
   "gold":{"display":"The HCF of two numbers is 8 and their LCM is 96. One number is 32. Find the other.","label":"Together: your first one","steps":[
     box("Multiply HCF × LCM: 8 × 96 = ",768,"8 × 96.",say="Use HCF × LCM = the product of the numbers."),
     box("This equals 32 × other, so other = 768 ÷ 32 = ",24,"768 shared into 32s.",phase="substitute"),
     box("Check the HCF of 32 and 24: 32 = \\(2^5\\), 24 = \\(2^3\\times 3\\), shared \\(2^3\\) = ",8,"2 × 2 × 2."),
     box("Check the LCM: \\(2^5\\times 3\\) = ",96,"32 × 3.",done="HCF 8 and LCM 96 both check out, so the other number is 24. That was the whole move.")]},
 }
}

# ============================ METHOD CARD (trim) ============================
method_card = {
 "title":"Factors, Multiples & Primes",
 "steps":[
   "Break each number into prime factors using a factor tree.",
   "Write it in index form, e.g. \\(2^3\\times 3\\times 5\\).",
   "HCF: multiply the shared primes at their lowest powers.",
   "LCM: multiply all primes at their highest powers."],
 "content":"<p><strong>Factors</strong> divide a number exactly; <strong>multiples</strong> are its times table. A <strong>prime</strong> has exactly two factors, 1 and itself, so 1 is not prime and 2 is the only even prime.</p><p>The <strong>HCF</strong> is the largest factor two numbers share; the <strong>LCM</strong> is the smallest multiple they share.</p><p>The efficient method is <strong>prime factor decomposition</strong>: break each number into primes in index form. For the HCF multiply the shared primes at their lowest powers; for the LCM multiply all primes at their highest powers.</p>",
 "example":"<p><strong>Find the HCF and LCM of 24 and 36</strong></p><p><strong>Step 1:</strong> \\(24 = 2^3 \\times 3\\) and \\(36 = 2^2 \\times 3^2\\)</p><p><strong>Step 2, HCF:</strong> shared primes, lowest powers: \\(2^2 \\times 3 = 12\\)</p><p><strong>Step 3, LCM:</strong> all primes, highest powers: \\(2^3 \\times 3^2 = 72\\)</p><p><strong>Answer:</strong> HCF = 12, LCM = 72</p>"
}

# ============================ ASSEMBLE (preserve originals) ============================
orig = json.load(io.open("_live_maths-ocr_number-L04.json", encoding="utf-8"))
pd = {
 "method_card": method_card,
 "topic_links": orig["topic_links"],
 "problem_bank": {
   "gold": gold, "bronze": bronze, "silver": silver,
   "bronze_description":"Find factors, multiples and simple HCFs and LCMs, and test small numbers for being prime.",
   "silver_description":"Use prime factorisation to find the HCF and LCM of larger numbers, including worded LCM problems.",
   "gold_description":"Solve multi-number LCMs, prime-factorise big numbers, and use HCF × LCM = product in reverse.",
 },
 "related_videos": orig["related_videos"],
 "worked_examples": json.loads(json.dumps(orig["worked_examples"], ensure_ascii=False).replace(" — ", ": ").replace("—", "-")),
 "tier_guides": tier_guides,
 "guided": guided,
}
json.dump(pd, io.open("lesson_maths-ocr_number-L04.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
for t in ("bronze","silver","gold"):
    print(t,"tier_guide words:", sum(words(s) for s in tier_guides[t]["steps"]))
print("method content words:", words(method_card["content"]))
print("opener svg len:", len(opener_svg))
print("WROTE lesson_maths-ocr_number-L04.json")
