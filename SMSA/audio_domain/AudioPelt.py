from pretty_midi import pretty_midi
from SMSA.audio_domain.ruptures.audio_segmentation import segmentation

from SMSA.utils.dataparser import construct_filename_with_your_extension

from SMSA.Segmenter import Segmenter


class AudioPelt(Segmenter):
    def __init__(self, algo_type, n_bkps_from_gt):
        # algo types: pelt, kernel
        self.algo_type = algo_type
        # n_bkps_from_gt: True, если берем данные из разметкм
        # False, если дефолтное
        self.n_bkps_from_gt = n_bkps_from_gt

    def predict(self, input_file):
        duration = pretty_midi.PrettyMIDI(construct_filename_with_your_extension(input_file, ".mid")).get_end_time()
        # n_bkps = len(parse_txt(construct_filename_with_your_extension(name, "_gt_mid.txt")))
        prediction_in_secs = segmentation(input_file, duration=duration, algo_type=self.algo_type)
        return prediction_in_secs


if __name__ == "__main__":
    model = AudioPelt(algo_type='pelt', n_bkps_from_gt=False)
    print(model.predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mp3"))
