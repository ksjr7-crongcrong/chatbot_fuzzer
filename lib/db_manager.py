"""
sqlite manager
"""
import sqlite3
import os

class DBManager:
    def __init__(self, db_path:str):
        newly_created = not os.path.isfile(db_path)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._cursor = self.conn.cursor()
        self.db_path = db_path
        if newly_created:
            self.cursor.executescript("""
                CREATE TABLE IF NOT EXISTS "questions" (
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "category" TEXT NOT NULL,
                    "msg" TEXT NOT NULL UNIQUE
                );
            """)
            self.conn.commit()
    
    def __del__(self):
        self.conn.close()
        os.remove(self.db_path)

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
