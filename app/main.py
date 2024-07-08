# Day 1
from enum import Enum
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

@app.get("/item")
async def item():
    return {'message': 'setup route'}

@app.get("/item/{item_id}")
async def item(item_id: int):
    return {'item': item_id}

# Day-2
class Cars(str, Enum):
    audi = "Audi"
    bmw = "BMW"
    mercedes = "Mercedes"

@app.get('/cars/{car_names}')
async def get_car(car_names: Cars):
    if car_names.value == car_names.audi:
        return {'car': car_names, 'message': "New Brands"}
    
    
    if car_names.value == 'BMW':
        return {'car': car_names, 'message': "My new car"}
    
    
    if car_names.value == 'Mercedes':
        return {'car': car_names, 'message': "Happy driving"}
