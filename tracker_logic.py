import sqlite3

connection = sqlite3.connect("time_invested.db")

cursor = connection.cursor()

tables_creation = """CREATE TABLE IF NOT EXISTS
sessions(
id INTEGER PRIMARY KEY, 
date TEXT, 
duration INTEGER
)"""

cursor.execute(tables_creation)

class trackerLogic:

    def tracking_hours(self):
        pass
        