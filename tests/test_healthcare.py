from nexus_ai.modules.healthcare import HealthCareModule

def test_symptom_diagnosis():
    module = HealthCareModule()
    result = module.process("Check symptom: fever and cough")
    assert "Diagnostic suggestions" in result
