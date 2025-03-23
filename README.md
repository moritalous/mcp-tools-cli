# mcp-tools-cli

This is a command-line client for interacting with Model Context Protocol (MCP) servers.

## Usage

```
mcp-tools-cli <action> --mcp-name <mcp_name> [options]
```

### Arguments

*   `action` (required): The action to perform. Must be one of:
    *   `list-tools`: Lists the available tools on the MCP server.
    *   `call-tool`: Calls a specific tool on the MCP server.
*   `--mcp-name` (required): The name of the MCP server to connect to, as defined in `mcp_config.json`.
*   `--tool-name` (required for `call-tool` action): The name of the tool to call.
*   `--tool-args` (optional): Arguments for the tool. Can be a JSON string or a single string value. If a single string value is not a valid JSON, it will be passed as the `query` argument to the tool.
*   `--config-path` (optional): Path to the `mcp_config.json` file. Defaults to `mcp_config.json` in the current directory.

### Configuration

The client uses a configuration file named `mcp_config.json` to store the connection details for MCP servers. The file should be in the following format:

```json
{
  "mcpServers": {
    "<mcp_name>": {
      "command": "<command to run the server>",
      "args": ["<argument1>", "<argument2>", ...],
      "env": {
        "<environment variable name>": "<environment variable value>",
        ...
      }
    },
    ...
  }
}
```

Replace `<mcp_name>` with the name of your MCP server (e.g., `time`). The `command`, `args`, and `env` fields specify how to run the server.

### Examples

> A sample using the [Time MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/time) is provided in mcp_config.sample.json. If you want to use this, please execute `pip install mcp-server-time` beforehand.

1.  List available tools:

```
mcp-tools-cli list-tools --mcp-name time --config-path mcp_config.sample.json
```

2.  Call the `get_current_time` tool with a query:

```
mcp-tools-cli call-tool --mcp-name time --tool-name get_current_time --config-path mcp_config.sample.json
```

### Error Handling

The client will print error messages to the console if any errors occur, such as:

*   FileNotFoundError: If the config file is not found.
*   json.JSONDecodeError: If the config file is not a valid JSON file.
*   ValueError: If the MCP server is not found in the config file, or if the command is missing.
*   argparse.ArgumentError: If there are invalid command-line arguments.
*   Other exceptions during tool execution.
