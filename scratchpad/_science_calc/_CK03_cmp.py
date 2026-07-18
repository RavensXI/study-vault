import json, hashlib

def load(fn):
    with open(fn, encoding="utf-8") as f:
        return json.load(f)

canon = load("_CK03_canonical.json")
p1 = load("_CK03_prop1.json")
p2 = load("_CK03_prop2.json")

def canon_bytes(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

hc = hashlib.sha256(canon_bytes(canon)).hexdigest()
h1 = hashlib.sha256(canon_bytes(p1)).hexdigest()
h2 = hashlib.sha256(canon_bytes(p2)).hexdigest()
print("canonical:", hc)
print("prop1    :", h1, "MATCH" if h1 == hc else "DIFFER")
print("prop2    :", h2, "MATCH" if h2 == hc else "DIFFER")
