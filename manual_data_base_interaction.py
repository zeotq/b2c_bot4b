import sqlite3 as sql

def data_base(user_command) -> str:
        connection = sql.connect('drons.db')
        cursor = connection.cursor()

        if user_command == 1:
            try:
                return_string = ''
                sqlite_select_query = """SELECT * from drons_in_flight"""
                cursor.execute(sqlite_select_query)
                dron_data = cursor.fetchall()
                for i in dron_data:
                    return_string += "id - {}, dron_type - {}, dron_position - {}, dron_status - {}\n".format(i[0],i[1],i[2],i[3])
                stat =  return_string
            except:
                stat = "Error_0: can't read DB"
        elif user_command == 2:
            try:
                sql_update_query = """Update drons_in_flight set dron_status = 'Available' where dron_status != 'Available'"""
                cursor.execute(sql_update_query)
                stat = 'Done'
            except:
                stat = "Error_1: can't reset DB"
        else:
            stat = 'Error_2: command_id not found'

        connection.commit()
        connection.close()
        return stat