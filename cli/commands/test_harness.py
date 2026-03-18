"""
Test Harness command for Nexus.AI Copilot CLI
Runs plugins inside a controlled test harness for debugging and validation.
"""

import json
from core.plug_in_registry import PlugInRegistry


def run(registry, flags):
    """
    Execute the test-harness command.
    Args:
        registry: PlugInRegistry instance (or dict, will be wrapped).
        flags: list of CLI args (supports --output=, --fail-fast, --summary-only, --vertical=)
    """
    print("🧪 Running plugin test harness...\n")

    required_fields = {"name", "vertical", "validated", "description", "module", "author", "version", "tags"}

    test_queries = {
        "fintech": "detect fraud",
        "edtech": "curriculum mapping",
        "automotive": "vehicle telemetry",
        "healthcare": "patient diagnostics",
        "it": "incident response"
    }

    output_file = None
    fail_fast = False
    summary_only = False
    vertical_filter = None

    # Parse flags
    for arg in flags[1:]:
        if arg.startswith("--output="):
            output_file = arg.split("=", 1)[1]
        elif arg == "--fail-fast":
            fail_fast = True
        elif arg == "--summary-only":
            summary_only = True
        elif arg.startswith("--vertical="):
            vertical_filter = arg.split("=", 1)[1].lower()

    try:
        # Ensure registry is a PlugInRegistry instance
        if isinstance(registry, dict):
            reg_obj = PlugInRegistry()
            reg_obj.plugins = registry
        else:
            reg_obj = registry

        results = []
        all_plugins = reg_obj.list_plugins()
        plugins_to_test = [p for p in all_plugins if vertical_filter is None or p == vertical_filter]

        for name in plugins_to_test:
            plugin = reg_obj.get(name)
            plugin_result = {
                "plugin": name,
                "metadata_ok": False,
                "run_ok": False,
                "errors": [],
                "output": None
            }

            if not summary_only:
                print(f"🔍 Testing plugin: {name}")

            # Metadata validation
            try:
                metadata = plugin.get_metadata()
                missing = required_fields - metadata.keys()
                if missing:
                    msg = f"❌ Metadata missing fields: {', '.join(missing)}"
                    if not summary_only:
                        print(msg)
                    plugin_result["errors"].append(msg)
                    if fail_fast:
                        if not summary_only:
                            print("🛑 Fail-fast enabled. Stopping test harness.")
                        results.append(plugin_result)
                        break
                else:
                    if not summary_only:
                        print("✅ Metadata OK")
                    plugin_result["metadata_ok"] = True
            except Exception as e:
                msg = f"❌ Error in get_metadata(): {e}"
                if not summary_only:
                    print(msg)
                plugin_result["errors"].append(str(e))
                if fail_fast:
                    if not summary_only:
                        print("🛑 Fail-fast enabled. Stopping test harness.")
                    results.append(plugin_result)
                    break
                results.append(plugin_result)
                if not summary_only:
                    print("─" * 60)
                continue

            # Method validation
            try:
                if not hasattr(plugin, "run"):
                    msg = "⚠️ No 'run' method found"
                    if not summary_only:
                        print(msg)
                    plugin_result["errors"].append(msg)
                    if fail_fast:
                        if not summary_only:
                            print("🛑 Fail-fast enabled. Stopping test harness.")
                        results.append(plugin_result)
                        break
                else:
                    query = test_queries.get(name, f"Test query for {name}")
                    output = plugin.run({"query": query})
                    if not summary_only:
                        print(f"✅ run() output: {output}")
                    plugin_result["run_ok"] = True
                    plugin_result["output"] = output
            except Exception as e:
                msg = f"❌ Error in run(): {e}"
                if not summary_only:
                    print(msg)
                plugin_result["errors"].append(str(e))
                if fail_fast:
                    if not summary_only:
                        print("🛑 Fail-fast enabled. Stopping test harness.")
                    results.append(plugin_result)
                    break

            results.append(plugin_result)
            if not summary_only:
                print("─" * 60)

        # Summary-only output
        if summary_only:
            print("\n📊 Plugin Validation Summary")
            print(f"{'Plugin':<12} {'Metadata':<10} {'Run':<10}")
            print("-" * 34)
            for r in results:
                meta = "✅" if r["metadata_ok"] else "❌"
                run = "✅" if r["run_ok"] else "❌"
                print(f"{r['plugin']:<12} {meta:<10} {run:<10}")

        # Save results to file if requested
        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2)
                print(f"\n📁 Results saved to: {output_file}")
            except Exception as e:
                print(f"⚠️ Failed to write output file: {e}")

    except Exception as e:
        print(f"❌ Test-harness command failed: {e}")