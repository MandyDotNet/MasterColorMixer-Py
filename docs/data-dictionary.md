# Data Dictionary — MasterColorMixer

This dictionary lists table purposes, columns, types, nullability, defaults, allowed values, indexes, and constraints for the project’s SQLite datastore.

---

## Table: `colors`
**Purpose:** Master list of all colors available to the app (base and discovered).

| Column | Type | Null | Default | Allowed / Notes |
|---|---|---:|---|---|
| `color_id` | INTEGER | NO | — | **PK**;`INTEGER PRIMARY KEY` (auto-increment). |
| `name` | TEXT | NO | — | **UNIQUE**; “Red”, “Purple”. |
| `hex` | TEXT | NO | — | **UNIQUE**; 7-char hex `#RRGGBB`. |
| `is_base` | INTEGER | NO | `0` | Boolean as `0/1`. `1` for base colors (red, blue, yellow). |

**Indexes & Constraints**
- `UNIQUE(name)`, `UNIQUE(hex)`

---

## Table: `sessions`
**Purpose:** Identifies a child’s play session so unlocked colors persist across runs.

| Column | Type | Null | Default | Allowed / Notes |
|---|---|---:|---|---|
| `session_id` | TEXT | NO | — | **PK**; use UUIDv4 string. |
| `created_at` | DATETIME | NO | `CURRENT_TIMESTAMP` | Creation time. |
| `last_active_at` | DATETIME | NO | `CURRENT_TIMESTAMP` | Update per interaction. |

**Indexes & Constraints**
- `PRIMARY KEY (session_id)`

---

## Table: `mix_events`
**Purpose:** Records every color mixing action for tracking, analytics, and replay.  
Each record logs which two colors were combined, the resulting color, and which session it belonged to.

| Column | Type | Null | Default | Allowed / Notes |
|---|---|---:|---|---|
| `mix_id` | INTEGER | NO | — | **Primary Key** — unique identifier for each mix event (`INTEGER PRIMARY KEY AUTOINCREMENT`). |
| `session_id` | TEXT | NO | — | **Foreign Key → sessions(session_id)**; identifies which play session this mix occurred in. |
| `color1_id` | INTEGER | NO | — | **Foreign Key → colors(color_id)**; ID of the first color mixed. |
| `color2_id` | INTEGER | NO | — | **Foreign**_

**Indexes & Constraints**
- **Index:** `idx_mix_session (session_id, occurred_at DESC)` for efficient lookups by session.
- **Foreign Keys:** All FKs reference parent tables using `ON DELETE CASCADE`.
- **Check Constraint:** `CHECK (color1_id <> color2_id)` prevents mixing a color with itself.

**Business Rule** 
- Each mix action records source colors, result, and session for reproducibility.

---

## Table: `unlocked_colors`
**Purpose:** Join table for colors a session has unlocked (capped at 20 per session).

| Column | Type | Null | Default | Allowed / Notes |
|---|---|---:|---|---|
| `session_id` | TEXT | NO | — | **FK → sessions(session_id)** |
| `color_id` | INTEGER | NO | — | **FK → colors(color_id)** |
| `unlocked_at` | DATETIME | YES | `CURRENT_TIMESTAMP` | Timestamp of unlock. |

**Indexes & Constraints**
- **PK:** `(session_id, color_id)` (prevents duplicates per session)
- **Index:** `idx_unlocked_session (session_id)`
- **FKs:** `ON DELETE CASCADE` (prevent manual cleanup)

**Business Rule**
- **Cap 20 colors per session** (application-enforced).
- Timestamps on unlocked colors helps guide adjsutments to the app like hints, or analytics on how the toddler progressed.
- If the app crashes or acts unexpectedly, timestamps help reproduce the issue.
- SQLite trigger: trg_cap_unlocked_colors

