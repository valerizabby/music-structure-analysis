from filename_utils import get_all_BPS_dataset_filenames
import numpy as np45

import pretty_midi

if __name__ == '__main__':
    filename_to_absolute_file = get_all_BPS_dataset_filenames()
    durations = []
    for filename in filename_to_absolute_file:
        dur = pretty_midi.PrettyMIDI(filename_to_absolute_file[filename]).get_end_time()
        durations.append(dur)

    print(durations)
    print(np.mean(np.array(durations)))

