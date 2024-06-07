from pathlib import Path
import librosa
import numpy as np

import logging as log

from musicaiz import LevelsBPS
from musicaiz.loaders import Musa

from SMSA.audio_domain.utils import compute_tempogram
from SMSA.utils.dataparser import parse_txt
from config import hop_length_tempo, min_size, jump

log.basicConfig(level=log.INFO)

from pretty_midi import pretty_midi

import ruptures as rpt

# Choose the number of changes (elbow heuristic)
from SMSA.utils.dataparser import construct_filename_with_your_extension



def kernel(filename, tempogram, mode, n_bkps_hard):

    # Segmentation
    if mode == "gt":
        n_bkps = len(parse_txt(construct_filename_with_your_extension(filename, "_gt_mid.txt")))
    else:
        n_bkps = n_bkps_hard

    log.info(f"Using kernel algo to compute segmentation")
    algo = rpt.KernelCPD(kernel="linear").fit(tempogram.T)
    log.info("Kernel fitted to tempo")
    bkps = algo.predict(n_bkps=n_bkps)
    return bkps


def pelt(filename, tempogram):

    log.info(f"Using pelt algo to compute segmentation")
    # midi_object = Musa(file=Path(construct_filename_with_your_extension(filename, ".mid")))
    pelt_args = LevelsBPS.MID.value
    # log.info(f"min_size: {pelt_args.alpha * (len(midi_object.notes))}")
    # log.info(f"jump: {int(pelt_args.betha * pelt_args.alpha * (len(midi_object.notes)))}")

    algo = rpt.Pelt(
        model="rbf",
        min_size=min_size,
        jump=jump,
    ).fit(tempogram.T)

    # algo = rpt.Pelt(model="rbf").fit(tempogram.T)
    log.info("Pelt fitted to tempo")
    bkps = algo.predict(pen=pelt_args.penalty)
    return bkps


def segmentation(filename, duration, n_bkps_hard=8, algo="pelt", mode="gt"):
    print(filename)
    """
    @param filename -- абсолютный путь до аудио файла (.ogg)
    @param duration -- продолжительность отрезка аудио в секундах
    @param n_bkps -- количество changepoint-ов
    """

    signal, sampling_rate = librosa.load(filename, duration=duration)

    oenv = librosa.onset.onset_strength(y=signal, sr=sampling_rate, hop_length=hop_length_tempo)

    tempogram = compute_tempogram(sampling_rate, oenv, hop_length_tempo)

    # Choose detection method
    if algo == "kernel":
        bkps = kernel(filename, tempogram, mode, n_bkps_hard)

    if algo == "pelt":
        bkps = pelt(filename, tempogram)

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
    current_prediction_in_secs = segmentation(name, duration=duration, algo_type="pelt")
    print(current_prediction_in_secs)

    # with open(construct_filename_with_your_extension(name, "_ruptures_pred.txt"), 'w') as f:
    #     for bound in current_prediction_in_secs:
    #         f.write(str(bound) + "\n")
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
