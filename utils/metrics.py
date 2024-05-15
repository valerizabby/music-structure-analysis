import mir_eval
from mir_eval.alignment import absolute_error
from mir_eval.segment import detection
from pathlib import Path
from musicaiz.datasets.bps_fh import BPSFH
from pathlib import Path
import glob

from predict_mid_structure import array_of_notes_to_end_sec
from utils.graph_figure_utils import get_boundaries
from musicaiz.loaders import Musa


dataset = Path("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset")
CONTENT_ROOT = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/"
data = BPSFH(dataset)


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
            array_of_notes = [note for note in musa_obj.notes if note.start_ticks <= musa_obj.beats[ref_mid[i]].start_ticks]
            pos = len(array_of_notes)
            sec_mid_predicted.append(array_of_notes_to_end_sec(array_of_notes))
            pos_mid.append(pos)

    return sec_mid_predicted


def get_all_BPS_dataset_filenames():
    files_in_dataset_directory = glob.glob("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/*", recursive=True)
    # list_of_midi_files = []
    filename_to_absolute_file = {}
    for directory in files_in_dataset_directory:
        if '.' not in directory:
            filename = Path(directory).stem
            filename_wo_extention = CONTENT_ROOT + "BPS_FH_Dataset/" + filename + "/" + filename
            midi_path = filename_wo_extention + ".mid"
            # list_of_midi_files.append(midi_path)
            filename_to_absolute_file[filename] = midi_path
    return filename_to_absolute_file


if __name__ == "__main__":
    # тут код достает гт разметку для всех файлов BPS
    filename_to_absolute_file = get_all_BPS_dataset_filenames()
    for filename in filename_to_absolute_file:
        if filename != '7':
            print(CONTENT_ROOT + "BPS_FH_Dataset/" + filename + "/" + filename + "_gt_mid.txt")
            current_gt = get_gt_boundaries(filename_to_absolute_file[filename])
            with open(CONTENT_ROOT + "BPS_FH_Dataset/" + filename + "/" + filename + "_gt_mid.txt", 'w') as f:
                for bound in current_gt:
                    f.write(str(bound) + "\n")


