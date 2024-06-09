import os
import logging
import logging as log
import matplotlib
import matplotlib.pyplot as plt
import warnings
import numpy as np
import networkx as nx
from pathlib import Path
from musicaiz.loaders import Musa
from musicaiz.features import (
    get_novelty_func,
    musa_to_graph)
from musicaiz.features import StructurePrediction
from musicaiz.datasets.bps_fh import BPSFH
from config import CONTENT_ROOT
from SMSA.utils.dataparser import parse_txt
from SMSA.symbolic_domain.utils.graph_figure_utils import get_boundaries, get_labels
from ruptures.metrics import precision_recall


warnings.filterwarnings("ignore")
log.basicConfig(level=logging.INFO)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
matplotlib.use('agg')

# dataset = "BPS_FH_Dataset"
dataset = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/BPS_FH_Dataset"
DIRECTORY_FOR_FIGURE = "app/static/Image"


def f1_score(gt, pred, M=10):
    # фиктивно приравниваем последние элементы
    # The end of the last regime is not the same for each of the partitions
    if (gt[-1] > pred[-1]):
        pred[-1] = gt[-1]
    else:
        gt[-1] = pred[-1]

    precision, recall = precision_recall(gt, pred, margin=M)
    return 2 * precision * recall / (precision + recall)


def array_of_notes_to_end_sec(array_of_notes):
    """
    на вход лист с нотами

    метод достает end_time последней ноты
    """
    return array_of_notes[-1].end_sec


def make_graph_figure(path_string):
    file = Path(path_string)
    filename = file.stem

    data = BPSFH(dataset)

    csv_mid = data.parse_anns(anns="mid")
    ref_mid = get_boundaries(csv_mid, filename)
    lab_mid = get_labels(csv_mid, filename)
    musa_obj = Musa(file)

    g = musa_to_graph(musa_obj)
    mat = nx.attr_matrix(g)[0]
    n = get_novelty_func(mat)
    nn = np.reshape(n, (n.size, 1))

    #### PREDICT MID ####

    log.info("Predicting mid...")
    sp = StructurePrediction(file)
    result_mid = sp.beats(level="mid", dataset="BPS")

    log.info("Making picture...")

    fig, axes = plt.subplots(
        nrows=4, ncols=1, figsize=(20, 9), dpi=300,
        gridspec_kw={'height_ratios': [60, 8, 8, 8]})

    ax1 = axes[0]
    ax2 = axes[1]
    ax3 = axes[2]
    ax4 = axes[3]

    ax1.set_xlabel("novelty curve")
    ax2.set_xlabel("mid gt")
    ax3.set_xlabel("pred")
    ax4.set_xlabel("ruptures")

    pos_mid = []
    sec_mid_predicted = []
    sec_mid_ground_truth = []

    for i in range(len(ref_mid)):
        # Note(start_sec=1.500000, end_sec=2.000000, start_ticks=288, end_ticks=384)
        # берем start_sec первой ноты и end_sec последней (?) на самом деле для каждого массива берем последнюю
        if i == 0:
            sec_mid_ground_truth.append(0)
        else:
            array_of_notes = [note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[ref_mid[i]].start_ticks]
            pos = len(array_of_notes)

            sec_mid_ground_truth.append(array_of_notes_to_end_sec(array_of_notes))
            pos_mid.append(pos)

    ax1.plot(range(nn.shape[0]), n)

    # ground truth mid
    for p, i in enumerate(pos_mid):
        if p % 2 == 0:
            color = '#7f9fbc'
        else:
            color = '#b6cfe6'
        ax2.axvline(i, color='#7f9fbc', linestyle="-", alpha=1)
        if p < len(pos_mid) - 1:
            ax2.text((pos_mid[p] + pos_mid[p + 1]) / 2, 0.5, lab_mid[p].tostring().decode('utf-8'), ha='center', va='center', size=13)
            ax2.axvspan(pos_mid[p], pos_mid[p + 1], facecolor=color, alpha=0.5)

    # predicted mid
    pred_mid = []
    for p, i in enumerate(result_mid):
        if (p == 0):
            sec_mid_predicted.append(0)
        else:
            array_of_notes = [note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[result_mid[p]].start_ticks]

            sec_mid_predicted.append(array_of_notes_to_end_sec(array_of_notes))
            res = len(array_of_notes)
            pred_mid.append(res)
            ax3.axvline(res, color='#f48383', linestyle="-", alpha=1)

    for p, i in enumerate(np.array(parse_txt('/data/BPS_FH_Dataset/13/13_ruptures_pred.txt')) * 10.6):
        ax4.axvline(i, color='#f48383', linestyle="-", alpha=1)

    ax1.set_xticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax4.set_xticks([])
    ax4.set_yticks([])

    ax1.margins(x=0)
    ax2.margins(x=0)
    ax3.margins(x=0)
    ax4.margins(x=0)

    result_dir = CONTENT_ROOT + DIRECTORY_FOR_FIGURE + "/" + filename + "-figure" + ".png"
    log.info("Saving pic into " + result_dir)
    plt.savefig(result_dir, dpi=300, bbox_inches='tight', pad_inches=0, transparent=False)
    return {"GT": sec_mid_ground_truth, "PREDICTED": sec_mid_predicted}


if __name__ == '__main__':
    result = make_graph_figure('/data/BPS_FH_Dataset/13/13.mid')

    # print(result)
    # print(f1_score(result["GT"], result["PREDICTED"], 5))
    # запустили symbolic алгоритм на всех файлах
    # filename_to_absolute_file = get_all_BPS_dataset_filenames()
    # for filename in filename_to_absolute_file:
    #     if filename != '7':
    #         log.info(f"Working with {filename_to_absolute_file[filename]}")
    #         current_prediction_in_secs = make_graph_figure(filename_to_absolute_file[filename])['PREDICTED']
    #         with open(CONTENT_ROOT + "BPS_FH_Dataset/" + filename + "/" + filename + "_symbolic_pred.txt", 'w') as f:
    #             for bound in current_prediction_in_secs:
    #                 f.write(str(bound) + "\n")
