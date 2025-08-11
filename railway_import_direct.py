#!/usr/bin/env python3
"""
Direct Railway Import - Uses Railway's DATABASE_URL automatically
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
    print("=== Railway Production Data Import ===")
    
    # Get DATABASE_URL from Railway environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL not found in environment")
        print("Make sure you're running this with: railway run python railway_import_direct.py")
        return
    
    # Fix postgres:// to postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    print(f"Using Railway database: {database_url.split('@')[1] if '@' in database_url else 'Production DB'}")
    
    try:
        # Create database connection
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Load local data
        print("Loading local data...")
        with open('local_data_export.json', 'r') as f:
            data = json.load(f)
        
        # Clear existing data
        print("Clearing existing production data...")
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM investment"))
            conn.execute(text("DELETE FROM expense"))
            conn.execute(text("DELETE FROM sale"))
            conn.commit()
        
        # Create tables if needed
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
        
        # Import investments
        investments = data.get('investments', [])
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
        
        # Import expenses
        expenses = data.get('expenses', [])
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
        
        # Import sales
        sales = data.get('sales', [])
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
        
        # Verify import
        print("\nVerifying import...")
        result = session.execute(text("SELECT COUNT(*) FROM investment"))
        inv_count = result.scalar()
        result = session.execute(text("SELECT COUNT(*) FROM expense"))
        exp_count = result.scalar()
        result = session.execute(text("SELECT COUNT(*) FROM sale"))
        sale_count = result.scalar()
        
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

if __name__ == "__main__":
    main()