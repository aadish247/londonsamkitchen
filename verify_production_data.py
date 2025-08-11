#!/usr/bin/env python3
"""
Verification script to check if data exists in the production database
"""
import os
import sys
from app import app, db, Investment, Expense, Sale

def verify_data():
    """Verify data in production database"""
    with app.app_context():
        print("=== Production Database Verification ===")
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        
        # Count records
        investment_count = Investment.query.count()
        expense_count = Expense.query.count()
        sale_count = Sale.query.count()
        
        print(f"Investments: {investment_count}")
        print(f"Expenses: {expense_count}")
        print(f"Sales: {sale_count}")
        
        if investment_count > 0:
            print("\n=== First 3 Investments ===")
            investments = Investment.query.limit(3).all()
            for inv in investments:
                print(f"- {inv.investor_name}: £{inv.amount} on {inv.date}")
        
        if expense_count > 0:
            print("\n=== First 3 Expenses ===")
            expenses = Expense.query.limit(3).all()
            for exp in expenses:
                print(f"- {exp.description}: £{exp.amount} on {exp.date}")
        
        if sale_count > 0:
            print("\n=== First 3 Sales ===")
            sales = Sale.query.limit(3).all()
            for sale in sales:
                print(f"- £{sale.amount} on {sale.date}")

if __name__ == "__main__":
    verify_data()