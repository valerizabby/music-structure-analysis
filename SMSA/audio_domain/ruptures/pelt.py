
import ruptures as rpt
import logging as log
import numpy as np

from SMSA.audio_domain.AudioPeltInterface import AudioPeltInterface
from SMSA.audio_domain.ruptures.utils.tempogram import bkps2sec
from SMSA.audio_domain.ruptures.utils.tempogram import tempo
from config import jump, penalty


import ruptures as rpt  # our package



class pelt(AudioPeltInterface):
    def __init__(self):
        pass

    def fit(self, filename: str, signal) -> rpt.Pelt:
        log.info(f"Using pelt algo to compute segmentation")

        tempogram = signal.T
        tempo_len: int = tempogram.shape[0]

        print(f"Current min_size {int(tempo_len / 15)}")
        print(f"Current jump {int(tempo_len / 1500)}")
        print(tempogram.shape)

        algo: rpt.Pelt = rpt.Pelt(
            model="rbf",
            min_size=int(tempogram.shape[0] / 15),
            jump=int(tempogram.shape[0] / 1500),).fit(tempogram)
        log.info("Pelt fitted to tempo")
        return algo

    def predict(self, filename: str) -> list:
        tempogram, sampling_rate = tempo(filename)
        algo = self.fit(filename, tempogram)
        log.info("Predicting boundaries")
        bkps = algo.predict(pen=penalty)
        log.info("Converting boundaries to seconds")
        result = bkps2sec(bkps, sampling_rate)
        return result


if __name__ == "__main__":
    # p = pelt()
    # filename = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/BPS_FH_Dataset/15/15.mp3"
    # print(p.predict(filename))

    # generate signal
    n_samples, dim, sigma = 500, 3, 3
    n_bkps = 6  # number of breakpoints
    signal, bkps = rpt.pw_constant(n_samples, dim, n_bkps, noise_std=sigma)
    print(signal.reshape(-1,1).shape[0])
    print(np.zeros((80362, 384)).reshape(-1, 1).shape[0] / signal.reshape(-1,1).shape[0])
