from typing import Hashable, Any

import pandas as pd
import pytest
from pandas import DataFrame


@pytest.fixture
def data_for_test_pd() -> dict:
    """Возвращает словари JSON с данными транзакций"""
    return {"Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"],
                   "Сумма операции с округлением": [160.89, 64.00]}


@pytest.fixture
def data_for_test_pd_result() -> DataFrame:
    """Возвращает словари JSON с данными транзакций"""
    sample_data = {"Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"],
                   "Сумма операции с округлением": [160.89, 64.00]}

    return pd.DataFrame(sample_data)