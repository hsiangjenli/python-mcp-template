FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

EXPOSE 8000

WORKDIR /workspace

COPY . /workspace/

RUN uv pip install --system -e .

CMD ["uv", "run", "mcp_tools/demo-streamable-http.py", "--mode", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]