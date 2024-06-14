from pretty_midi import pretty_midi

from SMSA.Dataparser import construct_filename_with_your_extension, make_set_file_to_absolute_path
from config import BPS_absolute_path, RUSSIAN_POP_ABSOLUTE_PATH
import numpy as np


def dur(filename: str):
    return pretty_midi.PrettyMIDI(construct_filename_with_your_extension(filename, ".mid")).get_end_time()


if __name__ == "__main__":
    dataset_to_duration = {RUSSIAN_POP_ABSOLUTE_PATH: 0, BPS_absolute_path: 0}
    for dataset in dataset_to_duration:
        durations = []
        filename_to_absolute_file = make_set_file_to_absolute_path(dataset, "mid")
        for filename in filename_to_absolute_file:
            name = filename_to_absolute_file[filename]
            current_duration = dur(name)

            durations.append(current_duration)

        dataset_to_duration[dataset] = np.mean(np.array(durations))

    print(dataset_to_duration)

#     result:
#     {'/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/RussianPop/': 189.995566,
#     '/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/BPS_FH_Dataset/': 455.55645161290323}

