import json, re
pd = json.load(open('_live_canonical.json'))
s = json.dumps(pd, ensure_ascii=False)
# board names
for b in ['AQA','Edexcel','OCR','Eduqas','WJEC']:
    if re.search(r'\b'+b+r'\b', s):
        print("BOARD NAME:", b)
# equation-sheet claims
for phrase in ['equation sheet','on your sheet','must memorise','memorise this','you must remember','given to you on','on the sheet','formula sheet']:
    if phrase.lower() in s.lower():
        print("SHEET CLAIM:", phrase)
# em dashes
if '—' in s: print("EM DASH FOUND")
# count em dashes with context
for m in re.finditer('.{20}—.{20}', s):
    print("emdash ctx:", m.group(0))
print("neutral phrasing occurrences of 'Check whether your board':", s.count('Check whether your board'))
print("done")
