import sqlite3 as sql
from sys_auth import register_user, authorisation
from sys_recom import result
import os
import subprocess
import sys

db_path = "imdb.db"
def usermenu(username):
    while(1):
        print("_" * 68)
        print(f"Вы вошли как: {username}")
        print("Выбирете действие:")
        print("1. Рекомендация.","2. История.","3. Возврат на прошлое окно.",sep = "\n")
        func = input()
        print("_" * 68)
        if func == "1":
            print("Ожидайте...")
            connuser = sql.connect("users.db")
            curuser = connuser.cursor()
            connimdb = sql.connect("imdb.db")
            curimdb =  connimdb.cursor()
            curimdb.execute("ATTACH DATABASE 'users.db' AS users")
            conditions = " OR ".join(
                ["titles.genres LIKE ?" for _ in genres]
            )
            query = f"""
            SELECT titles.title_id
            FROM titles
            JOIN ratings 
            ON titles.title_id = ratings.title_id
            JOIN akas
            ON titles.title_id = akas.title_id
            WHERE ({conditions})
            AND titles.title_id NOT IN(
                SELECT movie_id
                FROM users.vieved
                WHERE user_id = ?
            ) 
            AND (type = 'movie' OR type = 'tvSeries' OR type = 'tvMovie')
            AND akas.region = 'RU'
            ORDER BY ratings.rating DESC, ratings.votes DESC
            LIMIT 1
            """

            params = [f"%{genre}%" for genre in genres]
            params.append(current_user[0])

            res = curimdb.execute(query, params).fetchall()
            name = curimdb.execute(
                """
                SELECT title
                FROM akas
                WHERE title_id = ?
                ORDER BY
                    CASE region
                        WHEN 'RU' THEN 1
                        WHEN 'US' THEN 2
                        ELSE 3
                    END
                LIMIT 1
                """,(res[0])).fetchone()
            print(name[0])
            curuser.execute("INSERT INTO vieved(user_id, movie_id, movie_name) VALUES(?,?,?)",(current_user[0], res[0][0], name[0]))
            connuser.commit()
            curimdb.close()
            curuser.close()
        elif func == "2":
            with sql.connect("users.db") as udb:
                cur = udb.cursor()
                cur.execute("SELECT movie_name FROM vieved WHERE user_id = ?", (current_user[0],))
                history = cur.fetchall()
            print("История выподавших фильмов:")
            print(", ".join(row[0] for row in history))
        elif func == "3":
            break
        else:
            print("_" * 68)
            print("Команда введена не верно.")

 
while(1):
    if not os.path.exists(db_path):
        print("База данных imdb.bd не найдена выберите действие:", "1. Загрузить БД(~20GB).", "2. Выход.",sep = "\n")
        func = input()
        if func == "1":
            print("Ожидайте...")
            try:
                subprocess.run(
                ["imdb-sqlite", "--db", db_path], 
                stdout=sys.stdout, 
                stderr=sys.stderr, 
                check=True
                )
                print("База данных успешно создана!")
            except subprocess.CalledProcessError as e:
                print(f"Произошла ошибка при сборке базы данных: {e}")
        elif func == "2":
            break
        else:
            print("Команда введена не верно.")
    else:
        print("_" * 68)
        print("Вы должны зарегестрироваться или войти:","1. Регистрация", "2. Вход", "3. Выход",sep="\n")
        print("_" * 68)
        func = input("Введите значение:")
        if func == "1":
            username = input("Введите имя:")
            city = input("Введите город:")
            register_user(username, city)
        elif func == "2":
            username = input("Введите имя:")
            current_user = authorisation(username)
            if current_user != False:
                genres = result(current_user[0])
                usermenu(username)
        elif func == "3":
            break
        else:
            print("_" * 68)
            print("Команда введена не верно.")
