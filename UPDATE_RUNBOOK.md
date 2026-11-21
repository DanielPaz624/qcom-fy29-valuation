# Update runbook — refreshing this valuation each earnings release

The procedure for re-underwriting the model when Qualcomm reports. Following it makes each run
**systematic** (same steps, same sources every time) and **traceable** (you can always tell which
report a number came from, when it was run, and what changed since the last one).

**Current run: November 21, 2026, on Q4 / full-year FY2026 reported November 4.**
Next update: Q1 FY2027, when reported. Verify the date on Qualcomm IR; do not carry forward an unconfirmed date.

---

## 1. The prompt

Paste this into Claude Code from the repo directory. Change only the quarter label:

```
Update the QCOM FY29 valuation for Q1 FY2027.
Follow UPDATE_RUNBOOK.md in the repo.
Price anchor: last close before today.
```

That is the whole prompt, every quarter, forever. All the detail lives in this file, so the
procedure can improve without you having to remember a longer prompt.

**Optional modifiers**, appended when you want them:

| Add this line | Effect |
|---|---|
| `Anchors only — don't re-underwrite.` | Refresh price/shares/net debt/horizon and stop. Isolates "what the market did" from "what I assumed." |
| `Re-weight the scenarios.` | Opens the 25/50/25 probability weights for revision (otherwise they are carried forward). |
| `Also refresh peer multiples.` | Re-checks NVDA / AVGO / NXPI EV/EBITDA and post-print analyst targets before re-cutting exit multiples. |
| `Skip the notebook.` | Updates `model.py` + README only. Use when you want the number fast; the notebook then needs a follow-up run. |

---

## 2. Pick the mode

**Quarterly update — Q1, Q2, Q3.** Move the newly reported quarter into the current `FY__QUARTERS`
block in `model.py`, replacing the estimate that stood in for it, and refresh the trailing `Q_E`
guidance row from the new outlook.

**Annual rollover — Q4 + full year.** The November 2026 run completed this rollover.

1. Replace Q4 guidance with Q4 actuals in the completed-year quarterly history.
2. Record the **as-reported full-year** revenue, QCT/QTL revenue and EBT, stream
   revenue and D&A. Annual figures take precedence over quarterly rounding (up to $2M in FY26 QTL EBT).
3. Open the new year's quarterly block with Q1 guidance only. **Do not sum a lone
   Q1 guidance row and present it as a full-year estimate.** Retain the completed
   year's actuals as the trailing valuation and growth anchor until a properly
   supported full-year estimate exists. A later FY27 quarter replaces the guidance
   row with actuals and adds the next guidance row; labels must identify coverage.
4. Preserve FY25 figures for the historical comparison. Advance helper names only
   when the period they actually represent changes; `fy26_actuals()` still means
   completed FY26, not a renamed single-quarter FY27 forecast.
5. Keep new QCT data-center revenue separate from the other streams when reported;
   do not infer a historical data-center zero from absent separate disclosure.

The FY27 checkpoints are $5B data-center revenue and >60% non-handset growth,
reiterated on the November 4 release. Q1 guidance is not full-year total-revenue
or EPS guidance. Check whether the milestones land, change, or are withdrawn.

---

## 3. Pull the primary source

```bash
python3 tools/extract_release.py 2027 q1 --sections     # the blocks the model needs
python3 tools/extract_release.py 2027 q1                # full text, if a section is missing
```

Start with the earnings release. Use the company-hosted call transcript for guidance or target detail not in the release, and record both URLs. Never take a figure from a news summary
when the filing has it.

| Figure needed | Section it appears in |
|---|---|
| Total revenue; GAAP + non-GAAP EPS; non-GAAP EBT; **diluted shares** | headline table + GAAP-to-non-GAAP reconciliation |
| QCT revenue & EBT, QTL revenue & EBT (and EBT margins) | Segment Results |
| Handsets / Automotive / IoT revenue | QCT Revenue Streams |
| Cash, marketable securities, short- + long-term debt | Balance sheet — **exclude restricted cash** |
| Depreciation & amortization | Cash-flow statement |
| Year-to-date revenue | Statements of Operations — this is the **reconciliation gate**, §8 |
| Next-period guidance | Business Outlook / Current Guidance |

From outside the release: the **last close and its date**, and — only if re-cutting multiples —
current NVDA / AVGO / NXPI EV/EBITDA and post-print analyst price targets.

