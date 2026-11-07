#!/usr/bin/env python3
"""List mails in a folder with filtering and pagination."""
from __future__ import annotations
import sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from mail_client import ENDPOINT, build_base_parser, call, finish, paginate
COLUMNS = [("ID", ["messageId", "message_id", "id"]), ("From", ["fromAddress", "from", "sender"]), ("Subject", ["subject"]), ("Date", ["receivedTime", "sentDateInGMT", "date"])]
def build_parser():
    parser = build_base_parser("List Zoho Mail mails.")
    parser.add_argument("--account-id", default="me")
    parser.add_argument("--folder-id", help="folder ID (optional)")
    parser.add_argument("--limit", type=int, default=20)
    return parser
def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    result = paginate("list mails", path_variables={"accountId": args.account_id}, params=({"folderId": args.folder_id} if args.folder_id else {}), page_size=50, max_records=args.limit, timeout=args.timeout)
    records = result.get("data", []) if "error" not in result else []
    return finish(result, records, args, COLUMNS, empty="No mails found.")
if __name__ == "__main__":
    sys.exit(main())
