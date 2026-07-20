# Pyspark Cheatsheet Master Guide

A comprehensive, industry-grade guide to Pyspark Cheatsheet for data engineers, architects, and developers.

---

<ProgressTracker currentSection=1 totalSections=5 />

## 1. Introduction
Apache Spark is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters.

<ProgressTracker currentSection=2 totalSections=5 />

## 2. Why it exists & Problems it solves
Traditional MapReduce writes intermediate results to physical disk, causing massive disk I/O bottlenecks. Spark solves this by introducing in-memory processing via Resilient Distributed Datasets (RDDs).

<ProgressTracker currentSection=3 totalSections=5 />

## 3. Internal Working & Architecture
Spark uses a Master-Worker clustering model. The Driver program coordinates execution, creates the SparkSession, builds the Logical/Physical Execution Plans, and sends tasks to Executor worker nodes.

```mermaid
graph TD
    Driver[Driver Program / SparkSession] -->|DAG Scheduler| ClusterManager[Cluster Manager: YARN/K8s]
    ClusterManager --> Worker1[Worker Node 1 / Executor]
    ClusterManager --> Worker2[Worker Node 2 / Executor]
    Worker1 --> Task1[Task 1]
    Worker2 --> Task2[Task 2]
```

<ProgressTracker currentSection=4 totalSections=5 />

## 4. Hands-on PySpark DataFrame Operations
<Tabs>
  <Tab label="Syntax & Example">

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("ProductionETL") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# Create dataframe
df = spark.read.json("s3a://data-lake/raw/events.json")

# Transform data
processed_df = df.filter(col("status") == "ACTIVE") \
    .withColumn("priority", when(col("score") > 80, "HIGH").otherwise("LOW"))

# Write output to Delta Lake partitioned by date
processed_df.write \
    .format("delta") \
    .partitionBy("event_date") \
    .mode("overwrite") \
    .save("s3a://data-lake/processed/events")
