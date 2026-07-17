import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import configure_logging, get_decorator, path_file

log_file_path = path_file("log", "mylog_reports.log")
configure_logging(log_file_path)


@get_decorator(filename="report_1.log")
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None, logger: Optional[logging.Logger] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в рабочий и в выходной день за последние 3 месяца
    от определенной даты, если она установлена, либо от текущей даты
    :param transactions:
    :param date:
    :return:
    """

    if not date:
        date_obj = datetime.now()
        if logger:
            logging.info(f"\nВ качестве отчетной даты установлена текущая дата: {date_obj}")
    else:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        if logger:
            logging.info(f"\nВ качестве отчетной даты установлена дата: {date}")

    new_date_obj = date_obj - relativedelta(months=3)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    mask = (transactions["Дата операции"] >= new_date_obj) & (transactions["Дата операции"] <= date_obj)
    result = transactions[mask].copy()

    result["День недели"] = result["Дата операции"].dt.day_name()
    transactions_work_days = result.loc[
        result["День недели"].isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    ]
    transactions_weekdays = result.loc[result["День недели"].isin(["Saturday", "Sunday"])]

    mean_work_days = round(abs(transactions_work_days["Сумма операции"]).mean(), 2)
    mean_weekdays = round(abs(transactions_weekdays["Сумма операции"]).mean(), 2)
    result_spending = pd.DataFrame(
        {"Средние траты в рабочий день": [mean_work_days], "Средние траты в выходной день": [mean_weekdays]}
    )
    if logger:
        logging.info(f"\nПолучен следующий результат:\n {result_spending}")
    return result_spending


# trans_1 = pd.DataFrame({"Дата операции": ["2025-01-30", "2025-01-29", "2025-12-25", "2024-12-15", "2024-08-31"],
#                    "Сумма операции": [160.89, 64.00, 425.15, 780.00, 1000.88]})
# (print(trans_1))
# trans = get_read_excel(path_to_file=path_file("data", "operations_1.xlsx"))
# # print(trans)
#
# my_columns = ["Дата операции", "Сумма операции"]
# # my_columns = ["Дата операции"]
# result = get_required_columns(trans, my_columns)
# # print(type(result))
# # print(result)
# result_1 = get_formatted_date(result)
# # # print(result_1)
# spending = spending_by_workday(result_1, "2021-01-01", logger=configure_logging(path_file("log", "mylog_reports.log")))
# print(spending)
