# Inclusivity Heuristic Review — MasterColorMixer

## Overview
Two end-to-end tasks were reviewed using Letaw’s *Inclusivity Heuristics*:

1. **Task A — Tap a base color to hear its name**
2. **Task B — Mix two colors and hear the result**

---

## Findings

| ID | Finding | Heuristic | Affected Screen/Step | REQ-ID | Severity | Proposed Fix |
|----|----------|------------|----------------------|--------|-----------|---------------|
| **A1** | Tap targets may be too small for toddlers on smaller screens. | Motor accessibility; generous targets | Palette → Selecting color | REQ-1, REQ-2, REQ-10 | **High** | Ensure hit area ≥ 44×44 px; add 8–12 px padding around bubbles. |
| **A2** | Caregivers cannot adjust circle size for easier color selection. | Flexible layouts; motor accessibility | Palette (settings) | REQ-1, REQ-3, REQ-10 | **High** | Add Size control (Small • Default • Large). Enable horizontal scrolling if overflow hides bowl. |
| **A3** | Utilizing only one voice may alienate users with language or gender preference differences. | Language inclusivity; personalization | Settings → Voice | REQ-2, REQ-5, REQ-10 | **Medium** | Offer 3 selectable voices (Female EN, Male EN, Spanish ES). Persist selection per session. |
| **A4** | When the palette or mixing area remains unchanged for several seconds, toddlers may not realize what to do next. | Discoverability; user guidance; attention cues | Palette and Mixing Area | REQ-1, REQ-3, REQ-10 | **Medium** | Add a gentle visual cue (ex: palette pulses or brief highlight) and subtle chime if idle for 10–15 seconds. This draws attention to the tappable colors without startling the child. Fade effect resets on any interaction. |
| **A5** | Similar hues could confuse users with color-vision differences. | Perceivable alternatives; clarity | Palette rendering | REQ-1, REQ-10 | **Low** | Add high-contrast outline and optional texture or shape glyphs; provide “Color-blind friendly” enable in pallette settings. |

---

## Annotated Screenshots

Screenshots are included in `docs/inclusivity/screenshots/`:

1. **taskA1_tap_color_annotated.png** — small hit target and padding
2. **taskA2A3A5_settings_size_sound_shapes.png** - proposed options for circle size, voice, and color-blind options
3. **taskA5_mix_colors_color-blind_preview.png** — palette is presented with shapes to help user if color-blind