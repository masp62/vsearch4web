import sqlite3


class ConnectionException(Exception):
    pass


class UseDatabase:

    def __init__(self, db: str):
        self.database = db
        pass

    def __enter__(self) -> 'cursor':
        try:
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()

            return self.cursor
        except Exception as e:
            raise ConnectionException(str(e))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
