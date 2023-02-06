from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from routers import users,products

app = FastAPI()

# Add routes
app.include_router(users.router)
app.include_router(products.router)

# Add static files
# Para añadir archivos estaticos se utiliza el método mount. Tiene 3 párametros
# path: Nombre del path que usara la api,
# app: Que sera en este caso la clase StaticFiles, donde obtendra nuestros archivos estaticos
# name: Es el nombre que recibira por defecto
app.mount('/static',StaticFiles(directory='static',html=True),'static')


@app.get('/',status_code=200)
async def root():
    routes = []
    for route in app.routes:    
        if isinstance(route,APIRoute):
            routes.append({'path': route.path_format, 'method': route.methods})

    return routes