import os
import logging as log
import warnings
from pathlib import Path
from musicaiz.features import StructurePrediction
import numpy as np
from config import BPS_absolute_path
from models.Segmenter import Segmenter
from models.utils.dataparser import make_set_file_to_absolute_path, construct_filename_with_your_extension

warnings.filterwarnings("ignore")
log.basicConfig(level=log.INFO)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class SymbolicPelt(Segmenter):
    def __init__(self):
        pass

    def predict(self, input_file):
        """
        Params:
            input_file -- абсолютный путь до MIDI файла
        Return:
            
        """
        file = Path(input_file)
        log.info(f"Predicting mid structure for file {input_file}")
        sp = StructurePrediction(file)
        result_mid_ms = sp.ms(level="mid", dataset="BPS")
        return list(np.array(result_mid_ms) / 1000)


if __name__ == "__main__":
    # print(SymbolicPelt().predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/7/7.mid"))
    filename_to_absolute_file = make_set_file_to_absolute_path(BPS_absolute_path, "mid")
    for filename in filename_to_absolute_file:
        name = filename_to_absolute_file[filename]
        log.info(f"Working with {name}")
        current_prediction_in_secs = SymbolicPelt().predict(name)
        with open(construct_filename_with_your_extension(name, "_symbolic_pred.txt"), 'w') as f:
            for bound in current_prediction_in_secs:
                f.write(str(bound) + "\n")

