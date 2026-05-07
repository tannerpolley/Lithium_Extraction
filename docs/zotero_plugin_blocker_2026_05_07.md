# Zotero Plugin Blocker

Date: 2026-05-07

## Blocked Task

The requested deeper Lithium Recovery literature review must use the `@zotero-local-research` plugin. The user explicitly instructed to stop if that plugin does not work, so the review was not continued through the Zotero HTTP API, direct SQLite index access, local PDF search, or web fallback.

## Current Failure

Both tested Codex MCP plugin tools fail with the same transport error:

```text
tool call failed for `zotero-local/zotero_index_status`
Caused by:
    Transport closed
```

```text
tool call failed for `zotero-local/zotero_list_collections`
Caused by:
    Transport closed
```

## Checks Completed

- Zotero desktop process is running.
- Zotero local HTTP API responds with status `200` at `http://localhost:23119/api`.
- Direct MCP launcher smoke test succeeds:

```powershell
& 'C:\ProgramData\miniconda3\python.exe' -m zotero_local_mcp.launch --help
```

- Direct local index check succeeds from the plugin package:

```text
items_indexed=278
attachments_indexed=318
chunks_indexed=10030
embeddings_indexed=9540
```

- Four stale `python.exe -m zotero_local_mcp.launch` processes were found and stopped with the plugin-provided cleanup script:

```powershell
& 'C:\Users\Tanner\.codex\plugins\cache\zotero\zotero-local-research\0.1.1\scripts\stop-zotero-mcp-processes.ps1' -MinAgeMinutes 5 -Force
```

- After cleanup, no `zotero_local_mcp` processes remained, but Codex plugin calls still returned `Transport closed`.
- Codex app logs did not show an actionable Python/server traceback for this failure.

## Interpretation

The failure appears to be in the Codex app MCP/plugin transport for `zotero-local`, not in Zotero desktop, the Zotero local API, the plugin Python package, or the local retrieval index.

## Next Required Action

Reconnect/restart the `@zotero-local-research` plugin transport in Codex, then retry:

```text
zotero_index_status
zotero_list_collections
zotero_find_collections(query="Lithium Recovery")
```

Only after one of the plugin tools succeeds should the deeper library review, candidate-solvent expansion, and article-analysis revalidation continue under the user's stated constraint.
