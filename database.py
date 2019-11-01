import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class StockDatabase:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open(self, name):
        try:
            self.connection = sqlite3.connect(BASE_DIR + "/" + name)
            self.cursor = self.connection.cursor()

            self.create_tables()
        except sqlite3.Error as e:
            print("Ошибка подключения к базе")

    def close(self):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY,
                file_id TEXT,
                service_name TEXT,
                loadtime TEXT,
                answer TEXT
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS file_idx
                ON reports (file_id, service_name)
            """
        )

        try:
            for command in commands:
                self.cursor.execute(command)
        except (Exception, sqlite3.DatabaseError) as error:
            print(error)

    def query(self, query):
        return self.cursor.execute(query)

    def find_file(self, file_id, service_name):
        data = None

        try:
            self.cursor.execute("SELECT * FROM reports WHERE file_id = ? AND service_name = ?", (file_id, service_name,))
            data = self.cursor.fetchall()
        except (Exception, sqlite3.DatabaseError) as error:
            print(error)
        return data

    def write_report(self, file_id, service_name, loadtime, answer):
        try:
            self.cursor.execute("INSERT INTO reports (file_id, service_name, loadtime, answer) VALUES (?, ?, ?, ?)",
                                (file_id, service_name, loadtime, answer))
            self.connection.commit()
        except (Exception, sqlite3.DatabaseError) as error:
            print(error)
