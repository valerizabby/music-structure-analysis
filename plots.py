import numpy as np
import matplotlib.pyplot as plt

from os.path import  isfile
import logging as log

from SMSA.Dataparser import parse_txt, make_set_file_to_absolute_path, construct_filename_with_your_extension
from SMSA.audio_domain.ruptures.pelt import pelt
from SMSA.audio_domain.ruptures.utils.tempogram import tempo
from SMSA.utils.metrics import f1_score
from config import BPS_absolute_path

if __name__ == "__main__":
    data = np.array(parse_txt("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/tempo_len.txt"))
    # Plotting a basic histogram
    plt.hist(data, bins=30, color='skyblue', edgecolor='black')
    # Adding labels and title
    x1, y1 = [51600, 51600], [0, 3]
    plt.plot(x1, y1, color='red')
    plt.title('tempo shape distribution')
    # Display the plot
    plt.savefig('/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/tempo_distrib.png')

