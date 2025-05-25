from fastmcp import MCPServer
from resources.library import LibraryResource
from resources.item import ItemResource
from resources.folder import FolderResource
from resources.application import ApplicationResource
from resources.mcp import MCPResource


def main():
    server = MCPServer(
        name="Eagle MCP Server",
        description="An MCP server for Eagle",
        transport="stdio",  # stdioトランスポートで起動
    )

    server.add_resource(MCPResource())
    server.add_resource(LibraryResource())
    server.add_resource(ItemResource())
    server.add_resource(FolderResource())
    server.add_resource(ApplicationResource())

    server.run()


if __name__ == "__main__":
    main()
