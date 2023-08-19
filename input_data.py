import threading
import explorepy
import pylsl
import numpy as np
import matplotlib.pyplot as plt

from direction_classifier import DirectionClassifier
from filters import Filter
import constants

def write_file():
    lock = threading.Lock()
    explorer = explorepy.Explore()
    explorer.connect(device_name=constants.DEVICE_NAME)

    # Optional Setup
    explorer.set_sampling_rate(sampling_rate=constants.SAMPLING_RATE)
    explorer.set_channels(channel_mask=constants.CHANNEL_MASK)

    explorer.push2lsl()

    # Getting the time window
    buffer = np.empty((constants.WINDOW_SIZE, constants.NUM_ACTIVE_CHANNELS + 1))
    idx = 0
    buffer_update_freq = 50 #ms
    streams = pylsl.resolve_stream('name', constants.DEVICE_MODE)

    # Assign individual stream to channel
    inlet = pylsl.StreamInlet(streams[0])

    # Create figure for raw data
    plt.ion() # Interactive mode on
    fig,(ax1, ax2) = plt.subplots(1,2,figsize=(10,5))
    line1, = ax1.plot(buffer[:,0],buffer[:,1],color='red')
    ax1.set_ylabel('Readings')
    ax1.set_xlabel('Time')
    ax1.set_title('Channel 1 filtered recording')

    line2, = ax2.plot(buffer[:,0],buffer[:,2],color='orange')
    ax2.set_ylabel('Readings')
    ax2.set_xlabel('Time')
    ax2.set_title('Channel 2 filtered recording')

    while True:
        sample, timestamp = inlet.pull_sample()
        buffer[idx,0] = timestamp
        for i in range(constants.NUM_ACTIVE_CHANNELS):
            buffer[idx,i+1] = sample[i]
        idx += 1
        if (idx == constants.WINDOW_SIZE):
            idx = 0

            filtered_output = np.empty((constants.WINDOW_SIZE, constants.NUM_ACTIVE_CHANNELS))
            filtered_output[:,0] = Filter(buffer[:,1]).butter_bandpass(constants.LOW_CUTOFF, constants.HIGH_CUTOFF, constants.SAMPLING_RATE, constants.ORDER)
            filtered_output[:,1] = Filter(buffer[:,2]).butter_bandpass(constants.LOW_CUTOFF, constants.HIGH_CUTOFF, constants.SAMPLING_RATE, constants.ORDER)
            buffer[:,1:3] = filtered_output
            line1.set_xdata(buffer[:,0])
            line1.set_ydata(buffer[:,1])
            line2.set_xdata(buffer[:,0])
            line2.set_ydata(buffer[:,2])

            ax1.relim()
            ax1.autoscale_view()

            ax2.relim()
            ax2.autoscale_view()

            # energy_calculator = EnergyOperator(buffer, constants.WINDOW_SIZE)
            # energy_calculator.apply_tke()
            # output_matrix = energy_calculator.get_output_matrix()

            game_controller = DirectionClassifier(filtered_output, constants.THRESHOLD)
            command = game_controller.create_commands()
            with lock:
                with open(constants.COMMAND_FILE_NAME,"w") as file:
                    file.write(f"{command}\n")
                    print("Written: ", command)
            plt.pause(0.01)


writer_thread = threading.Thread(target=write_file)
writer_thread.start()