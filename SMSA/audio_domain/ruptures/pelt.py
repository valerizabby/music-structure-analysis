
import ruptures as rpt
import logging as log

from SMSA.audio_domain.AudioPeltInterface import AudioPeltInterface
from SMSA.audio_domain.ruptures.utils.tempogram import bkps2sec
from SMSA.audio_domain.ruptures.utils.tempogram import tempo
from config import jump, penalty


class pelt(AudioPeltInterface):
    def __init__(self):
        pass

    def fit(self, filename: str, signal) -> rpt.Pelt:
        log.info(f"Using pelt algo to compute segmentation")
        print(f"Current min_size {int(signal.T.shape[0] / 8)}")
        print(f"Current jump {int(signal.T.shape[0] / 800)}")
        tempogram = signal.T
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
    p = pelt()
    filename = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/RussianPop/batarei_nervi/batarei_nervi.mp3"
    print(p.predict(filename))
