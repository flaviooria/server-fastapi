import json


def read_json() -> list | dict:
    with open('users.json') as file:
        data = json.load(file)

    return data

