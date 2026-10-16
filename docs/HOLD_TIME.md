# HOLD_TIME: ES v11 3m/5m TradingView CSVs
- Script: v9_analysis/hold.py (output below).
- Capped P/L is an APPROXIMATION: open legs are exited at the Yahoo ES=F 5m close at entry + cap, with $5 commission and 1 tick slippage per contract. Positions with no Yahoo bar near the cap time are left unchanged.

```

3m: 55 positions, net $21700, PF 1.88
  hold h winners n=23 median 3.25 p80 7.30 max 15.90 | losers n=32 median 0.45 p80 1.50 max 6.70
  >1h: 26 positions, their net $29165
  >2h: 18 positions, their net $33495
  >3h: 14 positions, their net $34248
  >5h: 8 positions, their net $25920
  cap 5h: 8 positions affected (0 without Yahoo price, left as-is) -> net $11775 PF 1.48
  cap 3h: 14 positions affected (0 without Yahoo price, left as-is) -> net $9838 PF 1.41
  cap 2h: 18 positions affected (2 without Yahoo price, left as-is) -> net $8375 PF 1.37

5m: 47 positions, net $16430, PF 1.71
  hold h winners n=18 median 4.50 p80 12.17 max 28.67 | losers n=29 median 0.75 p80 3.67 max 11.00
  >1h: 30 positions, their net $23650
  >2h: 23 positions, their net $25008
  >3h: 18 positions, their net $22095
  >5h: 9 positions, their net $16522
  cap 5h: 9 positions affected (0 without Yahoo price, left as-is) -> net $13255 PF 1.68
  cap 3h: 18 positions affected (0 without Yahoo price, left as-is) -> net $15168 PF 1.85
  cap 2h: 23 positions affected (3 without Yahoo price, left as-is) -> net $9992 PF 1.64
```

**Finding:** winners hold much longer than losers (3m median 3.25 h vs 0.45 h). A 5h cap cuts 3m net from $21.7k to about $11.8k (PF 1.88 → 1.48) and 5m from $16.4k to about $13.3k (PF 1.71 → 1.68).
