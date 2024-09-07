import time
from datetime import datetime
from timelogger.data_manager import DataManager
from timelogger.utils import get_valid_float_input, confirmation_dialog, format_time

class TimeLogger:
    APP_VERSION = "1.3.0"

    def __init__(self):
        self.data_manager = DataManager()
        self.start_time = 0.0
        self.current_task = ""

    def run(self):
        self.print_splash_screen()
        self.handle_date_input()
        self.start_new_task()

        while True:
            command = input("Command (or RETURN to log task): ").strip().lower()
            if command == 'q':
                self.quit()
            elif command in self.commands:
                self.commands[command](self)
            elif command == "":
                self.log_current_task()
            else:
                print("Unknown command. Type 'help' for a list of commands.")

    def print_splash_screen(self):
        print("\n" + "=" * 40)
        print(f"TIME LOGGER v{self.APP_VERSION}".center(40))
        print("=" * 40)
        print(f"User: {self.data_manager.data.username}")
        print(f"Client: {self.data_manager.data.client_id}")
        print("\nType 'help' for available commands")
        print("=" * 40 + "\n")

    def handle_date_input(self):
        date_input = input("Enter date (YYYY-MM-DD) or press RETURN for today: ")
        if date_input == "":
            date_input = datetime.now().strftime("%Y-%m-%d")
        self.data_manager.log_time(f"DATE: {date_input}", 0, "")

    def start_new_task(self):
        if self.data_manager.data.unterminated_task:
            if confirmation_dialog("Unterminated task detected. Recover last session?"):
                self.start_time = self.data_manager.data.saved_start_time
            else:
                self.start_time = time.time()
        else:
            self.start_time = time.time()
        
        self.data_manager.data.saved_start_time = self.start_time
        self.data_manager.data.unterminated_task = True
        self.data_manager.save_data()
        
        self.current_task = input("Enter task description: ")
        print(f"\nTracking task: {self.current_task}")
        print("Press RETURN or enter a command at any time.")

    def log_current_task(self):
        duration = time.time() - self.start_time
        hours = duration / 3600

        self.data_manager.data.tracked_hours += hours
        self.data_manager.data.remaining_hours = max(self.data_manager.data.remaining_hours - hours, 0)

        print(f"\n{self.current_task.upper()}")
        print(f"Time logged: {format_time(hours)}")
        if self.data_manager.data.display_remaining_hours:
            print(f"Total hours remaining: {format_time(self.data_manager.data.remaining_hours)}")
        if self.data_manager.data.display_total_hours:
            print(f"Total hours tracked: {format_time(self.data_manager.data.tracked_hours)}")

        self.data_manager.log_time(self.current_task, hours, "hours")
        self.data_manager.data.unterminated_task = False
        self.data_manager.save_data()

        self.start_new_task()

    def quit(self):
        self.data_manager.save_data()
        print("Time Logger stopped.")
        exit()

    def documentation(self):
        print("\n" + "=" * 40)
        print("TIME LOGGER HELP".center(40))
        print("=" * 40)
        print("Available commands:")
        print("  help        - Show this help menu")
        print("  remain      - Show remaining hours")
        print("  update remain - Update remaining hours")
        print("  tracked     - Show total tracked hours")
        print("  task dur    - Show current task duration")
        print("  edit last   - Edit last time entry")
        print("  summary     - Show summary of today's tasks")
        print("  q           - Quit the application")
        print("=" * 40 + "\n")

    def remaining_hours(self):
        print(f"Total hours remaining: {format_time(self.data_manager.data.remaining_hours)}")

    def update_remaining_hours(self):
        new_hours = get_valid_float_input("Please enter a new number for remaining hours: ")
        if confirmation_dialog("Save?"):
            self.data_manager.data.remaining_hours = new_hours
            self.data_manager.save_data()
            print("Remaining hours updated.")
        else:
            print("Update canceled.")

    def tracked_hours(self):
        print(f"Total hours tracked: {format_time(self.data_manager.data.tracked_hours)}")

    def current_task_duration(self):
        if self.start_time == 0:
            print("\nNo task currently running.")
        else:
            duration = (time.time() - self.start_time) / 3600
            print(f"Current task duration: {format_time(duration)}")

    def edit_last_entry(self):
        last_entry = self.data_manager.get_last_entry()
        if not last_entry:
            print("No entries to edit.")
            return
        
        print(f"Last entry: {last_entry['description']} - {format_time(last_entry['duration'])}")
        new_duration = get_valid_float_input("Enter new duration in hours: ")
        if confirmation_dialog("Save changes?"):
            self.data_manager.update_last_entry(new_duration)
            print("Entry updated.")
        else:
            print("Edit canceled.")

    def daily_summary(self):
        entries = self.data_manager.get_todays_entries()
        if not entries:
            print("No entries for today.")
            return
        
        print("\nToday's tasks:")
        total_time = 0
        for entry in entries:
            print(f"- {entry['description']}: {format_time(entry['duration'])}")
            total_time += entry['duration']
        print(f"\nTotal time: {format_time(total_time)}")

    commands = {
        'help': documentation,
        'remain': remaining_hours,
        'update remain': update_remaining_hours,
        'tracked': tracked_hours,
        'task dur': current_task_duration,
        'edit last': edit_last_entry,
        'summary': daily_summary,
    }