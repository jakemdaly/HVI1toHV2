import sys
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
from hardware_configurator import *
from test_initialization import *
from hvi_configurator import *
import time

# Top level module which configures and runs sub-parts:
# triggerExample.py
#   1. test_initialization.py (Test initialization)
#   2. hardware_configurator.py (Hardware configuration)
#   3. hvi_configurator (HVI configuration)


# Choose which test to run. In this example we will run a trigger example in a single chassis with two modules
# Tell the test the location of the modules that you want to open (chassis number and slot number)

# Create dictionary from the array and hand this to the test initializer.
module_array = [[1, 4], [1, 5]]
module_dict = create_module_inventory(module_array)

# Set up the HVI trigger sync test
HVItriggersync_test = Test_HVItriggersync(module_dict, #dictionary of modules used in the test
                                          4, #master slot
                                          5, #slave slot
                                          1, #master channel
                                          1) #slave channel
HVItriggersync_test.set_waveform("C:\\Users\\Public\\Documents\\Keysight\\SD1\\Examples\\Waveforms\\Sin_10MHz_50samples_192cycles.csv")

# Configure the hardware for this test
configure_hardware(HVItriggersync_test)

# Load the HVI
configure_hvi(HVItriggersync_test, "TriggeringExample_modulesX2_V1_0.HVI")
HVItriggersync_test.hvi.start()

# Send the trigger
while(True):
    HVItriggersync_test.send_PXI_trigger_pulse(0)
    time.sleep(.3)