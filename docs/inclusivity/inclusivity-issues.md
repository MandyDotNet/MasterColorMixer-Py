# Prioritized Inclusivity Issue List — MasterColorMixer

| Priority | Issue | Finding ID | Heuristic | Target Sprint | REQ-IDs | Acceptance Criteria |
|-----------|--------|-------------|------------|----------------|---------|---------------------|
| **P1** | Enforce 44×44 px minimum tap targets | A1 | Motor accessibility; generous targets | Sprint 2 | REQ-1, REQ-2, REQ-10 | All bubbles ≥ 44×44 px, ≥ 8 px spacing; tap works with touch + mouse. |
| **P2** | Adjustable circle size + horizontal scroll | A2 | Flexible layouts; motor accessibility | Sprint 2 | REQ-1, REQ-3, REQ-10 | Size control (Small/Default/Large); overflow scrolls sideways; bowl remains visible. |
| **P3** | Add voice options (Female EN, Male EN, Spanish ES) | A3 | Language inclusivity; personalization | Sprint 2 | REQ-2, REQ-5, REQ-10 | Selectable voices + “Test Voice”; selection persists; safe fallback. |
| **P4** | Disable “Mix” until two colors present + inline hint. Disable "Clear" until at least one color is present. | A4 | Error prevention; clear status | Sprint 2 | REQ-3, REQ-4, REQ-10 | Mix button disabled until 2 colors; hint is a flashing highlight around the palette area. |
| **P5** | Result badge | A5 | Forgiving interactions; clear feedback | Sprint 2 | REQ-5, REQ-7, REQ-8, REQ-10 | Badge “You made &lt;COLOR&gt;!” spoken; Clear empties bowl. |
