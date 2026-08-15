# -*- coding: utf-8 -*-
"""Shared plumbing for the e2e ring: repo HTTP server, assert helper,
teacher session, standard mock shapes."""
import functools
import http.server
import json
import os
import threading

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FIXTURES = os.path.join(ROOT, "scripts", "tests", "fixtures")

_state = {"fails": 0}


def t(name, cond, detail=""):
    if not cond:
        _state["fails"] += 1
    print(("PASS " if cond else "FAIL ") + name + (" — " + str(detail) if detail != "" else ""))


def fails():
    return _state["fails"]


def serve_repo(port):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    handler.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def fixture(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return json.load(f)


def teacher_session(pg):
    pg.add_init_script(
        "sessionStorage.setItem('studyvault-auth', JSON.stringify("
        "{role:'teacher',teacher_id:'t1',school_id:null,full_name:'Test Teacher',pw:'x'}));")


def mock_json(pg, pattern, payload):
    pg.route(pattern, lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(payload)))


MY_CLASSES = {
    "classes": [
        {"id": "a54a74db-7622-4ce2-a77a-e741ee35ef98", "name": "10L1", "yearGroup": 10,
         "subject": "English Literature", "joinCode": "QENSA9", "joinOpen": True, "size": 25},
        {"id": "c2", "name": "10M2", "yearGroup": 10, "subject": "Mathematics",
         "joinCode": "8KY3JM", "joinOpen": True, "size": 25},
        {"id": "c3", "name": "11L4 Lit", "yearGroup": 11, "subject": "English Literature",
         "joinCode": "Z8Z2ZZ", "joinOpen": False, "size": 1},
    ],
    "subjects": [
        {"id": "s1", "name": "Business Studies", "own": True},
        {"id": "s2", "name": "Mathematics", "own": False},
    ],
}
