#!/usr/bin/env python3
"""
Railway Database Import Fix
This script fixes the Unicode issue and provides clear instructions for importing data
"""
import os
import sys
import json
import tempfile

def create_import_script(database_url):
    """Create a temporary import script without Unicode characters"""
    
    script_content = f'''#!/usr/bin/env python3
"""
Railway Production Data Import
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
    print("Starting Railway production data import...")
    
    # Database connection
    database_url = "{database_url}"
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Load data
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
        print("Creating tables...")
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
        print(f"Importing {{len(investments)}} investments...")
        for inv in investments:
            session.execute(
                text("INSERT INTO investment (investor_name, amount, date) VALUES (:name, :amount, :date)"),
                {{
                    'name': inv['investor_name'],
                    'amount': float(inv['amount']),
                    'date': datetime.fromisoformat(inv['date'].replace('Z', '+00:00'))
                }}
            )
        
        # Import expenses
        expenses = data.get('expenses', [])
        print(f"Importing {{len(expenses)}} expenses...")
        for exp in expenses:
            session.execute(
                text("INSERT INTO expense (description, amount, date, category) VALUES (:desc, :amount, :date, :category)"),
                {{
                    'desc': exp['description'],
                    'amount': float(exp['amount']),
                    'date': datetime.fromisoformat(exp['date'].replace('Z', '+00:00')),
                    'category': exp['category']
                }}
            )
        
        # Import sales
        sales = data.get('sales', [])
        print(f"Importing {{len(sales)}} sales...")
        for sale in sales:
            session.execute(
                text("INSERT INTO sale (amount, date, description) VALUES (:amount, :date, :desc)"),
                {{
                    'amount': float(sale['amount']),
                    'date': datetime.fromisoformat(sale['date'].replace('Z', '+00:00')),
                    'desc': sale['description']
                }}
            )
        
        session.commit()
        
        # Verify
        print("\\nVerifying import...")
        result = session.execute(text("SELECT COUNT(*) FROM investment"))
        inv_count = result.scalar()
        result = session.execute(text("SELECT COUNT(*) FROM expense"))
        exp_count = result.scalar()
        result = session.execute(text("SELECT COUNT(*) FROM sale"))
        sale_count = result.scalar()
        
        print(f"\\n=== Import Results ===")
        print(f"Investments: {{inv_count}}")
        print(f"Expenses: {{exp_count}}")
        print(f"Sales: {{sale_count}}")
        print("\\nSUCCESS: Data imported to Railway production database!")
        
    except Exception as e:
        print(f"ERROR: {{e}}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()
'''
    
    return script_content

def main():
    print("=== Railway Database Import Guide ===")
    print()
    print("To fix the data visibility issue on your hosted app:")
    print()
    print("1. Get your DATABASE_URL from Railway:")
    print("   - Go to https://railway.app")
    print("   - Open your Londons Kitchen project")
    print("   - Click on PostgreSQL database")
    print("   - Copy the DATABASE_URL from 'Connect' tab")
    print()
    
    database_url = input("Enter DATABASE_URL: ").strip()
    if not database_url:
        print("ERROR: No DATABASE_URL provided")
        return
    
    # Fix postgres:// to postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # Create temporary import script
    print("Creating import script...")
    import_script = create_import_script(database_url)
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(import_script)
        temp_script = f.name
    
    print(f"Created temporary script: {temp_script}")
    print("Running import...")
    
    # Run the import
    os.system(f"python {temp_script}")
    
    # Clean up
    try:
        os.remove(temp_script)
    except:
        pass
    
    print()
    print("=== Alternative Methods ===")
    print("1. Railway Dashboard:")
    print("   - Go to Railway Dashboard > PostgreSQL > Query tab")
    print("   - Use railway_import.sql file")
    print()
    print("2. Railway CLI:")
    print("   - Install: npm install -g @railway/cli")
    print("   - Login: railway login")
    print("   - Run: railway run python import_simple.py")
    print()
    print("3. Manual script:")
    print("   - Run: python import_simple.py")
    print("   - Enter DATABASE_URL when prompted")

if __name__ == "__main__":
    main()