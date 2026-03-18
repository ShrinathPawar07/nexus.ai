# nexus_ai/tests/run_plugin_test.py

import importlib
import os

PLUGIN_MODULES = [
    "nexus_ai.modules.fintech_api",
    "nexus_ai.modules.edtech_api",
    "nexus_ai.modules.edtech",
    "nexus_ai.modules.healthcare",
    # Add additional plugin paths here
]

TEST_QUERIES = {
    "fintech_api": "How do I open a business account?",
    "edtech_api": "Can you fetch a quiz on algebra?",
    "edtech": "Create a lesson plan for climate science.",
    "healthcare": "Suggest a diet plan for hypertension."
}

def load_and_test_module(module_path: str, test_query: str):
    try:
        module = importlib.import_module(module_path)
        class_name = [attr for attr in dir(module) if attr.endswith("Module")][0]
        plugin_class = getattr(module, class_name)
        plugin_instance = plugin_class()
        result = plugin_instance.process(test_query, "test_context")
        print(f"✅ [{class_name}] Response: {result}")
    except Exception as e:
        print(f"❌ [{module_path}] Error: {e}")

def main():
    print("🔍 Running plugin registry validation...\n")
    for mod_path in PLUGIN_MODULES:
        key = mod_path.split(".")[-1]
        test_query = TEST_QUERIES.get(key, "Default plugin query")
        load_and_test_module(mod_path, test_query)
    print("\n🧪 Plugin test run complete.")

if __name__ == "__main__":
    main()
