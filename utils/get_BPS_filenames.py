import glob
from pathlib import Path


CONTENT_ROOT = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/"


def get_all_BPS_dataset_filenames(extention=".mid"):
    files_in_dataset_directory = glob.glob("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/*", recursive=True)
    # list_of_midi_files = []
    filename_to_absolute_file = {}
    for directory in files_in_dataset_directory:
        if '.' not in directory and Path(directory).stem != 'estimations':
            filename = Path(directory).stem
            filename_wo_extention = CONTENT_ROOT + "BPS_FH_Dataset/" + filename + "/" + filename
            midi_path = filename_wo_extention + extention
            # list_of_midi_files.append(midi_path)
            filename_to_absolute_file[filename] = midi_path
    return filename_to_absolute_file


def construct_filename_with_your_extention(filename, ext):
    """
    Params:
    filename -- абсолютный путь до файла
    ext -- конец файла вида "_kek.ogg"
    """
    parent_name = Path(filename).parent
    name = Path(filename).stem
    return f"{parent_name}/{name}{ext}"
