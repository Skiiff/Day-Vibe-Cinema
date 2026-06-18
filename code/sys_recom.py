import sqlite3 as sql
import random

def result(current_user):
    from weather_check import weather
    from Data.Data_Organizer import get_events
    res = []
    with sql.connect("users.db") as udb:
        cur = udb.cursor()
        cur.execute("SELECT city FROM user WHERE id = ?",(current_user,))
        city = cur.fetchall()
        weather = weather(city[0][0])

    with sql.connect("Recom_Parameters.db") as weather_db:
        cursor = weather_db.cursor()
        res_weather = cursor.execute("SELECT genre FROM weather_genres WHERE weather_status = ?",(weather,))
        res_weather = res_weather.fetchall()

    a = res_weather[0][0].split(", ")

    b = get_events()
    i = random.randint(0, len(b) - 2)
    if b[-1] < 8:
        b = b[:-1]
        res.append(a[i])
        res.append(a[i-1])
        res.append(b[i])
    else:
        b = b[:-1]
        res.append(a[i])
        res.append(b[i])
        res.append(b[i-1]) 
    
    return res
