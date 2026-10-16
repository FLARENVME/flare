# FLARE v3: adjacent mapped-level boxes

**Files** (source checks only; v3 has NOT been compiled or backtested by me):
- working/FLARE_v3_adjacent.pine: indicator built from v1.
- working/FLARE_v3_strategy.pine: strategy built from v2.
- Diffs: working/CHANGES_v3_vs_v1.diff and working/CHANGES_v3strat_vs_v2.diff.
- The generator script (make_v3.py) applies the identical box patch to both files.
- Original, v1 and v2 are unchanged.

## How boxes are built now
The setting **Box construction** chooses between "Adjacent mapped levels (v3)" (the default) and "Original named-range midpoint" (the old path, untouched).

1. **Collect.** Take every enabled Spaceman calendar level from the existing map: 4H, Daily, Monday H/L/Mid/Open, Weekly, Monthly, Quarterly, Yearly, and FX sessions if enabled.
   - The derived structure-box centers (slots ≥ 37) are excluded. Only real calendar references are boundaries.
   - Your level toggles therefore decide which boundaries exist.
2. **Sort and merge.** Sort the levels with `array.sort_indices`.
   - Levels within half a tick of each other become one boundary with combined names ("PMH / PWH").
   - The merged boundary takes the higher weight.
   - It counts as developing only if every member is developing.
3. **Identity per boundary.**
   - **Name.**
   - **Weight** (a hypothesis, only exposed, not used to filter): Yearly 7, Quarterly 6, Monthly 5, Weekly 4, Monday 3, Daily 2, 4H/sessions 1.
   - **Developing flag:** Monday H/L/Mid during the CME Monday trading day (`time_tradingday`, so Sunday evening counts as Monday), and the current-year H/L/Mid.
4. **Boxes.** A box is the space between two adjacent boundaries.
   - If either endpoint is developing, the box is drawn grey and dashed and tagged **PROVISIONAL**. It is not an established weekly box.
5. **Reaction areas.** For every interior boundary L with neighbors D < L < U:
   - lower half-area = (D+L)/2 .. L
   - upper half-area = L .. (L+U)/2
   - Each side uses its own spacing. The lowest and highest boundaries have only one neighbor, so they are not signal boundaries.
6. **Reuse of the signal engine.** Each (D, L, U) is pushed as a (lo, center, hi) triple into the existing arrays (`f_v3Hierarchy`). The engine's existing yellow-half math, avg(lo,center)..center and center..avg(center,hi), therefore gives exactly the v3 areas.
7. **Top-down display.**
   - Charts of 15m or less: only the nearest N boxes above and below price (default 2).
   - Larger charts: N = 3, and boxes and half-areas whose boundaries all weigh below the emphasis threshold (default 4, Weekly) are dimmed further.
   - Fills are 97–99% transparent; labels are tiny.
   - The objects are rebuilt on the last bar and the old ones deleted.

## Worked example
Weekly Open WO = 5100 (weight 4) is the boundary below price, and Previous Month High PMH = 5200 (weight 5) is the boundary above. Assume no other levels lie between them, and PWL = 5000 sits below WO.
- **Box** WO→PMH covers 5100..5200, between a weekly and a monthly endpoint. Both are established, so the box is established.
- **Areas around WO** (D = PWL 5000, U = PMH 5200):
  - lower = 5050..5100
  - upper = 5100..5150
- **Areas around PMH** (D = WO 5100, U = the next level above, for example 5300):
  - lower = 5150..5200
  - upper = 5200..5250
- **If price sits at 5160:**
  - It is inside PMH's lower half-area. The status label shows "Approaching PMH • inside its lower half-area".
  - PMH is a watch target, not a guaranteed target.
