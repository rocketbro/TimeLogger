#
# TimeLogger.py
#
# Written by Asher Pope
# asher@asherpope.com
#
# 2024.02.12
# VERSION 1.1.0
#


import time
import json

# define & initialize global variables
tl_data = {}
start_time = 0
app_version = "1.1.1"


# define functions for managing data
def loadLocalData():
    try:
        with open("tl_data.json", "r") as data_file:
            return json.load(data_file)
    except Exception as error:
        print(error)


def save():
    global tl_data
    try:
        with open("tl_data.json", "w") as data_file:
            json.dump(tl_data, data_file, indent = 4)
    except Exception as error:
        print(error)


def logTime(description, total_time, format):
    global tl_data
    try:
        with open(tl_data["log_file_path"], "a") as log_file:
            log_file.write(
                f"\nDescription: {description.upper()}\nTime logged: {str(total_time)} {format}\n"
            )
    except Exception as error:
        print(error)


# define supported command functions
def quit():
    global tl_data
    print("\nSaving...")
    tl_data["unterminated_task"] = False
    save()
    print("Time Logger stopped.\n")
    exit()


def documentation():
    print(
        f"""
~~~

TIME LOGGER
Version: {app_version}

Created by Asher Pope
asher@asherpope.com
©2024 Intrinsic Creative

~~~

COMMANDS
These may be run anytime when using Time Logger.

'Q'
Quit Time Logger. This will mark the current task as terminated.
	
'help'
Show this documentation menu.

'remain'
Show the total number of hours remaining. 
The remaining hours functionality is useful for setting a maximum number of hours you want to track, i.e., 40 hours for one week.

'update remain'
Specify a new number for total remaining hours.

'tracked'
Show the total number of tracked hours. 
Note that even if the remaining hours number described above is 0, Time Logger will continue to update the total amount of tracked time.

'task dur'
Show the duration of the currently running task.

'recover'
Use the last saved start time as the start time for your current task.
This is useful if Time Logger was stopped before you logged your task and you want to pick up where you left off.
This command must be run as soon as Time Logger boots, before a new timer starts. Otherwise it will have no effect. 

'tog remain'
Show/hide the 'Total remaining hours' line in the console when logging a completed task.

'tog total'
Show/hide the 'Total hours tracked' line in the console when logging a completed task.

'initialize'
Initialize Time Logger.
This will set all preferences back to their default settings and erase all hour tracking information. The local 'tl_log.txt' file will be erased unless you have specified a unique client id (assuming you don't specify the same client id during initialization).
Current log file name: {tl_data['log_file_path']}

~~~

	"""
    )


def remainingHours():
    global tl_data
    print(f"Total hours remaining: {tl_data['remaining_hours']}")


def updateRemainingHours():
    global tl_data
    new_hours = input("Please enter a new number for remaining hours: ")
    while not new_hours.isdigit():
        new_hours = input("Please enter a valid numer: ")
    confirm = confirmationDialog("Save?")
    if confirm:
        tl_data["remaining_hours"] = float(new_hours)
        save()
    else:
        print("Update canceled.")


def trackedHours():
    global tl_data
    print(f"Total hours tracked: {round(tl_data['tracked_hours'], 2)}")


def currentTaskDuration():
    global start_time
    if start_time == 0:
        print(
            "\nCould not calculate task duration. Start a new task if the issue persists.\n"
        )
    else:
        # Total time elapsed since the timer started
        duration = round(((time.time() - start_time) / 60), 2)
        time_format = "minutes"
        if duration > 59.99:
            duration = round((duration / 60), 2)
            time_format = "hours"
        print(f"Current task duration: {duration} {time_format}")


def recover():
    global tl_data
    global start_time

    execute_recovery = confirmationDialog(
        "Do you want to use the last saved start time as your current task start time?",
        "Please enter",
    )
    if execute_recovery:
        if start_time == tl_data["saved_start_time"]:
            print("Your current start time already matches the last saved start time.")
            return False
        else:
            start_time = tl_data["saved_start_time"]
            return True
    else:
        print("Recovery canceled.")
        return False


