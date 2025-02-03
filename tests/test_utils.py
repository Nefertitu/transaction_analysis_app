import pytest

from unittest.mock import patch

import pandas as pd


from pandas import DataFrame
from src.utils import get_read_excel, path_file

from tests.conftest import data_for_test_pd_result, params


@patch("pandas.read_excel")
def test_get_read_excel(mock_read_excel: str, data_for_test_pd_result: DataFrame) -> None:
    """
    Проверяет, что функция корректно обрабатывает XLSX-файлы
    :param mock_read_excel:
    :param data_for_test_pd_result:
    :return:
    """
    mock_read_excel.return_value = data_for_test_pd_result
    result = get_read_excel("test.xlsx")
    pd.testing.assert_frame_equal(result, data_for_test_pd_result)


@patch("pandas.read_excel")
def test_get_read_excel_empty(mock_read_excel, data_for_test_pd_result_empty):
    """
    Проверяет, что функция читает пустой XLSX-файл и возвращает пустой список
    :param mock_read_excel:
    :return:
    """
    mock_read_excel.return_value = data_for_test_pd_result_empty
    result = get_read_excel("test.xlsx")
    pd.testing.assert_frame_equal(result, data_for_test_pd_result_empty)


@patch("pandas.read_excel")
@pytest.mark.parametrize("input_data, expected_output", params)
def test_get_read_excel_replace(mock_read_excel, input_data, expected_output):
    """
    Проверяет, что функция заменяет значения в пустых ячейках XLSX-файла на установленные и
    возвращает DataFrame или Series с измененными значениями
    в пустых ячейках
    """
    mock_read_excel.return_value = input_data
    result = get_read_excel("test.xlsx")
    pd.testing.assert_frame_equal(result, expected_output, check_frame_type=False, check_dtype=False)


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

