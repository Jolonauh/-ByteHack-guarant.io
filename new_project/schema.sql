DROP TABLE IF EXISTS posts;

CREATE TABLE warranty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    website TEXT NOT NULL,
    startdate TIME NOT NULL,
    enddate TIME NOT NULL,
    category TEXT
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    warranties TEXT 
);