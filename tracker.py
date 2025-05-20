import sqlite3
from os import system, name
from datetime import datetime
from emotions import emotions


def main():
    menu()


if __name__ == "__main__": 
    db = sqlite3.connect("data.db")
    dbCur = db.cursor()

    dbCur.execute('''CREATE TABLE IF NOT EXISTS moods(
                  id integer PRIMARY KEY AUTOINCREMENT,
                  date text NOT NULL,
                  score INTEGER,
                  emotion text,
                  comment text);''')
    

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
        score = getValidInput(question="On a scale from 1-10, how was your day?", type="score")
        emotion = getValidInput(question="What emotion are you feeling right now?", type="emotion")
        comment = getValidInput(question="Comment:", type="comment")

        contentToAdd = (t(),
                        score,
                        emotion,
                        comment)

        try:
            dbCur.execute('''INSERT INTO moods(date, score, emotion, comment) VALUES (?,?,?,?)''', contentToAdd)
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
        score = entry[2]
        emotion = entry[3]
        comment = entry[4]

        return f"{d} - {weekday} - {score}/10 - {emotion} - {comment}"


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


    def getValidInput(question: str, type: str) -> str | int:
        question = question + " " # This adds a space behind the question

        match type:
            case "score":
                while True:
                    clearTerminal()
                    score = input(question)

                    try:
                        score = int(score)
                        if score > 0 & score <= 10:
                            return score
                        else: raise
                    except:
                        raise TypeError("oopsies: please provide an integer between 1-10.")

            case "emotion":
                while True:
                    clearTerminal()
                    emotion = input(question)

                    if emotion in list(map(str.lower, emotions)):
                        return emotion
                    else:
                        input("Invalid emotion, please provide correct emotion!")
                        continue

            case "comment":
                clearTerminal()
                comment = input(question)
                return comment
            
            case _: raise TypeError(f"oopsies: {type} is not a allowed type.")





    main()


    db.commit()
    db.close()