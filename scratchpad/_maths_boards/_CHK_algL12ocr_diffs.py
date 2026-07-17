import json, io
ID="971cfba0-badb-4c6b-b0f8-e9d33d450b8c"
live=json.load(io.open("_CHK_algL12ocr_live.json","r",encoding="utf-8"))
dump=json.load(io.open("_pre_dump_maths-ocr.json","r",encoding="utf-8"))
pre=[v for v in dump if v.get("id")==ID][0]["practice_data"]

print("=== bronze[4] display ===")
print("PRE :", pre["problem_bank"]["bronze"][4]["display"])
print("LIVE:", live["problem_bank"]["bronze"][4]["display"])
print("PRE sol:", pre["problem_bank"]["bronze"][4]["solutions"], "LIVE sol:", live["problem_bank"]["bronze"][4]["solutions"])

print("\n=== gold[2] display ===")
print("PRE :", pre["problem_bank"]["gold"][2]["display"])
print("LIVE:", live["problem_bank"]["gold"][2]["display"])
print("PRE sol:", pre["problem_bank"]["gold"][2]["solutions"], "LIVE sol:", live["problem_bank"]["gold"][2]["solutions"])

print("\n=== worked_examples PRE ===")
print(json.dumps(pre["worked_examples"], ensure_ascii=False, indent=1))
print("\n=== method_card PRE ===")
print(json.dumps(pre["method_card"], ensure_ascii=False, indent=1))
