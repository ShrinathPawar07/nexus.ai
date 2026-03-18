import pytest
import json
from cli import commands
from core.plug_in_registry import PlugInRegistry


class DummyPlugin:
    def __init__(self, name="dummy", validated=True):
        self._name = name
        self._validated = validated

    def get_metadata(self):
        return {
            "name": self._name,
            "vertical": "fintech",
            "validated": self._validated,
            "description": f"{self._name} plugin for testing",
            "module": f"{self._name}_module",
            "author": "TestAuthor",
            "version": "0.1",
            "tags": ["test"],
        }

    def run(self, input_data):
        return f"[{self._name}] Received query: {input_data}"


@pytest.fixture
def registry():
    reg = PlugInRegistry()
    reg.register("pluginA", DummyPlugin("pluginA", validated=True))
    reg.register("pluginB", DummyPlugin("pluginB", validated=False))
    return reg


def test_doctor_command(capsys, registry):
    commands.doctor(registry, [])
    captured = capsys.readouterr()
    assert "Running registry diagnostics" in captured.out


def test_list_plugins_command(capsys, registry):
    commands.list_plugins(registry, [])
    captured = capsys.readouterr()
    assert "pluginA" in captured.out
    assert "pluginB" in captured.out


def test_describe_command(capsys, registry):
    commands.describe(registry, ["pluginA"])
    captured = capsys.readouterr()
    assert "Plugin Metadata" in captured.out
    assert "pluginA" in captured.out


def test_methods_command(capsys, registry):
    commands.methods(registry, ["pluginA"])
    captured = capsys.readouterr()
    assert "Methods available" in captured.out
    assert "run" in captured.out


def test_run_method_command(capsys, registry):
    flags = ["pluginA", "run", "--args={\"query\": \"hello\"}"]
    commands.run_method(registry, flags)
    captured = capsys.readouterr()
    assert "executed successfully" in captured.out
    assert "Received query" in captured.out


def test_run_all_command(capsys, registry):
    commands.run_all(registry, [])
    captured = capsys.readouterr()
    assert "Running all plugins sequentially" in captured.out
    assert "pluginA" in captured.out


def test_validate_plugins_command(capsys, registry):
    commands.validate_plugins(registry, [])
    captured = capsys.readouterr()
    assert "Validating all plugins" in captured.out
    assert "pluginA" in captured.out


def test_test_harness_command(capsys, registry):
    commands.test_harness(registry, [])
    captured = capsys.readouterr()
    assert "Testing plugin" in captured.out
    assert "pluginA" in captured.out


def test_plugin_init_scaffold_delete(capsys, tmp_path, registry):
    # Simulate plugin init
    plugin_name = "demo"
    flags = ["plugin", "init", plugin_name, "--force"]
    commands.plugin(registry, flags)
    captured = capsys.readouterr()
    assert f"Plugin '{plugin_name}' initialized" in captured.out

    # Simulate scaffold dry-run
    flags = ["plugin", "scaffold", plugin_name, "--dry-run"]
    commands.plugin(registry, flags)
    captured = capsys.readouterr()
    assert "Dry run" in captured.out

    # Simulate delete without confirmation
    flags = ["plugin", "delete", plugin_name]
    commands.plugin(registry, flags)
    captured = capsys.readouterr()
    assert "Use --yes to confirm deletion" in captured.out