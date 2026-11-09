#!/usr/bin/env python3
"""
SI-Agency-MCP (by SI NEWS) — Windows-Hardened 7-Server MCP Config Generator & Doctor.
Standard library only.
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def normalize_win_path(raw_path: str) -> str:
    """Converts Windows backslashes into JSON-safe forward slashes and strips trailing slash."""
    s = str(raw_path or "C:/Projects").strip().replace("\\", "/")
    while "//" in s:
        s = s.replace("//", "/")
    return s.rstrip("/") or "C:/Projects"


def build_7_server_config(workspace: str = "C:/Projects", db_name: str = "agency_app.db") -> Dict[str, Any]:
    ws = normalize_win_path(workspace)
    db_path = f"{ws}/{db_name.lstrip('/')}"
    return {
        "mcpServers": {
            "filesystem": {
                "command": "cmd",
                "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", ws],
            },
            "playwright": {
                "command": "cmd",
                "args": ["/c", "npx", "-y", "@playwright/mcp@latest", "--viewport-size=1920,1080"],
            },
            "sequential-thinking": {
                "command": "cmd",
                "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-sequential-thinking"],
            },
            "memory": {
                "command": "cmd",
                "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-memory"],
            },
            "sqlite": {
                "command": "uvx",
                "args": ["mcp-server-sqlite", "--db-path", db_path],
            },
            "git": {
                "command": "uvx",
                "args": ["mcp-server-git", "--repository", ws],
            },
            "fetch": {
                "command": "uvx",
                "args": ["mcp-server-fetch"],
            },
        }
    }


def repair_existing_config(cfg: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """Fixes bare 'npx' commands on Windows (wrapping with cmd /c) and normalizes backslash paths."""
    fixes: List[str] = []
    out = json.loads(json.dumps(cfg)) if isinstance(cfg, dict) else {"mcpServers": {}}
    servers = out.setdefault("mcpServers", {})
    for name, spec in servers.items():
        if not isinstance(spec, dict):
            continue
        cmd = str(spec.get("command", "")).strip()
        args = list(spec.get("args") or [])
        if cmd.lower() in ("npx", "npx.cmd"):
            spec["command"] = "cmd"
            spec["args"] = ["/c", "npx"] + args
            fixes.append(f"{name}: wrapped bare npx with 'cmd /c npx'")
        new_args = []
        for a in spec.get("args", []):
            if isinstance(a, str) and "\\" in a and (":" in a or a.startswith("\\")):
                fixed_a = normalize_win_path(a)
                new_args.append(fixed_a)
                fixes.append(f"{name}: normalized path '{a}' -> '{fixed_a}'")
            else:
                new_args.append(a)
        spec["args"] = new_args
    return out, fixes


def merge_configs(existing: Dict[str, Any], new_pack: Dict[str, Any]) -> Dict[str, Any]:
    repaired, _ = repair_existing_config(existing)
    merged = json.loads(json.dumps(repaired))
    target = merged.setdefault("mcpServers", {})
    for k, v in new_pack.get("mcpServers", {}).items():
        target[k] = v
    return merged


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SI-Agency-MCP Doctor (by SI NEWS)")
    parser.add_argument("--workspace", type=str, default="C:/Projects", help="Workspace folder path")
    parser.add_argument("--print", dest="do_print", action="store_true", help="Print 7-server JSON config")
    parser.add_argument("--install", type=str, nargs="?", const="AUTO", help="Merge into claude_desktop_config.json")
    args = parser.parse_args(argv)

    pack = build_7_server_config(args.workspace)
    if args.do_print or not args.install:
        print(json.dumps(pack, indent=2))
        return 0

    target_path = (
        Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
        if args.install == "AUTO"
        else Path(args.install)
    )
    existing: Dict[str, Any] = {}
    if target_path.exists():
        shutil.copyfile(target_path, target_path.with_suffix(".json.bak"))
        try:
            existing = json.loads(target_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    target_path.parent.mkdir(parents=True, exist_ok=True)
    merged = merge_configs(existing, pack)
    target_path.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    print(f"[OK] Installed 7 MCP servers into {target_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
