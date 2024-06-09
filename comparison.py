from config import BPS_absolute_path, RUSSIAN_POP_ABSOLUTE_PATH
from SMSA.Dataparser import parse_txt, construct_filename_with_your_extension, make_set_file_to_absolute_path
from ruptures.metrics import meantime
import logging as log
import numpy as np

from SMSA.utils.metrics import f1_score

log.basicConfig(level=log.INFO)


def meantime_custom(gt, pred, M=10):
    # фиктивно приравниваем последние элементы
    # The end of the last regime is not the same for each of the partitions
    if (gt[-1] > pred[-1]):
        pred[-1] = gt[-1]
    else:
        gt[-1] = pred[-1]
    return meantime(gt, pred)


if __name__ == "__main__":
    for abs_path in [RUSSIAN_POP_ABSOLUTE_PATH, BPS_absolute_path]:
        filename_to_absolute_file = make_set_file_to_absolute_path(abs_path, "mid")

        symbolic_scores = []
        audio_scores = []
        audio_11_scores = []
        lens = []
        for m in [5, 10]:
            for filename in filename_to_absolute_file:
                if filename != "15":
                    current_file = filename_to_absolute_file[filename]

                    construct_filename_with_your_extension(current_file, ".ogg")

                    gt_path = construct_filename_with_your_extension(current_file, "_gt_mid.txt")
                    symbolic_path = construct_filename_with_your_extension(current_file, "_symbolic_pred.txt")
                    ruptures_path = construct_filename_with_your_extension(current_file, "_ruptures_pred.txt")
                    if abs_path == RUSSIAN_POP_ABSOLUTE_PATH:
                        ruptures_11_path = construct_filename_with_your_extension(current_file, "_ruptures_pred_8.txt")
                    if abs_path == BPS_absolute_path:
                        ruptures_11_path = construct_filename_with_your_extension(current_file, "_ruptures_pred_11.txt")

                    gt = parse_txt(gt_path)

                    l = len(gt)

                    symb = parse_txt(symbolic_path)
                    rupt = parse_txt(ruptures_path)
                    rupt11 = parse_txt(ruptures_11_path)

                    f1_symb = f1_score(symb, gt, M=m)
                    f1_audio = f1_score(rupt, gt, M=m)
                    f1_audio_11 = f1_score(rupt11, gt, M=m)

                    lens.append(l)
                    symbolic_scores.append(f1_symb)
                    audio_scores.append(f1_audio)
                    audio_11_scores.append(f1_audio_11)

            print("|_____________________________________________|")
            print(f"Dataset: {abs_path}")
            print(f"Tolerance {m} secs")
            print(f"Символьная структура: {np.mean(np.array(symbolic_scores))}")
            print(f"Аудио changepoint из gt {np.mean(np.array(audio_scores))}")
            print(f"Аудио changepoint 8 {np.mean(np.array(audio_11_scores))}")
            print(f"Среднее число границ {np.mean(np.array(lens))}")
            print("|_____________________________________________|")
