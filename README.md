# Kairos – A Minimal CLI Time Tracker

> **Kairos** is a fast, terminal-first time tracking tool. It helps you capture your work sessions, tag tasks, and view productivity summaries without distractions or bloat.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Examples](#examples)
- [Data Format](#data-format)
- [Ideas for Future Work](#ideas-for-future-work)
- [License](#license)

---

## Overview

Kairos is a Python CLI utility for logging your task sessions with start/stop timers, tagging them for later review, and generating clean daily or weekly summaries. It's built to be minimal, readable, and easy to customize or extend.

---

## Features

- Start/stop time tracking
- Add task names and optional tags
- Export session data to `.json` or `.csv`
- View daily and weekly summaries
- Dependency-light (only needs `rich`)
- Zero distractions (terminal-first)

---

## Installation

Clone the repo:

```bash
git clone https://github.com/luanbartole/kairos.git
cd kairos
```

Install dependencies (only `rich`):

```bash
pip install rich
```

Run with:

```bash
python kairos.py <command> [options]
```

---

## Usage

Start tracking a task:

```bash
python kairos.py start "Write blog post" --tag writing
```

Stop tracking:

```bash
python kairos.py stop
```

View summaries:

```bash
python kairos.py summary --today
python kairos.py summary --week
```

Export your logs:

```bash
python kairos.py export --format csv --output logs/my_sessions.csv
```

---

## Commands

| Command   | Description                            |
|---------- |----------------------------------------|
| `start`   | Start a timer for a task (with optional tag) |
| `stop`    | Stop current timer and log the session |
| `summary` | Show daily or weekly summaries         |
| `export`  | Export session logs to JSON or CSV     |

---

## Examples

Start a task:

```bash
python kairos.py start "Fix bug #203" --tag dev
```

Stop the timer:

```bash
python kairos.py stop
```

Show weekly summary:

```bash
python kairos.py summary --week
```

Export to CSV:

```bash
python kairos.py export --format csv --output exports/week25.csv
```

---

## Data Format

### JSON (default)

```json
[
  {
    "date": "2025-06-29",
    "start": "09:00",
    "end": "10:45",
    "duration": "01:45",
    "task": "Write documentation",
    "tag": "writing"
  }
]
```

### CSV

```
date,start,end,duration,task,tag
2025-06-29,09:00,10:45,01:45,Write documentation,writing
```

---

## Ideas for Future Work

- Project-based tracking (`project@task`)
- Editable session history / undo
- Web or GUI productivity dashboards
- Configurable presets (tag shortcuts, output folders, time format)

---

## License

MIT License. See [LICENSE](./LICENSE) for details.

---

> “Kairos” (καιρός) is Greek for the *right or opportune moment*. Don’t just track time — **own it**.