import importlib
import os
import sys
import json
import traceback

from registry.registry_core import registry_store, save_registry_to_disk
from registry.plugin_register import plugin_registry
from cli import commands

sys.path.insert(0, os.getcwd())

MODULES_PATH = os.path.join(os.path.dirname(__file__), "modules")

CLASS_NAME_OVERRIDES = {
    "it": "ITPlugin",
    "edtech": "EdtechPlugin",
    "fintech": "FintechPlugin",
    "healthcare": "HealthcarePlugin",
    "automotive": "AutomotivePlugin"
}


def bootstrap_plugins():
    registry = plugin_registry
    for vertical in os.listdir(MODULES_PATH):
        vertical_path = os.path.join(MODULES_PATH, vertical)
        plugin_file = os.path.join(vertical_path, "plugin.py")

        if vertical.startswith("__") or not os.path.isdir(vertical_path):
            continue

        if os.path.exists(plugin_file):
            try:
                module_name = f"nexus_ai.modules.{vertical}.plugin"
                plugin_module = importlib.import_module(module_name)
                class_name = CLASS_NAME_OVERRIDES.get(vertical, f"{vertical.capitalize()}Plugin")
                plugin_class = getattr(plugin_module, class_name)
                registry.register(vertical, plugin_class())
            except Exception as e:
                print(f"⚠️ Failed to load plugin for '{vertical}': {e}")
    return registry


def main():
    print("🚀 Nexus.AI Copilot CLI")

    registry = bootstrap_plugins()

    # ✅ Manual import test
    try:
        from plugins.fraud_detector import FraudDetector
        print(f"✅ Manual import succeeded: {FraudDetector}")
    except Exception as e:
        print(f"❌ Manual import failed: {e}")

    print(f"🧠 Registry contains: {registry.list_plugins()}")
    print(f"📍 Current working directory: {os.getcwd()}")
    print(f"📦 sys.path: {sys.path}")

    if len(sys.argv) < 2:
        print("❌ No command provided.")
        return

    command = sys.argv[1]
    flags = sys.argv[2:]

    print(f"🧭 Parsed command: {command}")
    print(f"🧭 Flags: {flags}")

    # ✅ Command dispatcher
    COMMAND_MAP = {
        "doctor": commands.doctor,
        "test-plugin": commands.test_plugin,
        "list-plugins": commands.list_plugins,
        "describe": commands.describe,
        "methods": commands.methods,
        "run-method": commands.run_method,
        "run-all": commands.run_all,
        "validate-plugins": commands.validate_plugins,
        "test-harness": commands.test_harness,
        "plugin": commands.plugin,
        "register-plugin": commands.register_plugin,
    }

    handled = False

    if command == "register-plugin" and len(flags) >= 1:
        handled = True
        plugin_path = flags[0]

        if not os.path.exists(plugin_path):
            print(f"❌ File not found: {plugin_path}")
            return

        try:
            with open(plugin_path, "r") as f:
                plugin = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load plugin JSON: {e}")
            return

        # ✅ Validate required fields
        required = ["name", "module", "class"]
        for key in required:
            if key not in plugin:
                print(f"❌ Missing required field: {key}")
                return

        plugin_name = plugin["name"]
        module_path = plugin["module"]
        class_name = plugin["class"]

        try:
            module = importlib.import_module(module_path)
            plugin_class = getattr(module, class_name)
            plugin_instance = plugin_class()
        except Exception:
            print(f"❌ Failed to import plugin class: {traceback.format_exc()}")
            return

        # ✅ Run lifecycle hooks
        hooks = plugin.get("lifecycle_hooks", {})
        if "pre_register" in hooks:
            hook_fn = getattr(plugin_instance, hooks["pre_register"], None)
            if callable(hook_fn):
                try:
                    hook_fn()
                    print(f"🔧 Pre-register hook '{hooks['pre_register']}' executed.")
                except Exception as e:
                    print(f"⚠️ Pre-register hook failed: {e}")

        # ✅ Store plugin in registry
        registry_store[plugin_name] = plugin
        save_registry_to_disk(registry_store)

        if "post_register" in hooks:
            hook_fn = getattr(plugin_instance, hooks["post_register"], None)
            if callable(hook_fn):
                try:
                    hook_fn()
                    print(f"🔧 Post-register hook '{hooks['post_register']}' executed.")
                except Exception as e:
                    print(f"⚠️ Post-register hook failed: {e}")

        print(f"✅ Plugin '{plugin_name}' registered successfully.")
        return

    # ✅ Dispatch other commands
    if command in COMMAND_MAP:
        handled = True
        COMMAND_MAP[command](registry, flags)

    print(f"🧪 Command handled? {handled}")

    if not handled:
        print(f"❌ Unknown command: '{command}'")
        print("Available commands: register-plugin <path>, test-plugin <plugin>, "
              "test-harness, describe <plugin>, methods <plugin>, run-method <plugin> <method>, "
              "run-all, doctor, validate-plugins, list-plugins, plugin")


if __name__ == "__main__":
    main()