from __future__ import print_function
import msaf

import logging as log
import logging

log.basicConfig(level=logging.INFO)

CONTENT_ROOT = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/"


def msaf_segmentation(audio_file):
    """
    возвращает границы в секундах
    """
    boundaries, labels = msaf.process(audio_file)
    return boundaries


if __name__ == "__main__":
    # TODO пофиксить ошибку WARNING:root:Audio file too short, or too many few beats estimated. Returning empty estimations.
    audio_file = "/BPS_FH_Dataset/23/23.mp3"
    # boundaries = msaf_segmentation(audio_file)
    boundaries, labels = msaf.process(audio_file, boundaries_id="foote", labels_id="cnmf")
    print(boundaries)
# if __name__ == "__main__":
#     # тут код достает гт разметку для всех файлов BPS
#     filename_to_absolute_file = get_all_BPS_dataset_filenames(".mp3")
#     for filename in filename_to_absolute_file:
#         if filename != '7':
#             log.info(f"Working with {filename_to_absolute_file[filename]}")
#             current_boundaries = msaf_segmentation(filename_to_absolute_file[filename])
#             with open(CONTENT_ROOT + "BPS_FH_Dataset/" + filename + "/" + filename + "_msaf_pred.txt", 'w') as f:
#                 for bound in current_boundaries:
#                     f.write(str(bound) + "\n")

