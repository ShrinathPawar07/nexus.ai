import os
import importlib
import traceback

def to_pascal_case(s):
    return ''.join(word.capitalize() for word in s.replace('-', '_').split('_'))

def validate_plugins():
    modules_path = os.path.join(os.path.dirname(__file__), "..", "modules")
    modules_path = os.path.abspath(modules_path)

    print("🔍 Validating plugins in:", modules_path)
    print("─" * 60)

    total = 0
    failures = 0

    for vertical in os.listdir(modules_path):
        vertical_path = os.path.join(modules_path, vertical)
        plugin_file = os.path.join(vertical_path, "plugin.py")

        if not os.path.isdir(vertical_path):
            continue

        total += 1
        vertical_display = vertical.capitalize()
        class_name = f"{to_pascal_case(vertical)}Plugin"

        if not os.path.exists(plugin_file):
            print(f"❌ {vertical_display}: Missing plugin.py")
            failures += 1
            continue

        try:
            module_name = f"nexus_ai.modules.{vertical}.plugin"
            plugin_module = importlib.import_module(module_name)

            if not hasattr(plugin_module, class_name):
                print(f"⚠️  {vertical_display}: plugin.py missing class '{class_name}'")
                failures += 1
                continue

            plugin_class = getattr(plugin_module, class_name)
            instance = plugin_class()
            if not hasattr(instance, "run"):
                print(f"⚠️  {vertical_display}: '{class_name}' missing 'run()' method")
                failures += 1
                continue

            print(f"✅ {vertical_display}: Plugin loaded successfully")

        except Exception as e:
            print(f"❌ {vertical_display}: Error loading plugin")
            print("   ↪", str(e))
            failures += 1

    print("─" * 60)
    print(f"Summary: {total} verticals scanned, {failures} issues found")