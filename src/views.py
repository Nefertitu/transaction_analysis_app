import json
from datetime import datetime, timedelta

import pandas as pd
from pandas import DataFrame

from src.external_api import get_exchange_rate, get_stock_prices
from src.utils import get_read_excel, path_file, get_formatted_date, get_required_columns, get_choice_data
from tests.conftest import transactions_random_data, transactions_sample_data


def get_event_page(transactions: pd.DataFrame, date: str, time_range: str = "M") -> dict | str:
    """
    Функция реализует функционал веб-страницы 'События', включающий предоставление
    следующих данных: расходы, поступления, курсы валют, стоимость акций из S&P 500
    :param transactions:
    :param date:
    :param time_range:
    :return:
    """
    # Получаем DataFrame, отфильтрованный по дате/периоду:
    result_df = get_choice_data(transactions, date, time_range)

    # Расходы:
    expenses_category = result_df.loc[~result_df["Категория"].isin(["Зарплата", "Пополнения", "Бонусы", "Наличные", "Перевод с карты", "Переводы", "Перевод средств с брокерского счета"])]
    expenses_amount = round(abs(expenses_category["Сумма операции"].sum().item()), 2)
    expenses_amount_category = abs(expenses_category.groupby("Категория")["Сумма операции"].sum())
    total_count = len(expenses_amount_category)

    if total_count >= 7:
        sort_expenses_main_categories = expenses_amount_category.sort_values(ascending=False).head(7)

    else:
        sort_expenses_main_categories = expenses_amount_category.sort_values(ascending=False).head(total_count - 1)

    categories_expenses_data = []

    for category, amount in sort_expenses_main_categories.items():
        categories_expenses_data.append({"category": category, "amount": round(amount, 2)})

    if total_count >= 7:
        expenses_other_categories_amount = round(abs(expenses_amount_category.sort_values(ascending=False).iloc[8:].sum().item()), 2)

    else:
        expenses_other_categories_amount = round(abs(expenses_amount_category.sort_values(ascending=False).iloc[total_count - 1:].sum().item()), 2)

    categories_expenses_data.append({
        "category": "Остальное",
        "amount": expenses_other_categories_amount,
    })

    # Переводы и наличные:
    cash_category = result_df.loc[result_df["Категория"].isin(["Наличные"])]
    cash_amount = round(abs(cash_category["Сумма операции"].sum().item()), 2)
    transfers_category = result_df.loc[result_df["Категория"].isin(["Перевод с карты", "Переводы", "Перевод средств с брокерского счета"])]
    transfers_amount = round(abs(transfers_category["Сумма операции"].sum().item()), 2)

    # Доходы
    income_category = result_df.loc[result_df["Категория"].isin(["Зарплата", "Пополнения", "Бонусы"])]
    income_amount = round(income_category["Сумма операции"].sum().item(), 2)
    income_categories_amount = income_category.groupby("Категория")["Сумма операции"].sum()
    sort_income_categories_amount = income_categories_amount.sort_values(ascending=False)

    income_categories_data = []

    for category, amount in sort_income_categories_amount.items():
        income_categories_data.append({"category": category, "amount": round(amount, 2)})

    # Курсы валют и стоимость акций:
    currency_rates = get_exchange_rate("../user_settings.json")
    stock_prices = get_stock_prices("../user_settings.json")

    # Данные для преобразования в JSON-строку:
    data = {
        "expenses": {
            "total_amount": expenses_amount,
            "main": [
                    categories_expenses_data,
            ],
            "transfers_and_cash": [
                {
                    "category": "Наличные",
                    "amount": cash_amount,
                },
                {
                    "category": "Переводы",
                    "amount": transfers_amount,
                }
            ]
        },
        "income": {
            "total_amount": income_amount,
            "main":
                income_categories_data,
        },
        "currency_rates": [
            currency_rates["USD"],
            currency_rates["EUR"],
        ],
        "stock_prices": [
                stock_prices["AAPL"],
                stock_prices["AMZN"],
                stock_prices["GOOGL"],
                stock_prices["MSFT"],
                stock_prices["TSLA"]
        ]
    }

    # return json.dumps(data, ensure_ascii=False, indent=2)
    return data

# data = {
#     "Дата операции": ["2025-01-30", "2025-01-29", "2025-12-25", "2025-12-24", "2024-08-31"],
#                    "Сумма операции": [160.89, 64.00, 425.15, 780.00, 1000.88]
# }
# df = pd.DataFrame(data)
#
# trans = get_read_excel(path_to_file=path_file("data", "operations.xlsx"))
# # print(trans)
# # print(trans.info())
# # print(trans.dtypes)
# # # # print(trans.isnull().sum())
# # #
# my_columns = ["Дата операции", "Сумма операции", "Категория"]
# # # # my_columns = ["Дата операции"]
# result = get_required_columns(trans, my_columns)
# # # # print(type(result))
# # # # print(result)
# result_1 = get_formatted_date(result)
# # print(result_1)
# filter_date = get_choice_data(result, "2020-06-16", "W")
# # print(filter_date)
# result = get_event_page(filter_date, "2020-06-16", "W")
# print(result)
# #
# print(json.dumps(result, ensure_ascii=False, indent=2))




