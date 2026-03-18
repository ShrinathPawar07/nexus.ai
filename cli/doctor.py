# nexus_ai/cli/doctor.py

from plug_in_registry_legacy import PlugInRegistry

def run_doctor():
    print("🩺 Running Nexus.AI system diagnostics...\n")

    registry = PluginRegistry()
    plugins = registry.list_plugins()

    if not plugins:
        print("❌ No plugins registered. Check your bootstrap flow.")
    else:
        print(f"✅ {len(plugins)} plugins registered:")
        for name in plugins:
            print(f"  - {name}")

    print("\n📦 Registry health check complete.")