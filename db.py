import sqlite3
import os
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ims.db")

@contextmanager
def get_db():
    con = sqlite3.connect(database=DB_PATH)
    cur = con.cursor()
    try:
        yield con, cur
    finally:
        con.close()
