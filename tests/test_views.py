import sys
from unittest.mock import patch

import pytest
import pandas as pd
sys.path.append('../src/')
from src.utils import get_choice_data
from src.views import get_event_page


@patch('src.views.get_stock_prices')
@patch('src.views.get_exchange_rate')
@pytest.mark.parametrize("date, period", [("2020-12-31", "M"), ("2020-08-15", "ALL")])
def test_categorize_expenses_and_income(mock_get_exchange_rate,
    mock_get_stock_prices,transactions_random_data: pd.DataFrame, date: str, period: str) -> None:
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
    expected_result_stocks = {
        "AAPL": {"stock": "AAPL", "price": 241.53},
        "AMZN": {"stock": "AMZN", "price": 230.37},
        "GOOGL": {"stock": "GOOGL", "price": 186.14},
        "MSFT": {"stock": "MSFT", "price": 410.54},
        "TSLA": {"stock": "TSLA", "price": 355.94}
    }
    expected_result_rates = {
        "USD": {"currency": "USD", "rate": 91.75},
        "EUR": {"currency": "EUR", "rate": 96.04}
    }
    mock_get_stock_prices.return_value = expected_result_stocks
    mock_get_exchange_rate.return_value = expected_result_rates
    result = get_event_page(df, date, period)

    transfers_and_cash_list = result["expenses"]["transfers_and_cash"]
    sum_transfers_and_cash = sum(item["amount"] for item in transfers_and_cash_list)
    final_total_amount = (
        float(result["expenses"]["total_amount"]) + sum_transfers_and_cash + float(result["income"]["total_amount"])
    )

    assert df_total_amount == final_total_amount


@patch('src.views.get_stock_prices')
@patch('src.views.get_exchange_rate')
@patch('src.views.get_choice_data')
def test_get_event_page_success(
    mock_get_choice_data,
    mock_get_exchange_rate,
    mock_get_stock_prices,
    df_for_views
):
    """Проверяет, что функция возвращает корректные данные."""

    df = df_for_views.copy()
    mock_get_choice_data.return_value = df

    expected_result_stocks = {
        "AAPL": {"stock": "AAPL", "price": 241.53},
        "AMZN": {"stock": "AMZN", "price": 230.37},
        "GOOGL": {"stock": "GOOGL", "price": 186.14},
        "MSFT": {"stock": "MSFT", "price": 410.54},
        "TSLA": {"stock": "TSLA", "price": 355.94}
    }

    expected_result_rates = {
        "USD": {"currency": "USD", "rate": 91.75},
        "EUR": {"currency": "EUR", "rate": 96.04}
    }

    mock_get_stock_prices.return_value = expected_result_stocks
    mock_get_exchange_rate.return_value = expected_result_rates

    result = get_event_page(df, "2020-06-16", "W")

    expected_result = {
        "expenses": {
            "total_amount": 422.37,
            "main": [
                [
                    {"category": "Супермаркеты", "amount": 322.37},
                    {"category": "Остальное", "amount": 100.00}
                ]
            ],
            "transfers_and_cash": [
                {"category": "Наличные", "amount": 0.00},
                {"category": "Переводы", "amount": 1600.00}
            ]
        },
        "income": {
            "total_amount": 413.00,
            "main": [
                {"category": "Пополнения", "amount": 300.00},
                {"category": "Бонусы", "amount": 113.00}
            ]
        },
        "currency_rates":
            list(expected_result_rates.values())
        ,
        "stock_prices":
            list(expected_result_stocks.values())
    }

    assert result == expected_result