"""
Qualcomm (QCOM) — FY2029 sum-of-the-parts EV/EBITDA valuation.

Base case = management's June 24, 2026 Investor Day FY29 revenue targets, taken at
face value. Bull / Bear flex revenue, EBITDA margins, and segment exit multiples.
FY29 equity value is discounted back to a present value per share.

Re-underwritten on Q4 / full-year FY2026 actuals (see PROVENANCE below).

Pure standard-library Python — no dependencies. Run it with:

    python3 model.py

(The notebook qcom_fy29_valuation.ipynb imports this logic and adds charts/sensitivity.)

NOT investment advice. Every forward number is a management target or an author assumption.
"""

# ----------------------------------------------------------------------------------
# PROVENANCE — what this run is based on, and when it was made.
# ----------------------------------------------------------------------------------

from datetime import date, datetime

VALUATION_DATE = "November 21, 2026"
LATEST_REPORT = "Q4 / FY2026 — year ended September 27, 2026, reported November 4, 2026"
REPORT_URL = "https://investor.qualcomm.com/files/content_files/FY2026-4th-Quarter-Earnings-Release.pdf"
FILING_URL = "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000804328/29e9b475-f432-4e1d-83c3-c602cafb234b.pdf"
CALL_URL = "https://s204.q4cdn.com/645488518/files/content_files/Q4FY26-Earnings-Conference-Call_Transcript_11-5-26_Final.pdf"
PRICE_DATE = "November 20, 2026"
PRICE_URL = "https://stockanalysis.com/stocks/qcom/history/"

# ----------------------------------------------------------------------------------
# ASSUMPTIONS  — change anything here and re-run. This block is the whole model.
# ----------------------------------------------------------------------------------

# --- Market anchors ---
CURRENT_PRICE = 149.94  # Nov 20, 2026 regular-session close
SHARES_OUT    = 1.073   # billion; Q4 non-GAAP EPS reconciliation, not period-end shares
NET_DEBT      = (2.492 + 12.620) - (4.636 + 3.045)  # $B; restricted cash excluded
DISCOUNT_RATE = 0.10
YEARS_TO_FY29 = (date(2029, 9, 30) - datetime.strptime(VALUATION_DATE, "%B %d, %Y").date()).days / 365.25

# --- Completed FY2026 actual quarters ($M; GAAP total revenue) ------------------
FY26_QUARTERS = {
    #        total    QCT     QCT_EBT   QTL    QTL_EBT  handset   auto     iot
    "Q1":  (12_252, 10_613,   3_302,  1_592,   1_231,   7_824,   1_101,  1_688),
    "Q2":  (10_599,  9_076,   2_465,  1_382,     994,   6_024,   1_326,  1_726),
    "Q3":  ( 9_947,  8_504,   2_192,  1_278,     881,   5_086,   1_588,  1_830),
    "Q4":  (10_322,  9_015,   2_142,  1_304,     918,   5_137,   1_990,  1_888),
}
# Full-year as-reported figures take precedence over quarterly rounding.
FY26_REVENUE = 43.120
FY26_QCT_REVENUE, FY26_QTL_REVENUE = 37.208, 5.556
FY26_QCT_EBT, FY26_QTL_EBT = 10.101, 4.022
FY26_HANDSET, FY26_AUTOMOTIVE, FY26_IOT = 24.072, 6.004, 7.132
FY26_D_AND_A = 1.630

# New fiscal year: only Q1 is guided; this is NOT a full-year FY27 estimate.
# Release ranges: revenue $10.4-11.2B; QCT $9.0-9.6B; QTL $1.3-1.5B;
# non-GAAP EPS $2.15-2.35. Call: QCT EBT margin 20-22%, QTL 72-76%.
FY27_QUARTERS = {"Q1E": {"revenue": 10.8, "qct": 9.3, "qtl": 1.4,
                           "qct_ebt_margin": 0.21, "qtl_ebt_margin": 0.74,
                           "non_gaap_eps": 2.25}}
FY27_DATACENTER_TARGET = 5.0
Q1_FY27_DATACENTER_MIN = 0.650  # call says greater than this, not a midpoint

