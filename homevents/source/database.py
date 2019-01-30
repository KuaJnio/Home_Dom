import logging
from threading import Lock
import sqlite3


class DatabaseHandler(object):
    def __init__(self, name):
        try:
            self.lock = Lock()
            self.connection = sqlite3.connect(name, check_same_thread=False)
            self.create_table()
        except Exception as e:
            logging.error('Error in DatabaseHandler.__init__: ' + str(e))

    def create_table(self):
        try:
            self.lock.acquire()
            c = self.connection.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS matches (timestamp int, value text)')
            self.connection.commit()
            self.lock.release()
        except Exception as e:
            logging.error('Error in DatabaseHandler.create_table: ' + str(e))

    def insert_match(self, timestamp, value):
        try:
            self.lock.acquire()
            c = self.connection.cursor()
            c.execute('INSERT INTO matches VALUES (?, ?)', (timestamp, value))
            self.connection.commit()
            self.lock.release()
        except Exception as e:
            logging.error('Error in DatabaseHandler.insert_match: ' + str(e))

    def check_for_value(self, test_timestamp, test_value):
        try:
            res = False
            self.lock.acquire()
            c = self.connection.cursor()
            c.execute('SELECT * FROM matches WHERE timestamp > ? AND value = ?', (test_timestamp, test_value))
            content = c.fetchone()
            if content:
                res = True
            self.lock.release()
            return res
        except Exception as e:
            logging.error('Error in DatabaseHandler.check_for_value: ' + str(e))
