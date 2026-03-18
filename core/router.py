# nexus_ai/core/router.py
import os
import json
import importlib

from plug_in_registry_legacy import PlugInRegistry
from modules.fintech.fintech_module import FintechModule
from modules.edtech import EdtechModule
from modules.healthcare import HealthcareModule
from modules.automotive import AutomotiveModule

class Router:
    def __init__(self, debug: bool = True):
        # Static fallback modules (predefined)
        self.static_modules = {
            "fintech": FintechModule(),
            "edtech": EdtechModule(),
            "healthcare": HealthcareModule(),
            "automotive": AutomotiveModule()
        }

        # Dynamic registry for user-defined or third-party modules
        self.registry = PlugInRegistry()
        self.registry.discover_modules()
        self.debug = debug

    def route_query(self, query: str, context: str) -> str:
        ctx = context.lower()

        # Try dynamic registry first
        module = self.registry.get_module(ctx)

        # Fallback to static modules
        if not module:
            module = self.static_modules.get(ctx)

        if self.debug:
            print(f"[Router] Context: '{ctx}' | Module: {type(module).__name__ if module else 'None'}")

        if module:
            try:
                return module.process(query)
            except Exception as e:
                return f"[Router] Error while processing query in '{ctx}' module: {e}"
        return f"[Router] No module found for context: '{ctx}'"

    def route_command(self, command: str, flags: list):
        print(f"🧭 Parsed command: {command}")
        print(f"🧭 Flags: {flags}")

        if command == "list-plugins":
            from cli.plugin_commands import list_plugins
            list_plugins(self.registry)

        elif command == "describe":
            if not flags:
                print("❌ Missing plugin name.")
                return
            plugin_name = flags[0]
            self.registry.describe(plugin_name)

        elif command == "methods":
            if not flags:
                print("❌ Missing plugin name.")
                return
            plugin_name = flags[0]
            plugin = self.registry.get(plugin_name)
            if plugin:
                print(f"🔧 Methods for '{plugin_name}': {dir(plugin)}")
            else:
                print(f"❌ Plugin '{plugin_name}' not found.")

        elif command == "run-method":
            if len(flags) < 2:
                print("❌ Usage: run-method <plugin> <method>")
                return
            plugin_name, method_name = flags[0], flags[1]
            plugin = self.registry.get(plugin_name)
            if plugin and hasattr(plugin, method_name):
                getattr(plugin, method_name)()
            else:
                print(f"❌ Method '{method_name}' not found in plugin '{plugin_name}'.")

        elif command == "run-all":
            for name in self.registry.list_plugins():
                plugin = self.registry.get(name)
                if hasattr(plugin, "run"):
                    print(f"🚀 Running '{name}'...")
                    plugin.run()

        elif command == "doctor":
            from cli.doctor import run_doctor
            run_doctor(self.registry)

        elif command == "validate-plugins":
            from cli.plugin_commands import validate_plugins
            validate_plugins(self.registry)

        
        elif command == "register-plugin":
            if not flags:
               print("❌ Missing plugin path.")
               return
            plugin_path = flags[0]
            try:
                with open(plugin_path, "r") as f:
                  plugin = json.load(f)
                from registry.registry_core import register_plugin
                register_plugin(plugin)
            except Exception as e:
                print(f"❌ Failed to register plugin: {e}")
            return  # ✅ Prevents fall-through to "Unknown command"


            if not os.path.exists(plugin_path):
                print(f"❌ File not found: {plugin_path}")
                return

            with open(plugin_path, "r") as f:
              plugin = json.load(f)

            print(f"📦 Parsed plugin: {plugin}")  # Add this for debugging

            from registry.registry_core import register_plugin
            register_plugin(plugin)    

        else:
            print(f"❌ Unknown command: '{command}'")
            print("Available commands: test-harness, describe <plugin>, methods <plugin>, run-method <plugin> <method>, run-all, doctor, validate-plugins, list-plugins")
            print("🛑 This should never print if return works")