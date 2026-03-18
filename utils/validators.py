import importlib.util
import os
from typing import Dict

def validate_metadata_schema(metadata: Dict) -> bool:
    required_fields = ["name", "vertical", "lifecycle", "module"]
    missing = [field for field in required_fields if field not in metadata]
    return len(missing) == 0

def check_editable_install(module_name: str) -> bool:
    try:
        spec = importlib.util.find_spec(module_name)
        if not spec or not spec.origin:
            return False

        # Check if module is installed in editable mode (i.e., from source)
        return "site-packages" not in spec.origin and os.path.isdir(os.path.dirname(spec.origin))
    except Exception:
        return False