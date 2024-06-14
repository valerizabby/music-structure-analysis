
import ruptures as rpt
import logging as log
import numpy as np

from config import RUSSIAN_POP_ABSOLUTE_PATH, BPS_absolute_path

from SMSA.Dataparser import make_set_file_to_absolute_path
from SMSA.audio_domain.AudioPeltInterface import AudioPeltInterface
from SMSA.audio_domain.ruptures.utils.tempogram import bkps2sec
from SMSA.audio_domain.ruptures.utils.tempogram import tempo
from config import jump, penalty
import time


import ruptures as rpt  # our package


time_for_fitting = []
time_for_predicting = []
tempo_lens = []


class pelt(AudioPeltInterface):
    def __init__(self):
        pass

    def fit(self, filename: str, signal, n: int = 15) -> rpt.Pelt:
        log.info(f"Using pelt algo to compute segmentation")

        tempogram = signal.T
        tempo_len: int = tempogram.shape[0]

        print(f"Current min_size: {int(tempo_len / n)}")
        print(f"Current jump: {int(tempo_len / (100 * n))}")
        print(f"Tempogram shape: {tempogram.shape}")
        tempo_lens.append(tempogram.shape[0])
        start_time = time.time()

        algo: rpt.Pelt = rpt.Pelt(
            model="rbf",
            min_size=int(tempogram.shape[0] / n),
            jump=int(tempogram.shape[0] / (100 * n)),).fit(tempogram)

        end_time = time.time()

        # time_for_fitting.append(end_time - start_time)

        print(f"Time for fitting to tempogram: {end_time - start_time}")
        log.info("Pelt fitted to tempo")
        return algo

    def predict(self, filename: str, n: int = 15) -> list:
        tempogram, sampling_rate = tempo(filename)
        print(tempogram.shape)
        algo = self.fit(filename, tempogram, n=15)
        log.info("Predicting boundaries")
        start_time = time.time()
        bkps = algo.predict(pen=penalty)
        end_time = time.time()
        # time_for_predicting.append(end_time - start_time)
        print(f"Time for predicting: {end_time - start_time}")
        log.info("Converting boundaries to seconds")
        result = bkps2sec(bkps, sampling_rate)
        return result


if __name__ == "__main__":

    filename_to_absolute_file = make_set_file_to_absolute_path(RUSSIAN_POP_ABSOLUTE_PATH, "mp3")
    print(filename_to_absolute_file)
    # for filename in filename_to_absolute_file:
    #     name = filename_to_absolute_file[filename]
    #     log.info(f"Working with {name}")
    #     print(pelt().predict(name))

    # with open("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/time_for_fitting.txt", 'w') as f:
    #     for bound in time_for_fitting:
    #         f.write(str(bound) + "\n")
    #
    # with open("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/time_for_predicting.txt", 'w') as f:
    #     for bound in time_for_predicting:
    #         f.write(str(bound) + "\n")

    # with open("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/tempo_len.txt", 'w') as f:
    #     for bound in tempo_lens:
    #         f.write(str(bound) + "\n")
    #
    # print(np.mean(np.array(tempo_lens)))

    # print(f"average time for fitting: {np.mean(np.array(time_for_fitting))}")
    # print(f"average time for predict: {np.mean(np.array(time_for_predicting))}")

