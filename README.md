# Qualcomm (QCOM) — FY2029 EV/EBITDA Valuation

A scenario-based, sum-of-the-parts **EV/EBITDA** valuation of Qualcomm anchored to the
financial targets management laid out at its **June 24, 2026 Investor Day**, discounted back
to a present value. Three scenarios — **Bear / Base / Bull** — with the Base case taking
management's FY2029 guidance at face value.

> **Not investment advice.** This is an educational modeling exercise. All forward figures are
> management targets or the author's assumptions, not facts. Verify every input before relying on it.

- 📓 Model & charts: [`qcom_fy29_valuation.ipynb`](qcom_fy29_valuation.ipynb)
- 🐍 Runnable script (same logic, no Jupyter needed): [`model.py`](model.py)
- 🎛️ Every assumption lives in one `ASSUMPTIONS` block — change a number, re-run, done.

---

## 1. Headline result

Valuation date: **~June 2026** · Discount (required return): **10%** · Horizon to FY29 year-end: **~3.25 yrs**

| Scenario | FY29 EV (SOTP) | Implied FY29 equity value / share | **PV today / share** | vs. price (~$250) |
|----------|---------------:|----------------------------------:|---------------------:|-------------------:|
| 🐻 **Bear**   | ~$105B | ~$96  | **~$71**  | **−72%** |
| 😐 **Base**   | ~$231B | ~$215 | **~$158** | **−37%** |
| 🐂 **Bull**   | ~$399B | ~$372 | **~$274** | **+10%** |
| Prob-weighted (25/50/25) | — | — | **~$165** | **−34%** |

**Read:** at ~$250 (post-Investor-Day, +15% pop), the market is already pricing the stock close to
the **Bull** case. The data-center build-out has to land more-or-less in full just to justify today's
price. The base case — management's own FY29 targets, valued on segment-appropriate multiples and
discounted at 10% — implies meaningful downside. The valuation is **dominated by the data-center
assumption** (revenue ramp × EBITDA margin × exit multiple); see the sensitivity section in the notebook.

*Figures are illustrative outputs of the assumptions below; re-run the notebook for exact numbers.*

---

## 2. Company overview (the 60-second version)

**What Qualcomm is.** A fabless (design-only) semiconductor company plus a patent-licensing business.
It designs the chips that connect and compute on the "edge" — phones, cars, PCs, headsets, industrial
gear — and it owns a foundational patent portfolio on the cellular standards (3G/4G/5G) that *every*
mobile device on Earth pays to use.

**How it makes money — two engines:**

| Segment | What it is | ~Share of FY25 revenue | Economics |
|---|---|---:|---|
| **QCT** (Qualcomm CDMA Technologies) | Chip sales: Snapdragon mobile SoCs + modems, RF front-end, **automotive** (Snapdragon Digital Chassis), **IoT/compute** (Snapdragon X PC chips, XR), and the new **data-center** AI/CPU effort | ~87% ($38.4B) | ~30% target operating margin |
| **QTL** (Qualcomm Technology Licensing) | Royalties on 3G/4G/5G patents — collected on essentially every smartphone sold | ~13% ($5.6B) | ~70% target operating margin (cash machine) |

**FY2025 actuals (year ended Sept 28, 2025):** Revenue **$44.3B** · EBITDA **~$14.0B** ·
Diluted shares **~1.07B** · roughly net-debt-neutral · strong free cash flow (~$12–13B).

**Management (as of 2026):** Cristiano Amon (President & CEO) · Akash Palkhiwala (EVP, CFO & COO) ·
Alex Rogers (President, QTL & Global Affairs) · Nakul Duggal (Group GM — Automotive, Industrial & Cloud).
*Confirm current titles on the IR site before citing.*

**Competition by arena:**
- **Handset SoC/modem:** MediaTek, **Apple** (in-housing its own modem — a structural threat to both QCT handset and QTL), Samsung LSI, Google Tensor, UNISOC
- **RF front-end:** Broadcom, Skyworks, Qorvo
- **Automotive:** NXP, Renesas, Texas Instruments, Mobileye, NVIDIA (auto)
- **PC / compute:** Intel, AMD, Apple Silicon, NVIDIA (Arm PC)
- **Data center / AI inference (new):** NVIDIA, AMD, Broadcom, Marvell, and hyperscaler in-house silicon (Google TPU, AWS Trainium/Graviton, Meta MTIA)

**Key risks the model is sensitive to:**
1. **Apple modem in-housing** — erodes a meaningful, high-margin slice of QCT handset + QTL over time.
2. **China concentration** — large share of revenue ties to Chinese OEMs / the China region.
3. **Handset cyclicality & maturity** — the core ~⅓ of revenue is low-growth and terminal-risk-laden.
4. **Data-center execution & customer concentration** — the entire bull thesis. Early, unproven, and
   anchored on a small number of customers (e.g., the Meta relationship highlighted at the 2026 day).
5. **Licensing/legal** — QTL renewals and the Arm licensing dispute.

**Sell-side snapshot (post–June 2026 Investor Day):** ratings cluster around **Hold/Mixed** with a very
wide target range as analysts digest the data-center pivot — from **~$150** (Barclays, Underweight) to
**~$300** (Benchmark), with a cluster of raises into the **$235–$265** band (JPMorgan, RBC, Rosenblatt,
DZ Bank, UBS). The dispersion itself is the story: nobody agrees on what the data-center business is worth.

---

## 3. Investor Day comparison — Nov 2024 vs. June 2026 (FY2029 targets)

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
| TAM | ~$900B by 2030 | reaffirmed/expanded with AI-inference | — |

