import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database
        specified by db_file
        :param db_file: database file
        :return: connection object or None
        """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print (e)
    finally:
        conn.close()

if __name__ == '__main__':
    create_connection('D:\\Documents\sqlite\pythonsqlite.db')
