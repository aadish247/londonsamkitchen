#!/usr/bin/env python3
"""
Test database connection for Railway production database
"""
import os
from sqlalchemy import create_engine, text

# Test the DATABASE_URL environment variable
database_url = os.environ.get('DATABASE_URL')

if not database_url:
    print("❌ DATABASE_URL environment variable is NOT set!")
    print("Please set DATABASE_URL in Railway variables")
    print("Use: postgresql://postgres:aJxyryWChNKUztgJvTkasZIlOwidIdqr@shortline.proxy.rlwy.net:50512/railway")
    exit(1)

print(f"✅ DATABASE_URL found: {database_url}")

# Fix postgres:// to postgresql:// if needed
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

print("Testing database connection...")

try:
    engine = create_engine(database_url)
    with engine.connect() as conn:
        # Test connection
        result = conn.execute(text('SELECT 1'))
        print("✅ Database connection successful!")
        
        # Get table counts
        inv_count = conn.execute(text('SELECT COUNT(*) FROM investment')).scalar()
        exp_count = conn.execute(text('SELECT COUNT(*) FROM expense')).scalar()
        sale_count = conn.execute(text('SELECT COUNT(*) FROM sale')).scalar()
        
        print(f"📊 Database contains:")
        print(f"  Investments: {inv_count}")
        print(f"  Expenses: {exp_count}")
        print(f"  Sales: {sale_count}")
        
        if inv_count > 0 or exp_count > 0:
            print("🎉 Your data is in the database!")
            print("The web app should now display your entries.")
        else:
            print("⚠️ Database is empty - run the import script first")

except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("Check your DATABASE_URL and network connection")