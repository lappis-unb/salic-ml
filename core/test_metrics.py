from core.finance.financial_metrics import FinancialMetrics

fm = None

def test_init():
    print('starting fm')
    fm = FinancialMetrics()
    print('fm loaded')
    print(fm.datasets)
    print(fm.metrics)
    assert True
