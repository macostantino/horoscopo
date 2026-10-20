"""Persistencia SQLite de horóscopos generados (versiones, publicado, fecha de creación)."""
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime

DB_PATH = os.environ.get("HOROSCOPO_DB", os.path.join("data", "horoscopo.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS horoscopes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    published INTEGER NOT NULL DEFAULT 0,
    UNIQUE (year, month, version)
);
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    horoscope_id INTEGER NOT NULL REFERENCES horoscopes(id) ON DELETE CASCADE,
    sign TEXT NOT NULL,
    category TEXT NOT NULL,
    day TEXT NOT NULL,
    text TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_entries_h ON entries(horoscope_id);
CREATE INDEX IF NOT EXISTS idx_entries_text ON entries(text);
"""


@contextmanager
def connect(path=None):
    path = path or DB_PATH
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def used_texts(path=None):
    """Todos los textos ya guardados (historial completo)."""
    with connect(path) as c:
        return {r[0] for r in c.execute("SELECT DISTINCT text FROM entries")}


def used_sentences(path=None):
    """Todas las oraciones ya guardadas (historial completo), separadas de cada texto."""
    from engine import split_sentences
    out = set()
    for text in used_texts(path):
        out.update(split_sentences(text))
    return out


def save_horoscope(year, month, entries, path=None):
    """Guarda una nueva versión del mes y devuelve su id."""
    with connect(path) as c:
        row = c.execute(
            "SELECT COALESCE(MAX(version), 0) FROM horoscopes WHERE year=? AND month=?",
            (year, month),
        ).fetchone()
        version = row[0] + 1
        cur = c.execute(
            "INSERT INTO horoscopes (year, month, version, created_at, published) VALUES (?,?,?,?,0)",
            (year, month, version, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        hid = cur.lastrowid
        c.executemany(
            "INSERT INTO entries (horoscope_id, sign, category, day, text) VALUES (?,?,?,?,?)",
            [(hid, e.sign, e.category, e.day.isoformat(), e.text) for e in entries],
        )
        return hid


def list_horoscopes(path=None):
    with connect(path) as c:
        return [dict(r) for r in c.execute(
            "SELECT * FROM horoscopes ORDER BY year DESC, month DESC, version DESC")]


def get_horoscope(hid, path=None):
    with connect(path) as c:
        r = c.execute("SELECT * FROM horoscopes WHERE id=?", (hid,)).fetchone()
        return dict(r) if r else None


def get_entries(hid, path=None):
    """Entradas en el orden del Excel original: signo (según content.SIGNS), día, categoría."""
    from content import CATEGORIES, SIGNS
    with connect(path) as c:
        rows = [dict(r) for r in c.execute("SELECT sign, category, day, text FROM entries WHERE horoscope_id=?", (hid,))]
    rows.sort(key=lambda r: (SIGNS.index(r["sign"]), r["day"], CATEGORIES.index(r["category"])))
    return rows


def set_published(hid, published, path=None):
    with connect(path) as c:
        c.execute("UPDATE horoscopes SET published=? WHERE id=?", (1 if published else 0, hid))


def delete_horoscope(hid, path=None):
    with connect(path) as c:
        c.execute("DELETE FROM horoscopes WHERE id=?", (hid,))
