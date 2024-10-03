from pathlib import Path
import yaml

BASE_DIR = Path(__file__).parent  # Определение базового каталога относительно местоположения текущего файла

def load_regexes():
    """
    Загружает регулярные выражения и порядок их применения из конфигурационных файлов YAML.

    Returns:
        tuple: Возвращает кортеж, содержащий словарь с регулярными выражениями и список, определяющий порядок их применения.
    """
    regexes = {}
    order_path = BASE_DIR / 'masking_order.yaml'  # Путь к файлу с порядком применения масок
    with open(order_path, 'r', encoding='utf-8') as file:  # Открытие файла порядка маскирования
        order_list = yaml.safe_load(file)["masking_order"]  # Загрузка списка порядка маскирования

    for order in order_list:
        regex_path = BASE_DIR / f'config/{order}.yaml'  # Формирование пути к файлу конфигурации каждого регулярного выражения
        if regex_path.exists():  # Проверка существования файла
            with open(regex_path, 'r', encoding='utf-8') as file:  # Открытие файла конфигурации
                regexes[order] = yaml.safe_load(file)  # Загрузка регулярного выражения из файла
    return regexes, order_list  # Возвращение словаря с регулярными выражениями и списка порядка

# Сохранение результатов загрузки в переменные для использования в других частях программы
regex_patterns, masking_order = load_regexes()

if __name__=="__main__":
    print(load_regexes())  # Вывод загруженных данных при выполнении файла как скрипта
