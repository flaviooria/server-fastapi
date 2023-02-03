from fastapi import FastAPI, Path, Query
from fastapi.routing import APIRoute

from operator import attrgetter

from entities import UserEntity
from utils import search_user

# Instantiate FastApi
app = FastAPI()

# User's list
users_list = [
    UserEntity(id=1,name='Flavio', surname='Oria', url='www.google.com', age=23),
    UserEntity(id=2,name='Cesar', surname='Levano', url='www.google.com', age=26),
    UserEntity(id=3,name='Gabi', surname='Oria', url='www.google.com', age=23)
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
async def insertUser(user: UserEntity) -> list[UserEntity]:
    name, surname, url, age = attrgetter('name','surname','url','age')(user)
    if not name and surname and url and age:
        return {'error': 'Campos invalidos, asegurate de completar todos'}

    # Get the last user id
    id_generated = users_list[-1].id + 1
    user.id = id_generated

    users_list.append(user)
    return users_list

# PUT 
@app.put('/users')
async def user(id: int = Query(default=...,alias='id',title='User\'s id'), *, user: UserEntity):
    founded = -1
    for index, saver_user in enumerate(users_list):
        if saver_user.id != id:
            continue
        
        user.id = id
        users_list[index] = user
        founded = index
        break

    if founded == -1:
        return {'error': 'No se ha acutalizado el usuario'}
    
    return [users_list[founded]]
    
# DELETE
@app.delete('/users')
async def user(id: int = Query(default=...,alias='id',title='User\'s id')):
    foundedUser = search_user(id,users_list)
    
    if not type(foundedUser) == UserEntity:
        return {'error': 'Usuario no eliminado'}
    
    users_list.remove(foundedUser)

    return users_list