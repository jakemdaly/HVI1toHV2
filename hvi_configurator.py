import sys
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
import keysightSD1

# This is a switch that will route to the correct function to configure a given Test object's HVI sequence
def configure_hvi(Test_obj, filestr):
    if Test_obj.test_key == "HVItriggersync":
        _HVItriggersync_hvi_config(Test_obj, filestr)
    else:
        print("[ERROR] hvi_configurator.configure_HVI: Test object's test_key variable did not match a valid key")

# This is the HVI configurator for the two module HVI trigger sync test
def _HVItriggersync_hvi_config(Test_obj, filestr):
    Test_obj.set_hvi(filestr)