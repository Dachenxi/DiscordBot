import json
import os

def load_json(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    return data

def save_json(file_path: str, data: dict) -> None:
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def update_json(file_path: str, key: str, value) -> None:
    data = load_json(file_path)
    data[key] = value
    save_json(file_path, data)
    
def delete_key_from_json(file_path: str, key: str) -> None:
    data = load_json(file_path)
    if key in data:
        del data[key]
        save_json(file_path, data)


def get_value_json(file_path: str, key: str):
    data = load_json(file_path)
    return data.get(key, None)