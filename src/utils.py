import datetime
import json
import logging

from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Hashable, Union

import pandas as pd
from pathlib import Path

from pandas import DataFrame



def path_file(my_directory: str, my_filename: str) -> Path:
    """Получение абсолютного пути к фалу"""
    root_dir = Path(__file__).parent.parent
    filepath = root_dir/my_directory/my_filename
    return filepath

# print(path_file("src", "utils.py"))


def get_read_excel(path_to_file: str | Path) -> pd.DataFrame | str:
    """
    Считывание данных о финансовых операциях из файла Excel
    :param path_to_file:
    :return:
    """

    try:
        data_transactions = pd.read_excel(path_to_file)

    except FileNotFoundError as exc_info:
        raise FileNotFoundError(f"Function {get_read_excel.__name__} error: {type(exc_info).__name__}")
    except ValueError as exc_info:
        raise ValueError(f"Function {get_read_excel.__name__} error: {str(exc_info)}")

    else:
        if data_transactions.empty:
            return "Файл пустой."

        else:
            values = {"Номер карты": "*0000", "Категория": data_transactions["Описание"]}
            data_transactions = data_transactions.fillna(value=values).dropna(subset=["Дата операции"], how='any')
            return data_transactions




        # return data_transactions.head().to_dict(orient="records")
        # return data_transactions.head().to_json(orient='records', indent=4, lines=True, force_ascii=False)


def get_required_columns(transactions:  DataFrame, names_column: list[str]) -> pd.DataFrame:
    """
    Функция позволяет получить данные из списка словарей с транзакциями в соответствии
    с заданными параметрами (названиями столбцов)
    :param transactions:
    :param names_column:
    :return:
    """

    data_filter = transactions.loc[:, names_column]
    # return data_filter.to_dict(orient="records")
    return data_filter


def get_formatted_date(transactions: pd.DataFrame) -> pd.Series | pd.DataFrame:
    """
    Применение функции преобразования формата даты к столбцу с датами
    :return:
    """


    def convert_date(date_str: str) -> str:
        """
        Преобразование формата даты в данных о финансовых транзакциях (ГГГГ-ММ-ДД)
        :param date_str:
        :return:
        """
        date_string, _ = date_str.split(maxsplit=1)
        date_obj = datetime.strptime(date_string.strip(), '%d.%m.%Y')
        return date_obj.strftime("%Y-%m-%d")

    transactions["Дата операции"] = transactions["Дата операции"].apply(convert_date)
    return transactions


def get_list_dict_transactions(transactions: pd.DataFrame) -> list[dict[Hashable, Any]]:
    """
    Преобразует формат данных с информацией о транзакциях из DataFrame в список словарей
    :param transactions:
    :return:
    """

    result = transactions.to_dict(orient="records")

    return result


def get_to_json_investment_savings(month: str, transactions: list[dict[Hashable, Any]], limit: int) -> str:
    """
    Возвращает JSON_ответ для сервиса "Инвесткопилка"
    :param month:
    :param limit:
    :return:
    """

    invest_savings = []
    for transaction in transactions:
        amount = transaction["Сумма операции"]

        if month in transaction["Дата операции"]:
            accumulation = round((limit - (abs(amount) % limit)), 2)
            invest_savings.append(accumulation)

        else:
            continue
    total_amount = round(sum(invest_savings), 2)
    result = {"Сумма инвестиционных накоплений": [f"{total_amount}"],
              "Период для расчета накоплений": [f"{month}"],
              "Лимит округления": [int(f"{limit}")]}

    return  pd.DataFrame(result).to_json(orient="records", indent=4, lines=True, force_ascii=False)


def update_user_settings(new_currencies: list[str], new_stocks: list[str]) -> str:
    """
    Обновляет файл `user_settings.json` пользовательскими настройками
    :param new_currencies:
    :param new_stocks:
    :return:
    """

    with open('../user_settings.json', 'w') as file:
        json.dump({'user_currencies': new_currencies, 'user_stocks': new_stocks}, file, indent=4)
    return f"Данные успешно переданы."


def get_choice_data(transactions: pd.DataFrame, date: str, time_range: str) -> pd.Series | Union[pd.DataFrame, None]:

    date_obj = datetime.strptime(date, '%Y-%m-%d')
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])

    if time_range == "M":
        first_day_of_month = date_obj.replace(day=1)
        mask = (transactions["Дата операции"] >= first_day_of_month) & (transactions["Дата операции"] <= date_obj)
        transactions['Дата операции'] = transactions['Дата операции'].dt.strftime('%Y-%m-%d')
        return transactions[mask].copy()

    elif time_range == "W":

        diff = date_obj.weekday()
        start_of_week = date_obj - timedelta(days=diff)
        mask = (transactions["Дата операции"] >= start_of_week) & (transactions["Дата операции"] <= date_obj)
        transactions['Дата операции'] = transactions['Дата операции'].dt.strftime('%Y-%m-%d')
        return transactions[mask].copy()

    elif time_range == "Y":

        start_of_year = date_obj.replace(month=1, day=1)
        mask = (transactions["Дата операции"] >= start_of_year) & (transactions["Дата операции"] <= date_obj)
        transactions['Дата операции'] = transactions['Дата операции'].dt.strftime('%Y-%m-%d')
        return transactions[mask].copy()


    elif time_range == "ALL":

        mask = (transactions["Дата операции"] <= date_obj)
        transactions['Дата операции'] = transactions['Дата операции'].dt.strftime('%Y-%m-%d')
        return transactions[mask].copy()
    
    else:
        raise ValueError(f"Неправильный параметр time_range: {time_range}")



# path_to_file = path_file("data", "./operations.xlsx")
# trans = get_read_excel(path_to_file)
# # print(trans)
# my_columns = ["Дата операции", "Сумма операции"]
# # my_columns = ["Дата операции"]
# result = get_required_columns(trans, my_columns)
# # print(type(result))
# # print(result)
# result_1 = get_formatted_date(result)
# # print(result_1)
# # print(type(result_1))
#
# # print(update_user_settings(["EUR", "USD"], ["GOOGL", "TSLA"]))
#
# filter_date = get_choice_data(result_1, "2020-02-15", "W")
# print(filter_date)
# print(type(filter_date))
