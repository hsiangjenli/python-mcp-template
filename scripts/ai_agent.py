import asyncio

from langchain_ollama.chat_models import ChatOllama
from mcp_use import MCPAgent, MCPClient


async def main():
    config = {
        "mymcp": {
            "type": "http",
            "url": "http://127.0.0.1:8000/mcp",
        }
    }

    client = MCPClient.from_dict({"mcpServers": config})

    llm = ChatOllama(model="deepseek-r1:7b")
    agent = MCPAgent(llm=llm, client=client)

    result = await agent.run(
        "What is the sum of 5 and 10?",
        max_steps=30,
    )
    print(f"\nResult: {result}")


if __name__ == "__main__":
    asyncio.run(main())
