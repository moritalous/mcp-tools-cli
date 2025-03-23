# mcp-tools-cli

これは、Model Context Protocol（MCP）サーバーと対話するためのコマンドラインクライアントです。

## インストール

`mcp-tools-cli`はpipを使用してインストールできます。

```
pip install mcp-tools-cli
```

## 設定

クライアントは、MCPサーバーの接続詳細を保存するために`mcp_config.json`という名前の設定ファイルを使用します。次の内容で`mcp_config.json`というファイルを作成してください。

```json
{
  "mcpServers": {
    "time": {
      "command": "python",
      "args": ["-m", "mcp_server_time", "--local-timezone=America/New_York"]
    }
  }
}
```

値を自分のMCPサーバー構成に置き換えてください。


## 使い方

```
mcp-tools-cli <action> --mcp-name <mcp_name> [options]
```

### 引数

*   `action` (必須): 実行するアクション。次のいずれかである必要があります。
    *   `list-tools`: MCPサーバーで利用可能なツールを一覧表示します。
    *   `call-tool`: MCPサーバー上の特定のツールを呼び出します。
*   `--mcp-name` (必須): 接続するMCPサーバーの名前。`mcp_config.json`で定義されている必要があります。
*   `--tool-name` (`call-tool`アクションの場合に必須): 呼び出すツールの名前。
*   `--tool-args` (オプション): ツールの引数。JSON形式の文字列、または単一の文字列を指定できます。単一の文字列が有効なJSONでない場合、ツールの`query`引数として渡されます。
*   `--config-path` (オプション): `mcp_config.json`ファイルへのパス。デフォルトは現在のディレクトリの`mcp_config.json`です。

### 設定

クライアントは、MCPサーバーの接続詳細を保存するために`mcp_config.json`という名前の設定ファイルを使用します。ファイルは次の形式である必要があります。

```json
{
  "mcpServers": {
    "<mcp_name>": {
      "command": "<サーバーを実行するコマンド>",
      "args": ["<引数1>", "<引数2>", ...],
      "env": {
        "<環境変数名>": "<環境変数値>",
        ...
      }
    },
    ...
  }
}
```

`<mcp_name>`をMCPサーバーの名前に置き換えます（例：`time`）。`command`、`args`、および`env`フィールドは、サーバーの実行方法を指定します。

### 例

> `mcp_config.sample.json`には、[Time MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/time)の使用例が記載されています。これを使用する場合は、事前に`pip install mcp-server-time`を実行してください。

1.  利用可能なツールの一覧を表示する:

```
mcp-tools-cli list-tools --mcp-name time --config-path mcp_config.sample.json
```

2.  `get_current_time`ツールをクエリとともに呼び出す:

```
mcp-tools-cli call-tool --mcp-name time --tool-name get_current_time --config-path mcp_config.sample.json
```

### エラー処理

クライアントは、次のエラーが発生した場合、コンソールにエラーメッセージを出力します。

*   FileNotFoundError: 設定ファイルが見つからない場合。
*   json.JSONDecodeError: 設定ファイルが有効なJSONファイルではない場合。
*   ValueError: MCPサーバーが設定ファイルに見つからない場合、またはコマンドが欠落している場合。
*   argparse.ArgumentError: 無効なコマンドライン引数がある場合。
*   ツールの実行中にその他の例外が発生した場合。
