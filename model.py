"""
Qualcomm (QCOM) — FY2029 sum-of-the-parts EV/EBITDA valuation.

Base case = management's June 24, 2026 Investor Day FY29 targets, taken at face value.
Bull / Bear flex revenue, EBITDA margins, and segment exit multiples.
FY29 equity value is discounted back to a present value per share.

Pure standard-library Python — no dependencies. Run it with:

    python3 model.py

(The notebook qcom_fy29_valuation.ipynb mirrors this logic and adds charts/sensitivity.)

NOT investment advice. Every forward number is a management target or an author assumption.
"""

# ----------------------------------------------------------------------------------
# ASSUMPTIONS  — change anything here and re-run. This block is the whole model.
# ----------------------------------------------------------------------------------

# --- Market anchors (refresh before reuse; gathered ~June 2026) ---
CURRENT_PRICE = 250.0   # QCOM post-Investor-Day (~$222 on Jun 23 pre-day, +~15% pop)
SHARES_OUT    = 1.07    # billion, diluted (FY25)
NET_DEBT      = 1.5     # $B, roughly net-debt-neutral (cash+investments ~ debt)
DISCOUNT_RATE = 0.10    # required annual return
YEARS_TO_FY29 = 3.25    # ~mid-2026 -> FY29 year-end (Sept 2029)

# FY2025 actuals, for context / multiple sanity checks
FY25_REVENUE = 44.3     # $B
FY25_EBITDA  = 14.0     # $B

# --- Scenario inputs ---------------------------------------------------------------
# Segments: handset (incl. licensing), automotive, iot (industrial+PC/compute+XR), datacenter
SEGMENTS = ["handset", "automotive", "iot", "datacenter"]

# FY29 revenue ($B). BASE = management Investor-Day targets at face value.
REVENUE = {
    "Bear": {"handset": 18, "automotive":  8, "iot": 11, "datacenter":  7},
    "Base": {"handset": 20, "automotive": 10, "iot": 14, "datacenter": 15},  # mgmt FY29 targets
    "Bull": {"handset": 22, "automotive": 12, "iot": 16, "datacenter": 20},
}

# FY29 EBITDA margin (consistent with QCT ~30% / QTL ~70% op-margin targets + D&A addback)
EBITDA_MARGIN = {
    "Bear": {"handset": 0.35, "automotive": 0.24, "iot": 0.26, "datacenter": 0.18},
    "Base": {"handset": 0.38, "automotive": 0.28, "iot": 0.30, "datacenter": 0.25},
    "Bull": {"handset": 0.40, "automotive": 0.30, "iot": 0.33, "datacenter": 0.30},
}

# FY29 exit EV/EBITDA multiple per segment (see README §4 for peer justification)
EXIT_MULTIPLE = {
    "Bear": {"handset":  7, "automotive": 10, "iot": 10, "datacenter": 10},
    "Base": {"handset":  9, "automotive": 13, "iot": 14, "datacenter": 18},
    "Bull": {"handset": 11, "automotive": 16, "iot": 18, "datacenter": 25},
}

# Probability weights for the blended fair value
WEIGHTS = {"Bear": 0.25, "Base": 0.50, "Bull": 0.25}

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


def print_segment_table(rows):
    print(f"  {'segment':<12}{'rev $B':>8}{'margin':>9}{'EBITDA':>9}{'exit x':>8}{'EV $B':>9}")
    for seg, rev, margin, ebitda, mult, ev in rows:
        print(f"  {seg:<12}{rev:>8.0f}{margin:>8.0%}{ebitda:>9.2f}{mult:>7.0f}x{ev:>9.1f}")


def main():
    bar = "=" * 80
    trailing_x = (CURRENT_PRICE * SHARES_OUT + NET_DEBT) / FY25_EBITDA
    print(bar)
    print("QUALCOMM (QCOM) — FY2029 SOTP EV/EBITDA VALUATION")
    print(f"Price ${CURRENT_PRICE:.0f} | shares {SHARES_OUT}B | net debt ${NET_DEBT}B | "
          f"discount {DISCOUNT_RATE:.0%} over {YEARS_TO_FY29}y")
    print(f"FY25 context: revenue ${FY25_REVENUE}B, EBITDA ${FY25_EBITDA}B "
          f"(trailing EV/EBITDA ~{trailing_x:.1f}x)")
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
              f"| upside {summary['upside']:+.0%} | 3.25y CAGR {summary['cagr']:+.0%}")

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
          f"${blended_pv:.0f}/sh  ({blended_pv/CURRENT_PRICE-1:+.0%} vs ${CURRENT_PRICE:.0f})")
    print(f"\nCross-check vs mgmt FY29 non-GAAP EPS target (>$18): "
          f"at ${CURRENT_PRICE:.0f} that's ~{CURRENT_PRICE/18:.1f}x FY29 EPS.")
    print("\nNOT investment advice. Outputs are a function of the assumptions above.")


if __name__ == "__main__":
    main()
