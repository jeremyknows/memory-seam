# memory-seam-mcp

`memory-seam-mcp` is a user-started MCP stdio bridge for Memory Seam. Agents consume the seam over MCP; this package imports the Memory Seam core and exposes read-only local markdown envelopes through three tools:

- `memory_seam_health`
- `memory_seam_context(include?: list)`
- `memory_seam_recall(query: str, n?: int)`

The bridge uses `LocalMarkdownAdapter` through `AdapterMemorySeamProvider`, `LocalReadOnlyRuntime`, and `StaticIdentityVerifier`. Tool outputs are the full Memory Seam envelope with receipts and `safe_posture`.

## Install

```bash
pip install "git+https://github.com/jeremyknows/memory-seam.git#subdirectory=bridge"
```

For local development:

```bash
bridge/scripts/verify.sh
```

The bridge package depends on plain `memory-seam`. For in-repo development,
`bridge/scripts/verify.sh` installs the core package from the same checkout
before installing the bridge.

## Claude Code

```json
{
  "mcpServers": {
    "memory-seam": {
      "command": "memory-seam-mcp",
      "args": ["--root", "/path/to/notes"]
    }
  }
}
```

## Claude Desktop

```json
{
  "mcpServers": {
    "memory-seam": {
      "command": "memory-seam-mcp",
      "args": ["--root", "/path/to/notes"]
    }
  }
}
```

## Posture

This is a bridge. It is started by the user through an MCP client over stdio. It binds no socket, runs no daemon, does not auto-start, reads no credentials, and does not mutate global config. The local markdown adapter is read-only, and every context/recall answer includes a metadata read receipt plus safe posture flags.
