#!/usr/bin/env python3
"""Extracts per-module replay files and a manifest from probes.md.

Each probe becomes one replay message, preceded by a comment line carrying the
probe id. With --check, regenerates and diffs against the files on disk
instead of writing, so a post-run invocation proves replays still match the
frozen probe file.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(HERE, "probes.md")
REPLAYS = os.path.join(HERE, "replays")


def parse(path):
    sections = []
    current = None
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for line in lines:
        module = re.match(r"^## Module \d+ — (modules/[\w.-]+\.md)$", line)
        probe = re.match(r"^### Probe (\d+\.\d+) — (.+)$", line)
        if module:
            current = {"module": module.group(1), "probes": []}
            sections.append(current)
        elif probe and current is not None:
            current["probes"].append({"id": probe.group(1), "category": probe.group(2), "lines": []})
        elif current is not None and current["probes"]:
            current["probes"][-1]["lines"].append(line)
    for section in sections:
        for probe in section["probes"]:
            lines = probe["lines"]
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
            if any(not line.strip() for line in lines):
                sys.exit(f"probe {probe['id']} contains a blank line; messages must be one paragraph")
            probe["message"] = "\n".join(lines).strip()
            if not probe["message"]:
                sys.exit(f"probe {probe['id']} has no message text")
    return sections


def render(sections):
    files = {}
    manifest = []
    for section in sections:
        number = re.match(r"modules/(\d+)-", section["module"]).group(1)
        blocks = []
        for probe in section["probes"]:
            blocks.append(f"# probe {probe['id']} — {probe['category']}\n{probe['message']}")
        files[f"probes-m{number}.txt"] = "\n\n".join(blocks) + "\n"
        manifest.append(f"m{number}\t{section['module']}")
    return files, "\n".join(manifest) + "\n"


def main():
    check = "--check" in sys.argv[1:]
    sections = parse(PROBES)
    files, manifest = render(sections)
    if check:
        for name, content in files.items():
            with open(os.path.join(REPLAYS, name), encoding="utf-8") as f:
                if f.read() != content:
                    sys.exit(f"{name} does not match probes.md; re-run without --check")
        with open(os.path.join(REPLAYS, "manifest.txt"), encoding="utf-8") as f:
            if f.read() != manifest:
                sys.exit("manifest.txt does not match probes.md; re-run without --check")
        print("make-replays: replays match probes.md")
        return
    os.makedirs(REPLAYS, exist_ok=True)
    for name, content in files.items():
        with open(os.path.join(REPLAYS, name), "w", encoding="utf-8") as f:
            f.write(content)
    with open(os.path.join(REPLAYS, "manifest.txt"), "w", encoding="utf-8") as f:
        f.write(manifest)


if __name__ == "__main__":
    main()
