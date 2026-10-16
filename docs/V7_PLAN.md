# FLARE v7: regime and confirmation toggles

**Files:**
- working/FLARE_v7_strategy.pine, built from v6. v6 is unchanged.
- Diff: working/CHANGES_v7_vs_v6.diff.

**Status:** source checks only; not compiled.

**Static checks:**
- `static_check.py`: parentheses and brackets balance, indentation is clean, 4 of 64 plots.
- `request.security` calls: 3. The new CHOP request uses `[1]` with lookahead_on (the non-repainting pattern).
- No negative offsets.
- `static_check2.py`: shorttitle 'FLARE v7' is 8 characters, no use-before-declare.

Prop rules are ignored (v5 prop mode stays OFF).

## Definitions
**(a) Breakeven gate** (default ON)
- The v6 rule moves the stop to entry + 1 tick after a closed bar reaches +1R.
- With the gate on, that rule runs only when the chart timeframe is at least the input (default 15). On 3m and 5m the exits are therefore v4 exits.

**(b) Choppiness filter** (default OFF)
- CHOP(n) = 100 · log10(Σ ATR(1) over n / (highest high − lowest low over n)) / log10(n).
- Defaults: n = 14, measured on the 15m timeframe. If the chosen timeframe is below the chart timeframe, the chart timeframe is used.
- The value comes from the last closed bar: `request.security(..., f(n)[1], lookahead_on)`.
- Entries are blocked when CHOP < 40 (a trending regime).

**(c) Structure-break confirmation** (default OFF; requires v1 sweep mode)
- At EARLY L, the level is frozen as max(warning high, most recent confirmed pivot high).
- Pivot length is 3. A pivot counts only after its 3 right-hand bars have closed, and it is published after setup processing.
- A later closed candle must close above that level within 12 bars, otherwise the setup is EXPIRED.
- Invalidation (trading beyond the frozen sweep extreme) is still checked first, and the stop stays at the sweep extreme.
- Shorts mirror this with min(warning low, last confirmed pivot low).

**(d) VWAP stretch** (default OFF)
- Session VWAP: `ta.vwap(hlc3, session.isfirstbar, 1)`. σ = upper band − VWAP, the volume-weighted standard deviation.
- At the warning close, a long fade needs (VWAP − close)/σ ≥ k; a short needs (close − VWAP)/σ ≥ k. Default k = 1.0.
- The value is frozen at the warning and checked at entry.
- For ES, the session starts at the CME open (about 15:00 PT).

**(e) ATR stop** (default OFF)
- Stop = frozen sweep extreme ∓ 0.25 × ATR(14), replacing the 2-tick buffer.
- The trade is skipped if |reference − stop| > 1.5 × ATR(14). ATR is taken at the signal bar.

**(f) Time window**
- This is the existing v5 "(e) Session window (PT)" input (`time(..., "America/Los_Angeles")`, default 06:30–13:00, OFF).
- It allows one window per run; to exclude 00:00–03:00, run the window as 03:00–00:00.

Every filter applies on the confirmed L/S bar and is counted in "Skipped".

## Time-of-day evidence (v4 and v6, PT, from v6_analysis/tod_out.txt)
- Every bucket has fewer than 30 trades per half, so none qualifies under the consistency rule.
- **00:00–03:00 PT** is net negative in all 10 version × timeframe cells. By half (10 half-cells per version), v4 is PF < 1 in 7 and v6 in 8. This is the most consistent weak window.
- **06:30–11:00 PT (RTH open and mid)** loses on 3m and 5m in both versions. Mostly PF 0.11–0.86 by half, with one cell (v4 3m RTH open, 1st half) at 1.64.
- **08:00–11:00 PT** is positive on 30m in both halves (PF 1.11–2.93).
- **18:00–00:00 PT (Asia)** is the largest bucket. It is positive on 3m and 5m in the 1st half but weakens in the 2nd half.
- **Conclusion:** keep the time window as a test toggle only. Don't hard-code a window from these small samples.

## Test sequence
Same settings throughout: ES1!, 1 contract, $2.50/side, 1 tick slippage, $50K, the same date ranges, v4MinRR = 1.0, all v5 filters OFF.
- Split each timeframe's range at a midpoint fixed in advance; report both halves.
- **Accept a toggle only if:**
  - PF improves in both halves;
  - at least 30 trades remain per half;
  - the trades it removes are net losers in both halves.
- **Runs, one toggle at a time:**
  0. v7 defaults, (a) only. Expect 3m/5m ≈ v4 and 15m–2h ≈ v6. This checks the gate.
  1. +(c) structure-break confirmation (largest expected effect per the community research).
  2. (a) + (b) CHOP < 40 block.
  3. (a) + (d) VWAP stretch k = 1.0.
  4. (a) + (e) ATR stop.
  5. (a) + (f) window 03:00–00:00 PT (excludes 00:00–03:00).
- **Each run is (a) plus one toggle**, never stacked until each one has been judged alone.
- **Then stack the accepted toggles** in the order they passed.
- **Parameters stay at their defaults**; don't tune on these dates.
