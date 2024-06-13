from abc import ABC, abstractmethod


class Segmenter(ABC):

    def __init__(self):
        pass

    def fit(self, input_file: str):
        """
        Params:
            input_file -- абсолютный путь до файла
        """

    @abstractmethod
    def predict(self, input_file: str) -> list:
        """
        Params:
            input_file -- абсолютный путь до файла
        Returns:
            лист timestamps
        """
