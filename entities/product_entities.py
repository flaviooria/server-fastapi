from pydantic import BaseModel

class Product(BaseModel):
    id: str | None
    name: str
    category: str