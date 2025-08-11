@echo off
echo Adding psycopg2-binary to requirements.txt...
echo psycopg2-binary==2.9.7 >> requirements.txt

echo Adding changes to git...
git add requirements.txt
git commit -m "Add psycopg2-binary for PostgreSQL support"
git push

echo Changes pushed! Railway should automatically rebuild and deploy.
echo You can check the Railway dashboard for deployment status.
pause