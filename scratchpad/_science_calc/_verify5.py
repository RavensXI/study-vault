import json,re
raw=open('_live_canonical.json',encoding='utf-8').read()
low=raw.lower()
# board names
for b in ['aqa','edexcel','ocr','eduqas','wjec']:
    for m in re.finditer(b,low):
        print("BOARD:",b,raw[max(0,m.start()-40):m.start()+40].replace('\n',' '))
# equation-sheet claims
for phrase in ['equation sheet','on your sheet','you must memorise','memorise this','given to you','formula sheet','data sheet']:
    if phrase in low:
        i=low.find(phrase); print("SHEETCLAIM:",phrase,'|',raw[max(0,i-50):i+50])
# em dashes in student-facing (rough: check for em dash char)
print("EM DASH count:", raw.count('—'))
# find em dashes context (excluding internal note fields is hard; just list)
for m in re.finditer('—',raw):
    print("  emdash ctx:",raw[m.start()-40:m.start()+40].replace('\n',' '))
