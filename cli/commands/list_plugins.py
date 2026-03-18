"""
List Plugins command for Nexus.AI Copilot CLI
Displays all plugins currently registered in the system, with optional filters and output formats.
"""

import json
from core.plug_in_registry import PlugInRegistry


def run(registry, flags):
    """
    Execute the list-plugins command.
    Args:
        registry: PlugInRegistry instance (or dict, will be wrapped).
        flags: list of CLI flags (e.g. ["--validated-only", "--verbose", "--json", "--vertical=fintech"])
    """
    vertical = None
    validated_only = "--validated-only" in flags
    tag_filter = None
    output_format = "table"
    verbose = "--verbose" in flags
    json_output = "--json" in flags

    # Parse extra flags
    for arg in flags[1:]:
        if arg.startswith("--vertical="):
            vertical = arg.split("=")[1].lower()
        elif arg.startswith("--tag="):
            tag_filter = arg.split("=")[1].lower()
        elif arg.startswith("--format="):
            output_format = arg.split("=")[1].lower()

    try:
        # Ensure registry is a PlugInRegistry instance
        if isinstance(registry, dict):
            reg_obj = PlugInRegistry()
            reg_obj.plugins = registry
        else:
            reg_obj = registry

        plugins = reg_obj.list_plugins()
        if not plugins:
            print("📭 No plugins registered.")
            return

        # JSON output mode
        if json_output:
            output = []
            for name in plugins:
                plugin = reg_obj.get(name)
                try:
                    metadata = plugin.get_metadata()
                    output.append(metadata)
                except Exception as e:
                    output.append({"name": name, "error": str(e)})
            print(json.dumps(output, indent=2))
            return

        # Verbose mode
        if verbose:
            print("\n📦 Verbose Plugin Metadata\n" + "-" * 40)
            for name in plugins:
                plugin = reg_obj.get(name)
                try:
                    metadata = plugin.get_metadata()
                    print(f"\n🔍 {name}")
                    print(json.dumps(metadata, indent=2))
                except Exception as e:
                    print(f"⚠️ Failed to fetch metadata for '{name}': {e}")
            return

        # Default listing with filters
        filtered = []
        for name in plugins:
            plugin = reg_obj.get(name)
            try:
                metadata = plugin.get_metadata()
                if validated_only and not metadata.get("validated", False):
                    continue
                if vertical and metadata.get("vertical", "").lower() != vertical:
                    continue
                if tag_filter and tag_filter not in [t.lower() for t in metadata.get("tags", [])]:
                    continue
                filtered.append(name)
            except Exception as e:
                print(f"⚠️ Failed to fetch metadata for '{name}': {e}")

        print("📋 Registered Plugins:")
        for name in filtered:
            print(f"- {name}")

        print(f"✅ Total plugins: {len(filtered)}")

    except Exception as e:
        print(f"❌ Failed to list plugins: {e}")