import sqlite3 as sql
def register_user(username, city):
    with sql.connect("users.db") as udb:
        curs = udb.cursor()
        try:
            curs.execute("INSERT INTO user(username, city) VALUES(?, ?)",(username ,city))
            udb.commit()
            print(f"Пользователь: {username} зарегестрирован.")        
        except:
            print(f"Не удалось зарегестрировать пользователя: {username}")

def authorisation(username):
    with sql.connect("users.db") as udb:
        curs = udb.cursor()
        curs.execute("SELECT city FROM user WHERE username = ?",(username,))
        row = curs.fetchall()
        curs.execute("SELECT id FROM user WHERE username = ?",(username,))
        id = curs.fetchall()
    
    try:
        if id != []:
            print("Авторизация прошла успешно")
            return id[0][0],row
        else:
            print("Неверное имя пользователя.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
