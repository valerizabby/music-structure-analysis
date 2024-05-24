from pretty_midi import pretty_midi
from models.audio_domain.ruptures.audio_segmentation import segmentation

from models.utils.dataparser import construct_filename_with_your_extension

from models.Segmenter import Segmenter


class AudioPelt(Segmenter):
    def __init__(self, algo_type):
        self.algo_type = algo_type

    def predict(self, input_file):
        duration = pretty_midi.PrettyMIDI(construct_filename_with_your_extension(input_file, ".mid")).get_end_time()
        # n_bkps = len(parse_txt(construct_filename_with_your_extension(name, "_gt_mid.txt")))
        prediction_in_secs = segmentation(input_file, duration=duration, algo_type=self.algo_type)
        return prediction_in_secs


if __name__ == "__main__":
    AudioPelt(algo_type='pelt').predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mp3")
