# LONG HISTORY: ES v11 TradingView CSVs, 15m (May–Oct 2026) and 30m (Jan 2025–Oct 2026)
- **Scripts:** v9_analysis/longh.py. Full tables are below and in v9_analysis/longh_out.md.
- **Stats are per position**, with the scalp and runner legs merged.
- **Month regimes** use Yahoo ES=F daily bars.
- **Structure-break is OFF at 15m and above in v11** (cutoff = 15 min). So these runs test the v1 sweep/reclaim confirmation, not the setup that worked on 3m/5m.
- **FLARE_v11_SB_30m.csv was not present** when this was run. Also present but not requested: FLARE_v11_S_{3m,5m,15m}.csv (not analysed).

## Key findings
1. **The held ≥ 50 filter cannot be validated from these CSVs.** v11 already applies it (Min held % = 50), so there are no positions with h% < 50. Only "50–65", "≥66" and "no history" (passes) exist.
   - **To validate it:** export 30m with Min level held % = 0.
   - **Within the filtered set (30m, split at 2025-11-21):**
     - 50–65: PF 1.65 → 0.45 (H1 → H2).
     - ≥66: PF 2.01 → 0.64.
     - No history: 0.66 → 0.92.
   - **By quarter, neither bucket is stable** (≥66 ranges from PF 0.19 to 3.67).
   - **Held% does not protect the second year on 30m.**
2. **30m loses over the long sample:**
   - Overall PF 0.87 (−$13,380).
   - 2025: +$11,789, profitable in 3 of 4 quarters.
   - 2026 Q1–Q3: −$23,375, every quarter losing.
   - The structure has decayed.
3. **Losing regime = trend months.**
   - On 30m, months whose |close − open| is ≥ 60% of the month's range lost in **6 of 6** (−$13,260).
   - Other months were flat overall (−$120).
   - The best months were wide two-way months (2025-04, range 16.7%, trend 0.06: +$12,990) and choppy months (2026-09, trend 0.04).
   - Choppy months still lose too: 2026-07 had trend 0.08 and lost −$9,258 (30m) and −$17,752 (15m). So trend explains some losses, not all.
4. **Side asymmetry on 30m:**
   - Longs: PF 1.41 (+$18,640).
   - Shorts: PF 0.46 (−$32,020).
   - On 15m it is the opposite (shorts 1.20, longs 0.81), so treat this as regime-driven, not a rule.
5. **Level family (30m):**
   - Monday (w3): PF 1.06.
   - Daily (w2): PF 1.00.
   - Weekly (w4): 0.80.
   - Monthly (w5): 0.57.
   - Quarterly / yearly (w6/w7): 0.23–0.31, n = 8.
   - Higher-timeframe levels do worse at 30m. On 15m, w4 is best (1.62) and w2 is worst (0.37), so this is inconsistent across timeframes.
6. **Legs:** in losing months both legs lose. The scalp leg is not a cushion: it is only 0.5R to the half-way point, while the full stop hits both legs.
   - 30m runner total: −$1,450 vs scalp −$11,930.
   - The runner carries the good months (2025-04: +$9,282).

## Verdict
- **v11 at 15m/30m (no structure-break) has no edge over a long history:** 30m PF 0.87, and 15m PF 1.01 with a −$17.7k July.
- **The 3m/5m results (structure-break ON) are ~2 months only.** Long-history validation of the actual H config needs:
  - 3m/5m exports over a longer period, if TradingView history allows (Premium); or
  - **FLARE_v11_SB_30m** (structure-break forced on at 30m by setting the cutoff above 30).
- **Before trusting held ≥ 50:** export 30m with Min held % = 0 and compare h% ≥ 50 vs < 50 per half and per quarter.
- **Candidate filter (an observation, not tested as a rule):** skip during established trend months. This would need a non-lookahead proxy, e.g. month-to-date |close − MO| / MTD range ≥ 0.6. Test it only after the above.

