# Database Status (SQLite)

- File: /home/kavia/workspace/code-generation/user-list-viewer-186205-186214/database/myapp.db
- Table: users

Schema:
- id INTEGER PRIMARY KEY
- name TEXT NOT NULL
- email TEXT UNIQUE NOT NULL
- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Row count:
- SELECT COUNT(*) FROM users -> 5

Notes:
- Previous schema used "username"; it has been migrated to "name".
- init_db.py is idempotent and will keep the table seeded without duplicates.
