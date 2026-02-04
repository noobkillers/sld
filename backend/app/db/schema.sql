CREATE TABLE IF NOT EXISTS equipment (
    id TEXT PRIMARY KEY,
    semantic_id TEXT NOT NULL,
    name TEXT NOT NULL,
    equipment_type TEXT NOT NULL,
    rating_json TEXT NOT NULL,
    manufacturer TEXT,
    install_date TEXT,
    criticality INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS connectivity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_id TEXT NOT NULL,
    to_id TEXT NOT NULL,
    relation TEXT NOT NULL,
    FOREIGN KEY(from_id) REFERENCES equipment(id),
    FOREIGN KEY(to_id) REFERENCES equipment(id)
);

CREATE TABLE IF NOT EXISTS timeseries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    metric TEXT NOT NULL,
    value REAL NOT NULL,
    source TEXT NOT NULL,
    FOREIGN KEY(equipment_id) REFERENCES equipment(id)
);

CREATE TABLE IF NOT EXISTS incidents (
    id TEXT PRIMARY KEY,
    equipment_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    severity TEXT NOT NULL,
    summary TEXT NOT NULL,
    root_cause TEXT,
    impact TEXT,
    recommendations TEXT,
    FOREIGN KEY(equipment_id) REFERENCES equipment(id)
);

CREATE TABLE IF NOT EXISTS learning_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id TEXT NOT NULL,
    prediction_type TEXT NOT NULL,
    predicted_value REAL NOT NULL,
    actual_value REAL,
    timestamp TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY(equipment_id) REFERENCES equipment(id)
);
