import csv
from os import system, name
from datetime import date

DAYNAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
FIELDNAMES = ["date", "weekday", "mood"]

def main():
    menu()


if __name__ == "__main__": 
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


    def writeMood(): # Asks for mood and appends it to the file with date included
        clearTerminal()
        mood = input("Today I'm feeling...")

        with open("mood_data.csv", "a") as mood_file:
            writer = csv.DictWriter(mood_file, fieldnames=FIELDNAMES)
            writer.writerow({"date": date.today(),
                             "weekday": date.today().weekday(),
                             "mood": mood})
        input("Entry added! Press ANY to return to main menu...")


    def readMoods() -> list[dict]:
        moods = []
        with open("mood_data.csv", "r") as mood_file:
            moodreader = csv.DictReader(mood_file, fieldnames=FIELDNAMES)

            for mood in moodreader:
                moods.append(mood)
                
        return moods


    def viewHistory(): # Prints csv file line by line
            clearTerminal()
            file = readMoods()
            print(f"Here is your history ({len(file) - 1} days):")
            for mood in file:
                if file.index(mood) != 0:
                    print(f"{mood["date"]} - {DAYNAMES[int(mood["weekday"])]} - {mood["mood"]}")
            input("Press ANY to return to main menu...")


    def getEntryByDate(date) -> list[dict] | None: # Title of func explains what it does
        file = readMoods()
        try:
            for i, e in enumerate(file):
                if e["date"] == date:
                    return file[i]
        except:
            return None


    def promptEntryDate(): # Title also explains what function does
        while True:
            clearTerminal()
            choice = input("Enter date (format: YYYY-MM-DD) or exit: ")

            if choice == "exit":
                break
            elif getEntryByDate(choice) == None:
                input("Wrong format or no entry with date found!")
                continue
            else: 
                entry = getEntryByDate(choice)
                print(f"{entry["date"]} - {DAYNAMES[int(entry["weekday"])]} - {entry["mood"]}")


    main()