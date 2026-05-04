from scipy.io import wavfile
from scipy.signal import stft
from scipy.ndimage import maximum_filter
import numpy as np
import math

FAN_OUT = 10
MAX_TIME_DELTA = 100
MAX_PEAKS = 1000

def get_freq_band(freq_bin, n_bands=12):
    if freq_bin <= 10:
        return 0
    return min(int(math.log2(freq_bin / 10) * 3), n_bands - 1)

def generate_hashes(filepath):

    sample_rate, signal = wavfile.read(filepath)

    if len(signal.shape) == 2:
        signal = signal.mean(axis=1)

    signal = signal.astype(np.float32) / 32767.0


    f, t, Zxx = stft(signal, fs=sample_rate, nperseg=1024)


    spec = np.abs(Zxx)
    log_spec = np.log1p(spec)
    log_spec = log_spec / (np.max(log_spec) + 1e-6)


    neighborhood_size = (30, 10)
    local_max = maximum_filter(log_spec, size=neighborhood_size) == log_spec
    threshold = np.mean(log_spec) + 0.5 * np.std(log_spec)
    detected_peaks = local_max & (log_spec > threshold)
    freq_idx, time_idx = np.where(detected_peaks)

    # filter low frequency bins
    peaks = [(f, t, v) for f, t, v in zip(freq_idx, time_idx, log_spec[freq_idx, time_idx]) if f > 10]
    peaks = sorted(peaks, key=lambda x: -x[2])
    peaks = peaks[:MAX_PEAKS]


    peaks_by_time = sorted(peaks, key=lambda x: x[1])


    hashes = []
    for i in range(len(peaks_by_time)):
        f1, t1, _ = peaks_by_time[i]
        b1 = get_freq_band(f1)
        pairs_found = 0
        j = i + 1
        while j < len(peaks_by_time) and pairs_found < FAN_OUT:
            f2, t2, _ = peaks_by_time[j]
            b2 = get_freq_band(f2)
            delta_t = t2 - t1
            if delta_t > MAX_TIME_DELTA:
                break
            delta_tq = (delta_t // 3) * 3
            hashes.append(((b1, b2, delta_tq), t1))
            pairs_found += 1
            j += 1

    return hashes