```

  </Tab>
  <Tab label="Interactive Playground">
    <InteractiveExample 
      language="python"
      initialCode="from pyspark.sql import SparkSession\nfrom pyspark.sql.functions import col, when\n\n# Initialize SparkSession\nspark = SparkSession.builder \\\n    .appName(\"ProductionETL\") \\\n    .config(\"spark.sql.shuffle.partitions\", \"200\") \\\n    .getOrCreate()\n\n# Create dataframe\ndf = spark.read.json(\"s3a://data-lake/raw/events.json\")\n\n# Transform data\nprocessed_df = df.filter(col(\"status\") == \"ACTIVE\") \\\n    .withColumn(\"priority\", when(col(\"score\") > 80, \"HIGH\").otherwise(\"LOW\"))\n\n# Write output to Delta Lake partitioned by date\nprocessed_df.write \\\n    .format(\"delta\") \\\n    .partitionBy(\"event_date\") \\\n    .mode(\"overwrite\") \\\n    .save(\"s3a://data-lake/processed/events\")" 
      instruction="Execute and edit this PYTHON example."
    />
  </Tab>
</Tabs>

<ProgressTracker currentSection=5 totalSections=5 />

## 5. Performance Optimization & Troubleshooting
- **Data Skew**: Use salting techniques to distribute hot keys.
- **OOM Errors**: Increase executor memory (`spark.executor.memory`) and tune serialization config (`spark.serializer=org.apache.spark.serializer.KryoSerializer`).

---

---

### Knowledge Verification Check

<Quiz 
  question="What are the two core phases of a MapReduce job?" 
  options=["Read and Write phases.", "Map (transforming input records) and Reduce (aggregating key-value pairs after shuffling).", "Compile and Execute phases.", "Load and Partition phases."] 
  answerIndex=1 
  explanation="MapReduce divides work. The Map step processes input lines to produce intermediate key-value sets. The Reduce step summarizes those values per key." 
/>

<Quiz 
  question="Why is Apache Spark faster than legacy Hadoop MapReduce for iterative algorithms?" 
  options=["It runs queries in the web browser.", "It performs processing in-memory (RAM) and caches intermediate states, avoiding MapReduce's frequent disk reads and writes.", "It uses NoSQL databases internally.", "It bypasses network communication entirely."] 
  answerIndex=1 
  explanation="Hadoop writes intermediate step outputs to HDFS disk. Spark keeps data in memory as Resilient Distributed Datasets (RDDs) and updates lazily, boosting speed." 
/>

<Quiz 
  question="What does a Resilient Distributed Dataset (RDD) represent in Spark?" 
  options=["A SQL table stored on a single host.", "A read-only, partitioned collection of records that can be operated on in parallel across a cluster with automatic lineage-based fault tolerance.", "A backup directory of CSV files.", "An index structure for fast search."] 
  answerIndex=1 
  explanation="RDDs are Spark's core abstraction. Distributed across worker nodes, RDDs track transformation history (lineage), allowing partitions to be rebuilt if nodes fail." 
/>

<Quiz 
  question="How are messages distributed within an Apache Kafka Topic?" 
  options=["All messages are written to one single log file.", "Topics are split into Partitions distributed across brokers; messages are appended sequentially to partitions using keys for routing.", "Messages are stored in MongoDB collections.", "Messages are deleted automatically on read."] 
  answerIndex=1 
  explanation="Partitions enable Kafka to scale. A partition is an ordered append-only commit log. Distributing partitions across cluster brokers supports high write and read scaling." 
/>

<Quiz 
  question="What does a Kafka Consumer Group enable?" 
  options=["Running multiple database queries concurrently.", "Coordinated parallel reading of topic partitions, where each partition is assigned to exactly one consumer member in the group.", "Creating backup copies of Kafka topics.", "Compiling stream processing binaries."] 
  answerIndex=1 
  explanation="Consumer groups partition message reading. By coordinating partition assignments, Kafka scales processing: adding group members divides the read workload." 
/>

<Quiz 
  question="What is a Directed Acyclic Graph (DAG) in data workflow orchestration (e.g. Apache Airflow)?" 
  options=["A database schema layout diagram.", "A collection of all tasks to run, organized in a way that reflects their relationships and execution dependencies without loop cycles.", "A network path routing table.", "A type of column-oriented index."] 
  answerIndex=1 
  explanation="Airflow uses DAGs to define workflows. Tasks are represented as nodes. Directed edges define dependencies. The acyclic rule prevents circular dependency loops." 
/>

<Quiz 
  question="How does dbt (data build tool) differ from traditional ETL tools?" 
  options=["It focuses strictly on the 'T' (Transformation) phase in ELT pipelines, compiling SQL models and running them inside the target data warehouse.", "It handles data extraction from APIs.", "It stores data in-memory on local server nodes.", "It compiles SQL into Go binaries."] 
  answerIndex=0 
  explanation="dbt doesn't move data. It acts after data is loaded (ELT), letting analysts write SQL models that dbt compiles and executes as tables/views inside warehouses." 
/>

<Quiz 
  question="What is Schema Evolution in data storage frameworks (like Parquet or Delta Lake)?" 
  options=["Updating database driver software automatically.", "The ability to modify database schema definitions (e.g. adding columns) over time without rewriting historical data files.", "Deleting old database files when schemas change.", "Automatically compiling queries to match new versions."] 
  answerIndex=1 
  explanation="Schema evolution allows column additions or type changes. Query engines read historical data with back-compatibility, avoiding expensive dataset rewrites." 
/>

<Quiz 
  question="What is the difference between Partitioning and Bucketing in large-scale table optimization?" 
  options=["Partitioning is for databases; Bucketing is for cache.", "Partitioning divides tables into directories based on column values (e.g. date); Bucketing splits data into fixed files using a hash function on a key.", "They are synonyms.", "Bucketing encrypts column fields."] 
  answerIndex=1 
  explanation="Partitioning creates folder hierarchies (e.g. `year=2026/month=07`). Bucketing (Clustering) hashes a key column to divide data into equal files within partition paths, optimizing joins." 
/>

<Quiz 
  question="What does Lazy Evaluation mean in Apache Spark execution?" 
  options=["The cluster waits for system idle time before executing jobs.", "Spark delays execution of transformations until an Action (e.g. `count()`, `collect()`) is called, enabling optimization of the entire execution plan.", "Spark runs computations slowly to save energy.", "Queries are executed only on subset samples."] 
  answerIndex=1 
  explanation="Transformations (like `filter()`, `select()`) only build a logical execution plan (DAG). When an action requests output, Spark optimizes and compiles the DAG for execution." 
/>

<Quiz 
  question="What is Change Data Capture (CDC) in data pipelines?" 
  options=["A system for version-controlling SQL files.", "A design pattern that identifies and tracks changes (inserts, updates, deletes) in a source database, streaming those events to target systems in real-time.", "A data quality validation framework.", "A database snapshotting utility."] 
  answerIndex=1 
  explanation="CDC monitors database transaction logs. Whenever modifications occur, events are streamed (e.g. via Debezium and Kafka) to update analytical warehouses immediately." 
/>

<Quiz 
  question="What is the primary difference between Lambda and Kappa data pipeline architectures?" 
  options=["Lambda uses Python; Kappa uses Go.", "Lambda processes data through batch and speed layers in parallel; Kappa processes all data using a single stream processing engine, treating batch as historical stream.", "Kappa uses SQL databases; Lambda uses NoSQL databases.", "Lambda is serverless; Kappa runs on VMs."] 
  answerIndex=1 
  explanation="Lambda balances batch stability and stream latency by using duplicate code paths. Kappa simplifies this by processing all data through a single stream pipeline (e.g., Flink) with raw logs." 
/>
