import re
from pathlib import Path
from typing import Any

from src.reports import spending_by_workday
from src.utils import (
    get_formatted_date,
    get_list_dict_transactions,
    get_read_excel,
    get_required_columns,
    get_to_json_investment_savings,
    get_to_json_views,
    path_file,
    update_user_settings, configure_logging,
)
from src.views import get_event_page


# Страница "События":
def main_events(path_to_file: str | Path) -> str:
    """Функция отвечает за основную логику страницы "События" и связывает
    функциональности страницы между собой"""

    time_range = ""
    user_currencies = []
    user_stocks = []
    user_date = ""
    user_range = ""
    user_data_json = ""

    answer_1 = input(
        """\nПривет! Добро пожаловать в программу работы с банковскими транзакциями!\n
Приветствуем на странице 'События'!\n
Желаете получить информацию о доходах/расходах? (Да/Нет): """
    )
    answers = ["да", "lf", "нет", "ytn"]
    while answer_1.lower() not in answers:
        input("\nВведите 'Да' или 'Нет': ")

    # определение периода и даты для вывода данных о доходах/расходах:
    if answer_1.lower() == "да" or answer_1.lower() == "lf":

        user_input = input(
            """\nВведите дату, по состоянию на которую требуются данные,
и период, который следует отобразить в отчете.\n\nДата (в формате ГГГГ-ММ-ДД): """
        )
        pattern = r"\b(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[01])\b"
        while re.search(pattern, user_input) is None:
            user_input = input("\nВведите дату в формате ГГГГ-ММ-ДД: ")

        user_date += user_input

        answer = ["неделя", "ytltkz", "месяц", "vtczw", "год", "ujl", "все данные", "dct lfyyst"]
        user_input = input("\nОтчетный период ('неделя', 'месяц', 'год', 'все данные'): ")
        while user_input.lower() not in answer:
            user_input = input("\nВведите период ('неделя', 'месяц', 'год' или 'все данные'): ")
        if user_input.lower() == "неделя" or user_input.lower() == "ytltkz":
            user_range = "W"
            time_range += user_range
        elif user_input.lower() == "месяц" or user_input.lower() == "vtczw":
            user_range = "M"
            time_range += user_range

        elif user_input.lower() == "год" or user_input.lower() == "ujl":
            user_range = "Y"
            time_range += user_range

        elif user_input.lower() == "все данные" or user_input.lower() == "dct lfyyst":
            user_range = "ALL"
            time_range += user_range

        # вывод информации о курах валют и стоимости акций:
        answer_currencies = input("\nЖелаете получить информацию о текущем курсе валют? (Да/Нет): ")
        answer = ["да", "lf", "нет", "ytn"]
        while answer_currencies.lower() not in answer:
            answer_currencies = input("\nВведите 'Да' или 'Нет': ")

        if answer_currencies.lower() == "да" or answer_currencies.lower() == "lf":
            user_input = input("\nВведите код валюты для получения текущего курса (USD, EUR и т.д.): ")
            pattern = r"\b[A-Z]{3}\b(?:\s*,\s*|\s+)"
            while re.search(pattern, (str(user_input)).upper()) is None:
                user_input = input("\nВведите код валюты (USD, EUR и т.д.): ")

            user_currencies += [currency.strip() for currency in user_input.split(",")]

        elif answer_currencies.lower() == "нет" or answer_currencies.lower() == "ytn":
            user_currencies += []

        answer_stocks = input("\nЖелаете получить информацию о текущей стоимости акций? (Да/Нет): ")
        answer = ["да", "lf", "нет", "ytn"]
        while answer_stocks.lower() not in answer:
            answer_stocks = input("\nВведите 'Да' или 'Нет': ")

        if answer_stocks.lower() == "да" or answer_stocks.lower() == "lf":
            user_input = input("""\nВведите тикеры(названия) интересующих акций \n(AAPL, AMZN, GOOGL, MSFT, TSLA и др.): """)
            pattern = r"\b[A_Z]{1, 6}\b(?:\s*,\s*|\s+)"
            while re.findall(pattern, (str(user_input)).upper()) is None:
                user_input = input("""\nВведите тикеры(названия) акций \n(AAPL, AMZN, GOOGL, MSFT, TSLA и др.): """)

            user_stocks += [ticker.strip() for ticker in user_input.split(",")]

        elif answer_stocks.lower() == "нет" or answer_stocks.lower() == "ytn":
            user_stocks += []

        user_data = get_read_excel(path_to_file)

        user_settings_json = update_user_settings(user_currencies, user_stocks)
        print(user_settings_json)
        user_data_formatted_date = get_formatted_date(user_data)
        user_data_dict = get_event_page(user_data_formatted_date, user_date, user_range)

        user_data_json += get_to_json_views(user_data_dict)

    elif answer_1.lower() == "нет":
        user_data_json += "Завершение программы"

    print("\nРаспечатываю итоговые данные... ")

    return f"\n\n{user_data_json}"


