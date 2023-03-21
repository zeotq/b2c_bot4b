import sqlite3 as sql

class taxiuser(object):

    def __init__(self, uid, phone_number: str = None, name: str = None, location: str = None) -> None:
        connection = sql.connect('users_taxi.db')
        db_data = connection.execute(f"""SELECT * FROM users WHERE id = {uid}""").fetchone()
        if db_data is None:
            self.id = uid
            self.name = name
            self.phone_number = phone_number
            self.location = None
        else:
            self.id = uid
            self.phone_number = db_data[1]
            self.name = db_data[2]
            self.location = None

    def __eq__(self, __o: object) -> bool:
        if self.id == __o.id:
            return True
        return False

    def update(self, phone_number:str = None, name:str = None, location:str = None) -> None:
        if phone_number != None:
            self.phone_number = phone_number
        if name != None:
            self.name = name
        if location != None:
            self.location = location

    def get_data(self):
        return self.id, self.phone_number, self.name

    def isFull(self):
        if self.phone_number != None and self.name != None:
            return True
        return False
    
    def write(self) -> None:
        connection = sql.connect('users_taxi.db')
        if connection.execute(f"""SELECT * FROM users WHERE id = {self.id}""").fetchone() == None:
            command = f"""INSERT INTO users (id, phone, name, location) values ('{self.id}', '{self.phone_number}', '{self.name}', '{self.location}')"""
        else:
            command = f"""UPDATE users set (phone, name, location) = ('{self.phone_number}', '{self.name}', '{self.location}) WHERE ID = '{self.id}'"""
        connection.execute(command)
        connection.commit()
        connection.close()