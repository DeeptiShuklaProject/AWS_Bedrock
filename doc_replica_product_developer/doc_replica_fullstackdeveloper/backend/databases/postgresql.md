# PostgreSQL Master Engineering Guide

PostgreSQL is a powerful, open-source object-relational database system (ORDBMS) with over 35 years of active development. It is known for its reliability, feature robustness, and performance under heavy workloads.

<ProgressTracker currentSection=1 totalSections=26 />

## 1. Introduction

### 1.1 What is PostgreSQL?
PostgreSQL (pronounced *post-gres-Q-L*) is an enterprise-class, open-source object-relational database management system (ORDBMS). It extends the SQL language by adding support for user-defined types, operators, index methods, and procedural languages.

### 1.2 History & Origin
Developed originally in 1986 under the POSTGRES project at the University of California, Berkeley, led by Professor Michael Stonebraker. In 1996, the project was renamed to PostgreSQL to emphasize its support for SQL.

### 1.3 Why it was Created & Problems it Solves
- **Extensibility**: Allows developers to add custom functions, data types, and index types (such as GIN and GiST).
- **Concurrency**: Introduced Multi-Version Concurrency Control (MVCC) to eliminate read-write locking conflicts.
- **SQL Compliance**: Highly compliant with SQL standards (ANSI SQL:2023).
- **Reliability**: Guarantees ACID compliance under any system failures.

### 1.4 Licensing, Release, and Industry Adoption
- **License**: PostgreSQL License (similar to BSD/MIT), allowing commercial use, modification, and distribution without fees.
- **Latest Stable Version**: PostgreSQL 16 (with PostgreSQL 17 in release candidate stage).
- **Major Users**: Netflix, Apple, Uber, Spotify, Instagram, Reddit, and thousands of fintech, healthtech, and logistics giants.

---
<ProgressTracker currentSection=2 totalSections=26 />

## 2. Database Fundamentals

### 2.1 DBMS vs RDBMS vs NoSQL
- **DBMS**: General system for storing and managing file-based databases.
- **RDBMS**: Restricts data model to tabular rows and columns linked by relations (keys) and enforces strict constraints.
- **NoSQL**: Schema-less document, key-value, graph, or wide-column store designed for horizontal scaling.

### 2.2 ACID Properties in PostgreSQL
- **Atomicity**: Transactions are all-or-nothing. Managed via the Write-Ahead Log (WAL) and Transaction status logs (`pg_xact`).
- **Consistency**: Enforces schema rules, foreign key constraints, check constraints, and unique indexes on every commit.
- **Isolation**: Separates concurrent transaction execution using MVCC.
- **Durability**: Ensures committed transaction writes are flushed to disk logs before returning success to the client.

### 2.3 CAP Theorem & BASE Model
PostgreSQL is a classic **CP (Consistency & Partition Tolerance)** database system. In distributed setups (like streaming replication), it prioritizes consistency over availability. The **BASE** model (Basically Available, Soft state, Eventual consistency) is rejected in favor of strict ACID compliance.

```mermaid
graph TD
    CAP[CAP Theorem Triad] --> C[Consistency: Strongest focus of Postgres]
    CAP --> A[Availability: Lower priority during partition failures]
    CAP --> P[Partition Tolerance: Maintained via replication failovers]
```

---
<ProgressTracker currentSection=3 totalSections=26 />

## 3. Internal Architecture

PostgreSQL uses a process-based architecture (not thread-based) where each client connection spawns a dedicated backend process.

```mermaid
graph TD
    Client[Client Application] -->|Connects| Postmaster[Postmaster / Parent Process]
    Postmaster -->|Spawns| Backend[Backend Worker Process]
    
    subgraph Shared Memory
        BufferCache[Shared Buffers / Page Cache]
        WALBuffer[WAL Buffer]
        LockMgr[Lock Manager]
    end
    
    Backend --> BufferCache
    Backend --> WALBuffer
    Backend --> LockMgr
    
    subgraph Background Processes
        Writer[Background Writer]
        Checkpointer[Checkpointer Process]
        WALWriter[WAL Writer]
        Autovacuum[Autovacuum Daemon]
    end
    
    BufferCache -.-> Writer
    BufferCache -.-> Checkpointer
    WALBuffer -.-> WALWriter
    
    subgraph Disk Storage
        Heap[Data Heap Files]
        Indexes[Index Files]
        WAL[Write-Ahead Logs]
    end
    
    Checkpointer --> Heap
    Checkpointer --> Indexes
    WALWriter --> WAL
```

