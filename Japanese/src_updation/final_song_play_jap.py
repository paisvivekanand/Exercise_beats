import math

import pymysql
import os
import configparser
import pickle
import pygame
import time
import numpy as np

from pydub import AudioSegment

mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="headphones_demo",
    autocommit=True
)
cursor = mydb.cursor()


def LoadDictionary(file):
    with open(file, "rb") as myFile:
        dict = pickle.load(myFile)
        print(dict)
        return dict


dir_name = os.path.join(__file__)
conf_handler = configparser.ConfigParser()
conf_handler.read('//home/ubuntu/Desktop/STEF/Japanese/config/conf.ini')
songsPath = conf_handler.get('file_path', 'music_files')
song_bpm_data = LoadDictionary(songsPath + 'song_bpm_time.pickle')


def db_initial_setup():
    cursor.execute("update Song set playing = 0")


def get_actual_name(song):
    if '/' in song:
        song = song.split('/')[-1]
    print(song)
    if song == 'Alan_Walker_Faded.wav':
        return 'Faded'
    elif song == 'Shape_of_you.wav':
        return 'Shape of You'
    elif song == 'Martin_Garrix_Animals.wav':
        return 'Animals'
    elif song == 'David_Guetta_Play_Hard.wav':
        return 'Play Hard'
    elif song == 'Fort_Minor.wav':
        return 'Fort Minor'
    elif song == 'This_Ones_For_You.wav':
        return "This One's For You"
    elif song == 'David_Guetta_Titanium.wav':
        return "Titanium"
    elif song == 'arashi_100.wav':
        return 'Arashi'
    elif song == 'Happiness_123.wav':
        return 'Happiness'
    elif song == 'Lemon_87.wav':
        return 'Lemon'
    elif song == 'Marigold_106.wav':
        return "Marigold"
    elif song == 'Radwimps_190.wav':
        return "Randwimps"
    elif song == 'Flamingo_120.wav':
        return "Flamingo"
    elif song == 'Loser_120.wav':
        return "Loser"
    elif song == 'Supercell_160.wav':
        return "Supercell"


def play_first_song(sound, dictionary):
    song = 'Lemon_87.wav'
    for index in dictionary:
        if dictionary[index]['Song'] == song:
            dictionary[index]['played'] = 1
    pulseRate = pulseRateMark = 50
    print("Initial pulse rate is:", pulseRate)
    curr_song = get_actual_name(song)
    query = 'update Song set playing = 1, average_bpm ='+ str(90)+', starting_point ='+str(0)+' where song_name = "'+curr_song+'"'
    cursor.execute(query)
    sound.play()
    time.sleep(30)
    print("Started first song. Sleeping for 10 seconds.")
    currsong = previous_song = song
    print("pulse rate mark for first song", pulseRateMark)
    return pulseRateMark, currsong, previous_song, sound


def is_end_of_song():
    if not pygame.mixer.get_busy():
        return True
    else:
        return False


def get_non_played_song(dictionary):
    song = None
    for index in dictionary:
        if dictionary[index]['played'] == 0:
            song = dictionary[index]['Song']
            print("Song which was unplayed was {}".format(song))
            break
    if song:
        for index in dictionary:
            if dictionary[index]['Song'] == song:
                dictionary[index]['played'] = 1
    return song


def update_in_db(prev_song, curr_song, bpm, index):
    print("Updating in db Previous Song: {} and current song: {}".format(prev_song, curr_song))
    curr_song = get_actual_name(curr_song)
    prev_song = get_actual_name(prev_song)
    cursor.execute('update Song set playing = 1, starting_point= "{}", average_bpm="{}" where song_name = "{}"'
                   .format(str(index), str(bpm), curr_song))
    cursor.execute('update Song set playing = 0 where song_name = "{}"'.format(prev_song))


def play_song(sound, sound2, start):
    sound2.set_volume(0)
    sound2.play()
    if not(start):
        for i in range(0, 4):
            vol1 = sound.get_volume()
            sound.set_volume(vol1 - 0.3)
            vol2 = sound2.get_volume()
            sound2.set_volume(vol2 + 0.3)
            print("v1: ", vol1, " v2: ", vol2)
            time.sleep(2)
    sound.set_volume(0)
    sound2.set_volume(1)
    time.sleep(10)
    return sound2, sound


