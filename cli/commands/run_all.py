"""
Run-All command for Nexus.AI Copilot CLI
Executes all registered plugins sequentially and prints their results.
"""

from core.plug_in_registry import PlugInRegistry


def run(registry, flags):
    """
    Execute the run-all command.
    Args:
        registry: PlugInRegistry instance (or dict, will be wrapped).
        flags: list of CLI flags (currently unused, but can extend later)
    """
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

        print("\n🚀 Running all plugins sequentially...\n")

        for name in plugins:
            plugin = reg_obj.get(name)
            if not plugin:
                print(f"❌ Plugin '{name}' could not be loaded.")
                continue

            print(f"\n🔍 Executing plugin: {name}")
            try:
                # Convention: each plugin should implement a `run(input_data)` method
                result = plugin.run({"query": "test input"})
                print(f"✅ Result from '{name}': {result}")
            except Exception as e:
                print(f"❌ Execution failed for '{name}': {e}")

        print("\n✅ Run-all completed")

    except Exception as e:
        print(f"❌ Run-all command failed: {e}")