# FLARE v8: trend veto, exit and entry toggles

**Files:**
- working/FLARE_v8_strategy.pine, built from v7. v7 is untouched.
- Diff: working/CHANGES_v8_vs_v7.diff.

**Defaults:** all v8 toggles are OFF, so v8 trades exactly like v7's defaults (v7 (a) ON, everything else OFF).

**Status:** source checks only; not compiled, not backtested.

**Ideas** come from GITHUB_RESEARCH.md (triple-barrier time limit, profit-tiered exits, regime gating, protections). The logic is written from scratch; no GPL code was used.

**Fixed:** the v6 entry comment was truncated to "L | " because a `//` comment ended up in the middle of the expression. v6 and v7 trade lists therefore lack the boundary and R:R fields. v8 restores them (comment text only, no trading effect).

**Static checks:**
- `static_check.py`: parentheses and brackets balance, indentation is clean, 4 of 64 plots.
- `request.security`: 5 calls. The new ones are D ADR and 1h EMA slope, both with `[1]` and lookahead_on.
- No negative offsets.
- `static_check2.py`: shorttitle 'FLARE v8' is 8 characters, no use-before-declare.

## Definitions
All checks are made on confirmed bars. R = |frozen reference − frozen stop|, where the reference is the signal close, the retest level, or the retrace price.

**(1) Trend-day regime veto.** Each sub-condition has its own toggle.
- **(1a) Range:** the CME trading day's high − low so far > X × ADR20 (default X = 1.0) blocks both sides.
  - ADR20 = SMA(high − low, 20) of completed daily bars: `request.security("D", sma[1], lookahead_on)`.
- **(1b) VWAP side:** at least N consecutive closes (default 24) below session VWAP (v7's `ta.vwap`) veto longs. N closes above veto shorts.
- **(1c) 1h EMA slope:** EMA50[1] − EMA50[4] on closed 1h bars, with `[1]` + lookahead_on. On charts above 1h, the chart timeframe is used.
  - Long vetoed if the slope is < 0; short vetoed if > 0.

**(2) Time stop.** If the trade's best favorable excursion, measured on closed bars from the frozen reference, is still below 0.5R after N bars (default 12), close at market ("time stop"). The bar count starts at the first closed bar in position.

**(3) Partial at 1R.**
- When ON, the position size is raised to at least `v8PartQty` (default 2); compare results per contract.
- Half (floor) exits with a limit at reference ± 1R ("1R").
- The rest goes to the selected single target (TP1 by default).
- After a closed bar has reached +1R, the remaining stop moves to reference ± 1 tick.

**(4) Trail.** Options: Off / ATR / Last confirmed swing.
- It arms after a closed bar reaches +1R.
- ATR: candidate = close ∓ 1.5 × ATR(14). Swing: the last confirmed pivot low/high, using v7's pivot length and published only after its confirmation bars.
- The stop only ratchets tighter, never looser. The exit comment is "trail".

**(5) Entry retrace50.**
- A limit order at (high + low)/2 of the confirmed L/S candle. R:R and targets are measured from that price.
- The order is canceled after M bars (default 4), or earlier if the frozen stop trades first.
- **Unfilled setups** get a shadow market entry at the next bar's open, scored as TP1 vs stop with the stop counted first when both are hit in the same bar.
- The table shows the unfilled count and the shadow wins / losses / still open.

**(6) Daily side guard.**
- After K losing trades (default 2) closed with a "stop" comment on one side within a CME trading day, new entries on that side are blocked until the next trading day.
- Partial legs from the same entry count once. Blocks are counted in the table.

## Test order
Same settings throughout: ES1!, $2.50/side, 1 tick slippage, the same dates, v4MinRR 1.0, v7 (a) ON.
- Each run is the v7-defaults baseline plus exactly one toggle.
- Report both halves, split at a fixed date chosen in advance.
- **Accept a toggle only if:**
  - PF improves in both halves;
  - at least 30 trades remain per half;
  - the removed trades (filters) or changed exits are net-negative in both halves.
- **Runs:**
  0. Baseline: confirm it matches v7.
  1. (1a) range veto.
  2. (1b) VWAP-side veto.
  3. (1c) 1h EMA slope veto.
  4. (6) side guard.
  5. (2) time stop.
  6. (4) trail ATR, then (4) trail swing as a separate run.
  7. (3) partial at 1R: 2 contracts; compare P/L per contract and drawdown against 1-contract runs.
  8. (5) retrace50: compare trades taken vs the unfilled shadow outcomes. If the shadows are mostly winners, the retrace is costing winners.
- **Then:** stack the accepted toggles one at a time, keeping parameters at their defaults (no tuning on these dates).
