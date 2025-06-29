import argparse
from datetime import datetime
import os
import json


def save_session(session, filename="sessions.json"):
    sessions = []

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                sessions = json.load(f)
            except json.JSONDecodeError:
                # file exists but is empty or invalid, treat as empty list
                sessions = []

    # Append the new session
    sessions.append(session)

    # Write updated list back to file
    with open(filename, "w") as f:
        json.dump(sessions, f, indent=2)


def handle_start(args):
    # format tag and general tag fallback if no tag is given
    tag = args.tag.lower() if args.tag else "general"
    now = datetime.now()

    # Stores the session
    print(f"Starting timer for task [{args.task}] with tag [{tag}]")
    with open("current_session.json", mode="w") as f:
        session = {
            "date": now.strftime("%Y-%m-%d"),
            "start": now.strftime("%H:%M"),
            "task": args.task,
            "tag": tag
        }
        json.dump(session, f, indent=2)


def handle_stop(args):
    # Check for active timers
    if not os.path.exists("current_session.json"):
        print("No active timer found. Start a timer first using the 'start' command.")
        return
    else:
        print("Stopping current timer.")

    # Update session (end time and duration)
    with open("current_session.json") as f:
        session = json.load(f)

        # Get the start and end time strings
        start_str = session['start']
        end_str = datetime.now().strftime("%H:%M")

        # Parse the strings into datetime objects (time only)
        start_time = datetime.strptime(start_str, "%H:%M")
        end_time = datetime.strptime(end_str, "%H:%M")

        # calculate the time difference (timedelta) and format the duration as "HH:MM"
        duration = end_time - start_time
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        duration_str = f"{hours:02d}:{minutes:02d}"

        # adds end time and duration
        session.update({
            "end": end_str,
            "duration": duration_str
        })

        print(f"Session saved: {session['task']} [{session['duration']}]")

        # Save to all sessions file and delete the temporary session file.
        save_session(session)
    os.remove("current_session.json")



def handle_summary(args):
    if args.today:
        print("Showing today's summary.")
    elif args.week:
        print("Showing weekly's summary.")


def handle_export(args):
    print(f"Exporting logs as {args.format} to {args.output or 'default file'}")


# Create the main parser
parser = argparse.ArgumentParser(
    prog="kairos",
    description="Kairos is a CLI tool to track time spent on tasks.",
    epilog="For more details and usage examples, visit https://github.com/luanbartole/kairos/",
)

# Subparsers (to handle commands)
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
export_parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Export format")
export_parser.add_argument("--output", help="Path or filename to export the logs")
export_parser.set_defaults(func=handle_export)


def main():
    args = parser.parse_args()
    args.func(args)
