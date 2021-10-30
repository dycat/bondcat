import sqlite3
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p',filename='bondcat.log', level=logging.INFO)


class DB:
    def __init__(self, db_name: str = 'bonds.db', test=False):
        if test:
            self.connection = sqlite3.connect(":memory:")
            self.cur = self.connection.cursor()
        else:
            self.connection = sqlite3.connect(db_name)
            self.cur = self.connection.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS bonds (bonds_name text, start_date text)")

    def select_all_bonds(self):
        self.cur.execute("SELECT * FROM bonds")
        all_bonds = self.cur.fetchall()
        return all_bonds

    def select_bonds_at(self, date):
        self.cur.execute("SELECT * FROM bonds WHERE start_date = '2021-11-01T00:00:00'")
        all_bonds = self.cur.fetchall()
        return all_bonds

    def save_bonds(self, bonds):
        self.cur.executemany("INSERT INTO bonds values (?,?)", bonds)
        self.connection.commit()
