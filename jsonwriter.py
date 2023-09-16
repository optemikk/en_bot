import json


# Функция для чтения файла JSON
def read_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


# Функция для записи в файл JSON
def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


# Функция для обновления файла JSON
def update_json(file_path, key, value):
    data = read_json(file_path)
    data[key] = value
    write_json(file_path, data)

if __name__ == "__main__":
    write_json(file_path='stats.json', data={})