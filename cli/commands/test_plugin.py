"""
Test Plugin command for Nexus.AI Copilot CLI
Runs health checks on a specific plugin.
"""

from cli.plugin_health import check_plugin_health


def run(registry, flags):
    """
    Execute the test-plugin command.
    Args:
        registry: PlugInRegistry instance
        flags: list of CLI args (expects plugin name as first flag)
    """
    if not flags:
        print("❌ No plugin specified for test-plugin")
        print("Usage: test-plugin <plugin_name> [--summary-only] [--fail-fast]")
        return

    plugin_name = flags[0]
    fail_fast = "--fail-fast" in flags
    summary_only = "--summary-only" in flags

    try:
        report = check_plugin_health(plugin_name, registry)

        if report["status"] == "broken" and "not found" in "".join(report["errors"]).lower():
            print(f"❌ Plugin '{plugin_name}' not found in registry.")
            return

        if summary_only:
            print(f"✅ Plugin '{plugin_name}' status: {report['status']}")
        else:
            print(f"\n🧪 Plugin: {report['plugin']}")
            print(f"Status: {report['status']}")

            if report["errors"]:
                print("\nErrors:")
                for e in report["errors"]:
                    print(f"❌ {e}")

            if report["warnings"]:
                print("\nWarnings:")
                for w in report["warnings"]:
                    print(f"⚠️ {w}")

            if report["metadata"]:
                print("\nMetadata:")
                for k, v in report["metadata"].items():
                    print(f"- {k}: {v}")

        print(f"✅ Plugin '{plugin_name}' health check completed")

    except Exception as e:
        print(f"❌ Plugin '{plugin_name}' health check failed: {e}")