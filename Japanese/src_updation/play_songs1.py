# runs on stubbed values

import pygame
import pymysql
import time
import os
import configparser
# from user_preferred_list import *
from pydub import AudioSegment
import pickle
import numpy as np
import src_updation.input_generator as g
import src_updation_real.input_generator as f
# import speech_recognition as sr
import math
mydb  = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="headphones_demo",
    autocommit=True
)



def LoadDictionary(File):
    with open(File, "rb") as myFile:
        dict = pickle.load(myFile)
        print(dict)
        return dict

dir_name = os.path.join(__file__)

conf_handler = configparser.ConfigParser()
# conf_handler.read(os.path.join(dir_name, '../config/conf.ini'))
conf_handler.read('/home/ubuntu/Desktop/STEF/Japanese/config/conf.ini')
pulseRateInputFile = conf_handler.get('file_path', 'pulse_rate_input')
songsPath = conf_handler.get('file_path', 'music_files')
song_bpm_data = LoadDictionary(songsPath + 'song_bpm_time.pickle')

#Real time Songs
def play_previous_song(previous_song, pulseRate, sound):
    print("play_previous_song:", previous_song)
    idx = (np.abs(song_bpm_data[previous_song] - pulseRate)).argmin()
    save_song_file(previous_song, idx, "partial_song3.wav")
    sound2 = pygame.mixer.Sound('partial_song3.wav')
    sound2.set_volume(0.1)
    sound2.play()
    for i in range(0, 4):
        vol1 = sound.get_volume()
        sound.set_volume(vol1 - 0.3)
        vol2 = sound2.get_volume()
        sound2.set_volume(vol2 + 0.3)
        print("v1: ", vol1, " v2: ", vol2)
        time.sleep(2)
    sound.set_volume(0)
    sound = sound2
    sound2.set_volume(0)
    sound.set_volume(1)
    return previous_song, sound


def Get_Song_Details(cur_bpm, dictionary):
    bpm_array = np.array([0])
    for index in dictionary:
        if (dictionary[index]['played'] == 0):

            bpm_array = np.append(bpm_array, dictionary[index]['BPM'])
        else:
            bpm_array = np.append(bpm_array, 0)
    if not np.sum(bpm_array):
        return None, None, None, None
    minimum_val = np.argmin(np.abs(bpm_array - cur_bpm))
    print("min val", minimum_val)
    song = dictionary[minimum_val]['Song']
    time = dictionary[minimum_val]['time']
    bpm = dictionary[minimum_val]['BPM']
    index_val = dictionary[minimum_val]['index']
    for index in dictionary:
        if (dictionary[index]['Song'] == song):
            dictionary[index]['played'] = 1
    print("get song details:", dictionary)
    return song, time, bpm, int(index_val/3)


def play_next_song(pulseRate, currsong, sound):
    song, index = get_song_detals(pulseRate, currsong)
    print("play_next_song: ", song)
    index = int(index)
    save_song_file(song, index, "partial_song3.wav")
    sound2 = pygame.mixer.Sound('partial_song3.wav')
    sound2.set_volume(0)
    sound2.play()
    for i in range(0, 4):
        vol1 = sound.get_volume()
        sound.set_volume(vol1 - 0.3)
        vol2 = sound2.get_volume()
        sound2.set_volume(vol2 + 0.3)
        print("v1: ", vol1, " v2: ", vol2)
        time.sleep(2)
    sound.set_volume(0)
    sound = sound2
    sound2.set_volume(0)
    sound.set_volume(1)
    return song, sound


def get_song_detals(currbpm, currsong=None):
    song_list = [*song_bpm_data]
    index_list = np.array([])
    bpm_list = np.array([])
    if currsong is None:
        for song in song_list:
            dtempo = song_bpm_data[song]
            idx = (np.abs(song_bpm_data[song] - currbpm)).argmin()
            index_list = np.append(index_list, [idx])
            bpm_list = np.append(bpm_list, [dtempo[idx]])
        idx1 = (np.abs(bpm_list - currbpm)).argmin()
        song = song_list[idx1]
        index = index_list[idx1]
    else:
        i = song_list.index(currsong)
        del song_list[i]
        print("deleted")
        print(song_list)
        for song in song_list:
            dtempo = song_bpm_data[song]
            idx = (np.abs(song_bpm_data[song] - currbpm)).argmin()
            index_list = np.append(index_list, [idx])
            bpm_list = np.append(bpm_list, [dtempo[idx]])
        idx1 = (np.abs(bpm_list - currbpm)).argmin()
        song = song_list[idx1]
        index = index_list[idx1]
    return song, index


