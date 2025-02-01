import pytest

from unittest.mock import patch, mock_open

import pandas as pd

from src.utils import get_read_excel, path_file
from tests.conftest import data_for_test_pd, data_for_test_pd_result


@patch("pandas.read_excel")
def test_get_read_excel(mock_read_excel, data_for_test_pd_result):
    mock_read_excel.return_value = data_for_test_pd_result
    result = get_read_excel("test.xlsx")
    pd.testing.assert_frame_equal(result, data_for_test_pd_result)


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
