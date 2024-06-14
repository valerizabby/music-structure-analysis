from musicaiz import StructurePrediction

from SMSA.symbolic_domain.SymbolicDomainInterface import SymbolicDomainInterface
from pathlib import Path
import numpy as np
import logging as log

class pelt(SymbolicDomainInterface):
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


if __name__ == '__main__':
    print(pelt().predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/BPS_FH_Dataset/1/1.mid"))
