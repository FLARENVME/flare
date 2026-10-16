# FLARE: product and YouTube launch plan
_By Erick Escareno. Drafted Oct 15, 2026 (PT). Internal planning doc, not marketing copy, and not legal advice._

> **Validation comes first.** FLARE is **not proven profitable**. Nothing gets sold, and no performance statement gets made anywhere (YouTube, TradingView, Discord, X, landing page), until the launch gates in §1 pass. Even after they pass, marketing describes **what the tool does**, never what it earns.

## 0. Where FLARE stands today (internal only, never quote this in marketing)
| Evidence | Result |
|---|---|
| Offline structure-break baseline, ES and NQ 5m, Aug–Oct 2026, split in halves (`IDEAS_v10.md`, `DNF_TRIGGER_TEST.md`) | **Lost money in 3 of 4 halves** (ES PF 0.69 / 1.10, NQ 0.68 / 0.77) |
| TradingView ES 3m/5m "H" config (`VALIDATION_v9.md`) | Positive, but only about 2 months, 21–32 positions per half, and chosen after many filter tests |
| ES 30m, Jan 2025–Oct 2026 (`LONG_HISTORY.md`) | PF 0.87; every 2026 quarter lost money |
| NQ (`NQ_DIAG.md`) | No edge; the held% filter works in the opposite direction from ES |
| DNF trigger | Not testable (fewer than 13 trades per half) and **not part of FLARE** |

**Read-out:** right now the honest product is a **level-mapping and trade-planning tool**, not a strategy that makes money.

**Two blockers before any sale:**
1. **TradingView changed the sales rules.** From **Nov 1, 2026**, access to invite-only scripts may not be sold outside TradingView's Marketplace. That includes Whop, Gumroad and paid Discords [1].
2. **FLARE reuses SpacemanBTC/sbtnc code.** The header says "SpacemanBTC framework credit: sbtnc". A closed-source paid script needs the original author's **explicit permission**, or that code must go [2][3][29].

---

## 1. Launch gates (what the backtest must show first)
Every gate is pass/fail. Write the thresholds down **before** running the tests, in this file and in a dated git commit.

| # | Gate | Pass criterion |
|---|---|---|
| G0 | **Freeze the rules** | One config (for example v14 "H": half-way scalp, runner to the next level, held% setting fixed) is committed with a hash and date. No tuning during G1–G4. Any change restarts G1. |
| G1 | **Long-history backtest** (TradingView Premium has all intraday minute history [13]) | At least 12 months (target 18–24) on **both ES1! and NQ1!**, on the chosen timeframe, with costs of $2.50/side/contract plus 1 tick slippage. Need **≥ 100 positions per market**, ≥ 30 positions per half, **PF > 1 in both halves on both markets**, and PF > 1 in ≥ 3 of 4 quarters. If NQ fails, the product is ES-only and says so. |
| G2 | **Untouched holdout** | The most recent 3 months, never looked at during development: PF > 1 with ≥ 30 positions. |
| G3 | **Robustness** | (a) Bootstrap 5th-percentile PF ≥ 1.0 on pooled positions. (b) Slippage doubled to 2 ticks: PF still ≥ 1.0. (c) Key inputs moved ±20% (confirm window, pivot length, held%): PF stays > 1, i.e. a plateau, not a knife edge. (d) Top 5 winners removed: PF ≥ 1.0. (e) Max drawdown and longest losing streak are recorded in R and in $ per contract. (f) Trend months and chop months are reported separately. |
| G4 | **Forward test (paper)** | 60–90 calendar days and ≥ 40 positions, from **live TradingView alerts** logged with timestamps to a public channel (see §6). PF > 1, or at least inside the 90% bootstrap band of the backtest. |
| G5 | **Clean IP and compliance** | Written sbtnc permission on file, or the Spaceman code replaced. §5 checklist complete. Disclaimer text reviewed by a lawyer. |

**If G1–G4 fail:** do **not** sell signals or the strategy. Choose one of these:
- (a) Keep FLARE free and grow the channel on honest research content.
- (b) Sell only a **map tool** (levels plus held/broken memory stats) with no entry signals and no backtest claims.
- (c) Redesign and restart at G0.

