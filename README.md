# Qualcomm (QCOM) — FY2029 EV/EBITDA Valuation

> | | Current run |
> |---|---|
> | **Valuation date** | **November 21, 2026** |
> | **Latest financials** | **Q4 / full-year FY2026**, ended September 27; reported November 4, 2026 |
> | **Price anchor** | **$149.94**, November 20, 2026 regular-session close |
> | **Targets** | June 24, 2026 Investor Day; FY29 growth targets supported again on the Q4 call |

A Bear/Base/Bull sum-of-the-parts EV/EBITDA valuation. All financial assumptions and
valuation calculations live in [model.py](model.py); the [notebook](qcom_fy29_valuation.ipynb)
imports them and adds charts and sensitivity tables. No live market feed is used at runtime.

**Not investment advice.** Forward revenue, margins, multiples and capital structure are
management targets or explicit author assumptions. Figures below describe this dated model.

## 1. Headline result

Required return **10%**; horizon **2.8583 years** to September 30, 2029;
current diluted shares **1.073B**; net debt **$7.431B**.

| Scenario | FY29 EV | FY29 equity/share | PV/share | vs. $149.94 |
|---|---:|---:|---:|---:|
| Bear | $104.49B | $90.45 | **$68.88** | -54.1% |
| Base | $240.40B | $217.12 | **$165.34** | +10.3% |
| Bull | $421.66B | $386.05 | **$293.99** | +96.1% |
| Weighted (25/50/25) | — | — | **$173.39** | **+15.6%** |

Base is about 10% above the price anchor; the weighted estimate
is higher, with a very wide downside/upside range. Data center contributes
29.0% of Base EV. Execution and exit-multiple
assumptions remain more important than apparent precision in the midpoint.

**Comparability matters:** the September weighted estimate was $157.86. Updating only
market anchors gives **$160.32**, with Base **$150.37**. Correcting
the revenue-target mapping then gives **$173.96** weighted; the new Bear
trajectory/margin assumptions bring it to **$173.39**. Most of the model increase
comes from a modeling correction, not an earnings-driven upgrade.

## 2. What changed — Q4 / full-year FY2026

