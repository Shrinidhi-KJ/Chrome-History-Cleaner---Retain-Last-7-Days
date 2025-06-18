import os
import sys
import time
import shutil
import sqlite3

def get_chrome_history_path():
    """Return the path to Chrome's default profile History file based on OS."""
    if sys.platform == 'win32':
        local_app_data = os.getenv('LOCALAPPDATA')
        if not local_app_data:
            raise Exception("Could not find LOCALAPPDATA environment variable.")
        return os.path.join(local_app_data, "Google", "Chrome", "User Data", "Default", "History")
    elif sys.platform == 'darwin':
        home = os.path.expanduser('~')
        return os.path.join(home, "Library", "Application Support", "Google", "Chrome", "Default", "History")
    else:  # Assume Linux
        home = os.path.expanduser('~')
        path = os.path.join(home, ".config", "google-chrome", "Default", "History")
        if not os.path.exists(path):
            path = os.path.join(home, ".config", "chromium", "Default", "History")
        return path

def unix_time_to_chrome_time(unix_time):
    """
    Convert Unix timestamp (seconds since 1970) to Chrome timestamp:
    microseconds since January 1, 1601.
    """
    return int((unix_time + 11644473600) * 1_000_000)

def clear_old_history(days=7):
    history_path = get_chrome_history_path()
    if not os.path.exists(history_path):
        print(f"Chrome History file not found at: {history_path}")
        return

    # Backup the History file before making changes
    backup_path = history_path + ".bak"
    if not os.path.exists(backup_path):
        shutil.copy2(history_path, backup_path)
        print(f"Backup of History file created at: {backup_path}")
    else:
        print(f"Backup already exists at: {backup_path}")

    threshold_unix = time.time() - (days * 24 * 60 * 60)
    threshold_chrome = unix_time_to_chrome_time(threshold_unix)

    try:
        conn = sqlite3.connect(history_path)
        cursor = conn.cursor()

        # Delete visits older than threshold
        cursor.execute("DELETE FROM visits WHERE visit_time < ?", (threshold_chrome,))
        print(f"Deleted {cursor.rowcount} visits older than {days} days.")

        # Delete URLs without any visits (orphans)
        cursor.execute("""
            DELETE FROM urls
            WHERE id NOT IN (SELECT url FROM visits)
        """)
        print(f"Deleted {cursor.rowcount} orphan URLs.")

        conn.commit()

        # Vacuum to optimize database size after deletion
        cursor.execute("VACUUM")
        print("Database vacuumed to optimize size.")

    except sqlite3.OperationalError as e:
        print("SQLite operational error:", e)
        print("Please ensure Chrome is fully closed before running this script.")
    except Exception as ex:
        print("An error occurred:", ex)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Clearing Chrome browsing history older than last 7 days...")
    clear_old_history(7)
    print("Done.")

