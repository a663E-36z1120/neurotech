from pylsl import StreamInlet, resolve_byprop
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.fftpack import fft, fftfreq
import numpy as np


LSL_SCAN_TIMEOUT = 5
CHUNK_LENGTH = 1
SAMPLE_SIZE = 500

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


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


def animate(i):

    for i in range(10):
        get_data_step()

    sampling_freq = len(timestamps) / (timestamps[-1] - timestamps[0])

    fourier_list = []
    freq_list = []
    label_list = ["TP9", "AF7", "AF8", "TP10", "Right AUX"]

    for sensor in sensor_list:
        fourier_list.append(fft(sensor))
        freq_list.append(fftfreq(len(sensor), 1 / sampling_freq))

    ax.cla()

    for i in range(len(sensor_list)):
        fourier = fourier_list[i]
        freq = freq_list[i]
        label = label_list[i]
        ax.plot(freq[0:int(np.ceil(len(freq)/2))], np.abs(fourier[0:int(np.ceil(len(fourier)/2))]), label=label)

    ax.set_title("(FFT) Power Spectrum of All Sensors")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")
    ax.legend(loc='upper right')




anim = FuncAnimation(plt.gcf(), animate)

fig.show()