# EBITDA here = (QCT EBT + QTL EBT) - unallocated corporate + D&A, on a non-GAAP basis.
# The corporate bridge is calibrated to the one quarter with a reported non-GAAP EBT:
# Q3 FY26 segment EBT $3,073M vs non-GAAP EBT $2,693M -> $380M/qtr.
# Carried-forward proxy, not reported EBITDA: the gap also includes net financing
# and investment items; reported D&A can overlap non-GAAP amortization exclusions.
CORPORATE_PER_YEAR = 1.5    # $B
NON_GAAP_TAX_RATE = 0.13    # QCOM non-GAAP effective rate
NET_INTEREST_FY29 = 0.5     # $B, interest expense net of investment income

# FY2025 actuals (year ended Sept 28, 2025), for the YoY comparison. EBITDA is
# derived from the same bridge as FY26 actuals so the two years are directly comparable.
FY25_REVENUE = 44.284       # $B   as-reported full-year figures, per the FY25 Q4 release
FY25_QCT_EBT = 11.670       # $B   (summing the four quarters gives the same 11,670)
FY25_QTL_EBT = 4.043        # $B   (summing quarters gives 4,044 — as-reported wins)
FY25_D_AND_A = 1.602        # $B

# --- Scenario inputs ---------------------------------------------------------------
# Segments: handset (incl. licensing), automotive, iot (industrial+PC/compute+XR), datacenter
SEGMENTS = ["handset", "automotive", "iot", "datacenter"]

# Management targets refer to QCT, excluding QTL. $40B non-handset with handsets
# ~one-third of QCT implies ~$20B handset chips, PLUS licensing, not including it.
# IoT >$14B / DC >$15B are rounded lower bounds. Allocate the $1B residual pro rata
# to those two lines; this is an AUTHOR allocation, not additional company guidance.
MGMT_NONHANDSET_FY29 = 40.0
FY29_QTL_REVENUE = FY26_QTL_REVENUE  # author: flat licensing after renewals
BASE_IOT_REVENUE = 30.0 * 14 / 29
BASE_DC_REVENUE = 30.0 * 15 / 29
REVENUE = {
    "Bear": {"handset": 16 + FY29_QTL_REVENUE, "automotive": 9, "iot": 9, "datacenter": 9},
    "Base": {"handset": MGMT_NONHANDSET_FY29 / 2 + FY29_QTL_REVENUE,
             "automotive": 10, "iot": BASE_IOT_REVENUE, "datacenter": BASE_DC_REVENUE},
    "Bull": {"handset": 23 + FY29_QTL_REVENUE, "automotive": 13, "iot": 16, "datacenter": 20},
}

# FY29 EBITDA margins are author assumptions, not a reconciliation to QCT/QTL
# guidance. Bear is where "input-cost inflation never normalizes"
# lives — Q4 FY26 QCT EBT margin is 24%; Q1 FY27 guidance is 20-22%.
# Bear handset margin 32% -> 30%; Base/Bull held on the long-term target.
# Bear auto revenue 8 -> 9 on the ~$8B exit run-rate; IoT 10 -> 9 on +4% YoY.
# Data-center Bear remains a downside assumption, never a contracted floor.
EBITDA_MARGIN = {
    "Bear": {"handset": 0.30, "automotive": 0.22, "iot": 0.24, "datacenter": 0.18},
    "Base": {"handset": 0.38, "automotive": 0.28, "iot": 0.30, "datacenter": 0.25},
    "Bull": {"handset": 0.40, "automotive": 0.30, "iot": 0.33, "datacenter": 0.30},
}

# FY29 exit EV/EBITDA multiple per segment (see README section 6 for peer justification)
EXIT_MULTIPLE = {
    "Bear": {"handset":  7, "automotive": 10, "iot": 10, "datacenter": 11},
    "Base": {"handset":  8, "automotive": 13, "iot": 13, "datacenter": 18},
    "Bull": {"handset": 10, "automotive": 16, "iot": 18, "datacenter": 25},
}

# Probability weights for the blended fair value
WEIGHTS = {"Bear": 0.25, "Base": 0.50, "Bull": 0.25}

# Management's own FY29 non-GAAP EPS target, for the cross-check
MGMT_FY29_EPS = 18.0
FY29_SHARES = 1.02          # billion; author EPS-only share assumption, carried forward
FY29_D_AND_A = 1.8          # $B

# ----------------------------------------------------------------------------------
# TRAILING ANCHOR — derived from the reported quarters above
# ----------------------------------------------------------------------------------

