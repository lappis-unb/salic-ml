from core.finance.financial_metrics import FinancialMetrics

fm = None

def test_init():
    fm = FinancialMetrics()
    print(fm.datasets)
    print(fm.metrics)
    assert False
