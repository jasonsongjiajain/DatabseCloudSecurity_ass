# Group6 TT2L DatabseCloudSecurity_ass
1) Install Django and necessary package: pip install pipenv,
pipenv install django,
pipenv install mssql-django,
pipenv install pyodbc

2) Enter virtual environment: 
pipenv shell

3) Add a new database named TestDB: 
create a new database at SSMS named TestDB

4) Make migrations, migrate and runserver :
python manage.py makemigrations,
python manage.py migrate,
python manage.py runserver,

5) Enter Web, when runserver it will pop out a localhost and remember to add /login/ or /register behind the link to enter the page: 
Exp: http://127.0.0.1:8000/login/


