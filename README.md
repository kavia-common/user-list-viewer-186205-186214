# User List Viewer (SQLPage + SQLite)

## Overview
This project is a simple SQLPage web app that displays a list of users from an SQLite database. SQLPage serves a web page directly from SQL files, without a traditional backend or frontend. The page shows all users in a table with a clear title and description.

- Database: SQLite with a users table containing id, name, and email
- Web: SQLPage rendering from SQL files in database/sqlpage
- Seeding: Handled by a Python script that is idempotent

## Prerequisites
- SQLPage CLI installed
  - Official website: https://sql.page
  - Installation script: curl -fsSL https://get.sql.page/install.sh | bash -s -- -y
- OR Docker (for running SQLPage without a local install)
  - Docker image: ghcr.io/sqlpage/sqlpage:latest

## Initialize or Verify the Database
1) Change directory to the database folder:
   cd user-list-viewer-186205-186214/database

2) Run the initialization script (reads database/db_connection.txt to get the SQLite path and seeds the users table if empty):
   python3 init_db.py

3) Confirm the printed count:
   You should see output like:
   SELECT COUNT(*) FROM users -> 5

## Confirm the Database Path
- The authoritative database path is stored in:
  user-list-viewer-186205-186214/database/db_connection.txt

- Look for the "File path:" line indicating the absolute path to myapp.db. In this repository it points to:
  /home/kavia/workspace/code-generation/user-list-viewer-186205-186214/database/myapp.db

- The SQLPage configuration uses this absolute path in database/sqlpage/config.yaml.

## Start SQLPage (Native CLI)
Run SQLPage from the database directory so relative paths resolve correctly:

cd user-list-viewer-186205-186214/database
sqlpage --config sqlpage/config.yaml

- The provided configuration binds SQLPage to port 5001 (see database/sqlpage/config.yaml).

## Start SQLPage (Docker Alternative)
From the same database directory:

docker run --rm -p 5001:5001 \
  -v "$PWD":/app \
  -w /app/database \
  ghcr.io/sqlpage/sqlpage:latest \
  sqlpage --config sqlpage/config.yaml

Notes:
- This mounts the repository into /app and runs from /app/database so the config.yaml and DB path align with the bound volume.

## Verify in the Browser
Open:
http://localhost:5001

You should see the Users page showing columns: id, name, email.

## Troubleshooting
- Port already in use:
  - SQLPage is set to listen on 5001 by default in database/sqlpage/config.yaml.
  - If port 5001 is in use, update server.port in database/sqlpage/config.yaml to another free port, then re-run SQLPage. Remember to adjust the -p PORT:PORT mapping in the Docker command if using Docker.

- Database path mismatch:
  - Ensure the absolute path in database/sqlpage/config.yaml (database.connection.filename) matches the "File path:" in database/db_connection.txt.
  - If you move the project, update both db_connection.txt and config.yaml accordingly.
  - Re-run python3 init_db.py to verify the count output.

- SQLPage not installed:
  - Use the Docker alternative above, or install via the official installer:
    curl -fsSL https://get.sql.page/install.sh | bash -s -- -y

- Preview system note:
  - The preview system starts on port 5001 by default. If your environment reserves that port, pick an alternative and update config.yaml.

## Files Created/Used
- database/sqlpage/config.yaml
  - Sets SQLPage server host/port and points to the absolute SQLite DB path.
- database/sqlpage/index.sql
  - SQLPage content to render the Users table (id, name, email).
- database/init_db.py
  - Initializes the database and seeds sample data. Safe to run multiple times; will not duplicate rows.
- database/db_connection.txt
  - Authoritative absolute path to the SQLite database (myapp.db).

## Project Structure (relevant parts)
- user-list-viewer-186205-186214/
  - database/
    - myapp.db
    - init_db.py
    - db_connection.txt
    - sqlpage/
      - config.yaml
      - index.sql