def toggleTotalHourDisplay():
    global tl_data
    tl_data["display_total_hours"] = not tl_data["display_total_hours"]
    save()
    print(f"Display total hours set to {tl_data['display_total_hours']}")


def toggleRemainingHourDisplay():
    global tl_data
    tl_data["display_remaining_hours"] = not tl_data["display_remaining_hours"]
    save()
    print(f"Display remaining hours set to {tl_data['display_remaining_hours']}")


# define initializtion method to configure Time Logger's initial state
def initialize():
    confirmed = confirmationDialog(
        "WARNING: THIS MAY OVERWRITE ANY EXISTING LOCAL TIME LOGGER FILES."
    )

    if confirmed:
        # set up dictionary for saveable data
        tl_data = {
            "client_id": "N/A",
            "client_id_display": "",
            "username": "",
            "username_display": "",
            "email": "",
            "remaining_hours": 0,
            "tracked_hours": 0,
            "saved_start_time": -1,
            "unterminated_task": False,
            "log_file_path": "tl_log.txt",
            "data_file_path": "tl_data.json",
            "display_total_hours": True,
            "display_remaining_hours": False,
        }

        # get config info from user
        print(
            "You may press RETURN to skip any of the following questions. Any information entered will exist only in files local to the current directory.\n"
        )

        username = input("Enter your name: ")

        email = input("Enter your email: ")

        tl_data["username"] = username
        if username != "":
            tl_data["username_display"] = f"\nUser: {username}"
        tl_data["email"] = email

        # ask for a client id
        client_id = input(
            "Add a client id if you want to track time for a specific client: "
        )

        # if a client id is specified, update the data dictionary
        if client_id != "":
            tl_data["client_id"] = client_id
            tl_data["client_id_display"] = f"Client: {client_id}\n"
            tl_data["log_file_path"] = f"tl_log_{client_id}.txt"

        # ask for initial hours
        initial_hours = input(
            "Enter a total number of hours to count down from, i.e., '40' for a work week: "
        )
        initial_hours = checkForIntOrSkip(initial_hours)
        tl_data["remaining_hours"] = initial_hours
        if initial_hours != "":
            tl_data["display_remaining_hours"] = True

        # write the json data file
        with open(tl_data["data_file_path"], "w") as data_file:
            json.dump(tl_data, data_file)

        # write the time log text file
        with open(tl_data["log_file_path"], "w") as log_file:
            client = tl_data["client_id_display"]
            log_file.seek(0)
            log_file.write(f"TIME LOGGER VER {app_version}\nTime Log\n")
            if tl_data["username"] != "":
                log_file.write(f"\n{tl_data['username']}")
            if tl_data["email"] != "":
                log_file.write(f"\n{tl_data['email']}\n")
            log_file.write(client)

        print("\nInitialization successful. Please restart Time Logger.")
        exit()

    else:
        print("\nInitialization cancelled.\n")
        exit()


# command dictionary. keys are the commands users must type to call the corresponding function
commands = {
    "Q": quit,
    "help": documentation,
    "remain": remainingHours,
    "update remain": updateRemainingHours,
    "tracked": trackedHours,
    "task dur": currentTaskDuration,
    "initialize": initialize,
    "recover": recover,
    "tog total": toggleTotalHourDisplay,
    "tog remain": toggleRemainingHourDisplay,
}


# define user input handler functions
def checkForIntOrSkip(value):
    if value == "":
        return 0
    elif value.isdigit():
        return int(value)
    else:
        checkForIntOrSkip(
            input("\nPlease enter a valid number or hit RETURN to skip: ")
        )


def confirmationDialog(displayMessage, confirmationLabel="Please confirm"):
    confirmation = input(f"{displayMessage}\n{confirmationLabel}: 'y' or 'n'\n")
    while confirmation.lower() not in ["y", "n"]:
        confirmation = input(f"\nInvalid selection. {confirmationLabel}: 'y' or 'n'\n")
    if confirmation.lower() == "y":
        print("Confirmed.")
        return True
    elif confirmation.lower() == "n":
        return False


