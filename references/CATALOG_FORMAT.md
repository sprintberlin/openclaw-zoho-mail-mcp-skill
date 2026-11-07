# Action Catalog Format

This document describes how MCP Action knowledge is stored in this skill. The same layout is used by the other Zoho MCP skills, so an agent learns the structure once and can then answer "which Actions do I need for this task".

## Problem

A Zoho MCP app exposes a set of Actions. Zoho Mail currently exposes 397 Actions. Written as prose Markdown, that catalog still has three defects:

1. An agent must load long descriptions into context to answer a small question.
2. Hand-written profile lists drift away from the real catalog.
3. Zoho adds, renames, and removes Actions, and a prose file makes that invisible in review.

## Design

JSON is the only source of truth. There is no generated or hand-maintained Markdown catalog.

| File | Purpose |
|---|---|
| `references/actions.jsonl` | Every known Action, one JSON object per line |
| `references/profiles.json` | Role profiles and task recipes, referencing Action keys |
| `scripts/import_actions.py` | Rebuilds `actions.jsonl` from a Zoho MCP setup UI dump |
| `scripts/lookup_actions.py` | Answers profile, task, and search questions without loading the full catalog |

### Why JSONL for the catalog

One Action per line keeps Git diffs readable. When Zoho changes the catalog, review shows exactly which lines were added, changed, or marked removed.

### Action record

```json
{"key":"send mail","name":"send mail","group":"Messages","summary":"Composes and sends a new mail.","description":"Full text as delivered by the MCP console.","added":"2026-11-07"}
```

- `key`: unique identifier used by profiles and tasks. Equal to `name` except for grouped Actions.
- `name`: the Action name shown in the Zoho MCP setup UI. On the live server it carries the `ZohoMail_` prefix and spaces become underscores (`send mail` becomes `ZohoMail_send_mail`).
- `group`: the Zoho console group, for example `Messages` or `Message Actions`.
- `summary`: shortened first line for fast scanning.
- `description`: the untouched description text delivered by Zoho.
- `added`: date the Action first appeared in the catalog.
- `removed`: set when an Action disappears from a newer dump.

This catalog was captured on 2026-11-07 from the Zoho MCP console service action catalog (397 Actions, 36 groups). Refresh it when Zoho expands the surface.

## Usage

```bash
python3 scripts/lookup_actions.py --profiles
python3 scripts/lookup_actions.py --profile mail-reader --names-only
python3 scripts/lookup_actions.py --task triage-inbox --names-only
python3 scripts/lookup_actions.py --search "draft"
python3 scripts/lookup_actions.py --action "send mail"
python3 scripts/lookup_actions.py --validate
```

## Maintaining the catalog

1. Open the Zoho MCP setup UI for Zoho Mail and copy the complete Action list into a text file, or export a live `mcporter list --json`.
2. Rebuild from a UI dump:

   ```bash
   python3 scripts/import_actions.py /tmp/mail_actions_dump.txt --dry-run
   python3 scripts/import_actions.py /tmp/mail_actions_dump.txt
   ```

3. Validate that profiles and tasks still reference existing Actions:

   ```bash
   python3 scripts/lookup_actions.py --validate
   ```

4. Fix any profile or task entry the validation rejects, then commit.

The catalog describes Actions that can exist for the app. It does not prove that an Action is enabled on a specific MCP server. Always confirm against the live server:

```bash
mcporter list "$ZOHO_MAIL_MCP_URL"
```

Runtime tool names carry the `ZohoMail_` prefix; the catalog and the setup UI use the bare Action name.
