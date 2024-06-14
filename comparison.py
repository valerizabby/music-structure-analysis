from config import BPS_absolute_path, RUSSIAN_POP_ABSOLUTE_PATH
from SMSA.Dataparser import parse_txt, construct_filename_with_your_extension, make_set_file_to_absolute_path
from ruptures.metrics import meantime
import logging as log
import numpy as np

from SMSA.utils.metrics import f1_score

log.basicConfig(level=log.INFO)


# todo запустить на бпс
# все добавить в сравнение
# переделать рисунок интерфейса и пайплайна
# посчитать сложность вычисления чистого пелта на бпс


# написать всякие описания

def meantime_custom(gt, pred, M=10):
    # фиктивно приравниваем последние элементы
    # The end of the last regime is not the same for each of the partitions
    if (gt[-1] > pred[-1]):
        pred[-1] = gt[-1]
    else:
        gt[-1] = pred[-1]
    return meantime(gt, pred)


if __name__ == "__main__":
    for abs_path in [RUSSIAN_POP_ABSOLUTE_PATH]:
        filename_to_absolute_file = make_set_file_to_absolute_path(abs_path, "mid")

        symbolic_scores = []
        audio_scores = []
        audio_11_scores = []
        pelt_scores = []
        symbolic_kernel_scores = []
        symbolic_kernel_hard_scores = []
        lens = []

        for m in [10]:
            for filename in filename_to_absolute_file:
                if filename != "15":
                    log.info(filename)
                    # if filename != "krugligod_anacondaz":
                    current_file = filename_to_absolute_file[filename]

                    construct_filename_with_your_extension(current_file, ".ogg")

                    gt_path = construct_filename_with_your_extension(current_file, "_gt_mid.txt")
                    symbolic_path = construct_filename_with_your_extension(current_file, "_symbolic_pred.txt")
                    ruptures_path = construct_filename_with_your_extension(current_file, "_ruptures_pred.txt")
                    # pelt_path = construct_filename_with_your_extension(current_file, "_pelt_pred.txt")
                    if abs_path == RUSSIAN_POP_ABSOLUTE_PATH:
                        ruptures_11_path = construct_filename_with_your_extension(current_file, "_ruptures_pred_8.txt")
                    if abs_path == BPS_absolute_path:
                        ruptures_11_path = construct_filename_with_your_extension(current_file, "_ruptures_pred_11.txt")
                    symbolic_kernel_path = construct_filename_with_your_extension(current_file, "_symbolic_pred_kernel_gt.txt")
                    symbolic_kernel_hard_path = construct_filename_with_your_extension(current_file, "_symbolic_pred_kernel_hard.txt")

                gt = parse_txt(gt_path)

                l = len(gt)

                symb = parse_txt(symbolic_path)
                rupt = parse_txt(ruptures_path)
                rupt11 = parse_txt(ruptures_11_path)
                # pelt = parse_txt(pelt_path)
                symbolic_kernel = list(set(parse_txt(symbolic_kernel_path)))
                symbolic_kernel_hard = list(set(parse_txt(symbolic_kernel_hard_path)))

                f1_symb = f1_score(symb, gt, M=m)
                f1_audio = f1_score(rupt, gt, M=m)
                f1_audio_11 = f1_score(rupt11, gt, M=m)
                # f1_pelt = f1_score(pelt, gt, M=m)
                f1_symb_kernel = f1_score(symbolic_kernel, gt, M=m)
                f1_symb_kernel_hard = f1_score(symbolic_kernel_hard, gt, M=m)

                lens.append(l)
                symbolic_scores.append(f1_symb)
                audio_scores.append(f1_audio)
                audio_11_scores.append(f1_audio_11)
                # pelt_scores.append(f1_pelt)
                symbolic_kernel_scores.append(f1_symb_kernel)
                symbolic_kernel_hard_scores.append(f1_symb_kernel_hard)

            print("|_____________________________________________|")
            print(f"Dataset: {abs_path}")
            print(f"Tolerance {m} secs")
            print(f"SymbolicDomain(algo=pelt): {np.mean(np.array(symbolic_scores))}")
            print(f"AudioDomain(algo=kernel, mode=gt) {np.mean(np.array(audio_scores))}")
            print(f"AudioDomain(algo=kernel, mode=hard) {np.mean(np.array(audio_11_scores))}")
            # print(f"AudioDomain(algo=pelt) {np.mean(np.array(pelt_scores))}")
            print(f"SymbolicDomain(algo=kernel, mode=gt) {np.mean(np.array(symbolic_kernel_scores))}")
            print(f"SymbolicDomain(algo=kernel, mode=hard) {np.mean(np.array(symbolic_kernel_hard_scores))}")
            print(f"Среднее число границ {np.mean(np.array(lens))}")
            print("|_____________________________________________|")
