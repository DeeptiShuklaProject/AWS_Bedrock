# Connected Databases & Integration Guide

Welcome to the Connected Databases & Integration guide. A full-stack application relies on reliable, secure, and performant data storage. Here, we will cover database paradigms (SQL vs NoSQL), database connection pooling, and configuration models using Python ORMs.

---

<ProgressTracker currentSection=1 totalSections=4 />

## 1. Database Paradigms: SQL vs NoSQL

| Paradigm | Relational (SQL) | Document-Oriented (NoSQL) |
| :--- | :--- | :--- |
| **Data Schema** | Structured, rigid table schemas with predefined column types. | Flexible schema storing JSON-like documents. |
| **Relationships** | Joins, primary keys, and foreign keys enforce relational integrity. | Embedded sub-documents or references. |
| **Scaling** | Vertical scaling (bigger servers). Horizontal scaling requires partitioning/sharding. | Horizontal scaling (sharding across clusters) by default. |
| **Examples** | PostgreSQL, MySQL, SQLite | MongoDB, AWS DynamoDB |

---

<ProgressTracker currentSection=2 totalSections=4 />

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

<ProgressTracker currentSection=3 totalSections=4 />

## 3. SQLAlchemy Relational Model Setup

Here is a complete setup for PostgreSQL using SQLAlchemy, defining a One-to-Many relationship between `Groups` and `Items`.

### Code Implementation: Relational Mapping

<Tabs>
  <Tab label="Syntax & Example">

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

  </Tab>
  <Tab label="Interactive Playground">
    <InteractiveExample 
      language="python"
      initialCode="# database.py\nfrom sqlalchemy import create_engine, ForeignKey, Column, Integer, String\nfrom sqlalchemy.orm import declarative_base, relationship, sessionmaker\n\nDATABASE_URL = \"postgresql://user:password@localhost:5432/my_store\"\n\n# Engine setup with Connection Pooling\nengine = create_engine(\n    DATABASE_URL,\n    pool_size=10,          # Keep 10 persistent connections\n    max_overflow=5,        # Spill over by 5 connections max\n    pool_recycle=1800,     # Recycle connections older than 30 mins\n    pool_pre_ping=True     # Check connection validity before using\n)\n\nSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\nBase = declarative_base()\n\n# One-to-Many Relationship Definitions\nclass DBGroup(Base):\n    __tablename__ = \"groups\"\n\n    id = Column(Integer, primary_key=True, index=True)\n    name = Column(String, unique=True, nullable=False)\n\n    # Establish relationship to Item: One Group can have many items\n    items = relationship(\"DBItem\", back_populates=\"group\", cascade=\"all, delete-orphan\")\n\n\nclass DBItem(Base):\n    __tablename__ = \"items\"\n\n    id = Column(Integer, primary_key=True, index=True)\n    name = Column(String, nullable=False)\n    description = Column(String, nullable=True)\n    group_id = Column(Integer, ForeignKey(\"groups.id\", ondelete=\"CASCADE\"), nullable=False)\n\n    # Back-reference group\n    group = relationship(\"DBGroup\", back_populates=\"items\")" 
      instruction="Execute and edit this PYTHON example."
    />
  </Tab>
</Tabs>

---

<ProgressTracker currentSection=4 totalSections=4 />

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

---

### Knowledge Verification Check

<Quiz 
  question="When must the `HAVING` clause be used in SQL instead of the `WHERE` clause?" 
  options=["When filtering records containing string patterns.", "When filtering groups of query results based on aggregate functions (e.g. SUM, AVG).", "When sorting results in descending order.", "When performing SQL join operations."] 
  answerIndex=1 
  explanation="The `WHERE` clause filters individual rows before grouping. The `HAVING` clause filters grouped results after aggregation has been applied." 
/>

<Quiz 
  question="Which type of SQL Join returns all rows from the left table, and matching rows from the right table, filling with NULL if no match is found?" 
  options=["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"] 
  answerIndex=1 
  explanation="A `LEFT JOIN` (or LEFT OUTER JOIN) returns all records from the left table and any corresponding matching records from the right table." 
/>

<Quiz 
  question="How does a B-Tree index speed up database SELECT queries, and what is its overhead?" 
  options=["It compresses table files to half size, slowing down writes.", "It provides logarithmic time search (O(log N)) for matching rows, but adds write overhead to update the index on INSERT, UPDATE, and DELETE operations.", "It turns relational tables into NoSQL collections.", "It runs queries in parallel on the GPU."] 
  answerIndex=1 
  explanation="B-Tree indexes speed up lookups by organizing data in a balanced search tree. However, every modification to indexed columns requires updating the tree structure, adding write overhead." 
