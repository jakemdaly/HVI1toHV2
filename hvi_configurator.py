import sys
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
import keysightSD1
import pyhvi

# This is a switch that will route to the correct function to configure a given Test object's HVI sequence
def configure_hvi(Test_obj, filestr):
    if Test_obj.test_key == "HVItriggersync":
        _HVItriggersync_hvi_config(Test_obj, filestr)
    elif Test_obj.test_key == "HVI external trigger":
        _HVIexternaltrigger_hvi_config(Test_obj, filestr)
    elif Test_obj.test_key == "FastBranching":
        _FastBranching_hvi_config(Test_obj, filestr)
    else:
        print("[ERROR] hvi_configurator.configure_HVI: Test object's test_key variable did not match a valid key")

# This is the HVI configurator for the two module HVI trigger sync test
def _HVItriggersync_hvi_config(Test_obj, filestr):
    Test_obj.set_hvi(filestr)

def _HVIexternaltrigger_hvi_config(Test_obj, filestr):
    Test_obj.set_hvi(filestr)

def _FastBranching_hvi_config(Test_obj, filestr):
    Test_obj.set_hvi(filestr)

# def FastBranching_hvi2_config(Test_obj):
#
#     # Create the two HVI engines from the two SD1 modules
#     master_SD1hvi = Test_obj.master_module.hvi
#     slave_SD1hvi = Test_obj.slave_module.hvi
#
#     sd_wait_trigger = master_SD1hvi.triggers.
#
#
#     #
#
