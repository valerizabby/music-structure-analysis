import os
import logging as log

from musicaiz.features import StructurePrediction
from musicaiz.loaders import Musa

from SMSA.Segmenter import Segmenter
import warnings
import ruptures as rpt
import numpy as np
import networkx as nx

from pathlib import Path

from musicaiz.features import (
    get_novelty_func,
    musa_to_graph
)


warnings.filterwarnings("ignore")
log.basicConfig(level=log.INFO)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class SymbolicPelt(Segmenter):
    def __init__(self):
        pass

    @staticmethod
    def feature_extraction(filename: str):
        musa_object = Musa(filename)
        g = musa_to_graph(musa_object)
        mat = nx.attr_matrix(g)[0]
        n = get_novelty_func(mat)
        nn = np.reshape(n, (n.size, 1))
        return nn

    def _get_structure_boundaries(
        self,
        filename
    ):

        musa_object = Musa(filename)
        signal = self.feature_extraction(filename)

        try:
            log.info("Fitting to novelty curve")
            algo = rpt.KernelCPD(kernel="linear").fit(signal)
            log.info("Predicting result")
            result = algo.predict(n_bkps=15)
        except:
            warnings.warn("No structure found.")
            result = [0, len(musa_object.notes)-1]
        return [musa_object.notes[n].start_sec for n in result]


    def fit(self, filename):
        file = Path(filename)
        sp = StructurePrediction(file)
        return sp

    def predict(self, filename):
        """
        Params:
            input_file -- абсолютный путь до MIDI файла
        Return:
        """
        log.info(f"Predicting mid structure for file {filename}")
        result_mid_ms = self.fit(filename).ms(level="mid", dataset="BPS")
        return list(np.array(result_mid_ms) / 1000)


if __name__ == "__main__":
    pass

    # # print(SymbolicPelt().predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mid"))
    # # filename_to_absolute_file = make_set_file_to_absolute_path(BPS_absolute_path, "mid")
    # # for filename in filename_to_absolute_file:
    # # name = filename_to_absolute_file[filename]
    # name = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/BPS_FH_Dataset/7/7.mid"
    # result = SymbolicPelt().predict(name)
    #
    # # log.info(f"Working with {name}")
    # # current_prediction_in_secs = SymbolicPelt().predict(name)
    # # print(current_prediction_in_secs)
    # with open(construct_filename_with_your_extension(name, "_symbolic_pred.txt"), 'w') as f:
    #     for bound in result:
    #         f.write(str(bound) + "\n")

