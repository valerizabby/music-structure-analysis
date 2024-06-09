
from pathlib import Path

import numpy as np
from musicaiz import BPSFH
from pretty_midi import pretty_midi
import logging as log

log.basicConfig(level=log.INFO)

from config import BPS_absolute_path
from SMSA.utils.dataparser import make_set_file_to_absolute_path, construct_filename_with_your_extension


def gt(dataset):
    data = BPSFH(dataset)
    csv = data.parse_anns(anns="mid")
    counts = []
    for file in make_set_file_to_absolute_path(BPS_absolute_path, "mid"):
        # count boundaries
        print(file)
        print(csv[Path(file).stem])
        counts.append(len(csv[Path(file).stem].index))

    mean_counts_file = np.asarray(counts).mean()
    std_counts_file = np.asarray(counts).std()
    print("Total number of boundaries: ", sum(counts))
    print("Mean number of boundaries per file: ", mean_counts_file)
    print("Standard deviation of boundaries per file: ", std_counts_file)

if __name__ == "__main__":
    gt(BPS_absolute_path)