def save_song_file(file_name, time_in_sec, new_file_name):
    sound = AudioSegment.from_wav(songsPath + file_name)
    partial_song = sound[time_in_sec * 1000:]
    partial_song.export(new_file_name, format="wav")





def play_first_song(sound, dictionary):
    song = 'Lemon.wav'
    for index in dictionary:
        if (dictionary[index]['Song'] == song):
            dictionary[index]['played'] = 1
    pulseRate = pulseRateMark = g.get_pulse_rate()
    # pulseRate = pulseRateMark = get_pulse_rate_initial()

    print("pulse rate:", pulseRate)
    # song, time_start, bpm, index = Get_Song_Details(pulseRate, song_bpm_data)
    # save_song_file(song, time_start, "partial_song1.wav")
    g.update_in_db_initial(song, 90, 0)
    # sound = pygame.mixer.Sound('partial_song1.wav')
    sound.play()
    time.sleep(10)
    currsong = previous_song = song
    print("pulse rate mark", pulseRateMark)
    return pulseRateMark, currsong, previous_song, sound


def play_song(sound, sound2):
    # sound2.set_volume(0)
    # sound2.play()
    # print("transition beginning:", sound.get_volume(),"   ", sound2.get_volume())
    # time.sleep(7)
    # print("will start now")
    # for i in range(0, 4):
    #     vol1 = sound.get_volume()
    #     sound.set_volume(vol1 - 0.3)
    #     vol2 = sound2.get_volume()
    #     sound2.set_volume(vol2 + 0.3)
    #     print("v1: ", vol1, " v2: ", vol2)
    #     time.sleep(2)
    #
    # sound.set_volume(0)
    # print(" sound stopped")
    # print(sound.get_volume(), sound2.get_volume())
    # sound = sound2
    # sound2.set_volume(0)
    # sound.set_volume(1)
    # time.sleep(3)
    sound2.set_volume(0)
    sound2.play()
    for i in range(0, 4):
        vol1 = sound.get_volume()
        sound.set_volume(vol1 - 0.3)
        vol2 = sound2.get_volume()
        sound2.set_volume(vol2 + 0.3)
        print("v1: ", vol1, " v2: ", vol2)
        time.sleep(5)
    sound.set_volume(0)
    sound = sound2
    sound2.set_volume(0)
    sound.set_volume(1)
    return sound, sound2


def get_non_played_song(dictionary):
    # backup song = This_Ones_For_You
    song = None
    for index in dictionary:
        if (dictionary[index]['played'] == 0):
            print(index)
            print(dictionary[index])
            song = dictionary[index]['Song']
            dictionary[index]['played'] = 1
            break
    if song:
        for index in dictionary:
            if (dictionary[index]['Song'] == song):
                dictionary[index]['played'] = 1
    return song


def is_end_of_song():
    if not pygame.mixer.get_busy():
        return True
    else:
        return False
############Real Time songs ended

#######################Stub Time songs
def play_previous_song1(previous_song, pulseRate, sound):
    print("play_previous_song:", previous_song)
    idx = (np.abs(song_bpm_data[previous_song] - pulseRate)).argmin()
    save_song_file(previous_song, idx, "partial_song3.wav")
    sound2 = pygame.mixer.Sound('partial_song3.wav')
    sound2.set_volume(0.1)
    sound2.play()
    for i in range(0, 4):
        vol1 = sound.get_volume()
        sound.set_volume(vol1 - 0.3)
        vol2 = sound2.get_volume()
        sound2.set_volume(vol2 + 0.3)
        print("v1: ", vol1, " v2: ", vol2)
        time.sleep(2)
    sound.set_volume(0)
    sound = sound2
    sound2.set_volume(0)
    sound.set_volume(1)
    return previous_song, sound



def play_next_song1(pulseRate, currsong, sound):
    song, index = get_song_detals1(pulseRate, currsong)
    print("play_next_song: ", song)
    index = int(index)
    save_song_file(song, index, "partial_song3.wav")
    sound2 = pygame.mixer.Sound('partial_song3.wav')
    sound2.set_volume(0)
    sound2.play()
    for i in range(0, 4):
        vol1 = sound.get_volume()
        sound.set_volume(vol1 - 0.3)
        vol2 = sound2.get_volume()
        sound2.set_volume(vol2 + 0.3)
        print("v1: ", vol1, " v2: ", vol2)
        time.sleep(2)
    sound.set_volume(0)
    sound = sound2
    sound2.set_volume(0)
    sound.set_volume(1)
    return song, sound


