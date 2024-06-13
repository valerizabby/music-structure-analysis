from abc import ABC


class AudioPeltInterface(ABC):
    def __init__(self):
        pass

    def fit(self, filename: str, signal):
        """
        Params:
            filename --
            signal --
        """

    def predict(self, filename: str) -> list:
        """
        Params:
            filename --
            signal --
        """
