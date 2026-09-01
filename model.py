"""
Qualcomm (QCOM) — FY2029 sum-of-the-parts EV/EBITDA valuation.

Base case = management's June 24, 2026 Investor Day FY29 revenue targets, taken at
face value. Bull / Bear flex revenue, EBITDA margins, and segment exit multiples.
FY29 equity value is discounted back to a present value per share.

Re-underwritten on Q3 FY2026 actuals (see PROVENANCE below).

Pure standard-library Python — no dependencies. Run it with:

    python3 model.py

(The notebook qcom_fy29_valuation.ipynb mirrors this logic and adds charts/sensitivity.)

NOT investment advice. Every forward number is a management target or an author assumption.
"""

# ----------------------------------------------------------------------------------
# PROVENANCE — what this run is based on, and when it was made.
# ----------------------------------------------------------------------------------

VALUATION_DATE = "September 1, 2026"
LATEST_REPORT = "Q3 FY2026 — quarter ended June 28, 2026, reported July 29, 2026"
REPORT_URL = ("https://s204.q4cdn.com/645488518/files/doc_financials/2026/q3/"
              "FY2026-3rd-Quarter-Earnings-Release.pdf")
PRICE_DATE = "August 31, 2026"

# ----------------------------------------------------------------------------------
# ASSUMPTIONS  — change anything here and re-run. This block is the whole model.
# ----------------------------------------------------------------------------------

# --- Market anchors ---
CURRENT_PRICE = 170.48  # Aug 31, 2026 close (was $250 in the June 2026 run)
SHARES_OUT    = 1.069   # billion, Q3 FY26 diluted (1,069M)
NET_DEBT      = 7.0     # $B: total debt $15.27B less cash+securities $8.30B
DISCOUNT_RATE = 0.10    # required annual return
YEARS_TO_FY29 = 3.08    # Sept 1, 2026 -> FY29 year-end (late Sept 2029)

# --- Reported FY2026 quarters ($M, as filed; Q4 = guidance midpoint) --------------
# This is the "latest report" the valuation is anchored to. The trailing-year
# figures below are derived from these rows rather than hardcoded, so the anchor
# is verifiable against the earnings releases.
FY26_QUARTERS = {
    #        total    QCT     QCT_EBT   QTL    QTL_EBT  handset   auto     iot
    "Q1":  (12_252, 10_613,   3_302,  1_592,   1_231,   7_824,   1_101,  1_688),
    "Q2":  (10_599,  9_076,   2_465,  1_382,     994,   6_024,   1_326,  1_726),
    "Q3":  ( 9_947,  8_504,   2_192,  1_278,     881,   5_086,   1_588,  1_830),
    # Q4 FY26 guidance midpoints: revenue $9.7-10.5B, QCT $8.4-9.0B, QTL $1.2-1.4B.
    # Segment split and EBT margins held at the Q3 exit rate.
    "Q4E": (10_100,  8_700,   2_262,  1_300,     897,   5_100,   1_700,  1_900),
}
FY26_D_AND_A = 1.6          # $B, full year (9M reported $1,202M)

# EBITDA here = (QCT EBT + QTL EBT) - unallocated corporate + D&A, on a non-GAAP basis.
# The corporate bridge is calibrated to the one quarter with a reported non-GAAP EBT:
# Q3 FY26 segment EBT $3,073M vs reported non-GAAP EBT $2,693M -> $380M/qtr.
CORPORATE_PER_YEAR = 1.5    # $B
NON_GAAP_TAX_RATE = 0.13    # QCOM non-GAAP effective rate
NET_INTEREST_FY29 = 0.5     # $B, interest expense net of investment income

# FY2025 actuals (year ended Sept 28, 2025), for the YoY comparison. EBITDA is
# derived from the same bridge as FY26E so the two years are directly comparable.
FY25_REVENUE = 44.284       # $B
FY25_QCT_EBT = 11.670       # $B (3,246 + 2,857 + 2,671 + 2,896)
FY25_QTL_EBT = 4.044        # $B (1,158 +   929 +   942 + 1,015)
FY25_D_AND_A = 1.602        # $B

# --- Scenario inputs ---------------------------------------------------------------
# Segments: handset (incl. licensing), automotive, iot (industrial+PC/compute+XR), datacenter
SEGMENTS = ["handset", "automotive", "iot", "datacenter"]

