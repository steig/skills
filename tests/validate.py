#!/usr/bin/env python3
"""Validate the marketplace/plugin manifests and skill layout.

Run from anywhere: python3 tests/validate.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


def load_json(rel):
    path = ROOT / rel
    check(path.is_file(), f"{rel}: missing")
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        failures.append(f"{rel}: invalid JSON ({e})")
        return None


def frontmatter(path):
    text = path.read_text()
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


marketplace = load_json(".claude-plugin/marketplace.json")
plugin = load_json(".claude-plugin/plugin.json")

if marketplace is not None:
    check(KEBAB.match(marketplace.get("name", "")), "marketplace: name must be kebab-case")
    check(marketplace.get("owner", {}).get("name"), "marketplace: owner.name required")
    plugins = marketplace.get("plugins", [])
    check(plugins, "marketplace: plugins must be non-empty")
    for entry in plugins:
        name = entry.get("name", "<unnamed>")
        check(KEBAB.match(entry.get("name", "")), f"marketplace plugin {name}: name must be kebab-case")
        source = entry.get("source")
        check(source, f"marketplace plugin {name}: source required")
        if isinstance(source, str):
            check(
                source == "./" or source.startswith("./"),
                f"marketplace plugin {name}: relative source must start with ./",
            )
            check(
                (ROOT / source / ".claude-plugin/plugin.json").is_file(),
                f"marketplace plugin {name}: source {source} has no .claude-plugin/plugin.json",
            )
        elif isinstance(source, dict):
            if source.get("source") == "github":
                check(
                    re.match(r"^[\w.-]+/[\w.-]+$", source.get("repo", "")),
                    f"marketplace plugin {name}: github source needs repo in owner/repo form",
                )
            else:
                check(source.get("source"), f"marketplace plugin {name}: source object needs a source type")

if plugin is not None:
    check(KEBAB.match(plugin.get("name", "")), "plugin: name must be kebab-case")
    check(plugin.get("description"), "plugin: description required")
    if marketplace is not None:
        entry = next((p for p in marketplace.get("plugins", []) if p.get("source") == "./"), None)
        check(entry is not None, "marketplace: no plugin entry sourced from this repo (./)")
        if entry is not None:
            check(
                entry.get("name") == plugin.get("name"),
                f"marketplace entry {entry.get('name')} != plugin.json name {plugin.get('name')}",
            )

skills_dir = ROOT / "skills"
skill_dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir()) if skills_dir.is_dir() else []
check(skill_dirs, "skills/: no skill directories found")
for d in skill_dirs:
    rel = d.relative_to(ROOT)
    skill_md = d / "SKILL.md"
    check(skill_md.is_file(), f"{rel}: missing SKILL.md")
    if not skill_md.is_file():
        continue
    fm = frontmatter(skill_md)
    check(fm is not None, f"{rel}/SKILL.md: missing YAML frontmatter")
    if fm is None:
        continue
    check(fm.get("name") == d.name, f"{rel}/SKILL.md: frontmatter name {fm.get('name')!r} != directory name {d.name!r}")
    check(fm.get("description"), f"{rel}/SKILL.md: frontmatter description required")

if failures:
    print("FAIL")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print(f"OK: manifests valid, {len(skill_dirs)} skill(s) checked: {', '.join(d.name for d in skill_dirs)}")
