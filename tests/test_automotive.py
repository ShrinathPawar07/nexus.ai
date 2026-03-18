from nexus_ai.modules.automotive import AutomotiveModule

def test_sensor_analysis():
    module = AutomotiveModule()
    result = module.process("Analyze sensor data from engine")
    assert "Sensor data insights" in result
