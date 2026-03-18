import pytest
import json
from cli.commands import list_plugins
from core.plug_in_registry import PlugInRegistry


class DummyPlugin:
    def __init__(self, name, vertical="fintech", validated=True, tags=None):
        self._name = name
        self._vertical = vertical
        self._validated = validated
        self._tags = tags or ["default"]

    def get_metadata(self):
        return {
            "name": self._name,
            "vertical": self._vertical,
            "validated": self._validated,
            "description": f"{self._name} plugin for testing",
            "module": f"{self._name}_module",
            "author": "TestAuthor",
            "version": "0.1",
            "tags": self._tags,
        }

    def run(self, input_data):
        return f"Ran {self._name} with {input_data}"


@pytest.fixture
def registry():
    reg = PlugInRegistry()
    reg.register("pluginA", DummyPlugin("pluginA", vertical="fintech", validated=True))
    reg.register("pluginB", DummyPlugin("pluginB", vertical="edtech", validated=False))
    return reg


def test_list_plugins_default(capsys, registry):
    flags = []
    list_plugins.run(registry, flags)
    captured = capsys.readouterr()
    assert "pluginA" in captured.out
    assert "pluginB" in captured.out


def test_list_plugins_validated_only(capsys, registry):
    flags = ["--validated-only"]
    list_plugins.run(registry, flags)
    captured = capsys.readouterr()
    assert "pluginA" in captured.out
    assert "pluginB" not in captured.out


def test_list_plugins_json_output(capsys, registry):
    flags = ["--json"]
    list_plugins.run(registry, flags)
    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert isinstance(output, list)
    assert any(p["name"] == "pluginA" for p in output)
    assert any(p["name"] == "pluginB" for p in output)


def test_list_plugins_with_vertical_filter(capsys, registry):
    flags = ["--vertical=fintech"]
    list_plugins.run(registry, flags)
    captured = capsys.readouterr()
    assert "pluginA" in captured.out
    assert "pluginB" not in captured.out