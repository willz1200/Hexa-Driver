from sdk.HexaSDK import *


def test_assert_true():
    return True

def test_connection():
    HEXA_SDK = HexaSDK()
    assert HEXA_SDK.isConnected()
    HEXA_SDK.disconnect()

def test_freqency_responce():
    HEXA_SDK = HexaSDK()
    assert HEXA_SDK.isConnected()
    HEXA_SDK.isEchoCommandsOn = True
    HEXA_SDK.setLinearActuatorWorkspace(0)
    HEXA_SDK.setLinearActuator(0, True)
    HEXA_SDK.setControllerMode(HEXA_SDK.mode.off)
    # HEXA_SDK.frequencyResponce(0.75)
    freqs = [0.1,0.5,0.25,0.75,1.0,1.25,1.5,2.0,2.5,3,4,5,7,10,15,20]
    # freqs = [1.0,1.25,1.5]
    HEXA_SDK.run_multiple_frequency_responces(freqs, "../data_out/")
    HEXA_SDK.disconnect()
    # HEXA_SDK.dump_pickel("../data_out/")

def test_step_responce():
    HEXA_SDK = HexaSDK()
    assert HEXA_SDK.isConnected()
    HEXA_SDK.isEchoCommandsOn = True
    HEXA_SDK.setLinearActuatorWorkspace(0)
    HEXA_SDK.setLinearActuator(0, True)
    HEXA_SDK.setControllerMode(HEXA_SDK.mode.off)
    HEXA_SDK.stepResponce(255)
    HEXA_SDK.disconnect()
    HEXA_SDK.dump_pickel("../data_out/")    
    
    
    