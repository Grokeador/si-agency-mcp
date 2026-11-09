import tempfile
import unittest
from pathlib import Path
import si_mcp_doctor as m


class TestSiAgency(unittest.TestCase):
    def test_normalize_win_path(self):
        self.assertEqual(m.normalize_win_path("C:\\Users\\jorge\\Projects\\"), "C:/Users/jorge/Projects")

    def test_build_7_servers_count_and_cmd_c(self):
        cfg = m.build_7_server_config("D:\\Dev\\Apps")
        servers = cfg["mcpServers"]
        self.assertEqual(len(servers), 7)
        self.assertEqual(servers["filesystem"]["command"], "cmd")
        self.assertEqual(servers["filesystem"]["args"][:2], ["/c", "npx"])
        self.assertEqual(servers["filesystem"]["args"][-1], "D:/Dev/Apps")
        self.assertEqual(servers["sqlite"]["args"][-1], "D:/Dev/Apps/agency_app.db")

    def test_repair_existing_wraps_bare_npx(self):
        broken = {
            "mcpServers": {
                "old_tool": {"command": "npx", "args": ["-y", "some-mcp", "C:\\Test\\Folder"]}
            }
        }
        repaired, fixes = m.repair_existing_config(broken)
        spec = repaired["mcpServers"]["old_tool"]
        self.assertEqual(spec["command"], "cmd")
        self.assertEqual(spec["args"][:2], ["/c", "npx"])
        self.assertEqual(spec["args"][-1], "C:/Test/Folder")
        self.assertTrue(len(fixes) >= 2)

    def test_merge_preserves_custom_servers(self):
        existing = {"mcpServers": {"godot-mcp": {"command": "node", "args": ["C:/godot/index.js"]}}}
        pack = m.build_7_server_config("C:/Projects")
        merged = m.merge_configs(existing, pack)
        self.assertIn("godot-mcp", merged["mcpServers"])
        self.assertEqual(len(merged["mcpServers"]), 8)

    def test_cli_install_to_temp_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_p = Path(tmp) / "claude_desktop_config.json"
            rc = m.main(["--workspace", "C:/MyCode", "--install", str(cfg_p)])
            self.assertEqual(rc, 0)
            self.assertTrue(cfg_p.exists())


if __name__ == "__main__":
    unittest.main()
