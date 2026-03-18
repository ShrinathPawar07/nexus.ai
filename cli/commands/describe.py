"""
Describe Plugin command for Nexus.AI Copilot CLI
Displays detailed metadata for a specific plugin, with optional flags for JSON, verbose, and method introspection.
"""

import json
import inspect
from core.plug_in_registry import PlugInRegistry


def run(registry, flags):
    """
    Execute the describe command.
    Args:
        registry: PlugInRegistry instance (or dict, will be wrapped).
        flags: list of CLI args (expects plugin name as second arg, e.g. ["describe", "fraud_detector"])
    """
    if len(flags) < 2:
        print("❌ No plugin specified for describe")
        print("Usage: describe <plugin_name> [--json] [--verbose] [--methods]")
        return

    plugin_name = flags[1]
    verbose = "--verbose" in flags
    json_output = "--json" in flags
    show_methods = "--methods" in flags

    try:
        # Ensure registry is a PlugInRegistry instance
        if isinstance(registry, dict):
            reg_obj = PlugInRegistry()
            reg_obj.plugins = registry
        else:
            reg_obj = registry

        plugin = reg_obj.get(plugin_name)
        if not plugin:
            print(f"❌ Plugin '{plugin_name}' not found.")
            return

        # Metadata output
        try:
            metadata = plugin.get_metadata()
            if json_output:
                print(json.dumps(metadata, indent=2))
            else:
                print(f"\n📦 Plugin Metadata for '{plugin_name}':")
                for k, v in metadata.items():
                    print(f"  {k}: {v}")
        except Exception as e:
            print(f"⚠️ Failed to fetch metadata: {e}")
            return

        # Methods introspection
        if show_methods:
            print(f"\n🔍 Methods in '{plugin_name}':")
            for attr in dir(plugin):
                if attr.startswith("_"):
                    continue
                method = getattr(plugin, attr)
                if callable(method):
                    try:
                        sig = inspect.signature(method)
                        doc = inspect.getdoc(method) or "No docstring provided."
                        print(f"• {attr}{sig}: {doc}")
                    except Exception as e:
                        print(f"⚠️ Could not introspect '{attr}': {e}")

        print(f"✅ Plugin '{plugin_name}' description completed")

    except Exception as e:
        print(f"❌ Describe command failed: {e}")