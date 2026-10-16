# NQ diagnosis (v10, TradingView CSVs + offline NQ=F 5m)
- **Scripts:** v9_analysis/nqdiag.py (CSV analysis), offline_v9/sim3.py and nqstop.py (offline tests). Output: offline_v9/nqstop_out.txt.
- **CSV stats are per position.**
- **Points are taken from the CSV fills.** Stop distance = |entry − stop fill|. MFE/MAE = TradingView excursion $ ÷ (qty × point value).

## Stops, MAE / MFE: NQ vs ES
| | PF | Win % | Both legs stopped | Median stop | Stopped ≤ 5 bars | Losers' median MFE | Losers that reached ≥ 1R first | Winners' median MAE |
|---|---|---|---|---|---|---|---|---|
| ES C 5m | 1.31 | 35 | 63% | 6.5 pt | 26% | 3.0 pt (0.46R) | 11 / 43 | 2.3 pt |
| ES H 3m | 1.88 | 42 | 55% | 6.75 pt | 40% | 2.2 pt | 3 / 30 | 2.5 pt |
| NQ C 5m | 1.00 | 30 | 70% | 30.75 pt | 35% | 21.9 pt (0.71R) | **17 / 49** | 9.1 pt |
| NQ H 5m | 1.08 | 30 | 70% | 30.5 pt | 36% | 26.6 pt | 10 / 28 | 10.9 pt |
| NQ C 3m | 0.83 | 17 | 83% | 27.5 pt | 40% | 15.1 pt | 17 / 48 | 16.1 pt |
| NQ H 3m | 0.46 | 9 | 89% | 25.75 pt | 44% | 15.1 pt | 14 / 39 | 16.1 pt |

## Stops in ATR terms (offline 5m ATR14 median: NQ 20.7 pt, ES 3.2 pt)
- **NQ stops are about 1.5 ATR, ES stops about 2 ATR.** So NQ stops are not unusually tight. The proportion stopped within 5 bars is similar on both (35–44% vs 26–45%), so pure noise stop-outs are not the main difference.
- **The real difference is losing trades that were in profit first.** On NQ, about one third of full-stop losers first moved ≥ 1R in favor and then went all the way to the stop. On ES the losers barely moved favorably (median 0.3–0.46R).
- **The cause is target placement.** NQ boundaries are far apart relative to the stop, so the "half-way" scalp is often not reached. And breakeven at +1R is disabled below 15m by the v7 (a) gate (on by default).
- **NQ 3m winners take heat:** median MAE 16 pt, about 0.6R. A wider stop would not have saved many losers, and the offline test below agrees.

## Breakdowns (NQ, small n; read loosely)
**Held %:** the v10 held ≥ 50 filter hurts on NQ 3m. Held 50–66 gives PF 0.46–0.54 and held ≥ 66 gives 0.20–0.22, while held < 50 gives 1.16–1.33. This is the opposite of ES, so it is not a transferable signal.

**Level family:**
- w3 (Monday) is positive in all 4 runs (PF 1.1–2.6).
- w4 (weekly) is bad: C 0.70 / 0.10, H 0.56 / 0.14.
- w2 (daily) is mixed. Each cell has n ≤ 24.

**Time of day:** CSV times are in the chart timezone; I bucketed them as if PT.
- Overnight is the bulk: 5m PF 0.93–1.11, 3m 0.40–0.47.
- RTH open has only 2–4 trades.

## Offline tests (NQ=F 5m; a 3m test is impossible because Yahoo has no 3m bars, and 1m data covers only about 7 days)
**Baseline:** NQ PF 0.72 (0.68 / 0.77).

**Stop changes** (stop = sweep extreme ± k·ATR):
| Variant | PF all | PF 1st / 2nd half |
|---|---|---|
| k = 0.25 | 0.66 | 0.61 / 0.72 |
| k = 0.5 | 0.66 | 0.60 / 0.73 |
| k = 1.0 | 0.65 | 0.58 / 0.73 |
| Minimum stop 10 / 15 / 20 pt | ≈ 0.72 | unchanged (stops are already wider) |
| Max stop 1.5× / 2.5× ATR | worse | — |
| R:R ≥ 1 | 0.70 | — |
| R:R ≥ 1.5 | 0.53 | — |
| k = 0.5 + R:R ≥ 1.5 | 0.44 | — |

All stop variants are worse than the baseline on NQ. (On ES, k = 0.5 + R:R ≥ 1.5 = 1.03 / 1.62 with 41 / 41 trades, which passes the rule. That's the ES side, not an NQ fix.)

**Exit change** (scalp at a fixed R instead of half-way to the next boundary):
| Scalp at | NQ PF 1st / 2nd half | ES PF 1st / 2nd half |
|---|---|---|
| 0.5R | 0.54 / 0.93 | 0.70 / 0.70 |
| 0.75R | 0.84 / 1.07 | — |
| **1.0R** | **0.87 / 1.35** (all 1.07) | 0.81 / 0.51 |

The 1.0R scalp is the only NQ improvement, but it does not pass the rule. It is market-specific: it hurts ES.

## Proposal: TradingView-testable on NQ with EXISTING v10 inputs (no code needed)
The v7 (e) ATR stop is still in v10: group "v7", label **"(e) ATR stop buffer"**, inputs "k·ATR(14)" (0.25) and "skip if stop > ×ATR" (1.5). Offline it does not help NQ, so treat it as a low priority.

Suggested tests on NQ1! 5m and 3m, starting from config C (min held % = 0):
1. **Scalp at 1R:** v9 "Scalp TP1 + runner" = **Fixed R**, R = **1.0**.
2. **Breakeven at +1R on 3m/5m:** turn OFF v7 "(a) Breakeven only on chart TF ≥" so that v2 "Breakeven after +k R" (k = 1.0) works on 3m/5m. This targets the third of losers that reached ≥ 1R first.
3. Tests 1 and 2 together.
4. **(Optional) ATR stop:** v7 (e) ON with k = 0.5, plus "Minimum reward:risk" = 1.5.

**v11 code change, if any of these wins:**
- A per-symbol preset input "Market profile" = Auto / ES / NQ.
  - NQ sets the scalp to Fixed 1R, breakeven at +1R regardless of timeframe, and min held % = 0.
  - ES keeps v10 H.
- Optional "Skip weekly (w4) levels" toggle, but only if NQ TradingView results confirm w4 is bad (it looks bad on ES too in places).
- Don't build it until the existing-input tests show NQ PF > 1 in both halves.

**Verdict:** the setup currently has no edge on NQ (offline PF 0.72; TradingView 0.46–1.08). The failure mode is trades that move ≥ 1R in favor and then reverse to the stop, not stops that are too tight. Fix the exits first, or don't trade NQ.
