# Day 1
from enum import Enum
from fastapi import FastAPI, status
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
###### FastAPI Authorization ###### 

# in python we declare Constants Capital Words

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

# To decode access token
def decode_access_token(token: str):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token

# decode_access_token route 
@app.get("/decode_token")
def decode_token(token: str):
    decoded_token = decode_access_token(token)
    return {"decoded token": decoded_token}



###### Response Status Codes  ######
@app.post("/msg/", status_code=status.HTTP_201_CREATED)
async def msg_status(msg: str):
    return {"message": msg}

@app.delete("/msg/{m}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_status(m: str):
    return m

@app.get("/status/{s}", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def get_status(s: str):
    return s

@app.get("/status_check/{status}", status_code=status.HTTP_401_UNAUTHORIZED)
async def get_status(status: str):
    return status



