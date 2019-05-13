import sys
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
import keysightSD1

# This is a switch that will route the top-level script to the correct function to configure the test's hardware
def configure_hardware(Test_obj):
    if Test_obj.test_key == "HVItriggersync":
        _HVItriggersync_hw_config(Test_obj)
    else:
        print("[ERROR] hardware_configurator.configure_hardware: Test object's test_key variable did not match a valid key")


# This is the hardware configurator for the two module HVI trigger sync test
def _HVItriggersync_hw_config(Test_obj):

#    errors = []

    #Create alternative pointer to master and slave modules for convenience
    awg_m = Test_obj.master_module
    awg_s = Test_obj.slave_module

    #Set up master module
    awg_m.channelWaveShape(Test_obj.master_channel, keysightSD1.SD_Waveshapes.AOU_AWG)
    awg_m.channelAmplitude(Test_obj.master_channel, Test_obj.Amplitude)
    awg_m.waveformLoad(Test_obj.waveform, Test_obj.wave_id)
    awg_m.waveformFlush()
    awg_m.AWGqueueWaveform(Test_obj.master_channel,
                           Test_obj.wave_id,
                           keysightSD1.SD_TriggerModes.SWHVITRIG,
                           Test_obj.start_delay,
                           Test_obj.cycles,
                           Test_obj.prescaler)
    awg_m.AWGqueueConfig(Test_obj.master_channel, keysightSD1.SD_QueueMode.CYCLIC)
    awg_m.AWGstart(Test_obj.master_channel)

    #Set up slave module
    awg_s.channelWaveShape(Test_obj.slave_channel, keysightSD1.SD_Waveshapes.AOU_AWG)
    awg_s.channelAmplitude(Test_obj.slave_channel, Test_obj.Amplitude)
    awg_s.waveformLoad(Test_obj.waveform, Test_obj.wave_id)
    awg_s.waveformFlush()
    awg_s.AWGqueueWaveform(Test_obj.slave_channel,
                           Test_obj.wave_id,
                           keysightSD1.SD_TriggerModes.SWHVITRIG,
                           Test_obj.start_delay,
                           Test_obj.cycles,
                           Test_obj.prescaler)
    awg_s.AWGqueueConfig(Test_obj.slave_channel, keysightSD1.SD_QueueMode.CYCLIC)
    awg_s.AWGstart(Test_obj.slave_channel)

