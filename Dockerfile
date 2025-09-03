FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

EXPOSE 8000

WORKDIR /workspace

COPY . /workspace/

ENV UV_PROJECT_ENVIRONMENT=/workspace/.venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN uv sync --locked --no-dev

CMD ["uv", "run", "--with", "fastmcp", "fastmcp", "run", "mcp_tools/main.py", "--transport", "stdio"]
