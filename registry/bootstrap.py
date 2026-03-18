import json
import os
import importlib
from core.plug_in_registry import PlugInRegistry   # ✅ import your registry class

REGISTRY_PATH = "registry_store.json"

def bootstrap_plugins() -> PlugInRegistry:
    registry = PlugInRegistry()   # ✅ create a registry object

    if not os.path.exists(REGISTRY_PATH):
        print("⚠️ No registry file found.")
        return registry

    try:
        with open(REGISTRY_PATH, "r") as f:
            plugins = json.load(f)
            print(f"📂 Raw plugin registry:\n{json.dumps(plugins, indent=2)}")
            print(f"📂 Loaded {len(plugins)} plugins from registry_store.json")
    except json.JSONDecodeError:
        print("❌ Failed to parse registry file.")
        return registry

    for name, plugin in plugins.items():
        print(f"🔍 Attempting to load plugin: {name}")
        print(f"   ↪ module: {plugin['module']}, class: {plugin['class']}")
        try:
            module_path = plugin["module"]
            class_name = plugin["class"]
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            instance = cls()
            registry.plugins[name] = instance   # ✅ store in registry.plugins
            print(f"✅ Loaded plugin: {name}")
        except Exception as e:
            print(f"❌ Failed to load plugin '{name}': {e}")

    return registry   # ✅ returns PlugInRegistry, not dict