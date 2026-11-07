# Zoho Mail MCP Action Profiles

Machine-readable source: [`profiles.json`](profiles.json), validated against [`actions.jsonl`](actions.jsonl). Use `scripts/lookup_actions.py` for copy-ready lists.

## The 300-Action Server Limit

A Zoho MCP server accepts at most 300 selected Actions. Zoho Mail exposes 397, so the whole catalog never fits on one server. Select a profile, not the catalog.

| Profile | Actions | Fits one server |
|---|---|---|
| `mail-reader` | 34 | yes |
| `mail-composer` (extends reader) | 40 | yes |
| `mail-organizer` (extends composer) | 74 | yes |
| `mail-employee` (extends organizer) | 87 | yes |

## Profiles

- `mail-reader`: accounts, folders, labels, list/get mails, headers, HTML, original, threads, attachments, search builders and search, filters (read), signatures (read), vacation reply (read), settings (read).
- `mail-composer`: adds send, reply, forward, save draft, save template, upload compose attachment.
- `mail-organizer`: adds read/unread, spam, flag, labels, move, archive, pin, snooze, undo, trash and restore, folder and label create/update/move, thread actions.
- `mail-employee`: adds own signatures, vacation reply, filters, reminders, compose and view settings. Recommended for an agent with its own mailbox.

## Deliberately excluded

Permanent deletion (`clear mails from trash`, `empty folder`, `clear folder from trash`, `delete account`), mail forwarding rules, Domain, User, Group, Policy, Org Management, Audit Logs, Shared Mailbox, Streams, Tasks, Hotkeys, Permalink. Add per task only with explicit need and the matching Zoho role. Admin Actions work only for users with admin rights in the Zoho Mail organization.

## Task recipes

```bash
python3 scripts/lookup_actions.py --tasks
python3 scripts/lookup_actions.py --task triage-inbox --names-only
```

- `read-and-search`, `reply-to-mail`, `send-new-mail`, `triage-inbox`
