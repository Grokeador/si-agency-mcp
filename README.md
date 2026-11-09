# SI-Agency-MCP: 7 Free MCP Servers Windows Installer & Doctor

**Created by [SI NEWS](https://www.youtube.com/channel/UC4m6veQiZdc_pAfxKQluRgA) • Official companion repo for *"7 Free MCP Servers That Turn Claude Desktop Into a Full Software Agency"*.**

Most `claude_desktop_config.json` examples online are written for macOS and fail on Windows 11 with `spawn npx ENOENT`, unescaped backslash syntax errors, or orphaned `node.exe` locks.

`si-agency-mcp` gives you a zero-dependency Python 3 tool (`si_mcp_doctor.py`) and an Autonomous Agency skill (`SKILL.md`) that:
1. **Generates a 100% Windows-hardened 7-Server `claude_desktop_config.json`** (`cmd /c npx -y ...` and normalized forward-slash paths).
2. **Safely merges into your existing `%APPDATA%\Claude\claude_desktop_config.json`** without deleting your other MCP servers.
3. **Audits & repairs broken Windows paths** (`C:\Projects` -> `C:/Projects`) and checks workspace readiness.

## Quick Start (Windows PowerShell)
```powershell
git clone https://github.com/Grokeador/si-agency-mcp
cd si-agency-mcp
python -m unittest discover -s tests -v
python si_mcp_doctor.py --workspace "C:/Projects" --print
```

To merge directly into your Claude Desktop config (creates a `.bak` backup first):
```powershell
python si_mcp_doctor.py --workspace "C:/Projects" --install
```

## The 7 Free MCP Servers Included
1. `filesystem` (`@modelcontextprotocol/server-filesystem`) — Local Architect & Coder
2. `playwright` (`@playwright/mcp@latest`) — Live Chromium UI Cloner & QA Tester
3. `sequential-thinking` (`@modelcontextprotocol/server-sequential-thinking`) — CTO Architecture Planner
4. `memory` (`@modelcontextprotocol/server-memory`) — Persistent Knowledge Graph
5. `sqlite` (`mcp-server-sqlite`) — Local Database Engineer
6. `git` (`mcp-server-git`) — DevOps Branch & Commit Manager
7. `fetch` (`mcp-server-fetch`) — Live 2026 Documentation Reader

MIT Licensed — Built by [SI NEWS](https://www.youtube.com/channel/UC4m6veQiZdc_pAfxKQluRgA).
