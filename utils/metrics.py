import mir_eval
from mir_eval.alignment import absolute_error
from mir_eval.segment import detection
from pathlib import Path
from musicaiz.datasets.bps_fh import BPSFH
from utils.graph_figure_utils import get_boundaries
from musicaiz.loaders import Musa
from config import CONTENT_ROOT
from musicaiz.rhythm import ms_per_tick


dataset = Path("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset")
data = BPSFH(dataset)


def get_gt_boundaries(path_string: str):
    """
    Сейчас возвращает pos_mid - в этих тиках или как их там
    а надо сделать секунды
    """
    file = Path(path_string)
    filename = file.stem

    print(filename)

    csv_mid = data.parse_anns(anns="mid")

    musa_obj = Musa(file)
    print(csv_mid, filename)
    ref_mid = get_boundaries(csv_mid, filename)

    pos_mid = []
    for i in range(len(ref_mid)):
        pos = len([note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[ref_mid[i]].start_ticks])
        pos_mid.append(pos)

    return pos_mid

if __name__ == "__main__":
# TODO для каждого файла из бпс датасета сделать txt файл с boundary GT
## TODO перевести эту хрень в секунды
    boundaries = get_gt_boundaries('/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mid')

    # with open(CONTENT_ROOT + 'BPS_FH_Dataset/1/1-gt-mid.txt', 'w') as f:
    #     for bound in boundaries:
    #         f.write(str(bound) + "\n")

