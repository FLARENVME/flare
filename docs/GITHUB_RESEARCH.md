# GitHub Research: Ideas for the ES/NQ Calendar-Level Sweep/Reclaim Reversal System
Date: 2026-10-15. All repo URLs fetched with WebFetch. Licenses/stars come from the GitHub API on this date.
GPL repos: the logic is described here in my own words. No code was copied.

| Repo | License | Stars | Notes |
|---|---|---|---|
| https://github.com/joshyattridge/smart-money-concepts | MIT | ~2.1k | swings, BOS/CHoCH (close_break), liquidity + Swept index, prev H/L, sessions |
| https://github.com/iterativv/NostalgiaForInfinity | GPL-3.0 | ~3.5k | freqtrade strategy: multi-TF regime gating, profit/time-tiered exits |
| https://github.com/freqtrade/freqtrade (docs) | GPL-3.0 | ~55k | custom_stoploss, minimal_roi (time-decaying target), protections, hyperopt, lookahead-analysis |
| https://github.com/freqtrade/freqtrade-strategies | GPL-3.0 | ~5.6k | community strats; README warns they are examples and not proven profitable |
| https://github.com/jesse-ai/jesse | MIT | ~8.7k | ATR-based stop/target sizing idioms, multi-TF candles, optimize mode |
| https://github.com/polakowo/vectorbt | Apache-2.0 + Commons Clause (NOASSERTION) | ~9.4k | walk-forward/param-grid examples, SL/TSL/TP sweeps via from_signals |
| https://github.com/hummingbot/hummingbot | Apache-2.0 | ~20k | "triple barrier" executor (SL / TP / time limit / trailing stop) |
| https://github.com/mementum/backtrader | GPL-3.0 | ~23k | bracket orders, StopTrail; inactive since 2024 |

**Evidence caveat:** none of these repos publish audited backtests on ES/NQ. NFI and freqtrade-strategies results are crypto-only, self-reported, and heavily hyperopted, so treat them as hypotheses. Everything below is meant to be tested in your own walk-forward.

## Ranked ideas (each one is a single toggle)

1. **Trend-day / regime veto** (NFI multi-TF gating; freqtrade informative pairs)
   NFI only allows entries when higher-TF conditions agree. Translation: `useRegimeVeto`. Skip a fade when the session's range so far is already greater than X × 20-day ADR at signal time, or when price has stayed on one side of VWAP / the opening-range mid for N straight bars, or when the 1h EMA slope is steep against the fade. This goes straight at the "continues through" losses. Pine: yes (request.security on 60m, VWAP, ta.atr daily).

2. **MSS/CHoCH confirmation after the sweep** (smartmoneyconcepts `bos_choch(close_break=True)` + `liquidity().Swept`)
   Toggle `requireMSS`. After the sweep plus reclaim, wait for a close beyond the most recent internal swing (lower TF, small swing length) in the reversal direction before entering. The stop stays at the sweep extreme. Expect fewer trades and a higher win rate. **Pitfall:** the library's swing_highs_lows is centered (it uses future candles). In Pine, a swing is only confirmed `len` bars later, so act on ta.pivothigh(len,len) only after it confirms. Pine: yes.

3. **ATR-normalized stop cap / skip** (jesse ATR idioms; freqtrade custom_stoploss)
   Toggle `maxStopATR`. If the distance from entry to the sweep extreme is more than k × ATR(14), skip the trade (or enter on a retrace limit instead). This fixes the "growing stops vs fixed targets" problem at the source. Pine: yes.

4. **Minimum R:R gate to the next mapped level**
   Toggle `minRR`. Only take the trade if (next level − entry) / (entry − stop) ≥ 1.5–2. Otherwise skip it, or target the level after next. Same logic as freqtrade's custom entry checks. Pine: yes. Cheap test, and likely a large PF effect given a 20–37% win rate.

5. **Triple barrier with a time stop** (hummingbot PositionExecutor/triple-barrier; freqtrade minimal_roi time table)
   Toggle `timeStopBars`. Exit after N bars (e.g. 10 on 3m, 6 on 15m) if the trade hasn't reached +0.5R. A true reversal should pay quickly; trades that stall usually turn into trend-day continuation. freqtrade's ROI table version: the required profit falls as time passes. Pine: yes (bar_index − entryBar).

6. **Partial exit at 1R, then break-even/trail** (NFI tiered exits; backtrader brackets)
   Toggle `partialAt1R`. Close 50% at 1R (or at the first intermediate level such as a mid), move the stop to break-even, and let the rest run to the mapped level. Pine: yes (strategy.exit with qty_percent).

7. **ATR / chandelier trailing on the runner** (freqtrade custom_stoploss; vectorbt sl_trail; hummingbot trailing_stop activation)
   Toggle `trailMode`. Off / ATR×k / last-swing. The trail only arms after +1R (hummingbot's "activation price" concept). Pine: yes (strategy.exit trail_points/trail_offset, or a manual swing trail).

8. **Entry timing: retrace limit instead of a close-confirmation market entry**
   Toggle `entryMode = close | retrace50`. After the confirmation close, place a limit at 50% of the warning/confirmation candle (or the reclaimed level itself) and cancel after M bars. This tightens the stop relative to the target. Mirrors freqtrade custom_entry_price. Pine: yes. Expect lower fill rate; check whether the unfilled trades were the winners (adverse selection).

9. **Session/time-of-day + loss protections** (freqtrade Protections: StoplossGuard, CooldownPeriod; smc `sessions`)
   Toggle `sessionFilter`. Only trade RTH windows (e.g. 9:30–11:30 and 13:30–15:00 ET). After 2 stop-outs on the same side in a day, stop fading that side (StoplossGuard logic, which also catches trend days). Pine: yes.

10. **Overfitting hygiene (not a signal)** (freqtrade lookahead-analysis & recursive-analysis docs; hyperopt; vectorbt walk-forward example)
   - Run anchored walk-forward (e.g. 12 months in-sample / 3 months out-of-sample, rolled). Report out-of-sample PF only.
   - Optimize ≤3 parameters at a time. Prefer flat plateaus over the single best value.
   - Test for lookahead: centered pivots, request.security without `lookahead_off` / [1] offset, and daily/weekly opens taken from incomplete bars.
   - Use realistic costs: ES ≈ 1 tick slippage + commission per side. At a 20–37% win rate, costs swing PF a lot.
   - The 2h PF of ~1.1 may come from a small sample. Check the trade count and do a bootstrap/Monte Carlo before trusting it.

## Recommended test order
4 (minRR) → 3 (maxStopATR) → 1 (regime veto) → 5 (time stop) → 2 (MSS) → 6/7 exits → 8 → 9. Turn on one toggle at a time against the baseline, and check out-of-sample on the walk-forward folds.
