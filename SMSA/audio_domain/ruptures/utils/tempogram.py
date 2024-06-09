import matplotlib.pyplot as plt
import librosa
import numpy as np

import logging as log

from SMSA.utils.prettyMIDI import dur
from config import n_bkps_max, hop_length_tempo

log.basicConfig(level=log.INFO)


def fig_ax(figsize=(15, 5), dpi=150):
    """Return a (matplotlib) figure and ax objects with given size."""
    return plt.subplots(figsize=figsize, dpi=dpi)


def get_sum_of_cost(algo, n_bkps):
    """Return the sum of costs for the change points `bkps`"""
    bkps = algo.predict(n_bkps=n_bkps)
    return algo.cost.sum_of_costs(bkps)


def plot_decision_graph(algo, array_of_n_bkps, path_to_save):
    """
    Строит график, по которому принимается решение о количестве changepoint-ов
    @param algo -- алгоритм
    @param array_of_n_bkps) --
    """
    fig, ax = fig_ax((7, 4))
    ax.plot(
        array_of_n_bkps,
        [get_sum_of_cost(algo=algo, n_bkps=n_bkps) for n_bkps in array_of_n_bkps],
        "-*",
        alpha=0.5,
    )
    ax.set_xticks(array_of_n_bkps)
    ax.set_xlabel("Number of change points")
    ax.set_title("Sum of costs")
    ax.grid(axis="x")
    ax.set_xlim(0, n_bkps_max + 1)
    fig.savefig(path_to_save)
    log.info(f"Elbow decision graph saved to {path_to_save}")


def compute_tempogram(sampling_rate, oenv, hop_length_tempo):
    tempogram = librosa.feature.tempogram(
        onset_envelope=oenv,
        sr=sampling_rate,
        hop_length=hop_length_tempo,
    )
    log.info("Tempogram computed")
    return tempogram


def tempo(filename):
    duration = dur(filename)
    signal, sampling_rate = librosa.load(filename, duration=duration)
    oenv = librosa.onset.onset_strength(y=signal, sr=sampling_rate, hop_length=hop_length_tempo)
    tempogram = compute_tempogram(sampling_rate, oenv, hop_length_tempo)
    return tempogram, sampling_rate


def bkps2sec(bkps, sampling_rate):
    # Convert the estimated change points (frame counts) to actual timestamps
    bkps_times = librosa.frames_to_time(bkps, sr=sampling_rate, hop_length=hop_length_tempo)
    print(bkps_times)
    # Compute change points corresponding indexes in original signal
    bkps_time_indexes = (sampling_rate * bkps_times).astype(int).tolist()
    result = (np.array(bkps_time_indexes) / sampling_rate)
    return result

