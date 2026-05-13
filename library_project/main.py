"""
wytworcza, singleton
dekorator, adapter(do pobierania z isbn)
pamiątka, iterator

run in terminal(not run): python main.py
"""
import datetime
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

            self.cursor.execute("create table in_possession(username varchar(255), title varchar(255))")

            self.cursor.execute("create table reservations(username varchar(255), title varchar(255))")
            # the same table as in_possession but works differently

            self.cursor.execute("create table history(id int primary key, username varchar(255), action varchar(20), title varchar(255), "
                                "author varchar(255), sql_command varchar(1000), reverse_sql_command varchar(1000))") # action = rent/return

            # save tables/changes to db
            self.mydb.commit()
            console.print(f"Database {self.database_name} created")  # :boom:")
        else:
            # for testing
            # print(self.cursor.execute("select name from sqlite_master where type='table'").fetchall())
            # print(self.cursor.execute("select name from sqlite_master where type='table'").fetchall()[0])
            # print(self.cursor.execute("select name from sqlite_master where type='table'").fetchall()[0][0])
            print("Server has been successfully connected")
            pass

    def select(self, what: list, table: str, condition: dict = None) -> list:
        columns = ""
        for i in range(len(what)):
            if i == 0:
                columns = f"{what[i]}"
            else:
                columns += f", {what[i]}"

        if condition is not None:
            cond = ""
            n = 0
            for i in condition.keys():
                if n == 0:
                    cond = f"{i} = ?"
                    n += 1
                else:
                    cond += f" and {i} = ?"

            values = tuple(condition.values())
            selection = self.cursor.execute(f"select {columns} from {table} where {cond}", values).fetchall()
        else:
            selection = self.cursor.execute(f"select {columns} from {table}").fetchall()
        return selection

    def update(self, what: list, values: list, table: str, condition: dict = None) -> list:
        columns = ""
        for i in range(len(what)):
            if i == 0:
                columns = f"{what[i]} = ?"
            else:
                columns += f", {what[i]} = ?"

        if condition is not None:
            cond = ""
            n = 0
            for i in condition.keys():
                if n == 0:
                    cond = f"{i} = ?"
                    n += 1
                else:
                    cond += f" and {i} = ?"

            all_values = tuple(values) + tuple(condition.values())

            self.cursor.execute(f"update {table} set {columns} where {cond}", all_values)
        else:
            self.cursor.execute(f"update {table} set {columns}", tuple(values))

        self.mydb.commit()

    def insert(self, what: list, table: str):
        increment = False
        if table == "books":
            increment = self.cursor.execute(f"select count(*) from {table} where title = ? and author = ? and year = ? and genre = ?",(what[0], what[1], what[2], what[3])).fetchone()[0] > 0

        if not increment:
            qm = ""
            for i in range(len(what)):
                if i == 0:
                    qm = "?"
                else:
                    qm += ", ?"

            self.cursor.execute(f"insert into {table} values ({qm})", tuple(what))
        else:
            copies = self.cursor.execute("select copies from books where title=? and author=? and year=? and genre=?", (what[0], what[1], what[2], what[3])).fetchone()[0]
            self.update(["copies"], [int(copies) + int(what[4])], "books", {"title":what[0], "author":what[1], "year":what[2], "genre":what[3]})

        self.mydb.commit()

    def remove(self, table: str, condition: dict = None):
        if condition is not None:
            cond = ""
            n = 0
            for i in condition.keys():
                if n == 0:
                    cond = f"{i} = ?"
                    n += 1
                else:
                    cond += f" and {i} = ?"

            self.cursor.execute(f"delete from {table} where {cond}", tuple(condition.values()))
        else:
            self.cursor.execute(f"delete from {table}")

        self.mydb.commit()

    def commit(self) -> None:
        self.mydb.commit()


class DatabaseAdapter:
    def __init__(self, database_connection: DatabaseConnection):
        self.db = database_connection

    def select(self, what: list, table: str, condition: dict = None) -> list:
        return self.db.select(what, table, condition)

    def insert(self, what: list, table: str):
        self.db.insert(what, table)

    def update(self, what: list, values: list, table: str, condition: dict = None):
        self.db.update(what, values, table, condition)

    def remove(self, table: str, condition: dict = None):
        self.db.remove(table, condition)

    def commit(self):
        self.db.commit()


