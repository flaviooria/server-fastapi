from pydantic import BaseModel

# Creamos nuestras entidades, empezamos por user
class User(BaseModel):
    id: int | None
    name: str
    surname: str
    url: str
    age: int 