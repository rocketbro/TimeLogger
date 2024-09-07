import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class TimeLoggerData:
    client_id: str = "N/A"
    username: str = "Anonymous"
    email: str = ""
    remaining_hours: float = 0.0
    tracked_hours: float = 0.0
    saved_start_time: float = -1.0
    unterminated_task: bool = False
    log_file_path: str = "tl_log.txt"
    data_file_path: str = "tl_data.json"
    display_total_hours: bool = True
    display_remaining_hours: bool = True

class DataManager:
    DATA_DIR = Path(__file__).parent.parent.parent / "data"
    LOG_DIR = Path(__file__).parent.parent.parent / "logs"
    DATA_FILE = DATA_DIR / "tl_data.json"

    def __init__(self):
        self.data = self.load_data()
        self.ensure_directories()

    def ensure_directories(self):
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOG_DIR.mkdir(exist_ok=True)

    def load_data(self) -> TimeLoggerData:
        try:
            with self.DATA_FILE.open("r") as data_file:
                return TimeLoggerData(**json.load(data_file))
        except (FileNotFoundError, json.JSONDecodeError):
            return TimeLoggerData()

    def save_data(self):
        with self.DATA_FILE.open("w") as data_file:
            json.dump(asdict(self.data), data_file, indent=4)

    def log_time(self, description: str, duration: float, time_format: str):
        log_file_path = self.LOG_DIR / self.data.log_file_path
        with log_file_path.open("a") as log_file:
            log_file.write(
                f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                f"\nDescription: {description.upper()}"
                f"\nTime logged: {duration:.2f} {time_format}\n"
            )

    def get_last_entry(self):
        log_file_path = self.LOG_DIR / self.data.log_file_path
        try:
            with log_file_path.open("r") as log_file:
                lines = log_file.readlines()
                if len(lines) < 3:
                    return None
                description = lines[-2].split(": ")[1].strip()
                duration = float(lines[-1].split(": ")[1].split()[0])
                return {"description": description, "duration": duration}
        except FileNotFoundError:
            return None

    def update_last_entry(self, new_duration):
        log_file_path = self.LOG_DIR / self.data.log_file_path
        with log_file_path.open("r") as log_file:
            lines = log_file.readlines()
        
        if len(lines) >= 3:
            lines[-1] = f"Time logged: {new_duration:.2f} hours\n"
        
        with log_file_path.open("w") as log_file:
            log_file.writelines(lines)

    def get_todays_entries(self):
        log_file_path = self.LOG_DIR / self.data.log_file_path
        today = datetime.now().strftime("%Y-%m-%d")
        entries = []
        try:
            with log_file_path.open("r") as log_file:
                lines = log_file.readlines()
                for i in range(0, len(lines), 4):
                    if today in lines[i]:
                        description = lines[i+1].split(": ")[1].strip()
                        duration = float(lines[i+2].split(": ")[1].split()[0])
                        entries.append({"description": description, "duration": duration})
        except FileNotFoundError:
            pass
        return entries