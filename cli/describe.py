# nexus_ai/cli/describe.py

from nexus_ai.plug_in_registry import PluginRegistry

def run_describe(module_name):
    registry = PluginRegistry()

    # Optional: preload plugins if needed
    # You could import bootstrap_plugins from main.py if modularized

    plugin = registry.get(module_name)
    if not plugin:
        print(f"❌ Plugin '{module_name}' not found in registry.")
        return

    if hasattr(plugin, "get_metadata"):
        metadata = plugin.get_metadata()
        print(f"📦 Metadata for '{module_name}':")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
    else:
        print(f"ℹ️ Plugin '{module_name}' does not expose metadata.")