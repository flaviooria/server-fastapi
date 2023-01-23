from enum import Enum
from fastapi import FastAPI, Query, Path
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel
from utils import read_json

# FastAPI es una clase de Python que provee toda la funcionalidad para tu API.

# Incializamos el server instanciando fastA api
app = FastAPI(title='Server webhook', version='0.1.0')
users = []

# routings

# Routings path, path se refiere a la última parte de una url comenzando por '/'

# Usammos el decorador @app, que sirve para crear las rutas

# Un "decorador" toma la función que tiene debajo y hace algo con ella.


@app.get('/')
def hello_world():
    return PlainTextResponse(content='Hello World')


# Routing path => Aquí le decimos a nuestra ruta que va a recibir un parametro id es requerido, este path no puede ser opcional
@app.get('/users/{userId}') # => http://localhost:3000/users/1
def allUsers(userId: int):
    users = read_json()
    if not userId:
        return JSONResponse(content={'data': 'user not found'},status_code=404)
    
    founded_user = users[userId - 1]

    return JSONResponse(content=founded_user, status_code=200)

# Routing path query => El query es el conjunto de pares de key-value que van después del ? en la URL, separados por caracteres &.
@app.get('/users/') # => http://localhost:3000/users/?limit=5
def allUsersWithLimit(limit:int | None = None):
    users = read_json()
    if limit:
        users = users[:limit]
    
    return JSONResponse(content=users, status_code=200)

# Enum de géneros, aquí nuestra clase hereda de string para que la api reconozca que los valores que debe recibir 
# son de ese tipo y en esas dos opciones.
class Gender(str,Enum):
    female = 'Female'
    male = 'Male'

# Creando un modelo o interfaz para nuestros métodos post, esto se le denomina un requers body
class UserModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    gender: Gender | None = None
    

@app.post('/users/')
def createUser(user: UserModel):
    id = user.id
    users.append(user)
    return JSONResponse(content={
        'msg': 'User created succesfully',
        'data': id
    }, status_code=201)


# En este paso vamos a integrar String and Numeric validations, para eso importamos Query
# Si queremos que nuestro parametro sea requerido,debemos no añadir ningun valor al default,añadir "..." o importar Required y asignarselo al default 
@app.get('/users/gender/')
async def getUsersByGender(gender: Gender = Query(default=...,description='Gender of user',title='gender',example='Male',alias='gender-user')):
    users = read_json()
    founded_users = list(filter(lambda user: user['gender'].lower() == gender.lower(),users))
    return JSONResponse(content=founded_users,status_code=200)

# Ahora con Los Numeric validations, es lo mismo que Query pero la clase es Path
# Tenemos que tener en cuenta que tanto como en las Query y Path, si se usan los alias, deben de coincidir con el mismo nombre del parametro de la ruta
@app.get('/users/id/{id_param}')
def getUserById(id: int = Path(default=...,alias='id_param',title='Id of user')):
    return {'id': id}