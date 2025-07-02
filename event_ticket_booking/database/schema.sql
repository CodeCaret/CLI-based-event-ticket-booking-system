-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0, -- 0 = user, 1 = admin
    user_id TEXT UNIQUE
);

-- Events Table
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    event_price REAL NOT NULL,
    location TEXT NOT NULL,
    date_time TEXT NOT NULL,
    total_seats INTEGER NOT NULL,
    event_id TEXT UNIQUE
);

-- Tickets Table
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    price REAL NOT NULL,
    booking_time TEXT NOT NULL,
    ticket_id TEXT UNIQUE,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);
