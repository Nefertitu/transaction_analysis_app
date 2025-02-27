import json
import random
import pandas as pd
import pytest

from pandas import DataFrame


@pytest.fixture
def data_for_test_pd_result() -> pd.DataFrame:
    """Возвращает DataFrame с данными транзакций"""
    sample_data = {"Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"],
                   "Сумма операции с округлением": [160.89, 64.00],
                   "Описание": ["Кэшбэк", "МТС"]}

    return pd.DataFrame(sample_data)

@pytest.fixture
def data_for_test_pd(data_for_test_pd_result) -> list[dict]:
    """Возвращает словари с данными транзакций"""
    df = data_for_test_pd_result.copy()
    return df.to_dict(orient="records")


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
    transactions_sample_data = data_for_test_pd_date_null.copy()
    return transactions_sample_data.fillna(value=replace_values).dropna(subset=["Дата операции"], how='any')


@pytest.fixture
def data_for_test_pd_replace_date_2(data_for_test_pd_date_null_2):
    transactions_sample_data = data_for_test_pd_date_null_2.copy()
    return transactions_sample_data.fillna(value=replace_values).dropna(subset=["Дата операции"], how='any')


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
                "price": 240.864,
                "volume": 36735534
            }
        ],
        [
            {
                "symbol": "AMZN",
                "price": 229.6542,
                "volume": 25569805
            }
        ],
        [
            {
                "symbol": "GOOGL",
                "price": 184.671,
                "volume": 59627739
            }
        ],
        [
            {
                "symbol": "MSFT",
                "price": 409.42,
                "volume": 14782766
            }
        ],
        [
            {
                "symbol": "TSLA",
                "price": 352.913,
                "volume": 55969352
            }
        ]
]


@pytest.fixture
def test_transactions_sample_data_to_dict(data_for_test_pd_result):
    transactions_sample_data = data_for_test_pd_result.copy()
    return transactions_sample_data.to_dict(orient="records")


@pytest.fixture
def json_user_settings() -> dict:
    data =  """
    {
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}"""
    return json.loads(data)


@pytest.fixture
def json_user_settings_copy(json_user_settings) -> dict:
    sample_data = json_user_settings.copy()
    return sample_data


@pytest.fixture
def json_user_settings_1() -> dict:
    return {
    "url": "http://example.com/api/exchange-rate"
}


@pytest.fixture
def json_user_settings_2() -> dict:
    return {
"url": "https://site.financialmodelingprep.com/sample/"
}


@pytest.fixture
def data_to_dict_for_services(data_for_test_pd_2):
    transactions_sample_data = data_for_test_pd_2.copy()
    return transactions_sample_data.to_dict(orient="records")


@pytest.fixture(scope="module")
def transactions_sample_data():
    """Фикстура для создания тестового датафрейма"""
    index = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')
    transactions_sample_data = pd.DataFrame(index=index)

    categories = ["Перевод с карты", "Переводы", "Перевод средств с брокерского счета", "Зарплата", "Пополнения",
                  "Бонусы", "Наличные", "Супермаркеты", "Фастфуд", "Топливо", "Развлечения", "Медицина", "Госуслуги",
                  "Дом и ремонт"]
    amount = list(range(0, 5000))

    new_categories = []
    amount_list = []

    for _ in range(366):
        random_category = random.choice(categories)
        random_number = random.choice(amount)
        new_categories.append(random_category)
        amount_list.append(float(random_number))

    transactions_sample_data["Категория"] = new_categories
    transactions_sample_data["Сумма операции"] = amount_list

    transactions_sample_data.reset_index(inplace=True)
    transactions_sample_data.rename(columns={"index": "Дата операции"}, inplace=True)

    return transactions_sample_data


@pytest.fixture
def transactions_random_data(transactions_sample_data):
    df_sample_data = transactions_sample_data.copy()
    return df_sample_data


@pytest.fixture
def df_sample_data():
    """Генерация DataFrame с транзакциями"""
    sample_data = {
        'Дата операции': ['2020-01-25', '2020-02-10', '2020-03-05', '2020-04-20'],  # Добавлена запись за январь
        'Сумма операции': [50, 100, 200, 300]
    }
    df = pd.DataFrame(sample_data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])

    return df


