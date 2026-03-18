# plugin_list.py

# Simulated registry store
REGISTERED_PLUGINS = []

def add_plugin_to_registry(plugin):
    REGISTERED_PLUGINS.append(plugin)

def plugin_list_command():
    print("[Registered Plugins]")
    for plugin in REGISTERED_PLUGINS:
        print(f"  - {plugin['name']} ({plugin['vertical']})")