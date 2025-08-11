# Data Migration Guide

## Problem
Your deployed application doesn't have any data because the production database is empty. This guide will help you transfer your local data to the production environment.

## Current Status
✅ **Local Data Found**: 
- 4 investments totaling £13,412
- 60 expenses totaling £2,486.47
- 0 sales recorded

## Solution: Two Methods

### Method 1: JSON Data Import (Recommended)

#### Step 1: Export Local Data (Already Done)
Your data has been exported to `local_data_export.json` containing all investments and expenses.

#### Step 2: Import to Production

**Option A: Using Railway Console**
1. Go to your Railway project dashboard
2. Click on your deployed service
3. Go to "Deployments" tab
4. Click on the active deployment
5. Go to "Shell" tab
6. Upload the `local_data_export.json` file using the file upload feature
7. Run: `python import_production_data.py`

**Option B: Using Railway CLI**
```bash
# Install Railway CLI if not already done
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Upload data file
railway upload local_data_export.json

# Run import script
railway run python import_production_data.py
```

### Method 2: Manual Data Entry (Alternative)
Use the web interface to manually enter data:
1. Visit your deployed application URL
2. Use the Investments, Expenses, and Sales pages to add data
3. Use the Export feature to verify data integrity

## Verification Steps

After importing, verify your data:

1. **Check Dashboard**: Visit your deployed app's dashboard
2. **Verify Totals**: Ensure totals match your local data:
   - Total Investment: £13,412.00
   - Total Expenses: £2,486.47
   - Net Position: £10,925.53

3. **Test Export**: Use the "Export to Excel" feature to verify all data is present

## Troubleshooting

### Common Issues

**Import Script Not Found**
```bash
# Ensure you're in the correct directory
pwd
# Should show: /app

# Check if files exist
ls -la *.json *.py
```

**Database Connection Issues**
- Railway automatically provides `DATABASE_URL` environment variable
- No manual database configuration needed

**Data Format Issues**
- The JSON format is automatically compatible between environments
- All date formats are ISO standard

### Getting Help

If you encounter issues:
1. Check Railway logs in the dashboard
2. Use the Railway shell to debug
3. Re-run the import script if needed

## Excel Export Issue

The "Excel sheet not proper" issue is likely because:
1. **Empty Database**: Production has no data, so Excel export is empty
2. **Production Environment**: Excel formatting is disabled in production for compatibility

After data import, the Excel export will work correctly and include all your data with proper formatting.

## Quick Start Commands

```bash
# On Railway Shell:
cd /app
python import_production_data.py

# Verify data:
curl -X GET https://your-app.railway.app/
```

## Support

For issues with data migration, check:
- Railway deployment logs
- Application logs in Railway dashboard
- Verify `local_data_export.json` contains expected data