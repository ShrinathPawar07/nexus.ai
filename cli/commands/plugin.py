"""
Plugin command for Nexus.AI Copilot CLI
Supports subcommands: init, scaffold, delete.
"""

import os
import json
from core.plug_in_registry import PlugInRegistry
from nexus_ai.utils.lifecycle import create_plugin, delete_plugin

# Path and overrides should be imported or defined globally
MODULES_PATH = "modules"
CLASS_NAME_OVERRIDES = {}


def run(registry, flags):
    """
    Execute the plugin command.
    Args:
        registry: PlugInRegistry instance (or dict, will be wrapped).
        flags: list of CLI args (expects subcommand like init/scaffold/delete)
    """
    if len(flags) < 2:
        print("❌ No subcommand specified for plugin")
        print("Usage: plugin <init|scaffold|delete> <plugin_name> [options]")
        return

    subcommand = flags[1]

    # --- INIT ---
    if subcommand == "init" and len(flags) >= 3:
        plugin_name = flags[2].lower()
        force = "--force" in flags

        plugin_path = os.path.join(MODULES_PATH, plugin_name)
        os.makedirs(plugin_path, exist_ok=True)

        class_name = CLASS_NAME_OVERRIDES.get(plugin_name, f"{plugin_name.capitalize()}Plugin")
        plugin_file = os.path.join(plugin_path, "plugin.py")

        if os.path.exists(plugin_file) and not force:
            print(f"⚠️ Plugin '{plugin_name}' already exists. Use --force to overwrite.")
        else:
            with open(plugin_file, "w", encoding="utf-8") as f:
                f.write(f'''class {class_name}:
    """{plugin_name.capitalize()} plugin for Nexus_AI."""

    def get_metadata(self):
        """Returns structured metadata for plugin registration, validation, and CLI introspection."""
        return {{
            "name": "{plugin_name}",
            "vertical": "{plugin_name}",
            "validated": False,
            "description": "Describe what this plugin does.",
            "module": "{plugin_name}_module",
            "author": "Shrinath",
            "version": "0.1",
            "tags": []
        }}

    def run(self, input_data: dict):
        """Executes plugin logic based on input query."""
        query = input_data.get("query", "")
        return f"[{class_name}] Received query: '{{query}}'"
''')
            print(f"✅ Plugin '{plugin_name}' initialized at: {plugin_file}")
        return

    # --- SCAFFOLD ---
    if subcommand == "scaffold" and len(flags) >= 3:
        plugin_name = flags[2].lower()
        force = "--force" in flags
        dry_run = "--dry-run" in flags
        confirm = "--yes" in flags

        if dry_run:
            print(f"🧪 Dry run: Would scaffold plugin '{plugin_name}' with force={force}")
            return

        if not confirm:
            print("⚠️ Use --yes to confirm scaffolding.")
            return

        create_plugin(plugin_name, force=force)
        print(f"✅ Plugin '{plugin_name}' scaffolded successfully")
        return

    # --- DELETE ---
    if subcommand == "delete" and len(flags) >= 3:
        plugin_name = flags[2].lower()
        confirm = "--yes" in flags
        if not confirm:
            print("⚠️ Use --yes to confirm deletion.")
            return

        delete_plugin(plugin_name)
        print(f"✅ Plugin '{plugin_name}' deleted successfully")
        return

    print(f"⚠️ Unknown plugin subcommand: {subcommand}")