def verify_permissions(fn: callable) -> callable:  # change to verify permissions
    def verification(self, *args: list, **kwargs: dict):
        # fn(self, *args, **kwargs)
        found = False

        for p in self.permissions:
            print(p)
            if str(fn).__contains__(p):
                # print("yay")
                found = True
        # print(str(fn).__contains__("borrow_book"))

        if not found:
            raise RuntimeError("You are not authorized to do this")

        return fn(self, *args, **kwargs)

    return verification


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
    def reserve_book(self, title: str, author: str) -> None:
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
    def __init__(self, username: str, password: str, name: str, surname: str, role: str, database: DatabaseAdapter) -> None:
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.role = role
        self.logged_in = False
        self.permissions = ["borrow_book", "return_book", "reserve_book"]
        self.books = []
        self.database = database

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
    def borrow_book(self, title: str, author: str) -> None:  # ???????????
        self.books.append((title, author))

        self.database.insert([self.username, title], "in_possession")

        ids = self.database.select(["id"], "history", {"username":self.username})
        id = 0
        for i in ids:
            if id == 0:
                id = int(i)
            else:
                if int(i) > id:
                    id = int(i)

        normal_sql = f"insert into in_possession (username, title) values (?, ?)"
        reversed_sql = f"delete from in_possession where username=? and title=?"

        self.database.insert([id+1, self.username, "borrow", title, author, normal_sql, reversed_sql], "history")

    @verify_permissions
    def return_book(self, title: str, author: str) -> None:  # ????????????
        self.books.remove((title, author))

        self.database.remove("in_possession", {"username": self.username, "title": title})

        ids = self.database.select(["id"], "history", {"username": self.username})[0]
        id = 0
        for i in ids:
            if id == 0:
                id = int(i)
            else:
                if int(i) > id:
                    id = int(i)

        reversed_sql = f"insert into in_possession (username, title) values (?, ?)"
        normal_sql = f"delete from in_possession where username=? and title=?"

        self.database.insert([id + 1, self.username, "return", title, author, normal_sql, reversed_sql], "history")

    @verify_permissions
    def reserve_book(self, title: str, author: str) -> None:
        if self.database.select(["count(*)"], "books", {"title":title, "author":author})[0][0] > 0:
            self.database.insert([self.username, title], "reservations")
        # raise Exception("Not implemented")

    @verify_permissions
    def edit_book(self, title_old: str, author_old: str, year_old: int, genre_old: str, copies_old: int, title: str, author: str, year: int, genre: str, copies: int) -> None:
        pass

    @verify_permissions
    def add_book(self, title: str, author: str, year: int, genre: str, copies: int) -> None:
        pass

    @verify_permissions
    def remove_book(self, title: str, author: str, year: int, copies: int) -> None:
        pass

    def revert_last_action(self):
        operations = self.database.select(["*"], "history", {"username":self.username})
        last_action = operations[len(operations)-1]
        print(last_action)
        # raise Exception("Not implemented")

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
    def __init__(self, username: str, password: str, name: str, surname: str, role: str, database: DatabaseAdapter) -> None:
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.role = role
        self.logged_in = False
        self.permissions = ["add_book", "edit_book", "remove_book"]
        self.database = database

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
    def reserve_book(self, title: str, author: str) -> None:
        pass

    @verify_permissions
    def edit_book(self, title_old: str, author_old: str, year_old: int, genre_old: str, copies_old: int, title: str, author: str, year: int, genre: str, copies: int) -> None:
        self.database.update(["title", "author", "year", "genre", "copies"], [title, author, year, genre, copies], "books", {"title":title_old, "author":author_old, "year":year_old, "genre":genre_old})

    @verify_permissions
    def add_book(self, title: str, author: str, year: int, genre: str, copies: int) -> None:
        self.database.insert([title, author, year, genre, copies], "books")

    @verify_permissions
    def remove_book(self, title: str, author: str, year: int, copies: int) -> None:
        self.database.remove("books", {"title":title, "author":author, "year":year})

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
    def create_user(self, username: str, password: str, name: str, surname: str, role: str, database: DatabaseAdapter) -> User:
        pass


