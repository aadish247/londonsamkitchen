#!/usr/bin/env python3
"""
Import data into production database from JSON export.
Run this script on Railway/Render after deployment to import your data.
"""

import json
import os
import sys
from datetime import datetime
from app import app, db, Investment, Expense, Sale

def import_data():
    """Import data from JSON file to production database"""
    
    # Check if data file exists
    DATA_FILE = 'local_data_export.json'
    if not os.path.exists(DATA_FILE):
        print(f"Data file {DATA_FILE} not found!")
        print("Please upload your exported data file first.")
        return
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    print(f"Importing data exported on: {data.get('exported_at', 'Unknown')}")
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to append)
        print("Clearing existing data...")
        Investment.query.delete()
        Expense.query.delete()
        Sale.query.delete()
        db.session.commit()
        
        # Import investments
        print(f"Importing {len(data['investments'])} investments...")
        for inv_data in data['investments']:
            investment = Investment(
                investor_name=inv_data['investor_name'],
                amount=float(inv_data['amount']),
                date=datetime.fromisoformat(inv_data['date'].replace('Z', '+00:00'))
            )
            db.session.add(investment)
        
        # Import expenses
        print(f"Importing {len(data['expenses'])} expenses...")
        for exp_data in data['expenses']:
            expense = Expense(
                description=exp_data['description'],
                amount=float(exp_data['amount']),
                category=exp_data['category'],
                date=datetime.fromisoformat(exp_data['date'].replace('Z', '+00:00'))
            )
            db.session.add(expense)
        
        # Import sales
        print(f"Importing {len(data['sales'])} sales...")
        for sale_data in data['sales']:
            sale = Sale(
                amount=float(sale_data['amount']),
                description=sale_data['description'],
                date=datetime.fromisoformat(sale_data['date'].replace('Z', '+00:00'))
            )
            db.session.add(sale)
        
        # Commit all changes
        db.session.commit()
        print("Data import completed successfully!")
        
        # Show summary
        total_investment = sum(inv.amount for inv in Investment.query.all())
        total_expenses = sum(exp.amount for exp in Expense.query.all())
        total_sales = sum(sale.amount for sale in Sale.query.all())
        
        print("\n=== Import Summary ===")
        print(f"Total Investment: £{total_investment:.2f}")
        print(f"Total Expenses: £{total_expenses:.2f}")
        print(f"Total Sales: £{total_sales:.2f}")
        print(f"Net Profit: £{total_sales - total_expenses:.2f}")

if __name__ == "__main__":
    import_data()