---
# Full tables

## 15m: 95 positions 2026-05-04 → 2026-10-14, net $675, PF 1.01

### Monthly
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| 2026-05 | 8 | -430 | 0.88 | 260 | -690 |
| 2026-06 | 15 | 5712 | 1.55 | 1450 | 4262 |
| 2026-07 | 29 | -17752 | 0.22 | -9170 | -8582 |
| 2026-08 | 20 | 612 | 1.07 | 1870 | -1258 |
| 2026-09 | 15 | 13862 | 4.67 | 6325 | 7538 |
| 2026-10 | 8 | -1330 | 0.76 | -928 | -402 |

### Quarterly
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| 2026Q2 | 23 | 5282 | 1.38 | 1710 | 3572 |
| 2026Q3 | 64 | -3278 | 0.91 | -975 | -2302 |
| 2026Q4 | 8 | -1330 | 0.76 | -928 | -402 |

### held% bucket × half (mid 2026-07-25)
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| 50-65 H1 | 14 | -3965 | 0.58 | -1632 | -2332 |
| no history H1 | 12 | -6208 | 0.23 | -2198 | -4010 |
| >=66 H1 | 21 | -872 | 0.94 | -2705 | 1832 |
| no history H2 | 18 | 2295 | 1.27 | 2005 | 290 |
| 50-65 H2 | 15 | 6138 | 2.14 | 1400 | 4738 |
| >=66 H2 | 15 | 3288 | 1.44 | 2938 | 350 |

### held% bucket × quarter
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| 50-65 2026Q2 | 5 | 3125 | 5.06 | 1775 | 1350 |
| no history 2026Q2 | 7 | -2282 | 0.44 | -235 | -2048 |
| >=66 2026Q2 | 11 | 4440 | 1.48 | 170 | 4270 |
| >=66 2026Q3 | 21 | 1040 | 1.10 | 1320 | -280 |
| no history 2026Q3 | 22 | -270 | 0.98 | 722 | -992 |
| 50-65 2026Q3 | 21 | -4048 | 0.70 | -3018 | -1030 |
| >=66 2026Q4 | 4 | -3065 | 0.15 | -1258 | -1808 |
| no history 2026Q4 | 1 | -1360 | 0.00 | -680 | -680 |
| 50-65 2026Q4 | 3 | 3095 | 7.38 | 1010 | 2085 |

### Level family (weight)
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| w4 | 19 | 7798 | 1.62 | 5050 | 2748 |
| w3 | 43 | 4882 | 1.25 | 2222 | 2660 |
| w2 | 19 | -7528 | 0.37 | -4358 | -3170 |
| w5 | 8 | 682 | 1.15 | -365 | 1048 |
| w6 | 6 | -5160 | 0.16 | -2742 | -2418 |

### Side
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| short | 50 | 5638 | 1.20 | 4245 | 1392 |
| long | 45 | -4962 | 0.81 | -4438 | -525 |

### Regime (month range % of open; trend = |close−open|/range)
| regime | months | net $ | months lost |
|---|---|---|---|
| range ≥ median (4.4%) | 3 | 19145 | 1/3 |
| range < median | 3 | -18470 | 2/3 |
| trend ≥ 0.6 | 1 | -430 | 1/1 |
| trend < 0.6 | 5 | 1105 | 2/5 |
| up month | 4 | 12715 | 2/4 |
| down month | 2 | -12040 | 1/2 |

| month | range % | trend | dir | net $ |
|---|---|---|---|---|
| 2026-05 | 5.7 | 0.82 | up | -430 |
| 2026-06 | 5.3 | 0.12 | down | 5712 |
| 2026-07 | 4.1 | 0.08 | down | -17752 |
| 2026-08 | 3.9 | 0.50 | up | 612 |
| 2026-09 | 4.4 | 0.04 | up | 13862 |
| 2026-10 | 2.9 | 0.35 | up | -1330 |

