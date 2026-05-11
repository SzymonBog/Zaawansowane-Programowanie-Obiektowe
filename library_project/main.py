"""
wytworcza, singleton
dekorator, adapter(do pobierania z isbn)
pamiątka, iterator
"""
from typing import Self
from abc import ABC, abstractmethod
import sqlite3


class Singleton:
    _instance: Self = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            instance = super().__new__(cls, *args, **kwargs)
            cls._instance = instance

        return cls._instance


class DatabaseConnection:
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
    """
    def connect(self):
        self.mydb = sqlite3.connect(self.database_name)  # commit
        self.cursor = self.mydb.cursor()  # mysql commands
    """


class User(ABC):
    pass


db = DatabaseConnection("library_database.db")
db1 = DatabaseConnection("library_database.db")

print(db is db1)
