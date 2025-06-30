from rich.table import Table
from rich.console import Console
from datetime import datetime, timedelta

class TerminalDisplay():

    def __init__(self):
        self.console = Console()

    def render_today_summary(self, sessions):
        today = datetime.today().strftime('%Y-%m-%d')
        today_sessions = [s for s in sessions if s.get('date') == today]

        if not today_sessions:
            self.console.print("[Bold yellow No sessions for today.[/bold yellow]")
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
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Helper: map dates to weekday names
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        def in_this_week(date_str):
            session_date = datetime.strptime(date_str, "%Y-%m-%d")
            return start_of_week.date() <= session_date.date() <= end_of_week.date()

        week_sessions = [s for s in sessions if in_this_week(s.get("date", ""))]

        if not week_sessions:
            self.console.print("[bold yellow]No sessions for today.[/bold yellow]")
            return

        def duration_to_minutes(duration_str):
            try:
                h, m = duration_str.split(":")
                return int(h) * 60 + int(m)
            except Exception:
                return 0

        summary = {}

        for session in week_sessions:
            tag = session.get("tag", "-")
            date_obj = datetime.strptime(session["date"], "%Y-%m-%d")
            weekday = weekdays[date_obj.weekday()]
            duration_str = session.get("duration", "00:00")
            mins = duration_to_minutes(duration_str)

            if tag not in summary:
                summary[tag] = {day: 0 for day in weekdays}
            summary[tag][weekday] += mins

        table = Table(title=f"Weekly Summary - {start_of_week.strftime('%b %d')}")

        table.add_column("Tag", style="magenta", no_wrap=True)
        for day in weekdays:
            table.add_column(day, justify="center")

        def format_minutes(mins):
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

        for tag, days in summary.items():
            row = [tag] + [format_minutes(days[day]) for day in weekdays]
            table.add_row(*row)

        self.console.print(table)
