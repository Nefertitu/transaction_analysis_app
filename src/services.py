from typing import List, Dict, Any, Hashable


def get_investment_bank(month: str, transactions: list[dict[Hashable, Any]], limit: int) -> float:
    """
    Функция производит расчет суммы, которую удалось бы отложить в "Инвесткопилку",
    с учетом задаваемого шага округления
    :param month:
    :param transactions:
    :param limit:
    :return:
    """
