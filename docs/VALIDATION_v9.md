# VALIDATION v9: TradingView CSVs (ES, 3m / 5m)

- **Script:** v9_analysis/val.py. Output: v9_analysis/val_out.txt.
- **Halves:** split by date midpoint (5m: 2026-09-19; 3m: 2026-09-29).
- **Bootstrap:** 5,000 resamples over positions.
- **Positions vs fills:** TradingView lists each exit fill as its own "trade". C/D/E positions are 2 contracts, with the scalp and runner legs listed separately. All stats below are per POSITION, so your headline trade counts (134/130) are fills, not positions.

## Per config
| Cfg | Positions (fills) | Net $ | Net $ per contract | PF | H1 n / PF | H2 n / PF | P(PF>1) | PF 5th pct |
|---|---|---|---|---|---|---|---|---|
| 5m A | 72 (72) | 1,865 | 1,865 | 1.10 | 38 / 0.88 | 34 / 1.34 | 0.64 | 0.66 |
| 5m B | 29 | −332 | −332 | 0.96 | 16 / 0.90 | 13 / 1.01 | 0.45 | 0.38 |
| **5m C** | 68 (134) | 10,370 | 5,185 | 1.31 | 36 / 1.04 | 32 / 1.60 | 0.78 | 0.75 |
| 5m D | 28 (56) | 482 | 241 | 1.03 | 16 / 1.27 | 12 / 0.79 | 0.49 | 0.40 |
| 5m E | 76 (152) | −9,935 | −4,968 | 0.63 | 39 / 0.61 | 37 / 0.65 | 0.10 | 0.31 |
| 3m A | 74 | 4,242 | 4,242 | 1.25 | 27 / 1.55 | 47 / 1.08 | 0.78 | 0.77 |
| 3m B | 31 | 4,920 | 4,920 | 1.83 | 12 / 1.34 | 19 / 2.28 | 0.93 | 0.94 |
| **3m C** | 66 (130) | 17,302 | 8,651 | 1.56 | 27 / 2.02 | 39 / 1.25 | 0.90 | 0.87 |
| 3m D | 29 (58) | 14,072 | 7,036 | 2.29 | 14 / 1.45 | 15 / 3.50 | 0.96 | 1.08 |

- PF > 1 in both halves: A 3m, B 3m, C 3m, C 5m (barely, 1.04), D 3m.
- Only 5m A (38 / 34) and 5m C (36 / 32) have 30 or more positions in each half. Of those, only C 5m is above PF 1 in both halves.
- D 3m is the only config whose 5th-percentile PF is above 1, but it has only 29 positions.

## Scalp vs runner legs (net $)
| Cfg | Scalp leg: net / PF | Runner leg: net / PF |
|---|---|---|
| 5m C | 3,788 / 1.22 | 6,582 / 1.39 |
| 3m C | 2,948 / 1.19 | 14,355 / 1.94 |
| 3m D | 4,155 / 1.76 | 9,918 / 2.78 |
| 5m D | 148 / 1.02 | 335 / 1.04 |

- **The runner earns most of the money.** The scalp leg is only slightly positive.
- **Leg assignment is approximate:** exits labelled "scalp" go to the scalp leg. When both legs were stopped, the fills were split in order; this doesn't matter because both legs lose the same amount.
- **Stops dominate the exits:** C 5m had 86 stop / 23 scalp / 14 runner / 8 BE fills.

## Does C beat A through more trades or better exits?
- **Trade count is not the reason:** C has the same number of positions as A or fewer (5m 68 vs 72; 3m 66 vs 74). Re-entries are not the source.
- **Per contract, C is better:** $5,185 vs $1,865 on 5m, and $8,651 vs $4,242 on 3m.
- **So the gain comes from exits:** the scalp locks in some profit, and the runner reaches the next boundary on the trades that work.
- **Caveat:** about half of C's headline net is simply from trading 2 contracts.

## Memory field on C (from entry comments; held% = H / (H + B))
| Bucket | 3m C: n / PF | 5m C: n / PF |
|---|---|---|
| held% < 33 | 5 / 0.00 | 11 / 0.96 |
| 33–50 | 8 / 0.55 | 14 / 0.73 |
| 50–66 | 19 / 0.72 | 22 / 1.56 |
| ≥ 66 | 20 / 3.71 | 15 / 0.95 |
| ≥ 60 | 29 / 2.74 (H1 2.74, H2 2.75) | 20 / 0.80 (H1 0.09, H2 1.17) |
| ≥ 50 | 39 / 1.80 (H1 1.52, H2 2.03) | 37 / 1.29 (H1 1.11, H2 1.42) |
| No memory field | 14 / 2.76 | 6 / 4.24 |
| last HOLD | 19 / 2.22 | 16 / 0.26 |
| last BEAR BRK | 13 / 0.53 | 22 / 0.98 |
| last BULL BRK | 16 / 0.93 | 15 / 2.53 |

- **Held% ≥ 50 is the only threshold positive in both halves on both timeframes:** 3m 1.52 / 2.03, 5m 1.11 / 1.42.
  - It keeps about 55–60% of positions and raises PF from 1.56 to 1.80 on 3m and from 1.31 to 1.29 on 5m, so it adds essentially nothing on 5m.
