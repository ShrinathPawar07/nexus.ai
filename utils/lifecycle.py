import os, json, shutil

PLUGIN_DIR = "nexus_ai/plugins"
REGISTRY_PATH = "nexus_ai/registry.json"

def create_plugin(name, force=False):
    plugin_path = os.path.join(PLUGIN_DIR, name)
    metadata_path = os.path.join(plugin_path, "metadata.json")

    if os.path.exists(plugin_path) and not force:
        print(f"⚠️ Plugin '{name}' already exists. Use --force to overwrite.")
        return

    os.makedirs(plugin_path, exist_ok=True)

    metadata = {
        "name": name,
        "vertical": name,
        "validated": False,
        "description": "Describe what this plugin does.",
        "module": f"{name.capitalize()}Module",
        "author": "Shrinath",
        "version": "0.1",
        "tags": []
    }

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    update_registry(name, metadata)
    print(f"✅ Plugin '{name}' scaffolded successfully.")

def delete_plugin(name):
    plugin_path = os.path.join(PLUGIN_DIR, name)
    if not os.path.exists(plugin_path):
        print(f"⚠️ Plugin '{name}' does not exist.")
        return

    shutil.rmtree(plugin_path)
    remove_from_registry(name)
    print(f"🗑️ Plugin '{name}' deleted and deregistered.")

def update_registry(name, metadata):
    registry = {}
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH) as f:
            registry = json.load(f)
    registry[name] = metadata
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)

def remove_from_registry(name):
    if not os.path.exists(REGISTRY_PATH):
        return
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)
    if name in registry:
        del registry[name]
        with open(REGISTRY_PATH, "w") as f:
            json.dump(registry, f, indent=2)