def get_song_detals1(currbpm, currsong=None):
    song_list = [*song_bpm_data]
    index_list = np.array([])
    bpm_list = np.array([])
    if currsong is None:
        for song in song_list:
            dtempo = song_bpm_data[song]
            idx = (np.abs(song_bpm_data[song] - currbpm)).argmin()
            index_list = np.append(index_list, [idx])
            bpm_list = np.append(bpm_list, [dtempo[idx]])
        idx1 = (np.abs(bpm_list - currbpm)).argmin()
        song = song_list[idx1]
        index = index_list[idx1]
    else:
        i = song_list.index(currsong)
        del song_list[i]
        print("deleted")
        print(song_list)
        for song in song_list:
            dtempo = song_bpm_data[song]
            idx = (np.abs(song_bpm_data[song] - currbpm)).argmin()
            index_list = np.append(index_list, [idx])
            bpm_list = np.append(bpm_list, [dtempo[idx]])
        idx1 = (np.abs(bpm_list - currbpm)).argmin()
        song = song_list[idx1]
        index = index_list[idx1]
    return song, index



def LoadDictionary(File):
    with open(File, "rb") as myFile:
        dict = pickle.load(myFile)
        print(dict)
        return dict


def play_first_song(sound, dictionary):
    song = 'Lemon_87.wav'
    for index in dictionary:
        if (dictionary[index]['Song'] == song):
            dictionary[index]['played'] = 1
    # pulseRate = pulseRateMark = get_pulse_rate()
    pulseRate = pulseRateMark = g.get_pulse_rate_initial()

    print("pulse rate:", pulseRate)
    # song, time_start, bpm, index = Get_Song_Details(pulseRate, song_bpm_data)
    # save_song_file(song, time_start, "partial_song1.wav")
    g.update_in_db_initial(song, 90, 0)
    # sound = pygame.mixer.Sound('partial_song1.wav')
    sound.play()
    time.sleep(10)
    currsong = previous_song = song
    print("pulse rate mark", pulseRateMark)
    return pulseRateMark, currsong, previous_song, sound


def play_song1(sound, sound2):
    # sound2.set_volume(0)
    # sound2.play()
    # print("transition beginning:", sound.get_volume(),"   ", sound2.get_volume())
    # time.sleep(7)
    # print("will start now")
    # for i in range(0, 4):
    #     vol1 = sound.get_volume()
    #     sound.set_volume(vol1 - 0.3)
    #     vol2 = sound2.get_volume()
    #     sound2.set_volume(vol2 + 0.3)
    #     print("v1: ", vol1, " v2: ", vol2)
    #     time.sleep(2)
    #
    # sound.set_volume(0)
    # print(" sound stopped")
    # print(sound.get_volume(), sound2.get_volume())
    # sound = sound2
    # sound2.set_volume(0)
    # sound.set_volume(1)
    # time.sleep(3)
    sound2.set_volume(0)
    sound2.play()
    for i in range(0, 4):
        vol1 = sound.get_volume()
        sound.set_volume(vol1 - 0.3)
        vol2 = sound2.get_volume()
        sound2.set_volume(vol2 + 0.3)
        print("v1: ", vol1, " v2: ", vol2)
        time.sleep(5)
    sound.set_volume(0)
    sound = sound2
    sound2.set_volume(0)
    sound.set_volume(1)
    return sound, sound2


