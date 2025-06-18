# Chrome History Cleaner - Retain Last 7 Days

A Python utility to selectively clear Google Chrome browsing history for the default profile, retaining only the last 7 days of history. This script safely removes older browsing records from your Chrome History SQLite database while preserving recent history, helping you manage your browser data effectively.

---

## Features

- Automatically detects the Chrome default profile History database location based on your operating system (Windows, macOS, Linux).
- Deletes browsing history entries older than 7 days, preserving recent activity.
- Handles both visit timestamps and URL entries to maintain database integrity.
- Creates a backup of your Chrome History database before making any changes for safety.
- Compact and optimize the Chrome History SQLite database after cleanup.
- Clear console output with the number of deleted entries and operations status.

---

## Installation & Usage

### Prerequisites

- Python 3.x installed on your system.

### Usage

1. **Close Google Chrome** completely before running the script to avoid database locks.

2. Download or clone this repository.

3. Run the script from the command line:

   ```bash
   python clear_chrome_history_last_7_days.py
