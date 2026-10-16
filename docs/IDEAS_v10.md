# FLARE "outside the box" idea tests (offline approximation)

**Data:** Yahoo `ES=F` and `NQ=F` 5m, 2026-08-05 → 2026-10-15 PT (about 13.6k bars each, continuous front month).

**Code:** offline_v9/sim2.py (engine) and ideas.py (tests). Output: offline_v9/ideas_out.txt.

**Model:** an APPROXIMATION of FLARE, not TradingView.
- **Levels:** DO, PDH/PDL/PDM, WO, PWH/PWL/PWM, MO, PMH/PML/PMM (weights 2 / 4 / 5).
- **Trigger:** sweep and reclaim (bar trades through the level, closes back on its prior side).
- **Confirmation:** a structure-break close beyond max(warning extreme, last confirmed pivot) within 12 bars. Pivots are 3/3 and used only after their confirmation bars.
- **Fills:** entry at the next bar's open; stop at the sweep extreme ± 2 ticks.
- **Exits:** 2 contracts. Scalp leg at half-way to the next level; runner at the next level; the runner moves to breakeven + 1 tick after the scalp fills (effective next bar). Stop first if both are hit in one bar.
- **Costs:** $2.50/side per contract, plus 1 tick slippage on the entry and on stop exits.
- **Split:** halves by bar index (about 2026-09-11).
- **Rule to "survive":** at least 30 trades in each half and PF > 1 in each half.

**Settings verified against sim2.py (2026-10-15):**
- Confirm window N=12 bars; invalidation if price trades beyond the sweep extreme.
- Pivots 3/3; a pivot is usable only from its confirmation bar, and only pivots confirmed by the sweep bar are used.
- SMT window: the other market's same bar plus the prior 3 bars (4 bars).
- Confluence radius: 3 pts on both ES and NQ (`3*T*4`).
- Stop buffer 2 ticks; breakeven = entry + 1 tick, applied from the bar after the scalp fills.
- Slippage: 1 tick at entry plus 1 tick on stop exits; limit exits get none.
- Correction: the memory outcome has a third state, 'fail'. A touch that closes back against a break seen within the previous 6 bars counts as 'fail', so 'last=BRK' excludes those touches. The Pine tracker has no 'fail' state.

## Baseline
| | n | TP1 hit | PF all | PF 1st / 2nd |
|---|---|---|---|---|
| ES | 186 | 50% | 0.88 | 0.69 / 1.10 |
| NQ | 194 | 57% | 0.72 | 0.68 / 0.77 |

## Results by idea
Subgroups are taken from the baseline run; "re-run" means the filter was applied in the simulation, which changes later trades.

**1. SMT (ES vs NQ at the same-named level, other market within the last 4 bars)**
| Group | ES PF 1st / 2nd (n) | NQ PF 1st / 2nd (n) |
|---|---|---|
| Divergence (other market did NOT sweep) | 0.55 (41) / 0.96 (34) | 0.72 (34) / 0.48 (41) |
| Both swept | 0.80 (48) / 1.17 (63) | 0.66 (60) / 1.06 (59) |
| Divergence re-run | 0.57 / 0.98 | 0.92 / 0.44 |

**Rejected:** divergence was worse than both-swept in 3 of 4 halves.

**2. Re-test timing (6–24 bars after a HOLD) and first touch of the period:** only 2–7 trades each. **Untestable at this sample size.**

**3. Overshoot stop** (stop = level ± p80 penetration from 1st-half sweeps; skip if the sweep went beyond it)
- **ES penetration:** median 0.62–0.75 pts, p80 0.62–2.00 pts, by family.
- **NQ penetration:** median 4.25–9.25 pts, p80 10.25–12.00 pts.
- **Results:**
  - ES PF falls from 0.69 / 1.10 to 0.55 / 0.89.
  - NQ PF falls from 0.68 / 0.77 to 0.65 / 0.70.
  - TP1 hit rate drops slightly.
- **Rejected:** the sweep-extreme stop is better.

**4. Time of session (PT)**
| Window | ES PF 1st / 2nd (n) | NQ PF 1st / 2nd (n) |
|---|---|---|
| 06:30–08:00 (first 90 min) | 0.57 (15) / 0.30 (10) | 0.54 (11) / 4.40 (10) |
| 08:00–13:00 | 0.74 (19) / 1.23 (25) | 0.56 (20) / 0.55 (17) |
| Overnight | 0.75 (55) / 1.35 (62) | 0.78 (63) / 0.69 (73) |

**Rejected:** no consistent window. The opening 90 minutes are small and inconsistent.

**5a. Confluence** (another level within 3 pts): ES 0.59 / 0.63 (14 / 22); NQ has almost none. **Rejected:** confluence is worse, not better.

**5b. Prior-day range vs the 10-day average**
| Group | ES PF 1st / 2nd | NQ PF 1st / 2nd |
|---|---|---|
| Range < average | 0.56 / 1.38 | 0.64 / 1.31 |
| Range ≥ average | 0.82 / 0.87 | 0.74 / 0.37 |

**Inconsistent:** neither group is above 1 in both halves.

