from SMSA.Dataparser import parse_txt, construct_filename_with_your_extension, make_set_file_to_absolute_path
from SMSA.symbolic_domain.SymbolicDomainInterface import SymbolicDomainInterface
from SMSA.symbolic_domain.utils.extraction import feature_extraction
import logging as log
from musicaiz.loaders import Musa
import warnings
import numpy as np
import ruptures as rpt

from config import RUSSIAN_POP_ABSOLUTE_PATH, BPS_absolute_path

warnings.filterwarnings("ignore")
log.basicConfig(level=log.INFO)

novelty_curve_shape = []

class kernel(SymbolicDomainInterface):

    def __init__(self, mode, kernel="rbf"):
        self.mode = mode
        self.kernel = kernel

    def fit(self, filename):
        signal = feature_extraction(filename)
        print(signal.shape)
        novelty_curve_shape.append(signal.shape[0])
        log.info("Fitting to novelty curve")
        algo = rpt.KernelCPD(kernel=self.kernel).fit(signal)

        return algo

    def predict(self, filename, n_bkps_hard=15):

        if self.mode == "gt":
            n_bkps = len(parse_txt(construct_filename_with_your_extension(filename, "_gt_mid.txt")))
        else:
            n_bkps = n_bkps_hard

        musa_object = Musa(filename)
        algo = self.fit(filename)
        log.info("Predicting result")
        result = algo.predict(n_bkps=n_bkps)
        print(result)
        return [musa_object.notes[n].start_sec for n in result]


if __name__ == '__main__':
    pass
    # filename_to_absolute_file = make_set_file_to_absolute_path(BPS_absolute_path, "mid")
    # for filename in filename_to_absolute_file:
    #     name = filename_to_absolute_file[filename]
    #     log.info(f"Working with {name}")
    #     print(kernel(mode="gt").fit(name))
    #
    # with open("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/novelty_shape_BPS.txt", 'w') as f:
    #     for bound in novelty_curve_shape:
    #         f.write(str(bound) + "\n")
    #
    # with open("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/time_for_predicting.txt", 'w') as f:
    #     for bound in time_for_predicting:
    #         f.write(str(bound) + "\n")
    #
    # with open("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/tempo_len.txt", 'w') as f:
    #     for bound in tempo_lens:
    #         f.write(str(bound) + "\n")
    #
    # print(f"average time for fitting: {np.mean(np.array(time_for_fitting))}")
    # print(f"average time for predict: {np.mean(np.array(time_for_predicting))}")
