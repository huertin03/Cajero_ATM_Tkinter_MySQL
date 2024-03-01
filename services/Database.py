import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'root'
        self.database = 'bancos_alvaro'
        self.conn = None

    def connect(self):
        if not self.conn:
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            except Error as e:
                if 'Unknown database' in str(e):
                    self.create_database()
                    self.conn = mysql.connector.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database=self.database
                    )
        return self.conn

    def create_database(self):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {self.database}")
        cursor.close()
        conn.close()
        self.connect()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
