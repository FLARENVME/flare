# FLARE v3 strategy: trade-list diagnosis and the v4 change

**Data:** TradingView trade-list CSVs from Erick's v3 runs (ES1!, 1 contract, $2.50/side, 1 tick slippage), saved at /home/box/Downloads/FLARE_v3_tf_trades/.
**Scripts:** v3_analysis/diag.py and v3_analysis/lossconc.txt; output in v3_analysis/diag_out_*.txt.

**Holdout:**
- Trades are split chronologically into halves. The first half was used for diagnosis; the second half is the check.
- The "held-out" half was not truly blind: I read both halves before choosing the rule.
- The second half has only about 87–233 trades per timeframe.

**Columns:** trade number, type, time, Signal (entry "L"/"S"; exit "TP1"/"stop"/"L"/"S"), price, net P/L, commission, favorable and adverse excursion (MFE/MAE), cumulative P/L, duration in bars.
- **Missing:** the boundary name, weight and developing flag, and the planned stop and target. Signal is only "L"/"S".
- v4 adds these to the entry comment so the next export can attribute each trade.

**Times:** I assumed the CSV times are PT. RTH = 06:30–13:00. I have not confirmed the chart timezone.

## Results by timeframe
| TF | Trades | PF | Win % | Avg win | Avg loss | Exits: TP1 / stop / opposite | 1st half PF | 2nd half PF |
|---|---|---|---|---|---|---|---|---|
| 3m | 212 | 0.82 | 35 | 440 | −294 | 66 / 128 / 18 | 0.87 | 0.77 |
| 5m | 204 | 0.78 | 37 | 467 | −354 | 73 / 122 / 9 | 0.75 | 0.82 |
| 15m | 248 | 0.78 | 52 | 452 | −630 | 125 / 113 / 10 | 0.55 | 1.15 |
| 30m | 465 | 0.85 | 52 | 557 | −715 | 241 / 204 / 20 | 0.78 | 0.91 |
| 2h | 174 | 1.00 | 61 | 648 | −1032 | 107 / 67 / 0 | 0.93 | 1.05 |

**Typical move size** (median points, entry to exit):

| TF | Stop-out | TP1 | Losses larger than the avg win (share of gross loss) | Break-even win % | Actual win % |
|---|---|---|---|---|---|
| 3m | 5.00 | 7.00 | 41% | 40 | 35 |
| 5m | 6.12 | 6.50 | 35% | 43 | 37 |
| 15m | 9.25 | 6.50 | 74% | 58 | 52 |
| 30m | 10.25 | 7.00 | 73% | 56 | 52 |
| 2h | 14.75 | 7.25 | 82% | 61 | 61 |

## Session, side, holding time, excursions
- **Session:**
  - RTH is worse on 3m (PF 0.65) and 5m (0.63); overnight is about break-even (1.00 / 0.91).
  - 15m and 30m: both sessions lose.
  - 2h: RTH PF 2.19 but on only 27 trades.
  - Not consistent across timeframes, so not chosen.
- **Long vs short:** shorts are slightly worse on 3m to 30m (PF 0.73–0.87 vs 0.68–0.89). The split is roughly balanced and shows no structural bias.
- **Holding time:** median bars for winners vs losers is 7/6 (3m), 6/5 (5m), 2/4 (15m), 1/4 (30m), 1/1 (2h).
- **Excursions:**
  - Only 9–20% of losers ever had MFE (best open profit) at least as large as their final loss. The median loser's MFE is $85–198, so losers are not winners that got cut.
  - Winners' median MFE (about $335–391) is close to their realized profit, which is the TP1 cap.
- **Opposite-signal reversal:** only 0–20 trades per timeframe (≤ 5%), with mixed P/L ranging from −$7.2K (30m) to +$2.0K (3m). Not the cause.

## Diagnosis
- Exits are almost entirely TP1 or stop.
- TP1 (the nearest half-area edge) is about 6.5–7.25 points on every timeframe, because it comes from map spacing, not volatility.
- The stop (sweep extreme + 2 ticks) grows with bar size: about 5 points on 3m, 15 points on 2h.
- On 15m and above, the planned reward is smaller than the risk, so even a 52–61% win rate only breaks even or loses.
- On 3m/5m the ratio is near 1, and the low win rate (35–37%) is the remaining problem.

## The single change in v4: a minimum reward:risk filter
- **Rule:** skip a setup unless |target − reference| ≥ `v4MinRR` × |reference − frozen stop|.
  - Default 1.0. Setting 0 restores v3 behavior.
  - The reference is the signal close (market mode) or the reclaimed level (retest mode).
  - The target is the one actually traded (TP1 by default).
  - All values are frozen at the signal. Skipped setups are counted in the on-chart table.
- **Why this rule:**
  - It addresses the only consistent cause across all five timeframes.
  - It is not tuned: 1.0 is the natural break-even line, and I did not search for an optimal value.
  - It does not change entries, exits or levels.
- **Rejected alternatives:**
  - RTH-only: inconsistent sign across timeframes.
  - Close-only on opposite signal: too few such trades.
  - Weight ≥ 4 or established-only: can't be tested because the CSV has no boundary info.
- **Entry comments** now carry: `L | <boundary name> • w<weight> • DEVELOPING/established [• PROVISIONAL box] | D: … • U: … | RR x.xx`. Each trade's boundary is then attributable on the next export.

## Expected effect (hypothesis, not tested)
- Many fewer trades on 15m and above, and fewer on 3m/5m.
- Average loss should fall toward or below the average win.
- The win rate may also drop. PF > 1 is not assured, especially on 3m/5m, where the ratio was already about 1 and the win rate is the issue.

## Next run
- Re-run the same settings with v4MinRR at 1.0, plus 0 as a control.
- Export the trade lists, then attribute results by boundary weight and developing flag using the entry comments.
- Then consider an established-only / weight ≥ 4 rule as the next single change.
- Don't optimize v4MinRR on these same dates.
