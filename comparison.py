from config import CONTENT_ROOT
from models.utils.dataparser import parse_txt
from ruptures.metrics import meantime
import logging as log
import numpy as np

from mir_eval.alignment import percentage_correct

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
    filename_gt = f"{CONTENT_ROOT}BPS_FH_Dataset/15/15_gt_mid.txt"
    filename_rup = f"{CONTENT_ROOT}BPS_FH_Dataset/15/15_ruptures_pred.txt"
    filename_symb = f"{CONTENT_ROOT}BPS_FH_Dataset/15/15_symbolic_pred.txt"

    gt = parse_txt(filename_gt, )
    data1 = parse_txt(filename_symb)
    data2 = parse_txt(filename_rup)

    print(len(gt))
    print(len(data1))
    print(len(data2))

    print(data2)

    print("symb: ", percentage_correct(np.array(data1), np.array(gt)))
    print("pelt: ", percentage_correct(np.array(data2), np.array(gt)))

    # filename_to_absolute_file = get_all_BPS_dataset_filenames()
    #
    # symbolic_scores = []
    # audio_scores = []
    #
    # for filename in filename_to_absolute_file:
    #     if filename != '7' and filename != '15':
    #         # log.info(f"Working with {filename_to_absolute_file[filename]}")
    #         current_file = filename_to_absolute_file[filename]
    #
    #         construct_filename_with_your_extention(current_file, ".ogg")
    #
    #         gt_path = construct_filename_with_your_extention(current_file, "_gt_mid.txt")
    #         symbolic_path = construct_filename_with_your_extention(current_file, "_symbolic_pred.txt")
    #         ruptures_path = construct_filename_with_your_extention(current_file, "_ruptures_pred.txt")
    #
    #         gt = parse_gt_txt(gt_path)
    #         symb = parse_gt_txt(symbolic_path)
    #         rupt = parse_gt_txt(ruptures_path)
    #
    #         f1_symb = f1_score(symb, gt, M=5)
    #         f1_audio = f1_score(rupt, gt, M=5)
    #
    #         # log.info(f"symb: {f1_symb}")
    #         # log.info(f"pelt: {f1_audio}")
    #
    #         symbolic_scores.append(f1_symb)
    #         audio_scores.append(f1_audio)
    #
    # print(np.mean(np.array(symbolic_scores)))
    # print(np.mean(np.array(audio_scores)))
