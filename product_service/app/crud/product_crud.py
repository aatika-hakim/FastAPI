from app.models.product_model import Product
from sqlmodel import Session, select  # type: ignore
from fastapi import HTTPException  # type: ignore
from app.models.product_model import ProductUpdate


def add_new_product(product_data: Product, session: Session):
    """Add a new product to the database."""
    session.add(product_data)
    session.commit()
    session.refresh(product_data)
    print(f"Product '{product_data.name}' added.")
    return product_data


def fetch_all_products(session: Session):
    """Get all products."""
    all_products = session.exec(select(Product)).all()
    print(f"Retrieved {len(all_products)} products.")
    return all_products


def fetch_product_by_id(product_id: int, session: Session):
    """Get a product by its ID."""
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        print(f"Product with ID {product_id} not found.")
        raise HTTPException(status_code=404, detail="Product not found")
    print(f"Retrieved product '{product.name}' with ID {product_id}.")
    return product


def remove_product_by_id(product_id: int, session: Session):
    """Delete a product by its ID."""
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        print(f"Product with ID {product_id} not found for deletion.")
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    print(f"Product with ID {product_id} deleted.")
    return {"message": "Product deleted successfully"}


def modify_product_by_id(product_id: int, to_update_product_data: ProductUpdate, session: Session):
    """Update a product's details by ID."""
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        print(f"Product with ID {product_id} not found for update.")
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = to_update_product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    print(f"Product with ID {product_id} updated.")
    return product


def validate_product_by_id(product_id: int, session: Session) -> Product | None:
    """Check if a product exists by ID."""
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product:
        print(f"Product with ID {product_id} is valid.")
    else:
        print(f"Product with ID {product_id} is invalid.")
    return product
