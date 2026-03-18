# registry_store.py

PLUGIN_REGISTRY = []

def add_plugin(plugin):
    PLUGIN_REGISTRY.append(plugin)

def get_all_plugins():
    return PLUGIN_REGISTRY

def find_plugins_by_vertical(vertical):
    return [p for p in PLUGIN_REGISTRY if p.get("vertical") == vertical]

def find_plugins_by_capability(cap):
    return [p for p in PLUGIN_REGISTRY if cap in p.get("capabilities", [])]

def find_plugins_by_tag(tag):
    return [p for p in PLUGIN_REGISTRY if tag in p.get("tags", [])]

