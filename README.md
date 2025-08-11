# London's Kitchen Financial Management System

A web-based financial management system for London's Kitchen food truck business. This application helps track investments, expenses, sales, and calculate profit/loss statements.

## Features

- Track investments from partners (Adwait and Shree)
- Record and categorize expenses
- Track daily sales
- View financial dashboard with:
  - Total investments
  - Total expenses
  - Total sales
  - Net profit/loss
  - Investment shares calculation

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Deployment to Railway

### Prerequisites
- A Railway account
- Git installed on your local machine

### Deployment Steps

1. **Push your code to a Git repository**
   - Create a repository on GitHub, GitLab, or any other Git provider
   - Push your code to the repository

2. **Deploy to Railway**
   - Log in to your Railway account
   - Create a new project
   - Connect your Git repository
   - Railway will automatically detect the Dockerfile and deploy your application

3. **Environment Variables**
   - Set the following environment variables in Railway:
     - `RAILWAY_ENVIRONMENT=production`

### Troubleshooting

If you encounter the `numpy.dtype size changed` error:
- The application has been configured to handle this by using compatible versions of numpy and pandas
- The Dockerfile and entrypoint script ensure the correct versions are installed

## Features

### Dashboard
- View total investments, expenses, and sales
- Calculate net profit/loss
- See investment shares distribution

### Investments
- Add new investments
- View investment history
- Track individual partner contributions

### Expenses
- Add new expenses with categories
- Track setup costs and monthly expenses
- Record salary expenses

### Sales
- Record daily sales
- Add optional descriptions
- View sales history

## Production Deployment

### Option 1: Railway.app (Recommended)

1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Deploy automatically - Railway will detect the required files:
   - `requirements.txt` - Python dependencies
   - `Procfile` - Application startup command
   - `runtime.txt` - Python version specification
4. Add environment variables in Railway dashboard:
   - `DATABASE_URL`: PostgreSQL connection string (automatically provided)
   - `SECRET_KEY`: Generate a secure random string

### Option 2: Render.com

1. Create account at [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Add environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: Generate a secure random string

### Option 3: PythonAnywhere

1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files via Git or manual upload
3. Configure web app settings
4. Set virtual environment and requirements

## Environment Variables

Create a `.env` file for local development:
```
DATABASE_URL=sqlite:///food_truck.db
SECRET_KEY=your-secret-key-here
```

For production deployment, set these variables in your hosting platform:
- `DATABASE_URL`: PostgreSQL database URL (automatically provided by Railway/Render)
- `SECRET_KEY`: Generate a secure random string (use `secrets.token_hex(32)`)
- `PORT`: Port number (automatically set by hosting platforms)

## Files Required for Deployment

Your repository should include these files:
- `requirements.txt` - Python dependencies including gunicorn
- `Procfile` - Application startup command (`web: gunicorn app:app`)
- `runtime.txt` - Python version specification (`python-3.11.0`)
- `.gitignore` - Exclude sensitive files from version control

## Quick Start for Deployment

1. **Push to GitHub**: Ensure all files are committed and pushed
2. **Connect Repository**: Link your GitHub repo to Railway/Render
3. **Deploy**: Click deploy - the platform will handle the rest
4. **Set Environment Variables**: Add SECRET_KEY in the platform dashboard
5. **Verify**: Visit the provided URL to test the deployment

## Technologies Used

- Flask (Python web framework)
- SQLite (Database)
- HTML/CSS
- JavaScript
