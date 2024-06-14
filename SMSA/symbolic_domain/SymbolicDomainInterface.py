import os
import logging as log
from abc import ABC

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

from SMSA.symbolic_domain.utils.extraction import feature_extraction

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
