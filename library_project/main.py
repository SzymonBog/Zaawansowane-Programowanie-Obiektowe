"""
wytworcza, singleton
fasada, dekorator
pamiątka, iterator
"""
from typing import Self
from abc import ABC, abstractmethod
import sqlite3


class Singleton:
    _instance: Self

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            instance = super().__new__(cls, *args, **kwargs)
            cls._instance = instance

        return cls._instance


class DatabaseConnection:
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
