CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    user_name TEXT UNIQUE,
    email TEXT UNIQUE,
    hashed_password TEXT UNIQUE,
    user_role TEXT
);

CREATE TABLE room(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number INTEGER UNIQUE,
    room_description TEXT,
    room_type TEXT,
    bed_count INTEGER,
    price REAL,
    facilities TEXT,
    is_available BOOLEAN
);

CREATE TABLE room_photo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER,
    photo_url TEXT,

    FOREIGN KEY (room_id) REFERENCES room(id)
);

CREATE TABLE room_service(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_service_name TEXT UNIQUE,
    room_service_description TEXT,
    price REAL,
    is_available BOOLEAN
);

CREATE TABLE service_order(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    room_id INTEGER,
    service_id INTEGER,
    order_date DATETIME DEFAULT (DATETIME('now')),
    order_status TEXT DEFAULT "in processing",

    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(room_id) REFERENCES room(id),
    FOREIGN KEY(service_id) REFERENCES room_service(id)
);

CREATE TABLE booking(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    room_id INTEGER,
    booking_date DATETIME DEFAULT (DATETIME('now')),
    check_in_date DATETIME,
    check_out_date DATETIME,

    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(room_id) REFERENCES room(id)
);