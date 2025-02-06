from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional

import pandas as pd

from src.utils import get_read_excel, path_file, get_required_columns, get_formatted_date


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в рабочий и в выходной день за последние 3 месяца
    от определенной даты, если она установлена, либо от текущей даты
    :param transactions:
    :param date:
    :return:
    """
    if not date:
        date_obj = datetime.now()
    else:
        date_obj = datetime.strptime(date, '%Y-%m-%d')

    new_date_obj = date_obj - relativedelta(months=3)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    mask = (transactions["Дата операции"] >= new_date_obj) & (transactions["Дата операции"] <= date_obj)
    result = transactions[mask].copy()
    print(result)

    result["День недели"] = result["Дата операции"].dt.day_name()
    transactions_work_days = result.loc[result["День недели"].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
    transactions_weekdays =  result.loc[result["День недели"].isin(['Saturday', 'Sunday'])]

    mean_work_days = abs(transactions_work_days["Сумма операции"]).mean()
    mean_weekdays = abs(transactions_weekdays["Сумма операции"]).mean()

    return pd.DataFrame({"Средние траты в рабочий день": [mean_work_days],
            "Средние траты в выходной день": [mean_weekdays]})


# trans_1 = pd.DataFrame({"Дата операции": ["2025-01-30", "2025-01-29", "2025-12-25", "2024-12-15", "2024-08-31"],
#                    "Сумма операции": [160.89, 64.00, 425.15, 780.00, 1000.88]})
# (print(trans_1))
trans = get_read_excel(path_to_file=path_file("data", "operations_1.xlsx"))
# print(trans)

# my_columns = ["Дата операции", "Сумма операции"]
# my_columns = ["Дата операции"]
# result = get_required_columns(trans, my_columns)
# print(type(result))
# print(result)
result_1 = get_formatted_date(trans)
# print(result_1)
print(spending_by_workday(result_1, "2021-01-01"))