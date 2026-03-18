# __init__.py
from .plugin_schema import validate_plugin
from .lifecycle_runner import run_hook
from .compliance_checker import check_compliance
from .registry_core import register_plugin, list_registered_plugins
from registry.plugin_register import plugin_registry