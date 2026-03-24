from typing import Self


# class Singleton:
#     _instance: Self = None
#
#     def __new__(cls, *args: list, **kwargs: dict) -> Self:
#         if cls._instance is None:
#             instance = super().__new__(cls, *args, **kwargs)
#             cls._instance = instance
#
#         return cls._instance


class DatabaseConnection:
    _instance: Self = None
    _initialized = False

    def __new__(cls, host=None, user=None, password=None, port=None, *args: list, **kwargs: dict) -> Self:
        if cls._instance is None:
            instance = super().__new__(cls, *args, **kwargs)
            cls._instance = instance

        return cls._instance

    def __init__(self, host=None, user=None, password=None, port=None):
        if not self.__class__._initialized:
            if host is None or user is None or password is None or port is None:
                raise ValueError("First instance requires full configuration")

            self.connected_database = None
            self.host = host
            self.user = user
            self.password = password
            self.port = port

            self.__class__._initialized = True
        else:
            if any([host, user, password, port]):
                raise RuntimeError("Configuration has already been set and cannot be changed")

    def connect_to_database(self, database: str, enabled: bool):  # only print
        if enabled:
            if self.connected_database is None or database != self.connected_database:
                self.connected_database = database
                print(f"Successfully connected to {database} database")
            elif database == self.connected_database:
                print(f"Cannot connect to {database} database. User is already connected")
        else:
            if self.connected_database is not None and self.connected_database == database:
                self.connected_database = None
                print(f"Disconnected from {database} database")
            else:
                print(f"Connection to {database} database not found")


cursor = DatabaseConnection("127.0.0.1", "root", "admin123", "3306")  # "127.0.0.1", "root", "admin123", "3306")
cursor.connect_to_database("database.db", True)
cursor.connect_to_database("database1.db", True)
cursor.connect_to_database("database.db", False)
cursor.connect_to_database("database1.db", True)
cursor.connect_to_database("database1.db", False)
cursor.connect_to_database("database1.db", False)

x = DatabaseConnection("127.0.0.1", "root", "admin123", "3306")  # "127.0.0.1", "root", "admin123", "3306")
y = DatabaseConnection()  # "127.0.0.1", "root", "admin123", "3306")
print(x is y)
