# Eagle MCP Server

...

> [!NOTE]
> API docs: http://localhost:8000/docs

## Requirements

- [uv](https://docs.astral.sh/uv/)

## Prerequisites

```
uv sync
```

## Usage

```
uv run main.py
```


## Connecting to the MCP Server using SSE

All the most popular MCP clients (Claude Desktop, Cursor & Windsurf) use the following config format:

```
{
  "mcpServers": {
    "eagle-mcp-server": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

VS Code

```
"mcp": {
    "servers": {
        "eagle-mcp-server": {
            "type": "sse",
            "url": "http://localhost:8000/mcp"
        }
    }
}
```
