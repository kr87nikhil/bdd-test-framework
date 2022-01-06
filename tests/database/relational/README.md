# SQL Alchemy
It has several distinct areas of functionality which can be used individually or combined together. Core contains the breadth of SQLAlchemy’s SQL and database integration and description services, the most prominent part of this being the <u>SQL Expression Language</u>

<img src='resources/SQL Alchemy.png' height='320'><br>

The two most significant front-facing portions of SQLAlchemy are the 
1. Core 
    - Has schema-centric view, focused around tables, keys and SQL concepts
2. ORM (Object relational mapping)
    - Uses object-centric view, encapsulate schema with business objects
<br><br>

## Dialect
The dialect is the system SQLAlchemy uses to communicate with various types of DBAPI implementations and databases. All dialects require that an appropriate DBAPI driver is installed.

Included dialect:
* PostgreSQL
* MySQL and MariaDB
* SQLite
* Oracle
* Microsoft SQL Server

Engine configuration: https://docs.sqlalchemy.org/en/14/core/engines.html
