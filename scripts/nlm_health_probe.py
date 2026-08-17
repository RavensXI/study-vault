# -*- coding: utf-8 -*-
"""NLM pipeline health probe (task #61, Tom's ask 16 Aug).

The 13-16 Aug outage: expired cookies made every `nlm video create`
silently no-op ("Could not retrieve..." with exit 0), so four daily
windows launched notebooks with NOTHING cooking and nobody knew. This
probe answers the one question that catches that on day one: "did the
most recent launch actually start generating?"

Checks, in order:
1. AUTH — `nlm notebook list` must succeed (the wrapper's re-auth
   normally handles expiry; if even that fails, alert).
2. COOKING — take the newest in_progress jobs launched 45min-26h ago,
   live-check up to 3 of their notebook studios; healthy = at least one
   shows a video artifact (any status — NLM's 'unknown' still means
   cooking). If launches exist but NO sampled studio has an artifact,
   the pipeline is silently dead — alert.
3. STALE — any in_progress job older than 48h is flagged in the alert
   body (informational).

Alerts via the house Resend pattern (RESEND_API_KEY / NOTIFY_TO /
NOTIFY_FROM), at most one per day (flag file). Exit 0 healthy or
nothing-to-check, exit 1 unhealthy.

Run: python scripts/nlm_health_probe.py [--stream explainer|podcast]
     [--force-alert] [--test-alert]
Wired into daily_explainer_build.ps1's and daily_podcast_build.ps1's
hourly heartbeats. --stream picks which pipeline's state to probe:
explainer (video artifacts, the default) or podcast (audio artifacts).
"""
import io
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
STREAM = "explainer"
if "--stream" in sys.argv:
    STREAM = sys.argv[sys.argv.index("--stream") + 1]
    assert STREAM in ("explainer", "podcast"), "unknown stream: " + STREAM
if STREAM == "podcast":
    STATE = os.path.join(HERE, "_batch_podcast_state.json")
    LOGDIR = os.path.join(HERE, "_podcast_daily_logs")
    ARTIFACT_TYPE = "audio"
else:
    STATE = os.path.join(HERE, "_batch_explainer_state.json")
    LOGDIR = os.path.join(HERE, "_explainer_daily_logs")
    ARTIFACT_TYPE = "video"
FLAG = os.path.join(LOGDIR, "_health_alerted_%s_%s.flag"
                    % (STREAM, time.strftime("%Y-%m-%d")))


def log(msg):
    line = "%s [health:%s] %s" % (time.strftime("%H:%M:%S"), STREAM, msg)
    print(line)
    try:
        io.open(os.path.join(LOGDIR, "health.log"), "a",
                encoding="utf-8").write(line + "\n")
    except OSError:
        pass


def notify(subject, body):
    key = os.environ.get("RESEND_API_KEY")
    to = os.environ.get("NOTIFY_TO")
    frm = os.environ.get("NOTIFY_FROM")
    if not (key and to and frm):
        log("Resend env missing - alert NOT sent")
        return False
    import urllib.request
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps({"from": frm, "to": [to], "subject": subject,
                         "text": body}).encode(),
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json",
                 # Cloudflare 1010-blocks the default Python UA
                 "User-Agent": "StudyVault-HealthProbe/1.0"})
    try:
        urllib.request.urlopen(req, timeout=20)
        log("alert sent: " + subject)
        return True
    except Exception as e:
        log("alert send failed: %s" % e)
        return False


def nlm(args, timeout=90):
    r = subprocess.run(["nlm"] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return (r.stdout or "") + (r.stderr or "")


def main():
    force = "--force-alert" in sys.argv
    if "--test-alert" in sys.argv:
        ok = notify("[StudyVault] NLM health probe - TEST",
                    "This is a wiring test of the NLM pipeline health "
                    "probe. If you can read this, alerts reach you.")
        sys.exit(0 if ok else 1)
    if os.path.exists(FLAG) and not force:
        log("already alerted today - skipping")
        sys.exit(0)

    problems = []

    # 1. auth
    out = nlm(["notebook", "list"])
    if "Authentication" in out and "Error" in out:
        problems.append("AUTH: nlm cookies expired and re-auth has not "
                        "recovered them. Run 'nlm login'.")
        log("auth check FAILED")
    else:
        log("auth check ok")

    # 2. cooking
    try:
        state = json.load(io.open(STATE, encoding="utf-8"))
    except OSError:
        log("no state file - nothing to check")
        sys.exit(0)
    now = time.time()
    recent = sorted(
        [j for j in state.get("jobs", [])
         if j.get("status") == "in_progress" and j.get("launched_ts")
         # a job that burned all 3 re-fires is a known-dead straggler
         # (the batch flips it to failed on its next pass) - one zombie
         # must not read as "the whole pipeline is down"
         and j.get("refires", 0) < 3
         and 0.75 * 3600 < now - j["launched_ts"] < 26 * 3600],
        key=lambda j: -j["launched_ts"])
    if recent and not problems:
        cooking = 0
        checked = 0
        for j in recent[:3]:
            out = nlm(["studio", "status", j["notebook_id"]])
            checked += 1
            try:
                idx = out.find("[")
                arts = json.loads(out[idx:out.rfind("]") + 1]) \
                    if idx >= 0 else []
            except ValueError:
                arts = []
            if any(a.get("type") == ARTIFACT_TYPE for a in arts):
                cooking += 1
        log("cooking check: %d/%d sampled notebooks have a %s artifact"
            % (cooking, checked, ARTIFACT_TYPE))
        if checked and cooking == 0:
            problems.append(
                "COOKING: %d %s job(s) were launched in the last 26h but "
                "none of %d sampled notebook studios contains ANY %s "
                "artifact. Launches are almost certainly no-opping "
                "(the 13-16 Aug failure mode). Newest job: %s"
                % (len(recent), STREAM, checked, ARTIFACT_TYPE,
                   recent[0].get("label", "?")))
    elif not recent:
        log("no recent launches to check")

    # 3. stale (informational)
    stale = [j for j in state.get("jobs", [])
             if j.get("status") == "in_progress" and j.get("launched_ts")
             and now - j["launched_ts"] > 48 * 3600]
    if stale:
        log("%d job(s) in_progress for >48h" % len(stale))

    if problems or force:
        body = ("NLM %s pipeline health probe failed on %s.\n\n%s\n\n"
                "%d job(s) stuck in_progress over 48h.\n\n"
                "State: %s\nLog:   %s"
                % (STREAM, time.strftime("%Y-%m-%d %H:%M"),
                   "\n\n".join(problems) if problems else
                   "(forced alert - no problems detected)", len(stale),
                   STATE, os.path.join(LOGDIR, "health.log")))
        if notify("[StudyVault] NLM %s pipeline UNHEALTHY - not "
                  "generating" % STREAM, body):
            io.open(FLAG, "w").write("1")
        sys.exit(1)
    log("HEALTHY")
    sys.exit(0)


if __name__ == "__main__":
    main()
