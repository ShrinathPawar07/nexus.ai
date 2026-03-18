"""
Doctor command for Nexus.AI Copilot CLI
Runs registry diagnostics on all loaded plugins.
"""

from core.plug_in_registry import PlugInRegistry
from registry.registry_core import run_registry_doctor


def run(registry, flags):
    """
    Execute the doctor command.
    Args:
        registry: PlugInRegistry instance (or dict, will be wrapped).
        flags: list of CLI flags (e.g. ["--summary-only", "--fail-fast"])
    """
    fail_fast = "--fail-fast" in flags
    summary_only = "--summary-only" in flags

    try:
        # Ensure registry is a PlugInRegistry instance
        if isinstance(registry, dict):
            reg_obj = PlugInRegistry()
            reg_obj.plugins = registry
        else:
            reg_obj = registry

        run_registry_doctor(reg_obj, fail_fast, summary_only)
        print(f"✅ Registry diagnostics completed. Mode: {'summary' if summary_only else 'detailed'}")

    except Exception as e:
        print(f"❌ Registry doctor failed: {e}")