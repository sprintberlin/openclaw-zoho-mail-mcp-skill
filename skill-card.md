## Description: <br>
Connects an agent to Zoho Mail through MCP so it can read, search, write, reply, forward, move, and organize mail in its own mailbox, with least-privilege action profiles and a catalog of all 397 Zoho Mail MCP Actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintcx](https://clawhub.ai/user/sprintcx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to give an agent its own Zoho Mail mailbox via MCP, configure least-privilege action profiles, and read, send, and organize mail through mcporter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ZOHO_MAIL_MCP_URL endpoint is credential-bearing and could expose mailbox access if echoed, logged, or shared. <br>
Mitigation: Treat the MCP URL like a password, avoid printing the full value, and enable only the Actions required for the chosen profile. <br>
Risk: Helper scripts pass the credential-bearing MCP endpoint to mcporter, so local process visibility and logs should be treated carefully. <br>
Mitigation: The scripts call mcporter directly without shell expansion and never print ZOHO_MAIL_MCP_URL intentionally. Run them only on trusted systems. <br>
Risk: Send and delete Actions can send mail or remove data if enabled on the MCP server. <br>
Mitigation: Start with mail-reader. Use mail-composer or mail-employee only for an agent with its own mailbox. Permanent deletion, admin, domain, and policy Actions are excluded from every profile. <br>
Risk: A mailbox contains personal and customer data. <br>
Mitigation: Load only required mails and never copy mail content, addresses, or IDs into chats, logs, or repositories. <br>


## Reference(s): <br>
- [Zoho Mail MCP ClawHub page](https://clawhub.ai/sprintcx/skills/zoho-mail-mcp) <br>
- [GitHub source repository](https://github.com/sprintberlin/openclaw-zoho-mail-mcp-skill) <br>
- [Zoho MCP portal](https://mcp.zoho.eu) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZOHO_MAIL_MCP_URL, a named profile, or a one-off endpoint; bundled helper scripts can print table or JSON output from Zoho Mail MCP calls.] <br>

## Skill Version(s): <br>
1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