> If the extractor fails, it says so loudly rather than emitting garbage. It auto-detects the font
> offset these PDFs use; if the encoding ever changes, it prints its candidate scores so you can
> diagnose it. `--url` overrides the URL pattern if Qualcomm renames their files.
>
> **FY26 Q4 exception:** the conventional q4cdn path returned HTML and the IR endpoint
> blocked direct downloads. The SEC-filed copy works. It uses standard PDF fonts:
> install the optional `PyPDF2>=2,<4` dependency and run with that interpreter:
>
> ```bash
> python3.7 tools/extract_release.py --url https://d18rn0p25nwr6d.cloudfront.net/CIK-0000804328/29e9b475-f432-4e1d-83c3-c602cafb234b.pdf --sections
> ```
>
> The extractor now falls back to PyPDF2 when CID streams are absent. If sections
> are missing, read full text; do not substitute a search-summary headline.

---

## 4. Update `model.py`

Walk the `PROVENANCE` and `ASSUMPTIONS` blocks top to bottom. Routine anchor changes belong in those blocks. A fiscal rollover or a documented
modeling correction may also require helper and display changes.

**Provenance** — this is what makes a run traceable, so do it first, not last:
`VALUATION_DATE`, `LATEST_REPORT` (quarter, period-end date, report date), `REPORT_URL`, `PRICE_DATE`.

**Market anchors:**

| Constant | How to derive it |
|---|---|
| `CURRENT_PRICE` | Last close before the valuation date. Record the date in `PRICE_DATE`. |
| `SHARES_OUT` | **Diluted** share count from the EPS reconciliation — *not* the balance-sheet "issued and outstanding" figure. They differ by ~12M. |
| `NET_DEBT` | (short-term + long-term debt) − (cash + marketable securities). Exclude **restricted** cash — it is committed to acquisition payments. |
| `YEARS_TO_FY29` | Days from the valuation date to FY29 year-end (~Sept 30, 2029) ÷ 365.25. |
| `DISCOUNT_RATE` | Carried forward unless you deliberately change it — if you do, log it (§7). |

```bash
# YEARS_TO_FY29 for a given valuation date
python3 -c "import datetime as d; print(round((d.date(2029,9,30)-d.date(2026,11,12)).days/365.25, 2))"
```

**Quarterly block:** per the mode in §2. The `#` comment above the guidance row should always record
the actual guidance *range*, not just the midpoint you used.

---

## 5. Re-underwrite the scenarios

The judgment step, and the only one that can't be mechanical.

> ### The one locked rule
> **Base-case FY29 revenue = management's stated targets, at face value, with explicit mappings where targets are rounded or expressed as a mix.** Base carries management's
> view; Bear and Bull carry yours. If management revises the FY29 targets, Base moves with them — but
> Base is never adjusted because you disagree with it. This is what makes "the Base case" mean
> something specific, and it is what the README's §7 caveat is honest about.
>
> Everything else — weights, discount rate, margins, multiples, the EBITDA basis — is yours to change
> on evidence. **But anything you change must be logged (§7).** Traceability here comes from the log,
> not from the lock.

**Mapping established November 2026:** the $40B non-handset target is QCT revenue.
Approximately one-third handset mix implies $20B handset **chips**, excluding QTL.
The model adds a separate, author-assumed flat $5.556B of licensing to all scenarios'
handset-chip assumptions. Automotive stays $10B. The $30B remainder is allocated
between IoT and data center in ratio 14:15 to respect the >$14B / >$15B thresholds.
Do not silently revert to the prior $39B sum or call the licensing add-on company
guidance. Revisit the allocation and QTL assumption on evidence, logging any change.

Start by running `python3 model.py` *before* touching anything and reading the **run-rate bridge** it
prints. It shows the CAGR each segment now needs to reach its FY29 target. That table, more than the
headline, is what should drive changes.

Then four questions:

1. **Trajectory.** For each segment, did the quarter move it toward or away from the FY29 path? A
   segment consistently below the required CAGR is evidence for the Bear revenue case, not just noise.
2. **Structural vs. cyclical.** Did a customer, competitive position, or margin regime change
   permanently? *Structural changes move exit multiples. Cyclical ones move Bear/Bull revenue.*
   Keeping these separate is what stops the model drifting with sentiment.
3. **Did management reaffirm or revise the FY29 targets?** Reaffirmed → Base holds, and any
   deterioration belongs in Bear. Revised → Base moves with them, and say so prominently.
4. **Does the Bear floor still hold?** Evidence can raise a floor as well as lower it — order
   backlogs, signed customers and shipped volume are floor-raisers.

**Worked example — the Q3 FY2026 cycle**, showing all four in action:

| Evidence | Question | What moved |
|---|---|---|
| Apple iPhone share guided "materially below" the prior ~20% | 2 — structural | Handset **exit multiple** 9× → 8× (not a revenue tweak: the business is permanently smaller) |
| Memory/wafer costs put QCT EBT at 26% vs a 30% target, but mgmt **reaffirmed** 30%/70% for FY29 | 3 — reaffirmed | **Bear margins only.** Base and Bull held, because management restated the target |
| Data center: hyperscaler POs, wafer starts, new $5B FY27 milestone | 4 — floor raised | Bear revenue $7B → $9B, Bear multiple 10× → 11× |
| IoT growing +9% against the ~+25%/yr its target needs | 1 — trajectory | IoT Base multiple 14× → 13×, Bear revenue 11 → 10 |

