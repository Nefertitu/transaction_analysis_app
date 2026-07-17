import pandas as pd

from src.reports import spending_by_workday


def test_spending_by_workday(sample_data_for_reports, capsys):
    """Проверяет, что функция выдает отчет о средних тратах
    в рабочий и выходной дни"""
    df = sample_data_for_reports
    result = spending_by_workday(df, "2020-04-20")
    expected_result = pd.DataFrame(
        {"Средние траты в рабочий день": [2546.02], "Средние траты в выходной день": [100.15]}
    )
    pd.testing.assert_frame_equal(result, expected_result)
    print(result)
    captured = capsys.readouterr()
    assert (
        captured.out == "   Средние траты в рабочий день  Средние траты в выходной день\n"
        "0                       2546.02                         100.15\n"
    )
