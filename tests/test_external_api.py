from unittest.mock import Mock, patch, MagicMock

import pytest
import requests.exceptions
from requests.exceptions import Timeout

from src.external_api import get_exchange_rate, get_stock_prices


@patch("requests.get")
def test_get_exchange_rate_success(mock_requests, apilayer_responses):
    """
    Проверяет, что функция, обращаясь к API сайта: 'https://api.apilayer.com/',
    возвращает курсы доллара(USD) и евро(EUR)
    :param mock_requests:
    :param apilayer_responses:
    :return:
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = lambda: apilayer_responses.pop(0)

    mock_requests.return_value = mock_response

    expected_result = {"USD": {"currency": "USD", "rate": 96.87},
                       "EUR": {"currency": "EUR", "rate": 100.50}}

    assert get_exchange_rate() == expected_result


@patch("requests.get")
def test_get_exchange_rate_raises_timeout(mocked_get):
    """
    Проверяет, что при возникновении ошибки `Timeout`, когда запрос не получил
    ответа в течение заданного времени, функция возвращает соответствующее сообщение.
    :param mocked_get:
    :return:
    """
    mocked_get = Mock(status_code=408)
    requests.get = mocked_get
    mocked_get.side_effect = Timeout("Request timed out. Please check your internet connection.")
    assert get_exchange_rate() == "Request timed out. Please check your internet connection."


@patch("requests.get")
def test_get_exchange_rate_http_error(mocked_get):
    """
    Проверяет, что при возникновении ошибки `HTTPError`, когда полученный ответ
    от сервера не является корректным HTTP-ответом, функция возвращает
    соответствующее сообщение.
    :param mocked_get:
    :return:
    """
    mocked_get = Mock(status_code=403)
    requests.get = mocked_get
    mocked_get.side_effect = requests.HTTPError("HTTP Error. Please check the URL.")
    assert get_exchange_rate() == "HTTP Error. Please check the URL."


@patch("requests.get")
def test_get_exchange_rate_connection_error(my_mock):
    """Проверяет, что при возникновении ошибки `ConnectionError`, когда запрос не может быть выполнен из-за проблем
    с сетью, функция возвращает соответсвующее сообщение"""
    requests.get.side_effect = requests.exceptions.ConnectionError
    my_mock.side_effect = ConnectionError("ConnectionError. Please check your internet connection.")
    with pytest.raises(ConnectionError):
        get_exchange_rate()


@patch("requests.get")
def test_get_sock_prices_negative(mock_response):
    """Проверяет, что функция, обращаясь к API сайта: `https://site.financialmodelingprep.com/`,
    возвращает стоимость акций из списка"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    requests.get.return_value = mock_response

    expected_result = "Ошибка при получении данных для ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']: код статуса 404, Not Found"

    assert get_stock_prices() == expected_result


@patch("requests.get")
def test_get_sock_prices_succsess(mock_requests, financialmodel_responses):
    """Проверяет, что функция, обращаясь к API сайта: `https://site.financialmodelingprep.com/`,
    возвращает стоимость акций из списка"""

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = lambda: financialmodel_responses.pop(0)

    mock_requests.return_value = mock_response

    expected_result = {"AAPL": {"stock": "AAPL", "price": 150.15},
                       "AMZN": {"stock": "AMZN", "price": 3173.18},
                       "GOOGL": {"stock": "GOOGL", "price": 2742.39},
                       "MSFT": {"stock": "MSFT", "price": 296.71},
                       "TSLA": {"stock": "TSLA", "price": 1007.08}}

    assert get_stock_prices() == expected_result