- **Long setup:** a closed candle trades below WO 5100 (or below WO's half-area edge 5050) and closes back above it, giving EARLY L. A later close above the frozen warning-candle high gives L.
- **v3 strategy targets for that long:**
  - TP1 = nearest half-area edge = 5150, the midpoint between WO and PMH.
  - TP2 = next boundary = PMH 5200.
  - TP3 = the boundary after that.
- **If it is Monday:** MON-L 5080 and MON-H 5180 are developing and sit inside this range. The boxes become PWL→MON-L→WO→MON-H→PMH, and every box touching a Monday level is PROVISIONAL.
  - The toy run in geom_test_v3.txt shows WO's areas become 5090..5100 and 5100..5140.
  - With the 5105 long reference used in that run, TP1 = 5140, TP2 = MON-H 5180, TP3 = PMH 5200.
  - Monday OPEN is fixed from the first bar and treated as established.

## Signals (v1 sequence, rewired to the v3 boundaries)
- **EARLY L:** in the sweep mode, a closed candle sweeps boundary L, or the lower half-area edge (D+L)/2, and reclaims it. EARLY S is the mirror, using the upper edge.
- **L/S:** a later close beyond the frozen warning-candle high/low. Invalidation (trading beyond the frozen sweep extreme), target (U or D), box change and expiry are all checked before confirmation. One signal per setup.
- **Frozen in the setup tooltip:**
  - the boundary name, weight and "DEVELOPING / established"
  - "PROVISIONAL box" when any endpoint is developing
  - the D and U names with their dev tags
  - mode, warning time, trigger level and invalidation level
- **Alerts:** the 4 alerts (Pre-Alert Long/Short, Confirmed Long/Short) and X are unchanged. "Allow signals at developing boundaries" defaults to on (the signals are tagged).

## State labels (tiny, closed bars, bounded marker pool)
They come from the existing per-level test tracker:
- **HOLD:** wick through the level, close back above.
- **REJ:** wick through the level, close back below.
- **BRK:** close through the level.
- **FAIL-BRK:** a BRK followed within 6 bars by a close back to the original side.
- **NR*n* (failed to reach):** counts confirmed pivots (`ta.pivothigh/low`, published only after the right-side bars) that stall inside the current box short of the nearest boundary.
  - It counts only pivots past `v3PushPct` (default 25%) of the box toward that boundary.
  - The marker appears after `v3FailN` (default 3) such pushes.
  - The count resets when the boundary is touched or the boundary changes.
  - No reversal is assumed.
- Spaceman level labels on developing levels get " · DEV" and are drawn dimmer.

## Counts and checks (static_check_v3.txt; source checks only)
- **Brackets / indentation:** parentheses and brackets balance; indentation is clean in both files.
- **Plots:** 4 of 64 in both.
- **`request.security`:** the same 2 calls as v1.
- **Offsets:** no negative offsets.
- **Labels:** markers sit in the existing bounded pool (≤ 90). Level labels number about 67 at most, plus 1 status label.
- **Boxes:** on the last bar, at most 2N box outlines plus 2(2N+1) half-areas, so ≤ 38 at N = 6.
- **Lines:** about 67 level lines plus quartiles, plus up to about 104 strategy lines in the strategy build.
- All of these are well under 500.

## Risks and open questions
- **FX sessions:** they are not tagged developing while live (they are off by default).
- **Moving neighbors:** developing Monday H/L or CYH/CYL can move D or U, which cancels a live setup ("box changed"). This is intended, but it can reduce signals on Mondays.
- **Very close levels:** levels less than 2 ticks apart are skipped as boundaries, but dense maps still create many narrow boxes, with many HOLD/REJ labels and short TP1 distances. The minimum target distance input still applies in the strategy.
- **Pine warnings:** functions that use `close[1]` are called inside loops, as in the original. I expect consistency warnings, not errors; this needs a TradingView compile to confirm.
- **NR timing:** pivots appear `boxPivotBars` bars late. A push made before the boundary changed can still count once.
- **Weight:** shown only, no filtering. Its usefulness has not been tested.
- **Confirmation needed:** a TradingView compile of both v3 files, and the ES 5m measurement plan from RESEARCH_v2.md run on v3 vs v2.
