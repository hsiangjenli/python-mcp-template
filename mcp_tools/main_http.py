from fastapi import FastAPI
from fastmcp import FastMCP

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from mcp_tools.schemas import NewEndpointRequest, NewEndpointResponse

app = FastAPI(
    title="Python MCP Template",
    description="A template for creating MCP-compliant FastAPI services.",
    version="0.1.0",
)


@app.post(
    "/new/endpoint/", operation_id="new_endpoint", response_model=NewEndpointResponse
)
async def new_endpoint(request: NewEndpointRequest):
    return {"message": f"Hello, {request.name}!"}


mcp = FastMCP.from_fastapi(app=app, stateless_http=True, json_response=True)
starlette_app = mcp.http_app(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
)

# starlette_app.mount("/api", app=app)  # (Optional) Keep the original FastAPI app at /api
