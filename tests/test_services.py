import pytest

from src.services import get_investment_bank


@pytest.mark.parametrize(
    "limit, expected_result",
    [
        (10, 29.28),  # Добавлены ожидаемые результаты для 10 и 50
        (50, 149.28),
        (100, 299.28),
    ],
)
def test_get_investment_bank(limit: int, expected_result: float, dict_sample_data: list[dict]) -> None:
    """
    Проверяет, что функция корректно производит расчет суммы, которую
    удалось бы отложить при использовании сервиса "Инвесткопилка",
    с учетом задаваемого шага округления
    :param dict_sample_data:
    :return:
    """

    result = get_investment_bank("2020-03", dict_sample_data, limit)
    assert result == expected_result
