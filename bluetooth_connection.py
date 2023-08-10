import explorepy
import pylsl
import numpy as np
import matplotlib.pyplot as plt

explorer = explorepy.Explore()
explorer.connect(device_name="Explore_8443")

# Optional Setup
explorer.set_sampling_rate(sampling_rate=1000)
explorer.set_channels(channel_mask="11111111")

explorer.push2lsl()

# 
buffer = np.empty(1000)
idx = 0
buffer_update_freq = 50 #ms
streams = pylsl.resolve_stream('name', 'Explore_8443_ExyG')
inlet = pylsl.StreamInlet(streams[0])

# Plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(buffer, 'r-') # Returns a tuple of line objects, thus the comma

while True:
    sample, timestamp = inlet.pull_sample()

    buffer[idx] = sample[0]
    idx += 1
    
    if (idx == len(buffer)):
        idx = 999 - buffer_update_freq
        buffer[:idx+1] = buffer[buffer_update_freq:]

        line1.set_ydata(buffer)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.ylim([np.amin(buffer), np.amax(buffer)])