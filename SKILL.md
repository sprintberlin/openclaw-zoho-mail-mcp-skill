---
name: "zoho-mail-mcp"
description: "Zoho Mail via MCP with the full 397-action catalog, least-privilege mailbox profiles (reader, composer, organizer, employee), and mailbox helpers. Use whenever a task involves reading, searching, writing, replying, forwarding, moving, labeling, or organizing mail in a Zoho Mail mailbox, or when an agent needs its own Zoho Mail account."
---

# Zoho Mail MCP

Use Zoho Mail through an MCP endpoint from `mcp.zoho.eu`. This skill is the canonical home for Mail-specific MCP action documentation and least-privilege action profiles.

Source: [sprintberlin/openclaw-zoho-mail-mcp-skill](https://github.com/sprintberlin/openclaw-zoho-mail-mcp-skill)

## Requirements

- A Zoho Mail MCP endpoint from `mcp.zoho.eu`, connected to the mailbox the agent should use
- `mcporter`
- Endpoint configuration via `ZOHO_MAIL_MCP_URL`, `--profile`, or `--mcp-url`

Treat the endpoint as a credential. Never print it, commit it, or copy it into tickets, prompts, or chats.

## Improve during daily use

Daily use is the discovery loop. Treat every reusable defect, missing capability, safer check, or useful simplification as a contribution.

1. Search open issues immediately with native `gh`; link a match or create one.
2. Include the need, sanitized evidence, expected behavior, and acceptance criteria. Never include MCP URLs, tokens, mail content, addresses, or live IDs.
3. If implementation is feasible now: issue, branch, code/docs/tests, PR, CI, merge.
4. If not feasible now: file the issue before finishing and return its URL.
5. Do not add a GitHub wrapper script. Use native `git` and `gh`. See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
REPO=sprintberlin/openclaw-zoho-mail-mcp-skill
gh issue list --repo "$REPO" --state open --search "<terms>"
python3 -m unittest discover -s tests -v
```

## First setup

1. Create a Zoho Mail MCP server at `mcp.zoho.eu` and authorize it with the mailbox owner's own Zoho account.
2. Pick one profile and select only its Actions. Resolve the exact list from the JSON catalog:

```bash
python3 scripts/lookup_actions.py --profiles
python3 scripts/lookup_actions.py --profile mail-reader --names-only
python3 scripts/lookup_actions.py --profile mail-composer --names-only
python3 scripts/lookup_actions.py --profile mail-organizer --names-only
python3 scripts/lookup_actions.py --profile mail-employee --names-only
python3 scripts/lookup_actions.py --task triage-inbox --names-only
```

3. Search the catalog when a profile lacks an Action:

```bash
python3 scripts/lookup_actions.py --search "label"
python3 scripts/lookup_actions.py --action "send mail"
```

4. Configure one default endpoint with `ZOHO_MAIL_MCP_URL`, or named profiles per [references/MULTI_ACCOUNT.md](references/MULTI_ACCOUNT.md).
5. Inspect the live server before relying on an Action:

```bash
mcporter list "$ZOHO_MAIL_MCP_URL"
```

The catalog describes possible Actions, not what is enabled on a given server. Runtime tool names carry the `ZohoMail_` prefix and use the `ref_name` form with underscores (for example `ZohoMail_send_mail`, `ZohoMail_list_mails`). The setup UI shows the display name (`send mail`). Some admin Actions are camelCase in both (`fetchUser`).

The Zoho Mail catalog has 397 Actions (captured 2026-11-07 from the MCP console). The 300-Action server limit applies: a server accepts at most 300 selected Actions, so never select the whole catalog. All profiles here stay far below it.

## Role profiles

| Profile | Actions | Purpose |
|---|---|---|
| `mail-reader` | 34 | read-only: accounts, folders, labels, mails, threads, attachments, search, settings |
| `mail-composer` | 40 | reader plus send, reply, forward, drafts, templates, compose attachments |
| `mail-organizer` | 74 | composer plus read state, flags, labels, move, archive, snooze, trash and restore, folders, thread actions |
| `mail-employee` | 87 | organizer plus own signatures, vacation reply, filters, reminders, compose/view settings |

Use `mail-employee` for an agent that works like a human employee in its own mailbox. Use `mail-reader` for lookup-only work.

Never selected by any profile: Domain, User, Group, Policy, Org Management, Audit Logs, mail forwarding rules, `clear mails from trash`, `empty folder`, `clear folder from trash`, account deletion, shared mailbox and Streams Actions. Add them only for an explicit task and the right Zoho role.

## Safe workflow

1. Confirm the right account. Never reuse an endpoint from another mailbox or customer.
2. `list accounts` first. Use the returned account ID. Never guess account, folder, label, or message IDs.
3. `list folders` and `list labels` to resolve IDs.
4. Search with the builder Actions (`build address search query`, `build content search query`, `build meta search query`), then `search mail advanced`.
5. Read before acting. Fetch the mail or thread before replying or moving.
6. Before sending: show the draft to the responsible human when the task requires approval. Use `save mail draft` for review flows. Check recipients, sender, and attachments.
7. After a write, read back (list the folder, fetch the mail) and report only what was verified.
8. Prefer `move mails to trash` over permanent deletion. `undo mail action` is available for a short window.

## Common calls

```bash
python3 scripts/list_accounts.py
python3 scripts/list_folders.py            # --account-id defaults to "me"
python3 scripts/list_mails.py --folder-id FOLDER_ID --limit 20
python3 scripts/get_mail.py --id MESSAGE_ID
```

Direct call with `mcporter`:

```bash
cat > /tmp/mail_accounts.json <<'JSON'
{"query_params": {}}
JSON
mcporter call "$ZOHO_MAIL_MCP_URL.ZohoMail_list_accounts" --args "$(< /tmp/mail_accounts.json)"
```

Use the schema shown by the live MCP server when it differs from these examples.

## Bundled scripts

All helpers resolve the endpoint via `--mcp-url`, `--profile`, or `ZOHO_MAIL_MCP_URL`, call `mcporter` without shell expansion, and accept `--json` and `--timeout`. Run any helper with `--help` without credentials.

## References

- [Action catalog](references/actions.jsonl)
- [Profiles and task recipes](references/profiles.json)
- [Catalog format](references/CATALOG_FORMAT.md)
- [Action profiles](references/ACTION_PROFILES.md)
- [Multi-account profiles](references/MULTI_ACCOUNT.md)

Query the catalog with `scripts/lookup_actions.py` instead of loading `actions.jsonl` into context.

## Troubleshooting and safety

- **No endpoint configured**: set `ZOHO_MAIL_MCP_URL`, use `--profile`, or `--mcp-url`; never print the value.
- **Authorization error**: the mailbox user lacks the right for that Action. Admin Actions need Zoho Mail admin rights. Do not switch to another mailbox.
- **New Actions added to the server**: Zoho asks for re-authorization; if not, regenerate the API key in the MCP console and update the stored endpoint.
- **Send-as for other mailboxes**: needs explicit delegation by the mailbox owner. Do not assume it.
- A mailbox contains personal and customer data. Load only what the task needs and never copy mail content, addresses, or IDs into chats, logs, or repositories.
