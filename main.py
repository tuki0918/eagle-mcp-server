from server import main
import asyncio


def run():
    """Entry point for the MCP server"""
    asyncio.run(main())


if __name__ == "__main__":
    run()
