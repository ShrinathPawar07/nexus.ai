# nexus_ai/scripts/dev_runner.py

from nexus_ai.core.engine import CopilotEngine
from nexus_ai.modules.fintech import FintechModule

def main():
    copilot = CopilotEngine()
    copilot.register_module("fintech", FintechModule())
    
    result = copilot.run_query("fintech", "Analyze recent revenue shift")
    print(result)

if __name__ == "__main__":
    main()
