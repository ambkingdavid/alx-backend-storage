-- Create table if not exist
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    email TEXT NOT NULL UNIQUE,
    name TEXT
);