class LibraryUserFactory(UserFactory):
    def create_user(self, username: str, password: str, name: str, surname: str, role: str, database: DatabaseAdapter) -> User:
        return LibraryUser(username, password, name, surname, role, database)


class LibraryAdminFactory(UserFactory):
    def create_user(self, username: str, password: str, name: str, surname: str, role: str, database: DatabaseAdapter) -> User:
        return LibraryAdmin(username, password, name, surname, role, database)

class Factory:
    _factories: dict

    def __init__(self, database: DatabaseAdapter) -> None:
        self._factories = {
            "user": LibraryUserFactory,
            "admin": LibraryAdminFactory,
        }
        self.database = database

    def create_user(self, username: str, password: str, name: str, surname: str, role: str) -> User:
        # print(self.database.select(["*"], "users", {"username": username}) == [])
        if self.database.select(["*"], "users", {"username": username}) == []:

            new_user = self._factories[role]().create_user(username, password, name, surname, role, self.database)
            self.database.insert([username, password, name, surname, role, False], "users")
            self.database.commit()

        else:
            raise ValueError(f"User {username} already exists")
        return new_user


class Book:
    def __init__(self, title: str, author: str, year: int, genre: str, copies: int) -> None:
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.copies = copies
        self.isbn = None

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

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn: str):
        self.isbn = isbn

    def __str__(self):
        return f"{self.title} by {self.author} written in {self.year}, available copies: {self.copies}, isbn: {self.isbn}"


class GenreIterator:
    books: list
    n: int
    limit: int

    def __init__(self, database: DatabaseAdapter) -> None:
        self.books = []
        self.database = database
        self.n = 0

    def find_books(self, genre: str):
        self.books = []
        if genre is not None:
            self.books = self.database.select(["*"], "books", {"genre": genre})
        else:
            self.books = self.database.select(["*"], "books", None)

        self.n = 0
        self.limit = len(self.books)

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Book:
        if self.n < self.limit:
            book = self.books[self.n]
            self.n += 1
            return Book(book[0], book[1], book[2], book[3], book[4])

        raise StopIteration


@app.command()
def run():
    mydb = DatabaseConnection("library_database.db")
    # mydb1 = DatabaseConnection("library_database.db")
    db_adapter = DatabaseAdapter(mydb)

    # print(mydb is mydb1)
    user_factory = Factory(db_adapter)

    try:
        user = user_factory.create_user("user1", "password1", "name1", "surname1", "user")
    except ValueError:
        print("This username has already been taken")

    try:
        pass
        #print(user.remove_book("", "", 15, 1))  # try except
    except RuntimeError:
        print("You are not authorized")


    # console.print(user)
    # console.print("TEST COLOR", style="bold red")
    db_adapter.insert(["It", "King", 2005, "horror", 1], "books")
    db_adapter.insert(["It2", "King", 2007, "horror", 1], "books")
    db_adapter.insert(["Harry Potter", "JKR", 2009, "fantasy", 1], "books")
    db_adapter.insert(["Harry Potter", "JKR", 2009, "fantasy", 1], "books")
    db_adapter.insert(["Harry Potter", "JKR", 2009, "fantasy", 1], "books")
    db_adapter.insert(["It", "King", 2005, "horror", 1], "books")
    db_adapter.insert(["It", "King", 2005, "horror", 1], "books")
    # db_adapter.update(["year"], [2000], "books", {"genre": "horror"})
    # db_adapter.remove("books", {"author": "JKR"})
    # db_adapter.commit()

    # user.reserve_book("It", "King")
    # print(db_adapter.select(["*"], "reservations"))

    """
    user.borrow_book("It", "King")
    c = db_adapter.select(["*"], "history")[0][6]
    t = db_adapter.select(["*"], "history")[0][3]
    u = db_adapter.select(["*"], "history")[0][1]
    print(db_adapter.select(["*"], "history"))
    print(db_adapter.select(["*"], "in_possession"))
    print(c)
    mydb.cursor.execute(c, (u, t))
    mydb.commit()
    print(db_adapter.select(["*"], "history"))
    print(db_adapter.select(["*"], "in_possession"))
    """

    it = GenreIterator(db_adapter)
    it.find_books(None)

    for i, j in zip(range(it.limit), it):
        print(f"{i+1}) {j}")


if __name__ == "__main__":
    app()
