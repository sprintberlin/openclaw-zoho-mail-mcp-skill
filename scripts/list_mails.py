#!/usr/bin/env python3
"""List mails in a folder with filtering and pagination."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from mail_client import ENDPOINT, build_base_parser, call, finish, paginate
COLUMNS = [("ID", ["messageId", "message_id", "id"]), ("From", ["fromAddress", "from", "sender"]), ("Subject", ["subject"]), ("Date", ["sentDateInGMT", "date", "receivedtime"])]
def build_parser():
    parser = build_base_parser("List Zoho Mail mails.")
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--folder-id", required=True)
    parser.add_argument("--limit", type=int, default=20)
    return parser
def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    result = paginate("list mails", headers={}, params={"account_id": args.account_id, "folder_id": args.folder_id}, page_size=20, max_records=args.limit, timeout=args.timeout)
    records = result.get("data", []) if "error" not in result else []
    return finish(result, records, args, COLUMNS, empty="No mails found.")
if __name__ == "__main__":
    sys.exit(main())