**5c. Level family:** daily ES 0.76 / 1.17 and NQ 0.68 / 1.13; weekly and monthly are small and mixed. **Rejected.**

**5d. Level memory, last touch at the level**
| Group | ES PF 1st / 2nd (n) | NQ PF 1st / 2nd (n) |
|---|---|---|
| Last = HOLD | 1.75 (33) / 2.60 (28) | 1.19 (32) / 1.10 (32), passes the rule |
| Last = BREAK | 0.29 (49) / 0.52 (57) | 0.56 (57) / 0.36 (53) |
| Re-run, last = HOLD | 0.91 / 1.11 | 1.04 / 0.71 |
| Re-run, last ≠ BREAK | 0.81 / 1.28 | 0.78 / 1.01 |

- **"Last touch was a BREAK → loser" is the most robust finding:** PF 0.29–0.56 in all 4 market-halves, each with 49 or more trades.
- **As a positive filter it weakens** in re-runs, because removing trades shifts which later setups get taken.

**6. Candle patterns (sweep candle "sw", confirm candle "cf")**
| Pattern | ES PF 1st / 2nd (n) | NQ PF 1st / 2nd (n) |
|---|---|---|
| sw engulfing | 2.07 (10) / 4.81 (11) | 0.97 (8) / 0.89 (6) |
| sw close in the top/bottom 25% of its range | 1.28 (41) / 0.99 (49) | 0.87 / 0.53 |
| sw body ≥ 0.5 ATR | 0.75 / 2.04 | 0.88 / 0.80 |
| sw wick ≥ 50% / 60% | 0.88 / 0.67, 0.90 / 0.54 | 0.49 / 0.75, 0.33 / 1.26 |
| sw small body / inside bar | < 1 mostly | < 1 mostly |
| cf engulfing | 0.46 / 0.81 | 0.98 / 0.92 |
| cf wick ≥ 50% | 0.00 (5) / 1.51 (5) | 2.58 (5) / 1.33 (8) |
| 3+ same-color candles into the level (exhaustion) | 2.76 (3) / 1.35 (6) | 0.28 (4) / ∞ (5) |

- **Long rejection wicks on the sweep candle did NOT help** (mostly PF < 1).
- **The sweep-engulfing result on ES is striking but tiny** (n = 10 per half) and does not replicate on NQ.

**Stacks** (structure-break + memory + the best other ideas, re-runs)
| Stack | ES PF 1st / 2nd (n) | NQ PF 1st / 2nd (n) |
|---|---|---|
| HOLD + confirm close in the top 25% | 1.05 (35) / 1.02 (37), passes the rule but only barely above 1 | 0.81 / 0.82 |
| HOLD + SMT divergence | 0.57 / 1.49 | 1.65 / 0.43 |
| HOLD + sweep wick ≥ 50% | 1.32 / 0.59 | 1.03 / 0.37 |

## Ranked list
1. **Skip setups whose level's last touch was a BREAK.** It is consistent on ES and NQ in both halves with large n. The effect size is large as a subgroup but shrinks in re-runs.
2. **Last touch = HOLD,** a positive version of #1. It passes the rule on NQ as a subgroup and nearly passes on ES (28 trades in the 2nd half); re-runs are mixed.
3. **HOLD + confirm-candle close in its top/bottom 25%:** the only stack that passed the rule (ES only), at PF 1.02–1.05. Fragile.
4. **Sweep-candle engulfing:** large effect on ES, n ≈ 10 per half, no NQ support. Watch only.
5. **Everything else is rejected:** SMT divergence, re-test timing (no sample), p80 overshoot stop, time-of-session, confluence, prior-day range, level family, wick ratios, inside bars, body size, exhaustion.

**Nothing clearly survives at a level worth trading.** The memory signal is real-looking but becomes marginal once applied as a filter.

## Proposed Pine v10 changes (small, testable; not compiled)
1. **Memory filter option** "Skip if last touch was a BREAK (BRK/FAIL ok)", in addition to v9's "Last touch was HOLD/REJ". It uses the same previous-bar snapshot as v9 (no lookahead).
2. **Optional confirm-candle close-location filter:** close in the top 25% of the bar's range for longs (bottom 25% for shorts). Default OFF.
3. **Optional sweep-candle engulfing flag,** shown in the tooltip and entry comment for attribution only. Default OFF as a filter.
4. **Logging in entry comments:** confirm close location, sweep wick ratio and engulfing flag, so TradingView trade lists can verify these on the real FLARE map across 3m/5m/15m and longer history.

**TradingView runs needed** (ES1! 3m and 5m, then NQ1!; both halves):
- v9 + memory "not BREAK".
- v9 + memory "HOLD/REJ".
- Each of the two runs above, plus the close-location filter.

**Accept a change only if** it reaches 30 or more trades per half with PF > 1 in both halves, on both ES and NQ.

**Caveats:**
- 60 days of Yahoo data and simplified levels.
- Halves are about 1 month each.
- Many subgroups were tested, so some will look good by chance. Results from the multiple-comparison search need replication in TradingView on longer data before any real money.
