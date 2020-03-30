from sdk.HexaSDK import *

# def assert_true():
#     return True

def test_led():
    assert True

def test_freqency_responce():
    HEXA_SDK = HexaSDK()
    HEXA_SDK.isEchoCommandsOn = True
    HEXA_SDK.setLinearActuatorWorkspace(0)
    HEXA_SDK.setLinearActuator(0, True)
    HEXA_SDK.setControllerMode(HEXA_SDK.mode.off)
    HEXA_SDK.frequencyResponce(1)