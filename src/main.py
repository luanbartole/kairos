import argparse
from src.kairos_manager import KairosManager

manager = KairosManager()

# Handlers
def handle_start(args):
    manager.start(args.task, args.tag)

def handle_stop(args):
    manager.stop()

def handle_summary(args):
    manager.summary(today=args.today, week=args.week)

def handle_export(args):
    manager.export(args.format, args.output)

# CLI parser
parser = argparse.ArgumentParser(
    prog="kairos",
    description="Kairos is a CLI tool to track time spent on tasks.",
    epilog="For more details and usage examples, visit https://github.com/luanbartole/kairos/",
)

subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

# Start
start_parser = subparsers.add_parser("start", help="Start a timer for a task")
start_parser.add_argument("task", help="The task you are working on (in quotes)")
start_parser.add_argument("--tag", "-t", help="Optional tag for this session")
start_parser.set_defaults(func=handle_start)

# Stop
stop_parser = subparsers.add_parser("stop", help="Stop the current timer")
stop_parser.set_defaults(func=handle_stop)

# Summary
summary_parser = subparsers.add_parser("summary", help="Show time summaries")
group = summary_parser.add_mutually_exclusive_group(required=True)
group.add_argument("--today", action="store_true", help="Show today's summary")
group.add_argument("--week", action="store_true", help="Show weekly summary")
summary_parser.set_defaults(func=handle_summary)

# Export
export_parser = subparsers.add_parser("export", help="Export logs to CSV or JSON")
export_parser.add_argument("--format", choices=["csv", "json"], default="json", help="Export format")
export_parser.add_argument("--output", help="Path or filename to export the logs")
export_parser.set_defaults(func=handle_export)

# Entrypoint
def main():
    args = parser.parse_args()
    args.func(args)
    print()

if __name__ == "__main__":
    main()
