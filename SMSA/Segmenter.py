from abc import ABC, abstractmethod


class Segmenter(ABC):


    @abstractmethod
    def predict(self, input_file) -> list:
        """
        Params:
            input_file -- абсолютный путь до файла
        Returns:
            лист timestamps
        """
