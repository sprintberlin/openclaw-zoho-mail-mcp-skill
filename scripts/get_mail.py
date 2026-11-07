#!/usr/bin/env python3
"""Get full details of a single mail."""
from __future__ import annotations
import json, sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from mail_client import ENDPOINT, build_base_parser, call
def build_parser():
    parser = build_base_parser("Get Zoho Mail details.")
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--folder-id", required=True)
    parser.add_argument("--id", required=True, help="message ID")
    return parser
def main(argv=None):
    args = build_parser().parse_args(argv)
    ENDPOINT.configure(args)
    result = call("get mail", {"headers": {}, "query_params": {"account_id": args.account_id, "folder_id": args.folder_id, "id": args.id}}, timeout=args.timeout)
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr); return 1
    print(json.dumps(result, indent=2, ensure_ascii=False)); return 0
if __name__ == "__main__":
    sys.exit(main())
