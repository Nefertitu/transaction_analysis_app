from typing import Hashable, Any

import pandas as pd
import pytest
from black.lines import Callable
from pandas import DataFrame


@pytest.fixture
def data_for_test_pd() -> dict:
    """Возвращает словари с данными транзакций"""
    return {"Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"],
                   "Сумма операции с округлением": [160.89, 64.00]}


@pytest.fixture
def data_for_test_pd_result() -> DataFrame:
    """Возвращает DataFrame с данными транзакций"""
    sample_data = {"Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"],
                   "Сумма операции с округлением": [160.89, 64.00]}

    return pd.DataFrame(sample_data)


@pytest.fixture
def data_for_test_pd_result_empty() -> DataFrame:
    """Возвращает словарь с данными транзакций"""
    sample_data = {}

    return pd.DataFrame(sample_data)


@pytest.fixture
def data_for_test_pd_formatted_date_1() -> DataFrame:
    """Возвращает DataFrame с данными транзакций"""
    sample_data = {"Дата операции": ["2021-12-31", "2021-12-31"],
                   "Сумма операции с округлением": [160.89, 64.00]}

    return pd.DataFrame(sample_data)



@pytest.fixture
def data_for_test_pd_formatted_date_2() -> DataFrame:
    """Возвращает DataFrame с данными транзакций"""
    sample_data = {"Дата операции": ["2021-12-31", "1111-11-11"],
                   "Сумма операции с округлением": [160.89, 64.00]}

    return pd.DataFrame(sample_data)


sample_data = {"Дата операции": ["31.12.2021 16:44:00", ""],
                   "Сумма операции с округлением": [160.89, 64.00]}


sample_data_2 = {"Номер карты": ["*5091", ""],
                   "Сумма операции": [-564.00, -800.00]}


replace_values = {"Дата операции": "11.11.1111 00:00:00", "Номер карты": "*0000", "Категория": "Не определена"}


@pytest.fixture
def data_for_test_pd_date_null():
    return pd.DataFrame(sample_data)

@pytest.fixture
def data_for_test_pd_date_null_2():
    return pd.DataFrame(sample_data_2)


@pytest.fixture
def data_for_test_pd_replace_date(data_for_test_pd_date_null):
    df = data_for_test_pd_date_null.copy()
    return df.fillna(value=replace_values)


@pytest.fixture
def data_for_test_pd_replace_date_2(data_for_test_pd_date_null_2):
    df = data_for_test_pd_date_null_2.copy()
    return df.fillna(value=replace_values)


params = [
    (pd.DataFrame(sample_data), pd.DataFrame(sample_data).fillna(replace_values)),
    (pd.DataFrame(sample_data_2), pd.DataFrame(sample_data_2).fillna(replace_values))
]

@pytest.fixture
def apilayer_responses() -> list[dict]:
    """Возвращает словарь с данными о конвертации транзакции
    (ответ сайта `https://api.apilayer.com`)"""
    return [
        {
  "base": "USD",
  "date": "2025-02-07",
  "rates": {
    "RUB": 96.865166
  },
  "success": True,
  "timestamp": 1738941317
},
        {
  "base": "EUR",
  "date": "2025-02-07",
  "rates": {
    "RUB": 100.503777
  },
  "success": True,
  "timestamp": 1738941545
}
    ]
