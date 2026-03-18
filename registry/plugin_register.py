# plugin_register.py

# registry/plugin_register.py

plugin_registry = {}

def list_all_plugins():
    return list(plugin_registry.keys())

def get_plugin(name: str):
    return plugin_registry.get(name)

def register_plugin_in_memory(plugin: dict):
    plugin_registry[plugin["name"]] = plugin  # ✅ This is the missing function


def plugin_register_command(plugin_path: str):
    import json
    from registry.registry_core import register_plugin

    try:
        with open(plugin_path, "r") as f:
            plugin = json.load(f)
        register_plugin(plugin)
    except Exception as e:
        print(f"❌ Failed to register plugin from '{plugin_path}': {e}")