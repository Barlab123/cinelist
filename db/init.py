import sqlite3
from flask import g, current_app

import click
import requests

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

##########################################
# EXTERNAL API


def download_data():
    db = get_db()

    api_urls = [
        ("Akcja", "https://api.sampleapis.com/movies/action"),
        ("Komedia", "https://api.sampleapis.com/movies/comedy"),
        ("Dramat", "https://api.sampleapis.com/movies/drama"),
        ("Horror", "https://api.sampleapis.com/movies/horror"),
        ("Animacja", "https://api.sampleapis.com/movies/animation"),
    ]

    inserted_count = 0
    skipped_count = 0

    for genre, url in api_urls:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        payload = response.json()

        if isinstance(payload, list):
            movies = payload
        elif isinstance(payload, dict):
            movies = (
                payload.get("results")
                or payload.get("movies")
                or payload.get("data")
                or []
            )
        else:
            movies = []

        for movie in movies[:30]:
            if isinstance(movie, dict):
                title = (
                    movie.get("title")
                    or movie.get("name")
                    or movie.get("Title")
                    or ""
                )
            elif isinstance(movie, str):
                title = movie
            else:
                skipped_count += 1
                continue

            title = str(title).strip()

            if len(title) < 4:
                skipped_count += 1
                continue

            existing_movie = db.execute(
                "SELECT id FROM tasks WHERE title = ?",
                [title],
            ).fetchone()

            if existing_movie:
                skipped_count += 1
                continue

            db.execute(
                """
                INSERT INTO tasks(title, done, genre)
                VALUES (?, ?, ?)
                """,
                [title, 0, genre],
            )

            inserted_count += 1

    db.commit()

    return inserted_count, skipped_count
@click.command("download-data")
def download_data_command():
    try:
        inserted_count, skipped_count = download_data()

        click.echo(f"Pobrano dane z API.")
        click.echo(f"Dodano filmów: {inserted_count}")
        click.echo(f"Pominięto duplikatów / błędnych rekordów: {skipped_count}")

    except requests.RequestException as error:
        click.echo(f"Błąd pobierania danych z API: {error}", err=True)


def download_data_command_init(app):
    app.cli.add_command(download_data_command)
