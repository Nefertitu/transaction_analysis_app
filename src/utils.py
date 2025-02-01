import datetime
from datetime import date, time, datetime, timedelta
from os.path import dirname
from typing import List, Dict, Any, Hashable, Type, MutableMapping

import pandas as pd
from pathlib import Path

from pandas import DataFrame



def path_file(my_directory: str, my_filename: str) -> Path:
    "Получение абсолютного пути к фалу"
    ROOT_DIR = Path(__file__).parent.parent
    filepath = ROOT_DIR/my_directory/my_filename
    return filepath

# print(path_file("src", "utils.py"))


def get_read_excel(path_to_file: str | Path) -> DataFrame:
    """
    Считывание данных о финансовых операциях из файла Excel
    :param path_to_file:
    :return:
    """
    try:
        data_transactions = pd.read_excel(path_to_file)
        # print(data_transactions)

    except FileNotFoundError as exc_info:
        raise FileNotFoundError(f"Function {get_read_excel.__name__} error: {type(exc_info).__name__}")
    except ValueError as exc_info:
        raise ValueError(f"Function {get_read_excel.__name__} error: {str(exc_info)}")

    else:
        return data_transactions
        # return data_transactions.head().to_dict(orient="records")
        # return data_transactions.head().to_json(orient='records', indent=4, lines=True, force_ascii=False)


# trans = get_read_excel(r"..\data\operations.xlsx")
# trans = get_read_excel(r"..\data\operations_error.json")
# print(type(trans))


# # Указываем правильный путь
# directory_path = r'C:\Users\Oper\PycharmProjects\pythonProject\transaction_analysis_app\data'
#
# # Проверяем существование директории
# if not os.path.exists(directory_path):
#     print(f"Папка {directory_path} не найдена.")
# else:
#     # Получаем список файлов в директории
#     directory_files = os.listdir(directory_path)
#     for file in directory_files:
#         print(file)


def get_required_columns(transactions:  DataFrame, names_column: list[str]) -> list[dict[Hashable, Any]] | DataFrame:
    """
    Функция позволяет получить данные из списка словарей с транзакциями в соотвтетсвии
    с заданными параметрами (названиями столбцов)
    :param transactions:
    :return:
    """

    data_filter = transactions.loc[:, names_column]
    # return data_filter.to_dict(orient="records")
    return data_filter


def get_formatted_date(transactions: pd.DataFrame) -> pd.Series | pd.DataFrame:
    """
    Применение функции преобразования формата даты к столбцу с датами
    :param transactions:
    :return:
    """

    def convert_date(date_str: str) -> str:
        """
        Преобразование формата даты в данных о финансовых транзакциях
        :param date_str:
        :return:
        """
        date_string, _ = date_str.split(maxsplit=1)
        # (print(date_string))
        date_obj = datetime.strptime(date_string.strip(), '%d.%m.%Y')
        return date_obj.strftime("%Y-%m-%d")

    transactions.iloc[:, 0].apply(convert_date)
    return transactions



path_to_file = path_file("data", "operations.xlsx")
trans = get_read_excel(path_to_file)
my_columns = ["Дата операции", "Сумма операции"]
# my_columns = ["Дата операции"]
result = get_required_columns(trans, my_columns)
# print(result)
result_1 = get_formatted_date(result)
# print(result_1)
# print(type(result_1))
