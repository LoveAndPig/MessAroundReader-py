import sqlite3


class History:
    def __init__(self):
        self.__history = {}

        self.__connection = sqlite3.connect("history.db")
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS history (
            file_path TEXT PRIMARY KEY,
            file_index INTEGER NOT NULL
        )""")
        self.__connection.commit()

        self.load_history()

    def update_history(self, file_path, index):
        self.__history[file_path] = index

    def load_history(self):
        self.__cursor.execute("""SELECT file_path, file_index FROM history""")
        data = self.__cursor.fetchall()
        for file_path, index in data:
            self.__history[file_path] = index

    def save_history(self):
        data = []
        for file_path, index in self.__history.items():
            data.append((file_path, index))
        self.__cursor.executemany(
            """INSERT OR REPLACE INTO history (file_path, file_index) VALUES (?, ?)""",
            data
        )
        self.__connection.commit()

    def get_history(self):
        return self.__history

    def get_index(self, file_path):
        return self.__history.get(file_path, 0)


history = History()
