import sys
import os
import pyhvi

sys.path.append('C:\Program Files (x86)\Keysight\SD1\Libraries\Python')
import keysightSD1
import argparse
from datetime import timedelta

"""HVI Hello World example

Keysight Confidential
Copyright Keysight Technologies 2019

Usage:  python helloworld.py [--simulate]

HelloWorld example compiles and runs an HVI sequence consisting in a turning ON and OFF a sequence_trigger.
First opens an SD1 card (real hardware or simulation mode), creates an HVI module from the card,
gets the SD1 hvi engine and adds it to the HVI Instrument, adds and configures the trigger used by the sequence,
adds the instructions, compiles and runs.

       Module     
        Eng1   
       Seq 0     

     +--------+	
     | Start  |	
     +--------+	
         | 10		
    +----------+	
    |TriggerON |	
    +----------+	
         |  10      
    +-----------+	
    |Trigger OFF|	
    +-----------+	
         |  10      
     +-------+	
     |  End  |	
     +-------+	  
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--simulate', help='Enable hardware simulation', action='store_true')
    return parser.parse_args()


def main():
    # Initialize variables used in 'finally:' block (in case an exception is thrown early)
    hvi = 0
    module = None

    try:
        # Parse the optional --simulate argument
        args = parse_args()
        hardware_simulated = args.simulate

        # Set the options string based on the value of the optional --simulate argument
        options = 'simulate=true' if hardware_simulated else ''

        # Open SD module
        module = keysightSD1.SD_AOU()

        chassis_number = 1
        slot_number = 4
        module_id = module.openWithOptions('M3201A', chassis_number, slot_number, options)
        if module_id < 0:
            raise Exception(
                f'Error opening module in chassis: {chassis_number}, {slot_number}, opened with ID: {module_id}')
        print(f'Module ID {module_id} opened')

        # Create SD_AOUHvi object from SD module
        sd_hvi = module.hvi
        if not sd_hvi:
            raise Exception('Module does not support HVI2')

        # Get engine from SD module's SD_AOUHvi object
        sd_engine_aou = sd_hvi.engines.master_engine

        # Create KtHvi instance
        module_resource_name = 'KtHvi'
        hvi = pyhvi.KtHvi(module_resource_name)

        # Add SD HVI engine to KtHvi instance
        engine = hvi.engines.add(sd_engine_aou, 'SdEngine1')

        # Configure the trigger used by the sequence
        sequence_trigger = engine.triggers.add(sd_hvi.triggers.pxi_5, 'SequenceTrigger')
        sequence_trigger.configuration.direction = pyhvi.Direction.OUTPUT
        sequence_trigger.configuration.drive_mode = pyhvi.DriveMode.PUSH_PULL
        sequence_trigger.configuration.trigger_polarity = pyhvi.TriggerPolarity.ACTIVE_LOW
        sequence_trigger.configuration.delay = 0
        sequence_trigger.configuration.trigger_mode = pyhvi.TriggerMode.LEVEL
        sequence_trigger.configuration.pulse_length = 250

        # *******************************
        # Start KtHvi sequences creation
        sequence = engine.main_sequence  # Obtain main squence from the created HVI instrument

        instruction1 = sequence.programming.add_instruction('TriggerOn', 10,
                                                            hvi.instructions.instructions_trigger_write.id)  # Add trigger write instruction to the sequence
        instruction1.set_parameter(hvi.instructions.instructions_trigger_write.parameters.trigger,
                                   sequence_trigger)  # Specify which trigger is going to be used
        instruction1.set_parameter(hvi.instructions.instructions_trigger_write.parameters.sync_mode,
                                   pyhvi.SyncMode.IMMEDIATE)  # Specify synchronization mode
        instruction1.set_parameter(hvi.instructions.instructions_trigger_write.parameters.value,
                                   pyhvi.TriggerValue.ON)  # Specify trigger value that is going to be applied

        instruction2 = sequence.programming.add_instruction('TriggerOff', 100,
                                                            hvi.instructions.instructions_trigger_write.id)  # Add trigger write instruction to the sequence
        instruction2.set_parameter(hvi.instructions.instructions_trigger_write.parameters.trigger,
                                   sequence_trigger)  # Specify which trigger is going to be used
        instruction2.set_parameter(hvi.instructions.instructions_trigger_write.parameters.sync_mode,
                                   pyhvi.SyncMode.IMMEDIATE)  # Specify synchronization mode
        instruction2.set_parameter(hvi.instructions.instructions_trigger_write.parameters.value,
                                   pyhvi.TriggerValue.OFF)  # Specify trigger value that is going to be applied

        hvi.programming.add_end('EndOfSequence', 10)  # Add the end statement at the end of the sequence

        # Assign triggers to HVI object to be used for HVI-managed synchronization, data sharing, etc
        trigger_resources = [pyhvi.TriggerResourceId.PXI_TRIGGER0, pyhvi.TriggerResourceId.PXI_TRIGGER1]
        hvi.platform.sync_resources = trigger_resources
        hvi.compile()  # Compile the instrument sequence(s)
        hvi.load_to_hw()  # Load the instrument sequence(s) to HW
        time = timedelta(seconds=1)
        hvi.run(time)  # Execute the instrument sequence(s)

    except Exception as ex:
        print(ex)
        print('helloworld.py encountered the error above - exiting')

    finally:
        # Release KtHvi instance from HW (unlock resources)
        if hvi:
            hvi.release_hw()

        # Close module
        if module:
            module.close()


if __name__ == '__main__':
    main()
