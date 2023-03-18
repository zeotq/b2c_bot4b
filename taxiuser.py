import sqlite3 as sql

class taxiuser(object):

    def __init__(self, uid, phone_number: str = None, name: str = None) -> None:
            self.id = uid
            self.name = name
            self.phone_number = phone_number

    def __eq__(self, __o: object) -> bool:
        if self.id == __o.id:
            return True
        return False

    def update(self, phone_number:str = None, name:str = None) -> None:
        if phone_number != None:
            self.phone_number = phone_number
        if name != None:
            self.name = name

    def get_user_data(self):
        return self.id, self.phone_number, self.name

    def isFull(self):
        if self.phone_number != None and self.name != None:
            return True
        return False
    
    def write_user(self) -> None:
        connection = sql.connect('users_taxi.db')
        command = f"""INSERT INTO users (id, phone, name) values ('{self.id}', '{self.phone_number}', '{self.name}')"""
        print(f"ID: {self.id} \ Username: {self.name}\nadded to database")
        connection.execute(command)
        connection.commit()
        connection.close()