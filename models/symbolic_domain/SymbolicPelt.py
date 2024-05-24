import os
import logging as log
import warnings
from pathlib import Path
from musicaiz.loaders import Musa
from musicaiz.features import StructurePrediction

from models.Segmenter import Segmenter

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
        musa_obj = Musa(file)
        #### PREDICT MID ####
        log.info("Predicting mid...")
        sp = StructurePrediction(file)
        result_mid = sp.beats(level="mid", dataset="BPS")

        sec_mid_predicted = []
        for p, i in enumerate(result_mid):
            if p == 0:
                sec_mid_predicted.append(0)
            else:
                array_of_notes = [note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[result_mid[p]].start_ticks]
                sec_mid_predicted.append(array_of_notes[-1].end_sec)
        return sec_mid_predicted


if __name__ == "__main__":
    print(SymbolicPelt().predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mid"))
