from indicators.fetch_complexity import pre_fetch_financial_complexity
from indicators.financial_metrics_instance import load_fetched_indicators

print("Attempting to fetch indicators")
pre_fetch_financial_complexity()
print("Indicators fetched")

print("Attempting to load indicators")
load_fetched_indicators()
print("Indicators loaded")