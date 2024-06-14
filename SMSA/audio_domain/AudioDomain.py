from SMSA.audio_domain.ruptures.kernel import kernel
from SMSA.audio_domain.ruptures.pelt import pelt
from SMSA.audio_domain.ruptures.utils.tempogram import tempo

from SMSA.Segmenter import Segmenter


class AudioDomain(Segmenter):
    def __init__(self, algo, mode="gt", n=15):
        # algo: ["pelt", "kernel"]
        self.algo = algo
        # mode: ["gt", "hard"]
        self.mode = mode
        # желаемое число точек изменения в методе pelt
        self.n = n

    def fit(self, filename: str):
        if self.algo == "kernel":
            return kernel().fit(filename=filename, signal=tempo(filename))

        if self.algo == "pelt":
            return pelt().fit(filename=filename, signal=tempo(filename))

    def predict(self, filename: str, n_bkps_hard: int = 8) -> list:
        if self.algo == "kernel":
            return kernel().predict(filename=filename, mode=self.mode, n_bkps_hard=n_bkps_hard)

        if self.algo == "pelt":
            return pelt().predict(filename=filename, n=self.n)


if __name__ == "__main__":
    model = AudioDomain(algo='pelt', mode="gt")
    print(model.predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/7/7.mp3"))
