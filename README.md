# Eagle MCP Server (Unofficial)

![](.github/docs/cover.png)

A Model Context Protocol (MCP) server for Eagle. [Wiki](https://github.com/tuki0918/eagle-mcp-server/wiki)

<details>

<summary>Supported file formats:</summary>

- `JPG` / `JPEG`
- `PNG`
- `PDF`
- `SVG`
- `MP4`
- `MP3`
- `FBX`
- `OBJ`
- `EPS`
- `TIF` / `TIFF`
- `WebP`
- `BMP`
- `ICO`
- `RAW`
- etc

</details>

- Eagle: https://eagle.cool/<br />
- Eagle API docs: https://api.eagle.cool/<br />

## Requirements

- Python 3.13
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
# To use a different endpoint:
# EAGLE_API_BASE_URL=http://localhost:12345 uv run main.py
```


## Connecting to the MCP Server using Streamable HTTP

Example config:

```
{
  "mcpServers": {
    "eagle-mcp-server": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## Tools

| Supported | Eagle API endpoint | Operation ID | Enabled (default) | Category |
|:----:|:---------------------------|:-------------------------|:----:|:------------|
| ✅ | -               | `connect`                |  | MCP         |
| ✅ | /api/application/info      | `get_application_info`   | ⚫︎ | Application |
| ✅ | /api/folder/create         | `create_folder`          | ⚫︎ | Folder      |
| ✅ | /api/folder/rename         | `rename_folder`          |  | Folder      |
| ✅ | /api/folder/update         | `update_folder`          | ⚫︎ | Folder      |
| ✅ | /api/folder/list           | `get_folder_list`        | ⚫︎ | Folder      |
| ✅ | /api/folder/listRecent     | `get_folder_list_recent` |  | Folder      |
| ✅ | /api/item/addFromURL       | `add_item_from_url`      |  | Item        |
| ✅ | /api/item/addFromURLs      | `add_items_from_urls`    |  | Item        |
| ✅ | /api/item/addFromPath      | `add_item_from_path`     | ⚫︎ | Item        |
| ✅ | /api/item/addFromPaths     | `add_items_from_paths`   |  | Item        |
| ✅ | /api/item/addBookmark      | `add_bookmark`           |  | Item        |
| ✅ | /api/item/info             | `get_item_info`          | ⚫︎ | Item        |
| ✅ | -           | `get_item_source`        | ⚫︎ | Item        |
| ✅ | /api/item/thumbnail        | `get_item_thumbnail`     |  | Item        |
| ✅ | /api/item/list             | `get_item_list`          | ⚫︎ | Item        |
| ✅ | /api/item/moveToTrash      | `move_item_to_trash`     | ⚫︎ | Item        |
| ✅ | /api/item/refreshPalette   | `refresh_item_palette`   |  | Item        |
| ✅ | /api/item/refreshThumbnail | `refresh_item_thumbnail` |  | Item        |
| ✅ | /api/item/update           | `update_item`            | ⚫︎ | Item        |
| ✅ | /api/library/info          | `get_library_info`       | ⚫︎ | Library     |
| ✅ | /api/library/history       | `get_library_history`    |  | Library     |
| ✅ | /api/library/switch        | `switch_library`         |  | Library     |
| ✅ | /api/library/icon          | `get_library_icon`       |  | Library     |

MCP Server API docs: 
- https://tuki0918.github.io/eagle-mcp-server/
- http://localhost:8000/redoc

## Use Cases

### 1) Same Host (Recommended)

```mermaid
flowchart LR

    subgraph 192.168.1.100
        direction LR
        
        subgraph FileSystem [File System]
        end
        subgraph EagleApp [Eagle App<br/>localhost:41595]
        end
        subgraph MCPServer [MCP Server<br/>localhost:8000]
        end
        subgraph MCPClient [MCP Client]
        end
    end

    EagleApp ==> MCPServer e1@==> MCPClient
    MCPClient e2@==> MCPServer ==> EagleApp
    EagleApp ==> FileSystem
    FileSystem ==> EagleApp

    e1@{ animate: true }
    e2@{ animate: true }
```

> [!TIP]
> You have direct access to the filesystem.

### 2) Same Host (Eagle App, MCP Server) + Other Host (MCP Client)

```mermaid
flowchart LR
  
    subgraph 192.168.1.100
        subgraph FileSystem [File System]
        end
        subgraph EagleApp [Eagle App<br/>localhost:41595]
        end
        subgraph MCPServer [MCP Server<br/>localhost:8000]
        end
    end

    subgraph 192.168.1.xxx
        subgraph MCPClient [MCP Client]
        end
    end

    EagleApp ==> MCPServer e1@==> MCPClient
    MCPClient e2@==> MCPServer ==> EagleApp
    EagleApp ==> FileSystem
    FileSystem ==> EagleApp

    e1@{ animate: true }
    e2@{ animate: true }
```

> [!WARNING]
> You don't have access to the filesystem.

### 3) Other Host

```mermaid
flowchart LR

    subgraph 192.168.1.100
        subgraph FileSystem [File System]
        end
        subgraph EagleApp [Eagle App<br/>localhost:41595]
        end
    end

    subgraph 192.168.1.101
        subgraph MCPServer [MCP Server<br/>localhost:8000]
        end
    end

    subgraph 192.168.1.xxx
        subgraph MCPClient [MCP Client]
        end
    end

    EagleApp ==> MCPServer e1@==> MCPClient
    MCPClient e2@==> MCPServer ==> EagleApp
    EagleApp ==> FileSystem
    FileSystem ==> EagleApp

    e1@{ animate: true }
    e2@{ animate: true }
```

> [!WARNING]
> You don't have access to the filesystem.
