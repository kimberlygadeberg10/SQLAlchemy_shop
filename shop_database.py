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
    
    # Step 8: Create all tables in the database
Base.metadata.create_all(engine)

print("Tables created successfully!")

# Step 9: Add sample users
user1 = User(name="Alice", email="alice@example.com")
user2 = User(name="Bob", email="bob@example.com")

# Add to session and commit
session.add_all([user1, user2])
session.commit()

print("Users added successfully!")

# Step 10: Add sample products
product1 = Product(name="Laptop", price=1200)
product2 = Product(name="Mouse", price=25)
product3 = Product(name="Keyboard", price=45)

# Add to session and commit
session.add_all([product1, product2, product3])
session.commit()

print("Products added successfully!")

if not session.query(User).filter_by(email="alice@example.com").first():
    session.add(User(name="Alice", email="alice@example.com"))

if not session.query(User).filter_by(email="bob@example.com").first():
    session.add(User(name="Bob", email="bob@example.com"))

session.commit()

# Step 11: Add sample orders (avoid duplicates)
# Fetch users and products from the database
alice = session.query(User).filter_by(email="alice@example.com").first()
bob = session.query(User).filter_by(email="bob@example.com").first()

laptop = session.query(Product).filter_by(name="Laptop").first()
mouse = session.query(Product).filter_by(name="Mouse").first()
keyboard = session.query(Product).filter_by(name="Keyboard").first()

# Only add orders if they don't already exist
if not session.query(Order).filter_by(user_id=alice.id, product_id=laptop.id).first():
    order1 = Order(user_id=alice.id, product_id=laptop.id, quantity=1)
    session.add(order1)

if not session.query(Order).filter_by(user_id=alice.id, product_id=mouse.id).first():
    order2 = Order(user_id=alice.id, product_id=mouse.id, quantity=2)
    session.add(order2)

if not session.query(Order).filter_by(user_id=bob.id, product_id=keyboard.id).first():
    order3 = Order(user_id=bob.id, product_id=keyboard.id, quantity=1)
    session.add(order3)

if not session.query(Order).filter_by(user_id=bob.id, product_id=mouse.id).first():
    order4 = Order(user_id=bob.id, product_id=mouse.id, quantity=3)
    session.add(order4)

session.commit()
print("Orders added successfully!")

# Step 12: Retrieve and print all users
print("\nAll Users:")
users = session.query(User).all()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    
    # Step 13: Retrieve and print all products
print("\nAll Products:")
products = session.query(Product).all()
for product in products:
    print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}")
    
    # Step 14: Retrieve all orders with user and product details
print("\nAll Orders:")
orders = session.query(Order).all()
for order in orders:
    print(f"User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}")
    
    # Step 15: Update a product's price
# Example: Change the price of "Laptop" from 1200 to 1100
laptop_product = session.query(Product).filter_by(name="Laptop").first()
if laptop_product:
    print(f"\nOld Laptop Price: ${laptop_product.price}")
    laptop_product.price = 1100
    session.commit()
    print(f"Updated Laptop Price: ${laptop_product.price}")