# "Инвесткопилка":
def main_investment(path_to_file: str | Path) -> str | Any:
    """Функция для взаимодействия с сервисом 'Инвесткопилка'"""

    answer_1 = input("""\nПредставляем Вашему вниманию сервис 'Инвесткопилка'.\n
Желаете узнать сумму возможных накоплений? (Введите: Да/Нет): """)

    user_date = ""
    user_limit = 0

    answer = ["да", "lf", "нет", "ytn"]
    while answer_1.lower() not in answer:
        input("\nВведите 'Да' или 'Нет'.")

    if answer_1.lower() == "нет" or answer_1.lower() == "ytn":
        return "Завершение работы приложения."

    if answer_1.lower() == "да" or answer_1.lower() == "lf":
        user_input = input("""\nОпределите месяц для которого будет рассчитана отложенная сумма.\n(Введите дату в формате 'ГГГГ-ММ'): """)
        pattern = r"\b(\d{4})-(0[1-9]|1[0-2])\b"
        while re.search(pattern, user_input) is None:
            user_input = input("\nВведите дату в формате ГГГГ-ММ: ")
        user_date += user_input

    user_limit_input = input("\nВведите лимит округления - 10, 50 или 100 (рублей): ")
    answer = ["10", "50", "100"]
    while user_limit_input not in answer:
        user_limit_input = input("\nВведите лимит округления - 10, 50 или 100: ")
    user_limit += int(user_limit_input)

    user_transactions = get_read_excel(path_to_file)
    user_transactions_1 = get_required_columns(user_transactions, ["Дата операции", "Сумма операции"])
    user_transactions_2 = get_formatted_date(user_transactions_1)
    transactions_dict = get_list_dict_transactions(user_transactions_2)
    user_data = get_to_json_investment_savings(user_date, transactions_dict, user_limit)

    print("\nРаспечатываю итоговые данные... ")

    return f"\n{user_data}"


# Траты в рабочий и выходной день:
def main_spending_by_workday(path_to_file: str | Path) -> str | Any:
    """Функция для взаимодействия с сервисом 'Траты в рабочий/входной день'"""

    user_date = ""

    answer_1 = input(
        """\nПредставляем вашему вниманию сервис 'Траты в рабочий/входной день'.
\nЖелаете узнать среднюю сумму трат в рабочий или в выходной день?
Расчет производится за последние 3 месяца от отчетной даты.
(Введите: Да/Нет): """
    )

    answer = ["да", "lf", "нет", "ytn"]
    while answer_1.lower() not in answer:
        input("\nВведите 'Да' или 'Нет'.")

    if answer_1.lower() == "нет" or answer_1.lower() == "ytn":
        return "\nЗавершение работы приложения."

    if answer_1.lower() == "да" or answer_1.lower() == "lf":
        answer_date = input("""\nЖелаете установить в качестве отчетной текущую дату? [ne sovetuju ))]\n(Введите: Да/Нет): """)
        answer = ["да", "lf", "нет", "ytn"]
        while answer_date not in answer:
            answer_date = input("\nВведите 'Да' или 'Нет': ")

        if answer_date == "да" or answer_date == "lf":
            print("\nВыбрана текущая дата.")
            user_date = ""

        elif answer_date == "нет" or answer_date == "ytn":
            user_input = str(input("\nВведите дату отсчета трехмесячного периода в формате 'ГГГГ-ММ-ДД': "))
            pattern = r"\b(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[01])\b"
            while re.search(pattern, user_input) is None:
                user_input = input("\nВведите дату в формате 'ГГГГ-ММ-ДД': ")
            user_date += user_input

    user_transactions = get_read_excel(path_to_file)
    user_transactions_1 = get_required_columns(user_transactions, ["Дата операции", "Сумма операции"])
    user_transactions_2 = get_formatted_date(user_transactions_1)
    user_data = spending_by_workday(user_transactions_2, user_date, logger=configure_logging(path_file("log", "mylog_reports.log")))
    user_data_json = user_data.to_json(orient="records", indent=4, lines=True, force_ascii=False)

    print("\nРаспечатываю итоговые данные... ")

    return user_data_json


if __name__ == "__main__":
    print("\n=====СТРАНИЦА_'СОБЫТИЯ'=====")
    print(main_events(path_to_file=path_file("data", "operations.xlsx")))

    print(input("\n\nДля продолжения работы приложения нажмите `Enter`_"))
    print("\n=====ИНВЕСТКОПИЛКА=====")
    print(main_investment(path_to_file=path_file("data", "operations.xlsx")))

    print(input("\nДля продолжения работы приложения нажмите `Enter`_"))
    print("\n=====ТРАТЫ_В_РАБОЧИЙ_И_ВЫХОДНОЙ_ДЕНЬ=====")
    print(main_spending_by_workday(path_to_file=path_file("data", "operations.xlsx")))

    print("\nЗавершение работы приложения.\n")
