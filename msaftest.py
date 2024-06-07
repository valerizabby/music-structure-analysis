# Simple MSAF example
from __future__ import print_function
import msaf

# 1. Select audio file
audio_file = "/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mp3"

# 2. Segment the file using the default MSAF parameters (this might take a few seconds)
boundaries, labels = msaf.process(audio_file)
print('Estimated boundaries:', boundaries)

# # 3. Save segments using the MIREX format
# out_file = 'segments.txt'
# print('Saving output to %s' % out_file)
# msaf.io.write_mirex(boundaries, labels, out_file)
#
# # 4. Evaluate the results
# try:
#     evals = msaf.eval.process(audio_file)
#     print(evals)
# except msaf.exceptions.NoReferencesError:
#     file_struct = msaf.input_output.FileStruct(audio_file)
#     print("No references found in {}. No evaluation performed.".format(
#         file_struct.ref_file))
