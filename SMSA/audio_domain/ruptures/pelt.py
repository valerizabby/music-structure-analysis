
import ruptures as rpt
import logging as log

from SMSA.audio_domain.AudioDomainSegmenter import AudioDomainSegmenter
from SMSA.audio_domain.utils import bkps2sec
from SMSA.audio_domain.utils import tempo
from config import min_size, jump, penalty


class pelt(AudioDomainSegmenter):
    def __init__(self):
        pass

    def fit(self, filename, signal):
        log.info(f"Using pelt algo to compute segmentation")
        # todo сделать здесь динамический подбор гиперпараметров
        # minsize = int(signal.shape[0]/14) или типа такого
        print(f"Current min_size {int(signal.T.shape[0] / 15)}")
        algo = rpt.Pelt(model="rbf", min_size=int(signal.T.shape[0] / 15), jump=jump,).fit(signal.T)
        # algo = rpt.Pelt(model="rbf", min_size=5000, jump=15,).fit(signal.T)
        log.info("Pelt fitted to tempo")
        return algo

    def predict(self, filename):
        tempogram, sampling_rate = tempo(filename)
        algo = self.fit(filename, tempogram)
        log.info("Predicting boundaries")
        bkps = algo.predict(pen=penalty)
        log.info("Converting boundaries to seconds")
        result = bkps2sec(bkps, sampling_rate)
        return result


if __name__ == "__main__":
    p = pelt()
    filename = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.ogg"
    print(p.predict(filename))
