from pretty_midi import pretty_midi

from SMSA.utils.dataparser import construct_filename_with_your_extension


def dur(filename):
    return pretty_midi.PrettyMIDI(construct_filename_with_your_extension(filename, ".mid")).get_end_time()
