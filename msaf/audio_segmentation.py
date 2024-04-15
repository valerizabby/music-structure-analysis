# Simple MSAF example
from __future__ import print_function
import msaf
from config import CONTENT_ROOT

def msaf_segmentation(audio_file):
    boundaries, labels = msaf.process(audio_file)
    return boundaries

# 3. Save segments using the MIREX format
# out_file = '/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/segments.txt'
# print('Saving output to %s' % out_file)
# msaf.io.write_mirex(boundaries, labels, out_file)


if __name__ == "__main__":
    audio_file = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/MIDIs/1/1.mp3"
    boundaries = msaf_segmentation(audio_file)

    with open(CONTENT_ROOT + 'data/seg-audio-msaf-result.txt', 'w') as f:
        for bound in boundaries:
            f.write(str(bound) + "\n")
