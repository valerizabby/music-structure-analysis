from pathlib import Path

from musicaiz.datasets.bps_fh import BPSFH


# dataset = "BPS_FH_Dataset"
dataset = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset"
DIRECTORY_FOR_FIGURE = "app/static/Image"
import numpy as np


def get_boundaries(csv, filename):
    ref = np.empty((len(csv[filename])), dtype=int)  # создайте матрицу 17x2, просто нажмите на матрицу csv[имя файла]
    for idx, row in enumerate(csv[filename].iterrows()):  # записать матрицу csv[имя файла]
        ref[idx] = row[1][1]
    ref = np.insert(ref, 0, 0)
    return ref


def get_labels(csv, filename):
    ref = np.empty((len(csv[filename])), dtype="S10")
    for idx, row in enumerate(csv[filename].iterrows()):
        ref[idx] = row[1][2]
    return ref


if __name__ == "__main__":
    file = Path("/BPS_FH_Dataset/3/3.mid")
    filename = file.stem
    data = BPSFH(dataset)
    csv_mid = data.parse_anns(anns="mid")
    ref_mid = get_boundaries(csv_mid, filename)
    print(ref_mid)
