import matplotlib.pyplot as plt
import librosa
import numpy as np

import logging as log

from config import BPS_absolute_path
from models.utils.dataparser import get_all_files_in_directory, make_set_file_to_absolute_path
from models.utils.dataparser import parse_txt

log.basicConfig(level=log.INFO)

from pretty_midi import pretty_midi

import ruptures as rpt

# Choose the number of changes (elbow heuristic)
from models.utils.dataparser import construct_filename_with_your_extension

n_bkps_max = 20  # K_max


def fig_ax(figsize=(15, 5), dpi=150):
    """Return a (matplotlib) figure and ax objects with given size."""
    return plt.subplots(figsize=figsize, dpi=dpi)


def get_sum_of_cost(algo, n_bkps):
    """Return the sum of costs for the change points `bkps`"""
    # todo
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


def segmentation(filename, duration, n_bkps_hard=8, algo_type="pelt", n_bkps_from_gt=True):
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


    # Segmentation
    if n_bkps_from_gt:
        n_bkps = len(parse_txt(construct_filename_with_your_extension(filename, "_gt_mid.txt")))
    else:
        n_bkps = n_bkps_hard

    # Choose detection method
    if algo_type == "kernel":
        algo = rpt.KernelCPD(kernel="linear").fit(tempogram.T)
        bkps = algo.predict(n_bkps=n_bkps)

    if algo_type == "pelt":
        # algo = rpt.Pelt(
        #                 model="rbf",
        #                 min_size=pelt_args.alpha*(len(self.midi_object.notes)/15),
        #                 jump=int(pelt_args.betha*pelt_args.alpha*(len(self.midi_object.notes)/15)),
        #             ).fit(nn)
        #             result = algo.predict(pen=pelt_args.penalty)
        algo = rpt.Pelt(model="rbf").fit(tempogram.T)
        # TODO какой тут пеналти ставить
        bkps = algo.predict(pen=0.5)

    # Convert the estimated change points (frame counts) to actual timestamps
    bkps_times = librosa.frames_to_time(bkps, sr=sampling_rate, hop_length=hop_length_tempo)
    # Compute change points corresponding indexes in original signal
    bkps_time_indexes = (sampling_rate * bkps_times).astype(int).tolist()
    result = (np.array(bkps_time_indexes) / sampling_rate)
    print(result)

    return result


if __name__ == "__main__":
    name = '/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/7/7.ogg'
    duration = pretty_midi.PrettyMIDI(construct_filename_with_your_extension(name, ".mid")).get_end_time()
    current_prediction_in_secs = segmentation(name, duration=duration, algo_type="kernel", n_bkps_from_gt=True)
    with open(construct_filename_with_your_extension(name, "_ruptures_pred.txt"), 'w') as f:
        for bound in current_prediction_in_secs:
            f.write(str(bound) + "\n")
    # filename_to_absolute_file = make_set_file_to_absolute_path(BPS_absolute_path, "ogg")
    # for filename in filename_to_absolute_file:
    #     if filename != '7':
    #         name = filename_to_absolute_file[filename]
    #         duration = pretty_midi.PrettyMIDI(construct_filename_with_your_extension(name, ".mid")).get_end_time()
    #         # n_bkps = len(parse_txt(construct_filename_with_your_extension(name, "_gt_mid.txt")))
    #         log.info(f"Working with {name}")
    #         current_prediction_in_secs = segmentation(name, duration=duration, n_bkps_hard=11, algo_type="kernel", n_bkps_from_gt=False)
    #         with open(construct_filename_with_your_extension(name, "_ruptures_pred_11.txt"), 'w') as f:
    #             for bound in current_prediction_in_secs:
    #                 f.write(str(bound) + "\n")
