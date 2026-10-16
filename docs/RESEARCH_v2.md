# FLARE v2: sweep/reclaim entries and structural exits (research + code notes)

**Files:**
- working/FLARE_v2_strategy.pine: separate strategy() build. v1 is unchanged (sha256 b3adef40…12bd).
- static_check_v2.txt: static check output.

**Status:**
- v1 compiled in TradingView (as reported by Erick).
- v2 has NOT been compiled or backtested by me.
- All results will come from TradingView's simulated Strategy Tester (its broker emulator), not a broker.

## 1. Public approaches
I read these free public articles and docs. No paid or closed indicator code was copied.

| Idea | Source | Testable in Pine with OHLCV? |
|---|---|---|
| A sweep is a wick through the level with the body closing back inside. A body close beyond the level is a breakout, not a sweep. | [LiquidityScan][1], [ICT Killzone][2] | Yes. This is exactly v1's `f_boxSweepOnly`. |
| MSS (market structure shift): after the sweep, a displacement candle closes through the last counter-swing. | [1], [GoForexHub][3] (adds a body > 1.5×ATR rule) | Yes, using confirmed pivots (`ta.pivothigh/low`, known only after the right-side bars). Not implemented yet; candidate filter for v3. |
| FVG (fair value gap) retest: a 3-candle gap with C1.high < C3.low; enter with a limit at the gap or its 50% midpoint. | [3], [TradingPlan][4], [liquiditysweeptrading][5] | Yes. v2 ships a simpler retest (a limit at the reclaimed box center). An FVG limit is a candidate for v3. |
| Stop beyond the sweep extreme plus a buffer; trading through the extreme kills the setup. | [1], [4], [5] | Yes. This is v2's stop. |
| Target the opposite liquidity / next level; partial at TP1, then move the stop to breakeven. | [1], [2], [4] | Yes. v2 targets the next map levels instead of generic liquidity pools. |
| Fill model: market orders fill at the next bar open. When stop and target are both inside one bar, the emulator assumes the extreme nearer the open is hit first. A gap through a level fills at the open. `use_bar_magnifier` uses lower-timeframe data instead (Premium). | [TradingView Strategies docs][6], [TradingView FAQ][7] | It applies to every backtest, so the results have to be read with it in mind. |

Not testable with chart OHLCV alone:
- "Institutional intent".
- Order flow or volume delta.
- News filters (they need an external calendar).
- True intrabar order of events without the bar magnifier.

## 2. Exact rules in v2
**Entry signal.** v1's confirmed L/S. The v1 mode defaults to the "v1 Sweep → warning-candle breakout" option.
- EARLY L: a closed candle's previous close was ≥ the box center C, its low went below C, and it closed above C.
- L: a later closed candle closes above the frozen warning-candle high.
- Before confirmation, invalidation, target, expiry and box change are checked first.
- Shorts are the mirror image.

**Entry modes.**
- **Market next open** (default): the order is sent at the L/S close and fills at the next bar open.
- **Retest limit:** a limit order at the frozen center C.
  - Valid for `v2RetestBars` bars (default 6).
  - Canceled if the frozen stop level trades before it fills.

**Frozen when the order is placed:**
- **Stop** = frozen sweep low − `v2StopTicks` ticks (default 2). Shorts: sweep high + ticks.
- **TP1** = nearest yellow edge (avg(lo, C) or avg(C, hi)) or box midpoint C, in the trade direction and at least `v2MinTpTicks` ticks (default 4) beyond the reference.
  - The reference is the signal close in market mode, or C in retest mode.
- **TP2** = next level beyond TP1 from all named-box edges, centers and yellow edges plus every enabled calendar map level.
- **TP3** = the level after TP2.
- If TP2 or TP3 doesn't exist, it collapses onto the previous target.
- If there is no TP1, or the stop is on the wrong side of the reference, the trade is skipped and counted.

**Position size and partials.**
- 1 contract: a single exit at `v2Single` (TP1 by default).
- 2 or more contracts: split by `v2Tp1Pct` / `v2Tp2Pct` (default 50/25), the rest goes to TP3.

**Breakeven (on by default).** After a closed bar has touched TP1, the stop on the TP2/TP3 legs moves to the average entry price from the next bar on. The intrabar touch is not used.

