from mcp.server.fastmcp import FastMCP
from fastapi.responses import StreamingResponse
import asyncio

# Initialize FastMCP server
mcp = FastMCP("SSE-Demo", host="0.0.0.0", port=8080)


# SSE tool that streams the process of adding numbers
@mcp.tool()
async def add(a: int, b: int):
    """Stream addition process using SSE"""
    async def event_stream():
        yield "data: Starting addition...\n\n"
        await asyncio.sleep(1)
        yield f"data: First number: {a}\n\n"
        await asyncio.sleep(1)
        yield f"data: Second number: {b}\n\n"
        await asyncio.sleep(1)
        result = a + b
        yield f"data: Result: {result}\n\n"
        yield "data: Completed.\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# SSE resource that streams a greeting
@mcp.resource("greeting://{name}")
async def greet(name: str):
    """Stream a greeting message"""
    async def event_stream():
        yield f"data: Preparing greeting...\n\n"
        await asyncio.sleep(1)
        yield f"data: Hello, {name}!\n\n"
        await asyncio.sleep(1)
        yield f"data: Have a great day, {name}!\n\n"
        yield "data: Done.\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# Start the MCP server
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
