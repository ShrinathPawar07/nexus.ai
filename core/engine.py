# nexus_ai/core/engine.py

class CopilotEngine:
    def __init__(self, modules=None):
        self.modules = modules or {}
    
    def register_module(self, name: str, handler):
        self.modules[name] = handler

    def run_query(self, module_name: str, query: str):
        if module_name in self.modules:
            return self.modules[module_name].process(query)
        raise ValueError(f"Module '{module_name}' not found")
