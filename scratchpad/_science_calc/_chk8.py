import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
ch=json.load(open('changes_higher-calculations-L02@689e4ebed1.json',encoding='utf-8'))
print(json.dumps(ch,ensure_ascii=False,indent=1)[:2500])
wl=json.load(open('_worklist_versions.json',encoding='utf-8'))
e=wl['higher-calculations-L02@689e4ebed1']
print("\nall_row_ids:",e['all_row_ids'])
