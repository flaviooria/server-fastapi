import json


def read_json(path: str) -> list | dict:
    with open(path) as file:
        data = json.load(file)

    return data

def search_user(id: int,users_list: list):
    users = list(filter(lambda user: user.id == id,users_list))
    try: 
        return users[0] 
    except:
        return {'error': 'No se ha encontrado el usuario'}