@pytest.fixture
def dict_sample_data() -> list[dict]:
    """Получение списка словарей с транзакциями"""
    return [
        {'Дата операции': '2020-01-25', 'Сумма операции': -50.25},
        {'Дата операции': '2020-03-04', 'Сумма операции': -100.15},
        {'Дата операции': '2020-03-05', 'Сумма операции': -2100.08},
        {'Дата операции': '2020-03-20', 'Сумма операции': -300.49}
    ]

@pytest.fixture
def sample_data_for_reports() -> pd.DataFrame:
    """Генерация DataFrame с транзакциями"""
    sample_data = {
        'Дата операции': ['2020-01-10', '2020-01-25', '2020-03-05', '2020-04-20'],  # Добавлена запись за январь
        'Сумма операции': [5000.25, 100.15, 2080.95, 3011.10]
    }
    df = pd.DataFrame(sample_data)
    # df["Дата операции"] = pd.to_datetime(df["Дата операции"])

    return df



#
# @pytest.fixture
# def get_choice_data_month(transactions_sample_data, date_str, time_range, ):
#     date_obj = datetime.strptime(date_str, '%Y-%m-%d')
#     if time_range == "M":
#         first_day_of_month = date_obj.replace(day=1)
#         last_day_of_month = first_day_of_month + pd.offsets.MonthEnd(0)
#         mask = (transactions_sample_data["Дата операции"] >= first_day_of_month) & (transactions_sample_data["Дата операции"] <= last_day_of_month)
#         return transactions_sample_data[mask].copy()
#     else:
#         raise ValueError(f"Неподдерживаемый временной диапазон: {time_range}")


@pytest.fixture
def data_df_for_test_views() -> pd.DataFrame:
    """Данные для теста модуля `views.py`"""
    data = {
        'Дата операции': ['2020-06-16', '2020-06-16', '2020-06-16', '2020-06-16', '2020-06-15', '2020-06-15',
                          '2020-06-15'],
        'Сумма операции': [113.00, 300.00, -198.67, -33.70, -100.00, -1600.00, -90.00],
        'Категория': ['Бонусы', 'Пополнения', 'Супермаркеты', 'Супермаркеты', 'Фастфуд', 'Переводы', 'Супермаркеты']
    }

    return pd.DataFrame(data).copy()

@pytest.fixture
def df_for_views(data_df_for_test_views) -> pd.DataFrame:
    df_sample_data = data_df_for_test_views.copy()
    return df_sample_data


    # return {'expenses': {'total_amount': 16324.54, 'main': [[{'category': 'ЖКХ', 'amount': 7693.0}, {'category': 'Супермаркеты', 'amount': 4400.54}, {'category': 'Различные товары', 'amount': 1339.0}, {'category': 'Книги', 'amount': 1056.0}, {'category': 'Аптеки', 'amount': 797.0}, {'category': 'Дом и ремонт', 'amount': 328.0}, {'category': 'Связь', 'amount': 250.0}, {'category': 'Остальное', 'amount': 261.0}]], 'transfers_and_cash': [{'category': 'Наличные', 'amount': 0.0}, {'category': 'Переводы', 'amount': 1600.0}]}, 'income': {'total_amount': 1043.39, 'main': [{'category': 'Пополнения', 'amount': 1043.39}]}}


@pytest.fixture
def apilayer_responses_views() -> dict:
    """Возвращает список курсов валют."""
    return {
        "USD": {"currency": "USD", "rate": 91.75},
        "EUR": {"currency": "EUR", "rate": 96.04}
    }



@pytest.fixture
def financialmodel_responses_views() -> dict:
    """Возвращает список стоимости акций."""
    return {
        "AAPL": {"stock": "AAPL", "price": 241.53},
        "AMZN": {"stock": "AMZN", "price": 230.37},
        "GOOGL": {"stock": "GOOGL", "price": 186.14},
        "MSFT": {"stock": "MSFT", "price": 410.54},
        "TSLA": {"stock": "TSLA", "price": 355.94}
    }

