# Qualcomm (QCOM) — FY2029 EV/EBITDA Valuation

> ### 📌 As of this run
> | | |
> |---|---|
> | **Valuation date** | **September 1, 2026** |
> | **Latest financials used** | **Q3 FY2026** — quarter ended June 28, 2026, [reported July 29, 2026](https://s204.q4cdn.com/645488518/files/doc_financials/2026/q3/FY2026-3rd-Quarter-Earnings-Release.pdf) |
> | **Price anchor** | **$170.48** (Aug 31, 2026 close) |
> | **Forward targets from** | June 24, 2026 Investor Day (FY29 targets reaffirmed at the Q3 print) |
>
> Every input is in one `ASSUMPTIONS` block in [`model.py`](model.py). Re-run after the next
> earnings release and update this block.

A scenario-based, sum-of-the-parts **EV/EBITDA** valuation of Qualcomm anchored to the FY2029
financial targets management laid out at its **June 24, 2026 Investor Day**, re-underwritten on
**Q3 FY2026 actuals** and discounted back to a present value. Three scenarios —
**Bear / Base / Bull** — with the Base case taking management's FY29 *revenue* targets at face value.

> **Not investment advice.** This is an educational modeling exercise. All forward figures are
> management targets or the author's assumptions, not facts. Verify every input before relying on it.

- 📓 Model & charts: [`qcom_fy29_valuation.ipynb`](qcom_fy29_valuation.ipynb)
- 🐍 Runnable script (same logic, no Jupyter needed): [`model.py`](model.py)

---

## 1. Headline result

Discount (required return): **10%** · Horizon to FY29 year-end: **3.08 yrs**

| Scenario | FY29 EV (SOTP) | FY29 equity value / share | **PV today / share** | vs. price ($170.48) |
|----------|---------------:|--------------------------:|---------------------:|--------------------:|
| 🐻 **Bear**   | ~$95B  | ~$83  | **~$62**  | **−64%** |
| 😐 **Base**   | ~$219B | ~$199 | **~$148** | **−13%** |
| 🐂 **Bull**   | ~$399B | ~$367 | **~$274** | **+61%** |
| Prob-weighted (25/50/25) | — | — | **~$158** | **−7%** |

**Read:** the June run concluded the market was pricing close to the **Bull** case at $250. The stock
has since fallen ~31%, and at **$170** it now trades within ~7% of the probability-weighted fair
value and ~15% above the Base case. **The mispricing this model flagged in June has largely closed —
by the price falling to the model, not the model rising to the price.**

What remains is a much more balanced setup with an unusually wide distribution: the spread between
Bear (−64%) and Bull (+61%) is far wider than the 7% gap at the midpoint. That dispersion, not the
midpoint, is the finding. The valuation is still **dominated by the data-center assumption**
(revenue ramp × EBITDA margin × exit multiple), which alone is ~31% of Base-case enterprise value.

*Figures are outputs of the assumptions below; run `python3 model.py` for exact numbers.*

---

## 2. What changed since the June 2026 run

Qualcomm reported **Q3 FY2026** on July 29, 2026. It was a beat on revenue, a miss on EPS, and a
material change to the underlying thesis in both directions.

| Q3 FY26 (quarter ended Jun 28, 2026) | Result | vs. prior year |
|---|---:|---:|
| Total revenue | $9,947M | −4% |
| Non-GAAP EPS | $2.21 | −20% |
| **QCT** | $8,504M · EBT margin **26%** | −5% · −4 pts |
| — Handsets | $5,086M | **−20%** |
| — Automotive | $1,588M | **+61%** |
| — IoT | $1,830M | +9% |
| **QTL** | $1,278M · EBT margin 69% | −3% · −2 pts |
| Q4 FY26 guidance | Rev $9.7–10.5B · EPS $2.05–2.25 | — |

**The FY26 trend matters more than the single quarter.** Across Q1 → Q2 → Q3 the three QCT lines
are diverging sharply:

| $M | Q1 FY26 | Q2 FY26 | Q3 FY26 | YoY trend |
|---|---:|---:|---:|---|
| Handsets | 7,824 | 6,024 | 5,086 | +3% → −13% → **−20%** |
| Automotive | 1,101 | 1,326 | 1,588 | +15% → +38% → **+61%** |
| IoT | 1,688 | 1,726 | 1,830 | +9% → +9% → +9% |
| QCT EBT margin | 31% | 27% | **26%** | vs. the 30% FY29 target |

Three read-throughs drove the re-underwrite:

1. **Apple in-housing stopped being a risk and became a number.** Management guided Qualcomm's
   share of the upcoming iPhone to "materially below" the prior ~20% estimate. This was risk #1 in
   the June write-up; it is now partly realized, and it is the reason the handset exit multiple is
   cut from 9× to 8×.
2. **Input-cost inflation is compressing margins now.** Wafer, assembly, test, packaging and
   especially memory costs pushed QCT EBT to 26% against a 30% target. Management is taking
   "double-digit pricing actions" expected to benefit gross margin over time, and **reaffirmed** the
   30%/70% FY29 targets — so this hits the Bear case, not Base.
3. **Data center got materially de-risked.** Two custom-silicon engagements with global hyperscalers
   now have **confirmed purchase orders and wafer starts**, with revenue starting in Q4 FY26 and a
   new interim milestone of **$5B in FY2027** en route to $15B in FY29. In June there was no
   evidence between "nothing" and "$15B." The Bear data-center case rises from $7B to $9B and its
   exit multiple from 10× to 11×.

Management reaffirmed the FY29 targets: non-handset revenue $40B, non-GAAP EPS >$18, with
non-handset growth accelerating from 24% in FY26 to **>60% in FY27**.

**Balance sheet moved too.** Net debt is now **~$7.0B** (total debt $15.27B less cash and marketable
securities $8.30B), against ~$1.5B assumed in June — the result of the Alphawave, Arduino and
Modular acquisitions plus continued buybacks. This is a real ~$5.5B haircut to equity value.
*Note: $2.3B of restricted cash is excluded as it is committed to acquisition payments.*

---

## 3. Revision history

| Run date | Latest financials used | Price anchor | Base PV/sh | Prob-wtd PV/sh | vs. price |
|---|---|---:|---:|---:|---:|
| Jun 29, 2026 | FY2025 results + Jun 24, 2026 Investor Day | $250.00 | ~$157 | ~$165 | −34% |
| **Sep 1, 2026** | **Q3 FY2026** (quarter ended Jun 28, 2026) | **$170.48** | **~$148** | **~$158** | **−7%** |

The fair-value estimate moved only ~4% ($165 → $158) while the price fell 32%. Most of the change in
the *gap* came from the price, not the model — which is the outcome you want from a valuation that
was not simply tracking the tape.

---

## 4. Company overview (the 60-second version)

**What Qualcomm is.** A fabless (design-only) semiconductor company plus a patent-licensing business.
It designs the chips that connect and compute on the "edge" — phones, cars, PCs, headsets, industrial
gear — and it owns a foundational patent portfolio on the cellular standards (3G/4G/5G) that *every*
mobile device on Earth pays to use.

**How it makes money — two engines:**

| Segment | What it is | ~Share of FY26E revenue | Economics |
|---|---|---:|---|
| **QCT** (Qualcomm CDMA Technologies) | Chip sales: Snapdragon mobile SoCs + modems, RF front-end, **automotive** (Snapdragon Digital Chassis), **IoT/compute** (Snapdragon X PC chips, XR), and the new **data-center** AI/CPU effort | ~86% ($36.9B) | 30% target operating margin; **running at 26%** |
| **QTL** (Qualcomm Technology Licensing) | Royalties on 3G/4G/5G patents — collected on essentially every smartphone sold | ~13% ($5.6B) | ~70% target operating margin (cash machine) |

**FY2026 estimate** (9M actual + Q4 guidance midpoint): Revenue **$42.9B** (−3% YoY) ·
EBITDA **~$14.3B** (−9% YoY) · Diluted shares **1.069B** · net debt **~$7.0B**.
FY2026E segment revenue: handsets ~$24.0B · automotive ~$5.7B · IoT ~$7.1B · licensing ~$5.6B.
*(FY2025 actual for comparison: revenue $44.3B, EBITDA ~$15.8B on the same basis.)*

**Management (as of 2026):** Cristiano Amon (President & CEO) · Akash Palkhiwala (EVP, CFO & COO) ·
Alex Rogers (President, QTL & Global Affairs) · Nakul Duggal (Group GM — Automotive, Industrial & Cloud).
*Confirm current titles on the IR site before citing.*

**Competition by arena:**
- **Handset SoC/modem:** MediaTek, **Apple** (in-housing its own modem — now materializing), Samsung LSI, Google Tensor, UNISOC
- **RF front-end:** Broadcom, Skyworks, Qorvo
- **Automotive:** NXP, Renesas, Texas Instruments, Mobileye, NVIDIA (auto)
- **PC / compute:** Intel, AMD, Apple Silicon, NVIDIA (Arm PC)
- **Data center / AI inference (new):** NVIDIA, AMD, Broadcom, Marvell, and hyperscaler in-house silicon (Google TPU, AWS Trainium/Graviton, Meta MTIA)

**Key risks the model is sensitive to:**
1. **Apple modem in-housing — now partly realized.** iPhone share guided materially below the prior
   ~20%. Erodes a high-margin slice of QCT handset and, over time, QTL.
2. **Input-cost inflation** — memory/wafer/packaging costs are compressing QCT margins today
   (26% vs. a 30% target); the offsetting pricing actions are unproven.
3. **China concentration** — large share of revenue ties to Chinese OEMs / the China region.
4. **Handset cyclicality & structural decline** — handsets fell 20% YoY in Q3 and are now ~60% of
   QCT revenue, down from ~70% a year ago.
5. **Data-center execution & customer concentration** — still the entire bull thesis, but now
   order-backed rather than purely aspirational. Anchored on a small number of hyperscalers.
6. **Licensing/legal** — QTL renewals and the Arm licensing dispute.

**Sell-side snapshot (post–Q3 FY26):** the June cluster of $235–265 targets is gone. Post-print
targets have compressed sharply toward the **$175** area — TD Cowen cut to **$175** (retaining Buy),
Piper Sandler cut **$190 → $175** (Overweight). The dispersion that defined the June setup has
narrowed as the data-center story moved from thesis to backlog and the handset erosion became
quantified.

---

## 5. Investor Day comparison — Nov 2024 vs. June 2026 (FY2029 targets)

The single biggest change: management nearly **doubled the FY29 non-handset revenue target from $22B to
$40B**, driven almost entirely by a **brand-new ~$15B data-center business** that didn't exist as a
stated FY29 line in 2024.

| FY2029 target | **Nov 2024 Investor Day** | **June 2026 Investor Day** | Change |
|---|---:|---:|:--|
| **Non-handset revenue** | **$22B** | **$40B** | **+82%** |
| — Automotive | $8B | $10B | +25% |
| — IoT (total) | $14B | $14B | flat (re-segmented internally) |
| &nbsp;&nbsp;&nbsp;• Industrial & robotics | ~$4B | **$8B** | +100% |
| &nbsp;&nbsp;&nbsp;• Personal AI / PC / XR | ~$6B (PC $4B + XR >$2B) | $6B | ~flat |
| — **Data center** | *not a stated FY29 target (nascent)* | **>$15B** | **new pillar** |
| Non-GAAP EPS (FY29) | ~$18 | **>$18** | maintained / slightly higher |
| Revenue-mix goal | 50/50 handset vs. auto+IoT by 2030 | ~⅓ handset / ⅓ auto+IoT / ⅓ data center | **data center added as a 3rd pillar** |
| QCT / QTL operating-margin targets | 30% / 70% | 30% / 70% | reaffirmed |

**Reaffirmed at the Q3 FY26 print (July 29, 2026)**, with two additions: an interim **$5B FY2027**
data-center milestone backed by purchase orders and wafer starts, and non-handset growth
accelerating from **24% in FY26 to >60% in FY27**.

**A subtle tell:** non-handset revenue roughly doubled ($22B → $40B), yet the FY29 **EPS** target barely
moved (~$18 → >$18). That implies the incremental data-center revenue is being modeled at **lower
incremental margin** (and/or assumes heavier reinvestment) than the legacy mix — which is exactly why
the model treats the data-center exit multiple, not just its revenue, as the key swing variable.

---

## 6. Valuation methodology & why these choices

**Why EV/EBITDA (not P/E or DCF as the headline)?**
- EBITDA is capital-structure- and tax-neutral, which matters for a company actively re-shaping its mix
  and balance sheet, and it's the *lingua franca* for comparing semiconductor peers.
- A DCF this far out would be falsely precise — the FY29 targets are management's own, and the honest
  uncertainty lives in *what multiple the market assigns each business*, which EV/EBITDA isolates cleanly.
- We cross-check against management's **>$18 FY29 EPS** — see §7, which is not a flattering check.

**Why sum-of-the-parts (SOTP)?**
A blended company multiple would hide the whole thesis. The entire investment case is that a low-multiple
handset/licensing business is being diluted by higher-multiple automotive, IoT, and (especially)
data-center businesses. SOTP forces each segment to be valued on its *own* peer set:

| Segment | Base exit EV/EBITDA | Justification | vs. June |
|---|---:|---|:--|
| Handset + licensing | **8×** | Mature, cyclical, now with Apple in-housing partly realized and handsets −20% YoY. Licensing's ~70% margins keep it from going lower. | 9× → 8× |
| Automotive | **13×** | Design-win-backed and compounding at +61% YoY; auto-semi peers are cyclical (NXPI ~12.9× as of Aug 2026). Growth premium balances cyclicality. | unchanged |
| IoT (industrial, PC/compute, XR) | **13×** | Edge-AI structural growth, but running at +9% YoY against a target path needing ~+25%/yr. Trimmed toward the auto multiple. | 14× → 13× |
| **Data center** | **18×** | The swing factor. AI-inference peers trade rich (NVDA ~25.8×, AVGO ~35× as of Aug 2026), but QCOM's effort is early and customer-concentrated → a large haircut to peers. Bull pushes toward 25×; Bear now a POs-backed 11× rather than a "show-me" 10×. | unchanged |

**Scenario design** (*Base = management revenue targets*):
- **Base / Neutral:** management's FY29 segment revenue at face value; segment margins consistent with the
  reaffirmed 30%/70% QCT/QTL targets; base multiples above.
- **Bull:** full execution + a diversification re-rating — revenue modestly above target (data center ~$20B),
  higher margins, peer-like multiples (data center ~25×).
- **Bear:** execution shortfall — data center scales only to the order-backed floor (~$9B), auto/IoT below
  target, handset erosion continues at the Q3 rate, and input-cost inflation never normalizes.

**The run-rate bridge — what each segment must actually do.** This is the most useful thing the Q3
data adds, and it is printed by `model.py`:

| Segment | FY26E | Q3 FY26 run-rate | FY29 Base target | CAGR needed (from FY26E) |
|---|---:|---:|---:|---:|
| Handset + licensing | $29.6B | $25.5B | $20B | **−12%/yr** |
| Automotive | $5.7B | $6.4B | $10B | **+21%/yr** |
| IoT | $7.1B | $7.3B | $14B | **+25%/yr** |
| Data center | ~$0 | ~$0 | $15B | new build ($5B FY27 milestone) |

Read this as a scorecard. Automotive at +61% YoY is comfortably ahead of the +21% it needs. **IoT at
+9% YoY is the quiet problem** — it needs +25%/yr and is delivering a third of that, and no one is
talking about it because data center absorbs all the attention. The handset line needs to fall
*faster* than it already is for the mix goal to hold, which is not usually how targets are framed.

**From segments to a per-share PV:**
1. Segment EBITDA = segment revenue × segment EBITDA margin
2. Segment EV = segment EBITDA × segment exit multiple
3. Enterprise Value = Σ segment EV
4. FY29 equity value = EV − net debt ($7.0B)
5. **PV today = FY29 equity value ÷ (1 + r)^n**, with r = 10%, n = 3.08 yrs
6. PV per share = PV ÷ current diluted shares (1.069B; buybacks treated as roughly value-neutral upside, not modeled)

Full sensitivity tables (price vs. discount rate, and price vs. data-center multiple) are in the notebook.

---

## 7. The honest caveat: "Base = management targets" is only half true

The model takes management's FY29 **revenue** at face value but applies the **author's** segment
EBITDA margins. Those two halves do not agree, and `model.py` now prints the gap rather than hiding it:

| | FY29 EBITDA | Implied margin | Implied FY29 EPS |
|---|---:|---:|---:|
| This model's Base | $18.4B | 31% | **~$13.69** |
| Management's >$18 EPS target implies | ~$23.4B | 40% | >$18.00 |

The Base case runs **~$5B (22%) below** the profitability management's own EPS target implies. Note
that 40% would be a large expansion from the ~33% EBITDA margin Qualcomm is running at in FY26 — so
the model's scepticism is defensible — but it should be stated plainly rather than buried in a
"Base = management guidance" label.

**If management is right on both revenue *and* margins**, the same Base exit multiples give roughly
**$200/share (+18%)**. That number belongs in the range as much as the $148 does.

---

## 8. Repo contents

```
qcom-fy29-valuation/
├── README.md                  # this file — overview, comparison, methodology, results
├── UPDATE_RUNBOOK.md          # how to re-underwrite this model each earnings release
├── qcom_fy29_valuation.ipynb  # the model: assumptions → SOTP → scenarios → PV → charts → sensitivity
├── model.py                   # identical logic as a plain Python script (run without Jupyter)
├── tools/
│   └── extract_release.py     # fetch + decode a QCOM earnings-release PDF to text
├── requirements.txt
└── .gitignore
```

**Run it:**
```bash
python3 model.py                      # no dependencies — prints the scenario tables and both bridges

pip install -r requirements.txt       # for the notebook with charts
jupyter notebook qcom_fy29_valuation.ipynb
```

**Update it when Qualcomm reports** — see [`UPDATE_RUNBOOK.md`](UPDATE_RUNBOOK.md) for the full
procedure. Pull the primary source with:
```bash
python3 tools/extract_release.py 2026 q4 --sections
```
*Next release: Q4 + full-year FY2026, November 11, 2026 (after close) — an annual rollover.*

---

## 9. Sources

**Primary — the financials this run is anchored to:**
- **[Q3 FY2026 earnings release (July 29, 2026)](https://s204.q4cdn.com/645488518/files/doc_financials/2026/q3/FY2026-3rd-Quarter-Earnings-Release.pdf)** — the latest report used
- [Q2 FY2026 earnings release](https://s204.q4cdn.com/645488518/files/doc_financials/2026/q2/FY2026-2nd-Quarter-Earnings-Release.pdf) ·
  [Q1 FY2026 earnings release](https://s204.q4cdn.com/645488518/files/doc_financials/2026/q1/FY2026-1st-Quarter-Earnings-Release.pdf)
- [FY2025 Q4 / full-year earnings release](https://s204.q4cdn.com/645488518/files/doc_financials/2025/q4/FY2025-4th-Quarter-Earnings-Release.pdf) — prior-year comparison

**Forward targets:**
- Qualcomm June 24, 2026 Investor Day —
  [Business Wire](https://www.businesswire.com/news/home/20260624286521/en/Qualcomm-Accelerates-Diversification-with-Comprehensive-Strategy-for-Data-Center-and-Sees-Multiple-Inflection-Points-Over-the-Next-3-to-5-Years) ·
  [Futurum](https://futurumgroup.com/insights/qualcomms-investor-day-2026-agentic-and-ai-inference-to-drive-2x-revenue-growth-by-2030/)
- Qualcomm Nov 2024 Investor Day —
  [Qualcomm IR](https://investor.qualcomm.com/news-events/investor-events/events/event-details/2024/Investor-Day-2024-IoT-and-Automotive-Diversification-Update/default.aspx)
- [Futurum — Q3 FY26 analysis](https://futurumgroup.com/insights/qualcomm-q3-fy-2026-automotive-growth-offsets-handset-weakness/) (Apple share commentary, data-center ramp)

**Market data:**
- Peer multiples as of Aug 2026: [NVDA ~25.8×](https://www.gurufocus.com/term/enterprise-value-to-ebitda/NVDA) ·
  [NXPI ~12.9×](https://www.gurufocus.com/term/enterprise-value-to-ebitda/NXPI)
- Price & analyst targets: [stockanalysis.com/QCOM](https://stockanalysis.com/stocks/qcom/) ·
  [MarketBeat](https://www.marketbeat.com/stocks/NASDAQ/QCOM/forecast/)

*Market data gathered September 1, 2026. Refresh the `ASSUMPTIONS` block in `model.py` before reuse.*
