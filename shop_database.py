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