Never "launch anyway with disclaimers."

---

## 2. Product offer and tiers
| Tier | What it includes | When |
|---|---|---|
| **FLARE Map (free, open-source)** | Calendar levels (D/W/M/Q/Y opens, previous H/L/mid, Monday range), held/broken memory % per level, the clean v14 visuals. Credits SpacemanBTC. | Phase 1. Complies with the open-source reuse rule [3] and starts the funnel. |
| **FLARE Pro (closed beta, free)** | Public invite-only script given to about 25–50 testers **only if they ask** [2]. Includes setups, scalp/runner plan lines, alerts, and the strategy version so users can run their own backtests. | Phases 2–3, during G4. Non-commercial use of invite-only scripts stays allowed [1]. |
| **FLARE Pro (paid)** | The same script in a TradingView **Paid Space**: one publication with ES/NQ presets (separate versions per market are banned as "suites" [2]), docs, changelog, support. | Phase 4, **only after G0–G5 pass**. |
| **Community (free)** | Discord for education, bug reports and the validation log. Script access is never bundled with a paid community [1]. | Phase 1 onward |

**Never offer:**
- A signal-calling room or copy trading.
- Account management or auto-execution on someone else's account. Directing accounts removes the CTA registration exemption [7].
- 1:1 advice tailored to someone's positions or finances [7].
- "Funded account" or "pass your prop challenge" promises.
- Lifetime deals. Paid Spaces bill monthly only [4].

**Positioning line** (describes the tool, makes no outcome claim): *"FLARE maps the calendar levels ES and NQ react to, tracks how often each level has held, and drafts a trade plan, with a scalp at the half-way point and a runner to the next level, when structure breaks. You decide whether to take it."*

---

## 3. Pricing
**Comparable tools (checked Oct 15, 2026):**
| Product | Price |
|---|---|
| TradingView Paid Spaces overall | $4.99–$199/mo [5] |
| LuxAlgo | Essential $24.99/mo, Premium $39.99/mo, monthly billing (annual is cheaper) [6] |
| Zeiierman | Monthly, quarterly, yearly and lifetime plans; an all-in suite of 80+ indicators plus Discord [15] |

**Recommendation:**
- **Beta:** $0.
- **Launch:** **$29/mo** (one Paid Space subscription). Reasons:
  - FLARE is a single, focused futures tool from a new creator, so it should sit below the big suites ($40–70).
  - It is high enough to filter out tyre-kickers.
- **Set the price once and keep it.** Paid Spaces cannot grandfather old prices: a price change hits existing subscribers at their next renewal [4].
- **Don't run "limited-time" discounts.** TradingView bans limited-time offers in vendor content, and prices may only appear in the Author's-instructions field and your profile Signature [2].
- **Economics:** platform fee is **0% today** but can change with notice; that 0% is locked in only for Spaces approved before Apr 1, 2026 [4]. 100 subscribers × $29 = **$2,900/mo gross before income tax**. Payout is monthly via PayPal, $100 minimum, with up to 30 days' settlement [4].
- **Review after 6 months** of paid operation and continued forward data. Any increase should come with added features, never with results.

---

## 4. Delivery and tech setup
**The platform decision (rules effective Nov 1, 2026):**
- Paid access to invite-only scripts goes through **TradingView only** [1].
- Paid Spaces requirements [4][9]:
  - Approval through the Creator Program, by application.
  - Premium or Ultimate plan, kept active for as long as the Space is live.
  - At least one public invite-only script.
  - A Partner Program payout account.
- TradingView is the merchant of record and handles billing, renewals, cancellation and sales tax [9].
- **Whop, Gumroad and Discord bots:** before the rule change, sellers granted access by **TradingView username**:
  - Whop's TradingView app adds the buyer's username to the invite-only access list and can auto-revoke on cancel [8].
  - Buyers enter their exact TradingView username, not their email [16].
  - **Don't build on this.** It is no longer allowed for paid access, and the Whop app needs your TradingView **session cookies** [8], which is a real account-security risk. Use Whop/Gumroad only for things unrelated to the script, if ever (fees: Whop 2.7% + $0.30 [10], Gumroad 10% + $0.50 [11]).
