from typing import Hashable, Any

import pandas as pd
import pytest
from black.lines import Callable
from pandas import DataFrame, Series


@pytest.fixture
def data_for_test_pd() -> dict:
    """Возвращает словари с данными транзакций"""
    return {"Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"],
                   "Сумма операции с округлением": [160.89, 64.00]}


@pytest.fixture
def data_for_test_pd_result() -> pd.DataFrame:
    """Возвращает DataFrame с данными транзакций"""
    sample_data = {"Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"],
                   "Сумма операции с округлением": [160.89, 64.00],
                   "Описание": ["Кэшбэк", "МТС"]}

    return pd.DataFrame(sample_data)


@pytest.fixture
def data_for_test_pd_result_empty() -> pd.DataFrame:
    """Возвращает словарь с данными транзакций"""
    sample_data = {}

    return pd.DataFrame(sample_data)


@pytest.fixture
def data_formatted_date_1() -> DataFrame:
    """Возвращает DataFrame с данными транзакций"""
    sample_data = {"Дата операции": ["2021-12-31", "2021-12-31"],
                   "Сумма операции с округлением": [160.89, 64.00],
                   "Описание": ["Кэшбэк", "МТС"]}

    return pd.DataFrame(sample_data)



@pytest.fixture
def data_for_test_pd_2() -> DataFrame:
    """Возвращает DataFrame с данными транзакций"""
    sample_data = {"Дата операции": ["2021-12-31", "2021-12-15"],
                   "Сумма операции": [160.89, 64.00],
                   "Описание": ["Fotostudiya", "Перевод на карту"]}

    return pd.DataFrame(sample_data)


@pytest.fixture
def data_for_test_pd_2_return() -> DataFrame:
    """Возвращает DataFrame с данными транзакций"""
    sample_data = {"Дата операции": ["2021-12-31", "2021-12-15"],
                   "Сумма операции": [160.89, 64.00]}

    return pd.DataFrame(sample_data)


sample_data = {"Дата операции": ["2021-12-31", ""],
               "Категория": ["Сервис", ""],
               "Сумма операции с округлением": [160.89, 64.00],
               "Описание": ["Fotostudiya", "Перевод на карту"]}

sample_data_2 = {"Дата операции": ["2021-12-31", ""],
                 "Номер карты": ["*5091", ""],
                 "Сумма операции": [-564.00, -800.00],
                 "Описание": ["Кэшбэк", "МТС"]}


replace_values = {"Дата операции": "", "Категория": "Перевод на карту", "Номер карты": "*0000"}


@pytest.fixture
def data_for_test_pd_date_null():
    return pd.DataFrame(sample_data)

@pytest.fixture
def data_for_test_pd_date_null_2():
   return pd.DataFrame(sample_data_2)


@pytest.fixture
def data_for_test_pd_replace_date(data_for_test_pd_date_null):
    df = data_for_test_pd_date_null.copy()
    return df.fillna(value=replace_values).dropna(subset=["Дата операции"], how='any')


@pytest.fixture
def data_for_test_pd_replace_date_2(data_for_test_pd_date_null_2):
    df = data_for_test_pd_date_null_2.copy()
    return df.fillna(value=replace_values).dropna(subset=["Дата операции"], how='any')


params = [
    (pd.DataFrame(sample_data), pd.DataFrame(sample_data).fillna(replace_values)),
    (pd.DataFrame(sample_data_2), pd.DataFrame(sample_data_2).fillna(replace_values))
]

@pytest.fixture
def apilayer_responses() -> list[dict]:
    """Возвращает словарь с данными о конвертации транзакции
    (ответ API сайта `https://api.apilayer.com`)"""
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


@pytest.fixture
def financialmodel_responses() -> list[list[dict]]:
    """Возвращает словарь с данными о курсе акций
    (ответ API сайта `https://site.financialmodelingprep.com/`)"""
    return [
        [
            {
                "symbol": "AAPL",
                "price": 150.154,
                "volume": 36735534
            }
        ],
        [
            {
                "symbol": "AMZN",
                "price": 3173.1842,
                "volume": 25569805
            }
        ],
        [
            {
                "symbol": "GOOGL",
                "price": 2742.391,
                "volume": 59627739
            }
        ],
        [
            {
                "symbol": "MSFT",
                "price": 296.71,
                "volume": 14782766
            }
        ],
        [
            {
                "symbol": "TSLA",
                "price": 1007.083,
                "volume": 55969352
            }
        ]
]


@pytest.fixture
def test_df_to_dict(data_for_test_pd_result):
    df = data_for_test_pd_result.copy()
    return df.to_dict(orient="records")