# db_visualizer - Quick Start

This is a minimal note to ensure the preview can start successfully.

Steps:
1) Install dependencies (non-interactive):
   npm ci --no-audit --no-fund

2) Start the server:
   npm start

The server binds to 0.0.0.0 on port 5001 (node server.js --host 0.0.0.0) and expects optional environment files like sqlite.env in this folder.

Notes:
- The express module error ("Cannot find module './lib/express'") is resolved by installing dependencies.
- Do not modify unrelated code or delete files; this project uses a minimal Node server solely for quick DB visualization.
