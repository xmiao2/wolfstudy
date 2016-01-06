drop table if exists questions;
create table questions (
	id      INTEGER PRIMARY KEY AUTOINCREMENT,
	title   TEXT NOT NULL,
	content TEXT NOT NULL
);

drop table if exists answers;
create table answers (
	id          INTEGER PRIMARY KEY AUTOINCREMENT,
	question_id INTEGER
	content
);
