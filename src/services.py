from typing import Any, Hashable

from src.utils import get_list_dict_transactions, get_required_columns, path_file, get_read_excel, get_formatted_date, \
    get_to_json_investment_savings


def get_investment_savings(month: str, transactions:  list[dict[Hashable, Any]], limit: int) -> float:
    """
    Функция производит расчет суммы, которую удалось бы отложить в "Инвесткопилку",
    с учетом задаваемого шага округления
    :param month:
    :param transactions:
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

    return round(sum(invest_savings), 2)


path_to_file = path_file("data", "operations_1.xlsx")
trans = get_read_excel(path_to_file)
my_columns = ["Дата операции", "Сумма операции"]
df = get_required_columns(trans, my_columns)
transactions_with_formatted_date = get_formatted_date(df)
transactions_as_list_of_dicts = (get_list_dict_transactions(transactions_with_formatted_date))
print(transactions_as_list_of_dicts)
investment_savings = get_investment_savings("2019-07", transactions_as_list_of_dicts,100)
print(investment_savings)
print(get_to_json_investment_savings(investment_savings, "2019-07", 100))

