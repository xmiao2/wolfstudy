PRAGMA foreign_keys = on; -- Enforce foreign key constraints

DROP TABLE IF EXISTS questions;
CREATE TABLE questions (
    -- id is an alias for ROWID because it is of type INTEGER PRIMARY KEY;
    -- it auto-increments by default. See SQLite3 documentation.
    id       INTEGER PRIMARY KEY,
    title    TEXT NOT NULL,
    content  TEXT NOT NULL
);

DROP TABLE IF EXISTS answers;
CREATE TABLE answers (
    id           INTEGER PRIMARY KEY,
    question_id  INTEGER,
    content      TEXT NOT NULL,
    FOREIGN KEY(question_id) REFERENCES questions(id)
);