## 30m: 158 positions 2025-01-02 → 2026-10-11, net $-13380, PF 0.87

### Monthly
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| 2025-01 | 9 | 5798 | 1.64 | 830 | 4968 |
| 2025-02 | 11 | -3122 | 0.60 | -1298 | -1825 |
| 2025-03 | 7 | -370 | 0.88 | -485 | 115 |
| 2025-04 | 6 | 12990 | 7.40 | 3708 | 9282 |
| 2025-05 | 5 | -2900 | 0.00 | -1450 | -1450 |
| 2025-06 | 6 | -1048 | 0.76 | -1180 | 132 |
| 2025-07 | 2 | -2095 | 0.00 | -1048 | -1048 |
| 2025-08 | 10 | 1025 | 1.22 | 675 | 350 |
| 2025-09 | 5 | -1588 | 0.20 | -588 | -1000 |
| 2025-10 | 5 | -1262 | 0.40 | -212 | -1050 |
| 2025-11 | 11 | 3065 | 1.74 | 2382 | 682 |
| 2025-12 | 4 | 1298 | 2.80 | 968 | 330 |
| 2026-01 | 9 | 1348 | 1.22 | 880 | 468 |
| 2026-02 | 8 | 858 | 1.22 | 135 | 722 |
| 2026-03 | 5 | -10375 | 0.00 | -5188 | -5188 |
| 2026-04 | 6 | -6310 | 0.00 | -3155 | -3155 |
| 2026-05 | 2 | -1045 | 0.00 | -522 | -522 |
| 2026-06 | 8 | -1805 | 0.77 | -1790 | -15 |
| 2026-07 | 12 | -9258 | 0.23 | -5140 | -4118 |
| 2026-08 | 12 | -4320 | 0.12 | -2490 | -1830 |
| 2026-09 | 13 | 7532 | 2.17 | 3498 | 4035 |
| 2026-10 | 2 | -1795 | 0.00 | -898 | -898 |

### Quarterly
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| 2025Q1 | 27 | 2305 | 1.12 | -952 | 3258 |
| 2025Q2 | 17 | 9042 | 1.97 | 1078 | 7965 |
| 2025Q3 | 17 | -2658 | 0.70 | -960 | -1698 |
| 2025Q4 | 20 | 3100 | 1.45 | 3138 | -38 |
| 2026Q1 | 22 | -8170 | 0.60 | -4172 | -3998 |
| 2026Q2 | 16 | -9160 | 0.40 | -5468 | -3692 |
| 2026Q3 | 37 | -6045 | 0.74 | -4132 | -1912 |
| 2026Q4 | 2 | -1795 | 0.00 | -898 | -898 |

### held% bucket × half (mid 2025-11-21)
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| 50-65 H1 | 29 | 11260 | 1.65 | 2238 | 9022 |
| no history H1 | 22 | -6695 | 0.66 | -4398 | -2298 |
| >=66 H1 | 23 | 5895 | 2.01 | 3485 | 2410 |
| 50-65 H2 | 31 | -14235 | 0.45 | -6785 | -7450 |
| >=66 H2 | 29 | -8490 | 0.64 | -5932 | -2558 |
| no history H2 | 24 | -1115 | 0.92 | -975 | -140 |

