#!/usr/bin/env python3
"""Self-check for runner.py.

Runs the runner against a stub model endpoint (by pointing a temporary config
at it) using the real corpus module, and checks the transcript contract:
per-turn learner message, verbatim reply, helper name, module, learner-state
presence, and model identity and parameters. Also checks that missing or
malformed inputs fail loudly.

Run: python3 test-runner.py
"""

import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "runner.py")
MODULE = os.path.join(HERE, "modules", "01-networking-foundations.md")

requests_seen = []


class StubHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["content-length"])
        body = json.loads(self.rfile.read(length))
        requests_seen.append(body)
        payload = {
            "id": "msg_stub",
            "type": "message",
            "role": "assistant",
            "model": body["model"],
            "content": [{"type": "text", "text": "STUB-REPLY-%d" % len(requests_seen)}],
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 1, "output_tokens": 1},
        }
        data = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def run_runner(args, env):
    return subprocess.run(
        [sys.executable, RUNNER] + args,
        cwd=HERE,
        env=env,
        capture_output=True,
        text=True,
    )


def check(condition, message):
    if not condition:
        print(f"FAIL: {message}")
        sys.exit(1)


def main():
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), StubHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = "http://127.0.0.1:%d" % server.server_address[1]

    tempdir = tempfile.mkdtemp()
    helper_path = os.path.join(tempdir, "smoke-tutor.md")
    state_path = os.path.join(tempdir, "learner-state.md")
    replay_path = os.path.join(tempdir, "replay.txt")
    config_path = os.path.join(tempdir, "config.json")
    transcript_path = os.path.join(tempdir, "transcript.md")
    with open(helper_path, "w", encoding="utf-8") as f:
        f.write("Be the smoke tutor. Ground answers in the module below.\n")
    with open(state_path, "w", encoding="utf-8") as f:
        f.write("- Current module: modules/01-networking-foundations.md\n")
    with open(replay_path, "w", encoding="utf-8") as f:
        f.write("# comment line\n\nfirst learner message\n\nsecond learner message\n")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({"base_url": base_url, "model": "stub-model", "max_tokens": 128}, f)
    env = dict(os.environ)
    env["ANTHROPIC_API_KEY"] = "test-key"

    result = run_runner(
        [
            "--helper", helper_path,
            "--module", MODULE,
            "--state", state_path,
            "--replay", replay_path,
            "--transcript", transcript_path,
            "--config", config_path,
        ],
        env,
    )
    check(result.returncode == 0, f"replay run failed: {result.stderr}")

    check(len(requests_seen) == 2, f"expected 2 model requests, saw {len(requests_seen)}")
    for i, request in enumerate(requests_seen):
        check(request["model"] == "stub-model", f"request {i} model not from config")
        check(request["max_tokens"] == 128, f"request {i} max_tokens not from config")
        check("Be the smoke tutor" in request["system"], f"request {i} system lacks instruction text")
        check("## Module metadata" in request["system"], f"request {i} system lacks module metadata")
        check("**Title**" in request["system"], f"request {i} system lacks module metadata content")
        check("## Module content" in request["system"], f"request {i} system lacks module content")
        check("CIDR" in request["system"], f"request {i} system lacks module content text")
        check("## Learner state" in request["system"], f"request {i} system lacks learner state")
    check(
        requests_seen[0]["messages"][0] == {"role": "user", "content": "first learner message"},
        "first request does not carry the first learner message",
    )
    second_history = requests_seen[1]["messages"]
    check(len(second_history) == 3, f"second request history has {len(second_history)} messages, expected 3")
    check(
        [m["role"] for m in second_history] == ["user", "assistant", "user"],
        f"second request history roles wrong: {[m['role'] for m in second_history]}",
    )
    check(
        second_history[1] == {"role": "assistant", "content": "STUB-REPLY-1"},
        "second request does not carry the first model reply in history",
    )

    with open(transcript_path, encoding="utf-8") as f:
        transcript = f.read()
    check("smoke-tutor" in transcript, "transcript lacks helper name")
    check("modules/01-networking-foundations.md" in transcript, "transcript lacks module")
    check(f"present ({state_path})" in transcript, "transcript lacks learner-state presence")
    check("stub-model" in transcript, "transcript lacks model identity")
    check("max_tokens=128" in transcript, "transcript lacks model parameters")
    check("first learner message" in transcript, "transcript lacks first learner message")
    check("second learner message" in transcript, "transcript lacks second learner message")
    check("STUB-REPLY-1" in transcript, "transcript lacks first reply")
    check("STUB-REPLY-2" in transcript, "transcript lacks second reply")
    check(transcript.count("### Turn") == 2, "transcript does not record two turns")

    # Missing module fails loudly.
    missing = run_runner(
        ["--helper", helper_path, "--module", os.path.join(tempdir, "nope.md"),
         "--replay", replay_path, "--transcript", transcript_path, "--config", config_path],
        env,
    )
    check(missing.returncode != 0, "missing module did not fail")
    check("cannot read module" in missing.stderr, f"missing module error not loud: {missing.stderr}")

    # Config without a model fails loudly.
    bad_config = os.path.join(tempdir, "bad-config.json")
    with open(bad_config, "w", encoding="utf-8") as f:
        json.dump({"base_url": base_url, "max_tokens": 128}, f)
    bad = run_runner(
        ["--helper", helper_path, "--module", MODULE, "--replay", replay_path,
         "--transcript", transcript_path, "--config", bad_config],
        env,
    )
    check(bad.returncode != 0, "config missing model did not fail")
    check("missing required key 'model'" in bad.stderr, f"bad config error not loud: {bad.stderr}")

    server.shutdown()
    print("test-runner: all checks passed")


if __name__ == "__main__":
    main()
