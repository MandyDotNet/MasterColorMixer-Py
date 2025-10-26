# Data Dictionary — MasterColorMixer

This dictionary lists table purposes, columns, types, nullability, defaults, allowed values, indexes, and constraints for the project’s SQLite datastore.

---

## Table: `colors`
**Purpose:** Master list of all colors available to the app (base and discovered).

| Column | Type | Null | Default | Allowed / Notes |
|---|---|---:|---|---|
| `color_id` | INTEGER | NO | — | **PK**; typically `INTEGER PRIMARY KEY` (auto-increment). |
| `name` | TEXT | NO | — | **UNIQUE**; e.g., “Red”, “Purple”. |
| `hex` | TEXT | NO | — | **UNIQUE**; 7-char hex `#RRGGBB`. |
| `is_base` | INTEGER | NO | `0` | Boolean as `0/1`. `1` for base colors (red, blue, yellow). |

**Indexes & Constraints**
- `UNIQUE(name)`, `UNIQUE(hex)`
- `CHECK(is_base IN (0,1))`
- (Optional) `CHECK(hex GLOB '#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]')`

---

## Table: `sessions`
**Purpose:** Identifies a child’s play session so unlocked colors persist across runs.

| Column | Type | Null | Default | Allowed / Notes |
|---|---|---:|---|---|
| `session_id` | TEXT | NO | — | **PK**; use UUIDv4 string. |
| `created_at` | DATETIME | NO | `CURRENT_TIMESTAMP` | Creation time. |
| `last_active_at` | DATETIME | NO | `CURRENT_TIMESTAMP` | Update per interaction (optional). |

**Indexes & Constraints**
- `PRIMARY KEY (session_id)`

---

## Table: `unlocked_colors`
**Purpose:** Join table for colors a session has unlocked (cap at 20 per session).

| Column | Type | Null | Default | Allowed / Notes |
|---|---|---:|---|---|
| `session_id` | TEXT | NO | — | **FK → sessions(session_id)** |
| `color_id` | INTEGER | NO | — | **FK → colors(color_id)** |
| `unlocked_at` | DATETIME | YES | `CURRENT_TIMESTAMP` | Timestamp of unlock. |

**Indexes & Constraints**
- **PK:** `(session_id, color_id)` (prevents duplicates per session)
- **Index:** `idx_unlocked_session (session_id)`
- **FKs:** `ON DELETE CASCADE` (recommended)

**Business Rule**
- **Cap 20 colors per session** (application-enforced).  
  Optional SQLite trigger:

```sql
CREATE TRIGGER IF NOT EXISTS trg_cap_unlocked_colors
BEFORE INSERT ON unlocked_colors
WHEN (
  (SELECT COUNT(*) FROM unlocked_colors WHERE session_id = NEW.session_id) >= 20
)
BEGIN
  SELECT RAISE(ABORT, 'Palette cap reached (20).');
END;
