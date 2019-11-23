import configparser
import os
import random
import time
import pymysql

dir_name = os.path.join(__file__)
conf_handler = configparser.ConfigParser()
# conf_handler.read(os.path.join(dir_name, '../config/conf.ini'))
conf_handler.read(r'/home/ubuntu/Desktop/backup/headphones/config/conf.ini')
pulse_rate_input_file = conf_handler.get('file_path', 'pulse_rate_input')
host = conf_handler.get('database', 'host')
username = conf_handler.get('database', 'username')
password = conf_handler.get('database', 'password')
db_name = conf_handler.get('database', 'database_name')
port = int(conf_handler.get('database', 'port'))
connection = pymysql.connect(host, username, None, db_name, port=port)
# user_id = 100
# query = "insert into sensor_data(user_id,pulse_rate) values({0},{1})"
# cursor = connection.cursor()
# while True:
#     number = random.randint(80, 139)
#     print(number)
#     cursor.execute(query.format(str(user_id), str(number)))
#     connection.commit()
#     with open(pulse_rate_input_file, "w") as f:
#         f.write(str(number))
#     time.sleep(25)
#
# connection.close()


# def get_pulse_rate():
#     connection = pymysql.connect(host, username, None, db_name)
#     cursor = connection.cursor()
#     query = 'select heart_rate from current_heart_rate order by time desc'
#     cursor.execute(query)
#     row = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     print(int(row[0]))
#     return int(row[0])

def get_pulse_rate_initial():
    num = random.randint(50,80)
    print("*****", num)
    connection = pymysql.connect(host, username, None, db_name, port = port)
    cursor = connection.cursor()
    query = 'insert into current_heart_rate(heart_rate) values({0})'
    cursor.execute(query.format(num))
    connection.commit()
    cursor.close()
    connection.close()
    return num

def get_pulse_rate(present_duration):
    if present_duration< 100:
        num = random.randint(50,110)
    elif ((present_duration >= 100) and (present_duration< 200)):
        num = random.randint(110, 145)
    elif present_duration >= 200:
        num = random.randint(145, 170)
    print("*****", num)
    connection = pymysql.connect(host, username, None, db_name, port = port)
    cursor = connection.cursor()
    query = 'insert into current_heart_rate(heart_rate) values({0})'
    cursor.execute(query.format(num))
    connection.commit()
    cursor.close()
    connection.close()
    return num


def get_sensor_status():
    connection = pymysql.connect(host, username, None, db_name, port = port)
    cursor = connection.cursor()
    query = 'select running from sensor_status'
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    print(int(row[0]))
    return int(row[0])


def get_actulal_name(song):
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


def db_initial_setup():
    query = "update Song set playing = 0"
    connection = pymysql.connect(host, username, None, db_name, port=port)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


def update_in_db(prev_song, curr_song, bpm, index):
    # curr_song = get_actulal_name(curr_song)
    print(curr_song, prev_song)
    # query_curr_prev = 'update Song set playing = 1 where song_name = "' + curr_song+'" ,playing = 0 where song_name = "' + prev_song+'"'
    # prev_song = get_actulal_name(prev_song)
    # print("prev_song", prev_song)
    # print("curr_song", curr_song)
    # print(curr_song, prev_song)
    # connection = pymysql.connect(host, username, None, db_name)
    # cursor = connection.cursor()
    # cursor.execute(query_curr_prev)
    # query_curr='update Song set average_bpm = %s , starting_point =%s where song_name = "' + curr_song+'"'
    # input=(int(bpm), index)
    # print(query_curr, input)
    # cursor.execute(query_curr, input)
    # connection.commit()
    # cursor.close()
    # connection.close()
    curr_song = get_actulal_name(curr_song)
    query_curr = 'update Song set playing = 1, starting_point= "'+str(index) +'", average_bpm="'+str(int(bpm))+'" where song_name = "' + curr_song+'"'
    prev_song = get_actulal_name(prev_song)
    print("prev_song", prev_song)
    print("curr_song", curr_song)
    print(curr_song, prev_song)
    query_prev = 'update Song set playing = 0 where song_name = "' + prev_song+'"'
    connection = pymysql.connect(host, username, None, db_name, port = port)
    cursor = connection.cursor()
    cursor.execute(query_prev)
    cursor.execute(query_curr)
    connection.commit()
    cursor.close()
    connection.close()



def update_in_db_initial(curr_song, bpm, index):
    curr_song = get_actulal_name(curr_song)
    query_curr = 'update Song set playing = 1 where song_name = "' + curr_song+'"'
    print(query_curr)
    connection = pymysql.connect(host, username, None, db_name, port = port)
    cursor = connection.cursor()
    cursor.execute(query_curr)
    query_curr='update Song set average_bpm = %s , starting_point =%s where song_name = "' + curr_song+'"'
    input=(int(bpm), index)
    print(query_curr, input)
    cursor.execute(query_curr, input)
    connection.commit()
    cursor.close()
    connection.close()


# get_pulse_rate()