def commandedInput(display_prompt, is_repeating=True):
    value = input(display_prompt)
    command = commands.get(value)
    if is_repeating:
        while command:
            command()
            value = input(f"\n{display_prompt}")
            command = commands.get(value)
        return value
    else:
        if command:
            command()
        else:
            return value


# define utility functions used within the main function
def startNewTask(isRecoveryTask=False):
    global tl_data
    global start_time

    if tl_data["unterminated_task"]:
        use_saved_start = confirmationDialog(
            "An unterminated task has been detected. Do you want to use the last saved start time as your current task start time?",
            "Please enter",
        )

        if use_saved_start:
            start_time = tl_data["saved_start_time"]
        else:
            print("Time Logger will use right now as the task start time.")
            start_time = time.time()
            date = input("Enter date or hit RETURN to skip.\n")
            if date != "":
                with open(tl_data["log_file_path"], "a") as log_file:
                    log_file.write(f"\n\n\nDATE: {date}\n~~~~~~~~~~~~~~~~\n")

    elif isRecoveryTask:
        start_time = tl_data["saved_start_time"]

    else:
        start_time = time.time()
        tl_data["saved_start_time"] = start_time

    tl_data["unterminated_task"] = True
    save()


def ensureHourFormat(time, format):
    ensured_time = time
    if format == "minutes":
        ensured_time = round((ensured_time / 60), 2)
    return ensured_time


# define the main function
def main():
    global tl_data
    global start_time

    # define variables
    value = ""
    date = ""

    # print splash screen
    print("\n")
    print("-" * 18)
    print(
        f"""TIME LOGGER
Version: {app_version}
Created by Asher Pope
asher@asherpope.com
{tl_data['username_display']}
{tl_data["client_id_display"]}
Type 'Q' and press RETURN anytime to end without updating time log.
Type 'help' for more info.
"""
    )
    print("-" * 18)
    print("\n")

    # get date
    if tl_data["unterminated_task"] == False:
        date = input(
            "Enter date or hit RETURN to skip.\nIf you want to recover your last session, type 'recover' now.\n"
        )

    isRecoveryTask = False
    command = commands.get(date)
    while command:
        if command == recover:
            isRecoveryTask = command()
            date = ""
            break
        else:
            command()
        date = input(
            "Enter date or hit RETURN to skip.\nIf you want to recover your last session, type 'recover' now.\n"
        )
        command = commands.get(date)

    if date != "":
        with open(tl_data["log_file_path"], "a") as log_file:
            log_file.write(f"\n\n\nDATE: {date}\n~~~~~~~~~~~~~~~~\n")

    # Timer starts
    startNewTask(isRecoveryTask)

    print("\nTimer started! Press RETURN to save and update the time log.")

    while value != "Q":
        # Input for the ENTER key press
        value = commandedInput("")

        # ask for description of work
        description = commandedInput("Description of work: ")

        if description == "":
            description = "N/A"

        # Total time elapsed since the timer started
        total_time = round(((time.time() - start_time) / 60), 2)
        format = "minutes"
        if total_time > 59.99:
            total_time = round((total_time / 60), 2)
            format = "hours"

        # FOR TESTING:
        # total_time = 30.00

        # calculate hour records
        tl_data["tracked_hours"] += ensureHourFormat(total_time, format)
        tl_data["remaining_hours"] = max(
            (tl_data["remaining_hours"] - ensureHourFormat(total_time, format)), 0
        )

        # print the results
        print(f"\n{description.upper()}\nTime logged: {str(total_time)} {format}")
        if tl_data["display_remaining_hours"]:
            print(f"Total hours remaining: {tl_data['remaining_hours']}")
        if tl_data["display_total_hours"]:
            print(f"Total hours tracked: {tl_data['tracked_hours']}")

        # save the results
        logTime(description, total_time, format)
        tl_data["unterminated_task"] = False
        save()

        startNewTask()
        print(
            "\nTracking new task.\nPress RETURN to log your current task and start a new one.\n"
        )


#
#
# SYSTEM START
#
#


try:
    tl_data = loadLocalData()
    main()
except Exception as error:
    print(error)
    print("Time Logger needs to be initialized.")
    initialize()
