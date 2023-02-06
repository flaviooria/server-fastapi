from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from entities import UserDBEntity, UserAuthEntity
from exceptions import users_except
from utils import Token, readJson, writeJson

# Vamos a utilizar el método de autenticación de password bearer, que es la que permite
# usar tanto usuario y contraseña, password request form, que sera la forma en que los datos son enviados desde el cliente y como la procesa el backend.

router = APIRouter(prefix='/auth')

# Creamos una instancia de oauth2  => es un estandar que indica comos se tiene que hacer las autenticaciones en el backend.
# tokenUrl sera la ruta donde se ingresara con las credenciales.
oauth2 = OAuth2PasswordBearer(tokenUrl='signIn')


users_db: list[UserDBEntity] = readJson('auth_users.json')


def loadUsersDB(data: list[UserDBEntity]) -> list[UserDBEntity]:
    data = readJson('auth_users.json')

def searchUser(username: str) -> UserDBEntity:
    if username in users_db:
        return UserDBEntity(**users_db[username])
    

def searchUserByToken(token: str) -> UserDBEntity | None:
    for username in users_db.keys():
        user_db = UserDBEntity(**users_db[username])
        if token == user_db.token:
            return user_db
    return None
        

# Función criterio de dependencia, esta función para obtener el token, tendremos quie buscarlo dentro de nuestro sistema de autentificación
# Por lo cual dependemos de oauth2
async def currentUserDepends(token: str = Depends(oauth2)):
    user = searchUserByToken(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=users_except.MSG_ERROR_USER_NOT_AUTHORIZED, 
            headers={'WWW-Authenticate': 'Bearer'})

    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=users_except.MSG_ERROR_USER_INACTIVE)

    return UserAuthEntity(**dict(user)) 
    


@router.post('/signIn')
# El dependes indicara que el form no depende de ninguna funcionalidad para poder utilizarlo
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # verificamos que el usuario exista en la base de datos
    founder_user_in_db = users_db.get(form.username)

    if not founder_user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=users_except.MSG_ERROR_USER_NOT_CORRECT)

    founded_user = searchUser(form.username)

    if not form.password == founded_user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=users_except.MSG_ERROR_USER_PASSWORD_INCORRECT)

    # Update the user with token
    founded_user.token = Token(founded_user.username, founded_user.password)
    users_db[founded_user.username] = dict(founded_user)
    # Generate persistenece
    writeJson(path='auth_users.json',mode='w',data=users_db)
    # Load the new values in users db
    loadUsersDB(users_db)

    return {'access_token': founded_user.token, 'token_type': 'bearer'}

@router.post('/signUp', status_code=201)
async def register(user: UserDBEntity):

    print(user.username)
    print(user.email)
    print(user.password)

    if not user.username or not user.email or not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=users_except.MSG_ERROR_USER_NOT_CORRECT)
    
    users_db[user.username] = dict(user)
    writeJson(path='auth_users.json',mode='w',data=users_db)

    return { user.username: users_db[user.username] }

@router.get('/users/me')
# Le vamos a dar un criterio de dependencia
async def getUser(user: UserAuthEntity = Depends(currentUserDepends)):
    return user
