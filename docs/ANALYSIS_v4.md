# FLARE v4 (R:R ≥ 1.0): attribution and the v6 decision

**Inputs:**
- v4 trade-list CSVs with entry comments, and the v3 CSVs.
- Scripts: v4_analysis/attr.py, cmp.py and the inline sims. Outputs in v4_analysis/*.txt.
- Halves are split chronologically by trade count per timeframe.

**Timezone:** inferred, not confirmed. Sunday entries appear from 19:30 on. RTH-family exits cluster at 06:30 and 12:00–13:00, which fits PT and the CME 06:30 PT cash open. Confirm in the chart settings.

**Comment prefix bug:** v4 entry comments start with the previous trade's direction ("S | …" on a long). The boundary, weight, developing and R:R fields are correct. Fixed in v6.

## 1. Attribution (PF, 1st half / 2nd half; groups with fewer than 30 trades are marked *)
| Group | 3m | 5m | 15m | 30m | 2h |
|---|---|---|---|---|---|
| ALL | 0.91 / 0.97 | 0.72 / 0.87 | 0.47 / 1.19 | 0.77 / 0.66 | 1.43 / 0.84* |
| Daily (w2) | 0.45* / 1.06* | 0.60* / 2.64* | 0.31* / 1.29* | 0.90 / 1.02 | 1.17* / 0.44* |
| Monday (w3) | 1.66* / 1.17 | 1.17* / 0.52 | 0.70* / 1.61* | 0.58 / 0.96 | n/a* |
| Weekly (w4) | 1.11* / 0.90* | 0.60* / 0.79* | 0.56* / 1.19* | 0.73* / 0.42* | n/a* |
| Monthly (w5) | 0.20* / 0.51* | 0.78* / 1.08* | 0.14* / 0.26* | 0.71* / 0.18* | n/a* |
| Weight ≥ 4 combined | worse than ALL on 3m–30m (Weekly and Monthly rows) | | | | |
| Established | 0.71 / 1.03 | 0.62 / 0.99 | 0.46 / 1.26 | 0.83 / 0.53 | 1.36 / 0.72* |
| Developing / PROVISIONAL | 2.74* / 0.19* | 1.96* / 0.00* | 0.58* / 0.78* | 0.47* / 2.68* | small |
| R:R 1–1.5 | 0.86* / 0.72* | 0.86* / 0.79* | 0.25 / 0.67* | 0.60 / 0.68 | small |
| R:R 4+ | 1.65* / 1.08* | 1.02* / 0.73* | 0.00* / 2.54* | 0.00* / 0.40* | 0.00* |
| RTH 06:30–13:00 | 0.95* / 0.67 | 0.24* / 0.77* | 0.45* / 2.36* | 0.58* / 1.18* | small |
| Overnight | 0.88 / 1.36 | 1.23 / 0.98 | 0.48 / 0.88 | 0.85 / 0.55 | 1.76* / 0.43* |
| Shorts | 0.67 / 1.14 | 0.46 / 0.87 | 0.45 / 1.40 | 0.52 / 0.55 | 1.55* / 1.55* |

*The family rows use the weight field (w2 = Daily, w3 = Monday, w4 = Weekly, w5 = Monthly), which is authoritative. The name-based family column in attr_out.txt mislabels MON-* levels as Monthly (a substring bug), so ignore that column.*

**Result:** no boundary family, weight, developing flag, R:R bucket, session or side is better than the baseline in both halves on most timeframes with 30 or more trades.
- Weight ≥ 4 established-only, filter (d), is unsupported: Monthly w5 is the worst group almost everywhere.
- The session filter flips sign between halves and timeframes.
- VWAP, RVOL and divergence can't be attributed from these CSVs (the values were not logged). They stay untested candidates.

## 2. Did the R:R filter mainly remove winners? No.
v3 trades with no matching v4 entry (same time and side):

| TF | Removed | Removed net | Removed PF (1st / 2nd) | v3 kept, PF |
|---|---|---|---|---|
| 3m | 55 | −4,525 | 0.85 / 0.35 | 157, 0.91 |
| 5m | 69 | −2,408 | 0.71 / 0.83 | 135, 0.79 |
| 15m | 135 | −6,725 | 0.71 / 0.99 | 109, 0.78 |
| 30m | 276 | −9,630 | 0.78 / 1.00 | 188, 0.80 |
| 2h | 119 | −7,770 | 0.59 / 0.99 | 46, 1.21 |

- The removed trades had a high win rate (52–70%) but were net losers.
- The trades that remained have about a 30% win rate, below what their planned R:R needs.
- v4's new-only trades (path changes after skips) were also losers.

## 3. Exit path, the consistent finding
Stopped-out trades that first had open profit of at least 1R (R = |loss| − $5 commission):

| TF | 1st half | 2nd half |
|---|---|---|
| 3m | 17% | 19% |
| 5m | 23% | 26% |
| 15m | 16% | 36% |
| 30m | 17% | 22% |
| 2h | 22% | 22% |

Estimated effect of breakeven at +1R: those stops become −$17.50 (commission plus 1 tick); everything else unchanged.

| TF | v4 PF → BE@1R PF, 1st half | 2nd half |
|---|---|---|
| 3m | 0.91 → 1.06 | 0.97 → 1.13 |
| 5m | 0.72 → 0.86 | 0.87 → 1.10 |
| 15m | 0.47 → 0.56 | 1.19 → 1.82 |
| 30m | 0.77 → 0.91 | 0.66 → 0.82 |
| 2h | 1.43 → 2.03 | 0.84 → 1.03 |

- It improves every timeframe in both halves, and each half has 32–116 trades.
- **Optimism caveats (upper bound):**
  - It assumes the breakeven moves at the moment +1R is touched. v6 moves it only after the bar closes.
  - It ignores current TP1 winners that would retrace to entry after +1R; those can't be seen in the CSV.
- **Contrast:** simply capping the target at 1R hurt 3m and 5m (0.91 → 0.64 and 0.72 → 0.55 in the 1st half), so it was rejected.

## 4. Decision for v6: breakeven after +1R
- **Rule:** once a closed bar has reached entry ± 1.0 × R (R = |fill − frozen stop|), the stop moves to entry + 1 tick (shorts mirrored), effective from the next bar.
- **Settings:** `Breakeven after +k R` default ON, k = 1.0, offset 1 tick. All v5 filters stay OFF and v4MinRR stays 1.0.
- **Also fixed:** the entry-comment prefix bug.
- **Why this and not a filter:**
  - It is the only change that is consistent across all five timeframes and both halves.
  - It is not tuned: 1R is the natural first threshold.
  - It changes only exits.
  - No filter attribution passed the consistency test.
- **Expected effect (hypothesis):**
  - Fewer full stop-outs and more small scratches tagged "BE" in the trade list.
  - A small number of TP1 winners turn into scratches.
  - PF improves by less than the upper bound above. PF > 1 is not assured, especially on 30m and the 1st half of 15m.
- **Next run:** v6 vs v6 with the breakeven off (= v4), same settings and dates.
  - Report BE exits as a count.
  - Report winners lost to BE.
  - Report the PF split by halves.

**Static checks:** parentheses and brackets balance, indentation is clean, 4 of 64 plots, the same 2 `request.security` calls, no negative offsets.
- Diff: working/CHANGES_v6_vs_v5.diff (92 lines). v5 is unchanged.
