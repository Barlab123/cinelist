import sqlite3
from flask import g

DATABASE = "movies.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
done INTEGER NOT NULL DEFAULT 0 CHECK (done in (0, 1)),
genre TEXT NOT NULL DEFAULT 'Inne',
created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_tasks_done ON tasks(done);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
"""

def get_db():
    if "db" not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.db = conn
    return g.db

def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript(SCHEMA_SQL)
    db.commit()

def init_db_command_init(app):
    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        print("Baza danych Watchlist została zainicjalizowana.")

def seed_db_comand_init(app):
    @app.cli.command("seed-db")
    def seed_db_command():
        db = get_db()
        howManyRows = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if howManyRows == 0:
            tasks = [
                ["Inception", 0, "Sci-Fi"],
                ["The Godfather", 1, "Dramat"],
                ["Interstellar", 0, "Sci-Fi"],
                ["Parasite", 0, "Thriller"],
                ["The Dark Knight", 1, "Akcja"],
            ]
            db.executemany("INSERT INTO tasks(title,done,genre) VALUES (?, ?, ?)", tasks)
            db.commit()
            print("✔ Dodano przykładowe filmy.")
        else:
            print("Tabela nie jest pusta, pomijam seed.")
