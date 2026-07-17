import json,sys,io
from fractions import Fraction as F
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_ADV_ps01_live.json",encoding="utf-8"))["practice_data"]
pb=live["problem_bank"]

# manual committed-error recompute per misconception, keyed by (tier,i,pattern)
# I compute what wrong answer the described error actually yields, compare to stored expect.
def red(n,d):
    f=F(n,d); return [f.numerator,f.denominator]

results=[]
# bronze
results.append(("bronze[0] fav_over_unfav",[3,5],[3,5]))          # 3 red vs 5 blue
results.append(("bronze[1] did_not_simplify",[3,6],[3,6]))        # 3/6 unsimplified
results.append(("bronze[2] forgot_complement",[3,10],[3,10]))     # gave P(win)=0.3=3/10
results.append(("bronze[3] fav_over_unfav",[6,9],[6,9]))          # 6 mint vs 9 toffee
results.append(("bronze[3] did_not_simplify",[6,15],[6,15]))
results.append(("bronze[4] fav_over_unfav",[3,9],[3,9]))          # 3 green vs 4+5=9 others
results.append(("bronze[4] did_not_simplify",[3,12],[3,12]))
results.append(("bronze[5] divide_not_multiply",[250],[250]))     # 50/0.2
results.append(("bronze[6] wrong_count",[1,11],[1,11]))           # counted 1 B
results.append(("bronze[7] counted_one_prime",[6,12],[6,12]))     # included 1
# silver
results.append(("silver[0] one_flip_only",[1,2],[1,2]))
# silver[1]: with-repl correct=4/25; error 'used 4/10*3/9'=without repl
wr=F(4,10)*F(3,9)
results.append(("silver[1] without_replacement", red(wr.numerator,wr.denominator), [1,15]))
results.append(("silver[2] with_replacement",[25,64],[25,64]))    # 5/8*5/8
results.append(("silver[3] added_not_multiplied",[9,10],[9,10]))  # 0.9
results.append(("silver[4] multiplied_not_added",[3,25],[3,25]))  # 4/10*3/10=12/100
results.append(("silver[5] forgot_to_cube",[2,3],[2,3]))
results.append(("silver[6] one_order_only",[16,90],[16,90]))
# gold
results.append(("gold[0] one_order_only",[24,90],[24,90]))
results.append(("gold[1] with_replacement",[343,1000],[343,1000]))
results.append(("gold[2] counted_none_case",[1,16],[1,16]))
results.append(("gold[3] one_path_only",[3,10],[3,10]))           # 0.3
results.append(("gold[4] one_order_only",[2,9],[2,9]))

for name,computed,stored in results:
    ok = computed==stored
    print(("OK  " if ok else "FAIL"), name, "computed",computed,"stored",stored)
