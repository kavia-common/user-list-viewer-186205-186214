#!/usr/bin/env python3
"""Initialize and seed the SQLite database for the SQLPage app.

This script:
- Reads the SQLite database file path from db_connection.txt (authoritative).
- Ensures a 'users' table exists with the required schema:
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- Inserts 3-5 sample rows only if the table is empty (one INSERT at a time).
- Prints the total user count at the end.

The operations are idempotent: running multiple times will not duplicate rows.
"""

import os
import re
import sqlite3
from typing import Optional, Tuple


DB_INFO_FILE = "db_connection.txt"


# PUBLIC_INTERFACE
def parse_db_path_from_info(file_path: str) -> Optional[str]:
    """Parse the absolute database file path from db_connection.txt.

    The file typically contains lines like:
      # File path: /abs/path/to/myapp.db

    Returns:
        Absolute file path string if found, otherwise None.
    """
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Try to locate explicit "File path: {abs_path}" first
    m = re.search(r"^[#\s]*File path:\s*(.+)$", content, flags=re.MULTILINE)
    if m:
        path = m.group(1).strip()
        if path:
            return path

    # Fallback: try to parse connection string sqlite:/// or sqlite:////abs/path
    m = re.search(r"^[#\s]*Connection string:\s*sqlite:(?://)?/+(.+)$", content, flags=re.MULTILINE)
    if m:
        # Ensure it is absolute if it contains a '/'
        path = m.group(1).strip()
        if path:
            # If path doesn't start with /, make it absolute relative to this directory
            if not path.startswith("/"):
                path = os.path.abspath(path)
            return path

    # Fallback: find python example line: sqlite3.connect('myapp.db')
    m = re.search(r"sqlite3\.connect\(['\"](.+?)['\"]\)", content)
    if m:
        # Resolve relative to current working directory of this script
        rel = m.group(1).strip()
        return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), rel))

    return None


def _connect(db_path: str) -> sqlite3.Connection:
    """Open a SQLite connection to the given path with sane pragmas."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    return conn


def _ensure_users_table(conn: sqlite3.Connection) -> None:
    """Create the users table if it does not exist, matching the required schema."""
    # Create table with exact required column names and constraints
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    # Minimal fix: if an existing database lacks the 'name' column (legacy schema),
    # add it to ensure subsequent INSERTs into (name, email) succeed.
    cur = conn.execute("PRAGMA table_info(users)")
    cols = [row[1] for row in cur.fetchall()]
    if "name" not in cols:
        conn.execute("ALTER TABLE users ADD COLUMN name TEXT")


def _table_is_empty(conn: sqlite3.Connection) -> bool:
    """Check if users table is empty. If table missing, it's treated as empty after creation."""
    cur = conn.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    return count == 0


def _seed_users_if_empty(conn: sqlite3.Connection) -> None:
    """Insert sample users if the table is empty. Use one INSERT per row."""
    if not _table_is_empty(conn):
        return

    # Sample rows (unique emails to preserve idempotency with UNIQUE constraint)
    seed_rows = [
        ("Alice Johnson", "alice@example.com"),
        ("Bob Smith", "bob@example.com"),
        ("Charlie Davis", "charlie@example.com"),
        ("Dana Lee", "dana@example.com"),
        ("Evan Wright", "evan@example.com"),
    ]

    # Insert rows one statement at a time
    for name, email in seed_rows:
        # Use INSERT OR IGNORE to ensure idempotency in case a row exists
        conn.execute(
            "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
            (name, email),
        )

    conn.commit()


def _get_user_count(conn: sqlite3.Connection) -> int:
    """Return total number of users."""
    cur = conn.execute("SELECT COUNT(*) FROM users")
    return int(cur.fetchone()[0])


def resolve_db_path() -> Tuple[Optional[str], str]:
    """Resolve the DB path using db_connection.txt. Returns (db_path, message)."""
    info_file_abs = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_INFO_FILE))
    path = parse_db_path_from_info(info_file_abs)
    if path and os.path.isabs(path):
        return path, f"Using database file: {path}"

    # As a fallback, if not found, assume local myapp.db in this directory
    fallback = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "myapp.db"))
    return fallback, f"db_connection.txt did not provide a valid path. Falling back to {fallback}"


def main():
    """Entrypoint to prepare the SQLite schema and seed data."""
    print("Starting SQLite schema setup and seeding...")

    db_path, resolution_msg = resolve_db_path()
    print(resolution_msg)

    # Ensure parent directory exists (it should already in this setup)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        with _connect(db_path) as conn:
            _ensure_users_table(conn)
            _seed_users_if_empty(conn)
            count = _get_user_count(conn)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise

    print(f"SELECT COUNT(*) FROM users -> {count}")
    print("SQLite initialization complete.")

if __name__ == "__main__":
    main()
