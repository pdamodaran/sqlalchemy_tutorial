from sqlalchemy import Integer, ForeignKey, String, Column, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)

    addresses = relationship("Address", backref="customer")


class Address(Base):
    __tablename__ = "address"
    address_id = Column(Integer, primary_key=True)
    address = Column(String)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))


class Supplier(Base):
    __tablename__ = "supplier"
    supplier_id = Column(Integer, primary_key=True)
    supplier_name = Column(String)


class Product(Base):
    __tablename__ = "product"
    product_id=Column(Integer, primary_key=True)
    product_name=Column(String(32))
    quantity=Column(Integer)
    price=Column(Numeric)



