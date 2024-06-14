import os
import logging as log
from SMSA.Segmenter import Segmenter
import warnings
from SMSA.symbolic_domain.methods.pelt import pelt
from SMSA.symbolic_domain.methods.kernel import kernel

warnings.filterwarnings("ignore")
log.basicConfig(level=log.INFO)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class SymbolicDomain(Segmenter):

    def __init__(self, algo, mode="gt", kernel="rbf"):
        self.algo = algo
        self.mode = mode
        self.kernel = kernel

    def fit(self, filename: str):
        if self.algo == "kernel":
            return kernel(mode=self.mode, kernel=self.kernel).fit(filename=filename)

        if self.algo == "pelt":
            return pelt().fit(filename=filename)

    def predict(self, filename: str, n_bkps_hard: int = 8) -> list:
        if self.algo == "kernel":
            return kernel(mode=self.mode).predict(filename=filename, n_bkps_hard=n_bkps_hard)

        if self.algo == "pelt":
            return pelt().predict(filename=filename)



if __name__ == "__main__":
    print(SymbolicDomain(algo="kernel", mode="gt").predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/BPS_FH_Dataset/1/1.mid"))


