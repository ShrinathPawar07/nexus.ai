# registry.py
# registry_core.py
import json
import os
import copy
from .plugin_schema import validate_plugin
from .compliance_checker import check_compliance
from .lifecycle_runner import run_hook
from cli.plugin_lifecycle import transition_plugin_state
from registry.plugin_register import plugin_registry
from registry.plugin_register import register_plugin_in_memory 

REGISTRY_PATH = "registry_store.json"

def register_plugin(plugin: dict):
    validate_plugin(plugin)

    REGISTRY_PATH = "registry_store.json"


    if not check_compliance(plugin):
        raise ValueError(f"Plugin '{plugin['name']}' does not meet compliance for vertical '{plugin['vertical']}'")

    run_hook(plugin, "pre_register")
    transition_plugin_state(plugin, "registered")  # ✅ Fixed call

    import json

    try:
      with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
      print("⚠️ Registry file is missing or corrupted. Reinitializing...")
      registry = {}
   
    # ✅ Register in-memory
    register_plugin_in_memory(plugin)
    from cli.plugin_health import check_plugin_health
    health = check_plugin_health(plugin["name"])
    plugin["health"] = health  # optional, if you want to embed it

    # Strip unserializable fields before saving

    import copy

    plugin_registry[plugin["name"]] = plugin  # Keep full plugin in memory

   # Strip unserializable fields before saving
    safe_plugin = {}
    for k, v in plugin.items():
      try:
        json.dumps({k: v})  # test serializability
        safe_plugin[k] = v
      except (TypeError, ValueError):
         print(f"⚠️ Skipping unserializable field: {k}")

         pass  # skip unserializable field

    registry[plugin["name"]] = safe_plugin

    with open(REGISTRY_PATH, "w") as f:
     json.dump(registry, f, indent=2)
    run_hook(plugin, "post_register")
    print(f"[Registry] Plugin '{plugin['name']}' registered successfully.")
    print(f"📦 Plugin loaded: {plugin}")

def list_registered_plugins():
    if not os.path.exists(REGISTRY_PATH):
        print("[Registry] No plugins registered yet.")
        return

    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    if not registry:
        print("[Registry] Registry is empty.")
        return

    print("[Registry] Registered Plugins:")
    for name, plugin in registry.items():
        print(f" - {name} ({plugin.get('vertical', 'unknown')})")


# ✅ Explicitly expose registry_store and save_registry_to_disk
registry_store = plugin_registry  # reuse your in-memory store
def save_registry_to_disk(store, path="registry_store.json"):
    import json
    with open(path, "w") as f:
        json.dump(store, f, indent=2)

def run_registry_doctor(registry=None):
    """
    Simple health check for the plugin registry.
    Prints diagnostics about registered plugins.
    """
    print("🩺 Running registry diagnostics...")

    if registry is None:
        registry = plugin_registry

    if not registry or len(registry) == 0:
        print("⚠️ No plugins registered.")
        return False

    print(f"✅ {len(registry)} plugin(s) currently registered:")
    for name, plugin in registry.items():
        vertical = plugin.get("vertical", "unknown") if isinstance(plugin, dict) else "unknown"
        print(f" - {name} (vertical: {vertical})")

    return True

__all__ = ["register_plugin", "list_registered_plugins", "registry_store", "save_registry_to_disk", "run_registry_doctor"]
