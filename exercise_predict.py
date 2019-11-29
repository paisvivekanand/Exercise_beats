import pymysql
from keras.models import load_model
import numpy as np
import time


connection = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="headphones_demo",
    autocommit=True
)

def determine_exercise(model):
    acx = []
    acy = []
    acz = []
    gcx = []
    gcy = []
    gcz = []
    test_data = []
    cursor=connection.cursor()
    query='select acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z from android_sensors order by id desc limit 60'
    result= cursor.execute(query)
    records = cursor.fetchall()
    for row in records:
        acx.append(row[0])
        acy.append(row[1])
        acz.append(row[2])
        gcx.append(row[3])
        gcy.append(row[4])
        gcz.append(row[5])
    cursor.close()

    test_data.append([acx,acy,acz,gcx,gcy,gcz])
    test_data=np.asarray(test_data,dtype=np.float32).reshape(-1,60,6)
    x_test=test_data.reshape(test_data.shape[0],360)
    out=model.predict(x_test).argmax()
    return out

exercise={0:'cycling' , 1:'squats', 2:'standing'}
model=load_model('best_model_real.01-0.06.h5')
exercise_list=np.full(5,2)
counter=0
while True:
    exercise_list[counter]=determine_exercise(model)
    print(exercise[np.argmax(np.bincount(exercise_list))])
    cursor=connection.cursor()
    query="Update Song set exercise='"+exercise[np.argmax(np.bincount(exercise_list))]+"';"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    counter=(counter+1)%5
    time.sleep(0.5)
