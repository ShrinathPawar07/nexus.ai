import importlib

class PlugInRegistry:
    def __init__(self):
        self.plugins = {}

    def load_plugin_instance(self, plugin_dict):
        module_path = plugin_dict["module"]
        class_name = plugin_dict["class"]

        try:
            plugin_module = importlib.import_module(module_path)
            plugin_class = getattr(plugin_module, class_name)
            return plugin_class()
        except Exception as e:
            print(f"❌ Failed to load plugin '{plugin_dict.get('name', 'unknown')}': {e}")
            return None

    def register(self, plugin_dict):
        instance = self.load_plugin_instance(plugin_dict)
        if instance:
            self.plugins[plugin_dict["name"].lower()] = instance
            print(f"✅ Plugin '{plugin_dict['name']}' registered in memory.")
        else:
            print(f"⚠️ Skipped plugin '{plugin_dict.get('name', 'unknown')}' due to load failure.")

    def get(self, name):
        return self.plugins.get(name.lower())

    def list_plugins(self):
        return list(self.plugins.keys())

    def describe(self, name):
        plugin = self.get(name)
        if plugin and hasattr(plugin, "get_metadata"):
            metadata = plugin.get_metadata()
            print(f"🔍 Metadata for '{name}': {metadata}")
            return metadata
        print(f"⚠️ No metadata found for plugin '{name}'")
        return None

    def discover_modules(self):
        print("🔍 Discovering plugin modules...")
        for name in self.list_plugins():
            print(f" - Found plugin: {name}")