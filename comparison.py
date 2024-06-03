from config import CONTENT_ROOT, BPS_absolute_path
from SMSA.utils.dataparser import parse_txt, construct_filename_with_your_extension, make_set_file_to_absolute_path
from ruptures.metrics import meantime
import logging as log
import numpy as np

from predict_mid_structure import f1_score

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
    # filename_gt = f"{CONTENT_ROOT}BPS_FH_Dataset/15/15_gt_mid.txt"
    # filename_rup = f"{CONTENT_ROOT}BPS_FH_Dataset/15/15_ruptures_pred.txt"
    # filename_symb = f"{CONTENT_ROOT}BPS_FH_Dataset/15/15_symbolic_pred.txt"
    # filename_rup_11_chang = f"{CONTENT_ROOT}BPS_FH_Dataset/15/_ruptures_pred_11.txt"
    #
    # gt = parse_txt(filename_gt, )
    # data1 = parse_txt(filename_symb)
    # data2 = parse_txt(filename_rup)
    #
    # print(len(gt))
    # print(len(data1))
    # print(len(data2))
    #
    # print(data2)
    #
    # print("symb: ", percentage_correct(np.array(data1), np.array(gt)))
    # print("pelt: ", percentage_correct(np.array(data2), np.array(gt)))

    filename_to_absolute_file = make_set_file_to_absolute_path(BPS_absolute_path, "ogg")

    symbolic_scores = []
    audio_scores = []
    audio_11_scores = []

    for filename in filename_to_absolute_file:
        if filename != '15':
            log.info(f"Working with {filename_to_absolute_file[filename]}")
            current_file = filename_to_absolute_file[filename]

            construct_filename_with_your_extension(current_file, ".ogg")

            gt_path = construct_filename_with_your_extension(current_file, "_gt_mid.txt")
            symbolic_path = construct_filename_with_your_extension(current_file, "_symbolic_pred.txt")
            ruptures_path = construct_filename_with_your_extension(current_file, "_ruptures_pred.txt")
            ruptures_11_path = construct_filename_with_your_extension(current_file, "_ruptures_pred_11.txt")

            gt = parse_txt(gt_path)
            symb = parse_txt(symbolic_path)
            rupt = parse_txt(ruptures_path)
            rupt11 = parse_txt(ruptures_11_path)

            f1_symb = f1_score(symb, gt, M=5)
            f1_audio = f1_score(rupt, gt, M=5)
            f1_audio_11 = f1_score(rupt11, gt, M=5)

            # log.info(f"symb: {f1_symb}")
            # log.info(f"pelt: {f1_audio}")

            symbolic_scores.append(f1_symb)
            audio_scores.append(f1_audio)
            audio_11_scores.append(f1_audio_11)

    print(f"Символьная структура: {np.mean(np.array(symbolic_scores))}")
    print(f"Аудио changepoint из gt {np.mean(np.array(audio_scores))}")
    print(f"Аудио changepoint 11 {np.mean(np.array(audio_11_scores))}")
