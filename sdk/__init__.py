
import os
import glob
import re

cased_path = glob.glob(re.sub(r'([^:])(?=[/\\]|$)', r'[\1]', __file__))[0]
MAIN_SDK_PATH = os.path.abspath(os.path.join(os.path.dirname(cased_path), os.pardir)) + "\\sdk\\"
GUI_UI_FILE_PATH = MAIN_SDK_PATH + "gui.ui"

