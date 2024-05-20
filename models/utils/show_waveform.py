import librosa
import librosa.display
import matplotlib.pyplot as plt
from config import CONTENT_ROOT


def show_waveform(filename):
    """
    Возвращает картинку с аудио волной
    """
    x, sr = librosa.load(filename)
    plt.figure(figsize=(15, 5))
    librosa.display.waveshow(x, alpha=0.8)
    plt.savefig(f"{CONTENT_ROOT}data/1-waveform.png")

if __name__ == "__main__":
    filename = '/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.wav'
    y, sr = librosa.load(filename, duration=401)
    fig, ax = plt.subplots()
    librosa.display.waveshow(y, sr=sr, ax=ax, color='deepskyblue')
    ax.set(title='Envelope view for 1 Beethoven sonata')
    ax.label_outer()
    plt.savefig(f"{CONTENT_ROOT}data/1-waveform.png")
