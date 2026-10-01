# Account and school-mode journeys (1 Oct 2026)

Real-browser journeys against the live site with disposable test pupils (created with the service key,
signed in by injecting a session token, deleted in a finally block). Run after any change to
account-sync.js, sync.js, school-session.js, dash-data.js or welcome.html.

    python scripts/tests/journeys/run_journeys.py     # six journeys, PASS/FAIL per step
    python scripts/tests/journeys/repro_signout.py    # sign out and back in keeps every subject and board

Rules: light single-row writes only, never DDL; stop if production slows; confirm cleanup at the end.
