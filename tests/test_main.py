import json
import sys
import unittest
from unittest.mock import patch, mock_open

import pandas as pd

from main import main_events
from src.utils import get_to_json_views, path_file


# # @patch("main.get_to_json_views")
# # @patch("src.views.get_event_page")
# # @patch("src.views.get_choice_data")
# @patch("main.get_formatted_date", return_value=pd.DataFrame({
#         'Дата операции': ['16.06.2020 00:00:00', '16.06.2020 00:00:00', '16.06.2020 00:00:00', '16.06.2020 00:00:00',
#                           '15.06.2020 00:00:00', '15.06.2020 00:00:00',
#                           '15.06.2020 00:00:00'],
#         'Сумма операции': [113.00, 30050.00, 198500.65, 3300.00, -1001.00, -1600.00, -900.40],
#         'Категория': ['Бонусы', 'Пополнения', 'Зарплата', 'Наличные', 'Фастфуд', 'Переводы', 'Супермаркеты']
#     }))
# @patch("main.get_read_excel", return_value=pd.DataFrame({ 'Дата операции': ['16.06.2020 00:00:00', '16.06.2020 00:00:00', '16.06.2020 00:00:00', '16.06.2020 00:00:00',
#                           '15.06.2020 00:00:00', '15.06.2020 00:00:00',
#                           '15.06.2020 00:00:00'],
#         'Сумма операции': [113.00, 30050.00, 198500.65, 3300.00, -1001.00, -1600.00, -900.40],
#         'Категория': ['Бонусы', 'Пополнения', 'Зарплата', 'Наличные', 'Фастфуд', 'Переводы', 'Супермаркеты']
#     }))
# @patch("builtins.input", side_effect=["да", "2020-06-01", "месяц", "нет", "нет"])
# def test_main_events(mock_input, mock_get_read_excel, mock_get_formatted_date, mock_get_choice_data, mock_get_event_page, capsys):
#     """Проверяет корректный вывод основной функции `main_events()`"""
#     pass
#     # mock_input.return_value = ["да", "2020-06-01", "месяц", "нет", "нет"]
#     # data = {
#     #     'Дата операции': ['16.06.2020 00:00:00', '16.06.2020 00:00:00', '16.06.2020 00:00:00', '16.06.2020 00:00:00',
#     #                       '15.06.2020 00:00:00', '15.06.2020 00:00:00',
#     #                       '15.06.2020 00:00:00'],
#     #     'Сумма операции': [113.00, 30050.00, 198500.65, 3300.00, -1001.00, -1600.00, -900.40],
#     #     'Категория': ['Бонусы', 'Пополнения', 'Зарплата', 'Наличные', 'Фастфуд', 'Переводы', 'Супермаркеты']
#     # }
#     #
#     # user_data = pd.DataFrame(data)
#     # # m = mock_open(read_data=str(user_data))
#     # # with patch("main.get_read_excel", return_value=m.return_value):
#     # print(main_events())
#     # mock_get_read_excel.return_value = user_data
#     # data_2 = {
#     #     'Дата операции': ['2020-06-16', '2020-06-16', '2020-06-16', '2020-06-16',
#     #                       '2020-06-15', '2020-06-15',
#     #                       '2020-06-15'],
#     #     'Сумма операции': [113.00, 30050.00, 198500.65, 3300.00, -1001.00, -1600.00, -900.40],
#     #     'Категория': ['Бонусы', 'Пополнения', 'Зарплата', 'Наличные', 'Фастфуд', 'Переводы', 'Супермаркеты']
#     # }
#     #
#     # user_data_2 = pd.DataFrame(data_2)
#     # mock_get_formatted_date.return_value = user_data_2
#     # mock_get_choice_data.return_value = user_data_2
#     user_data_3 = {
# "expenses": {
# "total_amount": 123.7,
# "main": [
#   [
#     {
#       "category": "Остальное",
#       "amount": 123.7
#     }
#   ]
# ],
# "transfers_and_cash": [
#   {
#     "category": "Наличные",
#     "amount": 0.0
#   },
#   {
#     "category": "Переводы",
#     "amount": 0.0
#   }
# ]
# },
# "income": {
# "total_amount": 343.39,
# "main": [
#   {
#     "category": "Пополнения",
#     "amount": 343.39
#   }
# ]
# },
# "currency_rates": [],
# "stock_prices": []
# }
#
#     # mock_get_event_page.return_value = user_data_3
#     # mock_get_to_json_views.return_value = get_to_json_views(user_data_3)
#
#     captured = capsys.readouterr()
#     expected_output = "\nРаспечатываю итоговые данные...\n" + json.dumps(user_data_3, ensure_ascii=False, indent=2)
#     assert expected_output in captured.out


@patch("builtins.open", return_value=["да", "2020-06-01", "месяц", "нет", "нет"])
def test_main_events_1():
    # for answer in mock_input.return_value:
    #     with patch("builtins.open") as f:
    #         mock_input = f.read()

    print(main_events(path_to_file=path_file("data", "operations.xlsx")))

