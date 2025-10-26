# Crow’s-Foot ERD — MasterColorMixer

> This ERD shows the logical data model for persistence in SQLite. It includes tables, primary keys, foreign keys, cardinalities, and key constraints used by the app.


### Entities & Relationships (Summary)
- **colors** *(1)* —< *(N)* **unlocked_colors**  
  Each unlocked color references exactly one row in `colors`.
- **sessions** *(1)* —< *(N)* **unlocked_colors**  
  A session can unlock many colors (capped at 20 by app logic).
- **sessions** *(1)* —< *(N)* **mix_events**  
  Each mix event belongs to one session.
- **colors** *(1)* —< *(N)* **mix_events** (via `color1_id`, `color2_id`, `result_color_id`)  
  Mixes reference two source colors and one resulting color.

### Notes on Constraints
- **Uniqueness:** `colors.name` and `colors.hex` are unique (prevents duplicates).
- **Composite PK:** `unlocked_colors (session_id, color_id)` prevents unlocking the same color twice per session.
- **Referential Integrity:** All FKs use `ON DELETE CASCADE` (recommended) so deleting a session removes related unlocks and events.
- **Application Rule:** Max **20 unlocked colors per session** is enforced in the service layer (SQLite can also use a trigger; see Data Dictionary for an optional example).

erDiagram
    SESSIONS ||--o{ UNLOCKED_COLORS : "has"
    COLORS   ||--o{ UNLOCKED_COLORS : "is"
    SESSIONS ||--o{ MIX_EVENTS      : "records"
    COLORS   ||--o{ MIX_EVENTS      : "inputs/result"

    SESSIONS {
      TEXT session_id PK
      DATETIME created_at
      DATETIME last_active_at
    }

    COLORS {
      INTEGER color_id PK
      TEXT name UK
      TEXT hex UK
      INTEGER is_base
    }

    UNLOCKED_COLORS {
      TEXT session_id PK,FK
      INTEGER color_id PK,FK
      DATETIME unlocked_at
    }

    MIX_EVENTS {
      INTEGER mix_id PK
      TEXT session_id FK
      INTEGER color1_id FK
      INTEGER color2_id FK
      INTEGER result_color_id FK
      DATETIME occurred_at
    }
