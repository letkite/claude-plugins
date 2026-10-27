#!/usr/bin/env python3
"""Check the marketplace and plugin manifests (standard library only).

Every JSON file must parse; the marketplace must list each plugin directory
with a matching plugin.json; MCP servers must be public HTTPS URLs; every
skill needs name and description frontmatter. Exits non-zero on a problem.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MCP_URL = "https://mcp.letkite.com/mcp"
FORBIDDEN = re.compile(r"\.dev\.letkite\.com|localhost|127\.0\.0\.1|\b10\.\d+\.\d+\.\d+")
NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")

errors = []


def fail(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        fail(path, f"invalid JSON: {e}")
        return None


def check_name(path, name):
    if not isinstance(name, str) or not NAME.match(name):
        fail(path, f"name {name!r} must be kebab-case")
    elif name.startswith(("claude-", "anthropic-")):
        fail(path, f"name {name!r} must not start with claude- or anthropic-")


for path in sorted(ROOT.rglob("*.json")):
    if ".git" in path.parts:
        continue
    data = load(path)
    if data is not None and FORBIDDEN.search(json.dumps(data)):
        fail(path, "mentions a private or development host")

market_path = ROOT / ".claude-plugin" / "marketplace.json"
market = load(market_path) or {}
check_name(market_path, market.get("name"))
if not isinstance(market.get("owner"), dict) or not market["owner"].get("name"):
    fail(market_path, "owner.name is required")
plugins = market.get("plugins")
if not isinstance(plugins, list) or not plugins:
    fail(market_path, "plugins must be a non-empty list")
    plugins = []

seen = set()
for entry in plugins:
    name = entry.get("name")
    check_name(market_path, name)
    if name in seen:
        fail(market_path, f"plugin {name!r} listed twice")
    seen.add(name)
    source = entry.get("source")
    if not isinstance(source, str) or not source.startswith("./"):
        fail(market_path, f"plugin {name!r}: source must be a ./ path in this repository")
        continue
    pdir = (ROOT / source).resolve()
    if not pdir.is_dir() or ROOT not in pdir.parents:
        fail(market_path, f"plugin {name!r}: {source} is not a directory here")
        continue

    manifest_path = pdir / ".claude-plugin" / "plugin.json"
    manifest = load(manifest_path) if manifest_path.is_file() else None
    if manifest is None:
        fail(manifest_path, "missing or invalid")
    else:
        if manifest.get("name") != name:
            fail(manifest_path, f"name {manifest.get('name')!r} differs from the marketplace entry {name!r}")
        if not re.match(r"^\d+\.\d+\.\d+$", str(manifest.get("version", ""))):
            fail(manifest_path, "version must be MAJOR.MINOR.PATCH")
        if not manifest.get("description"):
            fail(manifest_path, "description is required")

    mcp_path = pdir / ".mcp.json"
    if mcp_path.is_file():
        servers = (load(mcp_path) or {}).get("mcpServers")
        if not isinstance(servers, dict) or not servers:
            fail(mcp_path, "mcpServers must be a non-empty object")
            servers = {}
        for sname, server in servers.items():
            if server.get("type") != "http":
                fail(mcp_path, f"{sname}: type must be http")
            if server.get("url") != MCP_URL:
                fail(mcp_path, f"{sname}: url must be {MCP_URL}")
            if "headers" in server or "env" in server:
                fail(mcp_path, f"{sname}: no headers or env, sign-in is OAuth")

    for skill in sorted(pdir.glob("skills/*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        front = m.group(1) if m else ""
        sname = re.search(r"^name:\s*(\S+)\s*$", front, re.M)
        if not sname or sname.group(1) != skill.parent.name:
            fail(skill, "frontmatter name must match the directory name")
        if not re.search(r"^description:\s*\S", front, re.M):
            fail(skill, "frontmatter description is required")

for e in errors:
    print(f"error: {e}", file=sys.stderr)
if errors:
    sys.exit(1)
print(f"ok: {len(seen)} plugin(s) checked")