### 3.1 Architectural Components
- **Client & Driver**: Sends SQL query text over TCP socket using Frontend/Backend Protocol (v3.0).
- **Query Parser**: Analyzes SQL syntax and converts it into a parse tree.
- **Query Planner & Optimizer**: Analyzes data statistics to generate the most efficient execution plan (utilizing Sequential scan, Index scan, Nested loops, Hash joins).
- **Execution Engine**: Executes the plan, fetching pages into memory or returning filtered rows.
- **Storage Engine**: Manages physical layout of tables and indexes.
- **Shared Buffers (Buffer Cache)**: In-memory cache of database page blocks (typically 8KB).
- **WAL Writer**: Periodically flushes WAL buffer to physical disk logs.
- **Autovacuum**: Automatically reclaims disk space occupied by deleted/dead tuples (MVCC vacuuming).

---
<ProgressTracker currentSection=4 totalSections=26 />

## 4. Installation

### 4.0 Official Resources & Installation Flow
- **Download Link**: [Official PostgreSQL Download Page](https://www.postgresql.org/download/)

```mermaid
flowchart TD
    A[Start Installation] --> B[Download Installer/Package]
    B --> C[Configure Port 5432 & Password]
    C --> D[Initialize Database Cluster initdb]
    D --> E[Start PostgreSQL Service]
```


### 4.1 Linux (Ubuntu/Debian)
```bash
# Add the PostgreSQL official repository
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Install PostgreSQL 16
sudo apt-get update
sudo apt-get -y install postgresql-16
```

### 4.2 Windows
Download the graphical installer from EDB, run the `.exe` setup, set the superuser password, and configure the port (default `5432`).

### 4.3 Docker & Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:16-alpine
    container_name: postgres_master
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: supersecretpassword
      POSTGRES_DB: enterprise_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---
<ProgressTracker currentSection=5 totalSections=26 />

## 5. Database Creation & Management

### 5.1 Basic CLI Commands
```sql
-- Create Database
CREATE DATABASE app_db WITH OWNER admin ENCODING 'UTF8';

-- Rename Database
ALTER DATABASE app_db RENAME TO app_db_production;

-- Drop Database
DROP DATABASE app_db_production;
```

### 5.2 Backup & Restore Tools
- **pg_dump (Logical Backup)**:
  ```bash
  pg_dump -U admin -h localhost -d app_db -F c -b -v -f app_db_backup.dump
  ```
- **pg_restore (Logical Restore)**:
  ```bash
  pg_restore -U admin -h localhost -d app_db_restore -v app_db_backup.dump
  ```
- **Copy Command (CSV Export/Import)**:
  ```sql
  -- Export
  COPY users TO '/tmp/users.csv' WITH (FORMAT CSV, HEADER);
  
  -- Import
  COPY users FROM '/tmp/users.csv' WITH (FORMAT CSV, HEADER);
  ```

---
<ProgressTracker currentSection=6 totalSections=26 />

## 6. Data Types

PostgreSQL supports a massive, rich set of primitive and advanced data types.

| Data Type | Memory size | Typical Use Case | Example Syntax |
| :--- | :--- | :--- | :--- |
| `INT` / `INTEGER` | 4 bytes | Standard counting and ID fields | `id INT` |
| `BIGINT` | 8 bytes | High-volume logging / financial transactions | `amount BIGINT` |
| `NUMERIC(p,s)` | Variable | Exact decimals (money, scientific metrics) | `price NUMERIC(10,2)` |
| `VARCHAR(n)` | Variable | Limited string inputs | `username VARCHAR(50)` |
| `TEXT` | Variable | Unlimited character strings (descriptions) | `body TEXT` |
| `JSONB` | Variable | Binary JSON (supports GIN index, faster reads) | `metadata JSONB` |
| `UUID` | 16 bytes | Globally unique identifier keys | `id UUID DEFAULT gen_random_uuid()` |
| `TIMESTAMPTZ` | 8 bytes | Timestamp including timezone offsets | `created_at TIMESTAMPTZ` |

> [!WARNING]
> Always prefer `JSONB` over plain `JSON`. `JSONB` parses the JSON input and stores it in a decompressed binary format, which supports indexes and fast lookup queries.

---
<ProgressTracker currentSection=7 totalSections=26 />

## 7. Tables & Constraints

Creating tables with appropriate constraint validation ensures schema integrity at the database level.

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    uuid_key UUID DEFAULT gen_random_uuid() UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL CHECK (email LIKE '%@%'),
    salary NUMERIC(10, 2) DEFAULT 0.00 CHECK (salary >= 0),
    department_id INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_employee_composite UNIQUE (first_name, last_name)
);
```

---
<ProgressTracker currentSection=8 totalSections=26 />

## 8. CRUD Operations

PostgreSQL supports basic CRUD, plus advanced features like `ON CONFLICT` (Upsert) and `RETURNING`.

```sql
-- 1. INSERT with RETURNING
INSERT INTO employees (first_name, last_name, email, department_id, salary) 
VALUES ('John', 'Doe', 'john.doe@company.com', 1, 75000.00) 
RETURNING id, uuid_key;

