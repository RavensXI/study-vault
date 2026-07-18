import json,io
live=json.load(io.open('_live_canonical.json',encoding='utf-8'))
pre=json.load(io.open('_pre_canonical.json',encoding='utf-8'))
out=io.open('_displaydiff.txt','w',encoding='utf-8')
for t in ['bronze','silver','gold']:
    for i,(a,b) in enumerate(zip(live['problem_bank'][t],pre['problem_bank'][t])):
        if a.get('display')!=b.get('display'):
            out.write(f'DISPLAY CHANGED {t}[{i}]\n  pre : {b.get("display")}\n  live: {a.get("display")}\n')
        if a.get('solutions')!=b.get('solutions'):
            out.write(f'SOL CHANGED {t}[{i}] pre={b.get("solutions")} live={a.get("solutions")}\n')
# en/em dash chars in exam_context marks
import unicodedata
m=live['exam_context']['marks']
out.write('marks chars: '+ ' '.join(f'{c}=U+{ord(c):04X}' for c in m)+'\n')
out.close()
print('done')
