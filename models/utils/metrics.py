from musicaiz.datasets.bps_fh import BPSFH
from pathlib import Path

from ruptures.metrics import precision_recall

from models.utils.dataparser import make_set_file_to_absolute_path
from models.symbolic_domain.utils.graph_figure_utils import get_boundaries
from musicaiz.loaders import Musa
from config import CONTENT_ROOT, dataset, BPS_absolute_path

data = BPSFH(dataset)


def array_of_notes_to_end_sec(array_of_notes):
    """
    на вход лист с нотами

    метод достает end_time последней ноты
    """
    return array_of_notes[-1].end_sec


def get_gt_boundaries(path_string: str):
    """
    Сейчас возвращает pos_mid - в этих тиках или как их там
    а надо сделать секунды
    """
    file = Path(path_string)
    filename = file.stem
    csv_mid = data.parse_anns(anns="mid")
    musa_obj = Musa(file)
    ref_mid = get_boundaries(csv_mid, filename)

    pos_mid = []
    sec_mid_predicted = []

    print(len(ref_mid))
    for i in range(len(ref_mid)):
        if i == 0:
            sec_mid_predicted.append(0)
        else:
            array_of_notes = [note for note in musa_obj.notes if
                              note.start_ticks <= musa_obj.beats[ref_mid[i]].start_ticks]
            pos = len(array_of_notes)
            sec_mid_predicted.append(array_of_notes_to_end_sec(array_of_notes))
            pos_mid.append(pos)

    return sec_mid_predicted

    def f1_score(gt, pred, M=10):
        # фиктивно приравниваем последние элементы
        # The end of the last regime is not the same for each of the partitions
        if (gt[-1] > pred[-1]):
            pred[-1] = gt[-1]
        else:
            gt[-1] = pred[-1]

        precision, recall = precision_recall(gt, pred, margin=M)
        return 2 * precision * recall / (precision + recall)



if __name__ == "__main__":
    # тут код достает гт разметку для всех файлов BPS
    filename_to_absolute_file = make_set_file_to_absolute_path(BPS_absolute_path, "mid")
    for filename in filename_to_absolute_file:
        if filename != '7':
            print(CONTENT_ROOT + "BPS_FH_Dataset/" + filename + "/" + filename + "_gt_mid.txt")
            current_gt = get_gt_boundaries(filename_to_absolute_file[filename])
            with open(CONTENT_ROOT + "BPS_FH_Dataset/" + filename + "/" + filename + "_gt_mid.txt", 'w') as f:
                for bound in current_gt:
                    f.write(str(bound) + "\n")