/>

<Quiz 
  question="What does the ACID acronym stand for in database transaction management?" 
  options=["Aggregation, Consolidation, Indexing, Distribution.", "Atomicity, Consistency, Isolation, Durability.", "Availability, Concurrency, Isolation, Deletion.", "Access, Control, Integrity, Definition."] 
  answerIndex=1 
  explanation="ACID properties (Atomicity, Consistency, Isolation, Durability) ensure database transactions are processed reliably, maintaining data integrity." 
/>

<Quiz 
  question="Which ANSI SQL transaction isolation level prevents dirty reads and non-repeatable reads, but can allow phantom reads?" 
  options=["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"] 
  answerIndex=2 
  explanation="Repeatable Read prevents dirty reads and non-repeatable reads by holding locks on read rows, but does not lock index ranges, potentially allowing phantom rows to be inserted." 
/>

<Quiz 
  question="What is the primary goal of Third Normal Form (3NF) in database design?" 
  options=["To optimize search queries using caching.", "To eliminate transitive dependencies, ensuring all non-key columns depend only on the primary key, thereby reducing data redundancy.", "To split tables into document-based JSON rows.", "To enforce foreign key constraints across different databases."] 
  answerIndex=1 
  explanation="A database is in 3NF if it is in 2NF and has no transitive functional dependencies, meaning every non-prime attribute depends directly on the primary key." 
/>

<Quiz 
  question="What is a key difference between a Primary Key and a Unique constraint?" 
  options=["A table can have multiple Primary Keys, but only one Unique constraint.", "Primary Keys can contain NULL values, Unique constraints cannot.", "A table can have only one Primary Key, but multiple Unique constraints, and Unique constraints can allow NULL values.", "They are identical and have no functional differences."] 
  answerIndex=2 
  explanation="A table is limited to one primary key, which uniquely identifies rows and forbids NULL values. Unique constraints allow duplicate prevention across other columns, allowing NULLs." 
/>

<Quiz 
  question="What does a Foreign Key constraint enforce in a relational schema?" 
  options=["It encrypts columns to secure foreign user access.", "Referential integrity, guaranteeing that values in a column match existing values in the primary key of a referenced parent table.", "It automatically synchronizes tables with external APIs.", "It indexes columns for faster search."] 
  answerIndex=1 
  explanation="Foreign keys maintain referential integrity, preventing invalid data entries in child tables by ensuring they point to a valid parent record." 
/>

<Quiz 
  question="Which SQL aggregate function computes the rank of rows within query partitions without skipping rank numbers?" 
  options=["RANK()", "DENSE_RANK()", "ROW_NUMBER()", "PERCENT_RANK()"] 
  answerIndex=1 
  explanation="Unlike `RANK()`, which leaves gaps when ties occur (e.g. 1, 2, 2, 4), `DENSE_RANK()` assigns consecutive integers without gaps (e.g. 1, 2, 2, 3)." 
/>

<Quiz 
  question="What is the difference between a View and a Materialized View?" 
  options=["Views are stored on disk, Materialized Views exist only in memory.", "A View is a virtual table that executes its query dynamically, while a Materialized View precomputes and stores its result query data on disk.", "Materialized Views are used only in NoSQL databases.", "There is no difference; they are identical."] 
  answerIndex=1 
  explanation="Views run their queries on-demand, consuming computation resources each time. Materialized views cache query results physically on disk and must be refreshed when base data changes." 
/>

<Quiz 
  question="Why are Columnar databases preferred over Row-oriented databases for OLAP (Analytical) workloads?" 
  options=["They run transactions faster.", "They allow reading only the specific columns needed for aggregations, drastically reducing disk I/O and improving compression rates.", "They use JSON format internally.", "They require less memory to load."] 
  answerIndex=1 
  explanation="Row-oriented databases are optimized for OLTP (reading whole rows). Columnar databases group column values together, enabling high compression and fast aggregation over specific fields." 
/>

<Quiz 
  question="What is a Common Table Expression (CTE) in SQL?" 
  options=["A permanent database table used for caching.", "A temporary named result set defined within the scope of a single SELECT, INSERT, UPDATE, or DELETE query using the `WITH` keyword.", "A table index optimization strategy.", "A database schema validation rule."] 
  answerIndex=1 
  explanation="CTEs are defined using the `WITH` keyword. They act as temporary queries that exist during the execution of a main statement, improving query readability and enabling recursion." 
/>
