#!/usr/bin/env python3
"""List Zoho Mail folders for an account."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from mail_client import ENDPOINT, build_base_parser, call, finish, rows
COLUMNS = [("ID", ["folderId", "folder_id", "id"]), ("Name", ["folderName", "folder_name", "name"]), ("Count", ["count", "totalCount", "messageCount"])]
def build_parser():
    parser = build_base_parser("List Zoho Mail folders.")
    parser.add_argument("--account-id", default="me", help="Zoho Mail account ID (default: me)")
    return parser
def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    result = call("list folders", {"path_variables": {"accountId": args.account_id}}, timeout=args.timeout)
    records = rows(result) if "error" not in result else []
    return finish(result, records, args, COLUMNS, empty="No folders found.")
if __name__ == "__main__":
    sys.exit(main())
