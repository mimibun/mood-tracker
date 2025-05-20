import sqlite3
import json
from os import system, name
from datetime import datetime


def main():
    menu()


if __name__ == "__main__": 
    db = sqlite3.connect("data.db")
    dbCur = db.cursor()

    dbCur.execute('''CREATE TABLE IF NOT EXISTS moods(
                  id integer PRIMARY KEY AUTOINCREMENT,
                  date text NOT NULL,
                  emotion text,
                  mood text);''')
    
    
    def menu():
        while True:
            try:
                clearTerminal()
                print("Mimi's mood tracker:")
                print("1. Add a new entry")
                print("2. View history of entries")
                print("3. Find entry by date")

                choice = int(input("What do you want to do? "))

                match choice:
                    case 1: writeEntry()
                    case 2: viewHistory()
                    case 3: promptEntryDate()
                    case _: continue

            except KeyboardInterrupt: # Allows to exit the program
                clearTerminal()
                break 
            except: continue

    def t(): # Literally just an alias to get current moment in ISO format
        return datetime.now().isoformat()
    

    def clearTerminal(): # OS independent terminal clear
        try:
            if name == "nt":
                system("cls")
            else:
                system("clear")
        except: pass


    def writeEntry(): # Asks for mood and adds it as database entry
        while True:
            clearTerminal()
            emotion = input("What am I feeling right now? ")

            if isEmotion(emotion) == True:
                break
            else: continue 

        mood = input("Today I'm feeling...")
        contentToAdd = (t(),
                        emotion,
                        mood)

        try:
            dbCur.execute('''INSERT INTO moods(date, emotion, mood) VALUES (?,?,?)''', contentToAdd)
            db.commit()

            input("Entry added! Press ANY to return to main menu...")
        except:
            input("ERROR: Could not write to database. Press ANY to return to main menu...")


    def isEmotion(inputEmotion) -> bool:
        with open("emotions.json", "r") as file:
            emotions = json.load(file)
            if inputEmotion in emotions["emotions"]:
                return True
            else: return False


    def viewHistory(): # Prints 'SELECT * FROM moods' query line by line
            clearTerminal()

            dbCur.execute('''SELECT * FROM moods''')
            entries = dbCur.fetchall()

            print(f"Here is your history ({len(entries)} entries and {countDays(entries)} days):")
            for entry in entries:
                print(parseEntry(entry))

            input("Press ANY to return to main menu...")


    def countDays(entries) -> int: # Counts unique days from entries
        lastDay = None
        days = 0

        for entry in entries:
            if entry[1] != lastDay:
                lastDay = entry[1]
                days += 1
        return days


    def getEntryByDate(date) -> list[list]: # Title of func explains what it does
        try:
            dbCur.execute(f'''SELECT * FROM moods WHERE date like "%{date}%"''')
            return dbCur.fetchall()
        except:
            raise Exception("ERROR: Could not read from database. Please check for correct database setup.")
        

    def parseEntry(entry) -> str: # Title also explains what what it does
        d = datetime.fromisoformat(entry[1]).strftime("%Y-%m-%d")
        weekday = datetime.fromisoformat(entry[1]).strftime("%A")
        emotion = entry[2]
        mood = entry[3]

        return f"{d} - {weekday} - {emotion} - {mood}"


    def promptEntryDate(): # Title also explains what function does
        while True:
            clearTerminal()
            choice = input("Enter date (format: YYYY-MM-DD) or exit: ")
            if choice == "exit":
                break

            entries = getEntryByDate(choice)
            if entries != 0: 
                for entry in entries:
                    print(parseEntry(entry))
                input("Press ANY to return to main menu...")
            else:
                input("ERROR: Invalid format or no entry with date found! Press ANY to return to main menu...")
                continue


    main()


    db.commit()
    db.close()