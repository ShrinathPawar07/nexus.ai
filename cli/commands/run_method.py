"""
Run Method command for Nexus.AI Copilot CLI
Executes or describes a specific method of a plugin.
"""

import json
import inspect
from core.plug_in_registry import PlugInRegistry


def run(registry, flags):
    """
    Execute the run-method command.
    Args:
        registry: PlugInRegistry instance (or dict, will be wrapped).
        flags: list of CLI args (expects plugin name and method name as first two args)
    """
    if len(flags) < 2:
        print("❌ Not enough arguments for run-method")
        print("Usage: run-method <plugin_name> <method_name> [--describe] [--args='{...}']")
        return

    plugin_name = flags[0]
    method_name = flags[1]
    describe_only = "--describe" in flags

    # Extract --args='...' payload
    arg_payload = None
    for arg in flags[2:]:
        if arg.startswith("--args="):
            arg_payload = arg.split("=", 1)[1]

    try:
        # Ensure registry is a PlugInRegistry instance
        if isinstance(registry, dict):
            reg_obj = PlugInRegistry()
            reg_obj.plugins = registry
        else:
            reg_obj = registry

        plugin = reg_obj.get(plugin_name)
        if not plugin:
            print(f"❌ Plugin '{plugin_name}' not found.")
            return

        if not hasattr(plugin, method_name):
            print(f"❌ Method '{method_name}' not found in plugin '{plugin_name}'.")
            return

        method = getattr(plugin, method_name)
        if not callable(method):
            print(f"⚠️ '{method_name}' is not callable.")
            return

        # Describe mode
        if describe_only:
            sig = inspect.signature(method)
            doc = inspect.getdoc(method) or "No docstring provided."
            print(f"\n🧠 Method: {method_name}{sig}")
            print(f"📘 Docstring: {doc}")
            return

        # Execute mode
        try:
            kwargs = json.loads(arg_payload) if arg_payload else {}

            # Default args for fraud detector demo
            if method_name == "detect_fraud" and not arg_payload:
                kwargs = {
                    "transaction": {
                        "id": "TXN12345",
                        "amount": 12000,
                        "location": "offshore"
                    }
                }

            sig = inspect.signature(method)
            missing_args = [
                p.name for p in sig.parameters.values()
                if p.default == inspect.Parameter.empty and p.name not in kwargs
            ]

            if missing_args:
                print(f"⚠️ Missing required arguments: {missing_args}")
                print("💡 You can pass them using --args='{\"arg1\": value, ...}'")
                return

            result = method(**kwargs)
            print(f"\n🚀 Method '{method_name}' executed successfully.")
            print(f"📦 Result: {result}")

        except Exception as e:
            print(f"❌ Execution failed: {e}")

    except Exception as e:
        print(f"❌ Run-method command failed: {e}")