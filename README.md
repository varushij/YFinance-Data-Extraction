# YFinance-Data-Extraction
Used yfinance library in Python to extract data from Yahoo Finance in real time.

## Run the scripts
To run the scripts, update the scripts as follows:<br>
1. In helper_function.py, <br>
    In **def connect_postgres()**<br>
      dbname=DATABASENAME user=USERNAME password=PASSWORD<br>
    **Replace**<br>
    DATABASENAME with your databasename<br>
    USERNAME with the your postgres username <br>
    PASSWORD with your postgres database password<br>
    
    In **def connect_sqlalchemy()**<br>
      postgresql+psycopg2://USERNAME:PASSWORD@HOST:PORT/DATABASENAME<br>
    **Replace**<br>
    **USERNAME* with your postgres username<br>
    **PASSWORD** with your postgres database password<br>
    **HOST** with the database host<br>
    **PORT** with the database port<br>
    **DATABASENAME** with your database name<br>
  Host and port can be found by doing a right click on the server name, select Properties, got to ‘Connection’ tab.<br>
  
 2. Ensure that all the python files are stored in one place
 3. Run schedule_data.py
    This python file will start the scheduler and call the necessary files when required

