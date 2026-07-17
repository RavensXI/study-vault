import json
pre = json.load(open("_pre_numL03_pd.json",encoding="utf-8"))
live = json.load(open("_live_ocr_numberL03.json",encoding="utf-8"))
out=[]
out.append("PRE worked_examples:\n"+json.dumps(pre.get("worked_examples"),indent=2,ensure_ascii=False))
out.append("\n\nLIVE worked_examples:\n"+json.dumps(live.get("worked_examples"),indent=2,ensure_ascii=False))
# method_card diff
out.append("\n\nPRE method_card:\n"+json.dumps(pre.get("method_card"),indent=2,ensure_ascii=False))
open("_we_compare.txt","w",encoding="utf-8").write("\n".join(out))
print("written")
