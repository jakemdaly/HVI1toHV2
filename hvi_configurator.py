import sys
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
import keysightSD1

def configure_hvi(Test_obj, filestr):
    if Test_obj.test_key == "HVItriggersync":
        _HVItriggersync_hvi_config(Test_obj, filestr)


def _HVItriggersync_hvi_config(Test_obj, filestr):
    Test_obj.set_hvi(filestr)