# FY29 revenue ($B). BASE = management Investor-Day targets at face value (reaffirmed
# at the Q3 FY26 print). Bear/Bull re-cut on Q3 evidence — see README section 3.
REVENUE = {
    "Bear": {"handset": 16, "automotive":  8, "iot": 10, "datacenter":  9},
    "Base": {"handset": 20, "automotive": 10, "iot": 14, "datacenter": 15},  # mgmt FY29 targets
    "Bull": {"handset": 23, "automotive": 13, "iot": 16, "datacenter": 20},
}

# FY29 EBITDA margin. Base/Bull track the reaffirmed QCT ~30% / QTL ~70% op-margin
# targets (+ D&A addback). Bear is where "input-cost inflation never normalizes"
# lives — Q3 FY26 QCT EBT margin came in at 26% against that 30% target.
EBITDA_MARGIN = {
    "Bear": {"handset": 0.32, "automotive": 0.22, "iot": 0.24, "datacenter": 0.18},
    "Base": {"handset": 0.38, "automotive": 0.28, "iot": 0.30, "datacenter": 0.25},
    "Bull": {"handset": 0.40, "automotive": 0.30, "iot": 0.33, "datacenter": 0.30},
}

# FY29 exit EV/EBITDA multiple per segment (see README section 5 for peer justification)
EXIT_MULTIPLE = {
    "Bear": {"handset":  7, "automotive": 10, "iot": 10, "datacenter": 11},
    "Base": {"handset":  8, "automotive": 13, "iot": 13, "datacenter": 18},
    "Bull": {"handset": 10, "automotive": 16, "iot": 18, "datacenter": 25},
}

# Probability weights for the blended fair value
WEIGHTS = {"Bear": 0.25, "Base": 0.50, "Bull": 0.25}

# Management's own FY29 non-GAAP EPS target, for the cross-check
MGMT_FY29_EPS = 18.0
FY29_SHARES = 1.02          # $B shares after ~1.5%/yr net buyback shrink
FY29_D_AND_A = 1.8          # $B

# ----------------------------------------------------------------------------------
# TRAILING ANCHOR — derived from the reported quarters above
# ----------------------------------------------------------------------------------

def ebitda_from_segments(qct_ebt, qtl_ebt, d_and_a):
    """Non-GAAP EBITDA ($B) from reported segment EBT, via the corporate bridge."""
    return qct_ebt + qtl_ebt - CORPORATE_PER_YEAR + d_and_a


FY25_EBITDA = ebitda_from_segments(FY25_QCT_EBT, FY25_QTL_EBT, FY25_D_AND_A)


def fy26_actuals():
    """Roll the reported FY26 quarters up into a full-year estimate ($B)."""
    cols = list(zip(*FY26_QUARTERS.values()))
    total, qct, qct_ebt, qtl, qtl_ebt, handset, auto, iot = (sum(c) / 1000 for c in cols)
    ebitda = ebitda_from_segments(qct_ebt, qtl_ebt, FY26_D_AND_A)
    return {
        "revenue": total, "qct": qct, "qtl": qtl, "ebitda": ebitda,
        "handset": handset, "automotive": auto, "iot": iot,
        # the model's "handset" segment is handsets + licensing
        "handset_plus_qtl": handset + qtl,
    }


def q3_annualized():
    """Q3 FY26 segment revenue x4 — the exit run-rate ($B)."""
    _, _, _, qtl, _, handset, auto, iot = FY26_QUARTERS["Q3"]
    return {
        "handset": (handset + qtl) * 4 / 1000,
        "automotive": auto * 4 / 1000,
        "iot": iot * 4 / 1000,
        "datacenter": 0.0,
    }

# ----------------------------------------------------------------------------------
# ENGINE
# ----------------------------------------------------------------------------------

