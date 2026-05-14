"""
wytworcza, singleton
dekorator, adapter(do pobierania z isbn)
pamiątka, iterator

run in terminal(not run): python main.py
"""
import datetime
import random
from typing import Self
from abc import ABC, abstractmethod
import sqlite3
import typer
from rich import print
from rich.console import Console, RenderResult
from rich.text import Text


console = Console()

app = typer.Typer()


def generate_isbn():
    isbn = "798"
    for i in range(10):
        isbn += str(random.randint(0, 9))
    return isbn


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
                                "name varchar(20), surname varchar(50), role varchar(255), logged_in int, notification varchar(255))")

            self.cursor.execute("create table books(title varchar(255), author varchar(255), year int unsigned, "
                                "genre varchar(255), copies int unsigned, isbn varchar(13))")

            self.cursor.execute("create table in_possession(username varchar(255), title varchar(255))")

            self.cursor.execute("create table reservations(username varchar(255), title varchar(255))")
            # the same table as in_possession but works differently

            self.cursor.execute("create table history(id integer primary key autoincrement, username varchar(255), action varchar(20), title varchar(255), "
                                "author varchar(255), sql_command varchar(1000), reverse_sql_command varchar(1000))") # action = borrow/return

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

        if condition is not None and not ("distinct" in condition.keys() or ("distinct" in condition.values())):
            cond = ""
            n = 0
            for i in condition.keys():
                if i != "distinct":
                    if n == 0:
                        cond = f"{i} = ?"
                        n += 1
                    else:
                        cond += f" and {i} = ?"

            values = tuple(condition.values())
            selection = self.cursor.execute(f"select {columns} from {table} where {cond}", values).fetchall()

        elif condition is not None and ("distinct" in condition.keys() or ("distinct" in condition.values())):
            cond = ""
            n = 0
            for i in condition.keys():
                if i != "distinct":
                    if n == 0:
                        cond = f"{i} = ?"
                        n += 1
                    else:
                        cond += f" and {i} = ?"

            selection = self.cursor.execute(f"select distinct {columns} from {table}").fetchall()

        else:
            selection = self.cursor.execute(f"select {columns} from {table}").fetchall()
        return selection

    def update(self, what: list, values: list, table: str, condition: dict = None) -> None:
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

            if table == "books":
                qm += ", ?"

                isbn = generate_isbn()
                invalid = True
                while invalid:
                    if self.cursor.execute(f"select * from books where isbn=?", (isbn,)).fetchone() == None:
                        invalid = False
                    else:
                        isbn = generate_isbn()
                    #if self.cursor.execute(f"select * from books where isbn=?", (isbn,)).fetchone():

                what.append(isbn)

                self.cursor.execute(f"insert into {table} values ({qm})", tuple(what))
            elif table == "history":
                self.cursor.execute(f"insert into {table} (username, action, title, author, sql_command, reverse_sql_command) values ({qm})", tuple(what))
            else:
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
            # print(p)
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

    @abstractmethod
    def get_notification(self):
        pass

    @abstractmethod
    def set_notification(self, notif) -> None:
        pass

    @abstractmethod
    def revert_last_action(self):
        pass

    @abstractmethod
    def show_history(self):
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
        self.notification = None

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
        has_book = self.database.select(["count(*)"], "in_possession", {"username":self.username, "title":title})[0][0]

        if has_book != 0:
            raise RuntimeError("You already have this book")
        else:

            self.books.append((title, author))

            self.database.insert([self.username, title], "in_possession")

            """
            ids = self.database.select(["id"], "history", {"username":self.username})
            id = 0
            for i in ids:
                if id == 0:
                    id = int(i)
                else:
                    if int(i) > id:
                        id = int(i)
            """

            normal_sql = f"insert into in_possession (username, title) values (?, ?)"
            reversed_sql = f"delete from in_possession where username=? and title=?"

            # self.database.insert([id+1, self.username, "borrow", title, author, normal_sql, reversed_sql], "history")
            self.database.insert([self.username, "borrow", title, author, normal_sql, reversed_sql], "history")
            number_of_copies = self.database.select(["copies"], "books", {"title": title, "author": author})[0]
            self.database.update(["copies"], [number_of_copies[0]-1], "books", {"title": title, "author": author})

    @verify_permissions
    def return_book(self, title: str, author: str) -> None:  # ????????????
        self.books.remove((title, author))

        self.database.remove("in_possession", {"username": self.username, "title": title})

        """
        ids = self.database.select(["id"], "history", {"username": self.username})[0]
        id = 0
        for i in ids:
            if id == 0:
                id = int(i)
            else:
                if int(i) > id:
                    id = int(i)
        """

        reversed_sql = f"insert into in_possession (username, title) values (?, ?)"
        normal_sql = f"delete from in_possession where username=? and title=?"

        self.database.insert([self.username, "return", title, author, normal_sql, reversed_sql], "history")
        # self.database.insert([id + 1, self.username, "return", title, author, normal_sql, reversed_sql], "history")
        number_of_copies = self.database.select(["copies"], "books", {"title": title, "author": author})[0]
        self.database.update(["copies"], [number_of_copies[0] + 1], "books", {"title": title, "author": author})

        # notification
        try:
            username = self.database.select(["username"], "reservations", {"title": title})[0][0]
            self.database.remove("reservations", {"username": username, "title": title})
            self.database.update(["notification"], [f"Book {title} by {author} is now available"], "users", {"username": self.username})
        except IndexError:
            pass

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

    def get_notification(self):
        return self.notification

    def set_notification(self, notif) -> None:
        self.notification = notif

    def revert_last_action(self):
        operations = self.database.select(["*"], "history", {"username":self.username})
        # print(operations)
        last_action, title, author = operations[len(operations)-1][2], operations[len(operations)-1][3], operations[len(operations)-1][4]
        # print(last_action)
        if last_action == "borrow":
            self.return_book(title, author)
        if last_action == "return":
            self.borrow_book(title, author)
        # raise Exception("Not implemented")

    def show_history(self):  # shows from most recent
        history = self.database.select(["*"], "history", {"username":self.username})
        action_history = f"Your history(from most recent):"
        for h, i in zip(reversed(history), range(len(history))):
            action_history += f"\n{i+1}. {h[2]}ed book '{h[3]}' by {h[4]}"
        return action_history

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

    def get_notification(self):
        pass

    def set_notification(self, notif) -> None:
        pass

    def revert_last_action(self):
        pass

    def show_history(self):
        pass

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

    def create_user(self, username: str, password: str, name: str, surname: str, role: str, register: bool) -> User:
        # print(self.database.select(["*"], "users", {"username": username}) == [])
        if register:
            if role == "admin" or role == "user":
                if self.database.select(["*"], "users", {"username": username}) == []:
                    new_user = self._factories[role]().create_user(username, password, name, surname, role, self.database)
                    self.database.insert([username, password, name, surname, role, False, None], "users")
                    self.database.commit()

                else:
                    raise ValueError(f"User {username} already exists")
                return new_user
            else:
                raise ValueError(f"Invalid role: {role}")
        else:
            user = self._factories[role]().create_user(username, password, name, surname, role, self.database)
            user.set_logged_in()
            #self.database.insert([username, password, name, surname, role, False, None], "users")
            self.database.update(["logged_in"], [True], "users", {"username": username, "password": password})
            self.database.commit()
            return user


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
        return f"{self.title} by {self.author} written in {self.year}, available copies: {self.copies}, isbn: {self.get_isbn()}"


