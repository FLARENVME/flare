# FLARE v17 (from v16): live-execution aids

v16 and the originals are untouched. Full diff: `../CHANGES_v17_vs_v16.diff`. No trading logic changed: the entry and exit
prices, quantities and conditions are the same as v16. Only the order/exit **comment strings** changed, and no logic reads them except the two parsers covered below.

## Added (inputs group "v17 • Live trade panel / alerts")
1. **LIVE TRADE table**, top-right, `LIVE TRADE table` input ON by default, text size Large (Normal/Large/Huge).
   Rows show STATE (FLAT / PENDING LONG/SHORT / LONG / SHORT), ENTRY (average fill, or the limit/ref price while pending),
   STOP (the active stop of the remaining legs, after BE/partial-BE/trail), TP1 (marked "✓ filled" once filled),
   TP2/runner (plus TP3 in ladder mode), CONTRACTS (x of N), BARS IN TRADE, the latest PRE-ALERT (side, turn level and invalidation level, from the
   same gated pre-alerts that draw the v15 triangles), the pre-alert time and the last event message. All prices use `format.mintick`.
2. **alert() calls**, `alert.freq_once_per_bar_close`, on by default. To use them, create one alert with the condition "alert() function calls only". Messages:
   - `FLARE ES ORDER SHORT 2 MKT next open (ref 7694.50) SL 7706.50 TP1 7680.00 TP2 7660.00`: fires on the signal bar close, so it arrives at the same moment the strategy's own market order goes in (or `LMT @x` for retest/retrace).
   - `FLARE ES ENTRY SHORT 2 @7694.50 SL 7706.50 TP1 7680.00 TP2 7660.00`: fires on the close of the fill bar, with the exact average fill.
   - `FLARE ES TP1 SHORT 1 @7680.00 REMAIN 1 SL … TP2 … | <exit comment> | PnL …`
   - `FLARE ES STOP SHORT 1 SL 7694.75 (was 7706.50)`: the stop moved (BE / partial-BE / trail).
   - `FLARE ES EXIT SHORT 1 @… FLAT | <exit comment> | PnL …`
   - `FLARE ES CANCEL unfilled order`. Optional, default OFF: `FLARE ES PRE SHORT turn … inv …`.
3. **Comments**: the entry comment now starts with `SHORT 2 ref X SL Y TP1 Z TP2 W ||`, followed by the original text. The levels come first so the 240-char cap cannot cut them.
   Each exit leg's comment_profit and comment_loss now carries its price (e.g. `TP1 7680.00`, `stop SL 7706.50`, `scalp TP1 …`, `runner TP2 …`).
   These comments are re-issued every bar, so the List of trades shows the stop that was actually in force.
   - The Clean-mode exit-tag parser now uses `str.startswith` for "scalp" and "runner", because those comments are no longer exact matches. The other checks (`str.contains` "stop"/"BE"/"TP"/"1R", `== "TIME"`) and the v8 side-guard `str.contains(...,"stop")` still behave as before.
4. **Plots**: 3 `plot.style_stepline` lines (STOP pink, TP1 green until filled, TP2/runner cyan). They are drawn only while a position is open; otherwise the value and color are `na`.
   Toggle: `Plot stop / TP lines while a trade is open`. Plot count goes from 4 to 7 (limit 64).
5. Titles changed to `FLARE_NvME v17 | Live trade panel + alerts` / `FLARE v17` (shorttitle is 9 characters).

## Checks run
- `static_check.py`: parentheses and brackets balanced, no indent issues, plots 7, neg_offset 0, lookahead_on 10 (the same 10 as v16; every one
  is on a `[1]` / completed-HTF expression; nothing new added).
- `static_check2.py`: shorttitle 'FLARE v17' (9 chars) OK; use-before-declare: none.
- Manual: no new label/line drawn into old bars (the only new drawing is a table on the last bar); no tabs; all new `var` state is declared at the top (lines ~27-45).

## Not verified
- **Not compiled in TradingView.** Points to check: the `table.cell` text_halign args, `table.merge_cells`, and `force_overlay` on `plot`.
- Entry, TP1, stop and exit alerts are detected on bar close from `strategy.position_size` / `closedtrades`. For a market entry the
  ENTRY alert therefore comes one bar after the ORDER alert (the strategy itself fills at the next open). Mirror on ORDER, confirm on ENTRY.
- If a fill and its exit happen on the same bar, there is no ENTRY alert, only EXIT (with the trade's exit comment). There is no ORDER alert when the order is placed while still in an opposite position (Reverse mode); the ENTRY alert covers that case.
- Alerts and the table reflect the strategy's broker emulator, not a real broker. Paper Trading fills will differ by slippage.
