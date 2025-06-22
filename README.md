## 1. Clear Goal Setting
> Write a 1-2 sentence summary of your goal.

Kairos is a CLI tool to track time spent on projects and tasks throughout the days and weeks to generate insights
on how to make a better use of your time to achieve your goals. 

> Why am I making this project?

I want to learn how to build a complete project from scratch without relying on full tutorials, including
setting up a proper folder structure, using Git for version control, and understanding the development workflow
of an application.

My goal is to create a time-tracking tool that I can both use personally and add to my portfolio.

> What problem does it solve?

Solves the problem of untracked or disorganized time by letting users start/stop timers, tag sessions, and export clear summaries, making time use visible, structured, and easy to review. 

> Who is this for?

Developers, students, and productivity-focused individuals who prefer a fast, minimalist, terminal-based way to track and analyze how they spend their time.

> What will make it valuable?

Kairos is valuable because it offers a fast, light, and distraction-free way to track and organize work.

## 2. User Stories
> User should be able to...
- start a timer w/ task and tag (session)
- stop current timer (session)
- edit session start and end
- delete session logs
- show daily or weekly summary
- show monthly summary
- export time logs
- import time logs
> Nice to haves
- make a note for future self _(ex: do at least 30min of reading.)_
- delete note
- notification after each set period of time

## 3. Data Models
each timer will generate a session, which will be stored in a CSV or JSON.

### Session (Model)
```
date: 2025-06-22
start: 09:00
end: 10:30
duration: 01:30
task: write a book
tag: chapter 1
```

## 4. Minimum Viable Product (MVP)
- start a timer w/ task and tag (session)
- stop current timer (session)
- show daily or weekly time summary
- export time logs

## 5. Draw a Simple Prototype

### command syntax
```bash
python kairos.py <command> [options]
```

### start a timer w/ task and tag (session)
```bash
python kairos.py start "Build login page" --tag coding
```

### stop current timer (session)
```bash
python kairos.py stop
```

### show daily or weekly time summary
```bash
python kairos.py summary --today
python kairos.py summary --week
```

```
Daily Summary – 2025-06-22
╒═══════════════╤══════════╤══════════════════════╕
│ Time          │ Tag      │ Task                 │
╞═══════════════╪══════════╪══════════════════════╡
│ 09:00–10:00   │ coding   │ Build login page     │
│ 10:15–11:00   │ writing  │ Draft proposal       │
│ 14:00–15:30   │ meeting  │ Client sync          │
╘═══════════════╧══════════╧══════════════════════╛

Grouped by Tag
╒══════════╤════════════╕
│ Tag      │ Duration   │
╞══════════╪════════════╡
│ coding   │ 1h 00m     │
│ writing  │ 45m        │
│ meeting  │ 1h 30m     │
╘══════════╧════════════╛

Total: 3h 15m
```

```
Weekly Summary – June 17–23
╒══════════╤═══════╤═══════╤═══════╤═══════╤══════╤══════╤════════╕
│          │ Mon   │ Tue   │ Wed   │ Thu   │ Fri  │ Sat  │ Sun    │
╞══════════╪═══════╪═══════╪═══════╪═══════╪══════╪══════╪════════╡
│ coding   │ 2h    │ —     │ 1h    │ —     │ 2h   │ —    │ 15m    │
├──────────┼───────┼───────┼───────┼───────┼──────┼──────┼────────┤
│ writing  │ —     │ 30m   │ —     │ —     │ 1h   │ —    │ —      │
├──────────┼───────┼───────┼───────┼───────┼──────┼──────┼────────┤
│ meeting  │ —     │ 45m   │ —     │ —     │ —    │ —    │ —      │
├──────────┼───────┼───────┼───────┼───────┼──────┼──────┼────────┤
│ Total    │ 2h10m │ 45m   │ 1h30m │ —     │ 3h   │ —    │ 2h15m  │
╘══════════╧═══════╧═══════╧═══════╧═══════╧══════╧══════╧════════╛

```

### export time logs
```bash
python kairos.py export [--format csv|json] [--output /path/to/filename]
# Export time logs (default: CSV to default folder; use --format to change format)
# If you provide just a filename, it's saved in the default folder.
# If you provide a full or relative path, it's saved there instead.

# Example Cases:

python kairos.py export
# Exports as CSV to the default folder (e.g., kairos_export.csv)

python kairos.py export --format json
# Exports as JSON to the default folder (e.g., kairos_export.json)

python kairos.py export --output report.csv
# Exports as CSV to the default folder with the custom filename "report.csv"

python kairos.py export --format csv --output /home/user/timesheets/week.csv
# Exports as CSV to the specified absolute path
```

 CSV (default)

```
date,start,end,duration,task,tag
2025-06-19,09:00,10:30,01:30,Write report,writing
```

 JSON

```json
[
  {
    "date": "2025-06-19",
    "start": "09:00",
    "end": "10:30",
    "duration": "01:30",
    "task": "Write report",
    "tag": "writing"
  }
]
```

## 6. Define High Level Architecture
> How wil this thing live in the world

this will be a CLI application, local-only, with the following components.
```
         ┌────────────┐
         │ User Input │ ← CLI (argparse)
         └────┬───────┘
              │
              ▼
       ┌────────────┐
       │  Commands  │  (start, stop, summary, export)
       └────┬───────┘
            │
   ┌────────▼──────────┐
   │   Tracker Engine  │
   │  (session logic)  │
   └────────┬──────────┘
            │
   ┌────────▼────────────┐
   │  Data Storage Layer │ ← JSON / CSV file (local)
   └────────┬────────────┘
            │
   ┌────────▼──────────┐
   │  Output Formatter │ ← rich (tables)
   └───────────────────┘

```


## 7. Technologies
I will use Python as the programming language and a local file (CSV or JSON) to store data.

### Python modules:
- `argparse` for CLI parsing.
- `datetime`  for time-related functions.
- `os` to handle file paths, check file existence, default export directories.
- `json` save/load logs in JSON format.
- `csv` to save logs in csv format.
- `rich` to format the summary tables in the terminal. _[external library = needs installing]_




