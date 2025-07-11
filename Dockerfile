FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

EXPOSE 8000

WORKDIR /workspace

COPY . /workspace/

RUN uv pip install --system -e .

CMD ["uvicorn", "mcp_tools.main:app"]