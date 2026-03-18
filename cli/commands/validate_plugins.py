"""
Validate Plugins command for Nexus.AI Copilot CLI
Checks all registered plugins against schema rules and reports validation results.
"""

import json
from core.plug_in_registry import PlugInRegistry
from registry.registry_core import validate_plugin_metadata


def run(registry, flags):
    """
    Execute the validate-plugins command.
    Args:
        registry: PlugInRegistry instance (or dict, will be wrapped).
        flags: list of CLI flags (e.g. ["--json", "--fail-fast"])
    """
    fail_fast = "--fail-fast" in flags
    json_output = "--json" in flags

    try:
        # Ensure registry is a PlugInRegistry instance
        if isinstance(registry, dict):
            reg_obj = PlugInRegistry()
            reg_obj.plugins = registry
        else:
            reg_obj = registry

        plugins = reg_obj.list_plugins()
        if not plugins:
            print("📭 No plugins registered.")
            return

        results = []
        print("\n🧪 Validating all plugins...\n")

        for name in plugins:
            plugin = reg_obj.get(name)
            if not plugin:
                results.append({"plugin": name, "status": "broken", "errors": ["Plugin not found"]})
                if fail_fast:
                    break
                continue

            try:
                metadata = plugin.get_metadata()
                errors, warnings = validate_plugin_metadata(metadata)
                status = "valid" if not errors else "invalid"

                results.append({
                    "plugin": name,
                    "status": status,
                    "errors": errors,
                    "warnings": warnings,
                    "metadata": metadata
                })

                if fail_fast and errors:
                    print(f"❌ Validation failed for '{name}' (fail-fast mode)")
                    break

            except Exception as e:
                results.append({"plugin": name, "status": "broken", "errors": [str(e)]})
                if fail_fast:
                    break

        # Output results
        if json_output:
            print(json.dumps(results, indent=2))
        else:
            for r in results:
                print(f"\n🔍 Plugin: {r['plugin']}")
                print(f"Status: {r['status']}")
                if r.get("errors"):
                    print("Errors:")
                    for e in r["errors"]:
                        print(f"❌ {e}")
                if r.get("warnings"):
                    print("Warnings:")
                    for w in r["warnings"]:
                        print(f"⚠️ {w}")

        print("\n✅ Validation completed")

    except Exception as e:
        print(f"❌ Validate-plugins command failed: {e}")