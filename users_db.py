import sqlite3 as sql
from telegram_user import tg_user

def db_get_user_by_id(id: int) -> tg_user:
    try:
            connection = sql.connect('users.db')
            cursor = connection.cursor()

            sqlite_select_query = f"""SELECT * from users WHERE id = {id}"""
            cursor.execute(sqlite_select_query)
            data = cursor.fetchone()

            connection.commit()
            connection.close
            print(data)
        
            user = tg_user(data[0], username=data[1], first_name=data[2], last_name=data[3], user_trust = data[4], comments = data[5], is_bot = data[6], lg_code = data[7], admin = data[8])
            return user
    except: 
            return db_get_user_by_id(0)

def db_add_comment(uid, data: str = None) -> None:
    try:
        user = db_get_user_by_id(uid)
        old_comment = user.getComments()
        if old_comment != None:
            new_comment = old_comment + "\n" + data
        else:
            new_comment = data
        connection = sql.connect('users.db')
        connection.execute(f"""UPDATE users set comments = '{new_comment}' WHERE ID = '{uid}'""")
        connection.commit()
        connection.close
    except:
        print("comment_error")

def db_set_trustfactor(uid:int, value:int) -> None:
    try:
        user = db_get_user_by_id(uid)
        user.setTrustfactor(value)
        connection = sql.connect('users.db')
        connection.execute(f"""UPDATE users set trust_factor = '{user.trust_factor}' WHERE ID = '{uid}'""")
        connection.commit()
        connection.close
    except:
        print("tf_error")
