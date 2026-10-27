# letkite/claude-plugins

Claude Code plugin marketplace for [LetKite](https://letkite.com): connect
Claude to the machines in your LetKite account over the Model Context
Protocol.

## Plugins

| Plugin | Description |
| --- | --- |
| [letkite](./plugins/letkite) | Reach your machines from Claude: files, terminal, scheduled jobs and more, behind approvals and an audit log. |

## Quick start

```bash
claude plugin marketplace add letkite/claude-plugins
claude plugin install letkite@letkite
```

The plugin adds LetKite's hosted MCP server (`https://mcp.letkite.com/mcp`,
Streamable HTTP). Sign in with your LetKite account in the browser window that
opens on first use; there is no API key. Documentation:
[docs.letkite.com](https://docs.letkite.com/).

The plugin also ships a `letkite` skill that teaches Claude to use the server
safely: survey the fleet before acting, confirm high-risk commands, validate
configuration before reloading.

## Read-only connection

To let Claude look at your machines without changing anything, choose **Read
only** under *Permissions* on LetKite's consent page when you sign in, then
**Approve**. The connection then gets the `fleet.read` scope alone: the server
lists only read-only tools (`list_hosts`, `host_facts`, `read_file`,
`list_dir`, logs, ...), refuses every command, write and transfer, and keeps
credential files out of reach. The plugin is the same either way; the choice
is made per connection at sign-in. To change it later, revoke the connection
in the [console](https://dashboard.letkite.com/) (Connections) and sign in
again.

Prefer plain MCP configuration instead of a plugin?

```bash
claude mcp add --transport http letkite https://mcp.letkite.com/mcp
```

## Checks

`python3 scripts/check_manifests.py` checks every manifest (valid JSON,
names, the MCP URL, skill frontmatter) and CI runs it together with
`claude plugin validate . --strict` on every push and pull request.

## License

[MIT](./LICENSE)
