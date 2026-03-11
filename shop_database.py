# Import necessary SQLAlchemy modules
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Create engine and session
engine = create_engine('sqlite:///shop.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# -------------------------
# Define Tables
# -------------------------

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    status = Column(Boolean, default=False)  # False = not shipped

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")


# -------------------------
# Create Tables
# -------------------------

Base.metadata.create_all(engine)
print("Tables created successfully!")


# -------------------------
# Insert Users
# -------------------------

if not session.query(User).filter_by(email="alice@example.com").first():
    session.add(User(name="Alice", email="alice@example.com"))

if not session.query(User).filter_by(email="bob@example.com").first():
    session.add(User(name="Bob", email="bob@example.com"))

session.commit()
print("Users added successfully!")


# -------------------------
# Insert Products
# -------------------------

if not session.query(Product).filter_by(name="Laptop").first():
    session.add(Product(name="Laptop", price=1200))

if not session.query(Product).filter_by(name="Mouse").first():
    session.add(Product(name="Mouse", price=25))

if not session.query(Product).filter_by(name="Keyboard").first():
    session.add(Product(name="Keyboard", price=45))

session.commit()
print("Products added successfully!")


# -------------------------
# Insert Orders
# -------------------------

alice = session.query(User).filter_by(email="alice@example.com").first()
bob = session.query(User).filter_by(email="bob@example.com").first()

laptop = session.query(Product).filter_by(name="Laptop").first()
mouse = session.query(Product).filter_by(name="Mouse").first()
keyboard = session.query(Product).filter_by(name="Keyboard").first()

if not session.query(Order).filter_by(user_id=alice.id, product_id=laptop.id).first():
    session.add(Order(user_id=alice.id, product_id=laptop.id, quantity=1))

if not session.query(Order).filter_by(user_id=alice.id, product_id=mouse.id).first():
    session.add(Order(user_id=alice.id, product_id=mouse.id, quantity=2))

if not session.query(Order).filter_by(user_id=bob.id, product_id=keyboard.id).first():
    session.add(Order(user_id=bob.id, product_id=keyboard.id, quantity=1))

if not session.query(Order).filter_by(user_id=bob.id, product_id=mouse.id).first():
    session.add(Order(user_id=bob.id, product_id=mouse.id, quantity=3))

session.commit()
print("Orders added successfully!")


# -------------------------
# Queries
# -------------------------

# Retrieve all users
print("\nAll Users:")
users = session.query(User).all()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")


# Retrieve all products
print("\nAll Products:")
products = session.query(Product).all()
for product in products:
    print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}")


# Retrieve all orders
print("\nAll Orders:")
orders = session.query(Order).all()
for order in orders:
    print(f"User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}")


# -------------------------
# Update Product Price
# -------------------------

laptop_product = session.query(Product).filter_by(name="Laptop").first()

if laptop_product:
    print(f"\nOld Laptop Price: ${laptop_product.price}")
    laptop_product.price = 1100
    session.commit()
    print(f"Updated Laptop Price: ${laptop_product.price}")


# -------------------------
# Delete User
# -------------------------

user_to_delete = session.query(User).filter_by(name="Bob").first()

if user_to_delete:
    print(f"\nDeleting User: {user_to_delete.name}")
    session.delete(user_to_delete)
    session.commit()
    print("User deleted successfully!")


# -------------------------
# Bonus: Order Status
# -------------------------

orders = session.query(Order).all()

for i, order in enumerate(orders):
    order.status = (i % 2 == 0)

session.commit()
print("\nOrder status updated (shipped / not shipped)")


# -------------------------
# Query Unshipped Orders
# -------------------------

print("\nUnshipped Orders:")

unshipped_orders = session.query(Order).filter_by(status=False).all()

for order in unshipped_orders:
    user_name = order.user.name if order.user else "Deleted User"
    product_name = order.product.name if order.product else "Deleted Product"

    print(f"User: {user_name}, Product: {product_name}, Quantity: {order.quantity}")

# -------------------------
# Count Orders Per User
# -------------------------

print("\nTotal Orders Per User:")

order_counts = session.query(User.name, func.count(Order.id)).join(Order).group_by(User.id).all()

for name, count in order_counts:
    print(f"{name}: {count} order(s)")