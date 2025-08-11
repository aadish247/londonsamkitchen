#!/usr/bin/env python3
"""
Export data from local SQLite database to JSON format for production import.
Run this script locally to backup your data before deploying.
"""

import json
import sqlite3
import os
from datetime import datetime

# Path to local database
DB_PATH = os.path.join('instance', 'food_truck.db')

# Output file for exported data
EXPORT_FILE = 'local_data_export.json'

def export_data():
    """Export all data from local database to JSON"""
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    data = {
        'exported_at': datetime.now().isoformat(),
        'investments': [],
        'expenses': [],
        'sales': []
    }
    
    # Export investments
    cursor.execute("SELECT * FROM investment ORDER BY date")
    for row in cursor.fetchall():
        data['investments'].append({
            'investor_name': row['investor_name'],
            'amount': row['amount'],
            'date': row['date']
        })
    
    # Export expenses
    cursor.execute("SELECT * FROM expense ORDER BY date")
    for row in cursor.fetchall():
        data['expenses'].append({
            'description': row['description'],
            'amount': row['amount'],
            'category': row['category'],
            'date': row['date']
        })
    
    # Export sales
    cursor.execute("SELECT * FROM sale ORDER BY date")
    for row in cursor.fetchall():
        data['sales'].append({
            'amount': row['amount'],
            'description': row['description'],
            'date': row['date']
        })
    
    # Write to JSON file
    with open(EXPORT_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    conn.close()
    
    print(f"Data exported successfully to {EXPORT_FILE}")
    print(f"Investments: {len(data['investments'])}")
    print(f"Expenses: {len(data['expenses'])}")
    print(f"Sales: {len(data['sales'])}")

if __name__ == "__main__":
    export_data()