import glob
from pathlib import Path

from config import BPS_absolute_path


def parse_txt(filename: str) -> list:
    """
    Парсит txt файлы (где числа записаны через перенос строки) в лист
    """
    data = []
    with open(filename) as f:
        for line in f:
            data.append([float(x) for x in line.split()][0])
    return data


def get_all_files_in_directory(directory :str, extension: str):
    """
    Находит все файлы с данным расширением в данной директории
    Params:
        directory -- директория, в которой рекурсивно ищем файлы
        extension -- расширение искомых файлов
    Returns:
    """
    return glob.glob(f"{directory}/*/*.{extension}", recursive=True)


def make_set_file_to_absolute_path(directory: str, extension: str) -> dict:
    """
    Создает словарь: filename -> absolute filename
    """
    all_files_in_directory = get_all_files_in_directory(directory, extension)
    file_to_absolute_path = {}
    for directory in all_files_in_directory:
        file_to_absolute_path[Path(directory).stem] = directory
    return file_to_absolute_path


def construct_filename_with_your_extension(filename: str, extension: str):
    """
    Params:
        filename -- абсолютный путь до файла
        ext -- конец файла вида "_kek.ogg"
    """
    parent_name = Path(filename).parent
    name = Path(filename).stem
    return f"{parent_name}/{name}{extension}"
