import importlib
import traceback
from typing import Dict, Any, List
#from .health_report import PluginHealthReport  # if you modularized it


from registry.plugin_register import plugin_registry, list_all_plugins
from utils import validate_metadata_schema, check_editable_install

class PluginHealthReport:
    def __init__(self, name: str):
        self.name = name
        self.status = "unknown"
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.metadata: Dict[str, Any] = {}

    def mark_healthy(self):
        self.status = "healthy"

    def mark_broken(self, reason: str):
        self.status = "broken"
        self.errors.append(reason)

    def add_warning(self, warning: str):
        self.warnings.append(warning)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plugin": self.name,
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }

    def to_markdown(self) -> str:
        md = f"### Plugin: `{self.name}`\n- **Status**: {self.status}\n"
        if self.errors:
            md += "\n**Errors:**\n" + "\n".join(f"- ❌ {e}" for e in self.errors)
        if self.warnings:
            md += "\n**Warnings:**\n" + "\n".join(f"- ⚠️ {w}" for w in self.warnings)
        if self.metadata:
            md += "\n**Metadata:**\n" + "\n".join(f"- `{k}`: {v}" for k, v in self.metadata.items())
        return md + "\n"

def assess_plugin_health(plugin_name: str, registry) -> PluginHealthReport:
    report = PluginHealthReport(plugin_name)

    try:
        # Normalize plugin_name if passed as a dict
        if isinstance(plugin_name, dict):
            plugin_name = plugin_name.get("name")

        plugin = registry.get(plugin_name)
        if plugin is None:
            report.mark_broken(f"Plugin '{plugin_name}' not found in registry.")
            return report

        if not hasattr(plugin, "get_metadata"):
            report.mark_broken("Plugin does not implement get_metadata()")
            return report

        metadata = plugin.get_metadata()
        report.metadata = metadata

        if not validate_metadata_schema(metadata):
            report.add_warning("Metadata schema is incomplete or non-compliant.")

        lifecycle = metadata.get("lifecycle") or "active"
        if lifecycle in ["deprecated", "broken"]:
            report.mark_broken(f"Plugin marked as '{lifecycle}' in metadata.")
        else:
            report.mark_healthy()

        module_path = metadata.get("module")
        if not module_path or not isinstance(module_path, str):
           report.mark_broken("Missing or invalid 'module' in plugin metadata.")
           return report

        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            report.mark_broken(f"Import failed: {str(e)}")
            return report

        if not check_editable_install(metadata["module"]):
            report.add_warning("Plugin is not installed in editable mode.")

        health_fn = getattr(module, "health", None)
        if callable(health_fn):
            try:
                health_fn(report)
            except Exception as e:
                report.add_warning(f"Plugin-specific health check failed: {str(e)}")

    except Exception as e:
        report.mark_broken(f"Registry lookup failed: {traceback.format_exc()}")

    return report

def run_health_checks(as_markdown: bool = False) -> List[Any]:
    reports = []
    for plugin_name in list_all_plugins():
        report = assess_plugin_health(plugin_name)
        reports.append(report.to_markdown() if as_markdown else report.to_dict())
    return reports

def check_plugin_health(plugin_name: str, registry) -> Dict[str, Any]:
    report = assess_plugin_health(plugin_name, registry)
    return report.to_dict()

def test_plugin(name: str, fail_fast: bool = False, summary_only: bool = False):
    report = check_plugin_health(name)
    # Add lifecycle hook validation, method introspection, etc.
    return report



def list_plugin_methods(plugin_name=None):
    """
    Return available methods for a plugin.
    If plugin_name is provided, return methods for that plugin only.
    """
    from registry.plugin_register import plugin_registry

    if not plugin_registry:
        print("⚠️ No plugins registered.")
        return []

    if plugin_name:
        plugin = plugin_registry.get(plugin_name)
        if not plugin:
            print(f"⚠️ Plugin '{plugin_name}' not found.")
            return []
        return plugin.get("methods", [])

    # Otherwise, list methods for all plugins
    all_methods = {}
    for name, plugin in plugin_registry.items():
        all_methods[name] = plugin.get("methods", [])
    return all_methods