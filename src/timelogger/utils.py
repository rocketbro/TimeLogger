def get_valid_float_input(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def confirmation_dialog(message: str) -> bool:
    response = input(f"{message} (y/n): ").strip().lower()
    return response == 'y'

def format_time(hours):
    """Format time in hours to a string with appropriate units."""
    if hours < 1:
        return f"{hours * 60:.2f} minutes"
    else:
        return f"{hours:.2f} hours"