**A subtle tell:** non-handset revenue roughly doubled ($22B → $40B), yet the FY29 **EPS** target barely
moved (~$18 → >$18). That implies the incremental data-center revenue is being modeled at **lower
incremental margin** (and/or assumes heavier reinvestment) than the legacy mix — which is exactly why
the model treats the data-center exit multiple, not just its revenue, as the key swing variable.

---

## 4. Valuation methodology & why these choices

**Why EV/EBITDA (not P/E or DCF as the headline)?**
- EBITDA is capital-structure- and tax-neutral, which matters for a company actively re-shaping its mix
  and balance sheet, and it's the *lingua franca* for comparing semiconductor peers.
- A DCF this far out would be falsely precise — the FY29 targets are management's own, and the honest
  uncertainty lives in *what multiple the market assigns each business*, which EV/EBITDA isolates cleanly.
- We still cross-check against management's **>$18 FY29 EPS** in the notebook.

**Why sum-of-the-parts (SOTP)?**
A blended company multiple would hide the whole thesis. The entire investment case is that a low-multiple
handset/licensing business is being diluted by higher-multiple automotive, IoT, and (especially)
data-center businesses. SOTP forces each segment to be valued on its *own* peer set:

| Segment | Base exit EV/EBITDA | Justification |
|---|---:|---|
| Handset + licensing | **9×** | Mature, cyclical, Apple-in-housing & China terminal risk. Below QCOM's historical ~11–15× to reflect structural handset decline; licensing's 70% margins keep it from going lower. |
| Automotive | **13×** | Design-win-backed (~$65B pipeline) but auto-semi peers (NXP ~14×) are cyclical; growth premium balances cyclicality. |
| IoT (industrial, PC/compute, XR) | **14×** | Edge-AI structural growth, mixed maturity. Between auto and data center. |
| **Data center** | **18×** | The swing factor. AI-inference peers trade rich (NVIDIA ~19–30×, Broadcom ~24–37×), but QCOM's effort is **early, unproven, and customer-concentrated** → a large haircut to peers. Bull pushes toward 25×; Bear collapses it to a "show-me" 10×. |

**Scenario design** (per the chosen approach — *Base = management target*):
- **Base / Neutral:** management's FY29 segment revenue at face value; segment margins consistent with the
  30%/70% QCT/QTL targets; base multiples above.
- **Bull:** full execution + a diversification re-rating — revenue modestly above target (data center ~$20B),
  higher margins, peer-like multiples (data center ~25×).
- **Bear:** execution shortfall — data center largely fails to scale (~$7B), auto/IoT ~80–85% of target,
  handset flat-to-down, compressed margins and "show-me" multiples.

**From segments to a per-share PV:**
1. Segment EBITDA = segment revenue × segment EBITDA margin
2. Segment EV = segment EBITDA × segment exit multiple
3. Enterprise Value = Σ segment EV
4. FY29 equity value = EV − net debt
5. **PV today = FY29 equity value ÷ (1 + r)^n**, with r = 10%, n ≈ 3.25 yrs
6. PV per share = PV ÷ current diluted shares (buybacks treated as roughly value-neutral upside, not modeled)

Full sensitivity tables (price vs. discount rate, and price vs. data-center multiple) are in the notebook.

---

## 5. Repo contents

```
qcom-fy29-valuation/
├── README.md                  # this file — overview, comparison, methodology, results
├── qcom_fy29_valuation.ipynb  # the model: assumptions → SOTP → scenarios → PV → charts → sensitivity
├── model.py                   # identical logic as a plain Python script (run without Jupyter)
├── requirements.txt
└── .gitignore
```

**Run it:**
```bash
pip install -r requirements.txt
python3 model.py                      # prints the scenario tables
# or, for the full notebook with charts:
jupyter notebook qcom_fy29_valuation.ipynb
```

---

## 6. Sources

- Qualcomm June 24, 2026 Investor Day — press release & coverage:
  [Business Wire](https://www.businesswire.com/news/home/20260624286521/en/Qualcomm-Accelerates-Diversification-with-Comprehensive-Strategy-for-Data-Center-and-Sees-Multiple-Inflection-Points-Over-the-Next-3-to-5-Years) ·
  [CNBC](https://www.cnbc.com/2026/06/24/qualcomm-data-center-cpu-meta.html) ·
  [Futurum](https://futurumgroup.com/insights/qualcomms-investor-day-2026-agentic-and-ai-inference-to-drive-2x-revenue-growth-by-2030/) ·
  [TipRanks](https://www.tipranks.com/news/qualcomm-stock-qcom-rallies-on-solid-fy29-revenue-targets-meta-platforms-deal)
- Qualcomm Nov 2024 Investor Day:
  [Qualcomm IR](https://investor.qualcomm.com/news-events/investor-events/events/event-details/2024/Investor-Day-2024-IoT-and-Automotive-Diversification-Update/default.aspx) ·
  [Paolo Pescatore recap](https://paolopescatore.substack.com/p/qualcomm-investor-day-2024)
- FY2025 results: [Qualcomm Q4/FY25 earnings release](https://www.qualcomm.com/news/releases/2025/11/qualcomm-announces-fourth-quarter-and-fiscal-2025-results) ·
  [FY25 earnings PDF](https://s204.q4cdn.com/645488518/files/doc_financials/2025/q4/FY2025-4th-Quarter-Earnings-Release.pdf)
- Peer multiples: [valueinvesting.io (NVDA/AVGO/NXPI)](https://valueinvesting.io/NVDA/valuation/ev_ebitda-multiples)
- Price & analyst targets: [stockanalysis.com/QCOM](https://stockanalysis.com/stocks/qcom/) ·
  [MarketBeat](https://www.marketbeat.com/stocks/NASDAQ/QCOM/forecast/)

*Source figures were gathered around June 2026 and should be refreshed before reuse.*
