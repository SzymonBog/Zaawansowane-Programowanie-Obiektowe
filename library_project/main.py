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
                                "genre varchar(255), copies int unsigned)")

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


def verify_permissions(fn: callable) -> callable:  # change to verify permissions
    def getter(self, *args: list, **kwargs: dict):
        fn(self, *args, **kwargs)
        found = False

        for p in self.permissions:
            # print(p)
            if str(fn).__contains__(p):
                print("yay")
                found = True
        # print(str(fn).__contains__("borrow_book"))

        if not found:
            raise RuntimeError("You are not authorized to do this")

        """
        if self.role == "admin":
            self.permissions = ["add_book", "edit_book", "remove_book"]
        else:
            self.permissions = ["borrow_book", "return_book"]
        """

    return getter


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

    @abstractmethod
    def borrow_book(self, title: str, author: str) -> None:
        pass

    @abstractmethod
    def return_book(self, title: str, author: str) -> None:
        pass

    @abstractmethod
    def add_book(self, title: str, author: str, year: int, genre: str, copies: int) -> None:
        pass

    @abstractmethod
    def edit_book(self, title_old: str, author_old: str, year_old: int, genre_old: str, copies_old: int, title: str, author: str, year: int, genre: str, copies: int) -> None:
        pass

    @abstractmethod
    def remove_book(self, title: str, author: str, year: int, copies: int) -> None:
        pass


class LibraryUser(User):
    def __init__(self, username: str, password: str, name: str, surname: str, role: str) -> None:
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.role = role
        self.logged_in = False
        self.permissions = ["borrow_book", "return_book"]
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

    @verify_permissions
    def borrow_book(self, title: str, author: str) -> None:
        self.books.append((title, author))

    @verify_permissions
    def return_book(self, title: str, author: str) -> None:
        self.books.remove((title, author))

    @verify_permissions
    def edit_book(self, title_old: str, author_old: str, year_old: int, genre_old: str, copies_old: int, title: str, author: str, year: int, genre: str, copies: int) -> None:
        pass

    @verify_permissions
    def add_book(self, title: str, author: str, year: int, genre: str, copies: int) -> None:
        pass

    @verify_permissions
    def remove_book(self, title: str, author: str, year: int, copies: int) -> None:
        pass

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
    def __init__(self, username: str, password: str, name: str, surname: str, role: str) -> None:
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.role = role
        self.logged_in = False
        self.permissions = ["add_book", "edit_book", "remove_book"]

    def get_logged_in(self) -> bool:
        return self.logged_in

    def set_logged_in(self) -> None:
        if self.logged_in:
            self.logged_in = False
        else:
            self.logged_in = True

    def get_permissions(self) -> list:
        return self.permissions

    @verify_permissions
    def borrow_book(self, title: str, author: str) -> None:
        pass

    @verify_permissions
    def return_book(self, title: str, author: str) -> None:
        pass

    @verify_permissions
    def edit_book(self, title_old: str, author_old: str, year_old: int, genre_old: str, copies_old: int, title: str, author: str, year: int, genre: str, copies: int) -> None:
        raise Exception("Not implemented")

    @verify_permissions
    def add_book(self, title: str, author: str, year: int, genre: str, copies: int) -> None:
        raise Exception("Not implemented")

    @verify_permissions
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


class Book:
    def __init__(self, title: str, author: str, year: int, genre: str, copies: int) -> None:
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.copies = copies

    def get_title(self):
        return self.title

    def set_title(self, title: str):
        self.title = title

    def get_author(self):
        return self.author

    def set_author(self, author: str):
        self.author = author

    def get_year(self):
        return self.year

    def set_year(self, year: str):
        self.year = year

    def get_genre(self):
        return self.genre

    def set_genre(self, genre: str):
        self.genre = genre

    def get_copies(self):
        return self.copies

    def set_copies(self, copies: str):
        self.copies = copies


@app.command()
def run():
    mydb = DatabaseConnection("library_database.db")
    # mydb1 = DatabaseConnection("library_database.db")

    # print(mydb is mydb1)

    lu = LibraryUser("lu", "lu", "lu", "lu", "user")
    print(lu.get_permissions())

    lu1 = LibraryUser("lu", "lu", "lu", "lu", "admin")
    print(lu1.remove_book("", "", 15, 1))  # try except
    console.print(lu1)
    # console.print("TEST COLOR", style="bold red")


if __name__ == "__main__":
    app()
