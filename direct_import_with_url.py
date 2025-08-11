#!/usr/bin/env python3
"""
Direct import to Railway production database using provided DATABASE_URL
"""
import json
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Use the provided DATABASE_URL
DATABASE_URL = "postgresql://postgres:aJxyryWChNKUztgJvTkasZIlOwidIdqr@shortline.proxy.rlwy.net:50512/railway"

print("=== Railway Production Data Import ===")
print(f"Connecting to: shortline.proxy.rlwy.net:50512")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Load data from local export
    with open('local_data_export.json', 'r') as f:
        data = json.load(f)
    
    # Create tables first (this will handle if they don't exist)
    print("Setting up tables...")
    with engine.connect() as conn:
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS investment (
                id SERIAL PRIMARY KEY,
                investor_name VARCHAR(100) NOT NULL,
                amount FLOAT NOT NULL,
                date TIMESTAMP NOT NULL
            )
        '''))
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS expense (
                id SERIAL PRIMARY KEY,
                description VARCHAR(200) NOT NULL,
                amount FLOAT NOT NULL,
                date TIMESTAMP NOT NULL,
                category VARCHAR(100)
            )
        '''))
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS sale (
                id SERIAL PRIMARY KEY,
                amount FLOAT NOT NULL,
                date TIMESTAMP NOT NULL,
                description VARCHAR(200)
            )
        '''))
        conn.commit()
    
    # Clear existing data (now safe since tables exist)
    print("Clearing existing data...")
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM investment'))
        conn.execute(text('DELETE FROM expense'))
        conn.execute(text('DELETE FROM sale'))
        conn.commit()
    
    # Import investments
    investments = data.get('investments', [])
    print(f"Importing {len(investments)} investments...")
    for inv in investments:
        session.execute(
            text('INSERT INTO investment (investor_name, amount, date) VALUES (:name, :amount, :date)'),
            {'name': inv['investor_name'], 'amount': float(inv['amount']), 'date': inv['date']}
        )
    
    # Import expenses
    expenses = data.get('expenses', [])
    print(f"Importing {len(expenses)} expenses...")
    for exp in expenses:
        session.execute(
            text('INSERT INTO expense (description, amount, date, category) VALUES (:desc, :amount, :date, :category)'),
            {'desc': exp['description'], 'amount': float(exp['amount']), 'date': exp['date'], 'category': exp['category']}
        )
    
    # Import sales
    sales = data.get('sales', [])
    print(f"Importing {len(sales)} sales...")
    for sale in sales:
        session.execute(
            text('INSERT INTO sale (amount, date, description) VALUES (:amount, :date, :desc)'),
            {'amount': float(sale['amount']), 'date': sale['date'], 'desc': sale['description']}
        )
    
    session.commit()
    
    # Verify the import
    inv_count = session.execute(text('SELECT COUNT(*) FROM investment')).scalar()
    exp_count = session.execute(text('SELECT COUNT(*) FROM expense')).scalar()
    sale_count = session.execute(text('SELECT COUNT(*) FROM sale')).scalar()
    
    print(f"\n=== Import Complete ===")
    print(f"Investments: {inv_count}")
    print(f"Expenses: {exp_count}")
    print(f"Sales: {sale_count}")
    print("\nSUCCESS: Data imported to Railway production database!")
    print("Check your hosted app - data should now be visible.")
    
except Exception as e:
    print(f"ERROR: {e}")
    session.rollback()
    raise
finally:
    session.close()