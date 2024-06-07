from abc import ABC, abstractmethod


class Segmenter(ABC):

    def __init__(self):
        pass

    def fit(self):
        pass

    @abstractmethod
    def predict(self, input_file) -> list:
        """
        Params:
            input_file -- абсолютный путь до файла
        Returns:
            лист timestamps
        """
