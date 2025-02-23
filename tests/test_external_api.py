import json
from unittest.mock import Mock, patch, MagicMock, mock_open

import pytest
import requests.exceptions
from requests.exceptions import Timeout

from src.external_api import get_exchange_rate, get_stock_prices


@patch('requests.get')
@patch('builtins.open', new_callable=MagicMock)
def test_get_exchange_rate_success(mock_open, mock_requests, apilayer_responses, json_user_settings):
    """
    Проверяет, что функция, читает JSON-файл с пользовательскими параметрами и,
    обращаясь к API сайта: 'https://api.apilayer.com/',
    возвращает курсы валют из списка
    :param mock_open:
    :param mock_requests:
    :param apilayer_responses:
    :param json_user_settings:
    :return:
    """
    file_mock = mock_open.return_value.__enter__.return_value
    file_mock.read.return_value = json.dumps(json_user_settings)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = lambda: apilayer_responses.pop(0)
    mock_requests.return_value = mock_response

    expected_result = {"USD": {"currency": "USD", "rate": 96.87}, "EUR": {"currency": "EUR", "rate": 100.50}}

    result = get_exchange_rate("sample.json")

    assert result == expected_result


@patch('builtins.open')
@patch("requests.get")
def test_get_exchange_rate_raises_timeout(mocked_get, mock_open, json_user_settings):

    file_mock = mock_open.return_value.__enter__.return_value
    file_mock.read.return_value = json.dumps(json_user_settings)

    mocked_response = Mock()
    mocked_response.status_code = 408
    mocked_get.side_effect =  Timeout("Request timed out. Please check your internet connection.")
    mocked_get.return_value = mocked_response

    result = get_exchange_rate("sample.json")

    assert result == "Request timed out. Please check your internet connection."


@patch('builtins.open', new_callable=MagicMock)
@patch("requests.get")
def test_get_exchange_rate_http_error(mock_open, mocked_get, json_user_settings):
    """
    Проверяет, что при возникновении ошибки `HTTPError`, когда полученный ответ
    от сервера не является корректным HTTP-ответом, функция возвращает
    соответствующее сообщение.
    :param mock_open:
    :param mocked_get:
    :param json_user_settings:
    :return:
    """

    file_mock = mock_open.return_value.__enter__.return_value
    file_mock.read.return_value = json.dumps(json_user_settings)

    mocked_response = Mock()
    mocked_response.status_code = 403
    mocked_get.side_effect = requests.HTTPError("HTTP Error. Please check the URL.")

    mocked_get.return_value = mocked_response

    with pytest.raises(requests.HTTPError):
        get_exchange_rate("sample.json")


@patch('builtins.open')
@patch("requests.get")
def test_get_exchange_rate_connection_error(my_mock, mock_open, json_user_settings):
    """Проверяет, что при возникновении ошибки `ConnectionError`, когда запрос не может быть выполнен из-за проблем
    с сетью, функция возвращает соответсвующее сообщение"""

    file_mock = mock_open.return_value.__enter__.return_value
    file_mock.read.return_value = json.dumps(json_user_settings)

    requests.get.side_effect = requests.exceptions.ConnectionError
    my_mock.side_effect = ConnectionError("ConnectionError. Please check your internet connection.")
    with pytest.raises(ConnectionError):
        get_exchange_rate("sample.json")


@patch('builtins.open', new_callable=MagicMock)
@patch("requests.get")
def test_get_sock_prices_negative(mock_open, mocked_get, json_user_settings, capsys):
    """Проверяет, что функция, в случае ошибки сайта (при обращении к API
    сайта: `https://site.financialmodelingprep.com/`), вызовет HTTPError"""

    file_mock = mock_open.return_value.__enter__.return_value
    file_mock.read.return_value = json.dumps(json_user_settings)

    requests.get.side_effect = requests.exceptions.HTTPError
    mocked_response = Mock()
    mocked_response.status_code = 404
    mocked_get.side_effect = requests.HTTPError("Not Found")

    mocked_get.return_value = mocked_response

    with pytest.raises(requests.HTTPError):
        get_exchange_rate("sample.json")

        print(get_exchange_rate("sample.json"))
        captured = capsys.readouterr()
        assert captured.out == "Ошибка при получении данных для ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']: код статуса 404, Not Found\n"


@patch('builtins.open', new_callable=MagicMock)
@patch("requests.get")
def test_get_sock_prices_succsess(mock_requests, mock_open, financialmodel_responses, json_user_settings):
    """Проверяет, что функция, обращаясь к API сайта: `https://site.financialmodelingprep.com/`,
    возвращает стоимость акций из списка"""

    file_mock = mock_open.return_value.__enter__.return_value
    file_mock.read.return_value = json.dumps(json_user_settings)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = lambda: financialmodel_responses.pop(0)

    mock_requests.return_value = mock_response

    expected_result = {"AAPL": {"stock": "AAPL", "price": 240.86},
                       "AMZN": {"stock": "AMZN", "price": 229.65},
                       "GOOGL": {"stock": "GOOGL", "price": 184.67},
                       "MSFT": {"stock": "MSFT", "price": 409.42},
                       "TSLA": {"stock": "TSLA", "price": 352.91}}

    assert get_stock_prices("sample.json") == expected_result