### held% bucket × quarter
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| 50-65 2025Q1 | 11 | 3728 | 1.41 | 440 | 3288 |
| no history 2025Q1 | 6 | -7485 | 0.12 | -3230 | -4255 |
| >=66 2025Q1 | 10 | 6062 | 3.67 | 1838 | 4225 |
| >=66 2025Q2 | 3 | -805 | 0.00 | -402 | -402 |
| no history 2025Q2 | 7 | 2530 | 1.57 | -210 | 2740 |
| 50-65 2025Q2 | 7 | 7318 | 2.78 | 1690 | 5628 |
| no history 2025Q3 | 6 | 2540 | 1.96 | 1182 | 1358 |
| 50-65 2025Q3 | 6 | -3510 | 0.12 | -1505 | -2005 |
| >=66 2025Q3 | 5 | -1688 | 0.19 | -638 | -1050 |
| >=66 2025Q4 | 6 | 1615 | 2.16 | 2332 | -718 |
| no history 2025Q4 | 5 | -3150 | 0.27 | -1700 | -1450 |
| 50-65 2025Q4 | 9 | 4635 | 4.71 | 2505 | 2130 |
| 50-65 2026Q1 | 8 | -4180 | 0.51 | -1590 | -2590 |
| >=66 2026Q1 | 12 | -3970 | 0.67 | -2572 | -1398 |
| no history 2026Q1 | 2 | -20 | 0.00 | -10 | -10 |
| no history 2026Q2 | 7 | -4708 | 0.35 | -2485 | -2222 |
| >=66 2026Q2 | 4 | 1548 | 1.75 | 18 | 1530 |
| 50-65 2026Q2 | 5 | -6000 | 0.00 | -3000 | -3000 |
| no history 2026Q3 | 12 | 3268 | 1.58 | 1472 | 1795 |
| 50-65 2026Q3 | 13 | -3955 | 0.56 | -2582 | -1372 |
| >=66 2026Q3 | 12 | -5358 | 0.38 | -3022 | -2335 |
| 50-65 2026Q4 | 1 | -1010 | 0.00 | -505 | -505 |
| no history 2026Q4 | 1 | -785 | 0.00 | -392 | -392 |

### Level family (weight)
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| w4 | 29 | -4240 | 0.80 | -3188 | -1052 |
| w3 | 50 | 1688 | 1.06 | -2888 | 4575 |
| w2 | 54 | -40 | 1.00 | -350 | 310 |
| w5 | 17 | -5882 | 0.57 | -3815 | -2068 |
| w6 | 5 | -2738 | 0.31 | -1375 | -1362 |
| w7 | 3 | -2168 | 0.23 | -752 | -1415 |

### Side
| key | n | net $ | PF | scalp $ | runner $ |
|---|---|---|---|---|---|
| long | 81 | 18640 | 1.41 | 2848 | 15792 |
| short | 77 | -32020 | 0.46 | -15215 | -16805 |

### Regime (month range % of open; trend = |close−open|/range)
| regime | months | net $ | months lost |
|---|---|---|---|
| range ≥ median (5.6%) | 11 | -3045 | 8/11 |
| range < median | 11 | -10335 | 6/11 |
| trend ≥ 0.6 | 6 | -13260 | 6/6 |
| trend < 0.6 | 16 | -120 | 8/16 |
| up month | 14 | -5362 | 9/14 |
| down month | 8 | -8018 | 5/8 |

| month | range % | trend | dir | net $ |
|---|---|---|---|---|
| 2025-01 | 5.9 | 0.33 | up | 5798 |
| 2025-02 | 5.3 | 0.06 | down | -3122 |
| 2025-03 | 8.2 | 0.64 | down | -370 |
| 2025-04 | 16.7 | 0.06 | down | 12990 |
| 2025-05 | 7.3 | 0.72 | up | -2900 |
| 2025-06 | 6.7 | 0.89 | up | -1048 |
| 2025-07 | 3.9 | 0.53 | up | -2095 |
| 2025-08 | 4.5 | 0.40 | up | 1025 |
| 2025-09 | 5.9 | 0.68 | up | -1588 |
| 2025-10 | 6.1 | 0.36 | up | -1262 |
| 2025-11 | 5.6 | 0.05 | down | 3065 |
| 2025-12 | 4.0 | 0.14 | up | 1298 |
| 2026-01 | 3.3 | 0.28 | up | 1348 |
| 2026-02 | 4.0 | 0.18 | down | 858 |
| 2026-03 | 8.2 | 0.45 | down | -10375 |
| 2026-04 | 11.4 | 0.91 | up | -6310 |
| 2026-05 | 5.7 | 0.82 | up | -1045 |
| 2026-06 | 5.3 | 0.12 | down | -1805 |
| 2026-07 | 4.1 | 0.08 | down | -9258 |
| 2026-08 | 3.9 | 0.50 | up | -4320 |
| 2026-09 | 4.4 | 0.04 | up | 7532 |
| 2026-10 | 2.9 | 0.35 | up | -1795 |
---
# Regime filters (ES, structure-break ON 15m/30m + v11 30m + 3m/5m check)
- **Scripts:** v9_analysis/regime.py. Output: v9_analysis/regime_out.txt.
- **No lookahead:** features use only Yahoo ES=F 1h bars completed before entry. The month/week/day roll at 15:00 PT. Daily features use completed prior days.
- **Pass rule:** 30+ trades per half and PF > 1 in each half.

