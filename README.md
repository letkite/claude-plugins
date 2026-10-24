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

Prefer plain MCP configuration instead of a plugin?

```bash
claude mcp add --transport http letkite https://mcp.letkite.com/mcp
```

## License

[MIT](./LICENSE)
