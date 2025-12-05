#implement a SQLite repository/database
# responsible for palette CRUD, enforcing MAX_COLORS

import sqlite3
from pathlib import Path
from typing import List

from .palette_catalog import BASE_COLORS #ColorDef

#define global variables
DB_FILENAME = "mcm_palette.db"
MAX_COLORS = 20

class PaletteRepository:
    
    def __init__(self, db_path: str | Path | None = None) -> None:
        if db_path is None:
            db_path = DB_FILENAME
        self.db_path = Path(db_path)
        self._init_db()


    #connection management

    #initialize database

    #public API connections
    #load_palette
    #save_palette
    #add_color
    #clear_palette_to_base