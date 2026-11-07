"""Tests for the Zoho Mail catalog, profiles, and lookup CLI."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
CATALOG = REPOSITORY / "references" / "actions.jsonl"
PROFILES = REPOSITORY / "references" / "profiles.json"
LOOKUP = REPOSITORY / "scripts" / "lookup_actions.py"
sys.path.insert(0, str(REPOSITORY / "scripts"))
import lookup_actions  # noqa: E402
import mail_client  # noqa: E402

FORBIDDEN = {
    "addUser", "deleteUser", "resetUserPassword", "addDomain", "deleteDomain",
    "createPolicy", "addAllowedIP", "clear mails from trash", "empty folder",
    "clear folder from trash", "delete account", "addMailForward",
}


class MailCatalogTests(unittest.TestCase):
    def test_catalog_has_397_actions(self):
        lines = [line for line in CATALOG.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(lines), 397)
        keys = set()
        for line in lines:
            record = json.loads(line)
            for field in ("key", "name", "group", "summary", "description", "added"):
                self.assertTrue(str(record.get(field, "")).strip())
            self.assertNotIn(record["key"], keys)
            keys.add(record["key"])
        self.assertIn("send mail", keys)
        self.assertIn("search mail advanced", keys)

    def test_profiles_validate(self):
        result = subprocess.run([sys.executable, str(LOOKUP), "--validate"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_profile_sizes_and_rights(self):
        profiles = json.loads(PROFILES.read_text(encoding="utf-8"))["profiles"]
        counts = {name: len(lookup_actions.resolve_profile_actions(name, profiles)) for name in profiles}
        self.assertEqual(counts, {"mail-reader": 34, "mail-composer": 40, "mail-organizer": 74, "mail-employee": 87})
        reader = lookup_actions.resolve_profile_actions("mail-reader", profiles)
        employee = lookup_actions.resolve_profile_actions("mail-employee", profiles)
        self.assertIn("list mails", reader)
        self.assertNotIn("send mail", reader)
        self.assertIn("send mail", employee)
        self.assertIn("move mails", employee)
        self.assertTrue(FORBIDDEN.isdisjoint(employee))
        self.assertLessEqual(max(counts.values()), 300)

    def test_denied_applies_through_inheritance(self):
        profiles = {
            "a": {"actions": ["x", "y"], "denied": ["z"]},
            "b": {"extends": "a", "actions": ["z", "w"]},
        }
        self.assertEqual(lookup_actions.resolve_profile_actions("b", profiles), ["x", "y", "w"])

    def test_paginate_survives_server_side_page_cap(self):
        pages = [[{"id": i} for i in range(25)], [{"id": i} for i in range(25, 40)], []]
        calls = []

        def fake_call(tool, args, timeout=30):
            calls.append(args["query_params"]["start"])
            return {"data": {"messages": pages[len(calls) - 1]}}

        original = mail_client.call
        mail_client.call = fake_call
        try:
            result = mail_client.paginate("list mails", page_size=50, max_records=100)
        finally:
            mail_client.call = original
        self.assertEqual(len(result["data"]), 40)
        self.assertEqual(calls, [1, 26, 41])

    def test_accounts_primary_account_shape(self):
        result = {"data": {"data": {"primaryAccount": {"accountId": "1", "emailAddress": "a@b.c"}}}}
        self.assertEqual(mail_client.rows(result)[0]["accountId"], "1")

    def test_search_and_runtime_name(self):
        result = subprocess.run(
            [sys.executable, str(LOOKUP), "--search", "attachment", "--names-only"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("get mail attachment", result.stdout)
        self.assertEqual(mail_client.runtime_tool("send mail"), "ZohoMail_send_mail")
        self.assertEqual(mail_client.runtime_tool("fetchUser"), "ZohoMail_fetchUser")


if __name__ == "__main__":
    unittest.main()
