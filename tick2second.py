import pretty_midi


def midi_file_to_secs_using_pretty_midi(filename, array_of_ticks):
    pm = pretty_midi.PrettyMIDI(filename)
    for i in range(len(array_of_ticks)):
        array_of_ticks[i] = pm.tick_to_time(array_of_ticks[i])
    return array_of_ticks