def ebitda_from_segments(qct_ebt, qtl_ebt, d_and_a):
    """Non-GAAP EBITDA ($B) from reported segment EBT, via the corporate bridge."""
    return qct_ebt + qtl_ebt - CORPORATE_PER_YEAR + d_and_a


FY25_EBITDA = ebitda_from_segments(FY25_QCT_EBT, FY25_QTL_EBT, FY25_D_AND_A)


def fy26_actuals():
    """Completed FY26 as-reported annual figures ($B), not a FY27 forecast."""
    return {
        "revenue": FY26_REVENUE, "qct": FY26_QCT_REVENUE, "qtl": FY26_QTL_REVENUE,
        "ebitda": ebitda_from_segments(FY26_QCT_EBT, FY26_QTL_EBT, FY26_D_AND_A),
        "handset": FY26_HANDSET, "automotive": FY26_AUTOMOTIVE, "iot": FY26_IOT,
        "handset_plus_qtl": FY26_HANDSET + FY26_QTL_REVENUE,
    }


def q4_annualized():
    """Q4 FY26 segment revenue x4 ($B); a seasonal run-rate, not guidance."""
    _, _, _, qtl, _, handset, auto, iot = FY26_QUARTERS["Q4"]
    return {"handset": (handset + qtl) * 4 / 1000,
            "automotive": auto * 4 / 1000, "iot": iot * 4 / 1000,
            "datacenter": 0.0}


def run_rate_bridge():
    fy26 = fy26_actuals()
    actual = {"handset": fy26["handset_plus_qtl"], "automotive": fy26["automotive"],
              "iot": fy26["iot"], "datacenter": 0.0}
    run = q4_annualized()
    return [{"segment": s, "FY26 actual $B": actual[s], "Q4 run-rate": run[s],
             "FY29 Base": REVENUE["Base"][s],
             "CAGR from FY26": (REVENUE["Base"][s] / actual[s]) ** (1 / 3) - 1 if actual[s] else None,
             "CAGR from run-rate": (REVENUE["Base"][s] / run[s]) ** (1 / 3) - 1 if run[s] else None}
            for s in SEGMENTS]


# ----------------------------------------------------------------------------------
# ENGINE
# ----------------------------------------------------------------------------------

def value_scenario(name, discount_rate=None, datacenter_multiple=None):
    """Return (per-segment rows, summary dict) for one scenario."""
    rate = DISCOUNT_RATE if discount_rate is None else discount_rate
    rows = []
    total_rev = total_ebitda = total_ev = 0.0
    for seg in SEGMENTS:
        rev = REVENUE[name][seg]
        margin = EBITDA_MARGIN[name][seg]
        mult = (datacenter_multiple if seg == "datacenter" and datacenter_multiple is not None
                else EXIT_MULTIPLE[name][seg])
        ebitda = rev * margin
        ev = ebitda * mult
        rows.append((seg, rev, margin, ebitda, mult, ev))
        total_rev += rev
        total_ebitda += ebitda
        total_ev += ev

    blended_x = total_ev / total_ebitda
    equity_fy29 = total_ev - NET_DEBT
    price_fy29 = equity_fy29 / SHARES_OUT                       # undiscounted FY29 target price
    pv_equity = equity_fy29 / (1 + rate) ** YEARS_TO_FY29
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
        print(f"  {seg:<12}{rev:>8.2f}{margin:>8.0%}{ebitda:>9.2f}{mult:>7.0f}x{ev:>9.1f}")


def probability_weighted_pv():
    return sum(WEIGHTS[s] * value_scenario(s)[1]["pv_price"] for s in WEIGHTS)


def management_eps_value():
    """Illustrative allocation of EPS-implied EBITDA by revenue share."""
    mgmt_ebitda = eps_to_ebitda(MGMT_FY29_EPS)
    ev = sum(mgmt_ebitda * REVENUE["Base"][s] / sum(REVENUE["Base"].values())
             * EXIT_MULTIPLE["Base"][s] for s in SEGMENTS)
    return ((ev - NET_DEBT) / (1 + DISCOUNT_RATE) ** YEARS_TO_FY29) / SHARES_OUT


