"""
wytworcza, singleton
dekorator, adapter(do pobierania z isbn)
pamiątka, iterator

run in terminal(not run): python main.py
"""
from typing import Self
from abc import ABC, abstractmethod
import sqlite3
import typer
from rich import print
from rich.console import Console, RenderResult
from rich.text import Text


console = Console()

app = typer.Typer()


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
            console.print(f"Database {self.database_name} created")  # :boom:")
        else:
            # for testing
            # print(self.cursor.execute("select name from sqlite_master where type='table'").fetchall())
            # print(self.cursor.execute("select name from sqlite_master where type='table'").fetchall()[0])
            # print(self.cursor.execute("select name from sqlite_master where type='table'").fetchall()[0][0])
            pass

def set_permissions(fn: callable) -> callable:  # change to verify permissions
    def setter(self, *args: list, **kwargs: dict):
        fn(self, *args, **kwargs)

        if self.role == "admin":
            self.permissions = ["add books", "edit books", "remove books"]
        else:
            self.permissions = ["borrow books", "return books"]

    return setter


class User(ABC):
    @abstractmethod
    def get_logged_in(self) -> bool:
        pass

    @abstractmethod
    def set_logged_in(self) -> bool:
        pass

    @abstractmethod
    def get_permissions(self) -> list:
        pass

    #@abstractmethod
    #def set_permissions(self, permissions: list) -> None:
    #    pass


class LibraryUser(User):
    @set_permissions
    def __init__(self, username: str, password: str, name: str, surname: str, role: str) -> None:
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.role = role
        self.logged_in = False
        self.permissions = []
        self.books = []

    def get_logged_in(self) -> bool:
        return self.logged_in

    def set_logged_in(self) -> None:
        if self.logged_in:
            self.logged_in = False
        else:
            self.logged_in = True

    def get_permissions(self) -> list:
        return self.permissions

    def borrow_book(self, title: str, author: str) -> None:
        self.books.append((title, author))

    def return_book(self, title: str, author: str) -> None:
        self.books.remove((title, author))

    def __str__(self):
        return f"{self.role}: {self.username} - {self.name} {self.surname}"

    def __rich_console__(self, console, options):
        text = Text()

        text.append(f"{self.role}", style="bold green")
        text.append(": ")
        text.append(self.username, style="white")
        text.append(" - ")
        text.append(f"{self.name} {self.surname}", style="cyan")

        yield text

class LibraryAdmin(User):
    @set_permissions
    def __init__(self, username: str, password: str, name: str, surname: str, role: str) -> None:
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.role = role
        self.logged_in = False
        self.permissions = []

    def get_logged_in(self) -> bool:
        return self.logged_in

    def set_logged_in(self) -> None:
        if self.logged_in:
            self.logged_in = False
        else:
            self.logged_in = True

    def get_permissions(self) -> list:
        return self.permissions

    def add_book(self, title: str, author: str, year: int, copies: int) -> None:
        raise Exception("Not implemented")

    def remove_book(self, title: str, author: str, year: int, copies: int) -> None:
        raise Exception("Not implemented")

    # def __str__(self):
    #    return f"[bold red]{self.role}[/bold red]: {self.username} - {self.name} {self.surname}"

    def __rich_console__(self, console, options):
        text = Text()

        text.append(f"{self.role}", style="bold green")
        text.append(": ")
        text.append(self.username, style="white")
        text.append(" - ")
        text.append(f"{self.name} {self.surname}", style="cyan")

        yield text

class UserFactory(ABC):
    @abstractmethod
    def create_user(self, username: str, password: str, name: str, surname: str, role: str) -> User:
        pass


class LibraryUserFactory(UserFactory):
    def create_user(self, username: str, password: str, name: str, surname: str, role: str) -> User:
        return LibraryUser(username, password, name, surname, role)


class LibraryAdminFactory(UserFactory):
    def create_user(self, username: str, password: str, name: str, surname: str, role: str) -> User:
        return LibraryAdmin(username, password, name, surname, role)


class Factory:
    _factories: dict

    def __init__(self) -> None:
        self._factories = {
            "user": LibraryUserFactory(),
            "admin": LibraryAdminFactory(),
        }

    def create_user(self, username: str, password: str, name: str, surname: str, role: str) -> User:
        return self._factories[role](username, password, name, surname, role)


@app.command()
def run():
    mydb = DatabaseConnection("library_database.db")
    # mydb1 = DatabaseConnection("library_database.db")

    # print(mydb is mydb1)

    lu = LibraryUser("lu", "lu", "lu", "lu", "user")
    print(lu.get_permissions())

    lu1 = LibraryUser("lu", "lu", "lu", "lu", "admin")
    print(lu1.get_permissions())
    console.print(lu1)
    # console.print("TEST COLOR", style="bold red")

if __name__ == "__main__":
    app()