The release was **November 4**, not the November 11 date previously recorded here.
Financial figures are from the [release](https://investor.qualcomm.com/files/content_files/FY2026-4th-Quarter-Earnings-Release.pdf) and its [SEC-filed copy](https://d18rn0p25nwr6d.cloudfront.net/CIK-0000804328/29e9b475-f432-4e1d-83c3-c602cafb234b.pdf).

| Q4 FY26 | Reported | YoY |
|---|---:|---:|
| GAAP revenue | $10.322B | −8% |
| Non-GAAP revenue | $10.442B | −7% |
| Non-GAAP EPS | $2.17 | −28% |
| QCT revenue / EBT margin | $9.015B / 24% | −8% / −5 pts |
| Handsets | $5.137B | −26% |
| Automotive | $1.990B | +89% |
| IoT | $1.888B | +4% |
| QTL revenue / EBT margin | $1.304B / 70% | −7% / −2 pts |

| $M, actual | Q1 | Q2 | Q3 | Q4 |
|---|---:|---:|---:|---:|
| Handsets | 7,824 | 6,024 | 5,086 | 5,137 |
| Automotive | 1,101 | 1,326 | 1,588 | 1,990 |
| IoT | 1,688 | 1,726 | 1,830 | 1,888 |
| QCT EBT margin | 31% | 27% | 26% | 24% |

The [Q4 call](https://s204.q4cdn.com/645488518/files/content_files/Q4FY26-Earnings-Conference-Call_Transcript_11-5-26_Final.pdf) supports four judgments:

1. Automotive's stronger exit trajectory raises Bear FY29 revenue **$8B→$9B**.
2. IoT's slowdown raises execution risk against the growth required by Base; Bear
   revenue falls **$10B→$9B**. Base revenue remains tied to the management target.
3. QCT margin pressure persists. Bear handset/licensing EBITDA margin falls **32%→30%**.
   Base/Bull margins remain author assumptions; the 30% long-term QCT EBT target is retained.
4. Data-center customer progress supports retaining the ramp assumptions, but **$9B Bear
   revenue is an author downside case, not a contractual floor**. No multiple increase is assumed.

**FY27 checkpoint:** management reiterated $5B data-center revenue and >60% non-handset
growth. The call guides Q1 data center >$650M. Q1 total revenue guidance is $10.4–11.2B,
QCT $9.0–9.6B, QTL $1.3–1.5B and non-GAAP EPS $2.15–2.35. Call EBT-margin guidance is
20–22% QCT and 72–76% QTL; QCT now includes data center. Pricing benefits are expected
fully in the second half of FY27. There is **no full-year total-revenue/EPS forecast** in this model.

**Renewals:** Apple, Huawei and Transsion signed long-term QTL agreements. The call says
licensing's run rate is unchanged. Apple modem substitution affects chip sales; it does
not itself eliminate patent royalties. These are separate risks.

## 3. Revision history and audit trail

Historical rows are preserved as published, even where methodology was later corrected.

| Run date | Latest financials used | Price anchor | Base PV/sh | Prob-wtd PV/sh | vs. price |
|---|---|---:|---:|---:|---:|
| Jun 29, 2026 | FY2025 results + Jun 24, 2026 Investor Day | $250.00 | ~$157 | ~$165 | −34% |
| **Sep 1, 2026** | **Q3 FY2026** (quarter ended Jun 28, 2026) | **$170.48** | **~$148** | **~$158** | **−7%** |
| **Nov 21, 2026** | **Q4 / full-year FY2026** | **$149.94** | **$165.34** | **$173.39** | **+15.6%** |

Changes in this run:

- Anchors: price $170.48→$149.94; diluted shares 1.069B→1.073B; net debt
  $7.000B→$7.431B; horizon 3.08→2.8583 years, calculated from dates.
- Annual rollover: Q4 estimate replaced by actual; completed FY26 uses as-reported
  annual totals. FY27 opens with Q1 guidance only; Q1 is never called a full fiscal year.
- **Target mapping corrected:** the prior $20B handset line incorrectly included QTL.
  The management mix target applies to **QCT**, so the Base now has ~$20B handset chips
  **plus** author-assumed flat QTL revenue of $5.556B. The same licensing add-on is applied
  consistently to Bear/Bull's $16B/$23B handset-chip assumptions.
- The prior $10B auto + $14B IoT + $15B data center sum was $39B, not the stated $40B.
  Keep auto $10B and allocate the remaining $30B in the lower-bound ratio 14:15:
  IoT **$14.483B**, data center **$15.517B**. This interpolation
  satisfies both greater-than thresholds and the aggregate target; it is not an exact
  management segment split. Base revenue is **$65.556B**, including licensing.
- Bear auto/IoT revenue and handset margin changes are justified in §2. Other
  margins, all exit multiples, the 10% discount rate and 25/50/25 weights are unchanged.
- Notebook now imports the model. FY25 QTL EBT uses the script's as-reported **$4.043B**;
  weighted valuation uses full-precision values. Sensitivities use the same engine.
- EBITDA basis is **unchanged**, but explicitly labeled a proxy (§6). This avoids
  disguising a convention change as an operational improvement.

## 4. Company overview and current anchors

Qualcomm combines QCT chip sales with QTL patent licensing. The valuation groups
handset chips and licensing together, while automotive, IoT and data center receive
separate margins and multiples. This grouping is a modeling choice, not the company's
reported segment structure.

FY26 GAAP revenue was **$43.120B**, versus $44.284B in FY25. QCT revenue was $37.208B,
QTL $5.556B; handset chips $24.072B, automotive $6.004B and IoT $7.132B. Annual QCT EBT
was $10.101B and QTL EBT $4.022B; D&A $1.630B. The carried-forward EBITDA proxy is
**$14.253B**, versus $15.815B in FY25. GAAP total revenue and segment revenue are kept
on their reported bases; Q4 non-GAAP total revenue is $120M higher than GAAP.

Net debt: short-term debt $2.492B + long-term debt $12.620B − cash $4.636B − marketable
securities $3.045B = **$7.431B**. Restricted cash is excluded. Diluted shares **1.073B**
come from the non-GAAP EPS reconciliation, rather than issued/outstanding shares.

Key risks: Apple chip substitution and handset cyclicality; input costs and pricing
execution; China exposure; IoT growth shortfalls; data-center ramp, customer concentration,
capital needs and potential customer-warrant dilution; licensing and legal developments.

**Sell-side snapshot:** [Yahoo analyst data](https://finance.yahoo.com/quote/QCOM/analyst-insights/)
shows TD Cowen **Buy/$185** and Rosenblatt **Buy/$205**, dated November 5, and Barclays
**Underweight/$150**, dated November 5. These are dated external opinions, not model inputs.
The former $175 snapshot is retired. Peer trading multiples have not been refreshed;
the exit multiples below are carried-forward author assumptions.

## 5. Management targets and the Base interpretation

[Investor Day, June 24, 2026](https://investor.qualcomm.com/news-events/press-releases/news-details/2026/Qualcomm-Accelerates-Diversification-with-Comprehensive-Strategy-for-Data-Center-and-Sees-Multiple-Inflection-Points-Over-the-Next-3-to-5-Years/default.aspx)
sets $40B QCT non-handset revenue, $10B automotive, >$14B IoT, >$15B data center,
approximately one-third QCT handset mix, and >$18 non-GAAP EPS for FY29.
The Q4 call supports the FY29 growth plan. Base respects these targets with the
explicit allocation and licensing assumptions in §3; it does not impose a revenue haircut.

The original November 2024 diversification target was $22B auto+IoT; June 2026 added
the data-center pillar. These are long-range ambitions, not reported revenue or contracted minimums.

## 6. Valuation methodology and assumptions

Each table cell is **FY29 revenue ($B) / EBITDA margin / exit EV/EBITDA**.

| Segment | Bear | Base | Bull |
|---|---:|---:|---:|
| handset | 21.556 / 30% / 7× | 25.556 / 38% / 8× | 28.556 / 40% / 10× |
| automotive | 9.000 / 22% / 10× | 10.000 / 28% / 13× | 13.000 / 30% / 16× |
| iot | 9.000 / 24% / 10× | 14.483 / 30% / 13× | 16.000 / 33% / 18× |
| datacenter | 9.000 / 18% / 11× | 15.517 / 25% / 18× | 20.000 / 30% / 25× |

Handset/licensing is assigned a mature-business multiple; automotive reflects a
stronger growth trajectory with cycle risk; IoT assumes edge/industrial execution;
data center receives a growth premium and the widest range. Exit multiples have
not been re-marked to current peers. Combining licensing and chips still obscures
their different economics; the aggregate margins are author assumptions, not a
reconstruction of the QCT/QTL targets.

1. Segment EBITDA = revenue × assumed margin.
2. Segment EV = EBITDA × exit multiple; sum for enterprise value.
3. FY29 equity = EV − current net debt, held flat by assumption.
4. Discount equity at 10% over 2.8583 years; divide by current diluted shares.
5. Weight scenario PVs at 25/50/25 without intermediate rounding.

The model does not project interim dividends, buybacks, future balance-sheet changes
or incremental warrant dilution. Price CAGR excludes dividends. The 1.02B FY29 share
assumption is used only for the EPS cross-check, not the headline per-share valuation.

**Trailing EBITDA proxy:** QCT EBT + QTL EBT − $1.5B corporate bridge + reported D&A.
The corporate bridge was calibrated to a prior quarter's difference between segment
EBT and consolidated non-GAAP EBT, which also includes financing/investment effects.
Reported D&A may overlap amortization already excluded from non-GAAP earnings.
Consequently this is not company-reported EBITDA or a complete GAAP reconciliation;
the unchanged basis is retained for historical comparability. It does not feed the
forward segment EBITDA calculation.

**Growth bridge ($B):**

| Segment | FY26 actual | Q4 ×4 | FY29 Base | CAGR from FY26 | CAGR from Q4 ×4 |
|---|---:|---:|---:|---:|---:|
| handset | 29.63 | 25.76 | 25.56 | -4.8% | -0.3% |
| automotive | 6.00 | 7.96 | 10.00 | +18.5% | +7.9% |
| iot | 7.13 | 7.55 | 14.48 | +26.6% | +24.2% |
| datacenter | n/a | n/a | 15.52 | new | new |

Both growth columns use three fiscal years from FY26 year-end. Q4 ×4 is seasonal,
not guidance. A missing data-center baseline means no separate FY26 stream was reported.
Auto is ahead of its required trajectory; IoT remains well short. Notebook sensitivity
tables flex discount rates and the data-center exit multiple using the shared engine.

## 7. EPS cross-check

| | FY29 EBITDA | Margin | Implied non-GAAP EPS |
|---|---:|---:|---:|
| Base | $20.735B | 31.6% | $15.72 |
| >$18 EPS threshold | $23.403B | 35.7% | >$18 |

The Base EBITDA assumption is **11.4%** below the $18 EPS threshold's
implied profitability. The bridge assumes $1.8B D&A, $0.5B net interest, 13% tax and
1.02B FY29 shares. Allocating the EPS-implied EBITDA by revenue share and using Base
multiples gives an illustrative **$197.94/share**. This alternative
allocation is not a management segment-margin forecast.

## 8. Run, verify and update

```bash
python3 model.py
python3 -m unittest discover -s tests -v
pip install -r requirements.txt
jupyter notebook qcom_fy29_valuation.ipynb
```

Files: `model.py` (single source), notebook (executed outputs/charts),
`UPDATE_RUNBOOK.md` (earnings-update procedure), `tools/extract_release.py`
(PDF extraction), `tests/test_model.py` (financial reconciliation and regression checks).

Next update: Q1 FY2027, when reported; confirm its actual date on Qualcomm IR.
Keep completed FY26 actuals as the trailing anchor until enough FY27 information exists
to construct and clearly label a full-year estimate.

## 9. Sources

- [Q4 / FY2026 release, November 4, 2026](https://investor.qualcomm.com/files/content_files/FY2026-4th-Quarter-Earnings-Release.pdf)
- [SEC 8-K, Exhibit 99.1; downloadable alternative](https://d18rn0p25nwr6d.cloudfront.net/CIK-0000804328/29e9b475-f432-4e1d-83c3-c602cafb234b.pdf)
- [Q4 FY26 earnings-call transcript](https://s204.q4cdn.com/645488518/files/content_files/Q4FY26-Earnings-Conference-Call_Transcript_11-5-26_Final.pdf)
- [November 20 regular-session close](https://stockanalysis.com/stocks/qcom/history/)
- [Analyst snapshot](https://finance.yahoo.com/quote/QCOM/analyst-insights/)
- [Q3 FY2026 release](https://s204.q4cdn.com/645488518/files/doc_financials/2026/q3/FY2026-3rd-Quarter-Earnings-Release.pdf)
- [Q2 FY2026 release](https://s204.q4cdn.com/645488518/files/doc_financials/2026/q2/FY2026-2nd-Quarter-Earnings-Release.pdf)
- [Q1 FY2026 release](https://s204.q4cdn.com/645488518/files/doc_financials/2026/q1/FY2026-1st-Quarter-Earnings-Release.pdf)
- [FY2025 full-year release](https://s204.q4cdn.com/645488518/files/doc_financials/2025/q4/FY2025-4th-Quarter-Earnings-Release.pdf)

**Forward targets:**
- Qualcomm June 24, 2026 Investor Day —
  [Business Wire](https://www.businesswire.com/news/home/20260624286521/en/Qualcomm-Accelerates-Diversification-with-Comprehensive-Strategy-for-Data-Center-and-Sees-Multiple-Inflection-Points-Over-the-Next-3-to-5-Years) ·
  [Futurum](https://futurumgroup.com/insights/qualcomms-investor-day-2026-agentic-and-ai-inference-to-drive-2x-revenue-growth-by-2030/)
- Qualcomm Nov 2024 Investor Day —
  [Qualcomm IR](https://investor.qualcomm.com/news-events/investor-events/events/event-details/2024/Investor-Day-2024-IoT-and-Automotive-Diversification-Update/default.aspx)
- [Futurum — Q3 FY26 analysis](https://futurumgroup.com/insights/qualcomm-q3-fy-2026-automotive-growth-offsets-handset-weakness/) (Apple share commentary, data-center ramp)



Market anchors gathered November 21, 2026. Historic peer-multiple observations in
prior commits are not current market data. All modeling changes are logged in §3.