| Filter | SB 15m (H1 / H2) | SB 30m 2025 / 2026 | v11 30m 2025 / 2026 | 3m (H1 / H2) | 5m (H1 / H2) |
|---|---|---|---|---|---|
| Baseline | 0.99 / 1.31 (n 45) | 2.62 / 0.28 (n 58) | 1.26 / 0.59 (n 158) | 2.19 / 1.64 | 1.27 / 2.03 |
| **MTD trend ≥ 0.6 → skip** | 1.07 / 0.99 | 4.07 / 0.38 (net +$3,360) | 2.03 / **0.68** (PF 1.18, +$13,385) | 2.19 / 1.85 | 1.38 / 2.44 |
| MTD ≥ 0.6 → with-trend only | 0.99 / 1.07 | 2.80 / 0.29 | 1.40 / 0.56 | 2.19 / 1.77 | 1.27 / 2.17 |
| WTD ≥ 0.6 → skip | 1.41 / 1.29 (n 30) | 2.06 / 0.15 | 1.91 / 0.47 | 1.27 / 1.47 | 0.35 / 2.66 |
| WTD ≥ 0.6 → with-trend only | 1.09 / 1.10 | 2.80 / 0.23 | 1.29 / 0.44 | 1.86 / 1.50 | 0.87 / 2.57 |
| Prior-day range ≥ 1.5 × ADR10 → skip | 0.71 / 1.34 | 2.60 / 0.24 | 1.35 / 0.50 | 2.84 / 1.88 | 1.12 / 2.34 |
| 3-day streak → skip counter-trend | 1.15 / 1.19 | 4.34 / 0.30 | 1.53 / 0.45 | 2.66 / 1.65 | 0.88 / 3.36 |
| Beyond prior month H/L → skip counter-trend | 0.99 / 1.37 | 2.41 / 0.29 | 1.09 / 0.54 | 2.19 / 1.50 | 2.03 / 1.88 |

## Result: nothing passes
- **2026 loses on 30m under every filter:** best is MTD-skip on v11 30m at PF 0.68; the SB 30m best is 0.38. The 2025 → 2026 decay is not explained by month/week trend, range expansion, streaks or breakouts.
- **The 15m sample is too small:** n = 45 total, about 20–25 per half. WTD-skip (1.41 / 1.29) looks good but has only 18 / 12 trades.
- **MTD trend ≥ 0.6 → skip is the most useful filter:**
  - It turns v11 30m from −$13.4k into +$13.4k overall.
  - It does not hurt 3m/5m: PF 1.88 → 2.02 and 1.71 → 1.97.
  - But it fails the both-halves rule (H2 0.72), so it is a candidate, not a survivor.
- **No v13 built,** per the "only if something passes" rule.

**If you want to test MTD-skip in TradingView anyway:**
- It is a small change: at entry, skip if |close − monthly_open| / (month-to-date high − month-to-date low) ≥ 0.6, using completed-bar values.
- Test it on 3m/5m/30m.