- **Before you apply,** email **creators@tradingview.com** to confirm the current Marketplace path for a new author [1].

**Setup checklist:**
1. **IP:** message sbtnc (SpacemanBTC) and ask for written permission to use their code in a closed-source paid script. Save the reply. If you get no permission, rewrite the level engine from scratch (the levels themselves are generic concepts) and remove the reused code [2][3]. Keep the DNF mentor method out of any paid product unless the mentor gives written permission.
2. **TradingView Premium** (needed for invite-only publishing, Paid Spaces, webhooks and full minute history) [13].
3. **Publication hygiene [2][3]:**
   - English title and description. Explain **what is original** and why the code is closed.
   - For the strategy report, state the properties used: $2.50/side, 1 tick slippage, contract size, capital. Use standard candles only.
   - Keep the non-repainting audit. The lookahead/`request.security` fixes already done for DNF are the standard to hold to.
4. **Alerts:** TradingView webhook → Discord webhook into `#flare-log`, giving a timestamped forward record (G4).
5. **Docs** (GitBook or Notion, free tier): quick-start, inputs reference, known limitations (NQ weakness, trend months, holds of up to 5h or more), changelog, support email.
6. **Landing page** (Carrd or similar) plus an email list (free tier). It holds the full disclaimers, privacy policy and terms of use.
7. **Version control:** tag every published version. The release notes match the frozen config.

---

## 5. Legal and disclaimer checklist
_Have a futures/advertising lawyer review this before launch. Budget is in §9._

**CFTC / NFA**
- [ ] **Stay within the CTA registration exemption, Rule 4.14(a)(9).** Selling the same non-customized software and advice to everyone is exempt **only if** you (i) never direct client accounts and (ii) never tailor advice to anyone's positions or circumstances [7]. In Discord and YouTube comments, answer "how does the tool work", never "what should you do with your trade". A paid signal service that originates signals is CTA activity [14].
- [ ] **Anti-fraud still applies even when exempt:** CEA §4o and §4b, Rule 4.41(a) on deceptive ads, and Rule 4.41(b) on hypothetical results [7].
- [ ] **Any backtest or strategy-tester image carries the CFTC 4.41(b) statement, prominently and right next to the results** [12]:
  > "These results are based on simulated or hypothetical performance results that have certain inherent limitations. Unlike the results shown in an actual performance record, these results do not represent actual trading. Also, because these trades have not actually been executed, these results may have under- or over-compensated for the impact, if any, of certain market factors, such as lack of liquidity. Simulated or hypothetical trading programs in general are also subject to the fact that they are designed with the benefit of hindsight. No representation is being made that any account will or is likely to achieve profits or losses similar to these being shown."
- [ ] **Use NFA Rule 2-29 as the best-practice template** (it binds NFA members; you are not one) [17]:
  - Never mention profit without an **equally prominent** risk-of-loss statement.
  - Never say futures trading suits everyone.
  - Label hypothetical results and show the losing periods.
  - Add a "little or no actual trading experience with this system" line until a real record exists.
  - Once a real forward record exists, lead with it instead of the backtest.
- [ ] **Never use these words:** "guaranteed", "risk-free", "consistent profits", "win rate X%" as a selling point, "replace your job", "passive income". The CFTC calls promises of high profit with low risk a fraud red flag [18].

**FTC**
- [ ] **FTC Act §5 needs substantiation.** Earnings and performance claims need written proof that the results are typical. Raging Bull ($2.4M) [19] and **Warrior Trading** ($3M, day-trading education) [20] were penalized for exactly this. Simplest compliance: **make no earnings claims at all.**
- [ ] **Endorsement Guides [21]:**
  - Testimonials showing exceptional results must disclose generally expected results; "results not typical" is not enough.
  - Disclose every material connection: free access, affiliate links, sponsorships.
  - **Policy:** no P&L testimonials at all. Only feature or usability quotes.
- [ ] **Consumer Reviews and Testimonials Rule (16 CFR 465):** no fake, bought, AI-generated or insider reviews, and no suppressing negative reviews. Civil penalties apply [22].
- [ ] **Subscriptions (ROSCA):** disclose terms clearly, get express consent, and make cancelling easy. The 2024 click-to-cancel rule was vacated, but ROSCA still applies [23]. TradingView handles billing for Paid Spaces; this matters if you ever bill directly.

