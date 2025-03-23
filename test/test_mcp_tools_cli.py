import argparse

from src.mcp_tools_cli import main


def test_main_valid_arguments(monkeypatch, capsys):
    monkeypatch.setattr(
        "argparse.ArgumentParser.parse_args",
        lambda _: argparse.Namespace(
            action="list-tools",
            mcp_name="time",
            tool_name=None,
            tool_args=None,
            config_path="test/mcp_config.valid.json",
        ),
    )
    main()
    captured = capsys.readouterr()
    assert "Error" not in captured.out


def test_main_invalid_action(monkeypatch, capsys):
    monkeypatch.setattr(
        "argparse.ArgumentParser.parse_args",
        lambda _: argparse.Namespace(
            action="invalid-action",
            mcp_name="test_mcp",
            tool_name=None,
            tool_args=None,
            config_path="test/mcp_config.valid.json",
        ),
    )
    main()
    captured = capsys.readouterr()
    assert (
        "Error: MCP server 'test_mcp' not found in test/mcp_config.valid.json"
        in captured.out
    )


def test_main_invalid_mcp_name(monkeypatch, capsys):
    monkeypatch.setattr(
        "argparse.ArgumentParser.parse_args",
        lambda _: argparse.Namespace(
            action="list-tools",
            mcp_name="invalid_mcp",
            tool_name=None,
            tool_args=None,
            config_path="test/mcp_config.valid.json",
        ),
    )
    main()
    captured = capsys.readouterr()
    assert (
        "Error: MCP server 'invalid_mcp' not found in test/mcp_config.valid.json"
        in captured.out
    )


def test_main_invalid_config_path(monkeypatch, capsys):
    monkeypatch.setattr(
        "argparse.ArgumentParser.parse_args",
        lambda _: argparse.Namespace(
            action="list-tools",
            mcp_name="test_mcp",
            tool_name=None,
            tool_args=None,
            config_path="invalid_config.json",
        ),
    )
    main()
    captured = capsys.readouterr()
    assert (
        "Error: invalid_config.json not found. Please create the file." in captured.out
    )
