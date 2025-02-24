from typing import Any, Hashable

from src.utils import path_file, get_read_excel, get_required_columns, get_formatted_date, get_list_dict_transactions, \
    get_to_json_investment_savings


def get_investment_bank(month: str, transactions:  list[dict[Hashable, Any]], limit: int) -> float:
    """
    Функция производит расчет суммы, которую удалось бы отложить, в случае
    использования сервиса "Инвесткопилка", с учетом задаваемого шага округления
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


# path_to_file = path_file("data", "operations_1.xlsx")
# trans = get_read_excel(path_to_file)
# my_columns = ["Дата операции", "Сумма операции"]
# df = get_required_columns(trans, my_columns)
# print(df)
# transactions_with_formatted_date = get_formatted_date(df)
# print(transactions_with_formatted_date)
# transactions_as_list_of_dicts = (get_list_dict_transactions(transactions_with_formatted_date))
# print(transactions_as_list_of_dicts)
# investment_savings = get_investment_bank("2019-07", transactions_as_list_of_dicts,100)
# print(investment_savings)
# print(get_to_json_investment_savings("2019-07", transactions_as_list_of_dicts, 100))
# print(type(get_to_json_investment_savings("2019-07", transactions_as_list_of_dicts, 100)))
#
