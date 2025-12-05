#implement a SQLite repository/database
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
    # initialize database
    def _init_database(self) -> None:
        connection = self._get_connection()

        # if this is the first run, create base table with base colors
        try:
            cur = connection.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS palette (
                    name TEXT PRIMARY KEY,
                    r INTEGER NOT NULL,
                    g INTEGER NOT NULL,
                    b INTEGER NOT NULL,
                    is_base INTEGER NOT NULL DEFAULT 0
                )
                """
                )
            connection.commit()

            # there is a table, load it or fill it
            cur.execute("SELECT COUNT(*) FROM palette")
            count = cur.fetchone()
            if count == 0:
                for color in BASE_COLORS:
                    cur.execute(
                        # Python's parameterized safe insert
                        "INSERT INTO palette (name, r, y, b, is_base) VALUES (?, ?, ?, ?, ?)",
                        (color.name, color.r, color.y, color.b, 1 if color.is_base else 0),
                        )
                connection.commit()
        finally:
            connection.close() # connection will always close even if there was an error

    #--- public API connections ---
    def load_palette(self) -> List[ColorRecord]:
        connection = self._get_connection()
        try:
            current = connection.cursor()
            current.execute(
                "SELECT name, r, y, b, is_base"
                "FROM palette ORDER BY is_base DESC, name ASC" # order by base first then names
                ) # possible todo - order by an ID so that the unlock order is preserved in palette
            rows = current.fetchall()
        finally:
            connection.close()

        result: List[ColorRecord] = []
        for name, r, y, b, is_base in rows:
            result.append(ColorRecord(name, int(r), int(y), int(b), bool(is_base)))
        return result
    
    #save_palette
    #add_color
    #clear_palette_to_base