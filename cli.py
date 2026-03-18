# cli.py

import sys
import importlib
import pkgutil
from nexus_core.cli_router import handle_cli_command

def list_modules():
    print("📦 Registered Modules")
    print("=" * 60)

    package_path = "nexus_ai.modules"
    try:
        package = importlib.import_module(package_path)
    except ModuleNotFoundError:
        print(f"⚠️ Package '{package_path}' not found.")
        return

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        try:
            full_path = f"{package_path}.{module_name}"
            mod = importlib.import_module(full_path)

            class_name = "".join([part.capitalize() for part in module_name.split("_")]) + "Module"
            cls = getattr(mod, class_name)
            instance = cls()
            metadata = instance.get_metadata()

            print(f"🔹 {metadata.get('name', module_name)}")
            print(f"   Author     : {metadata.get('author', 'Unknown')}")
            print(f"   Vertical   : {metadata.get('vertical', 'N/A')}")
            print(f"   Tags       : {', '.join(metadata.get('tags', []))}")
            print(f"   Description: {metadata.get('description', 'No description')}")
            print("-" * 60)

        except Exception as e:
            print(f"⚠️ Failed to load {module_name}: {e}")
            print("-" * 60)

# Sample plugin for lifecycle testing
sample_plugin = {
    "name": "fin_validator",
    "version": "1.0.0",
    "description": "Validates financial transactions",
    "vertical": "fintech",
    "entry_point": "fin_validator.main",
    "capabilities": ["validate", "encrypt"],
    "tags": ["finance", "security"],
    "lifecycle_hooks": {
        "pre_register": lambda: print("Pre-register hook triggered"),
        "post_register": lambda: print("Post-register hook triggered"),
        "on_unload": lambda: print("Unload hook triggered")
    }
}

def main():
    if len(sys.argv) < 2:
        print("Usage: nexus_cli <command>")
        return

    command = sys.argv[1]

    if command == "list":
        list_modules()

    elif command == "register":
        handle_cli_command("plugin:register", plugin=sample_plugin)

    elif command == "status":
        handle_cli_command("plugin:status", plugin=sample_plugin)

    elif command == "plugin:list":
        handle_cli_command("plugin:list")

    elif command == "plugin:find":
        if len(sys.argv) < 4:
            print("Usage: nexus_cli plugin:find <filter_type> <value>")
        else:
            handle_cli_command("plugin:find", args=sys.argv[2:4])

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()