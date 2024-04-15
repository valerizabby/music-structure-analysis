import os
import logging
import logging as log
import matplotlib
import matplotlib.pyplot as plt
import warnings
import numpy as np
import networkx as nx
from pathlib import Path
from utils.parse_result import parse_result

from musicaiz.loaders import Musa
from musicaiz.features import (
    get_novelty_func,
    musa_to_graph)
from musicaiz.features import PeltArgs
from musicaiz.features import LevelsBPS
from musicaiz.features import StructurePrediction
from musicaiz.datasets.bps_fh import BPSFH
warnings.filterwarnings("ignore")

from config import CONTENT_ROOT

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
matplotlib.use('agg')

log.basicConfig(level=logging.INFO)

# DIRECTORY_FOR_SSM = "figures-produced-by-figure-ssm/"

dataset = "BPS_FH_Dataset"
DIRECTORY_FOR_FIGURE = "app/static/Image"


# TODO обобщить код
# TODO результаты разметки другими алгоритмами - сравнение (рисовать вместе)
# приводить выходы к одному виду - к какому? лист / json / tree / append строчка с разметкой(?)
# поиграться с визуализацией
# отрисовать MIDI (fluidsynth) и положить в audio (???)!!


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



def make_graph_figure(path_string):

    file = Path(path_string)
    filename = file.stem

    print(filename)

    data = BPSFH(dataset)
    csv_high = data.parse_anns(anns="high")
    csv_mid = data.parse_anns(anns="mid")
    csv_low = data.parse_anns(anns="low")

    ref_high = get_boundaries(csv_high, filename)
    ref_mid = get_boundaries(csv_mid, filename)
    ref_low = get_boundaries(csv_low, filename)

    lab_high = get_labels(csv_high, filename)
    lab_mid = get_labels(csv_mid, filename)
    lab_low = get_labels(csv_low, filename)

    musa_obj = Musa(file)

    g = musa_to_graph(musa_obj)
    mat = nx.attr_matrix(g)[0]
    n = get_novelty_func(mat)
    nn = np.reshape(n, (n.size, 1))

    # predict high
    log.info("Predicting high...")

    alpha = 0.8
    beta = 0.5
    sp = StructurePrediction(file)
    minsize = alpha * (len(musa_obj.notes) / 15)
    jump = int(round(beta * minsize))
    penalty = 2
    pelt_args = LevelsBPS.HIGH
    pelt_args = PeltArgs(
        penalty=penalty,
        alpha=alpha,
        betha=beta,
        level="high"
    )
    # pelt_args = PeltArgs(
    #     penalty=penalty,
    #     model="rbf",
    #     minsize=minsize,  # 100
    #     jump=jump,  # 20
    # )
    result_high = sp.beats(level="high", dataset="BPS")

    #result_high = sp.beats(pelt_args)

    # predict mid

    log.info("Predicting mid...")

    alpha = 0.6
    beta = 0.02
    sp = StructurePrediction(file)
    minsize = alpha * (len(musa_obj.notes) / 15)
    jump = int(round(beta * minsize))
    penalty = 0.5
    #pelt_args = LevelsBPS.MID
    pelt_args = PeltArgs(
        penalty=penalty,
        alpha=alpha,
        betha=beta,
        level="mid"
    )
    # pelt_args = PeltArgs(
    #     penalty=penalty
    #     # model="rbf",
    #     # minsize=minsize,  # 100
    #     # jump=jump,  # 20
    # )

    #result_mid = sp.beats(pelt_args)
    result_mid = sp.beats(level="mid", dataset="BPS")

    # predict low

    log.info("Predicting low...")

    alpha = 0.8
    beta = 0.5
    sp = StructurePrediction(file)
    minsize = alpha * (len(musa_obj.notes) / 15)
    jump = int(round(beta * minsize))
    penalty = 2
    #pelt_args = LevelsBPS.LOW
    pelt_args = PeltArgs(
        penalty=penalty,
        alpha=alpha,
        betha=beta,
        level="low"
    )
    # pelt_args = PeltArgs(
    #     penalty=penalty,
    #     model="rbf",
    #     minsize=minsize,  # 100
    #     jump=jump,  # 20
    # )

    result_low = sp.beats(level="low", dataset="BPS")
    #result_low = sp.beats(pelt_args)

    log.info("Making picture...")

    #labels = ("test", "test", "test", "test", "test", "test","test","test", "test")

    fig, axes = plt.subplots(
        nrows=9, ncols=1, figsize=(25, 18), dpi=300,
        gridspec_kw={'height_ratios': [61, 8, 5, 8, 5, 8, 5, 5, 6]})


    ax1 = axes[0]
    ax2 = axes[1]
    ax3 = axes[2]
    ax4 = axes[3]
    ax5 = axes[4]
    ax6 = axes[5]
    ax7 = axes[6]
    ax8 = axes[7]
    ax9 = axes[8]

    ax1.set_xlabel("gt")
    ax2.set_xlabel("low")
    ax3.set_xlabel("gt")
    ax4.set_xlabel("mid")
    ax5.set_xlabel("gt")
    ax6.set_xlabel("high")
    ax7.set_xlabel("ruptures")
    ax8.set_xlabel("msaf")

    # plt.ylabel('msaf', axes=ax1)
    # plt.ylabel('ruptures', axes=ax2)
    # plt.ylabel('high', axes=ax3)
    # plt.ylabel('gt', axes=ax4)
    # plt.ylabel('mid', axes=ax5)
    # plt.ylabel('gt', axes=ax6)
    # plt.ylabel('low', axes=ax7)
    # plt.ylabel('gt', axes=ax8)

    pos_high, pos_mid, pos_low = [], [], []
    for i in range(len(ref_high)):
        pos = len([note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[ref_high[i]].start_ticks])
        pos_high.append(pos)
        # ax1.axvline(pos, color='#f48383', linestyle="-", alpha=.5)
    for i in range(len(ref_mid)):
        pos = len([note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[ref_mid[i]].start_ticks])
        pos_mid.append(pos)
        # ax1.axvline(pos, color='#b5d9a6', linestyle="-", alpha=.5)
    for i in range(len(ref_low)):
        pos = len([note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[ref_low[i]].start_ticks])
        pos_low.append(pos)
        # ax1.axvline(pos, color='#bcbcbc', linestyle="-", alpha=.5)

    ax1.plot(range(nn.shape[0]), n)

    # ground truth high
    for p, i in enumerate(pos_high):
        if p % 2 == 0:
            color = '#f48383'
        else:
            color = '#f4cccc'
        ax2.axvline(i, color='#f48383', linestyle="-", alpha=1)
        if p < len(pos_high) - 1:
            ax2.text((pos_high[p] + pos_high[p + 1]) / 2, 0.5, lab_high[p].tostring().decode('utf-8'), ha='center',
                     va='center', size=14)
            ax2.axvspan(pos_high[p], pos_high[p + 1], facecolor=color, alpha=0.5)

    # predicted high
    for p, i in enumerate(result_high):
        res = len([note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[result_high[p]].start_ticks])
        ax3.axvline(res, color='#f48383', linestyle="-", alpha=1)

    # ground truth mid
    for p, i in enumerate(pos_mid):
        if p % 2 == 0:
            color = '#7f9fbc'
        else:
            color = '#b6cfe6'
        ax4.axvline(i, color='#7f9fbc', linestyle="-", alpha=1)
        if p < len(pos_mid) - 1:
            ax4.text((pos_mid[p] + pos_mid[p + 1]) / 2, 0.5, lab_mid[p].tostring().decode('utf-8'), ha='center',
                     va='center', size=13)
            ax4.axvspan(pos_mid[p], pos_mid[p + 1], facecolor=color, alpha=0.5)

    # predicted mid
    for p, i in enumerate(result_mid):
        res = len([note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[result_mid[p]].start_ticks])
        ax5.axvline(res, color='#f48383', linestyle="-", alpha=1)

    # ground truth low
    for p, i in enumerate(pos_low):
        if p % 2 == 0:
            color = '#a8d197'
        else:
            color = '#cae9bd'
        ax6.axvline(i, color='#94ba84', linestyle="-", alpha=1)
        if p < len(pos_low) - 1:
            ax6.text((pos_low[p] + pos_low[p + 1]) / 2, 0.5, lab_low[p].tostring().decode('utf-8'), ha='center',
                     va='center', size=13)
            ax6.axvspan(pos_low[p], pos_low[p + 1], facecolor=color, alpha=0.5)

    # predicted low
    for p, i in enumerate(result_low):
        res = len([note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[result_low[p]].start_ticks])
        ax7.axvline(res, color='#f48383', linestyle="-", alpha=1)

    # мои audio предикты
    # TODO сделать нормальный флоу! читать эту инфу из файла

    for p in np.array(parse_result("data/seg-audio-result.txt")) * (2156/401):
        ax8.axvline(p, color='#0000FF', linestyle="-", alpha=1)
    # for p in [213.41987253, 441.94580218, 729.21057356,
    #                        958.48556385, 1106.30020505, 1518.65811027,
    #                        1796.74688833, 2023.40016627, 2156.04632862]:
    #     ax8.axvline(p, color='#0000FF', linestyle="-", alpha=1)

    for p in np.array(parse_result("data/seg-audio-msaf-result.txt")) * (2156/401):
        ax9.axvline(p, color='#006400', linestyle="-", alpha=1)

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
    ax8.set_xticks([])
    ax8.set_yticks([])
    ax9.set_xticks([])
    ax9.set_yticks([])

    ax1.margins(x=0)
    ax2.margins(x=0)
    ax3.margins(x=0)
    ax4.margins(x=0)
    ax5.margins(x=0)
    ax6.margins(x=0)
    ax7.margins(x=0)
    ax8.margins(x=0)
    ax9.margins(x=0)
    # plt.show()

    result_dir = CONTENT_ROOT + DIRECTORY_FOR_FIGURE + "/" + filename + "-figure" + ".png"
    log.info("Saving pic into " + result_dir)
    plt.savefig(result_dir, dpi=300, bbox_inches='tight', pad_inches=0, transparent=False)
    return result_dir


if __name__ == '__main__':
    #make_graph_figure('app/data/upload_files_from_localhost/soldat.mid')
    make_graph_figure('MIDIs/1/1.mid')

