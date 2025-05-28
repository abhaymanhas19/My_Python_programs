from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize FastAPI app
app = FastAPI()

# Set up SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///items.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Item model for SQLAlchemy
class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic model for request/response
class Item(BaseModel):
    id: int
    name: str
    description: str = None
    price: float

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE: Add a new item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    db = next(get_db())
    db_item = ItemDB(id=item.id, name=item.name, description=item.description, price=item.price)
    existing_item = db.query(ItemDB).filter(ItemDB.id == item.id).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return item

# READ: Get all items
@app.get("/items/", response_model=List[Item])
async def read_items():
    db = next(get_db())
    items = db.query(ItemDB).all()
    return items

# READ: Get a specific item by ID
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    db = next(get_db())
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# UPDATE: Update an existing item by ID
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    db = next(get_db())
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if updated_item.id != item_id:
        raise HTTPException(status_code=400, detail="Cannot change item ID")
    db_item.name = updated_item.name
    db_item.description = updated_item.description
    db_item.price = updated_item.price
    db.commit()
    db.refresh(db_item)
    return updated_item

# DELETE: Delete an item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    db = next(get_db())
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": f"Item {item_id} deleted"}