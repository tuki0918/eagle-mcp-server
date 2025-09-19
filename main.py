#!/usr/bin/env python3
"""
Eagle MCP Server - Backward compatibility wrapper

This file maintains backward compatibility by importing and running the new FastMCP server.
"""

from server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
