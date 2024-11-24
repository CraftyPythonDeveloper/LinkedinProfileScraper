@echo off
set "anaconda_path=C:\Users\%USERNAME%\Anaconda3\Scripts"
set "project_folder=linkedinScraper"
set "Venvironment=linkedin_scraper"
call %anaconda_path%\activate.bat base
echo What is your database server host name?
set /p SERVER_NAME=
echo Enter a database name in which data needs to be stored..
echo Please make sure that database is already created..
set /p DATABASE_NAME=
del %project_folder%\settings.py
copy %project_folder%\settings.back %project_folder%\settings.py
echo. >> %project_folder%\settings.py
echo.params = quote_plus("DRIVER={SQL Server Native Client 11.0};" >> %project_folder%\settings.py
echo.                    "SERVER=%SERVER_NAME%;" >> %project_folder%\settings.py
echo.                    "DATABASE=%DATABASE_NAME%;" >> %project_folder%\settings.py
echo.                    "Trusted_Connection=yes;") >> %project_folder%\settings.py
echo. >> %project_folder%\settings.py
echo.SQL_CONNECTION_STRING = "mssql+pyodbc:///?odbc_connect={}".format(params) >> %project_folder%\settings.py
call conda create --name=%Venvironment% python=3.8 -y
call conda activate %Venvironment%
pip install -r requirements.txt
echo Installation and configuration complete..
pause