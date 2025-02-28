import json
from pathlib import Path


def path(file_name):
    return str(Path(__file__).parent.joinpath(f"resources/{file_name}"))


def load_json_data(file_name):
    """
    Загружает данные из JSON-файла.
    """
    file_path = path(file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
