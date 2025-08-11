# Fix Railway Database Connection

## Problem
Your web app is not connecting to the Railway production database because the DATABASE_URL environment variable is not set.

## Solution - Set DATABASE_URL in Railway

### Method 1: Railway Dashboard (Recommended)
1. Go to https://railway.app
2. Open your project (courageous-fulfillment)
3. Click on your **web service** (not the database)
4. Go to **"Variables"** tab
5. Click **"New Variable"**
6. Name: `DATABASE_URL`
7. Value: `postgresql://postgres:aJxyryWChNKUztgJvTkasZIlOwidIdqr@shortline.proxy.rlwy.net:50512/railway`
8. Click **"Add"**
9. **Redeploy** your service (Railway will auto-redeploy)

### Method 2: Railway CLI
1. Open Command Prompt (cmd)
2. Navigate to project: `cd "c:\Users\Aadish\py\Londons Kitchen project"`
3. Run: `railway variables set DATABASE_URL=postgresql://postgres:aJxyryWChNKUztgJvTkasZIlOwidIdqr@shortline.proxy.rlwy.net:50512/railway`
4. Redeploy: `railway deploy`

### Method 3: Railway CLI (Alternative)
```bash
railway login
railway link
railway variables add DATABASE_URL postgresql://postgres:aJxyryWChNKUztgJvTkasZIlOwidIdqr@shortline.proxy.rlwy.net:50512/railway
```

## Verification Steps
After setting the variable:
1. Wait 2-3 minutes for deployment
2. Check your Railway dashboard - deployment should show "Success"
3. Visit your hosted app URL
4. Data should now appear!

## Quick Test
You can also test the connection by running:
```bash
railway run python -c "import os; print('DATABASE_URL:', os.environ.get('DATABASE_URL'))"
```

This should output your database connection string.