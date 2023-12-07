CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    content TEXT,
    guild INTEGER,
    author INTEGER,
    created_at INTEGER
)