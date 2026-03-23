# Vault Structure Standard

This document defines the canonical folder layout for the Disney-Universal KB vault. Follow this pattern when adding new parks, attractions, or dining content.

---

## Standard park shape

```
[Brand]/Parks/[Park Name].md             ← park overview (strategy, layout, LL posture, closures)
[Brand]/Parks/[Park Name]/
  Attractions/
    Ranked.md                            ← ranked tier list with LL tier, height req, priority
    [Attraction Name].md                 ← one file per attraction (use Windows-safe names)
  Dining/
    Overview.md                          ← dining summary table; scored venues, quick vs. table
    [Restaurant Name].md                 ← optional: per-restaurant deep-dive (add when justified)
  Seasonal/                              ← only create if a seasonal overlay applies
    [Event Name].md
```

**Rules:**
- Park overview file lives at `Parks/[Park Name].md` (not inside the subfolder).
- `Attractions/Ranked.md` is the aggregated tier list; individual files go alongside it.
- `Dining/Overview.md` is the entry point; split into per-restaurant files only when meaningful detail exists.
- `Seasonal/` is optional — currently only EPCOT has one (Flower & Garden Festival 2026).
- Filenames must be Windows-safe: no `?`, `:`, `*`, `"`, `<`, `>`, `|`, `\` — use hyphens or spaces only.

---

## Brand-level layout

```
Disney/
  Overview.md
  Parks/          ← Magic Kingdom, EPCOT, Hollywood Studios, Animal Kingdom
  Resorts/        ← Disney's Pop Century Resort.md
  Strategy/       ← Lightning Lane, Early Theme Park Entry, April 2026 Context, Dining Reservations

Universal/
  Overview.md
  Parks/          ← Universal Studios Florida, Islands of Adventure, Epic Universe
  Resorts/        ← Universal's Endless Summer Resort - Surfside Inn and Suites.md
  Strategy/       ← Early Park Admission, Express Pass
```

---

## What still needs to be filled in

| Item | Status | Next step |
|---|---|---|
| Per-restaurant files under `Dining/` | Not yet created for any park | Add when dining research goes deep enough to justify individual notes |
| Universal Strategy: Epic Universe-specific strategy | Missing | Add `Universal/Strategy/Epic Universe Strategy.md` once more is known closer to trip |
| Disney dining reservations per restaurant | Tracked in `Disney/Strategy/Dining Reservations.md` | Consider expanding with per-restaurant booking windows and ADR priority scores |
| Animal Kingdom day plan | Lighter coverage than other parks | Review `Disney/Parks/Disney's Animal Kingdom/Attractions/Ranked.md` and add strategy notes if needed |
| Crowd calendar / park-day assignment | Tracked in `docs/Trip-Brief.md` and Google Sheet `Disney2026` | Once confirmed, add brief note to each park overview's "Best use case on this trip" section |

---

## Changelog

| Date | Change |
|---|---|
| 21 Mar 2026 | Initial structure created with flat `Dining.md` and `Attractions - Ranked.md` per park |
| 21 Mar 2026 | Refactored: `Dining.md` → `Dining/Overview.md`, `Attractions - Ranked.md` → `Attractions/Ranked.md`, EPCOT festival file → `Seasonal/` |
