from os.path import dirname

import pandas as pd
from pathlib import Path


def path_file(my_directory: str, my_filename: str) -> Path:
    "Получение абсолютного пути к фалу"
    ROOT_DIR = Path(__file__).parent.parent
    filepath = ROOT_DIR/my_directory/my_filename
    return filepath

# print(path_file("src", "utils.py"))


def get_read_excel(path_to_file: str | Path) -> str | list[dict]:
    """
    Считывание данных о финансовых операциях из файла Excel
    :param path_to_file:
    :return:
    """
    try:
        data_transactions = pd.read_excel(path_to_file)
        # print(data_transactions)

    except FileNotFoundError as exc_info:
        raise FileNotFoundError(f"Function {get_read_excel.__name__} error: {type(exc_info).__name__}")
    except ValueError as exc_info:
        raise ValueError(f"Function {get_read_excel.__name__} error: {str(exc_info)}")

    else:
        return data_transactions.head().to_dict(orient="records")
        # return data_transactions.head().to_json(orient='records', indent=4, lines=True, force_ascii=False)


# trans = get_read_excel(r"..\data\operations.xlsx")
# trans = get_read_excel(r"..\data\operations_error.json")
# print(trans)


# # Указываем правильный путь
# directory_path = r'C:\Users\Oper\PycharmProjects\pythonProject\transaction_analysis_app\data'
#
# # Проверяем существование директории
# if not os.path.exists(directory_path):
#     print(f"Папка {directory_path} не найдена.")
# else:
#     # Получаем список файлов в директории
#     directory_files = os.listdir(directory_path)
#     for file in directory_files:
#         print(file)
