"""Source reconciliation and invariants for the dated financial model (stdlib only)."""
import json
from pathlib import Path
import unittest
import model as m


class ModelChecks(unittest.TestCase):
    def test_reported_revenue_reconciliation(self):
        quarters = list(m.FY26_QUARTERS.values())
        self.assertEqual(sum(q[0] for q in quarters[:3]), 32798)
        self.assertEqual(sum(q[0] for q in quarters), 43120)
        self.assertAlmostEqual(m.fy26_actuals()['revenue'], 43.120)
        self.assertEqual(set(m.FY26_QUARTERS), {'Q1', 'Q2', 'Q3', 'Q4'})
        self.assertEqual(set(m.FY27_QUARTERS), {'Q1E'})

    def test_annual_as_reported_wins_over_quarter_rounding(self):
        annual = [m.FY26_REVENUE, m.FY26_QCT_REVENUE, m.FY26_QCT_EBT,
                  m.FY26_QTL_REVENUE, m.FY26_QTL_EBT, m.FY26_HANDSET,
                  m.FY26_AUTOMOTIVE, m.FY26_IOT]
        deltas = [round(sum(q[i] for q in m.FY26_QUARTERS.values())-v*1000)
                  for i,v in enumerate(annual)]
        # Explicit source rounding differences in $M; never replace annual totals.
        self.assertEqual(deltas, [0, 0, 0, 0, 2, -1, 1, 0])
        self.assertAlmostEqual(m.fy26_actuals()['ebitda'], 14.253)
        self.assertEqual(m.FY25_QTL_EBT, 4.043)

    def test_management_target_mapping(self):
        base = m.REVENUE['Base']
        non_handset = sum(base[s] for s in ['automotive', 'iot', 'datacenter'])
        chips = base['handset'] - m.FY29_QTL_REVENUE
        self.assertAlmostEqual(non_handset, 40)
        self.assertAlmostEqual(chips / (chips + non_handset), 1/3)
        self.assertGreater(base['iot'], 14)
        self.assertGreater(base['datacenter'], 15)
        for s, chip_assumption in [('Bear',16), ('Base',20), ('Bull',23)]:
            self.assertAlmostEqual(m.REVENUE[s]['handset']-m.FY29_QTL_REVENUE,chip_assumption)

    def test_market_anchor_and_dates(self):
        self.assertAlmostEqual(m.NET_DEBT, 7.431)
        self.assertAlmostEqual(m.YEARS_TO_FY29, 1044/365.25)
        self.assertEqual(m.CURRENT_PRICE, 149.94)
        self.assertEqual(m.PRICE_DATE, 'November 20, 2026')
        self.assertEqual(m.SHARES_OUT, 1.073)

    def test_probability_precision_and_order(self):
        self.assertAlmostEqual(sum(m.WEIGHTS.values()), 1)
        values = [m.value_scenario(s)[1]['pv_price'] for s in m.WEIGHTS]
        self.assertTrue(values[0] < values[1] < values[2])
        exact = sum(m.WEIGHTS[s]*m.value_scenario(s)[1]['pv_price'] for s in m.WEIGHTS)
        rounded = sum(m.WEIGHTS[s]*round(m.value_scenario(s)[1]['pv_price']) for s in m.WEIGHTS)
        self.assertEqual(m.probability_weighted_pv(), exact)
        self.assertNotEqual(exact, rounded)

    def test_sensitivity_uses_engine_without_mutating_inputs(self):
        before = m.value_scenario('Base')[1]
        self.assertEqual(before, m.value_scenario('Base',m.DISCOUNT_RATE,m.EXIT_MULTIPLE['Base']['datacenter'])[1])
        self.assertGreater(m.value_scenario('Base',discount_rate=.08)[1]['pv_price'],before['pv_price'])
        self.assertLess(m.value_scenario('Base',datacenter_multiple=12)[1]['pv_price'],before['pv_price'])
        self.assertEqual(m.value_scenario('Base')[1],before)
        self.assertAlmostEqual(m.eps_to_ebitda(m.ebitda_to_eps(before['ebitda'])),before['ebitda'])

    def test_notebook_has_one_source_of_financial_inputs(self):
        notebook = json.loads((Path(__file__).resolve().parents[1]/'qcom_fy29_valuation.ipynb').read_text())
        source = '\n'.join(''.join(c['source']) for c in notebook['cells'] if c['cell_type']=='code')
        self.assertIn('import model',source)
        self.assertNotIn('def value_scenario',source)
        self.assertNotIn('REVENUE =',source)
        self.assertIn('m.probability_weighted_pv()',source)
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                self.assertIsNotNone(cell['execution_count'])
            for output in cell.get('outputs',[]):
                self.assertNotEqual(output.get('output_type'),'error')


if __name__ == '__main__':
    unittest.main()
