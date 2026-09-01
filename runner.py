#!/usr/bin/env python3
"""Runs a learner conversation against the course corpus.

One turn end-to-end: helper instruction file + module (+ optional learner
state) are assembled into a single request to a model; the reply is printed
and both sides are appended to a human-readable transcript.

Usage:
  python3 runner.py --helper helpers/smoke-tutor.md \
                    --module modules/01-networking-foundations.md \
                    [--state learner-state.example.md] \
                    [--replay examples/replay-smoke.txt] \
                    [--transcript transcripts/smoke.md] \
                    [--config runner-config.json]

Without --replay the runner reads learner turns from the terminal until EOF
or /exit. With --replay it runs the pre-written messages in the file (blank
lines separate messages, lines starting with # are ignored) with no human
input.

The model credential is read from the environment: ANTHROPIC_API_KEY, then
ANTHROPIC_AUTH_TOKEN. Model identity and parameters come from the config file.

Stdlib only.
"""

import argparse
import datetime
import json
import os
import sys
import urllib.error
import urllib.request

API_VERSION = "2023-06-01"
REQUEST_TIMEOUT_SECONDS = 120


def fail(message):
    print(f"runner: error: {message}", file=sys.stderr)
    sys.exit(1)


def read_required(path, what):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        fail(f"cannot read {what} '{path}': {e}")
    if not text.strip():
        fail(f"{what} '{path}' is empty")
    return text


def load_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            config = json.load(f)
    except OSError as e:
        fail(f"cannot read config '{path}': {e}")
    except json.JSONDecodeError as e:
        fail(f"config '{path}' is not valid JSON: {e}")
    for key in ("base_url", "model", "max_tokens"):
        if not config.get(key):
            fail(f"config '{path}' is missing required key '{key}'")
    return config


def split_module(text, path):
    title_line, _, rest = text.partition("\n")
    if not title_line.startswith("# "):
        fail(f"module '{path}' has no title heading: not a corpus module")
    meta, marker, content = rest.partition("\n## ")
    if not marker:
        fail(f"module '{path}' has no content sections")
    if not meta.strip():
        fail(f"module '{path}' has no metadata block")
    return meta.strip(), "## " + content.rstrip()


def build_system(instruction, module_meta, module_content, state_text, state_path):
    parts = [
        instruction.rstrip(),
        "## Module metadata",
        module_meta,
        "## Module content",
        module_content,
    ]
    if state_text is not None:
        parts += ["## Learner state", state_text.rstrip()]
    return "\n\n".join(parts)


def parameter_summary(config):
    parts = [f"max_tokens={config['max_tokens']}"]
    if "temperature" in config:
        parts.append(f"temperature={config['temperature']}")
    return ", ".join(parts)


def call_model(config, api_key, system, history):
    body = {
        "model": config["model"],
        "max_tokens": config["max_tokens"],
        "system": system,
        "messages": history,
    }
    if "temperature" in config:
        body["temperature"] = config["temperature"]
    request = urllib.request.Request(
        config["base_url"].rstrip("/") + "/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        fail(f"model request failed: HTTP {e.code}: {detail}")
    except (urllib.error.URLError, OSError) as e:
        fail(f"model request failed: {e}")
    texts = [block["text"] for block in data.get("content", []) if block.get("type") == "text"]
    if not texts:
        fail(f"model reply has no text blocks: {json.dumps(data)[:500]}")
    return "\n".join(texts)


def run_header(mode, helper_name, helper_path, module_path, state_path, config):
    state_note = f"present ({state_path})" if state_path else "none"
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        f"## Run — {timestamp} ({mode})\n"
        f"- Helper: {helper_name} ({helper_path})\n"
        f"- Module: {module_path}\n"
        f"- Learner state: {state_note}\n"
        f"- Model: {config['model']} ({parameter_summary(config)})\n"
        f"- Base URL: {config['base_url']}\n"
    )


def turn_block(number, message, reply, helper_name, module_path, state_path, config):
    state_note = f"present ({state_path})" if state_path else "none"
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        f"\n### Turn {number}\n"
        f"- Helper: {helper_name}\n"
        f"- Module: {module_path}\n"
        f"- Learner state: {state_note}\n"
        f"- Model: {config['model']} ({parameter_summary(config)})\n"
        f"- Time: {timestamp}\n"
        f"\nLearner:\n\n{message}\n"
        f"\nHelper reply (verbatim):\n\n{reply}\n"
    )


def write_transcript(path, text):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    first_write = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if first_write:
            f.write("# Learner conversation transcript\n")
        f.write(text)


def read_replay(path):
    text = read_required(path, "replay file")
    messages = []
    for block in text.split("\n\n"):
        lines = [line for line in block.splitlines() if not line.lstrip().startswith("#")]
        message = "\n".join(lines).strip()
        if message:
            messages.append(message)
    if not messages:
        fail(f"replay file '{path}' contains no messages")
    return messages


def read_turns_interactive():
    while True:
        try:
            line = input("you> ")
        except EOFError:
            return
        line = line.strip()
        if line in ("/exit", "/quit"):
            return
        if line:
            yield line


def main():
    parser = argparse.ArgumentParser(description="Run a learner conversation against the corpus.")
    parser.add_argument("--helper", required=True, help="course-helper instruction file")
    parser.add_argument("--module", required=True, help="module file from modules/")
    parser.add_argument("--state", help="optional learner-state file")
    parser.add_argument("--replay", help="file of pre-written messages, run without human input")
    parser.add_argument("--transcript", help="transcript file (default: transcripts/<helper>.md)")
    parser.add_argument("--config", default="runner-config.json", help="model config file")
    args = parser.parse_args()

    config = load_config(args.config)
    instruction = read_required(args.helper, "helper instruction file")
    module_text = read_required(args.module, "module")
    module_meta, module_content = split_module(module_text, args.module)
    state_text = None
    if args.state:
        state_text = read_required(args.state, "learner-state file")

    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
    if not api_key:
        fail("no model credential: set ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN")

    helper_name = os.path.splitext(os.path.basename(args.helper))[0]
    transcript_path = args.transcript or os.path.join("transcripts", helper_name + ".md")

    system = build_system(instruction, module_meta, module_content, state_text, args.state)
    mode = "replay" if args.replay else "interactive"
    turns = read_replay(args.replay) if args.replay else read_turns_interactive()
    history = []

    write_transcript(
        transcript_path,
        run_header(mode, helper_name, args.helper, args.module, args.state, config),
    )

    number = 0
    for message in turns:
        number += 1
        history.append({"role": "user", "content": message})
        reply = call_model(config, api_key, system, history)
        history.append({"role": "assistant", "content": reply})
        print(f"{helper_name}: {reply}")
        write_transcript(
            transcript_path,
            turn_block(number, message, reply, helper_name, args.module, args.state, config),
        )

    print(f"transcript: {transcript_path}")


if __name__ == "__main__":
    main()
