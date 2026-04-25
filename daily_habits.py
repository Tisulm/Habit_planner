import logic, save
import time
from colorama import Style, Fore, init
from rich import print as rprint


init()

#Load habits previously dealt with or initialise an empty habit dictionary
habits = save.initial_load()
logic.new_day(habits)

#Print congratulations for 7 day streaks
logic.congratulate(habits)

#Print warnings for incomplete habits if it's getting late in the day
logic.warn_incomplete(habits)

#View habits
def view(): 
    logic.clear()
    if habits != {}:
        print("Today's (", logic.today(), ") habit progression:")
        print("")
        time.sleep(0.5)
        style = ""
        for habit in habits:
            time.sleep(0.5)
            print(style + Fore.LIGHTCYAN_EX + habit + Style.RESET_ALL + " is " + habits[habit]["completion"])
            style += " "
        time.sleep(0.5)
        print("")
        logic.end_menu()
    else:
        print(Fore.YELLOW + "You haven't added any habits yet!" + Style.RESET_ALL)
        time.sleep(0.7)
        logic.clear()

#Viewing all habit data
def log():
    logic.clear()
    if habits != {}:
        rprint(logic.process_log(habits))
        logic.end_menu()
    else:
        print(Fore.YELLOW + "You haven't added any habits yet!" + Style.RESET_ALL)
        time.sleep(0.7)
        logic.clear()

#Adding habits
def add():
    logic.clear()
    habit = input("Enter habit to add : \n" + Fore.GREEN + ">>> " + Style.RESET_ALL).strip().title()
    logic.process_add(habits, habit)
    time.sleep(1)
    print(Fore.YELLOW + habit + " added to habits!" + Style.RESET_ALL)
    time.sleep(1.2)
    logic.clear()

#Completing a daily habit
def complete():
    while True:
        if logic.show_todo(habits) == False:
            logic.clear()
            print(Fore.YELLOW + "You have no incomplete habits!" + Style.RESET_ALL)
            time.sleep(1)
            logic.clear()
            break
        else:
            logic.clear()
            print("Enter a habit to complete, or enter M to return to menu!")
            time.sleep(0.2)
            print(logic.show_todo(habits))
            time.sleep(0.3)
            choice = input(Fore.GREEN + ">>> " + Style.RESET_ALL).strip().title()
            time.sleep(0.8)
            if choice in habits:
                logic.process_complete(habits, choice)
                print(Fore.YELLOW + choice + " completed!" + Style.RESET_ALL)
                time.sleep(0.9)
                #break
            elif choice == "M":
                logic.clear()
                break
            else:
                logic.invalid()
    #logic.end_menu()

#Removing a habit
def remove(): 
    while True:
        logic.clear()
        if habits != {}:
            print(logic.show(habits))
            time.sleep(0.6)
            habit = input("Enter a habit to remove, or enter M to return to menu! \n" + Fore.GREEN + ">>> " + Style.RESET_ALL).strip().title()
            time.sleep(1)
            if logic.process_remove(habits, habit):
                print(Fore.YELLOW + habit + " has been removed!" + Style.RESET_ALL)
                save.save_data(habits)
                time.sleep(1)
                logic.clear()
                break
            elif habit == "M":
                logic.clear()
                break
            else:
                logic.invalid()
        else:
            print(Fore.YELLOW + "You haven't added any habits yet!" + Style.RESET_ALL)
            time.sleep(0.7)
            logic.clear()
            break
    #logic.end_menu()


#Main program execution
def main():
    while True:
        logic.title()
        print(
        "1. View daily habits \n" \
        "2. Add habit \n" \
        "3. Complete habit \n" \
        "4. Remove habit \n" \
        "5. Review habit log \n" \
        "6. Exit program" )
        action = input(Fore.GREEN + "Enter number of action" + Style.RESET_ALL + ": ").strip(" .")

        if action == "1":
            view()
        elif action == "2":
            add()
        elif action == "3":
            complete()
        elif action == "4":
            remove() #work needed
        elif action == "5":
            log() #last removed habits fix
        elif action == "6":
            logic.clear()
            print(Fore.RED + "Exiting program..." + Style.RESET_ALL)
            time.sleep(1)
            break
        else:
            time.sleep(0.5)
            print(Fore.RED + "Please enter a valid number for your action." + Style.RESET_ALL)
            time.sleep(1.5)
            logic.clear()

if __name__ == "__main__":
    main()


#Saving data and habit progression per time
save.save_data(habits)

