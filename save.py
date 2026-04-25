#Program save and load
#Loading files at beginning
import json, os, datetime

program_dir = os.path.dirname(os.path.abspath(__file__))
#File pathway for habits log
file_json = os.path.join(program_dir, "habits.json")
#File pathway for extra settings for successful execution
exc_file = os.path.join(program_dir, "exc.json")

#First-time boot up for both json files
def initial_load():
    try:
        with open(file_json) as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(file_json, "w") as file:
            json.dump({}, file)
        return {}

def initial_load_ex():
    try:
        with open(exc_file) as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(exc_file, "w") as file:
            json.dump({"last login": datetime.date.today().strftime("%d-%m-%Y"), "removed habits": {}}, file)
        return {"last login": datetime.date.today().strftime("%d-%m-%Y"), "removed habits": {}}

#Saving data
def save_data(habits):
    with open(file_json, "w") as file:
        json.dump(habits, file, indent = 4)

def save_ex(data):
    with open(exc_file, "w") as file:
        json.dump(data, file, indent = 4)

