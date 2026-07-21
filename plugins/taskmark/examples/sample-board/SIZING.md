# T-shirt sizing and story points

Seed estimates are **billable-session** minutes (AI-assisted), not human calendar days. Points stay Fibonacci.

| Size | Points | Meaning | Seed estimate |
|------|--------|---------|---------------|
| XS | 1 | Trivial (billable session) | 30 min |
| S | 2 | Small (billable session) | 2 h (120 min) |
| M | 3 | Medium (billable session) | 1 day (480 min) |
| L | 5 | Large (billable session) | 2 days (960 min) |
| XL | 8 | Extra large (prefer split) | 3+ days (1440 min) |

Weights for size rollups: XS=1, S=2, M=3, L=4, XL=5.

Effort uses **billable work-log minutes** only (idle auto-cap: next-day 12:00 UTC; session cap default 480). Never use calendar span. Recompute via `scripts/recompute-actuals.py`; calibrate seeds from median actuals (≥3 samples per size).

## Calibration log

| Date | Item | Sized | Points | Est | Actual | Note |
|------|------|-------|--------|-----|--------|------|
| 2026-07-20 | T-001 | M | 3 | 480 | 285 | Under estimate; fit M |