def print_bridge():
    print("\nRUN-RATE BRIDGE — FY26 actuals and Q4 annualized vs FY29 Base")
    print(f"  {'segment':<12}{'FY26 $B':>10}{'Q4 run-rate':>13}{'FY29 Base':>11}{'FY26 CAGR':>12}{'Q4 CAGR':>12}")
    for row in run_rate_bridge():
        a, b = row["CAGR from FY26"], row["CAGR from run-rate"]
        c1, c2 = (f"{a:+.0%}" if a is not None else "new"), (f"{b:+.0%}" if b is not None else "new")
        print(f"  {row['segment']:<12}{row['FY26 actual $B']:>10.1f}{row['Q4 run-rate']:>13.1f}"
              f"{row['FY29 Base']:>11.2f}{c1:>12}{c2:>12}")
    print("  Growth horizons: FY26 year-end to FY29 = 3 years; Q4 x4 is seasonal, not guidance.")
    print("  Data center: FY27 target $5B; Q1 FY27 >$0.65B; no separately reported FY26 revenue.")


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
    pv = management_eps_value()
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
    print("Base target mapping: QCT non-handset $40B + implied handset chips $20B + assumed QTL $5.556B.")
    print(f"Shares {SHARES_OUT}B | net debt ${NET_DEBT:.3f}B | "
          f"discount {DISCOUNT_RATE:.0%} over {YEARS_TO_FY29:.4f}y")
    print(f"FY26 actual (as reported): revenue ${fy26['revenue']:.1f}B "
          f"(QCT ${fy26['qct']:.1f}B / QTL ${fy26['qtl']:.1f}B), "
          f"EBITDA proxy ${fy26['ebitda']:.1f}B")
    print(f"FY25 actual: revenue ${FY25_REVENUE:.1f}B, EBITDA ${FY25_EBITDA:.1f}B  "
          f"-> revenue {fy26['revenue'] / FY25_REVENUE - 1:+.0%}, "
          f"EBITDA {fy26['ebitda'] / FY25_EBITDA - 1:+.0%} YoY")
    print(f"Trailing EV/EBITDA proxy on FY26 actuals at ${CURRENT_PRICE:.2f}: {trailing_x:.1f}x")
    print(bar)

    summaries = []
    for name in ["Bear", "Base", "Bull"]:
        rows, summary = value_scenario(name)
        summaries.append(summary)
        print(f"\n----- {name.upper()} -----")
        print_segment_table(rows)
        print(f"  => FY29: rev ${summary['rev']:.2f}B, EBITDA ${summary['ebitda']:.1f}B, "
              f"blended {summary['blended_x']:.1f}x, EV ${summary['ev']:.0f}B")
        print(f"     FY29 price ${summary['price_fy29']:.0f} | PV today ${summary['pv_price']:.0f} "
              f"| upside {summary['upside']:+.0%} | {YEARS_TO_FY29:.2f}y CAGR {summary['cagr']:+.0%}")

    print("\n" + bar)
    print("SCENARIO SUMMARY (PV today per share)")
    print(bar)
    print(f"  {'scenario':<10}{'FY29 rev':>10}{'FY29 EBITDA':>13}{'blended x':>11}"
          f"{'FY29 px':>10}{'PV today':>10}{'upside':>9}")
    for s in summaries:
        print(f"  {s['scenario']:<10}{s['rev']:>9.0f}B{s['ebitda']:>12.1f}B{s['blended_x']:>10.1f}x"
              f"{s['price_fy29']:>9.0f}{s['pv_price']:>10.0f}{s['upside']:>+9.0%}")

    blended_pv = probability_weighted_pv()
    print(f"\nProbability-weighted PV (Bear/Base/Bull = "
          f"{WEIGHTS['Bear']:.0%}/{WEIGHTS['Base']:.0%}/{WEIGHTS['Bull']:.0%}): "
          f"${blended_pv:.0f}/sh  ({blended_pv / CURRENT_PRICE - 1:+.0%} vs "
          f"${CURRENT_PRICE:.2f})")

    guide = FY27_QUARTERS["Q1E"]
    print(f"\nQ1 FY27 GUIDANCE MIDPOINTS ONLY: revenue ${guide['revenue']:.1f}B, "
          f"QCT ${guide['qct']:.1f}B, QTL ${guide['qtl']:.1f}B, EPS ${guide['non_gaap_eps']:.2f}.")
    print("FY27 milestones: data center $5B; non-handset growth >60%; no full-year total-revenue guide.")
    print_bridge()
    print_eps_bridge(next(s for s in summaries if s["scenario"] == "Base"))

    print(f"\nSource: {REPORT_URL}")
    print("NOT investment advice. Outputs are a function of the assumptions above.")


if __name__ == "__main__":
    main()
