import librosa
import librosa.display
import matplotlib.pyplot as plt


def show_waveform(filename):
    """
    Возвращает картинку с аудио волной
    """
    x, sr = librosa.load(filename)
    plt.figure(figsize=(15, 5))
    librosa.display.waveshow(x, alpha=0.8)
    plt.savefig('1-waveform.png')

if __name__ == "__main__":
    show_waveform('/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.wav')
