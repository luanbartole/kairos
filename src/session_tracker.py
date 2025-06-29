import os
import json
from datetime import datetime


class SessionTracker:
    """
    A simple session tracker to time tasks.

    Attributes:
        current_file (str): Path to the JSON file storing the current active session.
        all_file (str): Path to the JSON file storing all completed sessions.
    """

    def __init__(self, current_file='current_session.json', all_file='sessions.json'):
        self.current_file = current_file
        self.all_file = all_file

    def start(self, task, tag):
        """
        Start a new session timer for a given task and optional tag.

        Args:
            task (str): The name or description of the task.
            tag (str): An optional tag/category for the session.

        Behavior:
            - Records the current date and start time.
            - Saves the session info to `current_file` in JSON format.
            - Prints a confirmation message.
        """
        print(f"Starting timer for task [{task}] with tag [{tag.lower()}]")

        now = datetime.now()
        session = {
            "date": now.strftime("%Y-%m-%d"),  # Store date as YYYY-MM-DD
            "start": now.strftime("%H:%M"),    # Store start time as HH:MM (24h format)
            "task": task,
            "tag": tag.lower()
        }

        # Write current session data to the current_file
        with open(self.current_file, "w") as f:
            json.dump(session, f, indent=2)

    def stop(self):
        """
        Stop the currently active session timer.

        Behavior:
            - Reads the active session data from `current_file`.
            - Calculates the duration between start time and current time.
            - Updates the session with end time and duration.
            - Saves the session to the logbook file (`all_file`).
            - Deletes the current session file.
            - Prints confirmation and session summary.

        If no active session file exists, informs the user to start a timer first.
        """
        if not os.path.exists(self.current_file):
            print("No active timer found. Start a timer first using the 'start' command.")
            return

        print("Stopping current timer.")
        now = datetime.now()

        with open(self.current_file) as f:
            session = json.load(f)

        start_time = datetime.strptime(session["start"], "%H:%M")
        end_time = datetime.strptime(now.strftime("%H:%M"), "%H:%M")

        duration = end_time - start_time
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        duration_str = f"{hours:02d}:{minutes:02d}"

        session.update({
            "end": now.strftime("%H:%M"),
            "duration": duration_str
        })

        self._save_to_logbook(session)
        print(f"Session saved: {session['task']} [{session['duration']}]")
        os.remove(self.current_file)

    def _save_to_logbook(self, session):
        """Append a finished session to the logbook file."""
        logs = []
        if os.path.exists(self.all_file):
            with open(self.all_file, "r") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []

        logs.append(session)

        with open(self.all_file, "w") as f:
            json.dump(logs, f, indent=2)