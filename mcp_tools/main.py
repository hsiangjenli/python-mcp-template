from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from .schemas import NewEndpointRequest, NewEndpointResponse

app = FastAPI(
    title="Python MCP Template",
    description="A template for creating MCP-compliant FastAPI services.",
    version="0.1.0",
)

mcp = FastApiMCP(
    app,
    name="Item API MCP",
    description="MCP server for the Item API",
    describe_full_response_schema=True,
    describe_all_responses=True,
)

mcp.mount()


@app.post(
    "/new/endpoint/", operation_id="new_endpoint", response_model=NewEndpointResponse
)
async def new_endpoint(request: NewEndpointRequest):
    return {"message": f"Hello, {request.name}!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
