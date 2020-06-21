## SQLAlchemy Examples

In order to run the examples in the "sqlalchemy_examples.ipnyb" notebook, you need the following:

- A running database
- The following environment variables corresponding to the database defined on your machine:
    - DB_HOST
    - DB_PORT
    - DB_USER
    - DB_PASS
    - DB
- The following libraries installed
    - SQLAlchemy
    - Faker
    
This repository also includes a database checker utility (db_checker.py) that can be used to verify database schema prior to interacting with it.