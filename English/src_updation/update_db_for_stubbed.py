import pymysql
from time import sleep


mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="headphones_demo",
    autocommit=True
)

stubbed_value = [62,66,67,64,70,71,71,71,71,71,71,75,76,77,78,79,77,76,75,73,72,71,71,72,72,73,75,77,79,80,80,80,80,80,80,82,82,82,79,80,80,84,88,90,91,92,93,94,95,90,87,86,85,92,100,107,108,109,105,101,99,96,96,96,96,96,97,114,114,113,110,119,119,119,119,118,118,118,118,118,118,117,117,115,115,114,114,116,117,118,119,127,129,130,138,142,143,144,145,145,144,143,143,143,148,150,150,150,150,150,150,150,155,140,140,140,140,140,140,139,138,137,136,135,130,130,131,133,132,129,130,135,138,140,141,142,146,148,140,139,137,135,133,133,133,130,130,130,129,125,122,121,120,120,120,120,119,119,115,133,133,133,130,130,130,129,125,122,121,120,120,120,120,119,119,115,133,133,133,130,130,130,129,125,122,121,120,120,120,120,119,119,115,133,133,133,130,130,130,129,125,122,121,120,120,120,120,119,119,115,133,133,133,130,130,130,129,125,122,121,120,120,120,120,119,119,115]

mycursor = mydb.cursor()
mycursor.execute("select status from controls where id=0")
control = list(mycursor.fetchall())[0][0]
i=0
while True:
    if control == 2:
        print("Running stubbed> entering values to db.")
        try:
            value = stubbed_value[i]
            query = 'insert into current_heart_rate(heart_rate) values({0})'
            mycursor.execute(query.format(value))
            mydb.commit()
            sleep(1)
            i += 1
        except IndexError as ind:
            i = 0
    else:
        print("Running real time")
        i = 0
    mycursor.execute("select status from controls where id=0")
    control = list(mycursor.fetchall())[0][0]
