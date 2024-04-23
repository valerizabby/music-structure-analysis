import numpy as np
from musicaiz.rhythm import ms_per_bar
from musicaiz.structure import Bar

# Bar.get_bars_duration

def get_boundaries(csv, filename):
    ref = np.empty((len(csv[filename])),
                   dtype=int)  # crear una matriz 17x2, igual que el tamaño de la matriz csv[filename]
    for idx, row in enumerate(csv[filename].iterrows()):  # recorre la matriz csv[filename]
        ref[idx] = row[1][1]
    ref = np.insert(ref, 0, 0)
    return ref


def get_labels(csv, filename):
    ref = np.empty((len(csv[filename])),
                   dtype="S10")
    for idx, row in enumerate(csv[filename].iterrows()):
        ref[idx] = row[1][2]
    return ref


def bar_to_sec():
    pass
