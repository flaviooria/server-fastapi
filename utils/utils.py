import json


def readJson(path: str) -> list | dict:
    with open(path) as file:
        data = json.load(file)

    return data

def writeJson(path: str, mode: str = 'w', *, data: dict):
    try:
        with open(path, mode) as file:
            file.write(json.dumps(data))
    except Exception as e:
        print(e)

def searchUser(id: int,users_list: list):
    users = list(filter(lambda user: user.id == id,users_list))
    try: 
        return users[0] 
    except:
        return {'error': 'No se ha encontrado el usuario'}

def generateToken(username: str, password: str):
    token = ''
    for arg in [username,password]:
        for letter in arg:
            token += f'-{str(ord(letter))}'
    
    return token