sound=""
#############################Stub songs ended
#if __name__ == '__main__':
def trial_play_main_jap():
    f.db_initial_setup()
    global pulseRateInputFile
    global songsPath
    global song_bpm_data
    print(song_bpm_data)
    first_song = 1
    pygame.init()
    pulseRateMark = 0
    currsong = ''
    start_time =  time.time()
    sound=None
    mycursor = mydb.cursor()
    mycursor.execute("select status from controls where id=0")
    myresult = list(mycursor.fetchall())[0][0]
    while True:
        if myresult==2:
            print("Running stubbed")
            status = g.get_sensor_status()
            print(status)
            print("This is status")
            count_for_pulseRateMark = 0
            if status == 1:
                if first_song == 1:
                    # pulseRateMark = 0
                    sound = pygame.mixer.Sound(songsPath + 'Lemon_87.wav')
                    pulseRateMark, currsong, previous_song, sound = play_first_song(sound, song_bpm_data)
                    first_song = 0

                else:
                    print(is_end_of_song())
                    if is_end_of_song():
                        print("end of song")
                        previous_song = currsong
                        song = get_non_played_song(song_bpm_data)
                        if not song:
                            mycursor.execute("Update sensor_status set running=0")
                            continue
                        currsong = song
                        if 'bpm' in locals():
                            f.update_in_db(previous_song, currsong, bpm, 0)
                        else:
                            f.update_in_db(previous_song, currsong, 0, 0)
                        sound2 = pygame.mixer.Sound(songsPath + song)
                        sound, sound2 = play_song1(sound, sound2)
                    print("waiting for", math.floor(pulseRateMark + pulseRateMark / 20))
                    time.sleep(10)
                    print("***************************")
                    present_duration = time.time()- start_time
                    print(present_duration)
                    print("calling get pulse rate")
                    # pulseRate = get_pulse_rate()
                    pulseRate = g.get_pulse_rate(present_duration)
                    print(pulseRateMark)
                    print("now", pulseRate)
                    if pulseRateMark < pulseRate:
                        if abs(pulseRateMark - pulseRate) < math.floor(pulseRateMark / 20):
                            count_for_pulseRateMark = count_for_pulseRateMark + 0.5
                        else:
                            count_for_pulseRateMark = 0
                            pulseRateMark = pulseRate
                            previous_song = currsong
                            song, time_start, bpm, index = Get_Song_Details(pulseRate, song_bpm_data)
                            if not song:
                                mycursor.execute("Update sensor_status set running=0")
                                continue
                            currsong = song
                            print("switchng from ", previous_song, " to ", currsong)
                            print(song_bpm_data)
                            print("index: ", index)
                            f.update_in_db(previous_song, currsong, bpm, index)
                            print("switching to ", song, " Time: ", time_start)
                            save_song_file(song, time_start, "partial_song2.wav")
                            sound2 = pygame.mixer.Sound('partial_song2.wav')
                            sound, sound2 = play_song1(sound, sound2)
            else:
                if sound is not None:
                    sound.set_volume(0)
                time.sleep(5)
                first_song = 1
                pygame.init()
                pulseRateMark = 0
                currsong = ''
                start_time = time.time()
                return

        else:
            print("Running real time")
            status = f.get_sensor_status()
            print(status)
            print("This is status")
            count_for_pulseRateMark = 0
            if status == 1:
                if first_song == 1:
                    # pulseRateMark = 0
                    sound = pygame.mixer.Sound(songsPath + 'Lemon_87.wav')
                    pulseRateMark, currsong, previous_song, sound = play_first_song(sound, song_bpm_data)
                    first_song = 0

                else:
                    print(is_end_of_song())
                    if is_end_of_song():
                        print("end of song")
                        previous_song = currsong
                        song = get_non_played_song(song_bpm_data)
                        if not song:
                            mycursor.execute("update sensor_status set running=0")
                            print("All songs have been played so getting out now.")
                            continue
                        currsong = song
                        if 'bpm' in locals():
                            g.update_in_db(previous_song, currsong, bpm, 0)
                        else:
                            g.update_in_db(previous_song, currsong, 0, 0)
                        sound2 = pygame.mixer.Sound(songsPath + song)
                        sound, sound2 = play_song(sound, sound2)
                    print("waiting for", math.floor(pulseRateMark + pulseRateMark / 20))
                    time.sleep(10)
                    print("***************************")
                    present_duration = time.time() - start_time
                    print(present_duration)
                    print("calling get pulse rate")
                    pulseRate = f.get_pulse_rate()
                    # pulseRate = get_pulse_rate(present_duration)
                    print(pulseRateMark)
                    print("now", pulseRate)
                    if pulseRateMark < pulseRate:
                        if abs(pulseRateMark - pulseRate) < math.floor(pulseRateMark / 20):
                            count_for_pulseRateMark = count_for_pulseRateMark + 0.5
                        else:
                            count_for_pulseRateMark = 0
                            pulseRateMark = pulseRate
                            previous_song = currsong
                            song, time_start, bpm, index = Get_Song_Details(pulseRate, song_bpm_data)
                            if not song:
                                mycursor.execute("update sensor_status set running=0")
                                print("All songs have been played so getting out now.")
                                continue
                            currsong = song
                            print("switchng from ", previous_song, " to ", currsong)
                            print(song_bpm_data)
                            print("index: ", index)
                            g.update_in_db(previous_song, currsong, bpm, index)
                            print("switching to ", song, " Time: ", time_start)
                            save_song_file(song, time_start, "partial_song2.wav")
                            sound2 = pygame.mixer.Sound('partial_song2.wav')
                            sound, sound2 = play_song(sound, sound2)
            else:
                if sound is not None:
                    sound.set_volume(0)
                time.sleep(5)
                first_song = 1
                pygame.init()
                pulseRateMark = 0
                currsong = ''
                start_time = time.time()
                return
        mycursor = mydb.cursor()
        mycursor.execute("select status from controls where id=0")
        myresult = list(mycursor.fetchall())[0][0]