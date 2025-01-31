import pytest

from unittest.mock import patch

import pandas as pd

from src.utils import get_read_excel, path_file


@patch("pandas.read_excel")
def test_get_read_excel(mock_read_excel: pd.DataFrame):
    """
    Проверяет, что функция читает XLSX-файл и возвращает список словарей
    с данными о финансовых транзакциях
    :param mock_read_excel:
    :return:
    """

    sample_data = {"Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"], "Сумма операции с округлением": [160.89, 64.00]}
    mock_data = pd.DataFrame(sample_data)
    mock_read_excel.return_value = mock_data
    result = get_read_excel("sample")
    expected = [
        {"Дата операции": "31.12.2021 16:44:00", "Сумма операции с округлением": 160.89},
        {"Дата операции": "31.12.2021 16:42:04", "Сумма операции с округлением": 64.00},
    ]
    assert result == expected


@patch("pandas.read_excel")
def test_get_read_excel_invalid(mock_read_excel: pd.DataFrame):
    """
    Проверяет, что функция читает пустой XLSX-файл и возвращает пустой список
    :param mock_read_excel:
    :return:
    """
    mock_data = pd.DataFrame(None)
    mock_read_excel.return_value = mock_data
    result = get_read_excel("sample")
    expected = []
    assert result == expected


def test_get_read_excel_file_not_found_error():
    """Проверяет, что при отсутствии XLSX-файла для чтения данных, функция
    выбрасывает исключение `FileNotFoundError`"""
    with pytest.raises(FileNotFoundError) as exc_info:
        get_read_excel(r"\data\operations.xlsx")
    assert str(exc_info.value) == "Function get_read_excel error: FileNotFoundError"


def test_get_read_excel_value_error():
    """Проверяет, что при чтении файла неподходящего формата, функция
        выбрасывает исключение `ValueError`"""
    with pytest.raises(ValueError) as exc_info:
        get_read_excel(path_file("data", "operations_error.json"))

    assert str(exc_info.value) == "Function get_read_excel error: Excel file format cannot be determined, you must specify an engine manually."