**TradingView [2][3]**
- [ ] No unrealistic or unsubstantiated performance claims, **including off TradingView**.
- [ ] Prices appear only in Author's instructions or your Signature.
- [ ] Never promote the paid script in other publications. Exception: "HOW-TO:" ideas or videos, at most 10 per script per year.
- [ ] Grant access only on request. Remove anyone who asks.
- [ ] Don't sell private scripts.

**YouTube**
- [ ] Spam policy bans "get rich quick" schemes, malicious clickbait and off-platform diversion. It can lead to strikes or channel termination [24].
- [ ] Tick **"includes paid promotion"** for any sponsorship or affiliate deal [25].
- [ ] Thumbnails and titles carry no $ figures and no "100% win rate" or "this changed everything" claims.

**Standard footer** (description, landing page, Discord #rules, pinned comment):
> *Educational content only, not financial advice. FLARE is a charting tool; it does not know the future. Futures trading involves substantial risk of loss and is not suitable for everyone. Any backtest shown is hypothetical (see CFTC Rule 4.41 disclosure). Past or simulated results do not indicate future results. I am not a registered CTA and do not give personalized advice.*

**Business setup:** form a single-member LLC (state fees vary), keep business banking separate, and consider E&O insurance once you have paying users.

---

## 6. YouTube channel strategy
**Positioning:** *"An honest futures-tool builder: I test my own indicator in public, including the parts that fail."* This angle stands out in a niche full of P&L screenshots. Proven formats to borrow:
- **Trading Rush:** "I tested strategy X 100 times" style backtests [26].
- **AlgoGrade's journey log:** building a futures bot in public, losses included [27].
- **Shorts tip:** concrete, searchable findings ("this filter cut losses on trend days") outperform "I built X" framing [28].

**Formats (rotate):**
1. **Validation report** (monthly, long-form): G1–G4 progress with full tables, losers included, and the 4.41 disclaimer on screen.
2. **Pine Script build and teardown:** how FLARE's pieces work. Repainting, lookahead and `request.security` traps are evergreen, searchable topics.
3. **"Idea graveyard":** filters tested and rejected (SMT, session windows, wick ratios, DNF). Honest and cheap to make.
4. **Level-map education:** "how calendar levels work on ES/NQ" using past charts. **No live calls or trade recommendations.**
5. **Shorts:** one finding, one chart, about 30–45 seconds. Cut 2–3 from each long video.

**First 10 videos:**
1. "I'm building a futures indicator in public and it isn't profitable yet: here's the plan." (Rules for the series, the gates, the disclaimers.)
2. "Your TradingView indicator is probably repainting: 3 lookahead bugs I fixed." (Lessons from the DNF v2 fixes; pure education.)
3. "How to map daily, weekly and monthly levels on ES automatically (Pine v6)." (Launches the free FLARE Map.)
4. "Do ES levels 'remember'? Measuring how often a level held or broke." (The held% concept, shown honestly with its NQ contradiction.)
5. "I tested 12 filters on my strategy; 11 failed." (The idea graveyard.)
6. "Scalp at half-way, runner to the next level: does splitting a position actually help?" (Exit design, with the caveat that the scalp leg alone isn't a cushion.)
7. "Why my strategy works on ES and falls apart on NQ." (Stop size vs ATR, trades that reach 1R and reverse.)
8. "Backtests lie: in-sample vs holdout vs forward test, explained with my own data."
9. "Trend months broke my strategy: regime analysis on 22 months of ES."
10. "Forward test, month 1: every alert, every loser." (Starts the recurring series.)

**Cadence:**
- 1 long video per week (10–20 min) and 2–3 Shorts per week.
- 1 monthly validation report.
- One 2–4 hour batch session per week to film and edit.

**Building in public (rules):**
- Pre-announce the gates in video 1 and report against them every month.
- Show the forward log link and the losing streaks.
- If a gate fails, say so on camera and show the pivot. That episode is the series' credibility moment.

**Metrics to track:** CTR, average view duration, subscriber gain per video, free Map installs, Discord joins, and beta waitlist size. Do not track or show P&L as a channel metric.

---

## 7. Community
- **Discord (free).** Channels:
  - `#rules-and-disclaimer`, `#announcements`
  - `#flare-log` (auto-posted alerts plus outcomes)
  - `#validation-reports`
  - `#levels-education`
  - `#bug-reports`, `#feature-requests`
  - `#beta-feedback` (role-gated)
- **House rules:**
  - No trade calls and no "should I take this" advice (this protects the 4.14(a)(9) exemption [7]).
  - No P&L screenshots, which avoid becoming de-facto testimonials [21].
  - No affiliate spam.
- **Beta program:** 25–50 testers chosen from the waitlist, granted access on request [2]. Ask them for one structured feedback form every 2 weeks (bugs, clarity, usability) and pass bug fixes into the next frozen version.
- **Don't solicit on TradingView.** No comment spam and no unrequested access grants [2]. Grow through YouTube, the Signature link, and useful open-source publications.
- **Moderation:** set up AutoMod plus 1–2 trusted moderators by about 300 members.

---

## 8. Phased timeline (dates PT; later phases depend on gates, not on the calendar)
| Phase | Weeks (starting Oct 19, 2026) | Work | Exit criterion |
|---|---|---|---|
| **0: Foundations** | Wk 1–2 | Freeze rules (G0). Contact sbtnc. Email creators@tradingview.com. Upgrade to Premium. Create the YouTube channel, Discord and landing page. Draft disclaimers. Record videos 1–2. | Rules frozen; IP route chosen |
| **1: Long-history validation** | Wk 2–8 | Run G1–G3 on ES and NQ. Publish the free FLARE Map, open-source with credit. Videos 3–9. | G1–G3 pass, or a documented failure leading to the pivot in §1 |
| **2: Forward test and beta** | Wk 8–20 | Live alerts into `#flare-log` for 60–90 days (G4). Free invite-only beta. Monthly reports. | G4 pass; ≥ 25 active beta users; bug count trending down |
| **3: Compliance and Creator application** | Wk 16–22 | Lawyer review (G5). Finalize the publication text. Apply to the Creator Program. | Approved |
| **4: Paid launch** | Wk ~22+ (about Mar–Apr 2027 at the earliest) | Paid Space at $29/mo. "HOW-TO:" video. Beta users get a thank-you, not a lifetime deal. | First 30 days of support handled; churn reviewed |
| **5: Iterate** | Ongoing | Monthly forward report continues. Feature work. Re-validate every major version (back to G0). | — |

---

## 9. Costs (estimates; check current prices)
| Item | One-time | Monthly |
|---|---|---|
| TradingView **Premium** (needed for invite-only publishing, Paid Spaces, webhooks and full minute history) | — | About $30–60 depending on promo and billing; the pricing page showed a $29.95/mo promo on Oct 15, 2026 [13] |
| CME real-time data on TradingView (optional; backtests don't need it) | — | Small exchange fee per month |
| Lawyer review of disclaimers and terms (estimate) | $500–2,000 | — |
| LLC formation and registered agent (varies by state) | $50–500 | $0–25 |
| Microphone and lighting (OBS and DaVinci Resolve are free) | $100–250 | — |
| Domain and landing page, docs, email list (free tiers to start) | $15–20/yr | $0–20 |
| Discord | — | $0 |
| TradingView platform fee on sales | — | 0% today, can change [4] |
| **Total to reach Phase 4** | **About $700–2,800** | **About $30–100** |

---

## Sources (accessed Oct 15, 2026)
1. TradingView Blog, "Commercial scripts are moving to the TradingView Marketplace" (Sep 30, 2026): https://www.tradingview.com/blog/en/commercial-scripts-move-to-marketplace-61291/
2. TradingView, Vendor Requirements: https://www.tradingview.com/support/solutions/43000549951-vendor-requirements/
3. TradingView, Script Publishing Rules: https://www.tradingview.com/support/solutions/43000590599-script-publishing-rules/ and Pine docs on publishing: https://www.tradingview.com/pine-script-docs/writing/publishing/
4. TradingView, Creator Program (Paid Spaces) Terms: https://www.tradingview.com/support/solutions/43000772177-tradingview-creator-program-paid-spaces-terms/
5. TradingView Blog, "TradingView Creator Program: a new way to earn from your scripts": https://www.tradingview.com/blog/en/tradingview-creator-program-60011/
6. LuxAlgo pricing: https://www.luxalgo.com/pricing/
7. CFTC, Final Rule adopting 4.14(a)(9), 65 FR 12938 (2000): https://www.cftc.gov/foia/fedreg00/foi000310a.htm
8. Whop TradingView access app: https://xybtyddfvqkrw7t2amlo.apps.whop.com/apps/app_CBnePu0MQNJPhb/ and https://qlub99.com/tradingview
9. TradingView, Creator Program page: https://www.tradingview.com/creator-program/ and How to create a Paid Space: https://www.tradingview.com/support/solutions/43000790233-how-to-create-a-paid-space/
10. Whop fees: https://docs.whop.com/payments-and-billing/fees/fees
11. Gumroad pricing: https://gumroad.com/pricing
12. 17 CFR 4.41 (eCFR): https://www.ecfr.gov/current/title-17/chapter-I/part-4/subpart-D/section-4.41
13. TradingView pricing: https://www.tradingview.com/pricing/
14. CFTC Commissioner Pham statement (signal provider vs technology provider): https://www.cftc.gov/PressRoom/SpeechesTestimony/phamstatement082923
15. Zeiierman pricing: https://www.zeiierman.com/pricing
16. Example username-based access flows: https://stat-map.com/resources/how-to-claim-access-to-tradingview-indicators-on-whop and https://ez-algo.gitbook.io/ez-algo/getting-started/publish-your-docs
17. NFA Compliance Rule 2-29: https://www.nfa.futures.org/rulebooksql/rules.aspx?RuleID=RULE+2-29&Section=4
18. CFTC Fraud Advisory, Commodity Trading Systems Sold on the Internet: https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/fraudadv_tradingsystem.html and AI trading-bot advisory: https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/AITradingBots.html
19. FTC, Raging Bull settlement: https://www.ftc.gov/news-events/news/press-releases/2022/03/online-investment-site-pay-more-24-million-bogus-stock-earnings-claims-hard-cancel-subscription
20. FTC, Warrior Trading: https://www.ftc.gov/news-events/news/press-releases/2022/04/federal-trade-commission-cracks-down-warrior-trading-misleading-consumers-false-investment-promises
21. FTC Endorsement Guides, 16 CFR 255: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 and https://www.ftc.gov/legal-library/browse/rules/use-endorsements-testimonials-advertising
22. FTC Consumer Reviews and Testimonials Rule: https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials
23. Federal Register, Negative Option Rule revision (Feb 12, 2026): https://www.federalregister.gov/documents/2026/02/12/2026-02866/revision-of-the-negative-option-rule-withdrawal-of-the-cars-rule-removal-of-the-non-compete-rule-to and WilmerHale on the 8th Circuit vacatur: https://www.wilmerhale.com/en/insights/client-alerts/20250801-eighth-circuit-vacates-the-ftcs-click-to-cancel-rule-but-federal-and-state-regulators-likely-to-remain-active
24. YouTube Spam Policy: https://support.google.com/youtube/answer/2801973
25. YouTube paid promotion disclosure: https://support.google.com/youtube/answer/154235
26. Trading Rush, "Why I back test strategies only 100 times": https://tradingrush.net/indicator-trading-probability-important-why-i-back-test-trading-strategies-only-100-times/
27. AlgoGrade, building a futures bot in public: https://algograde.com/journey
28. DEV Community, "product framing beats build-in-public 14x" (Shorts experiment): https://dev.to/morinaga/what-i-learned-running-48-youtube-shorts-product-framing-beats-build-in-public-14x-394h
29. SpacemanBTC "Key Levels SpacemanBTC IDWM" (open-source; base of FLARE's level map): https://www.tradingview.com/script/PV6TowBV-Key-Levels-SpacemanBTC-IDWM/

_Notes:_
- eCFR pages block automated fetches. The 4.41(b) wording above matches the CFR text as quoted in search results and in the CFTC's 2000 rule [7]. Check the wording against the official CFR before publishing.
- Comparable prices change often. Check them again just before launch.
