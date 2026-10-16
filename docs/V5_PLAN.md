# FLARE v5: filter candidates and prop mode (plan)

**Files:**
- working/FLARE_v5_strategy.pine
- working/CHANGES_v5_vs_v4.diff
- static_check_v5.txt

**Relationship to v4:** v4 is unchanged. In v5, every filter and prop mode default to OFF, so v5 with everything off should trade exactly like v4. Entry comments only gain an "RVOL" field when filter (b) is on.

**Status:** source checks only; not compiled, not backtested.

**Static checks:** parentheses and brackets balance, indentation is clean, 4 of 64 plots, the same 2 `request.security` calls, no negative offsets.

## Definitions
All filters are evaluated when the order decision is made, on the closed L/S candle. Values marked "frozen" are captured on the EARLY (warning) candle.

**(a) VWAP side**
- Source: `ta.vwap(hlc3)`, anchored to the chart session. For ES that is the CME session starting about 15:00 PT, not a 06:30 RTH anchor.
- Long only if the L-candle close is above VWAP; short only if the S-candle close is below. A reclaim (crossing back above) is included in "close above".

**(b) Relative volume (RVOL)**
- RVOL = warning-candle volume / SMA(volume, N) of the N prior bars. Defaults: N = 20, minimum 1.5. Frozen at EARLY.
- OHLCV volume is a participation proxy, not order flow (the table and tooltip say so).

**(c) Divergence at the sweep**
- The oscillator is RSI(14) or the MACD(12, 26, 9) histogram.
- Bull: sweep-candle low < last confirmed pivot low, and oscillator now > oscillator at that pivot. Bear: the mirror, using pivot highs.
- Pivots use `ta.pivotlow/high` with the existing left/right bars. Each pivot is published only after its right-hand bars close, and only after setup processing, so no future data is used. Frozen at EARLY.

**(d) Boundary filter (v3 box mode only)**
- The weight of the frozen boundary L must be at least the minimum (default 4, Weekly or stronger).
- "Established only" (on by default inside this filter) also requires that L is not developing and the box is not PROVISIONAL.
- Ignored in the original box mode.

**(e) Session window**
- `time(timeframe.period, "0630-1300", "America/Los_Angeles")` checked on the L/S candle.
- The fill happens at the next bar's open, so it can land up to one bar after 13:00.

**Prop mode (Lucid Flex 50K baseline)**
- Rules taken from Lucid's help center, Oct 2026; verify with the firm before relying on them.
- At each trading-day change, closed-trade EOD balance = 50,000 + net profit as of the previous bar.
- The floor (MLL) = highest EOD balance − $2,000. Once the highest EOD balance exceeds $52,100, the floor locks at $50,100.
- Breach means an EOD balance at or below the floor. The table shows breached/never breached with the date, the current floor (trailing or locked), and the worst EOD room above the floor.
- Intraday dips and open P/L are not counted, because this is the EOD rule only.
- Contracts are capped at 4.
- Optional daily loss stop (default $1,000): realized + open P/L since the trading-day start ≤ −X flattens the position and blocks new entries until the next trading day.

## Test order
- **Baseline:** v5 with all filters off. First confirm it matches v4 exactly (same trade count and net) on the same chart, dates and Properties: ES1!, 1 contract, $2.50/side, 1 tick slippage, $50K, v4MinRR = 1.0.
- **Split:** each timeframe's date range is cut at a fixed midpoint chosen before running. The first half is used for decisions; the second half is held out and reported as-is.
- **Filters, one at a time vs the baseline, never stacked until each is judged alone:**
  1. (d) weight ≥ 4, established only. Structural and closest to the method.
  2. (e) session 06:30–13:00 PT.
  3. (a) VWAP side.
  4. (b) RVOL ≥ 1.5.
  5. (c) divergence, RSI first, then MACD as a separate run.
- **Timeframes:** 3m, 5m and 15m separately (also 30m and 2h if desired).
- **Metrics per run:** trades, PF, net after costs, win %, average win vs average loss, max closed drawdown, longs vs shorts, and how many baseline trades were removed with their combined P/L. The removed trades should be net losers in BOTH halves.
- **Accept a filter only if all of these hold:**
  - first-half PF improves;
  - the second half doesn't get worse;
  - at least 30 trades remain per half.
  Thresholds stay fixed (1.5 RVOL, weight 4, RSI 14); no tuning on these dates.
- **Combining:** only after the individual runs, stack accepted filters one at a time in the same order.
- **Prop mode:** run last on the best single configuration with 1 and then 4 contracts. Record breach yes/no and date, and the worst EOD room.

## Open questions
- Should VWAP be anchored at 06:30 RTH instead of the CME session? That would need a custom anchor.
- RVOL with ES1! roll days and holiday sessions: should those be excluded?
- With the daily loss limit on, Lucid's DLL value differs per account; enter the real number.
- An intraday (realtime) breach check against the floor is not modeled.
