from mido.midifiles.units import tick2second
from mido import MidiFile
import pretty_midi

from utils.metrics import get_gt_boundaries


def midi_file_to_secs_using_pretty_midi(filename, array_of_ticks):
    pm = pretty_midi.PrettyMIDI(filename)
    for i in range(len(array_of_ticks)):
        array_of_ticks[i] = pm.tick_to_time(array_of_ticks[i])
    return array_of_ticks


def midi_file_to_secs(filename, array_of_ticks):
    """
    tick - сами тики которые надо перевести в секунды
    tick_per_beat ??? вроде то же самое что resolution
    tempo??? (bpm) видимо динамика в миди файле = velocity
    """
    mid = MidiFile(filename)
    info_about_midi_file = mid.tracks[0]
    MetaMessages = []

    for msg in info_about_midi_file:
        MetaMessages.append(msg)

    # TODO вообще tempo это не то, tempo = velocity каждого message в MIDI файле
    #  по идее надо проходиться по датасету и доставать velocity по кусочкам
    tempo = MetaMessages[0].tempo
    ticks_per_beat = mid.ticks_per_beat

    for i in range(len(array_of_ticks)):
        array_of_ticks[i] = tick2second(array_of_ticks[i], ticks_per_beat, tempo)
    return array_of_ticks

if __name__ == "__main__":
    filename = '/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mid'
    # 404 секунды ~=~ 2156 тиков(?)
    print(midi_file_to_secs(filename, get_gt_boundaries(filename)))
    print(midi_file_to_secs_using_pretty_midi(filename, get_gt_boundaries(filename)))

