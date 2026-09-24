"""
Dry run of supabase/migrations/20260924210000_school_content_private.sql (24 Sep 2026).

Applies the migration inside a transaction, reads the content tables as each kind of user, prints
what each can see, then ROLLS BACK: nothing is changed. With --rollback-check it also applies the
rollback file inside the same transaction and checks the policies match the saved backup.

Usage:  python scripts/security/test_content_rls.py [--after]     (--after: no migration, test live)
        python scripts/security/test_content_rls.py --rollback-check
"""
import json
import os
import re
import sys

import psycopg2

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MIG = os.path.join(ROOT, "supabase", "migrations", "20260924210000_school_content_private.sql")
RB = MIG.replace(".sql", ".rollback.sql")


def body(path):
    sql = open(path, encoding="utf-8").read()
    return re.sub(r"^\s*(BEGIN|COMMIT);\s*$", "", sql, flags=re.M)


c = psycopg2.connect(host="aws-1-eu-west-2.pooler.supabase.com", port=5432,
                     user="postgres.baipckgywpnwapobwtsy", password=os.environ["SUPABASE_DB_URL"], dbname="postgres")
c.autocommit = False
cur = c.cursor()


def one(q, a=()):
    cur.execute(q, a)
    return cur.fetchone()


UNITY = one("select id from schools where slug='unity-college'")[0]
SEVERN = one("select id from schools where slug='severn-vale'")[0]
# people to act as
pupil_profile = one("select id from profiles where role='student' and school_id=%s and not coalesce(is_demo,false) limit 1", (UNITY,))[0]
pupil_member = one("""select p.id from class_members cm join classes c on c.id=cm.class_id join profiles p on p.id=cm.student_id
                      where c.school_id=%s and p.school_id is null limit 1""", (UNITY,))[0]
free_pupil = one("select id from profiles where role='student' and school_id is null limit 1")
teacher_unity = one("select id from profiles where role='teacher' and school_id=%s limit 1", (UNITY,))[0]
teacher_severn = one("select id from profiles where role='teacher' and school_id=%s limit 1", (SEVERN,))[0]
admin = one("select id from profiles where role='platform_admin' limit 1")[0]

if "--after" not in sys.argv:
    cur.execute(body(MIG))

CHECKS = [
    ("school subjects", "select count(*) from subjects where school_id is not null"),
    ("Unity subjects", f"select count(*) from subjects where school_id='{UNITY}'"),
    ("Severn Vale subjects", f"select count(*) from subjects where school_id='{SEVERN}'"),
    ("free live subjects", "select count(*) from subjects where school_id is null and status='live'"),
    ("school units", "select count(*) from units u join subjects s on s.id=u.subject_id where s.school_id is not null"),
    ("school lessons", "select count(*) from lessons l join units u on u.id=l.unit_id join subjects s on s.id=u.subject_id where s.school_id is not null"),
    ("Unity lessons", f"select count(*) from lessons l join units u on u.id=l.unit_id join subjects s on s.id=u.subject_id where s.school_id='{UNITY}'"),
    ("Severn lessons", f"select count(*) from lessons l join units u on u.id=l.unit_id join subjects s on s.id=u.subject_id where s.school_id='{SEVERN}'"),
    ("free live lessons", "select count(*) from lessons l join units u on u.id=l.unit_id join subjects s on s.id=u.subject_id where s.school_id is null and l.status='live'"),
    ("unpublished lessons", "select count(*) from lessons where status<>'live'"),
    ("school guide pages", "select count(*) from guide_pages g join subjects s on s.id=g.subject_id where s.school_id is not null"),
    ("lesson overrides", "select count(*) from lesson_overrides"),
]
WHO = [("anonymous", None), ("free-tier pupil", free_pupil[0] if free_pupil else None),
       ("Unity pupil (profile)", pupil_profile), ("Unity pupil (class only)", pupil_member),
       ("Unity teacher", teacher_unity), ("Severn Vale teacher", teacher_severn), ("platform admin", admin)]

res = {}
for label, uid in WHO:
    cur.execute("savepoint s")
    if uid is None:
        cur.execute("set local role anon")
        cur.execute("select set_config('request.jwt.claims', '{\"role\":\"anon\"}', true)")
    else:
        cur.execute("set local role authenticated")
        cur.execute("select set_config('request.jwt.claims', %s, true)", (json.dumps({"sub": str(uid), "role": "authenticated"}),))
    res[label] = [one(q)[0] for _, q in CHECKS]
    cur.execute("rollback to savepoint s")

w = max(len(n) for n, _ in CHECKS)
print("".ljust(w), *[l[:13].rjust(14) for l, _ in WHO])
for i, (n, _) in enumerate(CHECKS):
    print(n.ljust(w), *[str(res[l][i]).rjust(14) for l, _ in WHO])

if "--after" not in sys.argv:
    cur.execute("select count(*) from public.get_invitation_subjects('not-a-token')")
    print("\nsign-up subjects for a bad token:", cur.fetchone()[0], "(free-tier live subjects only)")

if "--rollback-check" in sys.argv:
    cur.execute(body(RB))
    cur.execute("""select tablename,policyname,permissive,roles::text,cmd,qual,with_check from pg_policies
                   where schemaname='public' and tablename in ('subjects','units','lessons','guide_pages','lesson_overrides') order by 1,2""")
    now = [dict(zip(['table', 'name', 'permissive', 'roles', 'cmd', 'qual', 'with_check'], r)) for r in cur.fetchall()]
    saved = json.load(open(os.path.join(ROOT, "scripts", "_backup_content_rls_2026-09-24.json"), encoding="utf-8"))
    print("rollback restores the saved policies exactly:", now == saved)

c.rollback()
print("\nrolled back: nothing changed")