class BookIterator:
    books: list
    n: int
    limit: int

    def __init__(self, database: DatabaseAdapter) -> None:
        self.books = []
        self.database = database
        self.n = 0

    def find_books_by_genre(self, genre: str):
        self.books = []
        if genre is not None:
            self.books = self.database.select(["*"], "books", {"genre": genre})
        else:
            self.books = self.database.select(["*"], "books", None)

        self.n = 0
        self.limit = len(self.books)

    def find_books_by_isbn(self, isbn: str):
        self.books = []
        if isbn is not None:
            self.books = self.database.select(["*"], "books", {"isbn": isbn})
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
            b = Book(book[0], book[1], book[2], book[3], book[4])
            b.set_isbn(book[5])
            return b

        raise StopIteration


def register_user(user_factory: Factory):
    name = input("Enter your name> ")
    surname = input("Enter your surname> ")
    username = input("Enter your username> ")
    password = input("Enter your password> ")
    role = input("Enter your role(admin or user)> ")
    try:
        user_factory.create_user(username, password, name, surname, role, True)
    except ValueError as e:
        print(e)


def log_in_user(user_factory: Factory, db_adapter: DatabaseAdapter):
    username = input("Enter your username> ")
    password = input("Enter your password> ")
    user_data = db_adapter.select(["name", "surname", "role"], "users", {"username": username, "password": password})

    if user_data == []:
        return None, "Invalid username or password"
    else:
        name, surname, role = user_data[0]
        user = user_factory.create_user(username, password, name, surname, role, False)
        return user, "Logged in"


def options(user: User, user_factory: Factory, db_adapter: DatabaseAdapter, iterator: BookIterator):
    if user is None:
        print("1 - Log in\n2 - Register user\n3 - Quit\n")
        choice = input("> ")

        match(choice):
            case "1":
                user, note = log_in_user(user_factory, db_adapter)
                print(note)
                return user
            case "2":
                register_user(user_factory)
            case "3":
                print("Goodbye!")
                quit(0)
            case _:
                print("Invalid input")

        return None

    elif user.__class__ == LibraryUser:
        print("1 - List all books\n2 - Search book by genre\n3 - Search book by isbn\n4 - Borrow book\n5 - Return book\n6 - Reserve book\n7 - Show history\n0 - Log out\n")
        choice = input("> ")

        match(choice):
            case "1":
                iterator.find_books_by_genre(None)

                for i, j in zip(range(iterator.limit), iterator):
                    print(f"{i + 1}) {j}")

            case "2":
                genre = db_adapter.select(["genre"], "books", {"distinct":"distinct"})
                # print(genre)
                if genre != []:

                    while True:
                        for i in range(len(genre)):
                            print(f"{i + 1}) {genre[i][0]}")

                        choice2 = input("> ")

                        try:
                            choice2 = int(choice2)

                            if not 1 <= choice2 <= len(genre):
                                raise ValueError("Invalid choice")
                            else:
                                genre = genre[choice2-1][0]
                                break

                        except ValueError:
                            print("Invalid input")

                    iterator.find_books_by_genre(genre)

                    for i, j in zip(range(iterator.limit), iterator):
                        print(f"{i + 1}) {j}")

                else:
                    print("There are no books")

            case "3":
                choice2 = input("Enter isbn> ")

                iterator.find_books_by_isbn(choice2)

                if iterator.limit == 0:
                    print(f"There is no book with isbn: {choice2}")
                else:
                    for i, j in zip(range(iterator.limit), iterator):
                        print(f"{i + 1}) {j}")


@app.command()
def run():
    mydb = DatabaseConnection("library_database.db")
    db_adapter = DatabaseAdapter(mydb)
    user_factory = Factory(db_adapter)
    iterator = BookIterator(db_adapter)
    user = None

    while True:
        if user is None:
            user = options(user, user_factory, db_adapter, iterator)
        else:
            options(user, user_factory, db_adapter, iterator)

if __name__ == "__main__":
    app()
