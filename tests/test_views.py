import pytest
import pandas as pd

from src.utils import get_choice_data
from src.views import get_event_page


@pytest.mark.parametrize(
    "date, period",
    [
        ("2020-12-31", "M"),
        ("2020-08-15", "ALL")
    ]
)
def test_categorize_expenses_and_income(transactions_random_data: pd.DataFrame, date: str, period: str) -> None:
    """
    Проверяет, что функция правильно разбивает транзакции на категории
    :param transactions_random_data:
    :param date:
    :param period:
    :return:
    """

    df = transactions_random_data
    df_choice_data = get_choice_data(df, date, period)
    df_total_amount = df_choice_data["Сумма операции"].sum().item()
    result = get_event_page(df, date, period)

    transfers_and_cash_list = result['expenses']['transfers_and_cash']
    sum_transfers_and_cash = sum(item['amount'] for item in transfers_and_cash_list)
    final_total_amount = float(result["expenses"]["total_amount"]) + sum_transfers_and_cash + float(result["income"]["total_amount"])

    assert df_total_amount == final_total_amount
