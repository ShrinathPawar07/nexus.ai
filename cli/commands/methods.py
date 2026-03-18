"""
Methods command for Nexus.AI Copilot CLI
Lists all callable methods of a specific plugin.
"""

from core.plug_in_registry import PlugInRegistry
from cli.plugin_health import list_plugin_methods


def run(registry, flags):
    """
    Execute the methods command.
    Args:
        registry: PlugInRegistry instance (or dict, will be wrapped).
        flags: list of CLI args (expects plugin name as second arg, e.g. ["methods", "fraud_detector"])
    """
    if len(flags) < 2:
        print("❌ No plugin specified for methods")
        print("Usage: methods <plugin_name>")
        return

    plugin_name = flags[1]

    try:
        # Ensure registry is a PlugInRegistry instance
        if isinstance(registry, dict):
            reg_obj = PlugInRegistry()
            reg_obj.plugins = registry
        else:
            reg_obj = registry

        print(f"\n🔍 Listing methods for plugin '{plugin_name}'...")
        list_plugin_methods(plugin_name, reg_obj)
        print(f"✅ Methods listing for '{plugin_name}' completed")

    except Exception as e:
        print(f"❌ Methods command failed: {e}")