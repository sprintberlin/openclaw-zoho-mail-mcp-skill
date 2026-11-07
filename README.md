# Zoho Mail MCP

Connect your agent to Zoho Mail through the Model Context Protocol (MCP). This skill gives an agent its own mailbox: read, search, write, reply, forward, move, label, and organize mail, with least-privilege action profiles and a searchable catalog of all 397 Zoho Mail MCP Actions.

## What This Skill Includes

- Agent instructions in `SKILL.md`
- JSON action catalog (`references/actions.jsonl`, 397 Actions, captured from the MCP console on 2026-11-07)
- Four profiles: **mail-reader** (34), **mail-composer** (40), **mail-organizer** (74), **mail-employee** (87), plus task recipes
- Helpers for accounts, folders, mail lists, and single mails via `mcporter`
- Multi-account endpoint profiles, no shell expansion, no credentials in output
- Issue-first contribution rules in [CONTRIBUTING.md](CONTRIBUTING.md)

## Requirements

| Requirement | Details |
|---|---|
| Zoho Mail MCP server | Endpoint from [mcp.zoho.eu](https://mcp.zoho.eu), authorized by the mailbox owner |
| mcporter | MCP client CLI |
| Endpoint | `ZOHO_MAIL_MCP_URL`, named profile, or `--mcp-url` |

```bash
export ZOHO_MAIL_MCP_URL='<your Zoho Mail MCP endpoint>'
mcporter list "$ZOHO_MAIL_MCP_URL"
python3 scripts/list_accounts.py
```

## Pick the Actions

```bash
python3 scripts/lookup_actions.py --profiles
python3 scripts/lookup_actions.py --profile mail-employee --names-only
python3 scripts/lookup_actions.py --search "attachment"
python3 scripts/lookup_actions.py --validate
```

A Zoho MCP server accepts at most 300 Actions, so select a profile, not the catalog.

## Security

The MCP URL is a password. Keep it in a secret store. Admin, domain, user, policy, org, and permanent-delete Actions are excluded from every profile by design. A mailbox contains personal data: load only what the task needs.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT
