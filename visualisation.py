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
from SMSA.Dataparser import parse_txt, construct_filename_with_your_extension
from SMSA.symbolic_domain.utils.graph_figure_utils import get_boundaries, get_labels
from config import BPS_absolute_path


warnings.filterwarnings("ignore")
log.basicConfig(level=logging.INFO)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
matplotlib.use('agg')

# dataset = "BPS_FH_Dataset"
dataset = BPS_absolute_path
# DIRECTORY_FOR_FIGURE = "app/static/Image"


def array_of_notes_to_end_sec(array_of_notes):
    """
    на вход лист с нотами

    метод достает end_time последней ноты
    """
    return array_of_notes[-1].end_sec


def make_graph_figure(path_string, result_dir):
    file = Path(path_string)
    musa_obj = Musa(file)
    g = musa_to_graph(musa_obj)
    mat = nx.attr_matrix(g)[0]
    n = get_novelty_func(mat)
    nn = np.reshape(n, (n.size, 1))

    log.info("Predicting mid...")

    sp = StructurePrediction(file)
    result_mid = sp.beats(level="mid", dataset="BPS")

    log.info("Making picture...")

    fig, axes = plt.subplots(
        nrows=7, ncols=1, figsize=(20, 12), dpi=350,
        gridspec_kw={'height_ratios': [60, 8, 8, 8, 8, 8, 8]})

    ax1 = axes[0]
    ax2 = axes[1]
    ax3 = axes[2]
    ax4 = axes[3]
    ax5 = axes[4]
    ax6 = axes[5]
    ax7 = axes[6]

    ax1.set_xlabel("novelty curve")
    ax2.set_xlabel("ground-truth")
    ax3.set_xlabel("SymbolicDomain(pelt)")
    ax4.set_xlabel("SymbolicDomain(kernel, hard)")
    ax5.set_xlabel("SymbolicDomain(kernel, gt)")
    ax6.set_xlabel("AudioDomain(kernel, hard)")
    ax7.set_xlabel("AudioDomain(kernel, gt)")

    sec_mid_predicted = []
    sec_mid_ground_truth = []

    ax1.plot(range(nn.shape[0]), n)

    for p, i in enumerate(np.array(parse_txt(construct_filename_with_your_extension(path_string, "_gt_mid.txt"))) * 10.6):
        ax2.axvline(i, color='#8383f4', linestyle="-", alpha=1)

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

    for p, i in enumerate(np.array(parse_txt(construct_filename_with_your_extension(path_string, "_symbolic_pred_kernel_hard.txt"))) * 10.6):
        ax4.axvline(i, color='#f48383', linestyle="-", alpha=1)

    for p, i in enumerate(np.array(parse_txt(construct_filename_with_your_extension(path_string, "_symbolic_pred_kernel_gt.txt"))) * 10.6):
        ax5.axvline(i, color='#f48383', linestyle="-", alpha=1)

    for p, i in enumerate(np.array(parse_txt(construct_filename_with_your_extension(path_string, "_ruptures_pred_8.txt"))) * 10.6):
        ax6.axvline(i, color='#f48383', linestyle="-", alpha=1)

    for p, i in enumerate(np.array(parse_txt(construct_filename_with_your_extension(path_string, "_ruptures_pred.txt"))) * 10.6):
        ax7.axvline(i, color='#f48383', linestyle="-", alpha=1)

    ax1.set_xticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax4.set_xticks([])
    ax4.set_yticks([])
    ax5.set_xticks([])
    ax5.set_yticks([])
    ax6.set_xticks([])
    ax6.set_yticks([])
    ax7.set_xticks([])
    ax7.set_yticks([])


    ax1.margins(x=0)
    ax2.margins(x=0)
    ax3.margins(x=0)
    ax4.margins(x=0)
    ax5.margins(x=0)
    ax6.margins(x=0)
    ax7.margins(x=0)

    log.info("Saving pic into " + result_dir)
    plt.savefig(result_dir, dpi=350, bbox_inches='tight', pad_inches=0, transparent=False)
    return {"GT": sec_mid_ground_truth, "PREDICTED": sec_mid_predicted}


if __name__ == "__main__":
     make_graph_figure("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/RussianPop/meloch_kiskis/meloch_kiskis.mid",
                       "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/visualisation.png")

     # make_graph_figure("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/BPS_FH_Dataset/1/1.mid",
     #                   "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/")
