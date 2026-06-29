import json, os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
state = json.load(open(os.path.join(ROOT, "scratch_rollout_state.json"), encoding="utf-8"))
removed = 0
for key, v in state.items():
    if v == "nohero":
        skey, slug = key.split("/")
        for f in glob.glob(os.path.join(ROOT, "design-lab", "assets", f"path-bg-u-{skey}-{slug}-land*.png")):
            os.remove(f); removed += 1
print(f"cleanup: removed {removed} stale backdrop files for no-hero units")
