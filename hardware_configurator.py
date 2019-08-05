import sys
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
import keysightSD1

# This is a switch that will route the top-level script to the correct function to configure the test's hardware
def configure_hardware(Test_obj):
    if Test_obj.test_key == "HVItriggersync":
        _HVItriggersync_hw_config(Test_obj)
    elif Test_obj.test_key == "HVI external trigger":
        _HVIexternaltrigger(Test_obj)
    elif Test_obj.test_key == "FastBranching":
        _FastBranching_hw_config(Test_obj)
    else:
        print("[ERROR] hardware_configurator.configure_hardware: Test object's test_key variable did not match a valid key")

def _HVIexternaltrigger(Test_obj):

    awg_a = Test_obj.module_a
    awg_b = Test_obj.module_b

    awg_a.channelWaveShape(Test_obj.module_a_channel, keysightSD1.SD_Waveshapes.AOU_AWG)
    awg_b.channelWaveShape(Test_obj.module_b_channel, keysightSD1.SD_Waveshapes.AOU_AWG)
    awg_a.waveformFlush()
    awg_a.AWGflush(Test_obj.module_a_channel)
    awg_b.waveformFlush()
    awg_b.AWGflush(Test_obj.module_b_channel)

    awg_a.waveformLoad(Test_obj.waveform, Test_obj.wave_id)
    awg_b.waveformLoad(Test_obj.waveform, Test_obj.wave_id)

    awg_a.AWGqueueWaveform(Test_obj.module_a_channel,
                           Test_obj.wave_id,
                           keysightSD1.SD_TriggerModes.SWHVITRIG,
                           Test_obj.start_delay,
                           Test_obj.cycles,
                           Test_obj.prescaler)
    awg_b.AWGqueueWaveform(Test_obj.module_b_channel,
                           Test_obj.wave_id,
                           keysightSD1.SD_TriggerModes.SWHVITRIG,
                           Test_obj.start_delay,
                           Test_obj.cycles,
                           Test_obj.prescaler)
    awg_a.AWGqueueConfig(Test_obj.module_a_channel, keysightSD1.SD_QueueMode.CYCLIC)
    awg_b.AWGqueueConfig(Test_obj.module_b_channel, keysightSD1.SD_QueueMode.CYCLIC)
    awg_a.AWGstart(Test_obj.module_a_channel)
    awg_b.AWGstart(Test_obj.module_b_channel)

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

# This is the hardware configurator for the two module HVI trigger sync test
def _FastBranching_hw_config(Test_obj):

    #Create alternative pointer to master and slave modules for convenience
    awg_m = Test_obj.master_module
    awg_s = Test_obj.slave_module

    #Create waveforms
    wave = keysightSD1.SD_Waveshapes.AOU_AWG


    #Set up master module
    awg_m.channelWaveShape(Test_obj.master_channel, wave)
    awg_m.channelAmplitude(Test_obj.master_channel, Test_obj.Amplitude)
    awg_m.waveformFlush()
    awg_m.AWGflush(Test_obj.master_channel)


    error = awg_m.waveformLoad(Test_obj.waveform_array[0], Test_obj.wave_id_array[0])
    if error < 0:
        print("ERROR loading waveform to master module {}".format(error))
    error = awg_m.waveformLoad(Test_obj.waveform_array[1], Test_obj.wave_id_array[1])

    if error < 0:
        print("ERROR loading waveform to master module {}".format(error))
    error = awg_m.waveformLoad(Test_obj.waveform_array[2], Test_obj.wave_id_array[2])
    if error < 0:
        print("ERROR loading waveform to master module {}".format(error))
    error = awg_m.waveformLoad(Test_obj.waveform_array[3], Test_obj.wave_id_array[3])
    if error < 0:
        print("ERROR loading waveform to master module {}".format(error))

    error = awg_m.AWGstart(Test_obj.master_channel)
    if error < 0:
        print("ERROR starting master AWG {}".format(error))

    #Set up slave module
    awg_s.channelWaveShape(Test_obj.slave_channel, keysightSD1.SD_Waveshapes.AOU_AWG)
    awg_s.channelAmplitude(Test_obj.slave_channel, Test_obj.Amplitude)
    awg_s.waveformFlush()
    awg_s.AWGflush(Test_obj.slave_channel)

    error = awg_s.waveformLoad(Test_obj.waveform_array[0], Test_obj.wave_id_array[0])
    if error < 0:
        print("ERROR loading waveform to slave module {}".format(error))
    error = awg_s.waveformLoad(Test_obj.waveform_array[1], Test_obj.wave_id_array[1])
    if error < 0:
        print("ERROR loading waveform to slave module {}".format(error))
    error = awg_s.waveformLoad(Test_obj.waveform_array[2], Test_obj.wave_id_array[2])
    if error < 0:
        print("ERROR loading waveform to slave module {}".format(error))
    error = awg_s.waveformLoad(Test_obj.waveform_array[3], Test_obj.wave_id_array[3])
    if error < 0:
        print("ERROR loading waveform to slave module {}".format(error))

    error = awg_s.AWGstart(Test_obj.slave_channel)
    if error < 0:
        print("ERROR starting slave AWG {}".format(error))