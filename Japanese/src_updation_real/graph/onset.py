import librosa
import numpy as np

# Compute local onset autocorrelation
y, sr = librosa.load(librosa.util.example_audio_file())
hop_length = 512
oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)

times = librosa.frames_to_time(np.arange(len(oenv)),
                               sr=sr, hop_length=hop_length)
print(np.ediff1d(times))

lent=librosa.get_duration(y=y, sr=sr)
samples_per_sec = (len(times)/lent)

import json
oenv1 = oenv.tolist()

data_points_d = {
    'song1': oenv1
}

data = json.dumps(data_points_d)
# with open('data_points.json', 'w') as outfile:
#     json.dump(data, outfile, ensure_ascii=False)

import numpy as np
import codecs, json

file_path = "path.json" ## your path variable
json.dump(data, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format



















# # Compute local onset autocorrelation
# y, sr = librosa.load(librosa.util.example_audio_file())
# hop_length = 512
# oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
# print(oenv)
# print(max(oenv))
# print(len(oenv))
#
# times = librosa.frames_to_time(np.arange(len(oenv)),
#                                sr=sr, hop_length=hop_length)
# print(times)
# print(np.ediff1d(times))
# print(len(times))
#
# lent=librosa.get_duration(y=y, sr=sr)
# samples_per_sec = (len(times)/lent)
# print()
#
#
# tempogram = librosa.feature.tempogram(onset_envelope=oenv, sr=sr,
#                                     hop_length=hop_length)
# print(tempogram)
# print(len(tempogram))
# # Compute global onset autocorrelation
# ac_global = librosa.autocorrelate(oenv, max_size=tempogram.shape[0])
# ac_global = librosa.util.normalize(ac_global)
# # Estimate the global tempo for display purposes
# tempo = librosa.beat.tempo(onset_envelope=oenv, sr=sr,
#                        hop_length=hop_length)[0]
# print(tempo)


