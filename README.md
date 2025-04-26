# Eagle MCP Server

...

## Requirements

- [uv](https://docs.astral.sh/uv/)

## Prerequisites

Install the required dependencies:

```bash
uv sync
```

## Usage

1. Launch the [Eagle](https://eagle.cool/) app.
2. Launch this MCP server by running the following command:

```bash
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

## Tools

| TODO | Operation ID            | API endpoint (v4.0.0)      | tag         |
|:----:|:------------------------|:---------------------------|:------------|
| [x]  | connect                 | /api/connect               | MCP         |
| [x]  | get_application_info    | /api/application/info      | Application |
| [x]  | create_folder           | /api/folder/create         | Folder      |
| [x]  | rename_folder           | /api/folder/rename         | Folder      |
| [x]  | update_folder           | /api/folder/update         | Folder      |
| [x]  | get_folder_list         | /api/folder/list           | Folder      |
| [x]  | get_folder_list_recent  | /api/folder/listRecent     | Folder      |
| [ ]  | add_item_from_url       | /api/item/addFromURL       | Item        |
| [ ]  | add_items_from_urls     | /api/item/addFromURLs      | Item        |
| [ ]  | add_item_from_path      | /api/item/addFromPath      | Item        |
| [ ]  | add_items_from_paths    | /api/item/addFromPaths     | Item        |
| [ ]  | add_bookmark            | /api/item/addBookmark      | Item        |
| [ ]  | get_item_info           | /api/item/info             | Item        |
| [ ]  | get_item_thumbnail      | /api/item/thumbnail        | Item        |
| [ ]  | get_item_list           | /api/item/list             | Item        |
| [ ]  | move_item_to_trash      | /api/item/moveToTrash      | Item        |
| [ ]  | refresh_item_palette    | /api/item/refreshPalette   | Item        |
| [ ]  | refresh_item_thumbnail  | /api/item/refreshThumbnail | Item        |
| [ ]  | update_item             | /api/item/update           | Item        |
| [ ]  | get_library_info        | /api/library/info          | Library     |
| [ ]  | get_library_history     | /api/library/history       | Library     |
| [ ]  | switch_library          | /api/library/switch        | Library     |
| [ ]  | get_library_icon        | /api/library/icon          | Library     |

> [!NOTE]
> MCP Server API docs: http://localhost:8000/docs

> [!NOTE]
> Official Eagle API docs: https://api.eagle.cool/