-- 2. UPSERT (INSERT or UPDATE on conflict)
INSERT INTO employees (first_name, last_name, email, department_id, salary)
VALUES ('John', 'Doe', 'john.newemail@company.com', 1, 80000.00)
ON CONFLICT (first_name, last_name) 
DO UPDATE SET email = EXCLUDED.email, salary = EXCLUDED.salary;

-- 3. UPDATE
UPDATE employees SET salary = salary * 1.10 WHERE department_id = 1 RETURNING id, salary;

-- 4. DELETE
DELETE FROM employees WHERE salary < 30000.00 RETURNING id;
```

---
<ProgressTracker currentSection=9 totalSections=26 />

## 9. Advanced SQL Queries

PostgreSQL supports complex ANSI-compliant querying constructs.

```sql
-- Advanced aggregation with HAVING and window analytical operations
SELECT 
    department_id,
    AVG(salary) AS avg_salary,
    COUNT(id) AS total_employees,
    RANK() OVER (ORDER BY AVG(salary) DESC) as dept_rank
FROM employees
WHERE created_at > '2020-01-01'
GROUP BY department_id
HAVING COUNT(id) > 2
LIMIT 5 OFFSET 0;
```

---
<ProgressTracker currentSection=10 totalSections=26 />

## 10. Joins

PostgreSQL uses Nested Loop, Hash Join, and Merge Join algorithms internally depending on the query planner strategy.

```mermaid
graph TD
    Join[Joins in PostgreSQL] --> Inner[Inner Join: Matches in both]
    Join --> Left[Left Join: All left + matches]
    Join --> Full[Full Outer Join: All rows from both]
    Join --> Cross[Cross Join: Cartesian product]
```

```sql
-- FULL OUTER JOIN Example
SELECT e.first_name, d.name AS dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.id;
```

---
<ProgressTracker currentSection=11 totalSections=26 />

## 11. Functions

PostgreSQL features aggregate, window, JSON, math, and date manipulation functions.

```sql
-- JSONB parsing, Date truncation, and Window Functions
SELECT 
    date_trunc('month', created_at) AS join_month,
    metadata->>'role' AS user_role,
    LAG(salary, 1) OVER (PARTITION BY department_id ORDER BY created_at) AS prev_employee_salary
FROM employees;
```

---
<ProgressTracker currentSection=12 totalSections=26 />

## 12. Indexes

PostgreSQL indexes speed up query lookups. B-Tree is the default index structure.

```mermaid
graph TD
    IndexType[Index Types] --> BTree[B-Tree: Default comparison =, <, >]
    IndexType --> GIN[GIN: Generalized Inverted Index - Array/JSONB search]
    IndexType --> Hash[Hash: Direct match =]
    IndexType --> BRIN[BRIN: Block Range Index - Huge sorted datasets]
