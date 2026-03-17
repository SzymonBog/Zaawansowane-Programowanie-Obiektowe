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

    def __new__(cls, *args: list, **kwargs: dict) -> Self:
        if cls._instance is None:
            instance = super().__new__(cls, *args, **kwargs)
            cls._instance = instance

        return cls._instance

    def __init__(self):  # , host, user, password, port):
        # self.host = host
        # self.user = user
        # self.password = password
        # self.port = port
        self.connected_database = None

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


cursor = DatabaseConnection()  # "127.0.0.1", "root", "admin123", "3306")
cursor.connect_to_database("database.db", True)
cursor.connect_to_database("database1.db", True)
cursor.connect_to_database("database.db", False)
cursor.connect_to_database("database1.db", True)
cursor.connect_to_database("database1.db", False)
cursor.connect_to_database("database1.db", False)

x = DatabaseConnection()  # "127.0.0.1", "root", "admin123", "3306")
y = DatabaseConnection()  # "127.0.0.1", "root", "admin123", "3306")
print(x is y)
