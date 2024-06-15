import os
import logging as log
from abc import ABC
import warnings

warnings.filterwarnings("ignore")
log.basicConfig(level=log.INFO)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class SymbolicDomainInterface(ABC):
    def __init__(self):
        pass

    def fit(self, filename):
        pass

    def predict(self, filename):
        pass



if __name__ == "__main__":
    pass
