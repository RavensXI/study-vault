import json, re
raw=open('_chk_8a0771_live.json',encoding='utf-8').read()
low=raw.lower()
boards=['aqa','edexcel','ocr','eduqas','wjec']
for b in boards:
    for m in re.finditer(b, low):
        print("BOARD NAME:", b, "...", raw[max(0,m.start()-40):m.start()+20].replace(chr(10),' '))
for phrase in ['equation sheet','on your sheet','you must memorise','formula sheet','given to you']:
    if phrase in low:
        i=low.find(phrase); print("PHRASE:", phrase, "...", raw[max(0,i-50):i+30])
print("board-neutrality scan done")
