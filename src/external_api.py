import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from src.utils import path_file

load_dotenv()
apilayer_key = os.getenv("API_KEY_1")
alphavantage_key = os.getenv("API_KEY_2")


def get_exchange_rate(path_to_file: str) -> dict | str:
    """
    Возвращает курс доллара(USD) и евро(EUR) в рублях по состоянию на текущую дату,
    обращаясь к сайту: 'https://api.apilayer.com/'
    :return:
    """

    with open(path_to_file) as file:
        user_settings = json.load(file)

    user_currencies = user_settings['user_currencies']

    headers = {"apikey": f"{apilayer_key}"}

    results = {}

    for currency in user_currencies:
        try:
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"

            response = requests.get(url, headers=headers, timeout=5)

            response.raise_for_status()

        except requests.exceptions.Timeout:
            return "Request timed out. Please check your internet connection."

        except requests.exceptions.ConnectionError:
            return "ConnectionError. Please check your internet connection."

        except requests.exceptions.HTTPError:
            return "HTTP Error. Please check the URL."

        else:

            if response.status_code == 200:
                rate = round(response.json()["rates"]["RUB"], 2)
                results[currency] = {'currency': currency, 'rate': rate}

    return results


# print(get_exchange_rate("../user_settings.json"))
#
#
def get_stock_prices(path_to_file: Path | str) -> dict | str:
    """
    Возвращает стоимость акций из установленного списка, обращаясь
    к сайту `https://site.financialmodelingprep.com/`
    :param path_to_file:
    :return:
    """

    with open(path_to_file) as file:
        user_settings = json.load(file)

    user_stocks = user_settings['user_stocks']

    results = {}
    apikey = f"{alphavantage_key}"

    for stock in user_stocks:
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{stock}?apikey={apikey}"
        response = requests.get(url)

        if response.status_code == 200:
            result = response.json()
            for data in result:
                stock = data["symbol"]
                price = round(data["price"], 2)
                results[stock] = {'stock': stock,  "price": price}

        else:
            return (f"Ошибка при получении данных для {user_stocks}: код статуса {response.status_code}, {response.reason}")

    return results


# print(get_stock_prices("../user_settings.json"))