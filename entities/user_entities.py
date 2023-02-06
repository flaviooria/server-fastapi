from pydantic import BaseModel

# Creamos nuestras entidades, empezamos por user
class UserBase(BaseModel):
    id: int | None
    name: str
    surname: str
    url: str
    age: int

class UserAuth(BaseModel):
    username: str
    email: str
    disabled: bool | None = False

class UserDB(UserAuth):
    password: str
    token: str | None