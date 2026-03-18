# plugin_status.py

from nexus_core.registry.compliance_checker import check_compliance

def plugin_status_command(plugin):
    status = {
        "name": plugin["name"],
        "vertical": plugin["vertical"],
        "registered": True,  # You can later wire this to actual registry state
        "hooks": list(plugin["lifecycle_hooks"].keys()),
        "compliant": check_compliance(plugin)
    }

    print("[Plugin Status]")
    for key, value in status.items():
        print(f"  {key}: {value}")