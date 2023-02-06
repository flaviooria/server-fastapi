from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from entities import UserDBEntity, UserAuthEntity
from exceptions import users_except

# Vamos a utilizar el método de autenticación de password bearer, que es la que permite
# usar tanto usuario y contraseña, password request form, que sera la forma en que los datos son enviados desde el cliente y como la procesa el backend.

router = APIRouter(prefix='/auth')

# Creamos una instancia de oauth2  => es un estandar que indica comos se tiene que hacer las autenticaciones en el backend.
# tokenUrl sera la ruta donde se ingresara con las credenciales.
oauth2 = OAuth2PasswordBearer(tokenUrl='login')

users_db = {
    "flavio_dev": {'username': 'flavio_dev', 'email': 'flavio@dev', 'password': '12345abc', 'disabled': True},
    "valki_dev": {'username': 'valki_dev', 'email': 'valki@dev', 'password': '12345def', 'disabled': False}
}


def searchUser(username: str) -> UserDBEntity:
    if username in users_db:
        return UserDBEntity(**users_db[username])

# Función criterio de dependencia, esta función para obtener el token, tendremos quie buscarlo dentro de nuestro sistema de autentificación
# Por lo cual dependemos de oauth2


async def currentUserDepends(token: str = Depends(oauth2)):
    user = searchUser(token)

    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=users_except.MSG_ERROR_USER_INACTIVE)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=users_except.MSG_ERROR_USER_NOT_AUTHORIZED, 
            headers={'WWW-Authenticate': 'Bearer'})
    
    return UserAuthEntity(**dict(user)) 
    


@router.post('/login')
# El dependes indicara que el form no depende de ninguna funcionalidad para poder utilizarlo
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # verificamos que exista en la base de datos
    user_db = users_db.get(form.username)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=users_except.MSG_ERROR_USER_NOT_CORRECT)

    user = searchUser(form.username)

    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=users_except.MSG_ERROR_USER_PASSWORD_INCORRECT)

    return {'access_token': user.username, 'token_type': 'bearer'}


@router.get('/users/me')
# Le vamos a dar un criterio de dependencia
async def getUser(user: UserAuthEntity = Depends(currentUserDepends)):
    return user
