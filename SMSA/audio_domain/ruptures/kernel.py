from SMSA.audio_domain.AudioPeltInterface import AudioPeltInterface
import ruptures as rpt
from SMSA.utils.dataparser import construct_filename_with_your_extension
import logging as log
from SMSA.audio_domain.ruptures.utils.tempogram import tempo, bkps2sec
from SMSA.utils.dataparser import parse_txt

log.basicConfig(level=log.INFO)


class kernel(AudioPeltInterface):
    def __init__(self):
        pass

    def fit(self, filename, signal):
        log.info(f"Using kernel algo to compute segmentation")
        algo = rpt.KernelCPD(kernel="linear").fit(signal.T)
        log.info("Kernel fitted to tempo")
        return algo

    def predict(self, filename, n_bkps_hard=8, mode="gt"):
        if mode == "gt":
            n_bkps = len(parse_txt(construct_filename_with_your_extension(filename, "_gt_mid.txt")))
        else:
            n_bkps = n_bkps_hard

        tempogram, sampling_rate = tempo(filename)

        if n_bkps > 1:
            algo = self.fit(filename, tempogram)
            log.info("Predicting boundaries")
            bkps = algo.predict(n_bkps=n_bkps)
            log.info("Converting boundaries to seconds")
            result = bkps2sec(bkps, sampling_rate)
        else:
            result = []
            log.warning(f"NUMBER OF CHANGEPOINTS FOR {filename} IS NOT OK!")
        return result


if __name__ == "__main__":
    k = kernel()
    filename = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.ogg"
    print(k.predict(filename))

