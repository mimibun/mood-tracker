import sqlite3
import json
from datetime import datetime

class Entry():
    db = sqlite3.connect("data.db")
    dbCursor = db.cursor()

    dbCursor.execute('''CREATE TABLE IF NOT EXISTS moods(
                  id integer PRIMARY KEY AUTOINCREMENT,
                  date text NOT NULL,
                  emotion text,
                  comment text);''')


    def getEntryRaw(self, pattern, column="id"):
            validColumn = {"id", "date", "emotion", "comment"}

            if column not in validColumn:
                 raise ValueError("column is not in validColumn")

            self.dbCursor.execute(f'''SELECT * FROM moods WHERE {column} like {pattern}''')
            entries = self.dbCursor.fetchall()

            return entries


    def getEntry(self):
        ...


    def writeNewEntry(self, emotion, mood, date=datetime.now().isoformat()):
        try:
            self.dbCursor.execute('''INSERT INTO moods(date, emotion, mood) VALUES (?,?,?)''', (date, emotion, mood))
            self.db.commit()
        except:
            raise Exception("ERROR: Writing to database!")


    def isEmotion(self) -> bool:
        ...




# TODO: add entry - validate, add date, add emotion, check for correct emotion,
#  get entry - how to return entry, as in what return type
#  get entry by a date, check for correct date format, handle errors (user inputs OwO) 