import os.path
import numpy as np

from config import CONTENT_ROOT


def parse_result(filename) -> list:
    # тут костыль: читаем без последнего элемента, потому что там ''
    audio_file = os.path.join(CONTENT_ROOT, filename)
    with open(audio_file, 'r') as f:
        result = f.read().split("\n")[:-1]
    return list(map(float, result))


if __name__ == "__main__":
    res = parse_result('data/seg-audio-result.txt')
