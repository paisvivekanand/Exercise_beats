import json
import librosa, os, pickle, codecs
import numpy as np

def SaveDictionary(dictionary, File):
    with open(File, "wb") as myFile:
        pickle.dump(dictionary, myFile)

path1= '/home/ubuntu/headphones/resource/'
song_list = [f for f in os.listdir(path1) if f.endswith('.wav')]
song_bpm_data = dict()
for f in song_list:
    song_bpm_data = dict()
    song_time_data = dict()
    print(f)
    y, sr = librosa.load(path1 + f)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    # dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
    # print(len(dtempo))
    song_bpm_data.update({f: list(onset_env[::3])})
    print(song_bpm_data)
    print(len(list(onset_env[::3])))
    data = json.dumps((song_bpm_data))
    file_path = f[:-4]+".json" ## your path variable
    print(file_path)
    json.dump(data, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
    times = librosa.frames_to_time(np.arange(len(onset_env)),
                                   sr=sr, hop_length=512)
    song_time_data.update({f: list(times[::3])})
    data_time = json.dumps(song_time_data)
    file_path_t = 'time_json/'+f[:-4] + "_time.json"  ## your path variable
    print(file_path_t)
    json.dump(data_time, codecs.open(file_path_t, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)


