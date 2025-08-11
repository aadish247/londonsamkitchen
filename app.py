from flask import Flask, render_template, request, jsonify, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pandas as pd
import os
import calendar
import io

app = Flask(__name__)

# Use DATABASE_URL for production, fallback to SQLite for local development
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Handle Railway/Render database URL format
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_truck.db'

# Use environment variable for secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
db = SQLAlchemy(app)


class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investor_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(100))


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(200))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    total_investment = sum(inv.amount for inv in Investment.query.all())
    total_expenses = sum(exp.amount for exp in Expense.query.all())
    total_sales = sum(sale.amount for sale in Sale.query.all())

    investment_count = Investment.query.count()
    expense_count = Expense.query.count()
    sale_count = Sale.query.count()

    return render_template('index.html',
                           total_investment=total_investment,
                           total_expenses=total_expenses,
                           total_sales=total_sales,
                           investment_count=investment_count,
                           expense_count=expense_count,
                           sale_count=sale_count)


@app.route('/investments')
def investments():
    investments = Investment.query.order_by(Investment.date.desc()).all()
    total_investment = sum(inv.amount for inv in investments)
    return render_template('investments.html', investments=investments, total=total_investment)


@app.route('/add_investment', methods=['POST'])
def add_investment():
    data = request.json
    new_investment = Investment(
        investor_name=data['investor_name'],
        amount=float(data['amount']),
        date=datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(new_investment)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/expenses')
def expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_expenses = sum(exp.amount for exp in expenses)
    return render_template('expenses.html', expenses=expenses, total=total_expenses)


@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    new_expense = Expense(
        description=data['description'],
        amount=float(data['amount']),
        category=data['category'],
        date=datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/sales')
def sales():
    sales = Sale.query.order_by(Sale.date.desc()).all()
    total_sales = sum(sale.amount for sale in sales)
    return render_template('sales.html', sales=sales, total=total_sales)


@app.route('/add_sale', methods=['POST'])
def add_sale():
    data = request.json
    new_sale = Sale(
        amount=float(data['amount']),
        description=data['description'],
        date=datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/delete_investment/<int:id>', methods=['POST'])
def delete_investment(id):
    investment = Investment.query.get_or_404(id)
    db.session.delete(investment)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/delete_expense/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/delete_sale/<int:id>', methods=['POST'])
def delete_sale(id):
    sale = Sale.query.get_or_404(id)
    db.session.delete(sale)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/edit_investment/<int:id>', methods=['GET', 'POST'])
def edit_investment(id):
    investment = Investment.query.get_or_404(id)

    if request.method == 'POST':
        data = request.json
        investment.investor_name = data['investor_name']
        investment.amount = float(data['amount'])
        investment.date = datetime.strptime(data['date'], '%Y-%m-%d')
        db.session.commit()
        return jsonify({'status': 'success'})

    return jsonify({
        'id': investment.id,
        'investor_name': investment.investor_name,
        'amount': investment.amount,
        'date': investment.date.strftime('%Y-%m-%d')
    })


@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':
        data = request.json
        expense.description = data['description']
        expense.amount = float(data['amount'])
        expense.category = data['category']
        expense.date = datetime.strptime(data['date'], '%Y-%m-%d')
        db.session.commit()
        return jsonify({'status': 'success'})

    return jsonify({
        'id': expense.id,
        'description': expense.description,
        'amount': expense.amount,
        'category': expense.category,
        'date': expense.date.strftime('%Y-%m-%d')
    })


@app.route('/edit_sale/<int:id>', methods=['GET', 'POST'])
def edit_sale(id):
    sale = Sale.query.get_or_404(id)

    if request.method == 'POST':
        data = request.json
        sale.description = data['description']
        sale.amount = float(data['amount'])
        sale.date = datetime.strptime(data['date'], '%Y-%m-%d')
        db.session.commit()
        return jsonify({'status': 'success'})

    return jsonify({
        'id': sale.id,
        'description': sale.description,
        'amount': sale.amount,
        'date': sale.date.strftime('%Y-%m-%d')
    })


@app.route('/export_data')
def export_data():
    try:
        # Create a buffer to store the Excel file
        output = io.BytesIO()

        # Check if we're in production environment (Railway)
        is_production = os.environ.get('RAILWAY_ENVIRONMENT') == 'production'

        # Create Excel writer with formatting
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            workbook = writer.book

            # Export Investments with formatting
            investments = Investment.query.all()
            inv_data = [{
                'Date': i.date.strftime('%Y-%m-%d'),
                'Investor': i.investor_name,
                'Amount': i.amount
            } for i in investments]

            inv_df = pd.DataFrame(inv_data)
            inv_df.to_excel(writer, sheet_name='Investments', index=False)

            # Only apply formatting in development environment to avoid potential issues
            if not is_production:
                # Format Investment sheet
                inv_sheet = writer.sheets['Investments']
                for col in ['A', 'B', 'C']:
                    inv_sheet.column_dimensions[col].width = 15
                inv_sheet.column_dimensions['B'].width = 12

                # Apply currency format to Amount column
                for row in range(2, len(inv_data) + 2):
                    inv_sheet[f'C{row}'].number_format = '"£"#,##0.00'

        # Export Expenses with formatting
        expenses = Expense.query.all()
        exp_data = [{
            'Date': e.date.strftime('%Y-%m-%d'),
            'Description': e.description,
            'Category': e.category,
            'Amount': e.amount
        } for e in expenses]

        exp_df = pd.DataFrame(exp_data)
        exp_df.to_excel(writer, sheet_name='Expenses', index=False)

        # Only apply formatting in development environment
        if not is_production:
            # Format Expense sheet
            exp_sheet = writer.sheets['Expenses']
            exp_sheet.column_dimensions['A'].width = 12
            exp_sheet.column_dimensions['B'].width = 30
            exp_sheet.column_dimensions['C'].width = 15
            exp_sheet.column_dimensions['D'].width = 12

            # Apply currency format to Amount column
            for row in range(2, len(exp_data) + 2):
                exp_sheet[f'D{row}'].number_format = '"£"#,##0.00'

        # Export Sales with formatting
        sales = Sale.query.all()
        sales_data = [{
            'Date': s.date.strftime('%Y-%m-%d'),
            'Description': s.description,
            'Amount': s.amount
        } for s in sales]

        sales_df = pd.DataFrame(sales_data)
        sales_df.to_excel(writer, sheet_name='Sales', index=False)

        # Only apply formatting in development environment
        if not is_production:
            # Format Sales sheet
            sales_sheet = writer.sheets['Sales']
            sales_sheet.column_dimensions['A'].width = 12
            sales_sheet.column_dimensions['B'].width = 30
            sales_sheet.column_dimensions['C'].width = 12

            # Apply currency format to Amount column
            for row in range(2, len(sales_data) + 2):
                sales_sheet[f'C{row}'].number_format = '"£"#,##0.00'

        # Create enhanced Summary sheet
        total_investment = sum(i.amount for i in investments)
        total_expenses = sum(e.amount for e in expenses)
        total_sales = sum(s.amount for s in sales)
        net_profit = total_sales - total_expenses

        # Calculate investment shares
        shree_investment = sum(
            i.amount for i in investments if i.investor_name == 'Shree')
        adwait_investment = sum(
            i.amount for i in investments if i.investor_name == 'Adwait')

        summary_data = [
            ['London\'s Kitchen Financial Summary', ''],
            ['', ''],
            ['Summary Overview', ''],
            ['Total Investment', total_investment],
            ['Total Expenses', total_expenses],
            ['Total Sales', total_sales],
            ['Net Profit/Loss', net_profit],
            ['', ''],
            ['Investment Breakdown', ''],
            ['Adwait\'s Investment', adwait_investment],
            ['Shree\'s Investment', shree_investment],
            ['', ''],
            ['Profit Sharing (Based on Investment)', ''],
            ['Adwait\'s Share %',
                f"{(adwait_investment/total_investment*100):.1f}%" if total_investment > 0 else "0%"],
            ['Shree\'s Share %',
                f"{(shree_investment/total_investment*100):.1f}%" if total_investment > 0 else "0%"],
            ['', ''],
            ['Adwait\'s Profit Share',
                f"£{net_profit * (adwait_investment/total_investment):,.2f}" if total_investment > 0 else "£0.00"],
            ['Shree\'s Profit Share',
                f"£{net_profit * (shree_investment/total_investment):,.2f}" if total_investment > 0 else "£0.00"]
        ]

        summary_df = pd.DataFrame(summary_data, columns=['Category', 'Amount'])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Only apply formatting in development environment
        if not is_production:
            # Format Summary sheet
            summary_sheet = writer.sheets['Summary']
            summary_sheet.column_dimensions['A'].width = 35
            summary_sheet.column_dimensions['B'].width = 20

            # Apply formatting to Summary sheet
            from openpyxl.styles import Font
            summary_sheet['A1'].font = Font(bold=True, size=14)
            summary_sheet['A3'].font = Font(bold=True, size=12)
            summary_sheet['A9'].font = Font(bold=True, size=12)
            summary_sheet['A13'].font = Font(bold=True, size=12)

            # Apply currency format to amount columns
            currency_rows = [4, 5, 6, 7, 10, 11, 17, 18]
            for row in currency_rows:
                summary_sheet[f'B{row}'].number_format = '"£"#,##0.00'

        output.seek(0)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'London_Kitchen_Financial_Report_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
        )
    except Exception as e:
        app.logger.error(f"Error in export_data: {str(e)}")
        flash(f"Error exporting data: {str(e)}", "error")
        return render_template('error.html', error=str(e))


@app.route('/dashboard')
def dashboard():
    total_investment = sum(inv.amount for inv in Investment.query.all())
    total_expenses = sum(exp.amount for exp in Expense.query.all())
    total_sales = sum(sale.amount for sale in Sale.query.all())
    net_profit_loss = total_sales - total_expenses

    # Calculate shares
    investments = Investment.query.all()
    shree_total = sum(
        i.amount for i in investments if i.investor_name == 'Shree')
    adwait_total = sum(
        i.amount for i in investments if i.investor_name == 'Adwait')

    # Get recent activity (last 10 items)
    recent_expenses = Expense.query.order_by(
        Expense.date.desc()).limit(5).all()
    recent_sales = Sale.query.order_by(Sale.date.desc()).limit(5).all()
    
    # Monthly sales analysis for the current year
    current_year = datetime.now().year
    monthly_sales = []
    monthly_expenses = []
    
    for month in range(1, 13):
        start_date = datetime(current_year, month, 1)
        if month == 12:
            end_date = datetime(current_year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(current_year, month + 1, 1) - timedelta(days=1)
            
        month_sales = Sale.query.filter(Sale.date >= start_date, Sale.date <= end_date).all()
        month_expenses = Expense.query.filter(Expense.date >= start_date, Expense.date <= end_date).all()
        
        monthly_sales.append({
            'month': calendar.month_name[month],
            'total': sum(sale.amount for sale in month_sales),
            'count': len(month_sales)
        })
        
        monthly_expenses.append({
            'month': calendar.month_name[month],
            'total': sum(expense.amount for expense in month_expenses),
            'count': len(month_expenses)
        })

    return render_template('dashboard.html',
                           total_investment=total_investment,
                           total_expenses=total_expenses,
                           total_sales=total_sales,
                           net_profit_loss=net_profit_loss,
                           adwait_investment=adwait_total,
                           shree_investment=shree_total,
                           recent_expenses=recent_expenses,
                           recent_sales=recent_sales,
                           monthly_sales=monthly_sales,
                           monthly_expenses=monthly_expenses,
                           current_year=current_year)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
