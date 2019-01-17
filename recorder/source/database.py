from threading import Lock
from sqlite3 import connect as sqlite3_connect
from models import Data
import logging


class DatabaseHandler(object):
    def __init__(self, database_path):
        self._database_path = database_path
        self.lock = Lock()
        self.connection = sqlite3_connect(self._database_path, check_same_thread=False)
        self.init_table()

    def init_table(self):
        self.lock.acquire()
        c = self.connection.cursor()
        query = '''
                    CREATE TABLE IF NOT EXISTS data
                    (
                        timestamp INTEGER,
                        feature TEXT,
                        identifier TEXT,
                        value TEXT
                    );
                '''
        c.execute(query)
        self.connection.commit()
        self.lock.release()

    def insert_data(self, data):
        self.lock.acquire()
        c = self.connection.cursor()
        c.execute('INSERT INTO data VALUES (?, ?, ?, ?)', data.get_database_tuple())
        self.connection.commit()
        self.lock.release()

    def get_data(self):
        data_list = []
        self.lock.acquire()
        c = self.connection.cursor()
        c.execute('SELECT * FROM data ORDER BY timestamp ASC')
        content = c.fetchall()
        self.lock.release()
        for i in content:
            data = Data.from_database(i)
            data_list.append(data)
        return data_list