def value_scenario(name):
    """Return (per-segment rows, summary dict) for one scenario."""
    rows = []
    total_rev = total_ebitda = total_ev = 0.0
    for seg in SEGMENTS:
        rev = REVENUE[name][seg]
        margin = EBITDA_MARGIN[name][seg]
        mult = EXIT_MULTIPLE[name][seg]
        ebitda = rev * margin
        ev = ebitda * mult
        rows.append((seg, rev, margin, ebitda, mult, ev))
        total_rev += rev
        total_ebitda += ebitda
        total_ev += ev

    blended_x = total_ev / total_ebitda
    equity_fy29 = total_ev - NET_DEBT
    price_fy29 = equity_fy29 / SHARES_OUT                       # undiscounted FY29 target price
    pv_equity = equity_fy29 / (1 + DISCOUNT_RATE) ** YEARS_TO_FY29
    pv_price = pv_equity / SHARES_OUT                           # PV today per current share
    upside = pv_price / CURRENT_PRICE - 1
    cagr = (price_fy29 / CURRENT_PRICE) ** (1 / YEARS_TO_FY29) - 1

    summary = {
        "scenario": name,
        "rev": total_rev,
        "ebitda": total_ebitda,
        "blended_x": blended_x,
        "ev": total_ev,
        "price_fy29": price_fy29,
        "pv_price": pv_price,
        "upside": upside,
        "cagr": cagr,
    }
    return rows, summary


def ebitda_to_eps(ebitda):
    """Convert an FY29 EBITDA ($B) to an implied non-GAAP EPS."""
    ebt = ebitda - FY29_D_AND_A - NET_INTEREST_FY29
    return ebt * (1 - NON_GAAP_TAX_RATE) / FY29_SHARES


def eps_to_ebitda(eps):
    """Inverse of ebitda_to_eps — the EBITDA an EPS target implies."""
    ebt = eps * FY29_SHARES / (1 - NON_GAAP_TAX_RATE)
    return ebt + FY29_D_AND_A + NET_INTEREST_FY29


def print_segment_table(rows):
    print(f"  {'segment':<12}{'rev $B':>8}{'margin':>9}{'EBITDA':>9}{'exit x':>8}{'EV $B':>9}")
    for seg, rev, margin, ebitda, mult, ev in rows:
        print(f"  {seg:<12}{rev:>8.0f}{margin:>8.0%}{ebitda:>9.2f}{mult:>7.0f}x{ev:>9.1f}")


def print_bridge(fy26):
    """Q3 FY26 exit run-rate and FY26E vs the FY29 Base targets."""
    rr = q3_annualized()
    print("\n" + "=" * 80)
    print("RUN-RATE BRIDGE — what each segment has to do to hit the FY29 Base target")
    print("=" * 80)
    print(f"  {'segment':<12}{'FY26E $B':>10}{'Q3 run-rate':>13}{'FY29 Base':>11}"
          f"{'CAGR fr FY26E':>15}{'fr run-rate':>13}")
    fy26_seg = {
        "handset": fy26["handset_plus_qtl"],
        "automotive": fy26["automotive"],
        "iot": fy26["iot"],
        "datacenter": 0.0,
    }
    for seg in SEGMENTS:
        base = REVENUE["Base"][seg]
        f26, run = fy26_seg[seg], rr[seg]
        c1 = f"{(base / f26) ** (1 / 3) - 1:+.0%}" if f26 else "new"
        c2 = f"{(base / run) ** (1 / YEARS_TO_FY29) - 1:+.0%}" if run else "new"
        print(f"  {seg:<12}{f26:>10.1f}{run:>13.1f}{base:>11.0f}{c1:>15}{c2:>13}")
    print("  (datacenter starts from ~zero: mgmt guides $5B in FY27 on confirmed POs/wafer starts)")


def print_eps_bridge(base_summary):
    print("\n" + "=" * 80)
    print("EPS CROSS-CHECK — is the Base case consistent with mgmt's >$18 FY29 EPS?")
    print("=" * 80)
    implied_eps = ebitda_to_eps(base_summary["ebitda"])
    mgmt_ebitda = eps_to_ebitda(MGMT_FY29_EPS)
    print(f"  This model's Base FY29 EBITDA  ${base_summary['ebitda']:.1f}B "
          f"({base_summary['ebitda'] / base_summary['rev']:.0%} margin) "
          f"-> implied FY29 EPS ~${implied_eps:.2f}")
    print(f"  Mgmt FY29 EPS target           >${MGMT_FY29_EPS:.0f}      "
          f"-> requires EBITDA ~${mgmt_ebitda:.1f}B "
          f"({mgmt_ebitda / base_summary['rev']:.0%} margin)")
    print(f"  Gap: this model runs ${mgmt_ebitda - base_summary['ebitda']:.1f}B "
          f"({1 - base_summary['ebitda'] / mgmt_ebitda:.0%}) below the profitability "
          f"mgmt's own EPS target implies.")
    print("  => 'Base = management targets' is true of REVENUE, not of margins. The")
    print("     segment EBITDA margins here are the author's and are the more")
    print("     conservative half of the Base case.")

    # What the Base multiples give you if management is right on margins too.
    ev = sum(mgmt_ebitda * (REVENUE["Base"][s] / sum(REVENUE["Base"].values()))
             * EXIT_MULTIPLE["Base"][s] for s in SEGMENTS)
    pv = ((ev - NET_DEBT) / (1 + DISCOUNT_RATE) ** YEARS_TO_FY29) / SHARES_OUT
    print(f"\n  If mgmt hits BOTH revenue and EPS, at Base exit multiples "
          f"(revenue-weighted): ~${pv:.0f}/sh ({pv / CURRENT_PRICE - 1:+.0%})")


