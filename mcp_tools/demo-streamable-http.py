from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("strava", stateless_http=True, host="0.0.0.0", port=8000)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


app = FastAPI(title="Strava", lifespan=lambda app: mcp.session_manager.run())
app.mount("/strava", mcp.streamable_http_app())

if __name__ == "__main__":
    import json

    mcp.run(transport="streamable-http")
