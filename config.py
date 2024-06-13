from pathlib import Path

# routes
CONTENT_ROOT = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/"
RUSSIAN_POP_ABSOLUTE_PATH = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/RussianPop/"
dataset = Path("/BPS_FH_Dataset")
BPS_absolute_path = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/data/BPS_FH_Dataset/"

# kernelCPD settings
n_bkps_max = 20  # K_max
hop_length_tempo = 256


penalty = 5
min_size = 2100
jump = 8
