# Import necessary SQLAlchemy tools needed to build the database
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Step 2: Create the database engine
engine = create_engine('sqlite:///shop.db')

# Step 3: Create a base class for our tables
Base = declarative_base()

# Step 4: Create a session to talk to the database
Session = sessionmaker(bind=engine)
session = Session()

# Step 5: Create the User table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    # Relationship: one user can have many orders
    orders = relationship("Order", back_populates="user")
    
    # Step 6: Create the Product table
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    # Relationship: one product can appear in many orders
    orders = relationship("Order", back_populates="product")
    
    # Step 7: Create the Order table
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    # Relationships
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")