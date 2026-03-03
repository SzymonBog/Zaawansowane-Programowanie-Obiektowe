from abc import ABC, abstractmethod
from datetime import datetime


class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self, con: bool):
        pass

    @abstractmethod
    def execute_query(self, query: str):
        pass


class MySQLConnection(DatabaseConnection):
    def __init__(self):
        self.connected = False

    def connect(self, con: bool):
        if not con:
            if self.connected:
                print("Disconnected from MySQL server")
                self.connected = False

            else:
                print("Cannot disconnect from MySQL server. User is already disconnected")
        else:
            if self.connected:
                print("Cannot connect to MySQL server. User is already connected")

            else:
                print("Connected to MySQL server")
                self.connected = True

    def execute_query(self, query: str):
        if query == "" or query is None:
            print("Cannot execute query. Query not found")
        else:
            print("Query executed successfully")


class PostgreSQLConnection(DatabaseConnection):
    def __init__(self):
        self.connected = False

    def connect(self, con: bool):
        if not con:
            if self.connected:
                print(f"Disconnected from PostgreSQL server at: {datetime.now().time()}")
                self.connected = False

            else:
                print(f"{datetime.now().time()} - Error: Cannot disconnect from PostgreSQL server. User is already disconnected")
        else:
            if self.connected:
                print(f"{datetime.now().time()} - Error: Cannot connect to PostgreSQL server. User is already connected")

            else:
                print(f"Connected to PostgreSQL server at: {datetime.now().time()}")
                self.connected = True

    def execute_query(self, query: str):
        if query == "" or query is None:
            print(f"{datetime.now().time()} - Error: Cannot execute query. Query not found")
        else:
            print(f"Query executed successfully at {datetime.now().time()}")


mysql = MySQLConnection()
mysql.connect(False)
mysql.connect(True)
mysql.connect(True)
mysql.connect(False)
mysql.execute_query(None)
mysql.execute_query("select * from data")


pgrqsl = PostgreSQLConnection()
pgrqsl.connect(False)
pgrqsl.connect(True)
pgrqsl.connect(True)
pgrqsl.connect(False)
pgrqsl.execute_query(None)
pgrqsl.execute_query("select * from data")