**Opposite confirmed signal.** Configurable: Reverse (default), Close only, or Ignore. A pending retest order is canceled on reverse or close.

**Same bar touches both stop and target.**
- Erick's rule is to assume the stop hit first.
- The TradingView emulator can't be forced to do that: it uses the open-proximity path.
- So v2 counts how many in-trade bars touched both the stop and TP1, shown in an on-chart table, to bound how much the result depends on this.
- To apply the conservative rule, re-score each of those trades as a full stop loss.
- For the true intrabar order, turn on Bar Magnifier if available.

**Gaps.** If a bar opens beyond the stop, it fills at the open plus 1 tick of slippage (worse). If it opens beyond a target, the limit fills at the open (better), per the emulator rules [6]. Gapped trades should be listed separately in the analysis.

**Costs and settings** (set in strategy(), editable in Properties):
- Commission $2.50 per side per contract; slippage 1 tick.
- 1 contract, pyramiding 0.
- `process_orders_on_close=false`, `calc_on_every_tick=false`.
- `alertcondition()` is commented out in the strategy build (the alert() call is kept). Use v1 for the Pre-Alert/Confirmed alerts.

**Source checks I ran** (static_check.py):
- Parentheses and brackets balance; indentation is clean.
- 4 plots out of 64 (no new plots; the levels are drawn as lines plus one table).
- Same 2 `request.security` calls as v1. Previous-period values use [1]; current-period open/time use lookahead_on.
- No negative offsets.
- All signal state changes happen on confirmed bars.

## 3. ES 5m measurement plan
- **Data:** CME_MINI:ES1! (back-adjusted continuous contract, recorded) on 5m.
- **Dates:** fixed. In-sample 2025-01-02 → 2025-12-31, out-of-sample 2026-01-02 → 2026-09-30. Then repeat on NQ and on 3m and 15m, each separately.
- **Session:** full electronic session. Optionally split RTH 06:30–13:00 PT.
- **Runs, changing one variable at a time:**
  1. Baseline: Market entry, TP1 only, 1 contract.
  2. Single target at TP2, then at TP3.
  3. 3 contracts, 50/25/25 split, breakeven on vs off.
  4. Retest entry vs Market entry.
  5. Opposite-signal handling: Reverse / Close only / Ignore.
  6. Stop buffer of 0, 2 and 4 ticks.
- **Metrics:**
  - Net P/L after costs, profit factor, expectancy per trade in R.
  - Win rate, long/short counts and P/L.
  - Max drawdown, closed-trade vs intratrade (from the Tester's run-up/drawdown).
  - Average bars held.
  - Skipped trades.
  - The ambiguous-bar count, with the stop-first re-score.
  - Gap fills.
  - Retest fill rate.
  - Signal-level counts: EARLY → L conversion, invalidations, expirations, confirmation delay in bars.
- **Rule:** pick settings on in-sample only and report out-of-sample as-is. At least 100 trades per variant before drawing conclusions.
- **Export:** List of Trades CSV from the Tester, plus the browser task's signal log, joined on bar time (PT).

## 4. Open questions
- Should TP1 skip a yellow edge that is closer than 1R? That would be a minimum-R:R filter.
- Should an MSS filter (close through the last confirmed counter-pivot) or an FVG-retest entry be added as v3 toggles?
- Should trading be limited to RTH or a time window, and what are the prop-firm daily-loss and trailing-drawdown rules?
- Should breakeven include costs (entry ± 1–2 ticks)?
- Contract roll handling for ES1!.

[1]: https://liquidityscan.io/blog/liquidity-sweep-then-structure-shift-the-stop-hunt-to-reversal-sequence
[2]: https://www.ictkillzone.com/ict-liquidity-sweep
[3]: https://www.goforexhub.com/en/guides/trading-course-ict-smc-algo/sweep-mss-fvg-model
[4]: https://tradingplan.io/strategies/liquidity-sweep-reversal/
[5]: https://liquiditysweeptrading.com/learn/liquidity-trading-strategies/
[6]: https://www.tradingview.com/pine-script-docs/concepts/strategies/
[7]: https://www.tradingview.com/pine-script-docs/faq/strategies/
