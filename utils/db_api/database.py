import random
import sqlite3
from data import config as cfg
from loader import bot
from datetime import datetime
conn = sqlite3.connect(r"utils\db_api\database.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id PRIMARY KEY,
    username TEXT,
    date TEXT,
    token TEXT,
    ban INT)
""")

cur.execute("""CREATE TABLE IF NOT EXISTS table_topic(
    id PRIMARY KEY,
    id_user INT,
    thread_id INT,
    time INT)
""")

#Users
def create_user(userId,username):
    try:
        date = str(datetime.now())[:19]
        cur.execute("INSERT INTO users VALUES(?,?,?,?,?)",(userId,username,date,0,0))
        conn.commit()
    except Exception as e:
        pass

def get_user_ids():
    result = []
    cortejs = cur.execute("SELECT * FROM users")
    for crtj in cortejs:
        result.append(int(crtj[0]))
    return result

def get_user(userId):
    try:
        user_data = cur.execute("SELECT * FROM users WHERE id = ?",(userId,)).fetchone()
        return parse_user_data(user_data)
    except:
        pass

def get_all_users():
    result = []
    cortejs = cur.execute("SELECT * FROM users")
    for crtj in cortejs:
        result.append(parse_user_data(crtj))
    return result

def parse_user_data(data):
    return {'id':data[0],'username':data[1],'date':data[2],'token':data[3],'ban':data[4]}

def update_userfield(user_id,field,update):
    cur.execute(f"UPDATE users SET {field} = ? WHERE id = ?",(update,user_id))
    conn.commit()

def plus_userfield(user_id,field,plus_value):
    old = cur.execute(f"SELECT {field} FROM users WHERE id = ?", (user_id,)).fetchone()[0]
    if old == None:
        old = ""
    new = old + plus_value
    update_userfield(user_id,field,new)


#topic
def get_topics_by_user_id(user_id: int):
    # Выполняем запрос для получения всех тем пользователя
    rows = cur.execute("SELECT * FROM table_topic WHERE id_user = ?", (user_id,)).fetchall()

    # Если есть результаты, преобразуем их в список тем
    if rows:
        return [parse_topic_table(row) for row in rows]

    # Если тем нет, возвращаем пустой список
    return []

def parse_topic_table(data):
    return {'id': data[0], 'id_user': data[1], 'thread_id': data[2], 'time': data[3]}

def create_table_topic(thread_id,user_id):
    try:
        id = random.randint(111111111,999999999)
        cur.execute("INSERT INTO table_topic VALUES(?,?,?,?)",(id,user_id,thread_id,0))
        conn.commit()
    except Exception as e:
        print(e)
        pass

def get_all_topic_rows():
    rows = cur.execute("SELECT * FROM table_topic").fetchall()
    return [parse_topic_table(row) for row in rows]

def get_topic_for_id(id):
    row = cur.execute("SELECT * FROM table_topic WHERE id = ?", (id,)).fetchone()
    if row:
        return parse_topic_table(row)
    return None

def delete_topic(id):
    cur.execute("DELETE FROM table_topic WHERE id = ?", (id,))
    conn.commit()

def update_topic_table(user_id,field,update):
    cur.execute(f"UPDATE table_topic SET {field} = ? WHERE id = ?",(update,user_id))
    conn.commit()