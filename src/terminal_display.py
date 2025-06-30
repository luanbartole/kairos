from rich.table import Table
from rich.console import Console
from datetime import datetime, timedelta


class TerminalDisplay:
    """
    Handles all terminal UI rendering using the rich library.
    """

    def __init__(self):
        """Initialize a console object for styled terminal output."""
        self.console = Console()

    def render_today_summary(self, sessions):
        """
        Display a table summarizing today's sessions.

        Args:
            sessions (list): List of all session dictionaries.
        """
        today = datetime.today().strftime('%Y-%m-%d')
        today_sessions = [s for s in sessions if s.get('date') == today]

        if not today_sessions:
            self.console.print("[bold yellow]No sessions for today.[/bold yellow]")
            return

        table = Table(title=f"Daily Summary - {today}")

        table.add_column("Time", style="cyan", justify="center")
        table.add_column("Duration", style="yellow", justify="center")
        table.add_column("Tag", style="magenta", justify="center")
        table.add_column("Task", style="green", justify="center")

        for session in today_sessions:
            time = f"{session['start']}-{session.get('end', '??')}"
            duration = session.get("duration", "--:--")
            tag = session.get("tag", "-")
            task = session["task"]
            table.add_row(time, duration, tag, task)

        self.console.print(table)

    def render_weekly_summary(self, sessions):
        """
        Display a table summarizing total time spent per tag for each weekday.

        Args:
            sessions (list): List of all session dictionaries.
        """
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        week_sessions = [
            s for s in sessions
            if self._in_this_week(s.get("date", ""), start_of_week, end_of_week)
        ]

        if not week_sessions:
            self.console.print("[bold yellow]No sessions found for this week.[/bold yellow]")
            return

        summary = {}

        for session in week_sessions:
            tag = session.get("tag", "general")
            date_obj = datetime.strptime(session["date"], "%Y-%m-%d")
            weekday = weekdays[date_obj.weekday()]
            duration_str = session.get("duration", "00:00")
            mins = self._duration_to_minutes(duration_str)

            if tag not in summary:
                summary[tag] = {day: 0 for day in weekdays}
            summary[tag][weekday] += mins

        table = Table(title=f"Weekly Summary - {start_of_week.strftime('%b %d')}")

        table.add_column("Tag", style="magenta", no_wrap=True)
        for day in weekdays:
            table.add_column(day, justify="center")

        for tag, days in summary.items():
            row = [tag] + [self._format_minutes(days[day]) for day in weekdays]
            table.add_row(*row)

        self.console.print(table)

    # ─── Helper Methods ────────────────────────────────────────────────

    def _in_this_week(self, date_str, start_of_week, end_of_week):
        """
        Check if a date string falls within the current week.

        Args:
            date_str (str): Date in 'YYYY-MM-DD' format.
            start_of_week (datetime): Monday of the current week.
            end_of_week (datetime): Sunday of the current week.

        Returns:
            bool: True if date is in this week, else False.
        """
        try:
            session_date = datetime.strptime(date_str, "%Y-%m-%d")
            return start_of_week.date() <= session_date.date() <= end_of_week.date()
        except Exception:
            return False

    def _duration_to_minutes(self, duration_str):
        """
        Convert HH:MM duration string to total minutes.

        Args:
            duration_str (str): Duration string in "HH:MM" format.

        Returns:
            int: Total duration in minutes.
        """
        try:
            h, m = duration_str.split(":")
            return int(h) * 60 + int(m)
        except Exception:
            return 0

    def _format_minutes(self, mins):
        """
        Format a number of minutes into "Xh Ym" string.

        Args:
            mins (int): Total minutes.

        Returns:
            str: Formatted time string.
        """
        if mins == 0:
            return ""
        h = mins // 60
        m = mins % 60
        if h and m:
            return f"{h}h {m}m"
        elif h:
            return f"{h}h"
        else:
            return f"{m}m"

    # ───────────────────────────────────────────────────────────────────
