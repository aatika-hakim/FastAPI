from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from sqlmodel import Session, SQLModel  # type: ignore
from fastapi import FastAPI, Depends, HTTPException  # type: ignore
from aiokafka import AIOKafkaProducer  # type: ignore
import asyncio
import json
from app import settings
from app.db_engine import engine
from app.deps import get_kafka_producer, get_session
from app.models.product_model import Product, ProductUpdate
from app.crud.product_crud import fetch_all_products, remove_product_by_id, modify_product_by_id, fetch_product_by_id
from app.consumer.product_consumer import consume_product_messages


def initialize_database() -> None:
    """Set up the database and create tables if they don't exist."""
    SQLModel.metadata.create_all(engine)
    print("Database initialized.")


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Starting application...")

    initialize_database()
    
    # Start consuming messages from Kafka
    task = asyncio.create_task(consume_product_messages(settings.KAFKA_PRODUCT_TOPIC, 'broker:19092'))
    
    yield

    print("Shutting down application...")


app = FastAPI(
    lifespan=app_lifespan,
    title="Product Service API",
    version="1.0.0",
)


@app.get("/")
def welcome():
    return {"message": "Welcome to the Product Service!"}


@app.post("/products/", response_model=Product)
async def create_product(
    product: Product,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
):
    """Create a new product and send a message to Kafka."""
    product_dict = {field: getattr(product, field) for field in product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("Sending product data to Kafka...")
    
    await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, product_json)
    
    return product


@app.get("/products/", response_model=list[Product])
def list_products(session: Annotated[Session, Depends(get_session)]):
    """Get all products from the database."""
    return fetch_all_products(session)


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """Get a specific product by ID."""
    try:
        return fetch_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e


@app.delete("/products/{product_id}")
def delete_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """Delete a product by ID."""
    try:
        return remove_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate, session: Annotated[Session, Depends(get_session)]):
    """Update product details."""
    try:
        return modify_product_by_id(product_id=product_id, to_update_product_data=product, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
