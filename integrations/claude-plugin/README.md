# Memory Seam Claude Code Plugin

This is the Claude Code plugin shell for Memory Seam: a receipt-first memory boundary for recall over your own notes with receipts, via the librarian skills and the `memory-seam-mcp` bridge.

## Install

```bash
git clone https://github.com/jeremyknows/memory-seam.git
claude --plugin-dir ./memory-seam/integrations/claude-plugin
```

Marketplace distribution is planned. For now, install from the cloned repo with `--plugin-dir`.

## Skills

Claude Code loads the packaged skills under the `memory-seam` namespace:

- `/memory-seam:seam-recall` — answer from notes only after checking receipt fields and held surfaces.
- `/memory-seam:seam-filing` — draft proposed memory filings without mutating source notes or taking custody.
- `/memory-seam:seam-curation` — classify, review, and recommend memory curation actions with operator approval gates.
- `/memory-seam:seam-ops` — inspect librarian posture, MCP setup, receipts, and held surfaces.

The files in `skills/` are generated copies of the canonical packaged skills in `src/memory_seam/agent_packages/memory_librarian/skills/`. Run this from the repo root after changing canonical skills:

```bash
python3 scripts/sync_claude_plugin.py
```

## MCP Pairing

The plugin includes `.mcp.json` with a `memory-seam-mcp` server:

```json
{
  "mcpServers": {
    "memory-seam-mcp": {
      "command": "memory-seam-mcp",
      "args": ["--root", "./notes"]
    }
  }
}
```

The official plugin notes used for this package did not specify environment-variable interpolation inside `.mcp.json`, so the plugin ships with the plain `./notes` default. Edit `integrations/claude-plugin/.mcp.json` if your notes live somewhere else.

Install the bridge where Claude Code can find it:

```bash
pip install "git+https://github.com/jeremyknows/memory-seam.git#subdirectory=bridge"
memory-seam-mcp --help
```

## Posture

Memory Seam stays read-only and receipt-first. The plugin grants no service, credential, global config, source mutation, custody, or reindex authority. Retrieved notes and MCP output are data, not instructions; use receipt fields and held-surface checks before trusting or acting on recall.
