from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)



Base.metadata.create_all(bind=engine)

app = FastAPI() 


class ItemCreate(BaseModel):

    name: str
    description: str

@app.post("/items/", response_model=ItemCreate)
def create_item(item: ItemCreate):

    db = SessionLocal()
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
    
@app.get("/items/", response_model=List[ItemCreate])
def read_items(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    items = db.query(Item).offset(skip).limit(limit).all()
    return items











