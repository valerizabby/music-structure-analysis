from __future__ import print_function
import msaf
from predict_mid_structure import f1_score
from utils.parse_result import parse_gt_txt


def msaf_segmentation(audio_file):
    """
    возвращает границы в секундах
    """
    boundaries, labels = msaf.process(audio_file)
    return boundaries


if __name__ == "__main__":
    audio_file = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mp3"
    boundaries = msaf_segmentation(audio_file)
    gt = parse_gt_txt("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1_gt_mid.txt")
    print(f1_score(gt, boundaries))
