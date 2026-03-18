# cli_router.py

from nexus_core.cli.plugin_register import plugin_register_command
from nexus_core.cli.plugin_status import plugin_status_command
from nexus_core.cli.plugin_list import plugin_list_command, add_plugin_to_registry
from nexus_core.cli.plugin_find import plugin_find_command

def handle_cli_command(command, plugin=None, args=None):
    if command == "plugin:register":
        plugin_register_command(plugin)
        add_plugin_to_registry(plugin)

    elif command == "plugin:status":
        plugin_status_command(plugin)

    elif command == "plugin:list":
        plugin_list_command()

    elif command == "plugin:find":
        if args and len(args) == 2:
            filter_type, value = args
            plugin_find_command(filter_type, value)
        else:
            print("Usage: plugin:find <filter_type> <value>")

    else:
        print(f"[CLI] Unknown command: {command}")