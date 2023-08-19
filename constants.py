# Constants

DEVICE_NAME = "Explore_8443" # The name of the device shown in the bluetooth menu
DEVICE_MODE = 'Explore_8443_ExG' # Used to identify stream of device
SAMPLING_RATE = 1000
WINDOW_SIZE = 500
CHANNEL_MASK = "00000011" # LSB shows channel 1. 1 denotes the active channels 0 for inactive channels. Need a str with 8 characters
NUM_ACTIVE_CHANNELS = 2 # Number of active channels. Do not change for current implementation
COMMAND_FILE_NAME = 'commands.txt'
LOW_CUTOFF = 30
HIGH_CUTOFF = 100
ORDER = 6
THRESHOLD = 50
CONNECTION_PORT = 8005