from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.requests import Request
from fastapi.responses import JSONResponse,PlainTextResponse


app = FastAPI()

@app.get('/',response_class=PlainTextResponse)
def hello():
    return PlainTextResponse(content='Hola Mundo Fast Api')


@app.post('/items/')
def items(item_id: int):
    return {'item_id': item_id}

@app.post('/hook',response_class=JSONResponse)
def hook():
    return JSONResponse(content=[{'id': 1}],status_code=202)

@app.post('/payload',response_class=JSONResponse)
async def payload(request: Request):
    data: dict | list = await request.json()
    print(data)
    return JSONResponse(content={'data': 'payload succesfully'},status_code=201)