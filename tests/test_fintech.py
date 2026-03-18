def test_bnpl_risk_detection():
    module = FintechModule()
    response = module.process("Detect risk in BNPL lending")
    assert "Risk detection triggered" in response