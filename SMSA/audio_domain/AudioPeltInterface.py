from abc import ABC


class AudioPeltInterface(ABC):
    def __init__(self):
        pass

    def fit(self, filename, signal):
        """
        Params:
            filename --
            signal --
        """

    def predict(self, filename):
        """
        Params:
            filename --
            signal --
        """
