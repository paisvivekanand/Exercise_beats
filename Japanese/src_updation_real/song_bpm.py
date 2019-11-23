import librosa.display
import os
import configparser
import pickle
import math
import json
import pickle
import pygame
import numpy as np

conf_handler = configparser.ConfigParser()
conf_handler.read(r'/home/ubuntu/Desktop/backup/headphones/config/conf.ini')
song_resource = conf_handler.get('file_path', 'music_files')


def LoadDictionary(File):
    with open(File, "rb") as myFile:
        dict = pickle.load(myFile)
        print(dict)
        return dict


def SaveDictionary(dictionary, File):
    with open(File, "wb") as myFile:
        pickle.dump(dictionary, myFile)


def pickle_to_dict(song_resource):
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pickle_bpm = open("song_bpm.pickle", "rb")
    pickle_time = open("song_bpm_time.pickle", "rb")
    bpm_dict1 = pickle.load(pickle_bpm)
    time_dict = pickle.load(pickle_time)
    song_name_list = list(bpm_dict1.keys())

    j = 0
    count_dict = 1
    bpm_dict = {}
    print(song_name_list, j)
    while j < len(song_name_list):
        song = song_name_list[j]
        z = bpm_dict1[song]
        print(song, z)
        i = 1
        bpm_dict.update({count_dict: {'Song': song_name_list[j], 'BPM': math.ceil(z[0]), 'time': 0, 'played': 0, 'index': 0}})
        count_dict += 1
        while i < math.ceil(len(z)):
            if (abs(z[i] - z[i - 1] > 5)):
                bpm_dict.update({count_dict: {'Song': song_name_list[j], 'BPM': z[i],
                                              'time': time_dict[song_name_list[j]][i], 'played': 0, 'index': i}})
                count_dict += 1
            i += 1
        j += 1

    print(bpm_dict)
    SaveDictionary(bpm_dict, song_resource + 'song_bpm_time.pickle')


def generate_bpm_and_time_pickles():
    song_bpm_data = dict()
    song_bpm_time = dict()
    song_list = [f for f in os.listdir(song_resource) if f.endswith('.wav')]
    for f in song_list:
        print(f)
        song_name = os.path.join(song_resource, f)
        y, sr = librosa.load(song_name)
        onset_env = librosa.onset.onset_strength(y, sr=sr)
        dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
        times = librosa.frames_to_time(np.arange(len(onset_env)),
                                       sr=sr, hop_length=512)
        len1 = math.ceil(len(dtempo)-200)
        print(len1)
        song_bpm_time.update({f: times[:len1]})
        song_bpm_data.update({f: dtempo[:len1]})
    # print(librosa.core.get_duration(y, sr=sr))

    SaveDictionary(song_bpm_data, 'song_bpm.pickle')
    SaveDictionary(song_bpm_time, 'song_bpm_time.pickle')


generate_bpm_and_time_pickles()

pickle_to_dict(song_resource)
