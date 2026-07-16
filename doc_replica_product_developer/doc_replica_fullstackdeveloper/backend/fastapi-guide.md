# FastAPI Architecture & Setup

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.

---

## 1. FastAPI Architecture Diagram

FastAPI runs on an ASGI server (like **Uvicorn**) and handles concurrency asynchronously using Python's event loop, making it extremely fast.

```mermaid
graph LR
    Client[Client Requests] -->|Async Socket| Uvicorn[Uvicorn ASGI Server]
    Uvicorn -->|Event Loop| FastAPI[FastAPI Router]
    FastAPI -->|Dependency Inject| DBConn[SQLAlchemy Session]
    DBConn -->|Connection Pool| Postgres[(PostgreSQL)]
```

---

## 2. API Code Implementation

Below is a complete FastAPI setup. It configures the database connection pool using SQLAlchemy, creates an `items` table model, handles request validation using Pydantic, and exposes API endpoints.

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# 1. Database Configuration
DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model (Database Table Schema)
class DBItem(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

# Create tables in the DB
Base.metadata.create_all(bind=engine)

# 2. Pydantic Schemas (Request/Response Validation)
class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemResponse(ItemBase):
    id: int
    class Config:
        orm_mode = True

# 3. FastAPI App Initialization
app = FastAPI(title="FastAPI Generic Items API")

# Dependency Injection for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. API Endpoints
@app.get("/api/items", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    items = db.query(DBItem).all()
    return items

@app.post("/api/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemBase, db: Session = Depends(get_db)):
    db_item = DBItem(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

---

## 3. Key Concepts to Master
1. **Asynchronous Handlers**: Use `async def` for IO-bound endpoints. FastAPI runs synchronous endpoints (`def`) in an external thread pool to prevent blocking the event loop.
2. **Dependency Injection**: The `Depends(get_db)` syntax simplifies testing and ensures connections are reliably returned to the pool after each request.
3. **Automatic Documentation**: FastAPI automatically generates interactive documentation at `/docs` (Swagger UI) and `/redoc` (ReDoc) based on Pydantic schemas.
