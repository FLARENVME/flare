# FLARE v14: Clean visuals (trading logic unchanged)
- **Built from v13.** Every diff line is visual-only; `CHANGES_v14_vs_v13.diff` contains no strategy.entry/exit/close/cancel changes.
- **Alerts are unchanged.**
- **Static checks pass:** 4 plots; labels at most about 60 pre-alerts + 3×N trade labels + map labels (limit 500); trade lines at most 4×N.

## New inputs (group "v14 • Visuals")
| Label | Default | Effect |
|---|---|---|
| Visual mode | Clean | Clean = new visuals; Full = the exact v13 visuals |
| Show levels within X ATR of price | 6 | Clean only. Map lines/labels farther than X·ATR(14) from the close are not drawn, and v3 boxes are clipped to close ± X·ATR, so the price scale is not stretched. 0 = off |
| Trade line sets to keep | 5 | Number of recent trades whose lines and tags are kept |

## Clean mode
1. **BUY / SELL** (size.normal, neon green / pink, below / above the bar): drawn only on bars where the strategy position actually opens or flips (read from strategy.position_size). The tooltip shows the entry comment.
2. **Pre-alert:** a small dim-yellow triangle with no text. The tooltip shows the full setup hint. The old "EARLY L/S", "L/S", "X", "B", HOLD/REJ/BRK/FAIL-BRK and NRn text markers (the stacking counters) are shown only in Full mode.
3. **Per-trade lines:** entry (silver), stop (pink, dashed), TP1/scalp (green, dotted), runner target (cyan, dotted).
   - They are thin, about 55% transparent, and drawn from the entry bar until the position closes. The last N sets are kept.
   - In Clean mode the scalp line uses Fixed-R or v2 TP1, matching the v9 scalp setting. The runner line follows "Runner target".
   - The old fixed 12-bar v2 bracket lines are shown only in Full mode.
4. **Exit tags:** one tiny label per exit bar, combining all legs closed on that bar. Tags are ✓ TP1 (scalp), ✓ RUN (runner), ✕ SL (stop), • BE, ⏱ TIME, ✓ TP (TP1/2/3 or 1R), • EXIT (anything else).

## Not controllable from code
- **The "+1 / −1" stacked markers are TradingView's built-in strategy order markers.** Hide them in Settings → Style → "Trades on chart" (uncheck, or uncheck "Signal labels" / "Quantity").
- **I could not render this.** Check in TradingView that:
  - the triangle and label sizes look right;
  - the clipping does not hide a level you care about (raise X).

# v15 fixes (FLARE_v15_strategy.pine; CHANGES_v15_vs_v14.diff; trading logic unchanged)
1. **Far-level filter now covers every drawing path in Clean mode:**
   - v14 already covered f_draw level lines and labels (Yearly Open, Current Year, Prev Quarter, and so on) and the v3 boxes.
   - Added: structure-wing boxes (skipped when both edges are far, otherwise clipped), wing and named-box center lines, and the active structure zone box.
   - The script has no level `plot()` calls; its 4 plots are hold/break plotshapes.
2. **EARLY L/S and X text:** the only source is f_auxMarker, and it has been gated to Full mode since v14.
   - If they still show, most likely another FLARE copy (v13, or the v1 indicator) is still on the chart, or the v14 input "Visual mode" was set to Full. Remove other FLARE instances.
3. **Pre-alert triangles (size.tiny):** shown only when the setup passes these filters, all known at warning time:
   - level memory filter;
   - Min level held %;
   - Skip strong trend month;
   - HTF bias.

   Structure-break cannot be known at warning time (it is the confirmation step), so it is not part of the pre-filter.
4. **Footer:** "FLARE v15 • simulated Strategy Tester".
5. **Per-trade lines and tags were likely garbage-collected.** In v14 they were created on historical bars. On the last bar the map recreates many lines and labels, and TradingView deletes the OLDEST objects beyond 500, which were exactly the trade drawings.
   - v15 records trade data in arrays every bar and draws the lines, BUY/SELL labels and exit tags on the last bar, after the map is rendered. They are the newest objects, so they survive. They also show for history, not only realtime.
