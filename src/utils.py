import datetime
import json
import logging

from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable,Hashable, Union

import pandas as pd
from pathlib import Path

from pandas import DataFrame


def path_file(my_directory: str, my_filename: str) -> Path:
    """Получение абсолютного пути к фалу"""
    root_dir = Path(__file__).parent.parent
    filepath = root_dir/my_directory/my_filename
    return filepath

# print(path_file("src", "utils.py"))


def configure_logging(log_path: Path):
    """Настраивает логирование с указанной кодировкой."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(levelname)s: %(asctime)s - %(funcName)s() - %(message)s'))
    logger.addHandler(handler)


def get_decorator(filename: str = None) -> Callable[[Callable], Callable]:
    """
    Декоратор для записи отчетов результатов выполнения функций
    :param filename: Имя файла для записи отчетов
    :return: Декорированная функция
    """

    if not filename:
        filename = f'{path_file("log", "report.log")}'
    filename = f'{path_file("log", filename)}'

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # logging.info(f"Starting {function.__name__} with arguments: {args}, {kwargs}")

            try:
                start_time = datetime.now()
                result = function(*args, **kwargs)
                end_time = datetime.now()

                with open(filename, 'w', encoding="utf-8") as file:
                    file.write(
                        f"Function_name: {function.__name__}.\n"
                        f"Function call time: {start_time}.\n"
                        f"Execution time: {(end_time - start_time).total_seconds():.7f}\n\n"
                        f"Result = {result}.\n"
                    )

                return result

            except Exception as exc_info:

                with open(filename, 'w') as file:
                    file.write(
                        f"{function.__name__} error: {type(exc_info).__name__}: {str(exc_info)}.\n"
                        f"Inputs: {args}, {kwargs}\n\n"
                    )

                return (f"{function.__name__} failed with exception: {exc_info}. Arguments: {args}, {kwargs}.")

        return wrapper

    return decorator


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


def update_user_settings(new_currencies: list[str] = None, new_stocks: list[str] = None) -> str:
    """
    Обновляет файл `user_settings.json` пользовательскими настройками
    :param new_currencies:
    :param new_stocks:
    :return:
    """
    if new_currencies and new_stocks:
        with open('./user_settings.json', 'w') as file:
            json.dump({'user_currencies': new_currencies, 'user_stocks': new_stocks}, file, indent=4)
        return f"\n\nДанные успешно переданы."
    else:
        with open('./user_settings.json', 'w') as file:
            file.write("")
        return f"\n\nНет данных."

# new_currencies = []
# new_stocks = ['AAPL', 'AMZN']
# print(update_user_settings(new_currencies, new_stocks))


def get_choice_data(transactions: pd.DataFrame, date: str, time_range: str) -> pd.Series | Union[pd.DataFrame, None]:

    if not isinstance(transactions, pd.DataFrame):
        raise ValueError("Ожидается объект типа DataFrame")

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


def get_to_json_views(data_transactions: dict) -> str:
    """
    Преобразует данные страницы "События" в JSON формат
    :param data_transactions:
    :return:
    """

    result = json.dumps(data_transactions, ensure_ascii=False, indent=2)

    return result

# data = {'expenses': {'total_amount': 2681.82, 'main': [[{'category': 'Другое', 'amount': 2127.32}, {'category': 'Топливо', 'amount': 221.0}, {'category': 'Красота', 'amount': 179.5}, {'category': 'Остальное', 'amount': 154.0}]], 'transfers_and_cash': [{'category': 'Наличные', 'amount': 0.0}, {'category': 'Переводы', 'amount': 0.0}]}, 'income': {'total_amount': 500.0, 'main': [{'category': 'Бонусы', 'amount': 500.0}]}, 'stock_prices': [([{'stock': 'AAPL', 'price': 247.9}, {'stock': 'AMZN', 'price': 214.45}])]}
# print(get_to_json_views(data))


# path_to_file = path_file("data", "operations.xlsx")
# trans = get_read_excel(path_to_file)
# print(trans)
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