def get_pulse_rate():
    cursor.execute('select heart_rate from current_heart_rate order by time desc')
    row = cursor.fetchone()
    try:
        print("Current heart rate is {}".format(int(row[0])))
        return int(row[0])
    except Exception as ex:
        return 50


def save_song_file(file_name, time_in_sec, new_file_name):
    sound = AudioSegment.from_wav(songsPath + file_name)
    partial_song = sound[time_in_sec * 1000:]
    partial_song.export(new_file_name, format="wav")


def Get_Song_Details(cur_bpm, dictionary):
    bpm_array = np.array([0])
    for index in dictionary:
        if dictionary[index]['played'] == 0:
            bpm_array = np.append(bpm_array, dictionary[index]['BPM'])
        else:
            bpm_array = np.append(bpm_array, 0)
    if not np.sum(bpm_array):
        return None, None, None, None, None
    minimum_val = np.argmin(np.abs(bpm_array - cur_bpm))
    song = dictionary[minimum_val]['Song']
    start_time = dictionary[minimum_val]['time']
    bpm = dictionary[minimum_val]['BPM']
    index_val = dictionary[minimum_val]['index']
    for index in dictionary:
        if dictionary[index]['Song'] == song:
            dictionary[index]['played'] = 1
    print("get song details:", dictionary)
    bpm_array = np.array([0])
    for index in dictionary:
        if dictionary[index]['played'] == 0:
            bpm_array = np.append(bpm_array, dictionary[index]['BPM'])
        else:
            bpm_array = np.append(bpm_array, 0)
    if not np.sum(bpm_array):
        last_song = 1
    else:
        last_song = 0
    return song, start_time, bpm, int(index_val/3), last_song


def final_play_jap():
    global song_bpm_data
    db_initial_setup()
    print(song_bpm_data)
    first_song = 1
    last_song = 0
    pygame.init()
    pulseRateMark = 0
    currsong = ''
    sound = None
    while True:
        cursor.execute("select status from controls where id=0")
        running_method = list(cursor.fetchall())[0][0]
        if running_method == 1:
            print("Running real time")
        else:
            print("Running stubbed.")
        cursor.execute("select running from sensor_status")
        running_status = list(cursor.fetchall())[0][0]
        if running_status:
            print("Running status is active from sensor_status table. So running the program.")
            if first_song:
                first_song = 0
                song_bpm_data = LoadDictionary(songsPath + 'song_bpm_time.pickle')
                sound = pygame.mixer.Sound(songsPath + 'Lemon_87.wav')
                pulseRateMark, currsong, previous_song, sound = play_first_song(sound, song_bpm_data)
            elif last_song:
                print("Playing the last song so waiting for no song change")
                if is_end_of_song():
                    cursor.execute("update sensor_status set running=0")
                    cursor.execute("update controls set status = 0")
                    print("All songs have been played so getting out now.")
            else:
                if is_end_of_song():
                    print("Current song ended. So switching to different song.")
                    previous_song = currsong
                    currsong = get_non_played_song(song_bpm_data)
                    if not currsong:
                        cursor.execute("update sensor_status set running=0")
                        cursor.execute("update controls set status = 0")
                        print("All songs have been played so getting out now.")
                        continue
                    update_in_db(previous_song, currsong, 0, 0)
                    sound2 = pygame.mixer.Sound(songsPath + currsong)
                    sound, sound2 = play_song(sound, sound2, 1)
                else:
                    print("waiting for heart rate {}".format(pulseRateMark))
                    time.sleep(1)
                    print("***************************")
                    pulseRate = get_pulse_rate()
                    if pulseRateMark < pulseRate:
                        pulseRateMark = math.floor(pulseRate+(pulseRate/20))
                        song, time_start, bpm, index, last_song = Get_Song_Details(pulseRate, song_bpm_data)
                        if not song:
                            print("All songs have been played so getting out now.")
                            continue
                        previous_song = currsong
                        currsong = song
                        print("Switching from {} to {}".format(previous_song, currsong))
                        print(song_bpm_data)
                        print("index: ", index)
                        update_in_db(previous_song, currsong, bpm, index)
                        print("switching to ", song, " Time: ", time_start)
                        save_song_file(song, time_start, "partial_song2.wav")
                        sound2 = pygame.mixer.Sound('partial_song2.wav')
                        sound, sound2 = play_song(sound, sound2, 0)
        else:
            print("Running status has stopped from sensor_status table. So stopping the program.")
            if sound is not None:
                sound.set_volume(0)
            print("Returning the control to main program")
            return