---

## 6. Notebook

The notebook imports `model.py` and reloads it in its first code cell. Edit financial
inputs and calculations in the Python module only, then re-execute **with outputs committed**
so the charts render on GitHub. Keep full precision until presentation; charts and
sensitivities must call the shared engine rather than reimplement valuation formulas.

```bash
MPLCONFIGDIR=/tmp/qcom-matplotlib IPYTHONDIR=/tmp/qcom-ipython JUPYTER_RUNTIME_DIR=/tmp/qcom-jupyter python3.7 -c "
import nbformat; from nbclient import NotebookClient
p='qcom_fy29_valuation.ipynb'; nb=nbformat.read(p, as_version=4)
NotebookClient(nb, timeout=300, kernel_name='python3').execute(); nbformat.write(nb, p)
print('ok')"
```

**Environment gotchas on this machine** (they cost an hour the first time):

- Use **`python3.7`** for the notebook — it is the only interpreter here with pandas/matplotlib. The
  default `python3` has none of them. `model.py` itself is stdlib-only and runs on any version.
- Use **`nbclient`**, not `nbconvert` — the `jupyter nbconvert` entry point is broken here.
- There is no **poppler**, so `pdftotext`/`pdftoppm` are unavailable. That is why
  `tools/extract_release.py` exists.
- Watch for **rounding drift**: the notebook must not read a rounded value back out of `summary` for
  downstream math, or it will disagree with `model.py` in the last decimal.

---

## 7. Update the README

- **Header block** — valuation date, latest report, price anchor. The first thing a reader sees.
- **§1 Headline result** — regenerate the table, and rewrite the "Read:" paragraph. If the conclusion
  has changed, say so plainly rather than editing around it.
- **§2 What changed** — replace with this quarter's. Include the quarter's table, the segment trend,
  and the two or three read-throughs that actually drove scenario changes.
- **§3 Revision history — append a row, never overwrite one.** This is the audit trail.
- **§4** FY figures, risk list, and the **sell-side snapshot** (which goes stale fast).
- **§9 Sources** — add the new release; keep the prior ones.

**Log any convention change.** If you altered the probability weights, the discount rate, or the
EBITDA basis, add a line under the revision-history table saying what changed and why. Without that,
a future reader cannot tell whether fair value moved because the business changed or because the
method did.

---

## 8. Verification gates

All of these before committing.

1. Run `python3 -m unittest discover -s tests -v`. **The reconciliation gate.** Quarterly revenue rows must sum to the year-to-date figure printed in
   the release. *This caught a $188M error last cycle* — two quarterly totals had been taken from
   press-release headlines ("$12.3 billion") rather than the filing ($12,252M).
2. `python3 model.py` runs on **stdlib alone** — no imports beyond the standard library.
3. **Notebook equals `model.py`.** Compare the scenario summary line by line. Any disagreement is a
   bug in one of them, usually rounding drift.
4. **Every headline number in the README appears in `model.py` output or is derived from its unrounded summary.** The README must not assert a
   valuation figure the model does not produce. Source tables must be checked against the filings.
5. **Grep for the previous run's values** to catch leftovers — old price, old horizon, old net debt,
   old analyst-target range.
6. **Look at the charts.** Not "did they render" — open them. Check that guidance/estimate periods
   stay visually distinguished from actuals (dashed line, hatched bar), and that no labels collide.

---

## 9. Commit

Fixed shape, so `git log` reads as a valuation history:

```
Re-underwrite FY29 valuation on <Q_ FY____> actuals

<what the quarter said — the two or three facts that mattered>

<anchors: price, shares, net debt, horizon — from -> to>

<scenario changes, each with the evidence that drove it>

<result: Base PV and prob-weighted PV, before -> after>
```

Then push to `master`. Keep `.claude/` and `tools/.cache/` out of the repo.

---

## 10. Terminal condition — read this by FY2028

This model discounts a FY29 exit back to today. As the horizon shortens the exercise quietly
degrades: with ~1 year to go, "the FY29 target" is no longer a long-range thesis to discount but
near-term guidance, and a sum-of-the-parts on exit multiples stops being the right frame.

By the **FY2028 annual rollover** (roughly November 2028, `YEARS_TO_FY29` ≈ 0.9), stop and decide
deliberately rather than re-running the procedure out of habit. The realistic options are to roll the
target year forward (FY32, needing new management targets), switch to a near-term earnings-multiple
frame, or close the model out and write up how the FY29 call actually landed — which, given the
revision history, would be the most interesting output of all.
