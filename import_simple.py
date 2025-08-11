#!/usr/bin/env python3
"""
Simple Railway Database Import Script
"""
import os
import sys
import json
from datetime import datetime

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
except ImportError:
    print("Installing required packages...")
    os.system("pip install sqlalchemy psycopg2-binary")
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker

def main():
    print("=== Railway Database Import ===")
    print()
    print("To find your DATABASE_URL:")
    print("1. Go to https://railway.app")
    print("2. Open your Londons Kitchen project")
    print("3. Click on your PostgreSQL database")
    print("4. Go to 'Connect' tab")
    print("5. Copy the DATABASE_URL value")
    print()
    
    url = input("Enter DATABASE_URL: ").strip()
    if not url:
        print("ERROR: No DATABASE_URL provided")
        return
    
    # Fix postgres:// to postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    
    print(f"Connecting to database...")
    
    try:
        # Create database connection
        engine = create_engine(url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Load local data
        print("Loading local data...")
        with open('local_data_export.json', 'r') as f:
            data = json.load(f)
        
        # Clear existing data
        print("Clearing existing data...")
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM investment"))
            conn.execute(text("DELETE FROM expense"))
            conn.execute(text("DELETE FROM sale"))
            conn.commit()
        
        # Create tables
        print("Setting up tables...")
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS investment (
                    id SERIAL PRIMARY KEY,
                    investor_name VARCHAR(100) NOT NULL,
                    amount FLOAT NOT NULL,
                    date TIMESTAMP NOT NULL
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS expense (
                    id SERIAL PRIMARY KEY,
                    description VARCHAR(200) NOT NULL,
                    amount FLOAT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    category VARCHAR(100)
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS sale (
                    id SERIAL PRIMARY KEY,
                    amount FLOAT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    description VARCHAR(200)
                )
            """))
            conn.commit()
        
        # Import data
        investments = data.get('investments', [])
        expenses = data.get('expenses', [])
        sales = data.get('sales', [])
        
        print(f"Importing {len(investments)} investments...")
        for inv in investments:
            session.execute(
                text("INSERT INTO investment (investor_name, amount, date) VALUES (:name, :amount, :date)"),
                {
                    'name': inv['investor_name'],
                    'amount': float(inv['amount']),
                    'date': datetime.fromisoformat(inv['date'].replace('Z', '+00:00'))
                }
            )
        
        print(f"Importing {len(expenses)} expenses...")
        for exp in expenses:
            session.execute(
                text("INSERT INTO expense (description, amount, date, category) VALUES (:desc, :amount, :date, :category)"),
                {
                    'desc': exp['description'],
                    'amount': float(exp['amount']),
                    'date': datetime.fromisoformat(exp['date'].replace('Z', '+00:00')),
                    'category': exp['category']
                }
            )
        
        print(f"Importing {len(sales)} sales...")
        for sale in sales:
            session.execute(
                text("INSERT INTO sale (amount, date, description) VALUES (:amount, :date, :desc)"),
                {
                    'amount': float(sale['amount']),
                    'date': datetime.fromisoformat(sale['date'].replace('Z', '+00:00')),
                    'desc': sale['description']
                }
            )
        
        session.commit()
        
        # Verify
        print("\nVerifying...")
        result = session.execute(text("SELECT COUNT(*) FROM investment"))
        inv_count = result.scalar()
        result = session.execute(text("SELECT COUNT(*) FROM expense"))
        exp_count = result.scalar()
        result = session.execute(text("SELECT COUNT(*) FROM sale"))
        sale_count = result.scalar()
        
        print(f"\n=== Results ===")
        print(f"Investments: {inv_count}")
        print(f"Expenses: {exp_count}")
        print(f"Sales: {sale_count}")
        print("\nImport complete! Check your hosted app.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        if 'session' in locals():
            session.rollback()
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()