# HTF bias: offline check on the ES v11 TradingView CSVs
- **Scripts:** offline_v9/htfbias.py. Output: offline_v9/htfbias_out.txt.
- **Bias data:** Yahoo ES=F 1h (730 days); 4h bars are built from the 1h bars, starting at the 15:00 PT session open.
- **CSV timestamps are PT** (I checked entry prices against Yahoo 5m bars).
- **No lookahead:** only HTF bars completed before the entry time are used.
- **Approximate levels:** DO/WO/MO plus prior D/W/M H/L/M only, not the full FLARE map.
- **Format:** each cell is half-1 / half-2 positions and PF.

| Chart TF | Option | With bias | Against bias |
|---|---|---|---|
| 3m (55) | 1h (a) | 13/16 PF 4.24/1.56 | 10/16 PF 0.55/1.77 |
| 3m | 4h (a) | 14/16 PF 5.33/1.52 | 9/16 PF 0.19/1.82 |
| 3m | 4h (b) | 15/16 PF 3.76/0.91 | 8/16 PF 0.16/3.11 |
| 3m | 4h (c) | 8/11 PF 4.58/1.52 | 5/11 PF 1.26/3.33 |
| 5m (47) | 1h (a) | 11/19 PF 0.68/2.16 | 10/7 PF 2.75/1.61 |
| 5m | 1h (b) | 15/18 PF 1.45/2.16 | 6/8 PF 0.48/1.70 |
| 5m | 4h (c) | 7/9 PF 1.82/4.61 | 4/8 PF 0.84/5.45 |
| 15m (95) | 1h (a) | 22/29 PF 1.14/1.58 | 25/19 PF 0.27/1.50 |
| 15m | 4h (b) | 26/28 PF 1.06/1.59 | 21/20 PF 0.27/1.47 |
| 15m | 4h (d) | 21/16 PF 1.36/1.31 | 11/17 PF 0.42/2.14 |
| 30m (158) | all | mixed; nothing holds in half 2 | |

**Verdict:**
- **No option is consistently better WITH the bias across both halves and timeframes.**
- **The pattern is the same everywhere:** in half 1, with-bias trades beat against-bias trades (often by a lot); in half 2, against-bias trades are equal or better.
- **The closest candidates:**
  - **(a) 1h:** with > against in half 1 on 3m and 15m. It holds in both halves only on 15m, by a hair.
  - **(b):** with > against in both halves only on 5m with 1h and on 15m with 4h.
- **Samples are 5–30 positions per cell.** This is far from proof, and it may be regime-dependent (an Aug–Sep trend, then chop).

**v12:** inputs "HTF bias" (Off / a / b / c / d) and "HTF bias timeframe" (60 / 240), default Off. The bias blocks against-bias entries only (neutral is allowed). It is shown in the signal tooltip, the entry comment ("htf BULL/BEAR/neutral") and the status table row.
- **Pine (b) caveat:** it evaluates the completed HTF bar against the *current* map levels, so on a day or week rollover the levels may already be the new period's.

**Suggested TradingView tests:**
1. 3m and 5m with (a) at 60.
2. 3m and 5m with (b) at 60.
3. If either one helps both halves, try 240.
