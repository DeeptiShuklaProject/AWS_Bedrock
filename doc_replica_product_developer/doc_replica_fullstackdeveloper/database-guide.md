# Connected Databases & Integration Guide

Welcome to the Connected Databases & Integration guide. A full-stack application relies on reliable, secure, and performant data storage. Here, we will cover database paradigms (SQL vs NoSQL), database connection pooling, and configuration models using Python ORMs.

---

## 1. Database Paradigms: SQL vs NoSQL

| Paradigm | Relational (SQL) | Document-Oriented (NoSQL) |
| :--- | :--- | :--- |
| **Data Schema** | Structured, rigid table schemas with predefined column types. | Flexible schema storing JSON-like documents. |
| **Relationships** | Joins, primary keys, and foreign keys enforce relational integrity. | Embedded sub-documents or references. |
| **Scaling** | Vertical scaling (bigger servers). Horizontal scaling requires partitioning/sharding. | Horizontal scaling (sharding across clusters) by default. |
| **Examples** | PostgreSQL, MySQL, SQLite | MongoDB, AWS DynamoDB |

---

## 2. Connection Pooling

Establishing a new database connection for every API request introduces high network latency and CPU overhead. A **Connection Pool** pre-establishes a set of active connections that are reused across different client threads.

```mermaid
graph TD
    subgraph API Application
        Client1[Worker Thread 1] -->|Request Connection| Pool[Connection Pool Manager]
        Client2[Worker Thread 2] -->|Request Connection| Pool
        Client3[Worker Thread 3] -->|Request Connection| Pool
    end
    
    subgraph Database Cluster
        Pool <-->|Persistent Socket 1| DBConn1[DB Engine Connection 1]
        Pool <-->|Persistent Socket 2| DBConn2[DB Engine Connection 2]
        Pool <-->|Persistent Socket 3| DBConn3[DB Engine Connection 3]
    end
```

### SQLAlchemy Pool Parameters:
* `pool_size`: The maximum number of persistent connections to keep open.
* `max_overflow`: The maximum number of additional temporary connections allowed during spikes.
* `pool_timeout`: Number of seconds to wait before throwing an error if all connections are busy.

---

## 3. SQLAlchemy Relational Model Setup

Here is a complete setup for PostgreSQL using SQLAlchemy, defining a One-to-Many relationship between `Groups` and `Items`.

### Code Implementation: Relational Mapping

```python
# database.py
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/my_store"

# Engine setup with Connection Pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # Keep 10 persistent connections
    max_overflow=5,        # Spill over by 5 connections max
    pool_recycle=1800,     # Recycle connections older than 30 mins
    pool_pre_ping=True     # Check connection validity before using
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# One-to-Many Relationship Definitions
class DBGroup(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Establish relationship to Item: One Group can have many items
    items = relationship("DBItem", back_populates="group", cascade="all, delete-orphan")


class DBItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)

    # Back-reference group
    group = relationship("DBGroup", back_populates="items")
```

---

## 4. Django DB Schema Management & Migrations

Django handles schema configurations internally. When models change, Django compares them against your previous state and generates Python migration scripts automatically.

### Lifecycle of a Schema Change:
1. **Define Models**: Update your model schema classes in your app's `models.py`.
2. **Generate Migration**: Run the make migrations script:
   ```bash
   python manage.py makemigrations
   ```
   *This analyzes changes and generates a migration file like `0002_add_item_group.py`.*
3. **Execute Migration**: Run the migrate script to apply changes to the live database:
   ```bash
   python manage.py migrate
   ```
   *This executes SQL commands matching the target database driver (e.g. PostgreSQL, MySQL).*
