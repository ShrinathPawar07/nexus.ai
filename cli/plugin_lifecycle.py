# plugin_lifecycle.py

import logging
from cli.plugin_health import check_plugin_health

logger = logging.getLogger(__name__)

# Default no-op fallback
def _noop(plugin_name, hook_name):
    logger.debug(f"No '{hook_name}' hook defined for plugin '{plugin_name}'.")

# Lifecycle hook dispatcher
def invoke_hook(plugin, hook_name):
    hook = getattr(plugin, hook_name, None)
    if callable(hook):
        try:
            logger.info(f"Invoking '{hook_name}' for plugin '{plugin.get('name', 'unknown')}'...")
            hook()
            logger.info(f"'{hook_name}' completed successfully for '{plugin.get('name', 'unknown')}'.")
        except Exception as e:
            logger.error(f"Error during '{hook_name}' for '{plugin.get('name', 'unknown')}': {e}")
    else:
        _noop(plugin.get("name", "unknown"), hook_name)

# Lifecycle entry points
def on_register(plugin):
    invoke_hook(plugin, "on_register")

def on_activate(plugin):
    invoke_hook(plugin, "on_activate")

def on_deactivate(plugin):
    invoke_hook(plugin, "on_deactivate")

def on_uninstall(plugin):
    invoke_hook(plugin, "on_uninstall")

# Unified state transition handler
def transition_plugin_state(plugin, target_state):
    valid_states = ["registered", "active", "inactive", "uninstalled"]
    if target_state not in valid_states:
        raise ValueError(f"Invalid target state: '{target_state}'")

    logger.info(f"Transitioning plugin '{plugin.get('name', 'unknown')}' to state '{target_state}'...")

    if target_state == "registered":
        on_register(plugin)
    elif target_state == "active":
        on_activate(plugin)
    elif target_state == "inactive":
        on_deactivate(plugin)
    elif target_state == "uninstalled":
        on_uninstall(plugin)

    plugin["state"] = target_state
    plugin["health"] = check_plugin_health(plugin)

    logger.info(f"Plugin '{plugin.get('name', 'unknown')}' now in state '{plugin['state']}' with health '{plugin['health']}'.")