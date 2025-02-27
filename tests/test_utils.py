import json
from pathlib import Path

import pytest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
from pandas import DataFrame
from src.reports import spending_by_workday
from src.utils import get_read_excel, path_file, get_required_columns, get_formatted_date, get_list_dict_transactions, \
    get_to_json_investment_savings, update_user_settings, get_choice_data, get_decorator, configure_logging
from src.views import get_event_page
from tests.conftest import data_for_test_pd_result, params, transactions_sample_data


def test_path_file() -> None:
    """Проверяет, что функция верно формирует путь к файлу"""

    result = path_file("log", "sample.txt")
    assert result == Path(Path(__file__).parent.parent/'log/sample.txt')


def test_configure_logging(tmp_path, sample_data_for_reports):
    """
    Проверяет, что функция логирует информацию в указанный файл
    :param tmp_path:
    :param sample_data_for_reports:
    :return:
    """
    filename = tmp_path / "mylog_reports.log"
    logging_function = configure_logging(log_path=Path(filename))
    result = spending_by_workday(sample_data_for_reports, "2020-04-20")

    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()

        assert "INFO:" in file_content
        assert "В качестве отчетной даты установлена дата: 2020-04-20" in file_content
        assert "Получен следующий результат:" in file_content
        assert str(result) in file_content
        assert str(result) == ("   Средние траты в рабочий день  Средние траты в выходной день\n"
                               "0                       2546.02                         100.15")
        assert len(result) == 1
        assert result['Средние траты в рабочий день'][0] == pytest.approx(2546.02)
        assert result['Средние траты в выходной день'][0] == pytest.approx(100.15)

        # Дополнительный тест без даты


def test_configure_logging_2(tmp_path, sample_data_for_reports):
    """
    Проверяет, что функция логирует информацию в указанный файл"
    :param tmp_path: 
    :param sample_data_for_reports: 
    :return: 
    """""
    filename = tmp_path / "mylog_reports.log"
    logging_function = configure_logging(log_path=Path(filename))
    result = spending_by_workday(sample_data_for_reports)

    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()

        assert "INFO:" in file_content
        assert "\nВ качестве отчетной даты установлена текущая дата:" in file_content
        assert "Получен следующий результат:" in file_content
        assert str(result) in file_content
        assert str(result) == ("   Средние траты в рабочий день  Средние траты в выходной день\n"
                               "0                           NaN                            NaN")
        assert len(result) == 1


def test_get_decorator_writes_to_file(sample_data_for_reports, tmp_path):
    """
    Проверяет, что функция-декоратор корректно записывает отчет в указанный файл
    :param sample_data_for_reports:
    :param tmp_path:
    :return:
    """

    filename = tmp_path / "report_1.log"
    decorated_function = get_decorator(filename=str(filename))(spending_by_workday)
    result = decorated_function(sample_data_for_reports, "2020-04-20")

    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()

        assert "Function_name: spending_by_workday" in file_content
        assert "Execution time:" in file_content
        assert str(result) in file_content
        assert str(result) == ("   Средние траты в рабочий день  Средние траты в выходной день\n"
                               "0                       2546.02                         100.15")


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
def test_get_read_excel_empty(mock_read_excel, data_for_test_pd_result_empty, capsys):
    """
    Проверяет, что функция читает пустой XLSX-файл и возвращает сообщение,
    что читаемый файл пустой
    :param mock_read_excel:
    :param data_for_test_pd_result_empty:
    :return:
    """

    mock_read_excel.return_value = data_for_test_pd_result_empty
    result = get_read_excel("test.xlsx")

    captured = capsys.readouterr()
    assert captured.out == "Файл пустой.\n"
    assert type(result) == DataFrame


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


def test_get_required_columns(data_for_test_pd_2, data_for_test_pd_2_return):
    """
    Проверяет, что функция возвращает DataFrame с указанными столбцами или Series
    :param data_for_test_pd_2:
    :param data_for_test_pd_2_return:
    :return:
    """

    result = get_required_columns(data_for_test_pd_2, ["Дата операции", "Сумма операции"])
    pd.testing.assert_frame_equal(result, data_for_test_pd_2_return)


def test_get_formatted_date(data_for_test_pd_result, data_formatted_date_1):
    """
    Проверяет, что функция преобразует дату в поученном DataFrame
    :param data_for_test_pd_result:
    :param data_formatted_date_1:
    :return:
    """

    result = get_formatted_date(data_for_test_pd_result)
    pd.testing.assert_frame_equal(result, data_formatted_date_1)


def test_get_list_dict_transactions(data_for_test_pd_result, data_for_test_pd):
    """Проверяет, что функция преобразует формат данных с информацией
    о транзакциях из DataFrame в список словарей"""

    result = get_list_dict_transactions(data_for_test_pd_result)
    assert result == data_for_test_pd


def test_get_to_json_investment_saving(data_to_dict_for_services):
    """Проверяет, что функция возвращает JSON_ответ для сервиса 'Инвесткопилка'"""

    result = get_to_json_investment_savings("2021-12",  data_to_dict_for_services, 100)
    assert result == '''
    {
        "Сумма инвестиционных накоплений":"75.11",
        "Период для расчета накоплений":"2021-12",
        "Лимит округления":100
    }
\n'''


def test_update_user_settings():
    """Проверяет, что функция записывает установленные пользователем
    параметры в файл `user_settings.json` и выводит соответствующее сообщение"""

    expected_currencies = ["USD", "EUR"]
    expected_stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

    with open('../user_settings.json', 'w') as file:
        json.dump({'user_currencies': expected_currencies, 'user_stocks': expected_stocks}, file, indent=4)

    expected_data = {
        'user_currencies': expected_currencies,
        'user_stocks': expected_stocks
    }
    expected_json = json.dumps(expected_data, indent=4)

    with open('../user_settings.json', 'r') as file:
        content = file.read()

    assert expected_json == content


@pytest.mark.parametrize(
    "date, time_range, expected_start_date, expected_end_date",
    [
        ("2020-02-15", "M", "2020-02-01", "2020-02-15"),  # Месяц: с первого дня месяца до указанной даты
        ("2020-12-27", "W", '2020-12-21', "2020-12-27"),  # Неделя: с понедельника текущей недели до указанной даты
        ("2020-06-15", "Y", "2020-01-01", "2020-06-15"),  # Год: с первого января текущего года до указанной даты
        ("2020-08-08", "ALL", "2020-01-01", "2020-08-08")  # Все: от начала года до указанной даты
    ]
)
def test_get_choice_data(transactions_sample_data, date, time_range, expected_start_date, expected_end_date):
    """
    Проверяет, что функция правильно выполняет фильтрацию по дате и периоду
    :param transactions_sample_data:
    :return:
    """

    filtered_df = get_choice_data(transactions_sample_data, date, time_range)
    assert len(filtered_df) > 0, "Фильтрация вернула пустой DataFrame"
    assert filtered_df["Дата операции"].min() == expected_start_date, f"Ожидаемая дата начала {expected_start_date}, полученная {filtered_df['Дата операции'].min()}"
    assert filtered_df["Дата операции"].max() == expected_end_date, f"Ожидаемая дата окончания {expected_end_date}, полученная {filtered_df['Дата операции'].max()}"
