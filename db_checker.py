from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

from data_model import Base

class DBChecker:
    def __init__(
        self, engine
    ):
        self.session = sessionmaker()
        self.engine = engine
        self.session.configure(bind=self.engine)
        self.db_session = self.session()
        self.database_tables = self.engine.table_names()

    def check_db(self):
        mapped_tables = DBChecker.get_mapped_tables()
        for mapped_table in mapped_tables:
            self.does_table_match(mapped_table)

    def does_table_match(self, mapped_table):
        inspector = inspect(self.engine)
        mapped_table_name = mapped_table.__tablename__
        if mapped_table_name in self.database_tables:
            table_fields = set(
                col["name"].lower()
                for col in inspector.get_columns(mapped_table_name)
            )
            print(f"Database field names for table {mapped_table_name}: {table_fields}")

            mapped_table_fields = set(
                col.key.lower() for col in mapped_table.__table__.columns
            )
            print(f"Mapped field names for mapped table {mapped_table}: {mapped_table_fields}")

            if mapped_table_fields == table_fields:
                return True
            else:
                print(f"There is a column mismatch in the table: {mapped_table_name}")
                return False
        else:
            print(f"Table: {mapped_table_name} does not exist in the database")
            return False

    @staticmethod
    def get_mapped_tables():
        mapped_tables = Base.__subclasses__()
        return mapped_tables
