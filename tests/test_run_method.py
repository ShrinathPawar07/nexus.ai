import pytest
import json
from cli.commands import run_method
from core.plug_in_registry import PlugInRegistry


class DummyPlugin:
    def __init__(self):
        pass

    def get_metadata(self):
        return {"name": "dummy", "validated": True}

    def echo(self, message: str):
        """Echoes back the message."""
        return f"Echo: {message}"

    def add(self, x: int, y: int):
        """Adds two numbers."""
        return x + y


@pytest.fixture
def registry():
    reg = PlugInRegistry()
    reg.register("dummy", DummyPlugin())
    return reg


def test_run_method_describe_mode(capsys, registry):
    flags = ["dummy", "echo", "--describe"]
    run_method.run(registry, flags)
    captured = capsys.readouterr()
    assert "Method: echo" in captured.out
    assert "Docstring" in captured.out


def test_run_method_with_args(capsys, registry):
    flags = ["dummy", "add", "--args={\"x\": 2, \"y\": 3}"]
    run_method.run(registry, flags)
    captured = capsys.readouterr()
    assert "executed successfully" in captured.out
    assert "Result: 5" in captured.out


def test_run_method_missing_args(capsys, registry):
    flags = ["dummy", "add"]
    run_method.run(registry, flags)
    captured = capsys.readouterr()
    assert "Missing required arguments" in captured.out


def test_run_method_invalid_plugin(capsys, registry):
    flags = ["nonexistent", "echo"]
    run_method.run(registry, flags)
    captured = capsys.readouterr()
    assert "Plugin 'nonexistent' not found" in captured.out


def test_run_method_invalid_method(capsys, registry):
    flags = ["dummy", "not_a_method"]
    run_method.run(registry, flags)
    captured = capsys.readouterr()
    assert "Method 'not_a_method' not found" in captured.out