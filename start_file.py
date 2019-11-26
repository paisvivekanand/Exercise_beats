from Japanese.src_updation.play_songs1 import trial_play_main_jap
from English.src_updation.play_songs1 import trial_play_main_eng
import Japanese.src_updation.play_songs1
import English.src_updation.play_songs1

import pymysql

mydb  = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="headphones_demo",
    autocommit=True
)

if __name__=='__main__':
    mycursor = mydb.cursor()
    mycursor.execute("select language from controls where id=0")
    value = list(mycursor.fetchall())[0][0]
    while True:
        mycursor.execute("select language from controls where id=0")
        value = list(mycursor.fetchall())[0][0]
        if value == 1:
            trial_play_main_eng()
        elif value == 2:
            trial_play_main_jap()
        else:
            print("No language selected")
            continue
