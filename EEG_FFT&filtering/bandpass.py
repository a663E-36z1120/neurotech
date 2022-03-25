from pylsl import StreamInlet, resolve_byprop
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from scipy.signal import butter, filtfilt

########################################################################################################################
FREQ_LIST = [8, 11, 14]
Delta = 0.2
########################################################################################################################

LSL_SCAN_TIMEOUT = 5
CHUNK_LENGTH = 1
SAMPLE_SIZE = 10000

FILTER_ORDER = 4



# Initialize LSL stream
streams = resolve_byprop('type', 'EEG', timeout=LSL_SCAN_TIMEOUT)
inlet = StreamInlet(streams[0], max_chunklen=CHUNK_LENGTH)

TP9 = []
AF7 = []
AF8 = []
TP10 = []
Right_AUX = []

sensor_list = [TP9, AF7, AF8, TP10, Right_AUX]
timestamps = []


def get_data_step():
    data, timestamp = inlet.pull_chunk(
        timeout=1.0, max_samples=CHUNK_LENGTH)
    if timestamp:
        # Enqueue sample data
        for i in range(len(sensor_list)):
            sensor_list[i].append(data[-1][i])
            if len(sensor_list[i]) > SAMPLE_SIZE:
                sensor_list[i].pop(0)
        # Enqueue sample timestamp
        timestamps.append(timestamp[-1])
        if len(timestamps) > SAMPLE_SIZE:
            timestamps.pop(0)


fig, ax = plt.subplots(len(FREQ_LIST))


def animate(i):

    for i in range(100):
        get_data_step()

    sampling_freq = len(timestamps) / (timestamps[-1] - timestamps[0])


    for i in range(len(FREQ_LIST)):
        ax[i].cla()
        b, a = butter(FILTER_ORDER, [FREQ_LIST[i]-Delta, FREQ_LIST[i]+Delta], btype='bandpass', output='ba', fs=sampling_freq)

        for sensor in sensor_list:
            filtered = filtfilt(b, a, sensor)
            ax[i].plot(timestamps, filtered)

    plt.setp(ax, ylim=(100, -100))



anim = FuncAnimation(plt.gcf(), animate)

plt.show()
