"""
wytworcza, singleton
dekorator, adapter(do pobierania z isbn)
pamiątka, iterator
"""
from typing import Self
from abc import ABC, abstractmethod
import sqlite3


class DatabaseConnection:  # singleton
    _instance: Self = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            instance = super().__new__(cls) # , *args, **kwargs
            cls._instance = instance

        return cls._instance

    def __init__(self, database_name):
        self.database_name = database_name
        self.mydb = sqlite3.connect(self.database_name)  # commit
        self.cursor = self.mydb.cursor()  # mysql commands

        if self.cursor.execute("select name from sqlite_master where type='table'").fetchall() == []:
            # table creation
            self.cursor.execute("create table users(username varchar(255) primary key, password varchar(255), "
                                "name varchar(20), surname varchar(50), role varchar(255), logged_in int)")

            self.cursor.execute("create table books(title varchar(255), author varchar(255), year int unsigned, "
                                "copies int unsigned)")

            self.cursor.execute("create table in_possession(username varchar(255), title varchar(255), "
                                "since timestamp, foreign key(username) references users(username), "
                                "foreign key(title) references books(title))")

            self.cursor.execute("create table reservations(username varchar(255), title varchar(255), "
                                "since timestamp, foreign key(username) references users(username), "
                                "foreign key(title) references books(title))")
            # the same table as in_possession but works differently

            self.cursor.execute("create table history(username varchar(255), action varchar(20), "
                                "sql_command varchar(1000), reverse_sql_command varchar(1000))") # action = rent/return

            # save tables/changes to db
            self.mydb.commit()
            print(f"Database {self.database_name} created")
        else:
            # for testing
            print(self.cursor.execute("select name from sqlite_master where type='table'").fetchall())
            print(self.cursor.execute("select name from sqlite_master where type='table'").fetchall()[0])
            print(self.cursor.execute("select name from sqlite_master where type='table'").fetchall()[0][0])
            pass


class User(ABC):
    pass


mydb = DatabaseConnection("library_database.db")
# mydb1 = DatabaseConnection("library_database.db")

# print(mydb is mydb1)
