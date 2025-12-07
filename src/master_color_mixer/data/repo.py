# implement a SQLite repository/database
# responsible for palette CRUD, enforcing MAX_COLORS

import sqlite3 # https://docs.python.org/3/library/sqlite3.html
from pathlib import Path
from typing import List

from .palette_catalog import BASE_COLORS, ColorDef

# define global variables
DB_FILENAME = "mcm_palette.db"
MAX_COLORS = 20
ColorRecord = ColorDef


class PaletteRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        if db_path is None:
            db_path = DB_FILENAME
        self.db_path = Path(db_path)
        self._init_db()

    # connection management
    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    # possible todo - rewrite using with for transaction safety ()
    def _init_db(self) -> None:
        connection = self._get_connection()
        try:
            current = connection.cursor()
            current.execute(
                """
                CREATE TABLE IF NOT EXISTS palette (
                    name TEXT PRIMARY KEY,
                    r INTEGER NOT NULL,
                    y INTEGER NOT NULL,
                    b INTEGER NOT NULL,
                    is_base INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            connection.commit()

            # seed base colors if table empty
            current.execute("SELECT COUNT(*) FROM palette")
            count = current.fetchone()[0]
            if count == 0:
                for color in BASE_COLORS:
                    current.execute(
                        "INSERT INTO palette (name, r, y, b, is_base) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (color.name, color.r, color.y, color.b, 1 if color.is_base else 0),
                    )
                connection.commit()
        finally:
            connection.close()

    # public API
    def load_palette(self) -> List[ColorRecord]:
        connection = self._get_connection()
        try:
            current = connection.cursor()
            current.execute(
                "SELECT name, r, y, b, is_base "
                "FROM palette ORDER BY is_base DESC, name ASC" # order by base first then names
                ) # possible todo - order by an ID so that the unlock order is preserved in palette
            rows = current.fetchall()
        finally:
            connection.close()

        result: List[ColorRecord] = []
        for name, r, y, b, is_base in rows:
            result.append(ColorRecord(name, int(r), int(y), int(b), bool(is_base)))
        return result

    def save_palette(self, colors: List[ColorRecord]) -> None:
        palette_list = list(colors)[:MAX_COLORS]
        connection = self._get_connection()
        try:
            current = connection.cursor()
            current.execute("DELETE FROM palette")
            for color in palette_list:
                current.execute(
                    "INSERT INTO palette (name, r, y, b, is_base) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (color.name, color.r, color.y, color.b, 1 if color.is_base else 0),
                )
            connection.commit()
        finally:
            connection.close()

    def add_color(self, color: ColorRecord) -> bool:
        connection = self._get_connection()
        try:
            current = connection.cursor()

            # enforce max size
            current.execute("SELECT COUNT(*) FROM palette")
            count = current.fetchone()[0]
            if count >= MAX_COLORS:
                return False

            # avoid duplicates by name
            current.execute("SELECT 1 FROM palette WHERE name = ?", (color.name,))
            if current.fetchone():
                return False

            current.execute(
                "INSERT INTO palette (name, r, y, b, is_base) "
                "VALUES (?, ?, ?, ?, ?)",
                (color.name, color.r, color.y, color.b, 1 if color.is_base else 0),
            )
            connection.commit()
            return True
        finally:
            connection.close()

    def clear_palette_to_base(self) -> None:
        self.save_palette(list(BASE_COLORS))