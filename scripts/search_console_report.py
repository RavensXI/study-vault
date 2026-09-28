"""Google Search Console pull (Tom, 28 Sep 2026: "you can just be checking it every now and again").

Read-only service account (added in Search Console as a Restricted user). The key file stays
outside the repo; its path is in the GSC_KEY_FILE environment variable.

  python scripts/search_console_report.py sites      list the properties the account can see
  python scripts/search_console_report.py [DAYS]     pull the last DAYS (default 28) and print a summary
  python scripts/search_console_report.py weekly     this week vs last week, emailed via Resend (Sunday audit)

Each pull is saved to scripts/_gsc/<date>.json so trends survive after Google's 16-month window.
"""
import datetime as dt, json, os, sys
from collections import defaultdict
from google.oauth2 import service_account
from googleapiclient.discovery import build

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_gsc")


def service():
    creds = service_account.Credentials.from_service_account_file(
        os.environ.get("GSC_KEY_FILE", os.path.expanduser(r"~\.secrets\gsc-reader.json")), scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def site(svc):
    if os.environ.get("GSC_SITE"): return os.environ["GSC_SITE"]
    s = [x["siteUrl"] for x in svc.sites().list().execute().get("siteEntry", [])]
    if not s: sys.exit("The service account sees no properties. Add it as a user in Search Console.")
    return next((x for x in s if x.startswith("sc-domain:")), s[0])


def query(svc, url, start, end, dims):
    rows, first = [], 0
    while True:
        r = svc.searchanalytics().query(siteUrl=url, body={
            "startDate": start, "endDate": end, "dimensions": dims, "rowLimit": 25000, "startRow": first}).execute()
        got = r.get("rows", [])
        rows += [dict(zip(dims, x["keys"]), clicks=x["clicks"], impressions=x["impressions"], position=round(x["position"], 1)) for x in got]
        if len(got) < 25000: return rows
        first += 25000


def weekly(svc):
    """This week against last week, emailed through Resend (run from the Sunday audit wrapper)."""
    import urllib.request
    url = site(svc)
    end = dt.date.today() - dt.timedelta(days=2)
    wk = lambda a, b: (a.isoformat(), b.isoformat())
    this, last = wk(end - dt.timedelta(days=6), end), wk(end - dt.timedelta(days=13), end - dt.timedelta(days=7))
    tot = lambda rs: (sum(r["clicks"] for r in rs), sum(r["impressions"] for r in rs),
                      round(sum(r["position"] * r["impressions"] for r in rs) / max(1, sum(r["impressions"] for r in rs)), 1))
    p_now, p_then = query(svc, url, *this, ["page"]), query(svc, url, *last, ["page"])
    qp = query(svc, url, *this, ["query", "page"])
    (c1, i1, pos1), (c0, i0, pos0) = tot(p_now), tot(p_then)
    before = {r["page"] for r in p_then if r["clicks"]}
    short = lambda p: p.split(".co.uk", 1)[-1] or "/"
    L = ["Google search, %s to %s (last week in brackets)" % this, "",
         "Clicks from Google: %d (%d)" % (c1, c0), "Times shown in results: %d (%d)" % (i1, i0),
         "Average position: %s (%s)" % (pos1, pos0), "Pages shown at least once: %d (%d)" % (len(p_now), len(p_then)), "",
         "Pages with clicks this week (new ones marked NEW):"]
    for r in sorted(p_now, key=lambda r: -r["clicks"])[:15]:
        if r["clicks"]: L.append("  %d  %s%s" % (r["clicks"], short(r["page"]), "  NEW" if r["page"] not in before else ""))
    L += ["", "Searches where a page is on page 1-2 of Google but gets few clicks (worth improving):"]
    for r in sorted([r for r in qp if r["position"] <= 20 and r["impressions"] >= 10], key=lambda r: -r["impressions"])[:10]:
        L.append("  shown %d, clicked %d, position %.0f: \"%s\"  %s" % (r["impressions"], r["clicks"], r["position"], r["query"][:70], short(r["page"])))
    text = "\n".join(L)
    print(text)
    if os.environ.get("RESEND_API_KEY") and os.environ.get("NOTIFY_TO") and os.environ.get("NOTIFY_FROM"):
        body = json.dumps({"from": os.environ["NOTIFY_FROM"], "to": [os.environ["NOTIFY_TO"]],
                           "subject": "StudyVault: Google search this week - %d clicks (%d last week)" % (c1, c0), "text": text}).encode()
        urllib.request.urlopen(urllib.request.Request("https://api.resend.com/emails", data=body, method="POST", headers={
            "Authorization": "Bearer " + os.environ["RESEND_API_KEY"], "Content-Type": "application/json"}), timeout=30)


def main():
    sys.stdout.reconfigure(encoding="utf-8")   # queries carry symbols the Windows console codepage lacks
    svc = service()
    if sys.argv[1:] == ["weekly"]:
        return weekly(svc)
    if sys.argv[1:] == ["sites"]:
        for x in svc.sites().list().execute().get("siteEntry", []): print(x["siteUrl"], x["permissionLevel"])
        return
    days = int(sys.argv[1]) if sys.argv[1:] else 28
    url = site(svc)
    end = dt.date.today() - dt.timedelta(days=2)          # the last two days are still filling in
    start = end - dt.timedelta(days=days - 1)
    s, e = start.isoformat(), end.isoformat()
    data = {"site": url, "start": s, "end": e,
            "by_date": query(svc, url, s, e, ["date"]),
            "by_page": query(svc, url, s, e, ["page"]),
            "by_query_page": query(svc, url, s, e, ["query", "page"]),
            "by_country": query(svc, url, s, e, ["country"]),
            "by_device": query(svc, url, s, e, ["device"])}
    os.makedirs(OUT, exist_ok=True)
    json.dump(data, open(os.path.join(OUT, dt.date.today().isoformat() + ".json"), "w", encoding="utf-8"), indent=1)

    print("%s  %s to %s" % (url, s, e))
    print("\nDay         clicks  impressions")
    for r in data["by_date"]: print("%s  %6d  %11d" % (r["date"], r["clicks"], r["impressions"]))
    print("\nPages with clicks:")
    for r in sorted(data["by_page"], key=lambda r: -r["clicks"])[:25]:
        if r["clicks"]: print("  %4d clicks  %5d impr  pos %5.1f  %s" % (r["clicks"], r["impressions"], r["position"], r["page"]))
    print("\nNearly ranking (position 8-20, 5+ impressions) - the pages worth improving:")
    near = [r for r in data["by_query_page"] if 8 <= r["position"] <= 20 and r["impressions"] >= 5]
    for r in sorted(near, key=lambda r: -r["impressions"])[:25]:
        print("  %5d impr  pos %5.1f  %-45s %s" % (r["impressions"], r["position"], r["query"][:45], r["page"]))
    subj = defaultdict(lambda: [0, 0])
    for r in data["by_page"]:
        p = r["page"].split("/")
        k = p[4] if len(p) > 4 and p[3] in ("lesson", "practice", "browse", "guide") else "/".join(p[3:4]) or "home"
        subj[k][0] += r["clicks"]; subj[k][1] += r["impressions"]
    print("\nBy subject:")
    for k, (c, i) in sorted(subj.items(), key=lambda kv: -kv[1][1])[:25]: print("  %4d clicks  %6d impr  %s" % (c, i, k))


if __name__ == "__main__":
    main()
