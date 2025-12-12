# Run SQLPage for the Users List App

This folder contains the SQLPage configuration and index.sql to render the Users table from the SQLite database.

What’s already done:
- Database file path: /home/kavia/workspace/code-generation/user-list-viewer-186205-186214/database/myapp.db
- Schema verified and aligned to expected columns: id, name, email, created_at
- Seeded 5 users successfully

Quick verification (already performed):
- Ran: python3 init_db.py
- Output: SELECT COUNT(*) FROM users -> 5

Start SQLPage on port 5001 using this config:
- Config: user-list-viewer-186205-186214/database/sqlpage/config.yaml
- Page: user-list-viewer-186205-186214/database/sqlpage/index.sql
- URL to open: http://localhost:5001

Option A: Native SQLPage binary (preferred if installed)
1) sqlpage --config sqlpage/config.yaml

Option B: Docker (if available)
1) docker run --rm -it -p 5001:5001 \
   -v $(pwd)/sqlpage:/app/sqlpage \
   -v /home/kavia/workspace/code-generation/user-list-viewer-186205-186214/database/myapp.db:/app/database/myapp.db \
   -e SQLPAGE_CONFIG=/app/sqlpage/config.yaml \
   ghcr.io/lovasoa/sqlpage:latest

Notes:
- The config.yaml already points to the absolute SQLite DB path.
- The Users table will render columns id, name, email (created_at is stored but not displayed by index.sql).
- If you change the DB path, update sqlpage/config.yaml accordingly.

Troubleshooting:
- If `sqlpage` command not found and Docker not available, install SQLPage via the official script:
  curl -fsSL https://get.sql.page/install.sh | bash -s -- -y

- Network-restricted environments: download the binary from a machine with internet and copy it to /usr/local/bin/sqlpage (chmod +x).
