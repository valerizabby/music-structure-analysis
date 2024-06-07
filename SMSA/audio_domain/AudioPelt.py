from SMSA.audio_domain.ruptures.kernel import kernel
from SMSA.audio_domain.ruptures.pelt import pelt
from SMSA.audio_domain.utils import tempo

from SMSA.Segmenter import Segmenter
from SMSA.utils.dataparser import make_set_file_to_absolute_path, construct_filename_with_your_extension
from config import BPS_absolute_path


class AudioPelt(Segmenter):
    def __init__(self, algo, mode="gt"):
        # algo: ["pelt", "kernel"]
        self.algo = algo
        # mode = "gt" если gt разметка, "hard" если хардкодед
        self.mode = mode

    def fit(self, filename):
        if self.algo == "kernel":
            return kernel().fit(filename=filename, signal=tempo(filename))

        if self.algo == "pelt":
            return pelt().fit(filename=filename, signal=tempo(filename))

    def predict(self, filename):
        if self.algo == "kernel":
            return kernel().predict(filename=filename, mode=self.mode)

        if self.algo == "pelt":
            return pelt().predict(filename=filename)
        # duration = pretty_midi.PrettyMIDI(construct_filename_with_your_extension(input_file, ".mid")).get_end_time()
        # # n_bkps = len(parse_txt(construct_filename_with_your_extension(name, "_gt_mid.txt")))
        # prediction_in_secs = segmentation(input_file, duration=duration, algo_type=self.algo)
        # return prediction_in_secs


if __name__ == "__main__":
    model = AudioPelt(algo='pelt', mode="gt")
    print(model.predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/7/7.mp3"))

    # filename_to_absolute_file = make_set_file_to_absolute_path(BPS_absolute_path, "mp3")
    #
    # for filename in filename_to_absolute_file:
    #     name = filename_to_absolute_file[filename]
    #     # проблемы с 11 (не хватает памяти) и с 7
    #     if (filename != "32" and filename != "20" and filename != "18" and filename != "27" and filename != "9" and filename != "11"):
    #         print(f"Working with {name}")
    #         current_prediction_in_secs = AudioPelt(algo='pelt').predict(name)
    #         with open(construct_filename_with_your_extension(name, "_audio_pelt_pred.txt"), 'w') as f:
    #             for bound in current_prediction_in_secs:
    #                 f.write(str(bound) + "\n")


