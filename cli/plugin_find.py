# plugin_find.py

from nexus_core.registry.registry_store import (
    find_plugins_by_vertical,
    find_plugins_by_capability,
    find_plugins_by_tag
)

def plugin_find_command(filter_type, value):
    if filter_type == "vertical":
        plugins = find_plugins_by_vertical(value)
    elif filter_type == "capability":
        plugins = find_plugins_by_capability(value)
    elif filter_type == "tag":
        plugins = find_plugins_by_tag(value)
    else:
        print(f"[Find] Unknown filter type: {filter_type}")
        return

    print(f"[Find] Plugins matching {filter_type} = '{value}':")
    for plugin in plugins:
        print(f"  - {plugin['name']} ({plugin['vertical']})")