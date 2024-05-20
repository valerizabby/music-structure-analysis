import os.path
import numpy as np

from config import CONTENT_ROOT


def parse_gt_txt(filename):
    """парсит txt файлы где через перенос строки числа записаны"""
    data = []
    with open(filename) as f:
        for line in f:
            data.append([float(x) for x in line.split()][0])
    return data


def parse_result(filename) -> list:
    # тут костыль: читаем без последнего элемента, потому что там ''
    audio_file = os.path.join(CONTENT_ROOT, filename)
    with open(audio_file, 'r') as f:
        result = f.read().split("\n")[:-1]
    return list(map(float, result))


if __name__ == "__main__":
    print(parse_gt_txt("/BPS_FH_Dataset/10/10_gt_mid.txt"))
