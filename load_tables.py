from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
import sys
import json

from data_model import Customer, Address, Supplier


class LoadTables:
    def __init__(self, engine):
        session = sessionmaker(bind=engine)
        self.db_session = session()
        self.fake = Faker()

    def load_customers(self):
        customer_dict_list = list()
        for i in range(1, 101):
            customer_dict = dict()
            customer_dict["customer_id"] = i
            customer_dict["customer_name"] = self.fake.name()
            customer_dict_list.append(customer_dict)
        self.load_records(Customer, customer_dict_list)

    def load_addresses(self):
        address_dict_list = list()
        for i in range(1, 101):
            address_dict = dict()
            address_dict["address_id"] = i
            address_dict["address"] = self.fake.address()
            address_dict["customer_id"] = random.randint(1,100)
            address_dict_list.append(address_dict)
        self.load_records(Address, address_dict_list)

    def load_suppliers(self):
        with open('suppliers.json') as json_file:
            supplier_dict_list = json.load(json_file)
        self.load_records(Supplier, supplier_dict_list)

    def load_records(self, table, records):
        try:
            self.db_session.bulk_insert_mappings(table, records)
            self.db_session.commit()
        except Exception as e:
            print(sys.exc_info())
        finally:
            self.db_session.close()



