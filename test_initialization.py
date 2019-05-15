import sys
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
from abc import ABC, abstractmethod
import keysightSD1
import time

# Test initialization and configuration.

class Test(ABC):

    # Test class contains base properties and methods that will be present in all sub-classes

    module_dict = {} #dictionary of modules that we will be using the test, with chassis and slot information

    #===================== CORE OBJECT THAT TESTS ACT ON ====================#
    _module_instances = [] # FORMAT: [INSTANCE, MODULE NAME, [CHASSIS SLOT]]
    #========================================================================#

    # init method will fill _module_instances list with SD objects specified by locations in module_dict
    @abstractmethod
    def __init__(self, module_dict):
        super().__init__()
        self.module_dict = module_dict
        for key, value in self.module_dict.items():
            if key[2] == '1':
                sd1_obj = keysightSD1.SD_AIN()
                sd1_obj_id = sd1_obj.openWithSlot("", value[0], value[1])
                if sd1_obj_id < 0:
                    print("[ERROR] Test.__init__: Error opening {}".format(key))
                self._module_instances.append([sd1_obj, key, value])
            elif key[2] == '2':
                sd1_obj = keysightSD1.SD_AOU()
                sd1_obj_id = sd1_obj.openWithSlot("", value[0], value[1])
                if sd1_obj_id < 0:
                    print("[ERROR] Test.__init__: Error opening {}".format(key))
                self._module_instances.append([sd1_obj, key, value])
            else:
                print("[ERROR] Test.__init__: Did not properly parse instrument type string.")

    @abstractmethod
    def _associate(self):
        pass


class Test_HVItriggersync(Test):

    # Dummy attributes
    Amplitude = 1
    wave_id = 1
    prescaler = 0
    start_delay = 0
    cycles = 100

    # Attributes accessible through object initialization
    test_key = "HVItriggersync"
    master_slot = None
    slave_slot = None
    master_index = None #index in HVI sequence (might need this if HVI project is built in simulate mode)
    slave_index = None #index in HVI sequence (might need this if HVI project is built in simulate mode)
    master_channel = None
    slave_channel = None

    # Attributes accessible through class methods
    master_module = keysightSD1.SD_AOU() #assigned with call to associate() method
    slave_module = keysightSD1.SD_AOU() #assigned with call to associate() method
    waveform = keysightSD1.SD_Wave()
    hvi = keysightSD1.SD_HVI()

    def __init__(self, module_dict, master_slot, slave_slot, master_channel, slave_channel, master_index=0, slave_index=1):
        super().__init__(module_dict)
        self.master_slot = master_slot
        self.slave_slot = slave_slot
        self.master_index = master_index
        self.slave_index = slave_index
        self.master_channel = master_channel
        self.slave_channel = slave_channel
        self._associate()

    # This private method associates the master & slave modules (publicly accessible) of this test with the modules
    # created in the base class
    def _associate(self):
        for module in self._module_instances:
            if module[2][1] == self.master_slot:  # if a module was found in master_slot, assign it to master_module
                self.master_module = module[0]
            elif module[2][1] == self.slave_slot:  # if a module was found in slave_slot, assign it to slave_module
                self.slave_module = module[0]
            else:
                print("[ERROR] Associate function: Module found in slot that was not specified as master or slave")

    def send_PXI_trigger_pulse(self, PXI_line_nbr, delay=.2):
        time.sleep(delay)
        self.master_module.PXItriggerWrite(PXI_line_nbr, 0)
        time.sleep(delay)
        self.master_module.PXItriggerWrite(PXI_line_nbr, 1)

    def set_waveform(self, filestr):
        self.waveform.newFromFile(filestr)
        print("Loaded {} into HVI Trigger Sync Test's waveform".format(filestr))

    def set_hvi(self, filestr):
        self.hvi.open(filestr)
        self.hvi.compile()
        self.hvi.load()
        print("Loaded {}.HVI into HVI Trigger Sync Test".format(filestr))

def create_module_inventory(module_array):
    # Takes array of module locations in format [chassis, slot], and returns a dictionary of modules with specific module type & location information

    dictionary = {}

    for mod in module_array:
        temp_mod = keysightSD1.SD_AOU() #Doesn't matter if it's dig or awg, it will be able to retrieve module name
        module_type = temp_mod.getProductNameBySlot(mod[0], mod[1])

        if module_type < 0:
            print("[ERROR] create_module_inventory: Could not find SD instrument at the specified location: Chassis {}, Slot {}".format(mod[0], mod[1]))
            sys.exit()
        else:
            print("Found {} in Chassis {}, Slot {}".format(module_type, mod[0], mod[1]))

        name = "{}_chassis{}_slot{}".format(module_type, mod[0], mod[1])
        dictionary.update({name: [mod[0], mod[1]]})
        temp_mod.close()

    return dictionary