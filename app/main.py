# Day 1
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def get():
    return {'message': 'Hello Fastapi'}

@app.post('/')
async def post():
    return {'message': 'post route'}


@app.put('/')
async def put():
    return {'message': 'put route'}

@app.patch('/')
async def put():
    return {'message': 'patch route'}  