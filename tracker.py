import sqlite3
from os import system, name
from datetime import date

DAYNAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
FIELDNAMES = ["date", "weekday", "mood"]

def main():
    menu()


if __name__ == "__main__": 
    db = sqlite3.connect("data.db")
    dbCur = db.cursor()

    dbCur.execute('''CREATE TABLE IF NOT EXISTS moods(
                  id integer PRIMARY KEY AUTOINCREMENT,
                  date text NOT NULL,
                  weekday integer,
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
                    case 1: writeMood()
                    case 2: viewHistory()
                    case 3: promptEntryDate()
                    case _: continue

            except KeyboardInterrupt: # Allows to exit the program
                clearTerminal()
                break 
            except: continue


    def clearTerminal(): # OS independent terminal clear
        try:
            if name == "nt":
                system("cls")
            else:
                system("clear")
        except: pass


    def writeMood(): # Asks for mood and adds it as database entry
        clearTerminal()
        mood = input("Today I'm feeling...")
        contentToAdd = (f"{date.today()}", f"{date.today().weekday()}", mood)

        try:
            dbCur.execute('''INSERT INTO moods(date, weekday, mood) VALUES (?,?,?)''', contentToAdd)
            db.commit()

            input("Entry added! Press ANY to return to main menu...")
        except:
            input("ERROR: Could not write to database. Press ANY to return to main menu...")


    def viewHistory(): # Prints 'SELECT * FROM moods' query line by line
            clearTerminal()

            dbCur.execute('''SELECT * FROM moods''')
            entries = dbCur.fetchall()

            print(f"Here is your history ({len(entries)} entries and {countDays(entries)} days):")
            for entry in entries:
                print(f"{entry[1]} - {DAYNAMES[int(entry[2])]} - {entry[3]}")

            input("Press ANY to return to main menu...")


    def countDays(entries) -> int: # Counts unique days from entries
        lastDay = None
        days = 0

        for entry in entries:
            if entry[1] != lastDay:
                lastDay = entry[1]
                days += 1
        return days


    def getEntryByDate(date) -> list[list] | None: # Title of func explains what it does
        try:
            dbCur.execute(f'''SELECT * FROM moods WHERE date = "{date}"''')
            return dbCur.fetchall()
        except:
            return None


    def promptEntryDate(): # Title also explains what function does
        while True:
            clearTerminal()
            choice = input("Enter date (format: YYYY-MM-DD) or exit: ")

            if choice == "exit":
                break
            elif getEntryByDate(choice): 
                entries = getEntryByDate(choice)
                for entry in entries:
                    print(f"{entry[1]} - {DAYNAMES[int(entry[2])]} - {entry[3]}")
                input("Press ANY to return to main menu...")
            else:
                input("ERROR: Invalid format or no entry with date found! Press ANY to return to main menu...")
                continue


    main()


    db.commit()
    db.close()