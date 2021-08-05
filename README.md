# YFinance-Data-Extraction
Used yfinance library in Python to extract data from Yahoo Finance in real time.

## Run the scripts
To run the scripts, update the scripts as follows:<br>
1. In helper_function.py,
    In **def connect_postgres()**
      <p>dbname=DATABASENAME user=USERNAME password=PASSWORD</p>
    Replace
    DATABASENAME with your databasename
    USERNAME with the your postgres username 
    PASSWORD with your postgres database password
    
    In**def connect_sqlalchemy()**
      postgresql+psycopg2://USERNAME:PASSWORD@HOST:PORT/DATABASENAME
    Replace
    USERNAME with your postgres username
    PASSWORD with your postgres database password
    HOST with the database host
    PORT with the database port
    DATABASENAME with your database name
  Host and port can be found by doing a right click on the server name, select Properties, got to ‘Connection’ tab.
  
 2. Ensure that all the python files are stored in one place
 3. Run schedule_data.py
    This python file will start the scheduler and call the necessary files when required

