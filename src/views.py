from datetime import datetime, timedelta
import pandas as pd

from src.utils import get_read_excel, path_file, get_formatted_date, get_required_columns


def get_event_page(transactions: pd.DataFrame, date: str, time_range: str = "M") -> pd.DataFrame:
    """
    Функция реализует функционал веб-страницы 'События', включающий предоставление
    следующих данных: расходы, поступления, курсы валют, стоимость акций из S&P 500
    :param transactions:
    :param date:
    :param time_range:
    :return:
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])

    if time_range == "M":

        first_day_of_month = date_obj.replace(day=1)
        mask = (transactions["Дата операции"] >= first_day_of_month) & (transactions["Дата операции"] <= date_obj)
        result = transactions[mask].copy()

    elif time_range == "W":

        diff = date_obj.weekday()
        start_of_week = date_obj - timedelta(days=diff)
        mask = (transactions["Дата операции"] >= start_of_week) & (transactions["Дата операции"] <= date_obj)
        result = transactions[mask].copy()

    elif time_range == "Y":

        start_of_year = date_obj.replace(month=1, day=1)
        mask = (transactions["Дата операции"] >= start_of_year) & (transactions["Дата операции"] <= date_obj)
        result = transactions[mask].copy()


    elif time_range == "ALL":

        mask = (transactions["Дата операции"] <= date_obj)
        result = transactions[mask].copy()

    else:
        raise ValueError(f"Неправильный параметр time_range: {time_range}")

    return result


# data = {
#     "Дата операции": ["2025-01-30", "2025-01-29", "2025-12-25", "2025-12-24", "2024-08-31"],
#                    "Сумма операции": [160.89, 64.00, 425.15, 780.00, 1000.88]
# }
# df = pd.DataFrame(data)

trans = get_read_excel(path_to_file=path_file("data", "operations.xlsx"))
print(trans)
print(trans.info())
print(trans.isnull().sum())

# my_columns = ["Дата операции", "Сумма операции"]
# my_columns = ["Дата операции"]
# result = get_required_columns(trans, my_columns)
# print(type(result))
# print(result)
result_1 = get_formatted_date(trans)
# print(result_1)
result = get_event_page(result_1, "2018-01-08", "W")
print(result)




