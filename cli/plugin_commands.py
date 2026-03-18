# nexus_ai/cli/plugin_commands.py

from plug_in_registry_legacy import PlugInRegistry
import json

def list_plugins(registry, vertical=None, validated_only=False, tag_filter=None, format="table"):
    plugin_names = registry.list_plugins()
    plugins = []

    for name in plugin_names:
        metadata = registry.describe(name) or {}
        plugin_vertical = metadata.get("vertical", "unspecified").lower()
        validated = metadata.get("validated", False)
        tags = metadata.get("tags", [])

        if vertical and plugin_vertical != vertical:
            continue
        if validated_only and not validated:
            continue
        if tag_filter and tag_filter not in tags:
            continue

        plugins.append({
            "name": name,
            "vertical": plugin_vertical,
            "validated": validated,
            "tags": tags
        })

    if format == "json":
        print(json.dumps(plugins, indent=2))
        return

    if format == "markdown":
        print("| Plugin Name | Vertical | Validated | Tags |")
        print("|-------------|----------|-----------|------|")
        for p in plugins:
            tag_str = ", ".join(p["tags"]) if p["tags"] else "—"
            print(f"| {p['name']} | {p['vertical']} | {'✅' if p['validated'] else '❌'} | {tag_str} |")
        return

    # Default: table format
    print(f"{'Plugin Name':<20} {'Vertical':<15} {'Validated':<10} {'Tags'}")
    print("-" * 70)
    for p in plugins:
        tag_str = ", ".join(p["tags"]) if p["tags"] else "—"
        print(f"{p['name']:<20} {p['vertical']:<15} {'✅' if p['validated'] else '❌':<10} {tag_str}")