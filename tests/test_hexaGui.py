from sdk.HexaGUI import *

def test_sometest():
    assert True

def test_GUI():
    if QtGui.QApplication.instance() is None:
        app = QtGui.QApplication(sys.argv)

    ObjHexaGUI = HexaGUI() # Instantiate the Hexa GUI object
    exitCode = ObjHexaGUI.guiMainLoop() # Enter the GUI event loop
    sys.exit(exitCode) # Exit with given code