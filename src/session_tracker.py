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
        """Initialize file paths for current and all sessions."""
        self.current_file = current_file
        self.all_file = all_file

    def start(self, task, tag):
        """Start a new session timer for a task with an optional tag."""
        print(f'Starting timer for task [{task}] with tag [{tag.lower()}]')
        now = datetime.now()
        session = {
            'date': now.strftime('%Y-%m-%d'),
            'start': now.strftime('%H:%M'),
            'task': task,
            'tag': tag.lower()
        }
        with open(self.current_file, 'w') as f:
            json.dump(session, f, indent=2)

    def stop(self):
        """
        Stop the current session, calculate duration,
        save it to the log, and delete the current session file.
        """
        if not os.path.exists(self.current_file):
            print('No active timer found. Start a timer first using the \'start\' command.')
            return

        print('Stopping current timer.')
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
        print(f'Session saved: {session["task"]} [{session["duration"]}]')
        os.remove(self.current_file)

    def _save_to_logbook(self, session):
        """
        Append a finished session to the logbook file.
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

    def export(self, format, output):
        """
        Export saved sessions to CSV or JSON.
        """
        data = self._load_sessions()
        if not data:
            print('No sessions to export.')
            return

        default_name = 'session_export.json' if format == 'json' else 'session_export.csv'
        output_path = Path(output or default_name)

        if not self._confirm_output_path(output_path):
            return

        if format == 'csv':
            self._write_csv(data, output_path)
        else:
            self._write_json(data, output_path)

        print(f'{format.upper()} export completed: {output_path}')

    def _load_sessions(self):
        """
        Load sessions from log file; return empty list if missing/corrupted.
        """
        if not os.path.exists(self.all_file):
            return []
        try:
            with open(self.all_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _confirm_output_path(self, path):
        """
        Check or create output directory; prompt user if missing.
        """
        if not path.parent.exists():
            confirm = input(f'Directory "{path.parent}" does not exist. Create it? (y/n): ').strip().lower()
            if confirm == 'y':
                path.parent.mkdir(parents=True, exist_ok=True)
                return True
            else:
                print("Export cancelled")
                return False
        return True

    def _write_csv(self, data, path):
        """
        Write session data to CSV file.
        """
        with open(path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def _write_json(self, data, path):
        """
        Write session data to JSON file.
        """
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)
