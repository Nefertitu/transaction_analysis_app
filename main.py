import re

from src.reports import spending_by_workday
from src.services import get_investment_bank
from src.utils import get_read_excel, path_file, get_required_columns, get_formatted_date, update_user_settings
from src.views import get_event_page


user_transactions = get_read_excel(path_to_file=path_file("data", "operations.xlsx"))


# Страница "События":
def main_events() -> str:
    """Функция отвечает за основную логику страницы "События" и связывает
    функциональности страницы между собой"""

    print("\nПривет! Добро пожаловать в программу работы с банковскими транзакциями.\n")

    print("\nПриветствуем на странице 'События'!")

    user_date = ""
    time_range = ""
    user_currencies = ""
    user_stocks = ""
    user_date = ""
    user_range = ""

    answer_1 = input("\nЖелаете получить информацию о доходах/расходах? (Да/Нет): ")
    answer = ["да", "нет"]
    while answer_1.lower() not in answer:
            input("\nВведите 'Да' или 'Нет'.")

    # определение периода и даты для вывода данных о доходах/расходах:
    if answer_1.lower() == "да":
        print("""\nВведите дату, по состоянию на которую требуются данные, и период, 
    который следует отобразить в отчете""")

        user_input = input("\nДата (в формате ГГГГ-ММ-ДД): ")
        pattern = r'\b(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[01])\b'
        while re.search(pattern, user_input) is None:
            user_input = input("\nВведите дату в формате ГГГГ-ММ-ДД: ")

        user_date += user_input

        answer = ["неделя", "месяц", "год", "все данные"]
        user_input = input("\nОтчетный период ('неделя', 'месяц', 'год', 'все данные'): ")
        while user_input.lower() not in answer:
            user_input = input("\nВведите период ('неделя', 'месяц', 'год' или 'все данные'): ")
        if user_input.lower() == "неделя":
            user_range = "W"
            time_range += user_range
        elif user_input.lower() == "месяц":
            user_range = "M"
            time_range += user_range

        elif user_input.lower() == "год":
            user_range = "Y"
            time_range += user_range

        elif user_input.lower() == 'все данные':
            user_range = "ALL"
            time_range += user_range


    elif answer_1 == "нет":
        print("")

    # user_transactions = get_read_excel(path_to_file=path_file("data", "operations.xlsx"))

    # вывод информации о курах валют и стоимости акций:
    answer_currencies = input("\nЖелаете получить информацию о текущем курсе валют? (Да/Нет): ")
    answer = ["да", "нет"]
    while answer_currencies.lower() not in answer:
        answer_currencies = input("\nВведите 'Да' или 'Нет': ")

    if answer_currencies.lower() == "да":
        user_input = list(input("\nВведите код валюты для получения текущего курса ('USD', 'EUR' и т.д.): "))
        pattern = r"\b[A-Z]{3}\b"
        while re.search(pattern, (str(user_input)).upper()) is None:
            user_input = list(input("\nВведите код валюты ('USD', 'EUR' и т.д.): "))

        user_currencies += user_input

    elif answer_currencies.lower() == "нет":
        print("")

    answer_stocks = input("\nЖелаете получить информацию о текущей стоимости акций? (Да/Нет): ")
    answer = ["да", "нет"]
    while answer_stocks.lower() not in answer:
        answer_stocks = input("\nВведите 'Да' или 'Нет': ")

    if answer_stocks.lower() == "да":
        user_input = list(input("""\nВведите тикеры(названия) интересующих акций ('AAPL', 'AMZN', 
    'GOOGL', 'MSFT', 'TSLA' и др.)"""))
        pattern = r"\b[A_Z]{1, 6}\b"
        while re.search(pattern, (str(user_input)).upper()) is None:
            user_input = list(input("""\nВведите тикеры(названия) акций ('AAPL', 'AMZN', 
        'GOOGL', 'MSFT', 'TSLA' и др.)"""))

        user_stocks += user_input

    if answer_stocks.lower() == "нет":
        print("")

    print(update_user_settings(list(user_currencies), list(user_stocks)))

    print("\nРаспечатываю итоговые данные... ")

    user_data = get_event_page(user_transactions, user_date, user_range)

    return user_data


user_transactions_1 = get_required_columns(user_transactions, ["Дата операции", "Сумма операции"])
user_transactions_2 = get_formatted_date(user_transactions_1)


# "Инвесткопилка":
def main_investment() -> float | str:
    """Функция для взаимодействия с сервисом 'Инвесткопилка'"""

    print("\nПредставляем Вашему вниманию сервис 'Инвесткопилка'")

    answer_1 = input("\nЖелаете узнать сумму возможных накоплений? (Введите: Да/Нет): ")

    # user_date = ""
    # user_limit = ""

    answer = ["да", "нет"]
    while answer_1.lower() not in answer:
        input("\nВведите 'Да' или 'Нет'.")

    if answer_1.lower() == "нет":
        return "Завершение работы приложения."

    if answer_1.lower() == "да":
        print("""\nВведите месяц для которого будет рассчитана отложенная сумма 
    (в формате 'ГГГГ-ММ')""")
    user_date = input("\nДата (в формате 'ГГГГ-ММ'): ")
    pattern = r'\b(\d{4})-([1-9]|1[0-2])\b'
    while re.search(pattern, user_date) is None:
        user_date = input("\nВведите дату в формате ГГГГ-ММ-ДД: ")
    # user_date += user_date

    user_limit = int(input("\nВведите лимит округления - 10, 50 или 100 (рублей): "))
    answer = [10, 50, 100]
    while user_limit not in answer:
        user_limit = int(input("\nВведите лимит округления - 10, 50 или 100: "))
    # user_limit += user_limit

    user_data = get_investment_bank(user_date, user_transactions_2, int(user_limit))

    print("\nРаспечатываю итоговые данные... ")

    return user_data

# Траты в рабочий и выходной день:
def main_spending_by_workday() -> str:
    """Функция для взаимодействия с сервисом 'Траты в рабочий/входной день'"""

    print("\nПредтавляем вашему вниманию сервис 'Траты в рабочий/входной день'")

    user_date = ""

    answer_1 = input("""\nЖелаете узнать среднюю сумму трат в рабочий или в выходной
день? Расчет произвоится за посление 3 месяца от отчетной даты? (Введите: Да/Нет): """)

    answer = ["да", "нет"]
    while answer_1.lower() not in answer:
        input("\nВведите 'Да' или 'Нет'.")

    if answer_1.lower() == "нет":
        return "Завершение работы приложения."

    if answer_1.lower() == "да":
        answer_date = input("""Желаете установить в качестве отчетной текущую дату? 
(Введите: Да/Нет)""")

        answer = ["да", "нет"]
        while answer_date.lower() not in answer:
            answer_date = input("\nВведите 'Да' или 'Нет'.")
        if answer_date.lower() == "да":
            print("\nВыбрана текущая дата.")
        user_date = None

        if answer_date == "нет":
            user_input = input("Введите дату отсчета трехмесячного периода в формате 'ГГГГ-ММ-ДД: '")
            pattern = r'\b(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[01])\b'
            while re.search(pattern, user_input) is None:
                user_input = input("\nВведите дату в формате ГГГГ-ММ-ДД: ")
            user_date += user_input

    user_data = spending_by_workday(user_transactions_2, user_date)
    user_data_json = user_data.to_json(orient="records", indent=4, lines=True, force_ascii=False)
    print("\nРаспечатываю итоговые данные... ")

    return user_data_json




