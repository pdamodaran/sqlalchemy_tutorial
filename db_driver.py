import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

import warnings

from db_checker import DBChecker

warnings.filterwarnings('ignore')

from data_model import Base
from load_tables import LoadTables


class DBDriver:
    def __init__(self):
        self.engine = self.get_engine()
        self.session_maker = sessionmaker()
        self.session_maker.configure(bind=self.engine)

    @contextmanager
    def session_scope(self):
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_engine(self):
        connection_string = DBDriver.get_connection_string()
        engine = create_engine(connection_string, echo=False)
        return engine

    @staticmethod
    def get_connection_string():
        host = os.environ["POSTGRES_HOST"]
        port = os.environ["POSTGRES_PORT"]
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        dbname = os.environ["POSTGRES_DB"]

        connection_string = "{}://{}:{}@{}:{}/{}".format(
            "postgresql", user, password, host, port, dbname
        )
        return connection_string

    def create_tables(self):
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def load_data(self):
        load_tables = LoadTables(self.engine)
        load_tables.load_customers()
        load_tables.load_addresses()
        load_tables.load_suppliers()


if __name__ == "__main__":
    dbdriver = DBDriver()
    dbdriver.create_tables()
    dbchecker = DBChecker(dbdriver.engine)
    dbchecker.check_db()
    dbdriver.load_data()