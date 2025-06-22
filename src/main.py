import argparse
import datetime
from idlelib.debugger_r import start_debugger

import rich
import json
import csv
import os

def handle_start(args):
    print(f"Starting timer for task: {args.task} with tag: {args.tag}")

def handle_stop(args):
    print("Stopping current timer.")

def handle_summary(args):
    if args.today:
        print("Showing today's summary.")
    elif args.week:
        print("Showing weekly's summary.")

def handle_export(args):
    print(f"Exporting logs as {args.format} to {args.output} or 'default file'")

# Create the main parser
parser = argparse.ArgumentParser(prog='kairos',
                                 description='Kairos is a CLI tool to track time spent on tasks.',
                                 epilog='For more details and usage examples, visit'
                                        'https://github.com/luanbartole/kairos/”')

# Subparsers (to handle commands)
subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

# ---- START ----
start_parser = subparsers.add_parser('start', help='Start a timer for a task')
start_parser.add_argument('task', help='The task you are working on (in quotes)')
start_parser.add_argument('--tag', '-t', help='Optional tag for this session')
start_parser.set_defaults(func=handle_start)

# ---- STOP ----
stop_parser = subparsers.add_parser('stop', help='Stop the current timer')
stop_parser.set_defaults(func=handle_stop)

# ---- SUMMARY ----
summary_parser = subparsers.add_parser('summary', help='Show time summaries')
group = summary_parser.add_mutually_exclusive_group(required=True)
group.add_argument('--today', action='store_true', help='Show today\'s summary')
group.add_argument('--week', action='store_true', help='Show weekly summary')
summary_parser.set_defaults(func=handle_summary)

# ---- EXPORT ----
export_parser = subparsers.add_parser('export', help='Export logs to CSV or JSON')
export_parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='Export format')
export_parser.add_argument('--output', help='Path or filename to export the logs')
export_parser.set_defaults(func=handle_export)

# Parse and run the appropriate handler
def main():
    args = parser.parse_args()
    args.func(args)









