import pandas as pd

from src.reports import spending_by_workday
# from src.utils import get_decorator, configure_logging


def test_spending_by_workday(sample_data_for_reports):
    """Проверяет, что функция выдает отчет о средних тратах
    в рабочий и выходной дни"""
    df = sample_data_for_reports
    result = spending_by_workday(df, "2020-04-20")
    expected_result = pd.DataFrame({"Средние траты в рабочий день": [2546.02],  "Средние траты в выходной день": [100.15]})
    pd.testing.assert_frame_equal(result, expected_result)
