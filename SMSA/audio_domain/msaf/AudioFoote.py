from msaf.algorithms.foote import segmenter
from msaf.input_output import FileStruct
import msaf


if __name__ == "__main__":
    print(msaf.process("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mp3"))
    # fs = FileStruct("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mp3")
    # s = segmenter.Segmenter(fs)
    # print(s.processFlat())
