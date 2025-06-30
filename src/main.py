import argparse
from pathlib import Path
from src.session_tracker import SessionTracker
from src.terminal_display import TerminalDisplay

tracker = SessionTracker()
display = TerminalDisplay()

def handle_start(args):
    message = tracker.start(args.task, args.tag)
    display.console.print(f"[green]{message}[/green]")


def handle_stop(args):
    try:
        message = tracker.stop()
        display.console.print(f"[green]{message}[/green]")
    except FileNotFoundError as e:
        display.console.print(f"[red]{e}[/red]")

def handle_summary(args):
    data = tracker.get_sessions()
    if not data:
        display.console.print("[yellow]No sessions found.[/yellow]")
        return

    if args.today:
        display.render_today_summary(data)
        print()
    elif args.week:
        display.render_weekly_summary(data)
        print()

def handle_export(args):
    output_path = args.output or None
    try:
        message = tracker.export(args.format, output_path)
        display.console.print(f"[green]{message}[/green]")
    except FileNotFoundError as e:
        # Handle missing directory with user prompt
        if "does not exist" in str(e):
            create = input(f"{e} Create it? (y/n): ").strip().lower()
            if create == 'y':
                path = Path(output_path or '')
                path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    message = tracker.export(args.format, output_path)
                    display.console.print(f"[green]{message}[/green]")
                except Exception as ex:
                    display.console.print(f"[red]Error exporting: {ex}[/red]")
            else:
                display.console.print("[red]Export cancelled[/red]")
        else:
            display.console.print(f"[red]{e}[/red]")
    except Exception as e:
        display.console.print(f"[red]Unexpected error: {e}[/red]")

# Setup argparse
parser = argparse.ArgumentParser(
    prog="kairos",
    description="Kairos is a CLI tool to track time spent on tasks.",
    epilog="For more details and usage examples, visit https://github.com/luanbartole/kairos/",
)

subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

# ---- START ----
start_parser = subparsers.add_parser("start", help="Start a timer for a task")
start_parser.add_argument("task", help="The task you are working on (in quotes)")
start_parser.add_argument("--tag", "-t", help="Optional tag for this session")
start_parser.set_defaults(func=handle_start)

# ---- STOP ----
stop_parser = subparsers.add_parser("stop", help="Stop the current timer")
stop_parser.set_defaults(func=handle_stop)

# ---- SUMMARY ----
summary_parser = subparsers.add_parser("summary", help="Show time summaries")
group = summary_parser.add_mutually_exclusive_group(required=True)
group.add_argument("--today", action="store_true", help="Show today's summary")
group.add_argument("--week", action="store_true", help="Show weekly summary")
summary_parser.set_defaults(func=handle_summary)

# ---- EXPORT ----
export_parser = subparsers.add_parser("export", help="Export logs to CSV or JSON")
export_parser.add_argument("--format", choices=["csv", "json"], default="json", help="Export format")
export_parser.add_argument("--output", help="Path or filename to export the logs")
export_parser.set_defaults(func=handle_export)

def main():
    args = parser.parse_args()
    args.func(args)
    print()

if __name__ == "__main__":
    main()
