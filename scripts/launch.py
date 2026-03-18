import argparse
from nexus_ai.core.plug_in_registry import PlugInRegistry


def bootstrap_registry():
    registry = PlugInRegistry()
    registry.discover_modules()
    return registry

def main():
    parser = argparse.ArgumentParser(description="Nexus.AI Vertical Plugin Launcher")
    parser.add_argument("--vertical", type=str, required=True, help="Vertical to route query to (e.g. fintech, edtech)")
    parser.add_argument("--query", type=str, required=True, help="Query to process")

    args = parser.parse_args()
    vertical = args.vertical
    query = args.query

    registry = bootstrap_registry()
    plugin = registry.get_module(vertical)

    if not plugin:
        print(f"[Router] No plugin found for vertical: '{vertical}'")
        return

    print(f"[Router] Context: '{vertical}' | Module: {plugin.__class__.__name__}")
    response = plugin.process(query)
    print(f"🤖 Response ({vertical}): {response}")

if __name__ == "__main__":
    main()

