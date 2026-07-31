# -*- coding: utf-8 -*-
"""Full StudyVault backup to OneDrive (survives local deletion via cloud sync
+ OneDrive's 30-day recycle bin; independent of any one credential).

Captures: every core Supabase table as gzipped JSON (REST, paginated),
the auth user list, a git bundle of ALL branches (including unpushed work),
the private Business folder, and the assistant memory directory.

    python scripts/_backup_studyvault.py
Destination: OneDrive/Documents/StudyVault Backups/YYYY-MM-DD/
"""
import datetime
import gzip
import io
import json
import os
import shutil
import subprocess
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SB_URL = os.environ["SUPABASE_URL"]
SB_KEY = os.environ["SUPABASE_SERVICE_KEY"]
STAMP = datetime.date.today().isoformat()
DEST = os.path.join(r"C:\Users\tshau\OneDrive\Documents", "StudyVault Backups", STAMP)
REPO = r"C:\Users\tshau\Documents\Study Vault"
BUSINESS = r"C:\Users\tshau\Documents\StudyVault Business"
MEMORY = r"C:\Users\tshau\.claude\projects\C--Users-tshau-Documents-Study-Vault\memory"

TABLES = ["schools", "subjects", "units", "lessons", "guide_pages",
          "school_subscriptions", "classes", "class_members", "teacher_subjects",
          "teacher_invitations", "profiles", "progress", "events",
          "upload_jobs", "content_pipeline_logs", "notifications"]


def sq(path):
    r = urllib.request.Request(SB_URL + path, headers={"apikey": SB_KEY,
                                                       "Authorization": "Bearer " + SB_KEY})
    return json.load(urllib.request.urlopen(r, timeout=120))


def dump_table(name, outdir):
    rows, off = [], 0
    while True:
        page = sq(f"/rest/v1/{name}?select=*&order=id&limit=1000&offset={off}")
        rows += page
        if len(page) < 1000:
            break
        off += 1000
    with gzip.open(os.path.join(outdir, f"{name}.json.gz"), "wt", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False)
    print(f"  {name}: {len(rows)} rows")
    return len(rows)


def main():
    os.makedirs(os.path.join(DEST, "supabase"), exist_ok=True)
    total = 0
    for t in TABLES:
        try:
            total += dump_table(t, os.path.join(DEST, "supabase"))
        except Exception as e:
            print(f"  {t}: FAILED {str(e)[:90]}")

    # auth users (ids/emails/metadata keys — hashes are not exportable, by design)
    try:
        users, page = [], 1
        while True:
            r = urllib.request.Request(
                SB_URL + f"/auth/v1/admin/users?page={page}&per_page=200",
                headers={"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY})
            batch = json.load(urllib.request.urlopen(r, timeout=60)).get("users", [])
            users += [{"id": u["id"], "email": u.get("email"),
                       "created_at": u.get("created_at"),
                       "meta_keys": sorted((u.get("user_metadata") or {}).keys())}
                      for u in batch]
            if len(batch) < 200:
                break
            page += 1
        with gzip.open(os.path.join(DEST, "auth_users.json.gz"), "wt", encoding="utf-8") as f:
            json.dump(users, f)
        print(f"  auth users: {len(users)}")
    except Exception as e:
        print("  auth users FAILED:", str(e)[:90])

    # git bundle: every branch, including local-only commits
    try:
        subprocess.run(["git", "bundle", "create",
                        os.path.join(DEST, "study-vault-all-branches.bundle"), "--all"],
                       cwd=REPO, check=True, capture_output=True, timeout=600)
        print("  git bundle: ok")
    except Exception as e:
        print("  git bundle FAILED:", str(e)[:90])

    for src, name in ((BUSINESS, "business"), (MEMORY, "memory")):
        try:
            shutil.copytree(src, os.path.join(DEST, name), dirs_exist_ok=True)
            print(f"  {name}: copied")
        except Exception as e:
            print(f"  {name} FAILED: {str(e)[:90]}")

    print(f"BACKUP COMPLETE -> {DEST} ({total} DB rows)")


if __name__ == "__main__":
    main()
