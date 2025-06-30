from pathlib import Path
from src.session_tracker import SessionTracker
from src.terminal_display import TerminalDisplay
from rich.prompt import Prompt


class KairosManager:
    """
    Handles all CLI operations and mediates between session tracking and terminal display.
    """

    def __init__(self):
        self.tracker = SessionTracker()
        self.display = TerminalDisplay()

    def start(self, task, tag):
        if Path(self.tracker.current_file).exists():
            self.display.console.print(
                "[red]A timer is already running. Stop it before starting a new one.[/red]"
            )
            return
        message = self.tracker.start(task, tag)
        self.display.console.print(f"[green]{message}[/green]")

    def stop(self):
        try:
            message = self.tracker.stop()
            self.display.console.print(f"[green]{message}[/green]")
        except FileNotFoundError as e:
            self.display.console.print(f"[red]{e}[/red]")

    def summary(self, today=False, week=False):
        data = self.tracker.get_sessions()
        if not data:
            self.display.console.print("[yellow]No sessions found.[/yellow]")
            return

        if today:
            self.display.render_today_summary(data)
        elif week:
            self.display.render_weekly_summary(data)

    def export(self, format, output_path):
        try:
            message = self.tracker.export(format, output_path)
            self.display.console.print(f"[green]{message}[/green]")
        except FileNotFoundError as e:
            if "does not exist" in str(e):
                create = Prompt.ask(f"{e} Create it?", choices=["y", "n"], default="n")
                if create == 'y':
                    path = Path(output_path or '')
                    path.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        message = self.tracker.export(format, output_path)
                        self.display.console.print(f"[green]{message}[/green]")
                    except Exception as ex:
                        self.display.console.print(f"[red]Error exporting: {ex}[/red]")
                else:
                    self.display.console.print("[red]Export cancelled[/red]")
            else:
                self.display.console.print(f"[red]{e}[/red]")
        except Exception as e:
            self.display.console.print(f"[red]Unexpected error: {e}[/red]")
