from fastapi import APIRouter, Path, Query, HTTPException, status


from operator import attrgetter

from entities import UserEntity
from utils import search_user
from exceptions import users_except

# Instantiate FastApi
router = APIRouter(prefix='/users',tags=['users'])

# User's list
users_list = [
    UserEntity(id=1,name='Flavio', surname='Oria', url='www.google.com', age=23),
    UserEntity(id=2,name='Cesar', surname='Levano', url='www.google.com', age=26),
    UserEntity(id=3,name='Gabi', surname='Oria', url='www.google.com', age=23)
]


@router.get('/',status_code=200,response_model=list[UserEntity])
async def users():
    return users_list


# Endpoint con path
@router.get('/{id}',status_code=200,response_model=list[UserEntity])
async def getUsersById(id: int = Path(default=...,alias='id',title='User id',example=1)):
    founded_user = list(filter(lambda user: user.id == id,users_list))

    if len(founded_user) == 0:
        # Usamos el http exception para generar una excepción, esta recibe 3 párametros
        # el código de estado, detail = que es el mensaje, si no recibe nada, devuelve un mesanje respecto al código de estdo que se le haya pasado.

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=users_except.MSG_ERROR_USER_NOT_FOUND)
    
    return founded_user



# Endpoint con query
@router.get('/age',status_code=200,response_model=list[UserEntity])
async def getUsersByAge(age: int | None = Query(default=None,alias='age',title='User\'s age')):
    if not age:
        return users_list

    users = list(filter(lambda user: user.age == age,users_list))

    if len(users) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=users_except.MSG_ERROR_USER_NOT_FOUND)
    
    return users

#POST
@router.post('/',status_code=201,response_model=list[UserEntity])
async def insertUser(user: UserEntity) -> list[UserEntity]:
    name, surname, url, age = attrgetter('name','surname','url','age')(user)
    if not name and surname and url and age:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Fields not indicated or empty in the body')

    # Get the last user id
    id_generated = users_list[-1].id + 1
    user.id = id_generated

    users_list.append(user)
    return users_list

# PUT 
@router.put('/',status_code=200,response_model=list[UserEntity])
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
@router.delete('/')
async def user(id: int = Query(default=...,alias='id',title='User\'s id')):
    foundedUser = search_user(id,users_list)
    
    if not type(foundedUser) == UserEntity:
        return {'error': 'Usuario no eliminado'}
    
    users_list.remove(foundedUser)

    return users_list