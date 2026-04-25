import save
import os, datetime, time
from colorama import Fore, Style, init
from rich.table import Table; from rich.console import Console; from rich.align import Align

init()
exc_files = save.initial_load_ex()
console = Console()

def title():
    console.print(Align.center("[bold]My Habit Tracker[/bold]"))

def clear():
    os.system("cls" if os.name == "nt" else "clear")
    time.sleep(1)

def end_menu():
    time.sleep(0.5)
    input("Enter a character to return to main menu! \n>>> ")
    time.sleep(0.1)
    clear()

def show(habits):
    display = list(habits.keys())
    prep = "Your habits are: "
    for habit in range(len(display)):
        if 0 <= habit < (len(display) - 1):
            prep += Fore.LIGHTCYAN_EX + display[habit] + Style.RESET_ALL + ", "
        elif habit == (len(display) - 1):
            prep += Fore.LIGHTCYAN_EX + display[habit] + Style.RESET_ALL + "."
        else:
            break
    return prep

def show_todo(habits):
    display = [] #list(habits.keys())
    prep = "Your incomplete habits are: "
    for hbt in habits:
        if habits[hbt]["completion"] == "in progress":
            display.append(hbt)
    if display != []:
        for habit in range(len(display)):
            if 0 <= habit < (len(display) - 1):
                prep += Fore.LIGHTCYAN_EX + display[habit] + Style.RESET_ALL + ", "
            elif habit == (len(display) - 1):
                prep += Fore.LIGHTCYAN_EX + display[habit] + Style.RESET_ALL + "."
    else:
        return False
    return prep
        

def invalid():
    print(Fore.RED + "Enter a valid habit please." + Style.RESET_ALL)
    time.sleep(1.5)

def warn_incomplete(habits):
    def warning():
        storage = []
        for habit in habits: 
            now = datetime.datetime.now()
            time_day = now - datetime.datetime.strptime(habits[habit]["initiation date"], "%d-%m-%Y")
            hour_day = now.time().replace(second= 0, microsecond= 0)
            if habits[habit]["streak"] != time_day.days and habits[habit]["completion"] == "in progress" and datetime.time(22, 15) <= hour_day <= datetime.time(23, 59):
                storage.append(habit) 
        return storage
    if warning() != []:
        string = ""
        for habit in warning():
            if habits.index(habit) == 0:
                string += Fore.LIGHTCYAN_EX + habit + Style.RESET_ALL + " "
            else:
                string += Fore.RED + ", " + Fore.LIGHTCYAN_EX + habit + Style.RESET_ALL
        string += Fore.RED + " completion has almost expired! Practice it now!" + Style.RESET_ALL
        print(string)


def process_add(habits, habit):
    habits[habit] = {"completion": "in progress", "streak": 0, "days missed": 0, "initiation date": datetime.date.today().strftime("%d-%m-%Y")}
    save.save_data(habits)

def process_complete(habits, habit):
    habits[habit]["completion"] = "completed"
    save.save_data(habits)

def process_remove(habits, habit):
    if habit in habits:
        habits.pop(habit)
        exc_files["removed habits"][habit] = today()
        save.save_ex(exc_files)
        return True
    else:
        return False

def process_log(habits):
    log_table = Table(title= "Habit Log")
    log_table.add_column("Habit", style= "bold")
    log_table.add_column("Today's progress", style= "bold")
    log_table.add_column("Streak", style= "bold")
    log_table.add_column("Missed days", style= "bold")
    log_table.add_column("Day added", style= "bold")

    for habit in habits:
        log_table.add_row(habit, habits[habit]["completion"], str(habits[habit]["streak"]), str(habits[habit]["days missed"]), habits[habit]["initiation date"])
    return log_table

def today():
    return datetime.date.today().strftime("%d-%m-%Y")

def congratulate(habits):
    yay_content = {}
    for habit in habits:
        streak_n = habits[habit]["streak"]
        if streak_n % 7 == 0 and streak_n != 0:
            yay_content.setdefault(streak_n, []).append(habit)

    if yay_content != {}:
        say = "[bold italic]Well done[/bold italic][italic] on your streaks[/italic] :"
        design = ""
        for streak_count, allhabits in yay_content.items():
            addon = ""
            if len(allhabits) > 1:
                for x in range(len(allhabits)):
                    if x == len(allhabits) - 1:
                        addon += allhabits[x] + "!"
                    elif x == 0:
                        addon += allhabits[x] + ", "
                    else:
                        addon += allhabits[x] + ", "
            elif len(allhabits) == 1:
                addon += allhabits[0] + "!"
            say += "\n" + design + "[italic]a streak of {} in {}[/italic]".format(streak_count, addon)
            design += " "
        console.print(say + "\n")


def new_day(habits):
    def day_reset():
        ll = datetime.datetime.strptime(exc_files["last login"], "%d-%m-%Y")
        last_login = ll.date()
        if last_login == datetime.date.today():
            pass
        elif last_login != datetime.date.today():
            for habit in habits:
                day_info = datetime.date.today() - last_login
                if habits[habit]["completion"] == "completed" and day_info.days == 1:
                    habits[habit]["streak"] += 1
                else:
                    habits[habit]["streak"] = 0
                    habits[habit]["days missed"] += day_info.days - 1
                habits[habit]["completion"] = "in progress"
        save.save_data(habits)
    if exc_files["last login"] != today():
        day_reset()
        exc_files["last login"] = today()
        save.save_ex(exc_files)