- **Held% ≥ 60–66 looks excellent on 3m** (PF 2.7–3.7) **but is negative on 5m.** That is unstable: n ≤ 17 per half.
- **last=HOLD contradicts across timeframes:** PF 2.22 on 3m vs 0.26 on 5m.

**Verdict:** held% ≥ 50 is a plausible mild filter, and higher thresholds are probably overfit. Subgroups are about 10–20 per half, so none meet the 30+ per half rule.

## Changes made in v10 (default off)
- Input "Min level held %" (default 0 = off). It uses holds / (holds + breaks) from the tracker, read from the bar before the sweep. A level with no history passes.
- Held % shown in the signal tooltip ("held NN%") and in the entry comment ("h%NN").

**Suggested TradingView runs:** C config with Min held % = 50 on 3m and 5m, checking per-half results.

# v10: Min level held % = 50 (H) vs C, TradingView CSVs
- **Script:** v9_analysis/v10.py.
- **Stats are per position.** Halves split by date midpoint (5m: 2026-09-19; 3m: 2026-09-29).

| | Positions (fills) | Net $ | PF | H1 n / PF / $ | H2 n / PF / $ | P(PF>1) | PF 5th pct |
|---|---|---|---|---|---|---|---|
| 5m C | 68 (134) | 10,370 | 1.31 | 36 / 1.04 / 640 | 32 / 1.60 / 9,730 | 0.78 | 0.75 |
| 5m H | 47 (92) | 16,430 | 1.71 | 21 / 1.27 / 2,565 | 26 / 2.03 / 13,865 | 0.92 | 0.90 |
| 3m C | 66 (130) | 17,302 | 1.56 | 27 / 2.02 / 12,668 | 39 / 1.25 / 4,635 | 0.90 | 0.87 |
| 3m H | 55 (108) | 21,700 | 1.88 | 23 / 2.19 / 13,032 | 32 / 1.64 / 8,668 | 0.95 | 1.02 |

## Positions H removed from C, and positions new in H
| | Removed from C: n / net $ (H1, H2) | New in H (not in C): n / net $ |
|---|---|---|
| 5m | 26 / −1,185 (H1 **+792**, H2 −1,978) | 5 / +2,338 (H1 +2,718) |
| 3m | 13 / −5,818 (H1 −1,450, H2 −4,368) | 2 / −1,420 |

- **5m:** the filter removed net winners in H1. All of H's H1 improvement comes from 5 *new* trades, which became possible because skipped setups freed the position slot (path dependence, not the filter's own judgment).
- **3m:** the removed trades lost money in both halves (PF 0.25). The filter genuinely helps on 3m.

## Why the offline v9 bucketing said "no difference" on 5m and TradingView shows a big gain
1. **Different handling of levels with no history.** My v9 bucket "held% ≥ 0.5" dropped positions with no history (H + B = 0). The Pine filter lets them through. On 5m C those 6 positions had PF 4.24 (+$6,665), and they explain most of the gap: the C-CSV simulation with no-history passing gives PF 1.57 (43 positions) vs 1.29 before.
2. **Path dependence.** H is a full re-run, so skipping a trade frees the position slot and lets later setups fill. On 5m that produced 5 new trades worth +$2,338. A CSV filter cannot see those.
3. **Rounding:** the comment's h% is rounded, so exactly 50% is treated the same either way. This is a minor effect.

## Threshold sensitivity
Simulated by filtering the C CSV entry comments (h%NN). No-history positions pass. No path effects.

| Threshold | 5m: n / PF / H1 PF / H2 PF | 3m: n / PF / H1 PF / H2 PF |
|---|---|---|
| 40 | 51 / 1.37 / 0.85 / 1.89 | 60 / 1.78 / 2.19 / 1.48 |
| 45 | 47 / 1.49 / 0.90 / 2.05 | 58 / 1.81 / 2.10 / 1.57 |
| 50 | 43 / 1.57 / 0.98 / 2.02 | 53 / 2.00 / 2.43 / 1.68 |
| 55 | 30 / 1.18 / 0.16 / 1.68 | 47 / 2.80 / 3.87 / 2.16 |
| 60 | 26 / 1.31 / 0.16 / 2.08 | 43 / 2.75 / 3.87 / 2.03 |

- **3m:** smooth and monotonic. Every threshold from 40 to 60 improves both halves, so it is not a knife edge.
- **5m:** H1 stays at or below 1 for every threshold in the filter-only simulation, and it collapses at 55 and above. The TradingView H1 PF of 1.27 depends on the new trades. The 5m result is fragile.

## Verdict
- **3m:** Min held % = 50 is a credible improvement. It holds in both halves, the removed trades were losers in both halves, the threshold plateau runs from 40 to 60, and the bootstrap 5th-percentile PF is 1.02.
  - Sample is still small: 23 / 32 positions per half, under the 30+ rule in H1.
- **5m:** not confirmed. The headline gain rests on H2 plus path-dependent new trades, and H1 does not improve from the filter itself.
- **Recommendation:**
  - Use 50 on 3m (or 45–50 to stay off the edge).
  - Keep it optional on 5m.
  - Re-validate on more history (earlier months, or NQ1!) before trusting it.
