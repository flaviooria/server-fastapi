from fastapi import FastAPI
from fastapi.routing import APIRoute

from routers import users,products

app = FastAPI()

# Add routes
app.include_router(users.router)
app.include_router(products.router)

@app.get('/',status_code=200)
async def root():
    routes = []
    for route in app.routes:    
        if isinstance(route,APIRoute):
            routes.append({'path': route.path_format, 'method': route.methods})

    return routes