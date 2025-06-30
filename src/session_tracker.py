import os
import json
import csv
from datetime import datetime
from pathlib import Path


class SessionTracker:
    """
    Stores current and completed sessions in JSON files.
    """

    def __init__(self, current_file='current_session.json', all_file='sessions.json'):
        """
        Args:
            current_file (str): Path for the current active session file.
            all_file (str): Path for the logbook file containing all sessions.
        """
        self.current_file = current_file
        self.all_file = all_file

    def start(self, task, tag):
        """
        Start a new session timer for a task with an optional tag.

        Args:
            task (str): Task description.
            tag (str): Optional tag for the session.

        Returns:
            str: Confirmation message.
        """
        now = datetime.now()
        session = {
            'date': now.strftime('%Y-%m-%d'),
            'start': now.strftime('%H:%M'),
            'task': task,
            'tag': tag.lower() if tag else "general"
        }
        with open(self.current_file, 'w') as f:
            json.dump(session, f, indent=2)
        return f"Started timer for task: {task} (tag: {session['tag']})"

    def stop(self):
        """
        Stop the current session, calculate duration,
        save it to the log, and delete the current session file.

        Returns:
            str: Confirmation message.

        Raises:
            FileNotFoundError: If no active timer is found.
        """
        if not os.path.exists(self.current_file):
            raise FileNotFoundError("No active timer found. Start a timer first using the 'start' command.")

        now = datetime.now()
        with open(self.current_file) as f:
            session = json.load(f)

        start_time = datetime.strptime(session['start'], '%H:%M')
        end_time = datetime.strptime(now.strftime('%H:%M'), '%H:%M')

        duration = end_time - start_time
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        duration_str = f'{hours:02d}:{minutes:02d}'

        session.update({
            'end': now.strftime('%H:%M'),
            'duration': duration_str
        })

        self._save_to_logbook(session)
        os.remove(self.current_file)

        return f"Session saved: {session['task']} — duration: {session['duration']}"

    # ─── Helper Method ────────────────────────────────────────────────

    def _save_to_logbook(self, session):
        """
        Append a finished session to the logbook file.

        Args:
            session (dict): Session data to be saved.
        """
        logs = []
        if os.path.exists(self.all_file):
            try:
                with open(self.all_file, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

        logs.append(session)

        with open(self.all_file, 'w') as f:
            json.dump(logs, f, indent=2)

    # ───────────────────────────────────────────────────────────────────

    def export(self, format, output):
        """
        Export saved sessions to CSV or JSON.

        Args:
            format (str): 'csv' or 'json'.
            output (str): Output filename or path.

        Returns:
            str: Export success message.

        Raises:
            FileNotFoundError: If no sessions found to export.
            FileNotFoundError: If output directory doesn't exist.
        """
        data = self.get_sessions()
        if not data:
            raise FileNotFoundError("No sessions to export.")

        default_name = 'session_export.json' if format == 'json' else 'session_export.csv'
        output_path = Path(output or default_name)

        if not output_path.parent.exists():
            raise FileNotFoundError(f'Directory "{output_path.parent}" does not exist.')

        if format == 'csv':
            self._write_csv(data, output_path)
        else:
            self._write_json(data, output_path)

        return f"{format.upper()} export completed: {output_path}"

    # ─── Helper Methods ────────────────────────────────────────────────

    def _write_csv(self, data, path):
        """
        Write session data to CSV file.

        Args:
            data (list): List of session dicts.
            path (Path): Output file path.
        """
        with open(path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def _write_json(self, data, path):
        """
        Write session data to JSON file.

        Args:
            data (list): List of session dicts.
            path (Path): Output file path.
        """
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    def get_sessions(self):
        """
        Load sessions from log file.

        Returns:
            list: List of session dicts, or empty list if none found.
        """
        if not os.path.exists(self.all_file):
            return []
        try:
            with open(self.all_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