def main():
    bar = "=" * 80
    fy26 = fy26_actuals()
    trailing_x = (CURRENT_PRICE * SHARES_OUT + NET_DEBT) / fy26["ebitda"]

    print(bar)
    print("QUALCOMM (QCOM) — FY2029 SOTP EV/EBITDA VALUATION")
    print(bar)
    print(f"Valuation run     : {VALUATION_DATE}")
    print(f"Latest financials : {LATEST_REPORT}")
    print(f"Price anchor      : ${CURRENT_PRICE:.2f} ({PRICE_DATE} close)")
    print(bar)
    print(f"Shares {SHARES_OUT}B | net debt ${NET_DEBT}B | "
          f"discount {DISCOUNT_RATE:.0%} over {YEARS_TO_FY29}y")
    print(f"FY26E (9M actual + Q4 guide midpoint): revenue ${fy26['revenue']:.1f}B "
          f"(QCT ${fy26['qct']:.1f}B / QTL ${fy26['qtl']:.1f}B), "
          f"EBITDA ${fy26['ebitda']:.1f}B")
    print(f"FY25 actual: revenue ${FY25_REVENUE:.1f}B, EBITDA ${FY25_EBITDA:.1f}B  "
          f"-> revenue {fy26['revenue'] / FY25_REVENUE - 1:+.0%}, "
          f"EBITDA {fy26['ebitda'] / FY25_EBITDA - 1:+.0%} YoY")
    print(f"Trailing EV/EBITDA on FY26E at ${CURRENT_PRICE:.2f}: {trailing_x:.1f}x")
    print(bar)

    summaries = []
    for name in ["Bear", "Base", "Bull"]:
        rows, summary = value_scenario(name)
        summaries.append(summary)
        print(f"\n----- {name.upper()} -----")
        print_segment_table(rows)
        print(f"  => FY29: rev ${summary['rev']:.0f}B, EBITDA ${summary['ebitda']:.1f}B, "
              f"blended {summary['blended_x']:.1f}x, EV ${summary['ev']:.0f}B")
        print(f"     FY29 price ${summary['price_fy29']:.0f} | PV today ${summary['pv_price']:.0f} "
              f"| upside {summary['upside']:+.0%} | {YEARS_TO_FY29}y CAGR {summary['cagr']:+.0%}")

    print("\n" + bar)
    print("SCENARIO SUMMARY (PV today per share)")
    print(bar)
    print(f"  {'scenario':<10}{'FY29 rev':>10}{'FY29 EBITDA':>13}{'blended x':>11}"
          f"{'FY29 px':>10}{'PV today':>10}{'upside':>9}")
    for s in summaries:
        print(f"  {s['scenario']:<10}{s['rev']:>9.0f}B{s['ebitda']:>12.1f}B{s['blended_x']:>10.1f}x"
              f"{s['price_fy29']:>9.0f}{s['pv_price']:>10.0f}{s['upside']:>+9.0%}")

    blended_pv = sum(WEIGHTS[s["scenario"]] * s["pv_price"] for s in summaries)
    print(f"\nProbability-weighted PV (Bear/Base/Bull = "
          f"{WEIGHTS['Bear']:.0%}/{WEIGHTS['Base']:.0%}/{WEIGHTS['Bull']:.0%}): "
          f"${blended_pv:.0f}/sh  ({blended_pv / CURRENT_PRICE - 1:+.0%} vs "
          f"${CURRENT_PRICE:.2f})")

    print_bridge(fy26)
    print_eps_bridge(next(s for s in summaries if s["scenario"] == "Base"))

    print(f"\nSource: {REPORT_URL}")
    print("NOT investment advice. Outputs are a function of the assumptions above.")


if __name__ == "__main__":
    main()
