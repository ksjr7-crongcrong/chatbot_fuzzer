"""
sqlite manager
"""
import sqlite3
import os
from typing import Any


class DBManager:
    def __init__(self, db_path: str):
        newly_created = not os.path.isfile(db_path)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._cursor = self.conn.cursor()
        self.db_path = db_path
        if newly_created:
            self.cursor.executescript("""
                CREATE TABLE IF NOT EXISTS "questions" (
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "category" TEXT NOT NULL,
                    "msg" TEXT NOT NULL UNIQUE,
                    "stype" INT NOT NULL
                );
            """)
            self.conn.commit()

    def __del__(self):
        if self.conn:
            self.conn.close()

    def query(self, stmt) -> Any:
        self.cursor.execute(stmt)
        rows = self.cursor.fetchall()
        result = [row[0] for row in rows]
        if len(result) == 1:
            return result[0]
        return result

    @property
    def conn(self):
        """ db connection getter """
        return self._conn

    @property
    def cursor(self):
        """ db cursor getter """
        return self._cursor


if __name__ == "__main__":
    db_manager = DBManager("test.db")
