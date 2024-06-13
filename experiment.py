from SMSA.audio_domain.AudioPelt import AudioPelt
from SMSA.symbolic_domain.SymbolicPelt import SymbolicPelt
from SMSA.Dataparser import make_set_file_to_absolute_path, construct_filename_with_your_extension
from config import RUSSIAN_POP_ABSOLUTE_PATH, BPS_absolute_path
import logging as log


def dataset_bypass(dataset_abs_path, algo, input_ext, output_ext, to_save=True):
    """
        dataset_abs_path -- абсолютный путь до датасета
        algo -- алгоритм, у которого определен метод predict
        input_ext -- расширение входных аудио файлов
        output_ext -- название, куда сохраняем ответы
        to_save -- сохранять предсказания или нет (по умолчанию true)
    """
    filename_to_absolute_file = make_set_file_to_absolute_path(dataset_abs_path, input_ext)
    for filename in filename_to_absolute_file:
        name = filename_to_absolute_file[filename]
        log.info(f"Working with {name}")
        current_prediction_in_secs = algo.predict(name)
        print(current_prediction_in_secs)
        if to_save:
            with open(construct_filename_with_your_extension(name, output_ext), 'w') as f:
                for bound in current_prediction_in_secs:
                    f.write(str(bound) + "\n")



if __name__ == "__main__":
    # EXPERIMENT 1
    # dataset_bypass(dataset_abs_path=RUSSIAN_POP_ABSOLUTE_PATH,
    #                algo=SymbolicPelt(),
    #                input_ext="mid",
    #                output_ext="_symbolic_pred.txt")

    # EXPERIMENT 2
    # dataset_bypass(dataset_abs_path=RUSSIAN_POP_ABSOLUTE_PATH,
    #                algo=AudioPelt(algo="kernel", mode="gt"),
    #                input_ext="mp3",
    #                output_ext="_ruptures_pred.txt")

    # EXPERIMENT 3
    # dataset_bypass(dataset_abs_path=RUSSIAN_POP_ABSOLUTE_PATH,
    #                algo=AudioPelt(algo="kernel", mode="hard"),
    #                input_ext="mp3",
    #                output_ext="_ruptures_pred_8.txt")

    # EXPERIMENT 4
    # dataset_bypass(dataset_abs_path=BPS_absolute_path,
    #                algo=AudioPelt(algo="pelt"),
    #                input_ext="mp3",
    #                output_ext="_pelt_pred.txt")

    dataset_bypass(dataset_abs_path=RUSSIAN_POP_ABSOLUTE_PATH,
                       algo=AudioPelt(algo="pelt"),
                       input_ext="mp3",
                       output_ext="_pelt_pred.txt")
