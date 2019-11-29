import pymysql
from English.src_updation.final_song_play_eng import final_play_eng
from Japanese.src_updation.final_song_play_jap import final_play_jap

mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="headphones_demo",
    autocommit=True
)

if __name__=='__main__':
    mycursor = mydb.cursor()
    language = 0
    status = 0
    while True:
        if status:
            mycursor.execute("select language from controls where id=0")
            language = list(mycursor.fetchall())[0][0]
            if language == 1:
                final_play_eng()
            elif language == 2:
                final_play_jap()
        print("No language selected")
        mycursor.execute("select running from sensor_status")
        status = list(mycursor.fetchall())[0][0]
