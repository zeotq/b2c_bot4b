import sqlite3 as sql
def data_writer(data: dict) -> None:

    connection = sql.connect('users.db')
    cursor = connection.cursor()
    data_id = data.get('id')
    data_username = data.get('username')
    data_first_name = data.get('first_name')
    data_last_name = data.get('last_name')
    data_is_bot = data.get('is_bot')
    data_language_code = data.get('language_code')
    command = f"""INSERT INTO users (id, username, first_name, last_name, is_bot, language_code) values ('{data_id}', '{data_username}', '{data_first_name}', '{data_last_name}', '{data_is_bot}', '{data_language_code}')"""


    check = connection.execute(f"""SELECT * FROM users WHERE id = {data_id}""").fetchone()
    if check is None:
        print(f"ID: {data_id} \ Username: {data_username}\nadded to database")
        connection.execute(command)
    else:
        print(f"ID: {data_id} \ Username: {data_username}\ndata updated: ", end = "")

        old_last_name = str(connection.execute(f"""SELECT last_name FROM users WHERE id = {data_id}""").fetchone()[0])
        old_username = str(connection.execute(f"""SELECT username FROM users WHERE id = {data_id}""").fetchone()[0])
        connection.execute(f"""UPDATE users set first_name = '{data_first_name}' WHERE ID = '{data_id}'""")

        if data_last_name != None and data_last_name != old_last_name:
            connection.execute(f"""UPDATE users set last_name = '{data_last_name}' WHERE ID = '{data_id}'""")
            print(f'new last name - {data_last_name}', end = '; ')
        elif data_last_name == None and old_last_name.find("None now") == -1:
            connection.execute(f"""UPDATE users set last_name = '{old_last_name} (None now)' WHERE ID = '{data_id}'""")
            print(f'saved old lastname - {old_last_name}', end = '; ')
        if data_username != None and old_username != data_username:
            connection.execute(f"""UPDATE users set username = '{data_username}' WHERE ID = '{data_id}'""")
            print('username updated;')
        elif data_username == None and old_username.find("None now") == -1:
            connection.execute(f"""UPDATE users set username = '{old_username} (None now)' WHERE ID = '{data_id}'""")
            print('username deleted;')
    connection.commit()
    connection.close()