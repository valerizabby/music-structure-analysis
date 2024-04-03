from midi2audio import FluidSynth


def midi2wav(input_file, output_file):
    FluidSynth().midi_to_audio(input_file, output_file)


if __name__ == "__main__":
    FluidSynth().midi_to_audio('BPS_FH_Dataset/1/1.mid', '1.wav')
