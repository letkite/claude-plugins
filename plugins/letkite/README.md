# LetKite plugin for Claude Code

[LetKite](https://letkite.com) connects AI clients to the machines in your
account over the [Model Context Protocol](https://modelcontextprotocol.io/):
files, a terminal, scheduled jobs, sharing and more, behind per-connection
permissions, approvals by a person and an audit log.

The plugin adds LetKite's hosted MCP server to Claude Code:

- URL: `https://mcp.letkite.com/mcp` (Streamable HTTP)
- Authentication: OAuth. On first use Claude Code opens a browser window to
  sign in to LetKite and approve what the connection may do. There is no API
  key to copy.

You need a LetKite account with at least one machine connected; check both in
the [console](https://dashboard.letkite.com/). Documentation:
[docs.letkite.com](https://docs.letkite.com/).

## Install

Add this marketplace, then install the plugin:

```bash
claude plugin marketplace add letkite/claude-plugins
claude plugin install letkite@letkite
```

Or add the server without the plugin:

```bash
claude mcp add --transport http letkite https://mcp.letkite.com/mcp
```

## License

MIT, see [LICENSE](../LICENSE).
