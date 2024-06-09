import logging
import os
import logging as log
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from scipy.spatial import distance
from scipy import signal
from pathlib import Path

from musicaiz.features import get_novelty_func, get_segment_boundaries
from musicaiz.loaders import Musa

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
matplotlib.use('agg')

log.basicConfig(level=logging.INFO)

# DIRECTORY_FOR_SSM = "figures-produced-by-figure-ssm/"
DIRECTORY_FOR_SSM = "app/static/Image"
dataset = "BPS_FH_Dataset"


def get_ioi(notes):
    iois = []
    for i, next in zip(notes, notes[1:]):
        iois.append(next.start_sec - i.start_sec)
    return iois


def get_pitches(notes):
    return [note.pitch for note in notes]


def get_local_direction(
        notes,
):
    """Notes must be sorted by note on."""
    directions = []
    pitches = get_pitches(notes)
    for i, pitch in enumerate(pitches):
        if i == 0:
            continue
        if pitches[i - 1] > pitches[i]:
            direction = -1
        if pitches[i - 1] < pitches[i]:
            direction = 1
        if pitches[i - 1] == pitches[i]:
            direction = 0
        directions.append(direction)
    return directions


def znormalization(ts):
    """
    ts - each column of ts is a time series (np.ndarray)
    """
    mus = ts.mean(axis=0)
    stds = ts.std(axis=0)
    return (ts - mus) / stds


def make_ssm_figure(file_name: str):
    """
    Финальная функция кот генерит ссм
    """

    file = Path(file_name)
    filename = file.stem

    log.info(f"Processing {filename}")

    midi = Musa(file)

    iois = get_ioi(midi.notes)
    local_dir = get_local_direction(midi.notes)
    vector = [local_dir[i] + iois[i] for i in range(len(iois))]
    vector = np.asarray(vector)

    ###############################################################
    ####################### Normalize IOIs ########################
    ###############################################################
    zts = znormalization(vector)

    threshold = 1.0
    window = 20  # notes

    def peak_picking(array, threshold, window):
        # Peaks detection - sliding window
        lamda = round(window)  # window length
        peaks_position = signal.find_peaks(
            array,
            height=threshold,
            distance=lamda,
            width=1,
        )[0]  # array of peaks
        peaks_values = signal.find_peaks(
            array,
            height=threshold,
            distance=lamda,
            width=1,
        )[1]['peak_heights']  # array of peaks

        # Adding elements 1 and N' to the begining and end of the array
        if peaks_position[0] != 0:
            peaks_position = np.concatenate([[0], peaks_position])
        if peaks_position[-1] != array.shape[0] - 1:
            peaks_position = np.concatenate([peaks_position, [array.shape[0] - 1]])
        return peaks_position

    try:
        all_peaks = peak_picking(zts, threshold, window)
    except:
        all_peaks = [0]

    # breakpoint()

    ###############################################################
    ############## Evaluar antes de limpiar picos #################
    ###############################################################

    # Plot picos en iois
    plt.figure(figsize=(20, 5), dpi=300)
    plt.plot(zts, '-+', label="ts", alpha=0.2)
    for i in range(len(all_peaks)):
        if all_peaks[i] == len(zts):
            plt.plot(all_peaks[i], zts[-1], '-+', color="r", label="segments")
        else:
            plt.plot(all_peaks[i], zts[all_peaks[i]], '-+', color="r", label="segments")
        plt.axvline(all_peaks[i], color="r", label="boundaries", alpha=0.2)
    plt.savefig("figures-produced-by-figure-ssm/peaks.png", dpi=300, bbox_inches='tight', pad_inches=0,
                transparent=False)

    # Group notes in the predicted segments
    notes_segments = []
    for i in range(len(all_peaks)):
        if i + 1 == len(all_peaks):
            notes_segments.append(midi.notes[all_peaks[i]:-1])
            break
        notes_segments.append(midi.notes[all_peaks[i]:all_peaks[i + 1]])

    # Distance
    dists = []
    for i in range(len(notes_segments)):
        if i + 1 == len(all_peaks):
            dists.append(0.0)
            break
        s1, s2 = sum(get_ioi(notes_segments[i])), sum(get_ioi(notes_segments[i + 1]))
        if s1 == 0:
            s1 = []
        else:
            s1 = [s1]
        if s2 == 0:
            s2 = [0]
        else:
            s2 = [s2]
        d = distance.euclidean(s1, s2)
        dists.append(d)

    ssm = np.empty((len(notes_segments), len(notes_segments)))
    for i in range(len(notes_segments)):
        for j in range(len(notes_segments)):
            s1, s2 = sum(get_ioi(notes_segments[i])), sum(get_ioi(notes_segments[j]))
            if s1 == 0:
                s1 = []
            else:
                s1 = [s1]
            if s2 == 0:
                s2 = [0]
            else:
                s2 = [s2]
            d = distance.euclidean(s1, s2)
            ssm[i, j] = d

    nov = get_novelty_func(ssm)

    bounds = get_segment_boundaries(
        ssm=ssm,
        threshold=0.5,
        window=2,
    )

    # tow subplots as columns
    fig, axes = plt.subplots(
        nrows=1, ncols=2, figsize=(10, 5), dpi=300, tight_layout=True)
    ax1 = axes[0]
    ax2 = axes[1]

    ax1.imshow(ssm, origin="lower", extent=(0, ssm.shape[0], 0, ssm.shape[0]))

    x = np.arange(nov.shape[0])
    ax2.plot(-nov, x)
    for b in bounds:
        ax2.axhline(b, color="r", alpha=0.7, linewidth=1)

    ax1.margins(0)
    ax2.margins(0)
    plt.gcf().tight_layout()
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)

    result_dir = DIRECTORY_FOR_SSM + "/" + filename + ".png"
    plt.savefig(result_dir, dpi=300, bbox_inches='tight', pad_inches=0, transparent=False)
    log.info(f"SMM figure saved to {result_dir}")

    return result_dir, bounds

# if __name__ == '__main__':
#     make_graph_figure('11/11.mid')
