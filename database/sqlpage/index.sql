-- SQLPage index: Users list page
-- Renders a title and description, then a table of users from SQLite.

-- Page header section
SELECT
  'title'   AS component,
  'Users'   AS title,
  'A simple list of users served by SQLPage from the SQLite database.' AS subtitle;

-- Users table section
SELECT
  'table' AS component,
  'Users' AS title;

-- Table data
SELECT
  id,
  name,
  email
FROM users
ORDER BY id;
