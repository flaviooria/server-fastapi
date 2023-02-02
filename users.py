from fastapi import FastAPI, Path, Query, Body
from fastapi.requests import Request
from pydantic import BaseModel
from fastapi.routing import APIRoute

app = FastAPI()

# Creamos nuestras entidades, empezamos por user


class User(BaseModel):
    id: int 
    name: str
    surname: str
    url: str
    age: int 


# User's list
users_list = [
    User(id=1,name='Flavio', surname='Oria', url='www.google.com', age=23),
    User(id=2,name='Cesar', surname='Levano', url='www.google.com', age=26),
    User(id=3,name='Gabi', surname='Oria', url='www.google.com', age=23)
]


@app.get('/api')
async def root():
    routes = []
    for route in app.routes:    
        if isinstance(route,APIRoute):
            routes.append({'path': route.path_format, 'method': route.methods})

    return routes

@app.get('/users')
async def users():
    return users_list

# Endpoint con parth
@app.get('/users/{id}')
async def getUsersById(id: int = Path(default=...,alias='id',title='User id',example=1)):
    try:
        founded_user = list(filter(lambda user: user.id == id,users_list))
        return founded_user
    except:
        return {'error': 'No se ha encontrado el usuario'}


# Endpoint con query
@app.get('/users/age/')
async def getUsersByAge(age: int | None = Query(default=None,alias='age',title='User\'s age')):
    try:
        if not age:
            return users_list

        return list(filter(lambda user: user.age == age,users_list))
    except:
        return {'error': 'No se ha encontrado el usuario'}


#POST
@app.post('/users')
async def insertUser(user: User):
    print(user.id)
    type_user = type(search_user(user.id,users_list))
    if type_user == User:
        return {'error': 'Usuario ya existe'}
    
    users_list.append(user)
    return users_list


# utils 

def search_user(id: int,users_list: list[User]) -> User:
    users = list(filter(lambda user: user.id == id,users_list))
    try: 
        return users[0]
    except:
        return {'error': 'No se ha encontrado el usuario'}