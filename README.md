# SQLAlchemy Shop Assignment - Quick Overview

## What It Does
A small relational database project using **Python + SQLAlchemy**:

- Users, Products, Orders tables with relationships  
- Add, read, update, delete data (CRUD)  
- Bonus: track shipped/unshipped orders and count total orders per user  

---

## Setup & Run

1. Install SQLAlchemy:

```bash
python3 -m pip install SQLAlchemy

2. Run the script:

python3 shop_database.py

Creates shop.db with sample users, products, and orders

Prints all users, products, orders, updated prices, and order statuses

Key Highlights

Relationships: Users ↔ Orders ↔ Products

Data Validation: Prevents duplicate users/products

Bonus Features:

Boolean status for orders (shipped or not)

Query unshipped orders

Count total orders per user

Author: Kimberly Gadeberg