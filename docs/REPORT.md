# FLARE_NvME v1: two-stage signals (source-only report)

**Source:** original FLARE_original.pine, 999 lines, sha256 `ac6f7356…9a72` (full: ac6f735631e20ca73c248b0af56d27e57983fe18932527b28ea8e07a4f2b9a72).
**Working copy:** working/FLARE_v1_sweepreclaim.pine, 1020 lines, sha256 b3adef40…12bd. Diff: working/CHANGES.diff.
**Status:** I only checked the source. It has NOT been compiled in TradingView and NOT tested on historical data.

## Geometry (checked against the source, unchanged)
- Named ranges (lo, center = avg(lo, hi), hi) are built in `f_namedBox` (L326-342) and `f_hierarchy` (L343-363).
- The yellow halves are drawn at L857-861: lower = avg(lo, center)..center, upper = center..avg(center, hi). With D=lo, L=center, U=hi this is exactly (D+L)/2..L and L..(L+U)/2.
- Note: here L is the midpoint of a named range, not an arbitrary adjacent map level. The "· half N" sub-boxes (L338-341) re-narrow toward the side `close` is on, so they move with price.
- Monday range (L206-224) uses `time_tradingday`, so it includes the Sunday CME evening session and freezes once Monday is over. DAY · DO / MON-L is used only after Monday completes and is off by default (L273, L361). The plotted MON-H/L level lines still update live during Monday.

## How the signals work
| Stage | Marker | Alert (new, directional) | Rule |
|---|---|---|---|
| Pre-alert long | yellow "EARLY L" below bar | **Pre-Alert Long** | Closed candle reacts at a named box center. Freezes the setup box, the turn (warning high), the invalidation (warning low), the bar index and the time. |
| Confirmed long | green "L" below bar | **Confirmed Long** | A later closed candle closes above the frozen turn. One per setup (`setupConfirmed`). |
| Pre-alert / confirmed short | yellow "EARLY S" / pink "S" above bar | **Pre-Alert Short / Confirmed Short** | Exact mirror. |
| End | grey "X" | Box: INVALIDATED (existing) | Trading beyond the frozen sweep extreme, the box changing, or expiry (`boxExpire`, default 12 bars) before confirmation. |

- All events are set only inside `if ... barstate.isconfirmed`, so markers and alerts happen on closed bars only.
- On any candle, invalidation, target and expiry are checked before confirmation (the if/else chain in the setup engine).
- The original generic alerts (BUILDUP, CONFIRMED BULL/BEAR, EARLY WARNING, INVALIDATED, plus the structure-box alerts) are kept.
- **In TradingView, create alerts with "Once Per Bar Close".**

### Mode input "Setup / confirmation mode" (default = Original)
- **Original (unchanged logic):**
  - The pre-alert can come from a center sweep, a reclaim, or a yellow-edge rejection (`f_boxReaction`).
  - Confirmation needs a close beyond the turn and a candle body in the trade direction.
  - With "Require prior confirmed local pivot" on, the turn is the last confirmed pivot.
  - If the target is touched before confirmation, the setup is marked "RESOLVED".
- **v1 Sweep → warning-candle breakout:**
  - Pre-alert only on a sweep and reclaim: the previous close was on the support side, price traded through the center, and the candle closed back.
  - Confirmation is any later close beyond the frozen warning high/low.
  - A target touched before confirmation counts as EXPIRED (it sends an X and the INVALIDATED alert).
- The legend for EARLY L / EARLY S / L / S is in that input's tooltip. Marker tooltips now also show the mode and the warning timestamp.

## Did the sweep/reclaim candidate already exist?
Partly. The `sweep` branch at L667 matches the baseline, and freezing, invalidation-first ordering, expiry and one-signal-per-setup were already there. Gaps:
- It was mixed with the reclaim and reject triggers.
- Confirmation needed a directional candle body.
- There were no direction-specific alerts.
v1 fixes these behind the mode toggle.

## Changes (all marked `// FLARE v1 CHANGE`)
1. Added the mode input with the legend tooltip.
2. Added `f_boxSweepOnly`.
3. Added `var setupTime`, frozen when the setup is created.
4. v1 confirmation rule.
5. v1 rule for a target reached before confirmation.
6. Turn and trigger selection by mode.
7. Four directional alertconditions.

## Evidence
**Source checks I actually ran** (static_check.py, output in static_check_output.txt):
- Parentheses and brackets balance; indentation is 4 spaces (plus 5-space continuation lines).
- Plots: 4 out of a 64 limit.
- 2 `request.security` calls, 0 negative offsets; 13 alertconditions (9 → 13).
- Repaint review:
  - L154 `f_period` requests `[time, open, time[1], high[1], low[1]]` with lookahead_on when the HTF is at least the chart timeframe. Previous high/low use [1], so they are safe. Current-period open/time are known at the period start, which is acceptable but worth checking in Codex.
  - L182 uses [1] with lookahead_on, so it is safe.
  - Pivots are only used after their right-side bars confirm, and there is no backward offset.
- No TP1/TP2/TP3 definitions exist.

**TradingView compilation:** NOT DONE (no access).
**Historical testing:** NOT DONE (no data).

## Inputs not provided
- A TradingView compile.
- ES/NQ data exports.
- The six scalping_lab screenshots.
- The original full backup indicator.
- The prop-firm rules.

## Proposed test protocol
- CME ES1! and NQ1!, on 3m, 5m and 15m tested separately.
- A fixed date window, for example 2025-01-01 to 2026-06-30, with a holdout period.
- Cost model: $2.50/side commission and 1 tick slippage per side.
- Run both Original and v1 modes.
- Metrics:
  - Lead time from pre-alert to confirmation.
  - False pre-alerts (invalidated or expired).
  - Missed reversals: a move of at least X ATR from a named center with no pre-alert.
  - Confirmation delay in bars.
  - Invalidations and expirations.
  - Long/short balance.
  - Net result after costs.
  - Closed-trade drawdown vs intratrade drawdown.

## Open questions
- Should boundaries other than the center (yellow edges, lo/hi) also be able to trigger in v1?
- Should the MON-H/L lines show a "developing" tag during Monday?
- The half-box cancellations (they move with close) can kill setups. Should v1 limit setups to main ranges only?
