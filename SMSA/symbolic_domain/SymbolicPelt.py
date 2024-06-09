import os
import logging as log
import warnings
from pathlib import Path
from musicaiz.features import StructurePrediction
import numpy as np
from config import BPS_absolute_path
from SMSA.Segmenter import Segmenter
from SMSA.utils.dataparser import make_set_file_to_absolute_path, construct_filename_with_your_extension

warnings.filterwarnings("ignore")
log.basicConfig(level=log.INFO)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class SymbolicPelt(Segmenter):
    def __init__(self):
        pass

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
    # print(SymbolicPelt().predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mid"))
    # filename_to_absolute_file = make_set_file_to_absolute_path(BPS_absolute_path, "mid")
    # for filename in filename_to_absolute_file:
    # name = filename_to_absolute_file[filename]
    name = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/BPS_FH_Dataset/7/7.mid"
    result = SymbolicPelt().predict(name)

    # log.info(f"Working with {name}")
    # current_prediction_in_secs = SymbolicPelt().predict(name)
    # print(current_prediction_in_secs)
    with open(construct_filename_with_your_extension(name, "_symbolic_pred.txt"), 'w') as f:
        for bound in result:
            f.write(str(bound) + "\n")

