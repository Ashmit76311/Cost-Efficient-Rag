# Databases

A database is an organized collection of structured data stored electronically. Database management systems (DBMS) provide mechanisms for storing, retrieving, updating, and managing data efficiently and securely.

## Relational Databases and SQL

Relational databases organize data into tables (relations) with rows (tuples) and columns (attributes). Each table has a primary key that uniquely identifies each row. Foreign keys establish relationships between tables. SQL (Structured Query Language) is the standard language for interacting with relational databases.

Key SQL operations include SELECT (querying data), INSERT (adding data), UPDATE (modifying data), DELETE (removing data), and JOIN (combining data from multiple tables). JOINs include INNER JOIN (matching rows from both tables), LEFT JOIN (all rows from left table plus matches), RIGHT JOIN, and FULL OUTER JOIN. Popular relational databases include PostgreSQL, MySQL, SQLite, and Oracle.

## Normalization

Database normalization is the process of organizing tables to reduce data redundancy and improve data integrity. The normal forms are:

- **1NF (First Normal Form)**: Each column contains atomic values (no repeating groups or arrays).
- **2NF (Second Normal Form)**: Meets 1NF and all non-key attributes are fully dependent on the entire primary key (no partial dependencies).
- **3NF (Third Normal Form)**: Meets 2NF and no non-key attribute depends on another non-key attribute (no transitive dependencies).
- **BCNF (Boyce-Codd Normal Form)**: A stricter version of 3NF where every determinant is a candidate key.

Over-normalization can hurt performance due to excessive joins. In practice, most databases are normalized to 3NF, with some controlled denormalization for performance-critical queries.

## ACID Properties

ACID properties guarantee reliable transaction processing:

- **Atomicity**: A transaction is all-or-nothing. If any part fails, the entire transaction is rolled back.
- **Consistency**: A transaction brings the database from one valid state to another, maintaining all defined rules and constraints.
- **Isolation**: Concurrent transactions execute as if they were sequential. Isolation levels include Read Uncommitted, Read Committed, Repeatable Read, and Serializable.
- **Durability**: Once a transaction is committed, the changes persist even in the event of system failure (typically through write-ahead logging).

## Indexing

An index is a data structure that improves the speed of data retrieval at the cost of additional storage space and slower writes. B-tree indexes are the most common type in relational databases, supporting equality and range queries with O(log n) lookup time. Hash indexes provide O(1) lookup for equality queries but don't support range queries.

A composite index covers multiple columns. The order of columns matters — a composite index on (A, B) can efficiently query on A alone or on A and B together, but not on B alone. Over-indexing wastes storage and slows down insert/update operations, so indexes should be created based on actual query patterns.

## NoSQL Databases

NoSQL databases provide alternative data models for specific use cases:

- **Document stores** (MongoDB, CouchDB): Store data as JSON-like documents. Flexible schema, good for hierarchical data.
- **Key-value stores** (Redis, DynamoDB): Simple key-value pairs. Extremely fast for simple lookups and caching.
- **Column-family stores** (Cassandra, HBase): Store data in column families. Good for large-scale distributed data with high write throughput.
- **Graph databases** (Neo4j, ArangoDB): Store data as nodes and edges. Optimized for relationship-heavy queries like social networks and recommendation engines.

## SQL vs NoSQL

SQL databases are best for structured data with complex relationships, ACID compliance needs, and complex queries. NoSQL databases excel at horizontal scaling, flexible schemas, high write throughput, and specific access patterns. Many modern applications use a polyglot persistence approach, combining multiple database types based on the needs of different services.