```

```sql
-- 1. Standard B-Tree Index
CREATE INDEX idx_emp_email ON employees(email);

-- 2. GIN Index for JSONB columns
CREATE INDEX idx_emp_metadata ON employees USING GIN(metadata);

-- 3. Partial Index (indexed only for active employees)
CREATE INDEX idx_active_emp ON employees(department_id) WHERE salary > 50000;
```

---
<ProgressTracker currentSection=13 totalSections=26 />

## 13. Views & Materialized Views

- **View**: A virtual table representing a saved query. Runs the underlying query every time it is referenced.
- **Materialized View**: Persists the query result to disk. Must be refreshed manually or programmatically.

```sql
-- Materialized View
CREATE MATERIALIZED VIEW dept_salary_summary AS
SELECT department_id, SUM(salary) AS total_payout
FROM employees
GROUP BY department_id;

-- Refresh Materialized View concurrently (requires a unique index on the view)
CREATE UNIQUE INDEX idx_mv_dept_id ON dept_salary_summary(department_id);
REFRESH MATERIALIZED VIEW CONCURRENTLY dept_salary_summary;
```

---
<ProgressTracker currentSection=14 totalSections=26 />

## 14. Stored Procedures, Functions & Triggers

PostgreSQL supports writing database logic using PL/pgSQL.

```sql
-- Trigger Function to update timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger definition
CREATE TRIGGER update_emp_modtime
BEFORE UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
```

---
<ProgressTracker currentSection=15 totalSections=26 />

## 15. Transactions & Concurrency Control (MVCC)

PostgreSQL implements MVCC (Multi-Version Concurrency Control). When updating a row, PostgreSQL writes a new version (tuple) of that row instead of overwriting the old one.

### Isolation Levels
1. **Read Committed** (Default): Prevents dirty reads.
2. **Repeatable Read**: Prevents dirty reads and non-repeatable reads.
3. **Serializable**: Provides full transaction isolation.

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Transaction operations
COMMIT;
```

<ProgressTracker currentSection=16 totalSections=26 />

## 16. Locks

PostgreSQL uses multiple lock modes (Shared, Exclusive, RowShare, AccessExclusive).

```mermaid
graph TD
    LockMgr[Postgres Locks] --> RowLock[Row-level: Shared/Exclusive during UPDATE]
    LockMgr --> TableLock[Table-level: AccessExclusive during ALTER TABLE]
    LockMgr --> AdvisoryLock[Advisory: Custom application-level locks]
```

---
<ProgressTracker currentSection=17 totalSections=26 />

## 17. Performance Optimization

To analyze a slow-running query, prepend it with `EXPLAIN (ANALYZE, BUFFERS)` to see the actual execution plan, node operations, cost, and time details.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM employees WHERE email = 'john.doe@company.com';
```

### Key Optimizations
- **Index Tuning**: Avoid indexing columns with low selectivity.
- **Partitioning**: Split tables by range or hash (e.g., partition orders by order date).
- **Connection Pooling**: Use PgBouncer to manage database connections.

---
<ProgressTracker currentSection=18 totalSections=26 />

## 18. Replication & High Availability

PostgreSQL supports physical streaming replication and logical replication.

```mermaid
graph LR
    Primary[Primary Database: Write/Read] -->|WAL Shipping| Replica1[Physical Replica 1: Read-Only]
    Primary -->|WAL Shipping| Replica2[Physical Replica 2: Read-Only]
