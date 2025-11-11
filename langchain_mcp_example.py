#!/usr/bin/env python3
"""
LangChain MCP Integration Example

This script demonstrates how to integrate a remote MCP server (PIA) with LangChain
using the official langchain-mcp-adapters package.

The example shows:
- Connecting to remote MCP server via streamable_http
- Automatic tool discovery using MultiServerMCPClient
- Support for multiple LLM providers (OpenAI, Azure OpenAI, Claude)
- Creating AI agents with MCP tools using create_agent

Requirements:
- See README.md for environment variable setup
"""

import asyncio
import os
import sys
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import AzureChatOpenAI, ChatOpenAI

# Load environment variables from .env file
load_dotenv()


def create_llm(provider: str = "openai") -> Any:
    """Create an LLM instance based on the provider."""
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,  # Use 0 for more deterministic responses
            openai_api_key=api_key,
        )

    elif provider == "azure":
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

        if not all([api_key, endpoint, deployment]):
            raise ValueError(
                "AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and "
                "AZURE_OPENAI_DEPLOYMENT_NAME are required for Azure"
            )

        return AzureChatOpenAI(
            azure_endpoint=endpoint,
            azure_deployment=deployment,
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            api_key=api_key,
            temperature=0,  # Use 0 for more deterministic responses
        )

    elif provider == "claude":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        return ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            anthropic_api_key=api_key,
            temperature=0,  # Use 0 for more deterministic responses
        )

    else:
        raise ValueError(
            f"Unknown provider: {provider}. Use 'openai', 'azure', or 'claude'"
        )


async def main():
    """Main execution function."""
    # Get configuration from environment
    mcp_url = os.getenv("PIA_MCP_URL", "https://mcp.programintegrity.org")
    mcp_api_key = os.getenv("PIA_API_KEY")
    llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if not mcp_api_key:
        print("❌ Error: PIA_API_KEY environment variable is required")
        print("   Get an API key from: https://mcp.programintegrity.org/register")
        sys.exit(1)

    print("🚀 Starting LangChain MCP Example")
    print(f"   MCP Server: {mcp_url}")
    print(f"   LLM Provider: {llm_provider}")
    print()

    # Initialize MultiServerMCPClient for remote HTTP/SSE MCP server
    print("🔄 Connecting to PIA MCP Server...")
    client = MultiServerMCPClient({
        "pia": {
            "transport": "streamable_http",  # For remote HTTP/SSE servers
            "url": mcp_url,
            "headers": {
                "x-api-key": mcp_api_key
            }
        }
    })
    print("✅ Connected to MCP server")
    print()

    # Get tools from MCP server
    print("🔄 Fetching available tools...")
    tools = await client.get_tools()
    print(f"✅ Retrieved {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool.name}")
    print()

    # Create LLM
    print(f"🔄 Initializing {llm_provider.upper()} LLM...")
    llm = create_llm(llm_provider)
    print("✅ LLM initialized")
    print()

    # Create agent using modern LangChain 1.0 API
    print("🔄 Creating agent with MCP tools...")
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""You are a helpful assistant with access to the Program Integrity Alliance (PIA) database.

IMPORTANT INSTRUCTIONS:
1. You MUST use the available tools to search the database for every query
2. When you receive tool results, READ THE ENTIRE JSON response carefully
3. The tool returns a JSON object with "output" containing "results" and "citations"
4. ALWAYS summarize what you found from the tool results
5. If tool results show documents, describe them to the user
6. Include specific details like titles, agencies, and dates from the results
7. Never say "no results" if the tool returned data with a positive total_count

Use the available tools to search for government audit recommendations, reports, and integrity data."""
    )
    print("✅ Agent created")
    print()

    # Example queries
    queries = [
        "Search for fraud recommendations from GAO",
    ]

    # Use custom query if provided via command line
    if len(sys.argv) > 1:
        custom_query = " ".join(sys.argv[1:])
        print(f"🔍 Running custom query: {custom_query}")
        print()
        queries = [custom_query]
    else:
        print("🔍 Running example query...")
        print("   (You can also pass a custom query as a command-line argument)")
        print()

    # Run queries
    for i, query in enumerate(queries, 1):
        print("=" * 80)
        print()
        print(f"📝 Query {i}: {query}")
        print("-" * 80)
        print()

        try:
            # Invoke agent with the query
            print("🤖 Agent processing query...")
            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]},
                {"configurable": {"thread_id": "1"}}
            )

            # Extract and display the response
            print()
            if "messages" in response:
                messages = response["messages"]
                print(f"📊 Agent executed {len(messages)} steps")
                
                # Show tool calls if any
                for msg in messages:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        print(f"   🔧 Tool calls made: {len(msg.tool_calls)}")
                        for tc in msg.tool_calls:
                            print(f"      - {tc.get('name', 'unknown')}")
                
                # Show final response
                if messages:
                    last_message = messages[-1]
                    content = last_message.content if hasattr(last_message, "content") else str(last_message)
                    print()
                    print("💬 Agent Response:")
                    print(content)
                else:
                    print("💬 Agent Response: (no messages)")
            else:
                print("💬 Agent Response:")
                print(response)

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

        print()

    print("✅ Example complete!")
    print()
    print("💡 Tips:")
    print("   - Pass your own query as a command-line argument")
    print("   - Modify the script to build more complex agent workflows")
    print("   - Check the README.md for more information")


if __name__ == "__main__":
    asyncio.run(main())
