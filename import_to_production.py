#!/usr/bin/env python3
"""
Production database import script for Railway deployment
This script imports local data to the Railway production PostgreSQL database
"""
import os
import sys
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Force use of production database URL
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL environment variable not found!")
    print("💡 To run this script, use:")
    print("   railway run python import_to_production.py")
    print("   OR")
    print("   DATABASE_URL=your_railway_db_url python import_to_production.py")
    sys.exit(1)

# Handle Railway database URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print("=== Production Database Import ===")
print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Production DB'}")

# Create engine for production database
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def create_tables():
    """Create tables in production database"""
    print("Creating tables...")
    
    create_investments_table = """
    CREATE TABLE IF NOT EXISTS investment (
        id SERIAL PRIMARY KEY,
        investor_name VARCHAR(100) NOT NULL,
        amount FLOAT NOT NULL,
        date TIMESTAMP NOT NULL
    );
    """
    
    create_expenses_table = """
    CREATE TABLE IF NOT EXISTS expense (
        id SERIAL PRIMARY KEY,
        description VARCHAR(200) NOT NULL,
        amount FLOAT NOT NULL,
        date TIMESTAMP NOT NULL,
        category VARCHAR(100)
    );
    """
    
    create_sales_table = """
    CREATE TABLE IF NOT EXISTS sale (
        id SERIAL PRIMARY KEY,
        amount FLOAT NOT NULL,
        date TIMESTAMP NOT NULL,
        description VARCHAR(200)
    );
    """
    
    with engine.connect() as conn:
        conn.execute(text(create_investments_table))
        conn.execute(text(create_expenses_table))
        conn.execute(text(create_sales_table))
        conn.commit()

def import_data():
    """Import data from local_data_export.json to production"""
    try:
        # Load local data
        with open('local_data_export.json', 'r') as f:
            data = json.load(f)
        
        print("Clearing existing production data...")
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM investment"))
            conn.execute(text("DELETE FROM expense"))
            conn.execute(text("DELETE FROM sale"))
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
                    'date': datetime.fromisoformat(inv['date'])
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
                    'date': datetime.fromisoformat(exp['date']),
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
                    'date': datetime.fromisoformat(sale['date']),
                    'desc': sale['description']
                }
            )
        
        session.commit()
        
        # Verify import
        result = session.execute(text("SELECT COUNT(*) as count FROM investment"))
        inv_count = result.scalar()
        result = session.execute(text("SELECT COUNT(*) as count FROM expense"))
        exp_count = result.scalar()
        result = session.execute(text("SELECT COUNT(*) as count FROM sale"))
        sale_count = result.scalar()
        
        print("\n=== Import Summary ===")
        print(f"Investments: {inv_count}")
        print(f"Expenses: {exp_count}")
        print(f"Sales: {sale_count}")
        
        if inv_count > 0 or exp_count > 0:
            print("✅ Data successfully imported to production database!")
            print("🌐 Check your hosted app - the data should now be visible.")
        else:
            print("⚠️ No data was imported. Check local_data_export.json file.")
    
    except Exception as e:
        print(f"❌ Error during import: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    create_tables()
    import_data()