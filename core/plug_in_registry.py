import os
import importlib
import json
import traceback


class PlugInRegistry:
    def __init__(self):
        # Dictionary of plugin_name -> plugin_instance
        self.plugins = {}

    def discover_modules(self):
        """
        Discover and load plugins from the modules folder.
        Expects classes named {name.capitalize()}Module inside nexus_ai/modules/{name}.py
        """
        base_path = "nexus_ai/modules"
        for folder_name in os.listdir(base_path):
            if folder_name.endswith(".py") and not folder_name.startswith("__"):
                module_name = folder_name[:-3]
                print(f"[Registry] Attempting to load: {module_name}")
                try:
                    plugin = self._load_module(module_name)
                    self.plugins[module_name] = plugin
                    print(f"[Registry] Loaded plugin: {module_name}")
                except Exception as e:
                    print(f"[Registry] Failed to load {module_name}: {e}")

    def _load_module(self, name):
        """
        Dynamically import a module and instantiate its plugin class.
        """
        module_path = f"nexus_ai.modules.{name}"
        print(f"[Registry] Importing: {module_path}")
        module = importlib.import_module(module_path)
        class_name = f"{name.capitalize()}Module"
        plugin_class = getattr(module, class_name)
        return plugin_class()

    def get_module(self, name):
        """
        Retrieve a plugin instance by name.
        """
        return self.plugins.get(name)

    def register_plugin_from_json(self, plugin_path: str):
        """
        Register a plugin defined in a JSON file.
        JSON must contain: name, module, class
        """
        if not os.path.exists(plugin_path):
            print(f"❌ File not found: {plugin_path}")
            return False

        try:
            with open(plugin_path, "r") as f:
                plugin = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load plugin JSON: {e}")
            return False

        required = ["name", "module", "class"]
        for key in required:
            if key not in plugin:
                print(f"❌ Missing required field: {key}")
                return False

        plugin_name = plugin["name"]
        module_path = plugin["module"]
        class_name = plugin["class"]

        try:
            module = importlib.import_module(module_path)
            plugin_class = getattr(module, class_name)
            plugin_instance = plugin_class()
        except Exception:
            print(f"❌ Failed to import plugin class: {traceback.format_exc()}")
            return False

        # Store plugin instance
        self.plugins[plugin_name] = plugin_instance
        print(f"✅ Plugin '{plugin_name}' registered successfully.")
        return True
    
    def list_plugins(self):
        """
        Return a list of all registered plugin names.
        """
        return list(self.plugins.keys())

    # Optional: make registry iterable like a dict
    def __iter__(self):
        return iter(self.plugins)

    def __len__(self):
        return len(self.plugins)
