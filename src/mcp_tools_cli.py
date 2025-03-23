import argparse
import asyncio
import json
from contextlib import AsyncExitStack
from typing import Optional

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()  # load environment variables from .env


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(
        self, command: str, args: list, env: dict[str, str] = None
    ):
        """Connect to an MCP server"""

        server_params = StdioServerParameters(command=command, args=args, env=env)

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

    async def list_tools(self):
        result = await self.session.list_tools()
        return result.model_dump_json()

    async def call_tool(self, tool_name: str, tool_args: dict):
        result = await self.session.call_tool(tool_name, tool_args)
        return result.model_dump_json()

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


def load_config(mcp_name: str, config_path: str = "mcp_config.json"):
    """Loads the MCP configuration from the specified JSON file."""
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            mcp_config = config.get("mcpServers", {}).get(mcp_name)
            if not mcp_config:
                raise ValueError(f"MCP server '{mcp_name}' not found in {config_path}")
            return mcp_config
    except FileNotFoundError:
        raise FileNotFoundError(f"{config_path} not found. Please create the file.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"{config_path} is not a valid JSON file.", "", 0)
    except ValueError as e:
        raise e


async def process(
    mcp_name: str,
    action: str,
    tool_name: str = None,
    tool_args=None,
    config_path: str = "mcp_config.json",
):
    """Main function that connects to the MCP server and lists available tools."""
    try:
        config = load_config(mcp_name, config_path)
        command = config.get("command")
        args = config.get("args", [])
        env = config.get("env")
        if not command:
            raise ValueError(
                f"Command not found for MCP server '{mcp_name}' in {config_path}"
            )

        client = MCPClient()
        try:
            await client.connect_to_server(command, args, env)
            if action == "list-tools":
                tools = await client.list_tools()
                print(tools)
            elif action == "call-tool":
                if not tool_name:
                    raise ValueError("tool-name is required for call-tool action")

                if tool_args:
                    try:
                        tool_args = json.loads(tool_args)
                    except json.JSONDecodeError:
                        # If it's not a valid JSON, pass it as a string
                        tool_args = {"query": tool_args}

                    result = await client.call_tool(tool_name, tool_args)
                    print(result)
            else:
                print(f"Error: Invalid action: {action}")
        except Exception as e:
            print(f"Error calling tool: {e}")
        finally:
            await client.cleanup()

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        ValueError,
        argparse.ArgumentError,
    ) as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Connect to an MCP server and list available tools."
    )
    parser.add_argument(
        "action",
        choices=["list-tools", "call-tool"],
        help="Action to perform: list-tools or call-tool",
    )
    parser.add_argument(
        "--mcp-name",
        help="The name of the MCP server to connect to (defined in mcp_config.json)",
        required=True,
    )
    parser.add_argument(
        "--tool-name", help="The name of the tool to call", required=False
    )
    parser.add_argument(
        "--tool-args", help="Arguments for the tool (JSON string or a single string)"
    )
    parser.add_argument(
        "--config-path",
        help="Path to the mcp_config.json file",
        default="mcp_config.json",
    )
    args = parser.parse_args()

    asyncio.run(
        process(
            args.mcp_name, args.action, args.tool_name, args.tool_args, args.config_path
        )
    )


if __name__ == "__main__":
    pass
