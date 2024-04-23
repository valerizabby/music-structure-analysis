from midi2audio import FluidSynth
from pathlib import Path


# FluidSynth('sound_font.sf2')
# FluidSynth().play_midi('soldat.mid')


def midi2audio(audiofile : str):
    # # fs.midi_to_audio(audiofile, 'output-soldat.flac')
    # fs.midi_to_audio(audiofile, Path(audiofile).stem + ".flac")
    FluidSynth('sound_font.sf2').midi_to_audio(audiofile, Path(audiofile).stem + ".flac")


if __name__ == "__main__":
    midi2audio("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mid")
