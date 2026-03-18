# nexus_ai/api/plugin_router.py

from fastapi import APIRouter, Request
from pydantic import BaseModel
import importlib

router = APIRouter()

# Define the input schema
class PluginRequest(BaseModel):
    query: str
    context: str
    plugin: str  # e.g., "fintech_api", "edtech", "healthcare"

@router.post("/plugin/invoke")
async def invoke_plugin(req: PluginRequest):
    try:
        module_path = f"nexus_ai.modules.{req.plugin}"
        plugin_module = importlib.import_module(module_path)
        class_name = [attr for attr in dir(plugin_module) if attr.endswith("Module")][0]
        plugin_class = getattr(plugin_module, class_name)
        plugin_instance = plugin_class()

        result = plugin_instance.process(req.query, req.context)
        return {"plugin": req.plugin, "response": result}

    except Exception as e:
        return {"error": str(e), "plugin": req.plugin}
