# Day 1
from enum import Enum
from fastapi import FastAPI
from jose import jwt, JWTError
from datetime import datetime, timedelta

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

#Day 2
# FastAPI Authorization

# in python we declare Constants Capital

ALGORITHM = "HS256"
SECRET_KEY = "secretkey1234567890"

# to generate access token
def create_access_token(subject: str, expires_delta: timedelta) -> str:
    expiration = datetime.utcnow() + expires_delta
    to_encode = {"sub": subject, "exp": expiration}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/get_token")
def get_token(name: str):
    access_token_expiry = timedelta(minutes=10)
    access_token = create_access_token(subject=name, expires_delta=access_token_expiry)
    return {"access token": access_token}
