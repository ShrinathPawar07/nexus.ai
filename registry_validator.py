from nexus_ai.modules.fintech import FintechModule
from nexus_ai.modules.edtech import EdTechModule
from nexus_ai.modules.healthcare import HealthcareModule
from nexus_ai.modules.automotive import AutomotiveModule
from nexus_ai.modules.it import ItModule

REQUIRED_FIELDS = ["name", "version", "author", "vertical", "description", "capabilities", "tags"]

def validate_metadata(meta):
    missing = [field for field in REQUIRED_FIELDS if field not in meta]
    return missing

def run_registry_validation():
    plugins = [
        FintechModule(),
        EdTechModule(),
        HealthcareModule(),
        AutomotiveModule(),
        ItModule()
    ]

    print("🧪 Registry Metadata Validation")
    print("=" * 60)

    for plugin in plugins:
        try:
            meta = plugin.get_metadata()
            plugin_name = meta.get("name", "Unknown")
            print(f"🔍 Validating {plugin_name}...")

            missing_fields = validate_metadata(meta)
            if missing_fields:
                print(f"❌ Incomplete metadata: Missing {', '.join(missing_fields)}")
            else:
                print(f"✅ {plugin_name} metadata is complete.")

        except Exception as e:
            print(f"❌ Error validating plugin: {e}")

        print("-" * 60)

if __name__ == "__main__":
    run_registry_validation()