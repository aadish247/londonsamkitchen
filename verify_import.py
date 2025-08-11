#!/usr/bin/env python3
"""
Verify the data import to Railway production database
"""
from sqlalchemy import create_engine, text

# Use the provided DATABASE_URL
DATABASE_URL = "postgresql://postgres:aJxyryWChNKUztgJvTkasZIlOwidIdqr@shortline.proxy.rlwy.net:50512/railway"

print("=== Verifying Railway Production Database ===")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Get counts
    inv_count = conn.execute(text('SELECT COUNT(*) FROM investment')).scalar()
    exp_count = conn.execute(text('SELECT COUNT(*) FROM expense')).scalar()
    sale_count = conn.execute(text('SELECT COUNT(*) FROM sale')).scalar()
    
    print(f"Total Investments: {inv_count}")
    print(f"Total Expenses: {exp_count}")
    print(f"Total Sales: {sale_count}")
    
    # Show sample data
    print("\n=== Sample Investments ===")
    inv_results = conn.execute(text('SELECT * FROM investment ORDER BY id LIMIT 3')).fetchall()
    for inv in inv_results:
        print(f"ID: {inv[0]}, Investor: {inv[1]}, Amount: £{inv[2]}, Date: {inv[3]}")
    
    print("\n=== Sample Expenses ===")
    exp_results = conn.execute(text('SELECT * FROM expense ORDER BY id LIMIT 3')).fetchall()
    for exp in exp_results:
        print(f"ID: {exp[0]}, Description: {exp[1]}, Amount: £{exp[2]}, Date: {exp[3]}, Category: {exp[4]}")
    
    print("\n=== Sample Sales ===")
    sale_results = conn.execute(text('SELECT * FROM sale ORDER BY id LIMIT 3')).fetchall()
    for sale in sale_results:
        print(f"ID: {sale[0]}, Amount: £{sale[1]}, Date: {sale[2]}, Description: {sale[3]}")

print("\n✅ Database verification complete!")
print("Your hosted app should now display this data.")