#!/usr/bin/env python3
"""List Zoho Mail accounts accessible to the authenticated user."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from mail_client import ENDPOINT, build_base_parser, call, field, finish, rows
COLUMNS = [("ID", ["accountId", "id", "account_id"]), ("Email", ["emailAddress", "email", "email_address"]), ("Name", ["displayName", "display_name", "name"]), ("Primary", ["isDefaultAccount", "isPrimary", "is_primary"])]
def build_parser():
    parser = build_base_parser("List Zoho Mail accounts.")
    parser.add_argument("--full", action="store_true", help="with --json, print complete records")
    return parser
def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    result = call("list accounts", {"query_params": {}}, timeout=args.timeout)
    records = rows(result) if "error" not in result else []
    return finish(result, records, args, COLUMNS, empty="No accounts found.")
if __name__ == "__main__":
    sys.exit(main())
