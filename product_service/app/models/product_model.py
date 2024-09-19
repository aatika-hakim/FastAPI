from sqlmodel import SQLModel, Field # type: ignore

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    quantity: int | None = None  # Inventory manages it


class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None
