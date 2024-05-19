import matplotlib.pyplot as plt
import librosa
import numpy as np

import logging as log

from utils.parse_result import parse_gt_txt

log.basicConfig(level=log.INFO)

from pretty_midi import pretty_midi

import ruptures as rpt

# Choose the number of changes (elbow heuristic)
from utils.get_BPS_filenames import get_all_BPS_dataset_filenames, construct_filename_with_your_extention

n_bkps_max = 20  # K_max


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
    # Compute the tempogram
    tempogram = librosa.feature.tempogram(
        onset_envelope=oenv,
        sr=sampling_rate,
        hop_length=hop_length_tempo,
    )
    log.info("Tempogram computed")
    # # Display the tempogram
    # fig, ax = fig_ax()
    # _ = librosa.display.specshow(
    #     tempogram,
    #     ax=ax,
    #     hop_length=hop_length_tempo,
    #     sr=sampling_rate,
    #     x_axis="s",
    #     y_axis="tempo",
    # )
    # fig.savefig(CONTENT_ROOT + "data/tempo.png")
    # print("Tempogram saved to " + CONTENT_ROOT + "data/tempo.png")

    return tempogram


def segmentation(filename, duration, n_bkps=8):
    print(filename)
    """
    @param filename -- абсолютный путь до аудио файла (.ogg)
    @param duration -- продолжительность отрезка аудио в секундах
    @param n_bkps -- количество changepoint-ов
    """

    signal, sampling_rate = librosa.load(filename, duration=duration)
    hop_length_tempo = 256
    oenv = librosa.onset.onset_strength(
        y=signal, sr=sampling_rate, hop_length=hop_length_tempo
    )

    tempogram = compute_tempogram(sampling_rate, oenv, hop_length_tempo)
    # Choose detection method
    algo = rpt.KernelCPD(kernel="linear").fit(tempogram.T)

    # Start by computing the segmentation with most changes.
    _ = algo.predict(n_bkps_max)

    array_of_n_bkps = np.arange(1, n_bkps_max + 1)

    plot_decision_graph(algo, array_of_n_bkps, construct_filename_with_your_extention(filename, "_elbow_graph.png"))

    # TODO как считать количество changepoint-ов inplace?
    # _ = ax.scatter([5], [get_sum_of_cost(algo=algo, n_bkps=5)], color="r", s=100)

    # Segmentation
    bkps = algo.predict(n_bkps=n_bkps)
    # Convert the estimated change points (frame counts) to actual timestamps
    bkps_times = librosa.frames_to_time(bkps, sr=sampling_rate, hop_length=hop_length_tempo)

    # for b in bkps_times[:-1]:
    #     ax.axvline(b, ls="--", color="white", lw=4)

    # Compute change points corresponding indexes in original signal
    bkps_time_indexes = (sampling_rate * bkps_times).astype(int).tolist()

    # for segment_number, (start, end) in enumerate(rpt.utils.pairwise([0] + bkps_time_indexes), start=1):
    #     # ВРЕМЯ В СЕКУНДАХ
    #     print("Start", round(start / sampling_rate, 3), "end", round(end / sampling_rate, 3))

    result = (np.array(bkps_time_indexes) / sampling_rate)
    print(result)
    return result


if __name__ == "__main__":
    count = 0
    filename_to_absolute_file = get_all_BPS_dataset_filenames('.ogg')
    for filename in filename_to_absolute_file:
        if filename != '7':
            name = filename_to_absolute_file[filename]
            duration = pretty_midi.PrettyMIDI(construct_filename_with_your_extention(name, ".mid")).get_end_time()
            # # TODO узнаем количество точек разбиения из gt, как без этого?
            n_bkps = len(parse_gt_txt(construct_filename_with_your_extention(name, "_gt_mid.txt")))
            log.info(f"Working with {name}")
            current_prediction_in_secs = segmentation(name, duration=duration, n_bkps=n_bkps)
            with open(construct_filename_with_your_extention(name, "_ruptures_pred.txt"), 'w') as f:
                for bound in current_prediction_in_secs:
                    f.write(str(bound) + "\n")
