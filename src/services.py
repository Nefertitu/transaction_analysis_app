from typing import List, Dict, Any, Hashable

from src.utils import get_list_dict_transactions, get_required_columns, path_file, get_read_excel, get_formatted_date


def get_investment_savings(month: str, transactions: list[Dict[str, Any]], limit: int) -> float:
    """
    Функция производит расчет суммы, которую удалось бы отложить в "Инвесткопилку",
    с учетом задаваемого шага округления
    :param month:
    :param transactions:
    :param limit:
    :return:
    """

    investment_savings = []
    for transaction in transactions:
        amount = transaction["Сумма операции"]

        if month in transaction["Дата операции"]:
            accumulation = round((limit - (abs(amount) % limit)), 2)
            investment_savings.append(accumulation)

        else:
           continue

    return round(sum(investment_savings), 2)


path_to_file = path_file("data", "operations_1.xlsx")
trans = get_read_excel(path_to_file)
my_columns = ["Дата операции", "Сумма операции"]
df = get_required_columns(trans, my_columns)
transactions_with_formatted_date = get_formatted_date(df)
# print(transactions_with_formatted_date)
transactions_as_list_of_dicts = list(get_list_dict_transactions(transactions_with_formatted_date))
investment_savings = get_investment_savings("2019-07", transactions_as_list_of_dicts,10)
print(investment_savings)

