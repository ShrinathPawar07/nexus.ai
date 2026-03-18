# plugin_schema.py

def validate_plugin(plugin):
    required_fields = [
        "name", "version", "description", "vertical",
        "entry_point", "capabilities", "lifecycle_hooks"
    ]
    for field in required_fields:
        if field not in plugin:
            raise ValueError(f"Missing required field: {field}")
    if not isinstance(plugin["capabilities"], list):
        raise TypeError("Capabilities must be a list")
    if not isinstance(plugin["lifecycle_hooks"], dict):
        raise TypeError("Lifecycle hooks must be a dictionary")