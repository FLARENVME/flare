# FLARE v9: level memory, trendline trigger, scalp + runner

**Files:**
- working/FLARE_v9_strategy.pine, built from v8. v8 is untouched.
- Diff: working/CHANGES_v9_vs_v8.diff.

**Status:** source checks only; not compiled.

**Static checks:**
- `static_check.py`: parentheses and brackets balance, indentation is clean, 4 of 64 plots, 5 `request.security` calls (no new ones), no negative offsets.
- `static_check2.py`: shorttitle 'FLARE v9' is 8 characters, no use-before-declare.

**Defaults:** v9 defaults equal v8 defaults (v7 A + structure-break below 120m). All new features default OFF.

## What is offline estimate vs what needs TradingView
**Offline (offline_v9/sim.py, outputs in sim_out.txt, analysis_out.txt and memfilter_out.txt):**
- An APPROXIMATION of the sweep/reclaim logic in Python, not FLARE itself.
- **Data:** Yahoo `ES=F` 5m bars, 2026-08-05 → 2026-10-15 PT (13,638 bars, continuous front month, about 60 days, one timeframe).
- **Levels:** DO, PDH/PDL/PDM, WO, PWH/PWL/PWM, MO, PMH/PML/PMM. No Monday/quarterly/yearly levels and no v3 box filters.
- **Trades:** entry at the next bar's open; stop at the sweep extreme ± 2 ticks; when stop and target are both hit in one bar, the stop counts first.
- **Costs:** $2.50/side per contract, plus 1 tick slippage on the entry and on stop exits.
- **Not modeled:** the R:R filter, CHOP and the other v5/v8 filters.
- Treat it as directional evidence only.

**Needs TradingView:** everything in the Pine file (compile, the real FLARE map, all five timeframes, longer history).

## Offline results (ES 5m, 2 contracts, halves split by trade count)
**Breakeven TP1 hit rate** (scalp leg alone). Median stop: 5.75 pts with the v1 trigger, 7.5 pts with structure-break.

| TP1 size | Breakeven hit rate (v1 / structure-break) |
|---|---|
| 0.3R | 82% / 81% |
| 0.5R | 72% / 70% |
| 0.75R | 62% / 61% |
| 1.0R | 54% / 53% |

**Exit models** (TP1 hit rate = win rate of the scalp leg; PF is net of all legs):

| Trigger | Exit | n | TP1 hit | PF all | PF 1st / 2nd |
|---|---|---|---|---|---|
| v1 (warning extreme) | 0.3R + runner (BE) | 345 | 70% | 0.73 | 0.59 / 0.90 |
| v1 | 0.5R + runner | 310 | 60% | 0.70 | 0.54 / 0.86 |
| structure-break | 0.3R + runner | 206 | 67% | 0.72 | 0.61 / 0.86 |
| structure-break | 0.5R + runner | 190 | 59% | 0.70 | 0.66 / 0.75 |
| structure-break | half-way to next level + runner | 186 | 50% | 0.88 | 0.69 / 1.12 |
| structure-break | single target at next level only | 193 | 50% | 0.77 | 0.62 / 0.96 |
| trendline break | 0.3R + runner | 162 | 60% | 0.67 | 0.58 / 0.74 |
| trendline break | 0.5R + runner | 153 | 57% | 0.57 | 0.63 / 0.54 |

- An **80% win rate is not reached** with any tested TP1. Even at 0.3R the hit rate is 67–72%, below the 81–82% needed to break even after costs.
- A **0.3R scalp is about 2 pts** on a 6–8 pt stop, so the round-trip cost (about $17.50 per contract) eats most of each win.
- **Trendline break** was weaker than structure-break offline.

**Level memory** (structure-break, 0.5R + runner), subgroups of one run:

| Group | n | PF | PF 1st / 2nd (n) |
|---|---|---|---|
| Last touch = HOLD | 63 | 1.53 | 1.16 (36) / 2.23 (27) |
| Last touch = BREAK | 105 | 0.35 | 0.44 (52) / 0.30 (53) |

- These two groups are the **only memory feature that is consistent across halves.** "1st vs 3rd touch" can't be judged (only 8 first touches).
- **Applied as an actual filter** (a re-run that also changes the trade path), structure-break + last=HOLD + 0.5R + runner gives n = 104, PF 1.00: 0.81 in the 1st half, 1.22 in the 2nd.
- The "last touch ≠ BREAK" version gives PF 0.70 / 1.39.
- **Conclusion:** promising but not proven. In the 2nd half every hold group has fewer than 30 trades.

## Pine v9 additions (all OFF by default)
**1. Level memory filter.** Options: Off / "Last touch was HOLD/REJ (not a break)" / "Prior holds > breaks".
- It reads the boundary's held/broken counts and last outcome from the existing per-level tracker, using the snapshot taken at the end of the previous bar. The sweep candle's own touch is therefore excluded and there is no lookahead.
- Counts reset when the level's price changes (a new period).
- For merged boundaries, the strongest member's slot is used.
- The memory is always shown in the setup tooltip (EARLY/L/S markers, status) and in entry comments as "mem H# B# last …".

**2. Trendline-break confirmation.**
- At EARLY L: if the last two confirmed pivot highs (v7 pivot length) are descending, the line through them is frozen.
- Confirmation is a closed candle closing above the line's value at that bar. If there is no valid line, the warning-candle extreme is used.
- Shorts mirror this with ascending pivot lows.
- It overrides structure-break when ON. Invalidation is still processed first.

**3. Scalp + runner.** Options: Off / "Fixed R" (default 0.5R) / "Half-way to next boundary (v3 TP1)".
- When ON, size is raised to at least `v9Qty` (default 2).
- Half the contracts exit at the scalp level ("scalp").
- The rest go to the runner target (default TP2, the next boundary).
- After a closed bar reaches the scalp level, the runner's stop moves to entry + 1 tick.

## TradingView runs needed (ES1!, $2.50/side, 1 tick, same dates, report both halves)
1. v9 defaults: confirm it matches v8.
2. Scalp half-way-to-next-boundary + runner TP2 on 3m and 5m (the best offline variant), 2 contracts.
3. Scalp Fixed 0.5R + runner, then 0.3R, to confirm the offline finding that small targets lose after costs.
4. Memory filter "Last touch was HOLD/REJ", alone, on top of the run-1 defaults.
5. Memory filter + the best scalp setting.
6. Trendline trigger vs structure-break (same exits).

Accept a change only if PF improves in both halves with at least 30 trades per half. Report both the TP1 hit rate and net PF.

## Honest framing for Erick
- A high win rate is achievable mechanically with a tiny TP1, but on ES with these structural stops it requires about 80% hits, and nothing tested gets there after costs.
- The more promising path offline is selectivity at the level (memory: last touch held) plus a mid-sized first target (half-way to the next boundary) with a runner. That is what v9 lets you test in TradingView.
