# *** Schubert Winterreise dataset ***
#
# This script loads measure annotations and audio for the first song D911-01
# in the performance by Huesch 1933 and cuts the audio to virtually restore the
# missing repetition, with the aim of achieving consistency with all other
# performances in the dataset
#
# Christof Weiss, AudioLabs Erlangen, 2019

import os
import numpy as np
import librosa
import csv
import pandas as pd
import soundfile as sf

path_data = 'HU33_originalShort_musopen'
path_ann_meas = os.path.join(path_data, 'ann_audio_measure')
path_audio = os.path.join(path_data, 'audio_wav_22050_mono')

path_output = 'HU33_Song01_WithRepetition'
file_name = 'Schubert_D911-01_HU33'

# Load measure annotations
df = pd.read_csv(os.path.join(path_ann_meas, file_name + '.csv') , sep=',', keep_default_na=False, header=None)
ann_meas_short = df.to_numpy()

# Load audio
x, Fs = librosa.load(os.path.join(path_audio, file_name + '.wav'))

# Calculate repeat points
repeat_first_meas = 7
repeat_last_meas = 38

repeat_start_seconds = ann_meas_short[repeat_first_meas-1, 0]
repeat_end_seconds = ann_meas_short[repeat_last_meas, 0]

repeat_start_samples = librosa.time_to_samples(repeat_start_seconds, sr=Fs)
repeat_end_samples = librosa.time_to_samples(repeat_end_seconds, sr=Fs)

x_long = np.concatenate((x[0:repeat_end_samples], x[repeat_start_samples:]))
sf.write(os.path.join(path_output, 'audio_wav', file_name + '.wav'), x_long, Fs)

offset = [repeat_end_seconds-repeat_start_seconds, repeat_last_meas-repeat_first_meas+1]
ann_meas_long = np.concatenate((ann_meas_short[0:repeat_last_meas], ann_meas_short[repeat_first_meas-1:] + offset))
np.savetxt(os.path.join(path_output, 'ann_audio_measure', file_name + '.csv'), ann_meas_long, delimiter=",", fmt='%.9f,%.1f')

print('Done! Version of first song by Huesch (1933) with inserted repetition written to folder '+str(path_output)+'.')
