# FLARE v7 validation: A (baseline) vs AC (+structure-break) vs AB (+CHOP)

**Data:** v7 CSVs. Script: v7_analysis/val.py; output in v7_analysis/val_out.txt.
- **Split:** each timeframe is split at the median entry time of A, and AC uses the same date.
- **Matching:** trades are matched across runs by entry time and side.
- **Caveat:** the AC∩AB combo and the 00:00–03:00 exclusion are approximations made by filtering the CSVs; they are not real reruns. Filtering ignores how removing a trade changes later trades.

## Halves (n / net / PF)
| TF | A 1st | A 2nd | AC 1st | AC 2nd | A trades removed by AC: 1st / 2nd |
|---|---|---|---|---|---|
| 3m | 85 / −1,450 / 0.91 | 86 / −742 / 0.96 | 27 / +3,378 / 1.55 | 47 / +865 / 1.08 | −1,478 (0.89) / −2,278 (0.79) |
| 5m | 74 / −5,432 / 0.72 | 75 / −2,300 / 0.87 | 41 / +908 / 1.09 | 31 / +958 / 1.11 | −5,540 (0.56) / −3,162 (0.77) |
| 15m | 69 / −16,445 / 0.41 | 70 / +6,762 / 1.53 | 33 / −4,290 / 0.70 | 28 / +4,398 / 1.62 | −15,335 (0.18) / +315 (1.04) |
| 30m | 113 / −2,065 / 0.94 | 114 / −12,945 / 0.69 | 42 / +15,390 / 2.32 | 46 / −14,342 / 0.49 | −2,002 (0.92) / −3,840 (0.83) |
| 2h | 32 / +4,802 / 1.55 | 33 / −740 / 0.96 | 13 / +1,398 / 1.34 | 14 / −7,870 / 0.09 | +2,350 (1.41) / +6,175 (1.50) |

- **3m and 5m:** AC is PF > 1 in both halves, and the trades it removed were net losers in both halves.
  - It fails the 30-trades-per-half rule on 3m (27 in the 1st half). 5m passes narrowly (41 / 31).
- **15m:** AC beats A in the 1st half (0.70 vs 0.41) but is roughly level in the 2nd (1.62 vs 1.53). The removed trades were losers only in the 1st half.
- **30m:** AC's 2nd half collapses (0.49) while the removed trades were losers. This is inconsistent; it fails.
- **2h:** AC removed winners (PF 1.41 / 1.50) and is 0.09 in the 2nd half. It fails.

## Bootstrap of AC trade P&L
10,000 resamples with replacement, plus 5,000 shuffles for max drawdown.

| TF | n | P(PF > 1) | PF 5% / 50% / 95% | Net 5th pct | Net median | Shuffled max DD median / 95th |
|---|---|---|---|---|---|---|
| 3m | 74 | 0.78 | 0.77 / 1.25 / 1.97 | −4,595 | +4,168 | 3,990 / 6,372 |
| 5m | 72 | 0.62 | 0.65 / 1.09 / 1.74 | −7,422 | +1,640 | 4,875 / 7,712 |

The edge is not yet statistically distinguishable from zero: the 5th-percentile PF is below 1 on both timeframes.

## Combos (approximate)
| TF | AC ∩ CHOP pass: all / 1st / 2nd PF (n) | AC excluding 00:00–03:00 PT: all / 1st / 2nd PF (n) |
|---|---|---|
| 3m | 1.10 (41) / 0.97 (15) / 1.18 (26) | 1.29 (66) / 1.80 (24) / 1.02 (42) |
| 5m | 1.28 (38) / 1.25 (22) / 1.31 (16) | 1.10 (62) / 0.85 (36) / 1.48 (26) |
| 15m | 1.72 (38) / 1.27 (21) / 2.73 (17) | 0.88 (50) / 0.70 (27) / 1.25 (23) |
| 30m | 0.72 (52) / 2.18 (20) / 0.40 (32) | 1.22 (71) / 2.81 (35) / 0.53 (36) |
| 2h | 0.37 (8) | 0.51 (26) |

- **CHOP on top of AC** looks helpful on 5m and 15m, but every half has fewer than 30 trades, so it is not accepted. AB alone was below 1 on every timeframe.
- **Excluding 00:00–03:00** is mixed (it hurts 5m in the 1st half and 15m overall), so it is not accepted.

## Verdict
- **Structure-break confirmation (c)** is the first change that is positive in both halves on 3m and 5m, and the trades it removes are losers in both halves there. Treat it as provisionally supported on 3m and 5m only.
  - The evidence is weak: about 70 trades per timeframe, P(PF > 1) of 0.62–0.78, and a 5th-percentile net of −$4.6K to −$7.4K.
- It does not hold on 30m or 2h, and 15m is inconclusive.
- **v8 defaults are now** v7 A + (c) ON when the chart timeframe is below `v8MssBelowMin`. That input defaults to 120 minutes, as requested, so 30m remains included.
  - **Recommendation:** set the cutoff to 15 (3m/5m only) unless the sensitivity runs rescue 15m and 30m.
- **Next:** the TradingView sensitivity grid.
  - Pivot length 2 / 3 / 4 × N bars 8 / 12 / 16, on 3m and 5m.
  - Accept (c) only if most grid cells keep PF > 1 in both halves.
  - Then extend the date range to reach 30 or more trades per half.

**v8 static checks:**
- `static_check.py`: parentheses and brackets balance, indentation is clean, 4 of 64 plots, 5 `request.security` calls with `[1]` + lookahead_on, no negative offsets.
- `static_check2.py`: shorttitle 'FLARE v8' is 8 characters, no use-before-declare.
