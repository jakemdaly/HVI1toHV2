# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:27:14 2019

@author: Administrator
"""

import sys
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
sys.path.append('C:\Python37\Lib\site-packages')
import keysightSD1
import pyhvi
from datetime import timedelta

# Define awg module in chassis
AWG_slot_a = 4
AWG_slot_b = 5
chassis = 1
AWG_a_channel = 1 #Remember to ensure these registers get set
AWG_b_channel = 1
AWG_NAME = 'M3201A'
waveshape = keysightSD1.SD_Waveshapes.AOU_AWG
prescaler = 0
product = ''
ResourceName = "KtHvi"
#user defined constants

#Defining wave with saved file
wave_id = 1
wave = keysightSD1.SD_Wave()
wave.newFromFile('Gaussian.csv')

#initialize AWG
AWG_a = keysightSD1.SD_AOU()
AWG_b = keysightSD1.SD_AOU()
AWG_ID_a = AWG_a.openWithSlot(product,chassis,AWG_slot_a)
AWG_ID_b = AWG_b.openWithSlot(product,chassis,AWG_slot_b)
if AWG_ID_a < 0:
    print("Error opening AWG_a")

error_chanWaveShape = AWG_a.channelWaveShape(AWG_a_channel,waveshape)
AWG_a.waveformFlush() 
AWG_a.AWGflush(AWG_a_channel) #clear waveform from channel

if AWG_ID_b < 0:
    print("Error opening AWG_b")
    
error_chanWaveShape = AWG_b.channelWaveShape(AWG_b_channel,waveshape)
AWG_b.waveformFlush() 
AWG_b.AWGflush(AWG_b_channel) #clear waveform from channel


SD1hvi_a = AWG_a.hvi
SD1hvi_b = AWG_b.hvi
#get engine from SD module's HVI object
engine =
engine_a = SD1hvi_a.engines.master_engine;
engine_b = SD1hvi_b.engines.master_engine;

hvi = pyhvi.KtHvi(ResourceName)


#Add simulateed chassis
hvi.platform.chassis.add_with_options(1, "Simulate=True,DriverSetup=model=M9018B,NoDriver=True")


engineAOU_a = hvi.engines.add(engine_a, "SdEngine1")
engineAOU_b = hvi.engines.add(engine_b, "SdEngine2")


# triggerList = [SD1hvi_a.triggers.front_panel_1,SD1hvi_b.triggers.front_panel_1]

AWG_a_sequence = engineAOU_a.main_sequence
AWG_b_sequence = engineAOU_b.main_sequence

###############################################################################
# STARTS TO GET A LITTLE ROCKY DOWN HERE... 

# I DON"T THINK YOU NEED THE BLOCK BELOW, HENCE IT"S COMMENTED OUT
##Add trigger
#engineAOU_a.triggers.Add(triggerList[triggerIndex], "sequenceTrigger");
#                trigger = engineAOU_a.Triggers["sequenceTrigger"];
#                trigger.Configuration.Direction = Direction.Output;
#                trigger.Configuration.DriveMode = DriveMode.PushPull;
#                trigger.Configuration.Polarity = TriggerPolarity.ActiveLow;
#                trigger.Configuration.Delay = 0;
#                trigger.Configuration.TriggerMode = TriggerMode.Level;
#                trigger.Configuration.PulseLength = 250;

#Below will probably have to change
instruction_a = AWG_a_sequence.programming.add_instruction('TriggerOn', 10, hvi.instructions.instructions_trigger_write.id)    # Add trigger write instruction to the sequence
instruction_a.set_parameter(hvi.instructions.instructions_trigger_write.parameters.trigger, trigger_list[index])       # Specify which trigger is going to be used
instruction_a.set_parameter(hvi.instructions.instructions_trigger_write.parameters.sync_mode, pyhvi.SyncMode.IMMEDIATE)  # Specify synchronization mode
instruction_a.set_parameter(hvi.instructions.instructions_trigger_write.parameters.value, pyhvi.TriggerValue.ON)        # Specify trigger value that is going to be applyed
#trigger b
instruction_b = AWG_b_sequence.programming.add_instruction('TriggerOn', 10, hvi.instructions.instructions_trigger_write.id)    # Add trigger write instruction to the sequence
instruction_b.set_parameter(hvi.instructions.instructions_trigger_write.parameters.trigger, trigger_list[index])       # Specify which trigger is going to be used
instruction_b.set_parameter(hvi.instructions.instructions_trigger_write.parameters.sync_mode, pyhvi.SyncMode.IMMEDIATE)  # Specify synchronization mode
instruction_b.set_parameter(hvi.instructions.instructions_trigger_write.parameters.value, pyhvi.TriggerValue.ON)        # Specify trigger value that is going to be applyed

hvi.programming.add_end('EndOfSequence', 10)  # Add the end statement at the end of the sequence

#Start awg
startDelay = 0
cycles = 0
AWG_a.AWGqueueConfig(AWG_a_channel, keysightSD1.SD_QueueMode.CYCLIC)
AWG_b.AWGqueueConfig(AWG_b_channel, keysightSD1.SD_QueueMode.CYCLIC)
AWG_a.waveformLoad(wave, wave_id)
AWG_b.waveformLoad(wave, wave_id)
AWG_a.AWGqueueWaveform(AWG_a_channel,wave_id,keysightSD1.SD_TriggerModes.SWHVITRIG, startDelay, cycles, prescaler)
AWG_b.AWGqueueWaveform(AWG_b_channel,wave_id,keysightSD1.SD_TriggerModes.SWHVITRIG, startDelay, cycles, prescaler)
AWG_a.AWGstart(AWG_a_channel)
AWG_b.AWGstart(AWG_b_channel)

# Compile the instrument sequence(s)
hvi.compile()       

# Load the instrument sequence(s) to modules and lock resources
hvi.load_to_hw()    

# Execute the instrument sequence(s)
time = timedelta(seconds=1)
hvi.run(time)      

# Release the modules and rsources locked by HVI when calling load_to_hw()
hvi.release_hw()