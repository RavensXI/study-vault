import json
live=json.load(open('_chk_L04_de190166.json',encoding='utf-8'))

# Verify each guided box independently by re-deriving from the pre/say text semantics manually encoded:
# Instead, spot-check every box value against my hand-solve table.
expected={
 'teach.bronze':[15,8,23,23],
 'teach.silver':[25,50,47,47],
 'teach.gold':[12,4,2,20],
 'opener':[11,15],
}
for k,exp in expected.items():
    if k=='opener': steps=live['guided']['opener']['steps']
    else:
        t=k.split('.')[1]; steps=live['guided']['teach'][t]['steps']
    got=[s['answer'] for s in steps if 'answer' in s]
    print(k,'boxes',got,'EXPECT',exp,'OK' if got==exp else 'MISMATCH')

# bronze/silver full box sequences vs my hand table
bronze_boxes=[[6,11,11],[24,23,23],[12,10,22],[-10,-13,-13],[20,17,17],[5,8,8],[18,14,14],[15,-5,-5]]
silver_boxes=[[16,21,21],[36,30,6],[9,18,19],[12,17,17],[4,12,4,12],[9,10,2],[16,-8,0]]
for t,table in [('bronze',bronze_boxes),('silver',silver_boxes)]:
    for j,p in enumerate(live['problem_bank'][t]):
        got=[s['answer'] for s in p['guided_steps'] if 'answer' in s]
        print(f'{t}[{j}] boxes',got,'EXPECT',table[j],'OK' if got==table[j] else 'MISMATCH')

# Gold MC: verify solution index and expects
gold_correct=[0,0,0,1,0]
for j,p in enumerate(live['problem_bank']['gold']):
    print(f'gold[{j}] sol={p["solutions"]} expect_correct={gold_correct[j]} OK={p["solutions"]==[gold_correct[j]]} it={p["input_type"]}')
    for m in p['misconceptions']:
        print('    expect',m['expect'],'note',m['note'])
