# DNF trigger test (offline, Yahoo ES=F / NQ=F 5m)

Code: `dnf_test/dnf.py` (imports `offline_v9/sim2.py`, which is unchanged). Raw output: `dnf_test/out.txt`. Nothing in `working/` was touched.

## Method
- **Data:** Yahoo 5m bars, about 2026-08-05 to 2026-10-15 PT. Each market is split in half by bar index, at about 2026-09-10/11 PT (the same split ideas.py uses).
- **Levels:** sim2's mapped levels (DO, PD H/L/M, WO, PW H/L/M, MO, PM H/L/M) and sim2's "hold" setup detection, both unchanged. A setup stays live for 12 bars, or until its sweep extreme is taken out. This is the same as the baseline.
- **Baseline:** `sim2.run(M,'mss','half')`, the structure-break confirm. It enters at the next bar's open and puts the stop at the sweep extreme ±2 ticks. Its numbers match `ideas_out.txt` BASE exactly.
- **DNF trigger:** CM MacD is EMA(2) minus EMA(7), with an SMA(9) signal line. A trade needs a cross on the bar's close, plus Stoch(13,3,3) %K ≤20 for longs or ≥80 for shorts on that same closed bar.
- **10m/15m alignment:** I build 10m and 15m bars from the 5m data, using epoch-aligned buckets. Each timeframe tracks the direction of its last trigger, the same way the Pine `_state` does. A 10m or 15m bar only counts once it has fully closed by the 5m bar's close, so there is no lookahead. Longs need both states at +1; shorts need both at −1.
- **DNF entry:** the trigger has to fire, in the setup's direction, while a hold setup at that level is live. Entry is the next bar's open, which is about the trigger close. The stop is 1 tick beyond the trigger candle's body (body low for longs, body high for shorts).
- **Exits (same for both triggers):** 1 contract scalps at half-way to the nearest mapped level that is at least 4 ticks away. The second contract runs to that level. After the scalp fills, the runner's stop moves to breakeven plus 1 tick. If a bar touches both stop and target, the stop is assumed to fill first. Only one position is open at a time.
- **Costs:** $2.50 per side per contract ($5 round trip). 1 tick of slippage on the entry and on stop exits. Net $ is per 2-contract position.
- **Meaningful:** at least 30 trades in each half.

## Assumptions / deviations
- I used the trigger exactly as specified. The original Pine is looser: it also requires the signal line below 0 for longs (above 0 for shorts), and it accepts a %K extreme from the prior bar, from %D, or within an 8-bar lookback. The regime gate and the cooldown are not applied.
- "Near a mapped level" means a live sim2 hold setup at that level. I did not use a distance threshold.
- Yahoo continuous futures are only an approximation of the TradingView data.

## Results
| Market / trigger / half | Trades | Win% | PF | Net $ | Max DD $ |
|---|---|---|---|---|---|
| ES Structure-break H1 | 89 | 43% | 0.69 | -13,259 | 17,914 |
| ES Structure-break H2 | 97 | 52% | 1.10 | 3,624 | 8,824 |
| ES Structure-break All | 186 | 47% | 0.88 | -9,635 | 17,914 |
| ES DNF H1 | 3 | 33% | 0.33 | -349 | 520 |
| ES DNF H2 | 9 | 0% | 0.00 | -2,965 | 2,965 |
| ES DNF All | 12 | 8% | 0.05 | -3,314 | 3,314 |
| NQ Structure-break H1 | 94 | 53% | 0.68 | -30,839 | 38,865 |
| NQ Structure-break H2 | 100 | 58% | 0.77 | -20,971 | 23,179 |
| NQ Structure-break All | 194 | 56% | 0.72 | -51,810 | 51,920 |
| NQ DNF H1 | 6 | 33% | 3.41 | 3,209 | 1,020 |
| NQ DNF H2 | 13 | 38% | 0.54 | -3,605 | 6,630 |
| NQ DNF All | 19 | 37% | 0.96 | -396 | 6,630 |

Sensitivity check (not in the table): there are 688 raw 5m triggers on ES and 709 on NQ. The bottleneck is requiring a trigger, alignment and a level setup at the same time. Even with the setup window widened to 36 bars, there are only 16 ES and 23 NQ trades in total.

## Verdict
**Not enough data. The DNF trigger can't be judged from this.** It produced 3/9 trades by half on ES and 6/13 on NQ, far below 30 per half. Taken as anecdote only, ES is clearly negative (1 winner in 12) and NQ is roughly flat (PF 0.96, −$396). There is no sign of an edge. The structure-break baseline does have enough trades in both halves (about 90–100 each). But on this Yahoo sample it loses money on NQ in both halves (PF 0.68 / 0.77) and on ES in H1 (PF 0.69), with only ES H2 above 1 (PF 1.10). So it fails the both-halves PF>1 test too. Neither trigger is supported. Don't add DNF to v10 as an alternate entry on this evidence. To test it properly would need much more history, or a looser level-proximity rule, which would be a different hypothesis.
