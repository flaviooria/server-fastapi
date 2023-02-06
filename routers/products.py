from fastapi import APIRouter

from utils import readJson
from entities import ProductEntity

# El prefijo sirve para no tener que añadir el /products en cada route que añadieramos
# y el tags, servira para darle una categoría y en la documentación se muestre de esa manera
router = APIRouter(prefix='/products',tags=['products'])
products: list[ProductEntity] = readJson('products.json')

@router.get('/',status_code=200,response_model=list[ProductEntity])
def getProducts():
    return products