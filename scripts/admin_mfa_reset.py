"""Lock-out recovery for admin two-factor sign-in (Tom, 29 Sep 2026).

If the phone with Microsoft Authenticator is lost and its cloud backup cannot restore the
StudyVault entry, this removes the admin account's two-factor factors with the service key.
The next sign-in at /teacher/login then asks to set up a new phone (a new QR code).

    python scripts/admin_mfa_reset.py              list the admin's factors (changes nothing)
    python scripts/admin_mfa_reset.py --delete     delete them

The admin is the profile with role platform_admin (there is one). Uses SUPABASE_URL and
SUPABASE_SERVICE_KEY. If the Auth admin API is unreachable, the same can be done in SQL through
the pooler (host aws-1-eu-west-2.pooler.supabase.com, port 5432, user
postgres.baipckgywpnwapobwtsy, password in SUPABASE_DB_URL):
    delete from auth.mfa_factors where user_id = '<admin id>';
Documented in Documents/StudyVault Business/BACKUP_RUNBOOK.md.
"""
import json, os, sys, urllib.request

U, K = os.environ["SUPABASE_URL"].rstrip("/"), os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}


def call(path, method="GET"):
    r = urllib.request.urlopen(urllib.request.Request(U + path, headers=H, method=method), timeout=30)
    body = r.read()
    return json.loads(body) if body else None


def main():
    admins = call("/rest/v1/profiles?select=id,full_name&role=eq.platform_admin")
    if len(admins) != 1:
        sys.exit("Expected exactly one platform_admin, found %d." % len(admins))
    uid, name = admins[0]["id"], admins[0]["full_name"]
    user = call("/auth/v1/admin/users/" + uid)
    factors = user.get("factors") or []
    print("%s (%s): %d factor(s)" % (name, user.get("email"), len(factors)))
    for f in factors:
        print("  %s  %s  %s  created %s" % (f["id"], f.get("factor_type"), f.get("status"), f.get("created_at", "")[:10]))
    if "--delete" not in sys.argv[1:]:
        print("Nothing changed. Run with --delete to remove them.")
        return
    for f in factors:
        call("/auth/v1/admin/users/%s/factors/%s" % (uid, f["id"]), method="DELETE")
        print("  deleted", f["id"])
    left = call("/auth/v1/admin/users/" + uid).get("factors") or []
    print("Factors left: %d. Sign in at https://www.studyvault.co.uk/teacher/login to set up the new phone." % len(left))


if __name__ == "__main__":
    main()
