# from config import BPS_absolute_path
# import numpy as np
#
# import pretty_midi
#
# from models.utils.dataparser import make_set_file_to_absolute_path
#
# if __name__ == '__main__':
#     filename_to_absolute_file = make_set_file_to_absolute_path(BPS_absolute_path, "mid")
#     durations = []
#     for filename in filename_to_absolute_file:
#         dur = pretty_midi.PrettyMIDI(filename_to_absolute_file[filename]).get_end_time()
#         durations.append(dur)
#
#     print(durations)
#     print(np.mean(np.array(durations)))
#
