import pandas as pd
from helper_functions import get_1month, get_tickers, connect_postgres, connect_sqlalchemy
from datetime import date

def check_date():
    if date.today().day == 1:
        get_1month_data()
    else:
        pass

def get_1month_data():

    # list of currency pairs
    currency_tickers = get_tickers()

    # Declaring the dataframes
    df_1month = pd.DataFrame()

    # Assigning values inside the dataframes
    list_1month = [get_1month(ticker) for ticker in currency_tickers]
    df_1month = df_1month.append(list_1month,ignore_index=True)
    df_1month['Timeframe']='1month'

    # Move dataframes to Postgres
    engine = connect_sqlalchemy()
    df_1month.to_sql('temp_monthly', con=engine, index=False, if_exists='append',chunksize = 1000)

    upsert_conn = connect_postgres()
    upsert_cursor = upsert_conn.cursor()
    insert_query = """Insert into forex_monthly(ticker,date,open,high,low,close,adj_close,volume,timeframe)
    select * from temp_monthly
    on conflict (ticker, date)
    do update set
    ticker = EXCLUDED.ticker,
    date = EXCLUDED.date,
    open = EXCLUDED.open,
    high = EXCLUDED. high,
    low = EXCLUDED.low,
    close = EXCLUDED.close,
    adj_close = EXCLUDED.adj_close,
    volume = EXCLUDED.volume,
    timeframe = EXCLUDED.timeframe;"""

    upsert_cursor.execute(insert_query)
    upsert_cursor.execute("DROP TABLE IF EXISTS temp_monthly;")
    upsert_conn.close()
