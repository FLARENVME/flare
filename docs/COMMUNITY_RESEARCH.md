# Community Indicator Research: Filters/Exits for the Spaceman Level Sweep-Reclaim System
_Compiled 2026-10-15 PT. Target: ES/NQ, 3m–15m, reversal at calendar levels (Y/Q/M/W/D opens, prev H/L, mids, Monday range), EARLY warning → confirmed close beyond warning candle, structural stop past the sweep, target = next mapped level. Baseline: WR 30–37%, PF 0.70–0.94._

## Ground rules
- Every URL below was loaded with WebFetch on 2026-10-15 and showed TradingView's **"Open-source script"** badge. None of these are protected or invite-only. No source code is copied here; only the logic is described in plain words.
- **License**: "MPL-2.0 (verified)" means the license was confirmed on the page or in the source header. "Open source, header unverified" means you need to open the Source tab and read the header before reusing any code. LuxAlgo scripts usually carry **CC BY-NC-SA 4.0** (attribution required, non-commercial, share-alike). Check that before borrowing any code, especially if FLARE will ever be sold.
- You can reimplement the ideas yourself (concepts can't be copyrighted). If you reuse actual code: keep the author's copyright line, keep the license file or header, and follow TradingView House Rules (don't republish code you haven't meaningfully changed).
- **Diagnosis that drives the ranking.** With PF < 1 and a 30–37% win rate at targets that average about 1.5–2R, the losses come mostly from entries that keep running through the level (trend days) and from fills that are too early. So the best filters are ones that **remove trend-day and chop entries** or **require displacement after the sweep**. Indicators that just add more levels rank lower.

## Ranked candidates (expected value × ease)

| # | Candidate | Author | Category | OHLCV-testable in Pine | EV | Ease |
|---|---|---|---|---|---|---|
| 1 | Anchored VWAP +/- SD Bands | Physiks81 | Session VWAP/σ | Yes | High | Very easy |
| 2 | Market Structure Break & Order Block | EmreKb | MSS confirm / OB | Yes | High | Medium |
| 3 | Choppiness Index | mdeacey (also TheLark) | Volatility regime | Yes | Med-High | Very easy |
| 4 | ICT Killzones + Pivots [TFO] | tradeforopp | Time-of-day | Yes | Med-High | Easy |
| 5 | Relative Volume at Time | TradingView | RVOL | Yes (volume) | Medium | Easy |
| 6 | Inversion Fair Value Gaps (IFVG) [LuxAlgo] | LuxAlgo | iFVG | Yes | Medium | Medium |
| 7 | Smart Money Concepts (SMC) [LuxAlgo] | LuxAlgo | CHoCH/BOS, OB, FVG | Yes | Medium | Medium-hard |
| 8 | ATR Stop Loss Finder | veryfid | ATR stop buffer | Yes | Medium (exit) | Very easy |
| 9 | Liquidity Sweeps [LuxAlgo] | LuxAlgo | Sweep detection | Yes | Low-Med | Easy |
| 10 | Divergence for Many Indicators v4 | LonesomeTheBlue | Momentum divergence | Yes | Low-Med | Medium |
| 11 | CVD - Cumulative Volume Delta Candles | TradingView | Volume delta | Partial (needs LTF intrabars) | Low-Med | Medium |

---

### 1. Anchored VWAP +/- SD Bands (Physiks81)
- URL: https://www.tradingview.com/script/lYQ2HxST-Anchored-VWAP-SD-Bands/
- License: **MPL-2.0 (verified, stated on page)**. Keep the attribution header if you reuse code.
- Core rule: VWAP is anchored at the futures open (18:00 ET), daily, or a custom time, with ±1/2/3σ bands and a live z-score of distance from VWAP. Includes reclaim and lost alerts.
- Testable: Yes (`ta.vwap` with stdev is built-in, or accumulate it manually).
- Plug-in (one toggle, **entry filter "VWAP stretch"**): take a fade only when the swept level sits at |z| ≥ 1.0–1.5 from session VWAP in the fade direction (short above +1σ, long below −1σ). Optional exit variant: use VWAP as T1 when it sits closer than the next mapped level. Logic: fades of extended price revert, while fades near VWAP on a trend day keep going.

### 2. Market Structure Break & Order Block (EmreKb)
- URL: https://www.tradingview.com/script/DkE7UniD/
- License: Open source, header unverified (check the Source tab).
- Core rule: a zigzag tracks swings. A bearish MSB happens when, after a higher high, price breaks the prior swing low by more than a fib factor. The order block (OB) is the last opposite-colour candle before the extreme. Also covers breaker and mitigation blocks.
- Testable: Yes (pivots and zigzag on OHLC).
- Plug-in (**entry confirmation "MSS-after-sweep"**): after the EARLY sweep of a Spaceman level, require a close beyond the most recent opposing internal swing (pivot length 2–3 on the entry TF) within N bars (for example 6), instead of only a close beyond the warning candle. This cuts entries without displacement. Optional variant: enter on a retrace into the OB with the stop beyond the sweep wick.

### 3. Choppiness Index (mdeacey, Pine v6; classic version by TheLark)
- URLs: https://www.tradingview.com/script/RPwONIEd-Choppiness-Index/ and https://www.tradingview.com/script/kFH4WVA0-FREE-INDICATOR-CHOPPINESS-INDEX-TREND-DETECTION-FROM-CHAOS/
- License: Open source, header unverified. CHOP itself is a public-domain formula (Dreiss): `100*log10(sum(ATR1,n)/(HH-LL))/log10(n)`.
- Core rule: above 61.8 is choppy or rotational, below 38.2 is trending.
- Testable: Yes, trivially.
- Plug-in (**regime filter**): block fades when CHOP(14) on the 15m or 30m chart is below about 38–45, meaning a trend leg is under way. Fades work best in rotational regimes. A second option is an ATR-percentile filter: skip when ATR(14) is above the 80th percentile of the last 100 days, which also catches news days.

### 4. ICT Killzones + Pivots [TFO] (tradeforopp)
- URL: https://www.tradingview.com/script/nW5oGfdO-ICT-Killzones-Pivots-TFO/
- License: Open source. The header is reported to be MPL-2.0 by a third-party mirror, so confirm it on the Source tab.
- Core rule: it draws configurable session windows (Asia/London/NY AM/NY lunch/PM) and keeps each session's high and low until price trades through them. It also has open-price lines and hit-rate statistics.
- Testable: Yes (`time()` session strings).
- Plug-in (**time-of-day filter**): allow entries only in windows like 09:30–11:30 ET and 13:30–15:30 ET, and block 12:00–13:30 ET plus the first 5 minutes after the cash open. Grid-test the windows on your trade log first. Splitting existing backtest trades by hour costs nothing and is the cheapest test on this list. Bonus: Asia and London session highs and lows can join the level map as extra sweep candidates.

### 5. Relative Volume at Time (TradingView / PineCoders)
- URL: https://www.tradingview.com/script/n0f50JKv-Relative-Volume-at-Time/
- License: Open source. TradingView's own scripts are typically MPL-2.0; verify the header.
- Core rule: compares bar volume, or volume cumulated since the period start, with the average volume at the **same time of day** over the past N sessions. Thresholds can be fixed (2.0) or a σ channel.
- Testable: Yes (ES/NQ volume on CME is good).
- Plug-in (**entry filter "sweep climax"**): require RVOL-at-time ≥ 1.5 on the sweep (warning) bar, which signals stops being absorbed, and ≤ about 1.2 on the confirmation bar. Alternative: skip when cumulative RVOL for the session is ≥ 2 by 10:30, which flags a trend day.

### 6. Inversion Fair Value Gaps (IFVG) [LuxAlgo]
- URL: https://www.tradingview.com/script/8FHucjY6-Inversion-Fair-Value-Gaps-IFVG-LuxAlgo/
- License: Open source. LuxAlgo standard is CC BY-NC-SA 4.0 (verify the header): non-commercial and share-alike.
- Core rule: a 3-bar FVG wider than ATR(200)×mult becomes "inverted" when price **closes through it** against its bias. The inverted gap then acts as support or resistance, and a signal fires on a retest and rejection. The author warns that its plotted signals repaint when backtested (mitigated zones get deleted), so compute your own state on confirmed bars.
- Testable: Yes, if you rebuild it bar by bar.
- Plug-in (**confirmation alternative**): treat "close through the most recent FVG created by the sweep leg" as the reclaim trigger in place of the warning-candle close. That is a stricter displacement test, and it pairs with #2.

### 7. Smart Money Concepts (SMC) [LuxAlgo]
- URL: https://www.tradingview.com/script/CnB3fSph-Smart-Money-Concepts-SMC-LuxAlgo/
- License: Open source, LuxAlgo CC BY-NC-SA 4.0 (verify).
- Core rule: internal and swing BOS/CHoCH, internal and swing OBs (with a volatility filter), EQH/EQL, FVGs with an auto threshold, MTF previous highs and lows, and premium/discount zones.
- Testable: Yes, but it's large and plots much of its state at barstate.islast. Reimplement only the internal CHoCH logic.
- Plug-in (**filter "internal CHoCH" or "premium/discount"**): require an internal CHoCH in the trade direction after the sweep (overlaps #2, so pick one). Alternatively, take shorts only in the premium half and longs only in the discount half of the current swing range.

### 8. ATR Stop Loss Finder (veryfid)
- URL: https://www.tradingview.com/script/LgjsidVh-ATR-Stop-Loss-Finder/
- License: Open source, header unverified.
- Core rule: long stop = low − ATR×mult and short stop = high + ATR×mult (default 1.5).
- Testable: Yes, trivially.
- Plug-in (**exit rule "ATR buffer"**): stop = sweep extreme ± k×ATR(14), with k in {0.1, 0.25, 0.5}, instead of a tick buffer. Also add a **max-risk cap**: skip if stop distance > 1.5×ATR, which removes the low-R:R trades that tend to come with big sweep wicks. Test it together with BE-at-1R. Stops that are too tight plus BE can turn into breakeven churn, so log the MAE/MFE distributions.

### 9. Liquidity Sweeps [LuxAlgo]
- URL: https://www.tradingview.com/script/JRqryeJ5-Liquidity-Sweeps-LuxAlgo/ (note: the "Liquidity Swings" URL returned 404)
- Alternative: Pure Price Action Liquidity Sweeps, https://www.tradingview.com/script/WYB2cYmM-Pure-Price-Action-Liquidity-Sweeps-LuxAlgo/ (seen in search results, not fetched)
- License: Open source, LuxAlgo CC BY-NC-SA 4.0 (verify).
- Core rule: a pivot level counts as swept when a wick passes it and the bar closes back inside ("wick" type), or when price closes through, retests, and leaves an opposite wick ("outbreak and retest"). The swept range becomes a "Sweep Area".
- Plug-in (**filter "confluence"**): require that the Spaceman level coincides (within x ticks) with an intraday swing pivot (len 5–10) that was swept on the same bar. Stacked liquidity makes for higher-quality sweeps. It's also the closest match for checking your own detection logic. Low incremental EV because you already detect sweeps.

### 10. Divergence for Many Indicators v4 (LonesomeTheBlue)
- URL: https://www.tradingview.com/script/n8AGnIZd-Divergence-for-Many-Indicators-v4/
- License: **MPL-2.0** (the v3 source header shows MPL-2.0 © LonesomeTheBlue; v4 is presumably the same, so check).
- Core rule: compares the current bar with up to 16 recent pivots for regular or hidden divergence across RSI, MACD, histogram, Stoch, CCI, Momentum, OBV, VWMACD, CMF, and MFI, with a minimum count of agreeing indicators.
- Plug-in (**filter**): require ≥ 2 regular divergences (for example RSI and MACD histogram) between the sweep extreme and the prior pivot on the entry TF. It usually lowers the trade count a lot, so use a "≥ 1 within the last N bars" version. Use confirmed pivots only, because the "don't wait for confirmation" option repaints.

### 11. CVD - Cumulative Volume Delta Candles (TradingView)
- URL: https://www.tradingview.com/script/NlM312nK-CVD-Cumulative-Volume-Delta-Candles/
- License: Open source (TradingView, Pine v6); verify the header.
- Core rule: estimates volume delta from lower-timeframe intrabar polarity via `request.security_lower_tf` and accumulates it from a session reset. Flags "divergence" when delta polarity ≠ bar polarity.
- Testable: Partly. It needs intrabar data, history depth depends on your plan, and it's not pure OHLCV. A chart-TF proxy is delta ≈ volume×(close−open)/(high−low).
- Plug-in (**filter "absorption"**): on the sweep bar, require delta to oppose the sweep, for example a new low with delta ≥ 0, or the session CVD to make a higher low while price makes a lower low.

---

## Recommended test order
1. **Time-of-day split** (#4) on the existing trade log. No new code; just bucket PF by 30-minute window.
2. **CHOP / ATR-percentile regime** (#3): one line of code.
3. **VWAP z-score stretch** (#1).
4. **MSS-after-sweep confirmation** (#2, or #6 as an alternative), replacing the warning-candle close.
5. **ATR stop buffer and max-risk cap** (#8), crossed with BE-at-1R on/off.
6. Then RVOL (#5), and divergence/CVD (#10/#11) last.
Add one toggle at a time and check results walk-forward (for example, in-sample 2022–2024, out-of-sample 2025–2026). Require more than about 100 trades per variant so that a PF gain isn't just over-fitting from filtering out a handful of trades.
