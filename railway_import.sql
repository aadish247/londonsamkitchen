-- Railway Database Import Script
-- Use this in Railway Dashboard > PostgreSQL > Query tab

-- Clear existing data
DELETE FROM investment;
DELETE FROM expense;
DELETE FROM sale;

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS investment (
    id SERIAL PRIMARY KEY,
    investor_name VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS expense (
    id SERIAL PRIMARY KEY,
    description VARCHAR(200) NOT NULL,
    amount FLOAT NOT NULL,
    date TIMESTAMP NOT NULL,
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS sale (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    date TIMESTAMP NOT NULL,
    description VARCHAR(200)
);

-- Sample data (replace with your actual data from local_data_export.json)
-- Investments
INSERT INTO investment (investor_name, amount, date) VALUES
('John Smith', 5000.00, '2024-01-15 10:00:00'),
('Jane Doe', 3000.00, '2024-01-20 14:30:00'),
('Mike Johnson', 2500.00, '2024-02-01 09:15:00'),
('Sarah Williams', 2912.00, '2024-02-10 16:45:00');

-- Expenses
INSERT INTO expense (description, amount, date, category) VALUES
('Food Supplies', 150.50, '2024-01-16 08:00:00', 'Food'),
('Equipment', 2000.00, '2024-01-17 10:00:00', 'Equipment'),
('Marketing', 300.00, '2024-01-18 14:00:00', 'Marketing'),
('Rent', 1500.00, '2024-02-01 00:00:00', 'Rent'),
('Utilities', 250.00, '2024-02-05 12:00:00', 'Utilities');

-- Sales
INSERT INTO sale (amount, date, description) VALUES
(450.00, '2024-01-25 12:00:00', 'Daily sales'),
(380.00, '2024-01-26 12:00:00', 'Daily sales'),
(520.00, '2024-02-05 12:00:00', 'Daily sales'),
(410.00, '2024-02-06 12:00:00', 'Daily sales');

-- Verify import
SELECT 'Investments' as table_name, COUNT(*) as count FROM investment
UNION ALL
SELECT 'Expenses' as table_name, COUNT(*) as count FROM expense
UNION ALL
SELECT 'Sales' as table_name, COUNT(*) as count FROM sale;