```

### High Availability Tooling
- **Patroni**: Template for HA using Consul, Etcd, or ZooKeeper for leader election and automatic failover.
- **PgBouncer**: Lightweight connection pooler to reduce connection overhead.

---
<ProgressTracker currentSection=19 totalSections=26 />

## 20. Security

PostgreSQL authentication is managed via `pg_hba.conf` (Host-Based Authentication).

### Best Practices
- **Never use the superuser account (`postgres`) in application backends.**
- **Use SSL/TLS** connections to encrypt traffic between client and server.
- **Implement Role-Based Access Control (RBAC)**:
  ```sql
  CREATE ROLE readonly_app;
  GRANT USAGE ON SCHEMA public TO readonly_app;
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_app;
  ```

---
<ProgressTracker currentSection=20 totalSections=26 />

## 22. Monitoring & Metrics

Key system catalogs to monitor performance:
- `pg_stat_activity`: Shows currently executing queries and connection states.
- `pg_stat_statements`: Captures query execution time metrics.

```sql
-- Find top 5 slowest queries
SELECT query, calls, total_exec_time, mean_exec_time 
FROM pg_stat_statements 
ORDER BY total_exec_time DESC 
LIMIT 5;
```

---
<ProgressTracker currentSection=21 totalSections=26 />

## 24. Integration & ORM Support

### Python (using `psycopg3` and `SQLAlchemy`)
<Tabs>
  <Tab label="Syntax & Example">

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connect using pgpool / psycopg
engine = create_engine("postgresql+psycopg://postgres:secret@localhost:5432/mydb", pool_size=20)
SessionLocal = sessionmaker(bind=engine)
```

  </Tab>
  <Tab label="Interactive Playground">
    <InteractiveExample 
      language="python"
      initialCode="from sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker\n\n# Connect using pgpool / psycopg\nengine = create_engine(\"postgresql+psycopg://postgres:secret@localhost:5432/mydb\", pool_size=20)\nSessionLocal = sessionmaker(bind=engine)" 
      instruction="Execute and edit this PYTHON example."
    />
  </Tab>
</Tabs>

### Node.js (using `Prisma` ORM)
```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

---
<ProgressTracker currentSection=22 totalSections=26 />

## 26. AI Integration: `pgvector`

PostgreSQL supports vector database functionality natively using the `pgvector` extension. This is critical for storing and querying vector embeddings in RAG and LLM systems.

```sql
-- 1. Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create table with vector column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536) -- 1536 dimensions for OpenAI text-embedding-3-small
);

-- 3. Query closest documents using Cosine Distance (<=> operator)
SELECT content, 1 - (embedding <=> '[0.012, -0.023, ...]') AS similarity
FROM documents
ORDER BY embedding <=> '[0.012, -0.023, ...]'
LIMIT 3;
```

---
<ProgressTracker currentSection=23 totalSections=26 />

## 29. Common Errors & Solutions

### Error 1: "FATAL: remaining connection slots are reserved for non-replication superuser connections"
- **Reason**: Database ran out of connection slots.
- **Solution**: Install and configure **PgBouncer** connection pooler, or increase `max_connections` in `postgresql.conf`.

### Error 2: "ERROR: deadlock detected"
- **Reason**: Two transactions are blocked waiting for locks held by each other.
- **Solution**: Ensure your application acquires locks in the same table order, and keep transactions short.

---

<ProgressTracker currentSection=24 totalSections=26 />

## 30. Interview Questions

### Q1: What is the difference between `VACUUM` and `VACUUM FULL`?
- **VACUUM**: Reclaims space from dead tuples and makes it available for new rows in the same table without locking the table.
- **VACUUM FULL**: Rewrites the entire table to a new file, reclaiming all empty space and shrinking the file size on disk. It requires an AccessExclusiveLock, blocking all reads and writes.

---

<ProgressTracker currentSection=25 totalSections=26 />

## 31. Cheat Sheet & Checklist

- **Connect to database**: `psql -U username -d dbname`
- **List tables**: `\dt`
- **Show execution plan**: `EXPLAIN ANALYZE <query>`
- **Show active queries**: `SELECT * FROM pg_stat_activity;`

---

<ProgressTracker currentSection=26 totalSections=26 />

## 35. Final Summary

PostgreSQL stands as the industry-standard relational database due to its incredible performance tuning capabilities, extensible architecture, and extensions like `pgvector`. Ensure you utilize connection pooling, run `ANALYZE` frequently, and monitor your index usage.

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
