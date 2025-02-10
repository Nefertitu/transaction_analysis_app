import logging
from datetime import datetime
from functools import wraps
from typing import Callable, Any

logging.basicConfig(level=logging.INFO,
                    filename='.log//mylog.txt',
                    filemode='a',
                    format='%(levelname)s: %(asctime)s - %(funcName)s() - %(message)s')


def get_log_decorator(filename: str = '.log/report.txt') -> Callable[[Callable], Callable]:
    """
    Декоратор для записи отчетов результатов выполнения функций
    :param filename: Имя файла для записи отчетов
    :return: Декорированная функция
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logging.info(f"Starting {function.__name__} with arguments: {args}, {kwargs}")
            try:
                start_time = datetime.now()
                result = function(*args, **kwargs)
                end_time = datetime.now()

                logging.info(f"{function.__name__} completed successfully.")

                with open(filename, 'a') as file:
                    file.write(
                        f"{function.__name__} with args: {args} and kwargs: {kwargs}.\n"
                        f"Result = {result}.\n"
                        f"Function call time: {start_time}.\n"
                        f"Execution time: {(end_time - start_time).total_seconds():.7f}\n\n"
                    )

                return result

            except Exception as exc_info:
                logging.error(f"{function.__name__} failed with exception: {exc_info}. Arguments: {args}, {kwargs}.")

                with open(filename, 'a') as file:
                    file.write(
                        f"{function.__name__} error: {type(exc_info).__name__}: {str(exc_info)}.\n"
                        f"Inputs: {args}, {kwargs}\n\n"
                    )

                raise

        return wrapper

    return decorator

